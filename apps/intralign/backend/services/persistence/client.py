"""Supabase client provider — the single place app code obtains the Postgres transport.

Constraints (DL-054; code/CLAUDE.md):
- Supabase Postgres is the canonical system of record; repositories in
  responsibility modules go THROUGH this provider, never construct ad-hoc clients.
- Configuration comes from the environment only (``SUPABASE_URL`` +
  ``SUPABASE_SERVICE_ROLE_KEY``); a missing value fails loudly — no silent
  fallback endpoint, no embedded credentials.
- ``supabase`` is imported lazily so importing app modules (e.g. for
  introspection tests or OpenAPI generation) never requires the backing-store
  driver or a configured environment.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # import-time dependency only for type checkers
    from supabase import Client

_ENV_URL = "SUPABASE_URL"
_ENV_KEY = "SUPABASE_SERVICE_ROLE_KEY"


def get_supabase_client() -> Client:
    """Create a Supabase client from the environment, or fail with a clear error.

    Raises:
        RuntimeError: if ``SUPABASE_URL`` or ``SUPABASE_SERVICE_ROLE_KEY`` is
            unset/empty (locally: run ``supabase start`` and export both from
            ``supabase status``).
    """
    url = os.environ.get(_ENV_URL)
    key = os.environ.get(_ENV_KEY)
    if not url or not key:
        missing = [name for name, val in ((_ENV_URL, url), (_ENV_KEY, key)) if not val]
        raise RuntimeError(
            f"Supabase client not configured — missing environment variable(s): "
            f"{', '.join(missing)}. Locally: `cd code && supabase start`, then "
            f"export both values from `supabase status`."
        )

    from supabase import create_client  # lazy: keep module import dependency-free

    return create_client(url, key)
