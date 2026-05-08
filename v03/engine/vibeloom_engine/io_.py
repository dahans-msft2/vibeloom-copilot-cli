"""Filesystem layer: discovery + path conventions.

Walks a v0.3 governed repo (full mode or vibe mode) and lists candidate
artifacts. Parsing happens in `parser.py`. The engine never reads under
`templates/` (it's a build artifact for the skill, not engine input).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DiscoveredFile:
    rel_path: str  # forward-slash repo-relative
    abs_path: Path
    mtime: float


# Root contract files (full mode + vibe).
ROOT_CONTRACT_FILES: tuple[str, ...] = (
    "intent.md",
    "defaults.md",
    "prd.md",
    "usm.md",
    "dm.md",
    "ux.md",
    "system.md",
    "containers.md",
)

CONFIG_FILES: tuple[str, ...] = ("AGENTS.md", "CLAUDE.md")

# Validation registry lives at root; tier "meta".
META_FILES: tuple[str, ...] = ("validation-registry.md",)

# Directories that are never treated as containers.
SKIP_DIRS: frozenset[str] = frozenset(
    {".vibeloom", ".git", "node_modules", "__pycache__", "engine", "ux-specs", "templates", "decisions"}
)


def _norm(p: Path, root: Path) -> str:
    return p.relative_to(root).as_posix()


def _df(p: Path, root: Path) -> DiscoveredFile:
    st = p.stat()
    return DiscoveredFile(rel_path=_norm(p, root), abs_path=p, mtime=st.st_mtime)


def discover_artifacts(repo_root: Path) -> list[DiscoveredFile]:
    """Walk a v0.3 governed repo and return the list of artifact files."""
    discovered: list[DiscoveredFile] = []

    # 1. root-level contract files
    for name in ROOT_CONTRACT_FILES:
        p = repo_root / name
        if p.is_file():
            discovered.append(_df(p, repo_root))

    # 2. root-level config & meta
    for name in CONFIG_FILES + META_FILES:
        p = repo_root / name
        if p.is_file():
            discovered.append(_df(p, repo_root))

    # 3. container/component tree
    for child in sorted(repo_root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith(".") or child.name in SKIP_DIRS:
            continue
        container_md = child / "container.md"
        if not container_md.is_file():
            continue
        discovered.append(_df(container_md, repo_root))
        for cfg in CONFIG_FILES:
            p = child / cfg
            if p.is_file():
                discovered.append(_df(p, repo_root))
        for grand in sorted(child.iterdir()):
            if not grand.is_dir() or grand.name.startswith(".") or grand.name == "context":
                continue
            comp_md = grand / "component.md"
            if not comp_md.is_file():
                continue
            discovered.append(_df(comp_md, repo_root))
            for cfg in CONFIG_FILES:
                p = grand / cfg
                if p.is_file():
                    discovered.append(_df(p, repo_root))
            bdd_dir = grand / "context" / "bdd"
            if bdd_dir.is_dir():
                for bdd in sorted(bdd_dir.glob("BDD-*.md")):
                    if bdd.is_file():
                        discovered.append(_df(bdd, repo_root))

    return discovered


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def vibeloom_dir(repo_root: Path) -> Path:
    return repo_root / ".vibeloom"


def cache_dir(repo_root: Path) -> Path:
    return vibeloom_dir(repo_root) / "cache"


def traces_dir(repo_root: Path) -> Path:
    return vibeloom_dir(repo_root) / "traces"


def runs_dir(repo_root: Path) -> Path:
    return vibeloom_dir(repo_root) / "runs"


def decisions_dir(repo_root: Path) -> Path:
    return repo_root / "decisions"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


__all__ = [
    "DiscoveredFile",
    "ROOT_CONTRACT_FILES",
    "CONFIG_FILES",
    "META_FILES",
    "SKIP_DIRS",
    "discover_artifacts",
    "read_text",
    "vibeloom_dir",
    "cache_dir",
    "traces_dir",
    "runs_dir",
    "decisions_dir",
    "ensure_dir",
]
