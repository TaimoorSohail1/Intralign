"""QA-WU-ACCEPT U2 (positive) — the Acceptance-Impact reconcile (DTM-0017).

After a recompute produces new values, the Evaluate-owned reconcile scans the
project's active version-pinned UARs and, for each whose accepted item drifted
≥10 pts or a band change vs the pin (Calibration §3), emits ONE Derived
Acceptance-Impact Assessment: a CHR is appended (output_kind=acceptance_impact)
and the events fire; a recompute supersedes a prior assessment for the SAME UAR;
no-drift / below-threshold raises nothing; the assessment references the UAR +
both the pinned and the latest CHR.
"""

from __future__ import annotations

import uuid

from backend.orchestration.wave_u import reconcile_acceptance_impact
from backend.services.observability.events import CollectingEventEmitter
from shared.epistemic import AcceptanceImpactAssessment, EpistemicState
from tests.positive.acceptance.fakes import InMemoryAcceptanceStore, InMemoryChrRepo

PROJECT = str(uuid.uuid4())


def _seed_pin(repo: InMemoryChrRepo, *, index: float, band: str):
    """Seed the version-pinned outcome_confidence CHR (the accepted value)."""
    return repo.seed(
        project_id=PROJECT,
        output_kind="outcome_confidence",
        output_payload={"index": index, "band": band},
    )


def _seed_latest(repo: InMemoryChrRepo, *, index: float, band: str):
    """Seed a NEWER outcome_confidence CHR (the recompute's moved value)."""
    import time

    time.sleep(0.001)  # ensure a strictly-later emitted_at
    return repo.seed(
        project_id=PROJECT,
        output_kind="outcome_confidence",
        output_payload={"index": index, "band": band},
    )


def test_drift_raises_one_derived_assessment_with_chr_and_events() -> None:
    repo = InMemoryChrRepo()
    store = InMemoryAcceptanceStore()
    pinned = _seed_pin(repo, index=82.0, band="high")
    latest = _seed_latest(repo, index=68.0, band="medium")
    uar = store.add_uar(version_pin=str(pinned.chr_id), action="accept", project_id=PROJECT)

    emitter = CollectingEventEmitter()
    raised = reconcile_acceptance_impact(
        project_id=PROJECT,
        store=store,
        chr_repo=repo,
        emitter=emitter,
        recompute_trigger="reanalysis",
    )

    # Exactly ONE Acceptance-Impact Assessment per drifted UAR.
    assert len(raised) == 1
    assessment = raised[0]
    assert isinstance(assessment, AcceptanceImpactAssessment)
    # Derived, never canonical / world-truth (hard rule #2; the seven (G)).
    assert assessment.epistemic_state == EpistemicState.DERIVED
    assert assessment.is_canonical is False
    # References the UAR + the pinned & latest CHRs (read-only lineage).
    assert assessment.uar_ref == uar["uar_id"]
    assert assessment.pinned_chr == str(pinned.chr_id)
    assert assessment.latest_chr == str(latest.chr_id)
    assert assessment.delta == -14.0
    assert assessment.band_changed is True

    # A CHR was appended (output_kind=acceptance_impact) with the lineage.
    impact_chrs = [r for r in repo.append_calls if r.output_kind == "acceptance_impact"]
    assert len(impact_chrs) == 1
    chr_row = impact_chrs[0]
    assert chr_row.upstream_lineage == {
        "uar_id": uar["uar_id"],
        "pinned_chr": str(pinned.chr_id),
        "latest_chr": str(latest.chr_id),
    }
    assert chr_row.provenance_ref == {"emitted_by": "evaluate"}
    assert chr_row.epistemic_state == EpistemicState.ATTESTED_OSLO  # the CHR receipt

    # Both events fired: the append pairing + the Acceptance-Impact signal.
    assert emitter.names.count("cognition_history_record_appended") == 1
    assert emitter.names.count("acceptance_impact_assessed") == 1
    assessed = next(p for n, p in emitter.events if n == "acceptance_impact_assessed")
    assert assessed["uar_id"] == uar["uar_id"]
    assert assessed["pinned_chr"] == str(pinned.chr_id)
    assert assessed["latest_chr"] == str(latest.chr_id)


def test_no_drift_below_threshold_raises_nothing() -> None:
    repo = InMemoryChrRepo()
    store = InMemoryAcceptanceStore()
    pinned = _seed_pin(repo, index=80.0, band="high")
    _seed_latest(repo, index=76.0, band="high")  # -4 pts, same band → no drift
    store.add_uar(version_pin=str(pinned.chr_id), action="accept", project_id=PROJECT)

    emitter = CollectingEventEmitter()
    raised = reconcile_acceptance_impact(
        project_id=PROJECT, store=store, chr_repo=repo, emitter=emitter
    )

    assert raised == []
    assert [r for r in repo.append_calls if r.output_kind == "acceptance_impact"] == []
    assert "acceptance_impact_assessed" not in emitter.names


def test_recompute_supersedes_prior_assessment_for_same_uar() -> None:
    """A second reconcile after a further move supersedes the prior assessment
    for the SAME UAR (append-only history; the prior CHR stays intact)."""
    repo = InMemoryChrRepo()
    store = InMemoryAcceptanceStore()
    pinned = _seed_pin(repo, index=82.0, band="high")
    _seed_latest(repo, index=68.0, band="medium")
    store.add_uar(version_pin=str(pinned.chr_id), action="accept", project_id=PROJECT)

    first = reconcile_acceptance_impact(project_id=PROJECT, store=store, chr_repo=repo)
    assert len(first) == 1
    first_chr = next(r for r in repo.append_calls if r.output_kind == "acceptance_impact")

    # The understanding moves further; a fresh recompute re-assesses.
    _seed_latest(repo, index=40.0, band="low")
    second = reconcile_acceptance_impact(project_id=PROJECT, store=store, chr_repo=repo)
    assert len(second) == 1

    impact_chrs = [r for r in repo.append_calls if r.output_kind == "acceptance_impact"]
    # APPEND, never overwrite — two assessment CHRs, the second superseding the first.
    assert len(impact_chrs) == 2
    second_chr = impact_chrs[1]
    assert str(second_chr.supersedes_chr_id) == str(first_chr.chr_id)
    # The prior assessment CHR is byte-intact (still present, unchanged payload).
    assert first_chr in repo.records


def test_only_accept_and_direct_edit_uars_are_reconciled() -> None:
    """reject/defer confirm nothing — they are not reconciled for impact."""
    repo = InMemoryChrRepo()
    store = InMemoryAcceptanceStore()
    pinned = _seed_pin(repo, index=82.0, band="high")
    _seed_latest(repo, index=60.0, band="medium")
    store.add_uar(version_pin=str(pinned.chr_id), action="reject", project_id=PROJECT)
    store.add_uar(version_pin=str(pinned.chr_id), action="defer", project_id=PROJECT)

    raised = reconcile_acceptance_impact(project_id=PROJECT, store=store, chr_repo=repo)
    assert raised == []


def test_direct_edit_uar_is_reconciled() -> None:
    repo = InMemoryChrRepo()
    store = InMemoryAcceptanceStore()
    pinned = _seed_pin(repo, index=82.0, band="high")
    _seed_latest(repo, index=60.0, band="medium")
    store.add_uar(
        version_pin=str(pinned.chr_id), action="direct_edit", project_id=PROJECT
    )

    raised = reconcile_acceptance_impact(project_id=PROJECT, store=store, chr_repo=repo)
    assert len(raised) == 1
