# Release 1 Implementation Contract Template v1

**Document Type:** Operational Template (contract instantiation — delivery architecture) · **Status:** Draft · **Date:** 2026-05-31
**Conforms to / subordinate to (authoritative — must not redefine):** `AI_FIRST_PRODUCT_DELIVERY_ARCHITECTURE_V1.md` · `IMPLEMENTATION_CONTRACT_SPECIFICATION_V1.md` · `RELEASE_1_UX_PRODUCT_BACKLOG_V1.md` · `RELEASE_1_UX_EXECUTION_PLAN_V1.md` · `RELEASE_1_UX_SCOPE_FREEZE_AND_BACKLOG_CONTROL_SPECIFICATION_V1.md`.

> **Non-negotiable constraints.** This template defines **contract structure, field descriptions, and completion expectations** only. It must **NOT** define APIs, schemas, frameworks, implementation details, vendor/model choices, coding standards, deployment details, infrastructure, or testing tooling. **Implementation remains outside this document.** Source specs govern.

> **Not a specification — a template.** This is the **operational form** populated for **every Release 1 backlog story** to produce an Implementation Contract conforming to `IMPLEMENTATION_CONTRACT_SPECIFICATION_V1.md`.

---

## A. Purpose

Provide the canonical template used to **instantiate Implementation Contracts** for Release 1 UX stories. **Every Release 1 backlog story must be transformed into an Implementation Contract using this structure.** The populated template is directly usable by **AI implementation systems** (to implement within contract), **human reviewers** (to approve/own), **QA contract generators** (to derive validation), and **observability contract generators** (to derive runtime observation). The template carries intent **losslessly** from a canonical source story to executable work, with traceability, dual acceptance, and bound invariants.

---

## B. Contract Header

| Field | Description |
|---|---|
| **Contract ID** | Stable unique ID; resolves to one story/epic (convention: `IC-EP##-US#.#-v#`). |
| **Contract Name** | Human-readable name (mirrors the source story title). |
| **Contract Version** | Version of this contract instance. |
| **Status** | Draft / Ready / In Implementation / In Review / Accepted / Rejected / Needs Clarification. |
| **Epic ID** | Source epic (EP-##). |
| **Story ID** | Source backlog story (US-#.#). |
| **Construct Type** | Per the ratified taxonomy (Workspace / Panel / Companion Surface / Interaction Layer / Understanding Object). |
| **Priority** | From backlog sequencing (no estimates). |
| **Created Date** / **Last Updated** | Provenance dates. |

## C. Source Traceability

| Field | Description / instruction |
|---|---|
| **Source Specification(s)** | Canonical spec(s) governing this work. |
| **Source Section(s)** | The exact governing sections/clauses. |
| **Source Story** | The backlog story text (As-a/I-want/so-that). |
| **Source Acceptance Criteria** | The spec's relevant `*-C#` conformance items (positive). |
| **Source Negative Acceptance Criteria** | The spec's relevant explicit fail conditions (negative). |
| **Applicable Invariants** | The cross-surface invariants that constrain this work (§I). |

**Instruction:** every obligation below MUST resolve to one of these sources (bidirectional traceability). **No contract may invent intent** — anything not derivable goes to the Ambiguity Register (§L), not into scope.

## D. User Intent

| Field | Description |
|---|---|
| **User Role** | The user type from the story ("As a …"). |
| **User Goal** | The capability ("I want …"). |
| **User Outcome** | The benefit ("so that …"). |
| **Business Purpose** | The product/outcome reason the story exists. |

This section **preserves original intent** verbatim from the source story; implementation must serve this intent and nothing beyond it.

## E. Functional Scope

| Field | Description |
|---|---|
| **Required Behaviors** | What the increment must do (positive obligations). |
| **Expected User Experience** | The interaction outcome (structure/states, not styling). |
| **Context Requirements** | What context the surface operates within / preserves. |
| **Routing Requirements** | Entry/exit routes; destination-vs-layer rules. |
| **State Requirements** | Analysis/stale/reanalysis/lifecycle states involved. |

**Scope must be derived only from source specifications** (§C); nothing is added by inference.

## F. Explicit Out-of-Scope Boundaries

| Field | Description |
|---|---|
| **Deferred Capabilities** | Capabilities deferred per Scope Freeze / spec Deferred Items. |
| **Forbidden Behaviors** | Behaviors the spec forbids (first-class). |
| **Non-Goals** | What this contract intentionally does not pursue. |
| **Explicitly Excluded Scope** | Adjacent scope owned by other contracts/specs. |

This section **protects against implementation drift** — it is as load-bearing as the positive scope.

## G. Positive Acceptance Contract

| Acceptance Criterion ID | Acceptance Requirement | Source Reference |
|---|---|---|
| AC-1 | *(required behavior, objective)* | *(spec §/`*-C#`)* |
| AC-2 | … | … |
*(Repeatable. Each row proves a required behavior **exists**.)*

## H. Negative Acceptance Contract

| Negative Criterion ID | Forbidden Behavior | Source Fail Condition | Source Reference |
|---|---|---|---|
| NA-1 | *(must-not-occur)* | *(spec fail condition)* | *(spec §)* |
| NA-2 | … | … | … |
*(Repeatable. Each row proves a forbidden behavior is **absent**.)* **Negative acceptance is mandatory — a contract instance without it is invalid (§Q).**

## I. Invariant Binding

| Invariant ID | Invariant Description | Applicability | Validation Requirement |
|---|---|---|---|
| INV-1 | Only reanalysis changes assessment | *(applies? where)* | *(how validated)* |
| INV-2 | Recommendation only in Finding context | … | … |
| INV-3 | Confidence is trust in understanding, never project health/score | … | … |
| INV-4 | Stale never current | … | … |
*(Repeatable; include every applicable invariant — see Product Backlog §D for the full set.)*

## J. States

| Field | Description |
|---|---|
| **Normal States** | Expected operational states. |
| **Empty States** | Each distinct empty case (distinguished, honest). |
| **Failure States** | Each distinct failure case (honest, recoverable, non-fabricating). |
| **Recovery Expectations** | How the user recovers from each failure. |

**All state behavior must be explicitly defined** — no implicit/undefined states.

## K. Dependencies

| Field | Description |
|---|---|
| **Upstream Contracts** | Contracts that must complete first. |
| **Required Preconditions** | Conditions that must hold before this work. |
| **Related Contracts** | Sibling contracts sharing context. |

## L. Ambiguity Register

| Ambiguity ID | Description | Blocking Status | Required Owner Decision |
|---|---|---|---|
| AMB-1 | *(gap/conflict/silence/new-construct)* | Blocking / Non-blocking | *(what the owner must decide)* |
*(Repeatable.)* **No ambiguity may be resolved by implementation** — it is flagged here and routed to owner clarification/reconciliation (Impl Contract Spec §F).

## M. Human Review Requirements

| Field | Description |
|---|---|
| **Review Trigger** | What triggers mandatory review (ambiguity · invariant risk · deferred-scope request · failed validation · source conflict · post-implementation). |
| **Reviewer Role** | Who must review/approve. |
| **Approval Required** | Yes/No (machines propose; humans approve). |

## N. QA Contract Handoff

| Field | Description |
|---|---|
| **QA Contract ID** | The bound QA Contract instance (to be generated). |
| **Validation Scope** | What the QA Contract must validate. |
| **Positive Validation Requirements** | From §G (acceptance → tests). |
| **Negative Validation Requirements** | From §H (fail conditions → negative tests). |
| **Invariant Validation Requirements** | From §I (bound invariants → invariant tests). |

This section **prepares handoff to QA Contract generation** (structure of the QA Contract is defined elsewhere).

## O. Contract Completion Checklist

- [ ] Source traceability complete
- [ ] Intent captured
- [ ] Scope defined
- [ ] Out-of-scope defined
- [ ] Acceptance complete
- [ ] Negative acceptance complete
- [ ] Invariants attached
- [ ] States defined
- [ ] Dependencies recorded
- [ ] Ambiguities resolved or flagged
- [ ] Human review requirements recorded
- [ ] QA handoff complete

A contract instance is eligible for implementation **only** when every box is checked.

---

## P. Example Contract (fully worked)

> Worked instance for **EP-7 / US-7.2 — "Recommendation Panel from Finding Only."** Populated from actual Release 1 source material; realistic enough for an AI implementation system to implement the feature.

### B. Contract Header
- **Contract ID:** IC-EP07-US7.2-v1 · **Contract Name:** Recommendation Panel — Finding-Context-Only Launch · **Contract Version:** 1 · **Status:** Ready
- **Epic ID:** EP-7 (Finding & Recommendation Panels) · **Story ID:** US-7.2 · **Construct Type:** **Panel** (contextual) · **Priority:** Step 6 (after MRI/Artifact, Finding Panel) · **Created:** 2026-05-31 · **Last Updated:** 2026-05-31

### C. Source Traceability
- **Source Specification(s):** `RECOMMENDATION_PANEL_SPECIFICATION_V1.md`; `FINDING_PANEL_SPECIFICATION_V1.md`; `FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md` (Option A); `UNDERSTANDING_COMPANION_RECONCILIATION_DECISION_001.md` (Option B).
- **Source Section(s):** Recommendation Panel §A, §D (surface model), §J (alternatives), §K (actions), §R (RP-C1, RP-C4, RP-C6); Surface Decision §A (Panel Model).
- **Source Story:** *As a user, I want to open recommendations only from a Finding, so that advice stays attributed to its weakness.*
- **Source Acceptance Criteria:** RP-C1 (opens only in Finding context); RP-C4 (alternatives persist; Selected Path ≠ OSLO Recommended); RP-C2 (advisory; attribution preserved).
- **Source Negative Acceptance Criteria:** RP-C1 fail (opens standalone / without Finding); RP-C4 fail (alternatives disappear / Selected Path replaces OSLO Recommended); RP-C9 fail (a Resolution-Path/Clarification/Resolution-Candidate object appears).
- **Applicable Invariants:** INV-2 (Recommendation only in Finding context); INV-1 (only reanalysis changes assessment); INV-3 (presentation-only resolution constructs); INV-10 (context preserved); INV-11 (no forbidden capabilities).

### D. User Intent
- **User Role:** project user investigating a weakness. **User Goal:** open recommendations only from a Finding. **User Outcome:** advice stays attributed to its weakness (recommendation→finding traceability). **Business Purpose:** preserve attribution integrity and the single Artifact→Finding→Recommendation model (Surface Decision Option A).

### E. Functional Scope
- **Required Behaviors:** the Recommendation Panel is reachable **only** from an open Finding (Finding Panel) context; it opens **in context** over the Finding; it presents the finding's recommendations advisorily (OSLO Recommended / Possible Resolution Paths / Selected Path as presentation constructs); it preserves the Finding context beneath and restores it on close.
- **Expected User Experience:** from a Finding Panel, the user opens recommendations and evaluates them without losing the finding context; closing returns to the Finding.
- **Context Requirements:** Finding context required and preserved; recommendation→finding attribution always reachable.
- **Routing Requirements:** entry **only** via Finding (Finding Panel / Companion-routed-via-Finding / Chat-routed-via-Finding); **no** entry from Overview/MRI/Artifact/Companion/Chat/Awareness/History/Export without a Finding.
- **State Requirements:** reanalysis-aware (running/complete); recommendation lifecycle presented; stale honored.

### F. Explicit Out-of-Scope Boundaries
- **Deferred Capabilities:** none added (no execution/governance/automation).
- **Forbidden Behaviors:** opening standalone; manual finding resolution; executing/applying a recommendation; changing assessment.
- **Non-Goals:** finding explanation content (US-7.1), reanalysis outcomes UI (US-7.3) — sibling contracts.
- **Explicitly Excluded Scope:** Companion Top-Recommendation routing internals (EP-8/US-8.2, which routes via Finding); Chat routing internals (EP-9).

### G. Positive Acceptance Contract
| ID | Acceptance Requirement | Source Reference |
|---|---|---|
| AC-1 | Recommendation Panel opens **only** when a Finding context is present | RP-C1 |
| AC-2 | Panel opens in context and **preserves** the Finding beneath; closing returns to it | RP-C1, INV-10 |
| AC-3 | Recommendations presented **advisorily** with recommendation→finding attribution reachable | RP-C2 |
| AC-4 | OSLO Recommended / Possible Resolution Paths / Selected Path shown; **alternatives persist** after acceptance | RP-C4 |

### H. Negative Acceptance Contract
| ID | Forbidden Behavior | Source Fail Condition | Source Reference |
|---|---|---|---|
| NA-1 | Panel opens standalone or from Overview/MRI/Artifact/Companion/Chat/Awareness/History/Export **without a Finding** | "opens without Finding context" | RP-C1 fail; INV-2 |
| NA-2 | Alternatives disappear after acceptance, or Selected Path **replaces** OSLO Recommended | "alternatives disappear / Selected Path replaces OSLO Recommended" | RP-C4 fail; INV-3 |
| NA-3 | A **Resolution-Path / Clarification-Candidate / Resolution-Candidate object** is introduced | "such object appears" | RP-C9 fail; INV-3 |
| NA-4 | Any panel interaction **changes assessment** (CAF/Reliability/Confidence/finding state) outside reanalysis | "assessment changes without reanalysis" | RP-C7 fail; INV-1 |

### I. Invariant Binding
| ID | Description | Applicability | Validation Requirement |
|---|---|---|---|
| INV-2 | Recommendation only in Finding context | **Primary** | attempt entry from every non-Finding surface → blocked |
| INV-1 | Only reanalysis changes assessment | applies | no panel action mutates assessment |
| INV-3 | Presentation-only resolution constructs | applies | OSLO Recommended/Resolution Paths/Selected Path never objects; alternatives persist |
| INV-10 | Context preserved | applies | open/close preserves Finding context |
| INV-11 | No forbidden capabilities | applies | no execution/governance/apply affordance |

### J. States
- **Normal:** Finding present → Recommendation Panel available; recommendation lifecycle presented.
- **Empty:** no alternatives → show OSLO Recommended (or single rec) with "no alternative recommendations" (not an empty shell).
- **Failure:** recommendations unavailable → "unavailable — retry/return," Finding context retained, no fabrication.
- **Recovery:** close returns to Finding Panel; retry from there.

### K. Dependencies
- **Upstream Contracts:** Finding Panel (US-7.1); Artifact/MRI surfaces (EP-5/EP-6); App Shell (EP-1).
- **Required Preconditions:** an open Finding context exists.
- **Related Contracts:** US-7.3 (reanalysis outcomes); US-8.2 (Companion routes via Finding); EP-9 Chat routing.

### L. Ambiguity Register
| ID | Description | Blocking | Required Owner Decision |
|---|---|---|---|
| — | None. Finding-context-only entry is fully resolved by Surface Decision (Option A) + Companion Decision (Option B). | Non-blocking | None |

### M. Human Review Requirements
- **Review Trigger:** post-implementation; any attempt to broaden entry beyond Finding context (invariant risk). **Reviewer Role:** owner/UX lead. **Approval Required:** Yes.

### N. QA Contract Handoff
- **QA Contract ID:** QA-EP07-US7.2-v1 (to generate). **Validation Scope:** Finding-context-only launch + alternative persistence + non-mutation.
- **Positive Validation:** AC-1…AC-4. **Negative Validation:** NA-1…NA-4. **Invariant Validation:** INV-2 primary (entry blocked from all non-Finding surfaces), INV-1/INV-3/INV-10/INV-11.

### O. Completion Checklist — all checked ✓ (traceability, intent, scope, out-of-scope, acceptance, negative acceptance, invariants, states, dependencies, ambiguities, review, QA handoff).

## Q. Conformance Requirements

A valid contract instance MUST pass; it **fails** if it:
- **missing traceability** (any obligation not resolvable to a cited source);
- **missing acceptance** (no positive acceptance);
- **missing negative acceptance** (positive-only — invalid);
- **missing invariants** (an applicable invariant unbound);
- **invented scope** (intent not from a canonical source);
- **unresolved ambiguity implemented** (a flagged ambiguity built around rather than escalated);
- **deferred capability included** (without owner promotion).

**Explicit fail conditions.** A contract instance is invalid if it omits any required field/section (§B–§N, checklist §O), lacks bidirectional source traceability, contains positive without negative acceptance, omits an applicable invariant, invents or expands scope, includes a deferred/forbidden capability, resolves an ambiguity/conflict without owner decision, or introduces implementation/technology detail.

---

*This template instantiates Implementation Contracts for every Release 1 UX story per `IMPLEMENTATION_CONTRACT_SPECIFICATION_V1.md`. It provides the contract header; source traceability; user intent; functional scope; explicit out-of-scope boundaries; repeatable positive and (mandatory) negative acceptance tables; repeatable invariant binding; normal/empty/failure states with recovery; dependencies; an ambiguity register (no ambiguity resolved by implementation); human-review requirements; QA-contract handoff; and a completion checklist — plus a fully worked example (EP-7 / US-7.2, Recommendation-Panel-from-Finding-only) populated from real Release 1 source material demonstrating traceability, dual acceptance, invariant binding, ambiguity handling, and QA handoff. It defines structure, field descriptions, and completion expectations only — no APIs, schemas, frameworks, implementation, vendor/model choices, coding standards, deployment, infrastructure, or testing tooling. Source specs govern.*

**Release 1 Implementation Contract Template v1 complete.**
