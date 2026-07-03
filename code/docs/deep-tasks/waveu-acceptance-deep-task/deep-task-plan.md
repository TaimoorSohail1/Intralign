# Deep-task plan — Wave U: User Acceptance & Reconciliation

Two vertical slices on `feat/phase5-waveu-user-acceptance`. One fresh worker per task, EM
review → fix → verify → approve between tasks. **Coding gated on the Phase IV exit-gate (PR #46)
+ DL-044 per-wave authorization** — these files are planning only.

## Slices

| # | Module | Slice (vertical outcome) | Contract | Depends on |
|---|---|---|---|---|
| 1 | DTM-0016 | **Plan-Fact recording:** on accept / direct-edit, write the user-attested **plan fact** (`AttestedAssertion`, `attested-user`) alongside the existing UAR; reject/defer write none; add the acceptance emitter → `user_acceptance_record_appended` + `plan_fact_recorded`; define `PlanFact`; never-self-accept + the (G) negatives | IC/QA/OBS-WU-ACCEPT (U1.2/U2/U3) | Wave A acceptance path; Phase IV (recs to accept) |
| 2 | DTM-0017 | **Acceptance-Impact Assessment:** Evaluate-owned reconcile-on-drift — after a recompute, scan active version-pinned UARs; drift ≥10pts/band vs the pin → emit a Derived `AcceptanceImpactAssessment` (CHR `acceptance_impact`, supersedes prior) + `acceptance_impact_assessed`; define the type; wired into the 00R recompute additively | IC/QA/OBS-WU-ACCEPT (U1.3) + Calibration §3 | DTM-0016 |

## Test strategy

- **QA-mapped (`test_u2_*` positive, `test_u2_neg_*`/`test_u3_*` negative):**
  - DTM-0016 positives: accept → UAR + plan fact (append-only, version-pinned, `attested-user`);
    direct-edit → plan fact even without a recommendation; reject/defer → UAR, **no** plan fact;
    events emitted.
  - DTM-0016 negatives (the (G) boundary): acceptance marking content **world-true / OSLO-approved**;
    UAR treated as a **Governance Decision**; acceptance/plan-fact **overwritten** (DB + surface);
    acceptance **not version-pinned**; **OSLO promoting its own recommendation to Attested**
    (user must author the plan fact); **OSLO self-accept** impossible.
  - DTM-0017 positives: drift ≥10pts/band vs the pin → one Acceptance-Impact Assessment (Derived,
    CHR appended); recompute supersedes a prior assessment; no-drift → no assessment.
  - DTM-0017 negatives: the impact comparison treated as **canonical** (it is Derived); an
    assessment that mutates the UAR/plan fact; drift below threshold raising an alert.
- **Determinism:** UAR + plan fact **record-exact** (Attested); Acceptance-Impact **semantic /
  band-stable** (it's a value comparison — rule-derived, so exact for the comparison, semantic
  for any AI-derived input value it reads).
- **Recorded-fixture CI (ADR-0004):** zero provider calls; reconcile is a rule comparison.
- ruff + gate-4 + gate-5 green; the live A→B→C→(accept→impact) path passes (env-gated e2e);
  baseline (offline 518 / live 587 at the Wave-C head) must not regress.

## Manual checks (EM / owner)

- Live (Supabase up): accept a recommendation → `user_acceptance_record` row (version-pinned)
  **and** an `attested_assertion` plan fact (`attested-user`); mutate the underlying knowledge →
  recompute → an `acceptance_impact` CHR appears for the accepted item; prior records byte-intact.
- AST/grep: no path marks an item true/approved; OSLO never writes a plan fact without a user
  action; the impact assessment never writes canonical-as-truth.

## Done = Wave U complete

U2 positive/negative sets covered; plan fact written on accept/direct-edit (not reject/defer),
version-pinned + append-only; Acceptance-Impact drift surfaces at ≥10pts/band; the
non-governance / never-self-accept boundary proven by negatives; events + replay present.
**Phase V candidate-complete for owner exit-gate review before Phase VI (Wave E / Disclose).**
