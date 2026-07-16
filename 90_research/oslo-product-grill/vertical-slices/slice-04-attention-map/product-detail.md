# Slice 4 — Attention Map (MRI) · Product Detail

Advisory-only (D001). Client-side prototype (D016). Cumulative over Slices 1–3.

## Scope of this slice
Deepen the Slice-2 heatmap into the primary MRI visual and wire cell → Issues routing. Build the scoped-list **seam** (not the full Slice-6 Issues surface). Add empty/all-clear states and the field-view toggle. Preserve all prior behavior.

## Feature detail

### F4.1 — Heatmap primary (D057)
- Grid: **7 rows** (plan artifacts, grouped Understanding: Intent · Context · Scope · Requirements; Execution: Work breakdown · Schedule · Resources) × **3 columns** (Clarity · Alignment · Feasibility).
- Each **cell** is an `{artifact, dimension}` bucket. Its shade = **attention severity** of the most severe open issue in the bucket:
  - `l0` — no open issue (neutral, inert)
  - `l1` — warning
  - `l2` — moderate
  - `l3` — critical (brightest)
- Cell content: the **open-issue count** (large) + a **mini severity label** ("critical" / "moderate" / "warning"). Cells with >1 open issue show a subtle "multiple" pip.
- Legend: **"Brighter = more attention — not a health score."** plus the axis key.

### F4.2 — Cell → Issues routing (D058)
`openFindingsFor(artifact, dimension)`:
- **exactly one** open issue → `openIssue(id)` (the light issue panel).
- **more than one** → `openScopedIssues({art, dim})` — the scoped Issues list with **both filters lit**.
- Row header → `openFindingsForArtifact(art)` (artifact filter only). Field card → `openFindingsDim(dim)` (dimension filter only). Both collapse to the single-issue panel when only one matches.
- `openCell` / `showSectionIssues` retained as **aliases** routing through the deepened logic (Slice-2/3 callers unbroken).
- The scoped panel shows: title (scope name), lit filter chips (each removable), a **dashed seam note** ("full Issues surface arrives in Slice 6"), and a scannable list. Clearing both filters closes the panel (the full unscoped list is Slice 6).

### F4.3 — Field view (D059)
- **Heatmap / Field** toggle. Heatmap primary; Field secondary.
- Field view: three dimension cards (Clarity · Alignment · Feasibility) with a neutral maturity level + bar, an **open-issue count**, and a routing pointer. The limiting dimension is marked "· the limit."
- Mirrors v4's `mview-heat` / `mview-field`; simplified to the light field read (the full CAF-triangle field canvas is out of R1 slice scope).

### F4.4 — Severity-only coloring + hover + legend (D060)
- The red/amber ramp appears **only** on `l1`–`l3` cells. Confidence, CAF bars, reliability, and the field-view levels stay on the **neutral maturity ramp**.
- Live cells scale on hover (`transform:scale(1.06)`); `l0` cells are overridden to not react.
- Legend restates: attention, not health.

### F4.5 — Empty / all-clear (D061)
- **Per-cell empty:** `l0` — neutral surface, no border color, `cursor:default`, no `role`/`tabindex`/`onclick` → inert.
- **Map all-clear:** when `heatModel().openTotal === 0`, the grid is hidden and the `#heatClear` state shows ("Nothing needs your attention right now"), framed as all-clear on attention, not success. Reachable via the "Sim all-clear" demo trigger.

### F4.6 — Co-primary placement + context preservation (D062)
- Reachable from the top-center **Overview · Attention** switch (co-primary) and the Overview **"Attention map →"** pointer.
- `showView()` records the leaving pane's `scrollTop` and restores the target pane's remembered scroll — returning preserves prior context.

## Boundaries (do NOT build here)
- **Slice 5** artifact editor — not built. Row headers route to issues, not an editor.
- **Slice 6** full Issues surface — only the scoped seam + lit filters. No grouping toggle, triage, or resolved tab.
- **Slice 7** timeline/history — not built.
- No confidence/CAF health-coloring; severity color stays on cells only (D003/D060).

## Open flags / spec notes
- None new. The multi-issue cell used for the D058 demo (Resources × Feasibility = 2 open issues: ISS-01 critical + ISS-03 moderate) is illustrative fake data, consistent with the Slice-2 issue set.
- **Extended-state cell map (post-Deep-Pass, per Enhancement #2 Phase 2):** once Extended Analysis auto-runs, the map holds **9 open issues across 8 of 21 cells**. Two more multi-issue cells appear — **Schedule × Feasibility** (ISS-04 moderate + ISS-07 critical) and **Scope × Alignment** (ISS-08 moderate + ISS-09 moderate) — plus **Scope × Clarity** (ISS-08) and **Schedule × Alignment** (ISS-07). ISS-07 (Feasibility+Alignment) and ISS-08 (Clarity+Alignment, a Resources↔Scope coherence gap) each light two cells via `_dimsOf`. The Alignment column now spans element↔element and element↔outcome coherence (ISS-05 accountability, ISS-07 sequencing, ISS-08 resource↔scope, ISS-09 scope↔outcome), not just stakeholder-agreement. A boot guard `_assertAlignmentSpansCoherence` covers this (self-check 141/141, 0 pageerrors). All fake/illustrative (D016).
