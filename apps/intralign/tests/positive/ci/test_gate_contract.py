"""Gate 2 (contract-traceability) — positive: valid citations and the Phase-I bypass pass."""

import pytest

from ci.gate_contract import (
    APPROVED_CONTRACT_IDS,
    BYPASS_LABEL,
    check_contract_citation,
    main,
    parse_labels,
)


@pytest.mark.parametrize("contract_id", sorted(APPROVED_CONTRACT_IDS))
def test_every_approved_contract_id_is_accepted(contract_id: str) -> None:
    passed, message = check_contract_citation(f"Implements {contract_id}.", [])
    assert passed
    assert contract_id in message


def test_contract_id_embedded_in_prose_is_accepted() -> None:
    body = (
        "## Summary\nWires the recompute backbone per the ratified contract "
        "IC-WA-00R (Wave A package); see traceability matrix."
    )
    passed, _ = check_contract_citation(body, [])
    assert passed


def test_bypass_label_passes_with_empty_body() -> None:
    passed, message = check_contract_citation("", [BYPASS_LABEL])
    assert passed
    assert BYPASS_LABEL in message


def test_bypass_label_passes_among_other_labels() -> None:
    passed, _ = check_contract_citation(None, ["docs", BYPASS_LABEL, "ci"])
    assert passed


def test_multiple_ids_including_valid_one_pass() -> None:
    passed, _ = check_contract_citation("IC-WA-001 and IC-WB-INFER", [])
    assert passed


def test_parse_labels_json_array() -> None:
    assert parse_labels('["phase-1-infra", "ci"]') == ["phase-1-infra", "ci"]


def test_parse_labels_comma_list_and_empty() -> None:
    assert parse_labels("a, b") == ["a", "b"]
    assert parse_labels(None) == []
    assert parse_labels("") == []


def test_cli_main_exits_zero_on_valid_citation() -> None:
    assert main(["--body", "Implements IC-WE-DISCLOSE", "--labels", "[]"]) == 0


def test_cli_main_exits_zero_on_bypass_label() -> None:
    assert main(["--body", "", "--labels", f'["{BYPASS_LABEL}"]']) == 0


def test_cli_main_reads_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PR_BODY", "Cites IC-WU-ACCEPT.")
    monkeypatch.setenv("PR_LABELS", "[]")
    assert main([]) == 0
