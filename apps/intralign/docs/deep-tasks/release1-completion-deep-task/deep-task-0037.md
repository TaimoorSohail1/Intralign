# DTM-0037 — OSLO Chat backend (ChatExchange + send/trigger; no canonical write)

**Status:** In progress · **Module:** DTM-0037 · **Phase:** Completion · **Contract:** DL-047 (OSLO
Chat CHAT-01…04) + Wave I OBS (`ChatExchange`) · **Depends:** the LLM seam + `submit_trigger`.
**Branch:** `feat/release1-completion`.

## Goal / observable behavior

The frontend OSLO Chat (DTM-0029) gets a backend. New endpoint:
- `POST /v1/projects/{pid}/chat` `{message, context?, intent?}` → a **`ChatExchange`** (non-canonical
  interaction record): the user message + OSLO's response, with context inheritance (issue/
  recommendation/artifact/finding). Intent **Explain/Clarify** = consume existing cognition (read +
  an LLM-phrased explanation via the existing fixture-backed `services/llm_provider` seam). Intent
  **Improve** = **trigger** cognition (`submit_trigger("deep_pass", …)` with the materializer
  injected, like DTM-0032). Emits a non-canonical `ChatExchange` event.
**Critical: Chat writes NO canonical (no AttestedAssertion/CHR/UAR), mutates NO artifact, changes NO
assessment.** It only reads governed objects, produces a non-canonical exchange, and may trigger a
recompute (which the frozen cognition path owns).

## Source docs / constraints

- DL-047 (OSLO Chat: consumes/triggers cognition, generates no canonical, changes no assessment;
  Explain/Clarify/Improve; context inheritance; Critical negative = Chat writing canonical/mutating/
  changing assessment). Wave I OBS (`ChatExchange` events, non-canonical). The OSLO Chat UX spec.
  `code/CONTEXT.md` (OSLO Chat glossary). `code/CLAUDE.md` canonical vocab (`ChatSession`,
  `ChatExchange`).
- Code: `backend/services/llm_provider/` (the adapter + the recorded-fixture pattern ADR-0004 — the
  chat response uses a fixture in CI, gemma live in dev), `backend/orchestration/runner.py`
  (`submit_trigger` for Improve), the read seam (to consume cognition for Explain), the command/DI
  pattern (DTM-0032), `shared/epistemic.py` (add `ChatExchange` / `ChatSession` as non-canonical
  presentation/interaction types — NOT governed cognition; mark clearly), events + gate-5.

## Locked decisions (do not re-derive)

- **Chat writes NO canonical (Critical, negative-proven):** no AttestedAssertion / CHR / UAR write;
  no artifact mutation; no assessment change. Explain/Clarify read + phrase; Improve triggers the
  frozen recompute (the recompute appends CHRs via the frozen retain path — that is the cognition's
  write, NOT the chat's).
- **ChatExchange is non-canonical** — an interaction record (like a notification: platform state).
  **No new migration in this slice** — keep exchanges ephemeral/returned (the frontend DTM-0029
  treats them as ephemeral); if durable chat history is wanted, flag a `chat_session/chat_exchange`
  platform table as a follow-up (do NOT add a migration here without a separate flag).
- **LLM via the existing seam + fixtures** (ADR-0004) — the chat response is fixture-backed in CI
  (zero network), gemma live in dev. Reuse `services/llm_provider`; no new model/routing (DL-069
  unchanged).
- Additive command router; emit the `ChatExchange` event name (gate-5 vocab). `Idempotency-Key`;
  workspace-scoped. No new dependency.

## Owned files / boundaries

- **OWN:** `backend/responsibilities/disclose/chat.py` (or `backend/platform/chat.py`) — the chat
  responder (consume/phrase/trigger, non-canonical) · `backend/api/v1/routers/chat.py` (NEW) +
  include · `backend/api/v1/schemas/` · `shared/epistemic.py` (ChatExchange/ChatSession non-canonical
  types) · DI in `deps.py` · the chat response fixture · `tests/{positive,negative}/...`. Event vocab
  + gate-5 fixtures.
- **READ-ONLY:** the cognition stages + retain (Improve calls submit_trigger; never writes canonical
  directly), the LLM adapter (use, don't change), migrations (none), read seam.

## Packages / refactors — none new.

## Implementation instructions (TDD)

1. Red (pytest, TestClient + overrides + a recorded chat fixture): Explain/Clarify → a ChatExchange
   with a phrased response (fixture), context inherited; Improve → `submit_trigger` called
   (materializer injected) + a ChatExchange; the `ChatExchange` event emitted. **Negatives
   (Critical):** chat writes NO canonical row (assert via a fake store / AST — no
   insert_assertion/chr append/UAR); mutates NO artifact; changes NO assessment (the governed
   projections/CHRs unchanged by an Explain/Clarify); 401/404; idempotency.
2. Build the responder + router; add the ChatExchange types + event + fixture; include in
   `v1/__init__.py`.

## API / data / schema contracts

- Returns a `ChatExchange` (non-canonical). Emits `ChatExchange` (non-canonical). No schema change
  (chat persistence flagged as a follow-up).

## Test plan

- **Positive:** Explain/Clarify (read + phrased response + context); Improve (trigger + exchange);
  event; idempotency; scoping.
- **Negative (Critical):** no canonical write; no artifact mutation; no assessment change; 401/404.
- `.venv/bin/pytest` + ruff + gate-4 + gate-5 (new vocab) green.

## Manual checks (EM)

- POST chat Explain → a response referencing the project's cognition, no canonical row written;
  Improve → a recompute is triggered (a run appears); the assessment only changes via that recompute,
  never by the chat itself.

## Done criteria

- Chat endpoint: Explain/Clarify (consume + phrase) + Improve (trigger), ChatExchange non-canonical,
  Critical no-canonical-write/no-mutation/no-assessment-change negative-proven, LLM via fixtures, no
  new dep/migration, gates green. PR cites DL-047. Ready for DTM-0038.

## Worker report

**Status: Ready for review.** TDD (red → green). DL-047 CHAT-01…04 + Wave I
`IC/OBS-WI-INTERACT`. No new dependency, no migration, no canonical write from chat.

### Endpoint + Explain/Clarify/Improve wiring

- **`POST /v1/projects/{pid}/chat`** `{message, context?, intent?}` →
  `ChatExchange` (HTTP 201). New router `backend/api/v1/routers/chat.py` (additive;
  included in `backend/api/v1/__init__.py` after the DTM-0035 routers). Request
  schema `backend/api/v1/schemas/chat.py` (`ChatRequest{message, intent=explain, context?}`).
- The responder `backend/responsibilities/disclose/chat.py` (`ChatResponder`) is a
  Disclose-class **consumer/trigger**:
  - **Explain / Clarify / Resolve = CONSUME.** The router READS the governed
    projections (`finding/recommendation/confidence/caf/outcome_confidence`) through
    the SELECT-only `ProjectionReader` read seam and hands them to the responder as
    a read-only snapshot; the responder phrases a response over them via the LLM
    seam. These intents **trigger nothing** (`triggered_run is None`).
  - **Improve = TRIGGER.** The responder builds a `TriggerClaim(REANALYSIS,
    information_changed=True, source="oslo_chat_improve")` and calls the EXISTING
    `submit_trigger("deep_pass", claim, materializer=…)` seam (the DTM-0032 pattern,
    DTM-0030 materializer injected). The frozen Deep-Pass recompute owns its CHR
    append — **never the chat**. The exchange records the triggered run id
    (non-canonical bookkeeping).
  - **Context inheritance (CHAT-01):** a launching `{object_type, object_id}`
    (issue/recommendation/artifact/finding/CRR) flows into `ChatExchange.context`.
- DI: `get_chat_responder` added in `backend/api/deps.py` (overridable in tests;
  wired to `LLMProvider()` + `submit_trigger` + materializer in prod). It is
  constructed with **NO** retention/CHR/intake/projection-store handle.

### ChatExchange non-canonical type

- `shared/epistemic.py`: added `ChatExchange` + `ChatSession` + `ChatContext` +
  `ChatIntent`, marked clearly **NOT governed cognition** — an interaction record
  like a notification. New `EpistemicState.NON_CANONICAL = "non-canonical"`; both
  types **pin** `epistemic_state` to it (never `attested-*`, never `derived`).
  `CognitionEntity.is_canonical` updated so a non-canonical record is never
  canonical. `extra='forbid'` makes any assessment/confidence/accepted/attested
  field structurally unrepresentable on a ChatExchange.
- **No migration.** Exchanges are ephemeral (returned to the frontend). A durable
  `chat_session`/`chat_exchange` platform table is FLAGGED as a follow-up (see
  "Chat-persistence flag" below) — not added here.

### LLM-fixture approach (ADR-0004; zero network in CI)

- Phrasing reuses the existing `services/llm_provider` seam via the `advise`
  routing stage (internal gemma primary, DL-069 — **no new model/routing**; DL-048
  §4c Free-tier chat routes to the cheap class). In CI a recorded model-response
  fixture drives it offline (`tests/_fixtures/recorded_model_responses/wi_chat_v0.json`,
  baseline-stamped `gemma4@wi-chat-v0`). The fixture is **never** named
  "replay"/"cassette" (DL-053 reserved). Self-test `tests/replay/test_recorded_chat_fixture.py`
  proves zero provider calls + no provider-SDK import + `live_calls_enabled()` False.

### Event + gate-5

- `chat_exchange` (the "Chat Exchange" OBS-WI-INTERACT event name verbatim, snake
  form) added as `EVENT_NAMES_CHAT` in `events.py` and `EXPECTED_EVENT_NAMES_CHAT`
  in `ci/gate_observability.py` (contract-vocab tuple + `_UNION_NAME_ORDER` + the
  union concatenation). Both gate-5 test fixtures updated
  (`tests/positive/observability/test_gate_observability.py`,
  `tests/negative/observability/test_gate_observability_negative.py`): added the
  CHAT leg to the synthetic `GOOD_EVENTS_PY`, the missing-assignment count
  (18→19), the not-found assertion, and the union-drop search string; added a
  dedicated `chat_exchange`-is-its-own-set verbatim test. The chat event never
  pairs with a CHR append (chat writes no canonical; an Improve's recompute owns
  `cognition_history_record_appended`).

### Critical negatives proven (`tests/negative/api/test_chat_command_negatives.py`)

- **Chat writes NO canonical:** an Explain + an Improve run with the responder
  holding NO write collaborator (asserted absent: `retention_store`/`chr_repo`/
  `intake_store`/`body_store`/`projection_store`) — both succeed (the success IS
  the proof). Source scan of the router + responder finds **no** write-seam token
  (`insert_assertion`/`AttestedAssertion`/`record_acceptance`/`UserAcceptanceRecord`/
  `chr_repo`/`ChrRepository`/`cognition_history_record`/`submit_artifact`/
  `ArtifactBodyStore`/`projection_store`/`.upsert(`).
- **Mutates NO artifact / changes NO assessment:** an Explain leaves the governed
  projection rows + their CHR refs **byte-identical** (deep-copy compare) while
  confirming it DID read them; the read seam is SELECT-only and the responder holds
  no store handle.
- **401 / 404:** unauthenticated ⇒ 401; out-of-workspace project ⇒ 404 (existence
  not leaked) with nothing triggered.
- **Idempotency:** `Idempotency-Key` returns the same exchange and does **not**
  re-trigger (positive suite).

### Exact verify commands + results

```
$ .venv/bin/pytest tests/positive tests/negative -q
721 passed, 65 skipped, 3 warnings in 3.63s
```
(zero network: chat phrasing runs entirely on the recorded fixture — the replay
self-test asserts no provider-SDK import and `live_calls_enabled()` is False.)

```
$ .venv/bin/pytest tests/replay -q
39 passed, 6 skipped in 0.64s

$ .venv/bin/ruff check .
All checks passed!

$ .venv/bin/python ci/gate_invariants.py        # gate-4
[gate-4 epistemic-invariant] PASS: no forbidden tokens, no authority module, no canonical-table mutations in migrations.

$ .venv/bin/python ci/gate_observability.py      # gate-5
[gate-5 observability] PASS: every CHR-append call-site emits 'cognition_history_record_appended', the per-contract A6 vocabularies are pinned verbatim (union consistent), and the replay harness is present.
```

Confirmed: **no new dependency** (pyproject unchanged), **no migration**
(none staged/modified), **no canonical write from chat** (negatives above).

### Chat-persistence flag (follow-up — NOT done here)

`ChatExchange`/`ChatSession` are ephemeral in this slice (returned, not persisted).
If durable chat history is wanted, add a `chat_session` / `chat_exchange` **platform**
(non-canonical) table + repos as a separate slice — it needs a migration (human
approval per code/CLAUDE.md) and was deliberately NOT added here.

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_

## Approved by engineering manager

Status: Approved

Executive summary:
- OSLO Chat backend: `POST /v1/projects/{pid}/chat` → a non-canonical `ChatExchange`. Explain/Clarify/
  Resolve CONSUME (read governed projections + phrase via the fixture-backed LLM seam); Improve
  TRIGGERS (`submit_trigger("deep_pass", …, materializer=…)`). Context inheritance. DL-047 CHAT-01…04
  + Wave I OBS. New `ChatExchange/ChatSession/ChatContext` + `EpistemicState.NON_CANONICAL` in
  shared/epistemic.py.

Verification (EM re-ran): `.venv/bin/pytest` → **721 passed, 65 skipped** (15 new; replay 39 passed;
zero network — chat uses the recorded fixture). ruff clean; gate-4 PASS; gate-5 PASS (`chat_exchange`
vocab pinned). No new dep, no migration.

Critical negatives proven: chat writes NO canonical (exploding-store + absent-collaborator + source
scan; the responder holds no retention/CHR/projection handle — the only `append` is a list builder);
mutates NO artifact; an Explain leaves governed projections + CHR refs byte-identical (no assessment
change); 401/404; idempotency. Improve's recompute appends CHRs via the FROZEN retain path, never the
chat.

Remaining risks / flagged: chat history is ephemeral (no `chat_session/chat_exchange` table) — a
durable platform table is a flagged follow-up (owner-gated migration), not needed for the functional
endpoint. LLM live path uses gemma (DL-069) in dev; fixture in CI (ADR-0004).
