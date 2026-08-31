# Deep-task decisions — Wave B: Understanding (Synthesis · Infer · Evaluate)

Implementation-control record for the Wave B sequence. Cites source-of-truth; does not
restate it. **Branch:** `feat/phase3-waveb-understanding` (ADRs already committed `c316a82`).

## Source-of-truth docs (binding; read, do not edit from deep-task)

- **Contracts:** `20_handoff/contracts/WAVE_S_CONTRACT_PACKAGE_SYNTHESIS_ENGINE.md`
  (IC/QA/OBS-WS-SYNTH; A1–A7, §2 QA, §3 OBS, DL-048 additions) ·
  `20_handoff/contracts/WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING.md`
  (IC/QA/OBS-WB-INFER §1, IC/QA/OBS-WB-EVAL §2, §0.1 modes, DL-047 + DL-048 additions) ·
  `20_handoff/contracts/WAVE_B_CONTRACT_AMENDMENT_FAST_DEEP_60S_DISPOSITION.md` (DL-046 A–G).
- **ADRs (locked this phase):** `code/docs/adr/0004` (recorded model-response test strategy),
  `0005` (3-slice build plan), `0006` (v0 scoring adoption), `0001` (monorepo ratified).
- **Scoring:** `30_engineering/scoring/CAF_CONFIDENCE_V0_SCORING_FORMULA_V1.md` (v0 arithmetic) ·
  `…/CONFIDENCE_MODEL_V2.md` · `…/RELIABILITY_MODEL_V2.md` · `…/CAF_SCORING_MODEL_V2.md` (meaning).
- **Calibration / determinism:** `30_engineering/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md`
  (§1 tiers, §2 bands, §3 drift, §4c routing/budgets, §4h CAF/Confidence params) ·
  `30_engineering/testing_fixtures/DETERMINISM_CALIBRATION_NOTE_001.md` (DT-3/5/6/10; REPLAY reserved).
- **Architecture / model:** `30_engineering/specifications/OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md` ·
  `30_engineering/runtime_models/RELEASE_1_LOGICAL_DATA_MODEL_V1.md` (§2 canonical, §3 derived projection).
- **Anti-assumption:** `00_owner/ANTI_ASSUMPTION_BUILD_PROTOCOL.md` (scaffold metric; never invent a number).
- **Plan:** `code/docs/deep-tasks/waveb-understanding-deep-task/deep-task-plan.md`.

## Repo facts (current code, grounding the slices)

- Stage seam: `orchestration/stages.py` — `register_stage(name, fn)` replaces
  `wave_b_placeholder_infer` / `wave_b_placeholder_evaluate`; `CHAIN_STAGE_ORDER =
  (retain, infer, evaluate, advise)`; `StageContext(emitter, chr_repo)` already carries the
  append-only `ChrRepository`. Graph topology in `orchestration/graphs/deep_pass.py` is
  fixed (`append_chrs → stage_infer → stage_evaluate → stage_advise`); Wave B injects, never
  re-wires.
- Extraction seam: `responsibilities/perceive/extraction.py` — `ClaimExtractor` Protocol +
  `RuleBasedExtractor` (version `wa001-e1`, tier EXACT). Wave S wires an LLM-backed extractor
  behind the SAME `ClaimExtractor` interface (decision #5 already anticipates this).
- LLM: `services/llm_provider/__init__.py` is a one-line stub; `pydantic-ai>=0.0.14` already
  declared in `pyproject.toml`. Keys empty by design (Wave A was records/rules).
- Events: `services/observability/events.py` — per-contract pinned tuples (`EVENT_NAMES_WA00R/
  WA001/WA002`) + union `EVENT_NAMES`; `CollectingEventEmitter` rejects unknown names;
  gate-5 (`ci/gate_observability.py`) asserts the vocab verbatim. Wave B extends additively.
- Epistemic: `shared/epistemic.py` — `EpistemicState` enum (`attested-evidence|oslo|user|
  derived`); `CANONICAL_OUTPUTS` already lists `Finding, Issue, Confidence, CAFAssessment,
  OutcomeConfidence, SynthesizedPlanningModel, PlanningArtifact`. New cognition types subclass
  `CognitionEntity` (carries `epistemic_state`).
- Schema: canonical append-only tables + a `derived` projection schema exist (DTM-0002
  migrations). `cognition_history_record` is the per-emission receipt.

## Locked decisions (apply to all three slices unless noted)

1. **One fresh worker per slice, strictly sequential** (ADR-0005): DTM-0009 → DTM-0010 →
   DTM-0011. No slice starts until the prior is reviewed, fixed, verified, approved.
2. **AI test wiring = recorded model-response fixtures** (ADR-0004). Live model in dev +
   nightly baseline-update only; **PR CI never calls a provider.** Implement with
   `pydantic-ai`'s `TestModel`/`FunctionModel` driven from in-repo JSON fixtures — **no new
   package.** Each fixture stamps `model_version` + `config` (the model/fixture component of
   the `(config × fixture × model-version)` determinism baseline, DT-5/10).
3. **Reserved-term guard:** the LLM double is a **recorded model-response fixture** — never
   named `replay`/`cassette` in code or test names. `replay` stays reserved for event-log
   reconstruction that does not re-run the LLM (Determinism Note §5; CONTEXT.md Register).
   The nightly live diff is a **baseline-update check, not a regression** (DT-6).
4. **CHR-append seam (architectural lock):** the real Infer/Evaluate stages append each
   emission's CHR through `ctx.chr_repo` (Retain's append-only `ChrRepository`) and emit via
   `ctx.emitter` — preserving *CHR-is-Retain-owned* (A3.5 of 00R) and *one producer per
   output* (Infer owns Finding CHRs; Evaluate owns Issue/Confidence/CAF/OutcomeConfidence
   CHRs). **No change to `deep_pass.py` topology** — injection via `register_stage` only. The
   head `append_chrs` continues to drain any trigger-declared emissions (zero in a pure
   cognition recompute — Wave B real producers replace the Wave-A trigger-declared stub,
   DTM-0008 flag #2).
5. **Derived, never Attested.** All Wave B/S output carries `epistemic_state = derived`;
   nothing is written to a canonical table as Attested. The only Attested write Wave S causes
   is the **user's edit** of a generated artifact, admitted as a *new Attested input* via the
   existing Retain admission path (DTM-0008) → triggers 00R recompute. Workers do not invent
   a new admission path.
6. **mode + confidence_stage are attributes, not objects** (DL-046): `mode ∈ {fast, deep}`,
   `confidence_stage ∈ {orientation, expanded, validated}`, `understanding_state ∈ {initial,
   partial, refined, validated, mature}` (DL-047 AE-04). Carried on each emission **and** its
   CHR. A stage/state change without recompute is a Critical invariant breach (test it).
7. **Cost governance (DL-048):** Fast/Deep + synthesis run within per-tier token budgets from
   config (Calibration §4c: Free Fast 150k/run, Deep 600k/run, daily 500k, monthly 4M;
   routing extraction→nano, synthesis/eval→mini, Haiku fallback). Over-budget → graceful
   degradation (Fast truncates → partial orientation; Deep coalesces/defers), **never** silent
   overspend or runaway re-analysis; emit `ai_spend_recorded`. Cap *numbers* are config; the
   *enforcement* is contracted.
8. **v0 scoring** (ADR-0006, DTM-0011): implement `CAF_CONFIDENCE_V0` arithmetic
   (per-dim `100·Π(1−impactᵢ)`, power-mean p≤1 with ε floor, bands 0–49/50–74/75–100 ±3 edge
   guard, reliability a separate qualifier). Pin `rule_version` (e.g. `wb-eval-caf-v0`) into
   the determinism baseline → rule-arithmetic replays **exact**. v0 params live in config
   (Calibration §4h); **scaffold the calibration harness, assert no hard threshold** until the
   owner sets it (Anti-Assumption). v0 introduces no new dimension/entity/state/probability.
9. **Event vocab additions** (additive, decision-#1 pattern + gate-5), derived from the OBS
   contracts (worker pins verbatim against each A6/C2):
   - `EVENT_NAMES_WS = (claim_extracted, planning_artifact_generated,
     planning_artifact_regenerated, synthesized_model_updated)`
   - `EVENT_NAMES_WB_INFER = (finding_detected, finding_superseded)`
   - `EVENT_NAMES_WB_EVAL = (issue_generated, caf_assessed, outcome_confidence_computed,
     understanding_state_changed, false_confidence_flagged)`
   - `EVENT_NAMES_COST = (ai_spend_recorded,)` — single shared shape, introduced in DTM-0009.
   `cognition_history_record_appended` is reused (already in WA00R). Union extended; gate-5
   updated with per-contract verbatim + union + tamper negatives (DTM-0007/0008 pattern).
10. **Determinism tiers** (Calibration §1): rule/formula + explicit attributions = **exact**;
    AI-numeric (Confidence/CAF/Reliability/OutcomeConfidence) = **±7 & same band**; AI-text
    (Findings/Issues/artifacts) = **semantic-equivalent**; set-level ≥90% stable-identity
    overlap. Two-axis replay: record-exact emission + derivation-by-tier.
11. **Determinism baseline (CI):** AI exercised only through recorded fixtures; the
    `RECORDED_MODEL_FIXTURES`-style harness lives under `tests/` and is shared across slices
    (DTM-0009 builds it first). No provider call in `pytest`/PR CI; live runs gated behind an
    env flag used by dev + the nightly job only.

## Packages

- **Approved (already declared):** `pydantic-ai` (LLM adapter + `TestModel`/`FunctionModel`
  for fixtures). No new runtime dependency for Wave B.
- **Not approved / do not add:** any VCR/cassette library (reserved-term + dependency drift —
  build the fixture harness in-repo), any new vector/graph/LLM SDK. New dependency ⇒ STOP
  (CLAUDE.md STOP-rule 4, owner approval).

## Refactors

- None pre-approved. Placeholders are replaced via `register_stage`; `deep_pass.py`,
  `state.py`, `runner.py`, `checkpointer.py` are **read-only** (a topology/state change ⇒
  STOP and escalate). Existing `retain`/`perceive`/`adapt` modules are read-only except the
  additive `ClaimExtractor` implementation point (DTM-0009).
- **Infer-node fusion (EM ruling 2026-06-17):** the single `infer` chain node holds one fn,
  but Infer now spans synthesis (DTM-0009) + finding (DTM-0010), each proven at stage-fn
  level. Resolution: DTM-0011 adds an **additive** `orchestration/wave_b.py` that composes a
  single `infer` stage (synthesis→finding, by *calling* the frozen stage fns) and registers
  `evaluate`, then proves one live end-to-end. No edit to the frozen stage files or graph
  topology. This is the only orchestration-write authorized for Wave B.

## Open conflicts / escalations (must resolve before the affected slice codes)

- **OWNER GATE — Wave B start (DL-044 cond. 2): CLEARED — owner authorized 2026-06-17.**
  DTM-0009 coding proceeds; DTM-0010/0011 remain sequentially gated on prior-slice approval.
- **LLM keys (Day-0):** dev + nightly need `OPENAI_API_KEY` / `ANTHROPIC_API_KEY`; PR CI does
  not. Owner provisioning is parallel, not blocking PR CI (fixtures cover it).
- **Schema for Derived types (SCHEMA):** persist via the **generic CHR `output_kind`/
  `output_payload`** (no typed tables). **RESOLVED for Wave S — owner approved 2026-06-17:**
  the canonical CHR `output_kind` CHECK + `retain/models.py` `OutputKind` Literal are widened
  by **exactly two** values (`synthesized_planning_model`, `planning_artifact`) via a new
  append-only-preserving migration (DTM-0002 predates needing them; append-only discipline
  unchanged). This authorizes DTM-0009 to add that migration + the 2 Literal values **only**.
  Wave B kinds (finding/issue/confidence/caf/outcome_confidence/…) already exist in the CHECK
  — no migration needed for DTM-0010/0011. Any **further** typed-table or kind beyond these
  two ⇒ STOP and escalate.
- **Open-TBD (non-blocking, scaffold-only):** Fast/Deep p50/p95 + project-size envelope (A2/A1)
  and the v0 calibration table (F1) are owner-deferred — scaffold the gate/harness, assert no
  numeric pass/fail (Anti-Assumption). The `<60s` ceiling itself is ratified (assert it as the
  bound; envelope value is the owner's).

## Slice index

| Task | Contract | File |
|---|---|---|
| DTM-0009 | IC/QA/OBS-WS-SYNTH (+ DL-048) | `deep-task-0009.md` |
| DTM-0010 | IC/QA/OBS-WB-INFER (+ DL-046) | `deep-task-0010.md` |
| DTM-0011 | IC/QA/OBS-WB-EVAL (+ DL-046/047/048, v0) | `deep-task-0011.md` |
