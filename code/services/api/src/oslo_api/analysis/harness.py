import re
from typing import Protocol

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
        ArtifactType.CONTEXT: "Context",
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
            part.strip()
            for part in re.split(r"(?<=[.!?])\s+", combined)
            if part.strip()
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
                f"{depth} evidence contains conflicting budgets: "
                f"{self._human_list(budgets)}."
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
                    or (
                        f"{depth} evidence-qualified "
                        f"{self._titles[artifact_type].lower()}."
                    ),
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
                    leading_indicator=(
                        "Evidence that the stated outcome is materializing"
                    ),
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
        ) -> None:
            refs = tuple(
                item.reference
                for item in perception.evidence
                if any(term.lower() in item.content.lower() for term in terms)
            )[:5]
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
                )
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
            ),
        )
