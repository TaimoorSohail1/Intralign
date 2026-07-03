# Reasoning Layer — Implementation-Ready Checklist (v1.0)

**System:** OSLO

**Layer:** Reasoning

**Audience:** Lead Engineer, QA

**Goal:** Implement a deterministic, auditable Reasoning Layer that emits canonical Findings consumable by Judgment.

---

## **1. Foundations**

☐ **Lock the Reasoning public contract**

- Output payload schema: ContextEnvelope + ReasoningRunHeader + Findings[] + EvidenceIndex
- Finding schema + enums (types, domains, severities, statuses)
- Stable ordering + stable IDs requirements

☐ **Lock version identifiers**

- reasoning_ruleset_version
- policy_version (pass-through)
- determinism_key composition (ruleset + config + engine version)

☐ **Define Reasoning execution modes**

- PASS_1_STRUCTURAL
- PASS_2_INFERENTIAL
- CONTINUOUS (if included in v1; otherwise explicitly out-of-scope)

---

## **2. Inputs & Canonical Read Model**

☐ **Canonical read-only inputs only**

- Canonical project state snapshot (facts + inferences already in canon)
- Lifecycle stage (explicit)
- Mode/pass (explicit)
- Tier (explicit)

☐ **Input snapshot semantics**

- Create snapshot_hash for all canonical inputs consumed
- Ensure the run is reproducible from the snapshot

☐ **Forbidden inputs blocked**

- Raw user text (unless already canonicalized in Knowledge)
- Free-form LLM completions
- UI state / client-derived flags

---

## **3. Rules & Policy Repository (Executable Constraints)**

☐ **Rules are externalized files**

- Typed rule definitions (no prose-only rules)
- Operators supported are explicitly enumerated
- Rule file schema validated at load time

☐ **Rule determinism**

- No randomness
- No clock-time dependence (except via explicit timestamp input)
- No non-deterministic iteration (e.g., unordered maps without sorting)

☐ **Rule ordering contract**

- Define and enforce evaluation order (by domain, artifact, element path, rule priority)

---

## **4. Finding Generation (Core Engine)**

☐ **Implement Finding builders**

- One builder per finding_type category:
    - STRUCTURE_GAP
    - CONTENT_QUALITY_GAP
    - SMART_GAP
    - ALIGNMENT_GAP
    - FEASIBILITY_RISK
    - DRIFT_SIGNAL
    - CONFLICT | INCONSISTENCY
    - MISSING_EVIDENCE

☐ **Deterministic Finding IDs**

- finding_id = hash(finding_type + domain + target_ref + summary_code + key_parameters + ruleset_version)
- Verify stable ID across runs with identical inputs

☐ **Stable Finding ordering**

- Sort findings deterministically:
    
    domain → target_ref.element_path → severity → finding_type → finding_id
    

☐ **No duplicate findings**

- Define dedupe key (same as ID inputs)
- Ensure dedupe occurs after normalization

---

## **5. Evidence Index (Traceability)**

☐ **Evidence objects are first-class**

- evidence_type: CANON_FACT | CANON_INFERENCE | DERIVED_METRIC | RULE_TRACE
- Every non-INFO finding must reference evidence

☐ **Evidence referential integrity**

- All evidence_refs resolve to evidence_index
- Reject / fail run if any reference is missing

☐ **Rule trace capture**

- For each finding, store:
    - rule id
    - operator path
    - matched canonical paths
    - snapshot hash

---

## **6. Pass / Mode Behavior (Strict)**

☐ **PASS 1 — Structural baseline**

- Only emits:
    - STRUCTURE_GAP
    - MISSING_EVIDENCE
    - INCONSISTENCY (structure-only)
- **No inference-derived gaps** in Pass 1

☐ **PASS 2 — Inferential reasoning**

- Allowed:
    - content quality gaps
    - SMART gaps
    - alignment gaps
    - feasibility risks
    - conflicts
- Must tag inference dependence in evidence types (CANON_INFERENCE)

☐ **Mode is never inferred**

- Must be explicit input and emitted in ContextEnvelope

---

## **7. Run Header & Error Semantics**

☐ **ReasoningRunHeader required**

- run_id, input_hash, determinism_key, started_at, completed_at, status, error_code

☐ **Error policy**

- FAILED_VALIDATION: schema issues, missing context, evidence integrity failures
- FAILED_EXECUTION: engine failure/exception
- If status != SUCCESS:
    - findings must be empty
    - evidence_index may include error traces only (if desired)
    - error_code required

---

## **8. Supersession & Retention (Across Runs)**

☐ **Supersession logic implemented**

- Emit supersedes[] when a new finding replaces an older one (same dedupe key, different ID inputs)
- Never mutate prior run outputs

☐ **Retention policy**

- Keep historical runs for audit
- Define retrieval: “latest applicable run per lifecycle/mode”

---

## **9. Observability (Audit-First)**

☐ **Log every run**

- input_hash + determinism_key
- counts by finding_type and severity
- evidence integrity status
- execution timings

☐ **Replay capability**

- Store references sufficient to re-run:
    - snapshot hash
    - ruleset version
    - config version
    - engine version

---

## **10. Test Suite (Implementation-Ready)**

☐ **Contract tests**

- Output schema validation
- Stable ordering
- Stable IDs
- Enum boundedness
- Evidence referential integrity

☐ **Determinism tests**

- Same snapshot + ruleset → identical payload
- Conflict resolution deterministic

☐ **Mode tests**

- Pass 1 never emits inferential finding types
- Pass 2 emits allowed types only

☐ **Negative tests**

- Missing lifecycle/mode/tier → FAILED_VALIDATION
- Unknown rule operator → FAILED_VALIDATION
- Evidence ref missing → FAILED_VALIDATION

---

## **11. Explicitly Out of Scope (v1)**

☐ Natural-language explanations for UI

☐ Recommendations / actions

☐ Learning / tuning from outcomes

☐ Cross-project benchmarking

☐ Non-deterministic heuristics

---

## **Final “Done” Gate**

> Can Judgment consume Reasoning output with
> 
> 
> **strict parsing**
> 
> **replayable determinism**
> 
> **canonical evidence**
> 

If yes → Reasoning layer is implementation-complete for v1.