# Release 1 Runtime Layer Ownership Specification v1

**Document Type:** Ownership Analysis (evidence-based, alignment only) · **Status:** **Superseded (secondary) by `RELEASE_1_RUNTIME_OWNERSHIP_UPDATE_SPECIFICATION_V1` under DL-043** · **Date:** 2026-05-31

> **⚠ DL-043 (2026-06-04):** This is the **layer-primary** ownership analysis. Under DL-043 the canonical ownership model is the **responsibility-primary** `RELEASE_1_RUNTIME_OWNERSHIP_UPDATE_SPECIFICATION_V1.md`. Retained as a historical/secondary dependency-ordering view; **not an implementation source.** Authority references herein are layer-stack framing — see DL-043 (Authority inactive in R1).
**Reviewed sources (repository evidence only):** `OSLO_ARCHITECTURE_BASELINE_V1.md` (§2 layer responsibilities, §3 workflow, §5 capability inventory, §9 open questions) · `03_architecture/` (`runtime_architecture/08_state_logic_state_machines.md`, `judgement_layer/09_confidence_integrity_logic.md`, `governance_layer/11_governance_override_logic.md`, `components/05_component_system_specification.md`, `README.md`) · `01_governance/` (Framework 001/001A; `CLAUDE.md`) · Release 1 UX scope (`RELEASE_1_UX_PRODUCT_BACKLOG_V1.md`, `RELEASE_1_UX_EXECUTION_PLAN_V1.md`, `RELEASE_1_UX_SCOPE_FREEZE_…`, `RELEASE_1_UX_HANDOFF_PACKAGE_…`, active Release 1 UX specs).

> **Mode: ownership analysis only.** **No inference. No rationalization. No proposed ownership. No new layers/responsibilities. No assumptions.** Repository evidence governs. Where ownership is not documented, the item is marked **Unmapped**, **Conflicting**, or **Requires Owner Decision** — gaps are not filled. No conflict is silently resolved. **Any inferred ownership is a conformance failure (§Conformance).** Note: subdirectory layer specs named in the prompt (`communication_layer/`, `context_plane/`, `knowledge_layer/`, `reasoning_layer/`) are **not present** in the repository; documented layer responsibilities are sourced from `OSLO_ARCHITECTURE_BASELINE_V1.md` §2 (the most complete documented statement found) and the four present layer-logic files.

---

## Executive Summary

The OSLO runtime cognition pipeline is **well-documented** and the Release 1 understanding objects and signals map onto it with **Confirmed** evidence for a substantial portion of scope: **Findings → Reasoning Layer**; **Issues, CAF (Clarity/Alignment/Feasibility), Confidence, Severity → Judgment Layer**; **canonical knowledge & assumptions → Knowledge Layer**; **intake/orientation → Context Plane**; **exposure dispositions (expose/suppress/defer/block) → Governance Layer**; **rendering of all surfaces → Communication Layer**.

However, **significant ownership gaps and one structural conflict** prevent full alignment:
- **Recommendation *production* has no documented owning layer** — every layer's documented non-responsibilities disclaim "recommendation generation," while the workflow (Stage 8/12) and capability inventory assert recommendations are produced. **Conflicting.**
- **MRI** is documented as a **Planned stub** ("doctrinal scoping pending," RB-015/DL-034) — **no runtime-layer ownership documented.**
- **Reliability** as a first-class signal, **Clarifications** (Clarification Engine = Planned), **escalation** (not a documented Governance disposition), and **stale/reanalysis-state labeling** lack documented layer ownership.
- **UX surface "ownership"** (Overview/MRI/Artifact Workspace/Panels/Companion/Chat/Notifications/History/Export/Sharing) is a **product/UX construct**; the runtime architecture documents only that the **Communication Layer renders** — it does not document layer *ownership* of these product surfaces.

**Final assessment: Partially Aligned** (§Final Assessment) — the cognition core is documented and largely rendered by Release 1 UX, but several first-class Release 1 concepts require owner decisions before implementation contracts are generated.

## Layer Responsibility Summary (Documented Only)

*From `OSLO_ARCHITECTURE_BASELINE_V1.md` §2. Subject: a user's outcome/project knowledge.*

- **Context Plane** — ingestion, normalization, staging, identity/idempotency, temporal ordering, promotion-readiness; **Fast Extraction → 60-Second Orientation** and **Deep Extraction**. *No governance.*
- **Knowledge Layer** — sole system of record for canonical project knowledge; append-only versioned history; records **explicit assumptions, intents, estimates, constraints**; records execution facts and governance authorization events. *No inference/scoring/generation.*
- **Reasoning Layer** — derives **Findings** (STRUCTURE_GAP, CONTENT_QUALITY_GAP, SMART_GAP, ALIGNMENT_GAP, FEASIBILITY_RISK, traceability). *No severity/confidence/recommendations/mutations.*
- **Judgment Layer** — **severity + confidence + epistemic state → Issues**; Clarity/Alignment/Feasibility scoring (Stage 10). *No exposure/authorization/recommendations.*
- **Governance Layer** — **exposure governance (expose/suppress/defer/block)** + action authorization (Tier ∩ Posture ∩ Governance); outcome resolution. *No execution/reasoning/recommendation.*
- **Communication Layer** — **render/disclose** (Communication Units), posture-aware disclosure, surface-invariant meaning. *No reasoning/authorization/recommendation generation.*
- **Execution Coordination** (emerging, posture-gated) — signal ingestion (observational), recompute triggers (always-on). *No interpretation/severity.*

## Ownership Matrix

*Columns: Ownership · Producer · Consumer · Governance · Communication (render) · Evidence · Confidence · Status. "—" = not documented. CP=Context Plane, KL=Knowledge, RE=Reasoning, JU=Judgment, GO=Governance, CO=Communication, EC=Execution Coordination, ROD=Requires Owner Decision.*

### Project Intake
| Capability | Own | Producer | Consumer | Gov | Render | Evidence | Conf | Status |
|---|---|---|---|---|---|---|---|---|
| Create Project | CP | CP | KL | — | CO | Baseline §2 CP, §3 Stage 1 | Med | **Requires Owner Decision** (CP intake documented; "project creation" not named) |
| Upload Artifact | CP | CP | KL | — | CO | §2 CP (ingestion/normalization); §3 Stage 1–4 | High | **Confirmed** (CP ingestion) |
| Paste Content | CP | CP | KL | — | CO | §2 CP; §3 Stage 1 | High | **Confirmed** (CP ingestion) |
| Orientation (60-Second) | CP→RE→JU | CP Fast Extraction; RE Fast Analysis Pass; JU scoring | CO | GO (exposure) | CO | §2 CP (Fast Extraction → 60-Second Orientation); §3 Stage 8; §5 "60-Second Orientation: Planned" | Med | **Confirmed** (pipeline) / status **Planned** per §5 |

### Knowledge Objects
| Capability | Own | Producer | Consumer | Gov | Render | Evidence | Conf | Status |
|---|---|---|---|---|---|---|---|---|
| Charter / Scope / Requirements / WBS / Resource Plan / Schedule / Summary / Project Metadata | KL (generic canonical knowledge) | CP→KL (promotion) | RE | GO (promotion authorization, G-03) | CO | §2 KL ("canonical assertions, entities, relationships"); §3 Stage 7 | Low–Med | **Requires Owner Decision** — KL stores **generic** canonical knowledge; these **specific named object types are not individually documented** as Release 1 runtime objects (Release 1 UX treats project content generically as "artifacts") |

### Understanding Objects
| Capability | Own | Producer | Consumer | Gov | Render | Evidence | Conf | Status |
|---|---|---|---|---|---|---|---|---|
| Findings | RE | RE | JU | — | CO | §2 RE; §3 Stage 8 | High | **Confirmed** |
| Issues | JU | JU | GO | GO (disposition) | CO | §2 JU; §3 Stage 9/11 | High | **Confirmed** |
| Recommendations | **—** | **—** (every layer disclaims "recommendation generation") | user | GO (constrains exposure) | CO | §2 RE/JU/GO/CO non-resp; §3 Stage 8/12; §5 Recommendation Engine; I7 | — | **Conflicting** (no documented producing layer; production asserted but disclaimed) |
| Clarifications | — | — (Clarification Engine = **Planned**) | — | — | CO | §5 "Clarification Engine: Planned" | Low | **Requires Owner Decision** |
| Assumptions | KL | KL (records explicit assumptions; epistemic status) | RE/JU | — | CO | §2 KL; §5 Assumption Detection (Doctrine 03) | High | **Confirmed** |
| Alignment Gaps | RE | RE (ALIGNMENT_GAP) | JU | — | CO | §2 RE | High | **Confirmed** |
| Coverage Gaps | RE | RE (STRUCTURE_GAP / coverage) | JU | — | CO | §2 RE ("coverage gaps, orphans") | High | **Confirmed** |
| Quality Gaps | RE | RE (CONTENT_QUALITY_GAP) | JU | — | CO | §2 RE | High | **Confirmed** |
| SMART Gaps | RE | RE (SMART_GAP) | JU | — | CO | §2 RE; §5 SMART Validation | High | **Confirmed** |

### Project Surfaces
| Capability | Own | Producer | Consumer | Gov | Render | Evidence | Conf | Status |
|---|---|---|---|---|---|---|---|---|
| Overview | — (UX surface) | — | user | GO (exposure of contents) | **CO** | §2 CO (render/disclose) | Med | **Confirmed (render=CO)** / ownership **ROD** |
| MRI | **—** | — | user | — | CO | §5 "Project MRI: **Planned** … doctrinal scoping pending (RB-015/DL-034)" | Low | **Requires Owner Decision** (runtime stub) |
| Artifact Workspace | — (UX surface) | — | user | GO (UI-authorized mutation, G-03) | CO | §2 CO; §3 Stage 7 (G-03) | Med | **Confirmed (render=CO)** / ownership **ROD** |
| Finding Panel | — (UX surface) | RE (finding content) | user | GO (exposure) | CO | §2 RE/CO/GO | Med | **Confirmed (render=CO; content=RE)** / surface ownership **ROD** |
| Recommendation Panel | — (UX surface) | **—** (see Recommendations conflict) | user | GO (exposure) | CO | §2 GO/CO; Recommendations row | Low | **Conflicting** (depends on Recommendation producer) |
| Companion | — (UX surface) | — | user | — | CO | §2 CO | Low | **Confirmed (render=CO)** / ownership **ROD** |
| Chat | — (UX surface) | — | user | GO (disclosure) | CO | §2 CO | Low | **Requires Owner Decision** (no documented runtime "chat" surface) |
| Notifications | CO | CO | user | GO (exposure/timing) | CO | §2 CO; §5 Notifications ("Communication Layer responsibility; Planned") | Med | **Confirmed (CO)** / status **Planned** |
| History | KL (append-only history) | KL | user | — | CO | §2 KL ("append-only versioned history") | Med | **Confirmed (state=KL; render=CO)** / surface ownership **ROD** |
| Export / Sharing | — | — | user | GO (exposure) | CO | §5 Sharing/Reporting ("Planned"); §2 CO | Low | **Requires Owner Decision** (Planned) |

### Understanding Signals
| Capability | Own | Producer | Consumer | Gov | Render | Evidence | Conf | Status |
|---|---|---|---|---|---|---|---|---|
| CAF (Clarity/Alignment/Feasibility) | JU | JU (Stage 10 scoring) | GO/CO | — | CO | §2 JU; §3 Stage 10; §4 drivers | High | **Confirmed** |
| Reliability | **—** | — | — | — | CO | named in §4/§9? **not a named layer driver** (drivers: Clarity/Alignment/Feasibility + evidence strength/assumption stability) | Low | **Requires Owner Decision** (not documented as a distinct runtime signal/owner) |
| Confidence (composite) | JU | JU (Doctrine 06) | GO/CO | — | CO | §2 JU; §4 Composite Confidence | High | **Confirmed** |
| Severity | JU | JU | GO | GO (disposition) | CO | §2 JU | High | **Confirmed** |
| Stale State | — | EC/RE (recompute) | — | — | CO | §3 Stage 14 (recompute); "stale" **labeling** not a named layer resp | Low | **Requires Owner Decision** |
| Reanalysis State | EC (recompute triggers) | EC | RE→JU→GO | — | CO | §2 EC; §3 Stage 14 | Med | **Confirmed (recompute=EC)** / "reanalysis state" UX label **ROD** |

### Governance Interactions
| Capability | Own | Producer | Consumer | Gov | Render | Evidence | Conf | Status |
|---|---|---|---|---|---|---|---|---|
| Clarification Requests | — | — (Planned) | — | — | CO | §5 Clarification Engine: Planned | Low | **Requires Owner Decision** |
| Recommendation Exposure | GO | GO (disposition) | CO | GO | CO | §2 GO (expose) | Med | **Confirmed (exposure=GO)** — but depends on Recommendations conflict |
| Recommendation Suppression | GO | GO (suppress) | CO | GO | CO | §2 GO (suppress) | Med | **Confirmed (suppress=GO)** |
| Recommendation Escalation | **—** | — | — | — | — | §2 GO dispositions are **expose/suppress/defer/block** — "escalate" **not named** | Low | **Requires Owner Decision** |
| Owner Review Requirements | Repository governance (owner ratifies) | — | — | — | — | `CLAUDE.md`; Framework 001 — **repository governance**, distinct from runtime Governance Layer | Med | **Confirmed (repository governance)** — **distinct subject** from runtime GO |

## Gap Register (no documented ownership)

| Gap | Capability | Required clarification |
|---|---|---|
| G-1 | **Recommendation production** | Which layer produces Recommendations? Every layer disclaims "recommendation generation" while §3/§5/I7 assert production. |
| G-2 | **MRI** | MRI is a Planned stub (RB-015/DL-034); no runtime-layer ownership documented. |
| G-3 | **Reliability** | Reliability is a first-class Release 1 signal but is not a documented runtime driver/owner. |
| G-4 | **Clarifications / Clarification Requests** | Clarification Engine is Planned; no owning layer documented. |
| G-5 | **Recommendation Escalation** | "Escalate" is not a documented Governance disposition. |
| G-6 | **Stale-state labeling** | Recompute is documented (Stage 14); "stale" labeling is not a named layer responsibility. |
| G-7 | **UX surface ownership** | Overview/MRI/Artifact/Panels/Companion/Chat/Export/Sharing — runtime documents render (CO) only, not surface ownership. |
| G-8 | **Named Knowledge object types** | Charter/Scope/WBS/Resource Plan/Schedule are not individually documented runtime objects (KL stores generic canonical knowledge). |

## Conflict Register (conflicting evidence)

| Conflict | Description | Conflicting sources | Required owner decision |
|---|---|---|---|
| C-1 | **Recommendation generation owner** | §2 RE/JU/GO/CO all disclaim "recommendation generation" **vs** §3 Stage 8/12 + §5 Recommendation Engine + I7 asserting recommendations are produced | Which layer (or new component) owns Recommendation production? |
| C-2 | **"Finding" terminology** | Release 1 UX uses **Finding** as the canonical descriptive object **carrying severity**; runtime documents **Finding** (Reasoning, no severity) and **Issue** (Judgment, has severity) as **distinct** | Is the UX "Finding" the runtime Finding, the runtime Issue, or a composite? |
| C-3 | **Architecture representation under review** | `OSLO_ARCHITECTURE_BASELINE_V1.md` §9 Q#20 — "Surface B / native repository reconciliation … under governance review (GOV-ARCH-001/001A/000)" | Confirm authoritative architecture representation before binding ownership |
| C-4 | **"Governance" overlap** | Runtime **Governance Layer** (exposure/authorization) vs **repository governance** (owner ratification) | Confirm the two are distinct (Owner Review row) |

## Owner Decision Register

1. Recommendation production owner (C-1/G-1).
2. UX "Finding" vs runtime Finding/Issue reconciliation (C-2).
3. MRI runtime ownership / scope (G-2; RB-015/DL-034).
4. Reliability signal owner (G-3).
5. Clarification ownership (G-4).
6. Escalation as a Governance disposition (G-5).
7. Stale/reanalysis-state labeling owner (G-6).
8. Whether UX surfaces have runtime-layer ownership beyond CO rendering (G-7).
9. Named Knowledge object typing (G-8).
10. Authoritative architecture representation (C-3) and the two governances (C-4).

## Coverage Summary (per Release 1 Epic)

*Coverage = share of the epic's first-class artifacts with a **Confirmed** runtime mapping (produce/consume/govern/render) on documented evidence; Unmapped/Conflicting/ROD as marked. Qualitative bands, repository-evidence-only.*

| Epic | Confirmed | Unmapped/Conflicting | ROD |
|---|---|---|---|
| EP-1 App Shell & Navigation | Low (render=CO only) | — | High (surface ownership ROD) |
| EP-2 Entry & Onboarding | **High** (CP intake; orientation pipeline) | — | Low (Create-Project naming) |
| EP-3 Project Discovery | Low (render=CO) | — | High (project-list a UX construct) |
| EP-4 Project Overview | Med (signals=JU; render=CO) | — | Med (surface ownership) |
| EP-5 MRI | **Low** | — | **High** (MRI stub, G-2) |
| EP-6 Artifact Workspace & Editing | Med (KL state; G-03 mutation; render=CO) | — | Med (overlay = UX) |
| EP-7 Finding & Recommendation Panels | Med (Finding=RE) | **High** (Recommendation production C-1) | Med |
| EP-8 Understanding Companion | Low (render=CO) | — | High (surface ownership) |
| EP-9 OSLO Chat | Low | — | **High** (no documented runtime chat) |
| EP-10 Collaboration & Sharing | Low | — | High (Sharing Planned) |
| EP-11 Notification & Awareness | Med (CO; Planned) | — | Med |
| EP-12 History & Timeline | Med (KL append-only; render=CO) | — | Med (surface) |
| EP-13 Export & Share-Out | Low | — | High (Planned) |
| EP-14 Help & Support | — | — | **High** (no runtime concept) |
| EP-15 Settings & Tier Visibility | Low (Tier documented; periphery) | — | High (UX periphery) |
| EP-16 Cross-Surface Invariants | Med (signals/exposure documented) | Conflicting (C-1/C-2) | Med |

**Strongest documented alignment:** EP-2 (intake/orientation), understanding objects/signals (Findings/Issues/Gaps/CAF/Confidence/Severity), exposure governance, and rendering. **Weakest:** EP-5 MRI, EP-9 Chat, EP-14 Help, and Recommendation production (EP-7).

## Final Assessment

**PARTIALLY ALIGNED** (repository-evidence-only).

- The **OSLO cognition core is documented** and Release 1 understanding objects/signals map onto it with **Confirmed** evidence: Findings→Reasoning; Issues/CAF/Confidence/Severity→Judgment; assumptions/canonical knowledge & history→Knowledge; intake/orientation→Context Plane; exposure dispositions→Governance; **all surface rendering→Communication**. Release 1 UX is, in large part, the **Communication-Layer rendering** of these documented runtime outputs plus **Context-Plane intake**.
- **But alignment is not full:** **Recommendation production has conflicting evidence and no documented owning layer (C-1)**; **MRI is a Planned stub (G-2)**; **Reliability, Clarifications, escalation, and stale-state labeling lack documented ownership (G-3–G-6)**; UX **surface ownership** beyond rendering is undocumented (G-7); and named **Knowledge object types** are not individually documented (G-8). The architecture representation itself is **under governance review (C-3)**.
- Therefore Release 1 is **not "Fully Aligned"** (multiple first-class capabilities lack documented runtime ownership) and **not "Significant Ownership Gaps"** in the dismissive sense (the cognition core and most understanding objects/signals are Confirmed). It is **Partially Aligned**: a documented, render-ready cognition core with a bounded set of **owner-decision-blocking gaps** (Recommendation production, MRI, Reliability, Clarifications, escalation) that must be resolved **before** implementation contracts are generated for the affected capabilities.

## Conformance Requirements

This analysis **fails** if it: infers any ownership; creates a new responsibility or layer; assumes undocumented ownership; silently resolves a repository conflict; omits any Release 1 capability; or presents any recommendation as fact rather than owner decision. *This document is constructed to satisfy these requirements: every mapping cites evidence; undocumented ownership is marked Unmapped/Conflicting/Requires-Owner-Decision; conflicts are cited and left unresolved; every listed capability category is included; the final assessment is justified on repository evidence only and proposes no ownership.*

---

*This evidence-based ownership analysis maps the entire Release 1 product scope onto the documented OSLO runtime layers (Context Plane, Knowledge, Reasoning, Judgment, Governance, Communication, Execution Coordination — per OSLO_ARCHITECTURE_BASELINE_V1.md §2 and the present layer-logic files). It records documented layer responsibilities, then provides an ownership matrix (Ownership/Producer/Consumer/Governance/Communication + evidence + confidence + status) across Project Intake, Knowledge Objects, Understanding Objects, Project Surfaces, Understanding Signals, and Governance Interactions, marking each capability Confirmed / Unmapped / Conflicting / Requires-Owner-Decision. It finds the cognition core documented and Confirmed (Findings→Reasoning; Issues/CAF/Confidence/Severity→Judgment; assumptions/knowledge/history→Knowledge; intake/orientation→Context Plane; exposure→Governance; rendering→Communication) while flagging that Recommendation production has conflicting evidence with no documented owning layer, MRI is a Planned stub, and Reliability/Clarifications/escalation/stale-state-labeling/UX-surface-ownership/named-Knowledge-object-types lack documented ownership. It records eight gaps, four conflicts (including the GOV-ARCH architecture-representation review and the runtime-Finding-vs-Issue terminology question), a ten-item owner-decision register, and a per-epic coverage summary, concluding — on repository evidence only — that Release 1 is Partially Aligned with the OSLO runtime architecture, with a bounded set of owner-decision-blocking ownership gaps to resolve before implementation-contract generation. It infers no ownership, resolves no conflict, creates no layer or responsibility, and proposes no solution.*

**Release 1 Runtime Layer Ownership Specification v1 complete.**
