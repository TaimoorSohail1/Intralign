# DTM-0004 — Retain: append-only CognitionHistoryRecord repository

**Status:** Approved · **Module:** DTM-0004 · **Phase:** II (Wave A) · **Contract:** **IC-WA-00R** (A3.5; CHR is Retain-owned) · **Depends:** DTM-0002, DTM-0003 · **Gate:** owner authorized Phase II start 2026-06-12 (DL-044)

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

### Built

- `backend/responsibilities/retain/models.py` — Pydantic `CognitionHistoryRecord(CognitionEntity)`
  (placement as recommended: retain-owned `models.py`, not a `shared/epistemic.py` extension —
  the CHR is Retain's object per IC-WA-00R; `shared` keeps only the cross-cutting base).
  Fields mirror LDM §2.2 verbatim + the live table's LDM §1 universal fields:
  `chr_id` (uuid, client default), `output_kind` (`Literal` of the exact 12 CHECK values),
  `output_payload` (dict), `emitted_at` (server-assigned when `None`), `input_attestation_version`
  (str), `model_or_rule_version` (dict; provider+model, optional LangSmith run-id key),
  `upstream_lineage` (dict), `recompute_trigger` (`Literal` of the exact 5 values),
  `supersedes_chr_id` (uuid|None), `project_id` (uuid), `created_at` (server-assigned),
  `created_by` (default `"OSLO"`), `epistemic_state` **pinned** `Literal[EpistemicState.ATTESTED_OSLO]`,
  `provenance_ref` (dict), `version` (int, default 1).
- `backend/responsibilities/retain/repository.py` — `ChrRepository` with EXACTLY
  `append` / `get` / `latest_for_output` / `lineage_chain`. No update/delete/upsert anywhere on
  the class (introspection-tested, not just unused). `append` dumps `mode="json", exclude_none=True`
  so Postgres defaults assign `emitted_at`/`created_at`; `lineage_chain` walks `supersedes_chr_id`
  most-recent-first with a seen-set guard (terminates on malformed self-reference). No cognition
  logic — receipts only (A4.3).
- `backend/responsibilities/retain/__init__.py` — ownership docstring kept; exports
  `__all__ = ["ChrRepository", "CognitionHistoryRecord"]`.
- `backend/services/persistence/client.py` (+ `__init__.py` export, docstring kept) —
  `get_supabase_client()` reading `SUPABASE_URL`/`SUPABASE_SERVICE_ROLE_KEY`; raises a clear
  `RuntimeError` naming the missing variable(s). `supabase` is imported **lazily** inside the
  function so the no-db negative suite (and any CI venv without supabase-py) can import the
  repository class for introspection.
- Tests: `tests/positive/retain/test_chr_repository.py` (6 tests: append persists + server fields +
  independent DB read-back; get round-trip; get-missing → None; latest_for_output picks newest of 2
  by `emitted_at` and None for an unemitted kind; supersession appends a NEW row with the original
  intact; lineage chain C→B→A and root→[self]) and
  `tests/negative/retain/test_chr_repository_negative.py` (6 tests: no update/delete/upsert/remove/
  overwrite/purge attribute and public surface == exactly the locked 4-method set — both run with NO
  db env, no skip; pydantic rejects invalid `recompute_trigger`, unknown `output_kind`, and
  non-`attested-oslo` `epistemic_state`; raw UPDATE on `cognition_history_record` via supabase
  client → `permission denied` [skipif env]).

### ⚠️ FLAG — additive change to `shared/epistemic.py` (seam gap, as authorized by task)

`EpistemicState` lacked members for the DB CHECK values (`attested-evidence` / `attested-oslo` /
`attested-user` — LDM §1 universal-field vocabulary used by migration `20260612090000`). Added the
three members **additively**: `ATTESTED_EVIDENCE`, `ATTESTED_OSLO`, `ATTESTED_USER`.
`ATTESTED_INTAKE` / `ATTESTED_ACCEPTANCE` were NOT removed or renamed. Usage evidence:

```
grep -rn "attested-intake|attested-acceptance|ATTESTED_INTAKE|ATTESTED_ACCEPTANCE" (whole repo, .py/.md/.sql/.yml)
→ only hit: code/shared/epistemic.py itself (the two enum-member definition lines)
```

i.e. the legacy members are defined-but-unreferenced (docstring/comment-level only); nothing in
code, tests, migrations, or docs binds to them. Reconciling them against the LDM vocabulary (they
look like an earlier draft naming of evidence/user attestation) is an owner/EM decision — out of
scope here per the additive-only rule.

### Commands run (all from `code/`, venv `/tmp/oslo-ci-venv`, local Supabase up on 54331)

| Command | Result |
|---|---|
| `pytest tests/positive/retain tests/negative/retain -q` (before impl) | RED — 2 collection errors (imports missing), as expected |
| `pytest tests/positive/retain tests/negative/retain -q` (env exported) | **12 passed** |
| `env -u SUPABASE_URL -u SUPABASE_SERVICE_ROLE_KEY pytest tests/{negative,positive}/retain -q -rs` | **5 passed, 7 skipped** — introspection + pydantic negatives run with no db env; live tests skip with the standard reason |
| `pytest tests/positive tests/negative -q` (env exported) | **96 passed** (baseline 84 + 12 new; the `StatusCode.UNAVAILABLE` OTel lines are the pre-existing observability negative-suite noise, not failures) |
| `ruff check .` | `All checks passed!` |
| `python ci/gate_invariants.py` | `PASS: no forbidden tokens, no authority module, no canonical-table mutations in migrations.` (exit 0) |

### Deviations / notes

- `created_at` is on the model although the task's field list omitted it: the task also says fields
  "mirror LDM §2.2 + the table", and the table (and LDM §1 universal fields) carry `created_at`;
  modeled as server-assigned (`None` until persisted), same as `emitted_at`. EM may strike it.
- `upstream_lineage` typed `dict` (task: "dict or list-in-dict"); tests use
  `{"chr_ids": [...], "assertion_ids": [...]}`. jsonb accepts either shape; dict chosen so lineage
  refs are labeled, not positional.
- `lineage_chain(missing_id)` returns `[]`; `lineage_chain(root)` returns `[root]` (documented in
  the method docstring; covered by tests).
- No migrations touched; no schema gap found beyond the enum flag above. No new packages.
  Nothing committed (per task rules). `deep-task-decisions.md` shows a pre-existing uncommitted
  EM edit (Owner gates section) — not mine, left untouched.

## Engineering-manager review notes

**Review 1 (2026-06-12):** `repository.py` + `models.py` reviewed — append-only by
construction (4-method surface, introspection-locked by negative tests), supersession =
append with `supersedes_chr_id`, lineage walk loop-guarded, zero cognition logic (A4.3),
Literal-typed enums matching DB CHECKs exactly, lazy supabase import keeps the class
importable env-free. Placement ruling: retain-owned `models.py` accepted (CHR is Retain's
object). `created_at` on the model accepted (table + LDM §1 carry it; server-assigned).

**Enum ruling (worker flag 1):** legacy `ATTESTED_INTAKE`/`ATTESTED_ACCEPTANCE` were
EM-scaffold guesses predating the LDM binding, proven unreferenced by worker's repo-wide
grep — **removed by EM** (one-name-per-concept; LDM §1 vocabulary is canonical). The
worker's three additive members stand.

## Approved by engineering manager

Status: Approved

Executive summary:
- The retain responsibility now owns a database-backed, append-only CHR repository —
  the canonical receipt store every later wave appends through (IC-WA-00R A3.5).
  Append/get/latest/lineage only; mutation is impossible at three layers (class surface,
  role grants, DB trigger).

Verification (EM-run, independent, after enum cleanup):
- `pytest tests/positive tests/negative` (live Supabase) → **96 passed**.
- `ruff check .` → All checks passed; `ci.gate_invariants` → PASS.
- No-env run of `tests/negative/retain` → 5 passed, 1 skipped (introspection +
  pydantic negatives execute without a database, as designed).
- Worker TDD evidence: red first (2 collection errors), then green; raw UPDATE via
  client → permission denied.

Manual test plan:
- From `code/` with Supabase env set: `python -c "from backend.responsibilities.retain
  import ChrRepository; print([m for m in dir(ChrRepository) if not m.startswith('_')])"`
  → exactly ['append', 'get', 'latest_for_output', 'lineage_chain'].

Remaining risks:
- `model_or_rule_version` shape (provider/model/run-id keys) is convention-only until
  DTM-0006 pins it for replay — tracked there.
- PR citing `IC-WA-00R` happens at push time (commit message carries the id).
