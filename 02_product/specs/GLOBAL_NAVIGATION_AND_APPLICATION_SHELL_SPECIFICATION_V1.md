# Global Navigation & Application Shell Specification v1

**Document Type:** Experience Specification (UX / Interaction Model Only)
**Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Consistent with and subordinate to (authoritative — must not redefine):** `ONBOARDING_AND_PROJECT_CREATION_EXPERIENCE_SPECIFICATION_V1.md` · `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · `MRI_WORKSPACE_SPECIFICATION_V1.md` · `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` · `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW_SPECIFICATION_V1.md` · `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md` · `ACCOUNT_AND_WORKSPACE_SETTINGS_EXPERIENCE_SPECIFICATION_V1.md` · `SIXTY_SECOND_ORIENTATION_WORKFLOW_SPECIFICATION_V1.md` · `ORIENTATION_STATE_MODEL_V1.md` · CAF Assessment · Reliability v2 · Confidence v2 · Release 1 Tier Definitions.

> **Non-negotiable constraints.** This specification defines **UX architecture: the application shell, navigation architecture/hierarchy, workspace/project/cross-workspace/contextual navigation, screen-to-screen transitions, navigation states, empty states, failure states, and progressive disclosure** only. It must **NOT** define: governance, execution, agents, automation, permissions architecture, APIs, events, implementation, styling, workflows already defined elsewhere, calculations, assessment generation, findings generation, or recommendation generation.
>
> **The specification computes nothing. It generates nothing. It governs nothing. Only reanalysis changes assessment.**
>
> **Preserved invariants.** Artifacts remain the **source of truth**. Findings remain **descriptive**. Recommendations remain **advisory**. MRI remains the **diagnostic discovery** experience. **Project understanding remains the center of gravity.** No governance model. No execution model.

---

## A. Purpose

Define the canonical Release 1 **navigation architecture and application shell** for OSLO — the connective tissue that binds every previously ratified experience into one coherent product. It answers:

> **"How do users move through OSLO?"**

This is the **navigation constitution**: the authoritative reference for how every OSLO experience connects, how users move between them, and how context is preserved as they move. It **routes**; it never computes, generates, or governs.

## B. Scope

**In scope:** the application shell; the navigation hierarchy (Workspace / Project / Object contexts); global navigation; workspace navigation; project navigation; the understanding-lifecycle navigation; artifact navigation; contextual (panel) navigation; collaboration, history, and settings navigation entry points; returning-user navigation; navigation/empty/failure states; transitions; and progressive disclosure.

**Out of scope (explicitly):** the **internal behavior** of any destination experience (owned by its own spec, referenced not redefined); governance; execution; agents; automation; permissions architecture; APIs; events; implementation; styling; and any computation/generation. The shell **moves users between experiences and preserves context**; the experiences themselves remain authoritative for what happens inside them.

## C. Navigation Philosophy

Navigation exists to **get users to understanding with the least friction** and to **keep them oriented** as they move. Four commitments:

- **Understanding remains the center of gravity.** Navigation always foregrounds the path to and through project understanding (Orientation → Overview → MRI → Artifact → Panels); management surfaces (settings, account) sit at the periphery.
- **Navigation reduces cognitive load.** A small, stable, predictable structure — the user should always know *where they are*, *what context they're in*, and *how to get back* — never a sprawling menu of modes.
- **Navigation reinforces the understanding lifecycle.** Movement mirrors the ratified flow (discover → contextualize → explain → evaluate), so the structure teaches the model.
- **Navigation never becomes workflow management.** The shell routes between understanding experiences; it is **not** a task board, pipeline, approval queue, or execution console. It coordinates **no work** and governs **nothing**.

## D. Application Shell Architecture

The shell is organized around **three nested navigation contexts**, kept clearly separate so the user always knows their altitude:

```text
┌─ Workspace Context ─────────────────────────────────────────┐
│  Workspace Home · Project List · Create Project · Settings · │
│  Account                                                     │
│   ┌─ Project Context ──────────────────────────────────────┐ │
│   │  Project Overview · MRI Workspace · Artifact Workspace ·│ │
│   │  Collaboration · Activity/History                       │ │
│   │   ┌─ Object Context ─────────────────────────────────┐  │ │
│   │   │  Artifact (in Artifact Workspace) ·              │  │ │
│   │   │  Finding Panel · Recommendation Panel            │  │ │
│   │   └──────────────────────────────────────────────────┘  │ │
│   └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

- **Workspace Context (global):** spans projects — the home, project list, create-project, and the periphery (settings/account). Persistent global navigation lives here.
- **Project Context:** scoped to one open project — moving among Overview, MRI, Artifact, Collaboration, and Activity/History for that project. Project navigation lives here.
- **Object Context:** scoped to a specific object inside a workspace — an artifact in the Artifact Workspace, and the **contextual panels** (Finding, Recommendation). Object navigation is mostly **panels**, not screens (§J).

**Resolution.** **Global navigation** is the always-available frame for moving across the Workspace Context. **Project navigation** appears only inside an open project and moves within the Project Context. **Contextual navigation** (panels) operates inside the Object Context without leaving the project surface. The three never blur: entering a project doesn't lose the global frame; opening a panel doesn't lose the project surface.

## E. Global Navigation Experience

Persistent, always-available global navigation provides:

- **Workspace Home** — the user's landing surface and projects home.
- **Project List** — browse/select projects.
- **Create Project** — start the onboarding/creation flow (per the Onboarding spec).
- **Settings** — enter the settings periphery (per the Settings spec, §M).
- **Account Access** — account/profile entry and sign-out.

**What belongs in global navigation (resolved):** cross-project, always-relevant destinations — Workspace Home, Project List, Create Project, Settings, Account. These are the few stable anchors a user needs from anywhere.

**What does NOT belong in global navigation (resolved):** project-internal destinations (Overview / MRI / Artifact / Collaboration / Activity) — these are **Project Context** and appear only inside an open project; object-level surfaces (Finding/Recommendation Panels) — these are **Object Context** panels; and anything resembling workflow/task/approval/execution management. Global navigation stays small and stable.

## F. Workspace Navigation Experience

- **Project browsing:** the **Workspace Home / Project List** presents the user's projects for selection.
- **Project switching (Q3):** users switch projects by returning to the Project List / Workspace Home and opening another project — switching projects re-enters the **Project Context** for the new project (landing on its Project Overview or last state, §N). Switching is explicit; the user always knows which project they're in.
- **Workspace-level movement / return to home (resolved):** Workspace Home is always reachable from global navigation, returning the user to the **Workspace Context** from anywhere without losing saved project state.

## G. Project Navigation Experience

Within an open project, project navigation moves among:

- **Project Overview** — the understanding home of the project.
- **MRI Workspace** — diagnostic discovery ("where are the weaknesses?").
- **Artifact Workspace** — content context ("what does it say?").
- **Collaboration surfaces** — discussion around understanding (§K).
- **Activity / History surfaces** — recent activity and prior analyses (§L).

**Which experiences are primary vs. secondary (resolved):**

- **Primary:** **Project Overview**, **MRI Workspace**, **Artifact Workspace** — the understanding spine; these are the prominent, first-class project destinations.
- **Secondary:** **Collaboration** and **Activity/History** — important but supporting; reachable in context and from project navigation, but not competing with the understanding spine for primacy.

This ordering reinforces understanding as the center of gravity.

## H. Understanding Lifecycle Navigation

The canonical movement the shell reinforces:

```text
60-Second Orientation → Project Overview → MRI Workspace → Artifact Workspace
→ Finding Panel → Recommendation Panel
```

- **Can users jump directly? (resolved):** **Yes.** After the initial 60-Second Orientation has produced first understanding, users may navigate **directly** to Overview, MRI, or Artifact, and open Panels from the relevant context — the lifecycle is a **recommended path, not a gate**.
- **Is lifecycle order enforced? (resolved):** **No.** Order is **not enforced** beyond the natural precondition that **first understanding requires the initial analysis** (a brand-new project must reach the 60-Second Orientation before there is understanding to navigate). The shell **reinforces** the lifecycle through structure and emphasis; it does not lock steps.
- **How navigation preserves understanding context (resolved):** moving along the lifecycle **carries context forward** — e.g., selecting a weakness in MRI opens the relevant artifact/finding context; opening a Finding Panel keeps the artifact and selection beneath it; returning steps back to the prior context rather than a cold screen (§J).

## I. Artifact Navigation Experience

Consistent with `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` (referenced, not redefined):

- **Artifact switching (Q4):** users switch artifacts within the Artifact Workspace via the artifact list/selector.
- **Artifact hierarchy navigation:** users navigate structural relationships among artifacts where they exist.
- **Previous / Next artifact:** sequential traversal.

Artifact navigation **selects what to view**; it generates nothing and changes no assessment. The detailed model lives in the Artifact Workspace spec; the shell only provides the movement framing.

## J. Contextual Navigation Experience

- **Opening Finding Panels:** a finding (from MRI, an artifact overlay, etc.) opens its **Finding Panel in context** — beside/over the current surface.
- **Opening Recommendation Panels:** from a finding, the **Recommendation Panel** opens in context.
- **Returning to previous context:** closing a panel returns the user to exactly where they were — the underlying project/artifact surface and selection are preserved.

**Panel behavior vs. screen navigation (Q6, resolved):** **Finding and Recommendation experiences are contextual Panels, not separate screens/workspaces** (consistent with the Artifact Workspace and Collaboration specs). Panels keep the user in their current context (Object Context) rather than navigating away, preserving the understanding the user is investigating. **Preservation of context (resolved):** opening or closing a panel never discards the project/artifact context, selection, active MRI lens, or scroll position the user came from.

## K. Collaboration Navigation Experience

Subordinate to `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md`:

- **Where collaboration appears (Q7, resolved):** collaboration is reached **in context** — comments orbit the Artifact / Finding / Recommendation / Project objects at their surfaces — and via a **secondary** project-level Collaboration/discussion surface for project-wide conversation. It is not a primary destination competing with the understanding spine.
- **How users reach discussion:** from the object in view (artifact/inline comments, Finding/Recommendation Panel discussion) and from the project-level discussion surface.
- **Relationship to understanding:** collaboration **orbits** understanding — navigation to discussion always keeps the underlying object/context; collaboration never becomes the primary object or a work-management surface.

## L. History Navigation Experience

Subordinate to the approved history definitions (Artifact editing workflow, Collaboration activity):

- **Accessing history (Q8, resolved):** activity and history are a **secondary** project-context surface (and in-context where relevant, e.g., an artifact's prior analyses in the Artifact Workspace).
- **Accessing prior analyses:** users can inspect prior analyses/versions (append-only) from the relevant artifact/project history.
- **Returning to current understanding:** navigating history always offers a clear return to the **current** state; prior analyses are clearly marked as prior and never presented as current.

## M. Settings Navigation Experience

Subordinate to `ACCOUNT_AND_WORKSPACE_SETTINGS_EXPERIENCE_SPECIFICATION_V1.md`:

- **Entering settings (Q9, resolved):** settings is entered from **global navigation** (the account/workspace menu) as its own periphery surface.
- **Leaving settings:** the user exits back to where they were — Workspace Home or the project they came from.
- **Preserving workspace/project context (resolved):** entering/leaving settings **does not disturb** the open project's state or the workspace context; settings never overlays or alters the understanding workspaces.

## N. Returning User Navigation Experience

Consistent with the Onboarding spec's returning-user resolution:

- **Where users land (Q12, resolved):** returning users land on their **Workspace Home / Project List** — not onboarding.
- **How users resume projects:** opening a project returns them to its **Project Overview** (or the orientation/last state it was in), resuming where understanding stands.
- **How users resume understanding work:** the shell restores the project context so users continue from the lifecycle position they left; if the project's analysis is **stale**, that is communicated (§Q11 below) per the editing workflow.

## O. Empty States

Navigation must **distinguish**:

- **No projects** — empty Workspace Home ("create your first project").
- **No artifacts** — an open project with no artifacts ("add artifacts to begin"); understanding destinations present but awaiting content.
- **No analysis** — artifacts present but not yet analyzed (Analyzing/awaiting); MRI/Overview show their not-yet-analyzed states rather than empty understanding.
- **Unavailable** — a workspace/project/surface temporarily unavailable, distinct from "empty/none."

## P. Failure States

Navigation failures are **honest and recoverable**:

- **Unavailable screen/surface (Q14):** when a destination can't load, the shell shows an **"unavailable — retry"** state in place, **without losing** the surrounding context (the user stays oriented and can go back).
- **Unavailable project:** when a project can't open, the shell reports it and returns the user safely to Workspace Home / Project List rather than a dead end.
- **Navigation recovery behavior:** a clear path **back** is always available; the shell never strands the user, never silently redirects, and never fabricates content for a failed destination.

## Q. Progressive Disclosure

- **Primary navigation surfaces:** global anchors (Workspace Home / Project List / Create Project) and, within a project, the understanding spine (Overview / MRI / Artifact).
- **Secondary navigation surfaces:** Collaboration and Activity/History within a project; Settings/Account at the periphery.
- **Tertiary navigation surfaces:** contextual Panels (Finding, Recommendation) and in-context affordances (artifact switching, history of a specific artifact), surfaced where the user already is.
- **Intentionally absent:** workflow/task/approval/execution navigation; scores/computed metrics in the shell; governance/automation/agent surfaces; any destination that would make management — rather than understanding — the center of gravity.

## R. Integrity Rules

- **NAV-1.** **Understanding remains the center of gravity** — the understanding spine (Orientation → Overview → MRI → Artifact → Panels) is always primary; management sits at the periphery.
- **NAV-2.** **Navigation creates no assessment** — moving between surfaces never produces or alters CAF / Reliability / Confidence; **only reanalysis changes assessment**.
- **NAV-3.** **Navigation generates nothing** — no findings, recommendations, or content are created by navigating.
- **NAV-4.** **Navigation governs nothing** — no governance/approval/decision surface.
- **NAV-5.** **Navigation is not execution/workflow management** — the shell routes; it is not a task board, pipeline, queue, or execution console.
- **NAV-6.** **Three contexts stay separate and nested** — Workspace, Project, Object; entering one never silently loses the enclosing context.
- **NAV-7.** **Context is preserved across movement** — switching/opening/closing (including panels and settings) never discards the project/artifact/selection/lens the user came from.
- **NAV-8.** **Finding and Recommendation are contextual Panels**, not separate screens (consistent with the owning specs).
- **NAV-9.** **Lifecycle is reinforced, not enforced** — users may jump directly once understanding exists; only the natural "first understanding needs the initial analysis" precondition applies.
- **NAV-10.** **History/prior analyses are clearly marked as prior** and never presented as current; a return to current is always available.
- **NAV-11.** **Stale analysis is communicated** during navigation (per the editing workflow); the shell never presents stale understanding as current.
- **NAV-12.** **Collaboration orbits understanding** — discussion navigation keeps the underlying object and never becomes the primary object or a work-management surface.
- **NAV-13.** **Failures are recoverable** — a path back always exists; users are never stranded and no content is fabricated for a failed destination.
- **NAV-14.** The shell **redefines no owned experience** and defines **no permissions architecture, APIs, events, implementation, or styling**.

## S. Conformance Requirements

A conforming Global Navigation & Application Shell MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:

- **NAV-C1.** Provide a small, stable **global navigation** (Workspace Home / Project List / Create Project / Settings / Account) and keep project-internal and object-level destinations out of it (§E; NAV-1). **Fail** if workflow/task/approval/execution navigation appears anywhere in the shell.
- **NAV-C2.** Maintain the **three nested contexts** (Workspace / Project / Object) without blurring them (§D; NAV-6).
- **NAV-C3.** Make **Overview / MRI / Artifact the primary** project destinations and **Collaboration / Activity-History secondary** (§G; NAV-1).
- **NAV-C4.** Allow **direct navigation** among understanding surfaces once understanding exists, enforcing **no lifecycle order** beyond requiring the initial analysis for first understanding (§H; NAV-9). **Fail** if lifecycle steps are gated beyond that precondition.
- **NAV-C5.** Open **Finding and Recommendation experiences as contextual Panels**, preserving the underlying context on open/close (§J; NAV-7/NAV-8). **Fail** if they are separate screens that discard context.
- **NAV-C6.** Ensure **no navigation action changes assessment, or generates findings/recommendations/content** (NAV-2/NAV-3). **Fail** if navigating computes or generates anything.
- **NAV-C7.** Keep **collaboration in context / secondary**, subordinate to the Collaboration spec, never the primary object (§K; NAV-12).
- **NAV-C8.** Present **history/prior analyses as prior**, with a clear return to current and **stale communicated** (§L; NAV-10/NAV-11). **Fail** if prior or stale understanding is presented as current.
- **NAV-C9.** Enter/leave **Settings** from the periphery without disturbing workspace/project context (§M; NAV-7).
- **NAV-C10.** Land **returning users** on Workspace Home and restore project/understanding context on resume (§N).
- **NAV-C11.** Implement **empty states** distinguishing no projects / no artifacts / no analysis / unavailable (§O), and **failure states** that keep context, offer a path back, and **fabricate nothing** (§P; NAV-13).
- **NAV-C12.** Expose **no** governance, execution, automation, agent, permissions-architecture, API, event, implementation, or styling definition (NAV-4/NAV-5/NAV-14). **Fail if governance navigation appears. Fail if execution/workflow-management navigation appears.**

**Explicit fail conditions.** Conformance is **all-or-nothing**. The shell **fails** if it: changes any assessment or generates any finding/recommendation/content through navigation; introduces workflow/task/approval/execution/governance navigation; blurs the Workspace/Project/Object contexts; turns Finding/Recommendation into context-discarding screens; gates the understanding lifecycle beyond the initial-analysis precondition; presents prior or stale understanding as current; makes collaboration the primary object or a work-management surface; strands the user or fabricates content on a failed destination; disturbs project context when entering settings; or defines permissions architecture, APIs, events, implementation, or styling.

## T. Deferred Items

Explicitly **deferred / out of scope:** mobile-specific navigation; future multi-workspace navigation; advanced personalization (customizable navigation, pinned/recent intelligence); future navigation enhancements; the internal behavior of every owned experience (referenced, not redefined); governance; execution; agents; automation; permissions architecture; APIs; events; implementation; styling; and any numeric/calibration values.

---

*This specification defines the canonical Release 1 Global Navigation & Application Shell — OSLO's navigation constitution. It establishes three nested contexts (Workspace / Project / Object); a small stable global navigation (Workspace Home, Project List, Create Project, Settings, Account); the primary understanding spine (Project Overview, MRI Workspace, Artifact Workspace) with Collaboration and Activity/History secondary; an understanding lifecycle (60-Second Orientation → Overview → MRI → Artifact → Finding Panel → Recommendation Panel) that is reinforced but not enforced (direct jumps allowed once understanding exists); Finding and Recommendation as contextual Panels that preserve context; context preserved across all movement; prior/stale understanding always marked and never presented as current; returning users landed on Workspace Home with project context restored; and honest, recoverable empty and failure states. It is UX/interaction only — it routes users between experiences, computes nothing, generates nothing, governs nothing, keeps understanding the center of gravity, never becomes workflow or execution management, and introduces no governance, execution, agents, automation, permissions architecture, APIs, events, implementation, or styling; only reanalysis changes assessment.*

**Global Navigation & Application Shell Specification v1 complete.**
