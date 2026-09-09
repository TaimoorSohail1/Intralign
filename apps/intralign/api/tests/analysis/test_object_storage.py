from __future__ import annotations

import os

import httpx
import pytest

from oslo_api.analysis.object_storage import LocalObjectStorage, SupabaseObjectStorage


def _client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


@pytest.mark.skipif(os.name != "nt", reason="Windows long-path regression")
def test_local_storage_supports_content_addressed_keys_beyond_max_path(tmp_path) -> None:
    root = tmp_path / ("nested-storage-root-" * 4)
    storage = LocalObjectStorage(root)
    object_key = f"{'w' * 36}/{'p' * 36}/{'a' * 64}.pdf"
    target = root.resolve() / object_key
    assert len(str(target)) > 260

    storage.put(object_key, b"source pdf")

    assert storage.exists(object_key) is True
    assert storage.get(object_key) == b"source pdf"
    storage.delete(object_key)
    assert storage.exists(object_key) is False


def test_supabase_storage_puts_and_reads_a_private_object() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.method == "GET":
            return httpx.Response(200, content=b"source pdf")
        return httpx.Response(200, json={"Key": "source-documents/project/report.pdf"})

    storage = SupabaseObjectStorage(
        base_url="https://example.supabase.co",
        secret_key="sb_secret_example",
        bucket="source-documents",
        client=_client(handler),
    )

    storage.put("project/report.pdf", b"source pdf")
    assert storage.get("project/report.pdf") == b"source pdf"

    put = requests[0]
    assert put.method == "POST"
    assert put.url.path == "/storage/v1/object/source-documents/project/report.pdf"
    assert put.headers["apikey"] == "sb_secret_example"
    assert "authorization" not in put.headers
    assert put.headers["content-type"] == "application/pdf"
    assert put.headers["x-upsert"] == "false"


def test_supabase_storage_keeps_bearer_header_for_legacy_service_role_jwt() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200)

    storage = SupabaseObjectStorage(
        base_url="https://example.supabase.co",
        secret_key="eyJhbGciOiJIUzI1NiJ9.payload.signature",
        bucket="source-documents",
        client=_client(handler),
    )

    storage.put("project/report.pdf", b"source pdf")

    assert requests[0].headers["apikey"] == "eyJhbGciOiJIUzI1NiJ9.payload.signature"
    assert requests[0].headers["authorization"] == (
        "Bearer eyJhbGciOiJIUzI1NiJ9.payload.signature"
    )


def test_supabase_storage_exists_and_delete_are_idempotent() -> None:
    methods: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        methods.append(request.method)
        return httpx.Response(
            400,
            json={
                "statusCode": "404",
                "error": "not_found",
                "message": "Object not found",
                "code": "NoSuchKey",
            },
        )

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
