# OSLO Release 1 Scope Optimization Review

**Document:** OSLO_RELEASE_1_SCOPE_OPTIMIZATION_REVIEW.md
**Status:** Scope optimization analysis (recommendation only)
**Inputs:** `OSLO_RELEASE_1_MASTER_SPEC.md` · `OSLO_CAPABILITY_MATRIX_V2.md` · `OSLO_LINEAR_INITIATIVES_V2.md` · `OSLO_RELEASE_1_DEPENDENCY_GRAPH.md` · `OSLO_RELEASE_1_IMPLEMENTATION_PLAN.md`
**Date:** 2026-05-31

> **Governance.** Non-canonical planning artifact (analysis & recommendation). It does not ratify, adopt, or cut scope; the repository owner governs adoption. No initiatives, epics, or capabilities are invented; this review only re-groups and sequences the existing 20 / 45 / 98. No files were modified.
>
> **Deep Analysis Pass clarification (founder decision).** **Deep Analysis Pass (I8 / `AE-02`) is a required Active Release 1 capability.** Every "Wave 2" / "deferred" / "Lean Alpha excludes" reference to Deep Pass in this review denotes **implementation timing *inside* Release 1** (Deep Analysis sequences *after* the 60-Second Orientation), and does **not** imply removal from Release 1, Release 2 classification, or Future Architecture. The 60-Second Orientation is not the final analysis state; Deep Analysis continues after it and remains in Release 1.

---

## Verdict

**The current Release 1 scope is not bloated — but it is front-loaded.** All 20 initiatives / 45 epics / 98 capabilities are eventually required for the *full* §20 Alpha validation (Adoption, Understanding Creation, Understanding Improvement, Collaboration, Virality, Monetization). However, **only ~21 of 45 epics are needed for the first usable Alpha that proves the core hypothesis and user value.** The remaining ~24 epics validate *secondary* dimensions and can be **staged into later waves without damaging eventual validation** — the optimization is *sequencing*, not *cutting*.

Two items are genuinely low-value for an Alpha and can be deprioritized even long-term: **Monetization (I18)** — §20 explicitly optimizes for Learning Velocity, not Revenue — and **deep Performance/Compute optimization (I20)**, which is operationally necessary but tests no learning hypothesis.

---

## Q1 — Which epics are absolutely required for the first usable Alpha?

The core value loop: invited user → evidence → synthesized plan → CAF → Confidence → Issues → Recommendations → MRI (visible understanding). **21 epics:**

| Group | Epics | Why required |
|---|---|---|
| Access & substrate | I1-E1, I1-E2, I1-E3, I1-E4, I19-E1, I19-E2 | Invitation/auth, data model, persistence/event bus, workspace isolation — nothing runs without these |
| Evidence | I2-E1, I2-E2 | Only entry point for content; claim extraction |
| Synthesis | I3-E1, I3-E2 | Constructs the plan CAF scores — the core bet |
| Workspace (view) | I4-E1, I4-E3 | Surface to see artifacts + persistent issues/recs panel |
| CAF | I5-E1, I5-E2 | The pivot; findings everything consumes |
| Confidence | I6-E1 | Headline signal |
| Issues | I10-E1, I10-E2 | Improvement-loop entry; feeds recs |
| Recommendations | I11-E1, I11-E2 | Proves OSLO produces actionable guidance |
| MRI | I13-E1 | Makes understanding **visible** — the user-value surface |
| Orchestration | I7-E1 | Runs the analysis bundle (60-second acceptance **relaxed** for the lean release; the strict 60s tuning is I7-E2, deferred) |

Everything else (24 epics) is **not** required to demonstrate the six target capabilities.

## Q2 — Highest learning-value epics

Mapped to the §20 Alpha learning objectives (the questions Alpha must answer):

| Epic(s) | §20 question answered | Learning value |
|---|---|---|
| I3-E1/E2 Planning Synthesis | "Can OSLO build useful planning reality from incomplete evidence?" | **Highest — the central bet** |
| I5-E1/E2 CAF | "Do users trust CAF findings?" | Highest |
| I6-E1 Confidence | "Does confidence improve through usage?" / headline signal | Highest |
| I13-E1 MRI | "Does MRI effectively communicate understanding?" + passive virality | High |
| I11-E1/E2 Recommendations | "Do users act on recommendations?" | High |
| I8 + I9 + I11-E3 Improvement loop | "Does confidence improve through usage?" | High (Wave 2) |
| I15 CAF Review Requests | "Do CAF Review Requests improve understanding?" + active virality | High (Wave 3) |

## Q3 — Lowest learning-value epics

| Epic(s) | Why low learning value |
|---|---|
| I18-E1/E2 Monetization | §20 explicitly deprioritizes revenue in Alpha; tests no understanding hypothesis |
| I20-E1/E2 Performance/Compute | Engineering optimization; necessary operationally, but validates no product hypothesis |
| I19-E3 Audit & Compliance | Table-stakes hardening; no learning signal for a closed Alpha |
| I16 Sharing depth, I14-E1 collaboration depth (replies/mentions) | Incremental over the core comment/CRR loop |
| I7-E2 Understanding Progression UX, I13-E2 MRI viz polish | Enhancements over the core MRI; not hypothesis-testing |

## Q4 — Deferrable without damaging validation goals

Deferring these **sequences** validation across waves; it does not remove any §20 dimension:

| Deferred | Validation dimension | Restored in |
|---|---|---|
| I8, I9-E1, I11-E3, I4-E2, I6-E2 (improvement loop) | Understanding Improvement | Wave 2 |
| I12 OSLO Chat | AI-Assisted Refinement | Wave 2 |
| I14, I15, I9-E2, I13-E3 (collaboration + CRR) | Collaboration | Wave 3 |
| I16 Sharing | Virality | Wave 3 |
| I18 Monetization | Monetization | Wave 4 |
| I20 Performance, I19-E3 Audit | (operational, not a §20 dimension) | As needed |
| I17 Telemetry | Measurement of all dimensions | **Thread through from Wave 1** (see risk note) |

## Q5 — Epics with unresolved architecture dependencies (Master Spec gaps)

| Epic | Unresolved gap (Matrix §22) | Blocks the lean Alpha? |
|---|---|---|
| **I5-E1 CAF Core Scoring** | No CAF scoring algorithm (g1) | **Yes — must resolve before building** |
| **I6-E1 Confidence Core** | No CAF→Confidence formula; provisional thresholds (g1–2) | **Yes — must resolve before building** |
| I7-E1 Fast Pass | "Supported project sizes" for 60s undefined (g13) | Partially (60s relaxed in lean) |
| I8-E1 Deep Pass | Event-driven recompute / idempotency semantics undefined | No — **required Release 1 capability**; sequenced after the 60-Second Orientation within Release 1 (not removed, not Release 2, not Future) |
| I14-E1, I15-E1/E2 | **No Notification object** (g5); **external reviewer identity** undefined (g6) | No (deferred to Wave 3 — a reason to defer) |
| I2-E1 | Templates / guided-intake flow undefined (g3–4) | Minor (use upload/describe) |
| I16, I18 | Permission levels (g7), link expiry (g8), paid tiers (g10) undefined | No (deferred) |

**Key insight:** the two unresolved gaps that *do* sit in the lean scope (CAF scoring, Confidence formula) are on the critical path and unavoidable — you cannot lean your way around the pivot. The gap-blocked collaboration epics (I14/I15) are deferred anyway, so their unresolved gaps do **not** block the first Alpha — which is an argument *for* deferring them.

## Q6 — Smallest release proving Synthesis · CAF · Confidence · Issues · Recommendations · User value

The **Lean Alpha** of Q1: **21 epics, ~45 of 98 capabilities (~46%)**. It proves all six targets (user value via the visible MRI), with the 60-second constraint relaxed and the improvement loop, chat, collaboration, virality, and monetization deferred.

---

## Recommended Alpha Scope (Lean Alpha — Wave 1)

**21 epics · ~45 capabilities · ~47% of full Release 1 epic scope.**

| Initiative | Included epics | Capabilities |
|---|---|---|
| I1 Project Foundation | E1, E2, E3, E4 | PF-01, PF-03, PF-02, PF-04, PLAT-06, PLAT-01, PLAT-02 (PF-05 deferred) |
| I2 Evidence Ingestion | E1, E2 | EI-01, EI-02, EI-03, EI-04 |
| I3 Planning Synthesis | E1, E2 | PS-01, PS-02, PS-03, PS-04 |
| I4 Artifact Workspace | E1, E3 | AW-01, AW-02, AW-05, AW-06, AW-07 |
| I5 CAF Engine | E1, E2 | CAF-01, CAF-02, CAF-03, CAF-04, CAF-05 |
| I6 Confidence Engine | E1 | CONF-01, CONF-02, CONF-03 |
| I7 Fast Pass | E1 *(60s relaxed)* | AE-01 |
| I10 Issue Engine | E1, E2 | ISS-01, ISS-02, ISS-03, ISS-04 |
| I11 Recommendation Engine | E1, E2 | REC-01, REC-02, REC-03, REC-05 |
| I13 MRI | E1 | MRI-01, MRI-02, MRI-03 |
| I19 Security | E1, E2 | SEC-01, SEC-02, SEC-03, SEC-04, SEC-05 |

**Strongly recommended thin overlay (not strictly required, but needed to *measure* §20):** I17-E1 + the Understanding/Journey subset of I17-E2 (TEL-01, TEL-02, TEL-03) — so confidence deltas and MRI-reach are quantified, not just observed.

## Recommended Deferred Scope (Waves 2–4)

| Wave | Initiatives / epics | Proves | Precondition |
|---|---|---|---|
| **1.5** | I7-E2 + 60s tuning; full I17 | Adoption metric (Time-to-First-MRI < 60s) | Lean Alpha stable |
| **2** | I8-E1/E2, I9-E1, I11-E3, I4-E2, I6-E2, I12-E1/E2, I20-E1 | Understanding Improvement + AI Refinement | Resolve Deep Pass recompute semantics |
| **3** | I14-E1, I15-E1/E2, I9-E2, I13-E2/E3, I16-E1/E2, I20-E2 | Collaboration + Virality | **Resolve Notification + external-reviewer gaps first** |
| **4** | I18-E1/E2, I19-E3 | Monetization + compliance hardening | Value + virality proven |

---

## Capability Impact Analysis

| | Epics | Capabilities | % of 98 |
|---|---|---|---|
| Lean Alpha (Wave 1) | 21 | ~45 | ~46% |
| Deferred (Waves 1.5–4) | 24 | ~53 | ~54% |

**What deferral costs (and why it's safe):**
- **Improvement-loop capabilities** (Deep Pass, overlays, suggested fixes) — defers the "confidence improves through usage" proof to Wave 2. The core hypothesis (can OSLO *create* trustworthy understanding) is fully proven in Wave 1; improvement is a distinct, sequenced question.
- **Collaboration / CRR / Sharing** — defers virality + collaboration proof. These are gap-blocked anyway; deferring removes schedule risk rather than adding it.
- **Monetization** — zero impact on §20 learning goals.
- **60-second Fast Pass tuning** — Wave 1 proves value exists at a relaxed latency; Wave 1.5 proves it's fast enough to drive adoption.

**No deferral removes a §20 success dimension permanently — each is restored in a later wave.**

---

## Risk Analysis

**Risks of the Lean Alpha (and mitigations):**

| Risk | Severity | Mitigation |
|---|---|---|
| CAF scoring + Confidence formula still unresolved and *in* lean scope | **Critical** | Settle both designs + replay harness before building I5/I6 — unavoidable regardless of scope |
| Wave 1 doesn't prove "Understanding Improvement" | Medium | Sequenced to Wave 2; core creation hypothesis proven first |
| Relaxed 60s weakens adoption signal | Medium | Add I7-E2 + tuning in Wave 1.5 before any adoption push |
| Without telemetry, §20 metrics are qualitative | Medium | Adopt the thin I17 overlay in Wave 1 |

**Risks of NOT optimizing (shipping all 45 epics as one release):**

| Risk | Severity |
|---|---|
| 2 engineers × 45 epics → long time-to-first-learning; the central bet (synthesis quality, CAF trust) goes unvalidated for months | **High** |
| Building low-learning epics (Monetization, Performance, Audit) before proving the core hypothesis | **High** |
| Attempting M4 early runs into the unresolved Notification + external-reviewer gaps | **High** |
| Over-investing in the 60s Fast Pass and MRI polish before knowing whether users trust CAF at all | Medium |

**Net:** the optimization *reduces* aggregate risk by front-loading the learning and deferring the gap-blocked and low-learning work.

---

## Founder Recommendation

**Adopt a staged Alpha. Ship the 21-epic Lean Alpha (Wave 1) first; stage the remaining 24 epics across Waves 1.5–4.** Concretely:

1. **Before writing I5/I6 code, resolve the CAF-scoring and Confidence-aggregation designs** and stand up the deterministic replay/eval harness (M0–M1). This is the single highest-leverage action — it de-risks the pivot the whole product hangs on.
2. **Wave 1 = Lean Alpha (21 epics, ~46% of scope):** prove Synthesis + CAF + Confidence + Issues + Recommendations + user value (visible MRI), latency relaxed. Add the thin telemetry overlay so learning is measured.
3. **Wave 1.5:** add Fast Pass tuning + full telemetry → prove the 60-second adoption metric.
4. **Wave 2:** improvement loop + OSLO Chat → prove Understanding Improvement.
5. **Resolve the Notification + external-reviewer decisions before Wave 3**, then ship Collaboration + CAF Review Requests + Sharing → prove collaboration + virality.
6. **Treat Monetization (I18) and deep Performance (I20) as last** — they carry the lowest learning value and nothing depends on them.

**Bottom line:** the Release 1 scope is correct as the *eventual* validation surface, but shipping it as a single block is the wrong shape for a two-engineer team optimizing for learning velocity. Cutting the first release to ~21 epics gets you to the central learning ("can OSLO create trustworthy understanding from incomplete evidence?") roughly twice as fast, while preserving every §20 validation dimension across the later waves.

---

## Validation

- Scope universe referenced: **20 initiatives, 45 epics, 98 capabilities** (unchanged; nothing invented).
- Lean Alpha: **21 epics**, ~45 capabilities, drawn entirely from the existing set.
- Deferred: **24 epics**, ~53 capabilities, sequenced across Waves 1.5–4 (none removed from the program).
- Every §20 validation dimension remains represented across the wave plan.

*Scope Optimization Review complete. Recommends sequencing, not cutting. Subject to governance review before adoption.*
