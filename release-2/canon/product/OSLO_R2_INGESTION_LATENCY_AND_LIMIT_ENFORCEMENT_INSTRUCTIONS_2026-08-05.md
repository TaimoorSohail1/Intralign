# OSLO R2 — Ingestion Latency & Freemium Ingest-Limit Enforcement — Build Instructions

**Date:** 2026-08-05 · **Trigger:** R1 build test — a ~10-page planning document took **>6 minutes** in the analysis stage.
**Scope:** (1) compress ingestion + analysis latency in the R2 build; (2) enforce the freemium ingest limits so a first-time user never enters a >60s analysis.
**Grounding (reconciled against canon 2026-08-05):** `canonical-truth.md` (DL-046, D033/D034, D036), `RELEASE_1_BUILD_SPEC.md` (two-pass, ~60s target), `slice-02-intake-fastpass-orientation` (D031/D036 latency criteria), `slice-10-tiering-limits/tier-definitions-census.md` (§4b/§4c token caps + word envelope), `E4_PERCEIVE_PARALLELIZATION_MEMO`, `RELEASE_1_ANALYSIS_COST_OPTIMIZATION_SPECIFICATION_V1` + `DL-103/104` (cost basis), `DL-200–205` (DL-201 outcome unit, DL-202 commitment gate), `DR-7` (Basic $29/mo).

> **Number-status legend:** ✅ **RATIFIED** · 🟡 **ILLUSTRATIVE / owner-TBD** · ⏳ **PENDING RE-DERIVATION (was ratified; DL-103 reopened the basis)**. A developer must treat 🟡/⏳ values as config placeholders, not hard facts.

---

## 0. The decisive finding — the two-pass latency contract already exists; the 6 minutes means it isn't being honored

The pipeline is specified as **two passes**, and the first-read latency is a *design target*, currently owner-TBD as a hard NFR:

> **DL-046 (canonical-truth, High):** "Flow — Intake → **Fast Pass <60s** → 60-second orientation lands on MRI → **Deep Pass auto-runs (non-blocking) and supersedes**."
> **slice-02 D036 (success-criteria):** the arrival notice shows a **measured** elapsed time framed *"under the 60-second target"* — **"no hardcoded canonical number"**; prototype pacing ≈30s (D031).
> **slice-02 product-data (Owner-TBD):** "**Real Time-to-First-MRI NFR (D036)** — prototype shows ≈30s illustratively." → 🟡 the 60s is the *intent*; the enforceable NFR is unset.
> **canonical-truth:** first-run = **Fast-Pass-only** (note: *anonymous* first-run is a **GA-phase** concept; Alpha/Beta users are authenticated from activation — but the Fast-Pass-first rule still governs their first analysis).

So the first read must return from the **Fast Pass on the critical path**, and the **Deep Pass must run off it** and supersede via the recompute/supersession engine (`OSLO_BACKEND_CAPABILITIES` #1). A 6-minute first read is one root cause, in likelihood order:

1. **The read is blocked on the Deep Pass** (or a single full analysis) instead of returning from the Fast Pass. **← most likely; fixing this alone likely resolves the report.**
2. **The per-run token cap isn't enforced**, so the Fast Pass scales with document size instead of degrading to fit (the ratified degrade behavior below is not wired).
3. **The Perceive/extraction stage is sequential** rather than the E4 per-artifact fan-out.
4. **Cold start / heavy model** on the Fast-Pass path.

**Recommendation 0 — ✅ RATIFIED 2026-08-06:** **Time-to-First-MRI (Fast Pass) = ≤60s P95 / ~45s target, hard acceptance gate** (D036), measured against the Free envelope + the 150k Fast-Pass cap. It gates **time-to-first-read only, never completeness** — an over-envelope doc passes by returning a `Provisional` partial read within 60s and deferring depth to the Deep Pass.

---

## Part 1 — Compressing ingestion + analysis latency

Ordered by impact. L1–L2 are the fix; L3–L5 are the named engine economics (E1/E2/E4); L6–L7 are margin.

### L1 — Only the Fast Pass on the critical path; Deep Pass non-blocking (highest impact)
- The intake→read request returns as soon as the **Fast Pass** completes; it must not `await` the Deep Pass.
- On completion, land the read, then **enqueue the Deep Pass** on the event-driven recompute queue (debounce-coalesce-cooldown, `AE-03`/`PLAT-03`); it **supersedes** the read via append-only supersession (findings weaken/unchanged/superseded/close) while the user is already working.
- **Acceptance:** 10-page doc → first read **<60s** (P95); Deep Pass lands later as a supersession event; first-run triggers **no** Deep Pass on the critical path.

### L1a — Fast-Pass output contract (what the first read must contain)
The confirm card and the integrity read render **immediately after the Fast Pass** — they cannot wait for the Deep Pass — so the Fast Pass must emit all of the following, and this is where the old "synthesis + CAF" description is stale:
- **The 7 synthesized plan artifacts** + structured-table extraction (D033).
- **The outcome layer** — the **primary outcome, confirm-ready** (the confirm card binds to it), **detection of any secondary outcomes**, and the **primary-selection rationale** (the `_OC_IMPACT_NOTE` equivalent). Secondaries are captured here but **held** (deferred-disclosure UX contract, owner 2026-08-05) — surfaced post-engagement, not on the confirm card. This is a *data-must-exist-at-Fast-Pass* requirement; the holding is presentation, not a data gap. Ties to backend-caps #16 (multi-outcome NLU).
- **The full three-pillar Outcome Integrity read, not CAF alone.** The R1-era "synthesis + CAF" line (canonical-truth §67 / D033) is **superseded by the R2 three-pillar model** (DL-193/196/203): Integrity = **min(Viability, Grounding, Adaptability)**.
  - **Viability = CAF** — the heavy per-dimension LLM assessment (Clarity·Alignment·Feasibility).
  - **Grounding** — *derived* from the provenance the synthesis assigns; at first read everything is inferred, so it's the initial all-ungrounded state, a computation over the extracted items, **not a separate model pass**. (Expect Grounding to be the `min()` limiter at t0 — the honest first read.)
  - **Adaptability v1** — checkpoint-coverage read over the already-extracted plan structure (the simple v1 ratified 2026-08-06), **not** the full DL-195 model.
- **Latency note:** only Viability/CAF is a heavy pass; Grounding and Adaptability v1 are light derivations over artifacts already in hand — adding the two new pillars does **not** triple Fast-Pass cost, so it stays inside the ≤60s gate. The Deep Pass refines all three (deeper feasibility, checkpoint analysis); the Fast Pass must produce their initial values.

### L2 — Enforce the per-run token cap with graceful degradation (already ratified — wire it)
The degrade contract and its numbers are **✅ RATIFIED** (tier-census §4c):

| Per-run token cap → degrade | Fast Pass | Deep Pass |
|---|---|---|
| **Free** | **150k** | **600k** |
| **Basic** | **300k** | **1M** |

- Over the cap → **"partial orientation / coalesce-defer"** (not a hang, not a reject). The Fast Pass consumes highest-signal content first (objectives, milestones, structured tables), analyzes to the 150k cap, and **defers the remainder to the non-blocking Deep Pass**; the read is honestly marked **"still updating"** (`Provisional`).
- Reference envelope for a Deep run: **450k in / 50k out ≈ 500k tokens** (cost spec §0).
- **Acceptance:** a document 3× the Free budget still returns a Fast-Pass read <60s (partial, `Provisional`); no run exceeds its cap.

### L3 — E1: prompt caching (biggest cost/latency multiplier after L1)
- Cost basis (🟡 illustrative arithmetic, DL-103/104): **TODAY $0.260/analysis → +E1 prompt caching $0.122 → +E2 incremental $0.068 → E1+E2 $0.040 (~6.4× more analyses per dollar)**. Assumptions: cached input at **10% of list**, **85% corpus cache-hit**, model `mini`.
- Cache the perceived corpus + prompts so re-analysis and the Deep Pass reuse cached input rather than re-sending full text.

### L4 — E2: incremental / scoped recompute
- **"scoped recompute reduces processed corpus 5×"** (cost spec Step 3). Later edits re-run only affected slices via the existing incremental-reanalysis path, never the whole document. Perceive **once** into a normalized representation (the **7 plan artifacts** + extracted tables + token map); Fast Pass and Deep Pass both read that cache — never re-extract per pass.

### L5 — E4: parallelize the Perceive stage (the memo's mechanism, verbatim)
- Perceive is "the most wall-clock of the cognitive steps." Replace sequential extraction with **per-artifact (and per-chunk) fan-out**: *"Sequential extraction makes wall-clock ≈ the **sum** of the artifacts; concurrent extraction makes it ≈ the **slowest single artifact**."* Corpus = ~7 independent artifacts.
- Run under a **bounded concurrency cap tuned to local GPU batch capacity (reuse the queue-depth governor / DL-069)** via continuous/dynamic batching — not unbounded.
- Determinism: order-stable merge, sort key **"artifact id → span offset → item type → normalized text hash"** (reuses the E2 equivalence gate). Parallelism must not change results.
- Keep **deterministic extraction separate from LLM synthesis**: PDF/DOCX/PPTX/XLSX/CSV parsing + structured-table extraction is non-model (D033; **no OCR in R1**, D034). Only synthesis-into-artifacts and CAF assessment call the model.

### L6 — Right-size the model per pass; stream the read
- **Fast Pass = fast/cheap tier** (`mini`-class) tuned to the 150k cap; **Deep Pass = heavier tier**. (Model routing is **never tier-keyed** — DL-103 forbids tiering judgment quality; this is a per-*pass* choice, not a per-*customer* one.) Emit the read progressively as artifacts/dimensions complete so perceived latency < actual.

### L7 — Eliminate cold starts
- Warm worker/model pool so first-run never pays spin-up inside the budget.

**Instrument every stage** (extract / synthesize / fast-pass / deep-pass) on the existing telemetry envelope so the next slow document is diagnosable in one look. Note the standing posture: R1 economics say **"instrument; do not gate"** on budgets until **Beta (50+ users)** — so in Alpha you *measure and degrade*, you don't hard-block on token budget.

---

## Part 2 — Enforcing the ingest limits as the <60s guarantee

**The <60s guard is primarily the per-run token cap + degrade (L2), not a paywall.** File/size limits are a coarse safety pre-filter; the true content metric is **words**, and it is ratified.

### E1 — Meter the real driver: the word envelope (✅ ratified value, ⏳ basis pending)
Per-tier ingest envelope (tier-census §4b, CHG-056, owner-confirmed 2026-06-05 — explicitly *"it **is** ratified — it is Basic's envelope"*; monthly-budget basis is ⏳ pending DL-103 re-derivation):

| Tier | Docs | Words |
|---|---|---|
| **Free** | ~20 | **~50k** |
| **Basic** | ~40 | ~100k |
| **Pro** | ~80 | ~200k |
| **Team** | ~150 | ~400k |

- After the fast, deterministic extraction, compute **extracted word/token count** and compare to the tier envelope + the Fast-Pass 150k cap. This is the precise trip point; MB/file-count are the coarse pre-filter.
- **Outside the envelope, projects are NOT rejected — they "degrade gracefully (partial orientation + coalesced Deep)"** (tier-census row 24). That is the ratified behavior and it is exactly what prevents the 6-minute hang.

### E2 — File-level pre-filter (✅ posture RATIFIED 2026-08-06: content-metered gate, loose file rails)
- Accepted types (✅): **PDF, DOCX, TXT, MD, PPTX, XLSX, CSV + paste**. Reject unsupported types fast.
- **Content is the real gate** (extracted words vs the Free ~50k envelope + the 150k Fast-Pass cap + degrade-to-fit). The file limits are **loose abuse rails only**, in per-tier config: **~10 MB/file · ~10 files · ~25 MB total**. **No page ceiling** (no OCR in R1 — pages aren't content). Validate type/size/count at the boundary and return the contract's **`422`/`429`** (the ratified simulated codes; **no `413` in canon** — use `422` or add `413` deliberately). Mirror with a client pre-check so the user sees it before upload.

### E3 — Three enforcement classes — keep them distinct
Conflating these is how you either hang a first-timer or break doctrine:

| Class | What it governs | Mechanism | In Alpha |
|---|---|---|---|
| **Latency safety** | per-run Fast-Pass token cap (150k Free) | **degrade-to-fit** (partial orientation, defer to Deep) | **Enforced** — this is the <60s guarantee |
| **Ingest pre-filter** | file type / size / count | reject at boundary (`422`/`429`) | Enforced (safety, not monetization) |
| **Freemium capacity wall** | extra outcomes / plans / bigger envelope / auto-import | **DL-202 commitment gate** (block → show capability + price → checkout → grant); Basic **$29/mo** (DR-7) | Gated per DL-202 — with an honest free fallback |
| **Token/monthly budgets** | 4M/mo Free governor, etc. | **instrument; do not gate** until Beta | Measured, not blocked |

### E4 — Decide in <2s; never hang (this is what "enforce" means for first-run)
1. **Fits the Free envelope + 150k cap** → run the Fast Pass.
2. **Over the Free envelope, within safety** → degrade-to-fit (analyze the highest-signal ~50k words now, defer the rest to the non-blocking Deep Pass) **and** surface the freemium capacity path (the intake-envelope value moment, #16 → DL-202 gate) as *optional*, never as a blocker to getting a read.
3. **Unsupported type / oversized file** → `422`/`429` in <1s, clear message, no analysis started.

### E5 — First-run is Fast-Pass-only by contract
- Assert the first-run path cannot trigger a Deep Pass (✅ ratified). This structurally removes Deep-Pass latency from the first-time user. (*Anonymous* first-run is GA-phase; in Alpha/Beta the user is authenticated but the Fast-Pass-first rule is identical.)

### E6 — Acceptance tests
- Free user, content over ~50k words → **Fast-Pass read <60s** (partial, `Provisional`) + optional upgrade path; **never** a reject or a >60s run.
- Free user, file >~10 MB or unsupported type → **`422`/`429` in <1s**; no analysis started.
- No input path starts an analysis destined to exceed 60s for a Free/first-run user (fuzz with oversized/dense docs).
- Envelope/cap/file values read from **entitlement config**, not literals (grep for hard-coded `10`, `50000`, `150000`).

---

## Status flags a developer must know
- **60s NFR** = **✅ RATIFIED 2026-08-06**: ≤60s P95 / ~45s target, **hard gate** (D036); gates time-to-first-read only, never completeness.
- **Ingest boundary** = **✅ RATIFIED 2026-08-06**: content-metered (extracted words vs Free ~50k envelope + 150k token cap + degrade); file rails ~10 MB/file · ~10 files · **~25 MB total** (config); **no page ceiling**.
- **Per-run token caps (Fast 150k / Deep 600k Free; 300k / 1M Basic) + degrade** = **✅ ratified** — wire as-is.
- **Word envelope (Free ~50k / ~20 docs …)** = **✅ ratified value**, ⏳ monthly-budget basis pending DL-103.
- **Cost math ($0.260→$0.040, 6.4×)** = 🟡 illustrative arithmetic (DL-103) — directional, not a target.
- **Enforcement posture:** latency-safety + pre-filter enforced in Alpha; freemium capacity via DL-202 gate; **token/monthly budgets instrument-only until Beta**.
- **DL-202 (commitment gate)** = **✅ confirmed final 2026-08-06** (was flagged pending).

---
*Prepared 2026-08-05 in response to the R1 6-minute analysis result; reconciled against the E4 memo, the DL-103 cost basis, slice-02 latency criteria, and the slice-10 tier census. Part 1 restores the two-pass latency contract and wires the ratified degrade caps; Part 2 makes oversized input unable to re-break it for a first-time user.*
