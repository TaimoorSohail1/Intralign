"""
analysis_contracts.py — OSLO Release 1 Fast/Deep Analysis workflow data contracts.

Status: Active Architecture V1. Non-canonical pack; subject to owner governance review.

Implementation choice: stdlib dataclasses (no third-party dependency). If your codebase
uses Pydantic, these map 1:1 to BaseModel classes.

Traceability: each class/field is tagged in comments as canonical | derived | proposal | TBD.
Contracts encode NO formulas/weights/percentages/thresholds. Confidence is always
reliability-qualified. Findings are descriptive; recommendations are advisory.
Every claim/finding requires a resolvable source span (explainability to basis).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .analysis_enums import (
    PassType,
    CAFDimension,
    FindingType,
    FindingSeverity,
    RecommendationType,
    ReliabilityLevel,
    ReliabilityInput,
    ConfidenceBand,
    RunStatus,
    FindingStatus,
    RecommendationStatus,
    EvidenceSourceType,
    ContextItemType,
    ExtractionHorizon,
    ClaimModality,
    SupportStatus,
    TraceabilityConfidence,
    SourceClassification,
)


# === Evidence & source spans ================================================
@dataclass
class EvidenceRef:  # canonical (Data Model §9 Evidence)
    evidence_id: str                      # canonical
    project_id: str                       # canonical
    source_type: EvidenceSourceType       # canonical
    content_ref: str                      # canonical
    provenance: dict = field(default_factory=dict)  # canonical


@dataclass
class SourceSpan:  # canonical requirement (Engine §21 traceability); span fields = derived
    evidence_id: str                      # canonical (links to Evidence)
    start_offset: int                     # derived
    end_offset: int                       # derived
    verbatim_quote: Optional[str] = None  # proposal (claim attribute)


# === Claim (ContextItem of type 'claim') ====================================
@dataclass
class Claim:
    # Canonical ContextItem fields (Data Model §9)
    context_item_id: str                              # canonical
    project_id: str                                   # canonical
    produced_by_run_id: str                           # canonical
    item_type: ContextItemType = ContextItemType.CLAIM  # canonical
    extraction_horizon: ExtractionHorizon = ExtractionHorizon.FAST  # canonical
    evidence_id: Optional[str] = None                 # canonical (nullable)
    source_attribution: dict = field(default_factory=dict)  # canonical
    # Proposed claim attributes (NOT yet Data Model fields — OD-15)
    source_span: Optional[SourceSpan] = None          # proposal (required at runtime)
    normalized_text: Optional[str] = None             # proposal
    modality: Optional[ClaimModality] = None          # proposal
    support_status: Optional[SupportStatus] = None    # proposal
    is_measurable: Optional[bool] = None              # proposal (Clarity, rule-derivable)
    vagueness_flags: list = field(default_factory=list)  # proposal (Clarity)
    canonical_key: Optional[str] = None               # proposal (dedup/determinism)
    structured_proposition: Optional[dict] = None     # proposal
    referenced_entities: list = field(default_factory=list)  # proposal
    relationship_links: list = field(default_factory=list)   # proposal (enriched in Deep)
    affected_dimension_hint: Optional[CAFDimension] = None    # proposal
    extraction_confidence: Optional[TraceabilityConfidence] = None  # proposal


# === CAF assessment (CAFState) ==============================================
@dataclass
class CAFDimensionAssessment:
    dimension: CAFDimension                # canonical
    assessed_level: str                    # canonical value; SCALE = TBD (OD-6) — no formula
    reliability: ReliabilityLevel          # canonical qualitative (Reliability Model)
    # Proposed CAFState attributes (OD-16)
    evaluation_completeness: Optional[str] = None  # proposal ("full" | "preliminary")
    contributing_findings: list = field(default_factory=list)  # proposal (finding_ids)
    direction_vs_prior: Optional[str] = None       # proposal ("improved"|"declined"|"stable")


@dataclass
class CAFAssessment:  # canonical (Data Model §10 CAFState)
    caf_state_id: str                      # canonical
    analysis_run_id: str                   # canonical
    project_id: str                        # canonical
    clarity: CAFDimensionAssessment        # canonical
    alignment: CAFDimensionAssessment      # canonical
    feasibility: CAFDimensionAssessment    # canonical
    dimension_coverage: Optional[str] = None  # proposal (OD-16)
    # NOTE: there is intentionally NO composite CAF score field — summarization into
    # Outcome Confidence is the ConfidenceState's job (Confidence Model).  # canonical discipline


# === Reliability basis (explanation) ========================================
@dataclass
class ReliabilityBasis:  # canonical (Reliability Model §6/§11) — qualitative, no numeric scale (TBD)
    level: ReliabilityLevel                # canonical
    coverage: ReliabilityLevel             # canonical (ReliabilityInput.COVERAGE)
    evidence_availability: ReliabilityLevel  # canonical
    assessability: ReliabilityLevel        # canonical
    change_attribution: Optional[str] = None  # canonical (what last moved reliability)
    inputs_considered: list = field(
        default_factory=lambda: [
            ReliabilityInput.COVERAGE,
            ReliabilityInput.EVIDENCE_AVAILABILITY,
            ReliabilityInput.ASSESSABILITY,
        ]
    )  # canonical


# === Finding (descriptive) ==================================================
@dataclass
class Finding:  # canonical (Data Model §11 / Finding Model)
    finding_id: str                        # canonical
    project_id: str                        # canonical
    first_seen_run_id: str                 # canonical (deep ⇒ Expanded Finding)
    finding_type: FindingType              # canonical
    affected_dimensions: list              # canonical (list[CAFDimension])
    severity: FindingSeverity              # canonical (assignment basis = TBD, OD-14)
    status: FindingStatus = FindingStatus.DETECTED  # canonical
    evidence_links: list = field(default_factory=list)  # canonical (required, >=1)
    source_spans: list = field(default_factory=list)    # canonical requirement
    last_updated_run_id: Optional[str] = None           # canonical
    superseded_by_finding_id: Optional[str] = None      # canonical (supersession)
    description: Optional[str] = None       # canonical — DESCRIPTIVE only, never prescriptive


# === Recommendation (advisory) ==============================================
@dataclass
class Recommendation:  # canonical (Data Model §12 / Recommendation Model)
    recommendation_id: str                 # canonical
    project_id: str                        # canonical
    finding_id: str                        # canonical (always tied to a finding)
    first_seen_run_id: str                 # canonical (deep ⇒ Expanded Recommendation)
    recommendation_type: RecommendationType  # canonical
    status: RecommendationStatus = RecommendationStatus.GENERATED  # canonical
    rationale: Optional[str] = None        # canonical (basis)
    expected_dimension: Optional[CAFDimension] = None  # canonical
    superseded_by_recommendation_id: Optional[str] = None  # canonical


# === Confidence state =======================================================
@dataclass
class ConfidenceState:  # canonical (Data Model §10 / Confidence Model)
    confidence_state_id: str               # canonical
    analysis_run_id: str                   # canonical
    project_id: str                        # canonical
    outcome_confidence_value: str          # canonical value; SCALE = TBD (OD-7) — no formula
    confidence_band: ConfidenceBand        # canonical
    reliability_qualifier: ReliabilityLevel  # canonical — confidence is NEVER bare
    reliability_basis: Optional[ReliabilityBasis] = None  # canonical (explanation)
    supersedes_confidence_state_id: Optional[str] = None  # canonical (recalculation chain)


# === Traceability link ======================================================
@dataclass
class TraceabilityLink:  # derived (Engine §21: input → reasoning → finding → recommendation → confidence)
    from_id: str                           # derived
    from_kind: str                         # derived (e.g., "evidence", "claim", "finding")
    to_id: str                             # derived
    to_kind: str                           # derived
    classification: SourceClassification = SourceClassification.DERIVED  # derived


# === Stage input / output ===================================================
@dataclass
class StageInput:  # derived (pack stage I/O specs)
    pass_type: PassType                    # canonical
    stage: str                             # canonical (FastStage|DeepStage value)
    project_id: str                        # canonical
    analysis_run_id: str                   # canonical
    payload: dict = field(default_factory=dict)  # derived


@dataclass
class StageOutput:  # derived
    pass_type: PassType                    # canonical
    stage: str                             # canonical
    analysis_run_id: str                   # canonical
    produced: dict = field(default_factory=dict)  # derived (entity ids produced)
    events_emitted: list = field(default_factory=list)   # canonical (Event Model names only)
    state_transitions: list = field(default_factory=list)  # canonical
    ok: bool = True                        # derived
    notes: Optional[str] = None            # derived


# === Run contracts ==========================================================
@dataclass
class FastRun:  # canonical (AnalysisRun, run_type=fast_analysis_pass)
    analysis_run_id: str                   # canonical
    project_id: str                        # canonical
    run_status: RunStatus = RunStatus.QUEUED  # canonical
    pass_type: PassType = PassType.FAST_ANALYSIS_PASS  # canonical
    trigger_source: Optional[str] = None   # canonical
    previous_run_id: Optional[str] = None  # canonical
    caf_state_id: Optional[str] = None     # canonical (1:1)
    confidence_state_id: Optional[str] = None  # canonical (1:1)
    mri_snapshot_id: Optional[str] = None  # canonical
    model_config_ref: Optional[str] = None  # derived (determinism: pinned config — Engine §15)


@dataclass
class DeepRun:  # canonical (AnalysisRun, run_type=deep_analysis_pass)
    analysis_run_id: str                   # canonical
    project_id: str                        # canonical
    run_status: RunStatus = RunStatus.QUEUED  # canonical
    pass_type: PassType = PassType.DEEP_ANALYSIS_PASS  # canonical
    trigger_source: Optional[str] = None   # canonical
    previous_run_id: Optional[str] = None  # canonical (chains fast→deep→deep)
    caf_state_id: Optional[str] = None     # canonical
    confidence_state_id: Optional[str] = None  # canonical
    supersedes_run_id: Optional[str] = None    # canonical (prior current run)
    model_config_ref: Optional[str] = None     # derived


# === Validation result ======================================================
@dataclass
class ValidationIssue:  # derived
    code: str                              # derived
    message: str                           # derived
    severity: str = "error"                # derived ("error" | "warning")


@dataclass
class ValidationResult:  # derived (RULE_LLM_GUIDELINES §4 schema validation)
    ok: bool = True
    issues: list = field(default_factory=list)  # list[ValidationIssue]

    def add(self, code: str, message: str, severity: str = "error") -> None:
        self.issues.append(ValidationIssue(code=code, message=message, severity=severity))
        if severity == "error":
            self.ok = False


# === Minimal validators (deterministic, rule-based) =========================
def validate_finding_descriptive(f: Finding) -> ValidationResult:
    """A Finding must be descriptive and basis-linked (canonical invariants)."""
    r = ValidationResult()
    if not f.evidence_links:
        r.add("FIND_NO_BASIS", "Finding must link to >=1 evidence/claim (explainability).")
    if not f.source_spans:
        r.add("FIND_NO_SPAN", "Finding must carry a resolvable source span.")
    return r


def validate_recommendation_advisory(rec: Recommendation) -> ValidationResult:
    """A Recommendation must be advisory and tied to a finding (canonical invariants)."""
    r = ValidationResult()
    if not rec.finding_id:
        r.add("REC_NO_FINDING", "Recommendation must reference a finding_id.")
    return r


def validate_confidence_not_bare(c: ConfidenceState) -> ValidationResult:
    """Confidence must be reliability-qualified, never bare (Confidence/Reliability models)."""
    r = ValidationResult()
    if c.reliability_qualifier is None:
        r.add("CONF_BARE", "Confidence must be reliability-qualified (never bare).")
    return r


def validate_claim_has_span(c: Claim) -> ValidationResult:
    """Every claim must carry a resolvable source span (canonical traceability)."""
    r = ValidationResult()
    if c.source_span is None and not c.source_attribution:
        r.add("CLAIM_NO_SPAN", "Claim must carry a resolvable source span / attribution.")
    return r
