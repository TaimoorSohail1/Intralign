from __future__ import annotations

import json
from pathlib import Path


def test_integrity_maturity_guard_runs_as_a_client_test() -> None:
    code_root = Path(__file__).resolve().parents[4]
    registry = json.loads(
        (code_root / "ci" / "r2_guardrails.json").read_text(encoding="utf-8")
    )
    guard = registry["guards"]["GT-20"]

    assert guard["status"] == "active"
    assert guard["client_tests"] == [
        "apps/web/src/components/overview/project-overview.test.tsx"
    ]
    assert (
        code_root / guard["client_tests"][0]
    ).is_file(), "GT-20 must execute its rendered maturity-word assertions in the client lane"
