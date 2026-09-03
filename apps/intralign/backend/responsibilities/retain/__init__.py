"""Retain — canonical memory. Append-only stores; recompute appends, never overwrites (hard rule #3).

DTM-0004: CognitionHistoryRecord + ChrRepository. DTM-0008 (IC-WA-002):
integrity-gated admission, versioning/explicit supersession, archival-as-
history-event, and User Acceptance Record creation — all additive, all
append-only.
"""

from backend.responsibilities.retain.acceptance import (
    AcceptanceRecordingError,
    AcceptanceRecordResult,
    record_acceptance,
)
from backend.responsibilities.retain.admission import (
    AdmissionRejectedError,
    AdmissionResult,
    RetentionStore,
    admit_candidate,
)
from backend.responsibilities.retain.archival import (
    ArchivalResult,
    AssertionNotFoundError,
    NotArchivedError,
    UnarchivalResult,
    archive_assertion,
    is_archived,
    unarchive_assertion,
)
from backend.responsibilities.retain.models import CognitionHistoryRecord
from backend.responsibilities.retain.repository import ChrRepository
from backend.responsibilities.retain.versioning import (
    PriorAssertionNotFoundError,
    VersioningResult,
    version_assertion,
    version_chain,
)

__all__ = [
    "AcceptanceRecordResult",
    "AcceptanceRecordingError",
    "AdmissionRejectedError",
    "AdmissionResult",
    "ArchivalResult",
    "AssertionNotFoundError",
    "ChrRepository",
    "CognitionHistoryRecord",
    "NotArchivedError",
    "PriorAssertionNotFoundError",
    "RetentionStore",
    "UnarchivalResult",
    "VersioningResult",
    "admit_candidate",
    "archive_assertion",
    "is_archived",
    "record_acceptance",
    "unarchive_assertion",
    "version_assertion",
    "version_chain",
]
