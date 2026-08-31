# DL-242 — Narration may not assert what the mechanism does not enforce

- **Date:** 2026-08-24 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

## Decision

**A product surface may not assert in prose what its mechanism does not make true.**

**Where prose and mechanism disagree, the mechanism is the fact and the prose is the defect** — the
prose is corrected or deleted. ⚠️ **The mechanism is never bent to make the prose true**, unless that
is ruled separately and on its own merits.

**This is the product-side twin of a rule this project already operates on the build side** —
*a check that cannot fail is not a check*, *a gate that passes by not running is a broken gate*. Those
govern CI. Nothing governed the same failure on the surface the user reads. ⚠️ **It is a promotion of
an operating rule, not a new invention.**

## Why now — two instances in one day, in one review

**⚠️ Second instance is the whole justification.** Both were found on 2026-08-23 while diagnosing the
R2.0 defect handoff, and neither was caught by any guard.

**1 · The artifact `read:` line asserts provenance it cannot maintain.**
Every planning artifact carries a hardcoded prose read rendered as **"OSLO's read:"** directly above
the live per-item provenance chips, in the same card. **Thirteen of those strings assert provenance**
(*"the success metrics are still OSLO's inference"*, *"Owners inferred"*, *"one confirmed, one OSLO
inferred"*). ⚠️ **Nothing anywhere assigns `.read`** — it is fixture text for the life of the session.

Resolving the `metricset` issue flips **every** inferred goal, success criterion and KPI to
`prov:'you'`. So one user action turns every chip in the card to **"✓ yours"** while the line above
them keeps saying the metrics are OSLO's inference. **The product contradicts itself, inside one card,
about the same statements, on its honesty claim.**

**2 · The first-run freeze promises a lock that was deliberately not built.**
The copy reads *"Ground two decisions to open the full workspace · 0 of 2"*. Measured: the freeze class
is applied **only on the read view**, and the masthead outcome bar is **explicitly exempted** from the
dimming. Navigating away lifts it — **by design**, and the code comment records why: without the
escape the rail card and the crumbs are both `pointer-events:none` and **the user is trapped**.

⚠️ **The reported defect and the design intent are the same behaviour.** The freeze is a focus device
on one view. It was never an access gate, and the handoff's own "what must not be lost" list is right
to call it **non-coercive** — that is the point of it. **The copy is the only thing that was wrong.**

## What is ratified

| | ruling |
|---|---|
| **§1** | **Narration asserts no provenance.** Provenance is carried **per item**, on the item, where it is live and already guarded. ⚠️ **An artifact's prose read describes shape and completeness only.** |
| **§2** | **A first-run focus device is not an access gate, and may not be described as one.** Copy may not promise that anything opens, unlocks or is withheld unless the mechanism withholds it. |
| **§3** | **Where prose and mechanism disagree, correct the prose.** ⚠️ Making the mechanism match a promise is a separate decision requiring its own ratification — and for the freeze it is **rejected**: it would reintroduce the dead-end the escape hatch exists to fix, and convert a non-coercive nudge into a coercive one. |

## ⚠️ Why the cheaper option was chosen over the better-sounding one

**§1 could have been satisfied by DERIVING the read from the live items** — recomputing the provenance
clause on every render so it can never go stale. **That was considered and rejected.**

**Deriving makes a second source of truth honest. Deleting removes it.** The chip is already correct,
already per-statement, and already covered. ⚠️ **This file had THREE provenance sources when it should
have had one**; the fix that ends with two is not the fix. Deriving would also put generated prose on
a customer-facing honesty surface, which needs its own guard and its own review — **cost incurred to
preserve a sentence.**

⚠️ **Not every clause was derivable in any case.** *"most are OSLO's reconstruction from scattered
notes"* has no field behind it at all.

## Ripple

1. **`20_handoff/R2.0_DEFECT_REMEDIATION_HANDOFF.md` §4** — item 3.5 splits. **3.5a** (the provenance
   contradiction) is **ruled and buildable**. **3.5b** (the original two-surface report) remains **NOT
   ESTABLISHED** and is gated on a one-minute production observation. ⚠️ **3.5a's ruling does not close
   3.5b.** The freeze-copy item is likewise ruled.
2. **Two guards are owed**, and neither exists — **zero current guards assert prose-against-mechanism**:
   - *the artifact read asserts no provenance* — a prohibition, so it is cheap and it survives;
   - *first-run copy promises no lock the freeze does not apply*.
   ⚠️ **Until the guards land, §1 and §2 are asserted and not enforced — which is this decision's own
   failure mode.**
3. **`DL-237` (numeric confidence never serialized) and `DL-238` (a read that can execute the plan is
   not a read) are the same doctrine applied to other surfaces.** This record generalizes them; it does
   not amend them.
4. ⚠️ **Neither instance was found by a guard.** Both were found by reading source during a defect
   diagnosis. **That is the gap this record exists to close**, and it should be assumed there are more.

## Class

**Altering** (F002 §3) — it changes a displayed judgment. ⚠️ **The class was disputable for the
freeze-copy item**, since behaviour does not change; it is Altering under §3's rule that **a disputed
class is Altering until ruled otherwise**. **Each instance rides its own gated PR (§7).**
