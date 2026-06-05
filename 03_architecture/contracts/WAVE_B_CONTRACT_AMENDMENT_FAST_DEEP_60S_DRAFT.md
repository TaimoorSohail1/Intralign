# Wave B Contract Amendment (DRAFT) — Fast/Deep Analysis Modes + <60s Time-to-First-MRI

**Status:** **Proposed · Pending Owner Ratification.** A reviewable amendment to the ratified `WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING.md` (+ small notes to `WAVE_A_CONTRACT_PACKAGE_001` / `00R`). Implements the owner-directed backlog item `01_governance/backlog/BACKLOG_FAST_DEEP_CONTRACT_FORMALIZATION_DRAFT.md`. **Adopts nothing; edits no ratified contract.** On ratification, the owner applies the additions below verbatim and records the changelog entry.

> **Design guardrail (preserved):** this adds **no new responsibility and no new object.** Fast/Deep are **modes** of the existing Infer+Evaluate over the 00R recompute backbone; **confidence stage** (Orientation/Expanded/Validated) and **analysis mode** (fast/deep) are **attributes on the emission**, not new entities. Consistent with DL-043, DL-044, and the Cognitive Responsibility architecture.

---

## A. Shared clause — add to §1/§2 orientation of the Wave B package

**ADD (new shared sub-section, e.g., §0.1 "Analysis Modes — REQUIRED"):**

> **Analysis Modes (required, not implicit).** Wave B analysis runs in two modes over the same Derived-cognition machinery:
> - **Fast Pass** — a **latency-bound** first pass that produces **Orientation-stage** Confidence plus an initial set of Findings/Issues sufficient for the first MRI, within the **Time-to-First-MRI < 60s** budget (the only owner-approved numeric target; Master Spec §20 / M1).
> - **Deep Pass** — an **async, event-triggered, coalesced** continuation that expands Findings/Recommendations, recalculates Confidence, and matures the confidence stage. **The user is never blocked on Deep Pass.**
>
> **Progressive confidence stage** is an emission attribute that matures **Orientation → Expanded → Validated**. **Mode** (`fast` | `deep`) and **confidence_stage** are carried on every emission and its Cognition History Record. No new object or responsibility is introduced.

## B. `IC-WB-INFER` (§1.1) — add one Required-behavior item

**ADD to "Required behavior":**

> (5) **operate under both modes** — produce orientation-sufficient Findings on the **Fast Pass**, and expanded/matured Findings on the **Deep Pass**; record `mode` and `confidence_stage` on each emission and its Cognition History Record.

## C. `IC-WB-EVAL` (§2.1) — add one Required-behavior item

**ADD to "Required behavior":**

> (5) **compute Confidence at the current confidence stage** — Fast Pass yields **Orientation-stage** confidence; Deep Pass matures it toward **Validated** via recompute; carry `mode` + `confidence_stage` on each emission. Stage maturation occurs **only via recompute** (no stage change outside recompute).

## D. `QA-WB-INFER` (§1.2) & `QA-WB-EVAL` (§2.2) — add positives, a performance test, and negatives

**ADD — Positive:**
> - Both modes exercised: Fast Pass produces orientation-sufficient outputs; Deep Pass expands/matures them; `confidence_stage` transitions **Orientation → Expanded → Validated** are observable and history-tracked.

**ADD — Performance (new, QA-WB-EVAL):**
> - **Performance gate:** a test asserts **Time-to-First-MRI < 60 s** on the supported-project-size envelope *(envelope value `TBD – Owner Decision Required`; p50/p95 distribution `TBD`)*. This is a **ratified NFR acceptance gate** (§F).

**ADD — Negative (impossible/rejected):**
> - **Deep Pass blocks the user** (orientation must not wait on deep expansion);
> - **Fast Pass exceeds the 60 s ceiling** on the supported envelope;
> - **`confidence_stage` regresses or changes without recompute**;
> - **`mode`/`confidence_stage` modeled as a new object/entity** (must be attributes only).

**ADD — Failure classification:** Fast-Pass 60 s breach = **Major** (capability gate); stage-change-without-recompute or stage-as-object = **Critical** (invariant breach).

## E. Observability — add to `OBS-WB-INFER` (§1.3) & `OBS-WB-EVAL` (§2.3)

**ADD:**
> - **Events** carry `mode` (`fast`|`deep`) and `confidence_stage`.
> - **Metrics:** Fast Pass emits **Time-to-First-MRI latency**; Deep Pass emits **completion-time** (coalesced).
> - **Drift/Trust:** Fast-Pass latency over budget, or a stage maturing without recompute, are **trust signals**; stage maturation across history is a **product feature** (the "understanding kept improving after orientation" capability).

## F. Notes to Wave A contracts (small clarifications)

- **`IC-WA-001` (Perceive / Artifact Intake):** add — *intake feeds the **Fast Pass** orientation; integrity-gated admission must not block the 60 s Time-to-First-MRI budget.*
- **`IC-WA-00R` (Recompute / Stale Backbone):** add — *00R is the **Deep Pass** engine: async, event-triggered, **coalesced**, last-known-good on failure; it must not block the Fast Pass.*

## G. NFR ratification (proposed)

Adopt **Time-to-First-MRI < 60 s** as a **ratified Release 1 NFR acceptance gate** (owner-approved per Master Spec §20 / M1; today it is approved but not a contract/QA obligation). Carry forward the open `TBD – Owner Decision Required` items from `RELEASE_1_PERFORMANCE_AND_NFR_SPECIFICATION_V1` §20: p50/p95 distribution within the ceiling, and the supported-project-size envelope for which the 60 s target holds. *(Optionally record as a short named Decision so the only owner-approved numeric target is itself ratified scope.)*

---

## Conformance impact (for the re-review on ratification)

- **No architecture/object/responsibility change** — modes + stage are attributes; Infer/Evaluate ownership unchanged; 00R unchanged in role.
- **Re-run** the Wave B section of `WAVE_CONTRACT_PACKAGES_CONFORMANCE_REVIEW_001` §1 after applying, to confirm CONFORMANT with the added clauses (expected: clean; the additions tighten, not redefine).
- **Update** `RELEASE_1_CONTRACT_INVENTORY_V1` to note the mode/stage attributes and the 60 s NFR gate.

## Owner decision required
- [ ] Apply A–E to `WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING.md`.
- [ ] Apply F to `WAVE_A_CONTRACT_PACKAGE_001` + `…_00R`.
- [ ] Ratify G (60 s NFR gate); decide whether to record it as a named Decision.
- [ ] On ratification: re-run Wave B conformance §1; update Contract Inventory; record changelog (CHG-NNN); retire the backlog draft.

---
*This draft amendment formalizes the Fast Pass and Deep Pass analysis modes and the owner-approved < 60-second Time-to-First-MRI target as explicit obligations in the ratified Wave B contracts (with small clarifying notes to the Wave A intake and recompute contracts), expressed as required behavior, positive/negative QA including a performance gate, and observability — while introducing no new responsibility or object (mode and confidence-stage are emission attributes). It adopts nothing, edits no ratified contract, and routes ratification and application to the owner.*
