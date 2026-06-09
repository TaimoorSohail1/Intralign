# Proposal / Disposition (DRAFT) — DL-051 Pass 2: Split the Whole-Moved Folders by Ownership

> **Status:** **DRAFT · Pending Owner Ratification** — AI-drafted recommendation; ratifies nothing.
> Per `00_owner` `CLAUDE.md`: only the repository owner may ratify/adopt canonical content, and
> **doctrine is never introduced or relocated without owner action.** Nothing moves until ratified.
>
> **Proposed Decision ID:** **DL-052** · **Date drafted:** 2026-06-09 · **Layer:** Root Governance
> (structural; affects content tiers). **Builds on / completes:** DL-051 (Pass 1 moved these folders whole).

---

## 1. Purpose

DL-051 relocated five genuinely-mixed folders **whole** into a best-fit zone, deferring their internal
splits "to follow-on proposals" (the DL-037 Specs-10/12 precedent). DL-052 performs those splits: it routes
each file to its correct ownership zone by **tier** (doctrine / decision / product-meaning / interface /
realization / working-trail). It edits **no body content** — pure relocation, doc-integrity-gated.

The five folders: `10_product/domain` (34), `30_engineering/reviews` (13), `30_engineering/product_audits_reviews`
(19), `20_handoff/data_api_nfr` (14), `30_engineering/telemetry` (2).

---

## 2. Classification & routing (recommended)

### 2a. `10_product/domain/` (the models) — mostly stays; extract doctrine, decisions, realization

**STAY in `10_product/domain/`** — founder-approved **product domain-meaning** models (tech-independent
"what a concept means to the product"): `ACCEPTED_UNDERSTANDING_MODEL_V1`, `CAF_ASSESSMENT_MODEL_V1`,
`CONFIDENCE_MODEL_V1`, `DISPOSITION_MODEL_V1`, `FINDING_MODEL_V1`, `FINDING_SYSTEM_SPECIFICATION_V1`,
`GOVERNANCE_MODEL_V1`, `MRI_MODEL_V1`, `NOTIFICATION_MODEL_V1`, `ORIENTATION_STATE_MODEL_V1`,
`OVERLAY_MODEL_V1`, `PLANNING_INTELLIGENCE_SPECIFICATION_V1`, `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1`,
`RECOMMENDATION_MODEL_V1`, `RECOMMENDATION_SYSTEM_SPECIFICATION_V1`, `RELIABILITY_MODEL_V1`,
`RESOLUTION_CANDIDATE_MODEL_V1`, `REVIEW_REQUEST_MODEL_V1`, `MODEL_LINEAGE_INDEX_V1`, `README.md`.

**→ `00_owner/doctrine/`** — genuine **doctrine** (establishes human meaning, system-wide; "no formulas"):
`OUTCOME_CONFIDENCE_INTERPRETATION_DOCTRINE_001`, `OUTCOME_CONFIDENCE_LEADERSHIP_DOCTRINE_001`.
⚠ **Owner-confirm:** this *relocates* content into the doctrine tier. Recommended because each file's own
header declares it "Doctrine … establishes meaning, not measurement."

**→ `00_owner/decisions/`** — **decision** artifacts ("intended for entry into the decision log"):
`OUTCOME_CONFIDENCE_DOCTRINE_DECISION_001`, `OUTCOME_CONFIDENCE_CALIBRATION_DECISION_001`.

**→ `00_owner/doctrine/`** *(⚠ owner-confirm — alt: `90_research`)* — **doctrine reconstruction + founder
annotation**: `OUTCOME_CONFIDENCE_DOCTRINE_DISCOVERY_V1`. It is "doctrine archaeology" but carries
founder-authored doctrine direction; recommend owner-zone so the founder content stays canon-adjacent.

**→ `00_owner/backlog/`** *(⚠ owner-confirm — alt: `90_research`)* — **recommendations only, no doctrine
created**: `OUTCOME_CONFIDENCE_DOCTRINE_REFINEMENT_ASSESSMENT_001` (a refinement backlog input).

**→ `00_owner/audits/`** — governance reviews / coverage audits / maps:
`OUTCOME_CONFIDENCE_CALIBRATION_DECISION_001_GOVERNANCE_REVIEW`, `MODEL_COVERAGE_AUDIT_V1`,
`OUTCOME_CONFIDENCE_STACK_INDEX`.

**→ `30_engineering/` (realization)** — scoring formulas & L4 realization (the *how* of computation):
`CAF_CONFIDENCE_V0_SCORING_FORMULA_V1`, `CAF_SCORING_MODEL_V1`, `CAF_SCORING_MODEL_V2`,
`CONFIDENCE_MODEL_V2` (self-labeled "L4 realization"), `RELIABILITY_MODEL_V2` (self-labeled "L4 realization").
⚠ **Owner-confirm:** `CAF_SCORING_MODEL_V1/V2` — *scoring mechanism* (→ engineering) vs *banding semantics*
(→ product). Recommended engineering because they specify computation; the **invariant** (confidence ≠
probability) already lives as doctrine.

### 2b. `…/reviews` + `…/product_audits_reviews` — by grade (owner's DL-051 choice)

**STAY in `30_engineering/reviews/`** (consolidate both folders here) — **working** architecture/engineering
audits & validation/coverage/readiness reviews (the evidence trail; the *decisions* they informed already
live in `00_owner`): all of `reviews/` except the three below, plus all of `product_audits_reviews/`
(consistency/refactor/readiness/UX/data-state/scope-gap/terminology audits).

**→ `00_owner/audits/`** — **decision-grade governance / ratification** reviews:
`GOV_ARCH_001_CANONICAL_ARCHITECTURE_GOVERNANCE_REVIEW`, `OSLO_ADVISORY_COGNITION_RATIFICATION_REVIEW_002`,
`RECOMMENDATION_SYSTEM_SPECIFICATION_V1_GOVERNANCE_REVIEW`.

### 2c. `20_handoff/data_api_nfr/` — split three ways by artifact type

**→ `20_handoff/interfaces/`** (the agreed surface): `API_CONTRACT_ENDPOINT_CATALOG`,
`API_CONTRACT_READINESS_REPORT`, `RELEASE_1_API_CONTRACT_SPECIFICATION_V1`,
`RELEASE_1_EVENT_MODEL_SPECIFICATION_V1`, `RELEASE_1_STATE_MODEL_SPECIFICATION_V1`.

**→ `30_engineering/data/`** (schema/realization): `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.2`,
`DATA_MODEL_RECONCILIATION_CHANGE_LOG`, `DATA_MODEL_RECONCILIATION_IMPACT_REPORT`,
`DATA_MODEL_RECONCILIATION_PATCH_001`, `DATA_MODEL_V1_2_RECONCILIATION_APPLICATION_SPECIFICATION`.
**→ `30_engineering/analysis_engine/`**: `RELEASE_1_ANALYSIS_ENGINE_SPECIFICATION_V1`.

**→ `10_product/acceptance/`** (outcome/NFR **targets**): `RELEASE_1_NFR_ACCEPTANCE_MATRIX`,
`RELEASE_1_PERFORMANCE_AND_NFR_SPECIFICATION_V1`.

### 2d. `30_engineering/telemetry/` (2 files) — recommend **keep as realization**

`OSLO_RELEASE_1_OBSERVABILITY_AND_ECONOMICS_PLATFORM_SPECIFICATION_V1`,
`RELEASE_1_TELEMETRY_AND_PRODUCT_ANALYTICS_SPECIFICATION_V1` are **platform/observability realization**
specs → stay in `30_engineering`. The analytics/economics *targets* they reference are product acceptance
criteria that already live in `10_product`. *(No split needed; lowest-stakes folder.)*

---

## 3. Framework 001A Review

**Findings.** (1) The split is mostly *extraction* — ~70% of files stay; only ~30 relocate. (2) It strengthens
precedence: doctrine and decisions leave the product zone for `00_owner`. (3) Mechanical cost is low (pure
renames; basename-resolved references survive; doc-integrity stays green). (4) `models/` is the only
high-judgment cluster and is enumerated file-by-file with rationale.

**Concerns.** (1) **Doctrine relocation** (2a → `00_owner/doctrine`) is the highest-stakes change and must be
owner-confirmed (⚠ flags). (2) `CAF_SCORING_MODEL_V1/V2` mechanism-vs-semantics is a true judgment call
(⚠). (3) Two doctrine *analyses* (Discovery, Refinement Assessment) sit between `00_owner` and `90_research`
(⚠). (4) Review by-grade lines are defensible but contestable; the 3 picks are conservative.

**Dependencies.** New target dirs (`20_handoff/interfaces`, `30_engineering/data`, `10_product/acceptance`);
doc-integrity green as the gate; CODEOWNERS already zone-routed (no change). No body edits.

**Recommendation.** **Adopt** the routing in §2 with the ⚠ items confirmed by the owner, executed as one
atomic Pass-2 commit gated on a green doc-integrity run. Lowest-stakes items (2b working reviews, 2c interfaces,
2d telemetry) are safe to execute as recommended; the doctrine/realization extractions in 2a should get an
explicit owner yes/adjust first.

**Status.** **DRAFT — pending owner ratification.** No files moved. AI does not ratify.

---

## 4. Owner decision

- **(A)** Ratify §2 as recommended (I confirm the ⚠ calls below) → I execute Pass 2 as one verified commit.
- **(B)** Ratify with adjustments to specific ⚠ rows (tell me which) → I execute the adjusted map.
- **(C)** Execute the low-stakes folders now (2b/2c/2d) and hold `models/` (2a) for a deeper owner pass.

The ⚠ owner-confirm calls, consolidated: **(i)** relocate the two Doctrine files into `00_owner/doctrine`;
**(ii)** `CAF_SCORING_MODEL_V1/V2` → engineering (mechanism) vs product (semantics); **(iii)** the two doctrine
*analyses* → `00_owner/doctrine`/`backlog` vs `90_research`.
