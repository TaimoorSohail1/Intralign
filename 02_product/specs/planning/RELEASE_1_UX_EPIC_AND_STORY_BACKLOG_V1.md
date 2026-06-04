# Release 1 UX Epic & Story Backlog v1

**Document Type:** Backlog Structure (planning only — UX scope) · **Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Built from / subordinate to (authoritative — must not redefine):** `RELEASE_1_UX_HANDOFF_PACKAGE_SPECIFICATION_V1.md` · `RELEASE_1_UX_IMPLEMENTATION_READINESS_REVIEW_001.md` · `RELEASE_1_UX_EXECUTION_PLANNING_PACKAGE_V1.md` · `RELEASE_1_UX_EXECUTION_PLAN_V1.md` · `RELEASE_1_UX_SCOPE_FREEZE_AND_BACKLOG_CONTROL_SPECIFICATION_V1.md` · `UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION_001.md` · the canonical active UX spec set (Handoff §D).

> **Non-negotiable constraints.** Backlog structure only. **Redefines no UX surface**; introduces **no** implementation, APIs, events, schemas, styling, governance, execution, automation, agents, permissions enforcement, billing implementation, notification infrastructure, or assessment behavior. **Only reanalysis changes assessment.**

> **Required guardrails (binding):** Source specs govern · only canonical active specs in scope · superseded specs not implemented · Recommendation Panel opens only in Finding context · Outcome Confidence is trust in understanding, never project health/readiness/probability · stale means previous analysis, never current · only reanalysis changes assessment · history append-only · Chat & Companion are not destinations · Awareness creates no tasks/obligations · Export packages existing understanding only · Invite/share defines no permission enforcement · new constructs classified before specification · spec conflicts escalated, not resolved in code.

> **Acceptance precedence.** Each story's full acceptance set is the **source spec's Conformance Requirements** (positive) + **explicit fail conditions** (negative). Criteria below are anchors, not replacements; the **source spec governs**.

---

## A. Backlog Purpose

Convert the finalized, frozen, audit-verified Release 1 UX architecture into an **execution-ready backlog** — epics and stories with acceptance criteria, negative criteria, QA scenarios, and dependencies — without redefining surfaces or specifying implementation.

## B. Backlog Scope

**In scope:** epic list; per-epic story breakdown with the required fields (name, source specs, construct type, user value, included stories, out-of-scope boundaries, acceptance criteria, QA scenarios, dependencies); story acceptance & negative criteria; cross-surface invariant stories; QA story set; dependency order; deferred/out-of-scope; owner clarifications; drift warnings; Definition of Ready; Definition of Done.

**Out of scope:** tickets in a tracker; estimates/assignees/timeline; implementation/APIs/events/schemas/styling; governance/execution/automation/agents; permissions enforcement; billing/notification infrastructure; assessment behavior; Release 2.

## C. Epic List

E1 App Shell & Navigation · E2 Entry & Onboarding · E3 Project Discovery · E4 Project Overview · E5 MRI Diagnostic Discovery · E6 Artifact Workspace & Editing · E7 Finding & Recommendation Panels · E8 Understanding Companion · E9 OSLO Chat · E10 Collaboration & Sharing (+ Invite/Share) · E11 Awareness · E12 History & Timeline · E13 Export & Share-Out · E14 Help & Support · E15 Settings & Tier Visibility · **E16 Cross-Surface Invariants** · **E17 QA & Acceptance.**

## D–I. Epics (story breakdown, acceptance, QA, dependencies)

### E1 — App Shell & Navigation
- **Source specs:** Global Navigation, Understanding Journey · **Construct type:** Workspace shell + connective layer · **User value:** users always know where they are and can move/return without getting lost.
- **Stories:** S1.1 global nav frame (Workspace Home/Project List/Create/Settings/Account); S1.2 three-context model (Workspace/Project/Object); S1.3 journey transitions (Overview→MRI→Artifact→Finding→Recommendation, reinforced-not-enforced); S1.4 return/recovery (jump-to-primary; never stranded); S1.5 stale surfaced honestly during navigation.
- **Out-of-scope:** making Panels/Companion/Chat destinations; deep-link/URL mechanics; mobile nav.
- **Acceptance:** only Workspaces are destinations; direct jumps among Overview/MRI/Artifact once understanding exists; context preserved on every transition (NAV-C*). **Negative:** lifecycle gated beyond initial-analysis; context discarded; workflow/pipeline nav appears.
- **QA:** navigate full chain + back; attempt Recommendation without Finding (blocked); leave/return without context loss.
- **Dependencies:** none (foundation).

### E2 — Entry & Onboarding
- **Source specs:** Onboarding, 60-Second Orientation, Orientation State Model · **Construct type:** Workspace-context/pre-understanding · **User value:** fastest path to first understanding.
- **Stories:** S2.1 account create/sign-in; S2.2 create project (name required; type/workflow optional; empty allowed); S2.3 ingestion (upload/paste/combine; no AI-generated starts); S2.4 initiate analysis → 60-second orientation; S2.5 orientation states (analyzing/fast-pass/stale/reanalysis); S2.6 returning-user landing.
- **Out-of-scope:** templates/AI-generated content; permissions; assessment generation.
- **Acceptance:** min-to-value = name + one artifact; onboarding skippable; failures honest (no fabricated assessment) (OB-C*). **Negative:** optional metadata gates value; system generates starting content; fabricated assessment on failure.
- **QA:** create empty project; add one artifact → orientation < the 60s target (value); ingestion failure path.
- **Dependencies:** E1.

### E3 — Project Discovery
- **Source specs:** Project Dashboard & List · **Construct type:** Workspace-context · **User value:** find/resume the right project fast.
- **Stories:** S3.1 Workspace Home (recent/pinned/dashboard/list); S3.2 search/filter/sort over factual attributes; S3.3 status + stale marker per project; S3.4 understanding indicator (reliability-qualified, **no health/score**); S3.5 archive (reversible, non-destructive).
- **Out-of-scope:** project-health/metrics cockpit; computed ranking; deletion semantics.
- **Acceptance:** no computed score/"health"; stale marked, not triggered from list; archive deletes nothing (PL-C*). **Negative:** health/readiness indicator; filter/sort by computed dimension; archive destroys data.
- **QA:** stale project shows "previous analysis"; search returns none state; archive→unarchive.
- **Dependencies:** E1, E2.

### E4 — Project Overview
- **Source specs:** Project Overview · **Construct type:** Workspace (understanding home) · **User value:** see how strong/trustworthy understanding is.
- **Stories:** S4.1 understanding spine (CAF/Reliability/Confidence read-out, reliability-qualified, never bare); S4.2 context rail (findings/recommendations summary → routes); S4.3 stale presentation; S4.4 entry to MRI/Artifact/Panels/Companion/Chat.
- **Out-of-scope:** numeric confidence score; project-health; structured finding/recommendation actions (those are Panels).
- **Acceptance:** confidence = trust in understanding, **never** health/readiness/probability/score. **Negative:** any score/%/health rendered; assessment changed from Overview.
- **QA:** confidence shown reliability-qualified; no numeric score; stale honest.
- **Dependencies:** E1, E2.

### E5 — MRI Diagnostic Discovery
- **Source specs:** MRI Workspace, MRI Experience, MRI Visualization Model · **Construct type:** Workspace · **User value:** "where are the weaknesses?"
- **Stories:** S5.1 weakness heatmap (qualitative, **no scores**); S5.2 diagnostic lenses (CAF dim/type/severity/lifecycle/concentration/cross-artifact); S5.3 Missing/Risky/Incomplete grouping; S5.4 route to Artifact/Finding Panel; S5.5 stale/reanalysis presentation.
- **Out-of-scope:** issue tracker / flat finding list; artifact editing; assessment engine; numeric ranking.
- **Acceptance:** lenses are non-destructive presentation; qualitative only; routes to Panels/Artifact (MRIW-C*). **Negative:** numeric score/rank; MRI mutates assessment; becomes a list/tracker.
- **QA:** switch lenses (same data reorganized); heatmap intensity qualitative; select → Finding Panel in context.
- **Dependencies:** E1, E4.

### E6 — Artifact Workspace & Editing
- **Source specs:** Artifact Workspace, Artifact Authoring & Editing Workflow · **Construct type:** Workspace · **User value:** see/edit what the content says; weaknesses in situ.
- **Stories:** S6.1 content-primary surface; S6.2 CAF overlays embedded (1 overlay → 1+ findings, no new object); S6.3 finding discovery in content; S6.4 edit→save→pending→reanalysis state machine; S6.5 append-only version/analysis history; S6.6 collaborative edit visibility + conflict surfacing (no silent merge).
- **Out-of-scope:** finding list replacing content; recommendation execution; governance; restore/rollback.
- **Acceptance:** editing changes content only; **only reanalysis changes assessment**; overlays create no object; append-only (AW-C*, AE-C*). **Negative:** editing/saving mutates assessment; overlay creates object; stale shown as current; history mutated.
- **QA:** edit→save→stale marked→reanalyze→updated; reanalysis-failure retains last-known-good; conflict surfaced not merged.
- **Dependencies:** E1, E4, E5.

### E7 — Finding & Recommendation Panels
- **Source specs:** Finding Panel, Recommendation Panel · **Construct type:** Panel (contextual) · **User value:** why a weakness exists; what to consider.
- **Stories:** S7.1 Finding Panel opens in context (overlay/MRI/artifact/related); S7.2 finding content (descriptive: explanation/evidence/CAF impact); S7.3 Recommendation Panel **opens only from Finding**; S7.4 OSLO Recommended / Possible Resolution Paths / Selected Path (presentation-only; alternatives persist); S7.5 actions (accept/reject/defer; no manual resolve); S7.6 reanalysis outcomes (weaken/unchanged/superseded/closed).
- **Out-of-scope:** standalone destinations; manual finding resolution; execution/governance; Resolution-Path/Clarification/Resolution-Candidate object.
- **Acceptance:** **Recommendation only in Finding context**; findings descriptive; recommendations advisory; alternatives persist post-acceptance; assessment changes only via reanalysis (FP-C*, RP-C*). **Negative:** Recommendation opens standalone; manual resolve; alternatives disappear; Selected Path replaces OSLO Recommended; a resolution/candidate object appears.
- **QA:** open Recommendation only via Finding; accept a non-primary → both labels coexist, alternatives remain; no panel interaction changes assessment.
- **Dependencies:** E5, E6.

### E8 — Understanding Companion
- **Source specs:** Understanding Companion (+ Companion Reconciliation 001) · **Construct type:** Companion Surface (**not a destination**) · **User value:** always-visible understanding state.
- **Stories:** S8.1 persistent across Overview/MRI/Artifact; S8.2 read-out (Confidence/CAF/Top Findings/Top Recommendations/stale); S8.3 Top Findings → Finding Panel; S8.4 **Top Recommendations → associated Finding → Recommendation Panel**; S8.5 Ask OSLO → Chat; S8.6 collapsible (no effect on understanding).
- **Out-of-scope:** destination/dashboard; structured actions; numeric score/health; embedding Chat.
- **Acceptance:** presents existing understanding only; routes Top-Rec via Finding; no scores; not a destination (UC-C*). **Negative:** Recommendation opened directly; structured actions hosted; health/score shown; becomes destination.
- **QA:** Top-Rec routes through Finding; collapse changes nothing; stale marked.
- **Dependencies:** E4, E5, E6, E7, E9.

### E9 — OSLO Chat
- **Source specs:** OSLO Chat & Clarification · **Construct type:** Interaction Layer (**not a destination**) · **User value:** converse to explore/clarify understanding.
- **Stories:** S9.1 floating layer across surfaces; S9.2 explain findings/recommendations/CAF/confidence (existing, descriptive); S9.3 clarification (OSLO- & user-initiated) → **information feeding reanalysis**; S9.4 navigate/surface existing understanding (qualitative); S9.5 handoffs to Panels/MRI/Artifact (Recommendation via Finding); S9.6 stale-aware.
- **Out-of-scope:** destination/workspace; replacing Panels; generating findings/recommendations; governance/execution; changing assessment.
- **Acceptance:** clarifications change no assessment (feed reanalysis); no scores; complements not replaces Panels (CHAT-C*). **Negative:** clarification mutates assessment/resolves finding; Chat replaces a Panel; becomes destination; computes a score.
- **QA:** answer a clarification → analysis pending, not changed; ask "show findings affecting confidence" → qualitative routing; stale marked.
- **Dependencies:** E4–E7.

### E10 — Collaboration & Sharing (+ Invite/Share)
- **Source specs:** Collaboration & Sharing, Invite & Share Modal · **Construct type:** object-orbiting collaboration layer + contextual modal · **User value:** improve understanding together; manage access.
- **Stories:** S10.1 comments orbit Artifact/Finding/Recommendation/Project (no new object); S10.2 comment changes no assessment/finding/recommendation; S10.3 invite modal (invite by identity; participant types Owner/Collaborator/Viewer presentation-only); S10.4 shared-users list + remove (confirmation-gated, reversible); S10.5 view-only private invite link (routes into OSLO; public links deferred); S10.6 tier seat visibility.
- **Out-of-scope:** **permission enforcement**; public links/enforcement; approval/governance; billing; comment delivery infra.
- **Acceptance:** **invite/share enforces no permissions**; comments never change assessment; participant types presentation-only (CS-C*, IS-C*). **Negative:** permission enforcement/matrix; comment alters finding/recommendation/assessment; public link/enforcement; billing flow.
- **QA:** invite + remove (reversible); comment on superseded finding retained; at-seat-limit honest (no billing).
- **Dependencies:** E1, E4, E6, E7, E11.

### E11 — Awareness
- **Source specs:** Notification & Awareness · **Construct type:** Companion-Surface-class awareness layer · **User value:** see what changed and where to return.
- **Stories:** S11.1 awareness inbox (global entry + indicators); S11.2 categories (mentions/replies/comments/shared/invitation/reanalysis complete-failed/stale/conflict); S11.3 item structure + route to source (Recommendation via Finding); S11.4 read/unread (presentation only); S11.5 stale-aware.
- **Out-of-scope:** **tasks/obligations/workflow**; notification/delivery infrastructure; assessment change; creating comments.
- **Acceptance:** **awareness creates no tasks/obligations**; read/unread is presentation only; changes no assessment; points to comments (NA-C*). **Negative:** task/assignment/workflow; read/unread implies status; awareness changes assessment or creates a comment; delivery infra defined.
- **QA:** mark-all-read changes nothing; reanalysis-complete routes to context; stale item labeled previous analysis.
- **Dependencies:** E10, E6, E7.

### E12 — History & Timeline
- **Source specs:** History & Timeline · **Construct type:** Companion-Surface-class secondary surface · **User value:** trace how understanding changed.
- **Stories:** S12.1 project timeline (aggregates retained in-context histories); S12.2 categories (artifact versions/analysis runs/stale/finding+recommendation lifecycle & supersession/selected-rec/comment & sharing & awareness references); S12.3 item structure + prior/current marker; S12.4 route to retained context (supersession → both sides; Recommendation via Finding); S12.5 labels (current/prior/superseded/closed/stale/failed/unavailable).
- **Out-of-scope:** **mutation/deletion/rollback**; audit/compliance/governance; assessment change; event/log infra.
- **Acceptance:** **append-only**; prior never shown as current; traceability for understanding only (HT-C*). **Negative:** delete/rollback/mutate; prior presented as current; audit/approval framing; history triggers reanalysis.
- **QA:** no mutation affordance; superseded opens prior + superseding; reanalysis-failed → last-known-good.
- **Dependencies:** E6, E7, E10, E11.

### E13 — Export & Share-Out
- **Source specs:** Export & Share-Out · **Construct type:** lightweight Companion-Surface-class action · **User value:** share understanding outside OSLO.
- **Stories:** S13.1 export action from relevant surfaces (thin config); S13.2 exportables (summaries/artifact/findings/recommendations/selected packages/raw artifacts); S13.3 formats (PDF/copyable/view-only link); S13.4 package structure (currency marker + **disclaimer**: understanding, not health/approval); S13.5 stale export labeled + warned; S13.6 tier format visibility.
- **Out-of-scope:** **generating new content/assessment**; document-generation logic; delivery infra; public link enforcement; billing.
- **Acceptance:** **packages existing understanding only**; stale labeled, never current; export changes nothing/triggers no reanalysis; confidence never health/score; disclaimer present (EX-C*). **Negative:** generates finding/recommendation/assessment; stale as current; confidence as health/score; disclaimer omitted; billing/doc-gen defined.
- **QA:** export stale → warning + "previous analysis"; package carries disclaimer; export changes no assessment.
- **Dependencies:** E4–E7, E12.

### E14 — Help & Support
- **Source specs:** Help & Support · **Construct type:** Companion-Surface-class help layer · **User value:** get help using OSLO.
- **Stories:** S14.1 help layer (global + contextual); S14.2 help types (product/concept/contextual/troubleshooting/contact); S14.3 concept help mirrors models (Confidence = trust, never health); S14.4 route to Chat (project Qs) / Onboarding (getting started); S14.5 contact-support entry.
- **Out-of-scope:** **ticketing workflow**; documentation authoring/CMS; guided tours; governance/automation/agents.
- **Acceptance:** help is about OSLO (no project data generated); concept help never redefines models; not Chat (HS-C*). **Negative:** generates project understanding; redefines a concept / Confidence-as-health; ticketing workflow; becomes Chat/destination.
- **QA:** concept help matches model definitions; contextual help changes nothing; contact entry has no ticket workflow.
- **Dependencies:** E1, E9, E2.

### E15 — Settings & Tier Visibility
- **Source specs:** Account & Workspace Settings · **Construct type:** periphery · **User value:** manage account/workspace; see plan.
- **Stories:** S15.1 account/profile/workspace edit (preferences only); S15.2 project defaults (non-gating); S15.3 collaboration/notification preferences; S15.4 subscription/billing/usage/limits **visibility-first**; S15.5 integrations view-only; S15.6 membership presentation-only.
- **Out-of-scope:** **billing/subscription/permissions implementation**; integration configuration; notification infra.
- **Acceptance:** never touches project understanding; visibility-first plan info (no billing impl); presentation-only membership (SET-C*). **Negative:** settings changes assessment; billing/entitlement/permission enforcement defined; integrations configurable.
- **QA:** plan shown as info (no score); editing a preference changes no assessment; destructive actions confirmation-gated.
- **Dependencies:** E1.

### E16 — Cross-Surface Invariants (§G stories)
- **Source specs:** Handoff §H + every surface's conformance · **Construct type:** runtime guarantees layer · **User value:** the product behaves consistently and safely everywhere.
- **Stories (invariant guarantees):** INV-S1 only-reanalysis-changes-assessment; INV-S2 Recommendation-only-in-Finding-context; INV-S3 Confidence-never-health/score; INV-S4 stale-never-current; INV-S5 presentation-only resolution constructs; INV-S6 history append-only; INV-S7 Chat/Companion not destinations; INV-S8 Export packages-only; INV-S9 Awareness no-tasks; INV-S10 Invite no-permission-enforcement; INV-S11 context preserved; INV-S12 no forbidden capabilities; INV-S13 classify-before-specify (governance gate).
- **Acceptance/Negative/QA:** the **§K matrix** below — each invariant a system-level pass/fail with negative tests.
- **Dependencies:** spans all epics.

### E17 — QA & Acceptance (§H stories)
- **Stories:** QA-S1 per-surface acceptance suites (conformance positive + fail-condition negative); QA-S2 invariant suite (E16); QA-S3 state/flow (orientation/stale/reanalysis, empty/failure); QA-S4 navigation/journey; QA-S5 guardrail/negative suite.
- **Dependencies:** runs throughout; gates Definition of Done.

## E. Story Acceptance Criteria

Every story's acceptance = the **source spec's relevant `*-C#` conformance items** (positive) interpreted as "behavior present and correct," plus structure/IA present, all empty & failure states honest, construct behaves as its classified type, and routing/context per Journey/Navigation. Threshold-dependent criteria are **TBD** until owner values (RR-1/RR-2).

## F. Negative Acceptance Criteria / Fail Conditions

Every story's negative acceptance = the **source spec's explicit fail conditions** as must-not-occur tests. Universal negatives (apply to all): assessment changed outside reanalysis; Confidence as score/health; stale as current; mutable history; Recommendation outside Finding context; object-to-Workspace inflation; a forbidden capability (governance/execution/automation/agents/approvals/task/permissions-enforcement/billing/notification-infra); a new construct un-classified.

## G. Cross-Surface Invariant Stories

= E16 (INV-S1…S13). These are **shared stories** referenced by every surface epic; a surface epic is not Done until its slice of the invariants passes.

## H. QA Story Set

= E17 (QA-S1…S5). The §K matrix is the invariant suite; per-spec conformance is the per-surface suite; empty/failure/state/journey suites complete coverage.

## I. Dependency Order

E1 → E2 → E3 → E4 → (E5, E6) → E7 → (E8, E9) → (E10, E11) → (E12, E13, E14) → E15. **E16 invariants + E17 QA run throughout.** (Mirrors Execution Plan §I; Companion E8 depends on Panels E7 and Chat E9 for routing/Ask-OSLO.)

## J. Deferred / Out-of-Scope Items

Per Scope Freeze §E / Execution Plan §E: APIs/events/schemas; delivery/notification/document-generation infra; permissions enforcement; billing/entitlement impl; public links; ticketing; restore/rollback & extra export formats; documentation authoring; guided tours; tier upgrade/transactional flow; mobile nav; shared empty/failure pattern library; Release 2 capabilities (governance/execution/automation/agents/plugins/integrations — separate classification). **None enters Release 1 silently** (§M intake + owner decision).

## K. Owner Clarification Items

RR-1 tier numbers · RR-2 calibration values · RR-3 private invite link in/out · RR-4 construct-type tags · RR-5 normalize older UI-layer docs. **Non-blocking**; gate only threshold-dependent tests. Prior owner items (classification doctrine, onboarding defaults) **closed**.

## L. Implementation Drift Warnings

- Do **not** implement superseded specs (`FINDING_WORKSPACE_…`, `RECOMMENDATION_WORKSPACE_…`) or older UI-layer docs.
- Do **not** open a Recommendation Panel outside Finding context.
- Do **not** render Confidence as a score/health, present stale as current, or make history mutable.
- Do **not** let Chat/Companion become destinations, Export generate content, Awareness create tasks, or Invite enforce permissions.
- Do **not** mint a new construct without classification, or resolve a spec conflict in code — **escalate** (Scope Freeze §K).

## M. Definition of Ready (for stories→tickets)

A story is **Ready** when it: maps to a canonical source spec with cited sections; uses that spec's conformance (positive) + fail conditions (negative) as acceptance; states construct type + routing/context; lists must-hold invariants (E16); has numeric values supplied or marked TBD; includes empty/failure states; and introduces no deferred/forbidden capability or unclassified construct.

## N. Definition of Done (Release 1 UX)

Release 1 UX is **Done** when: every epic E1–E15 passes its surface conformance (positive + negative); **E16 invariants pass** system-level (§K); no superseded spec implemented and no deferred/forbidden capability present; navigation/journey matches specs; **Confidence never score/health, stale never current, history append-only, assessment only via reanalysis, Chat/Companion not destinations, Export packages-only, Awareness no-tasks, Invite no-enforcement, Recommendation only in Finding context** — all verified; no spec conflict resolved in code; threshold tests have owner values or tracked TBD; and the **Release 1 acceptance boundary** (Execution Plan §R) and **Audit 002** are satisfied.

---

*This backlog converts the frozen, audit-verified Release 1 UX architecture into seventeen epics — fifteen surface epics (each with source specs, construct type, user value, stories, out-of-scope boundaries, acceptance criteria, QA scenarios, and dependencies), a cross-surface invariant epic, and a QA & acceptance epic — with story acceptance defined as each source spec's conformance (positive) and fail conditions (negative), shared cross-surface invariant stories, a dependency order, deferred/out-of-scope and owner-clarification registers, drift warnings, and Definitions of Ready and Done. It binds every guardrail: source specs govern; only canonical specs in scope; superseded specs not implemented; Recommendation Panel only in Finding context; Confidence is trust in understanding never project health/readiness/probability; stale means previous analysis never current; only reanalysis changes assessment; history append-only; Chat and Companion not destinations; Awareness creates no tasks; Export packages existing understanding only; Invite/share enforces no permissions; new constructs classified before specification; spec conflicts escalated not coded. It redefines no surface and introduces no implementation, APIs, events, schemas, styling, governance, execution, automation, agents, permissions enforcement, billing, notification infrastructure, or assessment behavior.*

**Release 1 UX Epic & Story Backlog v1 complete.**
