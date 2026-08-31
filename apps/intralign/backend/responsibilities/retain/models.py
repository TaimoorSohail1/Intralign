"""CognitionHistoryRecord — the OSLO-self-attested emission receipt (LDM §2.2).

Field source is RELEASE_1_LOGICAL_DATA_MODEL_V1.md §2.2 verbatim, plus the LDM
§1 universal fields the live ``cognition_history_record`` table carries
(migration 20260612090000). Constraints, not mechanics:

- The value lists for ``output_kind`` (14) and ``recompute_trigger`` (5) mirror
  the table CHECK constraints exactly — Pydantic rejects before the DB would.
- ``epistemic_state`` is PINNED to ``attested-oslo``: a CHR is OSLO-self-attested
  by definition (LDM §2.2); any other state is a validation error.
- ``emitted_at`` / ``created_at`` are server-assigned (Postgres ``now()``) when
  left ``None`` on append; a persisted record always carries both.
- Supersession is a NEW record carrying ``supersedes_chr_id`` — never a mutation
  of the prior record (IC-WA-00R A4.2; hard rule #3).
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal

from pydantic import Field

from shared.epistemic import CognitionEntity, EpistemicState

# LDM §2.2 exact value lists (mirrored by the table CHECK constraints).
OutputKind = Literal[
    "finding",
    "issue",
    "confidence",
    "reliability",
    "caf",
    "outcome_confidence",
    "recommendation",
    "clarification",
    "acceptance_impact",
    "alignment",
    "feasibility",
    "risk",
    # DTM-0009 / Wave S (DL-047) — owner-approved 2026-06-17 (the two Derived
    # kinds persisted via the generic CHR; migration 20260617120000 widens the
    # matching table CHECK by exactly these two values).
    "synthesized_planning_model",
    "planning_artifact",
]

RecomputeTrigger = Literal[
    "promotion",
    "knowledge-change",
    "clarification",
    "user-action",
    "reanalysis",
]


class CognitionHistoryRecord(CognitionEntity):
    """Append-only emission receipt: what was emitted, from what, by which model/rule.

    Carries everything a recompute-lineage walk or a "why did it change" audit
    needs (LDM §2.2); it is a receipt, not live cognition — the recomputable
    current-view lives in the derived layer (LDM §3.1).
    """

    chr_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    output_kind: OutputKind
    output_payload: dict = Field(
        ..., description="The emitted value/content snapshot (LDM §2.2)."
    )
    emitted_at: datetime | None = Field(
        default=None, description="Server-assigned (now()) when None on append."
    )
    input_attestation_version: str = Field(
        ..., description="Which Attested set the emission was computed over."
    )
    model_or_rule_version: dict = Field(
        ...,
        description=(
            "Provider + model identity (e.g. {'provider', 'model'}); an optional "
            "LangSmith run-id key is allowed."
        ),
    )
    upstream_lineage: dict = Field(
        ..., description="Refs to the CHRs/assertions the emission derived from."
    )
    recompute_trigger: RecomputeTrigger
    supersedes_chr_id: uuid.UUID | None = Field(
        default=None,
        description="Set on the NEW record a recompute appends — never a mutation.",
    )
    # LDM §1 universal fields not already named by §2.2 (table-mirrored).
    project_id: uuid.UUID
    created_at: datetime | None = Field(
        default=None, description="Server-assigned (now()) when None on append."
    )
    created_by: str = "OSLO"
    epistemic_state: Literal[EpistemicState.ATTESTED_OSLO] = Field(
        default=EpistemicState.ATTESTED_OSLO,
        description="Pinned: a CHR is OSLO-self-attested (LDM §2.2).",
    )
    provenance_ref: dict
    version: int = 1
