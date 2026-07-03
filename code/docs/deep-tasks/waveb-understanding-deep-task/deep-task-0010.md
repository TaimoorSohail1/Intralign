# DTM-0010 — Finding (Infer): gap/conflict/risk derivation, evidence-anchored, Fast/Deep

**Status:** **Approved** (EM, 2026-06-17) · **Module:** DTM-0010 · **Phase:** III (Wave B) ·
**Contract:** **IC/QA/OBS-WB-INFER** (+ DL-046) · **Depends:** DTM-0009 (landed `148400f`). ·
**Note:** live infer-node fusion (synthesis→finding) carried into DTM-0011.

## Goal / observable behavior

Infer derives **Findings** (types: **Gap, Conflict, Risk Signal**) from Attested knowledge
(Retain) + the synthesized model + the declared-outcome reference, **each anchored to the
Attested evidence it derives from**. Each emission emits `finding_detected` and **appends a
CHR** (via `ctx.chr_repo`); recompute re-derives and **supersedes** prior Findings (history
appended, prior CHR intact). Conflicts are **surfaced, not resolved**. Runs under both modes:
**Fast Pass** orientation-sufficient Findings; **Deep Pass** expanded/matured; `mode` +
`confidence_stage` (Orientation→Expanded→Validated) on each emission + CHR.

## Source docs / constraints

- `WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING.md` §1 (IC-WB-INFER 1.1 required/forbidden/states/
  invariants; QA 1.2 positive/negative/classification; OBS 1.3 events/audit/replay/drift) +
  §0/§0.1 shared invariants & modes.
- `WAVE_B_CONTRACT_AMENDMENT_FAST_DEEP_60S_DISPOSITION.md` B (Infer required-behavior #5), D
  (positives/negatives), E (OBS mode/stage + Time-to-First-MRI latency).
- ADR-0004 (fixtures), decisions #2–#6, #9–#11. Calibration §1 tiers, §4c routing/budget.

## Locked decisions

- **Producer boundary:** Infer is the **single producer of Findings**. It **must not**
  compute severity/confidence (Evaluate), generate recommendations/clarifications (Advise),
  write canonical / promote a Finding to Attested, govern exposure, or resolve a conflict into
  canonical truth. Reuses the DTM-0009 `llm_provider` + recorded-fixture harness.
- **Replace the `infer` placeholder** via `register_stage("infer", …)` — `deep_pass.py`
  topology unchanged. Findings append their CHRs through `ctx.chr_repo` (decisions #4); emit
  via `ctx.emitter`.
- **Evidence anchor mandatory:** every Finding traces to the `AttestedAssertion`(s) it derives
  from (Major failure if missing).
- **Persistence default:** generic `derived` projection + CHR (`output_kind=finding`). No new
  migration (typed-table need ⇒ STOP/escalate).
- **Modes:** Fast Pass produces orientation Findings without blocking; Deep Pass (the 00R
  async engine) expands; `confidence_stage` changes **only via recompute**; `mode`/stage are
  attributes, never new objects.
- Determinism: rule-structural gaps **exact**; AI-derived Findings **semantic**; set-level
  ≥90% stable identities across recompute.

## Owned files / boundaries

- **OWN (additive):** `backend/responsibilities/infer/**` (Finding engines: gap [alignment/
  coverage/quality/SMART], conflict, risk — additive to DTM-0009's synthesis modules) ·
  `events.py` (ADD `EVENT_NAMES_WB_INFER`, extend union) · `ci/gate_observability.py`
  (additive) · `shared/` (ADD `Finding` type if not already) · `tests/{positive,negative}/
  infer_finding/**`, `tests/replay/**`, additive recorded fixtures.
- **READ-ONLY:** `orchestration/**` (register_stage + StageContext only) · `retain/**`,
  `perceive/**`, `adapt/**`, DTM-0009 synthesis modules (consume the model; do not edit) ·
  ALL migrations · Wave A/S event tuples (extend only).

## Packages / refactors

- None new. No refactors (placeholder replaced via registry).

## Implementation instructions (TDD)

1. Red: `test_b2_*` (Findings typed + anchored + CHR + supersession + both modes + stage
   transitions) and `test_b3_*` (every forbidden behavior) first.
2. Gap/Conflict/Risk engines reading Attested knowledge + synthesized model; anchor each
   Finding; classify type; flag conflicts (surfaced).
3. Inject as the `infer` stage; CHR per Finding via `ctx.chr_repo`; emit `finding_detected`/
   `finding_superseded`; events + gate-5 vocab.
4. Fast/Deep: orientation-sufficient set on Fast; Deep expansion via 00R recompute; carry
   `mode`+`confidence_stage`; emit Fast-Pass Time-to-First-MRI latency.
5. OBS audit (assertions a Finding derived from, model/rule version, recompute lineage) +
   replay (record-exact emission; semantic derivation, exact for rule-structural gaps).
6. Integration: recompute (00R) re-derives + supersedes; prior Finding CHR intact; two
   emissions show surfaced drift; Deep Pass does not block the user.

## API / data / schema contracts

- `Finding`: Derived, `epistemic_state=derived`, `finding_type ∈ {gap, conflict, risk}`,
  `evidence_anchors=[assertion ids]`, `mode`, `confidence_stage`. CHR per emission
  (`output_kind=finding`). No schema change.

## Test plan (QA-WB-INFER)

- **Positive (`test_b2_*`):** Findings derived + Gap/Conflict/Risk typed + evidence-anchored;
  emission appends CHR; recompute supersedes (prior intact); both modes; stage
  Orientation→Expanded→Validated observable.
- **Negative (`test_b3_*`):** Infer computing severity/confidence; generating recs/
  clarifications; writing canonical / promoting to Attested *(Critical)*; resolving a conflict
  into canonical truth; Finding changed **without recompute** / CHR overwritten *(Critical)*;
  Deep Pass blocking the user; `confidence_stage` regressing or changing without recompute;
  `mode`/stage modeled as a new object *(Critical)*; missing evidence anchor *(Major)*.
- **Determinism:** rule-structural exact; AI semantic; ≥90% set overlap.
- AI offline via recorded fixtures (no provider call in PR CI).
- Full suite + ruff + gate-4 + gate-5 green; baseline must not regress.

## Manual checks (EM)

- AST/grep: `infer/` exports no severity/confidence/recommendation producer; only Finding.
- Studio: Finding rows are Derived + anchored; recompute leaves prior Finding CHR byte-intact.

## Done criteria

- WB-INFER B2/B3 traceability in report; conflicts surfaced-not-resolved proven; Fast/Deep +
  stage maturation demonstrated; PR cites `IC-WB-INFER`; no migration/package. Ready for
  DTM-0011.

## Worker report

**Ready for review.**

### What was built (additive only; DTM-0009 infra reused unchanged)

| File | Status | What |
|---|---|---|
| `shared/epistemic.py` | edit (additive) | New `Finding` CognitionEntity (pinned `derived`, `extra='forbid'`), `FindingType ∈ {gap,conflict,risk}`, `GapKind`, mandatory non-empty `evidence_anchors`, stable `finding_id`, `mode`/`confidence_stage`/`understanding_state` attributes, `model_or_rule_version` stamp. `Finding` already in `CANONICAL_OUTPUTS` (no change). |
| `backend/responsibilities/infer/finding.py` | new | `FindingEngine` + `FindingResult`. Rule-structural engines (EXACT): coverage gaps (missing constraint/dependency evidence), SMART gaps (non-measurable declared outcome), conflict detection (negation-pair, surfaced-not-resolved, anchored to BOTH). AI engines (SEMANTIC, budget-gated): alignment/quality gaps + risk signals from the synthesized model. Stable `finding_id` hash. Cost governance: AI passes defer (degraded) over budget; rule-structural always produced. |
| `backend/responsibilities/infer/finding_stage.py` | new | `build_finding_stage` (for `register_stage("infer", …)`) + `run_finding_stage`. One CHR per Finding via `ctx.chr_repo` (`output_kind="finding"` — already in CHECK+Literal, **no migration**); paired `cognition_history_record_appended` emit; `finding_detected`/`finding_superseded` (recompute, keyed by stable `finding_id`, carries `supersedes_chr_id` lineage); `mode`+`confidence_stage` on every emission+CHR; Fast-Pass `time_to_first_mri_ms` on the `ai_spend_recorded` payload. Does NOT touch synthesis `stage.py`/topology. |
| `backend/services/observability/events.py` | edit (additive) | `EVENT_NAMES_WB_INFER = ("finding_detected","finding_superseded")` (verbatim OBS-WB-INFER A6/C2); union extended `… + WB_INFER + COST`. |
| `ci/gate_observability.py` | edit (additive) | `EXPECTED_EVENT_NAMES_WB_INFER`; added to `_CONTRACT_VOCABULARIES` + `_UNION_NAME_ORDER` + the union. |
| `tests/positive/observability/test_gate_observability.py` | edit | Asserts the 6-way union + verbatim WB-INFER tuple (NOT left on the old union — DTM-0009 regression not repeated). |
| `tests/negative/observability/test_gate_observability_negative.py` | edit | `GOOD_EVENTS_PY` + union grown; new WB-INFER rename/missing tamper tests; missing-all count 6→7; union-drop test updated. |
| `tests/_fixtures/recorded_model_responses/wb_infer_v0.json` | new | Stamped (`model_version`/`config`) alignment/risk/unanchored/empty recorded responses. |
| `tests/positive/infer_finding/**` | new | `helpers.py` + `test_b2_derivation.py`, `test_b2_stage.py`, `test_b2_determinism.py`, `test_b2_cost_modes.py`. |
| `tests/negative/infer_finding/**` | new | `test_b3_finding_boundary.py`, `test_b3_producer_boundary.py`, `test_b3_recompute_and_modes.py`. |
| `tests/replay/test_recorded_finding_fixture.py` | new | Recorded-fixture harness self-test for WB-INFER (zero live calls; record-exact axis). |

### B2 / B3 → test traceability

| Contract requirement | Test |
|---|---|
| B2 Findings derived + each anchored | `test_b2_derivation::test_b2_findings_are_derived_and_each_anchored` |
| B2 Gap/Conflict/Risk typed correctly | `…::test_b2_all_three_finding_types_are_produced_and_typed` |
| B2 rule-structural coverage gap (EXACT) | `…::test_b2_rule_structural_coverage_gap_is_derived_exact` |
| B2 SMART gap / no-gap | `…::test_b2_rule_structural_smart_gap_for_non_measurable_outcome`, `…::test_b2_smart_outcome_produces_no_smart_gap` |
| B2 conflict anchored to both | `…::test_b2_conflict_is_surfaced_anchored_to_both_assertions` |
| B2 risk anchored from model | `…::test_b2_risk_signals_come_from_the_model_anchored` |
| B2 emission appends one CHR (+ pairing) | `test_b2_stage::test_b2_one_chr_appended_per_finding_paired_with_append_event` |
| B2 finding_detected per Finding + mode/stage | `…::test_b2_finding_detected_emitted_per_finding_first_pass` |
| B2 Fast-Pass Time-to-First-MRI latency | `…::test_b2_fast_pass_emits_time_to_first_mri_latency` |
| B2 recompute supersedes, prior CHR intact | `…::test_b2_recompute_appends_a_new_generation_keeping_prior_chr_intact`, `…::test_b2_recompute_emits_superseded_with_supersedes_lineage` |
| B2 both modes (Deep carries deep/expanded) | `…::test_b2_deep_pass_carries_deep_mode_on_emissions_and_chr` |
| B2 stage Orientation→Expanded→Validated | `…::test_b2_confidence_stage_matures_orientation_to_validated_via_recompute` |
| B2 determinism (rule EXACT / set ≥90%) | `test_b2_determinism::*` |
| B2 Fast orientation-sufficient + cost gov | `test_b2_cost_modes::*` |
| B3 Critical — Derived→Attested rejected | `test_b3_finding_boundary::test_b3_finding_cannot_be_attested_as_truth` |
| B3 Infer computing severity/confidence (producer boundary) | `test_b3_finding_boundary::test_b3_finding_cannot_carry_severity_confidence_score_or_recommendation`, `test_b3_producer_boundary::*` |
| B3 Major — missing evidence anchor | `test_b3_finding_boundary::test_b3_finding_missing_evidence_anchor_is_rejected_major` |
| B3 generating recs/clarifications | `test_b3_producer_boundary::test_b3_finding_module_exports_no_evaluate_or_advise_producer`, `…names_no_severity_or_confidence_compute` |
| B3 Critical — writing canonical / promote to Attested | `test_b3_producer_boundary::test_b3_finding_modules_write_no_canonical_attested_table` |
| B3 conflict resolved into canonical truth | `test_b3_producer_boundary::test_b3_conflict_is_surfaced_not_resolved` |
| B3 Critical — Finding changed without recompute / CHR overwrite | `test_b3_recompute_and_modes::test_b3_chr_repo_has_no_overwrite_surface`, `…recompute_appends_never_reduces_history`, `…appended_finding_chr_cannot_be_overwritten_via_returned_row`, `…confidence_stage_cannot_change_on_a_frozen_finding` |
| B3 Deep Pass blocking the user | `test_b3_recompute_and_modes::test_b3_deep_pass_does_not_block_orientation_findings` |
| B3 confidence_stage regress / change without recompute | `test_b3_finding_boundary::test_b3_finding_cannot_be_changed_in_place`, `test_b3_recompute_and_modes::test_b3_confidence_stage_cannot_change_on_a_frozen_finding` |
| B3 Critical — mode/stage as a new object | `test_b3_recompute_and_modes::test_b3_mode_and_stage_are_attributes_not_objects` |
| B3 unknown finding event rejected | `test_b3_recompute_and_modes::test_b3_unknown_finding_event_is_rejected_by_the_emitter` |
| Gate-5 vocab verbatim + tamper | `tests/{positive,negative}/observability/test_gate_observability*.py` (WB-INFER tuple) |

### Exact commands + results (offline)

```
$ python -m pytest tests/positive tests/negative tests/replay -q
374 passed, 67 skipped, 1 warning in 2.03s
   (baseline 326 passed / 67 skipped at HEAD 148400f → +48 passed, skips unchanged;
    gate-5 tests stayed GREEN with the WB-INFER vocab addition)

$ ruff check .
All checks passed!

$ python -m ci.gate_invariants
[gate-4 epistemic-invariant] PASS: no forbidden tokens, no authority module, no canonical-table mutations in migrations.

$ python -m ci.gate_observability
[gate-5 observability] PASS: every CHR-append call-site emits 'cognition_history_record_appended',
the per-contract A6 vocabularies are pinned verbatim (union consistent), and the replay harness is present.
```

(`python` = the repo `.venv`. The OTLP "Failed to export traces to 127.0.0.1" line in pytest output is the pre-existing no-collector side effect, not a test failure.)

### Flags / notes for the EM

- **No migration, no new package, no schema change.** `output_kind="finding"` was already in the CHR CHECK + `retain/models.py` `OutputKind` Literal (and `risk` too) — confirmed; nothing widened.
- **READ-ONLY honored:** `orchestration/**`, `retain/**`, `perceive/**`, `adapt/**`, the DTM-0009 `synthesis.py`/`stage.py`/`llm_provider/**`/fixture-harness, `ci/gate_invariants.py`, `ci/invariant_allowlist.txt` — none modified. The Finding stage is a NEW file (`finding_stage.py`), additive to synthesis `stage.py`.
- **Orchestration wiring deferred by design:** `build_finding_stage` is ready for `register_stage("infer", …)` but is NOT wired into a live graph in this slice (the synthesis `stage.py` already occupies the `infer` slot in DTM-0009). The contract scope is the Finding producer + its CHR/event/recompute behavior, all proven at the stage-fn level with a fake `StageContext`; an integration that composes synthesis + finding under one `infer` node is an orchestration concern (READ-ONLY here). **Confirm whether the EM wants both producers fused under the single `infer` node now or in DTM-0011** — flagged rather than guessed (it would require editing the DTM-0009 stage, which is approved/frozen).
- **`pydantic-ai` DeprecationWarning** ("no current event loop") is the same pre-existing warning DTM-0009 emits via `run_sync`; not introduced here.
- **Declared-outcome reference:** modeled as `(declared_outcome: str, outcome_anchor: str)` inputs to the engine (the R1 Intend-provisional Canonical Fact). The stage's `extract_inputs` maps them from GraphState; no new object invented.

## Engineering-manager review notes

**Review (2026-06-17).** Single worker, clean completion, no STOP. EM independently verified:

- **Scope:** changes confined to the DTM-0010 owned set — `shared/epistemic.py` (`Finding`),
  new `infer/finding.py` + `infer/finding_stage.py`, `events.py` + gate-5 (vocab + both test
  files updated — the DTM-0009 regression was **not** repeated), fixtures + `infer_finding`
  suites. DTM-0009 modules (`synthesis.py`, `stage.py`, `llm_provider/**`, `retain/models.py`,
  the migration, `gate_invariants.py`, `invariant_allowlist.txt`) **untouched**. No migration,
  no new package.
- **Producer boundary (read + test-proven):** Finding modules compute NO severity/confidence/
  CAF, generate NO recommendations, write NO canonical/Attested, and do NOT resolve conflicts.
  `confidence_stage` present is the legitimate DL-046 maturation attribute, not Evaluate's
  `Confidence`. Negatives confirm: `test_b3_conflict_is_surfaced_not_resolved`,
  `…cannot_carry_severity_confidence_score_or_recommendation`,
  `…missing_evidence_anchor_is_rejected_major`, `…finding_cannot_be_attested_as_truth`,
  `…chr_repo_has_no_overwrite_surface`.
- **Contract fidelity:** Gap/Conflict/Risk typed + evidence-anchored; one CHR per Finding via
  the Retain-owned repo (`output_kind=finding`, already in CHECK — no schema change); recompute
  supersedes by stable `finding_id` (prior CHR intact); Fast/Deep modes + stage; Fast-Pass
  `time_to_first_mri_ms` emitted; AI via recorded fixtures (offline, no provider call).

**EM-run verification (independent, 2026-06-17, offline):**
- `ruff check .` → All checks passed · `ci.gate_invariants` → PASS · `ci.gate_observability`
  → PASS · `pytest tests/positive tests/negative tests/replay` → **374 passed, 67 skipped,
  0 failed** (DTM-0009 baseline 326 → +48). (A 1-test failure appears only under a manual
  `OTEL_SDK_DISABLED` flag — `test_attaches_otel_span_event_when_tracer_active`, an existing
  observability test that asserts the SDK is active; an EM-run artifact, not a DTM-0010
  effect.)

**Carried integration item (decided, not a defect):** `build_finding_stage` is built + proven
at the stage-fn level but not yet wired into the live graph, because the single `infer` chain
node is occupied by DTM-0009's synthesis stage and fusing them would mean editing the frozen
DTM-0009 `stage.py`. **EM ruling:** defer the live fusion to DTM-0011 — compose the `infer`
node as synthesis→finding at the orchestration-wiring layer (a thin composed stage; no edit to
the frozen DTM-0009/0010 stage files), since Evaluate's own DoD (live end-to-end Fast Pass
<60s; recompute-drift) requires the full chain wired anyway. Recorded in DTM-0011 + decisions.

## Approved by engineering manager

Status: Approved

Executive summary:
- DTM-0010 delivers IC/QA/OBS-WB-INFER: Infer as the single producer of Findings (Gap /
  Conflict / Risk), each Derived and anchored to its Attested evidence, appending one CHR per
  emission via the Retain-owned repository, superseding on recompute, under Fast/Deep modes —
  conflicts surfaced-not-resolved, no severity/confidence/recommendation, no canonical write.
  Reuses the DTM-0009 llm_provider + recorded-fixture harness; CI stays offline-deterministic.

Verification:
- ruff clean · gate-4 PASS · gate-5 PASS · pytest 374 passed / 67 skipped / 0 failed offline
  (+48 vs DTM-0009). Scope-checked: DTM-0009 modules untouched; no migration/package.

Manual test plan:
- With local Supabase up + the composed infer node (DTM-0011): submit evidence → confirm
  `finding` CHR rows (Derived, evidence-anchored) in Studio; mutate an assertion → recompute →
  prior Finding CHR byte-intact, new one supersedes; confirm a conflict surfaces as a Finding
  rather than being resolved.

Remaining risks:
- Live infer-node fusion (synthesis→finding) is carried into DTM-0011 (above) — Finding
  behavior itself is fully proven at the stage-fn level here.
