"""OBS-WU-ACCEPT U3 — record-exact replay for the UAR + plan-fact records.

The User Acceptance Record and the user-attested plan fact are Attested writes
(tier: exact, tolerance 0): their canonical content must reproduce byte-for-byte
on replay, and the emitted ``user_acceptance_record_appended`` /
``plan_fact_recorded`` payloads must replay byte-identically. Server-assigned
ids (uar_id / assertion_id / history_id) and timestamps are excluded from the
record-exact content (they are storage identity, not the recorded fact). Pure —
never skips.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime

from backend.responsibilities.perceive.acceptance_capture import capture_acceptance
from backend.responsibilities.retain.acceptance import record_acceptance
from backend.services.observability.events import CollectingEventEmitter
from tests.positive.retain_retention.fakes import (
    InMemoryChrReader,
    InMemoryRetentionStore,
)

USER = "user-42"
PIN = "33333333-3333-3333-3333-333333333333"
PROJECT = "11111111-1111-1111-1111-111111111111"
CAPTURED_AT = datetime(2026, 6, 12, 10, 30, tzinfo=UTC)
CONTENT = "Adopt the proposed milestone plan."

# Storage-identity / server-assigned fields — not part of the recorded fact.
_NON_RECORD_KEYS = frozenset({"assertion_id", "uar_id", "created_at"})


def _record() -> tuple[dict, dict, list[tuple[str, dict]]]:
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    reader = InMemoryChrReader()
    reader.seed(PIN, {"summary": CONTENT})
    capture = capture_acceptance(
        {
            "user_id": USER,
            "target_kind": "recommendation",
            "version_pin": PIN,
            "action": "accept",
            "project_id": PROJECT,
            "captured_at": CAPTURED_AT,
        },
        emitter=CollectingEventEmitter(),
    )
    result = record_acceptance(
        capture, project_id=PROJECT, store=store, emitter=emitter, chr_reader=reader
    )
    uar = store.get_acceptance(result.uar_id)
    plan_fact = store.get_assertion(result.plan_fact_id)
    return uar, plan_fact, emitter.events


def _canonical(row: dict) -> bytes:
    content = {k: v for k, v in row.items() if k not in _NON_RECORD_KEYS}
    return json.dumps(
        content, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def test_plan_fact_record_replays_record_exact() -> None:
    """Same accept recorded twice -> byte-identical canonical plan-fact content."""
    _, first, _ = _record()
    _, second, _ = _record()
    assert _canonical(second) == _canonical(first)  # tolerance 0


def test_uar_record_replays_record_exact() -> None:
    first, _, _ = _record()
    second, _, _ = _record()
    assert _canonical(second) == _canonical(first)


def test_plan_fact_recorded_event_payload_replays_record_exact() -> None:
    _, _, events_a = _record()
    _, _, events_b = _record()
    [(_, _), (name_a, plan_a)] = events_a
    [(_, _), (name_b, plan_b)] = events_b
    assert name_a == name_b == "plan_fact_recorded"
    # The event payload (minus the server-assigned assertion_id/uar_id) replays.
    drop = {"assertion_id", "uar_id"}
    a = {k: v for k, v in plan_a.items() if k not in drop}
    b = {k: v for k, v in plan_b.items() if k not in drop}
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def test_tampered_plan_fact_proposition_is_detected() -> None:
    """Any drift in the confirmed content is visible (Critical, C6)."""
    _, plan_fact, _ = _record()
    snapshot = json.loads(_canonical(plan_fact))
    tampered = {**snapshot, "proposition": "something the user did NOT confirm"}
    assert tampered != snapshot
    differing = [k for k in sorted(snapshot) if snapshot[k] != tampered[k]]
    assert differing == ["proposition"]  # the drifted field is NAMED
