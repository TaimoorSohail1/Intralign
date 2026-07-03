# DL-065 — Decision-Recording Discipline (sequencing & conflict elimination)

- **Date:** 2026-06-16 · **Status:** Ratified with Conditions · **Decided by:** Idris (Founder Console)
- **Class:** A (canon — amends how decisions are recorded under Framework 001). Full lifecycle.
- **Source:** `PROPOSAL_DECISION_RECORDING_DISCIPLINE.md`; evidenced by the 2026-06-16 git history (#25/#28/#29/#30/#31/#32, the duplicate DL-061, out-of-order DL-058/059/061, and the DL-061 recorded-but-not-applied drift). References DL-030/031, DL-033, DL-051/052, DL-053, DL-063.

> **Note:** This is the **first decision authored under the discipline it ratifies** — it lives as an individual record file (R1), not as an entry appended to the monolithic `decision_log.md`.

## Decision
Adopt the five-rule **decision-recording discipline**:

- **R1 — One file per decision.** New decisions are individual files at `00_owner/decisions/records/DL-XXXX-slug.md`. `decision_log.md` is **frozen as the historical ledger through DL-064** and carries a generated index of the records. No more shared-monolith appends → the merge-conflict class is removed.
- **R2 — Number at merge, not at draft.** Drafts are `records/DL-PENDING-slug.md`; the DL number is stamped only when the decision lands on `main` (use `tools/dl_records.py next`). No optimistic numbering → no duplicates/gaps.
- **R3 — One canon PR in flight, merged linearly.** Branch from fresh `main`; merge → `pull` → start the next. Never stack open canon PRs.
- **R4 — CI guard.** `tools/doc_integrity_check.py` validates the records regime: correct naming, header↔filename DL match, required fields, uniqueness, and no `DL-PENDING` on `main`. Violations fail the gate.
- **R5 — One serializer.** The Founder Console is the sole path that authors, numbers, and releases decisions to `main`. No second stream merges canon in parallel.

## Conditions
1. **Freeze, don't migrate** — DL-029→DL-064 remain in `decision_log.md`; only DL-065+ are records. The R4 guard validates `records/` only and does not retroactively fail the frozen legacy log (its known gaps — DL-060 parked, CHG-087 — are grandfathered).
2. The records **index is generated** (`tools/dl_records.py index`), never hand-edited, so it can't become a merge point.
3. The **Framework 001 doc** gets the formal R1–R5 amendment as a follow-on; `CLAUDE.md` is amended now (operative AI-contributor rules).

## Resulting Actions (realized in this change, CHG-094)
- Created `00_owner/decisions/records/` + this record + `records/README.md`.
- Added `tools/dl_records.py` (`next`, `index`, `check`).
- Extended `tools/doc_integrity_check.py` with the R4 records guard.
- Froze `decision_log.md` (header note + generated index section).
- Amended `CLAUDE.md` with R1–R5.

## Supersedes/Amends
Amends the decision-recording mechanics of Framework 001 (additive; no past decision changed). Makes DL-063 (Risk-Tiered Routing) operable by giving it a conflict-free recording substrate.

## Provenance
Founder Console Decide log, decided 2026-06-16 by Idris. First record under R1.
