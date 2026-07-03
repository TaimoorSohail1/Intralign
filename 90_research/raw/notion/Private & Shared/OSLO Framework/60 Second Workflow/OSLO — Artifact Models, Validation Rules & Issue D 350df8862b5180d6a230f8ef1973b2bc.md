# OSLO — Artifact Models, Validation Rules & Issue Detection Logic

## **1. Implementation Objective**

Translate the artifact requirements into enforceable system structures:

1. **Pydantic-style models**
2. **Validation rules**
3. **Issue generation rules**
4. **Score impact mapping**
5. **Snapshot vs full-mode rendering logic**

Core principle:

> OSLO should not merely generate artifacts. It should evaluate artifact quality, expose uncertainty, and guide users toward improvement.
> 

---

# **2. Shared Enums**

```
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field

class EpistemicStatus(str, Enum):
    EXPLICIT = "explicit"
    INFERRED = "inferred"
    MISSING = "missing"

class ConfidenceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class IssueType(str, Enum):
    GAP = "gap"
    MISALIGNMENT = "misalignment"
    ASSUMPTION = "assumption"
    RISK = "risk"

class ImpactLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ScoreDimension(str, Enum):
    CLARITY = "clarity"
    ALIGNMENT = "alignment"
    FEASIBILITY = "feasibility"

class VisibilityMode(str, Enum):
    SNAPSHOT = "snapshot"
    FULL = "full"
```

---

# **3. Base Artifact Element Model**

Every artifact element should inherit from this.

```
class SourceRef(BaseModel):
    source_id: str
    source_type: str  # user_input, uploaded_doc, generated_inference, connected_system
    excerpt: Optional[str] = None
    timestamp: Optional[str] = None

class BaseArtifactElement(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

    epistemic_status: EpistemicStatus
    confidence_score: int = Field(ge=0, le=100)

    source_refs: List[SourceRef] = []
    linked_intent_ids: List[str] = []

    assumptions: List[str] = []
    risks: List[str] = []

    visible_in_snapshot: bool = False
    snapshot_priority: Optional[int] = None
```

Critical rule:

```
No artifact element may exist without:
- epistemic_status
- confidence_score
- source_refs or explicit missing-state explanation
```

---

# **4. Issue Model**

```
class Issue(BaseModel):
    issue_id: str
    title: str
    issue_type: IssueType
    impact_level: ImpactLevel

    affected_scores: List[ScoreDimension]

    description: str
    recommended_resolution: str

    linked_artifact_type: str
    linked_artifact_element_ids: List[str] = []

    current_score: Optional[int] = None
    projected_score_after_resolution: Optional[int] = None

    fix_now_prompt: Optional[str] = None
    should_surface_in_snapshot: bool = False
```

---

# **5. Scoring Model**

```
class ArtifactScore(BaseModel):
    clarity: int = Field(ge=0, le=100)
    alignment: int = Field(ge=0, le=100)
    feasibility: int = Field(ge=0, le=100)

    explanation: Optional[str] = None
    contributing_issue_ids: List[str] = []
```

Scoring rule:

```
Scores must be explainable by linked issues.
No score should be displayed without at least one supporting explanation.
```

---

# **6. Intent Artifact Model**

```
class BusinessObjective(BaseArtifactElement):
    pass

class DesiredOutcome(BaseArtifactElement):
    success_metrics: List[str] = []

class SuccessMetric(BaseArtifactElement):
    metric_name: str
    target_value: Optional[str] = None
    measurement_method: Optional[str] = None

class Stakeholder(BaseArtifactElement):
    role: Optional[str] = None
    responsibility: Optional[str] = None
    decision_authority: Optional[bool] = None

class Constraint(BaseArtifactElement):
    constraint_type: str  # budget, timeline, resource, compliance, technical, business

class IntentArtifact(BaseModel):
    artifact_id: str
    business_objectives: List[BusinessObjective] = []
    desired_outcomes: List[DesiredOutcome] = []
    success_metrics: List[SuccessMetric] = []
    strategic_alignment_drivers: List[BaseArtifactElement] = []
    stakeholders: List[Stakeholder] = []
    constraints: List[Constraint] = []
    assumptions: List[BaseArtifactElement] = []
    priority_logic: List[BaseArtifactElement] = []
    outcome_risks: List[BaseArtifactElement] = []
    high_level_dependencies: List[BaseArtifactElement] = []

    score: Optional[ArtifactScore] = None
    issues: List[Issue] = []
```

## **Intent Validation Rules**

### **Clarity Issues**

```
IF desired_outcomes is empty
THEN create HIGH gap issue affecting Clarity.

IF desired_outcome has no success_metrics
THEN create HIGH gap issue affecting Clarity and Alignment.

IF business_objective description is vague
THEN create MEDIUM clarity issue.

IF success_metric has no target_value or measurement_method
THEN create HIGH clarity issue.
```

### **Alignment Issues**

```
IF desired_outcome is not linked to a business_objective
THEN create HIGH misalignment issue affecting Alignment.

IF success_metric is not linked to a desired_outcome
THEN create MEDIUM misalignment issue.

IF planning artifacts exist without linked_intent_ids
THEN create HIGH alignment issue.
```

### **Feasibility Issues**

```
IF constraints are missing
THEN create MEDIUM feasibility issue.

IF high-level dependencies are missing
THEN create MEDIUM feasibility issue.

IF assumptions are inferred and high-impact
THEN create HIGH assumption issue affecting Feasibility.
```

---

# **7. Scope Artifact Model**

```
class ScopeItem(BaseArtifactElement):
    deliverable: str
    in_scope: bool = True
    out_of_scope: bool = False
    acceptance_criteria_ids: List[str] = []
    linked_requirement_ids: List[str] = []
    constraints: List[str] = []

class ScopeArtifact(BaseModel):
    artifact_id: str
    scope_items: List[ScopeItem] = []
    exclusions: List[BaseArtifactElement] = []
    boundaries: List[BaseArtifactElement] = []
    constraints: List[Constraint] = []

    score: Optional[ArtifactScore] = None
    issues: List[Issue] = []
```

## **Scope Validation Rules**

```
IF scope_items is empty
THEN create HIGH gap issue affecting Clarity and Feasibility.

IF scope_item has no linked_intent_ids
THEN create HIGH alignment issue.

IF scope_item has no acceptance_criteria_ids
THEN create MEDIUM clarity issue.

IF exclusions are empty
THEN create MEDIUM clarity issue.

IF scope boundaries are missing
THEN create HIGH clarity issue.
```

---

# **8. Requirements Artifact Model**

```
class RequirementType(str, Enum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non-functional"
    CONSTRAINT = "constraint"

class RequirementPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Requirement(BaseArtifactElement):
    requirement_type: RequirementType
    statement: str
    priority: RequirementPriority
    acceptance_criteria_ids: List[str] = []
    linked_scope_item_ids: List[str] = []
    dependencies: List[str] = []

class RequirementsArtifact(BaseModel):
    artifact_id: str
    requirements: List[Requirement] = []

    score: Optional[ArtifactScore] = None
    issues: List[Issue] = []
```

## **Requirements Validation Rules**

```
IF requirements is empty
THEN create HIGH gap issue affecting Clarity and Feasibility.

IF requirement has no linked_scope_item_ids
THEN create HIGH alignment issue.

IF requirement has no linked_intent_ids
THEN create HIGH alignment issue.

IF requirement has no acceptance_criteria_ids
THEN create MEDIUM clarity issue.

IF requirement statement is vague
THEN create MEDIUM clarity issue.

IF high-priority requirement has unresolved dependencies
THEN create HIGH feasibility issue.
```

---

# **9. WBS Artifact Model**

```
class WBSNode(BaseArtifactElement):
    wbs_id: str
    level: int
    parent_id: Optional[str] = None
    child_ids: List[str] = []
    linked_requirement_ids: List[str] = []
    estimated_effort: Optional[float] = None
    dependencies: List[str] = []

class WBSArtifact(BaseModel):
    artifact_id: str
    wbs_nodes: List[WBSNode] = []

    score: Optional[ArtifactScore] = None
    issues: List[Issue] = []
```

## **WBS Validation Rules**

```
IF wbs_nodes is empty
THEN create HIGH gap issue affecting Feasibility.

IF WBS node has no linked_requirement_ids
THEN create HIGH alignment issue.

IF WBS node has no estimated_effort
THEN create MEDIUM feasibility issue.

IF WBS has only one level
THEN create MEDIUM clarity issue.

IF parent-child hierarchy is invalid
THEN create HIGH feasibility issue.
```

---

# **10. Resource Plan Model**

```
class ResourceType(str, Enum):
    HUMAN = "human"
    SYSTEM = "system"
    EXTERNAL = "external"

class Resource(BaseArtifactElement):
    resource_id: str
    role: str
    resource_type: ResourceType
    capacity: Optional[float] = None
    availability: Optional[str] = None
    assigned_wbs_ids: List[str] = []
    constraints: List[str] = []

class ResourcePlanArtifact(BaseModel):
    artifact_id: str
    resources: List[Resource] = []

    score: Optional[ArtifactScore] = None
    issues: List[Issue] = []
```

## **Resource Validation Rules**

```
IF resources is empty
THEN create HIGH feasibility issue.

IF resource has no capacity
THEN create HIGH feasibility issue.

IF resource has no availability
THEN create MEDIUM feasibility issue.

IF WBS nodes exist without assigned resources
THEN create HIGH feasibility issue.

IF resource assignment is inferred
THEN create assumption issue affecting Feasibility.
```

---

# **11. Dependency Map Model**

```
class DependencyType(str, Enum):
    FS = "FS"
    SS = "SS"
    FF = "FF"
    SF = "SF"

class Dependency(BaseArtifactElement):
    dependency_id: str
    dependency_type: DependencyType
    predecessor_id: str
    successor_id: str
    lag: Optional[float] = 0

class DependencyMapArtifact(BaseModel):
    artifact_id: str
    dependencies: List[Dependency] = []

    score: Optional[ArtifactScore] = None
    issues: List[Issue] = []
```

## **Dependency Validation Rules**

```
IF WBS exists but dependencies are empty
THEN create HIGH feasibility issue.

IF dependency references missing predecessor/successor
THEN create HIGH feasibility issue.

IF dependency creates circular logic
THEN create HIGH feasibility issue.

IF dependency is inferred
THEN create assumption issue affecting Feasibility.
```

---

# **12. Risk Register Model**

```
class Risk(BaseArtifactElement):
    risk_id: str
    impact: ImpactLevel
    likelihood: ImpactLevel
    mitigation: List[str] = []
    linked_artifact_ids: List[str] = []

class RiskRegisterArtifact(BaseModel):
    artifact_id: str
    risks: List[Risk] = []

    score: Optional[ArtifactScore] = None
    issues: List[Issue] = []
```

## **Risk Validation Rules**

```
IF risks is empty
THEN create MEDIUM feasibility issue.

IF high-impact risk has no mitigation
THEN create HIGH feasibility issue.

IF risk has no linked_artifact_ids
THEN create MEDIUM alignment issue.

IF risk is inferred and high-impact
THEN surface in snapshot.
```

---

# **13. Assumptions Register Model**

```
class Assumption(BaseArtifactElement):
    assumption_id: str
    impact: ImpactLevel
    validation_required: bool = True
    linked_artifact_ids: List[str] = []

class AssumptionsRegisterArtifact(BaseModel):
    artifact_id: str
    assumptions: List[Assumption] = []

    score: Optional[ArtifactScore] = None
    issues: List[Issue] = []
```

## **Assumption Validation Rules**

```
IF inferred assumptions exist
THEN create assumption issues.

IF high-impact assumption requires validation
THEN surface in snapshot.

IF assumption has no linked artifact
THEN create MEDIUM alignment issue.

IF assumption impacts schedule or resource plan
THEN affect Feasibility score.
```

---

# **14. Acceptance Criteria Model**

```
class AcceptanceCriterion(BaseArtifactElement):
    criteria_id: str
    linked_scope_item_ids: List[str] = []
    linked_requirement_ids: List[str] = []

class AcceptanceCriteriaArtifact(BaseModel):
    artifact_id: str
    acceptance_criteria: List[AcceptanceCriterion] = []

    score: Optional[ArtifactScore] = None
    issues: List[Issue] = []
```

## **Acceptance Criteria Validation Rules**

```
IF acceptance_criteria is empty
THEN create HIGH clarity issue.

IF acceptance criterion has no linked requirement or scope item
THEN create MEDIUM alignment issue.

IF acceptance criterion is vague or not testable
THEN create HIGH clarity issue.
```

---

# **15. Schedule Artifact Model**

```
class ScheduleActivity(BaseArtifactElement):
    activity_id: str
    linked_wbs_id: Optional[str] = None
    duration_estimate: Optional[float] = None
    duration_unit: Optional[str] = "days"
    dependency_ids: List[str] = []
    assigned_resource_ids: List[str] = []
    milestone: bool = False
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class ScheduleArtifact(BaseModel):
    artifact_id: str
    activities: List[ScheduleActivity] = []
    milestones: List[ScheduleActivity] = []
    critical_path_activity_ids: List[str] = []
    estimated_duration_range: Optional[str] = None

    score: Optional[ArtifactScore] = None
    issues: List[Issue] = []
```

## **Schedule Validation Rules**

```
IF activities are generated before sufficient WBS confidence
THEN mark schedule as preliminary.

IF activity has no linked_wbs_id
THEN create HIGH alignment issue.

IF activity has no duration_estimate
THEN create HIGH feasibility issue.

IF activity has dependencies missing
THEN create HIGH feasibility issue.

IF activity has no assigned resource
THEN create HIGH feasibility issue.

IF exact dates are inferred
THEN do NOT show them in snapshot.
```

---

# **16. Snapshot Rendering Rules**

## **Intent Snapshot**

Show only:

```
- Top 1–3 outcomes
- High-level objectives
- Critical constraints
- High-impact assumptions
- Missing success metrics
```

Hide:

```
- full stakeholder model
- full dependency list
- full assumption register
- detailed risks
```

---

## **Planning Snapshot**

Show only:

```
- Scope themes
- Requirement clusters
- Top-level WBS nodes
- Resource signals
- High-impact assumptions
- High-impact risks
```

Hide:

```
- full requirements list
- full WBS hierarchy
- detailed resource allocation
- full dependency map
- full risk register
```

---

## **Schedule Snapshot**

Show only:

```
- Estimated duration range
- High-level phases
- sequencing risks
- resource feasibility concerns
```

Hide:

```
- exact dates
- detailed Gantt
- full critical path
- activity-level schedule
```

---

# **17. Snapshot Issue Prioritization**

At the end of the 60-second flow, show:

```
Top 3–5 issues only
```

Ranking formula should consider:

```
priority_score =
  issue_impact_weight
+ affected_score_weight
+ confidence_penalty
+ downstream_dependency_weight
+ user_actionability_weight
```

Suggested weighting:

```
IMPACT_WEIGHT = {
    "high": 40,
    "medium": 20,
    "low": 10
}

SCORE_WEIGHT = {
    "clarity": 15,
    "alignment": 20,
    "feasibility": 25
}

CONFIDENCE_PENALTY = {
    "low": 20,
    "medium": 10,
    "high": 0
}
```

---

# **18. Next Best Action Rule**

OSLO must identify one primary action.

Selection criteria:

```
Next Best Action =
highest score impact
+ lowest user effort
+ unlocks downstream artifact quality
+ improves confidence
```

Examples:

```
“Define measurable success metrics for the primary outcome.”

“Confirm whether the marketing site must support lead capture at launch.”

“Add resource availability for design and engineering roles.”

“Confirm the target launch date or desired delivery window.”
```

---

# **19. Chat Integration Requirements**

When user clicks an issue:

```
1. Issue context loads into OSLO chat
2. Chat explains the issue briefly
3. Chat asks for the specific missing/refinement input
4. User responds
5. Artifact updates
6. Scores update
7. Issue list reprioritizes
```

Example:

```
Issue: Success metrics missing

OSLO Chat:
“To improve Clarity and Alignment, we need measurable success criteria for your primary outcome. What would make this project successful? For example: increase demo requests by 25%, reduce onboarding time by 30%, or launch by a specific deadline.”
```

---

# **20. Progressive Improvement Loop**

```
User Input
→ Artifact Update
→ Validation
→ Issue Refresh
→ Score Update
→ Next Best Action Update
```

This loop is required.

No static report behavior.

---

# **21. Prohibited Behaviors**

Engineering must not build:

```
- separate lightweight artifact objects
- full project plan at 60 seconds
- exact schedule dates without confidence
- unfiltered issue dumps
- recommendations not tied to issues
- scores without explanations
- chat disconnected from issue context
```

---

# **22. Final Engineering Directive**

OSLO’s first-time experience should communicate:

```
“We understand your project.
Here is what is clear.
Here is what is missing.
Here is what may break.
Here is the highest-impact thing to fix next.”
```

It must not communicate:

```
“Here is your complete project plan.”
```

Final product behavior:

> OSLO should feel like an intelligent project governance co-pilot, not a project document generator.
>