# Slice 11 — Execution-Ready Planning & Export · Success Criteria

The developer's checklist for the execution-ready surfaces of the frozen build (md5 `a327d702`, boot 157/157). **FREEZE-INTACT:** these assert the build as frozen — not new enhancements. The Asana connector is **simulated** (no live API). Doctrine invariants + guards are baked in as assertions.

## Cumulative-integrity (no regression)
- [ ] SC-0 Every earlier-slice route, screen, interaction, theme token, and localStorage key still works (Overview journey arc + read, Issues, History, Inference map, Reports, Documents + the artifact editor, share/reader-export, chat + notices).
- [ ] SC-0b The build boots green (**157/157** guards) with no console error, including `criticalPathComputed` and `exportSendsPlanNotAnalysis`.

## Feature 1 — the authored, graded task tree (DL-146)
- [ ] SC-1 The Work breakdown document is an **authored task tree** — workstreams → tasks → subtasks, outline-numbered (`1 · 1.1 · 1.3.1`) with `data-lvl` indentation (5 workstreams, 14 tasks, 19 rows). Any "flat 5-row deliverable table" copy is retired.
- [ ] SC-2 **Every row is From OSLO until confirmed** (`_seedTableProvenance` marks all cells derived); confirming a row is the **existing** edit/accept attestation — no new validation path was built (DL-145 §3).
- [ ] SC-3 The thinnest inferences carry a neutral **`low confidence`** grade (`.conf-low`, `contenteditable="false"`) on tasks **1.2 · 1.3.1 · 1.3.2**; it is an **epistemic mark, never a severity colour** (D003 / DL-109).
- [ ] SC-4 The table format is **unchanged** — all Slice 5 table machinery (controls, per-cell provenance chips, row/col ops, autosave, version bumps) verifies on the deeper tree; the ISS-05/10/11 anchors are preserved. (Generic editing mechanics belong to Slice 5.)
- [ ] SC-5 Adding plan detail does **not** move the Outcome Confidence read — completeness ≠ readiness (DL-145 §3); a deeper, still-inferred plan is not a more mature one.

## Feature 2 — task-altitude assessment (DL-147)
- [ ] SC-6 **ISS-10 "The freeze rests on undated tasks"** (moderate · Feasibility · WBS) and **ISS-11 "Part of the breakdown is inferred"** (moderate · Clarity · WBS) surface on the **deeper (Extended) read** through the **same issue engine** (real `why`/`ev`/`rec`/`paths`), anchored on tasks 2.1 and 1.3.1.
- [ ] SC-7 The deeper read raises the Work breakdown open-issue count **1 → 3**; both light the CAF/Attention map/Jump-to-issue and route through `_submitClarification`/the analysis update like any other issue.
- [ ] SC-8 **ISS-11 is OSLO's honest read on its OWN low-confidence decomposition** — named as evidence honesty, **never a warning** about the plan (DL-109); it reads from the neutral low-confidence grade, never a severity.
- [ ] SC-9 The findings **invent nothing** (D177) — they re-read the decomposed WBS + Schedule; every citation is a real artifact; CI-71/72/73 keep the inference surfaces coherent.
- [ ] SC-10 A task-altitude finding resolves **only at an analysis update** (D088), never by the hand-path.

## Feature 3 — sequencing + the computed critical path (DL-148)
- [ ] SC-11 `WBS_TASKS` carries dependency edges + inferred durations; `_criticalPath()` runs earliest-finish over the DAG and reconstructs the longest chain **to the milestone**, returning **Close the CFP → Select 2 keynotes + 12 breakouts → Lock the run-of-show, ~5 weeks** into the fixed **Sep 1** freeze.
- [ ] SC-12 The chain is **computed, not authored** (D173) — `_assertCriticalPathComputed()` proves (a) each step depends on the previous and (b) the reported weeks equal the **milestone task's earliest finish**. Change an edge or a duration and the path moves.
- [ ] SC-13 The longer marketing chain (~8 wk) is **not** the critical path because it does not reach the Sep 1 milestone — the path is the longest chain **to the milestone**, not the longest anywhere (DL-150 correctness fix).
- [ ] SC-14 The **"Sequencing & critical path"** panel renders as **From OSLO**, durations **low confidence**, linked to ISS-10 **when live** — and renders **outside `#artdoc`** (never editable plan content, D160); the table/autosave machinery never touches it.
- [ ] SC-15 The panel is **feasibility analysis, not tracking** (DL-145 §1 / D003) — neutral chrome, a sequencing read, never a Gantt or a health signal.

## Feature 4 — the eighth "Full plan" consolidated view (DL-149/150)
- [ ] SC-16 A peer nav item **Full plan (⊞ `#sbFullPlan`)** opens `showView('fullplan')` → pane `#pane-fullplan` → `renderFullPlan()`, re-rendered live on entry, with nav + breadcrumb in sync. The seven documents are untouched.
- [ ] SC-17 **Execution readiness** (`_execReadiness`) shows a **named validation-progress state** (*Mostly OSLO's draft → Load-bearing confirmed → Fully validated*) derived from the **provenance coverage** of the execution-critical set (WBS · Schedule · Resources) — "N of M Confirmed by you · K From OSLO".
- [ ] SC-18 Readiness is **coverage + a state, never a score** (D183b); it describes **what you have validated, never a "will-succeed" verdict**; the coverage bar (`.fp-barfill`) is **Confirmed-by-you coverage, NOT health** (D003); it is **non-blocking** (DL-145 §4 — Export is always available).
- [ ] SC-19 The **consolidated plan** renders all 14 tasks × 5 workstreams from `WBS_TASKS` (owner · inferred duration · dependency · critical-path mark · low-confidence grade) — from **real data, not re-parsed HTML** (D173); every task is From OSLO until confirmed; critical-path rows carry a **neutral cool accent** (sequencing cue, never severity).
- [ ] SC-20 The **confirm-before-hand-off** list shows open execution issues **severity-ordered**, each routing via **Confirm →** (`openIssue`) to the **existing confirm surface** — validation, **not a shadow path** (D088). Empty → "Nothing execution-critical is unconfirmed right now."
- [ ] SC-21 The computed critical path (Feature 3) is reused verbatim (`_wbsCriticalPathHTML`), and **Export to your tool** (`.fp-exp`) opens the export.

## Feature 5 — the structured Asana export (DL-151)
- [ ] SC-22 **Export to Asana** opens a **mapping preview** (`#asanaExportScrim`, `renderAsanaExport`/`_asanaMapping`) showing all 14 tasks with assignee · due · dependency · **OSLO Provenance**, before it sends.
- [ ] SC-23 **Only the executable plan crosses** — tasks/subtasks → Asana tasks · owners → assignees · durations/dates → due dates · dependencies → dependencies. **OSLO's analysis — critical path, issues, the maturity read — does NOT cross** (it stays in OSLO). *(The single most important invariant of the slice.)*
- [ ] SC-24 `_assertExportSendsPlanNotAnalysis()` enforces the **allowlist** (`osloId · name · assignee · due · deps · prov`) — any analysis field (critical-path flag, issue, CAF/band/reliability) fails the build — **and** proves every task carries the two non-negotiables: **provenance** and **OSLO Task ID**.
- [ ] SC-25 Provenance rides as a native **OSLO Provenance** custom field (*Confirmed by you / From OSLO / From OSLO · low confidence*) — an OSLO-owned **read-only honesty signal** — plus an **OSLO Task ID** custom field (the anchor a future execution-monitoring phase would need). **Tag fallback** covers free-tier Asana.
- [ ] SC-26 The export is **non-blocking** (DL-145 §4) — the preview states how many statements are Confirmed by you vs cross flagged From OSLO; it never gates.
- [ ] SC-27 **Export ≠ share** (D107) — a distinct object from Slice 9's reader-export — and **an export is a read that produces no assessment** (D112): `doAsanaExport` appends a **History** record, runs no analysis, and moves no read; the hand-off is **simulated** (no live API) + a toast.
- [ ] SC-28 The Asana modal is registered opaque in `_DIALOG_PANELS` and resolves clean (D195a); `ax-*` classes carry CSS.

## Feature 6 — the execution-ready identity (DL-145)
- [ ] SC-29 OSLO **both authors and certifies** — every inferred task/owner/date/dependency is **marked From OSLO for validation** (D011/D069, DL-109); authoring never presents inference as fact (D173).
- [ ] SC-30 Sequencing dependencies + critical path are **in** (the "no dependency register" stance is retired), and are named **apart from D114 "understanding dependencies"** (waiting on a person) — the two never conflate.
- [ ] SC-31 There is **one converged task model** (`WBS_TASKS`) beneath the seven focused documents + this eighth consolidated view; nothing across the slice emits a composite/forecast/will-succeed verdict (D183b).

## Cross-cutting
- [ ] SC-32 Advisory-only throughout (D001); severity red/amber/green only on issues (D003); the `low confidence` grade + critical-path accent are neutral; no percentage-health fill anywhere; dark default + light parity; WCAG 2.1 AA.
- [ ] SC-33 Execution **monitoring** is out of R1 — nothing tracks percent-complete; the only forward hook is the OSLO Task ID anchor in the export.
</content>
