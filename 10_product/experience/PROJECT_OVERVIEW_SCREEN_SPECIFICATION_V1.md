# Project Overview Screen Specification v1

**Type:** Screen specification (UI architecture & interaction model only)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Consistent with (must not redefine):** `SIXTY_SECOND_ORIENTATION_WORKFLOW_SPECIFICATION_V1.md` · `ORIENTATION_STATE_MODEL_V1.md` · `FINDING_PRESENTATION_SPECIFICATION_V1.md` · `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` · `FINDING_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · CAF Assessment · Reliability v2 · Confidence v2 · Release 1 Tier Definitions.

> **Non-negotiable.** **Presentation architecture only.** No scoring/CAF/Confidence/Reliability calculation, finding/recommendation generation, governance, execution, agents, automation, API contracts, event definitions, or implementation/visual-styling. It translates ratified specs into a **concrete screen architecture**; it redefines no model. The screen must feel like **a strategic understanding console** — not a project-management tool.

---

## A. Purpose

Define the canonical Release 1 **Project Overview** screen — what a user sees when they open a project after analysis completes and the 60-Second Orientation is available — so designers/developers implement it consistently from one architecture.

## B. Scope

In scope: screen structure, section/card hierarchy, interaction zones, navigation entry points, progressive disclosure, and desktop/mobile layout **principles**. Out of scope: visual design, computation, generation, governance/execution, API/events, and implementation (Deferred §O).

## C. Screen Purpose

Answer the user's first question — *"How much can I trust what OSLO understands about my project, and where is attention most needed?"* — in one glance, then let them go deeper on demand. The screen is a **console for understanding**: confidence-first, explainable, advisory; it informs judgment and routes to the Findings and Recommendations experiences. It never executes work or manages tasks.

## D. Screen Hierarchy (canonical, top → bottom)

1. **Project Header**
2. **Outcome Confidence** (headline)
3. **CAF Assessment** (Clarity · Alignment · Feasibility)
4. **Reliability**
5. **Findings** (summary)
6. **Recommendations** (summary)
7. **Project Summary**

**Rationale.** This is the ratified Orientation information hierarchy (Workflow Spec §4) realized as a screen: the **headline trust signal first** (what the user came for), then **CAF** (*why* confidence sits there), then **Reliability** (*how much to trust that judgment*), then **Findings** (the concrete weaknesses), then **Recommendations** (the advisory path), then **Summary** (context). It is the assessment chain *in reverse* — signal first, basis on the way down — which is the natural comprehension order, builds trust through explainability, and keeps the console strategic rather than task-oriented.

## E. Above-the-Fold Model

- **Always visible (no scroll):** **Project Header** + **Outcome Confidence** (band + **reliability qualifier**, with a one-line explanation) + **CAF at-a-glance** (the three dimensions as a compact triad).
- **May be collapsed (visible, summarized):** **Reliability** (level + one-line), **Findings** summary (counts), **Recommendations** summary (OSLO Recommended + path count).
- **Requires expansion / dedicated experience:** full confidence/CAF/reliability explanations; the full **Findings** experience; the full **Recommendations** experience; **Project Summary** detail; history.

Confidence is **never** shown bare (always with its reliability qualifier) and **never** framed as health/probability — above the fold or anywhere.

## F. Card Architecture

### Confidence Card (headline)
- **Visible:** Outcome Confidence **band** (Very Low…Very High) · **reliability qualifier** · one-line cause-of-level.
- **Expandable:** full explanation (CAF + Reliability basis; what last changed it).
- **Entry points:** opens the confidence explanation / history.

### CAF Card
- **Visible:** **Clarity · Alignment · Feasibility**, each as a qualitative level with its per-dimension reliability; Alignment/Feasibility marked **preliminary** when provisional (Fast Pass).
- **Expandable:** per-dimension explanation (contributing findings; qualitative basis).
- **Dimension presentation:** three co-equal dimensions, no ranking/score; each links to the findings affecting it.

### Reliability Card
- **Visible:** Reliability **level** (High/Moderate/Low) + one-line.
- **Expandable:** basis (Coverage / Evidence Availability / Assessability); how it qualifies confidence. **Reliability always presented as a qualifier of confidence, never as something findings change.**

### Finding Summary Card
- **Visible:** top findings (highest-severity), each with title, type, affected dimension; **counts** by severity/dimension.
- **Grouping:** by **CAF dimension**, severity-ordered (per Finding Presentation Spec) — qualitative, no scores.
- **Navigation:** opens the full **Findings** experience (descriptive, finding-anchored).

### Recommendation Summary Card
- **Visible:** **OSLO Recommended** (the primary recommendation, advisory, no score) + a **Possible Resolution Paths** indicator (count of the other Recommendations for the relevant finding(s)).
- **OSLO Recommended presentation:** shown first, distinctly, as a suggestion — never a command.
- **Possible Resolution Paths presentation:** a **presentation grouping of multiple Recommendations** (no object/field); collapsible.
- **Navigation:** opens the full **Recommendations** experience; selecting one is accepting a Recommendation (**Selected Path**).

### Project Summary Card
- **Visible:** key observations / project context (concise).
- **Expandable:** fuller summary; links to artifacts/evidence.

## G. Navigation Model (principles)

- **View Findings** — from the Finding Summary Card into the full Findings experience (Finding Presentation Spec).
- **View Recommendations** — from the Recommendation Summary Card into the full Recommendations experience (Recommendation Presentation Spec).
- **Reanalysis access** — a clear affordance to update project information / trigger reanalysis (the only path that changes assessment). *(Free-tier deep-analysis / budget caps: the affordance **stays enabled** and follows the shared **limit-reached interaction rule** — attempt gated (`429`/DL-048) → upgrade prompt (UP-5/UP-6) + resolution (upgrade / wait / keep last analysis); never disabled or a raw error. See `12_freemium_tier_behavior_logic.md`.)*
- **History access** — reach prior (superseded) orientations (append-only; never deleted).
- **Project settings access** — basic project controls (rename/archive), separate from the understanding console.

Navigation is **hub-and-spoke**: the Overview is the hub; Findings, Recommendations, History, and Settings are spokes. The console surfaces summaries and routes to depth — it does not embed full task lists.

## H. Progressive Disclosure Model

- **Always visible:** Project Header, Outcome Confidence (+ reliability qualifier), CAF triad.
- **Expands in place:** explanations (confidence/CAF/reliability), finding/recommendation summaries.
- **Opens a dedicated experience:** full Findings, full Recommendations, History.
- **Intentionally hidden (not on this screen):** raw computation, scores/percentages, governance/execution affordances, automation — none of which exist in Release 1.

## I. Desktop Layout Principles (single canonical architecture)

**Recommended: a primary understanding spine (single column) + a secondary context rail.**
- **Primary column (focus):** the §D hierarchy as a vertical narrative — Confidence → CAF → Reliability → Findings summary → Recommendations summary → Summary.
- **Secondary right rail (context):** explainability/history, analysis-state indicator (provisional/updating), and the reanalysis affordance.
- **Visual hierarchy:** Confidence is the dominant focus area; CAF + Reliability are the supporting drivers; Findings + Recommendations are the actionable secondary areas; Summary is tertiary.

**Justification (vs single- or dual-column alternatives, choosing one):** a **spine + context rail** preserves the confidence-first narrative (rapid understanding, trust building) while giving explainability and state a home **without** cluttering the read — the "console" feel. A pure single column buries explainability/state in scroll; a symmetric dual-column dilutes the headline. The spine+rail is the single recommended architecture: simple for Release 1/freemium, and scalable (the rail can hold more context later without restructuring).

## J. Mobile Layout Principles

- **Ordering:** single column following §D exactly — Header → Confidence → CAF → Reliability → Findings → Recommendations → Summary. The context rail content (explainability/state/reanalysis) folds **inline** (state indicator near the top; explainability behind expanders).
- **Collapse behavior:** Confidence + CAF triad above the fold; Reliability, Findings, Recommendations, Summary collapsed/summarized with tap-to-expand or tap-to-open.
- **Navigation:** the spokes (Findings, Recommendations, History, Settings) open as dedicated views; the Overview stays the hub. Touch-sized affordances; provisional/updating state visible near the top.

## K. State Integration (presentation behavior per Orientation State — no state logic redefined)

| Orientation State | Project Overview behavior |
|---|---|
| **Analyzing** | Skeleton of the §D hierarchy + a "Building your 60-Second Orientation" indicator; no fabricated content. |
| **Fast Pass Complete** | Full screen rendered with a **provisional** banner ("Deep Analysis in progress"); Alignment/Feasibility marked preliminary; all summaries + navigation active. |
| **Deep Analysis Running** | Full **provisional** screen remains visible (non-blocking) + a "deepening" indicator in the context rail/top. |
| **Deep Analysis Complete** | Screen updates to **current** (provisional banner removed); confidence may have risen/fallen — presented as honest improvement; History link to the prior orientation. |
| **Reanalysis Running** | Prior **current** screen stays visible + an "updating" indicator; content reflects the previous analysis until done. |
| **Reanalysis Complete** | Screen updates to the new current orientation; prior retained in History. |
| **Error** | The **last-good** screen is preserved with an error/retry banner; if no prior exists, an explanatory empty state with retry — never a blanked or fabricated screen. |

## L. Empty-State Behavior

- **No Findings:** Finding Summary Card shows a neutral/positive "No issues found here yet" — never alarming; never implying incomplete analysis when complete.
- **No Recommendations:** Recommendation Summary Card shows "No recommendations yet" (e.g., nothing actionable surfaced); no empty OSLO Recommended slot implying failure.
- **Analysis not yet complete:** the Analyzing skeleton/indicator (per §K), not an empty overview.
- **Previous analysis unavailable (first-run error):** explanatory empty state + retry (per §K Error), distinct from "nothing found" and "filtered."

All empty states distinguish **none-found / not-yet-analyzed / unavailable**, consistent with the Orientation State Model and Finding Presentation Spec.

## M. Integrity Rules

- **POS-1.** **Outcome Confidence is the headline** (top focus), always with its **reliability qualifier**, **never** bare, **never** as health/probability.
- **POS-2.** The §D hierarchy order is preserved (Confidence → CAF → Reliability → Findings → Recommendations → Summary).
- **POS-3.** **Findings remain descriptive** on this screen (summaries, never framed as actions).
- **POS-4.** **Recommendations remain advisory**; OSLO Recommended is a suggestion (no score), shown distinctly.
- **POS-5.** **Possible Resolution Paths are presentation-only** (grouped Recommendations; no object/field).
- **POS-6.** **Reliability always qualifies confidence**; it is never depicted as findings-driven.
- **POS-7.** No screen interaction changes a CAF/Reliability/Confidence signal; **only reanalysis** does.
- **POS-8.** The screen routes (hub-and-spoke) to Findings/Recommendations/History; it does not embed execution/task management.
- **POS-9.** **No governance, execution, agent, or automation affordance** appears.
- **POS-10.** Provisional vs current is signaled per the Orientation State Model; last-good is preserved on Error.
- **POS-11.** No scores/percentages are displayed for confidence, CAF, reliability, findings, or recommendation ordering.

## N. Conformance Requirements

A conforming screen MUST (objective, structural, **non-numeric**):
- **POS-C1.** Render the §D hierarchy in order, with the Confidence Card as the dominant above-the-fold element (POS-1/POS-2).
- **POS-C2.** Always pair Confidence with its reliability qualifier; never bare; never health/probability framing (POS-1/POS-6).
- **POS-C3.** Present Findings (grouped by CAF dimension, severity-ordered, descriptive) and Recommendations (OSLO Recommended + Possible Resolution Paths) per their presentation specs, routing to the full experiences (POS-3/POS-4/POS-5/POS-8).
- **POS-C4.** Implement progressive disclosure per §H (headline always visible; basis/lists on expand/open); hide raw computation/scores/governance/execution (POS-11/POS-9).
- **POS-C5.** Reflect each Orientation State per §K, including provisional/updating indicators and last-good preservation on Error (POS-10).
- **POS-C6.** Ensure no overview interaction changes an assessment signal; only reanalysis does (POS-7).
- **POS-C7.** Implement empty states that distinguish none-found / not-yet-analyzed / unavailable (§L).
- **POS-C8.** Expose no governance/execution/agent/automation affordance in any state (POS-9).

Conformance is **all-or-nothing**; any bare/health-framed confidence, any displayed score, any non-reanalysis assessment change, any embedded execution/task management, any blanked last-good screen, or any governance/execution affordance **fails conformance**.

## O. Deferred Items

Explicitly **deferred** (out of scope): visual styling; colors; typography; component implementation; responsive breakpoints; animations; design-system details; API/events; computation/generation; calibration values; numeric tier boundaries.

## P. Ratified update — Confidence presentation (DL-085, 2026-07-02)

Ratified by **DL-085** (Accepted with Conditions). This block updates the Confidence *presentation* in §E/§F/§M/§N; all other integrity rules are unchanged, and meaning (Interpretation Doctrine) is unchanged. Visual reference of record: `product-design/oslo_r1_experience_mockup_v4.html`. *(Overview hierarchy / "Start here" / Explore-details changes are governed separately by the UX-Surface Reconciliation decision, not here.)*

- **Confidence Card (supersedes the §F "Confidence Card → Visible" line):** the **numeric Outcome Confidence index (0–100) is the focal element**, with its **band** (Very Low…Very High) and **reliability qualifier** shown directly alongside as qualifiers. Confidence is **still never shown bare** (band + reliability always present) and **never** framed as health/probability. Numeric 0–100 is sanctioned by Master Spec §20; the **band remains the authoritative unit of magnitude**.
- **Cause-bound movement:** when analysis changes the index the card states the **cause** (e.g., a resolved finding), and the index may move **up or down** (a fall after Extended/Deep Analysis reflects improved understanding, not a worse project). Surfaced via a "how this is calculated" affordance; **no "illustrative" caveat** in production.
- **Work-ledger:** a compact readout of **countable governed objects** (findings resolved/open by severity) accompanies the card; it counts only attested/governed objects and **never** restates the signal as a second number.
- **No gamification:** no points, streaks, or score-to-beat; the confidence ramp stays **neutral** (non health-color).
- **Retained verbatim:** the "never bare / never health-probability" requirement (POS-1, POS-C2). §E/§M/§N band-first framing is **superseded** to "number-focal, reliability-qualified."

---

*This specification defines the single canonical Release 1 Project Overview screen architecture: a confidence-first understanding console — Project Header → Outcome Confidence → CAF → Reliability → Findings → Recommendations → Summary — with a desktop understanding-spine + context-rail, a confidence-first mobile column, state-aware provisional/current presentation, hub-and-spoke navigation to the Findings and Recommendations experiences, and append-only history. It defines presentation architecture only — no models, scoring, computation, generation, governance, execution, automation, APIs, events, or styling — and preserves that confidence is reliability-qualified trust in understanding and only reanalysis changes assessment.*

## Q. Ratified update — Overview hierarchy (DL-088, 2026-07-02)

Ratified by **DL-088** (presentation-only; complements DL-085 §P). To reduce cognitive load the Overview is sequenced **Confidence → a single "Start here" next-action (the top severity-ordered open finding) → a compact Progress readout → Explore details (CAF · Reliability · Attention)**. The at-a-glance CAF triad is **demoted into Explore details** (it duplicated the CAF card). The §D canonical order and all integrity rules otherwise stand; findings/recommendations remain descriptive/advisory; only reanalysis changes assessment. Visual reference of record: `product-design/oslo_r1_experience_mockup_v4.html`.

## R. Ratified update — Overview cognitive-load trim (DL-090, 2026-07-02)

Ratified by **DL-090** (presentation-only; **amends §Q**). The Overview is trimmed to: **Confidence → a compact "What's driving it" CAF driver-glance → confidence trend → Start here → Progress → (quiet) project summary.** Removed from the Overview:
- **Reliability component breakdown** — headline stays on the confidence line; Coverage/Evidence availability/Assessability fold into the "how this is calculated" explainer. **Realization (DL-090):** that explainer is the **top-bar Confidence pill popover**, which shows the CAF dimension breakdown **and** the three reliability components; the confidence-line reliability qualifier links to it. Reliability remains a **qualifier** of Confidence, determined independently of CAF — not a fourth dimension, never findings-driven (POS-6). Verified by baseline `08-confidence-explainer`.
- **Recommendations summary** — Panel Model; recommendations live only inside a Finding ("Start here" carries the next action).
- **Attention heatmap** — relocated to its own **"Attention map" (MRI) left-rail surface** (see Global-Nav / MRI specs), not embedded here.

CAF driver chips are **qualitative** (level only; per-dimension 0–100 numbers move to drill-in). Confidence doctrine, Panel Model, and advisory-only unchanged. Visual reference of record: `product-design/oslo_r1_experience_mockup_v4.html` (baseline `02-overview`).

**Readability presentation (realization, presentation-only).** The §Q/§R hierarchy renders as **three whitespace-separated cards** — (1) *the read* (Confidence ring + number, reliability qualifier, "What's driving it" CAF chips, trend), (2) *Start here* (the single next action), (3) *Progress* (a 4-cell stat row: findings resolved · critical open · dependencies confirmed · plan sections read). Segmentation is by whitespace/cards, not hairline dividers. Type roles are limited to: hero number · section headline (~21px) · body/qualifier (~13px `muted`) · caption (~11px `subtle`); the reliability qualifier is never the smallest text. The first-run coaching banner does not persist on the steady-state Overview. This changes presentation hierarchy only — order, content set (DL-090), Confidence doctrine, and Panel Model are unchanged. Verified by baselines `02-overview`, `04-finding-panel`, `08-confidence-explainer`.

**Project Overview Screen Specification v1 complete.**
