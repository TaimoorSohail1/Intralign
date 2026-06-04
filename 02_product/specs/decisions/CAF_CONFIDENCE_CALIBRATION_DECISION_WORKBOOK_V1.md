# CAF / Confidence Calibration Decision Workbook v1

**Type:** Founder Decision Workbook (identification only)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Reviewed (not modified):** CAF Assessment Model · CAF Scoring Model · Reliability Model · Confidence Model · `PLANNING_INTELLIGENCE_SPECIFICATION_V1.md` · `RELEASE_1_ANALYSIS_ENGINE_SPECIFICATION_V1.md` · `RELEASE_1_TESTING_STRATEGY_V1.md` · `RELEASE_1_PERFORMANCE_AND_NFR_SPECIFICATION_V1.md`

> **Purpose & limits.** This workbook **surfaces** the calibration decisions the founder/owner must make before Release 1 implementation can be finalized. It **defines no formula, scoring, weight, or threshold**; it **modifies no model**; it **introduces no architecture or doctrine**. It only **identifies** open decisions and their dependencies. **All founder decisions remain unresolved here** — the capture template (Section 9) is intentionally blank. Cross-references to `FAST_DEEP_WORKFLOW_PACK/OPEN_DECISIONS.md` (OD-n) are provided where an item already appears there.

---

## Section 1 — Decision Inventory

Every remaining owner decision across CAF, Reliability, Confidence, Determinism, Severity, Fast Analysis, Deep Analysis. (Detail per category in Sections 2–7; this is the master index.)

| ID | Description | Why required | Downstream dependencies | Cross-ref |
|---|---|---|---|---|
| **CAL-CAF-1** | Equal vs differentiated treatment of Clarity / Alignment / Feasibility | The Confidence summary consumes three dimensions; whether they are treated alike or distinctly is unresolved (no weighting may be introduced — the question is *whether differentiation is permitted at all*) | Confidence synthesis, CAF UX, tests | OD-6 |
| **CAL-CAF-2** | CAF assessed-level scale (number of levels, labels, qualitative↔representation) | The engine must express each dimension's level; the scale is undefined | Data Model `*_index`, CAF UX, tests | OD-6 |
| **CAL-CAF-3** | Finding-type → dimension-impact assignment basis (qualitative) | Which finding types move which dimensions, and how strongly (qualitatively), is not fixed | Finding/CAF mechanics, tests | — |
| **CAL-REL-1** | Reliability scale definition (levels/labels) | Reliability qualifies CAF; its expressible scale is undefined (model uses High/Moderate/Low qualitatively) | Confidence, Reliability UX, tests | OD-8 |
| **CAL-REL-2** | How Coverage / Evidence Availability / Assessability determine a reliability level (qualitative policy, **not** arithmetic) | The model fixes the three inputs but not how they combine; a non-formula determination policy is needed | Engine reliability stage, tests | OD-8 |
| **CAL-REL-3** | Reliability display / visibility behavior in UI | How (and how prominently) reliability is shown is unresolved | UI, UX guidelines | — |
| **CAL-REL-4** | Strength/manner by which reliability qualifies confidence (qualitative, no weights) | Reliability "qualifies" CAF; the qualification policy is undefined | Confidence synthesis, UI | OD-7/OD-8 |
| **CAL-CONF-1** | CAF + Reliability → Outcome Confidence synthesis method (formula-free) | The summarization method is the central unresolved confidence decision | Engine confidence stage, UI, tests | OD-7 |
| **CAL-CONF-2** | Confidence band set / mapping to canonical confidence states | Data Model lists 5 bands; the qualitative-state mapping is unresolved | UI, Data Model, tests | OD-7 |
| **CAL-CONF-3** | What conditions should reduce confidence | Behavioral policy undefined (identification only) | Engine, UX, tests | OD-7 |
| **CAL-CONF-4** | What conditions should increase confidence | Behavioral policy undefined | Engine, UX, tests | OD-7 |
| **CAL-CONF-5** | Confidence reaction to ambiguity / assumptions / conflicts | How each finding class influences the summary is unresolved | Engine, tests | OD-7 |
| **CAL-SEV-1** | Severity assignment basis (critical / moderate / warning) | Severity is emitted per finding but its basis is undefined | Finding mechanics, UI "top findings", tests | OD-14 |
| **CAL-SEV-2** | Severity escalation/change basis across runs/supersession | Whether/how severity changes over time is unresolved | Engine, UI | OD-14 |
| **CAL-SEV-3** | Severity visibility / surfacing rules | What surfaces as "top" and how severity displays | UI, UX | OD-14 |
| **CAL-DET-1** | Bounded-equivalence tolerance over governable outputs | The determinism contract requires a tolerance; undefined | Determinism tests, Engine | OD-12 |
| **CAL-DET-2** | Replayability expectations (what must reconstruct exactly) | Replay scope/guarantees need owner confirmation | Replay tests, Engine | — |
| **CAL-DET-3** | Acceptable-variation definition (semantic-equivalence vs bit-exact) | The nature of permitted variation is unresolved | Tests, Engine | OD-12 |
| **CAL-DET-4** | Model-version change policy vs determinism guarantees | How config/model changes re-baseline determinism | Tests, ops, Engine | OD-1/OD-12 |
| **CAL-DET-5** | Regression-testing expectations for determinism | What constitutes a determinism regression / tolerance for tests | Testing Strategy | — |
| **CAL-FD-1** | Fast-pass scope (claim bound, evaluated set) | Fast scope drives the 60s budget and orientation completeness | Engine §9, NFR, tests, UI | OD-3 |
| **CAL-FD-2** | Deep-pass scope (full claim/relational set) | Deep scope drives latency/cost | Engine §10, NFR, tests | OD-4 |
| **CAL-FD-3** | Expansion boundaries (how far Deep expands) | Undefined expansion limits | Engine, NFR | OD-19 |
| **CAL-FD-4** | Deferral rules (what Fast defers to Deep — horizon boundary) | The fast/deep boundary is unresolved | Engine, tests, UX | OD-19 |
| **CAL-FD-5** | Recalculation rules / triggers (debounce/coalescing) | Recompute cadence undefined | Engine, Event flow, NFR | OD-10 |

---

## Section 2 — Confidence Decisions *(identify only — do not answer)*

- **CONF-Q1** What does Outcome Confidence represent at the value level (beyond the model's "summarized signal")? *(CAL-CONF-1)*
- **CONF-Q2** What conditions should **reduce** confidence? *(CAL-CONF-3)*
- **CONF-Q3** What conditions should **increase** confidence? *(CAL-CONF-4)*
- **CONF-Q4** How should confidence react to **ambiguity**? *(CAL-CONF-5)*
- **CONF-Q5** How should confidence react to **assumptions**? *(CAL-CONF-5)*
- **CONF-Q6** How should confidence react to **conflicts**? *(CAL-CONF-5)*
- **CONF-Q7** How does **reliability** qualify the surfaced confidence (manner/strength, no weights)? *(CAL-REL-4)*
- **CONF-Q8** What is the confidence **band set** and its mapping to canonical confidence states? *(CAL-CONF-2)*
- **CONF-Q9** How is the CAF + Reliability → Confidence **synthesis** performed without a formula? *(CAL-CONF-1)*

---

## Section 3 — Reliability Decisions *(identify only)*

- **REL-Q1** Reliability **scale** definition — levels, labels, qualitative↔representation. *(CAL-REL-1)*
- **REL-Q2** How do **Coverage / Evidence Availability / Assessability** combine into a level (qualitative policy, not arithmetic)? *(CAL-REL-2)*
- **REL-Q3** Reliability **display behavior** — where and how shown. *(CAL-REL-3)*
- **REL-Q4** Reliability **influence on confidence** — the qualification policy. *(CAL-REL-4)*
- **REL-Q5** Reliability **visibility in UI** — prominence, per-dimension vs overall. *(CAL-REL-3)*

---

## Section 4 — CAF Decisions *(identify only)*

- **CAF-Q1** Relative importance of **Clarity** — equal or differentiated? *(CAL-CAF-1)*
- **CAF-Q2** Relative importance of **Alignment** — equal or differentiated? *(CAL-CAF-1)*
- **CAF-Q3** Relative importance of **Feasibility** — equal or differentiated? *(CAL-CAF-1)*
- **CAF-Q4** **Equal treatment vs differentiated treatment** of the three dimensions (is differentiation even permitted, given independence)? *(CAL-CAF-1)*
- **CAF-Q5** CAF assessed-level **scale**. *(CAL-CAF-2)*
- **CAF-Q6** Finding-type → **dimension-impact** assignment basis. *(CAL-CAF-3)*

---

## Section 5 — Severity Decisions *(identify only)*

- **SEV-Q1** **Assignment basis** — what makes a finding Critical / Moderate / Warning? *(CAL-SEV-1)*
- **SEV-Q2** **Escalation basis** — does severity change across runs or on supersession, and why? *(CAL-SEV-2)*
- **SEV-Q3** **Visibility rules** — how severity surfaces; what counts as "top." *(CAL-SEV-3)*

---

## Section 6 — Determinism Decisions *(identify only)*

- **DET-Q1** **Replayability** — what must reconstruct exactly from the event log? *(CAL-DET-2)*
- **DET-Q2** **Equivalent outputs** — which outputs must match (governable set) for "same input → same output"? *(CAL-DET-1)*
- **DET-Q3** **Acceptable variation** — semantic-equivalence vs bit-exact; the tolerance band. *(CAL-DET-1/3)*
- **DET-Q4** **Model-version changes** — how a config/model change interacts with determinism guarantees and re-baselining. *(CAL-DET-4)*
- **DET-Q5** **Regression-testing expectations** — what is a determinism regression; test tolerance. *(CAL-DET-5)*

---

## Section 7 — Fast vs Deep Analysis Decisions *(identify only)*

- **FD-Q1** **Fast-pass scope** — claim bound and evaluated set. *(CAL-FD-1)*
- **FD-Q2** **Deep-pass scope** — full claim/relational extent. *(CAL-FD-2)*
- **FD-Q3** **Expansion boundaries** — how far Deep expands. *(CAL-FD-3)*
- **FD-Q4** **Deferral rules** — what Fast defers to Deep (horizon boundary). *(CAL-FD-4)*
- **FD-Q5** **Recalculation rules** — triggers, debounce/coalescing cadence. *(CAL-FD-5)*

---

## Section 8 — Dependency Analysis

| Decision | Impacted Specification | Impacted Test | Impacted UI | Impacted API |
|---|---|---|---|---|
| CAL-CAF-1 | Confidence Model (consumer), Engine §13 | CAF/Confidence behavior, determinism | Confidence + CAF drivers display | — (read schema only) |
| CAL-CAF-2 | Data Model `*_index`, Engine §13 | CAF state assertions | CAF level rendering | CAFState read fields |
| CAL-CAF-3 | Finding/CAF mechanics (Engine §11) | finding→dimension tests | finding/dimension display | — |
| CAL-REL-1 | Reliability/Confidence/Data Model | reliability assertions | reliability indicator | ConfidenceState/CAFState reliability fields |
| CAL-REL-2 | Engine reliability stage | reliability behavior | — | — |
| CAL-REL-3/5 | UI Spec §7/§11 | UX tests | reliability visibility | — |
| CAL-REL-4 | Confidence Model, Engine §13 | confidence-reliability tests | confidence qualifier | — |
| CAL-CONF-1 | Confidence Model, Engine §13 | confidence determinism + behavior | confidence band display | ConfidenceState |
| CAL-CONF-2 | Data Model band enum, UI Spec | band tests | confidence band/badge | confidence_band field |
| CAL-CONF-3/4/5 | Engine §13/§14 | confidence-reaction tests | confidence trend | — |
| CAL-SEV-1/2/3 | Finding Model, Engine §11 | severity tests | severity chips / "top findings" | Finding.severity filter |
| CAL-DET-1/3 | Engine §15, Testing §6 | determinism suite (pass/fail) | — | — |
| CAL-DET-2 | Engine §16, Testing §7 | replay suite | — | — |
| CAL-DET-4 | Engine §15, ops | regression baseline | — | — |
| CAL-DET-5 | Testing §6/§15 | regression gates | — | — |
| CAL-FD-1 | Engine §9, NFR §3 | 60s + Fast-output tests | orientation completeness | analysis endpoints |
| CAL-FD-2 | Engine §10, NFR §4 | Deep-output tests | deep results | analysis endpoints |
| CAL-FD-3/4 | Engine §9/§10, Planning Intel §16/§17 | expansion/deferral tests | fast vs deep UX | — |
| CAL-FD-5 | Event §15, Engine §14, NFR | recompute tests | refresh behavior | — |

---

## Section 9 — Founder Decision Matrix *(blank capture template)*

| Decision | Selected Option | Reasoning | Follow-Up Required |
|---|---|---|---|
| CAL-CAF-1 | | | |
| CAL-CAF-2 | | | |
| CAL-CAF-3 | | | |
| CAL-REL-1 | | | |
| CAL-REL-2 | | | |
| CAL-REL-3 | | | |
| CAL-REL-4 | | | |
| CAL-CONF-1 | | | |
| CAL-CONF-2 | | | |
| CAL-CONF-3 | | | |
| CAL-CONF-4 | | | |
| CAL-CONF-5 | | | |
| CAL-SEV-1 | | | |
| CAL-SEV-2 | | | |
| CAL-SEV-3 | | | |
| CAL-DET-1 | | | |
| CAL-DET-2 | | | |
| CAL-DET-3 | | | |
| CAL-DET-4 | | | |
| CAL-DET-5 | | | |
| CAL-FD-1 | | | |
| CAL-FD-2 | | | |
| CAL-FD-3 | | | |
| CAL-FD-4 | | | |
| CAL-FD-5 | | | |

*(Intentionally blank — founder decisions remain unresolved.)*

---

## Section 10 — Recommended Resolution Order *(sequence only — no answers)*

Derived **purely from dependency depth** (Section 8), not from any preferred answer:

**Tier 1 — Resolve first (block the analysis engine's core outputs):**
- CAL-CONF-1 (synthesis method) — most-depended-upon; gates every confidence value.
- CAL-REL-1 / CAL-REL-2 (reliability scale + determination) — confidence consumes reliability.
- CAL-CAF-1 / CAL-CAF-2 (treatment + scale) — confidence consumes CAF.
- CAL-DET-1 / CAL-DET-3 (equivalence + tolerance) — the determinism suite cannot define pass/fail without these.

**Tier 2 — Resolve next (block tests, behavior, and Fast/Deep tuning):**
- CAL-CONF-2/3/4/5 (bands + reaction policy).
- CAL-CAF-3 (finding→dimension), CAL-SEV-1 (severity basis).
- CAL-FD-1 / CAL-FD-4 (Fast scope + deferral boundary).
- CAL-DET-2 / CAL-DET-4 / CAL-DET-5 (replay scope, model-version policy, regression expectations).

**Tier 3 — Can wait (UX/visibility and Deep-tuning refinements):**
- CAL-REL-3/4/5 (reliability display/qualification).
- CAL-SEV-2/3 (escalation/visibility).
- CAL-FD-2 / CAL-FD-3 / CAL-FD-5 (Deep scope, expansion boundary, recompute cadence).

**Implementation-blocking subset:** Tier 1 in full. **Testing-blocking subset:** CAL-DET-1/3, CAL-CONF-1, CAL-SEV-1. **UI-blocking subset:** CAL-CONF-2, CAL-REL-3, CAL-CAF-2.

*(Sequence only; no specific answers recommended.)*

---

## Validation

- No formulas introduced — ✅
- No scoring defined — ✅
- No weights defined — ✅
- No thresholds defined — ✅
- No models modified — ✅
- No architecture modified — ✅
- No new doctrine introduced — ✅
- Founder decisions remain unresolved — ✅ (Section 9 blank)

**CAF / Confidence Calibration Decision Workbook complete.**
