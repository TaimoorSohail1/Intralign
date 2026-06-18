# Deep-task plan — Wave B: Understanding (Synthesis · Infer · Evaluate)

New branch `feat/phase3-waveb-understanding`. One fresh worker per task, strictly
sequential, EM review → fix → verify → approve between tasks (same discipline as Wave A
DTM-0001…0008). Three slices, one contract each (ADR-0005). **Coding starts only after
per-wave owner authorization (DL-044 condition 2) + readiness gate.**

This is the first wave with AI in the codebase: each slice wires real `services/llm_provider`
(Pydantic AI adapter, OpenAI primary / Anthropic fallback, DL-054) behind
**recorded-model-response fixtures** for CI (ADR-0004). All output is **Derived**,
recomputable, appends a CHR via the 00R backbone, and is observable before "done".

## Slices

| # | Module | Slice (vertical outcome) | Contract | Depends on |
|---|---|---|---|---|
| 1 | DTM-0009 | **Synthesis (Infer ext.):** `llm_provider` real wiring + recorded-fixture harness; extract→synthesize `SynthesizedPlanningModel` + generate `PlanningArtifact`s (Intent/Context/Scope/Requirements/WBS/Resources/Schedule) as Derived; CHR-per-generation + recompute-supersede; user-editable; OBS-WS events + gate-5 vocab extension; `AI Spend Recorded` event + per-tier token budget enforcement (DL-048) | IC-WS-SYNTH | Wave A approved (00R + Retain) |
| 2 | DTM-0010 | **Finding (Infer):** generate Findings (gap/conflict/risk) from Attested content + synthesized model; one producer; conflicts **surfaced, not resolved**; each Finding Derived; `stage_infer` real impl registered in `deep_pass`; Fast/Deep `mode` + `confidence_stage`; OBS-WB-INFER events; cost governance | IC-WB-INFER | DTM-0009 |
| 3 | DTM-0011 | **Evaluate:** Findings→Issues; **v0 CAF/Confidence formula** (version-pinned, ADR-0006) → Confidence/Reliability/CAF/Outcome Confidence; banded + reliability-qualified; False-Confidence Detection (CONF-06); seed CAF/Confidence from synthesized model; `stage_evaluate` real impl; drift surfaced ≥10 pts / band change; **&lt;60s Time-to-First-MRI** perf gate; OBS-WB-EVAL events | IC-WB-EVAL | DTM-0010 |

## Test strategy

- QA-mapped test names per each contract's QA section (`test_b2_*` positive, `test_b3_*`
  negative) — same traceability discipline as Wave A.
- **Determinism tiers** (Calibration §1; ADR-0004/0006): rule/formula steps replay **exact**
  (v0 `rule_version` pinned); AI-numeric (Confidence/CAF/Reliability/Outcome Confidence)
  within **±7 pts & same band**; AI-text (Findings/Issues/artifacts) **semantic-equivalent**.
  All AI exercised via **recorded-model-response fixtures** offline; no provider call in PR CI.
- **Mandatory negatives:** Derived-written-as-Attested impossible (DB-proven where it
  touches canonical); **confidence-as-health/probability/score rejected**; conflicts not
  collapsed/resolved; no assessment change without recompute (only-recompute-changes-
  assessment); generated `PlanningArtifact` cannot be written as Attested-truth or changed
  without recompute; over-budget run degrades gracefully (Fast truncates / Deep coalesces),
  never overspends silently (DL-048).
- **OBS:** record-exact replay for emissions; two-axis replay (record-exact / derivation-by-
  determinism) validated per OBS contract; CHR lineage answers "why did confidence change?".
- Full suite + ruff + gates 1–6 green at each approval; Wave-A baseline (327) must not
  regress.

## Reserved-term guard

The LLM test-double is a **recorded model-response fixture**, never "replay"/"cassette"
(`replay` is reserved — event-log reconstruction that does not re-run the LLM; Determinism
Note §5, DT-3). Enforce in code + test names (CONTEXT.md Disambiguation Register).

## Manual checks (EM)

- Recorded-fixture CI is offline and deterministic; provider keys present only in dev +
  nightly baseline-update job (a model-version diff is a **new baseline, not a regression** —
  DT-6).
- End-to-end: submit artifact → Fast Pass returns Orientation Confidence + initial MRI/
  findings **&lt;60s**; Deep Pass expands async (user not blocked); two emissions show
  surfaced confidence/outcome **drift**; CHR lineage reconstructs the change.
- Studio: `SynthesizedPlanningModel` + artifacts visible as Derived projections with their
  CHRs; no Derived row written to a canonical table.

## Done = Wave B complete

All three contracts' B2/B3 sets demonstrably covered; AI determinism tiers hold on replay;
confidence is banded, reliability-qualified, never project-health; conflicts surfaced;
Fast/Deep both observable with progressive confidence stages; cost governance enforced;
events + two-axis replay present. Phase III candidate-complete for **owner exit-gate review
before Phase IV / Wave C** (DL-044). Owner sign-off required between waves.
