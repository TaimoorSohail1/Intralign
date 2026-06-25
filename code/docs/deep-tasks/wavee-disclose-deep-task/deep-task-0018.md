# DTM-0018 — REST exposure: api/v1 read routers + render DTOs (the layer the UI consumes)

**Status:** Planned — BLOCKED on Wave E authorization (DL-044) + Wave U (#69) merge · **Module:**
DTM-0018 · **Phase:** VI (Wave E) · **Contract:** **IC-WE-DISCLOSE** (presentation transport) +
**ADR-0003** (REST `/v1`) · **Depends:** Waves A–U (the governed objects), Data Model v1.2.

## Goal / observable behavior

The frontend can fetch the governed objects over REST. `backend/api/v1/` exposes **read-mostly**
GET endpoints that present what Waves A–U produced — Projects, Findings, Issues, Recommendations,
Confidence/CAF/Outcome Confidence, the Cognition-History trail, User Acceptance Records + Plan
Facts, Acceptance-Impact, Notifications — each mapped by `services/render` into **Data Model v1.2
DTOs** (`shared/entities.py`), exposed verbatim. The OpenAPI grows from `/health` to the domain
surface; `npm run api:gen` regenerates the Orval client and the drift gate (`tsc`) stays green.
**The API presents; it never computes, mutates cognition, or accepts** (writes stay on the
existing capture/acceptance seams).

## Source docs / constraints

- IC-WE-DISCLOSE E0/E1 (Disclose presents; epistemic labels travel with every object); ADR-0003
  (REST `/v1`, DTOs = Data Model v1.2 verbatim, the Orval drift gate); the **API Contract Spec**
  (`20_handoff/interfaces/`) + **UI_SCREEN_INVENTORY** (which operations each screen needs);
  `deep-task-decisions.md` #3–#5, #9, #11; ANTI_ASSUMPTION.

## Locked decisions (from decisions file — do not re-derive)

- **Read-mostly:** the present endpoints are GET (list/detail) over governed objects. **No new
  write/mutation path** — acceptance/capture stay on the existing Wave-A/U seams (the
  Recommendation accept affordance, DTM-0021+, routes to the existing capture).
- **Render maps cognition → DTO:** `services/render` converts internal `epistemic.py` types
  (Finding/Issue/Confidence/CAF/…/CHR/UAR/PlanFact/AcceptanceImpact) into the external
  `shared/entities.py` DTOs. **Internal types are never serialized verbatim** (negative-proven).
  The DTO carries the **epistemic label** (Attested/Derived + confidence band + conflict) so the
  UI can render it without re-deriving.
- **Endpoints** bind to the API Contract Spec + the screen inventory's operation list (e.g.
  `GET /projects`, `GET /projects/{id}`, `…/findings`, `…/recommendations`, `…/issues`,
  `…/confidence`, `…/history`, `…/acceptance`, `…/notifications`). Pull each path/DTO from the
  spec — **do not invent** an endpoint a screen doesn't need or a DTO field not in Data Model v1.2
  (⇒ STOP/escalate on a gap).
- **Auth/scoping:** reuse `api/deps.py` (Supabase-JWT + workspace scoping + idempotency). **No
  migration.**
- Routers live under `api/v1/routers/` (the catalog already names them); `v1/__init__.py`
  includes them; `app.py` keeps serving `/openapi.json`.

## Owned files / boundaries

- **OWN (additive):** `backend/api/v1/routers/**` (the GET routers) · `backend/api/v1/__init__.py`
  (include them) · `backend/api/v1/schemas/**` (request inputs if any) · `backend/services/render/**`
  (the cognition→DTO mappers) · `shared/entities.py` (fill the DTO fields from Data Model v1.2 —
  additive) · `code/frontend/src/api/generated/**` (regenerate via `npm run api:gen`) ·
  `tests/{positive,negative}/api/**` + `tests/{positive,negative}/render/**`.
- **READ-ONLY:** all cognition/orchestration (`responsibilities/**`, `orchestration/**`,
  `retain/**` write paths), ALL migrations, the gates, `app.py` core. **No cognition change, no
  new write surface.**

## Packages / refactors

- None new (backend). No migration. Additive routers + render mappers only.

## Implementation instructions (TDD)

1. Red: pytest — `services/render` maps each governed object → its Data Model v1.2 DTO with the
   epistemic label intact; each GET endpoint returns the DTO (list + detail); auth/scoping
   enforced; **negatives:** no internal `epistemic.py` type serialized verbatim; the read surface
   exposes no mutation/accept/compute path; a DTO carries no field absent from Data Model v1.2.
2. `services/render` mappers → `api/v1/routers` GET endpoints → include in `v1/__init__.py`.
3. Regenerate the Orval client (`cd frontend && npm run api:gen`); run the drift gate
   (`bash scripts/check-openapi-drift.sh` / `tsc --noEmit`).

## API / data / schema contracts

- DTOs = `shared/entities.py` (Data Model v1.2), verbatim over REST (ADR-0003). Each carries
  `epistemic_label` (attested-*/derived) + confidence band + conflict where applicable. **No
  schema/DB change.**

## Test plan

- **Positive:** render maps cognition→DTO (labels intact); GET list/detail per resource; auth +
  workspace scoping; OpenAPI regen + drift gate green.
- **Negative:** internal cognition type leaked verbatim *(Critical)*; a write/mutation/accept/
  compute reachable from the read surface *(Critical)*; DTO field not in Data Model v1.2; missing
  epistemic label on a Derived object.
- ruff + gate-4 + gate-5 green; full backend suite no regression; frontend `tsc` green.

## Manual checks (EM)

- Backend up → `GET /v1/projects/{id}/findings` returns DTOs with labels; no endpoint mutates a
  canonical row; `frontend npm run api:gen` produces hooks for the new resources.

## Done criteria

- The domain REST surface exists + render mappers; Orval client regenerated; drift gate green; the
  read-mostly + no-verbatim-leak negatives pass; no migration/package; PR cites IC-WE-DISCLOSE /
  ADR-0003. Ready for DTM-0019.

## Worker report

_(worker fills)_

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_
