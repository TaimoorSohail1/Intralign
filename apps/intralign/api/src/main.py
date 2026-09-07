"""Vercel FastAPI entrypoint.

Vercel discovers FastAPI applications exported as ``app`` from ``src/main.py``.
The application itself remains in the ``oslo_api`` package so local and other
deployment entrypoints continue to use the same instance.
"""

from oslo_api.main import app

__all__ = ["app"]
