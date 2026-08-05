# OSLO / Intralign deep architecture and feature audit

Date: 30 July 2026  
Project tested: Project Wayfarer Property Management & Central Reservations Platform  
Project ID: `99276a4e-b6d9-48dd-9b4b-f7fe563a4397`

## Executive result

**Overall production-readiness rating: 5.5/10.**

The application shell and most user workflows are functional. The central weakness is the analysis architecture: it does not yet generalize reliably to unseen documents. It combines a large language model with an expanding set of document-specific regular-expression rules, a narrow structured evidence graph, and text-similarity issue reconciliation. This produces missed defects, duplicate findings, unstable issue identities, and scores that move with the generated issue list rather than only with the underlying evidence.

For the Wayfarer benchmark, the current read detects approximately **11 of 18 expected defect concepts (61%)** and **2 of 4 expected critical defect concepts (50%)**. It misses both critical overbooking/inventory and central-rate/local-discount contradictions. It also misses several traceability and completeness gaps. At the same time it publishes 26 active findings because several detected root causes are repeated across artifacts.

The product can support human review today. It should not yet be presented as a dependable autonomous document-assurance engine.

## What was tested

- Source PDF and expected-findings specification were read and visually checked.
- Overview, Issues, issue detail, History and historical snapshot, Attention Map, Inference Map, Reports, all seven artifacts, project sharing, Settings, and a mobile Overview were exercised in the running product.
- Report search, section navigation, schedule form, send form, and invalid-email validation were exercised without sending email.
- Sharing/reviewer controls were inspected without creating another public link or importing reviewer evidence.
- The project was not edited and no analysis was started, because that would change the retained project record.
- Actual email delivery, scheduled delivery, and authenticated export download were not executed because they cause durable/external side effects.

## Automated verification

| Check | Result |
|---|---|
| API tests | 208 passed, 3 warnings |
| Web tests | 105 passed across 20 files |
| Python Ruff | Passed |
| Web ESLint | Passed |
| Next.js production build and TypeScript | Passed |
| Live browser console | Failed: repeated React duplicate-key errors for assumption IDs `AS-01`, `AS-02`, and `AS-03` |
| Golden-document benchmark in CI | Missing |

The passing unit and build checks establish implementation health, but they do not measure unseen-document recall. The new benchmark evaluator is tested only with synthetic unit manifests; no Wayfarer/Greenway/Thornfield golden manifests are wired into a release gate.

## Biggest architectural problems

### P0 — Analysis is a hybrid of model judgment and a document-specific regex library

The workflow asks the model to construct and evaluate the seven artifacts, then merges its findings with deterministic validators. The deterministic validator has grown to 1,531 lines and contains specialized checks such as freeze conflicts, availability conflicts, funding conflicts, procurement gaps, cleaning validation, contamination control, and supplier fallback.

This helps documents that resemble an existing rule, but it does not create a general reasoning system. A new document with different terminology or a different domain can bypass those rules. This is the main reason repeated fixes improve one test pack but a new pack still scores 5–6/10.

Evidence:

- `workflow.py:168–190` merges model and deterministic issues.
- `semantic_validation.py:65–101` enumerates the specialized deterministic checks.
- `semantic_validation.py` is 1,531 lines.

### P0 — The structured evidence graph is too narrow

The evidence graph extracts dates, money, contingency, rates and volumes. Its only implemented relation is effectively a schedule/date constraint violation. It does not represent the general semantic relations needed for the benchmark:

- objective → requirement → deliverable → measure
- business rule → requirement contradiction
- scope inclusion → scope exclusion contradiction
- control obligation → assurance/test evidence
- requirement → traceability target

Because those relations are not first-class, the model must infer them from prose on every run. That is why Wayfarer misses the overbooking conflict, the central-rate/local-discount conflict, two traceability defects, disaster recovery, the missing Domain F requirements, and the unused peak ratio.

Evidence: `evidence_graph.py:117–153`.

### P0 — Completeness checking contains only one deterministic rule

The general completeness module currently defines one rule: regulated-output verification. PCI, privacy, disaster recovery, accessibility, supplier exit, communications, independent assurance and similar gaps still depend mainly on model recall.

Evidence: `completeness.py:24–55`.

### P0 — Evidence selection can omit important context

The model input is capped at 96,000 characters for an initial read and 140,000 for an extended read. Each evidence fragment is truncated to 2,000 characters and fragments containing a fixed keyword list are prioritized.

This is efficient, but it makes results dependent on document layout and vocabulary. A rule or exception outside the first 2,000 characters of a fragment, or expressed without one of the preferred words, can lose priority.

Evidence: `openai_harness.py:1081–1125`.

### P0 — Issue identity is text-similarity based and artifact-local

Reanalysis does not reconcile findings through a canonical evidence/claim identity. It matches wording tokens, only compares candidates inside the same artifact, and accepts a fuzzy threshold of 0.38. Cross-artifact deduplication also needs fairly strong textual/evidence overlap.

Consequences visible in the current project:

- the same availability contradiction appears in Intent, Context, Requirements and Work Breakdown;
- the bedroom-count conflict appears in Requirements and Resources;
- the O3/O5 trace gap appears in Intent and Requirements;
- the cancellation conflict appears in Requirements and Work Breakdown;
- the reservation-volume conflict appears in Scope and Resources.

Evidence: `issue_identity.py:88–128` and `issue_identity.py:147–185`.

### P0 — Scores are directly capped by the generated issue list

Two critical findings in one dimension cap that dimension at Low; four cap it at Very Low. Three material findings cap it at Moderate. Duplicated or misclassified findings therefore lower the score even when the underlying evidence has not changed.

This explains the current mismatch:

- expected Clarity: High; OSLO: Low;
- expected Feasibility: Low; OSLO: Very Low;
- expected Reliability: Moderate; OSLO: Low.

The current score is therefore partly a measure of the issue generator’s output, including its duplicates, rather than only a calibrated assessment of the document.

Evidence: `semantic_validation.py:495–555`.

### P0 — Benchmarking exists but does not govern releases

There is a new evaluator and an operational benchmark script, but:

- the script explicitly says it is not production analysis logic;
- no golden benchmark manifests were found in the repository;
- no CI/release workflow calls it;
- default gates allow only 75% overall recall, 90% critical recall, one trap, and a 10% duplicate rate.

For a product making critical assurance claims, critical recall should be 100% on the approved benchmark set, and repeated runs should be stability-tested.

Evidence: `evaluation.py:59–66` and `run_project_benchmarks.py:1–5`.

### P1 — Reanalysis can resolve a missing previous issue without direct confirmation

When a clarified issue cannot be found in the new analysis and there is not exactly one related issue, the lifecycle code appends the previous issue as resolved. This can mark a valid issue resolved because the new analysis failed to reproduce it, not because new evidence disproved or satisfied it.

Evidence: `understanding.py:113–163`, especially line 156.

### P1 — Large modules concentrate unrelated responsibilities

- Artifact editor: 968 lines
- Report workspace: 812 lines
- Collaboration service: 1,233 lines
- OpenAI harness: 1,154 lines
- Semantic validator: 1,531 lines

This increases regression risk and makes it difficult to test analysis, lifecycle, delivery, and presentation policies independently.

## Major feature problems

### Issues

**Health: Poor for analytical accuracy; good for basic interaction.**

- Filtering, grouping, drill-down, evidence disclosure and clarification controls work.
- The active read contains 26 findings but only about 11 distinct expected defect concepts.
- Several root causes are duplicated across artifacts.
- Filter-chip counts are calculated from all issues, including resolved issues, while the default result list shows active issues. This causes “13 Critical” in the filter with only 12 active critical cards and a confusing “1 finding hidden” message on the default Active view.

Evidence: `project-overview.tsx:1636–1757`.

### Reanalysis and resolution

**Health: Risky.**

- The UI clearly explains saved → stale → reanalyzing states.
- History preserves versions and snapshots.
- The current retained history shows a clarification followed by five new issues, one resolved issue, and a Feasibility downgrade.
- Issue matching is fuzzy and artifact-local, so wording changes can create a new issue while an old issue is resolved or retained separately.

### Inference Map

**Health: Poor.**

- Totals match the Overview: 339 grounded and 23 inferred claims.
- The same three assumptions are repeated across many artifacts with slightly different wording.
- Assumption IDs are reused across artifacts. The React list keys only use `assumption.id`, causing live duplicate-key errors for `AS-01`, `AS-02` and `AS-03`.
- The visual renders one fixed-size pip for every claim. A row with 74 claims needs roughly 888 pixels, so the pips overflow their grid column and overlap adjacent content.
- The assumption-to-issue relationship can be semantically weak because it links one artifact assumption to a text-matched issue.

Evidence:

- `project-provenance.ts:99–125`
- `inference-map.tsx:166–174`
- `globals.css:5086–5156`

### Reports

**Health: Mixed.**

- All seven report sections render.
- Find, section navigation, schedule form, send form and invalid-email validation work.
- Current/previous-analysis handling is implemented: a stale report can be sent only after an explicit warning confirmation.
- The Assumptions section concatenates assumptions from every artifact without semantic deduplication.
- The Plan of action maps the first five issues directly to recommendations, so duplicated issues produce identical recommendations. The live report repeats one recommendation four times.
- Actual email and scheduled delivery were not sent during this audit.

Evidence: `report-workspace.tsx:95–187` and `report-workspace.tsx:452–525`.

### Seven artifacts

**Health: Good extraction, mixed semantics and weak presentation.**

- Intent, Context, Scope, Requirements and Resources preserve much of the source accurately.
- Requirements correctly preserve the five objectives, measures, priorities and phases.
- Work Breakdown converts requirement groups into a WBS-like delivery structure even though the BRD contains no implementation plan. It does label many owners/dependencies unknown, but users can still mistake the generated structure for an approved delivery plan.
- Schedule includes document-control dates and requirement timing as schedule content. “Every date” is part of the generation contract, but document dates should be separated from delivery milestones.
- The same selected issue is passed to every artifact section, so the identical issue card is repeated after every section. This is visible twice in the first Requirements viewport and many more times down the page.
- “Grounded in project evidence” and “Provenance: From OSLO” are shown together. Technically one describes evidence state and the other describes who generated the artifact, but the copy is easy to interpret as contradictory.

Evidence: `artifact-workspace.tsx:559–578` and `artifact-workspace.tsx:954–965`.

### Overview and Attention Map

**Health: UI good; inherited analysis quality poor.**

- Navigation, counts, top-issue actions and the mobile card layout work.
- Attention Map counts sum correctly to the 26 active findings and cell drill-down works.
- Both surfaces faithfully display duplicated and misclassified underlying findings.
- The score labels are too pessimistic compared with the expected assessment because issue-count caps turn duplicate findings into score reductions.

### History

**Health: Good with lifecycle caveats.**

- Runs, version retention, change labels and read-only historical snapshots work.
- Snapshots clearly show the state before a later update.
- The timeline exposes instability: a clarification can be followed by additional findings and a worse dimension score.
- A historical snapshot cannot be restored, only inspected; the UI states this correctly.

### Settings and sharing

**Health: Good in the tested read-only flow.**

- Settings search works and filters to Notifications.
- Account, profile, appearance, notification, workspace, plan, billing and collaboration sections render.
- Disabled owner-only workspace naming is explained.
- Share modal loads workspace members, snapshot-link controls, external-review controls and existing reviewer responses.
- No new link, invitation, preference change or reviewer-evidence import was created during this audit.

## UX and accessibility observations

1. **Overview — Mixed.** The core confidence and grounding summary is readable, but it presents incorrect analytical bands with high visual authority.
2. **Issues — Poor.** The card interactions work, but duplicates and count inconsistencies make prioritization unreliable.
3. **Issue detail — Good.** Evidence, explanation, clarification and resolution paths are organized clearly.
4. **History snapshot — Good.** Read-only state and retained timing are understandable.
5. **Attention Map — Good.** It is the clearest navigation surface and its counts are internally consistent.
6. **Inference Map — Poor.** Claim pips overflow and repeated assumptions make the view difficult to interpret.
7. **Reports — Mixed.** Editing and delivery controls are understandable, but repeated assumptions and recommendations reduce usefulness.
8. **Intent — Good.** Source objectives and measures are preserved.
9. **Context — Good.** Governance and project context are well organized.
10. **Scope — Mixed.** Source content is preserved, but repeated inline findings create excessive page length.
11. **Requirements — Mixed.** Strong extraction; repeated issue cards and very long tables weaken scanning.
12. **Work Breakdown — Mixed.** Complete, but generated requirement groupings can look more authoritative than the evidence supports.
13. **Schedule — Mixed/Poor.** Document-control dates and delivery milestones are not sufficiently distinguished.
14. **Resources — Mixed.** Named parties and estate capacity are useful; business participants and delivery resources are blended.
15. **Settings — Good.** Search and controls are discoverable.
16. **Mobile Overview — Good with minor crowding.** The main cards stack correctly; the top icon bar is dense and some controls become icon-only.

This was not a full WCAG conformance audit. Keyboard semantics were inspected through the accessibility tree and one mobile viewport was checked, but screen-reader combinations, contrast calculations, zoom/reflow at multiple breakpoints and full keyboard traversal were not exhaustively tested.

## Recommended resolution sequence

### Phase 1 — Make correctness measurable

1. Convert Wayfarer, Greenway, Thornfield and at least 10 unseen domain packs into versioned golden manifests.
2. Run each document multiple times and record concept recall, critical recall, trap rate, duplicate-root rate, issue-ID stability, score-band stability and duration.
3. Block release when critical recall is below 100%, overall recall below 90–95%, traps are non-zero, duplicate roots exceed 5%, or score/identity changes across identical runs.

### Phase 2 — Replace text-first reasoning with a domain-general claim graph

1. Normalize objectives, requirements, business rules, scope boundaries, controls, actors, dates, measures, budgets, assumptions and evidence locations.
2. Give each claim and each root cause a stable identity.
3. Model relations such as contradicts, traces-to, satisfies, constrained-by, measured-by, owned-by and verified-by.
4. Run deterministic graph checks for contradiction, missing links and completeness. Use the language model to extract/interpret candidates, not as the sole source of truth.

### Phase 3 — Repair lifecycle and scoring

1. Store one canonical issue/root cause with multiple artifact impacts.
2. Reconcile by claim/evidence identity rather than artifact-local word similarity.
3. Never resolve an issue only because it disappeared from a new model response.
4. Keep `Addressed` after a saved user answer; move to `Resolved` only when the analysis verifies the answer against explicit closure criteria.
5. Calculate dimension bands from validated root causes and coverage confidence, not raw duplicated issue counts.

### Phase 4 — Simplify the product surfaces

1. Show an issue once per artifact at the best matching section, not after every section.
2. Replace one-pip-per-claim with a bounded proportional bar and numeric totals.
3. Deduplicate assumptions and report recommendations by canonical identity.
4. Separate source-derived facts, OSLO-derived structures and user-confirmed content with clearer labels.
5. Label document-control dates separately from delivery milestones.

### Phase 5 — Modularize and harden

1. Split semantic validators into independently testable rule families.
2. Split report composition, delivery, currency and history responsibilities.
3. Split the artifact editor into section, table, lifecycle and issue-annotation modules.
4. Add runtime-console-error checks and screenshot/reflow checks to E2E.

## Evidence screenshots

### Overview

![Overview](C:/Users/Hp/Downloads/oslo-app/output/deep-architecture-audit-2026-07-30/screenshots/01-overview.png)

### Issues

![Issues](C:/Users/Hp/Downloads/oslo-app/output/deep-architecture-audit-2026-07-30/screenshots/02-issues.png)

### Issue detail

![Issue detail](C:/Users/Hp/Downloads/oslo-app/output/deep-architecture-audit-2026-07-30/screenshots/03-issue-detail.png)

### Historical snapshot

![Historical snapshot](C:/Users/Hp/Downloads/oslo-app/output/deep-architecture-audit-2026-07-30/screenshots/04-history-snapshot.png)

### Attention Map

![Attention Map](C:/Users/Hp/Downloads/oslo-app/output/deep-architecture-audit-2026-07-30/screenshots/05-attention-map.png)

### Inference Map

![Inference Map](C:/Users/Hp/Downloads/oslo-app/output/deep-architecture-audit-2026-07-30/screenshots/06-inference-map.png)

### Reports

![Reports](C:/Users/Hp/Downloads/oslo-app/output/deep-architecture-audit-2026-07-30/screenshots/07-reports.png)

### Requirements

![Requirements](C:/Users/Hp/Downloads/oslo-app/output/deep-architecture-audit-2026-07-30/screenshots/artifact-requirements.png)

### Settings

![Settings](C:/Users/Hp/Downloads/oslo-app/output/deep-architecture-audit-2026-07-30/screenshots/10-settings.png)

### Mobile Overview

![Mobile Overview](C:/Users/Hp/Downloads/oslo-app/output/deep-architecture-audit-2026-07-30/screenshots/11-mobile-overview.png)

## Bottom line

The main problem is **architectural**, not simply a missing feature or a weak prompt. The UI is ahead of the reasoning engine. More one-document regex fixes will continue to improve individual test cases without producing dependable new-document performance. The route to a 9/10 product is a versioned golden benchmark gate plus a canonical claim/root-cause graph, stable lifecycle rules, and scoring that operates on validated unique defects rather than the raw model issue list.

No source code was changed during this audit. Only this report and audit screenshots were created.
