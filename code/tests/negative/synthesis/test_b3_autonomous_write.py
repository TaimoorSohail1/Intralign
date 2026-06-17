"""QA-WS-SYNTH B3 — no autonomous artifact write, no canonical-store-as-Attested.

A4.2/A4.5 (Critical): Infer must NOT autonomously edit a user's artifact, and
must NOT write a generated artifact (or the model) into the canonical store as
Attested-truth. The only Attested write Wave S causes is the user's EDIT,
admitted via the existing Retain admission path (DTM-0008) — which this slice
does not own and does not invent (decision #5).

These negatives introspect the Infer surface: it exposes ONLY synthesize/generate
(no edit/mutate/write-attested method), and its sole persistence is the
append-only CHR repo (OSLO-self-attested receipts) — it never targets an
``attested_assertion`` write path.
"""

from __future__ import annotations

import backend.responsibilities.infer.stage as stage_mod
import backend.responsibilities.infer.synthesis as synth_mod
from backend.responsibilities.infer.stage import (
    OUTPUT_KIND_PLANNING_ARTIFACT,
    OUTPUT_KIND_SYNTHESIZED_MODEL,
    run_synthesis_stage,
)
from tests.positive.synthesis.fakes import FakeStageContext
from tests.positive.synthesis.helpers import PROJECT, sample_drafts, synthesis_engine


def test_b3_infer_engine_exposes_no_autonomous_edit_method() -> None:
    """CRITICAL — there is no Infer method that mutates an existing artifact."""
    engine_methods = {m for m in dir(synth_mod.SynthesisEngine) if not m.startswith("_")}
    for autonomous in ("edit_artifact", "update_artifact", "mutate", "patch", "revise"):
        assert autonomous not in engine_methods


def test_b3_infer_modules_expose_no_attested_write_producer() -> None:
    """A4.2 — neither Infer module exports an Attested / canonical-write surface."""
    for module in (stage_mod, synth_mod):
        public = {n for n in dir(module) if not n.startswith("_")}
        for attested_write in (
            "admit_candidate",
            "write_attested",
            "AttestedAssertion",
            "attested_assertion",
        ):
            assert attested_write not in public


def test_b3_stage_persistence_is_chr_only_never_attested_assertion() -> None:
    """The stage's ONLY persistence is CHR appends — all OSLO-self-attested receipts."""
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
    # Every persisted row is a Wave-S CHR (a receipt) — none is an Attested assertion.
    kinds = {r["output_kind"] for r in ctx.chr_repo.rows}
    assert kinds == {OUTPUT_KIND_SYNTHESIZED_MODEL, OUTPUT_KIND_PLANNING_ARTIFACT}
    # The fake context carries no attested-assertion store at all (Infer never writes one).
    assert not hasattr(ctx, "attested_store")
    assert not hasattr(ctx.chr_repo, "attested_assertion")


def test_b3_stage_never_emits_a_retain_admission_event() -> None:
    """The user-edit -> Attested path is Retain's; Infer emits no admission event."""
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
    emitted = set(ctx.emitter.names)
    for retain_owned in ("knowledge_promoted", "user_acceptance_captured", "artifact_modified"):
        assert retain_owned not in emitted
