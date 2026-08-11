# DL-209 — Load-bearing sensitivity + the issue-classification / resolution model (R2, staged)

- **Date:** 2026-08-09 · **Status:** Ratified · **Decided by:** Idris (Founder Console) · **Class:** A (doctrine — the honesty invariant + classification criteria) with a B (architecture) realization.
- **Framework 001** — AI drafts; only the owner ratifies.
- **Basis:** R&D working session 2026-08-09. Chain: **RB-043** → Proposal (`release-2/GOVERNANCE_PROPOSAL_load-bearing-sensitivity-architecture.md`) → Review (five outputs, in the proposal) → this Decision. Trigger: the "Catering headcount" card tagged Grounding but resolved by a fix (evidence demoted) — an inference wearing a fix affordance, risking a fix raising the Grounding pillar (manufactured confidence).
- **Extends / completes:** DL-196 (integrity via the issue layer) · DL-197 (false-confidence type) · DL-193 (exposure/leverage queue) · DL-184 (R2 graph schema) · DL-190 (`level ≠ trust`). **Bounded by:** DR-7 / DL-103 (one accuracy bar; freemium gates capacity, never judgment quality). It formalizes and completes these; it supersedes none.
- **Placement:** staged in `release-2/`; withheld from `main` until R1 graduation (parity with DL-206/207/208). **No R2 freemium-build impact** (DL-172 §5); authorizes no build — realization routes to its own scoping.

---

## Decision

### A. First principles (ratified as canon)

1. **Issue = a load-bearing threat to outcome integrity.** Honest uncertainty and low-stakes imperfection are not issues (they live on the map, never nagged) — DL-196 §3.
2. **Load-bearing = magnitude of integrity-sensitivity ≥ a calibrated threshold** (two-sided: the span between "confirmed true" and "falsified," which is what catches false confidence — flat upside, large downside). Sensitivity is read from the plan's **dependency structure**, upstream of the integrity band. Two residues are **named boundaries, not defects**: (a) one global, owner-calibrated, auditable threshold applied uniformly; (b) sensitivity inherits the engine's dependency-model quality (a classifier-validation problem, not a criterion gap). The "would resolving move the band" and "span crosses a band" forms are rejected.
3. **Diagnosis ≠ resolution.** Which pillar an issue threatens is a separate question from what act closes it; never fuse them (the ad-hoc `primaryMove` defect).
4. **The honesty invariant — only *verify* moves the Grounding pillar.** A *build* may move Viability/Adaptability but **never** Grounding; a *decide* manufactures no certainty. Guarded, non-negotiable.
5. **Exactly three closing acts — verify · build · decide.** Verify = supply the true state of an inference (confirm **or refute**). Build = edit the plan (add/change/**remove**, incl. a checkpoint). Decide = a boundary/scope/tradeoff call or accept on the record. "De-risk"/"route"/"monitor" are not acts — a goal, or the orthogonal **who** (self/delegate) and **when** (now/deferred) dimensions. **Act→pillar matrix:** verify→{Grounding, and/or Viability-feasibility}; build→{Viability, Adaptability} never Grounding; decide→{Viability-clarity, or nothing}.

### B. Architecture (ratified — realization scopes separately)

**Quarantine the fuzziness:** only plan→dependency-model extraction is probabilistic; everything downstream is deterministic and decomposable. Layers: **L0** plan dependency graph (LLM-extracted, DL-184, uncertainty-tagged — the honest floor) · **L1** deterministic sensitivity engine (two-tier structural pre-filter → counterfactual span on the shortlist; **uncertainty-aware** and **runway-aware**, the plan-stage effect per DL-196 §4) · **L2** thin versioned calibration gate (the only place judgment lives) · **L3** static classification table (finding-type → pillar + permitted acts; only-verify-grounds; **multi-aspect decomposes into single-classed issues**, never dual-classes — DL-197 §7) · **L4** optional offline feedback (improves L2 only; truth-targeted not acceptance-targeted; holdout/off-policy for reflexivity; firewalled from the invariants). Retire the hand-set `primaryMove` in favor of L3 derivation. **Alternatives rejected:** LLM-judge, per-finding hand-rules, raw severity score — none are decomposable.

### C. Threshold strategy (ratified)

Launch a **single global threshold** with the hierarchical-shrinkage machinery built in but **dormant** (every segment shrunk to the global prior until validated data earns it). Decompose "segmentation": **plan-stage → L1** (runway-aware sensitivity, not an L2 segment); **stakes → an explicit owner input** scaling the asymmetric loss / floor (a declared property, transparent knob, never a learned segment); **domain base-rate → the only genuinely learned segment**. Plus a hard **critical-floor** and a separate **user surfacing-preference offset**. The L2 threshold + these knobs are **Demo-Config register entries**.

### D. Enforceable guards (the honesty firewall)

only-verify-moves-Grounding · load-bearing gate is sensitivity-based, never severity-feel · calibration never suppresses the critical floor · segment/preference calibration never lowers the honesty of the read for any segment (DR-7/DL-103) · **at zero data, segmented output equals global** · every surfacing decision is decomposable to its inputs.

## Doctrine preserved (unchanged)

Honesty-first — maturity read, never a forecast (D003/D183b). `level ≠ trust` (DL-190). One accuracy bar for all; freemium gates capacity, never judgment quality (DR-7 / DL-103). Single-hue integrity; decomposability (every figure traces to its source). The load-bearing discipline — only high-sensitivity threats surface; the benign tail stays on the map, never nagged (DL-196 §3 / DL-197 §4).

## Ratification amendment (2026-08-09) — final build dependencies closed

A follow-on owner pass closed the residuals so the engine build carries **no open dependency** — each is now an enforced guard or a defined procedure:

1. **L2 launch = a policy, not a number.** Ratified the **conservative over-surfacing bias** + always-surfaced `LB_CRITICAL_FLOOR` + `LB_ASYMMETRIC_LOSS` as the launch policy. The absolute `LB_THRESHOLD` is set by a **calibration procedure** — ship the policy → shadow-run against the first real plans → owner reviews the surfaced-vs-suppressed boundary → lock → telemetry-confirm — never a guessed constant.
2. **Escalate-on-new (new enforced invariant).** The finding-type table's 6 rows are **launch-complete**; an **unmapped finding-type hard-escalates** (surfaces to the owner) and never default-classifies — Anti-Assumption enforced in code (`findingTypeExhaustiveOrEscalates`, GT-38). New types graduate only via governance.
3. **Build vehicle = Slice 10.** Realized as `slices/10-load-bearing-sensitivity-engine.md`, sequenced in `BUILD_SEQUENCE.md` (Phase B+, after Slices 1 & 2), with server twins **GT-34…GT-44** in the Slice 9 acceptance gate.

## Open (deferred, non-blocking to build)

The L0 dependency-model validation is a named **classifier-validation track** (Slice 10 §6), owned separately from the honesty guards · L4 holdout design precedes any threshold learning (segmentation ships **dormant**, guarded by `zeroDataSegmentEqualsGlobal`). Neither gates the L0→L3 build.

## Affected artifacts

`GOVERNANCE_PROPOSAL_load-bearing-sensitivity-architecture.md` · `BACKLOG_RB-043_issue-classification-load-bearing.md` · `BUILD_SPEC_DL-209_load-bearing-sensitivity-engine.md` · **`slices/10-load-bearing-sensitivity-engine.md`** (the signed slice) · `slices/09-…` §3 register (**GT-34…GT-44**) · `BUILD_SEQUENCE.md` (Phase B+) · `acceptance/README.md` · `DEMO_CONFIG_REGISTER.md` (L2 params + launch policy) · prototype `oslo-prototype-r2.html` (L3 derivation + 5 firewall guards). Relationship: **completes DL-196/197**, consumes DL-184/193/190, bounded by DR-7/DL-103.

---

_AI-drafted (Framework 001); **ratified by the owner 2026-08-09**. Staged in `release-2`; folds into `main` at R1 graduation with the other R2-staged DLs._
