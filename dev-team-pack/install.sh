#!/usr/bin/env bash
# dev-team-pack/install.sh
# Installs the dev-team-pack into a target repository.
#
# Usage:
#   bash dev-team-pack/install.sh --target /path/to/your-project
#   bash dev-team-pack/install.sh --target /path/to/your-project --update
#
# Run from the vibeloom-copilot-cli root directory.

set -euo pipefail

# ── Colours ───────────────────────────────────────────────────────────────────
CYAN='\033[0;36m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
step()  { echo -e "  ${CYAN}→${NC} $1"; }
ok()    { echo -e "  ${GREEN}✓${NC} $1"; }
warn()  { echo -e "  ${YELLOW}⚠${NC} $1"; }
fail()  { echo -e "  ${RED}✗${NC} $1"; exit 1; }

# ── Args ──────────────────────────────────────────────────────────────────────
TARGET=""
UPDATE=0

while [[ $# -gt 0 ]]; do
    case $1 in
        --target|-t) TARGET="$2"; shift 2 ;;
        --update|-u) UPDATE=1; shift ;;
        *) fail "Unknown argument: $1" ;;
    esac
done

[[ -z "$TARGET" ]] && fail "--target is required"

# ── Resolve paths ─────────────────────────────────────────────────────────────
SOURCE="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="$(cd "$TARGET" && pwd)"

echo ""
echo "dev-team-pack installer"
echo "  Source : $SOURCE"
echo "  Target : $TARGET"
echo "  Mode   : $([ $UPDATE -eq 1 ] && echo 'Update (overwrite team files)' || echo 'Fresh install')"
echo ""

# ── Validations ───────────────────────────────────────────────────────────────
[[ "$TARGET" == "$SOURCE" ]] && fail "Target is the same as source (vibeloom-copilot-cli). Choose a different project."
[[ ! -d "$TARGET/.git" ]] && fail "Target does not appear to be a git repository (no .git directory found)."

VERSION_FILE="$TARGET/.agent-state/VERSION"
if [[ -f "$VERSION_FILE" && $UPDATE -eq 0 ]]; then
    warn "dev-team-pack is already installed in this project."
    warn "Use --update to overwrite team files."
    read -r -p "Continue anyway? (y/N) " confirm
    [[ "$confirm" != "y" ]] && echo "Aborted." && exit 0
fi

# ── Copy helpers ──────────────────────────────────────────────────────────────
copy_dir() {
    local src="$1" dst="$2"
    [[ ! -d "$src" ]] && fail "Source not found: $src"
    if [[ $UPDATE -eq 1 ]]; then
        cp -r "$src/." "$dst/"
    else
        rsync -a --ignore-existing "$src/" "$dst/" 2>/dev/null || {
            # fallback if rsync not available
            find "$src" -type f | while read -r f; do
                rel="${f#$src/}"
                dest="$dst/$rel"
                if [[ ! -f "$dest" ]]; then
                    mkdir -p "$(dirname "$dest")"
                    cp "$f" "$dest"
                fi
            done
        }
    fi
}

copy_file() {
    local src="$1" dst="$2"
    [[ ! -f "$src" ]] && fail "Source not found: $src"
    mkdir -p "$(dirname "$dst")"
    if [[ $UPDATE -eq 1 || ! -f "$dst" ]]; then
        cp "$src" "$dst"
    fi
}

add_gitignore_rule() {
    local repo_root="$1" rule="$2"
    local gi="$repo_root/.gitignore"
    if [[ -f "$gi" ]] && ! grep -qF "$rule" "$gi"; then
        echo "" >> "$gi"
        echo "$rule" >> "$gi"
    fi
}

# ── Install ───────────────────────────────────────────────────────────────────
step "Installing agents..."
mkdir -p "$TARGET/.github/agents"
copy_dir "$SOURCE/.github/agents" "$TARGET/.github/agents"
ok "agents installed"

step "Installing skills..."
mkdir -p "$TARGET/.github/skills"
copy_dir "$SOURCE/.github/skills" "$TARGET/.github/skills"
ok "skills installed"

step "Installing issue template..."
mkdir -p "$TARGET/.github/ISSUE_TEMPLATE"
copy_file "$SOURCE/.github/ISSUE_TEMPLATE/agent-blocker.md" \
          "$TARGET/.github/ISSUE_TEMPLATE/agent-blocker.md"
ok "issue template installed"

step "Installing agent docs..."
mkdir -p "$TARGET/docs"
copy_file "$SOURCE/docs/agent-principles.md"    "$TARGET/docs/agent-principles.md"
copy_file "$SOURCE/docs/escalation-protocol.md" "$TARGET/docs/escalation-protocol.md"
ok "docs installed"

step "Installing state library..."
mkdir -p "$TARGET/.agent-state/lib"
copy_file "$SOURCE/.agent-state/lib/state.py"    "$TARGET/.agent-state/lib/state.py"
copy_file "$SOURCE/.agent-state/lib/migrate.py"  "$TARGET/.agent-state/lib/migrate.py"
copy_file "$SOURCE/.agent-state/lib/__init__.py" "$TARGET/.agent-state/lib/__init__.py"
copy_file "$SOURCE/.agent-state/schema.sql"      "$TARGET/.agent-state/schema.sql"
copy_file "$SOURCE/.agent-state/README.md"       "$TARGET/.agent-state/README.md"
[[ ! -f "$TARGET/.agent-state/.gitignore" ]] && \
    copy_file "$SOURCE/.agent-state/.gitignore" "$TARGET/.agent-state/.gitignore"
mkdir -p "$TARGET/.agent-state/audit"
ok "state library installed"

step "Writing VERSION..."
COMMIT_SHA=$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null || echo "unknown")
INSTALLED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
cat > "$VERSION_FILE" <<EOF
source=$SOURCE
source_commit=$COMMIT_SHA
installed_at=$INSTALLED_AT
mode=copy
schema_version=1
EOF
ok "VERSION written"

step "Checking root .gitignore..."
add_gitignore_rule "$TARGET" ".agent-state/lib/__pycache__/"
ok "gitignore up to date"

step "Initializing state.db..."
STATE_DB="$TARGET/.agent-state/state.db"
if [[ ! -f "$STATE_DB" ]]; then
    if python3 -c "
import sys, os
sys.path.insert(0, os.path.join('$TARGET', '.agent-state'))
from lib import state
import pathlib
conn = state.connect(db_path=pathlib.Path('$STATE_DB'))
conn.close()
print('ok')
" 2>/dev/null; then
        ok "state.db initialized"
    else
        warn "Could not initialize state.db automatically (python3 not found or error)."
        warn "Run manually: PYTHONPATH=.agent-state python3 -m lib.state next-id"
    fi
else
    ok "state.db already exists — preserved"
fi

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}Installation complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Open the target project in VS Code: code \"$TARGET\""
echo "  2. In Copilot Chat, type: @tech-lead <your goal>"
echo "  3. Or type: @tech-lead resume  (to continue a paused task)"
echo ""
echo "State DB commands (from target project root):"
echo "  export PYTHONPATH=.agent-state"
echo "  python3 -m lib.state list"
echo "  python3 -m lib.state next-id"
echo "  python3 -m lib.state show T-YYMMDD-NN"
echo ""
