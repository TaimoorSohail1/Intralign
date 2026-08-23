# DL-239 — The Deep Pass gains a ratified latency target and ceiling — 120s target, 180s P95

- **Date:** 2026-08-23 · **Status:** Ratified · **Decided by:** Idris (R2.0 close-out rulings, 2026-08-22)
- **Class:** A

## Decision

**The Deep Pass gains a ratified latency target and ceiling: 120 s target, 180 s P95 ceiling.**

| | target | ceiling (P95) | source |
|---|---|---|---|
| **Fast Pass** | 45 s | **60 s** | DL-046, ratified |
| **Deep Pass** | **120 s** | **180 s** | this record |

Until now the Deep Pass had **no latency target of any kind**. DL-046's 60 s was the only
owner-approved numeric target in the corpus. **This is the second.**

## ⚠️ This deliberately inverts the process that was proposed

The staging review proposed that engineering answer *"what Deep P95 is achievable at the Tier-1
envelope once DL-105 E1–E3 land?"* and that **their answer would set the ceiling.**

**The owner has instead set the bar first and requires engineering to explain any shortfall.** This is
recorded as a choice, not an oversight, because the reasoning binds future targets too:

**A target derived from what the current implementation happens to achieve is not a target — it is a
description.** It can never exert pressure, because it is defined by the thing it is meant to move.

**The question to engineering therefore changes shape.** It is no longer *"what ceiling should we
set?"* It is now: **"Can you meet 120 / 180 once E1–E3 land — and if not, what is reachable, and
why?"** The burden of explanation sits with the side holding the measurements.

## Why these numbers, and not others

**3× the Fast ceiling, preserving Fast's own 1.5× target-to-ceiling ratio.** The figure is a ratio
against an already-ratified target rather than a guess or a round number.

**Measured baseline at ratification:** 281 s, 287 s, 330 s across three plans, with roughly 480 s
observed on the largest. **180 s therefore demands approximately 45 % off measured P95.**

⚠️ **That is demanding but not arbitrary, and the reason is on the record already.** **DL-103**
specifies the Deep Pass as *"a full re-derivation on every run."* **DL-105** commissioned **E1**
(prompt caching / KV-cache reuse, marked BUILD NOW), **E2** (scoped recompute) and **E3** (evidence
coalescing). **If DL-103's full re-derivation is still what ships, E2 alone should deliver most of the
required reduction** — the optimisation does not need inventing, only landing.

## The rationale that drives the number

Recorded because it is what makes 120 s the target rather than 180 s:

1. **Cost per Deep run gates how freely re-analysis can be triggered.** A cheaper pass lets
   re-analysis fire on more events without depending on batch mode.
2. **A user who acts on a finding should see the result of that action sooner.** Deep latency is felt
   as the delay between doing the work and seeing it land.

⚠️ **This connects directly to the `Deep 2/day` cap in DL-048.** That cap is a fixed integer, and
ratified doctrine says freemium gates **capacity**, never judgment quality. **The cap can only become
cost-derived once per-run spend is measured** — that tension is held on its own backlog row and is
**not** resolved here.

## What this obliges

1. **A QA performance gate for the Deep Pass**, mirroring the one DL-046 already requires for Fast.
   ⚠️ **A target with no gate is a preference.**
2. **Emitted latency at p50/p95 for the Deep Pass**, on the same contractual footing as
   Time-to-First-MRI. **The gate cannot be enforced against numbers nobody emits.**
3. **Over-budget behaviour is defer-and-disclose**, consistent with the Fast Pass contract: return what
   is ready, say plainly what was deferred, never silently truncate and present the result as complete.
4. **The debounce is unchanged.** This record sets a duration bound; it does not alter when analysis
   fires.

## What this does NOT decide

- **It does not relax or move the `Deep 2/day` cap.** That waits on measured per-run spend.
- **It does not rule on the Fast Pass breach.** `≤60 s P95` (DL-046) stands unchanged, and intake copy
  promising "under a minute" stands with it. ⚠️ **Stated flip condition:** if engineering establishes
  that 60 s is unreachable at the Tier-1 envelope, **the copy question returns to the owner** — and not
  before. The measurement forces that, not the inconvenience.
- **It does not price the user's wait.** Whether ~2 minutes is the right experience is a separate
  question from whether the system should be capable of it.

## ⚠️ The number is falsifiable, and that is intended

If engineering answers that 120 / 180 is unreachable at the Tier-1 envelope with E1–E3 landed, **this
record is amended rather than quietly missed.** A target that is revised on evidence stays a target; a
target that is silently breached becomes a description of whatever the build does.
