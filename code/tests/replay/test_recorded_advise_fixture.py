"""Recorded-fixture harness self-test for the WC-ADVISE fixture (ADR-0004).

NOT a "replay" (reserved — event-log reconstruction that does not re-run the
LLM; CONTEXT.md Register). It lives under tests/replay/ only because that is the
determinism-harness home, and it proves the DTM-0014 Advise derivation runs
ENTIRELY on recorded responses — PR CI makes ZERO provider calls. The two-axis
discipline (OBS-WC-ADVISE C3): recommendation/clarification TEXT is SEMANTIC
(many valid phrasings — never byte-pinned); the EMISSION surface (anchor, type,
stable id) is record-exact.
"""

from __future__ import annotations

import sys

from backend.responsibilities.advise.engine import AdviseEngine
from backend.services.llm_provider import LLMProvider, live_calls_enabled
from shared.epistemic import Finding
from tests._fixtures.recorded_model_responses import (
    build_recorded_model,
    load_fixture,
    response_key_directive,
)

_PROJECT = "11111111-1111-1111-1111-111111111111"


def _finding(fid: str, ftype: str, gap_kind, summary: str, anchors) -> Finding:
    return Finding(
        project_id=_PROJECT, finding_type=ftype, finding_id=fid, summary=summary,
        evidence_anchors=anchors, gap_kind=gap_kind,
        model_or_rule_version="wb-infer-finding-v0", mode="fast",
    )


def test_wc_advise_fixture_carries_a_baseline_stamp() -> None:
    fixture = load_fixture("wc_advise_v0")
    assert fixture.model_version
    assert fixture.config
    assert "recommendation" in fixture.responses
    assert "clarification" in fixture.responses


def test_advise_derivation_runs_entirely_on_recorded_responses() -> None:
    """The AI advise passes serve recorded output — zero live provider calls."""
    session = build_recorded_model("wc_advise_v0")
    provider = LLMProvider(recorded_model=session.model())
    engine = AdviseEngine(provider=provider, prompt_suffix_for=response_key_directive)
    before = set(sys.modules)
    gap = _finding("gap-coverage-1", "gap", "coverage",
                   "No constraint evidence is attested.", ("assertion-0",))
    conflict = _finding("conflict-1", "conflict", None,
                        "Attested assertions contradict (surfaced, not resolved).",
                        ("assertion-0", "assertion-1"))
    result = engine.derive(project_id=_PROJECT, findings=[gap, conflict])
    # Both AI passes (recommendation + clarification) were served by the fixture.
    assert session.call_count == 2
    assert set(session.served_keys) == {"recommendation", "clarification"}
    # Record-exact axis: the emission surface (anchor) resolves to the findings.
    assert {r.anchor for r in result.recommendations} <= {"gap-coverage-1", "conflict-1"}
    assert all(c.anchor == "conflict-1" for c in result.clarifications)
    # No provider SDK imported by exercising the harness.
    newly = set(sys.modules) - before
    assert not any(
        m.startswith(("pydantic_ai.models.openai", "pydantic_ai.models.anthropic"))
        for m in newly
    )


def test_pr_ci_never_enables_live_calls() -> None:
    assert not live_calls_enabled()
