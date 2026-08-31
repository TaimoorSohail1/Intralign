"""Phase 0 negative tests for the R2 doctrine-guardrail contract gate."""

import json
from pathlib import Path

from ci.gate_r2_guardrails import evaluate_repository, run_active_tests


APPLICATION_ROOT = Path(__file__).resolve().parents[3]


def _stage_contract(tmp_path: Path) -> tuple[dict[str, object], str]:
    registry = json.loads(
        (APPLICATION_ROOT / "ci" / "r2_guardrails.json").read_text(
            encoding="utf-8"
        )
    )
    guards = registry["guards"]
    assert isinstance(guards, dict)
    for registration in guards.values():
        assert isinstance(registration, dict)
        registration["status"] = "pending"
        registration["tests"] = []
        registration["client_tests"] = []
        registration["pending_reason"] = "Staged as pending for this isolated gate test."
    markdown = (
        APPLICATION_ROOT / "ci" / "contracts" / "r2-doctrine-guardrails.md"
    ).read_text(encoding="utf-8")

    return registry, markdown


def _write_contract(tmp_path: Path, registry: dict[str, object], markdown: str) -> None:
    contract_target = tmp_path / str(registry["contract_path"])
    contract_target.parent.mkdir(parents=True)
    contract_target.write_text(markdown, encoding="utf-8")

    registry_target = tmp_path / "ci" / "r2_guardrails.json"
    registry_target.parent.mkdir(parents=True, exist_ok=True)
    registry_target.write_text(json.dumps(registry), encoding="utf-8")

    surface_registry_target = tmp_path / "ci" / "r2_surface_contracts.json"
    surface_registry_target.write_text(
        (APPLICATION_ROOT / "ci" / "r2_surface_contracts.json").read_text(
            encoding="utf-8"
        ),
        encoding="utf-8",
    )
    surface_registry = json.loads(surface_registry_target.read_text(encoding="utf-8"))
    bound_paths: set[str] = set()
    for profile in surface_registry["profiles"].values():
        for field in ("frontend", "backend", "tests"):
            bound_paths.update(reference.split("::", 1)[0] for reference in profile[field])
    for route in surface_registry["routes"]:
        bound_paths.add(route["frontend"])
        bound_paths.update(route["backend"])
    for relative_path in bound_paths:
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.touch()

    prototype_target = tmp_path / "ci" / "contracts" / "oslo-prototype-r2.html"
    prototype_target.parent.mkdir(parents=True, exist_ok=True)
    prototype_target.write_text(
        (APPLICATION_ROOT / "ci" / "contracts" / "oslo-prototype-r2.html").read_text(
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


def test_missing_machine_surface_registry_fails_the_gate(tmp_path: Path) -> None:
    registry, markdown = _stage_contract(tmp_path)
    _write_contract(tmp_path, registry, markdown)
    (tmp_path / "ci" / "r2_surface_contracts.json").unlink()

    report = evaluate_repository(tmp_path)

    assert "R2 machine surface registry is missing" in report.errors


def test_an_active_red_guard_fails_the_gate(tmp_path: Path) -> None:
    registry, markdown = _stage_contract(tmp_path)
    guards = registry["guards"]
    assert isinstance(guards, dict)
    guards["GT-10"] = {
        "status": "active",
        "tests": ["tests/r2/test_red_guard.py::test_red_guard"],
    }
    red_test = tmp_path / "tests" / "r2" / "test_red_guard.py"
    red_test.parent.mkdir(parents=True)
    red_test.write_text("def test_red_guard():\n    assert False\n", encoding="utf-8")
    _write_contract(tmp_path, registry, markdown)

    report = evaluate_repository(tmp_path)

    assert report.errors == ()
    assert run_active_tests(report, tmp_path) != 0


def test_a_pending_guard_without_a_reason_fails_the_gate(tmp_path: Path) -> None:
    registry, markdown = _stage_contract(tmp_path)
    guards = registry["guards"]
    assert isinstance(guards, dict)
    guards["GT-04"] = {"status": "pending", "tests": [], "pending_reason": ""}
    _write_contract(tmp_path, registry, markdown)

    report = evaluate_repository(tmp_path)

    assert "Pending guard GT-04 must explain why it is not active" in report.errors


def test_an_active_guard_with_a_missing_client_test_fails_the_gate(tmp_path: Path) -> None:
    registry, markdown = _stage_contract(tmp_path)
    guards = registry["guards"]
    assert isinstance(guards, dict)
    guards["GT-21"] = {
        "status": "active",
        "tests": [],
        "client_tests": ["apps/web/src/components/missing.test.tsx"],
    }
    _write_contract(tmp_path, registry, markdown)

    report = evaluate_repository(tmp_path)

    assert (
        "Active guard GT-21 client test file does not exist: "
        "apps/web/src/components/missing.test.tsx"
    ) in report.errors


def test_a_declared_prototype_capability_without_a_simulation_fails_the_gate(
    tmp_path: Path,
) -> None:
    registry, markdown = _stage_contract(tmp_path)
    _write_contract(tmp_path, registry, markdown)
    prototype = tmp_path / "ci" / "contracts" / "oslo-prototype-r2.html"
    source = prototype.read_text(encoding="utf-8")
    prototype.write_text(source.replace("SIM:#24", "SIM:#23"), encoding="utf-8")

    report = evaluate_repository(tmp_path)

    assert "R2 prototype capability has no SIM tag or arc exception: 24" in report.errors
