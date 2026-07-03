# Release 1 UX Execution Planning Package v1

**Document Type:** Execution Planning Package (planning only — UX scope) · **Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Consistent with and subordinate to (authoritative — must not redefine):** `RELEASE_1_UX_HANDOFF_PACKAGE_SPECIFICATION_V1.md` · `RELEASE_1_UX_IMPLEMENTATION_READINESS_REVIEW_001.md` · `RELEASE_1_UX_FINAL_CONSISTENCY_AUDIT_002.md` · `RELEASE_1_UX_SCOPE_FREEZE_AND_BACKLOG_CONTROL_SPECIFICATION_V1.md` · `UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION_001.md` · the three ratified reconciliation decisions · and the canonical UX spec set (Handoff §D).

> **Non-negotiable constraints.** Planning only. This package **redefines no UX surface** and **introduces no** APIs, events, schemas, implementation details, styling, governance, execution, automation, agents, permissions enforcement, billing implementation, notification infrastructure, or assessment behavior. It computes nothing, generates nothing, governs no content, executes nothing, and changes no assessment. **Only reanalysis changes assessment.**

> **Required guardrails (binding):** **Source specs govern.** Release 1 UX is **ready for execution planning.** **Only canonical active specs are in scope**; **superseded specs must not be implemented.** **Recommendation Panel opens only in Finding context.** **Outcome Confidence is trust in understanding — never project health/readiness/probability.** **Stale means previous analysis, never current.** **Only reanalysis changes assessment.** **New constructs must be classified before specification.** **Spec conflicts must be escalated, not resolved in code.**

---

## A. Purpose

Translate the canonical, audit-verified Release 1 UX architecture into an **execution-ready plan** for design, development, QA, and acceptance testing — epics, sequence, dependencies, test plans, and definitions of ready/done — **without** redefining any surface or introducing implementation. It is the bridge from *specification* to *delivery planning*.

## B. Scope

**In scope:** design/development/QA epic breakdowns; recommended build sequence; dependency map; cross-surface invariant test plan; a per-surface acceptance-test template; non-blocking owner clarifications; deferred-scope guardrails; drift risks & mitigations; Definition of Ready (tickets) and Definition of Done (Release 1 UX); execution governance.

**Out of scope:** writing the actual tickets/stories/test cases; implementation, APIs, events, schemas, styling; governance/execution/automation/agents; permissions enforcement; billing/notification infrastructure; assessment behavior; Release 2 planning. This package **plans**; it does not build.

## C. Planning Assumptions

- The canonical set (Handoff §D) is **frozen and handoff-ready** (Audit 002 = READY; Readiness Review = READY).
- **Source specs govern**; this package references, never redefines.
- Each surface spec's **Conformance Requirements** are objective, non-numeric pass/fail — usable directly as acceptance criteria.
- **Cross-surface invariants** (Handoff §H) are the system-level test backbone.
- Styling/visual systems are a **design input to produce**, not a gap.
- Numeric thresholds (tier numbers, calibration) are **TBD pending owner values** (§K) and gate only *threshold-dependent* tests, not planning.

## D. Design Epic Breakdown

| Design Epic | Source specs | Key design outputs (within spec bounds) |
|---|---|---|
| **DE-1 App Shell & Navigation** | Global Navigation, Understanding Journey | nav frame, three-context model, journey transitions, return/recovery |
| **DE-2 Entry & Onboarding** | Onboarding, 60-Second Orientation, Orientation State Model | account/create flows, 60s orientation, analyzing/stale states |
| **DE-3 Project Discovery** | Project Dashboard & List | Workspace Home, recent/pinned, search/filter/sort, archived |
| **DE-4 Project Overview** | Project Overview | understanding home; reliability-qualified confidence read-out (no score) |
| **DE-5 MRI Diagnostic Discovery** | MRI Workspace, MRI Experience, MRI Visualization Model | heatmap, lenses, Missing/Risky/Incomplete, cross-artifact |
| **DE-6 Artifact Workspace & Editing** | Artifact Workspace, Artifact Authoring & Editing Workflow | content-primary surface, CAF overlays, edit→save→pending→reanalysis |
| **DE-7 Finding & Recommendation Panels** | Finding Panel, Recommendation Panel | contextual panels; Recommendation only from Finding; alternatives persist |
| **DE-8 Understanding Companion** | Understanding Companion | persistent read-out; launches; Top-Rec→Finding routing |
| **DE-9 OSLO Chat** | OSLO Chat & Clarification | floating layer; clarification; explain/navigate; handoffs |
| **DE-10 Collaboration & Sharing** | Collaboration & Sharing, Invite & Share Modal | comments orbit objects; invite/share modal; participant types |
| **DE-11 Awareness** | Notification & Awareness | awareness inbox; categories; routing; read/unread |
| **DE-12 History & Timeline** | History & Timeline | append-only timeline; prior/current labeling; routes to retained context |
| **DE-13 Export & Share-Out** | Export & Share-Out | package config; currency marker; disclaimer; view-only link |
| **DE-14 Help & Support** | Help & Support | help layer; concept/contextual help; contact entry |
| **DE-15 Settings & Tier Visibility** | Account & Workspace Settings | periphery; visibility-first subscription/billing/integrations |

## E. Development Epic Breakdown

Same fifteen epics (dev-E1…dev-E15, one per DE), each scoped to the source spec's **interaction model + conformance**, plus:
- **dev-E16 Cross-Surface Invariant Layer (QA-aligned):** shared runtime guarantees — only-reanalysis-changes-assessment; Recommendation-only-in-Finding-context; stale-never-current; append-only history; presentation-only resolution constructs; context preservation; forbidden-capability blocks.

Developers implement from the canonical specs only; **no** APIs/events/schemas/infrastructure are invented (out of scope/deferred — Handoff §G).

## F. QA / Acceptance Test Epic Breakdown

- **QA-E1 Per-surface acceptance suites:** each surface's `*-C#` conformance items → acceptance tests; each **explicit fail condition** → a negative test (template §J).
- **QA-E2 Cross-surface invariant suite:** the §I test plan (system-level).
- **QA-E3 State/flow suites:** orientation/stale/reanalysis transitions; empty/failure states per surface.
- **QA-E4 Navigation/journey suite:** canonical chain, direct jumps, Recommendation-only-in-Finding-context, return/recovery, context preservation.
- **QA-E5 Negative/guardrail suite:** forbidden capabilities (governance/execution/etc.), Confidence-as-score/health, stale-as-current, mutable history, object-to-Workspace inflation.

## G. Recommended Build Sequence

Dependency-first (from Readiness §G):
1. **DE/dev-E1 App Shell & Navigation** (frame everything else routes within).
2. **DE/dev-E2 Entry & Onboarding + Orientation** (reach first understanding).
3. **DE/dev-E3 Project Discovery** (Workspace Home).
4. **DE/dev-E4 Project Overview** (understanding home).
5. **DE/dev-E5 MRI** + **DE/dev-E6 Artifact** (the two primary understanding workspaces).
6. **DE/dev-E7 Finding & Recommendation Panels** (depend on Artifact/MRI context; enforce Finding-context rule).
7. **DE/dev-E8 Companion** + **DE/dev-E9 Chat** (layers over the above).
8. **DE/dev-E10 Collaboration & Invite** + **DE/dev-E11 Awareness** (collaboration loop).
9. **DE/dev-E12 History** + **DE/dev-E13 Export** + **DE/dev-E14 Help** (cross-cutting surfaces).
10. **DE/dev-E15 Settings & Tier Visibility.**
**dev-E16 invariant layer** and **QA suites** run **throughout**, not at the end.

## H. Dependency Map

```text
App Shell & Navigation
   ├─ Entry & Onboarding ─ Orientation State ─ Project Discovery ─ Project Overview
   │        └─ Project Overview ─┬─ MRI Workspace ──┐
   │                             └─ Artifact Workspace ┤
   │                                  (CAF overlays)   │
   │                                                   ▼
   │                                   Finding Panel ──► Recommendation Panel (only in Finding context)
   ├─ Understanding Companion (persists across Overview/MRI/Artifact; Top-Rec → Finding → Rec Panel)
   ├─ OSLO Chat (floating; routes into surfaces; clarification → reanalysis)
   ├─ Collaboration & Sharing ─ Invite & Share Modal ─ Notification & Awareness
   ├─ History & Timeline (references retained context across surfaces)
   ├─ Export & Share-Out (packages from relevant surfaces)
   ├─ Help & Support (cross-cutting)
   └─ Account & Workspace Settings (periphery)
Cross-cutting dependencies: Orientation State Model (stale/reanalysis) → Overview/MRI/Artifact/Companion/Chat/Awareness/History/Export;
Reliability v2 / Confidence v2 / CAF (read-only presentation) → all understanding surfaces.
```

## I. Cross-Surface Invariant Test Plan

| Invariant | Test (pass = holds everywhere) | Coverage |
|---|---|---|
| **Only reanalysis changes assessment** | no edit/save/clarify/navigate/companion/chat/awareness/history/export/share/settings action mutates CAF/Reliability/Confidence or finding/recommendation state | all |
| **Recommendation only in Finding context** | Rec Panel cannot open from Overview/MRI/Artifact/Companion/Chat/Awareness/History/Export without a Finding | Panels, Companion, Chat, Awareness, History, Export, Journey |
| **Confidence = trust, never health/score** | no numeric confidence score/%, no "health/readiness/probability" anywhere | Overview, MRI, Companion, Dashboard, Export, Help |
| **Stale never current** | stale labeled "previous analysis"; no surface presents stale as current or triggers reanalysis implicitly | Editing, Orientation, Dashboard, Companion, Chat, Awareness, History, Export, Journey |
| **Presentation-only resolution constructs** | OSLO Recommended / Possible Resolution Paths / Selected Path never objects/fields; alternatives persist post-acceptance | Rec Panel, Finding Panel, Companion, Export |
| **Append-only history** | no delete/mutate/rollback; supersession additive | History, Editing, Panels |
| **Context preserved** | open/close panel/companion/chat/modal/settings never discards context | all |
| **No forbidden capabilities** | no governance/execution/automation/agents/approvals/task/permissions-enforcement/billing/notification-infra surfaces | all |
| **Artifacts source of truth; edit ≠ assessment** | editing changes content only; reanalysis required to update assessment | Artifact, Editing |

## J. Per-Surface Acceptance Test Template

For each surface, instantiate (objective, non-numeric unless a TBD value is supplied):
- **Structure:** required regions/IA present per the spec's architecture section.
- **States:** empty states (each distinct case) and failure states (each case) present and honest (no fabrication).
- **Conformance (positive):** one acceptance test per `*-C#` requirement (pass = behavior present).
- **Conformance (negative):** one negative test per **explicit fail condition** (pass = forbidden behavior absent).
- **Invariant hooks:** the §I invariants relevant to this surface hold here.
- **Construct conformance:** the surface behaves as its **classified type** (destination only if Workspace; contextual if Panel; persistent/launcher if Companion; floating router if Interaction Layer; awareness/history/export/help as Companion-Surface-class layers).
- **Routing:** entry/exit routes match the Journey/Navigation specs; context preserved.
- **Threshold tests (deferred until values supplied):** any test needing a tier/calibration number is marked **TBD** (§K) and not failed for lack of a value.

## K. Non-Blocking Owner Clarifications

(From Readiness Review — none blocks planning; resolve before threshold-dependent tests are finalized.)
- **RR-1 Tier Definitions numbers** (seats/limits, format gating) — needed for tier-visibility acceptance tests.
- **RR-2 Calibration values** (CAF/Confidence/Reliability scales, stale suggested-vs-required, "Top N", MRI edge-case mapping) — design/calibration-time.
- **RR-3 Private invite link** in/out for first build (default optional).
- **RR-4 Construct-type tags** per surface spec (hygiene).
- **RR-5 Older UI-layer docs** normalization to the Panel model (hygiene / drift-source).

## L. Deferred Scope Guardrails

Do **not** plan into Release 1 (per Scope Freeze §E and each spec's Deferred Items): APIs/events/schemas; delivery/notification/document-generation infrastructure; permissions enforcement; billing/entitlement implementation; public links; ticketing; restore/rollback & extra export formats; documentation authoring; guided tours; tier upgrade/transactional flow; mobile navigation; shared empty/failure pattern library; and all Release 2 capabilities (governance/execution/automation/agents/plugins/integrations — separate classification). Implementing any of these in Release 1 is a conformance failure.

## M. Implementation Drift Risks & Mitigations

| Risk | Mitigation in planning |
|---|---|
| Building a **superseded Workspace spec** or **older UI-layer docs** | Plan from Handoff §D only; QA-E5 negative test; normalize UI-layer docs (RR-5). |
| **Recommendation opened outside Finding context** | dev-E16 + §I test; Journey/Panel/Companion enforcement; negative test. |
| **Confidence shown as score/health** | §I test; DE-4/DE-8/DE-13 design guard; negative test. |
| **Stale presented as current / implicit reanalysis** | §I test across Awareness/History/Export/Companion/Journey. |
| **Assessment mutated outside reanalysis** | INV system test; per-surface conformance. |
| **Mutable history / read-unread implies status** | History/Awareness conformance; QA-E5. |
| **New construct minted unclassified / forbidden capability creep** | Classify-before-specify gate (Scope Freeze §H); escalate, don't code (§P). |
| **Numeric thresholds guessed** | Mark TBD; supply RR-1/RR-2 before finalizing dependent tests. |

## N. Definition of Ready (for Tickets)

A ticket/story is **Ready** when:
- It maps to a **canonical source spec** (Handoff §D) and cites the section(s) it implements.
- Its **acceptance criteria** are the relevant **conformance items** (positive) and **fail conditions** (negative).
- Its **construct type** and **routing/context** behavior are stated (per the taxonomy + Journey).
- The relevant **invariants (§I)** are listed as must-hold.
- Any needed **numeric value** is either supplied (RR-1/RR-2) or explicitly marked **TBD** (test deferred, not guessed).
- It includes **empty/failure** states from the spec.
- It introduces **no** out-of-scope/deferred capability (§L) and **no** unclassified construct.

## O. Definition of Done (Release 1 UX)

Release 1 UX is **Done** when:
- Every canonical surface (Handoff §D) is implemented to its spec's **structure, states, and conformance** (positive + negative tests pass).
- **All cross-surface invariants (§I)** pass system-level QA.
- **No superseded spec** is implemented; **no deferred/forbidden capability** present (§L/§M).
- **Navigation/journey** matches the specs (destinations vs. layers; Recommendation-only-in-Finding-context; context preserved; return/recovery).
- **Confidence is never a score/health; stale is never current; history is append-only; assessment changes only via reanalysis** — all verified.
- **No spec conflict was resolved in code** (all via owner-ratified reconciliation, §P).
- Threshold-dependent tests have their **owner-supplied values** (RR-1/RR-2) or are explicitly tracked as TBD with the gap owned.
- The **audit of record** (Audit 002) and **scope boundary** (Scope Freeze §N) are satisfied.

## P. Execution Governance Rules

- **Source specs govern**; this plan never overrides a surface spec — discrepancies resolve to the spec.
- **Only canonical active specs (§D) are in scope**; **superseded specs are not implemented.**
- **Spec conflicts are escalated, not resolved in code** — route to owner-ratified reconciliation (Scope Freeze §K), source-governs precedence.
- **New constructs are classified before specification** (Classification doctrine); least-powerful classification preferred; governance/execution/agent capabilities → separate future-architecture classification.
- **Deferred items enter only via owner decision** (Scope Freeze §G/§I) — never silently.
- **Designers/developers do not fill gaps or resolve conflicts in implementation** — they raise them.
- **Invariants are non-negotiable** runtime guarantees; any plan/ticket violating one is rejected at DoR.

## Q. Deferred Items

Explicitly **deferred / out of scope** for this package: the actual tickets/stories/test cases (this is the plan, not the backlog); estimation/staffing/timeline; tooling (ticketing/test runners); Release 2 planning; future-architecture classification work; visual design systems and styling; and any numeric/calibration values (owner-supplied per RR-1/RR-2). This package is the **execution plan**, not the build or the schedule.

---

*This package translates the finalized, audit-verified (READY) Release 1 UX architecture into an execution-ready plan. It defines fifteen design and development epics (one per canonical surface) plus a cross-surface invariant layer; QA/acceptance epics built from each spec's objective conformance (positive tests) and explicit fail conditions (negative tests); a dependency-first build sequence (shell → entry/orientation → discovery → overview → MRI + artifact → panels → companion + chat → collaboration/invite + awareness → history + export + help → settings); a dependency map; a cross-surface invariant test plan; a per-surface acceptance-test template; a Definition of Ready and Definition of Done; and execution-governance rules. It binds the guardrails: source specs govern; only canonical active specs are in scope and superseded specs are not implemented; Recommendation Panel opens only in Finding context; Outcome Confidence is trust in understanding, never project health/readiness/probability; stale means previous analysis, never current; only reanalysis changes assessment; new constructs are classified before specification; and spec conflicts are escalated, not resolved in code. It redefines no surface and introduces no APIs, events, schemas, implementation, styling, governance, execution, automation, agents, permissions enforcement, billing, notification infrastructure, or assessment behavior. Non-blocking owner clarifications (tier/calibration values, private-link confirmation, hygiene) are tracked and gate only threshold-dependent tests.*

**Release 1 UX Execution Planning Package v1 complete.**
