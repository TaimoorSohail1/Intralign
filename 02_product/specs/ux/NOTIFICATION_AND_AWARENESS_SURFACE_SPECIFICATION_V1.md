# Notification & Awareness Surface Specification v1

**Document Type:** Experience Specification (UX / Interaction Model Only)
**Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Consistent with and subordinate to (authoritative — must not redefine):** `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md` · `OSLO_CHAT_AND_CLARIFICATION_EXPERIENCE_SPECIFICATION_V1.md` · `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1.md` · `PROJECT_DASHBOARD_AND_PROJECT_LIST_EXPERIENCE_SPECIFICATION_V1.md` · `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW_SPECIFICATION_V1.md` · `ORIENTATION_STATE_MODEL_V1.md` · `UNDERSTANDING_JOURNEY_AND_SURFACE_TRANSITION_EXPERIENCE_SPECIFICATION_V1.md` · `UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION_001.md` · CAF Assessment · Reliability v2 · Confidence v2.

> **Non-negotiable constraints.** UX / interaction model only. The surface **presents awareness only. It computes nothing, generates nothing, governs nothing, executes nothing, and changes no assessment.** It must **NOT** define: notification infrastructure, delivery mechanics, push/email notifications, APIs, events, implementation, styling, permission enforcement, governance, execution, automation, agents, approvals, task management, assessment generation, finding generation, or recommendation generation. **Only reanalysis changes assessment.** Artifacts remain the source of truth, Findings descriptive, Recommendations advisory, MRI the diagnostic discovery experience.

> **Position in the architecture.** This surface **completes the collaboration loop** by giving users a clear place to see **what changed, what needs attention, and where to return** — without becoming task management, governance, approval, execution, automation, or workflow.

---

## A. Purpose

Define the canonical Release 1 **Notification & Awareness Surface**. It answers:

> **"Where do users see awareness cues, mentions, replies, shared-project activity, and collaboration updates?"**

It gives users a single, lightweight place to **see what changed**, **what needs attention**, and **where to return** — and routes them to the **source context** — without creating tasks, obligations, governance, approvals, execution, automation, or workflow.

## B. Scope

**In scope:** the awareness entry point and surface structure; unread/new-activity visibility; mentions, replies, new comments, shared-project activity, project shared with me, invitation awareness; stale-analysis awareness; reanalysis-complete awareness; collaboration-conflict awareness; navigation from an awareness item to its source context; empty states; failure states; progressive disclosure; integrity rules; conformance requirements.

**Out of scope:** notification **infrastructure**; **delivery mechanics**; **push/email** notifications; **APIs**; **events**; implementation; styling; **permission enforcement**; governance; execution; automation; agents; approvals; task management; assessment/finding/recommendation **generation**. The surface **presents awareness and routes**; it produces and mutates nothing.

## C. Awareness Philosophy

Awareness exists to keep users **oriented to change** without converting change into work to be managed. It is a **calm pointer**, not a queue of obligations: it shows that something happened and **routes to where it happened**, then gets out of the way. It keeps **understanding the center of gravity** — awareness items point to collaboration and understanding context, never become the content themselves, and never imply a task, approval, or status. It is rigorously **non-mutating**: seeing or opening an awareness item changes no comment, finding, recommendation, or assessment; **only reanalysis changes assessment.**

## D. Construct Classification

Per the ratified governing taxonomy (`UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION_001.md`), the Notification & Awareness Surface is classified as a **Companion-Surface-class awareness layer**:

| Attribute | Classification |
|---|---|
| **Type** | **Companion Surface** (a persistent visibility + routing surface), in its **awareness** variant — a lightweight awareness layer / inbox. |
| **Purpose** | continuous **awareness visibility** + routing to source context. |
| **Navigation** | **not a destination**; a persistent layer reachable from global navigation; **routes** into Workspaces/Panels/Collaboration. |
| **Context** | reads/scopes to existing activity (read-only); presentation-only. |
| **Independent?** | No — a layer over the app, not a standalone place. |
| **Destination?** | **No.** |
| **Hosts actions?** | **No structured actions** — presents and routes only (read/unread is presentation state, not an action on understanding). |
| **Contains?** | **launches/routes** into surfaces; **does not contain** Workspaces/Panels/Chat. |
| **Not** | not a Workspace, not a Panel, not Chat (Interaction Layer), not a dashboard/cockpit, not an Understanding Object. |

This classification binds the rest of the spec: anything that would make the surface a destination, an action host, a task queue, or an assessment-changer is **out of type** and forbidden (§R/§S).

## E. Owner-Level Decisions — Resolutions (Q1–Q15)

### Q1 — What is the surface?
**Option C — a lightweight awareness layer / inbox** (Companion-Surface-class, §D). Not a global destination workspace (A), not a workspace-level surface (B), not project-scoped-only (D); it spans the user's projects but stays a **lightweight layer**, not a destination.

### Q2 — Where is it accessed?
Primary entry: a persistent **global-navigation** awareness entry point (bell/inbox affordance). Lightweight **indicators** may also appear at the **Project Dashboard** (per-project cue), **Collaboration surfaces** (in-context), and the **Understanding Companion** (indicator only, §N). **Chat** may *explain* an item but is **not** the access point (§M); **Settings** manages *preferences*, not the surface. One full surface; indicators are cues that route to it or to source.

### Q3 — Awareness categories (Release 1 vs. deferred)
| Category | Release 1? |
|---|---|
| **Mentions** | ✅ |
| **Replies** | ✅ |
| **New comments** | ✅ |
| **Shared-project activity** | ✅ |
| **Project shared with me** | ✅ |
| **Invitation received** | ✅ |
| **Reanalysis complete** | ✅ |
| **Reanalysis failed** | ✅ |
| **Stale analysis** | ✅ (awareness cue; §K) |
| **Collaboration conflict** | ✅ (routes to artifact editing context; §I) |

All ten listed categories are **Release 1**, as **presentation groupings over existing activity** (no new object). Anything beyond these (system/product announcements, digests) is **deferred** (§T).

### Q4 — What does an awareness item contain?
Visible structure only (no APIs, events, database fields, or implementation): **source object · actor/participant · project · surface context · activity type · timestamp/recency · short summary · read/unread status · navigation target** (§H).

### Q5 — How does navigation work?
Each item routes to its **source context**, preserving context, never fabricating destination content, never changing assessment:
mention → comment context · reply → thread context · new comment → object discussion · shared project → Project Overview · invitation → shared-project entry · reanalysis complete → Project Overview / Artifact / MRI (per context) · reanalysis failed → relevant prior-analysis context · stale analysis → Artifact / Project Overview · collaboration conflict → artifact editing context (§I).

### Q6 — Does awareness create tasks?
**No.** Awareness **does not create tasks**, **does not assign work**, **does not imply obligation**, **is not workflow management.**

### Q7 — Does awareness change assessment?
**No.** Awareness **changes no assessment**, **does not trigger reanalysis**, **does not resolve findings**, **does not accept recommendations**; **only reanalysis changes assessment.**

### Q8 — Read/unread?
**Presentation state only.** Must not imply completion, approval, governance, work status, or assessment state; marking read changes nothing (§J).

### Q9 — Stale analysis in awareness?
A **stale-analysis cue** signals understanding now reflects a **previous analysis**: stale means previous analysis, **never current**; awareness **does not trigger reanalysis**; **reanalysis is the only path** to updated understanding (§K).

### Q10 — Collaboration comments?
**Comments remain attached to objects**; awareness **points to** comments; it **does not become / create / modify** comments (§L).

### Q11 — OSLO Chat?
**Chat may explain** awareness context; **Chat does not create awareness items**; **awareness does not create chat**; **Chat is not the notification center** (§M).

### Q12 — Understanding Companion?
The **Companion may show a lightweight awareness indicator** while the **full awareness surface remains separate** (§N).

### Q13 — Empty states?
Distinguish: no awareness items · no unread items · no mentions · no project activity · unavailable (§O).

### Q14 — Failure states?
Define: awareness unavailable · target unavailable · stale/superseded target context · project no longer accessible · honest retry/return; no fabrication (§P).

### Q15 — Deferred?
Push notifications · email notifications · notification **delivery infrastructure** · user-configurable notification **routing** · real-time **event** infrastructure · notification **APIs** · automation rules · workflow escalations (§T).

## F. Surface Architecture

A **lightweight awareness layer / inbox** (Companion-Surface-class):

```text
Global navigation
   └─ Awareness entry point (unread cue)
        ▼
   Awareness Surface (lightweight inbox)
     • grouped by recency / unread
     • each item: source object · actor · project · surface context ·
       activity type · recency · short summary · read/unread · → route
        ▼ (select item)
   Source context (Overview / Artifact / MRI / Finding Panel /
                   Recommendation Panel / Collaboration thread / project entry)
```

- **Entry point** persistent in global navigation with an **unread** indicator; lightweight indicators may also appear on Dashboard, Collaboration surfaces, and the Companion (§N).
- The surface **lists awareness items** (grouped by recency/unread) and **routes** each to its source context. It hosts **no structured actions** (no accept/resolve/approve/assign), per its construct type (§D).
- It is **not a destination workspace** and **not** a work queue — a lightweight, dismissible awareness layer.

## G. Awareness Categories

The ten Release 1 categories (§E Q3) are **presentation groupings over existing collaboration/analysis activity** — they create **no new object**:
- **Collaboration-sourced:** mentions, replies, new comments, shared-project activity, project shared with me, invitation received, collaboration conflict — subordinate to `COLLABORATION_AND_SHARING_…`.
- **Analysis-state-sourced:** reanalysis complete, reanalysis failed, stale analysis — subordinate to the Orientation State Model / editing workflow; presented, never computed or triggered here.

## H. Awareness Item Structure

Each item presents exactly: **source object · actor/participant · project · surface context · activity type · timestamp/recency · short summary · read/unread status · navigation target.** The item is a **pointer**: it summarizes and routes; it is **not** the object/comment/finding/recommendation/assessment it references, and carries **no** action affordance beyond "open the source." No APIs, events, database fields, or implementation are implied.

## I. Navigation & Context Preservation

- Selecting an item **routes to its source context** per §E Q5, **preserving context** (the destination opens where the activity is, in the right project/surface).
- Routing obeys all surface rules — a recommendation-related item routes through its **Finding** (Recommendation Panel only in Finding context); a finding item opens the **Finding Panel** in context; a comment item opens the **object's discussion**; a collaboration conflict opens the **artifact editing context**.
- Routing **never fabricates** destination content and **never changes assessment**; an unavailable/superseded target triggers the failure states (§P), not invented content.
- Awareness **routes**; it embeds no investigation/editing and hosts no structured actions.

## J. Read / Unread Presentation

- Read/unread is **presentation state only** — a visibility convenience.
- It **must not imply** completion, approval, governance, work status, or assessment state.
- Marking read/unread (individually or "mark all read") **changes nothing** about the underlying object/comment/finding/recommendation/assessment, and **triggers no reanalysis**.
- Unread is a **cue to look**, never an obligation (Q6).

## K. Stale & Reanalysis Awareness

- **Reanalysis complete** → an item noting updated understanding is available, routing to Overview/Artifact/MRI as relevant.
- **Reanalysis failed** → an item noting the failure honestly, routing to the relevant prior-analysis context where retry is available (per the editing workflow); awareness fabricates no result and triggers nothing.
- **Stale analysis** → a cue that understanding reflects **previous analysis**; **never presented as current**; **does not trigger reanalysis**; routes to the artifact/overview; **reanalysis remains the only path** to updated understanding.
- Awareness **presents** these analysis states (owned upstream by the Orientation State Model / editing workflow); it never computes, triggers, or changes them.

## L. Collaboration Relationship

- **Comments remain attached to objects** (Collaboration spec); the awareness surface **points to** them.
- Awareness **does not become** the comment, **does not create** comments, and **does not modify** comments — it is a pointer that routes to the comment in its object/thread context.
- Collaboration-conflict awareness routes to the **artifact editing context** where the conflict is surfaced (per the editing workflow); awareness neither resolves nor merges anything.

## M. Chat Relationship

- **Chat may explain** awareness context (the user can ask "what changed here?"); routing from an item may lead to a surface where Chat is available.
- **Chat does not create awareness items; awareness does not create chat; Chat is not the notification center.** Distinct layers: Chat = conversational Interaction Layer; this surface = awareness layer.

## N. Companion Relationship

- The **Understanding Companion may show a lightweight awareness indicator** (e.g., an unread cue) as a convenience.
- The **full awareness surface remains separate** — the Companion does not embed, host, or duplicate it, and hosts no structured actions. The indicator routes to the awareness surface or source; it is not the surface.

## O. Empty States

- **No awareness items** — a neutral "you're all caught up" state.
- **No unread items** — items exist but all are read ("nothing new"), distinct from "no items at all."
- **No mentions** — neutral per-category empty state.
- **No project activity** — neutral state for a project/scope with no recent activity.
- **Unavailable** — the surface/data is temporarily unavailable (§P), distinct from "empty."

## P. Failure States

- **Awareness unavailable** — show "awareness unavailable — retry"; the rest of the app remains usable; fabricate no items.
- **Target unavailable** — selecting an item whose target can't load shows "unavailable — retry/return" **without** fabricating the destination's content; the user returns safely.
- **Stale / superseded target context** — if an item points to now-superseded context (e.g., a superseded finding/comment), route to the **retained prior** context clearly marked as prior (append-only), never re-presenting it as current; never invent current content.
- **Project no longer accessible** — if access was removed, say so plainly and return the user to a safe surface (Workspace Home); no fabricated access. *(Permission enforcement itself is out of scope; this is the honest presentation of an inaccessible target.)*
- **General principle:** honest, recoverable, non-fabricating; awareness never invents activity, content, or access.

## Q. Progressive Disclosure

- **Always available:** the global awareness entry point with an **unread cue**.
- **One interaction away:** the lightweight awareness list (grouped by recency/unread) with per-item summaries.
- **Through routing:** the **source context** (object/thread/surface) for full detail.
- **Through Chat (optional):** explanation of an item's context.
- **Intentionally absent:** task/assignment/approval/governance/execution affordances; assessment-changing or reanalysis-triggering controls; scores/percentages; the comment/finding/recommendation content itself (awareness points, never hosts); delivery configuration (deferred).

## R. Integrity Rules

- **NA-1.** The surface **computes nothing** (no scoring/CAF/Reliability/Confidence).
- **NA-2.** The surface **generates nothing** (no findings/recommendations/comments/assessment); awareness items are **pointers over existing activity**, not new objects.
- **NA-3.** The surface **governs nothing, executes nothing, automates nothing** — no governance/approval/execution/agent/automation.
- **NA-4.** Awareness **creates no tasks, assigns no work, implies no obligation**, and **is not workflow management.**
- **NA-5.** Awareness **changes no assessment**, **triggers no reanalysis**, **resolves no finding**, **accepts no recommendation**; **only reanalysis changes assessment.**
- **NA-6.** **Read/unread is presentation state only** — never completion/approval/governance/work/assessment status; marking read changes nothing.
- **NA-7.** Awareness **points to** comments; it **does not become/create/modify** comments (Collaboration spec governs comments).
- **NA-8.** Awareness **points to** findings/recommendations via their proper context (Recommendation via Finding); it never reframes them or hosts their structured actions.
- **NA-9.** **Stale is previous analysis, never current**; awareness surfaces it without triggering reanalysis.
- **NA-10.** Routing **preserves context** and **never fabricates** destination content/activity/access.
- **NA-11.** **Chat is not the notification center**; Chat may explain, not create awareness; awareness does not create chat.
- **NA-12.** The **Companion may show an indicator only**; the full surface stays separate; neither hosts structured actions.
- **NA-13.** The surface is a **Companion-Surface-class awareness layer**, **not a destination/Workspace/Panel/Chat/dashboard**, and hosts **no structured actions** (§D).
- **NA-14.** **No** notification/delivery infrastructure, event definitions, APIs, implementation, styling, or **permission enforcement** defined here; no existing model redefined.

## S. Conformance Requirements

A conforming Notification & Awareness Surface MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:

- **NA-C1.** Be a **Companion-Surface-class awareness layer/inbox** reachable from global navigation (with optional Dashboard/Collaboration/Companion indicators), **not a destination**, hosting **no structured actions** (§D, §F; NA-13). **Fail** if it becomes a destination or hosts structured actions.
- **NA-C2.** Present the Release 1 **categories** as groupings over existing activity, creating **no new object** (§G; NA-2). **Fail** if awareness generates a finding/recommendation/comment/object.
- **NA-C3.** Present each **item** with the §H fields and **route to source context** preserving context, **never fabricating** destination content and **never changing assessment** (§H, §I; NA-5/NA-10). **Fail** if a destination's content/activity/access is fabricated or assessment changes.
- **NA-C4.** Treat **read/unread as presentation only**, implying no completion/approval/work/assessment status, changing nothing on mark-read (§J; NA-6). **Fail** if read/unread implies status or changes an object.
- **NA-C5.** Ensure awareness **creates no tasks/obligations/assignments** and **is not workflow** (Q6; NA-4). **Fail if task management / assignment / obligation / workflow appears.**
- **NA-C6.** Ensure awareness **changes no assessment, triggers no reanalysis, resolves no finding, accepts no recommendation** (Q7; NA-5). **Fail if any awareness action changes assessment or triggers reanalysis.**
- **NA-C7.** Surface **stale as previous analysis**, never current, without triggering reanalysis (§K; NA-9). **Fail** if stale is presented as current or reanalysis is triggered.
- **NA-C8.** **Point to** comments/findings/recommendations in proper context (Recommendation via Finding); never become/create/modify them or host their actions (§L; NA-7/NA-8). **Fail** if awareness modifies a comment or opens a Recommendation outside Finding context.
- **NA-C9.** Keep **Chat not the notification center** and the **Companion indicator-only** (§M, §N; NA-11/NA-12).
- **NA-C10.** Implement empty states (no items / no unread / no mentions / no project activity / unavailable) and honest failure states (unavailable / target unavailable / superseded / no access) that fabricate nothing (§O, §P).
- **NA-C11.** Define **no** notification/delivery infrastructure, events, APIs, implementation, styling, or permission enforcement (NA-14; §T). **Fail** if delivery logic / events / APIs / permission enforcement are defined.

**Explicit fail conditions.** Conformance is **all-or-nothing**. The surface **fails** if it: creates tasks/assignments/obligations or becomes workflow; changes any assessment, triggers reanalysis, resolves a finding, or accepts a recommendation; generates a finding/recommendation/comment/object; lets read/unread imply completion/approval/work/assessment status; presents stale as current or triggers reanalysis; becomes/creates/modifies a comment or opens a Recommendation outside Finding context; fabricates destination content/activity/access on routing or failure; becomes a destination or hosts structured actions; takes on the role of Chat or is embedded as the full surface in the Companion; or defines notification/delivery infrastructure, events, APIs, implementation, styling, or permission enforcement.

## T. Deferred Items

Explicitly **deferred / out of scope:** push notifications; email notifications; notification **delivery infrastructure**; user-configurable notification **routing**; real-time **event** infrastructure; notification **APIs**; **automation rules**; **workflow escalations**; permission **enforcement** (this surface presents access honestly but enforces nothing); system/product-announcement categories; digest/summary notifications; mobile-specific awareness behavior; visual/styling realization; implementation; and any numeric/calibration values.

---

*This specification defines the canonical Release 1 Notification & Awareness Surface — a Companion-Surface-class lightweight awareness layer/inbox reachable from global navigation (with optional Dashboard/Collaboration/Companion indicators) that answers "Where do users see awareness cues, mentions, replies, shared-project activity, and collaboration updates?" It presents ten Release 1 categories (mentions, replies, new comments, shared-project activity, project shared with me, invitation received, reanalysis complete, reanalysis failed, stale analysis, collaboration conflict) as groupings over existing activity; each item presents source object, actor, project, surface context, activity type, recency, short summary, and read/unread, and routes to its source context preserving context, fabricating nothing, and changing no assessment. It completes the collaboration loop while remaining strictly presentation-only: it creates no tasks/obligations, is not workflow, changes no assessment, triggers no reanalysis, resolves no finding, accepts no recommendation; read/unread is presentation state only; comments stay on their objects (awareness points, never becomes/creates/modifies them); stale is shown as previous analysis and never as current; Chat is not the notification center and the Companion shows an indicator only. It defines no notification/delivery infrastructure, events, APIs, implementation, styling, or permission enforcement. Only reanalysis changes assessment.*

**Notification & Awareness Surface Specification v1 complete.**
