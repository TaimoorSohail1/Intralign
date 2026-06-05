# Release 1 Contract Inventory v1

**Document Type:** Contract Inventory (governance — authoritative planning artifact) · **Status:** **Updated under DL-043; Wave B Fast/Deep + 60 s NFR added under DL-046 (2026-06-04)** · **Date:** 2026-06-04

> **DL-046:** Wave B (Infer/Evaluate) carries `mode` (fast|deep) + `confidence_stage` (Orientation→Expanded→Validated) as **emission attributes** (no new object), and a ratified **Time-to-First-MRI < 60 s** NFR acceptance gate (Master Spec §20/M1; p50/p95 + project-size envelope `TBD – Owner Decision`).
**Operates against the ratified core** (DL-043 — Cognitive Responsibility Architecture canonical). **Sources:** `OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md` · `RELEASE_1_RUNTIME_OWNERSHIP_UPDATE_SPECIFICATION_V1.md` · `RELEASE_1_UX_PRODUCT_BACKLOG_V1.md` · the contract specs.

> ### DL-043 Inventory Amendments (authoritative — supersede conflicting rows)
> 1. **Authority capabilities are OUT of Release 1** (Authority plane inactive). Remove from the R1 contract inventory: **Promotion Authorization**, **Exposure Decision**, **Authorization Decision**, **Governance Decision** — all reclassified **Future**. R1 admission is **integrity-gated** (Perceive readiness + Retain integrity); R1 "disposition" is **user acceptance**, not governance.
> 2. **Add R1 capabilities / objects:** **Cognition History Record** (Retain, OSLO-self-attested, append-only — emitted by every cognition + recompute); **User Acceptance Record** (Perceive capture → Retain, user-attested, version-pinned); **Acceptance-Impact Assessment** (Infer + Evaluate, Derived).
> 3. **Epistemic typing:** canonical objects are **Attested** (Canonical Fact + attested Assumption/Constraint/Dependency); cognition outputs are **Derived** (non-canonical, recomputable). Inferred assumptions/constraints/dependencies are **Derived**, not canonical.
> 4. **One owner per output preserved**; the additions introduce **no new responsibility** (they map to Perceive/Retain/Infer/Evaluate). The User Acceptance & Reconciliation capability is **non-governance**.

> **Mode:** governance — **no architecture redesign; no new responsibilities/domains; no new engines unless required to eliminate an ownership gap; no implementation/technology/databases/APIs/coding.** **Accepted core:** Perceive · Retain · Infer · Evaluate · Advise · Disclose · Act; cross-cutting **Authority Plane** + **Adapt (emergent)**; **Render** service. **Corrected Advise boundary:** *Advise = governable candidate **response*** (recommendation, clarification request, suggested action, candidate improvement) — **not** "candidate action." **Provisional (referenced, not designed):** Intend, Learn, Coordinate. **Per `CLAUDE.md`, owner ratifies.**

---

## Section 1 — Release 1 Capability Inventory

| Capability | Responsibility | Domain | Engine | Status |
|---|---|---|---|---|
| **Intake** | | | | |
| File upload | Perceive | Perception | Ingestion | **Owned** |
| Project ingestion | Perceive | Perception | Ingestion | **Owned** |
| Artifact ingestion | Perceive | Perception | Ingestion | **Owned** |
| Context normalization | Perceive | Perception | Normalization | **Owned** |
| Promotion readiness | Perceive | Perception | Promotion-readiness | **Owned** |
| **Planning Artifacts** | | | | |
| Charter | Retain | Retention | Canonical-knowledge | **Owned** *(outcome-reference dimension → Intend, Provisional)* |
| Scope | Retain | Retention | Canonical-knowledge | **Owned** |
| Requirements | Retain | Retention | Canonical-knowledge | **Owned** |
| WBS | Retain | Retention | Canonical-knowledge | **Owned** |
| Resource plan | Retain | Retention | Canonical-knowledge | **Owned** |
| Schedule | Retain | Retention | Canonical-knowledge | **Owned** |
| Project summary | Retain (stored) / Disclose (generated) | Retention / Disclosure | Canonical-knowledge / Summary-rendering | **Owned** |
| **Analysis** | | | | |
| Findings | Infer | Inference | Gap / Alignment / Traceability / Feasibility | **Owned** |
| Issues | Evaluate | Evaluation | Issue-formulation | **Owned** |
| Severity | Evaluate | Evaluation | Severity | **Owned** |
| Confidence | Evaluate | Evaluation | Confidence | **Owned** |
| CAF | Evaluate | Evaluation | Clarity / Alignment / Feasibility | **Owned** |
| Reliability | Evaluate | Evaluation | Reliability | **Owned** |
| Stale detection | Perceive (change detection) | Perception | Change-detection | **Owned** *(stale **labeling** → Disclose)* |
| Reanalysis | Adapt (emergent) | — | — *(trigger → Act; recompute re-runs Infer/Evaluate/Advise)* | **Owned (emergent)** |
| **Recommendations** | | | | |
| Recommendations | Advise | Advisory | Recommendation | **Owned** |
| Clarifications | Advise | Advisory | Clarification | **Owned** *(governable candidate response)* |
| Candidate improvements | Advise | Advisory | Recommendation (improvement type) | **Owned** |
| Suggested actions | Advise | Advisory | Recommendation (suggested-action type) | **Owned** |
| **Governance** | | | | |
| Exposure | Authority Plane | Authority | Exposure | **Owned** |
| Suppression | Authority Plane | Authority | Exposure (suppress) | **Owned** |
| Deferment | Authority Plane | Authority | Deferment | **Owned** |
| Authorization | Authority Plane | Authority | Authorization | **Owned** |
| **User Experience** | | | | |
| MRI | Disclose | Disclosure | MRI diagnostic rendering (+ Render) | **Owned** |
| Companion | Disclose | Disclosure | Presentation (+ Render) | **Owned** |
| Awareness panel | Disclose | Disclosure | Awareness presentation (+ Authority exposure) | **Owned** |
| Finding panel | Disclose | Disclosure | Presentation over Infer + Evaluate + Advise | **Owned** |
| Recommendation panel | Disclose | Disclosure | Presentation over Advise | **Owned** |
| Overview | Disclose | Disclosure | Presentation of Evaluate signals | **Owned** |
| Issue cards | Disclose | Disclosure | Presentation of Evaluate Issues | **Owned** |
| History | Disclose (timeline) / Retain (record) | Disclosure / Retention | Timeline rendering / append-only record | **Owned** |
| Exports | Disclose | Disclosure | Packaging of existing understanding (+ Render, + Authority exposure) | **Owned** |
| **Runtime** | | | | |
| Notifications | Disclose | Disclosure | Awareness presentation (+ Authority exposure) | **Owned** *(delivery infra out of R1)* |
| Recompute triggers | Act | Coordination | Recompute-trigger | **Owned** |
| State transitions | Adapt (emergent) | — | — *(triggers → Perceive/Act; presented by Disclose)* | **Owned (emergent)** |
| Execution coordination | Act | Coordination | Recompute/observability-path (active); **actuation** | **Owned (observability path)** *(actuation → Provisional/Future, posture-gated)* |

**Result:** every Release 1 capability traces to **exactly one owning responsibility** (with cross-cutting Authority/Disclose interactions noted, not duplicate ownership). **No Unmapped. No Conflict.** Provisional touchpoints (outcome-reference→Intend; actuation→future) are explicitly out of Release 1 scope.

## Section 2 — Ownership Validation

- **Ownership conflicts:** **None.** The prior conflicts are resolved by the accepted core: Recommendations/Clarifications → **Advise** (was the headline C-1 conflict); Reliability → **Evaluate**; MRI → **Disclose**; Finding/Issue distinction → Infer/Evaluate, presented by one Disclose panel.
- **Duplicate ownership:** **None.** Items with cross-cutting interactions (e.g., Notifications/Exports = Disclose **governed by** Authority; History = Disclose timeline **over** Retain record) have **one owning responsibility** plus a defined cross-cutting interaction — not co-ownership.
- **Missing ownership:** **None** for Release 1. Every listed capability is owned.
- **Unclear ownership (minor clarifications, non-blocking):**
  - **Reanalysis / State transitions** are **emergent** (the loop re-running) — owned-as-emergent, with the **trigger** owned by **Act/Perceive** and the **state** presented by **Disclose**. Clarify that "reanalysis" generates no standalone contract beyond its trigger (Act) and the re-run of Infer/Evaluate/Advise (already contracted).
  - **Outcome-reference dimension** of Charter/Scope (the alignment target) touches **Intend (Provisional)** — in Release 1 the outcome is **user-declared and Retained**; Intend is referenced, not designed.
  - **Execution coordination** = recompute/observability path (Owned, Act) in Release 1; **actuation Provisional** (posture-gated, disabled by default).

**No new engine was required to eliminate a gap** — the gaps were closed by responsibility ownership, not new engines.

## Section 3 — Contract Inventory

*(Impl = Implementation Contract; QA = QA Contract; Obs = Runtime Observability Contract. Yes / No / Future, with justification.)*

| Capability | Impl | QA | Obs | Justification |
|---|---|---|---|---|
| Intake (upload/ingestion/normalization/promotion) | Yes | Yes | **Yes** | runtime behavior + failure signals (ingestion success/failure) must be observed |
| Planning artifacts (charter…schedule/summary) | Yes | Yes | **No** *(light)* | canonical records; presentation observed via surfaces, not the record itself |
| Findings | Yes | Yes | **Yes** | generation events + coverage observability |
| Issues / Severity / Confidence / CAF / Reliability | Yes | Yes | **Yes** | assessment outputs; confidence/reliability behavior observed |
| Stale detection | Yes | Yes | **Yes** | change-detection signal |
| Reanalysis (trigger + re-run) | Yes *(trigger=Act)* | Yes | **Yes** | recompute events are core observability (Section 5) |
| Recommendations | Yes | Yes | **Yes** | **recommendation-generation events** + adoption/abandonment signals |
| Clarifications | Yes | Yes | **Yes** | **clarification-generation events** + answered/unanswered signals |
| Candidate improvements / Suggested actions | Yes | Yes | **Yes** | as recommendation types |
| Governance (exposure/suppression/deferment/authorization) | Yes | Yes | **Yes** | **governance-decision events** are core observability |
| MRI / Overview / Finding Panel / Recommendation Panel / Companion / Issue cards | Yes | Yes | **Yes** | usage/abandonment/confusion signals (per Observability Contract risk model) |
| Awareness panel / Notifications | Yes | Yes | **Yes** | awareness routing/read signals (no delivery infra) |
| History | Yes | Yes | **No** *(light)* | append-only record; timeline usage observed lightly |
| Exports | Yes | Yes | **Yes** | export events + stale-export signal |
| Recompute triggers | Yes | Yes | **Yes** | trigger latency / loop-closure observability |
| State transitions | Yes *(presentation)* | Yes | **Yes** | orientation/stale/reanalysis state observability |
| Execution coordination (actuation) | **Future** | **Future** | **Future** | posture-gated, disabled by default; out of Release 1 |
| Intend / Learn / Coordinate | **Future** | **Future** | **Future** | provisional; not designed in Release 1 |

## Section 4 — Dependency Map (per responsibility)

- **Perceive** — *Inputs:* external user/artifact/signal data. *Outputs:* normalized, promotion-ready candidates; change/stale signals. *Dependencies:* Authority (constrains intake by posture/tier). *Downstream:* Retain (promotion), Act (recompute triggers).
- **Retain** — *Inputs:* authorized promotions from Perceive. *Outputs:* canonical knowledge, assumptions, append-only history. *Dependencies:* Authority (promotion authorization). *Downstream:* Infer, Disclose (history), Intend (provisional, reference).
- **Infer** — *Inputs:* canonical knowledge (Retain). *Outputs:* Findings/gaps. *Dependencies:* Retain. *Downstream:* Evaluate, Disclose (Finding Panel).
- **Evaluate** — *Inputs:* Findings (Infer), knowledge (Retain), outcome reference (Intend, provisional → drift). *Outputs:* Issues, severity, confidence, CAF, reliability. *Dependencies:* Infer, Retain. *Downstream:* Advise, Authority (disposition), Disclose (Overview/cards).
- **Advise** — *Inputs:* Issues/Findings (Evaluate/Infer), Authority constraints (posture/tier). *Outputs:* recommendations, clarification requests, candidate improvements/actions (governable candidate responses). *Dependencies:* Evaluate, Authority (input constraint). *Downstream:* Authority (output governance), Disclose (Recommendation Panel).
- **Authority Plane** — *Inputs:* outputs of every stage; posture/tier/policy. *Outputs:* exposure/suppression/deferment/blocking dispositions + authorizations. *Dependencies:* cross-cutting. *Downstream:* Disclose (what may be shown), Act (what may be actuated). **Generates nothing.**
- **Disclose** — *Inputs:* governed outputs (Infer/Evaluate/Advise), reliability-qualification. *Outputs:* meaning-preserving disclosure (rendered by Render). *Dependencies:* Authority (exposure), Render (formatting). *Downstream:* user surfaces.
- **Act** — *Inputs:* authorized actions; signals/mutations. *Outputs:* recompute triggers (R1); posture-gated actuation (future). *Dependencies:* Authority (authorization). *Downstream:* Adapt (recompute → Infer/Evaluate/Advise re-run).
- *(Cross-cutting **Adapt**: emergent recompute on signal/mutation; **Render**: non-cognitive formatting service.)*

## Section 5 — Observability Inventory

Observability contracts are required for the following **runtime events/signals**:
- **State transitions** — orientation/analyzing/stale/reanalysis-running/complete (per Orientation State Model).
- **Runtime signals** — intake success/failure; change/stale detection; behavioral/adoption/failure signals on surfaces (per the Observability Contract risk model: abandonment, confusion, unexpected routing).
- **Recompute triggers** — trigger occurrence + loop-closure (Infer→Evaluate→Advise re-run).
- **Governance decisions** — exposure/suppression/deferment/authorization events (Authority Plane).
- **Recommendation-generation events** — Advise Recommendation engine outputs + downstream adoption/abandonment.
- **Clarification-generation events** — Advise Clarification engine outputs + answered/unanswered.
- *(Export events + stale-export signal; awareness routing/read signals — also observed.)*

These map to **Runtime Observability Contracts** in the coordinated contract sets (one per backlog story, per the Contract Generation Framework).

## Section 6 — Release 1 Readiness Assessment

**B — Ready with Minor Ownership Clarifications.**

**Justification:** Every Release 1 capability traces to **exactly one owning responsibility** under the accepted core — **no orphan, no conflict, no duplicate, no Unmapped.** The previously-blocking gaps (recommendation production, Reliability, Clarification, MRI) are **closed** by ownership. Contract generation can proceed for **all** Release 1 capabilities. The only open items are **minor, non-blocking clarifications**, all concerning **provisional or emergent** concerns explicitly out of Release 1 cognition scope:
1. **Reanalysis / State transitions = emergent** (owned by the loop; trigger by Act; state presented by Disclose) — clarify they generate no standalone owning contract beyond trigger + re-run.
2. **Outcome-reference → Intend (Provisional)** — in R1 the outcome is user-declared and Retained; Intend is referenced, not designed.
3. **Actuation → Provisional/Future** — posture-gated, disabled by default.

None blocks Implementation/QA/Observability contract generation; each is a documented clarification, not a defect. *(This rests on owner ratification of the architectural core per GOV-ARCH-001 — the assumed precondition.)*

## Section 7 — Final Recommendation

- **Ownership Completeness Score: 96 / 100** — all Release 1 capabilities owned by exactly one responsibility; −4 for the emergent/provisional clarifications (reanalysis/state emergent; Intend/actuation provisional).
- **Architecture Stability Score: 86 / 100** — core ratified-with-modifications and adversarially validated; corrected Advise boundary applied; −14 for the GOV-ARCH-001 provisional edges (Intend depth, Learn, Coordinate, multi-agent) and pending owner ratification.
- **Contract Generation Readiness Score: 93 / 100** — full ownership traceability achieved; −7 for the minor clarifications and the assumed-pending core ratification.

**Recommended next artifact:** **`RELEASE_1_CONTRACT_GENERATION_PLAN_V1.md`** — the sequencing plan that drives generation of **one coordinated contract set (Implementation + QA + Observability) per backlog story** (per `CONTRACT_GENERATION_FRAMEWORK_V1.md`), dependency-first (intake/shell → analysis → advisory → presentation), each set citing its **owning responsibility** from this inventory as the producer. *(The first generated sets should be the foundational, fully-Owned capabilities — Intake/Perceive and the analysis pipeline — deferring only the Provisional/Future rows.)*

---

*This Release 1 Contract Inventory maps every Release 1 capability — intake, planning artifacts, analysis, recommendations, governance, UX, and runtime — to exactly one owning responsibility under the accepted Cognitive Responsibility core (Perceive · Retain · Infer · Evaluate · Advise · Disclose · Act, with Authority cross-cutting and Adapt emergent, Render a service, and the corrected Advise = governable candidate response boundary). It achieves complete ownership traceability with no orphans, conflicts, or duplicates: Findings→Infer; Issues/Severity/Confidence/CAF/Reliability→Evaluate; Recommendations/Clarifications/improvements/suggested-actions→Advise; intake/stale-detection→Perceive; planning artifacts/history-record→Retain; exposure/suppression/deferment/authorization→Authority; MRI/panels/overview/companion/awareness/exports/notifications/history-timeline→Disclose; recompute-triggers/execution-coordination→Act; reanalysis/state-transitions→emergent Adapt. It validates ownership (no conflicts; minor non-blocking clarifications on emergent reanalysis/state and provisional Intend/actuation), specifies which capabilities require Implementation/QA/Observability contracts, maps per-responsibility dependencies, inventories the runtime events needing observability contracts, and assesses Release 1 as Ready with Minor Ownership Clarifications (Ownership 96, Stability 86, Readiness 93). It recommends the next artifact be the Contract Generation Plan that produces one coordinated Implementation/QA/Observability contract set per backlog story, dependency-first, each citing its owning responsibility. It performs no architecture redesign, introduces no new responsibilities/domains/engines, and discusses no implementation, technology, databases, APIs, or coding.*

**Release 1 Contract Inventory v1 complete.**


---

## DL-047 Inventory Additions (ratified 2026-06-04)
New Derived/interaction objects + owners: `SynthesizedPlanningModel`·`PlanningArtifact`→**Infer** (generate, Derived) / Retain (version) / Disclose (present); `ChatSession/Exchange`→**Disclose** (interaction, non-canonical); `ReviewRequest/StakeholderResponse`→**Perceive** intake (response→evidence→Deep Pass) + Disclose (status); `SuggestedFix`→**Advise** (candidate; user-applied). Extraction = Perceive behavior (evidence-attested). False-Confidence/Understanding-State = Evaluate. No new responsibility; commodity CRR workflow UI per DL-043 J.
