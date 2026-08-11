"""Phase 0 negative tests for the R2 doctrine-guardrail contract gate."""

import json
from pathlib import Path

from ci.gate_r2_guardrails import evaluate_repository, run_active_tests


REPOSITORY_ROOT = Path(__file__).resolve().parents[4]


def _stage_contract(tmp_path: Path) -> tuple[dict[str, object], str]:
    registry = json.loads(
        (REPOSITORY_ROOT / "code" / "ci" / "r2_guardrails.json").read_text(
            encoding="utf-8"
        )
    )
    markdown = (
        REPOSITORY_ROOT
        / "release-2"
        / "slices"
        / "09-doctrine-guardrails-integration-map.md"
    ).read_text(encoding="utf-8")

    return registry, markdown


def _write_contract(tmp_path: Path, registry: dict[str, object], markdown: str) -> None:
    contract_target = tmp_path / str(registry["contract_path"])
    contract_target.parent.mkdir(parents=True)
    contract_target.write_text(markdown, encoding="utf-8")

    registry_target = tmp_path / "code" / "ci" / "r2_guardrails.json"
    registry_target.parent.mkdir(parents=True)
    registry_target.write_text(json.dumps(registry), encoding="utf-8")

    prototype_target = tmp_path / "release-2" / "oslo-prototype-r2.html"
    prototype_target.write_text(
        (REPOSITORY_ROOT / "release-2" / "oslo-prototype-r2.html").read_text(
            encoding="utf-8"
        ),
        encoding="utf-8",
    )


def test_removing_a_registered_guard_fails_the_gate(tmp_path: Path) -> None:
    registry, markdown = _stage_contract(tmp_path)
    guards = registry["guards"]
    assert isinstance(guards, dict)
    guards.pop("GT-10")
    _write_contract(tmp_path, registry, markdown)

    report = evaluate_repository(tmp_path)

    assert "Slice 9 guard is not registered: GT-10" in report.errors


def test_a_surface_without_an_async_contract_fails_the_gate(tmp_path: Path) -> None:
    registry, markdown = _stage_contract(tmp_path)
    markdown = markdown.replace(
        "| First read render | 3 | Fast-Pass output = L1a (7 artifacts + outcomes + 3 pillars) | — | `reanalysis.landed` (fast) | A |",
        "| First read render | 3 | Fast-Pass output = L1a (7 artifacts + outcomes + 3 pillars) | — | `reanalysis.landed` (fast) | |",
    )
    _write_contract(tmp_path, registry, markdown)

    report = evaluate_repository(tmp_path)

    assert "Integration Map row 21 has empty fields: Async" in report.errors


def test_an_active_red_guard_fails_the_gate(tmp_path: Path) -> None:
    registry, markdown = _stage_contract(tmp_path)
    guards = registry["guards"]
    assert isinstance(guards, dict)
    guards["GT-10"] = {
        "status": "active",
        "tests": ["tests/r2/test_red_guard.py::test_red_guard"],
    }
    red_test = tmp_path / "code" / "tests" / "r2" / "test_red_guard.py"
    red_test.parent.mkdir(parents=True)
    red_test.write_text("def test_red_guard():\n    assert False\n", encoding="utf-8")
    _write_contract(tmp_path, registry, markdown)

    report = evaluate_repository(tmp_path)

    assert report.errors == ()
    assert run_active_tests(report, tmp_path) != 0
