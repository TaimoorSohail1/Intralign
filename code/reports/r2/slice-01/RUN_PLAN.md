# R2 Slice 01 run plan

## Resumption plan - 2026-08-12 07:04 PKT

1. Restore the seeded Supabase, FastAPI, and Next.js stack and reconnect the required Codex in-app browser.
2. Complete the timeout to stale/last-good to retry journey plus keyboard, announcement/focus, reduced-motion, 200% zoom, permissions, adjacent-regression, and responsive checks if a page attaches.
3. Save and inspect current-run desktop, tablet, and mobile screenshots before accepting UI/UX or prototype-parity evidence.
4. Rerun automated gates and Code Review only after a successful manual gate or any product-code change.
5. Keep Slice 1 `IN PROGRESS` unless every open gate passes; do not acquire Slice 3 or touch Slices 4-10.

**Result:** Supabase Auth, PostgreSQL, FastAPI, and Next.js were reachable. The idempotent seed refresh stalled on the Docker control channel, but the existing seeded platform stayed healthy. The in-app browser timed out before attaching both the initial and supported-recovery fresh pages; controlled and user-visible tab lists stayed empty and visibility stayed false. No manual interaction, screenshot, product change, automated rerun, or completion claim was accepted. Slice 1 remains `IN PROGRESS`.

**Acquired:** 2026-08-11
**Starting branch / commit:** `codex/release-2-build` / `b649b25`
**Contract:** `release-2/slices/01-integrity-engine.md` AC-1…AC-10 and GT-07, GT-10, GT-11, GT-13, GT-19, GT-20.

1. Trace the inherited CAF, grounding, issue, read-projection, API, and overview UI seams; reuse only behavior that passes the R2 contract.
2. Deliver one end-to-end tracer through a public interface: normalized Viability, Grounding, and Adaptability pillars compose into the five-band `Integrity` read with the foundation-first limiting pillar and moment-in-time pending posture.
3. Complete the unified issue layer, false-confidence one-door behavior, care-point isolation, exposure ordering, and reanalysis-only mutation through observable RED → GREEN → REFACTOR cycles.
4. Bind the real API and executable UI to the Slice 1 integration-map surfaces, including loading, pending, failure/last-good, keyboard, accessibility, and responsive behavior required by the signed specification and prototype.
5. Run targeted unit/integration/negative/API/frontend/E2E tests, activate only genuinely proved GT selectors, run R2 guardrails and broad relevant regressions, then perform security/privacy/tenant-boundary code review.
6. Exercise the real application manually and audit desktop, tablet, and mobile against `release-2/oslo-prototype-r2.html`; store screenshots, test summaries, parity notes, and the manual checklist in this directory.
7. Commit coherent verified implementation, then record its exact SHA and final evidence in the ledger in a separate ledger commit.

## Resumption plan - 2026-08-12 05:03 PKT

1. Restore the seeded Supabase, FastAPI, and Next.js stack and reconnect the required Codex in-app browser.
2. Complete the timeout to stale/last-good to retry journey plus keyboard, announcement/focus, reduced-motion, 200% zoom, permissions, adjacent-regression, and responsive checks if a page attaches.
3. Save and inspect current-run desktop, tablet, and mobile screenshots before accepting UI/UX or prototype-parity evidence.
4. Rerun automated gates and Code Review only after a successful manual gate or any product-code change.
5. Keep Slice 1 `IN PROGRESS` unless every open gate passes; do not acquire Slice 3 or touch Slices 4-10.

**Result:** the seeded platform endpoints, API, and web server were reachable, but the in-app browser timed out before attaching both the initial and supported-recovery fresh pages. No manual interaction, screenshot, product change, or automated completion claim was accepted. Slice 1 remains `IN PROGRESS`.

No work is authorized for Slices 4–10. Slice 3 and Slice 2 remain unchanged during this run.
