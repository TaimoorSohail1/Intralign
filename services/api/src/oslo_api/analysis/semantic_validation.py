import calendar
import re
from dataclasses import dataclass, replace
from datetime import date

from oslo_api.analysis.models import (
    Artifact,
    ArtifactType,
    Assessment,
    EvidenceFragment,
    Issue,
)

_MONTHS = {
    name.casefold(): number
    for number in range(1, 13)
    for name in (calendar.month_name[number], calendar.month_abbr[number])
}
_MONTH_PATTERN = "|".join(sorted((re.escape(name) for name in _MONTHS), key=len, reverse=True))
_DATE_PATTERN = rf"\b([0-3]?\d)\s+({_MONTH_PATTERN})\s+(\d{{4}})\b"
_DATE_RE = re.compile(_DATE_PATTERN, re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class _View:
    fragment: EvidenceFragment
    raw: str
    flat: str


@dataclass(frozen=True, slots=True)
class _Window:
    start: date
    finish: date
    reference: str


def normalize_artifact_provenance(
    artifacts: tuple[Artifact, ...],
) -> tuple[Artifact, ...]:
    """Evidence-backed rows are grounded facts, not model inferences."""

    normalized: list[Artifact] = []
    for artifact in artifacts:
        sections = []
        for section in artifact.sections:
            states = list(section.row_states)
            if section.rows and len(states) < len(section.rows):
                states.extend("unknown" for _ in range(len(section.rows) - len(states)))
            for index, evidence_refs in enumerate(section.row_evidence_refs):
                if index >= len(states) or not evidence_refs:
                    continue
                if states[index] != "conflicting":
                    states[index] = "confirmed"
            sections.append(replace(section, row_states=tuple(states)))
        normalized.append(replace(artifact, sections=tuple(sections)))
    return tuple(normalized)


def audit_project_evidence(
    evidence: tuple[EvidenceFragment, ...],
) -> tuple[Issue, ...]:
    """Run deterministic, evidence-backed project-plan checks.

    These checks intentionally cover relationships that retrieval-only model calls
    routinely miss: cross-page contradictions, temporal violations, arithmetic
    reconciliation, and required registers implied by the plan itself.
    """

    views = tuple(
        _View(
            fragment=item,
            raw=item.content.replace("\u00a0", " "),
            flat=re.sub(r"\s+", " ", item.content.replace("\u00a0", " ")).strip(),
        )
        for item in evidence
        if item.content.strip()
    )
    checks = (
        _freeze_conflict(views),
        _freeze_violation(views),
        _availability_conflict(views),
        _threshold_gap(views),
        *_test_entry_violations(views),
        _measurement_window(views),
        _effort_split(views),
        _missing_gate_milestone(views),
        _funding_conflict(views),
        _milestone_order(views),
        _uncited_benchmark(views),
        _missing_dependency_register(views),
        _missing_procurement_approach(views),
        _missing_contamination_control_strategy(views),
        _missing_cleaning_validation(views),
        _missing_vendor_qualification(views),
        _missing_supply_fallback(views),
        _undeclared_stage_overlap(views),
        _short_operational_warranty(views),
    )
    return tuple(issue for issue in checks if issue is not None)


def merge_semantic_issues(
    model_issues: tuple[Issue, ...],
    deterministic_issues: tuple[Issue, ...],
) -> tuple[Issue, ...]:
    """Prefer deterministic findings and suppress obvious model duplicates."""

    merged = list(deterministic_issues)
    for model_issue in model_issues:
        if any(_issues_overlap(model_issue, existing) for existing in merged):
            continue
        merged.append(model_issue)
    return tuple(merged)


def apply_evidence_rubric(
    assessment: Assessment,
    evidence: tuple[EvidenceFragment, ...],
) -> Assessment:
    """Stabilize bands when the source is demonstrably dense and traceable.

    The model still reads qualitative plans. For highly structured plans, however,
    objective evidence density is a more stable measure of clarity and alignment
    than model wording or project complexity.
    """

    text = " ".join(item.content for item in evidence)
    date_count = len(_dates(text))
    threshold_count = len(re.findall(r"(?:≤|>=|<=|≥|>|<)\s*[\d.]+|[\d.]+\s*%", text))
    ownership_count = len(
        re.findall(
            r"\b(?:owner|accepted by|sign-off|accountable|decision authority)\b",
            text,
            re.I,
        )
    )
    identifier_families = {
        family
        for family in ("O", "D", "K", "M", "P", "R", "T", "N")
        if re.search(rf"\b{family}-?\d+\b", text, re.I)
    }
    traceable_plan = (
        {"O", "D", "K"}.issubset(identifier_families)
        and re.search(r"\bscope\b", text, re.I)
        and re.search(r"\brequirements?\b", text, re.I)
        and re.search(r"\b(?:acceptance criteria|success measures?|benefits?)\b", text, re.I)
    )
    dense_plan = (
        date_count >= 8
        and threshold_count >= 4
        and ownership_count >= 6
        and len(identifier_families) >= 5
    )
    references = {item.reference for item in evidence}
    traceable_issues = all(issue.evidence_refs for issue in assessment.issues)
    reliability = "High" if len(references) >= 5 and traceable_issues else assessment.reliability
    clarity = "High" if dense_plan else assessment.clarity
    alignment = "High" if traceable_plan else assessment.alignment
    feasibility_findings = [
        issue
        for issue in assessment.issues
        if issue.dimension == "Feasibility"
        and issue.status != "resolved"
        and issue.severity in {"Critical", "Moderate"}
    ]
    feasibility = (
        "Moderate"
        if dense_plan and traceable_plan and feasibility_findings
        else assessment.feasibility
    )
    confidence_band = (
        "High"
        if clarity == "High"
        and alignment == "High"
        and feasibility in {"Moderate", "High"}
        and reliability == "High"
        else assessment.confidence_band
    )
    stable_index = {
        "Very Low": 18,
        "Low": 38,
        "Moderate": 62,
        "High": 82,
    }.get(confidence_band, assessment.confidence_index)
    return replace(
        assessment,
        confidence_index=stable_index,
        confidence_band=confidence_band,
        reliability=reliability,
        clarity=clarity,
        alignment=alignment,
        feasibility=feasibility,
    )


def _freeze_conflict(views: tuple[_View, ...]) -> Issue | None:
    windows = _freeze_windows(views)
    for index, left in enumerate(windows):
        for right in windows[index + 1 :]:
            overlaps = left.start <= right.finish and right.start <= left.finish
            if overlaps and (left.start, left.finish) != (right.start, right.finish):
                return _issue(
                    issue_id="DET-SCHEDULE-FREEZE-CONFLICT",
                    artifact_type=ArtifactType.SCHEDULE,
                    dimension="Alignment",
                    severity="Critical",
                    title="Trading freeze dates contradict",
                    why=(
                        "The plan defines overlapping production-freeze windows with "
                        "different start or finish dates, so the governing constraint is "
                        "not unambiguous."
                    ),
                    recommendation=(
                        "Confirm one authoritative freeze window and align the constraints, "
                        "phase plan, milestones, and risk responses to it."
                    ),
                    references=(left.reference, right.reference),
                    clarification="Which production-freeze dates are authoritative?",
                )
    return None


def _freeze_violation(views: tuple[_View, ...]) -> Issue | None:
    windows = _freeze_windows(views)
    for view in views:
        for match in re.finditer(
            rf"\b(P\d+)\s+(.{{1,180}}?)\s+({_DATE_PATTERN})\s+({_DATE_PATTERN})"
            r"\s+\d+\s+G\d+\b",
            view.flat,
            re.IGNORECASE,
        ):
            matched_dates = _dates(match.group(3))
            start = matched_dates[0] if matched_dates else None
            if start is None:
                continue
            for window in windows:
                if window.start <= start <= window.finish:
                    return _issue(
                        issue_id="DET-SCHEDULE-FREEZE-VIOLATION",
                        artifact_type=ArtifactType.SCHEDULE,
                        dimension="Feasibility",
                        severity="Critical",
                        title="A baseline phase starts inside a declared production freeze",
                        why=(
                            f"{match.group(1)} starts on {start:%d %b %Y}, inside a "
                            "hard production-freeze constraint."
                        ),
                        recommendation=(
                            "Move the phase outside the freeze or record an approved exception "
                            "with owner, scope, and operational safeguards."
                        ),
                        references=(window.reference, view.fragment.reference),
                        clarification=(
                            "Is the phase date wrong, the freeze date wrong, or is there an "
                            "approved exception?"
                        ),
                    )
    return None


def _availability_conflict(views: tuple[_View, ...]) -> Issue | None:
    candidates: list[tuple[date, str]] = []
    for view in views:
        for match in re.finditer(
            r"(?:partner delivery team|delivery team of \d+ named consultants|"
            r"\d+ named consultants)",
            view.flat,
            re.IGNORECASE,
        ):
            nearby = view.flat[max(0, match.start() - 100) : match.end() + 180]
            parsed = _dates(nearby)
            if parsed:
                candidates.append((parsed[-1], view.fragment.reference))
    unique_dates = sorted({candidate[0] for candidate in candidates})
    if len(unique_dates) < 2 or (unique_dates[-1] - unique_dates[0]).days < 14:
        return None
    references = tuple(reference for _, reference in candidates)
    return _issue(
        issue_id="DET-RESOURCES-AVAILABILITY-CONFLICT",
        artifact_type=ArtifactType.RESOURCES,
        dimension="Alignment",
        severity="Critical",
        title="Partner mobilisation dates contradict",
        why=(
            "The same named partner team is required from "
            f"{unique_dates[0]:%d %b %Y} but is shown as available from "
            f"{unique_dates[-1]:%d %b %Y}."
        ),
        recommendation=(
            "Confirm the contractual mobilisation date and name the capacity covering any "
            "work before that date."
        ),
        references=references,
        clarification="Which partner-team availability date is authoritative?",
    )


def _threshold_gap(views: tuple[_View, ...]) -> Issue | None:
    acceptance: tuple[float, str] | None = None
    rollback: tuple[float, str] | None = None
    for view in views:
        if not re.search(r"(?:stock(?: on hand)?\s*[-—]?\s*)?value variance", view.flat, re.I):
            continue
        accepted = re.search(r"(?:≤|<=|no more than)\s*([\d.]+)\s*%", view.flat, re.I)
        rolled_back = re.search(
            r"rollback.{0,180}?(?:exceeds|above|>)\s*([\d.]+)\s*%",
            view.flat,
            re.I,
        )
        if accepted:
            acceptance = (float(accepted.group(1)), view.fragment.reference)
        if rolled_back:
            rollback = (float(rolled_back.group(1)), view.fragment.reference)
    if acceptance is None or rollback is None or acceptance[0] >= rollback[0]:
        return None
    return _issue(
        issue_id="DET-REQUIREMENTS-THRESHOLD-GAP",
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Clarity",
        severity="Critical",
        title="Rollback action is undefined between acceptance thresholds",
        why=(
            f"Acceptance requires no more than {acceptance[0]:g}% variance, while "
            f"rollback begins only above {rollback[0]:g}%. The plan defines no action "
            "for results between those thresholds."
        ),
        recommendation=(
            "Define the action, authority, containment period, and proceed/rollback decision "
            "for the uncovered threshold range."
        ),
        references=(acceptance[1], rollback[1]),
        clarification="What action applies between the acceptance and rollback thresholds?",
    )


def _test_entry_violations(views: tuple[_View, ...]) -> tuple[Issue | None, ...]:
    for view in views:
        lower = view.flat.casefold()
        required = (
            "system integration test",
            "performance test",
            "user acceptance test",
            "operational readiness test",
        )
        if not all(name in lower for name in required):
            continue
        blocks = _stage_blocks(view)
        sit = blocks.get("system integration test")
        performance = blocks.get("performance test")
        uat = blocks.get("user acceptance test")
        readiness = blocks.get("operational readiness test")
        performance_issue = None
        readiness_issue = None
        if (
            sit
            and performance
            and "sit pass" in performance[0].casefold()
            and performance[1].start < sit[1].finish
        ):
            performance_issue = _issue(
                issue_id="DET-SCHEDULE-ENTRY-CRITERION-PERFORMANCE",
                artifact_type=ArtifactType.SCHEDULE,
                dimension="Feasibility",
                severity="Moderate",
                title="Performance testing starts before its entry criterion can be met",
                why=(
                    "Performance testing requires a SIT pass but begins before the "
                    "scheduled SIT window has finished."
                ),
                recommendation=(
                    "Move the performance-test start or define an earlier measurable SIT "
                    "checkpoint that satisfies the entry criterion."
                ),
                references=(view.fragment.reference,),
                clarification="Which dated SIT checkpoint authorizes performance testing?",
            )
        if (
            uat
            and readiness
            and "uat exit" in readiness[0].casefold()
            and readiness[1].start < uat[1].finish
        ):
            readiness_issue = _issue(
                issue_id="DET-SCHEDULE-ENTRY-CRITERION-ORT",
                artifact_type=ArtifactType.SCHEDULE,
                dimension="Feasibility",
                severity="Moderate",
                title="Operational readiness testing starts before UAT exit",
                why=(
                    "Operational readiness requires UAT exit but begins before the "
                    "scheduled UAT window has finished."
                ),
                recommendation=(
                    "Move readiness testing or define an approved partial-exit criterion "
                    "with accountable sign-off."
                ),
                references=(view.fragment.reference,),
                clarification="How can UAT exit be evidenced before readiness testing starts?",
            )
        return performance_issue, readiness_issue
    return None, None


def _measurement_window(views: tuple[_View, ...]) -> Issue | None:
    months: int | None = None
    measurement_ref: str | None = None
    for view in views:
        match = re.search(
            r"until\s+(\d+)\s+months?\s+after\s+national\s+go-live",
            view.flat,
            re.I,
        )
        if match:
            months = int(match.group(1))
            measurement_ref = view.fragment.reference
            break
    if months is None or measurement_ref is None:
        return None
    go_live: tuple[date, str] | None = None
    for view in views:
        match = re.search(
            rf"national\s+go-live.{{0,140}}?({_DATE_PATTERN})",
            view.flat,
            re.I,
        )
        if match:
            parsed = _parse_date_groups(match.groups()[-3:])
            if parsed:
                go_live = (parsed, view.fragment.reference)
                break
    if go_live is None:
        return None
    measurement_end = _add_months(go_live[0], months)
    late_measures: list[tuple[str, date, str]] = []
    for view in views:
        for match in re.finditer(
            rf"\b(K-\d+)\b(.{{0,260}}?)({_DATE_PATTERN})",
            view.flat,
            re.I,
        ):
            parsed = _parse_date_groups(match.groups()[-3:])
            if parsed and parsed > measurement_end:
                late_measures.append((match.group(1).upper(), parsed, view.fragment.reference))
    if not late_measures:
        return None
    measure, target_date, target_ref = late_measures[0]
    return _issue(
        issue_id="DET-SCHEDULE-MEASUREMENT-WINDOW",
        artifact_type=ArtifactType.SCHEDULE,
        dimension="Alignment",
        severity="Moderate",
        title="A success measure falls outside the measurement period",
        why=(
            f"{measure} is due {target_date:%d %b %Y}, after the stated measurement "
            f"period ends on {measurement_end:%d %b %Y}."
        ),
        recommendation=(
            "Extend the measurement period or move the target into the approved benefits "
            "measurement window."
        ),
        references=(measurement_ref, go_live[1], target_ref),
        clarification="Should the measurement period or the success-measure date change?",
    )


def _effort_split(views: tuple[_View, ...]) -> Issue | None:
    declared: tuple[int, str] | None = None
    for view in views:
        match = re.search(r"comprising\s+([\d,]+)\s+partner days", view.flat, re.I)
        if match:
            declared = (int(match.group(1).replace(",", "")), view.fragment.reference)
            break
    if declared is None:
        return None
    partner_tokens = {
        match.group(1).casefold()
        for view in views
        for match in re.finditer(
            r"\b([A-Z][A-Za-z]+)\s+(?:Supply Systems|Consulting|Partners?)\b",
            view.raw,
        )
    }
    if not partner_tokens:
        return None
    attributed = 0
    row_references: list[str] = []
    for view in views:
        for match in re.finditer(
            r"(?m)^(\d+\.\d+)\s*\n(.+?)\n([^\n]+)\n(P[\dP0-9–-]+)\n(\d+)\s*$",
            view.raw,
        ):
            owner = match.group(3).casefold()
            if any(token in owner for token in partner_tokens):
                attributed += int(match.group(5))
                row_references.append(view.fragment.reference)
    if attributed == declared[0]:
        return None
    return _issue(
        issue_id="DET-WORK-BREAKDOWN-EFFORT-SPLIT",
        artifact_type=ArtifactType.WORK_BREAKDOWN,
        dimension="Clarity",
        severity="Moderate",
        title="The declared partner effort split cannot be reconstructed",
        why=(
            f"The plan declares {declared[0]:,} partner days, but the WBS owner rows "
            f"explicitly attributable to the named partner total {attributed:,} days."
        ),
        recommendation=(
            "Add an internal/partner allocation to every work package or correct the "
            "declared effort split."
        ),
        references=(declared[1], *row_references),
        clarification="Which WBS rows make up the declared partner-day total?",
    )


def _missing_gate_milestone(views: tuple[_View, ...]) -> Issue | None:
    phase_gates: set[str] = set()
    phase_refs: list[str] = []
    milestone_gates: set[str] = set()
    milestone_refs: list[str] = []
    for view in views:
        if re.search(r"delivery phases", view.flat, re.I):
            phase_gates.update(match.upper() for match in re.findall(r"\bG\d+\b", view.flat, re.I))
            phase_refs.append(view.fragment.reference)
        if re.search(r"schedule and milestones", view.flat, re.I):
            milestone_gates.update(
                match.upper() for match in re.findall(r"\bGate\s+(G\d+)\b", view.flat, re.I)
            )
            milestone_refs.append(view.fragment.reference)
    missing = sorted(phase_gates - milestone_gates)
    if not missing:
        return None
    return _issue(
        issue_id="DET-SCHEDULE-MISSING-GATE-MILESTONE",
        artifact_type=ArtifactType.SCHEDULE,
        dimension="Clarity",
        severity="Moderate",
        title="A referenced delivery gate has no milestone",
        why=(
            f"{', '.join(missing)} appears in the delivery phases but has no corresponding "
            "entry in the milestone baseline."
        ),
        recommendation=(
            "Add the missing gate milestone with date, owner, predecessor, and decision criteria."
        ),
        references=(*phase_refs, *milestone_refs),
        clarification="What is the baseline milestone for the missing delivery gate?",
    )


def _funding_conflict(views: tuple[_View, ...]) -> Issue | None:
    baseline_ref = next(
        (
            view.fragment.reference
            for view in views
            if re.search(r"(?:budget|cost baseline)", view.flat, re.I)
            and re.search(r"hardware.{0,180}?\b[\d,]{4,}\b", view.flat, re.I)
        ),
        None,
    )
    contingency_ref = next(
        (
            view.fragment.reference
            for view in views
            if re.search(r"hardware.{0,180}?against contingency", view.flat, re.I)
        ),
        None,
    )
    if baseline_ref is None or contingency_ref is None:
        return None
    return _issue(
        issue_id="DET-RESOURCES-FUNDING-CONFLICT",
        artifact_type=ArtifactType.RESOURCES,
        dimension="Alignment",
        severity="Moderate",
        title="Hardware funding source contradicts the approved baseline",
        why=(
            "Hardware is included as a base-cost line but another control states that the "
            "order is funded against contingency."
        ),
        recommendation=(
            "Confirm whether hardware is base-funded or contingency-funded and align the "
            "budget, assumption, risk response, and approval route."
        ),
        references=(baseline_ref, contingency_ref),
        clarification="Is the hardware order funded from base cost or contingency?",
    )


def _milestone_order(views: tuple[_View, ...]) -> Issue | None:
    milestones: list[tuple[int, date, str]] = []
    for view in views:
        if not re.search(r"schedule and milestones", view.flat, re.I):
            continue
        lines = [line.strip() for line in view.raw.splitlines() if line.strip()]
        for index, line in enumerate(lines):
            identifier = re.fullmatch(r"M(\d+)", line, re.I)
            if identifier is None or index + 1 >= len(lines):
                continue
            if lines[index + 1].casefold() in {"yes", "no"}:
                continue
            for candidate in lines[index + 1 : index + 4]:
                parsed_dates = _dates(candidate)
                if parsed_dates:
                    milestones.append(
                        (
                            int(identifier.group(1)),
                            parsed_dates[0],
                            view.fragment.reference,
                        )
                    )
                    break
    milestones.sort(key=lambda item: item[0])
    for left, right in zip(milestones, milestones[1:], strict=False):
        if right[1] < left[1]:
            return _issue(
                issue_id="DET-SCHEDULE-MILESTONE-ORDER",
                artifact_type=ArtifactType.SCHEDULE,
                dimension="Clarity",
                severity="Warning",
                title="Milestone identifiers are not chronological",
                why=(
                    f"M{left[0]} is dated {left[1]:%d %b %Y}, after M{right[0]} on "
                    f"{right[1]:%d %b %Y}."
                ),
                recommendation=(
                    "Renumber the milestones or explain why identifier order intentionally "
                    "differs from baseline chronology."
                ),
                references=(left[2], right[2]),
                clarification="Should the milestone IDs or dates be corrected?",
            )
    return None


def _uncited_benchmark(views: tuple[_View, ...]) -> Issue | None:
    references = tuple(
        view.fragment.reference
        for view in views
        if re.search(r"\b(?:sector benchmark|competitor norm)\b", view.flat, re.I)
    )
    if not references:
        return None
    return _issue(
        issue_id="DET-CONTEXT-UNCITED-BENCHMARK",
        artifact_type=ArtifactType.CONTEXT,
        dimension="Clarity",
        severity="Warning",
        title="External benchmarks are not individually sourced",
        why=(
            "The plan uses a sector benchmark or competitor norm without identifying the "
            "external source, date, or comparison basis."
        ),
        recommendation=(
            "Cite the benchmark source and period, or label the comparison as an unverified "
            "planning assumption."
        ),
        references=references,
        clarification="What source supports the external benchmark or competitor norm?",
    )


def _missing_dependency_register(views: tuple[_View, ...]) -> Issue | None:
    implied_refs = tuple(
        view.fragment.reference
        for view in views
        if re.search(
            r"\b(?:integration to|dependent on|external dependencies?)\b",
            view.flat,
            re.I,
        )
    )
    has_register = any(
        re.search(
            r"(?im)^\s*(?:\d+(?:\.\d+)?\s+)?(?:external\s+)?"
            r"dependenc(?:y|ies)(?:\s+register)?\s*$",
            view.raw,
        )
        for view in views
    )
    if not implied_refs or has_register:
        return None
    return _issue(
        issue_id="DET-CONTEXT-MISSING-DEPENDENCY-REGISTER",
        artifact_type=ArtifactType.CONTEXT,
        dimension="Clarity",
        severity="Warning",
        title="External dependencies have no governed register",
        why=(
            "The scope relies on external systems or services, but no dependency register "
            "defines owners, dates, conditions, or escalation."
        ),
        recommendation=(
            "Create a dependency register covering each external service, accountable owner, "
            "required date, current status, and fallback."
        ),
        references=implied_refs,
        clarification="Where are the external dependencies, owners, and required dates governed?",
    )


def _missing_procurement_approach(views: tuple[_View, ...]) -> Issue | None:
    work_refs = tuple(
        view.fragment.reference
        for view in views
        if re.search(
            r"(?:vendor selection|procurement).{0,120}?"
            r"(?:contracting|commercial management|owner)",
            view.flat,
            re.I,
        )
    )
    has_approach = any(
        re.search(
            r"(?im)^\s*(?:\d+(?:\.\d+)?\s+)?procurement\s+"
            r"(?:approach|strategy|plan)\s*$",
            view.raw,
        )
        for view in views
    )
    raci_refs = tuple(
        view.fragment.reference
        for view in views
        if re.search(r"responsibility assignment|raci", view.flat, re.I)
    )
    procurement_in_raci = any(
        re.search(
            r"(?:responsibility assignment|raci).{0,300}\bprocurement\b",
            view.flat,
            re.I,
        )
        for view in views
    )
    if not work_refs or has_approach or procurement_in_raci:
        return None
    return _issue(
        issue_id="DET-RESOURCES-MISSING-PROCUREMENT-APPROACH",
        artifact_type=ArtifactType.RESOURCES,
        dimension="Clarity",
        severity="Warning",
        title="Procurement work has no defined approach or RACI role",
        why=(
            "Procurement owns vendor work, but the plan contains no procurement approach "
            "and Procurement is absent from the responsibility assignment."
        ),
        recommendation=(
            "Add the procurement route, commercial milestones, decision rights, approvals, "
            "and Procurement responsibilities."
        ),
        references=(*work_refs, *raci_refs),
        clarification="What procurement approach and accountable role govern vendor contracting?",
    )


def _missing_contamination_control_strategy(
    views: tuple[_View, ...],
) -> Issue | None:
    trigger_refs = tuple(
        view.fragment.reference
        for view in views
        if re.search(r"\b(?:sterile|aseptic)\b", view.flat, re.I)
        and re.search(r"\b(?:EU\s+GMP\s+)?Annex\s+1\b", view.flat, re.I)
    )
    has_control = any(
        re.search(r"\b(?:contamination control strategy|CCS)\b", view.flat, re.I)
        for view in views
    )
    if not trigger_refs or has_control:
        return None
    return _issue(
        issue_id="DET-REQUIREMENTS-MISSING-CONTAMINATION-CONTROL",
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Clarity",
        severity="Moderate",
        title="The regulated sterile design has no contamination control strategy",
        why=(
            "The plan invokes Annex 1 for sterile or aseptic operations but does not "
            "identify the required contamination control strategy or its approval."
        ),
        recommendation=(
            "Add the contamination control strategy deliverable, accountable owner, "
            "approval gate, and traceability to qualification and operations."
        ),
        references=trigger_refs,
        clarification="Where is the contamination control strategy governed and approved?",
    )


def _missing_cleaning_validation(views: tuple[_View, ...]) -> Issue | None:
    regulated = any(
        re.search(r"\b(?:sterile|aseptic|pharmaceutical|GMP)\b", view.flat, re.I)
        for view in views
    )
    shared_refs = tuple(
        view.fragment.reference
        for view in views
        if re.search(
            r"\bshared\b.{0,100}\b(?:equipment|asset|lyophili[sz]er|packaging|surface)\b"
            r"|\b(?:equipment|asset|lyophili[sz]er|packaging|surface)\b.{0,100}\bshared\b",
            view.flat,
            re.I,
        )
    )
    has_validation = any(
        re.search(r"\bcleaning validation\b", view.flat, re.I) for view in views
    )
    if not regulated or not shared_refs or has_validation:
        return None
    return _issue(
        issue_id="DET-REQUIREMENTS-MISSING-CLEANING-VALIDATION",
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Clarity",
        severity="Moderate",
        title="Shared regulated equipment has no cleaning validation plan",
        why=(
            "The plan relies on shared equipment in a regulated process but defines no "
            "cleaning-validation scope, acceptance criteria, owner, or release gate."
        ),
        recommendation=(
            "Add cleaning-validation protocols, limits, sampling, ownership, and a "
            "dated release criterion for every shared product-contact asset."
        ),
        references=shared_refs,
        clarification="How will cleaning validation release the shared assets for use?",
    )


def _missing_vendor_qualification(views: tuple[_View, ...]) -> Issue | None:
    trigger_refs = tuple(
        view.fragment.reference
        for view in views
        if re.search(r"\bsingle[- ]source\b", view.flat, re.I)
        and re.search(r"\b(?:vendor|supplier|equipment package|critical path)\b", view.flat, re.I)
    )
    has_qualification = any(
        re.search(
            r"\b(?:vendor qualification|supplier qualification|supplier audit|vendor audit)\b",
            view.flat,
            re.I,
        )
        for view in views
    )
    if not trigger_refs or has_qualification:
        return None
    return _issue(
        issue_id="DET-RESOURCES-MISSING-VENDOR-QUALIFICATION",
        artifact_type=ArtifactType.RESOURCES,
        dimension="Clarity",
        severity="Moderate",
        title="A single-source critical supplier has no qualification plan",
        why=(
            "The plan depends on a single-source supplier or vendor on the critical path "
            "but defines no qualification or audit control."
        ),
        recommendation=(
            "Add supplier due diligence, qualification evidence, acceptance authority, "
            "review date, and escalation criteria."
        ),
        references=trigger_refs,
        clarification="What evidence qualifies the critical single-source supplier?",
    )


def _missing_supply_fallback(views: tuple[_View, ...]) -> Issue | None:
    commitment_refs = tuple(
        view.fragment.reference
        for view in views
        if re.search(r"\bsigned\b.{0,80}\b(?:customer|supply)\s+agreements?\b", view.flat, re.I)
        and re.search(r"\b(?:depend|dependent|committed|delivery|production)\b", view.flat, re.I)
    )
    has_fallback = any(
        re.search(
            r"\b(?:fallback supply|alternate supply|alternative supply|"
            r"contract manufacturer|business continuity supply)\b",
            view.flat,
            re.I,
        )
        for view in views
    )
    if not commitment_refs or has_fallback:
        return None
    return _issue(
        issue_id="DET-SCOPE-MISSING-SUPPLY-FALLBACK",
        artifact_type=ArtifactType.SCOPE,
        dimension="Clarity",
        severity="Warning",
        title="Committed customer supply has no fallback route",
        why=(
            "Signed supply commitments depend on the project date, but the plan does "
            "not define an alternate supply route if qualification or launch fails."
        ),
        recommendation=(
            "Define the fallback source, activation threshold, accountable decision-maker, "
            "capacity, regulatory status, and customer communication."
        ),
        references=commitment_refs,
        clarification="What supply route protects signed commitments if the project misses launch?",
    )


def _undeclared_stage_overlap(views: tuple[_View, ...]) -> Issue | None:
    declared = any(
        re.search(
            r"\b(?:approved\s+)?(?:fast[- ]tracking|overlap)\b.{0,120}"
            r"\b(?:risk|approved|governed)\b",
            view.flat,
            re.I,
        )
        for view in views
    )
    if declared:
        return None
    for view in views:
        if not re.search(r"\b(?:schedule|stage|phase|qualification)\b", view.flat, re.I):
            continue
        markers = list(re.finditer(r"\bS(\d+)\b", view.flat, re.I))
        windows: list[tuple[str, _Window]] = []
        for index, marker in enumerate(markers):
            finish = markers[index + 1].start() if index + 1 < len(markers) else len(view.flat)
            block = view.flat[marker.start() : finish]
            dates = _dates(block)
            if len(dates) >= 2 and dates[1] >= dates[0]:
                windows.append(
                    (
                        f"S{marker.group(1)}",
                        _Window(dates[0], dates[1], view.fragment.reference),
                    )
                )
        for (left_id, left), (right_id, right) in zip(windows, windows[1:], strict=False):
            if right.start >= left.finish:
                continue
            return _issue(
                issue_id="DET-SCHEDULE-UNDECLARED-STAGE-OVERLAP",
                artifact_type=ArtifactType.SCHEDULE,
                dimension="Alignment",
                severity="Moderate",
                title="Consecutive delivery stages overlap without a governed exception",
                why=(
                    f"{left_id} runs to {left.finish:%d %b %Y}, while {right_id} "
                    f"starts on {right.start:%d %b %Y}; the plan does not declare "
                    "fast-tracking or govern the overlap as a risk."
                ),
                recommendation=(
                    "Remove the overlap or record its approval, dependencies, shared-resource "
                    "constraints, accountable owner, and risk response."
                ),
                references=(left.reference, right.reference),
                clarification="Is the stage overlap intentional and, if so, where is it governed?",
            )
    return None


def _short_operational_warranty(views: tuple[_View, ...]) -> Issue | None:
    warranty: tuple[int, str] | None = None
    for view in views:
        match = re.search(
            r"\bwarranty\b.{0,100}?\b(\d{1,3})\s+months?\s+from\s+delivery\b",
            view.flat,
            re.I,
        )
        if match:
            warranty = (int(match.group(1)), view.fragment.reference)
            break
    if warranty is None:
        return None

    delivery: tuple[date, str] | None = None
    production: tuple[date, str] | None = None
    for view in views:
        for match in re.finditer(r"\bdelivery\b", view.flat, re.I):
            nearby = view.flat[match.end() : match.end() + 140]
            dates = _dates(nearby)
            if dates:
                delivery = (dates[0], view.fragment.reference)
                break
        for match in re.finditer(r"\bcommercial production\b", view.flat, re.I):
            nearby = view.flat[match.end() : match.end() + 120]
            dates = _dates(nearby)
            if dates:
                production = (dates[0], view.fragment.reference)
                break
    if delivery is None or production is None:
        return None
    warranty_end = _add_months(delivery[0], warranty[0])
    operational_cover_days = (warranty_end - production[0]).days
    if operational_cover_days >= 183:
        return None
    return _issue(
        issue_id="DET-RESOURCES-SHORT-WARRANTY-COVER",
        artifact_type=ArtifactType.RESOURCES,
        dimension="Clarity",
        severity="Moderate",
        title="Most equipment warranty cover expires before operations can prove performance",
        why=(
            f"The warranty ends around {warranty_end:%d %b %Y}, leaving only "
            f"{max(0, operational_cover_days)} days after commercial production begins."
        ),
        recommendation=(
            "Extend warranty from acceptance or operational handover, or add funded support "
            "covering commissioning, qualification, ramp-up, and latent defects."
        ),
        references=(warranty[1], delivery[1], production[1]),
        clarification=(
            "What warranty or support protects the equipment through operational ramp-up?"
        ),
    )


def _freeze_windows(views: tuple[_View, ...]) -> tuple[_Window, ...]:
    windows = []
    for view in views:
        for match in re.finditer(
            rf"({_DATE_PATTERN})\s+(?:and|to|[-–])\s+({_DATE_PATTERN})",
            view.flat,
            re.I,
        ):
            context = view.flat[max(0, match.start() - 120) : match.end() + 120]
            if "freeze" not in context.casefold():
                continue
            groups = match.groups()
            start = _parse_date_groups(groups[1:4])
            finish = _parse_date_groups(groups[5:8])
            if start and finish and finish >= start:
                windows.append(_Window(start, finish, view.fragment.reference))
    return tuple(windows)


def _stage_blocks(view: _View) -> dict[str, tuple[str, _Window]]:
    names = (
        "system integration test",
        "performance test",
        "user acceptance test",
        "operational readiness test",
    )
    lower = view.flat.casefold()
    positions = sorted((lower.index(name), name) for name in names)
    result = {}
    for index, (start, name) in enumerate(positions):
        finish = positions[index + 1][0] if index + 1 < len(positions) else len(view.flat)
        block = view.flat[start:finish]
        window = _compact_date_range(block, view.fragment.reference)
        if window:
            result[name] = (block, window)
    return result


def _compact_date_range(text: str, reference: str) -> _Window | None:
    split_month = re.search(
        rf"\b([0-3]?\d)\s+({_MONTH_PATTERN})\s*[-–]\s*"
        rf"([0-3]?\d)\s+({_MONTH_PATTERN})\s+(\d{{4}})\b",
        text,
        re.I,
    )
    if split_month:
        left = _parse_date_groups(
            (split_month.group(1), split_month.group(2), split_month.group(5))
        )
        right = _parse_date_groups(split_month.groups()[2:5])
        return _Window(left, right, reference) if left and right else None
    same_month = re.search(
        rf"\b([0-3]?\d)\s*[-–]\s*([0-3]?\d)\s+"
        rf"({_MONTH_PATTERN})\s+(\d{{4}})\b",
        text,
        re.I,
    )
    if same_month:
        left = _parse_date_groups((same_month.group(1), same_month.group(3), same_month.group(4)))
        right = _parse_date_groups((same_month.group(2), same_month.group(3), same_month.group(4)))
        return _Window(left, right, reference) if left and right else None
    return None


def _dates(text: str) -> tuple[date, ...]:
    parsed = []
    for match in _DATE_RE.finditer(text):
        value = _parse_date_groups(match.groups())
        if value:
            parsed.append(value)
    return tuple(parsed)


def _parse_date_groups(groups: tuple[str, ...]) -> date | None:
    if len(groups) != 3:
        return None
    day, month, year = groups
    try:
        return date(int(year), _MONTHS[month.casefold()], int(day))
    except (KeyError, ValueError):
        return None


def _add_months(value: date, months: int) -> date:
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def _issue(
    *,
    issue_id: str,
    artifact_type: ArtifactType,
    dimension: str,
    severity: str,
    title: str,
    why: str,
    recommendation: str,
    references: tuple[str, ...],
    clarification: str,
) -> Issue:
    unique_references = tuple(dict.fromkeys(reference for reference in references if reference))
    return Issue(
        id=issue_id,
        artifact_type=artifact_type,
        dimension=dimension,
        severity=severity,
        title=title,
        why=why,
        recommendation=recommendation,
        evidence_refs=unique_references,
        clarification=clarification,
    )


def _issues_overlap(left: Issue, right: Issue) -> bool:
    if left.artifact_type is not right.artifact_type:
        return False
    left_tokens = _issue_tokens(left)
    right_tokens = _issue_tokens(right)
    union = left_tokens | right_tokens
    shared_tokens = left_tokens & right_tokens
    similarity = len(shared_tokens) / len(union) if union else 0
    shares_evidence = bool(set(left.evidence_refs) & set(right.evidence_refs))
    return (
        similarity >= 0.42
        or (shares_evidence and similarity >= 0.24)
        or (
            shares_evidence
            and left.dimension == right.dimension
            and len(shared_tokens) >= 3
        )
    )


def _issue_tokens(issue: Issue) -> set[str]:
    aliases = {
        "exchange": "currency",
        "euro": "currency",
        "euros": "currency",
        "sterling": "currency",
        "treasury": "currency",
        "conversion": "currency",
        "converted": "currency",
        "translated": "currency",
    }
    return {
        aliases.get(token, token)
        for token in re.findall(
            r"[a-z0-9]+",
            f"{issue.title} {issue.why}".casefold(),
        )
        if len(token) > 3
    }
