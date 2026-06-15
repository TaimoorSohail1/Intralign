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

import re
from collections.abc import Mapping
from typing import Any, Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

EXTRACTION_VERSION = "wa001-e1"

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
