# Release 1 — Build / Test / Observe Traceability Matrix

**Status:** Authoritative coverage map (capability → contract → test → observability) · **Date:** 2026-06-04
**Purpose:** the **checkable** artifact behind the §E+ traceability gate. Every Release-1 **cognitive** capability maps to an owning contract, an acceptance basis (test), and an observability event. The team/LLM builds **to the contract**, verifies **against the test column**, and confirms coverage here — **no inference about what a capability "should" do.** Commodity/platform capabilities (DL-043 J) are listed as such and are **not** cognition-contracted.

> If a capability you're building is not in this matrix, that is a **coverage defect** — STOP and escalate (per `ANTI_ASSUMPTION_BUILD_PROTOCOL.md`). Contract files are under `03_architecture/contracts/`.

## Legend
- **Contract:** owning contract id / package. **Test basis:** the QA obligation to satisfy (positive **and** negative). **Observe:** the event(s) that must emit. **Phase:** implementation phase.

## Cognitive capabilities (contracted)

| Cap | Capability | Contract (package · id) | Test basis | Observe | Phase |
|---|---|---|---|---|---|
| EI-01 | Artifact Ingestion | WAVE_A_001 · IC-WA-001 | admit≠canonical; provenance; idempotency; **no cognition in Perceive** (neg) | Artifact Admitted | II |
| EI-02 | Claim Extraction | **WAVE_S · IC-WS-SYNTH** (Perceive) | source-attributed assertions; **no unattributed fact** (neg) | Claim Extracted | II/III |
| PS-01 | Planning Synthesis Engine | **WAVE_S · IC-WS-SYNTH** (Infer) | model built from Attested; assumptions flagged (neg: silent gap-fill) | Synthesized Model Updated | III |
| PS-02 | Planning Artifact Generation | **WAVE_S · IC-WS-SYNTH** (Infer) | artifacts **Derived**; CHR per gen; **neg: Attested-as-truth / autonomous write** | Planning Artifact Generated/Regenerated | III |
| PS-03 | Understanding Evaluation (seed) | WAVE_S → WAVE_B · IC-WB-EVAL | Evaluate seeds CAF/Confidence from model | Issue/CAF/OutcomeConfidence events | III |
| PS-04 | Artifact Lifecycle (versioning) | WAVE_A_002 · IC-WA-002 (store) | append-only versions; supersession traceable | Version Recorded | II |
| AE-01 | Fast Pass | WAVE_B · IC/QA-WB (DL-046) | **Time-to-First-MRI < 60s** (perf gate); orientation outputs | events carry `mode=fast` | III |
| AE-02 | Deep Pass | WAVE_B · IC/QA-WB (DL-046) | async expansion; **neg: Deep blocks user** | `mode=deep` + completion-time | III |
| AE-03 | Event-Driven Recompute | WAVE_A_00R · IC-WA-00R | only info-change recomputes; coalesced; last-known-good | Recompute Triggered | II |
| AE-04 | Understanding State Model | WAVE_B (DL-047) | Initial→…→Mature attribute; change only via recompute | Understanding State Changed | III |
| AE-05 | Progressive Disclosure | WAVE_E (DL-047) | progressive present; never Unknown→Final-Truth (neg) | (presentation) | VI |
| CAF-01…05 | CAF Engine / Clarity / Alignment / Feasibility / taxonomy | WAVE_B · IC-WB-EVAL | CAF assessed; Derived; recompute-appends | CAF Assessed | III |
| CONF-01…04 | Outcome Confidence / score+states / explainability / history | WAVE_B · IC-WB-EVAL | confidence=understanding (neg: as health); band-edge guard | Outcome Confidence Computed | III |
| CONF-05 | Progressive Confidence Stages | WAVE_B (DL-046) | Orientation→Expanded→Validated | confidence_stage on emission | III |
| CONF-06 | False-Confidence Detection | WAVE_B (DL-047) | **neg: high confidence on weak understanding unflagged** | False-Confidence Flagged | III |
| MRI-01/02/03 | MRI generation / components / states | WAVE_E · IC-WE-DISCLOSE | presents governed objects; epistemic labels | MRI surface events | VI |
| MRI-04/05/06/07 | Heatmap / CAF Triangle / Timeline / Dependencies | WAVE_E (DL-047) | each sub-component present; traces to UX spec | (presentation) | VI |
| ISS-01…04 | Issue engine / severity / lifecycle / linkage | WAVE_B · IC-WB-EVAL | Issue from Finding; severity; append-only | Issue Generated | III |
| REC-01/02/03 | Recommendation engine / actions / lifecycle | WAVE_C · IC-WC-ADVISE | only-in-Finding-context; never accepts/executes (neg) | Recommendation Emitted | IV |
| REC-04 | Suggested Fixes | WAVE_C (DL-047) | suggest only; **neg: autonomous artifact write** | Suggested Fix Offered | IV |
| REC-05 | Validation Recommendations | WAVE_C (DL-047) | Validation type; routes to CRR on user action | Recommendation Emitted (Validation) | IV |
| OVL-01/02/03 | CAF Overlay engine / panel / actions | WAVE_E · IC-WE-DISCLOSE | overlay maps to CAF; in-context | (presentation) | VI |
| CHAT-01…04 | OSLO Chat (+context/functions/improvements) | WAVE_E (DL-047) | **neg: writes canonical / mutates artifact / changes assessment** | Chat Exchange | VI |
| CRR-01…05 | CAF Review Requests | WAVE_A_001 (DL-047 seam) + Wave E status; **workflow UI = commodity** | response→evidence→Deep Pass; **neg: response-as-truth** | Stakeholder Response Submitted | II/VI |
| AW-04/05 | Assisted Editing / Persistent Intelligence | WAVE_E (DL-047) | always-visible Confidence/CAF/state; routes to Chat/Fix | (presentation) | VI |
| (User Acceptance) | Accept + plan fact + Acceptance-Impact | WAVE_U · IC-WU-ACCEPT | user-attested; version-pinned; **neg: self-accept / overwrite** | Acceptance-Impact Assessed | V |

## Commodity / platform (NOT cognition-contracted — DL-043 J; build with normal engineering)
`PF-01/02/03/05` (alpha access, project init/lifecycle, pre-account) · `AW-01/02/03/06/07` (workspace, views, direct editing, panels, navigation) · `COLLAB` · `SHARE` · `TEL-01…07` (product telemetry) · `MON-01…04` (tiering/limits) · `SEC-01…07` (auth/RBAC/isolation/encryption/secrets/audit/privacy) · `PLAT-01…06` (persistence, orchestration, trigger efficiency, compute/token, perf arch, data model) · the **CRR workflow UI**.

## Deferred (NOT Release 1)
`AE-06` Understanding Debt (Future) · `CONF-07` Operational Confidence (Future).

---
*This matrix is the checkable coverage artifact mapping every Release-1 cognitive capability to its owning contract, its positive-and-negative acceptance basis, the observability event it must emit, and its implementation phase — so the external team/LLM builds to the contract and verifies coverage deterministically rather than inferring behavior. It marks the commodity/platform capabilities that are intentionally not cognition-contracted (DL-043 J) and the deferred non-Release-1 capabilities, and instructs that any capability missing from the matrix is a coverage defect to escalate, not a gap to fill by assumption.*
