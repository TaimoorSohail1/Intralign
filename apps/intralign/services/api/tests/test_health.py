import pytest
from fastapi.testclient import TestClient

from oslo_api.main import build_identity, create_app


def test_health_reports_ready() -> None:
    response = TestClient(create_app()).get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ready"
    assert payload["service"] == "oslo-api"


def test_health_names_the_running_build(monkeypatch: pytest.MonkeyPatch) -> None:
    """N-5: the running build resolves to its source commit."""

    monkeypatch.setenv("BUILD_SHA", "0123456789abcdef")

    response = TestClient(create_app()).get("/health")

    assert response.json()["build"] == "0123456789abcdef"


@pytest.mark.parametrize(
    "variable",
    ["BUILD_SHA", "HEROKU_SLUG_COMMIT", "SOURCE_VERSION", "VERCEL_GIT_COMMIT_SHA"],
)
def test_build_identity_reads_every_supported_platform_variable(
    variable: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    for name in ("BUILD_SHA", "HEROKU_SLUG_COMMIT", "SOURCE_VERSION", "VERCEL_GIT_COMMIT_SHA"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv(variable, "deadbeefcafe")

    assert build_identity() == "deadbeefcafe"


def test_unstamped_build_reads_unknown_rather_than_guessing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unstamped deploy must be visible, never silently plausible."""

    for name in ("BUILD_SHA", "HEROKU_SLUG_COMMIT", "SOURCE_VERSION", "VERCEL_GIT_COMMIT_SHA"):
        monkeypatch.delenv(name, raising=False)

    assert build_identity() == "unknown"
    assert TestClient(create_app()).get("/health").json()["build"] == "unknown"


def test_blank_platform_variable_does_not_count_as_a_build(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for name in ("BUILD_SHA", "HEROKU_SLUG_COMMIT", "SOURCE_VERSION", "VERCEL_GIT_COMMIT_SHA"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("HEROKU_SLUG_COMMIT", "   ")

    assert build_identity() == "unknown"
