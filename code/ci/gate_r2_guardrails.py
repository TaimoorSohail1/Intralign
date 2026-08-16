"""Phase 0 gate for the R2 doctrine-guardrail contract.

The authoritative definitions stay in Slice 9. This module checks that every
registered guard still exists there, every Phase 0 guard is present, and every
dynamic surface has a complete FE-to-BE binding. Pending guards are visible but
non-gating; active guards must name real pytest and/or Vitest tests.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
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
    machine_surface_count: int
    route_count: int
    prototype_correction_count: int
    active_test_selectors: tuple[str, ...]
    active_client_test_files: tuple[str, ...]

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


def _parse_integration_map(markdown: str) -> tuple[list[tuple[str, ...]], list[str]]:
    section = _section(
        markdown,
        "## 2. The consolidated FE",
        "## 3. Doctrine-guardrail test register",
    )
    if not section:
        return [], ["Slice 9 is missing the FE-to-BE Integration Map section"]

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
        return [], ["Slice 9 Integration Map header does not match the six-column contract"]

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
    complete_rows = [tuple(row) for row in rows[1:] if len(row) == 6]
    return complete_rows, errors


def _load_registry(registry_path: Path) -> dict[str, Any]:
    return json.loads(registry_path.read_text(encoding="utf-8"))


def _validate_surface_registry(
    repository_root: Path,
    contract_rows: list[tuple[str, ...]],
    registered_guards: set[str],
) -> tuple[int, int, list[str]]:
    registry_path = repository_root / "code" / "ci" / "r2_surface_contracts.json"
    if not registry_path.is_file():
        return 0, 0, ["R2 machine surface registry is missing"]

    errors: list[str] = []
    try:
        registry = _load_registry(registry_path)
    except (OSError, json.JSONDecodeError) as error:
        return 0, 0, [f"R2 machine surface registry is invalid: {error}"]

    if registry.get("schema_version") != 1:
        errors.append("R2 machine surface registry must use schema_version 1")

    profiles = registry.get("profiles")
    if not isinstance(profiles, dict) or not profiles:
        profiles = {}
        errors.append("R2 machine surface registry must define implementation profiles")

    code_root = repository_root / "code"
    for profile_id, profile in profiles.items():
        if not isinstance(profile, dict):
            errors.append(f"Surface profile {profile_id} must be an object")
            continue
        status = profile.get("status")
        if status not in {"shipped", "contract-only"}:
            errors.append(f"Surface profile {profile_id} has unsupported status {status!r}")
        if status == "contract-only" and not str(profile.get("pending_reason", "")).strip():
            errors.append(f"Contract-only surface profile {profile_id} needs a pending reason")
        for field in ("frontend", "backend", "tests"):
            references = profile.get(field)
            if not isinstance(references, list):
                errors.append(f"Surface profile {profile_id} {field} must be a list")
                continue
            if status == "shipped" and not references:
                errors.append(f"Shipped surface profile {profile_id} needs {field} bindings")
            for reference in references:
                if not isinstance(reference, str) or not reference.strip():
                    errors.append(f"Surface profile {profile_id} has an invalid {field} binding")
                    continue
                path = reference.split("::", 1)[0]
                if not (code_root / path).is_file():
                    errors.append(
                        f"Surface profile {profile_id} {field} binding does not exist: {path}"
                    )

    surfaces = registry.get("surfaces")
    if not isinstance(surfaces, list):
        surfaces = []
        errors.append("R2 machine surface registry 'surfaces' must be a list")

    ids: set[str] = set()
    labels: set[str] = set()
    for surface in surfaces:
        if not isinstance(surface, dict):
            errors.append("Every R2 machine surface must be an object")
            continue
        surface_id = surface.get("id")
        label = surface.get("contract_surface")
        profile_id = surface.get("profile")
        guard_ids = surface.get("guard_ids")
        if not isinstance(surface_id, str) or not re.fullmatch(r"r2-s[1-8]-[a-z0-9-]+", surface_id):
            errors.append(f"Machine surface has an invalid stable id: {surface_id!r}")
        elif surface_id in ids:
            errors.append(f"Machine surface id is duplicated: {surface_id}")
        else:
            ids.add(surface_id)
        if not isinstance(label, str) or not label.strip():
            errors.append(f"Machine surface {surface_id!r} has no contract_surface")
        elif label in labels:
            errors.append(f"Machine surface contract label is duplicated: {label}")
        else:
            labels.add(label)
        if profile_id not in profiles:
            errors.append(f"Machine surface {surface_id!r} uses unknown profile {profile_id!r}")
        if not isinstance(guard_ids, list) or not guard_ids:
            errors.append(f"Machine surface {surface_id!r} must bind at least one guard")
        else:
            for guard_id in guard_ids:
                if guard_id not in registered_guards:
                    errors.append(f"Machine surface {surface_id!r} uses unknown guard {guard_id!r}")

    contract_labels = {row[0] for row in contract_rows}
    for label in sorted(contract_labels - labels):
        errors.append(f"Integration Map surface lacks a machine binding: {label}")
    for label in sorted(labels - contract_labels):
        errors.append(f"Machine surface is absent from the Integration Map: {label}")

    routes = registry.get("routes")
    if not isinstance(routes, list):
        routes = []
        errors.append("R2 machine surface registry 'routes' must be a list")
    route_names: set[str] = set()
    route_frontends: set[str] = set()
    for route in routes:
        if not isinstance(route, dict):
            errors.append("Every R2 route binding must be an object")
            continue
        route_name = route.get("route")
        frontend = route.get("frontend")
        backend = route.get("backend")
        track = route.get("track")
        if not isinstance(route_name, str) or not route_name.startswith("/"):
            errors.append(f"R2 route has an invalid route name: {route_name!r}")
        elif route_name in route_names:
            errors.append(f"R2 route is duplicated: {route_name}")
        else:
            route_names.add(route_name)
        if not isinstance(frontend, str) or not (code_root / frontend).is_file():
            errors.append(f"R2 route {route_name!r} has a missing frontend binding: {frontend!r}")
        else:
            route_frontends.add(frontend.replace("\\", "/"))
        if not isinstance(backend, list) or not backend:
            errors.append(f"R2 route {route_name!r} must name a backend boundary")
        else:
            for reference in backend:
                if not isinstance(reference, str) or not (code_root / reference).is_file():
                    errors.append(f"R2 route {route_name!r} backend binding is missing: {reference!r}")
        if track not in {"canonical-r2", "workspace-settings-implementation", "legacy-compatibility"}:
            errors.append(f"R2 route {route_name!r} has an unsupported implementation track")

    discovery_roots = [
        code_root / "apps" / "web" / "src" / "app" / "intake",
        code_root / "apps" / "web" / "src" / "app" / "projects" / "[projectId]",
        code_root / "apps" / "web" / "src" / "app" / "review",
        code_root / "apps" / "web" / "src" / "app" / "share",
        code_root / "apps" / "web" / "src" / "app" / "settings",
        code_root / "apps" / "web" / "src" / "app" / "workspace",
    ]
    discovered_frontends = {
        path.relative_to(code_root).as_posix()
        for root in discovery_roots
        if root.is_dir()
        for path in root.rglob("page.tsx")
    }
    for frontend in sorted(discovered_frontends - route_frontends):
        errors.append(f"Shipped R2 route lacks a machine binding: {frontend}")
    for frontend in sorted(route_frontends - discovered_frontends):
        errors.append(f"Registered R2 route is outside the shipped route inventory: {frontend}")

    return len(surfaces), len(routes), errors


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
    max_cap_match = re.search(r"var\s+SIM_MAX_CAP\s*=\s*(\d+)", prototype)
    elsewhere_match = re.search(r"var\s+_SIM_ELSEWHERE\s*=\s*\[([^]]*)\]", prototype)
    if max_cap_match is None or elsewhere_match is None:
        errors.append("R2 prototype is missing the reverse SIM coverage register")
    else:
        max_capability = int(max_cap_match.group(1))
        elsewhere = {
            int(value)
            for value in re.findall(r"\d+", elsewhere_match.group(1))
        }
        simulated = {int(value) for value in re.findall(r"SIM:#(\d+)", prototype)}
        for capability in range(1, max_capability + 1):
            if capability not in simulated and capability not in elsewhere:
                errors.append(
                    "R2 prototype capability has no SIM tag or arc exception: "
                    f"{capability}"
                )
    return sum(corrections.values()), errors


def evaluate_repository(repository_root: Path) -> GateReport:
    registry_path = repository_root / "code" / "ci" / "r2_guardrails.json"
    registry = _load_registry(registry_path)
    contract_path = repository_root / registry["contract_path"]
    markdown = contract_path.read_text(encoding="utf-8")
    definitions, errors = _parse_guard_definitions(markdown)
    contract_rows, surface_errors = _parse_integration_map(markdown)
    surface_count = len(contract_rows)
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

    machine_surface_count, route_count, machine_errors = _validate_surface_registry(
        repository_root,
        contract_rows,
        set(registered),
    )
    errors.extend(machine_errors)

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
    active_client_tests: list[str] = []
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
        client_tests = registration.get("client_tests", [])
        if status == "pending":
            pending_count += 1
            if selectors != []:
                errors.append(f"Pending guard {guard_id} must have an empty tests list")
            if client_tests != []:
                errors.append(f"Pending guard {guard_id} must have an empty client_tests list")
            if not str(registration.get("pending_reason", "")).strip():
                errors.append(f"Pending guard {guard_id} must explain why it is not active")
        elif status == "active":
            active_count += 1
            if not isinstance(selectors, list):
                errors.append(f"Active guard {guard_id} tests must be a list")
                selectors = []
            if not isinstance(client_tests, list):
                errors.append(f"Active guard {guard_id} client_tests must be a list")
                client_tests = []
            if not selectors and not client_tests:
                errors.append(f"Active guard {guard_id} must name at least one executable test")
                continue
            for selector in selectors:
                if not isinstance(selector, str) or not selector.strip():
                    errors.append(f"Active guard {guard_id} has an invalid pytest selector")
                    continue
                test_path = selector.split("::", 1)[0]
                if not (repository_root / "code" / test_path).is_file():
                    errors.append(f"Active guard {guard_id} test file does not exist: {test_path}")
                active_selectors.append(selector)
            for client_test in client_tests:
                if not isinstance(client_test, str) or not client_test.strip():
                    errors.append(f"Active guard {guard_id} has an invalid client test file")
                    continue
                if not (repository_root / "code" / client_test).is_file():
                    errors.append(
                        f"Active guard {guard_id} client test file does not exist: {client_test}"
                    )
                active_client_tests.append(client_test)
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
        machine_surface_count=machine_surface_count,
        route_count=route_count,
        prototype_correction_count=prototype_correction_count,
        active_test_selectors=tuple(dict.fromkeys(active_selectors)),
        active_client_test_files=tuple(dict.fromkeys(active_client_tests)),
    )


def run_active_tests(report: GateReport, repository_root: Path) -> int:
    code_root = repository_root / "code"
    if report.active_test_selectors:
        command = [sys.executable, "-m", "pytest", *report.active_test_selectors]
        return_code = subprocess.run(command, cwd=code_root, check=False).returncode
        if return_code:
            return return_code
    if report.active_client_test_files:
        pnpm = shutil.which("pnpm.cmd") or shutil.which("pnpm") or "pnpm"
        web_root = Path("apps/web")
        client_test_files = [
            Path(client_test).relative_to(web_root).as_posix()
            for client_test in report.active_client_test_files
        ]
        command = [
            pnpm,
            "--filter",
            "@oslo/web",
            "test",
            *client_test_files,
        ]
        return subprocess.run(command, cwd=code_root, check=False).returncode
    return 0


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
