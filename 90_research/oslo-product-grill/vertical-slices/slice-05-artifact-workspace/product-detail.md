# Slice 5 — Plan Artifacts / Artifact Workspace · Product Detail

**Scope:** the Artifact Workspace of the frozen R1 build (md5 `a327d702`) — the plan-artifact explorer and the type-aware artifact editor (prose + tables), with autosave, event-driven reanalysis, epistemic provenance, and the weakness stepper. Cumulative (Slices 1–5). Product behaviour only; no backend/API/DB.

> Regenerated to match the frozen build. This supersedes the July-9 slice-05 doc set. **Boundary A (2026-07-20):** Slice 5 owns the generic editor mechanics; the execution-planning task model (decomposition, `low confidence` semantics, critical path, Full-plan view, Asana export) is **Slice 11** and is cross-referenced, not re-documented, here.

---

## Component: The explorer (`.sb-subgroup` rows) — D066 · D093 · `renderExplorerBadges()`

- **Location:** the persistent global left sidebar (moved there under D093), under **Plan artifacts** split into two subgroups: **Understanding** (Intent · Context · Scope · Requirements) and **Execution** (Work breakdown · Schedule · Resources). Order is `_ARTORDER` = `['Intent','Context','Scope','Requirements','WBS','Schedule','Resources']`; `WBS` displays as **Work breakdown** (`dispName`).
- **Each row** (`.sb-nav.sb-art`) opens the artifact in the center editor (`openArtifact(name)`); the active row is lit (`_syncNav`).
- **Open-issue badge (`.ex-fb`, `renderExplorerBadges`):** count = `_artOpenIssues(art)` (ISSUES with `sec===art` and status ≠ resolved); colour = the most-severe open issue's severity (`crit` / `mod` / `warn`, D003). No open issue → `.ex-fb.clear` (hidden). Driven **live** from the ISSUES model, so resolving/opening issues re-colours it.

## Component: The editor shell (`#artCenter` / `#artView`) — D066 · `openArtifact()`

- **Empty state** (`#artEmpty`): "Open a document to read and edit it" until an artifact is opened; hidden thereafter.
- **Head** (`.art-head`): `dispName(name)` as `<h1>`; an **"✎ Editable"** badge; an info tip stating drafted From OSLO / type to edit → Confirmed by you / **saving changes NO assessment; only an analysis update does** / inline colours mark weak spots; the layer label `_artLayer(name)` ("Understanding core" for Intent·Context·Scope·Requirements, "Execution plan" otherwise).
- **Toolbar** (`.art-bar`): prev/next document (`artStep(±1)`, disabled at the ends); the version marker `v{_artVersion}`; the weakness stepper `#wnav`; editor actions (`artUndoBtn` · `artRedoBtn` · `artInsertBtn` · `artFindBtn` · **`artAskBtn` ✦** `askOslo({type:'artifact'})`, D108); the autosave/reanalysis chip `#savestate`; the brief `#saveConfirm` slot.
- **Document** (`#artdoc`): one always-live `contenteditable`, `oninput="onArtInput()"`, `onblur="commitArtEdit()"`, body from `_artBodyLive(name)`. **No edit mode, no Save button.**
- **On open**, `openArtifact` wires everything: `_seedTableProvenance` · `attachTableControls` · block grips + DnD · `updateWnav` · `renderExplorerBadges` · resets the per-artifact undo history. For the Work breakdown artifact **only**, the critical-path panel HTML is appended **after** `#artdoc` (outside it).

## Component: Type-aware bodies (`ARTBODY`) — D067

Understanding = prose (mixed with bullets/tables); Execution = tables. Annotation ids reference real open issues (ISS-01…11) so hover/click routes to the live issue.

| Artifact | Rendering | Notes |
|---|---|---|
| Intent | prose + a bulleted "What success looks like" list | goals as list items |
| Context | prose + a small **Stakeholders** table | mixed |
| Scope | flowing prose (In scope / Out of scope) | carries a Deep-Pass finding span |
| Requirements | prose + an **Acceptance** list | weak spans wired to issues |
| **Work breakdown (WBS)** | **authored graded task tree, as a `<table>`** | outline-numbered task tree — see below |
| Schedule | a **Milestone / Date / Status** table | statuses carry issue spans |
| Resources | two tables (Vendors & dependencies; People & speakers) | carries the critical + moderate feasibility issues |

## Component: Autosave + event-driven reanalysis — D070 · D073 · D076 · D079 · `onArtInput()` / `commitArtEdit()`

- **`onArtInput`** (every keystroke): immediately attests the touched block(s) (D069), refreshes the cell reveal + row dot (D083), keeps the empty-hint / link-popover / find in sync — then stays **silent** (no "Editing…"/"Saving…" chip) and **debounces** ~1500ms to `commitArtEdit`. Actively typing cancels the in-flight commit.
- **`commitArtEdit`** (typing-idle or blur): autosaves `#artdoc` innerHTML + bumps `art-{name}-ver` in local storage; writes a Slice-7 `artifact_version` History event; shows the brief "Saved · vN" confirm; then sets the state chip to **`reana` ("Reanalyzing…")** and after ~1500ms to **`ok` ("Analysis up to date")**.
- **State chip** (`#savestate`, `.savestate`) states: `ok` (success dot, "Analysis up to date") · `saving` · `editing` · `stale` (warning) · `reana` (warning, pulsing dot). Conveyed by **dot colour + hover title only** — no reflowing text (D079). **No manual "Reanalyze" button exists** (D070).
- **Structural edits** (row/column add·insert·delete, paste, format, slash-insert, undo/redo restore) all commit through the **same** `_commitFromStructuralEdit` → the same debounced Saved→stale→Reanalyzing→Up to date chain (`_finishNewRow`, etc.).
- **D088 (the key rule):** the edit firms the content immediately (Confirmed by you), but the **Outcome Confidence read does not move on the edit** — it catches up at the next analysis update. Saving changes no assessment; only reanalysis does.

## Component: Epistemic provenance — D011 / D069 / D083 / D194b

- **Prose** blocks (`p`/`li`/`h3`) carry a `.epi-tag` (`_epiTag`) reading **From OSLO** (derived) by default; editing flips it to **Confirmed by you** (attested) via `_attestSelectionBlocks` (adds `.attested` + `data-epi="attested"`). Both are **positive** states (D011/D069).
- **Table cells** carry `data-epi="derived"|"attested"`, surfaced by a **per-cell reveal chip** (`_ensureCellReveal`, `contenteditable=false`, appended last so it never joins the text run) and a **per-row gutter dot** (`_rowProvState` / `_refreshRowDot` — attested if any cell in the row is). `_seedTableProvenance` marks untouched OSLO cells derived on open; editing a cell flips it attested live (`_refreshCellForSelection` / `_refreshRowDotForSelection`).
- **One reader:** class names come from `EPI_CLASSES` via `epiClassName` (D194b) — no surface types its own label.
- **D196a — the per-item verb is Confirm.** Editing or accepting a cell/task *is* confirming it; this is the ratified confirm mechanism at **cell + task** altitude. **D173:** From OSLO marks an inference; it is never presented as fact.
- **Re-draft merge guarantee** (`redraftArtifact`, D084): attested blocks/cells are kept verbatim; only derived content is refreshed from OSLO's canonical draft. Prototype-grade positional matching; no fabricated numbers.

## Component: Weakness annotations + the weakness stepper — D068 / D071 / D074

- **Annotations** (`.anno[data-fid]`, `_a(...)`): the contiguous weak span is inline-coloured on a **severity ramp (red/amber only, D003)** and wired to a real open issue. Hover → a `.anno-pop` summary; click → the **light issue panel** (`openIssueFromAnno` → `openIssue`) — **never resolved inline**. "Ask about this" hands the span's issue to chat (`askAboutSpan`, D108).
- **Live-only render:** `_artBodyLive(name)` unwraps annotations whose issue is no longer open (dropping the span and its ⚠ marker), so resolving an issue removes its inline mark on the next render.
- **Stepper** (`#wnav`, `updateWnav` / `weaknessNav`, `curAnnos`): "Jump to issue ⌃ *k* of *N* ⌄" cycles the live annotations in `#artdoc`, scroll-into-view + `.wstep` highlight; "✓ No issues in view" when none. Scoped hard to `#artdoc` (D164) — the readout has no issues and no stepper.

## Component: The Work breakdown task tree — DL-143→156 · 2A (**edited here; modelled in Slice 11**)

- **Render:** the Work breakdown artifact is an **authored graded task tree** inside the standard `<table>` editor. Rows are workstreams (`.wbs-h`, `data-lvl="0"`) → tasks (`data-lvl="1"`) → subtasks (`data-lvl="2"`), each with an **outline number** (`.wbs-n`: `1 · 1.1 · 1.3.1`) and indentation by level. Columns: Task · Owner.
- **Every row is From OSLO** until confirmed (the table-provenance engine seeds all cells derived); the **thinnest inferences carry a neutral `low confidence` grade** (`.conf-low` — a dashed neutral pill with a `~` glyph and a "confirm these first" tip). **D003:** the grade is epistemic, **never** a severity colour.
- **Reuses the unchanged editor:** `attachTableControls`, `_seedTableProvenance`, row/column ops, autosave, and the reanalysis commit all apply unmodified. Confirming a task = the generic cell edit (D196a).
- **The critical-path panel** (`_wbsCriticalPathHTML`, rendered **outside** `#artdoc`): a From-OSLO "Sequencing & critical path" read, durations flagged `low confidence`, linked to the live undated-freeze finding. It is **not editable** in this view.
- **⛔ Boundary A:** the decomposition, the `low confidence` grading semantics, the critical-path computation (`_criticalPath`, `_assertCriticalPathComputed`), the consolidated **Full plan** view, and the **Asana export** are **Slice 11** (`slice-11-execution-ready-planning-export`). Slice 5 documents only that the tree is *carried and edited* here through the generic engine, and that the critical-path panel renders read-only outside the editable doc.

## Behaviour: one editor, host indirection (D164) — the shared engine

The generic mechanics (rich-text selection toolbar · formatting · undo/redo · slash menu · find/replace · link popover · paste sanitization · block grips + drag-reorder · keyboard) are addressed through `_EDIT_HOST` / `_edDoc()`, so the **same engine** also drives the Reports readout (a Slice 10 surface). What stays **artifact-only** (gated so it never leaks to a readout): epistemic provenance chips, weakness annotations + the stepper, artifact versioning, and the reanalysis commit (`_edIsArtifact()` gates; `_assertReadoutEditorProducesNothing`, `_assertNoArtdocHardcodeInSharedEditorPaths`, `_assertEditorHostFollowsTheView`).

## Non-goals / seams (do not build here)

The full Issues surface is Slice 6 (annotations route to the light panel — the seam stays). The execution task model, critical path, Full-plan view and Asana export are **Slice 11**. Artifact versioning surfaces on History (Slice 7). The readout editor is Slice 10. Real store / server / AI are out of scope (D016).
