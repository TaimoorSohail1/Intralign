import hashlib
import re
from dataclasses import replace

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
    "is",
    "it",
    "no",
    "not",
    "of",
    "on",
    "or",
    "the",
    "to",
    "what",
    "which",
}


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
    text = " ".join(
        (
            issue.title,
            issue.why,
            issue.recommendation,
            issue.clarification or "",
        )
    ).casefold()
    return {
        token.rstrip("s")
        for token in re.findall(r"[a-z0-9]+", text)
        if len(token) > 2 and token not in _STOP_WORDS
    }


def _deterministic_id(issue: Issue) -> str:
    normalized = " ".join(sorted(_tokens(issue)))
    digest = hashlib.sha256(
        f"{issue.artifact_type.value}|{normalized}".encode()
    ).hexdigest()[:12].upper()
    return f"ISS-{issue.artifact_type.value.upper()}-{digest}"
