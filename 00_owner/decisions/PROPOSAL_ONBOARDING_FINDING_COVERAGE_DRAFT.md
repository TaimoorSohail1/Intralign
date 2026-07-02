# Proposal (DRAFT) — Minimum orientation finding-coverage via grounded gap-detection

> **DRAFT for owner ratification.** AI-drafted under Framework 001A (analysis / consistency checking / conflict identification / recommendation only). The owner ratifies; AI does not author canon or set numeric thresholds. Owner directed this draft (2026-07-02).

- **Type:** Framework 001 — Proposal + 001A Review (five outputs).
- **Layer touched:** synthesis / understanding contracts (`20_handoff/contracts` — Wave S / Wave B) + the Fast-Pass stage spec (`30_engineering/analysis_engine`). **No doctrine change; no new epistemic invariant.**

## 1. Problem

At onboarding, a user must see a **material** number of findings to trust that OSLO understood their project — even when the brief is **sparse**. Today the orientation surfaces few findings (~6–8 in the demo templates), and a disproportionate share are **inferred**. Two failure modes follow: (a) too little to engage with, and (b) with the DL-093 basis tags now visible, a wall of `inferred` findings reads as *"OSLO is guessing,"* undercutting trust.

## 2. The wrong lever, and the right one

**Wrong lever — infer more.** Raising inferred-finding output would violate the grounding invariant (Wave B: "anchor each Finding to its Attested evidence"; Wave S: "silent gap-filling" is forbidden), lower **Reliability**/**Confidence** (inference is self-penalizing by design), risk fabrication, and advertise thinness via the `inferred` basis tag.

**Right lever — grounded gap-detection, which scales *up* with sparseness.** A sparse brief does not have fewer issues; it fails more **completeness checks**. The Fast Pass already does a "coverage-gap set-difference vs the 8 artifact types." Those `coverage_gap` / `missing_information` / `ambiguity` findings are **structurally grounded** — the *absence* is the finding, anchored to the expected-artifact framework, not to an inference. So a sparse project should honestly yield a **large, mostly-grounded** finding set, with inference as a bounded minority.

**Illustration (realized in the prototype, this session):** the DevNorth sample was expanded from 6 to **15** findings for the same sparse brief — **10 grounded / 5 inferred**, spread across Clarity/Alignment/Feasibility — by running completeness checks per artifact (missing budget, no milestones, no risk register, no decision owner, undefined success threshold, unspecified audience, …). Density rose **and** the grounded:inferred ratio improved. Baseline `03-findings`.

## 3. Proposed specification (owner ratifies; thresholds owner-set)

1. **Orientation coverage rule.** The Fast-Pass / Infer synthesis runs a **grounded gap-detection matrix** — each of the 8 artifact types × the CAF dimensions × a **standard completeness-criteria set** (e.g., owner assigned · measurable success criteria · dependencies/milestones · budget/cost · risks/contingency · audience/scope boundaries). Each unmet criterion is a **grounded** finding (`coverage_gap` / `missing_information` / `ambiguity`), anchored to the expected-artifact framework.
2. **Density expectation, not fabrication.** Onboarding surfaces a **material** finding set sufficient for orientation; the number is an *outcome* of the completeness matrix, never a quota met by inventing findings. Sparser input → more grounded gaps (and correspondingly lower Reliability/Confidence — honest).
3. **Inference stays a bounded minority.** Inferred findings remain explicitly flagged (`basis = inferred`, DL-093) and should be the **minority** of the orientation set; grounded findings dominate. (Owner sets any target ratio / floor.)
4. **Standard completeness-criteria set** is owner-ratified config (extensible), not hard-coded — so "what counts as complete" is governed, not invented (Anti-Assumption).

## 4. Review (Framework 001A — five outputs)

**Findings.**
1. The mechanism already exists (coverage-gap set-difference; finding types include `coverage_gap`/`missing_information`) — this **strengthens and specifies** it, adding the completeness-criteria matrix and a density expectation.
2. Grounded gap findings are honest and scale with sparseness; they do not rely on inference and do not depress trust.
3. The prototype demonstrates the density is achievable within the grounding invariants.

**Concerns.**
1. **Noise vs signal** — a large gap set must stay **severity-ordered and dimension-grouped** (Finding Presentation §D/§E) so onboarding isn't overwhelming; "Start here" still surfaces the top item.
2. **Completeness-criteria authorship** — the criteria set is an owner decision; AI must not invent "what a complete plan requires" (escalate, per Anti-Assumption).
3. **Cost** — more detection is token/compute; must stay within the DL-048 per-tier budget (graceful degradation → partial coverage, deferred to Deep).
4. **No fabrication** — the rule must never be read as "hit a finding quota"; density is an *outcome* of grounded checks.

**Dependencies.**
- `WAVE_S_CONTRACT_PACKAGE_SYNTHESIS_ENGINE` (DL-047) · `WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING` (Infer finding grounding) · `FAST_PASS_STAGE_IO_SPEC` (coverage-gap detection; finding-type enum) · `RELEASE_1_EPISTEMIC_STATE_MODEL_DECISION_001` (grounding / Disclose) · DL-093 (basis tags) · DL-046 (Fast/Deep) · DL-048 (cost governance) · RB-033 (finding-type taxonomy). Reliability model (coverage/evidence/assessability) reflects the grounded-vs-inferred mix.

**Recommendation.**
**Accept** an orientation-coverage rule driven by a **grounded completeness-criteria matrix**, with inference a bounded minority and all numeric thresholds (criteria set, density floor, grounded:inferred target) **owner-set**. Amend the Wave S / Wave B synthesis contracts + Fast-Pass spec accordingly. No new epistemic invariant; no fabrication.

**Status.**
**DRAFT — recommended: Accept (rule); thresholds owner-set.** Owner ratification required (001A — AI may not ratify or set the numbers).

## 5. Open questions for the owner
1. The **standard completeness-criteria set** per artifact type (what "complete enough for orientation" means).
2. A **density floor** and/or **grounded:inferred target** for the orientation set (if any).
3. Whether this is R1 (tighten now) or an Alpha-tuning item refined from telemetry.

## Provenance

Owner concern 2026-07-02 (onboarding needs material findings even on sparse input; current output leans on inference). AI grounded the mechanism in the synthesis/understanding contracts + Fast-Pass spec, showed the honest density lever is grounded gap-detection (demonstrated in the prototype, `03-findings`, 15 findings / 10 grounded), and drafted this rule. Recommendation only; owner ratifies and sets thresholds. Numbered at landing (DL-065).
