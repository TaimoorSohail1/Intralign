"""Gate 4 — epistemic-invariant gate (Deployment Governance §4 gate 4; Critical on violation).

Static checks enforcing the DL-043 invariants (deep-task decision #8):

a. **Forbidden-token scan** — any occurrence of ``GovernanceDecision`` or
   ``Authority`` (word-start match, so ``AuthorityEngine`` is caught) in ``.py``
   files under ``code/backend`` and ``code/shared`` fails, EXCEPT lines listed in
   the explicit allowlist file ``code/ci/invariant_allowlist.txt`` (existing
   prose mentions like "No Authority engine"). Allowlist additions are reviewed
   under gate 7 — do not allowlist identifiers.
b. **No Authority module** — a directory named ``authority`` anywhere under
   ``code/backend`` fails (R1: specified-but-inactive; never built).
c. **Migration linter** — ``.sql`` files under ``code/supabase/migrations/`` must
   not contain ``UPDATE`` / ``DELETE`` / ``DROP TABLE`` / ``ALTER TABLE``
   statements TARGETING a canonical table (``attested_assertion``,
   ``cognition_history_record``, ``user_acceptance_record``, ``history_record``,
   ``artifact`` — the DTM-0007 append-only evidence anchor, LDM §2.3).
   ``CREATE`` / ``GRANT`` / ``REVOKE`` (including ``REVOKE UPDATE, DELETE``) /
   ``CREATE TRIGGER ... BEFORE UPDATE OR DELETE`` are fine — the linter is
   statement-aware, not keyword-grep. Dollar-quoted function bodies and SQL
   comments are stripped before linting (gate 7 human review backstops what a
   static linter cannot see). A missing or empty migrations dir passes — no
   migrations exist yet in Phase I.

Pure logic; the CLI main takes ``--code-root`` (default: this file's parent's
parent, i.e. ``code/``) and exits 0 (pass) / 1 (fail), printing every violation.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from pathlib import Path

# (a) Forbidden vocabulary — CLAUDE.md hard rule 4 + canonical vocabulary.
FORBIDDEN_TOKENS: tuple[str, ...] = ("GovernanceDecision", "Authority")
_TOKEN_PATTERN = re.compile(r"\b(?:GovernanceDecision|Authority)")

# Roots scanned for forbidden tokens, relative to code/.
SCAN_ROOTS: tuple[str, ...] = ("backend", "shared")

# (b) Forbidden module name under code/backend.
FORBIDDEN_DIR_NAME = "authority"

# (c) Append-only canonical tables (LDM §2; decision #4).
# DTM-0007 (IC-WA-001): + 'artifact' — the append-only evidence anchor
# (LDM §2.3). promotion_candidate is transient/mutable and deliberately absent.
CANONICAL_TABLES: frozenset[str] = frozenset(
    {
        "attested_assertion",
        "cognition_history_record",
        "user_acceptance_record",
        "history_record",
        "artifact",
    }
)

MIGRATIONS_RELPATH = "supabase/migrations"
ALLOWLIST_RELPATH = "ci/invariant_allowlist.txt"

# SQL normalization: strip comments and dollar-quoted bodies so REVOKE/TRIGGER
# clauses and function bodies don't false-positive the statement scan.
_SQL_LINE_COMMENT = re.compile(r"--[^\n]*")
_SQL_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
_SQL_DOLLAR_QUOTED = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)?\$.*?\$\1\$", re.DOTALL)

# A statement is forbidden iff it BEGINS with one of these verbs and targets a
# canonical table. REVOKE/GRANT/CREATE never match (they don't begin with these).
_FORBIDDEN_STMT = re.compile(
    r"^\s*(?:"
    r"UPDATE\s+(?:ONLY\s+)?(?P<update>\S+)"
    r"|DELETE\s+FROM\s+(?:ONLY\s+)?(?P<delete>\S+)"
    r"|DROP\s+TABLE\s+(?:IF\s+EXISTS\s+)?(?P<drop>\S+)"
    r"|ALTER\s+TABLE\s+(?:IF\s+EXISTS\s+)?(?:ONLY\s+)?(?P<alter>\S+)"
    r")",
    re.IGNORECASE,
)


def load_allowlist(allowlist_path: Path) -> list[tuple[str, str]]:
    """Load ``(relpath, line-substring)`` allowlist entries; ``#`` and blanks skipped."""
    entries: list[tuple[str, str]] = []
    if not allowlist_path.is_file():
        return entries
    for raw in allowlist_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        path_part, sep, substring = line.partition("::")
        if not sep or not substring.strip():
            continue
        entries.append((path_part.strip(), substring.strip()))
    return entries


def _is_allowlisted(
    relpath: str, line: str, allowlist: Sequence[tuple[str, str]]
) -> bool:
    return any(
        entry_path == relpath and entry_sub in line
        for entry_path, entry_sub in allowlist
    )


def scan_forbidden_tokens(
    code_root: Path, allowlist: Sequence[tuple[str, str]]
) -> list[str]:
    """(a) Flag forbidden tokens in .py files under the scan roots, minus allowlist."""
    violations: list[str] = []
    for root_name in SCAN_ROOTS:
        root = code_root / root_name
        if not root.is_dir():
            continue
        for py_file in sorted(root.rglob("*.py")):
            relpath = py_file.relative_to(code_root).as_posix()
            for lineno, line in enumerate(
                py_file.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if not _TOKEN_PATTERN.search(line):
                    continue
                if _is_allowlisted(relpath, line, allowlist):
                    continue
                violations.append(
                    f"{relpath}:{lineno}: forbidden token "
                    f"({' / '.join(FORBIDDEN_TOKENS)}) — add to "
                    f"{ALLOWLIST_RELPATH} ONLY for prose mentions, never identifiers: "
                    f"{line.strip()}"
                )
    return violations


def check_authority_dir(code_root: Path) -> list[str]:
    """(b) Flag any directory named ``authority`` under code/backend."""
    backend = code_root / "backend"
    if not backend.is_dir():
        return []
    return [
        f"{path.relative_to(code_root).as_posix()}/: forbidden module — "
        "no Authority engine in R1 (CLAUDE.md hard rule 4)"
        for path in sorted(backend.rglob("*"))
        if path.is_dir() and path.name.lower() == FORBIDDEN_DIR_NAME
    ]


def _normalize_sql(sql: str) -> str:
    sql = _SQL_BLOCK_COMMENT.sub(" ", sql)
    sql = _SQL_LINE_COMMENT.sub(" ", sql)
    return _SQL_DOLLAR_QUOTED.sub(" 'BODY' ", sql)


def _target_table(raw_identifier: str) -> str:
    """Reduce a SQL identifier to a bare lowercase table name (drop schema/quotes)."""
    cleaned = raw_identifier.strip().rstrip(";,")
    return cleaned.split(".")[-1].strip('"').lower()


def lint_migration_sql(sql: str) -> list[str]:
    """(c) Return one message per statement that mutates a canonical table."""
    violations: list[str] = []
    for statement in _normalize_sql(sql).split(";"):
        match = _FORBIDDEN_STMT.match(statement)
        if not match:
            continue
        verb, raw_target = next(
            (name, value)
            for name, value in match.groupdict().items()
            if value is not None
        )
        table = _target_table(raw_target)
        if table in CANONICAL_TABLES:
            violations.append(
                f"{verb.upper()} statement targets append-only canonical table "
                f"'{table}' (Deployment Governance §5; DL-043): "
                f"{' '.join(statement.split())[:120]}"
            )
    return violations


def lint_migrations(code_root: Path) -> list[str]:
    """Lint every .sql migration; a missing or empty migrations dir passes."""
    migrations_dir = code_root / MIGRATIONS_RELPATH
    if not migrations_dir.is_dir():
        return []
    violations: list[str] = []
    for sql_file in sorted(migrations_dir.rglob("*.sql")):
        relpath = sql_file.relative_to(code_root).as_posix()
        violations.extend(
            f"{relpath}: {message}"
            for message in lint_migration_sql(sql_file.read_text(encoding="utf-8"))
        )
    return violations


def run_all_checks(code_root: Path) -> list[str]:
    """Run checks (a)+(b)+(c); empty list == gate passes."""
    allowlist = load_allowlist(code_root / ALLOWLIST_RELPATH)
    return [
        *scan_forbidden_tokens(code_root, allowlist),
        *check_authority_dir(code_root),
        *lint_migrations(code_root),
    ]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--code-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="App root (the code/ directory). Default: parent of ci/.",
    )
    args = parser.parse_args(argv)

    violations = run_all_checks(args.code_root)
    if violations:
        print(
            f"[gate-4 epistemic-invariant] FAIL — {len(violations)} violation(s) "
            "(Critical; Deployment Governance §4 gate 4):"
        )
        for violation in violations:
            print(f"  - {violation}")
        return 1
    print(
        "[gate-4 epistemic-invariant] PASS: no forbidden tokens, no authority "
        "module, no canonical-table mutations in migrations."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
