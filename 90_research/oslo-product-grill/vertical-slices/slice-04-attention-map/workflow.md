# Slice 4 — Attention Map (MRI) · Workflow

Cumulative over Slices 1–3. Advisory-only (D001). The workflows below are the **new/changed** paths in Slice 4; all Slice 1–3 flows are preserved.

## W1 — Reach the Attention map (D062)
```
Overview  --[top-center: Attention]-->  Attention map (heatmap)
Overview  --["Attention map →" pointer]-->  Attention map (heatmap)
Attention --[top-center: Overview]-->  Overview  (scroll position restored)
```
Co-primary. Returning restores the prior pane's scroll (`_scrollMem`).

## W2 — Render the heatmap (D057/D060/D061)
```
renderHeat():
  model = heatModel()               // 21 AttentionCells + openTotal
  if openTotal == 0:                // D061
      hide grid, show #heatClear (all-clear)
  else:
      for each artifact row:
        for each dimension:
          cell = _cellFor(art, dim)
          if cell.level == l0:  render inert neutral cell (no click/role/tab)
          else:                 render colored cell (count + mini sev + multi pip),
                                clickable → openFindingsFor(art, dim)
```
Severity color (l1–l3) is applied **only** to non-empty cells (D060).

## W3 — Cell → Issues routing (D058)
```
click cell (art, dim)  ->  openFindingsFor(art, dim)
    ids = open issues in (art, dim)
    if ids.length == 1  ->  openIssue(ids[0])                 // light issue panel
    else                ->  openScopedIssues({art, dim})      // scoped list, BOTH filters lit

click row header (art) ->  openFindingsForArtifact(art)  ->  1 match? openIssue : scoped {art, dim:null}
click field card (dim) ->  openFindingsDim(dim)          ->  1 match? openIssue : scoped {art:null, dim}
```

### W3a — Scoped Issues list (D058 seam)
```
openScopedIssues({art, dim})
  -> renderScoped(): lit chips (art / dim) + seam note + scannable list
  -> click a row  -> openIssueFromScope(id) -> openIssue(id)  (scoped list stays underneath)
  -> close issue  -> returns to the scoped list
  -> clear a chip -> renderScoped() (re-scope); clear both -> closeScoped()
  -> "Back to map" -> closeScoped()
```
Full grouping/triage/resolved-tab = **Slice 6** (not built here).

## W4 — Field view toggle (D059)
```
mview('heat')   -> heatmap visible (primary), legend visible, field hidden
mview('field')  -> field cards visible (secondary), heatmap + legend hidden
(if openTotal == 0 and view == heat: all-clear shown instead of grid)
```

## W5 — Resolve an issue → live map update (inherited D042, reflected on the map)
```
open issue -> answer clarification -> simulate reanalysis -> _istatus[id]='resolved'
  -> renderHeat() + renderDims() + updateIssueCounts() + (renderScoped() if open)
  -> the cell dims / count drops; Feasibility shifts if the critical Resources issue closed
```

## W6 — All-clear demo (D061)
```
"Sim all-clear" (phase bar) -> resolve all open issues (backup kept)
  -> renderHeat(): openTotal==0 -> #heatClear shown
  -> toggle off -> restore statuses -> grid returns
```

## Non-goals in this workflow
- No artifact editing (Slice 5). No full Issues management (Slice 6). No timeline (Slice 7). No reanalysis beyond the existing simulated clarification loop.
