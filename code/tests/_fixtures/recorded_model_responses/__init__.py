"""Recorded model-response fixture harness (ADR-0004; decisions #2/#3/#11).

The SHARED test-double that lets CI exercise OSLO's LLM steps offline and
deterministically. Built here first (DTM-0009) and reused by every later AI
slice (DTM-0010/0011). It is NOT a "replay" and NOT a "cassette" — those names
are reserved/non-canon (CONTEXT.md Disambiguation Register; ``replay`` means
event-log reconstruction that does not re-run the LLM). This is a **recorded
model-response fixture**: a captured, version-stamped model output that stands
in for the (model-version × fixture) components of the determinism baseline
triple (DT-5/DT-10).

How it works:

- Fixtures are in-repo JSON files under this directory, each stamped with
  ``model_version`` + ``config`` (the baseline stamp — a model-version change
  is a NEW baseline, not a regression, DT-6) and a list of recorded responses
  keyed by a stable ``key``.
- :func:`build_recorded_model` turns a loaded fixture into a pydantic-ai
  ``FunctionModel`` whose function returns the recorded text + recorded token
  usage for the matched key. Selection is by an explicit per-request ``key``
  embedded in the prompt (deterministic — no model is consulted to choose).
- :class:`RecordedModelSession` counts invocations so a self-test can PROVE PR
  CI makes ZERO live provider calls: every response came from a fixture.

No provider SDK is imported here — the FunctionModel is a pure local callable.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    RequestUsage,
    TextPart,
    UserPromptPart,
)
from pydantic_ai.models.function import AgentInfo, FunctionModel

FIXTURE_DIR = Path(__file__).resolve().parent

# A recorded fixture MUST carry these stamp fields (ADR-0004 auditability).
_REQUIRED_STAMP_FIELDS = ("model_version", "config")

# The marker the engine embeds in a prompt to select a recorded response
# deterministically (no model is consulted to choose — selection is explicit).
RESPONSE_KEY_MARKER = "[[response_key:"


@dataclass(frozen=True)
class RecordedResponse:
    """One recorded model output: the text + the recorded token usage."""

    key: str
    text: str
    tokens_in: int
    tokens_out: int


@dataclass(frozen=True)
class RecordedFixture:
    """A version-stamped set of recorded responses (the baseline stamp)."""

    name: str
    model_version: str
    config: dict[str, Any]
    responses: dict[str, RecordedResponse]

    def response_for(self, key: str) -> RecordedResponse:
        if key not in self.responses:
            raise KeyError(
                f"recorded fixture {self.name!r} has no response for key {key!r} "
                f"— record one (keys: {sorted(self.responses)})"
            )
        return self.responses[key]


class FixtureStampError(ValueError):
    """A fixture missing its model_version/config stamp (ADR-0004 requirement)."""


def load_fixture(name: str) -> RecordedFixture:
    """Load a recorded fixture JSON by file stem, validating its baseline stamp."""
    path = FIXTURE_DIR / f"{name}.json"
    if not path.is_file():
        raise FileNotFoundError(f"no recorded fixture {name!r} at {path}")
    raw = json.loads(path.read_text(encoding="utf-8"))
    missing = [f for f in _REQUIRED_STAMP_FIELDS if not raw.get(f)]
    if missing:
        raise FixtureStampError(
            f"recorded fixture {name!r} is missing required stamp field(s) "
            f"{missing} — every fixture carries model_version + config (ADR-0004)"
        )
    responses = {
        r["key"]: RecordedResponse(
            key=r["key"],
            text=r["text"],
            tokens_in=int(r.get("tokens_in", 0)),
            tokens_out=int(r.get("tokens_out", 0)),
        )
        for r in raw.get("responses", [])
    }
    return RecordedFixture(
        name=name,
        model_version=raw["model_version"],
        config=dict(raw["config"]),
        responses=responses,
    )


def response_key_directive(key: str) -> str:
    """The directive the engine appends to a prompt to select a recorded response."""
    return f"{RESPONSE_KEY_MARKER}{key}]]"


def _extract_response_key(messages: list[ModelMessage]) -> str | None:
    """Find the explicit response key embedded in the latest user prompt."""
    for message in reversed(messages):
        if not isinstance(message, ModelRequest):
            continue
        for part in message.parts:
            if isinstance(part, UserPromptPart) and isinstance(part.content, str):
                marker = part.content.find(RESPONSE_KEY_MARKER)
                if marker != -1:
                    start = marker + len(RESPONSE_KEY_MARKER)
                    end = part.content.find("]]", start)
                    if end != -1:
                        return part.content[start:end]
    return None


@dataclass
class RecordedModelSession:
    """A FunctionModel bound to a fixture, counting invocations (zero-live proof).

    ``call_count`` increments on every recorded response served. A self-test
    asserts the engine ran entirely on recorded responses — i.e. a real
    provider was never reached (ADR-0004: PR CI makes zero provider calls).
    """

    fixture: RecordedFixture
    call_count: int = 0
    served_keys: list[str] = field(default_factory=list)

    def _function(self, messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        key = _extract_response_key(messages)
        if key is None:
            raise ValueError(
                "no response_key directive in the prompt — the engine must "
                "select a recorded response explicitly (deterministic harness)"
            )
        recorded = self.fixture.response_for(key)
        self.call_count += 1
        self.served_keys.append(key)
        return ModelResponse(
            parts=[TextPart(content=recorded.text)],
            usage=RequestUsage(
                input_tokens=recorded.tokens_in,
                output_tokens=recorded.tokens_out,
            ),
            model_name=f"recorded:{self.fixture.model_version}",
        )

    def model(self) -> FunctionModel:
        """The pydantic-ai FunctionModel serving this fixture's recorded responses."""
        return FunctionModel(self._function, model_name=f"recorded:{self.fixture.model_version}")


def build_recorded_model(name: str) -> RecordedModelSession:
    """Load fixture ``name`` and return a session wrapping its FunctionModel."""
    return RecordedModelSession(fixture=load_fixture(name))
