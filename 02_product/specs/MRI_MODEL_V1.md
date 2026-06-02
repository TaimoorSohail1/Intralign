# MRI Model v1 — MRI Visualization Model

**Document:** MRI_MODEL_V1.md
**Status:** Specification of the **MRI Visualization Model** (founder-approved positions formalized)
**Consumes (authoritative, unmodified):** `CAF_ASSESSMENT_MODEL_V1.md` · `CAF_SCORING_MODEL_V1.md` · `RELIABILITY_MODEL_V1.md` · `CONFIDENCE_MODEL_V1.md`
**Date:** 2026-05-31

> ## ℹ Repositioned under the MRI umbrella (per Reconciliation Decision 001)
> Per **`MRI_TERMINOLOGY_RECONCILIATION_DECISION_001.md`** (owner-ratified), **"MRI" is a single umbrella concept** comprising the **MRI Experience** (diagnostic understanding & navigation), the **MRI Visualization Model** (this document), **MRI Snapshot**, and **MRI Navigation**.
> - This document is the **MRI Visualization Model** — the component that makes understanding observable (CAF · Reliability · Outcome Confidence). The **MRI Experience** (`MRI_EXPERIENCE_SPECIFICATION_V1.md`) **uses** this model; it does not replace or compete with it.
> - **Substantive positions below are unchanged.** Where this document says "MRI," read it as the **MRI Visualization Model component** of the MRI umbrella. `MRISnapshot` and `Time-to-First-MRI` are unchanged. This is a naming/architecture reconciliation only — no position, behavior, or scope is altered.

> **Scope.** This document defines the **MRI Model** — what MRI is, what it represents, how it relates to CAF, Reliability, and Outcome Confidence, what it makes visible, how it behaves, and how it makes understanding explainable. It does **not** define recommendation logic, overlay behavior, UI implementation, dashboard layouts, scoring formulas, confidence formulas, reliability formulas, or environmental-signal processing. Qualitative levels (High / Moderate / Medium / Low) are used as the related models use them; no visual form, layout, or numeric value is fixed here.
>
> **Governance.** Non-canonical specification formalizing founder-approved positions; adoption subject to governance review. The CAF Assessment, CAF Scoring, Reliability, and Confidence models are consumed, not modified. Canonical terminology is preserved.

---

## 1. Purpose

Define, as a coherent specification, OSLO's **MRI Model**: the layer that makes project understanding observable by representing what OSLO already understands.

This document defines:

- what MRI is;
- what MRI represents;
- how MRI relates to CAF;
- how MRI relates to Reliability;
- how MRI relates to Outcome Confidence;
- what MRI visualizes;
- how MRI behaves;
- how MRI explains understanding.

It is a conceptual and behavioral model of the visualization layer. It defines no visual form, no layout, and no formula.

---

## 2. MRI Overview

**MRI is OSLO's visual representation of project understanding.** *(MRI Position #1)* MRI does not create understanding; **MRI makes understanding visible.** *(MRI Position #1)*

MRI is a **consumer** of the assessment layers — CAF, Reliability, and Outcome Confidence — and nothing more. **MRI does not independently assess, score, or interpret project reality.** *(MRI Position #2)* It holds no assessment of its own; it represents the assessments produced upstream.

**MRI visualizes the current state of project understanding.** Its primary signals are **CAF, Reliability, and Outcome Confidence.** *(MRI Position #3)*

The purpose of MRI is to **make understanding observable.** Through MRI, a user can see: *(MRI Position #4)*

- what OSLO understands;
- how strong that understanding is;
- how trustworthy the assessment is;
- where understanding is weak.

MRI **prioritizes understanding over activity.** It is designed to help users **identify weaknesses in understanding before those weaknesses become outcome failures.** *(MRI Position #7)* It is a window onto the integrity and supportability of understanding, not a record of work performed.

---

## 3. Relationship To CAF

CAF remains the primary assessment layer. In relation to it, MRI's role is bounded:

- **MRI consumes CAF.**
- **MRI does not alter CAF.**
- **MRI does not replace CAF.**
- **MRI visualizes CAF.**

CAF produces the dimensional assessment of understanding integrity; MRI makes that assessment visible without changing it. Nothing MRI does feeds back into CAF.

---

## 4. Relationship To Reliability

Reliability remains the supportability layer. In relation to it:

- **MRI exposes Reliability.**
- **MRI does not determine Reliability.**
- **MRI visualizes Reliability.**

Critically, **MRI must expose Reliability as a first-class signal, distinct from CAF and from Outcome Confidence.** *(MRI Position #8)* Reliability is never folded into the CAF picture or hidden inside the confidence signal; it stands on its own in MRI, so that a user can see *how trustworthy the assessment is* as a separate fact from *how strong the understanding is* and *how confident to be overall*.

---

## 5. Relationship To Outcome Confidence

Outcome Confidence remains the summarized confidence signal. In relation to it:

- **MRI exposes Outcome Confidence.**
- **MRI does not calculate Outcome Confidence.**
- **MRI visualizes Outcome Confidence.**

MRI presents the summarized signal that Confidence has already produced from CAF and Reliability; it performs none of that consolidation itself.

---

## 6. MRI Philosophy

Four questions sit across OSLO's assessment chain, and MRI makes all of them visible:

- **MRI answers:** *"What does OSLO currently understand about project reality?"*
- **CAF answers:** *"How strong is the understanding?"*
- **Reliability answers:** *"How trustworthy is the assessment?"*
- **Outcome Confidence answers:** *"How confident should we be in the understanding?"*

**MRI makes all of these visible.** It is the surface on which the upstream assessments become observable together — strength (CAF), trustworthiness (Reliability), and summarized confidence (Outcome Confidence) — alongside the understanding itself.

Because MRI prioritizes understanding over activity (Section 2), it is oriented toward exposing *where understanding is weak* — surfacing the gaps and weaknesses in understanding while they can still be addressed, rather than reporting on tasks completed.

---

## 7. Primary MRI Signals

MRI makes the current state of project understanding observable through its primary signals: *(MRI Position #3)*

- **CAF** — the strength of understanding, across its independent dimensions. Because the CAF dimensions are independent, MRI can make a weakness in any single dimension visible rather than hidden behind a summary, satisfying the requirement that users can see *where understanding is weak* (Position #4).
- **Reliability** — the trustworthiness of the assessment, exposed as a **first-class signal distinct from CAF and Outcome Confidence** (Position #8).
- **Outcome Confidence** — the summarized confidence signal consolidated upstream.

Alongside these, MRI provides **visibility into the findings that contribute to current understanding** (Section 8), so that the signals are not only seen but understood.

MRI presents these signals; it does not compute them. The strength comes from CAF, the trustworthiness from Reliability, the summary from Outcome Confidence. MRI's contribution is to make them observable together. The specific visual form in which they appear is a matter of visualization design and is out of scope here (Section 12).

---

## 8. MRI Explanation Model

**MRI must provide visibility into the findings that contribute to current understanding. MRI should make understanding explainable. MRI does not require every finding to be shown.** *(MRI Position #5)*

The explanation model therefore has three commitments:

- **Explainability.** MRI exposes enough of the contributing findings that a user can understand *why* the signals are what they are — why CAF sits where it does, and where understanding is weak. The signals are accompanied by the basis that accounts for them.
- **Selectivity.** MRI need not show every finding. Making understanding explainable does not require exhaustive disclosure; it requires that the findings material to the current understanding be visible.
- **Descriptive, not prescriptive.** **MRI is descriptive, not prescriptive.** It explains the current state of project understanding; it **does not prescribe what users should do next.** That function belongs to Recommendations, which are defined separately. *(MRI Position #9)* MRI shows *what is* and *why*; it does not instruct *what to do*.

In this way MRI makes understanding explainable by surfacing its basis — the contributing findings and the CAF, Reliability, and Confidence signals — without crossing into prescription.

---

## 9. MRI Behavior Examples

These examples illustrate the model's expected behavior conceptually. They introduce no formula and no visual specification; qualitative levels are used as the related models use them.

### Example A — strong understanding
- **CAF:** High · **Reliability:** High · **Confidence:** High
- **MRI behavior:** MRI displays strong understanding. All three primary signals are strong and mutually consistent; MRI represents an understanding that is strong, well supported, and confidently held.

### Example B — strong but weakly supported
- **CAF:** High · **Reliability:** Low · **Confidence:** Moderate
- **MRI behavior:** MRI **visibly exposes Reliability** so users understand why confidence is constrained. Because Reliability is a first-class signal (Position #8), MRI shows that the CAF assessment is strong yet the assessment is weakly supported — making clear that the Moderate confidence stems from low reliability, not from weak understanding. The user can see the cause, not just the result.

### Example C — a weakness among strengths
- **CAF:** High · **Reliability:** High · **Confidence:** Medium · *(one CAF dimension weak)*
- **MRI behavior:** MRI **exposes the contributing weakness and preserves explainability.** Because the CAF dimensions are independent, MRI makes the single weak dimension visible rather than averaging it away, and surfaces the findings that account for it (Section 8). The user can see *which* aspect of understanding is weak and *why* confidence is held to Medium despite an otherwise strong, well-supported assessment.

### Example D — understanding changes
- **Trigger:** project evidence changes → CAF changes → Confidence changes
- **MRI behavior:** **MRI updates.** The change in evidence moves CAF (and, through it, Confidence); MRI reflects the new state. **Reason: event-driven behavior** (Section 10) — MRI updated because understanding changed, not because time passed.

---

## 10. Event-Driven Behavior

**MRI is event-driven.** *(MRI Position #6)*

- **MRI updates when project understanding changes.** A change to the underlying assessments — CAF, Reliability, or Outcome Confidence — is what causes MRI to update.
- **MRI does not update merely because time passes.** Absent a change in understanding, MRI is stable.

This inherits directly from the assessment layers: CAF changes only when evidence or findings change; Reliability changes only when Coverage, Evidence Availability, or Assessability change; Outcome Confidence changes only when CAF or Reliability change. MRI, as their consumer, updates exactly when they do — never on the passage of time alone (Example D).

---

## 11. Preserved Model Principles

MRI is a consumer of the upstream models and preserves their principles without redefining them:

| Upstream principle | How MRI preserves it |
|---|---|
| CAF assesses integrity of understanding | MRI visualizes CAF; it does not alter or replace it (§3) |
| CAF dimensions are independent | MRI can expose a single weak dimension rather than hiding it in a summary (§7, §9 Ex. C) |
| Reliability is distinct from CAF and Confidence | MRI exposes Reliability as a first-class, distinct signal (§4, §7, Position #8) |
| Reliability measures supportability, not strength | MRI presents Reliability as trustworthiness of the assessment, separate from CAF strength (§4) |
| Confidence is derived from CAF and Reliability | MRI exposes Confidence; it does not calculate it (§5) |
| Confidence is confidence in understanding, not outcome | MRI represents understanding, prioritizing it over activity; it makes no outcome prediction (§2, §6) |
| Event-driven across the chain | MRI updates only when understanding changes (§10) |
| Findings explain assessments | MRI makes understanding explainable through visibility into contributing findings (§8) |
| Descriptive, not prescriptive | MRI describes; Recommendations prescribe (§8, Position #9) |

MRI **must not redefine** any of these models. It remains strictly a consumer and a visualization layer.

---

## 12. Future Evolution

Future versions may add:

- richer visualizations;
- navigation mechanisms;
- overlays;
- interaction layers.

These extend how understanding is surfaced and explored. **MRI remains the visualization layer**, and these capabilities belong to **separate models** — overlay behavior, interaction, navigation, UI implementation, and dashboard layout are all defined elsewhere, not here. Likewise, recommendation logic (the prescriptive function) and any future environmental-signal processing are out of scope for this model.

---

## 13. Summary

MRI is OSLO's visual representation of project understanding. It does not create, assess, score, interpret, or calculate anything; it makes visible the assessments produced upstream. Its primary signals are CAF (the strength of understanding), Reliability (the trustworthiness of the assessment, exposed as a first-class signal distinct from CAF and Confidence), and Outcome Confidence (the summarized confidence signal) — and alongside them, visibility into the findings that explain the current understanding.

MRI consumes CAF, Reliability, and Outcome Confidence; it visualizes each without altering, determining, or calculating any of them. It prioritizes understanding over activity, exists to make weaknesses in understanding observable before they become outcome failures, and is descriptive rather than prescriptive — it explains the current state but leaves the question of what to do next to Recommendations. MRI is event-driven: it updates when understanding changes and not when time merely passes.

This document defines the MRI model — what MRI represents and how it behaves. It does not define MRI's visual form, layout, overlays, interactions, or any recommendation logic; those belong to separate documents.

---

## Validation

**Founder position coverage**

| Position | Subject | Represented in |
|---|---|---|
| #1 | MRI is the visual representation of understanding; makes it visible, does not create it | §1, §2 |
| #2 | Consumer of CAF/Reliability/Confidence; does not independently assess, score, or interpret | §2 |
| #3 | Visualizes current understanding; primary signals CAF, Reliability, Confidence | §2, §7 |
| #4 | Makes understanding observable; users see what/how strong/how trustworthy/where weak | §2, §7 |
| #5 | Visibility into contributing findings; explainable; not every finding shown | §8 |
| #6 | Event-driven; updates on understanding change, not time | §10, §9 (Ex. D) |
| #7 | Prioritizes understanding over activity; exposes weakness before outcome failure | §2, §6 |
| #8 | Reliability exposed as first-class signal, distinct from CAF and Confidence | §4, §7 |
| #9 | Descriptive, not prescriptive; recommendations prescribe | §8 |

All nine founder positions are represented.

**Required behavior examples:** A (strong understanding), B (Reliability exposed to explain constrained confidence), C (contributing weakness exposed, explainability preserved), D (event-driven update) — all included and explained conceptually (§9).

**Exclusion checklist**
- MRI remains descriptive, not prescriptive — confirmed (§8, §13).
- MRI consumes CAF, Reliability, and Confidence — confirmed (§2–§5, §7).
- MRI does not independently assess project reality — confirmed (§2).
- Reliability remains visible as a first-class signal — confirmed (§4, §7, Position #8).
- MRI remains event-driven — confirmed (§10).
- No recommendation logic — confirmed (§8, §12).
- No overlay logic — confirmed (overlays named only as out-of-scope future, §12).
- No scoring / confidence / reliability formulas — confirmed.
- No UI implementation details or dashboard layouts — confirmed (§7, §12).
- CAF, Reliability, and Confidence models unmodified — confirmed (consumed only).

*MRI Model v1 complete. Formalizes the founder-approved MRI positions; defines MRI as the event-driven, descriptive visualization layer that consumes and makes visible CAF, Reliability, and Outcome Confidence, and makes understanding explainable through visibility into contributing findings. Defines the model only — not visual form, overlays, interaction, or recommendation logic. Subject to governance review before adoption.*
