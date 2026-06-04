# OSLO Cognitive Responsibility Architecture Ratification Package v1

**Document Type:** Owner-Ratification Package · **Status:** **Pending Owner Decision** · **Date:** 2026-05-31
**Decides:** `OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md` (Draft). **Inputs:** that spec · `OSLO_ARCHITECTURE_VALIDATION_REVIEW_003.md` · `OSLO_ADVISORY_COGNITION_ARCHITECTURE_SPECIFICATION_V1.md` · `RELEASE_1_RUNTIME_OWNERSHIP_UPDATE_SPECIFICATION_V1.md` · `RELEASE_1_UX_PRODUCT_BACKLOG_V1.md` · `RELEASE_1_UX_EXECUTION_PLAN_V1.md` · existing repository architecture docs.

> **Mode:** owner-ratification package only — **no** implementation, APIs, schemas, databases, frameworks, tools, prompts, vendors, or code. The Cognitive Responsibility Architecture is **Draft pending owner ratification**. This package **does not re-open the architecture debate**; it presents **only the decisions required before Contract Inventory generation**, separates **Release 1-blocking** from **future/non-blocking**, and **marks unresolved items** rather than inferring them. **Per `CLAUDE.md`, only the owner ratifies.**

---

## 1. Ratification Summary

- **What is being ratified:** OSLO's **canonical architectural model** — a **Cognitive Responsibility Architecture** (responsibility-primary), with the validated responsibility set and the closure of the Release 1 ownership gaps (recommendation production, Reliability, Clarification, MRI, Finding/Issue).
- **Why now:** Release 1 **Contract Inventory generation cannot begin** for cognition-owned capabilities until each has a **documented owning responsibility**. The model supplies them; **ratification is the single gating step** before contracts can trace to a producer.
- **What becomes canonical if approved:** the responsibility model becomes OSLO's **primary** architecture; the prior six-layer model is retained as a **secondary dependency-ordering representation**; Advisory Cognition (Advise), Intend, and the Authority-Plane reclassification become canonical; Release 1 ownership is **frozen** per §3.

## 2. Core Architecture Decision

**Proposed canonical model:**
```text
Perceive → Retain → Intend → Infer → Evaluate → Advise → Disclose → Act        (→ Coordinate, future/multi-agent)
   cross-cutting: AUTHORITY (Governance — constrains inputs, governs outputs, generates nothing)
   cross-cutting: PERCEPTION · ADAPT (emergent recompute)
   evolution: LEARN (future)        non-cognitive support: RENDER (service)
```

**The shift:** from **layer-primary** (six stacked layers as the fundamental unit) to **responsibility-primary** (the cognitive verb is fundamental; a Domain is a responsibility of engines; **Layer is a secondary representation**). This is a **change of primacy and vocabulary, not of the work OSLO already does** — it names the responsibilities OSLO performs, adds the previously-missing **Advise** and **Intend**, and corrects **Adapt** (emergent) and **Governance** (cross-cutting). It survived adversarial validation (Review 003).

## 3. Release 1 Ownership Freeze

| Release 1 element | Owning responsibility | Decision |
|---|---|---|
| Project intake / Create Project / Upload / Paste | **Perceive** | Ratify now |
| Charter / Scope / Requirements / WBS / Resource / Schedule / Summary | **Retain** (declared outcome → **Intend**) | Requires owner decision (Intend scope; object typing) |
| Assumptions · History | **Retain** | Already consistent |
| Findings · Alignment/Coverage/Quality/SMART Gaps | **Infer** | Already consistent |
| Issues · Severity · CAF · **Reliability** · Confidence | **Evaluate** | Ratify now (Reliability newly placed) |
| **Recommendations** · **Clarification Requests** | **Advise** | Ratify now (gap closed) |
| Stale / Reanalysis state | **Adapt** (emergent recompute) | Already consistent |
| Exposure / Suppression / Authorization / Timing | **Authority Plane** | Ratify now (reclassified cross-cutting) |
| **MRI** · Overview · Finding Panel · Recommendation Panel · Companion · Chat · Notifications/Awareness · Export/Sharing · History (timeline) | **Disclose / Render** | Ratify now (MRI gap closed) |
| Resolution Paths | **Disclose/Render** (presentation-only; multiple Advise recs) | Ratify now |
| Artifact Workspace (editing) | **Disclose/Render** + **Perceive** (edit→re-intake→Adapt) | Already consistent |
| Help · Settings | **Service / Periphery** (non-cognitive) | Requires owner decision (confirm classification) |
| Learn · Coordinate | — | **Future** (no Release 1 elements) |

## 4. Blocking Decisions Before Contract Inventory

*(These block or materially affect contract generation. Each is a Yes/Ratify decision.)*
- **B-1. Ratify the Cognitive Responsibility Architecture** as the target model (sequenced with GOV-ARCH-001/001A/000). **Gates all cognition-owned contracts.**
- **B-2. Confirm `Intend`** owns the **declared outcome / reference model** (the alignment target).
- **B-3. Confirm `Advise`** owns **Recommendations** and **Clarification Requests** (governable candidate generation).
- **B-4. Confirm `Evaluate`** owns **Reliability** (with Confidence/CAF/Severity).
- **B-5. Confirm `MRI`** is **Disclose/Render diagnostic** (not a cognitive layer).
- **B-6. Confirm Resolution Paths remain presentation-only** (multiple Advise recommendations; no object).
- **B-7. Confirm Authority/Governance is cross-cutting and generates nothing** (constrains inputs, governs outputs).

## 5. Non-Blocking / Future Decisions

- **Learn** responsibility (engine improvement from outcomes) — future; no Release 1 elements.
- **Coordinate** responsibility + **multi-agent arbitration** — future; no Release 1 elements.
- **Future engine catalogs** per domain — named illustratively; defer.
- **Naming refinements** (e.g., **Disclose** vs **Communication**; **Authority** vs **Governance**; **Perceive** vs **Context Plane**) — cosmetic; defer or fold into ratification at owner preference.
- **Object typing** (Charter/WBS/etc. as named objects vs generic artifacts) — refine post-ratification; does not block presentation contracts.

## 6. Ratification Options

| Option | Action | Consequence for Contract Inventory |
|---|---|---|
| **A. Ratify as written** | Adopt the model and §3 freeze as-is | **All** Release 1 contracts (presentation **and** cognition-owned) can be generated; fastest path; accepts current naming. |
| **B. Ratify with modifications** | Adopt the model + freeze, with minor **naming/scoping** changes (e.g., keep "Communication" label; confirm Intend/Help/Settings scope) | Same unblocking as A once modifications are recorded; small delay to capture the edits; **recommended**. |
| **C. Do not ratify yet** | Hold the model in Draft | **Presentation/UX contracts may proceed** (ownership already clear, §9); **cognition-owned contracts remain blocked** (no documented producer) — Release 1 contract inventory proceeds **partially** only. |

## 7. Recommended Owner Decision

**Recommend Option B — Ratify with minor naming/scoping modifications, then proceed to Release 1 Contract Inventory generation.**
- The model **closes the blocking ownership gaps**, **survived adversarial validation**, and **changes naming/primacy, not the work**. Ratifying unblocks **all** Release 1 contracts.
- The few genuinely-open items (Intend scope; Help/Settings classification; object typing; naming preferences) are **minor and non-structural** — capture them as the "modifications" in B rather than holding the whole model in Draft (Option C), which would only partially unblock the inventory.
- Sequence the ratification with **GOV-ARCH-001/001A/000** (the architecture-representation review), which this body of work directly informs toward a responsibility-primary resolution.

## 8. Post-Ratification Next Step

**Create `RELEASE_1_CONTRACT_INVENTORY_V1.md`** — generating, **per backlog story**, one **coordinated contract set**:
- **Implementation Contract** (what to build — per `IMPLEMENTATION_CONTRACT_SPECIFICATION_V1.md` / the Template),
- **QA Contract** (what to validate — per `QA_CONTRACT_SPECIFICATION_V1.md`),
- **Runtime Observability Contract** (what to observe — per `RUNTIME_OBSERVABILITY_CONTRACT_SPECIFICATION_V1.md`),
generated and consistency-checked per `CONTRACT_GENERATION_FRAMEWORK_V1.md`, each citing its **owning responsibility** (§3) as the producer. Presentation-epic sets may be generated immediately; cognition-owned sets upon ratification.

## 9. Conformance Rules

- **RP-1.** **No contract generation begins for cognition-owned items** (Advise/Intend/Evaluate-Reliability/Infer/Perceive/Adapt) **until ratification** (B-1).
- **RP-2.** **Presentation/UX contracts may proceed** where ownership is already clear (Disclose/Render — §3).
- **RP-3.** **No unresolved ownership may be hidden inside implementation** — any element not frozen in §3 or ratified in §4 is **Requires Owner Decision**, not an engineering default.
- **RP-4.** **No spec conflict may be resolved in code** — conflicts route to owner-ratified reconciliation (Scope Freeze §K).
- **RP-5.** Preserve all ratified Release 1 invariants (only-Adapt-changes-assessment; Recommendation-only-in-Finding-context; Confidence-never-health; stale-never-current; history append-only; Resolution-Paths presentation-only).

---

*This owner-ratification package converts the Cognitive Responsibility Architecture Specification into a concise owner decision before Release 1 Contract Inventory generation. It states what is being ratified (OSLO as a responsibility-primary architecture, with the validated set Perceive → Retain → Intend → Infer → Evaluate → Advise → Disclose → Act, Authority cross-cutting, Adapt emergent, Learn/Coordinate future, Render a service) and why now (contracts cannot trace to a producer until each cognition-owned capability has a documented owning responsibility). It freezes Release 1 ownership in a single table (each element marked Ratify-now / Already-consistent / Future / Requires-owner-decision), lists the seven blocking decisions before Contract Inventory (ratify the model; confirm Intend, Advise, Evaluate-Reliability, MRI-as-Disclose, Resolution-Paths-presentation-only, Authority-cross-cutting), separates the non-blocking/future decisions (Learn, Coordinate, multi-agent arbitration, engine catalogs, naming), presents three ratification options with their consequences for contract generation, and recommends Option B — Ratify with minor naming/scoping modifications, then proceed — sequenced with the GOV-ARCH architecture-representation review. It defines the post-ratification next step (RELEASE_1_CONTRACT_INVENTORY_V1, one coordinated Implementation/QA/Observability contract set per story, each citing its owning responsibility) and conformance rules (no cognition-owned contract before ratification; presentation contracts may proceed; no hidden ownership; no spec conflict resolved in code). It introduces no implementation and does not re-open the architecture debate.*

**OSLO Cognitive Responsibility Architecture Ratification Package v1 complete.**
