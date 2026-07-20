# Slice 11 — Execution-Ready Planning & Export · Product Detail

**Scope:** the execution-ready planning surfaces of the frozen R1 build (md5 `a327d702`) — the authored task tree, task-altitude assessment, the computed critical path, the eighth "Full plan" consolidated view, and the structured Asana export. Product behaviour only; no backend/API/DB. The Asana connector is **simulated** in the prototype (no live API). Built by DL-145 (identity) + DL-146→151 (build).

> NEW slice. Boundaries (owner-accepted 2026-07-20): Slice 11 owns the execution-planning model and all four surfaces; the **generic artifact-editing mechanics belong to Slice 5** (cross-referenced), and the **generic share + reader-export belong to Slice 9** (a distinct object, D107). Execution monitoring is out of R1.

---

## Feature 1 — The authored, graded task model (DL-146) · `WBS:` document body

- **Frame.** The Work breakdown document intro (`data-epi="derived"`) states OSLO decomposed the plan to the task level needed to execute and export; where inputs didn't specify a task/step/owner, OSLO inferred it, so every row is **From OSLO** until confirmed, and the thinnest inferences are flagged **`low confidence`**, worth confirming first.
- **Decomposition.** Five workstreams broken down to task and subtask level, rendered as an unchanged `<table>` (Task · Owner columns). Outline numbers in `.wbs-n`; task text in `.wbs-t` with `data-lvl` indentation (`0` = workstream header, also `.wbs-h`; `1` = task; `2` = subtask). Nineteen rows (5 workstream headers + 14 tasks).
- **From OSLO until confirmed.** Every cell is marked derived by the existing `_seedTableProvenance` engine; the user confirms a row by editing/accepting the cell (flips to **Confirmed by you**). **No new validation path** — authoring reuses the ratified attestation engine at task altitude (DL-145 §3).
- **Graded inference.** Three rows carry a neutral `.conf-low` grade (`contenteditable="false"`, dashed/subtle, a tooltip inviting confirmation): **1.2 Confirm 500-person Wi-Fi capacity**, **1.3.1 Map AV power drops**, **1.3.2 Lay out badging & check-in stations**. The grade is a **neutral epistemic mark, never a severity colour** (D003 / DL-109).
- **Preserved anchors.** ISS-05 (unassigned owner) stays on the CFP header owner cell; ISS-11 anchors on task 1.3.1 and ISS-10 on task 2.1 via inline `_a()` issue anchors.
- **Requirement — engine reuse (DL-146 guardrail):** the table stays a `<table>`; `attachTableControls`, `_seedTableProvenance`, per-cell hover provenance chips, row/column ops, autosave, and version bumps all keep working on the deeper tree. **The generic editing mechanics are documented in Slice 5** — Slice 11 owns only the execution-planning semantics (decomposition, grading, provenance meaning).

## Feature 2 — Task-altitude assessment (DL-147) · ISS-10 / ISS-11

Two task-level findings ship as ordinary issues (real `sec`/`dim`/`ev`/`why`/`rec`/`paths`), surfaced on the **deeper read** (Extended pass) through the same issue engine:

- **ISS-10 — The freeze rests on undated tasks.** `rectype:'planning'`, `ftype:'Coverage Gap'`, **moderate**, **Feasibility**, `sec:'WBS'`. *Why:* the Sep 1 run-of-show freeze depends on tasks that carry no dates — closing the CFP and selecting the program — and the breakdown dates neither. Evidence cites the Work breakdown dependency and the Schedule "Run-of-show final Sep 1". Recommendation: set target dates for the CFP close and program selection that clear the freeze. Paths: *Backdate the CFP-close and selection from Sep 1* · *Move the freeze if the upstream work can't fit*. Anchored on task 2.1 (Close the CFP).
- **ISS-11 — Part of the breakdown is inferred.** `rectype:'definition'`, `ftype:'Assumption'`, **moderate**, **Clarity**, `sec:'WBS'`. *Why:* part of the breakdown is OSLO's own low-confidence inference — three tasks the brief did not state — so the plan's completeness rests partly on OSLO's read. Named as **evidence honesty, never a warning** (DL-109). Anchored on task 1.3.1 (Map AV power drops).
- **Requirements.** Both are observation-type (no `clar`, opening-turn budget honoured, D167). They raise Work breakdown open issues 1 → 3 after the deeper read, light the CAF/Attention map/Jump-to-issue/issue panel, and route through `_submitClarification`/the analysis update like any other issue. Supporting context items CI-71/72/73 (`hz:'deep'`, `art:'WBS'`) keep the inference/assumptions surfaces coherent. They **re-read the inputs OSLO already has** — the decomposed WBS + Schedule — inventing no new evidence (D177).

## Feature 3 — Sequencing + the computed critical path (DL-148) · `WBS_TASKS`, `_criticalPath`, `_wbsCriticalPathHTML`

- **The model.** `WBS_TASKS` carries each task with `{id, ws, n, name, owner, dur (weeks, inferred), deps[], lowConf?, milestone?}`. Durations are OSLO's inference, flagged low confidence — the least-inferable input (DL-145 §5).
- **The computation.** `_criticalPath()` runs a standard **earliest-finish over the dependency DAG** and reconstructs the longest chain back from the milestone (`t-ros`, `milestone:'Sep 1'`). Returns `{chain:[task…], weeks}`. For DevNorth it computes **Close the CFP → Select 2 keynotes + 12 breakouts → Lock the run-of-show, ~5 weeks**. (The marketing chain *Launch the registration site → Run the promotion campaign* runs longer, ~8 wk, but does **not** run to the Sep 1 milestone — the critical path is the longest chain **to the milestone**, per the DL-150 correctness fix.)
- **The panel (`_wbsCriticalPathHTML`).** A `.cpath` panel: header "Sequencing & critical path" + a **From OSLO** chip; a sub-line; the chain as `.cp-node` boxes (`~N wk` durations; the milestone node shows "Sep 1", `.cp-end` cool accent) joined by `→` arrows; a footer "~5 weeks of sequenced work feeds the fixed Sep 1 freeze… the durations and the sequence are OSLO's inference `low confidence`, so confirm them to firm the path" + a link to ISS-10 **when it is live** (`_istatus['ISS-10'] !== 'resolved'`).
- **Placement.** Rendered **outside `#artdoc`** — appended after the editable doc when `name === 'WBS'` (`openArtifact`), so the table/autosave machinery never touches it. It is analysis (feasibility), on OSLO's side of the export handoff (DL-145 §1), never a Gantt or a health signal.
- **Guard `_assertCriticalPathComputed` (D173).** Proves (a) the reported chain is a real dependency chain — each step depends on the previous; and (b) the reported weeks equal the **milestone task's earliest finish** (the longest chain to the milestone). A path that doesn't follow the edges reddens the build.

## Feature 4 — The eighth "Full plan" consolidated view (DL-149/150) · `showView('fullplan')`, `renderFullPlan`

Nav item `#sbFullPlan` (⊞), pane `#pane-fullplan > #fullPlanBody`, breadcrumb "Full plan". Re-rendered live on entry. `renderFullPlan()` renders, all computed:

- **Head.** Kicker "Full plan"; title "*<Project>* — the whole plan, before export"; meta (`current analysis`/`provisional` + date); a **Export to Asana ↗** button (`.fp-exp` → `openAsanaExport()`).
- **(a) Execution readiness** (`_execReadiness`). A `.fp-ready` card: the **named state** (`.fp-state`: *Mostly OSLO's draft* / *Load-bearing confirmed* / *Fully validated*); a coverage line "**N** of **M** execution-critical statements Confirmed by you · **K** still From OSLO"; a **coverage bar** (`.fp-bar` / `.fp-barfill`, `role="img"`, aria "N% confirmed by you"); a note: *"This is how much of the plan you have validated — not a prediction that it will succeed. Export is always available; OSLO carries what is still From OSLO into the hand-off, flagged."* (Frozen-build render: *Mostly OSLO's draft · 7 of 23* — the exact numbers are **computed**, not authored; DL-149's earlier *7 of 29* example predates the DL-150 model promotion.)
- **(b) The consolidated plan** (`_fullPlanTasksHTML`). Section "The plan — every workstream, consolidated", an intro (every task From OSLO until confirmed; durations inferred; critical-path tasks marked), a header row (Task · Owner · Est. · sequence), then every task grouped by `.fpt-ws` workstream. Each `.fpt-row` (`.fpt-cp` when on the path): number, name (+`.conf-low` grade, +`.fpt-cptag` "critical path"), owner, estimate (`~N wk` or the milestone) + dependency (`after 1.1`). Rendered from `WBS_TASKS` (real data, not re-parsed HTML — D173). Critical-path rows carry a **neutral cool accent** (sequencing cue, never severity — D003).
- **(c) The sequence that drives the date.** `_wbsCriticalPathHTML()` reused verbatim (Feature 3).
- **(d) Confirm before you hand it off.** The open execution issues (`sec ∈ {WBS, Schedule, Resources}`, not resolved), **severity-ordered** (`_sevrank`). Each `.fp-conf-row`: severity word, title + location, **Confirm →** (`openIssue`). Empty → "Nothing execution-critical is unconfirmed right now." A note: confirming firms the item; the read catches up at the next analysis update (D088). **Validation, not a shadow path** (D088).
- **Foot.** "OSLO advises; you decide — this is your plan to review and confirm before it runs. Nothing here is confirmed that you have not confirmed."
- **Requirements.** Readiness is **coverage + a validation-progress state, never a score** (D183b); the bar is Confirmed-by-you coverage, **not health** (D003). Non-blocking (DL-145 §4). Computed, never invented (D173). The seven documents are untouched — this is an eighth *view*.

## Feature 5 — The structured Asana export (DL-151) · `_asanaMapping`, `renderAsanaExport`, `openAsanaExport`, `doAsanaExport`

- **Entry + modal.** *Export to Asana ↗* on the Full plan → `openAsanaExport()` renders the preview into `#asanaExportBody` and shows the scrim `#asanaExportScrim` (a `.wmodal`, `role="dialog"`, `aria-modal`, titled "Export to Asana", sub "The executable plan, mapped to Asana — a preview before you send"). Registered opaque in `_DIALOG_PANELS` (D195a).
- **The mapping (`_asanaMapping`).** For each of the 14 `WBS_TASKS`, returns exactly `{osloId, name, assignee (owner), due (milestone or ~N wk), deps (names), prov}`. Since nothing is Confirmed by you yet, every task crosses as **From OSLO** or **From OSLO · low confidence** (the three low-confidence tasks carry the 2A grade).
- **The preview (`renderAsanaExport`).** A boundary banner: *"OSLO sends the executable plan. Its intelligence — the critical path, the open issues, the maturity read — stays in OSLO, live… OSLO remains the plan of record."* A "How it maps" legend: Task·subtask → Asana task·subtask · Owner → Assignee · Duration·date → Due date · Depends on → Dependency · Provenance → custom field **OSLO Provenance** · OSLO task id → custom field **OSLO Task ID** (so OSLO can monitor execution back to the plan). A "What lands in Asana · 14 tasks" table (name +`after …` dependency · assignee · due · OSLO Provenance, low ones tinted). A free-tier note: *custom fields require Asana Premium; on free Asana provenance lands as a **tag** — enough for the honesty signal, a degraded mode for monitoring.* A readiness line: *N of M Confirmed by you; the rest cross flagged From OSLO. You can export now — nothing is blocked.*
- **The hand-off (`doAsanaExport`).** Simulated. `pushHistory('export', 'Exported the plan to Asana (14 tasks)', …)` records the executable plan mapped to Asana, each carrying its **OSLO Provenance** and **OSLO Task ID**, and states explicitly that OSLO's analysis stays in OSLO and this export runs no analysis and moves no read (D112). Closes the modal; `_stubToast('Plan exported to Asana — simulated…')`.
- **Guard `_assertExportSendsPlanNotAnalysis` (DL-151 §1, the load-bearing invariant).** Verifies every mapped task carries **only** the execution allowlist (`osloId · name · assignee · due · deps · prov`) and nothing from OSLO's intelligence (no critical-path flag, no issue, no CAF/band/reliability); and that the two non-negotiables — **provenance** and **OSLO Task ID** — are present on every task. Any analysis field fails the build.
- **Requirements.** Export ≠ share (D107) — a distinct object from Slice 9's reader-export; **simulated** like the reader-export but a separate hand-off. An export is a read; it produces no assessment (D112). Non-blocking (DL-145 §4). The provenance field is an epistemic state, not a rating — nothing crosses that could read as a forecast/health verdict (D003/D183b).

## Feature 6 — The execution-ready identity (DL-145)

The doctrine layer beneath the five build features, upheld as assertions across the slice:

- **OSLO both authors and certifies** — infer-to-complete + use-and-infer; **every inference is marked for validation** (D011/D069, DL-109). Authoring never breaks D173.
- **Completeness ≠ readiness** — a fully-decomposed, fully-inferred plan must never read as ready; readiness is a function of grounding, not decomposition (the Outcome Confidence read is untouched by adding plan detail).
- **Readiness = coverage → a named validation-progress state** — non-blocking, artifact-readiness not outcome-likelihood, **never a will-succeed verdict** (DL-145 §4, D183b).
- **Sequencing dependencies + critical path are IN** — this retires the "no dependency register" implementation stance, and is **distinct from D114 "understanding dependencies"** (waiting on a person's response); the two are named apart.
- **One converged task model** (`WBS_TASKS`); the seven documents stay focused views + this eighth consolidated view.
- **Execution-export = deep connector, Asana first, provenance as a native field** — the plan crosses, the analysis stays in OSLO.

## Non-goals / seams (do not build here)

- **Execution monitoring** (Execute → In execution → Outcome) — future phase, out of R1. The **OSLO Task ID** anchor is the only forward-looking hook; the read-back, live Asana API, and percent-complete tracking are not built.
- **Resource leveling** — deferred (DL-145 §5); this is edges + critical path only.
- **Generic artifact-editing** (Slice 5) and **generic share/reader-export** (Slice 9) — cross-referenced, not re-documented here.
</content>
