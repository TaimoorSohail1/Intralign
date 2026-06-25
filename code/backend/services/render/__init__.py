"""Render service — maps governed cognition → Data Model v1.2 DTOs (DTM-0018).

Presentation only (IC-WE-DISCLOSE E0): Render reads the GOVERNED SOURCE (the
``derived.*_current`` live projections + the canonical retention rows) and emits
the EXTERNAL ``shared.entities`` DTOs the REST surface exposes verbatim (ADR-0003).
It produces no cognition, accepts nothing, mutates nothing, appends no CHR. An
internal ``shared.epistemic`` type is never serialized verbatim — the mappers
translate it, carrying the epistemic label (Attested/Derived + band + conflict).
"""

from backend.services.render.mappers import (
    acceptance_impact_to_dto,
    analysis_run_to_dto,
    caf_to_dto,
    confidence_to_dto,
    finding_to_dto,
    notification_to_dto,
    plan_fact_to_dto,
    project_to_dto,
    recommendation_to_dto,
    uar_to_dto,
)
from backend.services.render.read_seam import (
    ProjectionReader,
    SupabaseProjectionReader,
)

__all__ = [
    "ProjectionReader",
    "SupabaseProjectionReader",
    "acceptance_impact_to_dto",
    "analysis_run_to_dto",
    "caf_to_dto",
    "confidence_to_dto",
    "finding_to_dto",
    "notification_to_dto",
    "plan_fact_to_dto",
    "project_to_dto",
    "recommendation_to_dto",
    "uar_to_dto",
]
