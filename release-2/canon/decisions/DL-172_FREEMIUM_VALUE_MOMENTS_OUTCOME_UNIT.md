# DL-172 — Freemium value moments & the unit of value: the OUTCOME (R2, freemium-only)

- **Date:** 2026-08-04 · **Status:** Ratified · **Decided by:** Idris (Founder Console) · **Class:** A (identity — the unit of value)
- **Framework 001** — AI drafts; only the owner ratifies.
- **Basis:** this session's alignment memo (`release-2/FREEMIUM_VALUE_MOMENTS_ALIGNMENT_DRAFT.md`) + validation pass (`release-2/R2_FREEMIUM_VALIDATION.md`, verdict: holds together, 20/20 `_S10` green). Grounded in `oslo-product-output/analysis-cost-basis-and-tier-rederivation.md` and **DL-158** (outcome-forward positioning).
- **Extends:** DL-158 (from messaging into the pricing unit). **Supersedes:** the implicit "**project** as the user-facing unit" → **outcome**; the surfaced "**monthly analyses** limit" → analyses are a **fair-use ceiling, not a product limit** (confirming the tier-rederivation); the prototype's "**Basic 10 seats**" → seats tight below Team.
- **Placement:** staged in `release-2/` (R2 copy-of-record); withheld from `main` until R1 graduation. R1/Alpha canon (≤DL-156) untouched.

---

## Decision

1. **Unit of value = the OUTCOME.** Extends DL-158. "1 outcome" is a **scope** unit — how many outcomes you can actively work — **never a success verdict** (D003/D183b hold: maturity ≠ health; no forecast/probability).

2. **Cardinality.** **Free = 1 outcome : 1 plan, kept NARROW (1 active outcome).** **Basic = multiple outcomes per plan AND multiple plans.** The **outcome** is a first-class metered object; the **plan** is its container (1:1 at Free, 1:N at Basic+).

3. **Archive.** Free keeps **one active outcome** + **non-destructive archive/reactivate** to rotate the active slot; the archived outcome's **record stays fully viewable** (canon never meters the record). The at-cap moment is an honest **choice — "archive to switch" (free) OR "keep both active" (paid)** — never a hard wall.

4. **Freemium value moments (Alpha = intent-capture only, NON-GATING).** **VM-1a** (add a 2nd outcome), **VM-1b** (start a 2nd plan), **VM-2** (intake envelope — too many/too-large files). Each is a **mirror** that names the *capability* and **measures intent**; it never delivers a paid tier, never blocks, and never meters the record, the reviewer/CRR loop, or Viewers.

5. **R2 build scope = FREEMIUM ONLY.** No paid-tier **capability** is built in R2. **POST-R2** (documented to map the landscape the walls point toward, not built): VM-3 continuous monitoring (Pro) · auto-import + two-way sync (Basic) · CM-1 seated collaborator + CM-2 enforced governance (Team) · roll-up/portfolio (Enterprise).

6. **NEUTRAL paid-tier copy.** It is premature to list paid tiers or pricing. **No paid-tier name or price appears in user-facing copy** ("a paid capability we're exploring"; "Paid plans — Coming; nothing for sale yet") until the owner decides otherwise. Internal telemetry may tag the tier a signal maps to; users never see it.

7. **Execution-handoff ladder (mapped; only rung 1 is R2).** Export a file = **Free** (a non-wall) · auto-import + two-way sync = **Basic** (connect & mirror) · continuous monitoring = **Pro** (interpret & watch). Rule: Basic *connects and mirrors*; Pro *interprets*.

8. **Collaboration = a Free→Team axis** (skips Basic). The **viral primitives — unlimited Viewers, free Reviewers/CRR, @mention comments — are free forever and never walled** (the growth engine). Seated collaborators + enforced governance are **Team** (post-R2).

## Doctrine preserved (unchanged)
Never tier judgment quality (one accuracy bar for all) · the record is never metered · the reviewer/CRR loop is free · no forecast/verdict (D003/D183b) · confirm/flag symmetry (D133) · "OSLO advises; you decide" · nothing gated in Alpha.

## Realized + validated
Built into `oslo-prototype-r2.html` this session (unit reframe, archive/reactivate, VM-1a/1b/2 intent-capture, neutral copy, `_S10` extended to 20). Validation pass: **holds together across personas**; one friction (VM-2 mis-timing) found + fixed in-pass. 20/20 `_S10`, verify_regress green, 0 JS errors.

## Affected artifacts
`FREEMIUM_VALUE_MOMENTS_ALIGNMENT_DRAFT.md` (now ratified by this DL) · `R2_FREEMIUM_VALIDATION.md` · `oslo-prototype-r2.html` · `R2_FREEMIUM_COMPLETION_CHECKLIST.md`. Feeds a Class-B build/implementation DL (real intent-telemetry persistence; the paid capabilities when their rungs activate).
