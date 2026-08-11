import json
import logging
import re
from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from time import monotonic, sleep
from typing import Annotated, Any, Literal

from openai import OpenAI
from pydantic import BaseModel, ConfigDict, Field, model_validator

from oslo_api.analysis.harness import AgentHarnessError
from oslo_api.analysis.models import (
    ARTIFACT_TYPES,
    Artifact,
    ArtifactAssumption,
    ArtifactConflict,
    ArtifactSection,
    ArtifactType,
    Assessment,
    ClaimKind,
    EvidenceFragment,
    HarnessCallMetadata,
    HarnessInvocation,
    Issue,
    Perception,
    RunKind,
)

_LOGGER = logging.getLogger(__name__)

PROMPT_VERSIONS = {
    "perceive": "oslo-perceive-v5",
    "construct": "oslo-construct-v5",
    "evaluate": "oslo-evaluate-v9",
}
ShortText = Annotated[str, Field(min_length=1, max_length=1_000)]
LongText = Annotated[str, Field(min_length=1, max_length=4_000)]
OptionalText = Annotated[str, Field(max_length=4_000)]
EvidenceReference = Annotated[str, Field(min_length=1, max_length=300)]
RatingBand = Literal["Very Low", "Low", "Moderate", "High"]
ReliabilityBand = Literal["Low", "Moderate", "High"]
EvidenceState = Literal["confirmed", "inferred", "conflicting", "unknown"]


class _StrictOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _PerceptionOutput(_StrictOutput):
    facts: list[ShortText] = Field(min_length=1, max_length=120)
    claims: list[ShortText] = Field(max_length=120)
    gaps: list[ShortText] = Field(max_length=120)
    evidence_refs: list[EvidenceReference] = Field(min_length=1, max_length=250)


class _ArtifactSectionOutput(_StrictOutput):
    heading: ShortText
    body: OptionalText = ""
    bullets: list[ShortText] = Field(default_factory=list, max_length=80)
    columns: list[ShortText] = Field(default_factory=list, max_length=20)
    rows: list[list[ShortText]] = Field(default_factory=list, max_length=120)
    evidence_refs: list[EvidenceReference] = Field(default_factory=list, max_length=100)
    row_evidence_refs: list[list[EvidenceReference]] = Field(
        default_factory=list,
        max_length=120,
    )
    row_states: list[EvidenceState] = Field(default_factory=list, max_length=120)

    @model_validator(mode="after")
    def validate_shape(self) -> "_ArtifactSectionOutput":
        if self.rows and not self.columns:
            raise ValueError("Structured artifact rows require columns")
        if any(len(row) != len(self.columns) for row in self.rows):
            raise ValueError("Structured artifact rows must match the column count")
        if self.rows and len(self.row_evidence_refs) != len(self.rows):
            raise ValueError("Each structured row requires its own evidence reference list")
        if self.rows and len(self.row_states) != len(self.rows):
            raise ValueError("Each structured row requires its own evidence state")
        if any(
            state == "confirmed" and not references
            for state, references in zip(
                self.row_states,
                self.row_evidence_refs,
                strict=True,
            )
        ):
            raise ValueError("Confirmed structured rows require source evidence")
        if not self.body.strip() and not self.bullets and not self.rows:
            raise ValueError("Artifact sections cannot be empty")
        return self


class _AssumptionOutput(_StrictOutput):
    id: Annotated[str, Field(min_length=1, max_length=100, pattern=r"^[A-Z0-9_-]+$")]
    statement: ShortText
    state: Literal["confirmed", "inferred", "conflicting"]
    load_bearing: bool
    evidence_refs: list[EvidenceReference] = Field(default_factory=list, max_length=20)


class _ConflictOutput(_StrictOutput):
    id: Annotated[str, Field(min_length=1, max_length=100, pattern=r"^[A-Z0-9_-]+$")]
    field: ShortText
    values: list[ShortText] = Field(min_length=2, max_length=20)
    evidence_refs: list[EvidenceReference] = Field(min_length=2, max_length=40)


class _ArtifactOutput(_StrictOutput):
    artifact_type: ArtifactType
    title: ShortText
    summary: LongText
    reliability: ReliabilityBand
    evidence_refs: list[EvidenceReference] = Field(min_length=1, max_length=50)
    basis: Literal["supported", "derived", "inferred"] = "derived"
    sections: list[_ArtifactSectionOutput] = Field(min_length=1, max_length=8)
    assumptions: list[_AssumptionOutput] = Field(default_factory=list, max_length=24)
    conflicts: list[_ConflictOutput] = Field(default_factory=list, max_length=24)


class _ArtifactsOutput(_StrictOutput):
    project_title: ShortText | None = None
    project_title_confidence: Literal["low", "moderate", "high"] = "low"
    artifacts: list[_ArtifactOutput] = Field(min_length=7, max_length=7)


class _SingleArtifactOutput(_StrictOutput):
    project_title: ShortText | None = None
    project_title_confidence: Literal["low", "moderate", "high"] = "low"
    artifact: _ArtifactOutput


class _IssueOutput(_StrictOutput):
    id: Annotated[str, Field(min_length=1, max_length=100, pattern=r"^[A-Z0-9_-]+$")]
    artifact_type: ArtifactType
    dimension: Literal["Clarity", "Alignment", "Feasibility"]
    severity: Literal["Warning", "Moderate", "Critical"]
    finding_type: Literal[
        "contradiction",
        "absence",
        "feasibility",
        "traceability",
        "clarity",
    ]
    exception_checked: bool
    title: ShortText
    why: LongText
    recommendation: LongText
    evidence_refs: list[EvidenceReference] = Field(min_length=1, max_length=20)
    clarification: ShortText | None = None
    status: Literal["open", "addressed", "resolved"] = "open"


class _CoverageAuditOutput(_StrictOutput):
    artifact_type: ArtifactType
    completeness: Literal["complete", "partial", "missing"]
    checked_controls: list[ShortText] = Field(min_length=2, max_length=30)
    missing_controls: list[ShortText] = Field(default_factory=list, max_length=30)


class _AssessmentOutput(_StrictOutput):
    confidence_index: int = Field(ge=0, le=100)
    confidence_band: RatingBand
    reliability: ReliabilityBand
    clarity: RatingBand
    alignment: RatingBand
    feasibility: RatingBand
    coverage_audit: list[_CoverageAuditOutput] = Field(min_length=7, max_length=7)
    issues: list[_IssueOutput] = Field(max_length=60)

    @model_validator(mode="after")
    def complete_coverage_audit(self) -> "_AssessmentOutput":
        if tuple(item.artifact_type for item in self.coverage_audit) != ARTIFACT_TYPES:
            raise ValueError("Coverage audit must contain all seven artifacts in order")
        return self


class OpenAIAgentHarness:
    """Three governed, schema-bound model calls inside the OSLO harness boundary."""

    def __init__(
        self,
        *,
        api_key: str,
        model: str | None = None,
        fast_model: str | None = None,
        extended_model: str | None = None,
        fallback_model: str | None = None,
        timeout_seconds: float = 30,
        client: Any | None = None,
        sleeper=sleep,
        max_retries: int = 1,
    ) -> None:
        self._client = client or OpenAI(
            api_key=api_key,
            timeout=timeout_seconds,
            max_retries=0,
        )
        selected_fast_model = fast_model or model
        if not selected_fast_model:
            raise ValueError("OPENAI_FAST_MODEL_REQUIRED")
        self._fast_model = selected_fast_model
        self._extended_model = extended_model or selected_fast_model
        self._fallback_model = fallback_model
        self._sleeper = sleeper
        self._max_retries = max(0, max_retries)

    def perceive(
        self,
        *,
        description: str,
        source_names: tuple[str, ...],
        evidence: tuple[EvidenceFragment, ...] = (),
        kind: RunKind,
        invocation: HarnessInvocation | None = None,
    ) -> Perception:
        selected_evidence = self._select_evidence(evidence, kind=kind)
        allowed_locators = self._allowed_evidence_refs(
            description=description,
            source_names=source_names,
            evidence=selected_evidence,
        )
        allowed_refs = set(allowed_locators)
        output = self._call_with_evidence_contract(
            name="oslo_perception",
            schema=_PerceptionOutput,
            max_output_tokens=8_000 if kind is RunKind.EXTENDED else 6_000,
            kind=kind,
            prompt_version=PROMPT_VERSIONS["perceive"],
            system=(
                f"You are OSLO Perceive ({PROMPT_VERSIONS['perceive']}). "
                "Extract only supported facts, "
                "claims and gaps. Never invent evidence. Every item must cite a supplied "
                "evidence locator copied exactly from allowed_evidence_locators; never "
                "reconstruct or alter page or fragment numbers. Be concise and consolidate "
                "duplicate findings without dropping distinct requirements, milestones, "
                "stakeholders, resources, decisions, assumptions, exclusions, or table rows. "
                "Keep diagnosed problems and causes separate from proposed interventions, "
                "features and success measures so later stages can test whether the solution "
                "actually addresses the problem. Preserve requirement modality exactly: "
                "labelled requirements and shall/must obligations are different from descriptive "
                "feature prose, targets or ideas. "
                "Return only the required JSON contract."
            ),
            payload={
                "analysis_kind": kind.value,
                "description": description,
                "source_names": source_names,
                "evidence": selected_evidence,
                "allowed_evidence_locators": allowed_locators,
            },
            invocation=invocation,
            allowed_refs=allowed_refs,
            evidence_refs=lambda result: result.evidence_refs,
        )
        return Perception(
            facts=tuple(output.facts),
            claims=tuple(output.claims),
            gaps=tuple(output.gaps),
            evidence_refs=tuple(output.evidence_refs),
            evidence=selected_evidence,
        )

    def construct(
        self,
        *,
        perception: Perception,
        kind: RunKind,
        invocation: HarnessInvocation | None = None,
    ) -> tuple[Artifact, ...]:
        """Compatibility API for callers outside the durable workflow.

        Production workflow execution calls ``construct_artifact`` directly so
        every artifact has an independent durable checkpoint.
        """
        if sum(len(item.content) for item in perception.evidence) > 16_000:
            return self._construct_sharded(
                perception=perception,
                kind=kind,
                invocation=invocation,
            )
        allowed_refs = self._perception_evidence_refs(perception)
        output = self._call_with_evidence_contract(
            name="oslo_artifacts",
            schema=_ArtifactsOutput,
            max_output_tokens=24_000,
            kind=kind,
            prompt_version=PROMPT_VERSIONS["construct"],
            system=(
                f"You are OSLO Construct ({PROMPT_VERSIONS['construct']}). "
                "Build exactly seven complete, structured artifacts in this exact "
                "order: intent, context, scope, requirements, work_breakdown, "
                "schedule, resources. Preserve every distinct source row and use "
                "separate sections for objectives, measures, stakeholders, "
                "governance, scope, requirements, acceptance criteria, work "
                "packages, milestones, resources, vendors and RACI assignments. "
                "Mark rows confirmed, inferred, conflicting or unknown. Confirmed "
                "means directly stated. Do not convert features or KPIs into formal "
                "requirements unless the source explicitly uses obligation language. "
                "Create one conflict per independently actionable subject and do not "
                "repeat project-wide conflicts across all seven artifacts. Use unknown "
                "for missing values. Every citation must be copied exactly from "
                "allowed_evidence_locators. Return JSON only."
            ),
            payload={
                "analysis_kind": kind.value,
                "perception": perception,
                "allowed_evidence_locators": sorted(allowed_refs),
            },
            invocation=invocation,
            allowed_refs=allowed_refs,
            evidence_refs=self._artifact_output_evidence_refs,
        )
        project_title = (
            output.project_title.strip()
            if output.project_title_confidence == "high" and output.project_title
            else None
        )
        artifacts = tuple(
            self._artifact_from_output(item, project_title=project_title)
            for item in output.artifacts
        )
        if tuple(item.artifact_type for item in artifacts) != ARTIFACT_TYPES:
            raise AgentHarnessError("SEVEN_ARTIFACT_CONTRACT_FAILED")
        return artifacts

    def construct_artifact(
        self,
        *,
        perception: Perception,
        artifact_type: ArtifactType,
        kind: RunKind,
        invocation: HarnessInvocation | None = None,
    ) -> Artifact:
        evidence = self._evidence_for_artifact(
            perception,
            artifact_type,
            character_budget=18_000,
        )
        facts = self._items_for_artifact(perception.facts, artifact_type, maximum=24)
        claims = self._items_for_artifact(perception.claims, artifact_type, maximum=24)
        gaps = self._items_for_artifact(perception.gaps, artifact_type, maximum=24)
        title_candidate = self._supported_title_candidate(perception)
        allowed_refs = {item.reference for item in evidence}
        if "description:1" in perception.evidence_refs:
            allowed_refs.add("description:1")
        structured_claims = tuple(
            claim
            for claim in perception.structured_claims
            if claim.evidence_ref in allowed_refs and claim.kind is not ClaimKind.TEXT
        )
        structured_claim_ids = {claim.id for claim in structured_claims}
        claim_relations = tuple(
            relation
            for relation in perception.claim_relations
            if relation.source_claim_id in structured_claim_ids
            and relation.target_claim_id in structured_claim_ids
        )
        output = self._call_with_evidence_contract(
            name=f"oslo_artifact_{artifact_type.value}",
            schema=_SingleArtifactOutput,
            max_output_tokens=8_000,
            kind=kind,
            prompt_version=PROMPT_VERSIONS["construct"],
            system=(
                f"You are OSLO Construct ({PROMPT_VERSIONS['construct']}). "
                f"Build only the {artifact_type.value} artifact as complete structured "
                f"sections and rows. Required coverage: "
                f"{self._artifact_contract(artifact_type)}. "
                "Preserve the most decision-relevant distinct source rows, using no "
                "more than 8 sections and 80 rows in total. Mark each row confirmed, "
                "inferred, conflicting or unknown and attach exact row-level evidence. "
                "Confirmed means directly stated, not merely derived from cited prose. "
                "For requirements, do not convert features, KPIs or descriptive prose "
                "into formal requirements or acceptance criteria unless the source "
                "explicitly labels them or uses shall/must/required language. Use "
                "unknown for missing values and never invent them. Record explicit or "
                "necessary labelled assumptions and retain all conflicting values, but "
                "only when they directly belong to this artifact. Create one conflict "
                "object per independently actionable subject. Do not duplicate the same "
                "fact across prose, rows, assumptions and conflicts. Keep summaries and "
                "body copy concise. Use typed claims and relations as deterministic "
                "comparison aids while retaining exact source locators. Extract a project "
                "title only when selected evidence supports it. Every citation must be "
                "copied exactly from allowed_evidence_locators. Return only the required "
                "JSON contract."
            ),
            payload={
                "analysis_kind": kind.value,
                "artifact_type": artifact_type.value,
                "facts": facts,
                "claims": claims,
                "gaps": gaps,
                "structured_claims": structured_claims,
                "claim_relations": claim_relations,
                "supported_project_title_candidate": title_candidate,
                "output_limits": {
                    "sections": 8,
                    "rows_total": 80,
                    "assumptions": 24,
                    "conflicts": 24,
                },
                "evidence": evidence,
                "allowed_evidence_locators": sorted(allowed_refs),
            },
            invocation=invocation,
            allowed_refs=allowed_refs,
            evidence_refs=self._single_artifact_output_evidence_refs,
        )
        if output.artifact.artifact_type is not artifact_type:
            raise AgentHarnessError("ARTIFACT_TYPE_CONTRACT_FAILED", retryable=True)
        project_title = (
            output.project_title.strip()
            if output.project_title_confidence == "high" and output.project_title
            else title_candidate
        )
        return self._artifact_from_output(
            output.artifact,
            project_title=project_title,
        )

    def _construct_sharded(
        self,
        *,
        perception: Perception,
        kind: RunKind,
        invocation: HarnessInvocation | None,
    ) -> tuple[Artifact, ...]:
        """Build dense projects by artifact with bounded parallelism.

        The project intake is capped at ten documents. Sharding prevents one large
        structured response from timing out while keeping concurrency bounded.
        """

        def construct_one(artifact_type: ArtifactType):
            local_invocation = (
                HarnessInvocation(run_id=invocation.run_id, phase=invocation.phase)
                if invocation is not None
                else None
            )
            artifact = self.construct_artifact(
                perception=perception,
                artifact_type=artifact_type,
                kind=kind,
                invocation=local_invocation,
            )
            return (
                artifact_type,
                artifact,
                (local_invocation.metadata if local_invocation is not None else None),
            )

        results = {}
        metadata = None
        # Two concurrent structured calls keep useful parallelism without the
        # provider instability observed when three large schema-bound responses
        # were generated at once.
        with ThreadPoolExecutor(max_workers=2, thread_name_prefix="oslo-construct") as pool:
            for artifact_type, artifact, call_metadata in pool.map(
                construct_one,
                ARTIFACT_TYPES,
            ):
                results[artifact_type] = artifact
                metadata = self._merge_metadata(metadata, call_metadata)
        if invocation is not None:
            invocation.metadata = metadata

        project_title = next(
            (
                artifact.project_title
                for artifact in results.values()
                if artifact.project_title
            ),
            self._supported_title_candidate(perception),
        )
        return tuple(
            artifact
            if artifact.project_title or not project_title
            else replace(artifact, project_title=project_title)
            for artifact in (results[item] for item in ARTIFACT_TYPES)
        )

    @staticmethod
    def _artifact_from_output(
        item: _ArtifactOutput,
        *,
        project_title: str | None,
    ) -> Artifact:
        return Artifact(
            artifact_type=item.artifact_type,
            title=item.title,
            summary=item.summary,
            reliability=item.reliability,
            evidence_refs=tuple(item.evidence_refs),
            basis=item.basis,
            sections=tuple(
                ArtifactSection(
                    heading=section.heading,
                    body=section.body,
                    bullets=tuple(section.bullets),
                    columns=tuple(section.columns),
                    rows=tuple(tuple(row) for row in section.rows),
                    evidence_refs=tuple(section.evidence_refs),
                    row_evidence_refs=tuple(
                        tuple(references) for references in section.row_evidence_refs
                    ),
                    row_states=tuple(section.row_states),
                )
                for section in item.sections
            ),
            assumptions=tuple(
                ArtifactAssumption(
                    id=assumption.id,
                    statement=assumption.statement,
                    state=assumption.state,
                    load_bearing=assumption.load_bearing,
                    evidence_refs=tuple(assumption.evidence_refs),
                )
                for assumption in item.assumptions
            ),
            conflicts=tuple(
                ArtifactConflict(
                    id=conflict.id,
                    field=conflict.field,
                    values=tuple(conflict.values),
                    evidence_refs=tuple(conflict.evidence_refs),
                )
                for conflict in item.conflicts
            ),
            project_title=project_title,
        )

    def evaluate(
        self,
        *,
        artifacts: tuple[Artifact, ...],
        perception: Perception,
        kind: RunKind,
        context: str = "",
        invocation: HarnessInvocation | None = None,
    ) -> Assessment:
        allowed_refs = self._perception_evidence_refs(perception)
        clarification_context = self._clarification_context(context)
        output = self._call_with_evidence_contract(
            name="oslo_assessment",
            schema=_AssessmentOutput,
            max_output_tokens=12_000 if kind is RunKind.EXTENDED else 9_000,
            kind=kind,
            prompt_version=PROMPT_VERSIONS["evaluate"],
            system=(
                f"You are OSLO Evaluate ({PROMPT_VERSIONS['evaluate']}). "
                "Apply the approved clarity, "
                "alignment and feasibility rubric. Identify actionable, evidence-cited issues. "
                "Before scoring, build and test this trace chain: diagnosed problems and causes "
                "to objectives, objectives to scope interventions, interventions to explicit "
                "requirements and deliverables, and objectives to outcome measures. Create an "
                "Alignment finding when a material problem or objective has no intervention or "
                "outcome measure; displaying a problem is not the same as resolving it. Check "
                "whether budget, ownership, stakeholders and risks support the stated purpose, "
                "not merely whether delivery roles and totals exist. Do not reward document "
                "detail, complexity, dates, identifiers or citations as proof of alignment, "
                "feasibility or reliability. A clear document can describe an undeliverable plan. "
                "Reliability depends on whether evidence supports the proposed solution and "
                "cross-artifact relationships, not the number of citations. Confidence must be "
                "limited by the weakest material dimension and any open critical finding. "
                "When the evidence includes a USER_CLARIFICATION, mark the tied issue addressed "
                "if the answer improves it but leaves a material gap, and resolved only when the "
                "answer fully satisfies the clarification. Treat a direct user answer as "
                "authoritative user-confirmed project evidence; do not require a separate "
                "document unless the user says the answer is unverified. Never leave a "
                "confirmation-type issue open only because independent source documents are "
                "absent: a clear answer that names the decision, owner, date, threshold, or "
                "fallback requested by the question is sufficient user-confirmed evidence. "
                "Reuse the exact "
                "Issue ID supplied inside USER_CLARIFICATION for that tied issue. "
                "For every open issue, include one concise clarification question whose answer "
                "would materially reduce the stated uncertainty. Consolidate duplicate issues "
                "only when they have the same root cause and corrective decision. Keep separate "
                "issues when different values, approvals or owners can be corrected "
                "independently, even if they appear in the same documents. Keep explanations "
                "concise. Before findings, complete the seven-artifact "
                "coverage audit. For every control material to the actual project, test "
                "problem-to-solution alignment; beneficiary and operational stakeholder "
                "representation. Calibrate control expectations to evidenced delivery scale, "
                "staff count, budget, regulatory and safety exposure, and procurement "
                "complexity. For a small owner-led business, do not require enterprise "
                "governance such as a steering committee, project board, RACI, formal risk "
                "register or formal change-control bureaucracy unless the project's actual "
                "consequences or source evidence imply that control. Continue the audit for "
                "formal requirements versus feature prose; acceptance and "
                "testing; privacy, safety, accessibility and regulatory assurance; staffing "
                "and capacity; dependencies, procurement, supplier exit and fallback; change, "
                "adoption and communications; benefit baselines, attribution and measurement "
                "timing; options appraisal; and evidence currency and citation. Do not require "
                "a control that the project's content and consequences do not imply. Preserve "
                "distinct material findings even when there are more than twenty. Run both "
                "comparison checks for contradictory values and absence checks for required "
                "owners, dates, thresholds, dependencies, controls, registers and decisions "
                "implied by the project. Check predecessor and prerequisite dates, overlapping "
                "use of constrained resources, capacity and FTE arithmetic, currencies and "
                "units, benefit double-counting, and whether a claimed baseline or source was "
                "available at the stated time. Absence findings must cite the "
                "nearest evidence that establishes the relevant plan area. For each candidate "
                "finding, actively check whether the source documents a rationale, approved "
                "exception, change-control rule, dual sign-off, estimate, exclusion or later "
                "measurement period; suppress the finding when that documented exception makes "
                "it valid. Complexity alone is never a defect. Do not expose hidden "
                "reasoning. Every evidence_refs value must be copied exactly from "
                "allowed_evidence_locators; never reconstruct or alter a locator. "
                "Return only the required JSON contract."
            ),
            payload={
                "analysis_kind": kind.value,
                "perception": perception,
                "artifacts": artifacts,
                "clarification_context": clarification_context,
                "allowed_evidence_locators": sorted(allowed_refs),
            },
            invocation=invocation,
            allowed_refs=allowed_refs,
            evidence_refs=lambda result: (
                reference for issue in result.issues for reference in issue.evidence_refs
            ),
        )
        return Assessment(
            confidence_index=output.confidence_index,
            confidence_band=output.confidence_band,
            reliability=output.reliability,
            clarity=output.clarity,
            alignment=output.alignment,
            feasibility=output.feasibility,
            issues=tuple(
                Issue(
                    id=item.id,
                    artifact_type=item.artifact_type,
                    dimension=item.dimension,
                    severity=item.severity,
                    title=item.title,
                    why=item.why,
                    recommendation=item.recommendation,
                    evidence_refs=tuple(item.evidence_refs),
                    clarification=item.clarification,
                    status=item.status,
                )
                for item in output.issues
            ),
        )

    @staticmethod
    def _clarification_context(context: str) -> dict[str, str] | None:
        matches = list(
            re.finditer(
                r"^USER_CLARIFICATION[^\n]*\n(?P<body>.*?)"
                r"(?:^END_USER_CLARIFICATION\s*$|\Z)",
                context,
                re.MULTILINE | re.DOTALL,
            )
        )
        if not matches:
            return None
        block = matches[-1].group("body")
        issue = re.search(r"^Issue ID:\s*(\S+)\s*$", block, re.MULTILINE)
        question = re.search(r"^Question:\s*(.+?)\s*$", block, re.MULTILINE)
        answer = re.search(r"^Answer:\s*(.+)\Z", block, re.MULTILINE | re.DOTALL)
        if not issue or not answer:
            return None
        return {
            "issue_id": issue.group(1).strip(),
            "question": question.group(1).strip() if question else "Clarification requested",
            "answer": answer.group(1).strip(),
        }

    def _call_with_evidence_contract(
        self,
        *,
        name: str,
        schema: type[BaseModel],
        max_output_tokens: int,
        kind: RunKind,
        prompt_version: str,
        system: str,
        payload: dict[str, Any],
        invocation: HarnessInvocation | None,
        allowed_refs: set[str],
        evidence_refs: Callable[[Any], Iterable[str]],
    ):
        """Quarantine unsupported findings or retry one indivisible contract.

        Issue and artifact responses can safely retain their independently supported
        content immediately. Indivisible perception responses receive the exact
        immutable locator allowlist once more. OSLO never guesses or silently rewrites
        an invented evidence reference.
        """

        accumulated_metadata: HarnessCallMetadata | None = None
        current_system = system
        current_payload = payload
        for correction_attempt in range(2):
            output = self._call(
                name=name,
                schema=schema,
                max_output_tokens=max_output_tokens,
                kind=kind,
                prompt_version=prompt_version,
                system=current_system,
                payload=current_payload,
                invocation=invocation,
            )
            if invocation is not None:
                accumulated_metadata = self._merge_metadata(
                    accumulated_metadata,
                    invocation.metadata,
                )
                invocation.metadata = accumulated_metadata

            invalid_refs = sorted(set(evidence_refs(output)) - allowed_refs)
            if not invalid_refs:
                return output
            quarantined = self._quarantine_invalid_findings(
                output,
                allowed_refs=allowed_refs,
            )
            if quarantined is not None:
                _LOGGER.warning(
                    "Quarantined %s unsupported analysis finding locator(s).",
                    len(invalid_refs),
                )
                return quarantined
            if correction_attempt == 1:
                raise AgentHarnessError(
                    "EVIDENCE_REFERENCE_CONTRACT_FAILED",
                    retryable=True,
                )

            current_system = (
                f"{system} This is a correction attempt. The previous response used "
                "invalid evidence locators. Replace them only with exact values from "
                "allowed_evidence_locators. Do not alter document, page, or fragment "
                "numbers and do not introduce new locators."
            )
            current_payload = {
                **payload,
                "citation_correction": {
                    "invalid_locator_count": len(invalid_refs),
                    "allowed_evidence_locators": sorted(allowed_refs),
                    "instruction": (
                        "Return the complete corrected JSON contract. Every evidence "
                        "reference must exactly match the allowlist."
                    ),
                },
            }

        raise AssertionError("unreachable evidence correction state")

    @staticmethod
    def _quarantine_invalid_findings(
        output: BaseModel,
        *,
        allowed_refs: set[str],
    ) -> BaseModel | None:
        """Omit unsupported findings without weakening other evidence contracts."""

        issues = getattr(output, "issues", None)
        if isinstance(issues, list):
            supported = [
                issue
                for issue in issues
                if set(getattr(issue, "evidence_refs", ())).issubset(allowed_refs)
            ]
            return output.model_copy(update={"issues": supported})
        if isinstance(output, _PerceptionOutput):
            supported_refs = [
                reference
                for reference in output.evidence_refs
                if reference in allowed_refs
            ]
            if supported_refs:
                return output.model_copy(update={"evidence_refs": supported_refs})
            return None
        if isinstance(output, _SingleArtifactOutput):
            return OpenAIAgentHarness._quarantine_invalid_artifact_content(
                output,
                allowed_refs=allowed_refs,
            )
        return None

    @staticmethod
    def _quarantine_invalid_artifact_content(
        output: _SingleArtifactOutput,
        *,
        allowed_refs: set[str],
    ) -> _SingleArtifactOutput | None:
        """Keep supported artifact content when only some model citations are invalid."""

        data = output.model_dump(mode="json")
        artifact = data["artifact"]
        artifact["evidence_refs"] = [
            ref for ref in artifact["evidence_refs"] if ref in allowed_refs
        ]
        retained_refs = set(artifact["evidence_refs"])
        sections = []
        for section in artifact["sections"]:
            original_section_refs = section["evidence_refs"]
            section["evidence_refs"] = [
                ref for ref in original_section_refs if ref in allowed_refs
            ]
            retained_refs.update(section["evidence_refs"])
            kept_rows = []
            kept_row_refs = []
            kept_row_states = []
            for row, row_refs, row_state in zip(
                section["rows"],
                section["row_evidence_refs"],
                section["row_states"],
                strict=True,
            ):
                if not set(row_refs).issubset(allowed_refs):
                    continue
                kept_rows.append(row)
                kept_row_refs.append(row_refs)
                kept_row_states.append(row_state)
                retained_refs.update(row_refs)
            section["rows"] = kept_rows
            section["row_evidence_refs"] = kept_row_refs
            section["row_states"] = kept_row_states
            had_invalid_section_ref = bool(
                set(original_section_refs) - allowed_refs
            )
            if had_invalid_section_ref and not section["evidence_refs"] and not kept_rows:
                continue
            sections.append(section)
        artifact["sections"] = sections
        artifact["assumptions"] = [
            item
            for item in artifact["assumptions"]
            if set(item["evidence_refs"]).issubset(allowed_refs)
        ]
        artifact["conflicts"] = [
            item
            for item in artifact["conflicts"]
            if set(item["evidence_refs"]).issubset(allowed_refs)
        ]
        for item in (*artifact["assumptions"], *artifact["conflicts"]):
            retained_refs.update(item["evidence_refs"])
        if not artifact["evidence_refs"]:
            artifact["evidence_refs"] = sorted(retained_refs)
        if not artifact["evidence_refs"] or not artifact["sections"]:
            return None
        return _SingleArtifactOutput.model_validate(data)

    @staticmethod
    def _merge_metadata(
        previous: HarnessCallMetadata | None,
        current: HarnessCallMetadata | None,
    ) -> HarnessCallMetadata | None:
        if previous is None:
            return current
        if current is None:
            return previous
        return HarnessCallMetadata(
            provider=current.provider,
            model=current.model,
            prompt_version=current.prompt_version,
            response_id=current.response_id,
            input_tokens=previous.input_tokens + current.input_tokens,
            output_tokens=previous.output_tokens + current.output_tokens,
            duration_ms=previous.duration_ms + current.duration_ms,
            attempts=previous.attempts + current.attempts,
            mode=current.mode,
            fallback_reason=current.fallback_reason,
        )

    def _call(
        self,
        *,
        name: str,
        schema: type[BaseModel],
        max_output_tokens: int,
        kind: RunKind,
        prompt_version: str,
        system: str,
        payload: dict[str, Any],
        invocation: HarnessInvocation | None,
    ):
        started = monotonic()
        attempts = 0
        model = self._extended_model if kind is RunKind.EXTENDED else self._fast_model
        fallback_reason: str | None = None
        current_system = system
        current_payload = payload
        while True:
            attempts += 1
            try:
                response = self._client.responses.parse(
                    model=model,
                    max_output_tokens=max_output_tokens,
                    input=[
                        {"role": "system", "content": current_system},
                        {
                            "role": "user",
                            "content": json.dumps(
                                current_payload,
                                default=self._json_default,
                            ),
                        },
                    ],
                    text_format=schema,
                )
                break
            except AgentHarnessError:
                raise
            except Exception as error:
                safe_error = self._safe_provider_error(error)
                if not safe_error.retryable:
                    raise safe_error from None
                if attempts > self._max_retries:
                    fallback_allowed = safe_error.code in {
                        "OPENAI_SCHEMA_INVALID",
                        "OPENAI_TIMEOUT",
                        "OPENAI_OUTPUT_LIMIT",
                        "OPENAI_UNAVAILABLE",
                        "OPENAI_RATE_LIMIT",
                    }
                    if (
                        self._fallback_model
                        and model != self._fallback_model
                        and fallback_reason is None
                        and fallback_allowed
                    ):
                        fallback_reason = safe_error.code
                        model = self._fallback_model
                    else:
                        raise safe_error from None
                if safe_error.code == "OPENAI_SCHEMA_INVALID":
                    current_system = (
                        f"{system} This is a schema repair attempt. Correct every "
                        "validation error listed in schema_repair.validation_errors "
                        "and return the complete JSON contract. Do not omit valid "
                        "content merely to satisfy the schema."
                    )
                    current_payload = {
                        **payload,
                        "schema_repair": {
                            "validation_errors": self._schema_validation_errors(error),
                            "attempt": attempts,
                        },
                    }
                elif safe_error.code == "OPENAI_OUTPUT_LIMIT":
                    current_system = (
                        f"{system} This is an output-limit repair attempt. Return the "
                        "complete JSON contract using concise wording. Preserve every "
                        "distinct material fact or finding, but remove repeated explanation."
                    )
                    current_payload = {
                        **payload,
                        "output_limit_repair": {
                            "instruction": "Return a complete, concise contract.",
                        },
                    }
                self._sleeper(0.5 * (2 ** (attempts - 1)))
        output = response.output_parsed
        if output is None:
            code = "OPENAI_REFUSAL" if self._has_refusal(response) else "OPENAI_RESPONSE_EMPTY"
            raise AgentHarnessError(code)
        if invocation is not None:
            usage = getattr(response, "usage", None)
            invocation.metadata = HarnessCallMetadata(
                provider="openai",
                model=getattr(response, "model", model),
                prompt_version=prompt_version,
                response_id=getattr(response, "id", None),
                input_tokens=getattr(usage, "input_tokens", 0) if usage else 0,
                output_tokens=getattr(usage, "output_tokens", 0) if usage else 0,
                duration_ms=max(0, round((monotonic() - started) * 1000)),
                attempts=attempts,
                mode="fallback" if fallback_reason else "primary",
                fallback_reason=fallback_reason,
            )
        return output

    @staticmethod
    def _schema_validation_errors(error: Exception) -> list[dict[str, str]]:
        """Return bounded validation detail for the model repair prompt only."""
        validation_errors = getattr(error, "errors", None)
        if callable(validation_errors):
            repaired = []
            for item in validation_errors()[:20]:
                if not isinstance(item, dict):
                    continue
                location = ".".join(str(part) for part in item.get("loc", ()))
                repaired.append(
                    {
                        "location": location or "response",
                        "type": str(item.get("type", "validation_error"))[:120],
                        "message": " ".join(str(item.get("msg", "")).split())[:500],
                    }
                )
            if repaired:
                return repaired
        return [
            {
                "location": "response",
                "type": type(error).__name__[:120],
                "message": " ".join(str(error).split())[:500],
            }
        ]

    @staticmethod
    def _safe_provider_error(error: Exception) -> AgentHarnessError:
        status_code = getattr(error, "status_code", None)
        body = getattr(error, "body", None)
        provider_code = None
        if isinstance(body, dict):
            error_body = body.get("error", body)
            if isinstance(error_body, dict):
                provider_code = error_body.get("code")
        type_name = type(error).__name__.lower()

        if status_code == 401:
            return AgentHarnessError("OPENAI_AUTHENTICATION")
        if status_code == 403:
            return AgentHarnessError("OPENAI_PERMISSION")
        if status_code == 429 and provider_code == "insufficient_quota":
            return AgentHarnessError("OPENAI_QUOTA")
        if status_code == 429:
            return AgentHarnessError("OPENAI_RATE_LIMIT", retryable=True)
        if status_code is not None and status_code >= 500:
            return AgentHarnessError("OPENAI_UNAVAILABLE", retryable=True)
        if "timeout" in type_name:
            return AgentHarnessError("OPENAI_TIMEOUT", retryable=True)
        if "connection" in type_name:
            return AgentHarnessError("OPENAI_UNAVAILABLE", retryable=True)
        if "lengthfinishreason" in type_name:
            return AgentHarnessError("OPENAI_OUTPUT_LIMIT", retryable=True)
        validation_errors = getattr(error, "errors", None)
        if callable(validation_errors):
            for item in validation_errors():
                context = item.get("ctx", {}) if isinstance(item, dict) else {}
                detail = str(context.get("error", "")).casefold()
                if item.get("type") == "json_invalid" and "eof" in detail:
                    return AgentHarnessError("OPENAI_OUTPUT_LIMIT", retryable=True)
        if "validation" in type_name:
            return AgentHarnessError("OPENAI_SCHEMA_INVALID", retryable=True)
        return AgentHarnessError("OPENAI_REQUEST_FAILED")

    @staticmethod
    def _has_refusal(response: Any) -> bool:
        for output in getattr(response, "output", ()):
            for content in getattr(output, "content", ()):
                if getattr(content, "type", None) == "refusal":
                    return True
        return False

    @staticmethod
    def _allowed_evidence_refs(
        *,
        description: str,
        source_names: tuple[str, ...],
        evidence: tuple[EvidenceFragment, ...],
    ) -> list[str]:
        refs = [item.reference for item in evidence]
        if description.strip():
            refs.insert(0, "description:1")
        if not evidence:
            refs.extend(f"source:{index + 1}:{name}" for index, name in enumerate(source_names))
        return list(dict.fromkeys(refs))

    @staticmethod
    def _perception_evidence_refs(perception: Perception) -> set[str]:
        return set(perception.evidence_refs).union(item.reference for item in perception.evidence)

    @staticmethod
    def _artifact_output_evidence_refs(result: _ArtifactsOutput) -> Iterable[str]:
        for artifact in result.artifacts:
            yield from OpenAIAgentHarness._one_artifact_evidence_refs(artifact)

    @staticmethod
    def _single_artifact_output_evidence_refs(
        result: _SingleArtifactOutput,
    ) -> Iterable[str]:
        yield from OpenAIAgentHarness._one_artifact_evidence_refs(result.artifact)

    @staticmethod
    def _one_artifact_evidence_refs(
        artifact: _ArtifactOutput,
    ) -> Iterable[str]:
        yield from artifact.evidence_refs
        for section in artifact.sections:
            yield from section.evidence_refs
            for row_refs in section.row_evidence_refs:
                yield from row_refs
        for assumption in artifact.assumptions:
            yield from assumption.evidence_refs
        for conflict in artifact.conflicts:
            yield from conflict.evidence_refs

    @staticmethod
    def _evidence_for_artifact(
        perception: Perception,
        artifact_type: ArtifactType,
        *,
        character_budget: int = 24_000,
    ) -> tuple[EvidenceFragment, ...]:
        keywords = OpenAIAgentHarness._artifact_keywords(artifact_type)
        scored = []
        for index, item in enumerate(perception.evidence):
            text = f"{item.source_name or ''} {item.content}".lower()
            scored.append(
                (
                    sum(keyword in text for keyword in keywords),
                    index,
                    item,
                )
            )

        # Keep one representative fragment from every source, then fill the
        # bounded context with the strongest artifact-specific evidence.
        representatives = {}
        for score, index, item in scored:
            source_key = item.source_name or item.reference.split(":fragment:", 1)[0]
            current = representatives.get(source_key)
            if current is None or (score, -index) > (current[0], -current[1]):
                representatives[source_key] = (score, index, item)
        ordered = list(representatives.values())
        selected_indexes = {entry[1] for entry in ordered}
        ordered.extend(
            entry
            for entry in sorted(scored, key=lambda entry: (-entry[0], entry[1]))
            if entry[1] not in selected_indexes
        )

        selected = []
        used = 0
        for _score, index, item in ordered:
            size = len(item.reference) + len(item.content) + 160
            if used + size > character_budget:
                continue
            selected.append((index, item))
            used += size
        selected.sort(key=lambda entry: entry[0])
        return tuple(item for _, item in selected)

    @staticmethod
    def _artifact_keywords(artifact_type: ArtifactType) -> tuple[str, ...]:
        return {
            ArtifactType.INTENT: (
                "purpose",
                "objective",
                "outcome",
                "benefit",
                "success",
                "charter",
                "business case",
            ),
            ArtifactType.CONTEXT: (
                "stakeholder",
                "governance",
                "decision right",
                "constraint",
                "forum",
                "authority",
                "risk",
                "mitigation",
                "dependency",
            ),
            ArtifactType.SCOPE: (
                "scope",
                "in scope",
                "out of scope",
                "exclusion",
                "deliverable",
                "boundary",
            ),
            ArtifactType.REQUIREMENTS: (
                "requirement",
                "acceptance",
                "functional",
                "non-functional",
                "quality gate",
                "decision",
            ),
            ArtifactType.WORK_BREAKDOWN: (
                "workstream",
                "work package",
                "breakdown",
                "deliverable",
                "owner",
                "dependency",
            ),
            ArtifactType.SCHEDULE: (
                "schedule",
                "milestone",
                "date",
                "timeline",
                "activity",
                "cutover",
                "dependency",
            ),
            ArtifactType.RESOURCES: (
                "resource",
                "role",
                "allocation",
                "capacity",
                "vendor",
                "raci",
                "responsible",
                "accountable",
                "budget",
                "cost",
            ),
        }[artifact_type]

    @staticmethod
    def _artifact_contract(artifact_type: ArtifactType) -> str:
        return {
            ArtifactType.INTENT: (
                "purpose, objectives, intended outcomes, benefits, success measures and every KPI"
            ),
            ArtifactType.CONTEXT: (
                "project profile, stakeholders, governance, decision rights, constraints, "
                "dependencies, documented risks and mitigations"
            ),
            ArtifactType.SCOPE: (
                "every inclusion, exclusion, boundary, deliverable and explicitly deferred item"
            ),
            ArtifactType.REQUIREMENTS: (
                "every functional and non-functional requirement, acceptance criterion, "
                "quality target and traceable metric"
            ),
            ArtifactType.WORK_BREAKDOWN: (
                "every phase, workstream, work package, deliverable, owner and dependency"
            ),
            ArtifactType.SCHEDULE: (
                "every date, milestone, duration, dependency, alternative timeline and "
                "commitment status"
            ),
            ArtifactType.RESOURCES: (
                "every role, named party, allocation, capacity, vendor, RACI assignment, "
                "budget, funding source and cost alternative"
            ),
        }[artifact_type]

    @staticmethod
    def _items_for_artifact(
        items: tuple[str, ...],
        artifact_type: ArtifactType,
        *,
        maximum: int = 40,
    ) -> tuple[str, ...]:
        """Retain relevant perception items without repeating the full project in every shard."""
        keywords = OpenAIAgentHarness._artifact_keywords(artifact_type)
        ranked = sorted(
            enumerate(items),
            key=lambda entry: (
                -sum(keyword in entry[1].lower() for keyword in keywords),
                entry[0],
            ),
        )
        relevant = [
            item for _index, item in ranked if any(keyword in item.lower() for keyword in keywords)
        ]
        if len(relevant) < maximum:
            relevant_set = set(relevant)
            relevant.extend(item for item in items if item not in relevant_set)
        return tuple(relevant[:maximum])

    @staticmethod
    def _supported_title_candidate(perception: Perception) -> str | None:
        """Return a repeated project title from governed document headers."""
        pattern = re.compile(
            r"^\s*(?P<title>[A-Za-z0-9][A-Za-z0-9 &'(),./+-]{2,159}?)"
            r"\s+[A-Z][A-Z0-9]*-[A-Z0-9-]{2,}\s*\|"
        )
        candidates: dict[str, tuple[str, set[str]]] = {}
        for item in perception.evidence:
            match = pattern.search(item.content[:300])
            if match is None:
                continue
            title = " ".join(match.group("title").split()).strip(" -|")
            if not 3 <= len(title) <= 160 or not 2 <= len(title.split()) <= 16:
                continue
            key = title.casefold()
            display, sources = candidates.setdefault(key, (title, set()))
            sources.add(item.source_name or item.reference)
            candidates[key] = (display, sources)
        supported = [
            (len(sources), display) for display, sources in candidates.values() if len(sources) >= 2
        ]
        if not supported:
            return None
        supported.sort(key=lambda item: (-item[0], item[1].casefold()))
        return supported[0][1]

    @staticmethod
    def _select_evidence(
        evidence: tuple[EvidenceFragment, ...],
        *,
        kind: RunKind,
    ) -> tuple[EvidenceFragment, ...]:
        if not evidence:
            return ()
        # A project is currently capped at ten documents. Preserve enough material to
        # cover a dense ten-document pack while still bounding the provider request.
        character_budget = 140_000 if kind is RunKind.EXTENDED else 96_000
        keywords = (
            "timeline",
            "duration",
            "milestone",
            "budget",
            "scope",
            "success metric",
            "success measure",
            "deployment",
            "regulatory",
            "resource",
            "capacity",
            "vendor",
            "migration",
            "dependency",
            "risk",
            "unknown",
            "unresolved",
            "conflict",
        )
        scored = [
            (
                sum(keyword in item.content.lower() for keyword in keywords),
                index,
                EvidenceFragment(
                    reference=item.reference,
                    content=item.content[:2_000],
                    source_name=item.source_name,
                    location=item.location,
                ),
            )
            for index, item in enumerate(evidence)
        ]
        high_signal = [entry for entry in scored if entry[0] > 0]
        ordinary = [entry for entry in scored if entry[0] == 0]
        high_signal.sort(key=lambda entry: (-entry[0], entry[1]))

        # Spread ordinary context across the full document instead of taking only page one.
        if ordinary:
            step = max(1, len(ordinary) // 12)
            sampled = ordinary[::step]
            remaining = [entry for entry in ordinary if entry not in sampled]
            ordinary = sampled + remaining

        representatives: dict[str, tuple[int, int, EvidenceFragment]] = {}
        for entry in scored:
            score, index, item = entry
            source_key = item.source_name or item.reference.split(":page:", 1)[0]
            current = representatives.get(source_key)
            if current is None or (score, -index) > (current[0], -current[1]):
                representatives[source_key] = entry
        representative_entries = sorted(
            representatives.values(),
            key=lambda entry: entry[1],
        )
        representative_indexes = {entry[1] for entry in representative_entries}
        ordered = representative_entries + [
            entry
            for entry in high_signal + ordinary
            if entry[1] not in representative_indexes
        ]

        selected: list[tuple[int, EvidenceFragment]] = []
        used = 0
        for _, index, item in ordered:
            estimated_size = len(item.reference) * 2 + len(item.content) + 160
            if used + estimated_size > character_budget:
                continue
            selected.append((index, item))
            used += estimated_size
        selected.sort(key=lambda entry: entry[0])
        return tuple(item for _, item in selected)

    @staticmethod
    def _json_default(value):
        if hasattr(value, "__dataclass_fields__"):
            return {field: getattr(value, field) for field in value.__dataclass_fields__}
        if hasattr(value, "value"):
            return value.value
        if isinstance(value, tuple):
            return list(value)
        raise TypeError(f"Unsupported prompt value: {type(value)!r}")
