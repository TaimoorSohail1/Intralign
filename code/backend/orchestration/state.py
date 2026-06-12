"""Typed graph state passed between LangGraph nodes.

State carries epistemic entities (shared.epistemic). Nodes read/extend state and
delegate the actual production to a responsibility module — they hold no domain
logic themselves (wiring, not work).
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
