"""Observable event transport (DTM-0006; OBS-WA-00R C2) — decorator over the seam.

``ObservedEventEmitter`` wraps any :class:`~backend.services.observability.events.EventEmitter`
(decorator pattern — ADDITIVE; the DTM-0005 dispatcher protocol and
``CollectingEventEmitter`` are untouched) and, for every A6 event the inner
emitter accepts:

1. logs the event as ONE structured-JSON line through the stdlib ``logging``
   module (logger ``oslo.observability.events``) — the C2 transport that always
   exists; and
2. attaches the event as an OpenTelemetry **span event** on the current span
   when a tracer is active (``span.is_recording()``) — a no-op otherwise, the
   same graceful-degradation philosophy as ``setup.configure_observability``.

Ordering is validate-then-observe: the INNER emitter runs first, so an unknown
event name (``UnknownEventError``) is rejected before anything is logged or
attached — the observable stream never contains a non-A6 name. Transport
problems (logging/OTel hiccups) never break the run: observability must not
block the backbone (same rule as setup.py).

External delivery (queue/webhook/stream) is deliberately NOT built — open NFR.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Mapping
from typing import Any

from backend.services.observability.events import EventEmitter

logger = logging.getLogger("oslo.observability.events")

# OTel span-event attribute namespace for event payload fields.
_ATTR_PREFIX = "oslo.event."


def _attribute_value(value: Any) -> str | bool | int | float:
    """Coerce a payload value into an OTel-legal attribute value (JSON otherwise)."""
    if isinstance(value, (str, bool, int, float)):
        return value
    return json.dumps(value, default=str, sort_keys=True)


class ObservedEventEmitter:
    """Structured-log + OTel-span-event decorator around an inner A6 emitter."""

    def __init__(self, inner: EventEmitter) -> None:
        self._inner = inner

    @classmethod
    def wrap(cls, emitter: EventEmitter) -> ObservedEventEmitter:
        """Wrap ``emitter``; idempotent (an already-observed emitter passes through)."""
        if isinstance(emitter, cls):
            return emitter
        return cls(emitter)

    @property
    def inner(self) -> EventEmitter:
        """The wrapped emitter (e.g. a CollectingEventEmitter in tests)."""
        return self._inner

    def emit(self, event_name: str, payload: Mapping[str, Any]) -> None:
        """Dispatch through the inner emitter, then observe (log + span event).

        The inner emitter validates the A6 vocabulary FIRST — a rejected name
        raises before any observation happens. Observation itself never raises.
        """
        self._inner.emit(event_name, payload)
        self._log_structured(event_name, payload)
        self._attach_span_event(event_name, payload)

    def __getattr__(self, name: str) -> Any:
        """Delegate non-emit attributes (e.g. ``events``/``names``) to the inner emitter."""
        return getattr(self._inner, name)

    def _log_structured(self, event_name: str, payload: Mapping[str, Any]) -> None:
        try:
            line = json.dumps(
                {"event": event_name, "payload": dict(payload)},
                default=str,
                sort_keys=True,
            )
            logger.info(line)
        except Exception:  # observability must never block the backbone
            logger.warning(
                "structured logging of event %r failed — event was still "
                "dispatched through the inner emitter.",
                event_name,
                exc_info=True,
            )

    def _attach_span_event(self, event_name: str, payload: Mapping[str, Any]) -> None:
        try:
            from opentelemetry import trace

            span = trace.get_current_span()
            if span is None or not span.is_recording():
                return  # no active tracer/span — graceful no-op (setup.py philosophy)
            attributes = {
                f"{_ATTR_PREFIX}{key}": _attribute_value(value)
                for key, value in payload.items()
                if value is not None
            }
            span.add_event(event_name, attributes=attributes)
        except Exception:  # observability must never block the backbone
            logger.warning(
                "attaching event %r as an OTel span event failed — event was "
                "still dispatched and structured-logged.",
                event_name,
                exc_info=True,
            )
