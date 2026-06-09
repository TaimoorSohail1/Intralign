# Finding Workspace Specification v1 — SUPERSEDED / REPOSITIONED

> **📦 ARCHIVED 2026-06-04 — historical.** Superseded by `FINDING_PANEL_SPECIFICATION_V1.md`. Moved to `04_research/historical_artifacts/` to keep the active tree clean; content preserved for history and does **not** govern implementation.

> ## ⛔ SUPERSEDED / REPOSITIONED — Surface Reconciliation Decision 001, Option A ratified (2026-05-31)
> - This document is **superseded/repositioned by `FINDING_PANEL_SPECIFICATION_V1.md`**.
> - The former **"workspace" framing is no longer canonical for Release 1.** Per `FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md` (Option A — Panel Model), the canonical Release 1 surface is a **contextual Finding Panel opened from the MRI Workspace and Artifact Workspace**, subordinate to them — **not a standalone destination**.
> - The substantive **descriptive-first / evidence-first / recommendation-enabled / reanalysis-driven** behavior below **remains valid where compatible** and is carried into the Finding Panel spec.
> - Findings remain first-class **descriptive model objects** (unchanged). This is a UX surface/document repositioning only — no object, lifecycle, CAF, Reliability, Confidence, or attribution change.
> - Retained for history (append-only); the content below no longer governs the canonical Release 1 surface.

**Type:** Workspace specification (user experience / interaction model only) — **SUPERSEDED by `FINDING_PANEL_SPECIFICATION_V1.md`**
**Status:** Superseded / Repositioned (was: Active Release 1) · **Date:** 2026-05-31
**Sits below (authoritative — implements, must not modify):** `FINDING_SYSTEM_SPECIFICATION_V1.md` · `FINDING_PRESENTATION_SPECIFICATION_V1.md` · `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` · `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md` · `SIXTY_SECOND_ORIENTATION_WORKFLOW_SPECIFICATION_V1.md` · `ORIENTATION_STATE_MODEL_V1.md` · `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · CAF Assessment · Reliability v2 · Confidence v2 · Release 1 Tier Definitions.

> **Non-negotiable.** UX/interaction only. **No** scoring, CAF/Confidence/Reliability calculation, finding/recommendation generation, governance, execution, agents, automation, API contracts, event definitions, implementation, or styling. The workspace is **descriptive-first, evidence-first, recommendation-enabled, reanalysis-driven** — and it must feel like an **investigative understanding workspace**, not a project-management screen. It redefines no model; **only reanalysis changes assessment**; **confidence is reliability-qualified trust in understanding, never finding-driven directly**.

The architecture it serves:
```text
Project → Finding → Recommendation → User Action → Information Change → Reanalysis → Updated Finding
```

---

## A. Purpose

The Finding Workspace is the primary environment a user enters after selecting a Finding from the Project Overview. It exists to answer: **"Why does this finding exist, what evidence supports it, what recommendations are available, and what should I do next?"** It is where the user investigates a weakness in understanding, reviews its evidence, evaluates advisory recommendations, updates project information, and triggers reanalysis.

## B. Scope

**In scope:** presentation/interaction for a single Finding — header, summary, evidence, supporting context, CAF impact, recommendations, history, reanalysis status, user actions, and state-aware behavior.

**Explicitly out of scope (excluded):** execution · task management · governance · accepted understanding · dispositions · agents · automation · project-health management. (Plus all computation/generation/API/events/styling — Deferred §S.)

## C. Workspace Goals (questions answered)

- **"Why was this finding created?"** → Finding Summary + rationale (§F).
- **"What evidence supports it?"** → Evidence (§G).
- **"What is weakening understanding?"** → CAF Impact (§I) + affected dimensions.
- **"What does OSLO suggest?"** → OSLO Recommended (§J).
- **"What other recommendations exist?"** → Possible Resolution Paths (§J).
- **"What changed recently?"** → Activity/History (§M) + reanalysis status (§L).
- **"What can I do next?"** → User Actions (§K) — evaluate recommendations, update information, reanalyze.

## D. Workspace Architecture (single canonical, top → bottom)

1. **Finding Header**
2. **Finding Summary**
3. **Evidence**
4. **Supporting Context**
5. **CAF Impact**
6. **Recommendations**
7. **Activity / History**
8. **Reanalysis Status**

**Rationale.** The order follows the investigative arc: **what it is** (Header) → **why it exists** (Summary) → **what supports it** (Evidence) → **what surrounds it** (Context) → **what it weakens** (CAF Impact) → **what to consider** (Recommendations) → **what changed** (History) → **what's updating** (Reanalysis Status). Descriptive/evidence content leads; advisory recommendations follow the understanding (never before it); reanalysis status anchors the bottom as the only path that changes assessment. This is a **single recommended architecture** — it maximizes understanding/explainability and Release 1 simplicity, and is the inverse-emphasis of a task tool (insight before action). Reanalysis Status may also surface as a persistent indicator (per §L) regardless of scroll.

## E. Finding Header

- **Visible:** title · finding type (user-friendly) · severity (qualitative: critical/moderate/warning) · affected CAF dimension(s) · lifecycle status (§N).
- **Descriptive only** — the header states the observed condition. **No recommendations or actions here** beyond navigation.

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
- **Never depicted:** Finding → *directly changes* Confidence; Finding → *influences* Reliability. Reliability is shown (where relevant) as an **independent qualifier** of confidence, never as finding-driven. The workspace never shows the finding "setting" CAF or confidence.

## J. Recommendations Section

Aligns **completely** with `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md`:
- **OSLO Recommended** — the primary recommendation for this finding, shown first, advisory, **no score**.
- **Possible Resolution Paths** — the **other Recommendations** for this finding, grouped as a presentation pattern (collapsible).
- **Selected Path** — the Recommendation the user has accepted (may differ from OSLO Recommended).

**These are presentation constructs only.** The workspace introduces **no** Resolution Path object, **no** Clarification Candidate, **no** Resolution Candidate. **Possible Resolution Paths remains a grouping of multiple Recommendations** (no entity/field/lifecycle/event).

## K. User Actions (Release 1 only)

**Allowed:** View Recommendation · Accept Recommendation · Reject Recommendation · **Defer Recommendation** · Update Project Information · Trigger Reanalysis.

**Explicitly prohibited:** Execute · Apply Automatically · Run Agent · Approve · Govern · **Resolve Finding manually**. The user **never** directly closes/resolves a finding from the workspace — a finding weakens/closes **only** through reanalysis (§L). OSLO advises; the user evaluates recommendations and changes information; reanalysis does the rest.

## L. Reanalysis Experience

- **Reanalysis Running:** the workspace remains **visible and readable** (non-blocking) with an "updating — reflects previous analysis" indicator; the prior finding state stays shown until reanalysis completes (per Orientation State Model).
- **Reanalysis Complete:** the finding updates. After reanalysis a finding may: **weaken**, **remain unchanged**, **close** (resolved), or be **superseded** (replaced; prior retained). The workspace reflects the new state and links the prior in history.
- **Only reanalysis changes assessment** — updating information / accepting / deferring a recommendation, by itself, changes no CAF/Reliability/Confidence and does not close the finding; it is the **reanalysis** that may weaken/close it.

## M. Finding History

- **Append-only:** the workspace shows the finding's **lifecycle history**, its **supersession chain**, and its **recommendation history** — all **retained, never deleted**.
- The user can reach prior (superseded/closed) states and the recommendations that were associated over time. History is **immutable** in presentation (no edit/delete affordance).

## N. State Integration (presentation per finding status — no lifecycle change)

| Status | Workspace presentation |
|---|---|
| **Detected** | new/open; prominent; full investigation available |
| **Acknowledged** | marked seen/accepted-as-real |
| **Addressed** | marked in-progress (work targeting it has begun) |
| **Closed** | shown resolved; moved toward history; reached via reanalysis, **not** a manual button |
| **Reopened** | shown returned-to-open with a reopened indicator |
| **Superseded** | shown in history (retained); links to the superseding finding |

The workspace **visualizes** status; it does not redefine the lifecycle and offers **no manual resolve/close** control (§K).

## O. Empty States

- **No evidence:** an explanatory state (rare — findings require evidence; a finding with no reachable evidence is a conformance failure, not a normal empty state).
- **No recommendations:** "No recommendations yet" — the finding is investigable; no empty OSLO Recommended slot implying failure.
- **No related findings/context:** a neutral "No related context" — not alarming.
- **Unavailable history:** distinguish "no prior history (first analysis)" from "history temporarily unavailable."
- All empty states **distinguish none-found / unavailable / not-yet-analyzed**, consistent with the Orientation State Model and Finding Presentation Spec.

## P. Progressive Disclosure

- **Always visible:** Finding Header + Finding Summary (what it is / why it exists) + a persistent Reanalysis Status indicator.
- **Expands in place:** Evidence detail · Supporting Context · CAF Impact explanation · recommendation rationale.
- **Opens a dedicated experience:** a specific Recommendation (full Recommendation view) · full History/timeline.
- **Intentionally absent:** scores/percentages, governance/execution/automation affordances, manual resolve/close.

## Q. Integrity Rules

- **FWS-1.** Findings remain **descriptive** throughout the workspace (never framed as actions/commands).
- **FWS-2.** Recommendations remain **advisory**; OSLO Recommended is a suggestion (no score), not a command.
- **FWS-3.** **Possible Resolution Paths** are presentation-only (grouped Recommendations); no object/field.
- **FWS-4.** **Reliability is never finding-driven**; it is shown as an independent qualifier of confidence.
- **FWS-5.** The workspace never depicts a finding **directly** changing CAF or Confidence; only **Finding → CAF → Confidence** (via Impact Assessment).
- **FWS-6.** **Only reanalysis changes assessment**; no workspace interaction alters a CAF/Reliability/Confidence signal.
- **FWS-7.** **No manual finding resolution** — findings weaken/close only via reanalysis.
- **FWS-8.** Evidence is **explainable and traceable**; **no opaque finding**.
- **FWS-9.** History is **append-only and immutable** in presentation; nothing deleted.
- **FWS-10.** **No governance** affordance (approve/govern/disposition/accepted-understanding).
- **FWS-11.** **No execution / no automation / no agent** affordance.
- **FWS-12.** The workspace is an **investigative understanding** surface, not a task/project-management or execution surface.

## R. Conformance Requirements

A conforming workspace MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:
- **FW-C1.** Render the §D architecture in order, descriptive/evidence content before recommendations (FWS-1/FWS-2).
- **FW-C2.** Present Evidence as traceable/explainable; **no opaque finding** (FWS-8).
- **FW-C3.** Present CAF Impact as **Finding → CAF → Confidence**; **never** finding→direct-Confidence or finding→Reliability (FWS-4/FWS-5). **Fail** if confidence is shown as finding-driven.
- **FW-C4.** Present Recommendations per the Recommendation Presentation Spec (OSLO Recommended / Possible Resolution Paths / Selected Path), advisory, no score; no Resolution-Path/Clarification/Resolution-Candidate object (FWS-2/FWS-3). **Fail** if recommendations become commands.
- **FW-C5.** Expose exactly the §K actions; expose **no** Execute/Apply/Run-Agent/Approve/Govern/manual-Resolve (FWS-7/FWS-10/FWS-11). **Fail** if execution or governance appears.
- **FW-C6.** Ensure no workspace interaction changes an assessment signal; only reanalysis does (FWS-6).
- **FW-C7.** Keep History **append-only/immutable**; reflect finding status per §N without manual resolve (FWS-9). **Fail** if history is mutable.
- **FW-C8.** Implement empty states distinguishing none-found / unavailable / not-yet-analyzed (§O).

Conformance is **all-or-nothing**; any execution/governance affordance, confidence-shown-as-finding-driven, recommendation-as-command, mutable history, or non-reanalysis assessment change **fails conformance**.

## S. Deferred Items

Explicitly **deferred / out of scope:** governance workflows · accepted understanding · disposition management · automation · agents · execution · future orchestration capabilities · visual styling/components/breakpoints/animations · APIs/events · computation/generation · calibration values · numeric tier boundaries.

---

*This specification defines the canonical Release 1 Finding Workspace: an investigative, descriptive-first, evidence-first, recommendation-enabled, reanalysis-driven environment — Header → Summary → Evidence → Supporting Context → CAF Impact → Recommendations → History → Reanalysis Status — that explains why a finding exists, surfaces its evidence and advisory recommendations, and routes change only through reanalysis. It defines no models, scoring, computation, generation, governance, execution, automation, agents, APIs, events, or styling; preserves Finding → CAF → Confidence (never finding→direct-confidence, never finding→reliability); keeps recommendations advisory and Possible Resolution Paths presentation-only; and keeps history append-only.*

**Finding Workspace Specification v1 complete.**
