# OSLO Application (`code/`)

The OSLO Release 1 application: a Python cognition backend + a React frontend, built
against the ratified canon in the surrounding knowledge base. This glossary fixes the
terms used in the code so they don't drift from each other or from canon.

## Language

**Orchestration**:
The wiring of a workflow — the LangGraph graph topology, durable runs, and run lifecycle.
Lives in one place (`backend/orchestration/`). It sequences work; it does not perform it.
_Avoid_: pipeline, engine, flow controller.

**Responsibility**:
A domain module that is the single producer of one governed output (perceive, retain,
infer, evaluate, advise, disclose, adapt, acceptance). Holds the business logic.
_Avoid_: service, handler, manager.

**Wiring vs work**:
The split this codebase is organised around: orchestration holds the wiring (how steps
connect), responsibilities hold the work (what each step decides). A graph node is thin —
it delegates to a responsibility.

**Governed output**:
A cognition entity OSLO produces under contract (Finding, Issue, Recommendation,
Confidence, …). Each is produced by exactly one responsibility (hard rule #1).

**Epistemic state**:
The mandatory marker on every cognition entity: `attested-*` (a canonical receipt) or
`derived` (a recomputable projection). Canonical and derived are separate layers.
_Avoid_: status, kind, knowledge type.

**Durable run**:
A graph execution whose state is checkpointed (Supabase Postgres) so it is resumable
after interruption/deploy/failure and its history is auditable.
_Avoid_: job, task run.

**DTO**:
A request/response shape exposed over the API. Produced by the render service from a
derived projection; the FastAPI OpenAPI schema is the single source the frontend's Orval
client is generated from.
_Avoid_: model (ambiguous with domain/Pydantic models), payload.

**Data Model entity**:
An external, API-exposed resource (Project, Artifact, Finding, Recommendation, AnalysisRun…)
defined by Data Model v1.2 and exposed verbatim over REST. Distinct from the internal
cognition that backs it: the `render` service maps internal cognition (a derived Finding +
its CHR) into the Finding *entity*. Entities live in `shared/entities.py`; internal cognition
types live in `shared/epistemic.py`.
_Avoid_: model, record (ambiguous with CHR).

**Backing service**:
A datastore the app runs against: Supabase (Postgres + Auth + pgvector + Storage), Neo4j,
Redis. The app runs natively; only backing services are containerised (DL-054).

## Wave B — Understanding (Infer · Evaluate)

**Synthesized planning model**:
`SynthesizedPlanningModel` — OSLO's recomputable, Derived model built by Infer from Attested
content; backs the generated `PlanningArtifact`s (Intent/Context/Scope/Requirements/WBS/
Resources/Schedule). Derived, CHR-per-generation, user-editable, never Attested-as-truth.
_Avoid_: plan, project model (ambiguous).

**Finding**:
The single governed output of Infer — a derived gap / conflict / risk anchored to Attested
evidence. Conflicts are **surfaced, not resolved**. Derived, never Attested.

**Confidence**:
The Evaluate output meaning **trust in OSLO's understanding** — banded (0–49/50–74/75–100,
±3 edge guard), reliability-qualified, reduces to its basis (never a bare number). It is
**never project health, readiness, probability, or a score** (negative tests enforce).
_Avoid_: score, health, probability, certainty.

**CAF / Outcome Confidence**:
`CAFAssessment` — Clarity / Alignment / Feasibility, three co-equal dimensions, each a
(integrity index · band · per-dimension reliability) triple. `OutcomeConfidence` —
alignment between current state and the declared outcome. Both Derived, both Evaluate-owned.

**Fast Pass / Deep Pass**:
The two mandatory analysis modes (DL-046). **Fast Pass** is synchronous and latency-bound —
delivers Orientation Confidence + initial MRI/findings within the **&lt;60s Time-to-First-MRI**
budget; the user is never blocked on Deep. **Deep Pass** is the async, event-triggered
expansion that runs via the 00R backbone after orientation. Emissions carry `mode` +
`confidence_stage` (Orientation → Expanded → Validated) as attributes — no new entity.
_Avoid_: quick/full scan, sync/async analysis (use the canonical names).

## Determinism & test doubles (Disambiguation Register — DL-053 discipline)

**Determinism baseline**:
The pinned reference a replayed/recomputed output is checked against — the
**(configuration × fixture × model-version)** triple (Determinism Note DT-5/DT-10). A
difference in the model-version component is a **new baseline, not a regression** (DT-6).

**Recorded model-response fixture**:
A captured, version-stamped LLM output used as the model/fixture component of the
determinism baseline so CI exercises AI offline and deterministically (ADR-0004). The live
model runs only in dev and a nightly baseline-update check.
_Avoid_: **"replay", "cassette"** — `replay` is reserved (see below); `cassette` is not
canon.

**Replay** (RESERVED — do not reuse):
Canonically (Determinism Note §5; DT-3; REPLAY-T1…T6) the reconstruction of state from the
append-only event log that **explicitly does NOT re-run the LLM**. The LLM test-double is a
*recorded model-response fixture*, **not** a replay. Keep the two strictly separate in code
and test names.

## Wave C — Advisory (Advise)

**Recommendation**:
A Derived, governable **candidate response** produced by Advise, **anchored to a Finding/Issue**
(never standalone — "Recommendation-only-in-Finding-context"). Types: suggested-action,
candidate-improvement. Advise *proposes*; it never accepts, scores, governs, or executes.
Multiple alternatives are *multiple Recommendations*, not a separate object.
_Avoid_: action, decision, resolution-path-object.

**Clarification request**:
A Derived Advise output that **requests user input** to resolve blocking ambiguity (an
information request, not an action); the answer feeds Perceive → recompute.

**Suggested fix**:
A Derived Advise **candidate edit** to a named artifact, anchored to a Finding. OSLO **never
applies it autonomously** (Critical invariant) — applying is a user-initiated artifact edit that
triggers recompute. _Avoid_: auto-fix, patch.

**Validation recommendation**:
A Recommendation type seeking **stakeholder confirmation** (validate an expectation / confirm a
criterion); routes to a CAF Review Request on user action. Derived.

**Resolution path** (presentation-only):
The rendering of *multiple Recommendations* as paths — a **presentation substructure**, never a
canonical object. Emitting a standalone Resolution-Path object is a rejected negative.

**Recommendation state** (user-owned, DL-055):
The lifecycle `Generated → {Accepted | Rejected | Deferred} → Implemented (+ Superseded)`. Advise
emits only `Generated`; **Accept/Defer/Reject/Apply are user actions recorded by Wave U**, not
Advise. "Modify" is not a state — a user edit supersedes via recompute. "Discuss"/"Share For
Review" are collaboration affordances, not states.

## Wave U — User Acceptance & Reconciliation (additive, non-governance)

**User Acceptance Record (UAR)**:
The append-only, **user-attested** canonical record that "user U, at time T, took action A
(accept/reject/defer/direct-edit) on item I at **version-pin** V". **version-pin is mandatory**
(no valid UAR without it) and pins the exact `CognitionHistoryRecord` accepted. Decoupled — it
marks no item true/approved. _Avoid_: approval, sign-off, governance decision.

**Plan fact**:
A **user-attested `AttestedAssertion`** (`attesting_source=user`, `attested-user`) — the
confirmed content recorded as **factual in the plan, NOT world-truth** (OSLO certifies neither).
Written on accept / direct-edit (never on reject/defer). The **user** authors it; OSLO never
auto-promotes its own Derived recommendation. _Avoid_: truth, fact (unqualified), approval.

**Acceptance-Impact Assessment**:
A **Derived** cognition (Infer/Evaluate) that fires when the value behind a *user-accepted* item
drifts **≥10 pts or a band change** vs the version-pinned acceptance (Calibration §3) — surfaced
as "a decision you confirmed is affected". Recomputable, appends a CHR; never canonical.

**Never self-accept** (hard rule #5, DL-043 G):
The **user is the acceptance authority**; OSLO records and reasons but never accepts on its own.
Acceptance ≠ world-truth, ≠ OSLO-approval, ≠ governance; a UAR is **not** a Governance Decision;
OSLO-level acceptance/approval/execution is Future (Outcome Governance, out of R1).
