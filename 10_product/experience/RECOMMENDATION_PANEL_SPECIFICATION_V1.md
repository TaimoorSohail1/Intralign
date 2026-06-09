# Recommendation Panel Specification v1

**Type:** Panel specification (user experience / interaction model only)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Canonical surface** per `FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md` (Option A — Panel Model, ratified). **Repositions** `RECOMMENDATION_WORKSPACE_SPECIFICATION_V1.md` (superseded; retained for history).
**Sits below (authoritative — presents, must not modify):** `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` · `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md` · `FINDING_SYSTEM_SPECIFICATION_V1.md` · `FINDING_PRESENTATION_SPECIFICATION_V1.md` · `FINDING_PANEL_SPECIFICATION_V1.md` · `RECOMMENDATION_OPTION_MULTIPLICITY_RECONCILIATION_V1.md` · `MRI_WORKSPACE_SPECIFICATION_V1.md` · `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` · `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1.md` · `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · `SIXTY_SECOND_ORIENTATION_WORKFLOW_SPECIFICATION_V1.md` · `ORIENTATION_STATE_MODEL_V1.md` · CAF Assessment · Reliability v2 · Confidence v2 · Release 1 Tier Definitions.

> **Non-negotiable.** UX/interaction only. **No** new objects, lifecycle, events, or governance concepts; **no** scoring, CAF/Confidence/Reliability computation, generation, execution, agents, automation, APIs, or styling. The Recommendation Panel is **contextual, advisory-first, finding-anchored, explanation-driven, alternative-aware, reanalysis-driven** — a panel opened **only from Finding context**, **not a standalone destination**. **Only reanalysis changes assessment.**

**Surface model (Option A):** the Recommendation Panel is a **contextual panel** opened **only from a Finding Panel** (Finding context), **subordinate to the Finding Panel**. It **cannot be opened directly from the Artifact Workspace without Finding context**. It opens over/beside the Finding context, preserving it, and closes back to it. It is **not** a primary navigation destination.

The architecture it serves:
```text
Project Overview → MRI Workspace → Artifact Workspace → Finding Panel → Recommendation Panel
(object chain) Finding → Recommendation → User Action → Information Change → Reanalysis → Assessment Change
```

---

## A. Purpose

The Recommendation Panel is the contextual surface opened when a user selects a Recommendation **from a Finding Panel** (Finding context). It answers: **"Why does this recommendation exist, what finding does it address, what alternatives exist, what does OSLO recommend, what happens if I choose a different path, and what should I do next?"** It is where the user **evaluates** an advisory recommendation in the context of its finding and its alternatives — **without leaving the Finding context** — then accepts/defers/rejects, updates information, or reanalyzes.

## B. Scope

**In scope:** presentation/interaction for a single Recommendation in a contextual panel opened from Finding context — header, summary, finding attribution, rationale, CAF impact, alternatives, history, user actions, reanalysis status, and open/close context preservation.

**Explicitly excluded:** standalone-destination/navigation framing · opening without Finding context · execution · governance · accepted understanding · agents · automation · task management · project-health management. (Plus computation/generation/API/events/styling — Deferred §S.)

## C. Panel Goals (questions answered)

- **"Why was this recommendation created?"** → Rationale (§H).
- **"Which finding does it address?"** → Finding Attribution (§G).
- **"Why is OSLO recommending it?"** → OSLO Recommended (§J) + Rationale.
- **"What alternatives exist?"** → Possible Resolution Paths (§J).
- **"What happens if I choose another option?"** → Selected Path semantics (§J).
- **"What did I previously choose?"** → Selection history (§M).
- **"What changed over time?"** → History (§M) + Reanalysis Status (§L).
- **"What should I do next?"** → User Actions (§K).
- **"How do I get back?"** → close the panel; the originating Finding context is preserved (§D).

## D. Panel Architecture & Context Behavior (single canonical, top → bottom)

**Opening & context.** The Recommendation Panel opens **in context** from a **Finding Panel** — over/beside the Finding context it was invoked from. The Finding context **remains beneath** the panel; closing returns the user **exactly** there. It **cannot be opened** without Finding context (no direct Artifact/MRI entry). It is never a separate destination (Global Navigation Object Context; NAV-8).

**Content order (top → bottom):**

1. **Recommendation Header**
2. **Recommendation Summary**
3. **Finding Attribution**
4. **Recommendation Rationale**
5. **CAF Impact**
6. **Alternative Recommendations** (OSLO Recommended · Possible Resolution Paths · Selected Path)
7. **Recommendation History**
8. **User Actions**
9. **Reanalysis Status**

**Rationale.** The order is the evaluation arc: **what is suggested** (Header/Summary) → **why it's grounded** (Finding Attribution) → **why it's advised** (Rationale) → **what it aims to improve** (CAF Impact) → **what else could be chosen** (Alternatives) → **what changed** (History) → **the decision** (User Actions) → **what's updating** (Reanalysis Status). Understanding-and-attribution precede the decision (advisory-first, finding-anchored); the decision sits near the bottom, after alternatives can be compared; reanalysis status anchors the foot as the only path to assessment change. Reanalysis Status may also persist as an indicator regardless of scroll.

## E. Recommendation Header

- **Visible:** recommendation title · type (user-friendly) · lifecycle status (§N) · **effort** (Low/Medium/High) · affected CAF dimension(s).
- **Advisory only** — the header frames a suggestion, never a directive. No "execute/apply" affordance here.

## F. Recommendation Summary

- **Visible:** the recommendation explanation · its intent · **what understanding weakness it addresses** · **expected impact (qualitative only)** (e.g., "addresses the ambiguity in F; expected to improve Clarity").
- **No scores · no probabilities · no guarantees.** Expected impact is structural/qualitative.

## G. Finding Attribution

- **Visible:** the **source finding** (the one this recommendation addresses) · related findings (context) · finding rationale · finding severity · affected CAF dimensions.
- **Always traceable to its finding** — the user can navigate recommendation → finding (View Finding returns to the Finding Panel, §K). Aligns with **REC-1** (traces to ≥1 finding) and **REC-8** (remains attributable throughout its lifecycle). A recommendation with no reachable finding is non-conformant. *(This panel can only have been opened from Finding context, so attribution is structurally guaranteed.)*

## H. Recommendation Rationale

- **Visible:** why OSLO generated it · why it is relevant to the finding · why it may improve understanding.
- **Explainable, never opaque** — the rationale reduces to its basis (the finding + its context). A recommendation whose rationale cannot be shown is non-conformant.

## I. CAF Impact

- **Visible:** the affected CAF dimension(s) the recommendation aims to improve — qualitatively.
- **Preserved chain:** **Recommendation → User Action → Information Change → Reanalysis → CAF change.** The panel shows the *intended* dimension of improvement, reached only through action + reanalysis.
- **Explicitly prohibited depictions:** Recommendation → CAF (direct); Recommendation → Confidence (direct); Recommendation → Reliability (any). The panel never shows a recommendation "moving" CAF, Confidence, or Reliability.

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

*(Selected Path is a presentation label for the accepted Recommendation; it is not a new object, it does not supersede OSLO Recommended, and it does not collapse the alternative set.)*

## K. User Actions (Release 1 only)

**Allowed:** Accept Recommendation · Reject Recommendation · **Defer Recommendation** · View Finding (returns to the Finding Panel) · Update Project Information · Trigger Reanalysis · Close Panel (returns to Finding context).

- **Limit-reached interaction (Free tier).** A capped action surfaced here — e.g. **applying a Suggested Fix at the daily allowance** — follows the shared **limit-reached interaction rule** (`12_freemium_tier_behavior_logic.md`): the action **stays enabled**, the attempt is **gated** (server `429`), and the surface presents the **upgrade prompt (UP-1) + resolution (upgrade / wait for reset)** — **never** a disabled/hidden control or a raw error. Presentation/interaction only; values per Tier Definitions.

**Explicitly prohibited:** Execute · Apply Automatically · Run Agent · Govern · Approve · **Resolve Finding** · Modify CAF · Modify Confidence. OSLO advises; the user decides among recommendations and changes information; **reanalysis** does the rest. The panel offers **no** path to act on the world, resolve a finding directly, or alter an assessment signal.

## L. Reanalysis Experience

- **Before reanalysis:** the recommendation and its alternatives are shown; the user evaluates. No assessment has changed from viewing/accepting/deferring.
- **During reanalysis (Running):** the panel remains **visible/readable** (non-blocking) with an "updating — reflects previous analysis" indicator (Orientation State Model); the Finding context beneath likewise remains visible.
- **After reanalysis (Complete):** the recommendation may **remain valid**, **supersede** (be replaced by an expanded one; prior retained), or **become irrelevant** (its finding resolved). The associated **finding may weaken or close**. The panel reflects the new state and links prior states in history.
- **Only reanalysis changes assessment** — accept/defer/reject/update by themselves change no CAF/Reliability/Confidence and do not resolve the finding.

## M. Recommendation History

- **Append-only, immutable (presentation):** the recommendation's **lifecycle history**, **supersession history**, **finding-attribution history**, and **selection history** (what the user chose over time) — all **retained, never deleted/edited**.
- The user can trace how the recommendation (and the user's choices) evolved. No edit/delete affordance on history.

## N. State Integration (presentation per status — no lifecycle change)

| Status | Panel presentation |
|---|---|
| **Generated** | available/new; full evaluation |
| **Accepted** | marked accepted (this is the **Selected Path** if user-chosen) |
| **Rejected** | de-emphasized / in a dismissed group; viewable |
| **Deferred** | marked set-aside, still valid; re-engageable |
| **Superseded** | shown in history (retained); links to the superseding recommendation |
| *(Implemented)* | shown acted-upon; **not** presented as success (success is via reanalysis weakening/removing the finding) |

The panel **visualizes** status; it does not redefine the lifecycle.

## O. Empty States

- **No alternatives:** show OSLO Recommended (or the single recommendation) with "No alternative recommendations" — never an empty Possible-Resolution-Paths shell implying failure.
- **No attribution:** a conformance failure, not a normal empty state (a recommendation must trace to a finding; structurally guaranteed by Finding-context-only entry).
- **No history:** distinguish "no prior history (first generation)" from "history unavailable."
- **Not yet generated:** if recommendations are still being produced, an "Analyzing/generating…" state (per Orientation State Model), not an empty panel.
- All empty states **distinguish none-exists / unavailable / not-yet-generated**.

## P. Progressive Disclosure

- **Always visible:** Recommendation Header + Summary (what's suggested / what it addresses) + a persistent Reanalysis Status indicator.
- **Expands in place:** Finding Attribution detail · Rationale · CAF Impact · the Possible Resolution Paths list.
- **Opens a contextual panel / returns:** the **source Finding** (returns to the Finding Panel) · an **alternative Recommendation** (its own Recommendation Panel, from the same Finding context) · full History.
- **Intentionally absent:** standalone-destination framing; scores/percentages · execute/apply/govern affordances · manual finding resolution.

## Q. Integrity Rules

- **RP-1.** Recommendations remain **advisory** (never commands/directives).
- **RP-2.** Recommendations remain **finding-anchored** and traceable (REC-1/REC-8); the panel opens **only** from Finding context.
- **RP-3.** **Acceptance ≠ success** — success is shown only via reanalysis weakening/removing the finding.
- **RP-4.** **Selected Path ≠ OSLO Recommended** — the accepted recommendation may differ from OSLO's suggestion; both labels coexist.
- **RP-5.** **Alternatives remain visible** after acceptance — acceptance never removes/hides Possible Resolution Paths.
- **RP-6.** **Possible Resolution Paths are presentation-only** — multiple Recommendations grouped; no object/field/lifecycle/event; no Clarification/Resolution Candidate.
- **RP-7.** The panel never depicts Recommendation → CAF / Confidence / Reliability directly.
- **RP-8.** **Only reanalysis changes assessment**; no panel interaction alters a CAF/Reliability/Confidence signal.
- **RP-9.** History is **append-only and immutable**; nothing deleted/edited.
- **RP-10.** **No execution / apply / agent / automation** affordance.
- **RP-11.** **No governance** (approve/govern/disposition/accepted-understanding); **no manual finding resolution**.
- **RP-12.** The Recommendation Panel is a **contextual decision-support surface subordinate to the Finding Panel** — **not a standalone destination**, **cannot be opened without Finding context**, and is not a task-execution or governance surface.
- **RP-13.** The panel **opens in context and preserves it** — opening/closing never discards the originating Finding context.

## R. Conformance Requirements

A conforming Recommendation Panel MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:
- **RP-C1.** Open **only from Finding context** (a Finding Panel), subordinate to it, preserving and returning to that context; **never** openable directly from Artifact/MRI without Finding context (RP-2/RP-12/RP-13). **Fail** if it is a standalone destination, opens without Finding context, or discards context.
- **RP-C2.** Render the §D content in order, advisory/attribution before the decision (RP-1/RP-2). **Fail** if a recommendation is presented as a command.
- **RP-C3.** Keep the recommendation **traceable to its finding** at all times (RP-2). **Fail** if finding attribution is lost.
- **RP-C4.** Present Alternatives per §J — OSLO Recommended, Possible Resolution Paths (grouped Recommendations), Selected Path; **alternatives remain visible after acceptance** (RP-4/RP-5/RP-6). **Fail** if alternatives disappear after acceptance or if Selected Path replaces OSLO Recommended.
- **RP-C5.** Present CAF Impact as **Recommendation → action → reanalysis → CAF**; never Recommendation→direct-CAF/Confidence/Reliability (RP-7).
- **RP-C6.** Expose exactly the §K actions; expose **no** Execute/Apply/Run-Agent/Govern/Approve/Resolve-Finding/Modify-CAF/Modify-Confidence (RP-10/RP-11). **Fail** if execution or governance appears.
- **RP-C7.** Ensure no panel interaction changes an assessment signal; only reanalysis does (RP-8). **Fail** if assessment changes without reanalysis.
- **RP-C8.** Keep History **append-only/immutable**; present status per §N; never present Implemented as success (RP-3/RP-9).
- **RP-C9.** Implement empty states distinguishing none-exists / unavailable / not-yet-generated (§O).

Conformance is **all-or-nothing**; any standalone-destination framing, opening without Finding context, context loss on open/close, recommendation-as-command, lost finding attribution, alternatives-disappearing-after-acceptance, Selected-Path-replacing-OSLO-Recommended, non-reanalysis assessment change, governance affordance, or execution affordance **fails conformance**.

## S. Deferred Items

Explicitly **deferred / out of scope:** governance workflows · accepted understanding · automation · agents · execution · future orchestration capabilities · APIs · events · computation · scoring · styling · numeric tier boundaries · calibration values.

---

*This specification defines the canonical Release 1 Recommendation Panel (Option A — Panel Model): a contextual, advisory-first, finding-anchored, explanation-driven, alternative-aware, reanalysis-driven panel opened only from a Finding Panel and subordinate to it — Header → Summary → Finding Attribution → Rationale → CAF Impact → Alternative Recommendations → History → User Actions → Reanalysis Status — that explains why a recommendation exists, traces it to its finding, presents OSLO Recommended alongside Possible Resolution Paths (multiple Recommendations, not objects), defines Selected Path as the accepted recommendation that neither replaces OSLO Recommended nor removes the alternatives, preserves originating Finding context on open/close, cannot be opened without Finding context, and routes change only through reanalysis. It is not a standalone destination. It introduces no new objects, lifecycle, events, or governance, and no execution/automation/agents/scoring/computation/APIs/styling.*

**Recommendation Panel Specification v1 complete.**
