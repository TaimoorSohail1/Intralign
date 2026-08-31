from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

from oslo_api.analysis.load_bearing import deterministic_finding_tags
from oslo_api.analysis.models import ArtifactType, EvidenceFragment, Issue


@dataclass(frozen=True, slots=True)
class CompletenessRule:
    id: str
    artifact_type: ArtifactType
    dimension: str
    severity: str
    trigger_patterns: tuple[str, ...]
    satisfaction_patterns: tuple[str, ...]
    title: str
    why: str
    recommendation: str
    clarification: str


_RULES = (
    CompletenessRule(
        id="regulated-output-verification",
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Clarity",
        severity="Moderate",
        trigger_patterns=(
            r"\blicen[cs]e conditions?\b|\bregulatory requirements?\b",
            r"\b(?:subtitl\w*|audio description|signed programming|accessibility)\b",
        ),
        satisfaction_patterns=(
            r"\b(?:test|verification|verify|acceptance|validate|validation)"
            r".{0,180}\b(?:subtitl\w*|audio description|signed programming|"
            r"accessibility)\b",
            r"\b(?:subtitl\w*|audio description|signed programming|accessibility)"
            r".{0,180}\b(?:test|verification|verify|acceptance|validate|validation)\b",
        ),
        title="Regulated output requirements have no verification route",
        why=(
            "The plan states regulated output obligations but does not define a "
            "test stage or acceptance criterion that verifies those outputs."
        ),
        recommendation=(
            "Add named verification activities, measurable acceptance thresholds, "
            "evidence owners, and the release decision that consumes the results."
        ),
        clarification=(
            "Which test and acceptance evidence proves each regulated output "
            "requirement before release?"
        ),
    ),
    CompletenessRule(
        id="availability-disaster-recovery",
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Clarity",
        severity="Moderate",
        trigger_patterns=(
            r"\b(?:availability|uptime)\b.{0,80}"
            r"(?:%|percent\b|service level\b|\bsla\b)|"
            r"(?:%|percent\b|service level\b|\bsla\b).{0,80}"
            r"\b(?:availability|uptime)\b",
        ),
        satisfaction_patterns=(
            r"\b(?:disaster recovery|recovery time objective|recovery point objective|"
            r"\brto\b|\brpo\b|backup|restore|failover|continuity plan)\b",
        ),
        title="Availability target has no disaster recovery requirement",
        why=(
            "The plan defines a measurable production availability target but "
            "does not define disaster recovery, recovery time, recovery point, "
            "backup, restore, or failover controls that support it."
        ),
        recommendation=(
            "Add approved RTO and RPO targets, backup and restore requirements, "
            "failover responsibilities, verification tests, and release evidence."
        ),
        clarification=(
            "Which disaster recovery, RTO, RPO, backup, restore and failover "
            "requirements support the availability target?"
        ),
    ),
    CompletenessRule(
        id="card-payment-security",
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Clarity",
        severity="Moderate",
        trigger_patterns=(
            r"\b(?:card\s+pre[- ]?authori[sz]ation|payment\s+capture|"
            r"card\s+payment|payment\s+gateway|tokeni[sz]ed\s+card)\b",
        ),
        satisfaction_patterns=(
            r"\b(?:pci(?:\s+dss)?|payment security|cardholder data|"
            r"card data security|payment security test|payment penetration test)\b",
        ),
        title="Card payment processing has no payment security requirement",
        why=(
            "The plan processes or exchanges card-payment information but does "
            "not define a PCI DSS or equivalent payment-security requirement "
            "and verification route."
        ),
        recommendation=(
            "Add the applicable PCI DSS scope, cardholder-data controls, "
            "accountable owner, security verification, evidence and release gate."
        ),
        clarification=(
            "Which PCI DSS or equivalent payment-security controls and tests "
            "govern card processing?"
        ),
    ),
    CompletenessRule(
        id="personal-data-protection",
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Clarity",
        severity="Moderate",
        trigger_patterns=(
            r"\b(?:guest|customer|citizen|patient|employee|student)\s+profiles?\b|"
            r"\bpersonal data\b|\bidentity\b.{0,80}\bcontact\b.{0,80}\bhistory\b",
        ),
        satisfaction_patterns=(
            r"\b(?:data protection|privacy requirement|privacy control|"
            r"data protection impact assessment|\bdpia\b|\bgdpr\b|"
            r"lawful basis|data subject access|right to erasure)\b",
        ),
        title="Personal-data processing has no data protection requirement",
        why=(
            "The plan stores material personal profile and history data but "
            "does not define a data-protection or privacy requirement covering "
            "lawful use, rights, controls and assurance."
        ),
        recommendation=(
            "Add applicable data-protection requirements, lawful basis, "
            "retention and disposal, data-subject rights, access controls, "
            "impact assessment, verification and accountable ownership."
        ),
        clarification=(
            "Which approved data-protection requirements and assessment govern "
            "the personal information in scope?"
        ),
    ),
    CompletenessRule(
        id="interactive-accessibility",
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Clarity",
        severity="Low",
        trigger_patterns=(
            r"\b(?:guest|customer|citizen|patient|student|staff|employee)"
            r"[- ]facing\b.{0,100}\b(?:interface|application|app|portal|"
            r"website|workflow)\b|"
            r"\b(?:interface|application|app|portal|website)\b.{0,100}"
            r"\b(?:guest|customer|citizen|patient|student|staff|employee)"
            r"[- ]facing\b|"
            r"\bbrand\s+website(?:\s+booking\s+engine)?\b",
        ),
        satisfaction_patterns=(
            r"\b(?:accessibility requirement|accessibility standard|"
            r"\bwcag\b|assistive technolog|screen reader|keyboard navigation|"
            r"accessible interface|accessibility test)\b",
        ),
        title="User-facing interfaces have no accessibility requirement",
        why=(
            "The plan includes user-facing interfaces or workflows but does not "
            "define an accessibility standard, acceptance criterion or "
            "verification route."
        ),
        recommendation=(
            "Add the applicable accessibility standard, measurable acceptance "
            "criteria, supported assistive technologies, accountable owner and "
            "release verification."
        ),
        clarification=(
            "Which accessibility standard and acceptance tests govern the "
            "user-facing interfaces?"
        ),
    ),
    CompletenessRule(
        id="operational-records-data-protection",
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Clarity",
        severity="Moderate",
        trigger_patterns=(
            r"\b(?:electronic batch records?|operator records?|workforce records?|"
            r"production user records?)\b",
        ),
        satisfaction_patterns=(
            r"\b(?:data protection|privacy requirement|processor terms?|"
            r"data processing agreement|\bdpa\b|sub-processor|security schedule|"
            r"retention and disposal)\b",
        ),
        title="Operational records have no data protection requirement",
        why=(
            "The system creates electronic batch or other operational records "
            "attributable to people but the "
            "plan defines no data-protection, processor, retention or security terms."
        ),
        recommendation=(
            "Add the processing purpose, roles, lawful basis, retention, access, "
            "security, sub-processor, incident and deletion requirements."
        ),
        clarification=(
            "Which approved data-protection and processor controls govern the "
            "operational records?"
        ),
    ),
    CompletenessRule(
        id="hosted-service-exit",
        artifact_type=ArtifactType.CONTEXT,
        dimension="Clarity",
        severity="Low",
        trigger_patterns=(
            r"\b(?:hosted managed service|hosting and managed service|"
            r"hosted enterprise (?:system|service)|software licences?)\b",
            r"\b(?:termination|contract exit|service expiry)\b",
        ),
        satisfaction_patterns=(
            r"\b(?:exit plan|exit provisions?|transition assistance|source-code escrow|"
            r"data return|data export|portable format|service handover|"
            r"migration assistance)\b",
        ),
        title="Hosted enterprise service has no exit or transition control",
        why=(
            "The plan depends on hosted software but defines no usable-data return, "
            "transition support, escrow or continuity obligation at exit."
        ),
        recommendation=(
            "Add data export format and timing, transition assistance, access "
            "continuity, deletion evidence and any required escrow arrangements."
        ),
        clarification="What protects continuity and data portability when the service ends?",
    ),
    CompletenessRule(
        id="system-level-acceptance",
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Clarity",
        severity="Low",
        trigger_patterns=(
            r"\b(?:acceptance applies to each deliverable|deliverable is deemed accepted|"
            r"acceptance of each deliverable)\b",
            r"\b(?:go-live|cutover|production release|project closure)\b",
        ),
        satisfaction_patterns=(
            r"\b(?:system-level acceptance criteria|go-live criteria|"
            r"operational acceptance threshold|project completion acceptance criteria|"
            r"end-to-end acceptance criteria)\b",
        ),
        title="Deliverable acceptance has no system-level success gate",
        why=(
            "Individual deliverables can be accepted, but nothing proves the combined "
            "system is ready, operationally successful or fit for go-live."
        ),
        recommendation=(
            "Add end-to-end system acceptance and go-live criteria with measures, "
            "evidence, owners, approvers and failure actions."
        ),
        clarification="Which evidence proves the whole system is acceptable for go-live?",
    ),
)


def audit_completeness(
    evidence: tuple[EvidenceFragment, ...],
    *,
    rules: tuple[CompletenessRule, ...] = _RULES,
) -> tuple[Issue, ...]:
    flattened = tuple(
        (
            fragment,
            re.sub(
                r"\s+",
                " ",
                fragment.content.replace("\u00a0", " "),
            ).strip(),
        )
        for fragment in evidence
        if fragment.content.strip()
    )
    combined = " ".join(text for _, text in flattened)
    issues: list[Issue] = []
    for rule in rules:
        trigger_refs = tuple(
            fragment.reference
            for fragment, text in flattened
            if any(re.search(pattern, text, re.I) for pattern in rule.trigger_patterns)
        )
        if not trigger_refs:
            continue
        if not all(re.search(pattern, combined, re.I) for pattern in rule.trigger_patterns):
            continue
        if any(
            re.search(pattern, text, re.I | re.S)
            for _, text in flattened
            for pattern in rule.satisfaction_patterns
        ):
            continue
        references = tuple(dict.fromkeys(trigger_refs))
        digest = hashlib.sha256(
            f"{rule.id}|{'|'.join(references)}".encode()
        ).hexdigest()[:12].upper()
        finding = deterministic_finding_tags(
            dimension=rule.dimension,
            title=rule.title,
            recommendation=rule.recommendation,
        )
        issues.append(
            Issue(
                id=f"DET-{rule.artifact_type.value.upper()}-MISSING-{digest}",
                artifact_type=rule.artifact_type,
                dimension=rule.dimension,
                severity=rule.severity,
                title=rule.title,
                why=rule.why,
                recommendation=rule.recommendation,
                evidence_refs=references,
                clarification=rule.clarification,
                finding_type=finding.finding_type,
                finding_basis=finding.basis.value,
                structural_target=finding.structural_target.value,
            )
        )
    return tuple(issues)
