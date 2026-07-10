# Slice 4 — Attention Map (MRI) · Success Criteria

Cumulative: the Slice 1–3 criteria still hold (no regression). Below are the Slice-4-specific acceptance criteria.

## Heatmap primary (D057)
- [ ] Attention view shows a grid: **7 rows** (plan artifacts, grouped Understanding / Execution) × **3 columns** (Clarity · Alignment · Feasibility).
- [ ] Cell shade tracks **attention severity** (l0 none → l1 warning → l2 moderate → l3 critical; brighter = more attention).
- [ ] Non-empty cells show the **open-issue count** + a **mini severity label**; multi-issue cells show a "multiple" marker.
- [ ] Legend reads **"Brighter = more attention — not a health score."**

## Cell → Issues routing (D058)
- [ ] A cell with **exactly one** open issue opens **that issue** in the light issue panel.
- [ ] A cell with **more than one** open issue opens the **scoped Issues list** with **both filters (artifact + dimension) visibly lit**.
- [ ] The scoped list is clearly a **seam** (dashed note referencing Slice 6); rows open their issues; closing an issue returns to the scoped list.
- [ ] Row header opens the artifact's issues; field card opens the dimension's issues (each collapses to the single-issue panel when only one matches).

## Field view (D059)
- [ ] A **Heatmap / Field** toggle exists; **Heatmap is primary**.
- [ ] Field view shows the three dimensions with a neutral level, an open-issue count, and a routing pointer.

## Severity-only coloring + hover (D060)
- [ ] Severity color (red/amber) appears **only** on attention cells (and issue severity chips).
- [ ] Confidence, CAF bars, reliability, and field-view levels are **neutral** — never health-colored.
- [ ] Hovering a live cell scales it; **empty cells do not react**.

## Empty / all-clear (D061)
- [ ] An artifact×dimension with no open issue is a **neutral, inert, non-clickable** `l0` cell (not in the tab order).
- [ ] When the whole map has no open issues, an **all-clear** state shows, framed as all-clear on *attention* (not success). Reachable via the "Sim all-clear" trigger.

## Co-primary + context (D062)
- [ ] Attention is reachable from the **top-center switch** and the **Overview "Attention map →" pointer**.
- [ ] Returning from Attention to Overview **restores the prior scroll position**.

## Boundaries / non-regression
- [ ] No Slice 5 artifact editor and no full Slice 6 Issues surface are built (only the scoped seam).
- [ ] Every Slice 1–3 route/screen/interaction still works (activation, intake, Fast/Deep pass, confidence pill + popover, false-confidence flag, clarification loop, tour, chat, "Plan artifacts" term).
- [ ] `node --check` on the extracted `<script>` passes with no error.

## Accessibility (D015)
- [ ] All live cells, row headers, field cards, and scoped rows are keyboard-focusable and activate on **Enter/Space**; empty cells are inert.
- [ ] Visible focus rings; dark default; AA contrast on the severity ramp.
