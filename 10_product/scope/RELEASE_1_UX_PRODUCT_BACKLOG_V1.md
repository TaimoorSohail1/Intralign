# Release 1 UX Product Backlog v1

**Document Type:** Product Backlog (planning only — UX scope) · **Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Built from / subordinate to (authoritative — must not redefine):** `RELEASE_1_UX_EXECUTION_PLAN_V1.md` · `RELEASE_1_UX_EXECUTION_PLANNING_PACKAGE_V1.md` · `RELEASE_1_UX_HANDOFF_PACKAGE_SPECIFICATION_V1.md` · `RELEASE_1_UX_SCOPE_FREEZE_AND_BACKLOG_CONTROL_SPECIFICATION_V1.md` · `UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION_001.md` · the canonical active UX spec set (Handoff §D).

> **Non-negotiable constraints.** Backlog only. **Redefines no UX surface**; introduces **no** APIs, events, schemas, implementation details, styling, governance, execution, automation, agents, permissions enforcement, billing implementation, notification infrastructure, or assessment behavior. Stories are **implementation-neutral** (no database/API/framework/event/schema/styling detail). **Only reanalysis changes assessment.**

---

## A. Backlog Overview

This backlog is derived from the **frozen** Release 1 UX scope (Scope Freeze §D; Audit 002 = READY) and the Execution Plan. **Source specs govern**: each story's authoritative acceptance is its source spec's **Conformance Requirements** (positive) and **explicit fail conditions** (negative); the criteria here are execution-ready anchors, not replacements. Nothing enters Release 1 outside the canonical set except via owner-decision intake (Scope Freeze §G). Superseded specs are **not** implemented.

## B. Epic Inventory

| ID | Epic | Source specs | Construct type | Purpose | Primary user value | Dependencies | Out-of-scope boundaries |
|---|---|---|---|---|---|---|---|
| **EP-1** | App Shell & Navigation | Global Navigation, Understanding Journey | Workspace shell + connective layer | Frame all surfaces; move/return safely | Never lost; coherent movement | — | Panels/Companion/Chat as destinations; deep-link mechanics; mobile nav |
| **EP-2** | Entry & Onboarding | Onboarding, 60-Second Orientation, Orientation State Model | Workspace-context / pre-understanding | Reach first understanding fast | Value in minutes | EP-1 | Templates/AI-generated starts; permissions; assessment generation |
| **EP-3** | Project Discovery | Project Dashboard & List | Workspace-context | Find/resume projects | Fast re-entry | EP-1, EP-2 | Project-health/metrics cockpit; computed ranking; deletion semantics |
| **EP-4** | Project Overview | Project Overview | Workspace (understanding home) | See strength/trust of understanding | Orient at a glance | EP-1, EP-2 | Numeric confidence score; project-health; structured object actions |
| **EP-5** | MRI Diagnostic Discovery | MRI Workspace/Experience/Visualization Model | Workspace | "Where are the weaknesses?" | Find what needs attention | EP-1, EP-4 | Issue tracker/flat list; artifact editor; assessment engine; numeric rank |
| **EP-6** | Artifact Workspace & Editing | Artifact Workspace, Authoring & Editing Workflow | Workspace | See/edit content; weaknesses in situ | Work the source of truth | EP-1, EP-4, EP-5 | Finding list replacing content; rec execution; governance; restore/rollback |
| **EP-7** | Finding & Recommendation Panels | Finding Panel, Recommendation Panel | Panel (contextual) | Why a weakness exists; what to consider | Understand & evaluate in context | EP-5, EP-6 | Standalone destinations; manual resolve; resolution/candidate objects |
| **EP-8** | Understanding Companion | Understanding Companion (+ Reconciliation 001) | Companion Surface (not a destination) | Always-visible understanding | Stay oriented anywhere | EP-4–EP-7, EP-9 | Destination/dashboard; structured actions; score/health; embedding Chat |
| **EP-9** | OSLO Chat | OSLO Chat & Clarification | Interaction Layer (not a destination) | Converse to explore/clarify | Ask in natural language | EP-4–EP-7 | Destination; replacing Panels; generation; governance; assessment change |
| **EP-10** | Collaboration & Sharing | Collaboration & Sharing, Invite & Share Modal | Object-orbiting layer + contextual modal | Improve understanding together; manage access | Shared understanding | EP-1, EP-4, EP-6, EP-7, EP-11 | Permission enforcement; public links; approvals; billing; delivery infra |
| **EP-11** | Notification & Awareness | Notification & Awareness | Companion-Surface-class awareness layer | See what changed; where to return | Stay aware | EP-10, EP-6, EP-7 | Tasks/obligations/workflow; delivery infra; assessment change |
| **EP-12** | History & Timeline | History & Timeline | Companion-Surface-class secondary surface | Trace how understanding changed | Traceability | EP-6, EP-7, EP-10, EP-11 | Mutation/rollback; audit/compliance/governance; event/log infra |
| **EP-13** | Export & Share-Out | Export & Share-Out | Lightweight Companion-Surface-class action | Share understanding outside OSLO | Take understanding with you | EP-4–EP-7, EP-12 | Generated content/assessment; doc-gen logic; delivery infra; billing |
| **EP-14** | Help & Support | Help & Support | Companion-Surface-class help layer | Get help using OSLO | Reduce friction | EP-1, EP-9, EP-2 | Ticketing workflow; docs authoring/CMS; guided tours; agents |
| **EP-15** | Settings & Tier Visibility | Account & Workspace Settings | Periphery | Manage account/workspace; see plan | Control & transparency | EP-1 | Billing/subscription/permissions implementation; integration config |
| **EP-16** | Cross-Surface Invariant Layer | Handoff §H + all conformance | Runtime guarantees layer | Consistent, safe behavior everywhere | Trust the product | spans all | (n/a — guarantees, not a surface) |

## C. User Stories by Epic

*(Acceptance/negative anchors below; full acceptance = each source spec's conformance + fail conditions. All stories implementation-neutral.)*

### EP-1 App Shell & Navigation
- **US-1.1 — Global navigation frame**
  As a **user**, I want **a persistent global navigation (Workspace Home, Project List, Create Project, Settings, Account)**, so that **I can reach the few stable anchors from anywhere.**
  *Source:* Global Navigation. *Construct:* Workspace shell. *Acceptance:* only Workspaces are destinations; project-internal/object surfaces excluded from global nav. *Negative:* workflow/task/approval/execution nav appears. *QA:* every primary surface reachable; no destination for Panels/Companion/Chat. *Deps:* —. *Deferred:* deep-link mechanics; mobile nav.
- **US-1.2 — Nested context model**
  As a **user**, I want **Workspace/Project/Object contexts kept distinct**, so that **I always know my altitude and don't lose the enclosing context.** *Acceptance:* entering one context never loses the outer; panels stay in Object context. *Negative:* contexts blur; entering a project loses global frame. *QA:* open panel over artifact — project surface preserved.
- **US-1.3 — Understanding journey & direct jumps**
  As a **user**, I want **to follow Overview→MRI→Artifact→Finding→Recommendation and also jump directly among Overview/MRI/Artifact**, so that **I can investigate flexibly once understanding exists.** *Acceptance:* lifecycle reinforced-not-enforced; only precondition is initial analysis; **Recommendation only in Finding context.** *Negative:* steps gated beyond initial-analysis; Recommendation opened without Finding. *QA:* direct jumps work; Recommendation blocked without Finding.
- **US-1.4 — Return & recovery**
  As a **user**, I want **a path back to any primary surface and Workspace Home**, so that **I'm never stranded.** *Acceptance:* inverse chain + jump-to-primary; stale surfaced during nav. *Negative:* dead end; silent redirect; stale as current. *QA:* recover from any depth.

### EP-2 Entry & Onboarding
- **US-2.1 — Create project (minimal)**
  As a **new user**, I want **to create a project with just a name (type/workflow optional, empty allowed)**, so that **I can start without friction.** *Source:* Onboarding. *Acceptance:* name required; type/workflow optional/non-gating; empty project allowed. *Negative:* optional metadata gates value. *QA:* create empty project; add metadata later. *Deferred:* templates/AI starts.
- **US-2.2 — Ingest artifacts**
  As a **user**, I want **to add artifacts by upload, paste, or combining sources**, so that **OSLO has content to analyze.** *Acceptance:* upload/paste/combine; **no AI-generated starting content.** *Negative:* system generates starting content. *QA:* combine two sources; ingestion-failure path retains added artifacts.
- **US-2.3 — First understanding in ~60 seconds**
  As a **user**, I want **analysis to produce a 60-second orientation then Project Overview**, so that **I reach first value quickly.** *Source:* 60-Second Orientation, Orientation State Model. *Acceptance:* min-to-value = name + one artifact; analyzing/stale/reanalysis states honest. *Negative:* fabricated assessment on failure. *QA:* orientation reached; failure shows no fabricated assessment.
- **US-2.4 — Returning user landing**
  As a **returning user**, I want **to land on my Workspace Home (not onboarding)**, so that **I resume quickly.** *Acceptance:* lands on projects home; resume to Overview/last state. *QA:* re-entry skips onboarding.

### EP-3 Project Discovery
- **US-3.1 — Workspace Home & discovery**
  As a **user**, I want **recent, pinned, a dashboard, and a searchable/filterable/sortable list**, so that **I find the right project fast.** *Source:* Dashboard & List. *Acceptance:* search/filter/sort over factual attributes; archived view. *Negative:* filter/sort by computed dimension. *QA:* search no-results state; archive→unarchive.
- **US-3.2 — Project status & understanding indicator**
  As a **user**, I want **each project's analysis status and an existing reliability-qualified understanding indicator**, so that **I can triage.** *Acceptance:* stale clearly marked; **no project-health/readiness/score.** *Negative:* health indicator; list triggers reanalysis. *QA:* stale shows "previous analysis"; no numeric score.
- **US-3.3 — Archive (non-destructive)**
  As a **user**, I want **to archive/unarchive projects**, so that **I declutter without losing data.** *Acceptance:* reversible; deletes nothing. *Negative:* archive destroys content/history.

### EP-4 Project Overview
- **US-4.1 — Understanding read-out**
  As a **user**, I want **the project's CAF/Reliability/Outcome-Confidence presented reliability-qualified**, so that **I see how strong and trustworthy understanding is.** *Source:* Project Overview. *Acceptance:* confidence = trust in understanding, never bare; **no score/health/readiness/probability.** *Negative:* numeric score/% or health rendered; assessment changed here. *QA:* reliability-qualified; no score.
- **US-4.2 — Route into investigation**
  As a **user**, I want **to enter MRI/Artifact and open Panels/Companion/Chat from Overview**, so that **I can deepen.** *Acceptance:* routes preserve context. *QA:* each route opens correct surface in context.
- **US-4.3 — Stale on Overview**
  As a **user**, I want **stale understanding clearly marked**, so that **I don't trust outdated reads.** *Acceptance:* "previous analysis"; never current; no implicit reanalysis.

### EP-5 MRI Diagnostic Discovery
- **US-5.1 — Weakness heatmap**
  As a **user**, I want **a qualitative weakness map**, so that **I see where to look.** *Source:* MRI Workspace. *Acceptance:* qualitative intensity; **no scores/ranks.** *Negative:* numeric score/rank. *QA:* intensity qualitative.
- **US-5.2 — Diagnostic lenses**
  As a **user**, I want **lenses (CAF dimension, type/Missing-Risky-Incomplete, severity, lifecycle, concentration, cross-artifact)**, so that **I organize weaknesses.** *Acceptance:* non-destructive reorganization of same data; routes to Panels/Artifact. *Negative:* MRI mutates assessment; becomes flat list/tracker. *QA:* switch lenses — same data reorganized.
- **US-5.3 — Drill to context**
  As a **user**, I want **to open a finding's Finding Panel or its Artifact location**, so that **I can investigate.** *Acceptance:* opens in context; Recommendation only via Finding. *QA:* select → Finding Panel.

### EP-6 Artifact Workspace & Editing
- **US-6.1 — Content-primary surface with CAF overlays**
  As a **user**, I want **the artifact content central with CAF overlays in situ**, so that **I see weaknesses where they live.** *Source:* Artifact Workspace. *Acceptance:* content primary; 1 overlay → 1+ findings; **no new object.** *Negative:* overlay creates object; content replaced by list. *QA:* overlay surfaces finding(s) in context.
- **US-6.2 — Edit → save → reanalyze**
  As a **user**, I want **to edit content, save, and trigger reanalysis**, so that **I improve understanding.** *Source:* Authoring & Editing Workflow. *Acceptance:* editing changes content only; saving changes no assessment; **only reanalysis changes assessment**; stale marked. *Negative:* edit/save mutates assessment; stale as current. *QA:* edit→save→pending→reanalyze→updated; reanalysis-fail → last-known-good.
- **US-6.3 — Append-only history & conflict surfacing**
  As a **user**, I want **retained versions/analyses and explicit conflict surfacing**, so that **nothing is lost and concurrent edits are visible.** *Acceptance:* append-only; conflicts surfaced, no silent merge. *Negative:* history mutated; silent merge.

### EP-7 Finding & Recommendation Panels
- **US-7.1 — Finding Panel in context**
  As a **user**, I want **a Finding Panel explaining why a weakness exists (evidence, CAF impact)**, so that **I understand it without leaving my surface.** *Source:* Finding Panel. *Acceptance:* opens in context; descriptive; evidence traceable; preserves underlying surface. *Negative:* standalone destination; finding framed as command; finding→direct-confidence. *QA:* open from overlay/MRI; close returns to context.
- **US-7.2 — Recommendation Panel from Finding only**
  As a **user**, I want **to open recommendations only from a Finding**, so that **advice stays attributed to its weakness.** *Source:* Recommendation Panel. *Acceptance:* **opens only in Finding context**; advisory; OSLO Recommended / Possible Resolution Paths / Selected Path presentation-only. *Negative:* opens standalone; resolution/candidate object; Selected Path replaces OSLO Recommended. *QA:* cannot open without Finding.
- **US-7.3 — Evaluate without changing assessment**
  As a **user**, I want **to accept/reject/defer recommendations**, so that **I decide — while reanalysis does the rest.** *Acceptance:* alternatives persist post-acceptance; **no manual finding resolution**; assessment changes only via reanalysis. *Negative:* manual resolve; alternatives disappear; acceptance mutates assessment. *QA:* accept non-primary → both labels coexist, alternatives remain.

### EP-8 Understanding Companion
- **US-8.1 — Persistent understanding read-out**
  As a **user**, I want **a persistent companion showing Confidence/CAF/Top Findings/Top Recommendations/stale across Overview/MRI/Artifact**, so that **I always see where understanding stands.** *Source:* Understanding Companion. *Acceptance:* presents existing understanding (no score/health); **not a destination**; collapsible without effect. *Negative:* score/health; structured actions; becomes destination. *QA:* collapse changes nothing; stale marked.
- **US-8.2 — Route Top Recommendations via Finding**
  As a **user**, I want **Top Recommendations to open their associated Finding then the Recommendation Panel**, so that **attribution is preserved.** *Source:* Companion Reconciliation 001 (Option B). *Acceptance:* routes via Finding; never standalone. *Negative:* opens Recommendation directly. *QA:* Top-Rec → Finding → Rec Panel.
- **US-8.3 — Ask OSLO entry**
  As a **user**, I want **an "Ask OSLO" entry that launches Chat**, so that **I can ask in context.** *Acceptance:* launches separate Chat layer; does not embed Chat. *QA:* entry opens Chat scoped to context.

### EP-9 OSLO Chat
- **US-9.1 — Floating conversational layer**
  As a **user**, I want **a floating Chat available on every surface**, so that **I can ask without leaving my work.** *Source:* OSLO Chat. *Acceptance:* floating; **not a destination**; preserves underlying surface. *Negative:* becomes destination/workspace. *QA:* open/close preserves surface.
- **US-9.2 — Explain & navigate understanding**
  As a **user**, I want **Chat to explain findings/recommendations/CAF/confidence and surface existing items**, so that **I understand faster.** *Acceptance:* explains existing (descriptive/advisory); qualitative navigation; **no scores**; complements Panels. *Negative:* generates findings/recommendations; computes a score; replaces a Panel. *QA:* "show findings affecting confidence" → qualitative routing.
- **US-9.3 — Clarification feeds reanalysis**
  As a **user**, I want **to answer OSLO's clarifying questions conversationally**, so that **I improve understanding** — knowing it updates only on reanalysis. *Acceptance:* clarification = information feeding reanalysis; **changes no assessment directly**; stale honest. *Negative:* clarification mutates assessment/resolves finding. *QA:* answer clarification → analysis pending, not changed.

### EP-10 Collaboration & Sharing
- **US-10.1 — Comments orbit objects**
  As a **collaborator**, I want **to comment on artifacts/findings/recommendations/project**, so that **we improve understanding together** — without changing it. *Source:* Collaboration & Sharing. *Acceptance:* comments orbit objects; **change no assessment/finding/recommendation**; no new object. *Negative:* comment alters a finding/recommendation/assessment. *QA:* comment on superseded finding retained.
- **US-10.2 — Invite & manage access**
  As an **owner**, I want **to invite people, set participant type (Owner/Collaborator/Viewer), see participants, and remove access**, so that **the right people collaborate.** *Source:* Invite & Share Modal. *Acceptance:* participant types presentation-only; **no permission enforcement**; remove confirmation-gated/reversible. *Negative:* permission matrix/enforcement; approval workflow. *QA:* invite + remove reversible; Viewer presented view-only (not enforced).
- **US-10.3 — Private invite link (optional)**
  As an **owner**, I want **a view-only private invite link that routes into OSLO**, so that **I can invite a specific person.** *Acceptance:* view-only; routes into OSLO; **public links/enforcement deferred**; distinct from Export link. *Negative:* public link / link enforcement. *QA:* link routes into OSLO context. *Deferred:* public links (RR-3 in/out decision).

### EP-11 Notification & Awareness
- **US-11.1 — Awareness inbox**
  As a **user**, I want **a lightweight awareness inbox of mentions/replies/comments/shared/invitation/reanalysis/stale/conflict**, so that **I see what changed.** *Source:* Notification & Awareness. *Acceptance:* groupings over existing activity; routes to source (Recommendation via Finding); **not a destination workspace.** *Negative:* generates an object; becomes destination. *QA:* reanalysis-complete routes to context.
- **US-11.2 — Read/unread without obligation**
  As a **user**, I want **read/unread cues**, so that **I track what's new** — without it implying work status. *Acceptance:* read/unread presentation only; **no tasks/obligations/workflow.** *Negative:* task/assignment/workflow; read/unread implies completion/approval. *QA:* mark-all-read changes nothing.
- **US-11.3 — Stale-aware awareness**
  As a **user**, I want **stale items labeled previous analysis**, so that **I don't treat them as current.** *Acceptance:* stale never current; no implicit reanalysis. *QA:* stale item labeled.

### EP-12 History & Timeline
- **US-12.1 — Project timeline**
  As a **user**, I want **a timeline aggregating retained histories (versions/analysis/lifecycle/supersession/selected-rec/comment & sharing & awareness references)**, so that **I trace evolution.** *Source:* History & Timeline. *Acceptance:* **append-only**; references retained context; no new retention mechanism. *Negative:* delete/rollback/mutate; audit/governance framing. *QA:* no mutation affordance.
- **US-12.2 — Prior/current labeling & routing**
  As a **user**, I want **each item labeled (current/prior/superseded/closed/stale/failed) and routed to retained context**, so that **I never confuse prior with current.** *Acceptance:* prior never shown as current; supersession opens prior + superseding; Recommendation via Finding. *Negative:* prior presented as current; history triggers reanalysis. *QA:* superseded → both sides; reanalysis-failed → last-known-good.

### EP-13 Export & Share-Out
- **US-13.1 — Package existing understanding**
  As a **user**, I want **to export a snapshot (summaries/artifact/findings/recommendations/selected packages) as PDF/copyable/view-only link**, so that **I share understanding outside OSLO.** *Source:* Export & Share-Out. *Acceptance:* **packages existing understanding only**; currency marker + **disclaimer** (understanding, not health/approval); confidence never health/score. *Negative:* generates finding/recommendation/assessment; confidence as health/score; disclaimer omitted. *QA:* package carries disclaimer; changes no assessment. *Deferred:* CSV/DOCX/image; doc-gen logic; delivery.
- **US-13.2 — Stale export handling**
  As a **user**, I want **stale exports labeled and warned**, so that **recipients aren't misled.** *Acceptance:* stale labeled "previous analysis"; pre-export warning; **no refresh/reanalysis.** *Negative:* stale as current; export triggers reanalysis. *QA:* export stale → warning + label.

### EP-14 Help & Support
- **US-14.1 — Help layer (product/concept/contextual/troubleshooting)**
  As a **user**, I want **product, concept, contextual, and troubleshooting help**, so that **I can use OSLO confidently.** *Source:* Help & Support. *Acceptance:* about OSLO (no project data generated); **concept help mirrors models** (Confidence = trust, never health); not Chat. *Negative:* generates project understanding; redefines a concept; becomes Chat/destination. *QA:* concept help matches model definitions; contextual help changes nothing.
- **US-14.2 — Contact support (entry only)**
  As a **user**, I want **a way to reach support**, so that **I get help from a human.** *Acceptance:* contact entry point; **ticketing workflow deferred.** *Negative:* ticketing/tracking/SLA workflow. *QA:* contact entry without workflow. *Deferred:* ticketing; docs CMS; guided tours.

### EP-15 Settings & Tier Visibility
- **US-15.1 — Manage account/workspace (preferences only)**
  As a **user**, I want **to edit account/profile/workspace/defaults and preferences**, so that **OSLO fits me** — without touching my project understanding. *Source:* Account & Workspace Settings. *Acceptance:* preferences/account info only; **never touches project understanding**; defaults non-gating. *Negative:* settings changes assessment. *QA:* editing a preference changes no assessment.
- **US-15.2 — Plan & tier visibility**
  As a **user**, I want **to view subscription/billing/usage/limits and integrations**, so that **I understand my plan.** *Acceptance:* visibility-first; **no billing/entitlement implementation**; integrations view-only; membership presentation-only. *Negative:* billing/permission enforcement; integration config. *QA:* plan shown as info (no score). *Deferred:* upgrade/transactional flow.

### EP-16 Cross-Surface Invariant Layer
→ See **§D** (system-level stories) and **§E** (QA matrix). Each surface epic is incomplete until its slice of these invariants passes.

## D. Cross-Surface Invariant Stories

| ID | Invariant story | Test (pass = holds everywhere) | Negative (must not occur) |
|---|---|---|---|
| **INV-1** | Only reanalysis changes assessment | no action mutates CAF/Reliability/Confidence or finding/recommendation state | edit/save/clarify/navigate/companion/chat/awareness/history/export/settings changes assessment |
| **INV-2** | Recommendation Panel only in Finding context | Rec Panel cannot open without a Finding from any surface/layer | opened from Overview/MRI/Artifact/Companion/Chat/Awareness/History/Export |
| **INV-3** | Confidence = trust, never health/score | no score/%/health/readiness/probability rendered | any numeric/health confidence framing |
| **INV-4** | Stale = previous analysis, never current | stale labeled; never current; no implicit reanalysis | stale shown as current; surface triggers reanalysis |
| **INV-5** | History append-only | no delete/mutate/rollback; supersession additive | mutation/rollback affordance; prior overwritten |
| **INV-6** | Chat & Companion not destinations | both remain layers | either becomes a primary destination |
| **INV-7** | Export packages existing understanding only | no generated content/assessment; currency + disclaimer | export generates a finding/recommendation/assessment |
| **INV-8** | Awareness creates no tasks/obligations | no task/assignment/workflow; read/unread presentation-only | task queue; read/unread implies status |
| **INV-9** | Invite/share no permission enforcement | participant types presentation-only | permission matrix/enforcement |
| **INV-10** | Context preserved across transitions | open/close panel/companion/chat/modal/settings never discards context | context discarded |
| **INV-11** | No forbidden capabilities | no governance/execution/automation/agents/approvals/task/permissions-enforcement/billing/notification-infra surfaces | any appears |
| **INV-12** | Classify before specification | no new construct un-typed | a new construct specified without classification |

## E. QA Matrix

| Epic | Key positive tests | Key negative tests | Invariants covered | Deferred values / TBD |
|---|---|---|---|---|
| EP-1 | full chain + back; contexts intact | workflow nav; context loss | INV-2, INV-10 | — |
| EP-2 | name+1 artifact → orientation | metadata gates; fabricated assessment | INV-4 | 60s target (owner-approved); RR-2 |
| EP-3 | search/filter/sort; archive reversible | health indicator; archive deletes | INV-3, INV-4 | RR-1 (limits) |
| EP-4 | reliability-qualified confidence | score/health; assessment change | INV-1, INV-3, INV-4 | RR-2 (scales) |
| EP-5 | lenses non-destructive; qualitative | numeric rank; MRI mutates | INV-1, INV-3 | RR-2 (Top N, mapping) |
| EP-6 | edit→save→reanalyze; append-only | edit mutates assessment; history mutated | INV-1, INV-4, INV-5 | RR-2 (stale thresholds) |
| EP-7 | Recommendation only via Finding; alternatives persist | standalone Rec; resolution object | INV-1, INV-2 | — |
| EP-8 | Top-Rec via Finding; collapse no-op | direct Rec; score/health; destination | INV-1, INV-2, INV-3, INV-6 | RR-2 (Top N) |
| EP-9 | clarification → pending; qualitative nav | clarification mutates; replaces Panel; destination | INV-1, INV-2, INV-4, INV-6 | — |
| EP-10 | invite/remove reversible; comments retained | permission enforcement; comment alters object | INV-1, INV-9 | RR-1 (seats), RR-3 (link) |
| EP-11 | route to source; mark-read no-op | task queue; read/unread status | INV-1, INV-2, INV-4, INV-8 | — |
| EP-12 | append-only; superseded both sides | rollback/mutate; prior as current | INV-1, INV-4, INV-5 | — |
| EP-13 | disclaimer present; stale warned | generates content; confidence-as-health | INV-1, INV-3, INV-4, INV-7 | RR-1 (format gating) |
| EP-14 | concept help matches models; no project gen | redefines concept; ticketing; becomes Chat | INV-3 | — |
| EP-15 | preference change no-op on assessment | billing/permission enforcement | INV-1, INV-11 | RR-1 (tier numbers) |
| EP-16 | §D invariant suite | §D negatives | all | RR-1/RR-2 |

## F. Dependency & Sequencing Plan

**Sequence:** 1) App Shell & Navigation → 2) Entry & Onboarding + Orientation → 3) Project Discovery → 4) Project Overview → 5) MRI + Artifact → 6) Finding & Recommendation Panels → 7) Companion + Chat → 8) Collaboration/Invite + Awareness → 9) History + Export + Help → 10) Settings & Tier Visibility. **EP-16 invariants + QA run throughout.**

**Parallelizable:** within step 5, **MRI and Artifact** proceed in parallel (shared dependency on Overview); within step 7, **Companion and Chat**; within step 8, **Collaboration/Invite and Awareness**; within step 9, **History, Export, and Help** are independent of each other. **Settings (EP-15)** can proceed early in parallel (depends only on EP-1). QA/invariant work parallels all epics.

## G. Definition of Ready (ticket readiness)

A ticket is **Ready** when it: maps to a **canonical source spec** with cited sections; uses that spec's **conformance (positive) + fail conditions (negative)** as acceptance; states **construct type + routing/context**; lists **must-hold invariants** (§D); has **numeric values supplied or marked TBD** (§J); includes **empty/failure** states; is **implementation-neutral**; and introduces **no** deferred/forbidden capability or **unclassified** construct.

## H. Definition of Done (release completion)

Release 1 UX is **Done** when: every epic EP-1…EP-15 passes its surface conformance (positive + negative); **EP-16 invariants pass** system-level (§D/§E); **no superseded spec implemented**, **no deferred/forbidden capability present**; navigation/journey matches specs; **Confidence never score/health, stale never current, history append-only, assessment only via reanalysis, Chat/Companion not destinations, Export packages-only, Awareness no-tasks, Invite no-enforcement, Recommendation only in Finding context** — all verified; **no spec conflict resolved in code** (all via owner-ratified reconciliation); threshold tests have owner values (RR-1/RR-2) or are tracked TBD; and the **Release 1 acceptance boundary** (Execution Plan §R) and **Audit 002** are satisfied.

## I. Deferred Scope Register

Must **not** enter Release 1 unless owner-promoted (Scope Freeze §G intake): APIs/events/schemas · delivery/notification/document-generation infrastructure · permissions enforcement · billing/entitlement implementation · public links · support ticketing · restore/rollback · CSV/DOCX/image export · documentation authoring/CMS · guided tours · tier upgrade/transactional flow · mobile navigation · cross-surface empty/failure pattern library · governance/execution/automation/agents/plugins/integrations.

## J. Owner Clarification Register

- **RR-1** Tier Definitions numbers (seats/limits, format gating).
- **RR-2** Calibration values (CAF/Confidence/Reliability scales; stale suggested-vs-required; "Top N"; MRI edge-case mapping).
- **RR-3** Private invite link in/out for first build (default optional).
- **RR-4** Construct-type tags per surface spec (hygiene).
- **RR-5** Older UI-layer doc normalization to the Panel model (hygiene / drift-source).
*Non-blocking; gate only threshold-dependent tests. Prior owner items (classification doctrine, onboarding defaults) closed.*

## K. Implementation Drift Warnings

For designers/developers — **do not:**
- Implement superseded Workspace specs (`FINDING_WORKSPACE_…`, `RECOMMENDATION_WORKSPACE_…`) or older UI-layer docs.
- Open Recommendations outside Finding context.
- Render Confidence as a score or health.
- Present stale as current.
- Mutate assessment outside reanalysis.
- Make History mutable.
- Make Chat or Companion destinations.
- Make Awareness a task queue.
- Make Invite/Share a permissions engine.
- Invent unclassified constructs (classify first; escalate conflicts — never resolve in code).

---

*This Release 1 UX Product Backlog converts the frozen, audit-verified Release 1 UX scope into sixteen epics with an inventory (source specs, construct type, purpose, user value, dependencies, out-of-scope), implementation-neutral user stories per epic (As-a / I-want / so-that with acceptance, negative acceptance, QA notes, dependencies, and deferred scope), system-level cross-surface invariant stories and a QA matrix, a dependency & sequencing plan with parallelizable work, Definitions of Ready and Done, and deferred-scope, owner-clarification, and drift-warning registers. Story acceptance is anchored to each source spec's conformance (positive) and fail conditions (negative); source specs govern. It binds every guardrail — only canonical specs in scope; superseded specs not implemented; Recommendation only in Finding context; Confidence is trust in understanding never project health/readiness/probability; stale means previous analysis never current; only reanalysis changes assessment; history append-only; Chat and Companion not destinations; Export packages existing understanding only; Awareness creates no tasks; Invite/share enforces no permissions; context preserved; no forbidden capabilities; classify before specification; conflicts escalated not coded — and introduces no APIs, events, schemas, implementation, styling, governance, execution, automation, agents, permissions enforcement, billing, notification infrastructure, or assessment behavior.*

**Release 1 UX Product Backlog v1 complete.**
