# OSLO analysis reliability implementation plan

Date: 30 July 2026  
Status: Approved architecture decisions; implementation not started

## 1. Objective

Replace the current document-specific, text-similarity-heavy analysis path with a benchmark-governed architecture that:

- works consistently across unseen project documents;
- detects all approved critical benchmark defects;
- represents evidence and relationships explicitly;
- produces one stable root issue with multiple artifact impacts;
- never resolves an issue merely because a later model response omitted it;
- calculates ratings from unique validated root causes and evidence coverage;
- preserves the last trusted read during reanalysis or failure.

## 2. Success gates

The new engine cannot become the default until it achieves:

| Gate | Required result |
|---|---:|
| Critical finding recall | 100% |
| Overall expected-finding recall | At least 90% |
| Documented trap findings | 0 |
| Duplicate-root rate | Below 5% |
| Evidence-locator coverage | 100% for published issues |
| Identical-run issue-ID stability | At least 95% |
| Identical-run rating-band stability | 100% |
| Initial-analysis p95 duration | 120 seconds or less |
| Extended-analysis p95 duration | 240 seconds or less |
| Analysis timeouts on release suite | 0 |
| Existing API, web, lint and build checks | All passing |

The first benchmark set will contain Wayfarer, Greenway, Thornfield and at least ten unseen packs from different domains. Benchmark documents must never be inserted into production prompts.

## 3. Scope

### In scope

- Golden benchmark manifests and CI release gates
- Semantic evidence coverage ledger
- Canonical claim and relationship graph
- General contradiction, traceability and completeness checks
- Canonical root issues and artifact impacts
- Stable reanalysis identity and governed issue lifecycle
- Calibrated Clarity, Alignment, Feasibility, Reliability and Confidence
- Artifact, Inference Map, Issues and Reports deduplication
- Historical compatibility, shadow mode, rollout and monitoring

### Out of scope

- Replacing the existing seven-artifact product model
- Automatically rewriting historical snapshots
- Removing human review for critical findings
- Training a custom foundation model
- Adding unrelated integrations, billing or collaboration features
- Guaranteeing perfect results for every possible future document

## 4. Target architecture

The future analysis path will be:

1. **Ingest:** parse every document into semantic sections with stable source locators.
2. **Coverage ledger:** record which sections were processed, truncated, unsupported or failed.
3. **Extract claims:** use structured extraction for objectives, requirements, rules, scope, controls, actors, dates, values, measures and assumptions.
4. **Normalize:** canonicalize dates, currencies, units, entities and requirement identifiers while preserving the source text.
5. **Build relations:** connect claims through `contradicts`, `traces_to`, `satisfies`, `measured_by`, `owned_by`, `verified_by`, `constrained_by` and `depends_on`.
6. **Validate:** run domain-general graph checks; use isolated domain extensions only when needed.
7. **Create root issues:** publish one canonical root cause with one or more artifact/section impacts.
8. **Reconcile:** match issues by stable claim/evidence identity across analysis runs.
9. **Score:** calculate ratings from validated unique root issues, applicability, evidence coverage and uncertainty.
10. **Present:** generate the seven artifacts, Issues, maps and Reports from the same canonical data.

The language model remains responsible for structured interpretation and candidate extraction. Deterministic code validates identity, arithmetic, relationships, applicability, lifecycle and release gates.

## 5. Delivery strategy

Implement behind an `analysis_engine_v2` feature flag. Keep the existing engine available throughout delivery. V2 initially runs in shadow mode and cannot replace the current result until all gates pass.

## 6. Phase plan

### Phase 0 — Baseline, benchmarks and safety

**Goal:** make quality measurable before changing production analysis.

Work:

1. Define the golden-manifest schema:
   - expected finding ID and severity;
   - root-cause concept;
   - expected evidence locations;
   - acceptable title variations;
   - prohibited traps;
   - expected dimension bands;
   - applicability notes.
2. Convert Wayfarer, Greenway and Thornfield expectations into versioned manifests.
3. Add at least ten unseen-domain packs.
4. Extend the benchmark runner to:
   - run initial and extended analysis;
   - repeat each run at least three times;
   - measure recall, traps, duplicates, locator coverage, identity stability, score stability, latency and failure rate.
5. Add CI reporting and release gates.
6. Store benchmark results as build artifacts for review.

Primary areas:

- `services/api/src/oslo_api/analysis/evaluation.py`
- `services/api/scripts/run_project_benchmarks.py`
- new versioned benchmark fixture directory
- CI configuration

Tests:

- Manifest schema validation
- Concept matching and duplicate-root detection
- Gate pass/fail tests
- Repeatability calculations
- Invalid or incomplete manifest handling

Exit criteria:

- Current engine has a recorded baseline.
- Benchmarks run locally and in CI.
- A failing critical-recall result blocks release.

Estimated effort: 1–2 weeks.

### Phase 1 — Tracer bullet: one claim graph path end to end

**Goal:** prove the new architecture with the smallest complete vertical slice.

Use the Wayfarer overbooking/inventory contradiction because the current engine misses it.

End-to-end behavior:

1. Extract the “5% overbooking” and “no inventory beyond physical capacity” claims.
2. Normalize both claims against the same inventory subject.
3. Create a `contradicts` relation with both evidence locators.
4. Produce one canonical critical root issue.
5. Attach its impacts to the appropriate artifacts/sections.
6. Display it once in Issues and once at the best artifact location.
7. Keep its ID unchanged across identical reanalysis.
8. Count it once in scoring.
9. Include it once in Reports and the Inference Map.

Primary areas:

- `services/api/src/oslo_api/analysis/evidence_graph.py`
- `services/api/src/oslo_api/analysis/models.py`
- `services/api/src/oslo_api/analysis/workflow.py`
- `services/api/src/oslo_api/analysis/persistence.py`
- `apps/web/src/components/overview/project-overview.tsx`
- `apps/web/src/components/artifacts/artifact-workspace.tsx`
- `apps/web/src/components/inference/inference-map.tsx`
- `apps/web/src/components/reports/report-workspace.tsx`

Tests:

- Claim extraction and normalization
- Contradiction relation
- Canonical root ID
- Multiple impacts without duplicate cards
- Stable repeated run
- UI/report presentation

Exit criteria:

- The missed critical contradiction is detected reliably.
- The complete UI/API/data path works behind the V2 flag.
- No existing project output changes when V2 is disabled.

Estimated effort: 1–2 weeks.

### Phase 2 — Semantic ingestion and coverage ledger

**Goal:** ensure every relevant source section is processed transparently.

Work:

1. Replace fixed fragment-first prioritization with semantic sectioning.
2. Preserve stable document/page/section/row locators.
3. Record coverage for every section:
   - processed;
   - partially processed;
   - unsupported;
   - extraction failed.
4. Use hierarchical summarization only after full section registration.
5. Make input-budget decisions visible to the analysis and reliability calculation.
6. Prevent issue publication when required evidence locators were lost.

Tests:

- Long table-heavy PDFs
- Requirements spanning page/chunk boundaries
- Repeated headings
- OCR and low-confidence extraction
- Ten-document maximum pack
- No silent source-section omission

Exit criteria:

- 100% source-section accounting.
- Any skipped or failed content lowers reliability transparently.
- Benchmark locator coverage is 100%.

Estimated effort: 1–2 weeks.

### Phase 3 — General claim graph and validation families

**Goal:** cover the benchmark through reusable relations rather than one-document regexes.

Implement these validation families:

1. **Value contradictions**
   - dates, quantities, rates, percentages, currencies, units and retention periods.
2. **Business-rule contradictions**
   - overbooking/inventory, central/local authority, policy exceptions and phase rules.
3. **Traceability**
   - problem → objective → intervention → requirement → deliverable → measure.
4. **Scope consistency**
   - inclusion/exclusion, deferred/Must, feature/out-of-scope.
5. **Control completeness**
   - applicability → requirement → owner → verification → evidence.
6. **Delivery feasibility**
   - dependency order, capacity, allocation, schedule, procurement and fallback.
7. **Benefits and measurement**
   - baseline, target, owner, frequency, attribution and double counting.

Rules must be configured by claim types and relations. Domain-specific patterns must live in isolated extension modules and require their own benchmark fixtures.

Tests:

- Every expected benchmark finding has a named automated test.
- Every documented trap has a negative test.
- Unit normalization and cross-unit comparison
- Rationale/exception suppression
- Missing-control applicability checks

Exit criteria:

- 100% critical recall and at least 90% overall recall on the approved suite.
- Zero documented traps.
- No validator depends on a specific project name.

Estimated effort: 2–3 weeks.

### Phase 4 — Canonical issues, lifecycle and reanalysis

**Goal:** make findings stable and governed across artifacts and time.

Data model:

- `root_issue`: canonical problem, severity, dimension, closure criteria and status.
- `issue_impact`: artifact, section, claim and presentation context.
- `issue_evidence`: supporting or conflicting claim/evidence IDs.
- `issue_transition`: actor, reason, source run and timestamp.

Lifecycle:

- `Open`: gap exists and no user response is saved.
- `Addressed`: a meaningful answer/fix is saved.
- `Resolved`: reanalysis verifies explicit closure criteria.
- `Reopened`: new or conflicting evidence invalidates closure.

Rules:

1. Disappearance from a model response never resolves an issue.
2. Issue identity is based on canonical claims and root-cause type.
3. Artifact placement changes do not change root identity.
4. A root issue can have many impacts but only one lifecycle.
5. Failed or timed-out analysis leaves the previous lifecycle unchanged.

Tests:

- Same evidence, changed wording
- Same root cause, different artifact impact
- Partial clarification → Addressed
- Complete evidence → Resolved
- Missing response → remains unchanged
- New contradiction → Reopened
- Timeout and retry

Exit criteria:

- At least 95% issue-ID stability across identical runs.
- Zero automatic resolutions caused only by omission.
- Duplicate-root rate below 5%.

Estimated effort: 1–2 weeks.

### Phase 5 — Rating calibration

**Goal:** make ratings stable, explainable and independent of duplicate cards.

Work:

1. Score unique validated root issues only.
2. Separate:
   - document clarity;
   - strategic alignment;
   - delivery feasibility;
   - evidence reliability;
   - analysis confidence.
3. Include applicability and coverage uncertainty.
4. Prevent presentation impacts from multiplying severity.
5. Store an explanation payload containing:
   - limiting validated roots;
   - coverage gaps;
   - calibration version;
   - benchmark version.
6. Calibrate against approved expected bands.

Tests:

- Duplicating an impact does not change the score.
- Moving an issue between artifacts does not change the score.
- Missing evidence affects Reliability/Confidence, not automatically Clarity.
- Identical evidence produces the same rating bands.

Exit criteria:

- 100% rating-band stability across identical runs.
- Wayfarer expected Clarity/Alignment/Feasibility bands match the approved benchmark.
- Every band has a user-readable explanation.

Estimated effort: 1 week.

### Phase 6 — Product-surface cleanup

**Goal:** present canonical data clearly.

Work:

1. Issues:
   - counts use the active lifecycle lens consistently;
   - root issue shown once;
   - impacted artifacts listed inside the issue.
2. Artifacts:
   - show an issue at the best matching section only;
   - link to other impacts;
   - distinguish source-grounded, OSLO-derived and user-confirmed content.
3. Inference Map:
   - use stable composite/canonical IDs;
   - replace one-pip-per-claim with bounded proportional bars;
   - deduplicate assumptions;
   - link assumptions through claim relations.
4. Reports:
   - deduplicate assumptions, risks and recommendations;
   - preserve the previous-analysis confirmation rule;
   - label source-derived versus generated planning structures.
5. Schedule and Work Breakdown:
   - separate document-control dates from delivery milestones;
   - clearly mark generated structures and unknown planning data.

Tests:

- No React duplicate-key warnings
- No horizontal overflow at desktop, tablet or mobile widths
- Count consistency across Overview, Issues and Attention Map
- One root recommendation in Reports
- Keyboard and screen-reader labeling
- Current/previous-analysis delivery warning

Exit criteria:

- Browser console contains no product errors.
- UI counts agree on all tested lifecycle filters.
- Responsive and accessibility QA passes.

Estimated effort: 1–2 weeks.

### Phase 7 — Migration, shadow mode and rollout

**Goal:** introduce V2 without corrupting trusted history.

Work:

1. Keep all existing snapshots read-only.
2. Do not rewrite old issue IDs or scores.
3. Generate V2 claims and issues only during a new controlled reanalysis.
4. Run V1 and V2 in parallel for selected internal projects.
5. Compare:
   - missed/extra findings;
   - issue consolidation;
   - score changes;
   - latency and cost.
6. Require human approval for material V1/V2 differences during shadow mode.
7. Roll out progressively:
   - internal QA;
   - selected pilot projects;
   - new projects by default;
   - existing projects on reanalysis;
   - V1 retirement after the rollback window.

Rollback:

- Disable `analysis_engine_v2`.
- Continue serving the last successful retained snapshot.
- Never apply V2 lifecycle transitions when the V2 run fails.

Exit criteria:

- Release gates pass on CI and shadow projects.
- No data-loss or lifecycle regression.
- Product and QA owners approve default activation.

Estimated effort: 1–2 weeks.

## 7. Kanban-ready work items

Each item should be implemented with failing tests first.

1. Create versioned benchmark manifest schema.
2. Convert Wayfarer expected findings into a golden manifest.
3. Convert Greenway and Thornfield into golden manifests.
4. Add ten unseen-domain benchmark packs.
5. Add repeated-run stability metrics and CI gates.
6. Introduce the V2 feature flag and shadow-run record.
7. Add canonical claim and relation models.
8. Implement the overbooking contradiction tracer bullet.
9. Add semantic sectioning and the coverage ledger.
10. Add value/unit normalization.
11. Add business-rule contradiction validators.
12. Add objective/requirement/measure traceability validators.
13. Add scope-consistency validators.
14. Add applicable-control completeness validators.
15. Add feasibility and dependency validators.
16. Add canonical root issue and impact persistence.
17. Replace fuzzy artifact-local lifecycle reconciliation.
18. Implement Open → Addressed → Resolved → Reopened transitions.
19. Rebuild rating calculation from validated roots and coverage.
20. Consolidate Issue and Attention Map counts.
21. Deduplicate artifact issue annotations.
22. Rebuild Inference Map claim visualization and keys.
23. Deduplicate report assumptions and recommendations.
24. Separate source-confirmed and OSLO-generated planning structures.
25. Add V1/V2 comparison dashboard and production metrics.
26. Run shadow rollout and approve default activation.

Every issue must include:

- goal;
- files or architectural area;
- acceptance criteria;
- unit/integration/E2E expectations;
- benchmark impact;
- migration or rollback risk.

## 8. Required review and QA gates

For every vertical slice:

1. Failing tests written first.
2. Smallest implementation makes them pass.
3. API and web unit tests pass.
4. Ruff, ESLint, TypeScript and production build pass.
5. Relevant golden benchmarks pass.
6. AI review checks correctness, security, privacy, lifecycle and regression risk.
7. Human code review approves data-model and product-policy changes.
8. Manual QA covers happy path, failure, timeout, retry, responsive layout and accessibility.
9. The feature flag remains off until the slice is accepted.

## 9. Main risks and controls

| Risk | Control |
|---|---|
| Benchmark overfitting | Keep unseen holdout packs and prohibit benchmark text in prompts |
| New graph creates more latency | Measure each stage, cache normalized claims and set phase budgets |
| V1/V2 issue identities conflict | Keep separate engine/calibration versions and migrate only on controlled reanalysis |
| Historical data changes | Never rewrite retained snapshots |
| Model wording remains variable | Base identity on normalized claims/evidence, not generated titles |
| General rules create false positives | Applicability checks, exception detection and negative trap fixtures |
| Scores change unexpectedly | Version calibration and show a V1/V2 comparison before activation |
| Failed rollout affects users | Feature flag, last-good snapshot and immediate V1 rollback |

## 10. Delivery estimate

For one cross-functional team with backend/AI, frontend and QA capacity:

- Expected implementation: **9–14 weeks**
- Shadow validation: **2–4 additional weeks**

For one developer working mostly sequentially, expect a longer schedule. These are planning ranges, not delivery commitments; Phase 0 benchmark results may change the estimate.

## 11. Definition of done

The work is complete only when:

- all approved success gates pass;
- V2 succeeds on the golden and unseen benchmark sets;
- identical runs are stable;
- critical findings require human confirmation;
- no issue is resolved because of model omission;
- historical snapshots remain unchanged;
- all product counts and reports use canonical issues;
- production monitoring and rollback are active;
- human code review and manual QA approve the rollout.

