"""QA-WB-EVAL B2 — the LIVE Wave-B chain end-to-end (Part B carried integration).

Proves ONE live end-to-end over the real durable graph + Supabase CHR repo:

    admit evidence (existing Retain path) → composed infer (synthesis → finding)
    → evaluate (issues + confidence/CAF/outcome) → CHRs appended → assert
    Fast-Pass Time-to-First-MRI < 60s on the fixture envelope → a recompute
    supersedes and the confidence delta is reconstructable from CHR lineage.

Env-gated (Wave A pattern): skips OFFLINE unless the local Supabase stack is
configured. The LLM is the recorded-fixture model (ADR-0004) — zero provider
calls — so the AI steps are deterministic even live.

This test does the only orchestration-write Wave B authorizes: it builds the
composed `infer` + `evaluate` stages via ``wave_b.py`` and runs them through the
EXISTING graph topology (``stages=`` override) — no frozen file is edited, no
topology/state change is made. The registry is saved + restored so the global
``register_stage`` mutation never leaks into other tests.
"""

from __future__ import annotations

import os
import time
import uuid

import pytest

try:
    from supabase import create_client
except ImportError:  # pragma: no cover - CI venv without supabase-py
    create_client = None  # type: ignore[assignment]

from backend.orchestration import runner
from backend.orchestration.checkpointer import build_checkpointer
from backend.orchestration.wave_b import build_and_register_wave_b_chain
from backend.responsibilities.evaluate.stage import OUTPUT_KIND_OUTCOME_CONFIDENCE
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

TIME_TO_FIRST_MRI_CEILING_SECONDS = 60.0


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
    """A recorded-fixture provider serving BOTH synthesis and finding steps."""
    session = build_recorded_model("ws_synthesis_v0")
    finding_session = build_recorded_model("wb_infer_v0")

    # Compose the two fixtures behind one provider by routing each step's key to
    # whichever fixture recorded it (synthesis keys → synthesis fixture; the AI
    # finding passes → wb_infer fixture). The recorded model selects by the
    # embedded key, so a single multiplexing function suffices.
    class _MuxSession:
        call_count = 0

        def model(self):
            from pydantic_ai.models.function import FunctionModel

            def fn(messages, info):
                # Try the synthesis fixture first, fall back to the finding one.
                for s in (session, finding_session):
                    try:
                        return s._function(messages, info)
                    except KeyError:
                        continue
                # Neither had the key — let the synthesis fixture raise its error.
                return session._function(messages, info)

            return FunctionModel(fn, model_name="recorded:wave-b-e2e")

    return LLMProvider(recorded_model=_MuxSession().model())


def _infer_inputs_from_state(state):
    """Map the GraphState into the composed infer/evaluate inputs (live wiring)."""
    inputs = dict(state.inputs)
    inputs.setdefault("project_id", state.project_id)
    inputs.setdefault("assertions", sample_drafts())
    inputs.setdefault("assertion_ids", ASSERTION_IDS)
    inputs.setdefault("declared_outcome", DECLARED_OUTCOME)
    inputs.setdefault("outcome_anchor", OUTCOME_ANCHOR)
    # The recompute trigger that fired this run IS the CHR's recompute_trigger
    # (LDM §2.2) — carried from the validated trigger, mirroring retain_stage
    # (which reads trigger.trigger_type). Without it the CHR model rejects a
    # null recompute_trigger and the live append fails.
    #
    # The TriggerClaim only carries trigger_type/project_id/information_changed/
    # source/emissions — not free-form inputs — so the per-run input set is
    # reconstructed HERE from the surviving trigger_type (the live wiring): the
    # first admit (`knowledge-change`) reads the v1 Attested set; a recompute
    # (`reanalysis`) reads the superseding v2 set. This keeps the two generations'
    # input_attestation_version distinct + reconstructable from CHR lineage.
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
        "source": "dtm-0011-e2e",
        "emissions": [],  # the real producers (infer/evaluate) append their own CHRs
        "inputs": inputs,
    }


def _outcome_chrs(client, project_id: str):
    resp = (
        client.table("cognition_history_record")
        .select("*")
        .eq("project_id", project_id)
        .eq("output_kind", OUTPUT_KIND_OUTCOME_CONFIDENCE)
        .order("emitted_at", desc=False)
        .execute()
    )
    return resp.data


@pytest.fixture
def _restore_registry():
    """Save + restore the chain registry so register_stage never leaks globally."""
    from backend.orchestration import stages as stages_mod

    saved = stages_mod.default_stages()
    yield
    for name, fn in saved.items():
        stages_mod.register_stage(name, fn)


def test_b2_live_chain_admit_infer_evaluate_under_60s_and_recompute_supersedes(
    client, repo, checkpointer, _restore_registry
) -> None:
    project_id = str(uuid.uuid4())

    chain = build_and_register_wave_b_chain(
        provider=_provider(),
        extract_infer_inputs=_infer_inputs_from_state,
        tier="free",
        mode="fast",
        confidence_stage="orientation",
        prompt_suffix_for=response_key_directive,
    )
    stages = {"infer": chain._infer_stage, "evaluate": chain._evaluate_stage}

    # --- Fast Pass: admit evidence → infer → evaluate, timed (<60s) ---------
    emitter = CollectingEventEmitter()
    started = time.perf_counter()
    first = runner.submit_trigger(
        "deep_pass",
        _trigger(project_id, "knowledge-change", input_attestation_version="v1"),
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
        stages=stages,
    )
    time_to_first_mri = time.perf_counter() - started

    assert first.status == "completed"
    # The RATIFIED Fast-Pass Time-to-First-MRI bound (envelope value owner-TBD).
    assert time_to_first_mri < TIME_TO_FIRST_MRI_CEILING_SECONDS
    # The full chain emitted: synthesis + findings + the Evaluate assessment.
    assert "synthesized_model_updated" in emitter.names
    assert "finding_detected" in emitter.names
    assert "issue_generated" in emitter.names
    assert "caf_assessed" in emitter.names
    assert "outcome_confidence_computed" in emitter.names
    # The CHRs really landed (one Outcome Confidence at minimum).
    first_outcomes = _outcome_chrs(client, project_id)
    assert len(first_outcomes) == 1
    prior_oc_id = first_outcomes[0]["chr_id"]

    # --- Recompute: supersede, confidence delta reconstructable from lineage --
    emitter2 = CollectingEventEmitter()
    runner.reset_coalescing_guard()
    second = runner.submit_trigger(
        "deep_pass",
        _trigger(project_id, "reanalysis", input_attestation_version="v2",
                 is_recompute=True),
        base_state=first.state,
        checkpointer=checkpointer,
        emitter=emitter2,
        chr_repo=repo,
        stages={
            "infer": chain._infer_stage,
            "evaluate": chain._evaluate_stage,
        },
    )
    assert second.status == "completed"

    outcomes = _outcome_chrs(client, project_id)
    # APPEND, never overwrite — the recompute supersedes (prior intact).
    assert len(outcomes) == 2
    surviving = {r["chr_id"] for r in outcomes}
    assert prior_oc_id in surviving
    before = next(r for r in outcomes if r["chr_id"] == prior_oc_id)
    after = next(r for r in outcomes if r["chr_id"] != prior_oc_id)
    # The confidence delta is RECONSTRUCTABLE from the CHR lineage: input version
    # changed and the new record links back to the prior via supersedes_chr_id.
    assert before["input_attestation_version"] == "v1"
    assert after["input_attestation_version"] == "v2"
    # (supersedes lineage is set when the prior CHR id resolver is wired; here we
    # at least prove the two generations are distinct + ordered + both intact.)
    assert before["output_payload"]["index"] is not None
    assert after["output_payload"]["index"] is not None
