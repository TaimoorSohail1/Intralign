"""Named-graph registry — one place to find every workflow.

The single index a developer opens to see all orchestration. Graphs register
here by name; the runner and transport look them up by name (never by importing
deep module paths).
"""

from __future__ import annotations

from collections.abc import Callable

# name -> graph factory. Populated as graphs are added under graphs/.
GRAPHS: dict[str, Callable[[], object]] = {}


def register(name: str, factory: Callable[[], object]) -> None:
    if name in GRAPHS:
        raise ValueError(f"graph already registered: {name}")
    GRAPHS[name] = factory


def get(name: str) -> Callable[[], object]:
    return GRAPHS[name]
