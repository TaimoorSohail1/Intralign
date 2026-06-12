"""Run / resume entrypoint for orchestration graphs.

The single seam transport calls into. Opens the LangSmith trace, emits run
start/end governed-output events (services.observability), runs the named graph
with the durable checkpointer, and returns the derived result for render.

OSLO never self-accepts and never autonomously applies a SuggestedFix — the
runner produces Derived output only; canonical writes happen inside the retain
responsibility (append-only CognitionHistoryRecord).
"""

from __future__ import annotations

from orchestration.state import GraphState


def run(graph_name: str, state: GraphState) -> GraphState:
    """Execute a registered graph durably. Stub — implemented in Phase II (IC-WA-00R)."""
    raise NotImplementedError("Wire registry + checkpointer + observability under IC-WA-00R.")
