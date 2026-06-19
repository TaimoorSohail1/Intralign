# Escalation — May a Third-Party Evaluation Lens Influence Evaluate/Advise, and Under What Governance?

- **Status:** **RESOLVED — DL-079** (2026-06-19): owner ratified the boundary — a lens is **governed input to first-party cognition, never third-party cognition**; it may surface attributed, confidence-qualified considerations but **never alters CAF/scores and never disposes** (OB-5). **Reference-only (A) first; governed overlay (B) north-star; Option C (scoring contribution) fenced as a separate future doctrine decision.** CAF stays first-party. This document is retained as the decision analysis; the ratified decision is `00_owner/decisions/records/DL-079-e4-lens-cognition-boundary.md`. **E4 remains design-only** until its realization is proposed under this boundary.
- **Source:** 2026-06-19 ecosystem brainstorm; `BACKLOG_ECOSYSTEM_MARKETPLACE_AND_CREATOR_PROGRAM` §E4 (NORTH-STAR, governance-gated). Owner direction 2026-06-19 to draft the escalation.
- **Gates:** E4 (evaluation lenses / domain rubrics); the domain-pack bundle (E6 = artifact set + templates + reference + **a governed lens**); and, by extension, the credibility of OSLO's **governed-cognition trust differentiator**.
- **Layer:** Touches the **governed epistemic core** (Evaluate · Advise) — therefore **doctrine**, not implementation. Precedence: Doctrine > Constitution > Implementation; this question sits at the top of that ladder.

---

## 1. The question

A domain expert's **"what good looks like / what risks to watch"** for a plan type (a *lens* / rubric) is the deepest value and deepest moat in the ecosystem. The backlog frames it as a **governed Derived lens** — "OSLO controls application; confidence-qualified; transparently attributed ('flagged per *[Expert]*'s lens')." But that framing contains an unresolved doctrine question:

> **Does a third-party lens *influence the assessment* (OSLO's CAF / confidence / Issues / Recommendations), or does it only *inform the user* as attributed reference surfaced by Disclose — and if it may influence, under what governance does third-party content touch the governed epistemic core without violating it?**

This is **the** structure↔cognition boundary crossing. Every other ecosystem capability (E1 templates, E6 artifact schema) is **structure** — Attested on adoption (DL-056), epistemically safe. **E4 is the one capability that crosses into cognition (L3).** That crossing is an **owner + doctrine decision**, not an engineering choice.

## 2. What the canon fixes vs. leaves open

**Fixed (binding — any answer must preserve):**
- **Attested vs Derived.** OSLO's assessments are **Derived** cognition the engine controls; only the **user's** input is Attested. A third party is neither — so a lens is *neither* Attested truth *nor* OSLO's own Derived cognition. Its epistemic status is **undefined** today.
- **OB-5 — only reanalysis changes assessment.** Nothing (clarifications, collaboration, adoption) silently changes an assessment except OSLO's own recompute.
- **"Advise proposes, never disposes."** Advise emits **candidate** Recommendations/Clarifications/Suggested Fixes; the human disposes. Human authority at evaluative steps is **deliberately preserved** (the architecture keeps Human Evaluation external).
- **CAF is first-class and first-party** (Clarity / Alignment / Feasibility — DL-062); drivers stay decomposable; confidence is never a probability.
- **No fabricated assessment / honest-limit disclosure** — OSLO must not present judgment it cannot ground.

**Open (the escalation):** whether — and how — a **non-OSLO, non-user** party may contribute to Evaluate/Advise; the **epistemic status** of a lens; whether CAF is **extensible** by lenses or strictly first-party; the **certification/calibration/audit** regime; and the **attribution/liability** surface of named third-party flags.

## 3. Why it matters (the opportunity *and* the risk)

- **Opportunity:** lenses are the **highest outcome-value, deepest-moat** capability — governed domain expertise, a supply-side network effect, per-domain calibration. They turn OSLO from a planning product into a **governed domain-expertise platform**.
- **Risk:** the moat and the **trust differentiator are the same asset** — "the marketplace that *can't* manipulate your judgment." If a third party can silently bias an assessment, OSLO forfeits exactly the governed-cognition trust that is its wedge. **The boundary must be drawn so the moat does not eat the differentiator.**

## 4. Options (for owner + doctrine decision — AI does not choose)

- **Option 0 — Forbidden.** Third parties never touch Evaluate/Advise; E4 is dropped. *Maximally safe; forgoes the deepest moat.*
- **Option A — Reference-only (Disclose-class).** A lens surfaces as **attributed advisory reference** ("considerations *[Expert]* flags for this plan type") via the **Disclose/Chat surface** — it **never enters CAF/confidence/scoring**. It informs the *user*, not the *assessment*. *Safe (it is E3-like reference, not cognition); preserves OB-5 and "advise proposes" trivially; the question becomes whether that is "influence" enough to be worth E4's billing.*
- **Option B — Governed Derived overlay.** OSLO **applies** the lens as its own **Derived, confidence-qualified, attributed** overlay: the lens may cause OSLO to **raise a flag / consideration / candidate Issue**, but it **cannot alter CAF/confidence values** and **never disposes** — it proposes considerations the OSLO engine and the human adjudicate. *The lens is **data the governed engine reads**, not logic a third party runs.* The likely north-star that keeps the differentiator intact.
- **Option C — Certified scoring contribution.** A **certified** lens contributes to **Evaluate scoring itself** (e.g., a domain-calibrated CAF/Issue weighting) under heavy governance (calibration, audit, confidence-attribution). *Most powerful; highest risk; this is the option that most directly tests OB-5 / human-authority doctrine and would require an explicit doctrine extension.*

## 5. Binding constraints any chosen option must preserve

1. **Derived, never Attested** — a lens is never recorded as truth; OSLO controls all application.
2. **Never silent** — every lens effect is **attributed** (named) and **confidence-qualified**; no anonymous or hidden influence.
3. **OB-5 holds** — a lens does not *change* an existing assessment except through OSLO's governed recompute (CHR-tracked).
4. **Advise proposes, never disposes** — a lens may propose considerations; it never makes or finalizes a judgment; the human retains authority.
5. **CAF integrity** — unless the owner explicitly extends doctrine (Option C), CAF/confidence/scoring stay **first-party**; lenses add considerations *around* the scores, not *into* them.
6. **No fabricated assessment / honest limits** — a lens never lets OSLO present grounding it lacks.
7. **Calibration before influence** — any lens that can flag must be **validated/calibrated and auditable** before it is allowed to.

## 6. Recommendation (AI — owner + doctrine ratifies; this resolves nothing)

- **Adopt the boundary as: a lens informs through a governed, attributed, confidence-qualified channel and never silently disposes** — i.e., **Option A as the safe first step and Option B as the north-star target**, with **Option C explicitly fenced as a separate doctrine question** the owner must open deliberately (it is the only option that puts third-party content *inside* the scoring).
- **Decide the epistemic status of a lens first** (it is the keystone): naming it a **Derived overlay OSLO applies** (Option B) — *not* a third-party assessment — is what keeps the whole thing inside the governed model. Recommend defining a lens as **governed input data to first-party cognition**, never as cognition a third party performs.
- **Design the boundary now, build last** (per the backlog): ratifying the boundary unblocks E6 design (domain packs bundle a lens) without authorizing any E4 build.
- **AI recommends a direction for evaluation only; the owner ratifies the doctrine.** Engineering authors no E4 realization until the boundary is ratified.

## 7. Sub-questions the owner decision should settle

1. **Influence vs inform** — may a lens affect the assessment (Option B/C), or only annotate for the user (Option A)?
2. **Epistemic status** — is a lens "governed input data to first-party cognition," or something new requiring a doctrine term?
3. **CAF extensibility** — strictly first-party (recommended), or extensible by certified lenses (Option C, doctrine extension)?
4. **Certification/calibration/audit** — the bar an author and a lens must clear before it may flag (DL-049 external `Principal`).
5. **Attribution & liability** — named flags carry an expert's reputation and a legal surface; how is that bounded?
6. **Relationship to the artifact-profile registry** — a lens likely attaches to artifact modules (`ARTIFACT_PROFILE_MECHANISM_REALIZATION_DESIGN_001`); is the registry the lens substrate, under the same governance?

## 8. Framework 001A Review

- **Findings:** E4 is the single ecosystem capability that crosses the structure↔cognition boundary; its core unknown is whether a lens **influences** or only **informs**, and the epistemic status of the lens. The binding constraints (Attested/Derived, OB-5, advise-proposes-never-disposes, CAF first-party, no-fabricated-assessment) are clear and admit a safe design (Option A/B); Option C alone would require a deliberate doctrine extension.
- **Concerns:** the moat and the trust differentiator are the same asset — a wrong boundary forfeits the wedge. "Governed Derived lens" is under-defined until the owner fixes the lens's epistemic status. Attribution carries a real reputational/legal surface. CAF integrity must be protected against silent third-party weighting.
- **Dependencies:** DL-062 (CAF), DL-047 (Evaluate seeds CAF/Confidence), DL-049 (`Principal` — lens authors as external principals), OB-5, the ecosystem boundary principle (E4 backlog), E6 (domain-pack bundle), and `ARTIFACT_PROFILE_MECHANISM_REALIZATION_DESIGN_001` (the registry a lens may attach to).
- **Recommendation:** **Ratify the boundary** — lens = governed, attributed, confidence-qualified input that never silently disposes (Option A now / Option B north-star; Option C fenced as a separate doctrine question). Settle the §7 sub-questions, starting with the lens's epistemic status. **Build nothing until ratified.** AI recommends; owner + doctrine ratifies.
- **Status:** OPEN — escalated; E4 remains design-only pending owner + doctrine ratification of the boundary.

## 9. Owner decision required (summary)

1. **Influence or inform?** — set the boundary (Option 0 / A / B / C).
2. **Epistemic status of a lens** — adopt "governed Derived input to first-party cognition" (recommended), or open a doctrine term?
3. **CAF** — first-party only (recommended), or certified-lens-extensible (a deliberate doctrine extension)?
4. **Governance regime** — certification/calibration/audit bar + attribution/liability bounds; and whether the artifact-profile registry is the lens substrate.

---

*This escalation surfaces — without resolving — the one ecosystem question that touches OSLO's governed epistemic core: whether a third-party evaluation lens may influence Evaluate/Advise or only inform the user, and under what governance third-party content can touch cognition without breaking it. It records what the canon fixes (Attested/Derived, OB-5, "advise proposes never disposes," first-party CAF, no fabricated assessment) and what it leaves open (the lens's epistemic status, CAF extensibility, certification, attribution/liability), lays out an option spectrum from "forbidden" to "certified scoring contribution," states the binding constraints any answer must preserve, and recommends — for owner-and-doctrine ratification only — drawing the boundary so a lens is governed, attributed, confidence-qualified input that never silently disposes, with the scoring-contribution option fenced as a separate doctrine question. It introduces no doctrine and resolves no ontology unilaterally; E4 stays design-only until the owner ratifies the boundary.*
