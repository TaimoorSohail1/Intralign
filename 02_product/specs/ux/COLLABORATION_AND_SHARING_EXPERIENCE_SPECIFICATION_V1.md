# Collaboration & Sharing Experience Specification v1

**Document Type:** Experience Specification (UX / Interaction Model Only)
**Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Consistent with and subordinate to (authoritative — must not redefine):** `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · `MRI_WORKSPACE_SPECIFICATION_V1.md` · `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` · `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW_SPECIFICATION_V1.md` · `FINDING_PRESENTATION_SPECIFICATION_V1.md` · `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` · `SIXTY_SECOND_ORIENTATION_WORKFLOW_SPECIFICATION_V1.md` · `ORIENTATION_STATE_MODEL_V1.md` · CAF Assessment · Reliability v2 · Confidence v2 · Release 1 Tier Definitions.

> **Non-negotiable constraints.** This is **UX and interaction only**. It must **NOT** define: governance workflows, approval workflows, decision workflows, execution workflows, automation, agents, APIs, events, implementation, permissions architecture, or styling. **The experience presents collaboration. It computes nothing. It generates nothing. It governs nothing. Only reanalysis changes assessment.**
>
> **Preserved invariants.** Artifacts remain the **source of truth**. Findings remain **descriptive**. Recommendations remain **advisory**. **Only reanalysis changes assessment.** **Collaboration never directly changes assessment.** No governance model. No execution model.

---

## A. Purpose

Define the canonical Release 1 **Collaboration & Sharing Experience** governing how users **invite, share, comment, review, collaborate, and participate** within OSLO projects. It defines how **multiple humans interact around project understanding** — improving understanding **together** — while preserving every previously ratified principle (artifacts source of truth; findings descriptive; recommendations advisory; only reanalysis changes assessment; no governance; no execution).

Collaboration's role in OSLO is to let people **build and improve shared understanding** of a project: to discuss what an artifact says, why a weakness exists, and what a recommendation might mean — **not** to manage tasks, approve decisions, or coordinate execution.

## B. Scope

**In scope:** the UX of sharing a project and inviting collaborators; user-visible participant categories; the **surfaces** where collaboration occurs; the **comment** experiences attached to Artifacts, Findings, Recommendations, and the project; activity/discussion history; collaboration behavior during **reanalysis** and **editing**; awareness (mentions/replies/new comments); empty states; progressive disclosure; and the rules/conformance that bound them.

**Out of scope (explicitly):** governance/approval/decision/execution workflows; automation; agents; APIs; events; implementation; **permissions architecture** (logic/enforcement); styling; and any computation (scoring / CAF / Reliability / Confidence) or generation (Findings / Recommendations / assessment objects). The experience **presents collaboration**; it changes no assessment and creates no assessment object.

## C. Collaboration Philosophy

Collaboration in OSLO is **Project Understanding Collaboration** —

- **not** Task Management,
- **not** Governance,
- **not** Execution.

It exists so that **multiple people improve understanding together**, orbiting the objects that carry understanding (Artifact → Finding → Recommendation). People comment to **clarify, question, contextualize, and discuss** understanding; their comments **enrich the human conversation** around the objects but **never alter the objects themselves** and **never change assessment**. The felt experience is *"multiple people improving understanding together,"* not *"multiple people managing work."* **Understanding first; collaboration second; collaboration exists to improve understanding, not to coordinate execution.**

## D. Experience Architecture

Comments **attach to existing objects**; they are not a parallel object hierarchy and create **no new assessment objects**:

```text
Project
   ↓
Artifact
   ↓
Finding
   ↓
Recommendation
   ↓
Comment   ← attaches to any of the above; never replaces or governs them
```

**Rationale.** Anchoring comments to the existing Project / Artifact / Finding / Recommendation objects keeps the **center of gravity on understanding** (Artifact → Finding → Recommendation) and prevents collaboration from becoming the primary object. A comment is a **human annotation in context** — it inherits the context of what it attaches to, so discussion stays where the understanding lives. Comments **orbit** these objects; they **never become the primary object**, never create a new assessment object, and never change the object they attach to. This deliberately avoids a separate "discussion/ticket" hierarchy that would drift toward task management or governance.

## E. Sharing Model

User-facing sharing UX (presentation only — **no permission implementation/architecture**):

- **Invite user** — bring a person into a project (by the product's invitation affordance), presented as adding a participant.
- **Share project** — make a project available to invited participants.
- **Remove share** — remove a participant's access, presented as a reversible sharing change.
- **View shared users** — see who currently has access and their **participant type** (§F).

Sharing is presented as a **human access change**, not a governance act. *(How access is enforced — permissions logic/architecture — is out of scope, §T.)*

## F. Participant Types

User-visible participant categories (**presentation only; no permission logic**):

- **Project Owner** — the person who owns the project; presented as the originating participant.
- **Collaborator** — a participant who can contribute (edit content per the editing workflow, comment, participate).
- **Viewer** — a **view-only** participant who can read understanding and discussion but does not contribute edits/comments where not permitted.

These categories describe **how a participant appears**, not what the system enforces. **What a view-only user sees (Q9):** the project's understanding (artifacts, overlays, findings, recommendations — reliability-qualified, presented), and the discussion/activity, in read-only form — i.e., they can **follow the understanding and the conversation** without contributing. *(Enforcement is permissions architecture — deferred, §T.)*

## G. Collaboration Surfaces

Collaboration can occur at each understanding surface, with a clear purpose at each layer:

| Surface | Collaboration purpose |
|---|---|
| **Project Overview** | Project-wide observations and cross-cutting discussion about overall understanding (§K). |
| **MRI Workspace** | Discussion oriented around **where weakness concentrates** — collaborating on *where to look* (diagnostic discussion), without turning MRI into a tracker. |
| **Artifact Workspace** | Content-centered discussion — commenting on what the artifact **says** (§H). |
| **Finding Panel** | Discussion of **why a weakness exists** — evidence and clarification (§I). |
| **Recommendation Panel** | Discussion of **what could be considered** — evaluating options (§J). |

At every surface, collaboration is **discussion around understanding**, anchored to the object in view; it never becomes work coordination or governance.

## H. Artifact Comment Experience

- **Comment on artifact content** — participants discuss what the content says, anchored to the artifact (and, where useful, to a location within it as an **inline comment**).
- **Comment threads** — replies form threaded discussion attached to the artifact/location.
- **Inline comments** — anchored to a passage/section so discussion stays in context.
- **Artifact discussion** — broader conversation about the artifact as a whole.
- **Content-centered:** the artifact **remains the source of truth and center of gravity**; comments orbit the content and **never replace it** or alter it. Commenting changes no assessment and triggers no reanalysis by itself.

## I. Finding Comment Experience

- **Commenting on findings** — participants discuss a finding in the Finding Panel context.
- **Discussion around findings** — threads exploring the weakness.
- **Evidence discussion** — discussing the evidence the finding rests on (presented per the Finding Presentation spec).
- **Finding clarification discussion** — humans clarifying their shared understanding of the finding.
- **Findings remain descriptive; comments do not alter findings.** A comment never changes a finding's content, type, severity, or lifecycle state, and never resolves it. Findings change **only** through reanalysis. Comments **enrich the human conversation** about a finding without becoming part of the finding object.

## J. Recommendation Comment Experience

- **Recommendation discussion** — participants discuss a recommendation in the Recommendation Panel context.
- **Alternative evaluation discussion** — discussing the **Possible Resolution Paths** (the multiple Recommendations presented together).
- **OSLO Recommended discussion** — discussing the recommendation OSLO surfaces foremost.
- **Selected Path discussion** — discussing which path the team is focusing on.
- **Recommendations remain advisory; comments do not alter recommendations.** OSLO Recommended / Possible Resolution Paths / Selected Path remain **presentation-only** constructs; comments never change them, never apply or execute them, and create **no** Resolution Path / Clarification Candidate / Resolution Candidate object. Recommendations change **only** through reanalysis.

## K. Project-Level Discussion Experience

- **Project-wide comments** — discussion attached to the project as a whole (e.g., from Project Overview).
- **Project observations** — broad human observations about overall understanding.
- **Cross-artifact discussions** — conversation spanning multiple artifacts (anchored to the project, optionally referencing the artifacts involved).
- **No governance workflows:** project-level discussion is **conversation about understanding**, not approval/decision/governance. It produces no decision object, no ratification, no governance state — it simply lets people talk about the project's understanding.

## L. Activity Experience

- **Recent activity** — a view of recent collaboration (new comments, replies, shares, edits-as-surfaced).
- **Discussion history** — the conversation over time, navigable by participants (Q13).
- **Collaboration timeline** — a chronological view of collaboration around the project.
- **Append-only; no deletion model.** Activity and discussion history are **retained**; the experience defines **no deletion** of activity/history and no mutable rewriting of it. Supersession (e.g., an edited comment, if supported) is presented additively, never as destructive erasure. *(How tracking activity (Q12) appears is presentation only — no event/notification infrastructure, §O/§T.)*

## M. Collaboration During Reanalysis

- **Visibility during reanalysis (Q10):** collaboration remains **visible and usable** — participants can keep reading and discussing while reanalysis runs; comments stay attached to their objects.
- **Stale-analysis communication (Q11):** when the analysis is **stale** (content changed since last analysis, per the editing workflow), discussion of findings/recommendations is clearly attributable to the **prior analysis** — the experience surfaces that the understanding under discussion may be **out of date** and awaiting reanalysis, consistent with the Pending Analysis State. Comments are never silently re-pointed to a different analysis.
- **Behavior while updating:** collaboration **changes no assessment**; reanalysis (not commenting) governs assessment. After reanalysis, findings/recommendations may change (weaken / unchanged / superseded / closed); **comments remain attached to the objects they were made on**, with their context preserved — a comment on a superseded finding remains visible in history attributed to that finding.
- Consistent with **"only reanalysis changes assessment."**

## N. Collaboration During Editing

- **Visibility of edits:** content edits are **visibly surfaced and attributed** within the shared artifact (per `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW_SPECIFICATION_V1.md`), so collaborators can see who changed what.
- **Collaboration around edits:** participants can discuss edits in context (artifact/inline comments) — discussion **orbits** the content; it neither performs the edit nor changes assessment.
- **Relationship to conflict surfacing:** when concurrent edits diverge, **conflicts are surfaced explicitly** (per the editing workflow) — collaboration presents the conflict for human reconciliation; it performs **no silent merge**, no auto-resolution, and no governance over the content.
- Consistent with the editing workflow: editing changes content only; only reanalysis changes assessment.

## O. Notifications & Awareness

User-visible awareness only (**no notification infrastructure, no event definitions**):

- **Mentions** — a participant is referenced and made aware in context.
- **Replies** — awareness that someone replied in a thread.
- **New comments** — awareness of new discussion on objects the user follows/participates in.
- **Shared project activity** — awareness of relevant collaboration on a shared project.

Awareness is presented as **human-facing cues**; the underlying delivery/event mechanism is out of scope (§T).

## P. Empty States

The experience must **distinguish**:

- **No collaborators** — the project is not shared / has only the owner (a neutral "invite people to collaborate" state).
- **No comments** — an object/surface has no discussion yet (distinct from "no collaborators").
- **No activity** — there has been no recent collaboration activity (distinct from "no comments anywhere").
- **Unavailable** — collaboration/discussion is temporarily unavailable (distinct from "none").

## Q. Progressive Disclosure

- **Immediately visible:** the understanding objects (Artifact / Finding / Recommendation) and presence of discussion (e.g., comment indicators) — understanding stays primary; comments orbit.
- **In context:** comment threads on the object in view (inline on artifacts; in the Finding/Recommendation Panels).
- **Through expansion:** full threads, replies, and participant detail.
- **Through activity history:** recent activity, discussion history, and the collaboration timeline (§L).
- **Intentionally absent:** anything that makes comments the primary object; scores/percentages/ranks; governance/approval/decision/execution affordances; automation/agents; finding/recommendation/assessment generation or mutation.

## R. Integrity Rules

- **CS-1.** Collaboration exists to **improve understanding** — it is Project Understanding Collaboration, not task management, governance, or execution.
- **CS-2.** **Comments never change assessment** (CAF / Reliability / Confidence). Only reanalysis changes assessment.
- **CS-3.** **Comments never change findings** — findings remain descriptive; not edited, resolved, or relabeled by comments.
- **CS-4.** **Comments never change recommendations** — recommendations remain advisory; OSLO Recommended / Possible Resolution Paths / Selected Path stay presentation-only.
- **CS-5.** **Comments never execute work** — no execution is introduced or implied.
- **CS-6.** **Comments never govern work** — no approval/decision/governance is introduced or implied.
- **CS-7.** **Comments never create new assessment objects** (no finding/recommendation/CAF/Reliability/Confidence/Resolution/Clarification object); comments attach to existing objects.
- **CS-8.** Comments **orbit** Artifact / Finding / Recommendation / Project; they **never become the primary object**; the center of gravity stays Artifact → Finding → Recommendation.
- **CS-9.** Artifacts remain the **source of truth**; comments never replace or alter content.
- **CS-10.** Activity and discussion **history are append-only** — no deletion model, no mutable rewriting; supersession is additive.
- **CS-11.** During reanalysis/staleness, discussion of findings/recommendations is attributable to the **prior analysis** and clearly communicated as potentially stale; comments are never silently re-pointed.
- **CS-12.** Collaboration around editing **surfaces conflicts explicitly** and performs **no silent merge** or governance over content (per the editing workflow).
- **CS-13.** Participant types and sharing are **presentation only** — **no permission logic/architecture** is defined.
- **CS-14.** Awareness is **human-facing presentation only** — **no notification infrastructure or event definitions**.
- **CS-15.** The experience **computes nothing and generates nothing**; **no APIs, events, implementation, or styling** are defined; no existing model is redefined.

## S. Conformance Requirements

A conforming Collaboration & Sharing experience MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:

- **CS-C1.** Attach comments to **existing** Project / Artifact / Finding / Recommendation objects, creating **no new assessment object** and keeping comments non-primary (§D; CS-7/CS-8). **Fail** if a comment creates a finding/recommendation/assessment/Resolution/Clarification object.
- **CS-C2.** Keep **artifact content primary**; comments orbit and never replace/alter content (§H; CS-9). **Fail** if comments replace or modify artifact content.
- **CS-C3.** Ensure **comments do not alter findings** — descriptive, not edited/resolved by comments (§I; CS-3). **Fail if comments directly alter findings.**
- **CS-C4.** Ensure **comments do not alter recommendations** — advisory; OSLO Recommended / Possible Resolution Paths / Selected Path presentation-only (§J; CS-4). **Fail if comments directly alter recommendations.**
- **CS-C5.** Ensure **no collaboration action changes assessment**; only reanalysis does (§M; CS-2). **Fail if comments alter assessment.**
- **CS-C6.** Expose **no governance/approval/decision** affordance in any collaboration surface (§K; CS-6). **Fail if governance workflows appear.**
- **CS-C7.** Expose **no execution/automation/agent** affordance (CS-5; CS-15). **Fail if execution workflows appear.**
- **CS-C8.** Maintain **append-only** activity/discussion history — no deletion model, no mutable rewriting (§L; CS-10). **Fail** if history is deleted or rewritten destructively.
- **CS-C9.** Communicate **staleness** during reanalysis and attribute finding/recommendation discussion to the prior analysis; preserve comment attachment across supersession (§M; CS-11). **Fail** if stale discussion is presented as current or comments are silently re-pointed.
- **CS-C10.** Surface **edit conflicts explicitly** with **no silent merge** (§N; CS-12). **Fail** if conflicts are auto-resolved silently.
- **CS-C11.** Present participant types/sharing and awareness as **presentation only** — no permissions logic, no notification/event infrastructure (§E/§F/§O; CS-13/CS-14). **Fail** if permission enforcement, events, or APIs are defined here.
- **CS-C12.** Implement empty states distinguishing **no collaborators / no comments / no activity / unavailable** (§P).

**Explicit fail conditions.** Conformance is **all-or-nothing**. The experience **fails** if: comments directly alter findings; comments directly alter recommendations; comments alter assessment; comments create a new assessment object; governance/approval/decision workflows appear; execution/automation/agent workflows appear; comments become the primary object or replace artifact content; activity/discussion history is deleted or destructively rewritten; stale discussion is presented as current; edit conflicts are silently merged; or permissions architecture, notification/event infrastructure, APIs, events, implementation, or styling are defined.

## T. Deferred Items

Explicitly **deferred / out of scope:** permissions architecture; governance; approvals; workflows (decision/approval/execution); automation; agents; APIs; events; implementation; styling; notification/delivery infrastructure; exact comment-anchoring/threading mechanics; concurrency/merge mechanics (owned by the editing workflow); numeric tier boundaries; and any calculation/scoring/generation.

---

*This specification defines the canonical Release 1 Collaboration & Sharing Experience — how multiple humans improve project understanding together. Comments orbit existing Project / Artifact / Finding / Recommendation objects (Project → Artifact → Finding → Recommendation → Comment), never becoming the primary object and never creating a new assessment object. Artifacts remain the source of truth, findings remain descriptive, recommendations remain advisory, and only reanalysis changes assessment — collaboration changes none of it. Sharing, participant types, and awareness are presentation only (no permissions architecture, no notification/event infrastructure); activity and discussion history are append-only; collaboration during reanalysis communicates staleness and preserves comment attachment across supersession; and collaboration during editing surfaces conflicts explicitly with no silent merge. It is UX/interaction only: no governance, approval, decision, execution, automation, agents, APIs, events, implementation, or styling — understanding first, collaboration second, collaboration to improve understanding, not to coordinate execution.*

**Collaboration & Sharing Experience Specification v1 complete.**
