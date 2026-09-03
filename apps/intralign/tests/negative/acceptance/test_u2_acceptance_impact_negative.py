"""QA-WU-ACCEPT U2 (negative) — the impossible/rejected Acceptance-Impact states.

Critical:
 - the impact comparison treated as CANONICAL rather than Derived (acceptance-
   impact-as-world-truth);
 - the assessment MUTATING the UAR or the plan fact (it is read-only over both).
Major:
 - an alert raised BELOW the ≥10pts/band threshold (Calibration §3).
"""

from __future__ import annotations

import uuid

import pytest
from pydantic import ValidationError

from backend.orchestration.wave_u import reconcile_acceptance_impact
from backend.responsibilities.evaluate.acceptance_impact import (
    AcceptedValue,
    compare_acceptance_impact,
)
from shared.epistemic import (
    AcceptanceImpactAssessment,
    CANONICAL_OUTPUTS,
    EpistemicState,
)
from tests.positive.acceptance.fakes import InMemoryAcceptanceStore, InMemoryChrRepo

PROJECT = str(uuid.uuid4())


# ---- Critical: impact-as-canonical / world-truth ---------------------------


def test_assessment_cannot_be_attested_canonical() -> None:
    """The Acceptance-Impact Assessment is Derived — pinning it Attested is rejected."""
    base = dict(
        project_id=PROJECT,
        uar_ref="uar-1",
        pinned_chr="chr-pin",
        latest_chr="chr-latest",
        delta=-14.0,
        band_changed=True,
        model_or_rule_version="caf-v0",
        mode="fast",
    )
    for canonical in (
        EpistemicState.ATTESTED_OSLO,
        EpistemicState.ATTESTED_USER,
        EpistemicState.ATTESTED_EVIDENCE,
    ):
        with pytest.raises(ValidationError):
            AcceptanceImpactAssessment(**base, epistemic_state=canonical)
    # The default IS derived (never canonical).
    assert AcceptanceImpactAssessment(**base).epistemic_state == EpistemicState.DERIVED


def test_assessment_carries_no_truth_or_governance_field() -> None:
    """extra='forbid' — no world-truth / approval / governance marker is representable."""
    base = dict(
        project_id=PROJECT,
        uar_ref="uar-1",
        pinned_chr="chr-pin",
        latest_chr="chr-latest",
        delta=-14.0,
        band_changed=True,
        model_or_rule_version="caf-v0",
        mode="fast",
    )
    for marker in (
        "true",
        "approved",
        "world_truth",
        "certified",
        "canonical",
        "governance",
        "decision",
        "authority",
    ):
        with pytest.raises(ValidationError):
            AcceptanceImpactAssessment(**base, **{marker: True})


def test_assessment_is_listed_as_derived_in_canonical_outputs_vocab() -> None:
    """It is a canonical-vocabulary NAME, but the entity itself is Derived."""
    assert "AcceptanceImpactAssessment" in CANONICAL_OUTPUTS
    inst = AcceptanceImpactAssessment(
        project_id=PROJECT,
        uar_ref="uar-1",
        pinned_chr="chr-pin",
        latest_chr="chr-latest",
        delta=-14.0,
        band_changed=True,
        model_or_rule_version="caf-v0",
        mode="fast",
    )
    assert inst.is_canonical is False


# ---- Critical: the assessment mutates neither the UAR nor the plan fact -----


def test_reconcile_never_mutates_the_uar_rows() -> None:
    """Read-only over the UAR: the rows are byte-intact after the reconcile."""
    repo = InMemoryChrRepo()
    store = InMemoryAcceptanceStore()
    pinned = repo.seed(
        project_id=PROJECT,
        output_kind="outcome_confidence",
        output_payload={"index": 82.0, "band": "high"},
    )
    import time

    time.sleep(0.001)
    repo.seed(
        project_id=PROJECT,
        output_kind="outcome_confidence",
        output_payload={"index": 60.0, "band": "medium"},
    )
    store.add_uar(version_pin=str(pinned.chr_id), action="accept", project_id=PROJECT)

    before = [dict(r) for r in store.acceptances]
    raised = reconcile_acceptance_impact(project_id=PROJECT, store=store, chr_repo=repo)
    assert len(raised) == 1  # it DID drift...
    after = [dict(r) for r in store.acceptances]
    assert after == before  # ...but the UAR rows are unchanged (read-only)


def test_reconcile_never_mutates_the_pinned_or_latest_value_chrs() -> None:
    """Read-only over the accepted item's value CHRs — only an acceptance_impact
    CHR is appended; the pinned/latest value CHRs are untouched."""
    repo = InMemoryChrRepo()
    store = InMemoryAcceptanceStore()
    pinned = repo.seed(
        project_id=PROJECT,
        output_kind="outcome_confidence",
        output_payload={"index": 82.0, "band": "high"},
    )
    import time

    time.sleep(0.001)
    latest = repo.seed(
        project_id=PROJECT,
        output_kind="outcome_confidence",
        output_payload={"index": 60.0, "band": "medium"},
    )
    store.add_uar(version_pin=str(pinned.chr_id), action="accept", project_id=PROJECT)

    pinned_snapshot = pinned.model_dump(mode="json")
    latest_snapshot = latest.model_dump(mode="json")

    reconcile_acceptance_impact(project_id=PROJECT, store=store, chr_repo=repo)

    # Every appended CHR is an acceptance_impact CHR — NEVER a rewrite of a value.
    for appended in repo.append_calls:
        assert appended.output_kind == "acceptance_impact"
    # The pinned + latest value CHRs are byte-intact.
    assert repo.get(pinned.chr_id).model_dump(mode="json") == pinned_snapshot
    assert repo.get(latest.chr_id).model_dump(mode="json") == latest_snapshot


# ---- Major: no alert below the ≥10pts/band threshold -----------------------


def test_below_threshold_raises_no_assessment_major() -> None:
    """< 10 pts AND same band — an alert here would be a Major false-surface."""
    drift = compare_acceptance_impact(
        pinned=AcceptedValue(index=80.0, band="high"),
        latest=AcceptedValue(index=72.0, band="high"),  # -8 pts, same band
    )
    assert drift.is_drift is False

    repo = InMemoryChrRepo()
    store = InMemoryAcceptanceStore()
    pinned = repo.seed(
        project_id=PROJECT,
        output_kind="outcome_confidence",
        output_payload={"index": 80.0, "band": "high"},
    )
    import time

    time.sleep(0.001)
    repo.seed(
        project_id=PROJECT,
        output_kind="outcome_confidence",
        output_payload={"index": 72.0, "band": "high"},
    )
    store.add_uar(version_pin=str(pinned.chr_id), action="accept", project_id=PROJECT)

    raised = reconcile_acceptance_impact(project_id=PROJECT, store=store, chr_repo=repo)
    assert raised == []
    assert [r for r in repo.append_calls if r.output_kind == "acceptance_impact"] == []
