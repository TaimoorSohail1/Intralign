# Proposal — Reconcile CAF-dimension bands to the ratified DL-086 5-band scheme (supersedes DL-097) — RB-039

- **Status:** Proposed — awaiting owner decision (Framework 001 · Review complete, Decision pending)
- **Class:** A (canonical definition — reconciliation). **Presentation; no scoring, model, contract, or doctrine change.**
- **Backlog:** RB-039 (this proposal)
- **Author (analysis/recommendation only):** AI contributor under Framework 001A / DL-033. **AI does not ratify.**
- **Owner decision:** required to adopt, reject, or amend.
- **Supersedes:** **DL-097** (the 4-band CAF-dimension vocabulary) and its RB-038 outcome.

> Governance note: this corrects a conflict. `DL-PENDING-caf-dimension-band-reconcile` carries the ratifiable decision text; spec/prototype edits are realization landed with the decision.

---

## 1. Problem

**DL-097** (2026-07-09) adopted a 4-band CAF-dimension vocabulary — **Limited · Forming · Solid · Strong** — on the stated premise that canon did not fix a per-dimension band vocabulary. **That premise was wrong.** **DL-086** (2026-07-02) had already ratified the v0 CAF/Confidence scoring formula (`30_engineering/scoring/CAF_CONFIDENCE_V0_SCORING_FORMULA_V1.md`), in which:

- each CAF dimension (Clarity / Alignment / Feasibility) computes to a **0–100 score** (§1), and
- the authoritative band unit is a ratified **5-band scheme — Very Low 0–34 · Low 35–49 · Moderate 50–74 · High 75–89 · Very High 90–100** (§3, with the ±3 band-edge guard), which the formula already applies to dimension scores ("caps the dimension at 45 = low band").

So DL-097 introduced a **conflicting second vocabulary** on the same 0–100 dimension score, and its "band→score thresholds" open item can't be resolved without choosing one scheme. (DL-097's analysis read the CAF Assessment Model and Confidence Model — which explicitly *exclude* scoring/bands — and missed the scoring formula spec where the bands actually live.)

## 2. Proposed change (one decision)

**CAF dimensions use the ratified DL-086 5-band scheme** — **Very Low · Low · Moderate · High · Very High** — the same authoritative band unit as the Confidence index. **DL-097's 4-band vocabulary is superseded and retired.**

## 3. Framework 001A Review

**Findings.**
- Resolves the conflict by adopting the **single already-ratified and calibrated** scheme; there are **no new thresholds** to set — DL-086's 50/75 edges + ±3 guard already band the per-dimension 0–100 score.
- **Lowers cognitive load** (the goal of the Overview redesign): Confidence and its three dimensions read on **one shared ramp**, so "Feasibility is Very Low → Confidence is only Moderate" is legible at a glance instead of forcing the user to learn two band vocabularies.
- The 5-band is doctrine-compliant **maturity** (DL-086; Visual §1.2 neutral ramp, never red/green health), so extending it to dimensions preserves the maturity framing.

**Concerns.**
- **C1 — the "forming" warmth is not lost.** "Understanding is forming" is the confidence **stage** (Orientation → Expanded → Validated, CONF-05), separate from the band, and is unchanged.
- **C2 — minimal spec change.** The v0 formula §3 already uses the 5-band words for dimensions informally; this makes it explicit. The amber "limit" flag on the weakest dimension still draws attention without health-coloring.
- **C3 — presentation-only.** DL-086's formula, scoring, and calibration are unchanged.

**Dependencies.**

| Artifact | Zone | Impact | Action |
|---|---|---|---|
| `DL-097` (4-band vocabulary) | 00_owner | **SUPERSEDE** | Retired by this decision |
| `CAF_CONFIDENCE_V0_SCORING_FORMULA_V1 §3` | 30_engineering/scoring | **CONFIRM** | Dimension bands = the 5-band scheme (already implied) |
| `CANONICAL_GLOSSARY` | 00_owner | **CHECK — none** | DL-097's band entry was never added; nothing to remove |
| Overview/Confidence presentation + v4 prototype | 10_product/experience, product-design | **MED** | Relabel dimensions Strong/Forming/Limited → the 5-band words |
| CAF band→score thresholds (DL-097 open item) | — | **CLOSED** | Dissolved — DL-086 already sets the edges |

**Recommendation.** Adopt. Clean conflict resolution, no calibration debt, and it serves the redesign's low-cognitive-load intent. **This closes the DL-097 threshold open item outright** (DL-086 owns the edges).

**Status.** Proposed — Review complete; **owner Decision pending.** Not ratified; not canon.
