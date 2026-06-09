# Artifact Workspace Specification v1

**Document Type:** Workspace Specification (UX / Interaction Model Only)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Consistent with and subordinate to (authoritative — presents, must not modify):** `MRI_WORKSPACE_SPECIFICATION_V1.md` · `MRI_EXPERIENCE_SPECIFICATION_V1.md` · `MRI_MODEL_V1.md` (MRI Visualization Model) · `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · `FINDING_SYSTEM_SPECIFICATION_V1.md` · `FINDING_PRESENTATION_SPECIFICATION_V1.md` · `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` · CAF Assessment · Reliability v2 · Confidence v2 · Release 1 Tier Definitions.

> **Non-negotiable constraints.** This specification defines **UX architecture, interaction model, navigation model, and workspace behavior** only. It must **NOT** define: scoring, CAF computation, Confidence computation, Reliability computation, Finding generation, Recommendation generation, governance, execution, agents, automation, APIs, events, implementation details, or styling.
>
> **Only reanalysis changes assessment.** Artifacts remain the canonical **planning context**. Findings remain the canonical **descriptive** object. Recommendations remain the canonical **advisory** object. MRI remains the canonical **diagnostic discovery** experience. The Artifact Workspace answers: **"What does the content actually say?"**

---

## Core Principle

```text
MRI Workspace          → "Where should I look?"            (diagnostic discovery)
Artifact Workspace     → "What does the content say?"      (content context)  ← THIS DOCUMENT
Finding Panel          → "Why does this weakness exist?"   (explanation)
Recommendation Panel   → "What could I consider doing?"    (evaluation)
```

The Artifact Workspace is the **bridge between diagnostic discovery and actual project content** — the primary working surface where weakness, discovered in MRI, is **contextualized in the artifact itself**. Throughout the experience, **the artifact remains the center of gravity**.

---

## A. Purpose

Define the canonical Release 1 **Artifact Workspace** — the primary **content-centered operating surface** where users:

- **review project artifacts** as the source of truth;
- experience **CAF-enabled overlays** embedded in artifact content;
- **discover findings** embedded *within* artifact content (not as a separate list);
- open **Finding Panels** and **Recommendation Panels** in context;
- **update artifact content**; and
- **trigger reanalysis** (the only thing that changes assessment).

It is where the project's content lives and where the user does the actual work of reading, understanding, and improving artifacts — answering **"What does the content actually say?"**

## B. Scope

**In scope:** the Artifact Workspace UX/interaction model — artifact header, navigation, content area, the **CAF overlay layer**, artifact context area, Finding/Recommendation **Panel** integration, the **editing** experience, the **reanalysis** experience, **append-only history**, empty states, progressive disclosure, and the rules/conformance that bound them.

**Out of scope (explicitly):** scoring; CAF/Reliability/Confidence computation; Finding/Recommendation generation; governance; execution; agents; automation; APIs; events; implementation; styling; and any redefinition of Artifacts, Findings, Recommendations, the MRI Visualization Model, or the CAF/Reliability/Confidence models. The Workspace **presents, navigates, edits content, and triggers reanalysis**; it **computes and generates nothing**.

## C. User Goals (questions answered)

- **"What does this artifact say?"** → the artifact content area (§F).
- **"Where are the weaknesses in this artifact?"** → CAF overlays embedded in content (§G, §H).
- **"Which CAF dimensions are affected?"** → overlays presented by CAF dimension (Clarity / Alignment / Feasibility) (§G).
- **"Which sections contain weaknesses?"** → overlay/navigation by location in the artifact (§E, §G).
- **"Why does this weakness exist?"** → the Finding Panel (§I).
- **"What recommendations are available?"** → the Recommendation Panel (§J).
- **"What changed recently?"** → reanalysis status + append-only history (§L, §M).

## D. Workspace Architecture

**Recommended canonical architecture: a single content-primary workspace** — one surface with the **artifact content at the center**, a CAF **overlay layer** rendered *within* that content, and **contextual panels** that open *beside/over* the content without navigating away. This is recommended over a multi-screen or list-first layout because the artifact must remain the **source of truth and center of gravity**: discovery, explanation, and evaluation all happen **in the context of the content the user is reading**, not on separate screens that pull the user out of the artifact.

The canonical architecture comprises eight regions:

1. **Artifact Header** — identifies the current artifact and presents its observable, **reliability-qualified** understanding signals (CAF / Reliability / Outcome Confidence per the MRI Visualization Model) and reanalysis status. **Presented, not computed.**
2. **Artifact Navigation** — switch artifacts, previous/next, artifact list, and hierarchy (§E).
3. **Artifact Content Area** — the canonical reading experience; the artifact as source of truth (§F).
4. **CAF Overlay Layer** — embedded visual indicators within the content marking where weakness sits (§G). The most important region.
5. **Artifact Context Area** — supporting context for the current artifact/selection (e.g., recent changes, the active overlay's summary), without replacing content.
6. **Finding Panel Integration** — contextual panel explaining a selected weakness (§I).
7. **Recommendation Panel Integration** — contextual panel presenting advisory options (§J).
8. **Reanalysis Status** — visible state of analysis/reanalysis (§L), with the artifact remaining visible throughout.

**Rationale.** A single content-primary surface keeps the artifact central while layering diagnosis (overlays), explanation (Finding Panel), and evaluation (Recommendation Panel) onto it contextually. It complements — does not duplicate — the **MRI Workspace**: MRI organizes weakness across the *whole project* ("where to look"); the Artifact Workspace shows weakness *inside one artifact's content* ("what it says"). The chain is preserved: **Weakness Discovery (MRI) → Artifact Context (here) → Finding Explanation (Panel) → Recommendation Evaluation (Panel)**.

## E. Artifact Navigation Model

The Workspace supports:

- **Switching artifacts** — move directly to any artifact in the project.
- **Previous / Next artifact** — sequential traversal.
- **Artifact list** — browse/select from the set of project artifacts.
- **Artifact hierarchy** — navigate structural relationships among artifacts (parent/child / grouping) where they exist.

Navigation **selects what to view**; it generates no findings/recommendations, edits no content by itself, and changes no assessment. *(No implementation details, routing, or styling are specified here.)*

## F. Artifact Content Area

- Defines the **canonical artifact reading experience** — the artifact's content presented faithfully for review.
- **The artifact remains the source of truth.** The content area is the primary region; everything else (overlays, panels, context) is layered *onto* or *beside* it.
- **Findings never replace content.** Findings are surfaced *within* the content via overlays (§G/§H); the content is never swapped for a findings list.
- **Recommendations never replace content.** Recommendations appear only in the contextual Recommendation Panel (§J); they never overwrite or stand in for artifact content.

## G. CAF Overlay Model

*The most important section.*

**Definition.** CAF overlays are **embedded visual indicators within artifact content** that mark *where* weakness in understanding sits, organized by **CAF dimension** (Clarity / Alignment / Feasibility). They make weakness **visible in situ** — the user sees, inside the content itself, which passages/sections carry weak understanding and along which dimension — without leaving the artifact. Overlays **present** existing CAF assessment and existing findings; they **compute nothing** and **create nothing**.

**User interactions.**

- **Hover overlay** — reveal a lightweight summary of the weakness at that location (which dimension, brief descriptor) without committing to a panel.
- **Click overlay** — open the associated weakness in context (surfacing the Finding Panel, §I).
- **Select overlay** — keep an overlay active/focused as the current investigation target (driving the context area and panels).
- **Navigate between overlays** — move from one overlay to the next/previous within the artifact (e.g., "next weakness"), enabling overlay-to-overlay traversal of the artifact's weaknesses.

**Overlay → Finding relationship.** An overlay is a **presentation marker over existing findings at a location**. **One overlay may surface one finding or multiple findings.** When multiple findings share a location, the overlay surfaces them together (routing to the Finding Panel, which presents them per the Finding Presentation spec). An overlay is **not** a finding, not a copy of a finding, and not a new object — it is a **view** onto findings already in the model.

**Constraints.** Overlays **must not create any new objects** (no overlay object, no resolution/clarification object, no finding/recommendation). Overlays **never replace content** (§F), display **no scores/percentages/ranks** (qualitative dimensional indication only), and change **no** assessment — interacting with an overlay alters no CAF/Reliability/Confidence signal and resolves no finding. Overlay strength/emphasis remains **reliability-qualified** and never presents understanding as fully supported when Reliability says otherwise.

## H. Finding Discovery Experience

- The user **discovers findings through the artifact content itself** — by reading the content and encountering CAF overlays embedded at the relevant locations.
- **The artifact is not replaced by a finding list.** There is no list-first mode that supplants the content; discovery is **in context**.
- **Findings are embedded in context** via overlays (§G); selecting one opens its explanation in a contextual panel (§I).
- Discovery **reveals existing findings**; the Workspace **generates none** and changes no assessment.

## I. Finding Panel Integration

- **Opening behavior:** the Finding Panel opens **in context** (beside/over the content) when the user clicks/selects an overlay or a finding — the user stays in the artifact; **no standalone navigation is required**.
- **Required information** (presented per `FINDING_PRESENTATION_SPECIFICATION_V1.md`): the **finding explanation** (why this weakness exists), its **evidence**, its **CAF impact** (which dimension(s) it bears on — presented, not computed), **supporting context**, and **access to recommendations** (a route into the Recommendation Panel, §J).
- **Contextual:** the panel presents the canonical finding — **descriptive**, explainable, append-only; it **never** duplicates, creates, edits, or resolves a finding, and never frames a finding as an action/command.

## J. Recommendation Panel Integration

- The Recommendation Panel presents the selected finding's Recommendations per `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md`, maintaining the presentation constructs:
  - **OSLO Recommended** — the recommendation OSLO surfaces foremost.
  - **Possible Resolution Paths** — the multiple Recommendations displayed together as alternative ways to resolve the finding.
  - **Selected Path** — the path the user is focusing on.
- **All three remain presentation-only constructs.** There is **no Resolution Path object, no Clarification Candidate, no Resolution Candidate** — only multiple **Recommendations** (each advisory, each with a single `finding_id`) displayed together.
- The panel **generates no recommendations**, applies nothing, executes nothing; **only the user acts**, and **only reanalysis changes assessment**.

## K. Editing Experience

- **The user may update artifact content.** Artifact **editing is permitted** in the Workspace — the artifact is a living planning context the user improves.
- **Editing itself changes no assessment.** Editing content does **not** modify CAF, Reliability, Confidence, or any finding's state on its own.
- **Only reanalysis changes assessment.** After editing, the user **triggers reanalysis** (§L) to produce an updated assessment of the changed content. Until reanalysis runs, the displayed assessment reflects the prior analysis (the Workspace makes this state clear, §L).
- Editing **generates no findings/recommendations** and performs no governance/execution/automation.

## L. Reanalysis Experience

- **The artifact remains visible during reanalysis** — the user is never blocked from reading the content while analysis runs.
- **Prior state remains visible** during reanalysis (overlays/findings reflect the previous analysis), with a clear **reanalysis status** indicator (§D.8) showing that an update is in progress.
- **Updated state appears after reanalysis** completes — overlays, findings, and signals refresh to the new analysis.
- **Possible per-finding outcomes** of reanalysis: a finding **weakens**, a finding is **unchanged**, a finding is **superseded**, or a finding **closes**. These outcomes are **produced by reanalysis**, presented here; the Workspace does not itself change finding state.

## M. History Experience

- Artifact analysis history is **append-only**.
- Users can **inspect prior artifact analyses** — earlier states of the artifact's findings/overlays/signals are retained and viewable.
- **No deletion. No mutable history.** Prior analyses are never overwritten or removed; supersession is additive (the prior state is retained alongside the new one).

## N. Empty States

The Workspace must **distinguish**:

- **No findings** — the artifact was analyzed and **no weaknesses were found** (neutral/positive; not alarming; not "incomplete").
- **No overlays** — there are no overlays to render for the current artifact/view (e.g., none in the visible section), distinct from "no findings in the artifact at all."
- **Not yet analyzed** — the artifact (or its latest edit) has **not been analyzed yet** (show the analyzing/awaiting-reanalysis state, per the Orientation State Model), distinct from "none found."
- **Unavailable** — the artifact or its analysis is **temporarily unavailable**, distinct from "none found."

## O. Progressive Disclosure

- **Artifact content is always primary** — the content area is the persistent, central surface.
- **Finding details are secondary** — surfaced via overlays and the contextual Finding Panel, one interaction from the content.
- **Recommendation details are tertiary** — surfaced via the Recommendation Panel, reached from a finding.
- **Intentionally absent:** scores/percentages/ranks; finding/recommendation generation; governance/execution/automation/agents; any new object surface; project/task management.

## P. Integrity Rules

- **AW-1.** **Artifact content remains primary** — the content area is the center of gravity; nothing replaces it.
- **AW-2.** **Overlays never replace content** and **create no new objects**; an overlay is a presentation marker over existing findings (one or multiple) at a location.
- **AW-3.** **Findings remain descriptive** — surfaced in context, never framed as actions/commands; never duplicated, created, edited, or resolved by the Workspace.
- **AW-4.** **Recommendations remain advisory** — OSLO Recommended / Possible Resolution Paths / Selected Path are **presentation-only**; no Resolution Path / Clarification Candidate / Resolution Candidate object.
- **AW-5.** **Editing changes no assessment**; **only reanalysis changes assessment** (CAF / Reliability / Confidence / finding state).
- **AW-6.** The Workspace **computes nothing** (no scoring / CAF / Reliability / Confidence calculation) and **generates nothing** (no Findings / Recommendations).
- **AW-7.** **History is append-only** — no deletion, no mutable history; supersession is additive.
- **AW-8.** **No governance.**
- **AW-9.** **No execution.**
- **AW-10.** **No automation.**
- **AW-11.** **No agent actions.**
- **AW-12.** **No APIs, events, implementation, or styling** are defined here.
- **AW-13.** Understanding signals/overlays are **reliability-qualified** and presented (per the MRI Visualization Model), never recomputed; **no scores/percentages/ranks** are displayed.
- **AW-14.** MRI remains the **diagnostic discovery** experience and an **umbrella concept**; the Artifact Workspace **uses** its signals/snapshot and does not redefine them.

## Q. Conformance Requirements

A conforming Artifact Workspace MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:

- **AW-C1.** Keep **artifact content primary and persistent**; never replace content with a findings list or recommendations (§F, §H; AW-1/AW-2). **Fail** if content is replaced by a list.
- **AW-C2.** Render **CAF overlays embedded within content**, organized by CAF dimension, supporting hover / click / select / navigate, where **one overlay surfaces one or multiple findings** and **creates no new object** (§G; AW-2). **Fail** if an overlay creates an object or displays a numeric score/rank.
- **AW-C3.** Open **Finding Panels in context** (no standalone navigation) presenting explanation, evidence, CAF impact, supporting context, and recommendation access (§I; AW-3).
- **AW-C4.** Present Recommendations as **advisory** with OSLO Recommended / Possible Resolution Paths / Selected Path as **presentation-only** constructs and **no** Resolution Path / Clarification / Resolution Candidate object (§J; AW-4). **Fail** if any such object appears.
- **AW-C5.** Permit **content editing** while ensuring **editing changes no assessment**; require **reanalysis** to update assessment (§K, §L; AW-5). **Fail** if editing mutates assessment or finding state directly.
- **AW-C6.** Keep the **artifact visible during reanalysis** with prior state shown and a status indicator, refreshing to the updated state on completion, and presenting (not producing) per-finding outcomes weaken / unchanged / superseded / closed (§L).
- **AW-C7.** Maintain **append-only history** — inspectable prior analyses, **no deletion, no mutable history** (§M; AW-7). **Fail** if history is deleted or overwritten.
- **AW-C8.** Implement empty states distinguishing **no findings / no overlays / not yet analyzed / unavailable** (§N).
- **AW-C9.** Expose **no** computation, finding/recommendation generation, governance, execution, agent, automation, API, or event affordance (AW-6/AW-8…AW-12). **Fail** if any appears.
- **AW-C10.** Use the MRI Visualization Model signals / MRI Snapshot and the CAF/Reliability/Confidence assessments **without redefining or recomputing** them; display **no** scores/percentages/ranks (AW-13/AW-14). **Fail** if any value is recomputed or a numeric score is shown.

**Explicit fail conditions.** Conformance is **all-or-nothing**. The Artifact Workspace **fails** if it: replaces artifact content with a findings/recommendations list; creates any new object via overlays (or anywhere); computes any score, CAF, Reliability, or Confidence value or displays a numeric score/percentage/rank; generates a Finding or Recommendation; mutates assessment or finding/recommendation state through editing or any interaction other than reanalysis; deletes or mutates history; introduces a Resolution Path / Clarification Candidate / Resolution Candidate object; or exposes governance, execution, agents, automation, APIs, or events.

## R. Deferred Items

Explicitly **deferred / out of scope:** styling; implementation details; APIs; events; governance; execution; automation; agent behavior; exact overlay visual form/encoding and layout; precise editing affordances and content-format handling; numeric tier boundaries; calibration values; any computation/scoring/formula; and exact artifact-hierarchy modeling beyond navigation intent.

---

*This specification defines the canonical Release 1 Artifact Workspace — OSLO's primary content-centered operating surface, answering "What does the content actually say?" It keeps the artifact as the source of truth and center of gravity, renders CAF overlays embedded in content (one overlay surfacing one or multiple existing findings, creating no new object), surfaces Findings and Recommendations through contextual Panels (OSLO Recommended / Possible Resolution Paths / Selected Path as presentation-only constructs), permits content editing where editing changes no assessment, and triggers reanalysis as the only thing that updates assessment — with append-only history. It is UX/interaction only: no scoring, CAF/Reliability/Confidence computation, Finding/Recommendation generation, governance, execution, agents, automation, APIs, events, implementation, or styling. It completes the chain MRI discovers weakness → Artifact Workspace contextualizes weakness → Finding Panels explain weakness → Recommendation Panels evaluate possible responses, with the artifact at the center throughout.*

**Artifact Workspace Specification v1 complete.**
