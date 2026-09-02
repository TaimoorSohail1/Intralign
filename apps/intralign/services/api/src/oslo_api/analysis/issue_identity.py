import hashlib
import re
from dataclasses import replace
from difflib import SequenceMatcher

from oslo_api.analysis.models import Issue

_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "in",
    "inconsistency",
    "inconsistent",
    "internal",
    "internally",
    "is",
    "it",
    "no",
    "not",
    "of",
    "on",
    "or",
    "project",
    "the",
    "to",
    "what",
    "which",
    "conflict",
    "conflicting",
}

_SEVERITY_RANK = {"Low": 0, "Moderate": 1, "Critical": 2}
_STATUS_RANK = {"resolved": 0, "answered": 1, "addressed": 2, "open": 3}


def deduplicate_issues(issues: tuple[Issue, ...]) -> tuple[Issue, ...]:
    """Merge repeated descriptions of one evidence-backed root cause.

    Findings in different artifacts are only merged when they cite shared
    evidence. This keeps genuinely distinct downstream impacts while removing
    the common model/deterministic duplicate of the same source defect.
    """

    merged: list[Issue] = []
    for issue in issues:
        duplicate_index = next(
            (
                index
                for index, existing in enumerate(merged)
                if _same_root_cause(issue, existing)
            ),
            None,
        )
        if duplicate_index is None:
            merged.append(issue)
            continue

        existing = merged[duplicate_index]
        preferred = max(
            (existing, issue),
            key=lambda item: (
                _SEVERITY_RANK.get(item.severity, -1),
                len(item.evidence_refs),
                len(item.why),
            ),
        )
        merged[duplicate_index] = replace(
            preferred,
            evidence_refs=tuple(
                dict.fromkeys((*existing.evidence_refs, *issue.evidence_refs))
            ),
            clarification=preferred.clarification
            or existing.clarification
            or issue.clarification,
            status=max(
                (existing.status, issue.status),
                key=lambda value: _STATUS_RANK.get(value, -1),
            ),
        )
    return tuple(merged)


def stabilize_issue_ids(
    current: tuple[Issue, ...],
    previous: tuple[Issue, ...],
) -> tuple[Issue, ...]:
    """Keep issue identity stable when wording or CAF placement changes."""

    previous_by_id = {issue.id: issue for issue in previous}
    unmatched = {issue.id: issue for issue in previous}
    stabilized = []
    for issue in current:
        if issue.id.startswith("DET-"):
            stabilized.append(issue)
            unmatched.pop(issue.id, None)
            continue
        if issue.id in previous_by_id:
            unmatched.pop(issue.id, None)
            stabilized.append(issue)
            continue
        candidate = _best_match(issue, tuple(unmatched.values()))
        if candidate is not None:
            unmatched.pop(candidate.id, None)
            stabilized.append(replace(issue, id=candidate.id))
            continue
        stabilized.append(replace(issue, id=_deterministic_id(issue)))
    return tuple(stabilized)


def _best_match(issue: Issue, candidates: tuple[Issue, ...]) -> Issue | None:
    issue_tokens = _tokens(issue)
    best: tuple[float, Issue] | None = None
    for candidate in candidates:
        if candidate.artifact_type is not issue.artifact_type:
            continue
        candidate_tokens = _tokens(candidate)
        union = issue_tokens | candidate_tokens
        score = len(issue_tokens & candidate_tokens) / len(union) if union else 0
        if set(issue.evidence_refs) & set(candidate.evidence_refs):
            score += 0.15
        if best is None or score > best[0]:
            best = (score, candidate)
    return best[1] if best is not None and best[0] >= 0.38 else None


def _tokens(issue: Issue) -> set[str]:
    # Identity follows the diagnosed weakness, not shared remediation boilerplate.
    text = f"{issue.title} {issue.why}".casefold()
    return {
        token.rstrip("s")
        for token in re.findall(r"[a-z0-9]+", text)
        if len(token) > 2 and token not in _STOP_WORDS
    }


def _same_root_cause(left: Issue, right: Issue) -> bool:
    left_tokens = _tokens(left)
    right_tokens = _tokens(right)
    union = left_tokens | right_tokens
    similarity = len(left_tokens & right_tokens) / len(union) if union else 0
    left_title = _text_tokens(left.title)
    right_title = _text_tokens(right.title)
    title_union = left_title | right_title
    title_similarity = (
        len(left_title & right_title) / len(title_union) if title_union else 0
    )
    title_sequence = SequenceMatcher(
        None,
        _normalized_title(left.title),
        _normalized_title(right.title),
    ).ratio()
    shared_evidence = bool(set(left.evidence_refs) & set(right.evidence_refs))
    left_concrete = _concrete_tokens(left)
    right_concrete = _concrete_tokens(right)
    shared_concrete = left_concrete & right_concrete
    concrete_equivalent = bool(shared_concrete) and (
        left_concrete == right_concrete
        or (
            min(len(left_concrete), len(right_concrete)) >= 2
            and abs(len(left_concrete) - len(right_concrete)) <= 1
            and (
                left_concrete.issubset(right_concrete)
                or right_concrete.issubset(left_concrete)
            )
        )
    )
    shared_semantic = {
        token
        for token in left_tokens & right_tokens
        if not token.isdigit()
    }

    if left.artifact_type is right.artifact_type:
        return (
            title_similarity >= 0.68
            or title_sequence >= 0.57
            or similarity >= 0.7
            or (shared_evidence and title_similarity >= 0.48)
        )
    return (
        shared_evidence
        and (title_similarity >= 0.7 or title_sequence >= 0.62)
    ) or (
        concrete_equivalent
        and len(shared_semantic) >= 2
        and similarity >= 0.24
    )


def _text_tokens(text: str) -> set[str]:
    return {
        token.rstrip("s")
        for token in re.findall(r"[a-z0-9]+", text.casefold())
        if len(token) > 2 and token not in _STOP_WORDS
    }


def _normalized_title(value: str) -> str:
    return " ".join(
        token.rstrip("s")
        for token in re.findall(r"[a-z0-9]+", value.casefold())
        if len(token) > 2 and token not in _STOP_WORDS
    )


def _concrete_tokens(issue: Issue) -> set[str]:
    text = " ".join((issue.title, issue.why)).casefold().replace(",", "")
    return set(
        re.findall(
            r"(?<![a-z])(?:\d+(?:\.\d+)?%?|£\d+(?:\.\d+)?[mk]?)(?![a-z])",
            text,
        )
    )


def _deterministic_id(issue: Issue) -> str:
    normalized = " ".join(sorted(_tokens(issue)))
    digest = hashlib.sha256(
        f"{issue.artifact_type.value}|{normalized}".encode()
    ).hexdigest()[:12].upper()
    return f"ISS-{issue.artifact_type.value.upper()}-{digest}"
