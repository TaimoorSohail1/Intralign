# Graph DB Schema vs OSLO Design Intent

---

## **1) “Always on update loop” is anchored at the wrong abstraction level**

### **Misalignment**

Your blue box (“always on update loop”) encloses:

- ElementVersion → Findings → Issues → IssueDisposition → RCU
    
    …and also includes Evidence/Execution Signal paths.
    

This implies the loop is a **pipeline that always runs end-to-end**.

In OSLO, recompute is:

- **triggered**
- **scoped**
- **incremental**
- often **partial** (e.g., only re-evaluate a subset of affected elements)

### **Risk**

Engineers will implement:

- full-chain recompute on every change
- unstable oscillation (especially if comm updates trigger canon updates)
- compute blowups and non-determinism

### **Fix**

Replace the blue box meaning with:

- **“Trigger-based recompute scope”**
    
    And add explicit nodes/edges:
    
- RecomputeTrigger (type, scope, cause)
- RecomputeRun (run_id, version, timestamp, status)

Also add:

> “Only affected subgraph is recomputed unless a global trigger class is raised.”
> 

---

## **2) ElementVersion is being treated as the**

## **origin**

## **of Findings (backwards)**

### **Misalignment**

Your chain says:

ElementVersion → Findings → Issues → IssueDisposition → RCU

This implies Findings are “inside” the element version, rather than:

- computed outputs
- that must reference the exact canonical snapshot they were computed from

In OSLO, Findings must be tied to:

- the **exact canon version** used
- the **reasoning policy version** used
- the evidence set used

### **Risk**

You won’t be able to answer:

> “What did the system find, using what snapshot, under what policy?”
> 

This breaks traceability guarantees.

### **Fix**

Introduce explicit compute lineage nodes:

- ReasoningRun
- JudgmentRun
- GovernanceDecision

And connect like:

- ReasoningRun **consumed** ElementVersion (and other relevant nodes)
- ReasoningRun **produced** Finding
- Finding **supportedBy** Evidence
- JudgmentRun **produced** Issue
- GovernanceDecision **produced** IssueDisposition
- CommunicationRender **produced** RCU

This restores OSLO’s “runs produce outputs” structure.

---

## **3) Epistemic state is not first-class across the graph**

### **Misalignment**

You have good epistemic ideas in properties (e.g., “is_canonical”, “derivedFrom”), but epistemic status is not explicitly required on:

- Finding
- Evidence
- Issue
- RCU
- Outcome

OSLO requires epistemic labels everywhere, especially on anything user-visible.

### **Risk**

Epistemic collapse:

- inferred treated as asserted
- output treated as truth
- RCUs become narrative objects not constrained by upstream states

### **Fix**

Add a mandatory property group on **all nodes** that represent claims/interpretations/communications:

**Epistemic Envelope**

- epistemic_status: asserted | inferred | assumed | observed | unknown
- source: user | system | execution | external
- confidence: 0..1
- provenance_ref: pointer(s)

And enforce it via schema validation (even if Neo4j-like, implement at app layer).

---

## **4) “IssueDisposition” is underspecified (Governance is being reduced again)**

### **Misalignment**

IssueDisposition has:

- outcome_type (PERMIT, DENY, REQUIRE_APPROVAL, BLOCK)
- rationale/reason codes

This models governance as a **decision outcome**, but not as a **constraint package**.

OSLO governance must be able to express:

- expose vs suppress
- disclosure requirements
- modality constraints (ask vs warn vs suggest vs execute)
- scope constraints (communication only vs execution allowed)
- tier/posture constraints

### **Risk**

Governance becomes a yes/no gate and loses:

- safe partial disclosure
- posture-aware behaviors
- controlled explanation requirements

### **Fix**

Replace “IssueDisposition” with a richer concept:

**GovernanceDispositionPackage**

- decision_class: suppress | defer | expose | escalate | authorize_action
- scope: communication | execution | both
- required_disclosures: [epistemic_label, uncertainty, limitations]
- allowed_action_classes: [...]
- expires_at
- policy_version
- posture_context

You can keep IssueDisposition as a node, but it must carry a **package**, not a single flag.

---

## **5) RCU is modeled as an endpoint, not a constrained render**

### **Misalignment**

RCU properties include:

- diagnostic
- why_it_matters
- how_we_know

This implies Communication is generating explanation content.

In OSLO, Communication may only render content that is:

- grounded in upstream judgment and evidence
- constrained by governance

### **Risk (high)**

RCUs become:

- free-text narrative
- post-hoc rationalization
- untraceable claims

### **Fix**

Add explicit required relationships for every RCU:

- RCU **rendersFrom** GovernanceDispositionPackage
- RCU **references** Issue
- RCU **referencesEvidence** Evidence (or EvidenceSet)
- RCU **usesTemplate** MessageTemplate (optional but recommended)

And add a hard invariant:

> No RCU can exist without references to upstream Issue + Governance decision.
> 

---

## **6) “Outcome” node is under-modeled and incorrectly treated as a terminal aggregate**

### **Misalignment**

Outcome has:

- title
- priority
- health score aggregate (clarity/alignment/feasibility)

But in OSLO, an outcome is not just a container + score:

- it is tied to intent
- dependencies
- constraints
- validation criteria
- and its health is *derived from* issues across multiple artifacts

### **Risk**

Outcomes become shallow “labels” and scoring becomes arbitrary.

### **Fix**

Add relationships:

- Outcome **hasIntent** (explicit outcome definition node)
- Outcome **validatedBy** (criteria/metrics)
- Outcome **supportedBy** (artifacts/elements)
- Outcome **impactedBy** (issues)

Make aggregate health score a computed projection, not canonical truth (or at least tag it as computed + versioned).

---

## **7) Evidence is too thin; “source reference” alone is not enough**

### **Misalignment**

Evidence node has just:

- ID
- source reference

Evidence in OSLO must support chaining and audit:

- what was observed
- when
- by whom/what system
- how reliable
- what it supports/contradicts

### **Risk**

You won’t be able to explain “how we know” safely.

Evidence becomes a hyperlink, not a structured artifact.

### **Fix**

Expand Evidence into:

- EvidenceItem (atomic)
- EvidenceSet (group used in a run)
    
    Properties:
    
- evidence_type
- captured_at
- captured_by
- reliability
- content_hash (or pointer)
    
    Relationships:
    
- Evidence **supports** Finding / Issue
- Evidence **contradicts** Finding / Issue (important)

---

## **8) “is_canonical” on ElementVersion is an epistemic trap**

### **Misalignment**

ElementVersion contains is_canonical.

This implies canonicality is a boolean property of a version.

In OSLO:

- Canonical means “in the authoritative store”
- A version can be canonical while still being inferred/assumed/unknown
- Canonicality is about *storage authority*, not *truth*

### **Risk**

Engineers will interpret:

- canonical == confirmed
    
    Which collapses epistemic separation.
    

### **Fix**

Remove or de-emphasize is_canonical. Replace with:

- in_canon: true (storage flag)
    
    And separately enforce:
    
- epistemic_status as above

This keeps “canon” orthogonal to truth-source.

---

# **Minimal Fix Set (Highest Leverage)**

If you do only 7 fixes, do these:

1. Add ReasoningRun / JudgmentRun / GovernanceDecision / CommunicationRender lineage nodes
2. Require Epistemic Envelope on all claim-like nodes
3. Replace IssueDisposition with a Disposition Package (scope + disclosures + action classes)
4. Require RCU references to Issue + Governance + Evidence
5. Add EvidenceItem/EvidenceSet with supports/contradicts relations
6. Reframe recompute loop as trigger-based + scoped runs
7. Remove “canonical == true/false” confusion (separate canon membership from epistemic status)

---

## **Bottom line**

This graph is **the right direction**—but right now it still encodes a story like:

> element changed → system produced finding → system produced issue → system decided → system explained
> 

OSLO must encode:

> canon snapshot → run-based reasoning (epistemic proposals) → run-based judgment (normative meaning) → governance disposition package (constraints) → constrained rendering (no new claims) → optional execution (authorized) → observed reality back into canon
> 

If you want, I can rewrite this as a **graph schema spec (node types + required relationships + required properties + invariants)** so your engineers can implement it without interpretation drift.