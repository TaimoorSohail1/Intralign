# DL-118 — Overview surface roles (governing boundary model) + Start-here charter extension: guidance ranks confirmations alongside issues

- **Date:** 2026-07-16 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# DL-PENDING — Overview surface roles (governing boundary model) + Start-here charter extension: guidance ranks confirmations alongside issues

**Class:** A (information architecture + guidance charter) · **Framework 001A** (AI drafts; **owner ratifies**; numbered at land per DL-065)
**Decided by:** Idris (Founder) · **Drafted:** 2026-07-16 · Grill record: **Enhancement #8** (intermediate release). Reference: `overview-role-model.html`.

## Problem
The Overview's **Progress** panel visibly overlaps the **Outcome Confidence** panel (grounded/inferred framing, "critical / limiting dimension", "since last analysis" deltas). The instinct to fix it by making Progress action-led would violate **D183g** ("Start here is GUIDANCE; Progress is STATE") — it would push an action into the panel doctrinally forbidden to own one. The overlap is **presentation bleed**, not a missing role: the four surfaces have distinct jobs; several just echo each other's framing, and the most *actionable* insight (load-bearing confirmations) has no doctrinally valid home today.

## Decision (recommended — owner ratifies)
**1. Ratify the four-surface role model as the governing boundary reference.** Each Overview surface answers exactly one question and owns exactly one thing; the model names what each must **never** say, so future work fixes boundaries rather than shuffling content:
- **Outcome Confidence — the READ (judgment).** Owns the band, CAF dimensions, limiter, one-word reliability qualifier, band trend. Never: a number/score (D183b), a global count (D179e), severity colour (D175), the grounding ledger.
- **Start here — the NEXT MOVE (guidance).** Owns the single most consequential thing to do now. Never: a tally (D179e — a pointer, not a number), the full list, "where you stand".
- **Understanding dependencies — BLOCKED ON OTHERS.** Owns the reads awaiting a third party. Never: severity colour (D003), a task/issue list.
- **Progress — WHERE YOU STAND (state).** Owns the grounding ledger (Confirmed-by-you vs From-OSLO — the star), the statement decomposition, the load-bearing **count**, the open/closed counts (their one home), the count deltas. Never: a burndown / "issues → 0" (D180), a completion forecast, a next-move/action (D183g — that's Start here), the read's judgment (Confidence).

**2. Extend the Start-here charter: guidance ranks load-bearing confirmations alongside open issues.** A load-bearing confirmation ("confirm the inferred statement that holds up your read") is a *"consequential item that could keep you from the outcome"* — Start-here's own charter — so it belongs in guidance, not Progress. Realized **issue-first** (a PM's problem-first mental model): the top item is the most-severe open issue, and **each issue carries its de-risking load-bearing confirmation attached** ("confirm this assumption first — it may dissolve the issue"), computed from the statement's `.sup` link to the issue. Standalone confirmations (hold up the limiter under no open issue) list below. Load-bearing is the **connective thread** — Progress reports it (state), Start here acts on it (guidance), Confidence is what it moves (read); it is never any single panel's headline.

**3. Progress echo-cleanup (scoped follow-up, same decision).** Progress leans into its state identity (the grounding ledger + the load-bearing *fact*) and drops the echoes of the read's framing; the load-bearing **action** now lives in Start here. No count leaves its one home (D179e).

## Conformance basis (no ratified invariant is weakened)
Every boundary is an existing rule made explicit: **D183g** (guidance vs state), **D179e** (counts one home = Progress), **D180** (Progress is grounding not clearing), **D175** (the hero card is neutral; severity colour is legitimate on Start here / Attention, which are not the hero), **D003** (waiting is not a severity), **D183b/D002/D051/D186c** (the read's elements). The Start-here extension is a **realization of D183g's own charter** ("the most consequential item"), not a new policy that overrides it.

## Guards (executable — `window._S10`)
Existing guards hold at **145/145, 0 pageerrors** after the Start-here build: `countsHaveOneHome` (D179e — the focus carries no tally), `d183OverviewOrder` (D183g — guidance/state ordering), the hero-neutrality suite (D175) unchanged. The `renderFocus` rewrite is proven to render the attached de-risk confirmation from real `.sup` state and to emit no count.

## Governance
Route via `dl-land` (owner ratifies; numbered at land per DL-065). The role model is proposed as a **canonical governing reference** for the Overview surfaces; the Start-here charter extension is a guidance realization proposed for ratification. Slice-3 (Overview) reopened; re-signoff required. AI recommends; only the owner ratifies.

## Provenance
Owner flagged Progress↔Confidence duplication (2026-07-16); critical analysis produced the four-surface role model; owner directed considering Start-here before evolving Progress, then ratified the model, chose issue-first ("better CX for project owners"), and approved the attach-to-issue pattern via mock. Built into slice-10 `renderFocus` + verified (145/145). AI implemented; owner ratifies.

## Scope boundary (explicitly NOT here)
- The **Progress echo-cleanup** — same decision, **BUILT + verified** (2026-07-16): the load-bearing line reports the fact and no longer restates the read's judgment ("Critical issue or the limiting dimension" removed); guards 145/145 (`loadBearingComputed` · `noDebtFrame` · `loadBearingHonestSubset` · `countsHaveOneHome` green).
- The **Confidence architecture** call (composite vs roll-up) — a separate decision (`DECISION-PACKET-outcome-confidence-architecture.md`): keep the composite for adoption, revisit at a tripwire.

### Sources
- Doctrine: **D183g** (Start here = guidance; Progress = state), **D179e** (counts one home), **D180** (grounding not clearing), **D175** (hero neutrality; severity belongs to issues/Attention), **D003** (waiting not a severity).
- Prototype: `oslo-product-output/vertical-slices/slice-10-tiering-limits/prototype.html` — `renderFocus` (unified guidance), `_ciLoadBearingStatements`/`_ciActiveSup` (the `.sup` linkage). Reference: `overview-role-model.html`.
