"""Offline fakes for the Wave S synthesis suite (DTM-0009).

A vocab-flexible, append-only fake CHR repo + a StageContext stand-in. The fake
repo is APPEND-ONLY by construction (insert + read only — no update/delete/
upsert method), mirroring the real ``ChrRepository`` surface. It accepts the
Wave-S ``output_kind`` values (``synthesized_planning_model`` /
``planning_artifact``) — now owner-approved into the canonical CHR CHECK +
``OutputKind`` Literal (migration ``20260617120000``, 2026-06-17). Rows are
deep-copied on append and read so a test can never mutate a "persisted" row in
place.
"""

from __future__ import annotations

import copy
from typing import Any

from backend.responsibilities.retain import CognitionHistoryRecord
from backend.services.observability.events import CollectingEventEmitter


class AppendOnlyFakeChrRepo:
    """Append + read only — no mutation surface (mirrors ChrRepository, A4.2).

    Matches the REAL ``ChrRepository.append`` contract (DTM-0013): it takes a
    ``CognitionHistoryRecord`` MODEL — NOT a bare dict — and, like the real repo,
    ``model_dump``s it to a stored row and returns a re-validated model carrying
    the server-shaped fields. A stage that passes a dict (the DTM-0013 defect)
    now raises here, so the offline suite catches the live failure mode.
    """

    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    def append(self, record: CognitionHistoryRecord) -> CognitionHistoryRecord:
        if not isinstance(record, CognitionHistoryRecord):
            raise TypeError(
                "ChrRepository.append takes a CognitionHistoryRecord model, not "
                f"a {type(record).__name__} — the real repo calls "
                "record.model_dump(...) (DTM-0013)"
            )
        # Mirror the real repo: persist the model_dump row; return a model.
        row = record.model_dump(mode="json", exclude_none=True)
        self.rows.append(row)
        return CognitionHistoryRecord.model_validate(row)

    def rows_for_kind(self, output_kind: str) -> list[dict[str, Any]]:
        return [copy.deepcopy(r) for r in self.rows if r.get("output_kind") == output_kind]


class FakeStageContext:
    """StageContext stand-in carrying a collecting emitter + the fake CHR repo."""

    def __init__(self) -> None:
        self.emitter = CollectingEventEmitter()
        self.chr_repo = AppendOnlyFakeChrRepo()
