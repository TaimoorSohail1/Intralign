# DTM-0036 — Auth seam (Supabase-JWT verify in current_principal)

**Status:** In progress — OWNER-APPROVED (auth seam + verify dep) 2026-06-26 · **Module:** DTM-0036
· **Phase:** Completion · **Contract:** API §3 (auth/scoping/RBAC) + Runtime Env §4 (Supabase Auth/
GoTrue + RLS) · **Depends:** `api/deps.py`. **Branch:** `feat/release1-completion`.

## Goal / observable behavior

`current_principal` actually verifies the caller's token. It extracts the bearer JWT, **verifies
signature + expiry** (Supabase Auth / GoTrue), and resolves it to `Principal(user_id, workspace_id,
role)` — workspace-scoped (single workspace per user in R1) with RBAC (owner/admin/member). A valid
token → Principal; bad signature/expiry/claims → 401. The test-override pattern
(`app.dependency_overrides[current_principal]`) is preserved (every command/read test still injects a
fixed Principal). The real signing secret is env-injected (no secret in repo).

## Source docs / constraints

- API §3 (51–59) — bearer token identifies user_id; resolves the single workspace_id; tenant
  isolation; RBAC owner/admin/member; **no SSO/enterprise auth in R1**. Runtime Env §4 — Supabase
  Auth (GoTrue) + RLS; the platform RBAC model. Deployment Governance §7 — **no secret in repo**;
  secrets via the platform store; Claude never prints/commits a secret. `code/CLAUDE.md` STOP #4
  (new dependency → owner approval — PRE-APPROVED for the auth verify lib; still flag the exact lib).
- Code: `backend/api/deps.py` `current_principal` (the stub raising 401) + `Principal`; the Supabase
  client (`backend/services/persistence/client.py` — does the Supabase SDK already expose a verify?
  prefer reusing it to avoid a new dep); how workspace_id/role are carried (a JWT custom claim /
  app_metadata, or a users/profiles lookup — ground it; if neither exists ⇒ flag).

## Locked decisions (do not re-derive)

- **Verify dependency (PRE-APPROVED, flag the exact one):** prefer **reusing the existing Supabase
  client's JWT verification** if available (no new dep). Else add **one** standard verify lib
  (PyJWT for HS256 with the Supabase JWT secret is the conventional choice) — name it in the report;
  the EM confirms before it's locked. **No secret committed** — the secret is read from env
  (`SUPABASE_JWT_SECRET` or equivalent), with a clearly-commented `.env.example` placeholder.
- **Claims → Principal:** `sub` → user_id; workspace_id + role from the token's app_metadata/custom
  claim per the Supabase Auth model. If workspace_id/role are NOT in the token, resolve via a
  users/profiles lookup (and flag whether that table exists — STOP if it requires an un-approved
  migration; the owner approved the auth seam, not necessarily a new users table — confirm).
- **Test-override preserved:** the dependency stays overridable; existing tests inject a fixed
  Principal unchanged. Add unit tests that sign a JWT with a test secret and verify the real path
  (valid → Principal; tampered/expired/missing-claim → 401).
- Workspace scoping + RBAC unchanged in behavior (the routers already use Principal). No change to
  the command/read routers.

## Owned files / boundaries

- **OWN:** `backend/api/deps.py` (`current_principal` impl) + maybe a small `backend/platform/auth.py`
  (verify helper) · `.env.example` (placeholder) · `pyproject.toml` ONLY if a verify dep is added
  (flagged) · `tests/{positive,negative}/api/test_auth*.py`.
- **READ-ONLY:** the routers (they consume Principal — unchanged), cognition, migrations (do NOT add
  one without a separate flag).

## Packages / refactors

- Possibly **one** new dep (verify lib) — PRE-APPROVED in principle; the worker names it + the EM
  confirms. No other dep.

## Implementation instructions (TDD)

1. Red (pytest): a JWT signed with a test secret + valid claims → `Principal(user_id, workspace_id,
   role)`; **negatives:** missing/blank bearer → 401; bad signature → 401; expired → 401; missing
   required claim → 401; cross-workspace still 404 at the router (unchanged). The existing
   dependency-override tests still pass (override unchanged).
2. Implement `current_principal` (reuse Supabase verify if possible; else the flagged lib + env
   secret); map claims → Principal; `.env.example` placeholder.

## API / data / schema contracts

- No API shape change (Principal is internal). No schema change (flag if a users table is needed).

## Test plan

- **Positive:** valid token → Principal (user_id/workspace_id/role); RBAC role surfaced.
- **Negative:** missing/blank/tampered/expired/missing-claim → 401; override path intact.
- `.venv/bin/pytest` + ruff + gate-4 + gate-5 + **gate-6 (secret scan — no secret committed)** green.

## Manual checks (EM)

- With a dev `SUPABASE_JWT_SECRET`, a hand-signed token authenticates and scopes to its workspace;
  no token / bad token → 401; `.env.example` documents the var (placeholder only).

## Done criteria

- `current_principal` verifies the Supabase JWT (sig/exp/claims) → Principal, workspace-scoped + RBAC,
  test-override preserved, secret env-injected (none committed), the verify dep (if any) flagged +
  EM-confirmed, gates incl. gate-6 green. PR cites API §3. Ready for DTM-0037.

## Worker report

**Status: Ready for review.**

### ⚠️ DEPENDENCY — NO NEW TRANSITIVE ADDED (EM please confirm)

Verify lib = **PyJWT** (`pyjwt[crypto]>=2.12`), declared explicitly in `pyproject.toml`.
**This is NOT a new dependency to the resolved environment:** `supabase>=2.5` (already
in the ratified stack) pulls it transitively — `supabase_auth-2.31.0` declares
`Requires-Dist: pyjwt[crypto]>=2.12.0`, and `jwt`/`pyjwt-2.13.0` are already present in
`.venv`. I declared it as a **direct** dependency (best practice: app code now imports
`jwt` directly, so it should not rely on a transitive). No other dependency added. The
PRE-APPROVED "one verify lib" allowance is therefore satisfied with zero net new install.

### Verify approach (reused Supabase vs named lib)

Considered the Supabase SDK's own verification first, as instructed. The SDK path is
`supabase_auth.SyncGoTrueClient.get_user(jwt)` — but that **validates via a network
round-trip to the GoTrue Auth server**, requiring a live Supabase instance + network on
every request, which is unsuitable for the read/command hot path and for offline CI. The
conventional Supabase server-side approach is **offline HS256 verification of the access
token against the project JWT secret** — done here with PyJWT (which already ships with
`supabase`). Offline, deterministic, unit-testable, no extra network/credential at request
time.

### Claims → Principal mapping

`backend/platform/auth.py::verify_token` (HS256, `audience="authenticated"`,
`options={"require": ["exp", "sub"]}`):
- `sub` → `Principal.user_id`
- `workspace_id` → `Principal.workspace_id` (custom claim; read from `app_metadata` first,
  top-level accepted as a fallback)
- `role` → `Principal.role` (read from `app_metadata` **first** — see flag — restricted to
  `{owner, admin, member}`)

`backend/api/deps.py::current_principal` extracts the bearer, calls `verify_token`, and maps
the result to `Principal`. Any `AuthError` → one `401 unauthenticated` (the verifier never
leaks *why*).

### workspace_id / role resolution + FLAG

Per the Supabase Auth model, `workspace_id` + RBAC `role` are **custom claims in
`app_metadata`** (GoTrue copies `app_metadata` into the issued access token). **No new
users/profiles table was added** — none is required because the scope/role travel in the
token (the auth seam, as approved; no un-approved migration).

- **FLAG 1 (deployment requirement, not a code gap):** the deployment must mint these custom
  claims into `app_metadata` — typically via a Supabase **Auth Hook / custom-access-token
  hook** (or admin `app_metadata` assignment) so each user's single `workspace_id` + RBAC
  `role` are present. If a future iteration prefers a DB-backed `profiles` lookup instead,
  that is a **separate, owner-approved migration** (out of scope here).
- **FLAG 2 (intentional precedence):** Supabase reserves the top-level `role` claim for the
  Postgres role (`authenticated`). The application RBAC role therefore reads from
  `app_metadata.role` **first** so it is not shadowed by the reserved value. Covered by
  `test_app_metadata_role_wins_over_reserved_top_level_role`.

### Env var + `.env.example` placeholder

Secret read from env `SUPABASE_JWT_SECRET` (`backend/platform/auth.py`). `.env.example` gains
a clearly-commented **empty placeholder** (`SUPABASE_JWT_SECRET=`) documenting the var, its
source (`supabase status` locally / platform secret store in staging+prod, Deployment
Governance §7). **No secret value is committed, printed, or hardcoded** anywhere — only the
env-var *name* string and an empty placeholder.

### Secret committed? users-table migration needed?

- **Dependency added?** PyJWT, declared explicitly — but **already transitively present via
  `supabase`; zero net new install** (see flag above).
- **Any secret committed?** **NO.** `.env.example` placeholder is empty; the only string
  literals are the env-var name and a low-entropy ephemeral **test** secret in the test files
  (descriptive English phrase — not a credential). Confirmed by inspection (no local
  `gitleaks` binary available).
- **Users-table migration needed?** **NO** for this slice (scope/role from token claims). A
  DB-backed `profiles` lookup would be a separate owner-approved migration — flagged, not
  done.

### Files changed

- **NEW** `backend/platform/auth.py` — `verify_token` / `extract_bearer` / `AuthError` /
  `VerifiedClaims` (offline HS256 verify + claims extraction).
- `backend/api/deps.py` — `current_principal` now extracts + verifies the bearer and maps
  claims → `Principal`; module docstring updated. **Override mechanism unchanged.**
- `.env.example` — `SUPABASE_JWT_SECRET=` placeholder (empty, commented).
- `pyproject.toml` — explicit `pyjwt[crypto]>=2.12` (see dependency flag).
- **NEW** `tests/positive/api/test_auth_seam.py`, `tests/negative/api/test_auth_seam_negatives.py`.

### Exact verify commands + results

```
$ .venv/bin/pytest tests/positive tests/negative -q
706 passed, 65 skipped, 3 warnings in 3.44s
```
(All pre-existing command/read tests still pass with the unchanged dependency-override; the
20 new auth tests pass. Trailing OTLP "Failed to export traces" lines are background
observability noise, not test failures.)

```
$ .venv/bin/ruff check .
All checks passed!

$ .venv/bin/python ci/gate_invariants.py        # gate-4
[gate-4 epistemic-invariant] PASS: no forbidden tokens, no authority module, no canonical-table mutations in migrations.

$ .venv/bin/python ci/gate_observability.py     # gate-5
[gate-5 observability] PASS: ...
```

Gate-6 (gitleaks): no local binary; confirmed by inspection that no secret value is
committed (empty placeholder; only the env-var name + an ephemeral test phrase). `git diff`
of tracked files + the two new test files reviewed — clean.

### 401 negatives proven

Verifier-level (`AuthError`) and HTTP-level (`401`): bad signature, expired, wrong audience,
tampered token, missing `sub`/`workspace_id`/`role`, unrecognised role, secret-not-configured;
HTTP: missing bearer, blank bearer, non-`Bearer` scheme, bad-sig, expired, missing-claim. Plus
`test_dependency_override_authenticates_without_a_token` proves the override path is intact.

**Not committed — changes staged for review (unrelated working-tree changes preserved).**

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_

## Approved by engineering manager

Status: Approved

Executive summary:
- `current_principal` now verifies the Supabase JWT offline (HS256 against the env `SUPABASE_JWT_SECRET`,
  `audience="authenticated"`, require exp+sub) → `Principal(user_id, workspace_id, role)`. New
  `backend/platform/auth.py` verify helper; claims from `app_metadata`. Test-override path intact.
  API §3 / Runtime Env §4.

Dependency (EM-confirmed): `pyjwt[crypto]>=2.12` declared direct — **already a transitive of
`supabase`** (in the ratified stack; pyjwt 2.13.0 present in `.venv`), so zero net-new install;
owner pre-approved the verify dep. Standard, conventional choice. Accepted.

Verification (EM re-ran): `.venv/bin/pytest` → **706 passed, 65 skipped** (20 new; all existing
override tests green — the test seam is untouched). ruff clean; gate-4 PASS; gate-5 PASS. No secret
committed (`.env.example` `SUPABASE_JWT_SECRET=` empty placeholder; no gitleaks locally — confirmed
by inspection). No migration.

Negatives proven (→401): missing/blank/non-Bearer; bad signature; expired; wrong audience; tampered;
missing sub/workspace_id/role; unrecognised role; secret-not-configured.

Remaining risks / flagged (deployment, not code):
- Deploy must mint `workspace_id` + RBAC `role` into `app_metadata` via a Supabase custom-access-token
  Auth Hook (documented in `.env.example` + report) — wired in DTM-0041.
- A DB-backed `profiles` lookup (if claims-in-token is later rejected) would be a separate
  owner-approved migration — not needed now (scope/role travel in the token).
- gate-6 (gitleaks/npm-audit) runs in CI; no secret in the diff (verified by inspection locally).
