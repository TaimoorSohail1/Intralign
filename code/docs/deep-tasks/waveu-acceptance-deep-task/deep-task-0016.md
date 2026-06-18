# DTM-0016 — Plan-Fact recording: accept/direct-edit → user-attested AttestedAssertion

> **Ready for review.**

**Status:** **Approved** (EM, 2026-06-18) · **Module:** DTM-0016 ·
**Phase:** V (Wave U) · **Contract:** **IC/QA/OBS-WU-ACCEPT** (U1.2, U2, U3) · **Depends:** Wave A
acceptance path (capture + UAR) + Phase IV (recs to accept) — present in this branch. · **Note:**
Phase IV PR #46 + the gate-3 fix sync to `main` still pending; owner directed Phase V start.

## Goal / observable behavior

Complete the confirm path: when a user **accepts** a recommendation (or **direct-edits**), OSLO
records **both** (a) the existing **UserAcceptanceRecord** (version-pinned, append-only) **and**
(b) a **plan fact** — a user-attested `AttestedAssertion` (`attesting_source=user`,
`epistemic_state=attested-user`) holding the **confirmed content** as "factual in the plan, not
world-truth". **reject/defer** record the UAR (action) but **no plan fact**. The acceptance path
emits `user_acceptance_record_appended` + `plan_fact_recorded`. The **user** authors the plan
fact; OSLO never auto-promotes its own Derived recommendation, never marks anything world-true,
and **never self-accepts**.

## Source docs / constraints

- `WAVE_C_AND_U…ADVISORY_AND_ACCEPTANCE.md` **Wave U** U0–U3: U1.2 (record TWO canonical items —
  UAR **and** plan fact), the (G) forbidden invariants, U2 QA, U3 OBS. Plan-Fact §0.1 (DL-043).
- ADR-0009; `deep-task-decisions.md` #2–#4, #7, #9–#10; LDM §2.1/§2.4; ANTI_ASSUMPTION.

## Locked decisions (from decisions file — do not re-derive)

- **Plan fact = `AttestedAssertion`** in `attested_assertion` (`attesting_source=user`,
  `epistemic_state=attested-user`, `content_type` from the LDM set — default `fact`), written
  **only** on `accept` and `direct_edit`. Content: for **accept**, derive from the pinned CHR's
  `output_payload` (the accepted recommendation's content — a data read, no LLM); for
  **direct_edit**, from the capture's edit content. **NO migration** (the table admits
  `attested-user`).
- **Extend `retain/acceptance.py` additively** (Wave-A approved): keep the UAR write as-is; ADD
  the plan-fact write (accept/direct-edit only) and ADD an **emitter** parameter (Wave A took
  none). Emit `user_acceptance_record_appended` (for the UAR) + `plan_fact_recorded` (for the
  plan fact). reject/defer: UAR only, no plan fact, no `plan_fact_recorded`.
- **Define `PlanFact`** in `shared/epistemic.py` (reserved in `CANONICAL_OUTPUTS`): Attested,
  `epistemic_state=attested-user`, `extra='forbid'`, carries the version-pin + content + user
  attribution; **no field marks world-truth/approval** (structurally).
- **Events:** add `EVENT_NAMES_WU_ACCEPT` (this slice's part: `user_acceptance_record_appended`,
  `plan_fact_recorded`) verbatim per OBS-WU C3; extend the union; gate-5 vocab + **both** gate-5
  test files (do not repeat the DTM-0009 regression). `acceptance_impact_assessed` is DTM-0017.
- **Never-self-accept (hard rule #5):** OSLO never authors a plan fact without a user action;
  no code path promotes an OSLO recommendation to Attested. Determinism: **record-exact**.

## Owned files / boundaries

- **OWN (additive):** `backend/responsibilities/retain/acceptance.py` (plan-fact write +
  emitter — additive; the UAR write stays intact) · `shared/epistemic.py` (ADD `PlanFact`) ·
  `backend/services/observability/events.py` (ADD `EVENT_NAMES_WU_ACCEPT`) ·
  `ci/gate_observability.py` (additive vocab + tamper) + **both** gate-5 test files ·
  `backend/responsibilities/perceive/acceptance_capture.py` (ONLY if the capture must carry
  direct-edit content — additive field; else read-only) · `tests/{positive,negative}/
  acceptance/**` (or `retain_retention/`), additive fixtures.
- **READ-ONLY:** the UAR row shape + `user_acceptance_record` table + ALL migrations (schema gap
  ⇒ STOP) · `services/persistence/retention_store.py` (use `insert_assertion`/`insert_acceptance`
  as-is) · advise/infer/evaluate/orchestration · gate_invariants/allowlist.

## Packages / refactors

- None new. No migration. Additive extension of the acceptance path only.

## Implementation instructions (TDD)

1. Red: `test_u2_*` (accept → UAR + plan fact, version-pinned, attested-user, append-only;
   direct-edit → plan fact without a recommendation; reject/defer → UAR only, no plan fact;
   events emitted) and the (G) negatives (world-true / OSLO-approved; UAR-as-GovernanceDecision;
   overwrite; missing version-pin; OSLO self-promotion/self-accept).
2. `PlanFact` type; plan-fact write in `record_acceptance` (accept/direct-edit branch); emitter
   wired; events + gate-5 vocab + both test files; OBS audit (user attribution + version-pin).

## API / data / schema contracts

- `PlanFact`: `AttestedAssertion` row — `attesting_source=user`, `epistemic_state=attested-user`,
  `content_type` (default `fact`), `proposition`/content, `provenance_ref` (version-pin + user +
  capture). **No schema change.** UAR row shape unchanged.

## Test plan (QA-WU-ACCEPT)

- **Positive (`test_u2_*`):** both UAR + plan fact on accept; direct-edit plan fact; reject/defer
  no plan fact; version-pin mandatory; events `user_acceptance_record_appended` +
  `plan_fact_recorded`.
- **Negative:** acceptance-as-world-truth / OSLO-approved *(Critical)*; UAR-as-Governance-Decision
  *(Critical)*; record overwrite *(Critical)*; missing version-pin *(Major)*; OSLO promoting its
  own recommendation to Attested / self-accept *(Critical)*.
- **Determinism:** record-exact replay for UAR + plan fact. AI offline (none needed here).
- ruff + gate-4 + gate-5 green; baseline (offline 518 / live 587) no regression.

## Manual checks (EM)

- Live: accept → `user_acceptance_record` (version-pinned) **and** `attested_assertion` plan fact
  (`attested-user`); reject → UAR only; both append-only (overwrite denied at the DB).
- AST/grep: no field/codepath marks an item true/approved; plan fact only on user action.

## Done criteria

- U2 positive/negative traceability in report; plan fact on accept/direct-edit (not reject/defer),
  version-pinned + append-only + attested-user; never-self-accept proven; events present; no
  migration/package; PR cites `IC-WU-ACCEPT`. Ready for DTM-0017.

## Worker report

**Summary.** Completed the confirm path additively: a user **accept** / **direct_edit**
now records **two** canonical items — the existing version-pinned `UserAcceptanceRecord`
(unchanged Wave-A write) **and** a new user-attested **plan fact** (`attested_assertion`
row, `attesting_source=<user_id>`, `epistemic_state=attested-user`, the confirmed content).
**reject / defer** record the UAR only (no plan fact). The path now emits
`user_acceptance_record_appended` (always) + `plan_fact_recorded` (confirm only). Defined
the `PlanFact` type, added `EVENT_NAMES_WU_ACCEPT`, wired gate-5. No migration, no new
package.

### Files changed

- `shared/epistemic.py` — **ADD** `PlanFact` (Attested, `epistemic_state` pinned
  `ATTESTED_USER`, `extra='forbid'`, mandatory `proposition` + `attested_by_user` +
  `version_pin` + `provenance_ref`; `content_type` default `fact`). No field can mark
  world-truth/approval/governance/applied (structurally forbidden). `PlanFact` was already
  reserved in `CANONICAL_OUTPUTS`.
- `backend/responsibilities/retain/acceptance.py` — **ADDITIVE rewrite**: UAR write kept
  intact; on `accept`/`direct_edit` also writes a plan fact via `store.insert_assertion`
  (`attesting_source=user`) + an audit history entry; added an **optional** `emitter`
  param (default `None` → existing callers unaffected) and an optional `chr_reader` (READ
  seam for the accept content); emits both OBS events. Added `ChrReader` protocol +
  `_plan_fact_proposition` (accept → pinned CHR `output_payload` data read, NO LLM;
  direct_edit → capture `edit_content`). `AcceptanceRecordResult` gained
  `plan_fact_id`/`plan_fact` (None on reject/defer).
- `backend/responsibilities/perceive/acceptance_capture.py` — **ADD** optional
  `edit_content` field to `AcceptanceCapture` (carries the direct-edit confirmed content;
  not a truth/approval marker).
- `backend/services/observability/events.py` — **ADD** `EVENT_NAMES_WU_ACCEPT =
  ("user_acceptance_record_appended", "plan_fact_recorded")`; extended the union (placed
  after `WC_FIX`, before `COST`); updated the `UnknownEventError` message.
- `ci/gate_observability.py` — **ADD** `EXPECTED_EVENT_NAMES_WU_ACCEPT`, union leg,
  `_CONTRACT_VOCABULARIES` entry (`IC-WU-ACCEPT C3`), `_UNION_NAME_ORDER` entry, docstring.
- `tests/positive/observability/test_gate_observability.py` +
  `tests/negative/observability/test_gate_observability_negative.py` — updated for the new
  tuple (verbatim test + tamper/missing tests + 10-way union + missing-assignment count
  10→11).
- **New tests:** `tests/positive/retain_retention/test_u2_plan_fact.py`,
  `tests/negative/retain_retention/test_u2_plan_fact_negative.py`,
  `tests/replay/test_plan_fact_replay.py`. **Fakes:** `InMemoryChrReader` added to
  `tests/positive/retain_retention/fakes.py`.
- **Updated existing tests** (additive impacts): `test_b2_acceptance.py` (chr_reader on
  accept; UAR-only-on-reject footprint; UAR history filter; live plan-fact assertions),
  `test_b4_acceptance_negative.py` (emitter is now an optional param; reject footprint),
  `test_b3_silent_supersession.py` (`acceptance.py` now an `insert_assertion` site but its
  plan-fact write carries NO `supersedes_id`), `test_b3_forbidden.py` (capture field set
  now includes `edit_content`).

### U2 → test map (incl. the (G) negatives)

| QA-WU-ACCEPT U2 item | Severity | Test(s) |
|---|---|---|
| Confirm writes BOTH UAR + plan fact (accept) | positive | `test_u2_accept_writes_both_the_uar_and_a_plan_fact` |
| Plan fact version-pinned to accepted emission | positive | `test_u2_accept_plan_fact_is_version_pinned_to_the_accepted_emission` |
| Accept content = pinned CHR payload (data read, no LLM) | positive | `test_u2_accept_plan_fact_content_is_a_data_read_of_the_pinned_chr` |
| Direct-edit plan fact from edit content, no recommendation | positive | `test_u2_direct_edit_writes_plan_fact_from_edit_content_without_a_recommendation` |
| reject → UAR only, no plan fact | positive | `test_u2_reject_records_the_uar_but_no_plan_fact` |
| defer → UAR only, no plan fact | positive | `test_u2_defer_records_the_uar_but_no_plan_fact` |
| Events: appended then plan_fact_recorded (accept) | positive | `test_u2_accept_emits_uar_appended_then_plan_fact_recorded` |
| Events: both on direct-edit | positive | `test_u2_direct_edit_emits_both_events` |
| Events: only UAR event on reject | positive | `test_u2_reject_emits_only_the_uar_event_not_plan_fact_recorded` |
| Append-only: two confirms → two distinct rows | positive | `test_u2_two_accepts_append_two_distinct_plan_facts_never_overwrite` |
| Plan-fact audit history appended | positive | `test_u2_plan_fact_history_entry_is_appended` |
| **(G) acceptance/plan-fact NOT world-true / NOT OSLO-approved** | **Critical** | `test_u2_plan_fact_row_carries_no_truth_or_approval_marker`, `test_u2_plan_fact_shape_forbids_a_truth_or_approval_field`, `test_u2_plan_fact_epistemic_state_cannot_be_oslo_or_derived` |
| **(G) UAR is NOT a Governance Decision** | **Critical** | `test_u2_governance_decision_is_banned_vocabulary`, `test_u2_acceptance_path_never_mentions_governance_or_authority` |
| **(G) record overwrite impossible (DB-shaped)** | **Critical** | `test_u2_plan_fact_write_never_carries_a_supersedes_id`, `test_u2_repeated_confirm_appends_a_new_row_never_overwrites`, `test_u2_store_has_no_update_or_delete_surface` |
| **(G) OSLO never self-promotes / self-accepts** | **Critical** | `test_u2_plan_fact_attesting_source_is_always_the_user_never_oslo`, `test_u2_no_plan_fact_is_authored_without_a_user_action`, `test_u2_plan_fact_marks_the_accepted_recommendation_nothing` |
| **(G) version-pin mandatory** | **Major** | `test_u2_confirm_without_version_pin_is_rejected_before_any_write`, `test_u2_direct_edit_without_edit_content_is_rejected` |
| Determinism: record-exact (UAR + plan fact + event) | replay | `test_plan_fact_replay.py` (4 tests, incl. tamper detection) |

### Never-self-accept + plan-fact-only-on-accept/edit — how proven

- **Never-self-accept (hard rule #5):** `PlanFact.epistemic_state` is a pinned `Literal`
  (`ATTESTED_USER`) — `attested-oslo` / `derived` are rejected at construction
  (`test_u2_plan_fact_epistemic_state_cannot_be_oslo_or_derived`); the write always sets
  `attesting_source=<user_id>` (`test_u2_plan_fact_attesting_source_is_always_the_user_never_oslo`);
  the accepted Derived recommendation is never mutated/promoted — the `chr_reader` is
  READ-only (`test_u2_plan_fact_marks_the_accepted_recommendation_nothing`).
- **Plan fact ONLY on accept/direct_edit:** `_PLAN_FACT_ACTIONS = {accept, direct_edit}`
  gates the write; reject/defer write nothing into `attested_assertion`
  (`test_u2_reject…`, `test_u2_defer…`, `test_u2_no_plan_fact_is_authored_without_a_user_action`).

### Exact commands + results

- **OFFLINE:**
  `env -u SUPABASE_URL -u SUPABASE_SERVICE_ROLE_KEY -u SUPABASE_DB_URL -u OSLO_LLM_LIVE .venv/bin/python -m pytest tests/positive tests/negative tests/replay -q`
  → **551 passed, 70 skipped** (baseline 518/69 → +33 passed, +1 skip [new live plan-fact
  test]; no regression).
- **LIVE:**
  `set -a; source .env; set +a; unset OSLO_LLM_LIVE; .venv/bin/python -m pytest tests/positive tests/negative tests/replay -q`
  → **621 passed** (baseline 587 → +34 live-runnable; no regression).
- `.venv/bin/ruff check .` → **All checks passed!**
- `.venv/bin/python -m ci.gate_invariants` → **gate-4 PASS**.
- `.venv/bin/python -m ci.gate_observability` → **gate-5 PASS**.

### Flags / notes for the EM

- **Schema interaction (no migration; resolved within boundaries):** the plan-fact write
  needed an audit `history_record` entry, but the `history_record.event_type` CHECK
  (migration `20260612090000`, line ~120) admits no `plan-fact-recorded` value. Per the
  no-migration constraint, the plan-fact history entry **reuses the admitted
  `acceptance-recorded` event_type**, discriminated by `subject_ref.record == "plan_fact"`
  + the `assertion_id`. The distinct OBS signal is the `plan_fact_recorded` event. The
  `attested_assertion` epistemic_state CHECK **does** admit `attested-user` (line 44) — the
  plan-fact row itself needs no schema change. (Caught only by the live tests; the offline
  fakes accept any event_type.)
- **`content_type` decision (residual #4):** defaulted to `fact` (LDM §2.1 set), per the
  contract/decisions default — an accepted recommendation's confirmed content is a plan
  fact. `PlanFactContentType` allows the full LDM set if a future caller needs it.
- **`AcceptanceRecordResult` shape grew** (`plan_fact_id`/`plan_fact`, both optional) —
  additive, defaults preserve existing reads.
- No STOP/escalation was required. All READ-ONLY boundaries respected (migrations,
  retention_store internals via `insert_*`, advise/infer/evaluate/orchestration,
  gate_invariants/allowlist untouched).

## Engineering-manager review notes

**Review (2026-06-18).** Single worker, no STOP, additive. EM independently verified:

- **Scope correct:** `retain/acceptance.py` (plan-fact write + optional emitter + read-only
  `ChrReader` seam), `perceive/acceptance_capture.py` (additive `edit_content`),
  `shared/epistemic.py` (`PlanFact`), `events.py` + gate-5 (both test files), 3 new test files +
  4 updated existing. **Frozen untouched** (empty diff): migrations, orchestration,
  advise/infer/evaluate, `services/persistence`, `gate_invariants`. **No migration, no package.**
- **Plan-fact only on accept/direct-edit:** `_PLAN_FACT_ACTIONS={accept,direct_edit}` gates the
  write; reject/defer write only the UAR. UAR write unchanged (version-pin still mandatory).
- **Never-self-accept + (G) boundary proven** (27 tests): `PlanFact.epistemic_state` pinned
  `attested-user` (oslo/derived rejected at construction); `extra='forbid'` + no truth/approval/
  governance/applied field; `attesting_source` always the user; no plan fact without a user
  action; repeated confirm appends (no overwrite); store has no update/delete surface; UAR ≠
  Governance Decision (banned vocab).
- **History-event reuse accepted:** the `history_record` event_type CHECK (migration line 120)
  admits no `plan-fact-recorded`; the worker reused `acceptance-recorded` discriminated by
  `subject_ref.record=="plan_fact"`, keeping the distinct OBS signal as the `plan_fact_recorded`
  event — correct call (avoids a migration), and surfaced honestly (offline fakes accept any
  event_type; only the live path exercises the CHECK).

**EM-run verification (independent, 2026-06-18):**
- OFFLINE → **551 passed, 70 skipped, 0 failed** (Wave-C baseline 518 → +33). LIVE (Supabase up)
  → **621 passed, 0 failed** (baseline 587 → +34). Plan-fact + (G) suites: 27 passed. ruff clean
  · gate-4 PASS · gate-5 PASS.

## Approved by engineering manager

Status: Approved

Executive summary:
- DTM-0016 completes the confirm path (IC-WU-ACCEPT U1.2): on accept/direct-edit, OSLO records
  both the version-pinned `UserAcceptanceRecord` (unchanged Wave-A write) **and** a user-attested
  **plan fact** (`AttestedAssertion`, `attested-user`) holding the confirmed content — "factual
  in the plan, not world-truth"; reject/defer write only the UAR. The path emits
  `user_acceptance_record_appended` + `plan_fact_recorded`. The **user** authors the plan fact;
  OSLO never self-accepts and never promotes its own recommendation to Attested (negative-proven).

Verification:
- ruff clean · gate-4 PASS · gate-5 PASS · OFFLINE 551/70/0 · LIVE 621/0. Scope-checked: frozen
  modules untouched; no migration/package; plan fact only on accept/direct-edit.

Manual test plan:
- Live (Supabase up): accept a recommendation → a `user_acceptance_record` (version-pinned) **and**
  an `attested_assertion` plan fact (`attested-user`); reject → UAR only; both append-only
  (overwrite denied at the DB).

Remaining risks:
- `plan-fact-recorded` rides the `acceptance-recorded` history event_type (discriminated) until/if
  the owner widens the `history_record` CHECK — accepted, no migration.
- Branch still carries the inherited gate-3 fix gap (loose pydantic-ai pin) until synced with main.
