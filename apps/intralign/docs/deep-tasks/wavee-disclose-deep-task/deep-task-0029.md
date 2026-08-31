# DTM-0029 — OSLO Chat + Assisted Editing (AW-04/05) + honest-limit disclosure (DL-048)

**Status:** In progress — DTM-0028 approved (`4d980a7`) · **Module:** DTM-0029 · **Phase:** VI
(Wave E) · **Contract:** **IC-WE-DISCLOSE** + **DL-047** (OSLO Chat CHAT-01…04, Assisted Editing
AW-04/05) + **DL-048** (honest-limit UP-4) · **Depends:** DTM-0018/0019/0020/0021/0022.

## Goal / observable behavior

Three DL-047/048 additions, the last Wave E surfaces:
1. **OSLO Chat** (Disclose-class): a conversation surface that **consumes** cognition (Explain/
   Clarify) and may **trigger** it (Improve → Advise/Deep Pass) — but **writes no canonical,
   mutates no artifact, changes no assessment** (Critical). Renders exchanges (non-canonical
   `ChatExchange`); inherits context when launched from an issue/recommendation/artifact/finding.
2. **Assisted Editing / Persistent Intelligence** (AW-04/05): an always-visible panel showing
   **Outcome Confidence + Clarity/Alignment/Feasibility (CAF) + Understanding-State** (read-only),
   routing assists to **Chat (B1)** or **Suggested Fix (B3)**.
3. **Honest-limit disclosure** (DL-048 UP-4): when a run is scope/budget-limited, present a
   **truthful partial-analysis disclosure** (reduced coverage + the reason); any upgrade prompt
   appears **alongside**, never **instead of**, the honest disclosure.

## Source docs / constraints

- Contract DL-047 additions (CHAT-01…04, AW-04/05) + DL-048 UP-4 + OBS-WE (`ChatExchange` events,
  non-canonical). UX: `10_product/experience/` → the OSLO Chat/clarification spec +
  `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW_SPECIFICATION_V1.md` (Assisted Editing) + the freemium/
  honest-limit copy. `code/CONTEXT.md` (OSLO Chat — no canonical write; honest-limit). Decisions
  #3, #5, #10.
- Consume the DTM-0018 reads (confidence/CAF for the Assisted-Editing panel). The `/chat` route was
  added as a placeholder in DTM-0025 — replace it. Inspect the generated client for any chat
  command endpoint.

## Locked decisions (do not re-derive)

- **Chat writes NO canonical / mutates NO artifact / changes NO assessment (Critical negative).**
  The chat surface renders the conversation + can request Explain/Clarify/Improve, but it itself
  records nothing canonical and changes no governed object. **Chat-command endpoint dependency
  (ANTI_ASSUMPTION):** DTM-0018 is read-only; if no chat send/trigger endpoint exists, render the
  conversation UI + input and FLAG the dependency (input present; "Improve" routes to the existing
  Advise/Deep-Pass trigger if/when exposed) — do NOT invent a canonical write, do NOT have Chat
  mutate anything locally.
- **Assisted Editing is read-only presentation** of governed values (Confidence/CAF/Understanding-
  State) via `EpistemicLabel`; it routes assists (to Chat / Suggested Fix) but performs none.
- **Honest-limit disclosure is truthful + non-coercive:** partial shown with the reason; upgrade
  prompt **alongside**, never **instead of** (negative-test: a scope/budget-limited result shown as
  complete, or an upgrade prompt shown in place of the honest disclosure, is rejected).
- No new dependency.

## Owned files / boundaries

- **OWN:** `code/frontend/src/surfaces/Chat/**` + `code/frontend/src/surfaces/AssistedEditing/**`
  (+ the honest-limit component, e.g. `src/components/HonestLimitDisclosure*`) + tests, and wiring
  the `/chat` route (replace the DTM-0025 placeholder) in `router.tsx`. Vitest + Playwright.
- **READ-ONLY:** backend, generated client, theme/EpistemicLabel, other surfaces.

## Packages / refactors — none new.

## Implementation instructions (TDD)

1. Red (Vitest):
   - **Chat:** renders a conversation (exchanges) + an input + Explain/Clarify/Improve affordances;
     context inheritance when launched with a source. **Negatives:** Chat writes no canonical /
     mutates no artifact / changes no assessment (assert no governed object is mutated, no canonical
     write call; sending is a non-canonical exchange or flagged-pending) — Critical.
   - **Assisted Editing:** always-visible Outcome Confidence + CAF + Understanding-State (labelled,
     Derived); routes-to-Chat / routes-to-Suggested-Fix affordances. **Negative:** no
     generate/score/accept/apply control (it routes, performs nothing).
   - **Honest-limit:** renders the truthful partial disclosure + reason; if an upgrade prompt is
     shown it is **alongside** the disclosure. **Negatives:** partial-as-complete rejected; upgrade-
     instead-of-disclosure rejected.
2. Implement; replace the `/chat` placeholder; mount the Assisted-Editing panel + honest-limit
   component; clean loading/empty states.

## API / data / schema contracts

- Consumes the DTM-0018 reads (confidence/CAF + `DerivedEnvelope`). Chat send/trigger: the existing
  chat/Advise seam — flag if no endpoint. No backend change; no canonical write.

## Test plan

- **Positive:** Chat conversation + context inheritance; Assisted-Editing always-visible
  confidence/CAF/state + assist routing; honest-limit disclosure + reason.
- **Negative (Critical for Chat):** Chat writes no canonical / mutates no artifact / changes no
  assessment; Assisted-Editing performs no cognition (routes only); partial-as-complete + upgrade-
  instead-of-disclosure rejected.
- `npm run build` + `vitest run` + Playwright + drift + `npm audit --omit=dev`.

## Manual checks (EM)

- `npm run dev` → Chat renders + Explain/Clarify/Improve (no canonical write / artifact mutation /
  assessment change); Assisted-Editing panel shows live confidence/CAF/state + routes assists;
  honest-limit disclosure truthful with any upgrade prompt alongside.

## Done criteria

- OSLO Chat (no-canonical-write, Critical-proven) + Assisted Editing (read-only intelligence,
  routes assists) + honest-limit disclosure (truthful, non-coercive) present; chat-command
  dependency wired-or-flagged; read-only; no new dep; tests green. PR cites IC-WE-DISCLOSE / DL-047
  / DL-048. **Last Wave E surface — Release 1 feature-complete pending the owner exit-gate.**

## Worker report

**Status: Ready for review.** All three DL-047/048 additions built TDD (failing Vitest
first → green), the last Wave E surfaces. No new dependency; one allowed route file
edited (`router.tsx`); EpistemicLabel / theme / generated client / other surfaces
untouched.

### Files

**1. OSLO Chat** (`src/surfaces/Chat/**`) — mounts at `/projects/$projectId/chat`
(replaces the DTM-0025 placeholder):
- `Chat.tsx` — the conversation surface: transcript of non-canonical `ChatExchange`,
  an always-enabled input, and Explain / Clarify / Improve affordances. Defines the
  non-canonical `ChatExchange` / `ChatContext` presentation types (NOT DTOs).
- `ChatRoute.tsx` — reads inherited context from the route search
  (`context_kind`/`context_id`/`context_label`) → pre-scopes the conversation read-only.
- `fixtures.ts`, `testHarness.tsx`, `Chat.test.tsx` (16 tests).

**2. Assisted Editing / Persistent Intelligence** (`src/surfaces/AssistedEditing/**`,
AW-04/05) — mounts in the Artifact Editor at `/artifacts/$artifactId` (replaces the
DTM-0019 placeholder):
- `AssistedEditing.tsx` — always-visible, read-only panel: Outcome Confidence + CAF
  (C/A/F) + Understanding-State, each via `EpistemicLabel` (Derived, banded). Routes
  assists to Chat (B1) and Suggested Fix via its Finding (B3, RP-C1).
- `ArtifactEditorRoute.tsx` — mounts the panel (needs `project_id` search context;
  clean empty state without it) + hosts the honest-limit disclosure on the same surface.
- `fixtures.ts`, `testHarness.tsx`, `AssistedEditing.test.tsx` (13 tests).

**3. Honest-limit disclosure** (`src/components/HonestLimitDisclosure.tsx`, DL-048 UP-4):
- `HonestLimitDisclosure.tsx` — truthful partial-analysis disclosure (reason +
  reduced-coverage), with the commodity upgrade prompt rendered ALONGSIDE (disclosure
  always first; renders nothing when not limited).
- `honestLimit.fixtures.ts`, `HonestLimitDisclosure.test.tsx` (10 tests).

**Wiring:** `src/app/router.tsx` — real `ChatRoute` (with context-inheritance search
validation) replaces the `/chat` placeholder; `ArtifactEditorRoute` (with `project_id` /
`finding_id` / `limited` search) replaces the `/artifacts/$artifactId` placeholder.
**E2E:** `e2e/chat.spec.ts`, `e2e/assisted-editing.spec.ts`.

### Chat-command endpoint finding (ANTI_ASSUMPTION — FLAGGED, not invented)

There is **no chat send/trigger endpoint, and no mutation/write endpoint of any kind**, in
the DTM-0018 generated client (`src/api/generated/**`): every exported hook is a GET read
(name ends in `…Get`) across confidence/caf/findings/recommendations/analysis-runs/
projects/notifications/acceptance. No `ChatSession`/`ChatExchange` resource and no
Advise/Deep-Pass trigger are exposed over REST. Per the protocol I did **not** invent a
canonical write: Chat renders the conversation + input, and a **send appends an ephemeral,
non-canonical `ChatExchange` marked "pending"** with an honest notice ("nothing was
recorded and no assessment changed"); **"Improve" routes to the existing Advise/Deep-Pass
trigger when that seam is exposed** (flagged pending). A structural Vitest asserts the
whole generated client is read-only so Chat *cannot* reach a write.

### How Assisted Editing routes (never performs)

The two assist affordances are **routing `<Link>`s, not action buttons** — B1 → the
project Chat surface (carrying the artifact as inherited context, read-only); B3 → the
Suggested Fix **via its Finding** (`/projects/$pid/findings/$fid`, never a standalone
`/recommendations` route — RP-C1). There are **zero `<button>` elements** in the panel
(asserted), so no generate/score/accept/apply control exists. Confidence/CAF/State are
read-only via `EpistemicLabel`; the raw 0–100 indices are never rendered.

### How honest-limit stays alongside-not-instead

`HonestLimitDisclosure` renders the disclosure block (`honest-limit-disclosure`:
partial + reason + coverage) **first/always** when `limited`, and the upgrade prompt
(`honest-limit-upgrade`) in a separate sibling block **after** it (DOM-order asserted).
The disclosure renders **even when no upgrade prompt is supplied** (mandatory disclosure,
optional commodity upgrade). When not limited it renders **nothing** (no fabricated
partial state). Negatives proven: partial-as-complete rejected (no "complete/full/final
analysis" copy); upgrade-instead-of-disclosure rejected (disclosure always present).

### Critical Chat negatives proven

- **No canonical write / no mutation:** structural test — the generated client exposes
  only `…Get` read hooks (no send/trigger/write hook to reach); Playwright asserts **zero
  POST/PUT/PATCH/DELETE** network requests on send.
- **No assessment change:** after send / Improve / Clarify the surface never reads
  `applied`/`accepted`/`resolved`/`saved`/`approved`; clarify is information-capture only
  (never "updated the assessment / changed confidence / resolved the finding"); Improve
  surfaces only a pending/route notice.
- **No accept/approve/govern/ratify control**; no score/percentage/health verdict.
- Context inheritance from finding/recommendation/artifact (search params) proven;
  contextual Finding-Panel handoff proven (complements, never replaces).

### Data gaps flagged (no invention; no DTO fabricated)

1. **Chat-command / Advise-Deep-Pass trigger endpoint** — not exposed over REST. Chat's
   input is present; sends are ephemeral pending; Improve will route to the existing
   trigger when exposed.
2. **DL-048 scope/budget-limit signal** (cap-hit / envelope-exceeded / budget gate) — not
   exposed over REST. `HonestLimitDisclosure` consumes a non-canonical presentation
   `HonestLimit` shape; the Artifact Editor's `limited` search param is the presentation
   **seam** for when the signal arrives.
3. **Understanding-State** — no aggregate "understanding/orientation state" DTO; derived
   from the governed `AnalysisRun` status (latest `superseded` ⇒ "based on the previous
   analysis"), exactly as the Companion does. No state flag invented.

### Verify (exact commands + results)

- `npm run build` (`tsc -b && vite build`) → **success** (804 modules; bundle-size warning
  only, pre-existing).
- `npx vitest run` → **17 files, 231 tests passed** (38 new: Chat 16 + AssistedEditing 13
  + HonestLimit 10 — note 3 suites; existing 193 unchanged).
- `npx playwright test` → **37 passed** (4 new chat + 5 new assisted-editing/honest-limit).
- `npm audit --omit=dev --audit-level=high` → **found 0 vulnerabilities**.
- Scope: only `src/app/router.tsx` modified; `package.json`/lockfile unchanged;
  EpistemicLabel / theme / `src/api` / other surfaces untouched. No new dependency.

PR cites **IC-WE-DISCLOSE / DL-047 / DL-048**. Last Wave E surface — Release 1
feature-complete pending the owner exit-gate.

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

Status: Approved

Executive summary:
- The final Wave E surfaces: **OSLO Chat** (`surfaces/Chat/**`, `/projects/$projectId/chat`) —
  conversation of non-canonical `ChatExchange` + Explain/Clarify/Improve + context inheritance;
  **Assisted Editing** (`surfaces/AssistedEditing/**`, `/artifacts/$artifactId`) — always-visible
  read-only Confidence/CAF/Understanding-State via `EpistemicLabel`, routes assists to Chat (B1) /
  Suggested Fix (B3); **Honest-limit disclosure** (`components/HonestLimitDisclosure.tsx`) —
  truthful partial + reason, upgrade prompt alongside.

Verification (EM re-ran): `npm run build` built; `npx vitest run` **231 passed** (38 new + 193);
worker playwright 37, audit 0. Scope = Chat/** + AssistedEditing/** + HonestLimitDisclosure + one
`/chat` route swap; dependency delta **NONE**.

Negatives proven (Critical for Chat): Chat writes no canonical / mutates no artifact / changes no
assessment — send appends an ephemeral non-canonical exchange; structural test + Playwright assert
no POST/PUT/PATCH/DELETE and no governed mutation. Assisted Editing performs no cognition (routes
only, zero action buttons). Honest-limit: partial-as-complete rejected, upgrade-instead-of-
disclosure rejected (disclosure always first).

Remaining risks / flagged (not invented): no chat send/trigger endpoint (GET-only client → ephemeral
exchange; Improve routes to Advise/Deep-Pass when exposed) — folds with the acceptance-command
backend follow-up (DTM-0030); DL-048 limit signal + Understanding-State are presentation seams
(limited param / AnalysisRun superseded status). The B1 Chat link carries artifact context
(`?context_kind=artifact&...`) rather than a bare `/chat` — intentional, strengthens inheritance.

**Last Wave E surface — all 10 surfaces present; Release 1 feature-complete pending the owner
exit-gate.**
