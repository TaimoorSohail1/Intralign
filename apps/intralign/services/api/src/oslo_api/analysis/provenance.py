from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from typing import Any

from oslo_api.analysis.models import (
    ARTIFACT_TYPES,
    Artifact,
    ArtifactAssumption,
    ArtifactSection,
    ArtifactType,
    Issue,
    normalize_evidence_state,
)

_OWNER_LANGUAGE = re.compile(
    r"\b(owner|ownership|accountable|responsib(?:le|ility)|approver)\b",
    re.IGNORECASE,
)
_NUMBER = re.compile(r"\b\d+(?:[.,]\d+)?\b")
_WORD = re.compile(r"[a-z0-9]+")
_MATCH_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "for",
    "from",
    "has",
    "in",
    "is",
    "it",
    "meet",
    "no",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "with",
}

_GROUNDING_BANDS = ("Fragile", "Weak", "Developing", "Solid", "Sound")


def _grounding_band(value: float) -> str:
    if value >= 1:
        return "Sound"
    if value >= 0.75:
        return "Solid"
    if value >= 0.5:
        return "Developing"
    if value >= 0.25:
        return "Weak"
    return "Fragile"


def grounding_issue_state(
    issue: Issue | Mapping[str, Any],
    action: Mapping[str, Any] | None = None,
) -> str:
    """Return the canonical state of one load-bearing issue.

    Only an evidence-bearing verification grounds the read. Building plan
    structure, routing work, or merely resolving a non-verification finding must
    not manufacture Grounding.
    """

    action = action or {}
    issue_status = (
        issue.status if isinstance(issue, Issue) else str(issue.get("status") or "open")
    )
    status = str(action.get("status") or issue_status)
    act = str(action.get("action") or action.get("act") or "")
    basis = action.get("basis")
    evidence_refs = (
        issue.evidence_refs
        if isinstance(issue, Issue)
        else tuple(issue.get("evidence_refs") or ())
    )
    has_evidence = bool(basis or evidence_refs)
    primary_act = (
        issue.primary_act
        if isinstance(issue, Issue)
        else str(issue.get("primary_act") or "")
    )

    if (
        status == "resolved"
        and has_evidence
        and act in {"confirm", "ground", "answer", "clarification"}
    ):
        return "grounded"
    if status == "resolved" and primary_act == "verify" and has_evidence:
        return "grounded"
    if act == "route" or status == "routed":
        return "routed"
    if status in {"addressed", "needs_fix", "needs_grounding", "resolved"}:
        return "addressed"
    return "inferred"


def build_grounding_projection(
    *,
    issues: Iterable[Issue | Mapping[str, Any]],
    issue_actions: Iterable[Mapping[str, Any]] = (),
    outcome_root_grounded: bool = True,
) -> dict[str, Any]:
    """Project one Grounding denominator and band for every product surface."""

    actions = {
        str(action.get("issue_id") or action.get("issue_stable_key") or ""): action
        for action in issue_actions
    }
    counts = {state: 0 for state in ("grounded", "addressed", "routed", "inferred")}
    for issue in issues:
        load_bearing = (
            issue.load_bearing
            if isinstance(issue, Issue)
            else bool(issue.get("load_bearing", True))
        )
        if not load_bearing:
            continue
        issue_id = issue.id if isinstance(issue, Issue) else str(issue.get("id") or "")
        counts[grounding_issue_state(issue, actions.get(issue_id))] += 1

    total = sum(counts.values())
    basis = counts["grounded"] / max(1, total)
    band = _grounding_band(basis)
    if not outcome_root_grounded:
        band = _GROUNDING_BANDS[min(_GROUNDING_BANDS.index(band), 1)]
    return {
        **counts,
        "total": total,
        "basis": basis,
        "band": band,
    }


def _claim_counts(artifact: Artifact | None) -> tuple[int, int]:
    if artifact is None:
        return 0, 0
    if not artifact.sections:
        grounded = int(bool(artifact.evidence_refs) or artifact.basis == "confirmed_by_user")
        return grounded, 0 if grounded else 1

    grounded = 0
    inferred = 0
    for section in artifact.sections:
        if section.rows:
            for index, _row in enumerate(section.rows):
                state = (
                    normalize_evidence_state(section.row_states[index])
                    if index < len(section.row_states)
                    else "unknown"
                )
                references = (
                    section.row_evidence_refs[index]
                    if index < len(section.row_evidence_refs)
                    else ()
                )
                if state in {"confirmed", "conflicting"} and references:
                    grounded += 1
                else:
                    inferred += 1
            continue
        claim_count = len(section.bullets) + int(bool(section.body.strip()))
        if section.evidence_refs:
            grounded += claim_count
        else:
            inferred += claim_count
    return grounded, inferred


def _untraceable_number_count(artifacts: tuple[Artifact, ...]) -> int:
    count = 0
    for artifact in artifacts:
        for section in artifact.sections:
            for index, row in enumerate(section.rows):
                references = (
                    section.row_evidence_refs[index]
                    if index < len(section.row_evidence_refs)
                    else ()
                )
                if not references and _NUMBER.search(" ".join(row)):
                    count += 1
            if not section.evidence_refs:
                count += sum(_NUMBER.search(item) is not None for item in section.bullets)
                if _NUMBER.search(section.body):
                    count += 1
    return count


def _match_terms(value: str) -> set[str]:
    return {
        word
        for word in _WORD.findall(value.casefold())
        if len(word) > 2 and word not in _MATCH_STOP_WORDS
    }


def _related_issue(
    *,
    artifact_type: ArtifactType,
    assumption_id: str,
    statement: str,
    evidence_refs: tuple[str, ...],
    issues: tuple[Issue, ...],
) -> Issue | None:
    """Link assumptions to issues without requiring identical model wording."""

    assumption_terms = _match_terms(statement)
    assumption_references = set(evidence_refs)
    ranked: list[tuple[int, float, Issue]] = []
    for issue in issues:
        issue_text = " ".join(
            (
                issue.title,
                issue.why,
                issue.recommendation,
                issue.clarification or "",
            )
        )
        issue_terms = _match_terms(issue_text)
        shared_terms = assumption_terms & issue_terms
        term_coverage = len(shared_terms) / max(1, min(len(assumption_terms), 6))
        shared_evidence = bool(assumption_references & set(issue.evidence_refs))
        mentions_id = assumption_id.casefold() in issue_text.casefold()

        # Evidence identifies the originating passage; shared concepts disambiguate
        # when several issues cite the same page. An explicit assumption ID is exact.
        if mentions_id:
            ranked.append((3, term_coverage, issue))
        elif (
            shared_evidence
            and len(shared_terms) >= (2 if issue.artifact_type == artifact_type else 3)
            and term_coverage >= 0.5
        ):
            ranked.append(
                (
                    2 + int(issue.artifact_type == artifact_type),
                    term_coverage,
                    issue,
                )
            )
        elif (
            issue.artifact_type == artifact_type
            and len(shared_terms) >= 3
            and term_coverage >= 0.5
        ):
            ranked.append((1, term_coverage, issue))

    if not ranked:
        return None
    return max(ranked, key=lambda item: (item[0], item[1]))[2]


def build_project_provenance(
    *,
    artifacts: tuple[Artifact, ...],
    issues: tuple[Issue, ...],
    issue_actions: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Build the canonical provenance projection once, at the API boundary.

    Every UI reads this projection. Claim grounding is based on persisted row
    states plus evidence references; pages never reinterpret artifact prose.
    """

    by_type = {artifact.artifact_type: artifact for artifact in artifacts}
    artifact_rows: list[dict[str, Any]] = []
    grounded_claims = 0
    inferred_claims = 0
    for artifact_type in ARTIFACT_TYPES:
        artifact = by_type.get(artifact_type)
        grounded, inferred = _claim_counts(artifact)
        total = grounded + inferred
        grounded_claims += grounded
        inferred_claims += inferred
        artifact_rows.append(
            {
                "artifact_type": artifact_type.value,
                "grounded": grounded,
                "inferred": inferred,
                "total": total,
                "verify_first": total > 0 and inferred > grounded,
            }
        )

    open_issues = tuple(issue for issue in issues if issue.status != "resolved")
    assumptions: list[dict[str, Any]] = []
    for artifact in artifacts:
        for assumption in artifact.assumptions:
            related = _related_issue(
                artifact_type=artifact.artifact_type,
                assumption_id=assumption.id,
                statement=assumption.statement,
                evidence_refs=assumption.evidence_refs,
                issues=open_issues,
            )
            assumptions.append(
                {
                    "id": assumption.id,
                    "artifact_type": artifact.artifact_type.value,
                    "text": assumption.statement,
                    "issue_id": related.id if related else None,
                    "issue_title": related.title if related else None,
                    "load_bearing": assumption.load_bearing or related is not None,
                    "state": normalize_evidence_state(assumption.state),
                }
            )
    unique_assumptions: dict[str, dict[str, Any]] = {}
    state_priority = {"confirmed": 3, "conflicting": 2, "inferred": 1}
    for item in assumptions:
        key = " ".join(_WORD.findall(item["text"].casefold()))
        current = unique_assumptions.get(key)
        if current is None:
            unique_assumptions[key] = item
            continue
        preferred = max(
            (current, item),
            key=lambda candidate: (
                candidate["issue_id"] is not None,
                candidate["load_bearing"],
                state_priority.get(candidate["state"], 0),
            ),
        )
        unique_assumptions[key] = {
            **preferred,
            "load_bearing": current["load_bearing"] or item["load_bearing"],
            "state": max(
                (current["state"], item["state"]),
                key=lambda state: state_priority.get(state, 0),
            ),
        }
    assumptions = list(unique_assumptions.values())
    assumptions.sort(key=lambda item: (not item["load_bearing"], item["text"].casefold()))

    unowned_parties = sum(
        bool(_OWNER_LANGUAGE.search(f"{issue.title} {issue.why}"))
        for issue in open_issues
        if issue.artifact_type
        in {ArtifactType.WORK_BREAKDOWN, ArtifactType.RESOURCES, ArtifactType.CONTEXT}
    )
    load_bearing = sum(
        assumption["load_bearing"] and assumption["state"] != "confirmed"
        for assumption in assumptions
    )
    intent = next(
        (item for item in artifact_rows if item["artifact_type"] == "intent"),
        None,
    )
    grounding = build_grounding_projection(
        issues=issues,
        issue_actions=issue_actions,
        outcome_root_grounded=(intent is None or intent["inferred"] == 0),
    )
    return {
        "schema_version": 1,
        "artifacts": artifact_rows,
        "assumptions": assumptions,
        "grounded_claims": grounded_claims,
        "inferred_claims": inferred_claims,
        "total_claims": grounded_claims + inferred_claims,
        "load_bearing_inferences": load_bearing,
        "grounding": grounding,
        "structure": {
            "unconfirmed_dependencies": load_bearing,
            "unowned_parties": unowned_parties,
            "untraceable_numbers": _untraceable_number_count(artifacts),
        },
        "this_week": {
            "user_grounded": sum(
                artifact.basis == "confirmed_by_user" for artifact in artifacts
            ),
            "oslo_inferred": inferred_claims,
        },
    }


def build_serialized_project_provenance(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Rebuild canonical provenance for retained snapshots written before it was stored.

    History reads immutable JSON snapshots rather than the live dataclasses used by
    Overview. Rehydrating the provenance inputs here keeps both surfaces on the same
    calculation and prevents legacy snapshots from being reported as ``0 of 0``.
    """

    artifacts = tuple(
        Artifact(
            artifact_type=ArtifactType(item["artifact_type"]),
            title=str(item.get("title", "")),
            summary=str(item.get("summary", "")),
            reliability=str(item.get("reliability", "Unknown")),
            evidence_refs=tuple(item.get("evidence_refs", [])),
            basis=str(item.get("basis", "derived")),
            sections=tuple(
                ArtifactSection(
                    heading=str(section.get("heading", "")),
                    body=str(section.get("body", "")),
                    bullets=tuple(section.get("bullets", [])),
                    columns=tuple(section.get("columns", [])),
                    rows=tuple(tuple(row) for row in section.get("rows", [])),
                    evidence_refs=tuple(section.get("evidence_refs", [])),
                    row_evidence_refs=tuple(
                        tuple(references)
                        for references in section.get("row_evidence_refs", [])
                    ),
                    row_states=tuple(section.get("row_states", [])),
                )
                for section in item.get("sections", [])
            ),
            assumptions=tuple(
                ArtifactAssumption(
                    id=str(assumption.get("id", "")),
                    statement=str(assumption.get("statement", "")),
                    state=str(assumption.get("state", "inferred")),
                    load_bearing=bool(assumption.get("load_bearing", False)),
                    evidence_refs=tuple(assumption.get("evidence_refs", [])),
                )
                for assumption in item.get("assumptions", [])
            ),
            project_title=item.get("project_title"),
        )
        for item in snapshot.get("artifacts", [])
    )
    assessment = snapshot.get("assessment") or {}
    issues = tuple(
        Issue(
            id=str(item.get("id", "")),
            artifact_type=ArtifactType(item["artifact_type"]),
            dimension=str(item.get("dimension", "")),
            severity=str(item.get("severity", "warning")),
            title=str(item.get("title", "")),
            why=str(item.get("why", "")),
            recommendation=str(item.get("recommendation", "")),
            evidence_refs=tuple(item.get("evidence_refs", [])),
            clarification=item.get("clarification"),
            status=str(item.get("status", "open")),
            load_bearing=bool(item.get("load_bearing", True)),
            primary_act=str(item.get("primary_act", "")),
        )
        for item in assessment.get("issues", [])
    )
    return build_project_provenance(artifacts=artifacts, issues=issues)
