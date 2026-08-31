from oslo_api.analysis.models import (
    Artifact,
    ArtifactConflict,
    ArtifactSection,
    ArtifactType,
    Assessment,
    EvidenceFragment,
    Issue,
)
from oslo_api.analysis.semantic_validation import (
    apply_evidence_rubric,
    audit_artifact_conflicts,
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


def test_cited_derived_rows_remain_inferred_until_source_states_them_directly() -> None:
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

    assert normalized[0].sections[0].row_states == ("inferred",)


def test_source_grounded_rows_are_normalized_for_the_artifact_contract() -> None:
    artifact = Artifact(
        artifact_type=ArtifactType.INTENT,
        title="Intent",
        summary="A source-grounded outcome.",
        reliability="High",
        evidence_refs=("document:charter:page:1",),
        sections=(
            ArtifactSection(
                heading="Objectives",
                columns=("ID", "Objective"),
                rows=(("OBJ-01", "Launch the portal"),),
                row_evidence_refs=(("document:charter:page:1",),),
                row_states=("source_grounded",),
            ),
        ),
    )

    normalized = normalize_artifact_provenance((artifact,))

    assert normalized[0].sections[0].row_states == ("confirmed",)


def test_structured_artifact_conflicts_are_never_lost_by_evaluation() -> None:
    reference = "document:plan:page:7:fragment:8"
    artifact = Artifact(
        artifact_type=ArtifactType.SCHEDULE,
        title="Schedule",
        summary="A qualification schedule.",
        reliability="High",
        evidence_refs=(reference,),
        sections=(
            ArtifactSection(
                heading="Activities",
                columns=("Activity", "Start", "Finish", "Prerequisite"),
                rows=(
                    (
                        "Operational Qualification",
                        "04 Jan 2028",
                        "26 Feb 2028",
                        "IQ complete",
                    ),
                ),
                row_evidence_refs=((reference,),),
                row_states=("conflicting",),
            ),
        ),
        conflicts=(
            ArtifactConflict(
                id="C-01",
                field="OQ schedule prerequisite",
                values=(
                    "OQ starts 04 Jan 2028.",
                    "IQ completes 02 Feb 2028 and is the stated prerequisite.",
                ),
                evidence_refs=(reference,),
            ),
        ),
    )

    issues = audit_artifact_conflicts((artifact,))

    assert len(issues) == 1
    assert issues[0].severity == "Critical"
    assert issues[0].dimension == "Feasibility"
    assert issues[0].evidence_refs == (reference,)


def test_compound_structured_conflicts_publish_one_issue_per_subject() -> None:
    references = (
        "document:brief:page:1:fragment:1",
        "document:minutes:page:1:fragment:1",
    )
    artifact = Artifact(
        artifact_type=ArtifactType.SCOPE,
        title="Scope",
        summary="Three design values changed.",
        reliability="High",
        evidence_refs=references,
        sections=(),
        conflicts=(
            ArtifactConflict(
                id="C-DESIGN",
                field="Approved design versus meeting decision",
                values=(
                    "Berth length: 210 m approved; 185 m agreed.",
                    "Deck method: precast approved; in-situ agreed.",
                    "Design vessel: 180 m approved; 195 m agreed.",
                ),
                evidence_refs=references,
            ),
        ),
    )

    issues = audit_artifact_conflicts((artifact,))

    assert len(issues) == 3
    assert {issue.title for issue in issues} == {
        "Berth length is internally inconsistent",
        "Deck method is internally inconsistent",
        "Design vessel is internally inconsistent",
    }
    assert all(issue.dimension == "Alignment" for issue in issues)


def test_cross_document_decision_controls_are_evaluated_independently() -> None:
    evidence = (
        _fragment(
            1,
            (
                "Client Brief v2.1. Project Team Role Name Organisation. "
                "Marine Engineer Vacant. RA-01 risk: licence assumed by June; "
                "highest-rated project risk."
            ),
        ),
        _fragment(
            2,
            (
                "14.3 Berth length. Cost pressure was reported. AGREED that the "
                "berth length be reduced from 210 metres to 185 metres. "
                "14.5 AGREED that the deck be changed from precast to in-situ. "
                "14.7 Licence determination is now expected in September. "
                "14.9 AGREED that the design vessel be revised from 180 metres "
                "to 195 metres. Actions Ref Action Owner By A14.2 Instruct the "
                "design change R. Castellan 20 Jun 2026."
            ),
        ),
        _fragment(
            3,
            (
                "This report excludes any effect of design changes currently "
                "under consideration by the Design Team."
            ),
        ),
    )

    issue_ids = {issue.id for issue in audit_project_evidence(evidence)}

    assert "DET-REQUIREMENTS-PHYSICAL-FIT" in issue_ids
    assert "DET-CONTEXT-DECISION-STATUS-CONFLICT" in issue_ids
    assert "DET-CONTEXT-MATERIALIZED-RISK-CONTROL" in issue_ids
    assert "DET-RESOURCES-ACTION-OWNER-ROLE-GAP" in issue_ids
    assert "DET-RESOURCES-COST-DRIVEN-CHANGE-UNQUANTIFIED" in issue_ids
    assert "DET-SCOPE-CHANGES-NO-REVISED-BASELINE" in issue_ids


def test_contract_payment_is_flagged_when_most_fees_are_due_before_proof() -> None:
    evidence = (
        _fragment(
            4,
            """
            The Client shall author and execute all system integration test and
            user acceptance test scripts. A deliverable is deemed accepted when
            the Client does not object within five business days.
            """,
        ),
        _fragment(
            5,
            """
            Payment milestones
            Contract signature 30% Execution of this Statement of Work
            Design approval 30% Acceptance of DL-01 and DL-02
            Commencement of user acceptance testing 25% The date Client testing
            begins, irrespective of outcome
            Site 1 go-live 15% Production cutover at Site 1
            Total 100%
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    issue = next(
        item for item in issues if "payable before the system is proven" in item.title
    )
    assert issue.severity == "Critical"
    assert issue.dimension == "Feasibility"
    assert set(issue.evidence_refs) == {
        "document:lantern:page:4",
        "document:lantern:page:5",
    }


def test_contract_scope_is_checked_against_deliverables_and_optional_pricing() -> None:
    evidence = (
        _fragment(
            2,
            """
            The supplier will implement the platform across the Client's three
            manufacturing sites. Deliverables include Configured system - Site 1
            and Site 1 cutover and go-live. Configuration, integration and cutover
            at Site 2 and Site 3 are optional additional services.
            """,
        ),
        _fragment(
            5,
            """
            The total fixed price is 3,860,000. Optional services for Site 2 and
            Site 3 are available at 1,240,000 per site under separate statements
            of work.
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    issue = next(item for item in issues if item.id == "DET-SCOPE-OPTIONAL-SITES")
    assert issue.severity == "Critical"
    assert issue.dimension == "Alignment"
    assert set(issue.evidence_refs) == {
        "document:lantern:page:2",
        "document:lantern:page:5",
    }


def test_regulated_traceability_is_checked_against_material_exclusions() -> None:
    evidence = (
        _fragment(
            2,
            """
            Scope includes full batch traceability records to BRC Global Standard.
            Exclusions include laboratory system integration, allergen master data
            configuration, and validation documentation for regulatory or customer
            audit purposes.
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    issue = next(
        item for item in issues if item.id == "DET-SCOPE-TRACEABILITY-EXCLUSIONS"
    )
    assert issue.severity == "Critical"
    assert issue.dimension == "Alignment"


def test_contract_acceptance_and_timeline_need_objective_baselines() -> None:
    evidence = (
        _fragment(
            2,
            """
            Deliverables
            Ref Deliverable Description Format
            DL-01 Solution design document Configuration approach PDF
            DL-02 Integration specification Interface definitions PDF
            """,
        ),
        _fragment(
            4,
            """
            The Client shall notify any material non-conformance within five
            business days. Otherwise the deliverable is deemed accepted.
            The engagement has an estimated duration of 34 weeks from the
            effective date. A detailed project plan will be agreed within
            15 business days of the effective date.
            """,
        ),
    )

    issues = audit_project_evidence(evidence)
    identifiers = {issue.id for issue in issues}

    assert "DET-REQUIREMENTS-DEEMED-ACCEPTANCE" in identifiers
    assert "DET-SCHEDULE-UNDEFINED-EFFECTIVE-DATE" in identifiers


def test_contract_risk_transfer_and_obligation_asymmetry_are_visible() -> None:
    evidence = (
        _fragment(
            3,
            """
            Where a Client dependency is not met, the supplier may apply standing
            charges of 4,200 per working day and re-plan at the Client's cost.
            """,
        ),
        _fragment(
            4,
            """
            Client Obligations 6.1 6.2 6.3 6.4 6.5 6.6 6.7 6.8 6.9 6.10
            6.11 6.12 6.13 6.14.
            Supplier Obligations 7.1 7.2 7.3 7.4.
            The supplier may substitute personnel at its discretion. The Client
            shall name its project manager, data lead and subject matter experts
            and shall not substitute them without supplier written agreement.
            """,
        ),
        _fragment(
            6,
            """
            Supplier liability is limited to fees actually paid in the six months
            preceding the claim. The supplier is not liable for loss of production,
            spoilage, or consequential loss. The Client may terminate for convenience
            subject to 40% of remaining unbilled contract value.
            """,
        ),
    )

    issues = audit_project_evidence(evidence)
    identifiers = {issue.id for issue in issues}

    assert "DET-RESOURCES-LIABILITY-RISK-TRANSFER" in identifiers
    assert "DET-CONTEXT-OBLIGATION-ASYMMETRY" in identifiers
    assert "DET-RESOURCES-PERSONNEL-SUBSTITUTION" in identifiers
    assert "DET-RESOURCES-TERMINATION-CHARGE" in identifiers


def test_deliverable_warranty_is_checked_against_engagement_duration() -> None:
    evidence = (
        _fragment(4, "The engagement has an estimated duration of 34 weeks."),
        _fragment(
            6,
            """
            Each deliverable is warranted for 90 days from the date of delivery
            of that deliverable. The sole remedy is correction or re-performance.
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    issue = next(
        item for item in issues if item.id == "DET-RESOURCES-EARLY-WARRANTY-EXPIRY"
    )
    assert issue.severity == "High"
    assert issue.dimension == "Alignment"


def test_contract_component_total_and_change_rate_are_reconciled() -> None:
    evidence = (
        _fragment(
            5,
            """
            The total fixed price is 3,860,000.
            Component
            Amount
            Professional services at a blended rate of 1,150
            2,461,000
            Software licences
            980,000
            Hosting and managed service
            420,000
            Data migration tooling
            115,000
            Total
            3,860,000
            """,
        ),
        _fragment(
            6,
            """
            The impact assessment is chargeable at 1,150 per person-day.
            Blended change-control rate 1,325
            """,
        ),
    )

    issues = audit_project_evidence(evidence)
    by_id = {issue.id: issue for issue in issues}

    assert "3,976,000" in by_id["DET-RESOURCES-COMPONENT-TOTAL-CONFLICT"].why
    assert "116,000" in by_id["DET-RESOURCES-COMPONENT-TOTAL-CONFLICT"].why
    assert "DET-RESOURCES-CHANGE-CONTROL-RATE-CONFLICT" in by_id

def test_same_structured_conflict_repeated_across_artifacts_is_deduplicated() -> None:
    references = (
        "document:plan:page:5:fragment:5",
        "document:plan:page:7:fragment:8",
    )

    def artifact(artifact_type: ArtifactType) -> Artifact:
        return Artifact(
            artifact_type=artifact_type,
            title=artifact_type.value,
            summary="A structured project read.",
            reliability="High",
            evidence_refs=references,
            sections=(
                ArtifactSection(
                    heading="Summary",
                    body="A shared resource is constrained.",
                ),
            ),
            conflicts=(
                ArtifactConflict(
                    id="C-LY02",
                    field="LY-02 shared-resource availability",
                    values=(
                        "Line 3 requires LY-02 during qualification.",
                        "Line 2 books LY-02 across the same window.",
                    ),
                    evidence_refs=references,
                ),
            ),
        )

    issues = audit_artifact_conflicts(
        (artifact(ArtifactType.SCHEDULE), artifact(ArtifactType.RESOURCES))
    )

    assert len(issues) == 1


def test_dense_traceable_plan_does_not_hide_modelled_delivery_risk() -> None:
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

    assert result.clarity == "Moderate"
    assert result.alignment == "Moderate"
    assert result.feasibility == "Low"
    assert result.reliability == "Moderate"
    assert result.confidence_band == "Moderate"
    assert result.confidence_index == 45


def test_critical_open_finding_caps_confidence_without_changing_dimension_bands() -> None:
    evidence = (_fragment(1, "The objective and proposed solution conflict."),)
    critical_issue = Issue(
        id="DET-ALIGNMENT-CRITICAL",
        artifact_type=ArtifactType.SCOPE,
        dimension="Alignment",
        severity="Critical",
        title="The proposed solution does not address the evidenced problem",
        why="The diagnosed causes have no corresponding intervention.",
        recommendation="Trace every cause to an intervention and outcome measure.",
        evidence_refs=(evidence[0].reference,),
    )
    assessment = Assessment(
        confidence_index=73,
        confidence_band="High",
        reliability="High",
        clarity="High",
        alignment="Low",
        feasibility="Moderate",
        issues=(critical_issue,),
    )

    result = apply_evidence_rubric(assessment, evidence)

    assert result.confidence_band == "Low"
    assert result.confidence_index == 38
    assert result.clarity == "High"
    assert result.alignment == "Low"
    assert result.feasibility == "Moderate"
    assert result.reliability == "High"


def test_repeated_critical_findings_cap_only_the_affected_dimension() -> None:
    issues = tuple(
        Issue(
            id=f"ALIGN-{index}",
            artifact_type=ArtifactType.SCOPE,
            dimension="Alignment",
            severity="Critical",
            title=f"Material objective {index} has no intervention",
            why="The objective does not trace to scope or a measured outcome.",
            recommendation="Add a directly linked intervention and outcome measure.",
            evidence_refs=(f"document:plan:page:{index}:fragment:1",),
        )
        for index in range(4)
    )
    assessment = Assessment(
        confidence_index=82,
        confidence_band="High",
        reliability="High",
        clarity="High",
        alignment="High",
        feasibility="High",
        issues=issues,
    )

    result = apply_evidence_rubric(assessment, ())

    assert result.alignment == "Very Low"
    assert result.clarity == "High"
    assert result.feasibility == "High"
    assert result.confidence_band == "Low"


def test_many_material_findings_reduce_only_the_affected_dimension_to_very_low() -> None:
    issues = tuple(
        Issue(
            id=f"ALIGN-MATERIAL-{index}",
            artifact_type=ArtifactType.SCOPE,
            dimension="Alignment",
            severity="Moderate",
            title=f"Material alignment weakness {index}",
            why="A separate project decision conflicts with its approved baseline.",
            recommendation="Reconcile the decision.",
            evidence_refs=(f"document:plan:page:{index}:fragment:1",),
        )
        for index in range(6)
    )
    assessment = Assessment(
        confidence_index=42,
        confidence_band="Low",
        reliability="High",
        clarity="High",
        alignment="High",
        feasibility="High",
        issues=issues,
    )

    result = apply_evidence_rubric(assessment, ())

    assert result.alignment == "Very Low"
    assert result.clarity == "High"
    assert result.feasibility == "High"


def test_summary_appendix_checks_find_conflicts_without_penalising_detail() -> None:
    issues = audit_project_evidence(
        (
            _fragment(
                3,
                "Executive summary. Schedule GREEN. Programme remains on schedule. "
                "Design is complete. The team is fully resourced and no recruitment "
                "concerns are reported. No actions remain outstanding.",
            ),
            _fragment(
                4,
                "Carried forward Action 10.4. Owner A. Still open. "
                "Automated sortation was removed from scope.",
            ),
            _fragment(
                5,
                "68% Programme complete. £2.1M underspend. The annual benefit is "
                "driven by automation. System cutover is planned on 12 to 14 August 2027.",
            ),
            _fragment(
                6,
                "Milestone summary: M7 System integration testing begins On track. "
                "The full tracker is in appendix A.",
            ),
            _fragment(
                12,
                "APPENDIX A Full Milestone Tracker. "
                "M4 | Design freeze | 31 Oct 2025 | 30 Sep 2026 | +48 weeks | Slipped "
                "M7 | System integration testing | 31 Jan 2027 | 28 May 2027 | "
                "+17 weeks | Slipped "
                "M8 | Required security approval | 28 Feb 2027 | Not scheduled | "
                "Not scheduled M11 | Handover | 31 Oct 2027 | 14 Feb 2028 | "
                "+15 weeks | Slipped",
            ),
            _fragment(
                13,
                "APPENDIX B Cost Breakdown. Forecast final. Deferred automated "
                "sortation. The underspend arises from the deferral.",
            ),
            _fragment(
                14,
                "APPENDIX C Full Risk Register. "
                "R-11 | Readiness and training not complete before cutover | 4 | 4 | 16 | A "
                "R-15 | Cutover falls within the change freeze "
                "(1 July – 6 September) | 5 | 4 | 20 | B "
                "R-18 | Three vacant engineer roles | 4 | 3 | 12 | C",
            ),
        )
    )
    issue_ids = {issue.id for issue in issues}

    assert {
        "DET-SCHEDULE-SUMMARY-REGISTER-CONFLICT",
        "DET-SCHEDULE-M7-STATUS-CONFLICT",
        "DET-RESOURCES-UNDERSPEND-FORECAST-CONFLICT",
        "DET-SCHEDULE-CUTOVER-PROTECTED-WINDOW",
        "DET-INTENT-BENEFIT-DESCOPED-DEPENDENCY",
        "DET-WORK-BREAKDOWN-OPEN-ACTION-CONFLICT",
        "DET-RESOURCES-VACANCY-CONFLICT",
        "DET-WORK-BREAKDOWN-READINESS-CONTROL-GAP",
    } <= issue_ids
    assert not any("appendix arithmetic" in issue.title.lower() for issue in issues)
