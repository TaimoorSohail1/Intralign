# Understanding Companion Surface Experience Specification v1

**Document Type:** Experience Specification (UX / Interaction Model Only)
**Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Consistent with and subordinate to (authoritative — must not redefine):** `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · `MRI_WORKSPACE_SPECIFICATION_V1.md` · `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` · `FINDING_PANEL_SPECIFICATION_V1.md` · `RECOMMENDATION_PANEL_SPECIFICATION_V1.md` · `OSLO_CHAT_AND_CLARIFICATION_EXPERIENCE_SPECIFICATION_V1.md` · `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1.md` · `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW_SPECIFICATION_V1.md` · CAF Assessment · Reliability v2 · Confidence v2.

> **Non-negotiable constraints.** This specification defines the persistent understanding companion surface, understanding visibility, understanding summaries, contextual understanding presentation, and navigation entry points only. It must **NOT** define governance, execution, automation, agents, approvals, task management, project-management workflows, APIs, events, implementation, styling, calculations, assessment generation, finding generation, recommendation generation, or direct assessment modification.
>
> The companion **computes nothing. Generates nothing. Governs nothing. Executes nothing.**
>
> **Only reanalysis changes assessment.** Artifacts remain the source of truth. Findings remain descriptive. Recommendations remain advisory. MRI remains the diagnostic discovery experience.

> ✅ **Reconciled — Q6 navigation (Decision 001, Option B ratified 2026-05-31).** Per `UNDERSTANDING_COMPANION_RECONCILIATION_DECISION_001.md` (Option B — Finding-Context Entry), selecting a Top Recommendation routes **Understanding Companion → Associated Finding Panel → Recommendation Panel**. The Companion never opens a Recommendation Panel directly; Recommendation Panels remain valid **only in Finding context** (consistent with `RECOMMENDATION_PANEL_SPECIFICATION_V1.md` and `FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md`). Reflected in Q6 and §I below.

---

## A. Purpose

Define the canonical Release 1 **Understanding Companion Surface**.

It answers:

> **"Where is the current state of project understanding always visible?"**

The Understanding Companion is the persistent understanding surface available throughout project-understanding work. It provides continuous visibility into:

- Outcome Confidence
- CAF understanding state
- Top Findings
- Top Recommendations
- Stale-analysis state
- OSLO Chat entry

without becoming a dashboard, cockpit, workflow-management surface, governance surface, execution surface, or assessment engine.

## B. Scope

**In scope:**

- Persistent understanding visibility
- Outcome Confidence visibility
- CAF visibility
- Top Findings visibility
- Top Recommendations visibility
- Stale-analysis visibility
- Contextual understanding presentation
- Understanding navigation shortcuts
- OSLO Chat entry
- Empty states
- Failure states
- Progressive disclosure

**Out of scope:** Everything excluded by governing specifications including: Governance · Execution · Automation · Agents · Approvals · Task management · Project-health management · Assessment generation · Finding generation · Recommendation generation · Direct assessment modification · APIs · Events · Implementation · Styling.

The companion **presents existing understanding only.**

## C. Companion Philosophy

The Understanding Companion exists to make project understanding **continuously visible** while users work.

It is: **visibility · orientation · understanding awareness.**

It is **not:** analysis · workflow · execution · governance · project health.

The companion provides a stable answer to:

> **"What does OSLO currently understand about this project?"**

without requiring users to navigate to MRI, Finding Panels, Recommendation Panels, or Chat. It **complements** those surfaces but **replaces none** of them.

## D. Owner-Level Decisions

**Q1 — Does Release 1 include a persistent companion?**
**Resolution: Yes.** A persistent Understanding Companion exists throughout project understanding work.

**Q2 — Where is it available?**
**Resolution:** Available within **Project Overview · MRI Workspace · Artifact Workspace.** Not available inside **Settings · Workspace Home · Project Dashboard · Project List.** The companion belongs to **Project Context.**

**Q3 — What information appears?**
**Resolution:** The companion presents: **Outcome Confidence Summary · CAF Summary · Top Findings · Top Recommendations · Stale Analysis State · Ask OSLO entry.** Nothing else.

**Q4 — Relationship to Chat**
**Resolution:** The companion contains an **Ask OSLO** entry point. Chat remains the conversational interaction layer. The companion is not Chat. Chat is not the companion.

```text
Understanding Companion
        ↓
      Ask OSLO
```

**Q5 — Relationship to Finding Panels**
**Resolution:** Top Findings launch:

```text
Understanding Companion
        ↓
     Finding Panel
```

Finding Panels remain the primary structured finding surface.

**Q6 — Relationship to Recommendation Panels**
**Resolution (per `UNDERSTANDING_COMPANION_RECONCILIATION_DECISION_001.md`, Option B):** Top Recommendations **do not** open Recommendation Panels directly. Because Recommendation Panels are valid **only in Finding context**, selecting a Top Recommendation **routes through the associated Finding.**

**Canonical path:**

```text
Understanding Companion
        ↓
 Associated Finding Panel
        ↓
 Recommendation Panel
```

This preserves Recommendation → Finding attribution and maintains Recommendation Panels as subordinate to Finding context. Recommendation Panels remain the primary structured recommendation surface.

**Q7 — Contextual behavior**
**Resolution: Yes.** The companion adapts to current context.

- **Project Overview** shows: Project-level understanding · Project-level findings · Project-level recommendations.
- **MRI Workspace** shows: Current MRI context · Relevant findings · Relevant recommendations.
- **Artifact Workspace** shows: Artifact-specific findings · Artifact-specific recommendations.

Context affects **presentation only.** No assessment changes occur.

**Q8 — Stale-analysis visibility**
**Resolution:** The companion **prominently surfaces stale-analysis state.** Understanding from stale analysis is clearly marked as **Previous Analysis** and **never presented as current understanding.** Consistent with: Navigation · Dashboard · Editing Workflow · OSLO Chat.

**Q9 — Finding filtering**
**Resolution:** Users may filter presented findings by CAF dimension: **Clarity · Alignment · Feasibility.** Filtering affects **presentation only.** No analysis occurs.

**Q10 — Collapsibility**
**Resolution:** The companion may be **expanded · collapsed.** Collapse affects **visibility only.** No understanding changes.

## E. Experience Architecture

```text
Project Surface
─────────────────────────────

Main Surface

(Project Overview
 MRI Workspace
 Artifact Workspace)

─────────────────────────────

Understanding Companion

• Outcome Confidence
• CAF Summary
• Top Findings
• Top Recommendations
• Stale Status
• Ask OSLO
```

The companion remains visible while users work. It is **not a destination.** It is part of the project-understanding environment.

## F. Outcome Confidence Visibility

The companion presents the existing **Outcome Confidence summary** and **reliability-qualified understanding state** as produced elsewhere.

The companion: **computes nothing · recalculates nothing · predicts nothing.**

Outcome Confidence remains **trust in understanding** — not project health, readiness, or outcome probability.

## G. CAF Visibility

The companion presents **Clarity · Alignment · Feasibility** as existing understanding dimensions. CAF visibility is **descriptive.** The companion performs **no CAF calculation.**

## H. Top Findings Visibility

The companion surfaces the **most relevant existing findings** from current understanding. Findings remain **descriptive · existing · previously produced.** Selecting a finding **opens the Finding Panel.**

## I. Top Recommendations Visibility

The companion surfaces the **most relevant existing recommendations** from current understanding. Recommendations remain **advisory · existing · previously produced.** Selecting a Top Recommendation **opens the associated Finding Panel first** and then **surfaces the Recommendation Panel from that Finding context.** The Companion **never opens a Recommendation Panel as a standalone destination** and **never bypasses the associated Finding** (per `UNDERSTANDING_COMPANION_RECONCILIATION_DECISION_001.md`, Option B).

## J. Ask OSLO Entry

The companion includes **Ask OSLO**, which launches OSLO Chat. The companion **never embeds the full chat experience.** Chat remains a separate interaction layer.

## K. Empty States

The companion distinguishes:

- **Not Yet Analyzed** — Understanding unavailable because analysis has not occurred.
- **No Findings** — No findings currently exist.
- **No Recommendations** — No recommendations currently exist.
- **No Context** — No contextual understanding available.
- **Unavailable** — Companion temporarily unavailable. Distinct from empty.

## L. Failure States

Failures are honest and recoverable.

- **Understanding Unavailable** — Display: *Understanding unavailable. Retry.* Never fabricate understanding.
- **Findings Unavailable** — Display: *Findings unavailable.* Never invent findings.
- **Recommendations Unavailable** — Display: *Recommendations unavailable.* Never invent recommendations.
- **Companion Unavailable** — Display: *Companion unavailable. Retry.* Underlying project surface remains usable.

## M. Progressive Disclosure

- **Immediately Visible:** Confidence Summary · CAF Summary · Stale State.
- **Secondary:** Top Findings · Top Recommendations.
- **Through Expansion:** Additional findings · Additional recommendations.
- **Through Navigation:** Finding Panel · Recommendation Panel · Ask OSLO.

## N. Integrity Rules

- **COMP-1.** Companion computes nothing.
- **COMP-2.** Companion generates nothing.
- **COMP-3.** Companion governs nothing.
- **COMP-4.** Companion executes nothing.
- **COMP-5.** Companion presents existing understanding only.
- **COMP-6.** Only reanalysis changes assessment.
- **COMP-7.** Confidence remains trust in understanding, never project health.
- **COMP-8.** Findings remain descriptive.
- **COMP-9.** Recommendations remain advisory.
- **COMP-10.** Companion complements but replaces no existing surface.
- **COMP-11.** Stale understanding is never presented as current.
- **COMP-12.** Companion introduces no new objects.
- **COMP-13.** Companion is not a workflow surface.
- **COMP-14.** Companion is not a governance surface.
- **COMP-15.** Companion contains no task-management behavior.
- **COMP-16.** Companion defines no APIs, events, implementation, or styling.

## O. Conformance Requirements

A conforming Understanding Companion MUST:

- Provide persistent understanding visibility.
- Present Confidence, CAF, Findings, Recommendations, Stale State, and Ask OSLO.
- Operate across Project Overview, MRI Workspace, and Artifact Workspace.
- Route to Finding Panels, Recommendation Panels, and Chat.
- Preserve all understanding invariants.
- Present stale understanding honestly.
- Compute nothing.
- Generate nothing.
- Govern nothing.

**Fail conditions include:**

- Computing scores.
- Generating findings.
- Generating recommendations.
- Presenting project health.
- Performing governance.
- Performing execution.
- Creating new objects.
- Presenting stale understanding as current.
- Becoming a workflow-management surface.

## P. Deferred Items

Explicitly deferred:

- Personalized companion layouts
- Companion customization
- Multi-project companion views
- Workspace-level companion views
- Mobile-specific companion behavior
- Advanced finding grouping
- Advanced recommendation grouping
- Implementation
- Styling
- APIs
- Events
- Any calculation behavior

---

*This specification defines the canonical Release 1 Understanding Companion Surface — the persistent understanding visibility layer available across Project Overview, MRI Workspace, and Artifact Workspace. It provides continuous visibility into Outcome Confidence, CAF understanding, Top Findings, Top Recommendations, stale-analysis state, and Ask OSLO, while remaining strictly presentation-only. It complements Chat, Finding Panels, Recommendation Panels, MRI, and Artifact Workspace without replacing any of them. It computes nothing, generates nothing, governs nothing, executes nothing, introduces no new objects, and preserves all understanding invariants. Only reanalysis changes assessment.*

**Understanding Companion Surface Experience Specification v1 complete.**
