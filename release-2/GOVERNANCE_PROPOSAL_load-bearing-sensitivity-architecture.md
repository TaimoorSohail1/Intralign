# Governance Proposal — Load-bearing sensitivity: the architecture for classifying and gating outcome-integrity issues

- **Status:** ✅ **RATIFIED 2026-08-09 by Idris → DL-209** (`canon/decisions/DL-209_LOAD_BEARING_SENSITIVITY_AND_ISSUE_CLASSIFICATION.md`). This proposal is the review record behind that decision.
- **Class:** A (doctrine — it fixes the honesty invariant and the issue-classification criteria) with an B (architecture) realization section.
- **Basis:** R&D working session 2026-08-09 (owner-directed critical design of the issue-classification / load-bearing model). Chain: **RB-043** → this Proposal → Review (five outputs, below) → owner Decision (candidate **DL-209**).
- **Grounds in / consumes:** DL-184 (R2 graph schema) · DL-193 (exposure/leverage queue) · DL-196 (integrity via the issue layer) · DL-197 (false-confidence issue type) · DL-190 (`level ≠ trust`) · DR-7 / DL-103 (one accuracy bar; freemium gates capacity, never judgment quality) · the Demo-Config register (owner-config thresholds).
- **Placement:** staged in `release-2/`; withheld from `main` until R1 graduation (parity with the other R2-staged decisions).

---

## 1. Problem

Issue classification and the resolution affordance offered on each card are currently set **ad hoc** per issue (a hand-set `primaryMove` of `ground`/`fix`), decoupled from the issue's pillar and from what actually closes it. This produces incoherence that erodes trust:

- The "Catering headcount" card is tagged **Grounding**, its basis is literally "OSLO's inference from Budget.md," yet its primary action is "Apply this fix" with evidence buried under "Other options." An *inference* wearing a *fix* affordance.
- The same decoupling makes the evidence CTA appear inconsistently even **within** the Grounding pillar.
- Worst case (the trust breach): a fix that raises the **Grounding** pillar without the underlying inference being grounded is *manufactured confidence* — the precise failure DL-197 exists to prevent.

The deeper gap is that the criteria for classifying an issue — and especially for deciding what is a **load-bearing** threat worth surfacing at all — are implicit and subjective, not an explicit, durable, enforceable model.

## 2. First principles (the doctrine to ratify)

Settled by critical analysis this session; five roots, each stress-tested.

1. **What earns the name "issue."** An issue is a **load-bearing threat to outcome integrity** — the outcome genuinely rests on it and it is currently weak. Honest uncertainty and low-stakes imperfections are **not** issues; they live on the map, never nagged. *(Already canon — DL-196 §3.)*

2. **"Load-bearing" is defined by effect on integrity, not by feel — in the magnitude-with-threshold form.** X is load-bearing iff the **magnitude of the outcome-integrity sensitivity to X ≥ a calibrated threshold**, where sensitivity is the span between "X confirmed true" and "X falsified," read from the plan's **dependency structure** (upstream of the integrity band it feeds). *Two-sided* is required — it is what catches false confidence (flat upside, huge downside). The earlier "would resolving it move the band" form is **rejected** (it misclassifies false confidence as benign), and "span crosses a band" is **rejected** (a discretization artifact). Two judgment residues are named, not hidden: **(a)** the threshold is one global, owner-calibrated, auditable parameter applied uniformly — a product choice, not a derivation; **(b)** sensitivity inherits the engine's dependency-model quality — a boundary that belongs to the classifier's validation, not to the criterion. Defensible *because* it confines judgment to one visible place; a claim of objectivity-all-the-way-down would be indefensible and off-doctrine (OSLO rejects false precision).

3. **Diagnosis and resolution are two different questions and must never be fused.** *Which pillar it threatens* (→ where integrity sits and moves) is separate from *what act honestly closes it* (→ the CTA). Fusing them via a hand-set `primaryMove` is the root defect.

4. **The honesty invariant — only the earning act moves its pillar.** Integrity rises only by an act that genuinely earns it. Precisely: **only *verify* moves the Grounding pillar** — a *build* may move Viability and/or Adaptability but **never Grounding**; a *decide* records a call and manufactures no certainty. Non-negotiable; this is the entire basis of user trust.

5. **Exactly three irreducible closing acts: verify · build · decide.** **Verify** = supply the true state of an inference (confirm **or refute**), by evidence or judgment. **Build** = edit the plan (add / change / **remove** an element, incl. a monitoring checkpoint). **Decide** = a boundary/scope/tradeoff call, or accept an exposure on the record. "De-risk," "route," and "monitor" are **not** acts — they are a *goal* (reached via verify/build) or two orthogonal dimensions: **who** performs the act (self / delegate) and **when** (now / deferred-via-checkpoint). Stress-tested against six candidate "fourth acts"; all decompose.

**Act → pillar-effect matrix (the enforceable heart, derived from Roots 4+5):** verify → {Grounding, and/or Viability-feasibility}, never Adaptability · build → {Viability and/or Adaptability}, **never Grounding** · decide → {Viability-clarity, or nothing}, never Grounding/Adaptability.

## 3. Architecture (the realization — addresses Root 2)

**Design thesis: quarantine the fuzziness.** The only step that must be probabilistic/LLM-driven is *extracting the plan into a dependency model*. Everything downstream — computing sensitivity, gating on it, classifying the issue — is **deterministic, pure, and explainable**. Sensitivity is *computed*, not *judged*.

- **L0 — Plan dependency graph** (LLM-extracted, DL-184 schema; each node/edge carries an **extraction-confidence**). The substrate and the honest floor. Uncertainty in the graph must **propagate**, not be dropped.
- **L1 — Sensitivity engine** (deterministic, pure function of L0). Per candidate element, sensitivity = magnitude of the outcome-integrity span between "confirmed true" and "falsified." **Two-tier for cost:** a cheap structural-leverage pre-filter (elements on outcome-critical paths) → expensive counterfactual recompute only on the near-threshold shortlist. **Uncertainty-aware:** a node whose own dependencies are uncertain scores *more* sensitive, never less (uncertainty compounds toward attention). **Runway-aware:** the plan-stage effect lives here, not in L2 — an unverified load-bearing item scores more sensitive as execution nears (less runway to fix it), per DL-196 §4. Every score decomposes to the paths that produced it.
- **L2 — Calibration gate** (thin, versioned, the *only* place judgment lives). Sensitivity → load-bearing? via a **small parameter set**. **Launch with a single global threshold** (one defensible, auditable number), but build the **hierarchical-shrinkage machinery in from day one, dormant** — every segment fully shrunk to the global prior until validated data moves it (so "segmented at zero data" ≡ "global," no premature commitment to segmentation axes). Distinguish the three things that "segmentation" conflates: **plan-stage → L1** (runway-aware sensitivity, above), **stakes → an explicit owner input** that scales the asymmetric loss / lowers the floor (a declared property and transparent knob, never a learned segment), and **domain base-rate → the only genuinely learned segment**, activated via shrinkage as per-domain labels accrue. Plus a **hard critical-floor** (always surfaced) and a separate **user surfacing-preference offset**. Emits the binary load-bearing flag **and** the continuous exposure rank (DL-193). Auditable config (Demo-Config entries), not scattered code.
- **L3 — Classification derivation** (static canonical table). Load-bearing element + finding-type → (pillar, permitted resolution acts) via the Root-5 lookup, with *only-verify-moves-Grounding* wired in. Deterministic; multi-aspect threats **decompose** into single-classed issues (never dual-classed — matches DL-197 §7).
- **L4 — Feedback / validation loop** (offline, optional, guarded). Improves **L2 parameters only** — never L0/L1/L3, never the invariants. Truth-targeted (outcome- or expert-labeled), **not** acceptance-targeted; holdout / off-policy-corrected against the reflexivity of OSLO influencing its own data; enabled per-segment only on data sufficiency (shrinkage handles the ramp).

**Cross-cutting honesty firewall (guards):** only-verify-moves-Grounding · the load-bearing gate is sensitivity-based, never severity-feel · calibration never suppresses the critical floor · segment/preference calibration never lowers the *honesty* of the read for any segment (DR-7/DL-103) · **at zero data, segmented output must equal the global output** (proves the dormant segmentation is unbiased and that no segment was hand-tuned without evidence) · every surfacing decision is decomposable to its inputs.

**Why the alternatives lose (defensibility):** pure LLM "is this load-bearing?" is opaque/uncalibratable/drifting and breaks decomposability; hand-authored per-finding rules are the ad-hoc `primaryMove` mess itself; a raw LLM severity score is the rejected "by feel." Graph-sensitivity is the *only* option that is principled, computable, calibratable, and fully decomposable — a forced move once "every surfacing decision must be explainable to its inputs" is accepted.

## 4. Named residuals (boundaries, written down — not buried)

- **Graph-quality floor (L0):** sensitivity is only as true as "what rests on what." A permanent modeling problem, not a definitional gap; the primary investment. Mitigated by uncertainty-propagation, asymmetric calibration, and user correction (verify/refute) feeding L4.
- **Cold start / label scarcity:** clean outcome labels are slow and confounded, so L4 improves gradually. The system therefore **ships correct on a conservative expert-set prior with zero feedback data** — learning is an enhancement, never a dependency.
- **Reflexivity:** OSLO's surfacing changes user behavior, which changes outcomes, which is the feedback. Holdouts are **non-negotiable** before L4 is ever allowed to move a threshold.

## 5. Build sequencing (viability)

Ship **L0→L3 with a hand-set, conservative, expert-informed L2 prior**. That alone fixes everything diagnosed in §1 — fully deterministic, defensible, decomposable on day one, no dependency on data you don't have. **L4 (learning)** and **per-segment calibration** are v2 enhancements that snap onto L2 without touching L0/L1/L3 or the invariants. Never blocked on the hard part to get the trustworthy part.

## 6. Review (the five outputs — Framework 001)

- **Findings:** classification + resolution affordance are ad-hoc (`primaryMove`) and decoupled from pillar; this produces the catering incoherence and a latent honesty breach (a fix can raise Grounding). The load-bearing criterion is implicit/subjective. The canon (DL-184/193/196/197) already contains the pieces; they are unformalized and incompletely wired.
- **Concerns:** (a) the graph-quality floor caps false-negative performance; (b) a naive feedback loop optimizing acceptance would train OSLO to suppress its most valuable warnings; (c) over-segmented calibration on thin data overfits; (d) any drift of learning into the invariants or into per-segment honesty would breach DR-7/DL-103 and DL-197. All are mitigated by the design (firewall, offline+optional L4, shrinkage, asymmetric floor) but must be guarded, not assumed.
- **Dependencies:** DL-184 graph (L0); DL-193 exposure (L1/L2 output); DL-196/197 issue layer (L3); Demo-Config register (L2 params); the analysis engine's dependency-model validation (the floor). No R2 freemium-build impact; this is a build-architecture + doctrine spec, not a freemium change.
- **Recommendation:** ratify the five first principles (§2) as canon — especially **Root 2 in the magnitude-with-threshold form with its two named residues**, **Root 4's "only verify moves Grounding,"** and **Root 5's three acts**. Adopt the layered architecture (§3) with the quarantine-the-fuzziness thesis and the cold-start-safe sequencing (§5). Retire the hand-set `primaryMove` in favor of L3 derivation.
- **Status:** PROPOSED — awaiting owner ratification.

## 7. Open for ratification (the specific calls)

1. Ratify Roots 1–5 (§2) as R2 canon; confirm the **only-verify-moves-Grounding** invariant and the act→pillar matrix as guarded invariants.
2. Confirm **load-bearing = magnitude-of-sensitivity ≥ calibrated-threshold** (two-sided), and accept the two named residues (one global auditable threshold; the engine-model-quality floor) as declared boundaries rather than defects.
3. Adopt the **L0–L4 layered architecture** and the **cold-start-safe sequencing** (L0–L3 + static prior first; L4/segmentation as v2).
4. Confirm **decomposition over dual-classing** for multi-aspect issues (per DL-197 §7).
5. **Confirm the threshold strategy:** launch a **single global threshold** with **dormant** hierarchical-shrinkage segmentation (segments = global until data earns them); **plan-stage → L1** (runway-aware sensitivity, DL-196 §4); **stakes → an explicit owner input** (scales the asymmetric loss / floor), not a learned segment; **domain → the only learned segment**; enforce the **zero-data-equals-global** guard. Direct where the L2 threshold + these knobs live in the **Demo-Config register**, and confirm learning (L4) is firewalled from the invariants and from per-segment honesty (DR-7/DL-103).

---

_AI-drafted proposal (Framework 001). The owner ratifies (→ candidate DL-209), amends, or rejects. Realization (build) routes to its own scoping after ratification; this proposal authorizes no build._
