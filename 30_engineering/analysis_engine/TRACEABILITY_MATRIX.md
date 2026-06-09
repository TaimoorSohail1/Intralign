# Traceability Matrix

**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Purpose:** Trace every stage, key output, enum, constant, and contract to its source classification: `canonical` (in an authoritative spec) · `derived` (entailed) · `proposal` (this pack) · `TBD – Owner Decision Required`.

## Fast Pass stages

| Stage | Exec | Source authority | Classification |
|---|---|---|---|
| 0 Intake & acquisition | rule | Engine §9; Event §15; Data §9 | canonical |
| 1 Normalization | rule | Engine §9; Context Plane (Baseline) | canonical |
| 2 Global skeleton | hybrid | Pack proposal (resolves chunking tension) | **proposal** |
| 3 Claim extraction | hybrid | Engine §9; Planning Intel §16; Data §9 | canonical (bound = proposal) |
| 4 CAF evaluation | hybrid | Planning Intel §9–§11; CAF model | canonical (scale = TBD) |
| 5 Finding generation | hybrid | Finding model; Planning Intel §6 | canonical (severity basis = TBD) |
| 6 Recommendation generation | hybrid | Recommendation model; Planning Intel §7 | canonical (type-map = proposal) |
| 7 Confidence & state | rule | Confidence/Reliability models; Data §10 | canonical (synthesis = TBD) |
| 8 MRI & publication | rule | Engine §20; Event §16; State §6 | canonical |

## Deep Pass stages

| Stage | Exec | Source authority | Classification |
|---|---|---|---|
| 1 Context expansion | hybrid | Engine §10; Planning Intel §17 | canonical |
| 2 Relationship expansion | hybrid | Planning Intel §15/§17 | canonical |
| 3 Assumption expansion | hybrid | Planning Intel §13/§17 | canonical |
| 4 Conflict discovery | llm | Planning Intel §14; Engine §10 | canonical (tolerance = TBD) |
| 5 Additional claim discovery | hybrid | Engine §10 | canonical (bound = proposal) |
| 6 CAF reassessment | hybrid | CAF/Reliability models; Planning Intel §18 | canonical (scale = TBD) |
| 7 Confidence recalculation | rule | Confidence model; Data §10; State §8 | canonical |
| 8 Expanded findings | hybrid | Planning Intel §19; Finding model | canonical |
| 9 Expanded recommendations | hybrid | Planning Intel §20; Recommendation model | canonical |
| 10 Publication & supersession | rule | Engine §20; Event §16; State §16 | canonical |

## Entities & state enums (Data Model v1.1 / State Model)

| Item | Values | Classification |
|---|---|---|
| `Project.lifecycle_state` | created, orienting, oriented, deep_analyzing, analyzed, archived | canonical |
| `AnalysisRun.run_type` | fast_analysis_pass, deep_analysis_pass | canonical |
| `AnalysisRun.run_status` | queued, running, completed, failed, cancelled, superseded | canonical (cancelled via Patch-001) |
| `Finding.status` | detected, acknowledged, addressed, closed, reopened, superseded | canonical (v1.1 reconciled) |
| `Recommendation.status` | generated, accepted, rejected, implemented, superseded | canonical (v1.1 reconciled) |
| `Notification.state` | created, viewed, dismissed, expired | canonical (v1.1 reconciled) |
| `Report.status` | draft, published, superseded, archived | canonical (v1.1 added) |
| `SharedArtifact.status` | created, shared, viewed, revoked, expired | canonical (v1.1 added) |
| `finding_type` | missing_information, ambiguity, assumption, inference, conflict, constraint, coverage_gap | canonical |
| `recommendation_type` | improvement, validation, suggested_fix | canonical |
| CAF dimensions | clarity, alignment, feasibility | canonical |
| `confidence_band` | very_low, low, moderate, high, very_high | canonical (Data §10) |
| reliability inputs | coverage, evidence_availability, assessability | canonical (Reliability §6) |
| reliability level scale | High/Moderate/Low (qualitative) | canonical qualitative; numeric scale = **TBD** |

## Events (Event Model — no new events)

| Event group | Classification |
|---|---|
| fast/deep `_requested/_started/_completed`, `analysis_failed/cancelled/superseded` | canonical |
| `confidence_created/recalculated/superseded` | canonical |
| `finding_created/updated/closed/reopened/superseded` | canonical |
| `recommendation_created/accepted/rejected/implemented/superseded` | canonical |
| `notification_created/viewed/dismissed/expired` | canonical |
| `report_generated/published/superseded/archived`; `comment_created/mention_created/artifact_shared/share_revoked/share_expired` | canonical |

## Proposed claim & CAF attributes (NOT yet Data Model fields)

| Attribute | On | Classification |
|---|---|---|
| verbatim_span, normalized_text, modality, support_status, clarity flags, canonical_key | Claim/ContextItem | **proposal** |
| structured_proposition, relationship_links, extraction_confidence | Claim/ContextItem | **proposal** |
| evaluation_completeness, contributing_findings, direction_vs_prior, dimension_coverage | CAFState | **proposal** |

## Constants (analysis_constants.py)

| Constant group | Classification |
|---|---|
| Stage order, display names | derived |
| Time-to-First-MRI < 60s | canonical |
| All other timing targets | TBD |
| Ingestion envelope, claim counts, LLM output limits | proposal / TBD |
| Required fields, forbidden terms, TBD marker | canonical / derived |

*Every artifact in this pack carries inline `canonical`/`derived`/`proposal`/`TBD` tags; this matrix is the index.*
