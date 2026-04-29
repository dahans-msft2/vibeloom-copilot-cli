#!/usr/bin/env node
// Render site/og-image-source.html to site/public/og-image.png at 1200x630.
//
// Why this exists: chrome --headless --screenshot doesn't reliably wait for
// web fonts before capturing, so we drive Chrome via the DevTools Protocol
// instead, set explicit device metrics, await document.fonts.ready, then
// capture. Output PNG matches the dev-server preview exactly.
//
// Usage: node site/scripts/render-og-image.cjs
//   - assumes the site dev server is running on http://localhost:8123
//     (npx http-server site/public -p 8123 -c-1)
//   - requires the `ws` npm package; auto-installs to /tmp if missing.

const { spawn, execSync } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const REPO_ROOT = path.resolve(__dirname, '..', '..');
const SOURCE = path.join(REPO_ROOT, 'site', 'og-image-source.html');
const OUT = path.join(REPO_ROOT, 'site', 'public', 'og-image.png');
const DEBUG_TMP = path.join(REPO_ROOT, 'site', 'public', '_og-debug.html');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const DEV_URL = 'http://localhost:8123/_og-debug.html';
const DEBUG_PORT = 9333;

// Ensure ws is available.
let WebSocket;
try {
  WebSocket = require('ws');
} catch {
  execSync('cd /tmp && npm install ws --silent', { stdio: 'ignore' });
  WebSocket = require(require.resolve('ws', { paths: ['/tmp/node_modules'] }));
}

// Copy source into public/ so the dev server can serve it (font caching, etc.)
fs.copyFileSync(SOURCE, DEBUG_TMP);

const child = spawn(CHROME, [
  '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-sandbox',
  `--remote-debugging-port=${DEBUG_PORT}`,
  '--user-data-dir=/tmp/chrome-og-render',
], { stdio: 'ignore' });

function httpGet(p) {
  return new Promise((resolve, reject) => {
    http.get(`http://127.0.0.1:${DEBUG_PORT}${p}`, res => {
      let d = '';
      res.on('data', x => d += x);
      res.on('end', () => resolve(d));
    }).on('error', reject);
  });
}

async function send(ws, method, params) {
  return new Promise((resolve, reject) => {
    const id = Math.floor(Math.random() * 1e9);
    const onmsg = data => {
      const m = JSON.parse(data);
      if (m.id === id) {
        ws.removeListener('message', onmsg);
        m.error ? reject(new Error(m.error.message)) : resolve(m.result);
      }
    };
    ws.on('message', onmsg);
    ws.send(JSON.stringify({ id, method, params: params || {} }));
  });
}

(async () => {
  try {
    await new Promise(r => setTimeout(r, 1500));
    const tabs = JSON.parse(await httpGet('/json'));
    const tab = tabs.find(t => t.type === 'page') || tabs[0];

    const ws = new WebSocket(tab.webSocketDebuggerUrl);
    await new Promise(r => ws.once('open', r));

    await send(ws, 'Page.enable');
    await send(ws, 'Emulation.setDeviceMetricsOverride', {
      width: 1200, height: 630, deviceScaleFactor: 1, mobile: false,
    });
    await send(ws, 'Page.navigate', { url: DEV_URL });

    // Wait for navigation + font load.
    await new Promise(r => setTimeout(r, 4500));

    const sanity = await send(ws, 'Runtime.evaluate', {
      expression: `(async()=>{
        await document.fonts.ready;
        const b = document.querySelector('.bottom').getBoundingClientRect();
        return { fonts: document.fonts.size, bottomBottom: b.bottom };
      })()`,
      awaitPromise: true,
      returnByValue: true,
    });
    console.log('debug:', JSON.stringify(sanity.result?.value));

    const shot = await send(ws, 'Page.captureScreenshot', {
      format: 'png',
      captureBeyondViewport: false,
      clip: { x: 0, y: 0, width: 1200, height: 630, scale: 1 },
    });
    fs.writeFileSync(OUT, Buffer.from(shot.data, 'base64'));
    const stat = fs.statSync(OUT);
    console.log(`wrote ${OUT} — ${stat.size} bytes`);

    ws.close();
  } finally {
    try { fs.unlinkSync(DEBUG_TMP); } catch {}
    child.kill();
  }
  process.exit(0);
})().catch(e => {
  console.error(e);
  try { fs.unlinkSync(DEBUG_TMP); } catch {}
  child.kill();
  process.exit(1);
});
