# DTM-0014 — Advise core: Recommendation + Clarification, anchored, Derived, live A→B→C

**Status:** **Approved** (EM, 2026-06-18) · **Module:** DTM-0014 ·
**Phase:** IV (Wave C) · **Contract:** **IC/QA/OBS-WC-ADVISE** (C0–C3) · **Depends:** Wave B
(Findings/Issues) + DTM-0013 CHR-model fix (present in this branch). · **Note:** Wave B PR #39
exit-gate sign-off still pending on main; owner directed Wave C start regardless.

## Goal / observable behavior

Advise generates **Recommendations** (types: suggested-action, candidate-improvement) and
**Clarification Requests**, each **anchored to a Finding/Issue** (never standalone), all
**Derived**. Each emission emits `recommendation_generated` / `clarification_requested` and
**appends a CHR** (via `ctx.chr_repo`, output_kind `recommendation`/`clarification`); recompute
re-derives and **supersedes** (prior CHR intact). Multiple alternatives coexist as multiple
Recommendations (no Resolution-Path object). The advise stage is wired live so the full **A→B→C
chain** runs end-to-end. Advise **proposes, never disposes** — no evaluate/score, no canonical
write, no govern/authorize/execute, no self-accept.

## Source docs / constraints

- `WAVE_C_AND_U_CONTRACT_PACKAGES_ADVISORY_AND_ACCEPTANCE.md` **Wave C** C0–C3 (IC required/
  forbidden/invariants; QA positive/negative/classification; OBS events/audit/replay/drift).
- Phase IV plan (DoD, invariants, exit gate); ADR-0008; `deep-task-decisions.md` #1–#12; DL-055
  (Recommendation state — **Generated only here**); DL-043/046; ADR-0004; ANTI_ASSUMPTION.

## Locked decisions (from decisions file — do not re-derive)

- **Producer boundary:** Advise is the **single producer** of Recommendation + Clarification. It
  **must not** evaluate severity/confidence (Evaluate), write canonical / promote to Attested,
  govern/authorize/execute, accept its own output, or change assessment outside recompute.
- **Anchoring mandatory:** every Recommendation traces to its Finding/Issue (Major if missing).
- **Wire via `register_stage("advise", …)`** + an **additive `orchestration/wave_c.py`** that
  composes A→B→C by calling the Wave B chain builder and adding the advise stage (mirror the
  `_RunHandoff` closure to pass Findings/Issues). **Do NOT** edit `wave_b.py`, `deep_pass.py`,
  `state.py`, `runner.py`, `registry.py`.
- **CHR-append (DTM-0013 model pattern):** `CognitionHistoryRecord(project_id=…,
  provenance_ref={"emitted_by":"advise"}, recompute_trigger=…, supersedes_chr_id=…, **spec)` →
  `ctx.chr_repo.append(record)` → emit `cognition_history_record_appended`. `output_kind ∈
  {recommendation, clarification}` (already in CHECK) → **NO migration**.
- **DL-055:** emit Recommendations in the **`Generated`** state only. **Do NOT** implement
  Accept/Defer/Reject/Apply (Wave U). Multiple alternatives = multiple Recommendations.
- **Resolution Paths** are presentation-only — a standalone Resolution-Path **object** is a
  rejected negative (Major).
- **LLM:** add `"advise"` to `RoutingStage` + an `advise` `ModelRef` in `TierRouting` (internal
  Gemma primary, DL-069); drive via recorded fixtures (zero PR-CI provider calls); emit
  `ai_spend_recorded`. Carry `mode` + `confidence_stage`. Determinism: AI-text **semantic**.

## Owned files / boundaries

- **OWN (additive):** `backend/responsibilities/advise/**` (Recommendation engine + Clarification
  engine + advise stage) · NEW `backend/orchestration/wave_c.py` · `shared/epistemic.py` (ADD
  `Recommendation`, `ClarificationRequest` classes) · `backend/services/llm_provider/config.py`
  (ADD `advise` routing stage) · `events.py` (ADD `EVENT_NAMES_WC_ADVISE`, extend union) ·
  `ci/gate_observability.py` (additive vocab + tamper) + **both** gate-5 test files ·
  `tests/{positive,negative}/advise/**`, `tests/replay/**`, additive recorded fixtures + an
  env-gated live A→B→C e2e under `tests/positive/`.
- **READ-ONLY:** `wave_b.py`, `graphs/deep_pass.py`, `state.py`, `runner.py`, `registry.py`,
  `stages.py` (use `register_stage` only) · `infer/**`, `evaluate/**`, `retain/**`, `perceive/**`
  · ALL migrations · `gate_invariants.py`/allowlist · the recorded-fixture harness content.

## Packages / refactors

- None new. No refactor of frozen modules (advise injected via registry; `wave_c.py` additive).

## Implementation instructions (TDD)

1. Red: `test_c2_*` (Recommendation anchored; Clarification on ambiguity; CHR appended;
   recompute supersedes; multiple alternatives; both modes/stage) and the negatives
   (`standalone/unanchored`, `resolution_path_object`, `advise_scoring`, `advise_govern_execute`,
   `advise_self_accept`, `change_without_recompute`, `history_overwrite`).
2. Recommendation engine (Finding/Issue-anchored, LLM via fixtures) + Clarification engine.
3. `Recommendation`/`ClarificationRequest` types (Derived, anchor field, `type`).
4. advise stage: CHR per emission (model pattern); emit `recommendation_generated`/
   `clarification_requested` + `cognition_history_record_appended`; `ai_spend_recorded`.
5. `wave_c.py`: compose A→B→C; `register_stage("advise", …)`; live e2e (env-gated).
6. events + gate-5 vocab + both test files; OBS audit (anchor lineage, model version) + replay
   (record-exact emission; semantic derivation).

## API / data / schema contracts

- `Recommendation`: Derived, `epistemic_state=derived`, `recommendation_type ∈ {suggested_action,
  candidate_improvement}`, `anchor` (Finding/Issue id), `mode`, `confidence_stage`. CHR
  `output_kind=recommendation`. `ClarificationRequest`: Derived, `anchor`, `question`,
  `output_kind=clarification`. **No schema change.**

## Test plan (QA-WC-ADVISE C2)

- **Positive (`test_c2_*`):** Recommendation generated + anchored; Clarification raised; CHR
  appended; recompute supersedes (prior intact); multiple alternatives coexist; modes/stage.
- **Negative:** standalone Recommendation *(Major)*; Resolution-Path-as-object *(Major)*; Advise
  evaluating/scoring; Advise govern/authorize/execute *(Critical)*; Advise self-accepting
  *(Critical)*; change without recompute / history overwrite *(Critical)*; missing anchor *(Major)*.
- **Determinism:** AI semantic; record-exact emission; ≥90% set overlap.
- AI offline via recorded fixtures; full suite + ruff + gate-4 + gate-5 green; baseline (offline
  455 / live 523) no regression; live A→B→C e2e passes.

## Manual checks (EM)

- Live: admit → infer → evaluate → advise → `recommendation`/`clarification` CHR rows, anchored;
  recompute supersedes, prior byte-intact.
- AST/grep: `advise/` exports no evaluate/accept/execute producer; Recommendation carries anchor.

## Done criteria

- WC-ADVISE C2 traceability in report; advise-proposes-never-disposes proven by negatives;
  Resolution-Path-presentation-only proven; A→B→C live; PR cites `IC-WC-ADVISE`; no migration/
  package. Ready for DTM-0015.

## Worker report

**Ready for review.**

DTM-0014 (IC/QA/OBS-WC-ADVISE core) is implemented: Advise is the single producer
of **Recommendation** + **ClarificationRequest**, both Derived, each **anchored to
a Finding/Issue** (never standalone), emitted in the **`generated`** state only
(DL-055 — no self-accept), AI-text via the LLM seam (`advise` routing stage,
internal gemma primary, DL-069) driven by recorded fixtures (zero PR-CI provider
calls). The advise stage appends one CHR per emission via `ctx.chr_repo` using the
DTM-0013 **model** pattern (`output_kind ∈ {recommendation, clarification}` —
already in the CHECK, **no migration**), emits `recommendation_generated` /
`clarification_requested` + `cognition_history_record_appended` + `ai_spend_recorded`,
carries `mode` + `confidence_stage`, and on recompute re-derives + supersedes
(prior CHR byte-intact). `wave_c.py` composes the full **A→B→C** chain by CALLING
the frozen Wave B builder and adding `advise` via `register_stage` — no frozen
file edited, no topology/state change.

### Files built / changed

| File | New? | What |
|---|---|---|
| `shared/epistemic.py` | edit | ADD `Recommendation` (Derived, `extra='forbid'`, `anchor` min_length=1, `recommendation_type ∈ {suggested_action, candidate_improvement}`, `state` pinned `generated`, mode/confidence_stage) + `ClarificationRequest` (Derived, `anchor`, `question`). `RecommendationType`/`RecommendationState` Literals. |
| `backend/responsibilities/advise/engine.py` | NEW | `AdviseEngine` — anchored Recommendation + Clarification derivation (AI-text via `stage="advise"`; anchor/type/id EXACT; unanchored model items DROPPED; stable structural ids; budget-gated, DL-048). |
| `backend/responsibilities/advise/stage.py` | NEW | `run_advise_stage` / `build_advise_stage` — one CHR per emission (DTM-0013 model pattern, `provenance_ref={"emitted_by":"advise"}`), events + append pairing, recompute supersedes, model-identity stamp. |
| `backend/responsibilities/advise/__init__.py` | edit | export the advise public surface. |
| `backend/orchestration/wave_c.py` | NEW | `WaveCChain` / `build_and_register_wave_c_chain` — composes A→B→C by calling the Wave B builder, wraps `infer` to capture Findings into a per-run advise handoff, forms Issues (reusing `EvaluateEngine.form_issue`, read-only), registers `advise`. |
| `backend/services/llm_provider/config.py` | edit | ADD `"advise"` to `RoutingStage` + an `advise` `ModelRef` to `TierRouting` (internal primary in `_internal_routing`, OpenAI in the disabled fallback). |
| `backend/services/observability/events.py` | edit | ADD `EVENT_NAMES_WC_ADVISE = (recommendation_generated, clarification_requested)`; extend the union (8-way) + the emitter error text. |
| `ci/gate_observability.py` | edit | ADD `EXPECTED_EVENT_NAMES_WC_ADVISE`; register in `_CONTRACT_VOCABULARIES` + `_UNION_NAME_ORDER` + union + docstring. |
| `tests/positive/observability/test_gate_observability.py` | edit | WC_ADVISE verbatim vocab test + live-seam equality + 8-way union. |
| `tests/negative/observability/test_gate_observability_negative.py` | edit | WC_ADVISE in `GOOD_EVENTS_PY` + rename/missing-tuple tampers + 8-way union/missing-all count (9). |
| `tests/_fixtures/recorded_model_responses/wc_advise_v0.json` | NEW | advise fixture (model_version/config stamped): `recommendation`, `clarification`, `recommendation_unanchored`, `*_empty`. |
| `tests/_fixtures/recorded_model_responses/wc_advise_e2e_v0.json` | NEW | advise fixture anchored to the deterministic Finding ids the FindingEngine derives from `sample_drafts()` under the fixed e2e project (composition + live e2e). |
| `tests/positive/advise/**` | NEW | `helpers.py`, `test_c2_derivation.py`, `test_c2_stage.py`, `test_c2_determinism.py`, `test_c2_wave_c_composition.py`, env-gated `test_c2_live_chain_e2e.py`. |
| `tests/negative/advise/**` | NEW | `test_c3_producer_boundary.py`, `test_c3_anchoring_and_resolution_path.py`, `test_c3_recompute_and_history.py`. |
| `tests/replay/test_recorded_advise_fixture.py` | NEW | harness self-test: advise runs entirely on recorded responses (zero live calls); two-axis (text semantic, emission record-exact). |

### C2 → test traceability

| Contract item (C2/C3) | Test(s) |
|---|---|
| **Positive** — Recommendation generated + ANCHORED to its Finding/Issue | `positive/advise/test_c2_derivation.py::test_c2_recommendation_generated_and_anchored_to_its_finding`, `::test_c2_recommendation_can_anchor_to_an_issue_id` |
| Clarification raised on blocking ambiguity | `…::test_c2_clarification_raised_on_blocking_ambiguity`, `::test_c2_no_clarification_without_blocking_ambiguity` |
| Emission appends a CHR (paired event) | `positive/advise/test_c2_stage.py::test_c2_one_chr_per_emission_paired_with_append_event`, `::test_c2_emission_events_emitted_with_mode_and_stage` |
| Recompute supersedes; prior intact | `…test_c2_stage.py::test_c2_recompute_appends_new_emission_keeping_prior_chr_intact`, `negative/advise/test_c3_recompute_and_history.py::test_c3_history_overwrite_is_impossible_recompute_appends` |
| Multiple alternatives coexist (no Resolution-Path object) | `…test_c2_derivation.py::test_c2_multiple_alternatives_coexist_as_multiple_recommendations`, `negative/advise/test_c3_anchoring_and_resolution_path.py::test_c3_multiple_alternatives_are_separate_recommendations_not_one_object` |
| Both modes + confidence_stage | `…test_c2_derivation.py::test_c2_both_modes_and_confidence_stage_carried`, `…test_c2_stage.py::test_c2_deep_pass_carries_deep_mode_on_emissions_and_chr` |
| Anchor lineage + model version on every CHR | `…test_c2_stage.py::test_c2_every_chr_carries_input_version_model_version_and_anchor_lineage` |
| Determinism (AI text semantic; emission record-exact; ≥90% set overlap) | `…test_c2_determinism.py::*`, `…test_c2_stage.py::test_c2_recompute_set_overlap_is_at_least_90_percent_stable`, `replay/test_recorded_advise_fixture.py::*` |
| `wave_c.py` composes A→B→C; registers advise | `positive/advise/test_c2_wave_c_composition.py::test_c2_build_and_register_wave_c_replaces_the_advise_placeholder`, `::test_c2_full_chain_advise_anchors_to_run_findings` |
| **Negative** — standalone/unanchored Recommendation rejected *(Major)* | `negative/advise/test_c3_anchoring_and_resolution_path.py::test_c3_standalone_recommendation_is_structurally_impossible`, `::test_c3_empty_anchor_recommendation_is_rejected`, `::test_c3_model_returned_unanchored_recommendation_is_dropped` |
| Resolution-Path-as-object rejected *(Major)* | `…test_c3_anchoring_and_resolution_path.py::test_c3_advise_builds_no_standalone_resolution_path_object` |
| Advise evaluating/scoring rejected | `negative/advise/test_c3_producer_boundary.py::test_c3_advise_modules_never_score_govern_execute_or_self_accept`, `::test_c3_recommendation_carries_no_severity_score_or_accept_field` |
| Advise govern/authorize/execute rejected *(Critical)* | `…test_c3_producer_boundary.py::test_c3_advise_exports_no_evaluate_accept_or_execute_producer`, `::test_c3_advise_engine_exposes_no_acceptance_or_execution_method`, `::test_c3_advise_modules_never_score_govern_execute_or_self_accept` |
| Advise self-accepting rejected *(Critical)* | `…test_c3_producer_boundary.py::test_c3_advise_self_accept_is_structurally_impossible` |
| Change without recompute rejected *(Critical)* | `…test_c3_recompute_and_history.py::test_c3_recommendation_is_frozen_no_change_outside_recompute` |
| History overwrite impossible *(Critical)* | `…test_c3_recompute_and_history.py::test_c3_history_overwrite_is_impossible_recompute_appends`, `::test_c3_append_only_fake_repo_has_no_mutation_surface`, `::test_c3_advise_stage_passes_a_model_not_a_dict_dtm0013` |
| Derived never Attested | `…test_c3_producer_boundary.py::test_c3_recommendation_outputs_are_all_derived_never_attested`, `::test_c3_recommendation_cannot_be_constructed_as_attested` |

### Exact commands + results

```
# OFFLINE (OSLO_LLM_LIVE unset, no Supabase env)
.venv/bin/python -m pytest tests/positive tests/negative tests/replay -q
→ 498 passed, 69 skipped   (baseline 455/68 → +43 new offline tests; +1 skip = the
                            env-gated live A→B→C e2e, which skips offline. No regression.)

# LIVE (local Supabase up; OSLO_LLM_LIVE unset → recorded fixtures drive the LLM)
set -a; source .env; set +a; unset OSLO_LLM_LIVE; \
  .venv/bin/python -m pytest tests/positive tests/negative tests/replay -q
→ 567 passed, 0 skipped     (baseline live 523 → +44; the live A→B→C e2e RAN and PASSED;
                            re-run twice to confirm idempotency under accumulated rows.)

.venv/bin/ruff check .                  → All checks passed!
.venv/bin/python -m ci.gate_invariants  → [gate-4 epistemic-invariant] PASS
.venv/bin/python -m ci.gate_observability → [gate-5 observability] PASS
```

### Flags / notes

- **Live A→B→C e2e RAN and PASSED** (local Supabase was up at `http://127.0.0.1:54331`).
  Two implementation notes for the EM: (1) a recorded advise fixture's anchors are
  the **deterministic Finding ids** the FindingEngine hashes — and that hash
  includes `project_id` — so the live e2e + composition test pin a **fixed
  project_id** (`11111111-…`) matching the recorded anchors; a random uuid would
  re-hash every Finding id and drop every Recommendation. (2) RLS forbids a
  test-side DELETE on `cognition_history_record`, so the live e2e asserts on the
  **delta** of CHR rows it appends (snapshot-before → diff-after), never absolute
  counts — idempotent across re-runs.
- **No STOP/escalation.** No topology/state/GraphState change was needed; the
  `deep_pass` `stage_advise` node already existed and is fed via `register_stage`.
- **No new package, no new migration, no new output_kind** (`recommendation` /
  `clarification` already in the CHECK + `OutputKind` Literal).
- READ-ONLY guardrails respected: no edits to `wave_b.py`, `deep_pass.py`,
  `state.py`, `runner.py`, `registry.py`, `stages.py`, `infer/**`, `evaluate/**`,
  `retain/**`, `perceive/**`, any migration, `gate_invariants.py`, or recorded-
  fixture content. `wave_c.py` reuses `EvaluateEngine.form_issue` only as a
  **read** to reconstruct anchorable Issue ids (Evaluate remains the sole producer
  of the persisted Issues). Naming: the test double is a *recorded model-response
  fixture* — nothing named "replay"/"cassette".
- Did NOT `git commit` (EM reviews + commits).

## Engineering-manager review notes

**Review (2026-06-18).** Single worker, no STOP. EM independently verified:

- **Scope correct:** `advise/{__init__,engine,stage}.py`, new `orchestration/wave_c.py`,
  `shared/epistemic.py` (Recommendation/ClarificationRequest), `config.py` (advise routing),
  `events.py` + gate-5 (both test files updated — DTM-0009 regression not repeated), advise test
  suites. **Frozen modules untouched** (empty diff): `wave_b.py`, `graphs/`, `state.py`,
  `runner.py`, `registry.py`, `stages.py`, `infer/**`, `evaluate/**`, `retain/**`, migrations,
  `gate_invariants`. No new package, no migration (`recommendation`/`clarification` already in CHECK).
- **One-producer preserved:** the advise path emits **no** `issue_generated` and appends no issue
  CHR; it re-derives Issue identity via the pure `EvaluateEngine.form_issue` only to anchor
  Recommendations. Evaluate stays the sole producer of persisted Issues.
- **"Advise proposes, never disposes" proven by negatives:** standalone/empty/unanchored
  Recommendation rejected or dropped; no standalone Resolution-Path object; Recommendation frozen
  (no change outside recompute); history-overwrite impossible; advise exports/exposes no
  evaluate/accept/execute/score producer; self-accept structurally impossible; Recommendation
  carries no severity/score/accept field; Clarification carries no answer/acceptance field.
  DL-055 honoured — emits the `generated` state only (no Accept/Defer/Reject/Apply).
- **CHR-append = DTM-0013 model pattern** (provenance_ref `{"emitted_by":"advise"}`); recompute
  supersedes (prior CHR byte-intact); `recommendation_generated`/`clarification_requested` +
  `cognition_history_record_appended` + `ai_spend_recorded`; mode/confidence_stage carried.
  AI-text via recorded fixtures (zero PR-CI provider calls); `wave_c.py` composes A→B→C by
  *calling* the frozen Wave B builder + `register_stage("advise", …)` — no topology change.

**EM-run verification (independent, 2026-06-18):**
- OFFLINE (`env -u SUPABASE_* -u OSLO_LLM_LIVE pytest`) → **498 passed, 69 skipped, 0 failed**
  (Wave-B baseline 455 → +43). LIVE (Supabase up, recorded fixtures) → **567 passed, 0 failed**
  (baseline 523 → +44); the **live A→B→C advise e2e PASSES** (2 passed). ruff clean · gate-4 PASS
  · gate-5 PASS.

**Accepted minor (follow-up, not a defect):** `wave_c.py` re-forms Issues via `form_issue` rather
than receiving them through the evaluate→advise handoff closure; pure+deterministic so the anchor
ids match what Evaluate persisted (live e2e confirms). Could be tightened to thread Issues via the
handoff in a later cleanup; not blocking.

## Approved by engineering manager

Status: Approved

Executive summary:
- DTM-0014 delivers IC/QA/OBS-WC-ADVISE core: Advise as the single producer of Recommendation +
  ClarificationRequest, each Derived and anchored to a Finding/Issue (standalone structurally
  impossible), emitted in the `generated` state only (DL-055), appending one CHR per emission via
  the Retain-owned repo and superseding on recompute. The advise stage is wired live (`wave_c.py`)
  so the full A→B→C chain runs end-to-end. "Advise proposes, never disposes" is proven by the
  governance-adjacent negative suite; Resolution-Paths stay presentation-only.

Verification:
- ruff clean · gate-4 PASS · gate-5 PASS · OFFLINE 498/69/0 · LIVE 567/0 (A→B→C e2e green).
  Scope-checked: frozen modules untouched; no migration/package; one-producer preserved.

Manual test plan:
- Live (Supabase up): admit evidence → infer → evaluate → advise → confirm `recommendation` +
  `clarification` CHR rows, each anchored to a Finding/Issue; recompute supersedes with prior CHRs
  byte-intact; no issue/finding CHR emitted by the advise path.

Remaining risks:
- The form_issue re-derivation (above) — accepted minor.
- Acceptance (Accept/Defer/Reject/Apply) is deliberately NOT here — Wave U / Phase V.
