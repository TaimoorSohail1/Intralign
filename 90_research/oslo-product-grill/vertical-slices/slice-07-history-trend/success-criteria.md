# Slice 7 — History & Confidence Trend · Success Criteria

Cumulative Slices 1–7. A build passes Slice 7 when all below hold and Slices 1–6 do not regress.

## D096 — Append-only History timeline
- [ ] The sidebar **History (◔)** item opens a **real** center pane (`#pane-history`) — the Slice-6 seam ("arrives in Slice 7") is **gone**.
- [ ] The pane shows a **chronological, newest-first** event list with plain labels, illustrative timestamps, and **current / prior** tags.
- [ ] Event types covered: **analysis runs** (Initial / Extended), **plan-artifact versions (vN)**, **issue lifecycle** (Open → Addressed → Resolved), **selected resolution paths**, **clarifications answered**.
- [ ] **Nothing is overwritten** — the list only grows (append-only).
- [ ] It grows **live** in-session: applying a fix, answering a clarification, editing/versioning an artifact, and completing Extended Analysis each append an event.
- [ ] The Overview **Timeline →** and Issue-panel **Open full timeline →** pointers route to this real pane (not a seam modal).

## D097 — "Understanding over runs" trend
- [ ] A sparkline titled **"Understanding over runs"** sits at the **top** of the History pane.
- [ ] Each point is **band-qualified** (5-band) and **cause-bound** (reason on hover).
- [ ] The line can **rise OR fall**; a ⓘ hover explains a fall usually means a deeper analysis found something real, not a worse project.
- [ ] Direction is shown (▲/▼) **without a fabricated magnitude** in the UI; the line is drawn in **neutral** maturity color (not severity color).
- [ ] The Overview quiet confidence-trend row (`#ov-trend`) is **kept** (unchanged).

## D098g — Last-good + read-only
- [ ] History is **read-only**: viewing any prior state never edits the plan or changes the assessment; a **"viewing history changes nothing"** note is present.
- [ ] Re-visiting the pane leaves the row set unchanged.
- [ ] An Extended-Analysis failure appends a **"showing last-good"** entry; the last-good read is preserved and the trend does not move.

## D099 — Version lineage
- [ ] Artifact **version (vN)** entries are append-only and appear in the timeline.
- [ ] Clicking a version entry shows a **read-only** snapshot note (toast) — labeled read-only, no edit; keyboard-operable.

## D100 — First-run state
- [ ] With only the initial analysis, History shows a **minimal state** with **"more appears as your plan evolves."**
- [ ] Once Extended Analysis completes or the user acts, the full timeline replaces the minimal card.

## Cross-cutting / no-regression
- [ ] Advisory-only framing intact; **"analysis update"/"analysis run"**, never "reanalysis", in user-facing copy (D092).
- [ ] "Issues" (not "Findings"); Clarity · Alignment · Feasibility; From OSLO / Confirmed by you; 5-band scale; **severity color only** on issue severity (D003) — trend/History chrome neutral.
- [ ] Dark default + WCAG 2.1 AA: timeline keyboard-navigable; version rows focusable with a visible focus ring; ⓘ hovers are the single home for honesty invariants.
- [ ] No threaded comments (Slice 9 seam left).
- [ ] All prior slices intact: activation funnel, intake, Fast Pass, confidence-led Overview, confidence pill + popover, Attention map, full artifact editor, full Issues surface + Panel, persistent sidebar + top bar + command palette, chat, tour, phase bar, issue flyout.

## Build integrity
- [ ] Extracted `<script>` passes `node --check`.
- [ ] jsdom structural parse: `body.children.length > 0`; `#pane-history` holds the real timeline (not the seam); trend sparkline present.
- [ ] jsdom runtime: History opens live; trend renders with rise/fall; apply-fix / answer-clarification / Extended-complete append events; viewing is read-only; first-run minimal state reachable; **0 console errors**.
