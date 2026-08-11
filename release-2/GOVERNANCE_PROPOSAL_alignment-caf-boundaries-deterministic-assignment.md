# Governance Proposal — CAF dimension boundaries + deterministic, structural-target dimension assignment (with the escalation model)

- **Status:** ✅ **RATIFIED 2026-08-09 by Idris → DL-210** (`canon/decisions/DL-210_CAF_DIMENSION_BOUNDARIES_AND_DETERMINISTIC_ASSIGNMENT.md`). This proposal is the review record behind that decision. AI drafts; the owner ratifies (Framework 001).
- **Class:** A (doctrine — it **amends founder-approved CAF positions #10/#11** and fixes the alignment/boundary criteria) with a B (realization) section that extends DL-209 / Slice 10.
- **Basis:** R&D working session 2026-08-09 (owner-directed critical design, continuation of the DL-209 thread). Chain: **RB-044** → this Proposal → Review (five outputs, below) → owner Decision (candidate **DL-210**).
- **Grounds in / consumes / reconciles:** `10_product/domain/CAF_ASSESSMENT_MODEL_V1.md` (founder Positions #2, #9, #10, #11) · **DL-196** (all three pillars resolve through the issue layer; the `dim`/`dims[]` space; the load-bearing discipline §3; the CARE-POINT pillar filter §5) · **DL-197** (false-confidence type) · **DL-209** (load-bearing sensitivity + L3 classification; the escalate-on-new valve) · DL-184 (graph schema) · DL-193 (exposure queue) · DR-7 / DL-103 (one accuracy bar).
- **Placement:** staged in `release-2/`; the CAF-model amendment folds into `main`/`10_product/domain` at R1 graduation (parity with the other R2-staged decisions). **R2-isolated until then.**
- **⚠️ What this amends (called out, not buried):** CAF Assessment Model §9 currently establishes each finding's affected dimensions "in judgment — not in formula" (Positions #10/#11). This proposal **narrows that**: dimension assignment becomes **deterministic from the finding's structural target in the graph**, with judgment quarantined to L0 extraction and surfaced (never hidden) wherever the target is ambiguous. Positions #2 (independent dimensions; a finding may bear on several) and #13 (flat taxonomy) are **preserved**.

---

## 1. Problem

DL-209 ratified a **pillar-agnostic** load-bearing test (two-sided integrity-sensitivity ≥ a calibrated threshold) but expressed it in grounding-native "true ↔ false" language and left the **Viability/CAF dimension endpoints implicit** — most importantly **Alignment**. Two gaps follow:

1. **An implicit criterion in a model built to kill implicit criteria.** If the Alignment/Feasibility/Clarity perturbation endpoints stay unstated, an implementer invents them ad hoc — the `primaryMove` disease in a new host. Alignment is the core Intralign concept; leaving it to inference is the worst place to be vague.
2. **An unreconciled tension with canonical CAF.** The CAF Assessment Model says finding-type does **not** determine dimension, a finding may bear on **several** dimensions, and affected dimensions are established in **Impact Assessment by judgment** (Positions #2/#10/#11). DL-209 says classification is **deterministic** and multi-aspect issues **decompose, never dual-class**. One of these has to give. This is an ontology conflict on the known R1↔R2 CAF-reconciliation seam and must be adjudicated by the owner, not resolved silently.

The owner has further established that **Alignment is relational** — it is a property of the *relationship between two elements*, assessed **top-down from the outcome down to the lowest supporting roots, along each element path** — and that the three CAF dimensions need **crisp scope boundaries** so each reinforces its own scope without double-counting.

## 2. First principles (the doctrine to ratify)

1. **The CAF dimension boundary cut — each dimension owns a distinct assessment-target question.**
   - **Clarity** — *is this element understood clearly enough to be assessed at all?* Unit: the element's own definition. The precondition.
   - **Alignment** — *do the relationships between clearly-understood elements cohere toward the outcome?* Unit: the **edge** (element → … → outcome).
   - **Feasibility** — *can clearly-understood, coherent elements actually be achieved in reality?* Unit: the element/path against real constraints.
   - **Precedence: Clarity → Alignment → Feasibility.** You cannot assess the alignment of something undefined, nor the feasibility of something incoherent. Precedence is how a downstream concern caused by an upstream gap is handled — deferred behind its cause, not raised as an independent issue.

2. **Alignment is relational and assessed top-down.** Alignment is evaluated over the plan's `serves` edges by traversing **from the outcome down to the lowest roots, along each element path**. Two outputs per path: **optimization** (an aggregate of how well-aligned the whole path is toward the outcome) and **misalignment/insufficiency** (a per-edge gate — is any edge too weakly aligned to carry the outcome). A **tangent** — an element not reachable on any outcome-rooted path — is a first-class alignment exposure (effort serving nothing above it). **Metric-mismatch** is one such bad edge (a metric→outcome relationship that doesn't track), folded under Alignment.

3. **Dimension assignment is deterministic from the structural target — not from the finding-type.** The failure mode DL-209 must avoid is a *finding-type → dimension* map, which canon Position #11 rightly forbids (the same type lands on different dimensions by content: an "Assumption" is Feasibility for a vendor date, Clarity for a term, Alignment for a purpose). The deterministic input is instead the finding's **structural target in the graph**: attaches to an element's *definition* → Clarity; to an *edge* → Alignment; to *achievability vs constraints* → Feasibility (and, at the pillar level: *truth of an inference* → Grounding; *coverage/checkpoint* → Adaptability). This is deterministic and decomposable, yet preserves "type ≠ dimension." **The only irreducible judgment is quarantined at L0** — deciding what a finding is *about* — and is never applied silently downstream.

4. **The escalation valve — no edge is ever silently judged.** Where the structural target is ambiguous or unmapped, the engine **escalates** rather than forcing a class (the DL-209 escalate-on-new valve, extended to target-classification). Determinism where the graph is crisp; escalation where it isn't.

5. **Decompose ⇄ multi-dimension, reconciled by layer.** A raw observation may bear on multiple dimensions (**canon Position #2 preserved** — carried in the issue's existing `dims[]` set). For **resolution**, it **decomposes into single-target issues**, each with a single primary `dim` (**DL-209 preserved**), ordered by the Clarity→Alignment→Feasibility precedence. Root-cause is expressed through precedence, not a separate judgment pass. R2's issue shape already carries both `dim` (primary) and `dims[]` (all affected), so this needs no new schema.

## 3. Architecture (the realization — extends DL-209 / Slice 10)

**Quarantine the fuzziness (unchanged from DL-209):** only L0 extraction is probabilistic; L1–L3 are deterministic and decomposable.

- **L0 — structural-target extraction.** Each finding is tagged with its structural target `{ definition | edge | achievability | truth | coverage }` plus its graph location, each with an extraction-confidence. This is the sole judgment and the honest floor.
- **L1 — sensitivity, incl. the alignment traversal.** For alignment: traverse `serves` edges **top-down outcome → roots**; per-edge sensitivity scales with the **stranded subtree** (a weak edge high in the tree strands everything beneath it → high sensitivity; a weak leaf edge → low, rests on the map); per-path **optimization** is the aggregate; the **tangent check** flags off-tree elements. For the node-local dimensions, the two-sided counterfactual span of DL-209.

  **Perturbation endpoints by structural target** (the previously-implicit table, now explicit — favorable ↔ adverse, bounded by *plausible* resolutions the evidence supports, not literal extremes, to avoid span inflation):

  | Target | Dimension | Favorable (X⁺) | Adverse (X⁻) |
  |---|---|---|---|
  | truth of an inference | Grounding | inferred value is true | inferred value is false |
  | achievability vs constraints | Feasibility (Viability) | constraint doesn't bind | constraint binds |
  | definition | Clarity (Viability) | ambiguity resolves to the supported favorable reading | resolves to the supported adverse reading |
  | **edge (serves-relationship)** | **Alignment (Viability)** | **the segment genuinely contributes to the outcome** | **the segment is a non-contribution / off-tree** |
  | coverage / checkpoint | Adaptability | on a shift, the plan adapts | on a shift, it can't |

- **L3 — deterministic dim/dims + acts.** The issue's `dim` (primary) and `dims[]` (all affected) and its resolution act are **derived** from the structural target, retiring any hand-set assignment. Multi-target observation → decomposed single-`dim` issues by precedence. **Unmapped/ambiguous target → escalate.**

- **Escalation resolution lifecycle (the process by which escalations resolve):**
  - **Runtime escalation (the *plan* is underspecified) → a user-facing issue.** If the target identity is missing/ambiguous → a **Clarity issue** ("I can't assess whether X supports Y until you clarify what X is for"), resolved by the user **clarifying**. If both elements are clear but whether one *sufficiently* supports the other is a judgment the plan doesn't settle → the **Alignment issue itself**, resolved by the user **verify/decide** on that edge. Either way it is a normal issue: it passes the **load-bearing gate** (benign ambiguities rest on the map — DL-196 §3), lands in the worklist only if load-bearing, and closes via the standard act → reanalysis loop. Clarifying often **cascades** — it unlocks a deterministic downstream assessment that was blocked, and a genuine misalignment underneath then surfaces as its own fix/decide issue (the precedence order, dynamically). The **stranded-subtree** logic collapses many downstream un-evaluable edges into a single upstream clarify.
  - **Model-gap escalation (OSLO's *own taxonomy* has no mapping) → owner/governance + a leverage-gated known-unknown.** It routes to the build/backlog via Framework 001 (resolved by the owner ratifying a new mapping). For the **user**, it is surfaced **only when its structural leverage puts it on a path to the outcome** (leverage is graph-computable even when classification isn't), as an explicitly **unassessed** "noted — help me understand this" item: **no dimension tag, no band color, distinct from graded issues**, carrying a clarify affordance that both lets the user resolve it and produces the labeled example that graduates the taxonomy. Benign model gaps rest on the map.

- **Integrity treatment of an unassessed load-bearing gap — an incompleteness ceiling, not a score.** A load-bearing model gap **prevents a Sound claim** and marks that region **incomplete / under review** (with the pending marker), because you cannot honestly call a plan Sound with a load-bearing piece you couldn't evaluate (weakest-gate honesty applied to unknowns). It is **not** scored Fragile or penalized numerically — *unknown ≠ bad*; scoring an unknown as a failure would be its own dishonesty. The ceiling is **localized and leverage-gated**, so benign gaps never drag the read down.

## 4. Named residuals (boundaries, written down — not buried)

- **Target-classification is itself a relocated judgment.** Determinism doesn't remove judgment; it moves it to L0 extraction ("what is this finding about?"). Where that is genuinely ambiguous, forcing a class = false precision. **The escalation valve is the honest response** — the residual is contained, not eliminated.
- **Early-maturity dead-ends.** While the taxonomy is thin, load-bearing model gaps could leave reads stuck "incomplete" on things only the owner can map. Mitigated by (a) the clarify path, which usually lets the *user* lift the ceiling by supplying the missing graph fact, and (b) treating a spike in load-bearing model gaps as the signal to grow the taxonomy. The alternative — not capping — trades an occasional stuck-incomplete for **systematic false confidence**, a worse trade for an honesty-first product.
- **Interaction-effect findings** that don't factor cleanly into independent single-dimension issues: precedence handles most; the residue escalates rather than being flattened into a wrong single class.

## 5. Build impact (extends Slice 10)

Additive to `slices/10-load-bearing-sensitivity-engine.md`: L0 gains structural-target extraction; L1 gains the top-down alignment traversal + the endpoints table + the tangent/leverage computations; L3 derives `dim`/`dims[]`/acts from the structural target; the escalation-resolution lifecycle and the model-gap display + incompleteness-ceiling become specified behavior. **New guards (server twins, continuing the register — GT-45…GT-50):** `sensitivityEndpointsComplete` (GT-45 — every structural target declares its (X⁺,X⁻) perturbation endpoints; an unmapped target escalates), `dimDerivedFromStructuralTarget` (GT-46), `alignmentIsRelationalTraced` (GT-47 — an alignment finding is edge-keyed and its sensitivity references outcome-reachability; a node-local alignment score fails), `escalationRoutesClarifyOrGovernance` (GT-48), `modelGapCeilingIsIncompleteNotFragile` (GT-49), `unknownNeverScoredAsWeak` (GT-50, pinned). The prototype already ships the escalate-on-new oracle (`findingTypeExhaustiveOrEscalates`); these extend it (engine-level, `pending()` until L1 is built).

## 6. Review (the five outputs — Framework 001)

- **Findings.** (1) Load-bearing is structurally pillar-agnostic (L1/L2 precede L3), so CAF/Viability issues gate by the same test as Grounding — the mechanism is already correct; only the *wording* was grounding-native. (2) Alignment's canonical definition ("coherence between project elements and intended outcomes") is already relational; the top-down edge traversal is its realization, not a new concept. (3) R2's `dim` + `dims[]` shape already supports decompose-with-multi-dim-record. (4) Structural-target assignment satisfies canon Position #11 (type ≠ dimension) while being deterministic.
- **Concerns.** (1) This **reverses CAF §9's "in judgment, not in formula"** for dimension assignment — a real amendment to founder-approved positions, requiring explicit ratification. (2) Deterministic assignment can manufacture false precision where the structural target is ambiguous; mitigated only by the escalation valve — if the valve is under-used, the model over-claims. (3) The incompleteness ceiling can, in an immature taxonomy, produce reads the user can't fully resolve; mitigated by the clarify path and taxonomy-growth signal. (4) The optimization aggregate must not become a hidden score/health readout (single-hue, decomposable, never RAG) — guard it.
- **Dependencies.** The CAF Assessment Model (main) — amendment applies at R1 graduation; DL-196 CARE-POINT pillar filter (Adaptability never leaks to CAF) must be preserved by the new derivation; DL-209 Slice 10 (this extends it); the Demo-Config leverage/threshold knobs; DL-193 exposure (leverage reuse).
- **Recommendation.** Ratify all five first principles. Adopt deterministic-by-structural-target with the escalation valve; adopt the top-down relational Alignment model; reconcile decompose⇄multi-dimension by layer; adopt the leverage-gated known-unknown display and the incompleteness-ceiling (unknown ≠ Fragile). Amend CAF Positions #10/#11 explicitly; preserve #2/#13.
- **Status.** ✅ RATIFIED 2026-08-09 → DL-210. Realization extends Slice 10 / BUILD_SPEC; GT-46…GT-50 registered; the CAF-model amendment is staged for R1 graduation.

## 7. Open for ratification (the specific calls)

1. The **dimension boundary cut** + the **Clarity → Alignment → Feasibility precedence** (§2.1).
2. **Alignment as relational, top-down outcome→roots**, with the optimization + misalignment outputs, tangent check, and metric-mismatch folded in (§2.2).
3. **Deterministic-by-structural-target** dimension assignment — **this amends CAF Positions #10/#11** (§2.3, §"What this amends").
4. The **escalation valve** and its **resolution lifecycle** — runtime → user clarify/verify issue; model-gap → owner/governance (§2.4, §3).
5. **Model-gap display** = leverage-gated known-unknown, and the **incompleteness ceiling** (unknown region can't read Sound, is marked incomplete, and is **never** scored Fragile) (§3).
6. Confirmation that **CAF #2 (independent, multi-dimension-capable) and #13 (flat taxonomy) are preserved**, and DL-196's CARE-POINT filter is guarded.

---

_AI-drafted (Framework 001); **ratified by the owner 2026-08-09 → DL-210**. RB-044 → this Proposal → Review → owner Decision. Realization: DL-210 record created, CAF-model amendment staged for R1 graduation, Slice 10 + BUILD_SPEC extended, GT-46…GT-50 registered._
