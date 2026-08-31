# OSLO Product Grill

Production application for the OSLO Product Grill vertical slices. The knowledge package and golden prototype remain external design inputs; this repository owns executable application code.

## Repository boundaries

- `apps/web` — Next.js App Router web application.
- `services/api` — FastAPI application and business capabilities.
- `packages/contracts` — generated/shared API contracts.
- `packages/ui` — OSLO design tokens and reusable UI primitives.
- `supabase` — reproducible local Supabase configuration and seed data.
- `infra` — deployment and operational configuration.
- `tests/e2e` — cross-service Playwright journeys.
- `docs/adr` — decisions that affect multiple capabilities.

Capability code stays together inside each service. Infrastructure adapters depend on application/domain interfaces, not the reverse.

## Local platform

1. Run `pnpm install`.
2. Run `pnpm supabase start`.
3. Run `pnpm seed:local`.
4. In one terminal, run `pnpm dev:api`.
5. In another terminal, run `pnpm dev:web`.

The local admin is `admin@oslo.local`; its development-only default password is `OsloLocalAdmin123!`. Override both values with the seed environment variables documented in `.env.example`.

- Supabase API: `http://127.0.0.1:55321`
- PostgreSQL: `127.0.0.1:55322`
- Studio: `http://127.0.0.1:55323`
- Mailpit: `http://127.0.0.1:55324`

## Verification

- API tests: `pnpm test:api`
- API lint: `pnpm lint:api`
- Web tests: `pnpm test:web`
- Web lint: `pnpm lint:web`
- Production web build: `pnpm build:web`
- Desktop and mobile tracer: `pnpm test:e2e`

The tracer covers Owner login, invitation delivery through Mailpit, account activation, one-time Welcome, draft-project creation, intake entry, resend, and revoke.
