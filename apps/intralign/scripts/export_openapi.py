"""Export the FastAPI OpenAPI schema to a file for offline Orval codegen.

The frontend API client (``frontend/src/api/generated/**``) is generated from the
backend contract, but it is a build artifact — not committed. In CI the live
backend is never started, so Orval cannot read ``http://localhost:8000/openapi.json``.
This dumps the schema straight from the app object (no server) to
``frontend/openapi.json``, which ``orval.config.ts`` then consumes.

Usage (from anywhere, backend installed):  python apps/intralign/scripts/export_openapi.py
"""

from __future__ import annotations

import json
from pathlib import Path

from backend.api.app import app

OUT = Path(__file__).resolve().parents[1] / "frontend" / "openapi.json"


def main() -> None:
    spec = app.openapi()
    OUT.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(Path.cwd())}" if OUT.is_relative_to(Path.cwd()) else f"wrote {OUT}")


if __name__ == "__main__":
    main()
