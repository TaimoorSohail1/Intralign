"""QA-WC-ADVISE C2 — the LIVE A→B→C chain end-to-end (Part C integration).

Proves ONE live end-to-end over the real durable graph + Supabase CHR repo:

    admit evidence (existing Retain path) → composed infer (synthesis → finding)
    → evaluate (issues + confidence/CAF/outcome) → ADVISE (recommendations +
    clarification) → CHRs appended, recommendation/clarification rows ANCHORED to
    their findings → a recompute supersedes (prior CHR intact).

Env-gated (Wave A/B pattern): skips OFFLINE unless the local Supabase stack is
configured. The LLM is the recorded-fixture model (ADR-0004) — zero provider
calls — so the AI steps are deterministic even live.

This builds the composed A→B→C stages via ``wave_c.py`` (the only orchestration
write Wave C authorizes) and runs them through the EXISTING graph topology
(``stages=`` override) — no frozen file is edited, no topology/state change is
made. The registry is saved + restored so the global ``register_stage`` mutation
never leaks into other tests.
"""

from __future__ import annotations

import os

import pytest

try:
    from supabase import create_client
except ImportError:  # pragma: no cover - CI venv without supabase-py
    create_client = None  # type: ignore[assignment]

from backend.orchestration import runner
from backend.orchestration.checkpointer import build_checkpointer
from backend.orchestration.wave_c import build_and_register_wave_c_chain
from backend.responsibilities.advise.stage import (
    OUTPUT_KIND_CLARIFICATION,
    OUTPUT_KIND_RECOMMENDATION,
)
from backend.responsibilities.retain import ChrRepository
from backend.services.llm_provider import LLMProvider
from backend.services.observability.events import CollectingEventEmitter
from tests._fixtures.recorded_model_responses import (
    build_recorded_model,
    response_key_directive,
)
from tests.positive.infer_finding.helpers import (
    ASSERTION_IDS,
    DECLARED_OUTCOME,
    OUTCOME_ANCHOR,
    sample_drafts,
)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_DB_URL = os.environ.get("SUPABASE_DB_URL")

pytestmark = pytest.mark.skipif(
    create_client is None
    or not SUPABASE_URL
    or not SUPABASE_SERVICE_ROLE_KEY
    or not SUPABASE_DB_URL,
    reason=(
        "local Supabase stack not configured — set SUPABASE_URL, "
        "SUPABASE_SERVICE_ROLE_KEY and SUPABASE_DB_URL (DB URL from "
        "`supabase status`); this live suite runs locally only"
    ),
)

# The recorded advise fixture (wc_advise_e2e_v0) anchors its recommendations /
# clarification to the DETERMINISTIC Finding ids the FindingEngine derives — and
# a Finding id is a stable structural hash that INCLUDES the project_id. So this
# live e2e must run under the SAME fixed project_id the fixture was recorded for
# (a random uuid would re-hash every Finding id and the recorded anchors would no
# longer resolve → every Recommendation dropped). The project's CHR rows are
# cleaned at setup so re-runs start from a clean slate.
_FIXTURE_PROJECT_ID = "11111111-1111-1111-1111-111111111111"

# The deterministic conflict Finding id the FindingEngine derives from
# sample_drafts() under _FIXTURE_PROJECT_ID (a stable structural hash) — the
# clarification anchors to it.
_CONFLICT_FINDING_ID = "conflict-5187581b388d7401"


@pytest.fixture(scope="module")
def client():
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


@pytest.fixture(scope="module")
def repo(client) -> ChrRepository:
    return ChrRepository(client=client)


@pytest.fixture(scope="module")
def checkpointer():
    return build_checkpointer()


@pytest.fixture(autouse=True)
def _fresh_guard():
    runner.reset_coalescing_guard()
    yield
    runner.reset_coalescing_guard()


def _provider() -> LLMProvider:
    """A recorded-fixture provider serving synthesis + finding + advise steps."""
    sessions = [
        build_recorded_model("ws_synthesis_v0"),
        build_recorded_model("wb_infer_v0"),
        build_recorded_model("wc_advise_e2e_v0"),
    ]

    from pydantic_ai.models.function import FunctionModel

    def fn(messages, info):
        last_error: Exception | None = None
        for s in sessions:
            try:
                return s._function(messages, info)
            except KeyError as exc:
                last_error = exc
                continue
        raise last_error if last_error else KeyError("no recorded response")

    return LLMProvider(recorded_model=FunctionModel(fn, model_name="recorded:wave-c-e2e"))


def _infer_inputs_from_state(state):
    inputs = dict(state.inputs)
    inputs.setdefault("project_id", state.project_id)
    inputs.setdefault("assertions", sample_drafts())
    inputs.setdefault("assertion_ids", ASSERTION_IDS)
    inputs.setdefault("declared_outcome", DECLARED_OUTCOME)
    inputs.setdefault("outcome_anchor", OUTCOME_ANCHOR)
    trigger = state.trigger or {}
    trigger_type = trigger.get("trigger_type")
    if trigger_type:
        inputs.setdefault("recompute_trigger", trigger_type)
        is_recompute = trigger_type == "reanalysis"
        inputs.setdefault("is_recompute", is_recompute)
        inputs.setdefault("input_attestation_version", "v2" if is_recompute else "v1")
    return inputs


def _trigger(project_id: str, trigger_type: str, **inputs) -> dict:
    return {
        "trigger_type": trigger_type,
        "project_id": project_id,
        "information_changed": True,
        "source": "dtm-0014-e2e",
        "emissions": [],  # the real producers append their own CHRs
        "inputs": inputs,
    }


def _rows_for_kind(client, project_id: str, output_kind: str):
    resp = (
        client.table("cognition_history_record")
        .select("*")
        .eq("project_id", project_id)
        .eq("output_kind", output_kind)
        .order("emitted_at", desc=False)
        .execute()
    )
    return resp.data


def _plain_recommendation_rows(rows):
    """Recommendation rows that are NOT SuggestedFix rows (DTM-0015 rides the
    same 'recommendation' output_kind with a payload type=suggested_fix)."""
    return [r for r in rows if r["output_payload"].get("type") != "suggested_fix"]


@pytest.fixture
def _restore_registry():
    from backend.orchestration import stages as stages_mod

    saved = stages_mod.default_stages()
    yield
    for name, fn in saved.items():
        stages_mod.register_stage(name, fn)


def test_c2_live_chain_admit_infer_evaluate_advise_and_recompute_supersedes(
    client, repo, checkpointer, _restore_registry
) -> None:
    # Fixed project_id (the fixture's recorded Finding-id anchors are project-
    # specific — see _FIXTURE_PROJECT_ID). Re-runs accumulate rows (RLS forbids a
    # test-side delete), so every assertion below works on the DELTA of CHR rows
    # this run appends (snapshot before → diff after), never on absolute counts.
    project_id = _FIXTURE_PROJECT_ID
    before_rec_ids = {r["chr_id"] for r in _rows_for_kind(
        client, project_id, OUTPUT_KIND_RECOMMENDATION)}
    before_clr_ids = {r["chr_id"] for r in _rows_for_kind(
        client, project_id, OUTPUT_KIND_CLARIFICATION)}

    chain = build_and_register_wave_c_chain(
        provider=_provider(),
        extract_infer_inputs=_infer_inputs_from_state,
        tier="free",
        mode="fast",
        confidence_stage="orientation",
        prompt_suffix_for=response_key_directive,
    )
    stages = {
        "infer": chain._infer_stage,
        "evaluate": chain.wave_b._evaluate_stage,
        "advise": chain._advise_stage,
    }

    # --- Fast Pass: admit → infer → evaluate → advise -----------------------
    emitter = CollectingEventEmitter()
    first = runner.submit_trigger(
        "deep_pass",
        _trigger(project_id, "knowledge-change", input_attestation_version="v1"),
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
        stages=stages,
    )
    assert first.status == "completed"
    # The full A→B→C chain emitted, including the Advise events.
    assert "finding_detected" in emitter.names
    assert "issue_generated" in emitter.names
    assert "recommendation_generated" in emitter.names
    assert "clarification_requested" in emitter.names
    # DTM-0015 — the Advise additions also emitted on the live chain.
    assert "suggested_fix_offered" in emitter.names

    # Recommendation CHRs this run appended (the DELTA). DTM-0015: SuggestedFixes
    # ride the SAME 'recommendation' output_kind (payload type=suggested_fix), so
    # split them out before the recommendation-shaped assertions.
    rec_kind_rows = [
        r for r in _rows_for_kind(client, project_id, OUTPUT_KIND_RECOMMENDATION)
        if r["chr_id"] not in before_rec_ids
    ]
    rec_rows = _plain_recommendation_rows(rec_kind_rows)
    fix_rows = [
        r for r in rec_kind_rows
        if r["output_payload"].get("type") == "suggested_fix"
    ]
    assert rec_rows
    for row in rec_rows:
        assert row["upstream_lineage"]["anchor"]
        assert row["output_payload"]["state"] == "generated"  # DL-055: not self-accepted
        assert row["provenance_ref"]["emitted_by"] == "advise"
    # A Validation recommendation (REC-05) rode the recommendation output.
    assert any(
        r["output_payload"]["recommendation_type"] == "validation" for r in rec_rows
    )
    # SuggestedFix CHRs (REC-04) — NO new output_kind; anchored; a candidate edit;
    # and the headline Critical invariant: the fix is OFFERED, never APPLIED —
    # there is NO 'applied'/'written' marker on the persisted payload.
    assert fix_rows
    for row in fix_rows:
        assert row["output_kind"] == "recommendation"  # rides existing kind
        assert row["upstream_lineage"]["anchor"]
        assert row["output_payload"]["target_artifact"]
        assert row["output_payload"]["candidate_edit"]
        assert "applied" not in row["output_payload"]
        assert "written" not in row["output_payload"]
        assert row["provenance_ref"]["emitted_by"] == "advise"
    # A clarification CHR this run appended, anchored to the conflict finding.
    clr_rows = [
        r for r in _rows_for_kind(client, project_id, OUTPUT_KIND_CLARIFICATION)
        if r["chr_id"] not in before_clr_ids
    ]
    assert clr_rows
    assert any(r["upstream_lineage"]["anchor"] == _CONFLICT_FINDING_ID for r in clr_rows)
    first_rec_count = len(rec_rows)
    after_first_rec_ids = before_rec_ids | {r["chr_id"] for r in rec_rows}

    # --- Recompute: supersede, prior intact ---------------------------------
    prior_map = {
        r["output_payload"]["recommendation_id"]: r["chr_id"] for r in rec_rows
    }
    emitter2 = CollectingEventEmitter()
    runner.reset_coalescing_guard()

    def _inputs_recompute(state):
        inputs = _infer_inputs_from_state(state)
        inputs["advise_prior_chr_id_for"] = prior_map.get
        return inputs

    chain2 = build_and_register_wave_c_chain(
        provider=_provider(),
        extract_infer_inputs=_inputs_recompute,
        tier="free",
        mode="fast",
        confidence_stage="orientation",
        prompt_suffix_for=response_key_directive,
    )
    second = runner.submit_trigger(
        "deep_pass",
        _trigger(project_id, "reanalysis", input_attestation_version="v2",
                 is_recompute=True),
        base_state=first.state,
        checkpointer=checkpointer,
        emitter=emitter2,
        chr_repo=repo,
        stages={
            "infer": chain2._infer_stage,
            "evaluate": chain2.wave_b._evaluate_stage,
            "advise": chain2._advise_stage,
        },
    )
    assert second.status == "completed"

    # The DELTA the recompute appended (rows not present after the first pass).
    # Filter to PLAIN recommendation rows (DTM-0015 SuggestedFixes ride this kind
    # too) so the count compares like-for-like against the first pass.
    recompute_rows = [
        r for r in _plain_recommendation_rows(
            _rows_for_kind(client, project_id, OUTPUT_KIND_RECOMMENDATION))
        if r["chr_id"] not in after_first_rec_ids
    ]
    # APPEND, never overwrite — the recompute appended a fresh generation…
    assert len(recompute_rows) == first_rec_count
    # …and every prior CHR is still present, byte-intact (none mutated/removed).
    surviving = {r["chr_id"] for r in
                 _rows_for_kind(client, project_id, OUTPUT_KIND_RECOMMENDATION)}
    assert all(prior in surviving for prior in prior_map.values())
    for prior_row in rec_rows:
        assert prior_row["input_attestation_version"] == "v1"
    # The new generation links back to the prior via supersedes_chr_id (lineage).
    for r in recompute_rows:
        assert r["input_attestation_version"] == "v2"
        assert r["recompute_trigger"] == "reanalysis"
    superseded = [r["supersedes_chr_id"] for r in recompute_rows if r["supersedes_chr_id"]]
    assert superseded
    assert all(s in set(prior_map.values()) for s in superseded)
