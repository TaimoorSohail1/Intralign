"""Phase 0 positive tests for the R2 doctrine-guardrail contract gate."""

from pathlib import Path

from ci.gate_r2_guardrails import evaluate_repository


REPOSITORY_ROOT = Path(__file__).resolve().parents[4]


def test_authoritative_r2_contract_is_registered_and_bound() -> None:
    report = evaluate_repository(REPOSITORY_ROOT)

    assert report.errors == ()
    assert report.phase0_guard_count == 50
    assert report.registered_guard_count == 60
    assert report.surface_count == 58
    assert report.machine_surface_count == 58
    assert report.route_count == 16
    assert report.prototype_correction_count == 6
    assert report.active_guard_count == 53
    assert report.pending_guard_count == 7
    assert len(report.active_test_selectors) == 41
    assert len(report.active_client_test_files) == 4
