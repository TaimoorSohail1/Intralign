# Release 1 — Acceptance-Criteria Coverage Reconciliation 001 (KIA2-4)

**Document Type:** AC coverage reconciliation (closes Capability-Matrix gap #11) · **Status:** Complete · **Date:** 2026-06-05
**Resolves:** `OSLO_CAPABILITY_MATRIX_V2.md` gap #11 — *"AC coverage is partial; 39 of 97 capabilities carry no AC reference."*
**Method:** map every capability category to **where its acceptance basis actually lives** — using evidence, not invention. (Per the Anti-Assumption Protocol, AC is **not fabricated**; it is *located* in the contracts/matrix or classified as commodity/normal-engineering, with genuine residuals flagged.)

---

## 0. Why #11 reads worse than reality

Gap #11 counted **only the §16 capability-matrix AC column.** Since that audit, the acceptance bases were authored **elsewhere** and now exist:
- **Wave QA contracts** (`QA-WB/WC/WU/WE/WS/WI`) — positive **and** negative acceptance per cognitive capability (10 contract files).
- **`RELEASE_1_BUILD_TEST_OBSERVE_TRACEABILITY_MATRIX.md`** — a **Test-basis column for every cognitive capability** (21 capability groups).
- **This session's additions** — DL-048 QA gate (cost), Seam-Audit limit-reached QA (MON), the Observability & Economics Platform spec (TEL), Deployment Governance gates (SEC), the Internal-bypass QA.

So the AC mostly **exists and is discoverable**; #11 is a *cross-reference* gap, not an *absence*. Commodity capabilities (DL-043 J) intentionally carry **no cognition-contracted AC** — that is **correct, not a defect** (the KIA2-5 principle: an intentional non-contract is an integrity strength).

## 1. Coverage map — every category → acceptance basis

| # | Category | Class | Acceptance basis (evidence) |
|---|---|---|---|
| 1 | **PF** Project Foundation | commodity (F) | normal engineering (DL-043 J); PS-04 lifecycle → Wave A-002 QA |
| 2 | **EI** Evidence Ingestion | cognitive | Wave A-001 + **Wave S QA** (`QA-WS-SYNTH`); matrix EI-01/02 |
| 3 | **PS** Planning Synthesis | cognitive | **Wave S QA**; matrix PS-01…04 |
| 4 | **AE** Analysis Engine (Fast/Deep) | cognitive | **Wave B QA** (DL-046 60s gate); matrix AE-01…05 |
| 5 | **CAF** | cognitive | **Wave B `QA-WB-EVAL`**; matrix CAF-01…05. *Numeric scoring formula = TBD-by-design (Open-TBD F1) → structural AC present, numeric AC deferred.* |
| 6 | **CONF** Confidence | cognitive | **Wave B `QA-WB-EVAL`**; matrix CONF-01…06 (incl. false-confidence). *Aggregation formula = F1 TBD-by-design.* |
| 7 | **MRI** | cognitive (Disclose) | **Wave E QA**; matrix MRI-01…07 |
| 8 | **ISS** Issues | cognitive | **Wave B QA**; matrix ISS-01…04 |
| 9 | **REC** Recommendations | cognitive | **Wave C + Wave I QA**; matrix REC-01…05 |
| 10 | **OVL** CAF Overlays | cognitive (Disclose) | **Wave E QA**; matrix OVL-01…03 |
| 11 | **AW** Artifact Workspace | mixed | AW-01/02/03/06/07 commodity (normal eng); **AW-04/05 → Wave E QA** + matrix |
| 12 | **CHAT** OSLO Chat | cognitive seam | **Wave I `QA-WI-INTERACT`**; matrix CHAT-01…04 |
| 13 | **COLLAB** | commodity | normal eng; COLLAB→AE-03 recompute is contracted (Wave A 00R QA) |
| 14 | **CRR** Review Requests | split | **Wave A/I QA** (response→evidence→Deep-Pass seam); workflow UI commodity |
| 15 | **SHARE** | commodity | normal eng + **SEC**; link-hygiene (P7) + attribution (P1) acceptance recorded |
| 16 | **TEL** Telemetry | commodity (F) | **`OSLO_RELEASE_1_OBSERVABILITY_AND_ECONOMICS_PLATFORM_SPECIFICATION_V1`** (events + `AI Spend Recorded` QA) + normal eng. *(was #11's gap — now covered)* |
| 17 | **MON** Monetization | commodity (C) | normal eng + **Seam-Audit limit-reached QA** + **DL-048 MON-COST QA gate** + upgrade-prompt criteria (freemium spec) |
| 18 | **SEC** Security & Compliance | commodity (E) | normal eng + **Deployment Governance gates** + **Internal-bypass QA** + the epistemic-invariant CI gate. *(was #11's gap — now covered)* |
| 19 | **PLAT** Platform Services | commodity (F) | normal eng + **Calibration Defaults** + Runtime Environment Constraint Profile. *(was #11's gap — now covered)* |

## 2. Genuine residuals (the only truly-open AC)

| Item | Status | Why it's not a defect |
|---|---|---|
| **CAF / Confidence numeric scoring AC** | **v0 FORMULA NOW PRESENT (2026-06-05)** → testable | `CAF_CONFIDENCE_V0_SCORING_FORMULA_V1.md` supplies the doctrine-compliant v0 (power-mean aggregation + baseline-minus-impact dims) **with its own §5 acceptance criteria** (no-findings→100; material weakness felt; exact replay; false-confidence flag; negatives: no static weights / not simple-average / not weakest-link / reliability-not-arithmetic / not-probability). The earlier "no formula to test against" gap is **closed**; only **parameter calibration** (`p`/`ε`/impact table) + canonical ratification remain owner-open. |
| **Numeric NFR acceptance** (latency, scale, etc.) | **owner-confirmed defaults** (Open-TBD A–E, 2026-06-05) | scaffolded with confirmed starting values; refine from telemetry. |

## 3. Resolution
- **Gap #11 is closed:** AC coverage = Wave QA contracts + the Build/Test/Observe Traceability Matrix (cognitive) + commodity normal-engineering (DL-043 J) + this session's specific QA (cost, limit-reached, telemetry, security, bypass). The only open AC is **formula-dependent numeric AC (F1, TBD-by-design)** — a legitimate deferral, not an absence.
- **KIA2-5 recorded:** a capability that is **intentionally commodity / not cognition-contracted** is **not an AC defect** — counting it as one understates real coverage. The traceability matrix is the canonical AC index for cognitive capabilities; the commodity list (matrix §"Commodity/platform") is the canonical "build-with-normal-engineering" set.

---
*This reconciliation closes Capability-Matrix gap #11 by demonstrating, with evidence, that the acceptance bases the original audit thought missing now exist — in the Wave QA contracts and the Build/Test/Observe Traceability Matrix for cognitive capabilities, and as intentional commodity/normal-engineering (DL-043 J) plus this session's specific QA additions (DL-048 cost gate, Seam-Audit limit-reached QA, the telemetry/economics spec, Deployment Governance and Internal-bypass security QA) for the Telemetry, Security, and Platform categories the audit flagged. It maps all nineteen capability categories to their acceptance basis, identifies the only genuinely-open AC as the formula-dependent CAF/Confidence numeric criteria (intentionally TBD-by-design pending calibration, Open-TBD F1) and the owner-confirmed numeric NFRs, and records the KIA2-5 principle that an intentional non-contract is an integrity strength rather than a coverage defect — without fabricating any acceptance criteria, per the Anti-Assumption Protocol.*

**Release 1 Acceptance-Criteria Coverage Reconciliation 001 complete.**
