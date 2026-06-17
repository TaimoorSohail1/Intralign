# DTM-0011 — Evaluate: Issue, Confidence, Reliability, CAF, Outcome Confidence (v0), <60s gate

**Status:** Planned — BLOCKED on DTM-0010 approval · **Module:** DTM-0011 · **Phase:** III
(Wave B) · **Contract:** **IC/QA/OBS-WB-EVAL** (+ DL-046, DL-047, DL-048; v0 per ADR-0006) ·
**Depends:** DTM-0010 (Findings).

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
- **READ-ONLY:** `orchestration/**` (register_stage + StageContext only) · `infer/**` (consume
  Findings) · `retain/**`, `perceive/**`, `adapt/**`, DTM-0009/0010 modules · ALL migrations ·
  the v0 formula doc + scoring models (cite, do not edit) · Wave A/S/B-Infer event tuples.

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

_(worker fills)_

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_
