# 60-Second Orientation Workflow Specification v1

**Type:** Workflow specification (user experience / workflow only)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Sits below (authoritative — presents/orchestrates UX, must not modify):** Outcome Confidence Doctrine (Decision/Interpretation/Leadership 001) · CAF Assessment · CAF Scoring v2 · Reliability v2 · Confidence v2 · `FINDING_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · `FINDING_PRESENTATION_SPECIFICATION_V1.md` · `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` · UI Specification §7 · Architecture Audit 001/002 · Release 1 Product Tier Definitions.

> **Non-negotiable.** Workflow/UX only. Defines **no** CAF scoring, Confidence/Reliability calculation, recommendation/finding generation logic, governance, execution, agents, or automation. The Orientation is **informational** — it surfaces existing analysis; **the user decides and acts**, and **only reanalysis changes CAF/Reliability/Confidence**. **Outcome Confidence is trust in understanding — never project health or outcome probability** (Confidence Doctrine); the Orientation must not imply otherwise.

---

## 1. Purpose

The **60-Second Orientation** is the workflow immediately after project intake + analysis. Its goal is to help the user **rapidly understand how trustworthy OSLO's current understanding of the project is, and where attention is most needed** — fast, in one view. It is the surfaced output of the **Fast Analysis Pass** (provisional, with Deep Analysis to follow).

It is **not** for: creating plans, managing execution, performing governance, or automating work.

> **Doctrinal framing (preserved).** Colloquially users ask "is my project healthy / on track?" The Orientation answers the question OSLO can actually answer: **"How much can I trust the current understanding, and what is weakening it?"** It does **not** present confidence as project health, readiness, or likelihood of success (Confidence Doctrine; SOW-7).

## 2. Workflow Overview

```text
Project Intake → Analysis (Fast Pass) → 60-Second Orientation → User Understanding → User Action → Reanalysis → (Updated Orientation)
```

- The Orientation is **informational**: it presents confidence, CAF, reliability, findings, and recommendations from the completed analysis.
- **The user decides what to do.** Acting (update info / accept-defer-reject a recommendation) produces information change → reanalysis → an updated Orientation.
- The Orientation is **provisional** (Fast Pass); Deep Analysis continues and supersedes it (Confidence may rise or fall as understanding deepens).

## 3. User Goals (the questions the Orientation answers)

- **"Can I trust what OSLO understands about my project?"** → Outcome Confidence (reliability-qualified). *(Not "is the project healthy?" — see §1.)*
- **"What should I focus on first?"** → Top Findings (by severity) and OSLO Recommended.
- **"Why is confidence where it is?"** → Confidence explanation (CAF + Reliability basis).
- **"What findings matter most?"** → Top Findings, organized by CAF dimension/severity.
- **"What recommendations should I consider?"** → OSLO Recommended + Possible Resolution Paths.

## 4. Information Hierarchy

**Display order (canonical):**
1. **Outcome Confidence** — the summarized, reliability-qualified trust signal (the headline).
2. **CAF Assessment** — Clarity / Alignment / Feasibility (what drives confidence).
3. **Reliability** — how well-supported the assessment is (qualifies confidence).
4. **Top Findings** — what is weakening understanding (the actionable observations).
5. **Top Recommendations** — OSLO Recommended + Possible Resolution Paths (advisory).
6. **Project Summary** — key observations / context.

**Justification:** confidence is the headline the user came for; CAF explains *why* it sits there; Reliability qualifies *how much to trust that judgment*; Findings make the weaknesses concrete; Recommendations offer the advisory path; the Summary grounds it. This mirrors the assessment chain (Finding → CAF → +Reliability → Confidence) **in reverse** — signal first, basis on the way down — which is the natural comprehension order and matches progressive disclosure (§6).

## 5. Orientation Screen Layout (canonical; no wireframes/implementation)

- **Header:** Project Name · Last Analysis Timestamp · *(provisional/"Deep Analysis in progress" indicator while applicable)*.
- **Outcome Confidence Section:** Confidence (with its **reliability qualifier**, never bare) · Confidence Band (Very Low…Very High) · Confidence Explanation (CAF + Reliability basis; cause-of-level).
- **CAF Section:** Clarity · Alignment · Feasibility — each with its per-dimension reliability qualifier; Alignment/Feasibility marked **preliminary** in the Fast Pass.
- **Reliability Section:** Reliability level (High/Moderate/Low) · Reliability Explanation (Coverage / Evidence Availability / Assessability basis).
- **Findings Section:** Top Findings (grouped by CAF dimension, severity-ordered, per Finding Presentation Spec) — entry point to the full Findings experience (§7).
- **Recommendations Section:** **OSLO Recommended** · **Possible Resolution Paths** (grouped Recommendations, presentation-only) — entry point to the Recommendation experience (§8).
- **Project Summary Section:** key observations.

## 6. Progressive Disclosure

- **Visible immediately (top-level):** Outcome Confidence (+ reliability qualifier), CAF (the three dimensions), Reliability.
- **Expands on demand:** Top Findings, Top Recommendations, and the supporting rationale (confidence explanation, CAF/reliability basis, finding evidence, recommendation rationale).
- The headline trust signal and its drivers are immediate; the detailed basis and the actionable lists are one interaction away — keeping the "60-second" read fast while preserving full explainability.

## 7. Finding Experience Entry Point

From the Findings Section, the user opens the **full Findings experience**, which MUST align with `FINDING_PRESENTATION_SPECIFICATION_V1.md`: findings presented as **descriptive** cards, grouped by **CAF dimension** with severity ordering, finding-anchored, explainable, with Recommendations nested beneath. The Orientation surfaces the **top** findings; the Findings experience shows the full set.

## 8. Recommendation Experience Entry Point

From the Recommendations Section, the user opens the **Recommendation experience**, which MUST align with `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md`: **OSLO Recommended** shown first (advisory, no score), other recommendations grouped as **Possible Resolution Paths** (presentation-only over multiple Recommendations), with **Selected Path** = the accepted one. Recommendations are advisory, never commands.

## 9. User Actions (Release 1 only)

- **View Finding** · **View Recommendation** (read/explore).
- **Accept Recommendation** · **Reject Recommendation** · **Defer Recommendation** (`deferred`, per Data Model v1.2 / State Model).
- **Update Project Information** (add/edit evidence/artifacts).
- **Trigger Reanalysis** (where applicable; otherwise reanalysis is event-driven on information change).

**Not available:** execution actions, agent actions, autonomous application, governance actions. **Only the user acts; OSLO advises.**

## 10. Reanalysis Workflow

```text
User Action → Information Change → Reanalysis → Updated Orientation
```
- Accepting/deferring/rejecting a recommendation, or acting on it, may produce an **information change**; **information change** drives **reanalysis** (event-driven; triggers owned by the Event Model — not defined here).
- **Only reanalysis changes CAF, Reliability, or Confidence.** Viewing, accepting, deferring, or selecting — by themselves — change **no** assessment signal. The updated Orientation reflects the reanalyzed state (which may supersede the prior, with Confidence rising or falling honestly).

## 11. Tier 1 Experience (Freemium)

Per **Release 1 Product Tier Definitions** (referenced, not redefined here; **no pricing/quotas defined**): Tier 1 provides the **full Orientation read** — Outcome Confidence, CAF, Reliability, Top Findings, OSLO Recommended + Possible Resolution Paths, and explainability — with **limited** active project capacity, recommendation interactions, and reanalysis volume. The **understanding experience is complete**; the limits are on scale/volume (defined in the Tier Definitions).

## 12. Tier 2 Experience (Basic)

Per **Release 1 Product Tier Definitions**: Tier 2 is **additive** — more recommendation interactions, more reanalysis volume, and greater project capacity, plus richer explainability/history surfaces. It introduces **no execution, automation, agent, or governance** capability; it scales the **same** Orientation workflow. Exact boundaries live in the Tier Definitions.

## 13. Integrity Rules

- **SOW-1.** The Orientation is **informational** — it surfaces existing analysis; it computes/decides nothing.
- **SOW-2.** The Orientation **performs no actions**; only the user acts.
- **SOW-3.** **Findings remain descriptive** in the Orientation (never framed as actions).
- **SOW-4.** **Recommendations remain advisory** (OSLO Recommended is a suggestion, not a command; no score shown).
- **SOW-5.** **Possible Resolution Paths** are presentation-only over multiple Recommendations (no object/field).
- **SOW-6.** **Only reanalysis changes CAF/Reliability/Confidence**; no Orientation interaction alters an assessment signal.
- **SOW-7.** Outcome Confidence is presented as **trust in understanding, reliability-qualified** — **never** as project health, readiness, or outcome probability/percentage.
- **SOW-8.** The Orientation is **provisional** (Fast Pass) — its non-final nature is communicated; Deep Analysis supersedes it, and a confidence change (including a decrease) is honest improvement, not deterioration.
- **SOW-9.** The information hierarchy (§4) is preserved: Confidence → CAF → Reliability → Findings → Recommendations → Summary.
- **SOW-10.** No execution, agent, automation, governance, or Future-Architecture affordance appears.

## 14. Conformance Requirements

A conforming implementation MUST (objective, structural, **non-numeric**):
- **SOW-C1.** Present the §4 hierarchy in order, with Outcome Confidence as the headline (SOW-9).
- **SOW-C2.** Always show Confidence **with its reliability qualifier**; never bare; never as health/probability (SOW-7).
- **SOW-C3.** Surface CAF (3 dimensions) and Reliability with their explanations on demand (progressive disclosure, §6).
- **SOW-C4.** Present Top Findings per the Finding Presentation Spec and Top Recommendations per the Recommendation Presentation Spec (§7/§8).
- **SOW-C5.** Expose only the §9 user actions; expose **no** execution/agent/governance action (SOW-2/SOW-10).
- **SOW-C6.** Ensure no Orientation interaction (view/accept/defer/reject/select) changes any CAF/Reliability/Confidence signal; only reanalysis does (SOW-6).
- **SOW-C7.** Communicate the Orientation's **provisional** nature (Fast Pass; Deep to follow) (SOW-8).
- **SOW-C8.** Keep findings descriptive and recommendations advisory throughout (SOW-3/SOW-4); Possible Resolution Paths presentation-only (SOW-5).

Conformance is **all-or-nothing**; any action affordance beyond §9, any assessment change from a non-reanalysis interaction, any confidence-as-health/probability framing, any bare confidence, or any governance/execution affordance **fails conformance**.

## 15. Deferred Items

Explicitly **deferred** (out of scope): execution workflows · governance workflows · agents · automation · future orchestration capabilities · the numeric tier boundaries (owned by Release 1 Product Tier Definitions) · calibration values (owner track).

---

*This specification defines the canonical Release 1 60-Second Orientation workflow: an informational, provisional, reliability-qualified read of Outcome Confidence, CAF, Reliability, Top Findings, and advisory Recommendations, from which the user understands and acts — with only reanalysis changing assessment. It defines no scoring, calculation, generation logic, governance, execution, agents, or automation, and preserves the doctrine that confidence is trust in understanding, not project health or outcome probability.*

**60-Second Orientation Workflow Specification v1 complete.**
