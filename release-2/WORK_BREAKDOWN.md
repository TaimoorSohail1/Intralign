# OSLO R2 — Work Breakdown

*The full scope of the R2 build, in dependency order. This is a **sequence, not a schedule** — build in roughly this order, but batch and iterate however your team works. Full ticket detail is in `BACKLOG.md`; the reasoning behind the ordering is in `BUILD_SEQUENCE.md`; the spec you build against is in `slices/`.*

**Two things hold no matter how you iterate within a stage:**
- **Only reanalysis resolves** — an act enqueues; a batched re-read is the *only* thing that moves a band, an issue, or integrity. (`GT-10`, pinned)
- **The pinned negatives stay red-if-violated forever** — the no-write projections (roll-up, grounding-map, generated reports, feedback/survey) and the never-metered exemptions (the record, reviewers, Viewers).

---

## Stage 0 — Make the prototype a faithful oracle

Before building against `oslo-prototype-r2.html`, correct the six places it deviates from canon. Small, self-contained, no backend. (`BACKLOG.md` epic `R2-PA`.)

- **R2-PA-1** — 5-step band scale (Fragile → Weak → Developing → Solid → Sound). *Owner input: confirm the three interior labels.*
- **R2-PA-2** — foundation-first tie-break (Viability → Grounding → Adaptability).
- **R2-PA-3** — Viability moves from real weakness reduction, not a fix count.
- **R2-PA-4** — bands normalize to plan size (placeholder cutpoints for now).
- **R2-PA-5** — build the real false-confidence issue layer (`ISS-FC-<art>`). *The big one — it's effectively the Slice 1 engine, prototyped.*
- **R2-PA-6** — activation = the 2nd grounding act (DR-6).
- **Done when:** `_S10` is 100% green headless with the new behavior, and the two honesty forks (`needsFixFork`, `mitigatedNeedsGrounding`) don't regress.

## Stage 1 — Foundation: integrity engine + reanalysis spine

Slice 1 (what a read *is*) and Slice 3 (the only thing that moves it), built together. Everything else renders on these. (`slices/01-integrity-engine.md`, `slices/03-reanalysis-freeze-unlock.md`.)

- **Integrity engine:** R2-S1-1 (the exposure-gated issue layer) → S1-2 / S1-3 / S1-4 (Viability, Grounding + false-confidence, Adaptability) → S1-5 (weakest-gates composite + pending marker) → S1-6 / S1-7 (size-normalization + care-point isolation).
- **Reanalysis + freeze:** R2-S3-1 (batched enqueue → resolve; the **`GT-10` spine**) · S3-4 (initial read emits all three pillars) · S3-3 (Fast/Deep two-pass, ≤60s P95) · S3-2 (STALE labeling) · S3-6 / S3-7 (freeze/unlock latch) · S3-5 (degrade-to-fit) · S3-8 (causal "your read moved").
- **Owner input before coding:** **O-3** (Fast-vs-Deep on the batch), **O-4** (`confirmCount` semantics). Band cutpoints (**O-1**) stay placeholder — calibrated later against real plans.

## Stage 2 — Issue lifecycle & grounding acts

Slice 2 — the acts (confirm / flag / fix / route / answer / withdraw), the attestation ledger, the two "acted-on-not-closed" forks. (`slices/02-issue-lifecycle-grounding-acts.md`.)

- R2-S2-1 lifecycle (only-reanalysis-resolves) · S2-2 ledger + BASIS enum · S2-3 flag fork · S2-4 mitigated fork · S2-5 fix ≠ grounding · S2-6 withdraw-appends-never-erases · S2-7 comment-never-grounds · S2-8 route-as-act.
- **Owner input:** **O-5** (reviewer-reject authority, `groundMitigated` ledger shape, withdraw→reanalysis, `answered`-basis rank).

## Stage 3 — Read surfaces (the funnel)

Slice 5 (read more than one outcome, hold the secondaries, disclose post-activation) with Slice 4 (the commitment gate that disclosure routes into). (`slices/05-multi-outcome-deferred-disclosure.md`, `slices/04-freemium-entitlement-commitment-gate.md`.)

- **Multi-outcome:** R2-S5-1…S5-7 (NLU + explainable ranking, held-pool, primary-only reveal, post-activation disclosure, primary-edit re-flag).
- **Freemium:** R2-S4-1…S4-9 (entitlement, ENFORCE commitment gate, outcome-as-metered-unit, reversible archive, never-metered exemptions, intent stream).
- **Owner input:** **O-7** (rationale-generation contract) before Slice 5; **O-6** (checkout provider) before Slice 4.

## Stage 4 — Collaboration & output

Slice 6 (scoped reviewer round-trip, roll-up, grounding map, share) and Slice 7 (reports & real export). (`slices/06-collaboration-reviewer-rollup-share.md`, `slices/07-reports-export-handoff.md`.)

- **Collaboration:** R2-S6-1…S6-7 (hard-enforced scoped reviewer / 403, round-trip, no-write projections, frozen view-only share, salience feed, k-factor invite).
- **Reports / export:** R2-S7-1…S7-9 (four reports, real export, reanalyze-if-pending, honest readiness signal, D153 disclaimer, PM-tool hand-off, scheduling).
- **Owner input:** **O-8** (scope-token shape) before Slice 6; **O-9** (first PM tool) before Slice 7.

## Stage 5 — Telemetry side channels

Slice 8 — feedback ticketing, the PMF survey + trigger/A-B, the funnel stream; structurally forbidden from touching the read. (`slices/08-feedback-survey-telemetry.md`.)

- R2-S8-1…S8-8 (isolated store with no write grant, ticketing, egress sanitization, funnel milestones off the `grounding_act` stream, survey trigger, non-surfaced readiness metric, sticky A/B, intent-only History exemption).
- **Owner input:** **O-10** (which feedback tracker) before build; readiness statistics stay placeholder.

## Throughout — the keystone (Slice 9)

Not an end-stage — it runs alongside everything. (`slices/09-doctrine-guardrails-integration-map.md`.)

- **From day one:** adopt the FE↔BE integration map as the build contract — a surface not in it isn't shippable.
- **As each stage lands:** port that stage's `_S10` guards to server-side twins; grow the `GT-01…GT-33` register.
- **Before ship:** the whole suite green, the pinned negatives wired red-if-violated. A red suite blocks the build.

---

## Owner-open decisions

All config/policy items are catalogued in `BACKLOG.md` → **Owner-Open Decisions (O-1…O-10)**. Timing: the structural / vendor picks (O-3, O-4, O-5, checkout O-6, rationale O-7, scope-token O-8, PM-tool O-9, tracker O-10) get ratified **before their stage**, because they steer the code. The empirical tuning numbers (band cutpoints, reanalysis windows, thresholds, prices, readiness statistics) get ratified **at a calibration pass, after the build produces data** — setting them earlier is just guessing you'll redo.
