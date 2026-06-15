"""LangSmith run linkage (DL-054 condition 1; DTM-0006 part C) — config-only helper.

When ``LANGSMITH_TRACING=true`` (canonical env name from ``code/.env.example``)
and a run id is available, every CHR a recompute appends carries
``langsmith_run_id`` inside ``model_or_rule_version`` (the optional key the
retain model explicitly allows — LDM §2.2). Dev-without-LangSmith is allowed
(deep-task assumption A3): tracing off, or no run id, simply contributes
nothing — the CHR is valid without the key.

The run id used is the backbone run id (``GraphState.run_id``): it is the
durable thread id AND the id LangSmith correlates a traced run under, so the
CHR ↔ trace linkage is one key lookup.
"""

from __future__ import annotations

import os

ENV_LANGSMITH_TRACING = "LANGSMITH_TRACING"
LANGSMITH_RUN_ID_KEY = "langsmith_run_id"

_TRUTHY = frozenset({"true", "1", "yes"})


def langsmith_tracing_enabled() -> bool:
    """True when the canonical ``LANGSMITH_TRACING`` env flag is set truthy."""
    return os.environ.get(ENV_LANGSMITH_TRACING, "").strip().lower() in _TRUTHY


def langsmith_run_linkage(run_id: str | None) -> dict[str, str]:
    """The ``model_or_rule_version`` linkage entry for this run, or ``{}``.

    ``{}`` when tracing is disabled OR no run id is available — both are
    legitimate dev configurations (A3); the caller merges the result over the
    emission's declared ``model_or_rule_version`` without overwriting
    provider/model identity.
    """
    if not langsmith_tracing_enabled() or not run_id:
        return {}
    return {LANGSMITH_RUN_ID_KEY: run_id}
