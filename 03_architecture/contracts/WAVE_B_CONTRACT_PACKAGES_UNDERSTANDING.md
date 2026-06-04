# Wave B Contract Packages — Understanding (Infer + Evaluate)

**Document Type:** Release 1 Contract Packages (architecture-level, environment-independent) · **Status:** **DL-043-conformed (2026-06-04) — Ready for Review** · **Date:** 2026-06-04
**Contract Sets:** IC/QA/OBS-WB-INFER · IC/QA/OBS-WB-EVAL · **Owning Responsibilities:** **Infer** (Finding) · **Evaluate** (Issue · Confidence · Reliability · CAF · Outcome Confidence)
**Consumes (authoritative):** Cognitive Responsibility Architecture · Runtime Object Model (DL-043) · Runtime Behavior Model (DL-043) · Contract Inventory · QA Governance · Observability Governance · Wave A (001 Perceive · 002 Retain · 00R Recompute backbone) · **DL-043** (Epistemic State Model · Derived Cognition Lifecycle). *(Environment binding deferred.)*

> **Mode:** the first cognition layer. **All Wave B output is Derived Cognition** — non-canonical, recomputable; each emission **appends a Cognition History Record** via the Wave A 00R backbone; **two-axis replay** applies (record-exact / derivation-by-determinism). No new responsibility; **no Authority** (inactive in R1). **Per `CLAUDE.md`, owner ratifies.**

---

## 0. Shared Orientation (applies to both packages)

**Position in the chain.** `Retain (Attested) → Infer (Findings) → Evaluate (Issues/Confidence/CAF/Outcome Confidence) → [Advise, Wave C]`. Infer reads canonical (Attested) knowledge; Evaluate reads Infer's Findings. **Both read Attested, produce Derived** — they never write canonical knowledge and never promote Derived to Attested (one-way flow).

**Shared invariants (every capability below):**
- **Derived, non-canonical, recomputable.** The live output is a projection; only the **Cognition History Record** of each emission is canonical (Attested, OSLO-self-attested, append-only).
- **Only recompute changes assessment.** A Finding/Issue/Confidence value changes only via the 00R recompute backbone; recompute **appends** history, never overwrites.
- **Two-axis replay.** Record-exact for every emission; derivation exact-if-rule / semantic-if-AI (band-stable for confidence).
- **Surfacing, not resolving.** Conflicts/ambiguity are surfaced (Infer conflict + Evaluate low confidence), never collapsed into canonical truth.
- **No governance, no acceptance.** No exposure/suppression/authorization (Authority inactive); no interpretation acceptance (deferred to user).

**Shared classification corrections (Object Model §8):** Gap/Conflict/Risk are **Finding types**; Severity/Confidence/Reliability are **attributes** (of Issue/assessment), not standalone Core objects; Resolution Paths are presentation-only (AMB-1, Wave E).

---

## 1. Package WB-INFER — Finding (Infer)

### 1.1 Implementation Contract — IC-WB-INFER
- **Owner:** Infer (single). **Object:** Finding (types: Gap, Conflict, Risk Signal). **Reads:** Attested knowledge (Retain) + the declared-outcome reference (Canonical Fact, R1 Intend-provisional). **Produces:** Findings (Derived). **Consumed by:** Evaluate, Disclose.
- **Required behavior:** (1) derive **structural implications** — gaps (alignment/coverage/quality/SMART), conflicts (contradictions among Attested assertions), risks (feasibility); (2) **anchor each Finding to its Attested evidence** (traceable to the assertions it derives from); (3) emit **Finding Detected / Finding Superseded** and **append a Cognition History Record** per emission (via 00R); (4) on recompute, **re-derive and supersede** prior Findings (live replaced; history appended).
- **Forbidden:** compute severity/confidence (Evaluate's); generate recommendations/clarifications (Advise's); write canonical knowledge or promote a Finding to Attested; govern exposure; resolve a conflict into canonical truth (surface only); change assessment outside recompute.
- **States:** `Derived (this pass) → Superseded (re-derivation)`; never deleted (history append-only).
- **Invariants:** Derived/non-canonical; anchored to Attested evidence; conflicts surfaced not resolved; only-recompute-changes-assessment; emission appends history.

### 1.2 QA Contract — QA-WB-INFER
- **Positive:** Findings derived from Attested knowledge with evidence anchors; Gap/Conflict/Risk typed correctly; emission appends a Cognition History Record; recompute supersedes prior Finding (prior record intact).
- **Negative (impossible/rejected):** Infer computing severity/confidence; generating recommendations/clarifications; writing canonical/promoting to Attested; resolving a conflict into canonical truth; a Finding changing without recompute; a history record overwritten.
- **Failure classification:** Critical — Infer writing canonical / promoting Derived→Attested / changing assessment without recompute / history overwrite; Major — missing evidence anchor; wrong Finding type; emission without history append; Minor — metadata gaps.

### 1.3 Observability Contract — OBS-WB-INFER
- **Events:** Finding Detected/Superseded; Cognition History Record appended. **Audit:** which Attested assertions a Finding derived from; model/rule version; recompute lineage. **Replay:** record-exact for each Finding emission; derivation **semantic** (exact for rule-structural gaps). **Drift/Trust:** Finding changed without recompute, missing evidence anchor, history overwrite = trust failures; **Outcome Drift** in Findings across history = product feature.

---

## 2. Package WB-EVAL — Issue · Confidence · Reliability · CAF · Outcome Confidence (Evaluate)

### 2.1 Implementation Contract — IC-WB-EVAL
- **Owner:** Evaluate (single). **Objects:** Issue (Core); **Severity/Confidence/Reliability** (attributes); **CAF Assessment** (Core, derived); **Outcome Confidence** (Core, derived aggregate). **Reads:** Findings (Infer) + Attested knowledge. **Produces:** Issues + assessment values (all Derived). **Consumed by:** Advise (Wave C), Disclose (Wave E).
- **Required behavior:** (1) **evaluate the current state** — assign **severity** to Findings (→ Issues), compute **confidence** and **reliability** (epistemic state), compute **CAF Assessment** and **Outcome Confidence** (aggregate); (2) **prioritize** the current state; (3) emit assessment events and **append a Cognition History Record** per emission (via 00R) carrying input-version + model/rule version + lineage; (4) on recompute, **recompute and supersede** (live replaced; history appended) — this is the **"why did confidence change"** backbone.
- **Forbidden:** generate Findings (Infer's), recommendations/clarifications (Advise's); write canonical/promote to Attested; govern exposure; accept an interpretation as truth; change any value outside recompute.
- **Confidence semantics (preserved):** Confidence = trust in **understanding**, **never** project health; reliability is a source-trust qualifier; CAF/Outcome Confidence are derived aggregates. **Band-level** stability under semantic replay.
- **Invariants:** Derived/non-canonical; only-recompute-changes-assessment; emission appends history; confidence ≠ project health; no acceptance.

### 2.2 QA Contract — QA-WB-EVAL
- **Positive:** severity assigned → Issue formed from a Finding; confidence/reliability computed (epistemic state); CAF + Outcome Confidence aggregated; each emission appends a Cognition History Record with input/model version + lineage; recompute supersedes prior values (prior records intact); a confidence change is **explainable** from the history (what input/model changed).
- **Negative (impossible/rejected):** Evaluate generating Findings or Recommendations; confidence interpreted as project health; a value changing without recompute; writing canonical / promoting to Attested; accepting an interpretation; a history record overwritten; an assessment changed by intake/acceptance alone.
- **Failure classification:** Critical — value changed without recompute / history overwrite / Derived→Attested / confidence-as-project-health / acceptance-as-truth; Major — missing lineage on emission; CAF/Outcome aggregation error; Minor — band-label/metadata gaps. **Determinism tier (QA Governance):** rule-derived components exact; AI-assisted confidence **band-semantic**.
- **Regression anchors:** only-recompute-changes-assessment; confidence=understanding-not-health; emission appends history; band stability.

### 2.3 Observability Contract — OBS-WB-EVAL
- **Events:** Issue Generated; CAF Assessed; Outcome Confidence Computed; Cognition History Record appended. **Audit:** for every value — input-attestation version, model/rule version, upstream Finding/Issue lineage (answers *what/when/why changed*). **Replay:** record-exact for every emission; derivation **band-semantic** (exact for formula components). **Drift/Trust:** value changed without recompute, confidence inflation, missing lineage, history overwrite = **trust failures**; **Outcome Drift** in confidence across history = **product feature** (the "why did Outcome Confidence drop 84→61" capability is satisfied by the Cognition History lineage).

---

## 3. Triad Consistency & Conformance (Framework §E/§H/§K)

- **§E traceability** ✅ — Finding/Issue/Confidence/CAF/Outcome Confidence trace to the Object Model (DL-043 epistemic overlay: all Derived); behaviors to the Behavior Model (Finding Detected/Issue Generated/CAF Assessed/Outcome Confidence Computed + append-on-recompute); ownership to the Inventory (Infer / Evaluate, one producer each).
- **§H triad consistency** ✅ — QA positives↔IC required, negatives↔IC forbidden; IC-emitted events ⊆ OBS-observed; invariants bound (IC) / validated (QA) / observed (OBS); the **emission→history-append** discipline is consistent across both packages and the 00R backbone.
- **§K pre-use** ✅ — no orphan behavior; **one producer per output** (Infer owns Findings; Evaluate owns Issues/assessment); no invented concepts (objects from the Object Model; Severity/Confidence/Reliability as attributes per §8); **no Authority** (inactive R1); no environment binding; no implementation/technology.
- **Cross-wave** ✅ — consumes Wave A (Attested knowledge from 002; emission/append discipline from 00R); feeds Wave C (Advise) and Wave E (Disclose). Acceptance-Impact Assessment (Wave U) will consume these emissions' history records.

## 4. Final Verdict

**READY FOR REVIEW — DL-043-conformed.** Wave B defines the Understanding layer: **Finding** (Infer) and **Issue/Confidence/Reliability/CAF/Outcome Confidence** (Evaluate), all **Derived/non-canonical/recomputable**, each emission appending a **Cognition History Record** with input/model lineage, under **two-axis replay** and **only-recompute-changes-assessment**. Confidence remains *trust in understanding, never project health*; conflicts/ambiguity are surfaced, not resolved; no Authority and no acceptance. The drift-explanation capability ("why did confidence change") is satisfied structurally by the Cognition History lineage.

> ### Proposed Owner Resolution
> Approve Wave B (WB-INFER, WB-EVAL) as the Understanding contract layer. Proceed to Wave C (Advise: Recommendation, Clarification) and Wave U (User Acceptance & Reconciliation).

---

*This Wave B package defines the Release 1 Understanding contracts for Infer (Finding, with Gap/Conflict/Risk types, anchored to Attested evidence) and Evaluate (Issue, Severity/Confidence/Reliability attributes, CAF Assessment, Outcome Confidence), establishing all of them as Derived Cognition that is non-canonical and recomputable, that emits an append-only Cognition History Record per emission carrying input-attestation and model/rule version plus upstream lineage, that obeys only-recompute-changes-assessment with two-axis replay (record-exact, derivation exact-if-rule/band-semantic-if-AI), that surfaces conflicts and ambiguity rather than resolving them into canonical truth, that preserves confidence as trust in understanding rather than project health, and that performs no governance and no interpretation acceptance. It includes mandatory positive-and-negative QA with QA-Governance severity and determinism tiers, observability whose Cognition History lineage satisfies the drift-explanation capability while distinguishing trust-failure drift from product Outcome Drift, and self-validation against Framework §E/§H/§K, introducing no new responsibility, no Authority, and no implementation or environment binding; routed to the owner for review.*

**Wave B Contract Packages — Understanding complete.**
