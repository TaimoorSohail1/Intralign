from oslo_api.analysis.models import ArtifactType, EvidenceFragment
from oslo_api.analysis.semantic_validation import audit_project_evidence


def _fragment(page: int, content: str) -> EvidenceFragment:
    return EvidenceFragment(
        reference=f"document:plan:page:{page}:fragment:1",
        content=content,
        source_name="Programme plan.pdf",
        location=f"Page {page}",
    )


def test_protected_operating_window_blocks_overlapping_cutover() -> None:
    evidence = (
        _fragment(
            3,
            """
            Aurora Sport carries the Continental Final live from 12 November 2027
            to 21 November 2027. Transmission continuity during this contractual
            rights window is mandatory and no platform change is permitted.
            """,
        ),
        _fragment(
            9,
            """
            Channel migration schedule
            Aurora Sport cutover: 13-15 November 2027.
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    assert len(issues) == 1
    issue = issues[0]
    assert issue.artifact_type is ArtifactType.SCHEDULE
    assert issue.dimension == "Feasibility"
    assert issue.severity == "Critical"
    assert "protected operating window" in issue.title.casefold()
    assert issue.evidence_refs == (
        "document:plan:page:3:fragment:1",
        "document:plan:page:9:fragment:1",
    )


def test_stated_contingency_percentage_is_reconciled_to_budget_amounts() -> None:
    evidence = (
        _fragment(
            2,
            "The approved cost baseline includes a 15% contingency.",
        ),
        _fragment(
            8,
            """
            Budget baseline
            Base cost: £28.4M
            Contingency: £3.1M
            Total approved cost: £31.5M
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    assert len(issues) == 1
    issue = issues[0]
    assert issue.artifact_type is ArtifactType.RESOURCES
    assert issue.dimension == "Clarity"
    assert issue.severity == "Moderate"
    assert "contingency percentage" in issue.title.casefold()
    assert "10.9%" in issue.why
    assert issue.evidence_refs == (
        "document:plan:page:2:fragment:1",
        "document:plan:page:8:fragment:1",
    )


def test_physical_measurements_are_compared_across_documents() -> None:
    evidence = (
        _fragment(
            2,
            "DR-05 Capital dredge volume 240,000 cubic metres.",
        ),
        _fragment(
            8,
            (
                "M-01 Capital dredge quantity re-measured at "
                "310,000 cubic metres."
            ),
        ),
    )

    issues = audit_project_evidence(evidence)
    conflict = next(
        issue for issue in issues if "measured values" in issue.title.casefold()
    )

    assert conflict.dimension == "Alignment"
    assert "240000" in conflict.why
    assert "310000" in conflict.why
    assert conflict.evidence_refs == (
        "document:plan:page:2:fragment:1",
        "document:plan:page:8:fragment:1",
    )


def test_contingency_drawdown_is_compared_with_delivery_progress() -> None:
    evidence = (
        _fragment(
            8,
            (
                "Contingency of £2,750,000 was allowed. Instructions have "
                "committed £2,150,000 (78.2%), leaving £600,000 uncommitted "
                "at 31% works completion."
            ),
        ),
    )

    issues = audit_project_evidence(evidence)
    issue = next(
        item for item in issues if item.id == "DET-RESOURCES-CONTINGENCY-DRAWDOWN"
    )

    assert issue.dimension == "Feasibility"
    assert issue.severity == "Critical"
    assert "78.2%" in issue.why
    assert "31%" in issue.why


def test_external_contract_expiry_is_checked_against_project_end() -> None:
    evidence = (
        _fragment(
            2,
            "The carrier circuit contract expires on 31 October 2027.",
        ),
        _fragment(
            7,
            "Migration and closure run through 25 February 2028.",
        ),
    )

    issues = audit_project_evidence(evidence)

    assert len(issues) == 1
    issue = issues[0]
    assert issue.artifact_type is ArtifactType.RESOURCES
    assert issue.dimension == "Clarity"
    assert issue.severity == "Moderate"
    assert "expires before project completion" in issue.title.casefold()
    assert issue.evidence_refs == (
        "document:plan:page:2:fragment:1",
        "document:plan:page:7:fragment:1",
    )


def test_contract_expiry_uses_a_project_closure_milestone_table() -> None:
    evidence = (
        _fragment(
            2,
            "The carrier circuit contract expires on 31 October 2027.",
        ),
        _fragment(
            7,
            """
            Milestones ID Milestone Baseline date Predecessor
            M9 Wave 3 complete 11 Feb 2028 M8
            M10 Facility decommissioned, project closure 25 Feb 2028 M9
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    assert any("expires before project completion" in issue.title.casefold() for issue in issues)


def test_approved_contract_extension_and_matching_budget_are_not_flagged() -> None:
    evidence = (
        _fragment(
            2,
            """
            The approved cost baseline includes a 10% contingency.
            The carrier circuit contract expires on 31 October 2027.
            """,
        ),
        _fragment(
            7,
            """
            Migration and closure run through 25 February 2028.
            The circuit contract extension through 31 March 2028 is approved,
            funded, and owned by Commercial Operations.
            """,
        ),
        _fragment(
            8,
            "Base cost: £20M. Contingency: £2M. Total approved cost: £22M.",
        ),
    )

    assert audit_project_evidence(evidence) == ()


def test_regulated_output_requirements_need_a_verification_route() -> None:
    evidence = (
        _fragment(
            4,
            """
            Licence conditions require subtitles on 90% of output, audio
            description on 10%, and signed programming on 5%.
            """,
        ),
        _fragment(
            10,
            """
            Test stages cover performance, failover, security, migration
            reconciliation, and operational readiness.
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    assert len(issues) == 1
    issue = issues[0]
    assert issue.artifact_type is ArtifactType.REQUIREMENTS
    assert issue.dimension == "Clarity"
    assert issue.severity == "Moderate"
    assert "verification route" in issue.title.casefold()
    assert issue.evidence_refs == ("document:plan:page:4:fragment:1",)


def test_regulated_output_requirements_with_acceptance_tests_are_not_flagged() -> None:
    evidence = (
        _fragment(
            4,
            """
            Licence conditions require subtitles on 90% of output, audio
            description on 10%, and signed programming on 5%.
            """,
        ),
        _fragment(
            10,
            """
            Accessibility output verification at UAT samples subtitles, audio
            description, and signed programming against each licence threshold.
            Release acceptance requires all samples to pass.
            """,
        ),
    )

    assert audit_project_evidence(evidence) == ()


def test_availability_requirement_needs_disaster_recovery_controls() -> None:
    evidence = (
        _fragment(
            6,
            """
            NFR-01: The production platform shall provide 99.9% availability,
            measured monthly.
            """,
        ),
        _fragment(
            9,
            """
            The acceptance plan covers performance, security and migration
            reconciliation.
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    assert len(issues) == 1
    issue = issues[0]
    assert issue.artifact_type is ArtifactType.REQUIREMENTS
    assert issue.dimension == "Clarity"
    assert issue.severity == "Moderate"
    assert "disaster recovery" in issue.title.casefold()
    assert issue.evidence_refs == ("document:plan:page:6:fragment:1",)


def test_card_payment_processing_needs_a_payment_security_requirement() -> None:
    evidence = (
        _fragment(
            5,
            """
            FR-046: The platform shall support card pre-authorisation and
            payment capture at check-in and check-out.
            """,
        ),
        _fragment(
            8,
            """
            IN-03: The payment gateway returns tokenised card references to
            the property management platform.
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    assert len(issues) == 1
    issue = issues[0]
    assert issue.artifact_type is ArtifactType.REQUIREMENTS
    assert issue.dimension == "Clarity"
    assert issue.severity == "Moderate"
    assert "payment security" in issue.title.casefold()
    assert issue.evidence_refs == (
        "document:plan:page:5:fragment:1",
        "document:plan:page:8:fragment:1",
    )


def test_large_personal_profile_store_needs_data_protection_requirements() -> None:
    evidence = (
        _fragment(
            3,
            """
            The platform will hold 3,410,000 active guest profiles including
            identity, contact, stay and folio history.
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    assert len(issues) == 1
    issue = issues[0]
    assert issue.artifact_type is ArtifactType.REQUIREMENTS
    assert issue.dimension == "Clarity"
    assert issue.severity == "Moderate"
    assert "data protection" in issue.title.casefold()
    assert issue.evidence_refs == ("document:plan:page:3:fragment:1",)


def test_customer_facing_interface_needs_accessibility_requirements() -> None:
    evidence = (
        _fragment(
            4,
            """
            The solution includes a guest-facing online reservation interface
            and staff-facing front desk workflows.
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    assert len(issues) == 1
    issue = issues[0]
    assert issue.artifact_type is ArtifactType.REQUIREMENTS
    assert issue.dimension == "Clarity"
    assert issue.severity == "Low"
    assert "accessibility" in issue.title.casefold()
    assert issue.evidence_refs == ("document:plan:page:4:fragment:1",)


def test_brand_website_booking_engine_needs_accessibility_requirements() -> None:
    evidence = (
        _fragment(
            2,
            "Reservations are taken through the brand website booking engine.",
        ),
    )

    issues = audit_project_evidence(evidence)

    assert len(issues) == 1
    assert "accessibility" in issues[0].title.casefold()
    assert issues[0].evidence_refs == ("document:plan:page:2:fragment:1",)


def test_documented_assurance_controls_suppress_completeness_findings() -> None:
    evidence = (
        _fragment(
            4,
            """
            The customer-facing portal is verified against WCAG 2.2 AA with
            keyboard and screen-reader acceptance tests.
            """,
        ),
        _fragment(
            5,
            """
            Card payment capture is governed by PCI DSS controls and an
            independent payment penetration test before release.
            """,
        ),
        _fragment(
            6,
            """
            The service provides 99.9% availability. Disaster recovery defines
            an RTO of four hours, an RPO of fifteen minutes, backup restoration
            tests and failover acceptance.
            """,
        ),
        _fragment(
            7,
            """
            Customer profiles are governed by GDPR and the approved data
            protection impact assessment, including lawful basis and erasure.
            """,
        ),
    )

    assert audit_project_evidence(evidence) == ()


def test_overbooking_requirement_conflicting_with_inventory_rule_is_one_issue() -> None:
    evidence = (
        _fragment(
            4,
            """
            FR-032: The system shall support controlled overbooking of up to
            5% of house capacity.
            """,
        ),
        _fragment(
            8,
            """
            BR-11: The system shall not permit a reservation to be confirmed
            where no inventory is available.
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    assert len(issues) == 1
    issue = issues[0]
    assert issue.artifact_type is ArtifactType.REQUIREMENTS
    assert issue.dimension == "Feasibility"
    assert issue.severity == "Critical"
    assert "overbooking" in issue.title.casefold()
    assert "inventory" in issue.title.casefold()
    assert issue.evidence_refs == (
        "document:plan:page:4:fragment:1",
        "document:plan:page:8:fragment:1",
    )


def test_central_rate_control_conflicting_with_property_discount_is_one_issue() -> None:
    evidence = (
        _fragment(
            5,
            """
            BR-03: Rates are set centrally and shall not be amended at
            property level.
            """,
        ),
        _fragment(
            7,
            """
            FR-027: Front desk managers shall be able to apply a discretionary
            discount of up to 15% at check-in.
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    assert len(issues) == 1
    issue = issues[0]
    assert issue.artifact_type is ArtifactType.REQUIREMENTS
    assert issue.dimension == "Feasibility"
    assert issue.severity == "Critical"
    assert "central" in issue.title.casefold()
    assert "property" in issue.title.casefold()
    assert issue.evidence_refs == (
        "document:plan:page:5:fragment:1",
        "document:plan:page:7:fragment:1",
    )


def test_go_live_before_resilience_and_readiness_testing_is_flagged() -> None:
    evidence = (
        _fragment(
            7,
            """
            Migration schedule
            Aurora Life cutover and go-live: 3 August 2027.
            Aurora Classics cutover and go-live: 7 September 2027.
            """,
        ),
        _fragment(
            11,
            """
            Failover and resilience testing runs 13-24 September 2027.
            Operational readiness testing runs 27 September-8 October 2027.
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    assert len(issues) == 1
    issue = issues[0]
    assert issue.artifact_type is ArtifactType.SCHEDULE
    assert issue.dimension == "Feasibility"
    assert issue.severity == "Low"
    assert "before resilience and readiness testing completes" in issue.title.casefold()
    assert issue.evidence_refs == (
        "document:plan:page:7:fragment:1",
        "document:plan:page:11:fragment:1",
    )


def test_volume_rate_and_delivery_window_are_reconciled() -> None:
    evidence = (
        _fragment(
            5,
            """
            The archive contains 480,000 hours. Sustained transfer capability is
            1,200 hours per week.
            """,
        ),
        _fragment(
            7,
            "Archive migration runs from 1 March 2027 to 25 February 2028.",
        ),
    )

    issues = audit_project_evidence(evidence)

    assert len(issues) == 1
    issue = issues[0]
    assert issue.artifact_type is ArtifactType.SCHEDULE
    assert issue.dimension == "Feasibility"
    assert issue.severity == "Critical"
    assert "throughput cannot complete the stated volume" in issue.title.casefold()
    assert "400.0 weeks" in issue.why
    assert issue.evidence_refs == (
        "document:plan:page:5:fragment:1",
        "document:plan:page:7:fragment:1",
    )


def test_table_headers_supply_context_to_compact_cutover_rows() -> None:
    evidence = (
        _fragment(
            3,
            """
            Aurora Sport exclusive rights require continuity during the live
            rights window from 12 November 2027 to 21 November 2027.
            """,
        ),
        _fragment(
            7,
            """
            Channel Migration Schedule Wave Channel Cutover date Risk
            2 Aurora Sport 13-15 November 2027 High
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    assert any("protected operating window" in issue.title.casefold() for issue in issues)


def test_hyphenated_subtotal_is_the_base_for_contingency_reconciliation() -> None:
    evidence = (
        _fragment(2, "Funding approval includes a 15% contingency."),
        _fragment(
            8,
            """
            Cost baseline
            Sub-total 28,400
            Contingency 3,100
            Total approved cost 31,500
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    assert any("contingency percentage" in issue.title.casefold() for issue in issues)


def test_month_level_migration_window_supports_throughput_math() -> None:
    evidence = (
        _fragment(
            5,
            """
            The archive comprises 480,000 hours. Sustained transfer capability is
            1,200 hours per week. Archive migration runs March 2027 to February 2028.
            """,
        ),
    )

    issues = audit_project_evidence(evidence)

    assert any("throughput cannot complete" in issue.title.casefold() for issue in issues)


def test_enterprise_system_contract_requires_privacy_exit_and_system_acceptance() -> None:
    evidence = (
        _fragment(
            2,
            """
            The supplier will implement a Manufacturing Execution System with
            electronic batch records, production visibility and a hosted managed
            service. Deliverables include configuration and Site 1 cutover.
            """,
        ),
        _fragment(
            4,
            """
            Acceptance applies to each deliverable. A deliverable is deemed accepted
            after five business days. No project-wide acceptance gate is stated.
            """,
        ),
        _fragment(
            6,
            """
            On termination the Client shall pay all sums due and return or destroy
            supplier confidential information.
            """,
        ),
    )

    issues = audit_project_evidence(evidence)
    titles = {issue.title for issue in issues}

    assert "Operational records have no data protection requirement" in titles
    assert "Hosted enterprise service has no exit or transition control" in titles
    assert "Deliverable acceptance has no system-level success gate" in titles


def test_invalid_calendar_date_does_not_fail_the_complete_evidence_read() -> None:
    evidence = (
        _fragment(
            8,
            "The period report was issued on 31 June 2026 and remains source evidence.",
        ),
    )

    # A source can contain a typo or a non-calendar date. It must remain available
    # to OSLO as text instead of crashing the complete analysis run.
    assert audit_project_evidence(evidence) == ()
