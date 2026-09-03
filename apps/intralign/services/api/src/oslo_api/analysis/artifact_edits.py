import hashlib
import json
from collections.abc import Callable, Mapping, Sequence
from copy import deepcopy

from oslo_api.analysis.models import EvidenceFragment

_SHARED_WBS_ROW_PREFIXES = ("work-breakdown-", "work_breakdown-", "legacy-wbs-")


def artifact_content_hash(content: Mapping[str, object]) -> str:
    """Return a stable identity for material artifact content.

    Browser-only editor identities keep React nodes stable while typing. They
    are excluded so adding those identities, or adding and then undoing a row,
    cannot create a new artifact version or analysis run.
    """

    canonical = json.dumps(
        _material_content(content),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _material_content(value: object) -> object:
    if isinstance(value, Mapping):
        return {
            key: _material_content(item)
            for key, item in value.items()
            if key not in {"id", "row_ids"}
        }
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [_material_content(item) for item in value]
    return value


def build_user_edit_evidence(
    *,
    artifact_type: str,
    version: int,
    content: Mapping[str, object],
) -> EvidenceFragment:
    """Represent a saved artifact edit as readable, untrusted project evidence.

    Prompt-control markers and raw JSON are deliberately excluded so internal
    transport syntax cannot leak into Overview, Reports, advisor answers, or
    exports.
    """

    display_type = artifact_type.replace("_", " ").title()
    lines = [f"{display_type} artifact changes confirmed by the user:"]
    sections = content.get("sections")
    if isinstance(sections, Sequence) and not isinstance(sections, (str, bytes)):
        for raw_section in sections:
            if not isinstance(raw_section, Mapping):
                continue
            heading = _text(raw_section.get("heading"))
            body = _text(raw_section.get("body"))
            bullets = _strings(raw_section.get("bullets"))
            columns = _strings(raw_section.get("columns"))
            rows = raw_section.get("rows")
            if heading:
                lines.append(f"Section: {heading}")
            if body:
                lines.append(body)
            lines.extend(f"- {bullet}" for bullet in bullets)
            if isinstance(rows, Sequence) and not isinstance(rows, (str, bytes)):
                for row in rows:
                    cells = _strings(row)
                    if not cells:
                        continue
                    if columns and len(columns) == len(cells):
                        lines.append(
                            "; ".join(
                                f"{column}: {cell}"
                                for column, cell in zip(columns, cells, strict=True)
                            )
                        )
                    lines.append(" | ".join(cells))
    if len(lines) == 1:
        lines.append("The user saved an empty artifact.")
    return EvidenceFragment(
        reference=f"user:artifact:{artifact_type}:version:{version}",
        content="\n".join(lines),
        source_name=f"User-confirmed {display_type} edit",
        location=f"Artifact version {version}",
    )


def project_work_breakdown_tasks(
    *,
    artifact_type: str,
    content: Mapping[str, object],
    work_breakdown_content: Mapping[str, object],
) -> dict:
    """Project confirmed WBS tasks into their Schedule/Resources facets.

    The Work Breakdown owns task identity. Schedule and Resources expose the
    same task IDs with artifact-specific cells, so a task cannot silently
    disappear or multiply as a user moves between the three plan views.
    """

    if artifact_type not in {"schedule", "resources"}:
        return deepcopy(dict(content))

    projected = deepcopy(dict(content))
    raw_sections = projected.get("sections")
    if not isinstance(raw_sections, list):
        return projected

    tasks = _work_breakdown_tasks(work_breakdown_content)
    task_ids = {task_id for task_id, _ in tasks}
    existing_ids: set[str] = set()

    for section_index, section in enumerate(raw_sections):
        if not isinstance(section, dict):
            continue
        rows = section.get("rows")
        if not isinstance(rows, list):
            continue
        row_ids = _aligned_strings(
            section.get("row_ids"),
            len(rows),
            fallback=lambda index, current_section=section_index: (
                f"{artifact_type}-section-{current_section + 1}-row-{index + 1}"
            ),
        )
        keep_indexes = [
            index
            for index, row_id in enumerate(row_ids)
            if not (
                row_id.startswith(_SHARED_WBS_ROW_PREFIXES)
                and row_id not in task_ids
            )
        ]
        section["rows"] = [rows[index] for index in keep_indexes]
        section["row_ids"] = [row_ids[index] for index in keep_indexes]
        for field, default in (
            ("row_evidence_refs", []),
            ("row_states", "confirmed"),
            ("row_provenance", "confirmed_by_user"),
        ):
            values = _aligned_values(section.get(field), len(rows), default)
            section[field] = [values[index] for index in keep_indexes]
        existing_ids.update(section["row_ids"])

    target = next(
        (
            section
            for section in raw_sections
            if isinstance(section, dict)
            and isinstance(section.get("rows"), list)
            and isinstance(section.get("columns"), list)
            and bool(section["columns"])
        ),
        None,
    )
    if target is None:
        target = {
            "heading": "Shared plan tasks",
            "body": "",
            "bullets": [],
            "columns": (
                ["Milestone", "Date", "Status"]
                if artifact_type == "schedule"
                else ["Resource", "Role", "Status"]
            ),
            "rows": [],
            "row_ids": [],
            "row_evidence_refs": [],
            "row_states": [],
            "row_provenance": [],
        }
        raw_sections.append(target)

    columns = target.get("columns")
    column_count = len(columns) if isinstance(columns, list) and columns else 3
    for task_id, task_name in tasks:
        if task_id in existing_ids:
            continue
        target["rows"].append([task_name, *("" for _ in range(column_count - 1))])
        target["row_ids"].append(task_id)
        target["row_evidence_refs"].append([])
        target["row_states"].append("confirmed")
        target["row_provenance"].append("confirmed_by_user")
        existing_ids.add(task_id)
    return projected


def _work_breakdown_tasks(content: Mapping[str, object]) -> list[tuple[str, str]]:
    tasks: list[tuple[str, str]] = []
    sections = content.get("sections")
    if not isinstance(sections, Sequence) or isinstance(sections, (str, bytes)):
        return tasks
    for section_index, section in enumerate(sections):
        if not isinstance(section, Mapping):
            continue
        columns = _strings(section.get("columns"))
        rows = section.get("rows")
        if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)):
            continue
        normalized_columns = [column.casefold() for column in columns]
        code_index = next(
            (index for index, name in enumerate(normalized_columns) if name == "wbs"),
            None,
        )
        name_index = next(
            (
                index
                for index, name in enumerate(normalized_columns)
                if name in {"item", "task", "name", "key deliverable"}
            ),
            0,
        )
        row_ids = _aligned_strings(
            section.get("row_ids"),
            len(rows),
            fallback=lambda index, current_section=section_index: (
                f"work-breakdown-section-{current_section + 1}-row-{index + 1}"
            ),
        )
        for row_id, raw_row in zip(row_ids, rows, strict=True):
            if not isinstance(raw_row, Sequence) or isinstance(raw_row, (str, bytes)):
                continue
            cells = [str(cell).strip() for cell in raw_row]
            if code_index is not None and code_index < len(cells):
                code = cells[code_index]
                if code and code.rsplit(".", 1)[-1] == "0":
                    continue
            if name_index >= len(cells) or not cells[name_index]:
                continue
            tasks.append((row_id, cells[name_index]))
    return tasks


def _aligned_strings(value: object, length: int, *, fallback: Callable[[int], str]) -> list[str]:
    source = value if isinstance(value, list) else []
    return [
        source[index]
        if index < len(source) and isinstance(source[index], str) and source[index]
        else fallback(index)
        for index in range(length)
    ]


def _aligned_values(value: object, length: int, default: object) -> list[object]:
    source = value if isinstance(value, list) else []
    return [deepcopy(source[index] if index < len(source) else default) for index in range(length)]


def _text(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def _strings(value: object) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]
