# DTM-0016 — Plan-Fact recording: accept/direct-edit → user-attested AttestedAssertion

**Status:** Planned — BLOCKED on Phase IV exit-gate (PR #46) + DL-044 authorization · **Module:**
DTM-0016 · **Phase:** V (Wave U) · **Contract:** **IC/QA/OBS-WU-ACCEPT** (U1.2, U2, U3) ·
**Depends:** Wave A acceptance path (capture + UAR), Phase IV (recommendations to accept).

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

_(worker fills)_

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_
