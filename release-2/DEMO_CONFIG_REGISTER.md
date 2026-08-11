# Demo-Config Register — production sourcing for every demo-tuned value

**Date:** 2026-08-09 · **Author:** AI (analysis/recommendation only — owner ratifies values) · Resolves gap **G1** of `DEMO_VS_PRODUCTION_AUDIT_2026-08-09.md`.

**Purpose:** The capability register (`OSLO_BACKEND_CAPABILITIES.md`) specifies simulated *behaviors*; this register specifies simulated *values*. Every hard-coded number/timing/threshold/flag in the prototypes appears here with a **classification** and a **production source**, so a demo value can never silently become the shipped value.

**Classification key**
- **SLA** — a real backend target the production system must actually meet (or the dependent copy must change).
- **OWNER-CONFIG** — a real, owner-tunable setting in production; must be config, not a hard-coded constant.
- **RATIFIED** — already an owner-ratified product number; confirm the prototype value matches canon.
- **DERIVED** — should be computed at runtime in production, not a fixed constant.
- **COSMETIC** — pure demo pacing/animation; carries no production meaning and **must never be read as an SLA**.

**Decision key:** ✅ ratified · ⚠️ owner-open (needs a decision) · 🎬 cosmetic (no decision needed, but must not leak).

---

## Product (`oslo-prototype-r2.html`)

| Constant | Demo value | Class | Production source / decision | Cap |
|---|---|---|---|---|
| `SV_NUDGE_TTL` | 45 s (wall-clock) | OWNER-CONFIG | ✅ **RATIFIED 2026-08-09:** survey retirement is **EVENT/SESSION-based, not a wall-clock timer** — retire when the user keeps working past it (≈ a couple more grounding acts without acting on it). The 45 s is a demo stand-in only; production number is a config placeholder. | #23/#18 |
| `SV_NUDGE_SNOOZE` | 120 s | OWNER-CONFIG | ✅ **RATIFIED:** re-offer in a **LATER SESSION**, not on a 120 s timer; cross-session persisted. Config placeholder. | #23/#18 |
| `SV_NUDGE_MAX` | 3 | OWNER-CONFIG | ✅ **RATIFIED:** cap ~3 lifetime offers per user; owner-config placeholder. | #23/#18 |
| `COACH_MAX` | 2 | OWNER-CONFIG | ✅ **RATIFIED:** per-card count (teach on N distinct cards then retire) — already event-based; make the `2` owner-config. | #23 |
| `_isEngaged` threshold | `confirmCount ≥ 3` (demo proxy) | DERIVED | ✅ **RATIFIED 2026-08-09 (owner):** "engaged / value-experienced" = a **milestone**, not a count — user has grounded **≥ half the load-bearing details (≥3 of 6) OR the integrity band rose ≥1 level** from start, whichever first (fraction owner-config, default ½). Must be a **durable, per-user, cross-session** signal. Prototype keeps the count proxy (demo); production uses the milestone. | #23/#15 |
| Freeze / activation gate | `confirmCount < 2` (2 calls unlock) | OWNER-CONFIG | ✅ **RATIFIED 2026-08-09 (owner):** default **2**, exposed as real **owner-config** (A/B-able once telemetry #15 exists), not a hardcoded `<2`. A "call" = **confirm / flag / route** — the three grounding acts; NOT proposals or checkpoints (those don't move the read). | #16/#15 |
| `_SURVEY_TRIGGER_AB` | `'immediate'` (vs `'delayed'`) | OWNER-CONFIG | ⚠️ Experiment assignment becomes a real A/B variant from telemetry. | #18/#15 |
| `REANALYSIS_DEBOUNCE` | 1500 ms | OWNER-CONFIG | ⚠️ Real debounce window for the batched reanalysis engine; #1 marks thresholds "deferred (§S)". | #1 |
| `REANALYSIS_MS` | 900 ms | COSMETIC→SLA | ⚠️ Demo "perceived pass" duration; production = real per-pass compute target (~1–2 s per #1/#7). | #1/#7 |
| `IMMEDIATE_THRESHOLD` | 5000 ms | OWNER-CONFIG | ⚠️ Window that classifies a resolve as "immediate" for banner logic; owner sets. | #1 |
| Intake envelope | 10 files / 10 MB (Free) — **upload rails** | RATIFIED (canon) | ✅ **RATIFIED 2026-08-09:** per canon (slice 04, DL-201/202, DR-7, audit F11) the Free limit is **content-metered ~50k words (entitlement config)**, NOT file count; `10 files / 10 MB` are upload guardrails/placeholders (ingest is content-metered — one over-envelope file trips it, many tiny ones don't, INV-7). Build = single-source **per-tier entitlement config** (fixes F11). Exact per-tier word numbers (Free ~50k · Basic bigger, **undefined**) = config placeholders, deferred to tune on real usage. | #16 |
| Basic price | `$29/mo` | RATIFIED | ✅ Owner-ratified (DR-7); keep out of user-facing copy until owner rules (neutral-copy rule, #16). | #16 |
| `roleType` default | `'pm'` (also `'owner'`/`'other'`) | DERIVED | ⚠️ Production = real identity/role from auth (#12), not a code default. | #12 |
| `firstRun` | `true` (resets on reload) | DERIVED | ✅ **RATIFIED (decision 3):** production = durable per-user **onboarded** flag (completed first-run once, ever → never replay first-run scaffolding), distinct from the **engaged** milestone above. | #23/#11 |
| DevNorth sample data | `ARTIFACTS`, `ISSUES`, `EXWBS`, `_PLANS`, `HISTORY`, `CLARIFY`, `CHK_PROPOSALS` | DERIVED | ⚠️ **All authored sample content.** Production = extracted from the user's real plan (#22) + generated (#5/#6/#8); never ship the sample. | #22/#11 |
| `$120K` / `$300K` in copy | — | (not config) | Plan **data** inside the DevNorth sample, not a system constant; goes away with the sample. | #22 |

## Onboarding arc (`onboarding-arc-prototype.html`)

| Constant | Demo value | Class | Production source / decision | Cap |
|---|---|---|---|---|
| `PASS_MS` | 60000 ms | **SLA** | ✅ **RATIFIED 2026-08-09 (owner):** the promise = *analysis completion* (not time-to-decision). Backend SLA = **typical/p50 target ≈45 s**; large uploads may exceed ("usually" covers this). Copy unchanged. | #21 |
| `GUIDED_MIN` | 47500 ms | COSMETIC | 🎬 Guided-arc floor. ✅ Per decision 1, the ~69 s guided run-time is **decoupled from the promise** (it's onboarding narration, not the analysis clock) — no longer an inconsistency. | — |
| `EV_DELAY` | outcome 8.4 s · plan-structure 13 s · inference 20 s · pillars 30 s | COSMETIC→SLA | ⚠️ **Fake fast-pass event timings.** Production emits each event when data is actually ready (#21). Demo values must NOT be read as SLAs. | #21 |
| `STEP` (ingest) | 1200 ms | COSMETIC | 🎬 Pacing of the 8 analysis-step labels; no production meaning. | — |
| `_slowGates` (×2.4) | demo toggle | COSMETIC | 🎬 Prototype dev-bar control ("slow · holds"); not shipped. | — |

---

## Load-bearing calibration (DL-209 · the L2 gate)

Per **DL-209**, "load-bearing" = magnitude of integrity-sensitivity ≥ a calibrated threshold. The prototype does **not** gate on a numeric threshold (the 6 DevNorth fixture items are all load-bearing by construction; each now declares `basisInference` and the resolution is **derived** by `_issueModel`/`_primaryMove`, retiring the hand-set `primaryMove`; an unmapped finding-type **escalates** rather than default-classifying — guard `findingTypeExhaustiveOrEscalates`). These are the **production L2 config** the build must expose — launch a **single global** value; the hierarchical-shrinkage segmentation ships **dormant**.

**Ratified launch policy (2026-08-09):** ship the **conservative over-surfacing bias** + the always-surfaced `LB_CRITICAL_FLOOR` + `LB_ASYMMETRIC_LOSS` as the *policy*; the absolute `LB_THRESHOLD` stays a placeholder resolved by the **calibration procedure**, not a guessed constant: (1) ship the policy, (2) **shadow-run** the engine against the first batch of real plans (surface nothing to users), (3) owner reviews the surfaced-vs-suppressed boundary, (4) **lock** the value, (5) telemetry-confirm at launch. Hardcoding a threshold in user-facing copy turns the suite red.

| Constant | Demo value | Class | Production source / decision | Cap |
|---|---|---|---|---|
| `LB_THRESHOLD` (global load-bearing sensitivity cutoff) | — (not gated in demo) | **OWNER-CONFIG** | DL-209 §C — one global, auditable value applied uniformly. **Ratified launch policy:** conservative-floor bias; the value is set by the calibration procedure (shadow-run → owner boundary review → lock → telemetry-confirm), never guessed. | — |
| `LB_ASYMMETRIC_LOSS` (miss-vs-marginal weight) | — | **OWNER-CONFIG** | DL-209 §D — a missed load-bearing item costs more than a marginal surface; biases toward surfacing within the anti-treadmill budget. | — |
| `LB_CRITICAL_FLOOR` (always-surfaced floor) | — | **OWNER-CONFIG** | DL-209 §D — a hard floor the surfacing-preference can never suppress. | — |
| `LB_SURFACE_PREF` (user surfacing-preference offset) | — | **OWNER-CONFIG** | DL-209 §C — explicit user dial (aggressive ↔ conservative); changes surfacing, **never** the honesty of the read (DR-7/DL-103). | — |
| Segmentation (domain thresholds) | — | **OWNER-CONFIG (dormant)** | DL-209 §C — hierarchical-shrinkage, **global at launch**; stage → L1 runway (not here), stakes → explicit input, domain → learned via L4 as data earns it. Guard: **zero-data segment = global**. | — |

**⚠️ Production L2 config, not current demo constants** — the prototype surfaces the fixture set directly; the real gate is DL-209's sensitivity engine (L1) + this calibration (L2). The prototype's contribution is the **derived** resolution model (L3): guards `resolutionDerivedFromModel`, `onlyVerifyMovesGrounding`, `loadBearingInferenceVerify`, `findingModelComplete`, `findingTypeExhaustiveOrEscalates`.

### DL-210 — structural-target assignment + escalation (L3 display config)

| Constant | Demo value | Class | Production source / decision | Cap |
|---|---|---|---|---|
| `MODELGAP_LEVERAGE_GATE` (surface an unmapped/model-gap item only when its structural leverage puts it on a path to the outcome) | — (no model gaps in the fixture) | **OWNER-CONFIG** | DL-210 §C — leverage is graph-computable even when classification isn't; below the gate, a model gap rests on the map (benign), above it surfaces as a leverage-gated **known-unknown**. Owner-calibrated. | — |
| Incompleteness ceiling (a load-bearing model gap reads *incomplete / under review*, blocks a Sound claim, **never** Fragile) | — | **DERIVED (behavior, not a number)** | DL-210 §D — weakest-gate honesty applied to unknowns; localized + leverage-gated. Guards `modelGapCeilingIsIncompleteNotFragile`/`unknownNeverScoredAsWeak` (GT-49/50). | — |

**⚠️ Production config, not demo constants.** The prototype has no model gaps (the 6-item fixture is fully mapped). These govern the real engine's escalation/known-unknown surface; dimension assignment itself is **deterministic from the structural target** (DL-210 L3), never a tunable.

---

## Open decisions for the owner (⚠️ rows above)
1. ✅ **RATIFIED 2026-08-09 — SLA reconciliation:** "usually under a minute" promises *analysis completion*; backend SLA = typical/p50 ≈45 s, large uploads may exceed. Guided-walkthrough length decoupled (no copy change). Feeds capability #21.
2. ✅ **RATIFIED 2026-08-09 — cadences:** survey retirement is **event/session-based** (retire on continued work, re-offer next session, cap ~3 lifetime); coaching stays **per-card count** (`COACH_MAX`). All numbers = owner-config placeholders, cross-session persisted, never wall-clock. Prototype keeps its demo timers as a stand-in.
3. ✅ **RATIFIED 2026-08-09 — freeze gate:** default **2** as owner-config (call = confirm/flag/route).
5. ✅ **RATIFIED 2026-08-09 — intake envelope:** per canon, Free = content-metered **~50k words (entitlement config)**; `10 files / 10 MB` = upload rails/placeholders. Build = per-tier config (fixes F11). Exact word numbers (Free ~50k · Basic undefined) deferred to config.
4. ✅ **RATIFIED 2026-08-09 — engagement signal:** **engaged** = milestone (≥ half the load-bearing read grounded OR integrity up ≥1 band; config default ½), persisted per-user cross-session, alongside a durable **onboarded** flag. Replaces the `confirmCount≥3` / `firstRun`-reset proxy.
6. ✅ **RATIFIED 2026-08-09 — SIM-tag gate:** KEEP `_S10.demoSimsTagged` as a **permanent build gate** + the convention (every demo behavior carries `/* SIM:#NN */`; a `SIM:TODO` placeholder is rejected). Applied to BOTH prototypes. Auto-detect of *untagged* sims deferred (false-positive risk). Full capability tagging complete (product caps #1–20, 22, 23; arc #21, 22).

**All six owner-open decisions ratified 2026-08-09.**

7. ✅ **RATIFIED 2026-08-09 → DL-209 — load-bearing sensitivity + issue-classification.** Resolution is **derived** from the finding's nature (L3), retiring the hand-set `primaryMove`; only **verify** moves Grounding; every load-bearing inference leads with a verify CTA (fixed the catering card). L2 calibration params registered above — **global threshold at launch, dormant segmentation** (stage→L1, stakes→explicit, domain→learned), zero-data-equals-global guard. **Final ratification pass 2026-08-09:** (a) L2 launch **policy** ratified (conservative floor + calibration procedure — no guessed number becomes canon); (b) the 6-row finding-type table is **launch-complete**, with **escalate-on-new** enforced in code + `findingTypeExhaustiveOrEscalates`/GT-38; (c) the engine build is vehicled as **Slice 10** (`slices/10-load-bearing-sensitivity-engine.md`), wired into `BUILD_SEQUENCE.md`, with server twins **GT-34…GT-44**. Prototype L3 = 5 firewall guards; L0/L1/L2/L4 = the Slice 10 build. **No open build dependencies remain** — every residual is an enforced guard or a defined procedure.

8. ✅ **RATIFIED 2026-08-09 → DL-210 — CAF dimension boundaries + deterministic structural-target assignment.** The three CAF/Viability dimensions get crisp scope boundaries (Clarity=definition · Alignment=edge/relational · Feasibility=achievability) with **Clarity→Alignment→Feasibility precedence**; **Alignment is relational**, assessed top-down outcome→roots. Dimension assignment is **deterministic from the finding's structural target** (not finding-type; **amends CAF Positions #10/#11**, preserves #2/#13), judgment quarantined at L0 and surfaced via **escalation** (runtime→user clarify/verify issue; model-gap→governance + leverage-gated known-unknown). A load-bearing model gap ceilings integrity **incomplete, never Fragile**. Config above (`MODELGAP_LEVERAGE_GATE` + the incompleteness ceiling); guards GT-45…GT-50 (engine-level, pending until L1 built). Realization extends Slice 10 §3b.

_AI recommends; the owner ratifies. Route value decisions through the BACKLOG "Owner-Open Decisions" (Framework 001)._
