# Judgement, Governance, and Communication Layer Responses

Below are implementation-explicit answers. I’m going to resolve each “gap” by turning it into **a hard rule + where it lives in code + what gets stored**. No subjective room.

---

# **0) Non-negotiable layer contracts (so implementation is deterministic)**

## **Judgment Layer (J)**

**Input:** Reasoning Findings + Canonical constraints + Project policy profile

**Output:** **Judgment Records** (severity, disposition recommendation, confidence, required actions)

**Write permissions:**

- May write **Judgment Records** into **Machine Repository** (MR) as run output
- May NOT modify canonical plan
- May NOT resolve disputes by itself

## **Governance Layer (G)**

**Input:** Judgment Records + System reliability state + User posture/authorization state

**Output:** **Governance Decisions** (what to surface, when, where, and which UI actions are allowed)

**Write permissions:**

- May write governance state + suppression reasons + notification obligations (CS or MR; see below)

## **Communication Layer (C)**

**Input:** RCUs (render-agnostic units) + Governance Decisions

**Output:** UI payloads (chat message, panel cards, PDF sections)

**Write permissions:** None to plan. It only produces text/UI view models.

---

# **Judgment Layer**

## **1) “Normative” vs deterministic (subjectivity gap)**

**Answer:** “Normative” means “based on declared policy,” not “human vibes.” Determinism means **same inputs → same outputs**.

### **Where thresholds live**

They live in a **versioned Policy Profile** in Canonical Store.

**CS tables:**

- policy_profile
    - policy_profile_id
    - project_id
    - version
    - created_at
    - active boolean
    - content JSON (thresholds + mappings)

### **How “High vs Medium” is decided**

Judgment must use a **pure function**:

```
severity = map(score_vector, confidence, policy_profile.thresholds)
```

Example mapping rule (deterministic):

- If impact >= 0.7 AND likelihood >= 0.6 → HIGH
- else if impact >= 0.5 → MEDIUM
- else → LOW

### **How adjusted if PM disagrees**

PM disagreement is not an ad-hoc override. There are only two supported mechanisms:

1. **Policy change** (project-level governance):
- user edits policy profile thresholds (authorized UI)
- new profile version becomes active
- next judgment run uses it
1. **Case override** (exception handling):
- stored as a **canonical override** attached to a specific finding case
- overrides only that case’s severity, not the policy globally

**CS tables:**

- finding_case_override
    - finding_case_id
    - override_severity
    - reason
    - created_by_user_id
    - expires_at nullable

Judgment must read overrides and apply them after computing default severity.

**Determinism preserved** because overrides + policy are explicit stored inputs.

---

## **2) Confidence vs Score paradox**

**Answer:** Score and Confidence are **not two competing numbers**. They represent different dimensions and must be displayed as such.

### **Required semantics (hard rule)**

- **Score** = “Best-estimate evaluation of plan quality *given the available model*”
- **Confidence** = “Reliability of that score based on evidence completeness + contradiction level”

They cannot be merged without losing critical information (otherwise the system hides uncertainty).

### **Implementation: Score must be “conditional”**

In UI and API it must be labeled as:

> “Feasibility Score (given current inputs)”
> 

### **What should the user do with “100% score, low confidence”**

Governance must convert this into a **Reliability Warning** RCU:

- “This score is based on incomplete/weak evidence; treat as provisional.”
- Required CTA: “Provide missing facts” or “Validate assumptions”

### **Deterministic coupling rule (to avoid nonsense)**

Judgment must enforce a constraint:

- If confidence == LOW, score_cap = 0.85 (example)
    
    or
    
- If confidence == LOW, score is displayed with “provisional” badge and cannot show “green/complete” state.

Pick one rule and make it policy-driven. Implementation must not allow “perfect/green” plan state while confidence is low.

**Where the rule lives:** Policy Profile JSON:

- display_constraints: { block_green_if_confidence_below: MEDIUM }
    
    or score_caps_by_confidence.
    

---

## **3) Human-in-the-loop location (user disagrees with severity)**

**Answer:** Human feedback lives in **Canonical Store** as **Judgment Overrides and Constraints**, not as “facts.”

Two distinct user actions:

### **A) “Your severity is wrong”**

That is not a fact. It is a **governance preference / override**.

Store:

- finding_case_override (as above)

Judgment must stop overriding because it must always:

1. compute default severity
2. check finding_case_override
3. output final severity = override if present

### **B) “Your underlying assumption is wrong”**

That *is* a fact/constraint issue.

Store in CS:

- constraint / asserted_value at element level (e.g., “Start date is X”)
- or “Rejected inferred date Y” constraint (from previous message)

Then Reasoning will stop generating the candidate; Judgment will never see it.

**Where HITL sits in code:** UI writes to CS (authorized), then the next run consumes CS as input.

---

# **Governance Layer**

## **4) “Fail-silent” safety risk**

**Answer:** Fail-silent applies only to **proactive recommendations**, not to **system health disclosure**.

### **Hard rule**

If Governance suppresses output due to reliability, it must still emit a **System Health RCU** that is:

- visible in the UI (banner/badge)
- non-dismissable during the degraded period
- includes the reason + last successful monitoring timestamp

So: **not silent**; silent only about *advice*, not about *monitoring state*.

### **Required fields (CS or MR)**

- system_health_state
    - project_id
    - state ENUM: OK | DEGRADED | FAIL_SILENT
    - reason_codes[] (e.g., BUDGET_EXHAUSTED, CONTEXT_STALE, DATA_CONFLICT)
    - last_successful_run_at
    - updated_at

Governance must always render a health indicator if state != OK.

---

## **5) G-03 Authorization blur (chat CTA vs panel button)**

**Answer:** The distinction is not “chat vs panel.” The distinction is **authorized UI action vs non-authoritative text**.

### **Hard rule**

Any plan mutation must be executed only by a **UI Action Service** that:

- validates an authorization token
- validates the action is allowed by Governance
- writes to CS
- logs an audit record

Chat can display a CTA, but it must call the **same UI Action Service** as any panel button.

So the real contract is:

- **Chat text** cannot mutate.
- **UI Action invocation** can mutate (regardless of where the button is rendered).

### **Implementation**

- POST /actions/apply_fix
    - requires action_token minted by Governance
    - token includes project_id, allowed_action_ids, expires_at, context_hash

This removes terminology ambiguity.

---

## **6) ContextService bottleneck (high-speed edits, stale evidence)**

**Answer:** Context snapshots must be **coalesced** and **versioned**, and runs must be cancellable.

### **Required model**

- Every canonical change increments canonical_revision for the project.
- ContextService creates system_context snapshots tied to a revision.

**CS fields:**

- project.canonical_revision (monotonic integer)

**MR table:**

- system_context
    - context_id
    - project_id
    - canonical_revision
    - context_hash
    - created_at

### **Coalescing rule (must implement)**

If multiple edits occur quickly:

- Only the **latest revision** is eligible for new runs.
- Older queued contexts are **superseded** and must not be processed unless explicitly requested for audit/replay.

### **Staleness guard (must implement)**

Every Reasoning/Judgment/Governance run must include context_hash.

If, at completion time, the project revision has advanced beyond the run’s revision:

- mark run STALE
- do not surface its outputs (except for internal audit)
- optionally schedule a run for the latest revision

This prevents obsolete evidence chains from reaching UI.

---

# **Communication Layer**

## **7) “LLM expression only” sandboxing (avoid meaning drift)**

**Answer:** You do not “trust” an LLM. You **constrain it** and **verify outputs**.

### **Hard rule: LLM never receives raw freedom**

It receives:

- A fully structured RCU JSON (facts, epistemic statuses, boundary statements)
- Allowed style instructions
- A requirement to output **a templated format** with placeholders preserved

### **Two enforcement mechanisms (both required)**

1. **Structural templating**
- The output must preserve required fields verbatim:
    - Boundary Statements
    - Epistemic labels (FACT / INFERRED / UNKNOWN)
    - CTA disclaimers
- Implement by using message templates with explicit slots, e.g.:
    - {{BOUNDARY_STATEMENT}} inserted without rewriting
    - {{EPISTEMIC_TAGS}} rendered by code, not the LLM
1. **Post-generation contract validator**
- Parse LLM output into a structured message schema
- Validate:
    - all required boundary blocks present
    - no epistemic tag changes
    - no removal of “system health” notices when required
        
        If validation fails → fallback to deterministic non-LLM renderer.
        

**Net:** LLM is optional sugar. Deterministic renderer is always available.

---

## **8) RCU surface invariance vs progressive disclosure**

**Answer:** Progressive disclosure happens at the **renderer**, not by changing the RCU.

### **Hard rule**

RCU must be complete. Views choose how much to show via:

- view_projection rules (summary vs full)
- not by truncating the underlying meaning

### **Implementation**

RCU contains:

- headline
- summary (short)
- details (full)
- evidence_refs[]
- boundary_statements[]
- cta_options[]

Chat renderer shows headline + summary and a “View details” link. Panel renderer shows headline + summary + details + evidence.

No truncation of “details” is allowed unless:

- the UI explicitly hides it behind a disclosure control
- and the user can always access the full RCU

Meaning is preserved because the RCU itself isn’t modified.

---

## **9) “No action implication” rule + delegated action language**

**Answer:** If the system can change data (delegated posture), it must do so via the **same UI Action Service** and must emit a **Change Disclosure RCU**.

### **Hard rule**

- If any mutation occurs, a disclosure record is mandatory.
- Language must state **what happened**, **who authorized**, and **where to review**.

### **How to say it without sounding authoritative**

Use a fixed disclosure template (not LLM-invented):

> “Change applied (user-authorized): [what changed].
> 

> Source: [which recommendation/case].
> 

> Review: [link/button to diff].”
> 

If delegated posture is enabled (pre-authorization), disclosure must say:

> “Change applied under your delegation settings.”
> 

### **Storage**

- CS stores mutation audit:
    - plan_change_event {event_id, action_id, actor=SYSTEM, authorized_by=user_id or delegation_policy_id, before_hash, after_hash, created_at}

Communication can only say it changed data if a plan_change_event exists for the referenced action_id.

---

# **Implementation-ready summary (what you tell him to build)**

1. **Deterministic Judgment** driven by **versioned Policy Profiles** + optional **case overrides** stored in CS.
2. **Score and Confidence** are separate; UI must treat low-confidence as non-green via policy constraints.
3. **Human feedback** is stored as **overrides/constraints** in CS and must be consumed on every run.
4. **Fail-silent suppresses advice, never hides monitoring state**—always surface a health RCU with timestamp.
5. **Authorization is enforced at an Action Service**, not by “chat vs panel.” CTAs mint tokens; actions mutate.
6. **Context snapshots are versioned + coalesced**; stale runs are discarded from UI by revision/hash check.
7. **LLM is sandboxed by templates + validators + fallback renderer**; it cannot remove boundaries or change epistemic status.
8. **RCU contains summary + details**; progressive disclosure is view projection, not truncation.
9. **Delegated actions require audit events + mandatory disclosure RCUs** with fixed wording.

If you want this to be fully “buildable,” I can output **three concrete JSON schemas** (JudgmentRecord, GovernanceDecision, RCU) plus the **ActionToken** schema and required validation rules.