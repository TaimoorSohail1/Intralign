# OSLO Pre-UI Testing Approach

## **Core testing principle**

Do **not** test OSLO through UI first.

Test OSLO as a **headless intelligence pipeline**:

```
External Inputs
↓
Context Plane
↓
Knowledge Layer
↓
Reasoning Layer
↓
Judgment Layer
↓
Governance Layer
↓
Communication Layer
↓
Structured OSLO Output Package
```

The UI should only consume outputs after this pipeline is proven.

---

# **1. Build an OSLO Test Harness**

Create a CLI or simple internal developer console:

```
oslo test run test_001
oslo test run-all
oslo inspect context test_001
oslo inspect knowledge test_001
oslo inspect reasoning test_001
oslo inspect judgment test_001
oslo inspect governance test_001
oslo inspect communication test_001
```

The harness should output:

```
Context staging package
Knowledge snapshot
Reasoning findings
Judgment scores
Governance decisions
Communication response
Evidence chains
Assumption register
Promotion/rejection log
```

---

# **2. Create canonical test scenarios**

Start with 15–25 test projects.

Each scenario should include raw input, expected staging behavior, expected knowledge promotion, and expected OSLO output.

Recommended scenarios:

```
1. Clean simple project
2. Vague project description
3. Missing outcome definition
4. Missing success criteria
5. Conflicting stakeholder goals
6. Conflicting dates
7. Uploaded plan with weak scope
8. Execution data contradicts planning data
9. Validation input changes expected outcome
10. Duplicate documents
11. Stale document vs newer update
12. Inferred resource plan
13. Unrealistic timeline
14. Missing stakeholder ownership
15. Compliance-sensitive project
16. Ambiguous business value
17. Multiple source inputs with inconsistent terminology
18. Strong planning data but weak execution data
19. Strong execution data but weak outcome data
20. High ambiguity project that should not produce confident output
```

---

# **3. Test the Context Plane first**

This is now the front door to OSLO.

The Context Plane must prove it can ingest, normalize, classify, stage, and control promotion before anything reaches Knowledge.

## **Context Plane test areas**

```
Input ingestion
Input type classification
Input normalization
Source attribution
Freshness detection
Duplicate detection
Conflict detection
Validation status
Promotion readiness
Quarantine/rejection
```

## **Required pass conditions**

The Context Plane should pass only if it can answer:

```
What came in?
Where did it come from?
What type of input is it?
Is it planning, execution, or validation input?
Is it complete enough to stage?
Is it stale, conflicting, duplicate, or unsupported?
Is it ready to promote into Knowledge?
What should remain unpromoted?
```

## **Critical invariant**

```
No external input enters the Knowledge Layer unless the Context Plane has classified, normalized, sourced, staged, and assigned promotion status.
```

---

# **4. Test Knowledge Layer promotion**

The Knowledge Layer should only receive promoted, structured context.

Test whether it can:

```
Store canonical project facts
Preserve source attribution
Preserve timestamps
Separate facts from assumptions
Separate observed data from inferred data
Maintain a “What OSLO Understands” snapshot
Represent gaps explicitly
Represent conflicts explicitly
```

## **Critical invariant**

```
The Knowledge Layer must never silently convert staged, inferred, or weak context into fact.
```

---

# **5. Test Reasoning Layer behavior**

The Reasoning Layer should operate on Knowledge, not raw external input.

Test whether it can:

```
Detect ambiguity
Detect contradictions
Identify missing planning elements
Identify unsupported assumptions
Infer cautiously
Generate evidence chains
Identify downstream planning risks
Distinguish strong evidence from weak evidence
```

## **Critical invariant**

```
Reasoning may infer, but every inference must be labeled, sourced to its basis, and assigned confidence.
```

---

# **6. Test Judgment Layer behavior**

The Judgment Layer should evaluate project confidence, not merely summarize findings.

Test whether it can produce:

```
Outcome Confidence
Clarity score
Alignment score
Feasibility score
Confidence drivers
Confidence reducers
Fragility signals
Severity ranking
Recommended next actions
```

## **Critical invariant**

```
Confidence must not increase unless evidence quality, clarity, alignment, or feasibility improves.
```

---

# **7. Test Governance Layer behavior**

The Governance Layer protects OSLO from false certainty.

Test whether it can:

```
Block unsupported conclusions
Flag overconfident outputs
Prevent final-plan language when context is weak
Require clarification when critical inputs are missing
Escalate high-risk assumptions
Detect when inferred execution details are being treated as validated
Apply different policies based on risk level
```

## **Critical invariant**

```
Governance must stop OSLO from presenting provisional, inferred, or weakly sourced outputs as settled truth.
```

---

# **8. Test Communication Layer behavior**

The Communication Layer should convert OSLO intelligence into useful user-facing guidance.

Test whether it clearly communicates:

```
What OSLO understands
What is missing
What is inferred
What is conflicting
What is risky
What should be clarified next
What can safely proceed
What should remain provisional
```

It should support different views:

```
PM view
Executive view
Developer/debug view
```

## **Critical invariant**

```
Communication must preserve epistemic status: known, inferred, assumed, missing, conflicting, provisional.
```

---

# **9. Run end-to-end scenario tests**

Each canonical project should run through the full pipeline.

For each test, validate:

```
Raw input was staged correctly
Only valid context was promoted
Knowledge snapshot is accurate
Reasoning findings are supported
Judgment scores are explainable
Governance warnings are enforced
Communication output is clear and safe
```

The expected output does not need exact wording. It should test structure and behavior.

Example expected result:

```
Should detect missing success criteria
Should classify delivery date conflict
Should mark resource plan as inferred
Should reduce feasibility confidence
Should recommend sponsor clarification
Should not present execution plan as final
```

---

# **10. Add regression tests**

Every defect should become a permanent test.

Examples:

```
If OSLO once turned an inferred stakeholder into a fact, create a regression test.
If OSLO once ignored stale execution data, create a regression test.
If OSLO once overstated confidence, create a regression test.
If OSLO once promoted conflicting context without warning, create a regression test.
```

---

# **11. Add mutation tests**

Deliberately damage inputs and confirm OSLO responds safely.

Examples:

```
Remove sponsor name
Remove success criteria
Add conflicting deadline
Add duplicate document
Add stale execution report
Add unsupported budget claim
Add vague objective
Add unrealistic timeline
```

Expected behavior:

```
Confidence decreases
Gaps are surfaced
Conflicts are flagged
Clarification is requested
Unsupported claims are blocked
```

---

# **12. Define hard failure conditions**

A test should fail if OSLO:

```
Promotes unclassified input into Knowledge
Loses source attribution
Converts inference into fact
Ignores conflicting context
Inflates confidence without evidence
Generates final-plan language from weak inputs
Skips governance
Hides uncertainty from the user
Cannot explain a judgment score
Cannot show why a recommendation was made
```

---

# **Final recommendation**

Build OSLO testing around one core idea:

```
Raw context in → governed knowledge → explainable reasoning → confidence judgment → safe communication out
```

Before UI, developers should prove the stack can produce a reliable **OSLO Intelligence Package** from messy real-world project inputs.