import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Protocol
from urllib.parse import quote

import httpx

_CONTENT_TYPES_BY_SUFFIX = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".txt": "text/plain",
    ".md": "text/markdown",
}


class ObjectStorage(Protocol):
    """Storage boundary used by document ingestion.

    Object keys are opaque to callers. A cloud adapter can implement this
    contract later without changing parsing or the analysis workflow.
    """

    def put(self, object_key: str, content: bytes) -> None: ...

    def get(self, object_key: str) -> bytes: ...

    def exists(self, object_key: str) -> bool: ...

    def delete(self, object_key: str) -> None: ...


class LocalObjectStorage:
    def __init__(self, root: Path) -> None:
        self._root = root.resolve()

    def put(self, object_key: str, content: bytes) -> None:
        target = self._target(object_key)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            return
        temporary_path: Path | None = None
        try:
            with NamedTemporaryFile(dir=target.parent, delete=False) as temporary:
                temporary.write(content)
                temporary.flush()
                os.fsync(temporary.fileno())
                temporary_path = Path(temporary.name)
            temporary_path.replace(target)
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()

    def get(self, object_key: str) -> bytes:
        return self._target(object_key).read_bytes()

    def exists(self, object_key: str) -> bool:
        return self._target(object_key).exists()

    def delete(self, object_key: str) -> None:
        target = self._target(object_key)
        if target.exists():
            target.unlink()

    def _target(self, object_key: str) -> Path:
        target = (self._root / object_key).resolve()
        if not target.is_relative_to(self._root):
            raise ValueError("OBJECT_KEY_INVALID")
        return target


class SupabaseObjectStorage:
    """Private, durable object storage backed by Supabase Storage."""

    def __init__(
        self,
        *,
        base_url: str,
        secret_key: str,
        bucket: str,
        client: httpx.Client | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._bucket = bucket
        self._client = client or httpx.Client(timeout=60)
        self._headers = {"apikey": secret_key}
        if not secret_key.startswith("sb_secret_"):
            self._headers["authorization"] = f"Bearer {secret_key}"

    def put(self, object_key: str, content: bytes) -> None:
        content_type = _CONTENT_TYPES_BY_SUFFIX.get(
            Path(object_key).suffix.lower(),
            "application/octet-stream",
        )
        response = self._client.post(
            self._object_url(object_key),
            content=content,
            headers={
                **self._headers,
                "content-type": content_type,
                "x-upsert": "false",
            },
        )
        if response.status_code == 409:
            return
        response.raise_for_status()

    def get(self, object_key: str) -> bytes:
        response = self._client.get(
            self._object_url(object_key),
            headers=self._headers,
        )
        if self._is_not_found(response):
            raise FileNotFoundError(object_key)
        response.raise_for_status()
        return response.content

    def exists(self, object_key: str) -> bool:
        response = self._client.get(
            self._object_url(object_key),
            headers={**self._headers, "range": "bytes=0-0"},
        )
        if self._is_not_found(response):
            return False
        response.raise_for_status()
        return True

    def delete(self, object_key: str) -> None:
        response = self._client.delete(
            self._object_url(object_key),
            headers=self._headers,
        )
        if self._is_not_found(response):
            return
        response.raise_for_status()

    def _object_url(self, object_key: str) -> str:
        if (
            not object_key
            or "\\" in object_key
            or any(part in {"", ".", ".."} for part in object_key.split("/"))
        ):
            raise ValueError("OBJECT_KEY_INVALID")
        bucket = quote(self._bucket, safe="")
        key = quote(object_key, safe="/")
        return f"{self._base_url}/storage/v1/object/{bucket}/{key}"

    @staticmethod
    def _is_not_found(response: httpx.Response) -> bool:
        if response.status_code == 404:
            return True
        if response.status_code != 400:
            return False
        try:
            payload = response.json()
        except ValueError:
            return False
        return payload.get("code") == "NoSuchKey" or str(
            payload.get("statusCode")
        ) == "404"
