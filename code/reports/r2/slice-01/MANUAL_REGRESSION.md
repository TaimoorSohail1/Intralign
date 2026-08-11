# R2 Slice 01 manual regression

**Run:** 2026-08-11 23:10–23:34 PKT

**Environment:** local Supabase, FastAPI, Next.js, Codex in-app browser

**Verdict:** **PARTIAL PASS — completion blocked by the unexercised forced timeout/retry/last-good journey.**

## Passed in the real application

1. Signed in as the seeded workspace owner.
2. Created a DevNorth sample project and exercised intake → analysis → Overview.
3. Verified the five bands, limiting pillar, all three pillar controls, moment-in-time copy, and always-visible `live tracking begins at execution` marker.
4. Verified Viability `Sound` (4/4), Grounding `Sound` (12/12), Adaptability `Fragile`, with Adaptability correctly gating the read.
5. Opened the Integrity breakdown and verified all three pillars and anti-forecast copy.
6. Checked 768×1024 and 390×844 responsive geometry. Both had zero horizontal overflow; mobile stacked the pillar controls and moved navigation to the bottom.
7. Inspected the successful Overview browser console; no errors or warnings were present.

## Defects found and corrected

- The live journey exposed an incorrect Grounding `0 of 0` projection. The canonical provenance count now drives Grounding; the real Overview rerun showed 12/12.
- Automated keyboard regression found that Escape dropped focus after closing the breakdown. Focus now returns to the masthead trigger.

## Open manual gate

Automated tests prove failed reanalysis preserves the last-good snapshot and direct issue actions do not move integrity. The required manual forced timeout → stale/last-good → retry journey could not be completed after the chosen in-app browser's semantic click and screenshot channels repeatedly timed out and fresh pages stopped attaching. The browser tabs and viewport overrides were finalized after the attempt.

No alternative browser was substituted. The Product Design browser constraint and the user's explicit in-app-browser requirement therefore leave this gate open; Slice 1 must remain `IN PROGRESS`.
