# Slice 5 — Plan Artifacts / Artifact Workspace · Success Criteria

The developer's checklist for the Artifact Workspace of the frozen build (md5 `a327d702`, boot 157/157). **FREEZE-INTACT:** these assert the build as frozen — not new enhancements. Refs name the governing doctrine / guard.

## Cumulative-integrity (no regression)
- [ ] SC-0 Every Slice 1–4 route, screen, interaction, theme token, and localStorage key still works (activation funnel, four-method intake, Fast Pass ≈30s, read-led Overview, CAF/grounding read + chip/popover, Attention map, chat + completion notices, tour, clarification loop, analysis-state machine).
- [ ] SC-0b The build boots green (157/157 guards) with no console error.

## The explorer (D066 / D093)
- [ ] SC-1 The seven plan artifacts appear in the persistent sidebar under **Plan artifacts**, grouped **Understanding** (Intent · Context · Scope · Requirements) and **Execution** (Work breakdown · Schedule · Resources); each row opens the artifact in the center editor. (`_ARTORDER` / `_artLayer` / `openArtifact`)
- [ ] SC-2 Each artifact's explorer badge shows its **live** open-issue count coloured by its **most-severe** open issue (critical/moderate/warning); an artifact with no open issue shows **no badge**. (`renderExplorerBadges` / `_artOpenIssues`; D003)

## The type-aware editor (D067)
- [ ] SC-3 Understanding artifacts render as **prose** (mixing a bulleted list or a small table where it reads better); Execution artifacts render as **tables**. (`ARTBODY`)
- [ ] SC-4 The document is **one always-live contenteditable** — no "edit mode", no Save button; you click and type. The head shows "✎ Editable", the layer label, and the info tip stating **saving changes no assessment**.
- [ ] SC-5 The toolbar carries prev/next document, the version marker (`vN`, bumps on commit), the weakness stepper, undo/redo/insert/find, **✦ Ask OSLO about this document** (D108), and the save/analysis chip.

## Epistemic notation — From OSLO / Confirmed by you (D011 / D069 / D083 / D196a / D173)
- [ ] SC-6 Every prose block and table cell shows an epistemic state — **From OSLO** (derived) by default; **From OSLO** is an inference, never presented as fact (D173). Both From OSLO and Confirmed by you are **positive** states (D011/D069).
- [ ] SC-7 Editing (or accepting) a prose block flips it to **Confirmed by you**; editing a table **cell** flips that cell's reveal chip and its row's gutter dot to **Confirmed by you** live. Editing an item **is** confirming it — the per-item verb is **Confirm** (D196a). This is the ratified confirm mechanism at **cell + task** altitude. (`_attestSelectionBlocks` / `_seedTableProvenance` / `_ensureCellReveal` / `_refreshRowDot`)
- [ ] SC-8 The class names come from one registry — no surface types its own label. (`EPI_CLASSES` / `epiClassName`; D194b)
- [ ] SC-9 On a simulated re-draft, **Confirmed by you** blocks/cells are preserved verbatim; only **From OSLO** content is refreshed. (`redraftArtifact`; D084)

## Autosave + event-driven reanalysis (D070 / D073 / D076 / D079 / D088)
- [ ] SC-10 Editing is **silent** while typing (no "Editing…"/"Saving…" churn); on ~1500ms idle or on blur it autosaves + versions, then the chip runs **Reanalyzing… → Up to date**. (`onArtInput` / `commitArtEdit`)
- [ ] SC-11 There is **no manual "Reanalyze" button anywhere**; reanalysis is event-driven. (D070)
- [ ] SC-12 **Saving changes no assessment** — the Outcome Confidence read moves **only at an analysis update** (D088), not on the keystroke. Editing firms the content (Confirmed by you) immediately, but the read catches up at the update.
- [ ] SC-13 The save/analysis state is conveyed by the chip's **dot colour + hover title only** (Up to date / Reanalyzing… / stale), with no reflowing text block. (D079)
- [ ] SC-14 Structural edits (row/column add·insert·delete, paste, format, slash-insert, undo/redo restore) run the **same** debounced commit as typing. (`_commitFromStructuralEdit`)

## Weakness annotations + stepper (D068 / D071 / D074 / D003)
- [ ] SC-15 Weak text is inline-coloured on a **severity ramp (red/amber only)** and wired to a real open issue; hover shows a summary; clicking opens the **light issue panel** — a weakness is **never resolved inline**. (`_a` / `openIssueFromAnno`; D003)
- [ ] SC-16 The weakness stepper cycles the **live** annotations in the open artifact ("Jump to issue ⌃ k of N ⌄"), highlighting each; only still-open annotations render (resolved marks drop on re-render); "✓ No issues in view" when none. (`updateWnav` / `weaknessNav` / `_artBodyLive`)

## The Work breakdown task tree (DL-143→156 · 2A) — edited here, **modelled in Slice 11**
- [ ] SC-17 The Work breakdown artifact renders as an **authored graded task tree** — workstreams → tasks → subtasks, **outline-numbered** (`1 · 1.1 · 1.3.1`), indented by level — inside the **unchanged `<table>` editor**, so all generic machinery (provenance, row/col ops, autosave, reanalysis) applies. (`ARTBODY.WBS` / `attachTableControls` / `_seedTableProvenance`)
- [ ] SC-18 **Every row is From OSLO** until confirmed; the thinnest inferences carry a **neutral `low confidence` grade** — an epistemic grade, **never a severity colour** (D003). Confirming a task = the generic cell edit (D196a). (`.conf-low`)
- [ ] SC-19 A From-OSLO **"Sequencing & critical path"** panel renders in the Work-breakdown view **outside** the editable `#artdoc` and is **not editable** here; its task-model/critical-path/export semantics belong to **Slice 11** and are not re-documented in Slice 5. (`_wbsCriticalPathHTML`; Boundary A)

## The shared engine boundary (D164)
- [ ] SC-20 The generic editor mechanics are shared with the Reports readout via host indirection, but the **artifact-only** surfaces — provenance chips, weakness annotations + stepper, versioning, and the reanalysis commit — are gated so they never leak into a readout. (`_edIsArtifact` gates; `_assertReadoutEditorProducesNothing` · `_assertNoArtdocHardcodeInSharedEditorPaths` · `_assertEditorHostFollowsTheView`)

## Cross-cutting
- [ ] SC-21 Advisory-only throughout (D001); OSLO drafts/explains, the calls stay with the user. Artifacts are **uncapped and never metered** (D128 P1).
- [ ] SC-22 Severity red/amber only on annotations + explorer badges (D003); all epistemic notation and the `low confidence` grade are neutral. Dark default + light parity; WCAG 2.1 AA (focus, keyboard, reduced-motion).
