# Artifact Authoring & Editing Workflow Specification v1

**Document Type:** Workflow Specification (UX Workflow Only)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Aligns with and is subordinate to (authoritative — must not redefine):** `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` · `MRI_WORKSPACE_SPECIFICATION_V1.md` · `FINDING_PRESENTATION_SPECIFICATION_V1.md` · `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` · `SIXTY_SECOND_ORIENTATION_WORKFLOW_SPECIFICATION_V1.md` · `ORIENTATION_STATE_MODEL_V1.md` · `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · CAF Assessment · Reliability v2 · Confidence v2.

> **This is UX workflow only.** It must **not** define: APIs, events, implementation, styling, calculations, generation logic, governance workflows, or execution workflows. It **does not redefine any existing model.**
>
> **Core invariants.** Artifacts remain the **source of truth**. Editing **modifies content only**. **Saving changes no assessment.** **Only reanalysis changes assessment** (CAF, Reliability, Confidence, Findings, Recommendations). Findings remain **descriptive**; Recommendations remain **advisory**. Prior analysis remains visible until superseded. History is **append-only**. No governance, execution, automation, agent actions, scoring, calculation, or generation.

---

## A. Purpose

Define the canonical Release 1 workflow for **creating, editing, reviewing, saving, versioning, and reanalyzing** project artifacts **within the Artifact Workspace** — i.e., how users interact with **artifact content itself**. It answers:

> **"How do users improve project understanding through artifact authoring and editing?"**

The Artifact Workspace establishes artifact content as the primary **source of truth and center of gravity** but does not itself define the editing workflow. This specification supplies that workflow while preserving the diagnostic chain:

```text
Project Overview → MRI Workspace → Artifact Workspace → CAF Overlay Discovery
→ Finding Panel → Recommendation Panel → Artifact Editing → Reanalysis
```

so that artifacts remain the source of truth, findings remain descriptive, recommendations remain advisory, **editing changes no assessment directly**, and **only reanalysis** changes CAF / Reliability / Confidence / Findings / Recommendations.

## B. Scope

**In scope:** the UX workflow and state model for authoring/editing artifact content — entering/exiting editing, unsaved-change handling, **save vs. reanalysis**, overlay/finding/recommendation behavior **during** editing, **stale-analysis** communication, when reanalysis is **suggested vs. required**, the reanalysis experience, versioning/history surfacing, collaborative-edit appearance and conflict surfacing, and error states.

**Out of scope (explicitly):** APIs; events; implementation; styling; any calculation/scoring; any generation logic (Findings/Recommendations/CAF/Reliability/Confidence); governance workflows; execution workflows; agent/automation behavior; and any redefinition of Artifacts, Findings, Recommendations, the MRI Visualization Model, or the assessment models. The workflow **edits content and triggers reanalysis**; it **computes and generates nothing**.

## C. User Goals (questions answered)

- **"How do I change the content?"** → enter Editing Mode (§F).
- **"How do I keep my changes?"** → Save (§G) — distinct from reanalysis.
- **"Is what I'm seeing still accurate?"** → stale-analysis communication in the Pending Analysis State (§H).
- **"How do I get an updated assessment?"** → trigger Reanalysis (§I).
- **"What happens to the weaknesses I saw while I edit?"** → overlay/finding/recommendation behavior during editing (§J–§L).
- **"Can I see earlier versions?"** → versioning and append-only history (§M).
- **"What if someone else is editing?"** → collaborative editing and conflict surfacing (§N).
- **"What if reanalysis fails?"** → error states (§O).

## D. Workflow Overview

The workflow is a **content-editing state machine** layered on the Artifact Workspace, leaving assessment untouched until reanalysis:

```text
Artifact Workspace
   ↓
View Mode  ──edit──▶  Edit Mode  ──save──▶  Save
                                              ↓
                                     Pending Analysis State   (content saved; analysis now stale)
                                              ↓ (reanalysis triggered)
                                          Reanalysis           (running; prior state still visible)
                                              ↓
                                     Updated Understanding     (new analysis supersedes prior; appended to history)
```

Each state is defined in §E–§I with **purpose, visible information, allowed actions, transition conditions, and supersession behavior**. Across the whole machine: **content** advances through edit/save; **assessment** advances **only** at the Reanalysis → Updated Understanding step.

## E. Viewing Mode

- **Purpose:** read the artifact as the source of truth, with CAF overlays, Finding/Recommendation Panels, and the current (possibly prior) analysis visible. The default, non-editing state.
- **Visible information:** artifact content; CAF overlays; understanding signals (reliability-qualified, presented); reanalysis/staleness status (if the current analysis is stale, §H); access to history (§M).
- **Allowed actions:** read; navigate artifacts/overlays; open Finding/Recommendation Panels; inspect history; **enter Edit Mode**; **trigger reanalysis** (if applicable).
- **Transition conditions:** **→ Edit Mode** when the user enters editing; **→ Reanalysis** when the user triggers reanalysis from a stale/pending state.
- **Supersession behavior:** none here — Viewing Mode displays the **current canonical** analysis (or a clearly labelled prior analysis when pending, §H); it changes nothing.

## F. Editing Mode

- **Purpose:** modify **artifact content only**. This is authoring/editing of the artifact, not of assessments, findings, or recommendations.
- **Visible information:** the editable artifact content; an explicit **editing indicator**; unsaved-change indication; the prior analysis context shown **read-only** (overlays/findings are not editable and are visually held as "based on the previous analysis," §J–§K).
- **Allowed actions:** edit content; **save** (§G); **discard/cancel** unsaved changes; **exit** editing (with unsaved-change handling, below). The user may **not** edit findings/recommendations or any assessment value (those are not user-authored content).
- **Transition conditions / entering & exiting:**
  - **Enter (Q1):** the user explicitly enters Editing Mode from Viewing Mode (an intentional mode switch); the Workspace shows the editing indicator.
  - **Exit (Q2):** the user explicitly exits — by **saving** (→ Save/Pending Analysis) or by **discarding** (→ Viewing Mode with content unchanged). Exiting is always explicit about whether changes are kept.
  - **Unsaved changes (Q3):** unsaved changes are clearly indicated; attempting to leave with unsaved changes prompts the user to **save or discard** — changes are never silently lost and never silently saved.
- **Supersession behavior:** editing **supersedes nothing** by itself — it changes content in the working state only; no assessment, finding, recommendation, or history entry is superseded until **Save** (content) and **Reanalysis** (assessment) occur.

## G. Save Workflow

- **Purpose:** persist the edited **content**. Saving is a **content** operation.
- **Save vs. reanalysis (Q4 — central distinction):** **Saving changes content only and changes no assessment.** It does **not** modify CAF, Reliability, Confidence, Findings, or Recommendations. **Reanalysis** is a separate, explicit step that produces the updated assessment. A user can save without reanalyzing; the saved content then carries a **stale** prior analysis until reanalysis runs (§H).
- **Visible information:** confirmation that content is saved; an indication that the **displayed analysis now reflects prior content** (stale) and that **reanalysis is available** (§H).
- **Allowed actions:** continue editing; return to Viewing Mode; **trigger reanalysis**.
- **Transition conditions:** **Save → Pending Analysis State** whenever saved content differs from the content the current analysis was based on.
- **Supersession behavior:** the saved content **supersedes the prior saved content** (prior content retained in append-only history, §M); the **analysis is not yet superseded** — it remains the prior, now-stale analysis until reanalysis completes.

## H. Pending Analysis State

- **Purpose:** represent that **content has changed since the last analysis** — the displayed assessment is **stale** and awaits reanalysis. This is how the workflow keeps "content" and "assessment" honestly separated.
- **Visible information / stale communication (Q8, Q9):** the artifact shows its **current saved content** together with a clear, persistent indicator that **the displayed findings/overlays/signals are based on a previous analysis** and **do not reflect the latest edits**. Staleness is communicated explicitly (a labelled "analysis is out of date — reanalysis needed/recommended" state), never implied or hidden.
- **Allowed actions:** continue reading/editing; **trigger reanalysis**; inspect prior analysis/history.
- **When reanalysis is suggested vs. required (Q10, Q11):**
  - **Suggested** when content has changed in ways that *may* affect understanding — the Workspace **recommends** reanalysis (advisory prompt) but the user may keep working; the stale indicator persists.
  - **Required** when the displayed analysis would be **misleading if treated as current** — e.g., before relying on the assessment as up-to-date (such as treating findings/signals as reflecting the latest content). The workflow **requires** reanalysis to clear the stale state and present a current assessment. *(Exact triggering boundaries are presentation calibration, deferred — §S; this spec fixes the principle, not thresholds.)*
- **Transition conditions:** **→ Reanalysis** when reanalysis is triggered; remains Pending while content is stale and reanalysis has not run.
- **Supersession behavior:** none yet — the prior analysis is **retained and shown as prior**; supersession of the assessment occurs only at Updated Understanding (§I).

## I. Reanalysis Workflow

- **Purpose:** produce the **updated assessment** for the current saved content. **Reanalysis is the only operation that changes assessment** (CAF, Reliability, Confidence, Findings, Recommendations).
- **What happens during reanalysis (Q12):** OSLO reanalyzes the current content and produces updated CAF / Reliability / Confidence, and updated Findings/Recommendations, which then **supersede** the prior analysis. *(The workflow presents this; it defines no generation/calculation logic.)*
- **What remains visible during reanalysis (Q13):** the **artifact remains visible**; the **prior analysis (overlays/findings/signals) remains visible** as the last-known state, with a clear **reanalysis-in-progress** status. The user is never blocked from reading content.
- **Outcome — Updated Understanding:** on completion, overlays/findings/signals refresh to the new analysis. **Possible per-finding outcomes** (presented, not produced here): a finding **weakens**, is **unchanged**, is **superseded**, or **closes**.
- **Transition conditions:** **Reanalysis → Updated Understanding** on success; **→ Error State** on failure (§O).
- **Supersession behavior:** the **new analysis supersedes the prior analysis** (append-only — the prior analysis is retained in history, §M); content is unchanged by reanalysis.

## J. Overlay Behavior During Editing (Q5)

- During Editing/Pending states, **CAF overlays reflect the previous analysis** and are held as **stale/read-only context** — clearly marked as "based on the previous analysis," not as live assessment of the edited text.
- Overlays are **not edited** by content editing and **create no new objects**; they neither move to track edits nor recompute. They update **only** after reanalysis.
- Overlays never replace content and display no scores/ranks (per the Artifact Workspace spec).

## K. Finding Behavior During Editing (Q6)

- **Findings remain descriptive** and are shown as **based on the prior analysis** while content is being edited or is pending reanalysis; they are **not regenerated, edited, or resolved** by editing.
- Editing content does **not** change a finding's state. Findings change **only** through reanalysis (where they may weaken, stay unchanged, be superseded, or close).
- The Finding Panel remains available in context but is clearly attributed to the prior analysis until reanalysis completes.

## L. Recommendation Behavior During Editing (Q7)

- **Recommendations remain advisory** and are shown as **based on the prior analysis** during editing/pending; they are **not regenerated, applied, or executed** by editing.
- OSLO Recommended / Possible Resolution Paths / Selected Path remain **presentation-only** constructs; **no** Resolution Path / Clarification Candidate / Resolution Candidate object is introduced.
- Recommendations change **only** through reanalysis; editing changes none of them.

## M. Versioning And History (Q14, Q18)

- **Append-only.** Each saved content version and each completed analysis is **retained**; nothing is deleted or mutated.
- **Surfacing prior versions (Q14):** users can inspect prior **artifact content versions** and the **prior analyses** associated with them — the history shows how content and understanding evolved together.
- **Editing × history (Q18):** saving a new content version **appends** a version (prior retained); reanalysis **appends** a new analysis that supersedes the prior **without deleting it**. Supersession is **additive**, never destructive.
- **No deletion. No mutable history.**

## N. Collaborative Editing (Q16, Q17)

- **Collaborative edits appear (Q16)** as clearly attributed content changes within the shared artifact — the artifact remains the single source of truth; concurrent contributions are surfaced visibly rather than applied silently.
- **Conflicts are surfaced (Q17)**, not auto-resolved: when concurrent edits diverge, the workflow **presents the conflict** for the user to reconcile; it does **not** silently merge or pick a winner, and it performs **no governance** over the content.
- Collaboration changes **content** only; it changes no assessment — reanalysis still governs assessment, and findings/recommendations remain attributed to the analysis they came from. *(Detailed concurrency/merge mechanics are implementation — deferred, §S; this spec fixes the UX principles: visible attribution, explicit conflict surfacing, no silent merge.)*

## O. Error States (Q15)

- **Reanalysis failure (Q15):** if reanalysis fails, the workflow **retains the prior analysis as the last-known-good state** (still visibly attributed as prior), communicates the failure clearly, and offers **retry** — it does **not** discard content, fabricate an assessment, or leave the user without a coherent state.
- **Save failure:** communicated clearly with unsaved changes preserved (never silently lost).
- **Unavailable:** distinguish "temporarily unavailable" from a substantive empty/none state.
- Error states are **honest and recoverable**: content is never lost, assessment is never invented, and the user always knows whether what they see is current, stale, or failed.

## P. Progressive Disclosure

- **Always primary:** artifact content (source of truth) and the current mode (View/Edit) with staleness/reanalysis status.
- **Secondary:** finding details (overlays + Finding Panel), attributed to the prior or updated analysis as appropriate.
- **Tertiary:** recommendation details (Recommendation Panel); version/analysis history.
- **Intentionally absent:** scores/percentages/ranks; finding/recommendation generation; governance/execution/automation/agents; any new object surface; silent merges or silent saves.

## Q. Integrity Rules

- **AE-1.** Artifacts remain the **source of truth**; the workflow centers content.
- **AE-2.** **Editing modifies content only** — never findings, recommendations, or assessment values.
- **AE-3.** **Saving changes no assessment** — save is a content operation, explicitly distinct from reanalysis.
- **AE-4.** **Only reanalysis changes assessment** (CAF, Reliability, Confidence, Findings, Recommendations).
- **AE-5.** **Findings remain descriptive**; not regenerated, edited, or resolved by editing/saving.
- **AE-6.** **Recommendations remain advisory**; OSLO Recommended / Possible Resolution Paths / Selected Path are **presentation-only**; no Resolution Path / Clarification / Resolution Candidate object.
- **AE-7.** **Prior analysis remains visible until superseded** by a completed reanalysis; staleness is communicated explicitly.
- **AE-8.** **History is append-only** — no deletion, no mutable history; supersession is additive.
- **AE-9.** Unsaved changes are never silently lost and never silently saved; exiting edit is explicit (save or discard).
- **AE-10.** Overlays during editing are **stale, read-only context** that **create no new objects** and **recompute nothing**; they update only after reanalysis.
- **AE-11.** Collaboration surfaces edits visibly and **surfaces conflicts explicitly** — **no silent merge**, no auto-winner.
- **AE-12.** On reanalysis failure, the **prior analysis is retained** as last-known state; no assessment is fabricated; content is not lost.
- **AE-13.** **No governance. No execution. No automation. No agent actions. No scoring. No calculation. No generation.**
- **AE-14.** **No APIs, events, implementation, or styling** are defined here; no existing model is redefined.

## R. Conformance Requirements

A conforming Artifact Authoring & Editing workflow MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:

- **AE-C1.** Provide explicit **enter/exit Editing Mode** with an editing indicator and explicit unsaved-change handling (save or discard; never silent) (§F; AE-9). **Fail** if changes are silently saved or silently lost.
- **AE-C2.** Implement **Save as a content-only operation** that **changes no assessment**, distinct from reanalysis (§G; AE-3). **Fail** if saving alters CAF/Reliability/Confidence or any finding/recommendation state.
- **AE-C3.** Enter a **Pending Analysis State** when saved content differs from the analyzed content, communicating **staleness explicitly** (displayed analysis is based on previous content) (§H; AE-7). **Fail** if stale analysis is presented as current.
- **AE-C4.** Treat **reanalysis as the only operation that changes assessment**, keeping the artifact and prior analysis visible during reanalysis, and presenting (not producing) outcomes weaken / unchanged / superseded / closed (§I; AE-4). **Fail** if any non-reanalysis action changes assessment.
- **AE-C5.** Hold **overlays/findings/recommendations as prior-analysis context** during editing — not regenerated, edited, applied, executed, or resolved by editing (§J–§L; AE-2/AE-5/AE-6/AE-10). **Fail** if editing mutates a finding/recommendation/overlay or creates an object.
- **AE-C6.** Keep Recommendation constructs **presentation-only** with **no** Resolution Path / Clarification / Resolution Candidate object (§L; AE-6). **Fail** if any such object appears.
- **AE-C7.** Maintain **append-only versioning/history** for content and analyses — inspectable prior versions, **no deletion, no mutable history**, additive supersession (§M; AE-8). **Fail** if history is deleted or overwritten.
- **AE-C8.** Surface **collaborative edits visibly** and **conflicts explicitly**, with **no silent merge** and no governance over content (§N; AE-11). **Fail** if conflicts are auto-resolved silently.
- **AE-C9.** On **reanalysis failure**, retain the prior analysis as last-known-good, communicate the failure, offer retry, and lose no content (§O; AE-12). **Fail** if an assessment is fabricated or content is lost.
- **AE-C10.** Expose **no** governance, execution, automation, agent, scoring, calculation, generation, API, or event affordance (AE-13/AE-14). **Fail** if any appears.

**Explicit fail conditions.** Conformance is **all-or-nothing**. The workflow **fails** if it: changes any assessment (CAF/Reliability/Confidence/Findings/Recommendations) through editing or saving rather than reanalysis; presents stale analysis as current; silently saves, discards, or merges changes; regenerates/edits/resolves findings or recommendations through editing; introduces a Resolution Path / Clarification Candidate / Resolution Candidate object; deletes or mutates history; fabricates an assessment on reanalysis failure or loses content; or exposes governance, execution, automation, agents, scoring, calculation, generation, APIs, or events.

## S. Deferred Items

Explicitly **deferred / out of scope:** APIs; events; implementation; styling; any calculation/scoring; any generation logic (Findings/Recommendations/assessments); governance workflows; execution workflows; agent/automation behavior; exact thresholds for **reanalysis suggested vs. required** (presentation calibration); detailed concurrency/merge mechanics for collaborative editing; content-format/editor specifics; and numeric tier boundaries or calibration values.

---

*This specification defines the canonical Release 1 Artifact Authoring & Editing workflow within the Artifact Workspace — a content-editing state machine (View Mode → Edit Mode → Save → Pending Analysis → Reanalysis → Updated Understanding) that answers "How do users improve project understanding through artifact authoring and editing?" Artifacts remain the source of truth; editing modifies content only; saving changes no assessment; only reanalysis changes CAF, Reliability, Confidence, Findings, or Recommendations; prior analysis stays visible and explicitly marked stale until a completed reanalysis supersedes it; history is append-only; collaborative edits are visibly attributed and conflicts explicitly surfaced; and reanalysis failures retain the last-known-good analysis without losing content. It is UX workflow only: no APIs, events, implementation, styling, calculation, generation, governance, execution, automation, or agent actions, and it redefines no existing model.*

**Artifact Authoring & Editing Workflow Specification v1 complete.**
