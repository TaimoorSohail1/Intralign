# Slice 8 — Multi-Project Workspace & Awareness · Product Data

Cumulative Slices 1–8. **Client-side only — no database, no backend, no network (D016).** All state is in-memory JS plus `localStorage`. Numbers are **illustrative** (visibility-first). One real project (DevNorth 2026); the rest illustrate the multi-project structure.

## Entity: Project (`PROJECTS[]`)

| Field | Type | Values / notes |
|---|---|---|
| `id` | string | stable key (`devnorth`, `q3mig`, `brand`, `offsite`) |
| `name` | string | display name |
| `ownership` | enum | `Owner` \| `Shared` (rendered *Owned* / *Shared with me*) |
| `analysisStatus` | enum | `current` \| `stale` (stale = edited since its last analysis) |
| `band` | enum | understanding maturity band — `Low` \| `Moderate` \| `High` (neutral maturity, **not** health — D002) |
| `reliability` | enum | `Low` \| `Moderate` \| `High` — qualifies the band (independent of it) |
| `recency` | string | illustrative relative time (e.g. `2h ago`, `edited 20m ago`, `2 months ago`) |
| `openIssues` | number | illustrative open-issue count |
| `artifacts` | number | illustrative artifact count |
| `pinned` | boolean | shown under ★ Pinned |
| `archived` | boolean | shown under Archived; non-destructive |
| `tag` | string | small chip (`sample · event`, `shared`, `marketing`, `event`) |
| `real` | boolean | true only for DevNorth 2026 — the one project that actually enters the shell |

**Seed rows.**
- `devnorth` — Owner · current · Moderate/Moderate · 2h ago · 6 issues · 7 artifacts · pinned · real.
- `q3mig` — Shared · **stale** · Low/Low · edited 20m ago · 3 issues · 5 artifacts.
- `brand` — Owner · current · High/High · 1d ago · 1 issue · 6 artifacts.
- `offsite` — Owner · current · High/Moderate · 2 months ago · **archived**.

Understanding-dot color = neutral maturity ramp via `_bandDot(band)` → `var(--conf-high|medium|low)`. **No cross-project aggregate is ever computed** (D102 honesty note).

## Entity: Notification (`NOTIFS[]`)

| Field | Type | Values / notes |
|---|---|---|
| `cat` | enum | `mention` \| `reply` \| `shared with me` \| `analysis complete` \| `analysis failed` \| `stale` |
| `ic` | string | glyph |
| `l` | string | label (title) |
| `m` | string | source/detail line |
| `tm` | string | illustrative relative time |
| `unread` | boolean | **presentation-only** — toggling changes nothing real (D104) |
| `route` | string | routing target: `history` \| `issues` \| `overview` \| `workspace` \| `artifact:<id>` |

Seed: 6 items, 3 unread (mention, analysis complete, shared-with-me). Unread count feeds the top-bar and Workspace-Home badges (`updateNotifBadges()`), which are **neutral/brand** (D003). `route` never carries an "analyze" action — routing only navigates to an existing surface (D092).

## Settings model (static; visibility-first)

Rendered statically (no persisted values except the theme). Sections: Account · Profile · **Appearance** · Notifications · Workspace · Project defaults · Collaboration · Membership · Subscription · Billing · Integrations. The four commercial areas expose **facts only**: Plan `Free`, Active projects `1 of 1`, Analysis `Initial only`, Payment method `none on file`, Invoices `—`, Connected tools `none`, Membership `Idris = Owner, 1 member`. **No enforcement, no real billing, no writes.**

## Appearance / theme state (D106)

| Key | Store | Values |
|---|---|---|
| `data-theme` | `document.documentElement` attribute | absent = dark (default) · `"light"` = light |
| `oslo-s1-theme` | `localStorage` (via `LS`) | `"dark"` \| `"light"` · absent = follow system |

`initTheme()` at boot: read `LS.theme`; if unset, use `prefers-color-scheme` (dark fallback); apply via `setTheme(t, save=false)`. `matchSystemTheme()` deletes the key and re-derives. A `matchMedia('(prefers-color-scheme: light)')` change listener updates the theme only while no explicit override is stored.

## localStorage keys (namespaced `oslo-s1-*`, via `LS`)

Inherited: `account`, `staySignedIn`, `phase`, `orientSeen`, `tourSeen`, per-artifact `<key>` + `<key>-ver`.
**New in Slice 8:** `theme` (`"dark"` | `"light"`).

## Persistence & lifecycle

- **No DB.** Projects, notifications and settings facts are in-memory illustrative data; the only Slice-8 persisted value is the theme.
- **Non-destructive archive/restore** are illustrative (a confirming toast) — no data is mutated or deleted.
- **read/unread** mutates the in-memory `NOTIFS[]` only (badge display); it is not persisted and changes no assessment.
