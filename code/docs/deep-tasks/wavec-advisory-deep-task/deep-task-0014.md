# DTM-0014 — Advise core: Recommendation + Clarification, anchored, Derived, live A→B→C

**Status:** Planned — BLOCKED on Wave B exit-gate + DL-044 authorization · **Module:** DTM-0014 ·
**Phase:** IV (Wave C) · **Contract:** **IC/QA/OBS-WC-ADVISE** (C0–C3) · **Depends:** Wave B
(Findings/Issues) approved; the DTM-0013 CHR-model fix.

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

_(worker fills)_

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_
