# Slice 6 — Issues & Recommendations (Panel Model) · User Experience

**Release:** OSLO R1 (ALPHA). **Cumulative:** Slice 1 + 2 + 3 + 4 + 5 + 6.
**Baseline of record:** frozen prototype (md5 `a327d702`, boot 157/157).
**Boundary:** advisory-only (D001); OSLO reads and explains — nothing changes the plan or resolves an issue without the user (D001/D088); severity red/amber/green belongs to issues, the read stays neutral (D003); recommendations live ONLY inside the issue (D009); dark default + WCAG 2.1 AA (D015). Client-side prototype only (D016).

> This document notes what is **INHERITED** from Slices 1–5 (unchanged) and what is **CURRENT in Slice 6**. Nothing prior regresses. **This is a regeneration to match the frozen build.** The original July-9 slice-06 docs (a standalone Issues list beside a separate "Attention map" nav row, an "Acknowledge" lifecycle step, a hand-resolvable issue) are **retired** — the build now consolidates Issues and Attention into **one destination with a Map ⇄ List toggle** (DL-136), removes Acknowledge (D094), resolves an issue only by an analysis update (D088), and carries two **task-altitude findings** (ISS-10/11) through the same engine on the deeper read.

---

## What Slice 6 is

Slice 6 is OSLO's **issue engine** — the surface a PM works when they ask *"what's wrong, and what do I do about it?"* It owns: the **all-issues destination** (Map ⇄ List), the **issue panel**, the **lifecycle** (Open → Addressed → Resolved), the **resolution paths** (Selected option → Apply this fix → analysis update resolves), the **clarification requests**, and the **CAF dimension drill-down**. Individual issues always open as a contextual panel over whatever surface routed to them (Panel Model, D009).

The organising idea: an issue is a finding OSLO surfaced, and the user is always the one who acts on it. OSLO can draft a fix, but **only an analysis update ever marks an issue Resolved** — never a manual button (D088/D094). A rising issue count is a **deeper read, not a regression** (a deeper analysis finds more and firms the read at once, D177).

> **Boundary with Slice 11.** The engine now carries two **task-altitude findings** — **ISS-10 "The freeze rests on undated tasks"** and **ISS-11 "Part of the breakdown is inferred"** — surfaced on the deeper read. The engine (list · panel · lifecycle · CAF drill) is Slice 6's; the **task-altitude analysis that produces them** (the WBS task tree, the critical path, the low-confidence decomposition) is **Slice 11's** (`slice-11-execution-ready-planning-export`). This doc documents that the engine carries them and cross-references Slice 11 for how they are produced; it does not re-document the task model.

---

## INHERITED (unchanged)

- **Slice 1/2:** activation funnel; four-method intake; Fast Pass ≈30s; read-led Overview; the clarification loop (a light prompt in *Start here* + the question/answer inside the tied issue → analysis update → issue closes); completion notices in OSLO chat; analysis-state machine.
- **Slice 3:** the Overview's persistent Outcome Confidence read, the CAF rows, the top-bar chip + popover, and the **beat-aware "Start here" re-ranking** — that re-ranking is the **Overview's** surface, NOT the Issues list. The full Issues list is grouped and filtered, never beat-ordered.
- **Slice 4:** the Attention heatmap (7 documents × Clarity · Alignment · Feasibility; brighter = more attention, not health — D062/D060); cell → issue routing (`openFindingsFor`, D058); the all-clear empty state (D061).
- **Slice 5:** the Artifact Workspace + editor; epistemic notation ("From OSLO" / "Confirmed by you"); event-driven reanalysis (no manual "Reanalyze" button).
- **App shell:** persistent left sidebar (Overview · **Issues** · History · Inference map · Reports · Documents · Full plan), top bar, command palette, chat rail. Chrome neutral; severity colour on issues only.

---

## CURRENT in Slice 6 — top to bottom

### 1. The all-issues destination — one place, two views (DL-136)

The old separate "Attention map" nav row is **retired**. Issues and Attention are **one destination** reached by the single **Issues** sidebar item; a **Map ⇄ List toggle** (`.iaview-toggle`) sits at the top of both views. The **Map is the default** (`_iaView='map'`); the last view the user saw persists (`_iaView`) so re-entry is consistent. The breadcrumb reads **"Issues · Map"** or **"Issues · List"** (`_viewLabel`). The single **Issues** sidebar item stays active for both.

- **Map view** (`#pane-attention`): heading **"Where your plan needs attention"** over the heatmap (Documents × Clarity · Alignment · Feasibility). Brightness is attention, not a health score. Clicking a cell investigates: exactly one open issue → that issue's panel; more than one → the List, scoped to that document × dimension with both filters lit and an "Ask OSLO about this cell →" affordance. All-clear when nothing is open (D061).
- **List view** (`#pane-issues`): heading **"Issues"** + a live count + "What needs your attention." A **group toggle** (By dimension · By severity · By document) and **filters** — Document · Dimension · Severity · Status (Open · Resolved · All). Under *By severity* a triage strip counts Critical · Moderate · Warning. A multi-dimensional finding appears under **each** of its dimensions (CAF §8.3). Honest **"N hidden by filters · clear"** when a filter conceals issues.
- **Four honest empty states** (`_issEmpty`, D091), each a distinct truth: **none-found** ("No issues — your plan looks clear"), **none-under-lens** ("Nothing under this lens" — filters hide them), **not-yet-analyzed** ("Not yet analyzed" — the read isn't in yet), and **unavailable** ("Issues are temporarily unavailable · This is a technical problem, not an all-clear"). An all-clear and a failure never wear the same face.

### 2. The issue panel (`openIssue`, D087) — progressive disclosure by intent

A contextual flyover. The user opens it to learn *what's wrong and what to do*; everything else is one scannable, keyboard-accessible row (D162b). Top to bottom:

- **Header:** severity chip + title + close. **Meta:** Dimension · Artifact (a link into the document where it lives) · Issue id.
- **Lifecycle chip** (Open ⇄ Addressed ⇄ Resolved): the states are drawn with **`⇄` arrows and no trailing fill** — only the state the issue is actually in is lit, because the states are **reversible** and the chip is state, never progress (D192b). An ⓘ says what moves it: an analysis update moves it forward, withdrawing a decision can bring it back — either way the analysis moves it, never a manual step.
- **Why this matters** (the plain-language read) → **`<dimension>` impact** (what it weakens).
- **OSLO recommends** — the recommendation the button would apply, **resident above its own button** (D184: a fix the user cannot read is one they cannot consent to). **"Apply this fix"** (`applyFix`) is the single primary action; **"Discuss"** hands it to chat (changes nothing); **"Other options (N)"** expands the alternatives in place — each selectable (Select → *Confirmed by you*) or discussable, plus a free **"Write my own fix in `<document>` →"** door. Applying is OSLO doing the edit; writing it yourself is always free.
- **Evidence** (collapsible row, cited by document) · **Clarification** (when OSLO is the one asking — collapsed by default; the textarea appears when the user chooses to answer) · **Reviews** (attestations) · **Comments** — each a row.
- **Actions:** ⤴ Share for review (never disabled, never metered — CR-2) · ✦ Discuss with OSLO.
- **History pointer** into the full timeline (Slice 7).

### 3. Lifecycle Open → Addressed → Resolved (D088/D094)

- **Acknowledge is gone** (D094). There is **no manual "Resolve."**
- **Select an option** (`selectPath`) moves Open → Addressed — an *intention*, freely clearable back to no selection (nothing in the plan changed, nothing attested).
- **Apply this fix** (`applyFix`) or **answer a clarification** (`_submitClarification`) moves Open → Addressed, marks the tied document **Confirmed by you**, and raises its Reliability. About ~1.9s later the **analysis update lands and moves it to Resolved** — **only an analysis update ever resolves** (D088). The panel shows *"✓ Resolved by the analysis update."*
- **Every decision has a withdraw.** A selection clears; a fix or answer is withdrawn — named for what it does ("Withdraw this fix" / "Withdraw this answer" / "Clear selection"), never "Undo." Withdrawing is the user retracting *their own word* on *their own document*; the read then moves **by analysis**, which re-opens the issue if the gap is genuinely back (D191/D192a). OSLO never deletes the user's own writing to undo its change (D193a); the attestation is refcounted so a document stays confirmed while any standing decision attests it (D193b). **No hand-path ever moves the read** (D191).

### 4. Resolution paths & clarifications

- **Resolution paths → Selected option (Attested).** OSLO's own recommendation plus alternative options; the user selects one (or writes their own). The recommendation the Apply button carries is **computed by rank** (moves the limiting dimension · is appliable · matches the user's selection), never an array index (D184.3).
- **Clarification requests** — where OSLO is the one asking, the panel carries the question and answering (in the panel *or* in chat) runs the **same** door (`_submitClarification`, D108): the same project-info update, the same lifecycle move, the same timeline entry (D096). The chat is not a side channel and never claims to have closed an issue itself.

### 5. CAF dimension drill-down (Option C · DL-116/DL-123/124)

On the Overview read, each CAF row (Clarity · Alignment · Feasibility) shows a mini ramp + level word + a **per-dimension evidence cue** ("Mostly inferred · 1 of 3"). **Level ≠ trust:** the cue is provenance, never folded into the band. Clicking the row toggles a drill-down (`toggleCafDrill`): **Rests on** (grounded/inferred split), **Held back by** (open issues by severity), the **most-severe open issue** as a card routing to its panel, **To lift it** (the top issue's own recommendation), and a Level-2 **finding-type cut** routing each issue to its panel. **The band stays a band — only the drivers are quantified** (DL-116). **Alignment is live** (D133): an attested reviewer **Approve or Reject** is evidence about alignment and moves it **symmetrically** — a stakeholder disagreeing lowers Alignment, which is information about alignment, not a verdict that the plan is wrong. It **never** resolves, re-opens, or invalidates the issue.

### 6. Task-altitude findings on the deeper read (ISS-10 / ISS-11 · Slice 11 analysis)

The deeper (Extended) read surfaces two findings through the **same engine** (`_deepPassSurfaceFindings` — the one door; from that instant they are ordinary issues in every list, count, heat cell, and panel):

- **ISS-10 "The freeze rests on undated tasks"** (Moderate · Feasibility · WBS) — the Sep 1 run-of-show freeze depends on undated upstream tasks.
- **ISS-11 "Part of the breakdown is inferred"** (Moderate · Clarity · WBS) — OSLO's honest read on its **own** low-confidence decomposition. Framed as **evidence honesty, never a warning about the plan** (DL-109).

They raise the **Work breakdown (WBS) open count 1 → 3** (ISS-05 was the only prior WBS issue) and route through the existing recommendation/confirm paths exactly like ISS-01…06. *(See Slice 11 for how the task-altitude analysis produces them.)*

---

## Journey (Slice 6 lens)

1. From the Overview, a limiter or a Start-here item routes into the **issue panel** (or the user opens the **Issues** destination — Map by default).
2. On the **Map**, the user reads where attention clusters and clicks a cell; on the **List**, they group/filter and open a card. Either way the **same panel** opens over the surface.
3. In the panel: read *Why this matters* and the *`<dim>` impact*, then **Apply this fix**, **Select an option**, **Write their own fix**, or **Answer a clarification**. The issue moves to **Addressed**.
4. The **analysis update lands** (~1.9s) → the issue moves to **Resolved**, the read firms direction-only, the payoff shows what changed. The user may **withdraw** at any point — the analysis re-opens the issue if the gap is back.
5. On the **deeper read**, ISS-10/11 appear; the count rises and the read firms in the same payoff (D177). Nothing is gated; the calls stay with the user (D001).

---

## Chat integration (inherited, adapted to Slice 6)

The OSLO rail is advisory (D001). The issue panel hands any issue to the chat; answering a clarification in chat runs the identical `_submitClarification` path (byte-identical history, D096); a reviewer's response is narrated as evidence, never as OSLO's verdict, and it resolves nothing on its own. The chat mutates nothing and never claims to have closed an issue.
