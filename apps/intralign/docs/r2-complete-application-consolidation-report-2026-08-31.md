# R2 complete application consolidation report

Date: 2026-08-31

Status: Ready for draft pull request; not merged or deployed

## Scope

The complete tracked R2 application from `feature/r2-defect-remediation` was consolidated into the client repository at `apps/intralign/`. The consolidation branch was created from the latest fetched `client/main` and does not alter `main` directly.

| Evidence | Result |
| --- | --- |
| Client base | `a2c1732c9530aa5368e2af5752528c66eecbd4b1` |
| R2 source | `cfe060c3` (`feature/r2-defect-remediation`) |
| Safety branch | `backup/r2-defect-remediation-20260831` |
| Consolidation branch | `feature/r2-complete-application` |
| Original tracked application files | 1,222 |
| Missing files after relocation | 0 |
| Additional immutable test/contract fixtures | 4 |

The four additional fixtures preserve prototype and doctrine comparisons inside the application boundary, so tests no longer depend on the former repository layout.

## Changes

- Relocated the complete R2 web app, API, packages, Supabase configuration, tests, scripts, and deployment files into `apps/intralign/`.
- Kept secrets and generated dependencies out of Git. Only `.env.example` is tracked.
- Updated application CI to run from `apps/intralign/` and to report on every pull request while running expensive gates only when the application changes.
- Updated operational documentation, CODEOWNERS commentary, test fixtures, and guardrails for the new path.
- Kept the root knowledge-base document-integrity check independent from application documentation while still resolving references to application files.
- Did not merge or deploy any code.

## Verification

| Check | Result |
| --- | --- |
| File-manifest comparison | Pass — 1,222/1,222 source paths present |
| Web unit/component tests | Pass — 297/297 |
| API non-integration tests | Pass — 390/390 |
| R2 guardrail unit tests | Pass — 8/8 |
| R2 registry and prototype corrections | Pass — 60 registered, 53 active, 7 pending, 58 mapped surfaces, 6/6 corrections |
| Web lint | Pass |
| API lint | Pass |
| Next.js production build and TypeScript | Pass |
| Authored-change whitespace check | Pass; preserved legacy reports, PDFs, and prototype fixtures retain pre-existing whitespace warnings |
| Workflow YAML parse | Pass |
| Root document-integrity gate | Pass — 840 documents, 0 errors; 60 existing non-blocking warnings |
| Local database integration and browser E2E | Pending GitHub CI — local Docker/Supabase engine unavailable |
| Local gitleaks binary | Unavailable; repository security/CI checks remain required |

## Governance and release status

The current delivery record still names `code/` as the application location. Moving the application to `apps/intralign/` therefore requires explicit owner review/ruling in the pull request. The PR must remain a draft and must not be merged until:

1. GitHub application CI and repository-required checks pass.
2. The owner approves the new application path and the altering release change.
3. Human review confirms the complete R2 scope and deployment configuration.

Deployment is deliberately excluded from this consolidation. After an approved merge, staging should be deployed from `apps/intralign/` and followed by the full authenticated smoke and browser E2E suite before production promotion.
