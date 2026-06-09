# Chain of Custody Diagram vs OSLO Design Intent

## **High-level verdict**

The diagram correctly conveys **linear dependency** (“this comes after that”), but OSLO requires **custodial enforcement**, not just sequencing.

Right now, the diagram still teaches this dangerous idea:

> “Later layers depend on earlier outputs.”
> 

OSLO must enforce:

> Later layers cannot exist without consuming authenticated outputs of earlier layers, produced by a recorded run, under a canonical snapshot.
> 

That distinction is everything.

---

## **1) “Structural Truth” language breaks epistemic custody**

### **Misalignment**

You label the second node:

> Findings (Structural Truth)
> 

This implies:

- closure
- correctness
- authority

In OSLO, Reasoning **never produces truth** — only *epistemic claims*.

### **Risk**

This breaks the first custody boundary:

- Judgment starts from “truth,” not proposals
- Confidence and severity become cosmetic
- Evidence chains become justification, not grounding

### **Fix**

Rename explicitly:

> Findings (Epistemic Claims / Candidate Structures)
> 

And add a custody annotation:

> “Findings are non-normative and non-authoritative.”
> 

This preserves Reasoning → Judgment separation.

---

## **2) Evidence chains are treated as an attachment, not a custody mechanism**

### **Misalignment**

“Evidence Association” flows into “Evidence Chains (Traceability)”.

This suggests evidence is *optional support*.

In OSLO, evidence is **custody enforcement**:

- no evidence → no downstream authority
- incomplete evidence → constrained governance

### **Risk**

Engineers may allow:

- issues without evidence
- judgments with soft links
- RCUs with hand-wavy “why we know”

### **Fix**

Change the semantics:

- Evidence Chains must be **required inputs** to:
    - Issues
    - Health aggregation
    - IssueDisposition
    - RCUs

Add an explicit gate:

> “No Issue may be formed without an Evidence Chain reference.”
> 

This makes evidence a custody lock, not a note.

---

## **3) Issues node collapses Judgment authority into a single object**

### **Misalignment**

“Issues (Severity + Confidence)” bundles:

- interpretation
- scoring
- prioritization

But Judgment in OSLO is:

- run-based
- frame-dependent
- reversible
- versioned

### **Risk**

Issues become:

- mutable facts
- overwritten by “latest”
- detached from the judgment context that created them

This breaks historical custody.

### **Fix**

Split conceptually (even if not visually heavy):

- **JudgmentRun**
    - applies normative frames
    - consumes Findings + Evidence
- **Issue**
    - produced by a JudgmentRun
    - immutable once created
    - superseded only by a later run

Add annotation:

> “Issues are outputs of JudgmentRuns, not editable entities.”
> 

---

## **4) Health score aggregation bypasses custody lineage**

### **Misalignment**

Issues feed directly into:

> Health Scores (Clarity, Alignment, Feasibility)
> 

This implies:

- health is a derived metric
- but not governed

In OSLO, health scores:

- influence governance decisions
- must be traceable
- must be reproducible

### **Risk**

Health scores become:

- cached numbers
- recalculated ad hoc
- impossible to audit

### **Fix**

Add custody requirements:

- Health Scores are produced by a **HealthAggregationRun**
- Inputs:
    - Issue IDs
    - JudgmentRun IDs
- Outputs:
    - versioned score
    - aggregation policy version

Even a small note preserves custody integrity.

---

## **5) Governance is depicted as downstream logic, not a custody authority**

### **Misalignment**

“IssueDispositions (Expose, Suppress, Defer)” sits *after* Issues as if it’s just another transformation.

In OSLO, Governance is:

- an **authority boundary**
- the point where **permission enters the system**

### **Risk**

Engineers treat governance as:

- a filter
- a routing step
- a UI decision

Which allows bypass via “internal consumers.”

### **Fix**

Visually and semantically elevate Governance:

- Rename to:
    
    > Governance Disposition Package
    > 
- Annotate:
    
    > “No downstream artifact may exist without a Governance Disposition reference.”
    > 

This enforces custody at the policy boundary.

---

## **6) ActionAuthorization is shown as a branch, not a gate**

### **Misalignment**

ActionAuthorization appears as a sibling outcome of policy evaluation.

This suggests:

- authorization is optional
- execution might happen elsewhere

### **Risk (high)**

Execution paths get wired directly from Issues or RCUs.

### **Fix**

Make this explicit:

> Execution cannot occur without an ActionAuthorization artifact produced by Governance.
> 

Visually:

- Draw ActionAuthorization as a **required gate**, not a side output.
- Annotate:
    
    > “Execution layers must validate authorization reference.”
    > 

---

## **7) “Faithful Translation” is not enforceable as drawn**

### **Misalignment**

IssueDisposition → RCUs labeled “Faithful Translation”.

This is aspirational, not enforceable.

### **Risk**

Communication becomes:

- interpretive
- narrative-driven
- subtly authoritative

### **Fix**

Replace the phrase with a constraint:

> “RCUs must reference:
> 
- Issue ID
- Evidence Chain IDs
- Governance Disposition ID
- Required disclosures”

This turns “faithful” into **verifiable custody**.

---

## **8) Missing explicit “no bypass” enforcement markers**

### **Misalignment**

The purpose says:

> “how one layer cannot bypass another layer”
> 

But the diagram does not *enforce* that — it only implies order.

### **Risk**

Engineers can still:

- query Findings directly
- build UI from Issues
- trigger execution from RCUs

### **Fix (critical)**

Add explicit custody invariants on the diagram:

- ❌ Findings cannot be rendered
- ❌ Issues cannot be executed
- ❌ RCUs cannot exist without GovernanceDisposition
- ❌ Execution cannot occur without ActionAuthorization

These can be small lock icons or footnotes, but they matter.

---

# **Minimal Fix Set (to make this a true chain-of-custody diagram)**

If you only do **seven fixes**, do these:

1. Rename “Structural Truth” → **Epistemic Claims**
2. Make Evidence Chains mandatory inputs, not optional
3. Introduce **JudgmentRun** as the producer of Issues
4. Version Health Score aggregation as a run
5. Elevate Governance to a custody authority (Disposition Package)
6. Make ActionAuthorization a hard execution gate
7. Replace “Faithful Translation” with reference-based enforcement

---

## **Bottom line**

Right now, this diagram explains **logical flow**.

OSLO requires it to explain **custodial authority**.

The difference is this:

> Flow says
> 
> 
> *what happens next*
> 

> Custody says
> 
> 
> *what is allowed to exist at all*
> 

With the fixes above, this becomes one of your **most important diagrams** — the one that prevents silent bypass and preserves trust.

If you want next, I can:

- rewrite this as a **formal custody invariant spec**, or
- convert it into a **developer-facing “bypass prevention checklist”** tied to each artifact type.