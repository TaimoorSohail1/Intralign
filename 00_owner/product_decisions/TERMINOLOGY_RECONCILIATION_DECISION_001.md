# Terminology Reconciliation Decision 001

**Document:** TERMINOLOGY_RECONCILIATION_DECISION_001.md
**Type:** Founder-decision artifact (decision package — defers all decisions to the founder)
**Reviewed (authoritative, unmodified):** `TERMINOLOGY_RECONCILIATION_AUDIT_V1.md` · `MODEL_COVERAGE_AUDIT_V1.md` · `MODEL_LINEAGE_INDEX_V1.md` · `GOVERNANCE_MODEL_V1.md` · `ACCEPTED_UNDERSTANDING_MODEL_V1.md` · `DISPOSITION_MODEL_V1.md` · `RESOLUTION_CANDIDATE_MODEL_V1.md` · `RECOMMENDATION_MODEL_V1.md`
**Date:** 2026-05-31

> **Architecture V1 note (added by the Architecture V1 Simplification Refactor).** Per the founder decision, the Governance Domain is **Future Architecture**. All three decision areas in this package — *Accepted / Acceptance*, *Governed vs Accepted Understanding*, and *Outcome* — concern the deferred Governance Domain or its endpoint, so they are **Future Scope**: **not on the Architecture V1 critical path** and **not blocking V1 implementation.** This package is **preserved in full** as decision-support for when governance is activated; no decision is required for V1.

> **Nature of this document.** This is **not** a model specification, a governance model, or an architecture redesign. It is a **decision package** that surfaces terminology collisions for founder decision. It **changes no terminology**, modifies no model, introduces no doctrine, creates no new concept, and implements no recommendation. Every collision is presented with options; **no option is selected.** All decisions are deferred to the founder.

---

## 1. Purpose

This document exists to support **founder terminology decisions** identified by two prior read-only reviews:

- `TERMINOLOGY_RECONCILIATION_AUDIT_V1.md` — the terminology collision/overload/synonym analysis.
- `MODEL_COVERAGE_AUDIT_V1.md` — which independently surfaced the "Accepted" overload and the "Governed vs Accepted Understanding" question.

Its job is to: identify the terminology collisions that require a founder decision; explain the implications of each; present decision options neutrally; identify the documents each decision would touch; and **defer every decision to the founder.**

**Explicit statement: no terminology is changed by this document.** It prepares decisions; it does not make them.

---

## 2. Decision Area Inventory

Collisions classified by the audits as **High Risk** or **Architecturally Significant**, carried forward here as decision areas.

| # | Decision area | Term(s) | Location(s) | Affected models |
|---|---|---|---|---|
| 1 | **Accepted / Acceptance** | "Accepted," "Acceptance," "accepted" | Disposition outcomes; Recommendation outcomes; Resolution Candidate outcomes; Governance acceptance; Accepted Understanding | Disposition, Recommendation, Resolution Candidate, Governance, Accepted Understanding |
| 2 | **Governed Understanding vs Accepted Understanding** | "Governed Understanding," "Accepted Understanding" | Resolution Candidate bridge phrase; Governance & Accepted Understanding output; index lineage | Resolution Candidate, Governance, Accepted Understanding, Model Lineage Index |
| 3 | **Outcome** | "Outcome Confidence," "evaluation outcome," "governance outcome" | Confidence signal name; Disposition records; Governance result | Confidence, Disposition, Governance, Accepted Understanding |

Secondary (lower-risk) findings are inventoried in Section 6.

---

## 3. Decision Area #1 — Accepted / Acceptance

### Usages discovered
- **Disposition** — conceptual outcomes "**Accepted**, Rejected, Deferred, Superseded." A Disposition records the outcome of an evaluation; "Accepted" denotes that the evaluation affirmed a proposed resolution.
- **Recommendation** — a Recommendation "may be **accepted**, rejected, deferred, or ignored" (user choice). Here "accepted" denotes a user affirming a suggestion.
- **Resolution Candidate** — conceptual outcomes "**accepted**, rejected, superseded, withdrawn, or remain unresolved." Here "accepted" denotes affirmation of a proposed resolution at the candidate level.
- **Governance** — "governs **acceptance**," "responsible for **acceptance**." Here "acceptance" denotes the governance act of accepting *understanding*.
- **Accepted Understanding** — "**Accepted Understanding** is the output of Governance"; "understanding **accepted**." Here it denotes the durable governed *state/object*.

### Meanings discovered
- **M1 — Affirmation of a proposal or suggestion** (Disposition outcome, Recommendation outcome, Resolution Candidate outcome).
- **M2 — Governance acceptance of understanding** (Governance act → Accepted Understanding object/state).

### Affected models
Disposition, Recommendation, Resolution Candidate, Governance, Accepted Understanding.

### Why the collision matters
The same root word marks an **evaluation-level affirmation** (M1) and the **flagship governance result** (M2). A reader can collapse "the Disposition was **Accepted**" into "the understanding is **Accepted**," short-circuiting the specified sequence *Disposition → Governance → Accepted Understanding*. Because every future Governance Domain consumer (including any Knowledge Layer) builds on "accepted" understanding, an unsettled meaning here propagates downstream.

### Possible interpretations *(presented, not selected)*
- **Interpretation A — One concept, context-disambiguated.** "Accepted" is a single notion ("affirmed/agreed"); the layer is inferred from context; no lexical change is needed.
- **Interpretation B — Two distinct concepts sharing a root.** M1 (evaluation affirmation) and M2 (governance acceptance) are different concepts that merely share a word and warrant lexical distinction.
- **Interpretation C — A genuine relationship, not a collision.** M1 is a precondition that *feeds* M2 (evaluation-acceptance enables governance-acceptance); the shared word reflects a real chain rather than an accident.

*No interpretation is selected.*

---

## 4. Decision Area #2 — Governed Understanding vs Accepted Understanding

### Occurrences discovered
- **"Governed Understanding"** — appears as the **bridge target** of the Resolution Candidate Model ("the bridge between Understanding and Governed Understanding") and in that model's index entry. It is used only in the Resolution Candidate context and is not formally defined as an object or state.
- **"Accepted Understanding"** — the **formal output object** of Governance: used by the Governance Model ("bridges Understanding and Accepted Understanding"), the Accepted Understanding Model (the object itself), and the index lineage endpoint.

### Meanings discovered
- **"Governed Understanding"** — an informal phrase for understanding that has entered/passed through governance (umbrella, undefined).
- **"Accepted Understanding"** — the specific durable governed object produced when Governance accepts understanding (defined).

### Affected models
Resolution Candidate (uses "Governed Understanding"), Governance and Accepted Understanding (use "Accepted Understanding"), Model Lineage Index (uses both).

### Why the collision matters
The architectural **endpoint** is named two ways with no cross-definition. Any future Knowledge Layer that "consumes the governed endpoint" must know whether it consumes "Governed Understanding" or "Accepted Understanding," and whether those are one thing.

### Possible interpretations *(presented, not selected)*
- **Synonymous** — the two phrases name the same state; one is informal shorthand for the other.
- **Parent/child** — "Governed Understanding" is the broader category (any understanding under governance, accepted or not); "Accepted Understanding" is a specific governed state within it.
- **Separate states** — "Governed Understanding" denotes understanding *in* governance (in-process); "Accepted Understanding" denotes the *terminal accepted* state — two distinct points in the chain.

*No interpretation is selected.*

---

## 5. Decision Area #3 — Outcome

### Usages discovered
- **Outcome Confidence** (Confidence) — the named signal "Outcome Confidence." The Confidence Model explicitly states it is **not** outcome prediction or success probability; the word "Outcome" in the compound denotes the project-outcome-achievement context the confidence ultimately serves.
- **Evaluation Outcome** (Disposition) — "records the **outcome** of an evaluation"; "recorded outcome." Here "outcome" denotes the *result of a process step*.
- **Governance Outcome** (Governance, and Accepted Understanding's explanation chain) — "governance **outcome**"; "accepted-understanding outcome." Again the *result of a step*.

### The collision
The head word "outcome" carries two senses: **(S1)** project-outcome-achievement context (embedded in the flagship "Outcome Confidence"), and **(S2)** the result/conclusion of a governance or evaluation step. A reader meeting "outcome" must infer which sense applies, and the flagship compound "Outcome Confidence" sits beside frequent S2 usage in the Governance Domain.

### Affected models
Confidence, Disposition, Governance, Accepted Understanding.

### Possible interpretations *(presented, not selected)*
- **A — Compound-vs-generic, no action.** "Outcome Confidence" is a fixed compound term; "evaluation/governance outcome" is separate generic usage; context suffices.
- **B — Distinct senses to be separated.** S1 and S2 are different enough that the flagship term and the governance usage should be lexically distinguished.
- **C — Distinct but tolerable.** The senses differ but the collision is low-consequence and may be accepted as-is.

*No interpretation is resolved.*

---

## 6. Secondary Terminology Findings

Lower-risk findings carried from the Terminology Audit, documented for completeness — **not resolved.**

- **Governance (domain vs model)** — "Governance" names both the Governance **Domain** and the Governance **Model** within it.
- **Resolution** — "Resolution Candidate" (a governance proposal) vs a Finding's "resolved" lifecycle state.
- **Context** — "assessment context" vs "governance context," where governance context is defined to *include* assessment context (nesting).
- **Lifecycle vocabulary overlap** — one "ending" concept expressed as *disappear / retire / withdraw / close / become historical*; reused outcome words (Accepted/Rejected/Deferred/Superseded across objects); varied "creation" verbs (appear/generation/creation/recording/establishment).
- **Recommendation vs Resolution Candidate** — lexically near-synonymous ("suggest a path" / "propose a resolution"); distinguished by orientation, not vocabulary.
- **Reliability** — per-dimension "reliability qualifier" (CAF Scoring) vs assessment-level "Assessment Reliability" (Reliability Model).
- **Confidence** — "Outcome Confidence" vs generic "confidence in integrity" vs future "Assessment Confidence" / "recommendation confidence."
- **Justified vs rationale vs basis/lineage** — epistemic warrant vs explanatory reason vs traceability term.
- **Evaluation vs review** — a "Review Request" requests "evaluation"; the external step is "Human Evaluation," not "Human Review."

*All secondary findings are deferred.*

---

## 7. Impact Analysis (mapping only — no recommendations)

### Decision Area #1 — Accepted / Acceptance
- **Affected models:** Disposition, Recommendation, Resolution Candidate, Governance, Accepted Understanding.
- **Affected lineage diagrams:** the governance lineage in the Model Lineage Index (Finding → Resolution Candidate → Review Request → Human Evaluation → Disposition → Governance → Accepted Understanding); the Disposition and Governance explanation chains.
- **Affected glossary entries:** any future canonical definitions of "Accepted," "Acceptance," and "Accepted Understanding" (no formal glossary exists yet; the canonical-definitions registry would be the home).
- **Affected future Knowledge Layer work:** high — truth promotion / canonical knowledge would build directly on "accepted" understanding; the unsettled meaning would carry into that layer.

### Decision Area #2 — Governed vs Accepted Understanding
- **Affected models:** Resolution Candidate, Governance, Accepted Understanding, Model Lineage Index.
- **Affected lineage diagrams:** the Resolution Candidate bridge label ("Governed Understanding"); the governance lineage endpoint ("Accepted Understanding").
- **Affected glossary entries:** the definition of the architectural endpoint term(s).
- **Affected future Knowledge Layer work:** high — the Knowledge Layer consumes the governed endpoint; it must know which term names it.

### Decision Area #3 — Outcome
- **Affected models:** Confidence, Disposition, Governance, Accepted Understanding.
- **Affected lineage diagrams:** the "Outcome Confidence" node in the understanding-improvement loop; "outcome" within governance explanation chains.
- **Affected glossary entries:** definitions of "Outcome Confidence" and of process-result "outcome."
- **Affected future Knowledge Layer work:** low-moderate — primarily an Understanding-Domain flagship term; limited Knowledge Layer exposure.

---

## 8. Founder Decision Matrix

*No answers — only the decisions required.*

| Decision Area | Decision Required | Affected Models |
|---|---|---|
| Accepted / Acceptance | **Yes** | Disposition, Recommendation, Resolution Candidate, Governance, Accepted Understanding |
| Governed Understanding vs Accepted Understanding | **Yes** | Resolution Candidate, Governance, Accepted Understanding, Model Lineage Index |
| Outcome | **Yes** | Confidence, Disposition, Governance, Accepted Understanding |
| Governance (domain vs model) | Optional | Governance, Model Lineage Index |
| Resolution (proposal vs resolved state) | Optional | Finding, Resolution Candidate, Recommendation |
| Context (assessment vs governance) | Optional | Recommendation, Resolution Candidate, Review Request, Disposition, Governance |
| Lifecycle vocabulary overlap | Optional | Finding, Recommendation, Resolution Candidate, Review Request, Disposition, Governance, Accepted Understanding |

---

## 9. Recommended Resolution Order

*No solutions are recommended. This section identifies only which decisions should occur first, using architectural-dependency reasoning.*

1. **Decision Areas #1 and #2 are coupled and should be decided first (together).** Both define the **terminal governed state** of the architecture — #2 names it, #1 governs the word for the act/outcome that produces it. The future Knowledge Layer consumes this terminal state; therefore endpoint clarity gates downstream modeling. Because #2 ("what the endpoint is called") and #1 ("whether 'Accepted/Acceptance' is shared across layers") both bear on the same terminal object, deciding one in isolation could pre-constrain the other.
2. **Decision Area #3 (Outcome) follows, and is comparatively independent.** It centers on a flagship Understanding-Domain term ("Outcome Confidence") with limited Knowledge Layer exposure; it has low dependency on #1/#2 and can be decided after, or in parallel.
3. **Secondary findings last.** They are local to individual objects, have the lowest cross-model coupling, and do not gate any downstream domain.

The ordering reflects dependency only: terminal-state vocabulary (consumed downstream) before flagship-signal vocabulary (locally contained) before local hygiene.

---

## 10. Final Assessment

- **The architecture remains structurally sound.** Both prior audits found the model set complete and internally consistent in structure; no structural defect underlies these collisions.
- **The remaining ambiguity is semantic, not structural.** Every item here is a *vocabulary* question — overloaded words, an unsettled endpoint term, a shared head word — not a missing or conflicting mechanism.
- **These terminology decisions should occur before Knowledge Layer modeling.** The Knowledge Layer consumes the governed endpoint and the "accepted" state; settling Decision Areas #1 and #2 first would prevent the ambiguity from propagating into that future layer.

This document creates no new terminology and proposes no architecture change. It is a decision package only.

---

## Verification

- **No model modified** — confirmed (this is a separate decision artifact; the reviewed documents are referenced only).
- **No terminology changed** — confirmed (terms are quoted and analyzed; none altered or redefined).
- **No doctrine introduced** — confirmed.
- **No architecture redesigned** — confirmed (no mechanism, model, or relationship is changed or proposed).
- **Only decision preparation performed** — confirmed (collisions surfaced, options presented neutrally, all decisions deferred to the founder; no option selected).

*Terminology Reconciliation Decision 001 complete. A founder-decision package surfacing three High-Risk terminology collisions (Accepted/Acceptance; Governed vs Accepted Understanding; Outcome) plus secondary findings, with usages, meanings, affected documents, neutral interpretation options, impact mapping, and a dependency-based decision order. No terminology changed, no model modified, no decision made.*
