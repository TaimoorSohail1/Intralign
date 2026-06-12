# DTM-0001 — App CI: six-gate pipeline, provably failing

**Status:** Not started · **Module:** DTM-0001 · **Phase:** I · **Contract:** none (Phase-I infra; PR label `phase-1-infra`)

## Goal / observable behavior

A PR touching `code/**` triggers `.github/workflows/app-ci.yml`, which runs the
Deployment-Governance gate sequence in order and **blocks the PR when any gate fails**.
Each gate has a demonstrated forced-failure (red) proof.

## Source docs / constraints

- Gate sequence + semantics: `00_owner/build_governance/DEPLOYMENT_GOVERNANCE_SPECIFICATION_V1.md`; reference template `30_engineering/delivery/starter_kit/ci-pipeline.yml`.
- Decisions file: gate realism table (decisions #2), gate-2 exemption (#3), gate-4 checks (#8).
- Must NOT touch `.github/workflows/doc-integrity.yml`.

## Locked decisions

- Path filter: `on: pull_request/push` with `paths: ["code/**", ".github/workflows/app-ci.yml"]`.
- Gates: 1 build (pip install + ruff + frontend tsc/vite build) · 2 contract-traceability (PR body cites valid `IC-*` id; label `phase-1-infra` bypasses) · 3 tests (pytest `tests/positive` AND `tests/negative`; fail if either suite empty) · 4 epistemic-invariant (forbidden-token scan; no `/authority` dir; migration linter per decisions #8) · 5 observability (scaffold: assert hook files exist; upgraded in DTM-0006) · 6 security (gitleaks secret-scan + pip-audit + npm audit).
- Gate scripts live in `code/ci/` (e.g. `gate_contract.py`, `gate_invariants.py`) so they're testable locally; workflow steps call them.

## Owned files

- `.github/workflows/app-ci.yml` (new), `code/ci/**` (new).
- Read-only: everything else; do not modify app skeleton or docs.

## Packages / refactors

- Approved: gitleaks action, pip-audit. No others. No refactors.

## Implementation instructions

1. Write `code/ci/` gate scripts with unit-testable logic (pure functions; exit codes).
2. Author `app-ci.yml` calling them in gate order; any failure stops the job.
3. Positive+negative tests for gate scripts under `code/tests/{positive,negative}/ci/`.
4. Document the forced-failure procedure per gate in `code/ci/README.md` (one throwaway commit per gate flips it red).

## Test plan

- Automated: pytest for gate scripts (valid/invalid PR bodies; token scan hits/misses; migration linter accepts good SQL, rejects `UPDATE`/`DELETE`/`DROP`/`ALTER` on canonical tables).
- Manual (EM): forced-failure PR proof, each gate red exactly once.

## Done criteria

- Workflow green on the branch; every gate demonstrated red via forced failure; gate scripts tested both ways; doc-integrity workflow untouched.

## Worker report

_(worker fills in: what changed, commands run, results)_

## Engineering-manager review notes

_(EM fills in)_

## Approved by engineering manager

_(pending)_
