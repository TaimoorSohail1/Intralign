# Deep-task decisions — Release 1 completion (every layer → 100% live)

Implementation-control record for the **completion phase**: take the app from "cognition + read +
presentation built" to **live, persistent, write-capable, authenticated, deployable**. Cites
source-of-truth; does not restate it. **Branch:** `feat/release1-completion` (new, off the current
stack HEAD — created at execution start; keeps the Wave E branch PR-able).

## Source-of-truth docs (binding; read, do not edit from deep-task)

- **API Contract (every WRITE op):** `20_handoff/interfaces/RELEASE_1_API_CONTRACT_SPECIFICATION_V1.md`
  §5 (lines ~98–166) + `API_CONTRACT_ENDPOINT_CATALOG.md` — POST/PATCH paths, request/response,
  `Idempotency-Key`, workspace-scoping, the emitted event names. §3 (auth/scoping/RBAC), §9
  (errors), §10 (idempotency).
- **Logical Data Model:** `30_engineering/runtime_models/RELEASE_1_LOGICAL_DATA_MODEL_V1.md` — §2
  canonical (Attested/CHR/UAR/PlanFact/History, append-only), **§3.1 Live Cognition Projection**
  (the `derived.*_current` row shape + "recompute appends CHR → projection updated in sync;
  rebuildable from latest CHR"), §5 lifecycle rules, §6 physical binding (Supabase/Neo4j/Redis).
- **Event Model / OBS:** `RELEASE_1_EVENT_MODEL_SPECIFICATION_V1.md` §8 (the write-path events:
  `fast/deep_analysis_*`, `recommendation_accepted/rejected/deferred/implemented`,
  `finding_acknowledged/…`, `notification_viewed/dismissed`, `project_created/…`) + the wave OBS
  contracts + `00_owner/build_governance/OBSERVABILITY_GOVERNANCE_SPECIFICATION_V1.md`.
- **Auth / env / deploy:** `30_engineering/environment/RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1.md`
  §4 (Supabase Auth/GoTrue + RLS, RBAC) + `00_owner/build_governance/DEPLOYMENT_GOVERNANCE_SPECIFICATION_V1.md`
  (§4 CI gates, §5 migration discipline, §9 agent STOP conditions) + DL-054.
- **Governance:** `00_owner/ANTI_ASSUMPTION_BUILD_PROTOCOL.md`; `code/CLAUDE.md` "Human approval
  REQUIRED" + STOP rules; `00_owner/OPEN_TBD_REGISTER.md` (A3/A4/D1 latency+tolerance still TBD —
  do not invent). DL-043/044/046/047/048/054/055/069.

## Repo facts — what's DONE vs MISSING (from the code + docs scan)

**DONE (build on, don't redo):**
- Cognition engines (Perceive/Retain/Infer/Evaluate/Advise/Acceptance) + orchestration runner
  (`backend/orchestration/runner.py` `submit_trigger`+`run`, durable Supabase checkpointer; A→B→C→U
  chains composed). `record_acceptance` (`responsibilities/retain/acceptance.py`) writes UAR +
  plan fact (version-pinned). CHR repo + retention store (Supabase, append-only). Migrations for
  **canonical** tables (`attested_assertion`, `cognition_history_record`, `user_acceptance_record`,
  `history_record`) + the **8 `derived.*_current` projection tables** + intake — all exist
  (`code/supabase/migrations/`). REST **read** surface + render DTOs (DTM-0018). Frontend: shell +
  10 surfaces (DTM-0019–0029).

**MISSING (the gaps to 100%):**
1. **Projection materializer** — NOTHING writes `derived.*_current`. The cognition stages append
   CHRs only; `mark_current` does not upsert the projection rows the render `ProjectionReader`
   reads. ⇒ surfaces are empty even live. (LDM §3.1: recompute appends CHR → projection updated in
   sync.) **The critical unblocker.**
2. **REST write/command endpoints** — every router is GET-only (DTM-0018). API Contract §5
   specifies: project CRUD, analysis-run triggers (`:fast`/`:deep`/`:cancel`), acceptance
   (`recommendations/{id}:accept|reject|defer|implement`), finding lifecycle
   (`:acknowledge|address|reopen`), notification state (`:view|:dismiss`), evidence/artifact intake,
   collaboration (comments/shares/reports). None built.
3. **Platform persistence** — `backend/platform/` is a 1-line stub; `project`/`analysis_run`/
   `notification` tables are NOT migrated (read seam references them). Needs migrations + repos.
4. **Auth seam** — `api/deps.py` `current_principal` raises 401 unconditionally (Supabase-JWT verify
   not wired).
5. **OSLO Chat backend** — `ChatSession`/`ChatExchange` are canonical-vocab placeholders only; no
   module/endpoint (DL-047).
6. **Read-shape gaps** — no first-class Issue DTO/`GET …/issues`, no aggregate counts/overview DTO,
   no unified CHR history feed (Wave E surfaces flagged these).
7. **Env binding / deploy** — backing-service wiring (docker-compose), env config, staging.
   Production is owner-only.
8. **DL-048 token-budget enforcement** — the spend-gate mechanism (verify present/complete).

## Governance gates (per `code/CLAUDE.md` + Deployment Governance §9 — FLAG, do not bypass)

- **OWNER-APPROVAL REQUIRED (STOP before coding the migration/seam):**
  - **Any new migration** — DTM platform tables (`project`/`analysis_run`/`notification`) +
    any schema. Canonical tables stay append-only; platform tables additive. Owner ratifies.
  - **Auth seam** (Supabase-JWT verify) — security seam; may need a verify dependency + secrets.
  - **Env binding / production deploy** — production is human-only; staging Claude-proposes.
  - **LLM routing** — unchanged (gemma primary, DL-069) — do not alter.
- **WITHIN-CONTRACT (buildable once the gate above clears / no new migration):** the projection
  materializer (derived tables exist), the acceptance command (UAR table exists), read-shape DTOs,
  frontend write-wiring, chat (non-canonical). Each cites its API-Contract-§5 / LDM clause.
- **Epistemic invariants hold throughout:** recompute appends (materializer upserts the DERIVED
  projection only, never mutates a CHR/canonical row); no Derived→Attested; OSLO never self-accepts
  (acceptance is user-initiated via the command → `record_acceptance`); no Authority engine.

## Locked decisions (apply across slices)

1. **One fresh worker per slice, strictly sequential**; EM review→fix→verify→approve→commit between.
2. **Projection materializer FIRST (DTM-0030)** — it unblocks live data for every surface and the
   read tests, with no new migration.
3. **Owner-gated slices (DTM-0031 migration, 0036 auth, 0041 deploy) are authored now but coding
   STOPS pending explicit owner approval.** The ungated slices (0030, 0033, 0037, 0038, 0039) can
   proceed on the user's authorization.
4. **Every write endpoint follows API Contract §5 verbatim:** path/method (incl. the `:action`
   command syntax), `Idempotency-Key`, workspace-scoping via `deps.py`, returns affected resource +
   emits the §8 event name. Wire to the EXISTING seams (`submit_trigger`, `record_acceptance`,
   intake) — invent no new ownership.
5. **Write endpoints are a separate concern from the read surface** — additive routers; the
   read-surface read-mostly negatives (DTM-0018) stay green (writes live on their own command
   routers).
6. **No invented numerics** — latency targets (A3/A4) + determinism tolerance (D1) are TBD on the
   OPEN_TBD register; do not invent. Use the owner-confirmed values only (Tier-1 envelope, DL-048
   budgets, WCAG AA, Intralign).
7. **Gates stay green** — gate-2 (contract id in PR), gate-3 (pos+neg), gate-4 (invariants), gate-5
   (obs vocab + CHR-append pairing), gate-6 (audit/secrets). New events → gate-5 vocab updates.

## Packages / refactors

- **Likely a new backend dependency for the auth seam** (a Supabase/JWT verify lib) — **owner
  approval required** (STOP rule #4). Flag in DTM-0036; do not add silently.
- Materializer + command routers + platform repos are additive; no refactor of frozen cognition/
  orchestration topology (compose by calling existing builders, like the wave chains do).

## Open items / residuals

- **Phase VI implementation README is stale** ("Wave E: Not started") — Wave E is built (DTM-0019–
  0029). Not edited from deep-task; flag to owner to update the implementation index.
- Collaboration (comments/shares/reports) is API-Contract-specified but **Category-E commodity** —
  scoped as an OPTIONAL late slice (DTM-0042), deferrable from the R1 critical path.
- A3/A4 latency + D1 tolerance numbers remain owner-TBD (do not block; enforcement structure builds
  without the exact numbers).

## Slice index (see deep-task-plan.md for detail)

| Task | Scope | Gate | File |
|---|---|---|---|
| DTM-0030 | Projection materializer (`derived.*_current` upsert in `mark_current`) | ungated | `deep-task-0030.md` |
| DTM-0031 | Platform persistence — `project`/`analysis_run`/`notification` migrations + repos | **OWNER (migration)** | authored next |
| DTM-0032 | REST command: analysis triggers (`:fast`/`:deep`/`:cancel`) → submit_trigger | after 0031 | — |
| DTM-0033 | REST command: acceptance (`recommendations:accept/reject/defer/implement`) → record_acceptance | ungated | — |
| DTM-0034 | REST command: project CRUD + evidence/artifact intake | after 0031 | — |
| DTM-0035 | REST command: finding lifecycle + notification state | after 0031 | — |
| DTM-0036 | Auth seam — Supabase-JWT verify in `current_principal` | **OWNER (security)** | — |
| DTM-0037 | OSLO Chat backend (ChatSession/ChatExchange + send/trigger, DL-047) | ungated | — |
| DTM-0038 | Read-shape additions — Issue DTO/`GET issues`, counts/overview, CHR history feed | ungated | — |
| DTM-0039 | Frontend write-wiring — surface affordances → the new command endpoints | after cmds | — |
| DTM-0040 | DL-048 token-budget enforcement (verify/complete the spend-gate) | ungated | — |
| DTM-0041 | Env binding / staging deploy prep (compose, config) | **OWNER (deploy)** | — |
| DTM-0042 | (optional) Collaboration commands — comments/shares/reports (Category-E) | deferrable | — |
