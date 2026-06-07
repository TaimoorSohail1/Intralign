# Project Dashboard & Project List Experience Specification v1

**Document Type:** Experience Specification (UX / Interaction Model Only)
**Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Consistent with and subordinate to (authoritative — must not redefine):** `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1.md` · `ONBOARDING_AND_PROJECT_CREATION_EXPERIENCE_SPECIFICATION_V1.md` · `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · `MRI_WORKSPACE_SPECIFICATION_V1.md` · `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` · `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md` · `ACCOUNT_AND_WORKSPACE_SETTINGS_EXPERIENCE_SPECIFICATION_V1.md` · Release 1 Tier Definitions · CAF Assessment · Reliability v2 · Confidence v2.

> **Non-negotiable constraints.** This specification defines **Workspace Home, Project Dashboard, Project List, project discovery, organization, visibility, status visibility, search, filtering, sorting, archiving, empty states, failure states, and progressive disclosure** only. It must **NOT** define: governance, execution, automation, agents, permissions architecture, APIs, events, implementation, styling, assessment generation, findings generation, or recommendation generation.
>
> **The experience computes nothing. It generates nothing. It governs nothing. Only reanalysis changes assessment.**
>
> **Preserved invariants.** Artifacts remain the **source of truth**. Findings remain **descriptive**. Recommendations remain **advisory**. MRI remains the **diagnostic discovery** experience. **Outcome Confidence is trust in understanding — not project health, readiness, or outcome probability.** Project understanding remains the **center of gravity**. No governance model. No execution model.

---

## A. Purpose

Define the canonical Release 1 **Workspace Home, Project Dashboard, and Project List** experience — the **project discovery layer** where users land and from which they reach every project. It answers:

> **"How do users discover, organize, and access their projects?"**

This is the authoritative definition of the Workspace Home (the returning-user landing surface from the navigation shell) and the surface through which users browse, search, organize, and open their projects — **presenting** each project's existing state without computing, generating, or governing anything.

## B. Scope

**In scope:** Workspace Home; the Project Dashboard; the Project List; project discovery, organization, and visibility; per-project **status** and **understanding** visibility; search, filtering, sorting; recent/pinned/archived projects; project lifecycle and ownership/sharing visibility; and the empty, failure, and progressive-disclosure behavior of this surface.

**Out of scope (explicitly):** governance; execution; automation; agents; permissions architecture; APIs; events; implementation; styling; and any computation (scoring / CAF / Reliability / Confidence) or generation (Findings / Recommendations / assessment). The experience **lists and presents** projects and their **already-produced** state; it never produces or alters that state.

## C. Workspace Home Philosophy

Workspace Home exists to get users **back to understanding fast** — to find the right project and open it with minimal friction. It is a **calm index**, not a metrics dashboard or a management cockpit: it presents projects and their **existing** understanding state honestly, keeps **understanding the center of gravity**, and never editorializes into "health," "readiness," or "score." It **computes nothing and generates nothing** — every indicator it shows was produced upstream by analysis/reanalysis and is merely **presented** here, reliability-qualified and never bare.

## D. Workspace Home Architecture

Workspace Home is the **Workspace Context** landing surface (per the navigation shell), composed of:

```text
Workspace Home
 ├─ Header / actions       (Create Project · Search · Settings/Account via global nav)
 ├─ Recent Projects        (quick resume — §M)
 ├─ Pinned / Favorite      (user-chosen quick access — §N)
 ├─ Project Dashboard      (the at-a-glance project set — §E)
 └─ Project List           (the full, organizable list — §F)
       └─ Filters · Sort · (Active / Archived views)
```

- **Q1 (resolved): the user's home screen is Workspace Home** — the returning-user landing surface (consistent with the navigation shell and onboarding specs). It presents the project discovery layer (Dashboard + List) with quick-access affordances (Recent, Pinned).
- Each region has **purpose, visible information, allowed actions**, and empty/failure states. All regions **present** existing project state; none compute or generate.

## E. Project Dashboard Experience

- **Purpose:** an **at-a-glance** view of the user's projects — the quickest way to recognize and open the right one.
- **Visible information (per project — Q2):** project **name**; **ownership/sharing** indication (owned vs. shared, §Q); **status** (analysis state — e.g., analyzing / analyzed / stale; §K); a **presented understanding indicator** (the project's existing reliability-qualified understanding summary; §L); **last-updated/activity** recency; and optional descriptive metadata (type/workflow if set). All **presented**, none computed.
- **Allowed actions:** open a project; pin/unpin (§N); reach archive (§O); create a project.
- **Active-project limit (Free tier) — Create Project stays enabled.** A user at the active-project cap may **attempt** to create another; the attempt is **gated by the platform** (server returns the limit state — not computed here) and the surface **presents the upgrade prompt with two resolutions: upgrade, or archive the current project** (archiving is reversible, §O). **Do not disable or hide Create Project at the limit** (that would suppress the attempt). Limit *values* per Tier Definitions; this is **presentation/interaction, not computation or governance.**
- **Constraint:** the dashboard is **recognition and access**, not analytics — it shows no computed scores and no fabricated "health."

## F. Project List Experience

- **Purpose:** the **full, organizable** list of projects for browsing and management of access (not of work).
- **Visible information:** the same per-project information as the dashboard (§E, Q2), in a denser, **sortable/filterable** list, with **Active** and **Archived** views (§O).
- **Allowed actions:** search (§H), filter (§I), sort (§J); open; pin/unpin; archive/unarchive; create.
- **Constraint:** organizing the list **reorders/filters presentation only** — it changes no project, no content, and no assessment.

## G. Project Discovery Experience (Q3)

- **How users discover projects (resolved):** through **recognition and retrieval** — Recent (resume what you were doing), Pinned (your chosen few), the Dashboard (at-a-glance recognition), and the List with **search/filter/sort** for larger sets. Discovery scales from "a handful" (Recent/Dashboard suffices) to "many" (search/filter/sort).
- **Constraint:** discovery **surfaces existing projects**; it never creates, ranks-by-computation, or governs them.

## H. Project Search Experience (Q4)

- **How users search (resolved):** a **text search** over project **name** and lightweight descriptive metadata (e.g., description/type) the user already provided — to locate a known project quickly.
- **Allowed actions:** enter a query; open a result; clear search.
- **Constraint:** search **matches presented metadata**; it performs no semantic analysis of artifact content, no computation, and no generation. *(Exact match behavior is presentation calibration, deferred — §W.)*

## I. Project Filtering Experience (Q5)

- **How users filter (resolved):** by **presented, factual attributes** — **status** (analyzing / analyzed / stale), **ownership/sharing** (owned / shared with me), **lifecycle view** (active / archived), and optional **type/workflow** if set.
- **Allowed actions:** apply/clear filters (combinable).
- **Constraint:** filters **narrow presentation** over existing facts; they introduce no computed dimension (no "health"/score filter) and change nothing.

## J. Project Sorting Experience (Q6)

- **How users sort (resolved):** by **presented, factual attributes** — **recency** (last updated/activity), **name** (alphabetical), and **created date**. Recency is the sensible default for "get back to work."
- **Allowed actions:** choose a sort; reverse order.
- **Constraint:** sorting **reorders presentation** over existing facts; it never sorts by a computed score or fabricated ranking.

## K. Project Status Visibility Experience (Q11)

- **Purpose:** show each project's **analysis status** so users know what state its understanding is in.
- **Status states (presented, per the Orientation State Model / editing workflow):** **analyzing** (analysis/reanalysis in progress), **analyzed** (current understanding available), **stale** (content changed since last analysis — understanding may be out of date), and **awaiting/not-yet-analyzed** (e.g., no artifacts or analysis not started).
- **How stale projects are surfaced (Q11, resolved):** a project whose content changed since its last analysis is **clearly marked stale** in the dashboard/list — communicated honestly (e.g., "analysis out of date") and **never presented as current**, consistent with the editing workflow. The list **does not** trigger reanalysis; it only **surfaces** the stale state.
- **Constraint:** status is **presented**, not computed; the list runs no analysis.

## L. Project Understanding Visibility Experience (Q10)

- **Purpose:** surface each project's **existing understanding state** for recognition — **not** a health/readiness verdict.
- **What is surfaced (resolved):** the project's **already-produced, reliability-qualified understanding summary** (the Outcome Confidence summary as defined upstream — trust in understanding, reliability-qualified, **never bare**), presented as a **recognition indicator**, alongside whether understanding is **current or stale** (§K).
- **Explicit guard (Q10):** OSLO has **no "project health" concept.** This surface must **not** present a "health," "readiness," "on-track," or "outcome-probability" indicator, and must **not** compute or fabricate any score. It **presents** the existing understanding summary only, qualified by reliability, and reflects "where understanding is weak" only insofar as upstream analysis already expressed it — it computes nothing.
- **Constraint:** the understanding indicator is **presented**, reliability-qualified, and **changes only via reanalysis**; the list never recomputes or re-derives it.

## M. Recent Projects Experience (Q7)

- **Should recent projects exist? (resolved): Yes.** A **Recent Projects** region gives one-tap **resume** of recently opened/worked projects — directly serving "get back to understanding fast."
- **Visible information:** recently accessed projects with the same presented per-project info (§E).
- **Constraint:** recency is **presented activity/access order**, not a computed priority.

## N. Pinned / Favorite Projects Experience (Q8)

- **Should pinned projects exist? (resolved): Yes.** Users can **pin/favorite** projects for persistent quick access.
- **Allowed actions:** pin/unpin; open a pinned project.
- **Constraint:** pinning is a **user preference / presentation choice**; it changes no project, content, or assessment, and governs nothing.

## O. Archived Projects Experience (Q9)

- **How archived projects are handled (resolved):** users can **archive** a project to remove it from the active set without deletion; archived projects live in an **Archived view** and can be **unarchived**. Archiving is **reversible** and **non-destructive** — it hides from the active list, never deletes content, findings, recommendations, history, or assessment.
- **Allowed actions:** archive; view archived; unarchive.
- **Constraint:** archiving affects **list membership/visibility** only; it performs no deletion, no computation, and no governance. (Permanent deletion, if any, is out of scope — §W.)

## P. Project Lifecycle Visibility Experience

- **Purpose:** present a project's lifecycle position for recognition: **new/awaiting analysis → analyzed (understanding available) → ongoing (edited/reanalyzed over time) → archived**.
- **What is surfaced:** the project's current lifecycle/status (§K) and active-vs-archived state (§O), as **presented facts**.
- **Constraint:** lifecycle is **descriptive visibility**, not a workflow/pipeline/stage-gate; the list defines **no** lifecycle *workflow*, approval, or governance — it only shows where a project presently is.

## Q. Project Ownership & Sharing Visibility Experience (Q12)

- **How shared projects are surfaced (resolved):** each project indicates **ownership/sharing** — **owned by me** vs. **shared with me** — and is **filterable** by it (§I), consistent with the Collaboration spec's participant types (presentation only).
- **Visible information:** owner indication; that a project is shared and (where presented) with whom, as **presentation only**.
- **Constraint:** ownership/sharing is **presented**; this surface defines **no permissions architecture/enforcement** and performs no sharing actions (those live in the Collaboration spec).

## R. Empty States (Q13)

The experience must **distinguish**:

- **No projects (Q13)** — a first-time/empty workspace with a prominent **"create your first project"** (consistent with onboarding); not an error.
- **No results** — search/filter returns nothing ("no projects match"), distinct from "no projects at all," with a clear way to clear the query/filters.
- **No recent / no pinned** — neutral states for those regions (e.g., "your recent projects will appear here").
- **No archived** — neutral "no archived projects" in the Archived view.
- **Unavailable** — the list/region is temporarily unavailable (§S), distinct from "empty/none."

## S. Failure States (Q14)

Failures are **honest and recoverable**:

- **Project information unavailable (Q14):** when a project's presented info (status/understanding indicator/metadata) can't load, the card/row shows an **"information unavailable — retry"** state rather than blank or **fabricated** data; **no indicator is invented**, and an unavailable understanding indicator is never shown as a real value.
- **List unavailable:** when the list can't load, the surface shows an **"unavailable — retry"** state and keeps the user oriented (global navigation remains).
- **Action failure (pin/archive/search):** reported clearly with the prior state retained; no silent change.
- **General principle:** nothing is fabricated, no project state is silently changed, and a path to retry/return always exists.

## T. Progressive Disclosure

- **Primary:** the project set for recognition and access — Recent/Pinned and the Dashboard, plus **Create Project** and **Search**.
- **Secondary:** the full Project List with filter/sort; status and understanding indicators per project.
- **Tertiary:** Archived view; detailed ownership/sharing indication; optional metadata.
- **Intentionally absent:** computed scores, "health"/"readiness" indicators, or rankings; findings/recommendations/assessment surfaces; governance/approval/execution affordances; automation/agents; any management-cockpit framing that displaces understanding as the center of gravity.

## U. Integrity Rules

- **PL-1.** The experience **computes nothing** (no CAF / Reliability / Confidence / scoring / ranking).
- **PL-2.** The experience **generates nothing** (no findings / recommendations / assessment).
- **PL-3.** The experience **governs nothing** — no governance/approval/decision/lifecycle workflow.
- **PL-4.** The experience introduces **no execution, automation, or agent** behavior.
- **PL-5.** All per-project indicators are **presented** from upstream-produced state; **only reanalysis changes** the understanding/assessment shown.
- **PL-6.** **No "project health"/"readiness"/"outcome-probability" concept** is presented; the only understanding indicator is the **existing, reliability-qualified** understanding summary, **never bare**.
- **PL-7.** **Stale** projects are clearly marked and **never presented as current**; the list triggers no reanalysis.
- **PL-8.** Search / filter / sort operate over **presented factual attributes** only and **reorder/narrow presentation** without changing any project, content, or assessment.
- **PL-9.** **Archiving is reversible and non-destructive** — it changes list membership/visibility only; no deletion of content/findings/recommendations/history/assessment.
- **PL-10.** Pinning/favoriting and recency are **presentation/preference** only; they govern nothing.
- **PL-11.** Ownership/sharing is **presentation only**; **no permissions architecture** is defined here.
- **PL-12.** Failures are **honest and recoverable** — no fabricated indicators, no silent state changes, always a retry/return path.
- **PL-13.** **Project understanding remains the center of gravity**; the surface never becomes a metrics cockpit or work-management board.
- **PL-14.** **No APIs, events, implementation, or styling** is defined here; no existing model is redefined.

## V. Conformance Requirements

A conforming Project Dashboard & Project List experience MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:

- **PL-C1.** Make **Workspace Home** the landing surface presenting the discovery layer (Recent, Pinned, Dashboard, List) with Create Project and Search (§D; Q1).
- **PL-C2.** Present **per-project info** (name, ownership/sharing, status, reliability-qualified understanding indicator, recency, optional metadata) as **presented** state, **computing nothing** (§E; PL-1/PL-5). **Fail** if any value is computed or any score is displayed.
- **PL-C3.** Surface understanding **without** a "health/readiness/outcome-probability" indicator; present only the existing reliability-qualified understanding summary, never bare (§L; PL-6). **Fail** if a project-health/score/readiness indicator appears.
- **PL-C4.** Mark **stale** projects clearly and never present stale as current; trigger **no reanalysis** from the list (§K; PL-7). **Fail** if stale is shown as current or the list runs analysis.
- **PL-C5.** Provide **search/filter/sort** over **factual presented attributes** that reorder/narrow presentation only, changing no project/content/assessment (§H–§J; PL-8). **Fail** if filtering/sorting by a computed score is introduced or if organizing changes any project.
- **PL-C6.** Provide **Recent** and **Pinned** as presentation/preference quick-access, governing nothing (§M, §N; PL-10).
- **PL-C7.** Provide **reversible, non-destructive archiving** with an Archived view and unarchive; no deletion of content/history/assessment (§O; PL-9). **Fail** if archiving deletes project data.
- **PL-C8.** Present **lifecycle/status and ownership/sharing as descriptive visibility** only — no lifecycle workflow, no permissions architecture (§P, §Q; PL-3/PL-11). **Fail** if a lifecycle workflow or permission enforcement is defined.
- **PL-C9.** Implement **empty states** (no projects / no results / no recent / no pinned / no archived / unavailable) and **failure states** that fabricate no data, change nothing silently, and offer retry/return (§R, §S; PL-12). **Fail** if an unavailable indicator is shown as a real value.
- **PL-C10.** Expose **no** governance, execution, automation, agent, API, event, permissions-architecture, implementation, or styling definition (PL-3/PL-4/PL-14). **Fail if governance appears. Fail if execution/work-management appears.**

**Explicit fail conditions.** Conformance is **all-or-nothing**. The experience **fails** if it: computes any value, score, ranking, or "project health/readiness"; generates any finding/recommendation/assessment; presents stale understanding as current or triggers reanalysis from the list; filters/sorts by a computed dimension or changes any project/content/assessment while organizing; deletes project data on archive; defines a lifecycle/approval/governance workflow or permissions architecture; fabricates indicators or silently changes state on failure; displaces understanding as the center of gravity with a metrics/management cockpit; or defines APIs, events, implementation, or styling.

## W. Deferred Items

Explicitly **deferred / out of scope:** governance; execution; automation; agents; permissions architecture; APIs; events; implementation; styling; assessment/findings/recommendation generation; permanent project **deletion** semantics; advanced/grouping/folder organization; bulk operations; cross-workspace project views; advanced personalization of the dashboard; exact search-match and sort/tie-break calibration (presentation calibration); and any numeric tier/limit values beyond what Release 1 Tier Definitions specify (presented, not computed).

---

*This specification defines the canonical Release 1 Workspace Home, Project Dashboard, and Project List — OSLO's project discovery layer, answering "How do users discover, organize, and access their projects?" Workspace Home is the landing surface presenting Recent, Pinned, a recognition-oriented Dashboard, and a searchable/filterable/sortable List with Active and Archived views. Each project presents name, ownership/sharing, analysis status (including a clearly-marked stale state), and an existing reliability-qualified understanding indicator — explicitly NOT a "project health/readiness/outcome-probability" score, and computed by nothing here. Search, filter, and sort operate over factual presented attributes and only reorder/narrow presentation; archiving is reversible and non-destructive; pinning and recency are presentation/preference; ownership/sharing is presentation only. It is UX/interaction only — it presents projects and their already-produced state, computes nothing, generates nothing, governs nothing, keeps understanding the center of gravity, and introduces no governance, execution, automation, agents, permissions architecture, APIs, events, implementation, or styling; only reanalysis changes assessment.*

**Project Dashboard & Project List Experience Specification v1 complete.**
