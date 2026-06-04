# Wave A Contract Package 00R — Recompute & Stale Backbone

**Document Type:** Release 1 Contract Package (architecture-level, environment-independent) · **Status:** **DL-043-conformed (2026-06-04) — Ready for Review** · **Date:** 2026-06-04
**Contract Set:** IC-WA-00R / QA-WA-00R / OBS-WA-00R · **Owning Responsibility:** **Act / Adapt** *(Adapt is emergent loop behavior; trigger detection is Perceive/Act)*
**Consumes (authoritative):** Cognitive Responsibility Architecture Specification · Runtime Object Model · Runtime Behavior Model · Contract Inventory · QA Governance · Observability Governance · **DL-043** (Derived Cognition Lifecycle · Epistemic State Model). *(Environment binding deferred.)*

> **Mode:** the runtime backbone every later wave depends on — *when* understanding recomputes and *how* history accrues. No new responsibility (Adapt is emergent, not a responsibility). **Per `CLAUDE.md`, owner ratifies.**

---

## 0. Package Orientation

**What this package owns.** The **recompute backbone**: stale detection, recompute triggering, state transitions, and the rule that **every cognition emission appends a Cognition History Record (never overwrites)**. It does **not** itself reason, evaluate, advise, or store canonical knowledge — it **orchestrates re-running** the cognition chain and **enforces the append-only emission discipline**.

**Core principle.** **Only recompute changes assessment.** Evidence change, knowledge mutation, or a user action that changes information triggers `Retain → Infer → Evaluate → Advise`; nothing else alters a Finding/Issue/Confidence/Recommendation. **Adapt is emergent** — a property of the loop, owned by no single responsibility; **trigger detection** belongs to Perceive (change/stale) and Act (coordination).

**Primary objects (Object Model):** Recompute Event · State Transition Event · Stale signal *(Cognition History Record is Retain's object; this package governs the append-on-recompute discipline that produces them)*.

---

## 1. Implementation Contract — IC-WA-00R

### A1. Identity
- **Contract:** IC-WA-00R — Recompute & Stale Backbone.
- **Owner:** Act/Adapt (emergent loop). Trigger detection: Perceive (stale/change) + Act (orchestration).
- **Objects:** Recompute Event, State Transition Event, stale signal.

### A2. Purpose
Define *what triggers recompute, what recompute does to live cognition and to history, and what state transitions are valid* — preserving only-recompute-changes-assessment and append-only emission history.

### A3. Required Behavior
1. **Detect staleness** when canonical (Attested) knowledge changes or evidence/inputs change since the last analysis.
2. **Trigger recompute** on a valid trigger: **promotion** of new Attested knowledge, **knowledge-changing modification**, **clarification answered**, **information-changing user action**, or **explicit/auto reanalysis**.
3. **Re-run the cognition chain** `Retain → Infer → Evaluate → Advise` (and, where applicable, the **Acceptance-Impact Assessment**, Wave U).
4. **Replace the live Derived projection** with the recomputed result (live cognition is recomputable, non-canonical).
5. **Append a Cognition History Record** for each emission produced by the recompute — **append-only, never overwrite** a prior record. (Records are Retain-owned Attested facts; this package enforces the append discipline.)
6. **Record state transitions** (analyzing / current / stale / reanalyzing / failed) as events.
7. **On failure, retain last-known-good** live cognition and emit a recompute-failed event; do not corrupt history.

### A4. Forbidden Behavior
1. **Change any assessment without recompute** (only recompute changes assessment).
2. **Overwrite or delete** a Cognition History Record (append-only).
3. **Reason/evaluate/advise** itself — it orchestrates the owners, it is not a cognition producer.
4. **Mutate canonical (Attested) knowledge** — recompute reads Attested, produces Derived.
5. **Promote Derived to Attested** (one-way flow).
6. **Treat intake/acceptance-capture alone** as an assessment change (they are info-change; recompute is the only assessment-changing event).

### A6. Emitted Events
- **Stale Detected** · **Reanalysis Triggered** · **Recompute Started** · **Cognition History Record Appended** (per emission) · **Recompute Completed** · **Recompute Failed (last-known-good retained)** · **State Transition Occurred**.

### A7. States
`Current → (input/knowledge change) → Stale → Reanalyzing → Current' (live replaced; history appended)` · failure branch: `Reanalyzing → Failed (last-known-good retained)`. All transitions emit events; history is append-only.

### A9. Recompute Relationship (the spine)
This **is** the recompute mechanism. Valid triggers (A3.2) → chain re-run → live replaced + **history appended**. Two-axis replay (per Lifecycle decision): the **emission record** is record-exact; the **derivation** is exact-if-rule / semantic-if-AI. **Outcome Drift** surfaced across the Cognition History stream is a **product feature** (surfaced, never failed).

### A10. Bound Invariants
Only-recompute-changes-assessment · recompute appends history (never overwrites) · Adapt is emergent (no new responsibility) · live cognition is non-canonical/recomputable · one-way flow (Derived↛Attested) · last-known-good retained on failure.

---

## 2. QA Contract — QA-WA-00R

### B2. Positive Validation
1. A valid trigger initiates recompute; the chain re-runs; live projection is replaced.
2. **Each emission appends a new Cognition History Record**; prior records intact.
3. State transitions emitted (stale/reanalyzing/current/failed).
4. On failure, last-known-good retained; history uncorrupted.
5. Stale detected on Attested-knowledge/evidence change.

### B3. Negative Validation (must be impossible/rejected)
1. An assessment value changes **without** a recompute.
2. A Cognition History Record **overwritten or deleted**.
3. Intake or acceptance-capture **alone** changing an assessment.
4. The backbone **producing cognition** itself (reasoning/evaluating/advising).
5. Canonical (Attested) knowledge **mutated** by recompute; or Derived **promoted** to Attested.

### B4. Failure Classification
- **Critical:** assessment-without-recompute; history overwrite/deletion; Derived→Attested promotion; canonical mutation by recompute.
- **Major:** missing history append on an emission; stale not detected; failure not retaining last-known-good.
- **Minor:** state-event metadata gaps.

### B5. Regression Anchors
only-recompute-changes-assessment; append-only emission; last-known-good-on-failure; one-way flow; Adapt emergent.

---

## 3. Observability Contract — OBS-WA-00R

### C2. Observable Events
Stale detected; reanalysis triggered; recompute started/completed/failed; **cognition-history-record appended**; state transitions.

### C3. Audit
Per recompute: trigger source, inputs/versions consumed (Attested-knowledge + model/rule version), emissions produced (→ which history records appended), and outcome (completed/failed). The **append-not-overwrite** property is auditable.

### C5. Replay
- **Record-exact** replay of each appended Cognition History Record (Attested).
- **Trigger/lineage replay** — reconstruct what triggered a recompute and which emissions it appended.
- **Drift monitoring** — Outcome Drift across the history stream is surfaced (product feature), distinct from determinism-drift trust failures.

### C6. Drift / Trust Signals
Trust failures: assessment changed without an observed recompute; a history record overwritten; recompute mutating canonical; missing last-known-good on failure. (Determinism drift / confidence inflation are trust failures; **Outcome Drift is a feature**.)

### C7. Severity
Map to Observability Governance Critical (assessment-without-recompute, history overwrite, canonical mutation) / Major / Minor.

---

## 4. Readiness Assessment
Architecture ✅ (emergent Adapt; trigger Perceive/Act) · Ownership ✅ (no new responsibility) · Object ✅ (Recompute/State events; Cognition History Record discipline) · Behavior ✅ (triggers/append/states) · QA ✅ (positive+negative) · Observability ✅ (record-exact + drift) · Environment binding **Deferred (correct)**.

## 5. Conformance Validation
**§E** all behavior traces to Behavior Model (recompute/stale/state) + Lifecycle decision (append-on-recompute). ✅ **§H** QA positives↔IC required, negatives↔IC forbidden, IC events ⊆ OBS, invariants bound/validated/observed. ✅ **§K** no orphan behavior; no new responsibility (Adapt emergent); no invented concepts; no Authority; no environment binding. ✅

## 6. Final Contract Verdict
**READY FOR REVIEW — DL-043-conformed.** The recompute/stale backbone preserves *only recompute changes assessment*, enforces **append-only Cognition History** (recompute appends, never overwrites), retains last-known-good on failure, and treats Outcome Drift as a product feature — with no new responsibility (Adapt emergent) and no Authority. It completes the Wave A foundation alongside Package 001 (Perceive) and Package 002 (Retain).

> ### Proposed Owner Resolution
> Approve the Recompute & Stale Backbone package as the third Wave A foundation set (with 001 and 002), completing Wave A under DL-043. Proceed to Wave B (Infer + Evaluate).

---

*This package defines the Release 1 recompute and stale-detection backbone (IC/QA/OBS-WA-00R) under the emergent Adapt behavior with trigger detection by Perceive/Act, establishing the valid recompute triggers, the re-run of the Retain→Infer→Evaluate→Advise chain, replacement of the live Derived projection, and — per the ratified Derived Cognition Lifecycle — the append-only emission of Cognition History Records on every recompute (never overwriting), with last-known-good retention on failure. It preserves the invariants that only recompute changes assessment, that history is append-only, that Adapt is emergent (no new responsibility), that live cognition is non-canonical and recomputable, and that Derived is never promoted to Attested; includes mandatory positive-and-negative QA with severity classification and record-exact observability with Outcome-Drift-as-feature monitoring; self-validates against Framework §E/§H/§K; introduces no Authority, new responsibility, or environment binding; and completes the Wave A foundation for owner review.*

**Wave A Contract Package 00R — Recompute & Stale Backbone complete.**
