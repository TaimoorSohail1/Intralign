# OSLO Chat & Clarification Experience Specification v1

**Document Type:** Experience Specification (UX / Interaction Model Only)
**Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Consistent with and subordinate to (authoritative — must not redefine):** `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1.md` · `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · `MRI_WORKSPACE_SPECIFICATION_V1.md` · `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` · `FINDING_PANEL_SPECIFICATION_V1.md` · `RECOMMENDATION_PANEL_SPECIFICATION_V1.md` · `FINDING_PRESENTATION_SPECIFICATION_V1.md` · `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` · `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md` · `ONBOARDING_AND_PROJECT_CREATION_EXPERIENCE_SPECIFICATION_V1.md` · `ACCOUNT_AND_WORKSPACE_SETTINGS_EXPERIENCE_SPECIFICATION_V1.md` · `SIXTY_SECOND_ORIENTATION_WORKFLOW_SPECIFICATION_V1.md` · `ORIENTATION_STATE_MODEL_V1.md` · `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW_SPECIFICATION_V1.md` · `FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md` · CAF Assessment · Reliability v2 · Confidence v2.

> **Non-negotiable constraints.** This specification defines the **OSLO Chat experience, conversational interaction model, clarification experience, explanation experience, contextual chat behavior, awareness of conversational context, and chat-related navigation behavior only.** It must **NOT** define: governance workflows, execution workflows, automation, agent orchestration, approval workflows, task management, project-management workflows, APIs, events, implementation, model architecture, prompt architecture, permissions architecture, notification infrastructure, calculations, assessment generation, finding generation, recommendation generation, or styling.
>
> **OSLO Chat computes nothing. Generates nothing. Governs nothing. Executes nothing.** It presents **conversational interaction around existing project understanding.** **Only reanalysis changes assessment.** Artifacts remain the **source of truth**. Findings remain **descriptive**. Recommendations remain **advisory**. MRI remains the **diagnostic discovery** experience.

> **Position in the architecture.** OSLO Chat is **not another screen** — it is the **conversational interaction layer that sits across all project surfaces**, the primary **human-to-OSLO** surface for understanding exploration, clarification, explanation, and navigation. With it, OSLO becomes an **interactive understanding system** rather than a collection of screens.

---

## A. Purpose

Define the canonical Release 1 **OSLO Chat & Clarification Experience**. It answers:

> **"How do users interact conversationally with OSLO?"**

OSLO Chat provides a conversational interface for **understanding exploration, finding explanation, recommendation discussion, confidence explanation, CAF explanation, clarification conversations, and project-understanding navigation.** It exists to help users **understand what OSLO already knows.** It is **not** a workflow engine, a governance surface, an execution surface, or a task-management experience.

## B. Scope

**In scope:** the OSLO Chat surface and conversational interaction model; the **clarification** experience (OSLO- and user-initiated); the **explanation** experience (findings, recommendations, CAF, reliability, confidence); contextual chat behavior and **context-awareness**; chat-related **navigation** of understanding; **chat history** (presentation); the **collaboration relationship**; and the empty/failure/progressive-disclosure behavior bounding all of it.

**Out of scope:** everything in the non-negotiable constraints block — governance/execution/approval/task/project-management workflows, automation, agent orchestration, APIs, events, implementation, model/prompt/permissions architecture, notification infrastructure, calculations, and assessment/finding/recommendation generation; plus styling. Chat **presents, explains, clarifies, and navigates** existing understanding; it produces and mutates nothing.

## C. Chat Philosophy

OSLO Chat makes project understanding **explorable in natural language** while preserving every ratified invariant. It is a **conversation over existing understanding**, not a new source of it: it explains what OSLO already understands, helps the user supply missing information through clarification, and routes the user to the right structured surface. Chat **complements** the structured surfaces (it never replaces them), keeps **understanding the center of gravity**, and is rigorously **non-mutating** — asking OSLO a question or answering a clarification never changes CAF, Reliability, Confidence, a finding, or a recommendation. The only path to changed understanding remains **information change → reanalysis**.

## D. Owner-Level Decisions — Resolutions (Q1–Q14)

### Q1 — Canonical OSLO Chat surface
**Resolution: a floating conversational layer / persistent assistant available across all project surfaces.** Chat **lives** as an interaction layer above the project surfaces (not a dedicated workspace, not merely a single fixed panel). Users **access** it via a persistent, always-available entry point on every project surface. It is **globally available within a project** and **project-context aware** (§E, §F). It is **not** a global navigation destination.

### Q2 — Purpose
**Resolution: Chat supports** explanation, clarification, understanding exploration, navigation assistance, recommendation discussion, finding discussion, and project-understanding discussion. **Primary purpose: understanding** — specifically **clarification and explanation of existing understanding** (with navigation and discussion in support). Chat is the primary *conversational* understanding surface; it does **not** displace the structured surfaces as the primary understanding surfaces (see Architectural Analysis §Q).

### Q3 — Primary clarification interface
**Resolution: Yes.** Clarification occurs **through chat** (conversationally), **not** through Finding Panels or Recommendation Panels and **not** through a separate clarification experience. Panels remain **structured understanding surfaces**; clarification is **conversational** and lives in Chat (§G).

### Q4 — Explain Findings
**Resolution: Yes.** Users **ask about findings** in natural language ("Why does this finding exist?", "Show evidence", "What caused this?", "What assumptions led here?"). Chat **relates to the Finding Panel** by **contextual handoff** (Panel ↔ Chat, §H/§I); it **preserves finding context** (the finding under discussion stays in scope) and lets users **move between findings and chat** without losing place. Chat presents the finding's **existing** explanation/evidence/CAF-impact descriptively; it generates no finding.

### Q5 — Explain Recommendations
**Resolution: Yes.** Users **ask about recommendations** ("Why is this recommended?", "Why preferred?", "What are the tradeoffs?"). Chat **relates to the Recommendation Panel** by contextual handoff; **recommendation context is preserved** (the recommendation and its finding stay in scope). Chat presents existing rationale and the OSLO Recommended / Possible Resolution Paths / Selected Path constructs advisorily; it generates no recommendation.

### Q6 — Chat ↔ Finding Panels
**Resolution: Chat does NOT replace Finding Panels.** **Finding Panels launch Chat** ("Ask OSLO about this Finding"); **Chat references findings** and routes **into** the Finding Panel for structured investigation; **Finding Panels remain the primary structured understanding surface** for a finding. (Per `FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md`, the Finding Panel is the canonical structured finding surface; Chat complements it.)

### Q7 — Chat ↔ Recommendation Panels
**Resolution: Chat does NOT replace Recommendation Panels.** **Recommendation Panels launch Chat** ("Ask OSLO about this Recommendation"); **Recommendation Panels remain the primary structured recommendation surface.** Chat complements via handoff; structured actions (accept/defer/reject) stay in the Panel, not in Chat.

### Q8 — Contextual Chat launching
**Resolution: Yes — users can initiate Chat from Project Overview, MRI Workspace, Artifact Workspace, Finding Panels, and Recommendation Panels.** **Context follows the conversation:** invoking Chat from a surface/object pre-scopes the conversation to that context (project/artifact/finding/recommendation/surface), and the context persists for the conversation until the user changes it (§F).

### Q9 — Clarification conversations
**Resolution.** **OSLO asks clarification questions conversationally** (optionally with choice options); **users respond conversationally**; **clarifications remain conversational** (not a modeled object). **Clarifications relate to reanalysis** as **information capture** — a clarification answer is treated as a **project-information change** that makes the analysis **stale/pending** and **feeds the next reanalysis** (exactly like an artifact edit, per `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW_…`). **Answering a clarification changes no assessment by itself.** **Interaction with stale analysis:** a pending clarification is shown as awaiting reanalysis; Chat never implies the answer instantly updated understanding (§G, §K).

### Q10 — Understanding navigation through Chat
**Resolution: Yes.** Users can ask "show findings", "show recommendations", "show issues related to a CAF dimension", "explain confidence", "navigate project understanding." Chat **surfaces existing** understanding and **routes into MRI / Artifact / Panels** — it is a conversational **front door** to the same navigation those surfaces provide, **not** a separate navigation model. Ordering is by **existing qualitative** severity/CAF-impact — **no scores/percentages/ranks** (§J).

### Q11 — Chat during stale analysis
**Resolution.** **Chat remains available** when analysis is stale. **Stale understanding is communicated** — Chat clearly marks that findings/recommendations/confidence it presents **reflect the previous analysis** and may be out of date; **stale findings can still be discussed** (attributed to the prior analysis). **Stale-analysis warnings appear** inline in the relevant answer. Consistent with the Editing Workflow, Orientation State Model, and Navigation spec; Chat **never presents stale understanding as current** (§K).

### Q12 — Chat history
**Resolution.** **Conversations persist** (presentation-level): **users can return to prior conversations** within the project. The **relationship to project understanding** is one-way and read-only — history is a record of *conversation*, not a source of understanding; revisiting a past conversation that discussed now-superseded understanding clearly shows it as **prior** (never re-presented as current). **No notification infrastructure or implementation** is defined (persistence/storage mechanics are deferred, §N) (§L).

### Q13 — Collaboration relationship
**Resolution (subordinate to `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md`).** Users may **reference collaborators** in conversation (presentation only). **Chat does NOT create comments**, and **comments do NOT create chat** — the two are distinct surfaces. Collaboration **comments orbit objects** (Artifact/Finding/Recommendation/Project); Chat is a **conversation with OSLO about understanding**. Neither mutates the other or the assessment (§M).

### Q14 — Explicitly out of scope
**Excluded:** task management; project execution; workflow orchestration; governance actions; approvals; assignments; automation controls; agent controls; implementation details. Plus (per constraints) APIs, events, model/prompt/permissions architecture, notification infrastructure, calculations, assessment/finding/recommendation generation, and styling. Chat **declines** such requests honestly (§Q.O / §K).

## E. Experience Architecture

OSLO Chat is a **floating conversational layer** above the project surfaces — an **interaction layer**, not a destination:

```text
            ┌──────────────────────────────────────────────┐
            │  Project surface (Overview / MRI / Artifact / │
            │  Finding Panel / Recommendation Panel)        │
            │                          ╭────────────────╮   │
            │                          │   OSLO Chat     │  │
            │                          │  (floating,     │  │
            │                          │   context-aware)│  │
            │                          ╰────────────────╯   │
            └──────────────────────────────────────────────┘
```

- **Availability:** invocable from **every project surface**; floats above the current surface and **preserves** it — opening/closing Chat never navigates away or disturbs the underlying surface (consistent with the navigation shell).
- **Composition:** a conversation transcript; an input affordance; OSLO-initiated **clarification prompts** (optionally with choice options); **explanation** answers sourced from existing understanding; and **navigational/handoff links** into structured surfaces (Finding/Recommendation Panels, MRI, Artifact).
- **Non-destination:** Chat is **not** a primary navigation destination and does not appear in global navigation as a place; it is an assistant available *on* places.

## F. Context Model

Chat is **context-aware (read-only)** and the context **follows the conversation**:
- **Project context** — which project and its existing understanding.
- **Artifact context** — the open artifact/selection in the Artifact Workspace.
- **Finding context** — an open Finding Panel / selected finding.
- **Recommendation context** — an open Recommendation Panel / selected recommendation.
- **Current-surface context** — which surface invoked Chat.

**Context follow-through:** invoking Chat from a surface/object pre-scopes the conversation; the scope **persists** through the conversation and updates as the user moves or explicitly changes subject. Context is used only to **present and route** more relevantly — Chat never silently acts on, edits, or governs context, and never changes assessment because of it.

## G. Clarification Experience (the primary clarification interface — Q3, Q9)

**OSLO-initiated.** OSLO can ask clarifying questions conversationally, optionally offering choices:
```text
OSLO: I found conflicting success criteria. Which outcome is primary?
      [ A ]   [ B ]   [ C ]
```
**User-initiated.** Users can proactively clarify:
```text
User: Let me clarify stakeholder ownership.
```
**Clarification → information, not assessment.** A clarification **captures information** the user provides and is treated as a **project-information change** that makes analysis **stale/pending** and **feeds the next reanalysis** (like an edit). **Answering a clarification changes no CAF/Reliability/Confidence and resolves no finding by itself**; **only reanalysis** produces updated understanding. Chat communicates this honestly ("Thanks — I'll factor this into the next analysis"), never implying an instant change.

**No new objects.** Clarifications are **conversational information capture** — **not** a modeled object, lifecycle, or governance construct. No Clarification Candidate, Resolution Candidate, Resolution Path, disposition, or accepted-understanding object is created. This is the **primary** clarification surface (clarifications happen here, not inside panels).

## H. Finding Discussion Experience (Q4, Q6)

- Users **ask about findings** in natural language; Chat answers from the finding's **existing** explanation, evidence, supporting context, and CAF impact (per `FINDING_PRESENTATION_…`), **descriptively**.
- **Relationship to the Finding Panel:** **contextual handoff** — the Finding Panel offers "**Ask OSLO about this Finding**"; Chat offers "**Open the Finding Panel**" for structured investigation. **Finding context is preserved** across the handoff; users move between findings and chat without losing place.
- **Finding Panels remain primary** for structured understanding; Chat **complements**, never replaces (Q6). Chat never reframes a finding as a command and **generates no findings**.

## I. Recommendation Discussion Experience (Q5, Q7)

- Users **ask about recommendations** ("why recommended", "why preferred", "tradeoffs"); Chat answers from **existing** rationale and the **OSLO Recommended / Possible Resolution Paths / Selected Path** presentation constructs (per `RECOMMENDATION_PRESENTATION_…`), **advisorily**.
- **Relationship to the Recommendation Panel:** **contextual handoff** — the Recommendation Panel offers "**Ask OSLO about this Recommendation**"; Chat routes **into** the Recommendation Panel (which can only be reached in Finding context, per the surface decision). **Recommendation context is preserved.**
- **Recommendation Panels remain primary**; Chat complements, never replaces (Q7). Structured decisions (accept/defer/reject) stay in the Panel. Chat **generates no recommendations** and never turns advice into a directive.

## J. Understanding Navigation Experience (Q10)

- Users can **navigate understanding conversationally**: "show findings", "show recommendations", "show alignment (CAF dimension) issues", "explain confidence", "show findings affecting confidence most."
- Chat **surfaces existing** matching findings/recommendations and **routes into MRI / Artifact / Panels** — it is a **conversational front door** to the same understanding-navigation those surfaces own, **not a separate navigation model** and not a replacement for MRI/Artifact navigation.
- Ordering uses **existing qualitative** severity/CAF-impact and the existing **Finding → CAF → Confidence** relationship — **never** a chat-side score, percentage, or rank. Navigation **surfaces and routes**; it creates nothing and changes no assessment.

## K. Chat During Stale Analysis (Q11)

- **Chat remains available** when analysis is stale.
- **Stale is communicated inline** — when Chat presents findings/recommendations/confidence whose analysis is out of date (content changed since last analysis, or a clarification is pending), it **marks** the answer as reflecting the **previous analysis** and points to reanalysis as the path to current understanding.
- **Stale findings can still be discussed**, attributed to the prior analysis.
- **Never presents stale understanding as current.** Consistent with the Editing Workflow, Orientation State Model, and Navigation spec.

## L. Chat History Experience (Q12)

- **Conversations persist** (presentation-level) and **users can return to prior conversations** within the project.
- **Relationship to understanding (read-only):** history records the *conversation*, not understanding; it is **not** a source of assessment. A revisited conversation that discussed now-superseded understanding is clearly shown as **prior** — never re-presented as current.
- **No notification infrastructure or implementation** is defined here; persistence/storage mechanics are deferred (§N).

## M. Collaboration Relationship (Q13)

Subordinate to `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md`:
- Users may **reference collaborators** in conversation (presentation only — no permission logic).
- **Chat does not create comments; comments do not create chat** — distinct surfaces. Collaboration comments **orbit objects**; Chat is **conversation with OSLO about understanding**.
- Neither mutates the other, and neither changes assessment. Chat introduces no collaboration object.

## N. Empty States

- **No conversation yet** — a neutral opening ("Ask me about your findings, recommendations, or confidence").
- **No matching understanding** — a navigation/explanation query with no result ("nothing matches"), distinct from "not yet analyzed."
- **Not yet analyzed** — nothing to explain yet (awaiting analysis, per Orientation State Model), distinct from "none found."
- **No prior conversations** — a neutral history empty state.
- **Unavailable** — Chat temporarily unavailable, distinct from "no content."

## O. Failure States

- **Chat unavailable / response failure** — communicated honestly ("I couldn't respond — try again"); the underlying surface and its understanding remain fully usable; **no fabricated answer**.
- **Clarification capture failure** — the user's input is preserved and the failure reported; nothing silently dropped; no partial clarification treated as captured.
- **Out-of-scope request** — Chat **declines clearly** and points to the legitimate path (e.g., "I can't change the assessment directly — update the information and reanalysis will update it"; "I can't assign tasks or approve work").
- **No fabrication** — Chat never invents findings, recommendations, evidence, confidence, or a value to fill a gap.

## P. Progressive Disclosure

- **Always available:** the floating Chat entry point on every project surface.
- **In context:** the conversation scoped to the current surface/object; OSLO-initiated clarification prompts.
- **Through expansion:** longer explanations, evidence detail, alternative tradeoffs — with links **into** the structured Panels/MRI/Artifact for full depth.
- **Through history:** prior conversations (presentation), clearly marked when they reference prior understanding.
- **Intentionally absent:** execute/approve/govern/assign/automate affordances; scores/percentages/ranks; assessment-changing controls; finding/recommendation creation; project-health verdicts.

## Q. Architectural Analysis (determinations)

- **OSLO Chat is** a **persistent assistant / floating conversational layer available across project surfaces** — **not** a destination, **not** merely a single contextual panel, and **not** a dedicated workspace.
- **OSLO Chat is** a **separate interaction layer spanning both Project Context and Object Context** (it is aware of and scopes to both, but belongs to neither alone) — consistent with the navigation shell's context model.
- **Clarification occurs contextually and independently** — **not** strictly before or after recommendations. It can happen at any point (OSLO- or user-initiated), is scoped to context, and always routes through **information → reanalysis**.
- **Does Chat become the primary understanding interaction surface?** **It is the primary *conversational* understanding and *clarification* surface, but it does NOT displace the structured surfaces** (MRI, Artifact Workspace, Finding/Recommendation Panels) as the **primary understanding surfaces**. Understanding stays the center of gravity in the structured surfaces; Chat is the conversational layer over them.

## R. Integrity Rules

- **CHAT-1.** Chat **computes nothing** (no CAF/Reliability/Confidence/scoring/ranking); confidence/CAF are **presented, reliability-qualified, never bare**.
- **CHAT-2.** Chat **generates no findings or recommendations**; it explains/navigates **existing** ones.
- **CHAT-3.** Chat **changes no assessment directly** — asking a question or answering a clarification never alters CAF/Reliability/Confidence or a finding/recommendation state.
- **CHAT-4.** **Only reanalysis changes assessment** — clarifications are **information capture** that make analysis stale/pending and feed the **next reanalysis** (like an edit).
- **CHAT-5.** Findings remain **descriptive**; recommendations remain **advisory** (OSLO Recommended / Possible Resolution Paths / Selected Path presentation-only) — Chat never reframes them as commands.
- **CHAT-6.** Chat **introduces no new objects** — no Clarification Candidate, Resolution Candidate, Resolution Path, disposition, accepted-understanding, comment, or governance object.
- **CHAT-7.** Chat **does not replace** Finding/Recommendation Panels — it complements them via contextual handoff; structured actions stay in the Panels; Panels remain the primary structured surfaces.
- **CHAT-8.** Chat is **context-aware (read-only)** across Project and Object context; it never silently acts on, edits, or governs context.
- **CHAT-9.** Chat **marks stale** understanding and **never presents stale as current**.
- **CHAT-10.** Chat **navigates** by surfacing/filtering existing understanding qualitatively and routing into MRI/Artifact/Panels — **no scores/percentages/ranks**, **no separate navigation model**.
- **CHAT-11.** Chat performs **no governance, execution, automation, agent, task, approval, assignment, or project-health** action (Q14); it **declines** out-of-scope requests honestly.
- **CHAT-12.** Chat **fabricates nothing** — no invented finding/recommendation/evidence/confidence/value.
- **CHAT-13.** Chat is a **floating conversational layer / persistent assistant**, **not a destination** and not a replacement for any structured surface.
- **CHAT-14.** Chat **does not create comments; comments do not create chat** (subordinate to the Collaboration spec).
- **CHAT-15.** Chat **history is presentation-only and read-only** to understanding; prior conversations never re-present superseded understanding as current.
- **CHAT-16.** **No APIs, events, implementation, model/prompt/permissions architecture, notification infrastructure, or styling** defined here; no existing model redefined.

## S. Conformance Requirements

A conforming OSLO Chat experience MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:

- **CHAT-C1.** Be a **floating conversational layer across all project surfaces**, preserving the underlying surface context on open/close, not a destination (§E, §Q; CHAT-13). **Fail** if Chat is a standalone destination or disturbs the underlying surface.
- **CHAT-C2.** **Explain** existing findings/recommendations/CAF/reliability/confidence from existing data, descriptively/advisorily, **reliability-qualified**, computing nothing (§H, §I; CHAT-1/CHAT-2/CHAT-5). **Fail** if Chat computes a value, shows a score, or generates a finding/recommendation.
- **CHAT-C3.** Provide **OSLO- and user-initiated clarification** as the **primary** clarification interface, capturing clarifications as **information feeding reanalysis**, never as direct assessment change (§G; CHAT-3/CHAT-4). **Fail** if a clarification changes assessment or resolves a finding directly, or if clarification is hosted in a Panel instead.
- **CHAT-C4.** **Navigate** understanding by surfacing/filtering **existing** understanding qualitatively and routing into MRI/Artifact/Panels, with no separate navigation model (§J; CHAT-10). **Fail** if navigation ranks by a computed score or creates content.
- **CHAT-C5.** **Complement, not replace** Finding/Recommendation Panels via two-way contextual handoff; keep Panels primary and their structured actions in the Panels (§H, §I; CHAT-7). **Fail** if Chat replaces a Panel or hosts a Panel's structured actions.
- **CHAT-C6.** Be **context-aware read-only** across Project and Object context without acting on context (§F; CHAT-8).
- **CHAT-C7.** **Mark stale** understanding and **never present stale as current** (§K; CHAT-9). **Fail** if stale understanding is presented as current.
- **CHAT-C8.** Keep **history presentation-only/read-only**, never re-presenting superseded understanding as current, with **no notification infrastructure** (§L; CHAT-15/CHAT-16).
- **CHAT-C9.** Keep the **collaboration boundary** — no comment creation by Chat, no chat creation by comments (§M; CHAT-14).
- **CHAT-C10.** **Decline out-of-scope** requests (task/approval/assignment/governance/execution/automation/agent/project-health/direct-assessment-change) and **fabricate nothing** (§O; CHAT-11/CHAT-12). **Fail** if any such action is offered or performed, or content is fabricated.
- **CHAT-C11.** Introduce **no new object** and **no** API/event/implementation/architecture/styling (CHAT-6/CHAT-16). **Fail** if a Clarification/Resolution Candidate, Resolution Path, or comment object appears.
- **CHAT-C12.** Implement empty states (no conversation / no match / not-yet-analyzed / no prior conversations / unavailable) and honest failure states (§N, §O).

**Explicit fail conditions.** Conformance is **all-or-nothing**. OSLO Chat **fails** if it: changes any assessment directly (outside reanalysis); computes a value or shows a score/percentage/rank; generates a finding or recommendation; creates a Clarification Candidate / Resolution Candidate / Resolution Path / comment / any new object; replaces a Finding/Recommendation Panel or hosts their structured actions; presents stale understanding as current; re-presents superseded understanding as current in history; performs task/approval/assignment/governance/execution/automation/agent/project-health actions; fabricates findings/recommendations/evidence/confidence/values; becomes a standalone destination or disturbs the underlying surface; or defines APIs, events, implementation, model/prompt/permissions architecture, notification infrastructure, or styling.

## T. Deferred Items

Explicitly **deferred / out of scope:** task management; project execution; workflow orchestration; governance; approvals; assignments; automation/agent controls; implementation; APIs; events; model architecture; prompt architecture; permissions architecture; notification infrastructure; calculations; assessment/finding/recommendation generation; styling; conversation persistence/storage mechanics and cross-session retention depth; multilingual/voice modalities; exact clarification-prompt option mechanics; and any numeric/calibration values.

---

*This specification defines the canonical Release 1 OSLO Chat & Clarification Experience — the conversational interaction layer spanning all project surfaces (a floating, context-aware, persistent assistant, not a destination), answering "How do users interact conversationally with OSLO?" Resolutions: floating conversational layer available everywhere and project-context aware (Q1); purpose centered on clarification and explanation, with exploration, navigation, and discussion in support (Q2); the primary clarification interface (Q3) with OSLO- and user-initiated clarification captured as information feeding reanalysis (Q9); explanation of findings and recommendations via two-way contextual handoff that complements — never replaces — the Finding and Recommendation Panels (Q4–Q7); contextual launching from every surface with context following the conversation (Q8); conversational understanding-navigation that routes into MRI/Artifact/Panels with no separate navigation model (Q10); stale-aware behavior that never presents stale understanding as current (Q11); presentation-only, read-only chat history (Q12); a strict collaboration boundary subordinate to the Collaboration spec (Q13); and explicit exclusion of task/approval/assignment/governance/execution/automation/agent/project-health actions and direct assessment change (Q14). Architecturally, Chat is a separate interaction layer spanning Project and Object context and is the primary conversational understanding/clarification surface without displacing the structured surfaces as the primary understanding surfaces. It is UX/interaction only — it computes nothing, generates nothing, governs nothing, executes nothing, creates no new object, and changes no assessment directly; artifacts remain the source of truth, findings descriptive, recommendations advisory, MRI the diagnostic discovery experience, and only reanalysis changes assessment.*

**OSLO Chat & Clarification Experience Specification v1 complete.**
