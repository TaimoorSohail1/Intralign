from uuid import UUID

import httpx

from oslo_api.identity import SupabaseIdentityProvider


def test_valid_supabase_session_resolves_the_authenticated_user() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == "http://supabase.local/auth/v1/user"
        assert request.headers["authorization"] == "Bearer access-token"
        assert request.headers["apikey"] == "server-secret"
        return httpx.Response(
            200,
            json={
                "id": "018f9f7e-8de2-7000-8000-000000000011",
                "email": "owner@example.com",
            },
        )

    provider = SupabaseIdentityProvider(
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        supabase_url="http://supabase.local",
        api_key="server-secret",
    )

    user = provider.authenticate("access-token")

    assert user.id == UUID("018f9f7e-8de2-7000-8000-000000000011")
    assert user.email == "owner@example.com"
