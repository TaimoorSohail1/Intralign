# DTM-0001 — App CI: six-gate pipeline, provably failing

**Status:** Approved · **Module:** DTM-0001 · **Phase:** I · **Contract:** none (Phase-I infra; PR label `phase-1-infra`)

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

**Worker:** Claude (DTM-0001) · **Date:** 2026-06-12

### What was built

- **`.github/workflows/app-ci.yml`** (new) — `app-ci` workflow, `on: pull_request/push` to `main`, path-filtered `["code/**", ".github/workflows/app-ci.yml"]`, `permissions: contents: read`, `defaults.run.working-directory: code`. One job, gates as ordered steps; default GitHub Actions fail-fast = any gate failure stops the run.
  - Gate 1: `pip install -e ".[dev]"` + `ruff check .` (backend step); `npm ci` + `npm run build` (= `tsc -b && vite build`) in `code/frontend` (frontend step). Python 3.12 / Node 20 setup actions.
  - Gate 2: `python -m ci.gate_contract`, with `PR_BODY` / `PR_LABELS` passed via `env:` (never shell-interpolated — injection-safe). Step is `if: github.event_name == 'pull_request'` — push-to-main events carry no PR body/labels; the gate already ran on the PR and merge is gate-7 protected (deviation noted below).
  - Gate 3: `python -m pytest tests/positive` and `tests/negative` as **separate steps** — pytest exits 5 on an empty suite and 4 on an absent path, so "empty or absent suite fails" holds without extra script.
  - Gate 4: `python -m ci.gate_invariants`.
  - Gate 5 (scaffold): `test -f backend/services/observability/__init__.py` — a real step that CAN fail — then prints that the real check lands with Wave A (DTM-0006).
  - Gate 6: `gitleaks/gitleaks-action@v2` (checkout uses `fetch-depth: 0` for history scan) · `pipx run pip-audit .` (audits `[project.dependencies]` from pyproject — production scope) · `npm audit --omit=dev --audit-level=high`. All blocking; no warn-only.
  - Gate 7 noted in comments as branch protection on `main`, not workflow; gate 8 noted out of Phase I scope. `doc-integrity.yml` untouched.
- **`code/ci/gate_contract.py`** (new) — pure `check_contract_citation(body, labels) -> (bool, msg)`; approved-id set (IC-WA-00R, IC-WA-001, IC-WA-002, IC-WB-INFER, IC-WB-EVAL, IC-WC-ADVISE, IC-WU-ACCEPT, IC-WE-DISCLOSE); `phase-1-infra` bypass per decision #3; case-sensitive `\bIC-[A-Z0-9]+(-[A-Z0-9]+)*\b` extraction (so `IC-WA-001X` and `ic-wa-00r` are not citations); thin argparse/env CLI main, exit 0/1.
- **`code/ci/gate_invariants.py`** (new) — three pure checks + `run_all_checks(code_root)`:
  (a) forbidden-token scan (`GovernanceDecision`, `Authority` — word-start regex, so `AuthorityEngine` is caught) over `.py` under `backend/` + `shared/`, ANY occurrence flagged unless allowlisted (per task simplification — no docstring parsing);
  (b) fail on any dir named `authority` (case-insensitive) under `code/backend`;
  (c) statement-aware migration linter over `code/supabase/migrations/**/*.sql` — rejects `UPDATE` / `DELETE FROM` / `DROP TABLE` / `ALTER TABLE` statements targeting `attested_assertion` / `cognition_history_record` / `user_acceptance_record` / `history_record` (schema-qualified, quoted, `IF EXISTS`/`ONLY`, lowercase all handled); strips SQL comments + dollar-quoted bodies first, so decision #4's `REVOKE UPDATE, DELETE ON …` and `CREATE TRIGGER … BEFORE UPDATE OR DELETE ON …` do NOT false-positive; missing/empty migrations dir passes. CLI main `--code-root`, exit 0/1.
- **`code/ci/invariant_allowlist.txt`** (new) — `path :: line-substring` format; one entry for the only existing prose mention (`shared/epistemic.py` line 37 "Forbidden in new code: GovernanceDecision, Authority*"). Header forbids allowlisting identifiers.
- **`code/ci/__init__.py`** (new) — makes `ci` importable (`python -m ci.gate_*`; tests import via pyproject `pythonpath = ["."]`).
- **`code/ci/README.md`** (new) — gate table, local run commands, allowlist policy, and the per-gate forced-failure (red-proof) procedure for the EM.
- **Tests** (new): `code/tests/positive/ci/{__init__.py,test_gate_contract.py,test_gate_invariants.py}` and `code/tests/negative/ci/{__init__.py,test_gate_contract.py,test_gate_invariants.py}` — 55 tests. Covers: all 8 approved ids accepted; bypass label honored (incl. among other labels); missing/invalid/lowercase/partial/glued ids rejected; bypass label in body text (not on PR) rejected; CLI exit codes both ways incl. env-var path; clean tmp tree passes; **real repo tree passes**; allowlisted prose passes; allowlist for the wrong file does NOT exempt; token + authority-dir + bad-SQL detection; lawful decision-#4 DDL (REVOKE/GRANT/TRIGGER/dollar-quoted function) passes; mutations on non-canonical tables pass; missing AND empty migrations dir pass; aggregate count.

### Commands run (real results)

```
cd code && /tmp/oslo-ci-venv/bin/python -m pytest tests/positive/ci tests/negative/ci -v
  → 55 passed in 0.07s
/tmp/oslo-ci-venv/bin/ruff check ci tests/positive/ci tests/negative/ci   → All checks passed!
/tmp/oslo-ci-venv/bin/ruff check .  (whole code/, gate-1 parity)          → All checks passed!
python -m ci.gate_invariants (real tree)                                  → PASS, exit 0
PR_BODY="" PR_LABELS='["phase-1-infra"]' python -m ci.gate_contract       → BYPASS, exit 0
PR_BODY="nothing" PR_LABELS="[]" python -m ci.gate_contract               → FAIL, exit 1
pyyaml safe_load of app-ci.yml                                            → parses; on/paths/13 steps verified
git diff --stat                                                           → empty (no tracked file modified)
```

- `python3 -m pip install --user pytest` failed (PEP 668 externally-managed homebrew Python 3.14: "externally-managed-environment … pass --break-system-packages"). Per the no-global-install rule I instead created an **ephemeral venv** `/tmp/oslo-ci-venv` (pytest 9.0.3, ruff 0.15.17, pyyaml — pyyaml used only to validate the workflow YAML locally; nothing added to the project). Nothing installed globally.

### Deviations / assumptions (for EM)

1. **Gate 2 skipped on `push` events** (`if: github.event_name == 'pull_request'`): push-to-main has no PR body/labels in the event payload. The gate runs on every PR; merge to main is gate-7 (branch protection) controlled. Alternative (resolving the PR via API on push) needs extra permissions/API calls — escalating rather than inventing.
2. **`code/frontend` has no `package-lock.json`** → `npm ci` AND `npm audit` will fail in CI until a lockfile is committed (`npm install` once, commit the lock). Frontend is outside my owned files; not touched. EM action required before the workflow can go green.
3. **gitleaks-action@v2** needs `GITLEAKS_LICENSE` secret only for org-owned repos; free for user-owned repos. If this repo is org-owned, EM adds the secret.
4. **Migration linter scope is exactly the spec'd four verbs** — `TRUNCATE` (also destructive) is NOT linted because decisions #8 lists only UPDATE/DELETE/DROP TABLE/ALTER TABLE. Flagging, not adding (anti-assumption). Dollar-quoted function bodies are stripped, so a mutation hidden inside a plpgsql body would evade the static lint — gate 7 human review backstops; noted in the script docstring.
5. **`authority` dir check is case-insensitive** (`Authority/` also fails) — strictly more protective than the literal spec.
6. CI uses Python 3.12 (pyproject `requires-python >=3.11`; local dev machine runs 3.14 — both fine for these scripts).

### Could not verify

- Actual GitHub Actions execution (gitleaks step, pip-audit network resolution, path-filter behavior) — not runnable locally. Workflow YAML validated with pyyaml; gate scripts fully unit-tested. The EM red-proof procedure in `code/ci/README.md` doubles as the live verification script.
- `pipx run pip-audit .` project-mode audit assumes pip-audit ≥2.4 (pipx pulls latest on the runner) — expected fine; verify on first run.

### FIX-1 report

**Date:** 2026-06-12. **Scope:** gate-1 frontend scaffold defects (EM review note FIX-1).

Files touched (owned set only):

- `code/frontend/package.json` — added devDependencies `@types/react: ^18` and `@types/react-dom: ^18`; no other changes (diff: 2 insertions).
- `code/frontend/index.html` — created minimal Vite entry: `<!doctype html>`, `<div id="root">`, `<script type="module" src="/src/main.tsx">`, title "OSLO". No styling.
- `code/frontend/package-lock.json` — regenerated via `npm install --no-audit --no-fund`.
- This task file (this report).

Verification (real output):

- `npm install --no-audit --no-fund` → `added 2 packages, and changed 1 package in 1s` (lockfile consistent with edited package.json).
- `npm run build` (`tsc -b && vite build`) → exit 0. tsc clean (TS7016 resolved); vite: `✓ 76 modules transformed … dist/index.html 0.32 kB, dist/assets/index-BwLQm-b-.js 171.19 kB │ gzip: 54.23 kB ✓ built in 395ms`.
- `npm audit --omit=dev --audit-level=high` → `found 0 vulnerabilities`, exit 0 (gate-6 parity).

Constraints honored: no version bumps of existing deps, no other dependency changes, no app-code edits beyond index.html creation, `tsconfig.json` untouched (no change needed), nothing committed/pushed.

Pre-existing untracked artifacts noted, not touched (outside owned set): `code/frontend/src/main.js` (stale compiled emit of main.tsx) and `code/frontend/tsconfig.tsbuildinfo` — flagging for EM; `src/main.js` is shadow-artifact risk if ever resolved instead of `main.tsx`.

## Engineering-manager review notes

**Review 1 (2026-06-12):** Independently verified: 55/55 tests pass; gate scripts behave
both ways on the real tree (invariants PASS exit 0; contract valid→0 / invalid→1 with
correct guidance text); scope clean (only owned files + this report touched);
doc-integrity.yml untouched; workflow injection-safe (PR body via env), gate order per
Deployment Governance §4. Quality good — statement-aware linter, allowlist policy sound.

**Gap (FIX-1, reassigned to worker, scope expanded):** gate-1 frontend is red — baseline
scaffold defects (EM's pre-deep-task scaffold, not worker error): missing
`@types/react`/`@types/react-dom` devDeps, missing `index.html` vite entry, no
`package-lock.json`. Owned files for FIX-1 expand to: `code/frontend/package.json`
(devDeps only), `code/frontend/package-lock.json`, `code/frontend/index.html`.

**Accepted residuals:** CTE-wrapped mutations (`WITH … UPDATE`) evade the `^UPDATE` linter
match — gate-7 human review backstops, documented in script. `TRUNCATE` not linted
(decisions #8 lists four verbs; anti-assumption — escalate to owner with DTM-0002).
Gate 2 skipped on push events (PR-gated merges make this safe). gitleaks license secret
needed only if repo becomes org-owned. Live workflow run verifiable only on GitHub —
red-proof procedure documented in `code/ci/README.md` for the EM to execute on first PR.

## Approved by engineering manager

Status: Approved

Executive summary:
- Six-gate app CI (`.github/workflows/app-ci.yml`, path-filtered `code/**`) with gate
  logic in unit-testable scripts (`code/ci/gate_contract.py`, `gate_invariants.py`),
  allowlist policy, red-proof procedure (`code/ci/README.md`), and 55 tests across
  positive+negative suites. FIX-1 closed the frontend build gap (`@types/react{,-dom}`
  devDeps, `index.html` vite entry, lockfile). EM additionally set tsconfig `noEmit`
  (stops source-adjacent tsc emit) and gitignored `*.tsbuildinfo`.

Verification:
- `pytest tests/positive/ci tests/negative/ci` → **55 passed** (run independently by EM).
- `python -m ci.gate_invariants --code-root .` on real tree → PASS exit 0.
- `gate_contract`: valid id → exit 0; no id → exit 1 (correct guidance); `phase-1-infra` → bypass.
- `npm install && npm run build` → tsc clean + vite ✓ 76 modules, exit 0 (EM re-ran post-noEmit).
- `npm audit --omit=dev --audit-level=high` → 0 vulnerabilities.
- Scope: only owned files + task report touched; `doc-integrity.yml` untouched.

Manual test plan:
- Open the first PR on `feat/phase1-wavea-00r` with label `phase-1-infra` → workflow runs, all gates green.
- Execute the per-gate red-proof from `code/ci/README.md` (one throwaway commit each) → each gate red exactly once.

Remaining risks:
- Live GitHub run not yet executed (local-only verification); red-proof pending first PR.
- CTE-wrapped SQL mutations evade the static linter (gate-7 review backstops; documented).
- `TRUNCATE` unlinted — escalate to owner alongside DTM-0002 (anti-assumption).
- gitleaks needs `GITLEAKS_LICENSE` only if the repo moves to an org.
