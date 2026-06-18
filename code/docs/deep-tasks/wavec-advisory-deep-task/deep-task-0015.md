# DTM-0015 — Advise: Suggested Fix (REC-04) + Validation Recommendation (REC-05)

**Status:** Planned — BLOCKED on DTM-0014 approval · **Module:** DTM-0015 · **Phase:** IV
(Wave C) · **Contract:** **IC-WC-ADVISE — DL-047 Additions** (REC-04, REC-05) · **Depends:**
DTM-0014.

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

_(worker fills)_

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_
