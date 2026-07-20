# Slice 5 — Plan Artifacts / Artifact Workspace · Frontend / UI

Single openable HTML; dark default + light override on the same tokens (D015); WCAG 2.1 AA (focus-visible rings, keyboard operability, reduced-motion). No framework; plain JS + CSS variables. Colour discipline: severity **red/amber only** on weakness annotations + explorer badges (D003); the epistemic tags and the `low confidence` grade are **neutral chrome**, never severity or health colour.

> Regenerated to the frozen build (md5 `a327d702`). The Artifact Workspace is the **explorer (in the global sidebar) + a type-aware editor** — not the July-9 layout. **Boundary A:** the critical-path panel and the task model are rendered here but modelled in Slice 11.

## Layout

- **Explorer** — in the persistent left sidebar under **Plan artifacts**, subgroups **Understanding** / **Execution** (D093).
- **Editor pane** (`#pane-artifacts` / `.aw-pane`): a center column `#artCenter` holding the empty state `#artEmpty` and `#artView` (filled by `openArtifact`).

## The explorer — sidebar `Plan artifacts` rows

| Element | Selector / class | Notes |
|---|---|---|
| Subgroup label | `.sb-subgroup` | "Understanding" / "Execution" (D093) |
| Artifact row | `.sb-nav.sb-art` (`data-art`) | opens `openArtifact(name)`; active row lit via `_syncNav` |
| Open-issue badge | `.ex-fb` (`data-badge`) | `renderExplorerBadges`; `.crit` / `.mod` / `.warn` by most-severe open issue (D003); `.clear` (hidden) when none |

## The editor shell — `#artView` (`openArtifact`)

| Element | Selector / id | Notes |
|---|---|---|
| Empty state | `#artEmpty` (`.aw-empty`) | "Open a document to read and edit it" |
| Head | `.art-head` (`h1` + `.art-edit-badge` "✎ Editable" + `.info` + `.art-grp`) | layer label from `_artLayer` |
| Doc nav | `.art-nav` (`artStep(±1)`) | prev/next document; disabled at the ends |
| Version | `.art-layer.mono` | `v{_artVersion}`; bumps on commit |
| Weakness stepper | `#wnav` (`.wnav`) | see below |
| Editor actions | `.art-actions` (`artUndoBtn`·`artRedoBtn`·`artInsertBtn`·`artFindBtn`·`artAskBtn`) | undo/redo/insert/find + **✦ Ask OSLO** (D108) |
| Save/analysis chip | `#savestate` (`.savestate`) | dot + hover title only; states below |
| Save confirm | `#saveConfirm` (`.save-confirm`) | brief "Saved · vN"; fixed slot (opacity only, no reflow) |
| The document | `#artdoc` (`.doc`, `contenteditable`) | `oninput=onArtInput`, `onblur=commitArtEdit`; body `_artBodyLive` |
| Critical-path panel | `.cpath` (`_wbsCriticalPathHTML`) | **WBS view only, rendered AFTER `#artdoc`** — outside the editable doc, not editable |

## Autosave / reanalysis state chip — `#savestate` (D070 / D079)

| Class | Dot | Label (hover title) |
|---|---|---|
| `.ok` | success | "Analysis up to date" |
| `.saving` | subtle | (autosaving) |
| `.editing` | subtle | (calm typing) |
| `.stale` | warning | "analysis stale" |
| `.reana` | warning, **pulsing** (`sspulse`) | "Reanalyzing…" |

Conveyed by dot colour + title only — **no reflowing text block**, and **no manual reanalyze button** (D070). Pulse honours reduced-motion.

## Epistemic notation (D011 / D069 / D083)

| Element | Selector / class | Notes |
|---|---|---|
| Prose tag | `.epi-tag` (`.attested` when confirmed) | "From OSLO" / "Confirmed by you"; on `p`/`li`/`h3` |
| Cell reveal chip | `.cell-epi` (`.derived`/`.attested`, `data-epi-class`) | hover/focus per-cell chip; `contenteditable=false` |
| Row gutter dot | `.rowprov` (`.derived`/`.attested`) | glanceable per-row provenance |

Both classes single-sourced from `EPI_CLASSES` (D194b); **neutral/brand tints only — never severity colour as chrome** (D003).

## Weakness annotations + stepper (D068 / D071)

| Element | Selector / class | Notes |
|---|---|---|
| Weak span | `.anno[data-fid]` (`.editing`, `.wstep`) | severity ramp **red/amber only** (D003); wired to a real open issue |
| Hover summary | `.anno-pop` | one-line summary; suppressed while editing that span |
| Trailing marker | `.anno-mark` (⚠) | dropped when the issue resolves (`_artBodyLive`) |
| Stepper | `#wnav` (`.wnav-lab` · `.wbtn` ⌃/⌄ · `.wct`) | "Jump to issue ⌃ k of N ⌄"; "✓ No issues in view" when empty |

Click a span → the light issue panel (`openIssue`); **never resolved inline**.

## The Work breakdown task tree (DL-143→156 · 2A)

| Element | Selector / class | Notes |
|---|---|---|
| Outline number | `.wbs-n` | `1 · 1.1 · 1.3.1` |
| Task label | `.wbs-t` (`.wbs-h` for a workstream heading) | `data-lvl="0\|1\|2"` drives indentation; lvl-2 muted |
| Low-confidence grade | `.conf-low` | **neutral** dashed pill + `~` glyph; epistemic grade, **never** severity (D003) |

Rendered inside the standard `<table>` editor — all table chrome (`attachTableControls`, row/col controls, provenance) applies unchanged.

## Table editor chrome (shared engine, D075 / D081 / D084)

Row gutter with insert `+` / delete `×` + provenance dot; header top-insert `+`; per-column add/delete controls; whole-block drag grips; the Notion-style selection toolbar; the slash insert menu; find/replace; link popover; paste sanitization. Neutral tints only (a delete `×` may tint danger on hover — chrome, not severity data). The same engine drives the Reports readout (Slice 10) via `_EDIT_HOST` indirection; artifact-only surfaces (provenance, annotations, versioning, reanalysis) are gated off there.

## Color discipline (D003)

Explorer badges and weakness annotations use **severity red/amber**. Everything else — the epistemic tags/dots, the `low confidence` grade, the save/analysis chip, the critical-path panel, table chrome — is **neutral**. No health bars, no RAG on chrome. (The `#savestate` `stale`/`reana` warning tint is a workflow state, not plan severity.)

## Accessibility

- Explorer rows, doc nav, editor action buttons, stepper, row/column controls: `role="button"`/native buttons, `tabindex`, Enter/Space handlers, `aria-label`s.
- `#artdoc` is a labelled editable region; `#savestate` carries `aria-label`; provenance chips are `aria-hidden` decoration with the state in the row dot's `aria-label`.
- Focus-visible rings + reduced-motion inherited (the `reana` pulse and scroll-into-view respect reduced-motion). Colour is never the sole signal — provenance and the `low confidence` grade carry text.

## App shell (inherited)

Persistent left sidebar (Overview · Issues · History · Inference map · Reports · **Plan artifacts** [Understanding/Execution] · Full plan), top bar, command palette (⌘/Ctrl+K), chat rail. The Attention map and Issues panel route into the editor for a given artifact.
