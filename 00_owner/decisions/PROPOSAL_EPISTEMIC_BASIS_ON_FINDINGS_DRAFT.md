# Proposal (DRAFT v2) — Epistemic basis on Findings: a two-axis model (type + basis)

> **DRAFT for owner ratification.** AI-drafted under Framework 001A (analysis / consistency checking / conflict identification / recommendation only). The owner ratifies; AI does not author canon or resolve the ontology seam. Raised per the Anti-Assumption Build Protocol (escalate a spec gap, don't infer-and-fill). Owner directed this draft and steered the shape below (2026-07-02).
>
> **v2 supersedes v1.** v1 proposed a single flat "finding type" enumeration; a consistency check found that conflicts with the **ratified Gap/Conflict/Risk finding types** and conflated *inference* (an epistemic basis) with *type*. v2 adopts the **two-axis model** the owner selected.

- **Type:** Framework 001 — Proposal + 001A Review (five outputs) + recommended split (R1 presentation / R2 ontology).
- **Layer touched (R1):** `10_product/experience/FINDING_PRESENTATION_SPECIFICATION_V1` §C/§F + `FINDING_PANEL_SPECIFICATION_V1`. **No doctrine change. No object-model change in R1.**

---

## 1. Problem (owner observation)

Findings don't surface the epistemic language PMs think in — *inferred* vs *assumed* vs *stated*. A finding reads as a flat "issue," hiding OSLO's core value (honest, epistemically-typed understanding). This is most acute on clarity findings, which usually turn on exactly this distinction.

## 2. The model (owner-selected): two axes, not one

Canon already **separates content type from epistemic state** (Epistemic State Model: "separate content type — what a thing is about — from epistemic state — how grounded/settled it is"). A finding therefore carries **two** independent things:

- **Type** — *what the observation is.* The **ratified canonical set is Gap · Conflict · Risk** (Architecture Foundation M-3; Wave B contract "Finding types: Gap, Conflict, Risk Signal"), with finer kinds (Coverage gap, Missing information, **Assumption**, **Ambiguity**) beneath.
- **Basis** — *how grounded the finding is.* **Stated (Attested)** — anchored in something the plan states — vs **Inferred (Derived)** — OSLO's read of a not-yet-stated gap/assumption. This is the canonical Attested/Derived distinction applied at the finding level, and it is where **"inferred" belongs — not as a type.**

The user's ask maps onto **both**: `Assumption` (type) **·** `inferred`/`stated` (basis). "Inference" is *not* a peer of "Assumption" — every finding is Derived; the basis axis says whether its *anchor* is stated or inferred.

Guardrail that already holds: **type is "an input label, not a coefficient"** — severity comes from the Impact Assessment, never from type (Outcome-Confidence Calibration). So surfacing type/basis is **presentation-only** and cannot be read as driving severity.

## 3. Scope split (owner-selected)

**R1 — presentation, now (this proposal):**
1. **Amend `FINDING_PRESENTATION_SPECIFICATION_V1` §C** — the card carries **finding type** (affirming the existing required element) **and** a **basis** tag (`stated` / `inferred`).
2. **Amend §C/§F + `FINDING_PANEL_SPECIFICATION_V1`** — the finding panel states the basis in plain language, e.g. *"OSLO inferred this — it isn't stated in your inputs"* / *"Grounded in a stated item in your plan"* — discharging the Epistemic State Model **Disclose obligation** at the finding level (not only the coarse "From OSLO" Derived tag).
3. **Correct the mis-model** — "Inference" is dropped as a *type*; such findings are a **Gap** (or Conflict/Risk) with **basis = inferred**. (Realized in the prototype: `FND-2071` reclassified Coverage gap · inferred; baseline `03-findings` refreshed.)
4. **Labels (plain-language, DL-087 pattern; no glossary drift):** `stated` / `inferred` for basis; `Assumption`, `Ambiguity`, `Coverage gap`, `Missing information` for the finer type kinds; `Gap` / `Conflict` / `Risk` remain the canonical top level.

**R2 — ontology, deferred (do not do now):**
5. Formalize the **finer type kinds as sub-types of Gap/Conflict/Risk** in the Finding object model + Infer/Evaluate contracts (Assumption/Ambiguity/Coverage-gap/Missing-info nested; Conflict stays top-level). This is object-model surgery on a mid-build engine (Wave B/C merged, Wave U/#69 in flight) and deserves a deliberate pass, not a rushed edit.

## 4. Review (Framework 001A — five outputs)

**Findings.**
1. The two-axis split *is* canon (Epistemic State Model separates content type from epistemic state); this operationalizes it onto Findings.
2. R1 items 1–4 are **presentation-only** and largely *realize existing obligations* (§C already requires the type; the Disclose obligation already requires showing Derived) — low risk.
3. The only genuinely-new ontology work (sub-typing) is correctly deferred to R2.

**Concerns.**
1. **Basis-assignment rules** — *which* findings are `stated` vs `inferred` must be defined by Infer/Evaluate (the engine that anchors findings to Attested assertions), not guessed in the UI. R1 ships the *presentation*; the assignment contract is part of R2 (or a small Wave-B contract note). Until then the prototype's assignments are **illustrative**.
2. **Two tags = more chips** — mitigated by keeping both tags compact on the card and the full basis sentence in the panel (progressive disclosure).
3. **Terminology drift** — `inferred`/`stated`/`Assumption` must map to Derived/Attested/assumption-content-type, not become new glossary entries (label-map + Disambiguation Register note only).
4. **Scope discipline** — R1 changes no object, no doctrine, no severity mechanics.

**Dependencies.**
- `RELEASE_1_EPISTEMIC_STATE_MODEL_DECISION_001` (content-type vs epistemic-state; Disclose obligation) · Architecture Foundation M-3 + Wave B contract (Gap/Conflict/Risk) · `CANONICAL_GLOSSARY` (Attested/Derived; DL-087 labels) · `FINDING_PRESENTATION_SPECIFICATION_V1` §C/§F · `FINDING_PANEL_SPECIFICATION_V1` · Outcome-Confidence Calibration (type is a label, not a coefficient). R2 additionally: Finding object model + Wave B Infer/Evaluate contracts.

**Recommendation.**
**Accept the R1 presentation slice** (two-axis card + panel basis sentence; §C/§F + panel-spec amendments; keep the realized prototype). **Open an R2 backlog item** for the Gap/Conflict/Risk sub-typing + the basis-assignment contract. No new doctrine; no R1 object-model change.

**Status.**
**DRAFT — recommended: Accept (R1 presentation) + backlog (R2 ontology).** Owner ratification required (001A — AI may not ratify).

## 5. Decisions captured (owner steer, 2026-07-02) — confirm at ratification

1. **Model:** two axes — type + basis. ✔ (owner-selected)
2. **Ontology direction:** Assumption/Ambiguity/etc. become **sub-types of Gap/Conflict/Risk**; formalize in **R2**. ✔
3. **Granularity:** card = type + small basis tag; panel = full basis sentence. ✔
4. **Scope:** R1 presentation now; ontology reconciliation to R2. ✔

Residual owner confirmations: the exact basis-assignment authority (Infer vs Evaluate) and whether any finer kind other than {Assumption, Ambiguity, Coverage gap, Missing information} is needed for R1 labels.

## 6. If accepted — resulting actions

1. Owner ratifies via the Founder Console; number-at-merge (DL-065) as a DL amending `FINDING_PRESENTATION_SPECIFICATION_V1` §C/§F + `FINDING_PANEL_SPECIFICATION_V1`, plus a Disambiguation Register label-map note (stated/inferred → Attested/Derived).
2. Keep the realized prototype two-axis card (conformant); add the §F/panel basis sentence; refresh the finding-panel baseline if it changes.
3. Add a traceability row: finding type + basis → Disclose render → acceptance check (visual/behavioral gate).
4. Open **RB-0NN (R2):** Gap/Conflict/Risk sub-typing in the Finding object model + the basis-assignment contract (Infer/Evaluate).

## Provenance

Owner observation 2026-07-02 (Findings lack inferred/assumed language). AI surveyed canon (Epistemic State Model, glossary, Finding Presentation/Panel specs, Wave B contracts), found (a) the vocabulary + Disclose obligation already ratified, (b) the card non-conformant to §C — fixed, (c) a **conflict** between the draft's flat enumeration and the ratified Gap/Conflict/Risk types, and (d) inference conflated with type. Reworked to the owner-selected two-axis model and split R1-presentation / R2-ontology. Recommendation only; owner ratifies. Numbered at landing (DL-065).
