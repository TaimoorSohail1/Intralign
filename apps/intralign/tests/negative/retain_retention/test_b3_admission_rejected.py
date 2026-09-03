"""QA-WA-002 B3.3 + §B+ negatives 6/7 — non-cleared admission is impossible (pure).

Admission is INTEGRITY-GATED and integrity-gated only (DL-043): a candidate
that is not ready, or carries no integrity clearance, is rejected BEFORE any
row is written or any event emitted — and no governance-gate surface of any
kind exists on the retain modules for an admission to lean on instead
(§B+ negative 7: no such decision exists in R1).
"""

from __future__ import annotations

import inspect
import re
from pathlib import Path

import pytest

import backend.responsibilities.retain.acceptance as acceptance_module
import backend.responsibilities.retain.admission as admission_module
import backend.responsibilities.retain.archival as archival_module
import backend.responsibilities.retain.versioning as versioning_module
from backend.responsibilities.retain.admission import (
    AdmissionRejectedError,
    admit_candidate,
)
from backend.services.observability.events import CollectingEventEmitter
from tests.positive.retain_retention.fakes import InMemoryRetentionStore
from tests.positive.retain_retention.helpers import draft, ready_candidate

NEW_RETAIN_MODULES = (
    admission_module,
    versioning_module,
    archival_module,
    acceptance_module,
)
RETAIN_DIR = Path(inspect.getfile(admission_module)).parent
NEW_MODULE_FILES = ("admission.py", "versioning.py", "archival.py", "acceptance.py")


def _assert_nothing_happened(store, emitter) -> None:
    """The rejection happened BEFORE anything moved."""
    assert store.assertions == []
    assert store.history == []
    assert store.acceptances == []
    assert store.tables_written == []
    assert emitter.events == []


@pytest.mark.parametrize("readiness_state", ["pending", "failed"])
def test_b3_3_admission_without_readiness_rejected(readiness_state: str) -> None:
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    candidate = store.seed_candidate(ready_candidate(readiness_state=readiness_state))
    with pytest.raises(AdmissionRejectedError, match="readiness_state"):
        admit_candidate(candidate, [draft()], store=store, emitter=emitter)
    _assert_nothing_happened(store, emitter)


@pytest.mark.parametrize("clearance", [None, {}])
def test_b_plus_6_admission_without_integrity_clearance_rejected(clearance) -> None:
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    candidate = store.seed_candidate(ready_candidate(integrity_clearance=clearance))
    with pytest.raises(AdmissionRejectedError, match="integrity_clearance"):
        admit_candidate(candidate, [draft()], store=store, emitter=emitter)
    _assert_nothing_happened(store, emitter)


def test_b3_3_admission_of_a_missing_candidate_rejected() -> None:
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    with pytest.raises(AdmissionRejectedError, match="does not exist"):
        admit_candidate(
            "00000000-0000-0000-0000-000000000000",
            [draft()],
            store=store,
            emitter=emitter,
        )
    _assert_nothing_happened(store, emitter)


def test_admission_with_no_drafts_rejected() -> None:
    """An empty admission would be a contentless canonical write — rejected."""
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    candidate = store.seed_candidate(ready_candidate())
    with pytest.raises(AdmissionRejectedError, match="no assertion drafts"):
        admit_candidate(candidate, [], store=store, emitter=emitter)
    _assert_nothing_happened(store, emitter)


# --- §B+ negative 7: no governance-gate surface exists at all ----------------

_GOVERNANCE_GATE = re.compile(r"authori|governance_decision", re.IGNORECASE)


def test_b_plus_7_no_governance_gate_surface_in_the_new_retain_modules() -> None:
    """Introspection: no module mentions or exposes a governance-gate token —
    the only admission gate is integrity (gate-4 backstops the token scan)."""
    for name in NEW_MODULE_FILES:
        source = (RETAIN_DIR / name).read_text(encoding="utf-8")
        assert not _GOVERNANCE_GATE.search(source), (
            f"{name} mentions a governance-gate token — admission is "
            "integrity-gated; no governance decision exists in R1 (DL-043)"
        )
    for module in NEW_RETAIN_MODULES:
        offenders = [n for n in dir(module) if _GOVERNANCE_GATE.search(n)]
        assert offenders == [], f"{module.__name__} exposes {offenders}"


def test_b_plus_7_admission_signature_admits_no_governance_input() -> None:
    """The function CANNOT receive a governance decision: its parameters are
    exactly candidate + drafts + the store/emitter seams."""
    params = set(inspect.signature(admit_candidate).parameters)
    assert params == {"candidate", "drafts", "store", "emitter"}
