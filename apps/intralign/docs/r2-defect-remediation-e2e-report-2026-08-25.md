# R2.0 defect remediation and E2E report

**Date:** 25 August 2026  
**Branch:** `feature/r2-defect-remediation`  
**Base commit:** `3f91df2`  
**Deployment/merge:** Not performed

## Executive result

The authorised R2.0 copy, contract, grounding, lifecycle, outcome, provenance, and first-run defects have been implemented and exercised locally. A real PDF completed the primary OpenAI path, the automatic extended path, and a user-answer reanalysis path. Every published run also passed the deterministic evidence checks before atomic publication.

The implementation is **ready for code review**, but it is not yet an unconditional production release:

- Fast Pass took **142.7 seconds**, above the ratified **60-second P95** gate.
- The two Deep Pass samples took **139.1 seconds** and **109.5 seconds**. Both are below the 180-second ceiling, but only one is below the 120-second target.
- Batch 0 is now implemented and measured with an authenticated, project-scoped `delegate_pm` principal. Assigned-project access succeeds, unassigned-project and owner-only operations return `403`, and owner-only controls are absent from the Delegate-PM UI.

## Client defect status

| Client item | Result | Verification |
|---|---|---|
| Batch 0 — authenticated Delegate-PM request | **Fixed and measured** | Owner invitation grants `delegate_pm` access to exactly one project. The authenticated delegate receives `200` on the assigned project and `403` on an unassigned project and owner-only project creation. Owner-only workspace, invitation, plan, archive, and membership controls are hidden. |
| Batch 1 — page title | **Fixed** | Browser title is `Intralign`; production source no longer uses `OSLO Product Grill`. |
| Batch 1 — Reports dev ribbon | **Fixed** | Internal prototype ribbon removed. |
| Batch 1 — “in this slice” | **Fixed** | Internal delivery wording removed from Share. |
| Batch 1 — raw `[description:1]` token | **Fixed** | Export content uses rendered description text. |
| Batch 1 — lower-cased project names | **Fixed** | Original project-title casing is preserved. |
| Batch 1 — Project/Untitled fallback | **Fixed** | Canonical fallback is `Project`; legacy values remain readable. |
| Batch 1 — hard-coded DevNorth progress copy | **Fixed** | Analysis progress uses document-neutral language. |
| Batch 1 — CAF in export | **Fixed** | Export exposes Outcome Integrity and Viability/Grounding/Adaptability, not CAF as peer pillars. |
| Batch 1 — intake names CAF only | **Fixed** | Intake now explains Viability, Grounding, and Adaptability. |
| Batch 2 — client numeric confidence fields | **Fixed** | Public DTO/OpenAPI, retained snapshots, shared views, and PDF exports do not serialize numeric confidence. Schema-level tests guard renamed equivalents. |
| Batch 2 — false rising/eased trend | **Fixed** | No-history and zero-delta states render steady. |
| Batch 2 — Understanding as graded scale | **Fixed** | UI restores grounded/load-bearing counts; Understanding remains a document grouping only. |
| Batch 2 — HOLDS UP value kind | **Fixed** | Projection carries dependency paths rather than repeating issue description prose. |
| Batch 3.1 — automatic reanalysis | **Fixed** | Governed edits schedule one durable, 1.5-second-debounced run; manual refresh remains an override. |
| Batch 3.2 — conflicting Grounding computations | **Fixed** | Outcome, Overview, History, reports, and collaboration consume the canonical provenance projection. Count-to-band guards were added. |
| Batch 3.3 — basis-free confirmation | **Fixed** | The primary action presents existing confirmation bases directly and persists basis, actor, and timestamp. |
| Batch 3.3b — clarification answer attestation | **Fixed** | Free-text answer is retained and attributed as stated evidence; no second classification step is added. |
| Batch 3.4 — outcome fallback/provenance | **Fixed** | Only explicitly primary outcomes populate the primary slot; no first-item or finding-text fallback is used. |
| Batch 3.5a — narration asserts stale provenance | **Fixed** | Artifact narration is shape/completeness prose; live item provenance remains authoritative. |
| Batch 3.5b — same sentence on two surfaces | **Not reproduced** | Real-document route audit showed distinct Intent and Your Outcome surfaces; no character-identical duplicate was observed. |
| Batch 3.5c — freeze promises inaccessible workspace | **Fixed** | Copy explains a focus/read progression and no longer promises an access lock. |
| Batch 3.5d — CAF-only analysis surfaces | **Fixed** | Intake, analysis subtitle, and analysis log use Viability/Grounding/Adaptability wording. |
| Batch 4 — Fast/Deep performance | **Measured; Fast still fails gate** | Fast 142.7s; Deep 139.1s and 109.5s. The handoff authorizes measurement first, not speculative remediation. |

## Real-document hybrid-flow evidence

Document: `Detailed_Software_Launch_Project_Plan.pdf` (three-page non-sensitive test plan).

| Run | Provider/model | Mode | Runtime | Result |
|---|---|---|---:|---|
| Initial/Fast `427bb009…` | OpenAI `gpt-5.6-luna` | Primary, no fallback | 142.7s | Published 7 provisional artifacts and 16 issues. |
| Automatic Extended `a8cd318e…` | OpenAI `gpt-5.6-terra` | Primary, no fallback | 139.1s | Published the current 7-artifact read and 22 issues. |
| Answer-triggered Extended `9b64191f…` | OpenAI `gpt-5.6-luna` | Primary, no fallback | 109.5s | Published one new current version; latest snapshot has 7 artifacts, 25 total issues, and 24 open issues. |

The answer lifecycle behaved correctly:

1. A user answered the first issue with owner, channels, budget, targets, measurement, and review cadence.
2. The UI showed `Analysis pending`; the issue was not prematurely resolved.
3. Exactly one debounced reanalysis run was created.
4. After successful publication, the answered issue left the open list and all dependent sections moved to the new analysis version.

### Why this proves the hybrid path

- `analysis_node_attempts` recorded provider `openai`, primary execution mode, real model IDs, tokens, and durations for Perceive and Evaluate.
- The workflow then ran deterministic evidence-graph, completeness, contradiction, evidence-rubric, canonicalization, stable-identity, and deduplication checks.
- The seven-artifact and evidence-reference contracts passed before publication.
- No run used the deterministic test harness or a provider fallback.
- Publication was atomic; failed/incomplete states cannot replace the last successful read.

## Section audit on the real document

| Section | Result |
|---|---|
| Issues | Loaded the new current issue set; answer/reanalysis lifecycle passed. |
| Your Outcome | Loaded Outcome Integrity and canonical Viability/Grounding/Adaptability. |
| Grounding Map | Loaded the canonical grounding projection. |
| Reports | Loaded the latest analysis version after reanalysis; retained drafts remain immutable by design. |
| History | Loaded initial, extended, answer, reanalysis, and retained-snapshot events. Failed runs without snapshots now render safely. |
| Intent | Loaded real extracted content. |
| Scope | Loaded real extracted content. |
| Requirements | Loaded real extracted content. |
| Constraints | Loaded real extracted content. |
| Work Breakdown | Loaded real extracted content. |
| Schedule | Loaded real extracted content. |
| Resources | Loaded real extracted content. |
| Full plan/export | Loaded the current seven-document read. |

No audited route showed an application error, artifact-load error, R1 CAF shell, or stale current-analysis marker.

### TC-016 canonical Grounding verification

One published analysis was opened in all five Grounding consumers. Each surface displayed the same canonical result:

| Surface | Browser result |
|---|---|
| Grounding Map | `Fragile` — `0 of 13 load-bearing details grounded` |
| Your Outcome | `Fragile` — `0 of 13 details grounded` |
| Overview | `Fragile` — `0 of 13 settled` |
| History | `Fragile` — `Grounded 0 of 13 load-bearing` |
| Reports | `Fragile` — `0 of 13 load-bearing details rest on your evidence; 13 remain ungrounded` |

History and Reports no longer calculate Grounding from separate claim or evidence-register counts. Verified evidence, issue lifecycle, load-bearing inclusion, banding, and the primary-inference cap are now projected once and reused everywhere.

## Delegate-PM project-scope evidence

The authorised Batch 0 role model is implemented end to end:

1. An owner invites a Delegate-PM to a specific project.
2. Invitation activation creates a `project_memberships` grant, not an owner-level workspace membership.
3. The Delegate-PM can read, edit, co-ground, collaborate, and manage outcomes on the assigned project.
4. The same authenticated user receives `403` for an unassigned project's collaboration and outcome routes; a direct browser URL to that project now returns the delegate to `/workspace` instead of rendering an unowned Intake screen.
5. Project creation and owner-only workspace controls remain unavailable and return `403` at the API boundary.
6. The browser security measurement passed on desktop; tablet and mobile duplicates are intentionally skipped because authorization is viewport-independent.

## Automated verification

| Check | Result |
|---|---|
| TC-016 focused web suites | **47 passed** |
| Full web component/unit suite | **283 passed; 5 parallel-load timeouts**. The five timed-out suites passed independently (**72/72**), so no functional regression was reproduced. |
| API unit/integration suite | **430 passed** |
| R2 guardrails | **Passed** |
| API Ruff | **Passed** |
| Web ESLint | **Passed** |
| Production build and TypeScript | **Passed** |
| Cross-viewport Playwright E2E | **Passed** — 82 passed and 2 intentionally skipped; 84 tests across 15 files, with no failures |

The full API run initially exposed one History null-snapshot regression. It was fixed by treating failed runs as having zero provenance counts, and the targeted integration test plus the complete API suite passed afterward.

The cross-viewport run also exposed stale R1 assumptions in three E2E contracts: statements now require the explicit R2 Edit action, while tablet/mobile use the compact header instead of desktop-only Plan and sidebar controls. The tests now exercise the real responsive R2 interactions. No product route, data, editor, or lifecycle regression remained after those corrections.

## Recommendation

Proceed to code review for the R2 defect-remediation branch. Do not merge, deploy, or describe the release as performance-complete until:

1. The Fast Pass architecture meets the 60-second P95 gate.

All functional, contract, static, and cross-viewport gates exercised by this remediation are green. No merge or deployment was performed.
