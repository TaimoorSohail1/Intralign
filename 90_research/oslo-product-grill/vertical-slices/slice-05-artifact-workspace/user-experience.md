# Slice 5 — Plan Artifacts / Artifact Workspace · User Experience

**Release:** OSLO R1 (ALPHA). **Cumulative:** Slices 1–5.
**Baseline of record:** frozen prototype (md5 `a327d702`, boot 157/157).
**Boundary:** advisory-only (D001); editing an artifact runs NO assessment — only an analysis update moves the read (D088); severity colour lives on weakness annotations / issues only, never on chrome or on the `low confidence` grade (D003); the epistemic states **From OSLO** and **Confirmed by you** are both positive (D011/D069); From OSLO marks an inference, never presented as fact (D173); dark default + WCAG 2.1 AA (D015). Client-side prototype only (D016).

> This document notes what is **INHERITED** from Slices 1–4 (unchanged) and what is **CURRENT in Slice 5**. Nothing regresses. **This is a regeneration to match the frozen build** — it supersedes the original July-9 slice-05 doc set (which predates the confidence/Option-C evolution and the DL-143→156 Work-breakdown task tree).

---

## What Slice 5 is

Slice 5 is OSLO's **Artifact Workspace** — the place a PM reads and edits the seven plan artifacts OSLO drafted at intake. It is a co-primary top-center view alongside the Overview and the Attention map. It has two parts: a **left-rail explorer** of the seven artifacts (in the persistent global sidebar), and a **type-aware editor** in the center that opens whichever artifact you pick.

The organising idea: **the plan lives in documents, and you edit the documents directly.** OSLO drafted every artifact **From OSLO** (an inference from your inputs); the moment you revise a sentence or a cell it becomes **Confirmed by you** — a plan fact. You never enter an "edit mode" and you never press "Save" or "Reanalyze": you click and type, changes autosave, and the read catches up on its own at the next analysis update.

**Boundary A (owner-accepted 2026-07-20).** Slice 5 owns the **generic artifact-editor mechanics** — the explorer, prose/table editing, autosave, the reanalysis lifecycle, the provenance flip, and the weakness stepper. The **execution-planning task model** it now surfaces in the Work breakdown artifact — the decomposition itself, the `low confidence` grading semantics, the critical-path computation, the consolidated Full-plan view, and the Asana export — belongs to **Slice 11** (`slice-11-execution-ready-planning-export`). This doc describes that the Work breakdown artifact *carries* an authored task tree and that it is edited/confirmed through the **same generic engine**; for the task-model semantics it cross-references Slice 11.

---

## INHERITED (unchanged)

- **Slices 1–2:** invite → activate → welcome funnel; four start methods; intake constructs all **7 plan artifacts** (Intent · Context · Scope · Requirements · Work breakdown · Schedule · Resources, D035); Fast Pass ≈30s; land on the read-led Overview with the Attention map co-primary; Outcome Analysis auto-runs, non-blocking; the clarification loop; completion notices in OSLO chat; optional tour.
- **Slice 3:** the Outcome Confidence read (five ordinal bands, Option C CAF rows, grounding rollup, the top-bar chip + popover); movement is direction-only (D056) and moves only at an analysis update (D088).
- **Slice 4:** the Attention map (7 artifacts × Clarity·Alignment·Feasibility), cells routing to the light issue panel / scoped Issues list.
- **App shell:** persistent left sidebar (Overview · Issues · History · Inference map · Reports · **Plan artifacts** subgroups · Full plan), top bar, command palette, chat rail. Chrome neutral; severity colour on issues only.

---

## CURRENT in Slice 5 — the Artifact Workspace, part by part

### 1. The explorer — the seven artifacts (D066 / D093)

The explorer lives in the **persistent global left sidebar** (moved there under D093), under a **Plan artifacts** heading split into two subgroups:

- **Understanding** — Intent · Context · Scope · Requirements.
- **Execution** — Work breakdown · Schedule · Resources.

Each row is a button that opens the artifact in the center editor. Each carries a **live open-issue badge** (`.ex-fb`) derived straight from the ISSUES data (`renderExplorerBadges` / `_artOpenIssues`): the number is that artifact's open-issue count, the colour is its **most-severe** open issue (critical / moderate / warning, D003). An artifact with no open issue shows **no badge** (the badge is hidden, never a green "all good" claim).

### 2. The editor — type-aware, always live (D067)

Picking an artifact fills the center pane (`openArtifact`). Before you open anything, an empty state invites you to "Open a document to read and edit it." Each open artifact shows:

- **A head** — the artifact name, an **"✎ Editable"** badge, an info tip (drafted From OSLO · type to edit · edits become Confirmed by you · saving changes no assessment), and the layer label ("Understanding core" / "Execution plan", `_artLayer`).
- **A toolbar** (`.art-bar`) — previous/next-document arrows (`artStep`), the version marker (`v2`, bumps on each committed edit), the **weakness stepper** (§4), editor action buttons (undo · redo · insert block · find/replace · **✦ Ask OSLO about this document**, D108), and the **autosave/reanalysis state chip** (§3).
- **The document** (`#artdoc`) — one always-live contenteditable. There is no enter/exit, no Save button: **click anywhere, type.**

**Type-aware rendering.** Understanding artifacts render as flowing **prose**, mixing a bulleted list or a small table where that reads better (Intent's goals list, Context's stakeholder table). Execution artifacts render as structured **tables** (Schedule milestones, Resources vendors/people). The Work breakdown artifact renders as a **task tree** built on the same `<table>` editor (§5).

The editor also carries the full generic writing toolkit — a Notion-style selection toolbar (bold/italic/lists/headings/link, D078/D080), a "/" slash insert menu, find & replace, undo/redo (per-artifact snapshots, D084/D085), whole-block drag-reorder grips, and paste sanitization. Every one of these is treated as an edit: it attests the block it touches and flows through the same quiet autosave→reanalysis commit as typing. *(The same underlying engine also drives the Reports readout editor — a Slice 10 surface — via a host indirection; the readout deliberately does not get artifact provenance, weakness annotations, versioning, or the reanalysis commit.)*

### 3. Autosave + event-driven reanalysis — the lifecycle (D070 / D073 / D076 / D079 / D088)

Editing is calm and silent. While you are actively typing, the editor shows **no "Editing…"/"Saving…"** churn and does not advance. On ~1500ms of typing-idle (or immediately on blur), the edit commits: it **autosaves** to local storage, bumps the artifact version, records a History event (Slice 7 seam), and then the state chip runs **Reanalyzing… → Up to date** on its own. There is **no manual "Reanalyze" button anywhere.**

Crucially, **saving changes no assessment.** Editing a sentence firms it into your plan immediately (it becomes Confirmed by you), but the Outcome Confidence read does **not** jump on the edit — it catches up when the analysis update lands (D088). The chip conveys the whole cycle by a dot's colour + a hover title only (Up to date / Reanalyzing…), never by a reflowing block of text.

### 4. Weakness annotations + the weakness stepper (D068 / D071 / D074)

OSLO's draft carries **inline weakness annotations** on the contiguous weak span — coloured on a severity ramp (**red/amber only**, D003), wired to real open issues. Hovering a span shows a one-line summary; clicking opens the **light issue panel** (the same panel as the Attention map) — a weakness is **never resolved inline**. The toolbar's **weakness stepper** ("Jump to issue ⌃ *k* of *N* ⌄", `updateWnav`/`weaknessNav`) walks between the weak spots in the open artifact, scrolling each into view and highlighting it. Only **live** (still-open) annotations render — resolving an issue drops its inline mark on the next re-render — and when none remain the stepper reads "✓ No issues in view."

### 5. The Work breakdown task tree (DL-143→156 · 2A — the delta on this surface)

The **Work breakdown** artifact now renders as an **authored, graded task tree**: workstreams → tasks → subtasks, **outline-numbered** (`1 · 1.1 · 1.3.1`) with indentation by level. Every row is **From OSLO** until you confirm it, and the **thinnest inferences carry a neutral `low confidence` grade** — a dashed, neutral pill, *never* a severity colour (D003: the grade is epistemic, not a health signal). It is built on the **unchanged `<table>` editor**, so all the generic machinery — per-cell/row provenance, add/insert/delete row and column, autosave, the reanalysis commit — applies to it for free. Confirming a task is exactly the generic cell edit: type in (or accept) a cell and it flips **Confirmed by you** (D196a — the per-item verb is Confirm).

A From-OSLO **"Sequencing & critical path"** panel also renders in the Work-breakdown view — but **outside** the editable `#artdoc` (it is analysis, not editable plan content) and it is **not editable** here.

> **Slice 11 owns the task-model semantics.** The decomposition, what `low confidence` grades and how it is computed, the critical-path computation, the consolidated Full-plan view, and the Asana export are documented in `slice-11-execution-ready-planning-export`. Slice 5's story is only that the artifact *carries* the tree and that it is edited/confirmed via the same generic engine, and that the critical-path panel renders read-only outside `#artdoc`.

---

## Epistemic notation — From OSLO vs Confirmed by you (D011 / D069 / D083 / D196a)

Both are **positive** epistemic states. Prose blocks (paragraphs, list items, headings) wear a **`.epi-tag`** reading "From OSLO" or "Confirmed by you"; editing a block flips its tag to Confirmed by you immediately (`_attestSelectionBlocks`). Table cells can't wear the prose tag, so each body **cell** carries an epistemic state (`data-epi="derived"|"attested"`) surfaced two ways — a glanceable **per-row gutter dot** and a **per-cell hover/focus reveal chip** (`_seedTableProvenance` / `_ensureCellReveal`). Editing a cell flips it to Confirmed by you live, and its row dot recomputes. The class names come from one registry (`EPI_CLASSES` / `epiClassName`, D194b) so every surface reads the same words. **This is the ratified confirm mechanism at cell + task altitude** (D196a — the per-item verb is Confirm; editing/accepting an item *is* confirming it).

On a simulated OSLO re-draft, the **merge guarantee** holds: blocks and cells you have Confirmed by you are preserved verbatim; only From OSLO content is refreshed (`redraftArtifact`).

---

## Journey (Slice 5 lens)

1. From the Overview/Attention/Issues, click a **Plan artifacts** row (or an Attention cell that routes to it) → the artifact opens in the center editor.
2. **Read** the draft — inline weakness spans mark the weak spots; the stepper jumps between them; hover for a summary, click to open the issue.
3. **Edit** a sentence or a cell → it flips **Confirmed by you** instantly; the change autosaves silently.
4. Editing settles → the state chip runs **Reanalyzing… → Up to date**. The Outcome Confidence read catches up at the analysis update — not on the keystroke (D088).
5. Open the **Work breakdown** artifact → the graded task tree renders (outline-numbered, low-confidence rows flagged neutrally), with the read-only Sequencing & critical path panel below the editable doc.
6. Step to the next document (`›`) or hand the open artifact to the chat (**✦**) for "what's weak here and where it came from."

All calls stay with the user (D001). OSLO drafts and explains; nothing changes the plan without the user.

---

## Chat integration (inherited, adapted to Slice 5)

The **✦ Ask OSLO about this document** button hands the open artifact to the chat (`askOslo({type:'artifact'})`); a weak span's "Ask about this" hands that span's issue over (`askAboutSpan`). The chat reports the artifact's epistemic basis (From OSLO / Confirmed by you) and reliability honestly, and routes to the live issue — it mutates nothing and never claims to have edited or resolved anything itself.
