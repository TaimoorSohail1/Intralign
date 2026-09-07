"""Vercel FastAPI entrypoint for the IC-WA-001 deployment contract.

Vercel discovers FastAPI applications exported as ``app`` from ``src/main.py``.
The application itself remains in the ``oslo_api`` package so local and other
deployment entrypoints continue to use the same instance.
"""

import sys
from pathlib import Path

# Vercel loads this file directly and does not add the ``src`` layout to
# ``sys.path``. Make the package import explicit without changing local runs.
_SRC_DIR = Path(__file__).resolve().parent
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from oslo_api.main import app  # noqa: E402

__all__ = ["app"]
