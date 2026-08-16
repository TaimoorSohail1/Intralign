# R2 Slice 6 — Collaboration implementation plan

Status: **Draft engineering plan — requires owner approval before implementation**

This plan does not ratify or modify OSLO canon. It translates the existing R2 Slice 6 build design and the accepted grill recommendations into an executable delivery sequence for the application repository.

## 1. Outcome

Slice 6 will let an owner ask a collaborator or tightly scoped external reviewer for evidence, receive an attributed response, and have that response enter the existing governed reanalysis flow. It will also deliver read-only owner roll-up and Grounding map projections plus revocable, frozen, view-only sharing.

The user-visible result is:

1. The owner routes one issue to a reviewer.
2. An external reviewer sees only the assigned question and its cited source.
3. The reviewer confirms or rejects with an evidence note.
4. OSLO records the response under the reviewer's identity and queues reanalysis.
5. Only reanalysis changes the issue lifecycle or integrity read.
6. The owner sees the response in the pending work, notification feed, roll-up and Grounding map.
7. The owner can withdraw the request or share a frozen, revocable snapshot without creating a seat or entitlement charge.

## 2. Authoritative basis

- `release-2/canon/product/OSLO_R2_DELTA_SLICE_MAP_2026-08-06.md`
- `release-2/slices/06-collaboration-reviewer-rollup-share.md`
- `release-2/slices/09-doctrine-guardrails-integration-map.md`
- DL-166, DL-168, DL-169, DL-204 and DL-205 as referenced by the Slice 6 design
- Existing application security and delivery rules in `code/AGENTS.md`

The older R1 "Slice 6 — Issues & Recommendations" numbering is not the R2 Slice 6 scope. Existing Issues behavior remains a Slice 1–5/Slice 2 regression dependency and must not be removed.

## 3. Agreed scope

### In scope

- External reviewer request → delivery → pending → response → attributed evidence → reanalysis round-trip.
- Collaborator/Delegate-PM full-read route and co-grounding affordance.
- External-reviewer scope enforced in the API and data layer, not only hidden in the UI.
- Confirm and reject responses, including the rejected-evidence → Needs a fix fork.
- Request withdrawal, token expiry, reroute invalidation and append-only history.
- Awaiting-evidence and reviewer-response states in the main Issues/read experience.
- Read-only owner roll-up projection.
- Read-only Grounding map projection with issue deep links.
- Frozen, recipient-bound, view-only shared snapshots with revocation.
- Minimal snapshot view audit with disclosed tracking.
- Salience-filtered notifications for routed responses and direct mentions.
- OSLO-drafted invitation after a reviewer response; explicit user send only.
- Desktop, tablet and mobile behavior, accessibility and complete failure states.

### Out of scope

- Live collaborative editing.
- Automatic invitations or messages sent without user confirmation.
- Advanced enforced Owner-versus-Delegate permission differences; those roles are display-level in this slice.
- Recipient-tailored snapshot variants or automatic supersession.
- Billing changes; reviewers and Viewers remain unmetered.
- Reports/export work assigned to R2 Slice 7.
- Feedback/survey/funnel telemetry assigned to R2 Slice 8.
- New issue-lifecycle doctrine; Slice 6 consumes the Slice 2 lifecycle.

## 4. Working product bindings

These are implementation-plan bindings from the grill, not new canonical decisions.

| Topic | Working binding |
|---|---|
| Roles | Owner has full control; Delegate-PM sees the full read and may co-ground; External sees one question and source; Viewer sees one snapshot. |
| External review token | Bound to one review request, question and source; seven-day expiry; one active token per route; revoked on withdrawal or reroute. |
| Reviewer delivery | Email link plus in-app delivery state. Use a bounded three-attempt delivery policy, then expose copy-link/manual resend without claiming delivery. |
| Reviewer response | Confirm or reject with a required evidence note. Submission is idempotent and creates an attributed record. |
| Reanalysis | Response enqueues the existing batched reanalysis path. The response handler never resolves an issue directly. |
| Shared snapshot | Frozen at creation, recipient-bound, view-only, revocable, unmetered; retain the current 30-day link expiry unless owner changes it. |
| Snapshot replacement | Owner explicitly creates a new snapshot and revokes an earlier one; no automatic supersession. |
| View audit | Snapshot ID, recipient, first/last viewed timestamp only; disclose tracking; retain for 90 days. |
| Notifications | Reviewer response, rejection and direct mention are salient; routine/self acknowledgements remain quiet. |
| Invitation | OSLO drafts after a useful external response; user explicitly sends it. |

## 5. Current implementation and gap analysis

| Capability | Reuse | Missing or incorrect for R2 Slice 6 |
|---|---|---|
| Comments and mentions | `project_comments`, API endpoint and issue discussion UI exist. | Add notification salience rules and pinned proof that comments never write lifecycle, provenance or integrity. |
| Snapshot sharing | Hashed bearer token, retained assessment snapshot, public page, expiry and revocation already exist. | Add recipient binding, view audit/consent, never-metered proof and R2 share-panel parity. |
| External review links | Hashed token, expiry, revoke, public page and response table already exist. | Current public payload includes the full `snapshot_json`; replace it with a strict `{question, source}` DTO and hard 403 scope enforcement. |
| Reviewer response | Response is stored and can later be promoted by the owner. | R2 requires the response itself to enqueue an attributed Slice 2 act and Slice 3 reanalysis; remove the extra "Use as project evidence" decision for confirm/reject responses. |
| Reviewer verdicts | `approve`, `reject`, `comment`, `suggest_alternative` exist. | Bind confirm → `basis=answered`; reject → attributed flag/Needs a fix; keep comment isolated from evidence. |
| Reviewer state | Invite, response and revoke records exist. | Make requested/delivered/pending/answered/withdrawn states explicit and observable. |
| Roles | Current collaboration response models expose only `owner`. | Add display-level Delegate-PM and External/Viewer representations; hard-enforce External only. |
| Awaiting evidence | Main read has routed and awaiting trays. | Bind them to real review-request delivery/response state and refresh after the batch lands. |
| Grounding map | A provenance/inference map exists. | Add the R2 node projection `grounded|addressed|routed|inferred`, enforce read-only behavior and deep-link nodes to their issue. |
| Owner roll-up | Parts exist across Overview, provenance and collaboration state. | Add one read-only projection containing integrity gate, trend, owner queue, reviewer state and who-is-grounding-what. |
| Notifications | History events exist. | Add a salience-filtered routed-response source and quiet routine/self events. |
| E2E | Existing `slice-six.spec.ts` tests the older Issues slice. | Preserve that test as an Issues regression, reclassify its name, and create the real R2 Slice 6 collaboration tracer. |

## 6. Architecture and contracts

### 6.1 Domain services

Split the current large collaboration service behind cohesive injected boundaries:

- `ReviewRequestService`: create, deliver, respond, withdraw, reroute and expose scoped public DTOs.
- `SharedSnapshotService`: create recipient grant, resolve frozen snapshot, record disclosed view and revoke.
- `CollaborationProjectionService`: owner roll-up, Grounding map and awareness-feed projections; read-only dependencies only.
- Reuse the existing Slice 2 issue-lifecycle/attestation service and Slice 3 reanalysis queue. Do not duplicate lifecycle logic inside collaboration.
- Keep SMTP/Postmark, SQL, token generation and notification delivery as injected adapters.

### 6.2 Data migration

Create one additive Supabase migration that extends existing collaboration tables rather than starting a second history.

Proposed additions:

- `project_review_grants`: `scope_kind`, `question_text`, `source_ref`, `source_excerpt`, `delivery_state`, `delivery_attempts`, `delivered_at`, `responded_at`, `withdrawn_at`, `token_version`.
- `project_review_responses`: normalized verdict, `basis='answered'`, evidence reference, attributed reviewer identity and enqueue/idempotency key.
- `project_share_links`: recipient name/email or recipient identifier and explicit active/revoked state if not already derivable.
- `project_snapshot_views`: snapshot/share reference, recipient reference, first/last viewed timestamps and retention deadline; no behavioral trail.
- Preserve SHA-256 token hashes only. Never persist or log raw review/share tokens.
- Add indexes for active request by issue, active share by project/recipient and response idempotency.
- Extend RLS so workspace members manage requests/shares, while public token resolution goes through narrowly scoped server functions only.

### 6.3 API surface

FastAPI/OpenAPI remains the source of truth. Prefer explicit R2 endpoints while keeping compatibility adapters for existing routes during migration.

- `POST /v1/projects/{project_id}/issues/{issue_id}/review-requests`
- `GET /v1/projects/{project_id}/review-requests`
- `DELETE /v1/projects/{project_id}/review-requests/{request_id}`
- `POST /v1/projects/{project_id}/review-requests/{request_id}/resend`
- `GET /v1/public/reviews/{token}` → strict question/source DTO only
- `POST /v1/public/reviews/{token}/responses`
- `GET /v1/projects/{project_id}/collaboration/roll-up`
- `GET /v1/projects/{project_id}/collaboration/grounding-map`
- `POST /v1/projects/{project_id}/shared-snapshots`
- `DELETE /v1/projects/{project_id}/shared-snapshots/{share_id}`
- `GET /v1/public/shared-snapshots/{token}`

Every mutation accepts an idempotency key or has a stable server-derived equivalent. Public token routes return generic unavailable copy without exposing whether a project, issue or recipient exists.

### 6.4 Hard security boundary

- A scoped review token authorizes only its public review GET and response POST.
- The public review response contains reviewer display name, expiry, question, cited source metadata/excerpt and response state—never the full assessment snapshot, all issues, artifacts, workspace members or project history.
- Presenting a review token to any unrelated resource returns 403.
- Expired, revoked, responded, withdrawn and rerouted states fail closed with non-enumerating responses.
- A reroute revokes the previous token before a new token is committed.
- Authorization is enforced in API/service queries and RLS, with negative tests at both boundaries.
- Reviewers and Viewers bypass entitlement evaluation completely; tests assert zero `gate_hit` events.

## 7. UI/UX plan

### Owner flow

1. From an issue, choose **Ask for evidence**.
2. Choose **Project collaborator** or **External evidence holder**.
3. For external review, show exactly what will be shared: question and cited source.
4. Enter reviewer name/email, then explicitly send or copy the link.
5. Show server-confirmed delivery state: Draft, Sending, Delivered, Delivery failed or Awaiting response.
6. Route the item into **Awaiting evidence** with reviewer, expiry and withdraw/resend actions.
7. On response, show an attributed notification and pending-reanalysis state.
8. When the batch lands, move the issue according to Slice 2 rules and keep the review history append-only.

### External reviewer flow

1. Open a branded, account-free scoped page.
2. See only reviewer name, project display name, assigned question and cited source.
3. Choose Confirm or Reject and enter a required evidence note.
4. Submit once; render a server-confirmed receipt and state that no account or seat was created.
5. Never expose navigation into the project or any unrelated snapshot content.

### Collaborator flow

- A workspace collaborator opens the full read through authenticated access and co-grounds using the same issue action/attestation path.
- Role labels are visible, but Owner-versus-Delegate enforcement beyond current editor access is deferred.

### Roll-up and Grounding map

- Roll-up shows the weakest integrity gate, direction-only trend, decision queue, pending reviewers, who-is-grounding-what and the basis of the read.
- Grounding map renders detail-level nodes as grounded, addressed, routed or inferred.
- Both are read-only. Clicking a row/node deep-links to the actionable issue surface.
- No inline fix, confirm, comment or write control may exist on these projections.

### Share flow

- The owner chooses a recipient and creates a frozen view-only snapshot.
- The UI clearly distinguishes **Share snapshot** from **Export**.
- Show recipient, created/expiry/viewed state and a Revoke action.
- A revoked or expired link renders a generic unavailable page.
- The Viewer page discloses that view timestamps are recorded and that the content is a frozen snapshot.

### Responsive and accessibility behavior

- Desktop: keep the R2 fixed-width OSLO rail; collaboration panels must not shift the header or document center.
- Mobile: owner composer and public reviewer response become full-width sheets/pages with sticky primary action and no horizontal overflow.
- Use semantic headings, fieldsets and live regions; trap/restore focus in dialogs; support Escape; visible focus rings; 44px touch targets; reduced-motion parity.
- Every asynchronous action has pending, success, timeout/error and retry states. Never show "sent", "recorded" or "resolved" before server confirmation.

## 8. Delivery increments and TDD sequence

### Increment 0 — Characterize and protect existing behavior

- Add characterization tests around current review grants, share links, comments and public pages.
- Rename/reclassify the existing old-numbered Slice 6 Issues E2E as an Issues/Slice 2 regression without deleting it.
- Add failing guards for GT-08, GT-14 and GT-17 before behavior changes.

Exit: current behavior is captured and the security leak is reproduced by a red test.

### Increment 1 — External-review tracer bullet

- Owner routes one real issue with a real citation.
- Server creates a single-question token.
- External reviewer page renders only question/source.
- Reviewer confirms with an evidence note.
- Response is stored, attributed and queues one reanalysis batch.
- Owner sees Awaiting → Response received → Analysis pending → settled result.

Exit: smallest UI → API → DB → event → reanalysis path is green.

### Increment 2 — Security, rejection, withdrawal and reroute

- Enforce 403 for every unrelated resource.
- Add expiry, revoke, already-responded, reroute and stale-link handling.
- Map Reject to attributed flag/Needs a fix.
- Implement withdrawal as append-only reversal and preserve prior request/response records.
- Prove duplicate response/delivery/reanalysis calls are idempotent.

Exit: all hard access and lifecycle negative tests pass.

### Increment 3 — Collaborator and delivery lifecycle

- Bind authenticated collaborator routing to full-read co-grounding.
- Add Draft/Sending/Delivered/Failed/Awaiting/Answered/Withdrawn states.
- Add bounded email retry and copy-link fallback.
- Keep Owner/Delegate labels display-level while External remains enforced.

Exit: collaborator and external routes are clearly distinct and observable.

### Increment 4 — Read-only owner projections

- Build server projections for roll-up and Grounding map.
- Render R2 prototype-aligned screens and deep links.
- Add pinned no-write tests by intentionally handing projections a write-capable dependency and requiring rejection.

Exit: projection data matches the current read and no projection can mutate state.

### Increment 5 — Recipient-bound frozen sharing

- Extend snapshot creation with recipient binding and view audit.
- Add disclosure, expiry, frozen-content and revocation behavior.
- Verify post-snapshot project edits/reanalysis never alter the Viewer payload.

Exit: active snapshots are frozen; revoked snapshots 404; Viewers are unmetered.

### Increment 6 — Notifications and user-controlled invitation

- Add salience-filtered routed-response notifications.
- Keep routine/self events quiet and comments non-grounding.
- Draft the invite-to-own-read offer after a useful external response; require explicit user send.

Exit: the owner cannot miss a response, and OSLO never auto-sends.

### Increment 7 — UI parity, responsive QA and regression closure

- Complete desktop/mobile prototype comparison.
- Add loading/error/timeout/retry states, focus management and reduced-motion coverage.
- Run the real-document collaboration journey and full Slice 1–5 regression suite.

Exit: no open release-blocking UI, functional, access-control or regression defect.

## 9. Trackable implementation issues

| ID | Outcome | Primary acceptance test |
|---|---|---|
| S6-01 | Scope external reviews to one question and source | Full snapshot/artifact/project requests with review token return 403. |
| S6-02 | Persist explicit review-request lifecycle | Requested → Delivered → Pending → Answered/Withdrawn is durable and idempotent. |
| S6-03 | Enqueue attributed reviewer responses | Confirm writes `basis=answered`; only the resulting reanalysis changes the issue. |
| S6-04 | Route rejection to Needs a fix | Reject creates an attributed flag and never marks Resolved. |
| S6-05 | Make reviewer decisions reversible | Withdraw reopens live state through reanalysis and appends rather than erases. |
| S6-06 | Deliver and retry review requests honestly | UI never says Delivered before provider confirmation; terminal failure offers retry/copy. |
| S6-07 | Add collaborator full-read co-grounding | Collaborator uses authenticated issue acts; External cannot cross the scope boundary. |
| S6-08 | Add read-only roll-up projection | Roll-up matches read state and has no mutation path. |
| S6-09 | Add read-only Grounding map projection | Node counts/states match issues and every node deep-links without writing. |
| S6-10 | Add recipient-bound frozen sharing and view audit | Edit after sharing does not change Viewer payload; revoke returns 404. |
| S6-11 | Add salience notifications and invite draft | Reviewer response surfaces; routine events stay quiet; invite requires Send. |
| S6-12 | Complete desktop/mobile/a11y E2E and regression | Full Slice 6 tracer plus Slice 1–5 suite passes. |

Each issue follows RED → GREEN → REFACTOR and includes API, UI or integration coverage proportional to its boundary.

## 10. Test and QA matrix

### Backend unit and integration

- Review-request state machine and idempotency.
- Token hashing, expiry, revocation, reroute and response consumption.
- Confirm/reject attribution and `basis=answered`.
- Response → one batch → only-reanalysis-resolves.
- Withdraw appends and preserves activation/history.
- Snapshot freezing, recipient binding and view audit retention.
- Notification salience and comment isolation.
- Tenant isolation and RLS across two workspaces.

### Pinned negative guardrails

- GT-02: reviewer and Viewer operations are never metered.
- GT-08 and GT-17: scoped token leaks nothing; stale/rerouted token fails closed.
- GT-12: comment/@mention never grounds.
- GT-14: roll-up/Grounding map cannot write.
- GT-25: withdrawal appends and never erases.
- GT-26: reviewer answer basis is typed and attributed.
- GT-A1: no premature sent/recorded/resolved UI.
- GT-A3: every round-trip has error/timeout/retry behavior.

Activate the corresponding entries in `ci/r2_guardrails.json` only when their concrete tests exist and pass.

### Frontend component tests

- Owner composer preview, role choice and exact shared scope.
- Pending/delivered/failed/responded/withdrawn displays.
- External reviewer confirm/reject, errors and already-responded receipt.
- Awaiting-evidence tray refresh after response and batch.
- Roll-up/Grounding map read-only affordances and issue deep links.
- Share recipient, viewed/expiry/revoke states.
- Keyboard/focus and responsive behavior.

### Desktop/mobile Playwright tracer

1. Analyze a real multi-section project document that produces cited issues.
2. Route one issue to an external reviewer.
3. Assert the public page contains the chosen question/source and none of the other artifacts/issues.
4. Confirm as reviewer and verify the owner receives an attributed pending response.
5. Wait for reanalysis and verify the lifecycle result.
6. Route a second issue, reject it and verify Needs a fix.
7. Withdraw/reroute and prove the old link fails closed.
8. Open roll-up and Grounding map, deep-link to an issue and prove no projection write occurs.
9. Share a snapshot, then edit/reanalyse the live project; verify the Viewer still sees the frozen copy.
10. Revoke the snapshot and verify 404/unavailable behavior.
11. Repeat critical reviewer/share paths at mobile width and assert no horizontal overflow.

### Regression gate

- Full web unit/integration suite.
- Full API suite and Ruff.
- ESLint, TypeScript and production build.
- R2 guardrail registry and active tests.
- Existing Slice 1–5 desktop/mobile Playwright suite.
- Git whitespace check.

## 11. Observability

Emit durable, tenant-scoped events without raw tokens or sensitive source excerpts:

- `review.requested`
- `review.delivery_attempted`
- `review.delivered`
- `review.delivery_failed`
- `review.responded`
- `review.withdrawn`
- `review.rerouted`
- `notify.routed_response`
- `share.created`
- `snapshot.viewed`
- `share.revoked`
- `invite.drafted`
- `invite.sent`

Every event carries project/workspace/request correlation IDs, actor type, timestamp and outcome. Reanalysis events retain their existing causation link to the response/attestation event.

## 12. Risks and controls

| Risk | Control |
|---|---|
| Existing public reviewer page leaks the full snapshot | Make the strict DTO and 403 tests the first implementation increment. |
| Duplicate reviewer submissions trigger multiple runs | Unique response constraint plus idempotency key and batch coalescing. |
| A manual handler resolves an issue | Reuse Slice 2/3 services; GT-10 remains gating. |
| Review token appears in logs/history | Hash at rest, scrub URL query/path values and forbid raw-token event payloads. |
| Roll-up or map grows a shadow write path | Separate read-only service interface and pinned negative GT-14. |
| Viewer sees future project changes | Snapshot ID pinned at creation and frozen-payload regression test. |
| Email provider delay produces dishonest success | Server-confirmed delivery states, bounded retry and manual copy-link fallback. |
| Existing R1 collaboration tests are lost | Characterize before refactor; migrate routes with compatibility coverage. |
| Slice numbering causes test/report confusion | Reclassify the old Issues Slice 6 tracer and name new tests `r2-slice-six-collaboration`. |
| Mobile panels shift the established R2 shell | Explicit desktop/mobile visual comparison and overflow assertions. |

## 13. Definition of done

Slice 6 is complete only when:

- All twelve implementation issues meet their acceptance tests.
- External scope is hard-enforced and proven by 403 negative tests.
- Confirm/reject responses are attributed and enter exactly one governed reanalysis batch.
- Comments remain discussion-only.
- Roll-up and Grounding map are demonstrably read-only.
- Shared snapshots are frozen, recipient-bound, revocable and unmetered.
- Reviewer responses are salient; routine events remain quiet; invitations require user send.
- Desktop/mobile prototype comparison, accessibility checks and the real-document E2E tracer pass.
- Full Slice 1–5 regressions, build, lint and guardrails pass.
- AI review, human code review and manual QA are recorded.
- Deployment is performed only after owner approval, followed by live health/log and authenticated smoke verification.

## 14. Recommended execution order

Implement in this order: **S6-01 → S6-02 → S6-03 → S6-04/S6-05 → S6-06/S6-07 → S6-08/S6-09 → S6-10 → S6-11 → S6-12**.

This front-loads the current security gap and proves the complete external-review path before expanding the projections, share polish and notification layer.
