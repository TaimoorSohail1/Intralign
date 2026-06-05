# Phase VI — Wave E: Disclose Surfaces (Presentation)

**Sequence:** Last. · **Status:** Not started · **Owner gate:** required before Release 1 production readiness.
**Contracts:** `IC/QA/OBS-WE-DISCLOSE` (`03_architecture/contracts/WAVE_E_CONTRACT_PACKAGES_DISCLOSE_SURFACES.md`).

## Goal
Present everything the prior phases produced — **epistemically safely**. Disclose is a **consumer** (presents, never generates); **Render** is its non-cognitive service. Every surface labels uncertainty (Attested/Derived + confidence band + conflict) and shows both current understanding and its history. This is the user-facing layer of Release 1.

## Scope (surfaces, per ratified UX specs)
- **MRI** (umbrella), **Finding Panel** & **Recommendation Panel** (RP-C1: Recommendation Panel only in Finding context), **Issue Cards**, **Project Overview**, **Understanding Companion** (routes via Finding — Option B), **Notification/Awareness**, **History/Timeline**, **Export/Share-out**.

## Depends on
Phases II–V (there is nothing to disclose until the cognition + acceptance records exist).

## Expected outcomes (definition of done)
- ✅ Each surface presents the governed objects it owns and **traces** to its ratified UX spec.
- ✅ Every surface labels **epistemic state** (Attested vs Derived), the **confidence band**, and any **conflict** — Derived is never shown as settled (negative tests enforce; band-edge guard applied).
- ✅ **Recommendation Panel renders only in a Finding context** (RP-C1) — enforced in Disclose (presentation), not duplicated as a cognition rule.
- ✅ Plan facts display as **user-attested** (distinct from evidence-attested and OSLO-self-attested).
- ✅ Both **current foreground** and **history/timeline** are presented; history is append-only in presentation.
- ✅ **Export** packages existing understanding only, carrying epistemic labels; exposure = epistemic-safety labeling (no Authority gate in R1).
- ✅ Disclose **generates nothing** and **changes no assessment** (negative tests); Render performs no cognition.

## Invariants enforced
Disclose presents (consumer, not producer); Render = service; epistemic-safety labeling everywhere; RP-C1; stale-never-current; history append-only; export packages existing understanding only; no Authority.

## Testing focus
Presentation negatives + E2E (Playwright/Cypress): reject Derived-as-settled, overstated confidence, RP-C1 violation, acceptance-by-Disclose, unsourced export. Visual/interaction coverage of the surfaces.

## Exit gate (owner-approved — Release 1 feature-complete)
All surfaces present the cognition chain + acceptance with enforced epistemic-safety labeling and current+history views; Disclose proven to generate nothing and change no assessment. → Release 1 ready for production-readiness review (production deploy remains owner-only).
