# Slice 6 — Issues & Recommendations (Panel Model) · Success Criteria

The developer's checklist for the issue engine of the frozen build (md5 `a327d702`, boot 157/157). **FREEZE-INTACT:** these assert the build as frozen — not new enhancements. Guard names and doctrine refs are cited per item.

## Cumulative-integrity (no regression)
- [ ] SC-0 Every Slice 1–5 route, screen, interaction, theme token, and localStorage key still works (activation funnel, four-method intake, Fast Pass ≈30s, read-led Overview, heatmap, artifact workspace + editor, chat + notices, tour, analysis-state machine).
- [ ] SC-0b The build boots green (157/157 guards) with no console error.

## The all-issues destination — Map ⇄ List (DL-136)
- [ ] SC-1 Issues and Attention are **one destination** reached by the single **Issues** sidebar item; a Map ⇄ List toggle fronts both views; the old separate "Attention map" nav row does not exist (`_syncNav` — `#sbIssues` active for `issues` and `attention`).
- [ ] SC-2 The **Map is the default** view; the last-seen view persists (`_iaView`) so re-entry is consistent (`showIssuesView` / `showView`).
- [ ] SC-3 The breadcrumb reads **"Issues · Map"** or **"Issues · List"** per view (`_viewLabel`).
- [ ] SC-4 The Map's heading is **"Where your plan needs attention"**; brightness is attention, not a health score (D060/D062); all-clear is honest (D061).
- [ ] SC-5 The List (`renderIssues`) offers group tabs (By dimension default · By severity · By document) and filters **Document · Dimension · Severity · Status**; a multi-dimensional finding appears under **each** of its dimensions (CAF §8.3, `_dimsOf`).
- [ ] SC-6 A filtered list shows an honest **"N hidden by filters · clear"**; a map cell routing in shows the scoped header + "Ask OSLO about this cell →" with both filters lit (D058).

## The issue panel (D087/D162)
- [ ] SC-7 The panel opens as a contextual flyover over whatever surface routed to it (Panel Model, D009); **recommendations exist ONLY inside the issue** (D009).
- [ ] SC-8 Always visible: severity · title · Dimension · Artifact link · Issue id · the lifecycle chip · **Why this matters** · **`<dimension>` impact** · the recommendation · ONE primary action. Everything else is a collapsible row with `aria-expanded` (D162b).
- [ ] SC-9 The panel order is **Header → Why → Evidence → `<dim>` impact → Recommendations → History pointer → reanalysis note**, and Evidence cites its documents.

## Lifecycle Open → Addressed → Resolved (D088/D094)
- [ ] SC-10 There is **no "Acknowledge"** step and **no manual "Resolve"** button anywhere (D094).
- [ ] SC-11 An issue reaches **Resolved only via an analysis update** — never by hand (D088); `_active` treats open and addressed alike until the update lands.
- [ ] SC-12 The lifecycle chip is drawn with **`⇄` arrows and no trailing fill** — only the current state is lit; the ⓘ says the analysis moves it, never a manual step (`_assertLifecycleIsNotDrawnAsARatchet`, D192b).
- [ ] SC-13 Every writer of `addressed`/`attested` has a declared, reachable inverse (`_ISSUE_TRANSITIONS`: `selectPath`→`clearSelection`, `applyFix`/`_submitClarification`→`withdrawDecision`); a one-way transition fails the build (`_assertEveryDecisionTransitionHasAnInverse`).

## Resolution paths & Apply this fix (D089/D184)
- [ ] SC-14 The recommendation the Apply button would apply is **resident above the button**, and the button is built from the same object (`_primaryRec`); **no renderable recommendation ⇒ no button** (`_assertApplyAffordanceShowsItsRecommendation`, D184).
- [ ] SC-15 The primary recommendation is **chosen by computed rank** (`_recRankScore` — appliable · moves the limiting dimension · matches the user's selection · OSLO's own), never an array index (`_assertRecommendationRankIsComputed`, D184.3).
- [ ] SC-16 The single primary action label is the constant **"Apply this fix"** (`APPLY_LABEL`/`_applyLabel`, one string across panel + chat, D190a).
- [ ] SC-17 Other options expand **in place** beneath the recommendation (Select = *Confirmed by you* · Discuss · the free **"Write my own fix in `<document>` →"** door); the options have **one home** (`_assertOptionsHaveOneHome`, D190c). The assisted-apply cap is unset in normal operation and **never hides the recommendation** (`_assertRecommendationNeverHidden`, DL-103 §7d).
- [ ] SC-18 Applying marks the tied document **Confirmed by you** + raises Reliability, moves the issue **Open → Addressed**, then the analysis update (~1.9s) moves it to **Resolved**, firms the read direction-only (D056), and renders the payoff (D088/D173b).

## Withdraw — every decision is reversible (D191/D192/D193)
- [ ] SC-19 Every decision has a withdraw named for what it does ("Withdraw this fix" / "Withdraw this answer" / "Clear selection", never "Undo", `_wdLabel`); an act that touches the document raises a consent line with the subject on screen first (D191/D184).
- [ ] SC-20 Withdraw is available even on a **Resolved** issue; withdrawing drops the attestation and the **analysis** re-opens the issue — no hand-path moves the read (`_assertWithdrawSurvivesResolution` / `_assertNoHandPathMovesTheRead`, D192a).
- [ ] SC-21 A document edited since the fix is **never restored** — OSLO never deletes the user's writing (`_docTouchedSince`, `_assertWithdrawalNeverDeletesTheUsersWriting`, D193a); the attestation is **refcounted by decision** and Reliability restores to its pre-first-attestation value (`_assertAttestationIsRefcountedByDecision`, D193b).

## Clarification requests (D090/D108)
- [ ] SC-22 A clarification is answerable in the panel **or** in chat through the **same door** (`_submitClarification`) with byte-identical history (D096); the chat never claims to have closed the issue.
- [ ] SC-23 Answering updates project info, attests the tied document + raises Reliability, moves Open → Addressed, and the analysis update resolves it (D088). The clarification row defaults minimized — the textarea appears on demand (D162c).

## Four honest empty states (D091)
- [ ] SC-24 The list distinguishes **none-found · none-under-lens · not-yet-analyzed · unavailable** (`_issEmpty`); "unavailable" states plainly it is a technical problem, **not an all-clear**.

## CAF drill-down — Option C (DL-116/DL-123/124)
- [ ] SC-25 Each CAF row carries a mini ramp + level word + a **per-dimension evidence cue**; **level ≠ trust** — the cue is provenance, never folded into the band.
- [ ] SC-26 Clicking a row toggles a drill-down (`toggleCafDrill` → `_cafDrillHTML`): Rests on · Held back by · the top open issue card · To lift it · a Level-2 finding-type cut — each routing to `openIssue`. **The band stays a band; only drivers are quantified** (DL-116).

## Alignment is live (D133)
- [ ] SC-27 An attested reviewer **Approve or Reject** is evidence about **Alignment** and moves it **symmetrically** (`ALIGN_STEP`, `_reviewAnalysisRun`); a Reject can make the read **fall**, rendered exactly like a rise (D173c).
- [ ] SC-28 A review response is recorded as **Attested by `<name>`** and **never resolves, re-opens, or invalidates** the tied issue; evidence is **never gated on any tier** (`_assertEvidenceNeverGated`, D126).

## Task-altitude findings on the deeper read (ISS-10/11 · Slice 11 analysis)
- [ ] SC-29 The deeper read surfaces **ISS-10 "The freeze rests on undated tasks"** (Feasibility · WBS) and **ISS-11 "Part of the breakdown is inferred"** (Clarity · WBS) through the **same engine** (`_deepPassSurfaceFindings` — the one door); from that instant they behave exactly like ISS-01…06.
- [ ] SC-30 ISS-10/11 raise the **WBS open count 1 → 3** and route through the existing recommendation/confirm paths; ISS-11 is OSLO's honest read on its own low-confidence decomposition — **never a warning** (DL-109). The count can rise **and** the read firm in one payoff (D177).

## Cross-cutting
- [ ] SC-31 Advisory-only throughout (D001); **severity red/amber/green only on issues** (heat cells + issue badges); the read/CAF/lifecycle stay neutral (D003); dark default + light parity; WCAG 2.1 AA (focus, keyboard, reduced-motion).
