# OSLO application engineering rules

## Architecture

- Keep the Next.js application in `apps/web` and FastAPI capabilities in `services/api`.
- Business rules must not import Supabase, SMTP, HTTP, or SQL adapters. Inject those boundaries.
- Keep capability code cohesive; avoid generic `utils`, `helpers`, and catch-all service modules.
- FastAPI OpenAPI is the API source of truth. Shared/generated client contracts belong in `packages/contracts`.
- Supabase migrations under `supabase/migrations` are the database source of truth. Never maintain a second migration history.

## Security

- Treat every workspace-scoped operation as tenant-scoped and enforce authorization in the API and PostgreSQL RLS.
- Never persist or log raw invitation, access, refresh, or service-role tokens.
- Browser sessions use Secure/HttpOnly/SameSite cookies; server actions revalidate through the backend/provider.
- Public signup and anonymous access remain disabled during Alpha.

## Delivery

- Use one observable RED → GREEN → REFACTOR cycle per behavior.
- Run Python tests and Ruff for API changes; Vitest, ESLint, and `next build` for web changes.
- Run the desktop and mobile Playwright tracer before declaring Slice 1 releasable.
- Preserve the golden prototype’s tokens and behavior unless a ratified product decision supersedes it.
