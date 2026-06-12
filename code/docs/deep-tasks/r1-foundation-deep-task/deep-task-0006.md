# DTM-0006 — OBS-WA-00R: events, audit, two-axis replay; CI gate-5 goes real

**Status:** Not started · **Module:** DTM-0006 · **Phase:** II (Wave A) · **Contract:** **IC-WA-00R / OBS-WA-00R** · **Depends:** DTM-0005

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

_(pending)_

## Engineering-manager review notes

_(pending)_

## Approved by engineering manager

_(pending)_
