# DTM-0039 — Frontend write-wiring (surface affordances → the command endpoints)

**Status:** In progress · **Module:** DTM-0039 · **Phase:** Completion · **Contract:** API §5 + the
Wave E surface flags · **Depends:** DTM-0032–0038 (the commands + new reads). **Branch:**
`feat/release1-completion`.

## Goal / observable behavior

The UI becomes fully functional end-to-end. Regenerate the Orval client against the now-complete
OpenAPI (≈30 endpoints) and wire each surface affordance to its real command (TanStack
`useMutation` + invalidate the read):
- **Recommendation Panel (DTM-0022):** accept/reject/defer/implement → `POST /recommendations/{id}:…`
  (DTM-0033). Replace the navigation hand-off with the real mutation (Disclose still renders the
  affordance; the command records the UAR — Disclose itself never accepts).
- **OSLO Chat (DTM-0029):** send/Improve → `POST /projects/{id}/chat` (DTM-0037). Replace the
  ephemeral stub with the real exchange.
- **Notification (DTM-0026):** view/dismiss → `POST /notifications/{id}:view|:dismiss` (DTM-0035).
  Replace the local-only state with the real platform-state mutation.
- **Finding Panel/Issue Cards:** acknowledge/address/reopen → `POST /findings/{id}:…` (DTM-0035).
- **Dashboard/Overview:** create project → `POST /projects`; trigger analysis → `POST …/analysis-runs:fast|:deep`
  (DTM-0032/0034). Add evidence → `POST …/evidence`.
- **Issue Cards / Overview / History:** swap the DTM-0023/0024/0027 placeholders to the first-class
  reads (`/issues`, `/overview`, `/history` — DTM-0038).
The epistemic-safety negatives (Disclose presents, never generates; RP-C1; Derived-as-settled
impossible) stay green.

## Source docs / constraints

- API §5 (the command/read endpoints) + the Wave E surface task files (DTM-0022/0023/0024/0026/0027/
  0029 — their flagged hand-off/local stubs are what this replaces). `code/CONTEXT.md` (Disclose
  presents; the affordance routes to the user-initiated command — Disclose never accepts itself).
- Code: `frontend/orval.config.ts` + `scripts/check-openapi-drift.sh` (regen against the live
  OpenAPI — boot the backend first), the surfaces under `frontend/src/surfaces/**`, the generated
  client `frontend/src/api/generated/**` (consume the new hooks), the QueryClient (invalidate on
  mutate).

## Locked decisions (do not re-derive)

- **Regenerate the Orval client** from the backend's live `/openapi.json` (boot the app or the
  seeded dev_server on :8000, `npm run api:gen`). The drift gate (`tsc`) stays green.
- **Wire mutations, preserve the epistemic contract:** the affordance calls the user-initiated
  command (the backend writes the UAR/exchange/state); Disclose still presents + never performs
  cognition/acceptance locally. The Wave E negatives (no Disclose-side accept/generate; RP-C1;
  Derived-never-settled; Chat-no-canonical) MUST stay green — re-run them.
- **No new dependency** (TanStack Query is present; `useMutation` is built-in). Keep the Intralign
  theme + EpistemicLabel unchanged.

## Owned files / boundaries

- **OWN:** `frontend/src/surfaces/**` (wire mutations into the existing surfaces) · the regenerated
  `frontend/src/api/generated/**` (regen, don't hand-edit) · a small shared mutation/query-invalidate
  helper if needed · the surface tests (vitest) + e2e (playwright).
- **READ-ONLY:** backend, theme, EpistemicLabel internals, the router structure (RP-C1 nesting stays).

## Packages / refactors — none new.

## Implementation instructions (TDD)

1. Boot the backend (uvicorn or the seeded `scripts/dev_server.py`) on :8000; `cd frontend &&
   npm run api:gen`; run the drift gate.
2. Red (vitest): each surface's affordance calls the right generated mutation hook + invalidates the
   read (mock the hook, assert the call + the optimistic/invalidate). **Negatives:** Disclose-side
   accept/generate still impossible (the affordance calls the command, performs no local cognition);
   RP-C1 intact; Derived-never-settled; Chat sends via the endpoint (no local canonical).
3. Wire the mutations into the surfaces; swap the Issue/Overview/History placeholders to the
   first-class reads. Playwright happy-paths for the key flows.

## API / data / schema contracts

- Consumes the regenerated command + read hooks. No backend change.

## Test plan

- **Positive:** accept/reject/defer (Recommendation); chat send/Improve; notification dismiss;
  finding lifecycle; project create + analysis trigger; issues/overview/history from the new reads.
- **Negative:** the Wave E epistemic-safety negatives all stay green (no Disclose-side accept/
  generate; RP-C1; Derived-never-settled; Chat-no-canonical-local).
- `npm run build` + `vitest run` + Playwright + drift gate + `npm audit --omit=dev` green.

## Manual checks (EM)

- With the backend (seeded or live): accept a recommendation → it persists (History shows the UAR);
  chat Explain → a response; dismiss a notification → persists; create project + trigger analysis →
  surfaces fill. The epistemic labels stay correct.

## Done criteria

- The Orval client regenerated; every surface affordance wired to its real command (mutation +
  invalidate); Issue/Overview/History on the first-class reads; the Wave E epistemic-safety negatives
  green; build + vitest + playwright + drift + audit green; no new dep. PR cites API §5. Ready for
  DTM-0040.

## Worker report

**Status: Ready for review.**

### STEP 1 — client regeneration (against the live, now-complete OpenAPI)

- Booted the seeded backend on :8000 (`.venv/bin/uvicorn backend.api.app:app --port 8000`),
  regenerated the Orval client (`npm run api:gen`), ran the drift gate
  (`bash scripts/check-openapi-drift.sh` → regen + `tsc --noEmit` clean), then stopped the backend.
- The generated client now exposes **41 paths** (40 `/v1/*` + `/health`) — all the command + read
  hooks DTM-0030–0038 landed. New generated modules: `acceptance-commands`, `analysis-commands`,
  `finding-commands`, `notification-commands`, `project-commands`, `chat`, `issues`, `overview`,
  `history`. Confirmed the new hooks exist (accept/reject/defer/implement, chat, notification
  view/dismiss, finding acknowledge/address/reopen, project create, fast/deep analysis triggers,
  add-evidence, issues/overview/history reads).
- The generated client is **gitignored (regenerated, never hand-edited)** — consistent with the
  drift-gate design; re-running the gate is idempotent.

### Each surface's wiring (affordance → hook + invalidate)

| Surface | Affordance | Generated hook (DTM) | Invalidates |
|---|---|---|---|
| Recommendation Panel | accept/reject/defer/implement | `useAccept/Reject/Defer/ImplementRecommendation…Post` (0033) | finding-recs read |
| OSLO Chat | send / Explain / Clarify / Improve | `useChatV1ProjectsProjectIdChatPost` (0037) | — (non-canonical exchange; Improve triggers Deep Pass server-side) |
| Notification | mark-read / dismiss | `useView/DismissNotification…Post` (0035) | notifications read |
| Finding Panel | acknowledge / address / reopen | `useAcknowledge/Address/ReopenFinding…Post` (0035) | finding read |
| Dashboard | create project | `useCreateProjectV1ProjectsPost` (§5) | projects read |
| Project Overview | Start Fast/Deep Pass · add evidence | `useStartFast/DeepAnalysis…Post` (0032) · `useAddEvidence…Post` (0034) | analysis-runs read |

### Reads swapped to the first-class endpoints (DTM-0038)

- **Issue Cards** → `useListIssues…` (was: `useListFindings…` + client-side severity filter).
  Fixtures retyped `Finding[]`→`Issue[]` (added `issue_id`); the source-finding link still uses
  `finding_id`.
- **Project Overview** → `useGetOverview…` (was: 4 composed reads + client-side counts). Counts now
  read from the governed `Overview.counts` (`kind = finding|issue|recommendation`).
- **History/Timeline** CHR trail → `useListHistory…` (was: `useListAnalysisRuns…` as a CHR proxy).
  Supersession is now driven by `HistoryEntry.supersedes_chr_id` (append-only; the superseded CHR
  stays visible; current = the newest un-superseded CHR). UAR + plan-fact sections keep
  `/acceptance` + `/plan-facts` (the `/history` read is the CHR trail only).

### Wave E negatives — updated (old-stub → mutation) vs. unchanged

**Updated (asserted OLD stub behavior; now assert the command path while keeping the invariant):**
- Recommendation Panel — the DTM-0022 *"accept navigates to Wave U, does not flip"* test → now
  *"accept calls the accept mutation; the SURFACE does not flip the status locally"* (status stays
  `generated` after click; the mutation is the recorded path). Added command-path positives
  (accept/reject/defer/implement each call their hook; onSuccess invalidate is wired).
- Chat — the *"the whole client is read-only / no mutation hook to reach"* negative → now *"the READ
  modules stay GET-only; Chat reaches no canonical-write hook; the ONLY write is the chat ENDPOINT
  (non-canonical)"*. Send tests now assert the message goes through the endpoint and OSLO's phrased
  `response` is appended from the result (never fabricated locally); Improve discloses the triggered
  Deep Pass.
- Notification — the *"dismiss/mark-read is LOCAL state"* criticals → now *"dismiss/mark-read is a
  PLATFORM-STATE command; the surface mutates NO governed object locally"* (the in-memory DTO is
  byte-for-byte unchanged; the platform state is written by the command + re-read via invalidate).
- Finding Panel — read-only docstring relaxed to allow the workflow affordance; the negative regex
  (`accept|resolve|generate|recompute|reanalyze|apply…`) is **unchanged** — acknowledge/address/
  reopen are workflow status transitions, not assessment changes, and don't match it.
- Timeline — the *"failed run shown honestly"* test (no failed concept in the CHR `/history` read) →
  *"a prior un-superseded CHR stays in the trail, not marked current (append-only)"*.

**Unchanged (epistemic-safety negatives — still green, verbatim):**
- Recommendation Panel: no generate/score/recompute/resolve-finding/govern/approve/execute/apply
  control; no Resolution-Path object emitted; never presented as settled (label stays Derived); RP-C1
  (no recommendation content outside a Finding context).
- Chat: no accept/approve/govern/sign-off control; clarify is information-capture only; never shows a
  score/%/health verdict; Improve never claims an applied/resolved change.
- Notification: no generate/score/accept/resolve/govern control; Acceptance-Impact never renders
  settled/auto-resolved (label stays Derived); dismissing a notification does NOT resolve the
  Acceptance-Impact.
- Finding Panel: evidence anchors stay Attested/evidence (never Derived); finding never settled; no
  inline recommendation list (RP-C1).
- Issue Cards / Overview / Dashboard: no edit/score/accept/generate control; Derived stays Derived
  (never Attested); confidence never reads as project health/readiness/probability/%/bare score.
- Timeline: no edit/accept/generate/delete/rollback/govern control; APPEND-EXACT ordering preserved;
  CHR entries stay Derived; plan facts stay user-attested (never world-truth/evidence/OSLO-attested);
  rendering mutates no governed DTO.

### Verify (exact commands + results, from `code/frontend`)

- `npm run build` (tsc -b + vite) → **PASS** (817 modules; `dist/assets/index-*.js` 661 kB / 205 kB
  gzip).
- `npx tsc --noEmit` (drift gate typecheck) → **PASS** (exit 0).
- `npx vitest run` → **245 passed (17 files)** — all new + existing Wave E suites.
- `npx playwright test` → **41 passed** — incl. 4 new DTM-0039 happy-paths (accept / chat-via-endpoint /
  dismiss / create-project + Start Fast Pass) plus the unchanged Wave E negatives.
- `npm audit --omit=dev --audit-level=high` → **found 0 vulnerabilities**.
- `bash scripts/check-openapi-drift.sh` (regen + tsc) → **"Frontend is in sync with the backend
  OpenAPI contract."**

### Confirmations

- Client **regenerated, not hand-edited** (gitignored; idempotent regen; drift gate green).
- **No new dependency** — `package.json`/`package-lock.json` unchanged; TanStack `useMutation`/
  `useQueryClient` are built-in.
- **Theme + EpistemicLabel + router structure unchanged** (`git status` clean for `src/theme`,
  `src/components/EpistemicLabel.tsx`, `src/app/router.tsx`); RP-C1 nesting intact.
- Changes confined to OWNed boundaries: `src/surfaces/**` + their vitest/fixtures + `e2e/` (one new
  spec `e2e/write-wiring.spec.ts`, one updated `e2e/chat.spec.ts`). Unrelated working-tree changes
  preserved (staged, not committed).

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_

## Approved by engineering manager

Status: Approved

Executive summary:
- The UI is functional end-to-end. Orval client regenerated against the now-complete OpenAPI (41
  paths; 9 new command/read modules). Every Wave E affordance wired to its real command via TanStack
  `useMutation` + read-invalidate: Recommendation accept/reject/defer/implement (0033), Chat send/
  Improve (0037), Notification view/dismiss (0035), Finding lifecycle (0035), project create +
  analysis triggers + evidence (0032/0034). Issue/Overview/History swapped to the first-class reads
  (0038). API §5.

Verification (EM re-ran): `npm run build` built; `npx vitest run` → **245 passed** (17 files);
worker playwright 41 (4 new happy-paths), drift gate in sync, `npm audit --omit=dev` 0. Scope = 7
surfaces + tests + 1 e2e; generated client gitignored (regenerated, not hand-edited). Dependency
delta **NONE**; theme/EpistemicLabel/router structure unchanged.

Epistemic-safety preserved: only the negatives asserting the OLD stub were updated (e.g. RP "accept
navigates, doesn't flip" → "accept calls the mutation; the SURFACE doesn't flip status locally");
Disclose-presents-never-generates / RP-C1 / Derived-never-settled / Chat-no-canonical-local all stay
green.

Remaining risks / minor: the RecommendationPanel `testHarness.tsx` retains an unused Wave-U stub
route (harmless, typechecks; trim-on-touch later).
