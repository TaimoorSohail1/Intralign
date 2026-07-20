# Slice 6 — Issues & Recommendations (Panel Model) · Frontend / UI

Single openable HTML; dark default + light override on the same tokens (D015); WCAG 2.1 AA (focus-visible rings, keyboard operability, reduced-motion). No framework; plain JS + CSS variables. Colour discipline: **severity red/amber/green appears only on issues** (heat cells + issue badges); the read/CAF/lifecycle stay neutral (D003).

> Regenerated to the frozen build (md5 `a327d702`). Issues + Attention are **one destination with a Map ⇄ List toggle** (DL-136); the standalone "Attention map" nav row is retired. The lifecycle chip is drawn as `⇄` with no trailing fill (D192b); the recommendation is **resident above its Apply button** (D184). No "Acknowledge" control exists.

## Destination layout — Map ⇄ List (DL-136)

Two peer panes switched by `showView`, each fronted by the same toggle:
- `#pane-attention` — the **Map** (heatmap). `.iaview-toggle` [Map on · List → `showView('issues')`].
- `#pane-issues` — the **List**. `.iaview-toggle` [Map → `showView('attention')` · List on].

Both toggles are `role="tablist"` with `aria-selected`. The single `#sbIssues` sidebar item is active for both views (`_syncNav`). Crumb `#tbCrumb` reads "Issues · Map" / "Issues · List" (`_viewLabel`).

## Map view — `#pane-attention`

| Element | Selector / class | Notes |
|---|---|---|
| View toggle | `.iaview-toggle` (`.iav`) | Map (on) / List; `▦` / `☰` glyphs |
| Heading | `.mri-head h1` "Where your plan needs attention" + `.mri-sub` | Documents × Clarity · Alignment · Feasibility |
| Legend / lead | `.mri-bar .lead` (`.brighter`) | "Brighter = more attention — not a health score" + ⓘ (D060) |
| Heatmap | `#heatGrid` (`renderHeat()`) | rows = documents · cols = C·A·F; l0–l3 severity ramp only (D003) |
| All-clear | `#heatClear` (`.heat-clear`) | shown when nothing is open; "all-clear on **attention** — not a guarantee of success" (D061) |
| Legend key | `#heatLegend` | Calm → Needs attention; "Rows = documents · columns = C·A·F" |

## List view — `#pane-issues` (D086)

| Element | Selector / id | Notes |
|---|---|---|
| View toggle | `.iaview-toggle` | Map / List (on) |
| Heading + count | `.iss-head h1` "Issues" + `#iss-count` | live count ("N open" / "(filtered)") |
| Sub | `#iss-sub` | "What needs your attention" |
| Group tabs | `.grp-tabs` (`#grpDim` / `#grpSev` / `#grpArt`) | By dimension (default) · By severity · By document; `role="tab"`, `setGroup` |
| Filters | `.iss-filters` (`#if-art` / `#if-dim` / `#if-sev` / `#if-status`) | Document (`renderArtFilters`, live counts) · Dimension · Severity · Status (Open/Resolved/All); `setFilt` / `clearFilt` |
| Triage | `.triage` (`.tg.crit/.mod/.warn`) | shown under By severity — Critical · Moderate · Warning counts |
| Group heading | `.iss-group` / `.iss-gh` | "`<label>` · N" |
| Issue card | `.icard` (`_issueCard`) | `.isevbar` severity + `.ic-t` title + `.ic-m` [`.ic-sev` · `.ic-loc` document·dimension · `.ic-life` status · clarification flag · await chip]; opens `openIssue` |
| Hidden count | `.iss-hidden` | "N hidden by filters · clear" |
| Scoped-from-map header | `.iss-hidden` (cell scope) | "Scoped from the Attention map · `<doc>` × `<dim>` · Ask OSLO about this cell →" |
| Empty states | `.iss-empty` (`.good`/`.wait`/`.err`) | four honest states (`_issEmpty`, D091) |

## Issue panel — `#issuepanel` (over `#issueScrim`) · `openIssue` (D087/D162)

| Element | Selector / class | Notes |
|---|---|---|
| Header | `.ip-top` (`.ip-sev` · `.ip-title` · `.ip-x`) | severity + title + close (Esc closes) |
| Meta | `.ip-meta` | Dimension · Artifact (link → `openIssueArtifact`) · Issue id |
| Lifecycle | `.ip-life` (`.st`, `.a` = `⇄`) + `.info` | `Open ⇄ Addressed ⇄ Resolved`; **no trailing fill**, only current lit; ⓘ "these states move both ways… never a manual step" (D192b) |
| Await chip | `.crr-chip.await` (`_awaitChip`) | "◷ Awaiting review · `<who>`" — not a severity, doesn't change status |
| Why | `.ip-h` "Why this matters" + `.ip-p` | the plain-language read (`f.why`) |
| Impact | `.ip-weak` (`.wk-dim`) | "`<dimension>` impact" (`f.caf`) |
| Recommendation | `.ip-primary.ip-rec` (`#ipRecBlock`) | `.rtag` "◆ OSLO recommends" + `#ipRecText` (resident) |
| Apply | `#ipApplyBtn` (`.btn-primary`) | label constant **"Apply this fix"** (`APPLY_LABEL`); `applyFix`; **no rec ⇒ no button** (D184) |
| Discuss / Other options | `.btn-ghost` · `#ipOtherBtn` (`aria-controls="ipAlts"`) | Discuss → `askOslo`; Other options (N) → `ipToggleAlts` |
| Alternatives | `.ip-alts` (`#ipAlts`) | options in place: `.ip-path` (Select `selectPath` / `.ip-discuss` / `.selmark`), `.ip-selpath` Selected option, `.ip-ownfix` "✎ Write my own fix in `<document>` →" (`data-voice="user"`) |
| Answer (clar) | `.ip-primary button` "Answer" | when `f.clar` and no appliable rec; opens the clar row (`ipOpenRow`) |
| Rows | `.ip-rows` (`_ipRowHTML`) | Evidence (`.ip-ev`) · Clarification (`.ip-clar`, textarea `#clarInput`, "Answer in chat →", Submit) · Reviews (`_reviewsHTML`) · Comments (`_commentsHTML`) — each `.ip-row` w/ `.ip-rowh` button + `.chev` + `aria-expanded` |
| Actions | `.ip-acts` | ⤴ Share for review (`openCrr`, never disabled/metered — CR-2) + ✦ Discuss with OSLO |
| Addressed / Resolved | `.ip-addressed` / `.ip-resolved` | "Addressed · updating…" / "✓ Resolved by the analysis update" + withdraw affordance |
| History pointer | `.ip-hist` | "Detected in your last analysis… Open full timeline →" (`openHistorySeam`, Slice 7) |

**Guards on the panel:** `_assertLifecycleIsNotDrawnAsARatchet` · `_assertApplyAffordanceShowsItsRecommendation` · `_assertRecommendationRankIsComputed` · `_assertRecommendationNeverHidden` · `_assertOptionsHaveOneHome`.

## Withdraw affordance — `_ipWithdrawHTML` (D191/D184)

Named for what it does (`_wdLabel` — "Withdraw this fix" / "Withdraw this answer" / "Clear selection"); raises a consent line (`_wdConsentLine`) with the subject on screen **before** it acts (`_wdConfirm`). One home per panel — never repeated. A touched document is never restored, and the line says so honestly (D193a).

## CAF drill-down — the Overview CAF rows (Option C · DL-116/DL-123/124)

| Element | Selector / id | Notes |
|---|---|---|
| CAF row | `#cg-clar` / `#cg-align` / `#cg-feas` (`.cafrow`) | caret + name + `.ramp.mini` + `.cafband` level + `.caf-ev` evidence cue + `.cafdbtn` Details ▾; `toggleCafDrill` |
| Drill host | `#cg-*-drill` (`.cafdrill`) | `.open` / `.l2open` on container (survives refresh) |
| Level 1 | `.cd-line` (Rests on · Held back by · To lift it) + `.cd-issue` | `_cafDrillHTML`; grounded `.pgx-sw.att` / inferred `.pgx-sw.inf` (neutral tokens); only "critical" tinted (`.cd-crit`) |
| Level 2 | `.cd-l2` (`.cd-ftype` / `.cd-item`) | finding-type cut → `openIssue`; `toggleCafL2` |

**Level ≠ trust:** the `.caf-ev` cue is provenance, never folded into `.cafband`. The band stays a band; only drivers are quantified. Alignment is live (D133 — `_alignWhy`, `_reviewAnalysisRun`).

## Color discipline (D003)

Heat cells and issue severity badges use the red/amber/green **severity** ramp. The lifecycle chip, CAF bands, the drill, the recommendation block, grounding swatches, and the await chip are **neutral** (weight/shape, never hue). No percentage fill, no health bar. Severity is the only place colour carries meaning.

## Accessibility

- Toggles / group tabs / filters: `role="tab"`/`"tablist"`, `aria-selected`, keyboard operable.
- Issue cards, CAF rows, drill items, path options, withdraw: `role="button"`, `tabindex="0"`, Enter/Space handlers.
- Panel rows: `<button>` `.ip-rowh` with `aria-expanded`; Esc closes the panel; the scrim stacks above lower overlays (`#issueScrim`).
- Focus-visible rings + reduced-motion inherited (no analysis animation under reduced-motion); colour is never the sole signal.

## App shell (inherited)

Persistent left sidebar (Overview · **Issues** [Map+List] · History · Inference map · Reports · Documents subgroups · Full plan), top bar, command palette (⌘/Ctrl+K — carries an "Issues — Map" entry), chat rail. The Issues item routes to the last-seen view; nav chrome and badges stay neutral.
