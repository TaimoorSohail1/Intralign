# Slice 7 — History & Confidence Trend · Workflow

Cumulative Slices 1–7. The flows below assume the user is already in an analyzed project (Slices 1–6 complete). User-facing framing is **"analysis update" / "analysis run"**, never "reanalysis" (D092).

## Entry points into History (D096)
- The persistent sidebar **History (◔)** item (`showView('history')`).
- The Overview **"Timeline →"** pointer.
- The Issue-panel **"Open full timeline →"** pointer.

All three land on the same real `#pane-history` surface (the OSLO chat rail stays visible; breadcrumb → "History").

## Flow A — First-run minimal state (D100)
1. Open **History** right after the Initial Analysis (before Extended completes).
2. The **"Understanding over runs"** trend shows a single Initial point (Moderate).
3. Below it, the minimal card: *"Your history starts here — so far this is just your Initial Analysis. More appears as your plan evolves."*
4. As soon as Extended Analysis completes (or you act on the plan), the card gives way to the full timeline.

## Flow B — Timeline grows as Extended Analysis completes (D096/D097)
1. After Fast Pass, Extended Analysis auto-runs (non-blocking, Slice 2). On completion:
2. The trend appends an **Extended** point (here it **rises** Moderate → Moderate with the cause *"deeper analysis firmed the read; Feasibility rose Very Low → Low"*; a fall would be equally valid and is explained on hover).
3. The timeline appends, newest-first: **Extended Analysis complete** (current) · **7 plan-artifact versions retained (v1)** · **6 issues detected**.
4. Open History → the new rows are already present; **current / prior** tags are shown; nothing was overwritten.

## Flow C — Acting on an issue appends lifecycle + version events (D096)
1. In an Issue Panel, click **Apply this fix** (e.g. ISS-01, critical · Resources).
2. History appends **Applied OSLO's fix** (selected path) and a **Resources updated (vN)** version row immediately; the issue lifecycle shows **Addressed**.
3. On the analysis update, History appends **"Venue Wi-Fi… — Resolved"** (`issue_lifecycle`, current), and — because it was critical — the trend appends an **After your fix** point (direction-only, cause-bound).
4. Alternatively, **answer a clarification** → History appends **Clarification answered**, then a **Resolved** row on the update.
5. Alternatively, **select a resolution path** (without applying) → History appends **Resolution path selected** (Open → Addressed).

## Flow D — Edit a plan artifact → version lineage (D099)
1. Edit any plan artifact in the Slice-5 editor; on autosave commit a **"{Artifact} updated (vN)"** version row appends to History.
2. Open History → click the version row's **"view snapshot →"** (or focus it and press Enter/Space).
3. A **read-only toast** appears: *"…prior version · read-only — prior states are retained, never overwritten; viewing changes nothing."* No edit occurs.

## Flow E — Read-only / last-good honesty (D098g)
1. Navigate History → Overview → History again: the row set is **unchanged** (viewing changed nothing).
2. Arm the Extended-Analysis-fail demo trigger, then let Extended run: History appends **"Extended Analysis couldn't complete — showing last-good"**; the trend does **not** move; the last-good read is preserved. Retry (from OSLO chat) recovers and appends the completed Extended run.

## Non-goals (seams)
- **Threaded comments as timeline events** are **not** built (Slice 9) — a seam is left; History reflects lifecycle / analysis / version / clarification events only.
- Real timestamps, real confidence magnitudes, and a full version diff are owner-TBD / later — the prototype uses illustrative values and a labeled read-only snapshot note.
