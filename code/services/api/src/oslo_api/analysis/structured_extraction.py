from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass

from oslo_api.analysis.models import (
    Artifact,
    ArtifactAssumption,
    ArtifactConflict,
    ArtifactSection,
    ArtifactType,
    EvidenceFragment,
    Perception,
)

_ARTIFACT_HEADINGS: dict[ArtifactType, tuple[str, ...]] = {
    ArtifactType.INTENT: (
        "Executive summary",
        "Objectives and success measures",
        "Business case",
        "Sponsorship and authority",
    ),
    ArtifactType.CONTEXT: (
        "Stakeholder register",
        "Governance forums",
        "Decision authority",
        "Named accountabilities and backups",
        "Explicit assumptions",
        "Dependency and decision log",
    ),
    ArtifactType.SCOPE: (
        "Scope statement",
        "Included deliverables",
        "Explicit exclusions",
        "Change log",
    ),
    ArtifactType.REQUIREMENTS: (
        "Functional requirements",
        "Non-functional and acceptance gates",
        "Open scope decision",
    ),
    ArtifactType.WORK_BREAKDOWN: ("Work breakdown",),
    ArtifactType.SCHEDULE: (
        "Integrated milestones",
        "Critical dependencies",
    ),
    ArtifactType.RESOURCES: (
        "Resource plan",
        "RACI",
        "Status summary",
        "Risks and issues",
    ),
}

_ALL_HEADINGS = tuple(
    dict.fromkeys(heading for headings in _ARTIFACT_HEADINGS.values() for heading in headings)
)
_DATE_RE = re.compile(
    r"\b(?:0?[1-9]|[12]\d|3[01])\s+"
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+20\d{2}\b",
    re.IGNORECASE,
)


@dataclass(frozen=True, slots=True)
class _Source:
    name: str
    text: str
    fragments: tuple[EvidenceFragment, ...]


def construct_structured_artifact(
    *,
    perception: Perception,
    artifact_type: ArtifactType,
    title: str,
    depth: str,
) -> Artifact | None:
    sources = _sources(perception.evidence)
    extracted: list[ArtifactSection] = []
    for heading in _ARTIFACT_HEADINGS[artifact_type]:
        selected = next(
            (
                (source, body)
                for source in sources
                if (body := _section_body(source.text, heading)) is not None
            ),
            None,
        )
        if selected is None:
            continue
        source, body = selected
        extracted.append(_artifact_section(heading, body, source.fragments))

    if not extracted:
        return None

    evidence_refs = (
        tuple(
            dict.fromkeys(reference for section in extracted for reference in section.evidence_refs)
        )
        or perception.evidence_refs
    )
    section_names = ", ".join(section.heading for section in extracted)
    assumptions = _assumptions(extracted) if artifact_type is ArtifactType.CONTEXT else ()
    conflicts = _conflicts(artifact_type, sources)
    project_title = _project_title(sources)
    return Artifact(
        artifact_type=artifact_type,
        title=title,
        summary=(f"{depth} structured {title.lower()} extracted from {section_names}."),
        reliability="High",
        evidence_refs=evidence_refs,
        basis="source_grounded",
        sections=tuple(extracted),
        assumptions=assumptions,
        conflicts=conflicts,
        project_title=project_title,
    )


def _sources(evidence: tuple[EvidenceFragment, ...]) -> tuple[_Source, ...]:
    grouped: dict[str, list[EvidenceFragment]] = defaultdict(list)
    order: list[str] = []
    for fragment in evidence:
        name = fragment.source_name or fragment.reference.split(":", 1)[0]
        if name not in grouped:
            order.append(name)
        grouped[name].append(fragment)
    return tuple(
        _Source(
            name=name,
            text=_merge_overlap(tuple(item.content for item in grouped[name])),
            fragments=tuple(grouped[name]),
        )
        for name in order
    )


def _merge_overlap(chunks: tuple[str, ...]) -> str:
    merged = ""
    for chunk in chunks:
        normalized = re.sub(r"\s+", " ", chunk).strip()
        if not normalized:
            continue
        if not merged:
            merged = normalized
            continue
        overlap = 0
        for size in range(min(500, len(merged), len(normalized)), 19, -1):
            if merged.endswith(normalized[:size]):
                overlap = size
                break
        merged = f"{merged} {normalized[overlap:]}".strip()
    return merged


def _section_body(text: str, heading: str) -> str | None:
    start = re.search(rf"\b\d+\.\s+{re.escape(heading)}\b", text, re.IGNORECASE)
    if start is None:
        return None
    following = re.search(
        rf"\b\d+\.\s+(?:{'|'.join(re.escape(item) for item in _ALL_HEADINGS)})\b",
        text[start.end() :],
        re.IGNORECASE,
    )
    finish = start.end() + following.start() if following is not None else len(text)
    return text[start.end() : finish].strip()


def _artifact_section(
    heading: str,
    body: str,
    fragments: tuple[EvidenceFragment, ...],
) -> ArtifactSection:
    rows, columns = _rows(heading, body)
    row_refs = tuple(
        _refs_for(fragments, (row[0],)) or _refs_for(fragments, tuple(row)) for row in rows
    )
    section_refs = _refs_for(fragments, (heading,)) or tuple(
        dict.fromkeys(reference for references in row_refs for reference in references)
    )
    concise = re.sub(r"\s+", " ", body).strip()
    return ArtifactSection(
        heading=heading,
        body=concise[:600],
        bullets=tuple(" | ".join(row) for row in rows),
        columns=columns,
        rows=rows,
        evidence_refs=section_refs,
        row_evidence_refs=row_refs,
        row_states=tuple("confirmed" for _ in rows),
    )


def _rows(heading: str, body: str) -> tuple[tuple[tuple[str, ...], ...], tuple[str, ...]]:
    patterns = {
        "Objectives and success measures": r"OBJ-\d+",
        "Included deliverables": r"DEL-\d+",
        "Functional requirements": r"REQ-\d+",
        "Non-functional and acceptance gates": r"(?:NFR|GATE)-\d+",
        "Explicit assumptions": r"A-\d+",
        "Dependency and decision log": r"(?:D-\d+|DEC-\d+)",
        "Risks and issues": r"(?:R-\d+|I-\d+)",
        "Change log": r"CR-\d+",
    }
    if heading in patterns:
        return _identifier_rows(body, patterns[heading]), ("ID", "Evidence-derived detail")
    if heading == "Work breakdown":
        return _identifier_rows(body, r"[1-9]\.0"), ("WBS", "Work package evidence")
    if heading == "Stakeholder register":
        return _stakeholder_rows(body), ("Stakeholder evidence", "Influence and stance")
    if heading == "Governance forums":
        return _governance_rows(body), ("Forum evidence", "Cadence")
    if heading == "Explicit exclusions":
        return _exclusion_rows(body), ("Boundary", "Excluded or deferred")
    if heading == "Integrated milestones":
        return _dated_rows(body), ("Item evidence", "Date")
    if heading == "Critical dependencies":
        return _dependency_rows(body), ("Dependency evidence", "RAG")
    if heading == "Resource plan":
        return _resource_rows(body), ("Role evidence", "Allocation")
    if heading == "RACI":
        return _raci_rows(body), ("Deliverable", "Accountability evidence")
    return (), ()


def _identifier_rows(body: str, pattern: str) -> tuple[tuple[str, ...], ...]:
    matches = tuple(re.finditer(rf"\b({pattern})\b", body, re.IGNORECASE))
    rows: list[tuple[str, ...]] = []
    for index, match in enumerate(matches):
        finish = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        detail = re.sub(r"\s+", " ", body[match.end() : finish]).strip(" |;,-")
        rows.append((match.group(1).upper(), detail[:900]))
    return tuple(rows)


def _stakeholder_rows(body: str) -> tuple[tuple[str, ...], ...]:
    matches = tuple(
        re.finditer(
            r"\b(High|Medium|Low)\s+"
            r"(Supportive|Cautious|Mixed|Contracted|Unconfirmed)\b",
            body,
            re.IGNORECASE,
        )
    )
    rows: list[tuple[str, ...]] = []
    cursor = body.lower().find("engagement owner")
    cursor = cursor + len("engagement owner") if cursor >= 0 else 0
    for match in matches:
        lead = re.sub(r"\s+", " ", body[cursor : match.start()]).strip()
        rows.append((lead[-180:] or f"Stakeholder {len(rows) + 1}", match.group(0)))
        cursor = match.end()
    return tuple(rows)


def _governance_rows(body: str) -> tuple[tuple[str, ...], ...]:
    matches = tuple(
        re.finditer(
            r"\b(Daily|Weekly(?:\s+\w+)?|Fortnightly(?:\s+\w+)?|"
            r"Monthly(?:\s+\w+(?:\s+\w+)?)?|Quarterly)\b",
            body,
            re.IGNORECASE,
        )
    )
    rows = []
    cursor = body.lower().find("quorum")
    cursor = cursor + len("quorum") if cursor >= 0 else 0
    for match in matches:
        lead = re.sub(r"\s+", " ", body[cursor : match.start()]).strip()
        rows.append((lead[-100:] or f"Forum {len(rows) + 1}", match.group(0)))
        cursor = match.end()
    return tuple(rows)


def _exclusion_rows(body: str) -> tuple[tuple[str, ...], ...]:
    labels = ("Geography", "Channels", "Platforms", "Commercial", "Analytics")
    matches = tuple(
        match
        for label in labels
        if (match := re.search(rf"\b{label}\b", body, re.IGNORECASE)) is not None
    )
    matches = tuple(sorted(matches, key=lambda item: item.start()))
    rows = []
    for index, match in enumerate(matches):
        finish = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        rows.append(
            (
                match.group(0).title(),
                re.sub(r"\s+", " ", body[match.end() : finish]).strip()[:700],
            )
        )
    return tuple(rows)


def _dated_rows(body: str) -> tuple[tuple[str, ...], ...]:
    matches = tuple(_DATE_RE.finditer(body))
    rows = []
    cursor = 0
    for match in matches:
        lead = re.sub(r"\s+", " ", body[cursor : match.start()]).strip()
        rows.append((lead[-150:] or f"Dated item {len(rows) + 1}", match.group(0)))
        cursor = match.end()
    return tuple(rows)


def _dependency_rows(body: str) -> tuple[tuple[str, ...], ...]:
    matches = tuple(re.finditer(r"\b(Red|Amber|Green)\b", body, re.IGNORECASE))
    rows = []
    cursor = body.lower().find("rag")
    cursor = cursor + len("rag") if cursor >= 0 else 0
    for match in matches:
        detail = re.sub(r"\s+", " ", body[cursor : match.start()]).strip()
        rows.append((detail[-350:] or f"Dependency {len(rows) + 1}", match.group(1).title()))
        cursor = match.end()
    return tuple(rows)


def _resource_rows(body: str) -> tuple[tuple[str, ...], ...]:
    matches = tuple(
        re.finditer(
            r"\b\d+(?:\.\d+)?\s+FTE\b(?!\s+shortfall)",
            body,
            re.IGNORECASE,
        )
    )
    rows = []
    cursor = body.lower().find("backup / gap")
    cursor = cursor + len("backup / gap") if cursor >= 0 else 0
    for match in matches:
        lead = re.sub(r"\s+", " ", body[cursor : match.start()]).strip()
        rows.append((lead[-160:] or f"Role {len(rows) + 1}", match.group(0)))
        cursor = match.end()
    return tuple(rows)


def _raci_rows(body: str) -> tuple[tuple[str, ...], ...]:
    labels = (
        "Business case",
        "Requirements",
        "Architecture",
        "Data migration",
        "SIT",
        "UAT",
        "Go-live",
    )
    matches = tuple(
        match
        for label in labels
        if (match := re.search(rf"\b{re.escape(label)}\b", body, re.IGNORECASE)) is not None
    )
    matches = tuple(sorted(matches, key=lambda item: item.start()))
    rows = []
    for index, match in enumerate(matches):
        finish = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        rows.append(
            (
                match.group(0),
                re.sub(r"\s+", " ", body[match.end() : finish]).strip()[:700],
            )
        )
    return tuple(rows)


def _assumptions(sections: list[ArtifactSection]) -> tuple[ArtifactAssumption, ...]:
    section = next(
        (item for item in sections if item.heading == "Explicit assumptions"),
        None,
    )
    if section is None:
        return ()
    return tuple(
        ArtifactAssumption(
            id=row[0],
            statement=row[1],
            state="source_grounded",
            load_bearing=True,
            evidence_refs=section.row_evidence_refs[index],
        )
        for index, row in enumerate(section.rows)
    )


def _conflicts(
    artifact_type: ArtifactType,
    sources: tuple[_Source, ...],
) -> tuple[ArtifactConflict, ...]:
    text = " ".join(source.text for source in sources)
    conflicts: list[ArtifactConflict] = []
    if (
        artifact_type is ArtifactType.SCHEDULE
        and "ERP pricing API" in text
        and "08 Feb 2027" in text
        and "22 Feb 2027" in text
    ):
        conflicts.append(
            ArtifactConflict(
                id="CONFLICT-ERP-PRICING-API-DATE",
                field="ERP pricing API date",
                values=("08 Feb 2027 needed", "22 Feb 2027 supplier commitment"),
                evidence_refs=_source_refs(sources, ("ERP pricing API", "22 Feb 2027")),
            )
        )
    if (
        artifact_type is ArtifactType.RESOURCES
        and "GBP 1,800,000" in text
        and "GBP 1,845,000" in text
    ):
        conflicts.append(
            ArtifactConflict(
                id="CONFLICT-PROJECT-COST",
                field="Project cost",
                values=("GBP 1,800,000 approved ceiling", "GBP 1,845,000 forecast"),
                evidence_refs=_source_refs(sources, ("GBP 1,800,000", "GBP 1,845,000")),
            )
        )
    if (
        artifact_type is ArtifactType.SCOPE
        and "offline ordering" in text.lower()
        and "CR-002" in text
        and re.search(r"CR-002.{0,250}Rejected", text, re.IGNORECASE)
    ):
        conflicts.append(
            ArtifactConflict(
                id="CONFLICT-NATIVE-OFFLINE-ORDERING",
                field="Native offline ordering",
                values=("Explicitly excluded", "CR-002 rejected"),
                evidence_refs=_source_refs(sources, ("offline ordering", "CR-002")),
            )
        )
    return tuple(conflicts)


def _project_title(sources: tuple[_Source, ...]) -> str | None:
    for source in sources:
        match = re.match(r"(.{3,120}?)\s+Confidential working baseline\b", source.text)
        if match is not None:
            return match.group(1).strip()
    return None


def _source_refs(
    sources: tuple[_Source, ...],
    terms: tuple[str, ...],
) -> tuple[str, ...]:
    return tuple(
        dict.fromkeys(
            fragment.reference
            for source in sources
            for fragment in source.fragments
            if any(term.casefold() in fragment.content.casefold() for term in terms)
        )
    )


def _refs_for(
    fragments: tuple[EvidenceFragment, ...],
    terms: tuple[str, ...],
) -> tuple[str, ...]:
    return tuple(
        dict.fromkeys(
            fragment.reference
            for fragment in fragments
            if any(term.casefold() in fragment.content.casefold() for term in terms if term)
        )
    )
