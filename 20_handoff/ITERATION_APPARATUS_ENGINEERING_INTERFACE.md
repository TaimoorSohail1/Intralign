# How engineering interfaces with the iteration apparatus

**Audience:** @HamzaSohailCodes (dev lead) · @TaimoorSohail1 (engineer)
**Zone:** `20_handoff/` — the co-governed seam. Product and engineering both read this; neither owns it alone.
**Status:** interface contract. Not yet live — see §7.

---

## 1 · The one rule

**`20_handoff/ITERATION_QUEUE` is your day's work, and it is generated.**

Every row is derived from a governed object that already exists in the repository. There is no hand-add, and there is no hand-sort. If work is not represented by a durable object, it does not appear — and that is the point.

> **A chat message is not a source.** Work that lives only in an IM goes stale exactly the way an IM does. If you need something from product, or product needs something from you, the object comes first and the queue follows.

The file carries `⚠️ GENERATED — do not edit` at the top. `python3 tools/iteration_queue.py --check` fails the build if the committed queue has drifted from its sources, so editing it by hand is not a shortcut — it is a red build.

---

## 2 · Your day

Open `20_handoff/ITERATION_QUEUE`. It opens with the iteration goal, the window, and an open-row count, then four priority bands in fixed order:

| Band | Means | Derived from | Which release |
|---|---|---|---|
| **P0 · production-blocking** | A defect that blocks the release in build | `20_handoff/OBLIGATION_*.md` with `Status: OPEN` and the phrase *blocking for production* | **in build** (R2.0) |
| **P1 · freeze chain** | Exactly the §9.3 items not yet evidenced | `freeze_readiness_check.py` output — computed, never listed | **in design → freeze** (R2.1) |
| **P2 · apparatus** | The current layer's first increments | the iteration's `APPARATUS_PLAN` layer table | tooling |
| **P3 · due this iteration** | The register's own due verdict | `queued_work_check.py` against the design line — never re-derived | **in design** (R2.1) |

Each row is a table line: `id · what · owner · accepts · done when · source`.

- **owner** is who does it. It comes from the source object's `**Fix:**` field, not from an assignment made here.
- **accepts** is who signs it off. Not the same person.
- **done when** is the closing condition. It is the definition of finished — not "I pushed it".
- **source** is the file the row came from. Every row traces back; if you disagree with a row, argue with its source.

**The order is computed.** P0 outranks P1 by owner ruling of 2026-08-31: if production-blocking defects and the freeze chain compete for the same person, the defects win and **the freeze slips, deliberately.** You do not need to ask which to do first — the file has already answered.

---

## 3 · How to get work into the queue

Create the durable object. Three doors:

**A production-blocking defect → an obligation.** Add `20_handoff/OBLIGATION_<slug>.md`:

```markdown
# OBLIGATION — <one-line title>
**Status:** OPEN
**Fix:** <github-handle>
**Accepts:** <github-handle>
**Invariants violated:** GT-12, GT-45

<body — and include the phrase "blocking for production" if it is>

## 4 · DONE CONDITION
<the condition that closes it>
```

`Status: OPEN` puts it in the queue; anything else drops it out. The *blocking for production* phrase is what promotes it from P2 to P0. Keep the `**Invariants violated:**` list on its own declared line — the parser scopes GT ids to that line deliberately, because scanning the whole document once swept in ids that merely appeared in prose.

**Work that comes due on a date → a queued-work row** in the design line's `QUEUED_WORK`, with a `due:` and a machine-checkable `when:` predicate. The checker supports `ref-has-file:` and `ref-missing-file:` — use them whenever the condition lives on a different branch than the checker.

**A tooling increment → the apparatus plan's layer table.**

What you cannot do is add a row to `ITERATION_QUEUE`. That is not a restriction on you; it is the same rule for everyone including the owner.

---

## 4 · How work leaves the queue

**Satisfy the `done when` column.** Regenerate, and the row is gone. Rows are not "closed" by editing the queue.

**Deferral is an owner ruling, not a status.** A date passing is not a deferral. Pushing a row to the next iteration is recorded in `20_handoff/DEFERRALS.json` with the row id, where it lands, who ruled it, the date, and why — and deferred rows render in a visible tail of the queue, never hidden. *"No capacity" is a reason; "not done" is not.* A row deferred **twice escalates**, because the second slip means the row's premise is wrong, not its timing.

AI never defers. Neither does engineering. Ask the owner.

---

## 5 · Commands

```bash
python3 tools/iteration_queue.py             # regenerate the queue
python3 tools/iteration_queue.py --check     # FAIL if the committed queue is stale
python3 tools/iteration_queue.py --self-test # RED-proves ordering, derivation, freshness

tools/git_preflight.sh <expected-branch>     # run before ANY git write; exit 0 = safe
tools/git_preflight.sh --self-test
```

⚠️ **Read exit codes without a pipe.** `cmd | tail; echo $?` reports `tail`'s status, not the checker's.

**`git_preflight.sh` exists because `.git/index.lock` blocked commits four times in four days**, once silently for ~24 hours. It asserts you are on the branch you think you are on, and clears a *genuinely* stale lock — empty file, no holder across a sampling window. It never removes a non-empty lock and never removes one while a `git` process is running. Run it before writes; it is cheaper than the day it costs you.

---

## 6 · Fail-closed rows — do not "fix" these by deleting them

The queue distinguishes **empty** from **unknown**, and says so out loud. You will see rows like:

| Row | Means |
|---|---|
| `FREEZE-UNKNOWN` | The freeze-readiness checker is absent or did not run. The freeze chain is **unknown, not clear.** |
| `APPARATUS-UNKNOWN` | No apparatus plan reachable from this ref. This iteration's increments are **unknown, not absent.** |
| `ACTIVE_DESIGN_REF` | The design-line pointer is missing or names a branch that does not exist. **Every release-line row below it is incomplete** until it resolves. |

These are the mechanism working. A missing pointer must fail loudly, never SKIP-OK — that failure mode is what RB-076, RB-106 and RB-125 all were, and it is why the generator is ref-aware.

You will also see a **"Cannot be scoped — reported, not dropped"** tail. `BACKLOG` tickets carry depends-on, AC and GT but **no iteration field exists on any source in this repository.** Rather than silently omit them, the queue names the count it could not scope and why, so the schema gap stays visible until someone closes it. If you want those tickets scheduled, the fix is a schema field, not a bigger queue.

---

## 7 · Not live until — preconditions, named

This document describes the assembled system. The remaining preconditions:

1. ~~PR #255 must merge.~~ ✅ **Merged 2026-09-01.** `iteration_queue.py`, `git_preflight.sh`, `ITERATION.json` and `DEFERRALS.json` are on `main`.
2. **`freeze_readiness_check.py` and the `APPARATUS_PLAN` must be reachable.** Commit `1266bfc` dropped both from #255 to adopt Hamza's branch topology, so they live on his branches. Until they land, **P1 and P2 emit their UNKNOWN rows** — correctly, but the queue is not yet complete.
3. ~~The design-line name must be settled.~~ ✅ **Resolved 2026-09-01.** `design/release-2.1` is canonical — the workflow errors unless `ACTIVE_DESIGN_REF` matches `design/release-<version>`. #247 was re-targeted to it. `r2.1/rb126-deep-cap-doctrine` stays alive only as the head of PR #234 and must not be deleted before that resolves.
4. **Nothing wires `--check` into CI.** No workflow references the generator, so the freshness gate never runs. Advisory first, required once P1 and P2 have real sources.

**Open question for #255 review:** whether `ITERATION_QUEUE` should be committed at all, or generated by CI on each run. It is not committed today. Committed gives you a readable file in the repo and a freshness gate; generated-only removes the staleness class entirely. Hamza's call as dev lead.

---

## 8 · What this replaces

Before this, work was enumerated in four places and prioritized in none — `QUEUED_WORK`, `BACKLOG`, one-off `OBLIGATION_*` files discoverable only if you knew they existed, and `RB-###` rows under Framework 001. The ordering across them existed only in the owner's head, and could therefore only leave it as a chat message.

> **Owner, 2026-08-31:** *"me sending stale IMs via chat is not sustainable."*

That was never a discipline failure. It was the absence of this file.

The rule the apparatus enforces is the product's own doctrine turned on the process that builds it: **OSLO computes leverage and refuses to let anyone hand-rank findings.** A hand-maintained work list goes stale exactly the way an IM does — same failure, new filename.

---

MEASURED-BY: `tools/iteration_queue.py` and `tools/git_preflight.sh` at `apparatus/iteration-1` @ `071fdad`; `20_handoff/ITERATION.json` and `20_handoff/DEFERRALS.json` at the same ref; PR #255 mergebox and commit `1266bfc` read 2026-09-01.
