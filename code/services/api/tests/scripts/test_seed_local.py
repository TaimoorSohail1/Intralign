import importlib.util
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[2] / "scripts" / "seed_local.py"
SPEC = importlib.util.spec_from_file_location("seed_local", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
SEED_LOCAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SEED_LOCAL)
supabase_executable = SEED_LOCAL.supabase_executable


def test_supabase_executable_uses_windows_shim() -> None:
    executable = supabase_executable(Path("repo"), platform_name="nt")

    assert executable == Path("repo/node_modules/.bin/supabase.cmd")


def test_supabase_executable_uses_posix_shim() -> None:
    executable = supabase_executable(Path("repo"), platform_name="posix")

    assert executable == Path("repo/node_modules/.bin/supabase")
