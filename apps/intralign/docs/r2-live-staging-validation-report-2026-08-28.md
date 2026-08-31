# R2 live staging validation report

**Date:** 28 August 2026  
**Environment:** Heroku staging  
**Web:** `intralign-oslo-web-staging` release v45  
**API:** `intralign-oslo-api-staging` release v64  
**Branch:** `feature/r2-defect-remediation`  
**Main merged:** No  

## Executive result

**Overall: conditional pass for staging; no-go for public production.**

The complete authenticated R2 journey was exercised against the live staging application with an isolated QA account and project. Real DOCX, XLSX, and PDF evidence was processed through the OpenAI harness plus deterministic validation. Initial analysis, extended analysis, governed confirmation, reanalysis, atomic publication, OSLO chat, all project sections, exports, collaboration surfaces, settings, notifications, and the product tour were inspected in the browser.

| Result | Sections |
|---|---:|
| Passed | 8 |
| Partially passed | 2 |
| Failed | 0 |

The two partial results are analysis performance and unexecuted external delivery actions. Core analysis and lifecycle correctness passed.

## Test data and safety

- Isolated QA workspace: `Codex R2 Live Validation`
- Isolated project: `DevNorth 2026`
- Real files: one DOCX project brief, one XLSX schedule, and one PDF venue-evidence document
- No client project or user record was changed
- No invitation, external share link, scheduled report, or real email was sent
- Report/send/share forms were validated up to the final external side effect

## Ten-section result

| # | Section / slice | Result | Browser evidence |
|---:|---|---|---|
| 1 | Authentication and onboarding | Pass | Personalized welcome loaded; first outcome created a project; authenticated navigation remained stable. |
| 2 | Intake, upload, and analysis | **Partial** | DOCX/XLSX/PDF uploaded and completed with the real OpenAI harness and deterministic validation. Runtime exceeded the 60-second target. |
| 3 | Overview, Outcome, and integrity | Pass | Outcome Integrity, issue counts, grounding state, current-analysis state, and project summary were coherent. |
| 4 | Issues and governed reanalysis | Pass | `Confirm — it holds`, reviewer attestation, Analysis pending, one queued reanalysis, and atomic publication worked. One issue became grounded while 15 remained open. |
| 5 | Seven artifacts and Full Plan | Pass | Intent, Scope, Requirements, Constraints, Work Breakdown, Schedule, Resources, and Full Plan loaded with evidence and item-level provenance. Editing controls were present. |
| 6 | Grounding Map | Pass | Displayed 1 of 16 load-bearing details grounded and 15 inferred, consistent with the published issue state. |
| 7 | History and snapshots | Pass | Initial, extended, confirmation, and reanalysis events were retained. The completed run became the current trusted view without losing prior snapshots. |
| 8 | OSLO advisor/chat | Pass | A source question returned accurate page-level venue evidence: capacity, throughput, failover, date, and accountable owner. |
| 9 | Reports, export, share, and collaboration | **Partial** | Editor, recipient, sections, PDF/export formats, Send, Schedule, Share, Owner/Delegate-PM roles, and external-review UI worked. Final real email/invite/share actions were intentionally not executed. |
| 10 | Settings, tiering, notifications, tour, and workspace | Pass | Basic-plan copy, limits, settings sections, three non-duplicate run notifications, five-step tour, and project switcher worked. |

## Real analysis and synchronization evidence

| Check | Result |
|---|---|
| OpenAI harness, not deterministic test harness | Pass |
| Deterministic evidence validation | Pass |
| Unsupported locator safely quarantined | Pass |
| Initial analysis published atomically | Pass |
| Extended analysis published atomically | Pass |
| Exactly one reanalysis after confirmation | Pass |
| Project current-analysis ID matched completed reanalysis | Pass |
| Issues, Outcome, Grounding, History, Reports, Full Plan synchronized | Pass |
| Last successful read preserved during processing | Pass |
| Seven artifact versions retained | Pass |

The analysis correctly extracted DevNorth, 450 attendees, 18 September, 4.4/5, PKR 12m, schedule dates, network capacity, Wi-Fi/failover requirements, and the named accountable contact.

## Performance

| Operation | Observed | Target | Result |
|---|---:|---:|---|
| Initial analysis | 373 s | 60 s | Fail |
| Extended analysis | 176 s | 180 s | Pass, close to limit |
| Governed reanalysis | 134.5 s | 60 s | Fail |
| Authenticated section loads after deployment | 1.3–1.8 s | Practical UI response | Pass |

The initial run included a database-capacity interruption before the pool correction, so 373 seconds is not a clean model-only benchmark. Reanalysis still exceeded the 60-second product target.

## Defects found and fixed during live validation

| Defect | Root cause | Fix | Verification |
|---|---|---|---|
| Intermittent page and API failures | Default SQLAlchemy pools exceeded the Supabase session-mode connection limit | Bounded application pools to one connection with zero overflow, recycle, pre-ping, and LIFO | 28 authenticated route loads completed; no new `EMAXCONNSESSION`, 500, or error screen |
| Platform admin invitation access failure | Admin user was not resolved into the invitation workspace | Kept platform-admin invitation access attached to the correct workspace | Admin invitation route and authenticated shell passed |
| Basic account described Free limits | Settings copy was hard-coded to the Free plan | Made headings, capacity details, and comparison action plan-aware | Live v45 displayed Basic-specific copy |
| Missing inferred primary-outcome row | Publication updated an existing inferred outcome, but inserted a missing outcome only in the `None` branch | Moved insert-if-missing into the non-empty inferred-outcome branch | Isolated lifecycle test passed; active R2 guardrail integration path passed |

## Automated verification

| Gate | Result |
|---|---|
| Web assertions | 294/294 verified; four parallel-run timeouts passed 119/119 in isolated single-worker rerun |
| API suite | All assertions passed except the inferred-outcome defect discovered in the full run; the defect was fixed and its isolated test passed |
| Active R2 guardrail API set | 43/43 passed |
| Active R2 guardrail web set | 120/120 passed |
| Guardrail definition checks | 8/8 passed |
| Web lint | Pass |
| API Ruff | Pass |
| TypeScript and production build | Pass |
| Responsive desktop/tablet/mobile E2E baseline | 81/81 passed on the current R2 flow before the final API-only persistence correction |

The parallel Vitest run was resource-saturated on the Windows QA host. All timed-out tests passed when isolated; no assertion failure remained.

## Deployment verification

- API `/health`: `ready`
- API web dyno: up
- Durable worker dyno: up
- Authenticated post-deployment routes: Overview, Issues, Outcome, Grounding, History, Intent, Resources, Full Plan, and Reports all loaded without an error screen
- Post-deployment load time: 1.3–1.8 seconds per inspected route
- No new database-capacity, traceback, or server-error log entry after v64 startup

## Evidence

- [Live Outcome](https://intralign-oslo-web-staging-9f21dcd15274.herokuapp.com/projects/e0f0a2fc-4694-4829-beb7-673c2b11a9ab/outcome)
- [Live Reports](https://intralign-oslo-web-staging-9f21dcd15274.herokuapp.com/projects/e0f0a2fc-4694-4829-beb7-673c2b11a9ab/reports)
- [Live Issues](https://intralign-oslo-web-staging-9f21dcd15274.herokuapp.com/projects/e0f0a2fc-4694-4829-beb7-673c2b11a9ab/issues)
- [Live Grounding Map](https://intralign-oslo-web-staging-9f21dcd15274.herokuapp.com/projects/e0f0a2fc-4694-4829-beb7-673c2b11a9ab/grounding)

These authenticated routes contain the isolated QA evidence used for this report. They require access to the staging workspace.

## Remaining release risks

1. Initial analysis and reanalysis remain slower than the 60-second product target.
2. A real external Gmail/Postmark delivery, invitation acceptance, share link, and scheduled report still require an explicitly authorized end-to-end delivery test.
3. Supabase billing/quota status should be confirmed before public traffic.
4. Rotate any deployment credential that may have appeared in historical local deployment output as a precaution.

## Recommendation

**Staging:** ready for stakeholder review.  
**Public production:** no-go until performance is brought within the agreed target, Supabase capacity is confirmed, and one authorized real external-delivery journey passes.

Rollback points are web v44 and API v63.
