# Backlog — Adoption Acceleration & Growth Loops (Candidate Capabilities)

- **Status:** **Candidate — owner triage.** AI-drafted from the 2026-06-19 growth/defensibility advisory. **Not adopted, not contracts, not Release-scoped** until the owner triages. Each capability is **scoped against the epistemic-safety + privacy doctrines** per the Anti-Assumption protocol (scope before building; escalate; do not assume placement).
- **Thesis:** in the AI era, feature moats are gone; defensibility comes from **proprietary data loops, embedded workflows, switching costs, and trust.** The capabilities below are chosen so that **accelerating adoption and building the moat are the same move** — growth loops that get *harder to displace* the more they're used.
- **Source:** owner direction 2026-06-19; current B2B-AI growth/defensibility best practice; grounded in Doctrine 04 (Outcome Integrity), Doctrine 08 (Collaboration), Doctrine 09 (PLG), DL-047/DL-055 (CRR/Advise), DL-073 (deferred-signup/anonymous), DL-075 (outcome-lifecycle), and the Wave E Disclose / Export-Share-Out contracts.

> **Governance note (read first).** Two of these (G1 data loop, G2 benchmarking) **use plan + outcome data and produce Derived insight** — they are **cognition-adjacent, NOT commodity** (crosswalk rule: "if unsure whether something is commodity, treat it as cognitive and escalate"). They touch the epistemic core and aggregate/cross-tenant data → **owner + doctrine scoping required before any build.** Two (G3, G4) are mostly commodity growth-layer over **already-contracted** seams, with epistemic-safety constraints noted.

---

## Alpha / Beta scoping (verified 2026-06-19 against the wave / release plan)

**Owner direction (2026-06-19): G3 and G4 are Alpha scope** — the virality/sharing loops are the **engine for the §20 whole-Alpha graduation metrics** (50+ users + engagement that gate Beta), so they belong in Alpha, not parked for Beta (`RELEASE_1_VIRALITY_K_FACTOR_AUDIT` was P0). They sit **late in Alpha** (after their build deps land — G3 on Wave I, G4 on Wave E), and the **external non-user → convert half stays R2** (DL-049). Verified result:

| Capability | In Beta? | Ships in Beta | Deferred (with the reason) |
|---|---|---|---|
| **G3** alignment/CRR loop | **Alpha (late)** | the cohort-internal CRR collaboration loop **+ invitation generation + k-factor measurement** (Wave I `IC-WI-INTERACT`, contracted under DL-047) — built once Wave I lands; positioned to drive §20 graduation | the **external non-user recipient → convert** experience stays **R2** — **DL-049 ratified**: "R1 generates + measures invitations only"; recipient UI / auth / convert-moment / link-security (#339) = R2 |
| **G4** shareable artifact | **Alpha (late)** | the **branded, epistemic-safe share-out** within the controlled cohort (Disclose Export/Share-Out, Wave E) — a controlled-invite growth loop; built once Wave E lands | the **open no-account public acquisition view + link security** stays **R2** (same recipient-experience build as G3, #339) |
| **G1** plan→outcome data loop | **Capture only** | instrument **plan + outcome data capture** so the moat starts compounding from day one | the **learning / network-effect** is post-Beta — depends on the Validation/execution-monitoring capability (forward, Pro+), **scale** (no network effect at Beta N), and privacy/consent/doctrine scoping |
| **G2** benchmarking | **No** | — | **post-Beta** — **cannot honestly benchmark at low N without violating the epistemic-honesty invariant**; depends on G1 + corpus scale + k-anonymity/doctrine scoping |

**Alpha set:** G3 (loop + k-factor measurement) · G4 (cohort branded share-out) — both **late-Alpha**, positioned to drive the §20 graduation metrics · **plus** G1 (data-capture foundation). **Still R2:** the external-recipient conversion half of G3/G4 (the ratified DL-049 boundary), G1's learning, and G2. *(Moving G3/G4 to Alpha changes their build **timing**, not the DL-049 R2 external-conversion boundary.)*

---

## G1. Plan → Outcome Data Loop (data network effect) — *cognition-adjacent · forward*

**Growth thesis.** OSLO's Validation loop (DL-075 / Outcome Integrity) means it eventually sees plans **and their actual outcomes**. Captured as a first-class asset, this is a **data network effect** — the most achievable B2B AI moat: the product gets measurably smarter per customer per month (calibration, risk-pattern detection), and the improvement benefits the *individual* user, not just the aggregate. A competitor can copy features overnight; not the plan-and-how-it-turned-out dataset. **The acquisition story becomes "the only planning AI that learns from how plans actually go."**

**Why now (even pre-capability).** It compounds with time — the thing the competitive-displacement fear is about. Start **capturing** the loop before the full Validation capability ships.

**Mapping to canon.** Outcome Integrity (Doctrine 04: Intended vs Current Reality); Execution-&-Orchestration Maturity Phase 0–1 (Doctrine 10); the Validation stage (DL-075). Outcome data = **Attested evidence** (provenance = source system) → **Derived** understanding (recompute, CHR-appended).

**Epistemic-safety & privacy scoping (must clear before build).**
- Cross-tenant *learning* (calibration from aggregate) is the sensitive part — **per-tenant isolation, consent/opt-in, anonymization, and no leakage of one org's data into another's understanding.**
- Improvements stay **Derived, confidence-qualified**; no fabrication; existing epistemic invariants (Derived-never-Attested, only reanalysis changes assessment) hold.
- **Classification: cognition-adjacent + data infrastructure — escalate.** Likely Release 2+/post-Alpha.

**Owner decisions:** consent/data-rights model; per-tenant vs aggregate learning boundary; Release placement.

## G2. Benchmarking (collaborative network effect) — *cognition-adjacent · forward · depends on G1*

**Growth thesis.** Anonymous peer/industry comparison: "your charter's clarity is bottom-quartile for plans like this"; "plans with this risk profile typically drift on resourcing." **Collaborative intelligence no single org can build alone** — a moat *and* an owned-media engine ("State of Planning" reports). Fits OSLO's honesty doctrine: evidence-based, confidence-qualified.

**Mapping to canon.** Outcome Integrity (Current Reality vs peer baselines); Disclose (presentation of a Derived comparative read).

**Epistemic-safety & privacy scoping.**
- **Strict anonymization + k-anonymity thresholds + opt-in;** never expose an individual org's data.
- Benchmarks are **Derived, coverage/confidence-qualified, never shown as settled fact** (Disclose epistemic-safety; band-edge guard); no overstatement.
- **Classification: cognitive (a Derived comparative insight) — escalate.** Depends on G1's data loop. Release 2+.

**Owner decisions:** privacy/anonymity thresholds; opt-in model; whether comparative reads are a new Evaluate/Disclose surface (doctrine/ontology check).

## G3. Alignment-as-Native-Viral-Loop (collaborative by necessity) — *mostly commodity over a contracted seam · near-term*

**Growth thesis.** The most durable B2B virality isn't a referral incentive — it's **collaborative necessity.** Alignment and stakeholder divergence are CAF dimensions; you *cannot* resolve a clarification or validate an assumption **without** the stakeholder. So the **CRR (CAF Review Request) / clarification-request flow is OSLO's native viral loop** — every "this finding needs input from the assumption owner" is an invite to a likely non-user, motivated by the product's core job. **Instrument K-factor on this** (invite → join → conversion), not on a bolt-on reward.

**Mapping to canon.** DL-047/DL-055 (CRR = Advise + collaboration affordance — *already contracted*); Doctrine 08 (Collaboration & Shared Cognition); `BACKLOG_EXTERNAL_STAKEHOLDER_EXPERIENCE` + DL-049 (external-reviewer identity); calibration §4e (share/invite prompts, k-factor objective).

**Epistemic-safety scoping.**
- The **growth instrumentation** (non-user invite UX, k-factor telemetry) is **commodity** riding the **existing contracted CRR seam** — clean separation.
- The clarification request **does not change assessment** (only reanalysis does); the invite is a collaboration affordance, not cognition. Preserve OB-5.
- **Classification: commodity growth-layer over a contracted cognitive seam.** Near-term (CRR is R1-adjacent; external-stakeholder identity per DL-049).

**Owner decisions:** make CRR-invite the *primary* loop vs. referral reward; external-stakeholder lightweight-view scope.

## G4. Shareable Artifact as Content-Led Acquisition — *commodity delivery + contracted epistemic-safety · near-term*

**Growth thesis.** The 60-second orientation / MRI is a "wow" object. Make a shared orientation a **branded, view-without-account surface** (Loom/Gamma pattern), not just a file export — the sponsor/exec who receives "here's what OSLO understood about this plan in 60 seconds" becomes a **lead**. Content-led acquisition loop.

**Mapping to canon.** `EXPORT_AND_SHARE_OUT_EXPERIENCE_SPECIFICATION_V1` + Wave E **Disclose Export/Share-Out** contract; `INVITE_AND_SHARE_MODAL`; **DL-073** (anonymous / view-without-account model — the recipient's no-account view reuses the deferred-signup mechanics).

**Epistemic-safety & privacy scoping.**
- The shared artifact **must honor the Disclose export contract**: epistemic labels preserved (Attested/Derived, confidence band, plan-fact attribution), provenance intact, **no new claims** — a shared orientation can't quietly become an overstated marketing artifact.
- **Sharer controls scope;** view-without-account must not leak beyond the intended surface; respect sharing-permission boundaries.
- **Classification: commodity sharing/delivery with a contracted Disclose epistemic-safety constraint.** Near-term (builds on existing share-out + the DL-073 anonymous model).

**Owner decisions:** what's exposed in the no-account view (full orientation vs teaser); branding/CTA; share-scope controls.

## G5. Integration-as-Distribution — *commodity distribution + connector architecture · forward*

**Growth thesis.** OSLO imports from Jira / Asana / Linear / Planner / Smartsheet (Doctrine 09, Phase 0). Those integrations do **triple duty**: the **Validation mechanism** (execution-state / outcome ingestion → Current Reality), a **switching cost** (embedded where plans already live), and a **distribution channel** (their app marketplaces are acquisition surfaces). "Meet plans where they live."

**Mapping to canon.** Doctrine 09 Phase 0 (execution-state ingestion); the connector/integration architecture (tied to the **Pro+ execution-monitoring** scoping decision — `BACKLOG_TIER_PROGRESSION` Tier-3 note); Perceive intake (Attested, provenance = external system).

**Scoping.** Inbound import = Perceive intake (Attested); marketplace listing/distribution = commodity GTM. The execution-monitoring connectors are a **Pro+ forward** scoping decision (own decision). **Classification:** commodity distribution + a forward connector-architecture decision. **Horizon:** connectors forward (Pro+); marketplace distribution can begin once a first integration ships.

**Owner decisions:** which platforms first; marketplace-listing GTM; sequencing against the Pro+ execution-monitoring connector scoping.

## G6. Community Template Gallery — *commodity content loop · post-R1 expansion of DL-056*

**Growth thesis.** You have 5 owner-curated templates (DL-056). A **contributable / shareable template gallery** is a **cold-start** (instant value) **+ content-virality** loop — each shared template is an acquisition surface, and community contribution compounds the catalog.

**Mapping to canon.** DL-056 (Start From Template, R1; curated catalog of five; Guided Intake deferred R2); `RELEASE_1_TEMPLATE_INTAKE_SPECIFICATION_V1`; `10_product/experience/templates/`.

**Scoping.** A template is **pre-authored content the user adopts — explicitly NOT generation** (DL-056), so a gallery stays epistemic-safe (no generated content). Community contribution + sharing = commodity, but needs a **curation / moderation / quality-governance** model (the curated-catalog principle protects quality). **Classification:** commodity content loop with a curation-governance question. **Horizon:** curated-five is R1; the contributable gallery is a **post-R1 expansion** of DL-056.

**Owner decisions:** open-contribution vs curated-only; moderation/quality model; Release placement (expands DL-056).

---

## Triage summary

| # | Capability | Class | Primary moat/loop | Phase? | Depends on |
|---|---|---|---|---|---|
| G1 | Plan→outcome data loop | cognition-adjacent + data infra | data network effect | **capture only** | Validation (DL-075) |
| G2 | Benchmarking | cognitive — escalate | collaborative network effect | **no (post-Beta)** | G1 + scale |
| G3 | Alignment-as-viral-loop (CRR) | commodity over contracted seam | collaborative-necessity virality | **Alpha (late)** (ext. convert = R2) | DL-047 / DL-049 |
| G4 | Shareable artifact acquisition | commodity + Disclose constraint | content-led acquisition | **Alpha (late)** (open view = R2) | DL-073, Export/Share-Out |
| G5 | Integration-as-distribution | commodity + forward connectors | switching cost + marketplace distribution | forward (Pro+) | Doctrine 09 P0; exec-monitoring |
| G6 | Community template gallery | commodity content loop | content virality + cold-start | post-R1 | DL-056 |

**Recommended sequencing:** **Alpha (late)** = G3 (loop + k-factor measurement) · G4 (cohort branded share-out) — positioned to drive the §20 graduation metrics; **plus** G1 (data-capture foundation). **R2** = the external-recipient conversion half of G3/G4 (already DL-049's plan), G1's learning, G2, G6. **Forward (Pro+)** = G5 connectors + G1/G2 at scale. Start *capturing* the plan→outcome data (G1) early — it's the time-compounding moat that answers the displacement risk. G1/G2's learning and G6's open contribution require explicit owner + doctrine/curation scoping before build (privacy, consent, epistemic classification).

*Candidate backlog for owner triage. Introduces no contract, no doctrine, no Release commitment; every item maps to existing canon and is fenced by the epistemic-safety + privacy doctrines.*
