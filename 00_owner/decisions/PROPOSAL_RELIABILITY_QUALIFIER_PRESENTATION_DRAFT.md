# PROPOSAL — Reliability Qualifier Presentation Simplification (Single Quiet-by-Default State)

> **DRAFT for owner ratification (Framework 001).** AI-drafted at owner direction; AI analyzes/recommends, the **owner ratifies**. Route: Backlog → **Proposal (this)** → Review → Decision → Change → Changelog. This is a **presentation-doctrine** proposal — it governs how the Reliability qualifier is *shown to users*. It introduces **no** new epistemic object, changes **no** invariant, and alters **no** engine behavior. The three-component Reliability model (Coverage · Evidence availability · Assessability) and its independence from CAF are **preserved unchanged**.

- **Date:** 2026-07-10 · **Status:** Proposed (owner direction 2026-07-10) · **Class:** A (Reliability presentation / doctrine orientation; non-doctrinal — meaning unchanged)
- **Layer:** Presentation posture — touches Confidence Interpretation Doctrine surface + Visual/UX spec (Overview/MRI Reliability rendering). **Non-structural.**
- **Grounded in:** `OUTCOME_CONFIDENCE_INTERPRETATION_DOCTRINE_001` (read with basis; band + CAF + reliability), Reliability Model V1 (Coverage · Evidence availability · Assessability), Confidence Model CONF-06, `PROPOSAL_CONFIDENCE_INDEX_CALIBRATION_DRAFT` §5 composition invariants (Monotonic in CAF; Reliability qualifies, never inflates; Independence), DL-065 (user-facing Confidence presentation posture — number focal, never bare, band is the unit of magnitude), DL-043 (advisory-only). Companion to `PROPOSAL_CONFIDENCE_PROGRESS_PRESENTATION_DRAFT` (this refines the *reliability* leg of "never bare").

## Problem

Owner intent (2026-07-10): **simplify the scoring surface for the user.** Target users (pragmatic PMs) should read one focal number with a plain reason — not reconcile a lattice of sub-scores.

Today the score has, in principle, up to six moving parts a user could be exposed to: three CAF dimensions (Clarity · Alignment · Feasibility) and three Reliability components (Coverage · Evidence availability · Assessability). DL-065 already makes the **Confidence index** focal and collapses CAF behind a "how this is calculated" affordance. The **Reliability leg has not received the same treatment**: "never bare" currently requires a reliability qualifier alongside every value, but the doctrine does not yet specify *how much* of the three-component structure the user sees, or *when* it should draw attention.

Two failure modes if left unspecified:
- **Over-exposure** — surfacing Coverage / Evidence availability / Assessability as three standing readouts re-introduces the multi-score complexity DL-065 set out to remove, and invites users to add or average them.
- **Under-signaling** — hiding reliability entirely would silence the **false-confidence guard** (high CAF on low reliability), which is the single most important thing reliability exists to say.

The tension the owner raised — *should Reliability collapse into Clarity to simplify?* — is resolved **not** by merging constructs (that destroys the guard and breaches the Independence invariant) but by simplifying the **presentation** of an unchanged model.

## Proposal

Adopt a **single-state Reliability presentation**: the three internal components compose into **one user-facing "read-solidity" qualifier** that is **quiet by default and loud only on divergence.**

**1 — One qualifier, not three.** The user sees a single reliability state (e.g., *Solid read* / *Partial read* / *Thin read*, copy TBD at ratification), derived from the three components. Coverage · Evidence availability · Assessability remain the internal computation and remain visible **only** on demand, behind the existing "how this is calculated" affordance. The user is never asked to read, add, or reconcile the three.

**2 — Quiet by default.** When reliability is adequate and **consistent with CAF**, the qualifier is a subtle, low-emphasis badge attached to the focal number. It does not compete with the index or the cause annotation.

**3 — Loud on divergence (the guard speaks).** When a **high CAF band sits on low reliability**, the qualifier becomes prominent and carries the plain-language false-confidence message ("this reads strong, but on thin evidence — treat as provisional"). Prominence is **triggered by divergence, not shown continuously.** This is the existing false-confidence flag (Reliability Model V1 / CONF-06), rendered as the *only* time reliability foregrounds itself.

**4 — Qualifies, never a second score.** The reliability state is rendered as a **qualifier of the one number**, never as its own competing numeric. It can hold the index down and flag it; it never appears as a rival figure the PM tracks separately.

## Why this is on-doctrine (and invariant-safe)

| Move | Canon basis |
|---|---|
| Three components collapse to one *displayed* state | Presentation-only; internal Reliability Model V1 (three components) unchanged |
| Components still computed independently of CAF | **Independence** invariant preserved — this touches display, not computation (`CALIBRATION_DRAFT` §5) |
| Low reliability can foreground and hold the index down | **Reliability qualifies, never inflates** invariant preserved (`CALIBRATION_DRAFT` §5) |
| Reliability never rendered as a second number | DL-065 — "work-ledger never restates the signal as a second number"; band is the unit of magnitude |
| Number + band focal; reliability quiet unless it diverges | DL-065 (number focal, never bare) + Interpretation Doctrine ("read with basis") — "never bare" is satisfied by the single qualifier |
| Full three-component detail on demand | Interpretation Doctrine "read with basis" — basis remains inspectable via "how this is calculated" |

Critically, this proposal **does not merge Reliability into Clarity or CAF.** Clarity remains a first-order *finding about the plan*; Reliability remains a *qualifier about the assessment*, computed independently. Merging would collapse "clear plan" and "couldn't see enough to tell" into one figure and **eliminate the false-confidence state** — expressly forbidden by the Independence and "qualifies-never-inflates" invariants. Simplification is achieved at the surface only.

## Conditions (binding if ratified)

1. **One displayed state.** The three Reliability components are never surfaced as three standing readouts; they compose into a single user-facing qualifier. Full component detail is available **only** on demand via "how this is calculated."
2. **Quiet by default.** When reliability is adequate and consistent with CAF, the qualifier is low-emphasis and does not compete with the index or its cause annotation.
3. **Loud on divergence.** High-CAF-on-low-reliability (the false-confidence case) makes the qualifier prominent and carries the plain-language provisional message. Prominence is divergence-triggered, not continuous.
4. **Never a second number.** The reliability state is a qualifier of the one index; it is never rendered as a competing numeric, ring, or bar the PM could add to the index.
5. **Never bare, still honored.** Every index value and movement still ships with band + this reliability qualifier + cause (DL-065). The qualifier *is* the reliability leg of "never bare."
6. **Model unchanged.** No change to the Reliability Model V1 components, the Independence invariant, the "qualifies-never-inflates" invariant, or the false-confidence flag logic. Computation is untouched; only rendering changes.
7. **Neutral ramp retained.** The reliability qualifier uses the neutral (non health-color) treatment except where the false-confidence flag intentionally draws attention; it is not styled as project health-red.

## Concerns

- **Threshold ownership.** "Adequate / consistent with CAF" vs. "diverged" is a display threshold. It must trace to the same divergence condition the false-confidence flag already uses (CONF-06); it must **not** introduce a new, separately-tuned threshold. Recommend the Review confirm the trigger is the existing flag, not a new one.
- **Copy risk.** A three-into-one label ("Solid / Partial / Thin read" or similar) must not imply probability or project health. Copy review needed, consistent with the Interpretation Doctrine's anti-probability-misread posture.
- **Loss-of-nuance perception.** Advanced users may want the three components; mitigated by on-demand disclosure (Condition 1), but worth confirming the affordance is discoverable.
- **Divergence-only prominence.** If the flag under-triggers, a thin read could stay quiet when it shouldn't. This is inherited from the existing flag's calibration, not created here, but the Review should note the dependency.

## Recommendation

**Accept-in-substance with Conditions 1–7.** It delivers the owner's simplification goal — one focal number, one plain reason, one quiet qualifier — while leaving the epistemic model, its invariants, and the false-confidence guard fully intact. It is the reliability-leg companion to the already-ratified DL-065 posture and requires no doctrine edit: it lands as a **Confidence/Reliability-presentation addendum** (Interpretation Doctrine surface + Visual/UX spec) with a Changelog record. No structural change; no new invariant.

## Anti-Assumption note

This proposal deliberately does **not** resolve the "merge Reliability into Clarity" question by merging — that would be a structural/ontology change and is out of scope here. If the owner wishes to actually restructure the constructs (not simplify their presentation), that is a separate, doctrine-level change requiring its own proposal and must not be inferred from this one.

## Provenance

Owner direction 2026-07-10: simplify the scoring method for the user. AI analyzed the CAF/Reliability separation, confirmed the Independence and "qualifies-never-inflates" invariants make construct-merging unsafe, and recommended surface-layer simplification (single quiet-by-default qualifier, loud on divergence) as the on-doctrine path. AI drafted, mapped to canon, and surfaced the threshold-ownership and copy risks (Framework 001A — analysis / conflict identification / recommendation). The **owner ratifies.**
