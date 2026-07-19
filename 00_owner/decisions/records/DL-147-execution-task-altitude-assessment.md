# DL-147 — Execution-ready planning, Phase-2 · 2B — assessment scaled to task altitude

- **Date:** 2026-07-19 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# Execution-ready planning, Phase-2 · 2B — assessment scaled to task altitude

**Class:** B (a build within the ratified execution-ready framework — no new scope) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-19 · **Realizes** **DL-145** (execution-ready planning identity), Phase-2 slice **2B** — *assessment (CAF + issue model) scaled to task/subtask altitude* (DL-145 §5.2). **Extends** DL-146 (the decomposed task tree). **Upholds** D177 (a deeper read re-reads the same inputs — it invents nothing), D173 (computed, not invented), DL-109 (inference named honestly), D003 (maturity, not health), D088 (the read moves by analysis).

---

## Decision

Now that the plan is decomposed to tasks (DL-146 · 2A), OSLO **assesses at task altitude** — it finds gaps that were invisible when the Work breakdown was a five-row deliverable table. Two task-altitude findings ship, both surfaced on the **deeper read** (the Outcome Analysis / Extended pass) through the **same issue engine** as every other finding, anchored to the specific tasks they concern:

1. **ISS-10 — *The freeze rests on undated tasks*** (Feasibility · Work breakdown). The Sep 1 run-of-show freeze depends on *Close the CFP* and *Select the program*, and the breakdown dates neither — so OSLO can’t confirm the upstream work fits before the freeze. **This gap only exists at task altitude**: at deliverable altitude "run-of-show final Sep 1" was a single milestone; the undated upstream chain is visible only once the CFP stream is decomposed. Anchored on task **2.1 (Close the CFP)**.
2. **ISS-11 — *Part of the breakdown is inferred*** (Clarity · Work breakdown). OSLO’s read on **its own authored decomposition**: three tasks are its low-confidence inferences (the ones graded in 2A), so the plan’s completeness rests partly on OSLO’s read of the work — worth confirming before the breakdown is relied on. Named as **evidence honesty, never a warning about the plan** (DL-109). Anchored on task **1.3.1 (Map AV power drops)**, already flagged low-confidence.

Both are **real issues in the real model**: they carry a dimension, a severity, citations, a recommendation and resolution paths; they raise the Work breakdown’s open-issue count (1 → 3 after the deeper read); they light the CAF, the Attention map, Jump-to-issue and the issue panel; and they route through `_submitClarification`/the analysis update like any other issue. **This is the point of the deeper decomposition — it earns its place by producing assessable signal** (DL-145 §5.2).

## Why the deeper read, and why it invents nothing

Task-altitude gaps are, by nature, a **deeper** read — so the findings surface on the Extended pass (like ISS-07/08/09), which keeps the boot state stable and is thematically honest: finding task-level gaps is what a deeper analysis is *for*. And they **re-read the inputs OSLO already has** (the decomposed WBS task tree + Schedule) — no new evidence is invented (D177). Their supporting context items (CI-71–73, `hz:'deep'`, `art:'WBS'`) keep the inference/assumptions surfaces coherent when the findings land.

## Guardrails

- **Real model, not a bolt-on** — ISS-10/11 are ordinary issues (well-formed `sec`/`dim`/`ev`/`why`/`rec`); `_assertDeepPassMovesBandAndCounts` grades them like any deep finding, and the open-issue count / CAF tallies stay consistent (computed, D173).
- **Opening-turn budget honoured** (D167) — both findings are observation-type (no `clar`, like ISS-08/09); their chat opening turns fit the 50-word budget (the guard bit during the build and was satisfied by trimming, not by hiding copy).
- **Honest inference, not a health mark** (DL-109 / D003) — ISS-11 names OSLO’s own inference as evidence honesty; the low-confidence grade it reads from stays a neutral epistemic mark, never a severity.
- **The read still moves by analysis** (D088) — confirming a task-altitude finding firms the read at the next analysis update, never by hand.
- **Invents nothing** (D177) — the findings re-read the decomposed WBS + Schedule; every citation is a real artifact.

## Scope — 2B of Phase-2

This scales assessment to task altitude on the two clearest gap types (a dateless task against a hard freeze · a plan resting on low-confidence inference). Remaining Phase-2 slices: **2C** — the sequencing-dependency model + critical path (ISS-10 is its natural anchor — the undated dependency chain becomes a computed path); **2D** — the eighth consolidated pre-export view. Fast-pass task-altitude findings (vs deep-only) are a possible later refinement. Phase-3 remains the Asana export.

## Governance

Lands as **Class-B** canon via `dl-land`, realizing DL-145 Phase-2 · 2B and extending DL-146. Built + verified in the deliverable prototype (boot self-check **152/152**, 0 pageerrors; the deeper read surfaces both findings — Work breakdown 1 → 3 open, live annotations on tasks 2.1 and 1.3.1, all through the existing issue engine). AI drafted + built; **only the owner ratifies.**
