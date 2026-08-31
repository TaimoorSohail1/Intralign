import re
from typing import Protocol

from oslo_api.analysis.load_bearing import deterministic_finding_tags
from oslo_api.analysis.models import (
    ARTIFACT_TYPES,
    Artifact,
    ArtifactSection,
    ArtifactType,
    Assessment,
    EvidenceFragment,
    HarnessCallMetadata,
    HarnessInvocation,
    Issue,
    OutcomeCheckpoint,
    Perception,
    RunKind,
)
from oslo_api.analysis.structured_extraction import construct_structured_artifact

DETERMINISTIC_HARNESS_VERSION = "oslo-deterministic-v1"


class AgentHarnessError(RuntimeError):
    def __init__(self, code: str, *, retryable: bool = False) -> None:
        super().__init__(code)
        self.code = code
        self.retryable = retryable


class AgentHarness(Protocol):
    def perceive(
        self,
        *,
        description: str,
        source_names: tuple[str, ...],
        evidence: tuple[EvidenceFragment, ...],
        kind: RunKind,
        invocation: HarnessInvocation | None = None,
    ) -> Perception: ...

    def construct(
        self,
        *,
        perception: Perception,
        kind: RunKind,
        invocation: HarnessInvocation | None = None,
    ) -> tuple[Artifact, ...]: ...

    def construct_artifact(
        self,
        *,
        perception: Perception,
        artifact_type: ArtifactType,
        kind: RunKind,
        invocation: HarnessInvocation | None = None,
    ) -> Artifact: ...

    def evaluate(
        self,
        *,
        artifacts: tuple[Artifact, ...],
        perception: Perception,
        kind: RunKind,
        context: str = "",
        invocation: HarnessInvocation | None = None,
    ) -> Assessment: ...


class DeterministicAgentHarness:
    """Stable development/evaluation harness used before a live model is enabled."""

    _titles = {
        ArtifactType.INTENT: "Intent",
        # ``context`` remains the persisted enum for backwards compatibility,
        # but Release 2 presents this artifact as the user's explicit constraints.
        ArtifactType.CONTEXT: "Constraints",
        ArtifactType.SCOPE: "Scope",
        ArtifactType.REQUIREMENTS: "Requirements",
        ArtifactType.WORK_BREAKDOWN: "Work breakdown",
        ArtifactType.SCHEDULE: "Schedule",
        ArtifactType.RESOURCES: "Resources",
    }

    def perceive(
        self,
        *,
        description: str,
        source_names: tuple[str, ...],
        evidence: tuple[EvidenceFragment, ...] = (),
        kind: RunKind,
        invocation: HarnessInvocation | None = None,
    ) -> Perception:
        supplied = list(evidence)
        normalized = " ".join(description.split())
        if normalized:
            supplied.insert(
                0,
                EvidenceFragment(reference="description:1", content=normalized),
            )
        evidence_refs = tuple(item.reference for item in supplied) or tuple(
            f"source:{index + 1}:{name}" for index, name in enumerate(source_names)
        )
        combined = " ".join(item.content for item in supplied)
        facts = tuple(
            part.strip() for part in re.split(r"(?<=[.!?])\s+", combined) if part.strip()
        )[:30]
        result = Perception(
            facts=facts or (normalized or "Document evidence supplied.",),
            claims=(
                "The project has a defined outcome and delivery context.",
                "Delivery depends on evidence-qualified scope, schedule and resources.",
            ),
            gaps=(
                "Critical dependencies need confirmed owners.",
                "Resource and contingency assumptions need confirmation.",
            ),
            evidence_refs=evidence_refs,
            evidence=tuple(supplied),
        )
        self._record(invocation)
        return result

    def construct(
        self,
        *,
        perception: Perception,
        kind: RunKind,
        invocation: HarnessInvocation | None = None,
    ) -> tuple[Artifact, ...]:
        result = tuple(
            self.construct_artifact(
                perception=perception,
                artifact_type=artifact_type,
                kind=kind,
                invocation=None,
            )
            for artifact_type in ARTIFACT_TYPES
        )
        self._record(invocation)
        return result

    def construct_artifact(
        self,
        *,
        perception: Perception,
        artifact_type: ArtifactType,
        kind: RunKind,
        invocation: HarnessInvocation | None = None,
    ) -> Artifact:
        depth = "Extended" if kind is RunKind.EXTENDED else "Initial"
        structured = construct_structured_artifact(
            perception=perception,
            artifact_type=artifact_type,
            title=self._titles[artifact_type],
            depth=depth,
        )
        if structured is not None:
            self._record(invocation)
            return structured
        if artifact_type is ArtifactType.WORK_BREAKDOWN:
            fallback_work_breakdown = self._fallback_work_breakdown(
                perception=perception,
                depth=depth,
            )
            if fallback_work_breakdown is not None:
                self._record(invocation)
                return fallback_work_breakdown
        evidence_text = " ".join(item.content for item in perception.evidence)
        timelines = self._timeline_values(evidence_text)
        budgets = self._budget_values(evidence_text)
        scope_terms = self._scope_terms(evidence_text)

        summaries = {
            ArtifactType.SCHEDULE: (
                f"{depth} evidence shows conflicting durations: "
                f"{self._human_list([f'{value} months' for value in timelines])}."
                if len(timelines) > 1
                else ""
            ),
            ArtifactType.RESOURCES: (
                f"{depth} evidence contains conflicting budgets: {self._human_list(budgets)}."
                if len(budgets) > 1
                else ""
            ),
            ArtifactType.SCOPE: (
                f"{depth} evidence contains unresolved scope boundaries across "
                f"{self._human_list(scope_terms)}."
                if len(scope_terms) > 1
                else ""
            ),
        }
        result = Artifact(
            artifact_type=artifact_type,
            title=self._titles[artifact_type],
            summary=summaries.get(artifact_type)
            or (
                f"{depth} evidence-qualified {self._titles[artifact_type].lower()} "
                f"derived from the submitted project information."
            ),
            reliability="Moderate",
            evidence_refs=perception.evidence_refs,
            sections=(
                ArtifactSection(
                    heading=self._titles[artifact_type],
                    body=summaries.get(artifact_type)
                    or (f"{depth} evidence-qualified {self._titles[artifact_type].lower()}."),
                    bullets=perception.facts[:20],
                    evidence_refs=perception.evidence_refs,
                ),
            ),
        )
        self._record(invocation)
        return result

    def evaluate(
        self,
        *,
        artifacts: tuple[Artifact, ...],
        perception: Perception,
        kind: RunKind,
        context: str = "",
        invocation: HarnessInvocation | None = None,
    ) -> Assessment:
        extended = kind is RunKind.EXTENDED
        text = " ".join(item.content for item in perception.evidence)
        issues = self._evidence_issues(text, perception)
        if not issues:
            issues = self._default_issues(perception)
        clarity = self._dimension_band(issues, "Clarity", default="High")
        alignment = self._dimension_band(issues, "Alignment", default="Moderate")
        feasibility = self._dimension_band(
            issues,
            "Feasibility",
            default="Low" if extended else "Very Low",
        )
        critical_count = sum(issue.severity == "Critical" for issue in issues)
        moderate_count = sum(issue.severity == "Moderate" for issue in issues)
        confidence = max(20, 82 - critical_count * 8 - moderate_count * 4)
        evidence_specific = bool(self._evidence_issues(text, perception))
        result = Assessment(
            confidence_index=confidence if evidence_specific else (62 if extended else 58),
            confidence_band="Low" if confidence < 50 and evidence_specific else "Moderate",
            reliability="Moderate" if perception.evidence else "Low",
            clarity=clarity,
            alignment=alignment,
            feasibility=feasibility,
            issues=issues,
            outcome_checkpoints=(
                OutcomeCheckpoint(
                    id="CHK-PROJECT-OUTCOME",
                    workstream="Project outcome",
                    leading_indicator=("Evidence that the stated outcome is materializing"),
                    timing="Before the final delivery commitment",
                    lever="Change scope, sequence, resources, or approach",
                    registered=False,
                ),
            ),
        )
        self._record(invocation)
        return result

    @staticmethod
    def _record(invocation: HarnessInvocation | None) -> None:
        if invocation is not None:
            invocation.metadata = HarnessCallMetadata(
                provider="deterministic",
                model=DETERMINISTIC_HARNESS_VERSION,
                prompt_version=DETERMINISTIC_HARNESS_VERSION,
            )

    @staticmethod
    def _timeline_values(text: str) -> list[str]:
        return sorted(set(re.findall(r"\b(\d{1,2})\s+months?\b", text, re.I)), key=int)

    @staticmethod
    def _budget_values(text: str) -> list[str]:
        values = set(re.findall(r"\$\s*(\d+(?:\.\d+)?)\s*([mk])\b", text, re.I))
        return sorted(f"${amount}{suffix.upper()}" for amount, suffix in values)

    @staticmethod
    def _scope_terms(text: str) -> list[str]:
        candidates = ("mobile app", "HR module", "HR portal", "inventory integration")
        return [term for term in candidates if term.lower() in text.lower()]

    @staticmethod
    def _human_list(values: list[str]) -> str:
        if len(values) < 2:
            return values[0] if values else ""
        return ", ".join(values[:-1]) + f" and {values[-1]}"

    @staticmethod
    def _fallback_work_breakdown(
        *,
        perception: Perception,
        depth: str,
    ) -> Artifact | None:
        """Retain a source-stated plan list as a real three-level WBS.

        The deterministic harness must not promote analysis-history prose into work.
        This adapter only expands an explicit ``plan X: verb A, B and C`` statement;
        if that source grammar is absent the normal evidence-qualified fallback remains.
        """

        audit_prefix = re.compile(
            r"^(?:(?:schedule|resources|intent|scope|requirements|constraints|"
            r"work breakdown) artifact changes confirmed by the user:|"
            r"section:|issue:|question:|answer:)",
            re.IGNORECASE,
        )
        candidate = next(
            (
                fact.strip().lstrip("-• ")
                for fact in perception.facts
                if ":" in fact and not audit_prefix.search(fact.strip().lstrip("-• "))
            ),
            None,
        )
        if candidate is None:
            return None

        package_name, detail = (part.strip() for part in candidate.split(":", 1))
        fragments = tuple(
            part.strip().rstrip(".;")
            for part in re.split(r"\s*,\s*|\s+and\s+", detail, flags=re.IGNORECASE)
            if part.strip().rstrip(".;")
        )
        if len(fragments) < 2:
            return None
        first = re.match(r"^([a-z]+)\s+(.+)$", fragments[0], re.IGNORECASE)
        if first is None:
            return None

        verb = first.group(1).lower()
        task_fragments = (first.group(2), *fragments[1:])

        def sentence_case(value: str) -> str:
            normalized = value.strip().rstrip(".;")
            return normalized[:1].upper() + normalized[1:] if normalized else normalized

        deliverable = sentence_case(
            re.sub(
                r"^(?:plan|deliver|run|build|create|implement)\s+(?:an?\s+|the\s+)?",
                "",
                package_name,
                flags=re.IGNORECASE,
            )
        )
        repeated_verb = re.compile(
            rf"^{re.escape(verb)}\s+",
            flags=re.IGNORECASE,
        )
        tasks = tuple(
            sentence_case(f"{verb} {repeated_verb.sub('', fragment)}")
            for fragment in task_fragments
        )
        if not deliverable or not all(tasks):
            return None

        evidence_refs = tuple(
            item.reference
            for item in perception.evidence
            if package_name.casefold() in item.content.casefold()
        ) or perception.evidence_refs[:1]
        rows = (("1.0", sentence_case(package_name)),) + tuple(
            (f"1.{index}", task) for index, task in enumerate(tasks, start=1)
        )
        section = ArtifactSection(
            heading=deliverable,
            columns=("WBS", "Item"),
            rows=rows,
            evidence_refs=evidence_refs,
            row_evidence_refs=tuple(evidence_refs for _ in rows),
            row_states=tuple("confirmed" for _ in rows),
        )
        return Artifact(
            artifact_type=ArtifactType.WORK_BREAKDOWN,
            title="Work breakdown",
            summary=(
                f"{depth} evidence-qualified work breakdown retained as "
                "deliverable, work package and tasks."
            ),
            reliability="Moderate",
            evidence_refs=evidence_refs,
            basis="source_grounded",
            sections=(section,),
        )

    def _evidence_issues(
        self,
        text: str,
        perception: Perception,
    ) -> tuple[Issue, ...]:
        timelines = self._timeline_values(text)
        budgets = self._budget_values(text)
        scope_terms = self._scope_terms(text)
        lowered = text.lower()
        issues: list[Issue] = []

        def add(
            issue_id: str,
            artifact_type: ArtifactType,
            dimension: str,
            severity: str,
            title: str,
            why: str,
            recommendation: str,
            terms: tuple[str, ...],
            clarification: str | None = None,
        ) -> None:
            refs = tuple(
                item.reference
                for item in perception.evidence
                if any(term.lower() in item.content.lower() for term in terms)
            )[:5]
            finding = deterministic_finding_tags(
                dimension=dimension,
                title=title,
                recommendation=recommendation,
            )
            issues.append(
                Issue(
                    id=issue_id,
                    artifact_type=artifact_type,
                    dimension=dimension,
                    severity=severity,
                    title=title,
                    why=why,
                    recommendation=recommendation,
                    evidence_refs=refs or perception.evidence_refs[:5],
                    clarification=clarification,
                    finding_type=finding.finding_type,
                    finding_basis=finding.basis.value,
                    structural_target=finding.structural_target.value,
                )
            )

        objective_gap = re.search(
            r"\b(OBJ-\d+)\b(?:(?!\bOBJ-\d+\b).){0,700}?"
            r"\b(\d+(?:\.\d+)?)\s+TBD definition\b",
            text,
            re.IGNORECASE,
        )
        if objective_gap:
            objective_id = objective_gap.group(1).upper()
            target = objective_gap.group(2)
            add(
                f"ISS-{objective_id}-MISSING-UNIT",
                ArtifactType.INTENT,
                "Clarity",
                "Moderate",
                f"{objective_id} target is missing a unit",
                f"The source records a target of {target}, but the measure definition is TBD.",
                "Define the unit, baseline, measurement window and accountable owner.",
                (objective_id, "TBD definition"),
                f"What unit and measurement window make the {objective_id} target testable?",
            )

        requirement_owner_gap = re.search(
            r"\b(REQ-\d+)\b(?:(?!\bREQ-\d+\b).){0,900}?\bTBD\b",
            text,
            re.IGNORECASE,
        )
        if requirement_owner_gap:
            requirement_id = requirement_owner_gap.group(1).upper()
            add(
                f"ISS-{requirement_id}-OWNER-TBD",
                ArtifactType.REQUIREMENTS,
                "Alignment",
                "Moderate",
                f"{requirement_id} has no accountable owner",
                "The requirement and its related SLA decision are assigned to TBD.",
                "Name the accountable owner and approve the missing SLA decision.",
                (requirement_id, "action owner is TBD"),
                f"Who owns {requirement_id}, and what SLA must they approve?",
            )

        if re.search(
            r"ParcelLink.{0,220}\b(?:Unconfirmed|not confirmed)\b",
            text,
            re.IGNORECASE,
        ):
            add(
                "ISS-PARCELLINK-ACCESS-UNCONFIRMED",
                ArtifactType.SCHEDULE,
                "Feasibility",
                "Critical",
                "ParcelLink access is unconfirmed",
                (
                    "Carrier-rate API access is needed by the plan, "
                    "but commercial access is unconfirmed."
                ),
                (
                    "Confirm commercial access, owner, evidence and a fallback "
                    "before the dependency date."
                ),
                ("ParcelLink", "Commercial access not confirmed"),
                "Who can confirm ParcelLink access, and what fallback applies if it is late?",
            )

        if re.search(
            r"Solution Architect.{0,220}\bNo named backup\b",
            text,
            re.IGNORECASE,
        ):
            add(
                "ISS-SOLUTION-ARCHITECT-BACKUP",
                ArtifactType.RESOURCES,
                "Feasibility",
                "Moderate",
                "Solution Architect has no named backup",
                "The resource plan names the architect but explicitly records no backup.",
                "Name a qualified delegate and define the handover trigger.",
                ("Solution Architect", "No named backup"),
                "Who is the qualified Solution Architect backup?",
            )

        if re.search(
            r"Integration Lead.{0,240}\b0\.5 FTE shortfall\b",
            text,
            re.IGNORECASE,
        ):
            add(
                "ISS-INTEGRATION-LEAD-CAPACITY",
                ArtifactType.RESOURCES,
                "Feasibility",
                "Critical",
                "Integration Lead has a 0.5 FTE shortfall",
                "The January resource plan is short by 0.5 FTE for the Integration Lead role.",
                "Fund or reallocate 0.5 FTE and confirm the January coverage plan.",
                ("Integration Lead", "0.5 FTE shortfall"),
                "What named resource closes the 0.5 FTE January shortfall?",
            )

        if re.search(
            r"(?:Two stewards required; one confirmed|"
            r"One data steward confirmed against two required)",
            text,
            re.IGNORECASE,
        ):
            add(
                "ISS-DATA-STEWARD-CAPACITY",
                ArtifactType.RESOURCES,
                "Feasibility",
                "Critical",
                "Required data-steward capacity is missing",
                "Only one of the two required data stewards is confirmed.",
                (
                    "Confirm the second data steward and their availability "
                    "before migration preparation."
                ),
                ("Two stewards required", "One data steward confirmed"),
                "Who is the second data steward, and when are they available?",
            )

        if re.search(
            r"Pen-test (?:vendor|supplier)(?: is)? not contracted",
            text,
            re.IGNORECASE,
        ):
            add(
                "ISS-PEN-TEST-VENDOR",
                ArtifactType.RESOURCES,
                "Feasibility",
                "Critical",
                "Pen-test vendor is not contracted",
                "Security exit depends on a penetration-test supplier that is not contracted.",
                "Contract the supplier and confirm the test window, owner and fallback.",
                ("Pen-test vendor not contracted", "Pen-test supplier is not contracted"),
                "Who owns the pen-test procurement, and what is the confirmed test window?",
            )

        if re.search(
            r"GBP\s*45,000 forecast variance\s+is not approved",
            text,
            re.IGNORECASE,
        ):
            add(
                "ISS-FORECAST-VARIANCE-UNAPPROVED",
                ArtifactType.RESOURCES,
                "Alignment",
                "Critical",
                "GBP 45,000 forecast variance is not approved",
                (
                    "The forecast is GBP 1,845,000 against a GBP 1,800,000 ceiling, "
                    "and the GBP 45,000 variance is not approved."
                ),
                (
                    "Obtain the governed funding decision or reduce the forecast "
                    "to the approved ceiling."
                ),
                ("GBP 45,000 forecast variance", "Forecast exceeds approved ceiling"),
                (
                    "Which authority approves the GBP 45,000 variance, "
                    "and what evidence records that decision?"
                ),
            )

        if len(timelines) > 1:
            add(
                "ISS-TIMELINE-CONFLICT",
                ArtifactType.SCHEDULE,
                "Alignment",
                "Critical",
                "Conflicting project timelines",
                f"The evidence states {self._human_list([f'{v} months' for v in timelines])}.",
                "Approve one baseline duration and reconcile every milestone against it.",
                tuple(f"{value} months" for value in timelines),
            )
        if len(budgets) > 1:
            add(
                "ISS-BUDGET-CONFLICT",
                ArtifactType.RESOURCES,
                "Alignment",
                "Critical",
                "Conflicting project budgets",
                f"The evidence contains {self._human_list(budgets)} as competing budgets.",
                "Select an approved budget baseline and identify its accountable owner.",
                tuple(budgets),
            )
        if len(scope_terms) > 1 and re.search(
            r"\b(ambiguous|inconsistent|included|excluded|unclear)\b", lowered
        ):
            add(
                "ISS-SCOPE-AMBIGUOUS",
                ArtifactType.SCOPE,
                "Clarity",
                "Critical",
                "Project scope is ambiguous",
                f"Scope boundaries conflict across {self._human_list(scope_terms)}.",
                "Publish one in-scope/out-of-scope baseline and obtain stakeholder approval.",
                tuple(scope_terms),
            )
        if re.search(
            r"success (?:metrics|measures).{0,50}(?:not defined|missing|unknown)",
            lowered,
        ):
            add(
                "ISS-SUCCESS-METRICS",
                ArtifactType.REQUIREMENTS,
                "Clarity",
                "Critical",
                "Success metrics are missing",
                "The evidence explicitly states that success measures are not defined.",
                "Define measurable outcomes, baselines, targets and accountable owners.",
                ("success metrics", "success measures"),
            )
        if (
            "production deployment" in lowered
            and "regulatory approval" in lowered
            and re.search(r"(not included|pending|requires)", lowered)
        ):
            add(
                "ISS-DEPLOYMENT-REGULATORY",
                ArtifactType.SCHEDULE,
                "Feasibility",
                "Critical",
                "Deployment depends on unresolved regulatory approval",
                "Regulatory approval is required but is not reconciled with the delivery plan.",
                "Add the regulatory review, owner, lead time and release contingency.",
                ("production deployment", "regulatory approval"),
            )
        if re.search(
            r"(?:resource allocations?.{0,40}(?:conflict|inconsistent)|"
            r"conflicting resource plan)",
            lowered,
        ):
            add(
                "ISS-RESOURCE-CONFLICT",
                ArtifactType.RESOURCES,
                "Feasibility",
                "Critical",
                "Resource allocations conflict",
                "The supplied resource assumptions are inconsistent.",
                "Reconcile capacity by role, period and accountable delivery owner.",
                ("resource allocation", "conflicting resource plan"),
            )
        if re.search(
            r"(?:final )?vendor(?: selection)?.{0,30}(?:undecided|unresolved|pending)",
            lowered,
        ):
            add(
                "ISS-VENDOR-UNRESOLVED",
                ArtifactType.RESOURCES,
                "Feasibility",
                "Moderate",
                "Vendor selection is unresolved",
                "The delivery plan depends on a vendor that has not been selected.",
                "Set vendor decision criteria, owner and decision deadline.",
                ("vendor",),
            )
        if re.search(r"migration volume.{0,20}(?:unknown|unconfirmed|tbd)", lowered):
            add(
                "ISS-MIGRATION-UNKNOWN",
                ArtifactType.REQUIREMENTS,
                "Feasibility",
                "Critical",
                "Migration volume is unknown",
                "Migration size is unknown, so duration and capacity cannot be validated.",
                "Measure source volumes and run a representative migration rehearsal.",
                ("migration volume",),
            )
        return tuple(issues)

    @staticmethod
    def _dimension_band(
        issues: tuple[Issue, ...],
        dimension: str,
        *,
        default: str,
    ) -> str:
        relevant = [issue for issue in issues if issue.dimension == dimension]
        if any(issue.severity == "Critical" for issue in relevant):
            return "Low"
        if relevant:
            return "Moderate"
        return default

    @staticmethod
    def _default_issues(perception: Perception) -> tuple[Issue, ...]:
        capacity = deterministic_finding_tags(
            dimension="Feasibility",
            title="Critical delivery capacity is not confirmed",
            recommendation="Confirm the accountable owner and a tested contingency.",
        )
        milestones = deterministic_finding_tags(
            dimension="Alignment",
            title="Milestones are not fully reconciled",
            recommendation="Reconcile the milestone sequence with responsible owners.",
        )
        return (
            Issue(
                id="ISS-001",
                artifact_type=ArtifactType.RESOURCES,
                dimension="Feasibility",
                severity="Critical",
                title="Critical delivery capacity is not confirmed",
                why="The available evidence does not confirm ownership or contingency capacity.",
                recommendation="Confirm the accountable owner and a tested contingency.",
                evidence_refs=perception.evidence_refs,
                clarification="Who owns the critical dependency, and what is the fallback?",
                finding_type=capacity.finding_type,
                finding_basis=capacity.basis.value,
                structural_target=capacity.structural_target.value,
            ),
            Issue(
                id="ISS-002",
                artifact_type=ArtifactType.SCHEDULE,
                dimension="Alignment",
                severity="Moderate",
                title="Milestones are not fully reconciled",
                why="The schedule lacks evidence that dependent milestones agree.",
                recommendation="Reconcile the milestone sequence with responsible owners.",
                evidence_refs=perception.evidence_refs,
                finding_type=milestones.finding_type,
                finding_basis=milestones.basis.value,
                structural_target=milestones.structural_target.value,
            ),
        )
