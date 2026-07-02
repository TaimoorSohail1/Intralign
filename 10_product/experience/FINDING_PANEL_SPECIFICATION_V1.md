# Finding Panel Specification v1

**Type:** Panel specification (user experience / interaction model only)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Canonical surface** per `FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md` (Option A — Panel Model, ratified). **Repositions** `FINDING_WORKSPACE_SPECIFICATION_V1.md` (superseded; retained for history).
**Sits below (authoritative — presents, must not modify):** `FINDING_SYSTEM_SPECIFICATION_V1.md` · `FINDING_PRESENTATION_SPECIFICATION_V1.md` · `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` · `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md` · `MRI_WORKSPACE_SPECIFICATION_V1.md` · `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` · `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1.md` · `SIXTY_SECOND_ORIENTATION_WORKFLOW_SPECIFICATION_V1.md` · `ORIENTATION_STATE_MODEL_V1.md` · `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · CAF Assessment · Reliability v2 · Confidence v2 · Release 1 Tier Definitions.

> **Non-negotiable.** UX/interaction only. **No** scoring, CAF/Confidence/Reliability calculation, finding/recommendation generation, governance, execution, agents, automation, API contracts, event definitions, implementation, or styling. The Finding Panel is **contextual, descriptive-first, evidence-first, recommendation-enabled, reanalysis-driven** — a panel opened **in context**, **not a standalone destination**. It redefines no model; **only reanalysis changes assessment**; **confidence is reliability-qualified trust in understanding, never finding-driven directly**.

**Surface model (Option A):** the Finding Panel is a **contextual panel** — opened from **CAF overlays, MRI selections, artifact context, or related finding references** — **subordinate to the Artifact Workspace and MRI Workspace**. It opens over/beside the originating surface, preserving that context, and closes back to it. It is **not** a primary navigation destination.

The architecture it serves:
```text
Project Overview → MRI Workspace → Artifact Workspace → Finding Panel → Recommendation Panel
(object chain) Project → Finding → Recommendation → User Action → Information Change → Reanalysis → Updated Finding
```

---

## A. Purpose

The Finding Panel is the contextual surface a user opens after selecting a Finding — from a **CAF overlay** in the Artifact Workspace, an **MRI selection**, **artifact context**, or a **related finding reference**. It answers: **"Why does this finding exist, what evidence supports it, what recommendations are available, and what should I do next?"** It is where the user investigates a weakness in understanding **without leaving the surface they came from** — reviewing evidence, evaluating advisory recommendations, updating project information, and triggering reanalysis.

## B. Scope

**In scope:** presentation/interaction for a single Finding in a contextual panel — header, summary, evidence, supporting context, CAF impact, recommendations, history, reanalysis status, user actions, state-aware behavior, and open/close context preservation.

**Explicitly out of scope (excluded):** standalone-destination/navigation framing · execution · task management · governance · accepted understanding · dispositions · agents · automation · project-health management. (Plus all computation/generation/API/events/styling — Deferred §S.)

## C. Panel Goals (questions answered)

- **"Why was this finding created?"** → Finding Summary + rationale (§F).
- **"What evidence supports it?"** → Evidence (§G).
- **"What is weakening understanding?"** → CAF Impact (§I) + affected dimensions.
- **"What does OSLO suggest?"** → OSLO Recommended (§J).
- **"What other recommendations exist?"** → Possible Resolution Paths (§J).
- **"What changed recently?"** → Activity/History (§M) + reanalysis status (§L).
- **"What can I do next?"** → User Actions (§K) — evaluate recommendations, update information, reanalyze.
- **"How do I get back?"** → close the panel; the originating MRI/Artifact context (selection, overlay, scroll) is preserved (§D).

## D. Panel Architecture & Context Behavior (single canonical, top → bottom)

**Opening & context.** The Finding Panel opens **in context** — over/beside the Artifact Workspace or MRI Workspace surface it was invoked from. The originating context (artifact content + scroll, the CAF overlay, the MRI lens/selection) **remains beneath** the panel; closing returns the user **exactly** there. The panel requires **no standalone navigation** and is never a separate destination (Global Navigation Object Context; NAV-8).

**Content order (top → bottom):**

1. **Finding Header**
2. **Finding Summary**
3. **Evidence**
4. **Supporting Context**
5. **CAF Impact**
6. **Recommendations**
7. **Activity / History**
8. **Reanalysis Status**

**Rationale.** The order follows the investigative arc: **what it is** (Header) → **why it exists** (Summary) → **what supports it** (Evidence) → **what surrounds it** (Context) → **what it weakens** (CAF Impact) → **what to consider** (Recommendations) → **what changed** (History) → **what's updating** (Reanalysis Status). Descriptive/evidence content leads; advisory recommendations follow the understanding (never before it); reanalysis status anchors the bottom as the only path that changes assessment. Reanalysis Status may also persist as an indicator regardless of scroll.

## E. Finding Header

- **Visible:** title · finding type (user-friendly) · **epistemic basis** (`stated` / `inferred`) · severity (qualitative: critical/moderate/warning) · affected CAF dimension(s) · lifecycle status (§N).
- **Descriptive only** — the header states the observed condition. **No recommendations or actions here** beyond panel controls (e.g., open Recommendation Panel, close).
- **Basis (DL-093, presentation-only):** the header carries the finding's **basis** as a calm/neutral tag — **stated (Attested)** vs **inferred (Derived)** — and §F names it in plain language ("OSLO inferred this — not stated in your inputs" / "Grounded in a stated item in your plan"), discharging the Disclose obligation (`RELEASE_1_EPISTEMIC_STATE_MODEL_DECISION_001`). **"Inferred" is a basis, never a type.** Basis colour never uses the action/attention accent. Sub-typing + basis-assignment contract deferred to R2 (RB-033).

## F. Finding Summary Section

- **Visible:** the finding explanation · rationale (why OSLO identified it) · why it matters · **what aspect of understanding it weakens** (which dimension and how, qualitatively).
- Aligns with the Finding System Spec: descriptive, basis-grounded; never prescriptive.

## G. Evidence Section

- **Visible:** source evidence · supporting references · artifact references · supporting observations the finding is grounded in.
- **Explainable & traceable:** every claim the finding rests on is reachable; the user can trace from finding → evidence. **No opaque finding** — a finding lacking reachable evidence is non-conformant.

## H. Supporting Context Section

- **Visible (presentation only — no new models):** related assumptions · related findings · dependencies · constraints · other contextual information bearing on the finding.
- These are **existing** concepts (findings/context) surfaced for investigation; this section introduces no new object or model.

## I. CAF Impact Section

- **Visible:** how the finding contributes to **Clarity / Alignment / Feasibility** — the dimension(s) it affects and, qualitatively, how (its Impact-Assessment relationship). **No magnitudes, indices, or formulas.**
- **Preserved chain:** **Finding → contributes to CAF → contributes to Confidence.** The section may help the user see why confidence sits where it does *through* CAF.
- **Never depicted:** Finding → *directly changes* Confidence; Finding → *influences* Reliability. Reliability is shown (where relevant) as an **independent qualifier** of confidence, never as finding-driven. The panel never shows the finding "setting" CAF or confidence.

## J. Recommendations Section

Aligns **completely** with `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md`:
- **OSLO Recommended** — the primary recommendation for this finding, shown first, advisory, **no score**.
- **Possible Resolution Paths** — the **other Recommendations** for this finding, grouped as a presentation pattern (collapsible).
- **Selected Path** — the Recommendation the user has accepted (may differ from OSLO Recommended).

**These are presentation constructs only.** The panel introduces **no** Resolution Path object, **no** Clarification Candidate, **no** Resolution Candidate. **Possible Resolution Paths remains a grouping of multiple Recommendations** (no entity/field/lifecycle/event). Opening a recommendation routes to the **Recommendation Panel** (§K), itself opened **only** from this Finding context.

## K. User Actions (Release 1 only)

**Allowed:** View Recommendation (opens the **Recommendation Panel** in context) · Accept Recommendation · Reject Recommendation · **Defer Recommendation** · Update Project Information · Trigger Reanalysis · Close Panel (returns to originating context).

**Explicitly prohibited:** Execute · Apply Automatically · Run Agent · Approve · Govern · **Resolve Finding manually**. The user **never** directly closes/resolves a finding from the panel — a finding weakens/closes **only** through reanalysis (§L). OSLO advises; the user evaluates recommendations and changes information; reanalysis does the rest.

## L. Reanalysis Experience

- **Reanalysis Running:** the panel remains **visible and readable** (non-blocking) with an "updating — reflects previous analysis" indicator; the prior finding state stays shown until reanalysis completes (per Orientation State Model). The originating context beneath the panel likewise remains visible.
- **Reanalysis Complete:** the finding updates. After reanalysis a finding may: **weaken**, **remain unchanged**, **close** (resolved), or be **superseded** (replaced; prior retained). The panel reflects the new state and links the prior in history.
- **Only reanalysis changes assessment** — updating information / accepting / deferring a recommendation, by itself, changes no CAF/Reliability/Confidence and does not close the finding; it is the **reanalysis** that may weaken/close it.

## M. Finding History

- **Append-only:** the panel shows the finding's **lifecycle history**, its **supersession chain**, and its **recommendation history** — all **retained, never deleted**.
- The user can reach prior (superseded/closed) states and the recommendations associated over time. History is **immutable** in presentation (no edit/delete affordance).

## N. State Integration (presentation per finding status — no lifecycle change)

| Status | Panel presentation |
|---|---|
| **Detected** | new/open; prominent; full investigation available |
| **Acknowledged** | marked seen/accepted-as-real |
| **Addressed** | marked in-progress (work targeting it has begun) |
| **Closed** | shown resolved; moved toward history; reached via reanalysis, **not** a manual button |
| **Reopened** | shown returned-to-open with a reopened indicator |
| **Superseded** | shown in history (retained); links to the superseding finding |

The panel **visualizes** status; it does not redefine the lifecycle and offers **no manual resolve/close** control (§K).

## O. Empty States

- **No evidence:** an explanatory state (rare — findings require evidence; a finding with no reachable evidence is a conformance failure, not a normal empty state).
- **No recommendations:** "No recommendations yet" — the finding is investigable; no empty OSLO Recommended slot implying failure.
- **No related findings/context:** a neutral "No related context" — not alarming.
- **Unavailable history:** distinguish "no prior history (first analysis)" from "history temporarily unavailable."
- All empty states **distinguish none-found / unavailable / not-yet-analyzed**, consistent with the Orientation State Model and Finding Presentation Spec.

## P. Progressive Disclosure

- **Always visible:** Finding Header + Finding Summary (what it is / why it exists) + a persistent Reanalysis Status indicator.
- **Expands in place:** Evidence detail · Supporting Context · CAF Impact explanation · recommendation rationale.
- **Opens a contextual panel:** a specific Recommendation (the **Recommendation Panel**) · full History/timeline.
- **Intentionally absent:** standalone-destination framing; scores/percentages; governance/execution/automation affordances; manual resolve/close.

## Q. Integrity Rules

- **FP-1.** Findings remain **descriptive** throughout the panel (never framed as actions/commands).
- **FP-2.** Recommendations remain **advisory**; OSLO Recommended is a suggestion (no score), not a command.
- **FP-3.** **Possible Resolution Paths** are presentation-only (grouped Recommendations); no object/field.
- **FP-4.** **Reliability is never finding-driven**; it is shown as an independent qualifier of confidence.
- **FP-5.** The panel never depicts a finding **directly** changing CAF or Confidence; only **Finding → CAF → Confidence** (via Impact Assessment).
- **FP-6.** **Only reanalysis changes assessment**; no panel interaction alters a CAF/Reliability/Confidence signal.
- **FP-7.** **No manual finding resolution** — findings weaken/close only via reanalysis.
- **FP-8.** Evidence is **explainable and traceable**; **no opaque finding**.
- **FP-9.** History is **append-only and immutable** in presentation; nothing deleted.
- **FP-10.** **No governance** affordance (approve/govern/disposition/accepted-understanding).
- **FP-11.** **No execution / no automation / no agent** affordance.
- **FP-12.** The Finding Panel is a **contextual investigative surface subordinate to MRI/Artifact** — **not a standalone destination**, and not a task/project-management or execution surface.
- **FP-13.** The panel **opens in context and preserves it** — opening/closing never discards the originating MRI selection, artifact context, CAF overlay, or scroll position.

## R. Conformance Requirements

A conforming Finding Panel MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:
- **FP-C1.** Open **in context** from a CAF overlay / MRI selection / artifact context / related-finding reference, subordinate to MRI/Artifact, preserving and returning to the originating context (FP-12/FP-13). **Fail** if it is a standalone destination or discards context.
- **FP-C2.** Render the §D content in order, descriptive/evidence content before recommendations (FP-1/FP-2).
- **FP-C3.** Present Evidence as traceable/explainable; **no opaque finding** (FP-8).
- **FP-C4.** Present CAF Impact as **Finding → CAF → Confidence**; **never** finding→direct-Confidence or finding→Reliability (FP-4/FP-5). **Fail** if confidence is shown as finding-driven.
- **FP-C5.** Present Recommendations per the Recommendation Presentation Spec (OSLO Recommended / Possible Resolution Paths / Selected Path), advisory, no score; no Resolution-Path/Clarification/Resolution-Candidate object (FP-2/FP-3). **Fail** if recommendations become commands.
- **FP-C6.** Expose exactly the §K actions; expose **no** Execute/Apply/Run-Agent/Approve/Govern/manual-Resolve (FP-7/FP-10/FP-11). **Fail** if execution or governance appears.
- **FP-C7.** Ensure no panel interaction changes an assessment signal; only reanalysis does (FP-6).
- **FP-C8.** Keep History **append-only/immutable**; reflect finding status per §N without manual resolve (FP-9). **Fail** if history is mutable.
- **FP-C9.** Implement empty states distinguishing none-found / unavailable / not-yet-analyzed (§O).

Conformance is **all-or-nothing**; any standalone-destination framing, context loss on open/close, execution/governance affordance, confidence-shown-as-finding-driven, recommendation-as-command, mutable history, or non-reanalysis assessment change **fails conformance**.

## S. Deferred Items

Explicitly **deferred / out of scope:** governance workflows · accepted understanding · disposition management · automation · agents · execution · future orchestration capabilities · visual styling/components/breakpoints/animations · APIs/events · computation/generation · calibration values · numeric tier boundaries.

---

*This specification defines the canonical Release 1 Finding Panel (Option A — Panel Model): a contextual, descriptive-first, evidence-first, recommendation-enabled, reanalysis-driven panel opened from CAF overlays, MRI selections, artifact context, or related-finding references and subordinate to the Artifact Workspace and MRI Workspace — Header → Summary → Evidence → Supporting Context → CAF Impact → Recommendations → History → Reanalysis Status — that explains why a finding exists, surfaces its evidence and advisory recommendations, preserves originating context on open/close, and routes change only through reanalysis. It is not a standalone destination. It defines no models, scoring, computation, generation, governance, execution, automation, agents, APIs, events, or styling; preserves Finding → CAF → Confidence (never finding→direct-confidence, never finding→reliability); keeps recommendations advisory and Possible Resolution Paths presentation-only; and keeps history append-only.*

**Finding Panel Specification v1 complete.**
