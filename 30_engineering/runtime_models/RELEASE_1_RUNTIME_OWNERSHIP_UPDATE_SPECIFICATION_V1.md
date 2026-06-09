# Release 1 Runtime Ownership Update Specification v1

**Document Type:** Ownership Remap (architecture-to-Release-1; advisory — owner ratifies) · **Status:** **Ratified under DL-043 (2026-06-04) — with R1 Authority-scope reconciliation below** · **Date:** 2026-06-04
**Target model (authoritative for this remap):** `OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md` (Canonical under DL-043). **Supersedes the mapping in:** `RELEASE_1_RUNTIME_LAYER_OWNERSHIP_SPECIFICATION_V1.md` (layer-primary).

> ### ⚠ DL-043 RECONCILIATION (2026-06-04) — supersedes the "Authority involvement" column for Release 1
> The responsibility ownership (Producer column) is **canonical and unchanged**. But the **Authority-involvement** entries below (promotion authorization, "Authority governs exposure/timing", Wave D) describe the **target/Future model** — under DL-043, **Authority is inactive in Release 1** (Integrity-not-Authority): R1 admission is **integrity-gated** (Perceive readiness + Retain provenance), R1 exposure is **epistemic-safety disclosure** (Disclose), and R1 disposition is **user-acceptance attestation + reconciliation** (Wave U), **not** an Authority Governance Decision. Read the "Authority involvement" cells as **Future-model annotations**; in R1 they resolve to **integrity + Disclose**, no Authority engine.

> **Constraints.** No implementation, APIs, schemas, services, prompts, tools, or database design. **Does not re-open the architecture debate** — the Cognitive Responsibility model is **treated as the target**. Anything unclear or dependent on an unmade owner decision is marked **Requires Owner Decision (ROD)**. **The target architecture is Draft pending owner ratification (and sequenced with GOV-ARCH-001/001A/000); every mapping below is therefore conditional on that ratification.**

---

## 1. Purpose

Remap every Release 1 capability, object, surface, signal, and invariant from the **old layer-primary model** to the **new Cognitive Responsibility Architecture**, so that — once the target model is ratified — each Release 1 element has an unambiguous **owning responsibility** before Contract Inventory generation. This update closes the ownership gaps the prior (layer-primary) analysis left open, and states precisely what remains owner-dependent.

## 2. Source Documents Reviewed

`OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md` (target) · `OSLO_ARCHITECTURE_VALIDATION_REVIEW_003.md` · `OSLO_COGNITIVE_RESPONSIBILITY_VS_LAYER_ARCHITECTURE_REVIEW_001.md` · `OSLO_ADVISORY_COGNITION_ARCHITECTURE_SPECIFICATION_V1.md` · `RELEASE_1_RUNTIME_LAYER_OWNERSHIP_SPECIFICATION_V1.md` (prior) · `OSLO_ARCHITECTURE_BASELINE_V1.md` · `RELEASE_1_UX_PRODUCT_BACKLOG_V1.md` / `RELEASE_1_UX_EXECUTION_PLAN_V1.md` / `RELEASE_1_UX_HANDOFF_PACKAGE_SPECIFICATION_V1.md` and the active Release 1 UX specs · ratified UX decisions (AMB-1; MRI umbrella).

## 3. New Ownership Model Summary

In-loop responsibilities: **Perceive → Retain → Intend → Infer → Evaluate → Advise → Disclose → Act** (→ **Coordinate**, multi-agent). Cross-cutting: **Authority Plane** (Governance — constrains inputs, governs outputs; generates nothing), **Perception**, **Adapt** (emergent recompute). Evolution: **Learn**. Non-cognitive support: **Render** service. **Responsibility-primary**; layers retained only as dependency-ordering representation. *Cognition generates; Authority governs; Render formats; Disclose conveys meaning.*

## 4. Release 1 Ownership Matrix

*Producer = owning responsibility that creates it. Authority = Authority-Plane involvement (exposure/authorization). Disclose/Render = presentation. Status vs target model.*

| Release 1 element | Owning responsibility (Producer) | Authority involvement | Disclose / Render | Status (target model) |
|---|---|---|---|---|
| **Project intake / Create Project** | **Perceive** | posture/tier constrains intake | Render (intake UI) | **Mapped** |
| **Artifact ingestion (upload/paste)** | **Perceive** | constrains intake | Render | **Mapped** |
| **Charter / Scope / Requirements / WBS / Resource / Schedule / Summary** | **Retain** (canonical knowledge); the **declared outcome** within them → **Intend** (reference) | promotion authorization | Disclose/Render | **Mapped** (generic); **ROD** on individual object typing (R1 treats as generic "artifacts") + on whether Intend is a first-class R1 object |
| **Findings** | **Infer** | — | Disclose | **Mapped** |
| **Issues** | **Evaluate** | exposure disposition | Disclose | **Mapped** |
| **Recommendations** | **Advise** | constrains generation; governs exposure | Disclose (Recommendation Panel) | **Mapped — gap CLOSED** |
| **Clarifications** | **Advise** (Clarification engine) | governs exposure | Disclose (in context) | **Mapped — gap CLOSED** (was Planned/unowned) |
| **Assumptions** | **Retain** (epistemic record) | — | Disclose | **Mapped** |
| **CAF (Clarity/Alignment/Feasibility)** | **Evaluate** | — | Disclose (reliability-qualified) | **Mapped** |
| **Reliability** | **Evaluate** | — | Disclose | **Mapped — gap CLOSED** (was Unmapped) |
| **Confidence** | **Evaluate** | — | Disclose (never as health/score) | **Mapped** |
| **Severity** | **Evaluate** | disposition input | Disclose | **Mapped** |
| **Stale / Reanalysis state** | **Adapt** (emergent recompute) | — | Disclose (labeled "previous analysis") | **Mapped** (Adapt active in R1) |
| **MRI** | **Disclose** (diagnostic rendering of Infer/Evaluate outputs) + **Render** | exposure of contents | **Disclose/Render** | **Mapped — gap CLOSED** (was Planned stub) |
| **Overview** | **Disclose / Render** (presentation) | exposure | Disclose/Render | **Mapped** |
| **Artifact Workspace** | **Disclose / Render** (content presentation); **editing → Perceive** (re-intake of changed content → Adapt) | exposure; mutation authorization | Disclose/Render | **Mapped** |
| **Finding Panel** | **Disclose / Render** over **Infer** (Finding) + **Evaluate** (Issue assessment) + **Advise** (Recommendation) | exposure | Disclose/Render | **Mapped — Finding/Issue terminology resolved** |
| **Recommendation Panel** | **Disclose / Render** over **Advise** outputs | governed exposure | Disclose/Render | **Mapped — producer gap CLOSED** |
| **Companion** | **Disclose / Render** (persistent presentation) | exposure | Disclose/Render | **Mapped** |
| **Chat** | **Disclose / Render** (conversational disclosure); **clarification capture → Perceive** | exposure | Disclose/Render | **Mapped**; **ROD** on whether Chat's clarification capture is formally Perceive |
| **Notifications / Awareness** | **Disclose** (awareness presentation) | **Authority** governs exposure/timing | Disclose/Render | **Mapped** (no delivery infra — R1) |
| **History** | **Retain** (append-only) + **Disclose / Render** (timeline) | exposure | Disclose/Render | **Mapped** |
| **Export / Sharing** | **Disclose / Render** (packages existing understanding) | **Authority** governs exposure | Disclose/Render | **Mapped** |
| **Help** | **Render** service (+ light **Disclose**) — *about OSLO, not project understanding* | — | Render | **Mapped**; **ROD** on Service vs Disclose classification (non-cognitive) |
| **Settings** | **Service / periphery** (management; **outside** the cognitive loop) | — | Render | **Mapped** as non-cognitive; **ROD** to confirm "not a cognitive responsibility" |

**Invariant remap:**
- *Only reanalysis changes assessment* → **only Adapt (recompute) changes Evaluate/Advise outputs**; no Disclose/Render/Perceive-edit changes an assessment directly.
- *Recommendation only in Finding context* → **Advise outputs anchor to Infer/Evaluate (Finding/Issue)**; Disclose opens the Recommendation Panel only in Finding context.
- *Confidence = trust, never project health* → **Evaluate output**, Disclosed reliability-qualified, never reframed.
- *Stale never current* → **Disclose** presents **Adapt** state honestly.
- *History append-only* → **Retain** append-only.
- *Resolution Paths presentation-only* → **Disclose/Render** over multiple **Advise** recommendations (no object).

## 5. Epic-by-Epic Impact

| Epic | Primary responsibilities | Change from layer model |
|---|---|---|
| EP-1 App Shell & Navigation | Disclose/Render (+ Authority exposure) | unchanged (presentation/navigation) |
| EP-2 Entry & Onboarding | **Perceive** (+ Intend reference; Infer/Evaluate orientation) | intake clarified as Perceive; **Intend** newly named |
| EP-3 Project Discovery | Disclose/Render | unchanged |
| EP-4 Project Overview | **Evaluate** signals via **Disclose** | Reliability now **Evaluate** (was unmapped) |
| EP-5 MRI | **Disclose/Render** (diagnostic) | **gap closed** — MRI owned by Disclose (was stub) |
| EP-6 Artifact Workspace & Editing | Disclose/Render; **Perceive** (edit→re-intake); **Adapt** (reanalysis) | editing clarified as Perceive→Adapt |
| EP-7 Finding & Recommendation Panels | Disclose/Render over **Infer/Evaluate/Advise** | **gaps closed** — Recommendation producer = **Advise**; Finding/Issue resolved |
| EP-8 Understanding Companion | Disclose/Render | unchanged; Top-Rec routes via Finding (Advise) |
| EP-9 OSLO Chat | Disclose/Render + **Perceive** (clarification) | clarification capture clarified (ROD) |
| EP-10 Collaboration & Sharing | Disclose/Render (object-orbiting); Authority exposure | unchanged (comments orbit objects) |
| EP-11 Notification & Awareness | **Disclose** + Authority exposure | unchanged |
| EP-12 History & Timeline | **Retain** + Disclose/Render | history = Retain (append-only) |
| EP-13 Export & Share-Out | Disclose/Render + Authority | unchanged |
| EP-14 Help & Support | **Render** service | clarified as non-cognitive (ROD) |
| EP-15 Settings & Tier Visibility | **Service/periphery** | clarified as outside cognition |

**Net:** the EP-7 (Recommendations), EP-4/EP-5 (Reliability/MRI), and EP-9 (Clarification) ownership conflicts are **resolved** under the target model; presentation epics are unaffected (they remain Disclose/Render of existing outputs).

## 6. Contract-Generation Impact

The prior blocker to Contract Inventory was that **several Release 1 capabilities had no producing owner** (recommendation production = conflict; reliability/clarification = unmapped) — an Implementation Contract cannot trace to a producer that does not exist. Under the target model **every Release 1 element now has an owning responsibility**, so:
- **Presentation/UX contracts** (Disclose/Render — the large majority of Release 1 UX: shell, overview, MRI, panels, companion, awareness, history, export, help, settings) **can be generated now** — they present existing outputs and are unaffected by the ratification question.
- **Cognition-owned contracts** (Advise: Recommendations/Clarifications; Evaluate: Reliability/Confidence/CAF/Severity; Infer: Findings; Intend: outcome reference; Perceive: intake; Adapt: reanalysis) become generable **once the target model is owner-ratified** — at which point their Implementation Contracts can cite a documented producing responsibility (closing the C-1 traceability failure).
- **Until ratification**, contracts for Advise/Intend-owned capabilities should be **gated** (the producer is documented in a Draft, not yet canonical).

## 7. Remaining Owner Decisions (ROD)

1. **Ratify the target architecture** (`OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md`), sequenced with GOV-ARCH-001/001A/000 — **everything here is conditional on this.**
2. **Intend in Release 1:** is the project outcome/charter a first-class **Intend** reference object in R1, or user-declared-and-Retained only?
3. **Named Knowledge object typing** (Charter/WBS/Resource/Schedule…) vs generic "artifacts."
4. **Chat clarification capture** = formally **Perceive**?
5. **Help / Settings classification** as **Service/periphery** (non-cognitive) — confirm.
6. **Learn / Coordinate** = out of Release 1 (confirm; they have no R1 elements).
7. Calibration/tier values (carried RR-1/RR-2).

## 8. Gaps Closed by the New Architecture

- **Recommendation production** — now **Advise** (was the headline C-1 *conflict* with no owning layer). **Closed.**
- **Recommendation Panel content producer** — now **Advise**. **Closed.**
- **Reliability ownership** — now **Evaluate** (was Unmapped). **Closed.**
- **Clarification ownership** — now **Advise** (was Planned/unowned). **Closed.**
- **MRI ownership** — now **Disclose** (was a Planned stub). **Closed** (as a presentation concern over Infer/Evaluate).
- **Finding vs Issue terminology** — resolved: UX "Finding" = **Infer** Finding + **Evaluate** Issue assessment, presented as one panel; runtime distinction preserved. **Closed.**
- **Outcome/alignment reference** — now named **Intend** (was implicit). **Closed (named).**

## 9. Gaps Still Open

- **Target model not yet ratified** (Draft; GOV-ARCH-001 pending) — the **single gating open item**; all closures are conditional.
- **Intend scoping in R1** (ROD-2), **object typing** (ROD-3), **Chat-as-Perceive** (ROD-4), **Help/Settings classification** (ROD-5) — minor, non-blocking once the model is ratified.
- **Learn / Coordinate** — future responsibilities, **no R1 elements** (confirm out-of-scope).
- Calibration/tier numbers (RR-1/RR-2) — carried; gate threshold tests, not ownership.

## 10. Conformance Rules

A conforming Release 1 ownership mapping MUST (under the target model):
- **OW-1.** Assign every Release 1 element exactly one **owning responsibility** (Producer); no orphan, no duplicate.
- **OW-2.** **Recommendations/Clarifications → Advise** (governable candidate generation); **never** Infer/Evaluate/Authority/Disclose.
- **OW-3.** **Reliability/Confidence/CAF/Severity → Evaluate**; **Findings → Infer**; **assumptions/history → Retain**.
- **OW-4.** **MRI, panels, overview, companion, awareness, export → Disclose/Render**; **Render** performs no cognition.
- **OW-5.** **Authority** governs exposure/authorization; **generates nothing**; **only Adapt (recompute) changes assessment outputs**.
- **OW-6.** **Resolution Paths presentation-only** (Disclose over multiple Advise recommendations; no object).
- **OW-7.** Preserve all ratified Release 1 invariants (Recommendation-only-in-Finding-context; Confidence-never-health; stale-never-current; history append-only).
- **OW-8.** Mark anything model-dependent or undecided as **ROD**; do not infer.

## 11. Final Readiness Verdict for Contract Inventory Generation

**CONDITIONALLY READY.**

- **Ready now:** **Presentation/UX contracts** (Disclose/Render — the majority of Release 1 UX) — every Release 1 surface has a clear presentation owner, the invariants are intact, and these are unaffected by the architecture-ratification question. Contract Inventory generation for the **UX/presentation epics can proceed.**
- **Ready upon ratification:** **Cognition-owned contracts** (Advise/Intend/Evaluate-Reliability/Infer/Perceive/Adapt) — the new model **closes the ownership gaps that previously blocked these** (recommendation production, reliability, clarification, MRI), so they are *content-ready*; they become *generable* the moment the target architecture is **owner-ratified** (sequenced with GOV-ARCH-001).
- **Single blocking condition:** owner ratification of `OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md`. Until then, gate Advise/Intend-owned contracts; proceed with presentation contracts.

**Recommendation:** **(1)** generate the Contract Inventory for **presentation epics now**; **(2)** ratify the target architecture (with GOV-ARCH-001) to unblock **cognition-owned contracts**; **(3)** resolve the minor RODs (Intend scope, object typing, Chat/Help/Settings classification) alongside — none blocks beyond their specific contracts.

---

*This specification remaps every Release 1 capability, object, surface, signal, and invariant from the old layer-primary model onto the ratified-pending Cognitive Responsibility Architecture (Perceive/Retain/Intend/Infer/Evaluate/Advise/Authority Plane/Disclose/Act/Learn/Coordinate/Render). It provides a full ownership matrix and epic-by-epic impact showing the cognition core mapping cleanly — Findings→Infer; Issues/CAF/Confidence/Reliability/Severity→Evaluate; Recommendations/Clarifications→Advise; assumptions/history→Retain; intake→Perceive; reanalysis→Adapt; exposure→Authority; all surfaces (overview, MRI, panels, companion, awareness, history, export) →Disclose/Render — and closes the previously-blocking ownership gaps (recommendation production, Reliability, clarification, MRI, and the Finding/Issue terminology), while naming Intend as the outcome-alignment reference. It assesses contract-generation impact (presentation contracts generable now; cognition-owned contracts generable upon ratification, since they now have documented producers), records the remaining owner decisions (chief among them ratifying the target model, sequenced with GOV-ARCH-001), and concludes that Release 1 is Conditionally Ready for Contract Inventory generation: proceed with presentation/UX contracts now, and unblock the cognition-owned contracts upon owner ratification of the Cognitive Responsibility Architecture. It defines no implementation, APIs, schemas, services, prompts, tools, or databases, and does not re-open the architecture debate.*

**Release 1 Runtime Ownership Update Specification v1 complete.**
