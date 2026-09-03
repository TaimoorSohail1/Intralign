# Slice 2 Project Advisor and New Project Navigation Plan

## Outcome

Complete the two missing Overview interactions without weakening Slice 2 governance:

1. Let an authenticated member ask OSLO questions about the current project.
2. Let the member start another project from Overview while retaining the existing project.

## Acceptance criteria

- The advisor accepts a quick prompt or a typed question.
- The browser sends only the project ID and question; the API key remains server-side.
- The API resolves the authenticated tenant's current immutable Overview snapshot.
- OpenAI receives that bounded snapshot and returns a strict typed answer with up to three
  follow-up questions.
- The advisor does not invent facts, follow instructions embedded in project data, expose hidden
  reasoning or make decisions for the user.
- Provider failures return a safe retry message and do not change project data.
- Unauthenticated requests return `401`; inaccessible projects return `404`.
- A single New project action creates one fresh project and navigates to its Intake.
- Repeated clicks while creation is running do not create duplicate projects.
- The prior project remains available.
- The layout remains usable at desktop and mobile widths.

## Delivery sequence

1. Add failing API contract tests for advisor auth, input validation and provider behavior.
2. Add a backend-only OpenAI advisor with strict Pydantic structured output.
3. Add the tenant-scoped advisor endpoint using the current published Overview.
4. Add failing component tests for chat success, chat failure and new-project double-click.
5. Add authenticated Next.js proxy routes for advisor and project creation.
6. Wire the Overview chat, loading/error states, follow-up prompts and New project action.
7. Add responsive styling that follows the existing OSLO prototype system.
8. Run focused tests, complete regression suites, lint, production build and live browser checks.

## Verification gates

- API: full pytest suite and Ruff.
- Web: full Vitest suite, ESLint and Next.js production build.
- Live provider: authenticated Orion question returns a grounded OpenAI answer.
- Security: no-token request is rejected and inaccessible project is hidden.
- Browser: advisor completes, new project opens Intake, old Overview remains available and the
  controls remain present at mobile width.

## Status

Implemented and verified on 23 July 2026.
