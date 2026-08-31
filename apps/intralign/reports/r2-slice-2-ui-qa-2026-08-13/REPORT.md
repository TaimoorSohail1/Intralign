# R2 Slice 2 UI/UX and QA final report

**Audit date:** 2026-08-13
**Reference:** `release-2/oslo-prototype-r2.html`
**Implementation:** authenticated local application at the same 1280 × 720 viewport
**Verdict:** PASS for the applicable Slice 2 UI and owner-act flow. No open P0, P1, or P2 visual or functional defect remains.

## Corrections made during this audit

- Matched the prototype's complete OFFICIAL masthead copy, Understanding-document order, and governed OSLO header with a working Wider/Narrower control.
- Made issue opening scroll the inline card into view and use the prototype's 340 ms entrance timing.
- Restored the prototype issue-card hierarchy: summary and Affects/Holds up, first-time guidance, recommendation and three owner actions, then optional clarification and supporting disclosures.
- Removed implementation-only lifecycle/status chrome and proposal-kind badges from the prototype surfaces; durable state is still present in the lifecycle trays and backend.
- Copied the applicable prototype motion values for workspace unlock, notice entrance, tray flash, and tray-row settle, with a `prefers-reduced-motion` no-animation fallback.
- Preserved truthful backend-driven project names, findings, counts, pillars, evidence, and proposal text. These values intentionally differ from the DevNorth prototype fixture.

## Functional and manual regression

| Check | Result |
|---|---|
| Ranked queue and first issue open/close | PASS |
| Issue auto-position, keyboard focus, Escape/focus restoration | PASS |
| Confirm / flag / ask-for-evidence controls remain available | PASS |
| Route to external evidence holder | PASS — real secure review route created |
| Awaiting Evidence tray and 1 s cool-blue flash | PASS |
| Withdraw routed issue | PASS — queue restored without error |
| Proposal Accept/Reject surfaces | PASS — automated and prior live persisted decision coverage |
| Resolved / Awaiting / Acted-on lifecycle separation | PASS |
| 1280 × 720 prototype comparison | PASS |
| 390 × 844 responsive check | PASS — no horizontal overflow |
| Motion timing | PASS — 340 ms issue/proposal entrance, 1 s tray flash, 1.25 s row settle |
| Reduced-motion implementation | PASS by code inspection; the approved browser exposes viewport emulation but not media-preference emulation |

## Automated evidence

- API: **316 passed**.
- Web: **24 files / 145 passed**.
- Focused Overview: **46 passed**.
- R2 guardrails: **4 infrastructure + 17 active-runner tests passed; 18/60 guards active**.
- ESLint: PASS.
- Next.js production build and TypeScript: PASS.

## Matched-state visual evidence

- [Queue comparison](compare-01-queue.png)
- [Expanded issue comparison](compare-02-issue.png)
- [Proposal comparison](compare-03-proposals.png)
- [Live Awaiting Evidence tray](13-app-awaiting-tray.png)

The comparison accepts only structural/style parity. Fixture content is not copied into production: the prototype shows DevNorth data, while the application shows its actual persisted project state.

## Remaining

Only the owner-deferred combined spoken screen-reader session for Slices 1–3 remains. That is an accessibility evidence gate, not a known Slice 2 UI or functional defect. Slices 4–10 remain blocked by the release ledger.
