import json
import re
from collections.abc import Callable, Iterable
from time import monotonic, sleep
from typing import Annotated, Any, Literal

from openai import OpenAI
from pydantic import BaseModel, ConfigDict, Field

from oslo_api.analysis.harness import AgentHarnessError
from oslo_api.analysis.models import (
    ARTIFACT_TYPES,
    Artifact,
    ArtifactType,
    Assessment,
    EvidenceFragment,
    HarnessCallMetadata,
    HarnessInvocation,
    Issue,
    Perception,
    RunKind,
)

PROMPT_VERSIONS = {
    "perceive": "oslo-perceive-v2",
    "construct": "oslo-construct-v2",
    "evaluate": "oslo-evaluate-v5",
}
ShortText = Annotated[str, Field(min_length=1, max_length=1_000)]
LongText = Annotated[str, Field(min_length=1, max_length=4_000)]
EvidenceReference = Annotated[str, Field(min_length=1, max_length=300)]
RatingBand = Literal["Very Low", "Low", "Moderate", "High"]
ReliabilityBand = Literal["Low", "Moderate", "High"]


class _StrictOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _PerceptionOutput(_StrictOutput):
    facts: list[ShortText] = Field(min_length=1, max_length=30)
    claims: list[ShortText] = Field(max_length=30)
    gaps: list[ShortText] = Field(max_length=30)
    evidence_refs: list[EvidenceReference] = Field(min_length=1, max_length=50)


class _ArtifactOutput(_StrictOutput):
    artifact_type: ArtifactType
    title: ShortText
    summary: LongText
    reliability: ReliabilityBand
    evidence_refs: list[EvidenceReference] = Field(min_length=1, max_length=50)
    basis: Literal["supported", "derived", "inferred"] = "derived"


class _ArtifactsOutput(_StrictOutput):
    artifacts: list[_ArtifactOutput] = Field(min_length=7, max_length=7)


class _IssueOutput(_StrictOutput):
    id: Annotated[str, Field(min_length=1, max_length=100, pattern=r"^[A-Z0-9_-]+$")]
    artifact_type: ArtifactType
    dimension: Literal["Clarity", "Alignment", "Feasibility"]
    severity: Literal["Warning", "Moderate", "Critical"]
    title: ShortText
    why: LongText
    recommendation: LongText
    evidence_refs: list[EvidenceReference] = Field(min_length=1, max_length=20)
    clarification: ShortText | None = None
    status: Literal["open", "addressed", "resolved"] = "open"


class _AssessmentOutput(_StrictOutput):
    confidence_index: int = Field(ge=0, le=100)
    confidence_band: RatingBand
    reliability: ReliabilityBand
    clarity: RatingBand
    alignment: RatingBand
    feasibility: RatingBand
    issues: list[_IssueOutput] = Field(max_length=20)


class OpenAIAgentHarness:
    """Three governed, schema-bound model calls inside the OSLO harness boundary."""

    def __init__(
        self,
        *,
        api_key: str,
        model: str | None = None,
        fast_model: str | None = None,
        extended_model: str | None = None,
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
            max_output_tokens=3_000 if kind is RunKind.EXTENDED else 2_500,
            kind=kind,
            prompt_version=PROMPT_VERSIONS["perceive"],
            system=(
                f"You are OSLO Perceive ({PROMPT_VERSIONS['perceive']}). "
                "Extract only supported facts, "
                "claims and gaps. Never invent evidence. Every item must cite a supplied "
                "evidence locator copied exactly from allowed_evidence_locators; never "
                "reconstruct or alter page or fragment numbers. Be concise and consolidate "
                "duplicate findings. "
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
        allowed_refs = self._perception_evidence_refs(perception)
        output = self._call_with_evidence_contract(
            name="oslo_artifacts",
            schema=_ArtifactsOutput,
            max_output_tokens=4_000,
            kind=kind,
            prompt_version=PROMPT_VERSIONS["construct"],
            system=(
                f"You are OSLO Construct ({PROMPT_VERSIONS['construct']}). "
                "Build exactly seven artifacts "
                "in this exact order: intent, context, scope, requirements, work_breakdown, "
                "schedule, resources. Qualify uncertainty, cite evidence and keep each summary "
                "concise. Every evidence_refs value must be copied exactly from "
                "allowed_evidence_locators; never reconstruct or alter a locator. Return JSON only."
            ),
            payload={
                "analysis_kind": kind.value,
                "perception": perception,
                "allowed_evidence_locators": sorted(allowed_refs),
            },
            invocation=invocation,
            allowed_refs=allowed_refs,
            evidence_refs=lambda result: (
                reference
                for artifact in result.artifacts
                for reference in artifact.evidence_refs
            ),
        )
        artifacts = tuple(
            Artifact(
                artifact_type=item.artifact_type,
                title=item.title,
                summary=item.summary,
                reliability=item.reliability,
                evidence_refs=tuple(item.evidence_refs),
                basis=item.basis,
            )
            for item in output.artifacts
        )
        if tuple(item.artifact_type for item in artifacts) != ARTIFACT_TYPES:
            raise AgentHarnessError("SEVEN_ARTIFACT_CONTRACT_FAILED")
        return artifacts

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
            max_output_tokens=4_000 if kind is RunKind.EXTENDED else 3_500,
            kind=kind,
            prompt_version=PROMPT_VERSIONS["evaluate"],
            system=(
                f"You are OSLO Evaluate ({PROMPT_VERSIONS['evaluate']}). "
                "Apply the approved clarity, "
                "alignment and feasibility rubric. Identify actionable, evidence-cited issues. "
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
                "and keep explanations concise. Do not expose hidden "
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
                reference
                for issue in result.issues
                for reference in issue.evidence_refs
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
        """Retry one citation-only correction, then fail closed.

        The model receives the exact immutable locator allowlist again. OSLO never
        guesses, normalizes, or silently rewrites an invented evidence reference.
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
                    "invalid_locators": invalid_refs,
                    "allowed_evidence_locators": sorted(allowed_refs),
                    "instruction": (
                        "Return the complete corrected JSON contract. Every evidence "
                        "reference must exactly match the allowlist."
                    ),
                },
            }

        raise AssertionError("unreachable evidence correction state")

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
        model = (
            self._extended_model
            if kind is RunKind.EXTENDED
            else self._fast_model
        )
        while True:
            attempts += 1
            try:
                response = self._client.responses.parse(
                    model=model,
                    max_output_tokens=max_output_tokens,
                    input=[
                        {"role": "system", "content": system},
                        {
                            "role": "user",
                            "content": json.dumps(payload, default=self._json_default),
                        },
                    ],
                    text_format=schema,
                )
                break
            except AgentHarnessError:
                raise
            except Exception as error:
                safe_error = self._safe_provider_error(error)
                if not safe_error.retryable or attempts > self._max_retries:
                    raise safe_error from None
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
            )
        return output

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
            return AgentHarnessError("OPENAI_OUTPUT_LIMIT")
        validation_errors = getattr(error, "errors", None)
        if callable(validation_errors):
            for item in validation_errors():
                context = item.get("ctx", {}) if isinstance(item, dict) else {}
                detail = str(context.get("error", "")).casefold()
                if item.get("type") == "json_invalid" and "eof" in detail:
                    return AgentHarnessError("OPENAI_OUTPUT_LIMIT")
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
            refs.extend(
                f"source:{index + 1}:{name}"
                for index, name in enumerate(source_names)
            )
        return list(dict.fromkeys(refs))

    @staticmethod
    def _perception_evidence_refs(perception: Perception) -> set[str]:
        return set(perception.evidence_refs).union(
            item.reference for item in perception.evidence
        )

    @staticmethod
    def _select_evidence(
        evidence: tuple[EvidenceFragment, ...],
        *,
        kind: RunKind,
    ) -> tuple[EvidenceFragment, ...]:
        if not evidence:
            return ()
        character_budget = 48_000 if kind is RunKind.EXTENDED else 18_000
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

        selected: list[tuple[int, EvidenceFragment]] = []
        used = 0
        for _, index, item in high_signal + ordinary:
            estimated_size = len(item.reference) * 2 + len(item.content) + 160
            if used + estimated_size > character_budget:
                continue
            selected.append((index, item))
            used += estimated_size
        selected.sort(key=lambda entry: entry[0])
        return tuple(item for _, item in selected)

    @staticmethod
    def _json_default(value):
        if hasattr(value, "value"):
            return value.value
        if hasattr(value, "__dataclass_fields__"):
            return {
                field: getattr(value, field)
                for field in value.__dataclass_fields__
            }
        if isinstance(value, tuple):
            return list(value)
        raise TypeError(f"Unsupported prompt value: {type(value)!r}")
