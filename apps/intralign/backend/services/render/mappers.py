"""Render mappers — governed cognition → Data Model v1.2 DTO (DTM-0018; ADR-0003).

Render is presentation only (IC-WE-DISCLOSE E0): it maps the governed objects
into the EXTERNAL ``shared.entities`` DTOs the REST surface exposes verbatim. It
produces NO cognition, scores nothing, accepts nothing, and appends no Cognition
History Record (one-producer / CHR discipline preserved).

The headline invariant (decision #4; negative-proven): an internal
``shared.epistemic`` cognition type is NEVER serialized verbatim over REST. Every
mapper here reads the GOVERNED SOURCE — a ``derived.*_current`` projection row
(LDM §3.1: ``current_payload`` + the epistemic-safety envelope) or a canonical
retention row — and emits the Data-Model DTO, which carries the epistemic label
(Attested/Derived + confidence band + conflict) so the UI renders without
re-deriving (decision #5). A Derived DTO ALWAYS carries its ``label`` envelope.
"""

from __future__ import annotations

from typing import Any

from shared.entities import (
    AcceptanceImpactAssessment,
    AnalysisRun,
    CAFDimensionView,
    CAFState,
    ConfidenceState,
    DerivedEnvelope,
    Finding,
    GovernedCount,
    HistoryEntry,
    Issue,
    Notification,
    Overview,
    PlanFact,
    Project,
    Recommendation,
    UserAcceptanceRecord,
)


def _envelope(row: dict[str, Any]) -> DerivedEnvelope:
    """Build the epistemic-safety envelope from a ``derived.*_current`` row (LDM §3.1).

    The label TRAVELS with every Derived object: epistemic_label (always
    'derived'), the band (the user-facing value), the 0–100 value (explainability
    only), the conflict marker, and the lineage to the CHR version presented.
    """
    chr_ref = row.get("current_chr_ref")
    return DerivedEnvelope(
        epistemic_label=str(row.get("epistemic_label") or "derived"),
        confidence_value=row.get("confidence_value"),
        confidence_band=row.get("confidence_band"),
        conflict_state=row.get("conflict_state") or "none",
        current_chr_ref=str(chr_ref) if chr_ref is not None else None,
    )


def _payload(row: dict[str, Any]) -> dict[str, Any]:
    """The cognition snapshot a projection row carries (``current_payload``)."""
    payload = row.get("current_payload")
    return dict(payload) if isinstance(payload, dict) else {}


# --- Derived cognition projections → DTO --------------------------------------

def finding_to_dto(row: dict[str, Any]) -> Finding:
    """Map a ``derived.finding_current`` row → the Finding DTO (Data Model §11)."""
    p = _payload(row)
    return Finding(
        finding_id=str(p.get("finding_id") or row.get("projection_id")),
        project_id=str(row["project_id"]),
        first_seen_run_id=p.get("first_seen_run_id"),
        last_updated_run_id=p.get("last_updated_run_id"),
        finding_type=_finding_type(p.get("finding_type"), p.get("gap_kind")),
        affected_dimensions=list(p.get("affected_dimensions") or []),
        severity=p.get("severity"),
        status=p.get("status") or "detected",
        summary=p.get("summary"),
        evidence_links=list(p.get("evidence_anchors") or p.get("evidence_links") or []),
        created_at=p.get("created_at"),
        updated_at=p.get("updated_at"),
        closed_at=p.get("closed_at"),
        label=_envelope(row),
    )


# The internal Finding taxonomy (gap/conflict/risk + gap_kind) maps onto the
# Data-Model v1.2 §11 flat taxonomy. A conflict stays a conflict; a gap maps by
# its structural sub-kind; a risk maps to inference (a risk signal is an inferred
# implication). Defaults to ambiguity when the source carries no recognizable
# type (never invented — the source value wins when it is already a Data-Model one).
_DM_FINDING_TYPES = frozenset(
    {
        "missing_information",
        "ambiguity",
        "assumption",
        "inference",
        "conflict",
        "constraint",
        "coverage_gap",
    }
)
_GAP_KIND_TO_DM = {
    "coverage": "coverage_gap",
    "alignment": "missing_information",
    "quality": "ambiguity",
    "smart": "ambiguity",
}


def _finding_type(finding_type: Any, gap_kind: Any) -> str:
    ft = str(finding_type) if finding_type is not None else ""
    if ft in _DM_FINDING_TYPES:
        return ft
    if ft == "conflict":
        return "conflict"
    if ft == "gap":
        return _GAP_KIND_TO_DM.get(str(gap_kind), "coverage_gap")
    if ft == "risk":
        return "inference"
    return "ambiguity"


def issue_to_dto(row: dict[str, Any]) -> Issue:
    """Map a ``derived.issue_current`` row → the Issue DTO (Object Model §8).

    An Issue is the Derived, first-class prioritized Finding (``Issue ──from──>
    Finding``, severity an attribute). It carries the Finding's Data-Model field
    set PLUS its own identity (``issue_id``) and the source-Finding lineage
    (``finding_id``). The epistemic label travels (Derived + band + conflict). The
    internal-only payload fields (``mode`` / ``confidence_stage`` /
    ``understanding_state`` / ``epistemic_state``) are NOT carried onto the DTO —
    no internal cognition leaks verbatim (decision #4; negative-proven). Mirrors
    ``finding_to_dto`` for the shared Finding field set.
    """
    p = _payload(row)
    return Issue(
        issue_id=str(p.get("issue_id") or row.get("projection_id")),
        project_id=str(row["project_id"]),
        finding_id=str(p.get("finding_id") or ""),
        first_seen_run_id=p.get("first_seen_run_id"),
        last_updated_run_id=p.get("last_updated_run_id"),
        finding_type=_finding_type(p.get("finding_type"), p.get("gap_kind")),
        affected_dimensions=list(p.get("affected_dimensions") or []),
        severity=p.get("severity"),
        status=p.get("status") or "detected",
        summary=p.get("summary"),
        evidence_links=list(p.get("evidence_anchors") or p.get("evidence_links") or []),
        created_at=p.get("created_at"),
        updated_at=p.get("updated_at"),
        closed_at=p.get("closed_at"),
        label=_envelope(row),
    )


def recommendation_to_dto(row: dict[str, Any]) -> Recommendation:
    """Map a ``derived.recommendation_current`` row → the Recommendation DTO (§12)."""
    p = _payload(row)
    return Recommendation(
        recommendation_id=str(p.get("recommendation_id") or row.get("projection_id")),
        project_id=str(row["project_id"]),
        finding_id=str(p.get("finding_id") or p.get("anchor") or ""),
        first_seen_run_id=p.get("first_seen_run_id"),
        recommendation_type=_recommendation_type(p.get("recommendation_type")),
        status=_recommendation_status(p.get("status") or p.get("state")),
        title=p.get("title"),
        description=p.get("description") or p.get("summary"),
        rationale=p.get("rationale"),
        expected_dimension=p.get("expected_dimension"),
        effort=p.get("effort"),
        artifact_reference=p.get("artifact_reference"),
        artifact_element_reference=p.get("artifact_element_reference"),
        supersedes_recommendation_id=p.get("supersedes_recommendation_id"),
        created_at=p.get("created_at"),
        updated_at=p.get("updated_at"),
        label=_envelope(row),
    )


# Internal Advise recommendation_type (suggested_action/candidate_improvement/
# validation) → the Data-Model v1.2 §12 three-value enum.
_REC_TYPE_TO_DM = {
    "suggested_action": "improvement",
    "candidate_improvement": "improvement",
    "improvement": "improvement",
    "validation": "validation",
    "suggested_fix": "suggested_fix",
}
_DM_REC_STATUSES = frozenset(
    {"generated", "accepted", "rejected", "deferred", "implemented", "superseded"}
)


def _recommendation_type(value: Any) -> str | None:
    if value is None:
        return None
    return _REC_TYPE_TO_DM.get(str(value), "improvement")


def _recommendation_status(value: Any) -> str:
    v = str(value) if value is not None else ""
    return v if v in _DM_REC_STATUSES else "generated"


def confidence_to_dto(row: dict[str, Any]) -> ConfidenceState:
    """Map a ``derived.outcome_confidence_current`` (or confidence) row → ConfidenceState."""
    p = _payload(row)
    return ConfidenceState(
        project_id=str(row["project_id"]),
        confidence_state_id=row.get("projection_id"),
        analysis_run_id=p.get("analysis_run_id"),
        outcome_confidence_value=p.get("index", row.get("confidence_value")),
        confidence_band=row.get("confidence_band") or p.get("band"),
        reliability_qualifier=p.get("reliability_qualifier"),
        false_confidence_flagged=bool(p.get("false_confidence_flagged", False)),
        basis=list(p.get("basis") or []),
        supersedes_confidence_state_id=p.get("supersedes_confidence_state_id"),
        created_at=p.get("created_at") or row.get("recomputed_at"),
        label=_envelope(row),
    )


def caf_to_dto(row: dict[str, Any]) -> CAFState:
    """Map a ``derived.caf_current`` row → the CAFState DTO (three co-equal dimensions)."""
    p = _payload(row)
    dims = p.get("dimensions") or {}

    def _dim(name: str) -> CAFDimensionView:
        d = dims.get(name) or {}
        return CAFDimensionView(
            dimension=name,
            index=float(d.get("index", 0.0)),
            band=d.get("band") or row.get("confidence_band") or "low",
            reliability=str(d.get("reliability", "low")),
        )

    return CAFState(
        project_id=str(row["project_id"]),
        clarity=_dim("clarity"),
        alignment=_dim("alignment"),
        feasibility=_dim("feasibility"),
        label=_envelope(row),
    )


def acceptance_impact_to_dto(row: dict[str, Any]) -> AcceptanceImpactAssessment:
    """Map a ``derived.acceptance_impact_current`` row → the AcceptanceImpact DTO (§U1.3)."""
    p = _payload(row)
    return AcceptanceImpactAssessment(
        project_id=str(row["project_id"]),
        uar_ref=str(p.get("uar_ref") or ""),
        pinned_chr=str(p.get("pinned_chr") or ""),
        latest_chr=str(p.get("latest_chr") or ""),
        delta=float(p.get("delta", 0.0)),
        band_changed=bool(p.get("band_changed", False)),
        pinned_band=p.get("pinned_band"),
        latest_band=p.get("latest_band"),
        label=_envelope(row),
    )


# --- Overview / counts (DTM-0038 — presentation of governed objects) ----------

def overview_to_dto(
    project_id: str,
    *,
    finding_rows: list[dict[str, Any]],
    issue_rows: list[dict[str, Any]],
    recommendation_rows: list[dict[str, Any]],
    outcome_confidence_rows: list[dict[str, Any]],
    caf_rows: list[dict[str, Any]],
) -> Overview:
    """Aggregate the governed lists → the Overview DTO (counts + labelled aggregates).

    CRITICAL (Wave E not-project-health rule): every field is a COUNT of, or a
    labelled pass-through of, an already-governed object. The counts are sizes of
    the governed lists; the Outcome-Confidence + CAF are mapped through their
    existing Derived mappers (the band travels). NOTHING here computes a health /
    readiness / probability score — there is no such field on the DTO.
    """
    return Overview(
        project_id=str(project_id),
        counts=[
            GovernedCount(label="findings", kind="finding", count=len(finding_rows)),
            GovernedCount(label="issues", kind="issue", count=len(issue_rows)),
            GovernedCount(
                label="recommendations", kind="recommendation",
                count=len(recommendation_rows),
            ),
        ],
        outcome_confidence=(
            confidence_to_dto(outcome_confidence_rows[0]) if outcome_confidence_rows else None
        ),
        caf=caf_to_dto(caf_rows[0]) if caf_rows else None,
    )


# --- History feed (DTM-0038 — the Cognition-History trail, read exact) ---------

def history_entry_to_dto(row: dict[str, Any]) -> HistoryEntry:
    """Map a ``cognition_history_record`` row → the HistoryEntry DTO (read exact).

    The entry surfaces the CHR's identity + lineage exactly as the append-only
    receipt holds them (LDM §2.2) — it re-derives nothing. ``epistemic_label`` is
    ``attested-oslo`` (a CHR is OSLO-self-attested by definition).
    """
    chr_id = row.get("chr_id")
    supersedes = row.get("supersedes_chr_id")
    return HistoryEntry(
        chr_id=str(chr_id),
        project_id=str(row.get("project_id")),
        output_kind=str(row.get("output_kind")),
        recompute_trigger=row.get("recompute_trigger"),
        supersedes_chr_id=str(supersedes) if supersedes is not None else None,
        emitted_at=str(row["emitted_at"]) if row.get("emitted_at") is not None else None,
        epistemic_label=str(row.get("epistemic_state") or "attested-oslo"),
    )


# --- Canonical receipts → DTO (Wave U; user-attested, never truth) ------------

def uar_to_dto(row: dict[str, Any]) -> UserAcceptanceRecord:
    """Map a ``user_acceptance_record`` row → the UAR DTO (DTM-0008; attested-user)."""
    return UserAcceptanceRecord(
        uar_id=str(row.get("uar_id")),
        project_id=str(row["project_id"]),
        user_id=row.get("user_id"),
        action=str(row.get("action")),
        target_kind=row.get("target_kind"),
        version_pin=str(row.get("version_pin")),
        epistemic_label=str(row.get("epistemic_state") or "attested-user"),
        confirmed_at=row.get("confirmed_at"),
        created_at=row.get("created_at"),
    )


def plan_fact_to_dto(row: dict[str, Any]) -> PlanFact:
    """Map a plan-fact ``attested_assertion`` row → the PlanFact DTO (DTM-0016)."""
    prov = row.get("provenance_ref") or {}
    return PlanFact(
        plan_fact_id=str(row.get("assertion_id")),
        project_id=str(row["project_id"]),
        proposition=str(row.get("proposition") or ""),
        content_type=str(row.get("content_type") or "fact"),
        attested_by_user=row.get("attesting_source") or prov.get("user_id"),
        version_pin=prov.get("version_pin") or (row.get("source_ref") or {}).get("version_pin"),
        epistemic_label=str(row.get("epistemic_state") or "attested-user"),
        created_at=row.get("created_at"),
    )


# --- Platform objects → DTO (no epistemic cognition label; awareness only) ----

def project_to_dto(row: dict[str, Any]) -> Project:
    """Map a project row → the Project DTO (Data Model §7)."""
    return Project(
        project_id=str(row.get("project_id")),
        workspace_id=str(row.get("workspace_id")),
        created_by_user_id=row.get("created_by_user_id"),
        title=row.get("title"),
        description=row.get("description"),
        lifecycle_state=row.get("lifecycle_state") or "created",
        current_confidence_state_id=row.get("current_confidence_state_id"),
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
    )


def analysis_run_to_dto(row: dict[str, Any]) -> AnalysisRun:
    """Map an analysis_run row → the AnalysisRun DTO (Data Model §10)."""
    return AnalysisRun(
        analysis_run_id=str(row.get("analysis_run_id")),
        project_id=str(row.get("project_id")),
        run_type=row.get("run_type") or "fast_analysis_pass",
        run_status=row.get("run_status") or "queued",
        previous_run_id=row.get("previous_run_id"),
        started_at=row.get("started_at"),
        completed_at=row.get("completed_at"),
    )


def notification_to_dto(row: dict[str, Any]) -> Notification:
    """Map a notification row → the Notification DTO (Data Model §13; awareness only)."""
    return Notification(
        notification_id=str(row.get("notification_id")),
        workspace_id=str(row.get("workspace_id")),
        project_id=row.get("project_id"),
        source_object_type=row.get("source_object_type"),
        source_object_id=str(row.get("source_object_id")),
        event_type=str(row.get("event_type")),
        target_user_id=row.get("target_user_id"),
        state=row.get("state") or "created",
        created_at=row.get("created_at"),
        viewed_at=row.get("viewed_at"),
        dismissed_at=row.get("dismissed_at"),
        expired_at=row.get("expired_at"),
    )
