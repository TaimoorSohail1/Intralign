# Data Flow Diagram

Attaching both a diagram description and diagram for OSLO Framework to be used by development team to implement. Critically analyze for any issues not in alignment with our design.

Here are the misalignments / risks I see versus the OSLO design intent, plus concrete fixes.

## **Key misalignments in the diagram**

### **1) “Canon” is shown as an output of Intake only**

- Your OSLO model treats **inference as part of the canon** (epistemically tagged), not something that lives only “between layers.”
- In the diagram, L2 produces “Findings & EvidenceChains” but it’s not shown **writing back into canonical state** (versioned).

**Fix:** Add an explicit **Canonical Store / Knowledge Graph** (or “Canon”) node, with:

- L1 writing asserted facts → Canon
- L2 writing inferred nodes + evidence links → Canon (tagged inferred/assumed/etc.)
- L6 writing reality signals → Canon (tagged observed/telemetry)

### **2) Reality signals bypass Intake/Canon and go straight into Reasoning**

- In OSLO, execution signals must be **ingested, normalized, and versioned** before they are reasoned over (auditability + determinism + evidence chaining).
- Direct L6 → L2 implies “ephemeral signals” can influence reasoning without being captured as evidence.

**Fix:** Route **L6 → L1 (or Canon)** first, then L2 consumes the updated canon.

### **3) Missing user-interaction feedback loop**

- OSLO Communication isn’t only “output to UI.” It also triggers:
    - clarifying questions
    - evidence requests
    - confirmations / corrections
- Without L5/UI → L1, the system looks one-way, which undermines your “judgment-under-uncertainty” posture and Pass-based behavior.

**Fix:** Add **UI → L1 Intake** as “User responses / clarifications / artifact uploads.”

### **4) Governance → Communication contract is underspecified**

You previously called out the absence of a direct L4↔L5 relationship. This diagram adds “IssueDispositions,” but governance typically constrains more than dispositions:

- allowed/suppressed content classes
- required disclosures (epistemic labeling)
- posture/tier policies
- escalation rules
- action gating rationale (what can be stated, suggested, asked, or executed)

**Fix:** Rename/expand the arrow to something like:

- **“Communication Directives (policy + disclosures + narrative constraints) + Issue Dispositions”**

### **5) “Reasoned Comm Units (RCUs)” wording subtly breaks layering**

Calling them “Reasoned” suggests L5 is doing reasoning. In OSLO, L5 should be **rendering + interaction design** under governance constraints, not re-reasoning.

**Fix:** Rename RCUs to something like:

- **Governed Communication Units (GCUs)** or **Comms Units (policy-bound)**

### **6) Governance receives only “Issues & Health Scores”**

Depending on your existing contracts, Governance typically also needs:

- proposed actions (candidate actions/classes) to authorize/deny
- required comm actions (ask / disclose / warn / suppress)
- confidence/uncertainty metadata

If those are inside “Issues,” fine—but it’s ambiguous and invites implementation drift.

**Fix:** Change L3 → L4 payload label to something like:

- **“Judgments: issues + scores + uncertainty + proposed actions”**

### **7) “Initial prompt till UI” purpose statement conflicts with L6 loop**

Your description says the flow is from initial prompt to UI, but the diagram includes Execution and Reality Signals (which is good for OSLO, but conflicts with the stated scope).

**Fix:** Either:

- update the purpose to “prompt → UI **and** closed-loop execution monitoring,” or
- split into two diagrams: **Plan Generation Path** and **Closed-Loop Path**.

## **Minor but practical clarity issues**

- “Canonical Artifacts” implies documents; OSLO canon is **structured, versioned representation**, not necessarily “artifacts.” Consider “Canonical State / Canonical Graph.”
- If you want devs to implement correctly, include (even as footnotes):
    - versioning boundaries per layer output
    - epistemic tags required on every node/claim
    - audit/event log sidecar (even if not drawn)

If you want, I can rewrite the “Purpose” block into an engineering-facing paragraph (scope, invariants, and what each arrow *must* contain) so it can sit above the diagram as implementation guidance.