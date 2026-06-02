# Outcome Confidence Stack Index

**Type:** Governance & navigation artifact (map / lineage / maintenance guide — **not** doctrine, calibration, or implementation)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Read this first** before modifying *any* Outcome Confidence artifact.

> **What this document is and is not.** It defines the **structure, authority hierarchy, and relationships** of the Outcome Confidence document stack. It creates **no** doctrine, calibration, formulas, scores, thresholds, or governance decisions, and **modifies no existing document**. It only **describes existing relationships** and the rules for maintaining them.

---

## 1. Purpose of the Outcome Confidence Stack

The Outcome Confidence concept is developed across several documents, each answering a *different kind* of question, in a deliberate progression from **what the repository implies** to **what it means** to **how it is measured** to **how it is built**:

```text
Discovery  →  Decision  →  Interpretation  →  Leadership  →  Calibration  →  Implementation
(what is    (what it     (what each       (what it      (how it is     (how it is
 implied)    IS)          state means)     means to a    measured —     realized in
                                            leader)       principles)    models/code)
```

The stack exists so that **meaning is fixed before measurement, and measurement before implementation** — preventing the most common failure mode (an engineer or designer silently redefining what confidence *means* while choosing how to *score* it). Each layer **constrains the ones below it** and **may not redefine the ones above it**.

---

## 2. Authority Hierarchy

| Level | Document | Authority type | May override… | May NOT override… |
|---|---|---|---|---|
| **Source models** | CAF Assessment · CAF Scoring · Reliability · Confidence Models | Founder-position doctrine (upstream) | — | — (these are the doctrinal source) |
| **L0 · Doctrine (binding meaning)** | `OUTCOME_CONFIDENCE_DOCTRINE_DECISION_001.md` | **Authoritative** — fixes meaning | Discovery | Source models |
| **L0-support · Reconstruction** | `OUTCOME_CONFIDENCE_DOCTRINE_DISCOVERY_V1.md` | **Informative** (archaeology; non-binding) | — | Everything (superseded by Decision where they differ) |
| **L1 · Interpretation** | `OUTCOME_CONFIDENCE_INTERPRETATION_DOCTRINE_001.md` | **Derived** from L0 | — | L0, Source models |
| **L2 · Leadership** | `OUTCOME_CONFIDENCE_LEADERSHIP_DOCTRINE_001.md` | **Derived** from L1 + L0 | — | L1, L0 |
| **L3 · Calibration** | `OUTCOME_CONFIDENCE_CALIBRATION_DECISION_001.md` | **Derived** — binds implementation; principles only | — | L0–L2 (may not redefine meaning) |
| **L4 · Models (realization)** | `CONFIDENCE_MODEL_V2.md` · `CAF_SCORING_MODEL_V2.md` · `RELIABILITY_MODEL_V2.md` *(future)* | **Implementation-doctrine** — realizes L3 | — | L0–L3 |
| **L5 · Implementation** | Engine/Testing/UI realizations · Determinism Calibration Note *(future)* | **Implementation** | — | L0–L4 |

**Reading the hierarchy.** Authority flows **downward**: each level is bound by every level above it. **Discovery is informative only** — it reconstructs what the repository implies and is explicitly superseded by Doctrine Decision 001 where they differ. **Calibration is derived, not foundational** — it chooses *which principle governs measurement* but may never alter meaning. **Models and implementation realize; they never redefine.**

---

## 3. Document Roles

### `OUTCOME_CONFIDENCE_DOCTRINE_DISCOVERY_V1.md`
- **Purpose:** Reconstruct, from repository evidence, the doctrine the corpus already implies (incl. a Founder Annotation).
- **Key questions answered:** What does the repository already imply Outcome Confidence is / is not / how it relates to CAF, Reliability, findings, Fast/Deep?
- **What it must never do:** Create doctrine; bind any lower layer; override Decision 001.
- **Dependencies:** The source models + whole repository (read-only).
- **Future consumers:** Decision 001 (which accepts/refines its implications).

### `OUTCOME_CONFIDENCE_DOCTRINE_DECISION_001.md`
- **Purpose:** Establish, explicitly and authoritatively, the **meaning** of Outcome Confidence for Release 1.
- **Key questions answered:** What *is* Outcome Confidence? What is it *not*? Its relationship to CAF/Reliability; evolution; Deep-Analysis decline; representation; future boundary.
- **What it must never do:** Define measurement (formulas/scores/thresholds); introduce probability; create future architecture.
- **Dependencies:** Discovery (informative); source models (consistent-with).
- **Future consumers:** Interpretation, Leadership, Calibration, all Models.

### `OUTCOME_CONFIDENCE_INTERPRETATION_DOCTRINE_001.md`
- **Purpose:** Define the **human meaning of each confidence state**.
- **Key questions answered:** What does Very Low / Low / Moderate / High / Very High mean? How is reliability read? What do trends mean?
- **What it must never do:** Redefine meaning (L0); prescribe actions; introduce measurement.
- **Dependencies:** Decision 001.
- **Future consumers:** Leadership, UI, Calibration (meaning to conform to), Models.

### `OUTCOME_CONFIDENCE_LEADERSHIP_DOCTRINE_001.md`
- **Purpose:** Define **what confidence means to a leader** (posture, not procedure).
- **Key questions answered:** How should a leader hold the signal in judgment? Accountability? Misinterpretations to avoid?
- **What it must never do:** Redefine interpretation/meaning; prescribe decisions; introduce governance/automation.
- **Dependencies:** Interpretation 001 + Decision 001.
- **Future consumers:** Product/UX framing; future governance (above this layer).

### `OUTCOME_CONFIDENCE_CALIBRATION_DECISION_001.md`
- **Purpose:** Settle **calibration principles** (which existing principle governs measurement); includes Calibration Invariants.
- **Key questions answered:** How should CAF/Reliability synthesize *conceptually*? Severity basis? Determinism principle? (No numerics.)
- **What it must never do:** Redefine meaning; create formulas/weights/thresholds; introduce probability/governance/future architecture.
- **Dependencies:** Decision 001, Interpretation 001, Leadership 001, Discovery, Calibration Workbook.
- **Future consumers:** Confidence Model v2, CAF Scoring v2, Reliability v2, Determinism Calibration Note, Testing.

### Future: `CONFIDENCE_MODEL_V2.md` · `CAF_SCORING_MODEL_V2.md` · `RELIABILITY_MODEL_V2.md` · Determinism Calibration Note
- **Purpose:** **Realize** the calibrated principles as concrete scales, synthesis, and tolerances.
- **What they must never do:** Redefine meaning (L0–L2) or calibration principles/invariants (L3); introduce probability.
- **Dependencies:** Calibration Decision 001 (+ all meaning docs).
- **Future consumers:** Engine/Testing/UI implementation.

---

## 4. Doctrine Flow

```text
Discovery ──(implications accepted/refined)──▶ Decision ──▶ Interpretation ──▶ Leadership
```

- **Allowed downstream:** meaning fixed at Decision flows into Interpretation (state meaning) and Leadership (leader posture). Each lower layer **inherits and specializes** the layer above.
- **Forbidden upstream:** Interpretation may not change Decision; Leadership may not change Interpretation or Decision; nothing downstream may add to or contradict the meaning established upstream. **Information specializes as it descends; it never rewrites its source as it ascends.**

---

## 5. Calibration Flow

```text
Doctrine (meaning) ──▶ Calibration (principles) ──▶ Model Realization (numbers)
```

- **Calibration cannot redefine doctrine.** The Calibration Decision selects *which principle governs measurement*; it is bound by the fixed meaning and may never alter it (e.g., it may not make confidence a probability).
- **Implementation cannot redefine calibration.** The v2 models realize the principles/invariants; they may choose scales and arithmetic *only within* the calibrated principles and must preserve the Calibration Invariants (Confidence Stability, Explainability/Attribution, Reliability Non-Collapse).

---

## 6. Future Model Layer

| Future artifact | Expected to realize | Prohibited from changing |
|---|---|---|
| **`CONFIDENCE_MODEL_V2.md`** | The consolidate-then-qualify synthesis (between an average and a minimum) + band boundaries; preserve invariants | Meaning (L0–L2); the synthesis *properties*; the confidence-in-understanding definition |
| **`CAF_SCORING_MODEL_V2.md`** | CAF index scale; Impact-Assessment-driven assignment/magnitude; severity expression | Dimension independence/co-equality; "magnitude from Impact Assessment, not type" |
| **`RELIABILITY_MODEL_V2.md`** | Reliability level scale + non-formula determination from Coverage/Evidence/Assessability | Reliability's qualifier role; non-collapse invariant; determination-independent-of-findings |
| **Determinism Calibration Note** | Bounded-equivalence tolerance + regression-gate definition | The determinism *principle*; replay-exactness; per-config baseline rule |

Each realizes numbers/mechanics **only**; none may touch meaning or the calibrated principles.

---

## 7. Future Outcome Probability Boundary

**Existing doctrine (summary, not new):**

> **Outcome Confidence = trust in OSLO's current understanding of project reality.**
> **Outcome Probability (potential future) = an estimated likelihood of outcome achievement.**

These answer **different questions** and must remain **distinct signals** (Decision 001 §10, Option A; Discovery §F.2; Leadership §11).

**If a probability model is ever introduced, it must:**
- be a **separate** signal/artifact (not a redefinition of confidence);
- **not redefine** Outcome Confidence;
- **not modify** any existing Outcome Confidence doctrine;
- carry its own future doctrinal review.

This index **does not design Outcome Probability** — it only records the boundary. "Outcome Probability" remains **future-only terminology**, not part of Release 1.

---

## 8. Change Governance Rules

- **Modifiable with care (within their layer):** lower layers may be revised to better conform to higher ones (e.g., a clarity patch to Interpretation), via the governance lifecycle.
- **Require a governance decision:** any change to **Decision 001** (meaning) or **Calibration Decision 001** (principles/invariants); any new doctrine; any new calibration; introduction of any probability concept.
- **Conflict resolution:** **higher-authority documents win.** If two documents conflict, the one **higher** in the §2 hierarchy governs, and the lower document is the one corrected. Discovery loses to every other doctrine document.
- **How future doctrine changes should occur:** Backlog → Proposal → Review → Decision → Repository Change → Changelog (repository governance lifecycle). No layer self-ratifies; the repository owner ratifies.
- **Drift prevention:** every new/edited artifact must declare its layer and its "must never do," and must cite the higher layers it conforms to (as the existing stack documents do).

---

## 9. Stack Dependency Diagram

```text
            [ Source models: CAF Assessment · CAF Scoring · Reliability · Confidence ]
                                        │  (founder-position doctrine)
                                        ▼
Outcome Confidence Doctrine Discovery   ── informative / non-binding (reconstruction)
                                        │
                                        ▼
Outcome Confidence Doctrine Decision    ◀── AUTHORITATIVE MEANING (L0)
                                        │      ▲ nothing below may override
                                        ▼
Interpretation Doctrine                 ── meaning of each state (L1, derives from L0)
                                        │
                                        ▼
Leadership Doctrine                     ── meaning to a leader (L2, derives from L1)
                                        │
                                        ▼
Calibration Decision                    ── principles + invariants (L3, binds below; may not redefine meaning)
                                        │
                ┌───────────────────────┼───────────────────────┐
                ▼                       ▼                       ▼
        Confidence Model V2     CAF Scoring V2          Reliability Model V2     ── realization (L4)
                └───────────────────────┼───────────────────────┘
                                        ▼
                              Determinism Calibration Note
                                        │
                                        ▼
                              Implementation (Engine · Testing · UI)              ── (L5)

   Authority boundary: ───── above this line = MEANING (must not be changed by anything below)
   Calibration boundary: ─── L3 may constrain L4/L5 but may not alter L0–L2
   Probability boundary: ─── any future Outcome Probability is a SEPARATE branch, never inserted into this stack
```

---

## 10. Canonical Rules

1. Discovery cannot create doctrine (it reconstructs only).
2. Discovery is superseded by Decision 001 wherever they differ.
3. Interpretation cannot redefine doctrine.
4. Leadership cannot redefine interpretation or doctrine.
5. Calibration cannot redefine meaning.
6. Implementation cannot redefine calibration.
7. Models realize calibration; models cannot redefine doctrine or calibration principles.
8. The Calibration Invariants (Confidence Stability, Explainability/Attribution, Reliability Non-Collapse) must be preserved by every layer below L3.
9. Outcome Confidence is never a probability; any Outcome Probability is a separate signal that must not modify this stack.
10. Higher-authority documents win in any conflict; the lower document is the one corrected.
11. No layer self-ratifies; changes to meaning or calibration require an owner governance decision.
12. Every Outcome Confidence artifact must declare its layer, its dependencies, and what it must never do.

---

*This index describes the existing Outcome Confidence stack and the rules for maintaining it. It creates no doctrine, calibration, or implementation guidance and modifies no document. It is the first artifact to read before changing anything in the stack.*

**Outcome Confidence Stack Index complete.**
