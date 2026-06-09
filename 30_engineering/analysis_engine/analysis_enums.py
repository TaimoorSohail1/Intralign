"""
analysis_enums.py — OSLO Release 1 Fast/Deep Analysis workflow enums.

Status: Active Architecture V1. Non-canonical pack; subject to owner governance review.
Authority order: Planning Intelligence > State Model > Event Model > Data Model v1.1 >
                 Analysis Engine > NFR > API/UI/Testing > Supporting models > Proposal notes.

Traceability tags (in comments): canonical | derived | proposal | TBD
  canonical = value defined in an authoritative spec (Data/State/Event Model, CAF/Reliability/Confidence)
  derived   = entailed by an authoritative spec
  proposal  = recommended by this pack, pending owner ratification
  TBD       = TBD - Owner Decision Required

These enums introduce NO new states, events, or entities beyond the authoritative models.
No formulas, weights, percentages, or thresholds are encoded anywhere.
"""

from enum import Enum


class StrEnum(str, Enum):
    """String enum: members are usable as plain strings (JSON/DB friendly)."""

    def __str__(self) -> str:  # pragma: no cover
        return self.value


# --- Pass type -------------------------------------------------------------- canonical (Data Model v1.1: AnalysisRun.run_type)
class PassType(StrEnum):
    FAST_ANALYSIS_PASS = "fast_analysis_pass"   # canonical
    DEEP_ANALYSIS_PASS = "deep_analysis_pass"   # canonical


# --- Stages ----------------------------------------------------------------- derived (Engine §9/§10; this pack's stage I/O specs)
class FastStage(StrEnum):
    INTAKE_ACQUISITION = "fast_0_intake_acquisition"        # canonical
    NORMALIZATION = "fast_1_normalization"                  # canonical
    GLOBAL_SKELETON = "fast_2_global_skeleton"              # proposal
    CLAIM_EXTRACTION = "fast_3_claim_extraction"            # canonical
    CAF_EVALUATION = "fast_4_caf_evaluation"                # canonical
    FINDING_GENERATION = "fast_5_finding_generation"        # canonical
    RECOMMENDATION_GENERATION = "fast_6_recommendation_generation"  # canonical
    CONFIDENCE_AND_STATE = "fast_7_confidence_and_state"    # canonical
    MRI_AND_PUBLICATION = "fast_8_mri_and_publication"      # canonical


class DeepStage(StrEnum):
    CONTEXT_EXPANSION = "deep_1_context_expansion"          # canonical
    RELATIONSHIP_EXPANSION = "deep_2_relationship_expansion"  # canonical
    ASSUMPTION_EXPANSION = "deep_3_assumption_expansion"    # canonical
    CONFLICT_DISCOVERY = "deep_4_conflict_discovery"        # canonical
    ADDITIONAL_CLAIM_DISCOVERY = "deep_5_additional_claim_discovery"  # canonical
    CAF_REASSESSMENT = "deep_6_caf_reassessment"            # canonical
    CONFIDENCE_RECALCULATION = "deep_7_confidence_recalculation"  # canonical
    EXPANDED_FINDINGS = "deep_8_expanded_findings"          # canonical
    EXPANDED_RECOMMENDATIONS = "deep_9_expanded_recommendations"  # canonical
    PUBLICATION_SUPERSESSION = "deep_10_publication_supersession"  # canonical


# --- Execution type --------------------------------------------------------- derived (RULE_LLM_GUIDELINES)
class ExecutionType(StrEnum):
    RULE = "rule"      # deterministic, no LLM
    LLM = "llm"        # LLM-driven
    HYBRID = "hybrid"  # rule + LLM


# --- CAF dimensions --------------------------------------------------------- canonical (CAF Assessment Model §3)
class CAFDimension(StrEnum):
    CLARITY = "clarity"
    ALIGNMENT = "alignment"
    FEASIBILITY = "feasibility"


# --- Finding type ----------------------------------------------------------- canonical (Finding Model / Data Model §11)
class FindingType(StrEnum):
    MISSING_INFORMATION = "missing_information"
    AMBIGUITY = "ambiguity"
    ASSUMPTION = "assumption"
    INFERENCE = "inference"
    CONFLICT = "conflict"
    CONSTRAINT = "constraint"
    COVERAGE_GAP = "coverage_gap"


class FindingSeverity(StrEnum):  # canonical labels; assignment basis = TBD
    CRITICAL = "critical"
    MODERATE = "moderate"
    WARNING = "warning"


# --- Recommendation type ---------------------------------------------------- canonical (Recommendation Model / Data Model §12)
class RecommendationType(StrEnum):
    IMPROVEMENT = "improvement"
    VALIDATION = "validation"
    SUGGESTED_FIX = "suggested_fix"


# --- Reliability ------------------------------------------------------------ canonical qualitative (Reliability Model); numeric scale = TBD
class ReliabilityLevel(StrEnum):
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"


class ReliabilityInput(StrEnum):  # canonical (Reliability Model §6)
    COVERAGE = "coverage"
    EVIDENCE_AVAILABILITY = "evidence_availability"
    ASSESSABILITY = "assessability"


# --- Confidence band -------------------------------------------------------- canonical (Data Model §10 ConfidenceState.confidence_band)
class ConfidenceBand(StrEnum):
    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


# --- Statuses (Data Model v1.1 / State Model) ------------------------------- canonical
class ProjectLifecycleState(StrEnum):
    CREATED = "created"
    ORIENTING = "orienting"
    ORIENTED = "oriented"
    DEEP_ANALYZING = "deep_analyzing"
    ANALYZED = "analyzed"
    ARCHIVED = "archived"


class RunStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"   # canonical via Patch-001
    SUPERSEDED = "superseded"


class FindingStatus(StrEnum):  # canonical (v1.1 reconciled, R-1)
    DETECTED = "detected"
    ACKNOWLEDGED = "acknowledged"
    ADDRESSED = "addressed"
    CLOSED = "closed"
    REOPENED = "reopened"
    SUPERSEDED = "superseded"


class RecommendationStatus(StrEnum):  # canonical (v1.1 reconciled, R-2)
    GENERATED = "generated"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    IMPLEMENTED = "implemented"
    SUPERSEDED = "superseded"


class NotificationState(StrEnum):  # canonical (v1.1 reconciled, R-4)
    CREATED = "created"
    VIEWED = "viewed"
    DISMISSED = "dismissed"
    EXPIRED = "expired"
    # NOTE: 'delivered' intentionally NOT present — deferred until delivery-channel
    # semantics exist (Patch-001 / OPEN_DECISIONS OD-22). TBD - Owner Decision Required.


class ReportStatus(StrEnum):  # canonical (v1.1 added, R-5)
    DRAFT = "draft"
    PUBLISHED = "published"
    SUPERSEDED = "superseded"
    ARCHIVED = "archived"


class SharedArtifactStatus(StrEnum):  # canonical (v1.1 added, R-6)
    CREATED = "created"
    SHARED = "shared"
    VIEWED = "viewed"
    REVOKED = "revoked"
    EXPIRED = "expired"


# --- Source / support types ------------------------------------------------- canonical (Data Model §9) / proposal (support_status)
class EvidenceSourceType(StrEnum):  # canonical (Evidence.source_type)
    FREE_TEXT = "free_text"
    UPLOADED_DOCUMENT = "uploaded_document"
    STRUCTURED_INPUT = "structured_input"
    IMPORTED_CONTENT = "imported_content"


class ContextItemType(StrEnum):  # canonical (ContextItem.item_type)
    CLAIM = "claim"
    ASSUMPTION = "assumption"
    RELATIONSHIP = "relationship"
    ENTITY = "entity"
    METRIC = "metric"
    INTERPRETATION = "interpretation"


class ExtractionHorizon(StrEnum):  # canonical (ContextItem.extraction_horizon)
    FAST = "fast"
    DEEP = "deep"


class ClaimModality(StrEnum):  # proposal (claim attribute)
    MUST = "must"
    SHOULD = "should"
    MAY = "may"
    DESCRIPTIVE = "descriptive"


class SupportStatus(StrEnum):  # proposal (claim attribute; not yet a Data Model field)
    EVIDENCE_BACKED = "evidence_backed"
    ASSERTED_WITHOUT_SUPPORT = "asserted_without_support"
    INFERRED = "inferred"


# --- Traceability confidence ------------------------------------------------ proposal (extraction confidence band)
class TraceabilityConfidence(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# --- Source classification (for traceability tagging) ----------------------- derived (this pack's tagging scheme)
class SourceClassification(StrEnum):
    CANONICAL = "canonical"
    DERIVED = "derived"
    PROPOSAL = "proposal"
    TBD = "TBD - Owner Decision Required"
