# HTTP transport in `backend/api/v1/`; DTOs are Data Model entities in `shared/`

The ratified code-tree names no HTTP/transport home, but the ratified API Contract
Specification (`20_handoff/interfaces/`) fixes a REST `/v1` surface whose resources and
request/response schemas are the Data Model v1.2 entities, used verbatim. So transport is
required, and DTOs are not a free design — they mirror the entities.

We put all HTTP in one transport folder, `backend/api/` with a `v1/` namespace (matching
the canonical `/v1` prefix and §15 versioning): `app.py` (composition root, serves
`/openapi.json`), `deps.py` (Supabase-JWT auth + workspace scoping + idempotency),
`errors.py`, and `v1/routers/` (one per resource). Routers are thin — they delegate to
`orchestration`/`responsibilities` and project results via `services.render`.

Response DTOs are the canonical entity schemas, defined once in `shared/entities.py` (not
in transport), so `services.render` can produce them and `api` can expose them without a
service importing the transport layer. Request-input shapes live in `api/v1/schemas/`.
`shared/entities.py` (external Data Model resources) is kept distinct from
`shared/epistemic.py` (internal cognition); `render` maps between them.

## Status

accepted

## Considered Options

- **All DTOs in transport (`api/v1/schemas/`)** — rejected: forces `render` to return view
  objects the router re-maps, or inverts layering (a service importing transport).
- **Routers inside the `disclose` responsibility** — rejected: HTTP is commodity transport;
  mixing it into a responsibility module breaks the platform/cognition separation.

## Consequences

- The frontend Orval client is generated from `/openapi.json`; it is gitignored and
  **regenerated in CI with a drift gate** (build fails if frontend DTOs ≠ backend OpenAPI),
  keeping frontend types == backend contract == Data Model v1.2.
- The API spec predates DL-053: it uses legacy plane/layer names and "Data Model v1.1" in
  prose. Code uses canonical vocabulary and v1.2. Event transport (webhook vs stream) is an
  open NFR — only internal dispatch is built for now.
