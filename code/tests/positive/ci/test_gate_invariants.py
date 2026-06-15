"""Gate 4 (epistemic-invariant) — positive: clean trees, allowlisted prose, and lawful SQL pass."""

from pathlib import Path

from ci.gate_invariants import (
    ALLOWLIST_RELPATH,
    MIGRATIONS_RELPATH,
    check_authority_dir,
    lint_migration_sql,
    lint_migrations,
    load_allowlist,
    main,
    run_all_checks,
    scan_forbidden_tokens,
)

# Decision #4 belt-and-braces append-only DDL — the exact shapes the canonical
# migrations will use; the linter must NOT flag these.
_LAWFUL_CANONICAL_SQL = """
CREATE TABLE attested_assertion (id uuid PRIMARY KEY, attesting_source text);
CREATE TABLE cognition_history_record (id uuid PRIMARY KEY);

-- belt: revoke mutation privileges (mentions UPDATE/DELETE but is a REVOKE)
REVOKE UPDATE, DELETE ON attested_assertion FROM PUBLIC;
GRANT INSERT, SELECT ON attested_assertion TO oslo_app;

-- braces: trigger raising on mutation (BEFORE UPDATE OR DELETE is not a mutation)
CREATE FUNCTION reject_mutation() RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'canonical stores are append-only (DL-043)';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER attested_assertion_append_only
    BEFORE UPDATE OR DELETE ON attested_assertion
    FOR EACH ROW EXECUTE FUNCTION reject_mutation();
"""

# DTM-0007 (IC-WA-001) intake DDL shapes — artifact is canonical (append-only,
# belt-and-braces) and promotion_candidate is transient/mutable; the linter
# must not flag either (CREATE/REVOKE/TRIGGER are lawful; candidate mutations
# are on a NON-canonical table).
_LAWFUL_INTAKE_SQL = """
CREATE TABLE public.artifact (artifact_id uuid PRIMARY KEY, dedup_key text UNIQUE);
CREATE TABLE public.promotion_candidate (candidate_id uuid PRIMARY KEY, readiness_state text);

REVOKE UPDATE, DELETE, TRUNCATE ON public.artifact FROM anon, authenticated, service_role;

CREATE TRIGGER artifact_append_only
    BEFORE UPDATE OR DELETE ON public.artifact
    FOR EACH STATEMENT EXECUTE FUNCTION public.enforce_append_only();

-- promotion_candidate is mutable (readiness_state pending -> ready|failed)
UPDATE promotion_candidate SET readiness_state = 'ready';
"""


def _make_code_root(tmp_path: Path) -> Path:
    """Minimal clean app tree: scan roots present, no migrations, no allowlist."""
    (tmp_path / "backend" / "responsibilities").mkdir(parents=True)
    (tmp_path / "shared").mkdir()
    (tmp_path / "backend" / "responsibilities" / "retain.py").write_text(
        '"""Retain — appends CognitionHistoryRecord rows."""\n', encoding="utf-8"
    )
    (tmp_path / "shared" / "epistemic.py").write_text(
        "EPISTEMIC_STATES = ('attested-user', 'derived')\n", encoding="utf-8"
    )
    return tmp_path


def test_clean_tree_passes(tmp_path: Path) -> None:
    code_root = _make_code_root(tmp_path)
    assert run_all_checks(code_root) == []


def test_cli_main_exits_zero_on_clean_tree(tmp_path: Path) -> None:
    code_root = _make_code_root(tmp_path)
    assert main(["--code-root", str(code_root)]) == 0


def test_real_repo_tree_passes() -> None:
    # The actual code/ tree must satisfy gate 4 (allowlist covers prose mentions).
    code_root = Path(__file__).resolve().parents[3]
    assert run_all_checks(code_root) == []


def test_allowlisted_prose_mention_passes(tmp_path: Path) -> None:
    code_root = _make_code_root(tmp_path)
    (code_root / "shared" / "epistemic.py").write_text(
        "# Forbidden in new code: GovernanceDecision, Authority*\n", encoding="utf-8"
    )
    allowlist_file = code_root / ALLOWLIST_RELPATH
    allowlist_file.parent.mkdir(parents=True)
    allowlist_file.write_text(
        "shared/epistemic.py :: Forbidden in new code: GovernanceDecision, Authority*\n",
        encoding="utf-8",
    )
    assert run_all_checks(code_root) == []


def test_missing_migrations_dir_passes(tmp_path: Path) -> None:
    assert lint_migrations(_make_code_root(tmp_path)) == []


def test_empty_migrations_dir_passes(tmp_path: Path) -> None:
    code_root = _make_code_root(tmp_path)
    (code_root / MIGRATIONS_RELPATH).mkdir(parents=True)
    assert lint_migrations(code_root) == []


def test_lawful_canonical_ddl_passes(tmp_path: Path) -> None:
    code_root = _make_code_root(tmp_path)
    migrations = code_root / MIGRATIONS_RELPATH
    migrations.mkdir(parents=True)
    (migrations / "0001_canonical.sql").write_text(
        _LAWFUL_CANONICAL_SQL, encoding="utf-8"
    )
    assert lint_migrations(code_root) == []


def test_lawful_intake_ddl_passes(tmp_path: Path) -> None:
    """DTM-0007 — artifact (append-only) + mutable promotion_candidate are lawful."""
    code_root = _make_code_root(tmp_path)
    migrations = code_root / MIGRATIONS_RELPATH
    migrations.mkdir(parents=True)
    (migrations / "0002_intake.sql").write_text(_LAWFUL_INTAKE_SQL, encoding="utf-8")
    assert lint_migrations(code_root) == []


def test_mutations_on_non_canonical_tables_pass() -> None:
    sql = (
        "UPDATE derived.projection SET stale = true;\n"
        "DELETE FROM derived.projection WHERE stale;\n"
        "DROP TABLE scratch_notes;\n"
        "ALTER TABLE derived.projection ADD COLUMN note text;\n"
    )
    assert lint_migration_sql(sql) == []


def test_no_authority_dir_in_clean_backend(tmp_path: Path) -> None:
    assert check_authority_dir(_make_code_root(tmp_path)) == []


def test_token_scan_ignores_non_py_and_outside_roots(tmp_path: Path) -> None:
    code_root = _make_code_root(tmp_path)
    (code_root / "backend" / "notes.md").write_text(
        "GovernanceDecision is forbidden\n", encoding="utf-8"
    )
    (code_root / "docs").mkdir()
    (code_root / "docs" / "log.py").write_text("Authority = 1\n", encoding="utf-8")
    assert scan_forbidden_tokens(code_root, []) == []


def test_allowlist_loader_skips_comments_and_blanks(tmp_path: Path) -> None:
    allowlist = tmp_path / "allow.txt"
    allowlist.write_text(
        "# comment\n\nshared/x.py :: No Authority engine\nmalformed-line\n",
        encoding="utf-8",
    )
    assert load_allowlist(allowlist) == [("shared/x.py", "No Authority engine")]
