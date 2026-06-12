"""Gate 2 — contract-traceability (Deployment Governance §4 gate 2; hard gate).

Every increment must cite an approved contract id in its PR body; un-contracted
code fails. Phase-I exemption (deep-task decision #3, owner-confirmed 2026-06-12):
PRs labeled ``phase-1-infra`` bypass this gate until the owner closes Phase I —
the label is retired at Phase I exit.

Pure logic lives in :func:`check_contract_citation`; the CLI main reads the PR
body and labels from ``PR_BODY`` / ``PR_LABELS`` env vars (set by the workflow
from the GitHub event — env injection keeps untrusted PR text out of the shell)
or from ``--body`` / ``--labels`` flags, and exits 0 (pass) / 1 (fail).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections.abc import Sequence

# Approved contract ids — source of truth: 20_handoff/ contract packages and the
# starter-kit ci-pipeline.yml gate-2 list. Additions require owner ratification.
APPROVED_CONTRACT_IDS: frozenset[str] = frozenset(
    {
        "IC-WA-00R",
        "IC-WA-001",
        "IC-WA-002",
        "IC-WB-INFER",
        "IC-WB-EVAL",
        "IC-WC-ADVISE",
        "IC-WU-ACCEPT",
        "IC-WE-DISCLOSE",
    }
)

# Phase-I-only bypass label (decision #3). Retired at Phase I exit.
BYPASS_LABEL = "phase-1-infra"

# Candidate ids are extracted case-sensitively: contract ids are uppercase by
# convention and a lowercase mention is not a citation.
_CONTRACT_ID_PATTERN = re.compile(r"\bIC-[A-Z0-9]+(?:-[A-Z0-9]+)*\b")


def check_contract_citation(
    pr_body: str | None, labels: Sequence[str]
) -> tuple[bool, str]:
    """Return ``(passed, message)`` for the contract-traceability gate.

    Pass iff the bypass label is present, or the body cites at least one
    approved contract id. Citing only unknown ``IC-*`` ids still fails.
    """
    if BYPASS_LABEL in labels:
        return (
            True,
            f"BYPASS: label '{BYPASS_LABEL}' present (Phase-I infra exemption, "
            "decision #3; retired at Phase I exit).",
        )

    cited = set(_CONTRACT_ID_PATTERN.findall(pr_body or ""))
    approved = sorted(cited & APPROVED_CONTRACT_IDS)
    if approved:
        return (True, f"PASS: PR cites approved contract id(s): {', '.join(approved)}.")

    if cited:
        return (
            False,
            "FAIL: PR cites only unapproved contract id(s): "
            f"{', '.join(sorted(cited))}. Approved ids: "
            f"{', '.join(sorted(APPROVED_CONTRACT_IDS))}.",
        )
    return (
        False,
        "FAIL: PR body cites no contract id. Un-contracted code fails "
        "(Deployment Governance §4 gate 2). Cite one of: "
        f"{', '.join(sorted(APPROVED_CONTRACT_IDS))}, or label the PR "
        f"'{BYPASS_LABEL}' (Phase I infra only).",
    )


def parse_labels(raw: str | None) -> list[str]:
    """Parse labels from a JSON array (workflow's ``toJSON(...)``) or a comma list."""
    if not raw:
        return []
    raw = raw.strip()
    if raw.startswith("["):
        parsed = json.loads(raw)
        return [str(item) for item in parsed]
    return [part.strip() for part in raw.split(",") if part.strip()]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--body",
        default=None,
        help="PR body text (default: PR_BODY env var).",
    )
    parser.add_argument(
        "--labels",
        default=None,
        help="PR labels as a JSON array or comma list (default: PR_LABELS env var).",
    )
    args = parser.parse_args(argv)

    body = args.body if args.body is not None else os.environ.get("PR_BODY")
    labels = parse_labels(
        args.labels if args.labels is not None else os.environ.get("PR_LABELS")
    )

    passed, message = check_contract_citation(body, labels)
    print(f"[gate-2 contract-traceability] {message}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
