# Slice 7 — History & Confidence Trend · Product Detail

Cumulative Slices 1–7. This document specifies the behavior added in Slice 7. Inherited behavior from Slices 1–6 is unchanged.

## Scope
Replace the Slice-6 History **seam** (`#pane-history`, "arrives in Slice 7") with the **real** History & timeline surface: (1) an **append-only event timeline**, (2) an **"Understanding over runs" confidence trend**, (3) **read-only / last-good** honesty, (4) **artifact version lineage**, and (5) a **first-run minimal state**. Client-side only (D016): single HTML, plain JS, `localStorage`, fake data, simulated AI.

## Capabilities

### C7.1 — Append-only History timeline (D096)
- Center pane `#pane-history` (OSLO chat rail persists), reached from the sidebar **History (◔)** item (`showView('history')`), the Overview **Timeline →** pointer, and the Issue-panel **Open full timeline →** pointer (both via `openHistorySeam()`, now routing to the real pane).
- Model = `HISTORY` array, **append-only**: new events are `unshift`-ed (newest-first). Nothing is mutated or removed.
- Rendered by `renderHistory()` on pane entry and on every live append. Each row: icon (`_histicon[type]`) + label + optional detail + illustrative timestamp + a **current / prior** tag.
- **Event types** (`type` key): `analysis_run`, `reanalysis_run` (Extended), `artifact_version`, `issue_lifecycle`, `selected_path`, `clarification`, `last_good`.
- **Live appends** (`pushHistory(type,label,{d,cur,ver})`):
  - **Extended Analysis completes** (`deepComplete`) → adds the Extended run (current), the retained 7 plan-artifact versions (v1), and the 6 detected issues — **exactly once** (`_deepHistDone` guard).
  - **Apply this fix** (`applyFix`) → adds *Applied OSLO's fix* (selected path), a tied-artifact **version bump (vN)**, then on the analysis update a **`issue_lifecycle` Resolved** row (current).
  - **Select a resolution path** (`selectPath`) → adds *Resolution path selected* (+ Open→Addressed note).
  - **Answer a clarification** (`answerClarification`) → adds *Clarification answered*, then a **Resolved** row on the update.
  - **Edit a plan artifact** (`commitArtEdit`) → adds an **`artifact_version` (vN)** row on autosave commit.
- **Read-only:** rows are non-editable; rendering/viewing changes no assessment (see C7.3).

### C7.2 — "Understanding over runs" trend (D097)
- Model = `TREND` array of run points `{run, index, band, cause}`; seeded with just the **Initial** run (so the first-run state is honest).
- Rendered by `renderHistTrend()` into `#hist-trend` at the **top of the History pane**: a titled sparkline (`Understanding over runs — rises or falls with the read`) drawn as a **neutral** `var(--conf-medium)` polyline + point circles.
- Each point is **band-qualified** (5-band) and **cause-bound** (SVG `<title>` + the per-run caption's `cause`). Direction shown as ▲ (success tint) / ▼ (warning tint) — **direction-only**, no fabricated magnitude in the UI (illustrative indices live in code only, used solely to draw the line).
- The line **can rise OR fall**; a single ⓘ hover states a fall after a deeper analysis usually means it found something real, not a worse project.
- `pushTrend(run,index,band,cause)` appends a run point (from `deepComplete`, and from a critical-issue resolution). Re-renders live if the pane is open.
- The **Overview `#ov-trend` quiet trend row is kept** (D097) — unchanged.

### C7.3 — Read-only + last-good honesty (D098g)
- The pane foot shows **"Read-only · viewing history changes nothing"** with a ⓘ hover.
- No history interaction mutates `_istatus`, `PLAN_SECTIONS`, `READ`, `TREND`, or any assessment; re-visiting the pane leaves the row set unchanged.
- **Last-good:** on an Extended-Analysis failure (`deepFail`), a `last_good` row is appended ("couldn't complete — showing last-good"); the last-good understanding is preserved and the trend does **not** move.

### C7.4 — Version lineage (D099)
- `artifact_version` rows carry a `ver` payload and render as **clickable** (`.hrow.clickable`) with a **"view snapshot →"** affordance.
- Clicking (or Enter/Space) calls `histVersionNote(evId)` → a **read-only toast** (`_stubToast`): *"…prior version · read-only. Prior states are retained, never overwritten; viewing changes nothing."* Prototype-grade labeled read-only view (no full diff).

### C7.5 — First-run minimal state (D100)
- `#hist-first` shows when only the Initial Analysis exists (`HISTORY.length ≤ 1 && TREND.length ≤ 1`): *"Your history starts here … More appears as your plan evolves."*
- Once Extended Analysis completes or the user acts, the minimal card hides and the full timeline renders.

## Constraints honored
- Advisory-only (D001); assessment changes only via an analysis update (D006); **user-facing "analysis update"/"analysis run", never "reanalysis"** (D092).
- Severity color only on issue severity (D003) — the trend line and all History chrome are **neutral maturity**.
- 5-band vocabulary (D020); confidence is understanding maturity, not health (D002); direction-only movement (D056).
- Dark default + WCAG 2.1 AA (D015): keyboard-navigable timeline; version rows focusable; ⓘ hovers are the single home for the honesty invariants.
- **Threaded comments deferred to Slice 9** — seam only; History reflects lifecycle / analysis / version / clarification events.
