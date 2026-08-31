"""Typed graph state passed between LangGraph nodes.

State carries epistemic entities (shared.epistemic). Nodes read/extend state and
delegate the actual production to a responsibility module — they hold no domain
logic themselves (wiring, not work).

DTM-0005 (IC-WA-00R) extends the state additively with the recompute-backbone
fields: the validated trigger, the declared emission specs, the appended CHR
ids, the cognition state, the live-projection reference (last-known-good on
failure, A3.7) and failure info for the mark_failed edge.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class GraphState(BaseModel):
    """Run-scoped state for a cognition workflow (Fast Pass / Deep Pass)."""

    project_id: str
    run_id: str | None = None              # LangSmith run id — recorded into the CHR
    inputs: dict[str, Any] = Field(default_factory=dict)
    outputs: dict[str, Any] = Field(default_factory=dict)  # derived projections (non-canonical)

    # --- DTM-0005 / IC-WA-00R additive fields (recompute backbone) ---
    trigger: dict[str, Any] | None = None  # validated TriggerClaim dump (A3.2)
    emissions: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Declared emission specs the retain stage appends CHRs for.",
    )
    appended_chr_ids: list[str] = Field(
        default_factory=list,
        description="CHR ids appended by THIS run (one per emission, A3.5).",
    )
    cognition_state: str | None = None     # A3.6 value; moved by mark_* nodes only
    live_projection_ref: dict[str, Any] | None = Field(
        default=None,
        description=(
            "Reference to the live Derived projection. Replaced ONLY by "
            "mark_current; mark_failed leaves it untouched — last-known-good "
            "retained (A3.7)."
        ),
    )
    failure: dict[str, Any] | None = None  # set by a failing stage; routes to mark_failed
