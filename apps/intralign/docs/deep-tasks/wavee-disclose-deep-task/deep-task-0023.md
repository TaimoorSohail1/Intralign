# DTM-0023 — Issue Cards (Issues + severity/confidence; link to source Findings)

**Status:** In progress — DTM-0022 approved (`1e0d139`) · **Module:** DTM-0023 · **Phase:** VI
(Wave E) · **Contract:** **IC-WE-DISCLOSE** E1 (Issue Cards) · **Depends:** DTM-0018/0019/0020.

## Goal / observable behavior

**Issue Cards** present Issues with their **severity + confidence band**, each linking back to its
**source Finding(s)**. Read-only presentation; epistemic labels on every card.

## Source docs / constraints

- Contract E1 (Issue Cards row). UX: the issue/issue-card spec under `10_product/experience/`
  (read `UI_SCREEN_INVENTORY.md` for the screen that hosts issues — likely the workspace or a
  dedicated issues view). `code/CONTEXT.md` (Issue is an Evaluate output; severity + confidence
  band; Derived). Decisions #3, #5.
- Consume the DTM-0018 issues read (inspect the generated client; if issues ride within the
  findings/confidence DTOs rather than a dedicated endpoint, render from what exists and flag any
  gap — do NOT invent an endpoint). Reuse `EpistemicLabel`; link to the Finding Panel route.

## Locked decisions (do not re-derive)

- **Presents, never generates.** No edit/score/accept control. Severity + confidence are shown as
  governed values via `EpistemicLabel` (Derived + band); confidence is trust-in-understanding,
  never project health/probability.
- **Link to source Findings** (route to the Finding Panel). No new dependency.

## Owned files / boundaries

- **OWN:** `code/frontend/src/surfaces/IssueCards/**` (+ tests) and wiring the relevant route/
  placeholder in `router.tsx` (or mounting within the workspace if that's where the screen lives —
  the one swap). Vitest + Playwright.
- **READ-ONLY:** backend, generated client, theme/EpistemicLabel, other surfaces.

## Packages / refactors — none new.

## Implementation instructions (TDD)

1. Red (Vitest): each Issue renders as a card with severity + confidence (Derived label) + a link
   to its source Finding(s). **Negatives:** no edit/score/accept/generate control; Derived-as-settled
   impossible; confidence never reads health/probability; severity shown as a governed qualifier,
   not invented.
2. Build the cards from the DTM-0018 issue data; mount; clean loading/empty states.

## API / data / schema contracts

- Consumes the DTM-0018 issue data (+ `DerivedEnvelope`). No backend change. If no dedicated issues
  endpoint exists, render from the available DTO and FLAG the gap (do not invent).

## Test plan

- **Positive:** issue cards with severity + confidence label + source-finding link; empty/loading
  clean.
- **Negative:** no edit/score/accept control; Derived-as-settled impossible; confidence not health/
  probability.
- `npm run build` + `vitest run` + Playwright + drift + `npm audit --omit=dev`.

## Manual checks (EM)

- `npm run dev` → issues render as cards with severity + confidence + a link to the source finding;
  no edit/accept control.

## Done criteria

- Issue Cards present issues with severity + confidence labels + source-finding links, read-only,
  no new dep, tests green. PR cites IC-WE-DISCLOSE. Ready for DTM-0024.

## Worker report

**Status: Ready for review.** TDD (red → green); IC-WE-DISCLOSE E1.

### The issues-data finding (the important one — endpoint or not)

**There is NO dedicated Issue endpoint or Issue DTO in the DTM-0018 REST surface.**
The internal cognition `Issue` (`code/shared/epistemic.py:659`) — Evaluate's *prioritized
Finding* (a Finding + an assigned `severity`, carrying the source-Finding lineage:
`finding_id` / `finding_type` / `evidence_anchors`, Derived) — is **not exposed verbatim
over REST**: there is no `Issue` class in `code/shared/entities.py`, and nothing matching
`issue` in the generated client (`grep -rin issue src/api/generated/` → 0 hits). DTM-0018
exposed Finding / Confidence / Recommendation / CAF / Notification / Acceptance only.
`UI_SCREEN_INVENTORY.md` has **no dedicated "Issues" screen** either — issues are presented
in the project's findings context (`GET /projects/{pid}/findings`).

**What I rendered from (no endpoint invented):** the **Finding DTO** is the governed carrier
of exactly the data an Issue Card needs — it already carries `severity` (the very attribute
Evaluate assigns to FORM an Issue, per the `Issue` class docstring), the Derived confidence
`label` (`DerivedEnvelope` + band + conflict), and the source-finding identity
(`finding_id`/`finding_type`). So the cards render from the existing
`useListFindingsV1ProjectsProjectIdFindingsGet` read (`GET /projects/{pid}/findings`),
treating a Finding-with-`severity` as the prioritized Issue and linking each card back to its
source Finding (the Finding Panel route). **A Finding with no `severity` is not yet an Issue
and is filtered out — nothing is invented.**

**FLAGGED GAP (for the EM / DTM-0018 owner):** if Issues are to be a first-class read with
their own identity (`issue_id`) and lineage projected over REST, DTM-0018 needs an `Issue`
DTO in `shared/entities.py` + a `GET …/issues` endpoint (the internal `Issue` cognition
already exists; only the render-mapper + router are missing). I did **not** add a backend
endpoint (out of scope; no backend edits).

### Files

- **NEW** `src/surfaces/IssueCards/IssueCards.tsx` — the surface (renders Issue cards from the
  Finding read; severity governed qualifier + Derived `EpistemicLabel` + source-finding link;
  clean loading/positive-empty states).
- **NEW** `src/surfaces/IssueCards/IssueCardsRoute.tsx` — thin route adapter (params → props).
- **NEW** `src/surfaces/IssueCards/fixtures.ts` — Finding DTO fixtures (verbatim shape; the
  issues-data finding documented inline).
- **NEW** `src/surfaces/IssueCards/testHarness.tsx` — theme + query + in-memory router (findings
  index + finding-detail target so the source-finding link resolves/navigates).
- **NEW** `src/surfaces/IssueCards/IssueCards.test.tsx` — 13 Vitest (positives + negatives).
- **NEW** `e2e/issue-cards.spec.ts` — 2 Playwright (mounts + the presents-never-generates negative).
- **MODIFIED** `src/app/router.tsx` — the **one** route swap: `projectFindingsRoute` placeholder →
  `IssueCardsRoute` (mounts at `/projects/$projectId/findings`; MRI surface untouched).

### Negatives proven (the Disclose spine)

- **No edit / score / accept / defer / prioritise / generate / govern / recompute control** in the
  DOM (Vitest scans every button/`role=button`/input/textarea/select; Playwright scans every
  interactive role).
- **Derived-as-settled impossible** — every card's confidence is a Derived `EpistemicLabel`
  (`data-standing="derived"`, never `attested`); no "settled"/"resolved" text on the surface.
- **Confidence never reads health / readiness / probability / a bare score** (asserted absent);
  severity reads only as a governed qualifier `critical|moderate|warning` (regex-pinned), never a
  `%` / score.
- **Severity not invented** — only the governed `Severity` enum values render; a Finding without a
  severity is not shown as an Issue.
- **No upgrade of the governed value** — the high-band fixture renders its `confidence_band`
  verbatim.
- **Links to the source Finding** — each card's "View source finding" link points to
  `/projects/$projectId/findings/$findingId` (the Finding Panel route) and navigates there.

### Verify (exact commands + results)

```
cd code/frontend
npm run build         → ✓ tsc -b + vite build (722 modules, built in 1.16s)
npx vitest run        → ✓ 7 files, 83 tests passed (IssueCards: 13 new; all prior pass)
npx playwright test   → ✓ 12 passed (issue-cards: 2 new; finding/rec/mri/shell unchanged)
npm audit --omit=dev --audit-level=high → ✓ found 0 vulnerabilities
```

**No new dependency** (`git diff HEAD -- package.json package-lock.json` → empty). **No
out-of-scope edits** — working tree shows only `src/app/router.tsx` modified + the new
`src/surfaces/IssueCards/**` and `e2e/issue-cards.spec.ts`; backend / generated client / theme /
`EpistemicLabel` / other surfaces untouched. Cited contract: **IC-WE-DISCLOSE** E1 (Issue Cards).
Staged (green); not committed.

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

Status: Approved

Executive summary:
- Issue Cards (`surfaces/IssueCards/**`) at `/projects/$projectId/findings`: present
  Finding-with-severity as the prioritized Issue (matches the `Issue` cognition = prioritized
  Finding), severity as a governed qualifier + Derived confidence via `EpistemicLabel`, each card
  linking to its source Finding. Read-only.

Verification (EM re-ran): `npm run build` built; `npx vitest run` **83 passed** (13 new + 70);
worker playwright 12, audit 0. Scope = IssueCards/** + one route swap; dependency delta **NONE**.

Negatives proven: no edit/score/accept/prioritise/generate/recompute control; Derived-as-settled
impossible; confidence never reads health/readiness/probability/bare-score; severity pinned to the
governed enum (not invented); source-finding link routes to the Finding Panel.

Remaining risks / follow-up: **no first-class Issue REST identity** — Issues are not a dedicated
DTO/endpoint; the surface renders from Finding-with-severity (nothing invented, severity-less
Findings filtered out). If Issues need their own `issue_id`/`GET …/issues`, that's a DTM-0018
follow-up (Issue DTO + render-mapper + router) — folded with the other DTM-0018 read follow-ups.
