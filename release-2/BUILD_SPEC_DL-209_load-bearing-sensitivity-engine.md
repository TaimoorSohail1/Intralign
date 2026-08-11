# Build Spec — Load-bearing sensitivity + issue-classification engine (DL-209)

**Realizes:** DL-209 + **DL-210** (CAF dimension boundaries, deterministic structural-target assignment, relational alignment, the escalation model — see Slice 10 §3b for the full realization). **Extends:** Slice 01 (integrity engine), Slice 02 (issue lifecycle & grounding acts), DL-184 (graph schema), DL-193 (exposure queue). **Status:** ratified 2026-08-09; realized as **Slice 10** — staged in `release-2/`, R2-isolated. The prototype L3 (derived resolution + 5 firewall guards, incl. escalate-on-new) already ships in `oslo-prototype-r2.html`. This spec is the server/engine realization; Slice 10 is its signed slice form.

**Thesis (non-negotiable):** *quarantine the fuzziness.* The only probabilistic step is L0 (plan → dependency graph). L1–L3 are **deterministic and decomposable**: given a graph, every load-bearing decision and every resolution affordance is a pure function with a trace to its inputs. L4 is offline, optional, and firewalled to the L2 calibration parameters.

---

## 1. Locked decisions (DL-209 — the invariants the build must honor)

1. **Issue = a load-bearing threat.** Honest uncertainty and low-stakes imperfection never become issues (DL-196 §3).
2. **Load-bearing = magnitude of integrity-sensitivity ≥ a calibrated threshold** (two-sided span; catches false confidence). Read from the dependency structure, upstream of the band.
3. **Diagnosis ≠ resolution.** Pillar (where integrity sits) is derived separately from the closing act (the CTA).
4. **Only *verify* moves Grounding.** A build moves Viability/Adaptability, never Grounding; a decide manufactures no certainty.
5. **Three closing acts — verify · build · decide.** ("De-risk"/"route"/"monitor" are not acts — a goal, or the who/when dimensions.)

Act→pillar matrix: verify → {Grounding, and/or Viability-feasibility}; build → {Viability, Adaptability} never Grounding; decide → {Viability-clarity, or nothing}.

## 2. L0 — Plan dependency graph (data model; extends DL-184 / Slice 01)

The extractor (LLM, the sole probabilistic step) emits a typed graph. **Every node and edge carries an extraction-confidence** — uncertainty must propagate, never be dropped.

- **Node** `{ id, type: outcome|deliverable|workstream|task|assumption|inference|dependency|metric, label, provenance: grounded|inferred|proposed|accepted, extractionConfidence: 0..1 }`
- **Edge** `{ from, to, rel: supports|rests-on|feeds, weight: 0..1, extractionConfidence: 0..1 }` — `to` is what depends on `from`; weight = strength of dependence.

**Contract:** identical graph ⇒ identical downstream output. The graph is the honest floor (§8).

## 3. L1 — Sensitivity engine (deterministic)

Per candidate node X (an inference, a structural gap, a dependency):

1. **Structural-leverage pre-filter (cheap):** `lev(X)` = weighted sum of outcome-critical paths through X (graph centrality toward the outcome node). Shortlist = `lev(X) ≥ prefilterCut`.
2. **Two-sided counterfactual span (shortlist only):** `span(X) = | integrity(X := confirmed-true) − integrity(X := falsified) |`, recomputing the integrity function (Slice 01) under each counterfactual. Two-sided is mandatory — it is what catches false confidence (flat upside, large downside).
3. **Sensitivity:** `sensitivity(X) = f(span(X), lev(X)) · uncertaintyFactor(X) · runwayFactor(X)`
   - `uncertaintyFactor` **rises** when X's own dependencies have low `extractionConfidence` (uncertainty compounds *toward* attention, never away).
   - `runwayFactor` **rises** as execution nears (the plan-stage effect lives HERE, per DL-196 §4 — not in L2).
4. **Output per X:** `{ sensitivity, exposureRank (DL-193), trace: the paths + counterfactuals that produced the score }`. Deterministic and decomposable.

## 4. L2 — Calibration gate (the only place judgment lives)

Parameters (registered in the Demo-Config register):

| Param | Type | Launch | Role |
|---|---|---|---|
| `LB_THRESHOLD` | float | one global value | the load-bearing cutoff on `sensitivity` |
| `LB_ASYMMETRIC_LOSS` | float ≥1 | owner-set | miss costs more than a marginal surface; biases toward surfacing within the anti-treadmill budget |
| `LB_CRITICAL_FLOOR` | float | owner-set | sensitivity above this **always** surfaces (never suppressible) |
| `LB_SURFACE_PREF` | float (signed) | user dial | surfacing preference offset; changes surfacing, never the read's honesty |
| `segmentThreshold[domain]` | float | **dormant** | hierarchical; shrinks fully to `LB_THRESHOLD` until L4 earns it |

Gate: `isLoadBearing(X) = sensitivity(X) ≥ LB_CRITICAL_FLOOR OR sensitivity(X) ≥ effectiveThreshold(ctx)` where `effectiveThreshold(ctx) = shrink(LB_THRESHOLD, segmentThreshold[ctx.domain], n_labels[ctx.domain]) − LB_SURFACE_PREF`. **Stage is not a segment** (it's L1 runway); **stakes is an explicit input** scaling `LB_ASYMMETRIC_LOSS` / lowering the threshold, never a learned segment; **domain is the only learned segment**.

## 5. L3 — Classification derivation (the table; already prototyped)

`basisInference(issue)` = the read **rests on** a value OSLO inferred (not a structural absence). Table (finding-type → pillar, primary act, also-offered):

| finding-type | basis | pillar | primary | also-offered | rule |
|---|---|---|---|---|---|
| Inference gap · False confidence | inference | Grounding | **verify** | build (de-risk) | only verify grounds |
| Unowned · No deadline · No backup | structural | Viability | **build** | verify-to-refute (if "does it already exist?") | build never grounds |
| Coverage gap (no checkpoint) | structural | Adaptability | **build** (add checkpoint) | — | |
| Metric mismatch | structural | Viability | **build** (change KPI) | — | |
| No limit set (tradeoff) | decision | Viability | **decide** (draw line / accept) | — | |
| Dependency-may-fail (e.g. Wi-Fi) | inference + feasibility | Viability-feasibility | **verify** (confirm dependency) | build (fallback) | verify de-risks *and* grounds |

Derivation (prototype-proven): `basisInference ⇒ primary = verify`; else `primary = build` (decide for tradeoffs). **Multi-aspect ⇒ decompose** into single-typed issues (DL-197 §7) — never dual-class. Retire any hand-set `primaryMove`.

## 6. L4 — Feedback loop (offline · optional · firewalled)

- **Signals:** outcome-grounded labels (delayed, sparse, confounded — the honest label); expert labels; dismissal = **weak/ambiguous** signal (could be "wrong" or a deliberate accept). **Never** optimize acceptance — that trains suppression of false-confidence warnings.
- **Update:** L2 parameters only, offline (batch, versioned deploy — no online learning). Off-policy/**holdout**-corrected for reflexivity (OSLO influences its own data). Per-segment learning enabled only on data sufficiency; shrinkage handles the ramp.
- **Firewall:** never touches L0/L1/L3 or the invariants; never lowers the read's honesty for any segment (DR-7/DL-103).

## 7. Honesty invariants (testable) — server-twin GT register

Client `_S10` guards are the oracle; each gets a server twin (same name). New for DL-209 (continue the GT numbering from Slice 09):

- **onlyVerifyMovesGrounding** (integration) — no build/decide act raises the Grounding pillar; only a verify (attest/confirm) does.
- **resolutionDerivedFromModel** (structural) — resolution comes from the L3 table + `basisInference`; no hand-set `primaryMove` exists.
- **loadBearingInferenceVerify** (structural) — every load-bearing inference exposes a verify path as primary.
- **findingModelComplete** (structural) — every issue has a finding-type in the table and `basisInference` set.
- **findingTypeExhaustiveOrEscalates** (negative/pinned) — an unmapped finding-type returns `escalate` and surfaces to the owner; it never silently default-classifies (Anti-Assumption enforced in code).
- **sensitivityDeterministic** (unit) — identical graph ⇒ identical sensitivity.
- **sensitivityDecomposable** (unit) — every sensitivity carries a trace to its paths/counterfactuals.
- **falseConfidenceCaughtBySpan** (unit) — a strong-on-inference artifact qualifies via downside span (the DL-197 case).
- **zeroDataSegmentEqualsGlobal** (unit) — at zero labels, `effectiveThreshold` == global (dormant segmentation is unbiased).
- **floorNeverSuppressed** (negative/pinned) — no `LB_SURFACE_PREF`/segment value drops a `LB_CRITICAL_FLOOR` item.
- **calibrationNeverLowersHonesty** (pinned) — L4/segment calibration changes surfacing only; the accuracy bar is invariant across segments/tiers (DR-7/DL-103).

**DL-210 twins (GT-45…GT-50):** `sensitivityEndpointsComplete` (every structural target declares its endpoints; unmapped escalates) · `dimDerivedFromStructuralTarget` (pinned — dim from structural target, never finding-type; CAF #11 preserved) · `alignmentIsRelationalTraced` (pinned — alignment is edge-keyed, sensitivity references outcome-reachability) · `escalationRoutesClarifyOrGovernance` (runtime → user clarify/verify issue; model-gap → governance) · `modelGapCeilingIsIncompleteNotFragile` (pinned) · `unknownNeverScoredAsWeak` (pinned — unknown ≠ bad). Engine-level; `pending()` until L1 is built. Realization detail in Slice 10 §3b.

## 8. Named boundaries (residuals — write into acceptance, don't hide)

- **L0 dependency-model quality** is the permanent floor — sensitivity is only as true as "what rests on what." Primary investment; mitigated by uncertainty-propagation (L1), asymmetric calibration (L2), and user correction (verify/refute) feeding L4. Needs its own validation, separate from the affordance guards.
- **Label scarcity + reflexivity** — L4 improves gradually; holdouts are mandatory before any threshold learning.

## 9. Build sequencing (viability)

**Ship L0→L3 with a hand-set, conservative, global `LB_THRESHOLD`.** Deterministic, defensible, decomposable on day one; no dependency on data you don't have. **L4 + domain segmentation are v2** — they snap onto L2 without touching L0/L1/L3 or the invariants.

## 10. Reuse vs net-new

**Reuse:** L0 = DL-184 graph + Slice 01 integrity function; L3 resolution + "apply-fix firms Viability not Grounding" = Slice 02 (`_applyPlanChange`, the mitigated→needs-grounding fork); exposure rank = DL-193; only-verify-grounds = Slice 02's grounding-acts boundary. **Net-new:** L1 sensitivity engine (two-sided span + uncertainty/runway weighting), L2 calibration gate + params, L4 loop, and the GT twins in §7.

## 11. Residuals — all closed to a guard or a defined procedure (ratified 2026-08-09)

No open build dependencies remain. Each former open item now has an enforced exit:

- **`LB_THRESHOLD` / `LB_ASYMMETRIC_LOSS` / `LB_CRITICAL_FLOOR` values** → the ratified **launch policy** (conservative floor) + **calibration procedure**: ship the policy → shadow-run against the first real plans → owner reviews the surfaced-vs-suppressed boundary → lock → telemetry-confirm. The value is never guessed; `pending()` in the suite until locked (Demo-Config).
- **Finding-type table completeness** → the 6 rows are **launch-complete**; production types graduate via governance, and an unmapped type is caught by **`findingTypeExhaustiveOrEscalates` / GT-38** (escalate-on-new, in code today).
- **L0 dependency-model validation** → a named classifier-validation track (Slice 10 §6), owned separately from the honesty guards.
- **L4 holdout design** → required before any threshold learning; segmentation ships **dormant** until then (guarded by `zeroDataSegmentEqualsGlobal` / GT-42).

## 12. Build vehicle

Realized as **Slice 10** (`slices/10-load-bearing-sensitivity-engine.md`), sequenced in `BUILD_SEQUENCE.md` after Slices 1 & 2 (Phase B+). Server twins **GT-34…GT-44** registered in the Slice 9 acceptance gate.

---

_Realizes DL-209 (Framework 001). Ratified 2026-08-09; staged in `release-2`, folds into `main`/the build tree at R1 graduation. Authorizes the build against these interfaces; parameter values are set by the §11 calibration procedure, not guessed._
