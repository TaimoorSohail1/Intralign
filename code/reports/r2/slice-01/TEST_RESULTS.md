# R2 Slice 01 test results

**Run:** 2026-08-12 00:17 PKT

**Branch:** `codex/release-2-build`

**Status:** automated functional, build, and same-state viewport gates pass; mandatory manual failure/retry verification remains open.

## Passing commands

- `pnpm test:api` — **294 passed**, 3 dependency deprecation warnings.
- `pnpm test:web` — **23 files / 124 tests passed**.
- `pnpm test:r2-guardrails` — infrastructure **4 passed**; active selectors **9 passed**; registry **60 registered / 6 active / 54 pending / 58 mapped surfaces / 6 of 6 prototype corrections**.
- `$env:PLAYWRIGHT_BASE_URL='http://127.0.0.1:3002'; pnpm test:e2e -- specs/r2-slice-one-integrity.spec.ts` — **6 passed** across desktop, tablet, and mobile.
- `pnpm lint:api` — Ruff passed.
- `pnpm lint:web` — ESLint passed.
- `pnpm build:web` — Next.js production build and TypeScript passed; 17 pages generated/collected.
- `git diff --check` — passed.
- `pnpm supabase migration up --local` and `pnpm supabase migration list --local` — migration `20260811221000` is present in local and applied histories.

## Active Slice 1 guards

- `GT-07` — three normalized pillars compose through the weakest gate.
- `GT-10` — overview resolution overlay and failed governed-node last-good preservation.
- `GT-11` — flagging grounds the item without firming Viability.
- `GT-13` — proportional plan scaling leaves bands unchanged.
- `GT-19` — weakest-gate decomposition and foundation-first tie-breaking.
- `GT-20` — rendered integrity surfaces use maturity words without a numeric forecast.

## TDD defects caught

1. Evidence-grounded snapshots without explicit assumption rows rendered `Grounding Fragile · 0 of 0`. A failing public-projection test was added; Grounding now consumes the canonical provenance counts.
2. Closing the Integrity breakdown with Escape dropped focus to `body`. A failing component test was added; Escape now restores focus to the toolbar trigger.
3. The executable compact masthead omitted the prototype's three-pillar integrity shape. A failing component assertion was added; the masthead now exposes Viability, Grounding, and Adaptability with their bands and mini range bars at the applicable desktop width.

## End-to-end evidence

The Slice-1-only Playwright specification exercises only authorized Slice 1 behavior. It signs in as the seeded owner, opens a real analyzed project, verifies the five bands, three pillars, pending/live copy, absence of a numeric score, responsive overflow, breakdown dialog focus, and Escape restoration. It also advances the prototype to a matching read: Fragile, limited by Adaptability, with Viability and Grounding Sound, then saves source and combined comparisons for all three viewports.

The repository-wide Playwright command was intentionally not run because it includes owner-blocked Slice 4–10 suites. Automated evidence does not replace the still-open manual forced timeout/retry/last-good check.

## Rerun notes

- No automated suite was rerun during the 2026-08-12 05:03-05:10 PKT resumption because no product code changed and the mandatory manual gate failed before a browser page existed. The passing results above remain the latest implementation evidence; they are not used to claim manual completion.

- The first scoped E2E attempt recorded 3 implementation failures and 3 prototype passes because the local Next.js process had exited before navigation (`ERR_CONNECTION_REFUSED`). After restarting that same local process, the identical command passed 6/6.
- A first production-build attempt compiled successfully but exhausted Node memory while TypeScript ran concurrently with the full API, web, guardrail, and lint suites. The build was rerun alone and passed completely; no product defect was implicated.
