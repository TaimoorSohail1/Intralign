# House-doc reconciliation — DL-143 → DL-156 (2026-07-20)

**Status:** Reconciliation delta (non-canonical map). The **frozen prototype** (`vertical-slices/slice-10-tiering-limits/prototype.html`, md5 **a327d702**, boot 157/157) and the **DL records** (decision-log, through DL-156) are **authoritative**. Where a slice-10 house doc (`frontend-ui.md`, `user-experience.md`, `success-criteria.md`, `e2e-test-scenarios.md`, `edge-cases.md`, `open-items.md`, `product-detail.md`, `product-data.md`) disagrees with them, **they win** — this doc says how.
**Why this exists:** the house docs were last reconciled 2026-07-17 (through DL-124). DL-143 → DL-156 landed after that and were built into the prototype but not folded back into the (very large) house docs. This delta captures what changed so a developer is not misled by stale house-doc content, without a full 800 KB rewrite.

---

## The changes, grouped — what each supersedes

### A · Reports workspace completed + depth/export (DL-143, DL-144)

- **DL-143 — Decision Record (generated report #3).** The Reports workspace now hosts a third generated report: the owner's own decisions, computed from the `_decision` register, each paired with what it firmed and whether the read has taken it up (**Live in the read** vs **Awaiting the next analysis update**; D088 structural — a decision never credits itself with moving the read). Completes the report trio (Outcome Readiness · Assumptions & Evidence · Decision Record).
- **DL-144 — Summary ⇄ Full depth + Export.** A persisted per-report **Summary/Full** toggle on Assumptions & Evidence and Decision Record (Outcome Readiness is single-depth); every generated report reuses the **one ratified export modal** (`openExportSeam()`), distinct from share (D107).
- **Supersedes in:** `frontend-ui.md` / `user-experience.md` / `success-criteria.md` (any "Reports = one/two reports" or "no depth toggle" copy — it is now three reports with a depth toggle + export); `e2e-test-scenarios.md` (add the depth-toggle and generated-report-export flows).

### B · Execution-ready planning — a NEW direction (DL-145 identity; DL-146–150 model; DL-151 Asana export)

This is the largest addition and the house docs predate all of it.

- **DL-145 (identity, Class A)** — OSLO's deliverable is ratified as an **outcome-optimized plan detailed & exact enough to export into an execution tool and run**. Boundary = the export handoff; OSLO **both authors & certifies** (infer-to-complete + use-and-infer, every inference marked for validation); readiness = coverage of the execution-critical set → a **named validation-progress state**, non-blocking; **sequencing dependencies + critical path are in** (retires the "no dependency register" stance); one converged task model with the seven documents as focused views + an **eighth consolidated view**; execution-export = deep connector, Asana first, provenance as a native field.
- **DL-146 (2A)** — the **Work breakdown becomes an authored, graded task tree** (`WBS_TASKS`), every row From OSLO until confirmed, thinnest inferences carry a neutral `low confidence` grade.
- **DL-147 (2B)** — **task-altitude assessment**: two new task-level issues (ISS-10 the freeze rests on undated tasks; ISS-11 part of the breakdown is inferred) surface on the deeper read through the same issue engine.
- **DL-148 (2C)** — **sequencing dependencies + a computed critical path** (`_criticalPath()` over the DAG), rendered as a From-OSLO panel in the WBS view, outside `#artdoc` (never editable plan content).
- **DL-149 / DL-150 (2D)** — the **eighth "Full plan" consolidated view** (`showView('fullplan')`, nav ⊞): execution readiness (`_execReadiness()`), the computed critical path, a confirm-before-hand-off list, and **the consolidated plan itself** (all 14 tasks × 5 workstreams from `WBS_TASKS`), the pre-export surface.
- **DL-151 (Phase-3)** — the **structured Asana export**: `Export to Asana` on the Full plan opens a mapping preview → simulated hand-off + History record. **Only the plan crosses** (tasks/subtasks · assignees · dates · dependencies); **OSLO's analysis stays in OSLO**; provenance rides as an **OSLO-owned custom field** + an **OSLO Task ID** monitoring anchor; tag fallback for free-tier. Guard `_assertExportSendsPlanNotAnalysis`.
- **Supersedes in:** `frontend-ui.md` (add the Full plan view #pane-fullplan / nav ⊞; the WBS task-tree rendering; the `#asanaExportScrim` modal); `user-experience.md` (the whole execution-ready flow + the eighth view + export); `product-detail.md` / `product-data.md` (the `WBS_TASKS` task model, dependencies, durations, critical path, the two new ISS-10/11); `success-criteria.md` + `e2e-test-scenarios.md` + `edge-cases.md` (acceptance + tests + edges for the task tree, critical path, Full plan, and Asana export). **Any "Work breakdown is a flat 5-row table" or "no dependency register / no critical path" copy is retired.**

### C · The Overview hero → the plan's journey to the outcome (DL-152, DL-153, DL-154)

- **DL-152/154 (identity)** — the Overview hero is repositioned from **Outcome Confidence alone** to the **plan's journey to the outcome** (Direction C-1). The naming settled at **Understand → Optimize → Execute**, "on the way to the outcome." The third node is a **destination** (export non-blocking), never a "ready" verdict.
- **DL-153 (build)** — the journey arc + the nested Outcome Confidence read (later made persistent — see D) + the two-scope counts.
- **Supersedes in:** `frontend-ui.md` / `user-experience.md` — **any description of the Overview hero as "Outcome Confidence" alone is stale**; it is now a journey arc above the (still-present) Outcome Confidence read. Outcome Confidence is **unchanged as the concept + metric** (D199/D174/D003/D183b) — only its framing (the *Understand* / read node) changed.

### D · The two-beat journey — Understand → ⟮Optimize: Validate · Improve⟯ → Execute (DL-155, DL-156)

- **DL-155/156** — the middle *Optimize* splits into its two beats **on the axis**, under an **Optimize bracket**: **Validate** (confirm load-bearing inferences → the read becomes *trustworthy*; metric = execution-readiness coverage) then **Improve** (raise the trustworthy read; metric = the maturity band). **Each node owns one metric**; the two are **never merged** (level ≠ trust — 23/23 can still be Moderate). **Understand** is a **first-time milestone** (behavioural trigger `_planStage`, replaces the old band≥High rule). **The read is a PERSISTENT hero panel** (D179a — supersedes DL-153's read-under-Understand). **Start here is beat-aware** (`_beatOrder`/`renderFocus`): Validate leads with what grounds the read, Improve with the limiter dimension — computed, advisory, non-blocking, no tally. Demo: *Sim first-run (Understand)* + *Replay onboarding* in the Simulate ▾ menu.
- **Supersedes in:** `frontend-ui.md` / `user-experience.md` — the Overview hero is the **four-stop axis** (not the DL-152 three-node version); the read is **persistent** below it; **Start here re-ranks by the current beat** (any "Start here is pure severity order" copy is now qualified — severity breaks ties within the beat). `success-criteria.md` / `e2e-test-scenarios.md` — add: node position computed from state, the Validate→Improve threshold (frac ≥ 0.5), Start here follows the beat, Execute never gates.

## Cross-cutting invariants (unchanged — the house docs are still right on these)

D003 maturity-not-health · D183b no composite/forecast index · D179e counts have one home · D196a *Confirm* is the per-item verb · D088 the read moves only at an analysis update · D173 computed-not-authored · D107 export ≠ share · DL-145 §4 export non-blocking · D179a the read is the first panel. Nothing in DL-143→156 weakened these; several added guards that enforce them.

## What is NOT covered (out of R1 scope)

Execution monitoring (Execute → In execution → Outcome) is a **future phase**, not built and not in these docs. The three DL-156 logged follow-ons (demo Start-here reshuffle; per-beat inline detail; §6C coverage-bar treatment) are assessed as **not R1 gaps** (see the freeze marker in `RELEASE_1_BUILD_SPEC.md`).

---

**Bottom line for the developer.** Build from the **frozen prototype** (md5 a327d702, 157/157) and the **DLs** as the source of truth, with `RELEASE_1_BUILD_SPEC.md` as the consolidated instructions. Use the slice-10 house docs for depth on the parts they still describe correctly (tiering, the editor, history, notifications, the confidence architecture through DL-124) — but for the **Overview hero/journey, the execution-ready planning surface (task tree · critical path · Full plan · Asana export), and the reports trio**, this delta + the prototype override any older house-doc content.
