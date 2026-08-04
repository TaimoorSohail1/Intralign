from __future__ import annotations

import calendar
import hashlib
import re
from datetime import date

from oslo_api.analysis.models import (
    ClaimKind,
    ClaimRelation,
    EvidenceClaim,
    EvidenceFragment,
    EvidenceGraph,
)

_MONTHS = {
    name.casefold(): number
    for number in range(1, 13)
    for name in (calendar.month_name[number], calendar.month_abbr[number])
}
_MONTH_PATTERN = "|".join(
    sorted((re.escape(name) for name in _MONTHS), key=len, reverse=True)
)
_SAME_MONTH_RANGE_RE = re.compile(
    rf"\b(?P<start>[0-3]?\d)\s*(?:-|–|—|to)\s*(?P<finish>[0-3]?\d)"
    rf"\s+(?P<month>{_MONTH_PATTERN})\s+(?P<year>\d{{4}})\b",
    re.IGNORECASE,
)
_FULL_RANGE_RE = re.compile(
    rf"\b(?:from\s+)?(?P<start>[0-3]?\d)\s+(?P<start_month>{_MONTH_PATTERN})"
    rf"\s+(?P<start_year>\d{{4}})\s+(?:to|until|through|[-–—])\s+"
    rf"(?P<finish>[0-3]?\d)\s+(?P<finish_month>{_MONTH_PATTERN})"
    rf"\s+(?P<finish_year>\d{{4}})\b",
    re.IGNORECASE,
)
_MONTH_RANGE_RE = re.compile(
    rf"\b(?:from\s+)?(?P<start_month>{_MONTH_PATTERN})\s+"
    rf"(?P<start_year>\d{{4}})\s+(?:to|until|through|[-â€“â€”])\s+"
    rf"(?P<finish_month>{_MONTH_PATTERN})\s+(?P<finish_year>\d{{4}})\b",
    re.IGNORECASE,
)
_SINGLE_DATE_RE = re.compile(
    rf"\b(?P<day>[0-3]?\d)\s+(?P<month>{_MONTH_PATTERN})"
    rf"\s+(?P<year>\d{{4}})\b",
    re.IGNORECASE,
)
_CONSTRAINT_RE = re.compile(
    r"\b(?:rights window|freeze|blackout|no (?:platform|production|system) change|"
    r"change is not permitted|changes? (?:are )?prohibited|continuity.{0,40}mandatory|"
    r"must remain live|must not change)\b",
    re.IGNORECASE,
)
_ACTIVITY_RE = re.compile(
    r"\b(?:cutover|migration|go[- ]?live|deployment|release|commissioning)\b",
    re.IGNORECASE,
)
_VERIFICATION_RE = re.compile(
    r"\b(?:failover|resilience|operational readiness|acceptance|verification)"
    r".{0,80}\b(?:test|testing|assessment)\b|"
    r"\b(?:test|testing|assessment).{0,80}"
    r"(?:failover|resilience|operational readiness|acceptance|verification)\b",
    re.IGNORECASE,
)
_CONTINGENCY_RATE_RE = re.compile(
    r"(?:\b(?P<prefix>\d+(?:\.\d+)?)\s*%\s+contingency\b|"
    r"\bcontingency(?: rate| allowance)?\s*(?:of|:|=)?\s*"
    r"(?P<suffix>\d+(?:\.\d+)?)\s*%)",
    re.IGNORECASE,
)
_LABELLED_MONEY_RE = re.compile(
    r"\b(?P<label>base cost|base sub[- ]?total|sub[- ]?total|contingency|"
    r"total approved cost|approved total|total)\s*[:=-]?\s*"
    r"[£Ł$€]?\s*(?P<amount>\d[\d,]*(?:\.\d+)?)\s*(?P<scale>[mk])?\b",
    re.IGNORECASE,
)
_RATE_RE = re.compile(
    r"\b(?P<value>\d[\d,]*(?:\.\d+)?)\s*"
    r"(?P<unit>hours?|records?|items?|units?|channels?|devices?)\s*"
    r"(?:/|per)\s*(?P<period>week|day|month)\b",
    re.IGNORECASE,
)
_VOLUME_RE = re.compile(
    r"\b(?P<value>\d[\d,]*(?:\.\d+)?)\s*"
    r"(?P<unit>hours?|records?|items?|units?|channels?|devices?)\b",
    re.IGNORECASE,
)
_MEASUREMENT_RE = re.compile(
    r"\b(?P<value>\d[\d,]*(?:\.\d+)?)\s*"
    r"(?P<unit>cubic\s+metres?|square\s+metres?|metres?|kilometres?|"
    r"millimetres?|tonnes?|kilograms?|litres?)\b",
    re.IGNORECASE,
)
_OVERBOOKING_ALLOW_RE = re.compile(
    r"\b(?:controlled\s+)?overbooking\b.{0,100}?"
    r"(?:up\s+to\s+)?(?P<value>\d+(?:\.\d+)?)\s*%",
    re.IGNORECASE,
)
_NO_INVENTORY_CONFIRM_RE = re.compile(
    r"\b(?:shall|must)\s+not\s+permit\b.{0,100}?\breservation\b.{0,100}?"
    r"\bconfirm(?:ed|ation)?\b.{0,100}?\bno\s+inventory\b.{0,40}?\bavailable\b",
    re.IGNORECASE,
)
_CENTRAL_RATE_CONTROL_RE = re.compile(
    r"\brates?\b.{0,100}?\b(?:set|maintained|managed)\s+centrally\b"
    r".{0,140}?\b(?:shall|must)\s+not\s+be\s+amended\b"
    r".{0,80}?\bproperty\s+level\b",
    re.IGNORECASE,
)
_PROPERTY_DISCOUNT_RE = re.compile(
    r"\b(?:front\s+desk|property)\b.{0,100}?"
    r"\b(?:manager|staff|user)s?\b.{0,120}?\b(?:apply|amend|override)\b"
    r".{0,100}?\b(?:discretionary\s+)?discount\b.{0,80}?"
    r"(?:up\s+to\s+)?(?P<value>\d+(?:\.\d+)?)\s*%",
    re.IGNORECASE,
)
_STOP_WORDS = {
    "and",
    "are",
    "between",
    "change",
    "channel",
    "contractual",
    "cutover",
    "during",
    "final",
    "from",
    "into",
    "live",
    "mandatory",
    "migration",
    "november",
    "operating",
    "permitted",
    "platform",
    "project",
    "rights",
    "schedule",
    "the",
    "this",
    "transmission",
    "window",
    "with",
}


def build_evidence_graph(
    evidence: tuple[EvidenceFragment, ...],
) -> EvidenceGraph:
    claims = tuple(
        claim
        for fragment in evidence
        for claim in _claims_from_fragment(fragment)
    )
    relations: list[ClaimRelation] = []
    constraints = tuple(
        claim
        for claim in claims
        if claim.predicate == "constrains" and claim.kind is ClaimKind.DATE_RANGE
    )
    activities = tuple(
        claim
        for claim in claims
        if claim.predicate == "scheduled_for"
        and claim.kind is ClaimKind.DATE_RANGE
    )
    for constraint in constraints:
        for activity in activities:
            if not _date_ranges_overlap(constraint.value, activity.value):
                continue
            if not _same_subject(constraint.subject, activity.subject):
                continue
            relations.append(
                ClaimRelation(
                    source_claim_id=activity.id,
                    target_claim_id=constraint.id,
                    relation_type="violates",
                    evidence_refs=tuple(
                        dict.fromkeys((constraint.evidence_ref, activity.evidence_ref))
                    ),
                )
            )
    overbooking_claims = tuple(
        claim for claim in claims if claim.predicate == "allows_overbooking"
    )
    inventory_guards = tuple(
        claim
        for claim in claims
        if claim.predicate == "forbids_confirmation_without_inventory"
    )
    for overbooking in overbooking_claims:
        for inventory_guard in inventory_guards:
            relations.append(
                ClaimRelation(
                    source_claim_id=overbooking.id,
                    target_claim_id=inventory_guard.id,
                    relation_type="contradicts",
                    evidence_refs=tuple(
                        dict.fromkeys(
                            (overbooking.evidence_ref, inventory_guard.evidence_ref)
                        )
                    ),
                )
            )
    central_rate_controls = tuple(
        claim for claim in claims if claim.predicate == "forbids_property_rate_change"
    )
    property_rate_overrides = tuple(
        claim for claim in claims if claim.predicate == "allows_property_discount"
    )
    for central_control in central_rate_controls:
        for property_override in property_rate_overrides:
            relations.append(
                ClaimRelation(
                    source_claim_id=property_override.id,
                    target_claim_id=central_control.id,
                    relation_type="contradicts",
                    evidence_refs=tuple(
                        dict.fromkeys(
                            (
                                central_control.evidence_ref,
                                property_override.evidence_ref,
                            )
                        )
                    ),
                )
            )
    measurements = tuple(
        claim for claim in claims if claim.predicate == "measured_value"
    )
    for index, left in enumerate(measurements):
        for right in measurements[index + 1 :]:
            if (
                left.evidence_ref == right.evidence_ref
                or left.unit != right.unit
                or left.numeric_value == right.numeric_value
                or not _measurement_subjects_match(left.subject, right.subject)
            ):
                continue
            relations.append(
                ClaimRelation(
                    source_claim_id=left.id,
                    target_claim_id=right.id,
                    relation_type="contradicts_measurement",
                    evidence_refs=tuple(
                        dict.fromkeys((left.evidence_ref, right.evidence_ref))
                    ),
                )
            )
    return EvidenceGraph(claims=claims, relations=tuple(relations))


def _claims_from_fragment(fragment: EvidenceFragment) -> tuple[EvidenceClaim, ...]:
    text = re.sub(r"\s+", " ", fragment.content.replace("\u00a0", " ")).strip()
    ranges: list[tuple[date, date, str]] = []
    occupied: list[tuple[int, int]] = []
    range_predicates: list[str] = []
    for match in _FULL_RANGE_RE.finditer(text):
        start = _as_date(
            match.group("start"),
            match.group("start_month"),
            match.group("start_year"),
        )
        finish = _as_date(
            match.group("finish"),
            match.group("finish_month"),
            match.group("finish_year"),
        )
        ranges.append((start, finish, match.group(0)))
        occupied.append(match.span())
        range_predicates.append(
            _range_predicate(text, match.start(), match.end())
        )
    for match in _SAME_MONTH_RANGE_RE.finditer(text):
        if any(match.start() < finish and match.end() > start for start, finish in occupied):
            continue
        start = _as_date(match.group("start"), match.group("month"), match.group("year"))
        finish = _as_date(
            match.group("finish"),
            match.group("month"),
            match.group("year"),
        )
        ranges.append((start, finish, match.group(0)))
        occupied.append(match.span())
        range_predicates.append(
            _range_predicate(text, match.start(), match.end())
        )
    for match in _MONTH_RANGE_RE.finditer(text):
        if any(match.start() < finish and match.end() > start for start, finish in occupied):
            continue
        start_month = _MONTHS[match.group("start_month").casefold()]
        finish_month = _MONTHS[match.group("finish_month").casefold()]
        start_year = int(match.group("start_year"))
        finish_year = int(match.group("finish_year"))
        start = date(start_year, start_month, 1)
        finish = date(
            finish_year,
            finish_month,
            calendar.monthrange(finish_year, finish_month)[1],
        )
        ranges.append((start, finish, match.group(0)))
        occupied.append(match.span())
        range_predicates.append(
            _range_predicate(text, match.start(), match.end())
        )

    claims = [
        EvidenceClaim(
            id=_claim_id(
                fragment.reference,
                ClaimKind.DATE_RANGE,
                f"{start.isoformat()}/{finish.isoformat()}",
                index,
            ),
            kind=ClaimKind.DATE_RANGE,
            subject=_subject(text, matched),
            predicate=range_predicates[index],
            value=f"{start.isoformat()}/{finish.isoformat()}",
            raw_text=text,
            evidence_ref=fragment.reference,
            source_name=fragment.source_name,
            location=fragment.location,
            unit="date_range",
        )
        for index, (start, finish, matched) in enumerate(ranges)
    ]
    next_index = len(claims)

    for match in _OVERBOOKING_ALLOW_RE.finditer(text):
        rate = float(match.group("value"))
        claims.append(
            EvidenceClaim(
                id=_claim_id(
                    fragment.reference,
                    ClaimKind.REQUIREMENT,
                    f"reservation_inventory:allows_overbooking:{rate:g}",
                    next_index,
                ),
                kind=ClaimKind.REQUIREMENT,
                subject="reservation inventory",
                predicate="allows_overbooking",
                value=f"{rate:g}",
                raw_text=text,
                evidence_ref=fragment.reference,
                source_name=fragment.source_name,
                location=fragment.location,
                unit="percent",
                numeric_value=rate,
            )
        )
        next_index += 1

    if _NO_INVENTORY_CONFIRM_RE.search(text):
        claims.append(
            EvidenceClaim(
                id=_claim_id(
                    fragment.reference,
                    ClaimKind.REQUIREMENT,
                    "reservation_inventory:forbids_confirmation_without_inventory",
                    next_index,
                ),
                kind=ClaimKind.REQUIREMENT,
                subject="reservation inventory",
                predicate="forbids_confirmation_without_inventory",
                value="no confirmation without available inventory",
                raw_text=text,
                evidence_ref=fragment.reference,
                source_name=fragment.source_name,
                location=fragment.location,
            )
        )
        next_index += 1

    if _CENTRAL_RATE_CONTROL_RE.search(text):
        claims.append(
            EvidenceClaim(
                id=_claim_id(
                    fragment.reference,
                    ClaimKind.REQUIREMENT,
                    "rate_control:forbids_property_rate_change",
                    next_index,
                ),
                kind=ClaimKind.REQUIREMENT,
                subject="rate control",
                predicate="forbids_property_rate_change",
                value="central authority only",
                raw_text=text,
                evidence_ref=fragment.reference,
                source_name=fragment.source_name,
                location=fragment.location,
            )
        )
        next_index += 1

    for match in _PROPERTY_DISCOUNT_RE.finditer(text):
        rate = float(match.group("value"))
        claims.append(
            EvidenceClaim(
                id=_claim_id(
                    fragment.reference,
                    ClaimKind.REQUIREMENT,
                    f"rate_control:allows_property_discount:{rate:g}",
                    next_index,
                ),
                kind=ClaimKind.REQUIREMENT,
                subject="rate control",
                predicate="allows_property_discount",
                value=f"{rate:g}",
                raw_text=text,
                evidence_ref=fragment.reference,
                source_name=fragment.source_name,
                location=fragment.location,
                unit="percent",
                numeric_value=rate,
            )
        )
        next_index += 1

    for match in _SINGLE_DATE_RE.finditer(text):
        if any(match.start() < finish and match.end() > start for start, finish in occupied):
            continue
        value = _as_date(match.group("day"), match.group("month"), match.group("year"))
        context = text[max(0, match.start() - 120) : match.end() + 120]
        local_predicate = _predicate_around(text, match.start(), match.end())
        date_predicate = (
            "expires_on"
            if re.search(r"\b(?:contract|agreement|licen[cs]e).{0,80}expir", context, re.I)
            else "project_end"
            if re.search(
                r"\b(?:project|programme)\s+(?:closure|completion)\b|"
                r"\b(?:project|programme|migration).{0,100}"
                r"(?:through|until|ends?|finish|complete|closure)",
                context,
                re.I,
            )
            else local_predicate
        )
        claims.append(
            EvidenceClaim(
                id=_claim_id(
                    fragment.reference,
                    ClaimKind.DATE,
                    value.isoformat(),
                    next_index,
                ),
                kind=ClaimKind.DATE,
                subject=_subject(text, match.group(0)),
                predicate=date_predicate,
                value=value.isoformat(),
                raw_text=text,
                evidence_ref=fragment.reference,
                source_name=fragment.source_name,
                location=fragment.location,
                unit="date",
            )
        )
        next_index += 1

    for match in _CONTINGENCY_RATE_RE.finditer(text):
        rate = float(match.group("prefix") or match.group("suffix"))
        claims.append(
            EvidenceClaim(
                id=_claim_id(
                    fragment.reference,
                    ClaimKind.PERCENTAGE,
                    str(rate),
                    next_index,
                ),
                kind=ClaimKind.PERCENTAGE,
                subject="contingency",
                predicate="contingency_rate",
                value=f"{rate:g}",
                raw_text=text,
                evidence_ref=fragment.reference,
                source_name=fragment.source_name,
                location=fragment.location,
                unit="percent",
                numeric_value=rate,
            )
        )
        next_index += 1

    for match in _LABELLED_MONEY_RE.finditer(text):
        label = re.sub(r"[-\s]+", "_", match.group("label").casefold())
        amount = _money_value(match.group("amount"), match.group("scale"))
        claims.append(
            EvidenceClaim(
                id=_claim_id(
                    fragment.reference,
                    ClaimKind.MONEY,
                    f"{label}:{amount:g}",
                    next_index,
                ),
                kind=ClaimKind.MONEY,
                subject=match.group("label"),
                predicate={
                    "base_cost": "base_cost",
                    "base_subtotal": "base_cost",
                    "base_sub_total": "base_cost",
                    "subtotal": "base_cost",
                    "sub_total": "base_cost",
                    "contingency": "contingency_amount",
                    "total_approved_cost": "approved_total",
                    "approved_total": "approved_total",
                    "total": "approved_total",
                }[label],
                value=f"{amount:g}",
                raw_text=text,
                evidence_ref=fragment.reference,
                source_name=fragment.source_name,
                location=fragment.location,
                unit="currency_minor",
                numeric_value=amount,
            )
        )
        next_index += 1

    rate_spans: list[tuple[int, int]] = []
    for match in _RATE_RE.finditer(text):
        amount = float(match.group("value").replace(",", ""))
        unit = _singular(match.group("unit"))
        period = match.group("period").casefold()
        claims.append(
            EvidenceClaim(
                id=_claim_id(
                    fragment.reference,
                    ClaimKind.QUANTITY,
                    f"{amount:g}:{unit}:per_{period}",
                    next_index,
                ),
                kind=ClaimKind.QUANTITY,
                subject=_subject(text, match.group(0)),
                predicate="delivery_rate",
                value=f"{amount:g}",
                raw_text=text,
                evidence_ref=fragment.reference,
                source_name=fragment.source_name,
                location=fragment.location,
                unit=f"{unit}/per_{period}",
                numeric_value=amount,
            )
        )
        rate_spans.append(match.span())
        next_index += 1

    for match in _VOLUME_RE.finditer(text):
        if any(match.start() < finish and match.end() > start for start, finish in rate_spans):
            continue
        context = text[max(0, match.start() - 100) : match.end() + 80]
        if not re.search(
            r"\b(?:archive|volume|total|contains?|inventory|dataset|backlog)\b",
            context,
            re.I,
        ):
            continue
        amount = float(match.group("value").replace(",", ""))
        unit = _singular(match.group("unit"))
        claims.append(
            EvidenceClaim(
                id=_claim_id(
                    fragment.reference,
                    ClaimKind.QUANTITY,
                    f"{amount:g}:{unit}:total",
                    next_index,
                ),
                kind=ClaimKind.QUANTITY,
                subject=_subject(text, match.group(0)),
                predicate="total_volume",
                value=f"{amount:g}",
                raw_text=text,
                evidence_ref=fragment.reference,
                source_name=fragment.source_name,
                location=fragment.location,
                unit=unit,
                numeric_value=amount,
            )
        )
        next_index += 1

    for match in _MEASUREMENT_RE.finditer(text):
        amount = float(match.group("value").replace(",", ""))
        unit = _canonical_measurement_unit(match.group("unit"))
        subject = _measurement_subject(text, match.start())
        if not subject:
            continue
        claims.append(
            EvidenceClaim(
                id=_claim_id(
                    fragment.reference,
                    ClaimKind.QUANTITY,
                    f"{subject}:{amount:g}:{unit}",
                    next_index,
                ),
                kind=ClaimKind.QUANTITY,
                subject=subject,
                predicate="measured_value",
                value=f"{amount:g}",
                raw_text=text,
                evidence_ref=fragment.reference,
                source_name=fragment.source_name,
                location=fragment.location,
                unit=unit,
                numeric_value=amount,
            )
        )
        next_index += 1

    claims.append(
        EvidenceClaim(
            id=_claim_id(
                fragment.reference,
                ClaimKind.TEXT,
                hashlib.sha256(text.encode()).hexdigest(),
                next_index,
            ),
            kind=ClaimKind.TEXT,
            subject=fragment.source_name or "source evidence",
            predicate="source_text",
            value=text,
            raw_text=text,
            evidence_ref=fragment.reference,
            source_name=fragment.source_name,
            location=fragment.location,
        )
    )

    return tuple(claims)


def _as_date(day: str, month: str, year: str) -> date:
    return date(int(year), _MONTHS[month.casefold()], int(day))


def _claim_id(
    reference: str,
    kind: ClaimKind,
    value: str,
    index: int,
) -> str:
    digest = hashlib.sha256(
        f"{reference}|{kind.value}|{value}|{index}".encode()
    ).hexdigest()[:16]
    return f"claim:{digest}"


def _money_value(amount: str, scale: str | None) -> float:
    value = float(amount.replace(",", ""))
    if scale and scale.casefold() == "m":
        return value * 1_000_000
    if scale and scale.casefold() == "k":
        return value * 1_000
    return value


def _singular(unit: str) -> str:
    normalized = unit.casefold()
    return normalized[:-1] if normalized.endswith("s") else normalized


def _predicate_around(text: str, start: int, finish: int) -> str:
    context = text[max(0, start - 100) : min(len(text), finish + 100)]
    if _CONSTRAINT_RE.search(context):
        return "constrains"
    if _VERIFICATION_RE.search(context):
        return "verification_window"
    if _ACTIVITY_RE.search(context):
        return "scheduled_for"
    return "states"


def _range_predicate(text: str, start: int, finish: int) -> str:
    local = _predicate_around(text, start, finish)
    if local != "states":
        return local
    if re.search(
        r"\b(?:migration|deployment|release)\s+schedule\b.{0,180}"
        r"\b(?:cutover|go[- ]?live)\s+date\b",
        text,
        re.I,
    ):
        return "scheduled_for"
    return local


def _subject(text: str, matched: str) -> str:
    prefix = text.partition(matched)[0].strip(" :;.-")
    return prefix[-180:] if prefix else text[:180]


def _canonical_measurement_unit(value: str) -> str:
    normalized = re.sub(r"\s+", "_", value.casefold()).rstrip("s")
    return {
        "metre": "metre",
        "kilometre": "kilometre",
        "millimetre": "millimetre",
        "cubic_metre": "cubic_metre",
        "square_metre": "square_metre",
        "tonne": "tonne",
        "kilogram": "kilogram",
        "litre": "litre",
    }[normalized]


def _measurement_subject(text: str, start: int) -> str:
    prefix = text[max(0, start - 140) : start]
    tokens = [
        token
        for token in re.findall(r"[a-z][a-z0-9-]*", prefix.casefold())
        if token
        not in {
            "agreed",
            "allowed",
            "approved",
            "at",
            "be",
            "brief",
            "by",
            "from",
            "in",
            "increased",
            "metre",
            "metres",
            "of",
            "re-measured",
            "remeasured",
            "reduced",
            "report",
            "stated",
            "the",
            "to",
            "was",
        }
    ]
    aliases = {"quantity": "volume"}
    normalized = [aliases.get(token, token) for token in tokens]
    return " ".join(normalized[-6:])


def _measurement_subjects_match(left: str, right: str) -> bool:
    left_tokens = _meaningful_tokens(left)
    right_tokens = _meaningful_tokens(right)
    shared = left_tokens & right_tokens
    return len(shared) >= 2 and (
        len(shared) / min(len(left_tokens), len(right_tokens)) >= 0.5
    )


def _date_ranges_overlap(left: str, right: str) -> bool:
    left_start, left_finish = (date.fromisoformat(item) for item in left.split("/", 1))
    right_start, right_finish = (
        date.fromisoformat(item) for item in right.split("/", 1)
    )
    return left_start <= right_finish and right_start <= left_finish


def _same_subject(left: str, right: str) -> bool:
    left_tokens = _meaningful_tokens(left)
    right_tokens = _meaningful_tokens(right)
    if left_tokens & right_tokens:
        return True
    return bool(
        re.search(
            r"\bno (?:platform|production|system) change\b",
            left,
            re.IGNORECASE,
        )
    )


def _meaningful_tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z][a-z0-9-]+", value.casefold())
        if len(token) > 2 and token not in _STOP_WORDS and not token.isdigit()
    }
