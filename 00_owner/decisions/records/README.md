# Decision Records (DL-065+)

One file per decision (DL-065 onward), per **DL-065** (Decision-Recording Discipline). Decisions DL-029→DL-064 remain in the frozen `../decision_log.md`.

## Rules
- **Naming:** `DL-XXXX-slug.md` (zero-padded number, kebab-case slug). E.g. `DL-065-decision-recording-discipline.md`.
- **Drafting:** while in flight, name the file `DL-PENDING-slug.md`. The number is assigned **at merge** — run `python3 tools/dl_records.py next` to get the next number, rename the file, and stamp the header. (The CI guard fails if a `DL-PENDING-*.md` reaches `main`.)
- **Required header fields:** a top `# DL-XXXX — Title` line, and at least **Decision** and **Status**.
- **One PR in flight:** branch from fresh `main`, merge linearly (merge → pull → next).
- **Index:** `../decision_log.md`'s records index is generated — `python3 tools/dl_records.py index` — never hand-edited.

## Preferred landing path — the `dl-land` workflow (DL-067)
The easiest, no-local-git way to land a decision is the **DL Land** GitHub Actions workflow (`.github/workflows/dl-land.yml`): **Actions → DL Land → Run workflow**, fill in `title` + `body` (and optionally `slug`/`class`/`decided_by`). It runs server-side off current `main`, so it numbers correctly (no stale-clone risk), regenerates the index, appends the changelog, runs the gate **fail-closed**, and **opens a PR** — which the **owner merges** (canon is never auto-merged). The Founder Console "Approve & Land" button triggers this same workflow.

Do the steps below by hand only when you can't use the workflow.

## Helper
- `python3 tools/dl_records.py next` — print the next free DL number (scans the legacy log + records).
- `python3 tools/dl_records.py next-chg` — print the next free CHG number.
- `python3 tools/dl_records.py land --title "…" --body-file body.md [--slug … --class A --decided-by "…"]` — create the numbered record + index + changelog (this is what the workflow calls).
- `python3 tools/dl_records.py index` — regenerate the records index in `decision_log.md`.
- `python3 tools/dl_records.py check` — validate records (also run inside `doc_integrity_check.py`).
