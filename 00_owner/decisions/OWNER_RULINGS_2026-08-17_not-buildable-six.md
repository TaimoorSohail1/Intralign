<!-- GRADUATED, NOT RE-AUTHORED -->

> **Graduated to the control plane 2026-09-02.** This file was ratified on 2026-08-17 and has lived only
> on the R2.1 design line. **The body below is copied byte-for-byte; nothing was re-written.**
>
> **Source:** `design/release-2.1:release-2.1/OWNER_RULINGS_2026-08-17_not-buildable-six.md`
> **MEASURED-BY:** `git show <ref>:<path> | md5sum` across every local and remote-tracking ref —
> **32 refs carry it, all identical at `f0b4d250`.**
> **CONTROL:** a ref that does not carry the file returns the md5 of empty input (`d41d8cd9…`), which is
> *absent*, not *different* — so the agreement above is a real agreement and not an artifact of the probe.
>
> ⚠️ **Deliberately NOT claimed:** that this is the only copy, or that it is identical on refs no longer
> present. DL-214's graduation header asserted "identical across every ref carrying it" and was wrong —
> one ref held a version with a `## Graduation ripple` the others lacked. This header states what was
> measured and stops there.
>
> **Why now:** #220's plan-write contract cites **R8** as its commission, and a main-based canon PR
> cannot cite a record that exists only on the design line. C-2 governs: **graduate, never reconstruct.**

---

# Owner rulings — 2026-08-17: the six not-buildable capabilities

**Ratified by the owner (Idris) 2026-08-17**, on the evidence in
`PROPOSAL_six-not-buildable-capabilities.md`. AI framed and evidenced; the owner ruled. This file
**records** the rulings; it does not implement them. Continues R6 (Monday scope) and the A2/B2/C1/C2
rulings for capability #12.

⚠️ **These rulings COMMISSION work rather than descope it.** Three of the four add build scope to R2.1.
The consequence for the freeze is stated in §5 and is the most important thing in this file.

---

## R7 — #19 trade-off detection: **BUILD real detection before freeze**

**Ruled.** The Tier-1 honesty floor is an R2.1 obligation. R2.1 will not ship with a scripted trade-off
standing in for detection.

**Why this was a doctrine question, not a scope question.** The capability register classes #19 as the
Tier-1 honesty floor and ties it to DR-7: freemium gates **capacity**, never **judgment quality**, so
surfacing a real weakness in the primary outcome is free on every tier. Today the DevNorth sample
hard-codes **one** trade-off as authored content — a static `sponsor-tradeoff` entry against the `scope`
artifact plus the `noSoundWhileUnsurfacedPrimaryTradeoff` guard. It demonstrates the doctrine; it
detects nothing. On any customer plan, zero trade-offs are found — not because none exist, but because
nothing looks.

**What this commits to, and neither may be inferred:**

1. **The requirement spec must be authored.** `OSLO_R2_TIER1_HONESTY_FLOOR_REQUIREMENT_DRAFT` (expected under `release-2/`; extension omitted deliberately — see the note at the foot of this file)
   is **cited by the register and does not exist** on any of the three live refs. (Scope honesty: that
   is "absent from the three corpora scanned", not "never existed anywhere".)
2. **A DL-210 amendment via Framework 001.** The trade-off finding carries no `structuralTarget`, so its
   dimension cannot be derived without violating GT-46. Adding one amends ratified CAF-boundary canon —
   proposal → review → owner ratifies → PR → `doc-integrity`. **Explicitly not a hotfix.**

**Also owed, from the register's own FUTURE WORK note:** plan-specific boundary generation rather than
one hardcoded string; structured boundary modelling rather than a free-text blob; re-analysis on save so
a tighter line ripples to dependent artifacts; validation that the drawn boundary actually resolves the
tension rather than declaring it resolved; and provenance of the boundary decision in the ledger (#2).

**This is now the long pole for the R2.1 freeze.**

---

## R8 — #6 + #5: **COMMISSION the plan-write API contract**

**Ruled.** R2.1 ships a product that can write to a plan. One contract covers all four `_writeSpecs()`
mechanisms — `proposal` · `planfix` · `checkpoint` · `viabuild` — and **#5's clarification loop
registers as a fifth**.

**The gap being closed:** there is no API contract for **any** plan write. Verified: nothing in
`20_handoff/interfaces/` describes a plan-write endpoint. The path exists only as client function names,
while the server twins for GT-75/81/88 require the server to **reject an undeclared write** — which
cannot be implemented while nothing declares what a declared write looks like.

**Three defects the contract must resolve, not merely document:**

- *"Select an option"* writes an **identical line for two opposite options** on `buffer` (measured).
- *"Write my own"* deep-links to a document rather than to the statement being changed.
- **Reversal is asserted and nowhere designed** — `wifi` has a declared write with no reversal branch,
  so withdrawing leaves the line in the plan, against slice 02 AC-4.

**The contract must specify, per mechanism:** endpoint, payload shape, validation, conflict handling,
reversal semantics, and provenance recording.

**Why #5 rides along rather than being ruled separately:** its defining behaviour — an answer that
changes a plan value — *is* a plan write. Ruled apart, the same decision gets made twice. Its
question-generation and answer-interpretation contracts, and its currently **zero guard coverage**,
remain owed on top of the write mechanism.

---

## R9 — #11: **SPLIT — persistence in, projects-home out**

**Ruled.** Commission durable state; descope the multi-project surface.

**In scope:** durable per-user and per-plan state, so work survives a reload. This is what the **five
slices already asserting cross-session durability** actually depend on — `onboarded`, `everUnlocked`,
`_ocDisclosed`, survey eligibility, A/B assignment. Today state is in-memory and resets on reload, so
all five are currently asserting against something that does not exist.

**Out of scope:** the projects home, the projects list, and load/save across multiple plans.

**Owed either way:** the live `openDoor('projects')` surface ships and toasts *"stubbed."* It must be
removed or must state honestly that multi-project is not in this release. A shipped surface that says
"stubbed" is the product telling the user about its own backlog.

**Note:** the A2 ruling made Axis 2 `(principal, plan)`-keyed, so the multi-plan case is **expressible**
in the identity model. That is not the same as built, and this ruling does not build it.

---

## R10 — #23: the two open follow-ons are **owed as a framed decision**

**Ruled.** The owner will rule the baseline and the scope; they are to be framed with evidence first,
and **neither may be inferred**.

**Context:** #23 is closer to buildable than the audit implied. The capability register **already carries
the ratified definition verbatim** — *"'engaged' = a MILESTONE (≥ half the load-bearing read grounded OR
integrity up ≥1 band; config default 1/2), NOT a click count; plus a durable per-user 'onboarded' flag."*
Its (a)/(b)/(c) requirements are specific.

**The two open items:**

1. **Baseline** — "rose ≥1 level" *from what*? First-ever analysis, or re-baselined after a pass that
   lowers the band (which would let a user re-earn "engaged" repeatedly)?
2. **Scope** — the signal must be durable **per user**, but the predicate computes **per plan**. A user
   with three plans has no defined value: engaged-if-any, engaged-if-all, or engaged-on-the-first?

Item 2 interacts with **R9** — what persistence stores determines what can be asked.

**Blocked on R1's corrective as well:** Slice 8 L5 still reads *"an act past unlock"* and was never
amended. Held under RB-106 with the other five correctives.

---

## R11 — "start" is **fixed at first analysis and never moves**

**Ruled**, on the evidence in `PROPOSAL_engaged-baseline-and-scope.md`. The band a plan first read at is
the reference forever. A band that falls and recovers has **not** risen from start.

**Worked case that decided it:** first read Developing → reanalysis drops to Fragile → user works it back
to Developing. That is **not** a rise; the milestone does not fire.

**Why:** it cannot be gamed, it stores one value written once, and *"you are where you began"* stays a
true statement about the plan. Re-baselining would give a user whose plan degraded an easier path to the
milestone than one whose plan held steady — the signal would partly measure recovery from a dip rather
than value experienced — and the reference would only be knowable by replaying history.

⚠️ **Accepted cost, to be honoured in copy:** a user can do substantial real work and see no milestone,
and can end up further from it than when they started. **No prompt may imply they lost progress they had
earned.** The milestone is once-ever, so this only affects users who have not yet earned it.

⚠️ **Build requirement this creates:** nothing currently stores a starting band. Verified — all 15
matches for `baseline` in the prototype are CSS `align-items:baseline`; there is no `START_BAND`,
`_startBand`, `bandAtStart` or `firstRead`. **Record the band at first analysis, once, per plan.**
This lands in R9's persistence scope.

## R12 — engaged is **per-user, engaged-if-any**, and records which plan earned it

**Ruled.** The first plan to satisfy the predicate flips the user's durable flag **once, forever**.

**Worked case:** a user with a worked Plan A (passes) and a brand-new Plan B (fails) **is engaged** when
she opens Plan B. She sees no beginner coaching there, the survey does not re-fire, and she is counted
once in the funnel.

**Why:** all three consumers are person-level — #18 fires once per user with dismissal honoured
cross-session forever, #23 requires a returning engaged user never to re-see a first-run prompt, and
#15's `funnel_engaged` counts users. Only the predicate was per-plan. Engaged-if-all would mean a user
becomes *less* engaged by starting a second plan.

**Required clause:** the durable record stores **the flag, the plan that earned it, and when**. The
milestone must be auditable against the plan that produced it rather than trusted as a bare boolean —
a flag with no referent is the stand-in shape this line keeps paying for.

**Not settled by this ruling:** the guidance-prompt question for an experienced user on a brand-new plan
is handled by the separate, already-ratified **`onboarded`** flag (*"completed first-run once, ever"*),
which is a different fact from value-experienced. #23's requirement (c) — real cadence config replacing
the demo constants `SV_NUDGE_TTL` 45s / `SV_NUDGE_SNOOZE` 120s / `SV_NUDGE_MAX` 3 / `COACH_MAX` 2 —
remains owed.

**R10 is now discharged.** #23 is no longer blocked on definition; it is blocked on R1's corrective
landing, which is held under RB-106.

---

## #25 — NOT RULED, deliberately

The audit's grounds for calling #25 unbuildable **failed verification**. Its decision record
(`DL-214_FINDING_ORDERING_HONESTY_AND_DEPENDENCY_MODEL`), its build spec
(`BUILD_SPEC_DL-214_finding-dependency-frontier`) and its twelve-scenario acceptance suite
(`BACKLOG_RB-047_finding-dependency-frontier-model`) **all exist**, on `r2/altering-dl218-band-floor`.
The Tier-2 reviewers read the design line and concluded "does not exist."

**That is the same defect RB-094 names** — *"the index and its corpus are on DIFFERENT branches"* — and
the one RB-099 avoided by measuring across all three corpora.

**Ruling #25 as a scope matter would record a scope decision for a merge problem.** It is held pending
the branch question, alongside RB-106.

---

## §5 — What these rulings do to the freeze, stated plainly

**Three of the four commission work. The R2.1 freeze is further away than it was this morning, not
closer.** That is a legitimate outcome of ruling on evidence, but it should not be discovered later.

⚠️ **RB-100's trigger no longer expresses "ready to freeze."** Its five predicates watch capability #12
and Tier-1 findings 1–3. **None of them watches #19, the plan-write contract, or persistence** — so as
written, the freeze could arm while three commissioned capabilities are unbuilt.

**Owed:** a queue row per commissioned item, each with a machine-checkable trigger on its own artifact,
and a corresponding extension of RB-100's predicate list once those artifacts are named. Deferring that
wiring would leave the register asserting readiness it has not measured — the defect this whole line
exists to prevent.

**Not yet wired**, because the artifact paths do not exist yet and inventing them would be the same
stand-in error. The rows are proposed in the accompanying register change.

---

*Recorded under Framework 001A. AI framed and evidenced; the owner ruled. No gap was resolved by
inference, and two of the audit's grounds were corrected by measurement.*

---

## Note on the citations in this file

Four filenames above are written **without their `.md` extension, deliberately**. Each is cited to
record that the file is **absent from this line** — `OSLO_R2_TIER1_HONESTY_FLOOR_REQUIREMENT_DRAFT`
because it does not exist at all (that is R7's finding), and the three DL-214 / RB-047 artifacts because
they live on `r2/altering-dl218-band-floor` (that is why #25 is not ruled).

Written as full paths, `doc_integrity_check.py` reports each as a **broken link** and fails the build —
which it did, four times, on the first run of this file. The checker cannot distinguish *"citing a file
as evidence of its absence"* from *"linking to a file that should be there"*. Both look identical to it.

That is a real limitation rather than a formatting nuisance: it means **a governance document cannot
name a missing artifact by its true path**, which is exactly what an escalation about a missing artifact
needs to do. Recorded here rather than worked around silently; worth a backlog row if it recurs.

*(This is the third cross-track citation hazard today. The first two were PR #218 citing a release-line
path from `main`, and the session handoff citing a canon path from the release line.)*

---

## Graduation ripple

- **Main-canon documents touched:** none rewritten. This file becomes the control-plane home of rulings
  **R7 … R12** so that main-based PRs can cite them. The design-line copy at
  `release-2.1/OWNER_RULINGS_2026-08-17_not-buildable-six.md` remains where it is and is unchanged.
- **What this unblocks:** **#220** may now cite **R8** (*"COMMISSION the plan-write API contract"*) from
  `main`. **R7** (*"#19 trade-off detection: BUILD real detection before freeze"*) also becomes citable —
  it is listed as outstanding owner/dev-lead work and its text had the same reachability problem.
- **Amends / extends an earlier decision:** neither. **A graduation changes a record's LOCATION, never its
  content or its authority.** These rulings were ratified 2026-08-17 and are unchanged by this move.
- **Not rippled:** the R7 amendment and the §B `structuralTarget` ruling remain open owner/dev-lead work.
  Making R7 *citable* is not the same as *deciding* it, and this file does not pretend otherwise.
