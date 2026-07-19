# DL-148 — Execution-ready planning, Phase-2 · 2C — sequencing dependencies and the computed critical path

- **Date:** 2026-07-19 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# Execution-ready planning, Phase-2 · 2C — sequencing dependencies and the computed critical path

**Class:** B (a build within the ratified execution-ready framework — no new scope) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-19 · **Realizes** **DL-145** (execution-ready planning identity), Phase-2 slice **2C** — *the sequencing-dependency model + critical path* (DL-145 §5, edges + critical path; resource leveling deferred). **Extends** DL-146 (the task tree) and DL-147 (the undated-freeze finding, ISS-10). **Upholds** D173 (computed, never invented), DL-109 (inference named honestly), D003 (maturity, not health), D160 (the reading surface).

---

## Decision

OSLO now **sequences** the plan: it models task dependencies and inferred durations, and **computes the critical path** — the longest dependency chain that decides the earliest the Sep 1 run-of-show freeze can be met.

1. **A dependency + duration model.** `WBS_TASKS` carries each sequencing-relevant task with its inferred duration and its dependency edges. Durations are **OSLO’s inference, flagged low confidence** — the least-inferable input (DL-145 §5), so they carry the same graded mark as the tasks in 2A.
2. **The critical path is computed, not authored.** `_criticalPath()` runs a standard earliest-finish over the dependency DAG and reconstructs the longest chain back from the milestone. For DevNorth it computes **Close the CFP → Select the program → Lock the run-of-show (~5 weeks)** — longer than the venue chain — so that is the path driving the Sep 1 date. Change an edge or a duration and the path moves; a new guard proves it (below).
3. **Rendered as analysis, on OSLO’s side of the handoff.** A **“Sequencing & critical path”** panel renders the computed chain in the Work breakdown view — marked **From OSLO**, durations **low confidence**, and linked to the undated-freeze finding (ISS-10) when it is live. It is **feasibility analysis** — OSLO *analysing* the plan’s sequence, not *tracking* execution — so it sits cleanly on OSLO’s side of the export handoff (DL-145 §1). It renders **outside the editable document** (`#artdoc`), so it never becomes editable plan content and the table/autosave machinery never touches it.

**Resource leveling stays deferred** (DL-145 §5) — this is edges + critical path only.

## Why this is the interesting slice

2A decomposed the plan; 2B found that the freeze rests on undated tasks (ISS-10). 2C is where that finding gets a **computed structure behind it**: the “undated dependency chain” becomes an actual path with a length (~5 weeks) against a fixed date (Sep 1). This is what makes Feasibility credible at task altitude — not “Feasibility: Moderate,” but “this five-week chain drives your Sep 1 date, and its tasks are undated.” The read points at the thing.

## Guardrails

- **Computed, never authored** (D173) — `_assertCriticalPathComputed()` proves the reported chain is (a) a real dependency chain (each step depends on the previous) and (b) the **longest** chain in the model (no task’s earliest-finish exceeds the reported weeks). A path that doesn’t follow the edges reddens the build. (Boot self-check now **153/153** — one new guard.)
- **Inference named honestly** (DL-109) — durations are marked From OSLO and low-confidence; the panel says the sequence is OSLO’s inference, to be confirmed. Nothing is presented as fact.
- **Analysis, not tracking** (DL-145 §1 / D003) — the panel is neutral chrome, a sequencing read, never a health signal or a Gantt; OSLO computes the path, it does not run the schedule.
- **The reading surface is intact** (D160) — the computed panel is furniture outside `#artdoc`; the editable task tree, its provenance engine and all table machinery are untouched.

## Scope — 2C of Phase-2

This ships the dependency + duration model and the computed critical path, rendered in the Work breakdown. The last Phase-2 slice is **2D** — the eighth consolidated pre-export view, which renders this same computed path alongside the readiness-coverage state, validate-enabled. Phase-3 remains the Asana export (where the dependency edges map to the tool’s dependencies). Fast-pass vs deep-pass surfacing and richer duration provenance are possible later refinements.

## Governance

Lands as **Class-B** canon via `dl-land`, realizing DL-145 Phase-2 · 2C and extending DL-146/147. Built + verified in the deliverable prototype (boot self-check **153/153**, 0 pageerrors; the critical path computes to the CFP chain at ~5 weeks — longer than the venue chain — renders as a marked panel with the ISS-10 link, and the new computed-path guard passes). AI drafted + built; **only the owner ratifies.**
