# Reasoning Layer Test Case Matrix v1.0

**System:** OSLO

**Layer:** Reasoning

**Purpose:** QA/CI-ready matrix to verify Reasoning compliance (truth, determinism, evidence, isolation, placeholder rules)

**Aligned to:** Reasoning Layer Spec v1.0 + Reasoning Invariants Spec v1.0

---

## **A. Core invariants and boundary enforcement**

| **TC ID** | **Scenario** | **Setup** | **Action** | **Expected Result** | **Invariants** |
| --- | --- | --- | --- | --- | --- |
| R-TC-A01 | No canonical mutation | Canonical project snapshot S1 exists | Run Reasoning (Canonical) | **No canonical diffs**; outputs exist only in reasoning store | I-01 |
| R-TC-A02 | No decisions in outputs | Any valid snapshot S1 | Run Reasoning | No “should/need/recommend”; no severity/priority fields | I-02 |
| R-TC-A03 | No communication generation | Any valid snapshot S1 | Run Reasoning | Outputs are machine objects only (Issue/Inferred/Signal/Evidence) | I-03 |
| R-TC-A04 | No layer substitution | Any valid snapshot S1 | Run Reasoning | No scoring fields; no governance fields; no action execution fields | I-15 |
| R-TC-A05 | Structural truth only | Same structure; change only “preference” metadata (non-structural) | Run Reasoning twice | Identical outputs (hash match) | I-04 |

---

## **B. Determinism and replayability**

| **TC ID** | **Scenario** | **Setup** | **Action** | **Expected Result** | **Invariants** |
| --- | --- | --- | --- | --- | --- |
| R-TC-B01 | Determinism same inputs | Snapshot S1 + rule versions R1 pinned | Run twice | Outputs identical (stable IDs or stable hash) | I-06 |
| R-TC-B02 | Determinism scoped to rule version | Snapshot S1; run with R1 then R2 | Run twice with different rule versions | Outputs may differ; evidence chain records correct rule versions | I-06, I-09 |
| R-TC-B03 | Replay reconstructs outputs | Persist run artifacts (snapshots + rules + outputs) | Replay run | Replay reproduces identical outputs and evidence hashes | I-07 |
| R-TC-B04 | Evidence immutability | Existing evidence chain E1 | Attempt to modify E1 | Write rejected / immutable; new chain required | I-09 |

---

## **C. Evidence chain completeness**

| **TC ID** | **Scenario** | **Setup** | **Action** | **Expected Result** | **Invariants** |
| --- | --- | --- | --- | --- | --- |
| R-TC-C01 | Every issue has evidence | Create known gap scenario | Run Reasoning | Every Issue has evidence_chain_id referencing an immutable chain | I-08 |
| R-TC-C02 | Every inferred element has evidence | Scenario requiring structural completion | Run Reasoning | Every InferredElement references evidence chain | I-08 |
| R-TC-C03 | Every signal has evidence | Scenario producing at least 1 signal | Run Reasoning | Every StructuralSignal references evidence chain | I-08 |
| R-TC-C04 | Evidence contains limitations when incomplete | Missing required artifact/relationship | Run Reasoning | EvidenceChain.limitations populated; no fabrication to proceed | I-14, I-09 |
| R-TC-C05 | Evidence records assumptions explicitly | Scenario that triggers bounded assumption | Run Reasoning | EvidenceChain.assumptions_made includes the assumption(s) | I-12 |

---

## **D. Multi-pass behavior correctness**

| **TC ID** | **Scenario** | **Setup** | **Action** | **Expected Result** | **Invariants** |
| --- | --- | --- | --- | --- | --- |
| R-TC-D01 | Pass 1 has no inference | Any snapshot | Execute Pass 1 only (or inspect Pass 1 outputs) | No inferred elements; no synthetic placeholders | I-10 |
| R-TC-D02 | Pass 2 introduces placeholders only when required | Provide partial structure that blocks evaluation | Run full passes | Placeholders appear **only** for required missing structure; all are labeled | I-10, I-11 |
| R-TC-D03 | Pass 3 emits issues/signals | Provide scenario with known conflict | Run Pass 3 | Issues and signals emitted; all evidence-backed | I-08 |
| R-TC-D04 | Pass 4 incremental recompute | Make a governed canonical change affecting one subgraph | Run incremental recompute | Only impacted outputs superseded/updated; unaffected outputs stable | I-06 |

---

## **E. Inferred elements and placeholder rules**

| **TC ID** | **Scenario** | **Setup** | **Action** | **Expected Result** | **Invariants** |
| --- | --- | --- | --- | --- | --- |
| R-TC-E01 | Derived vs Synthetic classification | Scenario with computable derived value + missing value requiring placeholder | Run Reasoning | Derived has no invented content; SyntheticPlaceholder is explicitly labeled | I-10 |
| R-TC-E02 | Synthetic defaults Low certainty | Scenario requiring SyntheticPlaceholder | Run Reasoning | SyntheticPlaceholder certainty_band = Low | I-11 |
| R-TC-E03 | Synthetic never promoted | Any run producing synthetic placeholder | Run Reasoning | No output marks synthetic as canonical/factual; epistemic_state remains Proposed | I-11 |
| R-TC-E04 | Derived never downgrades to synthetic | Same snapshot; change irrelevant fields | Run twice | Derived stays Derived across runs if inputs unchanged | I-10 |
| R-TC-E05 | No hidden assumptions in inference | Scenario requiring heuristic | Run Reasoning | heuristic_used and assumptions are recorded; nothing implicit | I-12 |

---

## **F. Hypothetical isolation and containment**

| **TC ID** | **Scenario** | **Setup** | **Action** | **Expected Result** | **Invariants** |
| --- | --- | --- | --- | --- | --- |
| R-TC-F01 | Hypothetical outputs tagged | Create Hypothetical context run | Run Reasoning with mode=Hypothetical | All outputs tagged with context; separated run lineage | I-13 |
| R-TC-F02 | No cross-contamination | Run Hypothetical then Canonical on same project | Compare outputs | Canonical run does not include hypothetical inferred values or edges | I-13 |
| R-TC-F03 | Hypothetical cannot write canon | Hypothetical run | Attempt to persist to Knowledge | No canonical diffs; blocked by contract | I-01, I-13 |

---

## **G. Structural truth constraints (no invented goals/outcomes/intent)**

| **TC ID** | **Scenario** | **Setup** | **Action** | **Expected Result** | **Invariants** |
| --- | --- | --- | --- | --- | --- |
| R-TC-G01 | No invented goals/outcomes | Snapshot missing outcomes | Run Reasoning | Does **not** invent outcomes; records limitation and/or gap issue | I-05, I-14 |
| R-TC-G02 | No intent simulation | Add “desired strategy” text in notes | Run Reasoning | No new strategies inferred; outputs unchanged unless structure changed | I-04 |
| R-TC-G03 | Canon-only referencing | Snapshot includes outcomes O1..On | Run Reasoning | Any references resolve to canonical IDs; no phantom references | I-05 |

---

## **H. Failure-mode and partial-output safety**

| **TC ID** | **Scenario** | **Setup** | **Action** | **Expected Result** | **Invariants** |
| --- | --- | --- | --- | --- | --- |
| R-TC-H01 | Missing critical artifact | Remove a required artifact (e.g., no outcomes) | Run Reasoning | Emits partial signals (if possible), limitations recorded; no fabricated constraints | I-14 |
| R-TC-H02 | Conflicting constraints | Add mutually exclusive constraints | Run Reasoning | Emits conflict issue with evidence chain; no “best choice” suggestion | I-02, I-08 |
| R-TC-H03 | Unparseable input field | Corrupt one field | Run Reasoning | Records limitation/error; does not hallucinate substitute values | I-14 |
| R-TC-H04 | Extreme input size | Large graph snapshot | Run Reasoning | Completes or fails safely with limitations; never drops evidence requirements | I-08, I-14 |

---

## **I. Supersession and audit lineage**

| **TC ID** | **Scenario** | **Setup** | **Action** | **Expected Result** | **Invariants** |
| --- | --- | --- | --- | --- | --- |
| R-TC-I01 | Supersede, don’t delete | Run R1 then recompute to R2 | Run Reasoning recompute | Prior outputs remain; R2 outputs supersede R1 outputs; replay still works | I-07, I-09 |
| R-TC-I02 | Snapshot pinning | Run against snapshot S1; later canon changes create S2 | Replay R1 | Replay uses S1 only; unaffected by S2 | I-07 |
| R-TC-I03 | Rule pinning | Run uses rule version R1 | Replay later after rules updated | Replay still uses R1; rule version stored in evidence | I-07, I-09 |

---

## **Minimum CI Gate**

A build is **Reasoning-compliant** only if these pass at minimum:

- A01, A02, A03
- B01, B03
- C01–C03
- E02, E03
- F02
- G01
- H01
- I02, I03

---

If you want, I can turn this into a **starter Gherkin suite** grouped exactly by sections **A–I**, with feature files named like A_boundaries.feature, B_determinism.feature, etc., and step wording compatible with CI.