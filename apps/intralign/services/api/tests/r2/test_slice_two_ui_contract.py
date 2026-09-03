from __future__ import annotations

import os
import subprocess
from pathlib import Path


def test_slice_two_renders_itemized_cross_surface_owner_work_without_blank_state() -> None:
    """Exercise the rendered Slice 2 contract, not source-string markers."""

    code_root = Path(__file__).resolve().parents[4]
    web_root = code_root / "apps" / "web"
    vitest = web_root / "node_modules" / ".bin" / ("vitest.CMD" if os.name == "nt" else "vitest")
    assert vitest.exists(), "vitest is required for the active Slice 2 rendered UI guards"

    completed = subprocess.run(
        [
            str(vitest),
            "run",
            "src/components/overview/project-overview.test.tsx",
            "src/components/artifacts/artifact-workspace.test.tsx",
            "--testNamePattern",
            (
                "renders the Slice 2|keeps a persistent Start|creates a secure review|"
                "records Slice 2|keeps proposals itemized"
            ),
            "--reporter=dot",
        ],
        cwd=web_root,
        capture_output=True,
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )

    assert completed.returncode == 0, (completed.stdout or "") + (completed.stderr or "")
