# AI is tested against recorded model-response fixtures, not live calls in CI

Wave B is the first time OSLO calls an LLM (`services/llm_provider` — Pydantic AI adapter,
OpenAI primary / Anthropic fallback per DL-054). Two ratified obligations collide:
determinism (`DETERMINISM_CALIBRATION_NOTE_001`, Testing Strategy §6/§11) requires a
repeatable test baseline, while LLMs are stochastic and metered. Token budgets (DL-048 /
Open-TBD A6) make live-on-every-CI-run both flaky and a real cost.

We resolve this by pinning the model component of the determinism baseline. The baseline is
the **(configuration × fixture × model-version)** triple (DT-5/DT-10). For any AI step,
CI runs against a **recorded model-response fixture** — a captured, version-stamped model
output that stands in for the model-version × fixture components of that triple. The live
model runs only in dev (to author/refresh fixtures) and in a separate nightly job. PR CI
never calls a provider: it is deterministic, free, and offline.

Assertions still honour the determinism tiers: rule/formula steps replay **exact**;
AI-numeric (Confidence/CAF/Reliability/Outcome Confidence) within **±7 pts & same band**;
AI-text (Findings/Issues/Recommendations) **semantic-equivalent**. A recorded fixture makes
those tiers checkable without re-running the model.

## Naming constraint (do not violate)

**"Replay" is a reserved canonical term** (Determinism Note §5; DT-3; REPLAY-T1…T6): it
means event-log state reconstruction that **explicitly does not re-run the LLM**. The
LLM test-double is **not** a "replay" and **not** a "cassette" — those names collide with
canon. It is a **recorded model-response fixture**, versioned as the model/fixture
component of the determinism baseline. This distinction is recorded in `CONTEXT.md` (and
belongs in the canonical Disambiguation Register, DL-053 — an owner follow-up).

## Status

accepted — owner direction, 2026-06-16. (Provider routing itself is unchanged from DL-054;
this ADR governs only how AI is exercised under test.)

## Considered Options

- **Live model on every CI run, temp=0 + band tolerance** — rejected: stochastic across
  runs (flaky even at temp 0), spends tokens against the DL-048 budget on every push, and
  needs provider keys in CI secrets.
- **Recorded model-response fixtures, live in dev + nightly (chosen)** — deterministic,
  offline, free PR CI; matches the baseline-triple definition and the existing
  Finding/Confidence fixture-library specs.

## Consequences

- The nightly live-model run is a **baseline-update check, not a regression check**: per
  DT-6 a model-version difference is a **new baseline**, never a regression. When the
  nightly diverges, the action is to review and re-record fixtures (bumping the model
  component), not to fail the build as a defect.
- Each recorded fixture carries its `model_version` + `config` stamp so a baseline change
  is auditable and a stale fixture is detectable.
- Provider API keys live in dev and the nightly job only; PR CI holds none.
- Fixtures live under `tests/` beside the suites that consume them, mirroring the structure
  discipline (positive AND negative).
