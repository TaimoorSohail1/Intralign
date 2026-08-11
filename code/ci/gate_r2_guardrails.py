"""Phase 0 gate for the R2 doctrine-guardrail contract.

The authoritative definitions stay in Slice 9. This module checks that every
registered guard still exists there, every Phase 0 guard is present, and every
dynamic surface has a complete FE-to-BE binding. Pending guards are visible but
non-gating; active guards must name real pytest node selectors.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


GUARD_ID_RE = re.compile(r"GT-(?:\d{2}|A\d)\Z")
GUARD_ROW_RE = re.compile(r"^\|\s*(GT-(?:\d{2}|A\d))\s*\|")
SEPARATOR_RE = re.compile(r"^:?-{3,}:?$")
_ESCAPED_PIPE = "\0PIPE\0"


@dataclass(frozen=True)
class GuardDefinition:
    guard_id: str
    doctrine: str
    assertion: str
    source: str
    test_type: str


@dataclass(frozen=True)
class GateReport:
    errors: tuple[str, ...]
    contract_path: Path
    phase0_guard_count: int
    registered_guard_count: int
    active_guard_count: int
    pending_guard_count: int
    surface_count: int
    prototype_correction_count: int
    active_test_selectors: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return not self.errors


def _split_markdown_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    protected = stripped[1:-1].replace(r"\|", _ESCAPED_PIPE)
    return [cell.strip().replace(_ESCAPED_PIPE, "|") for cell in protected.split("|")]


def _is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(SEPARATOR_RE.fullmatch(cell) for cell in cells)


def _section(markdown: str, heading: str, next_heading: str) -> str:
    try:
        return markdown.split(heading, 1)[1].split(next_heading, 1)[0]
    except IndexError:
        return ""


def _parse_guard_definitions(markdown: str) -> tuple[dict[str, GuardDefinition], list[str]]:
    definitions: dict[str, GuardDefinition] = {}
    errors: list[str] = []
    for line_number, line in enumerate(markdown.splitlines(), 1):
        match = GUARD_ROW_RE.match(line)
        if not match:
            continue
        cells = _split_markdown_row(line)
        guard_id = match.group(1)
        if len(cells) != 5:
            errors.append(
                f"{guard_id} has {len(cells)} columns at Slice 9 line {line_number}; expected 5"
            )
            continue
        if guard_id in definitions:
            errors.append(f"{guard_id} is defined more than once in Slice 9")
            continue
        if any(not cell for cell in cells):
            errors.append(f"{guard_id} has an empty contract field in Slice 9")
            continue
        definitions[guard_id] = GuardDefinition(*cells)
    return definitions, errors


def _validate_integration_map(markdown: str) -> tuple[int, list[str]]:
    section = _section(
        markdown,
        "## 2. The consolidated FE",
        "## 3. Doctrine-guardrail test register",
    )
    if not section:
        return 0, ["Slice 9 is missing the FE-to-BE Integration Map section"]

    rows = [_split_markdown_row(line) for line in section.splitlines() if line.startswith("|")]
    rows = [row for row in rows if row and not _is_separator_row(row)]
    expected_header = [
        "Surface",
        "Slice",
        "Reads",
        "Written-by (act)",
        "Changed-by (event)",
        "Async",
    ]
    if not rows or rows[0] != expected_header:
        return 0, ["Slice 9 Integration Map header does not match the six-column contract"]

    errors: list[str] = []
    surfaces: set[str] = set()
    for row_number, row in enumerate(rows[1:], 1):
        if len(row) != 6:
            errors.append(f"Integration Map row {row_number} has {len(row)} columns; expected 6")
            continue
        surface, slice_id, reads, written_by, changed_by, async_state = row
        missing = [
            name
            for name, value in (
                ("Surface", surface),
                ("Slice", slice_id),
                ("Reads", reads),
                ("Written-by", written_by),
                ("Changed-by", changed_by),
                ("Async", async_state),
            )
            if not value
        ]
        if missing:
            errors.append(
                f"Integration Map row {row_number} has empty fields: {', '.join(missing)}"
            )
        if surface in surfaces:
            errors.append(f"Integration Map surface is duplicated: {surface}")
        surfaces.add(surface)
    return len(rows) - 1, errors


def _load_registry(registry_path: Path) -> dict[str, Any]:
    return json.loads(registry_path.read_text(encoding="utf-8"))


def _validate_prototype(prototype: str) -> tuple[int, list[str]]:
    via_level = prototype.split("function viaLevel()", 1)[-1].split(
        "function grdLevel()", 1
    )[0]
    corrections = {
        "five-step Fragile-to-Sound bands": (
            "var BANDS=['Fragile','Weak','Developing','Solid','Sound'];" in prototype
        ),
        "foundation-first Viability-to-Grounding-to-Adaptability tie-break": (
            "o={via:0,grd:1,ada:2}" in prototype
        ),
        "Viability has no fixed-count bump": (
            "function viaLevel()" in prototype
            and "bandOf(" in via_level
            and "_fixedCount" not in via_level
        ),
        "all pillars use size-normalized fractions": all(
            marker in prototype
            for marker in (
                "bandOf(clear/Math.max(1,UND.length))",
                "bandOf(grounded()/Math.max(1,ITEMS.length))",
                "bandOf(_CHKPTS/Math.max(1,CHK_PROPOSALS.length))",
            )
        ),
        "false-confidence issues come from the unified issue layer": (
            "function _falseConfidenceIssues()" in prototype and "ISS-FC-" in prototype
        ),
        "activation starts at the second grounding act": (
            "function _isActivated(){ return confirmCount>=2; }" in prototype
        ),
    }
    errors = [
        f"R2 prototype correction is not applied: {description}"
        for description, applied in corrections.items()
        if not applied
    ]
    return sum(corrections.values()), errors


def evaluate_repository(repository_root: Path) -> GateReport:
    registry_path = repository_root / "code" / "ci" / "r2_guardrails.json"
    registry = _load_registry(registry_path)
    contract_path = repository_root / registry["contract_path"]
    markdown = contract_path.read_text(encoding="utf-8")
    definitions, errors = _parse_guard_definitions(markdown)
    surface_count, surface_errors = _validate_integration_map(markdown)
    errors.extend(surface_errors)
    prototype_path = repository_root / "release-2" / "oslo-prototype-r2.html"
    prototype_correction_count, prototype_errors = _validate_prototype(
        prototype_path.read_text(encoding="utf-8")
    )
    errors.extend(prototype_errors)

    phase0_ids = tuple(registry.get("phase0_required_guard_ids", ()))
    expected_phase0_ids = tuple(f"GT-{number:02d}" for number in range(1, 51))
    if phase0_ids != expected_phase0_ids:
        errors.append("Phase 0 required guard list must be the ordered GT-01 through GT-50 range")

    registered = registry.get("guards", {})
    if not isinstance(registered, dict):
        errors.append("R2 guard registry 'guards' must be an object")
        registered = {}

    contract_ids = set(definitions)
    registered_ids = set(registered)
    for guard_id in sorted(contract_ids - registered_ids):
        errors.append(f"Slice 9 guard is not registered: {guard_id}")
    for guard_id in sorted(registered_ids - contract_ids):
        errors.append(f"Registry guard is not defined by Slice 9: {guard_id}")
    for guard_id in phase0_ids:
        if guard_id not in definitions:
            errors.append(f"Required Phase 0 guard is missing from Slice 9: {guard_id}")

    active_selectors: list[str] = []
    active_count = 0
    pending_count = 0
    for guard_id, registration in registered.items():
        if not GUARD_ID_RE.fullmatch(guard_id):
            errors.append(f"Invalid guard identifier in registry: {guard_id}")
            continue
        if not isinstance(registration, dict):
            errors.append(f"{guard_id} registration must be an object")
            continue
        status = registration.get("status")
        selectors = registration.get("tests")
        if status == "pending":
            pending_count += 1
            if selectors != []:
                errors.append(f"Pending guard {guard_id} must have an empty tests list")
        elif status == "active":
            active_count += 1
            if not isinstance(selectors, list) or not selectors:
                errors.append(f"Active guard {guard_id} must name at least one pytest selector")
                continue
            for selector in selectors:
                if not isinstance(selector, str) or not selector.strip():
                    errors.append(f"Active guard {guard_id} has an invalid pytest selector")
                    continue
                test_path = selector.split("::", 1)[0]
                if not (repository_root / "code" / test_path).is_file():
                    errors.append(f"Active guard {guard_id} test file does not exist: {test_path}")
                active_selectors.append(selector)
        else:
            errors.append(f"{guard_id} has unsupported status {status!r}")

    return GateReport(
        errors=tuple(errors),
        contract_path=contract_path,
        phase0_guard_count=len(phase0_ids),
        registered_guard_count=len(registered),
        active_guard_count=active_count,
        pending_guard_count=pending_count,
        surface_count=surface_count,
        prototype_correction_count=prototype_correction_count,
        active_test_selectors=tuple(dict.fromkeys(active_selectors)),
    )


def run_active_tests(report: GateReport, repository_root: Path) -> int:
    if not report.active_test_selectors:
        return 0
    command = [sys.executable, "-m", "pytest", *report.active_test_selectors]
    return subprocess.run(command, cwd=repository_root / "code", check=False).returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the R2 doctrine-guardrail contract")
    parser.add_argument("--run-active", action="store_true", help="run active guard tests")
    args = parser.parse_args(argv)

    repository_root = Path(__file__).resolve().parents[2]
    report = evaluate_repository(repository_root)
    print(
        "[R2 guardrails] "
        f"{report.registered_guard_count} registered · "
        f"{report.active_guard_count} active · "
        f"{report.pending_guard_count} pending · "
        f"{report.surface_count} mapped surfaces · "
        f"{report.prototype_correction_count}/6 prototype corrections"
    )
    if report.errors:
        for error in report.errors:
            print(f"ERROR: {error}")
        return 1
    if args.run_active:
        return run_active_tests(report, repository_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
