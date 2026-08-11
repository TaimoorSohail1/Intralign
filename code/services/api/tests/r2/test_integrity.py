import pytest

from oslo_api.analysis.integrity import (
    IntegrityArtifact,
    IntegrityInputs,
    IntegrityIssue,
    OutcomeCheckpoint,
    build_integrity_read,
    compute_integrity,
)


def test_integrity_composes_three_normalized_pillars_through_the_weakest_gate() -> None:
    integrity = compute_integrity(
        IntegrityInputs(
            viable_artifacts=3,
            load_bearing_artifacts=4,
            grounded_items=4,
            load_bearing_items=6,
            registered_checkpoints=2,
            needed_checkpoints=3,
        )
    )

    assert integrity.level == "Developing"
    assert integrity.limiting_pillar == "Grounding"
    assert integrity.posture == "moment-in-time"
    assert integrity.tracking == "pending-execution"
    assert {
        pillar.key: (pillar.band, pillar.basis)
        for pillar in integrity.decomposition
    } == {
        "Viability": ("Solid", 0.75),
        "Grounding": ("Developing", 2 / 3),
        "Adaptability": ("Developing", 2 / 3),
    }


def test_inferred_primary_outcome_caps_grounding_at_weak() -> None:
    integrity = compute_integrity(
        IntegrityInputs(
            viable_artifacts=4,
            load_bearing_artifacts=4,
            grounded_items=6,
            load_bearing_items=6,
            registered_checkpoints=3,
            needed_checkpoints=3,
            outcome_root_grounded=False,
        )
    )

    grounding = next(
        pillar for pillar in integrity.decomposition if pillar.key == "Grounding"
    )
    assert grounding.band == "Weak"
    assert grounding.basis == 1
    assert integrity.level == "Weak"
    assert integrity.limiting_pillar == "Grounding"


def test_false_confidence_issue_and_grounding_share_one_detector() -> None:
    inferred = IntegrityArtifact(
        key="scope",
        title="Scope",
        viable=False,
        reads_strong=True,
        grounded_items=1,
        inferred_items=3,
    )
    checkpoint = OutcomeCheckpoint(
        id="CHK-DELIVERY",
        workstream="Delivery",
        leading_indicator="Validated outcomes",
        timing="Before release",
        lever="Change scope or sequence",
        registered=True,
    )

    before = build_integrity_read(
        artifacts=(inferred,),
        checkpoints=(checkpoint,),
    )

    assert [issue.id for issue in before.issues] == ["ISS-FC-SCOPE"]
    assert before.issues[0].dim == "Grounding"
    assert before.issues[0].finding_type == "False Confidence"
    assert before.issues[0].recommendation_from_oslo is True

    after = build_integrity_read(
        artifacts=(
            IntegrityArtifact(
                key="scope",
                title="Scope",
                viable=True,
                reads_strong=True,
                grounded_items=4,
                inferred_items=0,
            ),
        ),
        checkpoints=(checkpoint,),
    )

    assert after.issues == ()
    grounding = next(
        pillar for pillar in after.integrity.decomposition if pillar.key == "Grounding"
    )
    assert grounding.band == "Sound"


def test_checkpoint_proposal_counts_only_after_registration() -> None:
    proposed = OutcomeCheckpoint(
        id="CHK-SPONSORSHIP",
        workstream="Sponsorship",
        leading_indicator="Confirmed sponsor dollars against target",
        timing="Two weeks before committed spend",
        lever="Trim discretionary spend or extend outreach",
        registered=False,
    )

    before = build_integrity_read(artifacts=(), checkpoints=(proposed,))

    assert [issue.id for issue in before.issues] == ["ISS-CP-CHK-SPONSORSHIP"]
    assert before.issues[0].dim == "Adaptability"
    assert before.issues[0].finding_type == "Coverage Gap"
    assert before.issues[0].section == "Schedule"
    assert "Confirmed sponsor dollars against target" in before.issues[0].recommendation
    adaptability_before = next(
        pillar
        for pillar in before.integrity.decomposition
        if pillar.key == "Adaptability"
    )
    assert adaptability_before.band == "Fragile"

    after = build_integrity_read(
        artifacts=(),
        checkpoints=(
            OutcomeCheckpoint(
                id=proposed.id,
                workstream=proposed.workstream,
                leading_indicator=proposed.leading_indicator,
                timing=proposed.timing,
                lever=proposed.lever,
                registered=True,
            ),
        ),
    )

    assert after.issues == ()
    adaptability_after = next(
        pillar
        for pillar in after.integrity.decomposition
        if pillar.key == "Adaptability"
    )
    assert adaptability_after.band == "Sound"


def test_unified_queue_ranks_across_pillars_without_cross_contaminating_viability() -> None:
    viability_issue = IntegrityIssue(
        id="ISS-CAF-SCOPE",
        dim="Viability",
        dims=("Viability",),
        finding_type="Clarity Gap",
        section="Scope",
        severity="Critical",
        status="open",
        title="Outcome boundary is undefined",
        why="The plan cannot distinguish outcome-bearing work from optional work.",
        recommendation="Define the outcome boundary.",
    )
    artifact = IntegrityArtifact(
        key="scope",
        title="Scope",
        viable=False,
        reads_strong=True,
        grounded_items=1,
        inferred_items=3,
        primary_outcome=True,
    )
    checkpoint = OutcomeCheckpoint(
        id="CHK-DELIVERY",
        workstream="Delivery",
        leading_indicator="Validated outcomes",
        timing="Before release",
        lever="Change scope or sequence",
        registered=False,
    )

    read = build_integrity_read(
        artifacts=(artifact,),
        checkpoints=(checkpoint,),
        issues=(viability_issue,),
    )

    assert [issue.id for issue in read.issues] == [
        "ISS-CAF-SCOPE",
        "ISS-FC-SCOPE",
        "ISS-CP-CHK-DELIVERY",
    ]
    assert {issue.dim for issue in read.issues} == {
        "Viability",
        "Grounding",
        "Adaptability",
    }
    viability = next(
        pillar
        for pillar in read.integrity.decomposition
        if pillar.key == "Viability"
    )
    assert viability.basis == 0
    assert viability.band == "Fragile"


def test_open_critical_viability_issue_stays_ahead_of_false_confidence() -> None:
    critical = IntegrityIssue(
        id="ISS-CAF-INTENT",
        dim="Viability",
        dims=("Viability",),
        finding_type="Alignment Gap",
        section="Intent",
        severity="Critical",
        status="open",
        title="Primary outcome conflicts with the governing intent",
        why="The outcome path cannot be read consistently.",
        recommendation="Reconcile the stated outcome with the governing intent.",
    )
    inferred = IntegrityArtifact(
        key="scope",
        title="Scope",
        viable=True,
        reads_strong=True,
        grounded_items=0,
        inferred_items=4,
    )

    read = build_integrity_read(
        artifacts=(inferred,),
        checkpoints=(),
        issues=(critical,),
    )

    assert read.integrity.limiting_pillar == "Grounding"
    assert [issue.id for issue in read.issues[:2]] == [
        "ISS-CAF-INTENT",
        "ISS-FC-SCOPE",
    ]


@pytest.mark.parametrize(
    ("numerator", "denominator", "expected"),
    [
        (0, 8, "Fragile"),
        (2, 8, "Weak"),
        (4, 8, "Developing"),
        (6, 8, "Solid"),
        (8, 8, "Sound"),
    ],
)
def test_integrity_uses_the_fixed_five_band_boundaries(
    numerator: int,
    denominator: int,
    expected: str,
) -> None:
    read = compute_integrity(
        IntegrityInputs(
            viable_artifacts=numerator,
            load_bearing_artifacts=denominator,
            grounded_items=denominator,
            load_bearing_items=denominator,
            registered_checkpoints=denominator,
            needed_checkpoints=denominator,
        )
    )

    assert read.decomposition[0].band == expected


def test_integrity_is_proportional_when_plan_size_changes() -> None:
    small = compute_integrity(IntegrityInputs(1, 2, 1, 2, 1, 2))
    large = compute_integrity(IntegrityInputs(5, 10, 5, 10, 5, 10))

    assert [pillar.band for pillar in small.decomposition] == [
        pillar.band for pillar in large.decomposition
    ]
    assert small.level == large.level == "Developing"


@pytest.mark.parametrize(
    ("viability", "grounding", "adaptability", "limiter"),
    [
        (1, 1, 2, "Viability"),
        (2, 1, 1, "Grounding"),
        (2, 2, 1, "Adaptability"),
    ],
)
def test_foundation_first_tie_breaking_is_deterministic(
    viability: int,
    grounding: int,
    adaptability: int,
    limiter: str,
) -> None:
    integrity = compute_integrity(
        IntegrityInputs(viability, 2, grounding, 2, adaptability, 2)
    )

    assert integrity.limiting_pillar == limiter


def test_flagging_grounds_the_read_without_raising_viability() -> None:
    before = build_integrity_read(
        artifacts=(
            IntegrityArtifact(
                key="requirements",
                title="Requirements",
                viable=False,
                reads_strong=False,
                grounded_items=0,
                inferred_items=1,
            ),
        ),
        checkpoints=(),
    )
    after_flag = build_integrity_read(
        artifacts=(
            IntegrityArtifact(
                key="requirements",
                title="Requirements",
                viable=False,
                reads_strong=False,
                grounded_items=1,
                inferred_items=0,
            ),
        ),
        checkpoints=(),
    )

    assert before.integrity.decomposition[0] == after_flag.integrity.decomposition[0]
    assert before.integrity.decomposition[1].band == "Fragile"
    assert after_flag.integrity.decomposition[1].band == "Sound"


def test_resolving_issue_count_cannot_change_any_integrity_pillar() -> None:
    artifact = IntegrityArtifact(
        key="scope",
        title="Scope",
        viable=True,
        reads_strong=False,
        grounded_items=1,
        inferred_items=0,
    )
    resolved = IntegrityIssue(
        id="ISS-OLD",
        dim="Viability",
        dims=("Viability",),
        finding_type="Clarity Gap",
        section="Scope",
        severity="Critical",
        status="resolved",
        title="Previously unclear boundary",
        why="Historical finding.",
        recommendation="No action remains.",
    )

    without_fix_count = build_integrity_read(artifacts=(artifact,), checkpoints=())
    with_resolved_issue = build_integrity_read(
        artifacts=(artifact,), checkpoints=(), issues=(resolved,)
    )

    assert with_resolved_issue.integrity == without_fix_count.integrity


def test_each_outcome_workstream_requires_its_own_registered_checkpoint() -> None:
    checkpoints = (
        OutcomeCheckpoint(
            id="CHK-ADOPTION",
            workstream="Adoption",
            leading_indicator="Weekly active teams",
            timing="Before rollout expansion",
            lever="Change enablement or rollout sequence",
            registered=True,
        ),
        OutcomeCheckpoint(
            id="CHK-RELIABILITY",
            workstream="Reliability",
            leading_indicator="Error budget consumption",
            timing="Before migration cutover",
            lever="Change cutover scope or timing",
            registered=False,
        ),
    )

    read = build_integrity_read(artifacts=(), checkpoints=checkpoints)

    assert [issue.id for issue in read.issues] == ["ISS-CP-CHK-RELIABILITY"]
    adaptability = next(
        pillar for pillar in read.integrity.decomposition if pillar.key == "Adaptability"
    )
    assert adaptability.band == "Developing"
