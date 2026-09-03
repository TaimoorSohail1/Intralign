# DTM-0015 — Advise: Suggested Fix (REC-04) + Validation Recommendation (REC-05)

> **Ready for review.**

**Status:** **Approved** (EM, 2026-06-18) · **Module:** DTM-0015 · **Phase:** IV
(Wave C) · **Contract:** **IC-WC-ADVISE — DL-047 Additions** (REC-04, REC-05) · **Depends:**
DTM-0014 (advise engine/stage + wave_c.py, landed).

## Goal / observable behavior

Advise generates a **`SuggestedFix`** — a candidate edit to a named artifact, **anchored to a
Finding**, **Derived**, CHR-appended — and a **Validation Recommendation** (REC-05): a
Recommendation `type=validation` seeking stakeholder confirmation. Emits `suggested_fix_offered`
(Validation rides `recommendation_generated`). **The headline invariant: OSLO never autonomously
writes/applies a fix** — applying is a *user-initiated* artifact edit that triggers recompute
(the apply surface + daily-cap MON are commodity / Wave I, NOT built here).

## Source docs / constraints

- `WAVE_C_AND_U_…ADVISORY…` **DL-047 Additions** (REC-04 SuggestedFix, REC-05 Validation) +
  Wave C C0–C3; Phase IV plan L56–58. `WAVE_I_CONTRACT_PACKAGE_INTERACTION_COLLABORATION.md`
  (Advise-relevant parts — application is Wave I/commodity, **out of scope here**).
- ADR-0008; `deep-task-decisions.md` #1–#12; DL-047/048; ADR-0004; ANTI_ASSUMPTION.

## Locked decisions

- **Reuse DTM-0014's advise stage + engines + wave_c.py** — additive only.
- **`SuggestedFix`** is a Derived Advise output anchored to a Finding; persists on the existing
  CHR `recommendation` `output_kind` + a payload `type=suggested_fix` discriminator (**NO new
  output_kind, NO migration** — a new kind ⇒ STOP/escalate). **Validation** is a Recommendation
  `type=validation` (rides `recommendation_generated`).
- **Critical negative:** OSLO autonomously writing/applying a fix to an artifact is **impossible**
  — no code path mutates an artifact; application originates from the user. Validation "routes to
  a CAF Review Request on user action" — the routing target is a user action, not an OSLO write.
- **Events:** ADD `EVENT_NAMES_WC_FIX = (suggested_fix_offered,)` (per the DL-047 OBS line);
  extend union + gate-5 + both test files. `recommendation_generated`/`cognition_history_record_
  appended` reused.
- **Types:** define `SuggestedFix` class in `shared/epistemic.py` (reserved in
  `CANONICAL_OUTPUTS`), Derived, `extra='forbid'`, with the Finding anchor + target-artifact ref
  + candidate-edit payload. Extend `Recommendation` with the `validation` type.
- **Cost (DL-048):** emit `ai_spend_recorded`; the daily fix-allowance gate is **commodity (MON),
  Wave I — do NOT build it here** (only note the seam).

## Owned files / boundaries

- **OWN (additive):** `backend/responsibilities/advise/**` (SuggestedFix + Validation generation —
  additive to DTM-0014) · `shared/epistemic.py` (ADD `SuggestedFix`; extend `Recommendation`
  type set) · `events.py` (ADD `EVENT_NAMES_WC_FIX`) · `ci/gate_observability.py` (additive) +
  both gate-5 test files · `tests/{positive,negative}/advise/**`, additive fixtures.
- **READ-ONLY:** everything DTM-0014 froze + `wave_b.py`, orchestration core, migrations,
  perceive/retain/infer/evaluate, gate_invariants/allowlist. **No artifact-mutation code anywhere.**

## Packages / refactors

- None new. No migration. No refactor of frozen modules.

## Implementation instructions (TDD)

1. Red: positives (`SuggestedFix`/`Validation` generate as Derived, Finding-anchored,
   CHR-appended; `suggested_fix_offered` emitted) + the **Critical negative** (no autonomous
   artifact write — AST/grep proof that `advise/` exports/calls no artifact writer, plus a
   behavioral test that generating a fix mutates no artifact and emits no write).
2. SuggestedFix generator + Validation type (LLM via fixtures); CHR per emission (model pattern);
   events + gate-5 vocab + both test files; OBS audit (the Finding it derives from).

## Test plan

- **Positive (`test_c2_*`):** SuggestedFix + Validation generate Derived + Finding-anchored +
  CHR-appended; `suggested_fix_offered` emitted; Validation as `recommendation_generated`
  `type=validation`.
- **Negative (Critical):** OSLO autonomously writing/applying a fix to an artifact — impossible
  (no artifact-mutation path; application is a user edit). Plus: SuggestedFix without a Finding
  anchor rejected; a new output_kind not introduced.
- **Determinism:** AI semantic; record-exact emission. AI offline via recorded fixtures.
- ruff + gate-4 + gate-5 green; full suite + live A→B→C no regression vs DTM-0014.

## Manual checks (EM)

- AST/grep: no function in `advise/` (or reachable from it) writes/edits an artifact.
- Live: a SuggestedFix persists as a `recommendation` CHR with `type=suggested_fix`, anchored;
  no artifact row is mutated.

## Done criteria

- REC-04/REC-05 generated as Derived, anchored, CHR-appended; **autonomous-write impossible**
  (Critical negative passes); no new kind/migration/package; PR cites `IC-WC-ADVISE` (DL-047).
  **Wave C candidate-complete → owner exit-gate before Phase V.**

## Worker report

**Ready for review.** DTM-0015 is additive to DTM-0014 — no frozen module rewritten.

### What was built (REC-04 SuggestedFix + REC-05 Validation)

- **`shared/epistemic.py`** — added the `SuggestedFix` class (Derived,
  `extra='forbid'`, `epistemic_state` pinned `DERIVED`): mandatory non-empty
  Finding `anchor`, `target_artifact` ref, `candidate_edit` payload, stable
  `suggested_fix_id`, version/`mode`/`confidence_stage`/`understanding_state`. The
  forbidden surface makes autonomous application unrepresentable (no
  `applied`/`written`/`apply`/`severity`/`score` field). Extended
  `RecommendationType` with `validation` (REC-05 rides the `recommendation`
  output).
- **`backend/responsibilities/advise/engine.py`** — added `derive_validations_ai`
  (Validation Recommendations, type pinned `validation`, anchored, unanchored
  dropped) and `derive_suggested_fixes_ai` (candidate edits anchored to a
  Finding; empty/unanchored dropped; `_suggested_fix_id` stable hash). Extended
  `AdviseResult` with `suggested_fixes`; wired both into `derive` (budget-gated
  like the existing passes, DL-048). The engine builds proposal objects only —
  it never writes/applies anything.
- **`backend/responsibilities/advise/stage.py`** — `SuggestedFix` persists on the
  EXISTING `recommendation` `output_kind` via `OUTPUT_KIND_SUGGESTED_FIX`
  (= `"recommendation"`) + a payload `type="suggested_fix"` discriminator (NO new
  kind, NO migration). One CHR per fix (DTM-0013 model pattern,
  `provenance_ref={"emitted_by":"advise"}`) paired with
  `cognition_history_record_appended`; `suggested_fix_offered` emitted per fix.
  Validations flow through the existing recommendation loop →
  `recommendation_generated` with `recommendation_type=validation`. Recompute
  supersedes by `suggested_fix_id`.
- **`backend/responsibilities/advise/__init__.py`** — exported
  `OUTPUT_KIND_SUGGESTED_FIX` + `SUGGESTED_FIX_PAYLOAD_TYPE`.
- **`events.py`** — added `EVENT_NAMES_WC_FIX = ("suggested_fix_offered",)` (per
  the DL-047 OBS line); extended the union (9-way) + the UnknownEventError text.
- **`ci/gate_observability.py`** — additive `EXPECTED_EVENT_NAMES_WC_FIX`, union
  leg, `_CONTRACT_VOCABULARIES` entry, `_UNION_NAME_ORDER` entry + docstring.
- **Both gate-5 test files updated** (not left on the old union): positive adds
  `test_wc_fix_vocabulary_is_the_one_dl047_suggested_fix_name_verbatim` + 9-way
  union assertion; negative adds WC_FIX tamper + missing-tuple tests, the 9-way
  union-drop, and bumps the missing-assignment count 9→10.
- **Fixtures (additive)** — `wc_advise_v0.json` (+`validation`, `suggested_fix`,
  `suggested_fix_unanchored`, `*_empty` keys) and `wc_advise_e2e_v0.json`
  (+`validation`, `suggested_fix` anchored to the deterministic Finding ids).

### C2 / DL-047 → test map (incl. the Critical autonomous-write negative)

| Contract behavior | Test |
|---|---|
| REC-04 SuggestedFix Derived + Finding-anchored | `tests/positive/advise/test_c2_suggested_fix_and_validation.py::test_c2_suggested_fix_generated_derived_and_anchored_to_its_finding` |
| REC-04 rides existing `recommendation` kind + `type=suggested_fix` (no new kind) | `…::test_c2_suggested_fix_persists_on_recommendation_kind_with_type_discriminator` |
| `suggested_fix_offered` emitted one-per-fix | `…::test_c2_suggested_fix_offered_emitted_one_per_fix` |
| REC-05 Validation rides recommendation, `type=validation` | `…::test_c2_validation_recommendation_rides_recommendation_with_type_validation` |
| REC-05 emitted as `recommendation_generated` `type=validation` | `…::test_c2_validation_emitted_as_recommendation_generated_type_validation` |
| Every emission pairs with a CHR append (incl. fixes) | `…::test_c2_every_emission_pairs_with_a_chr_append_including_fixes` |
| Recompute appends fix CHR, prior byte-intact | `…::test_c2_suggested_fix_recompute_appends_keeping_prior_chr_intact` |
| **CRITICAL — no autonomous artifact write (AST/grep): advise imports no artifact-writer** | `tests/negative/advise/test_c3_no_autonomous_fix_write.py::test_c3_advise_imports_no_artifact_writer_module` |
| **CRITICAL — advise calls no artifact-mutation method** | `…::test_c3_advise_modules_call_no_artifact_mutation_method` |
| **CRITICAL — advise exposes no apply/write surface** | `…::test_c3_advise_exposes_no_apply_or_write_surface` |
| **CRITICAL — behavioral: generating a fix mutates no artifact + emits no write event** | `…::test_c3_generating_fixes_mutates_no_artifact_and_emits_no_write_event` |
| SuggestedFix without a Finding anchor rejected | `…::test_c3_suggested_fix_without_anchor_is_structurally_impossible` / `…_empty_anchor_is_rejected` / `…_model_returned_unanchored_fix_is_dropped` |
| SuggestedFix carries no applied/written/apply field | `…::test_c3_suggested_fix_carries_no_applied_or_write_field` |
| No new `output_kind` introduced | `…::test_c3_no_new_output_kind_introduced_for_suggested_fix` |
| gate-5 vocab (WC_FIX verbatim) | `tests/positive/observability/test_gate_observability.py::test_wc_fix_vocabulary_is_the_one_dl047_suggested_fix_name_verbatim` (+ negative tamper/missing tests) |

### How the no-autonomous-write invariant is proven

Two independent ways, both red-proven (a synthetic module importing
`…persistence.intake_store` and calling `.apply(...)` is caught by the same
predicates): **(a)** AST/grep — advise's own modules import none of the
artifact-writer modules (`persistence.intake_store`/`retention_store`,
`perceive.intake`, `retain.repository`) and contain no
`update`/`upsert`/`delete`/`apply`/`write`/`commit`/`save`/`mutate` call (the
only `.append` is the Retain-owned CHR append — an append-only receipt, not an
artifact write); advise exposes no `def apply*`/`def write_artifact`/`def commit`
surface. **(b)** Behavioral — a full `run_advise_stage` run with a sentinel
artifact: fixes ARE offered (`suggested_fix_offered` emitted) yet the sentinel is
byte-untouched (`write_count == 0`) and no artifact-write/mutation event
(`artifact_modified`/`knowledge_*`) is emitted.

### Exact commands + results

- **OFFLINE** (zero provider calls):
  `env -u SUPABASE_URL -u SUPABASE_SERVICE_ROLE_KEY -u SUPABASE_DB_URL -u OSLO_LLM_LIVE .venv/bin/python -m pytest tests/positive tests/negative tests/replay -q`
  → **518 passed, 69 skipped** (baseline 498/69 → +20 new tests; no regression).
- **LIVE**:
  `set -a; source .env; set +a; unset OSLO_LLM_LIVE; .venv/bin/python -m pytest tests/positive tests/negative tests/replay -q`
  → **587 passed** (baseline 567 → +20; the A→B→C e2e
  `test_c2_live_chain_e2e.py` ran and passed — verified 1 passed, not skipped).
- `.venv/bin/ruff check .` → **All checks passed!**
- `.venv/bin/python -m ci.gate_invariants` → **PASS** (gate-4).
- `.venv/bin/python -m ci.gate_observability` → **PASS** (gate-5).

### Flags / notes

- Frozen DTM-0014 advise tests were updated ADDITIVELY (not rewritten in intent)
  because SuggestedFix rides the same `recommendation` output_kind: count/set
  assertions now filter fix rows by the payload `type` discriminator and account
  for the additive `validation` recommendation. Engine/stage core logic from
  DTM-0014 was extended, never rewritten.
- One reword in `shared/epistemic.py`: a SuggestedFix doc-comment originally said
  "no-Authority"; reworded to "the no-self-govern rule" so gate-4's forbidden-
  token scan stays clean (no allowlist entry needed).
- No new package, no new `output_kind`, no migration, no artifact-mutation path
  anywhere reachable from `advise/`. The apply surface + daily fix-cap (commodity
  MON / Wave I) were NOT built (out of scope). No STOP/escalation was required.

## Engineering-manager review notes

**Review (2026-06-18).** Single worker, no STOP, additive to DTM-0014. EM independently verified:

- **Scope correct:** `advise/{__init__,engine,stage}.py` (additive), `shared/epistemic.py`
  (`SuggestedFix` + `validation` rec type), `events.py` + gate-5 (`EVENT_NAMES_WC_FIX`) + both
  test files, fixtures, advise tests (DTM-0014 tests extended additively + 2 new files). **Frozen
  modules untouched** (empty diff): `wave_b.py`, `wave_c.py`, `graphs/`, `state.py`, `runner.py`,
  `infer/**`, `evaluate/**`, `retain/**`, migrations, `gate_invariants`. **No new package, no
  migration, no new output_kind** (SuggestedFix rides `recommendation` + a `type=suggested_fix`
  payload discriminator).
- **Critical negative (the headline) proven two ways:** (a) AST/grep — `advise/` imports no
  artifact-writer module and contains no `update/upsert/delete/apply/write/commit` call (only
  `.append` = the append-only CHR); (b) behavioral — generating fixes mutates no artifact and
  emits no write event. Four locking tests: `…imports_no_artifact_writer_module`,
  `…call_no_artifact_mutation_method`, `…exposes_no_apply_or_write_surface`,
  `…generating_fixes_mutates_no_artifact_and_emits_no_write_event`.
- **REC-04/REC-05:** SuggestedFix + Validation generate Derived, Finding-anchored, CHR-appended
  (DTM-0013 model pattern); `suggested_fix_offered` emitted; Validation rides
  `recommendation_generated` `type=validation`; recompute supersedes by `suggested_fix_id`.
  Application surface + daily fix-cap (Wave I / commodity MON) deliberately **not** built.
- **Minor accepted:** one `epistemic.py` doc-comment dropped the literal "Authority" token
  ("no-self-govern") to keep gate-4's forbidden-token scan clean without an allowlist entry —
  concept preserved, cosmetic.

**EM-run verification (independent, 2026-06-18):**
- OFFLINE → **518 passed, 69 skipped, 0 failed** (DTM-0014 baseline 498 → +20). LIVE (Supabase up)
  → **587 passed, 0 failed** (baseline 567 → +20); A→B→C e2e still green. The REC-04/05 +
  no-autonomous-write tests: 17 passed. ruff clean · gate-4 PASS · gate-5 PASS.

## Approved by engineering manager

Status: Approved

Executive summary:
- DTM-0015 completes Wave C with the DL-047 additions: Advise generates `SuggestedFix` (REC-04,
  a Finding-anchored candidate edit) and `Validation` Recommendations (REC-05, seeking
  stakeholder confirmation), both Derived and CHR-appended on the existing `recommendation`
  output_kind — and **OSLO never autonomously writes a fix** (the Critical invariant, proven by
  AST + behavioral negatives). The apply surface and daily fix-cap stay commodity / Wave I.

Verification:
- ruff clean · gate-4 PASS · gate-5 PASS · OFFLINE 518/69/0 · LIVE 587/0 (A→B→C e2e green).
  Scope-checked: frozen modules untouched; no migration/package/output_kind.

Manual test plan:
- Live (Supabase up): run the chain → a SuggestedFix persists as a `recommendation` CHR with
  payload `type=suggested_fix`, anchored to a Finding; no artifact row is mutated; a Validation
  recommendation appears with `recommendation_type=validation`.

Remaining risks:
- Apply/daily-cap surface is Wave I (not built) — intentional.
- The form_issue re-derivation carried from DTM-0014 (accepted minor) is unchanged.
