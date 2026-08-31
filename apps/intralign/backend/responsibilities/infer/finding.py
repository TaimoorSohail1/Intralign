"""Wave B Finding engine (DTM-0010; IC-WB-INFER 1.1) — Gap / Conflict / Risk.

Infer is the SINGLE producer of Findings (one-producer rule #1). This engine
derives the three Finding types from Attested knowledge (the AssertionDrafts
admitted by Retain) + the DTM-0009 ``SynthesizedPlanningModel`` + the declared-
outcome reference, ANCHORING each Finding to the AttestedAssertion id(s) it
derives from (IC-WB-INFER: missing anchor = Major failure — made impossible by
the ``Finding`` shape's non-empty ``evidence_anchors``).

Three engines (IC-WB-INFER 1.1 required-behavior #1):

1. **Gap** — structural implications of alignment / coverage / quality / SMART.
   RULE-STRUCTURAL gaps are computed deterministically (no model call) so they
   replay EXACT (decision #10): coverage gaps (an evidence category — constraint
   / dependency — absent from the Attested set), SMART gaps (a declared outcome
   reference with no measurable/time-bound attestation). An AI pass adds
   semantic alignment/quality gaps (SEMANTIC tier) when a model is wired.
2. **Conflict** — contradictions AMONG Attested assertions. RULE-STRUCTURAL
   negation-pair detection (exact); conflicts are SURFACED as Findings, NEVER
   resolved into canonical truth (IC-WB-INFER forbidden).
3. **Risk Signal** — feasibility risks. AI-derived (SEMANTIC tier) from the
   synthesized model's flagged assumptions + the Attested constraints.

FORBIDDEN here (IC-WB-INFER 1.1; guardrails): NO severity/confidence (Evaluate /
DTM-0011), NO recommendations/clarifications (Advise), NO canonical write / no
promotion to Attested, NO conflict resolution. The ``Finding`` shape forbids a
severity/score/recommendation field structurally (``extra='forbid'``); this
module exports no such producer (B3 introspects it).

Cost governance (DL-048): the AI passes run within the per-tier ``RunBudget``;
over-budget DEFERS the AI-derived Findings (a coalesced Deep Pass matures them)
rather than overspending — the rule-structural Findings are always produced
(orientation-sufficient on the Fast Pass; IC-WB-INFER #5).

Determinism (QA §1; decision #10): rule-structural gaps/conflicts are EXACT;
AI-derived Findings are SEMANTIC; set-level >=90% stable identities across
recompute (the ``finding_id`` is a stable structural hash, so the same input
re-derives the same id — supersession targets it).
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
    ConfidenceStage,
    Finding,
    Mode,
    SynthesizedPlanningModel,
    UnderstandingState,
)

if TYPE_CHECKING:  # pragma: no cover - typing only
    from backend.responsibilities.perceive.extraction import AssertionDraft

# The model/prompt/rule version stamp for Finding derivation (the determinism
# baseline component, DT-5/DT-10). The rule-structural sub-version is pinned so
# rule gaps/conflicts replay EXACT; the AI passes route to mini (Calibration §4c).
FINDING_VERSION = "wb-infer-finding-v0"

# A conservative pre-call token estimate per AI Finding pass, used by the budget
# accountant to decide whether the next pass still fits the per-run cap (DL-048).
_AI_PASS_TOKEN_ESTIMATE = 12_000

# Evidence categories a complete plan is expected to attest (coverage gap when
# absent). Constraints + dependencies bound the plan hardest; their absence is a
# structural coverage gap regardless of model (EXACT tier).
_EXPECTED_EVIDENCE_CATEGORIES: tuple[str, ...] = ("constraint", "dependency")

# Tokens that make a declared outcome measurable / time-bound (SMART). A
# declared outcome with none attested is a SMART gap (EXACT, rule-structural).
_SMART_MARKERS: tuple[str, ...] = (
    "by ",
    "%",
    "percent",
    "metric",
    "kpi",
    "deadline",
    "q1",
    "q2",
    "q3",
    "q4",
    "measur",
)

# Negation markers used for rule-structural conflict detection (EXACT).
_NEGATIONS: tuple[str, ...] = ("not", "no ", "never", "cannot", "can't", "won't", "without")

_RISK_INSTRUCTIONS = (
    "You surface feasibility RISK SIGNALS in a project plan. Return ONLY a JSON "
    "array; each item is {\"summary\": str, \"anchors\": [assertion-id, ...]}. "
    "Anchor every risk to the assertion id(s) it derives from. Do NOT assign "
    "severity, confidence, or scores; do NOT recommend fixes — only surface the "
    "risk. Use only the provided assertions and assumptions."
)

_ALIGNMENT_INSTRUCTIONS = (
    "You surface ALIGNMENT/QUALITY GAPS between a declared outcome and the "
    "attested evidence. Return ONLY a JSON array; each item is "
    "{\"summary\": str, \"anchors\": [assertion-id, ...]}. Anchor every gap to "
    "the assertion id(s) it derives from. Do NOT assign severity/confidence/"
    "scores and do NOT recommend fixes — only surface the gap."
)


@dataclass(frozen=True)
class FindingResult:
    """The output of a Finding-derivation run (Derived; plus the spend payload)."""

    findings: tuple[Finding, ...]
    degraded: bool
    spend_payload: dict[str, Any]

    def of_type(self, finding_type: str) -> tuple[Finding, ...]:
        return tuple(f for f in self.findings if f.finding_type == finding_type)


def _finding_id(project_id: str, finding_type: str, summary: str, anchors: Sequence[str]) -> str:
    """A stable structural identity for a Finding (recompute supersedes the SAME id).

    Hash over (project, type, summary, sorted anchors) so the SAME structural
    input re-derives the SAME id — supersession targets it (decision #10:
    set-level >=90% stable identities across recompute).
    """
    basis = json.dumps(
        [project_id, finding_type, summary.strip().casefold(), sorted(anchors)],
        sort_keys=True,
        ensure_ascii=False,
    )
    return f"{finding_type}-" + hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]


@dataclass
class FindingEngine:
    """Derives Gap / Conflict / Risk Findings within the per-run budget.

    ``provider`` is the DTM-0009 LLM seam (a recorded-fixture model in CI). The
    rule-structural passes never touch it; only the AI alignment/risk passes do,
    and only while the budget affords them (else they DEFER — DL-048).
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

    def _build(
        self,
        *,
        project_id: str,
        finding_type: str,
        summary: str,
        anchors: Sequence[str],
        gap_kind: str | None = None,
    ) -> Finding:
        return Finding(
            project_id=project_id,
            finding_type=finding_type,  # type: ignore[arg-type]
            finding_id=_finding_id(project_id, finding_type, summary, anchors),
            summary=summary,
            evidence_anchors=tuple(anchors),
            gap_kind=gap_kind,  # type: ignore[arg-type]
            model_or_rule_version=FINDING_VERSION,
            mode=self.mode,
            confidence_stage=self.confidence_stage,
            understanding_state=self.understanding_state,
        )

    def _run_ai(self, *, step_key: str, instructions: str, prompt: str, budget: RunBudget):
        """Run one AI Finding pass, recording its usage against the budget."""
        suffix = self._suffix(step_key)
        full = f"{prompt}\n{suffix}" if suffix else prompt
        from pydantic_ai import Agent

        model = self.provider.model_for(tier=self.tier, stage="synthesis")
        result = Agent(model, output_type=str, instructions=instructions).run_sync(full)
        tokens_in, tokens_out = usage_tokens(result.usage)
        model_name = self.provider.resolve(tier=self.tier, stage="synthesis").model_name
        budget.record(tokens_in=tokens_in, tokens_out=tokens_out, model=model_name)
        return result.output

    # -- rule-structural engines (EXACT tier) ---------------------------------

    def derive_coverage_and_smart_gaps(
        self,
        *,
        project_id: str,
        assertions: Sequence[AssertionDraft],
        assertion_ids: Sequence[str],
        declared_outcome: str | None,
        outcome_anchor: str | None,
    ) -> list[Finding]:
        """RULE-STRUCTURAL gaps — coverage + SMART (EXACT; no model call)."""
        findings: list[Finding] = []
        present_types = {a.content_type for a in assertions}
        all_ids = list(assertion_ids)

        # Coverage gaps: an expected evidence category is absent from the Attested
        # set. Anchored to the whole Attested set it was evaluated over (or, if
        # empty, the declared-outcome anchor) — never un-anchored.
        anchors_for_coverage = all_ids or ([outcome_anchor] if outcome_anchor else [])
        for category in _EXPECTED_EVIDENCE_CATEGORIES:
            if category not in present_types and anchors_for_coverage:
                findings.append(
                    self._build(
                        project_id=project_id,
                        finding_type="gap",
                        summary=f"No {category} evidence is attested for the plan.",
                        anchors=anchors_for_coverage,
                        gap_kind="coverage",
                    )
                )

        # SMART gap: a declared outcome with no measurable/time-bound attestation.
        if declared_outcome and outcome_anchor:
            text = declared_outcome.casefold()
            if not any(marker in text for marker in _SMART_MARKERS):
                findings.append(
                    self._build(
                        project_id=project_id,
                        finding_type="gap",
                        summary=(
                            "The declared outcome is not stated in measurable / "
                            "time-bound (SMART) terms."
                        ),
                        anchors=[outcome_anchor],
                        gap_kind="smart",
                    )
                )
        return findings

    def derive_conflicts(
        self,
        *,
        project_id: str,
        assertions: Sequence[AssertionDraft],
        assertion_ids: Sequence[str],
    ) -> list[Finding]:
        """RULE-STRUCTURAL conflict detection among Attested assertions (EXACT).

        Surfaces a contradiction when two assertions share a content stem but one
        negates it. The conflict is SURFACED as a Finding (anchored to BOTH
        assertion ids) — NEVER resolved into canonical truth (IC-WB-INFER).
        """
        findings: list[Finding] = []
        paired = list(zip(assertions, assertion_ids, strict=False))
        seen_pairs: set[frozenset[str]] = set()
        for i, (a_i, id_i) in enumerate(paired):
            for a_j, id_j in paired[i + 1 :]:
                if id_i == id_j:
                    continue
                if _contradicts(a_i.proposition, a_j.proposition):
                    pair_key = frozenset({id_i, id_j})
                    if pair_key in seen_pairs:
                        continue
                    seen_pairs.add(pair_key)
                    findings.append(
                        self._build(
                            project_id=project_id,
                            finding_type="conflict",
                            summary=(
                                "Attested assertions contradict each other: "
                                f"{a_i.proposition!r} vs {a_j.proposition!r} "
                                "(surfaced, not resolved)."
                            ),
                            anchors=[id_i, id_j],
                        )
                    )
        return findings

    # -- AI engines (SEMANTIC tier; budget-gated) -----------------------------

    def derive_alignment_gaps_ai(
        self,
        *,
        project_id: str,
        model: SynthesizedPlanningModel | None,
        declared_outcome: str | None,
        valid_ids: Sequence[str],
        budget: RunBudget,
    ) -> list[Finding]:
        """SEMANTIC alignment/quality gaps via the model (budget-gated)."""
        if model is None or not declared_outcome:
            return []
        prompt = (
            f"Declared outcome: {declared_outcome}\n"
            f"Synthesized intent: {model.intent_summary}\n"
            f"Synthesized scope: {model.scope_summary}\n"
            f"Assertion ids: {list(valid_ids)}"
        )
        raw = self._run_ai(
            step_key="alignment",
            instructions=_ALIGNMENT_INSTRUCTIONS,
            prompt=prompt,
            budget=budget,
        )
        return self._parse_ai_findings(
            project_id=project_id, raw=raw, finding_type="gap",
            valid_ids=valid_ids, gap_kind="alignment",
        )

    def derive_risk_signals_ai(
        self,
        *,
        project_id: str,
        model: SynthesizedPlanningModel | None,
        assertions: Sequence[AssertionDraft],
        valid_ids: Sequence[str],
        budget: RunBudget,
    ) -> list[Finding]:
        """SEMANTIC feasibility risk signals via the model (budget-gated)."""
        assumptions = (
            "; ".join(a.statement for a in model.flagged_assumptions) if model else ""
        )
        constraints = "; ".join(
            a.proposition for a in assertions if a.content_type == "constraint"
        )
        prompt = (
            f"Flagged assumptions: {assumptions}\n"
            f"Attested constraints: {constraints}\n"
            f"Assertion ids: {list(valid_ids)}"
        )
        raw = self._run_ai(
            step_key="risk",
            instructions=_RISK_INSTRUCTIONS,
            prompt=prompt,
            budget=budget,
        )
        return self._parse_ai_findings(
            project_id=project_id, raw=raw, finding_type="risk", valid_ids=valid_ids,
        )

    def _parse_ai_findings(
        self,
        *,
        project_id: str,
        raw: str,
        finding_type: str,
        valid_ids: Sequence[str],
        gap_kind: str | None = None,
    ) -> list[Finding]:
        """Build Findings from an AI pass, dropping any with no valid anchor.

        A model-returned Finding whose anchors do not resolve to a real Attested
        assertion id is DROPPED (never admitted un-anchored — IC-WB-INFER: a
        Finding must trace to its Attested evidence).
        """
        valid = set(valid_ids)
        findings: list[Finding] = []
        for item in _parse_json_array(raw):
            summary = str(item.get("summary", "")).strip()
            anchors = [a for a in item.get("anchors", []) if a in valid]
            if not summary or not anchors:
                continue  # never admit an empty or un-anchored Finding
            findings.append(
                self._build(
                    project_id=project_id,
                    finding_type=finding_type,
                    summary=summary,
                    anchors=anchors,
                    gap_kind=gap_kind,
                )
            )
        return findings

    # -- orchestrated run with cost governance --------------------------------

    def derive(
        self,
        *,
        project_id: str,
        assertions: Sequence[AssertionDraft],
        assertion_ids: Sequence[str],
        model: SynthesizedPlanningModel | None = None,
        declared_outcome: str | None = None,
        outcome_anchor: str | None = None,
        budget: RunBudget | None = None,
    ) -> FindingResult:
        """Derive all Findings WITHIN the per-run budget (DL-048).

        Rule-structural Findings (coverage/SMART gaps + conflicts) are ALWAYS
        produced — orientation-sufficient on the Fast Pass, EXACT-tier. The AI
        passes (alignment gaps, risk signals) run only while the budget affords
        them; over-budget DEFERS them (degraded=True) rather than overspending
        (a coalesced Deep Pass matures them). De-duplicated by ``finding_id``.
        """
        budget = budget or RunBudget.for_run(tier=self.tier, mode=self.mode)
        valid_ids = list(assertion_ids)

        findings: list[Finding] = []
        findings += self.derive_coverage_and_smart_gaps(
            project_id=project_id,
            assertions=assertions,
            assertion_ids=assertion_ids,
            declared_outcome=declared_outcome,
            outcome_anchor=outcome_anchor,
        )
        findings += self.derive_conflicts(
            project_id=project_id, assertions=assertions, assertion_ids=assertion_ids
        )

        # AI passes — budget-gated (DL-048: defer, never overspend).
        deferred = False
        ai_anchor_ids = valid_ids + ([outcome_anchor] if outcome_anchor else [])
        for pass_fn in (self._alignment_pass, self._risk_pass):
            if not budget.can_afford(_AI_PASS_TOKEN_ESTIMATE):
                deferred = True
                continue
            findings += pass_fn(
                project_id=project_id,
                model=model,
                assertions=assertions,
                declared_outcome=declared_outcome,
                valid_ids=ai_anchor_ids,
                budget=budget,
            )

        deduped = _dedupe_by_id(findings)
        payload = spend_event_payload(
            budget,
            user=self.user,
            model=self.provider.resolve(tier=self.tier, stage="synthesis").model_name,
            confidence_stage=self.confidence_stage,
            understanding_state=self.understanding_state,
            degraded=deferred,
        )
        return FindingResult(
            findings=tuple(deduped), degraded=deferred, spend_payload=payload
        )

    # Thin adapters so the budget loop above can treat both AI passes uniformly.
    def _alignment_pass(self, *, project_id, model, assertions, declared_outcome, valid_ids, budget):  # type: ignore[no-untyped-def]
        return self.derive_alignment_gaps_ai(
            project_id=project_id, model=model, declared_outcome=declared_outcome,
            valid_ids=valid_ids, budget=budget,
        )

    def _risk_pass(self, *, project_id, model, assertions, declared_outcome, valid_ids, budget):  # type: ignore[no-untyped-def]
        return self.derive_risk_signals_ai(
            project_id=project_id, model=model, assertions=assertions,
            valid_ids=valid_ids, budget=budget,
        )


def _contradicts(prop_a: str, prop_b: str) -> bool:
    """True when two propositions share a stem but exactly one negates it (EXACT)."""
    a, b = prop_a.casefold(), prop_b.casefold()
    neg_a = any(n in a for n in _NEGATIONS)
    neg_b = any(n in b for n in _NEGATIONS)
    if neg_a == neg_b:
        return False  # both or neither negated — not a structural contradiction
    # Strip negation tokens and compare the residual content words.
    words_a = _content_words(a)
    words_b = _content_words(b)
    if not words_a or not words_b:
        return False
    overlap = len(words_a & words_b) / max(len(words_a), len(words_b))
    return overlap >= 0.6


def _content_words(text: str) -> set[str]:
    """Lowercased content words (drop negations + short stopwords) for overlap."""
    stop = set(_NEGATIONS) | {"the", "a", "an", "is", "are", "be", "to", "of", "and", "we"}
    return {
        w.strip(".,!;:") for w in text.split()
        if w.strip(".,!;:") and w.strip(".,!;:") not in stop and len(w) > 2
    }


def _dedupe_by_id(findings: Sequence[Finding]) -> list[Finding]:
    """Keep the first Finding per ``finding_id`` (stable order)."""
    seen: set[str] = set()
    out: list[Finding] = []
    for f in findings:
        if f.finding_id in seen:
            continue
        seen.add(f.finding_id)
        out.append(f)
    return out


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
    if isinstance(parsed, dict) and "findings" in parsed:
        parsed = parsed["findings"]
    return [c for c in parsed if isinstance(c, dict)] if isinstance(parsed, list) else []
