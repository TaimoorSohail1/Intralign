# DL-105 — Commission E1–E3 analysis cost optimization into R1 — prompt caching, scoped recompute (Evaluate always full + equivalence gate), evidence coalescing; instrument, do not gate

- **Date:** 2026-07-12 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

## Decision

**Commission E1–E3 (analysis cost optimization) into Release 1**, per **DL-103 §3**, subject to the binding constraints below. Realization artifact: `RELEASE_1_ANALYSIS_COST_OPTIMIZATION_SPECIFICATION_V1` (`30_engineering/analysis_engine`). **E1–E3 change what is *paid for* and what is *re-read* — never what is *concluded*.**

**1. E1 — Prompt caching / KV-cache reuse. BUILD NOW (R1).**
The plan corpus is stable between runs; only the delta changes. Cache the stable portion of the model input; pay full price only for what moved. **Rented providers:** provider prompt-caching. **Local runtime (DL-069 — primary):** **KV-cache reuse**, behind the same `/services/llm_provider` seam. **Seam-only** — the three call sites (Perceive extraction, Infer synthesis/generation, Infer findings) are **unchanged** (DL-069 condition 1). **Epistemic impact: none** — caching changes what is *paid for*, never what is *computed*. Determinism (ADR-0004) unaffected.

**2. E2 — Incremental / scoped recompute. BUILD IN R1, CONDITIONAL on the two constraints below. Without them it MUST NOT ship.**

**2a. THE HAZARD (stated first, because the constraint only makes sense against it).**
A scoped recompute that updates only **part** of the read produces an **internally inconsistent assessment** — some CAF dimensions reflecting the new plan, others the old. **That is worse than honest staleness, because it is silently mixed.** OSLO's entire claim is a **coherent** read; a half-updated read is a **quiet lie**.

**2b. BINDING CONSTRAINT — scope the LLM stages; ALWAYS run Evaluate in FULL.**
**DL-069 condition 1 (ratified): *"Evaluate remains rule-arithmetic (no LLM)."*** The expensive stages are therefore **Perceive** (extraction) and **Infer** (synthesis/findings); **Evaluate is cheap and deterministic**.
- **Perceive and Infer MAY be scoped** to the changed artifact and its dependency closure.
- **Evaluate MUST ALWAYS run in FULL**, over the complete claim set.
The assessment is thus **always derived from the whole plan** — never partially stale — while the expensive re-reading is scoped to what actually moved. **The cheap stage is the one that guarantees coherence.** **A scoped Evaluate is a build-breaking defect.**

**2c. BINDING CONSTRAINT — EQUIVALENCE (P1 QA gate).**
> **For any project state, a SCOPED Deep run MUST produce an assessment IDENTICAL to what a FULL Deep run would produce for that same state.**
Directly testable against recorded fixtures (ADR-0004). **On failure the run MUST fall back to a full re-derivation.** Equivalence is a **P1 gate, not a performance target.**

**2d. Dependency closure — widen, never narrow.** A scoped run recomputes the changed artifact, every claim whose provenance touches it, and every artifact those claims bind to (transitively). **If the closure is uncertain, WIDEN it.** A closure that is too wide is merely expensive; **a closure that is too narrow is wrong, and wrong is unaffordable.**

**3. E3 — Evidence coalescing. BUILD NOW (R1). This one has genuine Alpha urgency.**
**CR-2** (DL-102, load-bearing) says evidence-seeking is **never metered**; **CRR-04** says every reviewer response triggers an Extended Analysis. So five reviewers answering = five runs, silently consuming the inviter's analysis budget. **CR-2 then holds in letter and dies in practice** — users learn that **asking for evidence costs them their own read**, and stop asking, killing the loop DL-102 exists to protect.
- **Reviewer responses arriving within the coalescing window SHALL settle into ONE analysis run** (extending the existing coalescer — §4c *"Deep concurrency 1 + coalescing on"*). This is also the **correct UX**: the read should not churn as each reviewer replies; it should **settle once they have answered**.
- **Urgency:** **C14 — "CAF Review Requests show stakeholder participation" — is an Alpha exit criterion.** Without E3, CRR is validated **against a broken incentive**.

**4. CR-2 vs the binding budget governor — record · defer · disclose.**
When a reviewer's evidence arrives **after** the budget has gated: **record the evidence, defer the run, disclose honestly.** The attestation is **appended immediately** (append-only; **CR-2 honoured — evidence is NEVER refused**); the **run defers**, with an honest line (*"…recorded. Your read will update when your monthly analysis budget resets, or on upgrade."*). **Evidence is never lost. Cost is bounded. The product stays honest about what it has not yet done.**

**5. Telemetry — instrument; do NOT gate. This is what unblocks every number DL-103 suspended.**
§4c is explicit: *"Numbers are estimate-based starting defaults; **the contracted cost telemetry replaces them with measured medians**."* **Cost-per-analysis cannot be re-derived from a specification — only from measured usage.** Emit on the contracted `AI Spend Recorded` event: **tokens per Deep run** (pre/post E1, pre/post E2) and **cache-hit rate** → the real cost-per-analysis · **analyses per user per month** (distribution) → the Free/Basic budgets · **fixes per session** (distribution) → the **UP-APPLY threshold** (DL-103 §7d: *above activation, below power use*) · **chat messages/day** → validates uncapping (D126) · **CRR responses per project and the runs they trigger** → the **Free CRR cost ceiling** · **coalescing ratio** → **OD-10** · **actual $/active user/month** → the ~$3 Free posture (DL-048).

**At audience rungs R1 (<5 users) and R2 (10–20) budgets SHALL NOT be enforced.** The cost is ~$15–60/month, and **enforcement would corrupt the very signal Alpha exists to buy.** **Instrument; do not gate.** Enforcement begins where it matters: **Beta (50+ users)**.

**6. Terminology collision — register it (DL-053).**
**"R1" is overloaded.** **DL-076 (ratified)** defines **R1–R5 as *audience-scale* rungs** (*"R1 = owner + <5 users; R2 = 10–20; 50+ = the Beta gate"*), while **every specification uses `RELEASE_1_*` to mean *Release 1, the product*** — the same token, two meanings, often in the same sentence. **Add a Disambiguation Register entry** (e.g. *Release 1* vs *Audience Rung R1*) with the doc-integrity regression guard per DL-053.

## Rationale

**Deep Pass is specified as a full re-derivation on every run** — a grep of `30_engineering/analysis_engine/` for *prompt caching · incremental · differential · scoped recompute · cache* returns **zero hits**. AE-03 ratifies *"no change → no reanalysis"*, but **nothing ratifies *scoped* reanalysis**. That single omission inflates cost-per-analysis by roughly **6×** (§4c basis: **$0.260 → $0.040**; **12 → ~74 analyses/month at the $3 Free ceiling**) — **with no model change and no quality trade.**

DL-103 suspended §4c's numeric basis until cost-per-analysis is re-derived **from the real engine**. **E1–E3 plus the §5 telemetry are therefore a prerequisite for setting ANY tier number.** They are the highest-leverage unbuilt work in the product.

## Conditions

1. **E2 MUST NOT ship without §2b (Evaluate always full) and §2c (equivalence).** Absent either, E2 is an **epistemic hazard** and is deferred to R2.
2. **No change to what OSLO concludes.** E1–E3 alter what is **paid for** and what is **re-read** — never the assessment. Determinism (ADR-0004) preserved.
3. **CR-2 is untouched and remains load-bearing.** Evidence is **never refused**; §4 defers the *run*, never the *evidence*.
4. **Anti-Assumption — owner-open, not set here:** **OD-10** (the coalescing window; settle/idle-based recommended — the Deep Pass spec already lists **`manual`** as a qualifying trigger, so *"Update now"* exists and is **free on every tier**, DL-103 §7d-bis) · the **CRR coalescing window** (may differ from OD-10 — reviewers answer over **hours**, not seconds) · **every tier number** (re-derived from §5 telemetry, never from a spec).

## Supersedes / Amends

- **Realizes DL-103 §3** (E1–E3 commissioned).
- **Extends AE-03** — scoped/incremental recompute (**bounded by §2b/§2c**) and evidence coalescing.
- **Amends** `30_engineering/analysis_engine/` — new spec `RELEASE_1_ANALYSIS_COST_OPTIMIZATION_SPECIFICATION_V1`; **OD-10** remains open.
- **Amends** the QA gate — **AC-2 (equivalence)**, **AC-3 (Evaluate always full)** and **AC-5 (evidence never refused)** are **P1**.
- **Reaffirms** DL-069 (seam-only; Evaluate is rule-arithmetic) · DL-102 (**CR-2**) · DL-048 (cost governance; telemetry replaces defaults with measured medians) · ADR-0004 (determinism).
- **Adds a DL-053 Disambiguation Register entry** for the **"R1"** collision.
