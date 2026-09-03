from oslo_api.analysis.persistence import _public_snapshot_summary


def test_legacy_artifact_edit_envelope_is_never_returned_as_public_summary() -> None:
    value = (
        "USER_ARTIFACT_EDIT (untrusted project evidence) "
        'Artifact: intent Content: {"sections":[{"body":"private envelope"}]}. '
        "At the expanded stage, OSLO mapped the supplied evidence into 7 plan artifacts."
    )

    result = _public_snapshot_summary(value)

    assert result == (
        "At the expanded stage, OSLO mapped the supplied evidence into 7 plan artifacts."
    )
    assert "USER_ARTIFACT_EDIT" not in result
    assert "private envelope" not in result
