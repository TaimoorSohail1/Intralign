# DTM-0008 — Retain: integrity-gated admission, versioning, supersession, archival, UAR

**Status:** Not started · **Module:** DTM-0008 · **Phase:** II (Wave A) · **Contract:** **IC-WA-002** (DL-043-amended: integrity-gated, NO Authority) · **Depends:** DTM-0007

## Goal / observable behavior

A ready, integrity-cleared Promotion Candidate is admitted as one or more
`attested_assertion` rows (Knowledge Promoted, initial version) referencing its integrity
clearance. A knowledge mutation creates a NEW version row with explicit supersession
(prior intact, marked, traceable) and emits a mutation event that constructs a valid 00R
trigger. Archival is an append-only `history_record` event (`archived`) — nothing
destroyed. A captured acceptance action becomes a User Acceptance Record (version-pinned,
decoupled, never truth-assertion). All OBS-WA-002 events emitted; admission/versioning
auditable + replayable.

## Source docs / constraints

- `20_handoff/contracts/WAVE_A_CONTRACT_PACKAGE_002_CANONICAL_KNOWLEDGE_RETENTION.md` —
  **DL-043 amendments govern** (integrity-gated; no Authority anywhere): A3 (10 required),
  A4 (12 forbidden — under amendment, A4.1 = "no admission without integrity clearance"),
  A7 lifecycle, A10 invariants, QA §B (+§B+ extensions), OBS §C (+§C+).
- Decisions file: #6 archival-as-history-event, #7 versioning, #9 UAR recording.
- LDM §2.1/§2.4/§2.5; existing schema (DTM-0002) — attested_assertion / user_acceptance_record /
  history_record tables live, append-only enforced.

## Locked decisions

- `responsibilities/retain/` additive modules: `admission.py` (admit candidate →
  assertions; REQUIRES readiness_state='ready' + integrity_clearance present — reject
  otherwise), `versioning.py` (new-version + explicit supersession; history events),
  `archival.py` (history-event based; status derivable), `acceptance.py` (UAR creation
  from 0007 handoff; version_pin mandatory — reject without it, QA B4 Major).
- Repositories follow DTM-0004 pattern: NO update/delete surfaces; supersession =
  new row + `supersedes_id`; every mutation also appends a `history_record`
  (`knowledge-versioned` / `superseded` / `archived` / `acceptance-recorded` /
  `integrity-clearance` event types — all already in the DTM-0002 CHECK).
- Events: `EVENT_NAMES_WA002 = (knowledge_promoted, knowledge_versioned,
  knowledge_superseded, knowledge_archived, knowledge_mutation_recorded)` — additive to
  events.py + gate-5 sets (pattern established in DTM-0007).
- Mutation events construct a valid 00R TriggerClaim (`promotion` for admission,
  `knowledge-change` for version/supersession) — Retain emits the trigger, never runs the
  cascade itself (A3.10); integration test submits via `runner.submit_trigger`.
- Retain produces NO cognition, NO confidence, NO presentation (A4.2/3/6) — introspection
  negatives like DTM-0004/5.

## Owned files

- `backend/responsibilities/retain/**` (additive modules only; repository.py/models.py
  from DTM-0004 are READ-ONLY — extend via new files), `backend/services/observability/events.py`
  (additive WA002 vocab), `code/ci/gate_observability.py` (+tests, additive),
  `tests/{positive,negative}/retain_retention/**`, `tests/replay/**` (additive fixtures),
  task file Worker report.
- READ-ONLY: perceive/ (consume 0007 objects as-is), adapt/, orchestration/ (consume
  `runner.submit_trigger` only), ALL migrations (schema gap → STOP and report).

## Packages / refactors

- None new. No refactors.

## Implementation instructions (TDD)

1. Red: QA-mapped tests (B2 + B+ positive; B3/B- negative) first.
2. admission → versioning/supersession → archival → UAR → events + gate vocab → OBS
   audit/replay extensions.
3. End-to-end integration test: 0007 intake → candidate → 0008 admission →
   knowledge_promoted → 00R Deep Pass run completes (the full Wave A loop, live).

## Test plan

- Positive: admission with clearance; version chain v1→v2 with both rows present;
  explicit supersession marked + traceable; archival event + status derivation; UAR with
  version pin; full-loop integration (intake→admission→recompute).
- Negative: admission without clearance/readiness rejected; UPDATE/DELETE impossible
  (DB + surface introspection); silent supersession impossible (no API without explicit
  event); UAR without version_pin rejected; no cognition/confidence surfaces on retain;
  provenance fields mandatory.
- Full suite green, ruff, gate-4, gate-5.

## Done criteria

- B2/B3 (+amendment §B+) traceability in report; full Wave A loop demonstrated live;
  PR cites `IC-WA-002`; Wave A candidate-complete for owner exit gate.

## Worker report

_(pending)_

## Engineering-manager review notes

_(pending)_

## Approved by engineering manager

_(pending)_
