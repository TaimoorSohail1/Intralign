import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Protocol


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
