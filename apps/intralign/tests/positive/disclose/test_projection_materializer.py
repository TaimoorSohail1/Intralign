"""DTM-0030 positive suite — projection materializer upserts ``derived.*_current``.

Proves the live read model: after a run appends CHRs, the materializer upserts
each ``derived.<kind>_current`` row with the CHR's snapshot + the epistemic-safety
envelope, in the EXACT shape the read seam (``SupabaseProjectionReader``) SELECTs
and the DTM-0018 render mappers consume; a re-run SUPERSEDES the projection (new
``current_chr_ref``, same deterministic ``projection_id``); ``rebuild_for_project``
repopulates from the latest CHRs.

A pure in-memory fake store + fake CHR repo stand in for Supabase (the house
style — see ``tests/positive/render``); the materializer logic is exercised
without a live stack. The shape is asserted against the render mappers so the
materialized row is provably consumable end-to-end.
"""

from __future__ import annotations

import uuid
from typing import Any

from backend.responsibilities.disclose import (
    ProjectionMaterializer,
    chr_to_projection_row,
    projection_id_for,
)
from backend.responsibilities.disclose.projection_writer import DERIVED_TABLE
from backend.responsibilities.retain.models import CognitionHistoryRecord
from backend.services.render import (
    caf_to_dto,
    confidence_to_dto,
    finding_to_dto,
    recommendation_to_dto,
)

PROJECT = "11111111-1111-1111-1111-111111111111"


class FakeChrRepo:
    """In-memory append-only CHR log — ``append`` + read methods only (no mutate)."""

    def __init__(self) -> None:
        self._by_id: dict[str, CognitionHistoryRecord] = {}
        self._order: list[str] = []

    def append(self, record: CognitionHistoryRecord) -> CognitionHistoryRecord:
        self._by_id[str(record.chr_id)] = record
        self._order.append(str(record.chr_id))
        return record

    def get(self, chr_id: uuid.UUID) -> CognitionHistoryRecord | None:
        return self._by_id.get(str(chr_id))

    def latest_for_output(self, project_id: uuid.UUID, output_kind: str):
        matches = [
            self._by_id[i]
            for i in self._order
            if self._by_id[i].project_id == project_id
            and self._by_id[i].output_kind == output_kind
        ]
        return matches[-1] if matches else None

    def chrs_for_project(self, project_id: str) -> list[CognitionHistoryRecord]:
        return [
            self._by_id[i]
            for i in self._order
            if str(self._by_id[i].project_id) == str(project_id)
        ]


class FakeProjectionStore:
    """In-memory ``derived.*_current`` — keyed UPSERT on projection_id (replace)."""

    def __init__(self) -> None:
        self.tables: dict[str, dict[str, dict[str, Any]]] = {
            kind: {} for kind in DERIVED_TABLE
        }

    @staticmethod
    def supports(output_kind: str) -> bool:
        return output_kind in DERIVED_TABLE

    def upsert_projection(self, output_kind: str, row: dict[str, Any]) -> dict[str, Any]:
        stored = dict(row)
        stored.setdefault("recomputed_at", "2026-06-26T00:00:00Z")
        self.tables[output_kind][row["projection_id"]] = stored
        return stored

    def list_for_project(self, output_kind: str, project_id: str) -> list[dict[str, Any]]:
        return [
            r
            for r in self.tables[output_kind].values()
            if str(r["project_id"]) == str(project_id)
        ]


def _chr(output_kind: str, payload: dict, *, chr_id: uuid.UUID | None = None,
         emitted_seq: int = 1) -> CognitionHistoryRecord:
    return CognitionHistoryRecord(
        chr_id=chr_id or uuid.uuid4(),
        project_id=uuid.UUID(PROJECT),
        output_kind=output_kind,
        output_payload=payload,
        input_attestation_version="v1",
        model_or_rule_version={"provider": "test", "model": "rule-v1"},
        upstream_lineage={"chr_ids": []},
        recompute_trigger="reanalysis",
        provenance_ref={"emitted_by": "dtm-0030-tests"},
        version=emitted_seq,
    )


def _run(store: FakeProjectionStore, repo: FakeChrRepo,
         records: list[CognitionHistoryRecord]) -> list[dict[str, Any]]:
    """Append the CHRs (canonical), then materialize their ids (Derived)."""
    ids = [str(repo.append(r).chr_id) for r in records]
    materializer = ProjectionMaterializer(store, repo)
    return materializer.materialize_chr_ids(ids)


# --- per-kind materialize (the eight projection tables) -----------------------

def test_finding_materializes_to_read_seam_shape() -> None:
    store, repo = FakeProjectionStore(), FakeChrRepo()
    record = _chr("finding", {
        "finding_id": "f-1", "finding_type": "conflict",
        "summary": "Two assertions contradict.", "evidence_anchors": ["a-0", "a-1"],
        "status": "detected",
    })
    (row,) = _run(store, repo, [record])

    # EXACT read-seam shape (every column the SELECT returns).
    assert set(row) >= {
        "projection_id", "project_id", "output_kind", "current_payload",
        "current_chr_ref", "epistemic_label", "confidence_value",
        "confidence_band", "conflict_state",
    }
    assert row["output_kind"] == "finding"
    assert row["epistemic_label"] == "derived"
    assert row["current_chr_ref"] == str(record.chr_id)
    assert row["conflict_state"] == "contested"  # finding_type=conflict
    assert row["current_payload"]["finding_id"] == "f-1"

    # The render mapper consumes it verbatim (DTM-0018 end-to-end).
    dto = finding_to_dto(row)
    assert dto.finding_id == "f-1"
    assert dto.finding_type.value == "conflict"
    assert dto.label.epistemic_label == "derived"
    assert dto.label.current_chr_ref == str(record.chr_id)


def test_confidence_materializes_band_from_index() -> None:
    store, repo = FakeProjectionStore(), FakeChrRepo()
    record = _chr("confidence", {
        "index": 62.0, "band": "medium", "reliability_qualifier": "moderate",
        "basis": ["clarity", "alignment"],
    })
    (row,) = _run(store, repo, [record])
    assert row["confidence_value"] == 62.0
    assert row["confidence_band"] == "medium"
    dto = confidence_to_dto(row)
    assert dto.outcome_confidence_value == 62.0
    assert dto.confidence_band.value == "medium"


def test_caf_materializes_three_dimensions() -> None:
    store, repo = FakeProjectionStore(), FakeChrRepo()
    record = _chr("caf", {"dimensions": {
        "clarity": {"index": 70.0, "band": "medium", "reliability": "moderate"},
        "alignment": {"index": 55.0, "band": "medium", "reliability": "low"},
        "feasibility": {"index": 80.0, "band": "high", "reliability": "high"},
    }})
    (row,) = _run(store, repo, [record])
    dto = caf_to_dto(row)
    assert dto.feasibility.band.value == "high"
    assert dto.label.epistemic_label == "derived"


def test_recommendation_materializes() -> None:
    store, repo = FakeProjectionStore(), FakeChrRepo()
    record = _chr("recommendation", {
        "recommendation_id": "r-1", "recommendation_type": "candidate_improvement",
        "anchor": "f-1", "summary": "Clarify the scope statement.", "state": "generated",
    })
    (row,) = _run(store, repo, [record])
    dto = recommendation_to_dto(row)
    assert dto.recommendation_id == "r-1"
    assert dto.label.epistemic_label == "derived"


def test_list_kinds_get_one_row_per_subject() -> None:
    """Two findings → two distinct projection rows (per-item subject id)."""
    store, repo = FakeProjectionStore(), FakeChrRepo()
    _run(store, repo, [
        _chr("finding", {"finding_id": "f-1", "summary": "a"}),
        _chr("finding", {"finding_id": "f-2", "summary": "b"}),
    ])
    rows = store.list_for_project("finding", PROJECT)
    assert len(rows) == 2
    assert {r["current_payload"]["finding_id"] for r in rows} == {"f-1", "f-2"}


def test_unmaterializable_kind_is_skipped() -> None:
    """A kind with no derived table (reliability) materializes nothing."""
    store, repo = FakeProjectionStore(), FakeChrRepo()
    written = _run(store, repo, [_chr("reliability", {"level": "moderate"})])
    assert written == []


# --- supersession: a re-run replaces the row (new current_chr_ref) ------------

def test_rerun_supersedes_projection_same_row_new_chr() -> None:
    store, repo = FakeProjectionStore(), FakeChrRepo()
    first = _chr("finding", {"finding_id": "f-1", "summary": "old", "status": "detected"})
    _run(store, repo, [first])
    rows = store.list_for_project("finding", PROJECT)
    assert len(rows) == 1
    assert rows[0]["current_chr_ref"] == str(first.chr_id)

    # Recompute appends a NEW CHR for the SAME subject; projection is replaced.
    second = _chr("finding", {"finding_id": "f-1", "summary": "new", "status": "detected"},
                  emitted_seq=2)
    _run(store, repo, [second])
    rows = store.list_for_project("finding", PROJECT)
    assert len(rows) == 1  # SUPERSEDED, not duplicated
    assert rows[0]["current_chr_ref"] == str(second.chr_id)
    assert rows[0]["current_payload"]["summary"] == "new"
    # Same deterministic projection_id (the upsert key) across the two runs.
    assert rows[0]["projection_id"] == projection_id_for(PROJECT, "finding", "f-1")
    # Both CHRs survive in the append-only log (history grows).
    assert repo.get(first.chr_id) is not None
    assert repo.get(second.chr_id) is not None


# --- rebuild_for_project repopulates derived.*_current from the CHR log --------

def test_rebuild_for_project_repopulates_from_latest_chrs() -> None:
    store, repo = FakeProjectionStore(), FakeChrRepo()
    f_old = _chr("finding", {"finding_id": "f-1", "summary": "v1"}, emitted_seq=1)
    f_new = _chr("finding", {"finding_id": "f-1", "summary": "v2"}, emitted_seq=2)
    conf = _chr("confidence", {"index": 80.0, "band": "high"}, emitted_seq=1)
    for r in (f_old, f_new, conf):
        repo.append(r)

    # Projection store starts EMPTY (lost/never-materialized) → rebuild restores.
    materializer = ProjectionMaterializer(store, repo)
    written = materializer.rebuild_for_project(PROJECT)

    findings = store.list_for_project("finding", PROJECT)
    assert len(findings) == 1  # one subject, latest wins
    assert findings[0]["current_chr_ref"] == str(f_new.chr_id)
    assert findings[0]["current_payload"]["summary"] == "v2"
    confidences = store.list_for_project("confidence", PROJECT)
    assert len(confidences) == 1
    assert confidences[0]["confidence_band"] == "high"
    assert len(written) == 2


def test_chr_to_projection_row_is_pure_and_deterministic() -> None:
    record = _chr("finding", {"finding_id": "f-9", "summary": "x"})
    row_a = chr_to_projection_row(record)
    row_b = chr_to_projection_row(record)
    assert row_a == row_b
    assert row_a["projection_id"] == projection_id_for(PROJECT, "finding", "f-9")
