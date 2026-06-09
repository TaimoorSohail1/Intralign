# Recommendation Presentation Specification v1

**Type:** User Experience / Presentation specification
**Status:** Active Release 1 · **Date:** 2026-05-31
**Sits below (authoritative — presents, must not modify):** `FINDING_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md` · `RECOMMENDATION_OPTION_MULTIPLICITY_RECONCILIATION_V1.md` (+ `…RECONCILIATION_DECISION_001.md`) · CAF Scoring v2 · Reliability v2 · Confidence v2 · UI Specification.

> **Non-negotiable.** This is a **presentation** spec. It does **not** modify recommendation behavior, lifecycle, Finding/Recommendation models, or CAF/Reliability/Confidence; introduces **no** new objects, states, events, governance, automation, or agents. It assumes the **ratified architecture**: a Finding has **multiple Recommendations**; **Possible Resolution Paths**, **OSLO Recommended**, and **Selected Path** are **UI rendering labels over those Recommendations**, not modeled constructs. Recommendations are **advisory, never commands**; Findings are descriptive; assessment changes only via reanalysis. No scoring/ranking arithmetic or calibration values are introduced.

---

## A. Recommendation Presentation Principles

**Goals.**
- **Understandable** — a user grasps *what* the recommendation proposes and *why* at a glance.
- **Actionable** — the user can see what acting would involve, and act (the user acts; OSLO advises).
- **Explainable** — every recommendation reveals its basis on demand (source findings, rationale, affected dimensions).
- **Prioritization visible** — OSLO's suggested primary option is clearly distinguished from alternatives, without implying a score.

**Establishing rules.**
- Recommendations are presented as **advice**, **never as commands** or instructions.
- Recommendations never imply autonomous action; the **user decides and acts**.
- Presentation is **finding-anchored** — recommendations are shown in the context of the finding(s) they address.
- Presentation uses **progressive disclosure** — a concise card first, full explainability on expand.

---

## B. Recommendation Hierarchy

**Canonical presentation hierarchy:**
```text
Project
 └─ Finding
     ├─ OSLO Recommended            → the primary Recommendation (derived from prioritization, Rec System §7)
     └─ Possible Resolution Paths   → the remaining Recommendation(s) for that Finding
```

- **Recommendations appear beneath Findings.** A recommendation is always shown in the context of its source finding(s).
- **Recommendations do not exist outside Findings** in the UI — every recommendation traces to ≥1 finding (Rec System REC-1); there is no "orphan recommendation" surface.
- **Multiple recommendations for one finding are grouped** under that finding: the primary as **OSLO Recommended**, the rest under **Possible Resolution Paths**. This grouping is a **view**, not a new object.
- A recommendation addressing **multiple findings** appears under each relevant finding (or in a shared cluster), consistently labeled; it is the same recommendation, not duplicated.

---

## C. OSLO Recommended Presentation

- **Selection for display.** The **OSLO Recommended** item is the Recommendation OSLO presents as **primary**, derived from the **conceptual prioritization** (Rec System §7: CAF impact → dependency influence → confidence influence → effort). **No score, percentage, or ranking number is shown or computed** — the primary is simply the top of the conceptual order; if no clear primary exists, none is marked.
- **Visual distinction.** The OSLO Recommended recommendation is **visually emphasized** (e.g., a distinct "OSLO Recommended" label/treatment) and shown **first** in the finding's recommendation group.
- **Canonical label:** **"OSLO Recommended."**
- **Collapsed state.** Shows the recommendation card essentials (§E default layout) with the OSLO Recommended label.
- **Expanded state.** Reveals full explainability (§F) and any history.
- **Advisory framing.** The label conveys *OSLO suggests this*, never *do this* — it is the recommended **option**, not a directive.

---

## D. Possible Resolution Paths Presentation

- **Canonical label:** **"Possible Resolution Paths."**
- **What it is.** The presentation grouping of the **other Recommendations** for the same Finding (alongside the OSLO Recommended one). **These are Recommendations — not separate objects, not separate lifecycle entities.**
- **Ordering.** Listed in the **conceptual prioritization order** (Rec System §7) beneath the OSLO Recommended item — **no numeric rank or score** displayed.
- **Grouping.** All alternatives for a single finding are grouped together under "Possible Resolution Paths"; alternatives never float free of their finding.
- **Display rules.** Each alternative renders as a recommendation card (§E). The user may act on **any** of them, including a non-primary one (the chosen one becomes **Selected Path**, §G).
- **Expand/collapse.** "Possible Resolution Paths" may be **collapsed by default** (showing a count, e.g., "2 more possible resolution paths") and **expanded** to reveal the alternative cards — progressive disclosure to keep the OSLO Recommended item prominent.

---

## E. Recommendation Card Specification

**Required fields (default card):**
- **Title** — the recommendation's short label.
- **Recommendation type** — the type (presented in user-friendly form).
- **Rationale** — concise "why."
- **Affected CAF dimensions** — which of Clarity / Alignment / Feasibility it aims to improve.
- **Effort** — qualitative **Low / Medium / High** (no numeric cost).
- **Lifecycle state** — the recommendation's current state (§G), as a status indicator.

**Optional fields (revealed on expand):**
- Artifact references · finding references · recommendation history.

**Layouts.**
- **Default card** — title, type, a one-line rationale, affected dimensions, effort, state; OSLO Recommended badge if primary.
- **Expanded card** — full rationale, affected dimensions detail, source findings, expected impact, history/supersession (§F).
- **Mobile** — single-column card; essentials above the fold (title, OSLO Recommended badge, state, primary action); details on tap-to-expand.

*No scores, percentages, or computed magnitudes appear on a card; effort and dimensions are qualitative.*

---

## F. Recommendation Explainability Presentation

Users can access (progressive disclosure):
- **Source findings** — the finding(s) the recommendation addresses (links into finding detail).
- **Rationale** — the full explanation of why it was generated.
- **Affected dimensions** — the CAF dimension(s) it targets.
- **Expected impact** — structural (e.g., "addresses the ambiguity in F; expected to improve Clarity") — **no magnitudes**.
- **Recommendation history** — prior states.
- **Supersession history** — the recommendation it superseded / was superseded by (retained, never deleted).

**Presentation rules.**
- **Progressive disclosure** — the card shows essentials; an **expanded view** shows the full basis.
- **Traceability** — from any recommendation the user can reach its source finding(s) and, from there, the evidence — and can reach the recommendation's superseded history. **No recommendation is opaque** (Rec System REC-5).
- Explainability reduces to **basis** (findings + rationale + dimensions), never to a number.

---

## G. Recommendation State Presentation

States visualized (definitions owned by Rec System §8 / ratified enum — **not modified here**; RS-R naming reconciliations pending):

| State | Visibility | User affordance |
|---|---|---|
| **Generated** | shown as new/available | view, expand |
| **Accepted** | shown as accepted (this is the **Selected Path** if it's the user's chosen one) | view; proceed to act |
| **Rejected** | de-emphasized / moved to a "dismissed" group | view; may re-surface only via new generation |
| **Deferred** | shown as deferred (set aside, still valid) | view; re-engage later |
| **Implemented / Completed** | shown as acted-upon | view; success is determined downstream by reanalysis, not by this state |
| **Superseded** | collapsed into history (retained) | view in history; links to the superseding recommendation |

**Presentation rules.**
- **History treatment** — superseded/rejected recommendations are **retained and viewable in history**, never deleted (append-only).
- **Selected Path** — the **Accepted** recommendation the user chose is labeled **"Selected Path"** in the UI; it may differ from the **OSLO Recommended** one (recommended ≠ selected).
- **Completed ≠ success** — the UI must not present "Completed/Implemented" as "the problem is solved"; success is shown only when reanalysis weakens/removes the source finding (§J finding-resolved).
- This section **visualizes** states; it **does not define or change** them.

---

## H. Finding Integration

- **Finding detail view.** Shows the finding (descriptive) followed by its recommendation group: **OSLO Recommended** first, then **Possible Resolution Paths** (collapsible).
- **Finding card (in lists).** Shows the finding summary plus a **recommendation count** (e.g., "3 possible resolution paths") and an indicator if an OSLO Recommended item exists; does **not** expand all recommendations inline.
- **Finding lists.** Findings are the primary entries; recommendations are reached by opening a finding.
- **Grouping rules.** **One finding → many recommendations**, always grouped under that finding; the OSLO Recommended item is the group's primary. A recommendation spanning multiple findings is shown consistently under each.
- **Recommendation count behavior.** Counts reflect **active** recommendations (superseded/rejected live in history, not the headline count).

---

## I. Tier Presentation Rules

*(Presentation/interaction only — no execution.)*

- **Tier 1 (Freemium).** Users can **view findings and their recommendations**, see the **OSLO Recommended** item and **Possible Resolution Paths**, **expand** for explainability, and **select/accept** a recommendation (Selected Path). Core advisory experience is fully visible.
- **Tier 2 (Basic).** Adds **richer presentation/interaction** — e.g., fuller recommendation history/supersession views, broader recommendation availability per project, and expanded explainability surfaces. *(Exact tier boundaries are a product/monetization decision; this spec only states that Tier 2 is additive presentation/interaction, introducing **no execution, automation, or new objects**.)*

No tier introduces autonomous action; in **every** tier, **only the user acts**.

---

## J. Empty States

- **No recommendations (yet).** Finding shown with a neutral "No recommendations yet" state — never implying the finding is unimportant.
- **Recommendation generation pending.** A non-blocking "Generating recommendations…" indicator while analysis/reanalysis runs; no fabricated content.
- **Recommendation superseded.** The active surface shows the current recommendation; superseded ones are in history with a link from the current item.
- **Finding resolved.** When reanalysis weakens/removes the finding, present it as **resolved** (success), with its recommendations moved to history; do **not** present an unresolved finding as resolved merely because a recommendation was Completed.

---

## K. Accessibility & Mobile Considerations

*(High level; no implementation details.)*
- **Mobile.** Single-column, card-based; OSLO Recommended and state above the fold; Possible Resolution Paths collapsed by default; tap-to-expand for explainability.
- **Responsive.** Reflows from multi-pane (desktop) to single column (mobile) without loss of function; recommendation grouping under findings preserved at all sizes.
- **Accessibility.** Keyboard-navigable cards/actions; screen-reader-labeled state, OSLO Recommended, and Selected Path; **state and emphasis conveyed by label/icon, not color alone**; predictable focus on expand/collapse and on event-driven updates.

---

## L. Recommendation Presentation Integrity Rules

*Objective, testable presentation rules.*

- **PRES-1.** Recommendations are presented **beneath their Finding(s)**; no recommendation is shown without its finding context.
- **PRES-2.** Recommendations are **attributable** in the UI — the user can reach their source finding(s) and basis.
- **PRES-3.** Recommendations are **explainable** in the UI — no opaque recommendation; full basis on expand.
- **PRES-4.** Recommendations **never appear as commands** or instructions; framing is advisory.
- **PRES-5.** Presentation **never implies autonomous action** — only the user acts; no "OSLO will do this" affordance.
- **PRES-6.** **OSLO Recommended** marks the primary recommendation (derived from conceptual prioritization), shown **without** any score/rank number.
- **PRES-7.** **Possible Resolution Paths** are presented as **Recommendations** (a grouping/view), **never** as separate objects, lifecycles, or entities.
- **PRES-8.** **Selected Path** reflects the user's accepted recommendation and **may differ** from OSLO Recommended.
- **PRES-9.** Recommendation **states are visualized** per §G **without altering** lifecycle definitions; superseded/rejected are retained in history (append-only).
- **PRES-10.** **Completed/Implemented is not presented as success**; success is shown only on finding resolution via reanalysis.
- **PRES-11.** Presentation introduces **no new object/state/event** and **no CAF/Reliability/Confidence change**; selecting a recommendation changes no assessment signal.
- **PRES-12.** No governance/agent/automation affordances appear in any recommendation surface.

---

## M. Conformance Requirements

A conforming UI MUST (objective, **non-numeric**, no pass-rate language):
- **C-1.** Render recommendations grouped under their finding(s), with **OSLO Recommended** first and **Possible Resolution Paths** grouped (PRES-1/PRES-6/PRES-7).
- **C-2.** Provide reachable explainability (source findings, rationale, affected dimensions, expected impact, history, supersession) from every recommendation (PRES-2/PRES-3).
- **C-3.** Present recommendations as advisory; expose **no** command, autonomous-action, governance, or automation affordance (PRES-4/PRES-5/PRES-12).
- **C-4.** Display the recommendation's state per §G; keep superseded/rejected in **history** (retained), not deleted (PRES-9).
- **C-5.** Label the user's accepted recommendation as **Selected Path**, allowing it to differ from OSLO Recommended (PRES-8).
- **C-6.** Never present Completed/Implemented as finding resolution; present resolution only on reanalysis (PRES-10; §J).
- **C-7.** Show no score/rank/percentage for OSLO Recommended or ordering (PRES-6).
- **C-8.** Introduce no new object/state/event and cause no assessment change through presentation/selection (PRES-11).

Conformance is **all-or-nothing on these rules**; any command framing, opaque/unattributed recommendation, autonomous-action affordance, deleted history, displayed score, or presentation-induced assessment change **fails conformance**.

---

*This specification defines the canonical user-facing presentation of Recommendations: finding-anchored, advisory, explainable, with OSLO Recommended and Possible Resolution Paths as rendering patterns over multiple Recommendations and Selected Path as the user's accepted one. It modifies no model, lifecycle, object, event, or assessment behavior, and introduces no governance, execution, or automation.*

**Recommendation Presentation Specification v1 complete.**
