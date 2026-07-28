from oslo_api.analysis.artifact_edits import (
    artifact_content_hash,
    build_user_edit_evidence,
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
