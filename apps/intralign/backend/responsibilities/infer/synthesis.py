"""Wave S synthesis + generation engine (DL-047 PS-01/PS-02; DL-048 cost gov).

Infer turns Attested assertions into:

1. a ``SynthesizedPlanningModel`` (PS-01) — Evidence Extraction -> Context
   Expansion -> Planning Construction; gaps filled with EXPLICITLY-FLAGGED
   assumptions (never silent — A4.4), and
2. the seven ``PlanningArtifact``s (PS-02) generated from that model.

Both are DERIVED Cognition (``epistemic_state=derived``; hard rule #2): never
written to the canonical store as Attested-truth. The user's EDIT of a
generated artifact is a separate, new Attested input through Retain's admission
path (DTM-0008) — this engine never autonomously edits an artifact (A4.5).

Cost governance (DL-048; decision #7): synthesis/generation run within the
per-tier per-run token budget. Over-budget -> graceful degradation — synthesize
a PARTIAL model from the highest-priority evidence within budget and DEFER the
remaining generation to a coalesced Deep Pass; never silent overspend, never
runaway. Every run carries an ``ai_spend_recorded`` payload.

Determinism (QA §2): the model/artifacts are AI-text -> SEMANTIC-equivalence
tier (same plan identity/intent; wording may differ); explicit attribution
lineage is EXACT. In CI the model is a recorded model-response fixture, so the
suite is offline-deterministic (ADR-0004).
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from backend.services.llm_provider import (
    LLMProvider,
    RunBudget,
    spend_event_payload,
    usage_tokens,
)
from shared.epistemic import (
    PLANNING_ARTIFACT_TYPES,
    ConfidenceStage,
    FlaggedAssumption,
    Mode,
    PlanningArtifact,
    PlanningArtifactType,
    SynthesizedPlanningModel,
    UnderstandingState,
)

if TYPE_CHECKING:  # pragma: no cover - typing only
    from backend.responsibilities.perceive.extraction import AssertionDraft

# The model/prompt/rule version stamp for synthesis (the determinism baseline
# component, DT-5/DT-10). Synthesis/generation route to mini (Calibration §4c).
SYNTHESIS_VERSION = "ws-synth-llm-v0"

# Priority order for "highest-priority evidence" when degrading under budget
# (DL-048): constraints + dependencies bound the plan hardest, then facts, then
# assumptions (already weakest — an assumption is a gap-fill, not evidence).
_EVIDENCE_PRIORITY: dict[str, int] = {
    "constraint": 0,
    "dependency": 1,
    "fact": 2,
    "assumption": 3,
}

# A conservative pre-call token estimate per generated artifact, used by the
# budget accountant to decide whether the next artifact still fits the cap.
# (A dial; the real usage is recorded post-call from the model's reported usage.)
_ARTIFACT_TOKEN_ESTIMATE = 12_000
_SYNTHESIS_TOKEN_ESTIMATE = 20_000

_SYNTHESIS_INSTRUCTIONS = (
    "You synthesize a project planning model from attested claims. Return ONLY "
    "a JSON object: {\"intent_summary\": str, \"scope_summary\": str, "
    "\"assumptions\": [{\"statement\": str, \"covers_gap\": str}]}. Every gap "
    "you fill MUST appear in assumptions — never present an inferred assumption "
    "as an attested fact."
)

_GENERATION_INSTRUCTIONS = (
    "You generate one planning artifact from a synthesized planning model. "
    "Return ONLY a JSON object: {\"title\": str, \"body\": str}. Use only the "
    "model and its flagged assumptions; do not invent un-flagged facts."
)


@dataclass(frozen=True)
class SynthesisResult:
    """The output of a synthesis+generation run (Derived; plus the spend payload)."""

    model: SynthesizedPlanningModel
    artifacts: tuple[PlanningArtifact, ...]
    deferred_artifact_types: tuple[PlanningArtifactType, ...]
    degraded: bool
    spend_payload: dict[str, Any]


@dataclass
class SynthesisEngine:
    """Drives synthesis + generation over the routed model within budget.

    ``prompt_suffix_for`` lets the recorded-fixture harness inject a per-step
    response-selection directive (empty string in live runs); the backend never
    imports the tests harness — only the directive string is passed in.
    """

    provider: LLMProvider
    tier: str = "free"
    mode: Mode = "fast"
    user: str = "anonymous"
    confidence_stage: ConfidenceStage = "orientation"
    understanding_state: UnderstandingState = "initial"
    prompt_suffix_for: Any = field(default=None)  # Callable[[str], str] | None

    # -- internal helpers -----------------------------------------------------

    def _suffix(self, step: str) -> str:
        if self.prompt_suffix_for is None:
            return ""
        return self.prompt_suffix_for(step) or ""

    def _agent(self, *, stage: str, instructions: str):  # type: ignore[no-untyped-def]
        from pydantic_ai import Agent

        model = self.provider.model_for(tier=self.tier, stage=stage)
        return Agent(model, output_type=str, instructions=instructions)

    def _run(
        self, *, stage: str, step_key: str, instructions: str, prompt: str, budget: RunBudget
    ):
        """Run one model step, record its usage against the budget.

        ``stage`` drives tier-keyed routing (DL-048 §4c); ``step_key`` drives
        the recorded-fixture response selection (harness plumbing — empty suffix
        in live runs).
        """
        suffix = self._suffix(step_key)
        full = f"{prompt}\n{suffix}" if suffix else prompt
        result = self._agent(stage=stage, instructions=instructions).run_sync(full)
        tokens_in, tokens_out = usage_tokens(result.usage)
        model_name = self.provider.resolve(tier=self.tier, stage=stage).model_name
        budget.record(tokens_in=tokens_in, tokens_out=tokens_out, model=model_name)
        return result.output

    # -- PS-01 synthesis ------------------------------------------------------

    def synthesize_model(
        self,
        *,
        project_id: str,
        assertions: Sequence[AssertionDraft],
        assertion_ids: Sequence[str],
        budget: RunBudget,
    ) -> SynthesizedPlanningModel:
        """Synthesize the Derived planning model; flag every gap-fill assumption."""
        evidence = "\n".join(f"- ({a.content_type}) {a.proposition}" for a in assertions)
        raw = self._run(
            stage="synthesis",
            step_key="synthesis",
            instructions=_SYNTHESIS_INSTRUCTIONS,
            prompt=f"Attested claims:\n{evidence}",
            budget=budget,
        )
        parsed = _parse_json_object(raw)
        assumptions = tuple(
            FlaggedAssumption(
                statement=str(a.get("statement", "")).strip(),
                covers_gap=str(a.get("covers_gap", "")).strip(),
            )
            for a in parsed.get("assumptions", [])
            if isinstance(a, dict) and a.get("statement")
        )
        return SynthesizedPlanningModel(
            project_id=project_id,
            model_version=SYNTHESIS_VERSION,
            intent_summary=str(parsed.get("intent_summary", "")).strip(),
            scope_summary=str(parsed.get("scope_summary", "")).strip(),
            derived_from_assertions=tuple(assertion_ids),
            flagged_assumptions=assumptions,
            mode=self.mode,
            confidence_stage=self.confidence_stage,
            understanding_state=self.understanding_state,
        )

    # -- PS-02 generation -----------------------------------------------------

    def generate_artifact(
        self,
        *,
        model: SynthesizedPlanningModel,
        artifact_type: PlanningArtifactType,
        budget: RunBudget,
    ) -> PlanningArtifact:
        """Generate one Derived PlanningArtifact from the synthesized model."""
        assumptions = "; ".join(a.statement for a in model.flagged_assumptions)
        prompt = (
            f"Artifact type: {artifact_type}\n"
            f"Intent: {model.intent_summary}\nScope: {model.scope_summary}\n"
            f"Flagged assumptions: {assumptions}"
        )
        raw = self._run(
            stage="generation",
            step_key=artifact_type,
            instructions=_GENERATION_INSTRUCTIONS,
            prompt=prompt,
            budget=budget,
        )
        parsed = _parse_json_object(raw)
        return PlanningArtifact(
            project_id=model.project_id,
            artifact_type=artifact_type,
            title=str(parsed.get("title", artifact_type.title())).strip(),
            body=str(parsed.get("body", "")).strip(),
            model_version=SYNTHESIS_VERSION,
            derived_from_assertions=model.derived_from_assertions,
            flagged_assumptions=model.flagged_assumptions,
            synthesized_model_version=model.model_version,
            mode=self.mode,
            confidence_stage=self.confidence_stage,
            understanding_state=self.understanding_state,
        )

    # -- orchestrated run with cost governance --------------------------------

    def synthesize_and_generate(
        self,
        *,
        project_id: str,
        assertions: Sequence[AssertionDraft],
        assertion_ids: Sequence[str],
        budget: RunBudget | None = None,
        artifact_types: Sequence[PlanningArtifactType] = PLANNING_ARTIFACT_TYPES,
    ) -> SynthesisResult:
        """Synthesize the model + generate artifacts WITHIN the per-run budget.

        Over-budget (DL-048): the model is synthesized from the HIGHEST-PRIORITY
        evidence within budget, and any artifact that would exceed the per-run
        cap is DEFERRED (to a coalesced Deep Pass) rather than overspent. The
        result carries the ``ai_spend_recorded`` payload and a ``degraded`` flag.
        """
        budget = budget or RunBudget.for_run(tier=self.tier, mode=self.mode)
        prioritized = _prioritize(assertions, assertion_ids)
        ordered_assertions = [a for a, _ in prioritized]
        ordered_ids = [i for _, i in prioritized]

        model = self.synthesize_model(
            project_id=project_id,
            assertions=ordered_assertions,
            assertion_ids=ordered_ids,
            budget=budget,
        )

        generated: list[PlanningArtifact] = []
        deferred: list[PlanningArtifactType] = []
        for artifact_type in artifact_types:
            if not budget.can_afford(_ARTIFACT_TOKEN_ESTIMATE):
                deferred.append(artifact_type)  # defer — do NOT overspend
                continue
            generated.append(
                self.generate_artifact(
                    model=model, artifact_type=artifact_type, budget=budget
                )
            )

        degraded = bool(deferred)
        payload = spend_event_payload(
            budget,
            user=self.user,
            model=self.provider.resolve(
                tier=self.tier, stage="synthesis"
            ).model_name,
            confidence_stage=self.confidence_stage,
            understanding_state=self.understanding_state,
            degraded=degraded,
        )
        return SynthesisResult(
            model=model,
            artifacts=tuple(generated),
            deferred_artifact_types=tuple(deferred),
            degraded=degraded,
            spend_payload=payload,
        )


def _prioritize(
    assertions: Sequence[AssertionDraft], assertion_ids: Sequence[str]
) -> list[tuple[AssertionDraft, str]]:
    """Order (assertion, id) pairs by evidence priority — stable within a tier."""
    paired = list(zip(assertions, assertion_ids, strict=False))
    return sorted(
        paired, key=lambda pair: _EVIDENCE_PRIORITY.get(pair[0].content_type, 9)
    )


def _parse_json_object(raw: str) -> dict[str, Any]:
    """Parse a model JSON object, tolerant of code-fenced output; {} on failure."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lstrip().startswith("json"):
            cleaned = cleaned.lstrip()[4:]
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}
