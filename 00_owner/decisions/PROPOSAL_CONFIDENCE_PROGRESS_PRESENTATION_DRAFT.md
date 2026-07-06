# PROPOSAL — User-Facing Confidence Movement & Quantified Progress Presentation

> **DRAFT for owner ratification (Framework 001).** AI-drafted at owner direction; AI analyzes/recommends, the **owner ratifies**. Route: Backlog → **Proposal (this)** → Review → Decision → Change → Changelog. This is a **presentation-doctrine** proposal — it governs how the Confidence signal and progress are *shown to users*. It introduces **no** new epistemic object, invariant, or engine behavior.

- **Date:** 2026-07-01 · **Status:** Proposed (owner direction 2026-07-01) · **Class:** A (Confidence presentation / doctrine orientation)
- **Layer:** Presentation posture — touches Confidence Interpretation Doctrine surface + Visual/UX spec. **Non-structural.**
- **Grounded in:** `OUTCOME_CONFIDENCE_INTERPRETATION_DOCTRINE_001` (change is cause-based; read with basis; expected to evolve; not probability/health), `06_confidence_understanding_model`, `OPEN_TBD_REGISTER` D1 (bounded-equivalence ±7 / same-band; exact index calibration-pending), DL-043 (advisory-only).

## Problem

Target users (pragmatic PMs) discount progress they cannot quantify. A purely qualitative Confidence presentation (bands only) is read as un-serious, and — critically — **a displayed number that does not move when the user acts reads as broken** and erodes trust in the whole signal. Owner design principle (2026-07-01): *do not show a dial you won't let move; if a number is on screen, causes must be reflected in effects.*

Simultaneously, the Confidence Interpretation Doctrine warns that a naked confidence number invites misreading as **probability/health**, that values **below band granularity are noise** (±7 tolerance, D1), and that a number users are trained to push *up* creates pressure against **honest decreases** (Confidence may fall as understanding improves).

## Proposal

Adopt a **two-track progress presentation** that satisfies the pragmatic-PM need for quantification while holding the Confidence Doctrine:

**Track 1 — Confidence signal (moves, but governed).** The user-facing Confidence index **moves on-screen** in response to cause, under four binding conditions:

1. **Cause-bound** — every movement is annotated with *why* ("rose because you resolved the critical Resources gap — a Feasibility/CAF change; reliability unchanged"). Never a bare delta. This *is* the doctrine's "change is cause-based" requirement and the owner's "causes reflected in effects" requirement — they converge.
2. **Both directions, honestly** — the number can **fall** (e.g., after Extended/Deep Analysis surfaces something real), and the UI frames a fall as improved *understanding*, not a worsening project.
3. **Never bare** — always rendered with its **band** (Very Low…Very High) and its **reliability** qualifier.
4. **Magnitude is calibrated, not caveated** — direction + cause are real now; the exact index value is **owner-TBD until calibration (D1)**, after which the number ships **clean** (per Condition 2). The **named band** remains the authoritative unit of magnitude, and movements below band granularity are treated as noise.

**Track 2 — Quantified work-ledger (fully countable, always safe).** Alongside the signal, surface a persistent readout of **concrete governed objects** the PM can audit: findings resolved/open by severity, evidence/dependencies confirmed, plan-section coverage, reanalysis runs. These are legitimately measurable (they are counts of attested objects, not an epistemic signal) and give PMs hard, un-caveated numbers to track improvement — *or its absence*.

## Why this is on-doctrine

| Move | Canon basis |
|---|---|
| Number moves only with a stated cause | Interpretation Doctrine — "change is cause-based"; "read with basis" |
| Number can fall; fall framed as better understanding | Interpretation Doctrine — "Confidence may decrease as understanding improves" |
| Band + reliability always shown; band is the unit of magnitude | Interpretation Doctrine — "not a midpoint on a probability scale"; read with CAF + reliability |
| Exact index labelled illustrative / calibration-pending | OPEN_TBD D1 (±7 / same-band; index owner-TBD) |
| Quantify findings/evidence/coverage, not the signal itself | Countable governed objects sit outside the Confidence Doctrine's scope |

## Conditions (binding if ratified)

1. Confidence is **never displayed as a bare number** — band + reliability + cause accompany every value and every movement.
2. **No permanent on-screen caveat.** The production UI shows the number **clean** — it does **not** print "illustrative." Honesty is preserved by *behaviour*: never shown bare (band + reliability + cause always present), a subtle **"how this is calculated"** affordance, and sub-band jitter (within the ±7 / same-band tolerance, D1) is **not** animated or celebrated as a change. Any temporary "calibration-pending" cue, if shown before D1 calibration lands, is explicitly removed on calibration. (The word "illustrative" in the prototype denotes *demo data*, a mockup artifact only.)
3. The presentation must make **downward movement legible and non-alarming** (both-directions honesty); it must not be styled as failure/health-red.
4. **No gamification** — no points, streaks, badges, or "score to beat"; the number is a reading, not a reward.
5. Confidence and CAF retain the **neutral (non health-color) ramp**; only *findings* carry severity color.
6. The **work-ledger counts only attested/governed objects**; it never restates the Confidence signal as a second number.
7. On calibration (D1) landing, the illustrative label is revisited by the owner.

## Concerns

- **Precision creep** — a visible moving number may still be over-read as probability; mitigated by Conditions 1–2 and the mandatory cause annotation, but worth owner attention in copy review.
- **Downside legibility** — the honest-decrease requirement (Condition 3) is the fragile part; if users experience a fall as punishment, engagement suffers. Recommend user-testing the fall case specifically.
- **Two-number confusion** — index vs. work-ledger counts must be visually distinct so PMs don't add them; the prototype separates them (ring/band vs. a labelled "Progress" strip).

## Recommendation

**Accept-in-substance with Conditions 1–7.** It resolves a real adoption risk (pragmatic PMs) without breaching the Confidence Doctrine: the number moves *because* the doctrine already requires cause-based change, and the un-caveated quantification is redirected onto countable objects where it is honest. Owner ratifies; on ratification it lands as a Confidence-presentation addendum (Interpretation Doctrine surface + Visual/UX spec) with a Changelog record. Prototype (`oslo_r1_experience_mockup_v2.html`) demonstrates the posture illustratively (non-canon) for evaluation.

## Provenance

Owner direction 2026-07-01: pragmatic PMs need quantifiable *and* qualifiable progress, and a displayed confidence number must move with cause to be credible. AI drafted, mapped to canon, and surfaced the probability-misread / sub-band-noise / honest-decrease risks and the two-track resolution (Framework 001A — analysis / conflict identification / recommendation). The **owner ratifies.**
