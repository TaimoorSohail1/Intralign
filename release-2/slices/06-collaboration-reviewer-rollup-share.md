# R2 Slice 6 — Collaboration: Reviewer Round-Trip, Roll-up, Grounding Map, Share — Build Design

*Grill artifact · 2026-08-06 · DRAFT — awaiting sign-off. Derived from capabilities #3/#9/#10/#12/#13; audit §4.6 (R2G1…R2G11) + DL-L8/DL-L2/DL-166; the collaboration surfaces in the prototype. Builds on Slice 1 (integrity), Slice 2 (attestation ledger + route-as-act), and R1 sharing/comment/notification canon (§6).*

**Scope:** the scoped external-reviewer round-trip, the read-only **roll-up** and **grounding-map** owner projections, the redesigned revocable **share** (view-only snapshot), the role/access model (owner|delegate|external), and the k-factor invite. Keystone: the external reviewer is a **hard-enforced scope** (DL-L8); everything else is a read-only projection or view-only snapshot that must never emit a write.

## 1. Locked decisions
| # | Decision | Source |
|---|---|---|
| L1 | **External reviewer = SCOPED, hard-enforced.** Sees ONLY the routed question + source; 403 on anything else. Access-control guarantee, not display-only. | DL-L8; cap #3/#12; R2G1 |
| L2 | **Collaborator (delegate/PM) sees the full read and co-grounds.** | cap #3; proto `routeTo(k,'pm')` |
| L3 | **Round-trip = request→deliver→pending→respond→(evidence\|reject→flag)\|withdraw.** A reviewer answer **enqueues** and resolves on the batch, attributed to them. | cap #3; DL-205 |
| L4 | **Roll-up + grounding-map = read-only Disclose projections** over #7/#2/#3. **They never emit a write** — every row routes into the read to act. | cap #10; R2G3 |
| L5 | **Share the read = a revocable, view-only SNAPSHOT** — not the live workspace. Viewers take no seat, **never metered**. | cap #9; R2G9; DL-L2 |
| L6 | **A comment never grounds** — carried into the awareness feed unchanged. | D133/CR-2; cap #4; R2G8 |
| L7 | **Awareness feed salience-filtered (DL-166):** only miss-worthy changes surface; routine/self-ack quiet-moded. | DL-166; cap #13; R2G8 |
| L8 | **Owner vs delegate role model may be display-only this release**; external scope (L1) enforced regardless. | DL-L8; R2G4 |
| L9 | **k-factor invite = invite-to-own-read**; OSLO drafts, user sends; nothing auto-sent. | cap #3; R2G10 |

## 2. State Model
**Review-request lifecycle** (a facet of the Slice-2 `Issue`): `requested` (composer open) → `delivered` (`state='routed'`, `routedTo={name,role,tier}`, `tier∈{pm=collaborator,ext=scoped}`) → `pending` (awaiting; in Awaiting-evidence group) → `answered·evidence` (`addr.kind='confirm'`, `attestedBy=reviewer`) | `answered·rejected` (`addr.kind='flag'`, forks to needs-a-fix) | `withdrawn` (→`inf`, `confirmCount--`).
**Transitions** (only-reanalysis-resolves holds — Slice 2 INV-1): `routeTo(k,'pm'|'ext')`→delivered; `respondRoute(k,'approve')`→answered·evidence + `_scheduleReanalysis` (+ if ext, `inviteOffer`); `respondRoute(k,'reject')`→answered·rejected (`flagged`); `withdrawRoute`→withdrawn; `_completeReanalysis` grounds/flags attributed to the reviewer.
**Share-snapshot:** `active`→`revoked`. `shareAddRecipient` adds a Viewer (`view-only`, `viewed:false`); `shareRevoke` removes. A **revoked snapshot 404s**; active serves a **frozen** copy of the committed read.

## 3. Data / Object model *(build ON R1 SharedArtifact/StakeholderResponse/Comment/Notification — §6)*
- **ReviewRequest** `id · issueRef · scope{scoped,collaborator} · question · source · reviewer{identity,role,tier} · state · channel · deliveredTs · respondedTs`. A **scoped** request mints a **scope token** granting read of `{question, source}` ONLY (L1). Extends R1 `ReviewRequest` (which R1 left uncontracted).
- **StakeholderResponse** (reuse DL-049) `requestRef · verdict{confirm,reject} · evidenceRef(never a comment) · attributedTo · basis='answered'`. Admitted as evidence-attested; triggers batch re-read; reject→first-class flag attributed to them.
- **SharedSnapshot** `id · readRef(frozen at snapshot time) · recipients[]{name,role,access:'Viewer',viewed} · link · state{active,revoked} · viewAudit[]`. **Never metered**. Distinct from R1's live-object share: R2 shares the *read* as a frozen artifact.
- **Role/Access** `owner|delegate|external`. owner/delegate = display-only visibility this release; **external = hard-enforced scope** (L1). No R1 `delegate-PM` role (R2G4) — net-new, owner-decision open.
- **Roll-up / grounding-map projections** (read-only, no persisted object): roll-up derives `min(V,G,A)` + gate + trend + owner decision-queue + who's-grounding-what + "what it rests on", role-scoped, every row deep-links (`rollupGo`). Grounding-map: per-detail node state `grounded|addressed|routed|inferred`, click opens the issue.

## 4. Event Model
| Event | Emitter | Notes |
|---|---|---|
| `review.requested` | `routeTo` | `scope='scoped'` mints the scope token; counts as a `grounding_act` |
| `review.delivered` | delivery channel | email/in-app; scoped surface link for `ext` |
| `review.responded` | `respondRoute` | enqueues the batch; **resolves only on reanalysis** |
| `review.withdrawn` | `withdrawRoute` | reverts to `inf`; `confirmCount--`; append (never erase) |
| `invite.drafted`/`invite.sent` | `inviteToRead`/`shareInvite` | OSLO drafts, user sends; honest "awaiting them", never fabricated "joined" |
| `share.created`/`share.revoked` | `shareAddRecipient`/`shareRevoke` | Viewer grant/revoke; view-only; never metered |
| `snapshot.viewed` | Viewer open | feeds `viewAudit` |
| `notify.routed_response` | on `review.responded` | **DL-166 salience:** routed answer is miss-worthy → surfaces; routine/self-ack quiet-moded |
| `notify.comment` | comment/@mention | discussion only — never carries a grounding effect |

## 5. Honesty invariants (testable)
- **INV-1 external-reviewer-scope-hard-enforced [403]** — a scoped token authorizes `{question, source}` ONLY; any other resource → 403 (not display-only).
- **INV-2 projections-cannot-emit-a-write [pinned negative]** — roll-up/grounding-map handlers have no write path to plan/finding/attestation/History; every action deep-links into the read.
- **INV-3 Viewers-and-reviewers-never-metered** — sharing a view-only read + asking anyone to ground a line consume no seat, hit no entitlement check.
- **INV-4 comment-never-grounds-in-the-feed** — a comment/@mention in the feed carries no write to prov/basis/state.
- **INV-5 share-is-a-frozen-snapshot** — serves the committed read at snapshot time; live edits don't leak to a Viewer; a revoked snapshot 404s.
- **INV-6 reviewer-answer-grounds-attributed** — confirm sets `attestedBy=reviewer`, `basis='answered'`, grounds on the batch as "Confirmed by {name}", never as the owner's own evidence.
- **INV-7 routed-response-notification-is-salient (DL-166)** — routed answer surfaces as miss-worthy; routine/self-ack quiet.
- **INV-8 withdraw-appends-never-erases** — `withdrawRoute` reverts live state + decrements the gate, but request/response records persist; the activation event stays immutable.

## 6. FE↔BE integration bindings
| FE surface | Reads | Written by | Resolved/gated by |
|---|---|---|---|
| Ask-for-evidence composer | `PM_CONTACT`/`EXT_CONTACT` | `routeTo(k,'pm'\|'ext')` → `review.requested` | scope token minted; enqueue on reply only |
| Awaiting-evidence group (`_awaitingGroup`) | `state==='routed'`, `routedTo` | `respondRoute`/`withdrawRoute` | reviewer reply → reanalysis batch |
| Scoped reviewer surface (external) | scope token → `{question,source}` | reviewer confirm/reject | **403 on anything else** |
| Roll-up door (`rollupDoorHTML`/`_ovwDoorHTML`) | `min(V,G,A)`, risks, ledger, reviewer state; `_ownsOutcome()` role-scope | — (read-only) | `rollupGo` deep-link into read |
| Grounding map (`groundMapHTML`) | `_mapNodeState(it)` | — (read-only) | `_openMapItem(k)` opens the issue |
| Redesigned share panel (`doorBody('share')`) | `_shareRecipients`, `_shareReviewerCount/Rows`, `_shOpen` folds | `shareAddRecipient`/`shareRevoke`/`shareCopyLink` | snapshot active/revoked; Viewers unmetered |
| Invite (`inviteToRead`/`shareInvite`) | `attestedBy` (fresh external) | `invite.drafted`→user sends | honest "awaiting them" |
| Awareness feed (notif door) | `HISTORY`, salience filter | — | `notify.routed_response` surfaces; comments quiet |

## 7. R1 reuse vs net-new
**Reuse (§6):** `SharedArtifact`/`POST /shares`/`:revoke` + lifecycle + tenant isolation; `Comment`/`Mention` + "a comment never grounds" (enforced in the feed); the `StakeholderResponse` reviewer-response→evidence seam (DL-049); `Notification` core + `:view`/`:dismiss`.
**Net-new:** the scoped-reviewer workflow (creation, delivery channel, enforced scope token, pending tracking, reject→flag — R2G1/G2/G7/G8); the owner-glance projections (roll-up + grounding-map read-only Disclose with the pinned no-write negative — R2G3); the role model (owner/delegate display-only + external hard-enforced — R2G4/DL-L8); share-the-read-as-frozen-snapshot (R2G9); the salience/quiet-mode filter + routed-response source (R2G8/DL-166); the k-factor invite delivery (R2G10).

## 8. Open items / placeholders
- **[owner] R2G4** owner vs delegate-PM role/access matrix (this release: display-only per DL-L8; enforced matrix deferred).
- **[owner] R2G11** recipient-tailoring enum + auto-supersession trigger.
- **[spec]** scope-token shape + revocation (TTL, single-question binding, re-issue on re-route; the 403 copy for a stale scoped link).
- **[spec]** `viewAudit` retention/consent.
- **[carry-forward]** delivery channel (email/in-app) + retry (shared with cap #13).

## 9. Acceptance criteria
1. A scoped external reviewer reads the question + source and **nothing else**; any other resource → **403**.
2. A collaborator sees the full read and can co-ground.
3. **Roll-up has no write path** — a pinned QA negative asserts no roll-up/grounding-map action mutates plan/finding/attestation/History; every row deep-links.
4. A **revoked snapshot 404s**; while active it serves a frozen copy — a post-snapshot edit doesn't appear to a Viewer.
5. A reviewer **answer grounds attributed to them** ("Confirmed by {name}", `basis='answered'`), only on the batch.
6. A reviewer **reject** forks the item to needs-a-fix (flag attributed), not Resolved.
7. **Withdrawing** reverts the item, decrements the live gate, **appends** a record; prior records persist; activation event immutable.
8. **Viewers and reviewers are never metered.**
9. A **comment/@mention** in the feed leaves state/prov/basis/bands unchanged.
10. A **routed-item response** surfaces as miss-worthy (DL-166); routine changes stay quiet.

*On sign-off, the collaboration surfaces already in the prototype become the ratified reference — with the external-reviewer scope promoted from simulated copy to a hard-enforced access guarantee.*
