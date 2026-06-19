# Backlog — Adoption Acceleration & Growth Loops (Candidate Capabilities)

- **Status:** **Candidate — owner triage.** AI-drafted from the 2026-06-19 growth/defensibility advisory. **Not adopted, not contracts, not Release-scoped** until the owner triages. Each capability is **scoped against the epistemic-safety + privacy doctrines** per the Anti-Assumption protocol (scope before building; escalate; do not assume placement).
- **Thesis:** in the AI era, feature moats are gone; defensibility comes from **proprietary data loops, embedded workflows, switching costs, and trust.** The capabilities below are chosen so that **accelerating adoption and building the moat are the same move** — growth loops that get *harder to displace* the more they're used.
- **Source:** owner direction 2026-06-19; current B2B-AI growth/defensibility best practice; grounded in Doctrine 04 (Outcome Integrity), Doctrine 08 (Collaboration), Doctrine 09 (PLG), DL-047/DL-055 (CRR/Advise), DL-073 (deferred-signup/anonymous), DL-075 (outcome-lifecycle), and the Wave E Disclose / Export-Share-Out contracts.

> **Governance note (read first).** Two of these (G1 data loop, G2 benchmarking) **use plan + outcome data and produce Derived insight** — they are **cognition-adjacent, NOT commodity** (crosswalk rule: "if unsure whether something is commodity, treat it as cognitive and escalate"). They touch the epistemic core and aggregate/cross-tenant data → **owner + doctrine scoping required before any build.** Two (G3, G4) are mostly commodity growth-layer over **already-contracted** seams, with epistemic-safety constraints noted.

---

## Release model + growth-loop scoping (Alpha = 3–5 releases; verified 2026-06-19)

**Release model (owner, 2026-06-19): the Alpha stage spans 3–5 releases**, scaling the user base toward the **§20 Alpha→Beta gate (50+ users)**: **R1** = owner + <5 (private validation; manual onboarding) → **R2** = 10–20 → … → **50+ ⇒ graduate to Beta.** R1/R2 are *early Alpha releases* below the gate; the 50+ metric is reached **at the end of Alpha**, not in R1/R2.

**G3 and G4 are R2** (the second Alpha release). Their **R1 foundations** are built in R1 — the CRR seam (Wave I `IC-WI-INTERACT`, DL-047) and the Export/Share-Out surface (Wave E Disclose) — so R2 has its dependencies met; the external non-user → convert half was already R2 (DL-049). **R1 has no growth loops** — owner validation is manual (DL-049: "R1 generates + measures invitations only"). The **full G3/G4 loops are built in R2 and drive the scale-up across the later Alpha releases (R3–R5) toward the 50+ §20 Beta gate.** Verified result:

| Capability | Phase | Scope | Foundation / dependency |
|---|---|---|---|
| **G3** alignment/CRR loop | **R2** | the full loop — cohort CRR collaboration + invitation generation/measurement **and** the external recipient → convert experience | foundation (CRR seam, Wave I `IC-WI-INTERACT`, DL-047) built in **R1**; "R1 generates + measures invitations only" (DL-049); full loop + recipient UI/auth/convert/link-security (#339) = R2 |
| **G4** shareable artifact | **R2** | the branded epistemic-safe share-out **and** the open no-account public-acquisition view | foundation (Export/Share-Out, Wave E Disclose) built in **R1**; the public no-account view + link security (#339) = R2 |
| **G1** plan→outcome data loop | **Alpha = capture only** | instrument **plan + outcome data capture** so the moat starts compounding from day one | the **learning / network-effect** is post-Beta — depends on the Validation/execution-monitoring capability (forward, Pro+), **scale**, and privacy/consent/doctrine scoping |
| **G2** benchmarking | **post-Alpha / forward** | — | **cannot honestly benchmark at low N** without violating the epistemic-honesty invariant; depends on G1 + corpus scale + k-anonymity/doctrine scoping |

**By Alpha release:** **R1** = cognition + the R1 foundations (CRR seam / Wave I; Export-Share-Out / Wave E) + **G1 data-capture**; **R2** = **G3 + G4 full growth loops** (on the R1 foundations); **R3–R5** = the loops drive the scale toward the **50+ §20 Beta gate**. **Beta+ / forward:** G1's learning, G2 (benchmarking — needs scale + the data loop), G5 (Pro+ connectors), G6. *(G3/G4 are Alpha-stage growth loops at R2 — they drive the §20 graduation across the later Alpha releases, kept whole on completed R1 foundations.)*

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
| G3 | Alignment-as-viral-loop (CRR) | commodity over contracted seam | collaborative-necessity virality | **R2** (foundation Wave I in R1) | DL-047 / DL-049 |
| G4 | Shareable artifact acquisition | commodity + Disclose constraint | content-led acquisition | **R2** (foundation Wave E in R1) | DL-073, Export/Share-Out |
| G5 | Integration-as-distribution | commodity + forward connectors | switching cost + marketplace distribution | forward (Pro+) | Doctrine 09 P0; exec-monitoring |
| G6 | Community template gallery | commodity content loop | content virality + cold-start | post-R1 | DL-056 |

**Recommended sequencing:** **R1 (Alpha)** = G1 (data-capture foundation only) — plus the R1 *foundations* G3/G4 sit on (CRR seam / Wave I; Export-Share-Out / Wave E). **R2** = G3 + G4 (the full growth loops, on those completed foundations) + G1's learning. **Forward (Pro+ / post-R1)** = G2, G5, G6. **Forward (Pro+)** = G5 connectors + G1/G2 at scale. Start *capturing* the plan→outcome data (G1) early — it's the time-compounding moat that answers the displacement risk. G1/G2's learning and G6's open contribution require explicit owner + doctrine/curation scoping before build (privacy, consent, epistemic classification).

*Candidate backlog for owner triage. Introduces no contract, no doctrine, no Release commitment; every item maps to existing canon and is fenced by the epistemic-safety + privacy doctrines.*
