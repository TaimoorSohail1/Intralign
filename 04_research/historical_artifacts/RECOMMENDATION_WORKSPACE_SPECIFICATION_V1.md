# Recommendation Workspace Specification v1 — SUPERSEDED / REPOSITIONED

> **📦 ARCHIVED 2026-06-04 — historical.** Superseded by `RECOMMENDATION_PANEL_SPECIFICATION_V1.md`. Moved to `04_research/historical_artifacts/` to keep the active tree clean; content preserved for history and does **not** govern implementation.

> ## ⛔ SUPERSEDED / REPOSITIONED — Surface Reconciliation Decision 001, Option A ratified (2026-05-31)
> - This document is **superseded/repositioned by `RECOMMENDATION_PANEL_SPECIFICATION_V1.md`**.
> - The former **"workspace" framing is no longer canonical for Release 1.** Per `FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md` (Option A — Panel Model), the canonical Release 1 surface is a **contextual Recommendation Panel opened only from a Finding Panel**, subordinate to it — **not a standalone destination**.
> - The substantive **advisory-first / finding-anchored / explanation-driven / reanalysis-driven** behavior below **remains valid where compatible** and is carried into the Recommendation Panel spec.
> - Recommendations remain first-class **advisory model objects** with finding attribution (unchanged). This is a UX surface/document repositioning only — no object, lifecycle, CAF, Reliability, Confidence, or attribution change.
> - Retained for history (append-only); the content below no longer governs the canonical Release 1 surface.

**Type:** Workspace specification (user experience / interaction model only) — **SUPERSEDED by `RECOMMENDATION_PANEL_SPECIFICATION_V1.md`**
**Status:** Superseded / Repositioned (was: Active Release 1) · **Date:** 2026-05-31
**Sits below (authoritative — implements, must not modify):** `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` · `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md` · `FINDING_SYSTEM_SPECIFICATION_V1.md` · `FINDING_PRESENTATION_SPECIFICATION_V1.md` · `FINDING_WORKSPACE_SPECIFICATION_V1.md` · `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · `SIXTY_SECOND_ORIENTATION_WORKFLOW_SPECIFICATION_V1.md` · `ORIENTATION_STATE_MODEL_V1.md` · CAF Assessment · Reliability v2 · Confidence v2 · Release 1 Tier Definitions.

> **Non-negotiable.** UX/interaction only. **No** new objects, lifecycle, events, or governance concepts; **no** scoring, CAF/Confidence/Reliability computation, generation, execution, agents, automation, APIs, or styling. The workspace is **advisory-first, finding-anchored, recommendation-centered, explanation-driven, reanalysis-driven** — a **recommendation evaluation and decision-support workspace**, not a task-execution or governance screen. **Only reanalysis changes assessment.**

The architecture it serves:
```text
Finding → Recommendation → User Action → Information Change → Reanalysis → Assessment Change
```

---

## A. Purpose

The Recommendation Workspace is the environment entered when a user selects a Recommendation from the **Project Overview** or **Finding Workspace**. It answers: **"Why does this recommendation exist, what finding does it address, what alternatives exist, what does OSLO recommend, what happens if I choose a different path, and what should I do next?"** It is where the user **evaluates** an advisory recommendation in the context of its finding and its alternatives, then accepts/defers/rejects, updates information, or reanalyzes.

## B. Scope

**In scope:** presentation/interaction for a single Recommendation — header, summary, finding attribution, rationale, CAF impact, alternatives, history, user actions, and reanalysis status.

**Explicitly excluded:** execution · governance · accepted understanding · agents · automation · task management · project-health management. (Plus computation/generation/API/events/styling — Deferred §S.)

## C. Workspace Goals (questions answered)

- **"Why was this recommendation created?"** → Rationale (§H).
- **"Which finding does it address?"** → Finding Attribution (§G).
- **"Why is OSLO recommending it?"** → OSLO Recommended (§J) + Rationale.
- **"What alternatives exist?"** → Possible Resolution Paths (§J).
- **"What happens if I choose another option?"** → Selected Path semantics (§J).
- **"What did I previously choose?"** → Selection history (§M).
- **"What changed over time?"** → History (§M) + Reanalysis Status (§L).
- **"What should I do next?"** → User Actions (§K).

## D. Workspace Architecture (single canonical, top → bottom)

1. **Recommendation Header**
2. **Recommendation Summary**
3. **Finding Attribution**
4. **Recommendation Rationale**
5. **CAF Impact**
6. **Alternative Recommendations** (OSLO Recommended · Possible Resolution Paths · Selected Path)
7. **Recommendation History**
8. **User Actions**
9. **Reanalysis Status**

**Rationale.** The order is the evaluation arc: **what is suggested** (Header/Summary) → **why it's grounded** (Finding Attribution) → **why it's advised** (Rationale) → **what it aims to improve** (CAF Impact) → **what else could be chosen** (Alternatives) → **what changed** (History) → **the decision** (User Actions) → **what's updating** (Reanalysis Status). Understanding-and-attribution precede the decision (advisory-first, finding-anchored); the decision is near the bottom, after the user can compare alternatives; reanalysis status anchors the foot as the only path to assessment change. This single architecture optimizes for **decision support**, not task execution. Reanalysis Status may also persist as an indicator regardless of scroll.

## E. Recommendation Header

- **Visible:** recommendation title · type (user-friendly) · lifecycle status (§N) · **effort** (Low/Medium/High) · affected CAF dimension(s).
- **Advisory only** — the header frames a suggestion, never a directive. No "execute/apply" affordance here.

## F. Recommendation Summary

- **Visible:** the recommendation explanation · its intent · **what understanding weakness it addresses** · **expected impact (qualitative only)** (e.g., "addresses the ambiguity in F; expected to improve Clarity").
- **No scores · no probabilities · no guarantees.** Expected impact is structural/qualitative.

## G. Finding Attribution

- **Visible:** the **source finding** (the one this recommendation addresses) · related findings (context) · finding rationale · finding severity · affected CAF dimensions.
- **Always traceable to its finding** — the user can navigate recommendation → finding (View Finding, §K). Aligns with **REC-1** (traces to ≥1 finding) and **REC-8** (remains attributable throughout its lifecycle). A recommendation with no reachable finding is non-conformant.

## H. Recommendation Rationale

- **Visible:** why OSLO generated it · why it is relevant to the finding · why it may improve understanding.
- **Explainable, never opaque** — the rationale reduces to its basis (the finding + its context). A recommendation whose rationale cannot be shown is non-conformant.

## I. CAF Impact

- **Visible:** the affected CAF dimension(s) the recommendation aims to improve — qualitatively.
- **Preserved chain:** **Recommendation → User Action → Information Change → Reanalysis → CAF change.** The workspace shows the *intended* dimension of improvement, reached only through action + reanalysis.
- **Explicitly prohibited depictions:** Recommendation → CAF (direct); Recommendation → Confidence (direct); Recommendation → Reliability (any). The workspace never shows a recommendation "moving" CAF, Confidence, or Reliability.

## J. Alternative Recommendations *(most important — implements AMB-1)*

Fully implements `RECOMMENDATION_OPTION_MULTIPLICITY_RECONCILIATION_V1.md` (AMB-1) and the Recommendation Presentation Spec.

### OSLO Recommended
The recommendation OSLO **currently suggests** as primary for the finding (derived from prioritization; **no score** shown). Displayed distinctly, advisory.

### Possible Resolution Paths
A **presentation grouping of the *other* Recommendations** addressing the **same finding**, shown alongside OSLO Recommended (collapsible).
**Possible Resolution Paths are NOT:** Resolution Paths · Resolution Path objects · Clarification Candidates · Resolution Candidates. **They are simply multiple Recommendations displayed together** — no entity, field, lifecycle, or event.

### Selected Path — *what happens when a user accepts a recommendation*
- **The Selected Path becomes the accepted recommendation** — the one the user accepted.
- **OSLO Recommended may remain different** — the user may accept a non-primary recommendation; recommended ≠ selected, and both labels can coexist on different recommendations.
- **Other recommendations remain visible** — acceptance does **not** remove or hide the alternatives; they stay available (e.g., to switch later).
- **Acceptance does not remove alternatives** — the Possible Resolution Paths grouping persists.
- **Acceptance does not change assessment** — selecting/accepting changes **no** CAF/Reliability/Confidence; only the subsequent user action → information change → reanalysis can.

*(This closes the ambiguity raised in the Finding Workspace review: Selected Path is a presentation label for the accepted Recommendation; it is not a new object, it does not supersede OSLO Recommended, and it does not collapse the alternative set.)*

## K. User Actions (Release 1 only)

**Allowed:** Accept Recommendation · Reject Recommendation · **Defer Recommendation** · View Finding · Update Project Information · Trigger Reanalysis.

**Explicitly prohibited:** Execute · Apply Automatically · Run Agent · Govern · Approve · **Resolve Finding** · Modify CAF · Modify Confidence. OSLO advises; the user decides among recommendations and changes information; **reanalysis** does the rest. The workspace offers **no** path to act on the world, resolve a finding directly, or alter an assessment signal.

## L. Reanalysis Experience

- **Before reanalysis:** the recommendation and its alternatives are shown; the user evaluates. No assessment has changed from viewing/accepting/deferring.
- **During reanalysis (Running):** the workspace remains **visible/readable** (non-blocking) with an "updating — reflects previous analysis" indicator (Orientation State Model).
- **After reanalysis (Complete):** the recommendation may **remain valid**, **supersede** (be replaced by an expanded one; prior retained), or **become irrelevant** (its finding resolved). The associated **finding may weaken or close**. The workspace reflects the new state and links prior states in history.
- **Only reanalysis changes assessment** — accept/defer/reject/update by themselves change no CAF/Reliability/Confidence and do not resolve the finding.

## M. Recommendation History

- **Append-only, immutable (presentation):** the recommendation's **lifecycle history**, **supersession history**, **finding-attribution history**, and **selection history** (what the user chose over time) — all **retained, never deleted/edited**.
- The user can trace how the recommendation (and the user's choices) evolved. No edit/delete affordance on history.

## N. State Integration (presentation per status — no lifecycle change)

| Status | Workspace presentation |
|---|---|
| **Generated** | available/new; full evaluation |
| **Accepted** | marked accepted (this is the **Selected Path** if user-chosen) |
| **Rejected** | de-emphasized / in a dismissed group; viewable |
| **Deferred** | marked set-aside, still valid; re-engageable |
| **Superseded** | shown in history (retained); links to the superseding recommendation |
| *(Implemented)* | shown acted-upon; **not** presented as success (success is via reanalysis weakening/removing the finding) |

The workspace **visualizes** status; it does not redefine the lifecycle.

## O. Empty States

- **No alternatives:** show OSLO Recommended (or the single recommendation) with "No alternative recommendations" — never an empty Possible-Resolution-Paths shell implying failure.
- **No attribution:** a conformance failure, not a normal empty state (a recommendation must trace to a finding).
- **No history:** distinguish "no prior history (first generation)" from "history unavailable."
- **Not yet generated:** if recommendations are still being produced, an "Analyzing/generating…" state (per Orientation State Model), not an empty workspace.
- All empty states **distinguish none-exists / unavailable / not-yet-generated**.

## P. Progressive Disclosure

- **Always visible:** Recommendation Header + Summary (what's suggested / what it addresses) + a persistent Reanalysis Status indicator.
- **Expands in place:** Finding Attribution detail · Rationale · CAF Impact · the Possible Resolution Paths list.
- **Opens a dedicated experience:** the **source Finding** (Finding Workspace) · an **alternative Recommendation** (its own workspace) · full History.
- **Intentionally absent:** scores/percentages · execute/apply/govern affordances · manual finding resolution.

## Q. Integrity Rules

- **RWS-1.** Recommendations remain **advisory** (never commands/directives).
- **RWS-2.** Recommendations remain **finding-anchored** and traceable (REC-1/REC-8).
- **RWS-3.** **Acceptance ≠ success** — success is shown only via reanalysis weakening/removing the finding.
- **RWS-4.** **Selected Path ≠ OSLO Recommended** — the accepted recommendation may differ from OSLO's suggestion; both labels coexist.
- **RWS-5.** **Alternatives remain visible** after acceptance — acceptance never removes/hides Possible Resolution Paths.
- **RWS-6.** **Possible Resolution Paths are presentation-only** — multiple Recommendations grouped; no object/field/lifecycle/event; no Clarification/Resolution Candidate.
- **RWS-7.** The workspace never depicts Recommendation → CAF / Confidence / Reliability directly.
- **RWS-8.** **Only reanalysis changes assessment**; no workspace interaction alters a CAF/Reliability/Confidence signal.
- **RWS-9.** History is **append-only and immutable**; nothing deleted/edited.
- **RWS-10.** **No execution / apply / agent / automation** affordance.
- **RWS-11.** **No governance** (approve/govern/disposition/accepted-understanding); **no manual finding resolution**.
- **RWS-12.** The workspace is a **decision-support** surface, not a task-execution or governance surface.

## R. Conformance Requirements

A conforming workspace MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:
- **RW-C1.** Render the §D architecture in order, advisory/attribution before the decision (RWS-1/RWS-2). **Fail** if a recommendation is presented as a command.
- **RW-C2.** Keep the recommendation **traceable to its finding** at all times (RWS-2). **Fail** if finding attribution is lost.
- **RW-C3.** Present Alternatives per §J — OSLO Recommended, Possible Resolution Paths (grouped Recommendations), Selected Path; **alternatives remain visible after acceptance** (RWS-4/RWS-5/RWS-6). **Fail** if alternatives disappear after acceptance or if Selected Path replaces OSLO Recommended.
- **RW-C4.** Present CAF Impact as **Recommendation → action → reanalysis → CAF**; never Recommendation→direct-CAF/Confidence/Reliability (RWS-7).
- **RW-C5.** Expose exactly the §K actions; expose **no** Execute/Apply/Run-Agent/Govern/Approve/Resolve-Finding/Modify-CAF/Modify-Confidence (RWS-10/RWS-11). **Fail** if execution or governance appears.
- **RW-C6.** Ensure no workspace interaction changes an assessment signal; only reanalysis does (RWS-8). **Fail** if assessment changes without reanalysis.
- **RW-C7.** Keep History **append-only/immutable**; present status per §N; never present Implemented as success (RWS-3/RWS-9).
- **RW-C8.** Implement empty states distinguishing none-exists / unavailable / not-yet-generated (§O).

Conformance is **all-or-nothing**; any recommendation-as-command, lost finding attribution, alternatives-disappearing-after-acceptance, Selected-Path-replacing-OSLO-Recommended, non-reanalysis assessment change, governance affordance, or execution affordance **fails conformance**.

## S. Deferred Items

Explicitly **deferred / out of scope:** governance workflows · accepted understanding · automation · agents · execution · future orchestration capabilities · APIs · events · computation · scoring · styling · numeric tier boundaries · calibration values.

---

*This specification defines the canonical Release 1 Recommendation Workspace: an advisory-first, finding-anchored, explanation-driven decision-support environment — Header → Summary → Finding Attribution → Rationale → CAF Impact → Alternative Recommendations → History → User Actions → Reanalysis Status — that explains why a recommendation exists, traces it to its finding, presents OSLO Recommended alongside Possible Resolution Paths (multiple Recommendations, not objects), defines Selected Path as the accepted recommendation that neither replaces OSLO Recommended nor removes the alternatives, and routes change only through reanalysis. It introduces no new objects, lifecycle, events, or governance, and no execution/automation/agents/scoring/computation/APIs/styling.*

**Recommendation Workspace Specification v1 complete.**
