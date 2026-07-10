# Slice 5 — Plan Artifacts / Artifact Workspace · Success Criteria

**Cumulative (Slices 1–5).** Slice 5 is successful when the following hold AND no Slice 1–4 behavior regresses.

Decisions covered: **D066–D071**.

---

## NEW — Slice 5

| # | Criterion | Decision |
|---|---|---|
| S5-1 | A third co-primary view **Artifacts** appears in the top-center switch and opens the workspace (explorer + editor). | D066 |
| S5-2 | The explorer lists the **7 plan artifacts** grouped **Understanding / Execution**; each carries a **live open-issue badge** whose count + color track the ISSUES data. | D066 |
| S5-3 | Clicking (or Enter/Space) an artifact opens it in the center editor; the active row is highlighted. | D066, D015 |
| S5-4 | **Understanding** artifacts render as prose by default and **at least one mixes bullets/tables** (Intent, Context, Requirements do); **Execution** artifacts render as **tables**. | D067 |
| S5-5 | The editor is **live-editable** (contenteditable); edits **autosave** to localStorage with a version bump. | D067 |
| S5-6 | Weak text is **inline-colored** (severity ramp, red/amber only); **hover** shows a summary; **click** opens the **light Issue panel**; weaknesses are **never resolved inline**. | D068, D003 |
| S5-7 | Blocks are **"From OSLO"** by default; **editing/confirming** flips a block to **"Confirmed by you"** with a **left-border accent**; copy states saving changes no assessment, only reanalysis does. | D069, D011 |
| S5-8 | Editing runs **Saved → analysis stale → Reanalyzing… → Up to date** automatically; **no manual "Reanalyze" button** exists anywhere. | D070, D006 |
| S5-9 | A **"Jump to weakness ⌃ k of N ⌄"** stepper cycles the weak spans in the open artifact; **‹ / ›** navigate between artifacts; both keyboard-operable. | D071, D015 |
| S5-10 | The **feature tour** includes a real **artifact-edit step** spotlighting the editor (former Slice-5 seam filled). | D071, D044 |
| S5-11 | Resolving a wired issue **drops its annotation** and **updates the explorer badge** live. | D066, D068 |

## Boundaries honored

| # | Criterion |
|---|---|
| S5-B1 | Severity color appears **only** on annotations, explorer badges, and the issue panel — confidence/CAF stay neutral (D003). |
| S5-B2 | The **full Issues surface** is **not** built; annotations route to the light panel (Slice-6 seam preserved) (D017). |
| S5-B3 | No backend/server/API/DB/auth/real-AI — client-side only, localStorage + simulated timers (D016). |
| S5-B4 | Advisory framing throughout — OSLO drafts/advises; the user edits and decides (D001). |
| S5-B5 | "Plan artifacts", "Issues", "Confirmed by you", "Clarification request", Clarity·Alignment·Feasibility terms used (D049, D017, D011/D069, D012). |

## Regression (Slices 1–4 must still pass)

| # | Criterion |
|---|---|
| R-1 | Activation funnel, four-method intake, Fast Pass ≈30s, orientation, advisory footer, account menu, GA preview toggle all work. |
| R-2 | Confidence-led Overview (Confidence→Start here→Progress→More), pill + popover, false-confidence flag, how-calculated, Project summary, "Strengthened" trend intact. |
| R-3 | Attention heatmap (heatmap-only), cell/scoped routing, empty + all-clear states intact. |
| R-4 | Clarification loop, light issue panel, Fast/Deep state machine (provisional→current, last-good+retry) intact. |
| R-5 | Chat rail + completion notices; feature tour (now with the editor step) run without error. |

## Verification

- `node --check` on the extracted `<script>` passes with no error.
- Manual walk-through: open all 7 artifacts; edit a block (observe Confirmed-by-you + the four-state chip); click an annotation (issue panel opens); step through weaknesses; navigate artifacts; confirm no reanalyze button.
