# QA Contract Specification v1

**Document Type:** Contract Specification (structure only — delivery architecture) · **Status:** Draft · **Date:** 2026-05-31
**Subordinate to / consistent with (authoritative — must not redefine):** `AI_FIRST_PRODUCT_DELIVERY_ARCHITECTURE_V1.md` (Layer 5) · `IMPLEMENTATION_CONTRACT_SPECIFICATION_V1.md` · `RELEASE_1_UX_PRODUCT_BACKLOG_V1.md` · `RELEASE_1_UX_EXECUTION_PLAN_V1.md` · `RELEASE_1_UX_SCOPE_FREEZE_AND_BACKLOG_CONTROL_SPECIFICATION_V1.md`.

> **Non-negotiable constraints.** This is a **contract specification only** — it defines **what a QA Contract contains and how it behaves**, not how testing is implemented. It must **NOT** define: APIs, test frameworks, CI/CD, automation implementation, coding standards, databases, infrastructure, observability implementation, vendors, or model choices. **The QA Contract validates what was built; it does not describe how testing is implemented.** Source specs govern.

---

## Architectural Position

```text
Source Spec → Backlog Story → Implementation Contract → AI Implementation → QA Contract → Validation Results → Human Review
```

The QA Contract is the **Layer 5 validation artifact**. It exists to **prevent implementation systems from validating themselves**: implementation and validation are **separate architectural artifacts**, derived independently from the same source understanding. An increment is trusted only after a QA Contract — not the implementer — confirms it.

## A. Purpose

Define the canonical structure of a **QA Contract**: the machine-consumable, human-reviewable validation artifact that determines whether an implementation satisfies its **Implementation Contract requirements, source specification conformance, source specification fail conditions, cross-surface invariants, and regression requirements.**

**Why QA Contracts exist:** to make validation **independent, traceable, and source-governed** — so correctness is proven against the *same* understanding the work was derived from, by an artifact the implementer does not own.

**How they differ:**
- **vs. user stories** — a story communicates intent to humans; a QA Contract states **what must be validated**, objectively and traceably.
- **vs. Implementation Contracts** — the Implementation Contract defines **what should be built**; the QA Contract defines **how correctness is validated** (the executable validation of the Implementation Contract's acceptance, fail conditions, and invariants).
- **vs. Observability Contracts** — a QA Contract validates the increment **before trust/release**; an Observability Contract defines what must be **observed after release** (§L).

## B. QA Philosophy

- **Source specs govern** — validation requirements derive from canonical specs and the Implementation Contract; never invented.
- **Validation must be traceable** — every requirement resolves to a source spec/conformance/fail-condition/contract/invariant.
- **Positive and negative validation are both required** — proving presence of required behavior **and** absence of forbidden behavior.
- **Invariants are first-class** — applicable cross-surface invariants are bound and validated.
- **Validation must not invent requirements** — anything untraceable is invalid.
- **Ambiguity is surfaced, not resolved** — validation flags gaps/conflicts; it does not settle them.
- **Validation proves behavior, not implementation** — a QA Contract asserts observable behavior, never a technique/technology.

## C. QA Contract Lifecycle

```text
Implementation Contract → QA Contract → Validation Execution → Evidence Collection → Human Review → Accepted / Rejected / Needs Clarification
```

- A QA Contract is **derived from** the Implementation Contract (and its sources), **independently** of the implementation.
- **Validation execution** checks positive, negative, invariant, state, and regression requirements (mechanics out of scope).
- **Evidence** is collected, sufficient for human review (§J).
- **Human review** yields **Accepted / Rejected / Needs Clarification**; failure/ambiguity/conflict routes to owner reconciliation and may re-enter Layer 2 understanding.

## D. Required QA Contract Fields

Every QA Contract MUST contain:
1. **QA Contract ID** (stable; resolves to one Implementation Contract).
2. **Linked Implementation Contract** (the bound IC ID).
3. **Source Story** (backlog US-#.#).
4. **Epic** (EP-##).
5. **Source Specifications** (canonical spec(s)).
6. **Validation Scope** (what this contract validates / does not).
7. **Positive Validation Requirements** (§F).
8. **Negative Validation Requirements** (§G — mandatory).
9. **Invariant Validation Requirements** (§H).
10. **State Validation Requirements** (normal/lifecycle states).
11. **Empty-State Validation Requirements** (each distinct empty case).
12. **Failure-State Validation Requirements** (each distinct failure case).
13. **Regression Validation Requirements** (§I).
14. **Evidence Requirements** (§J).
15. **Dependencies** (upstream contracts/surfaces).
16. **Ambiguities** (surfaced, not resolved).
17. **Human Review Requirements** (§K).
*(Additional fields permitted if traceable: e.g., construct type, deferred-scope exclusions, TBD-value markers.)*

A QA Contract missing any required field is **incomplete** (§M) and **fails** (§O).

## E. Traceability Rules

Every validation requirement MUST trace to: **source specification · source conformance item (positive) · source fail condition (negative) · the linked Implementation Contract · applicable invariant(s).** Traceability is **bidirectional**: the QA Contract cites its sources, and each validation requirement resolves to a specific source clause. **Validation may not invent requirements** — anything not traceable is **invalid** and removed or escalated as an ambiguity. The QA Contract validates **exactly** the Implementation Contract's obligations, no more and no less.

## F. Positive Validation Model

Positive validation proves **required behavior exists**:
- **Objective validation** — behavior is asserted in observable, non-numeric terms (unless an owner-supplied value is bound).
- **Acceptance validation** — each Implementation-Contract positive acceptance (AC-#) → one positive validation requirement, traced to the source `*-C#`.
- **State validation** — required normal/lifecycle states are present and behave per spec.
Positive validation confirms the increment **does what the contract requires**.

## G. Negative Validation Model

Negative validation proves **forbidden behavior is absent** — treated as **equal in importance** to positive validation. Each Implementation-Contract negative acceptance (NA-#) and applicable fail condition → one negative validation requirement. Examples (must be proven absent):
- Recommendation Panel opens **outside** Finding context.
- Confidence **shown as a score** (or project health/readiness/probability).
- Assessment **changes without reanalysis**.
- (and every other applicable source fail condition / invariant negative.)

**A QA Contract without negative validation is invalid.** Positive-only validation permits invariant and scope drift to pass undetected; absence-of-forbidden-behavior is a required proof.

## H. Invariant Validation

Applicable Release 1 invariants MUST be **bound** and validated (as negative/absence proofs and, where relevant, positive guarantees):
- **only reanalysis changes assessment**
- **Recommendation only in Finding context**
- **Confidence never health/score**
- **stale never current**
- **history append-only**
- **Chat and Companion not destinations**
- **Export packages existing understanding only**
- **Awareness creates no tasks**
- **Invite/share no permission enforcement**
- **no forbidden capabilities**
- (and **classify-before-specifying** as a governance check where a new construct could appear).

An invariant that applies to the surface but is **unbound** in the QA Contract makes it **invalid** (§O). Invariant validation is owned centrally (EP-16) and referenced per surface, so coverage is both system-level and local.

## I. Regression Validation

**Regression validation proves previously validated behavior remains valid after changes.** A QA Contract's regression requirements MUST:
- **preserve source conformance** (previously-passing `*-C#` still pass);
- **preserve invariants** (bound invariants still hold);
- **preserve routing** (entry/exit/journey rules, incl. Recommendation-only-in-Finding-context, unchanged);
- **preserve state behavior** (analysis/stale/reanalysis/empty/failure states unchanged).
Regression scope expands when a change touches shared surfaces/invariants (e.g., a change near Panels re-runs the Recommendation-context regression suite). Regression validation is **required**, not optional, for any change to an already-validated surface.

## J. Evidence Requirements

A QA Contract MUST define the **validation evidence** required, **sufficient for human review**:
- **Acceptance evidence** (positive requirements satisfied).
- **Negative evidence** (forbidden behaviors proven absent).
- **Invariant evidence** (bound invariants validated).
- **Regression evidence** (preserved behavior confirmed).
Evidence is **described as what must be produced**, not how it is produced — **no tooling, framework, or automation mechanics** are defined. Evidence must let a human reviewer judge Accepted/Rejected/Needs-Clarification without re-running the work.

## K. Human Review Requirements

Human review is **mandatory** when:
- **QA failure** (any positive/negative/invariant/regression requirement fails);
- **ambiguity** (the QA Contract's ambiguity register is non-empty);
- **invariant failure** (a bound invariant is violated);
- **regression failure** (previously-validated behavior broke);
- **source conflict** (specs/contract disagree).
**Humans approve; machines validate.** Review authority and outcome ownership are human; the QA Contract produces evidence and a recommendation, never an autonomous accept.

## L. Relationship to Observability Contracts

Separation of the three contracts:
- **Implementation Contract** — *what should be built.*
- **QA Contract** — *what must be validated* (before trust/release).
- **Observability Contract** — *what must be observed after release.*

The QA Contract hands off to an Observability Contract for the released increment. *(Observability Contract structure is **not** defined here — it belongs to `Runtime Observability Contract Specification v1`.)*

## M. Contract Completion Criteria

A QA Contract is **complete only when** it includes: a **linked Implementation Contract**; **traceable source references**; **positive validation**; **negative validation**; **bound applicable invariants**; **state, empty-state, and failure-state validation**; **regression validation**; **evidence requirements**; **dependencies**; an **ambiguity register**; and **human-review requirements**. Missing any → incomplete → not eligible to validate.

## N. Deferred Items

Explicitly **deferred / out of scope:** testing tools; frameworks; automation tooling; CI/CD; infrastructure; vendors; and implementation mechanics. This document defines the **QA Contract**, not the test suite, runner, or pipeline.

## O. Conformance Requirements

A valid QA Contract MUST pass; it **fails** if it:
- **traceability missing** (any requirement not resolvable to a source clause/contract);
- **negative validation missing** (positive-only — invalid);
- **invariant validation missing** (an applicable invariant unbound);
- **invented requirements** (validation not derived from a canonical source/contract);
- **implementation details included** (frameworks/CI/CD/tooling/vendor/coding);
- **ambiguity silently resolved** (a gap/conflict settled rather than surfaced);
- **source conflict ignored** (validates around a conflict instead of escalating).

**Explicit fail conditions.** A QA Contract is invalid if it: is missing any required field (§D/§M); cannot trace a requirement to its source/contract; contains positive without negative validation; omits an applicable invariant; invents requirements; embeds implementation/tooling detail; resolves an ambiguity or conflict without owner reconciliation; or fails to include regression validation for a change to an already-validated surface.

## P. Output Format

This specification uses formal OSLO specification style, mirroring `IMPLEMENTATION_CONTRACT_SPECIFICATION_V1.md`: **source-governed, invariant-bound, implementation-neutral**, with **positive and negative conformance requirements**. It defines the QA Contract artifact and its behavior; it specifies no testing technology, framework, pipeline, or tooling.

---

*This specification defines the canonical structure of a QA Contract — the Layer 5 validation artifact that determines whether an implementation satisfies its Implementation Contract, source conformance, source fail conditions, cross-surface invariants, and regression requirements. It establishes the QA Contract's architectural independence (implementation and validation are separate artifacts so implementation systems cannot validate themselves), the QA philosophy (source specs govern; validation traceable; positive and negative both required; invariants first-class; requirements never invented; ambiguity surfaced not resolved; validation proves behavior not implementation), the lifecycle, the required fields, bidirectional traceability rules, the positive validation model (required behavior exists), the negative validation model (forbidden behavior absent — a QA Contract without negative validation is invalid), invariant binding and validation, a dedicated regression-validation model (preserve conformance, invariants, routing, and state behavior), evidence requirements sufficient for human review, mandatory human-review triggers, the separation from Implementation and Observability Contracts, completion criteria, and conformance fail conditions. It defines the contract only — no APIs, test frameworks, CI/CD, automation implementation, coding standards, databases, infrastructure, observability implementation, vendors, or model choices.*

**QA Contract Specification v1 complete.**
