"""QA-WU-ACCEPT U2 negatives — the seven (G) forbidden invariants + never-self-accept.

DTM-0016; IC-WU-ACCEPT U1.2 "Forbidden". A plan fact / UAR records a USER
confirmation, never a truth claim, an approval, a governance decision, or an
OSLO acceptance. Proven negatively:

- Critical — acceptance/plan-fact is NOT world-true and NOT OSLO-approved: no
  field on the ``PlanFact`` shape or the persisted row marks it true/approved/
  governed/applied; ``extra='forbid'`` makes such a field unrepresentable.
- Critical — a UAR is NOT a Governance Decision: the canonical vocabulary bans
  ``GovernanceDecision`` and the acceptance path never emits/writes one.
- Critical — record overwrite is impossible: a second confirm APPENDS a new row
  (proven DB-shaped — no supersedes_id, distinct ids), never an update.
- Critical — OSLO never self-promotes / self-accepts (hard rule #5): the plan
  fact's epistemic_state is PINNED ``attested-user`` (never ``attested-oslo`` /
  ``derived``) and the attesting_source is ALWAYS the user; no code path authors
  a plan fact without a user action.
- Major — version-pin is mandatory: a confirm without a pin is rejected before
  any write.
"""

from __future__ import annotations

import ast
import inspect
import uuid
from pathlib import Path

import pydantic
import pytest

import backend.responsibilities.retain.acceptance as acceptance_module
from backend.responsibilities.retain.acceptance import (
    AcceptanceRecordingError,
    record_acceptance,
)
from shared.epistemic import CANONICAL_OUTPUTS, EpistemicState, PlanFact
from tests.positive.retain_retention.fakes import (
    InMemoryChrReader,
    InMemoryRetentionStore,
)

USER = str(uuid.uuid4())
PIN = str(uuid.uuid4())
PROJECT = str(uuid.uuid4())

# Tokens that would constitute a world-truth / approval / governance / applied
# marker on a plan fact (the seven (G) forbidden invariants; §0.1).
_FORBIDDEN_MARKERS = (
    "true",
    "world_truth",
    "approved",
    "approval",
    "certified",
    "valid",
    "governance",
    "governance_decision",
    "authority",
    "decision",
    "sign_off",
    "applied",
    "executed",
)


def _capture_fields(**overrides) -> dict:
    fields = {
        "user_id": USER,
        "target_kind": "recommendation",
        "version_pin": PIN,
        "action": "accept",
        "captured_at": None,
    }
    fields.update(overrides)
    return fields


def _reader() -> InMemoryChrReader:
    reader = InMemoryChrReader()
    reader.seed(PIN, {"summary": "Confirmed content."})
    return reader


# --- Critical: plan fact is not world-true / not OSLO-approved ------------------


def test_u2_plan_fact_row_carries_no_truth_or_approval_marker() -> None:
    store = InMemoryRetentionStore()
    result = record_acceptance(
        _capture_fields(), project_id=PROJECT, store=store, chr_reader=_reader()
    )
    plan_fact = store.get_assertion(result.plan_fact_id)
    keys = " ".join(plan_fact).lower()
    for marker in _FORBIDDEN_MARKERS:
        assert marker not in keys, (
            f"plan-fact row carries a forbidden marker {marker!r} — a plan fact "
            "is factual-in-the-plan, never world-true/approved/governed (§0.1)"
        )


def test_u2_plan_fact_shape_forbids_a_truth_or_approval_field() -> None:
    """extra='forbid' — a truth/approval/governance/applied field is structurally
    unrepresentable on the PlanFact shape."""
    base = {
        "project_id": PROJECT,
        "proposition": "x.",
        "attested_by_user": USER,
        "version_pin": PIN,
        "provenance_ref": {},
    }
    for marker in ("approved", "world_truth", "governance_decision", "applied", "executed"):
        with pytest.raises(pydantic.ValidationError):
            PlanFact(**base, **{marker: True})


def test_u2_plan_fact_epistemic_state_cannot_be_oslo_or_derived() -> None:
    """Hard rule #5 — OSLO never authors a plan fact: the state is PINNED
    attested-user; attested-oslo / derived are rejected at construction."""
    base = {
        "project_id": PROJECT,
        "proposition": "x.",
        "attested_by_user": USER,
        "version_pin": PIN,
        "provenance_ref": {},
    }
    for forbidden in (EpistemicState.ATTESTED_OSLO, EpistemicState.DERIVED):
        with pytest.raises(pydantic.ValidationError):
            PlanFact(**base, epistemic_state=forbidden)
    # The default (and only valid) state is attested-user.
    assert PlanFact(**base).epistemic_state == EpistemicState.ATTESTED_USER


# --- Critical: UAR is not a Governance Decision --------------------------------


def test_u2_governance_decision_is_banned_vocabulary() -> None:
    assert "GovernanceDecision" not in CANONICAL_OUTPUTS
    assert "PlanFact" in CANONICAL_OUTPUTS


def test_u2_acceptance_path_never_mentions_governance_or_authority() -> None:
    source = Path(inspect.getfile(acceptance_module)).read_text(encoding="utf-8")
    lowered = source.lower()
    for banned in ("governancedecision", "governance_decision", "authority"):
        assert banned not in lowered, (
            f"acceptance path mentions {banned!r} — a UAR/plan fact is NOT a "
            "Governance Decision and there is no Authority in R1 (DL-043 G)"
        )


# --- Critical: never overwrite — append-only (DB-shaped) -----------------------


def test_u2_plan_fact_write_never_carries_a_supersedes_id() -> None:
    """A plan fact is a NEW append-only row — the write never sets supersedes_id
    (overwrite is impossible; supersession is versioning's single evented path)."""
    tree = ast.parse(Path(inspect.getfile(acceptance_module)).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "insert_assertion"
        ):
            assert "supersedes_id" not in ast.unparse(node)


def test_u2_repeated_confirm_appends_a_new_row_never_overwrites() -> None:
    store = InMemoryRetentionStore()
    r1 = record_acceptance(
        _capture_fields(), project_id=PROJECT, store=store, chr_reader=_reader()
    )
    first = store.get_assertion(r1.plan_fact_id)
    r2 = record_acceptance(
        _capture_fields(), project_id=PROJECT, store=store, chr_reader=_reader()
    )
    # The first row is untouched; the second is a distinct, additional row.
    assert store.get_assertion(r1.plan_fact_id) == first
    assert r2.plan_fact_id != r1.plan_fact_id
    assert len(store.assertions) == 2


def test_u2_store_has_no_update_or_delete_surface() -> None:
    """DB-proven append-only: the store seam exposes insert/select only — no
    update/delete/upsert method exists to overwrite a plan fact."""
    surface = {name for name in dir(InMemoryRetentionStore) if not name.startswith("_")}
    forbidden = {"update", "delete", "upsert", "update_assertion", "delete_assertion"}
    assert surface & forbidden == set()


# --- Critical: OSLO never self-accepts / self-promotes -------------------------


def test_u2_plan_fact_attesting_source_is_always_the_user_never_oslo() -> None:
    """The plan fact is ALWAYS attributed to the user — OSLO is never the
    attesting source (hard rule #5; the user authors it)."""
    store = InMemoryRetentionStore()
    result = record_acceptance(
        _capture_fields(), project_id=PROJECT, store=store, chr_reader=_reader()
    )
    plan_fact = store.get_assertion(result.plan_fact_id)
    assert plan_fact["attesting_source"] == USER
    assert plan_fact["attesting_source"] != "oslo"
    assert plan_fact["created_by"] == USER


def test_u2_no_plan_fact_is_authored_without_a_user_action() -> None:
    """There is no code path that writes a plan fact on reject/defer (no user
    confirmation) — OSLO never promotes its own recommendation to Attested."""
    store = InMemoryRetentionStore()
    for action in ("reject", "defer"):
        result = record_acceptance(
            _capture_fields(action=action), project_id=PROJECT, store=store
        )
        assert result.plan_fact_id is None
    assert store.assertions == []  # nothing promoted to attested


def test_u2_plan_fact_marks_the_accepted_recommendation_nothing() -> None:
    """The accepted Derived recommendation is NEVER promoted: accepting it does
    not write back to / mutate the pinned CHR — the reader is READ-only and the
    plan fact is a separate, fresh attested-user row."""
    store = InMemoryRetentionStore()
    reader = _reader()
    before = reader.get(PIN)
    record_acceptance(
        _capture_fields(), project_id=PROJECT, store=store, chr_reader=reader
    )
    # The pinned CHR is unchanged (read-only); the plan fact is a NEW row.
    assert reader.get(PIN) == before


# --- Major: version-pin mandatory ----------------------------------------------


@pytest.mark.parametrize("pin", [None, "", "   "])
def test_u2_confirm_without_version_pin_is_rejected_before_any_write(pin) -> None:
    store = InMemoryRetentionStore()
    with pytest.raises(AcceptanceRecordingError, match="version_pin"):
        record_acceptance(
            _capture_fields(version_pin=pin),
            project_id=PROJECT,
            store=store,
            chr_reader=_reader(),
        )
    assert store.acceptances == []
    assert store.assertions == []
    assert store.tables_written == []


def test_u2_direct_edit_without_edit_content_is_rejected() -> None:
    """A direct edit must carry its user-authored content — there is no source
    for a plan fact otherwise; rejected before any write."""
    store = InMemoryRetentionStore()
    with pytest.raises(AcceptanceRecordingError, match="edit_content"):
        record_acceptance(
            _capture_fields(action="direct_edit", edit_content=None),
            project_id=PROJECT,
            store=store,
        )
    assert store.assertions == []
