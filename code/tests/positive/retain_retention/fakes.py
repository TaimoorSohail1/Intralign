"""In-memory retention store fake for the pure QA-WA-002 suites.

Structurally APPEND-ONLY exactly where the real
``SupabaseRetentionStore`` is: insert + select surfaces ONLY — no update, no
delete, no upsert method exists (the negative suite introspects both classes
against the same allowed-surface set). Rows are deep-copied on insert and on
read so a test (or the code under test) can never mutate a "persisted" row in
place — mirroring that the real table refuses UPDATE at the database.

``tables_written`` records WHICH tables each call touched, so tests can prove
e.g. "acceptance recording writes user_acceptance_record + history_record and
nothing else".
"""

from __future__ import annotations

import copy
import uuid
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any


class InMemoryRetentionStore:
    """Append-only assertion/UAR/history rows + read-only candidates, dict-backed."""

    def __init__(self) -> None:
        self.assertions: list[dict[str, Any]] = []
        self.acceptances: list[dict[str, Any]] = []
        self.history: list[dict[str, Any]] = []
        self.candidates: list[dict[str, Any]] = []
        self.tables_written: list[str] = []

    # -- seeding helper (test setup only; NOT part of the store surface) ------

    def seed_candidate(self, row: Mapping[str, Any]) -> dict[str, Any]:
        """Test setup: place a promotion_candidate row for admission to read."""
        seeded = {
            "candidate_id": str(uuid.uuid4()),
            "created_at": datetime.now(UTC).isoformat(),
            **copy.deepcopy(dict(row)),
        }
        self.candidates.append(seeded)
        return copy.deepcopy(seeded)

    # -- promotion candidate (READ only) --------------------------------------

    def get_candidate(self, candidate_id: str) -> dict[str, Any] | None:
        for row in self.candidates:
            if row["candidate_id"] == candidate_id:
                return copy.deepcopy(row)
        return None

    # -- attested_assertion ----------------------------------------------------

    def insert_assertion(self, row: Mapping[str, Any]) -> dict[str, Any]:
        persisted = {
            "assertion_id": str(uuid.uuid4()),
            "created_at": datetime.now(UTC).isoformat(),
            "supersedes_id": None,
            **copy.deepcopy(dict(row)),
        }
        self.assertions.append(persisted)
        self.tables_written.append("attested_assertion")
        return copy.deepcopy(persisted)

    def get_assertion(self, assertion_id: str) -> dict[str, Any] | None:
        for row in self.assertions:
            if row["assertion_id"] == assertion_id:
                return copy.deepcopy(row)
        return None

    # -- user_acceptance_record -------------------------------------------------

    def insert_acceptance(self, row: Mapping[str, Any]) -> dict[str, Any]:
        persisted = {
            "uar_id": str(uuid.uuid4()),
            "created_at": datetime.now(UTC).isoformat(),
            **copy.deepcopy(dict(row)),
        }
        self.acceptances.append(persisted)
        self.tables_written.append("user_acceptance_record")
        return copy.deepcopy(persisted)

    def get_acceptance(self, uar_id: str) -> dict[str, Any] | None:
        for row in self.acceptances:
            if row["uar_id"] == uar_id:
                return copy.deepcopy(row)
        return None

    # -- history_record -----------------------------------------------------------

    def insert_history(self, row: Mapping[str, Any]) -> dict[str, Any]:
        persisted = {
            "history_id": str(uuid.uuid4()),
            "at": datetime.now(UTC).isoformat(),
            "created_at": datetime.now(UTC).isoformat(),
            **copy.deepcopy(dict(row)),
        }
        self.history.append(persisted)
        self.tables_written.append("history_record")
        return copy.deepcopy(persisted)

    def history_for_assertion(self, assertion_id: str) -> list[dict[str, Any]]:
        return [
            copy.deepcopy(row)
            for row in self.history
            if row["subject_ref"].get("assertion_id") == assertion_id
        ]


class InMemoryChrReader:
    """Read-only CHR-by-id seam for the DTM-0016 plan-fact-on-accept tests.

    Satisfies the ``ChrReader`` protocol (``get(chr_id) -> mapping | None``); the
    plan-fact content for an accepted recommendation is a DATA read of the pinned
    CHR's ``output_payload`` (no LLM). Seed records by version-pin id.
    """

    def __init__(self) -> None:
        self._records: dict[str, dict[str, Any]] = {}

    def seed(self, chr_id: str, output_payload: Mapping[str, Any]) -> None:
        self._records[str(chr_id)] = {
            "chr_id": str(chr_id),
            "output_payload": copy.deepcopy(dict(output_payload)),
        }

    def get(self, chr_id: Any) -> dict[str, Any] | None:
        record = self._records.get(str(chr_id))
        return copy.deepcopy(record) if record is not None else None
