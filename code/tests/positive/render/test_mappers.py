"""Render mapper suite (DTM-0018) — governed cognition → Data Model v1.2 DTO.

Each mapper reads the GOVERNED SOURCE (a ``derived.*_current`` projection row or
a canonical retention row) and emits the external DTO with the epistemic label
intact (Attested/Derived + confidence band + conflict). These are the positive
proofs that the label TRAVELS with every Derived object (decision #5).
"""

from __future__ import annotations

from backend.services.render import (
    acceptance_impact_to_dto,
    caf_to_dto,
    confidence_to_dto,
    finding_to_dto,
    history_entry_to_dto,
    issue_to_dto,
    notification_to_dto,
    overview_to_dto,
    plan_fact_to_dto,
    project_to_dto,
    recommendation_to_dto,
    uar_to_dto,
)
from shared.entities import (
    AcceptanceImpactAssessment,
    CAFState,
    ConfidenceState,
    Finding,
    HistoryEntry,
    Issue,
    Notification,
    Overview,
    PlanFact,
    Project,
    Recommendation,
    UserAcceptanceRecord,
)

PROJECT = "11111111-1111-1111-1111-111111111111"


def _projection_row(output_kind: str, payload: dict, **envelope) -> dict:
    """A ``derived.<kind>_current`` row (LDM §3.1) with the epistemic envelope."""
    return {
        "projection_id": "proj-1",
        "project_id": PROJECT,
        "output_kind": output_kind,
        "current_payload": payload,
        "current_chr_ref": "chr-1",
        "epistemic_label": "derived",
        "confidence_value": envelope.get("confidence_value", 62.0),
        "confidence_band": envelope.get("confidence_band", "medium"),
        "conflict_state": envelope.get("conflict_state", "none"),
        "recomputed_at": "2026-06-25T00:00:00Z",
    }


def test_finding_mapper_carries_derived_label() -> None:
    row = _projection_row(
        "finding",
        {
            "finding_id": "f-1",
            "finding_type": "conflict",
            "summary": "Two assertions contradict.",
            "evidence_anchors": ["a-0", "a-1"],
            "status": "detected",
        },
        conflict_state="contested",
    )
    dto = finding_to_dto(row)
    assert isinstance(dto, Finding)
    assert dto.finding_id == "f-1"
    assert dto.finding_type.value == "conflict"
    assert dto.evidence_links == ["a-0", "a-1"]
    # The epistemic label travels: Derived + band + conflict (decision #5).
    assert dto.label.epistemic_label == "derived"
    assert dto.label.confidence_band.value == "medium"
    assert dto.label.conflict_state.value == "contested"
    assert dto.label.current_chr_ref == "chr-1"


def test_finding_gap_maps_to_datamodel_taxonomy() -> None:
    row = _projection_row(
        "finding",
        {"finding_id": "f-2", "finding_type": "gap", "gap_kind": "coverage",
         "summary": "no constraint evidence", "evidence_anchors": ["a-0"]},
    )
    dto = finding_to_dto(row)
    assert dto.finding_type.value == "coverage_gap"


def test_issue_mapper_carries_label_and_lineage() -> None:
    """An Issue is the Derived prioritized Finding: label travels + source lineage."""
    row = _projection_row(
        "issue",
        {
            "issue_id": "i-1",
            "finding_id": "f-1",
            "finding_type": "conflict",
            "severity": "critical",
            "summary": "Two assertions contradict.",
            "evidence_anchors": ["a-0", "a-1"],
            "status": "detected",
        },
        conflict_state="contested",
    )
    dto = issue_to_dto(row)
    assert isinstance(dto, Issue)
    assert dto.issue_id == "i-1"
    assert dto.finding_id == "f-1"  # source-Finding lineage
    assert dto.finding_type.value == "conflict"
    assert dto.severity.value == "critical"
    assert dto.evidence_links == ["a-0", "a-1"]
    # The epistemic label travels: Derived + band + conflict (decision #5).
    assert dto.label.epistemic_label == "derived"
    assert dto.label.confidence_band.value == "medium"
    assert dto.label.conflict_state.value == "contested"
    assert dto.label.current_chr_ref == "chr-1"


def test_issue_mapper_maps_gap_taxonomy() -> None:
    row = _projection_row(
        "issue",
        {"issue_id": "i-2", "finding_id": "f-2", "finding_type": "gap",
         "gap_kind": "coverage", "severity": "moderate", "summary": "x",
         "evidence_anchors": ["a-0"]},
    )
    dto = issue_to_dto(row)
    assert dto.finding_type.value == "coverage_gap"


def test_overview_mapper_counts_and_labelled_aggregates() -> None:
    """Overview is counts of governed lists + labelled aggregates (never health)."""
    findings = [_projection_row("finding", {"finding_id": f"f-{i}"}) for i in range(3)]
    issues = [_projection_row("issue", {"issue_id": f"i-{i}", "finding_id": f"f-{i}"})
              for i in range(2)]
    recs = [_projection_row("recommendation", {"recommendation_id": "r-1", "anchor": "f-1"})]
    oc = [_projection_row("outcome_confidence",
                          {"index": 62.0, "band": "medium", "basis": ["clarity"]})]
    caf = [_projection_row("caf", {"dimensions": {
        "clarity": {"index": 70.0, "band": "medium", "reliability": "moderate"},
        "alignment": {"index": 55.0, "band": "medium", "reliability": "low"},
        "feasibility": {"index": 80.0, "band": "high", "reliability": "high"}}})]
    dto = overview_to_dto(
        PROJECT, finding_rows=findings, issue_rows=issues, recommendation_rows=recs,
        outcome_confidence_rows=oc, caf_rows=caf,
    )
    assert isinstance(dto, Overview)
    counts = {c.kind: c.count for c in dto.counts}
    assert counts == {"finding": 3, "issue": 2, "recommendation": 1}
    # Each count is labelled (presentation of governed objects).
    assert {c.label for c in dto.counts} == {"findings", "issues", "recommendations"}
    # The aggregates carry their Derived band (pass-through, not a computed health).
    assert dto.outcome_confidence is not None
    assert dto.outcome_confidence.confidence_band.value == "medium"
    assert dto.outcome_confidence.label.epistemic_label == "derived"
    assert dto.caf is not None
    assert dto.caf.feasibility.band.value == "high"


def test_overview_dto_has_no_health_field() -> None:
    """The Overview DTO carries NO health/readiness/score/probability field (Wave E)."""
    fields = set(Overview.model_fields)
    banned = {"health", "readiness", "score", "probability", "project_health", "status"}
    assert not (fields & banned), f"Overview leaks a health-shaped field: {fields & banned}"


def test_history_entry_mapper_is_derived_trail_read_exact() -> None:
    """A history entry reads the CHR exact + carries the OSLO-self-attested label."""
    row = {
        "chr_id": "chr-2", "project_id": PROJECT, "output_kind": "outcome_confidence",
        "recompute_trigger": "knowledge-change", "supersedes_chr_id": "chr-1",
        "emitted_at": "2026-06-25T01:00:00Z", "epistemic_state": "attested-oslo",
        "output_payload": {"index": 55.0}, "model_or_rule_version": {"model": "x"},
    }
    dto = history_entry_to_dto(row)
    assert isinstance(dto, HistoryEntry)
    assert dto.chr_id == "chr-2"
    assert dto.output_kind == "outcome_confidence"
    assert dto.recompute_trigger == "knowledge-change"
    assert dto.supersedes_chr_id == "chr-1"  # the supersession link (drift backbone)
    assert dto.epistemic_label == "attested-oslo"
    # No internal CHR field leaks onto the trail DTO.
    assert "output_payload" not in HistoryEntry.model_fields
    assert "model_or_rule_version" not in HistoryEntry.model_fields


def test_recommendation_mapper_maps_type_and_status() -> None:
    row = _projection_row(
        "recommendation",
        {
            "recommendation_id": "r-1",
            "recommendation_type": "candidate_improvement",
            "anchor": "f-1",
            "summary": "Clarify the scope statement.",
            "state": "generated",
        },
    )
    dto = recommendation_to_dto(row)
    assert isinstance(dto, Recommendation)
    assert dto.recommendation_id == "r-1"
    assert dto.finding_id == "f-1"
    assert dto.recommendation_type.value == "improvement"  # mapped to DM 3-value enum
    assert dto.status.value == "generated"
    assert dto.label.epistemic_label == "derived"


def test_confidence_mapper_band_is_user_facing() -> None:
    row = _projection_row(
        "outcome_confidence",
        {"index": 62.0, "band": "medium", "reliability_qualifier": "moderate",
         "basis": ["clarity", "alignment"], "false_confidence_flagged": False},
    )
    dto = confidence_to_dto(row)
    assert isinstance(dto, ConfidenceState)
    assert dto.confidence_band.value == "medium"
    assert dto.outcome_confidence_value == 62.0
    assert dto.basis == ["clarity", "alignment"]
    assert dto.label.epistemic_label == "derived"


def test_caf_mapper_three_dimensions() -> None:
    row = _projection_row(
        "caf",
        {"dimensions": {
            "clarity": {"index": 70.0, "band": "medium", "reliability": "moderate"},
            "alignment": {"index": 55.0, "band": "medium", "reliability": "low"},
            "feasibility": {"index": 80.0, "band": "high", "reliability": "high"},
        }},
    )
    dto = caf_to_dto(row)
    assert isinstance(dto, CAFState)
    assert dto.clarity.dimension.value == "clarity"
    assert dto.feasibility.band.value == "high"
    assert dto.label.epistemic_label == "derived"


def test_acceptance_impact_mapper_is_derived_reference_only() -> None:
    row = _projection_row(
        "acceptance_impact",
        {"uar_ref": "uar-1", "pinned_chr": "chr-a", "latest_chr": "chr-b",
         "delta": -12.0, "band_changed": True, "pinned_band": "high", "latest_band": "medium"},
    )
    dto = acceptance_impact_to_dto(row)
    assert isinstance(dto, AcceptanceImpactAssessment)
    assert dto.uar_ref == "uar-1"
    assert dto.delta == -12.0
    assert dto.band_changed is True
    assert dto.label.epistemic_label == "derived"


def test_uar_mapper_is_attested_user() -> None:
    row = {
        "uar_id": "uar-1", "project_id": PROJECT, "user_id": "u-1",
        "action": "accept", "target_kind": "recommendation", "version_pin": "chr-1",
        "epistemic_state": "attested-user", "created_at": "2026-06-25T00:00:00Z",
    }
    dto = uar_to_dto(row)
    assert isinstance(dto, UserAcceptanceRecord)
    assert dto.epistemic_label == "attested-user"
    assert dto.version_pin == "chr-1"


def test_plan_fact_mapper_is_attested_user() -> None:
    row = {
        "assertion_id": "pf-1", "project_id": PROJECT, "proposition": "Scope excludes X.",
        "content_type": "fact", "attesting_source": "u-1", "epistemic_state": "attested-user",
        "provenance_ref": {"version_pin": "chr-1", "user_id": "u-1"},
        "created_at": "2026-06-25T00:00:00Z",
    }
    dto = plan_fact_to_dto(row)
    assert isinstance(dto, PlanFact)
    assert dto.epistemic_label == "attested-user"
    assert dto.proposition == "Scope excludes X."
    assert dto.attested_by_user == "u-1"


def test_project_mapper() -> None:
    row = {
        "project_id": "p-1", "workspace_id": "w-1", "title": "Demo",
        "lifecycle_state": "oriented", "created_at": "2026-06-25T00:00:00Z",
    }
    dto = project_to_dto(row)
    assert isinstance(dto, Project)
    assert dto.lifecycle_state.value == "oriented"


def test_notification_mapper_awareness_only() -> None:
    row = {
        "notification_id": "n-1", "workspace_id": "w-1", "project_id": PROJECT,
        "source_object_type": "finding", "source_object_id": "f-1",
        "event_type": "created", "state": "created",
    }
    dto = notification_to_dto(row)
    assert isinstance(dto, Notification)
    assert dto.state.value == "created"
    assert dto.source_object_type.value == "finding"
