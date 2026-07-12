# Slice 7 — History & Confidence Trend · User Experience

**Cumulative:** Slice 1 + Slice 2 + Slice 3 + Slice 4 + Slice 5 + Slice 6 + **Slice 7**. This slice **replaces the Slice-6 History seam** (`#pane-history` "arrives in Slice 7") with the **real History & timeline surface**: an **append-only** event list plus an **"Understanding over runs"** confidence trend. Everything from Slices 1–6 is preserved 1:1.

Decisions encoded: **D096** (append-only History/timeline), **D097** ("Understanding over runs" trend — rises or falls, cause-bound + band-qualified), **D098g** (last-good + read-only honesty), **D099** (artifact version lineage), **D100** (first-run minimal state) (+ inherited D001 advisory-only, D002 confidence = neutral maturity, D003 severity-only color, D006 analysis-update-only assessment, D040/D041 Extended Analysis supersede/last-good, D056 direction-only confidence, D092 no user-facing "reanalysis" mechanism, D015 dark + WCAG 2.1 AA, D017 "Issues", D049 "Plan artifacts").

---

## What's NEW in Slice 7

### The History nav item now opens a real surface (D096)
The persistent left-sidebar **History (◔)** item — which in Slice 6 routed to a labeled seam pane — now opens the **live History & timeline** center pane. The OSLO chat rail stays visible (History is a center pane, like Overview), and the top-bar breadcrumb reads **"History"**. The pane header reads **"History & timeline · append-only · prior states retained"** with a single ⓘ hover explaining that prior states are never overwritten and viewing changes nothing.

The **Overview "Timeline →"** pointer and the **Issue-panel "Open full timeline →"** pointer now route to this same real surface (no more seam modal, no "(Slice 7)" tail).

### An append-only event timeline (D096)
The timeline is a **chronological, newest-first** list of everything that has shaped OSLO's read of the project. Event types:
- **Analysis runs** — *Initial Analysis complete*, *Extended Analysis complete* (supersede the provisional orientation).
- **Plan-artifact versions (vN)** — each edit or applied fix retains a new version; prior versions are kept.
- **Issue lifecycle changes** — *Open → Addressed → Resolved* (Resolved only ever follows an analysis update, never a manual step).
- **Selected resolution paths** — when you pick a path or *Apply this fix*.
- **Clarifications answered** — when you answer an OSLO question.

Each row carries a plain label, an optional detail line, an illustrative timestamp, and a **current / prior** tag (the most recent analysis run and lifecycle-resolved events read **current**; superseded states read **prior**). **Nothing is overwritten** — the list only ever grows.

**It grows live.** As you work in the session, real events append in front of you: apply a fix or answer a clarification → the issue's lifecycle and a resolution entry appear; edit a plan artifact → a new version entry appears; when Extended Analysis completes → its run, the retained v1 versions, and the detected issues appear. Open History after acting and the new rows are already there.

### "Understanding over runs" — the confidence trend (D097)
At the **top of the History pane** sits a small sparkline titled **"Understanding over runs — rises or falls with the read."** Each point is a completed analysis run, **band-qualified** (Very Low · Low · Moderate · High · Very High) and **cause-bound** (a plain reason on hover, e.g. *"deeper analysis firmed the read (Feasibility rose Very Low → Low)"*). The line is drawn in the **neutral maturity color**, never a severity color — it is not a health score.

Crucially the line **can rise OR fall**. A **fall** after a deeper analysis usually means OSLO *found something real* — not that the project got worse — and the single ⓘ hover says exactly that. Direction is shown (▲/▼) without shouting a fabricated magnitude (illustrative demo indices live in code only). The **Overview's quiet confidence-trend row is kept** (D097) — this History trend is its fuller home.

### Read-only, last-good honest (D098g)
History is **read-only**. You can view any prior state, but viewing never edits your plan or changes the assessment — a subtle **"Read-only · viewing history changes nothing"** note sits at the foot of the pane. If **Extended Analysis fails**, the timeline records a **"couldn't complete — showing last-good"** entry; your last-good understanding is preserved, unchanged, and the trend does not move (nothing is overwritten).

### Version lineage — view a prior snapshot (D099)
Artifact **version (vN)** rows are subtly interactive: a **"view snapshot →"** affordance opens a **read-only** note (a toast: *"prior version · read-only — prior states are retained, never overwritten; viewing changes nothing"*). Prototype-grade — a labeled read-only view, not a full diff. Version rows are keyboard-operable (focusable, Enter/Space).

### First-run minimal state (D100)
Before more than the initial analysis exists, History shows a **minimal state**: *"Your history starts here — so far this is just your Initial Analysis. More appears as your plan evolves."* Once Extended Analysis completes or you act on the plan, the minimal card gives way to the full timeline.

---

## INHERITED (preserved 1:1 from Slices 1–6)

The following are unchanged and must not regress:

- **Access & onboarding (S1):** invite email ("Intralign Alpha") → activation → welcome → intake (Attach · Describe · Templates · Sample), one-time strategic-chain orientation, advisory footer, account menu (logout / stay-signed-in), GA-preview toggle (labelled, not default).
- **Intake & Fast-Pass orientation (S2):** four start methods, ≈30s Initial Analysis pacing, orientation lands on the confidence-led Overview, Extended Analysis auto-runs (non-blocking, supersedes), completion/failure notices delivered via OSLO chat, optional feature tour.
- **Overview & Understanding console (S3):** confidence-led Overview (focal score + meaning line + inline reliability qualifier + "Why"), CAF maturity bars, quiet confidence-trend row, top-bar confidence pill + popover (CAF + reliability basis + stage marker), false-confidence flag, "how this is calculated", Project summary in "More".
- **Attention map (S4):** heatmap (7 artifacts × Clarity·Alignment·Feasibility), severity-only cell coloring + legend, live re-render on entry, cell → scoped Issues routing, all-clear/empty states.
- **Plan artifacts / editor (S5):** left-sidebar explorer with badges, type-aware editor (prose/mixed/tables), inline weakness annotations, From OSLO / Confirmed by you epistemic accents, quiet debounced save→stale→updating→up-to-date indicator, Notion-style rich-text toolbar, full table row/column ops with drag-reorder, undo/redo, find/replace, slash-insert, version chip.
- **Issues & recommendations (S6):** all-issues surface (Artifact · Dimension · Severity filters + By dimension/severity/artifact group toggle + honest hidden count), full Issue Panel (Header → Why → Evidence → What this weakens → Recommendations → History pointer), lifecycle Open → Addressed → Resolved, Apply this fix, clarification loop, four honest empty states.
- **App shell (S6, carried):** persistent left sidebar + top bar + command palette (⌘/Ctrl+K), OSLO chat rail, phase bar, issue flyout.

## Boundaries (unchanged doctrine)
Advisory-only; "Issues" not "Findings"; Clarity · Alignment · Feasibility; From OSLO / Confirmed by you; the shared 5-band scale. **Severity color only on issue severity** — confidence, CAF, and the History **trend line are neutral maturity**. Dark default + WCAG 2.1 AA (timeline is keyboard-navigable; version rows focusable). User-facing framing is **"analysis update" / "analysis run"**, never "reanalysis" (D092). **Threaded comments as timeline events are OUT (Slice 9)** — a seam is left; History reflects lifecycle / analysis / version / clarification events only.

---

## Revision 2 (2026-07-09, D101 refinements)

History gap-analysis refinements. The append-only, read-only, and last-good-preserved promises are unchanged — viewing, grouping, collapsing, and filtering never edit the plan or change any assessment.

- **No internal jargon on screen.** The timeline no longer shows OSLO's internal event codes. Every entry now reads in plain language — an **Analysis run**, a **Version**, an **Issue update**, or **Your decision**.
- **Organized by analysis run.** Instead of one long flat list, History is grouped into **collapsible run cards** — newest run first (Initial Analysis, Extended Analysis, or a last-good run). The versions, issue updates, and decisions that followed each run nest beneath it, with a **Today / Yesterday** day marker. Groups open by default; click a header to collapse.
- **"What changed" per run.** Each run card carries a scannable delta: how many issues **opened** and **resolved**, notable maturity moves (e.g. *Feasibility Very Low → Low*), the understanding-stage change (*→ Expanded*), and the confidence **direction** (▲/▼ only — never a fabricated number, D056). The resolved count grows live as you act on the plan.
- **Trend and timeline connected.** Clicking a point (or its caption) on the **"Understanding over runs"** trend jumps to and briefly highlights that run's card. Each run card also states the confidence **band** it produced (e.g. *Moderate confidence*). The trend stays neutral maturity; hover still explains that a fall usually means deeper understanding, not a worse project.
- **Filter what you see.** Chips above the list — **All · Analysis · Issues · Versions · Your decisions** — filter the timeline, with an honest *"N hidden by this filter"* and a one-click way back to All. Keyboard-accessible, styled like the Issues surface filters.
- **Honest "current."** Only the **latest analysis run** is marked *current*; earlier runs read as *history*. Hovering any entry shows its (illustrative) absolute date and time.

Out of scope (deferred, unchanged): version diff/restore, history search, export, windowing; and "reanalysis" is never surfaced as a mechanism (always "analysis run"/"update", D092). Illustrative timestamps and delta values are prototype-grade, not canonical figures.

## Chat integration (D108 cascade)

OSLO's chat rail now **works** in this slice — you can type to it, and it answers from the real state of your plan, including **what changed in your last analysis run**. It stays advisory: it reads and explains, it never changes your plan.

- **Ask anything.** Type in the composer and press **Enter** (Shift+Enter for a new line) or click **Send**. OSLO answers from what it actually knows — your confidence band and reliability, the **limiting dimension**, your open issues and the one it would take first, the artifact you have open, its recommendations, and **your history and trend**. Every answer ends with links straight to the surface it's talking about.
- **"What changed in the last run?"** New on History: an **✦ Ask OSLO** button on the History pane, and one on **every analysis-run card**. OSLO explains that run in plain language — how many issues **opened** and **resolved**, what moved (e.g. *Feasibility Very Low → Low*), whether the understanding **stage** advanced, and which **direction** confidence went (never an invented number) — and links you back to that run's card on the timeline. A **"What changed in the last run?"** suggested chip sits in the composer.
- **Hand any surface to the chat.** A **Context** pill shows what the conversation is about, with an **×** to clear it: an issue, a flagged span in an artifact, a whole plan artifact, your confidence read, an Attention-map cell, a recommendation, or an analysis run.
- **Discuss a recommendation — without committing.** Every issue's **OSLO Recommended** and **every resolution path** carries a **Discuss** action. Discussing opens the conversation and weighs the trade-offs against the alternatives; **it does not select the path**. Selecting stays your explicit call, in the issue.
- **Answer OSLO's questions in the conversation.** When OSLO has a clarification, you can answer it right in the chat instead of the issue panel. It's the **same answer**: the same update to your project information, the same move to **Addressed**, the same analysis update that closes the issue, and the **same entries on your timeline**. The chat is not a side channel. Ask the same question twice and you still get **one** live answer box — never two.
- **It says what it can't do.** Ask it to fix, close, or apply something and it tells you plainly: it can't change your plan; an issue reaches **Resolved** only when an analysis update confirms the gap no longer holds — and that move is recorded on your timeline.
- **First-run and accessibility.** An empty state tells you what OSLO can answer before you've asked anything; replies are announced politely to screen readers; every in-chat action is a real, keyboard-operable button.

Unchanged: History stays **append-only and read-only** — asking about a run never edits it, and viewing never changes an assessment. "Reanalysis" is never surfaced as a mechanism (always "analysis run"/"analysis update"). Chat replies are prototype-grade simulations grounded in the live demo state — not a real language model.
