# OSLO Linear Initiatives v2

**Document:** OSLO_LINEAR_INITIATIVES_V2.md
**Status:** Release 1 Linear initiative structure (capability mapping + epic/story decomposition)
**Authoritative Sources:** `OSLO_RELEASE_1_MASTER_SPEC.md` (§19 initiative structure — approved, not under review) · `OSLO_CAPABILITY_MATRIX_V2.md` (98 capabilities)
**Not used:** `OSLO_LINEAR_INITIATIVES_V1.md` or any prior roadmap / initiative structure
**Date:** 2026-05-31

> **Scope of this document.** The initiative hierarchy is taken **verbatim from Master Spec §19** (20 initiatives) and is treated as approved. No initiative is invented, merged, or split. This document only (1) maps capabilities into the approved initiatives, (2) generates epics, (3) generates story categories, (4) validates coverage, (5) validates dependency sequencing, (6) identifies critical-path initiatives, (7) identifies parallelizable initiatives.
>
> **Governance.** Non-canonical planning artifact (analysis & recommendation). It does not ratify or adopt content; the repository owner governs adoption. Canonical terminology preserved.

---

## 0. How to read this

- **Initiatives** = the 20 approved §19 initiatives (I1–I20), used exactly as written.
- **Epics** (`I{n}-E{m}`) are proposed groupings of capabilities for delivery.
- **Story Categories** are suggested backlog buckets beneath each epic (not individual stories).
- **Capability IDs** (e.g., `CAF-01`) reference `OSLO_CAPABILITY_MATRIX_V2.md`.
- **Alpha Phase** references the §19 Alpha Release Sequencing (Phase 1–6); `Foundational` and `Cross-cutting` denote work that underpins or spans phases.

**Placement note (platform capabilities).** The matrix's Platform Services domain is distributed across the approved initiatives by §19 intent: core substrate needed from Phase 1 (`PLAT-01` State Persistence, `PLAT-02` Event Orchestration, `PLAT-06` Object & Data Model) maps to **I1 Project Foundation**; security/audit/compliance maps to **I19 Security, Compliance & Platform Hardening**; performance/compute/AI-cost (`PLAT-03/04/05`) maps to **I20 Performance, Compute & AI Cost Optimization**. No new initiative is created.

---

## 1. Initiative → Capability Map (summary)

| Init | Initiative (per §19) | Alpha Phase | Priority | #Caps | Capabilities |
|---|---|---|---|---|---|
| I1 | Project Foundation | Foundational (P1) | Critical | 8 | PF-01, PF-02, PF-03, PF-04, PF-05, PLAT-01, PLAT-02, PLAT-06 |
| I2 | Evidence Ingestion | Phase 1 | Critical | 4 | EI-01, EI-02, EI-03, EI-04 |
| I3 | Planning Synthesis Engine | Phase 1 | Critical | 4 | PS-01, PS-02, PS-03, PS-04 |
| I4 | Artifact Workspace | Phase 1 | Critical | 7 | AW-01, AW-02, AW-03, AW-04, AW-05, AW-06, AW-07 |
| I5 | CAF Engine | Phase 1 | Critical | 5 | CAF-01, CAF-02, CAF-03, CAF-04, CAF-05 |
| I6 | Confidence Engine | Phase 1 | Critical | 7 | CONF-01, CONF-02, CONF-03, CONF-04, CONF-05, CONF-06, CONF-07 |
| I7 | Fast Pass | Phase 1 | Critical | 3 | AE-01, AE-04, AE-05 |
| I8 | Deep Pass | Phase 2 | High | 3 | AE-02, AE-03, AE-06 |
| I9 | CAF Overlay System | Phase 2 | Critical | 3 | OVL-01, OVL-02, OVL-03 |
| I10 | Issue Engine | Phase 1–2 | Critical | 4 | ISS-01, ISS-02, ISS-03, ISS-04 |
| I11 | Recommendation Engine | Phase 2 | Critical | 5 | REC-01, REC-02, REC-03, REC-04, REC-05 |
| I12 | OSLO Chat | Phase 3 | High | 4 | CHAT-01, CHAT-02, CHAT-03, CHAT-04 |
| I13 | MRI | Phase 1 (evolves) | Critical | 7 | MRI-01, MRI-02, MRI-03, MRI-04, MRI-05, MRI-06, MRI-07 |
| I14 | Collaboration | Phase 4 | Medium | 3 | COLLAB-01, COLLAB-02, COLLAB-03 |
| I15 | CAF Review Requests | Phase 4 | High | 5 | CRR-01, CRR-02, CRR-03, CRR-04, CRR-05 |
| I16 | Sharing | Phase 5 | High | 5 | SHARE-01, SHARE-02, SHARE-03, SHARE-04, SHARE-05 |
| I17 | Telemetry | Cross-cutting (P1+) | High | 7 | TEL-01, TEL-02, TEL-03, TEL-04, TEL-05, TEL-06, TEL-07 |
| I18 | Monetization | Phase 6 | Medium | 4 | MON-01, MON-02, MON-03, MON-04 |
| I19 | Security, Compliance & Platform Hardening | Foundational (P1) | Critical | 7 | SEC-01, SEC-02, SEC-03, SEC-04, SEC-05, SEC-06, SEC-07 |
| I20 | Performance, Compute & AI Cost Optimization | Cross-cutting (P2+) | High | 3 | PLAT-03, PLAT-04, PLAT-05 |

**Total mapped: 98 / 98 capabilities across 20 initiatives.**

---

## 2. Initiatives, Epics & Story Categories

### I1 — Project Foundation  ·  Foundational (P1) · Critical · Deps: epic-level interleave with I19 (I1-E1 ← I19-E1) — no initiative-level cycle

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I1-E1 | Identity & Alpha Access | PF-01, PF-05 | I19-E1 | Invitation/activation flow; waitlist linkage; account activation; (future) pre-account session |
| I1-E2 | Project & Workspace Data Model | PF-03, PLAT-06 | — | Object schema (19 objects); workspace/project CRUD; relationship modeling; schema migrations |
| I1-E3 | Project Initiation & Overview | PF-02, PF-04 | I2, I6-E1, I13-E1 | Start-method chooser; name inference; overview assembly; analysis-status indicators |
| I1-E4 | Persistence & Event Bus | PLAT-01, PLAT-02 | I1-E2 | State stores (Confidence/CAF/MRI/Issue/Rec/Understanding/CRR); event bus; recompute dispatch; snapshotting |

### I2 — Evidence Ingestion  ·  Phase 1 · Critical · Deps: I1

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I2-E1 | Multi-Format Ingestion & Intake Paths | EI-01, EI-03 | I1-E4 | Upload pipeline; PDF/DOCX/TXT parsers; prompt/describe; template start; guided intake |
| I2-E2 | Claim Extraction & Maturity Handling | EI-02, EI-04 | I2-E1 | Claim extraction model; epistemic tagging; planning-maturity detection; no-gate promotion |

### I3 — Planning Synthesis Engine  ·  Phase 1 · Critical · Deps: I2

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I3-E1 | Synthesis Pipeline | PS-01, PS-03 | I2-E2 | Evidence extraction; context expansion; planning construction; understanding evaluation |
| I3-E2 | Artifact Generation & Lifecycle | PS-02, PS-04 | I3-E1 | 7 artifact generators (Intent/Context/Scope/Req/WBS/Resources/Schedule); editability; lifecycle state machine |

### I4 — Artifact Workspace  ·  Phase 1 · Critical · Deps: I3

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I4-E1 | Workspace Shell & Artifact Views | AW-01, AW-02 | I3-E2 | Workspace layout; 7 artifact views; rich-text editing |
| I4-E2 | Editing Paths | AW-03, AW-04 | I4-E1, I8-E1, I11-E3 | Direct edit + change detection; assisted edit; accept/modify/reject |
| I4-E3 | Persistent Intelligence & Navigation | AW-05, AW-06, AW-07 | I5-E1, I6-E1, I10-E1, I11-E1 | Confidence/CAF bar; issues & recs panel; bidirectional cross-object navigation |

### I5 — CAF Engine  ·  Phase 1 · Critical · Deps: I3

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I5-E1 | CAF Core Scoring | CAF-01, CAF-02, CAF-03, CAF-04 | I3-E1 | Clarity/Alignment/Feasibility scorers; CAF aggregation; CAF-state persistence; reliability signaling |
| I5-E2 | CAF Issue Taxonomy | CAF-05 | I5-E1 | Finding-type taxonomy; dimension-mapping rules; finding→issue routing |

### I6 — Confidence Engine  ·  Phase 1 · Critical · Deps: I5

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I6-E1 | Confidence Core | CONF-01, CONF-02, CONF-03 | I5-E1 | Derive-from-CAF; numeric score + bands; explainability generator |
| I6-E2 | Confidence Evolution | CONF-04, CONF-05, CONF-06, CONF-07 *(F)* | I6-E1, I8-E2 | History/trend; progressive stages; false-confidence detection; (future) operational confidence |

### I7 — Fast Pass  ·  Phase 1 · Critical · Deps: I3, I5, I6, I10, I11, I13

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I7-E1 | Fast Pass Orchestration | AE-01 | I3, I5-E1, I6-E1, I10-E1, I11-E1, I13-E1 | 60-second pipeline; parallel orchestration; reliability/maturity signaling; initial-output bundle |
| I7-E2 | Understanding Progression | AE-04, AE-05 | I7-E1 | Understanding-state model; progressive disclosure UX; interpretation-unstable handling |

### I8 — Deep Pass  ·  Phase 2 · High · Deps: I1, I5, I6

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I8-E1 | Event-Driven Recompute Engine | AE-03 | I1-E4 | Event handlers (edit/chat/collab/CRR); trigger rules; incremental recompute; no-change-no-reanalysis |
| I8-E2 | Understanding Expansion | AE-02, AE-06 *(F)* | I8-E1, I5-E1, I6-E1 | Finding maturation; alignment/feasibility validation; recommendation expansion; (future) understanding debt |

### I9 — CAF Overlay System  ·  Phase 2 · Critical · Deps: I5, I4

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I9-E1 | Overlay Engine & Panel | OVL-01, OVL-02 | I5-E1, I4-E1 | In-artifact anchoring; overlay rendering; panel content (dimension/type/impact/rec) |
| I9-E2 | Overlay Actions | OVL-03 | I9-E1, I12-E1, I14-E1 | Ask OSLO; resolve; comment; dismiss; share-for-review *(actions land as their target initiatives ship)* |

### I10 — Issue Engine  ·  Phase 1–2 · Critical · Deps: I5

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I10-E1 | Issue Generation & Severity | ISS-01, ISS-02 | I5-E2 | Issue formulation from findings; severity classification (Critical/Moderate/Warning) |
| I10-E2 | Issue Lifecycle & Linkage | ISS-03, ISS-04 | I10-E1, I4-E3 | Lifecycle states (Detected→…→Resolved); artifact linking; navigation |

### I11 — Recommendation Engine  ·  Phase 2 · Critical · Deps: I10

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I11-E1 | Recommendation Generation | REC-01, REC-05 | I10-E1 | Rec generation (what/why/dimension/impact); validation recommendations |
| I11-E2 | Actions & Lifecycle | REC-02, REC-03 | I11-E1 | Accept/Modify/Reject/Discuss/Apply/Share; lifecycle; verification |
| I11-E3 | Suggested Fixes | REC-04 | I11-E1 | One-click fix generation; apply-to-artifact; allowance gating |

### I12 — OSLO Chat  ·  Phase 3 · High · Deps: I3, I5, I6, I10, I11

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I12-E1 | Project-Aware Chat | CHAT-01, CHAT-02 | I3, I5-E1, I6-E1, I10-E1, I11-E1 | Chat runtime; project context binding; context inheritance from issue/rec/artifact/CRR |
| I12-E2 | Chat Functions & Edits | CHAT-03, CHAT-04 | I12-E1, I4-E2, I8-E1 | Explain/Clarify/Resolve/Improve; generate artifact edits; trigger Deep Pass |

### I13 — MRI  ·  Phase 1 (evolves through P4) · Critical · Deps: I5, I6, I10, I11

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I13-E1 | MRI Generation & Components | MRI-01, MRI-02, MRI-03 | I5-E1, I6-E1, I10-E1, I11-E1 | Understanding synthesis; component assembly; MRI states (Interpretation Unstable→Validated) |
| I13-E2 | MRI Visualizations | MRI-04, MRI-05, MRI-06 | I13-E1 | Artifact understanding heatmap; CAF triangle; understanding timeline |
| I13-E3 | Understanding Dependencies | MRI-07 | I13-E1, I15-E2 | Blocked-by-review surfacing; awaiting-input counts |

### I14 — Collaboration  ·  Phase 4 · Medium · Deps: I4, I19, I8

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I14-E1 | Comments, Replies & Mentions | COLLAB-01, COLLAB-02, COLLAB-03 | I4-E1, I19-E1, I8-E1 | Comment threads; replies; mentions; activity preservation; deep-pass trigger |

### I15 — CAF Review Requests  ·  Phase 4 · High · Deps: I9, I11, I8, I13

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I15-E1 | Review Request & Package | CRR-01, CRR-02 | I9-E2, I11-E1 | Share-for-review; stakeholder selection; review-package builder |
| I15-E2 | Responses & Feedback Loop | CRR-03, CRR-04, CRR-05 | I15-E1, I8-E1 | Reviewer responses (comment/approve/reject/alternative); evidence creation + deep pass; status visibility |

### I16 — Sharing  ·  Phase 5 · High · Deps: I13, I19

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I16-E1 | Sharing & Permissions | SHARE-01, SHARE-03, SHARE-05 | I19-E1 | Project/artifact sharing; permission levels; link management |
| I16-E2 | MRI Sharing & Export | SHARE-02, SHARE-04 | I13-E1 | Public/private links; view sharing; PDF export |

### I17 — Telemetry  ·  Cross-cutting (P1+) · High · Deps: I1

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I17-E1 | Telemetry Infrastructure | TEL-01 | I1-E4 | Event schema; ingestion pipeline; sink/warehouse |
| I17-E2 | Domain Instrumentation | TEL-02, TEL-03, TEL-04, TEL-05, TEL-06, TEL-07 | I17-E1 + source domains | Journey; understanding; improvement; collaboration; virality; conversion event sets |

### I18 — Monetization  ·  Phase 6 · Medium · Deps: I1, I11, I17

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I18-E1 | Tier & Usage Limits | MON-01, MON-03 | I1-E2 | Free-tier scope enforcement; project/chat/rec-application limits |
| I18-E2 | Fix Allowance & Upgrade | MON-02, MON-04 | I11-E3, I17-E2 | Daily fix reset; usage metering; contextual upgrade prompts |

### I19 — Security, Compliance & Platform Hardening  ·  Foundational (P1) · Critical · Deps: epic-level interleave with I1 (I19-E2 ← I1-E2; I19-E3 ← I1-E4) — no initiative-level cycle

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I19-E1 | Authentication & Authorization | SEC-01, SEC-02 | — | Email/password; Google SSO; Microsoft SSO; RBAC; session management |
| I19-E2 | Data Protection | SEC-03, SEC-04, SEC-05 | I1-E2 | Workspace/project isolation; encryption in transit/at rest; secret management |
| I19-E3 | Audit & Compliance | SEC-06, SEC-07 | I1-E4 | Audit logging; activity tracking; SOC 2 readiness; GDPR considerations |

### I20 — Performance, Compute & AI Cost Optimization  ·  Cross-cutting (P2+) · High · Deps: I7, I8

| Epic | Name | Capabilities | Dependencies | Suggested Story Categories |
|---|---|---|---|---|
| I20-E1 | Deep Pass Efficiency | PLAT-03 | I8-E1 | Debounce windows; event consolidation; analysis queues; cooldown; incremental reanalysis |
| I20-E2 | AI Cost & Performance | PLAT-04, PLAT-05 | I7-E1, I8-E2 | Token/compute minimization; artifact/finding reuse; parallel/async/queue/horizontal scaling |

---

## 3. Capability Coverage Validation

**Result: 98 / 98 capabilities mapped. 0 orphans. 0 duplicates.** Each capability appears in exactly one epic.

| Domain | Caps | Mapped Into | Count ✓ |
|---|---|---|---|
| Project Foundation (PF) | PF-01…05 | I1 | 5/5 |
| Platform (PLAT) | PLAT-01,02,06 → I1 · PLAT-03,04,05 → I20 | I1, I20 | 6/6 |
| Evidence Ingestion (EI) | EI-01…04 | I2 | 4/4 |
| Planning Synthesis (PS) | PS-01…04 | I3 | 4/4 |
| Artifact Workspace (AW) | AW-01…07 | I4 | 7/7 |
| CAF (CAF) | CAF-01…05 | I5 | 5/5 |
| Confidence (CONF) | CONF-01…07 | I6 | 7/7 |
| Analysis Engine (AE) | AE-01,04,05 → I7 · AE-02,03,06 → I8 | I7, I8 | 6/6 |
| CAF Overlays (OVL) | OVL-01…03 | I9 | 3/3 |
| Issues (ISS) | ISS-01…04 | I10 | 4/4 |
| Recommendations (REC) | REC-01…05 | I11 | 5/5 |
| OSLO Chat (CHAT) | CHAT-01…04 | I12 | 4/4 |
| MRI (MRI) | MRI-01…07 | I13 | 7/7 |
| Collaboration (COLLAB) | COLLAB-01…03 | I14 | 3/3 |
| CAF Review Requests (CRR) | CRR-01…05 | I15 | 5/5 |
| Sharing (SHARE) | SHARE-01…05 | I16 | 5/5 |
| Telemetry (TEL) | TEL-01…07 | I17 | 7/7 |
| Monetization (MON) | MON-01…04 | I18 | 4/4 |
| Security (SEC) | SEC-01…07 | I19 | 7/7 |
| **Total** | | | **98/98** |

**Future-scope capabilities (3)** are mapped but parked behind their initiative's Alpha epics: `PF-05` (I1-E1), `AE-06` (I8-E2), `CONF-07` (I6-E2). They carry no Alpha delivery commitment.

**§16 Acceptance-Criteria-backed capabilities** fall in I1–I16 (52 caps with AC). I17, I18 (partial), I19, I20 contain capabilities with **no defined AC** — flagged below as a delivery risk (acceptance must be authored before these initiatives can be "done"-defined).

---

## 4. Dependency Sequencing Validation

**Conclusion: the mapping is sequenceable with no unbreakable cycles.** Three dependency patterns need explicit handling:

1. **I1 / I19 (foundational interlock — epic-level only, no initiative-level cycle).** `I19-E1` (auth) and `I1-E2` (data model) start in parallel with no dependency between them; `I1-E4` (event bus) ← `I1-E2`; `I19-E2` (isolation) ← `I1-E2`; `I19-E3` (audit) ← `I1-E4`; `I1-E1` (Alpha Access) ← `I19-E1`; `I1-E3` (Overview) ← downstream. Resolved order: **(I19-E1 ∥ I1-E2) → I1-E4 → I19-E2 → I19-E3 → I1-E1 → I1-E3.** No cycle at epic granularity.

2. **Reverse/wrap dependency: Suggested Fixes vs Monetization.** `REC-04` (I11-E3, Phase 2) is the core improvement action; `MON-02` (I18-E2, Phase 6) only *gates* it. Build the fix capability in Phase 2 **ungated**, then wrap with the daily-fix allowance in Phase 6. The dependency is a wrap, not a blocker — annotated "gates, not blocks."

3. **Incremental-action dependency: Overlay Actions.** `OVL-03` (I9-E2) exposes Ask OSLO, Comment, and Share-for-Review, which depend on I12 (Chat, P3), I14 (Comments, P4), and I15 (CRR, P4). Ship `OVL-01/02` in Phase 2 and **light up each overlay action as its target initiative lands** rather than blocking the overlay system on later phases.

**Phase-order check (passes).** Every initiative's hard dependencies resolve in an equal-or-earlier phase:
`I1/I19 (Foundational) → I2 → I3 → {I4 ∥ I5} → I6 → I10 → I11 → I13 → I7` (Phase 1) → `I8, I9 complete, improvement loop` (Phase 2) → `I12` (Phase 3) → `I14, I15` (Phase 4) → `I16` (Phase 5) → `I18` (Phase 6); `I17` and `I20` instrument/optimize across phases. MRI's `MRI-07` (I13-E3) and confidence's `CONF-04+` (I6-E2) intentionally complete later when their upstreams (CRR, Deep Pass) exist.

---

## 5. Critical Path Initiatives

The critical path is the chain that gates the **Minimum Viable Alpha** (§19: Evidence → Planning Synthesis → Artifact Workspace → CAF → Confidence → Fast Pass → CAF Overlay → Issues → Recommendations) and the **60-second understanding** milestone (§20: Time-to-First-MRI < 60s).

**Critical-path initiatives (10):** **I1 → I2 → I3 → I5 → I6 → I10 → I11 → I9 → I13 → I7.**

- **I5 CAF Engine is the pivot.** Confidence (I6), Issues (I10), Recommendations (I11), Overlays (I9), and MRI (I13) all depend on it; it is the single highest-leverage initiative and the top schedule risk (its scoring method is unspecified — see risks).
- **I7 Fast Pass is the convergence point.** It cannot complete until I3, I5, I6, I10, I11, and I13 each produce their initial output; treat I7 as an integration initiative, not a leaf.
- **I1 + I19-E1/E2** are foundational prerequisites to the entire path (runtime, data model, auth, isolation).

§19 note: the literal MVA string does not enumerate MRI, but Fast Pass output (`AE-01`) includes Initial MRI, so **I13-E1 is on the critical path** for the signature experience even though the MVA list omits it by name.

---

## 6. Parallelizable Initiatives

Independent tracks that can proceed concurrently once their gate is met (swimlane view):

| Track | Initiatives | Can start once | Notes |
|---|---|---|---|
| **A — Intelligence / AI core (critical path)** | I2 → I3 → I5 → I6 → I10 → I11 → I7; then I8, I12, I13 | I1, I19-E1 ready | Mostly sequential; this is the spine |
| **B — Workspace & UX** | I4, I9, I13-E2 (viz), I16 | I3 (for I4); I5+I4 (for I9); I13-E1 (for I16) | Parallel to Track A after I3 |
| **C — Platform & Foundation** | I1, I19, I17, I20 | Day 1 (I1, I19); I1-E4 (I17); I8-E1 (I20) | Underpins all; runs continuously |
| **D — Growth & Collaboration** | I14, I15, I16, I18 | Phase-1 intelligence stable | I14 ∥ I15 (both P4); I16 (P5); I18 (P6) |

**Explicitly parallelizable with the critical path:** I4 (Workspace UX) alongside I5/I6 once I3 exists; I19 (Security) and I17 (Telemetry) from day one; I13 (MRI) alongside I10/I11 once I5/I6 exist; I20 (Performance) alongside Phase 2+. **Naturally parallel pairs:** I14 ∥ I15 (Phase 4); I8 ∥ I9 (Phase 2).

---

## 7. Recommended Linear Hierarchy & Counts

```
Release: OSLO Release 1 Alpha
└── Initiative (I1–I20, from Master Spec §19)
    └── Epic (I{n}-E{m}, 45 total)
        └── Story (created from the Suggested Story Categories)
```

Mapping convention for Linear:
- **Release** → one Linear Roadmap/Project label: "OSLO Release 1 Alpha."
- **Initiative** → Linear Initiative (I1–I20, names verbatim from §19).
- **Epic** → Linear Project (or Epic) under its Initiative.
- **Story Category** → Linear Issue label/grouping; individual Stories are authored beneath.
- **Alpha Phase** → Linear Cycle or milestone tag (Phase 1–6 + Foundational/Cross-cutting).

| Metric | Count |
|---|---|
| Initiatives (fixed by §19) | 20 |
| Epics | 45 |
| Capabilities mapped | 98 / 98 |
| Critical-path initiatives | 10 |
| Foundational initiatives | I1, I19 |
| Cross-cutting initiatives | I17, I20 |
| Future-scope capabilities parked | 3 (PF-05, AE-06, CONF-07) |

**Epics per initiative:** I1:4 · I2:2 · I3:2 · I4:3 · I5:2 · I6:2 · I7:2 · I8:2 · I9:2 · I10:2 · I11:3 · I12:2 · I13:3 · I14:1 · I15:2 · I16:2 · I17:2 · I18:2 · I19:3 · I20:2 = **45**.

---

## 8. Delivery Risks (sequencing-relevant)

1. **I5 CAF scoring method is unspecified** (Matrix §22 gap 1). The pivot of the critical path has no defined algorithm; this is the highest schedule risk. Resolve before Phase 1 detailed planning.
2. **I7 Fast Pass 60-second constraint with full Phase-1 outputs** (Confidence + MRI + Issues + Recs) is aggressive and depends on six initiatives converging; "supported project sizes" is undefined (gap 13). Integration-test early against the §20 metric.
3. **No Notification object/surface** (gap 5) blocks complete I14 (Collaboration) and I15 (CRR) UX — reviewers/commenters cannot be alerted. Needs an owner decision before Phase 4.
4. **External reviewer identity undefined** (gap 6) threatens I15 (CRR) and the active-virality loop. Decide reviewer auth model before Phase 4.
5. **I8-E1 Event-Driven Recompute is the backbone of the improvement loop**; correctness bugs cascade across Confidence/CAF/Issues/Recs/MRI. Pair tightly with I20-E1 efficiency from Phase 2.
6. **AC coverage gaps** in I17, I18, I19, I20 (Matrix: 46 caps lack acceptance criteria). "Done" is undefinable for these until ACs are authored.
7. **AI cost exposure** (I20) is deferred to cross-cutting/P2+, but Fast/Deep Pass are AI-heavy from Phase 1; introduce token/compute budgets early to avoid Alpha cost overruns.

---

*Linear Initiatives v2 complete. Initiative structure taken verbatim from Master Spec §19 (not under review). 98/98 capabilities mapped, 45 epics with story categories, coverage and dependency sequencing validated, critical path and parallel tracks identified. Subject to governance review before adoption.*
