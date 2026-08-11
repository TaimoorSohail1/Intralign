# R2 Slice 01 manual regression

**Run:** 2026-08-11 23:10–23:34 PKT

**Environment:** local Supabase, FastAPI, Next.js, Codex in-app browser

**Verdict:** **PARTIAL PASS — completion blocked by the unexercised forced timeout/retry/last-good journey.**

**Current-run retry:** 2026-08-12 00:00–00:09 PKT. The selected Codex in-app browser advertised the required backend, but three fresh-page attempts each timed out before a webview attached. Controlled and user-visible tab lists remained empty, and the visibility capability did not expose a page. No current-run interaction or screenshot was accepted from those attempts.

**Resumption retry:** 2026-08-12 01:02–01:05 PKT. The required Codex in-app browser connected and returned its supported control surface, but two fresh-page attempts timed out before a webview attached. After the first failure, the documented browser recovery procedure was applied: the existing browser binding was retained, controlled and user-visible tab lists were checked and found empty, a fresh tab was requested, and the visibility capability was exposed. Visibility remained false and a second fresh tab also failed to attach. The local Supabase, FastAPI, and Next.js services were healthy, with the API listening on `127.0.0.1:8000` and the web application on `127.0.0.1:3002`; therefore this run again produced no valid manual interaction or screenshot evidence.

**Second resumption retry:** 2026-08-12 02:02–02:05 PKT. The required in-app browser again connected and exposed its supported control surface. The first fresh page timed out before a webview attached. The documented recovery retained the browser binding, confirmed that controlled and user-visible tab lists were empty, requested visibility, and requested one fresh page. Visibility remained false, the second page also timed out before attachment, and both tab lists remained empty. Local Supabase, the seeded owner account, FastAPI on `127.0.0.1:8000`, and Next.js on `127.0.0.1:3002` were healthy. No interaction or screenshot was accepted, and no substitute browser was used.

**Third resumption retry:** 2026-08-12 03:02-03:10 PKT. The required in-app browser connected and returned its supported control surface. The first fresh-page request timed out before a webview attached. The documented recovery retained the browser binding, confirmed empty controlled and user-visible tab lists, exposed visibility, and requested one fresh page; the second request also timed out before attachment. FastAPI returned `200` on `127.0.0.1:8000/health` and Next.js returned `307` on `127.0.0.1:3002`. Supabase could not be reseeded because Docker Desktop's service was unavailable to the scheduler account and the local `54321` endpoint remained closed, but the browser failed before navigation and therefore before authentication or database access could become the active gate. No interaction, screenshot, substitute browser, product change, or automated completion claim was accepted. The open manual gate is unchanged.

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

Automated tests prove failed reanalysis preserves the last-good snapshot and direct issue actions do not move integrity. The required manual forced timeout → stale/last-good → retry journey could not be completed after the chosen in-app browser's semantic click and screenshot channels repeatedly timed out and fresh pages stopped attaching. The 2026-08-12 retry reproduced the attachment failure before any page became controllable.

No alternative browser was substituted. The Product Design browser constraint and the user's explicit in-app-browser requirement therefore leave this gate open; Slice 1 must remain `IN PROGRESS`.

The 01:02–01:05 PKT resumption attempt reached the same blocker before any page existed to control, so timeout → stale/last-good → retry and the remaining accessibility checks are still unexercised.

The 02:02–02:05 PKT resumption attempt reproduced the same attachment blocker after the supported recovery path. The open manual gate is unchanged.
