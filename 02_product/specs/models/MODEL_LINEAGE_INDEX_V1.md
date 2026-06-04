# Model Lineage Index v1

**Document:** MODEL_LINEAGE_INDEX_V1.md
**Status:** Informational architecture map (navigational index, onboarding guide, governance review aid)
**Architecture V1 classification (per founder decision):** **Active Architecture V1 (Planning Intelligence)** = CAF Assessment · CAF Scoring · Reliability · Confidence · MRI · Overlay · Finding · Recommendation · **Notification**. **Future Architecture (Outcome Orchestration / Agent Governance)** = Resolution Candidate · Review Request · Disposition · Governance · Accepted Understanding (preserved and specified; **not part of active V1**).
**Indexes (authoritative, unmodified):** `CAF_ASSESSMENT_MODEL_V1.md` · `CAF_SCORING_MODEL_V1.md` · `RELIABILITY_MODEL_V1.md` · `CONFIDENCE_MODEL_V1.md` · `MRI_MODEL_V1.md` · `OVERLAY_MODEL_V1.md` · `FINDING_MODEL_V1.md` · `RECOMMENDATION_MODEL_V1.md` · `RESOLUTION_CANDIDATE_MODEL_V1.md` · `REVIEW_REQUEST_MODEL_V1.md` · `DISPOSITION_MODEL_V1.md` · `GOVERNANCE_MODEL_V1.md` · `ACCEPTED_UNDERSTANDING_MODEL_V1.md` · `NOTIFICATION_MODEL_V1.md`
**Date:** 2026-05-31

> **Nature of this document.** This is an **index and architecture map**. It is **informational, not normative**. It introduces no new doctrine, defines no new model, and does not reinterpret or modify any existing model. Every statement here is drawn from the fourteen authoritative documents listed above; where this index and a model document appear to differ, the model document governs.
>
> **Governance.** Non-canonical navigational artifact; the indexed model documents remain the authority. Canonical terminology is preserved.

---

## 1. Purpose

Provide a single map of OSLO's current model architecture that:

- maps the complete model architecture;
- shows the conceptual flow between models;
- shows model dependencies;
- shows consumes / extends relationships;
- shows the descriptive vs prescriptive boundary;
- separates the Understanding Domain from the Governance Domain;
- helps future contributors understand where new models belong.

It serves three audiences: a **new contributor** orienting to the model set, a **governance reviewer** checking that a proposal fits the architecture, and an **author** deciding where a new model belongs.

---

## 2. Architectural Overview

OSLO's currently specified models form a single, closed **understanding-improvement loop**. The conceptual chain:

```text
Evidence
  ↓
Inference
  ↓
Finding
  ↓
Impact Assessment
  ↓
CAF
  ↓
Reliability
  ↓
Outcome Confidence
  ↓
MRI
  ↓
Overlay
  ↓
Recommendation
  ↓
User Action
  ↓
Evidence
```

This chain represents the **complete understanding-improvement loop currently defined by OSLO**. Evidence and inference produce Findings; Findings, through Impact Assessment, inform CAF; CAF (qualified by Reliability) yields Outcome Confidence; MRI makes the assessment observable; Overlays manage attention within it (bringing Findings to attention, as established in the Overlay and Finding models); Recommendations suggest improvement paths that operate on Findings; and **User Action** — not the Recommendation itself — produces new Evidence, returning to the top of the chain. The loop closes at User Action: improvement re-enters as evidence, and the chain re-runs.

All eight currently specified models live within this loop. They constitute the **Understanding Domain** (Sections 3–4) — the heart of **Active Architecture V1**, a **Planning Intelligence / Understanding-Improvement System**. The active V1 loop is **Evidence → Understanding → Assessment → Recommendation → User Action → Updated Evidence**; governance does not appear in it. A **supporting service**, **Notification** (Section 8), is part of **Active Architecture V1**; it surfaces awareness of changes to Findings, Recommendations, and understanding improvements without belonging to the loop.

Per the founder decision, the **Governance Domain** (Section 7) — Resolution Candidate, Review Request, Disposition, Governance, and Accepted Understanding — is **Future Architecture (Outcome Orchestration / Agent Governance)**: fully specified and preserved, but **not part of active Architecture V1**. The architecture therefore presents two classifications: **Active Architecture V1** (the eight Understanding Domain models + the Notification supporting service) and **Future Architecture** (the five Governance Domain models).

```text
Active Architecture V1 (Planning Intelligence)
  CAF Assessment · CAF Scoring · Reliability · Confidence · MRI · Overlay · Finding · Recommendation
  + Notification (Supporting Service)

Future Architecture (Outcome Orchestration / Agent Governance) — specified, preserved, deferred
  Resolution Candidate · Review Request · Disposition · Governance · Accepted Understanding
```

*Informational note (Active V1 only): active V1 understanding may be produced and improved through two analysis horizons — a **Fast Analysis Pass** (the 60-Second Orientation) and a **Deep Analysis Pass** (continuing after orientation to recalculate confidence and expand findings and recommendations). Both horizons are Active V1 within the Understanding-improvement loop; Deep Analysis improves understanding and is not a Governance or Future-Architecture capability. This note alters no Understanding-Domain, Governance-Domain, or Future-Architecture classification.*

---

## 3. Understanding Domain Overview

**Models:** CAF Assessment · CAF Scoring · Reliability · Confidence · MRI · Overlay · Finding · Recommendation.

**Purpose:** to **understand reality, assess that understanding, and improve it.**

**Primary questions the domain answers:**

- *What do we understand?*
- *How well do we understand it?*
- *What should we do to improve it?*

The Understanding Domain is **fully specified** by the eight authoritative documents. It spans the entire chain of Section 2 — from raw evidence through assessment, visualization, attention, and prescriptive improvement, back to action.

---

## 4. Understanding Domain Model Lineage

For each model: its purpose, what it consumes, what it produces, and its relationship to neighboring models — drawn only from the authoritative documents.

### CAF Assessment Model
- **Purpose:** Defines how CAF reasons about the **integrity of project understanding** across three independent dimensions (Clarity, Alignment, Feasibility), and defines the flat finding taxonomy and the Impact Assessment concept.
- **Consumes:** Evidence, Inference, Findings, and Impact Assessments (as reasoning inputs).
- **Produces:** The CAF assessment (the reasoning model) — the integrity assessment, the flat finding taxonomy, and the Impact Assessment factors.
- **Relationship to neighbors:** Foundational. Everything downstream depends on CAF. It defines *how CAF reasons*; the CAF Scoring Model defines *how that reasoning is scored*.

### CAF Scoring Model
- **Purpose:** Defines how the CAF assessment becomes a **represented, explainable score** per dimension — without fixing calibration.
- **Consumes:** The CAF Assessment Model (impact-assessed findings, evidence, coverage).
- **Produces:** Per-dimension CAF scores, each a triple of integrity index + state band + coverage-governed reliability qualifier, plus the explanation basis.
- **Relationship to neighbors:** Sits directly on top of the CAF Assessment Model. Its coverage-governed reliability qualifier connects to the Reliability Model; its scores feed Outcome Confidence.

### Reliability Model
- **Purpose:** Defines **Assessment Reliability** — the trustworthiness / supportability of the CAF assessment.
- **Consumes:** Coverage, Evidence Availability, and Assessability (conditions of the evidence surface). Determined **independently of CAF and of findings**.
- **Produces:** The Reliability signal (supportability of the assessment), distinct from CAF.
- **Relationship to neighbors:** Distinct from CAF (integrity) and from Confidence (summary). Consumed by Outcome Confidence; exposed by MRI as a first-class signal.

### Confidence Model
- **Purpose:** Defines **Outcome Confidence** — the summarized signal of how much to trust the current understanding.
- **Consumes:** CAF Assessment and Assessment Reliability (its only two inputs).
- **Produces:** Outcome Confidence — a constrained, reliability-qualified summary signal.
- **Relationship to neighbors:** Downstream of CAF and Reliability. Consumes both; is exposed (not calculated) by MRI.

### MRI Model
- **Purpose:** The **visualization layer** that makes project understanding observable.
- **Consumes:** CAF, Reliability, and Outcome Confidence, plus visibility into contributing Findings.
- **Produces:** The observable representation of project understanding (descriptive), exposing Reliability as first-class.
- **Relationship to neighbors:** Consumer of the assessment layers (CAF, Reliability, Confidence) and of Finding visibility. Consumed in turn by Overlays.

### Overlay Model
- **Purpose:** **Attention-management** lenses applied to MRI.
- **Consumes:** MRI (already-assessed, already-visible understanding) — never raw evidence.
- **Produces:** Alternate, emphasis-adjusted, deterministic views of MRI (descriptive); may emphasize, suppress, filter, or group without distorting.
- **Relationship to neighbors:** Consumes MRI; occupies the attention layer between MRI and Recommendations. Brings Findings to attention.

### Finding Model
- **Purpose:** Defines the **Finding as a governable object** between assessment and action (extending, not replacing, the Assessment Model's finding definition).
- **Consumes:** Produced through assessment; relates to CAF via Impact Assessment. Carries lifecycle state, relationships, grouping, and ownership.
- **Produces:** Governable Finding objects — the actionable unit of the loop.
- **Relationship to neighbors:** Dual role — an *input to assessment* (Finding → Impact Assessment → CAF) and the *actionable object* surfaced by MRI/Overlay that Recommendations operate on. Findings remain descriptive.

### Recommendation Model
- **Purpose:** The **prescriptive, advisory** suggestion intended to improve understanding.
- **Consumes:** Assessment context — Findings, CAF, Reliability, and Outcome Confidence (consumes, does not create).
- **Produces:** Advisory suggested improvement paths that operate on Findings; influences assessment signals only through user action.
- **Relationship to neighbors:** Operates on Findings (not directly on CAF); the hinge that closes the loop via User Action → new Evidence.

---

## 5. Model Responsibility Matrix

| Model | Primary Responsibility |
|---|---|
| CAF Assessment | Reason about the integrity of project understanding across Clarity, Alignment, Feasibility |
| CAF Scoring | Represent and explain CAF as a per-dimension score, deferring calibration |
| Reliability | Measure the supportability/trustworthiness of the CAF assessment, independently of CAF |
| Confidence | Summarize CAF, qualified by Reliability, into Outcome Confidence |
| MRI | Make project understanding observable (visualization layer) |
| Overlay | Manage attention within MRI without altering understanding |
| Finding | Define the governable object between assessment and action |
| Recommendation | Prescribe advisory improvement paths that operate on Findings |
| Resolution Candidate | Defines proposed resolutions to Findings as governance objects |
| Review Request | Requests evaluation of one or more Resolution Candidates |
| Disposition | Records the outcome of an evaluation |
| Governance | Determines whether understanding may be accepted |
| Accepted Understanding | Represents the durable, governed output of Governance |
| Notification | Surface awareness of relevant changes, requests, events, and governance activity without altering the underlying objects |

*(Classification per founder decision: the first eight rows are **Active Architecture V1** (Understanding Domain) models; the next five are **Future Architecture** (Governance Domain → Outcome Orchestration / Agent Governance) models, preserved and specified but **not active V1**; the last, Notification, is an **Active Architecture V1 Supporting Service**.)*

---

## 6. Descriptive vs Prescriptive Boundary

The architecture draws one intentional, load-bearing line:

**Descriptive models** (they describe and assess; they do not tell the user what to do):

- CAF Assessment
- CAF Scoring
- Reliability
- Confidence
- MRI
- Overlay
- Finding

**Prescriptive model** (it suggests what to do):

- Recommendation

**Findings describe. Recommendations prescribe.** A Finding states *what was observed about understanding*; a Recommendation suggests *what to do about it*. Everything from Evidence through Finding — assessment, scoring, supportability, summary, visualization, attention — is descriptive; only the Recommendation crosses into prescription, and even then only advisorily, with user action remaining the sole thing that changes understanding.

**This boundary is intentional and must be preserved.** It is what keeps OSLO's assessment honest (no layer prescribes its way into changing its own inputs) and keeps human authority intact (the one prescriptive layer is advisory). A new model should be placed on the correct side of this line and must not blur it.

---

## 7. Governance Domain Overview

**Classification: Future Architecture (deferred).** Per the founder decision, the **Governance Domain is not part of active Architecture V1.** It is **Future Architecture — Outcome Orchestration / Agent Governance / Enterprise Governance / Autonomous Execution** — fully specified and preserved for later activation, but not active V1 runtime architecture and not required for V1 planning operation. The five governance models (Resolution Candidate, Review Request, Disposition, Governance, Accepted Understanding) define how assessed understanding *would* move toward, and be recorded as, accepted understanding **once governance is activated**. The **Notification** supporting service (Section 8) is part of active V1 and does **not** require Governance Domain participation; it supports the Understanding Domain (Findings, Recommendations, awareness of changes).

**Future governance lineage (not an active V1 chain).** When governance is activated as Future Architecture, the five governance models would form the chain by which understanding becomes governed, ending in Accepted Understanding. **No active Architecture V1 lineage terminates in Accepted Understanding**; the active V1 loop closes at User Action → Updated Evidence (Section 2). The chain below is preserved as the specified future lineage:

```text
Finding
  ↓
Resolution Candidate
  ↓
Review Request
  ↓
Human Evaluation (external)
  ↓
Disposition
  ↓
Governance
  ↓
Accepted Understanding
```

**Human Evaluation** sits conceptually between Review Request and Disposition — a Review Request asks for evaluation, the evaluation occurs, and a Disposition records its outcome. Human Evaluation is **external to the models**: none of the governance models performs it; they establish the objects around it.

**Purpose (as an area):** to **govern, validate, and control understanding** — the questions that arise once understanding has been assessed and improvement suggested:

- *Who decides?*
- *Who reviews?*
- *Who owns?*
- *What becomes truth?*
- *What requires validation?*

These concerns belong to **Future Architecture**, not active V1. The specified governance models would address them — validation (Review Request), recorded outcomes (Disposition), acceptance (Governance), and the durable governed output (Accepted Understanding), with proposed resolutions (Resolution Candidate) as the entry point — **when governance is activated for Outcome Orchestration / Agent Governance.** **This index defines none of their behavior**; each is specified in its own document. Surfacing awareness of relevant changes is handled in active V1 by the **Notification** supporting service (Section 8), which supports the Understanding Domain and performs no governance.

---

## 8. Future Model Expansion Areas

Active Architecture V1 contains the eight Understanding Domain models plus the Notification supporting service. The five Governance Domain models are **Future Architecture** — specified and preserved, deferred to Outcome Orchestration / Agent Governance. No *unspecified* named future models remain.

**Future Architecture — Governance Domain Models (Outcome Orchestration / Agent Governance)** — *specified and preserved; not part of active Architecture V1*

- **Resolution Candidate Model** — defines proposed resolutions to Findings as governance objects that bridge Understanding and Governed Understanding. *(Specified: `RESOLUTION_CANDIDATE_MODEL_V1.md`.)*
- **Review Request Model** — defines the governance object that requests evaluation of one or more Resolution Candidates, bridging Proposed Resolution and Human Evaluation. *(Specified: `REVIEW_REQUEST_MODEL_V1.md`.)*
- **Disposition Model** — defines the governance object that records evaluation outcomes, bridging Human Evaluation and Governed Outcome Recording. *(Specified: `DISPOSITION_MODEL_V1.md`.)*
- **Governance Model** — defines the acceptance layer that bridges Understanding and Accepted Understanding. *(Specified: `GOVERNANCE_MODEL_V1.md`.)*
- **Accepted Understanding Model** — defines the durable, governed output of Governance and the bridge to future Knowledge Layer concepts. *(Specified: `ACCEPTED_UNDERSTANDING_MODEL_V1.md`.)*

**Specified Supporting Services**

- **Notification Model** — surfaces awareness of relevant changes, requests, and events across both domains; a supporting service that supports awareness and delivery, belongs to neither primary chain, and performs no assessment, governance, or decisions. *(Specified: `NOTIFICATION_MODEL_V1.md`.)*

**Future Expansion Areas**

Beyond the specified models, the further frontier is **Future Architecture**: Outcome Orchestration, Agent Governance, Enterprise Governance, and Autonomous Execution, which the five Governance Domain models support. The **Knowledge Layer** is treated as an existing, active capability and is **not gated by the Future-Architecture Governance Domain**; in active Architecture V1 it carries no Accepted-Understanding prerequisite, no governance gate, and no governance-promotion requirement. Any Accepted-Understanding → Knowledge-Layer relationship is a **future Outcome-Orchestration relationship**, not an active V1 dependency. This index neither defines nor redesigns the Knowledge Layer.

---

## 9. Architectural Principles

Principles already established across the model lineage, restated here for navigation (no new principle is introduced):

- **Event-driven** — every model updates only when understanding changes, never on the passage of time alone (established across CAF, Reliability, Confidence, MRI, Overlay, Finding, Recommendation).
- **Explainable** — every signal and object is traceable to its basis (CAF Scoring, Confidence, Reliability, MRI, Recommendation).
- **Human authority preserved** — Recommendations are advisory; user action alone changes understanding (Recommendation Model).
- **Findings descriptive** — Findings describe observations; they do not prescribe (Finding Model).
- **Recommendations prescriptive** — Recommendations prescribe advisory improvement paths (Recommendation Model).
- **Reliability distinct from CAF** — supportability is independent of integrity (Reliability Model).
- **Confidence distinct from CAF and Reliability** — Confidence summarizes; CAF assesses; Reliability qualifies (Confidence Model).
- **MRI consumes assessments** — MRI visualizes CAF, Reliability, and Confidence without altering them (MRI Model).
- **Overlays manage attention** — Overlays adjust salience over MRI without distorting understanding (Overlay Model).
- **Recommendations operate on Findings** — the Finding is the actionable object; CAF is context (Finding and Recommendation Models).

Governance Domain principles already established by the governance model set — these describe **Future Architecture (Outcome Orchestration / Agent Governance)** and are **not active Architecture V1 principles**; they are preserved for when governance is activated:

- **Governance distinct from assessment** — assessment and acceptance are separate responsibilities (Governance Model).
- **Acceptance distinct from understanding** — understanding is assessed; accepted understanding is governed (Governance and Accepted Understanding Models).
- **Human evaluation external** — human evaluation sits conceptually in the governance lineage but is external to the specified models (Review Request and Disposition Models).
- **Governance objects do not perform their downstream responsibility** — a Review Request requests but does not evaluate; a Disposition records but does not decide; Governance governs acceptance but does not assess (governance model set).
- **Accepted understanding preserves history** — reconsideration and supersession retain prior governed outcomes (Accepted Understanding and Disposition Models).
- **Governance outcomes explainable to their basis** — each governance object traces to the Finding and prior governance objects that produced it (governance model set).
- **Governance outcomes event-driven** — governance objects change only when governance context changes, never on time alone (governance model set).

Supporting Service (Notification) principles already established by the Notification Model:

- **Notifications support awareness, not assessment** — a Notification surfaces awareness; it performs no assessment (Notification Model).
- **Notifications support awareness, not governance** — a Notification surfaces awareness; it performs no governance and makes no decisions (Notification Model).
- **Notifications explainable** — every Notification traces to the object, event, or change that produced it (Notification Model).
- **Notifications event-driven** — Notifications arise from relevant changes or events, never from the passage of time alone (Notification Model).
- **Notifications preserve awareness history** — delivered or historical Notifications remain part of the awareness record (Notification Model).
- **Notifications alter no underlying object** — a Notification surfaces awareness of a change; it changes nothing it announces (Notification Model).

---

## 10. Summary

OSLO's currently specified models form one closed understanding-improvement loop: Evidence → Inference → Finding → Impact Assessment → CAF → Reliability → Outcome Confidence → MRI → Overlay → Recommendation → User Action → Evidence. Eight models populate this loop — CAF Assessment and CAF Scoring (assess and score integrity), Reliability (supportability), Confidence (summary trust), MRI (visualization), Overlay (attention), Finding (the governable actionable object), and Recommendation (the advisory prescriptive suggestion). Together they constitute the **Understanding Domain**, which is fully specified and answers what we understand, how well, and what to do to improve it.

A single intentional boundary runs through Active Architecture V1: seven descriptive models and one prescriptive model — Findings describe, Recommendations prescribe — with user action the only thing that changes understanding. **Active Architecture V1 is a Planning Intelligence / Understanding-Improvement System**: its loop is Evidence → Understanding → Assessment → Recommendation → User Action → Updated Evidence, and **governance does not appear in it.**

Per the founder decision, the five **Governance Domain** models — Resolution Candidate, Review Request, Disposition, Governance, Accepted Understanding — are **Future Architecture (Outcome Orchestration / Agent Governance / Enterprise Governance / Autonomous Execution)**: fully specified and preserved, but **not part of active Architecture V1**. When activated they would carry assessed understanding toward accepted understanding (Finding → Resolution Candidate → Review Request → Human Evaluation (external) → Disposition → Governance → Accepted Understanding); **no active V1 lineage terminates in Accepted Understanding.**

OSLO's documented model set comprises **fourteen specified models**: **Active Architecture V1 = nine** — eight Understanding Domain models + the Notification supporting service; **Future Architecture = five** — the Governance Domain models, preserved and deferred. The **Knowledge Layer** is treated as an existing active capability, not gated by the Future-Architecture governance chain. This document is an informational map of that architecture; it defines nothing new and points to where everything already defined lives.

---

## Validation

**Understanding Domain — all eight models represented**

| Model | Section 4 lineage | Responsibility matrix (§5) | Descriptive/Prescriptive (§6) |
|---|---|---|---|
| CAF Assessment | ✓ | ✓ | Descriptive |
| CAF Scoring | ✓ | ✓ | Descriptive |
| Reliability | ✓ | ✓ | Descriptive |
| Confidence | ✓ | ✓ | Descriptive |
| MRI | ✓ | ✓ | Descriptive |
| Overlay | ✓ | ✓ | Descriptive |
| Finding | ✓ | ✓ | Descriptive |
| Recommendation | ✓ | ✓ | Prescriptive |

**Future Architecture — Governance Domain models (specified, preserved, not active V1)**

| Model | Classification | Responsibility matrix (§5) | Future lineage (§7) | Specified list (§8) |
|---|---|---|---|---|
| Resolution Candidate | Future Architecture | ✓ | ✓ | ✓ |
| Review Request | Future Architecture | ✓ | ✓ | ✓ |
| Disposition | Future Architecture | ✓ | ✓ | ✓ |
| Governance | Future Architecture | ✓ | ✓ | ✓ |
| Accepted Understanding | Future Architecture | ✓ | ✓ (future endpoint) | ✓ |

**Supporting Services — Notification represented**

| Model | Responsibility matrix (§5) | Architecture role (§2, §3, §4) | Specified list (§8) |
|---|---|---|---|
| Notification | ✓ | ✓ (supporting service; belongs to neither primary chain) | ✓ |

**Checklist**
- No existing model modified — confirmed (this is an index; the fourteen documents are referenced only).
- No new doctrine introduced — confirmed (all content drawn from the authoritative documents).
- No new scoring models introduced — confirmed.
- No new governance behavior introduced — confirmed (the five specified Governance Domain models are referenced via their own documents; no governance behavior is defined here).
- All fourteen specified models represented — confirmed (eight Understanding + five Governance + one Supporting Service; tables above).
- Understanding Domain accurately described and unchanged — confirmed (§3, §4; lineage and descriptive/prescriptive boundary preserved).
- Active Architecture V1 = nine models — confirmed (§2, §5, §10): eight Understanding Domain + Notification supporting service.
- Governance Domain reclassified as Future Architecture — confirmed (§2, §5, §7, §8, §9, §10): five models, specified and preserved, **not active V1**; no active V1 lineage terminates in Accepted Understanding.
- Notification active in V1 — confirmed (§2, §5, §8): a Supporting Service that supports the Understanding Domain and requires no Governance Domain participation.
- Knowledge Layer active and not governance-gated — confirmed (§8): no Accepted-Understanding prerequisite or governance promotion requirement in active V1.
- Human Evaluation remains external — confirmed (present only in the future governance lineage, external to the specified models; §7, §10).
- Descriptive vs Prescriptive boundary preserved — confirmed (§6: 7 descriptive, 1 prescriptive, all within Active V1).
- Conceptual chains represented accurately — confirmed (§2 active V1 loop; §7 future governance lineage preserved verbatim).
- No governance model modified, deleted, or invalidated — confirmed (reclassified only; content preserved).

*Model Lineage Index v1 complete. An informational, non-normative map classifying the fourteen specified models into **Active Architecture V1** (eight Understanding Domain models + the Notification supporting service — a Planning Intelligence / Understanding-Improvement System) and **Future Architecture** (five Governance Domain models, preserved and deferred to Outcome Orchestration / Agent Governance). Governance is not part of active V1; no active lineage terminates in Accepted Understanding. Introduces no new doctrine and modifies no governance model.*
