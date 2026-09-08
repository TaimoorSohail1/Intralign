# Intralign Deployment Setup

This document explains how to run and deploy Intralign for a new developer.
It describes the current production layout and the environment variables needed
by the frontend and backend. It intentionally contains no secret values.

## 1. Production architecture

| Service | Vercel project | Repository root | Production URL |
| --- | --- | --- | --- |
| Frontend (Next.js) | `intralign-v2` | `apps/intralign/web` | `https://app.intralign.ai` |
| Backend API (FastAPI) | `intralign-v2-api` | `apps/intralign/api` | `https://api.intralign.ai` |
| Database/auth/storage | Supabase OSLO project | Managed outside the repository | Supabase project URL |

The browser talks to the frontend. The frontend's server-side actions call the
backend API, and the backend talks to Supabase, OpenAI, Postmark, and optional
billing/integration services.

```text
Browser
  |
  +--> app.intralign.ai  (Vercel: intralign-v2)
          |
          +--> api.intralign.ai  (Vercel: intralign-v2-api)
                    |
                    +--> Supabase / OpenAI / Postmark
```

## 2. Repository layout

Only the deployment-relevant folders are shown here:

```text
apps/intralign/
├── web/                 # Next.js frontend
├── api/                 # FastAPI backend
├── ci/                  # application validation and guardrails
├── docs/                # application documentation
└── infra/               # infrastructure/deployment support files
```

The repository root contains the governance and engineering documentation.
Do not move `web` or `api` without updating both Vercel Root Directory settings.

## 3. Environment files for local development

`.env.example` is a template only. Create local files from the template and
keep them untracked:

```text
apps/intralign/.env.example   # names and safe local defaults
apps/intralign/web/.env.local # frontend local values
apps/intralign/api/.env       # backend local values
```

Never commit `.env`, `.env.local`, `.env.production`, or any file containing a
real token, password, private key, or database credential.

### Frontend: `apps/intralign/web/.env.local`

```env
NEXT_PUBLIC_SUPABASE_URL=<supabase-project-url>
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=<supabase-publishable-key>
OSLO_API_URL=http://127.0.0.1:8000
```

`NEXT_PUBLIC_` values are included in the browser bundle. The publishable key
is intended for client use; do not place a Supabase service-role/secret key or
any other private credential in a `NEXT_PUBLIC_` variable.

### Backend: `apps/intralign/api/.env`

```env
DATABASE_URL=<postgres-connection-string>
SUPABASE_URL=<supabase-project-url>
SUPABASE_SECRET_KEY=<supabase-secret-or-service-key>
WEB_URL=http://localhost:3000
OPENAI_API_KEY=<openai-api-key>
POSTMARK_SERVER_TOKEN=<postmark-server-token>
EMAIL_FROM=<verified-sender-address>
FROM_NAME=<sender-display-name>
OBJECT_STORAGE_BACKEND=local
OBJECT_STORAGE_BUCKET=oslo-source-documents
```

Optional settings in `apps/intralign/.env.example` include Stripe billing,
Asana, model selection, worker tuning, and SMTP fallback. Add them only when
the corresponding feature is enabled.

## 4. Start the local services

From the repository root:

```powershell
# Frontend
cd apps/intralign/web
pnpm install
pnpm dev
```

In a second terminal:

```powershell
# Backend
cd apps/intralign/api
uv sync
uv run uvicorn oslo_api.main:app --reload --port 8000
```

The local frontend is normally available at `http://localhost:3000` and the
API at `http://127.0.0.1:8000`. Start the local Supabase stack when running
integration tests that require a local database or auth service.

## 5. Vercel environment variables

Add variables in **Vercel → Project → Settings → Environment Variables**.
Select the environment explicitly; adding a variable to Preview does not add
it to Production.

### Build identity (both Vercel projects)

Enable **Automatically expose System Environment Variables** for both
`intralign-v2` and `intralign-v2-api`. This makes Vercel's
`VERCEL_GIT_COMMIT_SHA` available while building and running each deployment.
It is the source of the build identity: the web renders it in `data-build` and
the footer, while the API returns it as `build` from `/health`.

Do not create a hand-maintained `VERCEL_GIT_COMMIT_SHA` value. For a
non-Vercel deployment only, set one of the supported commit variables
(`NEXT_PUBLIC_BUILD_SHA` for web; `BUILD_SHA`, `HEROKU_SLUG_COMMIT`, or
`SOURCE_VERSION` for API) to the immutable commit being deployed.

### Frontend project: `intralign-v2`

Set these for Preview and Production as appropriate:

```env
NEXT_PUBLIC_SUPABASE_URL=<supabase-project-url>
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=<supabase-publishable-key>
OSLO_API_URL=https://api.intralign.ai
```

### Backend project: `intralign-v2-api`

Set these as encrypted variables for Preview and Production. Use separate
values where staging and production are separate Supabase environments:

```env
DATABASE_URL=<postgres-connection-string>
SUPABASE_URL=<supabase-project-url>
SUPABASE_SECRET_KEY=<supabase-secret-or-service-key>
WEB_URL=https://app.intralign.ai
OPENAI_API_KEY=<openai-api-key>
POSTMARK_SERVER_TOKEN=<postmark-server-token>
EMAIL_FROM=<verified-sender-address>
FROM_NAME=<sender-display-name>
OBJECT_STORAGE_BACKEND=supabase
OBJECT_STORAGE_BUCKET=oslo-source-documents
```

Do not copy production database or service secrets into Preview unless that is
an explicit, approved decision. Use the Vercel Secret type for keys and tokens.

## 6. Vercel project settings

Confirm these settings before a deployment:

1. `intralign-v2` Root Directory is `apps/intralign/web`.
2. `intralign-v2-api` Root Directory is `apps/intralign/api`.
3. Both projects are connected to `idris-manley/oslo-knowledge-base`.
4. The backend commit contains the approved FastAPI Vercel entrypoint and
   includes the `src/oslo_api` package in the function bundle.
5. Preview and Production variables are present in their respective projects.
6. **Automatically expose System Environment Variables** is enabled in both
   Vercel projects so the deployment carries `VERCEL_GIT_COMMIT_SHA`.

## 7. Deployment flow

1. Create a branch from the current `main`.
2. Make the change and run the relevant local checks.
3. Open a GitHub pull request into `main`.
4. Wait for the required repository and Vercel Preview checks.
5. Review the Preview deployment using its generated URL.
6. Merge only after the required review/approval and checks are complete.
7. Deploy/promote the merged `main` commit to Production.
8. Record the deployed commit SHA and verify the production domains.

Production deployment must not be performed from an unreviewed feature branch.

## 8. Post-deployment verification

Check the following after each deployment:

- `https://app.intralign.ai/login` loads successfully.
- `https://api.intralign.ai/health` returns a healthy response.
- Frontend `data-build` and footer, and backend `/health` `build`, report the
  same expected `VERCEL_GIT_COMMIT_SHA` for the deployed commit.
- Login, invitation send/resend/accept, and access-control behavior work.
- A test document can be uploaded and analysis can be started.
- Results, history, confirmations, reports, and refresh persistence work.
- Browser console and Vercel runtime logs contain no new errors.

Run these checks on Preview first to validate the promotion candidate. Preview
results do **not** constitute sign-off evidence. Production is changed only
after Preview passes and the release is owner-approved; the sign-off evidence
is then collected against that Production deployment and its reported build
identity.

## 9. Secrets and incident handling

- Store secrets only in Vercel Environment Variables, local ignored files, or
  an approved secret manager.
- Never paste secret values into GitHub issues, pull requests, chat, or source.
- Rotate any credential that has been exposed.
- Keep Supabase secret/service keys backend-only.
- Use separate Preview/staging and Production credentials where possible.
- If a deployment fails, inspect the Vercel build/runtime logs before changing
  application code or production configuration.

## 10. Useful references

- Repository: <https://github.com/idris-manley/oslo-knowledge-base>
- Frontend: <https://app.intralign.ai>
- Backend: <https://api.intralign.ai>
- Vercel environment variables: <https://vercel.com/docs/environment-variables>
