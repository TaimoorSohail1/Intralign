# DL-121 — Start-here charter extension: the lead issue's Confirm acts on its load-bearing assumption inline; Review opens the issue

- **Date:** 2026-07-17 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# DL-PENDING — Start-here charter extension: the lead issue's Confirm ACTS on its load-bearing assumption inline; Review opens the issue

**Class:** A (guidance-charter realization) · **Framework 001A** (AI drafts realization; **owner ratifies**; numbered at land per DL-065)
**Decided by:** Idris (Founder) · **Drafted:** 2026-07-17 · **Extends:** DL-118 (Overview surface roles + Start-here charter). Grill record: intermediate-release track, folds into R1 per **DL-120**.

## Problem
DL-118 established that Start here ranks a de-risking **load-bearing confirmation** alongside each issue ("confirm the assumption that holds up your read — it may dissolve the issue"). But in the realization, the lead issue's **Confirm** button and its **Review the issue** link both routed to the same screen (`openIssue`). The two affordances were indistinguishable in behavior, so "Confirm" did not confirm — it was a second "open the issue" button. The differentiation DL-118 promised (act on the assumption vs. understand the issue) was not delivered.

## Decision
**Confirm and Review are two distinct jobs, and the realization must make them behave differently:**

**1. Confirm ACTS — inline, on the one assumption.** The lead issue's Confirm opens an inline attest step (*"Confirm the assumption — on what basis?"*). Attesting the **load-bearing statement** (the inferred statement whose `.sup` names this issue) firms the read at the issue's root; because the issue exists *because* that assumption is unconfirmed, the analysis update then resolves it. The user never leaves Start here — the panel advances to the next issue, and the outcome lands on the state surfaces (Progress counts, the read, History).

**2. Review OPENS — the full issue workspace** (all context, evidence, options, recommendation). Unchanged: `openIssue`. It is the deep dive, distinct from Confirm's shortcut.

**3. Standalone confirmations are POINTERS, not inline acts.** A load-bearing statement that holds up the read under **no open issue** has nothing to resolve — confirming it only firms the read, and the confirming happens on the Inference map. So its affordance is a **link** ("Confirm on the map →"), styled and labelled like Review — never a solid action button that masquerades as the lead's inline Confirm. (A full inline attest for standalone statements is **deferred**: it requires statement-scoped *withdrawable* attestation, which D191 makes mandatory and which the issue-scoped machinery does not yet provide.)

## Conformance basis (no ratified invariant is weakened)
The inline Confirm **reuses the existing guarded resolution engine** rather than hand-rolling state, so every guard that protects issue resolution protects it:
- **D191** — the attestation ("Confirmed by you") is **withdrawable**; the inline Confirm creates the same `_decision` record as a fix/answer, so the existing withdrawal path applies unchanged.
- **D088** — **only the analysis update resolves** the issue; Confirm attests → the read updates → the issue moves Addressed → Resolved. Start here shows "Confirmed — updating the read…" in between; it never hand-sets Resolved.
- **D173b** — the **payoff is computed from state** (the band/counts move because the evidence moved).
- **D179e** — counts stay in Progress (Start here carries no tally); **D183g** — Start here is guidance and *owns the next move*, so an action living here is doctrinally correct (it is the charter's own "most consequential item to do now").

## Scope boundary (explicitly NOT here)
- The **outcome notification** — the episodic "the read firmed" ping — is **deferred to Enhancement #4** (the notification router awaits owner commission, D179a: state outranks event). Today the payoff is the Overview payoff strip + Start here advancing + a History entry; the routed *ping* arrives when the router is commissioned.
- The **standalone inline confirm** (attest-and-firm with a withdrawal affordance) — deferred to the attestation-model pass.

## Guards (executable — `window._S10`)
Boot self-check holds at **145/145, 0 pageerrors**, both themes — **and after driving the full click flow** (Confirm → pick basis → confirm): the critical issue resolves, the critical count moves 1→0, the next issue promotes, and boot is still 145/145. `countsHaveOneHome` (D179e), the hero-neutrality suite (D175), `d183OverviewOrder` (D183g), and the attestation/withdrawal guards (D191) are green.

## Governance
Route via `dl-land` (owner ratifies; numbered at land per DL-065). A **realization of DL-118's charter**, not a new policy — Confirm-acts-inline is the charter's "act on the consequential item" made real. Slice-3 / slice-10 (Overview / Start here) reopened; re-signoff required. AI implemented; only the owner ratifies.

## Provenance
Owner reviewed the Start-here Confirm affordance (2026-07-17) and observed that Confirm and Review routed identically — "it's unclear how the confirm button offers a differentiated experience." Diagnosis confirmed both called `openIssue`. Inline-Confirm-with-payoff mocked, reviewed (basis-required attest; payoff computed, not scripted), and built into slice-10 `renderFocus` + `applyFix(id,{inline})`, verified 145/145 before and after the interaction. Standalone confirms relabeled as map pointers. AI implemented; owner ratifies.

### Sources
- Doctrine: **DL-118** (Start-here charter), **D183g** (guidance owns the next move), **D191** (withdrawable attestation), **D088** (only the analysis update resolves), **D173b** (computed payoff), **D179e** (counts one home), **D179a** (state outranks event).
- Prototype: `oslo-product-output/vertical-slices/slice-10-tiering-limits/prototype.html` — `renderFocus` (`startInlineConfirm` / `confirmLeadAssumption` / the addressed-lead transient), `applyFix(id, opts)` (the `inline` path).
