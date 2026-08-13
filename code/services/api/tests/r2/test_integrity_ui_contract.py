from __future__ import annotations

import os
import subprocess
from pathlib import Path


def test_integrity_surface_uses_maturity_words_without_numeric_forecast() -> None:
    code_root = Path(__file__).resolve().parents[4]
    web_root = code_root / "apps" / "web"
    vitest = web_root / "node_modules" / ".bin" / ("vitest.CMD" if os.name == "nt" else "vitest")
    assert vitest.exists(), "vitest is required for the active GT-20 rendered UI guard"

    completed = subprocess.run(
        [
            str(vitest),
            "run",
            "src/components/overview/project-overview.test.tsx",
            "--testNamePattern",
            "Slice 1 outcome-integrity|five-step integrity",
            "--reporter=dot",
        ],
        cwd=web_root,
        capture_output=True,
        check=False,
        text=True,
        timeout=120,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
