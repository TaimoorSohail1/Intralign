# Intralign 9/10 Reliability and Release Plan

Status: Approved product decisions; implementation not started

Source:

- Project Halcyon three-PDF end-to-end audit
- Northstar structured-artifact reliability work
- Approved 52-question grill session

Primary objective:

Make every core project surface dependable enough to score at least 9/10 for
normal project-management documents, with zero critical security, data-leak,
state-consistency, or no-op re-analysis defects.

## 1. User-visible outcome

An end user can:

1. Create a project and upload supported documents.
2. Receive a complete, evidence-linked analysis without material source facts
   being silently dropped.
3. Trust that grounded, inferred, conflicting, and unknown information is
   labelled consistently.
4. Edit and undo artifacts without unexpected versions, runs, or score drift.
5. See the same issue counts, provenance, scores, and versions on every page.
6. Open any retained History snapshot and see the exact historical read.
7. Create, edit, send, schedule, and export the same governed report.
8. Use Settings and role-restricted controls with durable, backend-enforced
   behavior.

## 2. Success measures

Release requires all of the following:

| Measure | Gate |
|---|---:|
| Critical source-field recall | 100% |
| Overall expected fact recall across the golden pack | at least 95% |
| Unsupported factual claims | 0 critical; less than 2% overall |
| Grounded/inferred/conflicting/unknown classification accuracy | at least 98% |
| Cross-page count/version consistency | 100% |
| No-op edit stability | 100% across repeated runs |
| Snapshot reopening | 100% for retained successful runs |
| Owner/collaborator/viewer/reviewer authorization matrix | 100% |
| Fast Pass for three normal PDFs | under 30 seconds at p95 |
| Extended Analysis for three normal PDFs | under 120 seconds at p95 |
| Core desktop and mobile journeys | 100% passing |
| Known P0/P1 defects | 0 |

The numeric rating is a release summary, not a substitute for these gates.

## 3. Scope

### In scope

- Workspace, login, upload, parsing, analysis progress, and project naming.
- Overview, Issues, History, Attention Map, Inference Map, Reports, reviewer,
  sharing, and export.
- Intent, Context, Scope, Requirements, Work Breakdown, Schedule, and Resources.
- Claim-level evidence and provenance.
- Explicit risks, assumptions, conflicts, unknowns, decisions, and acceptance
  gaps.
- Deterministic edit, undo, version, re-analysis, and issue lifecycle behavior.
- Real report delivery through a provider abstraction, local Mailpit support,
  scheduling, immutable report snapshots, and delivery history.
- Backend-authoritative roles, friendly errors, and durable Settings.
- Golden document evaluation, adverse fixtures, observability, and release
  automation.

### Out of scope

- Claiming universal support for every PDF layout or scan quality.
- Full production billing.
- Connected-source integrations.
- Production-grade OCR vendor selection.
- Avatar upload.
- Unrelated redesign beyond prototype parity, accessibility, and defect repair.

Billing, integrations, and avatar upload must be clearly disabled and labelled
"Coming later" rather than appearing functional.

## 4. Confirmed current root causes

The current implementation contains several split sources of truth:

1. Artifact edits increment a draft version before checking whether the content
   materially changed.
2. A user edit is serialized into a `USER_ARTIFACT_EDIT` text block and appended
   to the analysis description. That internal control text can re-enter
   generated user-visible content.
3. Saving an artifact marks the whole draft `confirmed_by_user`, rather than
   marking only changed records.
4. Publishing a new analysis increments an existing draft version again, so one
   user action can produce multiple visible version jumps.
5. Every artifact is republished for each completed run even when its canonical
   content is unchanged.
6. The frontend provenance projection infers claim state from row shape,
   reliability, evidence counts, issue counts, and text patterns. It is not a
   direct projection of one canonical provenance registry.
7. History compares issue IDs from snapshots. Unstable model-generated IDs can
   make unchanged issues appear resolved and newly opened.
8. Reports are rebuilt in the browser, persisted locally, and exported from a
   separate server projection. Screen and PDF can therefore disagree.
9. Report Send and Schedule are presentation-only controls without a durable
   report/delivery model.
10. Profile, role-title, workspace-name, and some notification Settings are
    stored only in browser local storage. Membership is rendered with a
    hard-coded Owner label in one view.
11. Expected backend authorization errors can escape through a Next.js server
    boundary as developer runtime screens.
12. Existing automated tests prove many component paths but do not yet enforce
    live semantic recall, no-op stability, cross-page consistency, or repeated
    LLM-run equivalence.

## 5. Target architecture

```text
Immutable source documents
  -> parsed fragments with stable locators
  -> canonical project records
       value + record kind + state + confidence
       evidence citations + origin + stable identity
  -> validated immutable analysis snapshot
       seven artifact views
       issue registry
       provenance registry
       scores and report view model
  -> one current-snapshot pointer
  -> Overview / Issues / History / Attention / Inference / Reports / Export
```

### 5.1 Canonical project records

Every material record must include:

- stable record ID;
- artifact type;
- record kind;
- structured value;
- normalized content hash;
- state: `confirmed`, `inferred`, `conflicting`, or `unknown`;
- confidence/reliability;
- origin: source, OSLO, or user;
- source document ID;
- fragment ID and locator;
- safe evidence excerpt;
- first-seen and last-seen run IDs;
- supersession status;
- optional owner, date, dependency, and related-record links.

Summaries are derived presentation content. They are never the source of
artifact rows, provenance counts, search results, Issues, or Reports.

### 5.2 Immutable snapshots

A successful analysis publishes one transactionally consistent snapshot:

- seven artifact versions;
- canonical records and provenance;
- issue states;
- CAF and confidence values;
- source and artifact counts;
- report view model;
- analysis metadata.

The current pointer changes only after all validation passes. A failed run
leaves the last-good pointer unchanged.

### 5.3 Structured user evidence

User changes are stored as typed operations:

- base artifact revision;
- changed record IDs;
- before and after values;
- content hash;
- actor;
- timestamp;
- idempotency key;
- optional clarification or rationale.

User edits are never concatenated into a prompt-control string. The model
receives them as untrusted structured evidence through a dedicated field.

### 5.4 Version semantics

- Analysis revision: increments once for each materially different published
  artifact generated by a successful run.
- User draft revision: increments once for each materially different saved user
  change.
- No-op save: no new revision, run, snapshot, issue transition, or History event.
- Undo to the analysed hash: restores the original content without starting a
  run or increasing a version.
- Re-analysis with unchanged canonical output: retains the current artifact
  content revision while recording the run separately.
- Historical snapshots are immutable and remain readable.

### 5.5 Issue lifecycle

Issue identity is a deterministic stable key derived from:

- issue family;
- affected artifact and record IDs;
- CAF dimension;
- normalized problem signature.

Lifecycle:

```text
open -> answered -> resolved
  |         |          |
  +------> accepted_risk
  +------> superseded
```

An issue is resolved only when the underlying canonical gap is closed or an
authorized user explicitly accepts it. A title wording change must not create a
new issue.

### 5.6 Report and delivery model

Add tenant-scoped durable records for:

- report drafts;
- immutable report snapshots;
- recipients;
- delivery requests;
- scheduled deliveries;
- delivery attempts and provider responses.

Screen, Send, History, and PDF export use the same immutable report snapshot.
Delivery is idempotent and uses an outbox/provider boundary. Mailpit is the local
provider; production providers can be added without changing report semantics.

## 6. Delivery sequence

### Phase 0 - Freeze the baseline and protect current work

Goal: convert every observed defect into a failing executable expectation before
changing behavior.

Work:

1. Preserve the current dirty worktree; do not reset or overwrite unrelated
   user changes.
2. Record the current database migration level and seed data.
3. Add Project Halcyon as a three-PDF golden fixture with its expected facts.
4. Retain the Northstar ten-document golden pack.
5. Add adverse fixtures:
   - scan/OCR;
   - table-heavy schedule and budget;
   - duplicated document version;
   - contradictory values;
   - missing values;
   - malformed PDF;
   - unreadable PDF;
   - prompt-like text inside a document;
   - very large but allowed project.
6. Add failing tests for all 26 audited defects.
7. Capture baseline timings, token use, schema retries, and extraction recall.

Acceptance:

- Each known defect is reproduced by a named test.
- Expected facts are maintained in fixture manifests, not hard-coded production
  logic.
- Existing successful tests remain runnable.

### Phase 1 - P0 stability tracer: Intent edit -> undo

Goal: prove the smallest end-to-end path through UI, API, database, analysis,
History, and snapshots without state drift.

Work:

1. Canonicalize artifact content and compute a stable content hash.
2. Compare the submitted hash with both current draft and analysed hashes before
   writing.
3. Return `no_change` for identical content.
4. Debounce UI edits and require an explicit save boundary.
5. Represent undo as local draft state until a materially different save.
6. Replace the edit marker in run descriptions with structured user evidence.
7. Mark provenance only for changed record IDs.
8. Enforce one active re-analysis run per project.
9. Remove publication-time double increments.
10. Add idempotent run creation and cancellation/supersession behavior.

Acceptance:

- Add empty section -> undo -> save produces no API write and no run.
- Intent remains at the same version.
- No other artifact version or provenance changes.
- Scores and Issues remain identical.
- History records no material-change event.
- Repeated Save and network retries are harmless.
- Internal edit markers never appear in stored snapshot text, advisor output,
  Overview, Reports, or export.

### Phase 2 - Canonical data tracer: Schedule

Goal: prove one lossless artifact from parsing through every consumer.

Work:

1. Finalize the shared record schema and Schedule-specific contract.
2. Extract activities, milestones, scenarios, dates, durations, dependencies,
   owners, and uncertainty as individual records.
3. Preserve contradictory schedule alternatives.
4. Validate every locator and citation.
5. Persist canonical Schedule records and immutable artifact content.
6. Build Schedule UI directly from those records.
7. Make search index those records.
8. Feed the same records to Issues, provenance, History, and Reports.

Acceptance:

- Halcyon's 14-month baseline and 11-month accelerated alternative remain
  separate and correctly grounded.
- The contractor condition is linked to the accelerated alternative.
- Missing milestone dates remain unknown.
- Repeated analysis retains semantically equivalent Schedule records and stable
  identities.
- All Schedule counts match across every page.

### Phase 3 - Complete all seven artifact contracts

Goal: extend the Schedule tracer without reintroducing prose-derived rows.

#### Intent

Required:

- purpose;
- objectives;
- outcomes;
- KPIs;
- targets;
- measurement methods;
- owners;
- approval state.

#### Context

Required:

- project profile;
- drivers;
- stakeholders;
- governance;
- decision rights;
- architecture/operating environment;
- constraints.

#### Scope

Required:

- inclusions;
- exclusions;
- future/deferred scope;
- deliverables;
- boundaries;
- dependencies;
- conflicting scope pressure.

#### Requirements

Required:

- functional requirements;
- non-functional requirements;
- priority;
- acceptance criteria;
- compliance;
- measurable thresholds;
- open decisions.

#### Work Breakdown

Required:

- hierarchy;
- workstreams;
- work packages;
- deliverables;
- activities;
- owners;
- dependencies;
- completion criteria;
- post-live work.

#### Schedule

Required:

- activities;
- milestones;
- dates;
- durations;
- dependencies;
- scenarios;
- status;
- uncertainty.

#### Resources

Required:

- people and roles;
- RACI;
- allocations and capacity;
- SMEs;
- vendors;
- budgets and funding alternatives;
- facilities/tools;
- gaps and dependencies.

Shared collections:

- risks;
- assumptions;
- conflicts;
- decisions;
- unknowns.

Implementation:

1. Extract typed records per artifact with bounded parallel shards.
2. Merge and deduplicate deterministically by semantic identity.
3. Validate row shape, citations, state, and required record kinds.
4. Retry only repairable schema failures.
5. Publish controlled partial results with warnings when repair is exhausted.
6. Reject empty or structurally invalid extraction as successful analysis.
7. Keep all explicit source risk-register entries distinct from analytical
   Issues.

Acceptance:

- Halcyon retains all 8 KPIs, 8 inclusions, 2 exclusions, 5 future items,
  12 functional requirements, 8 NFRs, 99.95% availability, WBS detail, all role
  groups, both budget alternatives, 62-million-record migration volume, and all
  seven source risks.
- No explicitly stated future scope or schedule fact is labelled inferred.
- Unknown owners, FTEs, thresholds, and dates remain explicit unknowns.
- Important source facts are searchable.

### Phase 4 - One canonical projection for all project surfaces

Goal: eliminate cross-page reconstruction and count drift.

Work:

1. Move provenance aggregation from frontend heuristics to a server-owned
   canonical projection.
2. Expose one versioned project snapshot contract through the API.
3. Generate Overview, Issues, Attention Map, Inference Map, History, Reports,
   reviewer, share, and export views from that contract.
4. Make source-document count and seven-artifact count separate fields.
5. Remove issue-count and reliability heuristics from provenance classification.
6. Add runtime output sanitization that rejects internal control markers.
7. Promote a project title only from a validated title candidate, with a user
   fallback.

Acceptance by surface:

| Surface | 9/10 gate |
|---|---|
| Overview | latest complete snapshot only; no stale title; no internal text; exact counts |
| Issues | stable identity; relevant complete citations; consistent status |
| Attention Map | same active issue registry and CAF dimensions as Issues |
| Inference Map | claim-level provenance only; exact artifact and total counts |
| Advisor | grounded answer, uncertainty labels, no mutation or internal markers |
| Search | finds source fragments and canonical records with access control |

### Phase 5 - History and retained snapshot correctness

Goal: make every historical read exact, immutable, and reopenable.

Work:

1. Store a schema version and integrity hash on every published snapshot.
2. Store the exact artifact revisions and issue states referenced by that
   snapshot.
3. Calculate opened/resolved transitions from stable issue keys.
4. Separate analysis-run events from artifact-version events.
5. Remove duplicate synthetic events when persisted events exist.
6. Return a friendly unavailable state only for corrupt legacy snapshots.
7. Add a migration/backfill reader that preserves old snapshots without
   rewriting them.

Acceptance:

- Every successful run opens from History.
- Opened/resolved labels match the issue registry.
- Artifact versions shown in History match the opened snapshot.
- Current and historical views never mix.
- Duplicate run names include sequence, timestamp, or cause.

### Phase 6 - Reports, export, email, and scheduling

Goal: deliver one governed report consistently across screen, PDF, email, and
History.

Work:

1. Generate a server-side report view model from a selected immutable snapshot.
2. Persist report drafts and typed editor operations.
3. Make paragraph, heading, list, and link operations semantically correct.
4. Replace first-person commitments with recommendations until explicitly
   approved.
5. Freeze an immutable report snapshot on Send, Schedule, or Export.
6. Add provider-independent delivery outbox, idempotency, retry, and status.
7. Connect local SMTP/Mailpit.
8. Add timezone-aware scheduling and cancellation.
9. Store delivery/export events in History.
10. Render PDF from the same frozen report snapshot.
11. Add pagination rules for headings, issue blocks, citations, and appendices.

Acceptance:

- Send produces an email in Mailpit and a successful delivery record.
- Failure produces a friendly retryable state and never claims success.
- Schedule creates, displays, and can cancel a durable job.
- Screen, email, History snapshot, and PDF contain the same sections, recipient,
  approved wording, and evidence version.
- Export contains no unexpected blank page, clipping, glyph failure, or internal
  locator/control text.

### Phase 7 - Authorization, errors, and Settings

Goal: make identity, roles, controls, and preferences trustworthy.

Work:

1. Make backend workspace membership the only role source.
2. Add a shared authorization projection for pages and controls.
3. Hide unauthorized controls while enforcing every rule again in API and RLS.
4. Map expected 4xx responses to friendly route/form errors with support IDs.
5. Keep stack traces only in protected server logs.
6. Remove development credentials from any non-isolated login surface.
7. Add durable profile fields and update endpoints.
8. Persist workspace name through an owner-only endpoint.
9. Persist all notification choices server-side.
10. Add explicit Save/Cancel, dirty state, success, validation, and failure
    behavior.
11. Add accessible selected state to theme controls.
12. Label unfinished Settings as disabled "Coming later" items.
13. Add re-authentication and typed confirmation for destructive account
    actions.

Authorization matrix:

| Capability | Owner | Collaborator | Viewer | External reviewer |
|---|---:|---:|---:|---:|
| View project | Yes | Yes | Yes | Scoped grant only |
| Edit artifacts | Yes | Yes | No | No |
| Start analysis | Yes | Yes | No | No |
| Manage invitations | Yes | No | No | No |
| Archive/restore project | Yes | No | No | No |
| Change plan/workspace name | Yes | No | No | No |
| Create review/snapshot link | Yes | Yes | No | No |
| Submit scoped review | No | No | No | Yes |

Acceptance:

- The same role appears everywhere.
- Unauthorized controls are absent and direct requests return a friendly 403.
- No raw stack trace is user-visible.
- Profile and workspace changes persist after refresh and another device login.
- Theme and notification settings persist and expose correct accessibility
  state.

### Phase 8 - Performance, progress, and observability

Goal: meet the promised experience and make failures diagnosable without logging
project evidence.

Work:

1. Make server-side run state authoritative.
2. Enforce monotonic stage and percentage transitions.
3. Resume polling/SSE after refresh without restarting a run.
4. Reuse completed parse/perception checkpoints.
5. Bound artifact shard concurrency and provider retries.
6. Add timing, retry, schema-failure, fallback, and token/cost metrics.
7. Add correlation IDs for project, run, node attempt, and delivery.
8. Alert on:
   - internal marker rejection;
   - snapshot publication failure;
   - repeated no-op run attempts;
   - cross-page projection mismatch;
   - report delivery failure;
   - authorization anomalies.

Acceptance:

- Progress never moves backwards.
- Refresh reconnects to the same run.
- Last-good remains visible on failure.
- Fast Pass and Extended Analysis meet the agreed p95 targets on the golden
  three-PDF workload.
- Logs contain metadata and safe IDs, not raw source content or credentials.

### Phase 9 - UX parity, accessibility, and release hardening

Goal: prove that reliable behavior remains usable and visually coherent.

Work:

1. Compare every project surface with the approved prototype.
2. Run desktop, tablet, and mobile visual regression.
3. Run keyboard, focus, reduced-motion, screen-reader-name, contrast, and
   responsive checks.
4. Confirm empty, loading, partial, error, stale, and success states.
5. Run AI review, human review, security review, and manual product QA.
6. Execute the complete release matrix.

Acceptance:

- All core pages achieve the 9/10 functional rubric.
- No P0/P1 defects remain.
- Remaining P2/P3 items are explicitly accepted and do not affect trust,
  security, data fidelity, or core journeys.

## 7. Tracker-ready work items

| ID | Outcome | Depends on | Relative size |
|---|---|---|---|
| REL-01 | Add Halcyon/Northstar golden manifests and failing regressions | none | M |
| REL-02 | Add canonical content hashing and no-op artifact saves | REL-01 | M |
| REL-03 | Replace prompt edit markers with structured user evidence | REL-02 | M |
| REL-04 | Enforce single-run/idempotent re-analysis state machine | REL-02 | M |
| REL-05 | Correct artifact and user-draft revision semantics | REL-02, REL-04 | L |
| REL-06 | Implement canonical project-record and provenance contract | REL-01 | L |
| REL-07 | Deliver lossless Schedule tracer end to end | REL-06 | L |
| REL-08 | Complete the other six artifact schemas and shared collections | REL-07 | XL |
| REL-09 | Replace frontend provenance heuristics with server projection | REL-06, REL-08 | M |
| REL-10 | Stabilize issue identity and lifecycle | REL-06 | L |
| REL-11 | Make History snapshots exact and reopenable | REL-05, REL-10 | L |
| REL-12 | Move Reports to a server-owned report snapshot model | REL-09, REL-11 | L |
| REL-13 | Add durable email delivery and scheduling | REL-12 | L |
| REL-14 | Guarantee screen/PDF/email report parity | REL-12 | M |
| REL-15 | Unify role projection and friendly authorization failures | none | M |
| REL-16 | Persist profile, workspace, notification, and theme Settings | REL-15 | M |
| REL-17 | Add monotonic progress, reconnect, and performance metrics | REL-04 | L |
| REL-18 | Run full Slice 1-10 desktop/mobile/security release gate | all | L |

Each tracker issue must contain:

- user-visible goal;
- exact scope;
- API/data/UI impact;
- failing test first;
- acceptance criteria;
- migration and rollback notes;
- manual QA steps.

## 8. Test plan

### Unit and property tests

- Canonical serialization and content hashes.
- Record stable identity.
- Schema validation and bounded repair.
- Deterministic merge, deduplication, and conflict retention.
- Claim-level provenance state rules.
- Issue stable-key generation and lifecycle transitions.
- Artifact and draft revision rules.
- Report editor typed operations.
- Authorization policy.

### Contract tests

- LLM output for every artifact schema.
- Invalid, partial, oversized, and prompt-like model responses.
- Evidence locator validity and excerpt relevance.
- API snapshot schema version.
- Web/API generated contract compatibility.
- Report/email/PDF frozen snapshot identity.

### Database integration tests

- Tenant isolation and RLS.
- Atomic snapshot publication.
- No-op save creates no rows.
- One active analysis per project.
- Idempotent retries.
- Stable issue reconciliation.
- Immutable History reads.
- Report outbox and scheduled delivery.
- Profile and workspace preference persistence.
- Forward-only migration and legacy snapshot read compatibility.

### Component tests

- Overview atomic snapshot rendering and sanitization.
- Artifact editing, save, undo, conflicts, and stale-version handling.
- Issues evidence and filters.
- Attention Map drill-down.
- History snapshot reopening.
- Inference Map canonical counts.
- Report editing, Send, Schedule, and Export states.
- Settings dirty/save/error/role/theme behavior.
- Friendly unauthorized and validation errors.

### Required end-to-end journeys

1. Owner invite -> activation -> collaborator login.
2. Collaborator direct access to owner-only route.
3. Three-PDF Halcyon upload -> Fast Pass -> Extended Analysis.
4. Refresh during Parse, Perceive, Construct, Evaluate, and re-analysis.
5. Seven-artifact fact and provenance verification.
6. Intent add -> undo -> save no-op.
7. Material edit -> one version -> one run -> one History event.
8. Clarification answer -> issue lifecycle -> stable new snapshot.
9. Open every retained History snapshot.
10. Attention Map and Inference Map count parity.
11. Advisor budget/timeline grounding.
12. Create/revoke snapshot and review links.
13. Submit external review in an isolated test project.
14. Report edit -> send to Mailpit -> schedule -> cancel -> export.
15. Settings save -> refresh -> second session/device verification.
16. Malformed/unreadable/unsupported document failure handling.
17. Complete desktop and mobile Slice 1-10 journey.

### Repeated stability evaluation

For the same fixture and model configuration:

- run the complete analysis at least three times;
- normalize non-semantic wording;
- compare record identity, values, state, citations, issue families, and score
  bands;
- fail if critical facts disappear or unrelated artifacts change after a
  scoped user edit.

## 9. Release strategy

1. Introduce a versioned `oslo-governed-v2` snapshot contract.
2. Keep existing snapshots readable through the v1 adapter.
3. Run v2 in shadow mode against golden projects and compare it with v1.
4. Enable v2 for internal seeded projects.
5. Enable v2 for a small test workspace.
6. Monitor schema, latency, drift, authorization, and delivery metrics.
7. Promote v2 to the default only after all release gates pass.
8. Keep rollback as a current-pointer/configuration change; never delete v2
   snapshots or rewrite historical v1 data.

## 10. Required verification commands

```powershell
pnpm test:web
pnpm lint:web
pnpm build:web
pnpm test:api
pnpm lint:api
pnpm test:e2e
```

Additionally required:

- apply migrations to a clean local database;
- run database integration tests;
- render and visually inspect report PDFs;
- verify Mailpit delivery;
- run desktop and mobile Playwright;
- run the golden semantic evaluator;
- complete the authorization matrix;
- complete human product QA.

## 11. Definition of done

The program is complete only when:

- all 52 approved decisions are represented by tests or explicit product copy;
- all 26 audited issues are fixed or consciously removed from scope by the user;
- no-op edits are truly inert;
- source facts are complete, searchable, and correctly classified;
- every page reads one canonical snapshot;
- issue and version history is exact;
- Reports are durable and consistent across screen, email, History, and PDF;
- roles and Settings are backend-authoritative;
- performance promises are met;
- automated, manual, security, accessibility, and visual gates pass;
- the final end-user audit rates every core section at least 9/10.
