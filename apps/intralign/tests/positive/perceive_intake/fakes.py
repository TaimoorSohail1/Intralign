"""In-memory intake store/body-store fakes for the pure QA-WA-001 suites.

Structurally APPEND-ONLY where the real thing is: the artifact fake exposes no
mutator at all and enforces the ``dedup_key`` UNIQUE constraint (a second
admission with the same key raises, exactly like Postgres would). The body
fake is content-addressed like the real ``ArtifactBodyStore`` and counts
uploads so idempotency tests can prove "no second Storage object".
"""

from __future__ import annotations

import hashlib
import uuid
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any


class DuplicateDedupKeyError(RuntimeError):
    """The fake's stand-in for the Postgres UNIQUE violation on dedup_key."""


class InMemoryIntakeStore:
    """Append-only artifact rows + candidate rows, dict-backed."""

    def __init__(self) -> None:
        self.artifacts: list[dict[str, Any]] = []
        self.candidates: list[dict[str, Any]] = []
        self.tables_written: list[str] = []  # audit of WHICH tables intake touches

    def find_artifact_by_dedup_key(self, dedup_key: str) -> dict[str, Any] | None:
        for row in self.artifacts:
            if row["dedup_key"] == dedup_key:
                return row
        return None

    def latest_artifact_for_source(
        self, project_id: str, source: str
    ) -> dict[str, Any] | None:
        matches = [
            row
            for row in self.artifacts
            if row["project_id"] == project_id
            and row["provenance"].get("source") == source
        ]
        if not matches:
            return None
        return max(matches, key=lambda row: row["version"])

    def save_artifact(self, row: Mapping[str, Any]) -> dict[str, Any]:
        if self.find_artifact_by_dedup_key(row["dedup_key"]) is not None:
            raise DuplicateDedupKeyError(
                f"dedup_key {row['dedup_key']!r} already admitted — UNIQUE"
            )
        persisted = {
            **dict(row),
            "artifact_id": str(uuid.uuid4()),
            "created_at": datetime.now(UTC).isoformat(),
        }
        self.artifacts.append(persisted)
        self.tables_written.append("artifact")
        return persisted

    def get_artifact(self, artifact_id: str) -> dict[str, Any] | None:
        for row in self.artifacts:
            if row["artifact_id"] == artifact_id:
                return row
        return None

    def save_candidate(self, row: Mapping[str, Any]) -> dict[str, Any]:
        persisted = {
            **dict(row),
            "candidate_id": str(uuid.uuid4()),
            "created_at": datetime.now(UTC).isoformat(),
        }
        self.candidates.append(persisted)
        self.tables_written.append("promotion_candidate")
        return persisted

    def candidate_for_artifact(self, artifact_id: str) -> dict[str, Any] | None:
        for row in reversed(self.candidates):
            if row["artifact_ref"] == artifact_id:
                return row
        return None


class InMemoryBodyStore:
    """Content-addressed body objects, mirroring ArtifactBodyStore semantics."""

    def __init__(self) -> None:
        self.objects: dict[str, bytes] = {}
        self.upload_calls = 0

    def upload_body(self, project_id: str, content: str | bytes) -> str:
        self.upload_calls += 1
        data = content.encode("utf-8") if isinstance(content, str) else content
        digest = hashlib.sha256(data).hexdigest()
        body_ref = f"artifacts/{project_id}/{digest}.txt"
        self.objects[body_ref] = data
        return body_ref

    def download_body(self, body_ref: str) -> bytes:
        return self.objects[body_ref]
