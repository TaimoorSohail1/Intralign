# DTM-0004 — Retain: append-only CognitionHistoryRecord repository

**Status:** Not started · **Module:** DTM-0004 · **Phase:** II (Wave A) · **Contract:** **IC-WA-00R** (A3.5; CHR is Retain-owned) · **Depends:** DTM-0002, DTM-0003 · **Gate:** owner authorizes Phase II start (DL-044)

## Goal / observable behavior

The `retain` responsibility exposes an append-only CHR repository: `append(...)` persists a
new `cognition_history_record` row (with lineage + provider/model version + LangSmith run id)
and returns it; no code path can update or delete one; reads support by-id, latest-per-output,
and lineage traversal.

## Source docs / constraints

- IC-WA-00R A3.5, A4.2 (append-only), A10 invariants; QA-WA-00R B2.2, B3.2.
- CHR fields: LDM §2.2 — verbatim, incl. `input_attestation_version`, `model_or_rule_version` (provider+model identity), `upstream_lineage`, `recompute_trigger`, `supersedes_chr_id`.
- `code/CONTEXT.md`: CHR is internal cognition (epistemic), not the API entity.

## Locked decisions

- Pydantic model `CognitionHistoryRecord(CognitionEntity)` in `shared/epistemic.py` extension or `responsibilities/retain/models.py` (worker proposes; EM reviews) — `epistemic_state = attested-*`.
- Repository in `responsibilities/retain/repository.py` using `services/persistence` Supabase client; **no UPDATE/DELETE methods exist** on the class (not "not called" — not present).
- Supersession is a new row with `supersedes_chr_id`, never mutation.

## Owned files

- `backend/responsibilities/retain/**`, `backend/services/persistence/**` (Supabase client + CHR data access), matching `tests/{positive,negative}/retain/**`.
- Read-only: migrations (escalate if a schema gap is found — do NOT edit migrations).

## Packages / refactors

- None new. No refactors.

## Implementation instructions (TDD)

1. Red: tests for append/read/lineage; negative tests that the repo surface has no update/delete and that raw UPDATE via the app role fails (DB enforcement from DTM-0002).
2. Green: model + repository.
3. Emit nothing yet (events are DTM-0006); keep the seam (return value carries what events will need).

## Test plan

- Positive: append returns persisted CHR; latest-per-`output_kind` query; lineage chain walk; supersession chain.
- Negative: no update/delete attribute on repository (introspection test); DB rejects UPDATE/DELETE; appending with unknown `recompute_trigger` value rejected (CHECK constraint).

## Done criteria

- QA-WA-00R B2.2/B3.2 demonstrably covered; PR cites `IC-WA-00R`; gates green.

## Worker report

_(pending)_

## Engineering-manager review notes

_(pending)_

## Approved by engineering manager

_(pending)_
