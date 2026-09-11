# Intralign AI-First Delivery Process

**Audience:** Client and delivery team — one PM, one developer, one engineering lead

**Status:** Client-shareable operational draft for review; proposed controls are not yet adopted or configured

**Revision:** 2 — 2026-09-08

**Purpose:** Prepare a complete release in GitHub with Claude, review its impact, freeze the design, and deliver its small items through Linear and tested pull requests.

## 1. The agreed operating model

The PM uses Claude to develop the complete release prototype and specifications in GitHub. The release contains small, numbered items. Each item is refined through commits, and the lead reviews technical impact during preparation.

When the complete design is ready, the owner freezes its approved revision through the existing governance process. A publishing action creates or updates one Linear project and its implementation issues from that approved release. The developer then delivers the items through short-lived branches and pull requests to main.

The lead approves technical quality. The PM accepts the running behavior against the approved design. Production release is a separate, owner-authorized step.

```text
GitHub: design/release-2.1
  Complete design release, tracked through a draft release PR
    Item R2.1-001 → prototype + specification + criteria
    Item R2.1-002 → prototype + specification + criteria
    Item R2.1-003…N
      ↓ incremental lead review + Claude impact analysis
  Complete release review → owner design freeze → governed promotion to main
      ↓
  ci-build-project: publish the approved revision to Linear
      ↓
Linear: Release 2.1 project
  Small issues → developer + AI → implementation PRs to main
      ↓
  Required CI + lead review → merge → PM acceptance in staging
      ↓
  Owner-approved production release → tagged commit + release evidence
```

One design release can contain many implementation tickets. Committing an item records progress; its readiness remains provisional until the complete release passes review. The developer builds from the approved baseline, rather than following ongoing edits to the next design release.

## 2. Three people, clear responsibilities

| Person | Owns | Uses AI for |
|---|---|---|
| PM | Release outcome, prototype, specifications, acceptance criteria, priority, Linear visibility, product acceptance | Generate/refine release items, compare prototype changes, draft impact summaries, publish approved tickets, prepare client updates |
| Developer | Implementation, tests, PR evidence, defect corrections | Read approved context, plan implementation, write code and tests, diagnose failures, prepare PR summaries |
| Lead | Technical impact, dependencies, estimates, CI quality, code review, deployment coordination | Challenge assumptions, review diffs independently, find test gaps, assess release evidence |

The owner remains the authority for canonical decisions, design freeze, and production approval. If the PM or lead also holds that authority, record it in the release overview; the job title alone does not grant it.

AI review is advisory. The lead reviews the original criteria and important failure cases, because an AI implementation and its generated tests can share the same mistaken assumption. The PM tests the actual behavior.

## 3. GitHub and Linear ownership

| Location | Authoritative for |
|---|---|
| GitHub design documents and prototype | Approved scope, item definitions, design history, impact review, frozen references |
| GitHub implementation PRs and CI | Code changes, technical review, executable checks, merge commits |
| Linear | Live issue ownership, priority, dependencies, blockers, delivery status |
| GitHub release record | Scope-to-issue mapping and dated snapshots of acceptance, test, and deployment evidence |

Linear is the team's shared delivery view. GitHub remains the PM's environment for prototyping and impact review.

Create the Linear release project as Planned when useful for early visibility, linking the draft GitHub release PR. Draft issues may exist in Backlog, but the approved publication step determines what becomes buildable.

Use the native GitHub–Linear integration for PR linking and ordinary status transitions where supported. Use MCP for approved ticket publication, context retrieval, and summary preparation. Assign one mechanism to each automatic transition so integrations do not fight over status.

## 4. Prepare the complete design release

The PM and Claude work on the protected next-release design line. Keep one draft release PR as the review entry point, with a release overview and an item index. Record refinements incrementally using the item IDs in commit messages.

The overview contains the release objective, scope and exclusions, PM/developer/lead names, item list, dependency order, and open questions. Link existing specifications and contracts instead of copying them into another document.

### Release-item template

Use this compact structure for each item. Reference existing sections where they already contain the required detail.

```markdown
### R2.1-001 — <item title>

- Outcome / use case: <who needs what, and why>
- Scope and exclusions: <included behavior and meaningful boundaries>
- References: <contract/specification IDs and sections; prototype screen/anchor>
- Acceptance criteria:
  - AC-01: <observable result>
  - AC-02: <observable result>
- Test cases: <happy path; failure/negative cases; links to AC IDs>
- Impact: FE <...>; BE <...>; data/migration <...>; observability <...>
- Dependencies: <item IDs or none>
- Effort: <overall developer/lead estimate; FE/BE split if useful>
- Change class: <Neutral / Additive / Altering, per existing governance>
- Open questions: <decision needed and owner, or none>
```

Each ID stays stable through GitHub, Linear, PRs, and the release record. After freeze, references resolve to the approved commit and document section; prototype references identify a screen or interaction, not only a general file URL.

An item should represent an independently testable outcome. Several inseparable UI details can share one ticket. Create sub-issues only for separately trackable work, such as a prerequisite API and its dependent integration. If several items share one issue, preserve each item ID and its criteria in that issue.

With one developer, one overall effort estimate is sufficient by default. Record FE/BE impact for every relevant item, and add separate estimates when they help expose complexity. AI estimates remain suggestions until the developer or lead checks them.

### Incremental impact review

The lead reviews completed groups of items while the release is being prepared. Claude compares the changed prototype/specifications with the previous baseline and identifies affected behavior, contracts, screens, APIs, migrations, tests, and dependencies.

A review records **Findings, Concerns, Dependencies, Recommendation, and Status**, following the existing review schema. Open questions remain visible; technical feasibility is checked before the PM invests further in dependent designs.

The draft release PR is a coordination point, not permission to bundle every change. Framework 002 still requires Altering changes to have their own gated PR and target main; permitted batching and canonical decision landing rules continue to apply. If a proposed promotion would conflict with those rules, resolve its routing with the owner before landing it.

## 5. Design freeze: approve what will be built

The complete release is reviewed before implementation handoff. The PM confirms product scope; the lead confirms build readiness; the owner supplies the required freeze authority.

Before declaring the design frozen:

- Every in-scope item has criteria, source references, tests, and an impact assessment.
- Dependencies resolve to known items and have no circular implementation ordering.
- Unresolved design decisions have been resolved or formally removed from the release scope.
- The complete prototype and applicable design checks pass.
- Required governance reviews and change classifications are complete.
- The owner records the approved commit, prototype checksum, and design-baseline tag.

Existing Framework 002 §9 requirements remain binding: complete preconditions, a build-readiness audit with zero unresolved escalations, a green state matrix at the frozen md5 including the terminal-state journey, acceptance-register alignment with the guard set, and the owner freeze declaration naming the md5 and tag.

Promote the approved design through the prescribed process to main. Publication into Linear uses this approved baseline. Any material edit after review requires renewed review of the affected scope.

**Design freeze establishes the build target. It does not establish that the application has been implemented, accepted, or released.** Record the design-baseline tag separately from the later production tag.

## 6. Publish to Linear with ci-build-project

Treat ci-build-project as an explicitly triggered publishing action against an approved release revision. It is a handoff action, separate from ordinary application builds and tests.

| Step | Required behavior |
|---|---|
| Read | Load the release manifest at the specified approved commit; verify freeze evidence and promotion |
| Validate | Check item IDs, references, criteria, test cases, dependencies, and required decisions before creating issues |
| Preview | Show proposed creates/updates and flag differences from any existing publication |
| Publish | Create/update one release project and its issues; create sub-issues only where defined |
| Link | Attach pinned GitHub references, stable item IDs, dependencies, assignment, and effort |
| Report | Produce the complete item-to-Linear mapping, publication revision, and any failures |

For the initial approved publication, buildable issues enter Ready. Items with unfinished dependencies remain in Backlog with explicit blocking relationships. Once their dependencies are satisfied, the lead/developer confirms readiness and moves them to Ready. This avoids adding a second “Ready to develop” approval queue.

Use release ID plus item ID as the stable mapping key. Re-running the action against the same revision must preserve existing issues, assignments, progress, comments, and acceptance evidence. New revisions require an approved change comparison; the publisher must not overwrite in-progress work or delete issues because an item disappeared from a file.

If creation partially fails, report which mappings succeeded and retry only missing work. Do not report a successful release handoff until all intended issues and dependencies are accounted for.

The automation uses scoped credentials and records its actor, source commit, target IDs, and run link. It cannot authorize new scope.

## 7. Linear workflow and client visibility

Use six issue statuses:

| Status | Entry condition | Responsible person |
|---|---|---|
| Backlog | Draft, unresolved scope, or an item awaiting a prerequisite | PM |
| Ready | Approved definition, references and criteria complete, prerequisites satisfied | PM; lead confirms technical questions |
| In progress | Developer starts implementation; draft PR may exist | Developer |
| In review | PR is ready for lead review; CI evidence is visible | Lead |
| Acceptance | Implementation merged; awaits staging availability and PM verification | PM |
| Done | PM accepted the agreed behavior against an identified running revision | PM |

Show blockers using dependencies and a short reason with a named next actor. A green CI run or AI comment cannot mark an issue Done.

Configure draft PRs to remain In progress and ready PRs to move to In review. Merges to main move to Acceptance; a design PR merge must not complete implementation tickets. If a ticket has several implementation PRs, wait for all required PRs before treating implementation as complete.

If a PR closes without merging, record the reason and return the issue to the appropriate working state. If the PM finds an acceptance defect, return it to In progress and attach the corrective PR. New scope becomes a separately reviewed change.

For client visibility, maintain one release project view with owner, status, dependencies, linked PR, and blocker information. Link the current staging preview and approved design baseline at project level. A brief PM-checked weekly update covers accepted outcomes, current work, blockers, scope changes, forecast changes, and what is live. AI may draft it from evidence.

Done means accepted. The release project and tagged release record establish whether accepted work is in production. Raw ticket counts should not be presented as a precise percentage of release effort.

## 8. Branching and PR standards

The following are naming examples; INT-123 is an illustrative Linear identifier.

| Branch or tag | Purpose | Base / destination |
|---|---|---|
| main | Protected integration and delivery truth | Receives approved implementation and governed design promotion |
| design/release-2.1 | PM/Claude prepare the complete next-release design | Isolated design line; governed promotion to main |
| feat/INT-123-artifact-upload | One implementation outcome | Current main → PR to main |
| fix/INT-124-upload-retry | One corrective change | Current main → PR to main |
| chore/INT-125-test-maintenance | Maintenance work | Current main → PR to main |
| v2.1.0 | Approved production version | Tag the tested and accepted production commit |

Maintain one active next-release design line and short-lived implementation branches. There is no standing develop branch or long-lived delivery branch per release. Corrective changes land on main; evolutionary design goes through the next design line and freeze/promotion.

The developer starts from current main after the relevant design baseline lands. Keep ordinary application PRs small and squash-merge them, then delete their branches. Canonical decision PRs retain the prescribed serialized landing procedure. Unfinished features must be safely incremental or disabled so main remains releasable; production promotion is separately controlled.

### Implementation PR template

```markdown
## Outcome
<Concrete change and reason>

## Traceability
Linear: <issue link>
Release items: <stable IDs>
Approved design: <commit and prototype/specification links>
Contract / source: <applicable approved reference>
Change class: <Neutral / Additive / Altering>

## Acceptance and evidence
- <criterion ID → test / screenshot / demonstration>
- <negative cases and CI evidence>

## Impact
<Data/migration, security, observability, deployment or rollback impact;
state none where applicable. Record unresolved questions.>
```

Proposed application merge rule: require one independent human code approval, normally the lead for developer-authored work and the developer for lead-authored work. Apply additional owner reviews where governance requires them. PM product acceptance is a separate responsibility.

Require current CI results, resolution of review conversations, and renewed approval after material code changes. Protect main and the design line against unauthorized direct pushes and force-pushes; keep CI and ownership configuration protected from bypass.

This human-review rule needs reconciliation with the current application self-merge arrangement before configuration. Listing two names in CODEOWNERS alone does not enforce both signatures; any policy requiring specific independent approvals needs explicit enforcement.

## 9. Design and implementation checks

| Stage | Automated checks | Human review |
|---|---|---|
| Design preparation / promotion | Document and source-reference integrity; applicable prototype build and interaction/visual checks; item completeness; dependency validation; required governance checks | Lead checks impact and feasibility; PM checks scope; owner approves freeze/canonical changes |
| Implementation PR | Formatting, lint, explicit type checks, production build, frontend/backend tests, integration tests, Playwright, applicable security and domain guardrails, valid traceability | Lead reviews behavior, failure cases, test evidence, and AI findings |
| Acceptance and production preparation | Checks on the candidate revision, full regression, applicable migration and observability verification | PM accepts the actual workflow; lead checks technical readiness; owner authorizes production |

Use the current test stack: Vitest for frontend tests, pytest for backend tests, and Playwright for user journeys. Use Prettier for applicable formatting, Ruff for Python quality, and ESLint for frontend lint. An additional Jest runner is unnecessary.

Positive and negative tests are required for governed behavior. Traceability checks must validate that referenced sources exist and have the required approval; matching an IC-shaped string is insufficient. Include applicable secret scanning, dependency scanning, static security analysis, migration safety, and governed-output observability/replay obligations.

Retain the current full Playwright run for applicable application PRs initially. Measure runtime and flakiness before introducing selective test routing. Document-only changes may have a justified scope exemption, but changes to CI, shared configuration, contracts, or dependencies must also be considered when deciding test applicability.

The run-tests label requests an additional full run or rerun. Required tests still run without the label. Adding commits invalidates earlier evidence for the changed revision. Missing tests, runner failures, or a failed required job must block merging; an applicable test must not be converted to “skipped” to obtain a green result.

Collect coverage reports and establish a reviewed baseline before choosing numeric thresholds. Enforce the adopted policy once configured; do not invent a percentage or describe it as already active. Criteria coverage and meaningful failure tests remain essential even when line coverage is high.

## 10. Acceptance and production release

After merge, deploy the approved staging candidate through the existing environment process. Keep the issue in Acceptance until the PM can access that revision and verify its criteria. Record the tested commit/environment and a short result; add screenshots or test links where useful.

At production preparation, the lead assembles the candidate commit, included items, PM acceptance, full-regression evidence, applicable migration plan, and rollback target. Later changes to the candidate require renewed relevant verification.

The authorized owner approves release of the identified candidate. Tag that commit with the production version, release the tested artifact, and record deployment and health-check evidence. The lead coordinates these actions within the existing human-only production rules.

The production record identifies who approved, what shipped, when, and how to recover. Update Linear's release project with that link. Never represent the design-baseline tag or a successful merge as a production deployment.

## 11. Ledger and changes after freeze

Maintain a compact mapping in GitHub:

| Release item | Approved design revision | Linear issue | Implementation PR(s) / commit | Evidence |
|---|---|---|---|---|
| R2.1-001 | <frozen commit and section> | <issue link> | <PR links and merged commit> | <CI, PM acceptance, production release link> |

Generate the initial mapping after publication as a CI artifact and, where a repository record is required, through a reviewed bot-authored PR. Later acceptance/release snapshots may include the observed Linear status and observation time. Linear remains authoritative for current execution status.

CI validates the committed record and publishes evidence; it does not silently commit to protected branches while checking a PR. This delivery mapping supplements the existing governed Refinement Ledger, whose required change records remain in force.

For a change after freeze:

1. PM and Claude identify the changed item, reason, and affected references.
2. Lead checks impact on existing tickets, dependencies, tests, and effort.
3. Route it through the existing change class and owner approval requirements.
4. Record the amended approved revision and review the intended Linear updates.
5. Preserve history and notify the developer before changed scope is built.

New ideas that do not need to alter the current baseline go to the next design release. A failed test is a development problem to fix and rerun; it does not authorize changing the approved criteria. Missing product decisions go to the PM/owner.

## 12. Lightweight team cadence

- PM develops the next complete design release in GitHub and keeps the release overview current.
- Lead reviews design impact incrementally and checks ready implementation PRs regularly.
- Developer pulls the next unblocked Ready item, using its pinned context with AI.
- PM accepts completed work promptly in staging so acceptance does not become an unseen queue.
- AI prepares evidence and concise updates at meaningful transitions rather than posting a running commentary to every issue.

Prefer one active implementation item per developer, with an exception for blocked work. Review and acceptance queues are visible in Linear. A short release review and a weekly client update are sufficient defaults; extra ceremonies need a concrete purpose.

## 13. Setup work and current limits

This revision updates the operating document. The following remains implementation/configuration work:

| Setup | Owner | Completion evidence |
|---|---|---|
| Release overview/item template and design/implementation PR templates | PM + lead | One complete example release can be reviewed using the templates |
| Linear project, six statuses, GitHub links, transition ownership | PM + lead | Draft, review, merge, rejection, and acceptance transitions behave as specified |
| ci-build-project publisher | Lead + developer | Approved publication, duplicate rerun, invalid input, and partial failure/retry verified |
| Branch protections and reviewer routing | Lead + owner | Applicable branches reject unapproved, failing, and stale-review PRs |
| Required quality checks and coverage policy | Lead + developer | Required checks run and demonstrably block a failing application change |
| Staging acceptance and release snapshots | PM + lead | Accepted revision traces to the deployed artifact and production tag |

Local-file inspection on 2026-09-08 found application CI already runs Ruff/ESLint, pytest/Vitest, a web build, R2 guardrails, and Playwright. Explicit formatting, coverage thresholds, and the complete security obligations are not all wired in that inspected workflow. Its contract-ID regex does not itself validate approval. The current CODEOWNERS file intentionally leaves pure application code without a required code owner.

These observations concern the local checkout. Live GitHub protections, Linear settings, publisher availability, and enforcement have not been verified. Configure and prove the intended behavior before describing the automation as operational.

## 14. Governing references

This is an operational proposal, subordinate to existing ratified policy. It does not ratify new rules or replace the governed freeze, refinement, decision, or deployment procedures.

- [Framework 001 — canonical change](../../00_owner/frameworks/framework_001.md)
- [Framework 001A — review outputs and authority](../../00_owner/frameworks/framework_001A.md)
- [Framework 002 — release classification, capture, topology, and freeze](../../00_owner/frameworks/framework_002.md)
- [Anti-Assumption Build Protocol](../../00_owner/ANTI_ASSUMPTION_BUILD_PROTOCOL.md)
- [Deployment Governance](../../00_owner/build_governance/DEPLOYMENT_GOVERNANCE_SPECIFICATION_V1.md)
- [Linear tracking boundary](LINEAR_IMPORT_README.md)

Before adoption, the owner and lead must reconcile the proposed application approval rule with current policy and settle any promotion routing affected by the per-Altering-change rule. The document's single release review entry point does not waive those requirements.
