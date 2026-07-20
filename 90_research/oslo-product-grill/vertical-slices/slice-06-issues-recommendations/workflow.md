# Slice 6 — Issues & Recommendations (Panel Model) · Workflow

Cumulative (Slices 1–6). Actor workflows on the issue engine of the frozen build. Actors: **User** · **System** (client-side prototype render/state) · **AI** (simulated OSLO — timers + fixed illustrative data; no real model, no network).

> Regenerated to match the frozen build. Flows reference the consolidated Map ⇄ List destination (DL-136), the Acknowledge-free lifecycle (D094), and analysis-only resolution (D088). The retired separate "Attention map" nav row and the hand-resolve path are gone.

## Preserved end-to-end journey (INHERITED)

Invite → Activate → Welcome → Intake (4 methods) → **Fast Pass ≈30s** → read-led Overview → **Outcome Analysis** auto-runs, non-blocking, supersedes provisional→current → the clarification loop closes issues via an analysis update. Completion notices land in OSLO chat. Optional tour.

## Flow A — Reach the issue engine (Map default)

1. **User** clicks the single **Issues** sidebar item (or a cell / Start-here item routes in).
2. **System** opens the last-seen view (`_iaView`, default **Map**); the crumb reads "Issues · Map". The Map (`renderHeat`) shows where the plan needs attention (D062).
3. **User** toggles **Map ⇄ List** — `showView('issues'|'attention')` switches the pane, persists `_iaView`, updates the crumb, keeps the **Issues** nav item active for both.

## Flow B — Map → panel

1. **User** clicks a heat cell.
2. **System** routes (`openFindingsFor`, D058): exactly one open issue → `openIssue`; more than one → the List scoped to that document × dimension (both filters lit) + "Ask OSLO about this cell →".
3. **System** re-renders the map live on entry so counts and routing agree.

## Flow C — List → group/filter → panel

1. **User** picks a grouping (By dimension / By severity / By document, `setGroup`) and filters (Document · Dimension · Severity · Status, `setFilt`).
2. **System** re-renders (`renderIssues`): grouped cards, triage strip under By severity, a multi-dim issue under each dimension, and an honest "N hidden by filters · clear". This is a **grouped/filtered list — not beat-ordered** (the beat re-ranking is the Overview's, Slice 3).
3. **User** opens a card → **System** opens the issue panel over the list (Panel Model, D009).

## Flow D — Read the panel (D087/D162)

1. **User** reads, always visible: severity · title · Dimension · Artifact · Issue id · the lifecycle chip · **Why this matters** · **`<dim>` impact** · the recommendation (resident above its button) · ONE primary action.
2. **User** expands a row (Evidence · Clarification · Reviews · Comments) — each independent, keyboard-accessible, `aria-expanded`; a contract lives on an ⓘ, never resident.
3. **System** draws the lifecycle as `Open ⇄ Addressed ⇄ Resolved` — `⇄` arrows, no trailing fill, only the current state lit; the ⓘ says an analysis moves it, never a manual step (`_assertLifecycleIsNotDrawnAsARatchet`).

## Flow E — Resolve by applying OSLO's fix (D088/D089/D184)

1. **User** clicks **"Apply this fix"** (`applyFix`) — the recommendation is on screen; the button is built from the same object (`_primaryRec`, computed rank).
2. **System** captures the pre-fix record (`_decision`), marks the tied document **Confirmed by you** + raises Reliability, moves the issue **Open → Addressed**, bumps the version, pushes history; shows "Updating…".
3. **AI** runs the analysis update (~1.9s) → **System** sets `_istatus='resolved'` (**only the update resolves**, D088), firms Feasibility if a critical Resources gap cleared, pushes a **direction-only** trend (D056), renders the payoff, routes a notification. The panel shows "✓ Resolved by the analysis update."
4. The assisted-apply cap is **unset** in normal operation — nothing is metered, the recommendation is never hidden, the free manual door is always open (`_assertRecommendationNeverHidden`).

## Flow F — Resolve by selecting an option or writing your own

1. **User** expands **Other options** and clicks **Select** on one (`selectPath`) → **System** moves Open → Addressed (a *selection is an intention* — nothing attested, freely cleared). Or **User** clicks **"Write my own fix in `<document>` →"** → **System** opens the artifact editor; a real edit runs the inherited reanalysis (Slice 5), which resolves via analysis update.
2. **User** may **Clear selection** (`clearSelection`) → back to **Open**; an append-only history event stays.

## Flow G — Clarification loop (D090/D108)

1. **User** answers OSLO's question in the panel (or in chat — same door).
2. **System** runs `_submitClarification`: updates project info, marks the tied document Confirmed by you + raises Reliability, moves the issue Open → Addressed, records the answer (`_clarAnswered`); byte-identical history whichever surface (D096).
3. **AI** runs the analysis update → **System** resolves the issue → refines the read (direction-only) → re-renders every issue-aware surface. The chat never claims to have closed the issue.

## Flow H — Withdraw a decision (D191/D192a/D193)

1. **User** clicks the withdraw affordance (named for what it does — "Withdraw this fix" / "Withdraw this answer" / "Clear selection", never "Undo").
2. **System** raises the consent line with the subject on screen; on confirm, `_withdrawUnit` drops the attestation, restores the pre-fix document **only if untouched** (`_docTouchedSince`) — a touched document is never restored (D193a) — and restores Reliability via the refcount (D193b).
3. **AI** re-reads the plan; **System** re-opens the issue if the gap is genuinely back. Withdraw survives a resolved status; **no hand-path moves the read** (`_assertWithdrawSurvivesResolution`/`_assertNoHandPathMovesTheRead`).

## Flow I — CAF drill-down (Option C · DL-116) + Alignment live (D133)

1. **User** clicks a CAF row on the Overview read (`toggleCafDrill`) → **System** shows Rests on / Held back by / the top open issue card / To lift it / a Level-2 finding-type cut — each routing to `openIssue`. **The band stays a band; only drivers are quantified.**
2. **AI** (Simulate ▾ → "Sim reviewer response") lands a reviewer **Approve or Reject** as evidence (`_reviewAnalysisRun`) → **System** moves **Alignment symmetrically** (±`ALIGN_STEP`), pushes to `ALIGN_EVIDENCE`, and renders the payoff — a Reject can make the read **fall**, drawn exactly like a rise (D173c). The response is **Attested by `<name>`**; the tied **issue does not move** — a review never resolves, re-opens, or invalidates it. Evidence is never gated (`_assertEvidenceNeverGated`).

## Flow J — Task-altitude findings on the deeper read (ISS-10/11)

1. **AI** completes the Extended (deep) pass → **System** calls `_deepPassSurfaceFindings()` (the one door) → surfaces **ISS-10** and **ISS-11** into `ISSUES`/`_istatus`.
2. **System** re-renders every surface: the WBS **open count rises 1 → 3**, the map and list carry them, and the payoff shows more issues **and** a firmer read in the same block (D177). ISS-11 is OSLO's honest read on its own decomposition — **never a warning** (DL-109).
3. From this instant they behave exactly like ISS-01…06 (confirm / select / write-your-own). *(The task-altitude analysis that produced them is Slice 11's.)*

## Flow K — Empty & honest states (D091)

**System** distinguishes four (`_issEmpty`): none-found (all-clear) · none-under-lens (filters hide them) · not-yet-analyzed · unavailable ("a technical problem, not an all-clear"). An all-clear and a failure never wear the same face.

## Simulated-AI boundary

All analysis is timers + fixed illustrative data. Lifecycle, counts, CAF drivers, the deep findings, and Alignment movement are all **computed from live state** (D173) — never authored. Resolution obeys D088 (only an analysis update resolves) and movement obeys D056 (direction + cause) in every simulated path. OSLO reads and explains; the calls stay with the user (D001).
