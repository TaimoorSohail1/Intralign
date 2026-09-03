# Iteration 1 Apparatus Plan — the machinery that makes a two-week cadence survivable

> **Iteration 1: 2026-08-31 → 2026-09-11.** Boundaries **Sep 11 · Sep 25 · Oct 9**.
> **Status: DRAFT · owner-directed, engineering-targeted. Ratifies nothing.** Every governance clause
> here routes Backlog → Proposal → Review → Decision under Framework 001. AI drafts; the owner ratifies.
>
> **Owner direction, 2026-08-31:** *"I'd prefer to attempt to incorporate all of the layers into the
> current sprint. If we fail that's fine, but I'd like engineering to target support for all of the
> layers, specifically for R2.1 freeze and build, and R2.2 design freeze."*
>
> ⚠️ DL-243 §6a–§6g is cited here only because its record now resolves on the control plane. An
> earlier version cited the id while it resolved to nothing, and the citation gate rejected it —
> correctly.
>
> ⚠️ **Release-line artifacts are named here, never linked.** This document lives on the control
> plane (`main`), which by design carries no release line at all — measured 2026-08-31: no
> `CURRENT_RELEASE`, no `release-*` directory. A link from here to a release-line file is therefore
> a broken link by construction, and `doc_integrity_check` is right to reject it. Reach those
> artifacts through `ACTIVE_DESIGN_REF`, the way the tools do.
>
> ⚠️ **This plan is therefore written as a TARGET, not a commitment.** Its success condition is not
> "all five layers land" — it is **"every layer has a named owner, a first increment, and a check that
> tells us whether it moved."** Layers that slip are visible, not silent. That distinction is the whole
> point: the failure this repository keeps measuring is not missing work, it is **work whose absence
> nothing detects.**

---

## §0 — Why apparatus, and why now

The 2026-08-29 R2.0 staging audit cost roughly a full working day and covered **18 of 131** acceptance
criteria — the auditor chose which. On a fixed two-week cadence that is ~10% of every iteration spent
producing evidence that **nobody can re-run and nobody can diff.** Three iterations of that and the
evidence is folklore.

Every gap below shares one shape, already named four times in this repository:

> **skip-as-pass / prove-the-happy-path.** A check that cannot evaluate its subject reports success.

`no_hardcoded_release_line.py` and `report_measurement_check.py` mechanized against it on the
governance side. **The apparatus is the same discipline extended to the release cycle.** Nothing here
is invented; it is the existing rule, made mechanical.

---

## §1 — The five layers

| # | Layer | First increment (iteration 1) | Owner | Serves |
|---|---|---|---|---|
| **L1** | **Freeze-readiness checker** | ✅ **BUILT** — `tools/freeze_readiness_check.py`, 5 checks, self-tested | AI drafted · **Hamza reviews** | R2.1 freeze · R2.2 design freeze |
| **L2** | **GT server-twin backfill** | Sequence + **RED-proof the 53 active twins**; register the B0 twin | **Taimoor** · Hamza accepts | R2.1 **build** · R2.0 defect closure |
| **L3** | **R2 handoff contract** | One contract doc at the seam, R2 vocabulary, replacing the R1-shaped one | **Owner drafts** · Hamza reviews | R2.1 freeze → build |
| **L4** | **Defect lane** | Operational split at the GT register: invariant → governed row; else tracker | **Hamza** defines the tracker half | R2.0 defect fixing |
| **L5** | **Promotion enforcement** | Wire L1 into CI as a **required** check on the design line | **Hamza** | R2.1 freeze · every freeze after |

**These are not five projects.** L1 is the *reader* of the evidence L2–L5 produce. Build L1 first (done),
and each later layer has a place to report into on the day it lands rather than a document to update.

⚠️ **L2 and L4 are ONE mechanism** (owner rulings 4 and 6, 2026-08-30). The GT server twin is at once
the invariant's test, the defect's governed row, and the proof of its fix. **Do not build them twice.**

---

## §2 — L1 · The freeze-readiness checker (BUILT)

`tools/freeze_readiness_check.py` assembles F002 §9.3's promotion evidence by machine.

```
python3 tools/freeze_readiness_check.py            # exit 0 = ready, 1 = not
python3 tools/freeze_readiness_check.py --self-test # RED-proves all five checks
```

**Live reading, 2026-08-31 — MEASURED-BY: `python3 tools/freeze_readiness_check.py` @ `work/release-cycle-2026-08-30`:**

| | §9.3 item | reading |
|---|---|---|
| **F1** | precondition register reads N-of-N | ❌ **no such artifact exists anywhere in the repository** |
| **F2** | build-readiness audit at freeze, zero escalations | ❌ the 2026-08-29 R2.1 freeze audit — **2 blocking** |
| **F3** | state matrix green at the frozen md5 | ✅ 3 journeys at `ba563375`, zero reds |
| **F4** | acceptance register synchronized | ❌ **118** GT ids vs pointer-of-record **s10=120** |
| **F5** | owner freeze declaration naming md5 + tag | ❌ manifest states **NOT FROZEN** |

**→ FREEZE NOT READY: 4 of 5 items not evidenced.**

### ⚠️ §2a — F1 is not a failing check. It is a missing artifact.

**§9.3 requires a "precondition register" and nothing in this repository is one.** The phrase occurs
only in prose — F002, DL-235, the #227 review, and my own gap analysis. **A freeze has never been
evidenced against it, because it has never existed.**

**This needs an owner decision, not an engineering task.** Three options:

1. **Author the register** — one file per line, N rows, each a named precondition with a met/unmet
   state. Cheapest reading, most new surface.
2. **Bind it to an existing artifact** — declare the design line's `QUEUED_WORK` register (or the Refinement Ledger) the
   register and have F1 read its unresolved-row count. No new surface; changes what those files mean.
3. **Amend §9.3** to drop the item, if the other four already carry the evidence it was meant to.

**Recommendation: (2).** The design line's `QUEUED_WORK` register already enumerates open obligations
per line and is already parsed by a checker. **Extend, don't mint.** But this is placement, not
substance — the owner's call.

### §2b — What the checker got wrong before it was handed over

Recorded because the errors are the *subject* of this plan, not incidental to it.

- **It selected the newest audit by filename**, which is a Tier-1 gate audit, not a freeze audit. Five
  of the line's seven audits carry no `▶ RESULT` line at all. **Fixed:** only `*_FREEZE.md` qualifies;
  a line with no freeze audit fails rather than falling back to any audit present.
- **It looked for the acceptance register at `<line>/acceptance/`**, which on the design line holds an
  RB-075 scoring corpus with zero GT ids. The real register is on the **delivery** line. **This is the
  RB-076 / RB-106 / RB-125 cause — checker and subject on different lines.** Fixed: search the line,
  then the delivery line, and **name which one answered**, so the owner can see that the design line
  carries no register of its own.

⚠️ **Both errors would have made the checker fail forever for reasons unrelated to the freeze — which
is how a team learns to bypass a gate.** A checker that is wrong in the failing direction is not "safe".

---

## §3 — L2 · GT server-twin backfill (Taimoor)

**Measured state — MEASURED-BY: `code/ci/r2_guardrails.json` @ `origin/codex/r2-uat-remediation`, 2026-08-30:**
**60 twins registered** (53 active · 7 pending · 9 naming no test) · **61 missing — exactly `GT-58…GT-118`**,
the README's range, because the registry's `contract_path` is Slice 9.

⚠️ **The open question is bigger than the backlog: are the 53 active twins RED-proved?** A twin that has
never failed is not a twin. `test_issue_identity.py` is the measured instance — one test guards
cross-run identity and both fixtures share the default `evidence_refs`, awarding the matcher's +0.15
bonus automatically. **It cannot fail.**

**Iteration 1 increment — in priority order:**

1. **RED-proof the 53 active twins.** Not backfill — *verify what we claim to already have.* Each twin
   runs once against a deliberately violating fixture and must fail. Any that passes is not a twin.
2. **Register the B0 twin** (finding identity), which closes the R2.0 blocker's done-condition.
3. **`gate_r2_guardrails.py` gains a `--self-test`.** Twelve `tools/` checkers have one; it has none.
   ⚠️ **This is due anyway on 2026-09-14** when DL-243 §6b's grace period expires (2026-09-14).
4. **Sequence the 61 missing** — a named count per iteration, not a backlog. At ~15/iteration the
   register is whole by Oct 9.

**Do not attempt all 61 this iteration.** Step 1 is the one that changes what we believe.

---

## §4 — L3 · The R2 handoff contract (owner drafts)

The seam at `20_handoff/` exists and is substantial — 34 files including a 372-line API contract.
**It is R1-shaped:** 29 of 34 files are R1; R2 pillar vocabulary returns **1 hit**.

**So the R2.1 freeze would hand engineering a contract written for a different product.**

**Increment:** one build contract at the seam — proposed name `R2.1_BUILD_CONTRACT` — carrying the R2 vocabulary — the fixed core
(**Intent · Constraints · Scope · Requirements**, DL-240), the two Grounding measures under their two
names (owner ruling R1, 2026-08-22), the maturity read as a read and never a forecast. **Not a rewrite
of the seam** — one contract for one freeze, and the R1 files stay where they are until something needs
them changed.

⚠️ **This is owner work, not engineering work.** It is product definition. Engineering's dependency on
it is real, so it is on the critical path for the R2.1 freeze — but it cannot be delegated.

---

## §5 — L4 · The defect lane (Hamza defines the tracker half)

**Owner ruling 6, 2026-08-30 — two tiers, split at the GT register:**

- **An invariant violation** → a governed row + the failing test from L2. It is a governance object.
- **Everything else** → the engineering tracker. **Not** a governance object.

⚠️ **The tell for leakage is an empty governed lane.** If a month passes with zero governed defect rows,
the split is being applied to avoid governance, not to scope it. **That is a metric, and it should be
read at every freeze.**

**Iteration 1 increment:** Hamza names the tracker (Linear or otherwise) and the field that carries the
GT id, so a governed row and a tracker row can be joined. **Open question the owner has not answered:
which register do governed defect rows live in** — the GT acceptance register, or a defect register of
its own? **Escalated, not assumed** (Anti-Assumption Protocol).

---

## §6 — L5 · Promotion enforcement (Hamza)

**G9: F002 §9.3 is enforced nowhere.** L1 now makes it *runnable*; L5 makes it *binding*.

**Increment:** add `freeze_readiness_check.py` to the doc-integrity workflow on the design line and
mark it **required**. ⚠️ **It will be RED on day one** — 4 of 5 items fail — so it must land as
**advisory-then-required**, with the promotion to required happening the moment F1's owner decision
lands and F2's two blockers clear. **A gate introduced red and left red teaches people to ignore red.**

⚠️ **Do not require the 75-minute app-CI monolith** as part of this (owner ruling 3 / RB-056) — it would
block every open PR. Fast tier required now; full tier after G3 fixes the timeout.

Also L5: **owner holds admin on production and read on every user-facing environment** (ruling 7),
with the environments enumerated. Currently `app.intralign.ai` appears in **zero repo files** and
`vercel.json` hardcodes one Heroku origin — **staging and production cannot differ without a code
change.** That is the mechanical cause of "no build identity" (G7) and it blocks DL-243 §6e.

---

## §7 — Sequencing against the two freezes

**R2.1 freeze and R2.2 design freeze both fall inside or just after this iteration.** The chain has not
started:

> `design/release-2.1` **(does not exist)** → RB-076 → #247 → B2

**Four links, nine working days.** ⚠️ **Hamza has not been told that `ACTIVE_DESIGN_REF = design/release-2.1`
was designated** — F002 §9.1 already specifies the convention; it was simply never instantiated.
**That message is the single highest-leverage thing the owner sends this week**, because every other
layer waits behind a branch that takes minutes to create.

**Standing ruling, unchanged: R2.0 defects OUTRANK the freeze.** If they collide, the freeze slips.
The consequence — that the first freeze under the new cadence may be missed, in the first iteration —
was accepted deliberately. **Recording it here so a missed Sep 11 freeze reads as a known trade, not a
process failure.**

**R2.2 design freeze** is owner-side design work and is not blocked by any of L1–L5. It *is* blocked by
the owner's own time, which L3 also claims. ⚠️ **L3 and R2.2 design compete for the same person** — the
same collision as tracks 1 and 2, one level up.

---

## §8 — The governance move that makes this durable

**Apparatus work becomes a standing iteration obligation** (owner ruling, 2026-08-31): each iteration
names its apparatus increment — which twins move to RED-proved, which manual step becomes a command —
**and the freeze checks it.**

Without this, apparatus is what gets cut when the iteration is tight, every iteration, forever. With it,
"we shipped no apparatus this iteration" is a visible, deliberate decision rather than a default.

**Proposed home: DL-243 §6.** ⚠️ **Do not mint a new framework.** Extend, don't mint.

---

## ▶ What the owner must decide

1. **F1's precondition register** — author it, bind it to the design line's `QUEUED_WORK` register, or amend §9.3. *(Recommend: bind.)*
2. **Where governed defect rows live** — the GT register, or a defect register of its own.
3. **Whether L5 lands advisory-then-required**, and what event promotes it to required.
4. **Whether L3 or R2.2 design gets the owner's hours** when they collide. They will.

---

> **Reminder:** this document is a recommendation and a plan of record for one iteration. It becomes
> canon only via Framework 001 — Backlog → Proposal → **Review** → **Decision** → Change → Changelog —
> and only on owner ratification.
