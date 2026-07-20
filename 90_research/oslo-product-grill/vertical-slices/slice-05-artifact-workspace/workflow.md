# Slice 5 — Plan Artifacts / Artifact Workspace · Workflow

Cumulative (Slices 1–5). Actor workflows on the Artifact Workspace surface of the frozen build. Actors: **User** · **System** (client-side prototype render/state) · **AI** (simulated OSLO — timers + fixed illustrative data; no real model, no network).

> Regenerated to match the frozen build. Flows reference the current provenance/reanalysis model and the DL-143→156 Work-breakdown task tree. **Boundary A:** the task-model/critical-path/export flows are Slice 11's and are only pointed to here.

## Preserved end-to-end journey (INHERITED)

Invite → Activate → Welcome → Intake (4 methods) → **Fast Pass ≈30s** → land on the read-led Overview (Attention co-primary) → Outcome Analysis auto-runs, non-blocking → clarification loop closes issues via an analysis update. Completion notices in OSLO chat. Optional tour. The seven plan artifacts are drafted at intake (D035).

## Flow A — Open an artifact

1. **User** clicks a **Plan artifacts** row in the sidebar (or an Attention cell / issue that routes to the document).
2. **System** `openArtifact(name)`: fills the center editor from `_artBodyLive(name)`, lights the active sidebar row, sets the breadcrumb, seeds table provenance (`_seedTableProvenance`), attaches table + block controls, builds the weakness stepper (`updateWnav`), refreshes explorer badges, resets undo history. For **Work breakdown** only, appends the read-only critical-path panel after `#artdoc`.
3. **User** reads the draft; every block/cell shows its epistemic state (From OSLO by default); weak spans are inline-coloured.

## Flow B — Edit a sentence (prose block) → Confirmed by you

1. **User** clicks into a paragraph/list item and types.
2. **System** `onArtInput`: immediately attests the block (`_attestSelectionBlocks`) → its `.epi-tag` flips to **Confirmed by you** (D069/D011); stays silent (no "Editing…"/"Saving…"); debounces ~1500ms.
3. **System** `commitArtEdit` (on idle or blur): autosaves + bumps the version + writes a History event → the state chip runs **Reanalyzing… → Up to date**.
4. **AI** the analysis catches up at the update — the Outcome Confidence read may move **then**, never on the keystroke (D088). Editing changed the content, not the assessment.

## Flow C — Edit a table cell → Confirmed by you (D083 / D196a)

1. **User** clicks a body cell (e.g. an owner, a status, a WBS task) and types, or accepts it.
2. **System** flips that cell `data-epi="attested"`, refreshes its reveal chip (`_ensureCellReveal`) and recomputes the row's gutter dot (`_refreshRowDot`) → both read **Confirmed by you** live. Editing a cell **is** confirming it (D196a — the per-item verb is Confirm).
3. **System** debounces to the same Saved→Reanalyzing→Up to date commit as prose.

## Flow D — Restructure a table (add / insert / delete row or column)

1. **User** uses the row gutter (+ insert / × delete) or the column controls.
2. **System** snapshots undo, mutates the table, re-attaches controls + provenance (a **user-authored** row is Confirmed by you; a **new empty column** is From OSLO until typed), and runs the **same** debounced reanalysis via `_commitFromStructuralEdit`. No manual reanalyze.

## Flow E — Navigate weaknesses (D068 / D071)

1. **User** clicks the stepper "Jump to issue ⌃ *k* of *N* ⌄" (`weaknessNav`).
2. **System** scrolls the next live annotation into view and highlights it (`.wstep`).
3. **User** hovers a weak span → **System** shows the summary popover; **User** clicks it → **System** opens the **light issue panel** (`openIssueFromAnno` → `openIssue`) — never resolved inline. Resolving the issue (via the analysis update) drops its inline mark on the next render (`_artBodyLive`).

## Flow F — Open the Work breakdown task tree (DL-143→156)

1. **User** opens **Work breakdown** → **System** renders the authored graded task tree (workstreams → tasks → subtasks, outline-numbered), every row **From OSLO**, the thinnest inferences flagged neutral **low confidence** (D003), plus the read-only From-OSLO **Sequencing & critical path** panel below the editable doc.
2. **User** confirms a task by editing/accepting its cell (Flow C) → it flips Confirmed by you.
3. For the decomposition / critical-path / Full-plan / export semantics → **Slice 11** (`slice-11-execution-ready-planning-export`).

## Flow G — Ask OSLO about this document (D108)

1. **User** clicks **✦** in the toolbar (or "Ask about this" on a weak span).
2. **AI** the chat reports the artifact's epistemic basis + reliability honestly and links to the live issue. It mutates nothing and never claims to have edited or resolved anything.

## Flow H — Simulated re-draft (merge guarantee, D084)

1. **User** triggers **Sim OSLO re-draft** (demo).
2. **System** `redraftArtifact`: keeps every **Confirmed by you** block/cell verbatim, refreshes only **From OSLO** content, re-wires provenance/controls, and runs the quiet reanalysis; a chat line confirms the kept edits.

## Simulated-AI boundary

All analysis is timers + fixed illustrative data. Provenance, the reanalysis chain, and the weakness set are computed from live DOM state (D173) — never authored to look further along. Every path obeys **D088** (the read moves only at an analysis update; editing runs no assessment) and **D003** (severity colour on annotations/issues only; the `low confidence` grade is neutral).
