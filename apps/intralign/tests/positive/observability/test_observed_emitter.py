"""DTM-0006 positive — ObservedEventEmitter transport (OBS-WA-00R C2). Pure.

The decorator (1) delegates to the inner emitter (CollectingEventEmitter
consumers unaffected), (2) logs each A6 event as ONE structured-JSON line, and
(3) attaches the event as an OTel span event when a tracer is active — while
degrading to a clean no-op when no span is recording (setup.py philosophy).
"""

from __future__ import annotations

import json
import logging

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
    InMemorySpanExporter,
)

from backend.services.observability.emitters import ObservedEventEmitter
from backend.services.observability.events import (
    EVENT_NAMES,
    CollectingEventEmitter,
)

LOGGER_NAME = "oslo.observability.events"


def test_delegates_to_inner_collecting_emitter() -> None:
    inner = CollectingEventEmitter()
    observed = ObservedEventEmitter(inner)
    observed.emit("recompute_started", {"project_id": "p1", "run_id": "r1"})

    assert inner.names == ["recompute_started"]
    assert inner.events[0][1] == {"project_id": "p1", "run_id": "r1"}
    # Convenience delegation: collecting surface visible through the wrapper.
    assert observed.names == ["recompute_started"]
    assert observed.inner is inner


def test_wrap_is_idempotent() -> None:
    inner = CollectingEventEmitter()
    once = ObservedEventEmitter.wrap(inner)
    twice = ObservedEventEmitter.wrap(once)
    assert twice is once  # runner.submit_trigger -> runner.run never double-wraps
    assert once.inner is inner


def test_each_event_logged_as_structured_json(caplog) -> None:
    emitter = ObservedEventEmitter(CollectingEventEmitter())
    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        for name in EVENT_NAMES:
            emitter.emit(name, {"project_id": "p1", "run_id": "r1", "i": 1})

    lines = [r.message for r in caplog.records if r.name == LOGGER_NAME]
    assert len(lines) == len(EVENT_NAMES)
    for name, line in zip(EVENT_NAMES, lines):
        parsed = json.loads(line)  # structured: every line is valid JSON
        assert parsed["event"] == name
        assert parsed["payload"] == {"project_id": "p1", "run_id": "r1", "i": 1}


def test_attaches_otel_span_event_when_tracer_active() -> None:
    exporter = InMemorySpanExporter()
    provider = TracerProvider()  # local provider — global tracer state untouched
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    tracer = provider.get_tracer("dtm-0006-test")

    emitter = ObservedEventEmitter(CollectingEventEmitter())
    with tracer.start_as_current_span("deep_pass_run"):
        emitter.emit(
            "cognition_history_record_appended",
            {"project_id": "p1", "run_id": "r1", "chr_id": "c1",
             "supersedes_chr_id": None, "payload_dict": {"k": "v"}},
        )

    (span,) = exporter.get_finished_spans()
    (event,) = span.events
    assert event.name == "cognition_history_record_appended"
    assert event.attributes["oslo.event.chr_id"] == "c1"
    assert event.attributes["oslo.event.run_id"] == "r1"
    # Non-primitive payload values are JSON-encoded; None values are dropped.
    assert json.loads(event.attributes["oslo.event.payload_dict"]) == {"k": "v"}
    assert "oslo.event.supersedes_chr_id" not in event.attributes


def test_no_active_span_is_a_clean_noop() -> None:
    """No tracer/span active: emit still delegates + logs, raises nothing."""
    inner = CollectingEventEmitter()
    ObservedEventEmitter(inner).emit("stale_detected", {"project_id": "p1"})
    assert inner.names == ["stale_detected"]
