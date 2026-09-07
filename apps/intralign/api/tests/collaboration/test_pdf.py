from oslo_api.collaboration.pdf import (
    render_full_plan_pdf,
    render_report_pdf,
    render_snapshot_pdf,
)


def test_snapshot_pdf_contains_all_artifacts_evidence_and_governance_markers() -> None:
    snapshot = {
        "state": "current",
        "published_at": "2026-08-15T10:30:00Z",
        "summary": "A retained project summary.",
        "artifacts": [
            {
                "artifact_type": artifact_type,
                "title": f"{artifact_type.title()} title",
                "summary": f"{artifact_type.title()} summary",
                "evidence_refs": [f"document:plan:page:{index}:fragment:0"],
            }
            for index, artifact_type in enumerate(
                (
                    "intent",
                    "context",
                    "scope",
                    "requirements",
                    "work_breakdown",
                    "schedule",
                    "resources",
                ),
                start=1,
            )
        ],
        "evidence_citations": [
            {
                "reference": f"document:plan:page:{index}:fragment:0",
                "source_name": "Northstar plan.pdf",
                "location": f"Page {index}",
            }
            for index in range(1, 8)
        ],
        "assessment": {
            "confidence_index": 62,
            "clarity": "High",
            "alignment": "Moderate",
            "feasibility": "Low",
            "issues": [
                {
                    "title": "Open dependency",
                    "severity": "Critical",
                    "status": "open",
                    "evidence_refs": ["document:plan:page:8:fragment:1"],
                },
                {
                    "title": "Resolved dependency",
                    "severity": "Moderate",
                    "status": "resolved",
                },
            ],
        },
    }

    pdf = render_snapshot_pdf("DevNorth", snapshot)

    assert pdf.startswith(b"%PDF-1.4")
    assert b"/Type /Pages" in pdf
    assert b"Intent: Intent title" in pdf
    assert b"Resources: Resources title" in pdf
    assert b"Northstar plan.pdf - Page 7" in pdf
    assert b"document:plan:page:7:fragment:0" not in pdf
    assert b"Open dependency" in pdf
    assert b"Resolved dependency" not in pdf
    assert b"OSLO Project Readout" in pdf
    assert b"Source documents: 0; plan artifacts: 7" in pdf
    assert b"Analysis dated: 2026-08-15T10:30:00Z" in pdf
    assert b"It does not update the project or run analysis." in pdf
    assert b"OSLO advises; you decide." in pdf


def test_full_plan_pdf_joins_governed_tasks_by_retained_row_identity() -> None:
    snapshot = {
        "artifacts": [
            {
                "artifact_type": "work_breakdown",
                "content": {
                    "sections": [
                        {
                            "columns": ["WBS", "Item"],
                            "rows": [
                                ["1.0", "Commerce platform"],
                                ["1.1", "Checkout"],
                                ["1.1.1", "Implement payment gateway"],
                                ["1.1.2", "Test payment recovery"],
                            ],
                            "row_ids": ["delivery-1", "package-1", "task-1", "task-2"],
                            "row_provenance": [
                                "confirmed_by_user",
                                "confirmed_by_user",
                                "confirmed_by_user",
                                "from_oslo",
                            ],
                        }
                    ]
                },
            },
            {
                "artifact_type": "schedule",
                "content": {
                    "sections": [
                        {
                            "columns": ["Task", "Start", "End"],
                            "rows": [
                                ["Implement payment gateway", "2026-09-01", "2026-09-12"],
                                ["Test payment recovery", "", ""],
                            ],
                            "row_ids": ["task-1", "task-2"],
                        }
                    ]
                },
            },
            {
                "artifact_type": "resources",
                "content": {
                    "sections": [
                        {
                            "columns": ["Task", "Owner"],
                            "rows": [["Implement payment gateway", "Dana"]],
                            "row_ids": ["task-1"],
                        }
                    ]
                },
            },
        ]
    }

    pdf = render_full_plan_pdf(
        "Atlas launch",
        snapshot,
        analysis_completed_at="2026-08-17T08:30:00Z",
    )

    assert pdf.startswith(b"%PDF-1.4")
    assert b"Atlas launch - Full plan" in pdf
    assert b"Implement payment gateway | Checkout | Commerce platform | Dana" in pdf
    assert b"2026-09-01 - 2026-09-12" in pdf
    assert b"yours" in pdf
    assert b"Test payment recovery | Checkout | Commerce platform | - unowned" in pdf
    assert b"unscheduled" in pdf
    assert b"inferred" in pdf
    assert b"Read-only: exporting does not run analysis." in pdf


def test_full_plan_pdf_keeps_a_terminal_work_package_without_child_tasks() -> None:
    snapshot = {
        "artifacts": [
            {
                "artifact_type": "work_breakdown",
                "content": {
                    "sections": [
                        {
                            "heading": "Delivery",
                            "columns": ["WBS", "Item"],
                            "rows": [["1.0", "Launch commerce platform"]],
                            "row_ids": ["delivery-1"],
                            "row_provenance": ["confirmed_by_user"],
                        }
                    ]
                },
            }
        ]
    }

    pdf = render_full_plan_pdf("Atlas launch", snapshot)

    assert b"Launch commerce platform" in pdf
    assert b"Delivery" in pdf
    assert b"- unowned" in pdf
    assert b"unscheduled" in pdf


def test_report_pdf_uses_the_exact_shared_draft_sections() -> None:
    content = {
        "sections": [
            {
                "id": f"section-{index}",
                "title": f"Section {index}",
                "body": [f"Exact paragraph {index}"],
            }
            for index in range(1, 8)
        ]
    }

    pdf = render_report_pdf(
        "Halcyon",
        content,
        analysis_completed_at="2026-08-15T10:30:00Z",
    )

    assert pdf.startswith(b"%PDF-1.4")
    for index in range(1, 8):
        assert f"Section {index}".encode() in pdf
        assert f"Exact paragraph {index}".encode() in pdf
    assert b"Analysis dated: 2026-08-15T10:30:00Z" in pdf
    assert b"OSLO advises; you decide." in pdf
    assert b"does not run analysis" in pdf
    assert b"/Count 1" in pdf


def test_snapshot_pdf_anchors_a_stale_summary_to_the_current_project() -> None:
    snapshot = {
        "state": "current",
        "published_at": "2026-08-15T10:30:00Z",
        "summary": (
            "DevNorth 2026 is a developer conference. At the expanded stage, "
            "OSLO mapped the supplied evidence into 7 plan artifacts; "
            "13 open findings identify the main uncertainty."
        ),
        "artifacts": [],
        "assessment": {
            "confidence_index": 62,
            "clarity": "High",
            "alignment": "Moderate",
            "feasibility": "Low",
            "issues": [
                {"title": "Open dependency", "severity": "Critical", "status": "open"}
            ],
        },
    }

    pdf = render_snapshot_pdf("Atlas launch", snapshot)

    assert b"Atlas launch. At the expanded stage" in pdf
    assert b"1 open finding" in pdf
    assert b"DevNorth" not in pdf
