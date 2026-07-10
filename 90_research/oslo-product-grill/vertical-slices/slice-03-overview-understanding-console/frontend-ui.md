# Slice 3 — Project Overview & Understanding Console · Frontend / UI

Single openable HTML; theme inherited 1:1 from `oslo_r1_experience_mockup_v4.html`. Dark default + light override on the same tokens (D015); WCAG 2.1 AA (focus-visible rings, keyboard operability, reduced-motion). No framework; plain JS + CSS variables.

## Reused v4 patterns (pixel-matched)
- **`.confpop` / `.cpp-*`** — the confidence popover + CAF/reliability rows (v4 mockup lines 199–207, 1170–1188).
- **`.stagepips`** — the quiet stage marker (v4 line 375–376).
- **`.conf-pill`** — the top-bar pill (inherited); extended with `.cpchev`, `.flagdot`, `.flagged`.

## New / changed UI elements (Slice 3)
| Element | Selector / id | Decision | Notes |
|---|---|---|---|
| Confidence pill (clickable) | `#confpill` (`.conf-pill`) | D050 | `onclick="toggleConfPop"`, `aria-haspopup="dialog"`, chevron + neutral flag dot. |
| Confidence popover | `#confpop` (`.confpop`) | D050 | `role="dialog"`; positioned under the pill; CAF → reliability → flag → CTA. |
| CAF rows (popover) | `.cpp-d` in `#cpp-caf` | D050 | Neutral maturity bars; band words. |
| Reliability basis rows | `#cpp-cov/-evd/-asr` (+`-bar`) | D051 | Coverage · Evidence availability · **How assessable**; High/Moderate/Low. |
| Stage marker | `#ov-stage` (`.stagepips`), `#cpp-stage` | D053 | Quiet; `cursor:help`; tooltip names the three stages. |
| How-calculated | `#howcalc` + `#howcalc-pop` (`.howcalc`) | D054 | Info-glyph pill; hover + click; small explainer popover. |
| False-confidence flag (popover) | `#cpp-flag` (`.cflag`) | D052 | **Neutral** surface (`--surface-3`), info glyph; conditional `.on`. |
| False-confidence flag (card) | `#ov-flag` (`.card-flag`) | D052 | Mirrors the popover flag; neutral. |
| Why box (reliability basis) | `#whybox` / `#why-rel` | D051 | Reliability basis in prose; synced by `syncReliabilityCopy`. |
| Project summary (rich) | `#proj-summary` (`#ps-*`) | D055 | Five-beat narrative in **More**. |
| Trend row (direction-only) | `#ov-trend` / `#ov-trend-lab` | D056 | "Up — deeper analysis firmed up the read"; no magnitude. |
| Phase-bar demo | `#falseConfBtn` | D052 | "Sim false-confidence" toggle (demo scaffolding, not product chrome). |

## Color discipline (D003)
- The false-confidence flag and all confidence/CAF/reliability surfaces use the **neutral** palette (`--subtle`, `--muted`, `--surface-2/3`, neutral maturity ramp `--conf-low/medium/high`). **Severity red/amber/green appears only on issues** (unchanged from Slice 1/2).

## Accessibility
- Pill: `aria-haspopup="dialog"`, `aria-expanded` toggled. Popover: `role="dialog"`, keyboard-reachable button inside. How-calc: `role="button"`, `tabindex="0"`, `aria-expanded`; opens on hover and click.
- Focus-visible rings inherited; reduced-motion inherited (no analysis animation).
- Neutral flag dot on the pill carries a `title`; the flag itself is text, not color-only (color is never the sole signal).

## Layout constraints (DL-096/D046)
- Overview sections stay **exactly** Confidence → Start here → Progress → More. **No new standing sections. No separate reliability card.** All Slice-3 depth lives in the pill popover, subtle card markers, the Why disclosure, and the More/Project summary.
