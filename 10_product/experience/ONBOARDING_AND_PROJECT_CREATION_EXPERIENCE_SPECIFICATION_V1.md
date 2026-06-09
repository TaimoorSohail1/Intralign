# Onboarding & Project Creation Experience Specification v1

**Document Type:** Experience Specification (UX / Interaction Model Only)
**Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Consistent with and subordinate to (authoritative — must not redefine):** `SIXTY_SECOND_ORIENTATION_WORKFLOW_SPECIFICATION_V1.md` · `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · `MRI_WORKSPACE_SPECIFICATION_V1.md` · `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` · `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW_SPECIFICATION_V1.md` · `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md` · `ORIENTATION_STATE_MODEL_V1.md` · CAF Assessment · Reliability v2 · Confidence v2 · Release 1 Tier Definitions.

> **Non-negotiable constraints.** This specification defines **UX architecture, onboarding flow, project creation flow, ingestion flow, and user interaction behavior only**. It must **NOT** define: CAF computation, Reliability computation, Confidence computation, Finding generation, Recommendation generation, governance workflows, execution workflows, agent workflows, automation, APIs, events, database design, implementation details, or styling.
>
> **The experience presents onboarding and project initialization. It computes nothing. It generates nothing. It governs nothing. Only reanalysis changes assessment.**
>
> **Preserved invariants.** Artifacts remain the **source of truth**. Findings remain **descriptive**. Recommendations remain **advisory**. MRI remains the **diagnostic discovery** experience. **Only reanalysis changes assessment.** Project understanding remains the **center of gravity**. No governance model. No execution model.

> ✅ **Release 1 defaults — owner-approved (2026-05-31).** The Release 1 resolutions in this spec are **owner-ratified**: **project name required**; **project type and workflow type optional** (non-gating); **empty project creation allowed**; **artifacts optional to create but required for value**; **minimum-to-value = project name + one artifact**; ingestion via **upload / paste / combined sources**; **templates and AI-generated starting content deferred** (out of Release 1). These were previously spec-defaults; they are now owner-approved (closes audit item UX-O3). Project-type / workflow-type taxonomies and whether they ever gate behavior remain deferred (§V).

---

## A. Purpose

Define the canonical Release 1 **Onboarding & Project Creation Experience** — how a user moves from arrival to their first project-understanding experience:

```text
New User → Account Creation → Workspace Initialization → Project Creation
→ Project Ingestion → Project Initialization → 60-Second Orientation → Project Overview
```

It answers:

> **"How does a user begin using OSLO and reach their first project understanding experience?"**

The purpose is to get a user to **first understanding** as directly as possible — to the 60-Second Orientation and Project Overview — without introducing any computation, generation, governance, or execution along the way.

## B. Scope

**In scope:** account creation; authentication entry; first-time user experience; returning-user experience; workspace initialization; project creation; project metadata collection; project setup; ingestion; project initialization; analysis initiation; the transition into the 60-Second Orientation; and the empty, progress, and failure states across this journey.

**Out of scope (explicitly):** permissions architecture; governance; execution; agents; automation; APIs; events; implementation; styling; database design; and any assessment generation/computation logic (CAF / Reliability / Confidence / Findings / Recommendations). The experience **initiates** analysis; it never performs or defines it.

## C. Onboarding Philosophy

Onboarding exists to **remove everything between a user and their first understanding** — not to train, gate, or govern. It is **understanding-first**: the fastest path from "new user" to "I can see what OSLO understands about my project, where it's weak, and how trustworthy that is." Onboarding collects the **minimum** needed to show value and defers everything else. It coordinates **no work**, makes **no decisions**, and computes/generates **nothing** — it simply gets the user to the orientation experience. **Project understanding remains the center of gravity** from the very first screen.

## D. Experience Architecture

The canonical Release 1 journey, as a linear flow with explicit states:

```text
New User
   ↓
Account Creation        ← establish identity
   ↓
Authentication          ← sign in / resume
   ↓
Workspace Initialization← the user's home for projects
   ↓
Project Creation        ← name + (optional) metadata
   ↓
Project Ingestion       ← add artifacts (upload / paste / combine)
   ↓
Project Initialization  ← prepare the project for analysis
   ↓
Analysis Initiation     ← user (or auto-on-ready) starts analysis  [initiates only]
   ↓
60-Second Orientation   ← first understanding (per Orientation State Model)
   ↓
Project Overview        ← the ongoing understanding home
```

Each step has **purpose, visible information, allowed actions, transition conditions**, and (where relevant) **failure/empty states**. The flow is **resumable** at each step (a user can leave and return to where they were) and **non-destructive** (nothing computed/generated; nothing governs).

## E. Account Creation Experience (Q1)

- **Purpose:** establish the user's identity so projects/workspaces persist.
- **Visible information:** the minimal fields to create an account (per the product's account mechanism); a clear path to **sign in** instead if returning.
- **Allowed actions:** create an account; switch to sign-in.
- **Transition conditions:** **→ Workspace Initialization** on success.
- **Out of scope:** authentication implementation, identity/permissions architecture (§V).

## F. Authentication Experience (Q2)

- **Purpose:** let a returning user **sign in** and resume.
- **Visible information:** sign-in entry; recovery path; switch-to-create-account.
- **Allowed actions:** sign in; recover access; create account.
- **Transition conditions:** **→ Workspace Initialization** (returning users land here, §P) on success.
- **Out of scope:** auth protocols, tokens, permissions (§V).

## G. First-Time User Experience (Q3)

- **Purpose:** orient a brand-new user just enough to create their first project and reach value.
- **What is shown:** a brief, **skippable** welcome that points directly at **"create your first project,"** plus the empty workspace (§R). It explains, minimally, that OSLO shows **what it understands about a project and where understanding is weak**, and that the fastest path to value is to add a project with at least one artifact.
- **Onboarding placement & skippability:** onboarding is **lightweight and interleaved with project creation**, not a long pre-gate. **It is skippable.** A first-time user can go straight to project creation.
- **Minimum information before value can be shown:** a **project name** and **at least one artifact** (§K). With those, OSLO can analyze and present the 60-Second Orientation. Nothing else is required to reach first value.

## H. Workspace Initialization Experience (Q4)

- **Purpose:** establish the user's **workspace** — the home that holds their projects.
- **How initialized:** on first sign-in, the workspace is presented in an **empty state** (§R) inviting the first project; on subsequent sign-ins it shows existing projects (§P).
- **Visible information:** the project list (empty for first-time users) and a primary **"Create project"** affordance.
- **Allowed actions:** create a project; open an existing project (returning users).
- **Transition conditions:** **→ Project Creation** on create.

## I. Project Creation Experience (Q5)

- **Purpose:** create a new project as the container for artifacts and understanding.
- **Visible information:** the minimal creation surface — **project name** (required) and optional metadata (§J).
- **Allowed actions:** name the project; optionally add metadata; proceed to ingestion.
- **Active-project limit (Free tier):** the **Create Project** entry remains available at the cap; a Free user may **attempt** creation and is **gated** with the **upgrade-or-archive prompt (UP-3)** — never a hidden or disabled control. The gate is **server-enforced** (API `422`); limit values per Tier Definitions (presented, not computed).
- **Release 1 resolutions:**
  - **Can a user create an empty project?** **Yes** — a project can be created without artifacts; artifacts are **optional to create the project** but **required to reach understanding/value** (the empty project simply waits in an "add artifacts" empty state, §R).
  - **Is a project name required?** **Yes** — a name is the minimal identity for a project.
  - **Is project type required?** **No** (optional in Release 1).
  - **Is workflow type required?** **No** (optional in Release 1).
  - **Are artifacts optional or required?** **Optional to create; required for value** (see above).
- **Transition conditions:** **→ Project Ingestion** (or directly to an empty project that prompts ingestion).

## J. Project Metadata Collection Experience (Q6)

- **Purpose:** collect **lightweight, optional** descriptive metadata that helps the user organize/understand the project — **never** a gate to value.
- **What information is collected:** **project name (required)**; optionally a short description, **project type**, and **workflow type** — all **optional** in Release 1. Metadata is **descriptive context only**; it drives no computation, no generation, and no governance.
- **Allowed actions:** add/skip metadata; edit later.
- **Principle:** the experience must not block reaching value on optional metadata; **when project information is incomplete, the user can still proceed** to ingestion and analysis (§G minimum: name + one artifact).

## K. Project Ingestion Experience (Q7)

- **Purpose:** bring **artifacts** into the project — the source of truth OSLO will analyze.
- **How ingestion works:** the user **adds artifacts** to the project via supported methods (§L), optionally **combining multiple sources** into one project. Added artifacts become the project's content; ingestion **presents and stores** them — it **computes/generates nothing** and triggers no assessment by itself (analysis is initiated separately, §N).
- **Visible information:** the artifacts added so far; an "add more" affordance; an indication that analysis can begin once at least one artifact exists.
- **Allowed actions:** add artifact(s); remove an added artifact before analysis; proceed to initialization/analysis.
- **Edge cases:**
  - **If no artifacts exist (Q9):** the project shows an **"add artifacts to begin"** empty state (§R); no analysis runs; value is not yet available — this is presented neutrally, not as failure.
  - **If artifacts already exist (Q10):** the user can proceed to **initialize/analyze**, or add more artifacts first; existing artifacts are listed and ready.

## L. Supported Ingestion Methods (Q8)

Release 1 ingestion methods (resolved):

- **Upload files — Yes.** Users can upload artifact files.
- **Paste content — Yes.** Users can paste content as an artifact.
- **Combine multiple sources — Yes.** Users can add several artifacts (uploads and/or pasted) to one project.
- **Start from templates — Deferred (optional, not Release 1 core).** If offered later, a template is **pre-provided content the user adopts and edits**, not generated content; deferred to keep Release 1 minimal (§V).
- **Start from AI-generated content — Deferred / out of scope for Release 1.** Generating starting content would be **generation**, which this experience must not introduce ("it generates nothing"); deferred to an owner decision (§V).

Ingestion methods **add content only**; none compute or generate assessment.

## M. Initial Project Generation Experience (Q — project initialization)

*("Generation" here means preparing the project, not generating content or assessment.)*

- **Purpose:** **initialize** the project so it is ready for analysis — assemble the added artifacts into the project context.
- **Visible information:** an initialization/progress state (§O); the artifacts being prepared; a clear path to **start analysis** when ready.
- **Allowed actions:** wait for initialization; start analysis (§N); add more artifacts.
- **Transition conditions:** **→ Analysis Initiation** when the project is ready (at least one artifact present).
- **Constraint:** initialization **prepares**; it performs **no** CAF/Reliability/Confidence computation and generates **no** findings/recommendations.

## N. 60-Second Analysis Initiation Experience (Q11, Q13)

- **Purpose:** **initiate** analysis and hand off to the **60-Second Orientation** — the first-understanding experience.
- **How a user initiates analysis (Q11):** from a ready project (≥1 artifact), the user starts analysis (or, where the project is ready on creation, analysis may begin automatically) — the experience **initiates only**; the analysis itself is owned by the analysis engine and is out of scope here.
- **Transition into 60-Second Orientation (Q13):** on initiation, the experience transitions to the **60-Second Orientation** per `SIXTY_SECOND_ORIENTATION_WORKFLOW_SPECIFICATION_V1.md` and `ORIENTATION_STATE_MODEL_V1.md` (Analyzing → Fast Pass Complete), presenting the provisional first understanding, then on to **Project Overview**.
- **Fastest path to first value:** **create project → add one artifact → start analysis → 60-Second Orientation.** Within the first 60 seconds, the user should experience their **first orientation to project understanding** (the owner-approved Time-to-First-MRI target); no other numeric target is fixed here.
- **Constraint:** this step **starts** analysis; it never computes or generates assessment.

## O. Progress & Status Experience (Q12)

- **Purpose:** communicate progress through ingestion, initialization, and analysis honestly.
- **How progress is communicated:** clear **progress/status states** for ingestion (adding/preparing artifacts), initialization (preparing the project), and analysis (Analyzing, per the Orientation State Model) — the user always knows what stage they're in and that understanding is on its way.
- **Principle:** progress is **presentation only** — no numeric scores, no fabricated completion percentages tied to assessment; status reflects the real stage. The artifact/project remains visible where applicable.

## P. Returning User Experience (Q17)

- **What screen users land on (Q17a):** a returning user lands on their **Workspace / projects home** (§H) — the list of their existing projects — not back at onboarding.
- **How they create additional projects (Q17b):** via the primary **"Create project"** affordance from the workspace (re-entering the §I flow); onboarding is not repeated.
- **How they resume existing projects (Q17c):** by opening a project from the list, landing on its **Project Overview** (or the orientation state it was in), resuming exactly where understanding stands. If a project's analysis is stale (content changed since last analysis), the stale state is communicated per the editing workflow (§Q, and `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW_SPECIFICATION_V1.md`).
- **Difference from first-time:** no welcome gate, no empty workspace — straight to projects and understanding.

## Q. Failure States (Q14, Q15, Q16)

Failures are **honest and recoverable**; nothing is fabricated and no partial assessment is presented as complete:

- **Ingestion fails (Q14) / uploaded files cannot be processed:** the experience **clearly reports** which artifact(s) could not be ingested, keeps successfully added artifacts, and offers **retry / remove / add a different source**. It does **not** silently drop content or proceed as if the artifact were present.
- **Project initialization fails (Q15) / partially succeeds:** the experience reports the failure, **retains what succeeded** (added artifacts, project metadata), and offers **retry**; a **partial success** is presented as partial — the user is told what is and isn't ready, and is never shown a fabricated "ready" or fabricated assessment.
- **Analysis fails (Q16) / cannot be completed:** the experience reports that analysis could not complete, **retains the project and artifacts**, and offers **retry**; it presents **no** assessment in the absence of a real one (no fabricated CAF/Reliability/Confidence/findings). Consistent with the orientation/editing specs, a prior valid analysis (if any) remains the last-known state.
- **General principle:** content is never lost, assessment is never invented, and the user always knows whether the project is ready, partial, or failed.

## R. Empty States

The experience must **distinguish**:

- **Empty workspace** — a first-time/returning user with **no projects** ("create your first project").
- **Empty project (no artifacts)** — a created project with **no artifacts yet** ("add artifacts to begin"); analysis cannot run; presented neutrally, not as failure.
- **No analysis yet** — artifacts present but **analysis not yet initiated/completed** (Analyzing/awaiting), distinct from "no artifacts."
- **Unavailable** — workspace/project temporarily **unavailable**, distinct from "empty."

## S. Progressive Disclosure

- **Immediately visible:** the single primary next step at each stage (create account → create project → add an artifact → start analysis) — the path to value is always the most prominent action.
- **In context:** optional metadata, additional ingestion methods, and "add more artifacts" — available but never blocking.
- **Through expansion:** project details and advanced options.
- **Through progress/history:** initialization/analysis status and, once analyzed, the orientation and overview.
- **Intentionally absent:** scores/percentages tied to assessment; finding/recommendation generation; governance/approval/execution affordances; automation/agents; any computation surface; mandatory long-form setup before value.

## T. Integrity Rules

- **OB-1.** The experience **computes nothing** (no CAF / Reliability / Confidence computation).
- **OB-2.** The experience **generates nothing** (no Findings / Recommendations; no AI-generated starting content in Release 1).
- **OB-3.** The experience **governs nothing** — no governance/approval/decision workflow.
- **OB-4.** The experience introduces **no execution, automation, or agent** workflow.
- **OB-5.** **Only reanalysis changes assessment** — onboarding/creation/ingestion/initialization **initiate** analysis but never produce or alter assessment.
- **OB-6.** **Artifacts remain the source of truth**; ingestion adds content, never assessment.
- **OB-7.** Findings remain **descriptive**; Recommendations remain **advisory** — neither is created here.
- **OB-8.** **MRI remains the diagnostic discovery experience**; onboarding routes toward it via the 60-Second Orientation, never redefining it.
- **OB-9.** **Project understanding is the center of gravity** — the fastest path to first understanding is always primary.
- **OB-10.** Minimum to first value is **project name + one artifact**; optional metadata/type/workflow never gate value.
- **OB-11.** Failures are **honest and recoverable** — content is never lost, partial states are shown as partial, and **no assessment is fabricated**.
- **OB-12.** Onboarding is **skippable** and lightweight; it never blocks a user from creating a project.
- **OB-13.** **No permissions architecture, APIs, events, database design, implementation, or styling** is defined here.
- **OB-14.** Progress/status is **presentation only** — honest stage reporting, no fabricated assessment-linked metrics.

## U. Conformance Requirements

A conforming Onboarding & Project Creation experience MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:

- **OB-C1.** Provide the complete journey **New User → Account Creation → Workspace Initialization → Project Creation → Project Ingestion → Project Initialization → 60-Second Orientation → Project Overview**, resumable at each step (§D).
- **OB-C2.** Require **only** a **project name + at least one artifact** to reach first value; keep **project type / workflow type / metadata optional**; allow **empty project creation** (§I, §J; OB-10). **Fail** if optional metadata gates value.
- **OB-C3.** Support ingestion via **file upload, paste, and combining multiple sources**; treat **templates and AI-generated content as deferred/out-of-scope** for Release 1 (§L; OB-2). **Fail** if starting content is generated by the system in Release 1.
- **OB-C4.** **Initiate** analysis and hand off to the **60-Second Orientation** per the orientation specs, without performing or defining analysis (§N; OB-1/OB-5). **Fail** if the experience computes or generates assessment.
- **OB-C5.** Communicate **progress/status honestly** with no fabricated assessment-linked metrics (§O; OB-14).
- **OB-C6.** Land returning users on their **workspace/projects home**, enabling create-additional and resume-existing without repeating onboarding (§P).
- **OB-C7.** Handle **ingestion / initialization / analysis failures** by retaining content, showing partial as partial, offering retry, and **fabricating no assessment** (§Q; OB-11). **Fail** if content is lost or an assessment is fabricated on failure.
- **OB-C8.** Implement empty states distinguishing **empty workspace / empty project / no analysis yet / unavailable** (§R).
- **OB-C9.** Keep **artifacts the source of truth**, **findings descriptive**, **recommendations advisory**, and **MRI** the diagnostic discovery experience — none created/redefined here (OB-6/OB-7/OB-8).
- **OB-C10.** Expose **no** governance, approval, decision, execution, automation, agent, API, event, permissions-architecture, database, implementation, or styling definition (OB-3/OB-4/OB-13). **Fail if governance workflows appear. Fail if execution workflows appear.**

**Explicit fail conditions.** Conformance is **all-or-nothing**. The experience **fails** if it: computes any CAF/Reliability/Confidence value; generates any finding, recommendation, or starting content; presents a fabricated or partial assessment as complete; loses content on failure; gates first value behind optional metadata/type/workflow; introduces governance/approval/decision workflows; introduces execution/automation/agent workflows; or defines permissions architecture, APIs, events, database design, implementation, or styling.

## V. Deferred Items

Explicitly **deferred / out of scope:** permissions architecture; governance; approvals; decision/execution workflows; automation; agents; APIs; events; database design; implementation; styling; assessment generation/computation logic; **template-based starts** and **AI-generated starting content** (owner decision); exact onboarding copy/visual form; project-type and workflow-type taxonomies and whether they ever gate behavior (owner decision); and any numeric targets beyond the owner-approved 60-second Time-to-First-orientation.

---

*This specification defines the canonical Release 1 Onboarding & Project Creation Experience — the complete journey New User → Account Creation → Workspace Initialization → Project Creation → Project Ingestion → Project Initialization → 60-Second Orientation → Project Overview. It resolves Release 1 questions: project name required; project type and workflow type optional; empty projects allowed; artifacts optional to create but required for value; ingestion via upload, paste, and combined sources (templates and AI-generated starts deferred); minimum-to-value is name + one artifact; onboarding lightweight and skippable; returning users land on their workspace; and failures are honest and recoverable with no fabricated assessment. It is UX/interaction only — it initiates analysis but computes nothing, generates nothing, and governs nothing; artifacts remain the source of truth, findings descriptive, recommendations advisory, MRI the diagnostic discovery experience, and only reanalysis changes assessment — introducing no governance, execution, agents, automation, APIs, events, database design, implementation, calculations, scoring, or assessment generation logic.*

**Onboarding & Project Creation Experience Specification v1 complete.**
