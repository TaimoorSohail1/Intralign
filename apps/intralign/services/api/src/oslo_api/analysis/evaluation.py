from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from oslo_api.analysis.models import Issue

_TOKEN = re.compile(r"[a-z0-9%]+")
_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "in",
    "inconsistency",
    "inconsistent",
    "internal",
    "internally",
    "is",
    "it",
    "no",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "with",
}


@dataclass(frozen=True, slots=True)
class BenchmarkFinding:
    """One expected defect expressed as domain-neutral concept alternatives.

    Every inner tuple is one required concept. Any term inside that tuple may
    satisfy it, allowing fixtures to match honest paraphrases without matching
    against exact model wording.
    """

    id: str
    severity: str
    concepts: tuple[tuple[str, ...], ...]


@dataclass(frozen=True, slots=True)
class BenchmarkTrap:
    """A documented condition that must not be reported as a defect."""

    id: str
    concepts: tuple[tuple[str, ...], ...]


_TRAP_PROFILES = {
    "small_business": (
        BenchmarkTrap(id="T-01", concepts=(("steering committee", "project board"),)),
        BenchmarkTrap(id="T-02", concepts=(("RACI", "responsibility matrix"),)),
        BenchmarkTrap(id="T-03", concepts=(("risk register", "scored risks"),)),
        BenchmarkTrap(
            id="T-04",
            concepts=(("formal change control", "tolerance thresholds"),),
        ),
        BenchmarkTrap(id="T-05", concepts=(("contingency line", "contingency"),)),
        BenchmarkTrap(id="T-06", concepts=(("named supplier", "supplier name"),)),
        BenchmarkTrap(id="T-07", concepts=(("two pages", "document brevity"),)),
        BenchmarkTrap(
            id="T-08",
            concepts=(("owner is project manager", "owner project manager"),),
        ),
        BenchmarkTrap(
            id="T-09",
            concepts=(("benefits realisation plan", "benefits realization plan"),),
        ),
        BenchmarkTrap(
            id="T-10",
            concepts=(("testing strategy", "test stages"),),
        ),
        BenchmarkTrap(
            id="T-11",
            concepts=(("rounded costs", "cost breakdown"),),
        ),
        BenchmarkTrap(
            id="T-12",
            concepts=(
                ("15 user licences", "15 user licenses"),
                ("11 staff",),
            ),
        ),
    ),
}


@dataclass(frozen=True, slots=True)
class BenchmarkGates:
    finding_recall: float = 0.9
    critical_recall: float = 1.0
    maximum_false_positive_traps: int = 0
    locator_coverage: float = 1.0
    maximum_duplicate_rate: float = 0
    maximum_duration_seconds: float | None = 180
    minimum_issue_id_stability: float = 0.95
    require_rating_stability: bool = True


@dataclass(frozen=True, slots=True)
class BenchmarkManifest:
    name: str
    findings: tuple[BenchmarkFinding, ...]
    traps: tuple[BenchmarkTrap, ...] = ()
    expected_ratings: tuple[str, str, str, str, str] | None = None
    gates: BenchmarkGates = BenchmarkGates()


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    fixture: str
    findings_found: tuple[str, ...]
    findings_missed: tuple[str, ...]
    false_positive_traps: tuple[str, ...]
    duplicate_issue_ids: tuple[str, ...]
    finding_recall: float
    critical_recall: float
    locator_coverage: float
    duplicate_rate: float
    duration_seconds: float | None
    performance_passed: bool
    rating_matches: bool
    expected_ratings: tuple[str, str, str, str, str] | None
    actual_ratings: tuple[str, str, str, str, str] | None
    passed: bool


@dataclass(frozen=True, slots=True)
class BenchmarkObservation:
    issues: tuple[Issue, ...]
    ratings: tuple[str, str, str, str, str]
    duration_seconds: float | None = None


@dataclass(frozen=True, slots=True)
class BenchmarkSeriesResult:
    fixture: str
    runs: tuple[BenchmarkResult, ...]
    issue_id_stability: float
    rating_stability: bool
    passed: bool


def evaluate_benchmark(
    manifest: BenchmarkManifest,
    issues: tuple[Issue, ...],
    *,
    duration_seconds: float | None = None,
    ratings: tuple[str, str, str, str, str] | None = None,
) -> BenchmarkResult:
    """Score governed output without feeding fixture answers into production."""

    open_issues = tuple(issue for issue in issues if issue.status != "resolved")
    issue_tokens = {issue.id: _issue_tokens(issue) for issue in open_issues}
    assigned_issue_ids: set[str] = set()
    found: list[str] = []
    for finding in manifest.findings:
        candidates = [
            issue
            for issue in open_issues
            if issue.id not in assigned_issue_ids
            and _matches(issue_tokens[issue.id], finding.concepts)
        ]
        if not candidates:
            continue
        selected = max(
            candidates,
            key=lambda issue: (
                issue.severity == finding.severity,
                len(issue_tokens[issue.id]),
            ),
        )
        assigned_issue_ids.add(selected.id)
        found.append(finding.id)

    found_set = set(found)
    missed = tuple(
        finding.id for finding in manifest.findings if finding.id not in found_set
    )
    critical = tuple(
        finding
        for finding in manifest.findings
        if finding.severity.casefold() == "critical"
    )
    critical_found = sum(finding.id in found_set for finding in critical)
    false_positive_traps = tuple(
        trap.id
        for trap in manifest.traps
        if any(_matches(tokens, trap.concepts) for tokens in issue_tokens.values())
    )
    duplicate_issue_ids = _duplicate_issue_ids(open_issues, issue_tokens)
    finding_recall = _ratio(len(found), len(manifest.findings))
    critical_recall = _ratio(critical_found, len(critical))
    locator_coverage = _ratio(
        sum(bool(issue.evidence_refs) for issue in open_issues),
        len(open_issues),
    )
    duplicate_rate = _ratio(len(duplicate_issue_ids), len(open_issues))
    gates = manifest.gates
    performance_passed = (
        duration_seconds is None
        or gates.maximum_duration_seconds is None
        or duration_seconds <= gates.maximum_duration_seconds
    )
    rating_matches = (
        manifest.expected_ratings is None
        or ratings == manifest.expected_ratings
    )
    passed = (
        finding_recall >= gates.finding_recall
        and critical_recall >= gates.critical_recall
        and len(false_positive_traps) <= gates.maximum_false_positive_traps
        and locator_coverage >= gates.locator_coverage
        and duplicate_rate <= gates.maximum_duplicate_rate
        and performance_passed
        and rating_matches
    )
    return BenchmarkResult(
        fixture=manifest.name,
        findings_found=tuple(found),
        findings_missed=missed,
        false_positive_traps=false_positive_traps,
        duplicate_issue_ids=duplicate_issue_ids,
        finding_recall=finding_recall,
        critical_recall=critical_recall,
        locator_coverage=locator_coverage,
        duplicate_rate=duplicate_rate,
        duration_seconds=duration_seconds,
        performance_passed=performance_passed,
        rating_matches=rating_matches,
        expected_ratings=manifest.expected_ratings,
        actual_ratings=ratings,
        passed=passed,
    )


def evaluate_benchmark_series(
    manifest: BenchmarkManifest,
    observations: tuple[BenchmarkObservation, ...],
) -> BenchmarkSeriesResult:
    """Evaluate repeated identical reads as one governed release decision."""

    if not observations:
        raise ValueError("benchmark series needs at least one observation")
    runs = tuple(
        evaluate_benchmark(
            manifest,
            observation.issues,
            duration_seconds=observation.duration_seconds,
            ratings=observation.ratings,
        )
        for observation in observations
    )
    reference_ids = _open_issue_ids(observations[0].issues)
    stability_scores = tuple(
        _set_similarity(reference_ids, _open_issue_ids(observation.issues))
        for observation in observations[1:]
    )
    issue_id_stability = min(stability_scores, default=1.0)
    reference_ratings = observations[0].ratings
    rating_stability = all(
        observation.ratings == reference_ratings
        for observation in observations[1:]
    )
    gates = manifest.gates
    passed = (
        all(run.passed for run in runs)
        and issue_id_stability >= gates.minimum_issue_id_stability
        and (rating_stability or not gates.require_rating_stability)
    )
    return BenchmarkSeriesResult(
        fixture=manifest.name,
        runs=runs,
        issue_id_stability=issue_id_stability,
        rating_stability=rating_stability,
        passed=passed,
    )


def manifest_from_mapping(payload: Mapping[str, Any]) -> BenchmarkManifest:
    """Load the small, version-control-friendly JSON benchmark contract."""

    gates_payload = payload.get("gates", {})
    gates = BenchmarkGates(
        finding_recall=float(gates_payload.get("finding_recall", 0.9)),
        critical_recall=float(gates_payload.get("critical_recall", 1.0)),
        maximum_false_positive_traps=int(
            gates_payload.get("maximum_false_positive_traps", 0)
        ),
        locator_coverage=float(gates_payload.get("locator_coverage", 1.0)),
        maximum_duplicate_rate=float(
            gates_payload.get("maximum_duplicate_rate", 0)
        ),
        maximum_duration_seconds=(
            None
            if gates_payload.get("maximum_duration_seconds", 180) is None
            else float(gates_payload.get("maximum_duration_seconds", 180))
        ),
        minimum_issue_id_stability=float(
            gates_payload.get("minimum_issue_id_stability", 0.95)
        ),
        require_rating_stability=bool(
            gates_payload.get("require_rating_stability", True)
        ),
    )
    shared_traps = tuple(
        trap
        for profile in payload.get("trap_profiles", ())
        for trap in _trap_profile(str(profile))
    )
    return BenchmarkManifest(
        name=str(payload["name"]),
        findings=tuple(
            BenchmarkFinding(
                id=str(item["id"]),
                severity=str(item["severity"]),
                concepts=_concepts(item["concepts"]),
            )
            for item in payload.get("findings", ())
        ),
        traps=shared_traps + tuple(
            BenchmarkTrap(
                id=str(item["id"]),
                concepts=_concepts(item["concepts"]),
            )
            for item in payload.get("traps", ())
        ),
        expected_ratings=_ratings(payload.get("expected_ratings")),
        gates=gates,
    )


def _ratings(value: Any) -> tuple[str, str, str, str, str] | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise ValueError("expected_ratings must be an object")
    fields = ("clarity", "alignment", "feasibility", "reliability", "confidence")
    ratings = tuple(str(value[field]) for field in fields)
    return ratings  # type: ignore[return-value]


def _concepts(value: Any) -> tuple[tuple[str, ...], ...]:
    if not isinstance(value, list):
        raise ValueError("benchmark concepts must be an array of term arrays")
    concepts = tuple(
        tuple(str(term).strip() for term in alternatives if str(term).strip())
        for alternatives in value
        if isinstance(alternatives, list)
    )
    if not concepts or any(not alternatives for alternatives in concepts):
        raise ValueError("every benchmark concept needs at least one term")
    return concepts


def _trap_profile(name: str) -> tuple[BenchmarkTrap, ...]:
    try:
        return _TRAP_PROFILES[name]
    except KeyError as error:
        raise ValueError(f"unknown benchmark trap profile: {name}") from error


def _open_issue_ids(issues: tuple[Issue, ...]) -> set[str]:
    return {issue.id for issue in issues if issue.status != "resolved"}


def _set_similarity(left: set[str], right: set[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 1.0


def _matches(
    tokens: set[str],
    concepts: tuple[tuple[str, ...], ...],
) -> bool:
    return bool(concepts) and all(
        any(_tokens(term).issubset(tokens) for term in alternatives)
        for alternatives in concepts
    )


def _issue_tokens(issue: Issue) -> set[str]:
    # Evaluate the diagnosed weakness, not repeated remediation boilerplate.
    return _tokens(f"{issue.title} {issue.why}")


def _tokens(value: str) -> set[str]:
    return {
        _normalise_token(token)
        for token in _TOKEN.findall(value.casefold())
        if token not in _STOP_WORDS
    }


def _normalise_token(token: str) -> str:
    """Normalize basic grammatical variants without fuzzy semantic guessing."""

    if len(token) > 4 and token.endswith("ies"):
        return f"{token[:-3]}y"
    if len(token) > 4 and token.endswith("s") and not token.endswith("ss"):
        return token[:-1]
    return token


def _duplicate_issue_ids(
    issues: tuple[Issue, ...],
    tokens: dict[str, set[str]],
) -> tuple[str, ...]:
    duplicates: list[str] = []
    retained: list[Issue] = []
    for issue in issues:
        duplicate = any(
            candidate.artifact_type == issue.artifact_type
            and candidate.dimension.casefold() == issue.dimension.casefold()
            and _jaccard(tokens[candidate.id], tokens[issue.id]) >= 0.55
            for candidate in retained
        )
        if duplicate:
            duplicates.append(issue.id)
        else:
            retained.append(issue)
    return tuple(duplicates)


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def _ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 1.0
