# Backlog (DRAFT) — Formalize Fast/Deep Analysis Modes + 60s Target in the Ratified Contracts

**Status:** **Proposed · Pending Owner Ratification.** Raised at owner direction (owner is uncomfortable with the Fast/Deep behavior modes and the 60-second performance target being *implicit* at the contract layer). Per `CLAUDE.md`, only the owner ratifies; this routes a contract-level change to the owner rather than editing ratified contracts directly.

## The gap

**Fast Pass and Deep (Analysis) Pass are confirmed Release 1 scope** — `OSLO_CAPABILITY_MATRIX_V2` §4 (AE-01 Fast Pass *Critical*, AE-02 Deep Pass *Active Release 1*), the active `02_product/specs/FAST_DEEP_WORKFLOW_PACK/`, the Analysis Engine spec, and the Performance/NFR spec. The **< 60-second Time-to-First-MRI** is the **only owner-approved numeric target in the entire corpus** (Master Spec §20 / Canonical Scope M1).

**However, the ratified responsibility-organized contracts do not name them.** Verified: the Wave A–E contract packages, the Cognitive Responsibility Architecture spec, and the Runtime Object/Behavior models contain **no** explicit "Fast Pass / Deep Pass / extraction / expansion" obligations. The two-pass behavior was abstracted into Perceive → Infer → Evaluate over the 00R recompute backbone; the **Orientation State Model** survives in the Contract Inventory, but the **two-mode behavior and the 60s latency ceiling are not contracted acceptance criteria.**

**Risk:** an engineer (or autonomous agent) building from the wave contracts could implement the pipeline *correctly* yet **not** structure it as a fast 60-second orientation pass + a deep continuous-expansion pass, and could miss the 60s target — because the ratified contracts don't require it. (The implementation *phase plans* now state it explicitly — Phase II/III — but plans are non-canonical; the **contracts** are the authoritative build spec.)

## Proposed change (owner to ratify)

Add **explicit, contracted obligations** so Fast/Deep + 60s are required, not inferred:

- **(A) `IC-WB-INFER` / `IC-WB-EVAL` (Analysis Engine, Wave B)** — add required behavior: the analysis engine operates in **two modes** — **Fast Pass** (latency-bound; produces Orientation Confidence + initial MRI/findings) and **Deep Pass** (async, event-triggered, continuous expansion: Confidence Recalculation, Expanded Findings/Recommendations) — with **progressive confidence stages** (Orientation → Expanded → Validated).
- **(B) `QA-WB-*`** — add acceptance: positive tests assert both modes exist and produce the specified outputs; a **performance test asserts Time-to-First-MRI < 60s** on the supported project-size envelope; negative test rejects "Deep Pass blocks the user / Fast Pass exceeds the 60s ceiling."
- **(C) `IC-WA-001` (Perceive) / `IC-WA-00R` (recompute)** — note explicitly that intake feeds the **Fast Pass** orientation and 00R is the **Deep Pass** continuous-expansion engine (coalesced; last-known-good; non-blocking to Fast).
- **(D) NFR** — adopt **Time-to-First-MRI < 60s** as a ratified Release 1 NFR acceptance gate (it is owner-approved per Master Spec §20/M1 but not yet a contract/QA obligation); enumerate the still-open `TBD – Owner Decision Required` items (p50/p95 distribution, supported-project-size envelope) from the Performance/NFR spec §20.

## Scope / governance notes

- Sources to fold in (all active): `RELEASE_1_ANALYSIS_ENGINE_SPECIFICATION_V1` · `FAST_DEEP_WORKFLOW_PACK/*` (Fast/Deep stage I/O, comparison, acceptance criteria, scope guardrails, traceability) · `RELEASE_1_PERFORMANCE_AND_NFR_SPECIFICATION_V1`.
- This is a **contract amendment**, so it follows the governance lifecycle (Proposal → Review → Decision → contract revision → changelog). It does **not** change architecture or introduce new responsibilities — Fast/Deep remain *modes* of the existing Perceive/Infer/Evaluate + recompute, surfaced by Disclose.
- The implementation phase plans (Phase II/III) have been updated to state Fast/Deep + 60s explicitly as an interim measure; **this backlog item makes it authoritative at the contract layer.**

## Owner decision required
- [ ] Approve formalizing Fast/Deep modes as explicit Wave B contract obligations (A).
- [ ] Approve the Fast/Deep + **60s performance** QA/acceptance criteria (B, D).
- [ ] Approve the Perceive/00R clarifications (C).
- [ ] On approval: route through the contract-revision lifecycle; record the changelog entry; (optionally) ratify the 60s NFR as a named Decision.

---
*This draft backlog item flags that Fast Pass, Deep Pass, and the owner-approved < 60-second Time-to-First-MRI target — all confirmed Release 1 scope at the product layer — are not explicit obligations in the ratified responsibility-organized contracts, and proposes adding them as contracted behavior + QA/NFR acceptance criteria. It is owner-directed, changes no architecture, and routes ratification to the owner; the implementation phase plans have been updated to state these explicitly in the interim.*
