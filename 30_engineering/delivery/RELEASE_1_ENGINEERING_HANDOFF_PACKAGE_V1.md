# Release 1 Engineering Handoff Package v1

**Document Type:** Engineering Handoff — the first document engineering (and Claude Code) reads · **Status:** **Handoff-Ready (2026-06-04)** · **Date:** 2026-06-04
**Reflects:** DL-043 (ratified) · the reorganized tree (commit `734e18a`) · the pre-handoff audit (`RELEASE_1_PRE_HANDOFF_AUDIT_001`).

> **Read me first.** This package points to the canonical foundation, states what is **Ratified vs Ready-for-Review vs Historical**, gives the build order, the hard rules, the readiness score, and the residuals. If you read one more doc after this, read the **Cognitive Responsibility Architecture Specification** and **DL-043**.
>
> **To actually start building**, read the **[Engineering Onboarding Runbook](RELEASE_1_ENGINEERING_ONBOARDING_RUNBOOK_V1.md)** (`03_architecture/`) — it sequences the who-does-what (Claude Code access, GitHub, environment bring-up, the per-wave loop). Tracker import and the env-bind starter kit (docker-compose, CI, `.env`) live in `30_engineering/delivery/`.

---

## 0. What OSLO Is (one paragraph)

OSLO is a **Planning Intelligence / Understanding-Improvement System**: it ingests project artifacts, builds an evidence-grounded understanding, assesses it (findings, issues, confidence), advises (recommendations, clarifications), and surfaces how understanding **changes over time**. The user retains authority — **OSLO recommends; the user decides; only evidence and action change understanding.** The governing principle for engineering: **OSLO never asserts truth or accepts interpretations** — it records *what evidence says*, *what OSLO computed* (with confidence), and *what the user decided*, each as an attributed, replayable record.

## 1. The Canonical Foundation — read in this order

| # | Document | Folder | Status |
|---|---|---|---|
| 1 | **Cognitive Responsibility Architecture Specification** | `30_engineering/specifications/` | **Canonical (DL-043 A)** |
| 2 | **DL-043** decision + disposition | `00_owner/decisions/decision_log.md` + `…_DL043_DISPOSITION.md` | **Ratified w/ Conditions** |
| 3 | **Epistemic State Model** · **Derived Cognition Lifecycle** · **User Acceptance / Plan-Fact** | `00_owner/architecture_decisions/` | **Ratified (DL-043 D/E/G)** |
| 4 | **Runtime Object Model** · **Behavior Model** · **Ownership Update** · **Logical Data Model** | `30_engineering/runtime_models/` | **Ratified/updated (DL-043)** |
| 5 | **Contract Inventory** · **Contract Generation Plan** | `20_handoff/contracts/` | **Updated (DL-043)** |
| 6 | **QA Governance** · **Observability Governance** | `01_governance/` | **Ratified (DL-043 H/I)** |
| 7 | **Application/Platform Classification** | `01_governance/` | **Ratified (DL-043 J)** |
| 8 | **Autonomous Implementation Control System** · **Claude Code Implementation Constraints** | `01_governance/` | **Ratified / Pending-ratify** |
| 9 | **Runtime Environment Constraint Profile** + **DL-043 reconciliation** + **Calibration Defaults** | `30_engineering/environment/` | **Owner-provided / R1–R5 confirmed** |

## 2. The Architecture in Five Sentences

1. **Responsibilities, not layers:** `Perceive → Retain → Infer → Evaluate → Advise → Disclose`, with **Act/Adapt** (recompute) cross-cutting and **Render** a non-cognitive service. One producer per output.
2. **Canonical = Attested:** Retain stores only **attributed, re-derivable** assertions — three attesting sources: **evidence**, **OSLO-self** (Cognition History Records), **user** (acceptance records + plan facts). Append-only.
3. **Cognition is Derived:** Findings/Issues/Confidence/CAF/Recommendations/Clarifications are **non-canonical, recomputable**; each emission **appends a Cognition History Record** (never overwrites). *Only recompute changes assessment.*
4. **No Authority engine in R1:** admission is **integrity-gated**; exposure is **epistemic-safety disclosure**; the user (not OSLO) accepts — recorded as **user-attested plan facts**. Outcome/Agent Governance is **deferred**.
5. **Two-axis replay:** every *record* replays exactly (audit); every *derivation* replays exact-if-rule / semantic-if-AI. Uncertainty is a **first-class label** (Attested/Derived + confidence band + conflict), surfaced by Disclose — never shown as settled.

## 3. Contract Roadmap & Build Order

All contract packages live in `20_handoff/contracts/`. Each is an **Impl + QA + Observability** triad.

| Wave | Package(s) | Owner | Status |
|---|---|---|---|
| **A** | 001 Artifact Intake · 002 Canonical Knowledge Retention · 00R Recompute/Stale Backbone | Perceive · Retain · Act/Adapt | **Ready for Review** |
| **B** | Understanding (Finding; Issue/Confidence/Reliability/CAF/Outcome Confidence) | Infer · Evaluate | **Ready for Review** |
| **C** | Advisory (Recommendation; Clarification) | Advise | **Ready for Review** |
| **U** | User Acceptance & Reconciliation (User Acceptance Record; plan fact; Acceptance-Impact) | Perceive/Retain/Infer/Evaluate/Disclose | **Ready for Review** |
| **E** | Disclose surfaces (MRI, Panels, Issue cards, Overview, Companion, Notifications, History, Exports) | Disclose / Render | **Ready for Review** |
| ~~D~~ | ~~Authority/Exposure~~ | — | **Removed from R1 (Future)** |

**Critical path:** A → B → C, with **U** after the cognition emissions exist and **E** parallelizable from object-model completion. **Coding an increment requires its approved contract triad** (Control System hard gate).

## 4. Environment & Code (from the Runtime Environment Constraint Profile)

- **Stack:** LangGraph (domain StateGraphs + reusable subgraphs, checkpointing). **Postgres** = append-only system of record (Attested assertions, Cognition History Records, User Acceptance Records, plan facts); **Neo4j** = dependency/relationship graph; **MongoDB** = artifact bodies; **Qdrant** = embeddings; **Redis** = live Derived-projection cache / sessions / event streams.
- **LLM:** OpenAI primary, Anthropic fallback, behind one **provider-abstraction** module; record `model_version` on every emission.
- **Deploy:** Heroku (backend) · Vercel (frontend) · Dev→Staging→Prod.
- **Code-tree & rules:** `01_governance/CLAUDE_CODE_IMPLEMENTATION_CONSTRAINTS_V1` — code organized by **responsibility** (`/backend/responsibilities/...`), **no Authority module**, canonical/derived stores separate, ratified-stack-only deps behind repository interfaces.
- **Owner-confirmed reconciliations (R1–R5):** human step = **record user acceptance** (not OSLO governance); **receipts are the system of record** (live findings are a refreshing view); "governance actions" events renamed to integrity/acceptance/recompute; RBAC ≠ Authority; logs map to the receipts + two-axis replay. Numbers in **Calibration Defaults** (owner-review pending).

## 5. The Hard Rules (engineering invariants — never violate)

1. **Canonical = Attested**; never write a Derived interpretation as Attested (one-way flow).
2. **Recompute appends a Cognition History Record; never overwrites.** Only recompute changes an assessment.
3. **OSLO never accepts/asserts truth.** The user accepts → a **user-attested plan fact** (canonical) + acceptance record; OSLO's recommendation stays Derived. Plan-fact ≠ world-truth.
4. **No Authority engine in R1** (integrity-gated admission; Disclose-side exposure).
5. **Disclose presents, never generates;** uncertainty (Attested/Derived + band + conflict) is always visible.
6. **One producer per output;** dependencies flow downward only.
7. **Every governed output has positive AND negative tests** (QA Governance) and emits its observability events.
8. **Build only what an approved contract specifies; stop and escalate at anything undefined** (Control System / Claude Code Constraints).

## 6. Readiness Re-Assessment (supersedes the historical "NOT READY ≈ 46%" audit)

| Area | Score | Note |
|---|---|---|
| Architecture | **95%** | Cognitive Responsibility canonical (DL-043); ESC-0 closed |
| Epistemic model & lifecycle | **95%** | Attested/Derived, history, two-axis replay ratified |
| Contracts | **90%** | Full roadmap generated (A/B/C/U/E) **+ consolidated conformance review (all CONFORMANT)**; owner approval pending |
| Data model | **85%** | Logical model complete; physical binding at env-bind |
| Environment | **85%** | Profile provided + reconciled; numeric calibration defaulted |
| Governance (QA/Obs/Control/Classification) | **90%** | Ratified; Claude Code Constraints pending owner ratification |
| Repository hygiene | **95%** | Reorganized, reference-intact, DL-043-consistent (audit 001) |
| Deployment | **85%** | **Deployment Governance v1 authored** (gates/branch/rollback/secrets/migration discipline); pending owner ratification; pipeline config at env-bind |
| **Overall** | **≈ 93% — READY WITH CONTROLS** | up from ≈46%; all four prior Criticals resolved; remaining gap is owner-ratification + build-time binding (appropriately open) |

## 7. Before Autonomous Coding Begins — owner actions

1. **Ratify `CLAUDE_CODE_IMPLEMENTATION_CONSTRAINTS_V1`** — it governs how Claude Code builds (the one standing pre-code gate).
2. **Approve the Wave contract packages** — all five are **CONFORMANT** per `contracts/WAVE_CONTRACT_PACKAGES_CONFORMANCE_REVIEW_001`; owner approval (per wave or as a set) is the remaining step.
3. **Confirm or adjust the Calibration Defaults** (`environment/RELEASE_1_CALIBRATION_DEFAULTS_V1`).
4. **Ratify `DEPLOYMENT_GOVERNANCE_SPECIFICATION_V1`** before the first production deploy (authored; concrete pipeline config produced at env-bind).

## 8. Maturity Ladder (so nobody mistakes status)

- **Ratified (build against these):** Cognitive Responsibility Architecture; DL-043 foundation (epistemic model, lifecycle, user-acceptance); object/behavior/ownership/data models; QA & Observability Governance; Application/Platform Classification; Control System.
- **Ready-for-Review (approve before coding):** Wave A/B/C/U/E contract packages (**conformance-reviewed CONFORMANT** — `contracts/WAVE_CONTRACT_PACKAGES_CONFORMANCE_REVIEW_001`); Claude Code Implementation Constraints (owner ratify); Deployment Governance (owner ratify, before production).
- **Owner-input pending (non-blocking):** numeric calibration; Deployment Governance.
- **Historical (reasoning trail — do not treat as current scope):** the pre-DL-043 reviews/audits under `03_architecture/reviews/` and the legacy layer material under `legacy_layer_engineering/` (all bannered).

## 9. Where Things Live (reorganized tree)

- `01_governance/` — doctrine, constitution, **decisions** (DL ledger), governance specs (QA/Obs/Control/Classification/Claude-Code), changelog.
- `30_engineering/specifications/ · runtime_models/ · contracts/ · decisions/ · reviews/ · environment/ · legacy_layer_engineering/`.
- `02_product/specs/ux · models · decisions · audits_reviews · data_api_nfr · testing_fixtures · planning` (+ `CURRENT_TRUTH.md` at root — *secondary representation under DL-043*).
- `04_research/`, `raw/` — **Source Material, non-binding** (never an implementation source).

---

*This Engineering Handoff Package is the first-read entry point for the Release 1 build. It states what OSLO is and the governing principle that OSLO never asserts truth or accepts interpretations; indexes the canonical foundation in reading order (Cognitive Responsibility Architecture, DL-043, the epistemic/lifecycle/user-acceptance decisions, the runtime and data models, the contract inventory/plan, QA/Observability governance, the platform classification, the control system and Claude Code constraints, and the environment profile with its owner-confirmed reconciliations); summarizes the architecture in five sentences (responsibilities not layers; Canonical = Attested across evidence/OSLO/user sources; cognition is Derived and recompute-appends; no Authority engine in R1; two-axis replay with uncertainty as a first-class label); gives the contract roadmap and build order (Wave A→B→C→U with E parallel; Wave D removed); the environment/code binding (LangGraph, Postgres-as-system-of-record with Neo4j/Mongo/Qdrant/Redis, provider-abstracted OpenAI/Anthropic, Heroku/Vercel, responsibility-organized code-tree, R1–R5 reconciliations); the eight non-negotiable engineering invariants; a readiness re-assessment of ≈88% READY WITH CONTROLS that supersedes the historical 46% audit; the owner actions required before autonomous coding (ratify the Claude Code constraints, approve waves, confirm calibration; deployment governance before production); the maturity ladder distinguishing ratified vs ready-for-review vs owner-input-pending vs historical; and the reorganized repository map. It introduces no new architecture and routes the standing owner actions accordingly.*

**Release 1 Engineering Handoff Package v1 complete.**
