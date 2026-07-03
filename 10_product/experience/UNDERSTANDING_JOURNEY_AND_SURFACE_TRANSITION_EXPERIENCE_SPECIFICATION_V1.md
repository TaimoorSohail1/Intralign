# Understanding Journey & Surface Transition Experience Specification v1

**Document Type:** Experience Specification (UX / Interaction Model Only)
**Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Consistent with and subordinate to (authoritative — must not redefine):** `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1.md` · `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · `MRI_WORKSPACE_SPECIFICATION_V1.md` · `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` · `FINDING_PANEL_SPECIFICATION_V1.md` · `RECOMMENDATION_PANEL_SPECIFICATION_V1.md` · `UNDERSTANDING_COMPANION_SURFACE_EXPERIENCE_SPECIFICATION_V1.md` · `OSLO_CHAT_AND_CLARIFICATION_EXPERIENCE_SPECIFICATION_V1.md` · `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW_SPECIFICATION_V1.md` · `ORIENTATION_STATE_MODEL_V1.md` · `SIXTY_SECOND_ORIENTATION_WORKFLOW_SPECIFICATION_V1.md` · `FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md` · CAF Assessment · Reliability v2 · Confidence v2.

> **Non-negotiable constraints.** UX / interaction model only — this spec defines **movement and transitions** between existing surfaces. It **computes nothing, generates nothing, governs nothing, executes nothing**, and **changes no assessment**. It introduces **no** workflow, governance, execution, task management, approval models, automation, agents, new objects, scoring, APIs, events, implementation, or styling. **Only reanalysis changes assessment.** Artifacts remain the **source of truth**, Findings **descriptive**, Recommendations **advisory**, MRI the **diagnostic discovery** experience, and understanding the **center of gravity.**
>
> This specification **redefines no surface** — each surface's internal behavior is owned by its own spec. It defines only **how users move between them** and how **context is preserved** across moves.

> **Position in the architecture.** This is the **connective journey layer**. With it, every surface, panel, companion, and interaction layer has a formally defined place in the journey — closing and completing the Release 1 understanding architecture.

---

## A. Purpose

Define the canonical Release 1 **understanding journey** and the **transition rules** between Project Overview, MRI Workspace, Artifact Workspace, Finding Panel, Recommendation Panel, Understanding Companion, and OSLO Chat. It answers:

> **"How does a user move through understanding?"**

It establishes the canonical flow, the **valid shortcuts and contextual jumps**, **context preservation**, **Chat and Companion handoffs**, **return behaviors**, and **stale-state behavior** — without introducing workflow, governance, execution, task management, approval models, automation, or assessment changes.

## B. Scope

**In scope:** the canonical understanding flow; entry points; the conditions/rationale for each transition (Overview→MRI→Artifact→Finding→Recommendation); level-skipping/shortcut rules; Companion- and Chat-mediated movement; the return path; context preservation across transitions; stale-understanding surfacing during navigation; recovery when lost; and forbidden navigation behaviors.

**Out of scope:** the internal behavior of any surface (owned by its spec); workflow/governance/execution/task/approval/automation/agents; assessment computation or change; new objects; APIs/events/implementation/styling. This spec governs **transitions and context**, not surface internals.

## C. Journey Philosophy

The journey is a **deepening investigation**, not a pipeline. Each step answers a sharper question about the same understanding; movement **carries context forward** so the user never loses their place; and the structure **reinforces** the understanding lifecycle without **enforcing** rigid step-gates. The journey keeps **understanding the center of gravity** — every transition leads toward seeing, explaining, or improving understanding, never toward managing work. Crucially, **moving changes nothing**: no transition computes, generates, or alters assessment; only **information change → reanalysis** does.

## D. Owner-Level Decisions — Resolutions (Q1–Q14)

### Q1 — Canonical understanding journey
**Resolution.** The canonical flow is a **deepening chain**, each step answering a sharper question:

```text
Workspace Home → Project Overview → MRI Workspace → Artifact Workspace → Finding Panel → Recommendation Panel
   (choose      (how strong is     (where are the    (what does the      (why does this   (what could I
    project)     understanding?)    weaknesses?)      content say?)       weakness exist?) consider?)
```
with the **Understanding Companion** persistent alongside Overview/MRI/Artifact and **OSLO Chat** as a floating layer available throughout — both **accelerators** of this flow, not separate journeys.

### Q2 — Canonical entry point
**Resolution.** The canonical entry into understanding is the **60-Second Orientation → Project Overview** (per onboarding/orientation). **Project Overview is the understanding home** and the standing entry point for a returning user opening a project. (Workspace Home is the pre-understanding entry that selects which project to enter.)

### Q3 — When Overview → MRI
**Resolution.** A user moves **Overview → MRI** when, having seen *how strong/trustworthy* understanding is overall, they want to know **where the weaknesses are** ("what needs attention?"). Triggered by intent (or by selecting a weakness summary on Overview / in the Companion). Not gated — it is the natural next deepening.

### Q4 — When MRI → Artifact
**Resolution.** A user moves **MRI → Artifact** when, having found *where* weakness concentrates, they want to see **what the content actually says** — the artifact in situ. Triggered by selecting a finding's location / "show in artifact." MRI = *where to look*; Artifact = *what it says*.

### Q5 — When Artifact → Finding
**Resolution.** A user moves **Artifact → Finding (Panel)** when, seeing a weakness in the content (e.g., a CAF overlay), they want to know **why it exists** — its explanation and evidence. The Finding Panel opens **in context** over the artifact (per the Panel surface model), preserving the artifact beneath.

### Q6 — When Finding → Recommendation
**Resolution.** A user moves **Finding → Recommendation (Panel)** when, understanding *why* a weakness exists, they want to know **what they could consider doing** — the advisory recommendations. The Recommendation Panel opens **only in Finding context** (per `RECOMMENDATION_PANEL_SPECIFICATION_V1.md` RP-C1), preserving the Finding beneath.

### Q7 — Can users skip levels?
**Resolution: Yes — within rules.** The lifecycle is **reinforced, not enforced** (per Global Navigation): once first understanding exists, users may jump directly among **Overview / MRI / Artifact** and open a **Finding Panel** from any context that references a finding (Overview/Companion/MRI/Artifact). **The one hard rule:** the **Recommendation Panel cannot be skipped to** — it opens **only from Finding context** (never directly from Overview/MRI/Artifact/Companion/Chat without a Finding). The only natural precondition is that **first understanding requires the initial analysis** (a brand-new project must reach the 60-Second Orientation first).

### Q8 — How the Companion influences movement
**Resolution.** The **Understanding Companion** (persistent across Overview/MRI/Artifact) is a **launcher**: Top Findings → Finding Panel; Top Recommendations → **associated Finding (Finding Panel) → Recommendation Panel**; Ask OSLO → Chat; shortcuts → MRI/Artifact. It **accelerates** valid transitions and **preserves context**; it is **not** a destination and hosts no structured actions.
> ✅ **Reconciled (Decision 001, Option B):** per `UNDERSTANDING_COMPANION_RECONCILIATION_DECISION_001.md`, the canonical route is **Companion → associated Finding Panel → Recommendation Panel** (the Companion never opens a Recommendation Panel directly; RP-C1 holds). This journey spec already reflects that route.

### Q9 — How Chat influences movement
**Resolution.** **OSLO Chat** (floating layer) is a **conversational front door**: it explains/clarifies/navigates and **routes into** the structured surfaces (Open Finding Panel / Show in Artifact / Open MRI). Chat **accelerates** movement and is **context-aware**, but it is **not a navigation model of its own** and **never bypasses** surface rules (e.g., it routes to a Recommendation only via its Finding). Chat does not become a destination.

### Q10 — Canonical path back
**Resolution.** The **return path is the inverse of the deepening chain**, and is always available:
```text
Recommendation Panel → Finding Panel → Artifact Workspace → MRI Workspace → Project Overview → Workspace Home
```
Closing a panel returns to the surface beneath it (preserving context); a user can also jump back to any primary surface (Overview/MRI/Artifact) directly. The user is **never stranded** — a path back always exists.

### Q11 — How context transitions are preserved
**Resolution.** Every transition **carries context forward and preserves it on return**: the MRI lens/selection, artifact + scroll, CAF overlay, selected finding, and selected recommendation persist beneath panels and are restored when panels close. Opening Chat or the Companion never disturbs the underlying surface. **No transition discards context, and none changes assessment.**

### Q12 — Stale understanding during navigation
**Resolution.** Stale understanding is **surfaced consistently at every surface and in the Companion/Chat** during navigation — labeled as **previous analysis**, **never presented as current** (per the Editing Workflow, Orientation State Model, Dashboard, Companion, Chat). Navigating does **not** clear staleness or trigger reanalysis; only reanalysis does.

### Q13 — How users recover when lost
**Resolution.** Recovery is always available: a **path back** to any primary surface (Overview/MRI/Artifact) and to **Workspace Home** is persistent (global navigation); **Project Overview** is the reliable "home base" for re-orientation; the **Companion** gives an always-visible read-out of where understanding stands; and **Chat** can answer "where am I / show me X." No dead ends, no silent redirects.

### Q14 — Forbidden navigation behaviors
**Resolution.** Forbidden: opening a **Recommendation Panel without Finding context**; any transition that **changes assessment**, **generates** a finding/recommendation, or **computes** a value; **workflow/pipeline/stage-gate** navigation; **governance/approval/execution/task/assignment/automation** navigation; making **Chat or the Companion a destination**; **stranding** the user or **fabricating** content/context on a failed transition; **discarding context** on transition; and presenting **stale as current** while navigating.

## E. Experience Architecture (the journey map)

```text
                         Workspace Home
                              │ (open project)
                              ▼
   ┌───────────────── Project Overview ◄───────────────────────┐
   │                        │  ▲                                │
   │   Companion (persistent)│  │ return                         │
   │   Chat (floating)       ▼  │                                │
   │                   MRI Workspace ◄──────────────┐           │
   │                        │  ▲                     │ return    │
   │                        ▼  │                     │           │
   │                 Artifact Workspace ◄──────┐     │           │
   │                        │  ▲                │     │           │
   │              (in context)│  │ close         │     │           │
   │                        ▼  │                │     │           │
   │                   Finding Panel ───────────┘     │           │
   │                        │  ▲   (only from Finding) │           │
   │              (in context)│  │ close                │           │
   │                        ▼  │                        │           │
   │                Recommendation Panel ───────────────┘           │
   └───────────────────────────────────────────────────────────────┘
        Deepening ▼   ·   Return ▲   ·   Direct jumps among Overview/MRI/Artifact   ·
        Companion launches & Chat routes accelerate valid transitions (context preserved)
```

- **Primary surfaces:** Overview, MRI, Artifact (direct jumps allowed among them).
- **Contextual panels:** Finding (from any finding reference), Recommendation (**only** from Finding).
- **Accelerators:** Companion (persistent launcher), Chat (floating router) — neither a destination.

## F. Transition Rules (canonical)

| From → To | Trigger / question | Rule |
|---|---|---|
| Workspace Home → Overview | open a project | enters Project Context at the understanding home (Q2). |
| Overview → MRI | "where are the weaknesses?" | open; context = project (Q3). |
| MRI → Artifact | "what does the content say?" | open; carries the selected finding's location (Q4). |
| Artifact → Finding Panel | "why does this exist?" | opens **in context** over the artifact (Q5). |
| Finding → Recommendation Panel | "what could I consider?" | opens **only in Finding context** (Q6, RP-C1). |
| any finding reference → Finding Panel | from Overview/Companion/MRI/Artifact | allowed (finding is first-class) (Q7). |
| Companion → Finding / (Finding →) Recommendation / Chat / MRI / Artifact | launcher | accelerates valid transitions; preserves context (Q8). |
| Chat → Finding Panel / Artifact / MRI / (Finding →) Recommendation | conversational routing | never bypasses surface rules (Q9). |
| any → back | return | inverse chain; close-to-underlying; jump-to-primary; never stranded (Q10). |

**Invariants on every transition:** context preserved (Q11); no assessment change; no generation/computation; stale surfaced honestly (Q12).

## G. Context Preservation

- **Carried forward:** project, MRI lens/selection, artifact + scroll, CAF overlay, selected finding, selected recommendation — as applicable to the destination.
- **Preserved beneath panels:** the originating surface remains beneath Finding/Recommendation panels and is restored on close.
- **Non-disturbing overlays:** opening the Companion or Chat never alters or navigates the underlying surface.
- **Never:** discards context, silently changes scope, or mutates assessment as a side effect of moving.

## H. Companion & Chat Handoffs

- **Companion (persistent, Overview/MRI/Artifact):** a **launcher** into Finding Panel / (associated Finding → Recommendation Panel) / Chat / MRI / Artifact; presentation-only; no structured actions; preserves context. *(Companion→Recommendation routes through the associated Finding per `UNDERSTANDING_COMPANION_RECONCILIATION_DECISION_001.md`, Option B.)*
- **Chat (floating, throughout):** a **router and explainer**; routes into structured surfaces without becoming one; respects all surface rules (esp. Recommendation-only-from-Finding); clarifications feed reanalysis, not direct change.
- Both are **accelerators** of the canonical flow — they add **valid shortcuts and contextual jumps**, never new destinations or new rules.

## I. Return & Recovery Behavior

- **Return:** inverse deepening chain; close-panel-to-underlying; direct jump to any primary surface; always available (Q10).
- **Recovery (lost):** persistent global navigation (back to Workspace Home / any primary surface); **Project Overview** as home base; **Companion** as always-visible orientation; **Chat** for "where am I / show me X" (Q13).
- **No dead ends, no silent redirects, no fabricated destinations.**

## J. Stale-State Behavior During Navigation

- Stale understanding is **labeled as previous analysis** consistently across surfaces, Companion, and Chat as the user navigates (Q12).
- Navigating **never** clears staleness, presents stale as current, or triggers reanalysis; **only reanalysis** updates understanding.

## K. Empty States

- **No project open** — Workspace Home (out of this spec's understanding-journey scope; entry only).
- **Not yet analyzed** — primary surfaces show analyzing/awaiting (per Orientation State Model); transitions into MRI/Artifact present not-yet-analyzed read-outs, not fabricated understanding.
- **No weaknesses / no findings / no recommendations** — deeper transitions present neutral "nothing here" states distinct from "not yet analyzed."
- **Unavailable** — a destination temporarily unavailable (§L), distinct from empty.

## L. Failure States

- **Transition/destination failure** — show "unavailable — retry" **in place**, preserve the originating context, and keep a path back; never strand, never fabricate the destination's content.
- **Lost context on failure** — never silently lost; the user is returned to a known surface with context intact where possible.
- **General principle** — honest, recoverable, non-fabricating; the journey never invents understanding to fill a failed transition.

## M. Progressive Disclosure

- **Primary movement:** the deepening chain (Overview → MRI → Artifact → Finding → Recommendation) and direct jumps among primaries.
- **Accelerated movement:** Companion launches and Chat routes (contextual jumps).
- **Return movement:** inverse chain and jump-to-primary, always available.
- **Intentionally absent:** workflow/pipeline/stage navigation; governance/approval/execution/task/assignment/automation movement; assessment-changing transitions; Chat/Companion as destinations; numeric/scored navigation.

## N. Integrity Rules

- **JNY-1.** Movement **computes nothing, generates nothing, governs nothing, executes nothing**.
- **JNY-2.** No transition **changes assessment**; **only reanalysis** does.
- **JNY-3.** The canonical flow is **Overview → MRI → Artifact → Finding Panel → Recommendation Panel**, **reinforced not enforced**.
- **JNY-4.** Users may **jump directly** among Overview/MRI/Artifact and open a **Finding Panel** from any finding reference, once first understanding exists.
- **JNY-5.** The **Recommendation Panel opens only from Finding context** — it can never be skipped to (RP-C1).
- **JNY-6.** Every transition **preserves context** (carry-forward and restore-on-return); none discards it.
- **JNY-7.** The **Companion** is a launcher and the **Chat** is a router — **accelerators, not destinations**, neither adds new rules or bypasses surface rules.
- **JNY-8.** A **path back is always available**; users are **never stranded**, never silently redirected.
- **JNY-9.** **Stale understanding is surfaced as previous analysis** during navigation and **never presented as current**; navigation triggers no reanalysis.
- **JNY-10.** Findings remain **descriptive**, Recommendations **advisory**; movement never reframes them.
- **JNY-11.** The journey **introduces no new objects** and **redefines no surface** (each surface's internals are owned by its spec).
- **JNY-12.** **No workflow, pipeline, stage-gate, governance, approval, execution, task, assignment, or automation** navigation.
- **JNY-13.** Failures are **honest and recoverable**; no fabricated destination/content/context.
- **JNY-14.** **No APIs, events, implementation, or styling** defined here.

## O. Conformance Requirements

A conforming Understanding Journey MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:

- **JNY-C1.** Provide the canonical deepening flow and **direct jumps** among Overview/MRI/Artifact, enforcing **no** lifecycle order beyond requiring the initial analysis for first understanding (§D Q1/Q7; JNY-3/JNY-4). **Fail** if steps are gated beyond that precondition, or if pipeline/stage navigation appears.
- **JNY-C2.** Open the **Recommendation Panel only from Finding context** (§D Q6; JNY-5). **Fail** if it opens directly from Overview/MRI/Artifact/Companion/Chat without a Finding.
- **JNY-C3.** **Preserve context** on every transition and restore it on return (§G; JNY-6). **Fail** if any transition discards context.
- **JNY-C4.** Treat **Companion as launcher** and **Chat as router** — accelerators, not destinations, never bypassing surface rules (§H; JNY-7). **Fail** if either becomes a destination or bypasses a surface rule.
- **JNY-C5.** Always provide a **path back / recovery** to any primary surface and Workspace Home; never strand or silently redirect (§I; JNY-8).
- **JNY-C6.** Surface **stale as previous analysis** during navigation, never as current, triggering no reanalysis (§J; JNY-9). **Fail** if stale is presented as current or reanalysis is triggered by navigating.
- **JNY-C7.** Ensure **no transition changes assessment, generates, or computes** (JNY-1/JNY-2). **Fail** if movement changes assessment or creates content.
- **JNY-C8.** Introduce **no new object**, redefine **no surface**, and define **no** workflow/governance/execution/task/approval/automation navigation (JNY-11/JNY-12). **Fail if workflow/governance/execution/task/approval/automation navigation appears.**
- **JNY-C9.** Handle **transition failures** honestly — preserve context, offer retry/return, fabricate nothing (§L; JNY-13).
- **JNY-C10.** Define **no** APIs/events/implementation/styling (JNY-14).

**Explicit fail conditions.** Conformance is **all-or-nothing**. The journey **fails** if it: opens a Recommendation Panel without Finding context; gates the lifecycle beyond the initial-analysis precondition or adds workflow/pipeline/stage navigation; discards context on any transition; changes assessment or generates/computes anything by moving; makes the Companion or Chat a destination or lets either bypass surface rules; strands the user, silently redirects, or fabricates a destination's content/context on failure; presents stale understanding as current or triggers reanalysis by navigating; introduces a new object or redefines a surface; or defines governance/approval/execution/task/assignment/automation navigation, APIs, events, implementation, or styling.

## P. Deferred Items

Explicitly **deferred / out of scope:** the internal behavior of every surface (owned by its spec); mobile/responsive transition behavior; deep-link/URL transition mechanics; navigation history depth and breadcrumb specifics; personalization of shortcuts; workflow/governance/execution/task/approval/automation; APIs; events; implementation; styling; and any numeric/calibration values.

---

*This specification defines the canonical Release 1 Understanding Journey & Surface Transitions — the connective layer answering "How does a user move through understanding?" It establishes the deepening flow Workspace Home → Project Overview → MRI Workspace → Artifact Workspace → Finding Panel → Recommendation Panel (reinforced, not enforced), with direct jumps among the primary surfaces, a Finding Panel openable from any finding reference, and a Recommendation Panel openable only from Finding context. The Understanding Companion acts as a persistent launcher and OSLO Chat as a floating router — accelerators that add valid shortcuts and contextual jumps without becoming destinations or bypassing surface rules. Every transition preserves context and restores it on return; a path back is always available; stale understanding is consistently surfaced as previous analysis and never presented as current; and recovery from being lost is always possible via global navigation, Project Overview, the Companion, and Chat. It is UX/interaction only — movement computes nothing, generates nothing, governs nothing, executes nothing, introduces no new objects, redefines no surface, and changes no assessment; only reanalysis changes assessment. With every surface, panel, companion, and interaction layer now formally placed in the journey, the Release 1 understanding architecture is closed and complete.*

**Understanding Journey & Surface Transition Experience Specification v1 complete.**
