# Release 1 UX Execution Plan v1

**Document Type:** Execution Plan (planning only — UX scope) · **Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Consolidates / consistent with and subordinate to (authoritative — must not redefine):** `RELEASE_1_UX_HANDOFF_PACKAGE_SPECIFICATION_V1.md` · `RELEASE_1_UX_IMPLEMENTATION_READINESS_REVIEW_001.md` · `RELEASE_1_UX_SCOPE_FREEZE_AND_BACKLOG_CONTROL_SPECIFICATION_V1.md` · `RELEASE_1_UX_EXECUTION_PLANNING_PACKAGE_V1.md` · `RELEASE_1_UX_FINAL_CONSISTENCY_AUDIT_002.md` · `UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION_001.md` · the three ratified reconciliation decisions · and the canonical UX spec set (Handoff §D).

> **Non-negotiable constraints.** Planning only. **Redefines no UX surface**; introduces **no** APIs, events, implementation details, schemas, styling, governance, execution, automation, agents, permissions enforcement, billing implementation, notification infrastructure, or assessment behavior. Computes/generates/governs/executes nothing; changes no assessment. **Only reanalysis changes assessment.**

> **Required guardrails (binding):** Source specs govern · Release 1 UX scope is **frozen** · only the **canonical active spec set** is in scope · **superseded specs must not be implemented** · **deferred items must not enter Release 1 silently** · **new constructs classified before specification** · **designers/developers may not resolve spec conflicts in implementation** · **Recommendation Panel opens only in Finding context** · **Outcome Confidence is trust in understanding, never project health/readiness/probability** · **stale means previous analysis, never current** · **only reanalysis changes assessment** · **history is append-only in presentation** · **Chat and Companion are not destinations** · **Export packages existing understanding only** · **Awareness creates no tasks or obligations** · **Invite/share defines no permission enforcement.**

---

## A. Purpose

Translate the **frozen** Release 1 UX scope into an execution-ready plan for **design, development, QA, acceptance testing, and backlog control** — epics, sequence, dependencies, invariant tests, per-epic acceptance criteria, definitions of ready/done, and the acceptance boundary — without redefining any surface or introducing implementation.

## B. Scope

**In scope:** execution principles; canonical build scope; deferred guardrails; design/development/QA epic plans; build sequence; dependency map; cross-surface invariant test matrix; per-epic acceptance criteria; backlog intake & scope-control; owner decision/clarification register; drift risks & mitigations; Definition of Ready; Definition of Done; Release 1 acceptance boundary.

**Out of scope:** the actual tickets/test cases; estimation/timeline/staffing; implementation, APIs, events, schemas, styling; governance/execution/automation/agents; permissions enforcement; billing/notification infrastructure; assessment behavior; Release 2 planning.

## C. Execution Principles

- **Source specs govern** — this plan references, never overrides; discrepancies resolve to the surface spec.
- **Scope is frozen** — only Handoff §D is in scope; nothing new without classification + owner decision.
- **Invariants are non-negotiable** runtime guarantees (§K); any ticket violating one is rejected at Definition of Ready.
- **Conformance = acceptance** — each spec's `*-C#` items (positive) and fail conditions (negative) are the tests.
- **Escalate, don't code** — conflicts/gaps go to owner-ratified reconciliation, never implementation choice.
- **Classify before specify** — any new construct is typed under the ratified taxonomy first.

## D. Canonical Build Scope

The build scope is **exactly** the canonical active spec set (Handoff §D), grouped as fifteen surface epics + one cross-surface invariant epic:

Shell & Journey (Global Navigation, Understanding Journey) · Entry & Onboarding (Onboarding, 60-Second Orientation, Orientation State Model) · Project Discovery (Dashboard & List) · Project Overview · MRI (Workspace, Experience, Visualization Model) · Artifact (Workspace, Authoring & Editing Workflow) · Finding Panel · Recommendation Panel · Understanding Companion · OSLO Chat · Collaboration & Sharing (+ Invite & Share Modal) · Notification & Awareness · History & Timeline · Export & Share-Out · Help & Support · Account & Workspace Settings — under the four ratified governing decisions, verified READY by Audit 002.

## E. Out-of-Scope / Deferred Guardrails

**Not in Release 1** (Scope Freeze §E; each spec's Deferred Items): APIs/events/schemas; delivery/notification/document-generation infrastructure; permissions **enforcement**; billing/entitlement implementation; public links; ticketing; restore/rollback & extra export formats; documentation authoring; guided tours; tier upgrade/transactional flow; mobile navigation; shared empty/failure pattern library; and all **Release 2 capabilities** (governance/execution/automation/agents/plugins/integrations — separate classification). Implementing any in Release 1 is a conformance failure; deferred items enter only via §M intake + owner decision.

## F. Design Epic Plan

| ID | Design Epic | Source spec(s) |
|---|---|---|
| DE-1 | App Shell & Navigation | Global Navigation, Understanding Journey |
| DE-2 | Entry & Onboarding | Onboarding, 60-Second Orientation, Orientation State Model |
| DE-3 | Project Discovery | Project Dashboard & List |
| DE-4 | Project Overview | Project Overview |
| DE-5 | MRI Diagnostic Discovery | MRI Workspace/Experience/Visualization Model |
| DE-6 | Artifact Workspace & Editing | Artifact Workspace, Authoring & Editing Workflow |
| DE-7 | Finding & Recommendation Panels | Finding Panel, Recommendation Panel |
| DE-8 | Understanding Companion | Understanding Companion |
| DE-9 | OSLO Chat | OSLO Chat & Clarification |
| DE-10 | Collaboration & Sharing | Collaboration & Sharing, Invite & Share Modal |
| DE-11 | Awareness | Notification & Awareness |
| DE-12 | History & Timeline | History & Timeline |
| DE-13 | Export & Share-Out | Export & Share-Out |
| DE-14 | Help & Support | Help & Support |
| DE-15 | Settings & Tier Visibility | Account & Workspace Settings |

## G. Development Epic Plan

Fifteen matching dev epics (dev-E1…dev-E15, one per DE), each scoped to its source spec's interaction model + conformance, plus **dev-E16 Cross-Surface Invariant Layer** (the §K guarantees implemented as shared runtime rules). No APIs/events/schemas/infrastructure invented (out of scope/deferred).

## H. QA & Acceptance Test Plan

- **QA-1 Per-surface suites:** each `*-C#` conformance → positive test; each explicit fail condition → negative test (template §L).
- **QA-2 Invariant suite:** the §K matrix (system-level).
- **QA-3 State/flow:** orientation/stale/reanalysis transitions; empty/failure states per surface.
- **QA-4 Navigation/journey:** canonical chain; direct jumps; Recommendation-only-in-Finding-context; return/recovery; context preservation.
- **QA-5 Guardrail/negative:** forbidden capabilities; Confidence-as-score/health; stale-as-current; mutable history; Chat/Companion-as-destination; Export-generates-content; Awareness-creates-tasks; Invite-enforces-permissions; object-to-Workspace inflation.

## I. Recommended Build Sequence

1. App Shell & Navigation → 2. Entry & Onboarding + Orientation → 3. Project Discovery → 4. Project Overview → 5. MRI + Artifact → 6. Finding & Recommendation Panels → 7. Companion + Chat → 8. Collaboration/Invite + Awareness → 9. History + Export + Help → 10. Settings & Tier Visibility. **dev-E16 invariant layer + QA suites run throughout.**

## J. Dependency Map

```text
App Shell & Navigation
  ├─ Entry/Onboarding ─ Orientation State ─ Project Discovery ─ Project Overview
  │      └─ Project Overview ─┬─ MRI Workspace ─┐
  │                           └─ Artifact Workspace (CAF overlays) ┤
  │                                                                ▼
  │                                 Finding Panel ─► Recommendation Panel (ONLY in Finding context)
  ├─ Understanding Companion (persists Overview/MRI/Artifact; Top-Rec → Finding → Rec Panel; not a destination)
  ├─ OSLO Chat (floating; routes into surfaces; clarification → reanalysis; not a destination)
  ├─ Collaboration ─ Invite & Share Modal (no permission enforcement) ─ Notification & Awareness (no tasks)
  ├─ History & Timeline (append-only; references retained context)
  ├─ Export & Share-Out (packages existing understanding only)
  ├─ Help & Support (cross-cutting)
  └─ Account & Workspace Settings (periphery)
Cross-cutting: Orientation State Model (stale/reanalysis) → all understanding surfaces; CAF/Reliability v2/Confidence v2 (read-only presentation) → all.
```

## K. Cross-Surface Invariant Test Matrix

| Invariant | Test (pass = holds everywhere) | Coverage |
|---|---|---|
| Only reanalysis changes assessment | no action mutates CAF/Reliability/Confidence or finding/recommendation state | all |
| Recommendation only in Finding context | Rec Panel cannot open without a Finding from any surface/layer | Panels, Companion, Chat, Awareness, History, Export, Journey |
| Confidence = trust, never health/score | no score/%/"health/readiness/probability" rendered | Overview, MRI, Companion, Dashboard, Export, Help |
| Stale never current | stale = "previous analysis"; never current; no implicit reanalysis | Editing, Orientation, Dashboard, Companion, Chat, Awareness, History, Export, Journey |
| Presentation-only resolution constructs | OSLO Recommended / Possible Resolution Paths / Selected Path never objects; alternatives persist | Rec/Finding Panels, Companion, Export |
| History append-only | no delete/mutate/rollback; supersession additive | History, Editing, Panels |
| Chat & Companion not destinations | both remain layers; never primary navigation destinations | Navigation, Journey, Companion, Chat |
| Export packages existing understanding only | export generates no new finding/recommendation/assessment; carries currency marker + disclaimer | Export |
| Awareness creates no tasks/obligations | no task/assignment/workflow; read/unread = presentation only | Awareness |
| Invite/share enforces no permissions | participant types presentation-only; no permission logic/enforcement | Invite Modal, Collaboration, Settings |
| Context preserved | open/close panel/companion/chat/modal/settings never discards context | all |
| No forbidden capabilities | no governance/execution/automation/agents/approvals/task/permissions-enforcement/billing/notification-infra | all |

## L. Per-Epic Acceptance Criteria (template + key per-epic anchors)

**Template (every epic):** structure/IA present · all empty & failure states present and honest (no fabrication) · one positive test per `*-C#` · one negative test per fail condition · relevant §K invariants hold · construct behaves as its classified type · entry/exit routing matches Journey/Navigation with context preserved · threshold tests marked **TBD** until owner values supplied (§N).

**Key per-epic anchors (illustrative, non-exhaustive):**
- **DE/dev-E1 Shell & Nav:** three contexts intact; only Workspaces are destinations; lifecycle reinforced-not-enforced; never stranded.
- **DE/dev-E4 Overview:** confidence presented reliability-qualified, **no score/health**.
- **DE/dev-E5 MRI:** qualitative lenses/heatmap, **no scores**; not a flat list/issue tracker.
- **DE/dev-E6 Artifact/Editing:** edit→save→pending→reanalysis; **editing changes no assessment**; append-only history.
- **DE/dev-E7 Panels:** **Recommendation only in Finding context**; alternatives persist post-acceptance; descriptive findings / advisory recommendations.
- **DE/dev-E8 Companion / E9 Chat:** **not destinations**; Companion Top-Rec routes via Finding; Chat clarifications feed reanalysis, change no assessment.
- **DE/dev-E11 Awareness:** **no tasks/obligations**; read/unread presentation-only; stale honest.
- **DE/dev-E12 History:** **append-only**; prior never shown as current; no rollback.
- **DE/dev-E13 Export:** **packages existing understanding only**; currency marker + disclaimer (understanding, not project health/approval).
- **DE/dev-E10 Invite/Collaboration:** **no permission enforcement**; participant types presentation-only; comments orbit objects.
- **DE/dev-E15 Settings:** visibility-first tiers; **no billing implementation**; periphery, non-assessment.

## M. Backlog Intake & Scope-Control Rules

Per `RELEASE_1_UX_SCOPE_FREEZE_AND_BACKLOG_CONTROL_SPECIFICATION_V1.md`: every new request/deferred-promotion/implementation discovery follows **capture → classify (taxonomy) → scope-test (canonical §D vs deferred §E vs new) → route (clarification §P/conflict §M-escalation/owner-decision) → decide & record.** Deferred items enter Release 1 **only** by owner decision; new constructs are **classified first**; governance/execution/agent capabilities require **future-architecture classification**. Designers/developers **never** resolve conflicts or fill gaps in code — they raise them; **source specs govern**, spec-vs-spec escalates to an owner-ratified reconciliation decision.

## N. Owner Decision / Clarification Register

(Non-blocking to planning; resolve before threshold-dependent tests finalize — from Readiness RR-1…5.)
- **RR-1** Tier Definitions numbers (seats/limits, format gating) — for tier-visibility tests.
- **RR-2** Calibration values (CAF/Confidence/Reliability scales; stale suggested-vs-required; "Top N"; MRI edge-case mapping).
- **RR-3** Private invite link in/out for first build (default optional).
- **RR-4** Construct-type tags per surface spec (hygiene).
- **RR-5** Normalize older UI-layer docs to the Panel model (hygiene / drift-source).
Both prior owner items (classification doctrine, onboarding defaults) are **closed**.

## O. Implementation Drift Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Building a superseded Workspace spec / older UI-layer docs | Plan from §D only; QA-5 negative; normalize UI-layer docs (RR-5). |
| Recommendation opened outside Finding context | dev-E16 + §K test; Panel/Companion/Journey enforcement; negative test. |
| Confidence as score/health | §K test; design guards (DE-4/8/13); negative test. |
| Stale presented as current / implicit reanalysis | §K test across Awareness/History/Export/Companion/Journey. |
| Assessment mutated outside reanalysis | §K system test; per-surface conformance. |
| Mutable history / read-unread implies status | History/Awareness conformance; QA-5. |
| Chat/Companion become destinations | Navigation/Journey conformance; §K test. |
| Export generates content / Awareness creates tasks / Invite enforces permissions | per-surface negative tests; §K rows. |
| Unclassified construct / forbidden-capability creep | classify-before-specify gate (§M); escalate, don't code. |
| Numeric thresholds guessed | mark TBD; supply RR-1/RR-2 before finalizing dependent tests. |

## P. Definition of Ready (for Tickets)

A ticket is **Ready** when it: maps to a **canonical source spec** (§D) with cited sections; uses the spec's **conformance (positive) + fail conditions (negative)** as acceptance criteria; states **construct type + routing/context**; lists the **must-hold invariants** (§K); has needed **numeric values supplied or explicitly TBD** (§N); includes **empty/failure** states; and introduces **no** deferred/forbidden capability (§E) and **no** unclassified construct.

## Q. Definition of Done (Release 1 UX)

Release 1 UX is **Done** when: every canonical surface is implemented to its spec's **structure/states/conformance** (positive + negative tests pass); **all §K invariants** pass; **no superseded spec** implemented and **no deferred/forbidden capability** present; **navigation/journey** matches specs (destinations vs. layers; Recommendation-only-in-Finding-context; context preserved; never stranded); **Confidence never a score/health, stale never current, history append-only, assessment changes only via reanalysis, Chat/Companion not destinations, Export packages-only, Awareness no-tasks, Invite no-enforcement** — all verified; **no spec conflict resolved in code** (all via owner-ratified reconciliation); threshold-dependent tests have owner values (RR-1/RR-2) or are tracked TBD; and the **acceptance boundary (§R)** and **Audit 002** are satisfied.

## R. Release 1 Acceptance Boundary

Release 1 UX is **accepted/complete** when it delivers **exactly** the canonical frozen scope (§D), honoring **all cross-surface invariants** (§K) and **each surface's conformance**, with **nothing deferred (§E) included**, **nothing new added except via §M intake + owner decision**, **no spec conflict resolved in code**, and **no unclassified construct present**. Anything outside this boundary is **out of Release 1** (fast-follow or Release 2). The boundary is the contract between specification and execution; crossing it is a conformance failure.

## S. Deferred Items

Explicitly **deferred / out of scope** for this plan: the actual tickets/stories/test cases (this is the plan, not the backlog); estimation/staffing/timeline/tooling; Release 2 planning; future-architecture classification work; visual design systems and styling; and any numeric/calibration values (owner-supplied, RR-1/RR-2). This is the **execution plan**, not the build, schedule, or backlog tool.

---

*This Release 1 UX Execution Plan converts the frozen, audit-verified (READY) UX scope into an execution-ready plan: fifteen design and development epics (one per canonical surface) plus a cross-surface invariant layer; a QA/acceptance plan built from each spec's objective conformance (positive) and explicit fail conditions (negative); a dependency-first build sequence and dependency map; a cross-surface invariant test matrix; per-epic acceptance criteria; backlog intake and scope-control rules; an owner decision/clarification register; drift risks with mitigations; a Definition of Ready and Definition of Done; and a firm Release 1 acceptance boundary. It binds every guardrail — source specs govern; scope frozen; only canonical specs in scope; superseded specs not implemented; deferred items never enter silently; new constructs classified before specification; conflicts escalated not coded; Recommendation Panel only in Finding context; Confidence is trust in understanding never project health/readiness/probability; stale means previous analysis never current; only reanalysis changes assessment; history append-only; Chat and Companion not destinations; Export packages existing understanding only; Awareness creates no tasks; Invite/share enforces no permissions. It redefines no surface and introduces no APIs, events, implementation, schemas, styling, governance, execution, automation, agents, permissions enforcement, billing, notification infrastructure, or assessment behavior.*

**Release 1 UX Execution Plan v1 complete.**
