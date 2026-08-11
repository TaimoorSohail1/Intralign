from __future__ import annotations

from dataclasses import dataclass

_BANDS = ("Fragile", "Weak", "Developing", "Solid", "Sound")
_PILLAR_ORDER = ("Viability", "Grounding", "Adaptability")


@dataclass(frozen=True, slots=True)
class IntegrityInputs:
    viable_artifacts: int
    load_bearing_artifacts: int
    grounded_items: int
    load_bearing_items: int
    registered_checkpoints: int
    needed_checkpoints: int
    outcome_root_grounded: bool = True


@dataclass(frozen=True, slots=True)
class Pillar:
    key: str
    band: str
    basis: float
    why: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Integrity:
    level: str
    limiting_pillar: str
    decomposition: tuple[Pillar, Pillar, Pillar]
    posture: str = "moment-in-time"
    tracking: str = "pending-execution"


@dataclass(frozen=True, slots=True)
class IntegrityArtifact:
    key: str
    title: str
    viable: bool
    reads_strong: bool
    grounded_items: int
    inferred_items: int
    primary_outcome: bool = False
    evidence_grounded_items: int | None = None
    evidence_inferred_items: int | None = None


@dataclass(frozen=True, slots=True)
class OutcomeCheckpoint:
    id: str
    workstream: str
    leading_indicator: str
    timing: str
    lever: str
    registered: bool
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class IntegrityIssue:
    id: str
    dim: str
    dims: tuple[str, ...]
    finding_type: str
    section: str
    severity: str
    status: str
    title: str
    why: str
    recommendation: str
    recommendation_from_oslo: bool = True


@dataclass(frozen=True, slots=True)
class IntegrityRead:
    integrity: Integrity
    issues: tuple[IntegrityIssue, ...]


def compute_integrity(inputs: IntegrityInputs) -> Integrity:
    """Compute the Slice 1 three-pillar, weakest-gate integrity read.

    Contract: R2 Slice 1 L1-L5, L8-L9 and AC-1/AC-2/AC-5/AC-6.
    """

    decomposition = tuple(
        _pillar(key, numerator, denominator)
        for key, numerator, denominator in (
            (
                "Viability",
                inputs.viable_artifacts,
                inputs.load_bearing_artifacts,
            ),
            ("Grounding", inputs.grounded_items, inputs.load_bearing_items),
            (
                "Adaptability",
                inputs.registered_checkpoints,
                inputs.needed_checkpoints,
            ),
        )
    )
    if not inputs.outcome_root_grounded:
        grounding = decomposition[1]
        decomposition = (
            decomposition[0],
            Pillar(
                key=grounding.key,
                band=_BANDS[min(_band_index(grounding.band), 1)],
                basis=grounding.basis,
                why=grounding.why
                + ("The primary outcome still rests on OSLO's inference",),
            ),
            decomposition[2],
        )
    floor = min(_band_index(pillar.band) for pillar in decomposition)
    limiting_pillar = next(
        key
        for key in _PILLAR_ORDER
        if next(pillar for pillar in decomposition if pillar.key == key).band
        == _BANDS[floor]
    )
    return Integrity(
        level=_BANDS[floor],
        limiting_pillar=limiting_pillar,
        decomposition=decomposition,  # type: ignore[arg-type]
    )


def build_integrity_read(
    *,
    artifacts: tuple[IntegrityArtifact, ...],
    checkpoints: tuple[OutcomeCheckpoint, ...],
    issues: tuple[IntegrityIssue, ...] = (),
) -> IntegrityRead:
    """Build the unified Slice 1 read from explicit outcome-path inputs.

    The false-confidence issue and Grounding basis intentionally consume the
    same artifact facts so attestation cannot retire one without the other.
    """

    false_confident = tuple(
        artifact
        for artifact in artifacts
        if artifact.reads_strong
        and _evidence_inferred(artifact) > _evidence_grounded(artifact)
    )
    unified_issues = (
        issues
        + tuple(_false_confidence_issue(artifact) for artifact in false_confident)
        + tuple(
            _checkpoint_issue(checkpoint)
            for checkpoint in checkpoints
            if not checkpoint.registered
        )
    )
    grounded_items = sum(artifact.grounded_items for artifact in artifacts)
    inferred_items = sum(artifact.inferred_items for artifact in artifacts)
    primary_outcomes = tuple(
        artifact for artifact in artifacts if artifact.primary_outcome
    )
    integrity = compute_integrity(
        IntegrityInputs(
            viable_artifacts=sum(artifact.viable for artifact in artifacts),
            load_bearing_artifacts=len(artifacts),
            grounded_items=grounded_items,
            load_bearing_items=grounded_items + inferred_items,
            registered_checkpoints=sum(
                checkpoint.registered for checkpoint in checkpoints
            ),
            needed_checkpoints=len(checkpoints),
            outcome_root_grounded=(
                all(_evidence_inferred(artifact) == 0 for artifact in primary_outcomes)
                if primary_outcomes
                else True
            ),
        )
    )
    ranked_issues = tuple(
        sorted(
            unified_issues,
            key=lambda issue: _issue_exposure(issue, integrity.limiting_pillar),
            reverse=True,
        )
    )
    return IntegrityRead(integrity=integrity, issues=ranked_issues)


def _false_confidence_issue(artifact: IntegrityArtifact) -> IntegrityIssue:
    return IntegrityIssue(
        id=f"ISS-FC-{artifact.key.upper()}",
        dim="Grounding",
        dims=("Grounding",),
        finding_type="False Confidence",
        section=artifact.title,
        severity="Moderate",
        status="open",
        title=(
            f"{artifact.title} reads solid — but on OSLO's inference, "
            "not your evidence"
        ),
        why=(
            f"Parts of {artifact.title} rest on OSLO's inference; it reads solid, "
            "which is exactly the trap."
        ),
        recommendation=(
            f"Confirm what {artifact.title} rests on — or flag it. Its read is strong, "
            "but most of it is OSLO's inference; confirming grounds it, and flagging "
            "records that it does not hold."
        ),
    )


def _evidence_grounded(artifact: IntegrityArtifact) -> int:
    return (
        artifact.evidence_grounded_items
        if artifact.evidence_grounded_items is not None
        else artifact.grounded_items
    )


def _evidence_inferred(artifact: IntegrityArtifact) -> int:
    return (
        artifact.evidence_inferred_items
        if artifact.evidence_inferred_items is not None
        else artifact.inferred_items
    )


def _checkpoint_issue(checkpoint: OutcomeCheckpoint) -> IntegrityIssue:
    return IntegrityIssue(
        id=f"ISS-CP-{checkpoint.id}",
        dim="Adaptability",
        dims=("Adaptability",),
        finding_type="Coverage Gap",
        section="Schedule",
        severity="Moderate",
        status="open",
        title=f"{checkpoint.workstream} has no outcome checkpoint",
        why=(
            f"The outcome is not re-read during {checkpoint.workstream} while there is "
            "still runway to change course."
        ),
        recommendation=(
            f"Add checkpoint: read {checkpoint.leading_indicator}; "
            f"{checkpoint.timing}; if it drifts, {checkpoint.lever}."
        ),
    )


def _issue_exposure(issue: IntegrityIssue, limiting_pillar: str) -> float:
    if (
        issue.status == "open"
        and issue.severity == "Critical"
        and issue.dim == "Viability"
    ):
        return 10
    severity = {"Warning": 1, "Moderate": 2, "Critical": 3}.get(
        issue.severity,
        0,
    )
    return severity + (1.5 if issue.dim == limiting_pillar else 0)


def _pillar(key: str, numerator: int, denominator: int) -> Pillar:
    if numerator < 0 or denominator < 0 or numerator > denominator:
        raise ValueError(f"INVALID_{key.upper()}_BASIS")
    basis = numerator / max(1, denominator)
    unit = {
        "Viability": "load-bearing understanding artifacts are clear",
        "Grounding": "load-bearing items rest on evidence",
        "Adaptability": "outcome checkpoints are registered",
    }[key]
    return Pillar(
        key=key,
        band=_band_for_fraction(basis),
        basis=basis,
        why=(f"{numerator} of {denominator} {unit}",),
    )


def _band_for_fraction(value: float) -> str:
    if value >= 1:
        return "Sound"
    if value >= 0.75:
        return "Solid"
    if value >= 0.5:
        return "Developing"
    if value >= 0.25:
        return "Weak"
    return "Fragile"


def _band_index(band: str) -> int:
    return _BANDS.index(band)
