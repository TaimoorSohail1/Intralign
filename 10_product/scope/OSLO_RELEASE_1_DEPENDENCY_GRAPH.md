# OSLO Release 1 Dependency Graph

**Document:** OSLO_RELEASE_1_DEPENDENCY_GRAPH.md
**Status:** Release 1 dependency model (re-evaluated — not a restatement of prior sequencing)
**Authoritative Sources:** `OSLO_RELEASE_1_MASTER_SPEC.md` (§19 sequencing, §18 object model) · `OSLO_CAPABILITY_MATRIX_V2.md` (98 capabilities, §22 gaps) · `OSLO_LINEAR_INITIATIVES_V2.md` (20 initiatives, 45 epics)
**Not used:** any prior dependency document or architecture diagram as authority
**Date:** 2026-05-31

> **Method.** Dependencies were re-derived from first principles using (a) capability-level dependencies in the matrix, (b) the §18 object-model lineage, and (c) the §19 sequencing — *in that order of authority for data necessity*. The V2 sequence was **not assumed correct**; §1.1 records the dependency errors found in V2 and the corrections applied here.
>
> **Governance.** Non-canonical planning artifact (analysis & recommendation). Does not ratify or adopt. Canonical terminology preserved.
>
> **Deep Analysis Pass note (founder decision).** **Deep Pass / `I8` (the Deep Analysis Pass) is an active, required Release 1 capability.** Where this graph shows the Minimum Viable Alpha *excluding* I8, that reflects **intra-Release-1 sequencing** (Deep Analysis runs after the 60-Second Orientation), not optional or future status. Deep Analysis is part of the Recommended Alpha (Phase 2), is **not** optional, **not** Release 2, and **not** Future Architecture; it improves understanding and performs no governance.

**Dependency-type definitions**

- **Hard** — cannot build or function without the prerequisite (data or functional necessity; confirmed by capability dep and/or object-model lineage).
- **Soft** — functions in a degraded/partial form without it; the prerequisite completes the capability.
- **Preferred** — sequencing convenience or richer output; not required for the capability to exist.

---

## Part 1 — Initiative Dependency Analysis

### 1.1 Dependency errors found in V2 (re-evaluation results)

Re-deriving against capability deps and the §18 object model surfaced **three dependency defects** in `OSLO_LINEAR_INITIATIVES_V2.md`. They are corrected in this model:

| # | Defect in V2 | Why it's wrong | Correction applied here |
|---|---|---|---|
| D-1 | `I3-E2` (Artifact Generation) depends on `I4-E1` (Workspace shell) | Artifact generation is a backend synthesis step producing Artifact objects; the workspace only renders/edits them. The §18 lineage is Evidence → **Artifacts** → ArtifactSections, with no UI in the chain. | Reverse it: **I4 depends on I3**, never the inverse. I3 needs only I1 (data model) + I3-E1. |
| D-2 | `I5-E2` (CAF Issue Taxonomy) ↔ `I10-E1` (Issue Engine) mutually depend | A circular dependency. The taxonomy is a classification scheme that must exist *before* the Issue Engine can classify. | Make it one-directional: **I5-E2 → I10-E1**. Taxonomy precedes issue generation. |
| D-3 | `I1 ↔ I19` modeled as a mutual initiative dependency | Reads as an initiative-level cycle. In fact auth (`SEC-01`) has no dependency on the OSLO data model, and the data model has no dependency on auth. | Treat as an **epic-level interleave, not a cycle**: I19-E1 ∥ I1-E2/E4 start together; I19-E2/E3 follow I1's data model; I1-E1/E3 follow auth. No cycle. |

A fourth item is a **modeling clarification, not an error**: V2 sequences `I8` (Deep Pass) strictly after `I7` (Fast Pass). Re-evaluation shows Deep Pass shares the CAF/Confidence/Issue/Rec engines and the event bus; its only dependency on Fast Pass is that it *operates on* the initial model Fast Pass emits. So **I8 → I7 is Soft (sequential), not Hard** — the two can be co-developed on shared engines.

### 1.2 Initiative dependency table

Prerequisite types: **(H)** Hard · **(S)** Soft · **(P)** Preferred. Validated against §19 / capability deps / §18 object model.

| ID | Initiative | Prerequisite Initiatives | Downstream Initiatives | Rationale (capability / object-model basis) |
|---|---|---|---|---|
| I1 | Project Foundation | I19-E1 auth (S) | I2(H), I4(H), I17(H), I18(H), I19-E2/E3(H), all (H) | Object model roots here: Workspace→Users→Projects→Evidence. PLAT-01/02/06 are the persistence, event bus, and schema everything writes to. Backend buildable before auth. |
| I2 | Evidence Ingestion | I1 (H) | I3 (H) | EI-01 deps I1-E4; object Projects→Evidence. No evidence object → nothing to ingest into. |
| I3 | Planning Synthesis | I2 (H) | I4(H), I5(H), I12(H) | PS-01 deps EI-02 (claims); object Evidence→Artifacts. Synthesis consumes extracted claims. |
| I4 | Artifact Workspace | I3 (H) | I9(H), I12(S), I14(H) | AW-01 deps PS-02 (generated artifacts to render). **Does not gate I3 (see D-1).** |
| I5 | CAF Engine | I3 (H) | I6(H), I9(H), I10(H), I13(H), I15(H) | CAF-01 deps PS-03; object Artifacts→CAF Findings. **The pivot** — all intelligence consumes findings. |
| I6 | Confidence Engine | I5 (H) | I7(H), I13(H) | CONF-01 deps CAF-01. §4: "Confidence should never exist independently of CAF." |
| I7 | Fast Pass | I3,I5,I6,I10,I11,I13 (H) | I8(S), I20(P) | AE-01 orchestrates the 60-second bundle (§5: Orientation Confidence, Initial MRI, Top Issues, Suggested Fixes). **Integration endpoint, not a leaf.** |
| I8 | Deep Pass | I1 event bus(H), I5,I6(H), I10,I11(S), I7(S) | I15(H), I20(H), I12(S), I14(S) | AE-03 deps I1-E4 (event bus). Shares engines with Fast Pass; **I7 dep is Soft (see clarification).** |
| I9 | CAF Overlay System | I5(H), I4(H) | I15(H) | OVL-01 deps CAF-01 + AW-02; object CAF Findings→CAF Overlays. Overlays render findings inside artifacts. |
| I10 | Issue Engine | I5 (H) | I11(H) | ISS-01 deps CAF-05; object CAF Findings→Issues. **Taxonomy precedes engine (see D-2).** |
| I11 | Recommendation Engine | I10 (H) | I7(H), I13(P), I15(H), I18(H) | REC-01 deps ISS-01; object Issues→Recommendations. Recs target issues. |
| I12 | OSLO Chat | I3,I4(H), I5,I6,I10,I11(P) | I9(S), I4(S) | CHAT-01 needs project + artifact context (H); richer context-inheritance (CHAT-02) preferred but degradable. |
| I13 | MRI | I5,I6(H), I10,I11(P) | I7(H), I16(H) | MRI-01 needs Confidence + CAF (H); Top Issues/Opportunities components (P). Object model terminal (derived). |
| I14 | Collaboration | I4(H), I19(H), I8(S) | I15(S) | COLLAB-01 needs artifact surface + identity; deep-pass trigger Soft. **Blocked by Notification gap.** |
| I15 | CAF Review Requests | I9(H), I11(H), I5(H), I8(H), I13(S) | I13-E3(S), I16(S) | Object: CAF Finding→CRR→Stakeholder Response→New Evidence→Deep Pass. **Blocked by Notification + external-reviewer gaps.** |
| I16 | Sharing | I13(H), I19(H) | — | SHARE-02 needs MRI to share; permissions need RBAC. Terminal virality surface. |
| I17 | Telemetry | I1(H); all domains(S) | I18(H) | TEL-01 deps I1-E4 (event bus). Instruments domains incrementally. |
| I18 | Monetization | I1(H), I11(H), I17(H) | — | MON-02 gates REC-04 (fixes) and meters via I17. Terminal conversion proof. |
| I19 | Security, Compliance & Platform Hardening | I1 data model (H, for E2/E3 only) | I1 access(S), I14(H), I16(H), all(H) | SEC-01 auth has no prereq; SEC-03 isolation needs the data model. **Co-foundational with I1 (see D-3).** |
| I20 | Performance, Compute & AI Cost | I8(H), I7(P) | — | PLAT-03 optimizes Deep Pass; PLAT-04/05 optimize the AI passes. Cross-cutting; cost budgets should inform I7/I8 design early. |

---

## Part 2 — Critical Path Analysis

### 2.1 True critical path

Built from **Hard edges only**. Two co-equal hard chains of length 7 converge on Fast Pass:

```
I1 → I2 → I3 → I5 → I10 → I11 → I7        (Recommendations branch)
I1 → I2 → I3 → I5 → I6  → I13 → I7        (Confidence→MRI branch)
```

- **Critical Path Length:** **7 initiatives** (longest hard chain).
- **Critical-path required set:** Fast Pass cannot complete until **I1, I2, I3, I5, I6, I10, I11, I13** all finish → **8 initiatives** for a usable (non-Fast-Pass) Alpha, **9** including **I7** for the 60-second Recommended Alpha.
- **Shared bottleneck:** **I5 (CAF Engine)** sits on *both* branches. **Convergence point:** **I7 (Fast Pass)**.
- `I9` (Overlay) is **not** on the critical path to the user-defined MVA (Part 4); it is required only for the §19 / Recommended Alpha.

### 2.2 Per-initiative criticality

| Init | Why critical | What depends on it | If it slips |
|---|---|---|---|
| I1 Project Foundation | Object model, persistence, event bus — the substrate every write targets | Everything | Total program stall; nothing can persist or recompute |
| I2 Evidence Ingestion | Only entry point for project content | I3→I5→… | No evidence → no synthesis → no understanding; Alpha cannot start |
| I3 Planning Synthesis | Constructs the planning model CAF scores | I4, I5, I12 | No artifacts → CAF/Confidence/MRI have nothing to evaluate |
| I5 CAF Engine | **The pivot**; produces findings all intelligence consumes | I6, I9, I10, I13, I15 | Cascade failure across Confidence, Issues, Recs, Overlays, MRI; highest blast radius |
| I6 Confidence Engine | Headline signal; required by Fast Pass & MRI | I7, I13 | No Outcome Confidence → core value proposition undeliverable |
| I10 Issue Engine | Improvement loop entry; feeds Recommendations | I11 | No issues → no recommendations → improvement loop broken |
| I11 Recommendation Engine | Longer hard branch to Fast Pass; powers fixes | I7, I13, I15, I18 | Fast Pass loses fixes; CRR loses validation recs; monetization loses its gated action |
| I13 MRI | Signature artifact; in Fast Pass output | I7, I16 | No MRI → loses the §20 Time-to-First-MRI metric and the primary shareable surface |
| I7 Fast Pass | 60-second integration endpoint; convergence of all above | I8 (soft), I20 | Misses the core 60-second promise (§5); understanding still works but slowly |

### 2.3 Critical-path risks

- **I5 has no defined scoring algorithm** (Matrix §22 gap 1) yet sits on both branches — the single largest schedule risk.
- **I7 depends on six initiatives converging** under a hard 60-second ceiling with "supported project sizes" undefined (gap 13) — integration-bottleneck risk.
- **I10→I11→I7 is the longest hard branch**; any slip in Issues or Recommendations directly extends the path. I6→I13 is the shorter branch and has slack.

---

## Part 3 — Parallelization Opportunities

The critical path (Part 2) is internally sequential but runs **parallel to four other workstreams**. Recommended workstreams:

| Workstream | Initiatives | Starts when | Rationale |
|---|---|---|---|
| **WS-A Foundation & Platform** | I1, I19, I17, I20 | Day 1 (I1, I19-E1) | Substrate + security + telemetry infra underpin everything; build continuously. I20 joins once I8 exists. |
| **WS-B Intelligence (AI core)** | I2 → I3 → I5 → I6 → I10 → I11 → I13 → I7; then I8 | I1 + I19-E1 ready | This **is** the critical path; sequential internally, parallel to A/C/D. |
| **WS-C Workspace & UX** | I4, I9, I12, I13-E2 (viz), I16-E2 | I3 ready (I4); I4+I5 (I9) | UI track can build alongside WS-B once artifacts (I3) exist; I9 needs CAF + workspace. |
| **WS-D Collaboration & Growth** | I14, I15, I16, I18 | Phase-1 intelligence stable | Growth surfaces depend on stable understanding; I14 ∥ I15 (both P4). |

**Explicitly concurrent with the critical path:**
- **I4 (Workspace)** alongside I5/I6 once I3 exists (UX vs intelligence are independent after artifacts).
- **I19 (Security)** and **I17 (Telemetry)** from day one.
- **I13 (MRI)** alongside I10/I11 once I5/I6 exist (MRI core needs only Confidence+CAF).
- **I20 (Performance)** alongside Phase 2+ (optimize what exists).

**Naturally parallel pairs:** I8 ∥ I9 (Phase 2); I14 ∥ I15 (Phase 4).

---

## Part 4 — Alpha Path Analysis

### 4.1 Minimum Viable Alpha (demonstrate Planning Synthesis + CAF + Confidence + MRI + Recommendations)

Smallest initiative set that demonstrates the five required capabilities **end-to-end and visibly**:

**I19-E1 (auth) + I1 → I2 → I3 → I4 → I5 → I6 → I10 → I11 → I13.**  *(9 initiatives; I4 included only as the minimal surface to view synthesized artifacts and recs.)*

- Demonstrates: Planning Synthesis (I3), CAF (I5), Confidence (I6), MRI (I13), Recommendations (I11).
- **Excludes** Fast Pass (I7), Overlays (I9), Deep Pass (I8) — understanding is demonstrable without the 60-second orchestration or in-artifact overlays.
- Note: this is **narrower** than §19's "Minimum Viable Alpha," which additionally lists Fast Pass and CAF Overlay. Both definitions are recorded; this one follows the Part 4 brief.

### 4.2 Recommended Alpha (founder-approved, §13 In-Scope / §19 all phases)

MVA **plus** the full Release 1 scope, sequenced by §19 phases:
- **+ I7 Fast Pass** (Phase 1 — the 60-second experience), **I9 Overlays, I8 Deep Pass, I11 fixes** (Phase 2 improvement loop), **I12 Chat** (Phase 3), **I14 Collaboration, I15 CAF Review Requests** (Phase 4), **I16 Sharing** (Phase 5), **I18 Monetization** (Phase 6), with **I17 Telemetry, I19 Security, I20 Performance** cross-cutting.
- All 20 initiatives; this is the complete validation of understanding → improvement → refinement → collaboration → virality → conversion.

### 4.3 Deferred Alpha Scope (delayable without compromising validation)

| Deferrable | Why safe to delay |
|---|---|
| **I18 Monetization** (Phase 6) | Nothing depends on it; conversion proof can follow value proof. Most delay-safe initiative. |
| **I20 Performance/Compute** (beyond early cost budgets) | Optimization of existing passes; defer tuning, but set token/compute budgets early (cost risk). |
| **I13-E2 MRI Visualizations** (heatmap/triangle/timeline polish) | MRI-01 core suffices for validation; richer viz is enhancement. |
| **I14 Collaboration depth** (replies/mentions beyond comments) | Core comment + CRR loop proves collaboration; depth is incremental. |
| **Future-scope caps** PF-05, AE-06, CONF-07 | Explicitly out of Alpha. |
| **Connector-style ingestion** | Not in Release 1; intake is upload/describe/template/guided only. |

---

## Part 5 — Architectural Bottlenecks

### 5.1 Single points of failure
- **I1 Project Foundation** — every object and recompute roots here. A flaw in the object model or event bus halts all downstream work.
- **I5 CAF Engine** — produces the findings consumed by Confidence, Issues, Recs, Overlays, and MRI. Highest blast radius of any feature initiative.
- **I8-E1 Event-Driven Recompute (AE-03)** — the backbone of the improvement loop; a correctness bug silently corrupts Confidence/CAF/Issues/Recs/MRI everywhere.

### 5.2 High-risk initiatives
- **I5** (undefined scoring; on both critical branches) — highest risk.
- **I7** (six-way convergence under a 60-second ceiling) — integration risk.
- **I8** (recompute correctness + idempotency under rapid edits) — cascade risk.
- **I15** (depends on two undefined subsystems — notifications and external-reviewer identity).

### 5.3 Undefined architectural areas / Master Spec gaps affecting delivery
Mapped to the requested focus items (all trace to Matrix §22):

- **CAF scoring** (gap 1) — no algorithm for computing Clarity/Alignment/Feasibility to 0–100. Blocks I5; cascades to I6/I9/I10/I13. *Must resolve before Phase 1 detailed design.*
- **Confidence calculations** (gaps 1–2) — no formula aggregating CAF→Confidence; band thresholds provisional. Blocks I6 acceptance.
- **Event-driven Deep Pass** (implied, §6/§12) — trigger semantics, debounce/cooldown, idempotency, and "no-change→no-reanalysis" detection are conceptual only. Blocks I8 correctness + I20 efficiency.
- **Notifications** (gap 5) — **no Notification object or surface** in §18/§15, yet CRR, comments, and mentions all require alerting. Blocks complete I14 and I15. *Needs an owner decision before Phase 4.*
- **External reviewer model** (gap 6) — no Stakeholder/Reviewer identity distinct from User; no external-auth path. Blocks I15 and the active-virality loop.
- **Security assumptions** (gap 10) — paid tiers, "Tier limits," and permission levels (gap 7) are referenced but unspecified; share-link expiry/revocation (gap 8) undefined. Constrains I16, I18, and I19 scope definition.

---

## Part 6 — Dependency Graph Visualization

### 6.1 Initiative Dependency Diagram (Hard edges; → = "required by")

```
                 ┌─────────────────────────── WS-A: Platform/Security ───────────────────────────┐
   I19-E1(Auth) ─┤                                                                                 │
                 │   I1 (Foundation: data model · persistence · event bus)                         │
                 │     │           │                          │                                    │
                 │     │           │                          └──> I17 (Telemetry) ──> I18 (Money) │
                 │     │           └──> I19-E2/E3 (Isolation · Audit)                  ^            │
                 └─────┼───────────────────────────────────────────────────────────  │ ───────────┘
                       v                                                              │
   WS-B: Intelligence  I2 ──> I3 ──┬──────────────> I4 (Workspace) ──> I9 (Overlay) ──┼──┐
   (critical path)                 │                   │                              │  │
                                   └──> I5 (CAF) ──┬──> I6 ────────────┐              │  │
                                                   ├──> I10 ──> I11 ───┤              │  │
                                                   └──(findings)       │              │  │
                                          I6,(I10,I11) ──> I13 (MRI) ──┤              │  │
                                   I3,I5,I6,I10,I11,I13 ─────────────> I7 (Fast Pass) │  │
                                   I1,I5,I6 ──> I8 (Deep Pass) ──> I20 (Perf)         │  │
   WS-D: Growth        I9,I11,I5,I8 ──> I15 (CRR) ──> I16 (Sharing) <── I13 ──────────┘  │
                       I4,I19,I8 ──> I14 (Collab) ··> I15                                 │
   WS-C: UX            I3,I4 ──> I12 (Chat) ··> I9 (Ask OSLO action) ─────────────────────┘
```
*(`··>` = Soft/incremental edge.)*

### 6.2 Critical Path Diagram

```
  ┌────┐   ┌────┐   ┌────┐   ┌═══════┐   ┌─────┐   ┌─────┐   ┌═══════┐
  │ I1 │──>│ I2 │──>│ I3 │──>║  I5   ║─┬>│ I10 │──>│ I11 │─┬>║  I7   ║   ← Fast Pass
  └────┘   └────┘   └────┘   ║ (CAF) ║ │ └─────┘   └─────┘ │ ║(conv.)║     (60s endpoint)
   root    evid.    synth.   ╚═══════╝ │                   │ ╚═══════╝
                              pivot    │ ┌────┐   ┌──────┐  │
                                       └>│ I6 │──>│ I13  │──┘
                                         └────┘   └──────┘
                                       (shorter branch — has slack)

  Longest hard chain = 7 initiatives.  Required set for Fast Pass = 9 (8 without I7).
  ═══ double-boxed = bottleneck (I5) and convergence (I7).
```

### 6.3 Parallel Workstream Diagram (swimlanes over §19 phases)

```
 Phase →     P0/Found.   P1            P2            P3        P4            P5        P6
 ─────────────────────────────────────────────────────────────────────────────────────────
 WS-A Plat/Sec  I1,I19 ███  I17 ███████████████████████████████████████████  I20 ████ (P2+)
 WS-B Intel             I2▶I3▶I5▶I6▶I10▶I11▶I13▶I7 ███  I8 ████
 WS-C UX                     I4 ████████  I9 ████      I12 ████   I13-viz ██
 WS-D Growth                                                      I14 ██ I15 ██ I16 ██ I18 ██
 ─────────────────────────────────────────────────────────────────────────────────────────
 ▶ = hard sequence on the critical path     ███ = continuous/cross-cutting build
```

---

## Part 7 — Delivery Recommendations

### 7.1 Staffing strategy (map teams to workstreams)
- **Foundation/Platform squad** → WS-A (I1, I19, I17, I20). Strongest backend/infra engineers; staff first and keep resident (highest fan-in).
- **Intelligence squad** → WS-B (I2–I13, I7, I8). AI/ML + backend; this squad owns the critical path and the CAF/Confidence risk — staff deepest here.
- **Workspace/UX squad** → WS-C (I4, I9, I12, MRI viz, sharing UI). Front-end + product design; starts once I3 lands.
- **Growth squad** → WS-D (I14, I15, I16, I18). Full-stack; starts Phase 4. Pair with Platform for the Notification subsystem decision before they begin.

### 7.2 AI-assisted development strategy
- Use AI codegen heavily on **boilerplate-dense, well-specified** initiatives: I1 (CRUD/schema), I17 (event instrumentation), I19 (auth/RBAC scaffolding), I16 (sharing/export).
- Keep **human-led, AI-assisted** on the **underspecified, high-blast-radius** initiatives: **I5 CAF scoring, I6 Confidence aggregation, I8 recompute semantics** — these need design decisions before code, and AI should draft options, not pick the model.
- Stand up a **replay/eval harness early** (deterministic fixtures for CAF/Confidence) so AI-generated scoring changes are regression-tested against the §20 metrics.
- Enforce **token/compute budgets** (I20-E2) from Phase 1 since Fast/Deep Pass are AI-heavy from day one.

### 7.3 Recommended implementation order
1. **M0 Foundation (P0):** I19-E1 auth ∥ I1 (data model, event bus, persistence) → I19-E2/E3, I17-E1.
2. **M1 Understanding / MVA (P1):** I2 → I3 → I4 ∥ I5 → I6 → I10 → I11 → I13 → **I7 Fast Pass**. *(MVA reachable at I13; M1 closes at I7.)*
3. **M2 Improvement loop (P2):** I9 Overlays, I8 Deep Pass, complete I10/I11, I20-E1 efficiency.
4. **M3 AI refinement (P3):** I12 OSLO Chat.
5. **M4 Collaboration (P4):** Notification decision → I14, I15 (with external-reviewer model resolved).
6. **M5 Virality (P5):** I16 Sharing.
7. **M6 Monetization (P6):** I18.
Cross-cutting throughout: I17 instrumentation, I19 hardening, I20 cost/perf.

### 7.4 Suggested milestone structure
| Milestone | Proves (§20 alignment) | Exit gate |
|---|---|---|
| M0 Foundation | System persists & recomputes; users authenticate | Object model live; auth + isolation; event bus emits |
| M1 Understanding (MVA→Fast Pass) | Synthesis, CAF, Confidence, MRI, Recs; Time-to-First-MRI <60s | §16 C1–C5, C7, C8, C10; §20 adoption metrics |
| M2 Improvement loop | Overlays, issues, recs, fixes, Deep Pass move confidence | §16 C3, C6; confidence improves on majority of projects |
| M3 AI refinement | Chat improves artifacts | §16 C9 |
| M4 Collaboration | Comments + CAF Review Requests with stakeholder participation | §16 C11, C14 |
| M5 Virality | MRI/artifact/review sharing | §16 C12; share + return metrics |
| M6 Monetization | Limits + upgrade prompts | §16 C13 |

---

## Validation Summary

| Metric | Value |
|---|---|
| **Total initiatives** | **20** |
| **Critical-path initiative count** | **8** (MVA core: I1, I2, I3, I5, I6, I10, I11, I13) — **9** including I7 Fast Pass |
| **Critical path length (longest hard chain)** | 7 initiatives |
| **Parallelizable initiative count** | **11** off the critical set: I4, I8, I9, I12, I14, I15, I16, I17, I18, I19, I20 |
| **Highest-risk initiative** | **I5 — CAF Engine** (undefined scoring algorithm; on both critical branches; widest blast radius) |
| **Most foundational initiative** | **I1 — Project Foundation** (object model, persistence, event bus; root of all dependencies) |
| **Most delayed-safe initiative** | **I18 — Monetization** (nothing depends on it; conversion proof can trail value proof) |
| Dependency defects corrected vs V2 | 3 (D-1 reverse edge, D-2 cycle, D-3 false interlock) + 1 clarification (I8→I7 Soft) |

---

*Dependency Graph complete. Dependencies re-derived from capability deps and the §18 object model; §19 sequence re-evaluated, not assumed. Critical path, parallel workstreams, Alpha paths, and architectural bottlenecks identified. Subject to governance review before adoption.*
