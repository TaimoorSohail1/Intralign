# DTM-0008 — Retain: integrity-gated admission, versioning, supersession, archival, UAR

**Status:** Approved · **Module:** DTM-0008 · **Phase:** II (Wave A) · **Contract:** **IC-WA-002** (DL-043-amended: integrity-gated, NO Authority) · **Depends:** DTM-0007

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

### Built (all additive; no migrations; no new packages; no refactors)

| Piece | File(s) |
|---|---|
| Integrity-gated admission | `backend/responsibilities/retain/admission.py` — `admit_candidate` (candidate row OR id + DTM-0007 `AssertionDraft`s) requires `readiness_state=='ready'` AND `integrity_clearance` present, else `AdmissionRejectedError` BEFORE any write/event. One `attested_assertion` INSERT per draft (v1); `provenance_ref` = origin artifact + candidate ref + integrity-clearance ref; `source_ref` = draft evidence locus (A3.3). Emits `knowledge_promoted` + `knowledge_mutation_recorded`; returns admitted ids + CONSTRUCTED `promotion` TriggerClaim (never submitted — A3.10). Also defines the `RetentionStore` protocol the other modules consume. |
| Versioning/supersession | `backend/responsibilities/retain/versioning.py` — `version_assertion` INSERTS new row `version=prior+1` + `supersedes_id` (prior untouched; DB enforces); appends `knowledge-versioned` AND `superseded` history entries; emits `knowledge_versioned` + `knowledge_superseded` + `knowledge_mutation_recorded`; returns new id + constructed `knowledge-change` TriggerClaim. `version_chain` mirrors DTM-0004 `lineage_chain` incl. seen-set guard. |
| Archival | `backend/responsibilities/retain/archival.py` — `archive_assertion`: NO row mutation/deletion; ONE `history_record` (`archived`, subject_ref carries assertion_id/version/reason); emits `knowledge_archived` + `knowledge_mutation_recorded`. `is_archived` derives status from history (any `archived` event ⇒ archived; no unarchive event type exists in R1 — documented out of scope). |
| UAR recording | `backend/responsibilities/retain/acceptance.py` — `record_acceptance(capture, *, project_id, store)`: `version_pin` MANDATORY (`AcceptanceRecordingError`); writes `user_acceptance_record` (attested-user, version-pinned, decoupled) + `acceptance-recorded` history. **Emits nothing and takes NO emitter** — acceptance is info-change, not knowledge mutation; `user_acceptance_captured` already fired in Perceive (documented in module docstring; introspected by test). Never marks anything true/approved. |
| Store seam | `backend/services/persistence/retention_store.py` — `SupabaseRetentionStore`: INSERT/SELECT ONLY (`get_candidate`, `insert/get_assertion`, `insert/get_acceptance`, `insert_history`, `history_for_assertion`); no update/delete surface exists (introspected). |
| Events + gate | `events.py`: `EVENT_NAMES_WA002` (5 names verbatim) + union `WA00R + WA001 + WA002`. `ci/gate_observability.py` check (b): WA002 tuple asserted verbatim; union check generalized to the 3-way name concatenation (left-fold flatten). Gate tests extended (positive verbatim/union + tamper negatives: renamed WA002 event, dropped WA002 tuple, drifted union, 4-way missing count). |
| OBS audit/replay | Audit: NO new helper — reconstruction proven by tests (`tests/positive/retain_retention/test_c3_audit_reconstruction.py`): full lifecycle (admission→version→supersession→archival) rebuilt from `history_record` rows + event stream alone; events↔history identity cross-check. Replay: `tests/replay/test_retention_replay.py` — record-exact replay of an admitted `attested_assertion` (canonical-JSON byte-compare, harness pattern; tamper negative names the field) + version-chain replay (v1→v2 reconstructed, BOTH rows present, prior byte-intact, integrity-clearance verified per hop). Pure + live axes. |
| Wave A loop | `tests/positive/retain_retention/test_full_loop_live.py` — ONE live test: `submit_artifact` → candidate ready → `RuleBasedExtractor` drafts → `admit_candidate` → `knowledge_promoted` → constructed promotion claim submitted via `runner.submit_trigger("deep_pass", …)` → durable Deep Pass completes (`cognition_state == "current"`) → CHR appended in live DB with `recompute_trigger='promotion'` and `upstream_lineage` = the admitted assertion ids. |
| Exports | `retain/__init__.py` + `services/persistence/__init__.py` — additive exports only. |

### Admission history-event choice (documented per directive)

**Dual events.** Per admission: ONE `integrity-clearance` entry (subject = candidate + admitted assertion ids + the full clearance jsonb — the C3/C5 integrity-clearance reference) PLUS one `knowledge-versioned` entry PER admitted assertion (v1 creation — A7 enters `Active (v1)`; versioning starts at admission). Most faithful to A3.6 ("every promotion, version … recorded") + C5 integrity-clearance verification: clearance and version-creation are separately replayable.

### B2/B3/§B+ → test traceability

| Clause | Test |
|---|---|
| B2.1 admission w/ clearance (amended: integrity-gated) | `positive/retain_retention/test_b2_admission.py::test_b2_1_*` |
| B2.2 version creation, prior intact | `test_b2_versioning.py::test_b2_2_mutation_creates_new_version_prior_intact` |
| B2.3 provenance preservation | `test_b2_admission.py::test_b2_3_*`, `test_b2_versioning.py::test_b2_2_provenance_carried_forward_on_version` |
| B2.4 history preservation | `test_b2_admission.py::test_b2_4_*`, `test_c3_audit_reconstruction.py` (all 3) |
| B2.5 explicit supersession | `test_b2_versioning.py::test_b2_5_supersession_is_explicit_marked_and_traceable` |
| B2.6 recompute triggering | `test_b2_admission.py::test_b2_6_*`, `test_b2_versioning.py::test_b2_6_*`, `test_full_loop_live.py` (live submit) |
| B2.7 archival w/o destruction | `test_b2_archival.py` (all 4) |
| B3.1 silent overwrite impossible | `negative/retain_retention/test_b3_no_mutation_surface.py` (surface = exactly insert+select; live UPDATE denied ×3) + replay prior-intact byte-compare |
| B3.2 deletion/destruction impossible | `test_b3_no_mutation_surface.py::test_raw_delete_*` (live ×3) + fake-surface introspection |
| B3.3 non-cleared admission impossible (amended) | `test_b3_admission_rejected.py` (readiness `pending`/`failed`; clearance `None`/`{}`; missing candidate; empty drafts — nothing written/emitted on every path) |
| B3.4/B3.5 no Findings/Recommendations/Confidence | `test_b3_no_cognition_surface.py::test_b3_4_b3_5_*`, `::test_admitted_rows_carry_no_score_or_assessment_field` |
| B3.6 assessment mutation w/o recompute impossible | `test_b3_no_cognition_surface.py::test_b3_6_*` (no orchestration import/call; no recompute event emitted) |
| B3.7 silent supersession impossible | `test_b3_silent_supersession.py` (AST: only versioning.py writes `supersedes_id`; emit-call introspection; event-sequence; rejection path) |
| B3.8 provenance loss impossible | admission/versioning carry-forward tests + replay clearance-per-hop check |
| B3.9 no cross-ownership / governance gate (amended ⇒ §B+ 7) | `test_b3_admission_rejected.py::test_b_plus_7_*` (token scan + signature introspection; gate-4 backstops) |
| §B+ 3 UAR version-pinned | `test_b2_acceptance.py::test_b_plus_3_uar_row_is_version_pinned_and_user_attested` (+ live table insert) |
| §B+ 4 (pos) attested asm/constraint/dep admit | `test_b2_admission.py::test_b_plus_4_*` |
| §B+ 5 clearance recorded on admission | `test_b2_admission.py::test_b2_3_*`/`test_b2_4_*` |
| §B+ neg 3 acceptance-as-truth impossible | `test_b4_acceptance_negative.py::test_b_plus_3_*` (row fields ⊆ allowed set; no truth marker; item untouched; module emits nothing) |
| §B+ neg 4 UAR w/o pin rejected | `test_b4_acceptance_negative.py::test_b_plus_4_*` |
| §B+ neg 6 admission w/o clearance | `test_b3_admission_rejected.py::test_b_plus_6_*` |
| C3/C4 audit reconstructable | `test_c3_audit_reconstruction.py` |
| C5 record-exact + version-chain + clearance verification | `tests/replay/test_retention_replay.py` (pure + live) |
| C2 events == A6 verbatim | gate-5 + `test_gate_observability.py::test_wa002_vocabulary_*` |

### Commands + real results (2026-06-12, local Supabase up)

| Command | Result |
|---|---|
| `pytest -q tests/positive tests/negative tests/replay` (live env) | **327 passed** (baseline 263 + 64 new; 0 failed, 0 skipped) |
| same, env unset (skip contract) | **260 passed, 67 skipped, 0 failed** |
| `ruff check .` | `All checks passed!` |
| `python -m ci.gate_invariants` | PASS (no forbidden tokens / no governance module / no canonical-table mutations) |
| `python -m ci.gate_observability` | PASS (pairing + per-contract vocabularies verbatim, union consistent + replay harness) |
| `pytest tests/positive/retain_retention/test_full_loop_live.py -v` | `test_wave_a_full_loop_intake_to_admission_to_recompute_receipt PASSED` |

### Flags

1. `backend/services/persistence/__init__.py` gained one additive export line (`SupabaseRetentionStore`) — mirrors the DTM-0007 pattern; not literally on the owned list.
2. Wave A loop CHR emission: with Infer/Evaluate placeholders, the recompute's emission spec is declared on the submitted trigger payload (locked DTM-0005/0006 pattern); the integration test sets its `upstream_lineage` to the admitted assertion ids. Waves B/C replace this with real cognition producers.
3. `gate_contract` (gate-2) reports FAIL locally only because no PR body exists yet — the Wave A PR must cite `IC-WA-002` (and `IC-WA-001`).
4. Audit kept test-proven (no new `services/observability` helper) — smaller owned surface; reconstruction demonstrated from history rows + events directly.

## Engineering-manager review notes

**Review 1 (2026-06-12):** Admission gate verified strict (rejection BEFORE any
write/event); versioning is the only superseding write path (AST-proven) with dual
explicit history events; archival mutates nothing; UAR recording deliberately takes no
emitter (info-change, not knowledge mutation — correct contract reading, documented +
introspected). Retention store INSERT/SELECT-only mirrors the DTM-0004 discipline. Flag
rulings: persistence `__init__` export line accepted (established pattern); loop-test
emission declared on trigger payload accepted (locked placeholder pattern until Wave B);
dual admission history events (`integrity-clearance` + `knowledge-versioned`) accepted as
the faithful reading.

## Approved by engineering manager

Status: Approved

Executive summary:
- Retain now fulfills IC-WA-002 as DL-043-amended: integrity-gated admission of cleared
  Promotion Candidates into the append-only canonical store with full provenance;
  versioning + explicit (never silent) supersession; destruction-free archival derived
  from history; version-pinned UAR recording that asserts no truth. Every mutation is
  history-recorded, evented (WA002 vocabulary), audit-reconstructable, and replayable.
  The full Wave A loop runs live end-to-end: intake → clearance → extraction → admission
  → promotion trigger → durable Deep Pass → CHR appended.

Verification (EM-run, independent):
- `pytest tests/positive tests/negative tests/replay` (live env) → **327 passed**
  (263 baseline intact + 64 new).
- `ruff check .` clean; gate-4 PASS; gate-5 PASS (3-contract vocabulary).
- Wave A loop integration test passed in isolation (1 passed).
- Scope check: no files modified beyond the owned/additive-allowed set.

Manual test plan:
- Run the loop test live; inspect in Studio: `attested_assertion` v1+v2 rows (prior
  intact), `history_record` trail (clearance → versioned → superseded → archived →
  acceptance-recorded), CHR row from the triggered Deep Pass.

Remaining risks:
- Recompute emissions remain trigger-declared until Wave B real stages (inherited).
- No unarchive in R1 (documented; owner can scope later).
