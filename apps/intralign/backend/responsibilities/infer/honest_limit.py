"""Honest-limit signal (DL-048 UP-4) — the truthful partial-analysis disclosure.

This is the DTM-0040 enforcement seam that was MISSING from Wave B. The
spend-gate (``RunBudget.can_afford``), the graceful degradation (defer the
remaining artifacts), and the ``ai_spend_recorded`` telemetry already exist
(``services/llm_provider/budget.py`` + ``infer/synthesis.py``). What did not
exist was the **honest-limit signal**: the truthful disclosure the DTM-0029
``HonestLimitDisclosure`` frontend renders when a run is budget-limited.

This module is a PURE builder — it maps an already-computed ``SynthesisResult``
(the degraded flag + the deferred artifacts the spend-gate produced) onto the
non-canonical ``HonestLimit`` presentation shape the frontend reads. It produces
no cognition, calls no provider, appends no CHR, and invents NO budget number —
the degrade trigger (the §4c per-run cap) lives ONLY in ``config.py``; here we
report the run's OWN coverage (generated vs deferred), which is data the run
already produced.

Epistemic-safety obligation (CONTEXT.md "honest-limit disclosure"; DL-048 UP-4):

- A budget-exceeded run is NEVER presented as complete — ``limited`` is True
  whenever the run degraded, so a partial orientation can't masquerade as a full
  result.
- The truthful disclosure (``reason`` + ``coverage_note``) is carried ALONGSIDE,
  never instead of, the commodity upgrade prompt — an attached ``upgrade`` never
  suppresses the disclosure (the frontend renders the disclosure first, always).

Shape (matches ``frontend/src/components/HonestLimitDisclosure.tsx``'s
``HonestLimit`` interface verbatim): ``limited: bool``, ``reason: str``,
``coverage_note: str``, optional ``upgrade: {message, cta_label}``. When the run
is complete the signal is ``{"limited": False}`` and the frontend renders nothing.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from shared.epistemic import PLANNING_ARTIFACT_TYPES

if TYPE_CHECKING:  # pragma: no cover - typing only
    from backend.responsibilities.infer.synthesis import SynthesisResult


def honest_limit_for_result(
    result: SynthesisResult,
    *,
    upgrade: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Build the ``HonestLimit`` signal from a (possibly degraded) synthesis run.

    Returns ``{"limited": False}`` for a complete run (the frontend shows
    nothing) and, for a degraded run, the truthful disclosure (``reason`` +
    ``coverage_note`` derived from the run's OWN generated/deferred counts) — plus
    the optional commodity ``upgrade`` carried ALONGSIDE (never instead-of).

    No invented number: ``reason``/``coverage_note`` are plain disclosure text +
    the run's own coverage counts; the budget cap that triggered the degrade is
    config (``config.budget_for_tier``), not embedded here.
    """
    if not result.degraded:
        # A complete run — not limited. The frontend renders nothing.
        return {"limited": False}

    generated = len(result.artifacts)
    deferred = len(result.deferred_artifact_types)
    total = len(PLANNING_ARTIFACT_TYPES)

    signal: dict[str, Any] = {
        "limited": True,
        # The reason coverage was reduced — shown verbatim (epistemic-safety duty).
        "reason": (
            "This run reached the analysis budget, so it covers only part of the "
            "project — what is shown is a partial orientation, not a full analysis."
        ),
        # Reduced-coverage detail from the run's OWN counts (no fabricated number):
        # how many planning artifacts were generated vs deferred to a Deep Pass.
        "coverage_note": (
            f"{generated} of {total} planning artifacts were generated; "
            f"{deferred} were deferred to a later, expanded analysis."
        ),
    }
    # The commodity Upgrade-Prompt (UP-4) rides ALONGSIDE — never instead of — the
    # disclosure above. It is optional commodity copy; the disclosure is mandatory.
    if upgrade:
        signal["upgrade"] = {
            "message": str(upgrade.get("message", "")),
            "cta_label": str(upgrade.get("cta_label", "")),
        }
    return signal
