# Wave U (User Acceptance) is distributed across existing modules, two slices; OSLO never self-accepts

Phase V / Wave U contracts `IC/QA/OBS-WU-ACCEPT`: the **user** accepts a recommendation and
that acceptance is recorded as a **user-attested plan fact**; later, if the understanding
behind an accepted item drifts, an **Acceptance-Impact Assessment** surfaces. Per DL-043
("Integrity, not Authority") this is **attestation + Derived cognition, not a governance
engine** — **no new responsibility, no Authority**. Owners are existing modules: Perceive
(capture) · Retain (record) · Infer/Evaluate (reconcile) · Disclose (surface, Wave E). This
ADR records how it lands in `code/`; the contract + DL-043 (constituent G) + DL-055 govern.

**What already exists (Wave A):** `perceive/acceptance_capture.py` captures the action;
`retain/acceptance.py::record_acceptance` writes the **UserAcceptanceRecord** (version-pinned,
mandatory, `attested-user`, append-only, decoupled). The `user_acceptance_record` table, the
`attested-user` epistemic state (admitted by the `attested_assertion` CHECK), and the CHR
`acceptance_impact` output_kind all already exist → **no migration**.

**What Wave U adds, in two slices:**
- **DTM-0016 — Plan-Fact recording.** Complete the confirm path: on **accept** (and
  **direct-edit**), in addition to the UAR, write the **user-attested plan fact** — an
  `AttestedAssertion` in `attested_assertion` with `attesting_source=user`,
  `epistemic_state=attested-user` ("factual in the plan, not world-truth"). **reject/defer
  write no plan fact.** Define the `PlanFact` type; emit `plan_fact_recorded` +
  `user_acceptance_record_appended`.
- **DTM-0017 — Acceptance-Impact Assessment.** Reconcile-on-drift (Infer/Evaluate): compare the
  current value (latest CHR) for an accepted item against its **version-pinned** acceptance; if
  drift **≥10 pts or a band change** (Calibration §3) → emit an `AcceptanceImpactAssessment`
  (Derived, CHR `output_kind=acceptance_impact`, appended via the DTM-0013 model pattern,
  superseding on re-assessment). Wired into the 00R recompute backbone (a recompute scans the
  project's active UARs for drift). Define `AcceptanceImpactAssessment`; emit
  `acceptance_impact_assessed`.

## Status

accepted — locked from docs (Phase V plan + Wave U contract U0–U3 + DL-043 G + DL-055 +
Calibration §3), 2026-06-18. **Coding gated on the Phase IV exit-gate (PR #46) + DL-044 per-wave
authorization + readiness gate.**

## Considered Options

- **A new `acceptance` responsibility/Authority engine** — rejected: the stub
  `responsibilities/acceptance/` exists only as a docstring marker; the contract + DL-043
  mandate acceptance be **distributed** across existing responsibilities with **no Authority**.
  Acceptance stays attestation, not governance.
- **One slice** — rejected: bundles the canonical plan-fact write with the Derived
  drift-reconcile (two distinct concerns + their negatives).
- **Two slices, distributed (chosen)** — clean separation: the append-only attestation
  (DTM-0016) then the Derived reconciliation (DTM-0017); matches the Wave B/C discipline.

## Consequences

- **No migration, no new package:** plan fact rides the existing `attested_assertion`
  (`attested-user`); Acceptance-Impact rides the existing CHR `acceptance_impact` kind.
- **Extends the Wave-A acceptance path:** `retain/acceptance.py` (approved in DTM-0008) gains an
  additive plan-fact write — the Wave-A contract covered acceptance *capture* + UAR; the *plan
  fact* + *reconciliation* are explicitly Wave U (IC-WU-ACCEPT). Not a rewrite.
- **OSLO never self-accepts** (hard rule #5): the user is the acceptance authority; OSLO never
  auto-promotes its own Derived recommendation to Attested — the **user** authors the plan
  fact. Negative-proven, alongside: acceptance ≠ world-truth, UAR ≠ Governance Decision, record
  never overwritten, version-pin mandatory, impact comparison is **Derived** not canonical.
- **Reconcile placement:** the drift comparison is owned by **Evaluate** (it owns the
  value/band semantics); Infer is not re-run for it. The reconcile runs as a step in the 00R
  recompute after Evaluate, scanning the project's version-pinned UARs.
- **Disclose surfacing is Wave E** — Wave U emits the Acceptance-Impact *alert event*; the UI
  surface lands in Phase VI.
- Detailed slice scope/tests live in `code/docs/deep-tasks/waveu-acceptance-deep-task/` (authored
  at build time).
