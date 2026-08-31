# Deep-task plan — Wave A completion (IC-WA-001 + IC-WA-002)

Branch `feat/phase1-wavea-00r` (continues). One fresh worker per task, sequential,
EM review → fix → verify → approve between tasks.

## Slices

| # | Module | Slice (vertical outcome) | Contract | Depends on |
|---|---|---|---|---|
| 1 | DTM-0007 | Perceive intake: artifact ingestion (Storage+PG), normalization, integrity clearance, Promotion Candidates, claim extraction seam, acceptance capture, stale signal → 00R trigger, OBS-WA-001 events + gate-5 vocab extension | IC-WA-001 | r1 sequence (approved) |
| 2 | DTM-0008 | Retain retention: integrity-gated admission of candidates → attested_assertion, versioning + explicit supersession, archival via history events, UAR recording, mutation events → 00R trigger, OBS-WA-002 | IC-WA-002 | DTM-0007 |

## Test strategy

- QA-mapped test names (`test_b2_*`, `test_b3_*`) per contract — same traceability
  discipline as 00R.
- 0007 negatives: upload≠Attested (B3.1), no cognition from Perceive (B3.2), no
  Authority step (B3.3), capture-not-accept (B3.4), no assessment change from intake
  (B3.5), provenance loss / non-idempotent intake impossible (B3.6), inferred-as-Attested
  impossible (B3.7).
- 0008 negatives: no self-admission without clearance, no overwrite/delete (DB-proven),
  no silent supersession, no cognition/confidence from Retain, provenance preserved.
- OBS: record-exact replay for acceptance capture (0007) + provenance replay; 0008 events
  extend the audit view coverage.
- Full suite + ruff + gate-4 + gate-5 green at each approval; baseline 206 must not regress.

## Manual checks (EM)

- Storage: artifact body visible in Supabase Studio bucket `artifacts`.
- End-to-end: submit artifact → candidate ready → (0008) admitted as attested_assertion →
  knowledge-promoted event → 00R trigger fires a Deep Pass run.

## Done = Wave A complete

Both contracts' B2/B3 sets demonstrably covered; events observable; Phase II Wave A
candidate-complete for owner exit-gate review (then Wave B planning).
