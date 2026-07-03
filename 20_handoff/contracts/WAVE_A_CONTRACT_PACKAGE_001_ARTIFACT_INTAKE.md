# Wave A Contract Package 001 — Artifact Intake

**Document Type:** Release 1 Contract Package (architecture-level, environment-independent) · **Status:** **DL-043-conformed re-issue (2026-06-04) — Ready for Re-Review** · **Date:** 2026-06-04
**Contract Set:** IC-WA-001 / QA-WA-001 / OBS-WA-001 · **Owning Responsibility:** **Perceive**
**Consumes (authoritative):** Cognitive Responsibility Architecture Specification · Runtime Object Model · Runtime Behavior Model · Contract Inventory · QA Governance · Observability Governance · **DL-043** (Epistemic State Model · Integrity-not-Authority · User Acceptance Recording). *(Environment binding deferred to the forthcoming Runtime Environment Constraint Profile.)*

> **Mode:** DL-043-conformed re-issue of the original Artifact Intake package. The original routed promotion through **Authority authorization**; under DL-043 **the Authority plane is inactive in Release 1** and admission is **integrity-gated**. No architecture redesign; no new responsibilities. **Per `CLAUDE.md`, only the repository owner ratifies.**

---

## DL-047 Additions (authoritative — ratified 2026-06-04)

**Claim Extraction (EI-02) — Perceive behavior.** Perceive's "no cognition" means **no Derived cognition (no Findings/assessments)** — Perceive **does perform source-attributed extraction**: it interprets admitted evidence into **evidence-attested `AttestedAssertion`s** (Canonical Fact / Assumption / Constraint / Dependency, each attributed to its source + re-derivable) and hands them to Retain. **Required:** every extracted assertion carries source attribution + re-derivability; **Forbidden:** inferring Findings/severity/confidence (that is Infer/Evaluate); promoting non-attributable content to Attested. **QA:** positive — extraction produces source-attributed assertions of the correct type; negative — Perceive emitting a Finding/assessment, or an unattributed "fact." **OBS:** `Claim Extracted` event + provenance.

**CRR response intake (CRR-04) — Perceive seam.** A submitted **StakeholderResponse** (from a CAF Review Request) is admitted as **new evidence** (evidence-attested) and triggers the Deep Pass recompute (00R). Perceive captures it; it is not a Governance Decision. **Negative:** a stakeholder response treated as world-truth or as OSLO self-acceptance.

---

## 0. Package Orientation

> **DL-046 note.** Intake feeds the **Fast Pass** orientation; integrity-gated admission must **not block** the **Time-to-First-MRI < 60 s** budget.

**What this package owns.** **Perceive** — the always-on origin of the loop: it ingests raw artifacts and user actions, normalizes them, checks **promotion-readiness + integrity**, and produces **Promotion Candidates** that Retain admits as **Attested** knowledge. Perceive is the only responsibility that **captures user input** — including **user-acceptance actions** (the Wave U input).

**What this package is not.** Perceive does **not** infer, evaluate, advise, disclose, govern, or accept. It does **not** decide what is true; it records *what was submitted, by whom, when*. It performs **no Authority/governance** step (none exists in R1).

**Position in the chain.** `User/source → Perceive (intake, normalize, readiness, integrity) → Promotion Candidate → Retain (Attested admission)`. Separately: `User acceptance action → Perceive (capture) → Retain (User Acceptance Record)`. Intake alone is **not** an assessment change — *only recompute changes assessment.*

**Primary objects (Runtime Object Model):** Intake Submission (transient) · Artifact (raw) · Promotion Candidate (transient, pre-admission) · Context Signal (event). *(Perceive also **captures** the user-acceptance action that Retain records as a User Acceptance Record — the record object is Retain's.)*

---

## 1. Implementation Contract — IC-WA-001

### A1. Identity
- **Contract:** IC-WA-001 — Artifact Intake (Perceive).
- **Owning Responsibility:** Perceive (single owner).
- **Objects:** Intake Submission, Artifact (raw), Promotion Candidate, Context Signal.
- **Downstream:** Promotion Candidate → Retain (Package 002, integrity-gated admission). Captured acceptance action → Retain (User Acceptance Record).

### A2. Purpose
Define required/forbidden behavior for ingesting artifacts and user actions, normalizing them, establishing **promotion-readiness + integrity**, producing Promotion Candidates, and emitting intake events — **without** inferring, evaluating, advising, governing, or changing assessment.

### A3. Required Behavior
Perceive **must**:
1. **Accept and preserve** submitted artifacts with **source attribution and provenance** (who/when/from-where), append-only.
2. **Normalize** to a consistent internal form without altering meaning.
3. **Establish promotion-readiness + integrity:** attribution present, idempotent (same submission not double-admitted), evidence-chain intact, re-derivability preserved. *(This is the R1 admission gate — integrity, not Authority.)*
4. **Produce a Promotion Candidate** for ready, integrity-cleared content, carrying its attribution for downstream **Attested** admission.
5. **Capture user actions**, including **user-acceptance actions** (item accepted + the **specific emission/version** accepted), and route them to Retain for **User Acceptance Record** creation. *(Capture only — Perceive does not interpret or accept.)*
6. **Emit intake events** (A6).
7. **Detect change / staleness** on re-submission/edit and signal it (does not itself recompute).
8. **Preserve idempotency & ordering** so re-intake is safe and time-attributed.

### A4. Forbidden Behavior
Perceive **must not**:
1. **Treat uploaded content as canonical/true** — upload ≠ Attested; admission is Retain's integrity-gated step.
2. **Infer, evaluate, advise, or generate** Findings/Issues/Confidence/Recommendations/Clarifications.
3. **Govern or authorize** — no Authority/exposure/disposition decisions (none in R1).
4. **Accept an interpretation** or mark any item true/approved/organizational-truth — it only *captures* the user's acceptance action.
5. **Change assessment** — intake alone never alters any cognitive output (only recompute does).
6. **Drop provenance/attribution** or admit content non-idempotently.
7. **Promote inferred content as Attested** — Perceive carries only attributed, re-derivable content forward.

### A5. Inputs
- Submitted artifacts / content (user or source).
- User actions, including acceptance actions (with the accepted item + version reference).
- External context signals.

### A6. Outputs / Emitted Events
- **Artifact Received / Normalizing / Normalized**
- **Promotion Candidate Ready** (integrity-cleared) / **Promotion-Readiness Failed**
- **User Acceptance Captured** (→ Retain creates the User Acceptance Record)
- **Context Signal Received**
- **Artifact Modified / Stale Detected** (change signal)

*(No "routed to Authority / authorization" event — removed per DL-043.)*

### A7. States
`Received → Normalizing → (Promotion-Readiness + Integrity Check) → Promotion Candidate Ready → [admitted by Retain] / Readiness-Failed / Re-submitted (stale)`. All append-only; provenance preserved at every transition.

### A8. Admission Relationship (integrity, not Authority)
Perceive establishes **promotion-readiness + integrity**; **Retain admits** the Attested result (Package 002). There is **no Authority authorization** between them in R1. The boundary is one-directional: Perceive prepares + attests-the-source; Retain canonicalizes (Attested).

### A9. Recompute Relationship
Intake alone is **not** an assessment change. A **promotion** (new attested knowledge) or a **knowledge-changing modification** triggers `Retain → Infer → Evaluate → Advise`. A **user-acceptance capture** is **info-change only** (no recompute by itself) but is later consumed by the **Acceptance-Impact Assessment** (Wave U). Invariant: *only recompute changes assessment.*

### A10. Bound Invariants
Upload ≠ canonical/true · admission is integrity-gated (no Authority in R1) · provenance/attribution always preserved · idempotent, ordered intake · Perceive does not reason/evaluate/advise/govern/accept · intake alone changes no assessment · only attributed/re-derivable content is carried forward (no inferred-as-Attested).

---

## 2. QA Contract — QA-WA-001

**Mandate (QA Governance):** positive **and** negative validation; failure classification by severity.

### B2. Positive Validation
1. Artifact accepted with full provenance/attribution; append-only.
2. Normalization preserves meaning.
3. Promotion-readiness + integrity check passes → Promotion Candidate produced (attributed).
4. Idempotent re-intake (no double-admission); ordering/time attribution preserved.
5. **User-acceptance action captured** with the accepted item + version, routed to Retain.
6. Change/stale detection signals on edit/re-submission.

### B3. Negative Validation (each must be impossible/rejected)
1. Uploaded content treated as canonical/true/Attested without Retain admission.
2. Perceive generating any Finding/Issue/Confidence/Recommendation/Clarification.
3. **Any Authority/governance/authorization step** (none exists in R1).
4. Perceive **accepting** an interpretation or marking it true/approved.
5. Assessment changed by intake alone (no recompute).
6. Provenance/attribution dropped; non-idempotent admission.
7. Inferred content carried forward as Attested.

### B4. Failure Classification
- **Critical:** content canonical-as-true without integrity admission; provenance/attribution loss; Perceive generating cognition; any Authority step; acceptance-as-truth; assessment-from-intake.
- **Major:** non-idempotent intake; missing readiness/integrity check; stale not detected; acceptance captured without version reference.
- **Minor:** incomplete optional metadata; normalization-label gaps.

### B5. Regression Anchors
Upload≠canonical; integrity-gated (no Authority); provenance preserved; idempotent intake; no-cognition-in-Perceive; only-recompute-changes-assessment; acceptance is captured-not-accepted.

---

## 3. Observability Contract — OBS-WA-001

### C1. Tiering
Intake observability is **audit/provenance** — **not cognitive replay**. Intake records (artifact, candidate, acceptance-capture) are **record-exact** replayable (Attested facts reproduced verbatim).

### C2. Observable Events
Artifact received/normalizing/normalized; promotion-candidate ready/failed; user-acceptance captured; context signal; artifact modified/stale.

### C3. Audit
Capture per event: **who/when/source** (attribution), **provenance/lineage**, **integrity-clearance reference** (readiness + idempotency + evidence-chain), and — for acceptance capture — the **accepted item + version reference**. *(No authorization-decision reference — removed in R1.)*

### C4. Trace
`Submission → Normalize → Integrity Clearance → Promotion Candidate → [Retain admission]`. Acceptance: `User action → Acceptance Captured → [Retain: User Acceptance Record]`.

### C5. Replay
- **Provenance replay** — reconstruct origin/lineage of any intake.
- **Integrity-clearance verification** — confirm each candidate passed readiness/idempotency/evidence-chain.
- **Record-exact replay** — for acceptance-capture events.
- **Not cognitive replay** — nothing reasoned here.

### C6. Drift / Trust Signals
Trust failures: uploaded content treated as canonical without integrity clearance; missing provenance; non-idempotent admission; any Authority/governance step appearing in R1; acceptance captured as truth; assessment changed by intake. Each is an integrity/trust failure (not product Outcome Drift).

### C7. Severity
Map to Observability Governance Critical (integrity bypass, provenance loss, cognition-in-intake, acceptance-as-truth) / Major / Minor, consistent with QA-WA-001 §B4.

---

## 4. Readiness Assessment

| Dimension | Claim | Basis |
|---|---|---|
| Architecture | Ready | Owner = Perceive; consistent with Cognitive Responsibility Architecture |
| Ownership | Ready (Perceive) | Single owner; integrity-gated handoff to Retain; no Authority |
| Object | Ready | Intake Submission, Artifact, Promotion Candidate, Context Signal (Object Model) |
| Behavior | Ready | Intake/normalize/readiness/candidate/stale + acceptance-capture events |
| QA | Ready | Positive + negative; failure classification |
| Observability | Ready | Audit/provenance + integrity-clearance; record-exact for acceptance capture |
| Environment binding | Deferred (correct) | Runtime Environment Constraint Profile (forthcoming) |

## 5. Conformance Validation (self-check)
**§E traceability:** objects/events/owner all trace to Object Model, Behavior Model, Inventory (DL-043-updated). ✅ **§H triad consistency:** QA positives↔IC required, negatives↔IC forbidden, IC events ⊆ OBS observed, invariants bound/validated/observed. ✅ **§K pre-use:** no orphan behavior; single owner (Perceive); no invented concepts; **no Authority in R1**; no environment binding; no implementation. ✅ **Cross-package:** hands off to Package 002 via **integrity-gated** admission (consistent — no Authority gate on either side). ✅

## 6. Final Contract Verdict

**READY FOR RE-REVIEW — DL-043-conformed.** Artifact Intake (IC/QA/OBS-WA-001) for **Perceive** is re-issued with the Authority authorization step removed (Authority inactive in R1) and admission **integrity-gated**; it adds **user-acceptance capture** as a Perceive input to the Wave U capability, preserves upload≠canonical, provenance, idempotency, no-cognition-in-Perceive, and only-recompute-changes-assessment. No new responsibility/object; environment binding deferred.

> ### Proposed Owner Resolution
> Approve the DL-043-conformed re-issue of Package 001 as the canonical Artifact Intake contract (superseding the original Authority-gated version); record that the prior 001 conformance review's Authority clauses are moot under DL-043. Proceed to the recompute/stale backbone package, then Wave B.

---

*This DL-043-conformed re-issue of Wave A Contract Package 001 defines the Artifact Intake contracts (IC/QA/OBS-WA-001) for Perceive with admission integrity-gated rather than Authority-authorized (Authority plane inactive in Release 1), adds user-acceptance-action capture as a Perceive input feeding Retain's User Acceptance Record, and preserves the invariants that uploaded content is not canonical/true until integrity-admitted by Retain, that Perceive performs no inference/evaluation/advice/governance/acceptance, that provenance and idempotency are always preserved, and that intake alone changes no assessment. It includes mandatory positive-and-negative QA validation with severity classification, audit/provenance observability with record-exact replay for acceptance-capture events and explicit non-cognitive tiering, self-validates against Contract Generation Framework §E/§H/§K, introduces no new responsibility/object or implementation/environment binding, and is routed to the owner for re-review.*

**Wave A Contract Package 001 — Artifact Intake (DL-043-conformed re-issue) complete.**
