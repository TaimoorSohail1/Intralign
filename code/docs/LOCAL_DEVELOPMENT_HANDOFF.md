# OSLO Local Development Handoff

**Purpose:** give a developer everything needed to run the current OSLO application locally without sharing any real `.env` file or committing secrets.

**Application branch:** `codex/release-2-build`

## 1. Security rule

- Share this document and `.env.example`.
- Never email, commit, or send an existing `.env`, `apps/web/.env.local`, or `services/api/.env` file.
- Share real OpenAI or Stripe test credentials through an approved password manager or another secure secret-sharing channel.
- Local Supabase credentials are generated on the receiving developer's machine and do not need to be shared.

## 2. What the project owner provides

| Item | Required | How to provide it |
|---|---:|---|
| Repository access | Yes | Add the developer to the GitHub repository. |
| Branch name | Yes | `codex/release-2-build` |
| OpenAI API key | Yes for real document analysis | Share securely; never place it in chat, email, source control, or screenshots. |
| Stripe test secret and webhook secret | Only for Slice 4 billing tests | Share securely. Test-mode values only. |
| Stripe Basic monthly and annual Price IDs | Only for Slice 4 billing tests | Share securely with the Stripe test credentials. |

The owner does **not** need to provide local database, Supabase, Neo4j, Redis, SMTP, or administrator credentials. The developer creates those locally.

## 3. What the developer installs

- Git
- Docker Desktop with the Docker Compose plugin
- Node.js `20.19+` or a compatible newer LTS release
- pnpm `10.25.0`
- Python `3.12`
- `uv`

Docker Desktop must be running before Supabase, Neo4j, or Redis is started. The Next.js web application and FastAPI service run natively; only backing services run in Docker.

## 4. Clone and install

```powershell
git clone https://github.com/idris-manley/oslo-knowledge-base.git
cd oslo-knowledge-base
git switch codex/release-2-build
cd code
corepack enable
corepack prepare pnpm@10.25.0 --activate
pnpm install
```

Running `pnpm install` also makes the repository-pinned Supabase CLI available through `pnpm supabase`.

## 5. Start Supabase and collect local credentials

```powershell
pnpm supabase start
pnpm supabase status
```

Copy the local API URL, publishable/anon key, secret/service-role key, and database URL from `pnpm supabase status`. These values belong only to the developer's local machine.

Local Supabase services:

| Service | Address |
|---|---|
| Supabase API | `http://127.0.0.1:55321` |
| PostgreSQL | `127.0.0.1:55322` |
| Supabase Studio | `http://127.0.0.1:55323` |
| Mailpit browser inbox | `http://127.0.0.1:55324` |
| Local SMTP | `127.0.0.1:55325` |

## 6. Create local environment files

Create these files locally. They are ignored by Git.

### 6.1 Web environment

Create `apps/web/.env.local`:

```dotenv
NEXT_PUBLIC_SUPABASE_URL=http://127.0.0.1:55321
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=<COPY_LOCAL_PUBLISHABLE_OR_ANON_KEY>
OSLO_API_URL=http://127.0.0.1:8000

# Optional: display the seeded local login on the development login screen.
OSLO_SHOW_DEV_CREDENTIALS=true
```

Only `NEXT_PUBLIC_*` values are exposed to the browser. Never put a Supabase secret/service-role key, OpenAI key, or Stripe secret in this file.

### 6.2 API environment

Create `services/api/.env`:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:55322/postgres
SUPABASE_URL=http://127.0.0.1:55321
SUPABASE_SECRET_KEY=<COPY_LOCAL_SECRET_OR_SERVICE_ROLE_KEY>
WEB_URL=http://localhost:3000

SMTP_HOST=127.0.0.1
SMTP_PORT=55325
EMAIL_SENDER="OSLO <no-reply@oslo.local>"

# Required for real AI document analysis.
OPENAI_API_KEY=<SECURELY_SHARED_OPENAI_KEY>
OPENAI_FAST_MODEL=gpt-5.6-luna
OPENAI_EXTENDED_MODEL=gpt-5.6-terra
OPENAI_FALLBACK_MODEL=
OPENAI_MAX_RETRIES=0

ANALYSIS_ARTIFACT_WORKER_THREADS=4
OBJECT_STORAGE_BACKEND=local
OBJECT_STORAGE_BUCKET=oslo-source-documents

# Optional — required only for real Slice 4 Stripe test-mode billing.
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
STRIPE_BASIC_MONTHLY_PRICE_ID=
STRIPE_BASIC_ANNUAL_PRICE_ID=

# Optional local seed overrides.
OSLO_LOCAL_ADMIN_EMAIL=admin@oslo.local
OSLO_LOCAL_ADMIN_PASSWORD=OsloLocalAdmin123!
```

If `OPENAI_API_KEY` is absent, the application can run deterministic/test paths, but real OpenAI-backed document analysis will fail closed. If any Stripe setting is missing, normal non-billing functionality remains available and Checkout fails safely without granting an entitlement.

### 6.3 Docker Compose environment

Create `code/.env` only if the developer wants to override the safe local Docker defaults:

```dotenv
NEO4J_USER=neo4j
NEO4J_PASSWORD=<CHOOSE_A_LOCAL_ONLY_PASSWORD>
NEO4J_HTTP_PORT=7474
NEO4J_BOLT_PORT=7687
REDIS_PORT=6379
```

Do not reuse any staging or production password locally.

## 7. Start backing services

For the complete local backing stack:

```powershell
docker compose up -d neo4j redis
```

Supabase already runs through its CLI and Docker. Neo4j and Redis are separate Docker Compose services. The optional observability stack can be started with:

```powershell
docker compose --profile observability up -d
```

The observability profile exposes OTLP on ports `4317`/`4318` and Grafana on `http://localhost:3000`; do not start it while the Next.js app is using port `3000` unless the Grafana port is changed.

## 8. Seed the local application

```powershell
pnpm seed:local
```

Default development login:

```text
Email: admin@oslo.local
Password: OsloLocalAdmin123!
```

These are local development defaults only. The developer may override them using `OSLO_LOCAL_ADMIN_EMAIL` and `OSLO_LOCAL_ADMIN_PASSWORD` before seeding.

## 9. Start the application

Terminal 1 — API:

```powershell
cd code
pnpm dev:api
```

Terminal 2 — web:

```powershell
cd code
pnpm dev:web
```

Application addresses:

| Component | Address |
|---|---|
| Web application | `http://localhost:3000` |
| FastAPI service | `http://127.0.0.1:8000` |
| FastAPI documentation | `http://127.0.0.1:8000/docs` |

## 10. Verify the setup

Run the checks from `code/`:

```powershell
pnpm test:api
pnpm lint:api
pnpm test:web
pnpm lint:web
pnpm build:web
pnpm test:r2-guardrails
```

For the full browser journey, install Playwright's browser once and run the tracer:

```powershell
pnpm --filter @oslo/e2e exec playwright install chromium
pnpm test:e2e
```

## 11. Normal shutdown

```powershell
pnpm supabase stop
docker compose down
```

Stopping services preserves their local Docker volumes. Do not add `-v` unless the developer intentionally wants to delete local Neo4j and Redis data.

## 12. Common setup problems

| Problem | Check |
|---|---|
| Supabase does not start | Confirm Docker Desktop is running and ports `55321–55325` are free. |
| Web login fails | Confirm `apps/web/.env.local` contains the current local Supabase publishable key. Restart `pnpm dev:web` after changing it. |
| API reports a missing Supabase key | Confirm `services/api/.env` contains the local secret/service-role key. Restart `pnpm dev:api`. |
| Real analysis fails | Confirm `OPENAI_API_KEY` is present in `services/api/.env`, has quota, and the configured models are available. |
| Stripe Checkout returns 503 | Supply all four Stripe test-mode variables or leave billing testing out of scope. |
| Port `3000` is occupied | Stop the optional Grafana profile or move its port before starting Next.js. |
| Seed login does not work | Run `pnpm seed:local` again after confirming the API environment and Supabase services. |

## 13. Handoff checklist

- [ ] Repository access granted.
- [ ] `codex/release-2-build` checked out.
- [ ] Docker Desktop, Node/pnpm, Python, and `uv` installed.
- [ ] Supabase started and local keys copied.
- [ ] `apps/web/.env.local` created.
- [ ] `services/api/.env` created.
- [ ] OpenAI key shared through a secure channel.
- [ ] Stripe test credentials shared only if billing testing is required.
- [ ] Neo4j and Redis started.
- [ ] Local seed completed.
- [ ] API and web applications started.
- [ ] Login, real document upload, analysis, and artifact workspace verified.
- [ ] Tests and production build pass.
