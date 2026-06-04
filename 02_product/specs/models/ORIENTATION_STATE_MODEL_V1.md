# Orientation State Model v1

**Type:** UX state model specification (presentation/workflow only)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Consistent with (must not modify):** Outcome Confidence Doctrine · CAF Assessment · CAF Scoring v2 · Reliability v2 · Confidence v2 · `FINDING_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · `FINDING_PRESENTATION_SPECIFICATION_V1.md` · `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` · `SIXTY_SECOND_ORIENTATION_WORKFLOW_SPECIFICATION_V1.md`.

> **Non-negotiable.** **User-visible states only.** Defines **no** CAF/Confidence/Reliability logic, finding/recommendation generation, governance, execution, agents, automation, API contracts, event triggers, or implementation. Transition conditions are described in **user-observable** terms (e.g., "when analysis finishes"), never as events/APIs. The Orientation is **informational**; **no state changes any assessment signal — only reanalysis does.**

---

## A. Purpose

Define the complete **user-experience lifecycle** of the 60-Second Orientation — from project upload through Fast Analysis, Deep Analysis, reanalysis, completion, and error — so the user experience is **consistent** and there is **no ambiguity about what the user sees while analysis is running.**

## B. Scope

In scope: the **user-visible states** of the Orientation and what the user sees, can do, and how newer analysis supersedes older. Out of scope: everything computational, generative, governance/execution, and all API/event/implementation concerns (Deferred §O).

## C. State Model Overview

**Recommended canonical Release 1 states (8):**
`Uploaded · Analyzing · Fast Pass Complete · Deep Analysis Running · Deep Analysis Complete · Reanalysis Running · Reanalysis Complete · Error`.

**Justification.** Each state conveys a **distinct user-visible meaning**. They fall into three behavioral groups:
- **Pre-orientation** (no orientation yet): `Uploaded`, `Analyzing`.
- **Orientation-visible** (the orientation is shown): `Fast Pass Complete`, `Deep Analysis Running`, `Deep Analysis Complete`, `Reanalysis Running`, `Reanalysis Complete`.
- **Fault:** `Error`.

The **Running** states (`Analyzing`, `Deep Analysis Running`, `Reanalysis Running`) differ by *what is being computed and whether an orientation is already visible* — a meaningful UX distinction, so they are kept separate rather than collapsed into one "loading." `Deep Analysis Complete` and `Reanalysis Complete` share the same "current orientation available" layout but are distinguished by **what triggered** the run (first deep pass vs a subsequent reanalysis after the user changed information). Keeping all 8 eliminates ambiguity (the document's purpose); merging would hide the provisional-vs-current and first-vs-update distinctions.

**Provisional vs current (key signal):** an orientation is **provisional** whenever a further analysis is **running or pending** (`Fast Pass Complete`, `Deep Analysis Running`, `Reanalysis Running` — a visible "analysis in progress" indicator). It is **current** when **no analysis is running** (`Deep Analysis Complete`, `Reanalysis Complete`). Even "current" is never "final/certain" — new information triggers reanalysis (consistent with the Confidence Doctrine; §L).

## D. State Definitions

### 1. Uploaded
- **Purpose:** the project's inputs are in; analysis has not yet produced an orientation.
- **User message:** "Project received. Starting analysis…"
- **Visible information:** project name; a summary of submitted inputs; **no** orientation content yet.
- **Allowed user actions:** view submitted inputs; (await analysis).
- **Transition conditions:** when Fast Analysis begins → **Analyzing**.
- **Supersession:** none (first state).

### 2. Analyzing (Fast Analysis in progress)
- **Purpose:** the Fast Pass is producing the first orientation.
- **User message:** "Building your 60-Second Orientation…"
- **Visible information:** a non-deceptive progress indicator (optionally a skeleton of the orientation layout); **no** confidence/CAF/findings yet.
- **Allowed user actions:** view inputs; wait. No orientation actions.
- **Transition conditions:** when the Fast Pass finishes → **Fast Pass Complete**; if it fails → **Error**.
- **Supersession:** none.

### 3. Fast Pass Complete (provisional orientation)
- **Purpose:** the provisional 60-Second Orientation is available.
- **User message:** "Your 60-Second Orientation is ready. This is a **provisional** read — Deep Analysis is in progress and may refine it."
- **Visible information:** the full Orientation per the Workflow Spec (Outcome Confidence **with reliability qualifier**, CAF with Alignment/Feasibility marked preliminary, Reliability, Top Findings, OSLO Recommended + Possible Resolution Paths, Summary) + a **provisional** indicator.
- **Allowed user actions:** view findings/recommendations; Accept/Reject/Defer a recommendation; Update Project Information; Trigger Reanalysis (the §9 Orientation actions).
- **Transition conditions:** when Deep Analysis is underway → **Deep Analysis Running** (orientation stays visible); if the user changes information → **Reanalysis Running**; if Deep fails → **Error** (this orientation retained).
- **Supersession:** will be superseded by **Deep Analysis Complete**; nothing prior to retain.

### 4. Deep Analysis Running (provisional orientation visible, deepening)
- **Purpose:** Deep Analysis is enriching understanding **without blocking** the user; the provisional orientation remains visible.
- **User message:** "Deep Analysis in progress — refining your understanding. The current view is **provisional**."
- **Visible information:** the provisional orientation + a background "deepening" indicator.
- **Allowed user actions:** same as Fast Pass Complete (non-blocking).
- **Transition conditions:** when Deep finishes → **Deep Analysis Complete**; if it fails → **Error** (provisional orientation retained as last-good); if the user changes information → **Reanalysis Running**.
- **Supersession:** the provisional orientation will be superseded by Deep Analysis Complete.

### 5. Deep Analysis Complete (current orientation)
- **Purpose:** a fuller, better-supported orientation — the **current** understanding for this cycle.
- **User message:** "Deep Analysis complete — this is your **current** understanding. Confidence may have **risen or fallen** as understanding deepened (a change is honest improvement, not a problem)."
- **Visible information:** the updated Orientation (recalculated confidence, expanded findings/recommendations); **no** provisional indicator (no analysis running); a link to history.
- **Allowed user actions:** full Orientation actions (view/accept/reject/defer/update/reanalyze).
- **Transition conditions:** if the user changes information / acts in a way that changes information → **Reanalysis Running**.
- **Supersession:** **supersedes** the Fast/provisional orientation; the prior is **retained in history** (never deleted).

### 6. Reanalysis Running (updating; prior orientation visible)
- **Purpose:** re-analyzing after the user changed project information; the prior current orientation stays visible.
- **User message:** "Updating your understanding based on your changes… The current view reflects the **previous** analysis until this finishes."
- **Visible information:** the prior (current) orientation + an "updating" indicator.
- **Allowed user actions:** Orientation actions (non-blocking); prior orientation remains readable.
- **Transition conditions:** when reanalysis finishes → **Reanalysis Complete**; if it fails → **Error** (prior orientation retained as last-good).
- **Supersession:** the prior orientation will be superseded by Reanalysis Complete.

### 7. Reanalysis Complete (updated current orientation)
- **Purpose:** the updated orientation reflecting the changed information.
- **User message:** "Understanding updated. Confidence may have changed because your project information changed."
- **Visible information:** the updated Orientation; the prior retained in history.
- **Allowed user actions:** full Orientation actions.
- **Transition conditions:** further information change → **Reanalysis Running** (the recurring loop).
- **Supersession:** **supersedes** the prior orientation; prior **retained in history**.
- *(Note: structurally the same "current orientation available" layout as Deep Analysis Complete; distinguished by trigger — a user-driven reanalysis vs the first deep pass.)*

### 8. Error (analysis could not complete)
- **Purpose:** an analysis (Fast/Deep/Reanalysis) failed.
- **User message:** "We couldn't complete the analysis. Your **previous** understanding (if any) is preserved. You can retry."
- **Visible information:** an error banner + retry; if a prior orientation exists, it **remains visible** as last-good; if the very first analysis failed (no prior), an explanatory empty/error state with retry.
- **Allowed user actions:** Retry; view the prior orientation (if any); Update Project Information.
- **Transition conditions:** on retry → the corresponding **Running** state (**Analyzing** or **Reanalysis Running**); on success → the corresponding **Complete** state.
- **Supersession:** a failed run **supersedes nothing**; the last-good orientation remains current.

## E. State Transition Model

```text
Uploaded → Analyzing → Fast Pass Complete → Deep Analysis Running → Deep Analysis Complete
                                                                          │
                                   (user changes information / acts)      ▼
                                          Reanalysis Running ⇄ Reanalysis Complete
                                                  │  (further change loops)
   Any Running state ──(failure)──▶ Error ──(retry)──▶ back to that Running state
   (Error preserves the last-good orientation as current)
```

- Forward progress: pre-orientation → provisional → current.
- Recurring loop: any current orientation + information change → Reanalysis Running → Reanalysis Complete.
- Error is reachable from any Running state and returns to it on retry, **without** discarding the last-good orientation.

## F. Upload Experience
`Uploaded → Analyzing` — the user sees confirmation of intake and an immediate, honest "starting analysis" signal; no orientation is fabricated before it exists.

## G. Fast Analysis Experience
`Analyzing → Fast Pass Complete` — a clear "building your orientation" progress signal, resolving into the **provisional** orientation with its provisional indicator. The user can begin reading and acting immediately.

## H. Deep Analysis Experience
`Fast Pass Complete → Deep Analysis Running → Deep Analysis Complete` — Deep runs **non-blocking** with the provisional orientation visible; on completion the orientation updates to **current**, and the UX communicates that a **rise or fall in confidence is expected and honest** (deeper understanding, not deterioration).

## I. Reanalysis Experience
`(current) → Reanalysis Running → Reanalysis Complete` — triggered by the user changing project information; the prior orientation stays visible while updating; on completion the orientation reflects the new information, with the prior retained in history. **Only this loop changes the assessment the user sees.**

## J. Error Experience
`Any Running → Error → (retry) → Running` — failures never blank the screen of a known-good orientation; the last-good orientation is preserved and labeled, with a clear retry. A first-analysis failure shows an explanatory state, not a fabricated orientation.

## K. Supersession Model

- Every **completed** analysis (Fast → Deep → Reanalysis) produces an orientation that **supersedes** the prior; the **visible orientation is always the latest**.
- **Superseded orientations are retained in history — never deleted** (append-only); the user can reach prior orientations.
- **Failed runs supersede nothing**; the last-good orientation remains current.
- Supersession is **presentation-level** here (which orientation is shown/historical); it asserts no assessment computation.

## L. User Expectations Model

- **Provisional means "still working":** whenever an analysis is running or pending (Fast Pass Complete, Deep/Reanalysis Running), the orientation is labeled provisional/updating and may change.
- **Current means "no analysis running":** Deep/Reanalysis Complete show the current understanding — but **never "final" or "certain."** New information will trigger reanalysis.
- **Confidence is trust in understanding** (reliability-qualified), **not** project health or outcome probability; a change after Deep/Reanalysis is honest evolution.
- **The user is in control:** the user reads, decides, and acts; the orientation never acts for them.

## M. Integrity Rules

- **ORST-1.** The Orientation (in every state) is **informational** — no state performs an action for the user.
- **ORST-2.** **No state modifies CAF.**
- **ORST-3.** **No state modifies Reliability.**
- **ORST-4.** **No state modifies Confidence.**
- **ORST-5.** **Only reanalysis changes the assessment** the user sees (Reanalysis Running → Complete; or Deep → Complete) — never a view/accept/defer/select interaction by itself.
- **ORST-6.** **Fast Pass is provisional** and labeled so; Deep Analysis follows.
- **ORST-7.** **Deep Analysis may raise or lower Confidence**, presented as honest improvement, not deterioration.
- **ORST-8.** **Supersession never deletes** prior analysis; superseded orientations are retained in history.
- **ORST-9.** No **governance** action/state appears in any orientation state.
- **ORST-10.** No **execution** action appears.
- **ORST-11.** No **agent** action appears.
- **ORST-12.** No **automation** behavior is defined; running/updating is communicated, not orchestrated, here.
- **ORST-13.** A known-good orientation is **never blanked by an Error**; last-good is preserved.

## N. Conformance Requirements

A conforming implementation MUST (objective, structural, **non-numeric**):
- **ORST-C1.** Implement exactly the 8 canonical states (§C); each state shows its defined Visible Information and permits only its Allowed Actions (§D).
- **ORST-C2.** Display a **provisional** indicator in Fast Pass Complete and in all Running states; **omit** it in Deep/Reanalysis Complete (§C/§L).
- **ORST-C3.** Keep any prior **current** orientation visible during Deep Analysis Running and Reanalysis Running (non-blocking) (§H/§I).
- **ORST-C4.** Ensure **no** state interaction (view/accept/reject/defer/select/update) changes a CAF/Reliability/Confidence signal; only the reanalysis/deep loop does (ORST-2…ORST-5).
- **ORST-C5.** Preserve the **last-good** orientation on Error and provide retry; never fabricate an orientation (ORST-13).
- **ORST-C6.** On any completed analysis, show the **latest** orientation and **retain** the prior in history (append-only) (ORST-8).
- **ORST-C7.** Present Confidence **reliability-qualified** and **never** as health/probability; present a post-Deep change as honest (ORST-6/ORST-7).
- **ORST-C8.** Expose **no** governance/execution/agent/automation affordance in any state (ORST-9…ORST-12).

Conformance is **all-or-nothing**; any non-reanalysis assessment change, any deleted prior orientation, any blanked last-good orientation, any confidence-as-health framing, or any governance/execution/agent affordance **fails conformance**.

## O. Deferred Items

Explicitly **deferred / out of scope**: API contracts; event triggers; analysis timing/latency; recommendation/finding generation; CAF/Confidence/Reliability computation; governance/execution/agent/automation workflows; visual design/wireframes; numeric tier boundaries; calibration values.

---

*This specification defines the canonical Release 1 user-visible state lifecycle of the 60-Second Orientation — Uploaded → Analyzing → Fast Pass Complete → Deep Analysis Running → Deep Analysis Complete → Reanalysis Running → Reanalysis Complete (+ Error) — with provisional-vs-current signaling, non-blocking deepening, append-only supersession, and last-good preservation on error. It is presentation/workflow state modeling only: no doctrine, scoring, calculation, generation, governance, execution, automation, agents, APIs, events, or implementation, and it preserves that only reanalysis changes assessment and confidence is trust in understanding.*

**Orientation State Model v1 complete.**
