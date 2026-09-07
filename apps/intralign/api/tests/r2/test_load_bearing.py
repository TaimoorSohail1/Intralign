from oslo_api.analysis.load_bearing import (
    CalibrationContext,
    CalibrationPolicy,
    EscalationRoute,
    FindingBasis,
    FindingType,
    PlanDependencyGraph,
    PlanEdge,
    PlanNode,
    PrimaryAct,
    SensitivityCandidate,
    StructuralTarget,
    apply_resolution_act,
    assess_unassessed_region,
    calibration_policy_from_environment,
    classify_finding,
    classify_finding_or_escalate,
    deterministic_finding_tags,
    evaluate_sensitivity,
    gate_sensitivity,
    perturbation_endpoints_or_escalate,
    route_runtime_escalation,
)
from oslo_api.analysis.models import ArtifactType, Assessment, Issue
from oslo_api.analysis.understanding import with_integrity


def test_resolution_is_derived_from_finding_model() -> None:
    """GT-34: resolution is derived; callers cannot author a primary move."""

    resolution = classify_finding(
        issue_id="ISS-VENUE-WIFI",
        finding_type=FindingType.DEPENDENCY_MAY_FAIL,
        basis=FindingBasis.INFERENCE,
        structural_target=StructuralTarget.ACHIEVABILITY,
    )

    assert resolution.primary_act is PrimaryAct.VERIFY
    assert resolution.pillar == "Viability"
    assert resolution.dimension == "Feasibility"
    assert resolution.also_offered == (PrimaryAct.BUILD,)


def test_inference_always_leads_with_verify_and_only_verify_can_ground() -> None:
    """GT-35/36: inference CTA is verify; build and decide cannot ground."""

    for finding_type, target in (
        (FindingType.INFERENCE_GAP, StructuralTarget.TRUTH),
        (FindingType.FALSE_CONFIDENCE, StructuralTarget.TRUTH),
        (FindingType.DEPENDENCY_MAY_FAIL, StructuralTarget.ACHIEVABILITY),
    ):
        resolution = classify_finding(
            issue_id=f"ISS-{finding_type.value}",
            finding_type=finding_type,
            basis=FindingBasis.INFERENCE,
            structural_target=target,
        )
        assert resolution.primary_act is PrimaryAct.VERIFY

    assert apply_resolution_act(PrimaryAct.VERIFY).grounding_delta > 0
    assert apply_resolution_act(PrimaryAct.BUILD).grounding_delta == 0
    assert apply_resolution_act(PrimaryAct.DECIDE).grounding_delta == 0


def test_structural_target_owns_dimension_not_finding_type() -> None:
    """GT-46: identical finding types can resolve to distinct target dimensions."""

    clarity = classify_finding(
        issue_id="ISS-CLARITY",
        finding_type=FindingType.UNOWNED,
        basis=FindingBasis.STRUCTURAL,
        structural_target=StructuralTarget.DEFINITION,
    )
    alignment = classify_finding(
        issue_id="ISS-ALIGNMENT",
        finding_type=FindingType.UNOWNED,
        basis=FindingBasis.STRUCTURAL,
        structural_target=StructuralTarget.EDGE,
    )

    assert clarity.dimension == "Clarity"
    assert alignment.dimension == "Alignment"


def test_unmapped_finding_type_escalates_instead_of_defaulting() -> None:
    """GT-37/38/48: unknown taxonomy is explicit and routed to governance."""

    result = classify_finding_or_escalate(
        issue_id="ISS-UNKNOWN",
        finding_type="novel_taxonomy_gap",
        basis="model_gap",
        structural_target="truth",
    )

    assert result.escalate is True
    assert result.route is EscalationRoute.GOVERNANCE
    assert result.primary_act is None
    assert result.dimension is None


def test_deterministic_classification_has_no_dimension_fallback() -> None:
    """GT-38: deterministic rules reject unknown dimensions rather than guessing."""

    try:
        deterministic_finding_tags(
            dimension="Novel dimension",
            title="Unknown rule",
            recommendation="Do something",
        )
    except ValueError as error:
        assert str(error) == "unmapped deterministic dimension: Novel dimension"
    else:
        raise AssertionError("unmapped dimensions must not receive a default target")


def _dependency_graph() -> PlanDependencyGraph:
    return PlanDependencyGraph(
        nodes=(
            PlanNode(
                id="ASSUMPTION-WIFI",
                type="inference",
                label="Venue Wi-Fi is sufficient",
                provenance="inferred",
                extraction_confidence=0.8,
            ),
            PlanNode(
                id="DELIVERY-ON-SITE",
                type="deliverable",
                label="On-site experience",
                provenance="accepted",
                extraction_confidence=0.9,
            ),
            PlanNode(
                id="OUTCOME",
                type="outcome",
                label="Successful conference",
                provenance="accepted",
                extraction_confidence=1.0,
            ),
        ),
        edges=(
            PlanEdge(
                from_id="ASSUMPTION-WIFI",
                to_id="DELIVERY-ON-SITE",
                rel="rests-on",
                weight=0.8,
                extraction_confidence=0.9,
            ),
            PlanEdge(
                from_id="DELIVERY-ON-SITE",
                to_id="OUTCOME",
                rel="supports",
                weight=0.5,
                extraction_confidence=0.85,
            ),
        ),
    )


def test_sensitivity_is_deterministic_decomposable_and_two_sided() -> None:
    """GT-39/40/41: graph output is stable, traced, and catches downside."""

    graph = _dependency_graph()
    candidate = SensitivityCandidate(
        id="ISS-WIFI",
        node_id="ASSUMPTION-WIFI",
        structural_target=StructuralTarget.TRUTH,
        favorable_integrity=0.9,
        adverse_integrity=0.1,
        runway_factor=1.25,
    )

    first = evaluate_sensitivity(graph=graph, candidate=candidate)
    second = evaluate_sensitivity(graph=graph, candidate=candidate)

    assert first == second
    assert first.trace.span_true == 0.9
    assert first.trace.span_false == 0.1
    assert first.trace.span == 0.8
    assert first.trace.paths == (("ASSUMPTION-WIFI", "DELIVERY-ON-SITE", "OUTCOME"),)
    assert first.trace.leverage > 0
    assert first.sensitivity > 0


def test_calibration_uses_global_prior_until_labels_and_never_suppresses_floor() -> None:
    """GT-42/43/44: segmentation starts dormant and cannot beat the floor."""

    policy = CalibrationPolicy(
        global_threshold=0.7,
        asymmetric_loss=1.2,
        critical_floor=0.9,
        surface_preference=-2.0,
        segment_thresholds={"events": 1.8},
        segment_label_counts={"events": 0},
    )
    context = CalibrationContext(domain="events", stakes=1.0)

    assert policy.effective_threshold(context) == 0.7
    gated = gate_sensitivity(
        sensitivity=0.95,
        policy=policy,
        context=context,
    )
    assert gated.load_bearing is True
    assert gated.critical_floor_applied is True
    assert gated.honesty_bar == "one_accuracy_bar"


def test_calibration_stays_in_shadow_until_every_owner_value_is_present() -> None:
    """L2 owner values are fail-closed: incomplete configuration is never guessed."""

    assert calibration_policy_from_environment({"LB_THRESHOLD": "0.7"}) is None

    policy = calibration_policy_from_environment(
        {
            "LB_THRESHOLD": "0.7",
            "LB_ASYMMETRIC_LOSS": "1.2",
            "LB_CRITICAL_FLOOR": "0.9",
            "LB_SURFACE_PREF": "0.05",
        }
    )

    assert policy is not None
    assert policy.global_threshold == 0.7
    assert policy.critical_floor == 0.9


def test_every_structural_target_has_endpoints_and_unknown_escalates() -> None:
    """GT-45: perturbation endpoints are complete and closed to extension."""

    for target in StructuralTarget:
        endpoint = perturbation_endpoints_or_escalate(target.value)
        assert endpoint.escalate is False
        assert endpoint.favorable
        assert endpoint.adverse

    unknown = perturbation_endpoints_or_escalate("novel-target")
    assert unknown.escalate is True
    assert unknown.route is EscalationRoute.GOVERNANCE


def test_alignment_sensitivity_is_edge_keyed_and_traces_outcome_reachability() -> None:
    """GT-47: Alignment is relational, not a node-local score."""

    graph = _dependency_graph()
    candidate = SensitivityCandidate(
        id="ISS-EDGE",
        node_id="DELIVERY-ON-SITE",
        edge_key=("DELIVERY-ON-SITE", "OUTCOME"),
        structural_target=StructuralTarget.EDGE,
        favorable_integrity=0.8,
        adverse_integrity=0.3,
        runway_factor=1.0,
    )

    record = evaluate_sensitivity(graph=graph, candidate=candidate)

    assert record.trace.edge_key == ("DELIVERY-ON-SITE", "OUTCOME")
    assert record.trace.outcome_reachability == ("OUTCOME",)


def test_runtime_ambiguity_routes_to_clarity_or_alignment() -> None:
    """GT-48: underspecification becomes a resolvable user issue."""

    missing_identity = route_runtime_escalation(
        issue_id="ISS-MISSING-TARGET",
        target_identity_known=False,
    )
    unsettled_edge = route_runtime_escalation(
        issue_id="ISS-UNSETTLED-EDGE",
        target_identity_known=True,
    )

    assert missing_identity.route is EscalationRoute.CLARIFY
    assert missing_identity.dimension == "Clarity"
    assert unsettled_edge.route is EscalationRoute.CLARIFY
    assert unsettled_edge.dimension == "Alignment"


def test_load_bearing_model_gap_is_incomplete_never_fragile_or_weak() -> None:
    """GT-49/50: an unknown can cap Sound without manufacturing a penalty."""

    assessment = assess_unassessed_region(load_bearing=True)

    assert assessment.incomplete is True
    assert assessment.blocks_sound is True
    assert assessment.surfaced is True
    assert assessment.band is None
    assert assessment.numeric_penalty is None
    assert assessment.graded_as_weak is False


def test_reanalysis_projects_sensitivity_trace_and_derived_action(monkeypatch) -> None:
    """Slice 10 vertical tracer: graph output reaches the persisted issue projection."""

    for name in (
        "LB_THRESHOLD",
        "LB_ASYMMETRIC_LOSS",
        "LB_CRITICAL_FLOOR",
        "LB_SURFACE_PREF",
    ):
        monkeypatch.delenv(name, raising=False)
    issue = Issue(
        id="ISS-WIFI",
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Grounding",
        severity="Warning",
        title="Venue Wi-Fi is assumed",
        why="The on-site experience rests on an unverified dependency.",
        recommendation="Confirm the venue capacity or build a fallback.",
        evidence_refs=("document:venue:page:1:fragment:1",),
        finding_type=FindingType.DEPENDENCY_MAY_FAIL.value,
        finding_basis=FindingBasis.INFERENCE.value,
        structural_target=StructuralTarget.ACHIEVABILITY.value,
    )
    candidate = SensitivityCandidate(
        id=issue.id,
        node_id="ASSUMPTION-WIFI",
        structural_target=StructuralTarget.ACHIEVABILITY,
        favorable_integrity=0.9,
        adverse_integrity=0.1,
        runway_factor=1.25,
        stakes=1.0,
    )
    assessment = Assessment(
        confidence_index=50,
        confidence_band="Moderate",
        reliability="Moderate",
        clarity="Moderate",
        alignment="Moderate",
        feasibility="Moderate",
        issues=(issue,),
        dependency_graph=_dependency_graph(),
        sensitivity_candidates=(candidate,),
    )

    projected = with_integrity(assessment, ())
    projected_issue = projected.issues[0]

    assert projected_issue.primary_act == "verify"
    assert projected_issue.dimension == "Feasibility"
    assert projected_issue.sensitivity is not None
    assert projected_issue.sensitivity_trace is not None
    assert projected_issue.sensitivity_trace["paths"]
    assert projected_issue.sensitivity_state == "shadow"


def test_reanalysis_ignores_sensitivity_candidate_for_unknown_edge() -> None:
    """A malformed optional model candidate cannot block an otherwise valid read."""

    issue = Issue(
        id="ISS-EDGE",
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Alignment",
        severity="Warning",
        title="Delivery dependency is unclear",
        why="The stated relationship is not present in the dependency graph.",
        recommendation="Confirm the dependency between delivery and the outcome.",
        evidence_refs=("document:plan:page:1:fragment:1",),
        finding_type=FindingType.UNOWNED.value,
        finding_basis=FindingBasis.STRUCTURAL.value,
        structural_target=StructuralTarget.EDGE.value,
    )
    candidate = SensitivityCandidate(
        id=issue.id,
        node_id="DELIVERY-ON-SITE",
        edge_key=("DELIVERY-ON-SITE", "UNKNOWN-OUTCOME"),
        structural_target=StructuralTarget.EDGE,
        favorable_integrity=0.8,
        adverse_integrity=0.3,
        runway_factor=1.0,
    )
    assessment = Assessment(
        confidence_index=50,
        confidence_band="Moderate",
        reliability="Moderate",
        clarity="Moderate",
        alignment="Moderate",
        feasibility="Moderate",
        issues=(issue,),
        dependency_graph=_dependency_graph(),
        sensitivity_candidates=(candidate,),
    )

    projected_issue = with_integrity(assessment, ()).issues[0]

    assert projected_issue.id == issue.id
    assert projected_issue.sensitivity is None
    assert projected_issue.sensitivity_trace is None
    assert projected_issue.sensitivity_state == "unavailable"


def test_reanalysis_never_leaves_a_deterministic_finding_unclassified() -> None:
    """GT-37/38: legacy deterministic findings receive explicit tags or escalate."""

    issue = Issue(
        id="ISS-CAPACITY",
        artifact_type=ArtifactType.RESOURCES,
        dimension="Feasibility",
        severity="Critical",
        title="Critical delivery capacity is not confirmed",
        why="The plan depends on capacity that has not been confirmed.",
        recommendation="Confirm the accountable owner and a tested contingency.",
        evidence_refs=("document:delivery:page:2:fragment:3",),
    )
    assessment = Assessment(
        confidence_index=50,
        confidence_band="Moderate",
        reliability="Moderate",
        clarity="Moderate",
        alignment="Moderate",
        feasibility="Moderate",
        issues=(issue,),
    )

    projected_issue = with_integrity(assessment, ()).issues[0]

    assert projected_issue.finding_type == FindingType.UNOWNED.value
    assert projected_issue.finding_basis == FindingBasis.STRUCTURAL.value
    assert projected_issue.structural_target == StructuralTarget.ACHIEVABILITY.value
    assert projected_issue.classification_state == "classified"
    assert projected_issue.primary_act == PrimaryAct.BUILD.value
