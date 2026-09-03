# OBLIGATION — N-4: the governed act path has no failure treatment (R8)

**Status:** OPEN
**Fix:** TaimoorSohail1 *(assigned by owner 2026-09-02 — product/engine defect lane)*
**Accepts:** idris-manley
**Class:** R2.0 production blocker · production-gating subset, Tier 3 · **partial** — substance passes, presentation fails
**Raised:** 2026-08-29/31 staging fitness audit — §R8
**Criterion:** **N-4** — *every round-trip has a failure path*. Subset state: **⚠️ partial.**
**Invariants:** **GT-A1** (working does not read as done) — **holds.** **GT-A3** (failure treatment) — **half-built.**
**New invariant:** **GT-120** — *no governed act surfaces a raw exception; every act path states whether the record changed* · **id minted by owner ruling 2026-09-02 (R2.0-6); oracle authored with the fix.**

## 1 · What was measured

MEASURED-BY: `window.fetch = () => Promise.reject(new TypeError('Failed to fetch'))`, then driving each
surface and diffing `document.body.innerText` line-sets before/after @ `/projects/8ae4e3a5-…/issues`,
2026-08-31. Client-side only; nothing was sent to the server.

| surface, network down | result |
|---|---|
| **OSLO chat** | ✅ **designed** — *"OSLO could not answer right now. **Your project data is unchanged.**"* |
| **Issue card render** | ✅ no defect — opens fully offline |
| **A governed act (confirm + basis)** | ⚠️ **split verdict** |

**On the governed act — substance passes:** the act did not report success. Settled held at *2 of 29*, the
open count held at 27, nothing claimed RECORDED.
**Presentation fails:** the only thing shown to the user is the raw JavaScript exception string
**`Failed to fetch`** — no explanation, no retry, and none of the reassurance the chat surface gives.

## 2 · Why this is blocking for production

The governed act is where the user's attestation is created. A raw exception string at exactly that moment
tells the user nothing about the one thing a governed product must make certain: **whether their record
changed.** The chat surface already answers it — *"your project data is unchanged"* — and the act path,
which needs the reassurance far more, does not.

⚠️ **The substance being correct is what makes this fixable and narrow, not what makes it acceptable.** A
user who cannot tell a failed act from a recorded one will re-act, and re-attestation on an append-only
record is not free.

## 3 · Cause and current state

**One surface already has the right treatment.** The pattern is designed, implemented and observed working
on chat; the act path simply does not inherit it. This is a propagation gap, not a design gap.

⚠️ **Three claims were withdrawn from the original test and are recorded rather than deleted** — a click
that never registered, a regex that could not match *"could not"*, and a `/Confirm/` false positive from
the resolved tray. **The surviving finding is the one that reproduced against an online control.**

## 4 · DONE CONDITION

On the deployed build carrying the fix, each result reported with the command or observation that
produced it:

1. **The act path renders a designed failure**, naming what happened and stating explicitly that the
   record is unchanged.
2. **A retry exists** and is reachable without losing the basis the user already selected.
3. **No raw exception text reaches any user-facing surface** on any governed act — measured by driving
   every act kind (confirm · flag · route) with `fetch` rejected, and diffing the line-sets.
4. **The online control runs first**, so a surface that fails for an unrelated reason is separable from
   one failing for this one.
5. **GT-A3 goes red when the treatment is removed.** Half-built is not provable; the twin must bite.

## 5 · Notes

Scope is the **act** path specifically. Read-only surfaces already pass and should not be re-worked here.

⚠️ Related but **not** in this row: `/outcome` renders **"↑ weakened this session"** — an up arrow labelled
*weakened*. That is R7 and belongs to **N-8**, because the surface it misleads is the stakeholder-facing
one. Filed there so neither row closes the other by accident.
