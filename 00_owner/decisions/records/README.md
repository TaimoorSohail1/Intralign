# Decision Records (DL-065+)

One file per decision (DL-065 onward), per **DL-065** (Decision-Recording Discipline). Decisions DL-029→DL-064 remain in the frozen `../decision_log.md`.

## Rules
- **Naming:** `DL-XXXX-slug.md` (zero-padded number, kebab-case slug). E.g. `DL-065-decision-recording-discipline.md`.
- **Drafting:** while in flight, name the file `DL-PENDING-slug.md`. The number is assigned **at merge** — run `python3 tools/dl_records.py next` to get the next number, rename the file, and stamp the header. (The CI guard fails if a `DL-PENDING-*.md` reaches `main`.)
- **Required header fields:** a top `# DL-XXXX — Title` line, and at least **Decision** and **Status**.
- **One PR in flight:** branch from fresh `main`, merge linearly (merge → pull → next).
- **Index:** `../decision_log.md`'s records index is generated — `python3 tools/dl_records.py index` — never hand-edited.

## Helper
- `python3 tools/dl_records.py next` — print the next free DL number (scans the legacy log + records).
- `python3 tools/dl_records.py index` — regenerate the records index in `decision_log.md`.
- `python3 tools/dl_records.py check` — validate records (also run inside `doc_integrity_check.py`).
