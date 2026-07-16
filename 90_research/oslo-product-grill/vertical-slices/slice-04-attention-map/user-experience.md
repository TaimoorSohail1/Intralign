# Slice 4 — Attention Map (MRI) · User Experience

**Cumulative:** Slice 1 + Slice 2 + Slice 3 + **Slice 4**. This slice deepens the Attention Map into the primary MRI visual and wires cell → Issues routing. Everything from Slices 1–3 is preserved.

Decisions encoded: **D057–D062** (+ inherited D007, D003, D038, D015, D001, D017, D049).

---

## INHERITED (preserved 1:1 from Slices 1–3)

The following are unchanged and must not regress:

- **Access & onboarding (S1):** invite email → activation → welcome → intake (four start methods: Attach · Describe · Templates · Sample), one-time strategic-chain orientation, advisory footer, account menu (logout, stay-signed-in), GA-preview toggle (anonymous run + save-to-keep, labelled, not default).
- **Intake & Fast-Pass orientation (S2):** Fast Pass "Initial Analysis" ≈30s, lands on the confidence-led Overview with Attention co-primary, seven plan artifacts constructed, completion notices in OSLO chat, optional feature tour, clarification loop, Fast/Deep analysis-state machine (provisional → current, last-good + retry on failure).
- **Overview & understanding console (S3):** Overview = Confidence → Start here → Progress → More; confidence pill + click popover (CAF dimensions + Reliability basis); neutral false-confidence flag; confidence stages (Orientation ▸ Expanded ▸ Validated); "how this is calculated" affordance; richer Project summary; direction-only confidence movement; "Strengthened" trend label.
- **Light issue panel (S2/S3):** the clarification loop panel (Header → lifecycle Open→Addressed→Resolved → Why → Evidence → Clarification → Suggested fixes). Reused as-is by Slice 4 routing.

## NEW in Slice 4

### The heatmap is the primary attention view (D057)
Switching to **Attention** shows a heatmap: **rows = the 7 plan artifacts** (grouped Understanding / Execution), **columns = Clarity · Alignment · Feasibility**. Each cell is shaded by how much **attention** it needs — from calm (no open issue) to bright (a critical open issue). Non-empty cells show the **open-issue count** and a small **severity label**; cells with more than one open issue carry a subtle "multiple" marker. The legend reads **"Brighter = more attention — not a health score."**

### Clicking a cell routes to its issues (D058)
- A cell with **exactly one open issue** opens **that issue** directly in the light issue panel.
- A cell with **more than one open issue** opens the **Issues list scoped to that artifact + dimension**, with **both filters visibly lit** (e.g. *Plan artifact · Resources* and *Dimension · Feasibility*). Each row opens its issue.
- A **row header** opens all issues for that artifact.
- The scoped list is a **seam** — the full Issues surface (grouping, By dimension / By severity, triage, resolved tab) is **Slice 6**. A dashed note says so.

### Field / Dimensions view — REMOVED (owner decision D063, Revision 3)
The secondary "field"/Dimensions view (D059) and the Heatmap / Field toggle were **removed** per owner decision D063 — the toggle wasn't helpful. The Attention map now shows **only the heatmap**; there is no toggle bar and no by-dimension view.

### Severity color only on cells; hover scales (D060)
The red/amber **severity ramp appears only on attention cells**. Confidence and the CAF dimensions stay on the **neutral maturity ramp** — never health-colored. Hovering a live cell scales it slightly; empty cells do not react. The legend restates attention-not-health.

### Empty and all-clear states (D061)
- An artifact×dimension with **no open issue** is a neutral, **inert (non-clickable)** `l0` cell — no severity color, no hover, no keyboard target.
- When the **whole map** has no open issues, the grid is replaced by an **all-clear** state: "Nothing needs your attention right now" — framed explicitly as all-clear on *attention*, not a guarantee of success.

### Co-primary placement + context preserved (D062)
The Attention map is reachable as the **co-primary top-center view** (the Overview · Attention switch) **and** from the Overview's **"Attention map →" pointer**. Switching back **restores prior context** — each pane remembers its scroll position, so returning to the Overview lands where you left it.

---

## Key user journeys (Slice 4)

1. **Scan attention:** land on Overview → click **Attention** (or the Overview "Attention map →" pointer) → read the heatmap. At Fast Pass the brightest cell (Resources × Feasibility) shows where the plan most needs attention; once **Extended Analysis** auto-runs it adds the Deep-Pass findings (per Enhancement #2 Phase 2), so the Extended map has **9 open issues across 8 of 21 cells** and more than one critical (`l3`) cell — Resources × Feasibility, Schedule × Feasibility, and Schedule × Alignment — plus a two-issue **Scope × Alignment** cell (ISS-08 + the new ISS-09). The Alignment column now reflects coherence between plan elements and intended outcomes, not just stakeholder-agreement.
2. **Single issue:** click a single-issue cell (e.g. Requirements × Clarity) → the issue opens directly.
3. **Multiple issues:** click the Resources × Feasibility cell (2 open) → the scoped Issues list opens with both filters lit → pick an issue → it opens; close returns to the scoped list.
4. **Resolve via clarification:** open the critical Resources issue → answer its clarification → reanalysis resolves it → the cell dims and the count drops (the heatmap updates live).
5. **All-clear (demo):** the phase-bar "Sim all-clear" trigger resolves all issues → the map shows the all-clear state; toggling off restores it.

## Accessibility (D015)
Every live cell and row header is keyboard-focusable and activates on **Enter/Space**; empty `l0` cells are inert (not in the tab order). The scoped list and issue panel are dialogs with visible focus rings. Dark default; the severity ramp keeps AA contrast.

---

## Revision 2 (2026-07-09) — feedback fixes

- **Live heatmap counts (bug fix):** entering the Attention view now re-renders the map (`renderHeat`/`renderDims`/`updateIssueCounts`), and every issue-status change already does the same. A cell's displayed count and its click routing (single issue vs. scoped list) can no longer disagree — resolve one of two issues in a cell and, on return, the cell reads "1" and opens that single issue.
- **Timeline → History seam:** the Confidence-card link row now reads **Why · Timeline → · Attention map →**. "Timeline →" opens a clearly-labeled **History & timeline** stub — *"arrives in Slice 7"* — a centered modal, **not** the Attention heatmap. The Attention pointer stays separate.
- **"How this is calculated" placement:** the chip now sits **directly under the confidence number** it explains, and its duplicate native tooltip was removed (only the custom popup remains).
- **Stage context:** the confidence **Stage** marker now has a visible **ⓘ** explaining Orientation → Expanded → Validated and which stage the read is at (Overview and popover).
- **CAF hover scope:** the dimension detail tip opens only when hovering the **dimension word** (Clarity / Alignment / Feasibility), not anywhere on the row. Row click-to-navigate is unchanged.

---

## Revision 4 (2026-07-09) — persistent app shell (shell cascade, D095)

The approved Slice-6 app shell was cascaded down to Slice 4 so navigation matches across slices (D093/D094/D095). The old top-center **Overview · Attention** switch is replaced by a **persistent left sidebar** and a **command palette** — no Slice-4 behavior regresses.

- **Left sidebar (always visible):** a **Project** group — **Overview**, **Issues**, **History**, **Attention map** — plus pinned utilities (Take a quick tour, Free-plan chip, Your account). In Slice 4, **Overview** and **Attention map** are live views; **Issues** opens a clearly-labeled *"Full Issues view arrives in Slice 6"* stub (single-issue investigation stays live via the Attention map and the palette); **History** opens the *"arrives in Slice 7"* stub. **There is no Plan-artifacts list yet** — the artifact editor arrives in Slice 5, so that sidebar section is intentionally absent here.
- **Top bar:** Intralign brand, a project switcher, a `sample` tag, and a **breadcrumb** that names where you are (Overview / Attention map), with the confidence pill and a right-hand cluster (search, Share, Export, report, Free plan). Share/Export are Slice-9 stubs.
- **Command palette (⌘/Ctrl+K or the `⌕` button):** type to jump to a view or **open an issue**. Fully keyboard-operable (↑↓ navigate, ↵ open, esc close). The Plan-artifacts group is omitted in Slice 4.
- **Navigation feel:** the current view is highlighted in the sidebar (`aria-current="page"`) and named in the breadcrumb; seams are unmistakable labeled stubs, never a wrong or broken view. On narrow screens the sidebar becomes a `☰` drawer and the chat rail collapses.
- **Unchanged:** the whole Attention map experience, the confidence-led Overview, the pill popover, the tour, the persistent OSLO chat, and the clarification loop.

## Chat integration (D108 cascade)

OSLO's rail stops being a noticeboard and becomes a **conversation** — one you can hold *about the thing you're looking at*. In Slice 4 that thing is, above all, a **cell on the Attention map**.

**You can now ask.** Type into the composer and press Enter (or click Send). OSLO answers from the read that is actually on your screen — the confidence band and its reliability qualifier, the limiting dimension, your open issues and the one it would take first, and the attention picture (which cells are lit, how brightly, and why). It does not invent numbers or issues. If you ask it to fix something, it says plainly that it cannot: it reads and explains; you decide.

**Ask about a cell — the signature move.** Hover any lit cell on the Attention map and a quiet **✦** appears; click it and OSLO takes that cell as context. A pill at the top of the rail reads **Context · Resources × Feasibility**, and OSLO opens with what that bucket actually means — *Resources read through Feasibility* — what is driving its brightness (the most severe open issue wins the cell's color), what else sits in it, and whether that dimension is the one holding your confidence back. The same "✦ Ask OSLO about this cell" sits in the header of the scoped issues list, so it is there whichever way the cell routed you. Everything after that is answered *inside* that cell until you clear the pill with **×**.

**Ask why the number is where it is.** "✦ Ask OSLO why" under the confidence number hands the read to the chat: the band, the reliability basis, the limiting dimension, and what would move it.

**Ask about an issue.** "✦ Ask OSLO about this issue" in the issue panel: why it matters, what it was read from, the fixes worth weighing — and links straight back to the issue and the cell it lives in.

**Answer a question without leaving the conversation.** When an issue carries one of OSLO's questions, the question comes with an answer box right in the thread. Answering there is *exactly* the same act as answering in the issue panel: your project information updates, that plan artifact becomes Confirmed by you, and the analysis update closes the issue — OSLO tells you when it lands, and the cell on the map stands down. There is no shortcut and no side door; the chat cannot do anything the surfaces cannot.

**Suggestions, not a blank box.** Above the composer sit a few suggested questions drawn from your actual state, and they change with it — with a cell in context they become "What's driving this cell?"; with nothing in context, "Why is Feasibility Very Low?" or "What needs the most attention?".

**Unchanged:** the heatmap and its routing, the inert all-clear cells, the confidence-led Overview, the light issue panel, the clarification loop, the tour, and OSLO's completion notices — which still land in the same rail, now alongside the conversation.
