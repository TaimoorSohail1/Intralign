# Deep-task decisions — Wave U: User Acceptance & Reconciliation (additive, non-governance)

Implementation-control record for Phase V / Wave U. Cites source-of-truth; does not restate it.
Two slices (DTM-0016, DTM-0017). **Branch:** `feat/phase5-waveu-user-acceptance` (do NOT create
another).

## Source-of-truth docs (binding; read, do not edit from deep-task)

- **Contract:** `20_handoff/contracts/WAVE_C_AND_U_CONTRACT_PACKAGES_ADVISORY_AND_ACCEPTANCE.md`
  — **Wave U section** U0–U3 (IC/QA/OBS-WU-ACCEPT: required behavior 1–4, the seven (G)
  forbidden invariants, QA U2 positive/negative, OBS U3 events/audit/replay). Contract WINS.
- **Plan:** `30_engineering/implementation/Phase_V_Wave_U_User_Acceptance/IMPLEMENTATION_PLAN.md`
  (Goal, Scope, DoD, Invariants, Exit gate).
- **ADR-0009** (`code/docs/adr/0009-wave-u-user-acceptance-build-plan.md`) — the locked build
  plan + the 17 locked decisions; **CONTEXT.md** Wave U glossary (UAR, Plan fact,
  Acceptance-Impact, never-self-accept).
- **DL-043 constituent G** + **Plan-Fact Clarification §0.1** (plan-fact ≠ world-truth;
  acceptance ≠ governance; Integrity-not-Authority); **DL-055** (recommendation states are the
  user's); **Calibration §3** (Acceptance-Impact drift = ≥10 pts or band change vs the pin);
  LDM §2.2/§2.4/§3.1; ADR-0004 (recorded-fixture CI); DTM-0013 CHR-model contract;
  ANTI_ASSUMPTION protocol.

## Repo facts (gap analysis — what exists vs what Wave U adds)

- **Exists (Wave A DTM-0007/0008):** `perceive/acceptance_capture.py` captures the action
  (accept/reject/defer/direct-edit) + emits `user_acceptance_captured` (WA001).
  `retain/acceptance.py::record_acceptance` INSERTS the **UserAcceptanceRecord** row
  (version-pin **mandatory** → `AcceptanceRecordingError`; `attested-user`; append-only;
  decoupled) + one `acceptance-recorded` history entry. **Takes no emitter; writes NO plan
  fact.**
- **Schema (no migration needed):** `attested_assertion` CHECK admits `attested-user`
  (migration `20260612090000` line 44) → a **plan fact** is a row in that table. The CHR
  `output_kind` Literal/CHECK already includes **`acceptance_impact`**. The
  `user_acceptance_record` table exists. `attested-user` epistemic state exists.
- **Persistence:** `services/persistence/retention_store.py` (`SupabaseRetentionStore`) has
  `insert_assertion` / `insert_acceptance` / `insert_history` (INSERT-only). `RetentionStore`
  protocol in `retain/admission.py`.
- **Types:** `shared/epistemic.py` lists `UserAcceptanceRecord`, `PlanFact`,
  `AcceptanceImpactAssessment` in `CANONICAL_OUTPUTS` but **PlanFact / AcceptanceImpactAssessment
  are not yet classes**.
- **Events:** `events.py` per-contract tuples + union; gate-5 asserts verbatim. The capture
  event `user_acceptance_captured` is in `EVENT_NAMES_WA001`.
- `responsibilities/acceptance/__init__.py` is a stub docstring — Wave U adds **no new
  responsibility**; work lands in perceive/retain/evaluate (distributed, per ADR-0009).

## Locked decisions (apply to both slices unless noted)

1. **One fresh worker per slice, sequential** (ADR-0009): DTM-0016 → DTM-0017. No slice starts
   until the prior is reviewed/fixed/verified/approved.
2. **No new responsibility, no Authority engine, no migration, no new package.** Distributed
   across existing modules.
3. **DTM-0016 — Plan-Fact:** extend the confirm path so that on **accept** and **direct-edit**
   (NOT reject/defer), in addition to the existing UAR, a **plan fact** is written — an
   `AttestedAssertion` in `attested_assertion` with `attesting_source=user`,
   `epistemic_state=attested-user`, the **confirmed content** (for accept: from the pinned
   CHR's payload; for direct-edit: from the capture's edit content). The **user** authors it;
   OSLO never auto-promotes its own Derived recommendation. Define the `PlanFact` type.
4. **DTM-0016 — events:** add an **emitter** to the acceptance path (additive — Wave A took
   none) and emit `user_acceptance_record_appended` + `plan_fact_recorded` (verbatim per
   OBS-WU C3; reuse `user_acceptance_captured` for capture). These are Attested writes →
   **record-exact** replay.
5. **DTM-0017 — Acceptance-Impact Assessment:** Evaluate-owned reconcile-on-drift. After a
   recompute produces new values, scan the project's **active version-pinned UARs**; for each,
   compare the **latest** value for the accepted item vs the **version-pinned** CHR's value; if
   drift **≥10 pts or a band change** (Calibration §3) → emit an `AcceptanceImpactAssessment`
   (Derived, CHR `output_kind=acceptance_impact`, appended via the **DTM-0013 model pattern**,
   superseding a prior assessment for the same UAR). Emit `acceptance_impact_assessed`. Define
   the `AcceptanceImpactAssessment` type. Determinism: **derivation semantic** (band-stable).
6. **DTM-0017 — wiring (least-invasive):** add `evaluate/acceptance_impact.py` (the pure
   compare) + run it in the recompute **after Evaluate**, via the **smallest additive change**
   (extend the evaluate stage, or an additive `orchestration/wave_u.py` that composes A→B→C
   +reconcile). **Do NOT edit** `deep_pass.py` topology, `state.py`, `runner.py`, `wave_b.py`.
   If wiring seems to require a frozen-core edit ⇒ **STOP and escalate.**
7. **The seven (G) invariants + never-self-accept (hard rule #5)** — negative-proven (QA U2):
   acceptance ≠ world-truth / ≠ OSLO-approved; UAR ≠ Governance Decision; record never
   overwritten; version-pin mandatory; OSLO never promotes its own recommendation to Attested;
   the impact comparison is **Derived**, never canonical.
8. **CHR-append (DTM-0013 model pattern)** for the Acceptance-Impact Assessment:
   `CognitionHistoryRecord(project_id=…, provenance_ref={"emitted_by":"evaluate"},
   recompute_trigger=…, supersedes_chr_id=…, **spec)` → `ctx.chr_repo.append` → emit
   `cognition_history_record_appended`. UAR + plan fact are canonical writes (not CHRs).
9. **Disclose surfacing is Wave E** — Wave U emits the alert *event*; the UI surface is Phase VI.
10. **Recorded-fixture CI unchanged** (ADR-0004): no test makes a network call. (Reconcile is
    a rule comparison; it needs no LLM. Plan-fact content from the pinned CHR is a data read.)

## Packages / refactors

- **No new package.** Additive extensions only: `retain/acceptance.py` (plan-fact write +
  emitter), `evaluate/` (reconcile). No rewrite of frozen modules; no orchestration-core edit.

## Open items / residuals (minor — none blocking)

- **GATE — Wave U coding is BLOCKED on:** the **Phase IV exit-gate** (PR #46 merge / DL-044
  sign-off) + per-wave authorization + readiness gate. **These files are planning only; no
  worker is spawned until the owner authorizes Wave U start.**
- Exact OBS-WU event snake_case — worker pins verbatim vs OBS-WU C3.
- Reconcile wiring (extend evaluate stage vs new `wave_u.py`) — least-invasive, no frozen-core
  edit (locked #6); worker picks within that bound.
- Plan-fact `content_type` for an accepted recommendation (`fact` vs a recommendation-derived
  type) — worker grounds in the LDM `content_type` set; default `fact`.
- This branch inherits the **gate-3 fix gap** (loose pydantic-ai pin) until synced with `main`;
  not a Wave U concern but will surface in CI until phase4/this branch rebases on merged main.

## Slice index

| Task | Scope | File |
|---|---|---|
| DTM-0016 | Plan-Fact recording (accept/direct-edit → user-attested AttestedAssertion + events) | `deep-task-0016.md` |
| DTM-0017 | Acceptance-Impact Assessment (reconcile-on-drift via the 00R recompute, Derived) | `deep-task-0017.md` |
