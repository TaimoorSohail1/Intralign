# Slice 5 — Plan Artifacts / Artifact Workspace · Product Detail

**Cumulative build (Slices 1–5).** This document specifies the NEW Slice-5 behavior in detail. Inherited behavior from Slices 1–4 is unchanged and specified in those slices' docs.

Decisions: **D066, D067, D068, D069, D070, D071.** Cross-cutting: D001, D003, D006, D011, D015, D017, D049.

---

## 1. Navigation & shell (D066)

- The top-center view switch gains a third segment: **Overview · Attention · Artifacts** (`#vsArtifacts`). It is a co-primary view (same tier as Overview and Attention), not nested.
- Selecting **Artifacts** activates `#pane-artifacts`, a two-column grid: **explorer** (214px) + **center editor** (flex). It sits inside the `.body` grid column, so the OSLO chat rail remains to its right.
- Overview/chat links that referenced "plan artifacts" (`openPlanSections()`) now route to the workspace and open Intent by default.
- Context preservation: Overview and Attention remember `.body` scroll; the workspace manages its own `aw-center` scroll. Returning to the workspace keeps the last-open artifact.

## 2. Explorer (D066)

- Fixed order: **Understanding** → Intent, Context, Scope, Requirements; **Execution** → Work breakdown (`WBS`), Schedule, Resources.
- Each row: icon + display name + **open-issue badge** (`.ex-fb`). Badge shows the **open-issue count** for that artifact; badge **color = the most-severe open issue** (`crit`/`mod`/`warn`), severity-only per D003. Zero open issues → badge hidden (`.clear`).
- Badges are recomputed **live** by `renderExplorerBadges()` on: workspace entry, boot/land, and every `updateIssueCounts()` (so resolving an issue updates the badge immediately).
- Rows are `role="button" tabindex="0"`, operable by Enter/Space (D015).

## 3. Type-aware editor (D067)

- **Format by artifact** (`_ARTFORMAT`):
  - `prose` — Scope (flowing prose only).
  - `mixed` — Intent (prose + bulleted goals list), Context (prose + stakeholder table), Requirements (prose + bulleted acceptance list). Understanding artifacts default to prose but mix bullets/tables where those better represent the items.
  - `table` — Work breakdown, Schedule, Resources (structured tables).
- The editor body (`.doc#artdoc`) is `contenteditable="true" spellcheck="false"`. Blocks (`p`, `li`, `td`, `h3`) are the edit units.
- **Autosave (simulated):** on input, after a debounce, the artifact's HTML + a bumped version are written to `localStorage` (`oslo-s1-art-<name>` / `-ver`). No server.
- Header shows an **"✎ Editable"** badge and an info tooltip stating the edit/attest/reanalysis rules.

## 4. Inline weakness annotations (D068)

- Weak spans are `<span class="anno crit|mod|warn" data-fid="ISS-0X" onclick="openIssueFromAnno('ISS-0X')">…</span>`, `contenteditable="false"` (atomic — not editable text).
- **Color:** severity ramp only (red critical / amber moderate / neutral warning). Dotted underline; hover tints.
- **Hover:** the `title` gives a one-line summary ("<Dimension> issue · <Severity> — hover reads the summary; click to investigate. (Never resolved inline.)").
- **Click:** opens the **light issue panel** (`openIssue`) for the wired issue — the existing Slice-2/4 panel with the clarification loop.
- Annotations map to the six real open issues: ISS-01 (Resources · Feasibility · critical), ISS-02 (Requirements · Clarity · moderate), ISS-03 (Resources · Feasibility · moderate), ISS-04 (Schedule · Feasibility · moderate), ISS-05 (Work breakdown · Alignment · moderate), ISS-06 (Context · Clarity · warning). When an issue resolves, re-rendering the open artifact drops its annotation.

## 5. Epistemic notation (D069)

- Each prose/list block carries `data-epi="derived"` and a hover chip `.epi-tag.derived` reading **"From OSLO"**.
- On edit, the block the caret is in flips to `data-epi="attested"`, gains the `.attested` class (**left-border accent**), and its chip becomes `.epi-tag.attested` reading **"Confirmed by you"** = a plan fact.
- The editing/stale hint bars state: *"What you change becomes Confirmed by you — part of your plan. Saving changes no assessment; only reanalysis does."*

## 6. Event-driven reanalysis (D070)

State machine on input (`onArtInput`), all via simulated timers:

1. **Saving…** (immediately, neutral dot).
2. **Saved · analysis stale** (~700ms; version bump written; warning dot; "stale" hint bar shows).
3. **Reanalyzing…** (~1.3s later; pulsing warning dot).
4. **Up to date** (~1.5s later; success dot; hint bar clears).

No manual reanalyze control exists. The assessment (confidence/issues) is not fabricated to move here — only genuine reanalysis paths (e.g. answering a clarification in the issue panel) change the model.

## 7. Weakness stepper + artifact nav (D071)

- **Weakness stepper** (`#wnav`): "Jump to weakness ⌃ [k of N] ⌄". `weaknessNav(±1)` cycles the `.anno` spans in `#artdoc`, outlines the current one (`.wstep`), scrolls it into view, and updates the "k of N" counter. If the artifact has no weaknesses, shows "✓ No weaknesses in view".
- **Artifact nav** (`.art-nav`): ‹ / › call `artStep(±1)` over `_ARTORDER`; disabled at the ends.
- Both are keyboard-focusable buttons (D015).
- **Tour step:** the feature tour's fifth step (`#artdoc`, view `artifacts`, `onEnter: openArtifact('Resources')`) spotlights the real editor, replacing the former Slice-5 seam placeholder.

## 8. Accessibility (D015)

- Explorer rows and editor blocks are keyboard-focusable; stepper and nav are operable by keyboard.
- Focus-visible rings inherited from the global token set; contenteditable blocks show focus outline.
- Severity color is never the sole carrier of meaning (annotations also carry a title + open the issue; badges carry a count).
