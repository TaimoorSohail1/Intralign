from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def test_integrity_surface_uses_maturity_words_without_numeric_forecast() -> None:
    code_root = Path(__file__).resolve().parents[4]
    pnpm = shutil.which("pnpm")
    assert pnpm is not None, "pnpm is required for the active GT-20 rendered UI guard"

    completed = subprocess.run(
        [
            pnpm,
            "--filter",
            "@oslo/web",
            "exec",
            "vitest",
            "run",
            "src/components/overview/project-overview.test.tsx",
            "--testNamePattern",
            "Slice 1 outcome-integrity|five-step integrity",
            "--reporter=dot",
        ],
        cwd=code_root,
        capture_output=True,
        check=False,
        text=True,
        timeout=120,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
