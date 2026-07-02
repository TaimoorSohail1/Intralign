from __future__ import annotations

import ssl
import sys

from backend.platform import project_fallback


def test_project_fallback_round_trips_without_redis(monkeypatch) -> None:
    monkeypatch.delenv("REDIS_URL", raising=False)
    project_fallback._memory_projects.clear()
    project_fallback._memory_workspace_index.clear()

    row = project_fallback.create_project(
        {
            "project_id": "11111111-1111-1111-1111-111111111111",
            "workspace_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "created_by_user_id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            "title": "Demo",
            "description": None,
            "lifecycle_state": "created",
        }
    )

    assert row["title"] == "Demo"
    assert project_fallback.get_project(row["project_id"])["workspace_id"] == row["workspace_id"]
    assert project_fallback.list_projects(row["workspace_id"]) == [row]

    updated = project_fallback.update_project(row["project_id"], {"title": "Updated"})
    assert updated["title"] == "Updated"
    assert project_fallback.list_projects(row["workspace_id"])[0]["title"] == "Updated"


def test_project_fallback_accepts_heroku_rediss_self_signed_chain(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class FakeRedis:
        @staticmethod
        def from_url(url: str, **kwargs: object) -> object:
            captured["url"] = url
            captured.update(kwargs)
            return object()

    monkeypatch.setenv("REDIS_URL", "rediss://example.test:6380")
    monkeypatch.setitem(sys.modules, "redis", type("RedisModule", (), {"Redis": FakeRedis}))

    assert project_fallback._redis_client() is not None
    assert captured["url"] == "rediss://example.test:6380"
    assert captured["decode_responses"] is True
    assert captured["ssl_cert_reqs"] == ssl.CERT_NONE
