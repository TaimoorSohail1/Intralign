# Production acceptance remediation report - 2026-09-10

## Scope and release boundary

This work was prepared from `client/main` build `e069da1a66a581e6c097ef9bffbe1e16e2dfc76c`
on branch `fix/production-acceptance-remediation-2026-09-09`.

Approved-contract traceability: `IC-WA-001` governs Artifact Intake / Perceive, and
`IC-WU-ACCEPT` governs the user confirmation and retained acceptance record.

The evidence below separates three states:

- Production observations already measured on build `e069da1`;
- fixes and regression evidence completed locally;
- items that still require Preview or Production evidence after human promotion.

No Production deployment or sign-off is claimed by this report. Repository policy keeps merge
and Production promotion owner-controlled.

## Acceptance status

| Row | Status | Evidence and remaining work |
|---|---|---|
| N-1 | Production pass, no demonstrated margin | Five measured delivery gaps were all below 10 seconds: `0.000`, `6.110`, `0.000`, `5.705`, `0.000`. The two non-zero measurements consumed more than one 5-second poll, and the zero readings resolve only to the polling interval. |
| N-4 | Local pass; Production untested | Confirm, flag, and route transport failures retain the original basis, evidence, reviewer, and idempotency key; raw transport errors are hidden; the UI says project data is unchanged and offers Retry. Production still needs controlled transport-level fault injection. |
| N-5 | Production pass | Production web and API both reported build `e069da1`, matching and resolvable. |
| N-7 | Production pass | Outcome, Overview, workspace, and briefing use the canonical Outcome Integrity band and limiting pillar. The closing criterion now counts distinct values, so repeated rendering of the same band does not false-fail. |
| N-8 | Partial; remains open | Raw evidence markers are absent. The Executive Briefing can still report OSLO finding churn as `What changed - N issues opened`. Runtime wording was not changed because the owner has not ruled whether this section means user-authored plan/evidence changes or OSLO read changes. |

## Defects reproduced and fixed locally

### PDF upload failed before parsing on Windows

The real PDF journey reproduced HTTP 500 at local object storage. Content-addressed object paths
exceeded the legacy Windows 260-character boundary; `os.replace` failed while moving the atomic
temporary file.

The local object-storage adapter now uses Windows extended-length paths for create, replace, read,
existence, and delete operations. A Windows-only regression creates a path longer than 260
characters and verifies the complete put/get/exists/delete lifecycle.

### PDF fixtures were vulnerable to Git byte normalization

The repository did not classify PDFs as binary. With line-ending conversion enabled, checked-in
PDF cross-reference bytes could be changed during checkout. The five-document Atlas pack and the
DevNorth flow fixture were repaired, validated with `pdfinfo`, rendered, and visually inspected.
`*.pdf binary` now prevents recurrence.

### Long PDF-derived outcome could not be confirmed

After upload was repaired, the full journey exposed a second HTTP 500: a long outcome statement
violated the `project_outcomes.title` 240-character database constraint. The full statement remains
available to the analysis/action response, while the first-class outcome record now stores a
whitespace-normalized 240-character display title. The regression verifies both properties.

## First-run grounding behavior

The Overview focus treatment remains intentional. It may dim and temporarily disable surrounding
Overview controls, but it does not guard the Reports route. The end-to-end test navigates directly
to Reports after one governed action and confirms the route remains available. No access gate was
added or restored.

## B0 and N-8 clarification

B0 code is already present in `client/main` through PR #280 / commit `56ad6585`; it did not need to
be reimplemented here. A server-side twin regression now covers:

- the legacy similarity threshold;
- below-threshold wording change with the same semantic plan element;
- identity preservation when a finding moves between artifacts.

The B0 obligation remains open as acceptance evidence because its required Production remeasurement
has not been completed. That is different from saying the mechanism has not landed.

N-8 must not be closed by merely hiding `N issues opened`. The owner decision still required is:

> Should Executive Briefing "What changed" report only user-authored plan/evidence changes, or also
> OSLO read changes produced by deeper analysis? If OSLO read changes are included, what owner-approved
> wording must attribute them to OSLO rather than to the plan?

## Verification completed

- Real-PDF production-build browser journey: **1 passed in 1.4 minutes**.
  It covers upload, processing-page transition, completed analysis, outcome confirmation, Overview,
  first-run guidance, direct Reports access, briefing band/pillar agreement, and raw-marker absence.
- Targeted API regression set: **36 passed**.
- Focused Overview component suite: **89 passed**.
- API Ruff lint: **passed**.
- Web ESLint: **passed**.
- Production Next build: **passed**.
- R2 guardrails: **8/8 static tests, 43/43 active API tests, and 131/131 active web tests passed**;
  the inventory reports 60 registered, 53 active, 7 pending, 58 mapped surfaces, and 6/6
  prototype corrections.
- All six QA PDFs: `pdfinfo` passed; first pages rendered and visually inspected without clipping,
  overlap, or unreadable content.
- Earlier unchanged-baseline runs in this worktree: API **474 passed** and web **326 passed**. Those
  broad runs preceded the two newly added API fixes, which are covered by the targeted suite above.

The local documentation-integrity command could not traverse a missing Windows pnpm linked-package
directory under `node_modules`. This is an environment traversal limitation, not a reported document
violation; the Linux CI document check remains required on the PR.

## Promotion and Production verification plan

1. Run the production Next build and repository release gates.
2. Push the branch and open a PR against `idris-manley/oslo-knowledge-base:main`.
3. Validate the real-PDF journey on the Vercel Preview deployment; do not treat Preview as sign-off.
4. After owner review and human merge/promotion, re-run the same journey on Production.
5. Perform N-4 controlled fault injection in Production or an owner-approved production-equivalent
   environment.
6. Re-run the B0 before/after Production measurement and record stable issue identities.
7. Resolve the owner wording question before changing or closing N-8 limb 2.
