# Slice 6 — Issues & Recommendations · Product Data

Cumulative Slices 1–6. All data is fake/illustrative and lives in memory + `localStorage` (D016). No database, API, or server.

## Issue (user-facing "Issue"; internal object = "Finding", D017)

Six real issues are wired (`ISS-01`…`ISS-06`) — the same set the Attention map, Overview and artifact badges already use. Slice 6 extends each record with recommendation, impact, and lifecycle fields.

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable id, e.g. `ISS-01`. |
| `title` | string | Short issue title (card + panel header). |
| `sev` | enum | `critical` \| `moderate` \| `warning`. Drives severity color **only** (D003). |
| `dim` | enum | CAF dimension: `Clarity` \| `Alignment` \| `Feasibility`. |
| `sec` | enum | Artifact key: `Intent`\|`Context`\|`Scope`\|`Requirements`\|`WBS`\|`Schedule`\|`Resources`. Displayed via `dispName` (e.g. `WBS` → "Work breakdown"); user-facing filter labeled **"Artifact"** (D049). |
| `status` | enum | Seed lifecycle: `open` (all seed `open`). |
| `why` | string | "Why this matters" body. |
| `ev` | array | Evidence: `[[source, quote], …]` — traceable to inputs; shown collapsible. |
| `caf` | string | "What this weakens" — the Clarity/Alignment/Feasibility impact narrative. |
| `rec` | string | **OSLO Recommended** action (From OSLO / Derived). |
| `paths` | string[] | **Possible resolution paths** (selectable → Selected Path). |
| `draft` | string? | Optional OSLO-drafted change (present on `ISS-01`, `ISS-02`) enabling "Apply this fix" to draft into the plan. |
| `clar` | object? | Clarification request `{q, hint}` (present on `ISS-01`, `ISS-02`). |

### Mutable runtime state (kept separate from the model)
| Var | Type | Meaning |
|---|---|---|
| `_istatus[id]` | enum | Live lifecycle: `open` \| `addressed` \| `resolved` (D088). Seeded from `status`. |
| `_selpath[id]` | string? | Selected Path: `'rec'` (OSLO Recommended) or `'p<index>'` (a `paths[]` choice) = **Confirmed by you** (D089). |
| `_LIFE` | array | `['open','addressed','resolved']` — lifecycle order. |
| `_lifeword` | map | Display words Open / Addressed / Resolved. |
| `_active(id)` | fn | `_istatus[id] !== 'resolved'` — "active" (open or addressed) governs map/badge/list visibility so counts and routing agree. |

## Filter / group / view state
| Var | Type | Meaning |
|---|---|---|
| `_filt` | object | `{art, dim, sev, status}`. `art`/`dim`/`sev` default `'all'`; `status` default `'active'` (Open). `status` ∈ `active` \| `resolved` \| `all`. |
| `_group` | enum | `'dim'` (By dimension, default) \| `'sev'` (By severity). |
| `_issuesState` | enum | `'ready'` \| `'analyzing'` \| `'unavailable'` — drives the not-yet-analyzed / unavailable empty states (D091). |
| `_DIMORDER` | array | `['Feasibility','Clarity','Alignment']` grouping order. |
| `_SEVORDER` | array | `['critical','moderate','warning']` grouping order. |
| `_ISSARTORDER` | array | The seven artifacts in canonical order for the Artifact filter. |
| `CURVIEW` | enum | Now includes `'issues'` alongside `overview`/`attention`/`artifacts`. |

## Derived / rendered values
- **Hidden count** = `total(status-matched) − shown(after art/dim/sev filters)`, surfaced only when filters are active and hidden > 0.
- **Header count** = shown + status label (`open`/`resolved`/`total`) + `(filtered)` when filters active.
- **Attention badge / Issues badge** = active (non-resolved) count.
- **Confidence move** on resolution is **direction-only** (D056) — no stored magnitude; illustrative CAF/idx nudge only when the critical Resources gap clears.

## Persistence
- The prototype simulates persistence via `localStorage` (activation, account, project, artifact edits/versions from Slice 5). Lifecycle changes are in-memory for the session (reset on reload) — consistent with the prototype boundary (D016). **No DB.**
