"""DTM-0030 negative suite (Critical) — the materializer's epistemic boundary.

Proves IMPOSSIBILITY, not mere absence (code/CLAUDE.md hard rules #2/#3; gate-4):

- The materializer + the projection store write the DERIVED layer ONLY: no
  surface touches a canonical table (``attested_assertion`` /
  ``cognition_history_record`` / ``user_acceptance_record`` / ``history_record``);
  the CHR repo is used READ-only (``get`` / project lister) — never ``append`` /
  ``update`` / ``upsert`` from inside the materializer.
- Every materialized row carries ``epistemic_label='derived'`` — never
  ``attested-*`` (no Derived → Attested promotion).
- A failed materialize leaves the last-known-good projection intact (no partial
  corruption): a store that raises mid-batch leaves prior rows untouched and the
  CHR log unchanged (append-only preserved).
"""

from __future__ import annotations

import ast
import inspect
import uuid
from pathlib import Path

import pytest

import backend.responsibilities.disclose.projection_writer as projection_writer
import backend.services.persistence.projection_store as projection_store
from backend.responsibilities.disclose import ProjectionMaterializer, chr_to_projection_row
from backend.responsibilities.disclose.projection_writer import DERIVED_TABLE
from backend.responsibilities.retain.models import CognitionHistoryRecord
from backend.services.persistence.projection_store import SupabaseProjectionStore

PROJECT = "22222222-2222-2222-2222-222222222222"

_CANONICAL_TABLES = {
    "attested_assertion",
    "cognition_history_record",
    "user_acceptance_record",
    "history_record",
}


def _chr(output_kind: str, payload: dict) -> CognitionHistoryRecord:
    return CognitionHistoryRecord(
        chr_id=uuid.uuid4(),
        project_id=uuid.UUID(PROJECT),
        output_kind=output_kind,
        output_payload=payload,
        input_attestation_version="v1",
        model_or_rule_version={"provider": "test", "model": "rule-v1"},
        upstream_lineage={"chr_ids": []},
        recompute_trigger="reanalysis",
        provenance_ref={"emitted_by": "dtm-0030-neg"},
    )


# --- no canonical table written (static AST scan over the DTM-0030 modules) ---

def _table_targets(source: str) -> set[str]:
    """Every string literal passed to ``.table(...)`` in the module source."""
    targets: set[str] = set()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "table"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        ):
            targets.add(node.args[0].value)
    return targets


def test_no_canonical_table_named_in_dtm0030_modules() -> None:
    """The materializer + store name NO canonical table anywhere (Derived-only)."""
    for module in (projection_writer, projection_store):
        source = Path(inspect.getfile(module)).read_text(encoding="utf-8")
        offending = _table_targets(source) & _CANONICAL_TABLES
        assert offending == set(), (
            f"{module.__name__} references canonical table(s) {offending} — "
            "the materializer writes the Derived layer ONLY (hard rule #2)"
        )


def test_projection_store_writes_only_derived_tables() -> None:
    """Every table the store can target is a ``derived.*_current`` table."""
    source = Path(inspect.getfile(projection_store)).read_text(encoding="utf-8")
    derived_tables = set(DERIVED_TABLE.values())
    for target in _table_targets(source):
        assert target in derived_tables, (
            f"store targets non-derived table {target!r}"
        )


def test_projection_store_has_no_canonical_or_append_surface() -> None:
    """The store exposes upsert/select onto derived only — no insert_* canonical."""
    public = {
        n
        for n in vars(SupabaseProjectionStore)
        if not n.startswith("_") and callable(getattr(SupabaseProjectionStore, n))
    }
    assert public == {"supports", "upsert_projection", "list_for_project"}
    # No method that would write a canonical store.
    for forbidden in ("insert_assertion", "insert_acceptance", "insert_history",
                      "append", "insert_chr"):
        assert not hasattr(SupabaseProjectionStore, forbidden)


# --- the materializer never appends/mutates a CHR (append-only intact) --------

class _ExplodingCanonicalRepo:
    """A CHR repo whose only mutation path explodes — proving it is never called."""

    def __init__(self, records: dict[str, CognitionHistoryRecord]) -> None:
        self._records = records
        self.append_calls = 0

    def get(self, chr_id: uuid.UUID) -> CognitionHistoryRecord | None:
        return self._records.get(str(chr_id))

    def append(self, record):  # pragma: no cover - the assertion is it's never hit
        self.append_calls += 1
        raise AssertionError("materializer attempted a CHR append")

    def chrs_for_project(self, project_id: str):
        return list(self._records.values())


class _RecordingDerivedStore:
    """Records upserts; raises on the Nth to simulate a mid-batch failure."""

    def __init__(self, fail_on: int | None = None) -> None:
        self.rows: dict[str, dict] = {}
        self.calls = 0
        self._fail_on = fail_on

    def upsert_projection(self, output_kind: str, row: dict) -> dict:
        self.calls += 1
        if self._fail_on is not None and self.calls == self._fail_on:
            raise RuntimeError("simulated derived-write failure")
        self.rows[row["projection_id"]] = dict(row)
        return self.rows[row["projection_id"]]

    def list_for_project(self, output_kind: str, project_id: str):
        return list(self.rows.values())


def test_materialize_never_appends_a_chr() -> None:
    record = _chr("finding", {"finding_id": "f-1", "summary": "x"})
    repo = _ExplodingCanonicalRepo({str(record.chr_id): record})
    store = _RecordingDerivedStore()
    ProjectionMaterializer(store, repo).materialize_chr_ids([str(record.chr_id)])
    assert repo.append_calls == 0  # append() was never invoked
    assert store.calls == 1


# --- never sets attested / never promotes Derived → Attested ------------------

def test_every_materialized_row_is_derived_never_attested() -> None:
    for output_kind in DERIVED_TABLE:
        payload = {"index": 60.0} if output_kind in (
            "confidence", "caf", "outcome_confidence"
        ) else {f"{output_kind}_id": "x-1", "summary": "y"}
        # CHR payloads can even carry a stray epistemic_state — it must NOT leak
        # into the projection's epistemic_label.
        payload = {**payload, "epistemic_state": "attested-oslo"}
        row = chr_to_projection_row(_chr(output_kind, payload))
        assert row is not None
        assert row["epistemic_label"] == "derived"
        assert "attested" not in str(row["epistemic_label"])


# --- failed materialize leaves last-known-good (no partial corruption) ---------

def test_failed_materialize_leaves_prior_rows_and_chr_log_intact() -> None:
    good = _chr("finding", {"finding_id": "f-1", "summary": "good"})
    bad_a = _chr("finding", {"finding_id": "f-2", "summary": "a"})
    bad_b = _chr("finding", {"finding_id": "f-3", "summary": "b"})
    records = {str(r.chr_id): r for r in (good, bad_a, bad_b)}
    repo = _ExplodingCanonicalRepo(records)

    # First run materializes the last-known-good row.
    store = _RecordingDerivedStore()
    ProjectionMaterializer(store, repo).materialize_chr_ids([str(good.chr_id)])
    good_id = next(iter(store.rows))
    snapshot = dict(store.rows[good_id])

    # A second batch fails on its FIRST upsert (the very next store call).
    store._fail_on = store.calls + 1
    with pytest.raises(RuntimeError):
        ProjectionMaterializer(store, repo).materialize_chr_ids(
            [str(bad_a.chr_id), str(bad_b.chr_id)]
        )

    # Last-known-good is untouched and STILL the only row (the failing batch
    # corrupted nothing); the append-only CHR log was never mutated.
    assert store.rows[good_id] == snapshot
    assert list(store.rows) == [good_id]
    assert repo.append_calls == 0
