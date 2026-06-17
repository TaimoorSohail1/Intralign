"""Gate 4 (epistemic-invariant) — negative: tokens, authority dir, and mutating SQL all fail."""

from pathlib import Path

import pytest

from ci.gate_invariants import (
    MIGRATIONS_RELPATH,
    check_authority_dir,
    lint_migration_sql,
    lint_migrations,
    main,
    run_all_checks,
    scan_forbidden_tokens,
)


def _make_code_root(tmp_path: Path) -> Path:
    (tmp_path / "backend").mkdir()
    (tmp_path / "shared").mkdir()
    return tmp_path


# --- (a) forbidden-token scan ---


def test_governance_decision_identifier_detected(tmp_path: Path) -> None:
    code_root = _make_code_root(tmp_path)
    (code_root / "backend" / "bad.py").write_text(
        "class GovernanceDecision:\n    pass\n", encoding="utf-8"
    )
    violations = scan_forbidden_tokens(code_root, [])
    assert len(violations) == 1
    assert "backend/bad.py:1" in violations[0]


def test_authority_prefixed_identifier_detected(tmp_path: Path) -> None:
    code_root = _make_code_root(tmp_path)
    (code_root / "shared" / "bad.py").write_text(
        "class AuthorityEngine:\n    pass\n", encoding="utf-8"
    )
    assert len(scan_forbidden_tokens(code_root, [])) == 1


def test_token_in_docstring_without_allowlist_detected(tmp_path: Path) -> None:
    # Spec keeps it simple: ANY occurrence flags unless explicitly allowlisted.
    code_root = _make_code_root(tmp_path)
    (code_root / "backend" / "doc.py").write_text(
        '"""No Authority engine in R1."""\n', encoding="utf-8"
    )
    assert len(scan_forbidden_tokens(code_root, [])) == 1


def test_allowlist_entry_for_other_file_does_not_exempt(tmp_path: Path) -> None:
    code_root = _make_code_root(tmp_path)
    (code_root / "backend" / "bad.py").write_text(
        "# No Authority engine\n", encoding="utf-8"
    )
    allowlist = [("shared/epistemic.py", "No Authority engine")]
    assert len(scan_forbidden_tokens(code_root, allowlist)) == 1


# --- (b) authority module ---


def test_authority_dir_detected(tmp_path: Path) -> None:
    code_root = _make_code_root(tmp_path)
    (code_root / "backend" / "authority").mkdir()
    violations = check_authority_dir(code_root)
    assert len(violations) == 1
    assert "backend/authority" in violations[0]


def test_nested_authority_dir_detected(tmp_path: Path) -> None:
    code_root = _make_code_root(tmp_path)
    (code_root / "backend" / "responsibilities" / "Authority").mkdir(parents=True)
    assert len(check_authority_dir(code_root)) == 1


# --- (c) migration linter ---


@pytest.mark.parametrize(
    ("sql", "verb"),
    [
        ("UPDATE attested_assertion SET attesting_source = 'x';", "UPDATE"),
        ("DELETE FROM cognition_history_record WHERE id = '1';", "DELETE"),
        ("DROP TABLE user_acceptance_record;", "DROP"),
        ("ALTER TABLE history_record DROP COLUMN payload;", "ALTER"),
        # DTM-0007: artifact is a canonical append-only evidence anchor (LDM §2.3)
        ("UPDATE artifact SET body_ref = 'x';", "UPDATE"),
        ("DELETE FROM artifact WHERE artifact_id = '1';", "DELETE"),
        ("DROP TABLE artifact;", "DROP"),
        ("ALTER TABLE artifact DROP COLUMN provenance;", "ALTER"),
    ],
)
def test_each_mutation_verb_on_canonical_table_rejected(sql: str, verb: str) -> None:
    violations = lint_migration_sql(sql)
    assert len(violations) == 1
    assert verb in violations[0]


def test_schema_qualified_and_quoted_targets_rejected() -> None:
    assert lint_migration_sql("UPDATE public.attested_assertion SET x = 1;")
    assert lint_migration_sql('DELETE FROM "history_record";')
    assert lint_migration_sql("DROP TABLE IF EXISTS public.history_record;")
    assert lint_migration_sql("ALTER TABLE ONLY cognition_history_record DROP COLUMN x;")


def test_lowercase_statements_rejected() -> None:
    assert lint_migration_sql("update attested_assertion set x = 1;")


def test_mutation_after_lawful_statements_still_rejected() -> None:
    sql = (
        "CREATE TABLE attested_assertion (id uuid);\n"
        "REVOKE UPDATE, DELETE ON attested_assertion FROM PUBLIC;\n"
        "DELETE FROM attested_assertion;\n"
    )
    violations = lint_migration_sql(sql)
    assert len(violations) == 1
    assert "DELETE" in violations[0]


# --- (c) reviewed ALTER allowlist stays TIGHT (DTM-0009, owner-approved) ---

_DTM0009_RELPATH = (
    f"{MIGRATIONS_RELPATH}/20260617120000_chr_output_kind_wave_s.sql"
)
# The exact substrings shipped in ci/invariant_allowlist.txt for DTM-0009.
_DTM0009_ALLOWLIST = [
    (
        _DTM0009_RELPATH,
        "drop constraint if exists cognition_history_record_output_kind_check",
    ),
    (
        _DTM0009_RELPATH,
        "add constraint cognition_history_record_output_kind_check check (output_kind in",
    ),
]


def test_allowlist_never_exempts_update_delete_drop() -> None:
    # Even with the DTM-0009 allowlist active, real data mutations still fail —
    # the exemption only ever short-circuits an ALTER.
    assert lint_migration_sql(
        "UPDATE cognition_history_record SET output_kind = 'x';",
        _DTM0009_RELPATH,
        _DTM0009_ALLOWLIST,
    )
    assert lint_migration_sql(
        "DELETE FROM cognition_history_record;", _DTM0009_RELPATH, _DTM0009_ALLOWLIST
    )
    assert lint_migration_sql(
        "DROP TABLE cognition_history_record;", _DTM0009_RELPATH, _DTM0009_ALLOWLIST
    )


def test_allowlist_does_not_exempt_other_canonical_alter() -> None:
    # A DIFFERENT ALTER on the same canonical table (not in the allowlist) fails.
    assert lint_migration_sql(
        "ALTER TABLE cognition_history_record DROP COLUMN output_payload;",
        _DTM0009_RELPATH,
        _DTM0009_ALLOWLIST,
    )


def test_allowlist_is_path_scoped() -> None:
    # The allowlisted ALTER text on a DIFFERENT migration path is NOT exempt.
    assert lint_migration_sql(
        "alter table cognition_history_record "
        "drop constraint if exists cognition_history_record_output_kind_check;",
        f"{MIGRATIONS_RELPATH}/other.sql",
        _DTM0009_ALLOWLIST,
    )


def test_bad_migration_file_fails_lint(tmp_path: Path) -> None:
    code_root = _make_code_root(tmp_path)
    migrations = code_root / MIGRATIONS_RELPATH
    migrations.mkdir(parents=True)
    (migrations / "0002_bad.sql").write_text(
        "UPDATE attested_assertion SET attesting_source = 'oslo';\n", encoding="utf-8"
    )
    violations = lint_migrations(code_root)
    assert len(violations) == 1
    assert "0002_bad.sql" in violations[0]


# --- aggregate + CLI ---


def test_run_all_checks_aggregates_all_violation_kinds(tmp_path: Path) -> None:
    code_root = _make_code_root(tmp_path)
    (code_root / "backend" / "bad.py").write_text(
        "GovernanceDecision = object()\n", encoding="utf-8"
    )
    (code_root / "backend" / "authority").mkdir()
    migrations = code_root / MIGRATIONS_RELPATH
    migrations.mkdir(parents=True)
    (migrations / "0003.sql").write_text(
        "DROP TABLE history_record;\n", encoding="utf-8"
    )
    assert len(run_all_checks(code_root)) == 3


def test_cli_main_exits_one_on_violation(tmp_path: Path) -> None:
    code_root = _make_code_root(tmp_path)
    (code_root / "shared" / "bad.py").write_text("Authority = True\n", encoding="utf-8")
    assert main(["--code-root", str(code_root)]) == 1
