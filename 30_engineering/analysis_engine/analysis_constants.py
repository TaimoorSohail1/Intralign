"""
analysis_constants.py — OSLO Release 1 Fast/Deep Analysis workflow constants.

Status: Active Architecture V1. Non-canonical pack; subject to owner governance review.

Traceability: every constant is tagged in a comment as
  canonical | derived | proposal | TBD - Owner Decision Required

IMPORTANT:
  * The ONLY owner-approved numeric performance target is TIME_TO_FIRST_MRI_SECONDS = 60 (canonical).
  * All other timing/size/count values are PROPOSAL or TBD and are clearly marked.
  * No formulas, weights, percentages, or thresholds for CAF/Reliability/Confidence appear here.
"""

from .analysis_enums import (  # noqa: F401  (import style adjust to your package layout)
    FastStage,
    DeepStage,
    CAFDimension,
    PassType,
)

# Marker string for any unresolved owner decision. ---------------------------- canonical (pack convention)
TBD = "TBD - Owner Decision Required"


# === Stage order ============================================================ derived (Engine §9/§10; pack stage I/O specs)
FAST_STAGE_ORDER = [
    FastStage.INTAKE_ACQUISITION,
    FastStage.NORMALIZATION,
    FastStage.GLOBAL_SKELETON,          # proposal stage
    FastStage.CLAIM_EXTRACTION,
    FastStage.CAF_EVALUATION,
    FastStage.FINDING_GENERATION,
    FastStage.RECOMMENDATION_GENERATION,
    FastStage.CONFIDENCE_AND_STATE,
    FastStage.MRI_AND_PUBLICATION,
]

DEEP_STAGE_ORDER = [
    DeepStage.CONTEXT_EXPANSION,
    DeepStage.RELATIONSHIP_EXPANSION,
    DeepStage.ASSUMPTION_EXPANSION,
    DeepStage.CONFLICT_DISCOVERY,
    DeepStage.ADDITIONAL_CLAIM_DISCOVERY,
    DeepStage.CAF_REASSESSMENT,
    DeepStage.CONFIDENCE_RECALCULATION,
    DeepStage.EXPANDED_FINDINGS,
    DeepStage.EXPANDED_RECOMMENDATIONS,
    DeepStage.PUBLICATION_SUPERSESSION,
]


# === Display names ========================================================== derived
FAST_STAGE_DISPLAY_NAMES = {
    FastStage.INTAKE_ACQUISITION: "Intake & Acquisition",
    FastStage.NORMALIZATION: "Normalization",
    FastStage.GLOBAL_SKELETON: "Global Skeleton",
    FastStage.CLAIM_EXTRACTION: "Claim Extraction",
    FastStage.CAF_EVALUATION: "CAF Evaluation",
    FastStage.FINDING_GENERATION: "Finding Generation",
    FastStage.RECOMMENDATION_GENERATION: "Recommendation Generation",
    FastStage.CONFIDENCE_AND_STATE: "Confidence & State",
    FastStage.MRI_AND_PUBLICATION: "MRI & Publication",
}

DEEP_STAGE_DISPLAY_NAMES = {
    DeepStage.CONTEXT_EXPANSION: "Context Expansion",
    DeepStage.RELATIONSHIP_EXPANSION: "Relationship Expansion",
    DeepStage.ASSUMPTION_EXPANSION: "Assumption Expansion",
    DeepStage.CONFLICT_DISCOVERY: "Conflict Discovery",
    DeepStage.ADDITIONAL_CLAIM_DISCOVERY: "Additional Claim Discovery",
    DeepStage.CAF_REASSESSMENT: "CAF Reassessment",
    DeepStage.CONFIDENCE_RECALCULATION: "Confidence Recalculation",
    DeepStage.EXPANDED_FINDINGS: "Expanded Findings",
    DeepStage.EXPANDED_RECOMMENDATIONS: "Expanded Recommendations",
    DeepStage.PUBLICATION_SUPERSESSION: "Publication & Supersession",
}


# === Timing targets ========================================================= MIXED — see tags
# CANONICAL: the 60-second orientation target (NFR §3 / Master Spec §20 / M1).
TIME_TO_FIRST_MRI_SECONDS = 60  # canonical

# PROPOSAL: per-stage Fast budget (seconds). Load-test pending. NOT approved.
FAST_STAGE_BUDGET_SECONDS_PROPOSAL = {  # proposal
    FastStage.INTAKE_ACQUISITION: (2, 4),
    FastStage.NORMALIZATION: (2, 3),
    FastStage.GLOBAL_SKELETON: (8, 10),
    FastStage.CLAIM_EXTRACTION: (12, 17),
    FastStage.CAF_EVALUATION: (10, 14),       # overlaps claim extraction
    FastStage.FINDING_GENERATION: (1, 1),
    FastStage.RECOMMENDATION_GENERATION: (4, 6),
    FastStage.CONFIDENCE_AND_STATE: (1, 3),
    FastStage.MRI_AND_PUBLICATION: (3, 5),
}

# Deep Pass timing — no approved targets exist.
DEEP_PASS_COMPLETION_TARGET_SECONDS = TBD     # TBD (NFR §4)
DEEP_PASS_TIMEOUT_SECONDS = TBD               # TBD (NFR §4)
DEEP_DEBOUNCE_COALESCE_WINDOW_SECONDS = TBD   # TBD (Event Model §15)

# Other NFR latency targets — undefined upstream.
API_READ_LATENCY_TARGET = TBD                 # TBD
API_WRITE_LATENCY_TARGET = TBD                # TBD
NOTIFICATION_LATENCY_TARGET = TBD             # TBD
REPORT_GENERATION_LATENCY_TARGET = TBD        # TBD


# === Proposed limits (NOT approved) ========================================= proposal / TBD
INGESTION_ENVELOPE_TOKENS_PROPOSAL = 20_000   # proposal (Fast design point) — OD-2
INGESTION_HARD_CEILING_TOKENS_PROPOSAL = 33_000  # proposal (Fast ceiling) — OD-2
FAST_CLAIM_COUNT_TARGET_PROPOSAL = (50, 100)  # proposal (salient subset) — OD-3
DEEP_CLAIM_COUNT_ESTIMATE_PROPOSAL = (350, 850)  # proposal (informational) — OD-4
PER_CLAIM_OUTPUT_TOKENS_ESTIMATE_PROPOSAL = 50   # proposal — OD-5
LLM_OUTPUT_TOKEN_LIMIT_PER_CALL = TBD         # TBD — OD-5
LLM_RETRY_LIMIT = TBD                          # TBD — OD-11
RUN_RETRY_LIMIT = TBD                          # TBD — OD-11
BOUNDED_EQUIVALENCE_TOLERANCE = TBD           # TBD — OD-12 (Engine §15)

# Model tiering (proposal): which tier handles which work.
MODEL_TIER_PROPOSAL = {  # proposal — OD-1
    "extraction": "fast_tier",          # claim extraction, global skeleton
    "relational_reasoning": "frontier", # alignment/feasibility, conflict discovery
    "rationale": "fast_tier",
}


# === Required fields per produced entity ==================================== canonical (Data Model v1.1)
REQUIRED_FIELDS = {  # canonical
    "Evidence": ["evidence_id", "project_id", "source_type", "content_ref", "provenance"],
    "ContextItem": [
        "context_item_id", "project_id", "item_type",
        "extraction_horizon", "produced_by_run_id", "content", "source_attribution",
    ],
    "AnalysisRun": [
        "analysis_run_id", "project_id", "run_type", "run_status", "trigger_source",
    ],
    "CAFState": [
        "caf_state_id", "analysis_run_id", "project_id",
        "clarity_index", "alignment_index", "feasibility_index",
        "clarity_reliability", "alignment_reliability", "feasibility_reliability",
    ],
    "ConfidenceState": [
        "confidence_state_id", "analysis_run_id", "project_id",
        "outcome_confidence_value", "confidence_band", "reliability_qualifier",
    ],
    "Finding": [
        "finding_id", "project_id", "first_seen_run_id", "finding_type",
        "affected_dimensions", "severity", "status", "evidence_links",
    ],
    "Recommendation": [
        "recommendation_id", "project_id", "finding_id", "first_seen_run_id",
        "recommendation_type", "status", "rationale", "expected_dimension",
    ],
}

# PROPOSED additional fields (not yet in the Data Model) — OD-15 / OD-16.
PROPOSED_CLAIM_FIELDS = [  # proposal
    "verbatim_span", "normalized_text", "modality", "support_status",
    "is_measurable", "vagueness_flags", "dedup_key",
    "structured_proposition", "relationship_links", "extraction_confidence",
]
PROPOSED_CAF_STATE_FIELDS = [  # proposal
    "evaluation_completeness", "contributing_findings",
    "direction_vs_prior", "dimension_coverage",
]


# === Forbidden terms (scope guardrails) ===================================== canonical (SCOPE_GUARDRAILS)
# Presence of any of these in produced content/behavior is a scope violation.
FORBIDDEN_TERMS = [  # canonical
    "governance_domain",
    "resolution_candidate",
    "review_request",
    "disposition",
    "governance",
    "accepted_understanding",
    "agent_governance",
    "autonomous_execution",
    "actuation",
    "outcome_orchestration",
    "execution_intelligence",
]

# Forbidden mechanics: confidence/CAF/reliability must NOT use these. ---------- canonical
FORBIDDEN_MECHANICS = ["formula", "weight", "percentage", "threshold"]  # canonical

# Required affirmations (must hold for every run). --------------------------- canonical
INVARIANTS = [  # canonical
    "findings_are_descriptive",
    "recommendations_are_advisory",
    "confidence_derived_from_caf_and_reliability",
    "confidence_never_bare",
    "prior_outputs_superseded_not_deleted",
    "fast_output_is_not_final",
    "user_retains_authority",
    "atomic_publication",
    "deterministic_under_pinned_config",
    "replayable",
    "tenant_isolated_by_workspace_id",
]
