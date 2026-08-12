# R2 Slice 2 implementation traceability

Date: 2026-08-13
Status: implemented and browser-verified; combined spoken screen-reader gate owner-deferred (non-canonical)

This record maps the owner-approved Slice 2 design to existing Release 1 contracts and Release 2 guards. It does not ratify product doctrine; the signed Slice 2 design and owner decisions remain authoritative.

| Observable outcome | Contract / guard | Existing seam | Implementation target | Verification |
|---|---|---|---|---|
| Only reanalysis resolves | AE-03, ISS-01…04; GT-10 | issue actions + Slice 3 batching | an act returns `addressed`/`routed`; only a landed pass changes terminal lifecycle state | API integration + negative tests |
| Confirm/answer are typed attestations | CLR-01, CRR-01…05; GT-26 | clarification evidence + ReviewRequest/StakeholderResponse seam | append-only attestation with BASIS, attribution, evidence reference, and immutable history | domain + API tests |
| Flag credits Grounding, not Viability | ISS-01…04; GT-11 | Slice 1 integrity issue projection | first-class flag attestation; linked statement remains inferred and Viability stays unchanged | domain + integrity tests |
| Fix does not fabricate Grounding | REC-04, AE-03; GT-27/33 | governed artifact edit + reanalysis | mitigated item renders in “Acted on · not yet closed” until separately grounded | domain + UI negative tests |
| Withdrawal appends and reanalyzes | AE-03; GT-09/25 | pending Undo + append-only history | reversal record supersedes live effect without erasing the prior act; activation remains latched | API integration tests |
| Comment never grounds | CHAT-01…04; GT-12 | collaboration comments | comment path cannot write lifecycle, provenance, BASIS, or integrity | pinned negative test |
| Reviewer response is evidence | CRR-01…05; GT-25/26 | collaboration review response | approve grounds with `answered`; reject creates an attributed flag; both resolve only through reanalysis | API integration tests |
| Build proposals resolve shared findings | DL-211; GT-51/53 | issue action + artifact edit | shared resolver state; all required build resolvers must land before the finding closes | API integration tests |
| Inference/optional proposals stay additive | DL-211; GT-52 | proposed responses | accepting an OSLO guess moves no Grounding band | pinned negative test |
| Findings/proposals stay itemized | DL-211; GT-54/55 | issue card + folded read | one independently actionable row per finding/proposal, never merged prose | UI structural tests |
| Cleared worklists still guide the user | GT-56 | Overview next-move guidance | start-here points to acted-on-not-closed or pending review work instead of disappearing | UI negative test |

## Accepted owner choices

- `answered` is a required BASIS, ranked below `verified-directly`, with visible responder attribution.
- Reviewer rejection appends a first-class attributed flag and routes the issue to needs-a-fix.
- Withdrawal immediately reopens live state, appends a reversal, preserves all prior records and the activation latch, and queues confirming reanalysis.
- `groundMitigated` appends a separate grounding attestation and keeps the earlier fix attestation.

## Scope firewall

Slice 2 builds on the verified Slice 1 issue object and Slice 3 reanalysis writer. It does not implement Release 2 Slices 4–10, which remain owner-blocked.

## Implementation and verification outcome

- The owner-act loop is live end to end: confirm, answer, flag, fix, ground, route, withdraw, reviewer approve/reject, and discussion-only comment paths are typed and append-only.
- Manual owner-work regression passed in the Codex in-app browser. Routing created a real scoped review grant, moved the issue to **Awaiting evidence**, and withdrawal restored the open ranked queue without deleting history. A separate confirmation completed reanalysis and moved the item to **Resolved**.
- Proposal decisions are itemized and synchronized across the folded read, issue card, and artifact surfaces. A live Reject check exposed a missing history run identifier; the source-read fallback and database integration regression were added, then the Reject flow passed and reduced the visible proposal count immediately.
- Side-by-side visual review used the owner-provided R2 queue and expanded-issue references at matched desktop states. The masthead, workspace-open notice, ranked queue, inline issue hierarchy, OSLO Proposes group, lifecycle trays, and governed OSLO rail have the same applicable visual structure. Live titles, counts, findings, and evidence remain backend-driven rather than copied prototype fixtures.
- Accessibility semantics expose named main/complementary/region/dialog landmarks, labelled lifecycle controls, expanded/collapsed state, and disabled/saving state. The owner-directed combined spoken screen-reader session for Slices 1–3 remains the only manual gate not run.

### Fresh verification evidence

| Gate | Result |
|---|---|
| Full API regression | **316 passed**: 315 tests in the main run plus the isolated integrity UI-contract subprocess test |
| Full web regression | **143 passed** across 24 files |
| Slice 2 focused web/domain tests | **63 passed**: 53 web plus 10 lifecycle/proposal/UI-contract tests |
| R2 doctrine guardrails | **4 infrastructure + 17 active tests passed**; 60 registered, 18 active, 42 pending, 58 surfaces, 6/6 prototype corrections |
| Static checks | Ruff and ESLint passed |
| Production build | Next.js build and TypeScript validation passed |
| Live browser regression | Route, scoped grant, withdraw, proposal Reject, proposal count update, confirm, reanalysis, and Resolved tray passed |
