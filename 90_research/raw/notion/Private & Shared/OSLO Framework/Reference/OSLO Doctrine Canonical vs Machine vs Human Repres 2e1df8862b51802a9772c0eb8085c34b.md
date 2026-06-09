# OSLO Doctrine: Canonical vs Machine vs Human Representations

---

**System:** OSLO

**Scope:** All project data (intake, reasoning, judgment, communication)

**Status:** Canonical

**Audience:** Product, Engineering, AI/ML, Governance

---

## **1. Purpose**

This doctrine defines the **three distinct representations** of project data used by OSLO and the **non-negotiable boundaries** between them.

Its purpose is to:

- Prevent epistemic drift (fact vs inference confusion)
- Preserve auditability and trust
- Enable deterministic reasoning and governed inference
- Ensure human-usable artifacts without corrupting system truth

---

## **2. The Three Representations (Authoritative Definitions)**

### **2.1 Canonical Representation (Logical Truth Model)**

**Definition**

The **canonical representation** is OSLO’s **authoritative logical model** of a project.

It is the **only representation OSLO reasons over**.

**Characteristics**

- Normalized and structured
- Deterministic and versioned
- Stable across storage implementations
- Epistemically explicit

**Canonical data MAY include**

- User-asserted facts
- Extracted facts from uploaded artifacts
- System-inferred propositions
- Explicit assumptions
- Known gaps / unknowns

**Canonical data MUST**

- Declare epistemic status per element
- Preserve provenance (source, derivation)
- Remain independent of storage format
- Never contain presentation or narrative concerns

**Canonical data MUST NOT**

- Implicitly infer missing information (unless permitted by posture/mode)
- Contain prose, persuasion, or UI-driven formatting
- Be altered directly by UI rendering logic

---

### **2.2 Machine-Readable Representation (Physical Persistence)**

**Definition**

The **machine-readable representation** is the **physical storage encoding** of the canonical model.

It exists to persist, query, and scale the canonical model — not to define it.

**Characteristics**

- Database, graph, JSON, or hybrid
- Optimized for performance and access
- Replaceable without semantic impact

**Machine-readable data MUST**

- Be a faithful serialization of canonical data
- Preserve all epistemic metadata
- Support versioning and diffing

**Machine-readable data MUST NOT**

- Introduce new semantics
- Perform inference
- Act as a source of truth independent of canonical logic

**Key invariant**

> Changing the storage technology MUST NOT change OSLO’s reasoning behavior.
> 

---

### **2.3 Human-Readable Representation (Rendered Artifacts)**

**Definition**

Human-readable representations are **rendered views** of canonical data intended for human consumption.

Examples:

- Project Charter
- Scope Definition
- Requirements
- WBS
- Resource Plan
- Schedule Narrative

**Characteristics**

- Narrative-friendly
- Contextual
- Executable by humans
- Multi-audience (PM, exec, team)

**Human-readable artifacts MAY include**

- Canonical facts
- Inferred recommendations
- Narrative explanation and rationale
- Confidence indicators and caveats

**Human-readable artifacts MUST**

- Be derived from canonical data
- Preserve epistemic boundaries (fact vs inference vs assumption)
- Never overwrite or redefine canonical truth

**Human-readable artifacts MUST NOT**

- Serve as an authoritative data source
- Introduce silent inference
- Mask uncertainty or gaps

**Key invariant**

> Artifacts express truth; they do not define it.
> 

---

## **3. Epistemic Status (Orthogonal to Representation)**

Epistemic status is a **required attribute of canonical elements**, not a data tier.

Minimal required statuses:

- **Asserted** – explicitly provided by user
- **Extracted** – parsed from source artifact
- **Inferred** – system-generated
- **Assumed** – explicit hypothesis
- **Unknown** – identified gap

**Rule**

> Any canonical element without an epistemic status is invalid.
> 

---

## **4. Transformation Rules (Non-Negotiable)**

1. **Intake → Canonical**
    - Extract, structure, label epistemic status
    - No silent inference in restricted modes
2. **Canonical → Machine**
    - Serialize only
    - No semantic transformation
3. **Canonical → Human**
    - Render with epistemic transparency
    - Narrative allowed; distortion forbidden
4. **Reverse flows**
    - Human → Canonical requires explicit re-intake and re-validation
    - Machine → Canonical is prohibited

---

## **5. Enforcement Invariants**

- Canonical is the **single source of truth**
- Inference is **tagged, governed, and reversible**
- Storage is **replaceable**
- Artifacts are **views, not facts**
- Epistemic clarity is **non-optional**

---

## **6. Failure Modes This Doctrine Prevents**

- Hallucinated plans
- Fact/inference conflation
- Trust erosion
- Audit failure
- Governance breakdown
- “Looks fine” project blindness

---

## **7. Doctrine Statement (Final)**

> OSLO does not reason over prose, databases, or UI artifacts.
> 

> OSLO reasons over a canonical model that is epistemically explicit, physically independent, and human-expressible without corruption.
> 

---

If you want, next steps I’d recommend:

- Turning this into **engineering guardrails + validators**
- Mapping it to **Pass 1 / Pass 2 intake rules**
- Writing the **Artifact Rendering Contract v1.0**

Just tell me which one to do next.