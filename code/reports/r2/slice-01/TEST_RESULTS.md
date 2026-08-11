# R2 Slice 01 test results

**Run:** 2026-08-11 23:30 PKT
**Branch:** `codex/release-2-build`
**Status:** functional gates pass; end-to-end visual-evidence gate remains blocked.

## Passing commands

- `pnpm test:api` — **294 passed**, 3 dependency deprecation warnings.
- `pnpm test:web -- --run --reporter=dot` — **23 files / 124 tests passed**.
- `pnpm test:r2-guardrails` — infrastructure **4 passed**; active selectors **9 passed**; registry **60 registered / 6 active / 54 pending / 58 mapped surfaces / 6 of 6 prototype corrections**.
- `pnpm lint:api` — Ruff passed.
- `pnpm lint:web` — ESLint passed.
- `pnpm build:web` — Next.js production build passed; 17 static/dynamic route entries collected successfully.
- `pnpm supabase migration up --local` and `pnpm supabase migration list --local` — migration `20260811221000` is present in both local and applied histories.

## Active Slice 1 guards

- `GT-07` — three normalized pillars compose through the weakest gate.
- `GT-10` — overview resolution overlay and failed governed-node last-good preservation.
- `GT-11` — flagging grounds the item without firming Viability.
- `GT-13` — proportional plan scaling leaves bands unchanged.
- `GT-19` — weakest-gate decomposition and foundation-first tie-breaking.
- `GT-20` — rendered integrity surfaces use maturity words without a numeric forecast.

## TDD defects caught in the real app

1. Evidence-grounded snapshots without explicit assumption rows rendered `Grounding Fragile · 0 of 0`. A failing public-projection test was added; Grounding now consumes the canonical provenance counts. The focused test and full API suite pass.
2. Closing the Integrity breakdown with Escape dropped focus to `body`. A failing component test was added; Escape now closes the dialog and restores focus to the toolbar trigger. The focused test and full web suite pass.

## End-to-end evidence status

The repository-wide Playwright command was not run because it includes owner-blocked Slice 4–10 suites. A Slice-1-only capture harness produced implementation and prototype images for desktop, tablet, and mobile, but it placed the prototype on its pre-confirmation state and the implementation on its post-analysis Overview state. Those files are retained as rejected evidence under `screenshots/`; no Playwright count or parity pass is claimed.

The required in-app-browser happy-path and responsive checks ran successfully before its screenshot channel became unavailable. Fresh retry tabs later failed to attach, so no accepted same-state end-to-end screenshot run exists.
