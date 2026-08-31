"""Gate 2 (contract-traceability) — negative: missing/invalid citations fail; no false bypass."""

import pytest

from ci.gate_contract import check_contract_citation, main


def test_empty_body_no_labels_fails() -> None:
    passed, message = check_contract_citation("", [])
    assert not passed
    assert "no contract id" in message


def test_none_body_fails() -> None:
    passed, _ = check_contract_citation(None, [])
    assert not passed


def test_body_without_contract_id_fails() -> None:
    passed, _ = check_contract_citation("Refactors the build, no contract.", [])
    assert not passed


def test_unapproved_contract_id_fails() -> None:
    passed, message = check_contract_citation("Implements IC-WZ-BOGUS.", [])
    assert not passed
    assert "IC-WZ-BOGUS" in message


def test_lowercase_id_is_not_a_citation() -> None:
    passed, _ = check_contract_citation("implements ic-wa-00r", [])
    assert not passed


def test_partial_id_is_not_a_citation() -> None:
    # "IC-WA" alone is not an approved id; the longer match must be exact.
    passed, _ = check_contract_citation("touches IC-WA stuff", [])
    assert not passed


def test_id_glued_into_longer_token_fails() -> None:
    # IC-WA-001X is a different (unapproved) token, not IC-WA-001.
    passed, _ = check_contract_citation("see IC-WA-001X", [])
    assert not passed


def test_other_labels_do_not_bypass() -> None:
    passed, _ = check_contract_citation("", ["phase-2-infra", "infra", "ci"])
    assert not passed


def test_bypass_label_in_body_text_does_not_bypass() -> None:
    # The label must be on the PR, not merely mentioned in the body.
    passed, _ = check_contract_citation("label me phase-1-infra please", [])
    assert not passed


def test_cli_main_exits_one_without_citation() -> None:
    assert main(["--body", "no contract here", "--labels", "[]"]) == 1


def test_cli_main_exits_one_with_empty_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PR_BODY", raising=False)
    monkeypatch.delenv("PR_LABELS", raising=False)
    assert main([]) == 1
