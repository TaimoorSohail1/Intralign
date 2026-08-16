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
        f"Confidence: {assessment.get('confidence_index', 'Not available')}/100",
        f"Clarity: {assessment.get('clarity', 'Not available')}",
        f"Alignment: {assessment.get('alignment', 'Not available')}",
        f"Feasibility: {assessment.get('feasibility', 'Not available')}",
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
