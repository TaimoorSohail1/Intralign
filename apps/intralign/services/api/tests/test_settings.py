from oslo_api.settings import Settings


def test_settings_selects_the_installed_psycopg_driver_for_plain_postgres_urls() -> None:
    settings = Settings(
        database_url="postgresql://postgres:postgres@127.0.0.1:55322/postgres",
        supabase_secret_key="local-test-secret-key-value",
    )

    assert settings.database_url == (
        "postgresql+psycopg://postgres:postgres@127.0.0.1:55322/postgres"
    )


def test_settings_preserves_an_explicit_sqlalchemy_driver() -> None:
    settings = Settings(
        database_url="postgresql+psycopg://postgres:postgres@127.0.0.1:55322/postgres",
        supabase_secret_key="local-test-secret-key-value",
    )

    assert settings.database_url == (
        "postgresql+psycopg://postgres:postgres@127.0.0.1:55322/postgres"
    )
