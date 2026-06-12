# DTM-0007 — Perceive: artifact intake, integrity clearance, claim extraction, acceptance capture

**Status:** Not started · **Module:** DTM-0007 · **Phase:** II (Wave A) · **Contract:** **IC-WA-001** (+ DL-047 EI-02/CRR-04)

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

_(pending)_

## Engineering-manager review notes

_(pending)_

## Approved by engineering manager

_(pending)_
