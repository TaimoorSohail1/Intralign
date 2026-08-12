# R2 Slice 3 implementation traceability

Date: 2026-08-12
Status: implementation working record (non-canonical)

This record maps the owner-approved Slice 3 build to existing Release 1 seams. It does not ratify product doctrine; the Release 2 canon and owner decisions remain authoritative.

| Slice 3 outcome | Contract / guard | R1 seam to reuse | R2 implementation target | Verification |
|---|---|---|---|---|
| Fast Pass is the first-read critical path | AE-01; R2 S3 AC-1/2; GT-23 | `AnalysisWorkflow`, analysis SSE, `AnalysisProgress` | Pass metadata and a progressive first-read experience driven by real run events; no Deep Pass awaited | API + component + browser tests |
| Deep Pass runs off-path and supersedes append-only | AE-02/AE-03; R2 S3 AC-1 | initial→extended hand-off, durable jobs, snapshots/history | Explicit pass kind/trigger; first-read publishes before a Deep job; later snapshot remains append-only | integration tests |
| Plan-affecting acts create one project batch | AE-03; R2 S3 AC-3/4; GT-10/24 | issue actions, answers, artifact edits, durable analysis jobs | durable pending changes, project consolidation key, configurable debounce/cooldown/max wait, one active pass | unit + API + integration tests |
| Only reanalysis changes the read | R2 S3 I1/AC-4 | addressed issue lifecycle; workflow publish is the writer | actions return addressed + stale metadata; only landed pass changes assessment/integrity | positive and negative tests |
| Read freshness is explicit | R2 S3 I4/AC-5 | overview last-good behavior | `fresh | stale | reanalyzing`, pending count, last-good run, visible “based on previous analysis” notice and Reanalyze now | API + UI tests |
| Failure preserves last-good and recovers | R2 approved failure policy | durable checkpoints/retry, overview `last_good` | one transient auto-retry, then visible manual retry; no blank read | service + browser tests |
| First-run freeze is presentation-only and latched | R2 S3 I2/I3/I7; GT-04/18 | membership orientation state | durable per-user×project onboarded / grounding-act count / ever-unlocked; default 2 owner-config; API never withholds read | API + component tests |
| “Your read moved” is causal | R2 S3 AC-9 | overview polling/history | transient on-read result; durable delayed/away notice with cause and pillar deltas; configurable threshold/linger | service + UI tests |
| Existing projects do not regress | owner-approved backfill | existing R1 project rows | migration backfills existing memberships/projects as onboarded and unlocked | migration inspection + integration test |
| Prototype parity is demonstrated | user acceptance requirement | R2 prototype/onboarding arc | exact analysis/progressive graph/outcome-confirmation and stale/reanalysis states using live data | same-viewport combined-image QA |

## Owner-approved operating defaults

- Batch debounce: 1.5 seconds.
- Batch cooldown: 5 seconds.
- Maximum batch wait: 16 seconds.
- Read-moved immediate threshold: 5 seconds.
- Read-moved linger: 16 seconds.
- First-run unlock: 2 grounding acts (`confirm`, `flag`, or `route`), configurable.
- Fast Pass: ≤60 seconds P95, ~45 seconds target; at 45 seconds show “still working”; by 60 seconds return an honest provisional/degraded read where possible.
- Normal grounding-act batches use scoped Fast reanalysis. Deep Pass is reserved for large, ambiguous, or explicit depth work.

## Verification record — 2026-08-12

- Full API regression: **303 passed**.
- Full web regression: **23 files / 131 tests passed**.
- Focused Slice 3 API and component coverage: passed.
- Ruff, ESLint, TypeScript, and Next.js production build: passed.
- R2 guardrails: **4 infrastructure + 9 active selectors passed**.
- Local database migration: applied successfully.
- Manual browser and identical-to-prototype gates: **open** because the selected in-app browser rejected the local page reload under its URL security policy. No browser substitution was used.

## Scope firewall

Slice 3 supplies the reanalysis/freshness/pass/freeze infrastructure and the analysis experience. Slice 2’s complete grounding-act lifecycle UI is not reimplemented here. Release 2 Slices 4–10 remain owner-blocked.
