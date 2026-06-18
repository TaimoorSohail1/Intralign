"""Claim extraction (DTM-0007; DL-047 EI-02) — source-attributed, deterministic.

Perceive's "no cognition" means no DERIVED cognition: it never assesses. It
DOES perform source-attributed extraction — interpreting admitted evidence
into evidence-attested assertion DRAFTS (fact | assumption | constraint |
dependency), each attributed to its evidence source and re-derivable, for
Retain to admit (DTM-0008). The drafts here are plain handoff objects; no
canonical row is written by this module.

DL-047 forbidden surface — structurally impossible here: no draft carries any
severity/score field (``extra='forbid'`` rejects unknown fields), the
``epistemic_state`` is Literal-pinned to ``attested-evidence`` (a draft can
NEVER claim ``derived`` content as Attested — B3.7), and the module exports
no assessment producers (B3.2 introspects this).

Extraction rules (version ``wa001-e1``) — deterministic, tier EXACT (same
normalized_form -> byte-identical draft list, in order):

- A line is a CLAIM LINE iff it is a bullet/numbered item (``- ``, ``* ``,
  ``+ ``, ``1. ``, ``1) ``) or a sentence-like line (ends with ``.`` or
  ``!``). Headings and blank lines are never claim lines.
- The proposition is the claim line with any bullet/number marker stripped.
- Classification — first match wins, case-insensitive, over the proposition:
    E1 ``\\b(must|shall)\\b``                       -> ``constraint``
    E2 ``depend(s|ed|ing)? on`` or ``dependenc``    -> ``dependency``
    E3 ``assum(e|es|ed|ing|ption)``                 -> ``assumption``
    E4 otherwise                                    -> ``fact``
- ``source_ref`` carries the artifact id + locus ``{section, line}`` (section
  index in ``normalized_form['sections']``; line index within that section).
- ``attesting_source`` is the EVIDENCE source id of the artifact (never
  'oslo' — nothing here is self-attested).
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:  # pragma: no cover - typing only
    from pydantic_ai.models import Model

EXTRACTION_VERSION = "wa001-e1"

# DL-047 EI-02 LLM extractor version (the model/prompt component of the
# determinism baseline; distinct from the rule-based wa001-e1). Extraction
# routes to nano (Calibration §4c) — this stamps the model/prompt identity.
LLM_EXTRACTION_VERSION = "ws-extract-llm-v0"

# Rule patterns (order = precedence; documented in the module docstring).
_CONSTRAINT_PATTERN = re.compile(r"\b(?:must|shall)\b", re.IGNORECASE)
_DEPENDENCY_PATTERN = re.compile(
    r"\bdepend(?:s|ed|ing)?\s+on\b|\bdependenc", re.IGNORECASE
)
_ASSUMPTION_PATTERN = re.compile(
    r"\bassum(?:e|es|ed|ing|ption|ptions)\b", re.IGNORECASE
)
_BULLET_MARKER = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")

DraftContentType = Literal["fact", "assumption", "constraint", "dependency"]


class AssertionDraft(BaseModel):
    """An evidence-attested AttestedAssertion DRAFT (LDM §2.1 field shape).

    A handoff object for Retain admission — NOT a canonical write. The shape
    admits no severity/score/assessment field (``extra='forbid'``) and its
    epistemic state is pinned: extracted content is evidence-attested, never
    Derived-as-Attested (A4.7 / B3.7).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    content_type: DraftContentType
    proposition: str
    attesting_source: str = Field(..., description="the evidence-source id")
    source_ref: dict = Field(..., description="{'artifact_id': ..., 'locus': ...}")
    re_derivable: Literal[True] = True
    epistemic_state: Literal["attested-evidence"] = "attested-evidence"


@runtime_checkable
class ClaimExtractor(Protocol):
    """The extraction seam (decision #5): rule-based now, LLM-backed later
    behind the SAME interface (Wave B/S wires Pydantic AI here)."""

    def extract(
        self,
        *,
        artifact_id: str,
        normalized_form: Mapping[str, Any],
        attesting_source: str,
    ) -> list[AssertionDraft]:
        ...  # pragma: no cover - protocol


def _classify(proposition: str) -> DraftContentType:
    """wa001-e1 classification — first match wins (E1 -> E2 -> E3 -> E4)."""
    if _CONSTRAINT_PATTERN.search(proposition):
        return "constraint"
    if _DEPENDENCY_PATTERN.search(proposition):
        return "dependency"
    if _ASSUMPTION_PATTERN.search(proposition):
        return "assumption"
    return "fact"


def _is_claim_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return False
    if _BULLET_MARKER.match(line):
        return True
    return stripped.endswith((".", "!"))


class RuleBasedExtractor:
    """Deterministic wa001-e1 extractor over an artifact's normalized_form."""

    version = EXTRACTION_VERSION

    def extract(
        self,
        *,
        artifact_id: str,
        normalized_form: Mapping[str, Any],
        attesting_source: str,
    ) -> list[AssertionDraft]:
        """Produce typed, source-attributed drafts — exact-tier deterministic."""
        drafts: list[AssertionDraft] = []
        for section in normalized_form.get("sections", []):
            for line_index, line in enumerate(section.get("lines", [])):
                if not _is_claim_line(line):
                    continue
                proposition = _BULLET_MARKER.sub("", line).strip()
                drafts.append(
                    AssertionDraft(
                        content_type=_classify(proposition),
                        proposition=proposition,
                        attesting_source=attesting_source,
                        source_ref={
                            "artifact_id": artifact_id,
                            "locus": {
                                "section": section["index"],
                                "line": line_index,
                            },
                        },
                    )
                )
        return drafts


# =============================================================================
# DL-047 EI-02 — LLM-backed extractor. A SECOND ClaimExtractor implementation
# behind the SAME Protocol (decision #5): the rule-based extractor above is
# byte-intact; config selects which impl is used. The LLM extractor still
# produces evidence-attested, source-attributed, re-derivable AssertionDrafts —
# NO Derived cognition (no severity/score/confidence; the AssertionDraft shape
# forbids it structurally). Perceive's "no cognition" boundary is preserved.
# =============================================================================

# Claims the LLM may return — same content-type vocabulary as the rule extractor.
_LLM_CLAIM_TYPES: frozenset[str] = frozenset(
    ("fact", "assumption", "constraint", "dependency")
)

_LLM_EXTRACTION_INSTRUCTIONS = (
    "You extract source-attributed claims from project evidence. Return ONLY a "
    "JSON array; each item is {\"content_type\": one of "
    "fact|assumption|constraint|dependency, \"proposition\": the claim text}. "
    "Do not assess, score, rank, or add severity/confidence — extraction is not "
    "cognition. Use the exact wording from the evidence where possible so each "
    "claim is re-derivable to its source."
)


def _normalized_line_index(
    normalized_form: Mapping[str, Any], proposition: str
) -> dict[str, Any]:
    """Locate ``proposition`` in the normalized form for a re-derivable locus.

    Returns the {section,line} locus of the first normalized line whose stripped
    text matches the proposition; otherwise an ``llm-derived`` marker (still
    attributed to the artifact + evidence source — the claim is never
    un-attributed, only its precise line could not be pinned).
    """
    target = proposition.strip().casefold()
    for section in normalized_form.get("sections", []):
        for line_index, line in enumerate(section.get("lines", [])):
            stripped = _BULLET_MARKER.sub("", line).strip().casefold()
            if stripped == target:
                return {"section": section["index"], "line": line_index}
    return {"section": None, "line": None, "match": "llm-derived"}


class LLMClaimExtractor:
    """LLM-backed extractor behind the ClaimExtractor Protocol (DL-047 EI-02).

    Drives a pydantic-ai ``Agent`` over an injected ``Model`` (a recorded
    model-response fixture in CI; a live, tier-routed model only behind the env
    flag). The model returns candidate claims; THIS extractor types them,
    attributes each to the artifact + evidence source, and pins a re-derivable
    locus — producing the SAME evidence-attested AssertionDraft shape as the
    rule-based extractor. It performs NO assessment (the draft shape forbids it).
    """

    version = LLM_EXTRACTION_VERSION

    def __init__(self, model: Model, *, prompt_suffix: str = "") -> None:
        # The pydantic-ai Model serving extraction (recorded fixture in CI).
        self._model = model
        # Optional prompt suffix (the harness uses it to embed a recorded-
        # response selection directive; empty in live runs). Backend never
        # imports the tests/ harness — the directive STRING is supplied in.
        self._prompt_suffix = prompt_suffix

    def _agent(self):  # type: ignore[no-untyped-def]
        # Imported lazily: pure-config modules never import pydantic-ai.
        from pydantic_ai import Agent

        return Agent(
            self._model,
            output_type=str,
            instructions=_LLM_EXTRACTION_INSTRUCTIONS,
        )

    def extract(
        self,
        *,
        artifact_id: str,
        normalized_form: Mapping[str, Any],
        attesting_source: str,
    ) -> list[AssertionDraft]:
        """Extract typed, source-attributed drafts via the model — no cognition."""
        text = normalized_form.get("text", "")
        prompt = f"Evidence:\n{text}"
        if self._prompt_suffix:
            prompt = f"{prompt}\n{self._prompt_suffix}"
        result = self._agent().run_sync(prompt)
        claims = _parse_claims(result.output)
        drafts: list[AssertionDraft] = []
        for claim in claims:
            content_type = claim.get("content_type")
            proposition = (claim.get("proposition") or "").strip()
            if content_type not in _LLM_CLAIM_TYPES or not proposition:
                continue  # never admit an un-typed / empty claim
            drafts.append(
                AssertionDraft(
                    content_type=content_type,
                    proposition=proposition,
                    attesting_source=attesting_source,
                    source_ref={
                        "artifact_id": artifact_id,
                        "locus": _normalized_line_index(normalized_form, proposition),
                        "extractor": LLM_EXTRACTION_VERSION,
                    },
                )
            )
        return drafts


def _parse_claims(raw: str) -> list[dict[str, Any]]:
    """Parse the model's JSON claim array; tolerant of code-fenced output."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lstrip().startswith("json"):
            cleaned = cleaned.lstrip()[4:]
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        return []
    if isinstance(parsed, dict) and "claims" in parsed:
        parsed = parsed["claims"]
    return [c for c in parsed if isinstance(c, dict)] if isinstance(parsed, list) else []
