# Model Coverage Audit v1

**Document:** MODEL_COVERAGE_AUDIT_V1.md
**Type:** Architecture coverage audit (read-only review; analysis & recommendation)
**Audited set (authoritative, unmodified):** CAF Assessment · CAF Scoring · Reliability · Confidence · MRI · Overlay · Finding · Recommendation · Resolution Candidate · Review Request · Disposition · Governance · Accepted Understanding · Model Lineage Index
**Date:** 2026-05-31

> **Constraints honored.** No model was modified and no new model, doctrine, governance behavior, Knowledge Layer behavior, or truth-promotion behavior is created here. Every statement is drawn only from the existing model set. This audit is an informational review artifact; it is non-normative.
>
> **Architecture V1 reclassification note (added by the Architecture V1 Simplification Refactor).** Per the founder decision, **Architecture V1 is a Planning Intelligence / Understanding-Improvement System and is complete without Governance Domain participation.** The five Governance Domain models (Resolution Candidate, Review Request, Disposition, Governance, Accepted Understanding) are **Future Architecture (Outcome Orchestration / Agent Governance)** — preserved and specified, but not active V1. **Notification remains active** because it supports the Understanding Domain. The findings below are **preserved in full**; where this audit describes the Governance Domain as a completed part of the architecture, read that as *completed and preserved as Future Architecture*, not as active V1. The audit's maturity and completeness assessments are reframed accordingly in §6 and §9.

---

## 1. Current Architecture Inventory

Thirteen models (eight Understanding Domain, five Governance Domain) plus one informational index. Purpose / domain / inputs / outputs / primary responsibility, using only what each document defines.

| Model | Domain | Inputs | Outputs | Primary responsibility |
|---|---|---|---|---|
| CAF Assessment | Understanding | Evidence, Inference, Findings, Impact Assessments | CAF assessment (integrity), flat finding taxonomy, Impact Assessment factors | Reason about the integrity of project understanding (Clarity/Alignment/Feasibility) |
| CAF Scoring | Understanding | CAF Assessment (impact-assessed findings, evidence, coverage) | Per-dimension CAF score = integrity index + state band + reliability qualifier; explanation basis | Represent and explain CAF as a score (calibration externalized) |
| Reliability | Understanding | Coverage, Evidence Availability, Assessability | Assessment Reliability signal (supportability) | Measure trustworthiness/supportability of the CAF assessment, independent of CAF & findings |
| Confidence | Understanding | CAF Assessment + Assessment Reliability | Outcome Confidence (summarized, reliability-qualified signal) | Summarize CAF qualified by Reliability into one trust signal |
| MRI | Understanding | CAF, Reliability, Confidence + finding visibility | Observable representation of understanding | Make understanding observable (visualization layer) |
| Overlay | Understanding | MRI | Alternate, emphasis-adjusted, deterministic views | Manage attention within MRI without altering understanding |
| Finding | Understanding | Produced through assessment; relates to CAF via Impact Assessment | Governable Finding objects (lifecycle, relationships, grouping, ownership) | Define the governable, actionable observation between assessment and action |
| Recommendation | Understanding | Assessment context (Findings, CAF, Reliability, Confidence) | Advisory suggested improvement paths (prescriptive) | Prescribe advisory improvement paths that operate on Findings |
| Resolution Candidate | Governance | Assessment context (Findings, Evidence, Inference, CAF, Reliability, Confidence) | Proposed resolution to a Finding (governance object) | Propose possible resolutions to a Finding for human evaluation |
| Review Request | Governance | Governance context (Findings, Resolution Candidates, assessment context, ownership info) | A request for evaluation of one or more candidates | Request — never perform — evaluation of Resolution Candidates |
| Disposition | Governance | Governance context (refs Findings, Resolution Candidates, Review Requests; the evaluation) | Durable recorded evaluation outcome | Record evaluation outcomes (preserving history) |
| Governance | Governance | Findings, Resolution Candidates, Review Requests, Dispositions | Governance outcome (acceptance) | Govern the acceptance of understanding (on human judgment) |
| Accepted Understanding | Governance | Governance outcomes (informed by Dispositions) | Durable governed accepted-understanding object | Hold the durable governed output of Governance; bridge to future Knowledge Layer |
| Model Lineage Index | Meta | The thirteen models | Navigational architecture map | Index/map the architecture (informational, non-normative) |

---

## 2. End-to-End Architectural Flow

### Understanding Domain — the improvement loop
```text
Evidence → Inference → Finding → Impact Assessment → CAF → Reliability → Outcome Confidence
   → MRI → Overlay → Recommendation → [User Action: external] → Evidence (re-enters)
```

### Governance Domain — the acceptance chain
```text
Finding → Resolution Candidate → Review Request → [Human Evaluation: external]
   → Disposition → Governance → Accepted Understanding → [Future Knowledge Layer: deferred]
```

### Domain boundary
The **Finding** is the hand-off point: produced and assessed in the Understanding Domain, and consumed by the Governance Domain (via Resolution Candidate). The two domains are separated by the **assessment-vs-acceptance** boundary the Governance Model makes explicit ("assessment and acceptance are separate responsibilities").

### Transition ownership check

| Transition | Owner | Status |
|---|---|---|
| Evidence / Inference / Finding (as observation) / Impact Assessment → CAF | CAF Assessment | Owned |
| CAF → score | CAF Scoring | Owned |
| Coverage/Evidence-Availability/Assessability → Reliability | Reliability | Owned |
| CAF + Reliability → Outcome Confidence | Confidence | Owned |
| Assessments → observable view | MRI | Owned |
| MRI → attention view | Overlay | Owned |
| Finding (as governable object) | Finding | Owned |
| Findings/context → improvement suggestion | Recommendation | Owned |
| **Recommendation → User Action** | — | **External (human); intentionally unowned** |
| User Action → new Evidence (loop closure) | CAF Assessment (Evidence) | Owned on re-entry |
| Finding → Resolution Candidate | Resolution Candidate | Owned |
| Resolution Candidate → Review Request | Review Request | Owned |
| **Review Request → Human Evaluation** | — | **External (human); intentionally unowned** |
| Human Evaluation → Disposition (recording) | Disposition | Owned |
| Disposition → Governance | Governance | Owned |
| Governance → Accepted Understanding | Accepted Understanding | Owned |
| **Accepted Understanding → Future Knowledge Layer** | — | **Unowned; intentionally deferred** |

**Unowned transitions:** three, all by design — two external human steps (User Action; Human Evaluation) that the architecture deliberately keeps external to preserve human authority, and one deferred frontier (Knowledge Layer). No *accidental* unowned transition exists in the primary chains.

---

## 3. Responsibility Coverage Matrix

Coverage status: **Covered** (a model owns it) · **Deferred** (intentionally externalized to a future artifact/model) · **Distributed** (owned in aggregate, no single owner) · **Unowned** (no owner today).

| Responsibility | Responsible model | Status | Notes |
|---|---|---|---|
| Assessment (integrity) | CAF Assessment | Covered | Three independent dimensions |
| Scoring / representation | CAF Scoring | Covered (structure) / Deferred (calibration) | Numeric weights, band boundaries, aggregation arithmetic externalized |
| Reliability (supportability) | Reliability | Covered | Independent of CAF and findings |
| Confidence (summary trust) | Confidence | Covered | Derived from CAF + Reliability only |
| Visualization | MRI | Covered (model) / Deferred (visual form) | UI/layout out of scope of the model |
| Attention management | Overlay | Covered (model) / Deferred (UI) | Deterministic, never distorting |
| Governable observation | Finding | Covered | Lifecycle, relationships, grouping, ownership |
| Recommendation | Recommendation | Covered | Prescriptive; operates on Findings |
| Proposed resolution | Resolution Candidate | Covered | First governance object |
| Evaluation request | Review Request | Covered | Requests, never performs, evaluation |
| Evaluation outcome recording | Disposition | Covered | Preserves history |
| Acceptance governance | Governance | Covered | Depends on human judgment |
| Accepted understanding | Accepted Understanding | Covered | Durable governed output |
| Evidence definition / ingestion | CAF Assessment (definition only) | Covered (definition) / Unowned (ingestion mechanics) | Models define *what* evidence is, not *how* it is ingested |
| Human evaluation execution | — | Unowned (external by design) | Established as external by Review Request / Disposition |
| Explainability lineage / audit | All models (each is explainable + history-preserving) | **Distributed** | No single audit/lineage owner consolidates the chain |
| Ownership assignment | Finding (concept) + Review Request (refs ownership info) | **Partial/Unowned** | Ownership *attribute* defined; *assignment mechanism* not owned |
| Notification / awareness delivery | — | **Unowned (future)** | Named only as a future supporting model in the index |
| Truth / canonical knowledge | — | Unowned (deferred) | Explicitly deferred by Governance & Accepted Understanding |

---

## 4. Gap Analysis (only genuinely unowned/under-owned items)

| Gap | Why it is a gap | Model that stops before it | Intentional? |
|---|---|---|---|
| **Knowledge Layer transition** | Accepted Understanding bridges to "future Knowledge Layer concepts" that no model defines | Accepted Understanding (stops at the bridge) | **Yes** — explicitly deferred |
| **Canonical truth representation** | No model defines what "accepted as true / canonical" means or how it is stored | Governance & Accepted Understanding (both decline truth promotion) | **Yes** — explicitly deferred |
| **Accepted Understanding promotion** | The step from accepted understanding to canonical/promoted knowledge is undefined | Accepted Understanding | **Yes** — deferred to the Knowledge Layer frontier |
| **Audit lineage** | Explainability and history exist in every model but no model consolidates an end-to-end audit/lineage view | All models (distributed) | **Partly** — distributed by design, but no consolidating owner is stated |
| **Notification delivery** | Surfacing awareness of relevant changes to responsible people is owned by nothing today | Named "future" in the index; no governance model claims it | **Yes** — held as a future supporting service |
| **Ownership assignment** | Finding defines ownership as an attribute and Review Request consumes "ownership information," but no model defines how ownership is assigned/resolved | Finding (attribute only) | **Unclear** — appears under-owned rather than deliberately excluded |
| **Review execution (human evaluation)** | The evaluation itself is performed by no model | Review Request / Disposition (establish the request and the record around it) | **Yes** — external to preserve human authority |

The two genuinely *non-intentional-looking* items are **audit lineage** (distributed, no consolidating owner) and **ownership assignment** (attribute defined, mechanism absent). The rest are deliberate deferrals or deliberate externalizations.

---

## 5. Overlap Analysis

| Pair | Boundary | Sufficiently defined? |
|---|---|---|
| **Finding vs Resolution Candidate** | Finding = descriptive observation (Understanding); Resolution Candidate = proposal that operates on a Finding (Governance). "A Resolution Candidate is not a Finding." | **Yes** — clear (descriptive object vs proposal; different domains) |
| **Recommendation vs Resolution Candidate** | Both consume assessment context, operate on Findings, are event-driven/explainable, and influence assessment only through action. Distinguished only by **orientation**: Recommendation = improvement-oriented/prescriptive (Understanding); Resolution Candidate = governance-oriented proposal for evaluation (Governance). | **Defined but thin** — the boundary rests on intent/orientation, not structure; this is the **highest overlap-risk pair** |
| **Governance vs Accepted Understanding** | Governance = the act/layer of acceptance; Accepted Understanding = the durable result. "Governance performs acceptance; Accepted Understanding is the result." | **Yes** — clear (act vs object) |
| **Review Request vs Disposition** | Review Request = requests evaluation (before); Disposition = records outcome (after). Sequential. | **Yes** — clear (request vs record) |

### Terminology conflicts found
1. **"Accepted" is overloaded.** It is a conceptual *Disposition outcome* ("Accepted/Rejected/Deferred/Superseded") **and** the *Governance/Accepted Understanding* result. A Disposition of "Accepted" (an evaluation accepted a resolution) is not the same as Governance producing **Accepted Understanding** (acceptance of the understanding) — yet the same word spans both layers. **Highest-value terminology finding; not reconciled in the set.**
2. **"Governed Understanding" vs "Accepted Understanding."** Resolution Candidate (and its index entry) bridges to **"Governed Understanding,"** while Governance/Accepted Understanding use **"Accepted Understanding."** Whether these are synonyms or distinct states is never explicitly reconciled.
3. **"Assessment context" vs "governance context."** Recommendation/Resolution Candidate consume "assessment context"; Review Request/Disposition/Governance consume "governance context" (which the Review Request defines to *include* assessment context). The layering is coherent but the two terms are nowhere cross-defined.
4. **Reused lifecycle-outcome vocabularies.** Resolution Candidate (accepted/rejected/superseded/withdrawn/unresolved), Review Request (fulfilled/withdrawn/superseded/closed/open), Disposition (accepted/rejected/deferred/superseded), Recommendation (accepted/rejected/deferred/ignored) reuse overlapping words. Each is scoped to its own object, but the shared vocabulary invites conflation across objects.

---

## 6. Domain Completeness Assessment

> **Architecture V1 reframing.** Per the founder decision, **Active Architecture V1 = the Understanding Domain (below) + Notification**, and it is **architecturally complete without Governance Domain participation.** The Governance Domain assessment that follows is preserved as a description of **Future Architecture**, not active V1.

### Understanding Domain — **Architecturally complete (conceptual layer); the whole of Active Architecture V1 (with Notification).**
Every transition from Evidence through Recommendation is owned (Section 2). The improvement loop closes through the one intentionally-external step (User Action), and re-enters as Evidence under CAF Assessment. The descriptive/prescriptive boundary is clean (seven descriptive models + one prescriptive). The only items outside the conceptual models — **evidence ingestion mechanics**, **scoring calibration**, **visual form/layout** — are explicitly deferred to product/UI/calibration artifacts, not conceptual gaps. **No active V1 transition requires the Governance Domain.** *Complete for what a conceptual model layer should own.*

### Governance Domain — **Future Architecture: specified chain complete and preserved; not active V1.**
As **Future Architecture (Outcome Orchestration / Agent Governance)**, the specified chain (Resolution Candidate → Review Request → [Human Evaluation] → Disposition → Governance → Accepted Understanding) is fully owned and terminates cleanly at Accepted Understanding. The in-chain external step (Human Evaluation) is intentional. This chain is **not part of active Architecture V1** and is not required for V1 planning operation; it is preserved for later activation. Its remaining supporting/cross-cutting items (ownership assignment, a consolidated audit/lineage owner) are themselves future concerns. **Notification, by contrast, is active V1** — it supports the Understanding Domain and requires no governance participation.

---

## 7. Candidate Future Models (identified from gaps only — not designed)

| Candidate | Purpose (one line) | Why needed (gap) |
|---|---|---|
| **Notification Model** | Surface awareness of relevant changes to the people responsible | "Notification delivery" gap; already named future in the index |
| **Knowledge Layer Model(s)** | Define what canonical/promoted knowledge is, downstream of Accepted Understanding | "Knowledge Layer transition" + "canonical truth" gaps; the destination of the whole chain |
| **Audit / Lineage Model** | Consolidate the per-model explainability and history into an end-to-end governance lineage | "Audit lineage" gap (currently distributed, no single owner) |
| **Ownership / Assignment Model** | Define how ownership is assigned and resolved across Findings and governance objects | "Ownership assignment" gap (attribute defined; mechanism absent) |

Notification and the Knowledge Layer are already anticipated by the index/Accepted Understanding; Audit/Lineage and Ownership/Assignment are surfaced newly by this audit. *Identification only — no behavior is proposed.*

---

## 8. Architectural Risks

**Circular dependencies — none at the conceptual level, one feedback loop to watch.**
No model depends on a downstream model's output as a static input. The one structure to watch is the **Finding's dual role**: it is both an *input to assessment* (Finding → Impact Assessment → CAF) and the *actionable object* surfaced by MRI/Overlay and acted on by Recommendation. This is a **managed feedback loop**, not a cycle — it closes through the external User Action and re-enters as Evidence, and every model is event-driven ("only action and evidence change assessment"). It is safe as specified but is the single place where a future change could accidentally introduce a true cycle.

**Undefined transitions.** Three, all intentional (User Action, Human Evaluation, Knowledge Layer) — see Section 2. Risk is operational, not architectural: the chain *stalls* (does not break) if a human step never occurs.

**Hidden assumptions.**
- A human will act at the two external steps; absent that, Resolution Candidates are never evaluated and Recommendations never acted upon (the loops stall).
- A reliable **evidence-ingestion path** exists so that "action → evidence → re-run" actually happens; the conceptual models assume but do not own it.
- **Calibration exists somewhere.** CAF Scoring, Reliability, and Confidence all defer numeric calibration; until a calibration artifact exists, all scores are conceptual only.
- The reader treats "Accepted" (disposition) and "Accepted Understanding" (governance result) as distinct despite the shared word (Section 5).

**Potential future governance conflicts.**
- **Reconsiderable acceptance vs canonical truth.** Accepted Understanding "may be reconsidered / is not permanence." A future truth-promotion/Knowledge Layer model that treats accepted understanding as fixed "truth" would conflict with this non-permanence principle. This is the most consequential latent conflict.
- **"Governed Understanding" vs "Accepted Understanding"** left unreconciled (Section 5) could let future governance models diverge in vocabulary.
- A future **Notification** model must remain a supporting service and not absorb governance judgment, disposition, or acceptance (the index already constrains this) — risk if it creeps.

---

## 9. Final Assessment

> **Architecture V1 reframing.** Under the founder decision, the maturity assessment below applies to **Active Architecture V1** = the eight Understanding Domain models + Notification, which is **complete without Governance Domain participation**. The Governance Domain's coherence is preserved as **Future Architecture** maturity, not active V1.

**Architecture maturity (qualitative):** **Active Architecture V1 is complete at the conceptual-model layer; pre-implementation below it.** The Understanding Domain (plus Notification) is coherent, internally consistent, and connected end-to-end, with a small, well-marked set of intentional deferrals; the Future-Architecture Governance Domain is likewise coherent and preserved. The set holds a remarkable uniformity of invariants across all thirteen models — event-driven, explainable-to-basis, history-preserving, "only action and evidence change assessment," and a clean descriptive / prescriptive / governance-object typing. What remains is *below* the conceptual layer (calibration, ingestion, UI, storage) and *beyond* it (Knowledge Layer), not *within* it.

**Most important unresolved gap:** the **Knowledge Layer / canonical-truth transition.** It is the destination of the entire chain — Accepted Understanding bridges to it — yet it is wholly undefined, and it carries the latent non-permanence conflict (Section 8). (The most *actionable near-term* gap is Notification, but it is smaller in architectural weight.)

**Most important architectural strength:** the **enforced separation of concerns**, expressed as the assessment-vs-acceptance domain boundary and the universal invariants applied identically across every model. Nothing changes understanding except action and evidence; every object is explainable to its basis and event-driven; the two human-authority steps are deliberately external. This consistency is what makes the architecture auditable and extensible.

**Recommended next modeling priority:** **Notification Model** — it is the only remaining model already named as future, it closes a concrete, long-standing gap (awareness delivery), and it is small and well-bounded. Before drafting it, a brief **terminology reconciliation** (the "Accepted" overload and "Governed vs Accepted Understanding") is the highest-leverage non-model housekeeping item, since it touches already-specified governance models. The **Knowledge Layer** is the larger strategic frontier but should follow, given its size and its latent conflict with reconsiderable acceptance.

---

*Model Coverage Audit v1 complete. Read-only review of fourteen documents; no model modified, no new model or doctrine created. Findings drawn solely from the existing model set. Subject to governance review.*
