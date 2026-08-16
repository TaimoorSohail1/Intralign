from oslo_api.analysis.artifact_edits import (
    artifact_content_hash,
    build_user_edit_evidence,
    project_work_breakdown_tasks,
)


def test_artifact_content_hash_is_stable_for_equivalent_key_order() -> None:
    first = {
        "sections": [
            {
                "heading": "Objectives",
                "body": "Improve care coordination.",
                "bullets": ["Reduce duplicate work."],
                "columns": [],
                "rows": [],
            }
        ]
    }
    second = {
        "sections": [
            {
                "rows": [],
                "columns": [],
                "bullets": ["Reduce duplicate work."],
                "body": "Improve care coordination.",
                "heading": "Objectives",
            }
        ]
    }

    assert artifact_content_hash(first) == artifact_content_hash(second)


def test_editor_identity_fields_do_not_create_a_material_artifact_change() -> None:
    stored = {
        "sections": [
            {
                "heading": "Milestones",
                "columns": ["Milestone", "Date"],
                "rows": [["Launch", "1 August 2026"]],
            }
        ]
    }
    browser = {
        "sections": [
            {
                "id": "section-schedule-1",
                "heading": "Milestones",
                "columns": ["Milestone", "Date"],
                "rows": [["Launch", "1 August 2026"]],
                "row_ids": ["row-schedule-1"],
            }
        ]
    }

    assert artifact_content_hash(stored) == artifact_content_hash(browser)


def test_user_edit_evidence_is_structured_readable_and_has_no_internal_marker() -> None:
    evidence = build_user_edit_evidence(
        artifact_type="intent",
        version=3,
        content={
            "sections": [
                {
                    "heading": "Objectives",
                    "body": "Improve care coordination.",
                    "bullets": ["Reduce duplicate work."],
                    "columns": ["Measure", "Target"],
                    "rows": [["Availability", "99.95%"]],
                }
            ]
        },
    )

    assert evidence.reference == "user:artifact:intent:version:3"
    assert evidence.source_name == "User-confirmed Intent edit"
    assert evidence.location == "Artifact version 3"
    assert "Objectives" in evidence.content
    assert "Improve care coordination." in evidence.content
    assert "Availability | 99.95%" in evidence.content
    assert "USER_ARTIFACT_EDIT" not in evidence.content
    assert "END_USER_ARTIFACT_EDIT" not in evidence.content


def test_shared_task_projection_does_not_put_rows_in_a_narrative_section() -> None:
    projected = project_work_breakdown_tasks(
        artifact_type="resources",
        content={
            "sections": [
                {
                    "heading": "Resource summary",
                    "body": "The delivery team is not fully staffed.",
                    "bullets": [],
                    "columns": [],
                    "rows": [],
                }
            ]
        },
        work_breakdown_content={
            "sections": [
                {
                    "heading": "Delivery",
                    "columns": ["WBS", "Item"],
                    "rows": [["1.1", "Validate production support handoff"]],
                    "row_ids": ["work-breakdown-section-1-row-1"],
                }
            ]
        },
    )

    assert projected["sections"][0]["rows"] == []
    assert projected["sections"][1]["columns"] == ["Resource", "Role", "Status"]
    assert projected["sections"][1]["rows"] == [
        ["Validate production support handoff", "", ""]
    ]
