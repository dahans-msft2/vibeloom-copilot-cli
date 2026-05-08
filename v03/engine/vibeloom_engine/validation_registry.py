"""Validation registry parser (§7).

`validation-registry.md` carries YAML frontmatter + a fenced ```yaml block
that lists runners. The engine parses the runners and exposes them as a
list; the orchestrator invokes them. The engine does not run runners —
that's a skill/orchestrator concern.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from vibeloom_engine.io_ import read_text
from vibeloom_engine.parser import split_frontmatter


@dataclass
class Runner:
    runner_id: str
    command: str
    scope: str = "workspace"
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "runner_id": self.runner_id,
            "command": self.command,
            "scope": self.scope,
            "inputs": list(self.inputs),
            "outputs": list(self.outputs),
        }


_FENCE_RE = re.compile(r"^```\s*yaml\s*$", re.MULTILINE)


def _extract_first_yaml_block(body: str) -> str:
    """Return the contents of the first ```yaml fenced block."""
    lines = body.splitlines()
    in_fence = False
    out: list[str] = []
    for line in lines:
        s = line.strip()
        if not in_fence:
            if s.lower().startswith("```yaml") or s.lower() == "```yaml":
                in_fence = True
            continue
        if s == "```":
            return "\n".join(out)
        out.append(line)
    return ""


def _parse_runner_records(yaml_block: str) -> list[Runner]:
    """Parse a list of `- runner_id: ...` records from the fenced block.

    The format is the spec's example: top-level `-` denotes start of a
    record; subsequent indented `key: value` lines are scalars or inline
    lists.
    """
    records: list[Runner] = []
    current: dict[str, Any] | None = None
    for raw in yaml_block.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        if line.startswith("- "):
            if current is not None:
                records.append(_to_runner(current))
            current = {}
            kv = line[2:]
            if ":" in kv:
                k, _, v = kv.partition(":")
                current[k.strip()] = _parse_scalar_or_list(v.strip())
            continue
        if current is None:
            continue
        # indented continuation
        stripped = line.lstrip()
        if ":" not in stripped:
            continue
        k, _, v = stripped.partition(":")
        current[k.strip()] = _parse_scalar_or_list(v.strip())
    if current is not None:
        records.append(_to_runner(current))
    return records


def _parse_scalar_or_list(s: str) -> Any:
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [x.strip() for x in inner.split(",")]
    if len(s) >= 2 and s[0] in ('"', "'") and s[-1] == s[0]:
        return s[1:-1]
    return s


def _to_runner(d: dict[str, Any]) -> Runner:
    return Runner(
        runner_id=str(d.get("runner_id", "")),
        command=str(d.get("command", "")),
        scope=str(d.get("scope", "workspace")),
        inputs=list(d.get("inputs") or []),
        outputs=list(d.get("outputs") or []),
    )


def parse_validation_registry(repo_root: Path) -> list[Runner]:
    """Parse `validation-registry.md` if present. Returns [] if absent."""
    p = repo_root / "validation-registry.md"
    if not p.is_file():
        return []
    text = read_text(p)
    _, body = split_frontmatter(text)
    block = _extract_first_yaml_block(body)
    if not block:
        return []
    return _parse_runner_records(block)


__all__ = ["Runner", "parse_validation_registry"]
