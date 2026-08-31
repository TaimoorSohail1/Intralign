"""DTM-0006 negative — transport forbidden/degraded behavior (C2). Pure.

- No event type outside the Event Model: the observed emitter REJECTS unknown
  names (inner validation first) and observes nothing for them — the structured
  log and span stream can never contain a non-A6 event.
- Observability never blocks the backbone: a failing OTel layer degrades to a
  warning; the event still reaches the inner emitter and the structured log.
"""

from __future__ import annotations

import json
import logging

import pytest

from backend.services.observability import emitters
from backend.services.observability.emitters import ObservedEventEmitter
from backend.services.observability.events import (
    CollectingEventEmitter,
    UnknownEventError,
)

LOGGER_NAME = "oslo.observability.events"


def test_unknown_event_rejected_and_not_observed(caplog) -> None:
    inner = CollectingEventEmitter()
    observed = ObservedEventEmitter(inner)

    with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
        with pytest.raises(UnknownEventError):
            observed.emit("free_form_logging", {"project_id": "p1"})

    assert inner.events == []  # nothing collected
    assert [r for r in caplog.records if r.name == LOGGER_NAME] == []  # nothing logged


def test_otel_failure_degrades_to_warning_never_blocks(monkeypatch, caplog) -> None:
    """Span attachment blowing up must not lose the event or raise (setup.py rule)."""
    inner = CollectingEventEmitter()
    observed = ObservedEventEmitter(inner)

    class _ExplodingTrace:
        @staticmethod
        def get_current_span():
            raise RuntimeError("otel exploded")

    import opentelemetry

    monkeypatch.setattr(opentelemetry, "trace", _ExplodingTrace, raising=True)

    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        observed.emit("recompute_started", {"project_id": "p1", "run_id": "r1"})

    # Event survived: collected AND structured-logged; failure was a warning.
    assert inner.names == ["recompute_started"]
    messages = [r for r in caplog.records if r.name == LOGGER_NAME]
    assert any(
        r.levelno == logging.INFO and json.loads(r.message)["event"] == "recompute_started"
        for r in messages
    )
    assert any(r.levelno == logging.WARNING for r in messages)


def test_structured_logging_failure_degrades_to_warning(monkeypatch, caplog) -> None:
    inner = CollectingEventEmitter()
    observed = ObservedEventEmitter(inner)

    def _bad_dumps(*args, **kwargs):
        raise TypeError("unserializable")

    monkeypatch.setattr(emitters.json, "dumps", _bad_dumps)
    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        observed.emit("stale_detected", {"project_id": "p1"})

    assert inner.names == ["stale_detected"]  # never lost
    assert any(
        r.levelno == logging.WARNING and r.name == LOGGER_NAME for r in caplog.records
    )
