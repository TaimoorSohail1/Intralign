# MRI Workspace Specification v1

**Type:** Workspace specification (user experience / interaction model only)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Component of the MRI umbrella** (per `MRI_TERMINOLOGY_RECONCILIATION_DECISION_001.md`): the MRI Workspace is where the **MRI Experience** is hosted — the primary diagnostic environment that **uses** the **MRI Visualization Model** and **MRI Snapshot**.
**Must be consistent with (authoritative — presents, must not modify):** `MRI_MODEL_V1.md` (MRI Visualization Model) · `MRISnapshot` · `SIXTY_SECOND_ORIENTATION_WORKFLOW_SPECIFICATION_V1.md` · `ORIENTATION_STATE_MODEL_V1.md` · `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · `FINDING_SYSTEM_SPECIFICATION_V1.md` · `FINDING_PRESENTATION_SPECIFICATION_V1.md` · `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` · CAF Assessment · Reliability v2 · Confidence v2 · `MRI_EXPERIENCE_SPECIFICATION_V1.md`.

> **Non-negotiable constraints.** UX and interaction only. **No** scoring logic, Confidence calculation, Reliability calculation, CAF calculation, Finding generation, Recommendation generation, governance, execution, agents, automation, APIs, events, implementation details, or styling specifications. **MRI remains an umbrella concept.** This specification defines the **user-facing MRI Workspace only**. Findings remain the canonical descriptive object; Recommendations the canonical advisory object; Artifacts the canonical planning context. **Only reanalysis changes assessment.**

---

## 1. Purpose

The **MRI Workspace** is OSLO's **primary diagnostic workspace** — the canonical environment for **discovering, exploring, visualizing, and navigating weaknesses in project understanding**. It sits between **Project Overview** and **Artifact Workspace** and answers the workspace's defining question:

> **"Where are the weaknesses in project understanding?"**

It is the place a user goes after the headline read (Project Overview / 60-Second Orientation) to **investigate** — to move from *"how strong is my understanding overall"* to *"where, specifically, is it weak, and where should I look?"* The MRI Workspace makes weakness **discoverable through visualization and exploration** rather than through a flat issue list.

It hosts the **MRI Experience** (Missing · Risky · Incomplete) and the **MRI Visualization Model**'s observable signals (CAF, Reliability, Outcome Confidence) within a single diagnostic console, and routes the user onward to artifact context, finding explanation, and recommendation evaluation.

## 2. Scope

**In scope:** the MRI Workspace as a **diagnostic discovery environment** — its visualization areas; its navigation model; the **diagnostic lenses** (CAF Dimension, Artifact, Finding Type, Severity, Lifecycle Status, Concentration, Cross-Artifact Relationships); the **heatmap** discovery experience; **cross-artifact relationship** exploration; the **finding discovery** and **artifact drill-down** workflows; **Finding Panel** and **Recommendation Panel** integration; progressive disclosure; state integration; and empty states.

**Out of scope (explicitly):** any computation (scoring / CAF / Reliability / Confidence); any generation (Findings / Recommendations); governance; execution; agents; automation; APIs; events; implementation; styling; and any redefinition of the MRI Visualization Model, Findings, Recommendations, or Artifacts. The Workspace **presents** and **navigates**; it computes and generates nothing.

## 3. User Goals (questions answered)

- **"Where are the weaknesses?"** → the visualization areas + heatmap (§5, §8).
- **"Where should I look first?"** → severity / concentration lenses + prioritized presentation (§7, §8).
- **"What kind of weakness is this — missing, risky, or incomplete?"** → MRI Experience categories surfaced as a lens (§7).
- **"Which dimension of understanding is weak?"** → the CAF Dimension lens (§7).
- **"Which artifact is most affected?"** → the Artifact lens + drill-down (§7, §11).
- **"How do weaknesses relate across artifacts?"** → cross-artifact relationship exploration (§9).
- **"Why does this weakness exist?"** → Finding Panel (§12).
- **"What could I consider doing about it?"** → Recommendation Panel (§13).
- **"Where do I go to see the actual content?"** → Artifact Workspace (§11).

## 4. Workspace Architecture

The MRI Workspace is the **diagnostic hub** in OSLO's investigation chain:

```text
Project Overview          ← "How strong is my understanding overall?"
   ↓
MRI Workspace             ← "Where are the weaknesses?"  (THIS DOCUMENT)
   ↓
Artifact Workspace        ← "What does the content actually say?"
   ↓
Finding Panel             ← "Why does this weakness exist?"
   ↓
Recommendation Panel      ← "What could I consider doing?"
```

**Rationale for this architecture.** The MRI Workspace and the **Artifact Workspace are complementary views of the same project understanding**:

- **MRI Workspace answers "Where should I look?"** — it is *diagnostic*, organizing understanding by weakness so the user can find what matters without reading everything.
- **Artifact Workspace answers "What does the content actually say?"** — it is *content-bound*, showing the artifact and its weaknesses in situ.

Keeping these as **two surfaces** (rather than one) is deliberate: a single screen that both diagnoses across the whole project and shows full artifact content would force a flat issue list and bury the diagnostic signal. Separating *where to look* from *what it says* lets MRI stay a **diagnostic console** and lets the Artifact Workspace stay a faithful content view. The chain preserves OSLO's understanding flow:

> **Project Understanding → Weakness Discovery → Artifact Context → Finding Explanation → Recommendation Evaluation**

**Panels, not workspaces, for Findings and Recommendations.** Findings and Recommendations are **first-class objects in the model**, but in the diagnostic flow they are surfaced **contextually** — through a **Finding Panel** and a **Recommendation Panel** that open *in the context the user is already investigating* — rather than through separate dedicated workspaces. This keeps the user in the diagnostic flow (discover → context → explanation → evaluation) instead of context-switching to standalone screens. *(This Release 1 panel-centric choice does not retract the canonical status of Findings/Recommendations as objects, nor the existing Finding/Recommendation presentation specs; it positions how they appear within the MRI Workspace.)*

**What the MRI Workspace is not:** a Findings list, an issue tracker, a project-management screen, a task-management screen, or a governance screen. **What it is:** diagnostic, exploratory, investigative, understanding-oriented — a **diagnostic console for project understanding**, not an issue-management system.

## 5. MRI Visualization Areas

The Workspace presents the **MRI Visualization Model**'s observable signals and the project's weakness structure as **discovery surfaces** (visual form/styling out of scope). The canonical areas are:

- **Understanding overview area** — the observable CAF / Reliability / Outcome Confidence signals (per the MRI Visualization Model), reliability-qualified and never bare; the orienting "state of understanding" the user is investigating from. **Presented, not computed.**
- **Weakness map (heatmap) area** — the primary discovery surface showing **where** weakness concentrates across the project (§8).
- **Lens / filter area** — controls to switch the active **diagnostic lens** (§7), reshaping the map and lists without changing any underlying assessment.
- **Discovery list / detail area** — the findings revealed by the current lens/selection, severity-ordered, each routing to context, explanation, and evaluation.
- **Relationship area** — cross-artifact relationship exploration (§9), revealing how weaknesses connect across artifacts.

All areas are **views over the same MRI Snapshot / current analysis**; switching areas or lenses **re-presents** existing data and changes nothing.

## 6. MRI Navigation Model

- **Entry:** from **Project Overview / 60-Second Orientation** ("investigate the weaknesses") into the MRI Workspace.
- **Within the Workspace:** the user **switches diagnostic lenses** (§7), **selects regions** of the heatmap (§8), and **traverses relationships** (§9) to narrow from the whole project to a specific weakness — exploration, not a linear list scroll.
- **Outward (MRI Navigation, per Decision 001):**
  - **→ Artifact Workspace** — "show me the content where this exists" (§11).
  - **→ Finding Panel** — "explain why this weakness exists" (§12), opened in context.
  - **→ Recommendation Panel** — "what could I consider" (§13), opened in context.
- **Return:** the user can return to the diagnostic view from any panel/drill-down without losing the active lens/selection.

Navigation **surfaces and routes**; it never edits artifacts, generates findings/recommendations, or alters assessment.

## 7. Diagnostic Lenses

The Workspace supports **multiple diagnostic lenses** over the **same** set of existing findings and observable signals. A lens is a **presentation reorganization** — it introduces no new object, finding, or computation. Release 1 lenses:

| Lens | "Where are the weaknesses, organized by…" | Built from (existing concepts) |
|---|---|---|
| **By CAF Dimension** | Clarity / Alignment / Feasibility | CAF dimensional assessment (presented, not computed) |
| **By Artifact** | which artifact each weakness sits in | finding ↔ artifact reference |
| **By Finding Type** | the canonical 7-type taxonomy; also expressible as the MRI Experience **Missing / Risky / Incomplete** grouping | Finding type; MRI Experience categories |
| **By Severity** | critical → moderate → warning (qualitative) | existing severity concept |
| **By Lifecycle Status** | detected / acknowledged / addressed / closed / reopened / superseded | Finding lifecycle |
| **By Concentration** | where weaknesses cluster (which artifacts/areas carry the most) | counts/grouping over existing findings |
| **By Cross-Artifact Relationships** | how weaknesses connect across artifacts | relationship exploration (§9) |

Lenses are **co-equal** (no canonical hierarchy among them) and **non-destructive**: switching a lens re-presents the same findings; it does **not** filter anything out of existence, recompute anything, or change a finding's state. Severity, concentration, and any ordering are **qualitative** — **no scores, percentages, or ranking numbers**.

## 8. Heatmap Experience

The **heatmap** is the Workspace's primary **discovery-through-visualization** surface — it answers *"where should I look?"* at a glance by making **concentration of weakness** visible across the project.

- **Purpose:** let users **discover** findings by exploring a visual weakness map rather than reading a flat issue list.
- **Organized by the active lens:** the heatmap re-projects under the current lens (e.g., artifact × severity, or CAF dimension × artifact) — same data, different projection.
- **Qualitative only:** intensity expresses **qualitative** concentration/severity (e.g., more/stronger weakness), **never a numeric score, percentage, or rank**. No formula determines intensity here; it reflects the existing qualitative signals.
- **Interactive discovery:** selecting a region narrows the discovery list (§5) to the findings in that region and offers the outward routes (Artifact / Finding Panel / Recommendation Panel).
- **Non-destructive & assessment-neutral:** exploring the heatmap changes no CAF/Reliability/Confidence signal and resolves no finding.
- **Reliability-qualified:** where the heatmap implies strength/weakness of understanding, it remains **reliability-qualified** (per the Visualization Model and Reliability v2) and never presents understanding strength as if fully supported when it is not.

## 9. Cross-Artifact Relationship Exploration

- **Purpose:** reveal how weaknesses **connect across artifacts** — e.g., the same ambiguity or conflict implicating multiple artifacts — so the user can see systemic weakness, not just isolated points.
- **Built from existing relationships only:** it presents relationships that already exist among findings/artifacts in the current analysis; it **creates no new relationship object, finding, or link** and infers nothing not already in the model.
- **Exploratory:** the user traverses from a weakness to related weaknesses across artifacts, then routes to Artifact context or Finding explanation.
- **Assessment-neutral:** traversal changes nothing; only reanalysis changes the relationships or the findings.

## 10. Finding Discovery Workflow

The canonical **discovery-by-exploration** flow (not an issue-list scan):

1. **Orient** — read the observable understanding signals (CAF / Reliability / Confidence) in the overview area.
2. **Scan the heatmap** — see where weakness concentrates under the default/selected lens (§8).
3. **Apply a lens** — reorganize by CAF dimension, type/MRI category, severity, lifecycle, concentration, or relationships (§7).
4. **Select a region / cluster** — narrow to the findings in a chosen area.
5. **Inspect a finding summary** — in the discovery list (severity-ordered).
6. **Route outward** — to **Artifact Workspace** (where), **Finding Panel** (why), or **Recommendation Panel** (what to consider).

At every step the user is **discovering** existing findings; the Workspace **generates no findings** and **changes no assessment**.

## 11. Artifact Drill-Down Workflow

- From a weakness (heatmap region, finding summary, or relationship node), the user **drills into the Artifact Workspace** to see *"what the content actually says"* — the artifact and its weaknesses **in situ**.
- The MRI Workspace **hands off location/context**; the **Artifact Workspace owns artifact content**. MRI does not embed full artifact content or editing.
- This preserves the complementary split (MRI = *where to look*; Artifact = *what it says*) and the chain **Weakness Discovery → Artifact Context**.
- Drill-down is read/navigation; it edits no artifact and changes no assessment.

## 12. Finding Panel Integration

- Selecting a finding opens the **Finding Panel** **in context** (within the diagnostic flow), answering *"why does this weakness exist?"* per `FINDING_PRESENTATION_SPECIFICATION_V1.md`.
- The panel **presents** the canonical finding — descriptive, explainable, append-only; it **never** duplicates, creates, edits, or resolves a finding.
- The panel preserves all Finding doctrine: findings are **descriptive**, never framed as actions/commands; lifecycle states are presented, not mutated by the Workspace.

## 13. Recommendation Panel Integration

- From a finding, the user opens the **Recommendation Panel** **in context**, answering *"what could I consider doing?"* per `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md`.
- The panel **presents** the finding's Recommendations as **advisory** only, maintaining **OSLO Recommended · Possible Resolution Paths · Selected Path** as **presentation constructs** (multiple Recommendations displayed together) — never objects, never Clarification/Resolution Candidates.
- The panel **generates no recommendations**, applies nothing, and executes nothing; only the user acts, and only reanalysis changes assessment.

## 14. Progressive Disclosure Model

- **Always visible:** the understanding overview signals and the weakness heatmap (the diagnostic "where").
- **One interaction away:** lens switching; heatmap region selection; the discovery list for a selection.
- **Expands in context:** finding summaries; relationship traversal.
- **Opens a contextual panel:** Finding Panel (why), Recommendation Panel (what to consider).
- **Opens a separate surface:** Artifact Workspace (what the content says).
- **Intentionally absent:** scores/percentages/ranks; finding/recommendation editing or generation; governance/execution/automation; any new object surface; project/task management.

## 15. State Integration

- The MRI Workspace reflects the **Orientation State Model** (`ORIENTATION_STATE_MODEL_V1.md`): it is populated after analysis, shows an **updating** indicator during **reanalysis** while remaining readable (reflecting the prior analysis until complete), and updates to the new state when reanalysis completes.
- It consumes the current **MRI Snapshot** / analysis; **only reanalysis changes** what is shown (findings, signals, relationships). Switching lenses, exploring the heatmap, or opening panels changes **nothing**.
- Prior states are **retained** (append-only); the Workspace shows the current analysis and never silently discards history.

## 16. Empty States

- **No weaknesses found (analysis complete):** a neutral/positive "No weaknesses found — understanding looks clear" state; never alarming, never implying analysis is incomplete when it is complete.
- **No weaknesses under the current lens:** a per-lens "Nothing here under this lens" state, distinct from "none in the project."
- **Not yet analyzed:** show the Analyzing state (per Orientation State Model), not an empty heatmap.
- **Reanalysis running:** show the updating indicator over the prior analysis (§15).
- **Unavailable:** distinguish "temporarily unavailable" from "none found."
- All empty states **distinguish none-found / none-under-lens / not-yet-analyzed / unavailable**.

## 17. Integrity Rules

- **MRIW-1.** UX/interaction only — the Workspace **computes nothing** (no scoring / CAF / Reliability / Confidence calculation).
- **MRIW-2.** The Workspace **generates nothing** — no Findings, no Recommendations.
- **MRIW-3.** The Workspace **presents** existing signals, findings, recommendations, and relationships; it never duplicates, creates, edits, or resolves them.
- **MRIW-4.** **Only reanalysis changes assessment.** No lens switch, heatmap interaction, panel open, or drill-down alters any CAF/Reliability/Confidence signal or any finding state.
- **MRIW-5.** Findings remain **descriptive**; Recommendations remain **advisory**; OSLO Recommended / Possible Resolution Paths / Selected Path are **presentation-only**.
- **MRIW-6.** MRI remains an **umbrella concept**: the Workspace **uses** the MRI Visualization Model and MRI Snapshot; it does not redefine or replace them.
- **MRIW-7.** Diagnostic lenses are **co-equal, non-destructive presentation reorganizations** over the same data; switching a lens hides nothing from existence and recomputes nothing.
- **MRIW-8.** Prioritization, heatmap intensity, severity, and concentration are **qualitative** — **no scores, percentages, or ranking numbers**.
- **MRIW-9.** The Workspace **routes** to Artifact Workspace (content), Finding Panel (why), Recommendation Panel (what to consider); it embeds no artifact editing, task management, or issue tracking.
- **MRIW-10.** No **governance, execution, agents, automation, APIs, events**, or implementation/styling are introduced.
- **MRIW-11.** Cross-artifact relationships **presented only from existing relationships**; none are created or inferred beyond the model.
- **MRIW-12.** Reliability-qualified throughout — understanding strength is never shown as fully supported when Reliability says otherwise (Non-Collapse Invariant honored, not recomputed).

## 18. Conformance Requirements

A conforming MRI Workspace MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:

- **MRIW-C1.** Present the understanding overview signals and a weakness heatmap as the always-visible diagnostic surface (§5, §8); **fail** if it presents primarily as a flat issue list / tracker.
- **MRIW-C2.** Provide the Release 1 diagnostic lenses (CAF Dimension, Artifact, Finding Type / MRI category, Severity, Lifecycle Status, Concentration, Cross-Artifact Relationships) as non-destructive reorganizations of the same data (§7, MRIW-7).
- **MRIW-C3.** Make heatmap intensity, severity, concentration, and ordering **qualitative only** — show **no** score/percentage/rank (MRIW-8). **Fail** if any numeric score/rank is displayed.
- **MRIW-C4.** Route to Artifact Workspace for content, Finding Panel for explanation, Recommendation Panel for evaluation, preserving the chain Discovery → Artifact Context → Finding Explanation → Recommendation Evaluation (§4, §10–§13).
- **MRIW-C5.** Surface Findings/Recommendations via contextual **Panels** (not standalone workspaces) without duplicating, creating, editing, or resolving them (MRIW-3); maintain OSLO Recommended / Possible Resolution Paths / Selected Path as presentation-only (MRIW-5).
- **MRIW-C6.** Ensure **no** Workspace interaction changes a CAF/Reliability/Confidence signal or a finding state; only reanalysis does (MRIW-4). **Fail** if assessment changes via the Workspace.
- **MRIW-C7.** Expose **no** computation, finding/recommendation generation, governance, execution, agent, automation, API, or event affordance (MRIW-1/2/10). **Fail** if any appears.
- **MRIW-C8.** Present cross-artifact relationships only from existing relationships (MRIW-11); create/infer none.
- **MRIW-C9.** Reflect Orientation State (populated / reanalysis-updating / complete), retain prior states append-only, and implement empty states distinguishing none-found / none-under-lens / not-yet-analyzed / unavailable (§15, §16).
- **MRIW-C10.** Use the MRI Visualization Model and MRI Snapshot without redefining them; keep MRI an umbrella concept (MRIW-6).

**Explicit failure conditions.** Conformance is **all-or-nothing**. The MRI Workspace **fails** if it: behaves as a Findings list / issue tracker / project- or task-management / governance screen; computes any score, CAF, Reliability, or Confidence value; generates a Finding or Recommendation; displays a numeric score, percentage, or rank; mutates a CAF/Reliability/Confidence signal or a finding/recommendation state outside reanalysis; creates or infers a relationship, finding, or object; exposes governance, execution, agents, automation, APIs, or events; embeds artifact editing or task management; or redefines/replaces the MRI Visualization Model, MRI Snapshot, Findings, or Recommendations.

## 19. Deferred Items

Explicitly **deferred / out of scope:** the **Artifact Workspace** full spec (referenced as a navigation target); exact heatmap visual form, layout, and styling; precise visual encoding of lens intensity; whether **MRI Navigation** becomes its own spec (deferred per Reconciliation Decision 001 §6); numeric tier boundaries; calibration values; any computation/scoring/formula; APIs/events/implementation; governance/accepted-understanding/disposition; automation/agents/execution; and exact edge-case lens/category mapping (presentation calibration).

---

*This specification defines the canonical Release 1 MRI Workspace — a component of the MRI umbrella hosting the MRI Experience and using the MRI Visualization Model and MRI Snapshot. It is OSLO's primary diagnostic discovery environment, answering "Where are the weaknesses in project understanding?" through a weakness heatmap, multiple non-destructive diagnostic lenses, and cross-artifact relationship exploration, complementary to the Artifact Workspace ("what the content says"). It surfaces Findings and Recommendations via contextual Panels and preserves the chain Project Understanding → Weakness Discovery → Artifact Context → Finding Explanation → Recommendation Evaluation. It is UX/interaction only: no scoring, CAF/Reliability/Confidence calculation, Finding/Recommendation generation, governance, execution, agents, automation, APIs, events, implementation, or styling; Findings remain descriptive, Recommendations advisory, Artifacts the planning context, and only reanalysis changes assessment.*

**MRI Workspace Specification v1 complete.**
