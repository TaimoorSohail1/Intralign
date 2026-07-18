# DL-131 — Per-dimension evidence cue — keep the word, drop the bar; hide when expanded

- **Date:** 2026-07-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# The per-dimension evidence cue keeps the word, drops the bar; hides when the drill is open

**Class:** B (experience-doctrine refinement) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-18 · **Refines** DL-123 (Option C — the per-dimension evidence cue).

---

## Decision

The CAF row's per-dimension evidence cue is **decluttered without losing its honesty**. It kept a mini grounded/inferred **bar** plus the word and fraction ("Thinly evidenced · 1 of 7"), which (a) added visual weight to every row and (b) duplicated the drill's "Rests on" line, which draws the same grounded/inferred split more completely when the row is expanded.

Two changes:
1. **Collapsed row — keep the word, drop the bar.** The cue now reads just the evidence **word** + fraction ("Thinly evidenced · 1 of 7"), no bar. The word is what carries the load-bearing signal — a dimension's **level is not its trustworthiness** (Option C: "Clarity: High" but 1-of-7 grounded means confirm it before leaning on it). The bar was the heavy, duplicated part; the word costs almost nothing and preserves the honesty at a glance.
2. **Expanded row — hide the cue entirely.** When a dimension's drill is open, its row cue hides (`.cafrow[aria-expanded="true"] .caf-ev`), because the drill's **"Rests on"** line is the cue's expanded form. To lose nothing, the evidence **word is folded into "Rests on"** — "Thinly evidenced — 1 of 7 grounded · 6 inferred". The grounded/inferred bar is now drawn exactly once in each state.

## Why not remove the cue entirely (considered, rejected)

Removing the per-dimension cue from the row was considered and declined: it would re-open the exact "level = trust" conflation Option C exists to close. "Clarity: High" alone reads as *solid*; the read surface would lose the at-a-glance signal that a high dimension is thinly evidenced, and per-dimension grounding would require a click into each drill. It is not redundant with the whole-read `#ov-grounding` rollup either — that is the aggregate (20 of 48 across the read), not *which dimension* is the inferred one. The cue is not guard-locked, so full removal would pass the self-check — but it would walk back a ratified honesty element silently, which is worse. So only the **bar** was cut (and the cue hides when expanded), never the word.

## Guardrails

- **Level ≠ trust preserved** — the evidence word stays on every collapsed row; a dimension's level never stands alone as if it were its trustworthiness (Option C / DL-123 intact).
- **One home for the thresholds** — the word is computed by a single `_evWord(grounded, total)` shared by the row cue and the drill, so the two can never disagree.
- **The bar is drawn once per state** — collapsed: no bar (word only); expanded: the cue hides and the drill's "Rests on" carries the bar + numbers + word.

## Governance

Lands as canon via `dl-land`, refining DL-123 (the per-dimension evidence cue's presentation only — no change to the read architecture or the level/grounding separation). Built + verified in the deliverable prototype (boot self-check **151/151**, 0 pageerrors; Option C / CAF-drill guards still green). AI drafted + built; **only the owner ratifies.**
