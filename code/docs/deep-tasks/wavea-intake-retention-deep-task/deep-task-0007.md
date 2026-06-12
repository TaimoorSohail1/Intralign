# DTM-0007 — Perceive: artifact intake, integrity clearance, claim extraction, acceptance capture

**Status:** Approved · **Module:** DTM-0007 · **Phase:** II (Wave A) · **Contract:** **IC-WA-001** (+ DL-047 EI-02/CRR-04)

## Goal / observable behavior

A submitted artifact is preserved (body → Supabase Storage, metadata+provenance → Postgres,
append-only), normalized without meaning change, integrity-cleared (attribution + idempotent
dedup_key + evidence chain), and produces a Promotion Candidate. Claim extraction yields
source-attributed evidence-attested assertion drafts. A user acceptance action is captured
(item + version pin) and handed off — not accepted. Re-submission with changed content emits
the change signal and constructs a valid 00R TriggerClaim. All OBS-WA-001 events emitted.

## Source docs / constraints

- `20_handoff/contracts/WAVE_A_CONTRACT_PACKAGE_001_ARTIFACT_INTAKE.md` — A3 (8 required),
  A4 (7 forbidden — prove impossible), A6/A7 events+states, QA B2/B3/B4, OBS C1–C7,
  DL-047 additions (EI-02 claim extraction, CRR-04 stakeholder-response-as-evidence).
- Decisions file (this folder): #1 event-vocab extension, #2 intake schema, #3 Storage,
  #4 dedup_key, #5 extraction seam, #8 stale→00R, #9 capture handoff.
- LDM §2.3; DL-053: `dedup_key` (never `canonical_key`).

## Locked decisions

- New migration: `artifact` (append-only, revoke+trigger like canonical; added to gate-4
  linter list — additive ci edit) + `promotion_candidate` (mutable readiness_state).
- Bodies in Storage bucket `artifacts`; Postgres stores `body_ref` + `normalized_form`.
- Events (decisions #1): `EVENT_NAMES_WA001 = (artifact_received, artifact_normalizing,
  artifact_normalized, promotion_candidate_ready, promotion_readiness_failed,
  user_acceptance_captured, context_signal_received, artifact_modified, stale_detected*)`
  — *`stale_detected` already exists in WA00R set; do NOT duplicate, reference it.
  Gate-5 check (b) updated to assert per-contract sets.
- Claim extraction: `responsibilities/perceive/extraction.py` — `ClaimExtractor` protocol +
  `RuleBasedExtractor` (deterministic; produces AttestedAssertion DRAFTS with
  `attesting_source`=evidence-source-id, `source_ref` carrying artifact+locus,
  `re_derivable=True`). NO Finding/severity/confidence anywhere (DL-047 forbidden).
- Acceptance capture: `responsibilities/perceive/acceptance_capture.py` — captures
  `{user_id, target_kind, version_pin, action}` → emits `user_acceptance_captured` +
  returns a handoff object; UAR row creation is DTM-0008 (Retain).
- Stale: re-submission same project+source, different content hash → `artifact_modified`
  + construct (not submit) a valid 00R TriggerClaim (`knowledge-change`,
  information_changed=True). Integration test MAY submit it via `runner.submit_trigger`.

## Owned files

- `backend/responsibilities/perceive/**` (new modules; keep staleness.py intact —
  additive), `code/supabase/migrations/<new>.sql`, `backend/services/persistence/**`
  (storage client additive), `backend/services/observability/events.py` (ADDITIVE vocab),
  `code/ci/gate_observability.py` + `gate_invariants.py` (additive: vocab sets; linter
  table list) + their tests, `tests/{positive,negative}/perceive_intake/**`, task file
  Worker report.
- READ-ONLY: retain/, adapt/, orchestration/ (consume only), existing migrations, api/.

## Packages / refactors

- None new. No refactors.

## Implementation instructions (TDD)

1. Red: QA-mapped tests first (B2.1–B2.6 positive; B3.1–B3.7 negative, each forbidden
   behavior provably impossible — introspection/static where structural, runtime rejection
   where behavioral).
2. Migration (artifact append-only + candidate) → storage client → intake pipeline →
   extraction → acceptance capture → events/vocab + gate updates.
3. OBS: provenance replay helper (reconstruct origin/lineage of an intake) +
   record-exact replay for acceptance-capture events — extend `tests/replay/` fixtures.

## Test plan

- Positive: full B2 set incl. idempotent re-intake (same dedup_key → same artifact id, no
  second Storage object), extraction produces typed source-attributed drafts, acceptance
  capture carries version pin, stale signal on edit.
- Negative: full B3 set; gate-4 linter accepts new migration; gate-5 passes with extended
  vocab (and its negative tests still red-able).
- Full suite green (baseline 206 + new), ruff, gate-4, gate-5.

## Done criteria

- B2/B3 traceability table in report; all gates green; bodies verifiably in Storage;
  PR cites `IC-WA-001`.

## Worker report

### Built (PR cites IC-WA-001)

| Piece | Path | Notes |
|---|---|---|
| Migration | `supabase/migrations/20260612100000_intake_artifact_candidate.sql` | `artifact` append-only (DTM-0002 pattern: single CREATE, inline constraints, reuses existing `public.enforce_append_only()` statement-level trigger + REVOKE UPDATE/DELETE/TRUNCATE from anon/authenticated/service_role; `dedup_key` UNIQUE; LDM §1 universal fields incl. `epistemic_state` CHECK `'attested-evidence'`, self-FK `supersedes_id`). `promotion_candidate` mutable (readiness_state CHECK pending\|ready\|failed, `integrity_clearance` jsonb, updated_at) — deliberately NO append-only lock. |
| Gate-4 | `ci/gate_invariants.py` | `CANONICAL_TABLES` += `'artifact'` (additive); docstring updated. Tests extended: positive lawful-intake-DDL case; negative 4 new mutation-verb cases on `artifact`. |
| Events | `backend/services/observability/events.py` | Decision #1: existing tuple renamed `EVENT_NAMES_WA00R` (unchanged content), new `EVENT_NAMES_WA001` (8 names, `stale_detected` NOT duplicated), `EVENT_NAMES = WA00R + WA001` kept as union alias; emitters accept the union. |
| Gate-5 | `ci/gate_observability.py` | Check (b) rewritten: each contract tuple asserted verbatim (literal, in order) + `EVENT_NAMES` union-consistency (accepts the `WA00R + WA001` name-concatenation or the literal union). Positive/negative tests extended (incl. WA001 tamper, duplicated `stale_detected`, broken union, non-literal contract tuple). |
| Storage client | `backend/services/persistence/storage.py` | `ArtifactBodyStore`: idempotent `ensure_bucket` (exists-ok), `upload_body(project_id, content)->body_ref`, `download_body(body_ref)`, `list_bodies`. Content-addressed paths `artifacts/<project>/<sha256>.txt` — identical content never multiplies objects. |
| Intake PG store | `backend/services/persistence/intake_store.py` | `SupabaseIntakeStore` (artifact/candidate rows; INSERT-only on artifact). Concrete impl of the seam perceive consumes by injection — keeps direct table access OUT of perceive (existing B3.5 static scan over perceive stays green). |
| Intake pipeline | `backend/responsibilities/perceive/intake.py` | `submit_artifact(submission, *, store, bodies, emitter)` → `IntakeResult`: preserve (Storage+PG) → normalize → integrity-clear → candidate (ready\|failed + clearance jsonb). Idempotent (dedup hit → existing artifact, no new Storage object/candidate). Changed re-submission → new version row (+`supersedes_id`) + `artifact_modified` + CONSTRUCTED 00R `knowledge-change` TriggerClaim (never submitted). Also `receive_context_signal` (A5/CRR-04 seam). |
| Claim extraction | `backend/responsibilities/perceive/extraction.py` | `ClaimExtractor` protocol + `RuleBasedExtractor` (deterministic, exact tier). `AssertionDraft` plain Pydantic (NOT a retain write): `content_type` Literal fact\|assumption\|constraint\|dependency, `attesting_source`=evidence-source-id, `source_ref` {artifact_id, locus}, `re_derivable` Literal[True], `epistemic_state` Literal['attested-evidence'], `extra='forbid'`+frozen. |
| Acceptance capture | `backend/responsibilities/perceive/acceptance_capture.py` | `capture_acceptance({user_id, target_kind, version_pin, action})` → frozen `AcceptanceCapture` handoff + `user_acceptance_captured`. `version_pin` mandatory (`VersionPinMissingError` before any emit — B4 Major). NO UAR row, no truth/approval marking. |
| Exports | `backend/responsibilities/perceive/__init__.py`, `backend/services/persistence/__init__.py` | Additive; `staleness.py` untouched. |
| Tests | `tests/{positive,negative}/perceive_intake/**`, `tests/replay/test_intake_provenance_replay.py`, `tests/replay/test_acceptance_capture_replay.py` | 51 new positive/negative + 6 new replay; live tests skipif env (existing pattern). |

### Normalization rules (version `wa001-n1`, documented in intake.py)

All whitespace-only ⇒ meaning-preserving (the non-whitespace character stream is untouched; asserted in B2.2): N1 CRLF/CR→LF · N2 strip trailing whitespace per line · N3 collapse blank-line runs to one · N4 drop leading/trailing blank lines · N5 section split on Markdown `#` headings (split adds no characters). `normalized_form` = `{version, rules, text, sections[{index, heading, lines}]}`.

**dedup_key** (DL-053, decision #4): SHA-256 over UTF-8 of `project_id + "\n" + source + "\n" + raw content` (raw, pre-normalization — idempotency is over what was submitted).

### Extraction rules (version `wa001-e1`, documented in extraction.py)

Claim line = bullet/numbered item or sentence-like line (ends `.`/`!`); headings/blanks never. Proposition = line minus bullet marker. Classification, first match wins, case-insensitive: E1 `\b(must|shall)\b`→constraint · E2 `depend(s|ed|ing)? on`/`dependenc`→dependency · E3 `assum(e|es|ed|ing|ption)`→assumption · E4 else→fact. Locus = `{section, line}` into `normalized_form.sections`. Determinism: exact tier (asserted: two runs byte-identical).

### B2 traceability (QA-WA-001 positive)

| QA | Test(s) |
|---|---|
| B2.1 provenance + append-only | `tests/positive/perceive_intake/test_b2_intake.py::test_b2_1_artifact_preserved_with_full_provenance_append_only`; live: `test_intake_live.py::test_live_intake_preserves_body_in_storage_and_rows_in_postgres` |
| B2.2 normalization preserves meaning | `test_b2_intake.py::test_b2_2_normalization_preserves_meaning` |
| B2.3 integrity → attributed candidate | `test_b2_intake.py::test_b2_3_integrity_clearance_produces_attributed_candidate` + `test_b2_3_evidence_chain_failure_yields_failed_candidate` (failed path + `promotion_readiness_failed`) |
| B2.4 idempotent, time-attributed | `test_b2_intake.py::test_b2_4_idempotent_reintake_same_artifact_no_new_objects`, `test_b2_4_dedup_key_is_project_and_source_scoped`; live no-second-Storage-object: `test_intake_live.py::test_live_idempotent_reintake_no_second_storage_object` |
| B2.5 acceptance captured w/ item+version | `test_b2_acceptance_capture.py::test_b2_5_acceptance_captured_with_item_and_version_pin`, `::test_b2_5_every_acceptance_action_kind_captures` |
| B2.6 change/stale signal on edit | `test_b2_intake.py::test_b2_6_change_signal_on_resubmission_with_changed_content`; live chain: `test_intake_live.py::test_live_changed_resubmission_chains_and_signals`; integration (constructed claim accepted by 00R): `test_intake_live.py::test_live_constructed_trigger_is_accepted_by_the_00r_backbone` |
| EI-02 extraction (DL-047 positive) | `test_extraction.py` (typed drafts, source attribution + re-derivability on every draft, locus points back into normalized_form, exact-tier determinism, seam protocol) |

### B3 traceability (QA-WA-001 negative — impossibility proofs)

| QA | Proof | Test(s) (`tests/negative/perceive_intake/`) |
|---|---|---|
| B3.1 upload ≠ Attested | behavioral (tables touched == {artifact, promotion_candidate} only) + structural (no perceive module imports retain) + DB (artifact UPDATE/DELETE rejected live) | `test_b3_forbidden.py::test_b3_1_*` (2), `test_artifact_append_only_live.py` (update/delete rejected; candidate-mutable contrast) |
| B3.2 no cognition surface | introspection: no exported name matching finding/issue/confidence/recommendation/clarification/severity/assessment; drafts: closed field set, `severity=`/`confidence=` kwargs raise | `test_b3_forbidden.py::test_b3_2_*` (2) |
| B3.3 no authorization step | source+namespace scan of all perceive modules for `authoriz`/`governance_decision` (gate-4 token scan backstops) | `test_b3_forbidden.py::test_b3_3_no_authorization_surface_anywhere_in_perceive` |
| B3.4 capture ≠ accept | closed+frozen capture shape (no truth/approved field possible; mutation raises), `capture_acceptance` has no store param, no perceive source mentions `user_acceptance_record` | `test_b3_forbidden.py::test_b3_4_*` (2) |
| B3.5 no assessment change | AST: no orchestration import, no `submit_trigger`/`run`/`invoke` call in any perceive module; behavioral: full intake (incl. modified path) emits zero recompute-vocabulary events | `test_b3_forbidden.py::test_b3_5_*` (2); pre-existing 00R scan `tests/negative/orchestration/test_backbone_negative.py::test_b3_5_*` also covers the new modules and stays green |
| B3.6 provenance mandatory; idempotency | `AttributionMissingError` raised BEFORE anything stored/emitted (per-field parametrized); double admission impossible (pipeline short-circuit + UNIQUE backstop, fake and live DB) | `test_b3_forbidden.py::test_b3_6_*` (2), `test_artifact_append_only_live.py::test_duplicate_dedup_key_is_rejected_by_the_database` |
| B3.7 inferred-as-Attested impossible | `epistemic_state` Literal-pinned (`'derived'`/`'attested-oslo'` raise), `re_derivable` pinned True; extractor output always evidence-attested | `test_b3_forbidden.py::test_b3_7_*` (2) |
| B4 Major (acceptance w/o version pin) | rejection before any event | `test_b4_acceptance_version_pin.py` (2) |

### OBS-WA-001

Events emitted at pipeline points through the existing `EventEmitter` seam (constructor-injected, default `CollectingEventEmitter`); C3 audit on every event: who/when/source (`submitted_by`/`submitted_at`/`source`), provenance, integrity-clearance reference on candidate events; acceptance events carry item + version pin. Replay (C5): provenance replay `tests/replay/test_intake_provenance_replay.py` (pure + live: rebuilds origin/lineage from artifact+candidate rows, walks `supersedes_id`, re-derives `normalized_form` from the preserved Storage body record-exactly; tamper-detection negative); record-exact acceptance replay `tests/replay/test_acceptance_capture_replay.py` (byte-compare canonical serialization; event payload reconstructable byte-exactly; tamper named).

### Commands run (real outputs)

| Command | Result |
|---|---|
| `supabase db reset` | clean — "Applying migration 20260612100000_intake_artifact_candidate.sql … Finished supabase db reset on branch feat/phase1-wavea-00r" |
| `python -m pytest -q` (env exported; live tests ran) | **249 passed** (baseline 198 + 51 new, zero regressions) |
| `python -m pytest -q tests/replay` | **14 passed** (baseline 8 + 6 new) — total 263 vs 206 baseline |
| `ruff check .` | All checks passed! |
| `python -m ci.gate_invariants` | PASS: no forbidden tokens, no authority module, no canonical-table mutations in migrations |
| `python -m ci.gate_observability` | PASS: per-contract A6 vocabularies pinned verbatim (union consistent), CHR pairing, replay harness present |
| Live Storage verification (one-off script) | artifact `ac6dc689-8f95-44a0-b078-1211b6892227`; `body_ref artifacts/5e782a96-211f-4ea3-a90a-48fd993361f8/5e3047a2…b999dc.txt`; bucket list shows the object (size 48, text/plain); download round-trips the exact body; readiness `ready` |

### Flags / notes for review

1. **Two consequential edits outside the strict owned list** (directed by decision #1 "check all existing usages incl. tests" — the EVENT_NAMES rename): `tests/positive/observability/test_c2_event_coverage.py` and `tests/negative/orchestration/test_backbone_negative.py` — import + assertion-target changed from `EVENT_NAMES` (now the union) to `EVENT_NAMES_WA00R` where the test pins the 7-name backbone set. No other content touched.
2. **`AcceptanceCapture.project_id` is optional** (`None` default): the contract's capture set is `{user_id, target_kind, version_pin, action}`; project scope is carried when provided because the LDM §2.4 UAR (DTM-0008) needs it. Flagged rather than silently required.
3. **PG writes for intake live in `backend/services/persistence/intake_store.py`** (not named in the task's file list, but within owned `backend/services/persistence/**`): perceive consumes injected protocols (`IntakeStore`/`BodyStore`) — this keeps the pre-existing 00R B3.5 static scan (no `.table`/client acquisition in perceive) green and matches "perceive holds the work, persistence holds the transport".
4. **Failed-readiness path**: attribution-missing is a hard rejection (nothing preserved — provenance loss is B4 Critical); the `failed` candidate path is exercised by an empty/whitespace-only body (evidence chain not intact). If the owner wants attribution failures to also produce failed candidates instead of rejection, that is a one-line policy change in `submit_artifact`.
5. **CRR-04**: a StakeholderResponse enters as ordinary new evidence via `submit_artifact` (documented on `ContextSignal`/intake docstring); no special-cased surface was invented.
6. `supabase db reset` wiped 00R checkpoint tables as expected (re-created on demand by the durable checkpointer); the full suite incl. live 00R runs passed after reset.

## Engineering-manager review notes

**Review 1 (2026-06-12):** Migration replicates the DTM-0002 append-only pattern correctly
(single CREATE, reuses shared trigger, REVOKE incl. TRUNCATE); `promotion_candidate`
deliberately mutable (transient per LDM §2.3) — correct. Event-vocab rename executed
exactly per locked decision #1; the two outside-owned-list test edits are assertion-target
renames forced by that decision (inspected diff — accepted). `intake_store.py` placement in
persistence keeps direct table access out of perceive and preserves the B3.5 static scan —
good design, accepted. AcceptanceCapture.project_id optional — accepted; DTM-0008 requires
scope at UAR recording time. Attribution-missing = hard reject vs broken-evidence-chain =
failed candidate — policy accepted, forwarded to owner list (one-line swap if preferred).

## Approved by engineering manager

Status: Approved

Executive summary:
- Perceive is live per IC-WA-001: artifacts preserved append-only (bodies content-addressed
  in Supabase Storage, metadata+provenance in Postgres with UNIQUE dedup_key idempotency),
  meaning-preserving normalization, integrity clearance producing ready/failed Promotion
  Candidates, deterministic claim extraction (EI-02 drafts, Literal-pinned
  attested-evidence, no cognition), acceptance capture (version-pin mandatory, capture ≠
  accept), changed re-submission → artifact_modified + constructed 00R TriggerClaim.
  OBS-WA-001 events flow through the extended per-contract vocabulary; gates 4+5 updated
  additively and verified.

Verification (EM-run, independent):
- `pytest tests/positive tests/negative tests/replay` (live env) → **263 passed**
  (baseline 206 intact + 57 new).
- `ruff check .` clean; gate-4 PASS (artifact now linted canonical); gate-5 PASS
  (per-contract vocab pinned verbatim, union consistent).
- Live Storage roundtrip: uploaded body → content-addressed path → downloaded bytes
  byte-exact (initial mismatch was EM's str-vs-bytes comparison, not a defect).
- Outside-scope diffs inspected: assertion-target renames only.

Manual test plan:
- Supabase Studio → Storage → bucket `artifacts` → object under the test project path;
  Table editor → `artifact` row append-only (edit attempt rejected).

Remaining risks:
- Attribution-missing policy (hard reject) pending owner preference vs failed-candidate.
- Rule-based extractor is the Wave-B-replaceable seam; rules documented as wa001-e1.
