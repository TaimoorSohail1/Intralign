# Slice 4 — Attention Map (MRI) · Product Data

Client-side only (D016): **no DB, no API, no server.** All state is in-memory JS + `localStorage` flags (inherited from Slices 1–3). Slice 4 adds **derived** view-models over the existing issue set — it introduces no new persisted store.

## Inherited data (unchanged)
- `PLAN_SECTIONS` — the 7 plan artifacts (id, grp, name, basis Derived/Attested, reliability, body).
- `ISSUES` — the issue set (title, sev, dim, sec, status, why, evidence, clarification, fixes). User-facing "Issues"; internal object = Finding (D017).
- `_istatus` — mutable per-issue status (`open` | `resolved`).
- `READ` — the ConfidenceReading (index, band, reliability basis, stage) — untouched by Slice 4.
- `localStorage` keys (`oslo-s1-*`): `account`, `staySignedIn`, `orientSeen`, `tourSeen`, `phase`. No new keys added.

## NEW derived models (Slice 4 — computed, not stored)

### AttentionCell (D057)
The atomic unit of the heatmap. One per `{artifact × dimension}` = 7 × 3 = **21 cells**. Derived live via `_cellFor(art, dim)`:

| Field | Type | Meaning |
|---|---|---|
| `art` | string | plan-artifact id (Intent … Resources) |
| `dim` | enum | `Clarity` · `Alignment` · `Feasibility` |
| `level` | enum | `l0` (none) · `l1` (warning) · `l2` (moderate) · `l3` (critical) — the **attention-severity** shade |
| `count` | int | number of **open** issues in this bucket |
| `sev` | enum\|null | most-severe open issue's severity (drives `level`); null when empty |
| `ids` | string[] | the open issue ids in this bucket |

`level` is computed from `sev` (`critical→l3`, `moderate→l2`, `warning→l1`, none→`l0`). **Severity is the only thing that colors a cell (D060).**

### HeatModel (D057/D061)
`heatModel()` → `{ cells: AttentionCell[21], openTotal: int }`. `openTotal` sums every cell's `count`; `openTotal === 0` triggers the map-wide **all-clear** state (D061).

### FieldModel (D059)
The secondary field view derives, per dimension, a neutral maturity level + bar width + a live **open-issue count** (`ISSUES` filtered by `dim` + status `open`). Feasibility is the limiter and shifts Very Low → Low once Extended Analysis supersedes (mirrors the Overview CAF read; **neutral**, never severity-colored).

### Scope (D058)
`_scope = { art, dim }` — the transient filter state of the scoped Issues list. `_scopeMatches()` = open issues where (`!art || sec===art`) AND (`!dim || dim===dim`), sorted by severity. Cleared/closed on navigation. Not persisted.

### View context (D062)
`_scrollMem = { overview, attention }` — remembered scroll offsets so returning to a pane restores prior context. In-memory only.

## Illustrative cell distribution (from the DevNorth fake issue set)
| Cell (artifact × dimension) | Open issues | Level | Route |
|---|---|---|---|
| Resources × Feasibility | ISS-01 (critical), ISS-03 (moderate) | `l3` | **multi → scoped list** (both filters lit) |
| Requirements × Clarity | ISS-02 (moderate) | `l2` | single → issue panel |
| Schedule × Feasibility | ISS-04 (moderate) | `l2` | single → issue panel |
| WBS × Alignment | ISS-05 (moderate) | `l2` | single → issue panel |
| Context × Clarity | ISS-06 (warning) | `l1` | single → issue panel |
| all other 16 cells | none | `l0` | inert (non-clickable) |

All values are **fake/illustrative** (D016). Resolving the critical Resources clarification drops ISS-01, dimming that cell and shifting Feasibility; resolving everything reaches the all-clear state.
