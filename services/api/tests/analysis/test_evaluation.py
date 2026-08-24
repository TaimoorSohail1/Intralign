import json
from pathlib import Path

from oslo_api.analysis.evaluation import (
    BenchmarkFinding,
    BenchmarkGates,
    BenchmarkManifest,
    BenchmarkObservation,
    BenchmarkTrap,
    evaluate_benchmark,
    evaluate_benchmark_series,
    manifest_from_mapping,
)
from oslo_api.analysis.models import ArtifactType, Issue


def _issue(
    issue_id: str,
    title: str,
    why: str,
    *,
    severity: str = "Moderate",
    evidence_refs: tuple[str, ...] = ("document:plan:page:4:fragment:1",),
) -> Issue:
    return Issue(
        id=issue_id,
        artifact_type=ArtifactType.SCHEDULE,
        dimension="Feasibility",
        severity=severity,
        title=title,
        why=why,
        recommendation="Resolve the conflict.",
        evidence_refs=evidence_refs,
    )


def test_benchmark_scores_recall_traps_locators_and_duplicates() -> None:
    manifest = BenchmarkManifest(
        name="Generic plan",
        findings=(
            BenchmarkFinding(
                id="F-01",
                severity="Critical",
                concepts=(("freeze", "blackout"), ("cutover", "migration")),
            ),
            BenchmarkFinding(
                id="F-02",
                severity="Moderate",
                concepts=(("contingency",), ("percent", "percentage", "%")),
            ),
        ),
        traps=(
            BenchmarkTrap(
                id="T-01",
                concepts=(("contingency",), ("unallocated",)),
            ),
        ),
    )
    issues = (
        _issue(
            "ISS-1",
            "Cutover conflicts with the freeze",
            "The migration starts during the protected blackout window.",
            severity="Critical",
        ),
        _issue(
            "ISS-2",
            "Contingency percentage does not reconcile",
            "The stated percent differs from the stated allowance.",
        ),
        _issue(
            "ISS-3",
            "Contingency is unallocated",
            "The plan keeps the contingency unallocated.",
        ),
        _issue(
            "ISS-4",
            "Cutover conflicts with freeze window",
            "Migration occurs during the same blackout.",
        ),
    )

    result = evaluate_benchmark(manifest, issues)

    assert result.findings_found == ("F-01", "F-02")
    assert result.finding_recall == 1
    assert result.critical_recall == 1
    assert result.false_positive_traps == ("T-01",)
    assert result.locator_coverage == 1
    assert result.duplicate_issue_ids == ("ISS-4",)
    assert result.passed is False


def test_default_benchmark_gates_match_the_approved_release_policy() -> None:
    gates = BenchmarkGates()

    assert gates.finding_recall == 0.9
    assert gates.critical_recall == 1
    assert gates.maximum_false_positive_traps == 0
    assert gates.locator_coverage == 1
    assert gates.maximum_duplicate_rate == 0


def test_repeated_benchmark_runs_must_keep_issue_ids_and_ratings_stable() -> None:
    manifest = BenchmarkManifest(
        name="Stable release fixture",
        findings=(
            BenchmarkFinding(
                id="F-01",
                severity="Critical",
                concepts=(("cutover",), ("freeze",)),
            ),
        ),
    )
    first_issue = _issue(
        "ISS-CUTOVER",
        "Cutover conflicts with the freeze",
        "The migration enters the protected freeze.",
        severity="Critical",
    )
    changed_id = _issue(
        "ISS-CHANGED",
        "Cutover conflicts with the freeze",
        "The migration enters the protected freeze.",
        severity="Critical",
    )

    result = evaluate_benchmark_series(
        manifest,
        (
            BenchmarkObservation(
                issues=(first_issue,),
                ratings=("High", "Low", "Low", "Moderate", "Low"),
                duration_seconds=80,
            ),
            BenchmarkObservation(
                issues=(changed_id,),
                ratings=("High", "Low", "Very Low", "Moderate", "Low"),
                duration_seconds=82,
            ),
        ),
    )

    assert result.issue_id_stability == 0
    assert result.rating_stability is False
    assert result.passed is False


def test_governed_release_manifests_are_valid_and_strict() -> None:
    manifest_directory = Path(__file__).parents[2] / "benchmarks" / "manifests"
    expected_counts = {
        "corveth.json": (17, 8),
        "greenway.json": (14, 8),
        "skyline.json": (15, 8),
        "tideline.json": (14, 8),
        "thornfield.json": (18, 8),
        "wayfarer.json": (18, 8),
        "ironvale.json": (16, 8),
        "millstone.json": (15, 8),
        "sb01-ferndale-dental.json": (3, 12),
        "sb02-ottolines-bakery.json": (3, 12),
        "sb03-ridgeway-grounds.json": (2, 12),
        "sb04-iron-harbour-gym.json": (3, 12),
        "sb05-halloran-pike.json": (3, 12),
        "sb06-marrow-co-coffee.json": (3, 12),
        "sb07-brackenfield-vets.json": (3, 12),
        "sb08-sandgate-pharmacy.json": (3, 12),
        "sb09-willowmere-nursery.json": (3, 12),
        "sb10-kelvin-motors.json": (3, 12),
    }

    for name, (finding_count, trap_count) in expected_counts.items():
        payload = json.loads((manifest_directory / name).read_text(encoding="utf-8"))
        manifest = manifest_from_mapping(payload)

        assert len(manifest.findings) == finding_count
        assert len(manifest.traps) == trap_count
        assert manifest.gates.finding_recall == 0.9
        assert manifest.gates.critical_recall == 1
        assert manifest.gates.maximum_false_positive_traps == 0
        assert manifest.gates.maximum_duplicate_rate == 0
        assert manifest.gates.maximum_duration_seconds == 180
        assert manifest.expected_ratings is not None


def test_benchmark_fails_locator_gate_when_a_finding_has_no_source() -> None:
    manifest = BenchmarkManifest(
        name="Traceability",
        findings=(
            BenchmarkFinding(
                id="F-01",
                severity="Critical",
                concepts=(("owner", "ownership"),),
            ),
        ),
    )

    result = evaluate_benchmark(
        manifest,
        (
            _issue(
                "ISS-OWNER",
                "Delivery owner is missing",
                "No accountable ownership is assigned.",
                severity="Critical",
                evidence_refs=(),
            ),
        ),
    )

    assert result.finding_recall == 1
    assert result.locator_coverage == 0
    assert result.passed is False


def test_manifest_loader_and_duration_gate_are_machine_readable() -> None:
    manifest = manifest_from_mapping(
        {
            "name": "Release fixture",
            "findings": [
                {
                    "id": "F-01",
                    "severity": "Critical",
                    "concepts": [["cutover", "go-live"], ["freeze"]],
                }
            ],
            "traps": [],
            "gates": {"maximum_duration_seconds": 120},
        }
    )

    result = evaluate_benchmark(
        manifest,
        (
            _issue(
                "ISS-CUTOVER",
                "Cutover enters the freeze",
                "Go-live occurs during the freeze.",
                severity="Critical",
            ),
        ),
        duration_seconds=121,
    )

    assert manifest.gates.maximum_duration_seconds == 120
    assert result.duration_seconds == 121
    assert result.performance_passed is False
    assert result.passed is False


def test_expected_ratings_are_part_of_the_release_gate() -> None:
    manifest = manifest_from_mapping(
        {
            "name": "Rating fixture",
            "expected_ratings": {
                "clarity": "High",
                "alignment": "Very Low",
                "feasibility": "Very Low",
                "reliability": "High",
                "confidence": "Low",
            },
            "findings": [],
            "traps": [],
        }
    )

    result = evaluate_benchmark(
        manifest,
        (),
        ratings=("Moderate", "Low", "Very Low", "Moderate", "Very Low"),
    )

    assert result.rating_matches is False
    assert result.expected_ratings == (
        "High",
        "Very Low",
        "Very Low",
        "High",
        "Low",
    )
    assert result.passed is False
