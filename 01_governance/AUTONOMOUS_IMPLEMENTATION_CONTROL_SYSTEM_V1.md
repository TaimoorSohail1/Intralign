# Autonomous Implementation Control System v1

**Document Type:** Governance Specification (control system for autonomous AI development) · **Status:** **Ratified with Conditions under DL-043 (2026-06-04)** · **Date:** 2026-06-03
**Purpose:** establish the operating system that governs **how Claude Code may autonomously implement OSLO** — what it may build, what it may not, when it must stop, when it must escalate, and which architecture/artifacts have authority. **This document does not define OSLO functionality.**

> **Mode:** skeptical, evidence-based, repository-verified. **Architecture-preserving** — no new responsibility, object, layer, plane, governance/runtime concept, service, workflow, or product capability is introduced. Where an architecture conflict exists, it is **surfaced and routed to the owner, not resolved unilaterally** (per `CLAUDE.md` and `REPOSITORY_ARCHITECTURE.md`: same-tier conflicts resolve through Proposals, only the owner ratifies).

---

## Headline (stated first)

**A repository-verified, Critical architecture conflict makes a clean Active Architecture Declaration impossible without an owner decision — and that conflict is now the #1 blocker to autonomous development.**

Two documents at the **same authority tier (Implementation)** assert **different active architectures for Release 1**:

- **`CURRENT_TRUTH.md`** (dated 2026-05-31, labeled *"Active source-of-truth," "the first document every engineer reads"*) declares the active Release 1 architecture as the **legacy layer stack** — **Context Plane · Knowledge Layer · Planning Intelligence · 8 Understanding Domain Models** — and states explicitly that **"Governance is deferred… Future Architecture… not part of Release 1,"** listing **Disposition, Governance, Accepted Understanding, Review Request** as **out of scope**.
- **The Cognitive Responsibility Architecture contract stack** (this thread: Cognitive Responsibility Spec, Ownership Update, Object/Behavior Models, Contract Generation Plan, Wave-A packages) treats **Authority/Governance as IN Release 1 and cross-cutting** — Wave A seeds **promotion authorization**, Wave D completes **exposure/Authority**, and Package 003 is **Authority Promotion Authorization**.

These cannot both be the implementation target. They disagree on (a) **which architecture is active** (layer vs. responsibility), (b) **whether Governance/Authority is in Release 1** (deferred vs. foundational), and (c) **whether Disposition/Review Request are in scope.** Both sit at the **Implementation tier**, so the repository's own precedence ladder (Doctrine > Constitution > Implementation) **cannot auto-resolve them** — this requires an **owner Proposal/decision.** GOV-ARCH-001 (which would ratify the Cognitive Responsibility core) is **still pending**, so neither has superseded the other.

**Consequence:** if Claude Code began now, `CURRENT_TRUTH` would tell it to build the layer stack *without governance*, while the contract packages tell it to build the responsibility architecture *with Authority*. That is a guaranteed-drift condition. This control system therefore makes the conflict a **hard STOP** and routes it to the owner.

---

## Deliverable 1 — Active Architecture Declaration

### Architecture Inventory

| Architecture / Artifact | Tier | Status |
|---|---|---|
| Cognitive Responsibility Architecture Spec | Implementation | **Active-proposed** (pending GOV-ARCH-001 ratification) |
| Runtime Ownership Update / Object Model / Behavior Model | Implementation | **Active-proposed** (consistent with the above) |
| `CURRENT_TRUTH.md` + `OSLO_RELEASE_1_CANONICAL_SCOPE_V1` (layer stack, governance-deferred) | Implementation | **Active-declared, CONFLICTING** |
| `OSLO_ARCHITECTURE_BASELINE_V1` (layer responsibilities) | Implementation | **Active-declared (legacy framing)** |
| Legacy layer engineering dirs — `03_architecture/{components, governance_layer, judgement_layer, runtime_architecture}` | Implementation | **Transitional / Unclassified** |
| `RELEASE_1_RUNTIME_LAYER_OWNERSHIP_SPEC` · `OSLO_RUNTIME_LAYER_RECONCILIATION_DECISION_001` · `…RESPONSIBILITY_VS_LAYER_REVIEW_001` | Implementation | **Transitional bridge** (layer↔responsibility) |
| `raw/notion/**` layer specs (Context Plane, Knowledge/Reasoning/Judgment/Governance/Communication) | Source Material | **Historical / Non-binding** (`04`-equivalent) |
| Context/Knowledge/Judgment/Governance/Communication **Layer Architectures** (as standalone systems) | — | **Deprecated-as-primary** (retained only as a dependency-ordering representation under the responsibility model) |

- **Which architecture Claude Code must implement:** **UNDECIDED — owner must declare.** This control system **cannot** designate one unilaterally because the two candidates are same-tier and the resolving ratification (GOV-ARCH-001) is pending.
- **Which Claude Code must ignore:** all `raw/notion/**` and `04_research/**` (non-binding Source Material) — this is the one unambiguous exclusion.
- **Unresolved conflicts:** **Yes — Critical.** `CURRENT_TRUTH` (layer, governance-deferred) vs. Cognitive Responsibility (responsibility, Authority-in-R1).

### Active Architecture Declaration (recommended, owner-gated)

> **RECOMMENDED (requires owner ratification):** Adopt the **Cognitive Responsibility Architecture** as the single canonical Release 1 implementation target, and **supersede or reconcile `CURRENT_TRUTH.md`** accordingly (it is the forward direction this thread has been building, and it *closes* the orphaned-recommendation/governance gap that the layer stack left open). **Until the owner ratifies this (or the alternative), no autonomous implementation may begin** — the conflict is the master stop condition (Deliverable 4, ESC-0).

---

## Deliverable 2 — Artifact Precedence Model

### Artifact Authority Hierarchy (highest → lowest)

1. **Doctrine** (`01_governance/doctrine/`) — truth; wins all conflicts.
2. **Constitution** (`01_governance/constitution/`) — operationalized doctrine.
3. **Governance Specifications** (QA Governance, Observability Governance, this Control System, Classification Decisions) — govern *how* implementation proceeds.
4. **Owner-ratified Architecture Spec** (the declared canonical architecture, once Deliverable 1 resolves).
5. **Ownership Specification** → **Object Model** → **Behavior Model** (the ratified triad, in that order).
6. **Owner-approved Contract Packages** (Impl/QA/Obs) — authoritative for *what to build*, **only after package + architecture ratification**.
7. **Product Specifications** (`02_product/specs/`) — subordinate to the ratified architecture; **conflicting legacy product specs are non-authoritative until reconciled.**
8. **UX Specifications** — authoritative for surface behavior *within* the ratified architecture.
9. **Backlog Items** — proposed, not authoritative.
10. **Notes / transitional bridges** — informational.
11. **Legacy / Source Material** (`04_research/**`, `raw/notion/**`) — **non-binding; never an implementation source.**

### Conflict Resolution Rules

- **Different tiers:** higher tier wins (Doctrine > Constitution > Implementation > Source).
- **Same tier (the live case):** **Claude Code MUST NOT choose.** Same-tier contradictions (e.g., `CURRENT_TRUTH` vs. Cognitive Responsibility) are **STOP-and-escalate** conditions resolved only by an owner Proposal/decision — never by Claude Code editing canonical content or picking a side.
- **Source vs. anything canonical:** canonical wins; Source is ignored for implementation.
- **Silence:** absence of a contract/owner/binding is **not** permission to invent — it is a stop condition (Deliverable 4).

---

## Deliverable 3 — Claude Code Operating Rules

### Autonomous Development Rules

**Claude Code MAY:**
- Implement a capability **only** when its Implementation Readiness Gate (Deliverable 7) is fully satisfied.
- Implement **owner-approved contract packages** exactly as written (Impl + the QA + Obs that accompany them).
- Generate tests **from approved QA contracts**; instrument **from approved Observability contracts**.
- Implement **owner-ratified UX specifications** for surfaces whose underlying contracts are approved.
- Implement **environment-bound** specifications **once** the Runtime Environment Constraint Profile exists and is ratified.
- Ask, stop, and escalate at any ambiguity.

**Claude Code MUST NOT:**
- Invent **architecture, ownership, objects, workflows, persistence models, governance behavior, contracts, UI behavior, environment/technology choices, or deployment processes.**
- Choose between **conflicting same-tier** artifacts (especially the active-architecture conflict) — **stop instead.**
- Implement any capability whose **owner, contract, QA, observability, dependencies, or environment binding** is missing.
- Implement from **Source Material** (`04_research/**`, `raw/notion/**`) or from **unreconciled legacy** specs.
- Edit canonical content to resolve a conflict, **ratify/adopt/supersede** anything, or proceed on an **assumption** in place of a ratified decision.
- Begin **any** implementation while the **Active Architecture Declaration (Deliverable 1) is unresolved.**

---

## Deliverable 4 — Autonomous Escalation Model

### Escalation Matrix

| Condition | Severity | Required Action |
|---|---|---|
| **ESC-0 — Active-architecture conflict unresolved** (`CURRENT_TRUTH` vs. Cognitive Responsibility) | **Critical** | **HARD STOP — all implementation.** Escalate for owner Architecture Reconciliation Decision. |
| Missing/ambiguous **owner** for a capability | Critical | STOP; escalate (classify-before-build). |
| Missing **contract** (Impl/QA/Obs) for the capability | Critical | STOP; do not invent; request contract generation. |
| **Architecture/ownership conflict** (any same-tier) | Critical | STOP; escalate; never pick a side. |
| Missing **environment binding** (Constraint Profile absent) | Critical | STOP for any environment-dependent work; escalate. |
| Undefined **persistence / data model** at field level | Major | STOP for persistence work; escalate. |
| Undefined **workflow** (entry/exit/state/failure) | Major | STOP for that workflow; escalate. |
| Undefined **dependency / prerequisite contract** not yet approved | Major | WAIT; do not implement ahead of dependency. |
| **Legacy vs. new** spec disagreement on a detail | Major | STOP; escalate for reconciliation. |
| Missing **deployment** process for a release step | Critical | STOP at release boundary; escalate. |
| Ambiguous but non-conflicting wording | Minor | Request clarification; may pause locally. |

**Allowed assumptions:** **none** that substitute for a ratified decision. Claude Code may only assume that **explicitly ratified** artifacts mean what they say. **Forbidden assumptions:** any inference of architecture, ownership, objects, persistence, environment, governance, or scope not explicitly ratified — including "the obvious choice."

---

## Deliverable 5 — Repository Structure Governance

### Repository Governance Rules

Per the verified `REPOSITORY_ARCHITECTURE.md` structure:

- **Governance / canonical control:** `01_governance/` (doctrine, constitution, decisions, frameworks, QA/Observability/Control governance).
- **Architecture (canonical, contracts):** `03_architecture/` (Cognitive Responsibility Spec, Ownership/Object/Behavior, Contract Packages, Generation Framework). **Contracts live here.**
- **Product / UX specifications:** `02_product/`.
- **Execution tracking / backlog:** `05_execution/` and `01_governance/backlog/`.
- **Historical / Source (non-binding):** `04_research/**` and `raw/notion/**`.
- **Generated code:** **no governed location is defined** — there is **no code-tree convention** in the repository (it is a knowledge base). *Finding:* a code-location convention does not yet exist and must be defined before code generation.

**Does current organization support safe autonomous development?** **Partially.** Document precedence and homes are clear and verifiable; **but** (a) the **legacy layer engineering dirs** (`03_architecture/{components, governance_layer, judgement_layer, runtime_architecture}`) sit at canonical Implementation tier **unreconciled** with the responsibility architecture, and (b) there is **no code-tree convention.** Both are drift exposures (Deliverable 8).

---

## Deliverable 6 — Contract Dependency Governance

### Contract Dependency Graph (verified state)

```text
[Pkg 001 Perceive/Intake ✅ approved-pending]
        │
        ▼
[Pkg 002 Retain/Canonical ✅ generated]
        │   ▲
        │   └── requires ── [Pkg 003 Authority/Promotion ✗ NOT GENERATED]  ◀ prerequisite for clean admission
        ▼
[Wave B: Infer→Finding ✗] ─▶ [Evaluate→Issue/Confidence/CAF ✗]
        ▼
[Wave C: Advise→Recommendation/Clarification ✗]
        ▼
[Wave D: Authority/Exposure ✗]      [Wave E: Disclose surfaces ✗ — parallelizable]
Cross-cutting (every wave): Authority gates ✗ · Observability ✗ (only 001/002 instantiated)
```

- **May proceed (generation):** Pkg 003, then Wave B — **only after** ESC-0 is resolved and GOV-ARCH-001 is ratified.
- **Must wait:** Waves C/D (depend on B); live-data presentation in E (depends on D exposure).
- **Missing prerequisites:** the **Runtime Environment Constraint Profile** (blocks *all* environment binding); **Pkg 003** (referenced by Pkg 002's admission gate); the **Active Architecture Declaration** (blocks *all*).

**Is the current generation sequence safe?** **The sequence is sound; the preconditions are not met.** Generating more contracts before ESC-0 is resolved risks producing contracts against an architecture that may not be the ratified target.

---

## Deliverable 7 — Implementation Readiness Gate

### Implementation Readiness Rules

A capability **may be implemented only if ALL hold** (any failure ⇒ STOP/escalate):

1. **Active Architecture Declaration resolved** (ESC-0 cleared) — *global precondition.*
2. **Owner exists** — exactly one owning responsibility (Contract Inventory).
3. **Contract exists & is owner-approved** — Implementation Contract present.
4. **QA exists** — positive + negative validation per QA Governance.
5. **Observability exists** — events/audit/replay per Observability Governance.
6. **Dependencies satisfied** — all prerequisite contracts approved.
7. **Environment binding exists** — Runtime Environment Constraint Profile ratified and the capability bound.
8. **Code-location convention exists** — a governed place for the code to live.

**Additional requirements identified (beyond the prompt's list):** **(1)** Active Architecture resolution (the global gate above); **(2)** code-tree convention; **(3)** Claude Code operating-rule ratification (this document). Without these, items 2–7 are insufficient.

---

## Deliverable 8 — Architecture Drift Prevention

### Drift Risk Register

| Risk | Severity | Mitigation |
|---|---|---|
| **Active-architecture conflict** (`CURRENT_TRUTH` layer/governance-deferred vs. Cognitive Responsibility/Authority-in-R1) | **Critical** | ESC-0 hard stop; owner Architecture Reconciliation Decision; supersede/reconcile `CURRENT_TRUTH`. |
| **Legacy layer specs at canonical tier, unreconciled** (`03_architecture/{components,governance_layer,judgement_layer,runtime_architecture}`, `OSLO_ARCHITECTURE_BASELINE_V1`) | **Critical** | Explicit reconciliation/supersession mapping onto responsibility architecture before any build. |
| **Scope conflict on Governance/Disposition/Review Request** (in vs. deferred) | High | Resolve with ESC-0; freeze scope in the ratified architecture. |
| **Conflicting/duplicate models** (e.g., multiple CAF/Confidence/Reliability/Data-Model versions in `02_product/specs/`) | High | Designate one canonical version per concept; mark others Historical. |
| **Phantom reference — Runtime Environment Constraint Profile** (cited, absent) | High | Create + ratify the Profile; until then, environment work is blocked. |
| **Source Material mistaken for canonical** (`raw/notion/**` layer/contract specs) | Medium | Hard rule: `04`/`raw` are never implementation sources. |
| **No code-tree convention** | Medium | Define governed code locations before code generation. |
| **Terminology drift** (layer vs. responsibility vocabulary coexisting) | Medium | Canonical glossary aligned to the ratified architecture; preserve canonical terms. |

**Highest-risk drift sources currently present:** the **active-architecture conflict** and the **unreconciled legacy layer corpus** — together they mean *the repository does not currently present a single, unambiguous thing to build.*

---

## Deliverable 9 — Autonomous Development Readiness Reassessment

*Effect of **ratifying this Control System** (controls/precedence/escalation/gates), holding other artifacts constant — and correcting the prior audit's architecture score downward now that the conflict is surfaced.*

| Area | Prior (Audit v1) | With Control System (this spec) | Note |
|---|---|---|---|
| Architecture | 88% | **70%** | *Lowered* — the surfaced active-architecture conflict was previously uncredited |
| Contracts | 20% | 20% | unchanged (2 of ~12; gated by ESC-0) |
| Environment | 25% | 25% | unchanged (Profile still absent) |
| QA | 45% | 45% | unchanged |
| Observability | 50% | 50% | unchanged |
| Repository Governance | (n/a) | **72%** | precedence + structure rules now explicit; capped by legacy/code-tree gaps |
| Claude Code Controls | 28% | **72%** | this spec supplies MAY/MUST-NOT, escalation, gates |
| Deployment Readiness | 10% | 10% | unchanged |
| **Overall** | ≈46% | **≈45–48%** | controls up; architecture corrected down; net flat |

**Improvement achieved by this specification:** it converts *"unsafe and undefined"* into *"safely blocked with explicit stop/escalation gates."* That is real progress — Claude Code now has a precedence model, operating rules, an escalation matrix, and a readiness gate — **but it raises control safety, not capability readiness.**

**Remaining blockers:** ESC-0 (active-architecture conflict) · missing Environment Constraint Profile · ~10 un-generated contracts · legacy-corpus reconciliation · no code-tree convention · no deployment governance.

---

## Deliverable 10 — Final Recommendation

### Critical Findings
1. **The repository does not present a single canonical Release 1 architecture.** `CURRENT_TRUTH` (layer, governance-deferred) and the Cognitive Responsibility contract stack (responsibility, Authority-in-R1) conflict at the same tier; GOV-ARCH-001 is unratified. **This alone blocks safe autonomous development.**
2. **A large legacy layer corpus sits at canonical tier, unreconciled** — a second, structural drift source.
3. **The Runtime Environment Constraint Profile is referenced but absent** (phantom dependency).
4. **No code-tree convention and no deployment governance exist.**

### Mandatory Next Artifacts (evidence-ranked by risk reduction)
1. **Active Architecture Reconciliation Decision (owner)** — resolve `CURRENT_TRUTH` vs. Cognitive Responsibility; supersede/reconcile the loser; ratify GOV-ARCH-001. *Outranks everything — all contracts are ambiguous until this lands.*
2. **Legacy Architecture Reconciliation/Supersession Map** — reclassify the layer engineering dirs and Baseline against the ratified architecture.
3. **Runtime Environment Constraint Profile** — unblocks all environment binding.
4. **Ratify this Control System + define the code-tree convention** — turns on the operating rules and gives code a home.
5. **Remaining contract packages (003 + Waves B–E)** — generate against the now-single architecture.
6. **Deployment Governance + Product Implementation Contract type.**

*(These are derived from verified repository evidence, not assumed; note this reorders the prior audit — the architecture-conflict resolution now precedes the Environment Profile, because an environment-bound contract against the wrong architecture is worse than none.)*

### Readiness Classification

**NOT READY.** This Control System is **necessary and should be ratified**, but it is a **control layer, not a readiness unlock**: it makes autonomous development *safely blocked and predictable* rather than *possible*. Autonomous implementation must not begin until at least Mandatory Artifacts 1–4 exist and are ratified.

---

> ### Proposed Owner Resolution
> **Resolution requested:** (1) **Ratify this Autonomous Implementation Control System** as the governing operating rules for autonomous development (precedence, MAY/MUST-NOT, escalation matrix, readiness gate, drift register). (2) **Acknowledge ESC-0** — the active-architecture conflict — as a hard STOP, and issue an **Active Architecture Reconciliation Decision** (recommended: adopt the Cognitive Responsibility Architecture and supersede/reconcile `CURRENT_TRUTH`, ratifying GOV-ARCH-001). (3) Authorize Mandatory Next Artifacts 2–4 (legacy reconciliation map, Runtime Environment Constraint Profile, code-tree convention). (4) Confirm **no autonomous implementation begins** until Artifacts 1–4 are ratified.
> **Out of bounds / not done here:** this spec **resolves no architecture conflict itself**, adopts nothing, and invents no responsibility/object/concept; it defines control and routes every substantive decision to the owner.

---

*This Autonomous Implementation Control System establishes the governance operating rules for autonomous Claude Code development of OSLO, on repository-verified evidence. Its central finding is a Critical, same-tier architecture conflict: CURRENT_TRUTH.md declares an active layer-based Release 1 with governance deferred, while the Cognitive Responsibility contract stack treats Authority/governance as in-scope and foundational — and GOV-ARCH-001 remains unratified, so neither supersedes the other; this is made a hard stop (ESC-0) and routed to the owner rather than resolved unilaterally. The specification provides an architecture inventory and an owner-gated (recommended) Active Architecture Declaration; an artifact authority hierarchy (Doctrine > Constitution > Governance Specs > ratified Architecture > Ownership/Object/Behavior > approved Contracts > Product > UX > Backlog > Notes > Source) with same-tier-conflict stop rules; Claude Code MAY/MUST-NOT operating rules; an escalation matrix (missing owner/contract/environment/persistence/workflow/dependency/deployment, plus the ESC-0 architecture conflict) with no decision-substituting assumptions permitted; repository structure governance (verified homes, plus the findings that legacy layer dirs are unreconciled and no code-tree convention exists); a contract dependency graph (only Pkg 001/002 generated; 003 and Waves B–E absent; sequence sound but preconditions unmet); an eight-condition implementation readiness gate; a drift risk register whose highest items are the active-architecture conflict and the unreconciled legacy corpus; and a readiness reassessment showing the spec raises Claude Code Controls and Repository Governance while correcting Architecture downward, leaving overall readiness NOT READY (~45–48%). It recommends, evidence-ranked, an owner Active Architecture Reconciliation Decision first, then legacy reconciliation, the Runtime Environment Constraint Profile, ratification of this control system and a code-tree convention, then the remaining contracts and deployment governance. It introduces no new architecture or concepts and routes all ratification to the owner.*

**Autonomous Implementation Control System v1 complete.**
