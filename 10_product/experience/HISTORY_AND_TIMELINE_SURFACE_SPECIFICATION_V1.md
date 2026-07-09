# History & Timeline Surface Specification v1

**Document Type:** Experience Specification (UX / Interaction Model Only)
**Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Construct type:** **Secondary Project-Context Surface / History Surface** — mapped to the ratified taxonomy as a **Companion-Surface-class** surface (presents + routes; hosts no structured actions; not a primary destination) (§D).
**Consistent with and subordinate to (authoritative — must not redefine):** `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW_SPECIFICATION_V1.md` · `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` · `FINDING_PANEL_SPECIFICATION_V1.md` · `RECOMMENDATION_PANEL_SPECIFICATION_V1.md` · `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md` · `NOTIFICATION_AND_AWARENESS_SURFACE_SPECIFICATION_V1.md` · `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1.md` · `UNDERSTANDING_JOURNEY_AND_SURFACE_TRANSITION_EXPERIENCE_SPECIFICATION_V1.md` · `ORIENTATION_STATE_MODEL_V1.md` · `UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION_001.md` · CAF Assessment · Reliability v2 · Confidence v2.

> **Non-negotiable constraints.** UX / interaction model only. The surface **presents retained history only. It computes nothing, generates nothing, governs nothing, executes nothing, and changes no assessment.** It must **NOT** define: an audit/compliance system, governance approvals, execution history, task history, APIs, events, implementation, styling, database design, mutation/deletion rules beyond presentation, assessment computation, finding generation, or recommendation generation. **Only reanalysis changes assessment.** Artifacts remain the source of truth, Findings descriptive, Recommendations advisory, MRI the diagnostic discovery experience.

> **Position in the architecture.** This surface makes **prior states visible and traceable** — *how project understanding, artifacts, findings, recommendations, comments, sharing, and reanalysis changed over time* — **without** becoming governance, audit approval, task history, execution history, or a mutable log. It complements the in-context histories already defined in the Artifact/Finding/Recommendation/Collaboration specs by **aggregating and linking** them.

---

## A. Purpose

Define the canonical Release 1 **History & Timeline Surface**. It answers:

> **"Where do users inspect how project understanding, artifacts, findings, recommendations, comments, sharing, and reanalysis changed over time?"**

It makes **prior states visible and traceable** for understanding — append-only, honestly labeled, routed to retained context — without becoming an audit/approval system, task/execution history, or a mutable log.

## B. Scope

**In scope:** the project-level timeline; artifact history; analysis/reanalysis history; finding history; recommendation history; comment/discussion history **references**; supersession history; stale/prior-state labeling; navigation from a timeline item to its **retained context**; empty states; failure states; progressive disclosure; integrity rules; conformance requirements.

**Out of scope:** audit/compliance system; governance approvals; execution history; task history; APIs; events; implementation; styling; database design; mutation/deletion rules beyond presentation; assessment computation; finding/recommendation generation. The surface **presents retained history and routes**; it produces and mutates nothing.

## C. History Philosophy

History exists to make **the evolution of understanding visible and traceable** — not to certify, approve, or audit it. It is a **read-only window onto retained prior states**: it shows what changed, when, and lets the user return to the retained context, while always distinguishing **prior** from **current**. It keeps **understanding the center of gravity** — timeline items point to retained understanding context, never become that context, and never imply approval, compliance, or work status. It is rigorously **non-mutating** and **append-only in presentation**: viewing history changes no comment, finding, recommendation, artifact, or assessment; **only reanalysis changes assessment.**

## D. Construct Classification

The History & Timeline Surface is a **Secondary Project-Context Surface**, mapped within the ratified governing taxonomy (`UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION_001.md`) to the **Companion-Surface class** (the visibility + routing family) — it is **not** a new sixth construct type:

| Attribute | Classification |
|---|---|
| **Type** | **Companion-Surface-class**, *history* variant — a project-context visibility/routing surface presenting retained history. |
| **Purpose** | make retained prior states **visible and traceable**, and route to retained context. |
| **Navigation** | a **secondary** project-context surface (reachable within a project; the Navigation spec lists History/Activity as *secondary*, never primary) — **not a primary destination/Workspace**. |
| **Context** | reads retained history (read-only); scopes to the project/object. |
| **Independent?** | No — secondary to the project's primary surfaces. |
| **Destination?** | **Not a primary destination**; it is a secondary project-context surface that presents and routes. |
| **Hosts actions?** | **No structured actions** — no restore/rollback/approve/edit/delete; viewing only (restore/rollback is **deferred**, §T). |
| **Contains?** | **routes** into retained object/version/thread context; **does not contain** Workspaces/Panels. |
| **Not** | not a Workspace, not a Panel, not Chat, not an Understanding Object, **not an audit log / governance / approval / compliance system**. |

This classification binds the spec: anything that would make History a primary destination, an action host (restore/approve/delete), a mutable log, or an audit/compliance system is **out of type** and forbidden (§R/§S).

## E. Owner-Level Decisions — Resolutions (Q1–Q14)

### Q1 — What is the History & Timeline Surface?
**Resolution: Option A — a project-level secondary surface** that aggregates the project's retained history, **complemented by** the in-context histories already defined inside each object (Option C remains true: artifacts/findings/recommendations/comments keep their own in-context history; this surface **aggregates and links** them). **Not** a workspace-level global cross-project history (B); **not** a full audit log (D — explicitly excluded). Best Release 1 model: **A (project-level secondary surface) + existing in-context histories.**

### Q2 — Where is history accessed?
**Resolution.** Access points: **Project Overview** (primary entry to the project timeline), **Global Navigation / Project Dashboard** (route into a project's history), and **in-context** from the **Artifact Workspace, Finding Panel, Recommendation Panel, and Collaboration surfaces** (each object's history opens its slice of the timeline), and from the **Notification & Awareness Surface** (an awareness item may route into history). All are **entry points**; the surface itself is one project-context history surface.

### Q3 — History categories (Release 1 vs. deferred)
| Category | Release 1? |
|---|---|
| **Artifact saved versions** | ✅ |
| **Analysis / reanalysis runs** | ✅ |
| **Stale-analysis transitions** | ✅ |
| **Finding lifecycle changes** | ✅ |
| **Finding supersession** | ✅ |
| **Recommendation lifecycle changes** | ✅ |
| **Recommendation supersession** | ✅ |
| **Selected-recommendation history** | ✅ |
| **Comments / discussion references** | ✅ (references only; §N) |
| **Sharing / collaboration activity references** | ✅ (references only) |
| **Notification / awareness references** | ✅ (references only; §M — awareness items appear in the retained timeline, never duplicated) |

All eleven listed categories are **Release 1**, as **presentation over already-retained history** (no new object, no new retention mechanism). Anything beyond these (execution/task history, compliance audit categories) is **out of scope / deferred** (§T).

### Q4 — What does a history item contain?
**Resolution (visible structure only — no APIs/events/database fields/implementation):** **timestamp/recency · source object · project · surface context · actor / system source (where relevant) · change type · short summary · prior/current marker · navigation target** (§H).

### Q5 — How does timeline navigation work?
**Resolution.** Each item routes to its **retained context**, preserving context, never fabricating content, never changing assessment:
artifact version → the retained artifact version context · reanalysis complete → the relevant updated-understanding context · reanalysis failed → the last-known-good / retry context · finding superseded → **both** the prior finding **and** the superseding finding · recommendation superseded → **both** the prior **and** superseding recommendation · selected-recommendation history → the associated **Finding** then the **Recommendation Panel** (Recommendation only in Finding context) · comment history → the comment thread context · sharing activity → the collaboration context · awareness item → its **relevant source context or retained prior context** (§I).

### Q6 — What is append-only history?
**Resolution.** History is **retained**; prior states are **never silently overwritten**; **deletion/mutation affordances are not exposed in Release 1**; **supersession is additive**; and history presentation **does not imply governance/audit compliance** (§J).

### Q7 — How are prior states labeled?
**Resolution.** Labels: **current · prior · superseded · closed · stale · failed · unavailable.** **Prior states must never be presented as current** (§K).

### Q8 — Does history change assessment?
**Resolution: No.** **Viewing history changes no assessment**; **viewing prior context changes no current state**; **history does not trigger reanalysis**; **only reanalysis changes assessment.** *(Restore/rollback is not a Release 1 affordance — §T; viewing a prior version never alters the current one.)*

### Q9 — Does history create governance?
**Resolution: No.** History **is not approval, not audit certification, not a decision record, not compliance evidence** — it is **traceability for understanding only** (§J/§R).

### Q10 — Relationship to notifications?
**Resolution.** **Awareness points to recent change**; **history preserves the broader retained timeline**; **notification items may route into history**; **history does not create notifications**; **notifications do not mutate history** (§M).

### Q11 — Relationship to collaboration?
**Resolution.** **Comments remain attached to objects**; history **may reference** discussion activity; history **does not become** the discussion and **does not edit** comments (§N).

### Q12 — Empty states?
**Resolution.** Distinguish: no history yet · no history in selected category · no prior versions · no reanalysis history · unavailable (§O).

### Q13 — Failure states?
**Resolution.** Define: timeline unavailable · target unavailable · retained prior context unavailable · superseded target unavailable · project no longer accessible · honest retry/return; no fabrication (§P).

### Q14 — Deferred?
**Resolution.** Compliance-grade audit logs · exportable audit reports · legal retention policies · **restore/rollback** behavior · permanent deletion semantics · detailed event infrastructure · timeline APIs · advanced filtering/search · visual diff tooling (§T).

## F. Surface Architecture

A **project-level secondary history surface** that aggregates retained history and routes to retained context:

```text
Project (entry: Project Overview / Global Nav / Dashboard / in-context object history / Awareness)
   ▼
History & Timeline Surface (secondary, project-context)
  • chronological timeline, grouped by recency / category
  • each item: timestamp · source object · project · surface context · actor/system ·
    change type · short summary · prior/current marker · → route
   ▼ (select item)
   Retained context (artifact version · prior/superseding finding · prior/superseding
                     recommendation · comment thread · collaboration context · updated/prior analysis)
```

- **Secondary, not primary:** reachable within a project; **not** a primary navigation destination/Workspace; hosts **no structured actions** (§D).
- **Aggregates + links** the in-context histories that the Artifact/Finding/Recommendation/Collaboration specs already retain (append-only); it introduces **no new retention mechanism or object**.
- Presents a **chronological timeline**; selecting an item **routes** to its retained context (§I).

## G. History Categories

The ten Release 1 categories (§E Q3) are **presentation over already-retained history**:
- **Artifact-sourced:** saved versions; (per the editing workflow's append-only history).
- **Analysis-sourced:** analysis/reanalysis runs; stale-analysis transitions (per Orientation State Model / editing workflow).
- **Finding-sourced:** lifecycle changes; supersession (per Finding Panel append-only history).
- **Recommendation-sourced:** lifecycle changes; supersession; selected-recommendation history (per Recommendation Panel append-only history).
- **Collaboration-sourced (references only):** comment/discussion references; sharing/collaboration activity references (per Collaboration spec; history references, never hosts).
- **Awareness-sourced (references only):** notification/awareness references (per `NOTIFICATION_AND_AWARENESS_SURFACE_…`; awareness items appear in the retained timeline as references and route to source/retained-prior context — History neither creates nor duplicates them).

## H. History Item Structure

Each item presents exactly: **timestamp/recency · source object · project · surface context · actor / system source (where relevant) · change type · short summary · prior/current marker · navigation target.** The item is a **pointer over retained history**: it summarizes and routes; it is **not** the object/version/comment/finding/recommendation it references, and carries **no** action affordance beyond "open the retained context." No APIs, events, database fields, or implementation are implied.

## I. Timeline Navigation & Context Preservation

- Selecting an item **routes to its retained context** per §E Q5, **preserving context**.
- Routing obeys all surface rules — supersession items open **both** the prior and superseding object; selected-recommendation history routes through the **associated Finding** to the Recommendation Panel (Recommendation only in Finding context); comment history opens the **thread**; artifact versions open the **retained version** context; an **awareness reference** routes to its relevant source context or retained prior context (consistent with the Awareness surface).
- Routing **never fabricates** content and **never changes assessment or current state**; viewing a prior version never alters the current one.
- An unavailable/superseded/inaccessible target triggers the failure states (§P), not invented content.

## J. Append-Only History Presentation

- History is **retained and append-only in presentation**: prior states are **never silently overwritten**; **supersession is additive** (prior retained alongside the superseding state).
- **No deletion/mutation affordances** are exposed in Release 1 (no delete/edit/rollback buttons; restore/rollback deferred, §T).
- History presentation **does not imply governance/audit compliance** — it is traceability for understanding, not a certified log (§ Q9).

## K. Prior / Current / Superseded State Labeling

- Every history item is clearly labeled: **current · prior · superseded · closed · stale · failed · unavailable.**
- **Prior states are never presented as current.** A superseded finding/recommendation links to its superseding state; a stale analysis is shown as previous analysis; a failed reanalysis is shown as failed (last-known-good retained).
- Labels are **presentation** of upstream-owned states (lifecycle / Orientation State Model); History computes or changes none of them.

## L. Relationship to Assessment & Reanalysis

- **Viewing history changes no assessment**; viewing prior context changes no current state; **history triggers no reanalysis**; **only reanalysis changes assessment.**
- Analysis/reanalysis runs and stale transitions are **presented** (owned upstream by the Orientation State Model / editing workflow); History never computes, triggers, or alters them.
- Reanalysis-failed items route to the **last-known-good / retry** context (per the editing workflow); History fabricates no result.

## M. Relationship to Notification & Awareness

- **Awareness points to recent change**; **History preserves the broader retained timeline** (subordinate to `NOTIFICATION_AND_AWARENESS_SURFACE_SPECIFICATION_V1.md`).
- **Notification items may route into History**; **History does not create notifications**; **notifications do not mutate History.** Distinct surfaces: Awareness = recent-change pointer; History = retained timeline.

## N. Relationship to Collaboration

- **Comments remain attached to objects** (Collaboration spec); History **references** discussion activity.
- History **does not become** the discussion and **does not edit** comments — it points to the thread in its object context. Sharing/collaboration activity appears as **references** only.

## O. Empty States

- **No history yet** — a neutral "no history yet" (e.g., a brand-new project).
- **No history in selected category** — neutral per-category empty state, distinct from "no history at all."
- **No prior versions** — for an object with only its current state.
- **No reanalysis history** — analysis has not run / no reanalysis yet.
- **Unavailable** — the surface/data is temporarily unavailable (§P), distinct from "empty."

## P. Failure States

- **Timeline unavailable** — "history unavailable — retry"; the rest of the app remains usable; fabricate no items.
- **Target unavailable** — selecting an item whose target can't load shows "unavailable — retry/return" without fabricating content.
- **Retained prior context unavailable** — if a retained prior state can't load, say so honestly; never reconstruct/fabricate it; never present a different state as the prior.
- **Superseded target unavailable** — route to whichever of prior/superseding is available, clearly labeled; never fabricate the missing one.
- **Project no longer accessible** — if access was removed, say so plainly and return to a safe surface (Workspace Home); no fabricated access. *(Permission enforcement is out of scope; this is honest presentation.)*
- **General principle:** honest, recoverable, non-fabricating; History never invents a prior state, version, or activity.

## Q. Progressive Disclosure

- **Always available (within a project):** the entry point to the project timeline.
- **One interaction away:** the chronological timeline (grouped by recency/category) with per-item summaries and prior/current labels.
- **Through routing:** the **retained context** (version/object/thread) for full detail.
- **In-context:** an object's own history slice from its surface (Artifact/Finding/Recommendation/Collaboration).
- **Intentionally absent:** restore/rollback/delete/edit/approve affordances; audit-certification/compliance framing; assessment-changing or reanalysis-triggering controls; scores/percentages; the referenced content itself hosted in History (it points, never hosts); advanced filtering/search/diff (deferred).

## R. Integrity Rules

- **HT-1.** The surface **computes nothing** (no scoring/CAF/Reliability/Confidence).
- **HT-2.** The surface **generates nothing** (no findings/recommendations/comments/assessment/new history objects); items are **pointers over already-retained history**.
- **HT-3.** The surface **governs nothing, executes nothing, automates nothing** — it is **not** approval, audit certification, a decision record, or compliance evidence; **traceability for understanding only**.
- **HT-4.** History **creates no tasks** and is **not** task/execution history or workflow.
- **HT-5.** **Viewing history changes no assessment or current state**; **triggers no reanalysis**; **only reanalysis changes assessment.**
- **HT-6.** History is **append-only in presentation** — prior states never silently overwritten; **supersession additive**; **no deletion/mutation affordances** in Release 1.
- **HT-7.** **Prior states are never presented as current**; labels (current/prior/superseded/closed/stale/failed/unavailable) are presentation of upstream-owned states.
- **HT-8.** History **references** comments; it **does not become/create/edit** comments (Collaboration governs comments).
- **HT-9.** History **points to** findings/recommendations in proper context (Recommendation via Finding) and to **both** sides of a supersession; it never reframes them or hosts their actions.
- **HT-10.** Routing **preserves context** and **never fabricates** content/version/activity/access.
- **HT-11.** **Awareness ≠ History** — notifications may route into History; History creates no notifications; notifications never mutate History.
- **HT-12.** The surface is a **Companion-Surface-class secondary project-context surface**, **not a primary destination/Workspace/Panel/Chat/audit-log**, and hosts **no structured actions**.
- **HT-13.** **No** APIs, events, implementation, styling, database design, audit/compliance system, or restore/rollback defined here; no existing model redefined; no new retention mechanism introduced.

## S. Conformance Requirements

A conforming History & Timeline Surface MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:

- **HT-C1.** Be a **secondary project-context history surface** (Companion-Surface-class), **not a primary destination**, hosting **no structured actions** (§D, §F; HT-12). **Fail** if it becomes a primary destination or hosts restore/rollback/approve/edit/delete actions.
- **HT-C2.** Present the Release 1 **categories** as presentation over already-retained history, creating **no new object or retention mechanism** (§G; HT-2). **Fail** if History generates an object or a new retention store.
- **HT-C3.** Present each **item** with the §H fields and **route to retained context** preserving context, **never fabricating** content and **never changing assessment/current state** (§H, §I; HT-5/HT-10). **Fail** if content is fabricated or assessment/current state changes.
- **HT-C4.** Be **append-only in presentation** — prior never silently overwritten, supersession additive, **no deletion/mutation affordances** (§J; HT-6). **Fail** if a delete/edit/rollback affordance appears or history is mutated.
- **HT-C5.** **Label** every item (current/prior/superseded/closed/stale/failed/unavailable) and **never present prior as current** (§K; HT-7). **Fail** if a prior state is presented as current.
- **HT-C6.** Ensure History **is not governance/approval/audit/compliance/decision-record** — traceability for understanding only (§J, Q9; HT-3). **Fail if approval/audit-certification/compliance/decision-record framing appears.**
- **HT-C7.** Ensure History **changes no assessment, triggers no reanalysis, creates no tasks** (§L; HT-4/HT-5). **Fail if any history action changes assessment, triggers reanalysis, or creates a task.**
- **HT-C8.** **Reference** comments/findings/recommendations in proper context (Recommendation via Finding; both sides of supersession); never become/create/edit them or host their actions (§N, §I; HT-8/HT-9). **Fail** if History edits a comment or opens a Recommendation outside Finding context.
- **HT-C9.** Keep **Awareness and History distinct** — notifications may route into History; History creates no notifications; notifications never mutate History (§M; HT-11).
- **HT-C10.** Implement empty states (no history / none in category / no prior versions / no reanalysis history / unavailable) and honest failure states (timeline/target/prior-context/superseded/no-access) that fabricate nothing (§O, §P).
- **HT-C11.** Define **no** APIs, events, implementation, styling, database design, audit/compliance system, or restore/rollback (HT-13; §T). **Fail** if any is defined.

**Explicit fail conditions.** Conformance is **all-or-nothing**. The surface **fails** if it: exposes restore/rollback/delete/edit/approve affordances or mutates history; presents a prior state as current; frames itself as audit/compliance/approval/decision-record; changes any assessment or current state, triggers reanalysis, or creates a task; generates an object/new retention mechanism; fabricates content/version/activity/access on routing or failure; becomes/creates/edits a comment or opens a Recommendation outside Finding context; becomes a primary destination or hosts structured actions; creates notifications or lets notifications mutate it; or defines APIs, events, implementation, styling, database design, an audit/compliance system, or restore/rollback.

## T. Deferred Items

Explicitly **deferred / out of scope:** compliance-grade audit logs; exportable audit reports; legal retention policies; **restore/rollback** behavior; permanent deletion semantics; detailed event infrastructure; timeline APIs; advanced filtering/search; visual diff tooling; execution/task history; permission enforcement (presented honestly, not enforced); mobile-specific history behavior; visual/styling realization; implementation; database design; and any numeric/calibration values.

---

*This specification defines the canonical Release 1 History & Timeline Surface — a secondary project-context history surface (Companion-Surface-class: presents + routes, hosts no structured actions, not a primary destination) that answers "Where do users inspect how project understanding, artifacts, findings, recommendations, comments, and reanalysis changed over time?" It aggregates and links the already-retained, append-only in-context histories across eleven Release 1 categories (artifact saved versions, analysis/reanalysis runs, stale-analysis transitions, finding lifecycle/supersession, recommendation lifecycle/supersession, selected-recommendation history, comment/discussion references, sharing/collaboration references, notification/awareness references); each item presents timestamp, source object, project, surface context, actor/system, change type, short summary, prior/current marker, and a navigation target, and routes to retained context — preserving context, fabricating nothing, and changing no assessment or current state. It is append-only in presentation (prior never silently overwritten, supersession additive, no deletion/mutation affordances), labels every item (current/prior/superseded/closed/stale/failed/unavailable) and never presents prior as current, and is traceability for understanding only — not governance, approval, audit certification, compliance evidence, decision record, task, or execution history, and not a mutable log. Awareness points to recent change while History preserves the broader timeline; notifications may route into History but never mutate it; comments stay on their objects (History references, never edits them). It defines no audit/compliance system, APIs, events, implementation, styling, database design, or restore/rollback. Only reanalysis changes assessment.*

## U. Ratified update — History as center pane (DL-088, 2026-07-02)

Ratified by **DL-088** (presentation-only). History is presented as a **center pane** reachable from the left rail (consistent with Overview/Findings), while remaining a **secondary, append-only, read-only** surface — no restore/rollback, no structured actions, no decision-record framing; viewing changes no assessment. Center-pane presentation does not elevate it to a primary understanding surface. Visual reference of record: `product-design/oslo_r1_experience_mockup_v3.html`.

**History & Timeline Surface Specification v1 complete.**
