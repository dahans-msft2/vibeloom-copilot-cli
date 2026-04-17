"""Status report composer.

Emits a status snapshot suitable for writing to .vibeloom/state/status.json and
for display to the user. Covers:

- Contract-tier lifecycle (draft | approved | not yet generated)
- For context and code: generated/not yet generated and current/stale
- Stale artifacts
- Affected tiers and scopes (when the caller provides an affected set)
- Coverage gaps (from eval findings at the "coverage" check)
- Current mode (read from engine state or frontmatter)

v0.1: mode is read from .vibeloom/state/mode.txt if present, else reported as "unknown".
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from vibeloom_engine.affected import AffectedSet
from vibeloom_engine.eval_ import eval_graph
from vibeloom_engine.models import Artifact, ArtifactType, Graph, Status
from vibeloom_engine.staleness import compute_stale


CONTRACT_TIERS = ("intent-specs", "product-specs", "system-specs")


@dataclass
class StatusReport:
    mode: str
    contract_lifecycle: dict[str, str] = field(default_factory=dict)  # tier → "draft"|"approved"|"absent"
    context_state: dict[str, str] = field(default_factory=dict)  # artifact_type → "generated"|"absent"|"stale"
    code_state: str = "absent"  # "generated" | "absent" | "stale" (v0.1 stub)
    stale_artifacts: list[str] = field(default_factory=list)
    coverage_gaps: list[str] = field(default_factory=list)
    affected_scopes: list[str] = field(default_factory=list)
    affected_tiers: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "contract_lifecycle": dict(self.contract_lifecycle),
            "context_state": dict(self.context_state),
            "code_state": self.code_state,
            "stale_artifacts": list(self.stale_artifacts),
            "coverage_gaps": list(self.coverage_gaps),
            "affected_scopes": list(self.affected_scopes),
            "affected_tiers": list(self.affected_tiers),
        }


def _read_mode(repo_root: Path) -> str:
    mode_file = repo_root / ".vibeloom" / "state" / "mode.txt"
    if mode_file.is_file():
        return mode_file.read_text(encoding="utf-8").strip()
    return "unknown"


def compute_status(
    graph: Graph,
    artifacts: list[Artifact],
    repo_root: Path,
    affected: AffectedSet | None = None,
) -> StatusReport:
    """Compose a status report from a parsed graph + artifact list."""
    report = StatusReport(mode=_read_mode(repo_root))

    # Contract lifecycle per tier: latest status across artifacts in that tier.
    for tier in CONTRACT_TIERS:
        tier_arts = [a for a in artifacts if a.tier == tier]
        if not tier_arts:
            report.contract_lifecycle[tier] = "absent"
        else:
            # If all are approved → "approved"; if any draft → "draft".
            if any(a.status == Status.DRAFT for a in tier_arts):
                report.contract_lifecycle[tier] = "draft"
            elif all(a.status == Status.APPROVED for a in tier_arts):
                report.contract_lifecycle[tier] = "approved"
            else:
                report.contract_lifecycle[tier] = "draft"

    # Context state per artifact_type.
    stale_ids = {s.artifact_id for s in compute_stale(graph)}
    report.stale_artifacts = sorted(stale_ids)

    for ctx_type in (ArtifactType.CONFIG, ArtifactType.PDR, ArtifactType.ADR, ArtifactType.BDD):
        present = [a for a in artifacts if a.artifact_type == ctx_type]
        if not present:
            report.context_state[ctx_type.value] = "absent"
        elif any(a.artifact_id in stale_ids for a in present):
            report.context_state[ctx_type.value] = "stale"
        else:
            report.context_state[ctx_type.value] = "generated"

    # Coverage gaps: findings from structural eval with check == "coverage".
    findings = eval_graph(graph, artifacts)
    gaps = [f.message for f in findings if f.check == "coverage"]
    report.coverage_gaps = gaps

    if affected is not None:
        report.affected_scopes = sorted(affected.scopes)
        report.affected_tiers = sorted(affected.tiers)

    return report
