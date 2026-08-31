"""History read router (DTM-0038) — GET the Cognition-History trail (read-mostly).

Presents the "what OSLO said when" trail: the append-only Cognition-History log
(``cognition_history_record``, LDM §2.2) for a project, in APPEND ORDER (oldest
emitted first), each entry read EXACT from its receipt and Derived-labelled
(``attested-oslo`` — a CHR is OSLO-self-attested). Consumed by the History /
Timeline surface (UI_SCREEN_INVENTORY).

The feed is CHR-ONLY (the user-attested receipts are already exposed by the
existing acceptance / plan-fact reads; the worker report records this choice).
GET ONLY — the append-only write path stays the Retain-owned ``ChrRepository``;
the read surface mutates nothing.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.api.deps import Principal, get_history_reader, require_principal
from backend.services.render import HistoryReader, history_entry_to_dto
from shared.entities import HistoryEntry

router = APIRouter(tags=["history"])


@router.get("/projects/{project_id}/history", response_model=list[HistoryEntry])
def list_history(
    project_id: str,
    principal: Principal = Depends(require_principal),
    reader: HistoryReader = Depends(get_history_reader),
) -> list[HistoryEntry]:
    """The project's Cognition-History trail, oldest-emitted first (Derived-labelled)."""
    rows = reader.list_history(project_id)
    return [history_entry_to_dto(row) for row in rows]
