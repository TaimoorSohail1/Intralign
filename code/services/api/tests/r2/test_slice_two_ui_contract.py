from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def test_slice_two_renders_itemized_cross_surface_owner_work_without_blank_state() -> None:
    """Exercise the rendered Slice 2 contract, not source-string markers."""

    code_root = Path(__file__).resolve().parents[4]
    pnpm = shutil.which("pnpm")
    assert pnpm is not None, "pnpm is required for the active Slice 2 rendered UI guards"

    completed = subprocess.run(
        [
            pnpm,
            "--filter",
            "@oslo/web",
            "exec",
            "vitest",
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
        cwd=code_root,
        capture_output=True,
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )

    assert completed.returncode == 0, (completed.stdout or "") + (completed.stderr or "")
