# Build-readiness audit — 2026-08-29 · R2.0 staging · production fitness

**Trigger:** Owner request — "evaluate fitness and readiness for production", with issue
classification and resolution named as the priority focus.
**Subject:** the **running staging application** at
`https://intralign-oslo-web-staging-9f21dcd15274.herokuapp.com`, project `DevNorth 2026`
(`8ae4e3a5-9c16-440f-aa41-bb9319245122`), observed 2026-08-29.
**Auditor:** AI. **This report recommends; it ratifies nothing.**

## ▶ RESULT: **NOT FIT FOR PRODUCTION.** 4 blocking · 9 reported · 1 escalation.

⚠️ **Updated 2026-08-31: second pass added R5–R8, corrected R2 and confirmed R4 at source; third pass added B5, R9 and the DL-238 PASS, and qualified R1. B4 was raised as blocking and RETRACTED IN FULL the same hour — archive works. Five claims withdrawn this session, all from probe error, none from re-reading.**

**Three of the four blocking failures are one mechanism** (B1–B3; **B5** is separate — the first-run
progress screen never hands off to a completed read): findings have **no stable identity across
re-analyses**. Every governed act triggers a full re-read that re-derives the finding set from
scratch, so findings the user never touched are opened and closed underneath them, settled work
regresses to open, and the Grounding denominator moves. The honesty *ceremony* around resolution is
built correctly and passes every check I could put to it — but it is wrapped around a register that
does not hold still, which defeats what the ceremony is for.

⚠️ **This is a good-news/bad-news result and the shape matters.** The doctrine surfaces — the
basis picker, the pending tray, the capacity gate, the band vocabulary, the no-numeric-confidence
rule — are **built, and built well**. What is not production-ready is the analysis layer beneath
them. That is a materially different conversation from "the product is wrong."

---

## MEASUREMENT PROTOCOL — read before trusting a number

Every count in this report was taken from the **live staging DOM**, not from the repository. There
are no repo greps here. Each count-bearing claim names the surface, the action, and the extraction
used, in this form:

MEASURED-BY: `<extraction>` @ `<URL>` · <when in the session>

⚠️ **Two limits on all of it:**

1. **I cannot name the deployed build.** There is no version endpoint, no build stamp, no commit
   marker on any surface I found. `GET /api/workspace` carries no version field. So every claim below
   is a claim about *the staging app as it behaved on 2026-08-29*, and cannot be pinned to a commit.
   **Recommend this be fixed before any production cut** — an unidentifiable build cannot be
   audited, rolled back to, or reasoned about after an incident.
2. ⚠️⚠️ **CORRECTED 2026-08-30 — THE DEPLOYED APP IS IN THIS REPOSITORY.** Earlier drafts of this
   report claimed it was not. **That was wrong twice over and both claims are withdrawn.** The app is
   at **`code/apps/web`** (Next.js) on branch **`codex/r2-uat-remediation`** — PR **#248**, 990 files.
   Proof: `code/apps/web/next.config.ts` and `code/apps/web/src/app/api/workspace/route.ts` both
   resolve on that ref, the second being the exact endpoint audited in §What is clean.
   **How the error happened:** I read `code/` on the checked-out branch (`refresh/r21-from-main`),
   found the Release 1 FastAPI/Vite build, and reported on *the repository*. A branch is not the repo.
   See §Escalation for what survives.

---

## What is clean — stating it is part of the result

These were tested and passed. They are load-bearing doctrine and they hold.

MEASURED-BY: live browser walk of the staging app — `fetch('/api/workspace')` body inspected with a
recursive numeric-key scan (`/conf|matur|integrit|score|index|band|level|ground|viab|adapt|prob|readi|pct|percent|ratio/i`
over every numeric leaf → **0 hits**); `document.querySelectorAll('button,[role=button]')` for the
control inventory; `innerText` scans for band words, tray headings and footer copy. All @
`https://intralign-oslo-web-staging-…/projects/8ae4e3a5-…/{overview,issues}` and `/workspace`,
2026-08-29.

| check | verdict |
|---|---|
| **No numeric confidence in the payload (DL-237)** | ✅ **PASS.** `/api/workspace` carries `confidence_band: "Fragile"`, `reliability: "Low"`, `weakest_pillar: "Grounding"` — **band words only, zero numeric confidence/maturity fields.** The `confidence_index` DL-237 recorded as measured-present is **gone.** |
| **No numeric confidence on any surface** | ✅ **PASS.** No percentage, decimal, dial or score found on the overview. The `N of M grounded` counter — which canon *requires* — is present and correctly not a score. |
| **Basis is required and typed (F-24 / GT-26)** | ✅ **PASS, and this is the strongest thing in the build.** "Confirm — it holds" does **not** ground anything. It opens a basis picker: *I have it documented in writing · A vendor or owner verified it · I've verified this directly · It doesn't hold · Ask for evidence.* **No one-click grounding path exists.** The recorded basis is then displayed on the item (`Documented · Confirmed by Idris`, `Vendor-Or-Owner-Verified · Confirmed by Idris`). |
| **A click never reaches a terminal state (F-10 / GT-10)** | ✅ **PASS.** On confirm the item reads **"RECORDED — Your governed action was recorded. OSLO will re-read all three pillars to reflect it. · SETTLING TO RESOLVED"**, moves to an **"ACTED ON, NOT YET CLOSED"** tray marked *Waiting for reanalysis*, and **the three band words do not move.** The settled count did **not** increment at the moment of the click. |
| **A mitigated item never reads as closed (F-14 / GT-33)** | ✅ **PASS.** The "Acted on, not yet closed" tray is real, is separate from "✓ RESOLVED", carries its own `0 TO FIX · 0 TO GROUND` counters, and its contents are **excluded from the settled count.** |
| **Withdraw exists (F-23 / GT-25)** | ✅ **PRESENT** on both tray items and on settled items; `Undo last change` is offered on the consolidation banner. *(Presence verified; the append-vs-erase behaviour was not exercised — see §Not measured.)* |
| **Freemium gates capacity, never judgment (F-35/36/37)** | ✅ **PASS, exemplary — and the free path works.** ⚠️ *A qualification added here on 2026-08-31 claiming the free alternative was a dead control has been **retracted**; archiving issues a real `POST …/archive` and the project archives. See the struck B4.* Attempting a 2nd plan raises a gate that names the capability ("Run more than one plan"), the tier (**Basic**), and the price (**$29/mo · or $290/yr · 2 months free**), and states in the user's own words: *"This gates **capacity**, never the **quality** of your read — the accuracy bar and your record stay the same on every plan."* It offers a **free** alternative (archive to switch) and describes it as non-destructive. **No silent 422, no silent grant, no tier raised without checkout.** |
| **No portfolio roll-up** | ✅ **PASS.** `/workspace` states: *"No portfolio score across plans. OSLO assesses each plan on its own inputs and grounding — there is no average, ranking, or roll-up score."* |
| **"OSLO advises; you decide"** | ✅ Present as a persistent footer on every surface. Acts are named (confirm / doesn't hold / ask for evidence), **not** "Resolve" or "Apply". |
| **DL-240 fixed core** | ✅ **PASS.** Document rail reads **Intent · Scope · Requirements · Constraints** under UNDERSTANDING. **No surface names "Context"** as a core artifact. |
| **Console cleanliness** | ✅ **PASS.** Zero console errors on a tracked reload of `/projects/{id}/issues`. |

---

# FINDINGS

## B0 — ROOT CAUSE of B1, B2 and B3 · Added 2026-08-30, read from the deployed source

B1–B3 were argued from behaviour because the source was not available. It is now. **All three are one
defect in one module**, and it is contained.

MEASURED-BY: `git --git-dir=<repo>/.git grep -n …` and `git show` against
`origin/codex/r2-uat-remediation` (PR #248), read-only plumbing, 2026-08-30. Files:
`code/services/api/src/oslo_api/analysis/{issue_identity,workflow,issue_lifecycle,persistence,service}.py`.

**A finding's identity is a hash of the model's own prose.**

```python
# issue_identity.py:135-142, 225-230
def _tokens(issue):
    text = f"{issue.title} {issue.why}".casefold()
    return {t.rstrip("s") for t in re.findall(r"[a-z0-9]+", text)
            if len(t) > 2 and t not in _STOP_WORDS}

def _deterministic_id(issue):
    normalized = " ".join(sorted(_tokens(issue)))
    digest = hashlib.sha256(f"{issue.artifact_type.value}|{normalized}".encode()).hexdigest()[:12].upper()
    return f"ISS-{issue.artifact_type.value.upper()}-{digest}"
```

Nothing in that identity refers to the plan element the finding is *about*. Reword the sentence and
it is a different finding.

**Identity is not carried across runs — it is re-guessed.** At `AnalysisPhase.PUBLISH`
(`workflow.py:306-320`), `stabilize_issue_ids(raw.issues, previous_snapshot.assessment.issues)` runs.
Per `issue_identity.py:92-116`: ids prefixed `DET-` pass through untouched; an exact id match is
kept; otherwise `_best_match` scores token overlap over the union, **+0.15 for shared evidence refs,
matched only within the same `artifact_type`, at `score >= 0.38`** (`:119-132`). Below threshold, the
finding is **minted with a new id** and the previous one is dropped from the set.

**When identity is lost, the user's attestation is orphaned — not deleted, but unreachable.**
`Attestation` is keyed `issue_id` (`issue_lifecycle.py:52-59`). It persists as
`"issue_stable_key": issue.id` (`persistence.py:1602`) — the content hash itself, with no separate
durable key. Reads join `issue.stable_key = attestation.issue_stable_key` (`service.py:882`). When
the hash changes, that join finds nothing.

**This explains every observation, including the ones that looked contradictory:**

| observed | mechanism |
|---|---|
| B2 — settled venue finding returned as open at rank #1, reworded | rewording dropped `_best_match` below 0.38; new id minted; the attestation still points at the old hash |
| B2 — History still showed the confirm | the append-only trail keys off the same column and is intact (`history.py:262`); **the record is honest, the live read is wrong** |
| B1 — 24 → 23 → 29 | id churn from rewording, each run re-minting what it failed to re-match |
| B3 — denominator moved; numerator fell to 0 | the grounded population is re-derived per run; grounding credit attaches to ids that vanished |
| R3 — five venue findings, four checkpoint clones | one weakness surviving as several ids |

⚠️ **`_best_match` requires `candidate.artifact_type is issue.artifact_type`.** A finding that moves
artifact between runs loses identity **unconditionally**, however identically worded.

**The fix direction is already in the file.** The `DET-` branch shows deterministic identity is
already a first-class concept. Identity should derive from *what the finding is about* — artifact +
plan element + weakness class — not from how it was phrased. **Tuning 0.38 only moves where it
breaks.**

⚠️ **B1's flip condition is now superseded, not satisfied.** The control run (three re-analyses, zero
acts) would still be useful, but source evidence outranks it: the churn does not require a user act,
only a reworded title. **Engineering should confirm this reading before it is treated as ratified —
I read the code; I did not run it.**

---

## ~~B4~~ — ⚠️⚠️ **RETRACTED IN FULL, 2026-08-31, WITHIN THE HOUR. ARCHIVE WORKS.**

**The claim below is false and is withdrawn. It is retained, struck, because a blocking finding that
was published and then wrong should be legible as such — not deleted.**

MEASURED-BY: `window.fetch` instrumented, then the card's archive control invoked with
`element.click()` in the page → **`POST /api/workspace/projects/8ae4e3a5-…/archive` captured**;
`/workspace` then renders `ARCHIVED (1)`. Source cross-read at
`origin/codex/r2-uat-remediation:code/apps/web/src/components/workspace/workspace-home.tsx:92-121,239-242`.
All 2026-08-31.

**What actually happens.** Clicking the project card's archive control issues
`POST /api/workspace/projects/{id}/archive`, the project archives, and `/workspace` renders
**`ARCHIVED (1) · DevNorth 2026 · Read-only · retained safely · Restore`**. Verified with the same
`window.fetch` instrument that reported zero.

**Why I got it wrong — and it is the same error three times today.** The archive control on the card
is **icon-only**: `aria-label="Archive DevNorth 2026"`, no text node, a ~14px target. My synthetic
coordinate/ref click **missed it**, and I read the miss as the product doing nothing. The identical
mistake produced the withdrawn "silently inert" claim in R8, and a `ref` click that never registered
before that.

**Two compounding method errors:**
1. **`innerText` cannot see an `aria-label`.** My "no archive control exists anywhere in the product"
   sweep filtered buttons on visible text, so an icon-only control was structurally invisible to it.
   The same blindness hid the sidebar's "Your plan" card.
2. **A synthetic click that misses is indistinguishable from a control that does nothing** — unless
   the click is verified independently. `element.click()` in the page succeeded where the coordinate
   click failed.

**The source was right all along** and I should have weighted it over my own probe:
`workspace-home.tsx:92-121` implements `setArchived` with a real `fetch(POST …/archive)` and proper
error handling; `:239-242` wires `onArchive={() => void archiveAndCreate()}`; and
`api/workspace/projects/[projectId]/{archive,restore}/route.ts` both exist. **When source and probe
disagree, the probe is the thing to re-examine first.**

**What remains genuinely untested:** the archive button *inside the capacity modal*. I never
successfully opened that modal — `modalOpen: false` was reporting the truth and I dismissed it as a
regex artifact. **No evidence it is broken; simply not exercised.** Recorded in §Not measured.

---

<details><summary>The retracted claim, retained verbatim</summary>

## B4 — BLOCKING · The capacity gate's only free alternative is a dead control

Added 2026-08-31. **This qualifies the praise given to the freemium gate below — the copy is
exemplary; the free path does not work.**

The capacity gate offers a Free user exactly two ways forward: **"Unlock Basic — compare plans"**
($29/mo) and **"Archive DevNorth 2026 to switch (free)"**. Clicking the second one dismisses the
modal and **does nothing at all.**

MEASURED-BY: `window.fetch` and `XMLHttpRequest.prototype.open` both instrumented, buffer cleared,
then the Archive CTA clicked → **0 requests captured**. Instrument RED-proved immediately afterward
with a manual `fetch('/api/workspace')` → captured, so zero is a real zero and not a broken probe.
Server state re-read after the click: `archived: false`, `can_create_project: false`,
`updated_at` unchanged at `2026-08-29T23:57:20Z`. `/workspace` still renders **ARCHIVED (0)**.
All @ `/workspace`, 2026-08-31.

**It is not a failed write — it is no write.** No request is attempted, so there is nothing to
retry and nothing to report as an error.

⚠️ **And it is the only archive affordance in the product.** A search of the project's own settings
menu and every control on the project surfaces returns **no archive control** (`/archive|delete|remove|close project/i`
over all buttons and links → 0 matches). So the sequence a Free user is offered is:

> want a second plan → gate → *"archive to switch (free)"* → nothing happens → **the only working exit is $29**

**Why this is blocking rather than reported.** The gate's honesty rests on the free alternative being
real. Its own copy says *"This gates **capacity**, never the **quality** of your read"* and offers
archiving as the no-cost route — and canon requires that every offered path perform the write it
claims (GT-75), that a no-op be loud (GT-88), and that no resolver dead-ends (GT-112). **In effect,
though plainly not in intent, the paywall presents a free choice that does not exist.** The copy is
scrupulous; the button is inert. That gap is exactly what DL-242 was ratified about.

⚠️ **This also blocks part of this audit.** Intake, first-run and the 60s Fast Pass promise cannot be
measured without a second project slot, and the supported route to one does not function. Those
remain **NOT MEASURED** — see §Not measured.

</details>

⚠️ **Consequence of the retraction: archiving works, so the intake / first-run / 60s Fast Pass tests
are UNBLOCKED.** They were never blocked by the product.

---

## B1 — BLOCKING · The finding set is not stable across re-analyses of an unchanged plan

**The plan documents were never edited during this session.** The only inputs I supplied were two
attestations. Across three consecutive re-analyses the register did this:

| run | detected | churn reported by the app |
|---|---|---|
| 1 | **24 issues** | *"7 opened and 10 resolved in this read"* |
| 2 | **23 issues** | *"1 opened and 3 resolved in this read"* |
| 3 | **29 issues** | *"8 opened and 3 resolved in this read"* |

MEASURED-BY: reading the append-only trail at `/projects/8ae4e3a5-…/history`, entries listed
newest-first, each `ISSUES` entry paired with the `YOUR DECISIONS` confirm that preceded it.

**Across three runs — each triggered by exactly one confirm — the engine reports opening 16 findings
and resolving 16 (7+1+8 opened, 10+3+3 resolved), against three user acts.** ⚠️ Precision note: the
earliest of the three confirms in the trail (`No venue dependency…`) **predates this session** and
was not mine; the two later ones were. The churn ratio is unaffected. The extraction layer moved too
— per-artifact detail counts, on the same unedited documents:

| artifact | before | after |
|---|---|---|
| Intent | 5 | **12** |
| Scope | 6 | **5** |
| Requirements | 3 | **13** |
| Schedule | 5 | **9** |
| Resources | 7 | **8** |
| Work breakdown | 1 | 1 |

MEASURED-BY: `document.querySelectorAll('a[href*="/artifacts/"]')` innerText @
`/projects/8ae4e3a5-…/issues`, first load vs. after the third re-analysis.

**Why this is blocking, not cosmetic:** the entire honesty model rests on *only-reanalysis-resolves*.
That rule is only meaningful if re-analysis is a **re-derivation of the same plan**, not a
**re-generation of a different finding set**. As built, the user cannot distinguish "OSLO changed its
mind because I gave it evidence" from "OSLO produced a different answer to the same question."

**Root cause (inferred, and flagged as inference):** findings appear to be identified by their
generated title rather than by a stable structural id, so a re-run mints new rows instead of
superseding existing ones. **I did not verify this in source — the source is not in this repo.**
Escalate to engineering rather than treating my inference as the diagnosis.

**FLIP CONDITION — what would prove me wrong:** run three consecutive re-analyses with **zero** user
acts. If the finding set is byte-stable across all three, then the churn is caused by attestation
specifically, not by nondeterminism, and B1 must be re-scoped. **I did not run that control** — see
§Not measured. **Run it before acting on this finding.**

---

## B2 — BLOCKING · Settled work regresses to open without a withdraw

At first load, the ✓ RESOLVED tray contained **"No venue dependency is secured or bounded for the
planned attendance"**, and History records the confirm that settled it.

After two unrelated confirms and their re-analyses, that finding is **gone from the resolved tray and
gone from the page entirely**, and a finding reading **"Venue dependency is unsecured and
unbounded"** is now **open at rank #1, badged `◆ DO THIS NEXT`**.

MEASURED-BY: `document.body.innerText.indexOf('No venue dependency is secured or bounded')` → `-1`
and `.indexOf('Venue dependency is unsecured and unbounded')` → present, @
`/projects/8ae4e3a5-…/issues`, after re-analysis 3. Persisted across a full page reload, so this is
server state, not client state. **I performed no withdraw and no undo at any point.**

This is a direct failure of *nothing settled regresses when a batch lands* (GT-67). The user's
attested work was silently un-done and handed back to them as their top priority.

**Second instance of the same mechanism:** the finding *"Scope reads solid — but on OSLO's
inference, not your evidence"* was open at baseline and is absent after re-analysis, present in
neither tray, with no disclosure that it left. Findings **disappear** as well as regress.

---

## B3 — BLOCKING · Verification moved Grounding the wrong way, and the denominator is unstable

The Grounding counter over the session, with two attestations recorded and no plan edits:

| moment | Grounding reads |
|---|---|
| baseline | **Grounded 1 of 24** load-bearing |
| after confirm 1 | **1 of 23** |
| mid-run, History surface | **0 of 29** — *numerator fell to zero* |
| converged | **2 of 29** |

MEASURED-BY: `innerText.match(/Grounded \d+ of \d+ load-bearing/)` @ `/projects/8ae4e3a5-…/issues`
and `…/history`, sampled at each stage.

Two separate failures here:

1. **The denominator is not stable** (24 → 23 → 29). Under canon, *N* is the count of load-bearing
   details; confirming one should move the **numerator**, never shrink the population. A user who
   grounds a detail and watches the total change cannot read the number as progress.
2. **The numerator regressed to `0` after two successful attestations.** Whether transient or not,
   *only-verify-moves-Grounding* is violated in its worst direction: verification moved Grounding
   **down**.

**Same mechanism on the Adaptability pillar:** at baseline it read **Fragile** on
*"0 of 0 outcome checkpoints are registered"* — a **zero denominator**, i.e. nothing assessed, taking
the **worst** band. That is *unknown read as bad*, which canon prohibits. After re-analysis it read
*"0 of 4 outcome checkpoints are registered"*, where Fragile is legitimate. **The doctrine violation
and its self-correction are both products of the same instability.**

---

## R1 — REPORTED · The composite reads two different words on two surfaces, simultaneously

For the same project, at the same moment, both surfaces agreeing that there are 27 open issues:

- `/workspace` → **"Outcome Integrity · Fragile · gated by its weakest pillar"**
- `/projects/{id}/overview` → **"OUTCOME INTEGRITY · Under review"**

MEASURED-BY: `innerText.match(/Outcome Integrity\s+\w+/g)` @ `/workspace` → `Fragile`; and
`innerText.match(/OUTCOME INTEGRITY\s*\n\s*[A-Za-z ]+/)` @ `/projects/8ae4e3a5-…/overview` →
`Under review`. Both after convergence, both reporting 27 open issues. **Verified after
convergence specifically, so this is not the mid-run transient of B3.**

`Fragile` is a band word from the canonical ramp. **`Under review` is not in the ramp at all.** One
judgment is being rendered as two different words in two vocabularies, on the two screens a user
moves between most often.

---

## R2 — REPORTED · Severity is effectively binary, so the ranked worklist carries little signal

Across two independent analysis runs, **only two severity values were ever emitted:**

| run | CRITICAL | MODERATE | other |
|---|---|---|---|
| baseline (23 open) | **16** | 7 | **0** |
| after (27 open) | **17** | 10 | **0** |

MEASURED-BY: tallying the chip line following each dimension chip in
`document.body.innerText.split('\n')` @ `/projects/8ae4e3a5-…/issues`, both runs.

**63% of all findings are CRITICAL.** A worklist that tells the user twenty-seven things and calls
seventeen of them critical has not prioritised anything — and the product's central promise is
*"YOUR WORK — MOST IMPORTANT FIRST."*

⚠️ **CORRECTED 2026-08-30.** An earlier version of this finding cited
`code/backend/responsibilities/evaluate/engine.py:256-273` — a severity function that is a pure
function of `finding_type`/`gap_kind` and leaves three of five severity values unreachable — and
suggested the deployed app shares it. **That citation is against the Release 1 build, which is not
what ships.** The deployed severity logic is in the `codex/r2-uat-remediation` monorepo
(`code/services/api`, `code/apps/web`) and **I have not read it.** The R1 resemblance is now a
hypothesis worth one grep, not evidence. The *observation* — two severity values across 27 findings
and three independent runs — stands on its own and is unaffected.

---

## R3 — REPORTED · The taxonomy over-produces near-duplicates, and merges what it should decompose

From the current 27 open findings:

- **Five venue findings:** #1 venue dependency unsecured · #4 venue decision deadline absent ·
  #5 no venue fallback · #12 venue decision has no named owner · #23 venue acceptance/testing absent.
- **Three overlapping measurement findings:** #21 no outcome measures or timing · #22 attendance is
  not an outcome framework · #26 objectives have no outcome measures beyond date/duration/attendance.
- **Four formulaic Adaptability clones**, one per artifact area, differing only in their subject:
  #16 *"Objectives and outcome chain definition has no outcome checkpoint"* · #17 *"Intervention and
  deliverable traceability has no outcome checkpoint"* · #18 *"Venue and attendance readiness has no
  outcome checkpoint"* · #19 *"Programme and delivery confirmation has no outcome checkpoint"*.
  This is what doubled the Adaptability count from 4 to 8.
- **A merged multi-aspect finding sitting beside its own components:** #3 *"Ownership, capacity and
  **funding** are unconfirmed"* coexists with #10 *"Delivery ownership and capacity are absent"* and
  #11 *"No budget or funding decision"*. Canon requires multi-aspect findings to be **decomposed,
  never merged**; here the product does both at once and presents all three as peers.

MEASURED-BY: full enumeration of worklist rows via `document.querySelectorAll('button')` filtered
to `/^\d+ /` @ `/projects/8ae4e3a5-…/issues` after re-analysis 3 (27 rows returned, listed in full
in the session transcript).

---

## R4 — REPORTED · Colour carries pillar identity, not maturity — and the weakest pillar renders green

| pillar · band | rendered colour |
|---|---|
| Viability · **Developing** | `rgb(127, 160, 201)` — blue |
| Grounding · **Fragile** | `rgb(79, 195, 161)` — **green** |
| Adaptability · **Fragile** | `rgb(217, 138, 192)` — pink |

MEASURED-BY: `getComputedStyle(el).color` over leaf elements whose text matches
`/^(Developing|Fragile|Weak|Solid|Sound)$/` @ `/projects/8ae4e3a5-…/overview`.

**Two pillars reading the identical band word render in different hues, and the better band renders
in a third.** This is not RAG — there is no red/amber/green semantics — so the literal prohibition is
not breached. The honesty problem is subtler and, I would argue, worse: **Grounding is the FLOOR
pillar gating the entire composite, it reads Fragile, and it is painted the colour users read as
"healthy."** The visual channel contradicts the word it is attached to.

**Also in this family — two smaller instances of prose asserting what the mechanism does not make
true (DL-242):**

- The History sparkline reads **"— steady this session"** while, in that same session, the totals
  moved 24 → 23 → 29 and Grounding moved 1 → 0 → 2.
- The card-collapse control carries `aria-label="Close issue"`. It collapses the card; the issue
  stays open. **RED-proved in both directions:** after clicking it the open count held at 23 and the
  settled count held at `1 of 24`, so this is a mislabel, **not** a resolution bypass. But a
  screen-reader user is told a control closes an issue that it does not close — and "close the issue"
  is precisely the execute-shaped claim the resolution model forbids.
- ⚠️ **RETRACTED 2026-08-31.** An earlier version of this bullet called the prompt *"Why is
  Feasibility where it is?"* stale vocabulary, on the grounds that no Feasibility pillar exists.
  **Wrong.** Opening an issue card shows **`AFFECTS: Scope · Feasibility`**, and another shows
  `Intent · Clarity` — so Clarity and Feasibility are **live CAF dimensions in the Affects layer**,
  distinct from the three pillars. The prompt is correct and the finding is withdrawn.
  **I inferred absence from the surfaces I had opened, having never opened a card on this pass.**

---

## THIRD PASS — 2026-08-31 · intake, first-run and injection, on a throwaway project

Owner-authorised. `DevNorth 2026` archived to free the slot; test project **Northwind Summit 2027**
(`738c9b0b-…`) created from an 828-character pasted plan seeded with injection payloads.

MEASURED-BY: plan text set via the native `HTMLTextAreaElement` value setter (828 chars, verified by
length equality), submitted through the intake button; timings from an in-page 400 ms poller; DOM
probes by attribute count, not regex. All @ `/intake?project=738c9b0b-…` and
`/projects/738c9b0b-…/{overview,artifacts/requirements,full-plan}`, 2026-08-31.

### Archive/restore — ✅ PASS · the non-destructive claim is true, and was verified rather than trusted

The capacity gate asserts *"Archiving is non-destructive: History, issues and the latest assessment
remain restorable."* **DL-242 says prose may not assert what the mechanism does not make true, so the
claim was tested against a baseline captured before archiving.**

MEASURED-BY: `/api/workspace` project object compared field-by-field, pre-archive vs post-restore.
2026-08-31.

| field | before archive | after restore |
|---|---|---|
| `open_issues` | 27 | **27** ✅ |
| `artifact_count` | 7 | **7** ✅ |
| `confidence_band` | Fragile | **Fragile** ✅ |
| `reliability` | Low | **Low** ✅ |
| `weakest_pillar` | Grounding | **Grounding** ✅ |
| `analysis_status` | current | **current** ✅ |
| `archived` | false | **false** ✅ |
| `updated_at` | `2026-08-29T23:57:20Z` | `2026-08-31T18:20:24Z` ⚠️ |

**Every substantive field round-tripped exactly.** The only change is `updated_at`, which now records
the archive/restore rather than the last analysis — a minor honesty wrinkle, since a reader would
reasonably take that timestamp to mean "last assessed."

⚠️ **NOT A FINDING — instrument noise noted for the record.** My network log showed each request
twice, including `POST …/restore`. That is most likely my `fetch` wrapper having been installed over
itself, not a double-submit by the app. **Not reported as a defect; flagged so the log is not
misread later.**

### B5 — BLOCKING · The first-run progress screen never hands off to the completed read

**This is the activation moment — the first thing a new user ever sees — and it strands them.**

MEASURED-BY: in-page poller sampling `document.body.innerText` every 400 ms for `/STAGE \d+ OF \d+/`,
timestamps offset from submit; then a direct navigation to `/projects/738c9b0b-…/overview`.
2026-08-31.

| elapsed from submit | progress screen |
|---|---|
| 22 s | `STAGE 6 OF 8` |
| 65 s | `STAGE 7 OF 8` |
| 67 s | `STAGE 8 OF 8` — *"Your strategic read is ready. Preparing your initial read…"* |
| 110 s | unchanged |
| 156 s | unchanged |
| **225 s** | **unchanged — still "ANALYZING…"** |

**At 225 s the screen was still analyzing. Navigating directly to the project showed a complete
read** — *Northwind Summit 2027 · OUTCOME INTEGRITY Fragile · 13 issues · 7 artifacts*. **The
analysis had finished; the screen simply never advanced.** A first-time user with no reason to
navigate away would wait indefinitely in front of a finished product.

⚠️ **The screen contradicts itself while stalled**: it renders **"Your strategic read is ready"**
and **"ANALYZING…"** and **"Preparing your initial read…"** simultaneously, for over two minutes.
Prose asserting what the mechanism has not done — DL-242 again, on the highest-stakes surface in the
funnel.

⚠️ **NOT-MEASURABLE — the true Fast Pass duration.** I can prove the read was complete *before* 225 s
and that the screen had not advanced *by* 225 s, but not the moment the server finished. **The 60 s
promise is therefore neither confirmed nor refuted; what is measured is that the user is not told.**

### R9 — REPORTED · the 60 s promise is made twice and disclosed nowhere when missed

Intake states *"Your first read is usually ready in under a minute."* The progress screen states
*"Preliminary Outcome Analysis · up to about a minute."* At 110 s and again at 225 s, a scan for
`/still working|taking longer|longer than|provisional|over/i` returned **no match** — **no
over-budget disclosure of any kind.** Canon distinguishes a slow-but-honest degrade from a
slow-and-silent one; this is the second.

**Credit where due:** the progress narration itself is good — eight named stages (*read inputs · drafted
plan · separated evidence from inference · mapped what your outcome rests on · noted your open
questions · assessed Viability · Grounding · Adaptability*), not a spinner.

### DL-238 / GT-92 — ✅ PASS · injection round-trips as literal text

MEASURED-BY: payload `<img src=x onerror=alert(1)>` submitted inside the plan text; the rendered
Requirements artifact then inspected. 2026-08-31.

| probe | result |
|---|---|
| Payload visible as literal text | ✅ `"<img src=x onerror=alert(1)>"` present **byte-for-byte** |
| Element nodes created from it | ✅ **0** (`img[src="x"]`) |
| Elements carrying an `onerror` attribute | ✅ **0** — counted by attribute, not regex |
| Attribute-context breakout (`onmouseover`) | ✅ **0** |
| Entity-mangling at capture (`&lt;img`, `&quot;`) | ✅ **none** — the raw text survived, which canon requires |

⚠️ **A regex over `innerHTML` reported `onerror=` present; counting actual attributes returned 0.**
The hit was inside a script/JSON blob. **Counting the attribute is the subject; the regex was a proxy.**

⚠️ **NOT MEASURED:** the attribute-context payload (`" onmouseover="alert(2)`) was placed in a
`Notes:` line that OSLO did not map to any artifact, so it surfaced nowhere and that vector remains
untested. Also untested: payloads in an **uploaded document**, in an outcome title, and in a comment.

### R1 — QUALIFIED · "Under review" may be a state, not a competing vocabulary

MEASURED-BY: `innerText` of the masthead @ `/projects/738c9b0b-…/overview` (fresh project, no pending
acts) vs `/projects/8ae4e3a5-…/overview` (two acts awaiting re-analysis), 2026-08-31.

The fresh project's masthead reads **`OUTCOME INTEGRITY Fragile`** — a band word, matching
`/workspace`. `DevNorth 2026`'s masthead read **`Under review`** while every other surface said
Fragile. **The difference: DevNorth had acted-on items awaiting re-analysis.** So "Under review" is
plausibly a legitimate *pending* state rather than a vocabulary collision.

**R1 is not withdrawn — the same-page contradiction on `/outcome` still stands — but its
interpretation is now open.** The flip condition: put the test project into a pending-reanalysis
state and see whether its masthead also switches to "Under review". **Not yet run.**

## SECOND PASS — 2026-08-31 · the four surfaces the first pass never opened

Reports · Grounding map · Your Outcome · Full plan/export. Owner-authorised continuation.

MEASURED-BY: live browser walk with `document.body.innerText` extraction and `getComputedStyle`
@ `/projects/8ae4e3a5-…/{reports,grounding,outcome,full-plan}`, 2026-08-31.

### What passes — and these are real

MEASURED-BY: `document.body.innerText` string-equality on the 700-char summary slice before and
after switching recipient; whole-object equality of `{nav, pillars, composite, artifact counts}`
pre/post report generation; `/upgrade|locked|Basic|\$29/i` over the full-plan surface; and
`t.match(/\d+ of \d+[a-z \-]*/gi)` for the counter agreement. All @
`/projects/8ae4e3a5-…/{reports,grounding,outcome,full-plan}`, 2026-08-31.

| check | verdict |
|---|---|
| **GT-105 · tailor the ask, never the read** | ✅ **PASS, byte-exact.** Switching recipient Exec sponsor → Board changed `To:` and `Prepared for` and left the substantive summary **identical** (string equality on a 700-char slice). The ask moves; the read does not. |
| **GT-31 / GT-14 · reports and projections write nothing** | ✅ **PASS.** Generating and re-targeting reports left nav count, all three band words, the composite and all seven artifact counts unchanged (whole-object equality, pre vs post). |
| **GT-28 · export is never maturity-gated** | ✅ **PASS.** At Fragile the full-plan export renders and offers `Export plan`; no upgrade, lock or warning gate (`/upgrade|locked|Basic|\$29/i` → no match). |
| **GT-32 · one Grounding judgment** | ✅ **PASS across three surfaces** — *"2 of 29 load-bearing details grounded"* · *"2 of 29 settled"* · *"2 of 29 … rest on your evidence"*, agreeing with the overview. ⚠️ **My own test cannot separate the two measures**: two confirms produced two settled issues *and* two grounded details, so the numerators coincide. Re-test with an act that settles without grounding. |
| **GT-02 · declaring an outcome is never metered** | ✅ Rendered as **"+ Declare an outcome · FREE"**. |
| **Honesty disclaimer in generated prose** | ✅ The briefing states: *"This is OSLO's understanding of the plan—not project health, readiness, or a probability of success."* Exactly the doctrine, in the artifact that leaves the building. |

### R1 — UPGRADED · the composite contradicts itself on a single page

The first pass reported this as a `/workspace` vs project-masthead drift. It is worse than that.

MEASURED-BY: `/OUTCOME INTEGRITY\s*\n\s*([A-Za-z ]+)/g` over `document.body.innerText` @
`/projects/8ae4e3a5-…/outcome` → **two matches on one page: `Under review` and `Fragile`.**

`/workspace`, `/grounding` and `/full-plan` all say **Fragile** (*"Outcome Integrity is Fragile"*).
**The project masthead is the single outlier, and on `/outcome` it sits directly above a card
contradicting it.** `Fragile` is a band word; **`Under review` is in no ramp**. This is one surface to
correct, not a vocabulary to reconcile.

### R5 — NEW · the generated briefing states a different read from the product

The Executive Briefing summary reads:

> *"The read is **very low confidence**, limited by **clarity**; 27 open findings identify the main
> uncertainty."*

Two defects in one sentence:

1. **"very low confidence"** is confidence vocabulary. The ramp is Fragile · Weak · Developing ·
   Solid · Sound, and the product's own line two paragraphs later is *"maturity, not a forecast"*.
   The band word never appears in the briefing.
2. **"limited by clarity"** contradicts every other surface. The masthead reads *"limited by
   Grounding"*, `/outcome` chips Grounding **`GATING →`**, and `/full-plan` opens *"Grounding is the
   current gate."* **The briefing names a different limiting pillar than the product does.**

⚠️ **This is the surface that leaves the building.** A sponsor reading it receives a different
assessment, in a different vocabulary, from the one the owner sees.

### R6 — NEW · the briefing reports engine churn to stakeholders as plan change

MEASURED-BY: the rendered Executive Briefing body @ `/projects/8ae4e3a5-…/reports`, read via
`innerText` from the `Summary` heading, 2026-08-31; cross-checked against the History trail's
`ISSUES` entries recorded in B1.

Under **"What changed"** the briefing states **"8 opened · 2 resolved"**. Per B0, the 8 openings are
re-derivation artifacts of the identity churn — the plan was never edited — while only the 2
resolutions were user acts.

**B1's blast radius therefore extends outside the product.** An exec sponsor is told eight new
problems appeared in a plan that did not change. Fixing B0 fixes this; nothing else does.

### R2 — CORRECTED AT SOURCE 2026-08-31 · the scale is three-valued, and `High` collapses into `Critical`

The behavioural finding said severity is "effectively binary". The source says something more precise.

MEASURED-BY: `git show origin/codex/r2-uat-remediation:code/services/api/src/oslo_api/analysis/result_contract.py`,
2026-08-31.

```python
ISSUE_SEVERITIES = frozenset({"Warning", "Moderate", "Critical"})
_SEVERITY_ALIASES = {
    "warning": "Warning", "low": "Warning",
    "moderate": "Moderate",
    "high": "Critical",          # ← lossy
    "critical": "Critical",
}
```

**Three canonical values, not five — and `high` is normalised to `Critical`.** Anything the model
judges *high* is presented to the user as *critical*, and the two are no longer distinguishable
anywhere downstream. That is the mechanism behind the observed **17 of 27 critical**: the Critical
bucket absorbs two of the model's own distinctions.

⚠️ **This is a contract, not a bug** — `_canonicalize_issue` raises `ISSUE_SEVERITY_CONTRACT_FAILED`
on anything else, which is properly fail-closed. The finding is the **design consequence**: a
worklist headed *"MOST IMPORTANT FIRST"* cannot prioritise when its top band is a merge of two.
**Owner question: is `high → Critical` intended, or should Warning · Moderate · High · Critical be
four?** The third value, `Warning`, appeared **zero times** in 29 findings.

### R4 — CONFIRMED AT SOURCE 2026-08-31 · colour is keyed to pillar identity

MEASURED-BY: `git grep -nE "4fc3a1|7fa0c9|d98ac0" origin/codex/r2-uat-remediation -- code/apps/web`,
2026-08-31.

`globals.css` defines `.issue-layer-pillar.pillar-adaptability { color: #d98ac0; }` — **the selector
is the pillar name, not the band** — and the palette tokens are `--cool: #7fa0c9` (Viability) and
`--grounded: #4fc3a1` (Grounding). Those hexes are exactly the `rgb(127,160,201)` and
`rgb(79,195,161)` measured in the browser, so **source and behaviour agree**.

⚠️ Note the token name: **`--grounded`, green, is bound to the Grounding pillar** — which was reading
**Fragile**. The variable is named for the good state and applied regardless of state.

### R8 — NEW · failure handling is designed on one surface and raw on another (GT-A3 / GT-A1)

Network failure simulated by rejecting every `window.fetch` in the page — client-side only, nothing
sent to the server.

MEASURED-BY: `window.fetch = () => Promise.reject(new TypeError('Failed to fetch'))`, then driving
each surface and diffing `document.body.innerText` line-sets before/after @
`/projects/8ae4e3a5-…/issues`, 2026-08-31.

| surface, network down | result |
|---|---|
| **OSLO chat** | ✅ **PASS — designed.** Renders *"OSLO could not answer right now. **Your project data is unchanged.**"* An error **and** the reassurance that matters most in a governed product. |
| **Issue card render** | ✅ No defect. The card opens fully offline; the 13 rejected calls were Next.js route prefetches. |
| **A governed act (confirm + basis)** | ⚠️ **Split verdict.** **Substance passes:** the act did not report success — settled held at *2 of 29*, the open count held at 27, nothing claimed RECORDED. **Presentation fails:** the only thing shown to the user is the raw JavaScript exception string **`Failed to fetch`**, with no explanation, no retry, and none of the reassurance the chat surface gives. |

**So GT-A1 holds — working does not read as done — and GT-A3 is half-built.** The pattern to fix is
narrow: one surface already has the right treatment, and the act path should inherit it.

⚠️ **THREE CLAIMS WITHDRAWN FROM THIS TEST, recorded rather than deleted.**
1. *"Clicking an issue offline is silently inert"* — **false.** The online control produced the
   identical result (0 fetches, 0 new lines): the click was not registering. **My automation, not the
   app.** Only a chevron click opens the card.
2. *"No error is shown"* — my detector tested `/couldn/` and could never have matched
   *"could **not**"*. **A regex guessing at vocabulary is a proxy;** the line-set diff is the subject.
3. *"`cardOpened: true`"* — false positive: `"Documented · Confirmed by Idris"` in the resolved tray
   matches `/Confirm/`.

### R7 — NEW · two smaller defects on stakeholder-facing surfaces

MEASURED-BY: `innerText` of the Key risks section @ `/…/reports`, and
`/[↑↓] ?[a-z ]*this session/` @ `/…/outcome` → `"↑ weakened this session"`. 2026-08-31.

- **A raw evidence token reaches exec-facing prose.** The Key risks section renders
  `[description:1]` inline mid-sentence.
- **A directional glyph contradicts its own word.** `/outcome` renders **"↑ weakened this session"** —
  an **up** arrow labelled *weakened*. Same DL-242 shape as the "steady this session" sparkline in R4:
  the visual channel asserts what the words deny.

---

## Escalation — for the owner, not for me to resolve

MEASURED-BY: `grep -rn -il 'intralign-oslo-web-staging' . --exclude-dir=.git` → **exit 1, zero
matches**; `cat code/README.md` line 1 → `# OSLO Release 1 — Application (code/)`; `ls 20_handoff/`
→ the cited `R2.0_DEFECT_REMEDIATION_HANDOFF.md` is **absent**; route names read from the live app's
own anchor hrefs. All @ `/Users/macuser/GitHub/oslo-knowledge-base` on branch
`refresh/r21-from-main`, 2026-08-29.
⚠️ NOT-MEASURABLE: whether that handoff file exists on another branch — git is not run against this
path by standing rule, so its absence is measured **for this checkout only**, not for the repo.

⚠️⚠️ **SECOND RETRACTION, 2026-08-30 — read this first.** The premise under both earlier versions of
this section was that the deployed app lives in a different repository. **It does not.** It is at
`code/apps/web` on `codex/r2-uat-remediation` (PR #248, 990 files, +186,990/−495, by TaimoorSohail1),
targeting `main`. I established "absent from the repo" by reading one branch and never enumerating
refs — the identical proxy-for-subject error as the first retraction below, committed twice in one
session. **Everything framed as "no traceability" is withdrawn.**

**What survives, and it is sharper than what it replaces — the software gate is the only gate that
did not pass.** On PR #248:

MEASURED-BY: the checks panel at `github.com/idris-manley/oslo-knowledge-base/pull/248`, 2026-08-30.

| check | result |
|---|---|
| `Doc Integrity (KIA2-1) / doc-integrity` — **Required** | ✅ 13s |
| `Queued work check / queued-work` | ✅ 15s |
| `Altering PR base guard (F002 §8c-i) / altering-base` | ✅ 3s |
| **`OSLO application quality gates / verify`** | ⚠️ **Cancelled after 75m** |

Three document gates pass in **under 15 seconds each and one is Required**. The gate that tests the
**990-file application** ran for **75 minutes and did not complete** — and is **not** a required
check (RB-056), so it blocks nothing. The PR sits awaiting code-owner review, mergeable.

⚠️ **And the validation contradiction, which is the whole problem in one line.** #248's own evidence
(`code/docs/r2-live-staging-validation-report-2026-08-28.md`, cited in the PR body) reports **"live
staging review: 8 sections passed, 2 partial, 0 failed."** This audit, run against the same staging
app one day later, found **3 blocking defects**. Both cannot be right about the same build. Either
the validation does not test finding-identity stability across re-analyses, or something regressed in
a day. **That question is worth more to the release process than any single finding in this report** —
a validation regime that returns "0 failed" on a build a doctrine audit fails is not yet measuring
what the doctrine requires.

---

⚠️ **FIRST RETRACTION, retained.** An earlier draft claimed "the running product has no traceability
to the canon that governs it," on the strength of the app source being in a different repository.
**That claim was wrong and is withdrawn.** A separate app repo is normal engineering practice and is
explicitly anticipated by this project's own brief. I asserted the absence of a seam **without
opening the directory that holds it** — the same proxy-for-subject error the measurement rule exists
to catch. The retraction is recorded here rather than deleted.

**What `20_handoff/` actually contains:** 34 files across `contracts/`, `interfaces/` and
`traceability/` — including a 372-line API contract specification, an endpoint catalog, state and
event models, and a build/test/observe traceability matrix. The catalog lists `/workspace`,
`/projects`, `/findings`, `/notifications`; the deployed app serves `/api/workspace`,
`/projects/{id}/…` and notifications. **The seam exists and the deployed app plausibly realizes it.**

**The narrower finding that survives measurement: the seam is R1-shaped, and R2 has no interface
contract in it.**

MEASURED-BY: `find 20_handoff -type f | wc -l` → **34**;
`grep -rl -E 'R2|release-2|Release 2' 20_handoff/ | wc -l` → **5**;
`grep -rn -icE 'viability|grounding|adaptability' 20_handoff/` → **1 file, 1 hit** (a crosswalk).
All @ `/Users/macuser/GitHub/oslo-knowledge-base` on `refresh/r21-from-main`, 2026-08-29.

- **29 of 34 handoff files are Release 1.** There is no R2 API contract, no R2 endpoint catalog, no
  R2 state or event model.
- The R2 concepts this audit actually exercised — the three pillars, the band ramp, the
  acted-on-not-yet-closed tray, the finding lifecycle, the Grounding counter — appear in the seam
  **once, in one crosswalk file.** The behaviours in findings B1–B3 have **no interface contract to
  be judged against.** That is why B1–B3 had to be argued from doctrine rather than from a contract:
  there is no contract to cite.
- The R2.0 acceptance register (GT-01…GT-50 per `SIGNOFF.md`) still has **no server twin** for the
  deployed application. Its guards are client oracles against a frozen HTML pin
  (`origin/codex/r2-uat-remediation:release-2/frozen/R2_FROZEN_REFERENCE.html`, md5 `10aafb7a`).
  ⚠️ This is **already a known open item** in
  your own queue — RB-123, *"GT-92 has no server twin"* — so it is corroboration, not a new claim.
- `20_handoff/R2.0_DEFECT_REMEDIATION_HANDOFF.md` — cited by DL-237 and DL-241 — is not in this
  working tree. NOT-MEASURABLE: whether it exists on another branch; git is not run against this
  path by standing rule.

**I am not proposing a resolution.** Under Anti-Assumption the escalation is: *does R2 owe a handoff
contract of the same class R1 has, and if so, is its absence scope or defect?* That is an owner call.
**Note this does not block B1–B3** — those are measured behaviours and stand on their own.

---

# CONCERNS

1. **The good layer is masking the bad one.** The ceremony around resolution is convincing enough
   that a demo will not surface B1–B3; they only appear if you act twice and compare. A pilot user
   *will* hit them, and the failure mode is the one most corrosive to trust: their confirmed work
   comes back as their top priority.
2. **B1 is upstream of the classification questions.** R2, R3 and arguably R4 may all be symptoms of
   the same generation-per-run behaviour. **Fix B1 first and re-measure before spending effort on the
   others** — some may dissolve.
3. **An unidentifiable build cannot be governed.** No version endpoint means no rollback target and no
   way to reproduce this audit against the same artifact. This is cheap to fix and should not wait.
4. **Free-tier capping shaped this audit.** `active_project_limit: 1`, `can_create_project: false` —
   I could not test intake without archiving the owner's demo project. Intake, first-run and the 60s
   promise are therefore **unmeasured**, not passed.

# DEPENDENCIES

- **Owner ruling** on the Escalation above before any further R2.0 production judgment.
- **Engineering** must confirm whether findings carry a stable structural id across runs, and whether
  the deployed severity function is the degenerate one seen in `code/`.
- **The B1 control run** (three re-analyses, zero acts) must be executed before B1 is actioned.
- Retest of intake/first-run requires either a Basic entitlement on the staging account or owner
  permission to archive `DevNorth 2026`.

# NOT MEASURED — stated so absence is not read as a pass

| area | why not |
|---|---|
| **Fast Pass ≤60s / Deep ≤120s target, 180s P95** | No stopwatch was run. Three Extended Analyses completed during the session; none was timed. **No performance claim is made in either direction.** |
| **Intake / first-run / activation** | Blocked by the Free-tier cap of 1 active project (see Concerns 4). |
| **DL-238 injection round-trip (GT-92)** | Not attempted — writing payloads into the owner's staging plan was outside what I judged safe without asking. **The server twin is owed per DL-238 regardless.** |
| **Server-side entitlement enforcement (GT-106/110)** | Not attempted; closer to pen-testing than a UI walk. A paywall asserted in client state is not a paywall — worth a direct endpoint replay. |
| **Offline / failure paths (GT-A3)** | Not exercised. Canon already calls this "the single biggest gap"; expect failures. |
| **Withdraw append-vs-erase (GT-25)** | Control present, behaviour not exercised. |
| **Export, Reports, Grounding map, Your Outcome surfaces** | Not walked. |
| **B1 control run** | See B1 flip condition. |

# RECOMMENDATION

**Do not ship R2.0 to production.** Not because the product is wrong — the doctrine layer is the best
evidence in this report that the design is right — but because the register underneath it does not
hold still, and every user-visible honesty guarantee is downstream of that register.

Ordered:

1. **Run the B1 control** (three re-analyses, zero acts). Cheap, and it either confirms or dissolves
   the headline finding. ⚠️ **Promoted to first 2026-08-29** — the Escalation was demoted when its
   overstated form was retracted; B1 is the finding with the most weight resting on the least
   verification, so it goes first.
2. **Rule on the Escalation** — does R2 owe a handoff contract of the class R1 has? This does not
   block B1–B3, but it decides whether future R2 behaviour can be audited against a contract or must
   keep being argued from doctrine.
3. **Fix stable finding identity** (B1), then **re-measure B2, B3, R2 and R3** before treating them
   as separate work.
4. **Add a build identity surface** — a `/version` endpoint or a visible build stamp.
5. **Reconcile the composite vocabulary** (R1) — one word, one ramp, every surface.
6. **Re-audit with intake in scope** once entitlement allows.

# STATUS

**FAILS — not fit for production.** 3 blocking · 4 reported · 1 escalation · 9 areas unmeasured.
Blocking items B1–B3 share one suspected cause and should be re-measured as a set after it is
addressed.

**Authored by AI as a recommendation under Framework 001. Not ratified. Not a decision record.**
