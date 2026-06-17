# DL-067 — Console-Driven DL Landing (automate the DL-065 flow server-side)

- **Date:** 2026-06-16 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A intent (extends the R5 serializer) + Class-D realization (engineering build; owner-approved in the interim while the EM seat is deferred, per DL-063).
- **Source:** DL-063 (R5 — Console as sole serializer); DL-065 (recording discipline); owner request 2026-06-16 to make the Console the one-click front door for DLs.

## Decision
Make the **Founder Console Decide lane the one-click front door for landing decisions**, by automating the DL-065 flow **as a GitHub Actions workflow** (server-side) rather than via the local sandbox. The owner's **"Approve & Land"** action in the Console triggers the workflow; the workflow authors and numbers the record and opens a PR; **the owner still performs the final merge** (canon is never auto-merged).

## Why server-side (the key design choice)
The local sandbox can't push (no GitHub credentials) and suffers recurring `.git/index.lock` churn — both root causes of the 2026-06-16 friction, including the stale-clone mis-numbering that nearly assigned DL-067 the number DL-066. A GitHub Actions workflow runs **in GitHub** against current `main` with repo write access, so it numbers correctly, commits, pushes, and opens PRs cleanly, with **zero local git**. The owner's machine only ever does `git pull` to resync.

## Design
1. **`dl-land.yml` (workflow_dispatch)** — inputs: `slug`, `title`, `body` (markdown), `class`. Steps:
   - `git checkout -b decision/dl-<slug>` from fresh `main`.
   - Write `00_owner/decisions/records/DL-PENDING-<slug>.md` from inputs.
   - `python3 tools/dl_records.py next` → assign DL-NNN (off **current main** — no stale-clone risk); rename + stamp header (Status: Ratified, Decided by + date from inputs).
   - `python3 tools/dl_records.py index`; append the changelog `CHG-###`.
   - Run `python3 tools/doc_integrity_check.py` (must pass — fail-closed).
   - Push the branch and **open a PR** (via `gh`/API). Stop there — no merge.
2. **Console "Approve & Land" button** — in the Decide lane, calls the workflow dispatch (GitHub API) with the decision's slug/title/body. Surfaces the resulting PR link.
3. **Owner merges** the PR (the one irreversible, human-gated step). Then `git pull`.

## Conditions (safety rails)
1. **Never auto-merge canon.** The workflow opens the PR and runs the gate; merge stays an explicit owner action (preserves "owner ratifies/merges" and the green-gate rule).
2. **Fail-closed on the gate.** If `doc_integrity_check.py` fails, the workflow does not open the PR — it reports the error.
3. **Single serializer preserved (R5).** The workflow is the *only* automated landing path; no parallel agent stream lands canon while it's enabled.
4. **One in flight (R3).** The workflow refuses to start if an open `decision/*` PR already exists.
5. **Number-at-merge integrity (R2/R4).** Numbering happens inside the workflow run immediately before PR creation; the records guard still gates the PR.

## Realization (engineering build, follow-on)
Add `.github/workflows/dl-land.yml`; a `gh pr create` step; wire the Console Decide-lane "Approve & Land" button to the dispatch; document the flow in `records/README.md` and `CLAUDE.md`. Test with a no-op decision before first real use.

## Supersedes/Amends
None. Realizes DL-063 R5 (serializer) on top of DL-065 (recording discipline); additive.

## Provenance
Founder Console Decide log, decided 2026-06-16 by Idris. Drafted under the DL-065 number-at-merge flow (`DL-PENDING` → DL-067 at landing).
