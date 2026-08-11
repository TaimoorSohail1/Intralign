# R2 Slice 01 manual regression

**Run:** 2026-08-11 23:10–23:34 PKT
**Environment:** local Supabase, FastAPI, production Next.js build, Codex in-app browser.
**Verdict:** **PARTIAL PASS — completion blocked by unexercised failure/retry states and invalid parity captures.**

## Exercised flow

1. Signed in as the seeded workspace owner.
2. Created a project from the DevNorth sample.
3. Submitted the intake and observed the real analysis transition to the project overview.
4. Verified the executable overview exposes the five bands, named limiting pillar, all three decomposition controls, moment-in-time copy, and always-visible `live tracking begins at execution` marker.
5. Verified the live read after the Grounding fix: Viability `Sound` (4/4), Grounding `Sound` (12/12 outcome-bearing items), Adaptability `Fragile`, with Adaptability correctly gating the read.
6. Opened the Integrity breakdown and verified the three decomposed pillars and anti-forecast copy.
7. Audited responsive geometry through the in-app browser at 768×1024 and 390×844. Both had zero horizontal overflow. Tablet retained a 62px navigation rail and three side-by-side pillar controls. Mobile used a 390px bottom navigation, a 338px content card, stacked 292px pillar controls, and a zero-height advisor slot.
8. Inspected the browser console during the successful overview path; no errors or warnings were reported.

## Failure and recovery checks

- The first overview load failed because an already-running `next start` process had its `.next` directory replaced by the production build. The exact validated local web/API processes were restarted and the identical journey passed; this was an environment-process mismatch, not accepted as a product pass/fail signal.
- The live journey exposed the incorrect Grounding `0 of 0` state. It was fixed and rerun successfully.
- Automated Slice 1 tests prove failed reanalysis preserves the last-good snapshot and direct issue actions do not move integrity; a full manual forced-timeout/retry exercise remains open because browser actions began timing out before that state could be completed.
- Authorization remains enforced by the existing user-context/project-access boundary. No cross-tenant mutation was introduced by the read-only integrity projection.

## Open manual gate

The in-app browser repeatedly returned `Unable to capture screenshot`, capture timeout, and then fresh-tab attachment timeout. Semantic DOM inspection and responsive geometry succeeded, but the required timeout/retry/last-good journey could not be completed.

A separate Slice-1-only capture harness saved six images. Inspection rejected them because the prototype is on its pre-confirmation screen while the implementation is on the analyzed Overview. They are blocker evidence, not parity evidence. Manual regression therefore cannot be marked complete.
