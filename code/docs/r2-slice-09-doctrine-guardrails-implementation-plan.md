# R2 Slice 9 — Doctrine Guardrails and FE↔BE Integration Map implementation plan

Status: **Approved for implementation planning on 2026-08-16; product implementation and deployment remain separate actions**

This is a non-canonical delivery plan. It does not ratify or rewrite OSLO doctrine. The authoritative Slice 9 definition remains `release-2/slices/09-doctrine-guardrails-integration-map.md`.

## 1. Outcome

Slice 9 will make the completed R2 application provable and release-gated. It introduces no new product capability. It binds every shipped dynamic surface to its frontend/backend contract and converts the applicable doctrine guards for Slices 1–8 into deterministic, merge-blocking tests.

The user-visible result is that the existing flows keep working consistently; the delivery result is that a broken honesty, permission, state, async or projection rule cannot pass CI unnoticed.

## 2. Agreed decisions

- Slice 9 is reopened for implementation planning and subsequent implementation when requested.
- No new product feature or redesign belongs in Slice 9.
- Every shipped dynamic surface must be mapped, including Issues, Your Outcome, Grounding Map, History, Reports, Workspace/Settings and collaboration.
- The Integration Map will remain human-readable and gain a machine-validated companion representation.
- Source precedence is Doctrine → Constitution → ratified decisions → implementation contracts → prototype.
- Slice 10 guards remain registered and pending; Slice 9 will not implement Slice 10 capability.
- Applicable Slice 1–8 guards become active only when backed by real deterministic tests.
- Owner-open values remain explicitly pending; they are never guessed or counted as passed.
- Active red guards block merge and release.
- Deployment requires a separate explicit owner instruction after local and staging verification.

## 3. Current baseline

The existing Phase 0 infrastructure is real and will be extended rather than replaced:

| Baseline | Current state |
|---|---:|
| Mapped dynamic surfaces | 58 |
| Registered guards | 60 |
| Active guards | 25 |
| Pending guards | 35 |
| Active pytest selectors | 20 |
| Prototype corrections checked | 6/6 |
| Phase 0 gate tests | Passing |

The 35 pending guards include 17 Slice 10 guards (`GT-34–GT-50`). Those remain pending. The remaining pending guards must be audited against the completed Slice 1–8 application and activated only where the implementation contract is settled.

## 4. Scope

### In scope

- Reconcile the map with every dynamic surface currently shipped by the local R2 application.
- Add stable surface identifiers and machine-readable contract metadata.
- Bind each surface to Reads, Written-by, Changed-by, Async, frontend location, backend handler and guard IDs.
- Add client assertions and server-side twins where the rule concerns persisted state, security or permissions.
- Activate applicable pending guards for Slices 1–8.
- Preserve permanent negative tests for no-write, never-metered, scoped-access and only-reanalysis rules.
- Add async loading/pending/success/error/retry/timeout coverage where the contract is implemented.
- Add complete five-document desktop/mobile E2E regression coverage.
- Make all active guards CI merge-blocking.
- Publish a traceability and release-readiness report.

### Out of scope

- New product features, scoring, workflows or UI screens.
- Implementing Slice 10's load-bearing sensitivity/classification engine.
- Ratifying unresolved owner values.
- Replacing current working Slice 1–8 behavior merely to simplify tests.
- Automatically deploying after the suite passes.
- Renumbering the prototype Workspace/Settings track as canonical Slice 8 without an owner decision.

## 5. Deliverables

1. Updated authoritative Integration Map with every shipped surface.
2. Machine-readable surface contract registry validated by CI.
3. Reconciled guard registry with active, pending and owner-open reasons.
4. Client smoke assertions and backend twins for applicable guards.
5. Permanent negative-test suite for doctrinal boundaries.
6. Five-document desktop/mobile E2E tracer across Slices 1–8.
7. CI merge gate and clear failure output.
8. Final traceability, visual QA and release-readiness report.

## 6. Delivery increments

### Increment 0 — Freeze and characterize the baseline

- Run the existing Phase 0 parser, active guards, web/API suites, lint and production build.
- Record the current 58 surfaces, 60 guards, active/pending counts and selector ownership.
- Capture current failures without changing product behavior.
- List every shipped route/component/API surface added since the original map.

Exit: baseline is reproducible and every later change can be compared with it.

### Increment 1 — Integration Map tracer bullet

- Select one complete path: ranked Issue row → issue act → API → event → reanalysis → History.
- Add stable IDs and full contract fields for every surface in that path.
- Create the machine-readable registry and parser validation.
- Prove the documentation row, frontend surface, endpoint, backend handler and test IDs stay synchronized.

Exit: one end-to-end surface fails CI if any contract binding is missing or stale.

### Increment 2 — Complete the shipped-surface inventory

- Inventory Intake/analysis, Overview/Issues, seven artifacts, Your Outcome, Roll-up, Grounding/Attention maps, collaboration/share/reviewer, Reports/export, History, Workspace/Settings, notifications and advisor surfaces.
- Add missing rows without changing canonical semantics.
- Label non-canonical implementation tracks explicitly instead of silently renumbering them.
- Add zero-unbound and no-duplicate-surface assertions.

Exit: every shipped dynamic surface has Reads, Written-by, Changed-by and Async, plus implementation/test bindings.

### Increment 3 — Strengthen the guard registry and runner

- Extend each guard registration with doctrine source, test type, client assertion, server twin, applicable slice, status and pending reason.
- Validate that active tests exist and are uniquely traceable.
- Validate that pending guards contain an owner-open or Slice 10 reason and no fake passing selector.
- Improve CI output so failures name the guard, doctrine, surface and failing test.

Exit: registry drift, orphan tests and unjustified pending states fail clearly.

### Increment 4 — Activate core state and lifecycle guards

- Cover full-read API independence from presentation freeze (`GT-04`).
- Cover latched unlock semantics (`GT-18`).
- Complete Fast/Deep pass and batching assertions (`GT-23`, `GT-24`).
- Reconfirm only-reanalysis-resolves, comment-never-grounds, typed basis, withdrawal append-only and proposal-resolution guards.
- Add server twins wherever current coverage only checks frontend shape.

Exit: state, lifecycle and reanalysis doctrine is enforced end to end.

### Increment 5 — Activate entitlement and outcome guards

- Cover neutral held/secondary outcome copy (`GT-21`).
- Cover deferred disclosure and frozen-workspace behavior (`GT-22`).
- Reconfirm never-metered reviewer/viewer/record paths and reversible archive.
- Verify entitlement failure and checkout confirmation cannot silently grant capability.

Exit: free/capacity boundaries are enforced without metering trust or access work.

### Increment 6 — Activate collaboration and projection guards

- Enforce scoped external-reviewer access and stale-link 403 behavior.
- Prove Roll-up, Grounding Map and generated projections have no write path.
- Prove comments remain discussion-only.
- Prove cumulative reviewer evidence, attribution, revocation and immutable History behavior.
- Verify viewer/reviewer access remains unmetered.

Exit: collaboration is secure, attributed and incapable of silently changing the read.

### Increment 7 — Activate Reports, export and feedback boundaries

- Enforce D153/advisory disclosure on every memo/export (`GT-16`).
- Enforce low-maturity disclosure without blocking export (`GT-28`).
- Enforce report projection no-write (`GT-31`).
- Enforce feedback sanitization/isolation and telemetry boundaries (`GT-05`, `GT-06`, `GT-15`, `GT-29`, `GT-32`) where the corresponding shipped capability exists.
- Keep a guard pending when its product capability is not shipped or its owner decision remains open.

Exit: reports and side channels cannot modify or misrepresent cognition.

### Increment 8 — Async and failure-state guardrails

- Verify server-authoritative actions show pending and never announce success before confirmation (`GT-A1`).
- Verify advisor/report-generation surfaces show thinking/streaming or a truthful bounded pending state (`GT-A2`).
- Verify every round trip has failure, retry and last-good-state handling (`GT-A3`).
- Avoid hard-coded timing thresholds until the owner ratifies them; test semantic sequencing instead.

Exit: applicable async guards are active; genuinely owner-open timing remains explicitly pending.

### Increment 9 — Full browser and real-document regression

- Use a controlled five-document project containing intent, scope, requirements, constraints, work breakdown, schedule and resources.
- Run Intake → Fast/Deep analysis → issue act → reanalysis → reviewer → share → Grounding Map → Reports → History → Settings.
- Test desktop and mobile, dark and light themes, keyboard/focus, fixed navigation/OSLO rail and horizontal overflow.
- Test owner, collaborator, reviewer and removed-access states.
- Restore temporary invitations, shares and test records after QA.

Exit: Slices 1–8 remain functionally and visually coherent under realistic data.

### Increment 10 — CI gate, review and release evidence

- Make Phase 0 validation and all active guard selectors mandatory in CI.
- Split deterministic fast checks and slower E2E jobs without weakening merge blocking.
- Run AI review, human code review and final manual QA.
- Publish active/pending/failed totals, surface coverage, screenshots and remaining owner decisions.
- Do not deploy until the owner explicitly approves the release candidate.

Exit: a red active guard blocks merge; a green release candidate has complete traceability.

## 7. Trackable work items

| ID | Outcome | Acceptance evidence |
|---|---|---|
| S9-01 | Characterize the existing guardrail baseline | Baseline report records 58 surfaces, 60 guards, 25 active and 35 pending. |
| S9-02 | Create a machine-readable surface registry | One issue lifecycle path is fully bound and CI detects a deliberately removed field. |
| S9-03 | Reconcile all shipped dynamic surfaces | Zero unbound and zero duplicate surfaces. |
| S9-04 | Strengthen registry validation and failure output | Invalid status, missing test, missing twin and unjustified pending states fail clearly. |
| S9-05 | Complete core state/reanalysis twins | Applicable lifecycle guards pass through real API and persistence boundaries. |
| S9-06 | Complete entitlement/outcome twins | Neutral disclosure, capacity and never-metered tests pass. |
| S9-07 | Complete collaboration/security twins | Reviewer 403, no-write projection, comments and attribution tests pass. |
| S9-08 | Complete Reports/feedback twins | D153, projection-only, sanitization and isolation tests pass where applicable. |
| S9-09 | Complete async/failure guardrails | Applicable `GT-A1–A3` tests pass without assuming unratified timings. |
| S9-10 | Add five-document cross-slice E2E | Full owner and reviewer journey passes on desktop and mobile. |
| S9-11 | Make active guardrails merge-blocking | A deliberately failing active guard produces a red CI job. |
| S9-12 | Publish release-readiness evidence | Traceability matrix and final pass/fail/pending report are complete. |

Every work item follows RED → GREEN → REFACTOR. No guard moves from pending to active until its test fails for the wrong implementation and passes for the correct one.

## 8. Test matrix

### Contract and registry

- Missing or duplicate surface.
- Empty Reads/Written-by/Changed-by/Async field.
- Missing frontend/API/backend/test binding.
- Active guard with no existing selector.
- Pending guard with no reason or with a fake selector.
- Contract guard absent from registry or registry guard absent from contract.

### Doctrine and data

- Only `reanalysis.landed` changes resolution or integrity.
- Read API is independent of presentation freeze.
- Comments, notifications and settings preferences change no cognition.
- Roll-up, maps and generated reports are read-only projections.
- Reviewer tokens expose one question/source only; stale or unrelated access returns 403.
- Reading, reviewers and viewers never trigger entitlement evaluation.
- Withdrawals and supersessions append; they never erase prior evidence.
- Integrity uses maturity words, no probability or 0–100 score.

### Async and resilience

- Pending controls disable duplicate submission.
- Errors preserve the last good read and present retry.
- Timeouts do not claim completion.
- Reanalysis batches acts into one governed pass.
- Stale state remains visible until the landed event.

### Browser/E2E

- Five real documents complete Fast and Deep analysis.
- All seven artifacts contain coherent, non-duplicated content.
- Ranked Issues actions and reviewer round trip work.
- Your Outcome, Roll-up, Grounding Map and History agree on state.
- Reports/export remain projections and include required disclosure.
- Workspace, Settings and notifications persist presentation preferences only.
- Desktop/mobile and dark/light layouts have no P0–P2 visual or accessibility defect.

## 9. CI design

The required merge gate runs in this order:

1. Contract/registry parser tests.
2. Active guard unit and negative tests.
3. Active guard API/integration twins.
4. Web unit/integration tests.
5. API suite and Ruff.
6. ESLint, TypeScript and production build.
7. Deterministic desktop/mobile E2E.
8. Traceability completeness check.

Nightly or pre-release jobs may contain longer real-document/browser scenarios, but no active doctrine guard may be relegated to a non-blocking report.

## 10. Risks and controls

| Risk | Control |
|---|---|
| Tests repeat implementation rather than doctrine | Derive assertions from the authoritative guard row and test through public boundaries. |
| A pending guard is mistaken for passing | Report active/pending separately and require a pending reason. |
| Slice 9 accidentally builds Slice 10 | Keep `GT-34–GT-50` registered and pending with explicit Slice 10 ownership. |
| Prototype conflicts with doctrine | Apply the documented source precedence; prototype controls visual reference only. |
| Workspace/Settings numbering conflicts with canonical Slice 8 | Use explicit implementation-track labels and request owner reconciliation before release docs change. |
| E2E tests become flaky | Use deterministic seeds, semantic waits and server-confirmed states; never fixed sleeps as proof. |
| Security is tested only in the UI | Require API/persistence twins for permissions and scope. |
| Real-document QA pollutes live data | Use isolated local/staging projects and clean temporary access artifacts. |
| Existing dirty work is overwritten | Limit edits per increment and review only Slice 9-owned diffs. |
| CI becomes too slow | Split jobs and cache safely, while keeping all active guards merge-blocking. |

## 11. Definition of done

Slice 9 is complete only when:

- Every shipped dynamic surface is mapped with complete contract and async fields.
- The human map and machine registry agree.
- Every applicable Slice 1–8 guard has a real deterministic assertion and required server twin.
- `GT-34–GT-50` remain pending for Slice 10 rather than being falsely passed.
- Every other pending guard has a documented owner-open or capability-not-shipped reason.
- All active guardrails, web/API suites, lint, Ruff, TypeScript and production build pass.
- Five-document desktop/mobile E2E passes across Slices 1–8.
- No unresolved P0, P1 or P2 functional, security, accessibility or prototype-parity defect remains.
- CI demonstrably blocks a deliberately red active guard.
- AI review, human review, manual QA and traceability evidence are recorded.
- The owner reviews the final pending list and explicitly approves deployment.

## 12. Recommended execution order

Execute:

**S9-01 → S9-02 → S9-03 → S9-04 → S9-05/S9-06 → S9-07/S9-08 → S9-09 → S9-10 → S9-11 → S9-12**

This sequence proves the contract and runner first, activates guard clusters only after traceability exists, and leaves full browser regression and release evidence until the deterministic doctrine gate is stable.
