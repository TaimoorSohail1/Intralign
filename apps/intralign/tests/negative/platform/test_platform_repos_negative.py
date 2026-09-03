"""DTM-0031 negative suite (Critical) — platform persistence boundaries.

Proves IMPOSSIBILITY, not mere absence (code/CLAUDE.md hard rules #2/#3; gate-4):

- The platform migration touches NO canonical table: scanning the migration SQL
  for any ALTER/UPDATE/DELETE/DROP TABLE targeting a canonical table finds none
  (the gate-4 linter — ``ci.gate_invariants`` — is the authority; this asserts
  it directly on the new file).
- The platform repos write the PLATFORM layer ONLY: no repo module names a
  canonical table (``attested_assertion`` / ``cognition_history_record`` /
  ``user_acceptance_record`` / ``history_record``) in any ``.table(...)`` call,
  and a round-trip leaves the canonical buckets of the store completely empty
  (the repos never insert a canonical/CHR row).
- Workspace scoping is structural: a cross-workspace read returns nothing.
"""

from __future__ import annotations

import ast
import inspect
import re
import uuid
from pathlib import Path

import backend.platform.analysis_run_repo as analysis_run_repo
import backend.platform.notification_repo as notification_repo
import backend.platform.project_repo as project_repo
from backend.platform import (
    SupabaseAnalysisRunRepository,
    SupabaseNotificationRepository,
    SupabaseProjectRepository,
)
from ci.gate_invariants import CANONICAL_TABLES, _normalize_sql, lint_migration_sql

from tests.support.fake_supabase import FakeSupabaseClient

WS_A = str(uuid.uuid4())
WS_B = str(uuid.uuid4())

_MIGRATION = (
    Path(__file__).resolve().parents[3]
    / "supabase" / "migrations" / "20260626120000_platform_tables.sql"
)


# --- the migration mutates NO canonical table (gate-4 linter is the authority) -

def test_platform_migration_touches_no_canonical_table() -> None:
    sql = _MIGRATION.read_text(encoding="utf-8")
    violations = lint_migration_sql(sql, relpath=_MIGRATION.name)
    assert violations == [], (
        f"platform migration mutates a canonical table: {violations}"
    )


def test_platform_migration_names_no_canonical_table_in_executable_sql() -> None:
    """Belt: outside SQL comments (the linter strips them), the migration's
    EXECUTABLE statements reference no canonical table by name at all — the
    platform tables are wholly distinct relations. (The doc-comment that lists
    the canonical tables to explain what is NOT touched is intentionally
    excluded by ``_normalize_sql``, exactly as gate-4 does. Whole-identifier
    matching avoids a false hit on the Data Model enum value ``shared_artifact``,
    which merely CONTAINS the canonical-table substring ``artifact``.)"""
    executable = _normalize_sql(_MIGRATION.read_text(encoding="utf-8")).lower()
    for table in CANONICAL_TABLES:
        assert not re.search(rf"\b{re.escape(table)}\b", executable), (
            f"platform migration references canonical table '{table}' in executable SQL"
        )


# --- repos name no canonical table (static AST scan over the repo modules) -----

_CANONICAL_TABLES = {
    "attested_assertion",
    "cognition_history_record",
    "user_acceptance_record",
    "history_record",
}


def _table_targets(source: str) -> set[str]:
    targets: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "table"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        ):
            targets.add(node.args[0].value)
    return targets


def test_repos_name_no_canonical_table() -> None:
    for module in (project_repo, analysis_run_repo, notification_repo):
        source = Path(inspect.getfile(module)).read_text(encoding="utf-8")
        offending = _table_targets(source) & _CANONICAL_TABLES
        assert offending == set(), (
            f"{module.__name__} references canonical table(s) {offending} — "
            "platform repos write the platform layer ONLY (hard rule #2)"
        )


def test_repos_have_no_canonical_write_method() -> None:
    for repo_cls in (
        SupabaseProjectRepository,
        SupabaseAnalysisRunRepository,
        SupabaseNotificationRepository,
    ):
        public = {n for n in vars(repo_cls) if not n.startswith("_")}
        for forbidden in (
            "insert_assertion", "insert_acceptance", "insert_history",
            "insert_chr", "append", "append_chr",
        ):
            assert forbidden not in public
            assert not hasattr(repo_cls, forbidden)


# --- a full round-trip never writes a canonical/CHR row ------------------------

def test_round_trip_leaves_canonical_buckets_empty() -> None:
    client = FakeSupabaseClient()
    pid = str(uuid.uuid4())
    run_id = str(uuid.uuid4())
    notif_id = str(uuid.uuid4())

    SupabaseProjectRepository(client).create({
        "project_id": pid, "workspace_id": WS_A, "lifecycle_state": "created"})
    SupabaseAnalysisRunRepository(client).create({
        "analysis_run_id": run_id, "project_id": pid,
        "run_type": "fast_analysis_pass", "run_status": "queued"})
    SupabaseNotificationRepository(client).create({
        "notification_id": notif_id, "workspace_id": WS_A,
        "source_object_type": "finding", "source_object_id": "s-1",
        "event_type": "e", "state": "created"})

    # No canonical/CHR bucket was ever created/written by the platform repos.
    for canonical in _CANONICAL_TABLES:
        assert ("public", canonical) not in client._tables, (
            f"platform repo wrote canonical table '{canonical}'"
        )
    # Only the three platform tables exist in the store.
    assert {name for (_schema, name) in client._tables} == {
        "project", "analysis_run", "notification"
    }


# --- cross-workspace isolation -------------------------------------------------

def test_cross_workspace_project_read_is_empty() -> None:
    client = FakeSupabaseClient()
    repo = SupabaseProjectRepository(client)
    repo.create({"project_id": str(uuid.uuid4()), "workspace_id": WS_A,
                 "lifecycle_state": "created"})
    # Workspace B has no projects — the scoped read returns nothing.
    assert repo.list_for_workspace(WS_B) == []


def test_cross_workspace_notification_read_is_empty() -> None:
    client = FakeSupabaseClient()
    repo = SupabaseNotificationRepository(client)
    repo.create({"notification_id": str(uuid.uuid4()), "workspace_id": WS_A,
                 "source_object_type": "finding", "source_object_id": "s-1",
                 "event_type": "e", "state": "created"})
    assert repo.list_for_workspace(WS_B) == []
