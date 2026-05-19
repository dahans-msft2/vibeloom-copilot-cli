<#
.SYNOPSIS
    Installs the dev-team-pack into a target repository.

.DESCRIPTION
    Copies the autonomous AI development team (agents, skills, state-lib, docs,
    issue template) from vibeloom-copilot-cli into a target project.

    Run this script from the vibeloom-copilot-cli root directory.

.PARAMETER Target
    Required. Absolute or relative path to the target git repository.

.PARAMETER Update
    If set, overwrites existing team files in the target (upgrade mode).
    Your state.db and audit/ are always preserved.

.EXAMPLE
    # Fresh install
    .\dev-team-pack\install.ps1 -Target C:\GitHub-Repos\my-project

    # Upgrade after pulling vibeloom-copilot-cli changes
    .\dev-team-pack\install.ps1 -Target C:\GitHub-Repos\my-project -Update
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$Target,

    [switch]$Update
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ── Helpers ──────────────────────────────────────────────────────────────────

function Write-Step([string]$msg) { Write-Host "  → $msg" -ForegroundColor Cyan }
function Write-Ok([string]$msg)   { Write-Host "  ✓ $msg" -ForegroundColor Green }
function Write-Warn([string]$msg) { Write-Host "  ⚠ $msg" -ForegroundColor Yellow }
function Fail([string]$msg)       { Write-Host "  ✗ $msg" -ForegroundColor Red; exit 1 }

function Copy-TeamDir([string]$src, [string]$dst, [bool]$overwrite) {
    if (-not (Test-Path $src)) { Fail "Source not found: $src" }
    New-Item -ItemType Directory -Path $dst -Force | Out-Null
    Get-ChildItem -Recurse -File -Path $src | ForEach-Object {
        $rel = $_.FullName.Substring($src.Length).TrimStart('\','/')
        $dest = Join-Path $dst $rel
        New-Item -ItemType Directory -Path (Split-Path $dest) -Force | Out-Null
        if ($overwrite -or -not (Test-Path $dest)) {
            Copy-Item -LiteralPath $_.FullName -Destination $dest -Force
        }
    }
}

function Copy-TeamFile([string]$src, [string]$dst, [bool]$overwrite) {
    if (-not (Test-Path $src)) { Fail "Source not found: $src" }
    New-Item -ItemType Directory -Path (Split-Path $dst) -Force | Out-Null
    if ($overwrite -or -not (Test-Path $dst)) {
        Copy-Item -LiteralPath $src -Destination $dst -Force
    }
}

function Add-GitignoreRule([string]$repoRoot, [string]$rule) {
    $gi = Join-Path $repoRoot ".gitignore"
    if (Test-Path $gi) {
        $content = Get-Content $gi -Raw
        if ($content -notmatch [regex]::Escape($rule)) {
            Add-Content -Path $gi -Value "`n$rule"
        }
    }
}

# ── Resolve paths ─────────────────────────────────────────────────────────────

$source = (Get-Item -LiteralPath $PSScriptRoot).Parent.FullName
$targetPath = (Resolve-Path $Target -ErrorAction SilentlyContinue)?.Path
if (-not $targetPath) {
    # Target might not be resolved yet if it doesn't exist — check parent
    $targetPath = $Target
    if (-not (Test-Path (Split-Path $targetPath))) {
        Fail "Target parent directory does not exist: $Target"
    }
}
$targetPath = $targetPath.TrimEnd('\','/')

Write-Host ""
Write-Host "dev-team-pack installer" -ForegroundColor White
Write-Host "  Source : $source"
Write-Host "  Target : $targetPath"
Write-Host "  Mode   : $(if ($Update) { 'Update (overwrite team files)' } else { 'Fresh install' })"
Write-Host ""

# ── Validations ───────────────────────────────────────────────────────────────

if ($targetPath -eq $source) {
    Fail "Target is the same as source (vibeloom-copilot-cli). Choose a different project."
}

if (-not (Test-Path (Join-Path $targetPath ".git"))) {
    Fail "Target does not appear to be a git repository (no .git directory found)."
}

$versionFile = Join-Path $targetPath ".agent-state\VERSION"
if ((Test-Path $versionFile) -and -not $Update) {
    Write-Warn "dev-team-pack is already installed in this project."
    Write-Warn "Use -Update to overwrite team files, or run as-is to skip."
    $confirm = Read-Host "Continue anyway? (y/N)"
    if ($confirm -ne 'y') { Write-Host "Aborted."; exit 0 }
}

$overwrite = [bool]$Update

# ── Install agents ────────────────────────────────────────────────────────────

Write-Step "Installing agents..."
Copy-TeamDir `
    (Join-Path $source ".github\agents") `
    (Join-Path $targetPath ".github\agents") `
    $overwrite
Write-Ok "agents installed"

# ── Install skills ────────────────────────────────────────────────────────────

Write-Step "Installing skills..."
Copy-TeamDir `
    (Join-Path $source ".github\skills") `
    (Join-Path $targetPath ".github\skills") `
    $overwrite
Write-Ok "skills installed"

# ── Install issue template ────────────────────────────────────────────────────

Write-Step "Installing issue template..."
Copy-TeamFile `
    (Join-Path $source ".github\ISSUE_TEMPLATE\agent-blocker.md") `
    (Join-Path $targetPath ".github\ISSUE_TEMPLATE\agent-blocker.md") `
    $overwrite
Write-Ok "issue template installed"

# ── Install agent docs ────────────────────────────────────────────────────────

Write-Step "Installing agent docs..."
Copy-TeamFile `
    (Join-Path $source "docs\agent-principles.md") `
    (Join-Path $targetPath "docs\agent-principles.md") `
    $overwrite
Copy-TeamFile `
    (Join-Path $source "docs\escalation-protocol.md") `
    (Join-Path $targetPath "docs\escalation-protocol.md") `
    $overwrite
Write-Ok "docs installed"

# ── Install VibeLoom substrate (v02) ─────────────────────────────────────────
# The vibeloom skill references ../../../v02/ relative to its location in
# .github/skills/vibeloom/SKILL.md — so v02/ must exist in the target repo.

Write-Step "Installing VibeLoom substrate (v02)..."
Copy-TeamDir `
    (Join-Path $source "v02") `
    (Join-Path $targetPath "v02") `
    $overwrite
Write-Ok "VibeLoom substrate installed"

# ── Install state library ─────────────────────────────────────────────────────

Write-Step "Installing state library..."
Copy-TeamFile `
    (Join-Path $source ".agent-state\lib\state.py") `
    (Join-Path $targetPath ".agent-state\lib\state.py") `
    $overwrite
Copy-TeamFile `
    (Join-Path $source ".agent-state\lib\migrate.py") `
    (Join-Path $targetPath ".agent-state\lib\migrate.py") `
    $overwrite
Copy-TeamFile `
    (Join-Path $source ".agent-state\lib\__init__.py") `
    (Join-Path $targetPath ".agent-state\lib\__init__.py") `
    $overwrite
Copy-TeamFile `
    (Join-Path $source ".agent-state\schema.sql") `
    (Join-Path $targetPath ".agent-state\schema.sql") `
    $overwrite
Copy-TeamFile `
    (Join-Path $source ".agent-state\README.md") `
    (Join-Path $targetPath ".agent-state\README.md") `
    $overwrite

# .gitignore for .agent-state (don't overwrite if target already has one)
$targetAgentStateGitignore = Join-Path $targetPath ".agent-state\.gitignore"
if (-not (Test-Path $targetAgentStateGitignore)) {
    Copy-TeamFile `
        (Join-Path $source ".agent-state\.gitignore") `
        $targetAgentStateGitignore `
        $false
}

# Ensure audit/ directory exists
New-Item -ItemType Directory -Path (Join-Path $targetPath ".agent-state\audit") -Force | Out-Null

Write-Ok "state library installed"

# ── Write VERSION ─────────────────────────────────────────────────────────────

Write-Step "Writing VERSION..."
$commitSha = (git -C $source rev-parse HEAD 2>$null) ?? "unknown"
$installedAt = [System.DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")
$versionContent = @"
source=$source
source_commit=$commitSha
installed_at=$installedAt
mode=copy
schema_version=1
"@
Set-Content -Path $versionFile -Value $versionContent -Encoding UTF8
Write-Ok "VERSION written"

# ── Update root .gitignore ────────────────────────────────────────────────────

Write-Step "Checking root .gitignore..."
# Ensure __pycache__ directories under .agent-state are not committed
Add-GitignoreRule $targetPath ".agent-state/lib/__pycache__/"
# v02 is vibeloom tooling, not the target project's own source
Add-GitignoreRule $targetPath "v02/"
Write-Ok "gitignore up to date"

# ── Initialize state DB ───────────────────────────────────────────────────────

$stateDb = Join-Path $targetPath ".agent-state\state.db"
if (-not (Test-Path $stateDb)) {
    Write-Step "Initializing state.db..."
    $initResult = py -c "
import sys, os
sys.path.insert(0, os.path.join(r'$targetPath', '.agent-state'))
from lib import state
conn = state.connect(db_path=__import__('pathlib').Path(r'$stateDb'))
conn.close()
print('ok')
" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Ok "state.db initialized"
    } else {
        Write-Warn "Could not initialize state.db automatically (Python not found or error)."
        Write-Warn "Run manually: py -c `"import sys; sys.path.insert(0, '.agent-state'); from lib import state; state.connect()`""
        Write-Warn "Details: $initResult"
    }
} else {
    Write-Ok "state.db already exists — preserved"
}

# ── Done ──────────────────────────────────────────────────────────────────────

Write-Host ""
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Open the target project in VS Code: code `"$targetPath`""
Write-Host "  2. In Copilot Chat, type: @tech-lead <your goal>"
Write-Host "  3. Or type: @tech-lead resume  (to continue a paused task)"
Write-Host ""
Write-Host "State DB commands (from target project root):" -ForegroundColor White
Write-Host "  `$env:PYTHONPATH = `".agent-state`""
Write-Host "  py -m lib.state next-id"
Write-Host "  py -m lib.state list"
Write-Host "  py -m lib.state show T-YYMMDD-NN"
Write-Host ""
