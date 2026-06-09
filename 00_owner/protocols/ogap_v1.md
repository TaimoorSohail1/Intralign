# OSLO Governance Acceleration Protocol (OGAP) v1.0

---

## Document Header

- **Document Type:** Governance Protocol (Operative)
- **Category:** Protocol — not a Framework, not a Doctrine, not a Constitution Article
- **Version:** v1.0
- **Authority:** Repository Owner per CLAUDE.md
- **Ratifying Decision:** DL-040
- **Date Ratified:** 2026-05-30
- **Operates Under:** Framework 001, Framework 001A
- **Status:** Operative (Ratified Protocol)

---

## Status Note (Per DL-040 Clarifications)

This document is a **Protocol**, not a Framework. The five clarifications attached to DL-040 establish:

1. OGAP is a Protocol category, not a new Framework.
2. OGAP does not modify Framework 001 or Framework 001A.
3. OGAP operates as a routing and acceleration protocol layered over Framework 001 and Framework 001A.
4. The CLAUDE.md prohibition on creating new Frameworks remains unchanged.
5. OGAP is authorized because it is owner-ratified as a Protocol, not because AI created a new governance Framework.

Frameworks 001 and 001A retain their authority and operate unchanged. OGAP routes governance items into Frameworks 001 and 001A more efficiently; it does not replace their lifecycle stages or Review semantics.

---

## Purpose

Reduce governance cycles by separating discovery from decision-making, enforcing evidence sufficiency checks, standardizing proposal structures, and preventing repeated reconciliation of already-decidable issues.

This protocol applies to all governance activities involving ambiguity resolution, classification decisions, authority decisions, terminology decisions, relationship decisions, adoption decisions, and related architecture governance matters.

---

## Governing Principle

Governance exists to resolve ambiguity.

Once ambiguity has been sufficiently analyzed, governance must transition from discovery to decision.

Do not continue generating reconciliation analyses once evidence sufficiency has been achieved unless new corpus evidence is introduced.

---

## Stage 1 — Governance Triage

Before performing any reconciliation, proposal generation, review, disposition drafting, or recommendation:

Classify the issue into exactly one category:

**A — Classification**

Examples:
- What is Context Plane?
- Layer vs Plane vs Component vs Boundary

**B — Relationship**

Examples:
- Does Ingestion & Transformation operate within Context Plane?
- Does Construct A depend on Construct B?

**C — Authority**

Examples:
- Who owns time semantics?
- Which construct governs identity?

**D — Terminology**

Examples:
- Which definition becomes canonical?
- Which term should be used?

**E — Adoption**

Examples:
- Should a specification be adopted?
- Should a proposal become canonical?

**F — Other**

Only if none of A-E fit.

**Output:**

- Governance Type:
- Why this type fits:
- Evidence required:
- Discovery required? (Yes/No)

Do not draft a proposal yet.

---

## Stage 2 — Discovery Governance

**Purpose:** Determine whether ambiguity actually exists.

**Allowed artifacts:**

- Reconciliation Analysis
- Corpus Evidence Report
- Contradiction Analysis
- Authority Inventory
- Dependency Analysis

**Not allowed:**

- Proposals
- Ratification recommendations
- Dispositions

**Output must conclude with one of:**

1. Ambiguity Confirmed
2. No Ambiguity Found

If ambiguity is not confirmed:

Stop. No proposal may be generated.

---

## Stage 3 — Evidence Sufficiency Gate

Before any proposal may be drafted, answer:

1. Is ambiguity confirmed?
2. Are candidate options known?
3. Is corpus evidence sufficient to distinguish among options?

**Return:**

- Proposal Ready
- OR Reconciliation Needed
- OR Discovery Incomplete

**Rules:**

If any answer is No:

Return: Evidence insufficient. Continue reconciliation. No proposal may be generated.

---

## Stage 4 — Decision Readiness Assessment

Score the issue using:

| Dimension | Range |
|---|---|
| Corpus Coverage | 0–5 |
| Contradiction Clarity | 0–5 |
| Authority Clarity | 0–5 |
| Scope Isolation | 0–5 |

**Total possible score = 20**

**Interpretation:**

| Total Score | State |
|---|---|
| 16–20 | Proposal Ready |
| 10–15 | Reconciliation Needed |
| 0–9 | Discovery Incomplete |

**Output:**

- Corpus Coverage:
- Contradiction Clarity:
- Authority Clarity:
- Scope Isolation:
- Total:
- Decision State:

---

## Stage 5 — Decision Ready Rule

If Decision Readiness Score ≥ 16:

The issue is Decision Ready.

At this point:

- STOP producing reconciliation analyses.
- STOP generating alternative evidence reports.
- STOP re-framing the same ambiguity.
- Proceed directly to Proposal Generation.

Additional reconciliation may only occur if:

- New corpus evidence is introduced.
- Existing evidence is found to be incorrect.
- Owner explicitly requests further reconciliation.

---

## Stage 6 — Proposal Generation

Use the template associated with the Governance Type.

### Type A — Classification Proposal

Structure:

1. Question
2. Candidate Classifications
3. Corpus Evidence
4. Contradictions
5. Proposed Canonical Wording
6. Decision Scope
7. What This Does Not Decide
8. Owner Decision Options
9. Framework 001A Review

### Type B — Relationship Proposal

Structure:

1. Construct A
2. Construct B
3. Candidate Relationships
4. Corpus Evidence
5. Contradictions
6. Proposed Relationship Wording
7. Decision Scope
8. What This Does Not Decide
9. Owner Decision Options
10. Framework 001A Review

### Type C — Authority Proposal

Structure:

1. Authority Domain
2. Existing Authority Attributions
3. Conflicts or Overlaps
4. Proposed Authority Wording
5. Explicit Exclusions
6. Decision Scope
7. What This Does Not Decide
8. Owner Decision Options
9. Framework 001A Review

### Type D — Terminology Proposal

Structure:

1. Term
2. Variants
3. Corpus Evidence
4. Contradictions
5. Proposed Canonical Term
6. Decision Scope
7. Owner Decision Options
8. Framework 001A Review

### Type E — Adoption Proposal

Structure:

1. Artifact Proposed For Adoption
2. Dependencies
3. Impact Analysis
4. Proposed Adoption Wording
5. Decision Scope
6. What This Does Not Decide
7. Owner Decision Options
8. Framework 001A Review

---

## Stage 7 — Review

Review the proposal.

The review must focus only on:

- Evidence quality
- Scope correctness
- Contradictions
- Dependencies
- Risks

The review must not:

- Invent new proposal types
- Introduce new governance questions
- Expand decision scope

---

## Stage 8 — Owner Decision

Owner selects:

- APPROVE
- MODIFY
- DEFER
- REJECT

Only the owner may ratify. AI may not ratify.

---

## Stage 9 — Disposition Processing

Disposition drafting is permitted only after owner approval.

Disposition may include:

- Disposition document
- Decision Log entry
- Changelog entry

Only after explicit owner direction.

---

## Governance Stop Rule

Once an issue reaches:

- Decision Ready
- AND a proposal exists
- AND a review exists

No further reconciliation analyses shall be generated unless:

1. New corpus evidence is introduced.
2. Existing evidence is invalidated.
3. Owner explicitly requests additional reconciliation.

**Default action:** Move to Owner Decision. Do not continue analyzing an already-decidable ambiguity.

---

## Expected Outcome

This protocol is intended to reduce governance cycles from approximately 5–8 iterations to approximately 2–3 iterations by:

1. Separating discovery from decision-making.
2. Enforcing evidence sufficiency.
3. Standardizing proposal structures.
4. Preventing repeated reconciliation of the same ambiguity.
5. Forcing transition from discovery to decision once readiness is achieved.

---

## Relationship to Framework 001 and Framework 001A

OGAP operates as a routing and acceleration layer over Framework 001 and Framework 001A:

- **Framework 001** continues to govern the canonical lifecycle (Backlog Entry → Proposal → Review → Decision → Repository Change → Changelog Entry). OGAP does not modify these stages.
- **Framework 001A** continues to govern Review output schema (Findings / Concerns / Dependencies / Recommendation / Status) and Review states (Accepted / Accepted with Conditions / Rejected / Deferred / Returned for Revision). OGAP constrains Review scope (Stage 7) but does not modify the schema or states.
- **OGAP Stages 1–5** insert before Framework 001's Proposal stage as Discovery + Triage + Gating discipline.
- **OGAP Stage 6** standardizes Proposal structure using Type-specific templates.
- **OGAP Stages 7–9** narrow Review focus and confirm owner-only ratification authority, consistent with Framework 001A and CLAUDE.md.
- **OGAP Stop Rule** prevents re-entry to Discovery without trigger conditions, complementing Framework 001's sequence.

The two Frameworks remain authoritative for their respective scopes. OGAP routes governance items through them more efficiently and prevents iteration overhead from re-analyzing already-decidable ambiguities.

---

## Authority Status

- **CLAUDE.md prohibition on creating new Frameworks:** Unchanged. AI may not create new Frameworks. OGAP is not a Framework; it is a Protocol.
- **AI may not ratify Protocols.** Owner ratification is required (DL-040 satisfies this for OGAP v1.0).
- **AI may apply OGAP discipline** when performing analytical work governed by Framework 001 / Framework 001A, consistent with AI's permitted activities (analysis, consistency checking, conflict identification, recommendation generation).

---

## Operative Effects

Upon ratification as DL-040:

- All future governance items routed through Framework 001 / Framework 001A will be triaged into Types A–E (or F) per Stage 1 before reconciliation, proposal, review, or disposition drafting.
- Discovery and Decision are separated per Stages 2 and 6–9.
- Evidence Sufficiency Gate (Stage 3) and Decision Readiness Assessment (Stage 4) gate proposal drafting.
- Stop Rule (Stage 5 + Governance Stop Rule section) prevents redundant reconciliation cycles.
- Type-specific Proposal Templates (Stage 6) standardize structure.
- Review (Stage 7) is constrained to the five permitted focus areas.

The OGAP v1.0 protocol is operative as of DL-040 ratification.

---

*End of OSLO Governance Acceleration Protocol v1.0.*
