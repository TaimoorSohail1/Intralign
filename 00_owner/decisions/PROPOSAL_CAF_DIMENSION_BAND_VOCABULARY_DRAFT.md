# Proposal — Canonical CAF-dimension maturity band vocabulary (RB-038)

- **Status:** Proposed — awaiting owner decision (Framework 001 · Review complete, Decision pending)
- **Class:** A (canonical definition — glossary addition). **Vocabulary/presentation; no scoring, model, contract, or doctrine change.**
- **Backlog:** RB-038 (this proposal)
- **Author (analysis/recommendation only):** AI contributor under Framework 001A / DL-033. **AI does not ratify.**
- **Owner decision:** required to adopt, reject, or amend.
- **Resolves:** the open item in **DL-096** (Overview redesign) — the placeholder CAF band words.

> Governance note: analysis + recommendation routed through Framework 001. No canonical artifact is changed by this document; the `DL-PENDING-caf-dimension-band-vocabulary` record carries the ratifiable decision text, and the glossary/spec edits are realization landed with the decision.

---

## 1. Problem

The CAF Assessment Model and Confidence Model define **CAF** (Clarity · Alignment · Feasibility) and the **Confidence bands** (Low / Moderate / High), but canon does **not** fix a **per-dimension** band vocabulary — the words a user reads for each dimension (e.g. Feasibility "Limited"). The Release-1 prototype used ad-hoc terms (`Limited` / `Forming`), and DL-096 adopted the Overview redesign with these as **placeholders**, explicitly deferring the canonical vocabulary to an owner decision (Anti-Assumption Protocol). Without a ratified set, the build has no source of truth for the per-dimension labels.

## 2. Proposed change (one decision)

Adopt a canonical **four-step CAF-dimension maturity band vocabulary**, ordered low→high, applied to each CAF dimension (Clarity, Alignment, Feasibility):

**Limited · Forming · Solid · Strong**

Add it to the `CANONICAL_GLOSSARY` as a canonical definition; reference it in the CAF Assessment Model and the Overview/Confidence presentation specs. This is the same kind of ratified-vocabulary decision as the DL-087 user-facing-label entries — it names how a computed assessment is *presented*, not how it is *computed*.

## 3. Framework 001A Review

**Findings.**
- Canon defines CAF and the Confidence bands but leaves the per-dimension band words unfixed; the prototype filled the gap ad-hoc. Ratifying a set removes the gap and gives the build a source of truth.
- The chosen ramp keeps the prototype's existing `Limited` / `Forming` and adds `Solid` / `Strong`, so it is a minimal, backward-compatible extension.
- It is a **maturity** ramp (understanding maturity), consistent with Visual Design §1.2 (neutral maturity, never red/green health), and reads distinctly from the overall Confidence band.

**Concerns.**
- **C1 — thresholds are a separate calibration item (OPEN, anti-assumption).** This ratifies the four **band names and their order**, NOT the numeric CAF-score cutoffs that map a dimension's score to a band. Those thresholds are owner/calibration-TBD and must not be assumed here.
- **C2 — keep the axes distinct.** The CAF-dimension band (an input's maturity) must not be conflated with: the **Confidence band** (Low/Moderate/High — the consolidated output), the **Understanding State** (AE-04: Initial→Partial→Refined→Validated→Mature), or the **MRI Understanding States** (MRI-03). This decision names one axis only and does not merge or alter the others.
- **C3 — presentation-only.** CAF-01 already produces the per-dimension assessments; this names the presentation bands. No scoring, model, or contract change.

**Dependencies.**

| Artifact | Zone | Impact | Action |
|---|---|---|---|
| `CANONICAL_GLOSSARY` | 00_owner | **HARD** | Add the canonical CAF-dimension band set (Limited · Forming · Solid · Strong) |
| `CAF_ASSESSMENT_MODEL_V1` | 10_product/domain | **MED** | Reference the band vocabulary (presentation of the assessment) |
| Overview / Confidence presentation specs | 10_product/experience | **MED** | Use the ratified bands per dimension |
| CAF scoring / calibration | 10_product, calibration | **OPEN** | Band→score thresholds — separate owner/calibration decision (C1) |

**Recommendation.** Adopt. It resolves the DL-096 open item, extends the prototype's existing terms minimally, stays on the neutral maturity ramp, and keeps the assessment logic untouched. **Ratify the vocabulary now; treat the band→score thresholds as a separate calibration item (C1) — do not assume them.**

**Status.** Proposed — Review complete; **owner Decision pending.** Not ratified; not canon.
