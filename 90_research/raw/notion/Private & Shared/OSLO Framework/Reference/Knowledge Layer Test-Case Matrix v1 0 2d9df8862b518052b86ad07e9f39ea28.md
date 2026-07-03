# Knowledge Layer Test-Case Matrix v1.0

---

## **A. Config and Contract Loading**

| **ID** | **Test** | **Inputs** | **Steps** | **Expected Result** |
| --- | --- | --- | --- | --- |
| A1 | Type registry loads | type_registry.yaml/json | Start service, load registry | Service boots; all object/edge/artifact keys registered |
| A2 | Unknown type rejected | registry + invalid object type | Attempt to create object with unknown object_type | Write rejected with deterministic error |
| A3 | Artifact schemas load | schemas/*.json | Start service, load schemas | Service boots; schema versions available |
| A4 | Schema mismatch rejected | valid plan + invalid field | Write field not in schema | Write rejected; error names field_key and artifact |

---

## **B. Tenancy and Isolation**

| **ID** | **Test** | **Inputs** | **Steps** | **Expected Result** |
| --- | --- | --- | --- | --- |
| B1 | Workspace isolation | Workspace A + Workspace B | Create objects in A; query from B | Query returns none / forbidden |
| B2 | Membership enforcement | User not in workspace | Attempt read/write | Forbidden |
| B3 | Plan scoping | Two plans same workspace | Query plan1 objects using plan2 id | Returns none / error |

---

## **C. Artifact Versioning and Immutability**

| **ID** | **Test** | **Inputs** | **Steps** | **Expected Result** |
| --- | --- | --- | --- | --- |
| C1 | Create version v1 draft | Artifact instance | Create v1 draft with objects/fields | v1 created; version_number=1 |
| C2 | Publish immutability | Published v1 | Publish v1; attempt update | Update rejected; v1 unchanged |
| C3 | New version from prior | Published v1 | Create v2; modify fields | v2 created; v1 unchanged |
| C4 | Monotonic numbering | v1→v2→v3 | Create multiple versions | version numbers strictly increase |
| C5 | Pointer correctness | artifact pointer table | Publish v2; check pointer | current_version points to v2 |

---

## **D. Workflow and Artifact Sequencing**

| **ID** | **Test** | **Inputs** | **Steps** | **Expected Result** |
| --- | --- | --- | --- | --- |
| D1 | Default workflow enforced | workflow_def + steps | Create default workflow | Created successfully |
| D2 | Workflow must start Intent→Context | invalid workflow | Step 1 not Intent OR step 2 not Context | Creation rejected |
| D3 | Plan binds workflow | plan + workflow | Assign workflow to plan | Plan workflow active |
| D4 | Workflow step ordering | steps out of order | Create steps with duplicate/missing indices | Rejected or normalized deterministically |

---

## **E. Structural Graph Invariants**

| **ID** | **Test** | **Inputs** | **Steps** | **Expected Result** |
| --- | --- | --- | --- | --- |
| E1 | WBS must be acyclic | WBS edges | Create HAS_CHILD cycle | Write rejected |
| E2 | WBS parent uniqueness (if required) | WBS node | Add two parents to same child | Write rejected |
| E3 | Schedule dependencies acyclic | PRECEDES edges | Create PRECEDES cycle | Write rejected |
| E4 | Edge type validation | edge registry | Create edge with invalid src/dst types | Write rejected |
| E5 | Required edges exist | objects needing edges | Create object missing required linkage | Validator flags failure (or blocks write) |

---

## **F. Work Objects inside Schedule Execution Sub-Layer**

| **ID** | **Test** | **Inputs** | **Steps** | **Expected Result** |
| --- | --- | --- | --- | --- |
| F1 | Work object must map to exactly one WBS | Task + WBS | Create Task with 0 MAPS_TO_WBS edges | Rejected |
| F2 | Reject >1 WBS mappings | Task + 2 WBS | Add two MAPS_TO_WBS edges | Rejected |
| F3 | Mapping must target WBSElement | Task + Requirement | MAPS_TO_WBS to non-WBS | Rejected |
| F4 | Optional Epic/Story allowed | Epic + WBS | Create Epic with mapping | Accepted |
| F5 | Execution hierarchy allowed | Task + SubTask | Create parent-child between work objects | Accepted |
| F6 | Execution hierarchy must not replace WBS | Task hierarchy only | Remove MAPS_TO_WBS, rely on parent | Rejected |

---

## **G. Provenance and Source State**

| **ID** | **Test** | **Inputs** | **Steps** | **Expected Result** |
| --- | --- | --- | --- | --- |
| G1 | Store explicit field | object + field | Write field with source_state=explicit | Stored correctly |
| G2 | Store inferred field | object + field | Write field with source_state=inferred | Stored + distinguishable |
| G3 | Store derived field | object + field | Write field with source_state=derived | Stored + distinguishable |
| G4 | Preserve provenance on new version | v1→v2 | Copy forward object; change one field | Only updated fields change; provenance preserved for others |
| G5 | Inference-prohibited-for-judgment still storable | flagged field | Store inferred value for prohibited field | Stored but flagged; not overwritten |
| G6 | Confidence tracking | inferred fields | Persist confidence values | Queryable and accurate |

---

## **H. Traceability, Queries, and Reports**

| **ID** | **Test** | **Inputs** | **Steps** | **Expected Result** |
| --- | --- | --- | --- | --- |
| H1 | End-to-end traceability path | Outcome→Req→WBS→Task | Create edges SUPPORTS_OUTCOME, COVERS_REQUIREMENT, MAPS_TO_WBS | Traversal returns correct closure set |
| H2 | Orphan detection query | orphaned objects | Create Requirement with no SUPPORTS_OUTCOME | Query returns it as orphan |
| H3 | Outcome coverage query | multiple outcomes | “Show all objects supporting Outcome X” | Correct set only |
| H4 | Report version binds artifact versions | report + artifact versions | Create Report v1; bind specific artifact versions | Report always resolves to those versions |
| H5 | Report immutability | published report | Modify rendered_content after publish | Rejected |
| H6 | Comment auth gating (data-layer) | anon comment attempt | Insert comment with null user where policy forbids | Rejected or flagged per rule |

---

## **Minimum “Green Bar” Suite (if you want the leanest CI gate)**

If you only gate on 8 tests initially, make it:

- C2 (immutability)
- D2 (Intent→Context workflow rule)
- E1 (WBS acyclic)
- E3 (Schedule deps acyclic)
- F1 (Task maps to exactly one WBS)
- G2 (inferred provenance stored)
- H1 (traceability traversal)
- H4 (report binds versions)

---

If you want, I can convert this matrix into a **starter Gherkin/BDD suite** (Feature files grouped A–H) so your engineer can wire them into CI immediately.