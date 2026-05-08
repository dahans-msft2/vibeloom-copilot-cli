"""Per-artifact frontmatter validation (§6).

Run after the parser. Returns blocking + advisory findings.
"""

from __future__ import annotations

from vibeloom_engine.ids import CONTAINER_LAYERS
from vibeloom_engine.models import (
    Artifact,
    ArtifactType,
    CONTEXT_TYPES,
    CONTRACT_TYPES,
    Finding,
    Status,
)


def _f(severity: str, artifact_id: str, check: str, message: str, item_id: str | None = None) -> Finding:
    return Finding(
        severity=severity,
        artifact_id=artifact_id,
        check=check,
        message=message,
        item_id=item_id,
    )


def validate_artifact(artifact: Artifact) -> list[Finding]:
    """Validate one artifact's frontmatter shape per §6."""
    findings: list[Finding] = []
    a = artifact

    # All artifacts: required fields.
    if not a.artifact_id:
        findings.append(_f("blocking", "(unknown)", "frontmatter", "missing artifact_id"))
    if not a.tier:
        findings.append(_f("blocking", a.artifact_id, "frontmatter", "missing tier"))
    if a.scope is None:
        findings.append(_f("blocking", a.artifact_id, "frontmatter", "missing scope_kind/scope_id"))
    if a.timestamp is None:
        findings.append(_f("advisory", a.artifact_id, "frontmatter", "missing timestamp"))

    # Contract-only fields.
    if a.artifact_type in CONTRACT_TYPES:
        if a.status is None:
            findings.append(_f("blocking", a.artifact_id, "frontmatter", "contract artifact missing status"))
        if a.approval_unit is None or a.approval_unit == "":
            findings.append(
                _f("blocking", a.artifact_id, "frontmatter", "contract artifact missing approval_unit (§6.1)")
            )
    elif a.artifact_type in CONTEXT_TYPES or a.artifact_type == ArtifactType.VALIDATION_REGISTRY:
        if a.status is not None:
            findings.append(
                _f("advisory", a.artifact_id, "frontmatter", f"non-contract artifact carries status ({a.status.value}); ignored")
            )
        if a.approval_unit is not None:
            findings.append(
                _f("advisory", a.artifact_id, "frontmatter", "non-contract artifact carries approval_unit; ignored")
            )

    # Container `layer` (§6.3).
    if a.artifact_type == ArtifactType.CONTAINER:
        if a.layer is None:
            findings.append(
                _f("blocking", a.artifact_id, "frontmatter", "container missing required `layer` (§6.3)")
            )
        else:
            if a.layer.value not in CONTAINER_LAYERS:
                findings.append(
                    _f(
                        "blocking",
                        a.artifact_id,
                        "frontmatter",
                        f"container layer {a.layer.value!r} not in {list(CONTAINER_LAYERS)}",
                    )
                )

    # status enum bounding (already enum; defensive)
    if a.status is not None and a.status not in (Status.DRAFT, Status.APPROVED):
        findings.append(_f("blocking", a.artifact_id, "frontmatter", f"unknown status {a.status!r}"))

    return findings


def validate_repo(artifacts: list[Artifact]) -> list[Finding]:
    """Run validate_artifact on every artifact + check for duplicate artifact_ids."""
    findings: list[Finding] = []
    seen: dict[str, str] = {}
    for a in artifacts:
        for f in validate_artifact(a):
            findings.append(f)
        if a.artifact_id in seen and seen[a.artifact_id] != a.path:
            findings.append(
                _f(
                    "blocking",
                    a.artifact_id,
                    "frontmatter",
                    f"duplicate artifact_id at {a.path} (also seen at {seen[a.artifact_id]})",
                )
            )
        else:
            seen[a.artifact_id] = a.path
    return findings


__all__ = ["validate_artifact", "validate_repo"]
