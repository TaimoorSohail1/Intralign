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
import uuid
from typing import Any

from backend.services.observability.events import CollectingEventEmitter


class AppendOnlyFakeChrRepo:
    """Append + read only — no mutation surface (mirrors ChrRepository, A4.2)."""

    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    def append(self, record: dict[str, Any]) -> dict[str, Any]:
        persisted = {
            "chr_id": str(uuid.uuid4()),
            **copy.deepcopy(dict(record)),
        }
        self.rows.append(persisted)
        return copy.deepcopy(persisted)

    def rows_for_kind(self, output_kind: str) -> list[dict[str, Any]]:
        return [copy.deepcopy(r) for r in self.rows if r.get("output_kind") == output_kind]


class FakeStageContext:
    """StageContext stand-in carrying a collecting emitter + the fake CHR repo."""

    def __init__(self) -> None:
        self.emitter = CollectingEventEmitter()
        self.chr_repo = AppendOnlyFakeChrRepo()
