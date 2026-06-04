# OSLO Cognitive Engine Architecture Review 001

**Document Type:** Architecture Review (evidence-based reconciliation; advisory — owner ratifies) · **Status:** **Pending Owner Decision** · **Date:** 2026-05-31
**Reviews / builds on:** `OSLO_RUNTIME_LAYER_RECONCILIATION_DECISION_001.md` · `OSLO_RUNTIME_RECOMMENDATION_OWNERSHIP_REVIEW_001.md`. **Evidence:** `OSLO_ARCHITECTURE_BASELINE_V1.md` (§1 doctrine framing, §2 layer responsibilities + "strict separation of concerns / single responsibility," §3 Stages 11–12, **§5 capability inventory — which already names "Recommendation Engine," "Clarification Engine," "Policy Engine," "Governance Decision Matrix"**) · `01_governance/` · `CLAUDE.md` · `RELEASE_1_RUNTIME_LAYER_OWNERSHIP_SPECIFICATION_V1.md` · ratified UX decisions (`RECOMMENDATION_RESOLUTION_PATHS_RECONCILIATION_DECISION_001.md`, AMB-1 Option A; `MRI_TERMINOLOGY_RECONCILIATION_DECISION_001.md`).

> **Constraints.** Repository evidence first; no inference of undocumented responsibilities; proposed extensions labeled as such; evaluate architecture **as a system** against documented **intent**, not documentation alone. **Per `CLAUDE.md`, only the owner ratifies/adopts canonical content** — every "Ratify" here is a recommendation to the owner.

---

## 0. Key Evidence Finding (frames the whole review)

The repository **already uses "Engine" to name cognitive capabilities within layers**: §5 names a **Recommendation Engine**, **Clarification Engine**, **Policy Engine**, **Governance Decision Matrix**; §2 shows each layer performing **multiple capabilities** (Reasoning = structural + consistency + feasibility + AI-assisted inference; Judgment = severity + confidence + epistemic; Governance = exposure + authorization + resolution). **OSLO has therefore *already* been implicitly treating layers as containers of multiple capabilities ("engines").** Option C does not invent this pattern — it **formalizes and names** it, and makes the **single-responsibility** principle apply at the **engine** granularity. This is the strongest evidence for Option C and reframes the central question.

## 1. Architectural Assessment (A vs B vs C)

| | Option A — Recommendation **Layer** | Option B — **Governance-owned** Engine | Option C — **Cognitive Engines** |
|---|---|---|---|
| Resolves recommendation-ownership gap | Yes | Yes | Yes |
| Keeps generation in **cognition** (not authority) | **Yes** | **No — violates Governance "no recommendation generation"** | **Yes** |
| Honors Stage 11→12 governed sequence | No (linear, generation before Governance) | Yes | Yes (engine governed by Governance) |
| Separation of concerns | Coarse (layer = many things) | **Violated** (Governance = authority **and** generation) | **Best** (engine = single capability) |
| Structural disruption | High (new top-level peer layer) | Low count, but doctrinal breach | **Low–Med** (formalizes existing implicit pattern) |
| New doctrine | Yes (new layer) | Yes (Governance gains generation) | **Clarification + minimal formalization** |

**Option B is doctrinally disqualified** (Governance generating contradicts its documented non-responsibility and the separation principle — established in `OSLO_RUNTIME_RECOMMENDATION_OWNERSHIP_REVIEW_001.md`). **Option A** is sound on ownership-tier but heavy (new peer layer) and mis-orders generation. **Option C** is the most faithful to "single responsibility" and formalizes an already-implicit pattern — **best of the three**, with caveats (§3).

## 2. Separation-of-Concerns Analysis

OSLO doctrine (§1/§2): layers separate *what is known / implied / judged / **allowed** / explained*; **each layer has a single responsibility.** In practice each layer already performs several capabilities, so "single responsibility" is most coherently read as **single cognitive *role* per layer, single capability per engine.** Option C makes this explicit: **Layers = where cognition occurs (role); Engines = what cognitive capability is performed.** This **strengthens** separation of concerns rather than diluting it, and — critically — keeps **generation in cognition** and **authority in Governance** (Option C's Exposure/Authorization engines stay in Governance; Recommendation/Clarification engines stay in cognition). **Option C best preserves the doctrine.**

## 3. Cognitive Engine Assessment (should it be formal?) — with caveats

**Yes — formalizing Cognitive Engines as a named architectural concept is justified** (it names an existing implicit pattern and gives the single-responsibility principle a precise unit). **But three evidence-based caveats constrain it:**

- **Caveat 1 — placement is reframed, not eliminated.** If engines reside **within layers**, the Recommendation/Clarification/Resolution engines need a host. They **cannot** sit in Reasoning or Judgment (both **disclaim** recommendation generation) or in Governance (authority, not generation). So Option C still requires the owner to recognize a **generative-advisory cognition responsibility** (host) positioned **after Judgment**, governed by Governance — whether named a "Layer" or a "cognition grouping." Option C **reframes** the layer-vs-grouping question productively but does **not** make it disappear.
- **Caveat 2 — Resolution Path Engine conflicts with a ratified UX decision.** Release 1 **ratified (AMB-1, Decision A)** that **"Possible Resolution Paths" is a presentation pattern over multiple Recommendations — NOT a runtime object.** A runtime **"Resolution Path Engine" that generates Resolution-Path objects would contradict that ratification.** Permissible reading: the **Recommendation Engine produces multiple Recommendations**, which Communication renders as "Possible Resolution Paths." A separate object-producing "Resolution Path Engine" must **not** be introduced. **Conflict — flag.**
- **Caveat 3 — taxonomy discipline.** Naming every capability an "engine" risks taxonomy bloat. Formalization should define **what qualifies as an engine** (a single, governable cognitive capability) to prevent proliferation, and should be sequenced **after GOV-ARCH-001/001A/000** (architecture representation under review).

## 4. Release 1 Impact Assessment (Q6 mapping)

| Release 1 concept | Cognitive Engine mapping | Status |
|---|---|---|
| **Findings** | Reasoning Layer · Gap/Alignment/Traceability/Feasibility engines | **Confirmed** (documented finding types) |
| **Issues** | Judgment Layer · Issue-formulation + Severity + Epistemic engines | **Confirmed** |
| **CAF** | Judgment Layer · Clarity/Alignment/Feasibility scoring engines | **Confirmed** (Stage 10) |
| **Confidence** | Judgment Layer · Outcome-Confidence engine | **Confirmed** (Doctrine 06) |
| **Reliability** | Judgment Layer · Reliability engine | **Proposed extension** (not documented as Judgment's) — owner decision |
| **Recommendations** | **Recommendation Engine** (generative-advisory cognition; **governed by** Governance) | **Resolves gap** |
| **Clarifications** | **Clarification Engine** (generative-advisory cognition; distinct construct) | **Resolves gap** (Planned today → extension) |
| **Resolution Paths** | **No object-producing engine.** Recommendation Engine emits **multiple Recommendations**; "Possible Resolution Paths" = Communication presentation | **Conflict if an object engine is added** (AMB-1) — constrain |
| **MRI** | Communication Layer · diagnostic rendering of governed Reasoning/Judgment outputs (no cognitive engine) | **Confirmed direction** (Decision 001 Q-D) |
| **Companion** | Communication Layer · presentation surface | **Confirmed** (render) |
| **Finding Panel** | Communication Layer · presentation construct over Finding + Issue + Recommendation (runtime distinctions preserved) | **Confirmed** (Decision 001 Q-E) |
| **Recommendation Panel** | Communication Layer · presentation construct over Recommendation Engine outputs | **Resolved** (now has a documented producer) |

**Net:** Cognitive Engines resolve **Recommendation, Clarification, MRI, and Finding/Issue** ownership; **Reliability** is a proposed extension; **Resolution Paths** must remain presentation-only (constraint, not a new engine).

## 5. Evolution Path

1. **Formalize the Layer/Engine distinction** as an OSLO architectural **clarification**: Layers = cognitive role / where; Engines = single capability / what. (Names the existing implicit pattern; defines engine-qualification to prevent bloat.)
2. **Recognize a generative-advisory cognition responsibility** hosting the **Recommendation Engine** and **Clarification Engine**, positioned **after Judgment**, **constrained and exposed by Governance** (cognition generates; Governance governs). Owner decides whether the host is a named Layer or a cognition grouping.
3. **Constrain Resolution Paths** to presentation-only (Recommendation Engine emits multiple Recommendations; no Resolution-Path object) — preserve AMB-1.
4. **Treat Reliability** (Judgment engine) and **Clarification** (Planned) as **explicit proposed extensions** requiring ratification.
5. **Confirm** MRI-as-Communication-diagnostic and panels-as-presentation-constructs (well-supported).
6. **Sequence after GOV-ARCH-001/001A/000**; this is an **architecture clarification + minimal doctrinal formalization**, owner-ratifiable.

## Review Questions

- **Q1 — Does Option C better preserve original intent than A/B?** **Yes.** It keeps generation in cognition (beats B, which violates Governance's documented non-responsibility), avoids a heavyweight new peer layer (lighter than A), honors Stage 11→12 (engine governed by Governance), and **formalizes an already-implicit, documented pattern** (engines named in §5). It is the most faithful to "single responsibility."
- **Q2 — Distinguish Architectural Layers from Cognitive Engines?** **Yes.** The repository already conflates them implicitly (layers contain multiple named capabilities/engines). Making them **distinct concepts — Layers = where cognition occurs; Engines = what capability** — clarifies single-responsibility and is the central, justified move.
- **Q3 — Less disruption than a new Recommendation Layer?** **Yes, on the structural axis** — it adds **no top-level peer layer** and names existing capabilities; but **it does not eliminate** the placement decision for the generative-advisory engines (Caveat 1), so it is "less structural disruption, equal conceptual decision."
- **Q4 — Resolves Recommendation/Clarification/Resolution ownership without violating "Governance = what is allowed" or "single responsibility"?** **Recommendation and Clarification: yes** (cognition-owned engines, Governance-governed; each a single capability → strengthens both principles). **Resolution paths: only if** they remain **presentation-only** (no object engine) — an object-producing Resolution Path Engine would violate the ratified AMB-1 decision (not the doctrine per se, but a ratified Release 1 decision).
- **Q5 — Where should engines reside?** **Within layers, as the unit of single-responsibility** (a Layer = a set of engines sharing a cognitive role). The generative-advisory engines (Recommendation/Clarification) reside in a **recognized cognition responsibility after Judgment** (host = Layer or grouping, owner's call), **governed by** Governance's Exposure/Authorization engines. **Not** a separate plane (that would over-detach cognition); **not** "between layers" as free-floating (breaks single-host clarity). **Engines-within-a-cognitive-role** is the most coherent model.
- **Q6 — Release 1 mapping:** §4 table.
- **Q7 — Classify the change:** **Architecture *clarification* + minimal new *doctrine* (formalization).** The **existence** of engines/capabilities is **documented** (clarification); **formally elevating "Cognitive Engine" to a named architectural concept with the Layer/Engine distinction** is a **minimal doctrinal addition** (owner-ratifiable). It is **not** "no change" and **not** a heavy "architecture modification" (no peer layer, no responsibility moved between layers).

## 6. Final Verdict

**RATIFY MODIFIED OPTION C** *(formalize Cognitive Engines; recommendation/clarification become cognition-owned, Governance-governed engines)* — **as a recommendation requiring owner ratification.**

**Modifications/conditions:**
- **M-1:** Adopt **Layers = where cognition occurs; Engines = what cognitive capability** as a formal clarification; define **engine-qualification** (single governable cognitive capability) to prevent taxonomy bloat.
- **M-2:** **Recommendation & Clarification engines are cognition-owned, Governance-governed** (reject Option B's Governance-generation framing).
- **M-3:** **No Resolution-Path object engine** — the Recommendation Engine emits multiple Recommendations; "Possible Resolution Paths" stays presentation-only (preserve AMB-1).
- **M-4:** **Reliability engine (Judgment)** and **Clarification engine** are **explicit proposed extensions** (undocumented/Planned) — adopt by owner decision, do not infer.
- **M-5:** Owner decides the **host** of the generative-advisory engines (named Layer vs cognition grouping) — Option C reframes but does not remove this decision.
- **M-6:** Confirm **MRI-as-Communication-diagnostic** and **panels-as-presentation-constructs**; **sequence after GOV-ARCH-001/001A/000**.

**Why Modified C over A:** C resolves the gaps with **finer single-responsibility** and **without a heavyweight new peer layer**, formalizing an existing pattern. **Why over B:** B violates Governance's documented non-responsibility and the separation doctrine. **Why "Modified":** Option C as drawn implies a stand-alone "Resolution Path Engine" (conflicts with AMB-1) and leaves the engine-host placement and Reliability/Clarification extensions undeclared — the modifications close these gaps. **Why not Reject:** the gap is real and C is the most doctrinally-coherent, least-disruptive resolution available on the evidence.

---

*This review evaluates resolving OSLO's recommendation-ownership gap via a new Recommendation Layer (A), a Governance-owned engine (B), or a formal Cognitive Engines concept (C). It establishes that OSLO already implicitly treats layers as containers of named capabilities/"engines" (Recommendation Engine, Clarification Engine, Policy Engine — baseline §5), so Option C formalizes an existing pattern rather than inventing one, and best preserves the documented "single responsibility" doctrine by making Engines the single-capability unit and Layers the cognitive-role unit (Layers = where; Engines = what). It disqualifies Option B (Governance generating recommendations violates Governance's documented non-responsibility and the separation principle) and finds Option A heavier and mis-ordered. It flags two evidence-based caveats — the generative-advisory engines still require a recognized cognition host after Judgment (placement reframed, not eliminated), and a runtime "Resolution Path Engine" would contradict the ratified AMB-1 decision that Possible Resolution Paths are presentation-only — and maps all Release 1 concepts into the engine model (Findings→Reasoning engines; Issues/CAF/Confidence→Judgment engines; Recommendations/Clarifications→cognition-owned, Governance-governed engines; Reliability→proposed Judgment engine; MRI→Communication diagnostic; panels→presentation constructs). It classifies the change as architecture clarification plus minimal doctrinal formalization and recommends Ratify Modified Option C — advisory, owner ratification required — conditioned on the Layer/Engine formalization, cognition-owned generation, no Resolution-Path object, explicit treatment of the Reliability/Clarification extensions, the host-placement decision, and sequencing after the GOV-ARCH architecture review. It infers no undocumented responsibility, labels every extension, resolves no conflict unilaterally, and proposes no implementation.*

**OSLO Cognitive Engine Architecture Review 001 complete.**
