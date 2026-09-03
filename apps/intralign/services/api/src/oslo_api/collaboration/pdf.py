from __future__ import annotations

import re
from io import BytesIO
from textwrap import wrap


def render_report_pdf(
    project_name: str,
    content: dict,
    *,
    analysis_completed_at: object | None = None,
) -> bytes:
    """Render the exact structured report draft shown in the readout editor."""

    lines = [f"{project_name} - Intralign Project Readout"]
    if analysis_completed_at is not None:
        lines.append(f"Analysis dated: {_iso_timestamp(analysis_completed_at)}")
    lines.append("")
    for section in content.get("sections", []):
        lines.append(str(section.get("title") or "Section"))
        lines.extend(
            str(paragraph)
            for paragraph in section.get("body", [])
            if str(paragraph).strip()
        )
        lines.append("")
    lines.extend(
        [
            "This export matches the retained report draft and does not run analysis.",
            "OSLO advises; you decide.",
        ]
    )
    return _simple_pdf(lines)


def render_snapshot_pdf(
    project_name: str,
    snapshot: dict,
    *,
    analysis_completed_at: object | None = None,
) -> bytes:
    """Render a dependency-free, immutable snapshot PDF for Alpha."""

    assessment = snapshot.get("assessment") or {}
    integrity = assessment.get("integrity") or {}
    integrity_bands = {
        str(item.get("key")): item.get("band")
        for item in integrity.get("decomposition", [])
    }
    artifacts = snapshot.get("artifacts") or []
    issues = [
        issue
        for issue in assessment.get("issues") or []
        if issue.get("status", "open") != "resolved"
    ]
    assumptions = [
        (artifact.get("title") or artifact.get("artifact_type", "Artifact").title(), item)
        for artifact in artifacts
        for item in artifact.get("assumptions") or []
    ]
    citation_labels = {
        str(citation.get("reference")): " - ".join(
            value
            for value in (
                str(citation.get("source_name") or "").strip(),
                str(citation.get("location") or "").strip(),
            )
            if value
        )
        for citation in snapshot.get("evidence_citations") or []
        if citation.get("reference")
    }
    lines = [
        f"{project_name} - OSLO Project Readout",
        "Analysis dated: "
        + _iso_timestamp(
            analysis_completed_at
            if analysis_completed_at is not None
            else snapshot.get("published_at", "Not available")
        ),
        "",
        f"State: {snapshot.get('state', 'current')}",
        "Outcome integrity: "
        + str(integrity.get("level", assessment.get("confidence_band", "Not available"))),
        f"Viability: {integrity_bands.get('Viability', 'Not available')}",
        f"Grounding: {integrity_bands.get('Grounding', 'Not available')}",
        f"Adaptability: {integrity_bands.get('Adaptability', 'Not available')}",
        "",
        "Summary",
        _current_read_summary(
            project_name,
            str(snapshot.get("summary") or "No summary available."),
            len(issues),
        ),
        "",
        "What changed",
        "This export reflects the latest retained analysis and artifact revisions.",
        "",
        "Key risks",
    ]
    if issues:
        for issue in issues[:7]:
            lines.append(
                f"- [{issue.get('severity', 'Issue')}] "
                f"{issue.get('title', 'Untitled issue')}: "
                f"{issue.get('why', 'No detail available.')}"
            )
    else:
        lines.append("No open material risk is present in the current read.")
    lines.extend(["", "Assumptions"])
    if assumptions:
        for artifact_title, assumption in assumptions[:12]:
            marker = "load-bearing" if assumption.get("load_bearing") else "supporting"
            lines.append(
                f"- {artifact_title}: {assumption.get('statement', 'Unspecified')} ({marker})"
            )
    else:
        lines.append("No material assumption is recorded in the current read.")
    lines.extend(["", "Plan of action"])
    if issues:
        for issue in issues[:7]:
            lines.append(f"- {issue.get('recommendation', 'Confirm the next action.')}")
    else:
        lines.append("Keep the retained evidence current and record material changes.")
    lines.extend(["", "Decisions needed"])
    questions = [issue.get("clarification") for issue in issues if issue.get("clarification")]
    lines.append(
        str(questions[0])
        if questions
        else "No decision is currently required from the report recipient."
    )
    lines.extend(["", "Appendix - seven plan artifacts"])
    for artifact in artifacts:
        title = artifact.get("title") or artifact.get("artifact_type", "Artifact").title()
        artifact_type = artifact.get("artifact_type", "artifact").replace("_", " ").title()
        lines.extend(
            [
                f"{artifact_type}: {title}",
                str(artifact.get("summary") or "No summary available."),
                "Evidence: "
                + ", ".join(
                    dict.fromkeys(
                        citation_labels.get(
                            str(reference), "Retained project evidence"
                        )
                        for reference in artifact.get("evidence_refs") or ["None"]
                    )
                ),
                "",
            ]
        )
    lines.extend(
        [
            (
                f"Source documents: {snapshot.get('source_document_count', 0)}; "
                f"plan artifacts: {len(artifacts)}."
            ),
        ]
    )
    lines.extend(
        [
            "",
            "This export is a retained OSLO snapshot. "
            "It does not update the project or run analysis.",
            "OSLO advises; you decide.",
        ]
    )
    return _simple_pdf(lines)


def render_full_plan_pdf(
    project_name: str,
    snapshot: dict,
    *,
    analysis_completed_at: object | None = None,
) -> bytes:
    """Render the read-only execution projection shown on Full plan · export."""

    rows = _full_plan_rows(snapshot)
    lines = [
        f"{project_name} - Full plan",
        "Analysis dated: "
        + _iso_timestamp(
            analysis_completed_at
            if analysis_completed_at is not None
            else snapshot.get("published_at", "Not available")
        ),
        "",
        "Task | Work package | Deliverable | Owner | Schedule | State",
    ]
    if rows:
        lines.extend(" | ".join(row) for row in rows)
    else:
        lines.append("No governed execution tasks are present in the retained plan.")
    lines.extend(
        [
            "",
            "Read-only: exporting does not run analysis.",
            "Incomplete ownership and schedule fields are retained as visible warnings.",
            "OSLO advises; you decide.",
        ]
    )
    return _simple_pdf(lines)


def _full_plan_rows(snapshot: dict) -> list[tuple[str, str, str, str, str, str]]:
    artifacts = {
        artifact.get("artifact_type"): artifact
        for artifact in snapshot.get("artifacts") or []
    }
    wbs_rows = _artifact_rows(artifacts.get("work_breakdown") or {})
    if not wbs_rows:
        return []

    schedule = _rows_by_identity(_artifact_rows(artifacts.get("schedule") or {}))
    resources = _rows_by_identity(_artifact_rows(artifacts.get("resources") or {}))
    codes = [str(row["values"][0]).strip() for row in wbs_rows if row["values"]]
    result: list[tuple[str, str, str, str, str, str]] = []
    hierarchy: dict[int, str] = {}
    for row in wbs_rows:
        values = row["values"]
        if len(values) < 2:
            continue
        code = str(values[0]).strip()
        title = str(values[1]).strip()
        if not code or not title:
            continue
        depth = len([part for part in code.split(".") if part and part != "0"])
        hierarchy[depth] = title
        for old_depth in [key for key in hierarchy if key > depth]:
            hierarchy.pop(old_depth, None)
        is_terminal_work_package = code.endswith(".0") and not any(
            candidate != code and candidate.split(".")[0] == code.split(".")[0]
            for candidate in codes
        )
        if (code.endswith(".0") and not is_terminal_work_package) or any(
            candidate != code and candidate.startswith(f"{code}.") for candidate in codes
        ):
            continue

        schedule_row = schedule.get(row["id"]) or schedule.get(title.casefold())
        resource_row = resources.get(row["id"]) or resources.get(title.casefold())
        owner = _column_value(resource_row, ("owner", "assigned", "person")) or _column_value(
            schedule_row, ("owner", "assigned", "person")
        )
        start = _column_value(schedule_row, ("start", "start date", "from"))
        due = _column_value(schedule_row, ("end", "due", "due date", "finish", "to"))
        schedule_label = (
            f"{start} - {due}"
            if start and due
            else start or due or "unscheduled"
        )
        provenance = str(row.get("provenance") or "from_oslo")
        state = "yours" if provenance == "confirmed_by_user" else "inferred"
        result.append(
            (
                title,
                (
                    title
                    if is_terminal_work_package
                    else hierarchy.get(max(depth - 1, 1), "-")
                ),
                (
                    str(row.get("section_heading") or "Plan")
                    if is_terminal_work_package
                    else hierarchy.get(1, title)
                ),
                owner or "- unowned",
                schedule_label,
                state,
            )
        )
    return result


def _artifact_rows(artifact: dict) -> list[dict]:
    rows: list[dict] = []
    for section in (artifact.get("content") or {}).get("sections") or []:
        columns = [str(value).strip().casefold() for value in section.get("columns") or []]
        row_ids = section.get("row_ids") or []
        provenance = section.get("row_provenance") or []
        for index, values in enumerate(section.get("rows") or []):
            rows.append(
                {
                    "id": str(row_ids[index]) if index < len(row_ids) else "",
                    "section_heading": str(section.get("heading") or "Plan"),
                    "columns": columns,
                    "values": [str(value).strip() for value in values],
                    "provenance": provenance[index] if index < len(provenance) else None,
                }
            )
    return rows


def _rows_by_identity(rows: list[dict]) -> dict[str, dict]:
    index: dict[str, dict] = {}
    for row in rows:
        if row["id"]:
            index[row["id"]] = row
        if row["values"]:
            index.setdefault(str(row["values"][0]).casefold(), row)
    return index


def _column_value(row: dict | None, candidates: tuple[str, ...]) -> str:
    if not row:
        return ""
    for candidate in candidates:
        for index, column in enumerate(row["columns"]):
            if (candidate == column or candidate in column) and index < len(row["values"]):
                return str(row["values"][index]).strip()
    return ""


def _current_read_summary(project_name: str, summary: str, open_issue_count: int) -> str:
    open_label = (
        f"{open_issue_count} open "
        f"{'finding' if open_issue_count == 1 else 'findings'}"
    )
    visible_summary = re.sub(
        r"\b\d+\s+open\s+(?:findings?|issues?|points?)\b",
        open_label,
        summary,
        flags=re.IGNORECASE,
    )
    governed_detail = re.search(
        r"\bAt the (?:orientation|expanded|validated) stage,.*$",
        visible_summary,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if project_name.strip() and governed_detail:
        return f"{project_name.strip()}. {governed_detail.group(0)}"
    return visible_summary


def _iso_timestamp(value: object) -> str:
    isoformat = getattr(value, "isoformat", None)
    rendered = isoformat() if callable(isoformat) else str(value)
    return rendered.replace("+00:00", "Z")


def _simple_pdf(lines: list[str]) -> bytes:
    heading_lines = {
        "Summary",
        "What changed",
        "Key risks",
        "Assumptions",
        "Plan of action",
        "Decisions needed",
        "Appendix - seven plan artifacts",
    }
    logical_lines: list[tuple[str, list[str]]] = []
    for line in lines:
        safe_line = _pdf_safe_text(line)
        logical_lines.append((safe_line, wrap(safe_line, width=92) or [""]))

    blocks: list[list[str]] = []
    index = 0
    while index < len(logical_lines):
        safe_line, wrapped = logical_lines[index]
        if safe_line in heading_lines and index + 1 < len(logical_lines):
            # Keep a section heading with its first content line.
            blocks.append(wrapped + logical_lines[index + 1][1])
            index += 2
            continue
        blocks.append(wrapped)
        index += 1

    pages: list[list[str]] = []
    current_page: list[str] = []
    for block in blocks:
        if current_page and len(current_page) + len(block) > 54:
            pages.append(current_page)
            current_page = []
        while len(block) > 54:
            room = 54 - len(current_page)
            current_page.extend(block[:room])
            pages.append(current_page)
            current_page = []
            block = block[room:]
        current_page.extend(block)
    if current_page:
        pages.append(current_page)
    pages = pages or [[""]]
    page_object_numbers = [3 + index * 2 for index in range(len(pages))]
    font_object_number = 3 + len(pages) * 2
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        (
            b"<< /Type /Pages /Kids ["
            + b" ".join(f"{number} 0 R".encode() for number in page_object_numbers)
            + f"] /Count {len(pages)} >>".encode()
        ),
    ]
    for page_index, page_lines in enumerate(pages):
        page_number = page_object_numbers[page_index]
        content_number = page_number + 1
        content = ["BT", "/F1 10 Tf", "52 780 Td", "13 TL"]
        for line_index, line in enumerate(page_lines):
            escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            if line_index:
                content.append("T*")
            content.append(f"({escaped}) Tj")
        content.append("ET")
        stream = "\n".join(content).encode("latin-1")
        objects.extend(
            [
                (
                    f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                    f"/Resources << /Font << /F1 {font_object_number} 0 R >> >> "
                    f"/Contents {content_number} 0 R >>"
                ).encode(),
                (
                    b"<< /Length "
                    + str(len(stream)).encode()
                    + b" >>\nstream\n"
                    + stream
                    + b"\nendstream"
                ),
            ]
        )
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    output = BytesIO()
    output.write(b"%PDF-1.4\n")
    offsets = [0]
    for number, obj in enumerate(objects, start=1):
        offsets.append(output.tell())
        output.write(f"{number} 0 obj\n".encode())
        output.write(obj)
        output.write(b"\nendobj\n")
    xref = output.tell()
    output.write(f"xref\n0 {len(objects) + 1}\n".encode())
    output.write(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.write(f"{offset:010d} 00000 n \n".encode())
    output.write(
        (f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF").encode()
    )
    return output.getvalue()


def _pdf_safe_text(value: object) -> str:
    """Normalize common project-document glyphs for the built-in PDF font."""
    text = str(value)
    replacements = {
        "\u00a0": " ",
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": " - ",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2022": "-",
        "\u2192": "->",
        "\u2264": "<=",
        "\u2265": ">=",
    }
    for source, replacement in replacements.items():
        text = text.replace(source, replacement)
    return text.encode("latin-1", "replace").decode("latin-1")
