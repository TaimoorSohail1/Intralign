"""Slice 0 (GO / NO-GO) — live-Gemma Time-to-First-MRI proof (DL-072 C3 · DL-046 · DL-070).

Discharges the one DL-072 condition that needs the LIVE internal-Gemma model: it measures
**Time-to-First-MRI** for a Fast Pass against the **ratified <60s ceiling** (Master Spec §20/M1),
on the **owner-confirmed Tier-1 (Free) envelope** (OPEN_TBD A1: ~20 artifacts / ~50k words /
1 active run). CI's "live" e2e (`tests/positive/evaluate/test_b2_live_chain_e2e.py`) uses a
RECORDED-fixture model — zero provider calls — which is exactly why DL-072 calls the live-Gemma
latency "unproven". This harness swaps in the real provider and repeats the run.

WHAT IT REUSES (unchanged wiring — faithful to the ratified live e2e test):
- `runner.submit_trigger("deep_pass", trigger, checkpointer=, emitter=, chr_repo=, stages=)`
- the composed Wave-B chain from `build_and_register_wave_b_chain(... tier="free", mode="fast",
  confidence_stage="orientation")`
- Time-to-First-MRI = wall-clock around `submit_trigger` (the same metric the ratified test asserts)

WHAT DIFFERS (the point of the proof):
- the provider is the LIVE one: `LLMProvider()` with NO recorded_model, requiring `OSLO_LLM_LIVE=1`
  and the internal-Gemma OpenAI-compatible `base_url` env (adapter.py) — set by the owner.
- it loops N>=30 runs and reports the distribution.

PASS / FAIL:
- RATIFIED GATE (hard): every run's Time-to-First-MRI < 60s  -> GO. Any breach at/under the
  Tier-1 envelope -> NO-GO (stop, file an engineering finding, escalate — do not "fix by assumption").
- REPORTED, NOT GATING: p50/p95 vs the *proposed* DL-046 targets (p50<=25s / p95<=50s). These are
  owner-TBD (OPEN_TBD A2) — printed for the owner, never auto-pass/fail (escalation E2).

RUN (owner environment only):
    # 1) Supabase up; export SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY / SUPABASE_DB_URL
    # 2) internal Gemma Llama runtime up; export OSLO_LLM_LIVE=1 + the base_url env (see .env.example)
    # 3) from apps/intralign/:
    python scripts/latency_proof/run_latency_proof.py --runs 30 --out latency_proof_result.json

This script is engineering tooling (non-canonical, apps/intralign/); it makes NO canonical change and writes
nothing to the repo. Its JSON output is the evidence attached to the Wave C exit-gate review.
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
import uuid
from typing import Any

# --- Ratified vs proposed thresholds -------------------------------------------------
TIME_TO_FIRST_MRI_CEILING_SECONDS = 60.0   # RATIFIED (Master Spec §20/M1) — the GO/NO-GO gate
PROPOSED_P50_SECONDS = 25.0                 # DL-046 PROPOSED, owner-TBD (OPEN_TBD A2) — report only
PROPOSED_P95_SECONDS = 50.0                 # DL-046 PROPOSED, owner-TBD (OPEN_TBD A2) — report only

# Owner-confirmed Tier-1 (Free) envelope — OPEN_TBD A1 (2026-06-05).
TIER1_ENVELOPE = {"artifacts": 20, "words": 50_000, "active_runs": 1}


def _require_live_env() -> None:
    """Fail loudly (not silently) if this is not a real live environment."""
    missing = [
        name
        for name in ("SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY", "SUPABASE_DB_URL")
        if not os.environ.get(name)
    ]
    if os.environ.get("OSLO_LLM_LIVE") != "1":
        missing.append("OSLO_LLM_LIVE=1")
    if missing:
        sys.exit(
            "NOT A LIVE ENVIRONMENT — this proof must run against live Gemma + Supabase.\n"
            "Missing: " + ", ".join(missing) + "\n"
            "See apps/intralign/README.md (Local bring-up) and .env.example for the internal-Gemma base_url."
        )


def _build_live_chain():
    """The composed Wave-B chain on the LIVE provider (no recorded fixture)."""
    from backend.orchestration.wave_b import build_and_register_wave_b_chain
    from backend.services.llm_provider import LLMProvider  # live: OSLO_LLM_LIVE=1 + base_url env
    from tests.positive.evaluate.test_b2_live_chain_e2e import (  # reuse the ratified wiring
        _infer_inputs_from_state,
    )

    # NOTE: the ratified e2e passes `prompt_suffix_for=response_key_directive`, which is a
    # RECORDED-fixture routing concept. For a LIVE run the chain builds prompts normally; if your
    # build still requires a `prompt_suffix_for`, pass the live equivalent here.
    # (Engineering to confirm the live builder signature — escalation E-harness, do not assume.)
    chain = build_and_register_wave_b_chain(
        provider=LLMProvider(),               # <-- LIVE (no recorded_model)
        extract_infer_inputs=_infer_inputs_from_state,
        tier="free",
        mode="fast",
        confidence_stage="orientation",
    )
    return chain


def _tier1_inputs() -> dict[str, Any]:
    """The Tier-1 envelope payload.

    ANTI-ASSUMPTION: a representative ~20-artifact / ~50k-word Tier-1 project is the owner's to
    supply (set OSLO_LATENCY_PROJECT to a JSON file). The synthetic pad below is a PLACEHOLDER so
    the harness runs end-to-end; replace it with a real project before recording the official proof.
    """
    path = os.environ.get("OSLO_LATENCY_PROJECT")
    if path:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    # Placeholder synthetic load at the envelope size (clearly flagged in the output).
    filler = ("requirement " * 8).strip()
    artifacts = [
        {"artifact_id": f"a{i}", "text": (filler + " ") * (50_000 // (20 * 2))}
        for i in range(TIER1_ENVELOPE["artifacts"])
    ]
    return {"artifacts": artifacts, "_synthetic_placeholder": True}


def _measure_one() -> float:
    """One Fast-Pass admit→infer→evaluate; returns wall-clock Time-to-First-MRI (seconds)."""
    from backend.orchestration import runner
    from backend.orchestration.checkpointer import build_checkpointer
    from backend.responsibilities.retain import ChrRepository
    from backend.services.observability.events import CollectingEventEmitter
    from supabase import create_client

    client = create_client(
        os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    )
    repo = ChrRepository(client=client)
    checkpointer = build_checkpointer()
    chain = _build_live_chain()
    stages = {"infer": chain._infer_stage, "evaluate": chain._evaluate_stage}

    project_id = str(uuid.uuid4())
    trigger = {
        "trigger_type": "knowledge-change",
        "project_id": project_id,
        "information_changed": True,
        "source": "latency-proof",
        "emissions": [],
        "inputs": {**_tier1_inputs(), "input_attestation_version": "v1"},
    }

    runner.reset_coalescing_guard()
    emitter = CollectingEventEmitter()
    started = time.perf_counter()
    result = runner.submit_trigger(
        "deep_pass",
        trigger,
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
        stages=stages,
    )
    elapsed = time.perf_counter() - started
    if getattr(result, "status", None) != "completed":
        raise RuntimeError(f"run did not complete: status={getattr(result, 'status', '?')}")
    return elapsed


def main() -> int:
    ap = argparse.ArgumentParser(description="Live-Gemma Time-to-First-MRI proof (Slice 0)")
    ap.add_argument("--runs", type=int, default=30, help="number of Fast-Pass runs (>=30)")
    ap.add_argument("--out", default="latency_proof_result.json", help="JSON evidence output")
    args = ap.parse_args()

    _require_live_env()

    samples: list[float] = []
    breaches: list[float] = []
    for i in range(args.runs):
        t = _measure_one()
        samples.append(t)
        flag = "  <-- BREACH (>=60s)" if t >= TIME_TO_FIRST_MRI_CEILING_SECONDS else ""
        if flag:
            breaches.append(t)
        print(f"run {i + 1:>3}/{args.runs}: {t:6.2f}s{flag}")

    p50 = statistics.median(samples)
    p95 = sorted(samples)[max(0, int(round(0.95 * len(samples))) - 1)]
    result = {
        "runs": args.runs,
        "envelope": TIER1_ENVELOPE,
        "synthetic_placeholder_used": os.environ.get("OSLO_LATENCY_PROJECT") is None,
        "ceiling_s": TIME_TO_FIRST_MRI_CEILING_SECONDS,
        "max_s": max(samples),
        "p50_s": p50,
        "p95_s": p95,
        "breaches": breaches,
        # RATIFIED gate result:
        "GATE_under_60s": len(breaches) == 0,
        "disposition": "GO" if not breaches else "NO-GO",
        # Reported-only (owner-TBD A2):
        "proposed_p50_target_s": PROPOSED_P50_SECONDS,
        "proposed_p95_target_s": PROPOSED_P95_SECONDS,
        "p50_within_proposed": p50 <= PROPOSED_P50_SECONDS,
        "p95_within_proposed": p95 <= PROPOSED_P95_SECONDS,
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)

    print("\n--- RESULT ---")
    print(f"  ratified <60s gate : {'GO ✅' if result['GATE_under_60s'] else 'NO-GO ❌'}")
    print(f"  max={result['max_s']:.2f}s  p50={p50:.2f}s  p95={p95:.2f}s")
    print(f"  (reported, owner-TBD A2) p50<=25s: {result['p50_within_proposed']}  "
          f"p95<=50s: {result['p95_within_proposed']}")
    if result["synthetic_placeholder_used"]:
        print("  WARNING: synthetic placeholder load used — set OSLO_LATENCY_PROJECT to a real "
              "Tier-1 project before recording the OFFICIAL proof.")
    print(f"  evidence -> {args.out}")
    return 0 if result["GATE_under_60s"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
