# Infrastructure

Deployment, observability, and production environment configuration live here. Local Supabase configuration remains in `supabase/`.

## Release contract

Every release must pass `.github/workflows/ci.yml`. It runs schema-backed API tests,
web tests, lint, the production build, and the complete desktop/tablet/mobile
Playwright journey using the deterministic analysis harness.

Production configuration must provide:

- managed PostgreSQL/Supabase with all committed migrations applied;
- private API credentials (`SUPABASE_SECRET_KEY`, `DATABASE_URL`, provider keys);
- public web credentials (`NEXT_PUBLIC_SUPABASE_URL` and publishable key only);
- durable object storage, SMTP delivery, HTTPS, and separate web/API processes;
- a durable process supervisor for analysis workers; and
- alerting for failed analyses, evidence quarantine, queue age, provider latency,
  HTTP 5xx, email delivery failures, and stale report-send attempts.

Never expose the Supabase secret key or document text in browser logs, analytics,
or exception telemetry.

## Deploy and rollback

1. Take a database backup and record the currently deployed web/API image IDs.
2. Apply migrations before starting the new API version.
3. Deploy API and workers, verify `/health`, then deploy the web application.
4. Run the production smoke journey: sign in, open an existing last-good project,
   create a disposable project, analyse it, and verify every section uses the same
   analysis-run ID.
5. If a gate fails, disable new analysis, restore the prior images, and retain the
   last successful analysis publication. Use a database restore only when a
   migration cannot be rolled forward safely.

## Backup verification

Schedule encrypted database and object-storage backups. At least monthly, restore
both into an isolated environment and verify that source documents, artifact
versions, analysis runs, History snapshots, shared links, and revocations agree.
