# code/ci — App CI gate logic (DTM-0001)

Unit-testable gate scripts called by `.github/workflows/app-ci.yml`, implementing
the Deployment Governance §4 gate sequence (semantics per the starter-kit
`30_engineering/delivery/starter_kit/ci-pipeline.yml`). Steps run in order; the
first failure stops the run and blocks the PR.

| Gate | Step(s) | Logic lives in |
|---|---|---|
| 1 Build | `pip install -e ".[dev]"` + `ruff check .`; frontend `npm ci` + `npm run build` (tsc + vite) | workflow |
| 2 Contract-traceability | PR body cites an approved `IC-*` id; label `phase-1-infra` bypasses (Phase I only, decision #3) | `gate_contract.py` |
| 3 Tests | `pytest tests/positive` and `pytest tests/negative` as separate steps — empty (exit 5) or absent (exit 4) suite fails on its own | workflow (pytest exit codes) |
| 4 Epistemic-invariant | forbidden-token scan (`invariant_allowlist.txt` exempts prose mentions only) · no `backend/**/authority` dir · canonical-table migration linter | `gate_invariants.py` |
| 5 Observability | REAL (**DTM-0006**, OBS-WA-00R): `python -m ci.gate_observability` — (a) every CHR-append call-site paired with a `cognition_history_record_appended` emit, (b) A6 event vocabulary pinned verbatim in `events.py`, (c) `tests/replay/` present + non-empty — then `python -m pytest tests/replay` (two-axis replay; live axes skip without Supabase, pure tamper axes always run) | `gate_observability.py` |
| 6 Security | gitleaks action (secret scan) · `pipx run pip-audit .` (production deps) · `npm audit --omit=dev --audit-level=high`; findings FAIL, never warn | workflow |
| 7 Human review | GitHub **branch protection** on `main` (required reviewer = owner) — not the workflow | — |

Run the gate-script tests locally (from `code/`):

```sh
python -m pytest tests/positive/ci tests/negative/ci -v
# gate-5 script tests live with the observability suites (DTM-0006):
python -m pytest tests/positive/observability tests/negative/observability -v
```

Run a gate by hand (from `code/`):

```sh
PR_BODY="Implements IC-WA-00R" PR_LABELS="[]" python -m ci.gate_contract
python -m ci.gate_invariants
python -m ci.gate_observability
```

## Allowlist (`invariant_allowlist.txt`)

Gate 4(a) flags ANY occurrence of `GovernanceDecision` / `Authority` in `.py`
files under `backend/` + `shared/`. Existing prose mentions (e.g. comments
restating "No Authority engine") are exempted via explicit
`path :: line-substring` entries. **Never allowlist an identifier**; every
addition is reviewed under gate 7.

## Forced-failure procedure (EM red-proof, one throwaway change per gate)

Each gate must be demonstrated red exactly once (DTM-0001 done criteria). On a
scratch branch, make ONE of the changes below, push, watch the gate fail, then
revert (or drop the branch). Do them one at a time — the run stops at the first
failure, so a later gate's proof needs the earlier gates left green.

1. **Gate 1 (build):** add a syntax error to any backend `.py` file (e.g. a bare
   `def broken(` at the end of `backend/__init__.py`) — `ruff check .` fails.
   Frontend leg: add `const x: number = "no"` to `frontend/src` — `tsc` fails.
2. **Gate 2 (contract):** open a PR whose body cites no `IC-*` id and carries
   **no** `phase-1-infra` label. Also prove the inverse: add the label, gate
   goes green with the same body.
3. **Gate 3 (tests):** add `assert False` to a test in `tests/positive/` (and
   once in `tests/negative/`). Empty-suite leg: temporarily move all files out
   of `tests/negative/` — pytest exits 5 (no tests collected) and the step fails.
4. **Gate 4 (invariants):** any one of:
   - add `GovernanceDecision = None` to `shared/entities.py` (token scan);
   - `mkdir code/backend/authority` with a `.gitkeep` (forbidden module);
   - add `code/supabase/migrations/9999_bad.sql` containing
     `UPDATE attested_assertion SET attesting_source = 'x';` (migration linter).
5. **Gate 5 (observability):** any one of:
   - remove/comment the `ctx.emitter.emit("cognition_history_record_appended", ...)`
     call in `backend/orchestration/stages.py` — the append↔event pairing
     check fails (a governed emission without its event). The check is
     AST-level: the docstring/comment mentions of the event name do NOT
     satisfy it;
   - rename one entry in `EVENT_NAMES` in
     `backend/services/observability/events.py` (e.g. `recompute_failed` →
     `recompute_errored`) — the A6 vocabulary check fails;
   - move `tests/replay/` aside (e.g. `mv tests/replay /tmp/replay.bak`) —
     the harness-presence check fails, and the `pytest tests/replay` leg
     exits 4 on the missing path.
6. **Gate 6 (security):** commit a fake high-entropy secret (e.g. a dummy AWS
   key `AKIA...` in a scratch file) — gitleaks fails. **Use an obviously fake
   value; never a real credential.** Dependency legs: pin a known-vulnerable
   version (e.g. temporarily set `axios` to `0.21.0` in
   `frontend/package.json` + lockfile) — `npm audit` fails.
7. **Gate 7:** not workflow-provable — verify branch protection blocks merging
   an unapproved PR.

Revert every throwaway change before the real PR is reviewed.
