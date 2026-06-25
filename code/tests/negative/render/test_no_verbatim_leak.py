"""Render negatives (DTM-0018) — the no-verbatim-leak + label invariants (Critical).

decision #4 (negative-proven): an internal ``shared.epistemic`` cognition type is
NEVER serialized verbatim over REST. The render mappers emit the EXTERNAL
``shared.entities`` DTOs only; a Derived DTO ALWAYS carries its epistemic label.
"""

from __future__ import annotations

import inspect

import shared.epistemic as epistemic
from backend.services.render import (
    confidence_to_dto,
    finding_to_dto,
    recommendation_to_dto,
)
from shared.entities import Finding, Recommendation

PROJECT = "11111111-1111-1111-1111-111111111111"


def _row(output_kind: str, payload: dict, **env) -> dict:
    return {
        "projection_id": "proj-1", "project_id": PROJECT, "output_kind": output_kind,
        "current_payload": payload, "current_chr_ref": "chr-1",
        "epistemic_label": "derived",
        "confidence_value": env.get("confidence_value", 60.0),
        "confidence_band": env.get("confidence_band", "medium"),
        "conflict_state": env.get("conflict_state", "none"),
        "recomputed_at": "2026-06-25T00:00:00Z",
    }


def test_finding_dto_is_not_the_internal_cognition_type() -> None:
    """The render output is the EXTERNAL DTO, never the internal Finding (Critical)."""
    dto = finding_to_dto(_row("finding", {
        "finding_id": "f-1", "finding_type": "conflict", "summary": "x",
        "evidence_anchors": ["a-0"],
    }))
    assert isinstance(dto, Finding)
    # Structurally distinct types: the internal cognition type lives in
    # shared.epistemic and is NOT what crosses the REST boundary.
    assert type(dto).__module__ == "shared.entities"
    assert type(dto) is not epistemic.Finding


def test_recommendation_dto_carries_no_internal_only_fields() -> None:
    """A Derived DTO carries no field absent from Data Model v1.2 (no internal leak)."""
    dto = recommendation_to_dto(_row("recommendation", {
        "recommendation_id": "r-1", "anchor": "f-1", "summary": "y",
        "state": "generated", "recommendation_type": "validation",
        # internal-only attribute that must NOT appear on the external DTO:
        "model_or_rule_version": "advise-v0",
        "understanding_state": "initial",
    }))
    assert isinstance(dto, Recommendation)
    field_names = set(Recommendation.model_fields)
    # The internal-cognition-only attributes are not Data-Model v1.2 fields.
    assert "model_or_rule_version" not in field_names
    assert "understanding_state" not in field_names
    assert "confidence_stage" not in field_names


def test_every_derived_dto_carries_an_epistemic_label() -> None:
    """Missing the epistemic label on a Derived object is a Critical trust failure."""
    finding = finding_to_dto(_row("finding", {
        "finding_id": "f-1", "finding_type": "gap", "gap_kind": "coverage",
        "summary": "x", "evidence_anchors": ["a-0"],
    }))
    conf = confidence_to_dto(_row("outcome_confidence", {
        "index": 60.0, "band": "medium", "reliability_qualifier": "moderate",
        "basis": ["clarity"],
    }))
    for dto in (finding, conf):
        assert dto.label is not None
        assert dto.label.epistemic_label == "derived"
        assert dto.label.confidence_band is not None  # band travels (decision #5)


def test_internal_epistemic_types_are_not_imported_by_the_transport_dtos() -> None:
    """shared.entities defines its OWN DTO types — it does not re-export the internal ones."""
    import shared.entities as entities

    src = inspect.getsource(entities)
    # The external DTO module must not alias the internal cognition classes.
    assert "from shared.epistemic import" not in src
