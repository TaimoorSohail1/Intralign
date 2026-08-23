# DL-238 — A read that can execute the plan is not a read

- **Date:** 2026-08-23 · **Status:** Ratified · **Decided by:** Idris (ratified 2026-08-19; record landed 2026-08-22)
- **Class:** A

## What this record does

**It records a ruling the owner already made.** On **2026-08-19** the owner ratified this doctrine anchor
together with GT-92's **DURABLE** tier. The ratification is recorded on GT-92's entry in
`release-2/acceptance/README.md`, which states it in those words:

> **Doctrine anchor — RATIFIED (owner, 2026-08-19):** *a read that can execute the plan is not a read.*

**Nothing new is decided here.** This record exists because the ratification had no numbered decision, and
a ruling that only lives in a guard's register entry is not reachable by anything that reads the decision
log.

⚠️ **Why it is three days late, stated rather than hidden.** The record could not be minted: `dl-land`
numbered off a counter that read one decision home on a `main` that was 79 numbers behind the corpus, so
a dispatch would have re-issued **DL-157**, an id already in use. Minting one by hand instead is precisely
the defect **RB-099** is made of, so the draft was held unnumbered and the blocker tracked as **RB-125**.
The numbering guard landed on `main` on 2026-08-22 and this record is the first thing it unblocks.

## The anchor

**A read that can execute the plan is not a read.**

The honesty doctrine says **OSLO advises; the user decides**. A plan that can run code in the reader's
session has taken a decision the reader never made — silently, at render time, without ever presenting
itself as a choice.

⚠️ **The anchor generalises past injection.** It is not a statement about escaping, or about HTML, or
about any particular payload. **It binds any case where READING a plan causes something to happen.**
Injection is the instance that raised it; the invariant is the class.

## Decision

1. **Text a user or their document supplies is rendered as TEXT** — on every surface, in every context —
   and **survives verbatim**. A fix that trades an injection for data loss is not a fix.
2. **The guarantee is asserted on node PRESENCE, never on execution.** ⚠️ This is measured, not stylistic:
   the original probe rendered into a **detached** element, so its zero execution count was never the
   reassurance it read as. **An invariant that depends on where the probe rendered is not an invariant.**
3. **Exemptions are a declared registry with asserted arity, not a list.** Widening the exemption turns
   the suite **red** rather than quietly growing.
4. **The anchor binds beyond rendering.** Any future capability where reading causes an effect is governed
   by this record, whether or not markup is involved.

## Tier — DURABLE

**Ratified DURABLE (owner, 2026-08-19)**, following the **DL-230** precedent that tiering is an owner
call. The invariant is not about R2's surfaces; it is about the relationship between user-supplied text
and rendered output, which every release line inherits.

⚠️ **The usual objection to DURABLE is answered by the guard's own shape, and that is why it was ratified
rather than hedged.** DURABLE binds future lines retroactively, so a future feature that legitimately
renders user-authored formatting would ordinarily be blocked by a *never markup* invariant. **It is not
blocked**, because the declared passthrough registry is a **legal path through** the guard. **The tier
binds the invariant without freezing the product** — that property is what made DURABLE safe to ratify,
and it is recorded because it is the reasoning, not the conclusion, that a future reader will need.

## Scope note — the review that raised this saw a minority of it

⚠️ The four typed paths named in the review that surfaced the defect are **not** the exposure. In
production the plan-derived fields come from the user's **own uploaded document** and are user-controlled
too — `it.title` alone appeared at **43 sites, escaped at zero of them**. **A fix confined to typed inputs
would not have been closure**, and this is recorded so the scope is not re-narrowed later by someone
reading only the originating review.

## What this record does NOT do

- **It does not close RB-122.** The client escaping is a **reference oracle**; the obligation is that the
  **server** encodes at render. That server twin is owed and tracked separately (**RB-123**).
- **It does not assert the guard is complete.** GT-92 was RED-proven 21 ways, one wrap removed at a time,
  and that proof **found four defects in its own probe plus one uncovered site — none of which were found
  by reading it.** The guard is trustworthy because it was made to fail, not because it is green.
- **It does not settle where the invariant is enforced.** Client-side assertion is where the oracle lives,
  not where the guarantee belongs — the same argument this repository already makes about **GT-104**: a
  paywall asserted in client state is not a paywall.
