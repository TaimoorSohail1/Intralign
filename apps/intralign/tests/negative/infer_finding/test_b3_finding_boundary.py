"""QA-WB-INFER B3 (the Finding boundary) — the Critical/Major negatives that
guard Derived-not-Attested, mandatory evidence anchors, the producer boundary,
and immutable Findings.

Each is a contract negative (IC-WB-INFER 1.1 forbidden / invariants), a REAL
test — not a comment:
- a Finding CANNOT be Attested-as-truth (Critical — Derived->Attested);
- a Finding CANNOT carry severity/confidence/score/recommendation (producer
  boundary — those are Evaluate's / Advise's);
- a Finding CANNOT be missing its evidence anchor (Major — IC-WB-INFER);
- a Finding CANNOT carry an unknown finding_type;
- a Finding CANNOT be changed in place (frozen — change only via recompute).
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from shared.epistemic import EpistemicState, Finding


def _finding(**overrides):
    base = dict(
        project_id="p",
        finding_type="gap",
        finding_id="gap-abc",
        summary="A coverage gap.",
        evidence_anchors=("assertion-0",),
        model_or_rule_version="wb-infer-finding-v0",
        mode="fast",
    )
    base.update(overrides)
    return Finding(**base)


def test_b3_finding_cannot_be_attested_as_truth() -> None:
    """CRITICAL — a Finding is pinned Derived; any Attested state is rejected."""
    for attested in (
        EpistemicState.ATTESTED_EVIDENCE,
        EpistemicState.ATTESTED_OSLO,
        EpistemicState.ATTESTED_USER,
    ):
        with pytest.raises(ValidationError):
            _finding(epistemic_state=attested)


def test_b3_finding_cannot_carry_severity_confidence_score_or_recommendation() -> None:
    """PRODUCER BOUNDARY — Evaluate owns severity/confidence; Advise owns recs.
    The Finding shape forbids those fields structurally (extra='forbid')."""
    for forbidden in ("severity", "confidence", "score", "reliability",
                      "caf", "recommendation", "clarification", "priority"):
        with pytest.raises(ValidationError):
            _finding(**{forbidden: 1})


def test_b3_finding_missing_evidence_anchor_is_rejected_major() -> None:
    """MAJOR — a Finding with no evidence anchor cannot be constructed."""
    with pytest.raises(ValidationError):
        _finding(evidence_anchors=())  # empty -> min_length=1 rejects it
    with pytest.raises(ValidationError):
        Finding(  # anchor field omitted entirely
            project_id="p", finding_type="gap", finding_id="x",
            summary="s", model_or_rule_version="v", mode="fast",
        )  # type: ignore[call-arg]


def test_b3_finding_cannot_carry_an_unknown_type() -> None:
    """A Finding type outside {gap, conflict, risk} is rejected (Object Model §8)."""
    with pytest.raises(ValidationError):
        _finding(finding_type="recommendation")
    with pytest.raises(ValidationError):
        _finding(finding_type="issue")


def test_b3_finding_cannot_be_changed_in_place() -> None:
    """CRITICAL (change-without-recompute) — the Finding is frozen; mutation fails."""
    finding = _finding()
    with pytest.raises(ValidationError):
        finding.summary = "edited without recompute"  # type: ignore[misc]
    with pytest.raises(ValidationError):
        finding.confidence_stage = "validated"  # type: ignore[misc]


def test_b3_finding_is_derived_by_default() -> None:
    assert _finding().epistemic_state is EpistemicState.DERIVED
