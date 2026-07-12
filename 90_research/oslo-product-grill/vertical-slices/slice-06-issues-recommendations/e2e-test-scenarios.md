# Slice 6 — Issues & Recommendations · E2E Test Scenarios

Cumulative Slices 1–6. Manual walkthroughs on the single `prototype.html`. Enter from an analyzed project (activate → sample/ingest → orientation).

1. **Issues view reachable.** Top-center switch shows Overview · Attention · **Issues** · Artifacts. Click Issues → list renders; badge shows the open count (6).
2. **Group toggle.** Toggle **By severity** → triage strip (Critical/Moderate/Warning) + severity groups; toggle back **By dimension** → Feasibility/Clarity/Alignment groups.
3. **Artifact filter labeled "Artifact".** The first filter row reads **Artifact** (not "Section"); picking "Resources" shows only Resources issues; count/header update.
4. **Dimension + Severity filters + hidden count.** Filter Dimension=Clarity, Severity=Warning → list narrows; footer shows "N hidden by filters · clear"; click **clear** → full list returns.
5. **None-under-lens empty state.** Filter to a combination with no matches (e.g. Artifact=Intent) → "Nothing under this lens · Clear filters".
6. **Card anatomy.** Each card shows title + severity chip + "Artifact · Dimension" + lifecycle pill (Open); clarification cards show a `❓ clarification` flag.
7. **Open full panel.** Click a card → panel shows Header (lifecycle Open lit) → Why → Evidence → What this weakens → Recommendations → History → reanalysis note.
8. **Evidence collapsible.** Click the Evidence header → sources expand/collapse; operable via keyboard (Enter/Space).
9. **Recommendations only inside the issue.** There is no standalone recommendations page; OSLO Recommended + resolution paths appear only in the panel.
10. **Select a resolution path.** Click a path → it becomes **Selected Path = Confirmed by you**; the lifecycle advances to **Addressed**; a "Selected Path" banner appears.
11. **Apply this fix → reanalysis → resolved.** Open ISS-01 (critical, Resources) → **Apply this fix** → "Re-analyzing…" → lifecycle **Addressed** then **Resolved**; the "Resolved by reanalysis" banner shows.
12. **No manual resolve.** Confirm there is no button that directly sets Resolved — resolution only follows the "Re-analyzing…" step.
13. **Confidence direction-only.** After resolving ISS-01, the confidence signal moves with a named cause (Feasibility) and **no fabricated number**; the Overview counts update (open ↓, resolved ↑).
14. **Status reflected everywhere.** After resolving, the issue drops off the Attention map cell, the artifact badge decrements, and the Issues badge/open count decrement.
15. **Resolved filter.** Set Status=Resolved → the resolved issue appears; Status=Open hides it again.
16. **Clarification loop.** Open ISS-02 (has clarification) → type an answer → Submit & re-analyze → the issue closes (Resolved); the clarification block is gone.
17. **Attention cell routing graduated.** From the Attention map, click a cell with one active issue → its full panel opens; click a cell/row with several → the **Issues pane opens scoped** (Artifact + Dimension filters lit).
18. **Annotation + Overview + chat entry.** An inline artifact annotation's "Open issue →", the Overview "Start here" top issue, and a chat issue link all open the same full panel.
19. **Not-yet-analyzed / Unavailable states.** Use the prototype-preview control under the list → the "Not yet analyzed" and "Issues temporarily unavailable (not an all-clear)" states render; **reset** returns to the live list.
20. **No regression (Slices 1–5).** Activation, four-method intake, Fast Pass ≈30s, confidence-led Overview + pill/popover, Attention heatmap, chat + notices, feature tour, and the full Artifact Workspace (editing, table row ops, undo/redo, weakness stepper, find/replace) all still work.
