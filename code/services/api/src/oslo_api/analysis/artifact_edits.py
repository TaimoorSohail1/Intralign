import hashlib
import json
from collections.abc import Mapping, Sequence

from oslo_api.analysis.models import EvidenceFragment


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


def _text(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def _strings(value: object) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]
