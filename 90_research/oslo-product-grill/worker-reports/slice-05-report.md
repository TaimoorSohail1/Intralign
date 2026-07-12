# Slice 5 — Plan Artifacts / Artifact Workspace · Worker Report

**Date:** 2026-07-10 · **Status:** Built + self-verified · **Base:** signed-off Slice 4 prototype (extended cumulatively, nothing removed).

## Files created (`.../vertical-slices/slice-05-artifact-workspace/`)
- `prototype.html` — cumulative Slices 1–5 (base copied from slice-04, then extended).
- `user-experience.md` (INHERITED vs NEW), `product-detail.md`, `product-data.md` (PlanArtifact / Block / AnnotationSpan model), `workflow.md`, `frontend-ui.md`, `success-criteria.md`, `e2e-test-scenarios.md` (20 scenarios).
- This report.

## What's new vs Slice 4 (D066–D071)
- **Third co-primary view "Artifacts"** added to the top-center switch (Overview · Attention · Artifacts). Opens a two-column workspace (explorer + editor) inside the body column; chat rail preserved.
- **D066 Explorer:** 7 artifacts grouped Understanding / Execution, each with a **live open-issue badge** (count + most-severe color) driven from the real `ISSUES` data — refreshes on entry, on land, and on every issue-status change.
- **D067 Type-aware editor:** Understanding = prose by default with **mixed bullets/tables** (Intent prose+bulleted goals; Context prose+stakeholder table; Requirements prose+bulleted acceptance); Execution (Work breakdown/Schedule/Resources) = **tables**. Contenteditable; autosave to localStorage with version bump.
- **D068 Inline weakness annotations:** severity-colored (red/amber only) spans wired to the 6 real open issues; hover → summary; click → **light Issue panel**; never resolved inline. Resolving an issue **unwraps** its annotation on re-render.
- **D069 Epistemic notation:** blocks are "From OSLO" (hover chip) by default; editing flips the touched block to **"Confirmed by you"** with a left-border accent. Copy states saving changes no assessment; only reanalysis does.
- **D070 Event-driven reanalysis:** editing runs **Saving… → Saved · analysis stale → Reanalyzing… → Up to date** via simulated timers. **No manual reanalyze button** anywhere.
- **D071 Weakness stepper + artifact nav:** "Jump to weakness ⌃ k of N ⌄" cycles weak spans; ‹ / › move between artifacts (disabled at ends); both keyboard-operable. The **feature tour's artifact-edit step seam is filled** — the tour now opens the workspace on Resources and spotlights the real editor.

## Boundaries honored
- Severity color only on annotations/badges/issue panel; confidence/CAF neutral (D003). Advisory-only (D001). Terms: Plan artifacts (D049), Issues (D017), From OSLO / Confirmed by you (D011/D069), Clarity·Alignment·Feasibility. Dark default + keyboard-operable stepper/blocks (D015).
- Full Issues surface **not** built — annotations route to the light panel (Slice-6 seam preserved). History/version timeline stays a Slice-7 seam (version chip bumps only). Client-side only (D016).

## Verification
- **`node --check`** on the extracted `<script>`: **PASS** (no JS error).
- **jsdom runtime drive-through (all PASS):** third view activates; all 7 artifacts open; Intent shows prose+bullets and Context shows prose+table (D067 mixed); explorer badges live (Resources crit:2, Requirements mod:1, Intent clear); edit flips block to attested + starts the save chain; annotation click opens the issue panel (ISS-01); weakness stepper applies `.wstep`; artifact prev/next steps and disables at ends; WBS displays "Work breakdown"; **no manual reanalyze button**; answering a clarification resolves the issue → its annotation drops (2→1) and the badge updates (crit:2→mod:1).
- **Regression:** heatmap renders, Overview intact (idx 58), clarification/issue-panel flow intact.

## Flags (genuine spec gaps — not invented)
- **None blocking.** One minor scoped-exception note for the owner: the annotation set is wired to the 6 canonical open issues (ISS-01..06). The v4 mockup showed a larger illustrative finding set (FND-20xx) and a "v2 ▾" version affordance tied to History; here the version chip is a non-interactive `vN` bump because **History/versioning is a Slice-7 seam** — consistent with prior slices, flagged for continuity when Slice 7 lands.

---

## Revision 2 (2026-07-09)

Two editor-interaction fixes to the existing Slice-5 prototype (edit-in-place; no other slice regressed). `node --check` on the extracted `<script>`: **PASS**.

- **D073 — patient / debounced reanalysis.** `onArtInput()` no longer walks the Saving→stale→Reanalyzing→Up-to-date chain ~700ms after every keystroke. While the user types it only shows a calm **"Editing…"** state (new `.savestate.editing`) and (re)arms a debounce timer; it does **not** advance toward reanalysis. The commit chain (Saved autosave → analysis stale → Reanalyzing… → Up to date, existing ~1300ms/~1500ms stage timings preserved) is now run by a new `commitArtEdit()`, fired on **~1500ms typing-idle** OR on **`#artdoc` blur** (a new `onblur="commitArtEdit()"` handler = the natural "entry complete" signal, commits immediately if edits are pending). D069 block-attestation ("Confirmed by you") still fires immediately on input. Net: a single keystroke shows only "Editing…"; the reanalysis notification appears once, only after a pause or on blur.
- **D074 — annotated weak text is directly (partially) editable.** The `.anno` span no longer carries `contenteditable="false"` and no longer has a text-`onclick`; clicking now places the **caret** (`cursor:text`) so the user can edit part of the weak phrase in place (verified via jsdom: editing the middle text node changes only that portion). Flag styling (color + dotted underline) is retained. Issue reachability without clicking the text is preserved two ways: (a) a hover popover `.anno-pop` with the summary + a clickable **"Open issue →"** (`openIssueFromAnno(id)`), and (b) a tiny **non-editable ⚠ marker** `.anno-mark` immediately after the span (`contenteditable="false"`, `onclick="openIssueFromAnno(id)"`). Editing never resolves the issue inline — it only triggers the (now debounced) reanalysis; closure remains reanalysis-owned. When the caret enters an annotation, `.anno.editing` quietly drops that span's flag styling. `_artBodyLive()` unwrap on issue-resolve was updated to use the weak **text only** (strips `.anno-pop`, removes the trailing `.anno-mark` sibling).

**Verification (this revision).** `node --check` PASS. Static + jsdom checks confirm: outer `.anno` has no `contenteditable`/`onclick`; the ⚠ marker and popover link both call `openIssueFromAnno`; the weak text is its own editable text node (partial edit changes only that portion, marker stays separate). Docs updated: `frontend-ui.md`, `user-experience.md` (D073/D074 noted).

## Revision 3 (2026-07-09)

Inline-annotation **hover-UX** fixes to the existing Slice-5 prototype (edit-in-place; D074 editable-annotation behavior preserved; no other slice regressed). `node --check` on the extracted `<script>`: **PASS**.

Owner testing surfaced three problems: (1) two overlapping tooltips on hover — the custom `.anno-pop` popover AND browser-native `title` attributes on the `.anno` text span and its pieces; (2) the popover's "Open issue →" link was unreachable because the popover floated above the text with a dead gap that dropped `:hover` before the cursor arrived; (3) the ⚠ `.anno-mark` had a `display:none` rule fighting its visible rule, so it flickered inconsistently.

- **Single tooltip — native `title` removed from the weak text.** In `_a()` (`~1760`) the outer `.anno` span no longer carries any `title` attribute, and the inner `.anno-open` popover link's `title` was removed too. The **only** remaining native tooltip is a short `title="Open {dim} issue"` + matching `aria-label` on the tiny ⚠ marker (accessibility). Hovering the weak text now spawns exactly one tooltip source: the custom `.anno-pop`.
- **⚠ marker = persistent, clickable primary "investigate" affordance.** Repaired the `display:none` conflict: the combined rule `.anno.editing .anno-mark,.anno.editing .anno-pop{display:none}` was split so `.anno-mark` gets an explicit `display:inline` base rule (always visible next to a flagged span) and is only hidden inside `.anno.editing` (where the flag itself is dropped). Added a clear hover state (`opacity:1` + tinted `background`, `border-radius`, transition). It stays `onclick="openIssueFromAnno(id)"` — it never disappears and is the dependable path to the issue.
- **Popover made hover-STABLE via an invisible bridge (chosen approach).** The popover keeps its position above the text (`bottom:calc(100% + 6px)`) but a transparent pseudo-element `.anno-pop::before{position:absolute;top:100%;height:9px;left:0;right:0}` now spans the 6px gap down to the text. Because the bridge is a child of `.anno-pop`, the cursor never leaves a `:hover` region as it travels from the weak text up to the "Open issue →" link — there is no dead space, so the popover stays open and the link is reliably clickable. The show rule is a single combined selector `.anno:hover>.anno-pop,.anno-pop:hover{display:block}`. I chose the bridge over JS hover-intent because it is CSS-only (no timers, no new listeners), can't get out of sync, and needs no teardown on re-render/unwrap. The "Open issue →" link still calls `openIssueFromAnno(id)`; the ⚠ marker remains the dependable path so the link is a convenience.

**D074 preserved.** The `.anno` text span is still directly editable (`cursor:text`, no `contenteditable="false"`, no text-`onclick`) — clicking places the caret; entering it applies `.anno.editing`, which drops the flag styling and suppresses the popover (`.anno.editing:hover>.anno-pop{display:none}`). Issue closure remains reanalysis-owned.

**Verification (this revision).** `node --check` PASS. Confirmed: `.anno` text span has **no** `title`; ⚠ marker has explicit `display:inline` (always visible) + hover state + `onclick`; popover show rule includes the `::before` bridge so the "Open issue →" link is reachable; only one tooltip source on the weak text. Docs updated: `frontend-ui.md` (annotation hover section).

## Revision 4 (2026-07-09)

**D075 — add-row / delete-row controls on the structured Execution tables** (and the mixed Understanding tables). Edit-in-place on the existing Slice-5 prototype; D073 debounced reanalysis, D074 editable annotations, and the Rev-3 hover-popover fixes are all preserved; no other slice regressed. `node --check` on the extracted `<script>`: **PASS**.

Owner asked for a way to restructure the tables — previously cells were editable but rows could not be added or removed.

- **How add/delete are wired.** A new **`attachTableControls()`** runs at the end of `openArtifact()` (after `#artdoc` is rendered from `ARTBODY`, so controls are re-attached on every open and after every add/delete) and is **idempotent** — stamps are keyed on `.row-gutter` / `.row-del` / `[data-addrow]`, so switching artifacts or re-opening never duplicates a control. For each `<table>` it (a) inserts an empty leading **`th.row-gutter`** on the header row, (b) stamps a leading **`td.row-del`** with a keyboard-accessible **`×`** (`.rowdel`) on every `tbody` row via `_ensureRowDel()`, and (c) inserts a **"+ Add row"** affordance (`.addrow`) directly **after** the table.
  - **`awAddRow(tbl)`** appends a `<tr>` whose data-cell count matches the header (`th:not(.row-gutter)`); each new cell is `.attested` / `data-epi="attested"` = **Confirmed by you** (D069, user-authored) and carries a zero-width space so it's caret-placeable. The caret is moved into the first new data cell, the row gets its own `×` gutter, then the debounced commit runs.
  - **`awDeleteRow(tr)`** removes the row (and calls `updateWnav()` since the row may have carried an inline `.anno`).
- **Reanalysis (D073) — same debounced path.** Both add and delete call a new **`_commitFromStructuralEdit()`**, which mirrors `onArtInput()`'s steps 2–3: set `_pendEdit`, show the calm **"Editing…"** chip, clear in-flight timers, and (re)arm the **same ~1500ms debounce** → `commitArtEdit()`. So a structural edit follows the identical **Editing… → Saved · analysis stale → Reanalyzing… → Up to date** chain — debounced, **not** immediate on click. Verified via jsdom timing: after an add the chip reads "Editing…" at t=100ms, "Saved · analysis stale" at 1600ms, "Reanalyzing…" at 3000ms, "Up to date" at 4600ms.
- **Header protection.** The header row carries only the empty `th.row-gutter` (no `×`), and `awDeleteRow()` early-returns for any row inside `thead` — the header can't be deleted. jsdom confirmed: calling `awDeleteRow(headerTr)` is a no-op and the `<thead>` row stays present.
- **Keyboard access (D015 / WCAG).** Both controls are `role="button" tabindex="0"` with `aria-label`s ("Add a row to this table" / "Delete this row") and Enter/Space handlers (in addition to click). The `×` is revealed on `tr:hover`, `tr:focus-within`, or its own `:focus-visible`, so keyboard users can reach and see it.
- **Non-editable chrome, not prose.** Every control (`.addrow`, `td.row-del`, `th.row-gutter`) is `contenteditable="false"`, so it never enters the text run and is never counted as artifact prose/annotations (`curAnnos()` still selects only `.anno`).
- **Theme (D003).** Controls are neutral/muted; the `×` tints to `--danger` only on hover/focus (`rgba(199,91,91,.12)` bg) — severity color stays reserved for issues; the add affordance tints to primary on hover.
- **Annotated rows.** Deleting a row that held an inline issue annotation is allowed (restructuring) — not hard-blocked; the mark goes away with the row and reanalysis reconciles the issue set. jsdom confirmed deleting the Schedule/Resources annotation-bearing row succeeds.

**Verification (this revision).** `node --check` PASS. jsdom drive-through (all PASS): opening **Work breakdown / Schedule / Resources** shows a `.addrow` under each table (Resources has 2 tables → 2 affordances); clicking **+ Add row** appends a row with the correct column count (3 = header data cols), new cells attested, new row gets its own `×`; the savestate chip advances through the full debounced chain (not immediate); hovering a body row exposes the `×` which removes the row and re-runs the chain; the header row can't be deleted; controls are `contenteditable="false"` and `tabindex="0"`/`role="button"`; re-opening an artifact re-attaches exactly one add affordance + one header gutter (no duplication). Docs updated: `frontend-ui.md` (new D075 section), `user-experience.md` (D075 add/delete-row section).

## Revision 5 (2026-07-09)

Two editor changes to the existing Slice-5 prototype — **D077** (demote the epistemic tag to hover) and **D078** (Notion-like rich-text editing). Edit-in-place; D073/D076 quiet debounced reanalysis, D074 editable annotations + hover popover, and D075 table row add/delete all preserved; no other slice regressed. Client-side only. `node --check` on the extracted `<script>`: **PASS**.

### D077 — epistemic tag demoted from permanent chrome to hover (accent retained)
Owner found the persistent per-block tag ("From OSLO" / "Confirmed by you") excessive/distracting.
- **Accent kept, text demoted.** The attested **left-border accent** (`.doc p.attested{box-shadow:inset 3px 0 var(--primary)}`) is untouched, so the derived/attested state still reads at a glance. Only the `.epi-tag` **text** moved to hover: the former permanent `.epi-tag.attested{display:inline-block}` rule was removed, so **both** derived and attested tags default to `display:none` and are revealed only on `:hover` **or** `:focus-within` of the `p/li/h3` block (keyboard-accessible per D015). `pointer-events:none` + `z-index:4` keep the tag from eating clicks or fighting the annotation popover.
- **Saving≠assessment note kept on the hover.** A tiny `.epi-why` ⓘ inside the tag (`pointer-events:auto`) carries the tooltip "Saving your changes makes no assessment — only reanalysis does." (reuses the `.info`-style `::after` pattern).
- **Live flip on edit.** Block-attestation was refactored into **`_attestSelectionBlocks()`** (shared by typing and formatting): it adds `.attested` + `data-epi="attested"` and rebuilds the hover tag's `innerHTML` to "Confirmed by you" **preserving the ⓘ**. The accent updates the instant a block flips derived→attested; the D069 edit→attested behavior is otherwise unchanged.

### D078 — Notion-like rich-text editing
- **Formatting.** Bold + italic (⌘/Ctrl+B, ⌘/Ctrl+I); bullet + numbered lists; **indent / outdent** via toolbar buttons and **Tab / Shift+Tab** (only hijacked when the caret is inside an `<li>`, so table/plain-text Tab is unaffected).
- **Floating selection toolbar (how it's done).** A single body-level `position:fixed` `.rt-toolbar#rtToolbar` (dark/subtle, `role="toolbar"`, aria-labeled buttons carrying `data-cmd`). `initRichText()` (wired once on boot, idempotent) listens on `document` `selectionchange` → `_rtPosition()` centers the toolbar above the selection's `getBoundingClientRect()`, clamped to the viewport and flipped below if there's no room, and shows it only for a **non-empty** selection **inside `#artdoc`** (`_rtInDoc()`); it hides on empty selection, focus loss, artifact re-render, or a mousedown outside editor+toolbar. A `mousedown`→`preventDefault` on the toolbar keeps `#artdoc` focused and the selection intact when a button is clicked. `queryCommandState` lights active buttons (`.on`). `z-index:120` sits **below** the annotation popover so the two never fight.
- **List / indent (how it's done).** Actions map to `document.execCommand('bold'|'italic'|'insertUnorderedList'|'insertOrderedList'|'indent'|'outdent')` (prototype-grade — a real build maps to a proper rich-text model). CSS was added so `execCommand`-emitted `<ol>` uses native `decimal` markers and nested lists (from indent) use native `disc` + indentation, while the top-level drafted Understanding bullets keep their custom `•`.
- **Same debounced commit as typing (D073/D076).** `rtExec(cmd)` runs the command, then calls `_attestSelectionBlocks()` (block → Confirmed by you), `attachTableControls()` + `updateWnav()` (list restructuring can move `.anno` spans), sets `_pendEdit`, and (re)arms the **same ~1500ms debounce** as text edits → silent while editing, then Reanalyzing… → Up to date. No "Editing…"/"Saving…" churn.
- **Coexistence.** Verified formatting works inside table cells; `.anno` spans, their editability, popover, and ⚠ marker are untouched; `curAnnos()` still finds `.anno`; the epistemic accents (D077) are preserved; the floating toolbar never overlaps the annotation popover.

**Verification (this revision).** `node --check` PASS. jsdom drive-through — **29/29 checks PASS**: floating toolbar exists with all six commands; all new functions defined; opening an artifact renders `#artdoc`; `.epi-tag` base is `display:none` with **no** force-shown attested rule and both `:hover` + `:focus-within` reveal rules present ("From OSLO" text present in body, saving-note ⓘ present); `curAnnos()` still finds `.anno` with `data-fid` + `anno-mark` sibling; `_attestSelectionBlocks()` flips a derived block to attested (class + `data-epi`) with the hover tag rebuilt to "Confirmed by you" retaining the ⓘ; attested left-border accent CSS retained; `rtExec` runs without throwing and shows **no** Editing…/Saving… churn chip; ordered/nested-list + `.rt-toolbar` CSS present. A separate timing drive-through confirmed the full quiet chain after a format: stays "Up to date" (silent) → "Reanalyzing…" at ~1.6s → "Up to date" at ~3.3s. Docs updated: `frontend-ui.md` (Epistemic accent + hover tag D077, new Rich-text D078 section), `user-experience.md` (D077 hover demotion, new D078 rich-text section).

## Revision 6 (2026-07-09)

**D080 — expand + restyle the floating rich-text toolbar into a Notion-style selection (RTF) popup.** Edit-in-place on the existing Slice-5 prototype; the D078 show-on-selection mechanics and every other editor behavior are preserved — D073/D076/D079 quiet debounced reanalysis + dot indicator, D074 editable annotations + popover + ⚠ marker, D075 table row add/delete, D077 hover epistemic tag. Client-side only; prototype-grade `execCommand`. `node --check` on the extracted `<script>`: **PASS**.

Owner asked to make the toolbar resemble Notion's selection popup (more block/format options, grouped, restyled) while keeping it a light selection toolbar — not a full editor chrome.

### Final toolbar contents + grouping
A single rounded pill, left→right, with thin `.rt-sep` dividers between groups:
- **Turn into ▾** (dropdown `#rtTurnBtn` → `#rtTurnMenu`, `role="menu"`): Text (Paragraph) · Heading 1 · Heading 2 · Heading 3 · Bulleted list · Numbered list · Quote. Blocks → `formatBlock` (`p`/`h1`/`h2`/`h3`/`blockquote`); lists → `insert(Un)orderedList`. Trigger label reflects the current block; active menu item highlighted.
- **Inline:** Bold · Italic · Underline · Strikethrough · Inline code. Bold/italic/underline/strikeThrough via `execCommand`; **code** (`_code`) toggles a `<code>` wrap around the selection.
- **Link:** 🔗 button (`_link`) swaps the pill into an inline URL field (`#rtLinkInput` + Apply); Enter/Apply → `execCommand('createLink')` (bare host prefixed `https://`; Escape cancels + restores selection; no navigation).
- **Indent:** Outdent · Indent.

### Notion-like styling (themed to the dark app)
Single pill `~36px` tall on `--surface-2` / `--border-2` with a layered `box-shadow`, rounded `10px`; icon/label buttons with `--hover-tint` hover and a primary-tinted **active state** (`.on`); thin vertical dividers; the caret arrow now matches `--surface-2`. The Turn-into menu is a small elevated popup on `--surface-3` with per-item glyphs and an `.on` active row. No red/amber/green anywhere in the toolbar — severity color stays reserved for issues (D003); no color swatch was added (would have risked the severity-only-color doctrine).

### How it stays wired to the same edit path
`rtExec(cmd, arg)` now routes the pseudo-commands (`_block` → `_rtFormatBlock`, `_code` → `_rtToggleCode`, `_link` → `createLink`) and the direct `execCommand` marks, then runs the **identical** post-edit chain as before: `_attestSelectionBlocks()` (block → Confirmed by you), `attachTableControls()` + `updateWnav()`, `_pendEdit=true`, and the **same ~1500ms debounce** → `commitArtEdit()`. So every new action (turn-into, underline, strike, code, link) attests the touched block and flows through the **D079 dot-only** Reanalyzing… → Up to date indicator with **no** "Editing…"/"Saving…" churn and **no reflow**.

### Active-state + accessibility
`_rtSyncActive()` lights inline buttons from `queryCommandState`, the code button from `_rtInCode()`, and the Turn-into label + active menu item from `_rtCurrentBlock()`. Buttons carry `title`/`aria-label`; the dropdown is `aria-haspopup="menu"` + `aria-expanded`, focuses its first item on open, and closes on **Escape**. Shortcuts: **⌘/Ctrl+B / +I**, and **+U** added for underline; **Tab / Shift+Tab** indent/outdent only inside an `<li>`.

### Positioning
`_rtPosition()` unchanged for the normal case (centered above the selection rect, viewport-clamped, flips below when no room); in link-entry mode it anchors off a saved range (`_rtSavedRange`) so the pill stays put while the URL field is focused (the field is exempted from the toolbar's `mousedown`→`preventDefault`).

**Coexistence (verified).** `.anno` spans, their editability, popover, and ⚠ marker untouched; `curAnnos()` still selects only `#artdoc .anno`; the issue stepper (`updateWnav`) still counts them; D075 table controls (`.addrow`, `row-del`, `row-gutter`, all `contenteditable="false"`) unaffected; the D077 hover epistemic tag + attested accent preserved; toolbar `z-index:120` still sits below the annotation popover.

**Verification (this revision).** `node --check` PASS. jsdom drive-through confirmed: toolbar present with `.rt-groups` + **3 dividers**; Turn-into dropdown with **7** items (`p/h1/h2/h3` + `insert(Un)orderedList` + `blockquote`); inline+link+indent group buttons = `bold, italic, underline, strikeThrough, _code, _link, outdent, indent`; link URL field + Apply button present; new functions `_rtToggleCode/_rtFormatBlock/_rtCurrentBlock/_rtOpenLink/_rtApplyLink/_rtCloseMenus` all defined; `rtExec` handles `_block`/`_code`/`_link`; underline shortcut present; three `commitArtEdit` 1500ms debounces retained (typing + structural + rtExec); D079 dot logic (`savestate reana`→`savestate ok`) and `curAnnos()` untouched. Docs updated: `frontend-ui.md` (Rich-text section expanded to D080 + decisions header), `user-experience.md` (D080 selection-toolbar section + decisions header).

## Revision 7 (2026-07-09)
**Insert row anywhere on the structured tables (D081, extends D075).** The tables' "+ Add row" affordance previously only **appended** at the end. Owner asked for inserting a row at **any** position. Added, in place, preserving every existing editor behavior (D073/D076/D079 quiet debounced reanalysis + dot indicator, D074 editable annotations + popover + ⚠ marker, D075 row add/delete + header protection, D077 hover epistemic tag, D078/D080 rich-text toolbar).

### Per-row insert-after ("+") — insert-anywhere
- Each body row's leading gutter cell (`td.row-del`) now stacks **two** controls in a new `.rowctlwrap` column: an insert **`+`** (`.rowins`) above the delete **`×`** (`.rowdel`). Both are stamped by the existing idempotent `_ensureRowDel(tr)` pass, so re-opening/switching artifacts never duplicates them and every new row gets its own pair.
- Clicking the `+` (or Enter/Space) → `_insertRowAfter(tr)`: inserts a fresh `<tr>` **immediately after that row** in the same `tbody`, matching the table's column count, marked **"Confirmed by you"** (Attested, D069), caret dropped in the first new cell.

### Top insertion
- Chose the cleaner of the two options: a single **top-insert `+` on the header gutter** (`th.row-gutter`) rather than an "insert-above" control on the first body row. The header gutter carries **only** this `+` (never a `×` — the header stays non-deletable). Click/Enter/Space → `_insertRowAtTop(tbl)`, inserting the new row as the **new first body row**.

### Shared row-building (refactor)
- Extracted **`_makeRow(tbl)`** (builds the `<tr>` — column count from `th:not(.row-gutter)` with first-body-row fallback; each cell `.attested`/`data-epi="attested"` + zero-width space) and **`_finishNewRow(tr)`** (stamps gutter controls via `_ensureRowDel`, places caret in first new cell, runs the debounced commit). All three paths — `awAddRow` (bottom append, **preserved**), `_insertRowAfter`, `_insertRowAtTop` — now share these, so column count, attested marking, caret placement, and control re-attachment stay identical.

### Reanalysis wiring (D073/D076/D079)
- Every add/insert/delete funnels through `_commitFromStructuralEdit()` (via `_finishNewRow` for the row-adding paths) → the **same ~1500ms debounce** as text edits → Reanalyzing… → Up to date. **Silent while editing** (no "Editing…"/"Saving…" churn, D076); dot-only indicator (D079). No immediate churn on each click.

### Theming + accessibility (D003/D015)
- All controls `contenteditable="false"` (never enter the text run; `curAnnos()` still selects only `.anno`). The insert `+` tints to brand (`--primary-light`, `rgba(217,122,58,.12)`) on hover/focus; the delete `×` tints to `--danger` (`rgba(199,91,91,.12)`) on hover/focus — **never** severity red/amber/green as chrome. Both `role="button" tabindex="0"`, keyboard-operable (Enter/Space), revealed on `tr:hover` / `tr:focus-within` / `:focus-visible`.

### Coexistence (verified)
- `.anno` spans, their editability, popover, and ⚠ marker untouched; the issue stepper (`updateWnav`/`curAnnos()`) still counts every annotation; the D078/D080 rich-text toolbar and D077 hover epistemic tag + attested accent preserved; the bottom "+ Add row" still appends.

### Verification (this revision)
- `node --check` **PASS**.
- jsdom drive-through confirmed: header gutter shows an insert `+` and **no** delete `×`; each body row shows both `+` and `×`; `_insertRowAfter(row0)` inserts directly at index 1 (empty, **3** data cols matching the header, attested, own `+`/`×` controls, caret set, ~1500ms debounce fired) with the following row's data ("2a") still after it; `_insertRowAtTop` makes a new empty first row and pushes the old first data down one; `awAddRow` still appends at the end; `awDeleteRow` on the `thead` row is a no-op (header survives); `attachTableControls()` re-run is idempotent (one `.row-gutter`, one `.row-del` per row); `_makeRow` cell count == header data-col count; body-row delete still works.
- Docs updated: `frontend-ui.md` (Structured-table row-controls section → D075 · insert-anywhere D081 + decisions header) and `user-experience.md` (add/insert/delete section rewritten for D081 + decisions header + coexistence line).

---

## Revision 8 (2026-07-09)

**Scope:** D082 — add table row **reordering** (drag + keyboard) and make **top-insert discoverable** in the Slice-5 artifact editor. Extends D075/D081; edited `prototype.html` in place. All prior behavior preserved (D073/D076/D079 quiet debounced reanalysis + dot indicator, D074 editable annotations + popover, D075/D081 row add/insert/delete + header protection, D077 hover epistemic tag, D078/D080 rich-text toolbar).

### Part A — Row reordering (drag + keyboard)
- **Drag handle (`.rowgrip` ⣿):** added to each body row's gutter (`_ensureRowDel`), stacked **above** the insert `+` and delete `×` in `.rowctlwrap`. `draggable="true"`, `contenteditable="false"`, `role="button" tabindex="0"`, `aria-label="Reorder row — drag, or use Up and Down arrow keys to move"`, `title="Drag to reorder (or ↑/↓)"`. `cursor:grab`/`grabbing`; revealed on `tr:hover` / `:focus-within` / `:focus-visible`.
- **Drag-and-drop reorder (prototype-grade HTML5 DnD):** `_wireRowGrip` sets `dragstart` (records source row in module-level `_dragRow`, adds `.row-dragging` dim) and `dragend` (clears state + cues). `attachTableControls()` stamps **delegated** `dragover`/`dragleave`/`drop` on each `<tbody>` once (`data-dndwired` guard) via `_wireTbodyDnD`, so current and future rows are covered. `dragover` computes above/below by pointer `clientY` vs the row mid-line and paints a drop indicator (`.drop-before` = `inset 0 2px 0 var(--primary)` / `.drop-after` = `inset 0 -2px`); `drop` moves `_dragRow` to that slot **within the same `tbody` only** (never above the header — the header has no grip; the delegation ignores non-body targets). The whole `<tr>` moves, data + attested/`data-epi` state intact.
- **Keyboard move (WCAG):** with a handle focused, **↑/↓ (or Alt+↑/↓)** → `_moveRow(tr, ∓1)`, reparenting the row one position inside its own `tbody` (no-op at the ends; header never touched), then **keeps focus on the handle** (`grip.focus()` after the move).
- **After any reorder (`_afterReorder`):** `attachTableControls()` (idempotent re-attach) → `updateWnav()` (a moved row may carry an inline `.anno`) → `_commitFromStructuralEdit()` (same ~1500ms quiet debounce).

### Part B — Discoverable top-insert
- The header-gutter top-insert `+` (`th.row-gutter .rowins`) resting opacity raised **0 → .4** (faint but always visible) and brightens to full on `thead tr:hover` / `:focus-within` / its own `:hover`/`:focus-visible`; `title="Insert row at top"` tooltip kept. Header stays **non-deletable** (no `×`).

### Keep clean / theming (D003)
- Gutter now stacks **three** subtle controls (grip · `+` · `×`), all `contenteditable="false"`, keyboard-accessible. Hover tints: grip → `--text` (`--hover-tint` bg), `+` → `--primary-light`, `×` → `--danger`; drop indicator uses `--primary` — **never** severity red/amber/green as chrome.

### Reanalysis (D073/D076/D079)
- Reorders (drag + keyboard) and inserts funnel through `_commitFromStructuralEdit()` → same ~1500ms debounce → Reanalyzing… → Up to date. **No "Editing…"/"Saving…" churn**; dot-only indicator preserved.

### Coexistence (verified)
- `curAnnos()` still selects only `.anno`; the issue stepper re-counts after reorder; bottom "+ Add row" (append), per-row "+" (insert below), header "+" (insert top) all still work; D078/D080 toolbar + D077 hover epistemic tag intact.

### Verification (this revision)
- `node --check` **PASS** (single extracted `<script>` block, 108,961 chars).
- jsdom drive-through confirmed: every body row has grip (`draggable=true`, `contenteditable=false`, `role=button`, `tabindex=0`) + insert `+` + delete `×`; **ArrowUp** on the grip of row B (`A,B,C` → `B,A,C`) keeps focus on the grip; **ArrowDown** on A (`B,A,C` → `B,C,A`); **drag-drop** row A onto row B upper-half → `.row-dragging` on source at dragstart, `.drop-before` indicator on dragover, reorder to `A,B,C` with the A cell text moving intact, drop cues cleared afterward; header has **no** grip and **no** delete `×`; header top-insert `+` present with `title="Insert row at top"` and aria-label; savestate shows **no** Editing/Saving churn (`savestate ok`) after reorder; `curAnnos()` callable.
- Docs updated: `frontend-ui.md` (row-controls section → D082 grip/DnD/keyboard/discoverable-top-insert bullets + theming + decisions header) and `user-experience.md` (reorder + discoverable-top-insert prose + decisions header + coexistence line).

---

## Revision 9 (2026-07-09)

**Scope:** D083 — add **epistemic provenance to table cells** in the Slice-5 artifact editor (approved design — option 1). Tables must show whether content is **From OSLO** (Derived) or **Confirmed by you** (Attested) **without** borrowing the prose `.epi-tag` chrome (which stays reserved for `p`/`li`/`h3`). Edited `prototype.html` in place. All prior behavior preserved (D069 block attestation, D073/D076/D079 quiet debounced reanalysis + dot, D074 editable annotations + popover, D075/D081/D082 table row add/insert/delete/reorder + gutter controls, D077 prose hover epistemic tag, D078/D080 rich-text toolbar).

### Part A — Per-row provenance dot (primary glanceable signal)
- **`.rowprov` dot** added to each body row's gutter (`.rowctlwrap`, below the grip `⣿` / insert `+` / delete `×`), `contenteditable="false"`. **Muted `--subtle`** = **From OSLO** (every data cell in the row is derived); **brand `--primary-light`** (with a faint `rgba(217,122,58,.18)` halo) = **Confirmed by you** (the row has ANY attested cell). `title` + `aria-label="Row provenance: <state>"` reflect the row state.
- **State computed from the row's cells** (`_rowProvState(tr)`: attested if any `td:not(.row-del)` is `data-epi="attested"`/`.attested`, else derived). `_refreshRowDot(tr)` sets the dot class + title/aria idempotently.
- **Live flip on edit:** `onArtInput()` (which already attests the `td` via `_attestSelectionBlocks`'s `closest('p,li,td,h3')` set) now also calls `_refreshCellForSelection()` + `_refreshRowDotForSelection()`, so editing a cell flips that cell to attested and recomputes only that row's dot.
- **Add/insert:** `_makeRow` cells are attested (D069), and `_finishNewRow` now runs `_ensureCellReveal` on each new cell + `_refreshRowDot(tr)` → a newly added/inserted row's dot is **Confirmed by you**.
- **Reorder:** the dot lives inside the `<tr>`, so it travels with the row on drag/keyboard move; `_afterReorder()` also calls `_refreshAllRowDots()` to keep title/aria + chips in sync.
- **Seed on open:** `_seedTableProvenance()` (called in `openArtifact` before `attachTableControls`) marks every untouched drafted body cell `data-epi="derived"` so untouched OSLO cells count as **From OSLO**. A cell that only holds an inline `.anno` annotation is still OSLO-derived content → derived unless edited.

### Part B — Per-cell hover/focus reveal
- **`.cell-epi` chip** appended (last child, `contenteditable="false"`, `aria-hidden`) to each body data cell by `_ensureCellReveal(td)`; reveals **"From OSLO"** / **"Confirmed by you"** on `td:hover` **or** `td:focus-within` (keyboard-accessible). So a **single edited cell** inside an otherwise-OSLO row is identifiable — its chip reads Confirmed by you while sibling untouched cells read From OSLO. `pointer-events:none` + appended-last so it never joins the text run, isn't caught by `curAnnos()` (`.anno` only), and doesn't fight the inline annotation popover or the gutter controls. `title` reuses the "saving ≠ assessment; only reanalysis does" note (`_EPI_WHY`).
- **Optional standing cue:** a faint corner dot (`td.attested::after`, `--primary-light` @ .5 opacity) on attested cells — low-noise; the row dot stays the primary glanceable signal.

### Theming (D003) — neutral/brand only
- Provenance chrome uses **only** `--subtle` (muted) and `--primary-light`/`--primary` (brand). **Never** severity red/amber/green as provenance chrome — verified programmatically (no `crit`/`mod`/`warn`/`danger`/`warning` class on any `.rowprov`/`.cell-epi`). Severity color stays reserved for issues/annotations.

### Reanalysis (D073/D076/D079) — unchanged
- No new reanalysis path. Cell/row-dot refresh is immediate and cosmetic; the quiet debounced Saved→stale→Reanalyzing…→Up to date chain still runs via the existing `onArtInput`/`_commitFromStructuralEdit` (~1500ms) with **no "Editing…"/"Saving…" churn** — dot-only indicator preserved. jsdom confirmed savestate stays `ok` (silent) during typing, then `reana` → `ok` after the debounce.

### Coexistence (verified)
- `curAnnos()` still selects only `.anno` (never `.cell-epi`); the in-table `.anno` (e.g. WBS ISS-05) is intact; stepper, D078/D080 rich-text toolbar, and D075/D081/D082 gutter controls (grip/insert/delete) all untouched. `rtExec` also refreshes the cell chip + row dot after a format edit inside a cell.

### Verification (this revision)
- `node --check` **PASS** (single extracted `<script>` block, 114,508 chars).
- jsdom drive-through (open **WBS** Execution table): all 5 body rows show a provenance dot defaulting to **From OSLO**; every body cell seeded `data-epi` + carries a reveal chip labelled From OSLO (`contenteditable=false`); editing a cell flips **that row's** dot to **Confirmed by you** and the edited cell's chip to Confirmed by you while a **sibling untouched cell** stays From OSLO and an **untouched sibling row** stays From OSLO; **`awAddRow`** → new row dot + chip = Confirmed by you; **`_moveRow`** carries the (attested) dot with the row; `curAnnos()` count unchanged and excludes `.cell-epi`; in-table annotation still present; savestate dot-only (no text) during edit; provenance chrome uses **no** severity class.
- Docs updated: `frontend-ui.md` (new "Table-cell epistemic provenance (D083)" section + decisions header) and `user-experience.md` (new D083 subsection + decisions header + coexistence line).

## Revision 10 (2026-07-09)

**Scope:** D084 — **Editor gap fold-in, Batch A** (trust + table core). Five prototype-grade additions to the Slice-5 artifact editor, edited in `prototype.html` in place. **All prior behavior preserved** (D073/D076/D079 quiet debounced reanalysis + dot; D074 editable annotations + popover + ⚠ marker; D075/D081/D082 table row add/insert/delete/reorder + gutter controls; D077 prose epistemic hover; D078/D080 rich-text toolbar; D083 table provenance row-dot + per-cell hover). All new controls are `contenteditable="false"`, keyboard-accessible, theme-consistent, and neutral/brand tints only (never severity color as chrome, D003).

### 1 — Undo / redo (snapshot history)
- Per-artifact `#artdoc` **innerHTML snapshot** stacks (`_undoStacks`/`_redoStacks`, cap 50), reset per open (`_resetHistory` in `openArtifact`). `_pushUndo()` snapshots **before** each structural op — `awAddRow`, `_insertRowAfter`, `_insertRowAtTop`, `awDeleteRow`, `_moveRow`, the drag-drop `drop` handler, `awAddColumn`, `awDeleteColumn`, `onArtPaste`, `rtExec` — and **coalesced typing** (one snapshot per idle burst via a `_needTextSnapshot` flag captured on the first content keydown, re-armed when `commitArtEdit` fires).
- `_restoreSnapshot` sets innerHTML, then re-runs `_seedTableProvenance` + `attachTableControls` + `_refreshAllRowDots` + `updateWnav` (controls/provenance/stepper re-attach) and the quiet `_commitFromStructuralEdit`. `_restoringSnapshot` guard blocks re-entrant pushes/commits. Keys: `⌘/Ctrl+Z` undo · `⌘/Ctrl+Shift+Z` / `Ctrl+Y` redo; clamp at ends; new edit clears redo.

### 2 — Reanalysis-merge preservation (`redraftArtifact(name)`)
- Wired to phase-bar demo trigger **`#redraftBtn` "Sim OSLO re-draft"**. Attested (`.attested`/`data-epi="attested"`) blocks + cells are kept **verbatim**; derived blocks/cells are refreshed from a fresh `_artBodyLive(name)` OSLO draft (positional match; derived cell keeps its `.cell-epi` chip, stays `derived`). **No fabricated numbers.** Then re-seed provenance/controls/stepper + quiet reanalysis; a quiet chat line confirms "Re-draft complete — your confirmed edits were kept."

### 3 — Table cell navigation
- `_tableCellNav`: **Tab** → next data cell, **Shift+Tab** → previous, wrapping rows; at the last cell of the last row Tab **appends a new row** (`awAddRow`, caret in first new cell); very-first-cell Shift+Tab stays put. `_tableCellVert` + `_caretAtCellEdge`: **Arrow Up/Down** move to the cell above/below in the same column at a cell edge. Table check runs **before** the list-indent branch, so **Tab still indents inside `<li>`** (unaffected).

### 4 — Table column operations
- `_ensureColControls(tbl)` (called from `attachTableControls`) stamps a `.colctl` on each non-gutter `<th>` with a brand-tinting **"+" (add column right)** + danger-hover **"×" (delete column)**, revealed on header hover/focus, keyboard-accessible. `awAddColumn`/`awDeleteColumn` update the header + **every** body row; new column cells are **`data-epi="derived"`/empty** (structure, not an authored fact — attests when typed; noted as the chosen convention). Both push undo, re-attach controls + provenance, run the quiet debounced reanalysis. (Column reorder/resize deferred to a later batch — higher-risk polish.)

### 5 — Paste sanitization
- `onArtPaste(e)` (delegated `paste` on `document`, gated to `#artdoc`) → `_sanitizePastedHTML` rebuilds the tree with an allowlist (`b/strong/i/em/u/br/p/div/ul/ol/li/h1/h2/h3/code`), **drops ALL attributes** (styles/classes/ids/handlers) + `script/style/link/meta`, unwraps disallowed tags. **Paste into a table cell → plain text** (stays in the cell). Then attest touched block + re-attach controls/provenance + quiet reanalysis. Nothing injected can break `.anno`, epistemic classes, or the theme.

### Prototype-grade caveats
- Undo/redo is a **snapshot** history, not a document/diff model (text undo coalesces to block/idle boundaries, not per-word). Re-draft matches blocks/cells **by position** (not a real semantic merge). Arrow Up/Down cell-edge detection is a **client-rect heuristic** (behaves in a real browser; jsdom returns zero rects so only Tab-nav is auto-tested). Column reorder/resize not built. All noted as production would use a proper editing/document model.

### Coexistence (verified)
- `curAnnos()` still selects only `.anno` (never `.colctl`/`.cell-epi`); the in-table annotation (Resources ISS-01/ISS-03, WBS ISS-05) survives a delete→undo (2→1→2). Weakness stepper, D078/D080 rich-text toolbar, D075/D081/D082 gutter controls, and D083 provenance dot/chip all re-attach after undo/redo/column ops. Savestate stays **dot-only** (no "Editing…/Saving…" text) through structural edits.

### Verification (this revision)
- `node --check` **PASS** (single extracted `<script>` block, 137,567 chars).
- jsdom drive-through: **undo/redo** reverses & re-applies a row delete (5→4→5→4, first-cell text matches; gutter/prov-dot/addrow present after undo) and a column add+delete (3→4→3, all rows keep matching cell count; undo/redo walk cols correctly); **re-draft** keeps an attested prose block verbatim while a tampered derived block is refreshed away; **Tab** moves cell0→cell1 and appends a new row at the last cell (5→6 rows), Shift+Tab at the first cell is a safe no-op; **paste** of `<p style… onclick… class…><script>…` yields `<p>Hi <b>bold</b> styled</p><div><ul><li>a</li></ul></div>` (no `style`/`class`/`onclick`/`script`; `<b>`/`<ul>`/`<li>`/text kept); annotations found only via `.anno`; savestate dot-only during edits.
- Docs updated: `frontend-ui.md` (new "Editor gap fold-in — Batch A (D084)" section + decisions header) and `user-experience.md` (new Batch A subsection + decisions header).

## Revision 11 (2026-07-09)
**Editor gap fold-in — Batch B (D084): authoring + accessibility.** Five more prototype-grade additions folded into `slice-05-artifact-workspace/prototype.html` in place. All existing behavior preserved (D073/D076/D079 quiet debounced reanalysis + dot; D074 annotations/popover/⚠; D075/D081/D082 table row add/insert/delete/reorder; D077 prose epistemic hover; D078/D080 rich-text toolbar; D083 table provenance; and **Batch A** undo/redo/`_pushUndo`/`_restoreSnapshot`, re-draft, cell nav, column ops, paste sanitize). Every new insertion routes through `_pushUndo()` (undoable) and the quiet `_commitFromStructuralEdit()` reanalysis (no "Editing…/Saving…" churn). New controls/menus are `contenteditable="false"`, keyboard-accessible, theme-consistent, neutral/brand tints only (never severity color as chrome, D003).

### 1 — Block insertion: "/" slash menu
- `#slashMenu` (`role="listbox"`, ce=false) opens near the caret when `/` is typed at block start (or after whitespace), detected in `onArtInput` → `_syncSlashFromInput()`. Items: **Text · Heading 1/2/3 · Bulleted list · Numbered list · Quote · Divider (`<hr>`) · Table · Image · File.** Type-to-filter (`_slashFiltered`), **↑/↓** navigate, **Enter/click** insert (`_slashChoose`), **Esc** close; the menu owns those keys while open (intercepted before editor shortcuts). Suppressed inside a table cell.
- `_slashChoose` pushes undo, strips the "/query" text (`_stripSlashText`), inserts (`_slashInsert` — turns the current empty block via `formatBlock`/list when possible, else inserts a new top-level block), attests it (`_attestNewBlock`), re-seeds provenance + `attachTableControls` + `_attachBlockGrips`, places caret, quiet reanalysis.
- **Table** (`_makeDefaultTable`) = default **3×3** (header + 2 body rows, cells attested) that **immediately** gets full controls (gutter grip/insert/delete, `.colctl`, provenance dots/chips, cell nav) via `_seedTableProvenance()`/`attachTableControls()`/`_refreshAllRowDots()`.

### 2 — Image / file embedding
- Slash **Image** (`_slashInsertImage`): prompt for a URL, or (blank) open a hidden `#embedFileInput` and **FileReader → data URL** (`_wireEmbedInput`). Inserts a themed `<img>` (max-width, rounded, bordered) in a `<figure class="embed" contenteditable="false" data-epi="attested">` with an editable `<figcaption>` + a keyboard-accessible remove control (`.embed-x`). A trailing empty `<p>` is guaranteed after the figure. Slash **File** = a generic `.filechip` (icon + name + size) for non-images. **No upload/backend** (data URL / picker only). `_removeEmbed` deletes it (undoable, quiet reanalysis).

### 3 — Keyboard/touch reachability of hover-only info (a11y, D015)
- `_wireA11yReveals()` (delegated on `#artdoc`) makes hover-only surfaces reachable by **focus + click/tap** without disturbing hover. **Annotation:** `:focus-within` reveals `.anno-pop`; the ⚠ marker on focus/Enter adds `.anno-peek` (stays open if focus enters the "Open issue →" link); **tap** reveals the summary on first tap, a second tap / the link opens the issue. **Epistemic:** tap a prose block or body cell toggles `.epi-peek` (reveals "From OSLO / Confirmed by you"); Esc + click-away clear peeks. CSS: `.anno:focus-within>.anno-pop`, `.anno.anno-peek>.anno-pop`, `.epi-peek>.epi-tag`, `td.epi-peek>.cell-epi`.

### 4 — Markdown input shortcuts
- `_tryMarkdown()` (first in `onArtInput`): at block start, the trigger space applies `# `→H1, `## `→H2, `### `→H3, `- `/`* `→bullet, `1. `→numbered, `> `→quote, `--- `→divider (`_MD_RULES`). Reads the block's typed text excluding grip/epi chrome + zero-width, strips the trigger, applies the `formatBlock`/list command (or direct `<hr>`), attests, quiet reanalysis; one undoable step (`_pushUndo`). **Never fires inside a table cell or a code span** (`_mdActiveBlock` guards).

### 5 — Whole-block drag-reorder
- `_attachBlockGrips()` stamps a **⣿ handle** (`.blk-grip`, draggable, `role="button" tabindex="0"`, ce=false) on every top-level block (`p/h1-3/ul/ol/blockquote/table/figure`), mirroring the row grip. Valid host per content model: **table → `<caption>`**, **ul/ol → first `<li>`**, else the block; `hr` moves via neighbours (no child grip). Mouse: HTML5 drag-drop (`_wireBlockDnD`, delegated) with above/below drop indicator (`.blk-drop-before/after`). Keyboard: focus handle + **↑/↓** (`_moveBlock`). After reorder (`_afterBlockReorder`): re-seed provenance + `attachTableControls` + `_refreshAllRowDots` + `_attachBlockGrips` + `updateWnav` + push undo + quiet reanalysis. **Table-internal row reorder (D082) untouched** — whole top-level blocks only. `_restoreSnapshot` also re-runs `_attachBlockGrips` so grips survive undo/redo.

### Prototype-grade caveats
- The "/" menu + markdown map to the **same in-browser `document.execCommand`** (`formatBlock`/lists) as the existing toolbar — jsdom no-ops execCommand, so those transforms were verified with an execCommand shim (all pass); the pure-DOM divider path fires even in jsdom. Images/files are **in-browser data URLs / picker only** (no upload/backend). Block drag-reorder is a **snapshot-backed move**, not a document model. The grip glyph `⣿` lives in an `ce=false` chrome span; text-detection helpers (`_blockText`, `_tryMarkdown`) strip it + zero-width so it never pollutes markdown/slash/attest logic. A production build would use a proper editing/document model + real asset storage.

### Coexistence (verified)
- `curAnnos()` still selects only `.anno` (never `.blk-grip`/`.slash-menu`/`.embed`); the Context annotation (ISS-06) survives, stepper renders. RTF toolbar (`rtExec`), table controls/column ops/cell nav, D083 provenance, and paste sanitization all intact. Slash insertion of a table yields the full control set (thead th + `.colctl` + `td.row-del` gutters + `.rowprov` dots + `.addrow`). Insertions are **undoable** (`artUndo` removes a slash-inserted table; markdown H3 undo restores prior). Savestate stays dot-only through Batch B edits (no "Editing…/Saving…").

### Verification (this revision)
- `node --check` **PASS** on the single extracted `<script>` block.
- jsdom drive-through: **/** opens the menu and **filters** ("head" → h1/h2/h3; all → 11 items); **slash inserts each block type** incl. a **fully-controlled 3×3 table** (thead th=4 with colctl, 2 body rows, 2 row-del gutters, addrow, 2 rowprov dots, 3 colctl) and an **image figure** (img src, editable caption, remove control, `ce=false`, attested); **markdown** `# `/`## `/`### `/`1. `/`> `/`- `/`* `/`--- ` all fire and transform (execCommand shim) and are **undoable**, and **do NOT fire inside a table cell**; a prose block **drag/keyboard-reorders** (`_moveBlock` swaps first↔second); **undo** removes a slash-inserted table; **a11y** tap on the ⚠ marker adds `.anno-peek` and tap on a block toggles `.epi-peek`; `curAnnos()`/stepper/`rtExec`/`attachTableControls`/`_pushUndo` intact.
- Docs updated: `frontend-ui.md` (new "Editor gap fold-in — Batch B (D084)" section) and `user-experience.md` (new Batch B subsection).

## Revision 12 (2026-07-09)
**Editor gap fold-in — Batch C (D084): polish.** Five prototype-grade polish additions folded into `slice-05-artifact-workspace/prototype.html` in place. All existing behavior preserved (D073/D076/D079 quiet debounced reanalysis + dot; D074 annotations/popover/⚠; D075/D081/D082 table row add/insert/delete/reorder + column ops + cell nav; D077 prose epistemic hover; D078/D080 rich-text toolbar + link creation; D083 table provenance; **Batch A** undo/redo/`_pushUndo`/`_restoreSnapshot`/re-draft/paste-sanitize; **Batch B** slash menu/image embed/a11y reveals/markdown shortcuts/block drag). Every new edit routes through `_pushUndo()` (undoable) + the quiet `_commitFromStructuralEdit()`/`commitArtEdit()` reanalysis (no "Editing…/Saving…" churn). New UI is `contenteditable="false"`, keyboard-accessible, theme-consistent, neutral/brand tints only (never severity color as chrome, D003).

### 1 — In-artifact find / replace
- `#findBar` (`role="search"`, ce=false) docks top-right of `.aw-center` (now `position:relative`). **⌘/Ctrl+F** opens it (`openFind`, guarded to an open artifact; intercepted in the `#artdoc` keydown handler). Fields: **find**, live **count** (`#findCount`), **prev/next** (`findStep`), and a **replace** field with **Replace** (`findReplaceCurrent`) / **Replace-all** (`findReplaceAll`).
- `_runFind()` walks **safe text nodes** of `#artdoc` (skipping chrome via `_FIND_SKIP`: grips, epi tags, cell reveals, `.anno-pop`/`.anno-mark`, row/col controls, add-row, provenance dots, captions) and wraps matches in **non-destructive `<span class="find-hit">`** (brand tint; current = `.find-current`). **Esc/×** closes and `_clearFindHighlights()` **unwraps every `.find-hit` + `normalize()`s** so annotations/epistemic spans/caret are never corrupted. Highlights are also cleared **before** any typing snapshot (keydown `_isFindOpen()` guard) and re-run in `onArtInput`. Replace/Replace-all swap the hit text, push undo, attest touched block(s), `updateWnav()`, quiet reanalysis, re-highlight.

### 2 — Link edit / remove
- `#linkPop` (`role="dialog"`, ce=false) surfaces near an existing content link on `selectionchange` → `_linkPopSyncFromSelection()` → `_currentLinkAnchor()` (`#artdoc a:not(.anno-open)` **with href** — the annotation popover's "Open issue →" `a.anno-open` is excluded so it's never mistaken for a content link). Shows the **URL** + **Edit / Remove / Open ↗**. **Edit** (`_linkEditApply`) updates the `href` (normalizes bare domains → `https://`), pushes undo, attests, quiet reanalysis. **Remove** (`_linkRemove`) unwraps the `<a>` keeping the text (undoable, `updateWnav`, quiet reanalysis). `mousedown` suppressed (except the URL field) so controls never collapse the selection; repositions on scroll/resize; Esc / click-away dismiss. A benign reference link seeded in the **Context** artifact makes it demonstrable out of the box.

### 3 — Explicit save confirmation (opt-in)
- Silent autosave (D076/D079) stays the default. `commitArtEdit()` now calls `_showSaveConfirm()` → fills a **fixed reserved slot** in the toolbar (`#saveConfirm`, `aria-live="polite"`) with **"Saved · vN · just now"** for ~2s then fades — **only opacity animates, no reflow**. No "Editing…/Saving…" reintroduced.

### 4 — Empty / placeholder states
- Per-block placeholders are **pure CSS** `:empty::before` (p/h1-3/blockquote/li hints; empty `td` → "—"; `figcaption:empty` reuses the existing caption hint), all `pointer-events:none; user-select:none`, vanishing on input. A **fully-empty artifact** gets a centered nudge (`#artdoc.doc-empty::after`, pointing at "/"). `_refreshEmptyState()` toggles `.doc-empty` (text + structural-child check) on open, input, and commit.

### 5 — Mobile / touch + responsive pass (~380px)
- Touch (`@media (hover:none),(pointer:coarse)`): gutter grip/insert/delete, column add/delete, block grips, embed remove get **reveal-on-focus + larger hit targets**; RTF-toolbar buttons + slash rows grow to tap size. Floating surfaces (`_rtPosition`/`_positionSlash`/`_positionLinkPop`) already clamp to the viewport; `@media(max-width:640px)` adds `max-width:calc(100vw-16px)` + `flex-wrap` so they never overflow. **Two-column collapse:** at ≤640px the explorer becomes a **"☰ Artifacts" drawer** (`.aw-explorer-toggle` → `toggleExplorer()`, `aria-expanded`); picking an artifact auto-closes it (`_collapseExplorerOnNarrow`). At ≤760px the chat rail collapses to its tab. Header/bar/doc/find-bar go full width.

### Prototype-grade caveats
- Find matches **within a single text run** (prototype-grade; no cross-node/regex search), highlighting via a **removable wrapper** rather than a search index. Link creation still relies on the existing `document.execCommand('createLink')` toolbar path (jsdom no-ops execCommand); the Context artifact ships a seeded `<a>` so edit/remove is exercisable directly. Save confirmation + placeholders are **presentation-only**. The responsive layout is **CSS breakpoints + a drawer toggle**, not a separate mobile build. A production build would use a proper search + document model and a responsive design system.

### Coexistence (verified)
- `curAnnos()` still selects only `.anno` (never `.find-hit`/`.link-pop`/drawer chrome); the Context annotation (ISS-06) survives, stepper renders. RTF toolbar (`rtExec`), table controls/column ops/cell nav, D083 provenance, undo/redo (`_pushUndo`/`_restoreSnapshot`), the slash menu, and paste sanitization all intact. Find highlights are stripped before undo snapshots + typing so the undo history and edited DOM stay clean. Replace/link-remove attest the touched block(s) and reanalyze quietly (dot-only; no "Editing…/Saving…").

### Verification (this revision)
- `node --check` **PASS** on the single extracted `<script>` block.
- jsdom drive-through (**26/26 assertions pass**): ⌘F opens the bar; find **highlights** matches (4 for "sponsor" in Context) with a **count** ("1/4") and **next** advances the current match; **Replace** edits text and **preserves annotations**; **Replace-all** runs; **closing find clears every `.find-hit` cleanly**. An existing link shows the **popover with its URL**; **Edit** updates the href and **Remove** unwraps the `<a>` keeping its text. The **"Saved · vN · just now"** confirmation shows after a commit (reads `Saved · v3 · just now`). A fully-empty `#artdoc` gets `.doc-empty`; it clears when content is present. `toggleExplorer()` opens/closes the drawer. `curAnnos()`/stepper/`weaknessNav`/`_slashChoose`/`redraftArtifact`/`_pushUndo` intact.
- Docs updated: `frontend-ui.md` (new "Editor gap fold-in — Batch C (D084)" section + decisions line) and `user-experience.md` (new Batch C subsection + decisions line).

## Revision 13 (2026-07-09)
**Visible editor-action toolbar (D085): discoverable keyboard actions.** Added a small, subtle `.art-actions` button group to the artifact toolbar (`.art-bar`) in `slice-05-artifact-workspace/prototype.html` so the previously keyboard-only editor actions are discoverable. All existing behavior preserved (D073/D076/D079 quiet debounced reanalysis + dot; D074 annotations; table controls + provenance; D078/D080 rich-text toolbar; D084 Batch A undo/redo, Batch B slash menu/embeds/markdown/block-drag, Batch C find/replace, link popover, save confirmation, empty states, responsive). New chrome is `contenteditable="false"`, keyboard-accessible, theme-consistent, neutral/brand tints only (never severity color as chrome, D003).

### The button group (`.art-actions`)
- Placed in `.art-bar` **between `#wnav` and `#savestate`**; `#savestate`'s `margin-left:auto` keeps the group in the left cluster and the state chip right-aligned — the version chip, `#wnav` stepper, and `#savestate` dot and their layout are undisturbed, and the group `flex-wrap`s with the bar (no body reflow).
- Four real, focusable `<button>`s, each with `title` (shortcut shown) + `aria-label`; CSS `.art-actions button` mirrors `.art-nav` chrome (24px, `--border-2`, `--muted`) with `--primary-light` hover + `:focus-visible` ring:
  1. **Undo (↶, `#artUndoBtn`)** → `artUndo()` — `disabled` when `_undoStacks[_curArt]` is empty.
  2. **Redo (↷, `#artRedoBtn`)** → `artRedo()` — `disabled` when `_redoStacks[_curArt]` is empty.
  3. **Insert (＋, `#artInsertBtn`, "Insert block (/)")** → `_insertBlockFromButton()`: focuses `#artdoc`; if the selection isn't inside it, drops the caret at the **end of the doc** (creating an empty `<p>` if the doc is empty) before `_openSlash()` — robust when the caret isn't in an empty block.
  4. **Find (⌕, `#artFindBtn`, "Find & replace (⌘F)")** → `openFind()`.

### Disabled-state sync
- New helper **`_syncUndoButtons()`** reads `_undoStacks`/`_redoStacks[_curArt]` depth and toggles the two buttons' `disabled`. Called after **`_pushUndo`**, inside **`_restoreSnapshot`** (covers both `artUndo` and `artRedo`), and at the end of **`openArtifact`** (fresh open → both disabled, per `_resetHistory`). Undo/Redo enable the moment the first edit pushes a snapshot and update as the stacks change.

### Coexistence (verified)
- The ⌘Z/⌘⇧Z/⌘Y (undo/redo), ⌘F (find), and "/" (slash) shortcuts are **unchanged** — the buttons call the same functions; the keydown handler and `_syncSlashFromInput` paths are untouched. Existing `.art-bar` items (nav ‹ ›, version, `#wnav`, `#savestate`, `#saveConfirm`) intact. Quiet debounced reanalysis unaffected (buttons only invoke existing undoable/quiet paths).

### Verification (this revision)
- `node --check` **PASS** on the single extracted `<script>` block.
- jsdom drive-through (**22/22 assertions pass**): the four buttons render in `.art-bar` as real focusable `<button>`s with `title`+`aria-label` (shortcuts in titles); Undo/Redo **disabled at fresh open**; after a `_pushUndo`+edit Undo **enables** (Redo still disabled); **clicking Undo reverses the change** (same result as the ⌘Z path) and then Redo enables / Undo disables; **Insert opens `#slashMenu` (`.show`)**; **Find opens the find bar**; existing toolbar items (version chip, `#wnav`, `#savestate`, nav arrows) all intact; `onclick` handlers wired to the existing `artUndo`/`artRedo`/`openFind` functions. (Slash `.show` confirms the menu opens; `_slashOpen` is a `let` binding not exposed on `window` under jsdom, so it's asserted via the `.show` class.)
- Docs updated: `frontend-ui.md` (toolbar line + new "Visible editor-action toolbar (D085)" section) and `user-experience.md` (new "Visible editor-action buttons (D085)" subsection).

## Revision 14 (2026-07-09, shell cascade D095)
**Ported the approved OSLO app shell (persistent left sidebar + top bar + command palette — D093/D094/D095) into the Slice-5 prototype so it matches the Slice-6 shell.** Edited `slice-05-artifact-workspace/prototype.html` in place; every Slice-5 behavior and the full artifact editor are preserved. The old top-center view switch (`.vswitch`: Overview·Attention·Artifacts) and the in-Artifacts left-rail explorer are removed.

### What changed
- **Grid → 3 columns.** `#app` is now `[sidebar | main | chat]` (`240px 1fr 340px`); `.body` moved to `grid-column:2`, `.chatp` to `grid-column:3`. Ported the full Slice-6 shell CSS: `.sidebar/.sb-*` sidebar, top-bar chrome (`.tb-proj/.tb-tag/.tb-ic/.tb-plan/.sb-hamburger`), `#palScrim/.pal-*` command palette, `.hist-seam`, `.sb-toast/.sb-scrim`, and the 860px sidebar-drawer + 760px chat-collapse media queries. Account menu re-anchored to the sidebar footer.
- **Persistent left sidebar (`#appSidebar`).** PROJECT nav — Overview (LIVE) · Issues · History · Attention map (LIVE) with `.sb-badge` open-issue counts — and PLAN ARTIFACTS grouped Understanding / Execution (the 7 `.sb-art` rows with live `.ex-fb` badges → `openArtifact`). Footer: Take-a-quick-tour (`#railTour`, moved from the floating affordance — no duplicate id) · Free-plan chip + Upgrade · Your account · Settings.
- **Top bar.** `sb-hamburger` · Intralign brand · project switcher (`#tbProj` holding `#projName`) · `sample` tag · breadcrumb (`#tbCrumb`) · unchanged confidence pill · right cluster (⌕ search · Share · Export · Reports · Free).
- **Command palette (D094).** `#palScrim` + `_palModel/_palFilter/_palKeydown/_palActivate/openSearch/closeSearch`; opens via `#tbSearch` and a new global ⌘/Ctrl+K listener. Groups: GO TO · PLAN ARTIFACTS (7, live) · OPEN AN ISSUE (open issues → the light issue panel). Canonical terms; keyboard-operable.
- **Nav sync + routing.** `showView()` now toggles `pane-issues` + `pane-history` and calls `_setCrumb(_viewLabel(v))` + `_syncNav()` (single source of truth for the sidebar highlight + `aria-current`); `openArtifact()` lights its sidebar row and drives the breadcrumb. `updateIssueCounts()` also seeds `#vsIssuesBadge`.
- **LIVE vs seams in Slice 5.** Overview + Attention map = **LIVE**. **Issues** → labeled Slice-6 seam pane (`#pane-issues`, "Full Issues view arrives in Slice 6"; individual issues still reachable via Attention map / Start-here / palette). **History** → labeled Slice-7 seam pane (`#pane-history`). Top-bar/sidebar seams (Projects/Share/Export/Reports/Settings/Upgrade) → labeled `#sbToast`. No broken links, never the wrong view.
- **Editor intact.** The Artifacts view center is now just the editor. Undo/redo, slash menu, tables + column ops, annotations, provenance, find/replace, RTF toolbar, quiet reanalysis, weakness stepper, save confirmation, responsive/touch — all preserved. Sidebar Plan-artifact clicks open the editor exactly as before. Retired the `.vswitch` tour-step selector → `#sbAttention`.

### Verification
- **`node --check`** on the single extracted `<script>` block: **PASS**.
- **jsdom static parse** (no scripts): `body.children.length>0`; `#appSidebar` + PROJECT nav (Overview/Issues/History/Attention) + PLAN ARTIFACTS (7 `.sb-art`, Understanding+Execution) + palette (`#palScrim`, "Search or jump to…") + confidence pill all present; **old `.vswitch`/`.vseg`/`.aw-explorer` gone**; single `#railTour` (no dup id). All 22 checks PASS.
- **jsdom runtime** (`runScripts:"dangerously"`), **25/25 PASS, 0 errors:** Overview/Attention switch views + light badge seeded; History = labeled seam (not the map); Issues = labeled seam (not broken); opening an artifact from the sidebar shows the editor (`#artdoc`, toolbar undo/insert/find) with the breadcrumb + sidebar row synced; ⌘K and `openSearch()` open the palette with the three canonical groups + 7 artifacts + working filter; palette "Open an issue" opens the light panel; seam stubs fire the toast without throwing.

## Revision 15 (2026-07-10)

**Same annotation-popover bleed-through fix as Slice 6 Rev 7 (the two slices share the editor). Edit-in-place; every editor behavior preserved; HTML structurally valid.**

The inline `.anno-pop` summary popover was `position:absolute` inside the contenteditable, so under the app-shell it was clipped by `.aw-center{overflow-y:auto}` and painted **under** the `.art-bar` toolbar — editor content bled through it (looked transparent), worst near the top of the editor. Converted it to a single body-level, **viewport-anchored** popover:

- **`#annoPop`** appended to `<body>`, `position:fixed`, `z-index:240` (below the issue flyout 260, above editor chrome), fully opaque, `display:none` by default. Inline `.anno-pop` is now `display:none !important` and kept only as the content source; the old CSS reveals were removed.
- **`showAnnoPop(anno)`** copies the inline span's `innerHTML` (summary + "Open issue →") into `#annoPop` and **`_positionAnnoPop()`** places it from `getBoundingClientRect()`: prefers **above**, **flips below** when it would cross the `.art-bar` bottom (`_annoPopTopFloor()`), **clamps horizontally** to the viewport.
- **Hover-stable** (open while over the `.anno` or `#annoPop`, ~140ms hover-intent hide); editor scroll / resize / Esc / click-away hide it; the ⚠ marker focus/tap paths drive it; `openIssueFromAnno(id)` and the `.editing` caret path call `hideAnnoPop()`. **Editability (D074) and `curAnnos()` (`.anno` only) preserved** — `#annoPop` is body-level, not inside `.doc`.

Docs updated: `frontend-ui.md` (§ annotation reachability / hover-stable popover / a11y reveals rewritten for `#annoPop`) and `user-experience.md` (popover now renders above/flip-below and fully opaque).

**Verification (Revision 15):**
- **`node --check`** on the extracted inline `<script>`: **PASS**.
- **jsdom static parse** (no `runScripts`): `body.children.length = 16` (> 0); `#annoPop` CSS present; inline `.anno-pop{display:none !important}` present.
- **Positioning unit-test** (extracted `showAnnoPop`/`_positionAnnoPop`, toolbar bottom y120, pop 280×90, viewport 1000×800): first-line anno → **flips below** (`top=136px`); mid anno → **above** (`top=304px`); right-edge anno → **clamped** (`left=712px`); `.editing` anno → **suppressed**. All as expected.
