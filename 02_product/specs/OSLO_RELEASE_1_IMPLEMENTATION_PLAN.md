# OSLO Release 1 Implementation Plan

**Document:** OSLO_RELEASE_1_IMPLEMENTATION_PLAN.md
**Status:** Executable development plan derived from the validated Release 1 DAG
**Authoritative Sources:** `OSLO_RELEASE_1_MASTER_SPEC.md` · `OSLO_CAPABILITY_MATRIX_V2.md` · `OSLO_LINEAR_INITIATIVES_V2.md` · `OSLO_RELEASE_1_DEPENDENCY_GRAPH.md`
**Date:** 2026-05-31

> **Constraints honored.** No new initiatives, capabilities, or epics are created. Architecture and §19 initiative sequencing are taken as-is. Where capability dependencies would *allow* earlier work than §19 sequences (e.g., CAF Overlays are dependency-ready in M1 but sequenced to Phase 2), the §19 phase is followed and the slack is noted, not exploited.
>
> **Governance.** Non-canonical planning artifact (analysis & recommendation). Does not ratify or adopt. Canonical terminology preserved.

---

# Part 1 — Executive Summary

| Metric | Value |
|---|---|
| Total capabilities | **98** |
| Total initiatives | **20** |
| Total epics | **45** |
| Critical path length (longest hard chain) | **7 initiatives** |
| Critical path required set | **8** (MVA core) / **9** with Fast Pass (I7) |
| Parallelizable initiatives (off critical set) | **11** |
| Highest-risk initiative | **I5 — CAF Engine** (undefined scoring; on both critical branches) |
| Most foundational initiative | **I1 — Project Foundation** (object model, persistence, event bus) |
| Most delay-safe initiative | **I18 — Monetization** |

**Recommended Alpha completion sequence (by milestone):**
**M0 Foundation → M1 Understanding → M2 Improvement → M3 AI Assistance → M4 Collaboration → M5 Virality → M6 Monetization.**

The critical path is `I1 → I2 → I3 → I5 → {I10 → I11 | I6 → I13} → I7`, with **I5 (CAF)** the shared bottleneck and **I7 (Fast Pass)** the M1 convergence point. Everything not on this chain (I4, I8, I9, I12, I14, I15, I16, I17, I18, I19, I20) runs in parallel workstreams around it.

---

# Part 2 — Milestone Plan

> Each epic is assigned to the milestone in which it **completes** (its last dependency resolves). Cross-cutting epics (I17-E2 instrumentation, I19 hardening, I20 optimization) begin earlier and continue.

### M0 — Foundation
- **Objective:** Stand up the substrate everything writes to: identity, data model, persistence, event bus, security baseline, telemetry pipeline.
- **Initiatives:** I1 (partial), I19, I17 (partial).
- **Epics (7):** I1-E1, I1-E2, I1-E4 · I19-E1, I19-E2, I19-E3 · I17-E1.
- **Capabilities delivered (14):** PF-01, PF-05, PF-03, PLAT-06, PLAT-01, PLAT-02 · SEC-01, SEC-02, SEC-03, SEC-04, SEC-05, SEC-06, SEC-07 · TEL-01.
- **User-visible outcomes:** A user can be invited, authenticate (email/password, Google/MS SSO), and a project persists across sessions; no analysis yet.
- **Exit criteria:** Object model (19 objects) live; auth + workspace isolation enforced; event bus emits recompute events; telemetry sink receiving events.

### M1 — 60-Second Orientation (Understanding / MVA + Fast Analysis Pass)
- **Objective:** Deliver the core understanding loop — evidence → planning synthesis → CAF → Confidence → Issues → Recommendations → MRI — within the 60-second **Fast Analysis Pass**, producing the **60-Second Orientation**.
- **Deliver (orientation outputs):** Initial Confidence · Initial Findings · Initial Recommendations.
- **Note:** *60-Second Orientation is not the final analysis state. Deep Analysis continues after orientation and remains part of Release 1 (see M2 — Deep Analysis Completion).*
- **Initiatives:** I1 (overview), I2, I3, I4 (shell + intelligence layer), I5, I6 (core), I10, I11 (gen + actions), I13 (gen + viz), I7, I17 (instrumentation).
- **Epics (19):** I1-E3 · I2-E1, I2-E2 · I3-E1, I3-E2 · I4-E1, I4-E3 · I5-E1, I5-E2 · I6-E1 · I10-E1, I10-E2 · I11-E1, I11-E2 · I13-E1, I13-E2 · I7-E1, I7-E2 · I17-E2.
- **Capabilities delivered (46):** PF-02, PF-04 · EI-01, EI-02, EI-03, EI-04 · PS-01, PS-02, PS-03, PS-04 · AW-01, AW-02, AW-05, AW-06, AW-07 · CAF-01, CAF-02, CAF-03, CAF-04, CAF-05 · CONF-01, CONF-02, CONF-03 · ISS-01, ISS-02, ISS-03, ISS-04 · REC-01, REC-02, REC-03, REC-05 · MRI-01, MRI-02, MRI-03, MRI-04, MRI-05, MRI-06 · AE-01, AE-04, AE-05 · TEL-02, TEL-03, TEL-04, TEL-05, TEL-06, TEL-07.
- **User-visible outcomes:** Upload/describe a project → within 60s see Outcome Confidence, CAF, an MRI with heatmap + CAF triangle, Top Issues, and Recommendations; edit artifacts in the workspace.
- **Exit criteria:** §16 C1–C5, C7, C8, C10 met; **§20 Time-to-First-MRI < 60s**; project successfully synthesized end-to-end.

### M2 — Deep Analysis Completion (Improvement)
- **Objective:** Complete the **Deep Analysis Pass** and prove the improvement loop — overlays, suggested fixes, and event-driven Deep Analysis that move confidence. Deep Analysis is Active Release 1 and continues after the 60-Second Orientation.
- **Deliver (Deep Analysis outputs):** Confidence Recalculation · Expanded Findings · Expanded Recommendations · Expanded Understanding.
- **Initiatives:** I8, I9 (engine), I4 (assisted editing), I6 (evolution), I11 (fixes), I20 (efficiency).
- **Epics (7):** I8-E1, I8-E2 · I9-E1 · I4-E2 · I6-E2 · I11-E3 · I20-E1.
- **Capabilities delivered (13):** AE-02, AE-03, AE-06 · OVL-01, OVL-02 · AW-03, AW-04 · CONF-04, CONF-05, CONF-06, CONF-07 · REC-04 · PLAT-03.
- **User-visible outcomes:** In-artifact CAF overlays; apply a suggested fix and watch confidence update via Deep Pass; confidence trend/history appears.
- **Exit criteria:** §16 C3, C6 met; confidence improves on a majority of active projects; Deep Pass is event-driven with debounce/cooldown working.

### M3 — AI Assistance
- **Objective:** Prove AI-assisted refinement through project-aware OSLO Chat.
- **Initiatives:** I12, I20 (cost/perf).
- **Epics (3):** I12-E1, I12-E2 · I20-E2.
- **Capabilities delivered (6):** CHAT-01, CHAT-02, CHAT-03, CHAT-04 · PLAT-04, PLAT-05.
- **User-visible outcomes:** Launch chat from any issue/rec/artifact with inherited context; chat generates artifact edits that trigger Deep Pass.
- **Exit criteria:** §16 C9 met; AI cost/perf budgets within target on the AI-heavy passes.

### M4 — Collaboration
- **Objective:** Prove collaboration via comments and CAF Review Requests with stakeholder participation.
- **Initiatives:** I14, I15, I9 (actions complete), I13 (understanding dependencies).
- **Epics (5):** I14-E1 · I9-E2 · I15-E1, I15-E2 · I13-E3.
- **Capabilities delivered (10):** COLLAB-01, COLLAB-02, COLLAB-03 · OVL-03 · CRR-01, CRR-02, CRR-03, CRR-04, CRR-05 · MRI-07.
- **User-visible outcomes:** Comment/reply/mention; Share-For-Review from an overlay; stakeholder responses become evidence and update confidence; MRI shows "awaiting review" dependencies.
- **Exit criteria:** §16 C11, C14 met; CAF Review Requests show stakeholder participation. **Gated on resolving the Notification and external-reviewer gaps (see Part 10).**

### M5 — Virality
- **Objective:** Prove passive + active virality through sharing.
- **Initiatives:** I16.
- **Epics (2):** I16-E1, I16-E2.
- **Capabilities delivered (5):** SHARE-01, SHARE-03, SHARE-05 · SHARE-02, SHARE-04.
- **User-visible outcomes:** Share project/artifact with permission levels; public/private MRI links; PDF export.
- **Exit criteria:** §16 C12 met; share + stakeholder-return telemetry flowing.

### M6 — Monetization
- **Objective:** Prove conversion via tier limits and contextual upgrade prompts.
- **Initiatives:** I18.
- **Epics (2):** I18-E1, I18-E2.
- **Capabilities delivered (4):** MON-01, MON-03 · MON-02, MON-04.
- **User-visible outcomes:** Free-tier limits enforced; daily fix allowance resets; upgrade prompts appear at limits.
- **Exit criteria:** §16 C13 met; conversion telemetry flowing.

**Milestone capability totals:** M0 14 · M1 46 · M2 13 · M3 6 · M4 10 · M5 5 · M6 4 = **98** ✓ (no milestone invented beyond M0–M6; the DAG required none).

---

# Part 3 — Workstream Strategy

Four workstreams emerge from the DAG (the dependency graph's WS-A…D):

### WS-A — Platform & Security
- **Initiatives:** I1, I19, I17, I20.
- **Epics:** I1-E1/E2/E3/E4 · I19-E1/E2/E3 · I17-E1/E2 · I20-E1/E2.
- **Dependencies:** I1 internal only; I19-E2/E3 ← I1; I17 ← I1-E4; I20 ← I8/I7.
- **Parallelization:** Runs day 1 and continuously; the rest of the program depends on it but it depends on almost nothing.
- **Risk level:** **High** (highest fan-in; a flaw here halts everything).

### WS-B — Intelligence (AI core = the critical path)
- **Initiatives:** I2, I3, I5, I6, I10, I11, I13, I7, I8.
- **Epics:** all epics of those initiatives (21 epics).
- **Dependencies:** strictly sequential internally (I2→I3→I5→{I6,I10→I11}→I13→I7; I8 shares engines).
- **Parallelization:** Parallel to A/C/D, but internally a chain — the program's pacing constraint.
- **Risk level:** **Critical** (contains I5, I6, I7, I8 — the undefined-algorithm and convergence risks).

### WS-C — Workspace & UX
- **Initiatives:** I4, I9, I12, plus MRI viz (I13-E2) and MRI sharing (I16-E2).
- **Epics:** I4-E1/E2/E3 · I9-E1/E2 · I12-E1/E2 · (I13-E2, I16-E2 co-owned with B/D).
- **Dependencies:** I4 ← I3; I9 ← I4+I5; I12 ← I3+I4 (+ context from I5/I6/I10/I11).
- **Parallelization:** Starts once I3 lands; UX and intelligence proceed independently after artifacts exist.
- **Risk level:** **Medium** (UX-heavy; AI-codegen-friendly).

### WS-D — Collaboration & Growth
- **Initiatives:** I14, I15, I16, I18.
- **Epics:** I14-E1 · I15-E1/E2 · I16-E1/E2 · I18-E1/E2.
- **Dependencies:** I14 ← I4+I19+I8; I15 ← I9+I11+I5+I8; I16 ← I13+I19; I18 ← I1+I11+I17.
- **Parallelization:** Phase 4–6; I14 ∥ I15; I16 and I18 are terminal (nothing depends on them).
- **Risk level:** **Medium-High** (I15 blocked by Notification + external-reviewer gaps).

---

# Part 4 — Critical Path Execution Plan

Critical path: **I1 → I2 → I3 → I5 → I10 → I11 → I7** (+ the I6 → I13 branch converging at I7).

| Init | Why on critical path | What depends on it | Recommended implementation order | Validation approach | Major risks |
|---|---|---|---|---|---|
| **I1** | Root substrate; all objects/recompute | Everything | I1-E2 (data model) ∥ I19-E1 → I1-E4 → I1-E3 (after I6/I13) | Replay fixtures persist & reload; event-bus emits on write | Schema-evolution choices lock in early |
| **I2** | Only entry point for content | I3 | I2-E1 → I2-E2 | Round-trip: upload → claims extracted with provenance | Parser breadth; extraction quality |
| **I3** | Builds the model CAF scores | I4, I5, I12 | I3-E1 → I3-E2 | Synthesize from minimal/partial/advanced maturity inputs | Synthesis quality (founder acceptance) |
| **I5** | **Pivot**; produces findings all intelligence consumes | I6, I9, I10, I13, I15 | I5-E1 → I5-E2 | Deterministic CAF eval harness; regression on fixtures | **Undefined scoring algorithm** (top risk) |
| **I6** | Headline signal; needed by Fast Pass + MRI | I7, I13 | I6-E1 (M1); I6-E2 (M2, after Deep Pass) | Confidence explainable to drivers; band stability | **Undefined CAF→Confidence formula** |
| **I10** | Improvement-loop entry; feeds recs | I11 | I10-E1 → I10-E2 | Issues map to CAF; severity correctness | Severity taxonomy stability |
| **I11** | Longest hard branch to Fast Pass | I7, I13, I15, I18 | I11-E1 → I11-E2 (M1); I11-E3 (M2) | Rec states what/why/dimension/impact; lifecycle verified | Rec quality; fix safety |
| **I13** | Signature artifact; in Fast Pass output | I7, I16 | I13-E1 → I13-E2 (M1); I13-E3 (M4) | MRI renders with confidence+CAF+heatmap; states correct | Synthesis + viz complexity |
| **I7** | 60-second integration endpoint | I8 (soft), I20 | I7-E1 → I7-E2 (after all above produce initial output) | **§20 Time-to-First-MRI < 60s** integration test | Six-way convergence under 60s ceiling; "supported sizes" undefined |

**If any slips:** a slip in I1/I2/I3/I5 stalls the entire program; I10→I11 is the longest branch so its slip directly extends the path; I6→I13 has slack against the I11 branch. I7 slipping costs the 60-second promise but not the underlying understanding.

---

# Part 5 — Minimum Viable Alpha (NOT the founder-approved Alpha)

Smallest implementation that demonstrates **Planning Synthesis · CAF · Confidence · Issues · Recommendations** (per this brief — note it omits MRI and Fast Pass).

**Required initiatives (8 + auth):** I19 (E1 only), I1, I2, I3, I4 (viewing), I5, I6 (core), I10, I11.

**Required epics (15):**
- I19-E1 (auth)
- I1-E2, I1-E4 (data model, persistence/event bus)
- I2-E1, I2-E2 (ingestion, claim extraction)
- I3-E1, I3-E2 (synthesis, artifact generation)
- I4-E1, I4-E3 (workspace shell to view artifacts; persistent issues/recs panel)
- I5-E1, I5-E2 (CAF scoring + taxonomy)
- I6-E1 (confidence core)
- I10-E1, I10-E2 (issues + linkage)
- I11-E1, I11-E2 (recommendation generation + actions)

**Required capabilities (31):** SEC-01, SEC-02 · PF-03, PLAT-06, PLAT-01, PLAT-02 · EI-01, EI-02, EI-03, EI-04 · PS-01, PS-02, PS-03, PS-04 · AW-01, AW-02, AW-05, AW-06, AW-07 · CAF-01, CAF-02, CAF-03, CAF-04, CAF-05 · CONF-01, CONF-02, CONF-03 · ISS-01, ISS-02, ISS-03, ISS-04 · REC-01, REC-02, REC-03, REC-05.

**Deferred from MVA (safe to delay):** Fast Pass (I7), MRI (I13), CAF Overlays (I9), Deep Pass (I8), OSLO Chat (I12), Collaboration (I14), CAF Review Requests (I15), Sharing (I16), Monetization (I18), Performance (I20); and within-initiative: I1-E1/E3 (invitation/overview), I4-E2 (assisted editing), I6-E2 (evolution), I11-E3 (suggested fixes), I19-E2/E3 (hardening can trail the demo).

This MVA proves the core hypothesis (incomplete evidence → useful, scored understanding with actionable recommendations) without the 60-second orchestration or the shareable MRI.

---

# Part 6 — Recommended Alpha (Founder-Approved)

The full Release 1 per Master Spec §13 In-Scope and §20 validation goals.

**Required initiatives:** all **20** (I1–I20).
**Required epics:** all **45**.
**Required capabilities:** all **98** (Alpha-scoped; the 3 Future caps PF-05/AE-06/CONF-07 are mapped but carry no Alpha commitment).

**Rationale.** §20's Alpha learning objectives require the complete chain: understanding generation (M1) → improvement loop (M2) → AI-assisted refinement (M3) → collaboration (M4) → virality (M5) → monetization signals (M6). Dropping any milestone removes a §20 success dimension (Adoption, Understanding Creation/Improvement, Collaboration, Virality, Monetization). The MVA proves the engine; the Recommended Alpha proves the *business* — the 60-second Fast Pass (the core UX promise, §5), the shareable MRI (passive virality), and CAF Review Requests (active virality) are what the founder approved as the validation surface.

---

# Part 7 — Team Allocation Strategy

Team: **Founder** (Product / UX / Acceptance), **Hamza**, **Kashif**, **AI-assisted development**. With two engineers against 20 initiatives, AI is a force multiplier and the founder owns acceptance, not implementation.

| Init | Primary | Secondary | Founder involvement | AI leverage |
|---|---|---|---|---|
| I1 Project Foundation | Kashif | Hamza | Low | **High** — CRUD, schema, migrations |
| I2 Evidence Ingestion | Hamza | Kashif | Medium (intake UX) | **High** — format parsers |
| I3 Planning Synthesis | Hamza | Founder | **High** (synthesis quality acceptance) | Medium — human-led prompts |
| I4 Artifact Workspace | Kashif | Founder | **High** (UX) | **High** — UI generation |
| I5 CAF Engine | Hamza | Founder | **High** (scoring decisions) | Low — human-led |
| I6 Confidence Engine | Hamza | Kashif | **High** (formula) | Low — human-led |
| I7 Fast Pass | Hamza | Kashif | **High** (60s acceptance) | Medium — orchestration |
| I8 Deep Pass | Hamza | Kashif | Medium | Medium — human-led on recompute |
| I9 CAF Overlay | Kashif | Hamza | Medium (UX) | **High** — UI |
| I10 Issue Engine | Hamza | Kashif | Medium | Medium |
| I11 Recommendation Engine | Hamza | Kashif | Medium | Medium |
| I12 OSLO Chat | Hamza | Kashif | Medium | **High** — chat UI + prompts |
| I13 MRI | Kashif (viz) | Hamza (synthesis) | **High** (signature UX) | **High** — visualizations |
| I14 Collaboration | Kashif | Hamza | Low | **High** — comments/mentions |
| I15 CAF Review Requests | Kashif | Hamza | Medium (workflow) | Medium — blocked by gaps |
| I16 Sharing | Kashif | Hamza | Low | **High** — sharing/export |
| I17 Telemetry | Kashif | Hamza | Low | **High** — instrumentation |
| I18 Monetization | Kashif | Hamza | Medium | Medium |
| I19 Security & Compliance | Kashif | Hamza | Low | **High** — auth/RBAC scaffolding |
| I20 Performance/Compute | Hamza | Kashif | Low | Medium |

**Pattern:** Hamza anchors WS-B (Intelligence/AI core), Kashif anchors WS-A + WS-C + WS-D (Platform, UX, Growth), Founder is deepest on I3/I5/I6/I7/I13 (where judgment and acceptance matter most), AI carries boilerplate, UI, and tests everywhere.

---

# Part 8 — AI Development Strategy

**Best epics for AI-assisted implementation:** I1-E2/E4 (schema/persistence), I17-E1/E2 (instrumentation), I19-E1/E2 (auth/RBAC/secrets scaffolding), I16-E1/E2 (sharing/export), I2-E1 (parsers), I14-E1 (comments).

**Best epics for AI-generated tests:** I5-E1/E2, I6-E1/E2, I8-E1/E2 (build a deterministic **replay/eval harness** with fixtures first), I10-E1, I11-E1 (regression on issue/rec generation), I7-E1 (60-second integration test).

**Best epics for AI-generated UI:** I4-E1 (workspace + artifact views), I9-E1 (overlay panel), I13-E2 (MRI heatmap/triangle/timeline), I12-E1 (chat UI), I16-E2 (share/export UI), PF-04 overview (I1-E3).

**High-risk AI areas — human-led, AI-assisted only (design decisions before code):**
- **Planning Synthesis (I3)** — synthesis quality is a founder-acceptance judgment; AI drafts, humans validate.
- **CAF scoring (I5)** — no defined algorithm; AI proposes scoring options, humans choose; never let AI silently pick the model.
- **Confidence calculations (I6)** — aggregation formula undefined; same discipline as I5.
- **Deep Pass + event-driven recompute (I8 / AE-03)** — idempotency, debounce, "no-change→no-reanalysis" detection; correctness bugs cascade silently. Pair with the replay harness.

**Cross-cutting AI discipline:** stand up the replay/eval harness in M0–M1 so every AI-generated scoring/recompute change is regression-tested against §20 metrics; enforce token/compute budgets (I20-E2) from M1 since Fast/Deep Pass are AI-heavy immediately.

---

# Part 9 — Validation Strategy

| Milestone | Demo criteria | Acceptance criteria | Founder review checkpoint | Go / No-Go |
|---|---|---|---|---|
| M0 Foundation | Invite → auth → project persists across restart | Object model live; auth (pw + Google/MS SSO); workspace isolation | Review object model + auth before M1 build | **Go** if data persists, event bus emits, isolation holds |
| M1 Understanding | Upload → <60s → Confidence/CAF/MRI/Issues/Recs | §16 C1–C5, C7, C8, C10; §20 TtFM < 60s | Founder accepts synthesis quality + 60s experience | **Go** if MVA works end-to-end **and** Fast Pass < 60s |
| M2 Improvement | Overlay → fix → confidence moves via Deep Pass | §16 C3, C6; confidence improves on majority | Founder reviews improvement loop credibility | **Go** if Deep Pass event-driven + efficiency budgets met |
| M3 AI Assistance | Chat improves an artifact with inherited context | §16 C9 | Founder reviews chat usefulness + cost | **Go** if chat edits trigger Deep Pass within budget |
| M4 Collaboration | Share-For-Review → stakeholder responds → confidence updates | §16 C11, C14 | Founder signs off on Notification + reviewer model | **No-Go until** notification + external-reviewer gaps resolved |
| M5 Virality | Share MRI (public/private link) + PDF export | §16 C12 | Founder reviews shareable surfaces | **Go** if links + permissions + export work |
| M6 Monetization | Hit limit → upgrade prompt; daily fix resets | §16 C13 | Founder reviews conversion flow | **Go** if limits enforced + prompts fire |

---

# Part 10 — Release Risks (ranked by severity)

| # | Risk | Category | Severity | Mitigation |
|---|---|---|---|---|
| 1 | **CAF scoring algorithm undefined** (Matrix §22 g1) — blocks I5, the critical-path pivot | Architectural / AI | **Critical** | Resolve scoring design before M1 detailed build; replay harness |
| 2 | **Fast Pass 60s with full outputs; "supported sizes" undefined** (g13) | Product / Architectural | **Critical** | Integration-test against §20 metric early; define size bounds |
| 3 | **Event-driven Deep Pass correctness/idempotency** (AE-03) | Architectural / AI | **High** | Pair I8 with I20-E1 efficiency + replay harness from M2 |
| 4 | **CAF→Confidence formula undefined** (g1–2) | Architectural | **High** | Decide aggregation + thresholds before I6 acceptance |
| 5 | **No Notification object/surface** (g5) — blocks M4 (I14, I15) | Dependency / Product | **High** | Owner decision before M4; do not start I15 build until resolved |
| 6 | **External reviewer identity undefined** (g6) — blocks CRR virality | Dependency / Product | **High** | Decide reviewer auth model before M4 |
| 7 | **2 engineers vs 20 initiatives** | Delivery / Staffing | **High** | Lean hard on AI for boilerplate/UI/tests; defer M5/M6 if needed |
| 8 | **AI cost from Phase-1 AI-heavy passes** | AI | **Medium** | Token/compute budgets (I20-E2) from M1 |
| 9 | **Confidence misread as probability** (g15) | UX | **Medium** | Explicit UI framing; never present as % success |
| 10 | **AC coverage gaps (46 caps lack AC)** in I17/I18/I19/I20 | Validation | **Medium** | Author ACs before those milestones close |

---

# Part 11 — Delivery Recommendation

### Recommended implementation order (topological, by wave)
- **Wave M0:** I19-E1 ∥ I1-E2 → I1-E4 → I19-E2, I19-E3, I17-E1.
- **Wave M1:** I2-E1 → I2-E2 → I3-E1 → I3-E2 → (I4-E1 ∥ I5-E1) → I5-E2 → I6-E1 → I10-E1 → I10-E2 → I11-E1 → I11-E2 → I4-E3 → I13-E1 → I13-E2 → I1-E3 → I7-E1 → I7-E2; I17-E2 instrumentation alongside.
- **Wave M2:** I8-E1 → I8-E2 → I9-E1 → I4-E2 → I6-E2 → I11-E3 → I20-E1.
- **Wave M3:** I12-E1 → I12-E2 → I20-E2.
- **Wave M4:** I14-E1 → I9-E2 → I15-E1 → I15-E2 → I13-E3.
- **Wave M5:** I16-E1 → I16-E2.
- **Wave M6:** I18-E1 → I18-E2.

### Recommended staffing strategy
Two squads with AI leverage: **Hamza → Intelligence (WS-B critical path)**; **Kashif → Platform/UX/Growth (WS-A/C/D)**; **Founder → acceptance + the judgment-heavy intelligence epics (I3/I5/I6/I7/I13)**; **AI → boilerplate, UI, and test generation throughout.** Resolve the Notification and external-reviewer gaps before WS-D's M4 work begins so the growth squad isn't blocked.

### Recommended milestone cadence
Sequential gating with parallel build inside each wave. M0 and M1 are the investment (M1 is the longest — it contains the full critical path and 19 epics); M2–M3 are tighter; M4 is gated on the two product-gap decisions; M5 and M6 are small and terminal. Treat each milestone's Go/No-Go (Part 9) as a hard gate before opening the next wave.

### Alpha launch-readiness criteria (per §20 graduation)
- 50+ active users; **80% reach MRI**; Time-to-First-MRI < 60s.
- Confidence improves on a majority of active projects.
- Meaningful CAF interaction across active projects.
- CAF Review Requests show stakeholder participation.
- Users report improved understanding of project reality.

---

# Validation Requirements

| Check | Required | Represented | Status |
|---|---|---|---|
| Total initiatives | 20 | I1–I20 across M0–M6 + workstreams | ✅ 20/20 |
| Total epics | 45 | M0:7 + M1:19 + M2:7 + M3:3 + M4:5 + M5:2 + M6:2 | ✅ 45/45 |
| Total capabilities | 98 | M0:14 + M1:46 + M2:13 + M3:6 + M4:10 + M5:5 + M6:4 | ✅ 98/98 |
| Critical path initiatives | 8–9 | I1, I2, I3, I5, I6, I10, I11, I13 (+I7) | ✅ represented |

**Capability coverage validation:** every one of the 98 capabilities appears in exactly one milestone via its epic; milestone totals sum to 98. Every initiative (I1–I20) and every epic (45) is placed. No new initiative, epic, or capability was introduced.

---

*Implementation Plan complete. Derived strictly from the validated Release 1 DAG; architecture and §19 sequencing unchanged. Subject to governance review before adoption.*
