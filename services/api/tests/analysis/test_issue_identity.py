from oslo_api.analysis.issue_identity import stabilize_issue_ids
from oslo_api.analysis.models import ArtifactType, Issue


def _issue(
    issue_id: str,
    *,
    title: str,
    why: str,
    dimension: str = "Clarity",
) -> Issue:
    return Issue(
        id=issue_id,
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension=dimension,
        severity="Critical",
        title=title,
        why=why,
        recommendation="Confirm the migration threshold.",
        evidence_refs=("document:plan:page:2:fragment:4",),
        clarification="What patient-match threshold is approved?",
    )


def test_semantically_equivalent_issue_keeps_previous_stable_id() -> None:
    previous = _issue(
        "ISS-MIGRATION",
        title="Production migration acceptance thresholds undefined",
        why="No approved patient-match threshold is documented.",
    )
    current = _issue(
        "MODEL-GENERATED-NEW-ID",
        title="Migration scope and patient-match threshold remain unconfirmed",
        why="The production migration has no confirmed patient-match threshold.",
        dimension="Feasibility",
    )

    stabilized = stabilize_issue_ids((current,), (previous,))

    assert stabilized[0].id == "ISS-MIGRATION"
    assert stabilized[0].dimension == "Feasibility"


def test_new_issue_receives_deterministic_id_independent_of_model_id() -> None:
    first = _issue(
        "MODEL-ONE",
        title="Acceptance criteria are insufficient for release",
        why="Release acceptance criteria are not measurable.",
    )
    second = _issue(
        "MODEL-TWO",
        title="Acceptance criteria are insufficient for release",
        why="Release acceptance criteria are not measurable.",
    )

    first_id = stabilize_issue_ids((first,), ())[0].id
    second_id = stabilize_issue_ids((second,), ())[0].id

    assert first_id == second_id
    assert first_id.startswith("ISS-REQUIREMENTS-")
