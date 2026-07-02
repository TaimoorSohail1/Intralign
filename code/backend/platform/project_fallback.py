"""Fallback storage for the mutable platform ``project`` table.

The release-completion branch includes the project table migration, but the
current hosted Supabase project has not had that migration applied. This fallback
keeps the demo deployment usable without weakening the governed/canonical stores:
it is only for the commodity platform ``project`` table.
"""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from typing import Any, Mapping

_PROJECT_KEY_PREFIX = "oslo:platform:project:"
_WORKSPACE_INDEX_PREFIX = "oslo:platform:workspace-projects:"
_memory_projects: dict[str, dict[str, Any]] = {}
_memory_workspace_index: dict[str, list[str]] = {}


def is_missing_project_table(exc: Exception) -> bool:
    return "PGRST205" in str(exc) and "public.project" in str(exc)


def _now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _redis_client() -> Any | None:
    redis_url = os.environ.get("REDIS_URL")
    if not redis_url:
        return None
    try:
        from redis import Redis

        return Redis.from_url(redis_url, decode_responses=True)
    except Exception:
        return None


def _project_key(project_id: str) -> str:
    return f"{_PROJECT_KEY_PREFIX}{project_id}"


def _workspace_key(workspace_id: str) -> str:
    return f"{_WORKSPACE_INDEX_PREFIX}{workspace_id}"


def create_project(row: Mapping[str, Any]) -> dict[str, Any]:
    project = dict(row)
    now = _now()
    project.setdefault("created_at", now)
    project.setdefault("updated_at", now)
    project_id = str(project["project_id"])
    workspace_id = str(project["workspace_id"])

    client = _redis_client()
    if client is not None:
        client.set(_project_key(project_id), json.dumps(project))
        client.lrem(_workspace_key(workspace_id), 0, project_id)
        client.lpush(_workspace_key(workspace_id), project_id)
        return project

    _memory_projects[project_id] = project
    index = _memory_workspace_index.setdefault(workspace_id, [])
    if project_id in index:
        index.remove(project_id)
    index.insert(0, project_id)
    return project


def get_project(project_id: str) -> dict[str, Any] | None:
    client = _redis_client()
    if client is not None:
        raw = client.get(_project_key(project_id))
        return json.loads(raw) if raw else None
    project = _memory_projects.get(project_id)
    return dict(project) if project else None


def list_projects(workspace_id: str) -> list[dict[str, Any]]:
    client = _redis_client()
    if client is not None:
        ids = client.lrange(_workspace_key(workspace_id), 0, -1)
        projects = []
        for project_id in ids:
            raw = client.get(_project_key(project_id))
            if raw:
                projects.append(json.loads(raw))
        return projects

    return [
        dict(_memory_projects[project_id])
        for project_id in _memory_workspace_index.get(workspace_id, [])
        if project_id in _memory_projects
    ]


def update_project(project_id: str, patch: Mapping[str, Any]) -> dict[str, Any]:
    project = get_project(project_id)
    if project is None:
        return {}
    project.update(dict(patch))
    project["updated_at"] = _now()

    client = _redis_client()
    if client is not None:
        client.set(_project_key(project_id), json.dumps(project))
    else:
        _memory_projects[project_id] = project
    return project
