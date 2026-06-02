# Overlay Model v1

**Document:** OVERLAY_MODEL_V1.md
**Status:** Specification of the Overlay Model (founder-approved positions formalized)
**Consumes (authoritative, unmodified):** `CAF_ASSESSMENT_MODEL_V1.md` · `CAF_SCORING_MODEL_V1.md` · `RELIABILITY_MODEL_V1.md` · `CONFIDENCE_MODEL_V1.md` · `MRI_MODEL_V1.md`
**Date:** 2026-05-31

> **Scope.** This document defines the **Overlay Model** — what an Overlay is, what it represents, how it relates to MRI and to CAF / Reliability / Outcome Confidence, what Overlays do and do not do, how they behave, and how they support attention management. It does **not** define recommendation logic, UI implementation, workflow behavior, dashboard layouts, scoring formulas, confidence formulas, reliability formulas, or environmental-signal processing. Overlay names used as examples are illustrative only and do not define a canonical overlay set.
>
> **Governance.** Non-canonical specification formalizing founder-approved positions; adoption subject to governance review. The CAF Assessment, CAF Scoring, Reliability, Confidence, and MRI models are consumed, not modified. Canonical terminology is preserved.

---

## 1. Purpose

Define, as a coherent specification, OSLO's **Overlay Model**: the attention-management layer that applies contextual lenses to MRI so users can focus on specific aspects of project understanding.

This document defines:

- what an Overlay is;
- what an Overlay represents;
- how Overlays relate to MRI;
- how Overlays relate to CAF, Reliability, and Outcome Confidence;
- what Overlays do;
- what Overlays do not do;
- how Overlays behave;
- how Overlays support attention management.

It is a conceptual and behavioral model. It defines no visual form, no layout, no workflow, and no formula.

---

## 2. Overlay Overview

**Overlays are contextual lenses applied to MRI.** *(Overlay Position #1)* An Overlay changes *how* understanding is viewed without changing the understanding itself: **Overlays do not create understanding; Overlays alter how understanding is viewed.** *(Overlay Position #1)*

**Overlays consume MRI.** They **do not consume raw evidence**; they **operate on already-assessed understanding.** *(Overlay Position #2)* By the time an Overlay is applied, evidence, inference, findings, impact assessment, CAF, Reliability, and Outcome Confidence have already done their work and MRI has made the result visible. The Overlay acts only on that finished, visible understanding.

**The purpose of Overlays is to prioritize attention.** Overlays help users focus on specific aspects of project understanding. *(Overlay Position #3)* An Overlay does not add information; it organizes the user's attention across information that already exists.

---

## 3. Relationship To MRI

MRI remains the visualization layer. In relation to it, the Overlay's role is bounded:

- **Overlays consume MRI.**
- **Overlays do not replace MRI.**
- **Overlays do not alter MRI.**
- **Overlays provide alternate views of MRI.**

An Overlay is a lens over MRI, not a substitute for it. The MRI beneath an Overlay is unchanged; the Overlay only changes which parts of that MRI are emphasized for the viewer. Multiple alternate views of the same MRI may coexist (Section 8).

---

## 4. Relationship To CAF

CAF remains the assessment layer.

- **Overlays do not assess understanding.**
- **Overlays may emphasize specific CAF dimensions** (for example, drawing attention to Clarity, Alignment, or Feasibility).
- **Overlays may not modify CAF.**

An Overlay can foreground a CAF dimension so the user attends to it, but the dimension's assessed value is untouched. Emphasis is a property of the view, not of the assessment.

---

## 5. Relationship To Reliability

Reliability remains the supportability layer.

- **Overlays may emphasize Reliability.**
- **Overlays may not modify Reliability.**

An Overlay can draw attention to how trustworthy the assessment is, but it neither determines nor changes Reliability. Reliability remains a first-class signal in MRI (per the MRI model); an Overlay only changes how prominently it is attended to.

---

## 6. Relationship To Outcome Confidence

Outcome Confidence remains the confidence layer.

- **Overlays may emphasize Confidence.**
- **Overlays may not modify Confidence.**

An Overlay can foreground the summarized confidence signal, but it performs none of the consolidation that produces Confidence and changes none of its value.

---

## 7. Overlay Philosophy

Three questions sit in sequence across the experience, and Overlays occupy the middle one:

- **MRI answers:** *"What does OSLO understand?"*
- **Overlays answer:** *"What deserves attention within that understanding?"*
- **Recommendations answer:** *"What should the user do next?"*

**Overlays occupy the attention-management layer between MRI and Recommendations.**

This positions Overlays precisely: **Overlays make attention navigable; Recommendations make action navigable.** *(Overlay Position #8)* Overlays are **descriptive** — they describe what within the understanding warrants focus. **Overlays do not prescribe actions; Recommendations perform that function.** *(Overlay Position #4)* An Overlay helps a user *look in the right place*; it never tells the user *what to do* there.

---

## 8. Overlay Behavior Model

**Overlays may highlight understanding; Overlays do not alter understanding.** CAF, Reliability, Confidence, and MRI remain unchanged under any Overlay. *(Overlay Position #6)*

**Permitted operations.** An Overlay may: *(Overlay Position #9)*

- **emphasize** — bring specific aspects of understanding to the foreground;
- **suppress** — push less relevant aspects to the background;
- **filter** — narrow the view to a relevant subset;
- **group** — organize aspects of understanding together for focus.

**The hard constraint.** **Overlays may never distort the underlying understanding.** *(Overlay Position #9)* Emphasis, suppression, filtering, and grouping change *salience*, never *substance*. An aspect that is suppressed is still part of the understanding; a subset that is filtered into view is shown as it actually is. No Overlay operation may misrepresent CAF, Reliability, Confidence, or MRI.

**Multiplicity.** **Multiple Overlays may exist over the same MRI simultaneously.** *(Overlay Position #5)* Illustrative examples include a Clarity Overlay, Alignment Overlay, Feasibility Overlay, Finding Overlay, Stakeholder Overlay, Review Overlay, or Risk Overlay. *These examples illustrate the concept only and do not define the canonical overlay set.*

**Determinism.** **The same project understanding produces the same overlay result when the same overlay configuration is applied.** Overlay behavior must be **deterministic.** *(Overlay Position #10)* Given identical MRI and an identical overlay configuration, the resulting view is identical — there is no variation that is not traceable to a change in the underlying understanding or the configuration.

---

## 9. Overlay Behavior Examples

These examples illustrate the model's expected behavior conceptually. They introduce no formula and no visual specification.

### Example A — Clarity Overlay
- **State:** MRI unchanged; a Clarity Overlay is applied.
- **Result:** Clarity-related understanding receives emphasis; the underlying understanding remains unchanged. The lens foregrounds Clarity for attention; CAF, Reliability, Confidence, and MRI are untouched (Section 8).

### Example B — Risk Overlay
- **State:** MRI unchanged; a Risk Overlay is applied.
- **Result:** Risk-relevant understanding receives emphasis; the underlying understanding remains unchanged. A different lens foregrounds a different aspect, again altering only salience, not substance.

### Example C — two users, two lenses
- **State:** Two users apply different overlays to the same project.
- **Result:** CAF, Reliability, and Confidence remain identical for both; only the attention lens differs. The understanding is one and the same; each user is simply attending to a different part of it. This demonstrates that Overlays change the *view*, never the *understanding*.

### Example D — understanding changes
- **State:** MRI changes because understanding changes.
- **Result:** The Overlay updates automatically. **Reason: event-driven inheritance** (Section 10) — the Overlay tracks its MRI, so when MRI moves, the Overlay's view moves with it.

---

## 10. Event-Driven Behavior

**Overlays inherit MRI's event-driven behavior.** *(Overlay Position #7)*

```text
MRI changes
  ↓
Overlay changes
```

- An Overlay updates **when the MRI it consumes changes** — which, per the MRI model, happens only when project understanding changes.
- **Time passing alone does not change overlays.** Absent a change in MRI (and therefore in understanding), an Overlay's view is stable.

This inheritance runs the full chain: CAF changes only on evidence or finding change; Reliability changes only on Coverage / Evidence Availability / Assessability change; Confidence changes only when CAF or Reliability change; MRI updates only when those change; and Overlays update only when MRI updates. Overlays add no independent timing of their own.

---

## 11. Preserved Model Principles

Overlays are consumers of the upstream models and preserve their principles without redefining them:

| Upstream principle | How Overlays preserve it |
|---|---|
| CAF assesses integrity of understanding | Overlays do not assess; they may emphasize CAF but never modify it (§4) |
| CAF dimensions are independent | Overlays may foreground a single dimension without changing any (§4) |
| Reliability is distinct and first-class | Overlays may emphasize Reliability but never determine or modify it (§5) |
| Confidence is derived, not independent | Overlays may emphasize Confidence but never calculate or modify it (§6) |
| MRI is the descriptive visualization layer | Overlays consume MRI, provide alternate views, and never replace or alter it (§3) |
| Event-driven across the chain | Overlays update only when MRI changes, never on time alone (§10) |
| Descriptive, not prescriptive | Overlays describe what deserves attention; Recommendations prescribe action (§7) |
| Understanding must not be distorted | Overlay operations change salience, never substance (§8) |

Overlays **must remain consumers** of these models and **must not redefine** them.

---

## 12. Future Evolution

Future versions may add:

- overlay composition;
- overlay hierarchies;
- advanced navigation;
- contextual workflows.

These are future capabilities. The Overlay model **remains an attention-management layer**; composition, hierarchy, navigation, and contextual workflows — along with UI implementation, dashboard layout, and recommendation logic — are defined elsewhere, not here. Any future environmental-signal processing is likewise out of scope.

---

## 13. Summary

Overlays are contextual lenses applied to MRI. They consume MRI — already-assessed, already-visible understanding — never raw evidence, and they exist to prioritize attention: to help users focus on specific aspects of project understanding. An Overlay may emphasize, suppress, filter, or group what is shown, but it may never distort the underlying understanding; CAF, Reliability, Confidence, and MRI remain unchanged under any Overlay, and multiple Overlays may view the same MRI at once.

Overlays sit in the attention-management layer between MRI and Recommendations: MRI shows what OSLO understands, Overlays show what deserves attention within it, and Recommendations — defined separately — address what to do next. Overlays are descriptive, not prescriptive; they make attention navigable, not action. They inherit the chain's event-driven behavior, updating only when MRI changes and never on the passage of time, and they are deterministic: the same understanding under the same overlay configuration yields the same view.

This document defines the Overlay model — what Overlays represent and how they behave. It does not define their visual form, layout, composition, navigation, workflows, or any recommendation logic; those belong to separate documents.

---

## Validation

**Founder position coverage**

| Position | Subject | Represented in |
|---|---|---|
| #1 | Contextual lenses on MRI; alter view, do not create understanding | §2 |
| #2 | Consume MRI, not raw evidence; operate on assessed understanding | §2 |
| #3 | Purpose is to prioritize attention | §2, §7 |
| #4 | Descriptive; do not prescribe; Recommendations prescribe | §7 |
| #5 | Multiple overlays over one MRI; example set illustrative only | §8 |
| #6 | May highlight, not alter; CAF/Reliability/Confidence/MRI unchanged | §8 |
| #7 | Inherit MRI event-driven behavior; time alone does not change overlays | §10, §9 (Ex. D) |
| #8 | Overlays make attention navigable; Recommendations make action navigable | §7 |
| #9 | May emphasize/suppress/filter/group; never distort | §8 |
| #10 | Deterministic; same understanding + config → same result | §8 |

All ten founder positions are represented.

**Required behavior examples:** A (Clarity Overlay — emphasis, understanding unchanged), B (Risk Overlay — emphasis, understanding unchanged), C (two users, different lenses, identical CAF/Reliability/Confidence), D (event-driven update) — all included and explained conceptually (§9).

**Exclusion checklist**
- Overlays remain consumers of MRI — confirmed (§2, §3).
- Overlays do not consume raw evidence — confirmed (§2).
- Overlays do not modify understanding — confirmed (§6, §8).
- Overlays remain descriptive — confirmed (§7).
- Overlays remain deterministic — confirmed (§8).
- Overlays remain event-driven — confirmed (§10).
- Overlays support attention management — confirmed (§2, §7, §8).
- No recommendation logic — confirmed (§7, §12).
- No workflow implementation details — confirmed (contextual workflows named only as out-of-scope future, §12).
- No UI implementation details — confirmed (§12).
- No scoring formulas — confirmed.
- CAF, Reliability, Confidence, and MRI models unmodified — confirmed (consumed only).

*Overlay Model v1 complete. Formalizes the founder-approved overlay positions; defines Overlays as deterministic, event-driven, descriptive attention-management lenses that consume MRI and emphasize, suppress, filter, or group understanding without ever altering or distorting it. Defines the model only — not visual form, composition, navigation, workflows, or recommendation logic. Subject to governance review before adoption.*
