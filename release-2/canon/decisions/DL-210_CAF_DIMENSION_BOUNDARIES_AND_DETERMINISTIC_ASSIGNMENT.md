# DL-210 — CAF dimension boundaries + deterministic, structural-target dimension assignment (with the escalation model)

- **Date:** 2026-08-09 · **Status:** Ratified · **Decided by:** Idris (Founder Console) · **Class:** A (doctrine — amends founder-approved CAF positions) with a B (realization) that extends DL-209 / Slice 10.
- **Framework 001** — AI drafts; only the owner ratifies.
- **Basis:** R&D working session 2026-08-09 (continuation of the DL-209 thread). Chain: **RB-044** → Proposal (`release-2/GOVERNANCE_PROPOSAL_alignment-caf-boundaries-deterministic-assignment.md`) → Review (five outputs, in the proposal) → this Decision.
- **Extends / reconciles:** **DL-209** (load-bearing sensitivity + L3 classification; the escalate-on-new valve) · **DL-196** (all three pillars via the issue layer; the `dim`/`dims[]` space; the load-bearing discipline §3; the CARE-POINT filter §5) · **DL-197** (false-confidence type) · DL-184 / DL-193. **Bounded by:** DR-7 / DL-103.
- **Amends canon:** `10_product/domain/CAF_ASSESSMENT_MODEL_V1.md` — founder **Positions #10/#11**. Applies at R1 graduation; R2-isolated until then.
- **Placement:** staged in `release-2/`; folds into `main` at R1 graduation with the other R2-staged decisions. Authorizes no freemium-build change; realization extends Slice 10.

---

## Decision

### A. First principles (ratified as canon)

1. **CAF dimension boundary cut — distinct assessment-target questions, with precedence.**
   - **Clarity** — is the element understood clearly enough to be assessed at all? (unit: the element's definition; the precondition)
   - **Alignment** — do the relationships between clearly-understood elements cohere toward the outcome? (unit: the **edge**)
   - **Feasibility** — can clearly-understood, coherent elements actually be achieved in reality? (unit: the element/path vs constraints)
   - **Precedence: Clarity → Alignment → Feasibility.** A downstream concern caused by an upstream gap is deferred behind its cause, not raised independently.

2. **Alignment is relational, assessed top-down.** Evaluated over the plan's `serves` edges by traversing **from the outcome down to the lowest roots, along each element path**. Two outputs per path: **optimization** (aggregate alignment quality toward the outcome) and **misalignment/insufficiency** (a per-edge load-bearing gate). A **tangent** (an element on no outcome-rooted path) is a first-class alignment exposure. **Metric-mismatch** is one such bad edge, folded under Alignment.

3. **Dimension assignment is deterministic from the finding's STRUCTURAL TARGET — not its finding-type.** Structural target `{ definition → Clarity | edge → Alignment | achievability → Feasibility | truth-of-inference → Grounding | coverage → Adaptability }`. This preserves CAF Position #11 (type ≠ dimension) while making assignment a graph function. The only irreducible judgment is **quarantined at L0 extraction** ("what is this finding about?") and is never applied silently.

4. **The escalation valve — no edge is ever silently judged.** Where the structural target is ambiguous or unmapped, the engine **escalates** rather than forcing a class (DL-209 escalate-on-new, extended to target-classification).

5. **Decompose ⇄ multi-dimension, reconciled by layer.** A raw observation may bear on several dimensions (**CAF #2 preserved** — carried in `dims[]`); for **resolution** it decomposes into single-target issues, each with one primary `dim` (**DL-209 preserved**), ordered by precedence. Root-cause is expressed through precedence, not a separate judgment pass. Uses R2's existing `dim` + `dims[]` shape — no schema change.

### B. Architecture (ratified — realization extends Slice 10)

**L0** structural-target extraction (`definition|edge|achievability|truth|coverage` + graph location, extraction-confidence — the sole judgment) → **L1** deterministic sensitivity incl. the **top-down outcome→roots alignment traversal** (per-edge sensitivity scales with the stranded subtree; per-path optimization aggregate; tangent check) with the perturbation-endpoint table below → **L3** deterministic `dim`/`dims[]`/acts derived from the structural target (retires hand-set assignment; unmapped/ambiguous → escalate).

**Perturbation endpoints by structural target** (favorable ↔ adverse, bounded by *plausible* resolutions the evidence supports — not literal extremes):

| Target | Dimension | X⁺ | X⁻ |
|---|---|---|---|
| truth of an inference | Grounding | inferred value true | inferred value false |
| achievability vs constraints | Feasibility | constraint doesn't bind | constraint binds |
| definition | Clarity | resolves to supported favorable reading | resolves to supported adverse reading |
| **edge (serves-relationship)** | **Alignment** | **segment genuinely contributes to the outcome** | **segment is a non-contribution / off-tree** |
| coverage / checkpoint | Adaptability | on a shift, the plan adapts | on a shift, it can't |

### C. Escalation resolution lifecycle (ratified)

- **Runtime escalation (the plan is underspecified) → a user-facing issue.** Missing/ambiguous target identity → a **Clarity issue** (resolve by clarifying). Both elements clear but sufficiency is a judgment the plan doesn't settle → the **Alignment issue itself** (resolve by verify/decide on the edge). It runs the load-bearing gate (benign ambiguities rest on the map — DL-196 §3), lands in the worklist only if load-bearing, closes via act → reanalysis, and **cascades** (clarifying unlocks the blocked downstream assessment; the stranded-subtree collapses many downstream un-evaluable edges into one upstream clarify).
- **Model-gap escalation (OSLO's taxonomy has no mapping) → owner/governance + a leverage-gated known-unknown.** Routes to build/backlog via Framework 001 (resolved by the owner ratifying a new mapping). Surfaced to the user **only when its structural leverage puts it on a path to the outcome**, as an explicitly **unassessed** "noted — help me understand this" item (no dimension tag, no band color, distinct from graded issues) carrying a clarify affordance that both resolves it and graduates the taxonomy. Benign model gaps rest on the map.

### D. Integrity treatment of an unassessed load-bearing gap (ratified)

A load-bearing model gap **prevents a Sound claim** and marks the region **incomplete / under review** (pending marker) — you cannot honestly call a plan Sound with a load-bearing piece you couldn't evaluate (weakest-gate honesty applied to unknowns). It is **NOT** scored Fragile or penalized numerically — *unknown ≠ bad*. The ceiling is **localized and leverage-gated**, so benign gaps never drag the read down.

### E. Enforceable guards (the honesty firewall — extends DL-209's)

dimension derived from structural target, never hand-set or type-mapped · alignment is edge-keyed and its sensitivity references outcome-reachability (never a node-local score) · an ambiguous/unmapped target escalates (never default-classifies) · a runtime escalation generates a user clarify/verify issue, a model-gap routes to governance · a load-bearing model gap ceilings integrity as **incomplete**, never as Fragile · CAF #2 (independent, multi-dimension-capable) and #13 (flat taxonomy) preserved; DL-196 CARE-POINT filter intact.

## What this amends (explicit)

CAF Assessment Model §9 establishes affected dimensions "in judgment — not in formula" (Positions #10/#11). DL-210 **narrows** this: dimension assignment becomes **deterministic from the structural target**, with judgment quarantined to L0 extraction and **surfaced via escalation**, never applied silently. Impact Assessment's other three factors (Significance, Scope, Evidence Support) are realized as the deterministic sensitivity pipeline (DL-209 L1/L2). **Preserved:** Position #2 (independent dimensions; a finding may bear on several) and Position #13 (flat taxonomy).

## Doctrine preserved (unchanged)

Honesty-first — maturity read, never a forecast. `level ≠ trust` (DL-190). One accuracy bar; freemium gates capacity, never judgment quality (DR-7 / DL-103). Single-hue integrity; decomposability. The load-bearing discipline (DL-196 §3 / DL-197 §4). The three-pillar CARE-POINT separation (DL-196 §5).

## Open (deferred, non-blocking)

Target-classification is a relocated judgment (contained by the escalation valve, not eliminated) · early-maturity model gaps could sit as incomplete (mitigated by the clarify path + taxonomy-growth signal) · interaction-effect findings that don't factor cleanly escalate. None gates the build.

## Affected artifacts

`GOVERNANCE_PROPOSAL_alignment-caf-boundaries-deterministic-assignment.md` · `BACKLOG_RB-044_alignment-caf-boundaries.md` · **`slices/10-load-bearing-sensitivity-engine.md`** + `BUILD_SPEC_DL-209_load-bearing-sensitivity-engine.md` (extended) · `slices/09-…` §3 register (**GT-45…GT-50**) · `acceptance/README.md` · `DEMO_CONFIG_REGISTER.md` (leverage-gate + incompleteness-ceiling) · `R2_DECISION_INDEX_PHASE_A.md` + `R2_TO_MAIN_INTEGRATION_PLAN.md` (DL-210 row + staged Phase-B changelog + **CAF-model amendment** at graduation) · at graduation: `10_product/domain/CAF_ASSESSMENT_MODEL_V1.md` Positions #10/#11.

---

_AI-drafted (Framework 001); **ratified by the owner 2026-08-09**. Staged in `release-2`; folds into `main` at R1 graduation with the other R2-staged DLs._
