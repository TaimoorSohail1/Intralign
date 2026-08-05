from __future__ import annotations

import httpx

from oslo_api.analysis.object_storage import SupabaseObjectStorage


def _client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_supabase_storage_puts_and_reads_a_private_object() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.method == "GET":
            return httpx.Response(200, content=b"source pdf")
        return httpx.Response(200, json={"Key": "source-documents/project/report.pdf"})

    storage = SupabaseObjectStorage(
        base_url="https://example.supabase.co",
        secret_key="secret-value",
        bucket="source-documents",
        client=_client(handler),
    )

    storage.put("project/report.pdf", b"source pdf")
    assert storage.get("project/report.pdf") == b"source pdf"

    put = requests[0]
    assert put.method == "POST"
    assert put.url.path == "/storage/v1/object/source-documents/project/report.pdf"
    assert put.headers["authorization"] == "Bearer secret-value"
    assert put.headers["x-upsert"] == "false"


def test_supabase_storage_exists_and_delete_are_idempotent() -> None:
    methods: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        methods.append(request.method)
        if request.method == "GET":
            return httpx.Response(404)
        return httpx.Response(200)

    storage = SupabaseObjectStorage(
        base_url="https://example.supabase.co/",
        secret_key="secret-value",
        bucket="source-documents",
        client=_client(handler),
    )

    assert storage.exists("missing.pdf") is False
    storage.delete("missing.pdf")
    assert methods == ["GET", "DELETE"]


def test_supabase_storage_rejects_parent_path_segments() -> None:
    storage = SupabaseObjectStorage(
        base_url="https://example.supabase.co",
        secret_key="secret-value",
        bucket="source-documents",
        client=_client(lambda request: httpx.Response(500)),
    )

    try:
        storage.get("../outside.pdf")
    except ValueError as error:
        assert str(error) == "OBJECT_KEY_INVALID"
    else:
        raise AssertionError("unsafe object key was accepted")
