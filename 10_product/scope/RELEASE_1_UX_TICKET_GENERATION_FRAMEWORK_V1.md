# Release 1 UX Ticket Generation Framework v1

**Document Type:** Ticket Generation Framework (planning/method only — UX scope) · **Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Authoritative inputs (must not redefine):** `RELEASE_1_UX_PRODUCT_BACKLOG_V1.md` · `RELEASE_1_UX_EXECUTION_PLAN_V1.md` · `RELEASE_1_UX_SCOPE_FREEZE_AND_BACKLOG_CONTROL_SPECIFICATION_V1.md` · `RELEASE_1_UX_HANDOFF_PACKAGE_SPECIFICATION_V1.md` · `UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION_001.md` · all canonical Release 1 UX source specs referenced by the Product Backlog.

> **Non-negotiable constraints.** Planning/method only. This document **defines how tickets are generated; it does not create the ticket inventory.** It must **not** define implementation, APIs, events, schemas, database design, styling, governance, execution, automation, agents, permissions enforcement, billing implementation, notification infrastructure, or assessment behavior. **Source specs govern.** **Only reanalysis changes assessment.** **Recommendation Panel opens only in Finding context.** **Outcome Confidence is trust in understanding, never project health/readiness/probability/score.** **Stale means previous analysis, never current.** **History is append-only in presentation.** **Chat and Companion are not destinations.** **Export packages existing understanding only.** **Awareness creates no tasks or obligations.** **Invite/share defines no permission enforcement.** **New constructs classified before specification.** **Spec conflicts escalated, not resolved in implementation.**

---

## A. Purpose

Convert the epics and user stories in `RELEASE_1_UX_PRODUCT_BACKLOG_V1.md` into a **repeatable framework for generating design, development, and QA tickets** — preserving full **traceability** (ticket → story → source spec section) and **preventing implementation drift** (every ticket carries its invariants, negative criteria, and escalation triggers). This framework defines the **method, structure, fields, decomposition logic, and acceptance/QA mapping**; it does **not** produce the tickets (that is `Release 1 UX Ticket Inventory v1`, next).

## B. Scope

**In scope:** ticket hierarchy; ticket types; required ticket fields; story-to-ticket decomposition rules; acceptance-criteria mapping; negative-acceptance mapping; QA ticket generation; invariant ticket generation; dependency mapping; out-of-scope rules; Definition of Ready; Definition of Done.

**Out of scope:** the actual tickets; estimates; assignees; sprint planning; implementation details; APIs/events/schemas; styling; Release 2 planning.

## C. Ticket Hierarchy

```text
Epic  →  Feature Group  →  Ticket  →  Acceptance Tests
```
- **Epic** — a canonical surface (or the invariant layer) from the Product Backlog (EP-1…EP-16). Owns user value and out-of-scope boundaries.
- **Feature Group (FG)** — a coherent slice of an epic (e.g., "Finding Panel Launch & Context"). Groups related tickets; aids sequencing and review (§L).
- **Ticket (TKT)** — a single execution-ready unit of design/dev/QA work decomposed from one or more user stories, carrying all required fields (§E).
- **Acceptance Tests** — the positive and negative tests attached to a ticket, mapped from source-spec conformance and invariants (§G/§H/§I).

Each level **traces upward** (ticket → FG → epic → backlog story → source spec) and **never** redefines a surface.

## D. Ticket Types

At minimum, the following types (a ticket has exactly one primary type; QA is always paired):
- **UX structure ticket** — required regions/IA of a surface per its architecture section.
- **Interaction behavior ticket** — how a surface responds to user actions (non-mutating unless reanalysis).
- **Routing/navigation ticket** — entry/exit routes, journey transitions, destination-vs-layer rules.
- **State handling ticket** — analysis/stale/reanalysis and lifecycle states.
- **Empty-state ticket** — each distinct empty case (distinguished, honest).
- **Failure-state ticket** — each distinct failure case (honest, recoverable, non-fabricating).
- **Context-preservation ticket** — open/close/transition preserves originating context.
- **Invariant enforcement ticket** — a cross-surface invariant guaranteed at this surface.
- **Negative-path ticket** — a must-not-occur behavior (from fail conditions / invariants).
- **QA acceptance ticket** — the test suite (positive + negative + empty + failure + invariant + regression).

## E. Required Ticket Fields

Every ticket MUST include:
- **Ticket ID** (§K) · **Epic ID** · **Feature Group** · **Source user story** (US-#) · **Source spec** · **Source spec section** · **Construct type** (per the ratified taxonomy) · **User value** · **Scope** · **Out of scope** · **Dependencies** (§M) · **Acceptance criteria** (§G) · **Negative acceptance criteria** (§H) · **Relevant invariants** (§J) · **Empty states** · **Failure states** · **QA notes** · **Deferred / TBD values** (§J owner register) · **Escalation trigger** (§N).

A ticket missing any field is **not Ready** (§O).

## F. Story-to-Ticket Decomposition Rules

Apply to every Product Backlog user story:
1. **Every story produces ≥1 implementation ticket and ≥1 QA ticket.**
2. **Navigation stories** produce a **routing ticket** and a **context-preservation ticket**.
3. **Stale-analysis stories** produce a **stale-state ticket** and a **stale-negative test** (stale-never-current; no implicit reanalysis).
4. **Finding/Recommendation stories** produce **Recommendation-only-in-Finding-context** negative tests where relevant.
5. **Confidence stories** produce **Confidence-not-health / not-score** negative tests.
6. **Export stories** produce **package-structure**, **stale-export**, and **disclaimer** tickets.
7. **Awareness stories** produce **no-task / no-obligation** negative tests.
8. **Invite/share stories** produce **no-permission-enforcement** negative tests.
9. **History stories** produce **append-only** and **prior-not-current** negative tests.
10. **Chat or Companion stories** produce **not-a-destination** negative tests.

*(These are additive: a single story may trigger several rules — e.g., a Companion Top-Recommendation story triggers rules 2, 4, and 10.)*

## G. Acceptance-Criteria Mapping

Each ticket's acceptance criteria are **copied/derived from** (in this precedence):
1. **The source story anchors** (Product Backlog §C acceptance).
2. **The source spec's Conformance Requirements** (`*-C#`) — the authoritative positive tests.
3. **The cross-surface invariant stories** (Product Backlog §D, this framework §J) relevant to the surface.

**The source spec always governs.** Where a story anchor and a spec conformance item differ, the **spec governs**; the ticket cites the spec section. Acceptance is **objective and non-numeric** unless a TBD value is supplied (§J owner register).

## H. Negative-Acceptance-Criteria Mapping

Every ticket MUST include negative criteria derived from:
1. **Explicit fail conditions** in the source spec (the authoritative must-not-occur tests).
2. **Cross-surface invariant negatives** (§J).
3. **Deferred-scope guardrails** (Scope Freeze §E; Product Backlog §I) — the ticket must not implement deferred/forbidden capabilities.
4. **Scope-freeze rules** — no new construct un-classified; no conflict resolved in code; nothing outside canonical scope.

## I. QA Ticket Generation Rules

Each QA acceptance ticket MUST include:
- **Positive-path test cases** (from §G).
- **Negative-path test cases** (from §H).
- **Empty-state tests** (each distinct empty case).
- **Failure-state tests** (each distinct failure case; honest/recoverable/non-fabricating).
- **Invariant tests** (the surface's slice of §J).
- **Cross-surface regression tests** where applicable (e.g., a change near Panels re-runs the Recommendation-only-in-Finding-context suite).

A surface epic is **not Done** until its QA tickets pass positive + negative + empty + failure + invariant.

## J. Invariant Ticket Generation Rules

Generate **invariant enforcement tickets** (and their negative-path twins) for each, mapped onto **every surface where the invariant applies**:
- **INV-1** Only reanalysis changes assessment.
- **INV-2** Recommendation Panel only in Finding context.
- **INV-3** Confidence is trust in understanding, never health/score.
- **INV-4** Stale is previous analysis, never current.
- **INV-5** History append-only.
- **INV-6** Chat and Companion not destinations.
- **INV-7** Export packages existing understanding only.
- **INV-8** Awareness creates no tasks/obligations.
- **INV-9** Invite/share defines no permission enforcement.
- **INV-10** Context preserved across transitions.
- **INV-11** No forbidden capabilities.
- **INV-12** Classify before specifying.

Each invariant ticket lives in **EP-16** as the canonical owner, and is **referenced** by every surface ticket it constrains (so coverage is both centralized and per-surface). Owner-clarification TBDs (RR-1…RR-5) are attached where an invariant test needs a value.

## K. Ticket ID Convention

Implementation/design ticket:
```text
EP-07-FG-02-TKT-003
```
- **EP-##** = epic (EP-01…EP-16) · **FG-##** = feature group within the epic · **TKT-###** = ticket number within the feature group.

QA ticket:
```text
EP-07-FG-02-QA-001
```
- Same epic/feature-group prefix · **QA-###** = QA ticket number within the feature group.

Invariant tickets (owned by EP-16) use the epic prefix and an INV tag, referenced from surface tickets:
```text
EP-16-FG-01-INV-002   (e.g., Recommendation-only-in-Finding-context)
```
IDs are **stable and traceable**; every ticket ID resolves to one epic → feature group → story → source spec.

## L. Feature Grouping Rules

Within each epic, create **Feature Groups (FG-1…FG-n)** that (a) cluster related stories/tickets, (b) end with an empty/failure group and a QA/negative group, and (c) follow the surface spec's own section order where natural. Canonical example —

**EP-7 Finding & Recommendation Panels:**
- **FG-1** Finding Panel Launch & Context
- **FG-2** Finding Explanation Content
- **FG-3** Recommendation Panel Launch Rules *(Finding-context-only)*
- **FG-4** Recommendation Evaluation Content
- **FG-5** Recommendation Actions *(accept/reject/defer; no manual resolve)*
- **FG-6** Reanalysis Outcomes
- **FG-7** Empty / Failure States
- **FG-8** QA & Negative Tests

Every epic ends with an **Empty/Failure FG** and a **QA & Negative FG**; feature groups never cross epic boundaries.

## M. Dependency Rules

Tickets MUST reference upstream dependencies; the ordering constraints:
- **Shell before surfaces** (EP-1 before all).
- **Overview before MRI/Artifact** (EP-4 before EP-5/EP-6).
- **MRI/Artifact before Panels** (EP-5/EP-6 before EP-7).
- **Panels before Companion recommendation routing** (EP-7 before EP-8 Top-Rec routing).
- **Panels before Chat recommendation routing** (EP-7 before EP-9 routing to Recommendation via Finding).
- **Collaboration before Awareness** (EP-10 before EP-11).
- **Retained history before History surface** (EP-6/EP-7/EP-10/EP-11 retention before EP-12).
- **Source context before Export** (EP-4–EP-7 before EP-13).
- **Chat before Help routing to Chat** (EP-9 before EP-14 routing).
A ticket whose dependency is unmet is **blocked**, not started; QA/invariant tickets may proceed in parallel as harnesses.

## N. Escalation Rules

A ticket MUST be **escalated** (to owner-ratified reconciliation per Scope Freeze §K — never resolved in implementation) if it:
- requires a **new construct** (classify first);
- **contradicts a source spec**;
- **introduces deferred scope** (Scope Freeze §E / Product Backlog §I);
- requires **implementation details not specified** (and not derivable within spec bounds);
- would **change assessment outside reanalysis**;
- would **open a Recommendation without Finding context**;
- would **frame Confidence as health or score**;
- would **present stale as current**;
- would **create governance / execution / task / agent behavior**.
The **escalation trigger** field (§E) records which of these applies; an escalated ticket is **not Ready** until reconciled.

## O. Definition of Ready (for ticket generation)

A story is ready to generate tickets when: **source spec known** · **construct type known** · **relevant invariants known** · **empty/failure states known** · **dependencies known** · **deferred scope identified** · **TBD values marked**. Missing any → not Ready (resolve via clarification or escalation first).

## P. Definition of Done (for ticket generation)

Ticket generation is done when: **every story has implementation tickets** · **every story has QA tickets** · **every relevant invariant has enforcement and negative tests** · **every ticket cites source specs (and section)** · **every ticket includes acceptance and negative acceptance** · **deferred items excluded** · **TBD values marked** · **escalation triggers explicit**. (This DoD governs the *generation* of the next artifact, the Ticket Inventory.)

## Q. Deferred Items

Explicitly **deferred / out of scope:** the **actual ticket inventory** (next artifact); estimates; assignees; sprint sequencing; implementation details; APIs/events/schemas; styling; and Release 2 capability planning. This document is the **framework**, not the tickets or the schedule.

---

*This framework converts the Release 1 UX Product Backlog into a repeatable method for generating design, development, and QA tickets without producing the inventory itself. It defines a four-level hierarchy (Epic → Feature Group → Ticket → Acceptance Tests), ten ticket types, the required ticket fields, ten story-to-ticket decomposition rules, acceptance and negative-acceptance mapping (source-spec conformance and fail conditions govern, augmented by cross-surface invariants, deferred guardrails, and scope-freeze rules), QA and invariant ticket-generation rules, a stable traceable ticket-ID convention, feature-grouping rules, dependency ordering, escalation triggers, and Definitions of Ready and Done for ticket generation. It binds every guardrail — source specs govern; only reanalysis changes assessment; Recommendation only in Finding context; Confidence is trust in understanding never health/score; stale never current; history append-only; Chat and Companion not destinations; Export packages existing understanding only; Awareness creates no tasks; Invite/share enforces no permissions; new constructs classified before specification; conflicts escalated not coded — and introduces no implementation, APIs, events, schemas, database design, styling, governance, execution, automation, agents, permissions enforcement, billing, notification infrastructure, or assessment behavior.*

**Release 1 UX Ticket Generation Framework v1 complete.**
