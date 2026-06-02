# Understanding Architecture Classification Decision 001

**Document Type:** Architecture Reconciliation Decision (Classification Doctrine)
**Status:** **Ratified · Governing Taxonomy** (owner-ratified 2026-05-31) · **Date:** 2026-05-31
**Raised by:** the pattern of reconciliations required because the stack lacked a formal construct taxonomy (Finding/Recommendation Workspace→Panel; MRI umbrella; Chat as Interaction Layer; Companion as Surface; Companion→Recommendation routing).

> **Mode: Ratified classification doctrine.** This decision **establishes the canonical architecture taxonomy** for OSLO's Release 1 understanding experience and is now the **governing taxonomy**. It **modifies no existing specification**, introduces no object, and does not redefine any surface's internals — it defines **what kind of construct each surface is** and **how future constructs must be classified before being specified.** Owner-ratified (§Owner Decision); current Release 1 specs already conform, so no retroactive edits are required.

> **Why this exists.** Recent UX work required several reconciliation decisions precisely because no doctrine defined what a "Workspace," "Panel," "Companion," "Layer," or "Object" *is*. Without this taxonomy, future Release 1/Release 2 specs may reintroduce drift by minting new "workspaces," "panels," or "layers" with no criteria. This document is intended to become the **governing taxonomy** that prevents that drift.

---

## Purpose

Establish the canonical architecture taxonomy for OSLO's understanding experience. It answers:

> **"What are the canonical understanding architecture building blocks of OSLO?"**

It classifies every experience construct into exactly one canonical type, defines what each owns and may do, and sets the rules by which **future** constructs must be classified before specification.

## A. Problem

Recent UX work required reconciliation decisions because the stack lacked a classification doctrine:
- Findings were initially treated as **Workspaces**, then ratified as **Panels** (`FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md`).
- Recommendations were initially **Workspaces**, then ratified as **Panels subordinate to Findings**.
- MRI was reconciled as an **umbrella** (Workspace + Visualization Model + Snapshot + Experience) (`MRI_TERMINOLOGY_RECONCILIATION_DECISION_001.md`).
- OSLO Chat was defined as an **Interaction Layer**, not a Workspace.
- Understanding Companion was defined as a persistent **Companion Surface**, not Chat and not a Workspace.
- Companion→Recommendation navigation required a further decision (`UNDERSTANDING_COMPANION_RECONCILIATION_DECISION_001.md`).

Each was avoidable with a taxonomy. This doctrine supplies it.

## B. Decision Required

Ratify the classification of every OSLO experience construct into one of five canonical types — **Workspace, Panel, Companion Surface, Interaction Layer, Understanding Object** — each defined by: **purpose · ownership · navigation behavior · context behavior · lifecycle relationship · independent existence · destination eligibility · action-hosting · containment.**

## C. Canonical Taxonomy

### Type 1 — Workspace
**Purpose:** a **primary project-level environment** where a user performs a **major mode** of understanding work.
**Current members:** Project Overview · MRI Workspace · Artifact Workspace.

| Attribute | Rule |
|---|---|
| Ownership | owns a major **mode** of understanding work (orientation / diagnostic discovery / content) |
| Navigation | **may be a destination** (primary navigation target) |
| Context | establishes **Project Context** for the work it hosts |
| Lifecycle | persistent within a project session; entered/left via navigation |
| Independent? | **Yes** — exists as a standing environment |
| Destination? | **Yes** |
| Hosts actions? | **Yes** (the mode's actions, e.g., edit/reanalyze in Artifact) |
| Contains? | **may host** Panels, the Companion Surface, and the Interaction Layer |
| Constraint | **must not be minted for every object** — a Workspace is justified only by a **major mode** of work or **project-level** scope |

### Type 2 — Panel
**Purpose:** a **contextual structured surface** for inspecting or evaluating a **first-class object** without leaving the current Workspace.
**Current members:** Finding Panel · Recommendation Panel.

| Attribute | Rule |
|---|---|
| Ownership | owns the **structured inspection/evaluation** of one Understanding Object |
| Navigation | **not a standalone destination**; opened in context |
| Context | **preserves the underlying Workspace/context** beneath it; restores on close |
| Lifecycle | opened/closed within a Workspace; subordinate to it |
| Independent? | **No** — exists only in context |
| Destination? | **No** |
| Hosts actions? | **Yes** — the object's structured actions (e.g., accept/defer a recommendation) |
| Contains? | may invoke the Interaction Layer; **may open a subordinate Panel only where ratified** (e.g., Finding → Recommendation) |
| Constraint | never becomes a destination; never bypasses required context (e.g., Recommendation Panel only in Finding context) |

### Type 3 — Companion Surface
**Purpose:** a **persistent visibility and navigation surface** that stays available across selected Workspaces.
**Current member:** Understanding Companion.

| Attribute | Rule |
|---|---|
| Ownership | owns **continuous visibility** of existing understanding + launch/routing |
| Navigation | **not a destination**; persistent alongside Workspaces; **launches** into Panels/Workspaces/Chat |
| Context | **reads/scopes** to the current Workspace context; presentation-only |
| Lifecycle | persistent across its host Workspaces (Overview/MRI/Artifact); collapsible without effect on understanding |
| Independent? | **No** — accompanies Workspaces |
| Destination? | **No** |
| Hosts actions? | **No structured actions** — presents and routes only |
| Contains? | **launches** Panels and Chat but **does not contain** them |
| Constraint | **not Chat, not a dashboard/cockpit, not an assessment engine**; presents existing understanding only |

### Type 4 — Interaction Layer
**Purpose:** a **conversational/assistive layer** that **spans surfaces** and supports user interaction with understanding.
**Current member:** OSLO Chat.

| Attribute | Rule |
|---|---|
| Ownership | owns **conversational** explanation/clarification/navigation across surfaces |
| Navigation | **not a destination**; floats across surfaces; **routes** into Panels/Workspaces |
| Context | **context-aware (read-only)**; spans Project and Object context |
| Lifecycle | available throughout; not entered/left as a place |
| Independent? | **No** — a layer over surfaces, not a standalone place |
| Destination? | **No** |
| Hosts actions? | **No structured actions**; it explains/clarifies/routes (clarifications feed reanalysis, never change assessment directly) |
| Contains? | **routes to** Panels/Workspaces but **does not contain** them |
| Constraint | **cannot replace** structured Workspaces or Panels; never bypasses surface rules |

### Type 5 — Understanding Object
**Purpose:** a **canonical domain object** that **carries project understanding.**
**Current members:** Finding · Recommendation. *(Adjacent domain concepts — CAF, Reliability, Outcome Confidence — are assessment signals these objects relate to; they are not surfaces and are owned by their models.)*

| Attribute | Rule |
|---|---|
| Ownership | owns a unit of **understanding** (descriptive Finding / advisory Recommendation) |
| Navigation | **surfaced by** Panels/Workspaces/Companion/Chat/navigation — **not itself a surface** |
| Context | carries its own attribution/context (e.g., Recommendation → Finding) |
| Lifecycle | model lifecycle (detected/…); changed **only by reanalysis** |
| Independent? | exists in the model independent of any surface |
| Destination? | **No** — an object is **not automatically a Workspace or destination** |
| Hosts actions? | n/a (objects don't host UI actions; surfaces do, on the object) |
| Contains? | n/a |
| Constraint | **must not be inflated into a Workspace**; it is surfaced, typically by a Panel |

## D. Required Evaluations

**D1 — Why are Findings Panels, not Workspaces?** A Finding is a **descriptive Understanding Object** that explains a weakness and **requires artifact/MRI context** to be meaningful. It should **preserve the underlying context** (the artifact/overlay/lens) rather than replace it with a separate environment. A Panel inspects one object in context; a Workspace hosts a major mode. One finding is not a mode of work → **Panel**.

**D2 — Why are Recommendations subordinate to Findings?** A Recommendation **exists because a Finding exists**; its explanatory value and **attribution depend on Finding context**. Therefore the **Recommendation Panel must not open independently** — it opens only from a Finding (ratified in `RECOMMENDATION_PANEL_SPECIFICATION_V1.md` and `UNDERSTANDING_COMPANION_RECONCILIATION_DECISION_001.md`). Subordinate Panel.

**D3 — Why is Chat an Interaction Layer, not a Workspace?** Chat **spans all surfaces**, is **conversational**, **routes and explains**, is **not a destination**, and **must not replace** structured surfaces. A Workspace is a destination hosting a mode of work; Chat is a cross-cutting assistive layer → **Interaction Layer**.

**D4 — Why is the Companion a Companion Surface, not a Workspace?** The Companion is **persistent**, a **read-out/navigation** surface, **not a destination**, and **does not own deep investigation** (it routes to the surfaces that do). It accompanies Workspaces rather than being one → **Companion Surface**.

**D5 — Why is MRI a Workspace but Findings are not?** MRI is **project-level diagnostic discovery** — it organizes **many** findings through lenses/heatmaps and cross-artifact relationships (a major mode of work). A Finding is an **individual diagnostic object**; a Finding Panel explains **one**. MRI owns discovery → **Workspace**; a finding is surfaced → **Panel/Object**.

**D6 — Why is Artifact a Workspace?** Artifact **content is the source of truth** and a **primary operating surface**; **overlays and editing** happen there, and it **hosts finding context in situ**. That is a major mode of understanding work → **Workspace**.

## E. Ownership Rules

Each capability has **one owning construct type**:

| Responsibility | Owned by |
|---|---|
| **Project-level understanding home** (the orientation/home base) | **Workspace** — Project Overview |
| **Diagnostic discovery** (where weaknesses are, across the project) | **Workspace** — MRI Workspace |
| **Artifact content context** (what the content says; source of truth) | **Workspace** — Artifact Workspace |
| **Finding explanation** (why a weakness exists) | **Panel** — Finding Panel (over the Finding object) |
| **Recommendation evaluation** (what to consider) | **Panel** — Recommendation Panel (over the Recommendation object, in Finding context) |
| **Persistent understanding visibility** (always-on read-out) | **Companion Surface** — Understanding Companion |
| **Conversational clarification** (talk to OSLO) | **Interaction Layer** — OSLO Chat |
| **Understanding navigation** (movement between constructs) | the **Journey/Navigation** specs route across constructs; **Companion launches**, **Chat routes**, Workspaces/Panels are the targets — no construct *owns* navigation alone |
| **Stale-state presentation** (marking understanding as previous analysis) | **shared presentation duty, single source of truth** — every Workspace/Panel/Companion/Chat **presents** stale state consistently; the **stale condition itself** is owned upstream by the analysis/reanalysis + editing-workflow state (Orientation State Model), never invented by a surface |
| **Return / recovery context** (the path back; never stranded) | the **Journey/Navigation** layer (global navigation + Project Overview as home base + Companion read-out + Chat "where am I") — recovery is a navigation-layer responsibility, not owned by any single Workspace/Panel |
| **Understanding itself** (the carried meaning) | **Understanding Object** — Finding, Recommendation |

No two construct **types** own the same primary capability; **stale-state presentation** is a shared *presentation* duty over a single upstream-owned condition, and **navigation/recovery** is owned by the Journey/Navigation layer (constructs route to each other but do not co-own a capability).

## F. Nesting Rules

| Container | May contain / host | May NOT |
|---|---|---|
| **Workspace** | host **Panels**; host the **Companion Surface**; invoke the **Interaction Layer** | be contained by a Panel/Companion/Chat |
| **Panel** | invoke the **Interaction Layer**; **open a subordinate Panel only where ratified** (Finding → Recommendation) | become a destination; contain a Workspace; open an unratified subordinate Panel |
| **Companion Surface** | **launch** Panels and Chat; route to Workspaces | **contain** Panels/Chat/Workspaces; host structured actions |
| **Interaction Layer (Chat)** | **route** to Panels/Workspaces | **contain** Panels/Workspaces; replace them |
| **Understanding Object** | be **surfaced by** any construct | be a container or a Workspace |

Canonical rule: **Workspaces contain Panels; Companion and Chat *launch/route* but never *contain*; Objects are surfaced, never containers.**

## G. Navigation Rules

| Question | Answer |
|---|---|
| **May be destinations** | **Workspaces only** (Project Overview, MRI, Artifact). |
| **Contextual (not destinations)** | **Panels** (Finding, Recommendation). |
| **Persistent (not destinations)** | **Companion Surface**; the **Interaction Layer** is always-available/floating. |
| **Can be launched** | Panels and Chat (by Workspaces/Companion; Panels also from Object references). |
| **Can route** | Companion (launches), Chat (routes), and the Journey/Navigation layer. |
| **Hard rule** | the **Recommendation Panel opens only in Finding context** (never directly from a Workspace/Companion/Chat without a Finding). |

## H. Future Extension Rules (how to classify new constructs)

Before any future construct is specified, it must be classified by these rules:
- A **new domain object** (e.g., **Risk, Assumption, Goal**) is an **Understanding Object** and is **surfaced by a Panel** — **not** automatically a Workspace. Object-to-Workspace inflation is forbidden (§I).
- A **new diagnostic construct** becomes a **Panel** **unless** it owns **project-level discovery across many objects** (lenses/heatmaps/cross-object), in which case it may be a **Workspace** (the MRI test).
- A **new cross-cutting assistant** (conversational/assistive, spanning surfaces) is an **Interaction Layer**.
- A **new persistent read-out** (continuous visibility, routing, no deep investigation) is a **Companion Surface**.
- A construct may be a **Workspace** **only if** it owns a **major mode of work or project-level scope** and justifies a **destination**.
- When in doubt, choose the **least powerful** classification that fits (Object < Panel < Companion/Layer < Workspace) to resist proliferation.

## I. Integrity Rules

- **ACD-1.** **No object-to-Workspace inflation** — a first-class Understanding Object (Finding, Recommendation, future Risk/Assumption/Goal) is surfaced by a **Panel**, not minted as a Workspace.
- **ACD-2.** **No Panel-to-destination drift** — Panels are contextual, preserve their Workspace, and are never standalone destinations.
- **ACD-3.** **Chat (Interaction Layer) never replaces** structured Workspaces or Panels; it routes/explains/clarifies only.
- **ACD-4.** **Companion never becomes a dashboard/cockpit/assessment engine** — it presents existing understanding and routes; it hosts no structured actions.
- **ACD-5.** **No Workspace proliferation** — a Workspace requires a major mode of work or project-level scope; not every concept earns one.
- **ACD-6.** **Recommendation Panels open only in Finding context** — never independently.
- **ACD-7.** **No governance/execution/automation/agents/task/approval** creep into any understanding construct — all five types are understanding constructs; none performs work-management.
- **ACD-8.** **Only reanalysis changes assessment** — no construct (Workspace/Panel/Companion/Layer) changes CAF/Reliability/Confidence or an Object's state directly; **Objects change only by reanalysis**.
- **ACD-9.** **One capability, one owning type** (§E) — constructs route to each other but do not co-own a capability.
- **ACD-10.** **Containment per §F** — Workspaces contain Panels; Companion/Chat launch/route but never contain; Objects are surfaced, never containers.
- **ACD-11.** **Classify before specifying** — every future construct is classified by §H **before** a spec is written for it; new "workspace/panel/layer" terms may not be coined ad hoc.
- **ACD-12.** **Least-powerful classification** preferred when ambiguous (§H).
- **ACD-13.** This doctrine **defines classification only** — it redefines no surface's internals and introduces no object, API, event, implementation, or styling.

## J. Conformance Requirements

A conforming OSLO experience construct / future spec MUST (objective, structural); it **fails** if any forbidden behavior appears:

- **ACD-C1.** Be classified as **exactly one** of the five types, satisfying that type's attribute rules (§C). **Fail** if a construct is unclassified or mixes types.
- **ACD-C2.** Surface a first-class **Object via a Panel** (or existing Workspace), **not** as a new Workspace without justification (§H; ACD-1). **Fail if a first-class object is treated as a Workspace without major-mode/project-level justification.**
- **ACD-C3.** Keep **Panels contextual** (preserve underlying Workspace, never standalone) (ACD-2). **Fail if a Panel is made a standalone destination.**
- **ACD-C4.** Keep **Chat routing/explaining**, never replacing Panels/Workspaces (ACD-3). **Fail if Chat replaces a Panel or Workspace.**
- **ACD-C5.** Keep the **Companion presentation/routing only**, hosting no structured actions, not a dashboard (ACD-4). **Fail if the Companion hosts structured actions.**
- **ACD-C6.** Open **Recommendation only in Finding context** (ACD-6). **Fail if a Recommendation opens without Finding context.**
- **ACD-C7.** Make **only Workspaces destinations**; keep Panels contextual and Companion/Chat persistent/floating (§G).
- **ACD-C8.** Respect **containment** (§F; ACD-10) and **one-capability-one-owner** (§E; ACD-9).
- **ACD-C9.** Introduce **no governance/execution/automation/agents/task/approval** into any construct, and change **no assessment** outside reanalysis (ACD-7/ACD-8). **Fail if governance/execution is introduced into an understanding construct.**
- **ACD-C10.** **Classify future constructs before specifying** them, choosing the least-powerful fit (§H; ACD-11/ACD-12).

**Explicit fail conditions.** Conformance is **all-or-nothing**. A spec **fails** this doctrine if it: treats a first-class object as a Workspace without justification; makes a Panel a standalone destination; allows Chat to replace Panels/Workspaces; allows the Companion to host structured actions or become a dashboard; opens a Recommendation without Finding context; proliferates Workspaces without a major-mode/project-level basis; introduces governance/execution/automation/agents/task/approval into any understanding construct; changes assessment outside reanalysis; violates containment or one-capability-one-owner; or coins a new construct without classifying it first.

## K. Deferred Items

Explicitly **deferred / out of scope:** Release 2 construct classifications; future **governance surfaces**; future **execution surfaces**; **agent surfaces**; **mobile-specific construct behavior**; **advanced plugin/marketplace surfaces**; **external integration surfaces**; visual/styling realization of any construct; APIs/events/implementation; and any numeric/calibration values. (When Release 2 introduces governance/execution/agent/plugin/integration constructs, they require their **own** classification types or extensions — they are **not** understanding constructs and must not be retrofitted into the five types above.)

## Owner Decision

### Owner Selection
```
[x] Ratify the five-type taxonomy and rules as the governing OSLO UX architecture doctrine — RATIFIED 2026-05-31
[ ] Request revisions
```

### Effective Canonical Taxonomy (ratified)
**Workspace · Panel · Companion Surface · Interaction Layer · Understanding Object** — as defined in §C, with ownership (§E), nesting (§F), navigation (§G), future-extension (§H), integrity (§I), and conformance (§J) rules. **Status: Ratified · Governing Taxonomy.**

### Authorized (owner-ratified)
- This doctrine is now the **governing taxonomy**: future UX specs **must** classify constructs per §H **before** specification, and existing specs are read as conforming to §C (they already do: Overview/MRI/Artifact = Workspaces; Finding/Recommendation = Panels over Objects; Companion = Companion Surface; Chat = Interaction Layer).
- **No retroactive edits** are required to current Release 1 specs (they already conform); a future hygiene pass may add a one-line "Construct type:" tag to each surface spec.
- Future governance/execution/agent/plugin/integration constructs require their **own** classification types or extensions (§K) — they are not understanding constructs and must not be retrofitted into the five types.

---

*This decision proposes the canonical OSLO understanding-architecture taxonomy — Workspace, Panel, Companion Surface, Interaction Layer, and Understanding Object — defining for each its purpose, ownership, navigation/context/lifecycle behavior, independence, destination eligibility, action-hosting, and containment, and explaining why Findings/Recommendations are Panels over Objects (not Workspaces), why Recommendations are subordinate to Findings, why Chat is an Interaction Layer, why the Companion is a Companion Surface, and why MRI/Artifact/Overview are Workspaces. It sets ownership, nesting, navigation, and future-extension rules so new constructs (Risk, Assumption, Goal, new assistants, new read-outs) are classified before being specified, and integrity/conformance rules that prevent object-to-workspace inflation, panel-to-destination drift, chat replacing structured surfaces, companion-as-dashboard, workspace proliferation, and governance/execution creep. It is classification doctrine only — it redefines no surface, introduces no object, changes no assessment, and is subject to owner ratification. Only reanalysis changes assessment.*

**Understanding Architecture Classification Decision 001 complete.**
