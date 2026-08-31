# DTM-0011 — Evaluate: Issue, Confidence, Reliability, CAF, Outcome Confidence (v0), <60s gate

**Status:** **Approved** (EM, 2026-06-17) · **Module:** DTM-0011 · **Phase:** III
(Wave B) · **Contract:** **IC/QA/OBS-WB-EVAL** (+ DL-046, DL-047, DL-048; v0 per ADR-0006) ·
**Depends:** DTM-0009 (`148400f`), DTM-0010 (`5e1e13f`). · **Also delivered:** the live
**infer-node fusion** (synthesis→finding) + full Wave-B chain wiring (`orchestration/wave_b.py`).

> ## Carried integration scope (EM ruling 2026-06-17) — the live chain
> DTM-0009 (synthesis) and DTM-0010 (finding) are each proven at the stage-fn level but not
> wired into the live graph (the single `infer` chain node can hold one fn). DTM-0011 wires
> the whole Wave-B chain live so Evaluate's own DoD (end-to-end Fast Pass <60s; "why did
> confidence change" via recompute) is demonstrable:
> - Add an **additive** orchestration-wiring module (e.g. `backend/orchestration/wave_b.py`)
>   that builds a **composed `infer` stage** = run DTM-0009 synthesis **then** DTM-0010 finding
>   over the same run (synthesis produces the model; finding analyzes it), and the **`evaluate`
>   stage** (this slice), and registers both via `register_stage(...)`.
> - **Do NOT edit** the frozen `infer/stage.py` (synthesis) or `infer/finding_stage.py`
>   (finding), `deep_pass.py` topology, `state.py`, or the `runner.py` core — compose by
>   *calling* the existing stage fns. If composition needs a topology/state change ⇒ STOP and
>   escalate.
> - Prove one **live end-to-end**: admit evidence → composed infer (model + findings) →
>   evaluate (issues + confidence/CAF/outcome) → CHRs appended → Fast-Pass Time-to-First-MRI
>   `<60s` on the fixture envelope; a recompute supersedes and the confidence delta is
>   reconstructable from CHR lineage. Env-gate the live (Supabase) parts to skip offline.

## Goal / observable behavior

Evaluate assesses the **current state**: assigns **severity** to Findings (→ **Issues**),
computes **Confidence** (trust in understanding — **never** project health) and **Reliability**,
computes the **CAF Assessment** (Clarity/Alignment/Feasibility) and **Outcome Confidence**
(aggregate) using the **v0 scoring formula**, seeds initial CAF/Confidence from the
`SynthesizedPlanningModel` (PS-03), and flags **False Confidence** (CONF-06). Each emission
appends a CHR (input-version + model/rule version + lineage) via `ctx.chr_repo`; recompute
supersedes — this is the **"why did confidence change?"** backbone (answerable from CHR
lineage). Confidence is **banded** (0–49/50–74/75–100, ±3 edge guard), reliability-qualified.
Fast Pass yields **Orientation**-stage; Deep Pass matures toward **Validated** via recompute.
A QA test asserts **Time-to-First-MRI < 60s** on the supported envelope.

## Source docs / constraints

- `WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING.md` §2 (IC-WB-EVAL 2.1 required/forbidden/confidence-
  semantics/invariants; QA 2.2 positive/negative/classification/determinism/**performance
  gate**/regression anchors; OBS 2.3 events/audit/replay/drift) + §0.1 modes + **DL-047
  additions** (PS-03 seed, **CONF-06 false-confidence**, AE-04 understanding-state) + **DL-048**
  (budget/routing/`ai_spend_recorded`).
- `WAVE_B_CONTRACT_AMENDMENT_FAST_DEEP_60S_DISPOSITION.md` C (#5 stage), D (**performance
  gate**, negatives, classification), E (OBS).
- **`30_engineering/scoring/CAF_CONFIDENCE_V0_SCORING_FORMULA_V1.md`** (the arithmetic) +
  `CONFIDENCE_MODEL_V2` / `RELIABILITY_MODEL_V2` / `CAF_SCORING_MODEL_V2` (meaning, properties,
  bands). `Calibration §2` bands, `§3` drift (≥10 pts or band change), `§4h` v0 params.
- ADR-0006 (v0 adoption, pin, scaffold calibration), `ANTI_ASSUMPTION_BUILD_PROTOCOL`,
  decisions #4–#11.

## Locked decisions

- **Producer boundary:** Evaluate is the **single producer** of Issues + Severity/Confidence/
  Reliability attributes + CAF + Outcome Confidence. It **must not** generate Findings (Infer)
  or recommendations/clarifications (Advise), write canonical / promote to Attested, govern
  exposure, accept an interpretation as truth, or change any value outside recompute.
- **v0 scoring** (ADR-0006): implement `CAF_CONFIDENCE_V0` exactly — per-dim
  `Dim = 100·Π(1−impactᵢ)` clamped [0,100]; consolidate the three floored dims with a
  **power-mean p≤1** + dimension floor `ε`; **bands** 0–49/50–74/75–100 with the **±3
  edge-guard**; **Reliability is a separate qualifier label, never multiplied in**; obey the
  **Non-Collapse Invariant** (low reliability alone must not drive Very Low when CAF strong).
  **Pin `rule_version` (`wb-eval-caf-v0`)** into the determinism baseline → rule-arithmetic
  replays **exact**; v0 params come from config (Calibration §4h). **Scaffold the calibration
  harness; assert NO hard numeric threshold** beyond the doctrinal band/±7 tier (Anti-
  Assumption). Finding type is a label, never a coefficient — magnitude comes from each
  Finding's Impact Assessment.
- **Confidence semantics:** trust in understanding, never project health/readiness/probability/
  score; band-level stable under semantic replay. CAF/Outcome Confidence are derived aggregates.
- **CONF-06 false confidence (mandatory):** flag high confidence built on low-reliability/
  low-coverage understanding; emit `false_confidence_flagged`. **QA negative:** high confidence
  over weak understanding **without** a flag.
- **Understanding state (AE-04):** classify Initial→Partial→Refined→Validated→Mature
  (attribute; extends `confidence_stage`); emit `understanding_state_changed`; never
  Unknown→Final-Truth; changes only via recompute.
- **Replace the `evaluate` placeholder** via `register_stage("evaluate", …)`; CHRs via
  `ctx.chr_repo`; topology unchanged. **Persistence default:** generic `derived` projection +
  CHR (`output_kind ∈ {issue, confidence, reliability, caf, outcome_confidence}`). No new
  migration (typed-table need ⇒ STOP/escalate).
- **Cost + perf:** run within per-tier budget (Free→mini, Haiku fallback); emit
  `ai_spend_recorded`; **performance test asserts Time-to-First-MRI < 60s** on the supported
  envelope — **envelope value + p50/p95 are owner-TBD (A1/A2): assert the `<60s` bound,
  scaffold the gate, do not invent the envelope number** (Anti-Assumption).
- Determinism: rule/formula components **exact**; AI-assisted confidence **band-semantic**
  (±7 & same band).

## Owned files / boundaries

- **OWN (additive):** `backend/responsibilities/evaluate/**` (severity → Issue; v0 scoring
  engine: Confidence/Reliability/CAF/OutcomeConfidence; false-confidence; understanding-state;
  PS-03 seed) · `events.py` (ADD `EVENT_NAMES_WB_EVAL`, extend union) ·
  `ci/gate_observability.py` (additive) · `shared/` (ADD `Issue`, `Confidence`,
  `CAFAssessment`, `OutcomeConfidence` types) · `tests/{positive,negative}/evaluate/**`,
  `tests/replay/**`, additive recorded fixtures · a **calibration harness** scaffold under
  `tests/` or `backend/.../scoring` (records inputs to fit `p/ε/impact` later; asserts no
  threshold).
- **OWN (carried integration, additive only):** a NEW `backend/orchestration/wave_b.py`
  wiring module that composes the `infer` node (synthesis→finding) + registers the `evaluate`
  stage via `register_stage(...)`, and a live end-to-end test under `tests/positive/`.
- **READ-ONLY:** `orchestration/**` EXCEPT the new additive `wave_b.py` (do NOT edit
  `deep_pass.py`/`state.py`/`runner.py` core or `registry.py`) · `infer/**` (call the existing
  synthesis + finding stage fns; do NOT edit `stage.py`/`finding_stage.py`) · `retain/**`,
  `perceive/**`, `adapt/**`, all DTM-0009/0010 modules · ALL migrations · the v0 formula doc +
  scoring models (cite, do not edit) · Wave A/S/B-Infer event tuples.

## Packages / refactors

- None new. No refactors (placeholder replaced via registry).

## Implementation instructions (TDD)

1. Red: `test_b2_*` (Issue formation, v0 scoring values + bands + reliability qualifier, CAF
   aggregation, Outcome Confidence, PS-03 seed, drift surfaced, both modes/stage, **<60s perf
   gate**) and `test_b3_*` (every forbidden behavior + confidence-as-health + false-confidence-
   without-flag + stage-without-recompute) first.
2. Severity → Issue from Finding; v0 CAF/Confidence/Reliability/OutcomeConfidence engine
   (exact arithmetic, `rule_version` pinned); Non-Collapse + band-edge guard.
3. CONF-06 false-confidence detector + `false_confidence_flagged`; understanding-state
   classifier + `understanding_state_changed`.
4. Inject as `evaluate` stage; CHR per value via `ctx.chr_repo`; emit `issue_generated`/
   `caf_assessed`/`outcome_confidence_computed`; events + gate-5 vocab; `ai_spend_recorded`.
5. Calibration harness scaffold (no thresholds). OBS audit (input-version, model/rule version,
   upstream Finding/Issue lineage) + replay (record-exact emission; band-semantic derivation,
   exact for formula components).
6. Integration: 00R recompute supersedes values; a confidence change is **explainable** from
   CHR lineage (the "why did Outcome Confidence drop 84→61" capability); drift ≥10 pts / band
   change surfaced; Deep Pass matures stage without blocking the user.

## API / data / schema contracts

- `Issue` (Core, Derived); `Confidence` = (band · reliability_qualifier · basis) — never a
  bare number; `CAFAssessment` = three dims each (index · band · per-dim reliability);
  `OutcomeConfidence` (aggregate). All Derived; CHR per emission carries input/model version +
  lineage; carry `mode`/`confidence_stage`/`understanding_state`. No schema change.

## Test plan (QA-WB-EVAL)

- **Positive (`test_b2_*`):** severity → Issue; Confidence/Reliability computed (epistemic
  state); CAF + Outcome Confidence aggregated (v0, exact rule replay); per-emission CHR with
  lineage; recompute supersedes (prior intact); confidence change **explainable** from
  history; both modes + stage maturation; PS-03 seed from synthesized model; **performance
  gate Time-to-First-MRI < 60s**.
- **Negative (`test_b3_*`):** Evaluate generating Findings/Recommendations; **confidence
  interpreted as project health** *(Critical)*; value changed **without recompute** / CHR
  overwritten / Derived→Attested *(Critical)*; accepting an interpretation; assessment changed
  by intake/acceptance alone; **false confidence without a flag** (CONF-06); `confidence_stage`/
  understanding-state changing without recompute or modeled as an object *(Critical)*; Fast
  Pass exceeding 60s on the envelope *(Major)*; Deep Pass blocking the user; cost bypass /
  silent overspend / wrong-tier routing.
- **Determinism:** formula components **exact** (pinned `rule_version`); AI confidence
  **±7 & same band**; band stability under semantic replay.
- AI offline via recorded fixtures; no provider call in PR CI.
- Full suite + ruff + gate-4 + gate-5 green; baseline must not regress.

## Manual checks (EM)

- Replay a recorded fixture twice → identical bands; nightly live diff treated as a
  **baseline update, not a regression** (DT-6).
- Studio/CHR: change a Finding → recompute → Outcome Confidence delta is reconstructable from
  CHR lineage with input/model version.
- Confirm the calibration harness asserts **no** numeric pass/fail (only the doctrinal band/±7).

## Done criteria

- WB-EVAL B2/B3 (+DL-046/047/048) traceability in report; v0 scoring exact-replays under its
  pinned `rule_version`; confidence-as-health and false-confidence-without-flag both
  negative-proven; `<60s` gate present (envelope owner-TBD, scaffolded); PR cites
  `IC-WB-EVAL`; no migration/package. **Wave B candidate-complete → owner exit-gate review
  before Phase IV / Wave C.**

## Worker report

**Ready for review.**

DTM-0011 (IC/QA/OBS-WB-EVAL, +DL-046/047/048, v0 per ADR-0006) is implemented as
**Part A** (the Evaluate responsibility + v0 scoring engine) and **Part B** (the
live Wave-B chain fusion). No migration, no new package, no canonical-schema
change, no hard numeric threshold (calibration scaffolded only), no edit to any
frozen DTM-0009/0010 module or to `deep_pass`/`state`/`runner`/`registry`. Did
NOT git commit.

### Files built / changed

| File | Part | What |
|---|---|---|
| `shared/epistemic.py` | A | ADD `Issue`, `Confidence`, `Reliability`, `CAFAssessment` (+`CAFDimensionScore`), `OutcomeConfidence` + the `Severity`/`ReliabilityLevel`/`ConfidenceBand`/`CAFDimension` Literals. All Derived; `extra='forbid'` forbids a `score`/`health`/`probability`/`recommendation` field structurally. |
| `backend/responsibilities/evaluate/config.py` | A | v0 params (Calibration §4h) as DIALS: impact table, `p=−0.5`, `ε=5`, band edges (50/75) + ±3 guard. Owner-tunable; no asserted threshold. |
| `backend/responsibilities/evaluate/scoring.py` | A | The v0 arithmetic EXACT: `per_dimension_index` (`100·Π(1−impactᵢ)`), `power_mean` (floored, p≤1), `band_for` (±3 edge guard). Pins `CAF_RULE_VERSION="wb-eval-caf-v0"`. |
| `backend/responsibilities/evaluate/engine.py` | A | `EvaluateEngine`: severity→Issue; CAF/Confidence/Reliability/OutcomeConfidence; CONF-06 false-confidence; AE-04 understanding-state classifier; PS-03 seed from the model; Non-Collapse (band from index only); reliability a separate qualifier. NO provider call. |
| `backend/responsibilities/evaluate/stage.py` | A | The injected `evaluate` stage: one CHR per value via `ctx.chr_repo` (`output_kind ∈ {issue,confidence,reliability,caf,outcome_confidence}` — all already in CHECK+Literal); lineage; recompute supersedes; `mode`+`confidence_stage`; emits `issue_generated`/`caf_assessed`/`outcome_confidence_computed`/`understanding_state_changed`/`false_confidence_flagged` + `ai_spend_recorded` (with Time-to-First-MRI latency). |
| `backend/responsibilities/evaluate/calibration.py` | A | Calibration-harness SCAFFOLD: `CalibrationRecorder` records inputs to fit `p`/`ε`/impact later; asserts NO pass/fail threshold (Anti-Assumption). |
| `backend/responsibilities/evaluate/__init__.py` | A | Public surface export. |
| `backend/services/observability/events.py` | A | ADD `EVENT_NAMES_WB_EVAL` (5 events, verbatim vs OBS-WB-EVAL §2.3 + DL-047); extend the union (now 7-way). |
| `ci/gate_observability.py` | A | Additive `EXPECTED_EVENT_NAMES_WB_EVAL` + contract-vocab + union order (tamper-checked). |
| `tests/positive/observability/test_gate_observability.py` | A | UPDATED for the new tuple (verbatim WB_EVAL test + 7-way union + leak checks). |
| `tests/negative/observability/test_gate_observability_negative.py` | A | UPDATED: WB_EVAL added to `GOOD_EVENTS_PY` + rename/missing tamper negatives + count fix (now 8 = 7 tuples + union). |
| `backend/orchestration/wave_b.py` | **B** | NEW additive wiring: `WaveBChain` builds a **composed `infer`** stage = `run_synthesis_stage` THEN `run_finding_stage` over the same run (by CALLING the frozen fns), and the `evaluate` stage; `register_stage("infer"/"evaluate", …)`. |
| `tests/positive/evaluate/**` (8 files) | A+B | helpers + `test_b2_*` (issue/scoring, CAF/outcome, seed/state, determinism, stage, drift/calibration, perf gate, **wave-b composition**, **live e2e**). |
| `tests/negative/evaluate/**` (4 files) | A | `test_b3_*` (producer boundary, confidence semantics, recompute/invariants, cost/perf). |

### B2/B3 → test traceability

| Contract requirement | Test |
|---|---|
| Severity → Issue from a Finding | `test_b2_issue_and_scoring::test_b2_severity_assigned_forms_issue_from_finding`, `..._is_a_label_not_a_score_and_scales_with_magnitude` |
| v0 per-dim `100·Π(1−impactᵢ)` + bands + ±3 edge guard | `test_b2_issue_and_scoring::test_b2_no_findings_dimension…`, `…single_material_weakness…`, `…band_edge_guard…`, `…accumulate_multiplicatively…` |
| CAF aggregation (power mean, between avg & min) | `test_b2_caf_and_outcome::test_b2_outcome_confidence_is_power_mean…`, `…between_average_and_minimum` |
| Outcome Confidence (aggregate) | `test_b2_caf_and_outcome::test_b2_outcome_confidence_is_power_mean…` |
| Reliability separate qualifier (never multiplied in) | `test_b2_caf_and_outcome::test_b2_reliability_is_a_separate_qualifier…`; `test_b3_confidence_semantics::test_b3_reliability_is_not_multiplied…` |
| **Non-Collapse invariant** | `test_b2_caf_and_outcome::test_b2_non_collapse_low_reliability_alone…` |
| **CONF-06 false-confidence (flag)** | `test_b2_caf_and_outcome::test_b2_conf06_false_confidence…`; stage `test_b2_stage::test_b2_false_confidence_flagged_event…` |
| CONF-06 negative (no silent drop) | `test_b3_confidence_semantics::test_b3_false_confidence_is_never_silently_dropped_conf06` |
| **PS-03 seed from SynthesizedPlanningModel** | `test_b2_seed_and_state::test_b2_ps03_seeds_confidence…`, `…without_a_model_cannot_be_past_initial` |
| AE-04 understanding-state (Initial→…→Mature; never →Final-Truth) | `test_b2_seed_and_state::test_b2_understanding_state_*`, `…never_skipping_to_truth` |
| Drift surfaced ≥10 pts / band change | `test_b2_drift_and_calibration::test_b2_confidence_drop…`, `…band_change_is_drift…` |
| Both modes + stage maturation | `test_b2_stage::test_b2_deep_pass_carries_deep_mode…`; `test_b2_seed_and_state::test_b2_state_progression_matures…` |
| **v0 EXACT replay under pinned rule_version** | `test_b2_determinism::test_b2_identical_inputs_replay_exact…`, `…per_dimension_arithmetic_is_exact`; AI ±7/band: `…ai_impact_jitter_stays_within_band_and_pm7` |
| CHR per value + lineage + recompute supersedes | `test_b2_stage::test_b2_one_chr_per_value…`, `…every_chr_carries_input_version…`, `…recompute_appends_new_values…` |
| "why did confidence change" reconstructable | `test_b2_stage::test_b2_why_did_confidence_change_reconstructable_from_chr_lineage` |
| **PERFORMANCE GATE <60s** | `test_b2_performance_gate::test_b2_fast_pass_evaluate_under_60s_ceiling`, `…emits_time_to_first_mri_latency_within_ceiling`; live: `test_b2_live_chain_e2e` |
| Confidence-as-health (Critical) | `test_b3_confidence_semantics::test_b3_confidence_shape_forbids_a_health…`, `…outcome_confidence_shape_forbids…`, `…never_renders_confidence_as_a_project_health_number` |
| value-without-recompute / CHR-overwrite / Derived→Attested (Critical) | `test_b3_recompute_and_invariants::test_b3_values_are_frozen…`, `…recompute_appends_a_new_chr…`, `…chr_repo_has_no_update_or_delete…`; `test_b3_producer_boundary::test_b3_value_cannot_be_constructed_as_attested` |
| stage/state without recompute / as-object (Critical) | `test_b3_recompute_and_invariants::test_b3_stage_change_only_via_recompute…`, `…understanding_state_is_an_attribute_not_a_new_object` |
| Evaluate generating Findings/Recs; accepting interpretation | `test_b3_producer_boundary::test_b3_evaluate_exports_no_finding_or_recommendation_producer`, `…does_not_accept_an_interpretation…`, `…issue_carries_no_recommendation…` |
| assessment changed by intake/acceptance alone | `test_b3_recompute_and_invariants::test_b3_an_assessment_does_not_change_by_intake_or_acceptance_alone` |
| Fast Pass >60s (Major) | `test_b3_cost_and_performance::test_b3_a_simulated_over_ceiling_latency_would_breach_the_gate` |
| cost bypass / silent overspend / wrong-tier | `test_b3_cost_and_performance::test_b3_spend_records_the_configured_free_tier_model…`, `…spend_event_is_always_emitted…`, `…never_calls_a_provider…` |
| **Part B composition (offline)** | `test_b2_wave_b_composition::*` (composed infer synthesis→finding; evaluate reads handoff; per-run handoff; register replaces placeholders, topology unchanged) |
| **Part B live e2e** | `test_b2_live_chain_e2e::test_b2_live_chain_admit_infer_evaluate_under_60s_and_recompute_supersedes` (env-gated) |

### Exact commands + results

```
$ .venv/bin/python -m pytest tests/positive tests/negative tests/replay -q
444 passed, 68 skipped, 1 warning
  (baseline at HEAD 5e1e13f was 374 passed / 67 skipped — no regression; +70 new
   passed, +1 skip = the env-gated live e2e. Live counts: the Supabase suite was
   not run — offline only; the live e2e + the DTM-0005 backbone suite skip.)
$ .venv/bin/ruff check .
All checks passed!
$ .venv/bin/python -m ci.gate_invariants
[gate-4 epistemic-invariant] PASS: no forbidden tokens, no authority module,
  no canonical-table mutations in migrations.
$ .venv/bin/python -m ci.gate_observability
[gate-5 observability] PASS: every CHR-append call-site emits
  'cognition_history_record_appended', the per-contract A6 vocabularies are
  pinned verbatim (union consistent), and the replay harness is present.
```

(`python` is the venv interpreter `.venv/bin/python`; bare `python`/`pytest` are
not on PATH here.)

### Flags / notes for the EM

- **Part B composes without editing frozen files.** `wave_b.py` builds the
  composed `infer` stage by *calling* the frozen `run_synthesis_stage` then
  `run_finding_stage` over the same `ctx`, and the `evaluate` stage by calling
  `run_evaluate_stage`. Cross-node handoff (infer node → evaluate node) is an
  **in-memory, per-run dict keyed by `run_id`**, private to the `WaveBChain`
  closure pair — it changes NO graph topology, NO `GraphState` field, and NO
  frozen module. No topology/state change was needed, so no STOP was triggered.
- **`register_stage` is a global mutation.** The live e2e (and the composition
  `register()` test) SAVE the registry via `default_stages()` and RESTORE it in a
  fixture/`finally`, so the global swap never leaks into other suites (the
  placeholder-dependent backbone tests stay green). A real app would call
  `register()` once at boot; tests must restore — flagged so the EM knows the
  registry is process-global by design (decision #6).
- **Owner-TBD <60s envelope handling (A1/A2).** The perf gate asserts ONLY the
  ratified `<60s` BOUND; the supported-project-size envelope and p50/p95 are
  owner-TBD and NOT invented (Anti-Assumption). The Fast-Pass latency is also
  surfaced on `ai_spend_recorded.time_to_first_mri_ms`.
- **Calibration is scaffolded, not thresholded (F1).** `calibration.py` records
  the inputs needed to fit `p`/`ε`/the impact table later; it asserts no numeric
  pass/fail. The only tolerances tested are the doctrinal ones (exact for rule
  arithmetic; ±7 / same band for AI inputs). The v0 params live in `config.py`.
- **v0 arithmetic note (p=−0.5, not geometric).** The v0 spec §7 sentence
  "`(100,100,0)` → 37 Low" describes the OLD geometric `p=0` behaviour in the
  "p revised 0→−0.5" discussion; with the ratified default `p=−0.5` the floored
  `(100,100,5)` aggregates to ≈21.5 (still Low) — a harsher-than-geometric value
  by design ("weakness felt a touch more strongly than geometric", §7). The
  implementation matches `p=−0.5`, `ε=5` (Calibration §4h) EXACTLY; the
  pressure-test results that were computed at `p=−0.5` (`(85,85,20)`→46 Low;
  `(85,85,60)`→75 Med edge; single material→45 Low) all reproduce.
- **No migration / no new output_kind.** `issue`/`confidence`/`reliability`/`caf`/
  `outcome_confidence` are all already in the canonical CHECK + `OutputKind`
  Literal — verified in `retain/models.py`. Nothing new was added.
- **DTM-0009 gate-5 regression fixed forward.** BOTH gate-5 test files were
  updated for the new WB_EVAL tuple (positive verbatim + negative tamper/missing),
  so they are not left on the old union — gate-5 stays GREEN.

## Engineering-manager review notes

**Review (2026-06-17).** Single worker, both Part A (Evaluate) + Part B (live chain fusion),
no STOP. EM independently verified:

- **Scope:** confined to `evaluate/**` (new `engine.py`/`scoring.py`/`config.py`/
  `calibration.py`/`stage.py`), the new additive `orchestration/wave_b.py`, `events.py` +
  gate-5 (both test files updated — DTM-0009 regression not repeated), 5 new `shared/`
  types, and `evaluate` test suites. **Frozen modules confirmed untouched** (empty diff):
  `infer/**`, `graphs/deep_pass.py`, `state.py`, `runner.py`, `registry.py`, `retain/**`,
  `llm_provider/**`, all migrations, gate-4 + allowlist. No migration, no new package.
- **v0 fidelity (read + re-derived against the formula doc):** `p=−0.5`, `ε=5`, the impact
  table, bands 0–49/50–74/75–100, and the conservative ±3 edge-guard all match
  `CAF_CONFIDENCE_V0_SCORING_FORMULA_V1` §1/§2/§3/§4h exactly; `rule_version=wb-eval-caf-v0`
  pinned → rule-arithmetic exact-replay. Reliability is a separate qualifier (never multiplied
  in); Non-Collapse holds; CONF-06 flags High+Low-reliability; calibration harness records
  fit-inputs but asserts no numeric threshold (Anti-Assumption). The §7 pressure-test cases
  reproduce.
- **Confidence-never-health:** `extra='forbid'` on every Evaluate type + negative
  `test_b3_confidence_shape_forbids_a_health_or_probability_field`; plus Derived-never-Attested,
  recompute-appends-never-overwrites, stage-change-only-via-recompute, wrong-tier-routing — all
  negative-proven.
- **Part B fusion:** `wave_b.py` builds the composed `infer` stage by *calling*
  `run_synthesis_stage` then `run_finding_stage` over one run, plus the `evaluate` stage, and
  registers both via `register_stage` only — no topology/state edit. The live durable
  end-to-end (env-gated) admits→infer→evaluate→CHRs, asserts the `<60s` bound (envelope
  owner-TBD, not invented), and proves a recompute supersedes with the confidence delta
  reconstructable from CHR lineage. `register_stage` is process-global; the
  register/live tests save+restore the registry so the swap doesn't leak into other suites
  (EM confirmed full-suite green proves no leak).

**EM-run verification (independent, 2026-06-17, offline):**
- `ruff check .` → clean · `ci.gate_invariants` → PASS · `ci.gate_observability` → PASS ·
  `pytest tests/positive tests/negative tests/replay` → **444 passed, 68 skipped, 0 failed**
  (DTM-0010 baseline 374 → +70; the +1 skip is the env-gated live e2e). `evaluate` suites in
  isolation: 67 passed / 1 skipped.

**Finding to surface to the owner (doc, not code):** the owner-canon formula doc
`CAF_CONFIDENCE_V0_SCORING_FORMULA_V1` §7 prose shows `(100,100,0)→37` — that is the
pre-revision **geometric** (`p=0`) value; under the ratified **`p=−0.5`** it is ≈21.5 (still
Low, floor still > 0). The implementation correctly follows the ratified `p=−0.5`; the §7
illustrative number was simply not restated when finding #1 revised `p`. Recommend the owner
correct the §7 example. Not edited here (owner canon; deep-task does not edit source-of-truth).

## Approved by engineering manager

Status: Approved

Executive summary:
- DTM-0011 delivers IC/QA/OBS-WB-EVAL: Evaluate as the single producer of Issue / Confidence /
  Reliability / CAF / Outcome Confidence (all Derived), computed on the pinned v0 CAF/Confidence
  formula (p=−0.5, ε=5, conservative bands), reliability-qualified and never project-health;
  PS-03 seeding from the synthesized model; CONF-06 false-confidence; AE-04 understanding-state;
  one CHR per value with lineage; recompute-supersede as the "why did confidence change"
  backbone. It also wires the **live Wave-B chain** (composed infer synthesis→finding, then
  evaluate) via an additive `orchestration/wave_b.py` and proves a durable end-to-end with the
  Fast-Pass <60s bound — without touching any frozen module.

Verification:
- ruff clean · gate-4 PASS · gate-5 PASS · pytest 444 passed / 68 skipped / 0 failed offline
  (+70 vs DTM-0010). Scope-checked: frozen modules untouched; no migration/package; v0 params
  re-derived against the formula doc.

Manual test plan:
- With local Supabase up: run the live e2e — admit evidence → composed infer (model + findings)
  → evaluate → inspect CHR rows (issue/confidence/caf/outcome_confidence, all Derived) in
  Studio; mutate an assertion → recompute → confirm Outcome Confidence drift is reconstructable
  from CHR lineage and the prior CHRs are byte-intact; confirm a High-confidence-on-low-
  reliability case raises the false-confidence flag.

Remaining risks:
- v0 scoring magnitudes (impact table, p, ε) and the <60s envelope/p50/p95 remain owner-TBD
  calibration (scaffolded, asserted only as the doctrinal band/±7 and the <60s bound).
- Owner-canon formula doc §7 has a stale worked-example number (above) — doc-only.
