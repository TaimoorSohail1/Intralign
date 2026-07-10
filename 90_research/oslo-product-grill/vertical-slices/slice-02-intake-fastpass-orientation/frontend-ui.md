# Slice 2 — Intake & Fast-Pass Orientation · Frontend UI

Single openable HTML, theme inherited 1:1 from `oslo_r1_experience_mockup_v4.html` and Slice 1 (D015/D016). Same semantic token set; dark default, light overrides same names. All new components below reuse existing tokens — no new colors.

## Layout regions (app shell) [Rev 2]
- **`#app`** — 2-column grid: main body (col 1) + **persistent OSLO chat rail** `.chatp` (col 2, collapsible via `.chat-collapsed`). Topbar spans both columns.
- **Topbar** — brand ▸ project crumb ▸ **top-center view switch** `.vswitch` (Overview · Attention, co-primary — D038/NAV-C3) ▸ spacer ▸ confidence pill ▸ account avatar.
- **Body** — two panes (`.pane`), one active at a time: `#pane-overview`, `#pane-attention`.
- **Chat rail** `.chatp` — `.chat-h` header, `.chat-scroll` (`.cmsg` messages; `.cmsg.done` = completion notices), `.chat-foot` composer. Re-open button `.chat-toggle` when collapsed.
- **Overlays** — analyzing, orientation, **feature tour** (`.tourmask`/`.tourtip`), light issue panel (`#issueScrim`), GA save-bar/signup (inherited), account menu (inherited), advisory footer (inherited).

## Overview components (confidence-led, DL-096 / D046) [Rev 2]
Sections are EXACTLY **Confidence → Start here → Progress → More**. Completion notices are **not** here (they render in the chat rail, D043).
| Component | Class | Notes |
|---|---|---|
| Confidence hero | `.card.hero` + `.conf-focus` | Focal `.idx` 52px + `/100`; meaning line; band + **reliability inline qualifier** (D046). No ring/green box/pill; no standalone Reliability card. |
| Analysis-state chip | `.ustate` (`.prov` / `.cur`) | Provisional (amber) ↔ Current (green) — D040 |
| CAF maturity bars | `.cafrow` (`.lim` on lowest) | "What's driving it"; neutral ramp; 5-band words; hover `.caftip`; "the limit". Severity color never here (D003). |
| Why / trend | `#whybox`, `.conf-trend-row` | Why disclosure carries the **reliability detail** (D046); quiet trend sparkline shown once superseded ("↗ N since your change · from X") |
| Summary counts | `.conf-foot` | "N issues open · M resolved" — **counts only** (D045); Why + Timeline links |
| Start here | `.focus` → `.focus-lead` + `.focus-item` | Top open issue + "Then:" + "See all N"; severity accent = left border only (D003). Light clarification pointer `.clar-prompt` → tied Issue (D042). |
| Progress | `.prog-grid` / `.prog-col` / `.prog-n` / `.prog-trk` | **Pixel-matched to canonical v4 `.pv-*` ledger** (`renderLedger()`), D047 + Rev 4. **Header:** uppercase "Progress" (`.ch h3`) + an `.info` icon (data-tip "Concrete, countable progress…"); the "since the last analysis" subtitle is removed. **Grid:** `grid-template-columns:1fr 1fr; gap:18px 44px; align-items:start`, collapsing to one column ≤640px (mirrors `.pv-2col`). **Left col — stats stack number-over-label** (`.prog-lead`/`.prog-sub` are `flex-direction:column; gap:3px`, mirroring `.pv-stat`). Both stat numbers share **one 26px mono rule** (`.prog-n`, mirroring `.pv-n`) — equal size, no inline override; resolved (`#pg-resolved`) turns primary-light when >0, critical (`#pg-crit`) carries `.danger` (red) when >0. Labels 11.5px/subtle (`.pv-l`). Left label "issues resolved · {open} open · view →" (view link `#pg-viewlink` shows only when resolved>0, routes to Attention); critical row "critical issues open" appends " · all clear" when 0 open (`#pg-crit-l`). **Right col, this order:** (1) "Dependencies confirmed" {n} / 3 + bar; (2) "Plan artifacts read" 7 / 7 + bar (plain-language "read", D012); meter labels 12.5px/muted (`.pv-mh`), 14px gap between meters (`.prog-bar-row+.prog-bar-row`). **Bar track** `--surface-3` with `--conf-medium` fill (mirrors `.pv-bar`). **No analysis-state line** — the removed `#lg-state`/`#pg-state` line is gone (not in v4); Extended-Analysis status surfaces via the OSLO chat and the Confidence provisional↔current chip (D043). |
| More (collapsible) | `.explore` / `.osec` | Project summary + 7 plan artifacts (`.plan-sec` with `.elabel`) — D035 |

## OSLO chat rail + feature tour (Rev 2 — D043/D044)
| Component | Class / fn | Notes |
|---|---|---|
| Chat rail | `.chatp` / `pushChat()` | Persistent advisor; completion/failure/claim-through notices land here as `.cmsg.done` |
| Fast-pass notice | `postFastPassComplete()` | "Initial Analysis complete in Ns — under the 60-second target" + `.tour-offer` link |
| Deep-pass notice | `postDeepPassComplete()` | "Extended Analysis complete — superseded the provisional orientation" |
| Feature tour | `.tourmask` / `.tourtip` / `startTour()` | Opt-in spotlight coachmarks; 4 Slice-2 surfaces; `tt-step/title/text` + Skip/Back/Next; seen in `localStorage` |
| Rail affordance | `.rail-tour` `#railTour` | small "Take a quick tour" bottom-left; hides once seen |

## Attention Map components (heatmap-primary — D007/D038)
| Component | Class | Notes |
|---|---|---|
| Heatmap grid | `.heat` / `.heat-cell` `l0–l3` | rows = 7 sections (grouped), cols = C/A/F; `l0` calm/neutral, `l1–l3` = warning/moderate/critical severity (D003) |
| Legend | `.heat-legend` | Calm → Needs attention |
| Dimensions (secondary) | `.dimwrap` / `.dimcard` (`.lim`) | CAF bands toggle |
| View filter | `.mfilter` / `.mf` | Heatmap / Dimensions |

## Light Issue panel (Slice-2 minimal — D042/D045; full UI is Slice 6)
`.issuepanel` slide-in: `.ip-top` (severity + title) → `.ip-life` (Open→Addressed→Resolved chips) → Why → `.ip-ev` evidence → `.ip-clar` clarification block (textarea + submit) → `.ip-fixes` suggested fixes → `.ip-resolved` **confirmation** on resolve. Per D045 the resolved-issue confirmation lives **here**, not on the Overview.

## Accessibility (D015)
- `:focus-visible` rings via `--color-focus` (per theme).
- `role="tab"`/`aria-selected` on the view switch; `role="button"`+`tabindex` on non-native clickables (cells, rows, close, clarification triggers); `role="dialog"`+`aria-modal` on the issue panel.
- `prefers-reduced-motion` kills spinner/pulse and caps transitions.
- Severity conveyed by label word + position, not color alone (heat cells carry the count + severity mini-label).

## Inherited from Slice 1 (unchanged)
Phase banner, activation/invite flow, intake composer + 4 start methods, analyzing overlay + trace, strategic-chain orientation, account menu + logout, GA save-to-keep bar + signup modal, advisory footer. All Slice-1 classes and IDs are preserved so no Slice-1 route regresses.

## Demo-only controls (scaffolding, not product chrome)
- Phase preview toggle (Alpha/GA) + Restart — inherited.
- **"Sim Extended-Analysis fail"** — arms the D041 failure path for the next Deep Pass.

## Revision 2 (2026-07-09)
D043 completion notices → OSLO chat rail (`.arrival`/`.deepbar` banners removed); D044 feature tour added; D045 confirmations in the Issue detail (Overview counts only); D046 Overview reconciled to DL-096 (standalone Reliability card removed → inline qualifier + Why disclosure; sections Confidence/Start here/Progress/More). No new colors; all Slice-1 classes/IDs preserved.
