# Release 1 Runtime Object Model v1

**Document Type:** Runtime Object Model (architecture-concept; governance) · **Status:** **Updated under DL-043 (2026-06-04)** · **Date:** 2026-06-04
**Foundation for:** Implementation/QA/Observability Contracts · State-Transition Definitions · Runtime & Governance Traceability. **Builds on:** `RELEASE_1_CONTRACT_INVENTORY_V1.md` (ownership — *who owns it*) · `OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md` (accepted core). **Consistent with ratified lifecycles:** Finding lifecycle (`FINDING_SYSTEM_…`), Recommendation lifecycle (post-v1.2 incl. `deferred`), AMB-1 (Resolution Paths presentation-only).

> **Mode:** runtime-concept modeling only — **no** databases, APIs, implementation, schemas, languages, frameworks, or UI technology. **Answers:** *what is it? how does it live? how does it change? how is it governed? how is it observed?* **Does not revisit ownership** unless a contradiction is found. **Accepted core:** Perceive · Retain · Infer · Evaluate · Advise · Disclose · Act; cross-cutting **Authority** + **Adapt**; **Advise = governable candidate response.** **Per `CLAUDE.md`, owner ratifies.**

---

## Section 1 — Runtime Object Inventory

| Object | Responsibility Owner | Classification |
|---|---|---|
| **Intake** | | |
| Intake Submission | Perceive | Supporting Runtime Object (transient) |
| Artifact (raw) | Perceive → Retain | Core Runtime Object |
| Promotion Candidate | Perceive | Supporting Runtime Object (transient, pre-promotion) |
| Context Signal | Perceive | Event Object (observational) |
| **Knowledge** | | |
| Project | Retain | Core Runtime Object |
| Project Artifact (canonical) | Retain | Core Runtime Object |
| Canonical Fact | Retain | Core Runtime Object |
| Assumption | Retain | Core Runtime Object |
| Constraint | Retain | Core Runtime Object |
| Dependency | Retain | Core Runtime Object (relationship) |
| **Infer** | | |
| Finding | Infer | Core Runtime Object |
| Gap | Infer | Supporting (Finding **type**) |
| Conflict | Infer | Supporting (Finding **type**) |
| Risk Signal | Infer | Supporting (Finding **type**: feasibility risk) |
| **Evaluate** | | |
| Issue | Evaluate | Core Runtime Object |
| Severity | Evaluate | Supporting (**attribute** of Issue) |
| Confidence | Evaluate | Supporting (**attribute** / per-driver) |
| Reliability | Evaluate | Supporting (**attribute** / qualifier) |
| CAF Assessment | Evaluate | Core Runtime Object (derived) |
| Outcome Confidence | Evaluate | Core Runtime Object (derived aggregate) |
| **Advise** | | |
| Recommendation | Advise | Core Runtime Object |
| Clarification Request | Advise | Core Runtime Object |
| Suggested Action | Advise | Supporting (Recommendation **type**) |
| Candidate Improvement | Advise | Supporting (Recommendation **type**) |
| **Authority** | | |
| Governance Decision | Authority Plane | Governance Object |
| Exposure Decision | Authority Plane | Governance Object (Decision **type**) |
| Authorization Decision | Authority Plane | Governance Object (Decision **type**) |
| **Disclose** | | |
| Awareness Card · Finding Card · Issue Card · Recommendation Card | Disclose | Presentation Object |
| MRI View · Companion View · Overview View | Disclose | Presentation Object |
| *(MRI Snapshot)* | Disclose | Supporting (snapshot rendered by MRI View) |
| **Runtime / Events** | | |
| Recompute Event | Adapt (trigger → Act) | Event Object |
| Notification | Disclose | Event / Presentation Object |
| State Transition Event | Adapt | Event Object |

**Note (classification correction, §8):** Severity/Confidence/Reliability are **attributes** of Issue/assessment, not standalone Core objects; Gap/Conflict/Risk are **Finding types**; Suggested-Action/Candidate-Improvement are **Recommendation types**; **Resolution Paths are NOT a runtime object** (presentation grouping of multiple Recommendations — AMB-1).

---

### Section 1A — DL-043 Epistemic Overlay (authoritative; supersedes conflicting rows)

Every Core object now carries an **epistemic classification** — orthogonal to its responsibility owner. This overlay governs where conflicting:

**Epistemic states (per the Epistemic State Model):**
- **Attested (canonical)** — source-attributed, re-derivable; admitted to Retain. Three attesting sub-classes: **evidence-attested**, **OSLO-self-attested**, **user-attested**.
- **Derived (non-canonical)** — OSLO-authored interpretation; recomputable; **never promoted to Attested** (one-way flow).

**Classification of existing objects:**
- **Attested / evidence-attested (Retain canonical):** Canonical Fact, **Assumption / Constraint / Dependency *only when attested*** (stated in evidence). *Inferred* assumptions/constraints/dependencies are **Derived**, owned by Infer — not canonical.
- **Derived (non-canonical; Infer/Evaluate/Advise):** Finding (+Gap/Conflict/Risk types), Issue, Confidence/Reliability/Severity (attributes), CAF Assessment, Outcome Confidence, Recommendation, Clarification Request, and the new **Acceptance-Impact Assessment**.

**New objects (added):**
| Object | Owner | Classification |
|---|---|---|
| **Attested Assertion** *(abstract canonical unit; content-typed: fact/assumption/constraint/dependency/goal)* | Retain | Core (epistemic root of canonical knowledge) |
| **Cognition History Record** *(OSLO-self-attested; "OSLO emitted C at T under conditions K")* | Retain | Core Runtime Object — Attested, append-only, immutable, recompute-appends |
| **User Acceptance Record** *(user-attested; "U accepted I at T"; version-pinned to a Cognition History Record or attestation id)* | Retain *(captured by Perceive)* | Core Runtime Object — Attested, append-only, decoupled from accepted item |
| **Acceptance-Impact Assessment** *(drift of a previously accepted decision vs current understanding)* | Infer + Evaluate | Core Runtime Object — **Derived**, recomputable |

**Authority objects — reclassified Future / inactive in R1 (DL-043 constituent B):**
| Object | R1 status |
|---|---|
| Governance Decision · Exposure Decision · Authorization Decision | **Out of R1 — Future (Authority plane specified but inactive).** R1 admission is **integrity-gated** (Perceive readiness + Retain provenance/idempotency/evidence-chain), not Authority-gated. R1 "disposition" is a **User Acceptance Record + Acceptance-Impact Assessment**, not a Governance Decision. |

**Invariants:** Canonical = Attested · persistence ≠ canonicalization · one-way flow (Derived↛Attested) · acceptance-recording ≠ truth-assertion · recompute appends history, never overwrites. *(Live Derived Cognition is held as a recomputable projection by its cognitive owner, not stored as canonical in Retain; only its Cognition History Records are canonical.)*

## Section 2 — Object Definitions (Core Runtime Objects)

*(Definition · Purpose · Owner · Produced By · Consumed By)*

- **Artifact** — a raw ingested input. *Purpose:* carry user/source content into OSLO. *Owner:* Perceive→Retain. *Produced by:* Perceive (intake). *Consumed by:* Retain (promotion), Infer (analysis).
- **Project** — the unit of outcome understanding. *Purpose:* container for an outcome's knowledge/analysis. *Owner:* Retain. *Produced by:* Perceive (creation). *Consumed by:* all responsibilities (scope).
- **Project Artifact (canonical)** — a promoted, canonical artifact. *Owner:* Retain. *Produced by:* Retain (on authorized promotion). *Consumed by:* Infer, Disclose.
- **Canonical Fact** — an atomic canonical assertion (incl. the **declared outcome** — the alignment reference in R1; Intend provisional). *Owner:* Retain. *Produced by:* Retain (promotion). *Consumed by:* Infer, Evaluate.
- **Assumption** — an explicitly-flagged epistemic assumption. *Owner:* Retain. *Produced by:* Perceive/Retain. *Consumed by:* Infer, Evaluate.
- **Constraint** — a declared limit (resource/time/dependency). *Owner:* Retain. *Consumed by:* Infer (feasibility), Evaluate.
- **Dependency** — a relationship between canonical objects. *Owner:* Retain. *Consumed by:* Infer (structure).
- **Finding** — a descriptive structural implication (gap/conflict/risk type). *Owner:* Infer. *Produced by:* Infer engines. *Consumed by:* Evaluate, Disclose (Finding Card), Advise (anchor).
- **Issue** — a judged Finding carrying severity/confidence/epistemic state. *Owner:* Evaluate. *Produced by:* Evaluate. *Consumed by:* Authority (disposition), Advise (anchor), Disclose (Issue Card).
- **CAF Assessment** — the Clarity/Alignment/Feasibility assessment (derived). *Owner:* Evaluate. *Consumed by:* Outcome Confidence, Disclose.
- **Outcome Confidence** — the reliability-qualified aggregate trust-in-understanding (derived). *Owner:* Evaluate. *Consumed by:* Disclose (Overview/Companion). *(Never project health.)*
- **Recommendation** — a governable candidate response (improvement/suggested-action type) anchored to a Finding/Issue. *Owner:* Advise. *Produced by:* Advise Recommendation engine. *Consumed by:* Authority (govern exposure), Disclose (Recommendation Card).
- **Clarification Request** — a governable candidate response seeking information to improve understanding. *Owner:* Advise. *Produced by:* Advise Clarification engine. *Consumed by:* Authority (exposure), Disclose; **answer feeds Perceive→reanalysis.**
- **Governance Decision** — an exposure/authorization decision over a governed object. *Owner:* Authority Plane. *Produced by:* Authority engines. *Consumed by:* Disclose (what may be shown), Act (what may be actuated). *(Generates no cognition.)*

## Section 3 — Lifecycle Definitions

*(Creation · Modification · Resolution · Archival · Retirement; + mutability)*

| Object | Mutability | Lifecycle |
|---|---|---|
| Artifact / Project Artifact | **Append-only (versioned)** | created on ingest/promotion; new version on edit; never deleted; superseded version retained |
| Canonical Fact / Assumption / Constraint / Dependency | **Append-only (versioned)** | created on promotion; superseded by new version; retained |
| Project | **Append-only (versioned)** | created; updated via versioned changes; archived (not deleted) |
| **Finding** | **Derived (append-only supersession)** | created by Infer; modified only via recompute (re-derivation); resolved = closed; superseded by re-derivation; prior retained |
| **Issue** | **Derived (append-only supersession)** | created by Evaluate from Findings; re-derived on recompute; resolved/superseded; prior retained |
| CAF Assessment / Outcome Confidence | **Derived** | recomputed each pass; prior snapshots retained (append-only) |
| **Recommendation** | **Derived (append-only supersession)** | generated by Advise; user-state (accepted/rejected/deferred/implemented) recorded; superseded by recompute; prior retained |
| **Clarification Request** | **Derived** | generated by Advise; answered/dismissed; answer → reanalysis; superseded; prior retained |
| **Governance Decision** | **Append-only** | created on disposition/authorization; superseded by a new decision; never mutated; full history retained |
| Notification | **Append-only** | created on event; read/dismissed (presentation state); retained |
| Recompute / State-Transition Event | **Immutable (append-only log)** | created on occurrence; never modified; retained |

**Retirement principle:** no Core object is *deleted*; retirement = **archival/supersession**, retained (append-only), consistent with OSLO's history doctrine.

## Section 4 — State Models

*(State · Allowed Transitions · Terminal States)*

- **Finding:** `detected → acknowledged → addressed → closed`; `addressed/closed → reopened`; any → `superseded`. **Terminal:** closed, superseded. *(Closure via reanalysis, not manual.)*
- **Issue:** `detected → (exposed | deferred | suppressed)` (via Governance) `→ resolved`; any → `superseded`. **Terminal:** resolved, superseded.
- **Recommendation:** `generated → (accepted | rejected | deferred) → implemented`; any → `superseded`. **Terminal:** implemented, rejected, superseded. *(Acceptance ≠ success; success via reanalysis.)*
- **Clarification:** `generated → (answered | dismissed)`; answered → `consumed` (feeds reanalysis); any → `superseded`. **Terminal:** consumed, dismissed, superseded.
- **Governance Decision:** `pending → decided (expose | suppress | defer | block | authorize)`; → `superseded` (by new decision). **Terminal:** decided, superseded.
- **Notification:** `created → delivered → (read | dismissed)`. **Terminal:** read, dismissed.
- **Recompute Event:** `triggered → running → (complete | failed)`. **Terminal:** complete, failed. *(Failed retains last-known-good.)*

All transitions are **append-only** (prior states retained); only **reanalysis (recompute)** changes Finding/Issue/Recommendation assessment content.

## Section 5 — Relationship Model

```text
Artifact ──promotion──▶ Canonical Fact / Assumption / Constraint / Dependency
   │
   └──analyzed──▶ FINDING ──judged──▶ ISSUE ──advised──▶ RECOMMENDATION ──governed──▶ GOVERNANCE DECISION ──disclosed──▶ Recommendation Card
                    │                    │                    │                                                 │
                    │                    └─contributes──▶ CAF Assessment ──▶ Outcome Confidence ──disclosed──▶ Overview / Companion View
                    │                    │
                    ├─anchors──▶ CLARIFICATION REQUEST ──governed──▶ Governance Decision ──disclosed──▶ (in context) ──answer──▶ Perceive → recompute
                    │
                    ├─disclosed──▶ Finding Card / Issue Card
                    └─grouped (presentation)──▶ MRI VIEW  (renders Findings/Issues by lens)
RECOMMENDATION (×N for one Finding) ──presentation grouping──▶ "Possible Resolution Paths"  (NOT an object — AMB-1)
Recompute Event ──re-derives──▶ Finding → Issue → Recommendation → (Outcome Confidence)   [Adapt loop]
State Transition Event ──reflects──▶ analysis/stale/reanalysis states ──disclosed──▶ all surfaces
```

**Canonical chain:** `Artifact → Finding → Issue → Recommendation → Governance Decision → Card/View`, with Clarification anchored to Finding/Issue (answer → recompute), CAF/Outcome-Confidence derived from Issues, and MRI a presentation view over Findings/Issues.

## Section 6 — Governance Touchpoints

| Object | Governed? | Governance Interaction |
|---|---|---|
| Artifact / Canonical Fact (promotion) | **Yes** | **Authorization** (promotion) |
| Finding | **Yes** | **Exposure** (expose/suppress/defer) |
| Issue | **Yes** | **Exposure** (disposition) |
| CAF / Outcome Confidence | **Yes** | **Exposure** |
| Recommendation | **Yes** | **Exposure + Authorization** (if action implicated) |
| Clarification Request | **Yes** | **Exposure** |
| Cards / Views (MRI/Companion/Overview/…) | **Yes** *(inherit)* | **Exposure** (of the objects they present) |
| Notification | **Yes** | **Exposure + timing** |
| Governance Decision | **No** *(it is governance)* | None |
| Recompute / State-Transition Event | **No** *(always-on, posture-invariant)* | None |
| Intake Submission / Promotion Candidate | partial | **Authorization** (at promotion) |

## Section 7 — Observability Requirements

*(Creation Event · State-Change Event · Governance Event · Recompute Trigger · Audit)*

| Object | Creation | State-Change | Governance | Recompute Trigger | Audit |
|---|---|---|---|---|---|
| Artifact / Canonical knowledge | Yes | Yes (version) | Yes (promotion) | Yes (mutation→recompute) | Yes |
| Finding | Yes (generation) | Yes (lifecycle) | Yes (exposure) | re-derived | Yes |
| Issue | Yes | Yes | Yes (disposition) | re-derived | Yes |
| CAF / Outcome Confidence | Yes | Yes (recompute) | Yes (exposure) | re-derived | Yes |
| Recommendation | Yes (**generation event**) | Yes (accept/reject/defer/implement) | Yes (exposure/auth) | re-derived | Yes |
| Clarification | Yes (**generation event**) | Yes (answered/dismissed) | Yes (exposure) | answer→trigger | Yes |
| Governance Decision | Yes (**decision event**) | Yes (superseded) | n/a | — | **Yes (core audit)** |
| Notification | Yes | Yes (read/dismiss) | Yes (exposure) | — | light |
| Recompute Event | **Yes (trigger event)** | Yes (running/complete/failed) | No | self | Yes |
| State Transition Event | **Yes** | n/a (immutable) | No | reflects | Yes |

Core observability surfaces: **state transitions, recompute triggers, governance decisions, recommendation-generation events, clarification-generation events** (consistent with Contract Inventory §5).

## Section 8 — Runtime Consistency Review

- **Duplicate objects:** none — but **classification corrections (Minor):** Severity/Confidence/Reliability are **attributes** of Issue/assessment, **not** standalone Core objects; modeling them as objects would duplicate Issue state.
- **Objects that should be merged (Minor):** Gap/Conflict/Risk Signal **into Finding** (as types); Suggested-Action/Candidate-Improvement **into Recommendation** (as types); Exposure/Authorization Decision **into Governance Decision** (as types).
- **Objects that should be split:** none.
- **Missing objects (Minor):** **Outcome Reference / alignment target** — in Release 1 this is a **Canonical Fact** (the declared outcome) under Retain; a distinct **Intend** object is **Provisional/Future** (do not add in R1). **MRI Snapshot** named as the supporting snapshot the MRI View renders (already in §1).
- **Ownership inconsistencies:** **none** — every object's owner matches the ratified inventory.
- **Forbidden object (consistency guard):** **no Resolution-Path object** — Resolution Paths are a presentation grouping of multiple Recommendations (AMB-1). Re-introducing it would contradict a ratified decision.

**Classification:** **No Critical. No Major.** Findings are **Minor** (attribute-vs-object classification; type-folding; outcome-reference = knowledge object in R1) — resolve as modeling clarifications before contract generation; none changes ownership or blocks contracts.

## Section 9 — Contract Generation Readiness

**B — Ready with Minor Clarifications.**

**Justification:** the model defines every Release 1 runtime object with **owner, lifecycle, state model, relationships, governance touchpoints, and observability** — sufficient for Implementation/QA/Observability contract generation **without inventing new runtime concepts.** The only open items are the **Minor classification clarifications** in §8 (severity/confidence/reliability = attributes; gap/conflict/risk and suggested-action/improvement = types; exposure/authorization = Governance-Decision types; outcome-reference = Canonical Fact in R1; no Resolution-Path object). Settling these (a modeling cleanup, not new concepts) lets contracts model objects correctly. **No Critical/Major gap; no ownership conflict.** *(Rests on owner ratification of the architectural core.)*

## Section 10 — Final Recommendation

- **Runtime Model Completeness Score: 93 / 100** — all Release 1 objects defined with lifecycle/state/relationships/governance/observability; −7 for the Minor classification clarifications and the provisional outcome-reference/Intend.
- **Object Ownership Clarity Score: 96 / 100** — every object maps to one owning responsibility, consistent with the Contract Inventory; −4 for attribute-vs-object edges.
- **Contract Readiness Score: 92 / 100** — contracts generable without inventing concepts; −8 for the Minor clarifications + assumed-pending core ratification.

**Recommended next artifact:** **`RELEASE_1_CONTRACT_GENERATION_PLAN_V1.md`** — the dependency-first sequencing that produces **one coordinated contract set (Implementation + QA + Observability) per backlog story** (per `CONTRACT_GENERATION_FRAMEWORK_V1.md`), each set referencing **this object model** (object definitions, state models, governance/observability touchpoints) and the **Contract Inventory** (owning responsibility). First sets: the foundational Core objects (Artifact/Perceive → Finding/Infer → Issue/Evaluate → Recommendation/Advise), deferring Provisional/Future objects (Intend, actuation, Learn/Coordinate).

---

*This Release 1 Runtime Object Model defines every runtime object required for Release 1 as an architecture concept — answering what it is, how it lives, how it changes, how it is governed, and how it is observed — building on the Contract Inventory's ownership answers. It inventories objects by owning responsibility and classification (Core/Supporting/Presentation/Governance/Event), defines the Core objects (Artifact, Project, Canonical Fact/Assumption/Constraint/Dependency, Finding, Issue, CAF Assessment, Outcome Confidence, Recommendation, Clarification Request, Governance Decision), specifies lifecycle and mutability (canonical knowledge append-only/versioned; Findings/Issues/Recommendations derived with append-only supersession; Governance Decisions and events append-only/immutable; nothing deleted), state models for Finding/Issue/Recommendation/Clarification/Governance-Decision/Notification/Recompute-Event consistent with the ratified lifecycles, the Artifact→Finding→Issue→Recommendation→Governance-Decision→Card relationship graph (Clarification anchored to Findings with answers feeding recompute; CAF/Outcome-Confidence derived; MRI a presentation view; no Resolution-Path object), governance touchpoints (exposure/authorization per object; recompute/events ungoverned), and observability requirements (state transitions, recompute triggers, governance decisions, recommendation/clarification generation events). A consistency review finds no Critical/Major issues — only Minor classification clarifications (severity/confidence/reliability are attributes; gap/conflict/risk and suggested-action/improvement are types; outcome-reference is a Canonical Fact in R1 with Intend provisional; no Resolution-Path object) — and assesses the model Ready with Minor Clarifications (Completeness 93, Ownership Clarity 96, Contract Readiness 92), recommending the Contract Generation Plan as the next artifact. It discusses no databases, APIs, implementation, schemas, languages, frameworks, or UI technology.*

**Release 1 Runtime Object Model v1 complete.**


---

## DL-047 Object Additions (ratified 2026-06-04)

| Object | Class | Owner | Notes |
|---|---|---|---|
| `SynthesizedPlanningModel` | **Derived** | Infer | constructed planning model from Attested assertions; recomputable; CHR per emission |
| `PlanningArtifact` (Intent/Context/Scope/Requirements/WBS/Resources/Schedule) | **Derived** (generated, user-editable) | Infer (generate) · Retain (store version) · Disclose (present) | a user edit = new Attested input → recompute; never Attested-as-truth |
| `ChatSession` / `ChatExchange` | **Non-canonical interaction** | Disclose | consumes/triggers cognition; writes no canonical |
| `ReviewRequest` / `StakeholderResponse` (CRR) | response → **evidence-attested** on submit | Perceive (intake) · Disclose (status) | response triggers Deep Pass; workflow UI = commodity |
| `SuggestedFix` | **Derived** (Advise candidate) | Advise | application = user edit; no autonomous OSLO write |

`confidence_stage` (DL-046) generalizes to the **Understanding State Model** (AE-04): Initial→Partial→Refined→Validated→Mature — an emission attribute, not a new object.

## DL-049 Object Additions (ratified 2026-06-05)

Resolves gap #337. **One identity object, two capability levels — not two objects.**

| Object | Class | Notes |
|---|---|---|
| `Principal` | **Identity (canonical account record)** | the single identity object. Attribute **`type: reviewer \| user`**. `reviewer` = email-verified, **scoped to shared items** (CRR finding / MRI), may view + respond, **no Workspace/projects**. `user` = `Principal` + Workspace/Account + projects + tier (default **Free**). |
| `StakeholderResponse` **author** | reference → `Principal` (`type = reviewer` typically) | the CRR response (DL-047) is authored by a `Principal`; remains **evidence-attested**, provenance = that `Principal`. No seam change. |

**Promotion `reviewer → user` (state transition, NOT a data migration):** flip `type` to `user`, provision Workspace, assign Free tier — **same `Principal` ID**. **Invariants:** identity ID stable → prior `StakeholderResponse` attribution **immutable** (append-only, never re-keyed); response = **evidence, not truth** (unchanged by promotion); **scope to the inviter's project is never widened** (account-type ≠ share-scope); promotion **audited** (SEC-06). Reviewer-driven recompute (CRR-04 → Deep Pass) is **DL-048-bounded** (draws the inviter's budget). Different-email later signup = a **new** `Principal` (optional later email-link; merge deferred); **de-dup on verified email**.
