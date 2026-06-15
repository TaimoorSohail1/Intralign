"""Supabase Storage client for artifact bodies (DTM-0007; DL-054 binding).

IC-WA-001 A3.1: artifact bodies are preserved in the Supabase Storage bucket
``artifacts``; Postgres keeps only the reference (``body_ref``) plus the
normalized form. Storage here is CONTENT-ADDRESSED: the object path is
``<project_id>/<sha256-of-body>.txt``, so re-uploading identical content is a
no-op overwrite of identical bytes and idempotent re-intake (A3.3/A3.8) never
multiplies Storage objects.

``body_ref`` format: ``artifacts/<project_id>/<sha256>.txt`` — the bucket name
is embedded so the reference is self-locating.

Bucket creation is idempotent (exists-ok): ``ensure_bucket`` checks for the
bucket first and only creates it when absent.
"""

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # import-time dependency only for type checkers
    from supabase import Client

ARTIFACTS_BUCKET = "artifacts"


class ArtifactBodyStore:
    """Upload/download artifact bodies in the ``artifacts`` Storage bucket."""

    def __init__(self, client: Client, *, bucket: str = ARTIFACTS_BUCKET) -> None:
        self._client = client
        self._bucket = bucket

    @property
    def bucket(self) -> str:
        return self._bucket

    def ensure_bucket(self) -> None:
        """Create the bucket when absent; an existing bucket is fine (exists-ok)."""
        try:
            self._client.storage.get_bucket(self._bucket)
        except Exception:  # bucket missing (StorageApiError) -> create it
            self._client.storage.create_bucket(self._bucket)

    def upload_body(self, project_id: str, content: str | bytes) -> str:
        """Preserve one raw body; return its ``body_ref`` (content-addressed).

        Identical content for the same project maps to the same object path,
        so a re-upload writes identical bytes — never a second object.
        """
        data = content.encode("utf-8") if isinstance(content, str) else content
        digest = hashlib.sha256(data).hexdigest()
        path = f"{project_id}/{digest}.txt"
        self.ensure_bucket()
        self._client.storage.from_(self._bucket).upload(
            path,
            data,
            file_options={
                "content-type": "text/plain; charset=utf-8",
                "upsert": "true",  # identical bytes at the same path — idempotent
            },
        )
        return f"{self._bucket}/{path}"

    def download_body(self, body_ref: str) -> bytes:
        """Fetch the raw body bytes for a ``body_ref`` produced by upload_body."""
        bucket, _, path = body_ref.partition("/")
        if not path:
            raise ValueError(
                f"malformed body_ref {body_ref!r} — expected '<bucket>/<path>'"
            )
        return self._client.storage.from_(bucket).download(path)

    def list_bodies(self, project_id: str) -> list[str]:
        """Object names stored under this project's prefix (verification aid)."""
        entries = self._client.storage.from_(self._bucket).list(project_id)
        return [entry["name"] for entry in entries]
