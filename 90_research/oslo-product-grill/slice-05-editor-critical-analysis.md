# Slice 5 Artifact Editor — Critical Analysis & Feature-Gap Review
Date: 2026-07-09 · Scope: the Plan-Artifacts editor in `slice-05-artifact-workspace/prototype.html` (prototype, illustrative). Severity: **S1** blocks/derails · **S2** meaningful friction · **S3** polish. "Deferred" = owned by a later slice.

## What the editor does well (baseline)
Type-aware prose + tables with mixed content; a Notion-style floating rich-text toolbar (bold/italic/underline/strike/code, headings, lists, quote, link, indent); inline issue annotations with hover summary + ⚠ marker; epistemic provenance for prose (accent + hover) and now tables (row gutter dot + per-cell hover); quiet debounced event-driven reanalysis; table rows add/insert/delete/reorder; issue stepper; artifact explorer with live badges. This is a strong, on-doctrine base.

## S1 — High impact

1. **No reliable undo/redo.** There is no custom undo stack, and the editor mixes native typing with programmatic DOM edits (row insert/delete/**reorder**, annotation edits, provenance stamping, `execCommand` formatting). Native ⌘Z will not cleanly reverse the programmatic operations — deleting or reordering a row, or applying formatting, is likely **not undoable**, and undo may desync the DOM from the provenance/annotation state. For an editor users are asked to trust with their plan, this is the most serious gap. Needs a real command/history model (or at minimum an undo stack for structural ops).

2. **Reanalysis ↔ user-edit merge is undefined.** Editing is "Confirmed by you" and canon says attested content is preserved, but the prototype never demonstrates what happens when OSLO **re-drafts** an artifact (Extended Analysis / a later reanalysis) while the user has edited it. Are attested cells/sentences protected from being overwritten? Is there a merge/conflict surface? This is a core trust question for an AI-drafted, user-edited document.

## S2 — Meaningful friction

3. **Table cell navigation.** `Tab` only indents inside list items; inside a table it does the browser default (not cell→next-cell). Users strongly expect Tab/Shift+Tab and arrow keys to move between cells; its absence makes table entry slow.

4. **No table column operations.** Rows can be added/inserted/deleted/reordered, but **columns cannot** be added, deleted, reordered, or resized. Real plan tables need column edits.

5. **No paste handling / sanitization.** Pasting from Word, the web, or another doc into a `contenteditable` brings foreign markup and inline styles that can corrupt the clean theme, break annotation spans, and confuse epistemic tracking. No paste normalization exists.

6. **No block-level insertion / "/" menu.** The user can format existing text but cannot insert net-new blocks — a new table, a divider, a callout, an image, or an additional section — inline. Notion-style "/" insertion is absent; authoring is constrained to the drafted structure + list/heading formatting.

7. **Hover-only information is not keyboard/touch reachable.** Key signals — the annotation summary, the epistemic "From OSLO / Confirmed by you", the "how calculated" and reliability details — are revealed on **hover**. Keyboard and touch users can't reach much of this (some focus-within was added, but not uniformly). This is both an accessibility gap (WCAG) and a touch-device gap.

8. **Thin "what changed" feedback after reanalysis.** After an edit reanalyzes, in-editor feedback that the edit *addressed* a specific issue (or created/moved one) is minimal — the annotation may drop and a chat line appears, but there's no clear "your edit resolved *Venue Wi-Fi*" confirmation at the point of edit. Users improving the plan want to see their action land.

9. **Image / file / diagram embedding.** Cells and prose are text-only. Plans routinely reference floor plans, run-of-show diagrams, budgets — no way to embed or link a file/image.

## S3 — Polish

10. **No markdown input shortcuts** ("# ", "- ", "1. ", "> ") — toolbar-only formatting is slower for power users.
11. **No whole-block drag-reorder** — table rows reorder, but prose blocks/sections can't be dragged to reorder.
12. **No in-artifact find/replace** — long artifacts are hard to navigate/edit.
13. **Link management** — insert exists; editing/removing/previewing an existing link is unclear.
14. **Save assurance** — silent autosave (deliberate, D076/D079) plus no "unsaved changes"/navigation guard means a cautious user has little explicit confirmation their edit persisted; consider a quiet "saved ✓ vN" affordance on demand.
15. **Empty/placeholder states** — clearing an artifact or empty cells give no guidance/placeholder.
16. **Mobile/touch layout** — the floating toolbar, gutter controls (grip/insert/delete/provenance), and drag-reorder are untested on narrow/touch.

## Deferred (owned by later slices — flag, don't build here)
- **Version history / diff / revert** (the `vN` chip bumps but there's no view/compare/revert) → **Slice 7 (History & Timeline)**. Worth an explicit editor entry point when it lands.
- **Inline comments / @mentions on artifact text** → **Slice 9 (Collaboration & Sharing)**.

## Recommended priority
1. **Undo/redo + reanalysis-merge model** (S1) — trust-critical; sequence before build handoff.
2. **Table UX: cell Tab navigation + column ops + paste sanitization** (S2) — the table is a first-class surface and currently thin.
3. **Keyboard/touch reachability of hover-only info** (S2) — accessibility + touch.
4. **Block insertion / "/" menu + image embedding** (S2) — authoring completeness.
5. Polish (markdown shortcuts, find/replace, block drag, save affordance).

## Note
All of the above are **product/UX gaps in the prototype**; several (undo, merge semantics, paste, columns) are also engineering-realization questions. None changes ratified canon; the reanalysis-merge and image-embedding items may warrant an owner spec decision.
