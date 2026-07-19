# DL-150 — Execution-ready planning, Phase-2 · 2D completion — the consolidated view displays the plan

- **Date:** 2026-07-19 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# Execution-ready planning, Phase-2 · 2D completion — the consolidated view displays the plan, not only the analysis

**Class:** B (a build within the ratified execution-ready framework — no new scope) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-19 · **Completes** **DL-149** (the eighth consolidated view) — closing an owner-reported gap: *the Full plan view displayed the analysis (readiness · critical path · confirm-list) but not the consolidated plan itself.* **Realizes** DL-145 §6 fully (the eighth view is *the whole sequenced plan in one place*). **Upholds** D173 (computed from data, not re-parsed HTML), D003 (neutral, not health), DL-145 §2/§3 (From OSLO until confirmed).

---

## Decision

The **Full plan** view now renders **the consolidated plan itself** — the whole task model in one place — not only the analysis around it. Owner-reported: the view showed readiness, the critical path and the confirm-list, but never the plan the user is about to export. Fixed.

1. **A real task model.** `WBS_TASKS` is promoted from the five sequencing-only tasks to **the full decomposition** — every task with its workstream, outline number, owner, inferred duration, and dependency edges. The consolidated view and the critical path both render from **this one source of data** (not re-parsed document HTML), so the plan shown is real, structured data. (The task names mirror the Work breakdown document; full convergence of the document itself onto this model is a later refinement.)
2. **The consolidated plan renders.** A new **“The plan — every workstream, consolidated”** section lists every task grouped by workstream, showing owner · inferred duration · dependency (*after 1.1*) · **critical-path** membership · **low-confidence** grade. Every task is **From OSLO until confirmed**; the critical-path tasks carry a neutral cool accent (a sequencing cue, never a severity/health colour — D003).
3. **A correctness fix to the critical path** (found by promoting the model). With the full plan, chains run to **different deadlines** — the marketing campaign chain (~8 wk to the event) is longer than the CFP chain (~5 wk to the Sep 1 run-of-show freeze). The critical path is the longest chain **to the milestone**, not the longest chain anywhere; the computation was already correct (it anchors on the milestone), and `_assertCriticalPathComputed()` was **tightened** to assert *reported weeks = the milestone task’s earliest finish* rather than *≥ the longest chain overall*. The reported path is unchanged (Close the CFP → Select the program → Lock the run-of-show, ~5 wk).

## Guardrails

- **Computed from data, not authored** (D173) — the consolidated plan and the critical path both render from `WBS_TASKS`; nothing is re-parsed from HTML or hard-coded. The tightened guard proves the path is the longest chain to the milestone.
- **From OSLO until confirmed** (DL-145 §2/§3) — the plan intro states every task is OSLO’s until the user confirms it; low-confidence tasks keep their grade; nothing is presented as confirmed.
- **Neutral, not health** (D003) — the critical-path accent is a cool sequencing cue; there is no severity colour, no RAG, no completion bar in the plan table.
- **The seven documents are untouched** — the consolidated view reads the model; the focused editing surfaces and their guards verify unchanged. Class-resolve clean (D195a): new `fpt-*` classes carry CSS.

## Scope

This completes the eighth view’s intent (DL-145 §6) — it now shows both the plan and its readiness. The deeper convergence (the Work breakdown *document* rendering from `WBS_TASKS` too, one true source) is a possible later refactor; today the document remains the authored editing surface and the model mirrors it. Phase-3 (the Asana export) is unchanged — it now has a real task model to map from.

## Governance

Lands as **Class-B** canon via `dl-land`, completing DL-149. Built + verified in the deliverable prototype (boot self-check **153/153**, 0 pageerrors; the consolidated plan renders 14 tasks across 5 workstreams with owners · durations · dependencies · 3 critical-path rows marked; the tightened critical-path guard passes on the fuller model). AI drafted + built; **only the owner ratifies.**
