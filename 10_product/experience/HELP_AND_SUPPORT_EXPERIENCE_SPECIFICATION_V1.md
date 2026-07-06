# Help & Support Experience Specification v1

**Document Type:** Experience Specification (UX / Interaction Model Only)
**Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Construct type:** **Cross-cutting Help Surface** — mapped to the ratified taxonomy as a **lightweight Companion-Surface-class layer/affordance** (presents help content + routes; hosts no understanding-actions; not a primary destination/Workspace) (§D).
**Consistent with and subordinate to (authoritative — must not redefine):** `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1.md` · `ONBOARDING_AND_PROJECT_CREATION_EXPERIENCE_SPECIFICATION_V1.md` · `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · `MRI_WORKSPACE_SPECIFICATION_V1.md` · `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` · `FINDING_PANEL_SPECIFICATION_V1.md` · `RECOMMENDATION_PANEL_SPECIFICATION_V1.md` · `OSLO_CHAT_AND_CLARIFICATION_EXPERIENCE_SPECIFICATION_V1.md` · `UNDERSTANDING_COMPANION_SURFACE_EXPERIENCE_SPECIFICATION_V1.md` · `NOTIFICATION_AND_AWARENESS_SURFACE_SPECIFICATION_V1.md` · `HISTORY_AND_TIMELINE_SURFACE_SPECIFICATION_V1.md` · `ACCOUNT_AND_WORKSPACE_SETTINGS_EXPERIENCE_SPECIFICATION_V1.md` · `UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION_001.md` · Release 1 Tier Definitions · CAF Assessment · Reliability v2 · Confidence v2.

> **Non-negotiable constraints.** UX / interaction model only. Help & Support **computes nothing, generates no findings/recommendations/assessment, governs nothing, executes nothing, and changes no assessment.** It must **NOT** define: governance, execution, automation, agents, task management, implementation, APIs, events, or assessment behavior. **Only reanalysis changes assessment.** Artifacts remain the source of truth, Findings descriptive, Recommendations advisory, MRI the diagnostic discovery experience; **Outcome Confidence remains trust in understanding** (never project health/readiness/probability).

> **Position in the architecture.** Help & Support is the **cross-cutting guidance layer** — where users get help understanding **OSLO itself** (the product, its concepts, how to use a surface) and how to **reach support**. It is distinct from OSLO Chat: **Help explains the product and concepts; Chat explains *your project's* understanding** (§I).

---

## A. Purpose

Define the canonical Release 1 **Help & Support Experience**. It answers:

> **"How do users get help, guidance, and support while using OSLO?"**

It gives users **product help, concept help, contextual help, troubleshooting, and a way to contact support** — without governance, execution, automation, agents, task management, or any assessment behavior.

## B. Scope

**In scope:** the help entry point(s) and access; help content **types** (product / concept / contextual / troubleshooting / contact); **contextual help** behavior inside understanding surfaces; the relationship to OSLO Chat, Onboarding, and Support/Contact; empty states; failure states; progressive disclosure; integrity rules; conformance.

**Out of scope:** governance; execution; automation; agents; task management; **support-ticket workflow/tracking** (a contact entry point is in scope; ticketing workflow is **deferred**, §Q); APIs; events; implementation; styling; delivery infrastructure; **documentation authoring/CMS**; and any assessment/finding/recommendation generation or computation. Help **presents guidance and routes**; it changes nothing.

## C. Help Philosophy

Help exists to **reduce friction in using OSLO**, not to manage the user's work. It is a **calm, always-reachable guidance layer**: it explains the product and its concepts, orients users in context, helps them troubleshoot, and points them to support — then gets out of the way. It keeps **understanding the center of gravity** by never interrupting or altering the user's project: opening Help changes no comment, finding, recommendation, artifact, or assessment, and **only reanalysis changes assessment**. Help is **about OSLO**; it never speaks for the user's specific project understanding (that is Chat's role, §I).

## D. Construct Classification

Per the ratified governing taxonomy (`UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION_001.md`), Help & Support is a **lightweight Companion-Surface-class layer/affordance** (the visibility + routing family), in a **help** variant — **not** a new construct type and **not** a Workspace:

| Attribute | Classification |
|---|---|
| **Type** | **Companion-Surface-class** help layer — a lightweight, cross-cutting help affordance (panel/menu), optionally with contextual help in surfaces. |
| **Purpose** | present **product/concept/contextual/troubleshooting help** and route to **support/docs**. |
| **Navigation** | reachable from **global navigation** (and contextually within surfaces); **not a primary destination/Workspace**. |
| **Context** | may be **context-aware (read-only)** to show relevant help; never acts on context. |
| **Independent?** | No — a layer over the app. |
| **Destination?** | **No.** |
| **Hosts actions?** | help navigation + a **contact-support entry point**; **no** understanding-changing or workflow actions. |
| **Contains?** | routes to docs/support/Chat/onboarding; **does not contain** Workspaces/Panels. |
| **Not** | not a Workspace, not a Panel, not Chat (Interaction Layer), not an Understanding Object, not a ticketing/workflow system. |

This binds the spec: anything that makes Help a ticketing/workflow system, a governance/automation surface, an assessment-changer, or OSLO Chat itself is **out of type** and forbidden (§O/§P).

## E. Owner-Level Decisions — Resolutions

### 1 — What is Help & Support in Release 1?
A **lightweight, cross-cutting help layer** (Companion-Surface-class, §D): product/concept/contextual help + troubleshooting + a contact-support entry point. **Not** a workspace, ticketing system, or knowledge-base authoring tool.

### 2 — Where is it accessed?
From **global navigation** (a persistent Help entry, e.g., a "?" affordance) available across the app; and **contextually within surfaces** (Onboarding, Project Overview, MRI, Artifact, Finding Panel, Recommendation Panel, Companion, Settings) via lightweight contextual help (§F, §H). One help layer; multiple entry points.

### 3 — What help types exist?
**All five are Release 1:** **product help** (how OSLO works / how to use a feature), **concept help** (what CAF / Reliability / Outcome Confidence / Finding / Recommendation / MRI mean — consistent with the models, never redefining them), **contextual help** (what *this* surface does, in place), **troubleshooting** (common issues and honest guidance), and **contact support** (an entry point to reach a human; ticket *workflow* deferred, §K/§Q).

### 4 — Chat vs. Help?
**Distinct (§I).** **Help explains OSLO** (product, concepts, how-to, troubleshooting) using **static/curated** guidance. **OSLO Chat explains *your project's* understanding** conversationally over project data. Help may **route to Chat** for project-specific questions; Chat may **route to Help** for product/concept questions. Help is **not Chat** and Chat is **not the help center**.

### 5 — Does Help include onboarding guidance?
**Yes (§J).** Help provides **re-accessible onboarding guidance** (re-open the lightweight, skippable onboarding / "getting started" guidance per `ONBOARDING_…`) — Help does not redefine onboarding; it points back to it.

### 6 — Does Help include documentation links?
**Yes.** Help surfaces **documentation links** (product docs / concept references) as routes. This spec defines the **UX of surfacing links**, not documentation authoring/CMS/hosting (deferred, §Q).

### 7 — Support ticket creation, or deferred?
**A contact-support entry point is Release 1; ticket creation/tracking workflow is deferred.** Help provides a clear way to **reach support** (a contact entry point); the **ticketing workflow, status tracking, and SLA/escalation are out of scope** (§K, §Q) — and would in any case be workflow, which Help must not become.

### 8 — How does Help behave inside understanding surfaces?
**Lightweight, in-context, non-intrusive (§H).** Contextual help explains *what this surface/concept is and how to use it*; it **never** changes the surface's data, never triggers reanalysis, never resolves a finding or accepts a recommendation, and never blocks the work. It opens beside/over without disturbing the underlying surface (consistent with the navigation shell).

### 9 — Empty states (§L) · 10 — Failure states (§M) · 11 — Deferred (§Q)
Resolved in their sections.

## F. Help Access Points

- **Global navigation:** a persistent **Help** entry (e.g., "?"), opening the help layer (search/browse product/concept/troubleshooting help + contact + docs links).
- **Contextual (in-surface):** lightweight contextual help affordances within Onboarding, Project Overview, MRI, Artifact, Finding/Recommendation Panels, Companion, and Settings — explaining *that* surface/concept in place (§H).
- **From Chat:** Chat may route product/concept questions to Help; **from Help:** Help may route project-specific questions to Chat (§I).
- All access points open the **same** help layer (or its contextual slice); Help is not a separate destination.

## G. Help Content Types

| Type | What it provides | Boundary |
|---|---|---|
| **Product help** | how OSLO works; how to use a feature/surface | how-to only; no project data; no actions |
| **Concept help** | what CAF / Reliability / Outcome Confidence / Finding / Recommendation / MRI mean | **consistent with the models; never redefines them**; Confidence = trust in understanding, never project health |
| **Contextual help** | what *this* surface does, in place | non-intrusive; changes nothing (§H) |
| **Troubleshooting** | common issues + honest guidance (e.g., "analysis is stale — reanalyze to update") | guidance only; never performs the fix or changes assessment |
| **Contact support** | a way to reach a human | entry point only; **ticketing workflow deferred** (§K) |

All content is **about OSLO**; none presents, computes, or alters the user's project understanding.

## H. Contextual Help Behavior

- Contextual help is **lightweight and in-context** — it explains the current surface/concept (e.g., "MRI groups weaknesses so you can see what needs attention"; "Outcome Confidence is trust in understanding, reliability-qualified").
- It **changes nothing**: no assessment, no finding/recommendation state, no reanalysis trigger, no comment; it never blocks the work and never hosts the surface's structured actions.
- It opens **beside/over** without disturbing the underlying surface and closes back cleanly (context preserved).
- Concept help **mirrors the canonical models** and never introduces a competing definition (e.g., never frames Confidence as project health/readiness/probability).

## I. Relationship to OSLO Chat

- **Division of labor:** **Help = the product/concepts** (static/curated, about OSLO); **Chat = your project's understanding** (conversational, over project data, per `OSLO_CHAT_…`).
- **Two-way routing:** Help routes project-specific questions to **Chat**; Chat routes product/concept questions to **Help**.
- **Distinct constructs:** Help is a Companion-Surface-class help layer; Chat is the Interaction Layer. **Help is not Chat; Chat is not the help center.** Neither creates the other's content; Help generates no conversational answers over project data, and Chat is not the support/contact channel.

## J. Relationship to Onboarding

- Help provides **re-accessible onboarding / getting-started guidance** by pointing back to the onboarding experience (`ONBOARDING_…`), which is lightweight and skippable.
- Help **does not redefine** onboarding, does not gate value, and re-opening guidance **changes nothing** about the project or assessment.

## K. Relationship to Support / Contact

- Help includes a **contact-support entry point** — a clear path to reach a human for help.
- **Ticket creation, tracking, status, SLA, and escalation are deferred** (§Q) — Help provides the entry point, not the workflow (a ticketing workflow would be task/workflow management, which Help must not become).
- Contacting support **changes no assessment**, creates no finding/recommendation, and is not governance/approval.

## L. Empty States

- **No help results** — a search/browse with no match ("no help found for that — try rephrasing or contact support"), distinct from "help unavailable."
- **No contextual help for this surface** — a neutral "no specific help here" rather than an empty/broken affordance.
- **Contact unavailable** — if the contact entry point can't be offered, say so honestly.
- **Unavailable** — Help temporarily unavailable (§M), distinct from "no results."

## M. Failure States

- **Help unavailable** — "help unavailable — retry"; the rest of the app remains fully usable; fabricate no help content.
- **Content/doc link unavailable** — a help article/doc link can't load → "unavailable — retry/return"; never fabricate guidance.
- **Contextual help unavailable** — fall back gracefully; the underlying surface remains usable.
- **Contact/support unavailable** — present honestly with a retry/alternative; never fabricate a support channel or a ticket.
- **General principle:** honest, recoverable, non-fabricating; Help never invents product facts, concept definitions, or support outcomes.

## N. Progressive Disclosure

- **Always available:** the global **Help** entry point.
- **In context:** lightweight contextual help on the current surface.
- **Through expansion:** product/concept/troubleshooting content; documentation links.
- **Through routing:** **Chat** (project-specific), **Onboarding** (getting-started), **Contact support** (reach a human).
- **Intentionally absent:** ticketing/workflow/task affordances; governance/approval/automation/agent affordances; assessment-changing or reanalysis-triggering controls; scores/percentages or any "project health/readiness/probability" framing; project data presented as help (that is Chat/the surfaces); documentation authoring controls.

## O. Integrity Rules

- **HS-1.** Help **computes nothing** (no scoring/CAF/Reliability/Confidence).
- **HS-2.** Help **generates no findings/recommendations/assessment**; help content is **about OSLO**, not produced project understanding.
- **HS-3.** Help **governs nothing, executes nothing, automates nothing**, and uses **no agents**.
- **HS-4.** Help **creates no tasks** and is **not** a ticketing/workflow/task-management system (contact entry point only; ticketing deferred).
- **HS-5.** Help **changes no assessment**, **triggers no reanalysis**, **resolves no finding**, **accepts no recommendation**; **only reanalysis changes assessment.**
- **HS-6.** **Concept help mirrors the canonical models** and never redefines them; **Outcome Confidence = trust in understanding**, never project health/readiness/probability.
- **HS-7.** **Help is not Chat; Chat is not the help center** — distinct constructs with two-way routing; neither creates the other's content.
- **HS-8.** Contextual help is **non-intrusive**, changes nothing, hosts no structured actions, and preserves the underlying surface.
- **HS-9.** Help **points back to Onboarding** without redefining or gating it.
- **HS-10.** Documentation/support are **surfaced as routes**; Help defines **no documentation authoring/CMS** and **no ticketing workflow**.
- **HS-11.** Help is a **Companion-Surface-class help layer**, **not a destination/Workspace/Panel/Chat/ticketing system**, and hosts **no understanding-changing actions**.
- **HS-12.** **No** APIs, events, implementation, styling, delivery infrastructure, or assessment behavior defined here; no existing model redefined; nothing fabricated.

## P. Conformance Requirements

A conforming Help & Support experience MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:

- **HS-C1.** Be a **lightweight cross-cutting help layer** reachable from global navigation and contextually in surfaces, **not a destination/Workspace** (§D, §F; HS-11). **Fail** if it becomes a destination or a ticketing/workflow system.
- **HS-C2.** Provide the five **help types** (product/concept/contextual/troubleshooting/contact), all **about OSLO**, generating no project understanding (§G; HS-2). **Fail** if Help generates a finding/recommendation/assessment or presents project data as help.
- **HS-C3.** Keep **concept help consistent with the canonical models**, never redefining them; **Confidence = trust in understanding**, never project health/readiness/probability (§G, §H; HS-6). **Fail** if a concept is redefined or Confidence is framed as health/score.
- **HS-C4.** Make **contextual help non-intrusive**, changing nothing and hosting no structured actions, preserving the underlying surface (§H; HS-8). **Fail** if contextual help changes data/assessment or hosts a surface's actions.
- **HS-C5.** Ensure Help **changes no assessment, triggers no reanalysis, resolves no finding, accepts no recommendation, creates no task** (§E.8, §H; HS-5/HS-4). **Fail** if any help action changes assessment or creates a task/ticket workflow.
- **HS-C6.** Keep **Help and Chat distinct** with two-way routing; Help is not the conversational project-answer engine and Chat is not the help center (§I; HS-7). **Fail** if Help answers over project data as Chat or becomes Chat.
- **HS-C7.** Provide a **contact-support entry point** without a ticketing **workflow** (deferred) (§K; HS-4). **Fail** if a ticketing/tracking/SLA workflow is defined.
- **HS-C8.** **Point back to Onboarding** without redefining/gating it (§J; HS-9), and surface docs as routes without defining authoring/CMS (§G; HS-10).
- **HS-C9.** Implement empty states (no results / no contextual help / contact unavailable / unavailable) and honest failure states (help/content/contextual/contact unavailable) that fabricate nothing (§L, §M).
- **HS-C10.** Define **no** governance, execution, automation, agents, task management, APIs, events, implementation, styling, or assessment behavior (HS-3/HS-12; §Q). **Fail if governance/execution/automation/agents/task-management/APIs/assessment behavior appears.**

**Explicit fail conditions.** Conformance is **all-or-nothing**. The experience **fails** if it: generates a finding/recommendation/assessment or presents project data as help; redefines a canonical concept or frames Confidence as project health/readiness/probability/score; changes any assessment, triggers reanalysis, resolves a finding, accepts a recommendation, or creates a task/ticket workflow; becomes a destination/Workspace or a ticketing/workflow system; becomes OSLO Chat or answers conversationally over project data; gates or redefines Onboarding; fabricates product facts/concept definitions/support outcomes; or defines governance, execution, automation, agents, task management, APIs, events, implementation, styling, delivery infrastructure, documentation authoring, or assessment behavior.

## Q. Deferred Items

Explicitly **deferred / out of scope:** support-ticket creation/tracking/status; SLA/escalation workflows; live chat/agent support; AI support agents; documentation authoring/CMS/hosting; in-product guided tours/interactive walkthroughs (beyond re-accessible onboarding); community/forum surfaces; feedback/bug-report workflows; localization of help content; tier-specific support entitlements implementation (tier *visibility* may note support levels per Tier Definitions, but entitlement/billing implementation is deferred); APIs; events; implementation; styling; delivery infrastructure; mobile-specific help behavior; and any numeric/calibration values.

---

*This specification defines the canonical Release 1 Help & Support Experience — a lightweight, cross-cutting, Companion-Surface-class help layer reachable from global navigation and contextually within surfaces, answering "How do users get help, guidance, and support while using OSLO?" It provides five Release 1 help types — product help, concept help (consistent with the canonical CAF/Reliability/Confidence/Finding/Recommendation/MRI models, never redefining them, with Confidence as trust in understanding and never project health/readiness/probability), contextual help, troubleshooting, and a contact-support entry point — plus re-accessible onboarding guidance and documentation links. It is strictly distinct from OSLO Chat (Help explains the product/concepts; Chat explains the user's project understanding) with two-way routing, and it is non-intrusive: opening or using Help changes no comment, finding, recommendation, artifact, or assessment, triggers no reanalysis, and creates no task. Support ticketing/tracking, documentation authoring, guided tours, and agent support are deferred. It defines no governance, execution, automation, agents, task management, APIs, events, implementation, styling, delivery infrastructure, or assessment behavior. Only reanalysis changes assessment.*

## R. Ratified update — adaptive teaching & tour location (DL-088, 2026-07-02)

Ratified by **DL-088** (presentation-only). Teaching/coach copy **sunsets by interaction/proficiency** — it fades once the user has demonstrably learned a flow (a small persisted proficiency store; each teaching message declares a threshold) and is re-enableable from **Settings → Help**. Status/feedback copy is exempt. The **feature tour** is present as a **lightweight, skippable Settings → Help entry** (a first-run invitation, not mandatory) — this narrows the prior "guided tours deferred" note to a minimal re-openable tour. Non-intrusive guarantees stand: help/teaching change no finding/recommendation/assessment and trigger no reanalysis. Visual reference of record: `product-design/oslo_r1_experience_mockup_v2.html`.

**Help & Support Experience Specification v1 complete.**
