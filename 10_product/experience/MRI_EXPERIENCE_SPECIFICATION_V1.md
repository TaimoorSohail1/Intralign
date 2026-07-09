# MRI Experience Specification v1 (Missing · Risky · Incomplete)

**Type:** Diagnostic understanding & navigation experience (UX/interaction only)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Sits below (authoritative — presents, must not modify):** `FINDING_SYSTEM_SPECIFICATION_V1.md` · `FINDING_PRESENTATION_SPECIFICATION_V1.md` · `FINDING_PANEL_SPECIFICATION_V1.md` · `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` · `RECOMMENDATION_PANEL_SPECIFICATION_V1.md` · `SIXTY_SECOND_ORIENTATION_WORKFLOW_SPECIFICATION_V1.md` · `ORIENTATION_STATE_MODEL_V1.md` · `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · CAF Assessment · Reliability v2 · Confidence v2 · Release 1 Tier Definitions.

> ## ℹ MRI is one umbrella concept (per Reconciliation Decision 001)
> Per **`MRI_TERMINOLOGY_RECONCILIATION_DECISION_001.md`** (owner-ratified), **"MRI" is a single umbrella concept** — there are not two MRIs. It comprises: the **MRI Experience** (this document — the diagnostic understanding & navigation experience, Missing · Risky · Incomplete), the **MRI Visualization Model** (`MRI_MODEL_V1.md` — makes understanding observable via CAF · Reliability · Confidence), **MRI Snapshot** (the visualization snapshot), and **MRI Navigation** (drill-down into Finding / Artifact / Recommendation).
> - The **MRI Experience uses** the MRI Visualization Model and MRI Snapshot; it **does not replace or compete with them**. The Visualization Model's positions and `MRISnapshot` / `Time-to-First-MRI` are **unchanged**.
> - This is consistent with `MRI_MODEL_V1.md` §12, which already anticipated **navigation** and **interaction layers** as separate components extending how understanding is surfaced.
>
> **Non-negotiable scope.** UX/interaction only. The MRI Experience is **not** a new object, model, governance capability, workflow engine, or replacement for Findings/Artifacts/Recommendations. It introduces **no** new ontology, findings, recommendation behavior, governance, execution, agents, automation, scoring, calculation, APIs, events, or implementation. **Findings remain the canonical descriptive object; Recommendations the canonical advisory object; Artifacts the canonical planning context.** Only reanalysis changes assessment.

---

## A. Purpose

The MRI Experience is a **diagnostic understanding and navigation surface** that helps users **discover weaknesses in project understanding** — *what needs attention* — before entering artifact-specific or finding-specific investigation. It is a **lens over existing Findings**, grouping them into three intuitive diagnostic categories (**Missing · Risky · Incomplete**) and routing the user to the right place to investigate.

It sits in the journey:
```text
Project Intake → Analysis → 60-Second Orientation → MRI Experience → Finding Panel  or  Artifact Workspace
```

- **MRI answers:** *"What needs attention?"*
- **Artifact Workspace answers:** *"Show me exactly where it exists."*
- **Finding Panel answers:** *"Explain why it exists."*

## B. Scope

**In scope:** the MRI navigation experience; the **Missing / Risky / Incomplete** views; finding **discovery**; prioritization **presentation**; drill-down navigation; and MRI's relationships to Findings, Artifacts, Recommendations, and Reanalysis.

**Out of scope:** new objects/findings; new recommendation behavior; governance; execution; agents; automation; scoring; calculations; API contracts; events; implementation (Deferred §Q).

## C. User Goals (questions answered)

- **"What is missing?"** → the **Missing** view.
- **"What is risky?"** → the **Risky** view.
- **"What is incomplete?"** → the **Incomplete** view.
- **"What should I investigate first?"** → prioritization presentation (§H) — most-severe first.
- **"Where should I go next?"** → drill-down to Finding Panel (why), Artifact Workspace (where), or Recommendation Panel (what to consider).

## D. Architectural Position

MRI (here) is the **Diagnostic Understanding Layer** — a **lens and navigation surface** over the existing assessment, **not** the Artifact Layer and **not** the Finding Layer.
- It **does not own** findings (the Finding Layer does) or artifacts (the Artifact Layer does); it **groups and routes** to them.
- It sits **between** the 60-Second Orientation (the headline read) and the investigation workspaces (Finding/Artifact), giving the user a structured "what needs attention" step before deep investigation.
- It performs **no assessment** and changes **no** signal — it is presentation/navigation only.

## E. MRI Categories (lens over existing findings — no new ontology)

The three categories are **presentation groupings over the canonical Finding taxonomy** (`missing_information, ambiguity, assumption, inference, conflict, constraint, coverage_gap`). **No new finding type or object is created.**

| MRI category | Meaning (diagnostic) | Existing findings shown under it |
|---|---|---|
| **Missing** | Understanding is **absent** — needed information/coverage isn't there | `missing_information`, `coverage_gap` |
| **Risky** | Understanding is **present but risky** — unsupported or conflicting | `assumption`, `inference`, `conflict`, `constraint` |
| **Incomplete** | Understanding is **present but unclear/partial** | `ambiguity` (and partially-formed understanding) |

These mappings are a **lens**: the same canonical findings, organized by the *kind of weakness* they represent. A finding appears under exactly one MRI category (its dominant character); the category is a view, not a property added to the finding. *(Exact mapping of edge cases is presentation calibration, deferrable; it introduces no new type.)*

## F. Information Architecture (single canonical)

```text
MRI Experience
 ├─ Missing      → [Findings: missing_information, coverage_gap]
 ├─ Risky        → [Findings: assumption, inference, conflict, constraint]
 └─ Incomplete   → [Findings: ambiguity, partial understanding]
```

- Three top-level **category sections** (Missing / Risky / Incomplete), each containing the **findings** that fall under it, severity-ordered (§H).
- Each finding entry is a **summary** that **drills down** to the Finding Panel (and onward to Artifact/Recommendation). MRI **does not duplicate** findings — it lists and routes to them.
- This single architecture (three categories → findings → drill-down) is recommended for diagnostic clarity and Release 1 simplicity.

## G. Navigation Model

- **Overview → MRI:** from the Project Overview's findings summary, the user enters MRI to triage "what needs attention" across categories.
- **MRI → Finding Panel:** selecting a finding opens its Finding Panel ("why it exists").
- **MRI → Artifact Workspace:** selecting a finding's location opens the Artifact Workspace ("where it exists") — MRI surfaces the issue; the artifact provides location/context.
- **MRI → Recommendation Panel:** from a finding's recommendation entry, the user opens the Recommendation Panel ("what to consider").

MRI is a **navigation hub for diagnosis**: it surfaces and routes; it does not embed full investigation or editing.

## H. Prioritization Presentation

- Within and across categories, findings are presented **by severity** (critical → moderate → warning) using the **existing** severity concept — **no scores, percentages, or ranking numbers**.
- "What should I investigate first?" is answered by **surfacing the highest-severity items first** (e.g., a category with critical findings is emphasized). Prioritization is **qualitative presentation only**, consistent with the Finding Presentation Spec.

## I. Finding Relationship

- MRI is a **lens over Findings** — it **never duplicates** a finding, never creates a finding, and never alters one.
- A finding shown in MRI is the **same** canonical finding; MRI adds only a **category grouping** and a route. Opening it leads to the Finding Panel (the descriptive home of the finding).
- All Finding doctrine holds: findings remain **descriptive**, explainable, append-only; MRI changes none of it.

## J. Artifact Relationship

- MRI **surfaces issues**; **Artifacts provide location and context.** When the user wants "where exactly is this," MRI routes to the **Artifact Workspace** (the artifact/element the finding concerns).
- MRI is **not** the Artifact Layer and does **not** edit artifacts; it points into artifact context. *(The Artifact Workspace is referenced as a navigation target; its full spec is separate/out of scope here.)*

## K. Recommendation Relationship

- From a finding in MRI, the user can reach its recommendations. Presentation maintains **OSLO Recommended · Possible Resolution Paths · Selected Path** as **presentation constructs only** (per the Recommendation Presentation/Workspace specs) — **multiple Recommendations displayed together**, never objects/Clarification/Resolution Candidates.
- MRI surfaces the *existence* of recommendations as part of "what to do next"; full evaluation happens in the Recommendation Panel.

## L. Reanalysis Relationship

- MRI **updates after reanalysis**: as findings are weakened/closed/superseded by reanalysis, the Missing/Risky/Incomplete views update to reflect the current set; prior states are retained in history (append-only).
- **Only reanalysis changes assessment** — entering MRI, triaging, or navigating changes **no** CAF/Reliability/Confidence and resolves no finding. During reanalysis (per the Orientation State Model), MRI remains readable with an "updating" indicator and reflects the previous analysis until complete.

## M. Empty States

- **No Missing / No Risky / No Incomplete findings:** the corresponding category shows a neutral/positive "Nothing needs attention here" — never alarming; never implying incomplete analysis when complete.
- **No findings at all:** a positive "No issues found — understanding looks clear" state, distinct from "not yet analyzed."
- **Not yet analyzed:** show the Analyzing/updating state (per Orientation State Model), not an empty MRI.
- **Unavailable:** distinguish "temporarily unavailable" from "none found."
- All empty states **distinguish none-found / unavailable / not-yet-analyzed**.

## N. Progressive Disclosure

- **Always visible:** the three category sections (Missing / Risky / Incomplete) with their counts and highest-severity items.
- **Expands in place:** the finding list within a category (severity-ordered); finding summaries.
- **Opens a dedicated experience:** a finding's **Finding Panel** (why), **Artifact Workspace** (where), or **Recommendation Panel** (what to consider).
- **Intentionally absent:** scores/percentages; editing affordances; governance/execution/automation; any new object surface.

## O. Integrity Rules

- **MRIE-1.** MRI introduces **no new objects, models, findings, or ontology** — it is a lens/navigation surface.
- **MRIE-2.** MRI is a **lens over existing Findings**; it never duplicates, creates, or alters a finding.
- **MRIE-3.** MRI categories (Missing/Risky/Incomplete) are **presentation groupings** over the canonical finding taxonomy.
- **MRIE-4.** MRI remains **diagnostic** — it surfaces "what needs attention," it does not investigate-in-place or edit.
- **MRIE-5.** MRI **performs no actions** and offers no execution/apply/agent/govern affordance.
- **MRIE-6.** MRI **never changes assessment** — only reanalysis does; navigating MRI alters no CAF/Reliability/Confidence and resolves no finding.
- **MRIE-7.** Findings remain **descriptive**; MRI never frames them as actions/commands.
- **MRIE-8.** Recommendations remain **advisory**; OSLO Recommended / Possible Resolution Paths / Selected Path are presentation-only (no objects).
- **MRIE-9.** Prioritization is **qualitative (severity)** — no scores/percentages/ranking numbers.
- **MRIE-10.** MRI **routes** to Finding/Artifact/Recommendation surfaces; it does not embed editing or task management.
- **MRIE-11.** History/state reflect the current analysis and update only via reanalysis; prior retained (append-only).
- **MRIE-12.** MRI introduces **no governance, accepted-understanding, disposition, agent, or automation** concept.

## P. Conformance Requirements

A conforming MRI Experience MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:
- **MRIE-C1.** Present exactly the three categories (Missing/Risky/Incomplete) as **groupings over existing findings**, with no new finding/object (MRIE-1/MRIE-2/MRIE-3).
- **MRIE-C2.** List, never duplicate, findings; route each to its Finding Panel (MRIE-2/MRIE-10).
- **MRIE-C3.** Route to Artifact context for "where" and Recommendation Panel for "what to consider," maintaining OSLO Recommended / Possible Resolution Paths / Selected Path as presentation-only (MRIE-8; §J/§K).
- **MRIE-C4.** Order by **severity** qualitatively; show **no** score/percentage/rank (MRIE-9).
- **MRIE-C5.** Ensure no MRI interaction changes a CAF/Reliability/Confidence signal or resolves a finding; only reanalysis does (MRIE-6). **Fail** if assessment changes via MRI.
- **MRIE-C6.** Expose **no** execution/apply/agent/govern/edit affordance (MRIE-5/MRIE-12). **Fail** if execution or governance appears.
- **MRIE-C7.** Update views after reanalysis; retain prior in history (append-only) (MRIE-11).
- **MRIE-C8.** Implement empty states distinguishing none-found / unavailable / not-yet-analyzed (§M).

Conformance is **all-or-nothing**; any new object/finding, duplicated finding, displayed score, governance/execution affordance, in-place editing, or assessment change via MRI **fails conformance**.

## Q. Deferred Items

**MRI terminology — resolved (not deferred):** the MRI umbrella reconciliation is **owner-ratified** in `MRI_TERMINOLOGY_RECONCILIATION_DECISION_001.md` (MRI = umbrella; Experience uses the MRI Visualization Model + MRI Snapshot). The only residual is non-urgent terminology hygiene (downstream docs renaming "MRI Model" → "MRI Visualization Model" on next touch) and whether **MRI Navigation** later separates into its own spec (deferred per Decision 001 §6).

Explicitly **deferred / out of scope:** the **Artifact Workspace** full spec; governance/accepted-understanding/disposition; automation/agents/execution; future orchestration; APIs/events; computation/scoring/calculations; styling; numeric tier boundaries; calibration values; exact edge-case category mapping (presentation calibration).

## R. Ratified update — Outcome Confidence presentation (DL-085, 2026-07-02)

Ratified by **DL-085**. Where the MRI understanding-overview surfaces the **Outcome Confidence** signal, it follows DL-085: the sanctioned **numeric index (0–100) is focal, with band + reliability as qualifiers, never bare** (Master Spec §20). This applies **only** to the Outcome Confidence signal. **MRIE-9 / MRIE-C4 are unchanged and binding:** finding **prioritization** and **weakness-map (heatmap) intensity** remain **qualitative** (severity) with **no scores, percentages, or ranking numbers** — the Outcome Confidence index is not a finding/heatmap score. Visual reference of record: `product-design/oslo_r1_experience_mockup_v4.html`.

---

*This specification defines the canonical Release 1 MRI Experience — a component of the MRI umbrella (per Reconciliation Decision 001) alongside the MRI Visualization Model, MRI Snapshot, and MRI Navigation. The MRI Experience (Missing · Risky · Incomplete) is a diagnostic understanding and navigation surface — a lens over existing Findings grouped into Missing/Risky/Incomplete, severity-ordered, that answers "what needs attention?" and routes to the Finding Panel (why), Artifact Workspace (where), and Recommendation Panel (what to consider). It uses the MRI Visualization Model and MRI Snapshot rather than competing with them. It introduces no new object, model, ontology, finding, recommendation behavior, governance, execution, automation, scoring, API, event, or styling; preserves Findings as descriptive, Recommendations as advisory, Artifacts as planning context, and that only reanalysis changes assessment.*

## S. Ratified update — reached via its own surface (DL-090, 2026-07-02)

Ratified by **DL-090** (presentation-only). The MRI Experience (weakness map / heatmap) is reached via its own **"Attention map" left-rail surface**, **not** embedded in the Project Overview (which previously hosted the heatmap). All MRI integrity rules stand (qualitative; no scores/ranks; only reanalysis changes assessment). Visual reference of record: `product-design/oslo_r1_experience_mockup_v4.html` (baseline `07-attention-map`).

**MRI Experience Specification v1 complete.**
