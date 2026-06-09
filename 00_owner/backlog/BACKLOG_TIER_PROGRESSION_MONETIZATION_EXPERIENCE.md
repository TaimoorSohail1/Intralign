# Backlog (DRAFT) — Tier-Progression / "Graceful-Limit-as-Upgrade-Moment" Experience + Paid-Tier Config Ladder

**Status:** **Proposed — owner-directed (2026-06-05).** Pending Owner Ratification. Per `CLAUDE.md`, only the owner ratifies; this routes a monetization-experience design + paid-tier config to the owner rather than editing contracts or defining tiers unilaterally. **No architecture change; no new responsibility/object.** Builds on DL-046 (Fast/Deep + 60s), DL-048 (tier-keyed cost governance), CHG-056 (Tier-1 envelope).

---

## 0. Owner intent (the desired experience)

> Active Tier-1 (Free) users should, **over time and with capability use, reach system constraints**, and at those moments be **encouraged to upgrade** — such that **project size (and capability) increases with each tier.**

This is a deliberate **growth-into-upgrade funnel**: Free starts small; sustained use bumps the user into the tier's ceilings (project size, active projects, depth, daily allowances, model quality); each ceiling is an **upgrade moment**; upgrading **relaxes those ceilings**.

## 1. Why this is mostly *already supported* (and where it isn't)

The DL-048 / CHG-056 scaffolding made the envelope, cost caps, model routing, and daily allowances all **tier-keyed config**. So "constraints tighten on Free and relax up-tier" is a **config ladder, not new architecture.** What is **not yet explicit anywhere** is the **experience of hitting a constraint** — today it is split across two places that were never tied together:

- **Contracted (cognitive) behavior:** beyond the Tier-1 envelope, the Fast/Deep engine **degrades gracefully** (partial orientation + coalesced Deep — DL-046/048). Disclose must surface reduced coverage/confidence honestly (progressive disclosure + false-confidence detection — DL-047).
- **Commodity (billing) behavior:** daily-cap gating (`429`/`422`) + **MON-04 Upgrade Prompts** (Category C/E, DL-043 J).

**The gap:** nobody owns the **seam** between them — the "constraint-reached → upgrade moment" as a single intentional experience. Built separately, the risk is **degradation so graceful the user never feels the limit** (no upgrade trigger), or a **bare error** with no honest explanation.

## 2. The design principle (the thing to get right)

**A Tier-1 constraint must be surfaced as an _attributable tier limit_, not silently absorbed.** "This is a **partial** analysis because your project exceeds the Free-tier size — upgrade to analyze it in full," not a silent truncation and not a dead-end error.

**Why this is durable, not a hack:** it is the *same behavior* OSLO's epistemic invariants already demand. OSLO must never overstate understanding; a scope-limited run must show **reduced confidence/coverage and say why**. So **honest limit-disclosure satisfies epistemic safety _and_ creates the upgrade moment with one behavior.** The constraint becomes a truthful disclosure — the most durable upgrade prompt there is. (Convergence, not conflict: surfacing limits is what OSLO does anyway.)

## 3. The upgrade levers (existing tier knobs — each a place a growing user bumps)

| Lever | Free / Tier 1 (set) | climbs with tier → |
|---|---|---|
| Project size (Fast-Pass envelope) | ~20 docs / ~50k words | larger guaranteed envelope |
| Active projects | 1 | several → many |
| Deep runs / day | 2 | more → on-demand |
| Suggested fixes · chats / day | 5 · 20 | higher → unmetered |
| Model routing (speed/depth) | nano/mini (cheap) | mini → full (faster, deeper) |
| Monthly token budget | 4M (~$3) | higher ceiling |

## 4. Illustrative paid-tier ladder (OWNER DECISION — starting points, not ratified)

Worst-case cost = user consumes the full monthly budget (median far below); reconciled to verified June 2026 pricing. **Price is a separate business decision** (willingness-to-pay), shown only to display margin headroom.

**Canonical tier taxonomy (owner-set 2026-06-05):** **Tier 1 Free · Tier 2 Basic · Tier 3 Pro · Tier 4 Team · Tier 5 Enterprise.** Project size and capability increase monotonically up the ladder. **T1 Free and T2 Basic are owner-confirmed (values in Calibration §4c); T3–T5 remain owner-decision.** Design rule: **Basic sells _capacity_; Pro adds _model quality_ (faster/deeper full-quality routing)** — keep premium routing above Basic to protect the low tier's margin and the Pro upsell.

| Tier | Envelope (docs / words) | Active proj | Deep/day | Fixes·chats/day | Routing | Token budget | **Worst-case cost/mo** | Illustrative price |
|---|---|---|---|---|---|---|---|---|
| **T1 — Free** ✓ *confirmed* | ~20 / 50k | 1 | 2 | 5 · 20 | cheap (nano/mini) | 4M | **~$3** | $0 (CAC/subsidy) |
| **T2 — Basic** ✓ *confirmed (2026-06-05)* | ~40 / 100k | 3 | 6 | 20 · 75 | cheap (nano/mini) | 10M | **~$8** | **$12 / mo** |
| **T3 — Pro** *(+ exec-monitoring — see note)* | ~80 / 200k | 10 | 15 | 50 · 200 | mid (mini, full fallback) | 25M | **~$20** | ~$39 / mo |
| **T4 — Team** (per seat) | ~150 / 400k | many | on-demand | high / unmetered | premium (GPT-4.1 synth) | 50M / seat | **~$97** | ~$99–149 / seat / mo |
| **T5 — Enterprise** | custom | custom | custom | custom | premium + dedicated | negotiated | **custom** | custom / contract |

**Economic insight to weigh:** **model-routing quality is a larger cost driver than token volume.** The jump from Pro (~$20, mid routing) to Team (~$97, premium routing) is driven by full-quality synthesis output, not just the larger budget — so the upper-tier upsell of "faster/deeper model" must be **priced high or premium-routing metered**, more so than "more tokens." Keeping cheap routing as the workhorse with full-quality reserved for select steps is the main lever to protect Team/Enterprise margin.

### Tier-3 (Pro) capability note — project-execution monitoring via 3rd-party platforms (owner, 2026-06-05)

Pro (Tier 3) and above will include **project-execution monitoring via integrations with 3rd-party platforms** (e.g. project/work-management tools). This is a **tier-gated capability**, available at **Pro and up** (Team/Enterprise inherit). Governance flags — **do not assume; scope before building:**

- **New capability — NOT in the R1 cognitive core, NOT assumed into R1 scope.** It is absent from `OSLO_CAPABILITY_MATRIX_V2` and must be **scoped as its own item** (which platforms; target Release; architecture). Integration work carries governance history — **DL-042 (Integration Moratorium Closure)** — so scope it deliberately, not by inference.
- **Epistemic fit (clean — it does not bypass the model):** execution data ingested from a 3rd-party platform is **inbound evidence → Perceive intake, Attested with provenance = the external system**; any "on-track / drifting" read is **Derived cognition** (recomputable, CHR-appended). It maps to the **Current-Reality** side of the **Outcome-Integrity** doctrine (coherence between Intended Reality and Current Reality) — execution monitoring *feeds* the Current-Reality signal rather than introducing a parallel truth path.
- **Surface area split:** the **connector/integration layer** (auth to external platforms, sync, field mapping, the platform-specific adapters) is largely **commodity integration** (Category-E, DL-043 J); the **evidence-intake seam** (external data → Attested → recompute) is the **contracted** part. This mirrors the **CRR pattern** — workflow/connector plumbing is commodity, the evidence→cognition seam is contracted.
- **Routing/cost:** continuous external-data polling is a **new recurring cost + rate-limit surface**; fold it under the DL-048 per-tier budget + coalescing (no per-poll recompute storms) when scoped.

**Status:** recorded as a **Pro-tier forward capability**; routes to a dedicated scoping decision (platforms, Release placement, the connector architecture, and a Capability-Matrix entry). **Not Release-1 unless the owner explicitly scopes it in.**

## 5. Scope / governance notes

- **No architecture change; no new responsibility/object.** Tiers are config rows; the only contracted behavior touched is **Disclose surfacing the limit honestly** (already an epistemic-safety obligation — this *names* the tier-limit case).
- **Commodity vs contracted split** (build accordingly):
  - **Commodity (MON, Category C/E — DL-043 J):** the tier definitions/config, daily-cap gating, MON-04 upgrade prompts, billing, the upgrade CTA UI.
  - **Contracted (cognitive):** the **honest limit-disclosure** in the MRI/confidence when a run is scope- or budget-limited (Disclose/Wave E + the DL-048 degradation behavior on the engine) — i.e. the limit must be *visible and attributable*, never silent overstatement.
- **Ties to open items:** resolves the paid-tier side of **Open-TBD A1 (envelope) + E3 (paid-tier limits)** into one coherent "define the paid tiers" decision; consumes the DL-048 §4c cost config pattern.

## 6. Owner decision required
- [ ] Approve the **tier-progression experience** as Release-1 (or fast-follow) scope — specifically that a Tier-1 limit is surfaced as an **honest, attributable tier-limit disclosure** that doubles as the upgrade moment (the contracted Disclose behavior), distinct from the commodity upgrade prompt.
- [ ] Decide the **paid-tier ladder** — confirm/adjust the §4 envelope, active-projects, depth, allowance, routing, and budget rows per tier (values are owner decisions; costs shown for reference).
- [ ] Decide whether paid tiers are **Release-1 scope** or **fast-follow** (Free-tier launch does not depend on them; the enforcement is already tier-parameterized).
- [ ] On approval: add paid-tier rows to **Calibration §4c** + resolve **Open-TBD A1/E3**; enumerate the **tier-limit disclosure** obligation in the Wave E Disclose contract (light — names an existing epistemic-safety behavior); record via changelog. (Pricing handled outside the repo.)

---
*This owner-directed draft captures the desired Tier-1→upgrade growth experience — Free users reach system constraints over time and are encouraged to upgrade, with project size and capability increasing per tier — and identifies that the tier-keyed DL-048/CHG-056 scaffolding already supports it as a config ladder, leaving one unowned seam: the "constraint-reached → upgrade moment." It proposes the governing design principle (a Tier-1 limit must be surfaced as an honest, attributable tier-limit disclosure rather than silently degraded, which converges with OSLO's epistemic-honesty invariants and doubles as the most durable upgrade prompt), separates the commodity billing parts from the one contracted Disclose behavior, and offers an illustrative, cost-reconciled five-tier ladder (T1 Free ~$3 / T2 Basic ~$8 / T3 Pro ~$20 / T4 Team ~$97 worst-case / T5 Enterprise custom) for owner decision — flagging that model-routing quality, not token volume, is the dominant cost driver at the top tier. It changes no architecture and routes the paid-tier definition (Open-TBD A1/E3) and the experience-scope call to the owner.*

**Tier-Progression / Monetization Experience backlog (DRAFT) prepared. Pending Owner Ratification.**
