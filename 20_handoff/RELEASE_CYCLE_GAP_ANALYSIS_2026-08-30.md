# Release cycle — gap analysis · 2026-08-30

**Purpose.** Establish a durable owner↔engineering release cycle. This document does **step one
only**: what the process is today, where it breaks, what each gap costs, and who owns the correction.
**It proposes no process.** Design follows once the owner has ruled on the gaps — designing against
unagreed gaps is how the last three months of correctives happened.

**Audience.** Joint — owner and engineering, as a shared working agreement. It is deliberately
neutral about fault and specific about ownership.

**Status.** Analysis. Authored by AI under Framework 001. **Not ratified. Not a decision record.**
Routing: this should become a Backlog entry → Proposal → Review → Decision, not a direct edit.

MEASURED-BY: read-only `git --git-dir` plumbing against `origin/codex/r2-uat-remediation` and the
working tree on `refresh/r21-from-main`; GitHub PR/checks/branch pages; the live staging app. Every
count below names its command inline. 2026-08-30.

---

## 0a · THE CADENCE CONSTRAINT — stated by the owner 2026-08-31

**Releases run on a fixed two-week iteration, and a freeze must occur inside each one.**

**Iteration 1: `2026-08-31` → `2026-09-11`.** Boundaries: **Sep 11 · Sep 25 · Oct 9**.

### ▶ SPRINT 1 SCOPE AND PRIORITY — owner, 2026-08-31

**Three tracks:** complete R2.0 validation and defect fixing · freeze R2.1 and begin build ·
owner begins R2.2 design.

⚠️ **Tracks 1 and 2 compete for the same two people.** Track 3 is the owner's and is genuinely
parallel.

**RULED — when they collide, R2.0 defects take priority and the freeze slips if needed.** The
deployed product's honesty guarantees outrank cadence. ⚠️ **Consequence accepted: the first freeze
under the new cadence may be missed, in the first iteration.** Stated so a slip is a known cost, not
a surprise.

**RULED — "complete R2.0 validation" means a NAMED production-gating subset** (18 criteria, listed at
`R2.0_PRODUCTION_ACCEPTANCE_CRITERIA.md` §4b), with the remaining 113 deferred to a named iteration.
⚠️ **R2.0 may then be described as "validated against the production-gating subset", never as
"validated".**

⚠️⚠️ **THE FIRST FREEZE UNDER THIS CADENCE IS DUE 2026-09-11 — nine working days — AND R2.1'S TWO
BLOCKERS ARE NOT CLOSE.** B2 needs the refresh via #247, which needs RB-076, which needs
`design/release-2.1` to exist — a branch not yet created. B3 needs the finding-ordering decision and R7 dispatched, which
only became possible when #237 merged today. **Neither chain has started.** Recorded so the first
iteration is not declared met by default.

⚠️ **This reframes several gaps below from "should fix" to "blocks the cadence", and it was not a
constraint the rest of this document was written against.**

F002 §9.3 requires, at **every** freeze: the precondition register at **N-of-N** · a
**build-readiness audit with zero unresolved escalations** · the state matrix **green at the frozen
md5** · the acceptance register **synchronized** · an **owner freeze declaration**. On a two-week
cadence that entire set must be satisfiable in **ten working days, repeatedly**.

Measured against that, today:

| requirement | state | consequence for the cadence |
|---|---|---|
| Build-readiness audit at freeze | The 2026-08-29/31 audit took **a day**, found **4 blocking**, and the auditor **chose what to test** | ~1 day in 10 spent auditing by hand, with self-selected coverage. **Not sustainable; must be mostly automated.** |
| App CI completes | **Cancelled after 75m** (§G3) | A short cycle needs fast trustworthy signal more than a thorough one that never finishes. **Ruling 3's tiering moves from good idea to precondition.** |
| Acceptance register synchronized | **61 of 121 invariants have no twin**; 53 more are unproved | **Cannot be backfilled in one iteration.** Needs sequencing across several, with a rule for what is required *now* versus later — which the criteria do not yet carry. |
| Freeze actually occurs | **R2.1's freeze is blocked** on B2 and B3 | If a freeze is routine every two weeks, the current state is **a cadence failure, not a delay**. |

**The honest read: the cadence is achievable, but not with the apparatus as it stands.** It depends
on the twin backfill and the CI split landing first — which is the work rulings 3 and 4 already task.
⚠️ **Stated here so the cadence is not quietly treated as met.**

---

## 0 · Read this before the gaps

**Two findings frame everything else, and the first one corrects an assumption I held for most of
this investigation.**

**The engineering team has real quality infrastructure.** The deployed monorepo carries **130 test
files** and the CI pipeline stands up a real database and drives a browser:

MEASURED-BY: `git ls-tree -r --name-only origin/codex/r2-uat-remediation -- code/…` filtered by
extension → `services/api/tests` **60** `.py` · `apps/web` **43** `.test/.spec.ts(x)` · e2e specs
**27**. `.github/workflows/app-ci.yml` on that ref: Gate 1 install · Gate 2 approved-contract
traceability · Gate 2b R2 doctrine-guardrails · Gate 3 `lint:api lint:web test:api test:web
build:web` · Gate 4 `test:e2e` against a started app with `supabase start` + `seed:local`.

This is not a team that does not test. **Every gap below is structural — about what is required,
what is proved, and what is carried between us. None is about effort or care.**

**The governance side is held to a standard the application side is not.** Every governance checker
carries a `--self-test` that proves it fails when it should; `no_hardcoded_release_line.py` exists
because one rule broke three times; `report_measurement_check.py` exists because four counts were
measured by proxy. That discipline — *a check that cannot fail is not a check* — is enforced in
`tools/` and **is nowhere in the application test suite.** Gap G5 is the sharpest instance, and it is
the one I would fix first.

---

## 1 · Canon → build handoff

### G1 · The handoff seam is R1-shaped; R2 has no interface contract
**Owner: joint.**

MEASURED-BY: `find 20_handoff -type f | wc -l` → **34**;
`grep -rl -E 'R2|release-2|Release 2' 20_handoff/ | wc -l` → **5**;
`grep -rn -icE 'viability|grounding|adaptability' 20_handoff/` → **1 file, 1 hit**.

`20_handoff/` is genuinely populated — a 372-line API contract spec, endpoint catalog, state and
event models, traceability matrices. **All of it describes Release 1.** The R2 concepts the product
now runs on — the three pillars, the band ramp, finding lifecycle, the Grounding counter — appear
once, in one crosswalk.

**What it costs.** The 2026-08-29 staging audit had to argue every finding from doctrine, because
there was no contract to cite. A defect and a design decision become indistinguishable: when the
Grounding denominator moved, nothing said whether that was wrong. **Engineering cannot be held to a
contract that does not exist, and the owner cannot accept a build against one either.**

### G2 · No framework governs the application at all
**Owner: owner.**

`framework_002.md:5-6` — *"Governs: how a change to a release line is classified, captured, gated
and delivered, and the branch topology those rules run on."* §9.5: *"Realization is engineering's —
rulesets, CODEOWNERS, CI, environments, migration."* Framework 001's objects are Frameworks,
Proposals, Decisions, Backlog and Changelog entries. **Neither says anything about building, testing,
deploying or accepting software.**

This is not a defect in F002 — it is a deliberate boundary. But it means **the release cycle being
asked for has no framework to live in**, which is why it keeps being improvised per release.

**Shape of the correction (not a proposal):** the gap is framework-sized. Whether it becomes
Framework 003, an F002 section, or a co-governed handoff contract is an owner ruling.

---

## 2 · Build → validation → QA

### G3 · The most thorough gate exceeds its own time budget
**Owner: engineering.**

MEASURED-BY: checks panel on PR #248, 2026-08-30; `app-ci.yml:23` `timeout-minutes: 75`.

| check on #248 | result |
|---|---|
| `doc-integrity` — **Required** | ✅ 13s |
| `queued-work` | ✅ 15s |
| `altering-base` | ✅ 3s |
| **`OSLO application quality gates / verify`** | ⚠️ **Cancelled after 75m** |

The pipeline is comprehensive enough to exceed its own ceiling. Everything runs in one sequential
job — install, Supabase start, seed, lint, unit, build, app start, Playwright — so any slow step
starves the rest and the whole thing dies at the wall.

**What it costs.** On the largest application PR in the repo's history — **990 files,
+186,990/−495** — the only gate that tests software did not finish, while three document gates
passed in under fifteen seconds each.

### G4 · The application gate is advisory; only document gates are required
**Owner: owner rules the ruleset; engineering already did its half.**

RB-056 (`origin/refresh/r21-from-main:release-2.1/QUEUED_WORK.md:74-88`) records this precisely: *"`verify` is not in protect-main's
required checks, so a red quality gate does not block main."* Owner ruled 2026-08-16: **always-runs
job**. Engineering completed that half — `app-ci.yml` now decides applicability inside the job. **The
ruleset half — marking it required — was never done.**

**What it costs.** Today a red or unfinished application gate blocks nothing. Combined with G3, the
software gate on #248 both failed to finish *and* could not have stopped anything if it had failed.

⚠️ **NOT-MEASURABLE from any file:** actual GitHub branch-protection state lives in repository
settings, in no ref. `CODEOWNERS:70-92` says so itself: *"THIS IS A DECLARED PROXY… nothing here can
observe it."* Someone must read the settings page and report what is actually required.

### G5 · The application suite proves the happy path and never RED-proves the failure
**Owner: engineering, on an owner ruling that the rule applies to `code/`.**

This is the gap I would fix first, because the 2026-08-29 audit's three blocking defects all trace to
one function — and **that function has a test.**

MEASURED-BY: `git show origin/codex/r2-uat-remediation:code/services/api/tests/analysis/test_issue_identity.py`
→ 297 lines, **11 tests** (`grep -n "^def test"`).

Of the 11, **nine test `deduplicate_issues`** (within-run merging) — and those are well done, with
genuine negative cases (`…_are_not_merged`, `…_does_not_replace_…`). **Only one test covers
`stabilize_issue_ids`**, the across-run identity function whose failure produced B1, B2 and B3:
`test_semantically_equivalent_issue_keeps_previous_stable_id`.

That test is constructed to pass. Both issues share the helper's default
`evidence_refs=("document:plan:page:2:fragment:4",)`, which awards the **+0.15 evidence bonus
automatically**, on top of heavy token overlap (*migration · threshold · patient · match ·
production*). **No test asserts what happens when a rewording falls below the `0.38` threshold. No
test varies `evidence_refs`. No test covers the `artifact_type` mismatch path**, where identity is
lost unconditionally.

**What it costs.** The suite is green, the defect shipped, and it reached a user-visible honesty
violation: attested work returning as the user's top priority. **The team already writes negative
tests — nine of them, in the same file, for the neighbouring function.** The discipline exists; it
was not applied to the function that carries the doctrine.

### G6 · Validation evidence is narrative, not gate output
**Owner: joint.**

PR #248's body reports *"live staging review: 8 sections passed, 2 partial, 0 failed"*, citing the
R2 live-staging validation report dated 2026-08-28 (in `code/docs/` **on
`codex/r2-uat-remediation`** — it does not exist on this line, which is why it is named here rather
than linked). The staging audit on **2026-08-29** — same app, next day — found **3 blocking**
defects.

Both cannot be right. Either the validation does not test finding-identity stability across
re-analyses, or something regressed in a day. **Either answer indicts the evidence, not the person:**
a hand-written pass/fail narrative cannot be re-run, cannot be diffed, and names no command.

**What it costs.** This is the exact failure the owner already mechanized against on the governance
side — `report_measurement_check.py` exists because counts were asserted rather than measured.
**Application validation is currently where governance reporting was before that rule.**

---

## 3 · Release → staging → production

### G7 · No build identity anywhere
**Owner: engineering.**

No `/version` endpoint, no build stamp, no commit marker; `GET /api/workspace` carries no version
field. MEASURED-BY: live payload inspection, 2026-08-29 — top-level keys are plan/limits/projects/
notifications only.

**What it costs.** The staging audit could describe behaviour but could not pin one finding to a
commit. There is no rollback target, no way to reproduce a result against the same artifact, and no
way to tell whether the build Taimoor validated on 08-28 is the build audited on 08-29. **This is the
cheapest fix in this document and it unblocks the most.**

### G8 · Environment ownership is split and undocumented
**Owner: owner.**

MEASURED-BY: `dashboard.heroku.com/apps` while signed in as the owner → 4 apps:
`dev-intralign-agent` · `dev-intralign-api` · `prod-intralign-agent` · `prod-intralign-api`.
`dashboard.heroku.com/apps/intralign-oslo-web-staging` → **"Access denied. This Heroku account does
not have the required permissions."**

A dev/prod split exists and the owner owns it. **The deployed OSLO web app is not in it, and the
owner cannot reach it.** No document defines which environments exist, what each is for, who
administers them, or what promotion between them requires.

**What it costs.** F002 §9.3 makes an owner freeze declaration and a build-readiness audit part of
promotion evidence. Against infrastructure the owner cannot read, neither can be produced.

### G9 · Promotion evidence is defined but not enforced anywhere
**Owner: joint.**

F002 §9.3 names the evidence a promotion requires — precondition register N-of-N, build-readiness
audit, state matrix green at the frozen md5, acceptance register synchronized, owner freeze
declaration. **None of it is checked at merge, and none of it is checked at deploy.** No document in
the repository names a required-check list.

---

## 4 · Defect intake back into canon

### G10 · The cycle has no lane for product defects
**Owner: joint.**

The dev lead's pending list of 2026-08-30 carries six items: merge #245 · dispatch the finding-ordering decision and R7 ·
name the R2.1 ref · RB-076's CI fix · #247 approval · #227 decisions. **Not one concerns the
product** — on a day when a staging audit found three blocking defects in what users are running.

This is not a criticism of anyone; it is what the queue is shaped to hold. Backlog rows, ledgers and
registers all describe canon and apparatus. **A product defect has no row type**, so it does not
appear, so it is not scheduled.

**What it costs.** Governance work is fully visible and correctly prioritized. Product defects
survive only in audit documents, and audits accumulate.

MEASURED-BY: `ls release-2/BUILD_READINESS_AUDIT_*.md release-2.1/BUILD_READINESS_AUDIT_*.md | wc -l`
→ **10** in the working tree, one of which — the **2026-08-24 R2.1 audit** — is **untracked**: a
governed audit on disk that the repository has no record of, while the measurement checker counts it
among its grandfathered reports.

⚠️ **That filename is deliberately not written as a path here.** Written as one, it is a broken link
on every ref, because the file it names is not in any of them — **which the pre-push gate proved by
blocking this document on 2026-08-31.** The finding is real and the citation must not resolve;
naming it without a path is the honest form. ⚠️ **And the same run exposed a flaw in how these
documents were being validated: `doc_integrity_check` run locally sees the WORKING TREE (1130 docs,
green), while the hook archives the REF and sees 1110 — untracked files make a local green
meaningless. Validate the ref, never the tree.**

### G11 · Scheduled governance checks evaluate nothing
**Owner: engineering, on an owner designation. In progress.**

RB-076's daily escalation runs from `main`, and `main` carries no `CURRENT_RELEASE`,
`DELIVERY_RELEASE`, `release-*` directory or
`origin/refresh/r21-from-main:RELEASE_LINE_CONVENTION.md` (all 404 on `main`,
verified 2026-08-30), so the resolver returns SKIP-OK and the check passes without measuring.

⚠️ **The failure mode is skip-as-pass**, which is the same shape as G5 and G6. The agreed
`ACTIVE_DESIGN_REF` fix must make an absent or dangling pointer **fail loudly**, or it rebuilds the
defect with an extra file.

### G12 · One approver is the throughput ceiling
**Owner: owner.**

27 open PRs; `dl-land` permits one canon PR in flight, so #245 gates the finding-ordering decision and R7 dispatches.
Four PRs currently sit approved and awaiting owner merge. **#227's "second canon approver" decision —
the structural remedy — is itself waiting in the queue it would relieve.**

---

## What this document does NOT claim

- It does not propose a process. That is step two.
- It does not measure GitHub branch-protection state (G4) — unreadable from any ref.
- It does not assess the app CI's *content*, only whether it completes and whether it is required.
- It does not evaluate `apps/web` or `services/api` beyond `issue_identity.py` and its test.
- **The G5 reading is from source, not execution.** Engineering should confirm before it is ratified.

## ▶ OWNER RULINGS CAPTURED 2026-08-30 — not yet ratified

⚠️ **These are the owner's rulings on the seven questions below, recorded as captured intent. They
are NOT ratified.** Each must route Backlog → Proposal → Review → Decision under Framework 001 before
it is canon. Recorded by AI; **AI ratifies nothing.**

| # | gap | ruling |
|---|---|---|
| 1 | **G2** | **Extend Framework 002** into a vacant section (§1/§2/§4/§6 — never renumber) with owner-level **build acceptance obligations**: what a build must prove to be promotable. Do **not** mint Framework 003. Realization stays engineering's per DL-235. ⚠️ Requires amending F002's scope statement. |
| 2 | **G12** | **Second approver, split by F002 class.** Dev lead may satisfy code-owner **review** on canon PRs and may **merge Neutral-class** changes on green gates. **Additive and Altering merges stay with the owner. Ratification is not delegated at all.** ⚠️ Interacts with `CODEOWNERS:12-14` required-approvals=0 — verify the live ruleset before relying on it. |
| 3 | **G4** | **Tiered requirement.** Owner obligation: unproven software may not reach `main`. Engineering splits the gate; the **fast tier becomes a required check immediately**, the **full tier becomes required once it completes inside budget** (G3). ⚠️ Do **not** require the current 75-minute monolith — it would block every open PR. |
| 4 | **G5** | **RED-proof extends to doctrine-realizing code, routed through the GT register.** Every GT invariant gains a **server-side test that must fail when the invariant is violated**. Closes **RB-123**. Not a blanket rule across `code/`. |
| 5 | **G6** | **Extend `report_measurement_check.py` to release validation reports.** Every pass/fail claim carries `MEASURED-BY:` (command or CI run) or `NOT-MEASURABLE:` (why). Human walkthroughs stay legitimate via the latter. |
| 6 | **G10** | **Two tiers, divided at the GT register.** Ordinary defects → engineering tracker. A defect violating a GT/doctrine invariant → **governed row + the failing server-side test from ruling 4**. ⚠️ Watch for under-calling: an empty governed-defect lane beside a busy tracker is the tell. |
| 7 | **G8** | **Owner holds admin on production and at minimum read on every environment serving users.** Environments enumerated in the handoff contract. Promotion stays gated on the F002 §9.3 evidence set. |

### ▶ RULING 11 — captured 2026-08-31 · #227's remaining decision

**The owner's bypass of branch protection is removed**, sequenced behind engineering rescoping the
rule. Two things were tangled and only one was the owner's: whether the rule should cover a PR's own
*source branch* is configuration (it currently does, which blocks normal PR work); whether the owner
may **override protection silently** is intent, and the answer is no.

MEASURED-BY: the push to `canon/dl-land-sentinel-fix` on 2026-08-31 printed
`Bypassed rule violations … Changes must be made through a pull request` — no confirmation, no
`--force`, a line in the output easily scrolled past. Precedent: a `git merge --ff-only` previously
put **235 files** on `main` past both the PR rule and `doc-integrity`.

⚠️ **Sequence matters: rescope first, then remove the bypass.** Removing it while the rule still
covers PR source branches would block ordinary work.

⚠️ **#227's other decision — the second canon approver — was already ruled** (ruling 2 above:
review on canon PRs + merge on Neutral class only). **#227 now has no open owner decisions.**

**Note the shape.** Rulings 4 and 6 are **one mechanism, not two** — the GT server twin is
simultaneously the invariant's test, the defect's governed row, and the proof of its fix. Ruling 1
gives that mechanism a home. **G3, G7, G9 and G11 remain engineering-side and are unaffected by these
rulings.**

---

## ▶ ROUTING — what needs canon, what just needs doing · 2026-08-30

**Result: exactly one of the seven rulings needs a decision record.** DL-243 (F002 §6) carries the
principle for four of the others; the rest are realization, configuration or documents, which §9.5
places with engineering via the `20_handoff/` seam. **Nothing below except ruling 1 waits on
ratification** — though work citing §6 should not land before §6 does.

MEASURED-BY: `sed -n '122,192p' 00_owner/frameworks/framework_002.md` (§8, §9) and
`sed -n '208,232p'` (§11), 2026-08-30.

| ruling | needs canon? | route | cites | closes |
|---|---|---|---|---|
| **1 · G2** F002 §6 | ✅ **YES — the only one** | `PROPOSAL_F002_S6_…_DL243_DRAFT.md` → F001 Backlog→Proposal→Review→Decision. ⚠️ blocked by `dl-land` while **#245** is open | — | G2 |
| **2 · G12** merge delegation | ❌ **No** | `20_handoff/` proposal → CODEOWNERS + ruleset change | §8c, §9.5 | G12 |
| **3 · G4** tiered gate | ❌ No | engineering splits the job; owner-approved ruleset marks the fast tier required | **§6a** | G4, G3 |
| **4 · G5** GT server twins | ❌ No | acceptance register gains server-side twins; engineering builds them | **§6c** | G5, **RB-123** |
| **5 · G6** validation evidence | ❌ No | one tooling change — widen `report_measurement_check.py`'s file scope | **§6d** | G6 |
| **6 · G10** defect tiers | ❌ No | operational definition of the governed-defect row + triage rule | **§6f** | G10 |
| **7 · G8** environments | ❌ No | Heroku access action + environment enumeration in the handoff contract | **§6e/§6g**, §9.3 | G8, and G1 alongside |

### ⚠️ Two questions that must be answered before realization, and are cheap to answer now

**Q1 — does the Neutral · Additive · Altering taxonomy apply to CANON-document PRs?** F002 §3
classifies **changes to a release line**. Ruling 2 delegates merge of **Neutral** changes — but the
PRs actually queueing on the owner are canon-document PRs (DL records, framework edits), and it is
**not established that the taxonomy classifies them at all**. If it does not, *"dev lead merges
Neutral"* is undefined for exactly the PRs it was meant to unblock, and ruling 2 delivers nothing.
**Owner clarification needed; it could ride DL-243 or stand as a one-line disposition.**

**Q2 — which register holds a governed defect row?** §6f says a defect violating an invariant *"is
recorded in the register"*. `origin/refresh/r21-from-main:release-2.1/QUEUED_WORK.md`
(69 rows, governance/tooling) and the acceptance
register (GT rows) are different objects. **Ruling 6 is not actionable until this names one.**
Recommendation, not a ruling: the **acceptance register**, since ruling 4 already puts the failing
server twin there — one artefact, one home.

### Ordering

**Ruling 5 first** — a single tooling change, no dependencies, and it makes every later validation
report legible. **Then 3 and 4 in parallel** (independent engineering tracks; 4 is the one that
prevents recurrence of the R2.0 blocking defects). **7 any time** — it is an access request, not a
build. **2 and 6 wait on Q1 and Q2.** **1 waits on #245.**

---

## Decisions this analysis puts to the owner

1. **G2** — does the application get a governing framework, and of what class?
2. **G4** — is the application quality gate made a required check, and at what scope?
3. **G5** — does the RED-proof rule that governs `tools/` extend to `code/`?
4. **G6** — must release validation cite gate output rather than narrative?
5. **G8** — what environments exist, who administers them, and what does promotion require?
6. **G10** — do product defects get a row type and a place in the queue?
7. **G12** — second canon approver: yes or no.

## Decisions this analysis puts to engineering

1. **G3** — split or parallelize the CI job so it completes inside its budget.
2. **G5** — RED tests for `stabilize_issue_ids` at and below threshold, and for `artifact_type` mismatch.
3. **G7** — expose a build identity surface.
4. **G11** — make an invalid `ACTIVE_DESIGN_REF` fail, never skip.
