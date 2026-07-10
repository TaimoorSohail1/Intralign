# Slice 5 — Plan Artifacts / Artifact Workspace · E2E Test Scenarios

**Cumulative (Slices 1–5).** Manual, single-file prototype. Each scenario is client-side only. ≤20 scenarios; NEW Slice-5 scenarios first, then key regressions.

Setup: open `prototype.html`; activate (invite → activate → welcome) or use a persisted session; land on Overview after Fast Pass. Use the phase bar **Restart** to reset.

---

## NEW — Slice 5

| # | Scenario | Steps | Expected |
|---|---|---|---|
| T1 | Open the workspace (D066) | Click **Artifacts** in the top-center switch. | The workspace opens: explorer (7 artifacts, Understanding/Execution) + empty-state editor prompt. |
| T2 | Live issue badges (D066) | Observe the explorer badges. | Resources shows a **red** badge (critical); Requirements/Schedule/Context/WBS show **amber/neutral** badges matching their open issues; Intent/Scope show no badge. |
| T3 | Open every artifact (D066/D067) | Click each of the 7 rows in turn. | Each opens in the editor: Intent/Context/Scope/Requirements read as prose (mixing bullets/table); Work breakdown/Schedule/Resources read as **tables**. Active row highlights. |
| T4 | Mixed-format Understanding (D067) | Open **Intent**, then **Context**. | Intent shows prose + a **bulleted goals list**; Context shows prose + a **stakeholder table**. |
| T5 | Edit → Confirmed by you (D069) | In any artifact, click into a prose block and type. | The block gains a **left-border accent**; its hover chip reads **"Confirmed by you"**. |
| T6 | Autosave + reanalysis chain (D070) | After T5, watch the status chip. | Chip runs **Saving… → Saved · analysis stale → Reanalyzing… → Up to date**; the stale hint bar appears then clears. |
| T7 | No manual reanalyze (D070) | Inspect the toolbar and page during/after editing. | There is **no "Reanalyze" button** anywhere; reanalysis is automatic. |
| T8 | Saving ≠ assessment copy (D069) | While editing, read the hint bar / info tooltip. | Copy states **saving changes no assessment; only reanalysis does.** |
| T9 | Annotation hover (D068) | Open **Resources**; hover the "Wi-Fi capacity unconfirmed" span. | The span is **red** (critical); the tooltip summarizes the Feasibility issue. |
| T10 | Annotation click → issue panel (D068) | Click that span. | The **light Issue panel** opens for ISS-01 (Why → Evidence → Clarification → Suggested fixes). Not resolved inline. |
| T11 | Weakness stepper (D071) | Open **Resources**; use **⌄ / ⌃** in "Jump to weakness". | The counter shows "k of N"; each step outlines a weak span and scrolls to it, cycling. |
| T12 | Artifact prev/next (D071) | Use the **‹ / ›** buttons. | Moves between artifacts in order; ‹ disabled on Intent, › disabled on Resources. |
| T13 | Resolve drops annotation + badge (D066/D068) | From T10, answer the clarification and submit. | After reanalysis the issue resolves; its annotation disappears from the artifact and the explorer badge decrements/clears. |
| T14 | Feature-tour editor step (D071/D044) | Start the tour; advance to the artifact step. | The workspace opens on **Resources** and the editor is spotlighted with edit/attest/reanalysis copy. |
| T15 | Autosave persistence (D067) | Edit an artifact; switch views and return. | The edited body (and Confirmed-by-you accents) persist within the session. |

## Regression (Slices 1–4)

| # | Scenario | Expected |
|---|---|---|
| T16 | Overview intact | Confidence → Start here → Progress → More; pill + popover; "how this is calculated"; "Strengthened" trend after Extended Analysis. |
| T17 | Attention heatmap intact | Heatmap-only (no field view); cell → issue / scoped-list routing; all-clear via the demo trigger. |
| T18 | Clarification loop intact | Light issue panel answers → reanalysis → issue resolves; Overview/heatmap counts update. |
| T19 | Funnel + chat intact | Activation, four-method intake, Fast Pass ≈30s, orientation, chat completion notices all work. |
| T20 | `node --check` clean | Extracted `<script>` passes `node --check` with no error. |
