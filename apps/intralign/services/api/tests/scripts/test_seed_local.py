import importlib.util
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[2] / "scripts" / "seed_local.py"
SPEC = importlib.util.spec_from_file_location("seed_local", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
SEED_LOCAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SEED_LOCAL)
supabase_executable = SEED_LOCAL.supabase_executable
local_status = SEED_LOCAL.local_status


class RecordingCursor:
    def __init__(self) -> None:
        self.statements: list[str] = []

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> None:
        return None

    def execute(self, statement: str, _parameters) -> None:
        self.statements.append(" ".join(statement.split()))


class RecordingConnection:
    def __init__(self, cursor: RecordingCursor) -> None:
        self._cursor = cursor

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> None:
        return None

    def cursor(self) -> RecordingCursor:
        return self._cursor


def test_supabase_executable_uses_windows_shim() -> None:
    executable = supabase_executable(Path("repo"), platform_name="nt")

    assert executable == Path("repo/node_modules/.bin/supabase.cmd")


def test_supabase_executable_uses_posix_shim() -> None:
    executable = supabase_executable(Path("repo"), platform_name="posix")

    assert executable == Path("repo/node_modules/.bin/supabase")


def test_local_status_uses_the_local_api_environment_without_waiting_for_cli(
    tmp_path,
    monkeypatch,
) -> None:
    env_file = tmp_path / "services" / "api" / ".env"
    env_file.parent.mkdir(parents=True)
    env_file.write_text(
        "\n".join(
            (
                "SUPABASE_URL=http://127.0.0.1:55321",
                "SUPABASE_SECRET_KEY=local-secret",
                "DATABASE_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:55322/postgres",
            )
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        SEED_LOCAL.subprocess,
        "run",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("CLI called")),
    )

    assert local_status(tmp_path) == {
        "API_URL": "http://127.0.0.1:55321",
        "SECRET_KEY": "local-secret",
        "DB_URL": "postgresql://postgres:postgres@127.0.0.1:55322/postgres",
    }


def test_seed_registers_the_local_identity_as_platform_admin(monkeypatch) -> None:
    cursor = RecordingCursor()
    connection = RecordingConnection(cursor)
    monkeypatch.setattr(SEED_LOCAL.psycopg, "connect", lambda _url: connection)

    SEED_LOCAL.ensure_application_records(
        database_url="postgresql://local",
        user_id=SEED_LOCAL.WORKSPACE_ID,
    )

    statements = "\n".join(cursor.statements)
    assert "insert into private.platform_admins" in statements
    assert "delete from public.memberships where user_id" in statements
    assert "insert into public.memberships" not in statements
