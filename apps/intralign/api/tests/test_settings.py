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


def test_settings_accepts_inline_serverless_analysis_execution() -> None:
    settings = Settings(
        analysis_execution_mode="inline",
        supabase_secret_key="local-test-secret-key-value",
    )

    assert settings.analysis_execution_mode == "inline"


def test_settings_parallelize_the_seven_independent_artifacts_by_default() -> None:
    settings = Settings(
        _env_file=None,
        supabase_secret_key="local-test-secret-key-value",
    )

    assert settings.analysis_artifact_worker_threads == 7
