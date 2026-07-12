# Slice 7 History & Trend — Critical Analysis & Refinements
Date: 2026-07-09 · Scope: the History/timeline pane + "Understanding over runs" trend in `slice-07-history-trend/prototype.html` (prototype, illustrative). Severity: **S1** blocks · **S2** meaningful · **S3** polish. "Deferred" = later-slice owner.

## What works well (baseline)
Append-only, read-only, "prior states never overwritten," last-good preserved on a failed run — all on-doctrine and trust-building. It grows live (applying a fix, answering a clarification, editing an artifact, completing Extended Analysis all append events), has honest current/prior labels, a first-run minimal state, version snapshots, and a direction-only trend whose fall-meaning is explained on hover. Good foundation.

## S2 — Meaningful (highest UX leverage)

1. **Internal event-type identifiers leak into the UI.** Each timeline row prints the raw internal `type` string in monospace — `analysis_run`, `issue_lifecycle`, `artifact_version`, `selected_path`, `last_good`. This is a developer artifact showing users backend enum values. Remove it, or replace it with a human category label ("Analysis run", "Issue update", "Version", "Your decision"). *(Concrete bug, low effort.)*

2. **No filtering by event type.** The timeline is one flat stream of everything. As it grows (many runs, versions, lifecycle changes, decisions), users can't isolate "just analysis runs," "just issue changes," "just my edits/decisions," or "just versions." Add filter chips (All · Analysis · Issues · Versions · Your decisions) with an honest "N hidden" — mirroring the Issues surface pattern already in the app.

3. **No time/run grouping.** Events are a flat list with relative stamps ("now − 2m"). For a real audit trail this gets hard to scan. Group by **analysis run** (each run and everything it caused, collapsible) and/or by **day** (Today / Yesterday / date). Run-grouping especially tells the core story: "this run → these issues opened/closed, confidence moved this way."

4. **Trend and timeline are disconnected.** The "Understanding over runs" sparkline and the event list don't talk to each other. Clicking a trend point should scroll to / highlight that run in the timeline; and each analysis-run event should show the confidence band it produced. Linking them turns two separate widgets into one coherent "how did my understanding change, and why" narrative — the whole point of this surface.

5. **No per-run "what changed" summary.** A run entry says "Extended Analysis complete" with a prose detail, but not a scannable delta: *+2 issues · 1 resolved · Feasibility Very Low → Low · stage → Expanded · confidence ▲.* Structured deltas per run make the timeline genuinely useful for "what did that change do."

6. **Version lineage is shallow.** Version rows open a read-only *toast*, not an actual prior-version view or a diff, and there's no restore. Users can't see *what* changed between v2 and v3 or roll back. (Ties to the editor's undo/version gap flagged in the Slice-5 analysis — the underlying versioning model is the shared dependency.)

## S3 — Polish

7. **Relative timestamps only.** "now − 2m" with no absolute date/time on hover — fine illustratively, but a real audit trail needs real timestamps (hover for the exact time).

8. **No search within history.** For a long timeline there's no "find when issue X was resolved." The command palette searches views/issues/artifacts but not history events — extending it (or an in-pane find) would help.

9. **"current / prior" tag semantics are noisy.** Several events carry a "current" tag, but for point-in-time events that reads oddly. Consider marking only the current *state* (the latest run = the read you're on) vs history, rather than tagging many individual events "current."

10. **Accessibility & scan-ability.** Use list semantics (role=list/listitem); drop the monospace type tag for screen readers (see #1); ensure the trend sparkline has a text alternative describing direction per run.

11. **Performance/windowing.** Flat `innerHTML` of all events is fine for a prototype; a real build needs windowing/pagination for long histories.

## Deferred (later-slice owners)
- **Export / share the audit trail** — for a governance-oriented product, teams will want to export or share History; → **Slice 9 (Export & Share)**.
- **Threaded comments as timeline events** → **Slice 9 (Collaboration)** (already a known seam).
- **Full version diff / restore** depends on a real versioning model → build-phase + ties to the editor undo work.

## Recommended priority
1. **Remove the internal `type` leak** (#1) — quick, clearly wrong.
2. **Run-grouping + per-run "what changed" deltas** (#3, #5) — the biggest jump in usefulness.
3. **Link the trend to the timeline** (#4) — makes the two halves one story.
4. **Event-type filters** (#2) — scale/scan.
5. Polish: absolute timestamps, history search, current/prior semantics, a11y.

## Note
All are product/UX refinements to the prototype; none changes ratified canon. Version diff/restore and export are also engineering-realization / later-slice items. The append-only + read-only + last-good honesty must be preserved through any of these changes.
