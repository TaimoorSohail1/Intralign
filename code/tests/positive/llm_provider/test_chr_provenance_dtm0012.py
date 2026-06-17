"""DTM-0012 — CHR provenance records the ACTUAL provider/model (DL-059 cond. 2).

After the switch to the internal gemma primary, each synthesis and Finding CHR
must stamp ``model_or_rule_version.provider == "internal"`` + the gemma model id
(merged with the existing prompt/rule version) — NOT the old hardcoded
``"openai"``. This is the model-consumption auditability fix (DL-054 cond. 3 /
DL-059 cond. 2). Offline: driven by recorded fixtures, zero provider calls.
"""

from __future__ import annotations

from backend.responsibilities.infer.finding_stage import run_finding_stage
from backend.responsibilities.infer.stage import (
    OUTPUT_KIND_PLANNING_ARTIFACT,
    OUTPUT_KIND_SYNTHESIZED_MODEL,
    run_synthesis_stage,
)
from backend.responsibilities.infer.synthesis import SYNTHESIS_VERSION
from backend.responsibilities.infer.finding import FINDING_VERSION
from backend.services.llm_provider import internal_model_id
from tests.positive.infer_finding.helpers import (
    ASSERTION_IDS as F_IDS,
)
from tests.positive.infer_finding.helpers import (
    DECLARED_OUTCOME,
    OUTCOME_ANCHOR,
    finding_engine,
)
from tests.positive.infer_finding.helpers import (
    sample_drafts as f_sample_drafts,
)
from tests.positive.infer_finding.helpers import (
    synthesized_model as f_synth_model,
)
from tests.positive.synthesis.fakes import FakeStageContext
from tests.positive.synthesis.helpers import PROJECT, sample_drafts, synthesis_engine


def test_synthesis_chr_records_internal_provider_and_gemma_id() -> None:
    """Synthesis + artifact CHRs stamp the resolved internal/gemma identity."""
    engine, _ = synthesis_engine()
    ctx = FakeStageContext()
    run_synthesis_stage(
        engine=engine,
        project_id=PROJECT,
        assertions=sample_drafts(),
        assertion_ids=[f"a{i}" for i in range(4)],
        ctx=ctx,
        input_attestation_version="v1",
        recompute_trigger=None,
        is_recompute=False,
    )
    gemma = internal_model_id()
    model_rows = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_SYNTHESIZED_MODEL)
    artifact_rows = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_PLANNING_ARTIFACT)
    assert model_rows and artifact_rows
    for row in model_rows + artifact_rows:
        mrv = row["model_or_rule_version"]
        assert mrv["provider"] == "internal"
        assert mrv["model"] == gemma
        assert mrv["model_version"] == SYNTHESIS_VERSION
        assert mrv["provider"] != "openai"  # the old hardcode is gone


def test_finding_chr_records_internal_provider_and_gemma_id() -> None:
    """Each Finding CHR stamps the resolved internal/gemma identity (not openai)."""
    engine, _ = finding_engine()
    ctx = FakeStageContext()
    run_finding_stage(
        engine=engine,
        project_id=PROJECT,
        assertions=f_sample_drafts(),
        assertion_ids=F_IDS,
        ctx=ctx,
        input_attestation_version="v1",
        recompute_trigger=None,
        is_recompute=False,
        model=f_synth_model(),
        declared_outcome=DECLARED_OUTCOME,
        outcome_anchor=OUTCOME_ANCHOR,
    )
    gemma = internal_model_id()
    finding_rows = ctx.chr_repo.rows_for_kind("finding")
    assert finding_rows
    for row in finding_rows:
        mrv = row["model_or_rule_version"]
        assert mrv["provider"] == "internal"
        assert mrv["model"] == gemma
        assert mrv["model_version"] == FINDING_VERSION
        assert mrv["provider"] != "openai"
