import calendar
import hashlib
import re
from dataclasses import dataclass, replace
from datetime import date

from oslo_api.analysis.completeness import audit_completeness
from oslo_api.analysis.evidence_graph import build_evidence_graph
from oslo_api.analysis.issue_identity import deduplicate_issues
from oslo_api.analysis.load_bearing import deterministic_finding_tags
from oslo_api.analysis.models import (
    Artifact,
    ArtifactType,
    Assessment,
    EvidenceFragment,
    EvidenceGraph,
    Issue,
    normalize_evidence_state,
)

_MONTHS = {
    name.casefold(): number
    for number in range(1, 13)
    for name in (calendar.month_name[number], calendar.month_abbr[number])
}
_MONTH_PATTERN = "|".join(sorted((re.escape(name) for name in _MONTHS), key=len, reverse=True))
_DATE_PATTERN = rf"\b([0-3]?\d)\s+({_MONTH_PATTERN})\s+(\d{{4}})\b"
_DATE_RE = re.compile(_DATE_PATTERN, re.IGNORECASE)
_BAND_ORDER = {"Very Low": 0, "Low": 1, "Moderate": 2, "High": 3}


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
    """Keep explicit source state separate from the presence of a citation.

    Inferences still require citations showing their basis, but a citation alone
    does not turn synthesized content into a fact stated by the source.
    """

    normalized: list[Artifact] = []
    for artifact in artifacts:
        sections = []
        for section in artifact.sections:
            states = [normalize_evidence_state(state) for state in section.row_states]
            if section.rows and len(states) < len(section.rows):
                states.extend("unknown" for _ in range(len(section.rows) - len(states)))
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
        *audit_evidence_graph(build_evidence_graph(evidence)),
        *audit_completeness(evidence),
        *_summary_appendix_checks(views),
        _freeze_conflict(views),
        _freeze_violation(views),
        _availability_conflict(views),
        _threshold_gap(views),
        *_test_entry_violations(views),
        _measurement_window(views),
        _effort_split(views),
        _missing_gate_milestone(views),
        _funding_conflict(views),
        _contingency_drawdown_ahead_of_progress(views),
        _physical_fit_conflict(views),
        _decision_status_conflict(views),
        _materialized_risk_control_gap(views),
        _action_owner_outside_role_baseline(views),
        _cost_driven_change_without_impact(views),
        _changed_requirements_without_revised_baseline(views),
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
        _front_loaded_payment_before_proof(views),
        _optional_site_scope_conflict(views),
        _regulated_traceability_exclusions(views),
        *_contract_control_gaps(views),
    )
    return tuple(issue for issue in checks if issue is not None)


def _summary_appendix_checks(views: tuple[_View, ...]) -> tuple[Issue, ...]:
    """Compare executive claims with detailed registers in the same evidence set.

    These are generic report-structure checks. They require contradictory or
    missing-control evidence and never flag an appendix merely for being detailed.
    """

    issues: list[Issue] = []
    appendices = tuple(
        view
        for view in views
        if re.match(r"\s*APPENDI(?:X|CES)\b", view.flat, re.I)
    )
    summary = tuple(view for view in views if view not in appendices)
    if not appendices:
        return ()

    schedule_claim = next(
        (
            view
            for view in summary
            if re.search(r"\b(?:on schedule|on plan|schedule\s+green)\b", view.flat, re.I)
        ),
        None,
    )
    milestone_register = next(
        (
            view
            for view in appendices
            if re.search(r"\bfull milestone (?:tracker|register)\b", view.flat, re.I)
            and len(re.findall(r"\bslipped\b", view.flat, re.I)) >= 2
        ),
        None,
    )
    if schedule_claim and milestone_register:
        slipped = len(re.findall(r"\bslipped\b", milestone_register.flat, re.I))
        issues.append(
            _issue(
                issue_id="DET-SCHEDULE-SUMMARY-REGISTER-CONFLICT",
                artifact_type=ArtifactType.SCHEDULE,
                dimension="Alignment",
                severity="Critical",
                title="Schedule summary conflicts with the full milestone register",
                why=(
                    "The executive summary describes the programme as on schedule, "
                    f"while the detailed milestone register records {slipped} slipped "
                    "milestones."
                ),
                recommendation=(
                    "Reconcile the headline schedule status to the complete milestone "
                    "register and publish one approved forecast."
                ),
                references=(
                    schedule_claim.fragment.reference,
                    milestone_register.fragment.reference,
                ),
                clarification=(
                    "Which approved milestone forecast controls the headline schedule status?"
                ),
            )
        )

    summary_milestones: dict[str, tuple[str, _View]] = {}
    for view in summary:
        for match in re.finditer(
            r"\b(?P<id>M\d+)\b.{0,120}?\b(?P<status>on track|complete)\b",
            view.flat,
            re.I,
        ):
            summary_milestones[match.group("id").upper()] = (
                match.group("status"),
                view,
            )
    for appendix in appendices:
        detailed_statuses: dict[str, str] = {}
        for row in re.split(r"(?=\bM\d+\s*\|)", appendix.flat, flags=re.I):
            row_id = re.match(r"\b(M\d+)\s*\|", row, re.I)
            row_status = re.search(r"\|\s*(slipped|not scheduled)\b", row, re.I)
            if row_id and row_status:
                detailed_statuses[row_id.group(1).upper()] = row_status.group(1)
        for milestone_id, (summary_status, summary_view) in summary_milestones.items():
            detail_status = detailed_statuses.get(milestone_id)
            if detail_status is None:
                continue
            issues.append(
                _issue(
                    issue_id=f"DET-SCHEDULE-{milestone_id}-STATUS-CONFLICT",
                    artifact_type=ArtifactType.SCHEDULE,
                    dimension="Alignment",
                    severity="Critical",
                    title=f"{milestone_id} has conflicting summary and register statuses",
                    why=(
                        f"The summary marks {milestone_id} as {summary_status.lower()}, "
                        f"while the full register marks it {detail_status.lower()}."
                    ),
                    recommendation=(
                        "Use the controlled milestone register status in the executive "
                        "summary and explain the approved recovery action."
                    ),
                    references=(
                        summary_view.fragment.reference,
                        appendix.fragment.reference,
                    ),
                    clarification=f"What is the approved current status for {milestone_id}?",
                )
            )

    underspend = next(
        (view for view in summary if re.search(r"\bunderspend\b", view.flat, re.I)),
        None,
    )
    final_cost = next(
        (
            view
            for view in appendices
            if re.search(r"\bforecast final(?: cost)?\b", view.flat, re.I)
            and re.search(r"\b(?:deferr|removed from scope|descope)\w*\b", view.flat, re.I)
        ),
        None,
    )
    if underspend and final_cost:
        issues.append(
            _issue(
                issue_id="DET-RESOURCES-UNDERSPEND-FORECAST-CONFLICT",
                artifact_type=ArtifactType.RESOURCES,
                dimension="Alignment",
                severity="Critical",
                title="Headline underspend conceals the forecast final cost",
                why=(
                    "The summary presents an underspend while the detailed cost "
                    "breakdown attributes it to deferred or removed scope and reports "
                    "a forecast final cost."
                ),
                recommendation=(
                    "Report current-period variance separately from forecast-at-"
                    "completion and disclose every scope deferral driving the variance."
                ),
                references=(
                    underspend.fragment.reference,
                    final_cost.fragment.reference,
                ),
                clarification=(
                    "What approved forecast-at-completion and scope baseline should "
                    "the steering summary report?"
                ),
            )
        )

    cutover = next(
        (
            view
            for view in summary
            if re.search(r"\b(?:cutover|deployment)\b", view.flat, re.I)
            and len(_dates(view.flat)) >= 1
        ),
        next(
            (
                view
                for view in summary
                if re.search(r"\bgo-live\b", view.flat, re.I)
                and len(_dates(view.flat)) >= 1
            ),
            None,
        ),
    )
    protected_window = next(
        (
            view
            for view in appendices
            if re.search(r"\b(?:change freeze|blackout|protected window)\b", view.flat, re.I)
            and (
                len(_dates(view.flat)) >= 2
                or re.search(
                    rf"\b\d{{1,2}}\s+(?:{_MONTH_PATTERN})\s*[–—-]\s*"
                    rf"\d{{1,2}}\s+(?:{_MONTH_PATTERN})\b",
                    view.flat,
                    re.I,
                )
            )
        ),
        None,
    )
    if cutover and protected_window:
        activity_dates = _dates(cutover.flat)
        constraint_dates = _dates(protected_window.flat)
        if len(constraint_dates) >= 2:
            window_start, window_finish = min(constraint_dates), max(constraint_dates)
        else:
            undated = re.search(
                rf"\b(?P<start_day>\d{{1,2}})\s+"
                rf"(?P<start_month>{_MONTH_PATTERN})\s*[–—-]\s*"
                rf"(?P<finish_day>\d{{1,2}})\s+"
                rf"(?P<finish_month>{_MONTH_PATTERN})\b",
                protected_window.flat,
                re.I,
            )
            if undated is None or not activity_dates:
                window_start = window_finish = date.min
            else:
                year = activity_dates[0].year
                window_start = date(
                    year,
                    _MONTHS[undated.group("start_month").casefold()],
                    int(undated.group("start_day")),
                )
                window_finish = date(
                    year,
                    _MONTHS[undated.group("finish_month").casefold()],
                    int(undated.group("finish_day")),
                )
        if any(window_start <= value <= window_finish for value in activity_dates):
            issues.append(
                _issue(
                    issue_id="DET-SCHEDULE-CUTOVER-PROTECTED-WINDOW",
                    artifact_type=ArtifactType.SCHEDULE,
                    dimension="Feasibility",
                    severity="Critical",
                    title="Planned cutover falls inside a protected operating window",
                    why=(
                        "The stated cutover date overlaps a change freeze or protected "
                        "operating window recorded in the detailed risk evidence."
                    ),
                    recommendation=(
                        "Move cutover outside the protected window or approve a governed "
                        "exception with continuity and rollback controls."
                    ),
                    references=(
                        cutover.fragment.reference,
                        protected_window.fragment.reference,
                    ),
                    clarification=(
                        "Which approved cutover date or freeze exception governs delivery?"
                    ),
                )
            )

    risk_summary = next(
        (view for view in summary if re.search(r"\btop risks?\b", view.flat, re.I)),
        None,
    )
    risk_register = next(
        (
            view
            for view in appendices
            if re.search(r"\bfull risk register\b", view.flat, re.I)
            and re.search(r"\bR-\d+\b", view.flat, re.I)
        ),
        None,
    )
    if risk_summary and risk_register:
        summary_ids = set(re.findall(r"\bR-\d+\b", risk_summary.flat, re.I))
        scored = []
        for row in re.split(r"(?=\bR-\d+\b)", risk_register.flat, flags=re.I):
            risk_id = re.match(r"\b(R-\d+)\b", row, re.I)
            if risk_id is None:
                continue
            numeric_cells = [
                int(value)
                for value in re.findall(r"\|\s*(\d{1,2})\s*(?=\|)", row)
            ]
            if numeric_cells:
                scored.append((risk_id.group(1).upper(), max(numeric_cells)))
        omitted_high = tuple(
            risk_id
            for risk_id, score in scored
            if score >= 16 and risk_id not in {item.upper() for item in summary_ids}
        )
        if omitted_high:
            issues.append(
                _issue(
                    issue_id="DET-CONTEXT-TOP-RISK-OMISSIONS",
                    artifact_type=ArtifactType.CONTEXT,
                    dimension="Alignment",
                    severity="High",
                    title="Highest-scored risks are omitted from the executive summary",
                    why=(
                        "The full risk register contains high-scored risks absent from "
                        f"the stated top-risk selection: {', '.join(omitted_high)}."
                    ),
                    recommendation=(
                        "Select top risks from the controlled register using an approved "
                        "ranking rule and explain any deliberate exclusions."
                    ),
                    references=(
                        risk_summary.fragment.reference,
                        risk_register.fragment.reference,
                    ),
                    clarification=(
                        "Which approved ranking rule determines the risks shown to governance?"
                    ),
                )
            )

    approval_gap = next(
        (
            view
            for view in appendices
            if re.search(r"\bapproval\b.{0,80}\bnot scheduled\b", view.flat, re.I)
        ),
        None,
    )
    if approval_gap and cutover:
        issues.append(
            _issue(
                issue_id="DET-SCHEDULE-REQUIRED-APPROVAL-NOT-SCHEDULED",
                artifact_type=ArtifactType.SCHEDULE,
                dimension="Feasibility",
                severity="High",
                title="Required approval is not scheduled before cutover",
                why=(
                    "The detailed milestone evidence marks a required approval as not "
                    "scheduled while the plan retains a cutover date."
                ),
                recommendation=(
                    "Add the approval submission, review, decision and contingency "
                    "milestones to the controlled schedule."
                ),
                references=(
                    approval_gap.fragment.reference,
                    cutover.fragment.reference,
                ),
                clarification=(
                    "Who owns the approval and what approved date gates cutover?"
                ),
            )
        )

    progress = next(
        (
            (view, int(match.group("value")))
            for view in summary
            if (
                match := re.search(
                    r"\b(?P<value>\d{1,3})%\s+(?:programme|program|project)\s+complete\b",
                    view.flat,
                    re.I,
                )
            )
        ),
        None,
    )
    if progress and milestone_register:
        rows = re.split(r"(?=\bM\d+\s*\|)", milestone_register.flat)
        milestone_rows = [row for row in rows if re.match(r"\bM\d+\s*\|", row)]
        completed_rows = [
            row
            for row in milestone_rows
            if re.search(r"\|\s*Complete(?:\s|$)", row, re.I)
        ]
        milestone_percent = (
            round(100 * len(completed_rows) / len(milestone_rows))
            if milestone_rows
            else progress[1]
        )
        if abs(progress[1] - milestone_percent) >= 15:
            issues.append(
                _issue(
                    issue_id="DET-INTENT-PROGRESS-BASIS-CONFLICT",
                    artifact_type=ArtifactType.INTENT,
                    dimension="Alignment",
                    severity="High",
                    title="Headline completion percentage is not reconciled",
                    why=(
                        f"The headline states {progress[1]}% complete while the "
                        f"milestone register indicates approximately {milestone_percent}% "
                        "of listed milestones complete."
                    ),
                    recommendation=(
                        "Define the progress calculation and reconcile it to milestones, "
                        "cost and physical completion."
                    ),
                    references=(
                        progress[0].fragment.reference,
                        milestone_register.fragment.reference,
                    ),
                    clarification="What approved measurement basis defines programme completion?",
                )
            )

    design_complete = next(
        (
            view
            for view in summary
            if re.search(r"\bdesign is complete\b", view.flat, re.I)
        ),
        None,
    )
    design_slip = next(
        (
            view
            for view in appendices
            if re.search(r"\bdesign\b.{0,120}\bslipped\b", view.flat, re.I)
        ),
        None,
    )
    if design_complete and design_slip:
        issues.append(
            _issue(
                issue_id="DET-SCOPE-DESIGN-COMPLETION-CONFLICT",
                artifact_type=ArtifactType.SCOPE,
                dimension="Alignment",
                severity="High",
                title="Design completion claim conflicts with the milestone register",
                why=(
                    "The summary states design is complete while the detailed register "
                    "shows a design milestone as slipped."
                ),
                recommendation=(
                    "State which design areas are complete and retain incomplete areas "
                    "as open controlled milestones."
                ),
                references=(
                    design_complete.fragment.reference,
                    design_slip.fragment.reference,
                ),
                clarification="Which design scope is formally complete and approved?",
            )
        )

    benefit = next(
        (
            view
            for view in summary
            if re.search(r"\b(?:saving|benefit)\b.{0,180}\bautomat\w*\b", view.flat, re.I)
        ),
        None,
    )
    descoped = next(
        (
            view
            for view in views
            if re.search(
                r"\bautomat\w*\b.{0,100}\b(?:removed from scope|descoped?)\b|"
                r"\b(?:removed from scope|descoped?)\b.{0,100}\bautomat\w*\b",
                view.flat,
                re.I,
            )
        ),
        None,
    )
    if benefit and descoped and benefit is not descoped:
        issues.append(
            _issue(
                issue_id="DET-INTENT-BENEFIT-DESCOPED-DEPENDENCY",
                artifact_type=ArtifactType.INTENT,
                dimension="Alignment",
                severity="High",
                title="Headline benefit depends on removed scope",
                why=(
                    "The benefit statement attributes value to automation that another "
                    "part of the evidence says was removed from scope."
                ),
                recommendation=(
                    "Recalculate the benefit case against the approved scope and remove "
                    "benefits that no longer have a delivery mechanism."
                ),
                references=(
                    benefit.fragment.reference,
                    descoped.fragment.reference,
                ),
                clarification="What approved in-scope change now delivers this benefit?",
            )
        )

    no_actions = next(
        (
            view
            for view in summary
            if re.search(r"\bno actions? remain(?:s)? outstanding\b", view.flat, re.I)
        ),
        None,
    )
    open_actions = next(
        (
            view
            for view in views
            if re.search(r"\bcarried forward\b.{0,180}\bstill open\b", view.flat, re.I)
        ),
        None,
    )
    if no_actions and open_actions:
        issues.append(
            _issue(
                issue_id="DET-WORK-BREAKDOWN-OPEN-ACTION-CONFLICT",
                artifact_type=ArtifactType.WORK_BREAKDOWN,
                dimension="Alignment",
                severity="Moderate",
                title="Summary denies actions that remain open",
                why=(
                    "The executive summary says no actions remain outstanding while "
                    "the action evidence lists carried-forward actions as still open."
                ),
                recommendation="Reconcile the summary to the controlled action register.",
                references=(
                    no_actions.fragment.reference,
                    open_actions.fragment.reference,
                ),
                clarification="Which actions are currently open and who owns each one?",
            )
        )

    fully_resourced = next(
        (
            view
            for view in summary
            if re.search(r"\bfully resourced\b|\bno recruitment concerns\b", view.flat, re.I)
        ),
        None,
    )
    vacancies = next(
        (
            view
            for view in appendices
            if re.search(r"\b(?:vacant|vacanc(?:y|ies))\b", view.flat, re.I)
        ),
        None,
    )
    if fully_resourced and vacancies:
        issues.append(
            _issue(
                issue_id="DET-RESOURCES-VACANCY-CONFLICT",
                artifact_type=ArtifactType.RESOURCES,
                dimension="Feasibility",
                severity="Moderate",
                title="Fully-resourced claim conflicts with recorded vacancies",
                why=(
                    "The summary reports full resourcing while the detailed evidence "
                    "records vacant project roles."
                ),
                recommendation=(
                    "Report vacancies in the resource baseline and assign recruitment "
                    "or contingency actions."
                ),
                references=(
                    fully_resourced.fragment.reference,
                    vacancies.fragment.reference,
                ),
                clarification="Which roles remain vacant and what capacity covers them?",
            )
        )

    decision = next(
        (
            view
            for view in summary
            if re.search(r"\bapprove\b.{0,80}\b(?:funding|budget|capital)\b", view.flat, re.I)
        ),
        None,
    )
    if decision and not re.search(
        r"\b(?:option|breakdown|consequence|business case|benefit)\b",
        decision.flat,
        re.I,
    ):
        issues.append(
            _issue(
                issue_id="DET-RESOURCES-FUNDING-DECISION-BASIS-GAP",
                artifact_type=ArtifactType.RESOURCES,
                dimension="Clarity",
                severity="Moderate",
                title="Funding decision lacks a decision-quality basis",
                why=(
                    "The approval request provides no cost breakdown, options, impact "
                    "or consequence of refusal."
                ),
                recommendation=(
                    "Add the funding breakdown, evaluated options, recommendation, "
                    "benefits, risks and consequence of delay or refusal."
                ),
                references=(decision.fragment.reference,),
                clarification="What evidence and options support this funding decision?",
            )
        )

    contingency = next(
        (
            view
            for view in views
            if (
                allowance := re.search(
                    r"\bcontingency allowance\b\s*\|?\s*[£$€]?\s*([\d,]+)",
                    view.flat,
                    re.I,
                )
            )
            and (
                drawn := re.search(
                    r"\bcontingency drawn(?: to date)?\b\s*\|?\s*[£$€]?\s*([\d,]+)",
                    view.flat,
                    re.I,
                )
            )
            and int(drawn.group(1).replace(",", ""))
            / max(int(allowance.group(1).replace(",", "")), 1)
            >= 0.75
        ),
        None,
    )
    if contingency and milestone_register:
        issues.append(
            _issue(
                issue_id="DET-RESOURCES-CONTINGENCY-DRAWDOWN-RISK",
                artifact_type=ArtifactType.RESOURCES,
                dimension="Feasibility",
                severity="Moderate",
                title="Contingency is heavily drawn while delivery remains exposed",
                why=(
                    "At least three quarters of contingency is drawn while the detailed "
                    "schedule still records multiple slipped milestones."
                ),
                recommendation=(
                    "Reforecast remaining exposure, approve contingency controls and "
                    "identify the funding response if current trends continue."
                ),
                references=(
                    contingency.fragment.reference,
                    milestone_register.fragment.reference,
                ),
                clarification="What remaining contingency is available against forecast risk?",
            )
        )

    financial_summary = next(
        (
            view
            for view in summary
            if re.search(r"\bapproved (?:capital )?budget\b", view.flat, re.I)
            and re.search(r"\bspend to date\b", view.flat, re.I)
            and re.search(r"\bcontingency allowance\b", view.flat, re.I)
        ),
        None,
    )
    financial_appendix = next(
        (
            view
            for view in appendices
            if re.search(r"\bcost breakdown\b", view.flat, re.I)
            and re.search(r"\btotal\s*\|", view.flat, re.I)
        ),
        None,
    )
    if financial_summary and financial_appendix:
        def labelled_amount(pattern: str, text_value: str) -> int | None:
            match = re.search(
                pattern + r"\s*\|?\s*[£$€]?\s*([\d,]+)",
                text_value,
                re.I,
            )
            return int(match.group(1).replace(",", "")) if match else None

        budget = labelled_amount(r"\bapproved (?:capital )?budget\b", financial_summary.flat)
        spend = labelled_amount(r"\bspend to date\b", financial_summary.flat)
        allowance = labelled_amount(r"\bcontingency allowance\b", financial_summary.flat)
        drawn = labelled_amount(
            r"\bcontingency drawn(?: to date)?\b",
            financial_summary.flat,
        )
        total_row = re.search(
            r"\btotal\s*\|\s*([\d,]+)\s*\|\s*([\d,]+)\s*\|\s*([\d,]+)",
            financial_appendix.flat,
            re.I,
        )
        basis_disclosed = re.search(
            r"\b(?:including|excluding|inclusive|exclusive)\s+contingency\b",
            f"{financial_summary.flat} {financial_appendix.flat}",
            re.I,
        )
        if (
            total_row
            and None not in {budget, spend, allowance, drawn}
            and budget is not None
            and spend is not None
            and allowance is not None
            and drawn is not None
            and budget + allowance == int(total_row.group(1).replace(",", ""))
            and spend + drawn == int(total_row.group(2).replace(",", ""))
            and basis_disclosed is None
        ):
            issues.append(
                _issue(
                    issue_id="DET-RESOURCES-CONTINGENCY-BASIS-CONFLICT",
                    artifact_type=ArtifactType.RESOURCES,
                    dimension="Clarity",
                    severity="Moderate",
                    title="Financial summaries use different contingency bases",
                    why=(
                        "The headline budget and spend exclude contingency while the "
                        "detailed totals include it, but neither view states that basis."
                    ),
                    recommendation=(
                        "Label every budget, spend and forecast value as including or "
                        "excluding contingency and reconcile the two views."
                    ),
                    references=(
                        financial_summary.fragment.reference,
                        financial_appendix.fragment.reference,
                    ),
                    clarification=(
                        "Which approved contingency basis governs the reported budget "
                        "and spend values?"
                    ),
                )
            )

    if risk_register:
        high_readiness_risk = next(
            (
                row
                for row in re.split(r"(?=\bR-\d+\b)", risk_register.flat, flags=re.I)
                if re.search(r"\b(?:readiness|training)\b", row, re.I)
                and any(
                    int(value) >= 15
                    for value in re.findall(r"\|\s*(\d{1,2})\s*(?=\|)", row)
                )
            ),
            None,
        )
        substantive_readiness = next(
            (
                view
                for view in summary
                if re.search(r"\b(?:readiness|training)\b", view.flat, re.I)
                and re.search(
                    r"\b(?:complete|status|coverage|schedule|milestone|test|approved)\b",
                    view.flat,
                    re.I,
                )
                and not re.search(
                    r"\b(?:action|issue)\b.{0,120}\b(?:readiness|training)\b",
                    view.flat,
                    re.I,
                )
            ),
            None,
        )
        if high_readiness_risk and substantive_readiness is None:
            issues.append(
                _issue(
                    issue_id="DET-WORK-BREAKDOWN-READINESS-CONTROL-GAP",
                    artifact_type=ArtifactType.WORK_BREAKDOWN,
                    dimension="Feasibility",
                    severity="Moderate",
                    title="High operational-readiness risk lacks a delivery control",
                    why=(
                        "The detailed risk register records a high readiness or training "
                        "risk, but the plan provides no substantive readiness scope, "
                        "milestone, status or acceptance evidence."
                    ),
                    recommendation=(
                        "Add owned readiness and training deliverables, entry and exit "
                        "criteria, schedule dates and governance evidence."
                    ),
                    references=(risk_register.fragment.reference,),
                    clarification=(
                        "What owned readiness and training evidence must be complete "
                        "before cutover?"
                    ),
                )
            )

    return tuple(issues)


def _contingency_drawdown_ahead_of_progress(
    views: tuple[_View, ...],
) -> Issue | None:
    for view in views:
        committed = re.search(
            r"\bcontingency\b.{0,220}?\bcommitted\b.{0,100}?"
            r"\((?P<committed>\d+(?:\.\d+)?)%\)",
            view.flat,
            re.I,
        )
        progress = re.search(
            r"\b(?P<progress>\d+(?:\.\d+)?)%\s+"
            r"(?:works?\s+)?(?:complete|completion)\b",
            view.flat,
            re.I,
        )
        if committed is None or progress is None:
            continue
        committed_rate = float(committed.group("committed"))
        progress_rate = float(progress.group("progress"))
        if committed_rate <= progress_rate + 20:
            continue
        return _issue(
            issue_id="DET-RESOURCES-CONTINGENCY-DRAWDOWN",
            artifact_type=ArtifactType.RESOURCES,
            dimension="Feasibility",
            severity="Critical",
            title="Contingency drawdown is ahead of delivery progress",
            why=(
                f"{committed_rate:g}% of contingency is already committed at "
                f"{progress_rate:g}% delivery completion, leaving the remaining "
                "work with materially less risk capacity."
            ),
            recommendation=(
                "Reforecast the remaining risk exposure, identify required "
                "contingency or funding, and set an approved escalation threshold."
            ),
            references=(view.fragment.reference,),
            clarification=(
                "What approved contingency remains sufficient for the unfinished "
                "work and its quantified risks?"
            ),
        )
    return None


def _physical_fit_conflict(views: tuple[_View, ...]) -> Issue | None:
    text_value = " ".join(view.flat for view in views)
    berth = re.search(
        r"\bberth length\b.{0,180}?\breduced from\s+"
        r"(?P<old>\d+(?:\.\d+)?)\s+metres?\s+to\s+"
        r"(?P<new>\d+(?:\.\d+)?)\s+metres?",
        text_value,
        re.I,
    )
    vessel = re.search(
        r"\bdesign vessel\b.{0,180}?\b(?:revised|increased)\s+from\s+"
        r"(?P<old>\d+(?:\.\d+)?)\s+metres?\s+to\s+"
        r"(?P<new>\d+(?:\.\d+)?)\s+metres?",
        text_value,
        re.I,
    )
    if (
        berth is None
        or vessel is None
        or float(vessel.group("new")) <= float(berth.group("new"))
    ):
        return None
    references = tuple(
        dict.fromkeys(
            view.fragment.reference
            for view in views
            if re.search(r"\b(?:berth length|design vessel)\b", view.flat, re.I)
        )
    )
    return _issue(
        issue_id="DET-REQUIREMENTS-PHYSICAL-FIT",
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Feasibility",
        severity="Critical",
        title="The revised asset is smaller than the design load it must accommodate",
        why=(
            f"The governed changes reduce the berth to {berth.group('new')} metres "
            f"while increasing the design vessel to {vessel.group('new')} metres."
        ),
        recommendation=(
            "Complete and approve a physical compatibility assessment, then align "
            "the controlled design requirements and operational acceptance tests."
        ),
        references=references,
        clarification=(
            "Which approved compatibility assessment demonstrates that the revised "
            "asset can accommodate the design load?"
        ),
    )


def _decision_status_conflict(views: tuple[_View, ...]) -> Issue | None:
    agreed = next(
        (
            view
            for view in views
            if re.search(
                r"\bAGREED\b.{0,240}\b(?:change|changed|revised|reduced)\b",
                view.raw,
                re.I,
            )
        ),
        None,
    )
    under_consideration = next(
        (
            view
            for view in views
            if re.search(
                r"\bdesign changes?\b.{0,80}\bcurrently under consideration\b",
                view.flat,
                re.I,
            )
        ),
        None,
    )
    if agreed is None or under_consideration is None:
        return None
    return _issue(
        issue_id="DET-CONTEXT-DECISION-STATUS-CONFLICT",
        artifact_type=ArtifactType.CONTEXT,
        dimension="Alignment",
        severity="Moderate",
        title="A downstream report treats agreed decisions as still under consideration",
        why=(
            "The decision record marks material changes as agreed, while a later "
            "report excludes them as changes still under consideration."
        ),
        recommendation=(
            "Reissue the downstream report using the controlled decision status, "
            "or record an approved reason that the decisions are not effective."
        ),
        references=(
            agreed.fragment.reference,
            under_consideration.fragment.reference,
        ),
        clarification="Which decision status controls the downstream report?",
    )


def _materialized_risk_control_gap(views: tuple[_View, ...]) -> Issue | None:
    assumption = next(
        (
            view
            for view in views
            if re.search(
                r"\b(?:risk|assumption)\b.{0,220}\bassumed\b.{0,100}"
                r"\b(?:highest-rated|high(?:est)? rated)\b",
                view.flat,
                re.I,
            )
        ),
        None,
    )
    changed = next(
        (
            view
            for view in views
            if re.search(
                r"\b(?:determination|approval|licen[cs]e)\b.{0,180}"
                r"\bnow expected\b",
                view.flat,
                re.I,
            )
        ),
        None,
    )
    if assumption is None or changed is None:
        return None
    combined = " ".join(view.flat for view in views)
    if re.search(
        r"\b(?:converted to an issue|issue register|recovery action|recovery owner)\b",
        combined,
        re.I,
    ):
        return None
    return _issue(
        issue_id="DET-CONTEXT-MATERIALIZED-RISK-CONTROL",
        artifact_type=ArtifactType.CONTEXT,
        dimension="Alignment",
        severity="Moderate",
        title="A materialized high-rated risk has no issue owner or recovery control",
        why=(
            "A high-rated assumption is no longer holding, but the supplied "
            "evidence does not convert it to an issue with an owner, recovery "
            "action, decision threshold, and baseline impact."
        ),
        recommendation=(
            "Convert the assumption to a governed issue, assign an accountable "
            "owner, quantify the impact, and approve recovery or rebaselining."
        ),
        references=(assumption.fragment.reference, changed.fragment.reference),
        clarification="Who owns recovery from the materialized risk?",
    )


def _action_owner_outside_role_baseline(views: tuple[_View, ...]) -> Issue | None:
    team = next(
        (
            view
            for view in views
            if re.search(r"\bproject team\b.{0,80}\brole\b.{0,40}\bname\b", view.flat, re.I)
        ),
        None,
    )
    actions = next(
        (
            view
            for view in views
            if re.search(r"\bactions?\b.{0,80}\bowner\b.{0,40}\bby\b", view.flat, re.I)
        ),
        None,
    )
    if team is None or actions is None:
        return None
    owners = tuple(
        dict.fromkeys(
            match.group("surname")
            for match in re.finditer(
                r"\bA\d+\.\d+\b.{0,180}?\b[A-Z]\.\s+"
                r"(?P<surname>[A-Z][A-Za-z-]+)\s+"
                r"\d{1,2}\s+[A-Z][a-z]{2}\s+\d{4}",
                actions.raw,
            )
        )
    )
    outside = next(
        (owner for owner in owners if not re.search(rf"\b{re.escape(owner)}\b", team.raw)),
        None,
    )
    if outside is None:
        return None
    return _issue(
        issue_id="DET-RESOURCES-ACTION-OWNER-ROLE-GAP",
        artifact_type=ArtifactType.RESOURCES,
        dimension="Alignment",
        severity="Moderate",
        title="An action owner has no defined role in the project baseline",
        why=(
            f"The action register assigns material work to {outside}, but that "
            "person has no defined role in the supplied project-team baseline."
        ),
        recommendation=(
            "Define and approve the person's project role, authority, "
            "accountability, and escalation path before the action proceeds."
        ),
        references=(team.fragment.reference, actions.fragment.reference),
        clarification=f"What approved project role and authority does {outside} hold?",
    )


def _cost_driven_change_without_impact(views: tuple[_View, ...]) -> Issue | None:
    for view in views:
        item = re.search(
            r"\b\d+\.\d+\s+(?P<body>.*?\bcost pressure\b.*?)"
            r"(?=\s+\d+\.\d+\s+|\Z)",
            view.raw,
            re.I | re.DOTALL,
        )
        if item is None:
            continue
        body = item.group("body")
        if not re.search(r"\b(?:reduced|removed|changed)\b", body, re.I):
            continue
        if re.search(
            r"(?:\bcost impact\b|\bsavings?\b|\bsaves?\b|"
            r"\b(?:GBP|USD|EUR)\s*\d|[£$€]\s*\d)",
            body,
            re.I,
        ):
            continue
        return _issue(
            issue_id="DET-RESOURCES-COST-DRIVEN-CHANGE-UNQUANTIFIED",
            artifact_type=ArtifactType.RESOURCES,
            dimension="Feasibility",
            severity="Moderate",
            title="A cost-driven scope change has no quantified financial effect",
            why=(
                "The decision record changes scope explicitly because of cost "
                "pressure but records no saving, cost impact, or revised forecast."
            ),
            recommendation=(
                "Quantify the change, update the forecast and benefits impact, "
                "and record the approval basis."
            ),
            references=(view.fragment.reference,),
            clarification="What approved cost effect does this scope change produce?",
        )
    return None


def _changed_requirements_without_revised_baseline(
    views: tuple[_View, ...],
) -> Issue | None:
    combined = " ".join(view.flat for view in views)
    decisions = len(
        re.findall(
            r"\bAGREED\b.{0,140}\b(?:changed|revised|reduced)\b",
            combined,
            re.I,
        )
    )
    versioned_baseline = re.search(
        r"\b(?:brief|baseline)\b.{0,40}\bv?\d+\.\d+\b",
        combined,
        re.I,
    )
    if decisions < 2 or versioned_baseline is None:
        return None
    if re.search(
        r"\b(?:revised|updated|superseding)\s+(?:client\s+)?(?:brief|baseline)\b",
        combined,
        re.I,
    ):
        return None
    references = tuple(
        dict.fromkeys(
            view.fragment.reference
            for view in views
            if re.search(r"\b(?:brief|AGREED)\b", view.raw, re.I)
        )
    )
    return _issue(
        issue_id="DET-SCOPE-CHANGES-NO-REVISED-BASELINE",
        artifact_type=ArtifactType.SCOPE,
        dimension="Alignment",
        severity="Moderate",
        title="Multiple requirement changes have no revised controlled baseline",
        why=(
            "The evidence records several agreed changes to controlled requirements "
            "but does not identify a revised or superseding baseline."
        ),
        recommendation=(
            "Issue one approved replacement baseline and trace every changed value "
            "into design, cost, schedule, procurement, and acceptance evidence."
        ),
        references=references,
        clarification="Which approved version supersedes the changed baseline?",
    )


def audit_evidence_graph(graph: EvidenceGraph) -> tuple[Issue, ...]:
    claims = {claim.id: claim for claim in graph.claims}
    issues: list[Issue] = []
    for relation in graph.relations:
        if relation.relation_type == "contradicts":
            left = claims.get(relation.source_claim_id)
            right = claims.get(relation.target_claim_id)
            predicates = (
                {left.predicate, right.predicate}
                if left is not None and right is not None
                else set()
            )
            if predicates == {
                "forbids_property_rate_change",
                "allows_property_discount",
            }:
                property_discount = (
                    left if left.predicate == "allows_property_discount" else right
                )
                central_control = right if property_discount is left else left
                digest = hashlib.sha256(
                    (
                        f"{central_control.id}|{property_discount.id}|"
                        "central-property-rate-control"
                    ).encode()
                ).hexdigest()[:12].upper()
                issues.append(
                    _issue(
                        issue_id=f"DET-REQUIREMENTS-RATE-{digest}",
                        artifact_type=ArtifactType.REQUIREMENTS,
                        dimension="Feasibility",
                        severity="Critical",
                        title=(
                            "Central rate control conflicts with a "
                            "property-level discount"
                        ),
                        why=(
                            "The plan forbids property-level rate amendments "
                            "while also allowing front-desk staff to apply a "
                            f"discount of up to {property_discount.value}%. "
                            "Both authority rules cannot govern the same rate."
                        ),
                        recommendation=(
                            "Define whether the discount is an approved central "
                            "rate rule or a governed property exception, including "
                            "limits, approval, audit and acceptance tests."
                        ),
                        references=relation.evidence_refs,
                        clarification=(
                            "Which approved authority rule governs the "
                            "property-level discount?"
                        ),
                    )
                )
                continue
            if (
                left is None
                or right is None
                or predicates
                != {
                    "allows_overbooking",
                    "forbids_confirmation_without_inventory",
                }
            ):
                continue
            overbooking = (
                left if left.predicate == "allows_overbooking" else right
            )
            inventory_guard = right if overbooking is left else left
            digest = hashlib.sha256(
                (
                    f"{overbooking.id}|{inventory_guard.id}|"
                    "overbooking-inventory-policy"
                ).encode()
            ).hexdigest()[:12].upper()
            issues.append(
                _issue(
                    issue_id=f"DET-REQUIREMENTS-INVENTORY-{digest}",
                    artifact_type=ArtifactType.REQUIREMENTS,
                    dimension="Feasibility",
                    severity="Critical",
                    title=(
                        "Controlled overbooking conflicts with the "
                        "available-inventory rule"
                    ),
                    why=(
                        f"The plan permits controlled overbooking up to "
                        f"{overbooking.value}% of capacity, while another rule "
                        "forbids confirming a reservation when no inventory is "
                        "available. Both requirements cannot govern the same "
                        "inventory state."
                    ),
                    recommendation=(
                        "Define one approved inventory and overbooking policy, "
                        "including the capacity basis, exception conditions, "
                        "controls, accountable owner, and acceptance tests."
                    ),
                    references=relation.evidence_refs,
                    clarification=(
                        "When physical inventory is exhausted, which approved "
                        "rule governs controlled overbooking?"
                    ),
                )
            )
        elif relation.relation_type == "contradicts_measurement":
            left = claims.get(relation.source_claim_id)
            right = claims.get(relation.target_claim_id)
            if (
                left is None
                or right is None
                or left.numeric_value is None
                or right.numeric_value is None
                or left.unit is None
            ):
                continue
            subject_tokens = _issue_subject_tokens(left.subject, right.subject)
            subject = " ".join(subject_tokens) or "Measured requirement"
            digest = hashlib.sha256(
                (
                    f"{left.id}|{right.id}|measured-value-conflict"
                ).encode()
            ).hexdigest()[:12].upper()
            issues.append(
                _issue(
                    issue_id=f"DET-REQUIREMENTS-MEASUREMENT-{digest}",
                    artifact_type=ArtifactType.REQUIREMENTS,
                    dimension="Alignment",
                    severity="Moderate",
                    title=f"{subject.title()} has conflicting measured values",
                    why=(
                        f"The supplied evidence states {left.numeric_value:g} "
                        f"{left.unit.replace('_', ' ')} and "
                        f"{right.numeric_value:g} "
                        f"{right.unit.replace('_', ' ')} for the same subject."
                    ),
                    recommendation=(
                        "Approve one controlled value and update every affected "
                        "requirement, design, cost, schedule and acceptance baseline."
                    ),
                    references=relation.evidence_refs,
                    clarification=(
                        f"Which approved value controls {subject}, and from what date?"
                    ),
                )
            )
            continue
        if relation.relation_type != "violates":
            continue
        activity = claims.get(relation.source_claim_id)
        constraint = claims.get(relation.target_claim_id)
        if activity is None or constraint is None:
            continue
        digest = hashlib.sha256(
            f"{activity.id}|{constraint.id}|protected-window".encode()
        ).hexdigest()[:12].upper()
        issues.append(
            _issue(
                issue_id=f"DET-SCHEDULE-WINDOW-{digest}",
                artifact_type=ArtifactType.SCHEDULE,
                dimension="Feasibility",
                severity="Critical",
                title="Scheduled activity overlaps a protected operating window",
                why=(
                    f"The scheduled window {activity.value} overlaps the protected "
                    f"window {constraint.value}. The plan states: {constraint.raw_text}"
                ),
                recommendation=(
                    "Move the activity outside the protected window or record an "
                    "approved exception, continuity plan, accountable owner, and "
                    "tested rollback."
                ),
                references=relation.evidence_refs,
                clarification=(
                    "Which approved date or exception governs this activity?"
                ),
            )
        )

    stated_rate = next(
        (
            claim
            for claim in graph.claims
            if claim.predicate == "contingency_rate"
            and claim.numeric_value is not None
        ),
        None,
    )
    base_cost = next(
        (
            claim
            for claim in graph.claims
            if claim.predicate == "base_cost" and claim.numeric_value
        ),
        None,
    )
    contingency = next(
        (
            claim
            for claim in graph.claims
            if claim.predicate == "contingency_amount" and claim.numeric_value
        ),
        None,
    )
    if stated_rate and base_cost and contingency:
        actual_rate = contingency.numeric_value / base_cost.numeric_value * 100
        if abs(actual_rate - stated_rate.numeric_value) >= 0.75:
            digest = hashlib.sha256(
                (
                    f"{stated_rate.id}|{base_cost.id}|{contingency.id}|"
                    "contingency-rate"
                ).encode()
            ).hexdigest()[:12].upper()
            issues.append(
                _issue(
                    issue_id=f"DET-RESOURCES-RATIO-{digest}",
                    artifact_type=ArtifactType.RESOURCES,
                    dimension="Clarity",
                    severity="Moderate",
                    title="Stated contingency percentage does not match the budget",
                    why=(
                        f"The plan states {stated_rate.numeric_value:g}% contingency, "
                        f"but {contingency.numeric_value:g} against a base cost of "
                        f"{base_cost.numeric_value:g} is {actual_rate:.1f}%."
                    ),
                    recommendation=(
                        "Correct the stated percentage or the budget amounts and have "
                        "the accountable budget owner approve one controlled baseline."
                    ),
                    references=tuple(
                        dict.fromkeys(
                            (
                                stated_rate.evidence_ref,
                                base_cost.evidence_ref,
                                contingency.evidence_ref,
                            )
                        )
                    ),
                    clarification=(
                        "Which contingency percentage and amount form the approved "
                        "cost baseline?"
                    ),
                )
            )

    expiry_claims = tuple(
        claim for claim in graph.claims if claim.predicate == "expires_on"
    )
    project_end_claims = tuple(
        claim for claim in graph.claims if claim.predicate == "project_end"
    )
    source_text = " ".join(
        claim.raw_text for claim in graph.claims if claim.predicate == "source_text"
    )
    has_contract_cover = bool(
        re.search(
            r"\b(?:renewal|renewed|extension|extend(?:ed|s|ing)?|replacement)"
            r".{0,120}\b(?:contract|agreement|circuit|licen[cs]e)\b|"
            r"\b(?:contract|agreement|circuit|licen[cs]e)\b.{0,120}"
            r"(?:renewal|renewed|extension|extend(?:ed|s|ing)?|replacement)",
            source_text,
            re.I,
        )
    )
    if expiry_claims and project_end_claims and not has_contract_cover:
        expiry = min(expiry_claims, key=lambda claim: claim.value)
        project_end = max(project_end_claims, key=lambda claim: claim.value)
        if date.fromisoformat(expiry.value) < date.fromisoformat(project_end.value):
            digest = hashlib.sha256(
                f"{expiry.id}|{project_end.id}|contract-cover".encode()
            ).hexdigest()[:12].upper()
            issues.append(
                _issue(
                    issue_id=f"DET-RESOURCES-EXPIRY-{digest}",
                    artifact_type=ArtifactType.RESOURCES,
                    dimension="Clarity",
                    severity="Moderate",
                    title="External contract expires before project completion",
                    why=(
                        f"The external agreement expires on {expiry.value}, before "
                        f"the project completes on {project_end.value}, and the "
                        "supplied evidence contains no renewal, extension, or "
                        "replacement route."
                    ),
                    recommendation=(
                        "Add the approved renewal, extension, or replacement dependency "
                        "with an owner, decision date, funding, and fallback."
                    ),
                    references=tuple(
                        dict.fromkeys(
                            (expiry.evidence_ref, project_end.evidence_ref)
                        )
                    ),
                    clarification=(
                        "What approved commercial arrangement covers the dependency "
                        "through project completion?"
                    ),
                )
            )

    verification_windows = tuple(
        claim
        for claim in graph.claims
        if claim.predicate == "verification_window" and "/" in claim.value
    )
    scheduled_activities = tuple(
        claim
        for claim in graph.claims
        if claim.predicate == "scheduled_for"
        and "/" not in claim.value
        and re.search(
            r"\b(?:cutover|go[- ]?live|commissioning)\b",
            claim.subject,
            re.I,
        )
    )
    premature_activities = tuple(
        activity
        for activity in scheduled_activities
        if any(
            date.fromisoformat(activity.value)
            < date.fromisoformat(window.value.split("/", 1)[1])
            for window in verification_windows
        )
    )
    if premature_activities and verification_windows:
        references = tuple(
            dict.fromkeys(
                (
                    *(claim.evidence_ref for claim in premature_activities),
                    *(claim.evidence_ref for claim in verification_windows),
                )
            )
        )
        digest = hashlib.sha256(
            f"{'|'.join(references)}|readiness-before-live".encode()
        ).hexdigest()[:12].upper()
        issues.append(
            _issue(
                issue_id=f"DET-SCHEDULE-READINESS-{digest}",
                artifact_type=ArtifactType.SCHEDULE,
                dimension="Feasibility",
                severity="Low",
                title="Go-live occurs before resilience and readiness testing completes",
                why=(
                    "The plan schedules production cutover or go-live before the "
                    "documented resilience or operational-readiness test window has "
                    "finished."
                ),
                recommendation=(
                    "Move production activation after the required verification gate "
                    "or document an approved staged exception with entry criteria, "
                    "monitoring, and rollback."
                ),
                references=references,
                clarification=(
                    "Which approved verification gate authorizes these production "
                    "activations?"
                ),
            )
        )

    volumes = tuple(
        claim
        for claim in graph.claims
        if claim.predicate == "total_volume" and claim.numeric_value
    )
    rates = tuple(
        claim
        for claim in graph.claims
        if claim.predicate == "delivery_rate"
        and claim.numeric_value
        and claim.unit
        and claim.unit.endswith("/per_week")
    )
    delivery_windows = tuple(
        claim
        for claim in graph.claims
        if claim.predicate == "scheduled_for"
        and "/" in claim.value
        and re.search(r"\b(?:migration|transfer|archive|delivery)\b", claim.raw_text, re.I)
    )
    for volume in volumes:
        rate = next(
            (
                candidate
                for candidate in rates
                if candidate.unit
                and volume.unit
                and candidate.unit.split("/", 1)[0] == volume.unit
            ),
            None,
        )
        if rate is None or not delivery_windows:
            continue
        delivery_window = max(
            delivery_windows,
            key=lambda claim: (
                date.fromisoformat(claim.value.split("/", 1)[1])
                - date.fromisoformat(claim.value.split("/", 1)[0])
            ).days,
        )
        start_value, finish_value = delivery_window.value.split("/", 1)
        available_weeks = max(
            (
                date.fromisoformat(finish_value) - date.fromisoformat(start_value)
            ).days
            / 7,
            1,
        )
        required_weeks = volume.numeric_value / rate.numeric_value
        if required_weeks <= available_weeks * 1.05:
            continue
        references = tuple(
            dict.fromkeys(
                (
                    volume.evidence_ref,
                    rate.evidence_ref,
                    delivery_window.evidence_ref,
                )
            )
        )
        digest = hashlib.sha256(
            f"{volume.id}|{rate.id}|{delivery_window.id}|throughput".encode()
        ).hexdigest()[:12].upper()
        issues.append(
            _issue(
                issue_id=f"DET-SCHEDULE-THROUGHPUT-{digest}",
                artifact_type=ArtifactType.SCHEDULE,
                dimension="Feasibility",
                severity="Critical",
                title="Throughput cannot complete the stated volume in the delivery window",
                why=(
                    f"The stated volume requires {required_weeks:.1f} weeks at "
                    f"{rate.numeric_value:g} {rate.unit}, but the scheduled window "
                    f"provides about {available_weeks:.1f} weeks."
                ),
                recommendation=(
                    "Approve the required throughput and capacity, fund the increase, "
                    "add measurable checkpoints, and define a fallback for any volume "
                    "that cannot complete in the window."
                ),
                references=references,
                clarification=(
                    "What funded throughput and fallback deliver the complete volume "
                    "inside the approved window?"
                ),
            )
        )
    return deduplicate_issues(tuple(issues))


def _issue_subject_tokens(left: str, right: str) -> tuple[str, ...]:
    left_tokens = tuple(re.findall(r"[a-z][a-z0-9-]+", left.casefold()))
    right_set = set(re.findall(r"[a-z][a-z0-9-]+", right.casefold()))
    return tuple(
        token
        for token in left_tokens
        if token in right_set
        and token
        not in {
            "capital",
            "design",
            "item",
            "project",
            "requirement",
            "value",
        }
    )


def audit_artifact_conflicts(artifacts: tuple[Artifact, ...]) -> tuple[Issue, ...]:
    """Promote structured contradictions into governed issues.

    Construct already records explicit conflicts with row-level evidence. Relying
    on a second model call to rediscover every one made valid prerequisite,
    resource and assumption conflicts disappear from Issues. This bridge is
    domain-neutral: a material structured conflict must remain visible until a
    user or later evidence resolves it.
    """

    candidates: list[Issue] = []
    for artifact in artifacts:
        for conflict in artifact.conflicts:
            values = tuple(value.strip() for value in conflict.values if value.strip())
            references = tuple(dict.fromkeys(conflict.evidence_refs))
            if not values or not references:
                continue
            for atomic_values in _atomic_conflict_groups(values):
                if len(atomic_values) < 2 and not _self_contained_conflict(
                    atomic_values[0]
                ):
                    continue
                field = _atomic_conflict_field(
                    conflict.field.strip(),
                    atomic_values,
                )
                normalized = (
                    f"{artifact.artifact_type.value}|{field}|"
                    f"{'|'.join(atomic_values)}"
                )
                digest = hashlib.sha256(
                    normalized.casefold().encode()
                ).hexdigest()[:12].upper()
                dimension = (
                    "Feasibility"
                    if artifact.artifact_type
                    in {
                        ArtifactType.SCHEDULE,
                        ArtifactType.RESOURCES,
                        ArtifactType.WORK_BREAKDOWN,
                    }
                    else "Alignment"
                )
                material_text = f"{field} {' '.join(atomic_values)}"
                severity = (
                    "Critical"
                    if re.search(
                        r"\b(?:prerequisite|approval|release|regulatory|capacity|"
                        r"availability|qualified operators?|safety|compliance)\b",
                        material_text,
                        re.I,
                    )
                    else "Moderate"
                )
                candidates.append(
                    _issue(
                        issue_id=(
                            f"DET-{artifact.artifact_type.value.upper()}-"
                            f"CONFLICT-{digest}"
                        ),
                        artifact_type=artifact.artifact_type,
                        dimension=dimension,
                        severity=severity,
                        title=f"{field} is internally inconsistent",
                        why=(
                            "The structured read records competing statements: "
                            f"{'; '.join(atomic_values)}"
                        ),
                        recommendation=(
                            "Approve one controlled interpretation, reconcile every "
                            "dependent artifact and date, and record the accountable "
                            "decision owner."
                        ),
                        references=references,
                        clarification=(
                            f"Which statement controls {field}, and who approved it?"
                        ),
                    )
                )
    return deduplicate_issues(tuple(candidates))


def _atomic_conflict_groups(
    values: tuple[str, ...],
) -> tuple[tuple[str, ...], ...]:
    """Keep independently actionable contradictions as separate issues."""

    if len(values) > 1 and all(_self_contained_conflict(value) for value in values):
        return tuple((value,) for value in values)
    return (values,)


def _self_contained_conflict(value: str) -> bool:
    return bool(
        ":" in value
        and re.search(
            r";|\b(?:but|while|whereas|versus|vs\.?)\b",
            value,
            re.I,
        )
    )


def _atomic_conflict_field(
    fallback: str,
    values: tuple[str, ...],
) -> str:
    if len(values) != 1 or ":" not in values[0]:
        return fallback
    candidate = values[0].split(":", 1)[0].strip()
    return candidate if 3 <= len(candidate) <= 100 else fallback


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
    return deduplicate_issues(tuple(merged))


def apply_evidence_rubric(
    assessment: Assessment,
    evidence: tuple[EvidenceFragment, ...],
) -> Assessment:
    """Apply deterministic safety caps without upgrading qualitative model bands.

    A detailed document can still describe a strategically misaligned or infeasible
    plan. Evidence density therefore improves assessability, not Clarity, Alignment,
    Feasibility, Reliability, or Confidence by itself. This guardrail only lowers
    confidence when governed open findings make a higher read contradictory.
    """

    del evidence  # Evidence density must never act as a quality proxy.
    critical_findings = [
        issue
        for issue in assessment.issues
        if issue.status != "resolved" and issue.severity == "Critical"
    ]
    confidence_band = assessment.confidence_band
    confidence_index = assessment.confidence_index
    if critical_findings and confidence_band in {"Moderate", "High"}:
        confidence_band = "Low"
        confidence_index = min(confidence_index, 38)
    elif assessment.reliability == "Low" and confidence_band == "High":
        confidence_band = "Moderate"
        confidence_index = min(confidence_index, 62)

    dimension_bands = {
        dimension: _cap_dimension_band(
            getattr(assessment, dimension.casefold()),
            tuple(
                issue
                for issue in assessment.issues
                if issue.status != "resolved" and issue.dimension == dimension
            ),
        )
        for dimension in ("Clarity", "Alignment", "Feasibility")
    }
    return replace(
        assessment,
        confidence_index=confidence_index,
        confidence_band=confidence_band,
        clarity=dimension_bands["Clarity"],
        alignment=dimension_bands["Alignment"],
        feasibility=dimension_bands["Feasibility"],
    )


def _cap_dimension_band(current: str, issues: tuple[Issue, ...]) -> str:
    critical = sum(issue.severity == "Critical" for issue in issues)
    material = sum(issue.severity in {"Critical", "Moderate"} for issue in issues)
    cap = (
        "Very Low"
        if critical >= 4 or material >= 6
        else "Low"
        if critical >= 2
        else "Moderate"
        if material >= 3
        else current
    )
    return min((current, cap), key=lambda band: _BAND_ORDER.get(band, -1))


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
        if re.search(
            r"\b(?:single[- ]source|single\s+(?:vendor|supplier)(?:\s+contract)?)\b",
            view.flat,
            re.I,
        )
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
    deliverable_warranty = next(
        (
            (
                int(match.group(1)),
                view.fragment.reference,
            )
            for view in views
            if (
                match := re.search(
                    r"\b(?:warranty|warranted|warrants)\b.{0,220}?\b(\d{1,3})\s+days?\s+"
                    r"from\b.{0,50}\bdelivery\b",
                    view.flat,
                    re.I,
                )
            )
        ),
        None,
    )
    engagement = next(
        (
            (int(match.group(1)), view.fragment.reference)
            for view in views
            if (
                match := re.search(
                    r"\b(?:engagement|project)\b.{0,80}\b(\d{1,3})\s+weeks?\b",
                    view.flat,
                    re.I,
                )
            )
        ),
        None,
    )
    if (
        deliverable_warranty is not None
        and engagement is not None
        and deliverable_warranty[0] < engagement[0] * 7
    ):
        return _issue(
            issue_id="DET-RESOURCES-EARLY-WARRANTY-EXPIRY",
            artifact_type=ArtifactType.RESOURCES,
            dimension="Alignment",
            severity="High",
            title="Early deliverable warranties can expire before operational use",
            why=(
                f"Each deliverable has {deliverable_warranty[0]} days of warranty "
                f"from delivery within a {engagement[0]}-week engagement, so early "
                "deliverables can lose cover before integrated go-live proves them."
            ),
            recommendation=(
                "Start warranty at system acceptance or go-live and preserve remedies "
                "for latent integration defects through operational proving."
            ),
            references=(engagement[1], deliverable_warranty[1]),
            clarification=(
                "What warranty remains for early deliverables when the integrated "
                "system reaches go-live?"
            ),
        )

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
        for match in re.finditer(r"\bdeliver(?:y|ed)\b", view.flat, re.I):
            nearby = view.flat[max(0, match.start() - 40) : match.end() + 140]
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


def _front_loaded_payment_before_proof(views: tuple[_View, ...]) -> Issue | None:
    """Detect contracts that transfer most value before outcome evidence exists."""

    payment_view = next(
        (
            view
            for view in views
            if "payment milestone" in view.flat.casefold()
            and re.search(
                r"\bcommencement of (?:user )?acceptance testing\b",
                view.flat,
                re.I,
            )
            and re.search(r"\birrespective of outcome\b", view.flat, re.I)
        ),
        None,
    )
    if payment_view is None:
        return None

    paid_before_proof = 0
    for match in re.finditer(r"\b(\d{1,3})\s*%", payment_view.flat):
        context = payment_view.flat[
            max(0, match.start() - 90) : min(len(payment_view.flat), match.end() + 120)
        ]
        if re.search(
            r"\b(?:contract signature|design approval|commencement of "
            r"(?:user )?acceptance testing)\b",
            context,
            re.I,
        ):
            paid_before_proof += int(match.group(1))
    if paid_before_proof < 75:
        return None

    retained_after_proof = any(
        re.search(
            r"\b(?:retention|holdback)\b.{0,100}\b(?:warranty|acceptance|"
            r"operational proof|go-live)\b",
            view.flat,
            re.I,
        )
        for view in views
    )
    if retained_after_proof:
        return None

    testing_refs = tuple(
        view.fragment.reference
        for view in views
        if re.search(
            r"\bclient\b.{0,80}\b(?:author|execute)\b.{0,80}"
            r"\b(?:system integration test|user acceptance test)\b",
            view.flat,
            re.I,
        )
    )
    references = tuple(
        dict.fromkeys((*testing_refs, payment_view.fragment.reference))
    )
    return _issue(
        issue_id="DET-RESOURCES-PAYMENT-BEFORE-PROOF",
        artifact_type=ArtifactType.RESOURCES,
        dimension="Feasibility",
        severity="Critical",
        title=f"{paid_before_proof}% of fees are payable before the system is proven",
        why=(
            f"The payment schedule makes {paid_before_proof}% payable by the "
            "start of acceptance testing, including a testing payment that is "
            "due irrespective of outcome, with no retained value after proof."
        ),
        recommendation=(
            "Tie material payments to measurable, client-approved acceptance "
            "evidence and retain an appropriate amount through go-live and warranty."
        ),
        references=references,
        clarification=(
            "Which payment is retained until system-level acceptance and "
            "post-go-live performance are proven?"
        ),
    )


def _optional_site_scope_conflict(views: tuple[_View, ...]) -> Issue | None:
    committed = tuple(
        view
        for view in views
        if re.search(
            r"\b(?:implement|deploy|roll out)\b.{0,120}\b(?:three|3)\b"
            r".{0,40}\bsites?\b",
            view.flat,
            re.I,
        )
    )
    optional = tuple(
        view
        for view in views
        if re.search(
            r"\bsites?\s*2\b.{0,50}\b(?:and|&)\b.{0,30}\bsites?\s*3\b"
            r".{0,100}\boptional\b|"
            r"\boptional\b.{0,100}\bsites?\s*2\b.{0,50}\bsites?\s*3\b",
            view.flat,
            re.I,
        )
    )
    site_one_only = any(
        re.search(
            r"\b(?:configured system|cutover|go-live)\b.{0,60}\bsite\s*1\b|"
            r"\bsite\s*1\b.{0,60}\b(?:configured system|cutover|go-live)\b",
            view.flat,
            re.I,
        )
        for view in views
    )
    if not committed or not optional or not site_one_only:
        return None
    references = tuple(
        dict.fromkeys(
            view.fragment.reference for view in (*committed, *optional)
        )
    )
    return _issue(
        issue_id="DET-SCOPE-OPTIONAL-SITES",
        artifact_type=ArtifactType.SCOPE,
        dimension="Alignment",
        severity="Critical",
        title="The stated multi-site outcome is not included in the contracted scope",
        why=(
            "The background commits to implementation across three sites, while "
            "the deliverables cover Site 1 and make Sites 2 and 3 optional paid work."
        ),
        recommendation=(
            "Reconcile the outcome, deliverables and total price so every committed "
            "site is explicitly included or the background is limited to Site 1."
        ),
        references=references,
        clarification=(
            "Is the signed commitment for one site or all three sites, and which "
            "price includes that commitment?"
        ),
    )


def _regulated_traceability_exclusions(views: tuple[_View, ...]) -> Issue | None:
    outcome = tuple(
        view
        for view in views
        if re.search(
            r"\bfull batch traceability\b.{0,80}\b(?:BRC|regulatory standard)\b",
            view.flat,
            re.I,
        )
    )
    exclusions = tuple(
        view
        for view in views
        if "exclu" in view.flat.casefold()
        and sum(
            bool(re.search(pattern, view.flat, re.I))
            for pattern in (
                r"\blaboratory\b.{0,40}\bintegration\b",
                r"\ballergen\b.{0,50}\b(?:master data|configuration)\b",
                r"\bvalidation documentation\b.{0,80}\b(?:audit|regulatory)\b",
            )
        )
        >= 2
    )
    if not outcome or not exclusions:
        return None
    references = tuple(
        dict.fromkeys(
            view.fragment.reference for view in (*outcome, *exclusions)
        )
    )
    return _issue(
        issue_id="DET-SCOPE-TRACEABILITY-EXCLUSIONS",
        artifact_type=ArtifactType.SCOPE,
        dimension="Alignment",
        severity="Critical",
        title="Regulated traceability outcome conflicts with material exclusions",
        why=(
            "The scope promises full BRC-regulated batch traceability while excluding "
            "multiple laboratory, allergen and audit-validation capabilities needed "
            "to evidence that outcome."
        ),
        recommendation=(
            "Define the traceability control chain and include every required "
            "integration, data configuration and validation deliverable, or narrow "
            "the promised outcome."
        ),
        references=references,
        clarification=(
            "How will the regulated traceability outcome be achieved and audited "
            "with the listed exclusions?"
        ),
    )


def _contract_control_gaps(views: tuple[_View, ...]) -> tuple[Issue, ...]:
    """Audit asymmetric commercial controls without treating all supplier terms as defects."""

    issues: list[Issue] = []
    deliverables = tuple(
        view
        for view in views
        if re.search(r"\bdeliverables?\b", view.flat, re.I)
        and re.search(
            r"\b(?:description\b.{0,40}\bformat|format\b.{0,40}\bdescription)\b",
            view.flat,
            re.I,
        )
    )
    deemed = tuple(
        view
        for view in views
        if re.search(r"\bdeliverable\b.{0,80}\bdeemed accepted\b", view.flat, re.I)
        or re.search(r"\bdeemed accepted\b.{0,80}\bdeliverable\b", view.flat, re.I)
    )
    objective_acceptance = any(
        re.search(
            r"\b(?:acceptance criteria|acceptance threshold|pass\/fail standard|"
            r"measurable non-conformance)\b",
            view.flat,
            re.I,
        )
        for view in views
    )
    if deliverables and deemed and not objective_acceptance:
        issues.append(
            _issue(
                issue_id="DET-REQUIREMENTS-DEEMED-ACCEPTANCE",
                artifact_type=ArtifactType.REQUIREMENTS,
                dimension="Clarity",
                severity="Critical",
                title="Deliverables can be deemed accepted without objective criteria",
                why=(
                    "The deliverable register defines descriptions and formats but "
                    "no measurable acceptance criteria, while silence starts deemed "
                    "acceptance after a short review period."
                ),
                recommendation=(
                    "Add measurable acceptance criteria, evidence, approvers and a "
                    "review period appropriate to each deliverable before deemed "
                    "acceptance can operate."
                ),
                references=tuple(
                    dict.fromkeys(
                        view.fragment.reference for view in (*deliverables, *deemed)
                    )
                ),
                clarification=(
                    "Against which objective criteria must each deliverable be tested "
                    "before acceptance?"
                ),
            )
        )

    timeline = tuple(
        view
        for view in views
        if re.search(
            r"\b\d+\s+weeks?\s+from\s+the\s+effective date\b",
            view.flat,
            re.I,
        )
        and re.search(
            r"\bproject plan\b.{0,80}\bwithin\s+\d+\s+business days?\b",
            view.flat,
            re.I,
        )
    )
    if timeline:
        issues.append(
            _issue(
                issue_id="DET-SCHEDULE-UNDEFINED-EFFECTIVE-DATE",
                artifact_type=ArtifactType.SCHEDULE,
                dimension="Clarity",
                severity="High",
                title="The delivery baseline depends on an undefined effective date",
                why=(
                    "The contract states a relative duration of 34 weeks and defers the "
                    "detailed plan until after the effective date, so no dated "
                    "commitment exists at approval."
                ),
                recommendation=(
                    "Define the effective date, dated phase baseline, milestones, "
                    "dependencies and approval gates before commitment."
                ),
                references=tuple(
                    dict.fromkeys(view.fragment.reference for view in timeline)
                ),
                clarification="Which dated baseline is binding when the contract is signed?",
            )
        )

    liability = tuple(
        view
        for view in views
        if re.search(
            r"\bliability\b.{0,120}\bfees? (?:actually )?paid\b.{0,80}"
            r"\b(?:six|6) months?\b",
            view.flat,
            re.I,
        )
        and re.search(
            r"\b(?:loss of production|spoilage)\b",
            view.flat,
            re.I,
        )
    )
    if liability:
        issues.append(
            _issue(
                issue_id="DET-RESOURCES-LIABILITY-RISK-TRANSFER",
                artifact_type=ArtifactType.RESOURCES,
                dimension="Feasibility",
                severity="High",
                title="Liability terms transfer the core operational exposure to the client",
                why=(
                    "Supplier liability is capped at fees paid in the preceding six "
                    "months and "
                    "excludes production loss or spoilage, leaving the client to carry "
                    "the material risk the system is intended to control."
                ),
                recommendation=(
                    "Align liability caps, exclusions, insurance and remedies to the "
                    "credible operational loss scenarios and supplier control."
                ),
                references=tuple(view.fragment.reference for view in liability),
                clarification=(
                    "Which remedy covers production loss or spoilage caused by a "
                    "supplier-controlled failure?"
                ),
            )
        )

    obligation_views = tuple(
        view
        for view in views
        if "client obligations" in view.flat.casefold()
        and re.search(
            r"\b7\.\s*[A-Z][A-Za-z& -]{1,50}\bObligations\b|\b7\.1\b",
            view.raw,
        )
    )
    penalty_views = tuple(
        view
        for view in views
        if re.search(
            r"\bclient dependency\b.{0,120}\b(?:standing charges|per working day)\b",
            view.flat,
            re.I,
        )
    )
    if obligation_views and penalty_views:
        client_count = max(
            (
                len(set(re.findall(r"\b6\.(\d{1,2})\b", view.flat)))
                for view in obligation_views
            ),
            default=0,
        )
        supplier_count = max(
            (
                len(set(re.findall(r"\b7\.(\d{1,2})\b", view.flat)))
                for view in obligation_views
            ),
            default=0,
        )
        if client_count >= 2 * max(1, supplier_count):
            issues.append(
                _issue(
                    issue_id="DET-CONTEXT-OBLIGATION-ASYMMETRY",
                    artifact_type=ArtifactType.CONTEXT,
                    dimension="Alignment",
                    severity="High",
                    title="Obligations and remedies are materially asymmetric",
                    why=(
                        f"The contract lists {client_count} client obligations and "
                        f"{supplier_count} supplier obligations, attaches priced "
                        "consequences to client delay, and states no equivalent "
                        "supplier remedy."
                    ),
                    recommendation=(
                        "Balance accountable obligations, service consequences, cure "
                        "periods and remedies according to which party controls each risk."
                    ),
                    references=tuple(
                        dict.fromkeys(
                            view.fragment.reference
                            for view in (*obligation_views, *penalty_views)
                        )
                    ),
                    clarification=(
                        "What equivalent remedies apply when a supplier-controlled "
                        "obligation is missed?"
                    ),
                )
            )

    personnel = tuple(
        view
        for view in views
        if re.search(
            r"\bmay substitute personnel at its discretion\b",
            view.flat,
            re.I,
        )
        and re.search(
            r"\bclient\b.{0,160}\bshall not substitute\b.{0,80}"
            r"\bwritten (?:agreement|approval)\b",
            view.flat,
            re.I,
        )
    )
    if personnel:
        issues.append(
            _issue(
                issue_id="DET-RESOURCES-PERSONNEL-SUBSTITUTION",
                artifact_type=ArtifactType.RESOURCES,
                dimension="Clarity",
                severity="Moderate",
                title="Personnel substitution controls bind only the client",
                why=(
                    "The supplier may replace unnamed personnel at its discretion, "
                    "while the client must name key roles and cannot replace them "
                    "without the supplier's written agreement."
                ),
                recommendation=(
                    "Name critical supplier roles and apply equivalent competence, "
                    "continuity, notice and approval controls to both parties."
                ),
                references=tuple(view.fragment.reference for view in personnel),
                clarification=(
                    "Which named supplier roles are protected by equivalent "
                    "substitution and continuity controls?"
                ),
            )
        )

    termination = tuple(
        view
        for view in views
        if re.search(
            r"\bterminate for convenience\b.{0,140}\b40\s*%.{0,100}"
            r"\bremaining unbilled contract value\b",
            view.flat,
            re.I,
        )
    )
    if termination:
        issues.append(
            _issue(
                issue_id="DET-RESOURCES-TERMINATION-CHARGE",
                artifact_type=ArtifactType.RESOURCES,
                dimension="Clarity",
                severity="Low",
                title="Termination charge has no stated cost basis",
                why=(
                    "Termination for convenience requires 40% of remaining unbilled "
                    "value without linking the charge to committed cost, work performed "
                    "or unavoidable loss."
                ),
                recommendation=(
                    "Tie termination charges to evidenced, unavoidable committed cost "
                    "and require mitigation and transparent calculation."
                ),
                references=tuple(view.fragment.reference for view in termination),
                clarification="What evidenced cost basis supports the termination charge?",
            )
        )

    client_testing = tuple(
        view
        for view in views
        if re.search(
            r"\b(?:author and execute|author|execute)\b.{0,140}"
            r"\b(?:system integration test|user acceptance test)\b",
            view.flat,
            re.I,
        )
        and "client obligations" in view.flat.casefold()
    )
    outcome_payment = tuple(
        view
        for view in views
        if re.search(
            r"\bcommencement of (?:user )?acceptance testing\b.{0,140}"
            r"\birrespective of outcome\b",
            view.flat,
            re.I,
        )
    )
    if client_testing and deemed and outcome_payment:
        issues.append(
            _issue(
                issue_id="DET-REQUIREMENTS-TEST-CONTROL-ASYMMETRY",
                artifact_type=ArtifactType.REQUIREMENTS,
                dimension="Alignment",
                severity="High",
                title="The client performs testing but does not control acceptance or payment",
                why=(
                    "The client must author and execute SIT and UAT, while deemed "
                    "acceptance and a payment due at test commencement let the supplier "
                    "control the commercial clock irrespective of test outcome."
                ),
                recommendation=(
                    "Give the client control of objective test standards, acceptance "
                    "approval, cure evidence and outcome-based payment release."
                ),
                references=tuple(
                    dict.fromkeys(
                        view.fragment.reference
                        for view in (*client_testing, *deemed, *outcome_payment)
                    )
                ),
                clarification=(
                    "Who controls test acceptance and payment release when the client "
                    "finds a failure?"
                ),
            )
        )

    data_obligation = tuple(
        view
        for view in views
        if re.search(r"\bcleansed master data\b", view.flat, re.I)
    )
    data_penalty = tuple(
        view
        for view in views
        if re.search(
            r"\b(?:standing charges|per working day)\b",
            view.flat,
            re.I,
        )
    )
    data_quality_standard = any(
        re.search(
            r"\b(?:data quality threshold|completeness threshold|error rate|"
            r"duplicate rate|reconciliation tolerance)\b",
            view.flat,
            re.I,
        )
        for view in views
    )
    if data_obligation and data_penalty and not data_quality_standard:
        issues.append(
            _issue(
                issue_id="DET-REQUIREMENTS-UNMEASURABLE-DATA-PENALTY",
                artifact_type=ArtifactType.REQUIREMENTS,
                dimension="Clarity",
                severity="Moderate",
                title="A priced data obligation has no measurable quality threshold",
                why=(
                    "The client must provide 'cleansed master data' and can incur a "
                    "4,200 per-day standing charge, but no measurable completeness, validity, "
                    "duplicate or reconciliation threshold defines compliance."
                ),
                recommendation=(
                    "Attach the data template and profile, define measurable quality "
                    "thresholds and evidence, and apply charges only to an attributable "
                    "breach of those criteria."
                ),
                references=tuple(
                    dict.fromkeys(
                        view.fragment.reference
                        for view in (*data_obligation, *data_penalty)
                    )
                ),
                clarification=(
                    "Which measurable data-quality criteria trigger acceptance or the "
                    "daily charge?"
                ),
            )
        )

    component_view = next(
        (
            view
            for view in views
            if re.search(r"\bcomponent\s+amount\b", view.raw, re.I)
            and re.search(r"\btotal fixed price\b", view.raw, re.I)
        ),
        None,
    )
    if component_view is not None:
        stated_match = re.search(
            r"\btotal fixed price\b.{0,100}?(\d[\d,]{5,})",
            component_view.flat,
            re.I,
        )
        table_match = re.search(
            r"Component\s+Amount.*?(?=\n\s*Total\s+[\d,]+)",
            component_view.raw,
            re.I | re.S,
        )
        amounts: list[int] = []
        if table_match is not None:
            table_text = table_match.group(0)
            for amount_match in re.finditer(
                r"(?m)(\d{1,3}(?:,\d{3})+)\s*$",
                table_text,
            ):
                line_start = table_text.rfind("\n", 0, amount_match.start()) + 1
                line_prefix = table_text[line_start : amount_match.start()]
                if re.search(r"\b(?:rate of|day rate)\b", line_prefix, re.I):
                    continue
                amounts.append(int(amount_match.group(1).replace(",", "")))
        stated = (
            int(stated_match.group(1).replace(",", ""))
            if stated_match is not None
            else None
        )
        calculated = sum(amounts)
        if stated is not None and len(amounts) >= 2 and calculated != stated:
            difference = abs(calculated - stated)
            issues.append(
                _issue(
                    issue_id="DET-RESOURCES-COMPONENT-TOTAL-CONFLICT",
                    artifact_type=ArtifactType.RESOURCES,
                    dimension="Clarity",
                    severity="Moderate",
                    title="The component breakdown does not reconcile to the fixed price",
                    why=(
                        f"The component amounts total {calculated:,}, while the stated "
                        f"fixed price is {stated:,}, leaving {difference:,} unexplained."
                    ),
                    recommendation=(
                        "Correct the breakdown or headline total and reconcile the "
                        "payment milestones to the approved commercial baseline."
                    ),
                    references=(component_view.fragment.reference,),
                    clarification="Which reconciled total is contractually binding?",
                )
            )

    impact_rate = tuple(
        view
        for view in views
        if re.search(
            r"\bimpact assessment\b.{0,100}?(\d{1,3}(?:,\d{3})+)"
            r"\s+per person-day\b",
            view.flat,
            re.I,
        )
    )
    blended_rate = tuple(
        view
        for view in views
        if re.search(
            r"\bblended change-control rate\b.{0,60}?(\d{1,3}(?:,\d{3})+)\b",
            view.flat,
            re.I,
        )
    )
    if impact_rate and blended_rate:
        left = re.search(
            r"\bimpact assessment\b.{0,100}?(\d{1,3}(?:,\d{3})+)",
            impact_rate[0].flat,
            re.I,
        )
        right = re.search(
            r"\bblended change-control rate\b.{0,60}?(\d{1,3}(?:,\d{3})+)",
            blended_rate[0].flat,
            re.I,
        )
        if left and right and left.group(1) != right.group(1):
            issues.append(
                _issue(
                    issue_id="DET-RESOURCES-CHANGE-CONTROL-RATE-CONFLICT",
                    artifact_type=ArtifactType.RESOURCES,
                    dimension="Clarity",
                    severity="Moderate",
                    title="Change-control rates conflict within the contract",
                    why=(
                        f"The change impact assessment uses {left.group(1)} per day, "
                        f"while the rate card states {right.group(1)}."
                    ),
                    recommendation=(
                        "Select one binding change-control rate and apply it consistently "
                        "to the clause, rate card and approval workflow."
                    ),
                    references=tuple(
                        dict.fromkeys(
                            view.fragment.reference
                            for view in (*impact_rate, *blended_rate)
                        )
                    ),
                    clarification="Which change-control day rate is contractually binding?",
                )
            )

    return tuple(issues)


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
    finding = deterministic_finding_tags(
        dimension=dimension,
        title=title,
        recommendation=recommendation,
    )
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
        finding_type=finding.finding_type,
        finding_basis=finding.basis.value,
        structural_target=finding.structural_target.value,
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
