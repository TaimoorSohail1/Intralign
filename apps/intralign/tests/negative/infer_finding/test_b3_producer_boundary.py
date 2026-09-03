"""QA-WB-INFER B3 (the one-producer boundary) — Infer owns Findings ONLY.

Introspective negatives proving Infer does NOT cross into Evaluate / Advise /
Retain: the Finding modules export no severity/confidence/CAF producer, no
recommendation/clarification producer, and no canonical-write / promote-to-
Attested path. Infer surfaces conflicts (it never resolves one into canonical
truth). These mirror the DTM-0009 perceive-boundary introspection style.
"""

from __future__ import annotations

import ast
from pathlib import Path

import backend.responsibilities.infer.finding as finding_mod
import backend.responsibilities.infer.finding_stage as finding_stage_mod

_FINDING_PY = Path(finding_mod.__file__)
_STAGE_PY = Path(finding_stage_mod.__file__)


def test_b3_finding_module_exports_no_evaluate_or_advise_producer() -> None:
    """A4.1-style introspection — no Confidence/CAF/Issue/Recommendation surface."""
    for module in (finding_mod, finding_stage_mod):
        public = {name for name in dir(module) if not name.startswith("_")}
        for forbidden in (
            "Confidence", "CAFAssessment", "OutcomeConfidence", "Issue",
            "Recommendation", "ClarificationRequest", "Severity", "Reliability",
        ):
            assert forbidden not in public, f"{module.__name__} leaks {forbidden}"


def test_b3_finding_module_names_no_severity_or_confidence_compute() -> None:
    """No function in the Finding modules computes severity/confidence/CAF."""
    for path in (_FINDING_PY, _STAGE_PY):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                lowered = node.name.lower()
                assert "severity" not in lowered
                assert "confidence" not in lowered or "stage" in lowered
                assert "recommend" not in lowered
                assert "clarif" not in lowered


def test_b3_finding_modules_write_no_canonical_attested_table() -> None:
    """Infer never writes canonical / promotes a Finding to Attested.

    The only persistence is the generic CHR append (Derived receipt) through
    ctx.chr_repo; no canonical-table client/insert appears in these modules.
    """
    for path in (_FINDING_PY, _STAGE_PY):
        src = path.read_text(encoding="utf-8")
        # No direct DB/table write surface (Supabase/Neo4j/INSERT) in Infer.
        for banned in ("supabase", "create_client", ".table(", "INSERT INTO", "attested_assertion"):
            assert banned not in src, f"{path.name} appears to write canonical state ({banned})"


def test_b3_conflict_is_surfaced_not_resolved() -> None:
    """A conflict Finding SURFACES the contradiction — it picks no winner."""
    from tests.positive.infer_finding.helpers import (
        ASSERTION_IDS,
        finding_engine,
        sample_drafts,
    )

    engine, _ = finding_engine()
    conflicts = engine.derive_conflicts(
        project_id="p", assertions=sample_drafts(), assertion_ids=ASSERTION_IDS
    )
    assert len(conflicts) == 1
    c = conflicts[0]
    # Anchored to BOTH sides; the engine never collapses them to a truth value.
    assert len(c.evidence_anchors) == 2
    assert "surfaced, not resolved" in c.summary
    # A conflict Finding carries no "resolution"/"winner"/"truth" field at all.
    assert not hasattr(c, "resolution")
    assert not hasattr(c, "resolved_value")
