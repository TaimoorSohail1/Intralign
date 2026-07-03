"""OpenTelemetry bring-up (DTM-0003) — TracerProvider + OTLP exporter + FastAPI auto-instrumentation.

Env-driven: tracing is enabled only when ``OTEL_EXPORTER_OTLP_ENDPOINT`` is set
(service name from ``OTEL_SERVICE_NAME``). Degrades gracefully — an unset/unreachable
endpoint or missing instrumentation packages must NEVER stop boot; the app logs a
warning and runs without traces. Operational traces only — governed-output events
are DTM-0006 and do not live here.
"""

from __future__ import annotations

import logging
import os
import socket
from urllib.parse import urlparse

from fastapi import FastAPI

logger = logging.getLogger(__name__)

DEFAULT_SERVICE_NAME = "oslo-backend"
DEFAULT_OTLP_GRPC_PORT = 4317


def configure_observability(app: FastAPI) -> bool:
    """Wire OTel tracing onto ``app``; return True when tracing is active.

    Never raises: every failure path degrades to a logged warning (DTM-0003 test plan).
    """
    endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "").strip()
    if not endpoint:
        logger.warning(
            "OTEL_EXPORTER_OTLP_ENDPOINT not set — observability disabled; "
            "traces will not be exported."
        )
        return False

    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
            OTLPSpanExporter,
        )
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except ImportError as exc:
        logger.warning(
            "OpenTelemetry packages unavailable (%s) — observability disabled.", exc
        )
        return False

    _warn_if_unreachable(endpoint)

    try:
        resource = Resource.create(
            {"service.name": os.environ.get("OTEL_SERVICE_NAME", DEFAULT_SERVICE_NAME)}
        )
        provider = TracerProvider(resource=resource)
        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
        trace.set_tracer_provider(provider)  # ignored (with a log) if already set
        FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
    except Exception:  # observability must never block boot
        logger.warning(
            "OpenTelemetry setup failed — observability disabled.", exc_info=True
        )
        return False

    logger.info("OpenTelemetry tracing enabled — exporting to %s.", endpoint)
    return True


def _warn_if_unreachable(endpoint: str) -> None:
    """Best-effort reachability probe — warn-only; the exporter retries in background."""
    parsed = urlparse(endpoint if "://" in endpoint else f"http://{endpoint}")
    host = parsed.hostname or "localhost"
    port = parsed.port or DEFAULT_OTLP_GRPC_PORT
    try:
        with socket.create_connection((host, port), timeout=0.5):
            pass
    except OSError:
        logger.warning(
            "OTLP endpoint %s is unreachable — app continues without exported traces "
            "(spans are retried/dropped in the background).",
            endpoint,
        )
