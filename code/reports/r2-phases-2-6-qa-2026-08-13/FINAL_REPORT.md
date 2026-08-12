# R2 Phases 2–6 Final QA and Implementation Report

**Date:** 2026-08-13  
**Branch:** `codex/release-2-build`  
**Authorized scope:** Slices 1–3 only; Slices 4–10 remain owner-blocked.

## Executive verdict

**PASS — Slices 1, 2, and 3 are complete for the authorized production scope.** The first-time and returning-client journeys, prototype motion, issue lifecycle, real-document extraction, reanalysis, responsive behavior, and regression gates pass. No blocker, major, or minor production-prototype gap remains in the audited states.

Prototype-only developer controls labeled **“not shipped”** are intentionally excluded from production. The spoken NVDA session was not restarted because the owner explicitly requested that NVDA be stopped; keyboard, focus, ARIA, reduced-motion, and responsive accessibility checks pass.

## Phase 1 gap re-check

| Screen / component | Prototype expectation | Original app gap / root cause | Severity | Result | Primary files |
|---|---|---|---|---|---|
| Invitation email | Intralign Alpha invitation card, exact copy, token, and CTA | Local mail used the generic invitation template and the activation origin was not the live web origin | Major | **FIXED** | `services/api/src/oslo_api/email.py`, `services/api/src/oslo_api/settings.py` |
| Account activation | Prefilled invite identity, display name, four role choices, password, stay-signed-in, back link | Activation form exposed only the reduced R1 credential path | Major | **FIXED** | `apps/web/src/components/auth/activation-form.tsx`, `apps/web/src/app/activate/actions.ts` |
| Welcome | Exact welcome copy and “Start your first outcome” CTA | R1 welcome content and geometry differed | Major | **FIXED** | `apps/web/src/app/welcome/page.tsx` |
| First-time intake | Exact headline, explanation, documents, sample, templates, and CTA | Intake used the earlier compact upload screen | Blocker | **FIXED** | `apps/web/src/components/intake/intake-experience.tsx` |
| Returning-client intake | Same intake UI without first-time guided animation | First-time and returning-client state were not separated reliably | Blocker | **FIXED** | `intake-experience.tsx`, `analysis-progress.tsx`, `oslo-api.ts` |
| Onboarding kinetic arc | Prototype graph, narration, outcome decision, Skip/Replay production controls | Simplified production animation and a late iframe-ready race could leave a completed run stuck | Blocker | **FIXED** | `public/r2/onboarding-arc.html`, `analysis-progress.tsx` |
| Prototype bottom controls | Developer timing/mode/restart controls are explicitly labeled “not shipped” | They appeared only in the standalone prototype | Minor | **N/A — correctly excluded**; production Skip/Replay controls pass | `public/r2/onboarding-arc.html`, analysis page |
| Issues shell and header | OFFICIAL masthead, project context, compact integrity, navigation, workspace notice, and OSLO rail | Earlier R1 overview shell and spacing did not match R2 | Blocker | **FIXED** | `project-overview.tsx`, `globals.css`, `brand-lockup.tsx` |
| OSLO proposals | Persistent itemized “OSLO proposes” group in the folded read | Not a data/filter bug: the Slice 2 proposal projection and folded-read renderer did not exist in the earlier production build | Major | **FIXED** | `project-overview.tsx`, API proposal routes, `analysis/service.py` |
| Issue open/close | Inline expansion without repositioning the work column | `scrollIntoView()` moved the selected issue and the detail styling changed the surrounding layout | Major | **FIXED**; main column remains stable | `project-overview.tsx`, `globals.css` |
| Workspace notice dismiss | Dismiss without moving the issue queue | Conditional unmount removed the banner height and reflowed the center column | Major | **FIXED** with a reserved stable slot | `project-overview.tsx`, `globals.css` |
| Proposals / lifecycle trays | Expand and collapse without scroll jump or page-height change | Bodies were mounted/unmounted, changing scroll height | Major | **FIXED** using reserved bodies and visibility states | `project-overview.tsx`, `globals.css` |
| Integrity / advisor toggles | Open/close and Wider/Narrower without moving the work column | Overlay width/state was coupled to surrounding layout | Major | **FIXED**; overlays remain layout-stable | `project-overview.tsx`, `globals.css` |
| Resolved empty state | Resolved tray remains visible at `0 of N settled` | Renderer returned `null` for an empty resolved list | Minor | **FIXED** | `project-overview.tsx` |
| Accepted proposal withdrawal | Accept → Resolved → Withdraw must reopen cleanly | Build proposal acceptance wrote a legacy issue action but no lifecycle attestation, so Withdraw returned `ISSUE_HAS_NO_LIVE_ACT_TO_WITHDRAW` | Blocker | **FIXED test-first and live verified** | `analysis/service.py`, `test_slice_two_analysis.py` |
| Spreadsheet formulas | Extract formula result, never leak formula syntax | `openpyxl` had no cached value for generated `SUM` cells | Major | **FIXED** with bounded simple-SUM evaluation | `analysis/documents.py`, `test_documents.py` |

Visual evidence: [prototype vs. production comparison](evidence/issues-prototype-vs-app.png).

## Phases 2–3 — fixes and re-comparison

- Reused the prototype’s actual onboarding graph/animation engine instead of approximating it.
- Preserved live project names, issue text, evidence counts, and outcomes; fixture values were not hard-coded.
- Verified stable rectangles and scroll positions for issue open/close, workspace dismiss, integrity expansion, advisor width, OSLO Proposes, and lifecycle trays.
- Re-compared the implemented Issues screen against the supplied prototype reference. Result: **no actionable P0/P1/P2 structural or motion mismatch**.

## Phase 4 — functional regression by slice

| Slice | End-to-end result | Notable controls and states exercised | Result |
|---|---|---|---|
| **1 — Outcome-Integrity Engine** | Three-pillar read, weakest-gate queue, workspace notice, inline issue, advisor, navigation, timeout/last-good/retry, responsive and reduced-motion states | Every issue disclosure, close/Escape, integrity toggle, advisor width, tour/dismiss action, navigation link, empty/loading/error/retry state | **PASS** |
| **2 — Issue Lifecycle & Grounding Acts** | Confirm, answer, flag, fix, ground, route, reviewer response, withdraw, OSLO proposal accept/reject, acted/resolved trays, immutable history | Accept → Resolved → Withdraw was live-tested after the final fix; no alert and proposal restored | **PASS** |
| **3 — Reanalysis + Freeze/Unlock** | Fast/deep runs, stale/Undo, retry, first-run kinetic arc, confirm/refine/defer outcome, handoff, returning-client watch mode | Guided and returning paths, Skip/Replay, iframe synchronization, outcome choices, reload persistence, error/recovery | **PASS** |

## Phase 5 — full flow test

| Flow | Evidence | Result |
|---|---|---|
| Admin creates a new client invitation | New invite `qa.r2.20260813@example.com`; exact local Mailpit invitation and working activation URL | **PASS** |
| New user activation and first outcome | Activation → role → welcome → intake → guided prototype animation → outcome handoff → Overview | **PASS** |
| Existing client adds a new project | New project `104beb43-5a79-4e1e-ba05-ead2572b3163`; returning/watch mode shown, guided first-time flow not replayed automatically | **PASS** |

## Phase 6 — real document and reanalysis test

Generated and uploaded:

- `output/r2-live-data/devnorth-2026-project-brief.docx`
- `output/pdf/devnorth-2026-venue-evidence.pdf`
- `outputs/r2-live-data/devnorth-2026-schedule.xlsx`

| Source field | Expected | Extracted | Result |
|---|---:|---:|---|
| Outcome | sold-out, well-rated | sold-out, well-rated | **PASS** |
| Event date | Sep 18 | Sep 18 | **PASS** |
| Registrations | 450 | 450 | **PASS** |
| Attendance target | 405 | 405 | **PASS** |
| Rating target | 4.4 | 4.4 | **PASS** |
| Sponsor revenue target | 12,000,000 | 12,000,000 | **PASS** |
| Total budget | 24,000,000 | 24,000,000 | **PASS** |
| Venue | Expo Centre Lahore | Expo Centre Lahore | **PASS** |
| Venue network capacity | 500 Mbps | 500 Mbps | **PASS** |
| Accountable owner | Aisha Khan | Aisha Khan | **PASS** |
| Spreadsheet formula | Evaluated value; no formula text | Evaluated value; formula did not leak | **PASS** |

Reanalysis on the same uploaded sources completed successfully. Evidence sources increased **8 → 9**, grounded load-bearing details increased **98 → 101**, the answered issue moved to Resolved, the Issues page remained populated with OSLO guidance/proposals, and all live actions remained functional.

## Final automated gates

| Gate | Result |
|---|---|
| Web tests | **24 files, 152 tests passed** |
| API tests | **319 passed** |
| R2 guardrail infrastructure | **4 passed** |
| Active R2 guardrails | **17 passed; 18 active guards; 6/6 prototype corrections** |
| Web lint | **PASS** |
| API lint | **PASS** |
| Next.js production build / TypeScript | **PASS** |

## Final per-slice status

| Slice | What works | Still broken | Prototype gaps | Status |
|---|---|---|---|---|
| 1 | Complete R2 Issues shell and Outcome Integrity flow | None in authorized production scope | None | **COMPLETE** |
| 2 | Complete governed issue/proposal lifecycle including withdrawal and reanalysis | None | None | **COMPLETE** |
| 3 | Complete first-time and returning-client intake/analysis journeys using the prototype motion engine | None | Prototype-only developer controls intentionally excluded | **COMPLETE** |

Slices **4–10 remain OWNER-BLOCKED** and were not modified or advanced.

## Files changed

Implementation changes are limited to the R2 onboarding, activation, welcome, intake, analysis animation adapter, Overview shell/lifecycle surfaces, API invitation/analysis/document services, and their tests. The exact working-tree file list is preserved by the accompanying commit.
