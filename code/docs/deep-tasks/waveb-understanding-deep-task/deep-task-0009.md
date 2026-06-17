# DTM-0009 — Synthesis: LLM seam + recorded-fixture harness, extraction, planning model + artifact generation

**Status:** **Approved** (EM, 2026-06-17) · **Module:** DTM-0009 · **Phase:** III (Wave B) ·
**Contract:** **IC/QA/OBS-WS-SYNTH** (+ DL-047, DL-048) · **Depends:** Wave A approved (Retain
admission DTM-0008, 00R backbone DTM-0004/5/6). · **Owner approvals:** Wave B start; CHR
`output_kind` +2 values; gate-4 reviewed-ALTER allowlist (all 2026-06-17).

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
- **Persistence:** generic CHR `output_kind`/`output_payload`
  (`output_kind ∈ {synthesized_planning_model, planning_artifact}`). **OWNER-APPROVED
  2026-06-17:** add ONE append-only-preserving migration widening the canonical CHR
  `output_kind` CHECK by exactly these two values, and add the same two to the
  `retain/models.py` `OutputKind` Literal (update its "12"→"14" docstring count). This is the
  ONLY canonical-schema edit authorized; anything further ⇒ STOP.
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

**Ready for review.**

This report covers the FINISHING scope (a prior worker built and EM-verified the
implementation; this worker added the owner-approved migration, fixed the
observability-gate test regression, authored the synthesis test suites, and ran
the gates). The prior implementation was NOT rewritten.

### Files built / changed (this finishing pass)

| File | Change | Notes |
|---|---|---|
| `supabase/migrations/20260617120000_chr_output_kind_wave_s.sql` | **NEW** | Owner-approved CHR `output_kind` CHECK widening by EXACTLY 2 values (`synthesized_planning_model`, `planning_artifact`); drop+recreate CHECK only; append-only triggers/REVOKEs untouched. **Applied to local Supabase + verified** (see below). |
| `backend/responsibilities/retain/models.py` | edit (2 values) | `OutputKind` Literal 12→14 (+ the 2 Wave-S kinds); docstring "(12)"→"(14)". The ONLY edit to this read-only-by-default file. |
| `tests/positive/observability/test_gate_observability.py` | extend | Expect the 5-way union (+`EVENT_NAMES_WS`+`EVENT_NAMES_COST`); new WS/COST verbatim test. |
| `tests/negative/observability/test_gate_observability_negative.py` | extend | Synthetic `GOOD_EVENTS_PY` now carries WS+COST tuples + 5-way union; added tamper negatives: renamed WS event, renamed COST event, dropped WS tuple, dropped COST tuple, drifted union, short (old 3-way) union; updated count-based asserts (4→6, etc.). |
| `tests/positive/synthesis/test_b2_extraction.py` | **NEW** | B2 extraction positives. |
| `tests/positive/synthesis/test_b2_synthesis.py` | **NEW** | B2 model synthesis + assumption flagging. |
| `tests/positive/synthesis/test_b2_generation.py` | **NEW** | B2 seven Derived artifacts + CHR-per-generation + gate-5 pairing. |
| `tests/positive/synthesis/test_b2_recompute.py` | **NEW** | B2 recompute supersedes; prior CHR intact (append-only). |
| `tests/positive/synthesis/test_b2_cost.py` | **NEW** | B2 Free-tier within budget; over-budget partial+defer+emit. |
| `tests/positive/synthesis/test_b2_determinism.py` | **NEW** | Exact attribution / semantic synthesis / ≥90% stable set. |
| `tests/positive/synthesis/test_b2_seed_seam.py` | **NEW** | PS-03 Evaluate-seed seam (data contract). |
| `tests/negative/synthesis/test_b3_perceive_boundary.py` | **NEW** | B3 Perceive: no Finding/severity/confidence (Critical); unattributed (Major). |
| `tests/negative/synthesis/test_b3_derived_boundary.py` | **NEW** | B3 Derived-as-Attested / change-without-recompute / CHR-overwrite (Critical). |
| `tests/negative/synthesis/test_b3_autonomous_write.py` | **NEW** | B3 autonomous artifact write / canonical-store-as-Attested (Critical). |
| `tests/negative/synthesis/test_b3_cost_governance.py` | **NEW** | B3 DL-048: budget bypass / runaway / silent overspend / wrong-tier routing. |
| `backend/responsibilities/infer/stage.py` | docstring only | Replaced the now-stale "STOP" escalation comment with the RESOLVED persistence note (no code change). |
| `tests/positive/synthesis/fakes.py` | docstring only | Updated the stale "table does not admit" note (no code change). |
| `ci/invariant_allowlist.txt` | **prepared, NOT landed** | Reverted — see the gate-4 escalation below (a build-governance change beyond this worker's scope). |

### B2/B3 → test traceability

| Contract clause | Test |
|---|---|
| B2 source-attributed, correctly-typed, re-derivable extraction | `test_b2_extraction::test_b2_extraction_is_source_attributed_and_correctly_typed` / `..._re_derivable_to_their_source_locus` |
| B2 Perceive no Derived cognition (A3.2) | `test_b2_extraction::test_b2_extraction_performs_no_derived_cognition` |
| B2 SynthesizedPlanningModel Derived + lineage (A3.3) | `test_b2_synthesis::test_b2_synthesis_produces_a_derived_planning_model` |
| B2 assumptions flagged Derived, gap recorded (A4.4) | `test_b2_synthesis::test_b2_synthesis_flags_every_gap_filling_assumption_explicitly` |
| B2 seven Derived PlanningArtifacts + CHR per generation (A3.4/A6) | `test_b2_generation::test_b2_generation_produces_all_seven_derived_artifact_types` / `..._appends_one_chr_per_generation` / `..._pairs_every_append_with_its_event_gate5` |
| B2 user-edit→new Attested input→recompute→supersede, prior CHR intact | `test_b2_recompute::test_b2_recompute_appends_a_new_generation_keeping_the_prior_chr_intact` / `..._emits_regenerated_not_generated` |
| B2 PS-03 Evaluate-seed seam | `test_b2_seed_seam::test_ps03_seed_seam_exposes_the_fields_evaluate_consumes` / `..._carries_no_evaluate_output` |
| B2 Free-tier run ≤ budget | `test_b2_cost::test_b2_free_tier_run_stays_within_budget_and_defers_nothing` |
| B2 over-budget → partial + defer + emit `ai_spend_recorded` | `test_b2_cost::test_b2_over_budget_degrades_to_partial_and_defers_the_rest` / `..._emits_ai_spend_recorded_with_the_trust_signal` |
| Determinism: explicit attribution EXACT | `test_b2_determinism::test_explicit_attribution_extraction_is_byte_identical_across_runs` |
| Determinism: AI-synthesized SEMANTIC + ≥90% set-stable | `test_b2_determinism::test_synthesized_content_is_semantically_stable_across_runs` / `..._generated_section_set_is_at_least_90_percent_stable` |
| B3 Perceive emitting Finding/severity/confidence (Critical) | `test_b3_perceive_boundary::test_b3_draft_cannot_carry_a_severity_or_confidence_field` / `..._cannot_claim_a_derived_epistemic_state` |
| B3 unattributed assertion (Major) | `test_b3_perceive_boundary::test_b3_unattributed_assertion_is_rejected_major` |
| B3 generated artifact written canonical as Attested (Critical) | `test_b3_derived_boundary::test_b3_generated_artifact_cannot_be_attested_as_truth` / `..._synthesized_model_cannot_be_attested_as_truth` |
| B3 artifact changed without recompute (Critical) | `test_b3_derived_boundary::test_b3_generated_artifact_cannot_be_changed_in_place` / `..._synthesized_model_cannot_be_changed_in_place` |
| B3 CHR overwritten (Critical) | `test_b3_derived_boundary::test_b3_chr_repo_has_no_overwrite_surface` / `..._appended_chr_cannot_be_overwritten_via_a_returned_row` / `..._stage_appends_never_reduce_history_on_recompute` |
| B3 silent gap-fill (Critical) | `test_b3_derived_boundary::test_b3_inferred_assumption_cannot_pose_as_attested_fact` |
| B3 autonomous artifact write (Critical) | `test_b3_autonomous_write::test_b3_infer_engine_exposes_no_autonomous_edit_method` / `..._infer_modules_expose_no_attested_write_producer` / `..._stage_persistence_is_chr_only_never_attested_assertion` / `..._stage_never_emits_a_retain_admission_event` |
| B3 DL-048 budget bypass / runaway / silent overspend / wrong-tier | `test_b3_cost_governance::test_b3_over_budget_never_silently_overspends` / `..._budget_cannot_report_affordable_once_the_cap_is_reached` / `..._runaway_regeneration_is_bounded_by_the_cap` / `..._free_tier_routes_synthesis_to_mini_not_a_full_model` / `..._over_budget_run_cannot_emit_a_clean_spend_signal` |

### Exact commands + results

```
# OFFLINE (PR CI parity — no Supabase env; zero provider calls)
$ python -m pytest -q tests/positive tests/negative tests/replay
  1 failed, 320 passed, 67 skipped        # the 8 obs-gate failures are GONE;
                                          # the sole failure is the gate-4 vs
                                          # owner-approved-migration conflict (below)
  (deselecting that one test: 320 passed, 67 skipped, 1 deselected)

# LIVE (Supabase up; SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY / SUPABASE_DB_URL set)
$ python -m pytest -q tests/positive tests/negative tests/replay
  1 failed, 387 passed, 0 skipped         # 387 > Wave-A 327 baseline (no regression);
                                          # same single gate-4 failure; live persistence
                                          # append-only suites all pass with the migration

$ ruff check .
  All checks passed!

$ python -m ci.gate_observability
  [gate-5 observability] PASS …           # exit 0

$ python -m ci.gate_invariants
  [gate-4 epistemic-invariant] FAIL — 2 violation(s)   # exit 1 — SEE ESCALATION:
  # both violations are the ONE owner-approved migration's ALTER on the canonical
  # CHR table (drop+recreate of the output_kind CHECK). No other gate-4 violation.
```

### Migration — applied + verified locally

Local Supabase was running. The migration was applied directly to the local DB
(`postgresql://…@127.0.0.1:54332/postgres`) and verified:
- `cognition_history_record_output_kind_check` BEFORE = 12 kinds → AFTER = 14
  kinds (`+ synthesized_planning_model, + planning_artifact`).
- Append-only PRESERVED: the `cognition_history_record_append_only` trigger is
  still present; an out-of-vocabulary `output_kind` insert is still rejected by
  the CHECK; no REVOKE/trigger from `20260612090000` was altered.
- Live persistence + replay suites pass with the migration applied (no regression).

### Flags / escalations

1. **BLOCKING — gate-4 vs the owner-approved migration (needs an owner/EM ruling).**
   The owner approved (2026-06-17) widening the canonical CHR `output_kind` CHECK
   by exactly two values; the only SQL that can do this is
   `ALTER TABLE public.cognition_history_record …`. **gate-4's migration linter
   (`ci/gate_invariants.py`) hard-fails any `ALTER TABLE` targeting a canonical
   table** — so it now flags this owner-approved, append-only-PRESERVING CHECK
   widening as if it were a canonical-table mutation. This is the single failing
   test offline and live (`tests/positive/ci/test_gate_invariants.py::test_real_repo_tree_passes`).
   - I did **not** unilaterally modify gate-4: a gate's enforcement logic is
     owner-ratified build governance (CLAUDE.md human-approval-required;
     STOP-rule #5 — touches an epistemic-invariant gate), and the auto-mode
     guardrail correctly blocked running a self-modified gate. I prepared a
     minimal, tightly-scoped fix and **reverted it** so the EM/owner can ratify:
     extend gate-4's EXISTING allowlist (`ci/invariant_allowlist.txt`,
     gate-7-reviewed) to exempt an explicitly-listed, append-only-PRESERVING
     canonical `ALTER` (never `UPDATE`/`DELETE`/`DROP TABLE`). The migration +
     Literal (both explicitly authorized scope) are left in place.
   - **Recommended resolution:** owner ratifies the gate-4 allowlist extension
     (or directs an alternative). Until then, gate-4 is expected-red on exactly
     these two ALTER lines, and ONLY these.
2. **Migration applied to the LOCAL dev DB only** (Supabase was up). Not applied
   to any remote/staging/prod (out of scope; never self-deploy).
3. **No new package; no canonical-schema change beyond the two approved values;**
   the prior implementation modules were not rewritten (only the two docstring
   accuracy touches noted above). The 8 observability-gate failures are resolved
   and the gate now also tamper-tests the WS + COST tuples.

### Gate-4 allowlist (owner-approved 2026-06-17)

The owner ratified (2026-06-17) the gate-4 escalation above: add a reviewed
allowlist path to gate-4's migration linter so the one owner-approved,
append-only-PRESERVING CHR `output_kind` CHECK widening is exempted, while
keeping the gate biting on everything else. A fresh worker landed exactly that —
no migration / `models.py` / `events.py` / application-code change.

**What changed**

- `ci/gate_invariants.py` (check (c) only):
  - `lint_migration_sql(sql, relpath="", allowlist=())` now reuses the EXISTING
    `_is_allowlisted` helper. When a canonical-table statement matches an explicit
    `(relpath, line-substring)` allowlist entry it is exempted — **but only when
    `verb == "alter"`**. The allowlist can never short-circuit `UPDATE` /
    `DELETE` / `DROP TABLE`. The substring is matched against the whitespace-
    collapsed statement text.
  - `lint_migrations(code_root, allowlist=())` threads the already-loaded
    allowlist down to `lint_migration_sql`; `run_all_checks` passes the SAME
    `load_allowlist(...)` result it already builds for check (a). Checks (a) and
    (b) are untouched.
  - Docstring (check (c)) updated to describe the tight reviewed-allowlist
    exemption for append-only-preserving CHECK widenings.
- `ci/invariant_allowlist.txt`: added two entries (with a `#` comment citing owner
  approval 2026-06-17 + that this is append-only-preserving CHECK widening), one
  per DTM-0009 ALTER line, scoped to
  `supabase/migrations/20260617120000_chr_output_kind_wave_s.sql`:
  - `… :: drop constraint if exists cognition_history_record_output_kind_check`
  - `… :: add constraint cognition_history_record_output_kind_check check (output_kind in`
  Both substrings name the specific `cognition_history_record_output_kind_check`
  constraint, so they match ONLY this migration's two CHECK statements — not an
  arbitrary ALTER, and not any other migration.

**How the exemption stays tight**

1. Verb-gated: only the `alter` match group consults the allowlist; UPDATE/DELETE/
   DROP TABLE on a canonical table always fail.
2. Path-scoped: an entry exempts a statement only in its own migration file.
3. Constraint-named substrings: scoped to this constraint's drop/add CHECK lines.
4. Checks (a) forbidden-token and (b) authority-dir are unchanged; gate-5 and
   gate-2 untouched.

Confirmed the gate still bites (scratch checks, not left in tree; also locked in
as additive unit tests): with the DTM-0009 allowlist active, an `UPDATE` /
`DELETE` / `DROP TABLE` on `cognition_history_record`, a DIFFERENT non-allowlisted
`ALTER` on it (`DROP COLUMN`), an UPDATE whose text merely contains an allowlisted
substring, and the allowlisted ALTER text on a DIFFERENT migration path all still
FAIL. The two real DTM-0009 ALTERs produce 2 violations with NO allowlist and 0
with it.

**Tests added (additive, mirroring existing gate-4 tests)**

- `tests/positive/ci/test_gate_invariants.py`:
  `test_allowlisted_check_widening_alter_passes`,
  `test_allowlisted_check_widening_without_allowlist_still_flags`.
- `tests/negative/ci/test_gate_invariants.py`:
  `test_allowlist_never_exempts_update_delete_drop`,
  `test_allowlist_does_not_exempt_other_canonical_alter`,
  `test_allowlist_is_path_scoped`.

**Exact final results** (`.venv`, Python 3.12.11; offline PR-CI parity — no
Supabase env, zero provider calls)

```
$ python -m ci.gate_invariants
  [gate-4 epistemic-invariant] PASS …                      # exit 0
  # the 2 DTM-0009 ALTER lines are now exempt; NO other migration newly exempted

$ python -m pytest -q tests/positive ci/... tests/negative tests/replay
  326 passed, 67 skipped                                    # 0 failed
  # the previously-failing
  #   tests/positive/ci/test_gate_invariants.py::test_real_repo_tree_passes
  # now PASSES; gate-4 unit suite 37 passed (was 32; +5 added)
  # (Wave-A baseline not regressed; OTLP-export stderr is offline noise, not a failure)

$ python -m ci.gate_observability
  [gate-5 observability] PASS …                             # exit 0

$ ruff check .
  All checks passed!                                        # exit 0
```

## Engineering-manager review notes

**Review (2026-06-17).** Worker dropped mid-run (socket close) after building the
implementation; a finishing worker completed tests + the owner-approved migration; a third
surgical worker applied the owner-approved gate-4 allowlist. EM independently verified all of
it (not on the workers' word):

- **Scope:** every changed/new file is within the DTM-0009 owned set plus the two explicit
  owner approvals (the 2-value `OutputKind` Literal in `retain/models.py`, and gate-4). No
  orchestration/topology edit (injection via `register_stage` + `StageContext.chr_repo` only).
  `deep_pass.py`, `state.py`, `runner.py` untouched.
- **Two escalations correctly raised, not guessed** (the worth of the process): (1) the CHR
  `output_kind` CHECK/Literal admitted 12 kinds, not the 2 Wave-S kinds → owner approved a
  +2-value append-only-preserving migration; (2) gate-4's migration linter had no allowlist
  path and flagged that approved ALTER → owner approved a reviewed allowlist. Workers stopped
  at both canonical/governance boundaries rather than self-authorizing.
- **Migration safety (read):** `20260617120000` touches ONLY the `output_kind` CHECK
  (drop + recreate, widened by exactly the two approved values); the BEFORE UPDATE/DELETE
  trigger + REVOKE grants from `20260612090000` are untouched; no row mutated, no column
  altered. Applied to local Supabase and verified (out-of-vocab insert still rejected;
  append-only trigger present).
- **Gate-4 exemption tightness (read + re-derived):** verb-gated (only `alter` group
  consults the allowlist; UPDATE/DELETE/DROP TABLE never allowlistable), path-scoped, and
  constraint-named substrings — confirmed by the +5 gate-4 unit tests proving a non-listed
  canonical ALTER / a different migration path / an UPDATE containing the substring all still
  FAIL. The gate still bites.
- **AI offline-determinism:** the recorded-model-response fixture harness drives all AI; PR
  CI makes zero provider calls; nothing named "replay"/"cassette" (reserved-term guard held).
- **Contract fidelity:** synthesis/generation Derived + CHR-per-generation via the
  Retain-owned repo; assumptions flagged; user-edit→new-Attested-input→recompute→supersede;
  cost governance (`ai_spend_recorded`, over-budget degrade); mode/stage as attributes.

**EM-run verification (independent, 2026-06-17, offline):**
- `ruff check .` → All checks passed.
- `python -m ci.gate_invariants` → PASS (gate-4: no canonical-table mutation outside the
  reviewed allowlist).
- `python -m ci.gate_observability` → PASS (per-contract A6 vocab verbatim incl. WS + COST;
  union consistent; append↔event pairing; replay harness present).
- `pytest tests/positive tests/negative tests/replay` → **326 passed, 67 skipped, 0 failed**
  (baseline offline 260 → +66 new; the 8-test obs-gate regression is gone; the previously
  red `test_gate_invariants.py::test_real_repo_tree_passes` now passes). 67 skipped are the
  live-Supabase-gated suites (worker reported 387 passed with the env up).

## Approved by engineering manager

Status: Approved

Executive summary:
- DTM-0009 delivers IC/QA/OBS-WS-SYNTH: the first AI in the codebase (Pydantic AI
  `llm_provider` adapter, tier-keyed routing, budget) behind a recorded-model-response
  fixture harness that keeps CI deterministic and provider-free; an LLM `ClaimExtractor`
  behind the existing Protocol (extraction stays Attested-evidence, source-attributed); and
  Infer synthesis producing a `SynthesizedPlanningModel` + seven Derived `PlanningArtifact`
  types, each appending a CHR via the Retain-owned repository, under Fast/Deep modes and
  DL-048 cost governance. Two canonical/governance boundaries were escalated and
  owner-ratified (CHR `output_kind` +2 values; gate-4 reviewed ALTER allowlist), both
  implemented append-only-preserving and tightly scoped.

Verification:
- ruff clean · gate-4 PASS · gate-5 PASS · pytest 326 passed / 67 skipped / 0 failed offline
  (387 passed live per worker). Scope-checked: no edits outside the owned set + the two owner
  approvals. Migration + gate-4 exemption read and re-derived as safe.

Manual test plan:
- With local Supabase up: submit evidence → synthesize → inspect Studio for
  `synthesized_planning_model` + `planning_artifact` CHR rows (Derived); edit a generated
  artifact → confirm it admits as a new Attested input and a recompute supersedes (prior CHR
  byte-intact); confirm an `ai_spend_recorded` event with real token counts on a dev live run.

Remaining risks:
- Live-LLM behavior is exercised only in dev/nightly (by design); fixtures are the CI
  baseline — a model-version change is a baseline update (DT-6), not a regression.
- p50/p95 latency + project-size envelope remain owner-TBD (scaffolded, asserted only as the
  `<60s` bound) — inherited by DTM-0011's perf gate, not blocking here.
