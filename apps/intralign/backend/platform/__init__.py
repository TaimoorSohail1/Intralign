"""Platform — commodity infrastructure: auth/RBAC, projects, settings, notifications-state.

NEVER mixed into responsibility modules. DTM-0031 adds the platform persistence
repos (project / analysis_run / notification) — mutable, workspace-scoped, with
NO surface onto the canonical epistemic store (hard rule #2).
"""

from backend.platform.analysis_run_repo import SupabaseAnalysisRunRepository
from backend.platform.notification_repo import SupabaseNotificationRepository
from backend.platform.project_repo import SupabaseProjectRepository

__all__ = [
    "SupabaseAnalysisRunRepository",
    "SupabaseNotificationRepository",
    "SupabaseProjectRepository",
]
