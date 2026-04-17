"""Per-artifact-type schema validation.

Validates required frontmatter fields (per vibeloom-implementation.md ## Metadata
Format) and required body carriers where feasible. Emits human-readable
findings.

This is the structural half of eval — it runs even on isolated artifacts
without needing the full graph. Graph-level checks (reference integrity,
contradiction across tiers) live in eval_.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from vibeloom_engine.ids import parse_id
from vibeloom_engine.models import (
    Artifact,
    ArtifactType,
    CONTEXT_TYPES,
    CONTRACT_TYPES,
    Status,
)


@dataclass
class Finding:
    severity: str  # "error" | "warning"
    artifact_id: str
    check: str
    message: str


# Required frontmatter keys per artifact class.
_CONTRACT_REQUIRED = (
    "artifact_id",
    "artifact_type",
    "tier",
    "scope_kind",
    "scope_id",
    "status",
    "timestamp",
    "derives_from",
)

_CONTEXT_REQUIRED = (
    "artifact_id",
    "artifact_type",
    "tier",
    "scope_kind",
    "scope_id",
    "timestamp",
    "derives_from",
)


def _frontmatter_present(
    artifact: Artifact,
    required: Iterable[str],
    check_name: str,
) -> list[Finding]:
    """Check that required frontmatter keys are present.

    Artifact is already parsed, so presence is inferred from model fields + extras.
    """
    findings: list[Finding] = []
    # Infer the set of "present" keys from what made it into the model.
    present: set[str] = {
        "artifact_id" if artifact.artifact_id else None,
        "artifact_type",
        "tier" if artifact.tier else None,
        "scope_kind" if artifact.scope else None,
        "scope_id" if artifact.scope else None,
        "timestamp" if artifact.timestamp else None,
        "derives_from",  # always present (defaults to [])
    }
    if artifact.status is not None:
        present.add("status")
    present.discard(None)  # type: ignore[arg-type]

    for key in required:
        if key not in present:
            findings.append(
                Finding(
                    severity="error",
                    artifact_id=artifact.artifact_id,
                    check=check_name,
                    message=f"missing required frontmatter field: {key}",
                )
            )
    return findings


def _component_required(artifact: Artifact) -> list[Finding]:
    """Component-specific required fields."""
    findings: list[Finding] = []
    required_extras = ("container_id", "component_id", "bounded_context", "owned_paths", "owned_interfaces")
    for key in required_extras:
        if key not in artifact.extras:
            findings.append(
                Finding(
                    severity="error",
                    artifact_id=artifact.artifact_id,
                    check="required-fields",
                    message=f"component.md missing required frontmatter field: {key}",
                )
            )
    return findings


def _container_required(artifact: Artifact) -> list[Finding]:
    """Container-specific required fields."""
    findings: list[Finding] = []
    if "container_id" not in artifact.extras:
        findings.append(
            Finding(
                severity="error",
                artifact_id=artifact.artifact_id,
                check="required-fields",
                message="container.md missing required frontmatter field: container_id",
            )
        )
    return findings


def _config_required(artifact: Artifact) -> list[Finding]:
    """Config-specific required fields."""
    findings: list[Finding] = []
    if "assistant" not in artifact.extras:
        findings.append(
            Finding(
                severity="error",
                artifact_id=artifact.artifact_id,
                check="required-fields",
                message="config artifact missing required frontmatter field: assistant",
            )
        )
    return findings


def _id_format(artifact: Artifact) -> list[Finding]:
    """Check that every item_id in an artifact is well-formed (PREFIX-####)."""
    findings: list[Finding] = []
    seen: set[str] = set()
    for item in artifact.items:
        parsed = parse_id(item.item_id)
        if not parsed:
            findings.append(
                Finding(
                    severity="error",
                    artifact_id=artifact.artifact_id,
                    check="required-fields",
                    message=f"malformed item ID: {item.item_id}",
                )
            )
        if item.item_id in seen:
            findings.append(
                Finding(
                    severity="error",
                    artifact_id=artifact.artifact_id,
                    check="required-fields",
                    message=f"duplicate item ID within artifact: {item.item_id}",
                )
            )
        seen.add(item.item_id)
    return findings


def _lifecycle_consistency(artifact: Artifact) -> list[Finding]:
    """Contract artifacts must have a status and, when approved, approval_mode."""
    findings: list[Finding] = []
    if artifact.artifact_type in CONTEXT_TYPES:
        # Context must not carry status.
        if artifact.status is not None:
            findings.append(
                Finding(
                    severity="error",
                    artifact_id=artifact.artifact_id,
                    check="lifecycle-consistency",
                    message="context artifact carries a status field (methodology says context has no lifecycle metadata)",
                )
            )
        return findings
    # Contract
    if artifact.status is None:
        findings.append(
            Finding(
                severity="error",
                artifact_id=artifact.artifact_id,
                check="lifecycle-consistency",
                message="contract artifact missing status",
            )
        )
        return findings
    if artifact.status == Status.APPROVED and artifact.approval_mode is None:
        findings.append(
            Finding(
                severity="error",
                artifact_id=artifact.artifact_id,
                check="lifecycle-consistency",
                message="approved contract artifact missing approval_mode",
            )
        )
    if artifact.status == Status.DRAFT and artifact.approval_mode is not None:
        findings.append(
            Finding(
                severity="warning",
                artifact_id=artifact.artifact_id,
                check="lifecycle-consistency",
                message="draft artifact carries approval_mode (provenance set on draft)",
            )
        )
    return findings


def validate_artifact(artifact: Artifact) -> list[Finding]:
    """Run all single-artifact structural checks. Returns a list of findings."""
    findings: list[Finding] = []
    findings.extend(_lifecycle_consistency(artifact))
    if artifact.artifact_type in CONTEXT_TYPES:
        findings.extend(_frontmatter_present(artifact, _CONTEXT_REQUIRED, "required-fields"))
    else:
        findings.extend(_frontmatter_present(artifact, _CONTRACT_REQUIRED, "required-fields"))

    if artifact.artifact_type == ArtifactType.COMPONENT:
        findings.extend(_component_required(artifact))
    elif artifact.artifact_type == ArtifactType.CONTAINER:
        findings.extend(_container_required(artifact))
    elif artifact.artifact_type == ArtifactType.CONFIG:
        findings.extend(_config_required(artifact))

    findings.extend(_id_format(artifact))
    return findings


def validate_repo(artifacts: list[Artifact]) -> list[Finding]:
    """Run per-artifact validation across an entire repo."""
    findings: list[Finding] = []
    # Declared relationships: items owned by correct artifacts, scopes, tiers.
    for a in artifacts:
        findings.extend(validate_artifact(a))
    # Cross-artifact: duplicate item IDs across the repo.
    seen: dict[str, str] = {}  # item_id -> artifact_id
    for a in artifacts:
        for item in a.items:
            if item.item_id in seen:
                findings.append(
                    Finding(
                        severity="error",
                        artifact_id=a.artifact_id,
                        check="required-fields",
                        message=f"duplicate item ID {item.item_id} (also defined in {seen[item.item_id]})",
                    )
                )
            else:
                seen[item.item_id] = a.artifact_id
    return findings
