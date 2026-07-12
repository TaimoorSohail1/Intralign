# Slice 6 — Issues & Recommendations (Panel Model) · User Experience

**Cumulative:** Slice 1 + Slice 2 + Slice 3 + Slice 4 + Slice 5 + **Slice 6**. This slice adds the **all-issues surface** (a fourth co-primary view) and **graduates** the light issue panel and the Attention-map scoped seam into the **full Issue Panel** with **lifecycle**, **recommendations**, **Apply this fix**, the **clarification loop**, and **honest empty states**. Everything from Slices 1–5 is preserved 1:1.

Decisions encoded: **D086** (all-issues surface — filters + group toggle + hidden count), **D087** (full Issue Panel), **D088** (lifecycle Open → Addressed → Resolved), **D089** (Recommendations + Apply this fix, Panel Model), **D090** (clarification loop in the panel), **D091** (four honest empty states), **D093** (persistent left-sidebar app-shell navigation) (+ inherited D001 advisory-only, D009 Panel Model, D003 severity-only color, D056 direction-only confidence, D006 reanalysis-only, D011/D069 Derived/Attested, D015 dark + WCAG 2.1 AA, D017 "Issues", D049 "Plan artifacts", D058 cell routing).

## App-shell navigation — persistent left sidebar + top bar (D093, reconciled to the owner-APPROVED design)

The app shell carries a **persistent left navigation sidebar** and a full **top bar**, reconciled to the owner's approved layout. There is one durable place to move around the project. Sidebar, top to bottom:

- **Project** — Overview (◎), **Issues** (⚑, with a neutral open-issue count badge), **History** (◔), Attention map (▦), in that approved order. We use the ratified term **"Issues"** (not "Findings", despite the approved image's label) and keep the count badge. History is a real nav item that routes to a clearly-labeled **Slice-7 seam** center pane ("History & timeline — arrives in Slice 7") — never the Attention map. The current view is highlighted (`aria-current="page"`); no severity color is used as navigation chrome.
- **Plan artifacts** — the seven artifacts split into two labeled subgroups: **Understanding** (Intent · Context · Scope · Requirements) and **Execution** (Work breakdown · Schedule · Resources), each showing its live per-artifact issue badge (severity-colored per D003/D066). Selecting one opens the Artifacts view with that artifact in the editor and highlights it. This is the single home for the artifact list.
- **Bottom (pinned)** — a bordered **"✦ Take a quick tour"** button (feature tour; sunsets once seen); a neutral **tier chip** (◆ **Free plan** · 1 active project) with an **Upgrade** button (visibility-first prompt); and a **Your account** row (avatar "ID" + "Your account" / "Settings" subtext) that opens the account menu (Settings lives here as a stub notice).

The **top bar**: left — Intralign brand, a **project switcher** chip ("DevNorth 2026 ▾"; a **Slice-8 seam** since multi-project isn't built), a **"sample"** tag, and a breadcrumb showing the current view or open artifact. Right — the always-visible **confidence pill** (unchanged), a **search** icon, **Share** and **Export** (both **Slice-9 seams**), a report/donut icon, and a **Free** plan chip. A ☰ hamburger sits far left for the responsive drawer. Chrome is neutral/brand only; only issue badges keep their severity color.

Seams for not-yet-built features are clearly labeled stubs, not broken links: History → Slice 7, project switcher → Slice 8, Share/Export → Slice 9. On narrow screens (≤860px) the sidebar collapses to an overlay drawer opened by the ☰ button; it auto-closes after a pick. The chat rail's existing collapse behavior is unchanged. Every prior surface — the full editor (S5), Issues surface (S6), Attention map, Overview, chat, tour, phase bar, and the issue-panel flyout — is preserved.

---

## INHERITED (preserved 1:1 from Slices 1–5)

The following are unchanged and must not regress:

- **Access & onboarding (S1):** invite email ("Intralign Alpha") → activation → welcome → intake (four start methods: Attach · Describe · Templates · Sample), one-time strategic-chain orientation, advisory footer, account menu (logout / stay-signed-in), GA-preview toggle (labelled, not default).
- **Intake & Fast-Pass orientation (S2):** Fast Pass "Initial Analysis" ≈30s, lands on the confidence-led Overview, seven plan artifacts constructed, completion notices in OSLO chat, optional feature tour, Fast/Deep analysis-state machine (provisional → current, last-good + retry on failure).
- **Overview & understanding console (S3):** Overview = Confidence → Start here → Progress → More; confidence pill + click popover; neutral false-confidence flag; "how this is calculated"; direction-only movement; "Strengthened" trend. Issues are shown as **summary counts only** (D045) — confirmations live in the Issue detail (now built out here).
- **Attention map (S4):** heatmap-only; rows = 7 plan artifacts × columns = Clarity · Alignment · Feasibility; severity-only cell color; empty + all-clear states; co-primary placement + context preservation.
- **Artifact Workspace (S5):** left-rail explorer with live issue badges, type-aware editor (prose / mixed / tables), inline weakness annotations, epistemic notation (From OSLO / Confirmed by you), the full editor feature set (undo/redo, tables, slash menu, find/replace, RTF toolbar, weakness stepper), event-driven debounced reanalysis. **All intact.**
  - **Rev 7 fix (annotation hover popover):** the weakness summary popover now renders **above** the annotation (flipping **below** near the top so it never sits under the artifact toolbar) as a single, **fully opaque**, viewport-anchored surface — fixing a bug where editor content bled through it (looked transparent) when it overlapped the header under the app-shell. Behavior is otherwise unchanged: hover or focus/tap the ⚠ shows the summary + "Open issue →"; clicking the weak text still edits it.

## NEW in Slice 6

### A fourth co-primary view: Issues (D086)
The top-center view switch now reads **Overview · Attention · Issues · Artifacts**. The **Issues** button carries a live open-count badge. Selecting it opens the **all-issues surface** in the center pane (the persistent OSLO chat rail stays to the right; individual issues still open as a contextual panel over the list — Panel Model, D009).

### The all-issues list, filters, and group toggle (D086, D092b)
- **Group toggle "By dimension / By severity / By artifact"** at the top. *By dimension* groups the issues under Feasibility · Clarity · Alignment. *By severity* shows a **triage strip** (Critical / Moderate / Warning counts) and groups by severity, most-urgent first. *By artifact* (D092b) groups the issues under their plan-artifact headers in plan order — Intent · Context · Scope · Requirements · Work breakdown · Schedule · Resources — showing only artifacts that hold issues; within each group, most-urgent first. All three tabs share styling/keyboard behavior and active-state.
- **Subtitle (D092b):** the sub-line is now the minimal, static **"What needs your attention"** in every mode. The earlier verbose tails ("most urgent first. Severity is qualitative", "grouped by dimension …") are gone — the group tabs already name the grouping, so the subtitle carries no mechanism copy.
- **Filters:** **Artifact · Dimension · Severity · Status.** The artifact-scoping filter is labeled **"Artifact"** (never "Section" — D049). The Artifact row is built live from the artifacts that actually hold issues, with per-artifact counts; empty artifacts are dimmed. Dimension = Clarity · Alignment · Feasibility. Severity = Critical · Moderate · Warning. Status = Open (default) · Resolved · All.
- **Honest "N hidden by filters · clear":** when filters hide some issues, the list footer states exactly how many are hidden and offers a one-click **clear**. The count line ("6 open", "2 open (filtered)", "1 resolved") never overstates.
- **Per-issue card:** title + a **severity chip** (color only, D003) + **location** (`Artifact · Dimension`, e.g. "Requirements · Clarity") + **lifecycle status** pill (Open / Addressed / Resolved) + a **❓ clarification** flag when one is pending. Clicking (or Enter/Space) opens the full Issue Panel.

### The full Issue Panel (D087) — graduated from the light panel
Opening any issue (from the list, an Attention cell, an inline annotation, the Overview "Start here", or the chat) opens the same contextual panel, now full:
1. **Header** — title · severity chip · `Dimension · Artifact` (the Artifact is a link to open that artifact in the workspace) · issue id · the **lifecycle track** Open → Addressed → Resolved (current stage lit) · a single subtle **ⓘ hover** beside the track — the one place the honesty guarantee is stated: *"Issues close as OSLO's understanding updates — you don't close them by hand."* (D092, single-home + hover §6.7).
2. **Why this matters** — the plain-language consequence.
3. **Evidence** — a **collapsible** list of traceable sources ("N sources, traceable to your inputs"), collapsed by default.
4. **What this weakens** — the Clarity / Alignment / Feasibility impact for this issue's dimension.
5. **Recommendations** (see below) — only when the issue is not yet resolved.
6. **History** — a short pointer ("Detected in your last analysis… Open full timeline →") that opens the **Slice-7 seam**; the full timeline is not built here.

> **Copy hygiene (D092).** The panel no longer carries standing "reanalysis" chrome. The honesty guarantee lives in **exactly one** subtle ⓘ hover on the lifecycle track (item 1), phrased as an outcome — no "reanalysis" mechanism word anywhere user-facing. The former standing `.ip-rean` note, the clarification standing line, and the apply-note mechanism copy were removed; user-facing statuses read **"Updating…"** rather than "Re-analyzing…". The lifecycle logic, apply-fix behavior, and how issues actually close are unchanged — still driven by reanalysis under the hood.

### Lifecycle: Open → Addressed → Resolved (D088)
The three-step track shows in the header. **There is no Acknowledge stage and no manual "Resolve" button.** Acting on an issue (selecting a resolution path, applying the fix, or answering a clarification) advances it to **"Addressed · updating…"**. The issue reaches **Resolved** only as OSLO's read updates to confirm it no longer holds (reanalysis under the hood, D088) — surfaced everywhere consistently (the card pill, the Attention cell dropping out, the artifact badge, the Overview counts). Per D092 the user-facing copy states this as an outcome, not a mechanism.

### Recommendations + Apply this fix (D089) — inside the Issue only
- **OSLO Recommended** — a single recommended action, tagged **From OSLO (Derived)**.
- **Apply this fix** — one action. Where OSLO **can draft** the change, applying **drafts it into the plan** (simulated), marks the tied artifact **Confirmed by you**, and advances the issue **Addressed** (transient **"Updating…"**) then **Resolved**. Confidence then moves **direction-only** (▲/▼ with a named cause — no fabricated number, D056). Behavior unchanged; only reanalysis closes it under the hood. The user-facing apply-note is trimmed to what applying does (D092) — no mechanism copy.
- **Possible resolution paths** — selectable options; choosing one records it as the **Selected Path = Confirmed by you** and advances the issue to Addressed. A **"Write my own fix in {Artifact} →"** link opens the artifact editor.
- **No recommendations exist outside the Issue** (D009): there is no standalone recommendations surface or orphan roll-up.

### Clarification loop in the panel (D090)
Thin-evidence issues carry a **Clarification request** block (question + answer input, a short neutral prompt "Add the detail OSLO is missing.", and a **Submit answer** button). Answering **updates the project info**, marks the tied artifact attested, and the issue **closes** as OSLO's read updates — consistent with the Slice-2 handling, now living inside the full panel. Per D092 the standing mechanism line was removed and the button is "Submit answer" (was "Submit & re-analyze"); behavior is unchanged.

### Four honest empty states (D091)
- **None-found** — "No issues — your plan looks clear" (all issues resolved).
- **None-under-lens** — "Nothing under this lens" with a **clear-filters** link (filters hide everything).
- **Not-yet-analyzed** — "Analysis hasn't finished yet" (analysis pending).
- **Unavailable** — "Issues are temporarily unavailable… this is a technical problem, not an all-clear" (load error).
Plus the honest **hidden-by-filters** count. A subtle **prototype-preview** control under the list makes the not-yet-analyzed / unavailable states reachable for review.

### Attention-map routing graduated (D058 → D086)
The Slice-4 cell routing now opens **into this full surface**: a cell with exactly one active issue opens that issue's full panel; a cell with several opens the **Issues center pane scoped** to that Artifact × Dimension (both filters lit). No separate scoped scrim — one consistent Issues destination.

---

## Boundaries (unchanged doctrine)
- **Advisory-only (D001):** OSLO advises; you decide and act. Nothing says OSLO "resolves" or "plans it for you." Issues close only via reanalysis.
- **Severity color only (D003):** red/amber on severity; confidence/CAF stay neutral.
- **Not built here (seams):** threaded comments / @mentions → Slice 9; the full History timeline → Slice 7 (the panel leaves a labeled pointer).

## Command palette — search / jump-to (D094)
Pressing the top-bar **⌕** or **⌘/Ctrl+K** opens a centered command palette — one keystroke to search or jump anywhere. A **"Search or jump to…"** input (autofocused) filters live, case-insensitive, across three grouped lists (empty groups disappear as you type):
- **GO TO** — Overview · Issues · History · Attention map (jumps to that view).
- **PLAN ARTIFACTS** — the seven artifacts (WBS reads "Work breakdown") — opens the artifact.
- **OPEN AN ISSUE** — every still-open issue, showing its title and a muted **"{Severity} · {Artifact}"** (e.g. "Keynote backups are unconfirmed — Moderate · Resources") — opens the issue's full panel.

The palette is fully keyboard-driven: **↑↓** move the highlight (the first result is pre-highlighted), **↵** opens the highlighted item, **Esc** (or a click on the dim scrim) closes it; clicking a row also opens it. On activation the palette closes first, then the destination is shown. The highlight is a neutral surface tint — issue rows name their severity in text, but the palette never uses severity color as a health signal (D003). Canonical terms are kept: the approved reference image labels these lists "Findings" / "OPEN A FINDING", but the ratified **Issues** / **OPEN AN ISSUE** wording is used. The palette and the issue flyout are never open at the same time.

---

## Chat integration (D108 cascade)

OSLO's rail stops being decoration in this slice. You can **type to it** — Send, or just press Enter (Shift+Enter for a new line) — and it answers from what it actually knows about *your* plan: the band and the reliability qualifier, the limiting dimension, how many issues are open and which one it would take first, what's open in the artifact you have on screen, and the recommendations attached to an issue. It never invents a number or an issue, and it never quietly does anything: **it reads and explains, you decide** (D001). It cannot select a path, cannot edit an artifact, and cannot close an issue — an issue reaches **Resolved** only when an analysis update confirms the gap no longer holds (D088), and OSLO says so rather than pretending otherwise.

**Context travels with you.** Every surface can hand what you're looking at to the chat, and a **context pill** at the top of the rail names it ("Keynote backups are unconfirmed (ISS-03)", "Resources · plan artifact", "Your confidence read", "Resources × Feasibility · Attention map"). Answers stay inside that context until you clear it with the pill's **×** — then OSLO widens back out to the whole project. The suggested chips under the composer change with it: unscoped they offer "What should I do next?" and "Why is Feasibility Very Low?"; inside an issue they offer "Why does this matter?", "What are my options?", "What happens if I leave it?".

**Where you can hand something over**
- **Overview** — "✦ Ask OSLO why" sits right under the confidence number.
- **Attention map** — after a cell routes you to the scoped Issues list, "Ask OSLO about this cell →".
- **Issue panel** — "✦ Ask OSLO about this issue →", and "Answer in chat →" beside any clarification.
- **Artifact editor** — the ✦ button in the toolbar, and "Ask about this →" in the popover on any weak span.
- **Recommendations** — **Discuss**, on OSLO Recommended and on every resolution path.

**Discuss is the one to notice.** Every recommendation and every resolution path now carries a quiet **Discuss** link. Clicking it opens the conversation about *that* path: what it buys you, what it costs, how it stacks up against the other paths and against OSLO's own recommendation. Crucially, **discussing is not choosing** — the path is not selected, the issue does not move to Addressed, nothing is recorded. The panel says so out loud ("Discussing changes nothing"), and OSLO repeats it in the answer. If, having weighed it, you *do* want that path, OSLO offers **Select this path →** — but you have to click it. Selecting stays an explicit, deliberate act that you take.

**Questions can be answered in the conversation.** When OSLO needs something confirmed, it can raise the question in the chat with an answer box, and answering there does exactly what answering in the Issue panel does: your project information updates, the artifact becomes **Confirmed by you**, the issue moves to **Addressed**, and the analysis update that follows moves it to **Resolved** — after which OSLO reports the new read back to you in the thread. The chat is never a side channel around the lifecycle. And if the same question comes up again in a longer conversation, there is only ever **one live answer box** for it — the earlier ones stand down so you can't answer the same question twice by accident.

The thread is a polite live region, so replies are announced to screen readers as they land, and every in-reply action is a real, keyboard-operable link into the surface it names.
