from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from math import prod
from os import environ as process_environment


class FindingBasis(StrEnum):
    INFERENCE = "inference"
    STRUCTURAL = "structural"
    DECISION = "decision"
    MODEL_GAP = "model_gap"


class FindingType(StrEnum):
    INFERENCE_GAP = "inference_gap"
    FALSE_CONFIDENCE = "false_confidence"
    DEPENDENCY_MAY_FAIL = "dependency_may_fail"
    UNOWNED = "unowned"
    NO_DEADLINE = "no_deadline"
    NO_BACKUP = "no_backup"
    COVERAGE_GAP = "coverage_gap"
    METRIC_MISMATCH = "metric_mismatch"
    NO_LIMIT_SET = "no_limit_set"


class PrimaryAct(StrEnum):
    VERIFY = "verify"
    BUILD = "build"
    DECIDE = "decide"


class EscalationRoute(StrEnum):
    CLARIFY = "clarify"
    GOVERNANCE = "governance"


class StructuralTarget(StrEnum):
    DEFINITION = "definition"
    EDGE = "edge"
    ACHIEVABILITY = "achievability"
    TRUTH = "truth"
    COVERAGE = "coverage"


@dataclass(frozen=True, slots=True)
class FindingResolution:
    issue_id: str
    finding_type: FindingType
    basis: FindingBasis
    structural_target: StructuralTarget
    pillar: str
    dimension: str
    primary_act: PrimaryAct
    also_offered: tuple[PrimaryAct, ...] = ()

    @property
    def escalate(self) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class FindingEscalation:
    issue_id: str
    finding_type: str
    basis: str
    structural_target: str
    route: EscalationRoute
    reason: str
    primary_act: None = None
    dimension: None = None
    pillar: None = None
    also_offered: tuple[PrimaryAct, ...] = ()
    escalate: bool = True


@dataclass(frozen=True, slots=True)
class ActEffect:
    grounding_delta: int = 0
    viability_delta: int = 0
    adaptability_delta: int = 0


@dataclass(frozen=True, slots=True)
class PlanNode:
    id: str
    type: str
    label: str
    provenance: str
    extraction_confidence: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.extraction_confidence <= 1.0:
            raise ValueError("node extraction confidence must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class PlanEdge:
    from_id: str
    to_id: str
    rel: str
    weight: float
    extraction_confidence: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.weight <= 1.0:
            raise ValueError("edge weight must be between 0 and 1")
        if not 0.0 <= self.extraction_confidence <= 1.0:
            raise ValueError("edge extraction confidence must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class PlanDependencyGraph:
    nodes: tuple[PlanNode, ...]
    edges: tuple[PlanEdge, ...]

    def __post_init__(self) -> None:
        node_ids = {node.id for node in self.nodes}
        if len(node_ids) != len(self.nodes):
            raise ValueError("dependency graph node ids must be unique")
        for edge in self.edges:
            if edge.from_id not in node_ids or edge.to_id not in node_ids:
                raise ValueError("dependency graph edges must reference known nodes")


@dataclass(frozen=True, slots=True)
class SensitivityCandidate:
    id: str
    node_id: str
    structural_target: StructuralTarget
    favorable_integrity: float
    adverse_integrity: float
    runway_factor: float
    edge_key: tuple[str, str] | None = None
    stakes: float | None = None


@dataclass(frozen=True, slots=True)
class SensitivityTrace:
    paths: tuple[tuple[str, ...], ...]
    span_true: float
    span_false: float
    span: float
    leverage: float
    uncertainty_factor: float
    runway_factor: float
    edge_key: tuple[str, str] | None = None
    outcome_reachability: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class SensitivityRecord:
    candidate_id: str
    node_id: str
    sensitivity: float
    exposure_rank: float
    trace: SensitivityTrace
    load_bearing: bool | None = None


@dataclass(frozen=True, slots=True)
class CalibrationContext:
    domain: str | None
    stakes: float = 1.0


@dataclass(frozen=True, slots=True)
class CalibrationPolicy:
    global_threshold: float
    asymmetric_loss: float
    critical_floor: float
    surface_preference: float
    segment_thresholds: dict[str, float]
    segment_label_counts: dict[str, int]
    prior_strength: int = 20

    def __post_init__(self) -> None:
        if self.asymmetric_loss < 1.0:
            raise ValueError("asymmetric loss must be at least 1")

    def effective_threshold(self, context: CalibrationContext) -> float:
        if context.domain is None:
            return self.global_threshold

        label_count = self.segment_label_counts.get(context.domain, 0)
        segment_threshold = self.segment_thresholds.get(context.domain)
        if label_count <= 0 or segment_threshold is None:
            return self.global_threshold

        weight = label_count / (label_count + max(1, self.prior_strength))
        shrunk = (
            (self.global_threshold * (1.0 - weight))
            + (segment_threshold * weight)
        )
        return shrunk - self.surface_preference


@dataclass(frozen=True, slots=True)
class GateDecision:
    sensitivity: float
    adjusted_sensitivity: float
    effective_threshold: float
    load_bearing: bool
    critical_floor_applied: bool
    honesty_bar: str = "one_accuracy_bar"


@dataclass(frozen=True, slots=True)
class PerturbationEndpoints:
    structural_target: StructuralTarget
    favorable: str
    adverse: str
    escalate: bool = False


@dataclass(frozen=True, slots=True)
class EndpointEscalation:
    structural_target: str
    route: EscalationRoute
    reason: str
    favorable: None = None
    adverse: None = None
    escalate: bool = True


@dataclass(frozen=True, slots=True)
class RuntimeEscalation:
    issue_id: str
    route: EscalationRoute
    dimension: str
    structural_target: StructuralTarget
    primary_act: PrimaryAct
    cascade_after_resolution: bool = True


@dataclass(frozen=True, slots=True)
class UnassessedRegion:
    incomplete: bool
    blocks_sound: bool
    surfaced: bool
    band: None = None
    numeric_penalty: None = None
    graded_as_weak: bool = False
    route: EscalationRoute = EscalationRoute.GOVERNANCE


@dataclass(frozen=True, slots=True)
class DeterministicFindingTags:
    finding_type: str
    basis: FindingBasis
    structural_target: StructuralTarget


_TARGET_CLASSIFICATION: dict[StructuralTarget, tuple[str, str]] = {
    StructuralTarget.DEFINITION: ("Viability", "Clarity"),
    StructuralTarget.EDGE: ("Viability", "Alignment"),
    StructuralTarget.ACHIEVABILITY: ("Viability", "Feasibility"),
    StructuralTarget.TRUTH: ("Grounding", "Grounding"),
    StructuralTarget.COVERAGE: ("Adaptability", "Adaptability"),
}


_PERTURBATION_ENDPOINTS: dict[StructuralTarget, tuple[str, str]] = {
    StructuralTarget.TRUTH: (
        "inferred value is true",
        "inferred value is false",
    ),
    StructuralTarget.ACHIEVABILITY: (
        "constraint does not bind",
        "constraint binds",
    ),
    StructuralTarget.DEFINITION: (
        "supported favorable reading",
        "supported adverse reading",
    ),
    StructuralTarget.EDGE: (
        "segment contributes to the outcome",
        "segment is a non-contribution or off-tree",
    ),
    StructuralTarget.COVERAGE: (
        "plan adapts when conditions shift",
        "plan cannot adapt when conditions shift",
    ),
}


_DIMENSION_TARGETS: dict[str, StructuralTarget] = {
    "Clarity": StructuralTarget.DEFINITION,
    "Alignment": StructuralTarget.EDGE,
    "Feasibility": StructuralTarget.ACHIEVABILITY,
    "Grounding": StructuralTarget.TRUTH,
    "Adaptability": StructuralTarget.COVERAGE,
}


def classify_finding(
    *,
    issue_id: str,
    finding_type: FindingType,
    basis: FindingBasis,
    structural_target: StructuralTarget,
) -> FindingResolution:
    """Derive the resolution path from the finding model.

    There is intentionally no caller-authored primary-action argument.  The
    action is a deterministic consequence of the finding type and structural
    target, so persisted or generated prose cannot silently change the route.
    """

    pillar, dimension = _TARGET_CLASSIFICATION[structural_target]

    if finding_type in {
        FindingType.INFERENCE_GAP,
        FindingType.FALSE_CONFIDENCE,
        FindingType.DEPENDENCY_MAY_FAIL,
    }:
        primary_act = PrimaryAct.VERIFY
        also_offered = (PrimaryAct.BUILD,)
    elif finding_type in {
        FindingType.UNOWNED,
        FindingType.NO_DEADLINE,
        FindingType.NO_BACKUP,
        FindingType.COVERAGE_GAP,
        FindingType.METRIC_MISMATCH,
    }:
        primary_act = PrimaryAct.BUILD
        also_offered = (
            (PrimaryAct.VERIFY,)
            if finding_type in {
                FindingType.UNOWNED,
                FindingType.NO_DEADLINE,
                FindingType.NO_BACKUP,
            }
            else ()
        )
    else:
        primary_act = PrimaryAct.DECIDE
        also_offered = ()

    return FindingResolution(
        issue_id=issue_id,
        finding_type=finding_type,
        basis=basis,
        structural_target=structural_target,
        pillar=pillar,
        dimension=dimension,
        primary_act=primary_act,
        also_offered=also_offered,
    )


def classify_finding_or_escalate(
    *,
    issue_id: str,
    finding_type: str,
    basis: str,
    structural_target: str,
) -> FindingResolution | FindingEscalation:
    """Parse an external finding safely, escalating every unmapped value."""

    try:
        parsed_type = FindingType(finding_type)
        parsed_basis = FindingBasis(basis)
        parsed_target = StructuralTarget(structural_target)
    except ValueError as exc:
        is_model_gap = basis == FindingBasis.MODEL_GAP.value or "taxonomy" in str(exc)
        return FindingEscalation(
            issue_id=issue_id,
            finding_type=finding_type,
            basis=basis,
            structural_target=structural_target,
            route=(
                EscalationRoute.GOVERNANCE
                if is_model_gap
                else EscalationRoute.CLARIFY
            ),
            reason="unmapped finding model" if is_model_gap else "underspecified finding",
        )

    if parsed_basis is FindingBasis.MODEL_GAP:
        return FindingEscalation(
            issue_id=issue_id,
            finding_type=finding_type,
            basis=basis,
            structural_target=structural_target,
            route=EscalationRoute.GOVERNANCE,
            reason="model taxonomy has no ratified mapping",
        )

    return classify_finding(
        issue_id=issue_id,
        finding_type=parsed_type,
        basis=parsed_basis,
        structural_target=parsed_target,
    )


def apply_resolution_act(act: PrimaryAct) -> ActEffect:
    """Return the allowed integrity effect for an issue-closing act."""

    if act is PrimaryAct.VERIFY:
        return ActEffect(grounding_delta=1)
    if act is PrimaryAct.BUILD:
        return ActEffect(viability_delta=1, adaptability_delta=1)
    return ActEffect(viability_delta=1)


def perturbation_endpoints_or_escalate(
    structural_target: str,
) -> PerturbationEndpoints | EndpointEscalation:
    try:
        target = StructuralTarget(structural_target)
    except ValueError:
        return EndpointEscalation(
            structural_target=structural_target,
            route=EscalationRoute.GOVERNANCE,
            reason="structural target has no ratified perturbation endpoints",
        )

    favorable, adverse = _PERTURBATION_ENDPOINTS[target]
    return PerturbationEndpoints(
        structural_target=target,
        favorable=favorable,
        adverse=adverse,
    )


def route_runtime_escalation(
    *,
    issue_id: str,
    target_identity_known: bool,
) -> RuntimeEscalation:
    if not target_identity_known:
        return RuntimeEscalation(
            issue_id=issue_id,
            route=EscalationRoute.CLARIFY,
            dimension="Clarity",
            structural_target=StructuralTarget.DEFINITION,
            primary_act=PrimaryAct.VERIFY,
        )
    return RuntimeEscalation(
        issue_id=issue_id,
        route=EscalationRoute.CLARIFY,
        dimension="Alignment",
        structural_target=StructuralTarget.EDGE,
        primary_act=PrimaryAct.DECIDE,
    )


def assess_unassessed_region(*, load_bearing: bool) -> UnassessedRegion:
    """Represent a known-unknown without converting uncertainty into weakness."""

    return UnassessedRegion(
        incomplete=load_bearing,
        blocks_sound=load_bearing,
        surfaced=load_bearing,
    )


def deterministic_finding_tags(
    *,
    dimension: str,
    title: str,
    recommendation: str,
) -> DeterministicFindingTags:
    """Classify deterministic-harness rules without a silent catch-all."""

    try:
        target = _DIMENSION_TARGETS[dimension]
    except KeyError as exc:
        raise ValueError(f"unmapped deterministic dimension: {dimension}") from exc
    text = f"{title} {recommendation}".casefold()
    if "checkpoint" in text:
        return DeterministicFindingTags(
            FindingType.COVERAGE_GAP.value,
            FindingBasis.STRUCTURAL,
            StructuralTarget.COVERAGE,
        )
    if any(term in text for term in ("owner", "accountable")):
        finding_type = FindingType.UNOWNED
        basis = FindingBasis.STRUCTURAL
    elif any(term in text for term in ("backup", "fallback")):
        finding_type = FindingType.NO_BACKUP
        basis = FindingBasis.STRUCTURAL
    elif any(term in text for term in ("deadline", "milestone date", "timing")):
        finding_type = FindingType.NO_DEADLINE
        basis = FindingBasis.STRUCTURAL
    elif any(
        term in text
        for term in ("metric", "measure", "baseline", "target", "missing a unit")
    ):
        finding_type = FindingType.METRIC_MISMATCH
        basis = FindingBasis.STRUCTURAL
    elif any(term in text for term in ("tradeoff", "trade-off", "limit set")):
        finding_type = FindingType.NO_LIMIT_SET
        basis = FindingBasis.DECISION
    elif any(
        term in text
        for term in ("dependency", "capacity", "vendor", "contract", "access")
    ):
        finding_type = FindingType.DEPENDENCY_MAY_FAIL
        basis = FindingBasis.INFERENCE
    else:
        return DeterministicFindingTags(
            "unmapped_deterministic_finding",
            FindingBasis.MODEL_GAP,
            target,
        )
    return DeterministicFindingTags(finding_type.value, basis, target)


def evaluate_sensitivity(
    *,
    graph: PlanDependencyGraph,
    candidate: SensitivityCandidate,
) -> SensitivityRecord:
    """Evaluate a candidate using only deterministic graph inputs.

    The score combines the two-sided integrity span with weighted structural
    leverage, extraction uncertainty, and execution runway.  Every component
    is retained in the returned trace.
    """

    node_by_id = {node.id: node for node in graph.nodes}
    if candidate.node_id not in node_by_id:
        raise ValueError(f"unknown sensitivity candidate node: {candidate.node_id}")

    edge_by_key = {(edge.from_id, edge.to_id): edge for edge in graph.edges}
    if candidate.structural_target is StructuralTarget.EDGE:
        if candidate.edge_key is None or candidate.edge_key not in edge_by_key:
            raise ValueError("alignment sensitivity requires a known edge key")
        start_id = candidate.edge_key[1]
        suffixes = _paths_to_outcomes(graph=graph, start_id=start_id)
        paths = tuple((candidate.edge_key[0], *path) for path in suffixes)
    else:
        paths = _paths_to_outcomes(graph=graph, start_id=candidate.node_id)

    leverage = sum(_path_weight(path=path, edges=edge_by_key) for path in paths)
    confidence_values = [node_by_id[candidate.node_id].extraction_confidence]
    for path in paths:
        confidence_values.extend(
            edge_by_key[(from_id, to_id)].extraction_confidence
            for from_id, to_id in zip(path, path[1:], strict=False)
        )
    uncertainty_factor = 1.0 + (1.0 - min(confidence_values))
    span = abs(candidate.favorable_integrity - candidate.adverse_integrity)
    sensitivity = span * leverage * uncertainty_factor * candidate.runway_factor
    outcome_ids = {node.id for node in graph.nodes if node.type == "outcome"}
    outcome_reachability = tuple(
        sorted({path[-1] for path in paths if path and path[-1] in outcome_ids})
    )
    trace = SensitivityTrace(
        paths=paths,
        span_true=candidate.favorable_integrity,
        span_false=candidate.adverse_integrity,
        span=span,
        leverage=leverage,
        uncertainty_factor=uncertainty_factor,
        runway_factor=candidate.runway_factor,
        edge_key=candidate.edge_key,
        outcome_reachability=outcome_reachability,
    )
    return SensitivityRecord(
        candidate_id=candidate.id,
        node_id=candidate.node_id,
        sensitivity=sensitivity,
        exposure_rank=sensitivity,
        trace=trace,
    )


def gate_sensitivity(
    *,
    sensitivity: float,
    policy: CalibrationPolicy,
    context: CalibrationContext,
) -> GateDecision:
    effective_threshold = policy.effective_threshold(context)
    loss_multiplier = 1.0 + max(0.0, policy.asymmetric_loss - 1.0) * max(
        0.0, context.stakes
    )
    adjusted_sensitivity = sensitivity * loss_multiplier
    critical_floor_applied = sensitivity >= policy.critical_floor
    return GateDecision(
        sensitivity=sensitivity,
        adjusted_sensitivity=adjusted_sensitivity,
        effective_threshold=effective_threshold,
        load_bearing=(
            critical_floor_applied or adjusted_sensitivity >= effective_threshold
        ),
        critical_floor_applied=critical_floor_applied,
    )


def calibration_policy_from_environment(
    values: Mapping[str, str] | None = None,
) -> CalibrationPolicy | None:
    """Load owner calibration only when the complete locked set is present."""

    source = process_environment if values is None else values
    names = (
        "LB_THRESHOLD",
        "LB_ASYMMETRIC_LOSS",
        "LB_CRITICAL_FLOOR",
        "LB_SURFACE_PREF",
    )
    if any(not source.get(name, "").strip() for name in names):
        return None
    return CalibrationPolicy(
        global_threshold=float(source["LB_THRESHOLD"]),
        asymmetric_loss=float(source["LB_ASYMMETRIC_LOSS"]),
        critical_floor=float(source["LB_CRITICAL_FLOOR"]),
        surface_preference=float(source["LB_SURFACE_PREF"]),
        segment_thresholds={},
        segment_label_counts={},
    )


def _paths_to_outcomes(
    *,
    graph: PlanDependencyGraph,
    start_id: str,
) -> tuple[tuple[str, ...], ...]:
    node_by_id = {node.id: node for node in graph.nodes}
    adjacency: dict[str, list[str]] = {}
    for edge in graph.edges:
        adjacency.setdefault(edge.from_id, []).append(edge.to_id)
    for destinations in adjacency.values():
        destinations.sort()

    paths: list[tuple[str, ...]] = []

    def walk(current_id: str, path: tuple[str, ...]) -> None:
        if node_by_id[current_id].type == "outcome":
            paths.append(path)
            return
        for destination in adjacency.get(current_id, []):
            if destination in path:
                continue
            walk(destination, (*path, destination))

    walk(start_id, (start_id,))
    return tuple(sorted(paths))


def _path_weight(
    *,
    path: tuple[str, ...],
    edges: dict[tuple[str, str], PlanEdge],
) -> float:
    return prod(
        edges[(from_id, to_id)].weight
        for from_id, to_id in zip(path, path[1:], strict=False)
    )
