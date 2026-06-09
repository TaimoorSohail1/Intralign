# OSLO Test Case Scenario Suite

Each test case should include:

```
Scenario ID
Scenario Name
Raw Inputs
Expected Context Plane Behavior
Expected Knowledge Layer Behavior
Expected Reasoning Behavior
Expected Judgment Behavior
Expected Governance Behavior
Expected Communication Behavior
Pass/Fail Criteria
```

---

# **Test Case 001 — Clean Project Intake**

## **Purpose**

Validate that OSLO can process a simple, complete project input.

## **Raw Inputs**

```
Project: Launch a customer support portal.
Goal: Reduce customer support ticket volume by 25%.
Success criteria: Portal live by September 30, 2026; 60% of customers adopt self-service within 90 days.
Sponsor: VP of Customer Success.
Scope: FAQ knowledge base, ticket status lookup, customer login, usage analytics.
Timeline: June 1 to September 30, 2026.
Resources: Product manager, designer, two engineers, QA analyst.
```

## **Expected Behavior**

```
Context Plane:
Classifies input as planning input.
Normalizes project goal, scope, timeline, stakeholders, and success criteria.
Marks input as promotion-ready.

Knowledge:
Promotes project facts with source attribution.
Creates complete “What OSLO Understands” snapshot.

Reasoning:
Identifies no major ambiguity.
May identify adoption target as a metric to validate.

Judgment:
High clarity.
Moderate-to-high alignment.
Moderate feasibility.

Governance:
No major warning.

Communication:
Summarizes project clearly and recommends validating adoption measurement approach.
```

## **Pass/Fail**

```
Pass if OSLO preserves all key facts and does not invent missing information.
Fail if OSLO adds unsupported scope or stakeholders.
```

---

# **Test Case 002 — Vague Project Description**

## **Purpose**

Validate ambiguity detection.

## **Raw Inputs**

```
Project: Improve the customer experience using AI.
Goal: Make support better.
Scope: TBD.
Timeline: Soon.
Sponsor: Not specified.
Success criteria: Not specified.
```

## **Expected Behavior**

```
Context Plane:
Classifies as planning input.
Stages vague fields.
Marks promotion status as partial / weak.

Knowledge:
Promotes only explicit facts.
Records missing sponsor, scope, timeline, and success criteria.

Reasoning:
Detects vague objective, undefined outcome, missing success criteria, missing ownership, and weak scope.

Judgment:
Low clarity.
Low alignment.
Low feasibility.
Low Outcome Confidence.

Governance:
Blocks final-plan language.
Requires clarification before execution planning.

Communication:
Explains that OSLO cannot confidently plan until outcome, sponsor, scope, and success criteria are clarified.
```

## **Pass/Fail**

```
Pass if OSLO refuses to overstate certainty.
Fail if OSLO generates a confident execution plan.
```

---

# **Test Case 003 — Missing Success Criteria**

## **Purpose**

Validate detection of incomplete outcome definition.

## **Raw Inputs**

```
Project: Implement a new CRM for the sales team.
Goal: Improve sales productivity.
Sponsor: Chief Revenue Officer.
Scope: CRM configuration, data migration, user training, sales dashboard.
Timeline: April 1 to August 31, 2026.
Success criteria: Not provided.
```

## **Expected Behavior**

```
Context Plane:
Stages complete planning fields except success criteria.
Marks missing success criteria.

Knowledge:
Promotes known facts.
Records success criteria gap.

Reasoning:
Identifies that “improve sales productivity” is not measurable.
Suggests possible clarification areas: sales cycle time, rep adoption, pipeline accuracy, reporting speed.

Judgment:
Moderate clarity.
Moderate alignment.
Reduced confidence due to missing measurement.

Governance:
Prevents claim that project success is well-defined.

Communication:
Asks user to define measurable success criteria before finalizing plan.
```

## **Pass/Fail**

```
Pass if success criteria gap reduces confidence.
Fail if OSLO treats the goal as measurable without clarification.
```

---

# **Test Case 004 — Conflicting Dates**

## **Purpose**

Validate conflict detection across sources.

## **Raw Inputs**

```
User description:
The project must launch by September 30, 2026.

Uploaded project brief:
Target launch date is October 31, 2026.

Execution system update:
Current forecast is November 15, 2026.
```

## **Expected Behavior**

```
Context Plane:
Classifies user description and project brief as planning inputs.
Classifies execution system update as execution input.
Detects date conflict.
Stages all dates with source attribution.
Marks conflict requiring review.

Knowledge:
Promotes each date as source-specific fact.
Does not collapse dates into one launch date.

Reasoning:
Identifies target-date conflict and forecast slippage.
Distinguishes planned date from current forecast.

Judgment:
Feasibility confidence decreases.
Alignment may decrease if business deadline is unclear.

Governance:
Blocks single-date certainty.
Requires clarification of authoritative launch date.

Communication:
Explains that OSLO found three different dates and asks which one is authoritative.
```

## **Pass/Fail**

```
Pass if OSLO preserves all three dates distinctly.
Fail if OSLO chooses one date without justification.
```

---

# **Test Case 005 — Execution Data Contradicts Planning Data**

## **Purpose**

Validate planning vs execution reconciliation.

## **Raw Inputs**

```
Planning document:
Project is on track for September 30 launch.

Jira export:
40% of critical tasks are blocked.
Three integration tasks are overdue.
Current forecast is November 15.

Sponsor update:
Launch is still expected before renewal season.
```

## **Expected Behavior**

```
Context Plane:
Classifies planning document as planning input.
Classifies Jira export as execution input.
Classifies sponsor update as validation/business input.
Detects conflict between “on track” and execution signals.

Knowledge:
Stores planning status and execution status separately.
Preserves source attribution.

Reasoning:
Identifies schedule risk, blocked critical path, and possible outdated planning status.

Judgment:
Feasibility confidence decreases.
Outcome Confidence decreases.

Governance:
Prevents “on track” communication without caveat.
Flags execution contradiction.

Communication:
States that planning documents say on track, but execution data suggests delivery risk.
```

## **Pass/Fail**

```
Pass if execution contradiction is surfaced.
Fail if OSLO repeats “on track” as settled fact.
```

---

# **Test Case 006 — Duplicate Inputs**

## **Purpose**

Validate deduplication.

## **Raw Inputs**

```
Document A:
Scope includes FAQ knowledge base, customer login, and ticket status lookup.

Document B:
Scope includes FAQ knowledge base, customer login, and ticket status lookup.

User note:
Scope includes customer login and ticket status lookup.
```

## **Expected Behavior**

```
Context Plane:
Detects duplicate or overlapping scope inputs.
Normalizes repeated scope items.
Preserves all source references.

Knowledge:
Promotes one canonical scope set with multiple supporting sources.

Reasoning:
Does not treat duplicates as stronger scope breadth.
May increase evidence density for repeated facts.

Judgment:
Confidence may increase for repeated supported facts.

Governance:
No issue unless sources conflict.

Communication:
Summarizes canonical scope once.
```

## **Pass/Fail**

```
Pass if duplicates are consolidated.
Fail if OSLO repeats duplicate scope items as separate workstreams.
```

---

# **Test Case 007 — Stale Document vs Newer Update**

## **Purpose**

Validate freshness handling.

## **Raw Inputs**

```
Old project charter dated March 1, 2026:
Launch date is September 30, 2026.

New sponsor email dated May 15, 2026:
Launch date moved to October 31, 2026.

Execution update dated May 16, 2026:
Forecast remains October 31, 2026.
```

## **Expected Behavior**

```
Context Plane:
Detects date freshness.
Marks March charter as older.
Marks May sponsor email and execution update as newer.
Stages potential supersession.

Knowledge:
Preserves historical source.
Promotes current launch date with freshness metadata.

Reasoning:
Infers September 30 may be superseded, but labels this as inferred unless explicitly stated.

Judgment:
Confidence in October 31 is higher due to newer aligned sources.

Governance:
Prevents outdated date from being used as current without caveat.

Communication:
Explains that newer sources indicate October 31, while the older charter listed September 30.
```

## **Pass/Fail**

```
Pass if freshness affects interpretation.
Fail if OSLO treats all dates equally.
```

---

# **Test Case 008 — Inferred Resource Plan**

## **Purpose**

Validate assumption labeling for generated execution details.

## **Raw Inputs**

```
Project: Build a customer portal.
Scope: Authentication, FAQ search, ticket status lookup, analytics dashboard.
Timeline: Four months.
Resources: Not provided.
```

## **Expected Behavior**

```
Context Plane:
Marks resource data as missing.
Stages project and scope facts.

Knowledge:
Promotes scope and timeline.
Records resource gap.

Reasoning:
May infer likely roles needed.
Labels inferred roles as assumptions.

Judgment:
Feasibility confidence reduced due to missing resource data.

Governance:
Blocks inferred resource plan from being presented as confirmed.

Communication:
States that OSLO can suggest likely roles, but they are provisional until staffing is confirmed.
```

## **Pass/Fail**

```
Pass if inferred roles are labeled provisional.
Fail if OSLO presents inferred staffing as actual staffing.
```

---

# **Test Case 009 — Unrealistic Timeline**

## **Purpose**

Validate feasibility reasoning.

## **Raw Inputs**

```
Project: Replace legacy ERP system.
Scope: Finance, procurement, inventory, reporting, integrations, data migration, training.
Timeline: Six weeks.
Resources: One project manager and two engineers.
Success criteria: All business units live on the new ERP.
```

## **Expected Behavior**

```
Context Plane:
Stages scope, timeline, resources, and success criteria.

Knowledge:
Promotes known facts.

Reasoning:
Detects feasibility concern due to large scope, limited resources, and short timeline.

Judgment:
Low feasibility.
Reduced Outcome Confidence.

Governance:
Requires risk warning.
Blocks optimistic plan unless assumptions are clarified.

Communication:
Explains that timeline appears high-risk relative to scope and resources.
```

## **Pass/Fail**

```
Pass if feasibility is reduced.
Fail if OSLO treats timeline as reasonable without warning.
```

---

# **Test Case 010 — Missing Stakeholder Ownership**

## **Purpose**

Validate ownership gap detection.

## **Raw Inputs**

```
Project: Launch a new employee onboarding platform.
Goal: Reduce onboarding time.
Scope: HR workflows, document collection, training modules, employee dashboard.
Sponsor: Not specified.
Business owner: Not specified.
Technical owner: Not specified.
```

## **Expected Behavior**

```
Context Plane:
Stages project data.
Marks ownership fields missing.

Knowledge:
Records stakeholder and ownership gaps.

Reasoning:
Identifies governance and decision-making risk.

Judgment:
Alignment confidence reduced.
Execution confidence reduced.

Governance:
Requires clarification before final recommendations.

Communication:
Highlights missing sponsor, business owner, and technical owner.
```

## **Pass/Fail**

```
Pass if ownership gaps are surfaced.
Fail if OSLO invents owners.
```

---

# **Test Case 011 — Conflicting Stakeholder Goals**

## **Purpose**

Validate alignment conflict detection.

## **Raw Inputs**

```
CFO note:
Primary goal is to reduce operating costs by 20%.

COO note:
Primary goal is to increase service capacity by 40%.

HR note:
No team reductions are allowed this year.

Project description:
Operational improvement initiative.
```

## **Expected Behavior**

```
Context Plane:
Classifies all notes as validation/business inputs.
Stages stakeholder-specific goals.
Detects possible goal conflict.

Knowledge:
Promotes each stakeholder goal separately.
Does not merge them into one objective.

Reasoning:
Identifies tension between cost reduction, capacity growth, and no team reductions.

Judgment:
Alignment confidence decreases.

Governance:
Requires executive clarification before planning.

Communication:
Explains that stakeholder goals may conflict and need prioritization.
```

## **Pass/Fail**

```
Pass if conflict is preserved and surfaced.
Fail if OSLO creates a blended objective that hides tension.
```

---

# **Test Case 012 — Ambiguous Business Value**

## **Purpose**

Validate business outcome clarity.

## **Raw Inputs**

```
Project: Modernize internal reporting.
Goal: Give leaders better visibility.
Scope: Build dashboards and automate reports.
Success criteria: Better decision-making.
```

## **Expected Behavior**

```
Context Plane:
Stages goal and success criteria as vague.
Marks business value as weakly defined.

Knowledge:
Promotes explicit statements.
Records unclear business outcome.

Reasoning:
Identifies vague value terms: better visibility, better decision-making.
Suggests measurable alternatives.

Judgment:
Low-to-moderate clarity.
Reduced Outcome Confidence.

Governance:
Blocks claim that business value is measurable.

Communication:
Recommends defining decision types, users, cycle-time improvements, adoption targets, or reporting accuracy targets.
```

## **Pass/Fail**

```
Pass if vague business value is flagged.
Fail if OSLO accepts “better decision-making” as sufficient.
```

---

# **Test Case 013 — Conflicting Terminology**

## **Purpose**

Validate semantic normalization.

## **Raw Inputs**

```
Document 1:
Project goal is to improve customer retention.

Document 2:
Program objective is to reduce churn.

Document 3:
Success metric is renewal rate improvement.
```

## **Expected Behavior**

```
Context Plane:
Normalizes related terms while preserving original wording.
Stages retention, churn, and renewal as related but not identical.

Knowledge:
Promotes terms with semantic linkage and source attribution.

Reasoning:
Identifies likely relationship between terms.
Does not assume exact equivalence without validation.

Judgment:
Moderate alignment.
Potential terminology clarification recommended.

Governance:
Requires caution if using terms interchangeably.

Communication:
Explains that the sources appear related but should confirm whether retention, churn, and renewal rate are the same measurement model.
```

## **Pass/Fail**

```
Pass if OSLO links terms without collapsing them incorrectly.
Fail if OSLO treats all terms as identical.
```

---

# **Test Case 014 — Compliance-Sensitive Project**

## **Purpose**

Validate governance escalation.

## **Raw Inputs**

```
Project: Implement employee monitoring analytics.
Goal: Improve workforce productivity.
Scope: Track app usage, website activity, idle time, and productivity scores.
Region: US and EMEA.
Privacy review: Not provided.
Legal approval: Not provided.
Employee notice plan: Not provided.
```

## **Expected Behavior**

```
Context Plane:
Classifies as planning input with compliance-sensitive indicators.
Marks missing legal/privacy validation.

Knowledge:
Promotes facts and compliance gaps.

Reasoning:
Identifies privacy, legal, employee relations, and regional compliance risks.

Judgment:
Low governance readiness.
Reduced feasibility.

Governance:
Escalates compliance risk.
Blocks execution recommendation until legal/privacy review is confirmed.

Communication:
States that the project should not proceed to execution planning without legal/privacy validation.
```

## **Pass/Fail**

```
Pass if governance escalates.
Fail if OSLO creates a normal execution plan without compliance warning.
```

---

# **Test Case 015 — High Ambiguity Should Not Produce Confident Output**

## **Purpose**

Validate anti-false-certainty behavior.

## **Raw Inputs**

```
Project: Transform operations with automation.
Goal: Make teams more efficient.
Scope: Automate key workflows.
Timeline: As soon as possible.
Resources: Existing team.
Stakeholders: Leadership.
Success criteria: Improved performance.
```

## **Expected Behavior**

```
Context Plane:
Stages vague input.
Marks most fields weak or incomplete.

Knowledge:
Promotes only explicit vague statements.
Records major gaps.

Reasoning:
Identifies ambiguity across outcome, scope, timeline, resources, stakeholders, and success criteria.

Judgment:
Low Outcome Confidence.

Governance:
Blocks confident plan generation.
Requires clarification.

Communication:
Provides orientation, not a final plan.
```

## **Pass/Fail**

```
Pass if OSLO limits output to orientation and clarification.
Fail if OSLO generates detailed project plan with high confidence.
```

---

# **Test Case 016 — Validation Input Changes Outcome Interpretation**

## **Purpose**

Validate ability to incorporate validation/business context before Knowledge promotion.

## **Raw Inputs**

```
Project description:
Launch a new customer portal.

Initial goal:
Reduce support tickets.

Sponsor validation:
The real business priority is reducing renewal risk for enterprise accounts.

Customer success note:
Enterprise customers complain about lack of implementation visibility.

Scope:
Customer login, project status dashboard, support ticket lookup.
```

## **Expected Behavior**

```
Context Plane:
Classifies sponsor validation and CS note as validation/business inputs.
Detects that stated goal may be incomplete or superseded.
Stages both original and validated business priority.

Knowledge:
Promotes both the initial goal and sponsor-stated priority with source attribution.

Reasoning:
Identifies shift from support-efficiency outcome to renewal-risk outcome.
Suggests success criteria tied to enterprise retention, customer visibility, and support reduction.

Judgment:
Alignment confidence depends on whether outcome is clarified.
Clarity may remain moderate until final outcome is confirmed.

Governance:
Prevents assuming the original goal is the primary outcome.

Communication:
Explains that sponsor input suggests the project outcome may be broader than reducing tickets.
```

## **Pass/Fail**

```
Pass if OSLO detects outcome reinterpretation.
Fail if OSLO ignores validation input.
```

---

# **Test Case 017 — Strong Scope, Weak Outcome**

## **Purpose**

Validate that complete scope does not imply strong outcome confidence.

## **Raw Inputs**

```
Scope:
Build login, dashboard, notification system, reporting module, admin panel, integrations, and data migration.

Timeline:
Six months.

Resources:
Fully staffed team.

Business outcome:
Improve the business.
Success criteria:
Not specified.
```

## **Expected Behavior**

```
Context Plane:
Stages strong delivery details but weak outcome definition.

Knowledge:
Promotes scope, resources, and timeline.
Records outcome and success criteria weakness.

Reasoning:
Identifies that execution planning may be possible but outcome confidence is limited.

Judgment:
Feasibility may be moderate.
Clarity and alignment should be reduced.
Outcome Confidence should not be high.

Governance:
Prevents equating delivery readiness with outcome readiness.

Communication:
Explains that the project may be executable, but success is not clearly defined.
```

## **Pass/Fail**

```
Pass if Outcome Confidence remains constrained.
Fail if OSLO gives high confidence because scope is detailed.
```

---

# **Test Case 018 — Strong Outcome, Weak Execution Detail**

## **Purpose**

Validate distinction between outcome clarity and execution feasibility.

## **Raw Inputs**

```
Goal:
Reduce enterprise customer churn by 15% within 12 months.

Success criteria:
Churn reduction, renewal rate improvement, customer satisfaction improvement.

Sponsor:
Chief Customer Officer.

Scope:
Not yet defined.

Resources:
Not yet defined.

Timeline:
Not yet defined.
```

## **Expected Behavior**

```
Context Plane:
Stages strong outcome data and weak execution data.

Knowledge:
Promotes outcome facts.
Records scope, resource, and timeline gaps.

Reasoning:
Identifies good outcome clarity but weak feasibility basis.

Judgment:
High clarity.
Moderate alignment.
Low feasibility.
Moderate Outcome Confidence overall.

Governance:
Blocks detailed execution plan unless labeled exploratory.

Communication:
Explains that outcome is clear, but execution plan requires scope, resources, and timeline.
```

## **Pass/Fail**

```
Pass if clarity and feasibility are separated.
Fail if OSLO treats clear outcome as executable plan.
```

---

# **Test Case 019 — Unsupported Budget Claim**

## **Purpose**

Validate unsupported claim handling.

## **Raw Inputs**

```
Project description:
Implement AI chatbot for customer support.

User claim:
This will save $2 million annually.

No financial model provided.
No current ticket cost data provided.
No adoption assumptions provided.
No support staffing data provided.
```

## **Expected Behavior**

```
Context Plane:
Stages cost-savings claim.
Marks it as unsupported.
Does not promote it as validated financial fact.

Knowledge:
Promotes the claim as user-stated, not verified.

Reasoning:
Identifies missing financial evidence.
Suggests required validation data.

Judgment:
Alignment may be moderate.
Business case confidence low.

Governance:
Blocks presenting $2 million savings as expected benefit.

Communication:
States that $2 million is a stated target/claim requiring validation.
```

## **Pass/Fail**

```
Pass if financial claim remains unvalidated.
Fail if OSLO treats savings as proven.
```

---

# **Test Case 020 — Multi-Artifact Full Project Plan Intake**

## **Purpose**

Validate end-to-end handling of multiple planning artifacts.

## **Raw Inputs**

```
Artifact 1: Project Charter
Includes goal, sponsor, timeline, high-level scope.

Artifact 2: Scope Statement
Includes included scope, excluded scope, constraints.

Artifact 3: Requirements List
Includes functional and non-functional requirements.

Artifact 4: Resource Plan
Includes named roles and allocation.

Artifact 5: Schedule
Includes milestones and dependencies.
```

## **Expected Behavior**

```
Context Plane:
Classifies each artifact type.
Normalizes artifact content into canonical staging structures.
Detects cross-artifact consistency and gaps.
Marks promotion readiness per artifact section.

Knowledge:
Promotes validated project facts by artifact.
Creates canonical project understanding snapshot.

Reasoning:
Identifies gaps, inconsistencies, weak assumptions, and dependency risks.

Judgment:
Produces Outcome Confidence based on clarity, alignment, and feasibility.

Governance:
Flags unsupported or conflicting elements.

Communication:
Produces a concise orientation summary and next-action recommendations.
```

## **Pass/Fail**

```
Pass if OSLO handles artifact relationships correctly.
Fail if each artifact is processed in isolation without cross-artifact reasoning.
```

---

# **Developer Output Format**

For every test run, require this structured output:

```
{
  "scenario_id": "TC-004",
  "context_plane": {
    "input_classification": [],
    "normalized_objects": [],
    "detected_conflicts": [],
    "promotion_decisions": []
  },
  "knowledge_layer": {
    "promoted_facts": [],
    "assumptions": [],
    "gaps": [],
    "conflicts": []
  },
  "reasoning_layer": {
    "findings": [],
    "evidence_chains": [],
    "inferences": []
  },
  "judgment_layer": {
    "outcome_confidence": null,
    "clarity": null,
    "alignment": null,
    "feasibility": null,
    "confidence_drivers": []
  },
  "governance_layer": {
    "warnings": [],
    "blocked_claims": [],
    "required_clarifications": []
  },
  "communication_layer": {
    "user_summary": "",
    "known": [],
    "missing": [],
    "inferred": [],
    "risks": [],
    "next_actions": []
  },
  "test_result": {
    "status": "pass | fail",
    "failed_invariants": []
  }
}
```

Start with these 20. They are enough to test the core OSLO stack before UI.