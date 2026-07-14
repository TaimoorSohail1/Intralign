# DL-111 — Progress panel adopts the owner LOCK foundation-bar (amends D176/D194c/D187/D179d/DL-109 for the Overview panel)

- **Date:** 2026-07-14 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# DL-PENDING — Progress panel adopts the owner LOCK foundation-bar (amends D176/D194c/D187/D179d/DL-109 for this surface)

**Class:** A (owner-directed UX doctrine change) · **Framework 001A** (AI drafts; **owner ratifies**; numbered at land per DL-065)
**Decided by:** Idris (Founder) · **Drafted:** 2026-07-14 · AI implementation, owner ratification owed.

## Decision
The Overview **Progress panel** adopts the owner-provided **"blend / 29-hero" foundation-bar** design (the locked reference `progress_panel_LOCK.html`). The panel now renders: a **hero count of GROUNDED FACTS** (attested + derived, computed), a **proportional foundation bar** whose *Confirmed-by-you* (attested) and *From-OSLO* (derived) segments are sized to the **real counts**, a **set-apart PROVISIONAL inferences tail**, a legend, and **OPEN / CLOSED** work stats with **severity red on Critical**. Deltas (↑/↓) show the change since the last analysis update.

This **supersedes, for this panel only**, the following ratified rules:
- **D176 / D194c** — "no fill, no proportion of a total; the grounded row is a class-ledger sentence." → The bar **is** a proportion, but of a **REAL population** (grounded facts your read is built on), never a completion/health fill toward a target.
- **D187 / D179d** — "no red anywhere in this panel; brand colour on actions/links only; earned-green only." → **Red is permitted on Critical** (severity), and **deltas may carry the accent** as "change since last analysis update."
- **DL-109** — "the inference surface is neutral; no set-apart 'provisional' framing." → Inferences are drawn as a **provisional tail**, visibly set apart from the solid grounded facts.
- **D194d / D197 / D186** — distinct grounded vs load-bearing rows; the load-bearing row is *the* name. → The load-bearing inferences are **folded into the provisional tail**.

Unchanged and still enforced: every number is **COMPUTED from `_progressRows()`** (nothing hard-coded); the hero equals attested+derived; segment widths equal the real counts; class labels are **single-sourced through `epiClassName()`**; **CLOSED is never a target** (no denominator/percentage/"remaining"). These are protected by a new guard, `_assertPgxBarIsComputedFromRealCounts()`.

## Guards to RE-BASE on ratification (currently SUSPENDED, logged by name at boot)
`_assertEveryPayoffCountIsComputed` (payoff-count → replaced by the new PGX guard), `_assertNoHoldingItAnywhere`, `_assertTrendColourIsEarnedOnly`, `_assertNoProgressRowSaysItTwice`, `_assertLoadBearingIsTheOneName`, `_assertThirdEpistemicClassIsRepresentable`, `_assertProgressRowsStayDistinct`, `_assertGroundingRisesWhileIssuesRise`, `_assertClosedIsNeverATarget` (re-checked by the new PGX guard), `_assertRisingInferenceIsNotARegression`.

On ratification these ten are **rewritten to the new doctrine** (e.g., red-permitted-only-on-Critical; grounding-rises proven against the bar's segments; third-party attestation shown as a third solid segment). Until then they are **suspended, not deleted**, and each logs a named `⚠️ PGX` warning at boot so the suspension is never silent.

## Provenance
Owner directive (Idris, 2026-07-14): after being shown a canon-legal typographic adaptation, the owner directed **"I want the original image I provided implemented."** The owner has the authority to amend the panel's doctrine; this record routes that reversal through Framework 001 so the paper trail is honest and the guards are re-based on ratification rather than silently bypassed.

## Supersedes / Amends
Amends **D176, D194c, D187, D179d, DL-109, D194d, D197, D186** *for the Overview Progress panel only*. No other surface (hero maturity ramp, Inference Map, reports) is changed; their guards remain fully in force.

---

## REVISION 2026-07-14 — RECONCILED VARIANT SHIPPED (owner-selected)

After a harmony review against the Outcome Confidence panel, the owner selected the **reconciled** variant (now live). This **narrows** the doctrine reversal:

- **Colour on state is restored to canon.** Orange is once again ACTIONS/LINKS only (D179d) — the hero underline and orange deltas are gone; deltas are neutral. The bar uses a **cool accent on "Confirmed by you"** that deliberately echoes the Confidence ramp's lit band (harmony, not decoration).
- **Red is retained ONLY on Critical** (severity), consistent with the Start Here CRITICAL chip. This is the sole surviving colour reversal of D187, and it is scoped to severity.
- **The inference tail is de-exiled** ("inferences your read leans on" / "Inferred — your read leans on these") — this **re-aligns with DL-109/D177** (inference is not a debt), so the DL-109 reversal is effectively withdrawn; only the *set-apart tail geometry* remains.
- **Still reversed:** the proportional foundation **bar** (D176/D194c) as a proportion of a REAL population; the **merged grounded + load-bearing** rows (D194d/D197/D186); the fixed attested/derived segments in place of the class map (D194c third-class).

Net: of the ten suspended guards, several (`_assertTrendColourIsEarnedOnly` re delta colour, `_assertRisingInferenceIsNotARegression`, `_assertNoDebtVocabulary`-adjacent copy) are now **much closer to passing on their own merits**; on ratification, re-base the remaining reversals (bar geometry, merged rows, red-on-Critical-only) and restore the rest to full force. Live build: **138/138 self-check, 0 pageerrors.**

---

## RATIFIED 2026-07-14 — guards re-based, suspension removed

On ratification the product build was updated to match: the `_PGX_AMEND` suspension scaffold is removed and the ten guards run live. Five were adapted to the bar's markup (payoff-counts-computed, closed-is-never-a-target, grounding-rises-while-issues-rise, rising-inference-is-not-a-regression, no-"holding-it"); the colour guard was replaced by `_assertPgxColourDiscipline()` (severity red scoped to Critical; orange/`--success` forbidden on panel state); `_assertPgxBarStructure()` was added; and four ledger-structure guards (D194a/D197/D194c/D194d) were retired as superseded, their one-home/count-survival concerns covered by `_assertNoCountIsRenderedTwice()` + the two PGX guards. **Third-party attestation as a third bar segment is the one deferred follow-up.** Live self-check: **135/135, 0 pageedrrors**, both themes.
