# Proposal — Analysis Cost Basis & Tier Re-derivation
2026-07-11 · **Draft — for owner ratification via Framework 001 + `dl-land`.** AI authored as scribe; **non-ratifying.**
Resolves the order of operations: **(1) model basis → (2) engine economics → (3) cost re-derivation → (4) tier ladder.**

---

# Step 1 — The model basis

## 1a. A ratified contradiction: we are not renting, but we priced as if we were

| | |
|---|---|
| **DL-069** (Ratified, 2026-06-18) | Primary LLM = **internal Gemma on a local Llama runtime**. OpenAI/Anthropic **"demoted from primary… disabled-by-default fallback."** Rationale: *"removes external-provider token cost and data-egress."* |
| **§4c** (2026-06-05) + **DL-074** (2026-06-19) | The **entire** ladder — governors, prices, the ~$3/mo ceiling, the 4M budget — is derived from **rented frontier pricing** (GPT-4.1 $2/$8 · mini · nano · Sonnet, per 1M tokens). |

**DL-074 postdates DL-069 by one day and still assumes rental.** The cost basis was never re-derived after the model decision changed. **Every tier number in canon inherits an assumption canon itself abandoned.**

**This must be resolved first. Nothing downstream is trustworthy until it is.**

## 1b. The doctrinal bomb: **"Pro adds model quality" tiers the accuracy of truth**

The ratified design rule is *"Basic sells capacity; **Pro adds model quality** (faster/deeper full-quality routing)."* Read plainly, that means **Free and Basic users receive a less accurate read.**

In an ordinary SaaS that's fine. **In OSLO it is not**, and here is the exact mechanism:

> OSLO's core epistemic signal is **Reliability** — Coverage · Evidence availability · **Assessability**. It is a statement about **the plan and the evidence**. If judgment quality is tiered, **Reliability becomes partly a function of the plan the user is billed on.** The product would have to say, honestly, *"your read is less reliable because you are on Free"* — which converts a **truth signal into an upsell**, and poisons the one number the whole product rests on.

That is a **doctrinal violation**, not a pricing preference. It is the same family as D128 ("never meter the epistemic record") and D126 ("never meter who gets an answer"), and it is arguably worse: metering *access* to understanding is uncomfortable; metering the *accuracy* of understanding is self-refuting for a product whose entire claim is that it tells you the truth about your plan.

## 1c. Recommendation — **never tier the quality of judgment**

**One judgment-quality bar for every tier.** Tier **capacity, scope, speed, collaboration, and capability** — never the accuracy of the read.

**This is already where the owner's latest thinking points.** Owner, 2026-07-11: *"Pro also adds **execution and program support**; Team/Enterprise add **governance and portfolio support**."* That **replaces** model quality as Pro's differentiator — with something that is a real capability rather than a better brain. The doctrinal problem disappears on its own.

**Consequences:**
- **Model routing is chosen by *step*, not by *tier*** — cheap models for extraction, the best available for judgment, **for everyone**. (§4c's `extraction → nano · synthesis/eval → mini` split is correct; **making it tier-keyed is not**.)
- The model question becomes **purely economic**: use whatever clears the quality bar, as cheaply as possible, for all users. **Local (DL-069) if it clears the bar; rented if it does not; hybrid by step either way.**
- **This is an empirical question and cannot be settled from the armchair.** It needs a judgment-quality eval of the local model against the CAF/issue-detection task. **That eval is the blocking work item.**
- **Supersedes:** the design rule *"Pro adds model quality"* (BACKLOG_TIER_PROGRESSION, §4c T3 row, DL-074 §4).

---

# Step 2 — Engine economics (the missing capability)

**Grep of `30_engineering/analysis_engine/` for `prompt cach` · `incremental` · `differential` · `scoped recompute` · `cache` → ZERO hits.**

**Deep Pass is specified as a full re-derivation on every run.** A user fixes one line in one artifact and the engine re-reads the entire corpus and regenerates everything. That is why a run costs ~500k tokens. **AE-03 ratifies *"no change → no reanalysis"* — but nothing ratifies *scoped* reanalysis.**

Two capabilities are missing, **both orthogonal to model choice and neither costing any quality**:

**E1 — Prompt caching.** Both Anthropic and OpenAI discount cached input by ~90%. **The plan corpus is stable between runs**; only the delta changes. Cache the corpus; pay full price only for what moved. *(If DL-069's local runtime is used, the equivalent is KV-cache reuse across runs.)*

**E2 — Incremental / scoped recompute.** A fix to one artifact should re-analyze **that artifact and its dependency closure**, not all seven artifacts plus all evidence. This is what AE-03 *should* have said. It requires a dependency graph between artifacts, claims and CAF dimensions — which the analysis engine largely has already (claims, evidence links, issue→artifact bindings).

**E3 — Coalesce evidence (from the alignment review, A4).** Reviewer responses arriving in a window settle into **one** run — not one run per reviewer. Otherwise collaborators silently consume the user's analysis budget and **CR-2 dies in practice**: users learn that asking for evidence costs them their own read, and stop asking, killing the loop DL-102 exists to protect.

---

# Step 3 — Cost re-derivation (computed, §4c June-2026 price basis)

Assumptions stated: Deep run 450k in / 50k out · cached input at 10% of list · 85% corpus cache-hit · scoped recompute reduces processed corpus 5× (output 2.5×). Model: `mini` (the current cheap-class workhorse).

| Scenario | $/analysis | **Analyses / month at the $3 Free ceiling** | vs today |
|---|---|---|---|
| **A. TODAY (canon)** — rented, brute-force | **$0.260** | **12** | 1.0× |
| B. + prompt caching (E1) | $0.122 | 25 | 2.1× |
| C. + incremental recompute (E2) | $0.068 | 44 | 3.8× |
| **D. BOTH (E1 + E2)** | **$0.040** | **74** | **6.4×** |

**The same $3 buys 12 analyses today and ~74 with the engine fixed. No model change. No quality trade.**

**Under local inference (DL-069):** marginal cost per token → ~0. Cost stops being **per-user metering** and becomes **fixed GPU throughput**. The governor then bounds **capacity (queue depth)**, not dollars — a different constraint with different numbers, and one that does not require rationing the user's thinking.

**Conclusion: the Free tier's "8 analyses/month" is not an economic fact. It is an artifact of (a) a superseded rental basis and (b) an unoptimized engine.** Tuning the tier ladder on top of it would bake a ~6× penalty into the pricing permanently.

---

# Step 4 — The re-derived tier ladder

**Once the engine is fixed, analysis volume stops being a scarce good for an individual user.** A working month for a serious PM is perhaps 20–40 analyses; the engine can deliver ~74 at Free's existing cost ceiling. **So volume can no longer carry the tier story — and it shouldn't.**

**The ladder must be rebuilt on scope, collaboration and capability** — which is exactly where the owner's latest thinking already lands:

| Tier | What it actually sells | Metered on |
|---|---|---|
| **Free** | The full core read on **one** plan. Viral primitives (comments, sharing, **CRR**). | **1 project · small envelope.** Analyses generous — an abuse ceiling, not a product limit. |
| **Basic** | **Capacity/scope** — more plans, bigger plans. | Projects · envelope. |
| **Pro** | **Execution & program support** (+ speed/priority). *(Not "a better brain.")* | Capability. |
| **Team** | **Collaboration as the product** — governance. | **Per seat.** |
| **Enterprise** | **Portfolio** + org governance. | Contract. |

**And one honest limit, in the user's currency:** ***analyses per month***, never tokens. It should rarely bind. Daily caps become invisible rate-limits (burst-smoothers), **not product limits** — §4c already concedes they are *"burst ceiling, not the governor."*

**Falls out of this:**
- **UP-1 (fix cap) and UP-2 (chat cap) disappear.** They meter near-free actions and tax the two behaviours we most want (applying a fix = the activation moment; chat = comprehension, which D126 forbids metering).
- **UP-6 (the monthly analysis budget) becomes the single, primary, honest limit.**
- **Seats stay tight below Team** — a $12 Basic granting 10 seats cannibalizes a $99–149/**seat** tier. CHG-061 is unaffected: virality runs on **unlimited Viewers** and **free Reviewers**, neither of which consumes a seat.

---

# What this supersedes

**§4c** (cost basis + tier-keyed model routing + daily caps) · **DL-074 §4** ("Pro adds model quality") · **BACKLOG_TIER_PROGRESSION** design rule · **MON-02 / MON-03** (daily fix + chat caps) · **UP-1 / UP-2 / UP-5** (prompts on limits that never bind) · **DL-102 E** (Basic seat count).
**Preserved:** every epistemic invariant · CR-2 · D124 · D126 · D128 · DL-069 (reaffirmed, and finally reflected in the cost basis) · DL-074's hybrid-pricing structure and guardrails (visible meter, user-set spend cap, no bill shock).

# Blocking work items (owner)

1. **Judgment-quality eval of the local model (DL-069) against the CAF / issue-detection task.** This is the only way to settle whether local inference clears the bar. **Empirical — cannot be decided on paper.**
2. **Ratify: never tier judgment quality.** (Recommendation above; already implied by the owner's Pro = execution/program positioning.)
3. **Commission E1 + E2 + E3** (prompt caching · incremental recompute · evidence coalescing) as engine capabilities. **Highest-leverage unbuilt work in the product.**
4. **OD-10** — the coalescing window (settle/idle-based; the manual trigger already exists in the Deep Pass spec).
5. **Then** set the tier numbers — in **analyses/month**, from the real engine cost.

# Status

**Draft. Nothing herein is canon.** AI authored as scribe and **may not ratify, reject, supersede, or adopt** (`CLAUDE.md` Authority Constraint). Land via **`dl-land`** (DL-067) — the sole serializer.
