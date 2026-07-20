# Slice 11 — Execution-Ready Planning & Export · Workflow

Actor workflows on the execution-ready surfaces of the frozen build. Actors: **User** · **System** (client-side prototype render/state) · **AI** (simulated OSLO — timers + fixed illustrative data; no real model, no network; the Asana connector is simulated).

> NEW slice. Flows reference `WBS_TASKS`, `_criticalPath`, `_execReadiness`, `renderFullPlan`, and the Asana export. The generic artifact-editing flow lives in Slice 5; the generic share/reader-export flow lives in Slice 9.

## Flow A — OSLO authors the task tree (DL-146)

1. **AI** (at intake / build) decomposes the plan to task/subtask altitude, inferring tasks the brief did not state; the thinnest inferences are graded `low confidence`.
2. **System** renders the Work breakdown document as an authored task tree (workstreams → tasks → subtasks, outline-numbered), every cell marked **From OSLO** by `_seedTableProvenance`, three rows carrying the neutral `low confidence` grade, ISS-05/10/11 anchors in place.
3. **User** opens the Work breakdown document, reads the intro (everything is From OSLO until confirmed), and reviews the tree.
4. **User** confirms a row by editing/accepting the cell → **System** flips it **From OSLO → Confirmed by you** via the existing attestation engine (Slice 5). No new path.

## Flow B — The deeper read finds task-altitude gaps (DL-147)

1. **User** (or auto) runs the deeper read (Extended pass).
2. **AI** re-reads the decomposed WBS + Schedule (invents nothing, D177) and surfaces **ISS-10** (undated freeze, Feasibility) and **ISS-11** (part of the breakdown is inferred, Clarity) through the same issue engine.
3. **System** raises the Work breakdown open-issue count (1 → 3), lights the CAF/Attention map/Jump-to-issue, annotates tasks 2.1 and 1.3.1, and adds CI-71/72/73 to the inference surfaces.
4. **User** opens either issue → **System** shows the standard issue panel (why · evidence · recommendation · resolution paths). **AI** resolves it only at the next analysis update (D088), never by the hand-path.

## Flow C — OSLO sequences the plan and computes the critical path (DL-148)

1. **System** (on entering the Work breakdown view) calls `_wbsCriticalPathHTML()` → `_criticalPath()` runs earliest-finish over the `WBS_TASKS` DAG and reconstructs the longest chain to the Sep 1 milestone.
2. **System** renders the **"Sequencing & critical path"** panel *outside* `#artdoc` (below the editable doc), marked **From OSLO**, durations `low confidence`, with the chain **Close the CFP → Select 2 keynotes + 12 breakouts → Lock the run-of-show (~5 weeks) → Sep 1**, and — when ISS-10 is live — a link to it.
3. **User** reads the panel as analysis (feasibility), not as editable plan content.
4. **Guard** `_assertCriticalPathComputed` proves the chain is a real dependency chain and equals the milestone's earliest finish (D173).

## Flow D — Review the whole plan before export (DL-149/150)

1. **User** clicks **Full plan (⊞)** in the left nav → **System** `showView('fullplan')` → `renderFullPlan()` re-renders live.
2. **System** renders, all computed: execution readiness (state + coverage + bar), the consolidated plan (14 tasks × 5 workstreams from `WBS_TASKS`, owners · durations · dependencies · critical-path marks · low-confidence grades), the critical path (reused from Flow C), and the confirm-before-hand-off list (open execution issues, severity-ordered).
3. **User** clicks a **Confirm →** in the list → **System** `openIssue()` routes to the existing confirm surface (validation, not a shadow path). **AI** firms the read at the next analysis update (D088).
4. Export is available throughout — the view never gates (DL-145 §4).

## Flow E — Export the executable plan to Asana (DL-151)

1. **User** clicks **Export to Asana ↗** on the Full plan → **System** `openAsanaExport()` builds `_asanaMapping()` (14 tasks, execution allowlist only) and shows the preview modal `#asanaExportScrim`.
2. **System** renders the mapping preview: the boundary banner (intelligence stays in OSLO), the "How it maps" legend, the 14-task table (name · assignee · due · OSLO Provenance), the free-tier tag-fallback note, and the readiness line.
3. **User** reviews and clicks **Export to Asana** → **System** `doAsanaExport()`:
   - **AI/System** performs a **simulated** hand-off (no live API).
   - **System** appends a History record ("Exported the plan to Asana (14 tasks)…"), stating the analysis stays in OSLO and the export runs no analysis and moves no read (D112).
   - **System** closes the modal and shows a simulated toast.
4. **Guard** `_assertExportSendsPlanNotAnalysis` verifies only the plan crossed (allowlist) and every task carries provenance + OSLO Task ID.

## Simulated-AI / simulated-connector boundary

All analysis is timers + fixed illustrative data. The task tree, the graded inferences, the critical path, execution readiness, the two findings, and the Asana mapping are all **computed/seeded from state** (D173) — never authored on the fly. The Asana export is **simulated** (no network). Movement obeys D088 (the read moves only at an analysis update) and D003 (nothing reads as health) in every path. OSLO advises; the user decides (D001) — nothing crosses the export handoff without the user, and the export commits no read.
</content>
