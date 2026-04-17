"""Filesystem layer: artifact discovery, mtime access, repo conventions.

The engine reads from a governed repo with layout defined by
vibeloom-implementation.md ## Governed Repo Layout.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


# Discovered artifact with its repo-relative path and filesystem mtime.
@dataclass(frozen=True)
class DiscoveredFile:
    rel_path: str  # forward-slash repo-relative path
    abs_path: Path  # absolute Path for reading
    mtime: float  # filesystem mtime (epoch seconds)


# Root-level contract artifacts by fixed filename.
ROOT_CONTRACT_FILES: tuple[str, ...] = (
    "intent.md",
    "defaults.md",
    "prd.md",
    "usm.md",
    "dm.md",
    "system.md",
    "containers.md",
)

# Root-level context ledgers under context/
ROOT_CONTEXT_LEDGERS: tuple[str, ...] = (
    "context/pdr.md",
    "context/adr.md",
)

# Assistant-specific config filenames (same shape at root, container, component).
CONFIG_FILES: tuple[str, ...] = ("AGENTS.md", "CLAUDE.md")


def _norm(p: Path, root: Path) -> str:
    """Return the forward-slash repo-relative path."""
    return p.relative_to(root).as_posix()


def _stat(p: Path) -> DiscoveredFile:
    st = p.stat()
    # NB: mtime is a float epoch; we keep the float (rather than converting to
    # ISO) so the engine can compare cheaply. Frontmatter `timestamp:` is
    # separately maintained by the skill/subagent that writes the artifact.
    return DiscoveredFile(rel_path="", abs_path=p, mtime=st.st_mtime)


def discover_artifacts(repo_root: Path) -> list[DiscoveredFile]:
    """Walk the repo and return all files that match the governed layout.

    Returns only files that exist. Does not parse or validate them.

    Layout reference (vibeloom-implementation.md ## Governed Repo Layout):

    Full modes (pm/dev/expert):
      /<root>.md  (intent, defaults, prd, usm, dm, system, containers)
      /AGENTS.md  /CLAUDE.md
      /context/pdr.md  /context/adr.md
      /<container>/container.md
      /<container>/AGENTS.md  /<container>/CLAUDE.md
      /<container>/<component>/component.md
      /<container>/<component>/AGENTS.md  /<container>/<component>/CLAUDE.md
      /<container>/<component>/context/bdd/BDD-####-<slug>.md

    Compact (vibe):
      /intent.md  /defaults.md  /system.md
      /AGENTS.md  /CLAUDE.md
    """
    discovered: list[DiscoveredFile] = []

    # 1. Root-level contract files.
    for name in ROOT_CONTRACT_FILES:
        p = repo_root / name
        if p.is_file():
            df = _stat(p)
            discovered.append(DiscoveredFile(rel_path=_norm(p, repo_root), abs_path=p, mtime=df.mtime))

    # 2. Root-level config files (AGENTS.md, CLAUDE.md).
    for name in CONFIG_FILES:
        p = repo_root / name
        if p.is_file():
            df = _stat(p)
            discovered.append(DiscoveredFile(rel_path=_norm(p, repo_root), abs_path=p, mtime=df.mtime))

    # 3. Root-level ledgers under context/.
    for rel in ROOT_CONTEXT_LEDGERS:
        p = repo_root / rel
        if p.is_file():
            df = _stat(p)
            discovered.append(DiscoveredFile(rel_path=_norm(p, repo_root), abs_path=p, mtime=df.mtime))

    # 4. Container and component artifacts + their configs + bdd scenarios.
    # Container = any top-level directory that contains a container.md.
    for child in sorted(repo_root.iterdir()):
        if not child.is_dir():
            continue
        # Skip hidden directories (.vibeloom, .git, etc.) and known non-container dirs.
        if child.name.startswith(".") or child.name in {"context", "node_modules", "__pycache__", "engine", "assets", "references"}:
            continue
        container_spec = child / "container.md"
        if not container_spec.is_file():
            # Not a governed container directory; skip.
            continue
        discovered.append(
            DiscoveredFile(
                rel_path=_norm(container_spec, repo_root),
                abs_path=container_spec,
                mtime=container_spec.stat().st_mtime,
            )
        )
        for name in CONFIG_FILES:
            p = child / name
            if p.is_file():
                discovered.append(
                    DiscoveredFile(
                        rel_path=_norm(p, repo_root),
                        abs_path=p,
                        mtime=p.stat().st_mtime,
                    )
                )
        # Components inside this container: any subdir containing component.md.
        for grand in sorted(child.iterdir()):
            if not grand.is_dir() or grand.name.startswith(".") or grand.name == "context":
                continue
            component_spec = grand / "component.md"
            if not component_spec.is_file():
                continue
            discovered.append(
                DiscoveredFile(
                    rel_path=_norm(component_spec, repo_root),
                    abs_path=component_spec,
                    mtime=component_spec.stat().st_mtime,
                )
            )
            for name in CONFIG_FILES:
                p = grand / name
                if p.is_file():
                    discovered.append(
                        DiscoveredFile(
                            rel_path=_norm(p, repo_root),
                            abs_path=p,
                            mtime=p.stat().st_mtime,
                        )
                    )
            # Component-scoped bdd/ files.
            bdd_dir = grand / "context" / "bdd"
            if bdd_dir.is_dir():
                for bdd_file in sorted(bdd_dir.glob("BDD-*.md")):
                    if bdd_file.is_file():
                        discovered.append(
                            DiscoveredFile(
                                rel_path=_norm(bdd_file, repo_root),
                                abs_path=bdd_file,
                                mtime=bdd_file.stat().st_mtime,
                            )
                        )

    return discovered


def read_text(path: Path) -> str:
    """Read a file as UTF-8 text."""
    return path.read_text(encoding="utf-8")


def state_dir(repo_root: Path) -> Path:
    """Return the .vibeloom/state/ directory path (may not exist)."""
    return repo_root / ".vibeloom" / "state"


def ensure_state_dir(repo_root: Path) -> Path:
    """Create .vibeloom/state/ if missing and return it."""
    sd = state_dir(repo_root)
    sd.mkdir(parents=True, exist_ok=True)
    return sd
