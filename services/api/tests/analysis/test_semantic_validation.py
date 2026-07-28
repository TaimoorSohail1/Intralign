from oslo_api.analysis.models import (
    Artifact,
    ArtifactSection,
    ArtifactType,
    Assessment,
    EvidenceFragment,
    Issue,
)
from oslo_api.analysis.semantic_validation import (
    apply_evidence_rubric,
    audit_project_evidence,
    merge_semantic_issues,
    normalize_artifact_provenance,
)


def _fragment(page: int, content: str) -> EvidenceFragment:
    return EvidenceFragment(
        reference=f"document:lantern:page:{page}",
        content=content,
        source_name="Project plan.pdf",
        location=f"Page {page}",
    )


def test_semantic_audit_detects_cross_page_contradictions_and_absences() -> None:
    evidence = (
        _fragment(
            5,
            """
            1.2 Client materials received
            CM-02 Operational KPI extract, FY24-FY26
            The consequences are measurable and documented in CM-02: stock file
            accuracy of 91.2% against a sector benchmark of 98%, order pick accuracy
            of 97.4%, and click-and-collect readiness averaging 4.2 hours against a
            competitor norm under 2 hours.
            """,
        ),
        _fragment(
            7,
            """
            3.1 In scope
            Integration to Dynamics 365 F&O, the transport management system,
            the e-commerce platform, and the carrier aggregation service.
            3.3 Assumptions
            A-01
            Meridian delivery team of 11 named consultants is available from
            6 Aug 2026 as per SOW Schedule 2
            A-05
            RF hardware lead time does not exceed 12 weeks from order
            Order early against contingency; see R-06
            3.4 Constraints
            Trading freeze: no production change between 1 November 2026 and
            10 January 2027, and between 20 November 2027 and 8 January 2028.
            """,
        ),
        _fragment(
            8,
            """
            5.2 Delivery phases
            Phase
            Description
            Start
            Finish
            Wks
            Gate
            P0
            Mobilisation and discovery
            06 Aug 2026
            25 Sep 2026
            7
            G1
            P1
            Solution design and vendor contracting
            28 Sep 2026
            18 Dec 2026
            12
            G2
            P2
            Build, configuration and unit test
            05 Jan 2027
            30 Apr 2027
            17
            G3
            P3
            Integration test, UAT and migration rehearsal
            03 May 2027
            25 Jun 2027
            8
            G4
            P4
            Pilot
            28 Jun 2027
            06 Aug 2027
            6
            G5
            P5
            National rollout
            09 Aug 2027
            03 Sep 2027
            4
            G6
            The gap between 18 December 2026 and 5 January 2027 is the FY27
            peak trading freeze.
            5.3 Work breakdown structure
            WBS
            Work package
            Owner
            Phase
            Effort (days)
            3.0
            Vendor selection, contracting and commercial management
            Procurement
            P0-P1
            70
            """,
        ),
        _fragment(
            9,
            """
            WBS
            Work package
            Owner
            Phase
            Effort (days)
            5.0
            Platform configuration and extension build
            Meridian
            P2
            620
            9.0
            Test management - SIT, performance, security, UAT
            Test Manager
            P2-P3
            215
            Total estimated effort 2,465 person-days, comprising 1,340 partner
            days and 1,125 internal days.
            """,
        ),
        _fragment(
            10,
            """
            6. Schedule and Milestones
            ID
            Milestone
            Baseline date
            Predecessor
            Critical path
            M1
            Project kickoff and team mobilised
            06 Aug 2026
            -
            Yes
            M2
            Vendor contract executed
            16 Oct 2026
            M1
            Yes
            M3
            Discovery report signed off
            25 Sep 2026
            M1
            Yes
            M4
            Gate G2 - solution design approval
            18 Dec 2026
            M2, M3
            Yes
            M6
            Gate G3 - build complete
            30 Apr 2027
            M5
            Yes
            M8
            Gate G4 - UAT exit
            25 Jun 2027
            M6, M7
            Yes
            M10
            Gate G5 - pilot acceptance
            06 Aug 2027
            M9
            Yes
            M11
            National go-live complete
            27 Aug 2027
            M10
            Yes
            M12
            Gate G6 - closure
            03 Sep 2027
            M11
            Yes
            7. Budget and Cost Baseline
            Hardware - RF devices, printing, network remediation
            486,000
            0
            486,000
            Base cost
            4,516,000
            Contingency
            334,000
            """,
        ),
        _fragment(
            11,
            """
            8.1 Project organisation
            Role
            Name
            Organisation
            Allocation
            Available from
            Test Manager
            Dominic Reyes
            Meridian Supply Systems
            1.0 FTE
            05 Jan 2027
            Partner delivery team
            11 named consultants
            Meridian Supply Systems
            9.2 FTE peak
            16 Oct 2026
            8.2 Responsibility assignment (RACI)
            Activity Sponsor PM Arch Ops IT Partner Finance
            """,
        ),
        _fragment(
            12,
            """
            10.2 Risk register
            R-06
            RF hardware lead time exceeds 12 weeks
            Order at M2 against contingency; 40 loan units in partner contract
            Procurement
            """,
        ),
        _fragment(
            14,
            """
            11.2 Migration acceptance thresholds
            T-03 Stock on hand - value variance
            <=0.25% of total stock value
            11.3 Cutover and rollback
            Rollback is invoked if stock value variance exceeds 1.0% at cutover
            plus 4 hours.
            """,
        ),
        _fragment(
            15,
            """
            12.1 Test stages
            System integration test
            D. Reyes
            All 9 interfaces deployed to SIT
            All interfaces pass
            03-28 May 2027
            Performance test
            D. Reyes
            SIT pass >=90%
            NFR targets met
            10-21 May 2027
            User acceptance test
            P. Raman
            SIT exit, migration mock 2 complete
            95% passed
            31 May-25 Jun 2027
            Operational readiness test
            C. Doyle
            UAT exit
            Runbooks executed
            21-25 Jun 2027
            """,
        ),
        _fragment(
            16,
            """
            14. Benefits Realisation and Success Measures
            Measurement begins at pilot go-live and is reported monthly until
            12 months after national go-live.
            K-06
            Inventory write-off, annualised
            1.34M
            <=0.85M
            31 Mar 2029
            Finance write-off ledger
            H. Kirkbride
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    assert {issue.id for issue in issues} == {
        "DET-SCHEDULE-FREEZE-CONFLICT",
        "DET-SCHEDULE-FREEZE-VIOLATION",
        "DET-RESOURCES-AVAILABILITY-CONFLICT",
        "DET-REQUIREMENTS-THRESHOLD-GAP",
        "DET-SCHEDULE-ENTRY-CRITERION-PERFORMANCE",
        "DET-SCHEDULE-ENTRY-CRITERION-ORT",
        "DET-SCHEDULE-MEASUREMENT-WINDOW",
        "DET-WORK-BREAKDOWN-EFFORT-SPLIT",
        "DET-SCHEDULE-MISSING-GATE-MILESTONE",
        "DET-RESOURCES-FUNDING-CONFLICT",
        "DET-SCHEDULE-MILESTONE-ORDER",
        "DET-CONTEXT-UNCITED-BENCHMARK",
        "DET-CONTEXT-MISSING-DEPENDENCY-REGISTER",
        "DET-RESOURCES-MISSING-PROCUREMENT-APPROACH",
    }
    assert sum(issue.severity == "Critical" for issue in issues) == 4
    assert all(issue.evidence_refs for issue in issues)


def test_semantic_audit_does_not_flag_documented_exceptions() -> None:
    evidence = (
        _fragment(
            3,
            """
            Contingency is held unallocated by the Sponsor and released through
            the approved change-control process.
            Open purchase orders at the future cutover are estimates.
            Scope excludes automation and the supplier portal under decision
            SC-2026-011.
            Migration acceptance uses dual sign-off, explicitly approved in the
            RACI.
            """,
        ),
    )

    assert audit_project_evidence(evidence) == ()


def test_semantic_audit_detects_implied_regulated_controls_without_fixture_names() -> None:
    evidence = (
        _fragment(
            3,
            """
            The project delivers a sterile aseptic fill-finish line under EU GMP
            Annex 1 (2022). The lyophiliser and secondary packaging assets are
            shared with another operating line.
            """,
        ),
        _fragment(
            5,
            """
            The isolator equipment package is single-source and sits on the
            programme critical path. Two signed customer supply agreements depend
            on commercial production starting 1 June 2028.
            """,
        ),
    )

    issues = audit_project_evidence(evidence)
    identifiers = {issue.id for issue in issues}

    assert "DET-REQUIREMENTS-MISSING-CONTAMINATION-CONTROL" in identifiers
    assert "DET-REQUIREMENTS-MISSING-CLEANING-VALIDATION" in identifiers
    assert "DET-RESOURCES-MISSING-VENDOR-QUALIFICATION" in identifiers
    assert "DET-SCOPE-MISSING-SUPPLY-FALLBACK" in identifiers


def test_semantic_audit_accepts_explicit_regulated_controls_and_supply_fallback() -> None:
    evidence = (
        _fragment(
            3,
            """
            The sterile line follows EU GMP Annex 1 (2022). The approved
            Contamination Control Strategy (CCS) governs the shared lyophiliser.
            Cleaning validation covers every product-contact and shared surface.
            The single-source critical-path vendor passed supplier audit and
            vendor qualification. A qualified contract manufacturer provides the
            fallback supply route for both signed customer agreements.
            """,
        ),
    )

    identifiers = {issue.id for issue in audit_project_evidence(evidence)}

    assert "DET-REQUIREMENTS-MISSING-CONTAMINATION-CONTROL" not in identifiers
    assert "DET-REQUIREMENTS-MISSING-CLEANING-VALIDATION" not in identifiers
    assert "DET-RESOURCES-MISSING-VENDOR-QUALIFICATION" not in identifiers
    assert "DET-SCOPE-MISSING-SUPPLY-FALLBACK" not in identifiers


def test_semantic_merge_deduplicates_currency_rate_findings_with_shared_evidence() -> None:
    reference = "document:plan:page:8"
    first = Issue(
        id="MODEL-FX-1",
        artifact_type=ArtifactType.RESOURCES,
        dimension="Alignment",
        severity="Moderate",
        title="Foreign exchange assumption conflicts with treasury policy",
        why="The euro equipment conversion uses 1.11 instead of the mandated 1.15 rate.",
        recommendation="Use the approved conversion basis.",
        evidence_refs=(reference,),
    )
    duplicate = Issue(
        id="MODEL-FX-2",
        artifact_type=ArtifactType.RESOURCES,
        dimension="Alignment",
        severity="Critical",
        title="Currency conversion breaches the group rate",
        why="Equipment priced in euros was translated to sterling at the wrong rate.",
        recommendation="Recalculate the budget.",
        evidence_refs=(reference,),
    )

    merged = merge_semantic_issues((first, duplicate), ())

    assert len(merged) == 1


def test_semantic_audit_detects_undeclared_stage_overlap_and_short_warranty_cover() -> None:
    evidence = (
        _fragment(
            6,
            """
            Qualification schedule
            S3 Commissioning and qualification 10 January 2028 9 April 2028 G3
            S4 Process validation 20 March 2028 12 May 2028 G4
            """,
        ),
        _fragment(
            8,
            """
            M3 Equipment delivery 24 September 2027.
            Commercial production starts 1 June 2028.
            """,
        ),
        _fragment(
            12,
            "The equipment warranty is 12 months from delivery.",
        ),
    )

    identifiers = {issue.id for issue in audit_project_evidence(evidence)}

    assert "DET-SCHEDULE-UNDECLARED-STAGE-OVERLAP" in identifiers
    assert "DET-RESOURCES-SHORT-WARRANTY-COVER" in identifiers


def test_semantic_audit_accepts_governed_overlap_and_sufficient_operational_warranty() -> None:
    evidence = (
        _fragment(
            6,
            """
            Qualification schedule
            S3 Commissioning 10 January 2028 9 April 2028 G3
            S4 Validation 20 March 2028 12 May 2028 G4
            The overlap is approved fast-tracking and risk R-14 governs shared work.
            """,
        ),
        _fragment(
            8,
            """
            M3 Equipment delivery 24 September 2027.
            Commercial production starts 1 June 2028.
            The equipment warranty is 24 months from delivery.
            """,
        ),
    )

    identifiers = {issue.id for issue in audit_project_evidence(evidence)}

    assert "DET-SCHEDULE-UNDECLARED-STAGE-OVERLAP" not in identifiers
    assert "DET-RESOURCES-SHORT-WARRANTY-COVER" not in identifiers


def test_evidence_backed_rows_are_not_reported_as_oslo_inference() -> None:
    artifact = Artifact(
        artifact_type=ArtifactType.SCHEDULE,
        title="Schedule",
        summary="A sourced baseline.",
        reliability="High",
        evidence_refs=("document:plan:page:8",),
        sections=(
            ArtifactSection(
                heading="Milestones",
                columns=("Milestone", "Date"),
                rows=(("Go-live", "2 Aug 2027"),),
                row_evidence_refs=(("document:plan:page:8",),),
                row_states=("inferred",),
            ),
        ),
    )

    normalized = normalize_artifact_provenance((artifact,))

    assert normalized[0].sections[0].row_states == ("confirmed",)


def test_dense_traceable_plan_receives_stable_understanding_bands() -> None:
    evidence = tuple(
        _fragment(
            page,
            (
                f"O{page} objective D-{page:02d} deliverable K-{page:02d} success measure "
                f"M{page} milestone P{page} phase R-{page:02d} risk. "
                f"Owner: Lead {page}. Accepted by Sponsor. Sign-off by Finance. "
                f"Threshold <=0.{page}% on {page} Aug 2027. "
                "Scope, requirements, acceptance criteria and benefits are traceable."
            ),
        )
        for page in range(1, 9)
    )
    feasibility_issue = Issue(
        id="DET-SCHEDULE-TEST",
        artifact_type=ArtifactType.SCHEDULE,
        dimension="Feasibility",
        severity="Moderate",
        title="A schedule dependency is infeasible",
        why="A dependent activity starts before its prerequisite finishes.",
        recommendation="Correct the dates.",
        evidence_refs=(evidence[0].reference,),
    )
    assessment = Assessment(
        confidence_index=45,
        confidence_band="Moderate",
        reliability="Moderate",
        clarity="Moderate",
        alignment="Moderate",
        feasibility="Low",
        issues=(feasibility_issue,),
    )

    result = apply_evidence_rubric(assessment, evidence)

    assert result.clarity == "High"
    assert result.alignment == "High"
    assert result.feasibility == "Moderate"
    assert result.reliability == "High"
    assert result.confidence_band == "High"
    assert result.confidence_index == 82
