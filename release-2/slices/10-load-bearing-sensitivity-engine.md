# Slice 10 — Load-Bearing Sensitivity + Issue-Classification Engine

**Realizes:** DL-209 + **DL-210** (CAF dimension boundaries, deterministic structural-target assignment, relational alignment, the escalation model). **Extends:** Slice 1 (integrity engine — the `Issue`/`Pillar`/`Integrity` objects and the exposure queue), Slice 2 (issue lifecycle & grounding acts — the derived resolution affordance). **Consumes:** DL-184 (graph schema), DL-193 (exposure/leverage queue). **Bounded by:** DR-7 / DL-103 (one accuracy bar). **Status:** signed-off build design (owner-ratified 2026-08-09). The prototype L3 (derived resolution + 5 firewall guards, incl. escalate-on-new) already ships in `oslo-prototype-r2.html` as the reference oracle; this slice is the server/engine realization.

**Thesis — quarantine the fuzziness.** The only probabilistic step is **L0** (plan → dependency graph). L1–L3 are **deterministic and decomposable**: given a graph, every load-bearing decision and every resolution affordance is a pure function with a trace to its inputs. **L4** is offline, optional, and firewalled to the L2 calibration parameters.

---

## 1. Locked decisions

DL-209's five first principles are the invariants the build honors:

1. **Issue = a load-bearing threat to outcome integrity.** Honest uncertainty and low-stakes imperfection are never issues — they live on the map, never nagged (DL-196 §3).
2. **Load-bearing = magnitude of integrity-sensitivity ≥ a calibrated threshold** (two-sided span; catches false confidence). Read from the dependency structure, upstream of the band.
3. **Diagnosis ≠ resolution.** Pillar (where integrity sits) is derived separately from the closing act.
4. **Only *verify* moves Grounding.** A build moves Viability/Adaptability, never Grounding; a decide manufactures no certainty. Guarded, non-negotiable.
5. **Three closing acts — verify · build · decide.** ("De-risk"/"route"/"monitor" are not acts.) Act→pillar matrix: verify → {Grounding, and/or Viability-feasibility}; build → {Viability, Adaptability} never Grounding; decide → {Viability-clarity, or nothing}.

**Ratified realization decisions (2026-08-09):**
- **L2 threshold launch policy** = a **conservative over-surfacing bias** + an always-surfaced `LB_CRITICAL_FLOOR` + asymmetric loss (`LB_ASYMMETRIC_LOSS`). The absolute `LB_THRESHOLD` is an owner-config placeholder, resolved by the **calibration procedure** (§7), not a guessed constant.
- **Finding-type table** = the ratified rows (§4, L3) are launch-complete; an unmapped type **hard-escalates** (never default-classifies) — enforced by GT-38.
- **Vehicle** = this slice (Slice 10), sequenced after the integrity/issue foundation it extends.

## 2. Data / object model

**L0 — Plan dependency graph** (extends DL-184; the extractor is the sole probabilistic step). Every node and edge carries an **extraction-confidence** so uncertainty propagates, never dropped.

- **Node** `{ id, type: outcome|deliverable|workstream|task|assumption|inference|dependency|metric, label, provenance: grounded|inferred|proposed|accepted, extractionConfidence: 0..1 }`
- **Edge** `{ from, to, rel: supports|rests-on|feeds, weight: 0..1, extractionConfidence: 0..1 }` — `to` depends on `from`; weight = strength of dependence.

**Sensitivity record** (L1 output, one per candidate) `{ nodeId, sensitivity: number, loadBearing: bool, exposureRank, trace: { paths[], spanTrue, spanFalse, lev, uncertaintyFactor, runwayFactor } }`.

**Finding record** (L3) `{ issueId, findingType, basis: inference|structural|decision, pillar, primaryAct: verify|build|decide, alsoOffered[] }` — or `{ issueId, findingType, escalate: true }` when the type is unmapped.

**Contract:** identical graph ⇒ identical L1/L2/L3 output. The graph is the honest floor (§6, named boundary).

## 3. Computation spec — L1 sensitivity engine (deterministic)

Per candidate node X (an inference, a structural gap, a dependency):

1. **Structural-leverage pre-filter (cheap):** `lev(X)` = weighted count of outcome-critical paths through X (centrality toward the outcome node). Shortlist = `lev(X) ≥ prefilterCut`.
2. **Two-sided counterfactual span (shortlist only):** `span(X) = | integrity(X := confirmed-true) − integrity(X := falsified) |`, recomputing the Slice 1 integrity function under each counterfactual. **Two-sided is mandatory** — it is what catches false confidence (flat upside, large downside).
3. **Sensitivity:** `sensitivity(X) = f(span(X), lev(X)) · uncertaintyFactor(X) · runwayFactor(X)`.
   - `uncertaintyFactor` **rises** when X's own dependencies have low `extractionConfidence` (uncertainty compounds *toward* attention).
   - `runwayFactor` **rises** as execution nears (the plan-stage effect lives HERE — DL-196 §4 — not in L2).
4. **Output:** the sensitivity record above — **decomposable** (every score carries its paths + counterfactuals).

### L2 — calibration gate (the only place judgment lives)

`isLoadBearing(X) = sensitivity(X) ≥ LB_CRITICAL_FLOOR OR sensitivity(X) ≥ effectiveThreshold(ctx)`, where `effectiveThreshold(ctx) = shrink(LB_THRESHOLD, segmentThreshold[ctx.domain], n_labels[ctx.domain]) − LB_SURFACE_PREF`. **Stage is not a segment** (it's L1 runway); **stakes is an explicit input** scaling `LB_ASYMMETRIC_LOSS`; **domain is the only learned segment**, dormant at launch (shrinks fully to the global prior until L4 earns it). Parameters are Demo-Config entries (§7).

### L3 — classification derivation (finite table; prototype-proven)

`basisInference(issue)` = the read **rests on** a value OSLO inferred (not a structural absence).

| finding-type | basis | pillar | primary | also-offered | rule |
|---|---|---|---|---|---|
| Inference gap · False confidence | inference | Grounding | **verify** | build (de-risk) | only verify grounds |
| Dependency-may-fail (e.g. Wi-Fi) | inference + feasibility | Viability-feasibility | **verify** (confirm dependency) | build (fallback) | verify de-risks *and* grounds |
| Unowned · No deadline · No backup | structural | Viability | **build** | verify-to-refute (if a "does it already exist?" path) | build never grounds |
| Coverage gap (no checkpoint) | structural | Adaptability | **build** (add checkpoint) | — | |
| Metric mismatch | structural | Viability | **build** (change KPI) | — | |
| No limit set (tradeoff) | decision | Viability | **decide** (draw line / accept) | — | |

Derivation: `basisInference ⇒ primary = verify`; else `primary = build` (decide for tradeoffs). **Multi-aspect ⇒ decompose** into single-typed issues (DL-197 §7) — never dual-class. **An unmapped finding-type escalates** (GT-38) — the table graduates via governance, never by silent default. Retire any hand-set `primaryMove`.

### L4 — feedback loop (offline · optional · firewalled)

Signals: outcome-grounded labels (delayed, sparse, confounded — the honest label), expert labels, and a **weak/ambiguous** dismissal signal. **Never optimize acceptance** — that trains suppression of false-confidence warnings. Updates **L2 parameters only**, offline (batch, versioned deploy), off-policy/**holdout**-corrected for reflexivity. Firewalled: never touches L0/L1/L3 or the invariants; never lowers the read's honesty for any segment (DR-7/DL-103).

## 3b. DL-210 — structural-target assignment, relational alignment & the escalation model

**Dimension assignment is deterministic from the finding's STRUCTURAL TARGET, not its finding-type** (preserves CAF Position #11). L0 tags each finding with `structuralTarget ∈ { definition | edge | achievability | truth | coverage }` + graph location + extraction-confidence — the sole judgment. L3 then derives `dim`/`dims[]`/acts deterministically:

| structuralTarget | dimension | resolution act |
|---|---|---|
| `definition` | Clarity (Viability) | clarify (verify) |
| `edge` | Alignment (Viability) | verify/decide on the edge |
| `achievability` | Feasibility (Viability) | build/decide |
| `truth` | Grounding | verify |
| `coverage` | Adaptability | build (checkpoint) |

**Precedence Clarity → Alignment → Feasibility.** A downstream concern caused by an upstream gap is deferred behind its cause, not raised independently. Multi-target observation → decomposed single-`dim` issues (multi-dimension recorded in `dims[]`; CAF #2 preserved). **DL-196 CARE-POINT preserved:** Adaptability issues never leak into the CAF band/rows/heat.

**Perturbation endpoints by structural target** (favorable ↔ adverse, bounded by the *plausible* resolutions the evidence supports — not literal extremes, to avoid span inflation):

| Target | Dimension | X⁺ | X⁻ |
|---|---|---|---|
| truth of an inference | Grounding | inferred value true | inferred value false |
| achievability vs constraints | Feasibility | constraint doesn't bind | constraint binds |
| definition | Clarity | resolves to the supported favorable reading | resolves to the supported adverse reading |
| **edge (serves-relationship)** | **Alignment** | **segment genuinely contributes to the outcome** | **segment is a non-contribution / off-tree** |
| coverage / checkpoint | Adaptability | on a shift, the plan adapts | on a shift, it can't |

**Relational alignment (top-down traversal).** Alignment is an **edge** property, evaluated over the `serves` edges by traversing **outcome → lowest roots along each element path**. Per-edge sensitivity scales with the **stranded subtree** (a weak edge high in the tree strands everything beneath it → high sensitivity; a weak leaf edge → low, rests on the map). Per-path **optimization** = an aggregate of how well-aligned the path is (single-hue, decomposable — never a RAG/health score). **Tangent check:** an element on no outcome-rooted path is a first-class alignment exposure. Metric-mismatch is one such bad edge.

**Escalation resolution lifecycle (no edge silently judged).**
- **Runtime (the plan is underspecified) → a user-facing issue.** Missing/ambiguous target identity → a **Clarity issue** (resolve by clarifying); both elements clear but sufficiency is a judgment the plan doesn't settle → the **Alignment issue itself** (resolve by verify/decide on the edge). Runs the load-bearing gate (benign ambiguities rest on the map), closes via act→reanalysis, and **cascades** — clarifying unlocks the blocked downstream assessment; the stranded-subtree collapses many downstream un-evaluable edges into one upstream clarify.
- **Model-gap (OSLO's taxonomy has no mapping) → owner/governance + a leverage-gated known-unknown.** Routes to build/backlog via Framework 001. Surfaced to the user **only when its structural leverage puts it on a path to the outcome** (leverage is graph-computable even when classification isn't), as an explicitly **unassessed** "noted — help me understand this" item: no dimension tag, no band color, distinct from graded issues, with a clarify affordance that resolves it and graduates the taxonomy. Benign model gaps rest on the map.

**Integrity treatment of an unassessed load-bearing gap.** It **prevents a Sound claim** and marks the region **incomplete / under review** (pending marker) — weakest-gate honesty applied to unknowns. It is **NOT** scored Fragile or penalized numerically (*unknown ≠ bad*). Localized and leverage-gated, so benign gaps never drag the read down.

## 4. Honesty invariants (testable)

- **INV-1** Only a *verify* act raises the Grounding pillar; a *build* or *decide* never does. (→ GT-35)
- **INV-2** The load-bearing gate is sensitivity-based (two-sided span), never a severity feel. (→ GT-39, GT-41)
- **INV-3** Every surfacing decision is decomposable to its inputs (paths + counterfactuals). (→ GT-40)
- **INV-4** At zero data, segmented output equals the global threshold. (→ GT-42)
- **INV-5** `LB_SURFACE_PREF` / segment calibration can never suppress a `LB_CRITICAL_FLOOR` item. (→ GT-43)
- **INV-6** Segment/preference/L4 calibration changes surfacing only — never the honesty of the read for any segment. (→ GT-44)
- **INV-7** Resolution is derived from finding-type + basis; no hand-set per-item `primaryMove`. (→ GT-34)
- **INV-8** Every load-bearing inference leads with a verify CTA; every issue is classified, and an unmapped type escalates. (→ GT-36, GT-37, GT-38)

## 5. FE ↔ BE integration bindings

| Surface | Reads | Written-by (act) | Changed-by (event) |
|---|---|---|---|
| Issue card **primary affordance** | L3 finding record (`primaryAct`) | — (read-only projection of the model) | `reanalysis.landed` (re-derive on graph change) |
| **Exposure / worklist** ordering | L1 sensitivity record (`exposureRank`, `loadBearing`) | — | `reanalysis.landed` |
| **Ground-it / evidence** CTA presence | L3 (`alsoOffered` verify path) | verify act → attestation ledger (Slice 2) | `reanalysis.landed` |
| **"Other ways"** disclosure | L3 (`alsoOffered`) | — | — |

The primary affordance and the load-bearing gate are **read-only projections** of the deterministic model — a `—` in Written-by, a pinned no-write negative (parity with GT-14). The hand-set `primaryMove` is retired; the card renders what the model derives.

## 6. R1 reuse vs net-new

**Reuse:** L0 = DL-184 graph + Slice 1 integrity function; L3 resolution + "apply-fix firms Viability not Grounding" = Slice 2 (`_applyPlanChange`, the mitigated→needs-grounding fork); exposure rank = DL-193; only-verify-grounds = Slice 2's grounding-acts boundary (GT-27/GT-33). **Net-new:** L1 sensitivity engine (two-sided span + uncertainty/runway weighting), L2 calibration gate + params, L4 loop, and the GT-34…GT-44 twins (§8).

**Named boundary (not a defect):** L0 dependency-model quality is the permanent floor — sensitivity is only as true as "what rests on what." Primary investment; mitigated by uncertainty-propagation (L1), asymmetric calibration (L2), and user correction (verify/refute) feeding L4. It needs its own classifier validation, separate from the affordance guards.

## 7. Open items / placeholders (calibration procedure — the exit for each)

None block the build; each residual has a defined exit rather than a "TBD":

1. **`LB_THRESHOLD` launch value** (+ `LB_ASYMMETRIC_LOSS`, `LB_CRITICAL_FLOOR`) — Demo-Config, owner-config. **Calibration procedure:** ship the conservative-floor policy → shadow-run the engine against the first batch of real plans (surface nothing to users) → owner reviews the surfaced-vs-suppressed boundary → lock the value → telemetry-confirm at launch. `pending()` in the suite until locked; hardcoding it in copy turns red.
2. **Finding-type table completeness** — ratified 6 rows are launch-complete; production types graduate via governance. Enforced safe by GT-38 (escalate-on-new).
3. **L0 dependency-model validation** — classifier-validation track, owned separately from the honesty guards.
4. **L4 holdout design** — required before any threshold learning is enabled; segmentation ships dormant until then.

## 8. Acceptance criteria (GT register — server-side twins)

Continues the Slice 9 register. Client `_S10` guards are the reference oracle; each server twin preserves the guard name.

1. **GT-34 · resolutionDerivedFromModel** (structural) — resolution is derived from finding-type + `basisInference`; no per-item `primaryMove` exists. (INV-7)
2. **GT-35 · onlyVerifyMovesGrounding** (integration, pinned) — no build/decide act raises Grounding; only a verify (confirm/refute) does. (INV-1)
3. **GT-36 · loadBearingInferenceVerify** (structural) — every load-bearing inference exposes a verify path as primary. (INV-8)
4. **GT-37 · findingModelComplete** (structural) — every issue carries a finding-type + basis. (INV-8)
5. **GT-38 · findingTypeExhaustiveOrEscalates** (negative, pinned) — an unmapped finding-type returns `escalate`, never a default class; a synthetic unclassified finding escalates, a classified one resolves. (INV-8)
6. **GT-39 · sensitivityDeterministic** (unit) — identical graph ⇒ identical sensitivity. (INV-2)
7. **GT-40 · sensitivityDecomposable** (unit) — every sensitivity carries a trace to its paths + counterfactuals. (INV-3)
8. **GT-41 · falseConfidenceCaughtBySpan** (unit) — a strong-on-inference artifact qualifies via downside span (the DL-197 case), not severity. (INV-2)
9. **GT-42 · zeroDataSegmentEqualsGlobal** (unit, pinned) — at zero labels, `effectiveThreshold == LB_THRESHOLD`. (INV-4)
10. **GT-43 · floorNeverSuppressed** (negative, pinned) — no `LB_SURFACE_PREF`/segment value drops a `LB_CRITICAL_FLOOR` item. (INV-5)
11. **GT-44 · calibrationNeverLowersHonesty** (negative, pinned) — L4/segment/preference calibration changes surfacing only; the accuracy bar is invariant across segments/tiers (DR-7/DL-103). (INV-6)

**DL-210 twins (GT-45…GT-50):**

12. **GT-45 · sensitivityEndpointsComplete** (structural) — every structural target declares its (X⁺, X⁻) perturbation endpoints; an unmapped target escalates.
13. **GT-46 · dimDerivedFromStructuralTarget** (structural, pinned) — an issue's `dim`/`dims[]` is derived from the finding's structural target, never hand-set and never mapped from finding-type (CAF #11 preserved).
14. **GT-47 · alignmentIsRelationalTraced** (structural, pinned) — an Alignment finding is edge-keyed and its sensitivity references outcome-reachability (top-down traversal); a node-local alignment score fails.
15. **GT-48 · escalationRoutesClarifyOrGovernance** (integration) — a runtime escalation generates a user Clarity/Alignment issue; a model-gap routes to governance and never default-classifies.
16. **GT-49 · modelGapCeilingIsIncompleteNotFragile** (negative, pinned) — a load-bearing model gap marks its region *incomplete* and blocks a Sound claim, and is never scored Fragile or penalized numerically.
17. **GT-50 · unknownNeverScoredAsWeak** (negative, pinned) — no unassessed region contributes a numeric/band penalty; unknown ≠ bad.

## 9. Build sequencing

**Ship L0→L3 with a hand-set, conservative, global `LB_THRESHOLD` (the launch policy).** Deterministic, defensible, decomposable on day one — no dependency on data you don't have. **L4 + domain segmentation are v2** — they snap onto L2 without touching L0/L1/L3 or the invariants. Slice depends on Slices 1 & 2 being green; freeze INV-1 (`onlyVerifyMovesGrounding`, pinned) with them before L1/L2 work begins.

---

*Slice 10 of the R2 delta (DL-209 realization). Depends on Slices 1 & 2. On sign-off → the L0 classifier-validation track and the L2 calibration procedure (§7). Prototype reference: `oslo-prototype-r2.html` L3 + the 5 DL-209 firewall guards.*
