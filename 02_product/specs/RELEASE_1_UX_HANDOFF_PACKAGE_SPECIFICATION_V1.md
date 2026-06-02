# Release 1 UX Handoff Package Specification v1

**Document Type:** Handoff Package Specification (index / governance only — UX/interaction scope)
**Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Consistent with and subordinate to (authoritative — must not redefine):** `RELEASE_1_UX_FINAL_CONSISTENCY_AUDIT_002.md` · `UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION_001.md` · and the full active UX spec set (§D). Also references the Release 1 Tier Definitions and the CAF / Reliability v2 / Confidence v2 models.

> **Non-negotiable constraints.** This package **indexes and packages** the finalized Release 1 UX architecture for design/development handoff. It **redefines no product surface**, **creates no new scope**, and **introduces no implementation details, APIs, events, styling, governance, execution, automation, agents, or assessment behavior.** It computes nothing, generates nothing, governs nothing, executes nothing, and changes no assessment. **Only reanalysis changes assessment.** Where this package and any source spec appear to differ, **the source spec governs** (this is an index, not an authority over surface internals).

> **Position.** This is the **handoff manifest**: it tells designers and developers *which specs are canonical*, *which are superseded*, *what invariants must hold*, *how surfaces are classified and connected*, *what remains as fast-follow*, and *how to escalate conflicts found during build* — so the ratified architecture is implemented without drift.

---

## A. Purpose

Define the canonical Release 1 **UX Handoff Package** — how the finalized UX architecture is packaged for design and development handoff. It answers: **"What does a designer/developer need to receive, treat as canonical, preserve, and escalate, to build Release 1 UX faithfully?"** — without redefining any surface, creating scope, or specifying implementation.

## B. Scope

**In scope:** the handoff manifest — the canonical active spec set; the superseded/out-of-scope set; the designer and developer handoff packages; the cross-surface invariants; the construct-classification map; the navigation/journey map; the fast-follow backlog; conflict-escalation rules; and handoff acceptance criteria.

**Out of scope:** any redefinition of a surface's internals (each source spec governs); new UX scope; implementation, APIs, events, styling, delivery infrastructure, document generation; governance/execution/automation/agents; and any assessment/finding/recommendation generation. This package **points to** the specs; it is not itself a surface spec.

## C. Handoff Philosophy

A clean handoff transfers **decisions, not ambiguity**. The package's job is to make the ratified architecture **unambiguous and traceable**: one canonical set, clearly-marked supersessions, explicit invariants, and a known escalation path so that questions found during build are **reconciled by owner decision**, not silently resolved in code. It preserves the product's spine — **understanding is the center of gravity; only reanalysis changes assessment** — and keeps designers/developers inside the ratified taxonomy and journey. It **adds no scope**: anything not in the canonical set or fast-follow backlog is out of Release 1.

## D. Canonical Active Spec Set (Q2)

The Release 1 UX architecture is **internally consistent and handoff-ready** (`RELEASE_1_UX_FINAL_CONSISTENCY_AUDIT_002.md` — READY). The canonical active specs:

**Shell & connective layer**
- `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1.md`
- `UNDERSTANDING_JOURNEY_AND_SURFACE_TRANSITION_EXPERIENCE_SPECIFICATION_V1.md`

**Entry & pre-understanding (Workspace Context)**
- `ONBOARDING_AND_PROJECT_CREATION_EXPERIENCE_SPECIFICATION_V1.md` *(Release 1 defaults owner-approved)*
- `PROJECT_DASHBOARD_AND_PROJECT_LIST_EXPERIENCE_SPECIFICATION_V1.md` (Workspace Home / Project List)
- `SIXTY_SECOND_ORIENTATION_WORKFLOW_SPECIFICATION_V1.md` · `ORIENTATION_STATE_MODEL_V1.md`

**Primary understanding Workspaces**
- `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md`
- `MRI_WORKSPACE_SPECIFICATION_V1.md` (+ `MRI_EXPERIENCE_SPECIFICATION_V1.md`, `MRI_MODEL_V1.md` = MRI Visualization Model — MRI umbrella)
- `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` (+ `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW_SPECIFICATION_V1.md`)

**Contextual Panels**
- `FINDING_PANEL_SPECIFICATION_V1.md`
- `RECOMMENDATION_PANEL_SPECIFICATION_V1.md` (opens only in Finding context)

**Companion Surface & Interaction Layer**
- `UNDERSTANDING_COMPANION_SURFACE_EXPERIENCE_SPECIFICATION_V1.md`
- `OSLO_CHAT_AND_CLARIFICATION_EXPERIENCE_SPECIFICATION_V1.md`

**Companion-Surface-class secondary/cross-cutting surfaces**
- `NOTIFICATION_AND_AWARENESS_SURFACE_SPECIFICATION_V1.md`
- `HISTORY_AND_TIMELINE_SURFACE_SPECIFICATION_V1.md`
- `EXPORT_AND_SHARE_OUT_EXPERIENCE_SPECIFICATION_V1.md`
- `HELP_AND_SUPPORT_EXPERIENCE_SPECIFICATION_V1.md`

**Collaboration & periphery**
- `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md`
- `ACCOUNT_AND_WORKSPACE_SETTINGS_EXPERIENCE_SPECIFICATION_V1.md`

**Ratified governing decisions (canonical, binding)**
- `UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION_001.md` — **Ratified · Governing Taxonomy**
- `FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md` — Option A (Panel Model)
- `UNDERSTANDING_COMPANION_RECONCILIATION_DECISION_001.md` — Option B (Finding-Context Entry)
- `MRI_TERMINOLOGY_RECONCILIATION_DECISION_001.md` — MRI umbrella

**Referenced model/tier inputs (authoritative, not UX surfaces):** CAF Assessment · Reliability v2 · Confidence v2 · Release 1 Tier Definitions.

**Audit of record:** `RELEASE_1_UX_FINAL_CONSISTENCY_AUDIT_002.md` (verdict: READY).

## E. Superseded / Out-of-Scope Specs (Q3)

**Superseded (retained, banner-marked — do NOT implement as standalone):**
- `FINDING_WORKSPACE_SPECIFICATION_V1.md` → superseded by **Finding Panel** (Surface Reconciliation 001, Option A).
- `RECOMMENDATION_WORKSPACE_SPECIFICATION_V1.md` → superseded by **Recommendation Panel** (same).
- `RECOMMENDATION_RESOLUTION_PATHS_SPECIFICATION_V1.md` → **RETIRED** (AMB-1 Decision A; "Possible Resolution Paths" is a presentation pattern, not an object).

**Out of UX handoff active scope (other tiers / historical):**
- Model-tier and governance docs (CAF/Reliability/Confidence models, governance/Future-Architecture models) — authoritative **inputs**, not UX surfaces; governed elsewhere.
- Historical audits `RELEASE_1_UX_ARCHITECTURE_CONSISTENCY_AUDIT_001.md` and the non-UX `RELEASE_1_ARCHITECTURE_CONSISTENCY_AUDIT_001/002.md` — **historical record**, not handoff instructions.
- Older UI-layer docs (`RELEASE_1_UI_SPECIFICATION_V1.md`, `UI_SCREEN_INVENTORY.md`) — **not canonical** for the understanding-experience handoff; pending hygiene normalization (UX-O6, §K). Developers should follow the canonical Panel-model specs, not these.

## F. Designer Handoff Package (Q4)

Designers receive (all from §D — references, not new artifacts):
- **The construct-classification map (§I)** and **navigation/journey map (§J)** — the architectural frame.
- **Each surface spec** in §D for its **structure, states, progressive disclosure, empty/failure states** (the *what* and *where*, not visual styling — styling is intentionally undefined).
- **Cross-surface invariants (§H)** — the non-negotiables every screen must honor.
- **Orientation State Model** and **stale-state doctrine** — how analysis/reanalysis/stale states present everywhere.
- **The three ratified decisions** (surface model, companion routing, MRI umbrella) and the **governing taxonomy** — so new screens are classified before being designed.
- **Tier visibility** (Release 1 Tier Definitions) for gating presentation (not entitlement logic).

Designers do **not** receive: styling/branding systems, visual diff tooling, or any implementation — these are deferred or out of scope.

## G. Developer Handoff Package (Q5)

Developers receive (references, not new artifacts):
- **The canonical active spec set (§D)** as the source of truth for behavior/interaction.
- **Cross-surface invariants (§H)** as hard runtime rules — especially **only reanalysis changes assessment**, **Recommendation Panel only in Finding context**, **append-only history**, **presentation-only resolution constructs**, and the **forbidden-capability boundaries**.
- **Construct map (§I)** and **journey/navigation map (§J)** for routing/state architecture (which surfaces are destinations vs. contextual vs. persistent layers).
- **Conformance requirements** in each surface spec (objective pass/fail, non-numeric) as the **acceptance tests** for that surface.
- **Fast-follow backlog (§K)** — what is explicitly *not* in the first build.

Developers do **not** receive (and must not invent): APIs/events/schemas, delivery/notification/document-generation infrastructure, permissions/billing/entitlement implementation, governance/execution/automation/agent systems — these are **out of scope or deferred** and require their own specs (and, for new construct types, classification first).

## H. Cross-Surface Invariants (Q6)

These hold across **every** Release 1 UX surface and must be preserved during design/dev:

- **INV-1.** **Only reanalysis changes assessment** — no surface/interaction changes CAF/Reliability/Confidence or a finding/recommendation state except reanalysis.
- **INV-2.** **Artifacts are the source of truth**; editing changes content only; saving changes no assessment.
- **INV-3.** **Findings are descriptive**; **Recommendations are advisory**; **OSLO Recommended / Possible Resolution Paths / Selected Path are presentation-only** (no Resolution-Path/Clarification/Resolution-Candidate object).
- **INV-4.** **Recommendation Panel opens only in Finding context** (never standalone).
- **INV-5.** **Outcome Confidence = trust in understanding**, reliability-qualified, never bare; **never project health, readiness, or outcome probability**; never a numeric score in UX.
- **INV-6.** **Stale = previous analysis, never current**; stale is surfaced honestly everywhere; navigation/awareness/history/export never present stale as current and never trigger reanalysis implicitly.
- **INV-7.** **History is append-only in presentation**; supersession is additive; no deletion/mutation affordances (restore/rollback deferred).
- **INV-8.** **Context is preserved** across all transitions and panel/overlay open/close.
- **INV-9.** **No forbidden capabilities** in any understanding surface: no governance, execution, automation, agents, approvals, task management, project health, scoring, generated findings/recommendations, direct assessment change, permissions architecture, billing implementation, or notification/delivery infrastructure.
- **INV-10.** **Classify before specifying** — any new construct must be typed under the governing taxonomy before a spec is written.

## I. Construct Classification Map (Q — per ratified taxonomy)

| Surface | Construct type |
|---|---|
| Project Overview · MRI Workspace · Artifact Workspace | **Workspace** (destinations) |
| Finding Panel · Recommendation Panel | **Panel** (contextual; Recommendation only in Finding context) |
| Understanding Companion | **Companion Surface** (persistent read-out/launcher) |
| OSLO Chat | **Interaction Layer** (floating router/explainer) |
| Notification & Awareness · History & Timeline · Export & Share-Out · Help & Support | **Companion-Surface-class** secondary/cross-cutting surfaces (present + route; no structured understanding-actions; not destinations) |
| Workspace Home / Project List · Onboarding · Project Dashboard | **Workspace-context / pre-understanding** surfaces (navigation shell) |
| Account & Workspace Settings | **Periphery** (management; non-assessment) |
| Collaboration & Sharing | **Object-orbiting** collaboration layer (comments orbit objects) |
| Finding · Recommendation | **Understanding Object** (surfaced by Panels; never inflated to Workspaces) |

Only **Workspaces** are destinations; Panels are contextual; Companion/Chat/awareness/history/export/help are persistent or lightweight layers; Objects are surfaced, never destinations.

## J. Navigation / Journey Map (Q — canonical)

```text
Workspace Home → Project Overview → MRI Workspace → Artifact Workspace → Finding Panel → Recommendation Panel
   (select       (understanding     (where are the   (what does the     (why does this   (what could I
    project)      home)             weaknesses?)     content say?)      weakness exist?) consider?)
```
- **Reinforced, not enforced:** direct jumps among Overview/MRI/Artifact once understanding exists; **Finding Panel** from any finding reference; **Recommendation Panel only in Finding context**; only precondition — first understanding requires the initial analysis.
- **Accelerators (not destinations):** **Understanding Companion** (launcher; Top Recommendations route via the associated Finding), **OSLO Chat** (router/explainer), **Notification & Awareness** (routes to source), **History & Timeline** (routes to retained context), **Export & Share-Out** (packages from relevant surfaces), **Help & Support** (cross-cutting guidance).
- **Return/recovery:** inverse chain + jump-to-primary; never stranded; stale honestly surfaced throughout. (Authoritative: `UNDERSTANDING_JOURNEY_…` and `GLOBAL_NAVIGATION_…`.)

## K. Fast-Follow Backlog (Q7)

Tracked as **non-blocking** (do not block Release 1 handoff). Each item, when taken up, gets its **own** spec and (for new constructs) classification first:
- **Invite / Share modal detail** (Collaboration §E intent specced; modal detail pending).
- **Tier-limit / Upgrade UX** (visibility-first present; transactional upgrade flow pending).
- **Mobile navigation / mobile-specific surface behavior** (deferred across specs).
- **Cross-surface empty/failure pattern library** (each spec defines its own; a shared catalog is optional hygiene).
- **Per-surface deferred items** (already enumerated in each spec): restore/rollback & history-excerpt/comments export; support ticketing workflow; CSV/DOCX/image export formats; documentation authoring/CMS; advanced filtering/search/visual diff; notification delivery (push/email).
- **Hygiene (UX-O6):** normalize older UI-layer docs to the Panel model; add a one-line "Construct type:" tag to each surface spec.

Owner items: **both closed** — classification doctrine **ratified**; onboarding defaults **owner-approved**.

## L. Conflict Escalation Rules (Q9)

Conflicts discovered during design/implementation are **reconciled, not silently coded around**, following the established governance pattern:
1. **Stop & flag** — do not unilaterally resolve a conflict between canonical specs or invariants.
2. **Source governs** — if the conflict is package-vs-spec, the **source spec governs**; if spec-vs-spec, escalate.
3. **Reconciliation decision** — author a `*_RECONCILIATION_DECISION_00X.md` (evaluate-only; options; recommendation) — the pattern used for the surface model (Option A), companion routing (Option B), and MRI umbrella.
4. **Owner ratifies** — only the owner selects; apply via banners/edits; clear flags; update the audit of record.
5. **Classify new constructs first** — any newly proposed surface is typed under the governing taxonomy **before** a spec is written (least-powerful classification that fits).
No conflict is resolved by implementation choice alone.

## M. Handoff Acceptance Criteria (Q10)

Handoff is **accepted** when (objective):
- **AC-1.** Designers/developers are working from the **canonical active set (§D)** only; superseded specs (§E) are not implemented as standalone.
- **AC-2.** The **construct map (§I)** and **journey map (§J)** are reflected: only Workspaces are destinations; Panels are contextual; Recommendation opens only in Finding context; Companion/Chat/awareness/history/export/help are layers, not destinations.
- **AC-3.** All **cross-surface invariants (§H)** are honored, verifiable against each surface's **conformance requirements** (the per-spec pass/fail tests).
- **AC-4.** **No forbidden capability** (INV-9) appears in any surface.
- **AC-5.** **Fast-follow items (§K)** are tracked as out-of-first-build, not silently implemented or silently dropped.
- **AC-6.** **No new scope** beyond §D + §K; any new construct was **classified before** specification.
- **AC-7.** The **conflict-escalation path (§L)** is in place; no spec-vs-spec conflict is resolved in code.
- **AC-8.** The **audit of record** (`RELEASE_1_UX_FINAL_CONSISTENCY_AUDIT_002.md`) verdict (READY) and **both closed owner items** are acknowledged.

## N. Integrity Rules

- **HP-1.** This package **indexes**; it **redefines no surface** (source specs govern) and **creates no new scope**.
- **HP-2.** It **introduces no implementation/APIs/events/styling/infrastructure** and no governance/execution/automation/agents/assessment behavior.
- **HP-3.** It preserves **all cross-surface invariants (§H)**; where it appears to differ from a source spec, the **source spec governs**.
- **HP-4.** It keeps the **ratified construct taxonomy and journey** intact; new constructs are **classified before specification**.
- **HP-5.** It tracks fast-follow as **non-blocking**, neither expanding nor dropping scope.
- **HP-6.** It routes conflicts to **owner-ratified reconciliation**, never to implementation choice.
- **HP-7.** It changes **no assessment**; **only reanalysis changes assessment.**

## O. Conformance Requirements

A conforming handoff MUST (objective); it **fails** if any forbidden behavior appears:
- **HP-C1.** Hand off the **canonical active set (§D)** and exclude **superseded specs (§E)** as standalone implementations. **Fail** if a superseded Workspace spec is implemented as a standalone surface.
- **HP-C2.** Reflect the **construct map (§I)** — only Workspaces as destinations; Recommendation Panel only in Finding context (§J). **Fail** if a Panel/layer becomes a destination or a Recommendation opens without Finding context.
- **HP-C3.** Enforce **all invariants (§H)**, verifiable via each surface's conformance tests. **Fail** if any invariant (esp. INV-1/INV-4/INV-5/INV-6/INV-9) is violated.
- **HP-C4.** Track **fast-follow (§K)** as out-of-first-build; **add no new scope** (§ AC-5/AC-6). **Fail** if undefined scope is implemented.
- **HP-C5.** Apply the **conflict-escalation path (§L)** — reconciliation + owner ratification, classify-before-specify. **Fail** if a spec-vs-spec conflict is resolved in code.
- **HP-C6.** Redefine **no surface** and define **no** implementation/APIs/events/styling/governance/execution/assessment (HP-1/HP-2). **Fail** if this package or the handoff introduces any of these.

**Explicit fail conditions.** The handoff **fails** if it: implements a superseded spec as a standalone surface; makes a Panel/layer a destination or opens a Recommendation outside Finding context; violates a cross-surface invariant (assessment changed outside reanalysis, Confidence-as-project-health, stale-as-current, mutable history, a forbidden capability); adds scope beyond §D + §K; specifies a new construct without classifying it first; resolves a spec conflict in code instead of via owner-ratified reconciliation; or introduces implementation/APIs/events/styling/governance/execution/automation/agents/assessment behavior.

## P. Deferred Items

Explicitly **deferred / out of scope** for this package: visual design systems, styling, and branding; implementation, APIs, events, schemas, and infrastructure; the fast-follow surfaces themselves (§K — each needs its own spec); Release 2 constructs (governance/execution/agent/plugin/integration surfaces — separate classification types per the taxonomy §K of the Classification Decision); analytics/telemetry; localization; and any numeric/calibration values. This package is the **manifest**, not the build.

---

*This specification defines the canonical Release 1 UX Handoff Package — the manifest that packages the finalized, audit-verified (READY) UX architecture for design/development handoff without redefining any surface or adding scope. It names the canonical active spec set (shell & journey; entry & pre-understanding; the primary understanding Workspaces Overview/MRI/Artifact; the Finding and Recommendation Panels; the Understanding Companion and OSLO Chat; the Companion-Surface-class Notification, History, Export, and Help surfaces; Collaboration and Settings; and the four ratified governing decisions), marks the superseded set (the former Finding/Recommendation Workspace specs and the retired Resolution Paths spec), and specifies the designer and developer packages, the cross-surface invariants (only reanalysis changes assessment; Recommendation Panel only in Finding context; Confidence as trust in understanding never project health; stale never current; append-only history; presentation-only resolution constructs; no forbidden capabilities; classify before specifying), the construct-classification map, the navigation/journey map, the non-blocking fast-follow backlog, the owner-ratified conflict-escalation path, and objective handoff acceptance criteria. It redefines no surface (source specs govern), introduces no implementation/APIs/events/styling/governance/execution/assessment behavior, creates no new scope, and changes no assessment. Only reanalysis changes assessment.*

**Release 1 UX Handoff Package Specification v1 complete.**
