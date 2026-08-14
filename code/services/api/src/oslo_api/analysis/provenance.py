from __future__ import annotations

import re
from typing import Any

from oslo_api.analysis.models import (
    ARTIFACT_TYPES,
    Artifact,
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
                    "state": assumption.state,
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
    return {
        "schema_version": 1,
        "artifacts": artifact_rows,
        "assumptions": assumptions,
        "grounded_claims": grounded_claims,
        "inferred_claims": inferred_claims,
        "total_claims": grounded_claims + inferred_claims,
        "load_bearing_inferences": load_bearing,
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
