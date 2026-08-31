"""Analysis-command request bodies (DTM-0032; API Contract §5 "Analysis").

Response DTOs are the canonical ``AnalysisRun`` entity (``shared.entities``,
Data Model v1.2 §10 verbatim) — only the INPUT shapes live here.
"""

from __future__ import annotations

from pydantic import BaseModel


class DeepAnalysisRequest(BaseModel):
    """``POST …/analysis-runs:deep`` body — ``{trigger_source=manual}`` (§5).

    ``trigger_source`` records why the deep pass was requested (default
    ``manual`` — a user-initiated request from the read surface).
    """

    trigger_source: str = "manual"
