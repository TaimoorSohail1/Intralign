# Founder Terminology Decision Workbook 001

**Document:** FOUNDER_TERMINOLOGY_DECISION_WORKBOOK_001.md
**Type:** Founder decision workbook (decision-facilitation material — captures decisions; makes none)
**Consumes (authoritative, unmodified):** `TERMINOLOGY_RECONCILIATION_DECISION_001.md` · `TERMINOLOGY_RECONCILIATION_AUDIT_V1.md` · `MODEL_COVERAGE_AUDIT_V1.md` · `MODEL_LINEAGE_INDEX_V1.md` · `GOVERNANCE_MODEL_V1.md` · `ACCEPTED_UNDERSTANDING_MODEL_V1.md` · `DISPOSITION_MODEL_V1.md` · `RESOLUTION_CANDIDATE_MODEL_V1.md`
**Date:** 2026-05-31

> **Architecture V1 note (added by the Architecture V1 Simplification Refactor).** Per the founder decision, the Governance Domain is **Future Architecture**. The three decision areas worked here — *Accepted / Acceptance*, *Governed vs Accepted Understanding*, and *Outcome* — are all in the deferred Governance Domain or at its endpoint, so they are **Future Scope**: **not on the Architecture V1 critical path** and **not blocking V1 implementation.** This workbook is **preserved in full** and can be completed when governance is activated; it is not required for V1.

> **Nature of this document.** This is **not** a model, a governance specification, or a terminology-change proposal. It is a **structured workbook** to help the founder make explicit decisions about unresolved terminology collisions. It **changes no terminology**, modifies no model, introduces no doctrine, and implements no recommendation. It poses questions and provides blank capture fields; it answers nothing.

---

## 1. Purpose

This workbook exists to **facilitate explicit founder decisions** on the terminology collisions already surfaced (not resolved) by:

- `TERMINOLOGY_RECONCILIATION_DECISION_001.md` — the founder-decision package (three High-Risk decision areas + secondary findings).
- `TERMINOLOGY_RECONCILIATION_AUDIT_V1.md` — the underlying terminology analysis.
- `MODEL_COVERAGE_AUDIT_V1.md` — which independently surfaced the "Accepted" overload and the "Governed vs Accepted Understanding" question.

It consumes those artifacts and turns each open decision into a workshop: a usage inventory, the architectural consequences of deciding either way, and explicit questions for the founder — followed by a blank response template to capture the decision.

**All decisions remain unresolved.** **This workbook changes nothing in the architecture.**

---

## 2. Decision Area Summary

| Decision area | Affected models | Why the decision matters (no solution) |
|---|---|---|
| **Accepted / Acceptance** | Disposition, Recommendation, Resolution Candidate, Governance, Accepted Understanding | The same root marks an evaluation-level affirmation and the flagship governance result; meaning propagates into any future "accepted" / truth work |
| **Governed Understanding vs Accepted Understanding** | Resolution Candidate, Governance, Accepted Understanding, Model Lineage Index | The architectural endpoint is named two ways with no cross-definition; downstream layers consume the endpoint |
| **Outcome** | Confidence, Disposition, Governance, Accepted Understanding | The flagship "Outcome Confidence" shares its head word with governance "outcome of an evaluation/step" |

*No solutions are offered in this summary or anywhere in this workbook.*

---

## 3. Decision Area #1 Workshop — Accepted / Acceptance

### Current Usage Inventory (by model)
- **Disposition** — conceptual outcomes "**Accepted**, Rejected, Deferred, Superseded." Sense: an evaluation affirmed a proposed resolution.
- **Recommendation** — "may be **accepted**, rejected, deferred, or ignored." Sense: a user affirmed a suggestion (user choice).
- **Resolution Candidate** — conceptual outcomes "**accepted**, rejected, superseded, withdrawn, or remain unresolved." Sense: affirmation of a proposed resolution at the candidate level.
- **Governance** — "governs **acceptance**," "responsible for **acceptance**." Sense: the governance act of accepting *understanding*.
- **Accepted Understanding** — "**Accepted Understanding** is the output of Governance," "understanding **accepted**." Sense: the durable governed state/object.

### Architectural Consequences
- If evaluation-affirmation and governance-acceptance are treated as **one concept**, the shared word stands and the lifecycle-outcome vocabularies across Disposition / Recommendation / Resolution Candidate remain aligned with the governance result.
- If they are treated as **distinct concepts**, the affected models would each carry a vocabulary distinction, and the flagship **Accepted Understanding** term would be insulated from the evaluation-outcome "Accepted."
- Whichever way it is decided, the result **flows downstream**: any future truth-promotion / Knowledge Layer work consumes the "accepted" state, so the chosen meaning is inherited there.
- The decision also interacts with Decision Area #2: "Accepted Understanding" is both the governance result (this area) and the endpoint term (next area).

### Questions For Founder *(do not answer here)*
- Are **evaluation acceptance** (a Disposition/Resolution Candidate outcome of "Accepted") and **governance acceptance** (producing Accepted Understanding) the **same concept**?
- Should they **share terminology**, or be lexically distinguished?
- If they are **related but not identical**, what is the relationship — precondition, hierarchy, or coincidence?
- Should **Recommendation "accepted"** (a user's choice on a suggestion) sit in the same family as governance acceptance, or be treated separately?
- Does the **Disposition outcome "Accepted"** need to be distinguishable from **"Accepted Understanding"** at a glance?

---

## 4. Decision Area #2 Workshop — Governed Understanding vs Accepted Understanding

### Current Usage Inventory (by model)
- **Resolution Candidate** — "the bridge between **Understanding** and **Governed Understanding**" (and its index entry). "Governed Understanding" is used only here, as a bridge-target phrase; it is not defined as an object or state.
- **Governance** — "bridges **Understanding** and **Accepted Understanding**."
- **Accepted Understanding** — the formal, defined output object: "the durable, governed output of Governance."
- **Model Lineage Index** — uses **both** phrases (Resolution Candidate entry → "Governed Understanding"; governance lineage endpoint → "Accepted Understanding").

### Architectural Consequences
- If **synonymous**, one phrase is shorthand for the other and the architecture has a single endpoint state under two labels.
- If **parent/child**, "Governed Understanding" is the broader category (understanding under governance, accepted or not) and "Accepted Understanding" is a specific state inside it — implying the architecture distinguishes "in governance" from "accepted."
- If **separate states**, the chain has two named points — understanding being governed vs understanding accepted — which would make the Resolution Candidate's bridge target (Governed Understanding) a *different* node from the chain endpoint (Accepted Understanding).
- The future **Knowledge Layer** consumes whatever the endpoint is; this decision determines what term it consumes and whether it consumes one state or two.

### Questions For Founder *(do not answer here)*
- Are "Governed Understanding" and "Accepted Understanding" **synonymous**?
- Are they **separate states** (e.g., in-governance vs accepted)?
- Is one a **parent category** of the other?
- Should the **Resolution Candidate bridge phrase** point at the same term the governance lineage ends in, or is the difference intentional?

---

## 5. Decision Area #3 Workshop — Outcome

### Current Usage Inventory (by model)
- **Confidence** — "**Outcome** Confidence" (the named signal). The Confidence Model states it is *not* outcome prediction or success probability; "Outcome" here denotes the project-outcome-achievement context the confidence ultimately serves.
- **Disposition** — "records the **outcome** of an evaluation," "recorded outcome." Sense: the result of a process step.
- **Governance** — "governance **outcome**"; and **Accepted Understanding**'s explanation chain references "accepted-understanding **outcome**." Sense: the result of a step.

### Architectural Consequences
- If the compound "Outcome Confidence" and the generic "outcome of a step" are treated as **separate, context-disambiguated** usages, nothing changes.
- If they are treated as a **collision to separate**, the flagship signal name or the governance usage would be distinguished to protect the flagship term.
- This area has **limited downstream reach**: "Outcome Confidence" is an Understanding-Domain flagship term; the governance "outcome" usages are local to the Governance Domain. Knowledge Layer exposure is low.

### Questions For Founder *(do not answer here)*
- Does **Outcome Confidence** use "Outcome" **differently** than Governance/Disposition use "outcome"?
- Is the shared head word **intentional** (a deliberate family) or incidental?
- Does the **ambiguity matter** enough to act on, given its limited downstream reach?

---

## 6. Dependency Analysis (mapping only — no recommendations)

| Decision area | Constrains future Knowledge Layer work? | Constrains future Truth Promotion work? | Affects only terminology? |
|---|---|---|---|
| #1 Accepted / Acceptance | **Yes** — the Knowledge Layer consumes the "accepted" state | **Yes** — truth promotion builds on accepted understanding | No (has downstream reach) |
| #2 Governed vs Accepted Understanding | **Yes** — the Knowledge Layer consumes the governed endpoint term | **Yes** — what is promoted depends on the endpoint definition | No (has downstream reach) |
| #3 Outcome | Low / minimal | Low / minimal | **Largely yes** (Understanding-Domain flagship term, locally contained) |
| Secondary findings (§2 of Decision 001) | No | No | **Yes** (local hygiene) |

**Coupling note:** #1 and #2 both bear on the **terminal governed state** (one names it, one governs the acceptance word that produces it); they are interdependent and the downstream layers inherit both.

---

## 7. Future Model Impact Matrix (no recommendations)

| Future Area | Dependent On Which Decision |
|---|---|
| **Knowledge Layer** | #1 (accepted state) and #2 (endpoint term it consumes) |
| **Truth Promotion** | #1 and #2 (promotes the accepted/governed understanding) |
| **Canonical Knowledge** | #1 and #2 (what is recorded as canonical inherits the endpoint meaning) |
| **Audit Models** | #1 (the acceptance/outcome lifecycle vocabulary appears in any audit lineage); partly #2 |
| **Notification** | Minimal / indirect (a future Notification surfacing "accepted" events would inherit #1's meaning, but Notification defines no governance judgment) |

*Mapping only; no future model is designed, proposed, or required by this table.*

---

## 8. Founder Response Template

*To be completed by the founder. Left intentionally blank. Capturing a response here records a decision; it does not change any model — implementation would follow separately, under founder direction.*

### Decision Area #1 — Accepted / Acceptance
- **Decision Area:** Accepted / Acceptance
- **Selected Option:** ______________________________________________
- **Reasoning:** ______________________________________________
- **Impacted Concepts:** ______________________________________________
- **Follow-up Required:** ______________________________________________

### Decision Area #2 — Governed Understanding vs Accepted Understanding
- **Decision Area:** Governed Understanding vs Accepted Understanding
- **Selected Option:** ______________________________________________
- **Reasoning:** ______________________________________________
- **Impacted Concepts:** ______________________________________________
- **Follow-up Required:** ______________________________________________

### Decision Area #3 — Outcome
- **Decision Area:** Outcome
- **Selected Option:** ______________________________________________
- **Reasoning:** ______________________________________________
- **Impacted Concepts:** ______________________________________________
- **Follow-up Required:** ______________________________________________

### Secondary Findings (optional)
- **Decision Area:** ______________________________________________
- **Selected Option:** ______________________________________________
- **Reasoning:** ______________________________________________
- **Impacted Concepts:** ______________________________________________
- **Follow-up Required:** ______________________________________________

---

## 9. Final Assessment

- **The architecture is structurally complete.** Both prior audits found the model set complete and internally consistent in structure; nothing here reflects a structural defect.
- **The remaining work is semantic.** Every open item is a vocabulary decision — an overloaded word, an unsettled endpoint term, a shared head word — not a missing or conflicting mechanism.
- **Decisions should be captured before Knowledge Layer modeling begins.** Decision Areas #1 and #2 define the terminal governed state that future Knowledge Layer and Truth Promotion work would consume; capturing them first prevents the ambiguity from propagating into that layer.

This workbook proposes no solution and chooses no option. It prepares the decisions and provides the means to record them.

---

## Verification

- **No terminology changed** — confirmed (terms are quoted and analyzed; none altered or redefined).
- **No model modified** — confirmed (this is a separate workbook; the reviewed documents are referenced only).
- **No doctrine introduced** — confirmed.
- **No architecture redesigned** — confirmed (no mechanism, model, or relationship is changed or proposed).
- **Only decision-facilitation material produced** — confirmed (usage inventories, consequences, founder questions, dependency mapping, and a blank response template; no answers, no selected options).

*Founder Terminology Decision Workbook 001 complete. A decision-facilitation workbook for three High-Risk terminology collisions (Accepted/Acceptance; Governed vs Accepted Understanding; Outcome) plus secondary findings, with per-area usage inventories, architectural consequences, explicit founder questions, dependency and future-model impact mapping, and a blank response template. No terminology changed, no model modified, no decision made.*
