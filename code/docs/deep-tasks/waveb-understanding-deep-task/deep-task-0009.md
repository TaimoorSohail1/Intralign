# DTM-0009 — Synthesis: LLM seam + recorded-fixture harness, extraction, planning model + artifact generation

**Status:** Planned — BLOCKED on owner Wave B authorization (DL-044) · **Module:** DTM-0009 ·
**Phase:** III (Wave B) · **Contract:** **IC/QA/OBS-WS-SYNTH** (+ DL-047, DL-048) ·
**Depends:** Wave A approved (Retain admission DTM-0008, 00R backbone DTM-0004/5/6) ·
**Gate:** owner authorizes Phase III / Wave B start (DL-044 cond. 2) before coding.

## Goal / observable behavior

OSLO turns admitted evidence into (a) source-attributed `AttestedAssertion`s (Perceive
extraction — Attested, no cognition) and (b) a **`SynthesizedPlanningModel`** + seven
**`PlanningArtifact`s** (Intent/Context/Scope/Requirements/WBS/Resources/Schedule) as
**Derived Cognition** (Infer) — recomputable, a CHR appended per generation, two-axis replay,
user-editable. A user edit to a generated artifact is admitted as a **new Attested input**
(existing Retain path) that triggers 00R recompute → re-synthesis supersedes the prior model
(history appended, prior CHR intact). This is the **first AI in the codebase**: it lands the
shared `llm_provider` adapter + the recorded-model-response fixture harness all later slices
reuse. Runs under Fast/Deep modes within the per-tier token budget; emits `ai_spend_recorded`.

## Source docs / constraints

- `20_handoff/contracts/WAVE_S_CONTRACT_PACKAGE_SYNTHESIS_ENGINE.md` — **A1–A7 govern**:
  A3 required (extraction 1–2; synthesis/generation 3–6), A4 forbidden (5 Criticals), A5
  states, A6 events, A7 invariants; §2 QA (positives + 5 Critical negatives + determinism
  tier); §3 OBS (events/audit/replay/drift); **DL-048 additions** (budget, routing,
  `ai_spend_recorded`).
- ADR-0004 (recorded fixtures), ADR-0006 (n/a here), `deep-task-decisions.md` #2–#7, #9–#11.
- Calibration §4c (Free routing extraction→nano, synthesis/generation→mini, Haiku fallback;
  budgets). LDM §2.1 (assertion), §3 (derived projection). DL-047 object additions
  (`SynthesizedPlanningModel`, `PlanningArtifact`).

## Locked decisions (from decisions file — do not re-derive)

- **LLM seam:** implement `services/llm_provider` as a Pydantic AI adapter, OpenAI primary /
  Anthropic fallback, **tier-keyed routing from config** (DL-054 cond. 3; DL-048 §4c). Real
  calls only when an env flag is set (dev/nightly); otherwise the provider is driven by a
  **recorded-model-response fixture** via `pydantic-ai` `TestModel`/`FunctionModel`. **No new
  package.**
- **Recorded-fixture harness** (shared, built here, under `tests/`): JSON fixtures stamped
  with `model_version` + `config`; loaded into a `FunctionModel`. Name it
  *recorded model-response fixture* — **never** `replay`/`cassette` (reserved-term guard).
- **Extraction:** add an LLM-backed `ClaimExtractor` implementation behind the EXISTING
  `perceive/extraction.py` `ClaimExtractor` Protocol (rule-based stays; LLM is a second impl
  selected by config). Extracted claims remain **Attested-evidence**, source-attributed,
  re-derivable; **no severity/score/Derived** (the `AssertionDraft` shape already forbids it).
- **Synthesis/generation in `responsibilities/infer/`:** produce `SynthesizedPlanningModel` +
  `PlanningArtifact`s as Derived (`epistemic_state=derived`); **append one CHR per generation
  via `ctx.chr_repo`** when run as the injected `infer` stage (decisions #4); flag every
  inferred assumption explicitly (never silent gap-fill).
- **User edit = new Attested input** through the existing Retain admission path → 00R
  recompute → re-synthesis supersedes. Infer **never** autonomously edits an artifact and
  **never** writes a generated artifact to a canonical table as Attested.
- **Persistence default:** generic `derived` projection + CHR `output_kind`/`output_payload`
  (`output_kind ∈ {synthesized_planning_model, planning_artifact}`). **No new migration** — a
  typed-table need ⇒ STOP and escalate (owner approval).
- **Cost governance:** synthesis/generation run within the per-tier budget; per-run
  over-budget → partial model from highest-priority evidence + defer (coalesced Deep); emit
  `ai_spend_recorded` (`tokens_in/out, est_cost, tier, user, mode, model`). Regeneration on
  edits is coalesced (no per-keystroke spend).
- **Modes/stage:** carry `mode` + `confidence_stage`/`understanding_state` on each emission +
  CHR (attributes, not objects).

## Owned files / boundaries

- **OWN (create/extend, additive):**
  `backend/services/llm_provider/**` (adapter, routing, budget accounting) ·
  `backend/responsibilities/infer/**` (synthesis + generation; **not** Findings — that is
  DTM-0010) · `backend/responsibilities/perceive/extraction.py` (ADD the LLM extractor impl
  only; rule-based + `AssertionDraft` + Protocol stay byte-intact) ·
  `backend/services/observability/events.py` (ADD `EVENT_NAMES_WS` + `EVENT_NAMES_COST`,
  extend union) · `code/ci/gate_observability.py` (additive vocab + tamper tests) ·
  `shared/entities.py` / `shared/epistemic.py` (ADD `SynthesizedPlanningModel`,
  `PlanningArtifact` types) · `tests/{positive,negative}/synthesis/**`, `tests/replay/**`,
  and `tests/_fixtures/recorded_model_responses/**` (the shared harness).
- **READ-ONLY:** `orchestration/**` (consume via `register_stage("infer", …)` + `StageContext`
  only — no topology/state edit) · `responsibilities/retain/**`, `adapt/**` · **ALL
  migrations** (schema gap → STOP) · all Wave A `events.py` tuples (extend, never edit).

## Packages / refactors

- None new (`pydantic-ai` already approved). No refactors; rule-based extractor untouched.

## Implementation instructions (TDD)

1. **Red first** — QA-mapped tests: `test_b2_*` (WS positives), `test_b3_*` (WS Critical
   negatives), determinism (exact attribution / semantic synthesis), cost (`ai_spend_recorded`,
   over-budget degrade), recorded-fixture harness self-test.
2. Build the **recorded-fixture harness** + `llm_provider` adapter (offline by default).
3. LLM `ClaimExtractor` behind the Protocol → typed, source-attributed Attested drafts.
4. `SynthesizedPlanningModel` synthesis (evidence→context→construction; assumptions flagged)
   → seven `PlanningArtifact` generators (Derived; CHR per generation via `ctx.chr_repo`).
5. Wire as the injected `infer` stage for synthesis emissions; events + gate-5 vocab; OBS
   audit (which assertions + model/prompt version + assumptions) + replay (record-exact
   emission; semantic derivation).
6. Integration: admit evidence (DTM-0008) → synthesize → artifacts generated as Derived with
   CHRs → user edit admitted as new Attested input → 00R recompute → re-synthesis supersedes.

## API / data / schema contracts

- `SynthesizedPlanningModel` / `PlanningArtifact`: Derived, `epistemic_state=derived`, carry
  `mode`/`confidence_stage`, lineage to source `AttestedAssertion`s + flagged assumptions.
- CHR per generation: `output_kind`, `output_payload`, `input_attestation_version`,
  `model_or_rule_version`, `upstream_lineage`, `recompute_trigger`. No schema change.

## Test plan (QA-WS-SYNTH)

- **Positive (`test_b2_*`):** source-attributed, correctly-typed extraction, re-derivable;
  seven Derived artifact types each with a CHR; user edit → new Attested input → recompute →
  prior superseded (prior CHR intact); Evaluate-seed seam (PS-03) exercised; assumptions
  flagged Derived; Free-tier run ≤ budget; over-budget → partial + defer + emit.
- **Negative (`test_b3_*`, each Critical unless noted):** Perceive emitting Finding/severity/
  confidence, or an **unattributed** assertion *(Major)*; generated artifact **written
  canonical as Attested**; artifact **changed without recompute** / **CHR overwritten**;
  **silent gap-fill** (assumption as evidence-attested fact); **autonomous artifact write**;
  budget bypass / runaway regeneration / silent overspend / wrong-tier routing (DL-048).
- **Determinism:** explicit attributions **exact**; AI-synthesized model/artifacts
  **semantic-equivalent** (same plan identity/intent), set-level ≥90% stable sections.
- **Harness self-test:** PR CI makes **zero** provider calls; fixtures carry `model_version`.
- Full suite + ruff + gate-4 + gate-5 green; Wave-A baseline (327) must not regress.

## Manual checks (EM)

- Grep/AST: no provider import is reachable from `pytest` without the env flag.
- Studio: `SynthesizedPlanningModel`/artifacts visible as Derived projections + CHRs; no
  generated artifact in a canonical table.
- Dev: one live synthesis run produces an `ai_spend_recorded` event with real token counts.

## Done criteria

- WS-SYNTH B2/B3 traceability table in the worker report; recorded-fixture harness in place
  and reused-ready; AI offline-deterministic in CI; PR cites `IC-WS-SYNTH`; no migration; no
  new package. Ready for DTM-0010.

## Worker report

_(worker fills: built files, B2/B3→test map, exact commands + results, flags)_

## Engineering-manager review notes

_(EM fills after diff inspection + independent verification)_

## Approved by engineering manager

_(added only after verification passes)_
