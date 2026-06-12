# DTM-0006 — OBS-WA-00R: events, audit, two-axis replay; CI gate-5 goes real

**Status:** Approved · **Module:** DTM-0006 · **Phase:** II (Wave A) · **Contract:** **IC-WA-00R / OBS-WA-00R** · **Depends:** DTM-0005

## Goal / observable behavior

Every backbone action emits its OBS-WA-00R event (stale detected · reanalysis triggered ·
recompute started/completed/failed · CHR appended · state transition) with full audit
fields (trigger source, inputs/versions, emissions, outcome). A replay harness reproduces:
(a) any CHR **record-exact**, and (b) the trigger→emissions lineage of any recompute.
CI gate-5 upgrades from scaffold to a real check: a governed emission without its event
fails the build.

## Source docs / constraints

- OBS-WA-00R C2 (events), C3 (audit), C5 (replay); Observability Governance Deliverables 3–4 (two-axis replay; tiered determinism — everything here is record/rule tier = exact).
- DL-054 condition 1: gate-5 satisfied by governed-output events + CHR recording provider/model/version + **LangSmith run id linkage**.
- Event names/payload envelope: `20_handoff/interfaces/RELEASE_1_EVENT_MODEL_SPECIFICATION_V1.md` — use verbatim; invent no event types.

## Locked decisions

- Events through `services/observability/` (emitter seam from DTM-0005), structured-logged + OTel span events; external delivery NOT built (open NFR).
- Replay harness in `tests/replay/` as reusable fixtures (it's the determinism harness the phase plans say engineering writes — code, not docs).
- Gate-5 check: static+test — every `CHR append` call site paired with an emit; replay tests must exist and pass.
- LangSmith: record `run_id` into CHR when tracing enabled; absent run_id allowed in dev (config-only, decisions A3).

## Owned files

- `backend/services/observability/**`, the emit call-sites inside `orchestration/` + `responsibilities/{adapt,perceive,retain}` (additive only), `tests/replay/**`, `code/ci/` gate-5 script, `tests/{positive,negative}/observability/**`.
- Read-only: everything else.

## Packages / refactors

- None new. No refactors.

## Implementation instructions (TDD)

1. Red: event-per-action tests (each backbone action → exactly its C2 event, correct audit fields); record-exact CHR replay test; lineage replay test; negative — suppressed event fails gate-5 script.
2. Green: emitter + call-sites + replay fixtures + gate-5 script upgrade.

## Test plan

- Positive: full C2 event set observed across one recompute cycle; replay reproduces CHR byte-exact (REPLAY_RECORD_TOLERANCE=0); lineage reconstruction matches.
- Negative: missing emit detected by gate-5; replay mismatch reported as Critical-class failure; no event type outside the Event Model.

## Done criteria

- C2/C3/C5 demonstrably covered with named tests; gate-5 real and proven red-able; PR cites `IC-WA-00R`; Phase II Wave A 00R candidate-complete for owner review.

## Worker report

**Worker:** DTM-0006 (2026-06-12) · **Contract cited:** IC-WA-00R / OBS-WA-00R · baseline 162 → 206 passed (no regressions).

### What was built

**C2 — observable event transport** (`backend/services/observability/emitters.py`, NEW)
- `ObservedEventEmitter(inner)` — decorator over the DTM-0005 `EventEmitter` protocol (CollectingEventEmitter untouched). Per accepted A6 event: (1) one structured-JSON log line via stdlib `logging` (logger `oslo.observability.events`), (2) an OTel **span event** on the current span when one is recording — clean no-op otherwise (same graceful-degradation rule as `setup.py`; transport failures degrade to warnings, never block the backbone). Validation order: inner emitter first, so a non-A6 name raises before anything is observed.
- `ObservedEventEmitter.wrap()` is idempotent; `__getattr__` delegates `.events`/`.names` so collecting consumers are unaffected.
- Wired at the two construction sites in `runner.py` (flagged below). `graphs/deep_pass.py` NOT touched (runner passes the already-wrapped seam into the factory).

**C3 — audit completeness** (`backend/services/observability/audit.py`, NEW)
- `audit_view(events, repo, run_id=None) -> RecomputeAuditRecord`: assembles, from a run's collected A6 events + the CHR repo: trigger type + **trigger source**, per-emission **inputs/versions consumed** (`input_attestation_version` + full `model_or_rule_version` incl. provider/model + optional `langsmith_run_id`), **emissions produced → appended CHR ids**, state-transition trail, **outcome** (completed/failed + failure info). Append-not-overwrite auditable: each `supersedes_chr_id` is re-resolved (`prior_intact`). Unreconstructable streams raise `AuditAssemblyError` (never a silent partial record).

**DL-054 cond.1 — LangSmith linkage** (`backend/services/observability/langsmith_linkage.py`, NEW)
- `langsmith_run_linkage(run_id)` → `{"langsmith_run_id": run_id}` iff `LANGSMITH_TRACING` (canonical name, `.env.example`) is truthy AND a run id exists; `{}` otherwise — dev-without-LangSmith allowed (decisions A3). Merged additively into `model_or_rule_version` by `retain_stage` (flagged edit below); declared spec values win on collision.

**C5 — two-axis replay harness** (`tests/replay/harness.py` + `conftest.py`, NEW — reusable fixtures; this IS the determinism harness)
- Record-exact axis: `canonical_chr_bytes` / `snapshot_chr` / `replay_chr_record(chr_id, repo, snapshot)` — re-read + **byte-compare** canonical JSON; `record_tolerance()` reads `REPLAY_RECORD_TOLERANCE` (default 0) and REJECTS any non-zero value (record tier is exact). Any diff → `ReplayMismatchError` with `severity="Critical"` naming the differing field(s).
- Trigger/lineage axis: `reconstruct_recompute(events, repo)` — rebuilds trigger → emissions → appended CHR ids → outcome (via `audit_view`) and verifies every supersession chain resolves through `repo.lineage_chain`; unresolvable link → Critical `ReplayMismatchError` naming `supersedes_chr_id`.

**Gate-5 real** (`ci/gate_observability.py`, NEW; workflow + README updated)
- (a) **Append↔event pairing** — documented approach: AST scan of `backend/**/*.py`; a module is a CHR-append call-site iff it contains a `*.append(...)` call whose receiver mentions `chr_repo`/`ChrRepository` (plain `list.append` never matches) or a direct `retain_stage(...)` call; `retain/repository.py` (the storage layer) excluded. A flagged module must contain an ACTUAL `*.emit("cognition_history_record_appended", ...)` **call** — AST-checked; docstring/comment mentions do NOT count (this was upgraded after live red-proof: the first text-level version was satisfied by the stages.py docstring — caught and fixed, negative test added).
- (b) **A6 vocabulary pinned** — `EVENT_NAMES` in `events.py` must equal the seven IC-WA-00R names verbatim, in order, as a static literal (rename/extra/missing/non-literal all fail).
- (c) **Replay harness present** — `tests/replay/` exists with ≥1 `test_*.py`.
- `.github/workflows/app-ci.yml` gate-5 step (only that step changed): scaffold `test -f` replaced by `python -m ci.gate_observability` + `python -m pytest tests/replay` (live axes skip without Supabase; pure tamper axes always run; empty/missing suite fails via pytest exit 4/5). `ci/README.md`: gate-5 row, run-by-hand block, red-proof item 5 rewritten.

### C2/C3/C5 → test traceability

| Contract | Test(s) |
|---|---|
| C2 transport (structured log + span event, no-op degrade) | `tests/positive/observability/test_observed_emitter.py` (5) · `tests/negative/observability/test_observed_emitter_negative.py` (3: unknown name rejected + not observed; OTel failure degrades; logging failure degrades) |
| C2 coverage end-to-end (== A6 7 names; extends DTM-0005, no duplication) | `tests/positive/observability/test_c2_event_coverage.py` — EXACT full event sequence of one successful run (8 events) and one failed run (7 events, `last_known_good_retained`), + vocabulary pin |
| C3 audit | `tests/positive/observability/test_audit_view.py` — live real run: all C3 fields asserted (trigger source, attestation version, provider/model, `langsmith_run_id`, chr ids, transitions, outcome); failed-run audit · `tests/negative/observability/test_audit_view_negative.py` (5 refusal modes) |
| DL-054 cond.1 linkage | `tests/positive/observability/test_langsmith_linkage.py` (3: enabled→key present inside model_or_rule_version; disabled/absent→no key, CHR still valid) |
| C5 record-exact | `tests/replay/test_record_exact_replay.py` — live append→snapshot→re-read byte-exact; tolerance default 0; **negative tamper** (snapshot mutated, DB untouched) → Critical naming `output_payload`; non-zero tolerance rejected; missing record fails |
| C5 trigger/lineage | `tests/replay/test_lineage_replay.py` — live 2-run chain reconstructed exactly (incl. lineage `[new, prior]`, `prior_intact`); failed-run reconstruction; pure broken-lineage → Critical |
| Gate-5 | `tests/positive/observability/test_gate_observability.py` (real tree passes; detection not vacuous) · `tests/negative/observability/test_gate_observability_negative.py` (10: unpaired append, docstring-only mention, unpaired retain_stage, missing/empty replay dir, renamed/extra/missing/non-literal vocabulary) |

### Commands run + real results (venv `/tmp/oslo-ci-venv`; Supabase live at 127.0.0.1:54331/54332)

```text
python -m pytest -q                                       # BEFORE changes: 162 passed (baseline confirmed)
ruff check .                                              # All checks passed!
python -m ci.gate_invariants                              # [gate-4] PASS
python -m ci.gate_observability                           # [gate-5] PASS (real tree)
python -m pytest tests/positive tests/negative tests/replay -q   # 206 passed (live; 162 baseline intact + 44 new)
env -u SUPABASE_* python -m pytest tests/replay -q        # 5 passed, 3 skipped (CI mode: pure axes run, live skip)
env -u SUPABASE_* python -m pytest tests/positive tests/negative -q  # 153 passed, 45 skipped
yaml.safe_load(app-ci.yml)                                # valid YAML
```

Gate-5 red-proof, executed live on a throwaway copy of the tree (`--code-root /tmp/gate5-redproof`):

```text
(a) emit call removed from stages.py        → FAIL exit 1: "CHR append call-site without a paired ... emit CALL"
(b) EVENT_NAMES recompute_failed→_errored   → FAIL exit 1: "EVENT_NAMES != the IC-WA-00R A6 vocabulary"
(c) tests/replay removed                    → FAIL exit 1: "tests/replay/: missing"
```

(Red-proof (a) initially PASSED against the first text-level check because the stages.py docstring names the event — check upgraded to AST emit-call detection, regression-tested in `test_docstring_mention_does_not_satisfy_the_pairing`.)

### Additive edits OUTSIDE services/observability (flagged, exact)

1. **`backend/orchestration/runner.py`** (transport wiring — anticipated by task A "wrap at construction sites"):
   - +1 import: `from backend.services.observability.emitters import ObservedEventEmitter`
   - `run()` line ~100 and `submit_trigger()` line ~166: `seam = emitter if ... else CollectingEventEmitter()` → `seam = ObservedEventEmitter.wrap(emitter if ... else CollectingEventEmitter())` (+ comment). Behavior-preserving for all existing callers (wrap delegates + is idempotent); proven by the untouched DTM-0005 suites staying green.
2. **`backend/orchestration/stages.py`** (run-id linkage — the anticipated emission-spec merge):
   - +1 import: `from backend.services.observability.langsmith_linkage import langsmith_run_linkage`
   - `retain_stage`: +`linkage = langsmith_run_linkage(state.run_id)` before the loop; inside the loop, when linkage non-empty, spec copied with `model_or_rule_version = {**linkage, **spec.get("model_or_rule_version", {})}` (declared values win; original spec dict not mutated).
3. No edits to `graphs/deep_pass.py`, retain models/repository, migrations, api/, adapt/, perceive/. `events.py`/`setup.py` untouched.

### Notes / open items for review

- Gate-5 step runs `pytest tests/replay` in CI where live axes skip (no Supabase in CI yet) — the pure tamper-detection axes still execute; live axes run locally/staging. `tests/replay` was deliberately NOT added to `pyproject` `testpaths` (file not owned by this task); the workflow and the report commands invoke it explicitly.
- `test_c2_list_is_exactly_the_seven_a6_names` sits in a live-skipped module; the same pin is enforced unconditionally by gate-5 check (b), so CI coverage is not lost.
- External event delivery (queue/webhook) intentionally NOT built — open NFR per locked decision.
- The local shell exporting `LANGSMITH_TRACING=true` without a valid key produces harmless 401 ingest warnings from langgraph's own tracer during live runs — pre-existing behavior, unrelated to this change.

### FIX-1 report

- **Problem:** tests monkeypatching `LANGSMITH_TRACING=true` (and graph-invoking tests after env contamination) let langchain/langgraph's global tracer POST real run payloads to `https://api.smith.langchain.com` (repeated 401 "Failed to multipart ingest runs" spam). Tests must never ship data externally.
- **Fix:** new root `tests/conftest.py` with an autouse **session** fixture `_langsmith_offline` setting `LANGSMITH_ENDPOINT=http://127.0.0.1:9`, `LANGCHAIN_ENDPOINT=http://127.0.0.1:9`, `LANGCHAIN_TRACING_V2=false` — any accidental tracer fails instantly and locally (`setdefault` was insufficient against monkeypatched flags). Verified `backend/services/observability/langsmith_linkage.py` reads only `LANGSMITH_TRACING` + run id, so DTM-0006 linkage tests are unaffected.
- **Verification:** `pytest tests/positive tests/negative tests/replay -q` → `206 passed, 18 warnings in 1.18s`; zero `Failed to multipart ingest` / `LangSmithAuthError` lines; `ruff check .` → `All checks passed!`.

## Engineering-manager review notes

**Review 1 (2026-06-12):** `emitters.py`/`audit.py`/`langsmith_linkage.py`/`gate_observability.py`
reviewed. Decorator pattern preserves the DTM-0005 seam (collecting consumers unaffected;
wrap idempotent); flagged runner/stages edits are exactly the two anticipated additive
sites (verified by diff). Gate-5's AST upgrade after the worker's own red-proof caught the
docstring false-pass is exemplary — the regression test for it is in place. Audit view
refuses partial reconstruction (`AuditAssemblyError`) rather than silently passing.

**Gap (FIX-1, closed):** tests with `LANGSMITH_TRACING=true` caused LangGraph's global
tracer to POST real payloads to api.smith.langchain.com (401 spam; external data egress
from tests). Fixed via root `tests/conftest.py` autouse session fixture pinning
`LANGSMITH_ENDPOINT`/`LANGCHAIN_ENDPOINT` to an unroutable local port +
`LANGCHAIN_TRACING_V2=false`. Re-verified: 206 passed, zero ingest/auth lines.

## Approved by engineering manager

Status: Approved

Executive summary:
- OBS-WA-00R is implemented end-to-end: every A6 backbone event flows as structured
  JSON logs + OTel span events (graceful no-op without a tracer); a C3 audit view
  reconstructs trigger→versions→emissions→outcome with append-not-overwrite auditability;
  the two-axis replay harness (record-exact byte-compare at tolerance 0 + trigger/lineage
  reconstruction) exists as reusable fixtures; CHRs carry `langsmith_run_id` when tracing
  is on (DL-054 cond. 1); CI gate-5 is real (AST append↔emit pairing, pinned A6
  vocabulary, replay-harness presence) and proven red-able.

Verification (EM-run, independent):
- `pytest tests/positive tests/negative tests/replay` (live env) → **206 passed**
  (baseline 162 intact + 44 new); after FIX-1: zero LangSmith network lines.
- `ruff check .` clean; `ci.gate_invariants` PASS; `ci.gate_observability` PASS.
- Flagged additive diffs inspected: ObservedEventEmitter.wrap at both runner seams;
  linkage merge in retain_stage with declared-values-win.
- Worker red-proofs: all three gate-5 checks demonstrated red (exit 1) live.

Manual test plan:
- Run a recompute with the README env + LANGSMITH_TRACING=true: watch structured event
  lines in the uvicorn log, span events in Tempo, and `langsmith_run_id` inside the new
  CHR's `model_or_rule_version` in Studio.

Remaining risks:
- LangSmith self-hosted instance still owner-pending (config-only stands).
- Replay harness covers record + lineage axes; the derivation axis (semantic, AI-tier)
  activates with Wave B real stages — by design.
