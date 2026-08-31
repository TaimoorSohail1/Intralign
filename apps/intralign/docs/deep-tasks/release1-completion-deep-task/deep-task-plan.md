# Deep-task plan — Release 1 completion (every layer → 100% live)

Vertical slices on `feat/release1-completion`. One fresh worker per task, EM review→fix→verify→
approve→commit between. Goal: the app is **live, persistent, write-capable, authenticated,
deployable** — surfaces show real data, users can act (create/analyze/accept/chat), and writes
persist. **Three slices are OWNER-gated** (migration / auth / deploy) — authored but coding stops
pending owner approval.

## Slices (dependency-ordered)

| # | Module | Slice (vertical outcome) | Gate | Source | Depends |
|---|---|---|---|---|---|
| 1 | **DTM-0030** | **Projection materializer** — a `mark_current` orchestration step upserts the `derived.*_current` row (current_payload + epistemic envelope + current_chr_ref) from each appended CHR, per LDM §3.1. Read surfaces show LIVE data; rebuildable from CHRs. No new migration. | ungated | LDM §3.1; Event Model §8 | — |
| 2 | **DTM-0031** | **Platform persistence** — migrations for `project`, `analysis_run`, `notification` tables (additive) + `backend/platform` repos + wire the read seam to real tables. | **OWNER (migration)** | LDM §6; API §5; Deployment §5 | — |
| 3 | **DTM-0032** | **REST: analysis triggers** — `POST …/analysis-runs:fast` / `:deep` / `POST /analysis-runs/{id}:cancel` → `submit_trigger`; AnalysisRun lifecycle + `fast/deep_analysis_requested` events. | after 0031 | API §5 (122–124); Event §8.8 | 0031 |
| 4 | **DTM-0033** | **REST: acceptance** — `POST /recommendations/{id}:accept|:reject|:defer|:implement` → `record_acceptance` (version-pinned UAR + plan fact); `recommendation_accepted/…` events. Wires the DTM-0022 affordance. | ungated (UAR table exists) | API §5 (140–143); DL-055 | — |
| 5 | **DTM-0034** | **REST: project CRUD + intake** — `POST /projects`, `PATCH /projects/{id}`, `:archive`; `POST …/evidence`, `…/artifacts`(+versions) → intake/promotion. | after 0031 | API §5 (98–116) | 0031 |
| 6 | **DTM-0035** | **REST: finding lifecycle + notification state** — `POST /findings/{id}:acknowledge|:address|:reopen`; `POST /notifications/{id}:view|:dismiss` (platform state, non-canonical). | after 0031 | API §5 (130–132); catalog 78–79 | 0031 |
| 7 | **DTM-0036** | **Auth seam** — implement `current_principal`: verify the Supabase-JWT (sig/exp/claims) → `Principal(user_id, workspace_id, role)`; workspace-scoping + RBAC. | **OWNER (security/dep)** | API §3; Runtime Env §4 | — |
| 8 | **DTM-0037** | **OSLO Chat backend** — `ChatSession`/`ChatExchange` (non-canonical) + `POST …/chat` (send → exchange; Improve → `submit_trigger` Deep-Pass); `ChatExchange` events. No canonical write. | ungated | DL-047; Wave I OBS | 0030 |
| 9 | **DTM-0038** | **Read-shape additions** — first-class Issue DTO + `GET …/issues`; aggregate counts/overview DTO; unified CHR history feed. Frontend swaps the Wave E placeholders to the real reads. | ungated | API §5; LDM §2–3 | 0030 |
| 10 | **DTM-0039** | **Frontend write-wiring** — wire the surface affordances to the new commands: Recommendation accept/reject/defer → 0033; Chat send/Improve → 0037; Notification dismiss → 0035; analysis trigger + project create → 0032/0034. Replace the DTM-0022/0026/0029 hand-off/local stubs with real mutations (TanStack `useMutation`). | after cmds | API §5; the Wave E flags | 0032–0035,0037 |
| 11 | **DTM-0040** | **DL-048 token-budget enforcement** — verify/complete the per-tier spend-gate + `AI Spend Recorded` telemetry + QA gate (numbers = DL-048 defaults, not invented). | ungated | DL-048; OPEN_TBD A6 | — |
| 12 | **DTM-0041** | **Env binding / staging deploy prep** — docker-compose for backing services (Supabase/Neo4j/Redis), env config (`.env` keys, no secrets committed), Heroku/Vercel binding, staging. Production stays owner-only. | **OWNER (deploy)** | Deployment §2–7; Runtime Env | all |
| 13 | **DTM-0042** | *(optional, deferrable)* Collaboration commands — comments / shares / reports (Category-E commodity). | deferrable | API §5 (149–166) | 0031 |

> Owner-gated slices (0031, 0036, 0041) are authored just-in-time and **coding STOPS pending owner
> approval** (migration / security / deploy). The rest proceed on the user's authorization.

## Test strategy

- **Materializer (0030):** pos — after a run, `derived.*_current` holds the latest CHR's payload +
  envelope; re-run supersedes (new current_chr_ref), append-only CHR preserved; neg — materializer
  writes NO canonical row, mutates no CHR, never promotes Derived→Attested. Live e2e: run → read
  surface shows data.
- **Command endpoints (0032–0035, 0037):** pos — each command wires the existing seam, returns the
  affected resource + emits the §8 event, idempotent on `Idempotency-Key`, workspace-scoped; neg —
  unauth 401, cross-workspace 404, invalid state transition 409, **OSLO never self-accepts** (accept
  is user-initiated), **Chat writes no canonical** (Critical), notification state non-canonical.
- **Auth (0036):** pos — valid token → Principal; neg — bad sig/exp/claims → 401; cross-workspace
  isolation.
- **Frontend wiring (0039):** the surface affordances now persist (useMutation) + invalidate the
  read; the epistemic-safety negatives stay green (no Disclose-side cognition).
- **Gates every slice:** ruff + gate-3 (pos+neg) + gate-4 (invariants) + gate-5 (obs vocab/CHR
  pairing — new events added) + frontend build/vitest/playwright + drift + audit. Determinism tiers
  per Calibration. No baseline regression.

## Manual checks (EM / owner)

- End-to-end live (no seed harness): create project → add evidence → trigger analysis → surfaces
  show findings/confidence/CAF → accept a recommendation (UAR + plan fact persisted, History shows
  it) → chat Explain/Improve → notification dismiss persists. Auth: a real token scopes to the
  workspace; cross-workspace blocked.

## Done = Release 1 100% (every layer live)

Surfaces show live materialized data; users create/analyze/accept/chat/dismiss and it persists;
auth scopes the workspace; the command endpoints emit the §8 events and append CHRs/UARs correctly;
all gates green; deploy config staged. → **Owner production-readiness review + production deploy
(owner-only).**
