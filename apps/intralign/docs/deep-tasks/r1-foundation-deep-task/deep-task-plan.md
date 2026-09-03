# Deep-task plan — R1 Foundation (Phase I) + Wave A 00R

One branch (`feat/phase1-wavea-00r`), one fresh worker per task, strictly sequential.
Each slice is vertical and independently verifiable. Contract for Phase II tasks: **IC-WA-00R**.

## Slices

| # | Module | Slice (vertical outcome) | Phase | Depends on |
|---|---|---|---|---|
| 1 | DTM-0001 | App CI: 6-gate `app-ci.yml` scoped to `code/**`, each gate provably fails | I | — |
| 2 | DTM-0002 | Canonical schema: Supabase migrations, append-only enforced in PG, derived separated; pytest proof | I | — (CI proves it on merge) |
| 3 | DTM-0003 | Local env verified: supabase + compose up, backend boots, OTel trace visible locally | I | 0002 |
| 4 | DTM-0004 | Retain CHR repository: append-only CognitionHistoryRecord persistence + lineage (IC-WA-00R A3.5) | II | 0002, 0003 |
| 5 | DTM-0005 | Recompute backbone: triggers, stale detection, state machine, chain orchestration (LangGraph durable), last-known-good | II | 0004 |
| 6 | DTM-0006 | OBS-WA-00R: governed-output events, audit record, two-axis replay hooks; CI gate-5 → real | II | 0005 |

## Test strategy

- Every task: positive AND negative suites (negatives mandatory — QA governance).
- DTM-0002/0004: negatives prove UPDATE/DELETE on canonical tables **rejected by the database**.
- DTM-0005: negatives prove QA-WA-00R B3 (assessment-without-recompute impossible; CHR overwrite rejected; backbone produces no cognition; Derived never promoted).
- DTM-0006: replay tests — record-exact CHR replay; trigger/lineage reconstruction.
- Determinism tiers per Calibration Defaults: exact for records/rules (everything in this sequence is records/rules — no AI-numeric yet).

## Manual checks (EM or owner)

- Forced-failure proof per CI gate (throwaway PR flips each red) — DTM-0001 done-criterion.
- `supabase start && docker compose up -d` healthy on a clean machine — DTM-0003.
- Grafana shows one trace (if local observability confirmed) — DTM-0003.

## Done = Phase I exit gate (kickoff §7) minus parked items

Items 1–4 + 6 (local) covered by DTM-0001..0003; item 5 (Staging/Production) **parked on owner
Day-0 accounts**. Phase II 00R covered by DTM-0004..0006 against IC/QA/OBS-WA-00R.
Owner sign-off required between Phase I and Phase II tasks (DL-044: per-wave start is owner-authorized).
