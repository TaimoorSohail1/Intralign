from uuid import UUID

import httpx

from oslo_api.slice_one import AuthenticatedUser, AuthSession


class InvalidSession(Exception):
    """Raised when the identity provider rejects a bearer session."""


class InvalidCredentials(Exception):
    """Raised when email/password authentication fails."""


class SupabaseIdentityProvider:
    def __init__(
        self,
        *,
        client: httpx.Client,
        supabase_url: str,
        api_key: str,
    ) -> None:
        self._client = client
        self._supabase_url = supabase_url.rstrip("/")
        self._api_key = api_key

    def authenticate(self, access_token: str) -> AuthenticatedUser:
        response = self._client.get(
            f"{self._supabase_url}/auth/v1/user",
            headers={
                "apikey": self._api_key,
                "authorization": f"Bearer {access_token}",
            },
        )
        if response.status_code != 200:
            raise InvalidSession
        payload = response.json()
        return AuthenticatedUser(id=UUID(payload["id"]), email=payload["email"])

    def find_user_by_email(self, email: str) -> AuthenticatedUser | None:
        response = self._client.get(
            f"{self._supabase_url}/auth/v1/admin/users",
            headers=self._admin_headers(),
            params={"page": 1, "per_page": 1000},
        )
        response.raise_for_status()
        expected_email = email.strip().casefold()
        user = next(
            (
                item
                for item in response.json()["users"]
                if item.get("email", "").casefold() == expected_email
            ),
            None,
        )
        if user is None:
            return None
        return AuthenticatedUser(id=UUID(user["id"]), email=user["email"])

    def create_user(self, *, email: str, password: str, display_name: str) -> AuthenticatedUser:
        response = self._client.post(
            f"{self._supabase_url}/auth/v1/admin/users",
            headers=self._admin_headers(),
            json={
                "email": email,
                "password": password,
                "email_confirm": True,
                "user_metadata": {"display_name": display_name},
            },
        )
        response.raise_for_status()
        user = response.json()
        return AuthenticatedUser(id=UUID(user["id"]), email=user["email"])

    def delete_user(self, user_id: UUID) -> None:
        response = self._client.delete(
            f"{self._supabase_url}/auth/v1/admin/users/{user_id}",
            headers=self._admin_headers(),
        )
        response.raise_for_status()

    def sign_in_with_password(self, *, email: str, password: str) -> AuthSession:
        response = self._client.post(
            f"{self._supabase_url}/auth/v1/token",
            params={"grant_type": "password"},
            headers={"apikey": self._api_key},
            json={"email": email, "password": password},
        )
        if response.status_code != 200:
            raise InvalidCredentials
        payload = response.json()
        return AuthSession(
            user_id=UUID(payload["user"]["id"]),
            email=payload["user"]["email"],
            access_token=payload["access_token"],
            refresh_token=payload["refresh_token"],
            expires_in=payload["expires_in"],
        )

    def _admin_headers(self) -> dict[str, str]:
        return {
            "apikey": self._api_key,
            "authorization": f"Bearer {self._api_key}",
        }
