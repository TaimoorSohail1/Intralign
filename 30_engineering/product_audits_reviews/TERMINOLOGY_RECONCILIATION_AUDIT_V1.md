# Terminology Reconciliation Audit v1

**Document:** TERMINOLOGY_RECONCILIATION_AUDIT_V1.md
**Type:** Read-only terminology review (analysis only)
**Reviewed (authoritative, unmodified):** CAF Assessment · CAF Scoring · Reliability · Confidence · MRI · Overlay · Finding · Recommendation · Resolution Candidate · Review Request · Disposition · Governance · Accepted Understanding · Model Lineage Index · Model Coverage Audit
**Date:** 2026-05-31

> **Architecture V1 note (added by the Architecture V1 Simplification Refactor).** Per the founder decision, the Governance Domain is **Future Architecture**. The terminology collisions analyzed here — chiefly *Accepted / Acceptance*, *Governed vs Accepted Understanding*, and the governance sense of *Outcome* — therefore sit in **Future Scope**: they are **not on the Architecture V1 critical path** and **do not block V1 implementation.** All findings below are **preserved unchanged** and apply when governance is activated for Outcome Orchestration / Agent Governance.

> **Constraints honored.** No model was modified, no doctrine introduced, no new model proposed, no definition created, and no terminology dispute resolved. This audit only **identifies and analyzes** terminology collisions, ambiguities, synonym drift, overloaded terms, and unresolved vocabulary relationships. Every observation is drawn from the existing documents. Non-normative.

---

## 1. Terminology Inventory

Major architecture terms, originating model, role, and concise definition (as used in the documents).

| Term | Originating model | Role | Concise definition (as used) |
|---|---|---|---|
| Understanding | CAF Assessment | Subject | OSLO's interpretation of project reality |
| Integrity (of understanding) | CAF Assessment | What CAF assesses | The degree to which understanding is justified by evidence |
| Evidence | CAF Assessment | Input | Information contributing to understanding |
| Inference | CAF Assessment | Characteristic | Understanding synthesized rather than directly evidenced |
| Finding | CAF Assessment + Finding | Object | An observation about understanding relevant to integrity; a governable object |
| Impact Assessment | CAF Assessment | Mechanism | Evaluates a finding's significance, affected dimensions, evidence support, scope |
| CAF (Clarity / Alignment / Feasibility) | CAF Assessment | Assessment | The three independent dimensions of understanding integrity |
| Finding Type / Taxonomy | CAF Assessment | Classification | Flat, seven-type categorization of findings |
| Coverage / Coverage Gap | CAF Assessment + Reliability | Finding type / Reliability input | Completeness of the observable evidence surface |
| Integrity Index / State Band / Reliability Qualifier | CAF Scoring | Representation | The per-dimension CAF score triple |
| Strengthening / Reducing Contribution | CAF Scoring | Effect | Evidence raises; findings lower; the index |
| Calibration | CAF Scoring | Deferral | Externalized numeric weights/thresholds/arithmetic |
| Assessment Reliability / Reliability | Reliability | Signal | Trustworthiness/supportability of the CAF assessment |
| Evidence Availability / Assessability | Reliability | Inputs | Two of Reliability's three inputs (with Coverage) |
| Supportability | Reliability | What Reliability measures | How well the assessment is supported by observable evidence |
| Outcome Confidence / Confidence | Confidence | Signal | Summarized, reliability-qualified trust in understanding |
| Constrained Aggregation | Confidence | Mechanism | How CAF dimensions combine without averaging or weakest-link domination |
| MRI | MRI | Surface | Visualization that makes understanding observable |
| Overlay | Overlay | Surface | Attention lens applied to MRI |
| Recommendation | Recommendation | Object | Prescriptive advisory suggestion to improve understanding |
| User Action | Recommendation | External step | The human act that alone changes understanding |
| Assessment Context | Recommendation + Resolution Candidate | Input bundle | Findings + CAF + Reliability + Confidence |
| Resolution Candidate | Resolution Candidate | Governance object | A proposed resolution to a Finding |
| Governance Context | Review Request | Input bundle | Findings + Resolution Candidates + assessment context + ownership info |
| Human Evaluation | (external) | External step | Human evaluation between Review Request and Disposition |
| Review Request | Review Request | Governance object | A request for evaluation of Resolution Candidate(s) |
| Disposition | Disposition | Governance object | A durable record of an evaluation outcome |
| Governance | Governance | Domain / Model | The acceptance layer; also the name of the domain |
| Acceptance | Governance | Act | Determining whether understanding may be accepted |
| Accepted Understanding | Accepted Understanding | Object | The durable, governed output of Governance |
| Governed Understanding | Resolution Candidate | Bridge phrase | Target of the Resolution Candidate "bridge"; not formally defined |
| Ownership / Ownership Information | Finding + Review Request | Attribute / input | Responsibility for a Finding; governance-context input |
| Basis / Rationale / Justification | Cross-cutting | Traceability | The grounds an object/signal is explained by |
| History / Supersession / Reconsideration | Cross-cutting | Lifecycle | History preservation and replacement concepts |
| Knowledge Layer | (future) | Frontier | Undefined destination beyond Accepted Understanding |

---

## 2. Overloaded Terms

| Term | Usages | Meanings | Collision risk |
|---|---|---|---|
| **Accepted** | (a) Disposition conceptual outcome "Accepted"; (b) Recommendation outcome "accepted"; (c) Resolution Candidate outcome "accepted"; (d) Governance "acceptance" → **Accepted Understanding** | (a–c) a user/evaluation accepting a proposal or recommendation; (d) Governance accepting *understanding* | **High** — the same word marks an evaluation-level outcome **and** the flagship governance result; a Disposition of "Accepted" is not the same as "Accepted Understanding" |
| **Acceptance** | Governance "governs acceptance"; Recommendation "may be accepted" | Governance act of accepting understanding vs a user accepting a recommendation | **High** — central governance act shares the word with a user choice |
| **Understanding** | "project understanding," "understanding integrity," "Accepted Understanding," "Governed Understanding," "understanding-improvement loop" | Base concept vs qualified states (assessed / governed / accepted) | **Medium** — the assessed-vs-governed distinction is explicit, but unqualified "understanding" is pervasive |
| **Governance** | (a) the Governance Domain; (b) the Governance Model; (c) "governance object"; (d) "governance context"; (e) "governance history" | Domain vs single model vs adjective | **Medium** — the Governance **Model** is one model *within* the Governance **Domain** while sharing the name |
| **Reliability** | CAF Scoring "reliability qualifier" (per-dimension, coverage-governed); Reliability Model "Assessment Reliability" (assessment-level, three inputs) | Per-dimension qualifier vs assessment-level supportability signal | **Medium** — same word at two granularities; partly reconciled by Reliability §8 |
| **Confidence** | Confidence Model "Outcome Confidence"; CAF Assessment/Reliability generic "confidence in the integrity"; future "Assessment Confidence"; future "recommendation confidence" | The formal signal vs generic confidence vs two future named confidences | **Medium-High** — a flagship signal name shares the word with generic usage and two anticipated future terms |
| **Resolution** | Resolution Candidate "proposed resolution"; Finding lifecycle "resolve / resolved" | A governance proposal vs a Finding reaching a resolved state | **Medium-High** — both concern a Finding being addressed; one is a proposal object, one is a lifecycle state |
| **Outcome** | Confidence "**Outcome** Confidence"; Disposition "evaluation **outcome** / recorded outcome"; Governance "governance outcome" | Project-outcome-adjacent (in the Confidence name) vs the result of a governance step | **High** — a flagship term anchors "outcome" to project achievement, while governance uses "outcome" to mean step-result |
| **Context** | "assessment context"; "governance context" (which is defined to *include* assessment context) | Two layered input bundles | **Low-Medium** — coherent nesting, but the reused word plus the containment relationship can confuse |

---

## 3. Synonym Drift Analysis

| Candidate pair | Where used | Assessment |
|---|---|---|
| **Governed Understanding** vs **Accepted Understanding** | "Governed Understanding": Resolution Candidate (and its index entry, as a bridge target). "Accepted Understanding": Governance & Accepted Understanding Models (the formal output object). | **Unresolved.** Never cross-defined. They may be synonyms (understanding that has passed through governance) or distinct (any understanding *under* governance vs specifically *accepted* understanding). The architectural endpoint deserves one term; today it has two. |
| **Supportability** vs **Evidence Support** | "Supportability": Reliability (what Reliability measures). "Evidence Support": CAF Assessment Impact Assessment factor. | **Closely related, not identical.** Both concern evidence backing, but Reliability's supportability is assessment-level while Impact Assessment's Evidence Support qualifies a single finding. Distinct as defined; drift risk if conflated. |
| **Evaluation** vs **Review** | Review Request "requests **evaluation**"; the external step is "Human **Evaluation**"; the model is named "**Review** Request." | **Mild drift.** The "Review" Request requests "evaluation," and the external step is "Human Evaluation," not "Human Review." The name and the activity use different roots. |
| **Recorded outcome** / **evaluation outcome** / **governance outcome** / **accepted-understanding outcome** | Disposition, Governance, Accepted Understanding explanation models | **Overlapping phrasings** of "the result of a step." Each is scoped to its object, but the shared "outcome" head reuses §2's overloaded term. |
| **Justified** vs **Rationale** | "Justified by evidence" (CAF Assessment / Confidence epistemology); "rationale" (every governance explanation model) | **Distinct but adjacent.** "Justified" is epistemic warrant; "rationale" is the explanatory reason given. Consistent today; conflation possible. |

*(Assessment only; not resolved.)*

---

## 4. Domain Boundary Vocabulary

Terms operating at the Understanding ↔ Governance boundary, evaluated for blur:

- **assessment vs acceptance** — *conceptually* clearly separated (Governance Model: "assessment and acceptance are separate responsibilities"). *Lexically* blurred by the "Accepted/Acceptance" overload (§2) and by "outcome" appearing on both sides.
- **governance** — blurs at the boundary because it names both the **domain** and one **model** in it (§2). A reader at the boundary cannot tell from the word alone whether "Governance" means the domain or the acceptance layer.
- **recommendation vs resolution (candidate)** — the **thinnest boundary** in the architecture (also flagged by the Coverage Audit). Both are downstream-of-assessment objects that operate on Findings and propose a way forward; the distinction is *orientation* (improvement vs governance), not vocabulary. Lexically, "suggest a path" (Recommendation) and "propose a resolution" (Resolution Candidate) are near-synonyms.
- **disposition vs resolution** — Disposition *records an outcome*; Resolution Candidate *proposes a resolution*. Different roles, but both are governance objects "about how a Finding is handled," and both orbit the overloaded "resolution/outcome" cluster.
- **Finding (the shared term)** — intentionally straddles both domains (assessment input *and* the actionable object governance consumes). This is a *designed* boundary term, not a blur — but it means "Finding" is the one term that must read identically on both sides.

The boundary's conceptual separation is sound; the **vocabulary** at the boundary is where the blur concentrates (acceptance/outcome/resolution).

---

## 5. Lifecycle Vocabulary Review

Lifecycle verbs across the seven object/layer models:

| Concept | Finding | Recommendation | Resolution Candidate | Review Request | Disposition | Governance | Accepted Understanding |
|---|---|---|---|---|---|---|---|
| Come into being | appear | generation | appear / generation | creation | recording | establishment | establishment |
| Change | change | change | change | change | change | change | change |
| Cease / end / inactive | disappear | retire | withdraw / disappear | withdraw / close | become historical | (superseded) | (superseded) |
| Replace | (reopen) | reappear | supersede | supersede | supersede | supersede | supersede |
| Outcome words | resolve/reopen | accepted/rejected/deferred/ignored | accepted/rejected/superseded/withdrawn/unresolved | fulfilled/withdrawn/superseded/closed/open | Accepted/Rejected/Deferred/Superseded | establish/reconsider/supersede | establish/reconsider/supersede |

**Reused words (consistent — low risk):** **change**, **supersede/supersession** (uniform meaning everywhere — a newer one replaces, prior retained), **reconsideration** (Governance & Accepted Understanding only), **history/historical retention** (uniform).

**Inconsistencies / confusion risk:**
- **"Ending" verbs proliferate.** The single concept "object no longer active/current" is expressed as **disappear, retire, withdraw, close, become historical** across objects — five different verbs for one idea. *Medium* confusion risk.
- **"Creation" verbs vary** — appear / generation / creation / recording / establishment for one idea. *Low-Medium.*
- **Outcome words collide with §2.** **Accepted / Rejected / Deferred / Superseded** recur as conceptual outcomes across Recommendation, Resolution Candidate, and Disposition — directly compounding the **"Accepted"** overload. *Medium-High.*
- **"Superseded" is both an event and an outcome** — a lifecycle event ("one supersedes another") and a named outcome (Resolution Candidate / Disposition). Minor.
- **"Resolve" (Finding) vs "fulfilled" (Review Request) vs "accepted" (Governance)** — three different "reached completion" verbs, some intentionally distinct in meaning.

---

## 6. Traceability Vocabulary Review

Terms for explainability, basis, rationale, justification, lineage, history:

- **Explainable / Explanation Model** — every model carries an "Explanation Model" and asserts it is "explainable." **Uniform — the strongest-consistency vocabulary in the set.**
- **Basis** — "traceable to its basis," "never appear disconnected from their basis," "reduces to a basis, not a formula." Used identically across all models. **Uniform.**
- **Rationale** — "rationale for candidate generation / evaluation request / governance rationale." Consistent governance-explanation usage. **Stable.**
- **Justified / Justification** — "understanding justified by available evidence" (CAF Assessment, Confidence). **Distinct from "rationale":** justification is the epistemic warrant of an assessment; rationale is the reason cited in an explanation. Not interchangeable; consistent today but a drift candidate if "justification" leaks into governance explanations or vice-versa.
- **Lineage** — appears in the **Coverage Audit** ("audit lineage") and the index, not in the model bodies; the models say "traceable to basis." Minor surface inconsistency between "lineage" (audit term) and "basis/traceability" (model term).
- **History** — "preserves history," "governance history," "historical retention." **Uniform** across Finding, Disposition, Governance, Accepted Understanding.

**Net:** traceability vocabulary is the healthiest cluster. The only watch-item is keeping **justification** (epistemic) separate from **rationale** (explanatory), and recognizing **lineage** as an audit-layer synonym for the models' **basis/traceability**.

---

## 7. Architectural Risk Assessment

Risk classified solely by future ambiguity potential.

| # | Terminology issue | Risk |
|---|---|---|
| 1 | **"Accepted" / "Acceptance"** overload (evaluation outcome vs governance result / Accepted Understanding) | **High** |
| 2 | **"Governed Understanding" vs "Accepted Understanding"** unresolved synonym at the architectural endpoint | **High** |
| 3 | **"Outcome"** overload ("Outcome Confidence" vs evaluation/governance outcome) | **High** |
| 4 | **"Resolution"** (governance proposal vs Finding "resolved" state) | **Medium** |
| 5 | **Recommendation vs Resolution Candidate** boundary vocabulary (near-synonymous "propose a path") | **Medium** |
| 6 | **"Confidence"** (Outcome Confidence vs generic vs future Assessment/recommendation confidence) | **Medium** |
| 7 | **Lifecycle "ending" verb proliferation** (disappear/retire/withdraw/close/become historical) | **Medium** |
| 8 | **Reused outcome words** (Accepted/Rejected/Deferred/Superseded across objects) | **Medium** (compounds #1) |
| 9 | **"Governance"** domain vs model naming | **Medium** |
| 10 | **"Reliability"** (per-dimension qualifier vs assessment-level signal) | **Medium** (partly reconciled) |
| 11 | **"Understanding"** unqualified vs qualified family | **Medium** |
| 12 | **"Context"** (assessment vs governance, nested) | **Low** |
| 13 | **"Evaluation" vs "Review"** (Review Request requests evaluation) | **Low** |
| 14 | **"Justified" vs "rationale" vs "lineage/basis"** | **Low** |
| 15 | **"Creation" verb variance** (appear/generation/creation/recording/establishment) | **Low** |

---

## 8. Recommended Reconciliation Priorities

*Identification only — no solutions proposed.* Ordered by risk × architectural centrality:

1. **"Accepted" / "Acceptance" (and the reused outcome words).** Resolve first. It is the highest-risk collision and sits on the flagship governance result (Accepted Understanding), while also recurring as a lifecycle outcome across three objects (§5/#8). Ambiguity here propagates through the entire Governance Domain.
2. **"Governed Understanding" vs "Accepted Understanding."** The architectural **endpoint** carries two terms with no cross-definition; this should be settled before any Knowledge Layer work consumes the endpoint.
3. **"Outcome."** A flagship term ("Outcome Confidence") and a pervasive governance word ("outcome of an evaluation") share a head with different meanings — high cross-domain reach.
4. **"Resolution"** (proposal vs Finding-resolved) and the **Recommendation/Resolution Candidate** boundary vocabulary. These are adjacent and feed the thinnest conceptual boundary; clarifying the vocabulary would harden that boundary.
5. **Lifecycle "ending"-verb proliferation.** A consistency-hygiene item: one concept, five verbs. Lower urgency, but cheap clarity across all governance objects.
6. **"Governance" domain-vs-model naming.** Lower risk, but worth settling because it sits at the domain boundary readers consult most.

Items 10–15 (Reliability granularity, Understanding family, Context nesting, evaluation/review, justification/rationale, creation verbs) are **Low** and can be deferred.

---

## 9. Final Assessment

**Terminology health: strong on invariants, concentrated weakness at the acceptance boundary.** The architecture's *cross-cutting* vocabulary — **basis, explainable, event-driven, history, supersession, reconsideration** — is remarkably uniform across all thirteen models and is the strongest evidence of disciplined authorship. The *assessment-layer* vocabulary (CAF, Clarity/Alignment/Feasibility, integrity, evidence, inference, impact assessment) is clean and unambiguous. The collisions are not scattered; they **cluster at the Understanding↔Governance boundary and around the acceptance/outcome family.**

**Highest-risk vocabulary collisions:**
1. **"Accepted / Acceptance"** — one word spanning an evaluation outcome and the governance result.
2. **"Governed Understanding" vs "Accepted Understanding"** — two terms for the architectural endpoint.
3. **"Outcome"** — flagship signal name vs governance step-result.

**Already-stable vocabulary areas:**
- Traceability cluster (basis / explainable / rationale / history) — uniform.
- Assessment cluster (CAF, integrity, evidence, inference, impact assessment) — clean.
- Lifecycle replacement/retention (supersession, reconsideration, history preservation) — consistent.
- Descriptive / Prescriptive / Governance-object typing — clean.

The terminology is healthy enough to extend, provided the **acceptance/outcome cluster** and the **endpoint term** are reconciled before the Governance Domain is consumed by any future Knowledge Layer work.

---

## Verification

- **All architecture models reviewed** — confirmed (15 documents: 13 models + index + coverage audit).
- **No model modified** — confirmed (read-only; this audit is a separate file).
- **No doctrine introduced** — confirmed.
- **No terminology changed** — confirmed (terms are quoted and analyzed, never altered or redefined).
- **Only terminology analysis performed** — confirmed (no solutions proposed; §8 identifies priorities without resolving them).

*Terminology Reconciliation Audit v1 complete. Read-only analysis across the specified architecture; identifies overloaded terms, synonym drift, boundary and lifecycle vocabulary collisions, and risk-ranked reconciliation priorities. No model modified, no doctrine introduced, no terminology resolved.*
