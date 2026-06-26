# DTM-0026 — Notification / Awareness (drift + Acceptance-Impact signals; read/dismiss = platform state, not canonical)

**Status:** In progress — DTM-0025 approved (`3d4282a`) · **Module:** DTM-0026 · **Phase:** VI
(Wave E) · **Contract:** **IC-WE-DISCLOSE** E1 (Notification/Awareness) · **Depends:** DTM-0018/0019.

## Goal / observable behavior

The **Notification / Awareness** surface presents **Outcome Drift** signals + **Acceptance-Impact**
alerts ("a decision you confirmed is affected") + new emissions, as awareness. **Read/unread/dismiss
is platform state (Category E) — NOT canonical** (a notification carries no governed truth; marking
one read changes no assessment). Read-only over governed objects; the only "write" is the platform
notification-state (read/dismiss), which is non-canonical and must never be treated as canonical.

## Source docs / constraints

- Contract E1 (Notification/Awareness row: "surface Outcome Drift + Acceptance-Impact as awareness;
  read/unread/dismiss is platform state (Category E), not canonical") + OBS-WE (`Notification
  Raised`, `Acceptance-Impact surfaced`; platform read/dismiss non-canonical). UX:
  `10_product/experience/NOTIFICATION_AND_AWARENESS_SURFACE_SPECIFICATION_V1.md`.
- `code/CONTEXT.md` (Acceptance-Impact Assessment = Derived, ≥10pts/band drift; notification state
  not canonical). Decisions #3, #5, #9.
- Consume the DTM-0018 notifications read (+ acceptance-impact). Reuse `EpistemicLabel` for any
  governed value surfaced (the drift/impact assessment is Derived).

## Locked decisions (do not re-derive)

- **Presents, never generates.** No generate/score/accept control. Drift + Acceptance-Impact are
  governed Derived objects surfaced via `EpistemicLabel`.
- **Notification state is platform/non-canonical (Critical negative):** read/unread/dismiss is a
  Category-E platform action; it writes NO canonical, changes NO assessment, promotes nothing.
  Marking a drift alert "read" does not resolve the drift. Negative-test: notification state written
  as canonical is rejected.
- **Acceptance-Impact** reads as "a decision you confirmed is affected" (links to the affected
  accepted item). No new dependency.

## Owned files / boundaries

- **OWN:** `code/frontend/src/surfaces/Notifications/**` (+ tests) and wiring the notifications
  route/placeholder in `router.tsx` (the one swap). Vitest + Playwright.
- **READ-ONLY:** backend, generated client, theme/EpistemicLabel, other surfaces.

## Packages / refactors — none new.

## Implementation instructions (TDD)

1. Red (Vitest): renders drift + Acceptance-Impact alerts (governed values labelled); read/unread/
   dismiss affordance present as a **platform** action. **Negatives:** no generate/score/accept
   control; Derived-as-settled impossible; **notification read/dismiss does NOT write canonical /
   change an assessment / resolve the drift** (assert it's local/platform state only — the governed
   alert object is unchanged); Acceptance-Impact never shown as auto-resolved.
2. Build from the DTM-0018 reads; mount; clean loading/empty states. If a dismiss endpoint doesn't
   exist, keep dismiss as local platform state and flag (do not invent a canonical write).

## API / data / schema contracts

- Consumes the DTM-0018 notifications + acceptance-impact reads (+ `DerivedEnvelope`). Notification
  read/dismiss = platform-state (local or a platform endpoint), non-canonical. No canonical write.

## Test plan

- **Positive:** drift + Acceptance-Impact alerts with labels; read/dismiss as platform state;
  empty/loading clean.
- **Negative:** no generate/score/accept control; Derived-as-settled impossible; notification-state
  -as-canonical rejected (dismiss changes no governed object/assessment); drift not auto-resolved.
- `npm run build` + `vitest run` + Playwright + drift + `npm audit --omit=dev`.

## Manual checks (EM)

- `npm run dev` → drift + Acceptance-Impact alerts; dismiss marks the notification read locally
  without changing the underlying governed alert/assessment; no accept/resolve-the-drift control.

## Done criteria

- Notification/Awareness presents drift + Acceptance-Impact as labelled awareness; read/dismiss is
  non-canonical platform state (negative-proven); read-only over governed objects; no new dep; tests
  green. PR cites IC-WE-DISCLOSE. Ready for DTM-0027.

## Worker report

**Status: Ready for review.**

### Files

Owned (new) — `code/frontend/src/surfaces/Notifications/`:
- `Notifications.tsx` — the surface (presentational; takes `projectId?` as a prop).
- `NotificationsRoute.tsx` — thin route element; reads the optional `project_id`
  search param and hands it to the surface.
- `fixtures.ts` — fixture DTOs mirroring the generated `Notification` +
  `AcceptanceImpactAssessment` types verbatim.
- `testHarness.tsx` — theme + query + in-memory-router harness (mirrors the real
  app paths the items route into).
- `Notifications.test.tsx` — 19 Vitest cases (positive + the critical negatives).

Owned (new) — E2E:
- `code/frontend/e2e/notifications.spec.ts` — mount happy-path + the
  presents-never-generates negative.

The one route swap (in scope):
- `code/frontend/src/app/router.tsx` — `/notifications` now mounts
  `NotificationsRoute` (was the DTM-0019 `Notification Center` placeholder); added
  a `validateSearch` for the optional `project_id` scope.

Stale-test repoint (consequence of the route swap, same as prior slices):
- `code/frontend/e2e/shell.spec.ts` — the DTM-0019 "a placeholder route resolves"
  smoke test probed `/notifications` for the old placeholder; repointed it to
  `/settings` (still a DTM-0019 placeholder). No assertion weakened.

No backend / generated-client / theme / `EpistemicLabel` / other-surface edits.
**No new dependency** (`package.json` / lockfile unchanged).

### How notification-state was modelled (local platform state vs an endpoint)

**Local platform state.** The DTM-0018 REST surface exposes only a notifications
**read** — `GET /v1/notifications` (`useListNotificationsV1NotificationsGet`).
There is **no platform read/dismiss WRITE** in the generated client (no
PATCH/POST/DELETE mutation for notification state anywhere under
`src/api/generated/notifications/`). Per the contract, read/unread and dismiss are
therefore modelled as **local component state** (`useState` maps `locallyRead` /
`locallyDismissed`), layered over the governed feed for display only. The handlers
mutate **no governed object** and write **no canonical** — and we did **not** invent
a canonical write. **Data gap flagged below.**

The governed `Notification` DTO itself is the proof of the boundary: it carries
**no `label` / `DerivedEnvelope`** (the generated schema docstring: *"Platform
awareness state (non-canonical): … carries no epistemic cognition label — it is not
a Derived projection — it references a source object"*). So the notifications feed
renders with NO epistemic label, while the **Acceptance-Impact** read
(`useListAcceptanceImpactV1ProjectsProjectIdAcceptanceImpactGet`, project-scoped)
**does** carry a `label` and is surfaced via `EpistemicLabel`
(`fromDerivedEnvelope`) — Derived, banded, conflict-aware, never settled.

The notifications feed is workspace-level; the Acceptance-Impact read is
project-scoped, so the surface gates the impact read on `projectId` (skipped when
absent — proven by the no-scope test).

### The not-canonical / Critical negative proven (Vitest)

Negatives in `Notifications.test.tsx`:
- **`dismiss` is LOCAL platform state** — snapshots the governed
  `unreadFindingNotification` (deep clone) before the action, dismisses, then asserts
  the governed object is byte-for-byte unchanged (`toEqual(before)`), its `state`
  stays `created`, `dismissed_at` stays `null`. No canonical write, no governed
  mutation.
- **`mark-read` is LOCAL platform state** — same proof on
  `unreadCommentNotification` (`state` stays `created`, `viewed_at` stays `null`).
- **dismiss does NOT resolve the drift** — after dismissing a notification, the
  Derived Acceptance-Impact alerts are untouched (same count, "a decision you
  confirmed is affected" still surfaced).
- **No generate / score / accept / reject / defer / resolve / approve / govern /
  recompute / reanalyze / apply / assign control** on the surface.
- **Acceptance-Impact never renders settled / resolved / auto-resolved**; every
  alert's label stays `data-standing="derived"`, never `attested`.
- **read/unread never reads as completion / approval / work / assessment status**.

E2E (`e2e/notifications.spec.ts`) repeats the presents-never-generates negative
against the running app.

### Exact verify commands + results

```
$ cd code/frontend && npm run build
> tsc -b && vite build
✓ 746 modules transformed.  ✓ built in 1.17s        # PASS

$ npx vitest run
Test Files  11 passed (11)
     Tests  145 passed (145)                          # PASS (19 new + 126 existing)

$ npx playwright test
24 passed (3.5s)                                       # PASS (2 new notifications specs;
                                                       #   shell placeholder probe repointed)

$ npm audit --omit=dev --audit-level=high
found 0 vulnerabilities                                # PASS
```

(One transient parallel-cold-start flake was seen on the very first `playwright
test` run — the dev server wasn't warm for the first-scheduled spec; it passed on
`--workers=1` and on the subsequent full parallel run. Not a surface defect.)

No new dependency; no out-of-scope edits (see Files). Unrelated working-tree
changes preserved (the untracked `src/surfaces/Companion/` from DTM-0025 is left
intact; staged only this slice's files).

### Data gap flagged

**No platform read/dismiss WRITE endpoint exists** in the DTM-0018 REST surface /
generated client (only `GET /v1/notifications`). Read/unread/dismiss is therefore
**local, non-persisted** platform state in this slice — correct for a Category-E,
non-canonical action, but it does not survive a reload. If the product wants
read/dismiss to **persist** (still non-canonical), DTM-0018 (or platform) would add
a notification-state write seam (e.g. `PATCH /v1/notifications/{id}`); that is a
backend/contract change, escalated rather than invented here.

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

Status: Approved

Executive summary:
- Notification/Awareness (`surfaces/Notifications/**`) at `/notifications`: presents the
  notifications feed (no Derived label — platform state) + project-scoped Acceptance-Impact alerts
  (Derived, via `EpistemicLabel`). read/unread/dismiss = LOCAL platform state (no write endpoint
  exists). Read-only over governed objects.

Verification (EM re-ran): `npm run build` built; `npx vitest run` **145 passed** (19 new + 126);
worker playwright 24, audit 0. Scope = Notifications/** + one route swap + the expected
`shell.spec.ts` placeholder-probe repoint (`/notifications`→`/settings`, no assertion weakened);
dependency delta **NONE**.

Negatives proven (the Critical one): dismiss/mark-read is LOCAL platform state — deep-clone
snapshot asserts the governed Notification is byte-for-byte unchanged (state stays `created`,
viewed_at/dismissed_at null); dismiss resolves no Acceptance-Impact drift; no generate/score/accept/
resolve control; Acceptance-Impact never auto-resolved/settled. Notification DTO carries no
`DerivedEnvelope` (correct — non-canonical platform state, not a Derived projection).

Remaining risks / flagged: no notification-state WRITE endpoint → read/dismiss is local only;
durable read/dismiss needs a backend platform notification-state seam (Category E, non-canonical) —
a follow-up, not invented here.
