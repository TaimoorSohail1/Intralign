"""Wave C Advise engine (DTM-0014; IC-WC-ADVISE 1.1) — Recommendation + Clarification.

Advise is the SINGLE producer of Recommendation + ClarificationRequest
(one-producer rule #1). This engine derives, from the Findings (Infer) + Issues
and assessment (Evaluate) that motivate them:

1. **Recommendations** — governable candidate *responses* of two types
   (Suggested Action, Candidate Improvement), each ANCHORED to the Finding/Issue
   it responds to (IC-WC-ADVISE: a standalone/unanchored Recommendation is a
   Major failure — made structurally impossible by the non-empty ``anchor``
   field on the ``Recommendation`` shape). Multiple alternatives persist as
   MULTIPLE Recommendations — there is NO standalone Resolution-Path object
   (presentation-only, AMB-1/Wave E). Emitted in the ``generated`` state ONLY
   (DL-055): Advise proposes; the user disposes (Wave U).
2. **Clarification Requests** — information requests on BLOCKING ambiguity (a
   question, not an action), each anchored to the Finding/Issue whose ambiguity
   they surface. Raised when the inputs leave understanding blocked (here: a
   conflict Finding — contradictory Attested assertions — is the canonical
   blocking ambiguity; recompute re-derives as the ambiguity resolves).

The recommendation/clarification TEXT is AI-text (the LLM via the ``advise``
routing stage); selection is deterministic in CI via the recorded-fixture
harness (ADR-0004 — zero provider calls in PR CI). The ANCHOR + the type are
EXACT (never model-chosen): the engine only admits a Recommendation/Clarification
whose anchor resolves to a real Finding/Issue id it was given, so a model that
returns an unanchored item is DROPPED (never admitted standalone).

FORBIDDEN here (IC-WC-ADVISE; guardrails): NO severity/confidence/score
(Evaluate's — the shapes forbid the field structurally, ``extra='forbid'``); NO
Findings (Infer's); NO canonical write / no promotion to Attested; NO
govern/authorize/execute; NO self-accept (the Recommendation ``state`` is pinned
``generated``); NO assessment change outside recompute; NO standalone
Resolution-Path object (this module never builds one — B3 introspects it).

Cost governance (DL-048): the AI passes run within the per-tier ``RunBudget``;
over-budget DEFERS the AI-derived text (a coalesced Deep Pass matures it) rather
than overspending. Recommendations are always anchored; the structural
clarification (on a conflict) is rule-driven and always produced.

Determinism (QA §C2; decision #8): recommendation/clarification TEXT is SEMANTIC
(never exact-replay); the anchor + type + id are EXACT; set-level >=90% stable
identities across recompute (the id is a stable structural hash, so the same
(anchor, type, summary) re-derives the same id — supersession targets it).
"""

from __future__ import annotations

import hashlib
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
    ClarificationRequest,
    ConfidenceStage,
    Mode,
    Recommendation,
    RecommendationType,
    UnderstandingState,
)

if TYPE_CHECKING:  # pragma: no cover - typing only
    from shared.epistemic import Finding, Issue

# The model/prompt/rule version stamp for advise derivation (the determinism
# baseline component, DT-5/DT-10). The advise text routes to the internal model
# (DL-069); the anchor/type/id are EXACT.
ADVISE_VERSION = "wc-advise-v0"

# A conservative pre-call token estimate per AI advise pass, used by the budget
# accountant to decide whether the next pass still fits the per-run cap (DL-048).
_AI_PASS_TOKEN_ESTIMATE = 12_000

_RECOMMENDATION_INSTRUCTIONS = (
    "You generate advisory RECOMMENDATIONS that respond to a project-plan "
    "finding/issue. Return ONLY a JSON array; each item is "
    "{\"summary\": str, \"anchor\": str, \"type\": \"suggested_action\" | "
    "\"candidate_improvement\"}. Anchor every recommendation to the exact "
    "finding/issue id it responds to. Offer alternatives as SEPARATE items. Do "
    "NOT assign severity, confidence, or scores; do NOT accept, approve, govern, "
    "or execute anything — only PROPOSE a candidate response. Use only the "
    "provided findings/issues."
)

_CLARIFICATION_INSTRUCTIONS = (
    "You raise a CLARIFICATION REQUEST when ambiguity BLOCKS understanding of a "
    "project plan. Return ONLY a JSON array; each item is "
    "{\"question\": str, \"anchor\": str}. Anchor every question to the exact "
    "finding/issue id whose ambiguity it surfaces. Ask only for the information "
    "needed to unblock understanding — do NOT recommend an action, assign a "
    "score, or resolve the ambiguity yourself."
)


@dataclass(frozen=True)
class AdviseResult:
    """The output of an Advise run (Derived; plus the spend payload)."""

    recommendations: tuple[Recommendation, ...]
    clarifications: tuple[ClarificationRequest, ...]
    degraded: bool
    spend_payload: dict[str, Any]


def _recommendation_id(
    project_id: str, anchor: str, rec_type: str, summary: str
) -> str:
    """A stable structural identity for a Recommendation (recompute supersedes it).

    Hash over (project, anchor, type, summary) so the SAME structural input
    re-derives the SAME id — supersession targets it (decision #8: set-level
    >=90% stable identities across recompute). Anchor + type are EXACT; the
    SEMANTIC summary is normalized (casefold/strip) so trivial whitespace/case
    variation does not fork the identity.
    """
    basis = json.dumps(
        [project_id, anchor, rec_type, summary.strip().casefold()],
        sort_keys=True,
        ensure_ascii=False,
    )
    return "rec-" + hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]


def _clarification_id(project_id: str, anchor: str, question: str) -> str:
    """A stable structural identity for a ClarificationRequest (supersession key)."""
    basis = json.dumps(
        [project_id, anchor, question.strip().casefold()],
        sort_keys=True,
        ensure_ascii=False,
    )
    return "clr-" + hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]


@dataclass
class AdviseEngine:
    """Derives Recommendations + Clarification Requests within the per-run budget.

    ``provider`` is the LLM seam (a recorded-fixture model in CI). The advise AI
    passes route to the ``advise`` stage (internal gemma primary, DL-069) and run
    only while the budget affords them (else they DEFER — DL-048).
    ``prompt_suffix_for`` lets the recorded-fixture harness inject a per-step
    response-selection directive (empty in live runs).
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

    def _run_ai(self, *, step_key: str, instructions: str, prompt: str, budget: RunBudget) -> str:
        """Run one AI advise pass, recording its usage against the budget."""
        suffix = self._suffix(step_key)
        full = f"{prompt}\n{suffix}" if suffix else prompt
        from pydantic_ai import Agent

        model = self.provider.model_for(tier=self.tier, stage="advise")
        result = Agent(model, output_type=str, instructions=instructions).run_sync(full)
        tokens_in, tokens_out = usage_tokens(result.usage)
        model_name = self.provider.resolve(tier=self.tier, stage="advise").model_name
        budget.record(tokens_in=tokens_in, tokens_out=tokens_out, model=model_name)
        return result.output

    def _build_recommendation(
        self, *, project_id: str, anchor: str, rec_type: RecommendationType, summary: str
    ) -> Recommendation:
        return Recommendation(
            project_id=project_id,
            recommendation_id=_recommendation_id(project_id, anchor, rec_type, summary),
            recommendation_type=rec_type,
            anchor=anchor,
            summary=summary,
            model_or_rule_version=ADVISE_VERSION,
            mode=self.mode,
            confidence_stage=self.confidence_stage,
            understanding_state=self.understanding_state,
        )

    def _build_clarification(
        self, *, project_id: str, anchor: str, question: str
    ) -> ClarificationRequest:
        return ClarificationRequest(
            project_id=project_id,
            clarification_id=_clarification_id(project_id, anchor, question),
            anchor=anchor,
            question=question,
            model_or_rule_version=ADVISE_VERSION,
            mode=self.mode,
            confidence_stage=self.confidence_stage,
            understanding_state=self.understanding_state,
        )

    # -- AI passes (SEMANTIC text; anchor/type EXACT; budget-gated) -----------

    def derive_recommendations_ai(
        self,
        *,
        project_id: str,
        findings: Sequence[Finding],
        issues: Sequence[Issue],
        valid_anchors: Sequence[str],
        budget: RunBudget,
    ) -> list[Recommendation]:
        """SEMANTIC recommendations anchored to the Findings/Issues (budget-gated)."""
        if not valid_anchors:
            return []
        prompt = (
            "Findings/Issues to respond to:\n"
            + "\n".join(self._anchor_lines(findings, issues))
            + f"\nValid anchor ids: {list(valid_anchors)}"
        )
        raw = self._run_ai(
            step_key="recommendation",
            instructions=_RECOMMENDATION_INSTRUCTIONS,
            prompt=prompt,
            budget=budget,
        )
        return self._parse_recommendations(
            project_id=project_id, raw=raw, valid_anchors=valid_anchors
        )

    def derive_clarifications_ai(
        self,
        *,
        project_id: str,
        blocking: Sequence[Finding],
        valid_anchors: Sequence[str],
        budget: RunBudget,
    ) -> list[ClarificationRequest]:
        """SEMANTIC clarification requests on BLOCKING ambiguity (budget-gated).

        ``blocking`` is the subset of Findings whose ambiguity blocks
        understanding (conflict Findings — contradictory Attested assertions).
        When nothing is blocking, NO clarification is raised (a clarification is
        an information request on a real block, never noise).
        """
        if not blocking or not valid_anchors:
            return []
        prompt = (
            "Blocking ambiguities (contradictions among attested assertions):\n"
            + "\n".join(
                f"- id={f.finding_id} :: {f.summary}" for f in blocking
            )
            + f"\nValid anchor ids: {list(valid_anchors)}"
        )
        raw = self._run_ai(
            step_key="clarification",
            instructions=_CLARIFICATION_INSTRUCTIONS,
            prompt=prompt,
            budget=budget,
        )
        return self._parse_clarifications(
            project_id=project_id, raw=raw, valid_anchors=valid_anchors
        )

    @staticmethod
    def _anchor_lines(
        findings: Sequence[Finding], issues: Sequence[Issue]
    ) -> list[str]:
        lines = [f"- id={f.finding_id} type={f.finding_type} :: {f.summary}" for f in findings]
        lines += [
            f"- id={i.issue_id} (issue, severity={i.severity}, finding={i.finding_id}) :: {i.summary}"
            for i in issues
        ]
        return lines

    def _parse_recommendations(
        self, *, project_id: str, raw: str, valid_anchors: Sequence[str]
    ) -> list[Recommendation]:
        """Build Recommendations from an AI pass, dropping any with no valid anchor.

        A model-returned Recommendation whose anchor does not resolve to a real
        Finding/Issue id is DROPPED (never admitted standalone — IC-WC-ADVISE:
        Recommendation-only-in-Finding-context). An unknown type defaults to
        Suggested Action (the conservative proposal), never invented.
        """
        valid = set(valid_anchors)
        out: list[Recommendation] = []
        seen: set[str] = set()
        for item in _parse_json_array(raw):
            summary = str(item.get("summary", "")).strip()
            anchor = str(item.get("anchor", "")).strip()
            rec_type = item.get("type", "suggested_action")
            if rec_type not in ("suggested_action", "candidate_improvement"):
                rec_type = "suggested_action"
            if not summary or anchor not in valid:
                continue  # never admit an empty or unanchored Recommendation
            rec = self._build_recommendation(
                project_id=project_id, anchor=anchor, rec_type=rec_type, summary=summary
            )
            if rec.recommendation_id in seen:
                continue
            seen.add(rec.recommendation_id)
            out.append(rec)
        return out

    def _parse_clarifications(
        self, *, project_id: str, raw: str, valid_anchors: Sequence[str]
    ) -> list[ClarificationRequest]:
        valid = set(valid_anchors)
        out: list[ClarificationRequest] = []
        seen: set[str] = set()
        for item in _parse_json_array(raw):
            question = str(item.get("question", "")).strip()
            anchor = str(item.get("anchor", "")).strip()
            if not question or anchor not in valid:
                continue
            clr = self._build_clarification(
                project_id=project_id, anchor=anchor, question=question
            )
            if clr.clarification_id in seen:
                continue
            seen.add(clr.clarification_id)
            out.append(clr)
        return out

    # -- orchestrated run with cost governance --------------------------------

    def derive(
        self,
        *,
        project_id: str,
        findings: Sequence[Finding] = (),
        issues: Sequence[Issue] = (),
        budget: RunBudget | None = None,
    ) -> AdviseResult:
        """Derive Recommendations + Clarifications WITHIN the per-run budget (DL-048).

        Anchors are the Finding ids + Issue ids supplied (EXACT). The AI passes
        (recommendation text, clarification text) run only while the budget
        affords them; over-budget DEFERS them (degraded=True) rather than
        overspending (a coalesced Deep Pass matures them). Clarifications are
        raised only for BLOCKING ambiguity (conflict Findings).
        """
        budget = budget or RunBudget.for_run(tier=self.tier, mode=self.mode)
        valid_anchors = [f.finding_id for f in findings] + [i.issue_id for i in issues]
        blocking = [f for f in findings if f.finding_type == "conflict"]

        recommendations: list[Recommendation] = []
        clarifications: list[ClarificationRequest] = []
        deferred = False

        if budget.can_afford(_AI_PASS_TOKEN_ESTIMATE):
            recommendations += self.derive_recommendations_ai(
                project_id=project_id,
                findings=findings,
                issues=issues,
                valid_anchors=valid_anchors,
                budget=budget,
            )
        else:
            deferred = True

        if blocking:
            if budget.can_afford(_AI_PASS_TOKEN_ESTIMATE):
                clarifications += self.derive_clarifications_ai(
                    project_id=project_id,
                    blocking=blocking,
                    valid_anchors=valid_anchors,
                    budget=budget,
                )
            else:
                deferred = True

        payload = spend_event_payload(
            budget,
            user=self.user,
            model=self.provider.resolve(tier=self.tier, stage="advise").model_name,
            confidence_stage=self.confidence_stage,
            understanding_state=self.understanding_state,
            degraded=deferred,
        )
        return AdviseResult(
            recommendations=tuple(recommendations),
            clarifications=tuple(clarifications),
            degraded=deferred,
            spend_payload=payload,
        )


def _parse_json_array(raw: str) -> list[dict[str, Any]]:
    """Parse a model JSON array, tolerant of code-fenced output; [] on failure."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lstrip().startswith("json"):
            cleaned = cleaned.lstrip()[4:]
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        return []
    if isinstance(parsed, dict) and "recommendations" in parsed:
        parsed = parsed["recommendations"]
    return [c for c in parsed if isinstance(c, dict)] if isinstance(parsed, list) else []
