# OSLO Runtime Layer Reconciliation Decision 001

**Document Type:** Architecture Reconciliation Review (evidence-based; advisory — owner ratifies) · **Status:** **Pending Owner Decision** · **Date:** 2026-05-31
**Reviewed (repository evidence only):** `OSLO_ARCHITECTURE_BASELINE_V1.md` (§2 layer responsibilities, §3 workflow Stages 8–14, §5 capability inventory, §9 open questions) · `03_architecture/` (`runtime_architecture/`, `judgement_layer/`, `governance_layer/`, `components/`, `README.md`) · `01_governance/` · `CLAUDE.md` · Framework 001/001A · `RELEASE_1_RUNTIME_LAYER_OWNERSHIP_SPECIFICATION_V1.md` · `OSLO_DELIVERY_ARCHITECTURE_ALIGNMENT_SPECIFICATION_V1.md` · active Release 1 UX specs.

> **Mode & constraints.** Architecture reconciliation only — **no** APIs/schemas/databases/services/frameworks/vendors/prompts/models/infrastructure/implementation. **No inference of undocumented OSLO responsibilities without checking evidence.** Conflicts are **cited, not resolved**; absent evidence → **owner ratification required**. **Governing constraint (`CLAUDE.md`): "Only the repository owner may ratify, reject, supersede, or adopt canonical content"; "Do not introduce new doctrine"; "Do not resolve ontology conflicts unilaterally."** Therefore this document **evaluates and recommends; it does not ratify.** Any "Ratify" verdict below is a **recommendation to the owner.**

---

## 1. Repository Evidence Review

**Supports the reconciliation:**
- **The recommendation-ownership gap is real and documented.** Every layer's documented **non-responsibilities** disclaim recommendation generation: Reasoning "no recommendations"; Judgment "no remediation recommendations"; Governance "no recommendation"/"no execution"; Communication "no recommendation generation" (`OSLO_ARCHITECTURE_BASELINE_V1.md` §2). Yet recommendations are asserted to be produced (§3 Stage 12; §5 Recommendation Engine; Initiative I7). **No layer owns recommendation production** — confirmed in `RELEASE_1_RUNTIME_LAYER_OWNERSHIP_SPECIFICATION_V1.md` C-1.
- **Finding vs Issue is documented and distinct:** Reasoning produces **Findings** (descriptive, no severity); Judgment produces **Issues** (severity, confidence, epistemic state) (§2). The proposed object model preserves this distinction.
- **CAF and confidence are documented as Judgment/Scoring** (§3 Stage 10; §4). 
- **MRI is documented as a Planned stub** ("doctrinal scoping pending," RB-015/DL-034; §5) — i.e., no cognitive-layer ownership exists to preserve.

**Conflicts with the reconciliation:**
- **Documented workflow ordering (decisive).** §3 places **Stage 11 — Issues → Governance disposition** *before* **Stage 12 — Recommendation Generation** ("constrained by … Governance policy"). The proposed **linear** model `Judgment → Recommendation → Governance` places the Recommendation Layer **entirely before Governance**, contradicting the documented sequence in which **Governance disposes Issues first** and recommendation generation is **constrained by Governance**. This is a **genuine flow conflict** (C-FLOW).
- **Reliability is not documented as a Judgment responsibility.** The documented confidence drivers are Clarity/Alignment/Feasibility (+ evidence strength, assumption stability) (§4). "Reliability" as a first-class Judgment-owned signal is **undocumented** — assigning it is an **extension**, not a confirmation.
- **Clarification is Planned and unowned.** "Clarification Engine — Planned" (§5). Assigning it to a new Recommendation Layer is a **new responsibility assignment**, not documented today.
- **Architecture representation is under governance review.** §9 Q#20: "Surface B / native repository reconciliation … under governance review (GOV-ARCH-001/001A/000)." Reconciling against a representation that is **itself unsettled** is a documented risk.
- **Governance discipline (`CLAUDE.md`).** Introducing a new **Recommendation Layer** is introducing **new architecture/doctrine** — explicitly reserved to the owner ("Do not introduce new doctrine"; "Only the repository owner may … adopt canonical content").

## 2. Recommendation Layer Analysis

- **Is it justified?** **Yes, on evidence.** It fills a documented orphaned responsibility (recommendation production) that **no existing layer claims and several explicitly disclaim**. It is the minimal change that resolves C-1 without overloading an existing layer.
- **Does it violate documented layer responsibilities?** **Not the responsibility assignments** — it claims work no layer owns, and it does not remove any documented responsibility. **But it conflicts with the documented *flow*** (C-FLOW): the documented sequence is Issues→**Governance disposition**→Recommendation Generation (constrained by Governance), whereas the proposal inserts Recommendation **before** Governance. Adopting the layer therefore **requires reconciling the insertion point** with Stages 11–12 (e.g., Governance disposes Issues, Recommendation Layer generates constrained by Governance policy, Governance then governs recommendation exposure). The proposed simple linear ordering does **not** capture this.
- **Does it resolve the recommendation-ownership conflict?** **Yes — substantively**, provided (a) the flow placement is reconciled (C-FLOW) and (b) the owner ratifies the new layer (governance discipline). Bundling **Clarification Requests** and **alternative resolution paths** into it is **coherent** but adds **undocumented** responsibilities (owner decision).

## 3. Runtime Object Reconciliation

| Object | Proposed definition | Evidence | Assessment |
|---|---|---|---|
| **Finding** | descriptive weakness produced by Reasoning | §2 Reasoning (Findings, descriptive) | **Confirmed** — matches documented Reasoning output |
| **Issue** | judged Finding with severity, confidence, CAF, **reliability**, epistemic state | §2 Judgment (severity/confidence/epistemic); CAF §4 | **Mostly Confirmed**; **"reliability" is an extension** (not documented as Judgment's) — owner decision |
| **Recommendation** | advisory response for a Finding/Issue | gap C-1; §3 Stage 12 (anchored to Issues) | **Resolves gap**; note §3 anchors recommendations to **Issues**, the proposal says "Finding or Issue" — minor scope widening to flag |
| **Clarification Request** | advisory request to improve understanding | §5 Clarification Engine: **Planned** | **Plausible**, but **unowned today** — new assignment, owner decision |

The object model **preserves the documented Finding↔Issue distinction** (resolving the C-2 terminology conflict at the runtime level), which is its strongest merit.

## 4. Release 1 Gap Resolution Assessment

| Gap | Proposed resolution | Repository-evidence verdict |
|---|---|---|
| **Recommendation production** | New Recommendation Layer owns it | **Resolves** the conflict in principle; requires **flow reconciliation (C-FLOW)** + **owner ratification** (new layer = new doctrine) |
| **Reliability ownership** | Reliability → Judgment | **Coherent extension**; **not documented** today → **owner ratification required** (do not infer) |
| **Clarification ownership** | Recommendation Layer produces; Governance governs | **Coherent if the layer is adopted**; Clarification is **Planned/unowned** → **owner decision** |
| **MRI ownership** (Question D) | MRI = **Communication-layer diagnostic experience** rendering governed Reasoning/Judgment outputs, **not** its own cognitive layer | **Strongly supported.** MRI is a Planned stub; the Release 1 UX already reconciled MRI as a **visualization/diagnostic experience** consuming CAF/Reliability/Confidence (MRI umbrella). Treating it as **Communication rendering, not a cognitive layer, preserves doctrine** and resolves G-2. **Recommend ratification** (with owner confirmation). |
| **Finding vs Issue terminology** (Question E) | UX **Finding Panel** = presentation construct that may contain Finding + Issue assessment + Recommendation content, **preserving runtime distinction** | **Strongly supported.** Consistent with the ratified UX classification doctrine (panels are presentation constructs over objects). **Resolves C-2 at the UX level without collapsing runtime objects. Recommend ratification.** |

**Question B (Reliability → Judgment):** coherent but an **extension** → owner ratification. **Question C (Clarification → Recommendation Layer, governed by Governance):** coherent **only if** the Recommendation Layer is ratified; Clarification remains Planned → owner decision.

## 5. Architectural Risks (introduced by the reconciliation)

- **R-1 Flow inconsistency (C-FLOW).** The linear `Judgment → Recommendation → Governance` contradicts documented Stages 11–12 (Governance disposes Issues before recommendation generation). Adopting without reconciling the insertion point creates a workflow contradiction.
- **R-2 Reconciling against an unsettled representation.** GOV-ARCH-001/001A/000 (architecture representation) is **under governance review** (§9 Q#20); inserting a layer now risks rework if the representation changes.
- **R-3 New-doctrine governance breach if adopted unilaterally.** A new layer is owner-ratifiable doctrine; AI adoption would violate `CLAUDE.md`.
- **R-4 Responsibility creep.** Bundling Recommendations + Clarifications + alternative resolution paths + rationale into one new layer assigns **multiple currently-unowned/Planned** responsibilities at once — larger surface than the minimal fix (recommendation production alone).
- **R-5 Reliability extension.** Placing Reliability in Judgment without doctrinal basis risks terminology drift if Reliability's relationship to the documented drivers is not first defined.
- **R-6 Object scope widening.** "Recommendation for a Finding **or** Issue" widens the documented "anchored to Issues"; and Issue gaining "reliability" extends Judgment — both small but real ontology changes.

## 6. Required Owner Decisions

1. **Ratify the Recommendation Layer?** (new layer = new doctrine — owner only.)
2. **Reconcile its flow placement** with documented Stages 11–12 (Governance disposition of Issues vs. Recommendation-before-Governance) — **C-FLOW must be resolved.**
3. **Reliability → Judgment** (extension): ratify and define Reliability's relationship to the documented drivers.
4. **Clarification ownership** (Planned → Recommendation Layer?): ratify or keep deferred.
5. **Object model extensions:** Issue gains "reliability"; Recommendation anchors to "Finding or Issue" (vs documented "Issues").
6. **MRI as Communication diagnostic** (Question D): confirm (well-supported).
7. **Finding Panel as presentation construct** (Question E): confirm (well-supported).
8. **Resolve GOV-ARCH-001/001A/000** (authoritative architecture representation) **before** binding the layer change.

## 7. Final Recommendation

**RATIFY WITH MODIFICATIONS — as a recommendation to the owner (owner ratification required; this document does not and cannot ratify).**

**Rationale (repository-evidence-based):** The reconciliation targets a **real, documented gap** (recommendation production is owned by no layer and disclaimed by all), and its **object model preserves OSLO's documented Finding↔Issue distinction** rather than collapsing it. **Questions D (MRI as a Communication-layer diagnostic) and E (Finding Panel as a presentation construct)** are **well-supported by existing evidence** and resolve the MRI and terminology gaps **without introducing new cognition** — these are recommended for ratification with high confidence.

**The modifications/conditions that make it ratifiable:**
- **M-1 (mandatory):** Resolve **C-FLOW** — define the Recommendation Layer's placement consistently with documented Stages 11–12 (Governance disposes Issues; recommendations generated **constrained by** Governance; Governance governs recommendation exposure). The simple linear ordering as drawn is **not** ratifiable as-is.
- **M-2:** Treat **Reliability→Judgment** and **Clarification→Recommendation Layer** as **owner-ratified extensions** (currently undocumented/Planned) — adopt explicitly, do not infer.
- **M-3:** Scope the new layer to its **minimal justified responsibility (recommendation production)** first; bundle Clarification/alternative-paths/rationale only by explicit owner decision (R-4).
- **M-4:** Sequence the change **after** owner resolution of **GOV-ARCH-001/001A/000** (R-2), since the architecture representation is under review.
- **M-5:** Define Reliability's relationship to the documented confidence drivers before binding it to Judgment (R-5).

**Why not "Ratify As Proposed":** the proposed linear flow **conflicts with documented Stages 11–12** (C-FLOW), several bindings are **extensions of undocumented/Planned responsibilities**, and unilateral adoption of a new layer would **violate the governance discipline** (`CLAUDE.md`). **Why not "Do Not Ratify":** the core change is **evidence-justified and minimal**, preserves OSLO's documented object distinctions and doctrine, and Questions D/E are clearly supportable — outright rejection would leave the documented recommendation-ownership gap unresolved.

**Net:** the reconciliation **can** resolve the Release 1 ownership gaps while preserving OSLO doctrine **if** the owner ratifies it with the modifications above — chiefly fixing the flow placement (M-1), adopting the extensions explicitly (M-2/M-5), keeping the first step minimal (M-3), and sequencing it after the architecture-representation review (M-4).

---

*This evidence-based reconciliation review evaluates a proposed OSLO Recommendation Layer and associated object-model/ownership reconciliations against the documented runtime architecture. It confirms the recommendation-ownership gap is real (every documented layer disclaims recommendation generation), that the Finding↔Issue distinction is documented and preserved by the proposed object model, and that treating MRI as a Communication-layer diagnostic (Q-D) and the Finding Panel as a presentation construct over runtime objects (Q-E) are well-supported and recommended. It flags a decisive flow conflict — the documented workflow disposes Issues through Governance (Stage 11) before recommendation generation (Stage 12, constrained by Governance), contradicting the proposed Judgment→Recommendation→Governance ordering — and notes that Reliability→Judgment and Clarification→Recommendation are undocumented extensions, that the architecture representation is under governance review (GOV-ARCH-001/001A/000), and that introducing a new layer is owner-ratifiable doctrine (CLAUDE.md). It records six architectural risks and eight required owner decisions, and recommends Ratify With Modifications — explicitly as advice requiring owner ratification, conditioned on resolving the flow placement, adopting extensions explicitly, keeping the first step minimal, and sequencing after the architecture-representation review. It infers no responsibility, resolves no conflict unilaterally, creates nothing canonical, and proposes no implementation.*

**OSLO Runtime Layer Reconciliation Decision 001 complete.**
