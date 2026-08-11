from oslo_api.collaboration.pdf import render_report_pdf, render_snapshot_pdf


def test_snapshot_pdf_contains_all_artifacts_evidence_and_governance_markers() -> None:
    snapshot = {
        "state": "current",
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
    assert b"It does not update the project or run analysis." in pdf


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

    pdf = render_report_pdf("Halcyon", content)

    assert pdf.startswith(b"%PDF-1.4")
    for index in range(1, 8):
        assert f"Section {index}".encode() in pdf
        assert f"Exact paragraph {index}".encode() in pdf
    assert b"/Count 1" in pdf
