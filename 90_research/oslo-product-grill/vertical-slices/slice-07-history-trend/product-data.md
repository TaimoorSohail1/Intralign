# Slice 7 — History & Confidence Trend · Product Data

Cumulative Slices 1–7. All data is fake/illustrative and lives in memory + `localStorage` (D016). **No database, API, or server.** Slice 7 adds two append-only client structures — `HISTORY` and `TREND`.

## HistoryEvent (`HISTORY[]`, D096)

An **append-only** list of everything that has shaped OSLO's read. New events are `unshift`-ed (newest-first); existing events are **never mutated or removed**.

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable event id, e.g. `H0`, `H1` (`'H'+(++_hEventSeq)`). |
| `ts` | string | **Illustrative** timestamp label (e.g. `now − 2m`, `just now`). Not a real clock; direction/order matters, not the value. |
| `type` | enum | Event type — one of `analysis_run` \| `reanalysis_run` \| `artifact_version` \| `issue_lifecycle` \| `selected_path` \| `clarification` \| `last_good`. Drives the row icon (`_histicon`). |
| `lab` | string | Plain event label (row title). |
| `d` | string? | Optional detail line. |
| `cur` | bool | **current** (`true`) vs **prior** (`false`) tag. The latest analysis run and lifecycle-resolved events read *current*; superseded states read *prior*. Append-only — a prior event is never rewritten. |
| `ver` | string? | Present on `artifact_version` events — the read-only snapshot label shown by `histVersionNote()` (e.g. `Resources (v3)`). Enables version-lineage view (D099). |

### `type` → user meaning (and icon)
| `type` | Icon | Appears when |
|---|---|---|
| `analysis_run` | ✦ | Initial Analysis completes. |
| `reanalysis_run` | ↻ | Extended Analysis completes (supersedes the provisional orientation). |
| `artifact_version` | ▤ | A plan artifact is edited/versioned, or a fix is drafted into it (vN retained). **Clickable → read-only snapshot.** |
| `issue_lifecycle` | ◆ | An issue moves Open → Addressed → Resolved (Resolved only via an analysis update). |
| `selected_path` | ✓ | A resolution path is selected, or *Apply this fix* is used. |
| `clarification` | ? | A clarification question is answered. |
| `last_good` | ! | Extended Analysis couldn't complete — showing last-good (D098g). |

### Seed
```
HISTORY = [ { id:'H0', ts:'now − 2m', type:'analysis_run',
              lab:'Initial Analysis complete',
              d:'7 plan artifacts drafted · Clarity · Alignment · Feasibility assessed · Confidence Moderate · 6 issues detected',
              cur:true } ]
```
Seeded with **only** the Initial Analysis so the first-run minimal state (D100) is the honest default.

## TrendPoint (`TREND[]`, D097)

One point per completed analysis **run**. Append-only.

| Field | Type | Meaning |
|---|---|---|
| `run` | string | Run label (e.g. `Initial`, `Extended`, `After your fix`). |
| `index` | number | **Illustrative** 0–100 index used **only to draw the polyline height**. Never shown bare in the UI (direction-only, D056); real magnitudes owner-TBD. |
| `band` | enum | 5-band label — Very Low · Low · Moderate · High · Very High (D020). Shown in the caption. |
| `cause` | string | Plain, cause-bound reason (SVG `<title>` + caption). The line rises OR falls; a fall usually means deeper analysis found something real (D097). |

### Seed
```
TREND = [ { run:'Initial', index:58, band:'Moderate',
            cause:'firmed the first read from your inputs' } ]
```

## Append-only rules
- **Never overwrite / never delete.** `pushHistory` and `pushTrend` only add. A "prior" state stays exactly as recorded.
- **current vs prior** is a per-event tag, not an edit — the newest analysis run / resolved event is `cur:true`; superseded rows keep their original tag.
- **Read-only** — no render or view path mutates any assessment structure (`_istatus`, `PLAN_SECTIONS`, `READ`) or the arrays themselves.
- **Idempotent Extended seeding** — the Extended-run bundle (run + versions + detected issues) is appended once (`_deepHistDone` guard), so a retry after a real completion never duplicates it.

## Persistence
- `HISTORY` / `TREND` are in-memory per session (illustrative). Artifact **version numbers** are the one History-adjacent value persisted, via the existing editor keys: `LS.get(_artKey(name)+'-ver', 2)` bumped on each commit / applied fix (Slice 5). No other History state is persisted; **no DB**.

## Relationship to existing data
- **Issues** (`ISSUES` / `_istatus`, Slice 6) — lifecycle transitions emit `issue_lifecycle` / `selected_path` / `clarification` history events; History reads them, never writes them back.
- **Plan artifacts** (`PLAN_SECTIONS`, Slice 5) — edits/applied fixes emit `artifact_version` events; the `ver` label reflects the editor's version counter.
- **Confidence read** (`READ`, `ANALYSIS_STATE`, Slice 3) — analysis-run completions emit `analysis_run` / `reanalysis_run` history + `TREND` points; a failure emits `last_good` and leaves the read untouched.
