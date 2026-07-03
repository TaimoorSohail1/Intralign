# DL-093 — Finding type + epistemic basis presentation (two-axis; RB-033 Phase R1)

- **Date:** 2026-07-02 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

- **Source:** Owner ratification 2026-07-02 of **RB-033 Phase R1** (`00_owner/decisions/PROPOSAL_EPISTEMIC_BASIS_ON_FINDINGS_DRAFT.md`). Grounded in `RELEASE_1_EPISTEMIC_STATE_MODEL_DECISION_001` (content-type vs epistemic-state; Disclose obligation), Architecture Foundation M-3 + `WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING` (Gap/Conflict/Risk finding types), `FINDING_PRESENTATION_SPECIFICATION_V1` / `FINDING_PANEL_SPECIFICATION_V1`, `OUTCOME_CONFIDENCE_CALIBRATION_DECISION_001` (type is a label, not a coefficient), and DL-087 (plain-language labels).
- **Layer:** `10_product/experience` (Finding presentation). **Presentation-only; non-doctrinal.** No object-model, scoring, or contract change.

## Decision
Ratify the **two-axis presentation** of a Finding for Release 1:

1. **Type** (the §C required "Finding type") — *what the observation is*: the canonical **Gap / Conflict / Risk** family, shown with its finer user-facing kind (Coverage gap · Missing information · **Assumption** · **Ambiguity**). Type is a **label, not a coefficient**; severity is governed by the Impact Assessment, never by type.
2. **Basis** — *how grounded the finding is*: **stated (Attested)** vs **inferred (Derived)** — the canonical Attested/Derived distinction at the finding level. **"Inferred" is a basis, never a type.**
3. The **card** carries the type plus a compact **basis tag** (`stated` / `inferred`); the **finding detail / panel** names the basis in plain language ("OSLO inferred this — it isn't stated in your inputs" / "Grounded in a stated item in your plan"), discharging the Epistemic-State-Model **Disclose obligation** at the finding level (Derived surfaced *as* Derived).
4. Basis colour is **calm/neutral** — never the action/attention accent (reserved for clarification/action).

Realized in the reference prototype (`product-design/oslo_r1_experience_mockup_v2.html`, baseline `03-findings`). Amends `FINDING_PRESENTATION_SPECIFICATION_V1` (**new §P**; amends §O re: card content — the type now appears on the card), `FINDING_PANEL_SPECIFICATION_V1` (§E/§F), and the `CANONICAL_GLOSSARY` Disambiguation Register (stated/inferred → Attested/Derived label-map).

## Conditions
Presentation-only — no new object, scoring, ranking, or doctrine. **Gap / Conflict / Risk** remain the canonical type family; type never drives severity (Impact Assessment does). Attested/Derived and the Panel Model are unchanged. Basis colour never uses the action/attention accent. **Deferred to R2 (RB-033 Phase R2):** formal sub-typing of the finer kinds under Gap/Conflict/Risk in the Finding object model, and the **basis-assignment contract** (which of Infer/Evaluate sets a finding's Attested/Derived basis).

## Supersedes / Amends
Amends `FINDING_PRESENTATION_SPECIFICATION_V1` (§P; amends §O card-content statement), `FINDING_PANEL_SPECIFICATION_V1` (§E/§F), `CANONICAL_GLOSSARY` (Disambiguation Register label-map). Adopts **RB-033 Phase R1**; RB-033 Phase R2 remains Proposed. No canonical model, doctrine, or object superseded.

## Provenance
Owner observation 2026-07-02 (Findings lack inferred/assumed language). AI surveyed canon, fixed the §C card non-conformance, identified the conflict between a flat enumeration and the ratified Gap/Conflict/Risk types, and proposed the owner-selected two-axis model (RB-033). Owner ratifies the R1 presentation slice; R2 ontology reconciliation tracked. Presentation-only; effect on canon at owner merge. Numbered at landing (DL-065).
