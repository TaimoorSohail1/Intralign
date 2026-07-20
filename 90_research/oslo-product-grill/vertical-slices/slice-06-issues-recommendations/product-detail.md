# Slice 6 — Issues & Recommendations (Panel Model) · Product Detail

**Scope:** the issue engine of the frozen R1 build (md5 `a327d702`) — the all-issues destination (Map ⇄ List), the issue panel, the lifecycle, the resolution paths and clarifications, and the CAF drill-down. Cumulative (Slices 1–6). Product behaviour only; no backend/API/DB.

> Regenerated to match the frozen build. The retired July-9 components — a standalone Issues list beside a separate "Attention map" nav row, an **"Acknowledge"** lifecycle step, and a hand-resolvable issue — are **gone** and are not documented as present. Issues + Attention are one destination (DL-136); resolution is by analysis update only (D088).

---

## Component: The all-issues destination — Map ⇄ List (DL-136) · `showView` / `_iaView`

- **One destination, two views.** The single **Issues** sidebar item routes here; a Map ⇄ List toggle (`.iaview-toggle`, `role="tablist"`) sits atop both. `_iaView` remembers the last-seen view (default `map`); `showView('attention')` sets it to the Map, `showView('issues')` to the List, so re-entry (`showIssuesView`) is consistent. The Attention-map cell-clicks and every "open the list" path already flow through `showView`, so the last view is tracked without touching those call sites.
- **Crumb** (`_viewLabel`): Map → **"Issues · Map"**; List → **"Issues · List"**. The single **Issues** nav item stays active for both (`_syncNav` — `v==='issues' || v==='attention'`).
- **Scroll memory** per pane (`_scrollMem`) restored on return.

## Component: Map view (`#pane-attention`) — the heatmap (D062/D057/D060/D061)

- Heading **"Where your plan needs attention"**; sub "Documents × Clarity · Alignment · Feasibility". Rendered by `renderHeat()`; always re-rendered on entry so cell counts are live.
- Rows = 7 documents × columns = Clarity · Alignment · Feasibility; cells shaded by **attention severity** (l0 none → l3 critical). Legend: **"Brighter = more attention — not a health score"** (D060). Severity ramp on cells only; the read stays neutral (D003).
- Cell → issue routing (`openFindingsFor`, D058): exactly one open issue → its panel; more than one → the List scoped to that document × dimension (both filters lit) + "Ask OSLO about this cell →".
- **All-clear** (`#heatClear`, D061): when nothing is open, "Nothing needs your attention right now … an all-clear on **attention** — not a guarantee of success."
- **The map's unique job (D062):** it says *where the plan needs attention*. (It is distinct from the Inference map, which says *where OSLO is guessing* — a peer pane, not this surface.)

## Component: List view (`#pane-issues`) — the all-issues surface (D086) · `renderIssues()`

- Heading **"Issues"** + live count (`#iss-count`, e.g. "5 open" / "(filtered)") + sub "What needs your attention". Re-rendered live on entry and after every lifecycle change (`_refreshIssueSurfaces`).
- **Group toggle** (`setGroup`, `_group`): **By dimension** (default) · **By severity** · **By document**. Order keys `_DIMORDER` (Feasibility · Clarity · Alignment) / `_SEVORDER` / `_ISSARTORDER`. This is a **grouped/filtered list — NOT beat-ordered**; the beat-aware "Start here" re-ranking is the Overview's (Slice 3).
- **Filters** (`setFilt`, `_filt`): Document (`renderArtFilters` — live per-document counts) · Dimension · Severity · **Status** (Open [active] · Resolved · All, `_statusMatch`). `clearFilt` resets Document/Dimension/Severity.
- **Triage strip** under *By severity* (`.triage`): Critical · Moderate · Warning counts.
- **Multi-dimensional findings** (CAF §8.3): under *By dimension* an issue with `dims:[…]` appears under **each** of its dimensions (`_dimsOf`).
- **Honest hidden count:** "N issue(s) hidden by filters · clear" when a filter conceals issues.
- **Per-issue card** (`_issueCard`): severity bar + title + location (Document · Dimension) + lifecycle status + a "❓ clarification" flag when the issue carries an unresolved `clar` + the "Awaiting review" chip. Opens `openIssue`. Severity colour only (D003).

## Component: Four honest empty states (D091) · `_issEmpty`

Each a distinct truth, never interchangeable:
- **none** ("No issues — your plan looks clear") — the all-clear.
- **none-lens** ("Nothing under this lens") — filters hide them; offers "Clear filters".
- **wait / not-yet-analyzed** ("Not yet analyzed") — the read isn't complete.
- **unavail / unavailable** ("Issues are temporarily unavailable · This is a technical problem, not an all-clear — nothing has been resolved.")

## Component: The issue panel (`openIssue`, D087/D162) — progressive disclosure by intent

- **Always visible (D162b):** severity chip + title + close; meta (Dimension · Artifact link `openIssueArtifact` · Issue id); lifecycle chip; **Why this matters** (`f.why`); **`<dimension>` impact** (`f.caf`); the recommendation block; ONE primary action.
- **Everything else is one row** (`_ipRowHTML`): label · count · chevron · hover · `aria-expanded`, expanding in place, keyboard-operable. A CONTRACT goes on an ⓘ, never resident (D162a).
- **Lifecycle chip (D192b):** `Open ⇄ Addressed ⇄ Resolved`, arrows are `⇄`, **no trailing fill** — only the current state is lit. An ⓘ: "These states move both ways. An analysis update moves an issue forward; withdrawing a decision can bring it back. Either way it is the analysis that moves it — never a manual step." → `_assertLifecycleIsNotDrawnAsARatchet`.
- **Recommendation block (D184/D190):** `_primaryRec(id)` is the recommendation the button will apply, **chosen by computed rank** (`_recRankScore`: appliable=0 · moves the limiting dimension=0 · matches the user's selection=0 · is OSLO's own rec=0), never `[0]`. Its **text is resident above** the button (`#ipRecText`); the label is the constant **"Apply this fix"** (`APPLY_LABEL`/`_applyLabel`, one string across panel + chat). **No renderable recommendation ⇒ no button** (D173 applied to actions). Other options (`_otherRecs`) expand in place (`#ipAlts`) — Select (`selectPath`) / Discuss (`askOslo`) / the Selected option tag / **"Write my own fix in `<document>` →"** (the free manual door, `data-voice="user"`). → `_assertApplyAffordanceShowsItsRecommendation` · `_assertRecommendationRankIsComputed` · `_assertOptionsHaveOneHome`.
- **Rows:** Evidence (`f.ev`, cited by document) · Clarification (when `f.clar`; **default minimized** — the textarea appears on demand, D162c) · Reviews (`_reviewsHTML`) · Comments (`_commentsHTML`, Panel Model only, D009).
- **Actions:** ⤴ Share for review (never disabled, never metered — CR-2, obeyed not narrated) · ✦ Discuss with OSLO.
- **Addressed/Resolved banners** carry the withdraw affordance; **History pointer** into the Slice-7 timeline.
- **Recommendations exist ONLY inside the issue** (D009).

## Behaviour: Lifecycle Open → Addressed → Resolved (D088/D094)

- `_LIFE = ['open','addressed','resolved']`; `_lifeword`; `_active(id)` = not resolved. Per-issue status is mutable `_istatus`, kept separate from the model object.
- **No Acknowledge** (D094). **No manual Resolve.** `_active` is open OR addressed-awaiting-reanalysis; **resolution only ever comes from reanalysis** (D088).
- **Every transition into `addressed`/`attested` is enumerated with its inverse** (`_ISSUE_TRANSITIONS`): `selectPath`→`clearSelection`; `applyFix`→`withdrawDecision`; `_submitClarification`→`withdrawDecision`. A one-way transition without a declared inverse **fails the build** (`_assertEveryDecisionTransitionHasAnInverse`).

## Behaviour: Resolution paths & apply (D089/D184)

- **`selectPath(id, ix)`** — Open → Addressed. A *selection is an intention, not an act*: nothing attested, freely cleared back to no selection (`clearSelection` → back to Open; append-only history event).
- **`applyFix(id)`** — the assisted apply. Captures the pre-fix record first (`_decision[id]` — version, body, basis, Reliability; **never a band/CAF width/confidence**, by construction). Sets `_selpath='rec'`, `_istatus='addressed'`, `_attestWith` the document, marks the tied `PLAN_SECTIONS` **attested** and bumps Reliability (Low→Moderate→High), bumps the artifact version, pushes history. Then after ~1.9s the **analysis update** sets `_istatus='resolved'`, firms Feasibility when a critical Resources gap clears (`_firmFeasibility`), pushes a direction-only trend, and renders the payoff. The assisted-apply **cap** (`_capHit('fixes')`, DL-103 §7d) is **UNSET in normal operation** — no cap fires; the recommendation is never hidden (`_assertRecommendationNeverHidden`), and the free manual door is always open.
- **Withdraw (D191/D192a/D193):** `withdrawDecision` raises a consent line with the subject on screen, then `_withdrawUnit` drops the attestation and — **only if the document is untouched** (`_docTouchedSince`) — restores the pre-fix version; a touched document is **never** restored (D193a — OSLO never deletes the user's writing). The attestation is **refcounted by decision** (`_attestBy`/`_ATTEST_BASE`): it stands while any decision attests the document, drops only when the last is withdrawn, and Reliability restores to its pre-first-attestation value (`_assertAttestationIsRefcountedByDecision`). Withdraw survives a resolved status; the **analysis** re-opens the issue (`_assertWithdrawSurvivesResolution`). **No hand-path moves the read** (`_assertNoHandPathMovesTheRead`).

## Behaviour: Clarification requests (D090/D108) · `_submitClarification`

- One door for panel and chat (`answerClarification` → `_submitClarification(id, val, src)`): updates project info, marks the tied document **Confirmed by you** + raises Reliability (the same two lines `applyFix` runs — an un-withdrawable answer is the same truth defect as an un-withdrawable fix, so it gets the same inverse), moves the issue Open → Addressed, records the answer (`_clarAnswered`), then the analysis update resolves it (D088). History is byte-identical whichever surface answered (D096). The chat reports back but never claims to have closed the issue.

## Component: CAF dimension drill-down (Option C · DL-116/DL-123/124) · `toggleCafDrill`

- Each CAF row shows a mini ramp + level word + a **per-dimension evidence cue** (`_evWord`, provenance separate from the level — level ≠ trust). Clicking toggles a drill-down (`_cafDrillHTML` via `_ciDimDrivers`): **Rests on** (grounded/inferred + evidence word) · **Held back by** (open issues by severity, only "critical" tinted) · the most-severe open issue as a card (`openIssue`) · **To lift it** (the top issue's own `rec`) · a Level-2 **finding-type cut** (`_cafDrillL2HTML`, `_FTYPE_ORDER`) routing each issue to `openIssue`. **The band stays a band — only the drivers are quantified** (DL-116). State lives on container classes (survives refresh).
- **D133 — Alignment is live.** `_reviewAnalysisRun`: an attested reviewer response is evidence about a CAF dimension; **Approve and Reject are both Alignment evidence** and move it **symmetrically** by the same `ALIGN_STEP` (±8, `ALIGN_MIN/ALIGN_MAX` clamped) — pushed to `ALIGN_EVIDENCE`. A stakeholder disagreeing lowers Alignment (the read can **fall**, rendered exactly like a rise, D173c); it is information about alignment, not a verdict that the plan is wrong. The response is recorded as **Attested by `<name>`** and **the issue does not move** — a review "NEVER resolves, re-opens or invalidates the issue." Evidence is **never gated on any tier** (`_assertEvidenceNeverGated`, D126: meter who gets a seat, never who gets an answer).
- **"Awaiting review" chip** (`_awaitChip`) on the list card and the panel: "Understanding on this issue is waiting on someone else. It is not a severity, and it does not change the issue's status."

## Behaviour: Task-altitude findings via the deeper read (ISS-10/11 · Slice 11 analysis)

- `_deepPassSurfaceFindings()` is the **one door** — idempotent, returns the ids it surfaced, so every downstream count is computed (D173). ISS-10/11 are **not** in `ISSUES`/`_istatus` at boot; once surfaced they behave exactly like ISS-01…06.
- **ISS-10** `{ftype:'Coverage Gap', sev:'moderate', dim:'Feasibility', sec:'WBS'}` — the Sep 1 freeze rests on undated upstream tasks; `rec` + two `paths` (no `clar`) → resolves via Apply this fix / Select an option / Write your own fix.
- **ISS-11** `{ftype:'Assumption', sev:'moderate', dim:'Clarity', sec:'WBS'}` — OSLO's honest read on its **own** low-confidence decomposition (three tasks flagged low-confidence); `rec` "Confirm or correct the low-confidence tasks OSLO added". Framed as **evidence honesty, never a warning** (DL-109).
- Both raise **WBS open count 1 → 3** (ISS-05 was the only prior WBS issue). The **task-altitude analysis that produces them is Slice 11's** (`slice-11-execution-ready-planning-export`); this engine only carries them.

## Non-goals / seams (do not build here)

The **task model / critical path / low-confidence decomposition** that produces ISS-10/11 is Slice 11. The **full History timeline** is Slice 7 (this panel only points into it). Execution monitoring is a future phase. The Inference map (where OSLO is guessing) is a peer surface, not this engine.
