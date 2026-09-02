# Owner rulings — 2026-09-02 · R2.0 closeout

**Framework 001 stage: Decision.** Ruled by Idris (Founder Console), 2026-09-02, in session.
**Drafted by AI from the owner's stated rulings; AI ratifies nothing.** Land this record with the changes
it authorizes.

---

## ⚠️⚠️ CORRECTED 2026-09-02 BEFORE LANDING — read this first

**This record was first drafted against GitHub state its author could not see** (the drafting sandbox has
no network and no `gh`). Three corrections, all found by reading the open PR list:

1. **The subset is 20 criterion ids across 17 rows, not 18** — per **#277, approved**. *18 is the
   CLASSIFIED count.* Three rows carry two ids each (GT-61·GT-93, GT-106·GT-110, GT-01·GT-02).
   ⇒ **pass 8 · fail 6 · untested 4 · UNCLASSIFIED 2.**
2. **"The remaining 113" was derived against 18.** #277 marks it for re-derivation against 20 and
   deliberately refuses to substitute a number: *"inventing the total would be the same failure in a new
   place."* **R2.0-2 below is therefore scoped to a set whose size is not yet established** — the split
   across iterations 2 and 3 stands as a shape; **the count does not.**
3. **Three of the seven obligations duplicated open PRs** — **#275** (N-5) and **#276** (N-7 *and* N-8, in
   one file). Those three are withdrawn; **#275 and #276 are the rows of record.**

⇒ **Landing set: the rulings record, `OBLIGATION_n4`, `OBLIGATION_gt107`, and the owner's two existing
untracked obligations. Five paths, not eight.**
★ **The cause, recorded because it is the session's own lesson:** the local corpus was read as a proxy for
the state of the work, which lives partly on GitHub. **One `gh pr list` before drafting would have
prevented six of seven duplicates.**

## R2.0-1 — Every open subset criterion gets a durable object

**RULED: all seven missing obligations are created.** *(Amended above: three are withdrawn as duplicates
of #275 and #276.)*

The production-gating subset holds **20 criterion ids across 17 rows** — **8 pass · 6 fail · 4 untested ·
2 unclassified**. Only four obligation files existed, all covering the B-series, so the iteration queue
derived **four** P0 rows against **twelve** criteria that are not passing.

```
MEASURED-BY: ls 20_handoff/OBLIGATION_*.md            → 4 files (B0, b1, b2, b3)
             cross-referenced against R2.0_PRODUCTION_ACCEPTANCE_CRITERIA.md §4b
```

**CONTROL:** the same listing resolves the four B-series obligations, so the absence of the other seven is
a real gap and not a listing error.

Created: **N-1** (B5) · **N-4** (R8) · **N-5** (build identity) · **N-7** (R1·R5) · **N-8** (R6·R7) ·
**GT-106·GT-110** (server-side entitlement) · **GT-107** (inferred root outcome caps Grounding).

⚠️ **Each is drafted with `Fix: TO BE ASSIGNED`.** The queue derives an owner from the row; an unassigned
row is visible but not actionable, so assignment is the next act.
⚠️ **Each records its invariants as NOT YET DETERMINED where no GT twin covers the criterion** (N-1, N-4,
N-5, N-7). **Escalated, not guessed** — the B-series precedent.

## R2.0-2 — The 113 deferred criteria are split across iterations 2 and 3

**RULED: split. Iteration 2 (2026-09-11 → 09-25) and iteration 3 (2026-09-25 → 10-09), sequenced.**

⚠️ **First ruled as "all 113 to iteration 2", then corrected in session** when §4a.3 was put back to the
owner: *"The 61 untwinned invariants (`GT-58…GT-118`) cannot land in one iteration. Each iteration names
which move to TWIN."* Naming all 113 to one iteration would have satisfied §4b's letter while creating
exactly what §4a.2 warns against — *"a criteria set that cannot be executed within one iteration is not a
gate; it is a backlog, and it will be skipped under cadence pressure."* **The corrected ruling satisfies
both sections.**

**Proposed split — owner to confirm the contents, the shape is ruled:**

| iteration | contents | basis |
|---|---|---|
| **2** · Sep 11–25 | the twin-gate `--self-test` and the **53** active-twin RED-proofs (R2.0-4 ①②), plus the ~**52** non-twin deferred criteria — Deep Pass timings, upload formats, collaboration surfaces, export, accessibility, withdraw append-vs-erase | two capacity pools: engineering for the RED-proofs, audit for the executable checks |
| **3** · Sep 25–Oct 9 | the **61** untwinned invariants `GT-58…GT-118`, authored as twins in named tranches | §4a.3: each iteration names which move to TWIN |

⚠️ **Neither iteration's capacity has been measured.** The one datapoint is §5: *"~25 of 131 criteria
exercised, by hand, in a day, by an auditor who chose them."* That makes ~52 executable checks roughly two
auditor-days — plausible — and says **nothing** about the 53 RED-proofs, which are engineering work in a
different pool. **State this as a plan, not a forecast.**
⚠️ **The split is only real if the iteration-3 tranches are named at the Sep 11 boundary**, not left to be
decided when iteration 3 begins. An unnamed tranche inside a named iteration is the same PENDING-SUBJECT
defect one level down.

## R2.0-3 — GT-39…GT-50 are out of scope for R2.0, and named

**RULED: the twelve `pending()` engine invariants are OUT OF SCOPE for R2.0, named for a later iteration.**

This clears them from PENDING-SUBJECT under §4.3 — *no criterion is in PENDING-SUBJECT without an owner
ruling accepting it as out of scope for this release.* **That ruling is now given.**

★ Supported by §3a.2's measurement: **the engine is built and the twins are real; the register's
`pending()` claim is stale.** So this is a scheduling call, not a risk acceptance.
⚠️ **The stale `pending()` claim in the register is not corrected by this ruling** and remains owed — a
register that misdescribes its own state will re-raise this question at the next freeze.
⚠️ **"A later iteration" must be a NAMED iteration**, or this ruling recreates the PENDING-SUBJECT problem
it just resolved. Naming is owed alongside R2.0-2's confirmation.

## R2.0-4 — The twin harness proves itself before the 53 are backfilled

**RULED: add `--self-test` to the twin gate first, then RED-prove the 53 active twins in named tranches.**

§4.1 requires every TWIN criterion to be RED-proved. §3b measured that **there is no evidence any of the
53 active twins is** — and that the gate running them **carries no `--self-test` while twelve governance
checkers do.**

⇒ **The harness that cannot demonstrate it would catch a broken twin is fixed before effort is spent
inside it.** A backfill validated by a harness of unknown soundness would have to be redone.

**Order:** ① `--self-test` on the twin gate, RED-proved in both directions · ② the 53 in named tranches,
each tranche RED-proved · ③ the 61 untwinned (`GT-58…GT-118`) per R2.0-2.

⚠️ **This is the largest single gap between the current build and a defensible production claim.** It does
not block the four execution-only criteria (GT-106·GT-110, GT-107, N-5) and should run in parallel with
them, not ahead of them.

**RULED: it does NOT gate the R2.1 freeze.** R2.1's freeze is governed by F002 §9.3's five items; R2.0's
twin coverage is a different subject on a different line. Kept separate deliberately, in both directions:
so the backfill does not silently become a freeze blocker, **and so it is not skipped to protect a freeze
date.**
⚠️ **This does not make R2.0 claimable.** §4.1 still requires every TWIN criterion to be RED-proved for a
production pass — the freeze and the production claim are different gates, and only the freeze is
unblocked by this ruling.

## R2.0-5 — Assignment and execution order

**RULED — assignment, split by kind:**

| lane | obligations | fix | accepts |
|---|---|---|---|
| product / engine defects | **N-1 · N-4 · N-7 · N-8** | **TaimoorSohail1** | idris-manley |
| checks & infrastructure | **N-5 · GT-106·GT-110 · GT-107** | **HamzaSohailCodes** | idris-manley |

Rationale: N-1/N-4/N-7/N-8 share the codebase B0–B3 are already being fixed in; N-5 and the two unrun
checks are execution and CI work. ⚠️ **Taimoor now carries eight P0 rows** (B0, b1, b2, b3 + four) during
an iteration that also has to carry the R2.1 freeze — **the T1/T2 contention is now measured, not
suspected.**
⚠️ **N-5 must be coordinated with the owner**, who is already working on `obligation/n5-build-identity`.

**RULED — execution order for the four criteria that need no fix at all:**

1. ★ **N-5 build identity FIRST.** Every other DONE CONDITION reads *"on the deployed build"* and **none of
   them can currently name which build that was.** It is not the largest defect; it is the one that makes
   every other result checkable. Closing B0–B3 without it reproduces the exact ambiguity that has left the
   identity fix stuck at *"verified locally only, by their own report."*
2. **GT-106 · GT-110** — server-side entitlement, the highest-value unrun check.
3. **GT-107** — the only unmeasured Tier 1 criterion. ⚠️ **If it fails, same-day escalation.**

These run **ahead of and independently of** the B-series deployment. ⚠️ Their results carry a build
identity only after item 1 lands — so if 2 or 3 are run first out of impatience, they will have to be
re-run.

## R2.0-6 — Four GT ids minted now; oracles authored with the fixes

**RULED: mint GT-119…GT-122 in this session so every subset criterion cites a real invariant. The oracles
are authored as part of each fix, not as separate work.**

| id | criterion | invariant |
|---|---|---|
| **GT-119** | N-1 | a completed analysis reaches the user |
| **GT-120** | N-4 | no governed act surfaces a raw exception; every act path states whether the record changed |
| **GT-121** | N-5 | a running build names the commit it was built from |
| **GT-122** | N-7 | every surface rendering the judgment names the same band word and the same limiting pillar, enumerated from one registry |

**Basis:** §4a.1 — *TWIN is the default; WALK is not a parking space for work nobody has automated.* All
four were WALK-by-default because no id existed, which is the parking space that section names.

```
MEASURED-BY: git grep -ohE 'GT-[0-9]{1,3}' refresh/r21-from-main | sed 's/GT-//' | sort -n | uniq
             → GT-01 … GT-118, contiguous, ZERO holes  (+ GT-A1…A3)
```

⚠️⚠️ **COLLISION RESOLVED, recorded so it is not re-created.** `PROPOSAL_2026-09-02_coaching-fade-guard-cannot-fail.md`
had already proposed **GT-119** for `coachingFadesWhenEngaged`. **That proposal is unruled; these four are
ruled.** Ruled work takes the earlier ids, and the coaching guard is **re-assigned to GT-123** — because
reserving an id for a guard that may never be adopted would leave a hole in a register whose contiguity is
measured and load-bearing. The proposal carries the re-assignment.

⚠️ **Minting an id is not authoring a guard.** Each of the four still owes a `_S10` oracle, a register
entry, a tier, and a RED-proof in both directions per `guard-add`. **An id with no oracle is a citation
with nothing behind it — the exact defect the citation gate exists to catch.**
⚠️ **The register's stated RANGE must be bumped when these land, and which sentence is the range of record
is still RB-109's open question** (`acceptance/README.md` states three different ranges). **Do not silently
pick one.**

## R2.0-7 — GT-39…GT-50 land in iteration 3

**RULED: iteration 3 (2026-09-25 → 2026-10-09).**

Completes R2.0-3, which ruled them out of scope but left *"a later iteration"* unnamed — recreating
PENDING-SUBJECT by a different route. They land with the 61 untwinned invariants: **same kind of work, same
pool, one tranche-naming exercise instead of two.**

## R2.0-8 — The register's stale `pending()` claim is corrected as engineering realization

**RULED: ordinary PR with the dev lead as reviewer. No Framework 001 proposal.**

The measurement is already done and ratified in §3a.2 — *the engine is built and the twins are real; the
register's `pending()` claim is stale.* **Correcting a register to match a ratified measurement is
realization, not a policy change** — the same boundary already recorded for workflow bug fixes.
⚠️ **The correction must cite §3a.2 as its basis in the PR body**, or the next reader cannot tell a
realization from an unratified edit to governed content.

## R2.0-9 — GT-35 is UNTESTED

**RULED: GT-35 (*only verify moves Grounding*) is classified untested, not carried by B3.**

#277 records the question as *"does B3's failure carry GT-35 with it, or is GT-35 separately satisfied?"*
**Neither reading is earned:**

- *B3 carries it* infers a violation from an adjacent defect. **B3 is that the COUNT is unstable; GT-35 is
  about what MOVES it.** A wrong number does not demonstrate a wrong mover.
- *Separately satisfied* is a pass with no evidence behind it, on a **Tier 1** honesty criterion.

⇒ Untested is the only classification anyone has earned. **It joins GT-107, GT-106·GT-110 and N-5 in the
execution-only set** and needs its own measurement.
★ **This may be cheap:** GT-35 sits in **GT-34…GT-44, the DL-209 twins**, and §3a.2 measured that engine's
twins as **real** — so a server twin may already exist and the work may be a run rather than a build.
**Check for the twin before commissioning one.**

## R2.0-10 — N-4 is a FAIL for gating

**RULED: a partial failure path is a fail.**

#277 records the question as *"is a partial failure path a fail for gating, or a pass with a recorded
defect?"*

**GT-A1 and N-4 measure different things, and that is what settles it.** GT-A1 asks whether the **record**
survived — it did: the act did not report success, settled held at *2 of 29*, the open count held at 27.
**N-4 asks whether the round-trip HAS a failure path**, and on the governed act path it does not: a raw
`Failed to fetch`, no explanation, no retry, and none of the reassurance the chat surface already gives.

⇒ A user who cannot distinguish a failed act from a recorded one will **re-attest, and re-attestation on an
append-only record is not free.** The substance passing is what makes this narrow, not what makes it
acceptable.
⚠️ **Provenance note:** the AI's drafted obligation already classified this as blocking — i.e. it
pre-empted a question #277 had escalated to the owner. **The ruling is the owner's; the draft was
premature and is recorded as such.**

## R2.0-11 — `ITERATION_QUEUE.md` is committed, with `--check` wired in the same change

**RULED: commit it AND wire `--check` in one change.**

#277's adjacent finding is the argument made concrete: the untracked generated file survived a branch
switch, went stale, and failed doc-integrity on a **clean** branch with
`[broken-link] → OBLIGATION_n7-n8-…md`. **A contributor reads that as their own change breaking the gate.**

The generator already documents the mechanism in the file's own header. ⚠️ **Committing it without wiring
`--check` creates exactly the stale artifact this ruling exists to prevent.**
⚠️ **Do NOT fold this into #271.** That PR ignores litter permanently; this keeps derived state current.
**Opposite mechanisms, same symptom.**

## R2.0-12 — N-5 is production-blocking, and the inclusion test never governed it

**RULED: production-blocking.** This closes the classification #275 escalated and unblocks that PR.

```
MEASURED-BY: git show origin/main:20_handoff/R2.0_PRODUCTION_ACCEPTANCE_CRITERIA.md | sed -n '251,263p'
  ## 4 · WHAT A PASS REQUIRES
  4. The build carries a **resolvable identity** (N-5, DL-243 §6e).
```

⚠️ **The decisive basis is §4.4, not §4b's inclusion test.** A resolvable build identity is already a
**condition of a pass**, independently of the subset. So N-5 never had to satisfy *"if this fails, is a
user actively misled or blocked?"* in order to gate — **§4 gates it directly.** That test triages
*product* defects; N-5 is a property of the *gate*. Applying a product-defect test to a measurement
precondition is a category error, and reading it literally is what made the classification look open.

★ **The code-owner review was right about the defect and right to block on it.** #275's `Class:` field
made the queue derive N-5 as P0 while the row's own §3 said the classification was *pending* — a row
operationalizing a recommendation before the decision existed. **The fix is the ruling, not a softer
`Class:` value.** §3 now records the decision; the `Class:` field is unchanged because it was, in the
event, correct.
⚠️ **This is the same defect the AI committed the same day** with N-4 — a drafted obligation answering a
question #277 had escalated to the owner. Caught in one document by the reviewer, in the other after the
fact. **A row may not classify what its own text says is unruled.**

⇒ **Consequence: N-5 is first in the execution order (R2.0-5), and every other row's DONE CONDITION —
each reading "on the deployed build" — becomes attributable only after it closes.**

---

## What these rulings do NOT do

- They do not close any criterion. **Ten subset criteria remain open: six failing, four untested.**
- They do not change the permitted claim. **R2.0 may only be described as "validated against the
  production-gating subset" — 18 of 131 criteria — never as "validated."**
- They do not name **iteration 3's tranches** (R2.0-2), owed at the Sep 11 boundary.
- They do not **author** the four minted oracles (R2.0-6). An id is not a guard.
- They do not settle **RB-109's range of record**, which the four new ids will force.
- They do not close any criterion, and they do not change the permitted claim.

## Landing

```
git checkout -b canon/r2.0-closeout-rulings origin/main
cp ~/Documents/Claude/Projects/'OSLO Knowledge Base'/OWNER_RULINGS_2026-09-02_r2.0-closeout.md 00_owner/decisions/
cp ~/Documents/Claude/Projects/'OSLO Knowledge Base'/obligations/OBLIGATION_*.md 20_handoff/
git add 00_owner/decisions/OWNER_RULINGS_2026-09-02_r2.0-closeout.md 20_handoff/OBLIGATION_*.md
git status --short
```

Must show exactly **8** added paths — one rulings record and seven obligations. Any other number means a
file was missed or something else was staged; name the paths rather than committing the sweep.

Then regenerate the queue and confirm the rows appear:

```
python3 tools/iteration_queue.py && grep -c '^| `' 20_handoff/ITERATION_QUEUE.md
```

**P0 should rise from 4 rows to 11.** If it does not, the obligations are present but not derivable — the
row format, not the filing, is wrong.
