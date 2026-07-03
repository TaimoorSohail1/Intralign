# Implementation Contract Specification v1

**Document Type:** Contract Specification (structure only — delivery architecture) · **Status:** Draft · **Date:** 2026-05-31
**Subordinate to / consistent with (authoritative — must not redefine):** `AI_FIRST_PRODUCT_DELIVERY_ARCHITECTURE_V1.md` (Layer 3) · `RELEASE_1_UX_PRODUCT_BACKLOG_V1.md` · `RELEASE_1_UX_EXECUTION_PLAN_V1.md` · `RELEASE_1_UX_SCOPE_FREEZE_AND_BACKLOG_CONTROL_SPECIFICATION_V1.md` · `RELEASE_1_UX_HANDOFF_PACKAGE_SPECIFICATION_V1.md` · `UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION_001.md`.

> **Non-negotiable constraints.** This is a **contract specification only** — it defines **what an Implementation Contract contains and how it behaves**, not how any system is built. It must **not** define: APIs, database schemas, implementation details, frameworks, coding standards, model/vendor choices, deployment architecture, UI styling, QA automation implementation, or observability tooling. **The contract defines what must be communicated to an AI implementation system, not how that system is built.** Source specs govern.

---

## A. Purpose

Define the canonical structure of an **Implementation Contract**: the **machine-consumable artifact** that translates **validated product understanding** into AI-executable implementation work (Layer 3 of the AI-First Product Delivery Architecture).

**Why they exist / how they differ from user stories.** A **user story communicates intent to humans** — it tolerates interpretation and assumes a human will fill gaps sensibly. An **Implementation Contract preserves intent for machines and humans** — it makes intent, acceptance, **forbidden behavior**, and **invariants** explicit and traceable, so an AI implementation system can act on the *same* understanding the spec encodes, without interpretation drift. The contract is the lossless carrier across the human→machine boundary: it does not re-describe the work narratively; it **binds** the work to its source understanding, its acceptance, and its constraints.

## B. Contract Philosophy

- **Source specs govern** — a contract carries intent from canonical specs; it never originates intent.
- **Intent must be traceable** — every contract resolves to its source spec/section, conformance, fail condition, backlog story, and invariants.
- **Acceptance must be explicit** — required behavior is stated as testable acceptance, not implied.
- **Negative constraints are first-class** — forbidden behavior and fail conditions travel with the contract, equal to positive acceptance.
- **Invariants must travel with the work** — applicable cross-surface invariants are bound to every contract.
- **Ambiguity must be surfaced, not guessed** — gaps/conflicts are flagged, never silently resolved.
- **AI implementation must not silently resolve conflicts** — conflicts escalate to owner-ratified reconciliation.
- **Human approval remains required** — a machine implements and proposes; a human approves and owns.

## C. Contract Lifecycle

```text
Source Spec / Backlog Story
  → Implementation Contract
    → AI Implementation Attempt
      → QA Contract Validation
        → Human Review
          → Accepted / Rejected / Needs Clarification
            → Backlog or Spec Update (if needed)
```

- A contract is **derived** from a canonical source spec and backlog story (Layer 2 understanding).
- An AI implementation system **attempts** the work strictly within the contract.
- The increment is **validated** against the bound QA Contract (positive + negative).
- A **human reviews**; the outcome is **Accepted / Rejected / Needs Clarification**.
- **Needs Clarification / conflict / deferred-scope** → owner reconciliation; **Backlog or Spec Update** re-enters Layer 2 understanding (the delivery loop). No state advances on guessed understanding.

## D. Required Contract Fields

Every Implementation Contract MUST contain (structure, not implementation):
1. **Contract ID** (§ traceable; resolves to one story/epic/spec).
2. **Source story ID** (backlog US-#).
3. **Epic ID** (EP-##).
4. **Source spec references** (canonical spec(s)).
5. **Source spec section(s)** (the governing sections).
6. **Construct type** (per the ratified taxonomy).
7. **User intent** (the "so that" — the outcome the work serves).
8. **Functional scope** (what the increment must accomplish).
9. **Explicit out-of-scope boundaries** (what it must not accomplish).
10. **Required behaviors** (positive obligations).
11. **Forbidden behaviors** (negative obligations — first-class).
12. **Acceptance criteria** (positive, objective; from source conformance).
13. **Negative acceptance criteria** (from source fail conditions; required).
14. **Cross-surface invariants** (applicable §G).
15. **Routing/context rules** (entry/exit, context preservation; e.g., Recommendation only in Finding context).
16. **State requirements** (analysis/stale/reanalysis/lifecycle states).
17. **Empty states** (each distinct case).
18. **Failure states** (each distinct case; honest/recoverable/non-fabricating).
19. **Dependencies** (upstream contracts/epics).
20. **Deferred items** (explicit out-of-Release-1 boundaries).
21. **Ambiguities / owner questions** (the ambiguity register; TBD values).
22. **Human review requirements** (when review is mandatory, §J) **and QA contract handoff** (the bound QA Contract reference, §L).

A contract missing any required field is **incomplete** (§K) and **fails conformance** (§N).

## E. Source Traceability Rules

Every contract MUST trace back to: **source spec · source section · source conformance requirement (positive) · source fail condition (negative) · backlog story · applicable cross-surface invariant(s).** Traceability is **bidirectional**: the contract cites its sources, and each obligation in the contract resolves to a specific source clause. **No implementation contract may invent intent** — anything not derivable from a canonical source (within its bounds) is an **ambiguity** to flag (§F), not a decision to make. A contract whose obligations cannot be traced to a source clause **fails** (§N).

## F. Ambiguity Handling

When the AI implementation system encounters any of the following, it MUST **not guess** and MUST **not implement around** the ambiguity — it **flags for owner clarification or reconciliation**:
- **Source specs conflict** → escalate to owner-ratified reconciliation (source-governs precedence; Scope Freeze §K).
- **Source spec is silent** → flag; do not infer intent.
- **Story lacks enough detail** → flag for clarification (or design-time decision only if the spec explicitly leaves it open).
- **Acceptance criteria conflict** → escalate.
- **Implementation requires a deferred capability** → stop; deferred scope enters only by owner decision.
- **A new construct appears** → stop; **classify before specification** (no un-typed construct).

**Rule:** *Do not guess. Do not implement around the ambiguity. Flag for owner clarification or reconciliation.* The ambiguity is recorded in the contract's **Ambiguities / owner questions** field (D-21) and blocks completion until resolved.

## G. Invariant Binding

Every contract MUST carry the **applicable** Release 1 invariants (bound, not optional), especially:
- **only reanalysis changes assessment**
- **Recommendation Panel only in Finding context**
- **Confidence is trust in understanding, never project health/readiness/probability/score**
- **stale means previous analysis, never current**
- **history append-only**
- **Chat and Companion are not destinations**
- **Export packages existing understanding only**
- **Awareness creates no tasks/obligations**
- **Invite/share defines no permission enforcement**
- **no forbidden capabilities** (governance/execution/automation/agents/approvals/task/permissions-enforcement/billing/notification-infra)
- **classify before specifying**

Bound invariants appear as **negative acceptance** (must-not-occur) and are validated by the QA Contract. A contract that omits an applicable invariant **fails** (§N).

## H. Acceptance Model

Acceptance is **dual and both-required**:
- **Positive acceptance** proves the **required behavior exists** (from source conformance `*-C#`).
- **Negative acceptance** proves the **forbidden behavior is absent** (from source fail conditions + bound invariants).

**The contract is incomplete without negative acceptance.** Positive-only acceptance is non-conformant (§N) — a contract that only proves presence, not absence, permits invariant drift. Acceptance is **objective and non-numeric** unless an owner-supplied value is bound (recorded as TBD until supplied).

## I. AI Implementation Boundaries

An AI implementation system **MAY:**
- implement **within** the contract;
- generate code **consistent with** the contract;
- **propose clarifying questions**;
- produce **implementation notes**;
- produce **validation evidence** (against the QA Contract).

An AI implementation system **MAY NOT:**
- change product scope;
- **reinterpret source intent**;
- introduce **deferred capabilities**;
- **resolve conflicts silently**;
- **create new constructs**;
- **violate invariants**;
- **treat assumptions as decisions** (an assumption is an ambiguity to flag, never a settled fact).

These boundaries are part of the contract's meaning: an increment produced outside them is rejected at review regardless of apparent correctness.

## J. Human Review Requirements

Human review is **required**:
- **before implementation starts** if ambiguity exists (the ambiguity register is non-empty);
- **after implementation completes** (every increment is reviewed before acceptance);
- when **invariant risk** appears;
- when **source conflict** appears;
- when **deferred scope** is requested;
- when **QA fails.**

Review authority is human (machines propose; humans approve/own). Review outcomes feed the lifecycle (§C): Accepted / Rejected / Needs Clarification.

## K. Contract Completion Criteria

An Implementation Contract is **complete only when** it includes: **traceable source references · required behavior · forbidden behavior · acceptance criteria · negative acceptance criteria · applicable invariants · dependencies · empty/failure states · deferred boundaries · ambiguity register · QA handoff.** Missing any → incomplete → not eligible for implementation.

## L. Relationship to QA Contract

The Implementation Contract **hands off to a QA Contract**: the Implementation Contract defines **what should be built** (required behavior, forbidden behavior, acceptance, invariants); the **QA Contract defines how correctness is validated** (the executable validation of those acceptance and negative criteria). The handoff reference (D-22) binds them. *(QA Contract structure is **not** defined here — it belongs to `QA Contract Specification v1`, per the architecture's future-specs list.)*

## M. Deferred Items

Explicitly **deferred / out of scope:** implementation methods; frameworks; APIs; schemas; test-automation mechanics; CI/CD; observability instrumentation; deployment validation; model/vendor choice. This document defines the **contract**, not the build, the tests, or the pipeline.

## N. Conformance Requirements

A valid Implementation Contract MUST satisfy the following; it **fails** if it:
- **lacks source traceability** (any obligation not resolvable to a source clause; §E);
- **omits negative acceptance** (positive-only; §H);
- **omits applicable invariants** (§G);
- **invents scope** (intent not derivable from a canonical source; §E);
- **includes deferred capabilities** (without owner promotion; §F);
- **resolves ambiguity without owner decision** (guesses or implements around a gap/conflict; §F);
- **introduces implementation details** (APIs/schemas/frameworks/coding/vendor; constraints block);
- **violates source specs** (contradicts a governing spec rather than escalating; §F).

**Explicit fail conditions.** A contract is invalid if it: is missing any required field (§D/§K); cannot trace an obligation to its source; contains positive acceptance without negative acceptance; omits an applicable Release 1 invariant; invents or expands scope; embeds a deferred/forbidden capability; settles an ambiguity or conflict without owner reconciliation; introduces implementation/technology detail; or contradicts a canonical source spec.

## O. Output Format

This specification is written in formal OSLO specification style: structure-only, source-governed, invariant-bound, with explicit positive and negative acceptance and conformance fail conditions. It defines the Implementation Contract artifact and its behavior; it specifies no implementation, technology, vendor, or tooling.

---

*This specification defines the canonical structure of an Implementation Contract — the machine-consumable Layer 3 artifact that translates validated product understanding into AI-executable work while preserving intent. It distinguishes the contract from a user story (a story communicates intent to humans; a contract preserves intent for machines and humans), sets the contract philosophy (source specs govern; intent traceable; acceptance explicit; negative constraints first-class; invariants travel with the work; ambiguity surfaced not guessed; conflicts never silently resolved; human approval required), the contract lifecycle, the twenty-two required fields, bidirectional source-traceability rules, ambiguity-handling rules (do not guess, do not implement around, flag for owner clarification or reconciliation), invariant binding, the dual positive-and-negative acceptance model (a contract is incomplete without negative acceptance), AI implementation boundaries (may implement within and propose; may not reinterpret intent, introduce deferred scope, resolve conflicts silently, create constructs, violate invariants, or treat assumptions as decisions), human-review requirements, completion criteria, the handoff to a QA Contract, and conformance fail conditions. It defines the contract only — no APIs, schemas, frameworks, coding standards, model/vendor choices, deployment architecture, styling, QA-automation implementation, or observability tooling.*

**Implementation Contract Specification v1 complete.**
