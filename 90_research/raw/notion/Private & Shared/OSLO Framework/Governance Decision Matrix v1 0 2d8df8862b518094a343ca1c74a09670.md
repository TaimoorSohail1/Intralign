# Governance Decision Matrix v1.0

---

**System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)

**Artifact Type:** Implementation Guide

**Status:** Canonical

**Audience:** Engineering, Product, QA

**Applies To:** All Governance decisions that gate visibility, timing, and surface selection for Reasoning/Judgment outputs.

---

## **1. Inputs Governance Must Evaluate (Required)**

Governance decisions MUST consider **all** of the following:

- lifecycle_phase ∈ {Draft, Active, Monitoring, Execution}
- workflow_mode ∈ {60Second, InteractiveBuild, SteadyState}
- user_state ∈ {Exploring, Focused, Responding}
- signal_type ∈ {Score, Issue, Drift, Summary}
- confidence ∈ {High, Medium, Low}
- placeholder_conditioned ∈ {true, false}
- blocking ∈ {true, false}
- recent_acknowledgement ∈ {true, false}

If any input is missing → **default to suppression**.

---

## **2. Hard Stops (Absolute Rules)**

These rules **override everything else**.

| **Condition** | **Decision** |
| --- | --- |
| workflow_mode = 60Second | **SUPPRESS ALL INTERRUPTIVE OUTPUTS** |
| user_state = Focused AND signal_type ≠ Drift(blocking) | **SUPPRESS** |
| confidence = Low AND signal_type ≠ Summary | **SUPPRESS** |
| recent_acknowledgement = true | **SUPPRESS** |
| Mutation implied without UI authorization (G-03) | **BLOCK** |

---

## **3. Surface Eligibility Matrix**

If not suppressed, select the **least-salient surface** that satisfies the condition.

### **3.1 Planning Phases (Draft / Active / Monitoring)**

| **Conditions** | **Allowed Surface** |
| --- | --- |
| Placeholder-conditioned = true | Inline / Summary |
| Confidence = Medium | Panel |
| Confidence = High AND blocking = true AND user_state = Responding | Modal |
| Confidence = High AND non-blocking | Panel |
| Repeated non-blocking signals | Aggregated Summary |
| Any condition + Chat | **DISALLOWED by default** |

> Chat requires explicit override justification.
> 

---

### **3.2 Interactive Build Mode**

| **Conditions** | **Allowed Surface** |
| --- | --- |
| Editing specific artifact | Inline only |
| Cross-artifact signal | Suppress |
| Blocking structural break | Inline callout |
| Placeholder-conditioned | Inline (annotated) |

---

### **3.3 Monitoring Phase**

| **Conditions** | **Allowed Surface** |
| --- | --- |
| High confidence drift | Panel / Notification |
| Medium confidence drift | Dashboard |
| Placeholder-conditioned | Dashboard only |
| Repeated alerts | Roll-up Summary |

---

### **3.4 Execution Phase (Forward-Declared)**

| **Conditions** | **Allowed Surface** |
| --- | --- |
| Blocking, high confidence | Modal (rare) |
| Non-blocking | Summary |
| Placeholder-conditioned | Suppress |
| Automation required | **Disallowed (opt-in contract required)** |

---

## **4. Score-Specific Governance Rules**

| **Score Condition** | **Governance Action** |
| --- | --- |
| Low score + placeholder-conditioned | Surface passively |
| Low score + high confidence | Consider panel |
| High score | No special treatment |
| Rapid score fluctuation | Suppress, wait for stabilization |

> Scores never trigger interrupts by themselves.
> 

---

## **5. Issue-Specific Governance Rules**

| **Issue Type** | **Default Action** |
| --- | --- |
| Clarity gap | Suppress during Draft |
| Alignment conflict | Panel if confidence ≥ Medium |
| Feasibility blocker | Inline or Panel (never chat) |
| Representation drift | Inline if Focused, Panel otherwise |

---

## **6. Decision Output Schema (Engine-Ready)**

Governance must emit a **decision object**, never text:

```
GovernanceDecision {
  action: "SUPPRESS" | "SURFACE",
  surface: "NONE" | "INLINE" | "PANEL" | "SUMMARY" | "MODAL",
  reason_codes[],
  requires_disclosure: true | false,
  justification_snapshot_id
}
```

---

## **7. Default-to-Silence Rule**

> If multiple rules conflict, the most suppressive outcome wins.
> 

This is intentional.

---

## **8. Test Cases (Minimum Set)**

Engineering must validate at least:

1. 60-Second flow never interrupts
2. Placeholder-conditioned low confidence never surfaces as modal
3. Focused editing suppresses cross-artifact alerts
4. Same issue acknowledged twice never re-interrupts
5. Execution signals never mutate planning knowledge
6. Chat never triggers without explicit override

---

## **Canonical Close**

> Governance is not a recommendation engine.
> 

> It is an attention firewall.
> 

> When in doubt, do nothing.
> 

---

If you want next, I can:

- Convert this into **policy code (YAML / JSON)**
- Create **QA automation scenarios**
- Build a **state-transition diagram**
- Generate **lint rules for layer violations**

Just say where to go next.