# DL-089 — Clarification flow contract (object-free; in-panel + chat — Option B)

- **Date:** 2026-07-02 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A (interface contract; R1 scope addition)

- **Source:** Owner scope decision 2026-07-01 (clarification in R1) + surface decision 2026-07-02 (Option B — Finding Panel). Contract: `00_owner/decisions/CLARIFICATION_CONTRACT_PACKAGE_DRAFT.md`; closes Integration-Map gap **G1**. Grounded in `OSLO_CHAT_AND_CLARIFICATION_EXPERIENCE_SPECIFICATION_V1` (Q3/Q9/§G), `WAVE_A_CONTRACT_PACKAGE_00R_RECOMPUTE_STALE_BACKBONE`, RELEASE_1 STATE/EVENT/API interfaces, DL-043.
- **Layer:** `20_handoff` interface amendments (Event + API) + `10_product/experience` Chat Q3 amendment. Non-doctrinal.

## Decision
Ratify the clarification flow as a **conformant, object-free information-capture path**: a clarification answer is a **project-information change** (like an artifact edit) that marks analysis stale and feeds the next reanalysis; it creates **no Clarification object/lifecycle** and mutates nothing by itself (only reanalysis changes assessment). Adds the event **`clarification_answer_captured`** and the command **`POST /projects/{pid}/clarification-answers`**. **Surface (Option B):** clarifications may be answered **in the Finding Panel** as well as in **Chat** (Chat remains the primary conversational home). *(Guardrails + mechanics per the contract package.)*

## Conditions
No modeled Clarification object/lifecycle/disposition (Chat spec §122); answering never mutates CAF/Reliability/Confidence or closes a finding without a run; clarification never blocks the user (advisory-only); Attested answer / Derived prompt (two-axis replay).

## Supersedes / Amends
Amends `20_handoff/interfaces/RELEASE_1_EVENT_MODEL_SPECIFICATION_V1.md` (+§14a `clarification_answer_captured`; + Deep-Analysis recompute trigger), `20_handoff/interfaces/API_CONTRACT_ENDPOINT_CATALOG.md` (+ clarification-answers command), and `10_product/experience/OSLO_CHAT_AND_CLARIFICATION_EXPERIENCE_SPECIFICATION_V1.md` Q3 (Option B — permit in-panel answering). Closes Integration-Map G1. Additive; no prior decision superseded.

## Provenance
AI checked canon first (found the ratified clarification model — no modeled object), drafted an object-free conformant contract riding the recompute-stale backbone, and escalated the surface conflict; owner chose **Option B** (Framework 001A). Owner ratifies; effect on canon at owner merge. Numbered at landing (DL-065).
