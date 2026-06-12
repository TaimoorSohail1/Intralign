"""Named-graph registry — one place to find every workflow.

The single index a developer opens to see all orchestration. Graphs register
here by name; the runner and transport look them up by name (never by importing
deep module paths).

A factory takes the wiring keyword arguments (checkpointer, emitter, repo,
stage overrides) and returns a compiled graph; the runner calls it per run.
"""

from __future__ import annotations

from collections.abc import Callable

# name -> graph factory. Populated as graphs are added under graphs/.
GRAPHS: dict[str, Callable[..., object]] = {}


def register(name: str, factory: Callable[..., object]) -> None:
    if name in GRAPHS:
        raise ValueError(f"graph already registered: {name}")
    GRAPHS[name] = factory


def get(name: str) -> Callable[..., object]:
    if name not in GRAPHS:
        _load_default_graphs()
    if name not in GRAPHS:
        raise KeyError(
            f"no graph registered under {name!r} — known graphs: "
            f"{sorted(GRAPHS) or '(none)'}"
        )
    return GRAPHS[name]


def _load_default_graphs() -> None:
    """Import the graph modules so their register() side effects run (lazy,
    avoids a circular import: graph modules import this registry)."""
    import backend.orchestration.graphs.deep_pass  # noqa: F401
