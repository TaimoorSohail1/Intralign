"""DTM-0006 positive — C2 event coverage end-to-end (OBS-WA-00R §3 C2). Live.

The OBS contract's C2 list IS the IC-WA-00R A6 seven-name vocabulary. DTM-0005
proved per-event presence with subsequence assertions; this suite EXTENDS that
(does not duplicate it) by pinning the EXACT full event sequence of one
successful recompute and one failed recompute — every backbone action emits
exactly its C2 event, nothing more, nothing missing, in order.
"""

from __future__ import annotations

import os
import uuid

import pytest

try:
    from supabase import create_client
except ImportError:  # pragma: no cover - CI venv without supabase-py
    create_client = None  # type: ignore[assignment]

from backend.orchestration import runner
from backend.responsibilities.retain import ChrRepository
from backend.services.observability.events import EVENT_NAMES, CollectingEventEmitter

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_DB_URL = os.environ.get("SUPABASE_DB_URL")

pytestmark = pytest.mark.skipif(
    create_client is None
    or not SUPABASE_URL
    or not SUPABASE_SERVICE_ROLE_KEY
    or not SUPABASE_DB_URL,
    reason=(
        "local Supabase stack not configured — set SUPABASE_URL, "
        "SUPABASE_SERVICE_ROLE_KEY and SUPABASE_DB_URL (DB URL from "
        "`supabase status`); this live suite runs locally only"
    ),
)


@pytest.fixture(scope="module")
def repo() -> ChrRepository:
    return ChrRepository(client=create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY))


@pytest.fixture(scope="module")
def checkpointer():
    from backend.orchestration.checkpointer import build_checkpointer

    return build_checkpointer()


@pytest.fixture(autouse=True)
def _fresh_guard():
    runner.reset_coalescing_guard()
    yield
    runner.reset_coalescing_guard()


def _emission(**overrides) -> dict:
    fields: dict = {
        "output_kind": "finding",
        "output_payload": {"summary": "c2 coverage emission"},
        "input_attestation_version": "v1",
        "model_or_rule_version": {"provider": "test", "model": "rule-v1"},
        "upstream_lineage": {"chr_ids": []},
        "provenance_ref": {"emitted_by": "dtm-0006-tests"},
    }
    fields.update(overrides)
    return fields


def _trigger(project_id: str, trigger_type: str, emissions: list[dict]) -> dict:
    return {
        "trigger_type": trigger_type,
        "project_id": project_id,
        "information_changed": True,
        "source": "dtm-0006-c2-test",
        "emissions": emissions,
    }


def test_successful_run_emits_exactly_the_expected_c2_sequence(
    repo, checkpointer
) -> None:
    """One emission, one success: the EXACT event list, in order (C2 == A6)."""
    project_id = str(uuid.uuid4())
    emitter = CollectingEventEmitter()

    outcome = runner.submit_trigger(
        "deep_pass",
        _trigger(project_id, "promotion", [_emission()]),
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
    )
    assert outcome.status == "completed"

    assert emitter.names == [
        "stale_detected",
        "state_transition_occurred",  # current -> stale
        "reanalysis_triggered",
        "recompute_started",
        "state_transition_occurred",  # stale -> reanalyzing
        "cognition_history_record_appended",
        "state_transition_occurred",  # reanalyzing -> current'
        "recompute_completed",
    ]
    # Every emitted name is C2/A6 vocabulary; no event type outside the model.
    assert set(emitter.names) <= set(EVENT_NAMES)


def test_failed_run_emits_exactly_the_expected_c2_sequence(
    repo, checkpointer
) -> None:
    """Retain-stage failure: failure sequence exact; no append, no completion."""
    project_id = str(uuid.uuid4())
    emitter = CollectingEventEmitter()

    outcome = runner.submit_trigger(
        "deep_pass",
        _trigger(project_id, "reanalysis", [_emission(output_kind="not-a-kind")]),
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
    )
    assert outcome.status == "failed"

    assert emitter.names == [
        "stale_detected",
        "state_transition_occurred",  # current -> stale
        "reanalysis_triggered",
        "recompute_started",
        "state_transition_occurred",  # stale -> reanalyzing
        "state_transition_occurred",  # reanalyzing -> failed
        "recompute_failed",
    ]
    failed = [p for n, p in emitter.events if n == "recompute_failed"]
    assert failed[0]["last_known_good_retained"] is True
    assert set(emitter.names) <= set(EVENT_NAMES)


def test_c2_list_is_exactly_the_seven_a6_names() -> None:
    """Contract pin (pure): the C2 observable-event list == A6, verbatim."""
    assert EVENT_NAMES == (
        "stale_detected",
        "reanalysis_triggered",
        "recompute_started",
        "cognition_history_record_appended",
        "recompute_completed",
        "recompute_failed",
        "state_transition_occurred",
    )
