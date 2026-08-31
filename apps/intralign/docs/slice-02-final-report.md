# OSLO Slice 2 implementation and verification report

Date: 23 July 2026
Branch: `feature/slice-2`

## Delivered

- Prototype-aligned Intake with description, five templates, sample project and supported-document
  selection.
- Authenticated multipart upload of the actual document bytes.
- Immutable local object storage for development, SHA-256 deduplication, MIME sniffing and a
  10 MB upload limit.
- Page-aware PDF extraction plus UTF-8 TXT, Markdown and CSV extraction.
- Durable source-document and source-fragment records with page/character evidence locators.
- Analysis runs linked to immutable document IDs rather than trusting filenames.
- Authenticated, idempotent analysis-run API.
- Twelve-node LangGraph workflow:
  Submit → Validate → Ingest → Perceive → Retrieve → Construct → Checkpoint → Evaluate →
  Validate result → Publish → Project to browser → Extended transition.
- Controlled three-call Agent Harness with live OpenAI execution for Perceive, Construct and
  Evaluate, plus a deterministic test/fallback provider.
- Versioned prompts, strict Pydantic structured-output contracts, evidence-reference validation,
  bounded context selection, phase-specific models and output-token limits.
- One bounded retry for transient provider/schema failures, safe error codes, consistent Initial
  fallback and last-good preservation for Extended failures.
- Provider/model/prompt version, response ID, token usage, duration, attempt count and execution
  mode persisted for every Agent Harness node without storing credentials.
- PostgreSQL persistence for runs, attempts, checkpoints, ordered events, immutable snapshots,
  seven artifact versions, stable issues, observations and current-result pointers.
- Tenant membership authorization and RLS policies.
- SSE progress with event IDs, replay through `Last-Event-ID`, heartbeats and safe reconnect.
- Initial provisional publication followed by automatic Extended Analysis and atomic supersession.
- Last-good preservation when Extended Analysis fails.
- Retry from the last successful checkpoint after Perceive, Construct or Evaluate failure.
- Professional responsive Overview with confidence, attention, progress, seven artifacts, issue
  details, first-use orientation, replay and advisory OSLO chat shell.

## Verification

| Suite | Result |
|---|---|
| FastAPI unit/API/integration | 77 passed |
| PostgreSQL Perceive failure + refresh + retry | Passed |
| PostgreSQL Construct failure + refresh + retry | Passed |
| PostgreSQL Evaluate failure + refresh + retry | Passed |
| Last-good pointer after Extended failure | Passed |
| Vitest component tests | 9 passed |
| ESLint | Passed |
| Ruff | Passed |
| Next.js production build and type check | Passed |
| Playwright full Slice 1 + Slice 2 suite | 15 passed |
| Desktop, tablet and mobile Slice 2 journey | Passed |
| Reduced motion and keyboard journey | Passed |
| Design QA | Passed |
| Exact 81-page stress PDF upload and extraction | Passed: 72,321 bytes, 82 fragments, pages 1-81 |
| Stress PDF Initial Analysis | Passed: 22/100, Low confidence, 8 evidence-linked issues |
| Stress PDF Extended Analysis | Passed: current snapshot, 22/100, 8 evidence-linked issues |
| Refresh during stress analysis | Passed: resumed from durable run state |
| Live OpenAI Fast Pass tracer | Passed: all 3 model calls and exactly 7 artifacts |
| Live OpenAI Extended tracer | Passed: all 3 model calls and exactly 7 artifacts |
| Live OpenAI database publication | Passed: provisional then current snapshot; 6 call records persisted |
| Accepted-invitation harmless replay | Passed: existing member returns to Intake without duplicate membership |

## Failure guarantees verified

- No partial assessment is published.
- Every completed node creates a durable checkpoint.
- Refresh reads persisted run state instead of restarting the workflow.
- SSE reconnect replays only events after the last acknowledged sequence.
- A retry reuses completed Perceive/Construct output and resumes at the failed node.
- A failed Extended run never replaces the current provisional/last-good snapshot.
- Publication writes the snapshot, artifact versions, issues and project pointer atomically.
- Re-uploading identical bytes returns the existing immutable source document without duplicate
  rows or fragments.
- Invalid, unsupported, empty and oversized documents are rejected before analysis.

## Supplied stress-PDF results

The live OpenAI Fast Pass detected all expected findings:

1. Conflicting 6, 9 and 12-month timelines.
2. Conflicting $1.8M, $2.1M and $2.5M budgets.
3. Ambiguous mobile/HR/inventory scope.
4. Missing success metrics.
5. Deployment dependency on unresolved regulatory approval.
6. Conflicting resource plans.
7. Unresolved vendor selection.
8. Unknown migration volume.

The completed live Extended run published a current snapshot with Very Low confidence, Low
Clarity, Moderate Alignment and Very Low Feasibility. It produced ten evidence-linked issues,
including the expected conflicts above; Extended may split or combine related findings differently
from Fast Pass while preserving evidence traceability.

The successful live Extended Agent Harness calls recorded:

| Node | Model input | Model output | Provider duration |
|---|---:|---:|---:|
| Perceive | 8,533 tokens | 1,479 tokens | 22.25 s |
| Construct | 9,215 tokens | 2,147 tokens | 17.22 s |
| Evaluate | 11,578 tokens | 2,392 tokens | 20.38 s |

## Global ERP live-provider regression

The supplied 21-page Global ERP plan exposed output truncation in the original Fast Pass token
envelope. Perceive first exhausted its 1,000-token response limit; after that correction, Construct
exhausted its 2,000-token limit. Both cases safely activated the deterministic fallback, but made
later stages appear to finish instantly.

The fix keeps the context envelope bounded while allowing complete structured contracts:
Perceive now allows 2,500 Fast Pass / 3,000 Extended output tokens, Construct 4,000, and Evaluate
3,500 Fast Pass / 4,000 Extended. Prompts also require concise, consolidated findings. Truncated
JSON is now classified as `OPENAI_OUTPUT_LIMIT` instead of a generic schema failure.

The final fresh run completed all twelve stages twice:

| Run | Perceive | Construct | Evaluate | Published state |
|---|---|---|---|---|
| Fast Pass | Luna, 10.38 s, 1,726 out | Luna, 10.19 s, 1,860 out | Luna, 12.09 s, 1,613 out | Provisional |
| Extended | Terra, 12.48 s, 2,105 out | Terra, 11.25 s, 1,627 out | Terra, 14.44 s, 1,644 out | Current |

There was no fallback in either final run. The current pointer moved from the immutable
Provisional snapshot to the Extended snapshot. The final Overview has exactly seven artifacts and
seven evidence-grounded issues covering contradictory scope, schedule, funding/capacity, vendor
selection, migration uncertainty, regulatory approval and missing success metrics.

## Project Atlas live-provider regression

The supplied 21-page Project Atlas healthcare plan completed Fast Pass in 37.07 seconds. All
twelve workflow nodes completed and all three Agent Harness nodes used live `gpt-5.6-luna`
responses:

| Fast Pass node | Input | Output | Provider duration |
|---|---:|---:|---:|
| Perceive | 3,593 tokens | 1,809 tokens | 10.53 s |
| Construct | 4,791 tokens | 1,694 tokens | 10.69 s |
| Evaluate | 6,737 tokens | 2,048 tokens | 14.08 s |

The first Extended Construct response altered one valid evidence locator by one page number. The
evidence gate correctly rejected that response, published nothing incomplete and preserved the
Provisional result. Construct and Evaluate now receive an explicit allowlist and are instructed to
copy locators exactly. The regression test proves that both prompts carry this contract.

After retry from the last completed checkpoint, Extended completed without deterministic fallback:

| Extended node | Input | Output | Provider duration |
|---|---:|---:|---:|
| Perceive | 4,634 tokens | 1,493 tokens | 9.27 s |
| Construct | 6,175 tokens | 1,352 tokens | 10.80 s |
| Evaluate | 7,769 tokens | 1,683 tokens | 14.67 s |

The current pointer now targets the immutable Extended snapshot. It reports 58/100 Moderate
confidence, Moderate Clarity, Low Alignment and Low Feasibility. Its seven evidence-linked issues
cover the claims-phase conflict, 10/12/14-month schedules, 10/6-developer capacity conflict,
USD 14.8M/13.9M/12.5M funding conflict, incomplete migration volume, unapproved success
thresholds, unresolved vendor selection, pending e-prescribing approval and missing measurable
operating conditions. Each issue includes why it matters, a next action and a clarification
question.

The actual token use remained well below the configured output caps. Increasing token limits would
not have corrected the failed locator and would only increase latency and cost.

## Project Orion live-provider regression

The supplied 9-page Project Orion supply-chain plan completed a fresh Fast Pass and automatic
Extended Analysis. Each run completed all twelve workflow phases once, published exactly seven
artifacts and used only live OpenAI primary execution for the three Agent Harness nodes.

| Run and node | Model | Input | Output | Provider duration |
|---|---|---:|---:|---:|
| Fast Pass - Perceive | `gpt-5.6-luna` | 3,394 | 1,351 | 8.81 s |
| Fast Pass - Construct | `gpt-5.6-luna` | 4,744 | 1,187 | 8.92 s |
| Fast Pass - Evaluate | `gpt-5.6-luna` | 6,160 | 1,791 | 13.03 s |
| Extended - Perceive | `gpt-5.6-terra` | 8,623 | 2,318 | 12.44 s |
| Extended - Construct | `gpt-5.6-terra` | 10,980 | 1,479 | 9.38 s |
| Extended - Evaluate | `gpt-5.6-terra` | 12,745 | 2,097 | 18.41 s |

Fast Pass completed in 32.48 seconds and published Provisional. Extended completed in 41.94
seconds and atomically became Current. All six calls used `execution_mode=primary`, with no
fallback, retry, provider error or output-limit event.

The Current result reports 52/100 Moderate confidence with Moderate Clarity, Alignment and
Feasibility. Its seven issues correctly cover the conditional transportation-optimization scope,
untestable requirements, unvalidated migration volumes and sequence, conflicting 15/13-month
schedule options, conflicting USD 22.4M/21.1M/19.8M funding positions, missing resource capacity,
unresolved dependencies and decisions, and unapproved KPI thresholds. Every issue reference
matches one of the 26 persisted Orion evidence fragments; every issue also includes a supported
explanation, action and clarification question.

## Runtime mode

Local development now uses `ANALYSIS_HARNESS=auto`: a securely configured `OPENAI_API_KEY`
activates the live provider; otherwise the deterministic provider is used. Fast Pass uses
`gpt-5.6-luna` and Extended uses `gpt-5.6-terra` by default. Tests explicitly use deterministic
mode so they are repeatable and do not spend API credits.

The key remains only in the ignored API environment file. It is not committed, logged, returned to
the browser or persisted in analysis metadata.

## Project Advisor and new-project navigation

The previously static OSLO Project Advisor is now an authenticated, project-scoped OpenAI
interaction. A question is sent through a server-only Next.js route to FastAPI. FastAPI resolves
the tenant-authorized Current Overview snapshot, sends only that bounded context to OpenAI and
requires a strict typed answer with no more than three follow-up questions. The prompt treats the
question and snapshot as untrusted data, forbids invented project facts and keeps the final
decision with the user. Provider failures return a safe retry message without changing project
state.

Overview now also includes a `New project` action. It creates a fresh project in the user's current
workspace and routes directly to that project's Intake. An in-flight guard prevents duplicate
creation from repeated clicks, and existing projects remain unchanged and accessible.

Verification completed on 23 July 2026:

- 81 API tests passed; Ruff passed.
- 12 web tests passed; ESLint and the Next.js production build passed.
- A live Orion advisor request returned `200` in 8.32 seconds with project-specific evidence,
  gaps and recommendations.
- An unauthenticated advisor request returned `401`; an inaccessible project returned `404`.
- Browser verification confirmed quick-prompt chat, live answer rendering, fresh-project Intake
  navigation, preservation of the previous Overview and mobile availability of both controls.

## Extended evidence-reference recovery

The previously stuck Extended run
`c5c3100a-b440-4564-9852-793ec7889205` was confirmed failed at Perceive because the model changed
an immutable evidence locator. The safety gate correctly preserved the Provisional snapshot, but
the Overview incorrectly continued to label the run as running.

The recovery path now:

- gives Perceive, Construct and Evaluate one bounded citation-only correction attempt;
- supplies the exact immutable locator allowlist and the invalid locator list;
- never guesses, normalizes or silently rewrites a reference;
- fails closed and preserves the last-good snapshot if the corrected response is still invalid;
- exposes the latest Extended status on the Overview API; and
- shows a safe failed state with a user-controlled Retry action instead of an endless spinner.

The persisted failed run was retried after deployment of the fix. It completed all twelve phases
in approximately 41 seconds and atomically replaced Provisional with Current:

| Extended node | Provider/model | Input | Output | Provider duration |
|---|---|---:|---:|---:|
| Perceive | OpenAI / `gpt-5.6-terra` | 7,248 | 1,664 | 12.03 s |
| Construct | OpenAI / `gpt-5.6-terra` | 8,948 | 1,327 | 9.59 s |
| Evaluate | OpenAI / `gpt-5.6-terra` | 10,555 | 1,638 | 16.49 s |

All three calls used primary live OpenAI execution with no deterministic fallback. The final
Current snapshot contains exactly seven artifacts and six issues. Every artifact and issue
reference matches one of the 22 persisted allowed evidence locators.

Final regression gates after this fix:

- 83 API tests passed; Ruff passed.
- 13 web tests passed; ESLint passed.
- TypeScript and the Next.js production build passed.

## Golden-prototype UI parity and clarification loop

The Slice 2 experience now follows the golden HTML prototype from analysis through decision
support:

- Fast Pass uses the centered scanner, four user-facing stages, live completed-step trace and
  quiet timing guidance.
- Overview uses the compact Confidence, Start here, Progress and More hierarchy with a persistent,
  collapsible OSLO advisor rail.
- First-use orientation matches the four-part Understanding / Judgement / Decision / Oversight
  contract and can be replayed from the account menu.
- Timeline and Attention open the matrix view; selecting a populated cell replaces the advisor
  with an evidence-linked issue panel.
- “Answer the first” opens the tied clarification request. Submitting an answer records durable,
  tenant-scoped evidence and starts an Extended re-analysis while the current last-good Overview
  remains visible.
- Mobile and tablet layouts preserve the same information architecture without clipping the
  orientation or issue controls.

Final verification for this increment:

- 84 API tests passed.
- 14 web unit/component tests passed.
- 3 Slice 2 Playwright journeys passed across desktop, tablet and mobile.
- ESLint, Ruff and the Next.js production build passed.
- Visual QA compared loading, orientation, Overview, Attention and issue states against the
  golden prototype; no P0/P1/P2 visual defects remain.

## Scope boundary

This is the complete local tracer implementation agreed for Slice 2. PDF, TXT, Markdown and CSV
content now flows into governed evidence inputs. OCR for scanned PDFs, DOCX/PPTX/XLSX parsers,
production cloud object storage and embeddings/semantic retrieval remain explicit
production-hardening increments.
