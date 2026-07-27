from __future__ import annotations

from io import BytesIO
from textwrap import wrap


def render_snapshot_pdf(project_name: str, snapshot: dict) -> bytes:
    """Render a dependency-free, immutable snapshot PDF for Alpha."""

    assessment = snapshot.get("assessment") or {}
    artifacts = snapshot.get("artifacts") or []
    lines = [
        f"{project_name} - OSLO Project Snapshot",
        "",
        f"State: {snapshot.get('state', 'current')}",
        f"Confidence: {assessment.get('confidence_index', 'Not available')}/100",
        f"Clarity: {assessment.get('clarity', 'Not available')}",
        f"Alignment: {assessment.get('alignment', 'Not available')}",
        f"Feasibility: {assessment.get('feasibility', 'Not available')}",
        "Currency: not specified",
        "",
        "Summary",
        str(snapshot.get("summary") or "No summary available."),
        "",
        "Seven plan artifacts",
    ]
    for artifact in artifacts:
        title = artifact.get("title") or artifact.get("artifact_type", "Artifact").title()
        artifact_type = artifact.get("artifact_type", "artifact").replace("_", " ").title()
        lines.extend(
            [
                f"{artifact_type}: {title}",
                str(artifact.get("summary") or "No summary available."),
                "Evidence: "
                + ", ".join(str(ref) for ref in artifact.get("evidence_refs") or ["None"]),
                "",
            ]
        )
    lines.extend(
        [
        "Open issues",
        ]
    )
    for issue in assessment.get("issues") or []:
        if issue.get("status", "open") == "resolved":
            continue
        lines.append(
            f"- [{issue.get('severity', 'issue')}] {issue.get('title', 'Untitled issue')}"
        )
        lines.append(
            "  Evidence: "
            + ", ".join(str(ref) for ref in issue.get("evidence_refs") or ["None"])
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


def _simple_pdf(lines: list[str]) -> bytes:
    safe_lines: list[str] = []
    for line in lines:
        ascii_line = line.encode("latin-1", "replace").decode("latin-1")
        safe_lines.extend(wrap(ascii_line, width=92) or [""])
    pages = [safe_lines[index : index + 54] for index in range(0, len(safe_lines), 54)]
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
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref}\n%%EOF"
        ).encode()
    )
    return output.getvalue()
