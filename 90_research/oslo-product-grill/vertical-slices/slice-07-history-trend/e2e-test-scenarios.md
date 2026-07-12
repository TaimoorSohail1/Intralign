# Slice 7 — History & Confidence Trend · E2E Test Scenarios

Cumulative Slices 1–7. Manual walkthroughs on the single `prototype.html`. Enter from an analyzed project (activate → sample/ingest → orientation). ≤20 scenarios.

1. **History nav opens the real surface.** Click the sidebar **History (◔)** → a real **History & timeline** pane opens (breadcrumb "History"); it is **not** the old seam ("arrives in Slice 7") and not the Attention map. The OSLO chat rail stays visible.
2. **Header + read-only note.** The header reads **"History & timeline · append-only · prior states retained"** (ⓘ hover); a **"Read-only · viewing history changes nothing"** note sits at the foot.
3. **"Understanding over runs" trend renders.** At the top, a sparkline titled **"Understanding over runs — rises or falls with the read"** shows point(s) with band labels; the line is neutral-colored (not red/amber/green).
4. **First-run minimal state (D100).** Open History before Extended Analysis completes → the trend shows a single **Initial** point and a minimal card: *"Your history starts here … More appears as your plan evolves."*
5. **Extended Analysis appends live (D096).** Let Extended Analysis complete → open History → new rows appear newest-first: **Extended Analysis complete** (current), **7 plan-artifact versions retained (v1)**, **6 issues detected**; the minimal card is gone.
6. **Trend rises or falls with cause (D097).** After Extended, the trend has an **Extended** point with a ▲/▼ direction arrow; hover a point → a cause line (e.g. "deeper analysis firmed the read (Feasibility rose Very Low → Low)"); the ⓘ explains a fall usually means it found something real.
7. **current vs prior labels.** The latest analysis run reads **current**; retained versions read **prior**; both tags are visible and neither row was overwritten.
8. **Apply a fix appends events (D096).** Open ISS-01 (critical · Resources) → **Apply this fix** → open History → **Applied OSLO's fix** and a **Resources updated (vN)** row have appeared; shortly a **"…— Resolved"** lifecycle row appears; a trend **After your fix** point is added.
9. **Answer a clarification appends an event.** Open ISS-02 → answer its clarification → open History → **Clarification answered — …** appears, then a **Resolved** row on the update.
10. **Select a resolution path appends an event.** In an issue, select a resolution path (without applying) → History shows **Resolution path selected — …** (Open → Addressed).
11. **Edit an artifact → version lineage (D099).** Edit any plan artifact (type, pause) → open History → a **"{Artifact} updated (vN)"** row has appended.
12. **View a prior version is read-only (D099).** Click a version row's **"view snapshot →"** → a **read-only toast** appears ("prior version · read-only — prior states retained, never overwritten; viewing changes nothing"); nothing is edited.
13. **Version row keyboard-operable.** Tab to a version row (visible focus ring) → press **Enter** → the same read-only note shows.
14. **Read-only: viewing changes nothing (D098g).** Note the row count → navigate Overview → back to History → the row set is unchanged; no assessment moved.
15. **Last-good on Extended failure (D098g).** Arm the "Sim Extended-Analysis fail" trigger, let Extended run → History appends **"Extended Analysis couldn't complete — showing last-good"**; the trend does not move; the confidence pill still shows the last-good read.
16. **Retry recovers.** From the OSLO chat failure message, click **Retry** → Extended completes → History appends the Extended run (the failed and recovered rows both remain — append-only).
17. **Overview trend row kept (D097).** On the Overview, the quiet confidence-trend row still renders once Extended supersedes — it was not removed by Slice 7.
18. **No "reanalysis" wording (D092).** Scan the History pane and hovers — user-facing copy says "analysis update"/"analysis run", never "reanalysis".
19. **Pointers route to the real pane.** From the Overview **Timeline →** and from an Issue-panel **Open full timeline →** → both open the real History pane (no seam modal, no "(Slice 7)" tail).
20. **No regressions.** Overview, Attention map, full artifact editor, Issues surface + Panel, command palette (⌘/Ctrl+K → GO TO History works), chat, tour, phase bar, and the issue flyout all still work; **0 console errors**.
