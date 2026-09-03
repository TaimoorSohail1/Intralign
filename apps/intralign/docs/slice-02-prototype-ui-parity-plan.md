# Slice 2 golden-prototype UI parity plan

Status: implementation-ready plan
Branch: `feature/slice-2`
Golden source: `oslo-product-grill/vertical-slices/slice-02-intake-fastpass-orientation/prototype.html`
Primary rule: reproduce the prototype's hierarchy, wording, density, states, and interactions. Do not redesign it.

## 1. Target user journey

```text
Intake
  -> Initial Analysis interstitial
  -> Provisional Overview
  -> one-time strategic orientation
  -> usable Overview
  -> Extended Analysis in the background
  -> Current Overview or preserved Last-good Overview
  -> Attention map
  -> Issue clarification
  -> re-analysis and updated read
```

The HTML prototype remains the visual and interaction source of truth. Production APIs,
database records, SSE events, and OpenAI results replace its fixtures and timers.

Prototype-only preview controls are excluded:

- Alpha/GA preview selector
- simulated analysis-failure button
- Restart button
- anonymous GA and save-to-keep messaging

## 2. Audit baseline

The audit used live captures from the golden prototype and the running production app.

| Surface | Current health | Main gap |
|---|---|---|
| Analysis loading | Partial | Current screen exposes a long technical step list instead of the focused four-phase prototype experience |
| Strategic orientation | Partial | Current wording, cards, sizing, and CTA do not match the prototype |
| Overview | Major gap | Current score ring, large issue-card grid, status banner, and seven artifact cards use a different hierarchy |
| Attention map | Missing | The Attention link is an anchor; there is no seven-by-three heatmap |
| Issue detail | Partial | Basic drawer exists, but lacks evidence, lifecycle, clarification answer, re-analysis, and suggested fixes |
| Answer the first | Missing | No tied clarification action and no mutual exclusion between the issue drawer and OSLO advisor |
| OSLO advisor | Partial | Advisor works, but cannot collapse, preserve context, or yield its rail to an issue drawer |
| Project summary | Major gap | Current UI renders seven artifact cards; prototype has one compact accordion |

## 3. Professional visual direction

“Professional and beautiful” means high-fidelity execution of the prototype, not a new
visual concept.

### Layout

- Desktop content width: approximately 820-880px.
- Advisor rail: fixed 330-340px.
- Header: compact 48px product shell.
- Main sections: Confidence, Start here, Progress, More.
- Cards use restrained borders, 10-12px radii, compact spacing, and minimal shadow.
- Issue information uses one-dimensional rows, not oversized dashboard tiles.

### Type and color

- UI font: Inter.
- Technical trace: JetBrains Mono.
- Background: `#111315`.
- Surface: `#1B1F24`.
- Raised surface: `#242A31`.
- Primary text: `#F5F4F0`.
- Muted text: `#B8BDC5`.
- Border: `#343B44`.
- OSLO orange: `#D97A3A`.
- Warning: `#D9A441`.
- Critical: `#C75B5B`.
- Current: `#4D8B6B`.

Severity color is reserved for issues. Confidence is a maturity read, not a health
grade, and should remain mostly neutral.

## 4. Route and state architecture

```text
/intake
/projects/{projectId}/analysis/{runId}
/projects/{projectId}/overview
/projects/{projectId}/attention
```

Overview and Attention share one `ProjectShell`. Both routes must be deep-linkable and
support browser Back/Forward.

### Authoritative UI state

```text
ProjectShellState
  activeView: overview | attention
  advisor: open | closed
  issueDrawer: closed | issueId
  summary: collapsed | expanded
  orientation: hidden | open
  snapshotState: provisional | current | last_good
```

Rules:

- Opening an Issue drawer closes the OSLO advisor rail.
- Closing the Issue drawer restores the advisor to its previous state.
- `Answer the first` opens the first open issue that has a clarification question.
- `Timeline` and the top `Attention` tab navigate to the Attention map.
- UI state must never overwrite the current published server snapshot.

## 5. Component architecture

```text
components/slice-two/
  analysis/
    analysis-interstitial.tsx
    analysis-phase-trace.tsx
  orientation/
    strategic-orientation.tsx
  shell/
    project-shell.tsx
    project-header.tsx
    advisory-footer.tsx
  overview/
    confidence-read.tsx
    dimension-bars.tsx
    start-here.tsx
    progress-read.tsx
    project-summary.tsx
  attention/
    attention-map.tsx
    attention-cell.tsx
    dimensions-view.tsx
  issues/
    issue-drawer.tsx
    clarification-form.tsx
  advisor/
    oslo-advisor.tsx
    advisor-context.tsx
```

`project-overview.tsx` becomes composition rather than one large component.

## 6. Screen contracts

### 6.1 Initial Analysis

Match the prototype:

- full-screen dark canvas
- glowing OSLO scanner
- `ANALYZING…` state pill
- one current human-readable phase title
- one supporting sentence
- four phase dots
- short monospace completion trace
- quiet expected-time label

Map the twelve backend nodes into four stable user phases:

1. Read inputs.
2. Build understanding.
3. Construct seven plan artifacts.
4. Assess clarity, alignment, and feasibility.

The UI is driven by SSE and durable run state. Refresh resumes the current phase.
Reduced-motion mode removes spin/pulse but retains all status text.

### 6.2 Strategic orientation

After the first provisional result, show the exact four-card modal:

1. Understanding — OSLO.
2. Judgement — You.
3. Decision — You.
4. Oversight — You.

CTA: `Get started →`.

Dismissal is persisted server-side. Replay remains available from the account menu.
The dialog traps focus, closes only through the approved action or Escape, and restores
focus correctly.

### 6.3 Overview

Use the prototype order only:

```text
Confidence
Start here
Progress
More
```

#### Confidence

- Large score with `/100`.
- `Ask OSLO why`.
- Provisional/Current/Last-good chip.
- Plain-language maturity and reliability statement.
- Trend from provisional to current when available.
- Horizontal Clarity, Alignment, and Feasibility bars.
- Limiting dimension uses orange.
- Open/resolved counts.
- `Why` disclosure.
- `Timeline →` navigates to Attention.

#### Start here

- Compact vertical list of the most consequential issues.
- The first critical issue receives the primary Review action.
- Remaining rows show severity, title, artifact, and chevron.
- `See all {n} open issues in the Attention map →`.
- Clarification strip appears only when a tied open question exists.
- `Answer the first →` opens that Issue drawer and closes the advisor.

#### Progress

Show audited facts only:

- issues resolved/open
- critical issues open
- dependencies confirmed
- plan artifacts read

Extended-analysis notices belong in the OSLO advisor rail, not in Progress.

#### More

One `Project summary` accordion:

- collapsed by default
- short one-line descriptor when collapsed
- narrative summary when expanded
- no seven-artifact card grid on Overview

Structured artifacts remain available to Attention and the Project view.

### 6.4 Attention map

`Timeline` and `Attention` open a dedicated project view.

The heatmap contains:

- rows: Intent, Context, Scope, Requirements, Work breakdown, Schedule, Resources
- columns: Clarity, Alignment, Feasibility
- Calm, Warning, Moderate, and Critical visual intensity
- count per populated cell
- Heatmap/Dimensions view switch

Cell counts are derived from the same published snapshot as Overview. Selecting a
populated cell opens the highest-severity Issue in that cell and allows navigation
through additional Issues.

Keyboard behavior:

- arrow keys move between cells
- Enter/Space opens a populated cell
- empty cells remain readable but do not open a drawer
- focus returns to the selected cell when the drawer closes

### 6.5 Issue and clarification drawer

The drawer replaces the advisor rail on desktop and becomes full-screen on mobile.

It contains:

- severity, title, CAF dimension, artifact, and finding type
- Open → Addressed → Resolved lifecycle
- `Ask OSLO about this issue`
- Why this matters
- evidence snippets and source labels
- clarification request
- answer textarea
- `Submit & re-analyze`
- suggested fixes

Submission rules:

- Empty answers are disabled.
- One idempotent command stores the user's answer as new evidence.
- The tied Issue becomes Addressed, never manually Resolved.
- A new analysis run starts and progress is announced.
- Only a successfully published result may resolve or change the Issue.
- Failure preserves the last-good Overview and the submitted answer.

### 6.6 OSLO advisor

- Persistent desktop rail, collapsible by the user.
- Full-height overlay on mobile.
- Mutually exclusive with the Issue drawer.
- Preserves the conversation when hidden.
- Shows initial and extended completion notices.
- Supports typed context: confidence, issue, or attention cell.
- Context can be cleared.
- Advisor explains and recommends; it does not mutate project truth.

### 6.7 Project summary

The bottom summary mirrors the prototype:

- compact label row
- chevron and `aria-expanded`
- smooth but restrained disclosure
- complete narrative only when expanded
- no page navigation

## 7. API and data work

### Existing data to reuse

The current Overview contract already exposes:

- confidence and CAF dimensions
- seven artifacts
- issues with artifact, dimension, severity, why, recommendation
- issue evidence references
- optional clarification
- provisional/current state
- extended-analysis status

### Required additions

#### Attention projection

Prefer a deterministic server projection:

```text
AttentionMapView
  snapshot_id
  rows[7]
  dimensions[3]
  cells:
    issue_count
    highest_severity
    issue_ids[]
```

#### Issue detail

Resolve evidence references to safe display snippets:

```text
IssueDetailView
  issue
  evidence[]
  clarification
  suggested_fixes[]
  lifecycle
```

#### Clarification command

```http
POST /v1/projects/{projectId}/issues/{issueId}/answers
Idempotency-Key: {uuid}

{
  "answer": "..."
}
```

Response:

```json
{
  "issue_status": "addressed",
  "analysis_run_id": "...",
  "accepted": true
}
```

The command must validate tenancy, membership, issue ownership, current snapshot, and
maximum answer length before writing.

## 8. Implementation work packages

### WP0 — lock the parity baseline

- Preserve the accepted prototype captures.
- Capture the current implementation at the same desktop viewport.
- Create deterministic API fixtures for provisional, current, last-good, no-issue,
  and clarification states.
- Add a visual-difference checklist.

Exit: every implementation state has an approved reference and stable fixture.

### WP1 — shared shell and tokens

- Extract OSLO design tokens.
- Build `ProjectShell`, top navigation, advisor slot, drawer slot, and footer.
- Add Overview and Attention routes.
- Add advisor collapse/restore behavior.

Exit: shell dimensions and navigation match the prototype.

### WP2 — Analysis and orientation

- Replace the technical ten-step display with the four-phase prototype treatment.
- Keep real SSE, retry, refresh recovery, and failure safety.
- Rebuild orientation wording, cards, spacing, and CTA to match.

Exit: Intake-to-Overview transition is visually and behaviorally faithful.

### WP3 — Overview parity

- Replace score ring with prototype confidence read.
- Add trend and dimension bars.
- Replace issue grid with compact Start-here list.
- Build clarification strip.
- Replace analysis-status banner with audited Progress.
- Replace artifact grid with Project summary accordion.

Exit: desktop Overview matches the golden hierarchy and content density.

### WP4 — Attention map

- Add deterministic 7×3 projection.
- Implement Heatmap and Dimensions views.
- Wire Timeline and Attention navigation.
- Add cell keyboard behavior and deep links.

Exit: counts reconcile with Overview and every populated cell opens the correct Issue.

### WP5 — Issue clarification workflow

- Expand Issue detail contract.
- Build prototype-matching drawer.
- Implement Answer-the-first selection.
- Add idempotent answer submission.
- Trigger and monitor re-analysis.
- Preserve answer and last-good snapshot on failure.

Exit: clarification → re-analysis → updated Issue is durable and testable.

### WP6 — Advisor integration

- Add collapse/reopen control.
- Make advisor and Issue drawer mutually exclusive.
- Preserve messages while hidden.
- Add typed context handoff and analysis notices.

Exit: advisor behavior matches the prototype without changing project truth.

### WP7 — responsive and accessibility hardening

- Tablet rail collapse.
- Mobile full-screen advisor and Issue drawer.
- Focus traps, focus restoration, Escape behavior, tabs, disclosures, and live regions.
- Reduced-motion loading.
- 320px minimum-width verification.

Exit: keyboard, screen-reader, mobile, tablet, and reduced-motion checks pass.

### WP8 — visual and release QA

- Playwright visual comparisons at 1440×900, 1024×768, and 390×844.
- Cross-browser checks.
- API integration tests.
- Failure/reconnect/retry tests.
- Manual prototype side-by-side review.

Exit: no unexplained visual deviation and all interaction acceptance tests pass.

## 9. TDD and verification matrix

### Component tests

- phase-to-copy mapping
- provisional/current/last-good labels
- limiting dimension and trend
- issue ordering and clarification selection
- Attention aggregation
- advisor/drawer mutual exclusion
- summary disclosure
- focus restoration

### API tests

- tenant isolation
- stale snapshot rejection
- idempotent clarification submission
- duplicate-click protection
- answer persistence before job enqueue
- enqueue failure recovery
- only completed analysis changes Issue state
- last-good preservation

### End-to-end tests

1. Upload → SSE loading → provisional Overview.
2. First project shows orientation once.
3. `Get started` reveals Overview.
4. Extended Analysis updates Provisional to Current.
5. `Timeline` opens Attention.
6. Attention cell opens the tied Issue.
7. `Answer the first` closes advisor and opens the clarification drawer.
8. Submit answer starts re-analysis and survives refresh.
9. Successful re-analysis updates the Issue and confidence read.
10. Failed re-analysis preserves the last-good read and offers Retry.
11. Project summary expands and collapses.
12. Advisor collapses, reopens, and preserves conversation.

### Visual release gates

- Reference and implementation screenshots use the same state and viewport.
- Playwright screenshot tolerance is intentionally low.
- Copy, component order, widths, spacing, borders, and type scale are asserted.
- Any deliberate deviation requires a written reason and approval.

## 10. Definition of done

- The Overview is immediately recognizable as the golden prototype.
- Loading uses live backend progress without exposing internal implementation noise.
- Orientation matches the prototype and appears once.
- Timeline opens the real Attention map.
- The map always contains seven artifact rows and three CAF columns.
- `Answer the first` opens the tied Issue and closes the advisor.
- The drawer includes evidence, clarification, re-analysis, lifecycle, and fixes.
- Project summary is the only Overview disclosure under More.
- Overview, Attention, Issue, and advisor counts cannot disagree.
- Refresh, reconnect, retry, and Extended failure preserve durable state.
- Desktop, tablet, mobile, keyboard, and reduced-motion behavior pass.
- All automated tests and visual baselines pass before merge.

## 11. Recommended implementation order

```text
WP0 baseline
  -> WP1 shell
  -> WP2 loading/orientation
  -> WP3 Overview
  -> WP4 Attention
  -> WP5 Issue clarification
  -> WP6 advisor
  -> WP7 responsive/accessibility
  -> WP8 release QA
```

This order delivers visible prototype parity early while the clarification write path
and re-analysis workflow are added safely behind it.
