# DTM-0035 — REST: finding lifecycle + notification state

**Status:** In progress · **Module:** DTM-0035 · **Phase:** Completion · **Contract:** API §5
(130–132) + catalog (notifications :view/:dismiss) + Event §8 · **Depends:** DTM-0031 (notification
repo) + DTM-0030 (finding projection). **Branch:** `feat/release1-completion`.

## Goal / observable behavior

New command endpoints:
- `POST /v1/findings/{fid}:acknowledge` → Finding(`acknowledged`), `finding_acknowledged`.
- `POST /v1/findings/{fid}:address` → Finding(`addressed`), `finding_addressed` (or
  `finding_updated`/`finding_closed` per the event spec).
- `POST /v1/findings/{fid}:reopen` → Finding(`reopened`), `finding_reopened`.
- `POST /v1/notifications/{nid}:view` → Notification(`viewed`), `notification_viewed`.
- `POST /v1/notifications/{nid}:dismiss` → Notification(`dismissed`), `notification_dismissed`.
Notification state via the DTM-0031 `notification_repo` (mark_viewed/mark_dismissed — **platform,
non-canonical**). Finding lifecycle = a **user workflow-status transition** (ground it: per the
State Model, finding status is an attribute on the Derived projection — update the
`derived.finding_current` status field via the DTM-0030 projection store, NOT a canonical write; if
the spec models it as a user-action record instead, wire that — confirm/flag). `Idempotency-Key`;
workspace-scoped.

## Source docs / constraints

- API §5 (130–132) + the catalog notification rows; `RELEASE_1_STATE_MODEL_SPECIFICATION_V1.md`
  (finding lifecycle Detected→Acknowledged→Addressed→Closed→Reopened — and **who owns the status**:
  projection attribute vs user-action). Event §8 (`finding_*`, `notification_viewed/dismissed` —
  notifications NEVER drive analysis). `code/CONTEXT.md` (notification state non-canonical; Derived
  projection is updatable). decisions #4, #5.
- Code: `backend/platform/notification_repo.py` (DTM-0031 mark_viewed/mark_dismissed), the projection
  store (`backend/services/persistence/projection_store.py` + the read seam — for the finding status
  update), `backend/api/v1/routers/findings.py` + `notifications.py` (existing GET — ADD command
  routers), the DTM-0032–0034 command/DI pattern, events + gate-5.

## Locked decisions (do not re-derive)

- **Notification state is platform/non-canonical** — `view`/`dismiss` via `notification_repo`; it
  changes NO assessment, drives NO analysis, writes NO canonical row. (Mirrors the Wave E DTM-0026
  contract.)
- **Finding lifecycle = workflow status on the Derived projection** — update `derived.finding_current`
  status (Derived, mutable; via the projection store/upsert) + emit the event. It is NOT a cognition
  change (the finding's content/confidence is unchanged), NOT a canonical write, NOT an acceptance
  (no UAR). If the State Model genuinely models acknowledge/address as a user-attested record ⇒
  STOP/flag (don't guess).
- Additive command routers; GET readers + negatives stay green. Emit §8 events (gate-5 vocab).
  `Idempotency-Key`; workspace-scoped (404). No new dep/migration.

## Owned files / boundaries

- **OWN:** `backend/api/v1/routers/finding_commands.py` + `notification_commands.py` (NEW) + include
  · `backend/api/v1/schemas/` · DI in `deps.py` · `tests/{positive,negative}/api/**`. Event vocab +
  gate-5 fixtures.
- **READ-ONLY:** notification_repo + projection store (call, don't change), read routers/seam,
  migrations, cognition.

## Packages / refactors — none new.

## Implementation instructions (TDD)

1. Red (pytest, TestClient + overrides): finding :acknowledge/:address/:reopen update the projection
   status + emit the event; notification :view/:dismiss via the repo + emit. **Negatives:**
   notification state writes NO canonical/assessment change (the finding's confidence/content
   unchanged); finding lifecycle is NOT an acceptance (no UAR) and changes no cognition; 401/404;
   idempotency; read routers unchanged.
2. Build the command routers; include in `v1/__init__.py`.

## API / data / schema contracts

- Returns Finding / Notification DTOs. Emits `finding_acknowledged/addressed/reopened`,
  `notification_viewed/dismissed`. Finding status = Derived projection update. No schema change.

## Test plan

- **Positive:** finding lifecycle transitions (+events); notification view/dismiss (+events);
  idempotency; scoping.
- **Negative:** notification-as-canonical rejected (no assessment change); finding lifecycle changes
  no cognition / no UAR; 401/404; read routers unchanged.
- `.venv/bin/pytest` + ruff + gate-4 + gate-5 (new vocab) green.

## Manual checks (EM)

- POST finding :acknowledge → the finding's status updates (read shows it); confidence/content
  unchanged. POST notification :dismiss → state dismissed; no assessment change.

## Done criteria

- Finding lifecycle (Derived status update) + notification state (platform, non-canonical) command
  endpoints emit §8 events, idempotent + scoped, no canonical/assessment change (negative-proven),
  read routers unchanged, gates green, no new dep/migration. PR cites API §5. Ready for DTM-0036.

## Worker report

**Status: Ready for review.**

### Endpoints delivered (additive command routers)

- `POST /v1/findings/{fid}:acknowledge` → Finding(`acknowledged`), emits `finding_updated`.
- `POST /v1/findings/{fid}:address` → Finding(`addressed`), emits `finding_updated`.
- `POST /v1/findings/{fid}:reopen` → Finding(`reopened`), emits `finding_reopened`.
- `POST /v1/notifications/{nid}:view` → Notification(`viewed`), emits `notification_viewed`.
- `POST /v1/notifications/{nid}:dismiss` → Notification(`dismissed`), emits `notification_dismissed`.

New files: `backend/api/v1/routers/finding_commands.py`, `notification_commands.py` (both
included in `v1/__init__.py`). DI providers added to `deps.py`: `get_projection_store`
(DTM-0030 `SupabaseProjectionStore`), `get_notification_repo` (DTM-0031 `SupabaseNotificationRepository`).
All `Idempotency-Key`-aware (per-route cache; retry returns the same DTO, no second write)
and workspace-scoped (401 unauth / 404 cross-workspace/missing — existence not leaked).

### Finding-status ownership finding (projection attribute vs user-record)

**The State Model models it as a projection/entity ATTRIBUTE, NOT a user-attested record —
no STOP/escalation needed.** Grounding:

- **State Model §10** (`RELEASE_1_STATE_MODEL_SPECIFICATION_V1.md`): the lifecycle
  Detected→Acknowledged→Addressed→Closed→Reopened is mapped directly to **`Finding.status`**
  (the §10 "Data-Model mapping" row: `detected/validated/addressed/resolved/reopened`). It is a
  status field on the Finding entity — never a `UserAcceptanceRecord` and never an append-only
  receipt. §10 also pins it descriptive ("a Finding's state describes the status of an
  observation; it never prescribes action").
- **§19 Open Question #6** leaves only the *actor* of "Acknowledged" open (user-only vs
  system auto-acknowledge) — NOT the storage class. The status-as-attribute is settled; only
  who may trigger it is deferred. I implemented it as a user action (the authenticated
  `Principal` is recorded in the event payload), which is the conservative reading.
- In the R1 runtime model the Finding is a **Derived** live-projection (`derived.finding_current`;
  LDM §3.1), so its status lives in the projection's `current_payload.status`.

**What I did:** the command reads the finding projection via the SELECT-only read seam
(workspace-scoped), validates the §10 transition, advances `current_payload.status`, and
UPSERTs the row back through the DTM-0030 projection store (`upsert_projection("finding", row)`).
The Derived layer is mutable/recomputable, so this is a legitimate projection update — **not**
a canonical write, **not** a CHR append, **not** an acceptance (no UAR).

### Events + gate-5

Per **API Contract §5 (130–132)** + the endpoint catalog (binding): `:acknowledge` and
`:address` both carry **`finding_updated`** (the resulting status rides the payload); `:reopen`
carries **`finding_reopened`**. API §5 line 251 is explicit that the granular
`finding_acknowledged`/`finding_addressed` names are **status FACETS of the canonical
`finding_updated` event — "no new event types are introduced beyond the Event Model"**. So I did
**not** introduce `finding_acknowledged`/`finding_addressed` event names (the task brief flagged
this option in line 12; the spec resolves it to `finding_updated`). `:view`/`:dismiss` emit
`notification_viewed`/`notification_dismissed` (EM §12) verbatim.

Two new gate-5 vocabulary groups, pinned verbatim in `events.py` + mirrored in
`ci/gate_observability.py` (per-contract tuple + union order + drift assertion):

- `EVENT_NAMES_FINDING = ("finding_updated", "finding_reopened")` — EM §10.
- `EVENT_NAMES_NOTIFICATION = ("notification_viewed", "notification_dismissed")` — EM §12.

Both gate-5 fixtures updated (positive `test_gate_observability.py` imports/asserts the two new
tuples + union; negative `test_gate_observability_negative.py` GOOD_EVENTS_PY gains the two
tuples + union legs, the missing-assignment count moved 16→18, and two new tamper/missing-tuple
negatives were added).

### How notification state stays non-canonical

`:view`/`:dismiss` call **only** `notification_repo.mark_viewed`/`mark_dismissed` (the DTM-0031
platform `notification` table). The router imports no projection store, no retention store, no
CHR repo. It writes no `derived.*_current` row, appends no CHR, and changes no assessment —
mirroring State Model §12 ("notification state changes do not alter Findings or Recommendations")
and EM §12 ("a notification event has zero recompute consumers"). Negative-proven below.

### Verify (exact commands + results)

- `cd code && .venv/bin/pytest tests/positive tests/negative -q` → **686 passed, 65 skipped**
  (no regression; the GET findings/notifications readers + their read-mostly negatives stay green).
- `.venv/bin/pytest` of the two new files → **21 passed**.
- `.venv/bin/ruff check .` → **All checks passed!**
- `.venv/bin/python ci/gate_invariants.py` (gate-4) → **PASS** (no forbidden tokens, no authority
  module, no canonical-table mutations).
- `.venv/bin/python ci/gate_observability.py` (gate-5) → **PASS** (per-contract A6 vocabularies
  pinned verbatim incl. the two new groups; union consistent).
- Confirmed: **no new dependency**, **no migration** (migrations dir untouched), GET read routers
  (`findings.py`/`notifications.py`) untouched, `notification_repo`/projection store are call-only.

### Negatives proven

- **Notification non-canonical:** `test_dismiss_does_not_change_the_referenced_finding` — a
  `:dismiss` leaves the referenced Finding's `current_payload` (content) and `confidence_value`
  byte-for-byte unchanged and writes **zero** projection upserts.
  `test_notification_command_uses_repo_only_no_canonical_or_assessment_write` — the router source
  wires `mark_viewed`/`mark_dismissed` only; never `upsert_projection`/`insert_*`/`chr_repo`/`.append(`.
- **Finding lifecycle = no cognition change / no UAR / no canonical write:**
  `test_finding_command_writes_no_uar_and_does_not_recompute` + `test_finding_command_preserves_cognition_payload`
  — only `status` changes; `confidence_value`/`summary`/`finding_type`/`evidence_anchors`/
  `current_chr_ref`/`epistemic_label='derived'` are all preserved across the upsert.
  `test_finding_command_wires_projection_store_only_no_acceptance` — the router source wires
  `upsert_projection` and never `record_acceptance(`/`insert_acceptance`/`insert_assertion`/
  `chr_repo.append`/`get_retention_store`.
- **Invalid transition → 409** (`acknowledge` a non-`detected` finding, `reopen` a non-`closed`
  finding) with **no** write; **401** unauth; **404** cross-workspace + missing (finding and
  notification); **idempotency** replays the same DTO with no second upsert/mark; read routers
  stay GET-only after the command routers are added.

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_

## Approved by engineering manager

Status: Approved

Executive summary:
- New additive `finding_commands` + `notification_commands` routers: finding :acknowledge/:address
  (→`finding_updated`) / :reopen (→`finding_reopened`) advance the Derived `derived.finding_current`
  status via the DTM-0030 projection store; notification :view/:dismiss via the DTM-0031
  notification_repo (platform, non-canonical). API §5 (130–132) + catalog.

Verification (EM re-ran): `.venv/bin/pytest` → **686 passed, 65 skipped** (25 new; no regression).
ruff clean; gate-4 PASS; gate-5 PASS (finding/notification vocab pinned). No new dep/migration; GET
readers `findings.py`/`notifications.py` unchanged.

Grounding (correct, no escalation): State Model §10 maps the finding lifecycle to `Finding.status`
(a projection attribute, NOT a UAR/receipt); API §5 line 251 makes acknowledge/address status facets
of `finding_updated` — so no invented event types. Notification state non-canonical (Wave E DTM-0026).

Negatives proven: notification dismiss leaves the finding's content+confidence byte-for-byte
unchanged + zero projection upserts; finding lifecycle changes only `status` (confidence/content/CHR/
`epistemic_label='derived'` preserved), no UAR/CHR/canonical write; 401/404; 409 invalid transition
(no write); idempotency replays; readers GET-only.
