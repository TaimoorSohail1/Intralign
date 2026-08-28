import json
import re
from dataclasses import asdict, is_dataclass, replace
from datetime import datetime
from hashlib import sha256
from time import monotonic, sleep
from urllib.parse import quote
from uuid import UUID, uuid4

from sqlalchemy import Connection, Engine, text

from oslo_api.analysis.history import append_history_event
from oslo_api.analysis.integrity import Integrity, OutcomeCheckpoint, Pillar
from oslo_api.analysis.models import (
    AnalysisEvent,
    AnalysisPassKind,
    AnalysisPhase,
    AnalysisRun,
    AnalysisRunRequest,
    AnalysisRunStatus,
    Artifact,
    ArtifactAssumption,
    ArtifactConflict,
    ArtifactSection,
    ArtifactType,
    Assessment,
    AssessmentSnapshot,
    ClaimKind,
    ClaimProvenance,
    ClaimRelation,
    EvidenceCitation,
    EvidenceClaim,
    EvidenceFragment,
    HarnessCallMetadata,
    Issue,
    Perception,
    ReanalysisTrigger,
    ReliabilityBasis,
    RunKind,
)
from oslo_api.analysis.provenance import build_project_provenance


def _stable_payload_hash(payload: object) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return sha256(canonical.encode("utf-8")).hexdigest()


def evidence_reference(
    *,
    document_id: UUID,
    ordinal: int,
    locator: dict[str, object],
) -> str:
    """Create a stable evidence URI without losing source-format location."""

    prefix = f"document:{document_id}"
    kind = locator.get("kind")
    if kind == "docx_section":
        location = f"section:{quote(str(locator.get('section', 'Document')), safe='')}"
    elif kind == "pptx_slide":
        location = f"slide:{locator.get('slide', 1)}"
    elif kind == "xlsx_range":
        sheet = quote(str(locator.get("sheet", "Sheet")), safe="")
        cell_range = quote(str(locator.get("cell_range", "A1")), safe="")
        location = f"sheet:{sheet}:range:{cell_range}"
    else:
        location = f"page:{locator.get('page', 1)}"
    return f"{prefix}:{location}:fragment:{ordinal}"


def evidence_location(locator: dict[str, object]) -> str:
    kind = locator.get("kind")
    if kind == "docx_section":
        return f"Section: {locator.get('section', 'Document')}"
    if kind == "pptx_slide":
        return f"Slide {locator.get('slide', 1)}"
    if kind == "xlsx_range":
        return f"Sheet: {locator.get('sheet', 'Sheet')} · {locator.get('cell_range', 'A1')}"
    return f"Page {locator.get('page', 1)}"


def _json_default(value):
    if isinstance(value, (UUID, datetime)):
        return str(value)
    if hasattr(value, "value"):
        return value.value
    raise TypeError(f"Unsupported JSON value: {type(value)!r}")


def _state_json(state: dict[str, object]) -> dict[str, object]:
    def encode(value):
        if is_dataclass(value):
            return asdict(value)
        if hasattr(value, "value"):
            return value.value
        if isinstance(value, (UUID, datetime)):
            return str(value)
        raise TypeError(f"Unsupported checkpoint value: {type(value)!r}")

    return json.loads(json.dumps(state, default=encode, sort_keys=True))


def _restore_state(payload: dict[str, object]) -> dict[str, object]:
    restored: dict[str, object] = {}
    harness_calls = payload.get("harness_calls")
    if isinstance(harness_calls, dict):
        restored["harness_calls"] = harness_calls
    perception_data = payload.get("perception")
    if isinstance(perception_data, dict):
        restored["perception"] = Perception(
            facts=tuple(perception_data.get("facts", [])),
            claims=tuple(perception_data.get("claims", [])),
            gaps=tuple(perception_data.get("gaps", [])),
            evidence_refs=tuple(perception_data.get("evidence_refs", [])),
            evidence=tuple(
                EvidenceFragment(
                    reference=item["reference"],
                    content=item["content"],
                    source_name=item.get("source_name"),
                    location=item.get("location"),
                )
                for item in perception_data.get("evidence", [])
            ),
            structured_claims=tuple(
                EvidenceClaim(
                    id=item["id"],
                    kind=ClaimKind(item["kind"]),
                    subject=item["subject"],
                    predicate=item["predicate"],
                    value=item["value"],
                    raw_text=item["raw_text"],
                    evidence_ref=item["evidence_ref"],
                    source_name=item.get("source_name"),
                    location=item.get("location"),
                    unit=item.get("unit"),
                    numeric_value=item.get("numeric_value"),
                    provenance=ClaimProvenance(item.get("provenance", "source_grounded")),
                )
                for item in perception_data.get("structured_claims", [])
            ),
            claim_relations=tuple(
                ClaimRelation(
                    source_claim_id=item["source_claim_id"],
                    target_claim_id=item["target_claim_id"],
                    relation_type=item["relation_type"],
                    evidence_refs=tuple(item.get("evidence_refs", [])),
                )
                for item in perception_data.get("claim_relations", [])
            ),
        )
    artifact_data = payload.get("artifacts")
    if isinstance(artifact_data, list):
        restored["artifacts"] = tuple(_artifact_from_dict(item) for item in artifact_data)
    assessment_data = payload.get("assessment")
    if isinstance(assessment_data, dict):
        restored["assessment"] = _assessment_from_dict(assessment_data)
    return restored


def _artifact_from_dict(data: dict) -> Artifact:
    return Artifact(
        artifact_type=ArtifactType(data["artifact_type"]),
        title=data["title"],
        summary=data["summary"],
        reliability=data["reliability"],
        evidence_refs=tuple(data["evidence_refs"]),
        basis=data.get("basis", "derived"),
        sections=tuple(
            ArtifactSection(
                heading=section["heading"],
                body=section.get("body", ""),
                bullets=tuple(section.get("bullets", [])),
                columns=tuple(section.get("columns", [])),
                rows=tuple(tuple(row) for row in section.get("rows", [])),
                evidence_refs=tuple(section.get("evidence_refs", [])),
                row_evidence_refs=tuple(
                    tuple(references) for references in section.get("row_evidence_refs", [])
                ),
                row_states=tuple(section.get("row_states", [])),
            )
            for section in data.get("sections", [])
        ),
        assumptions=tuple(
            ArtifactAssumption(
                id=assumption["id"],
                statement=assumption["statement"],
                state=assumption.get("state", "inferred"),
                load_bearing=bool(assumption.get("load_bearing", False)),
                evidence_refs=tuple(assumption.get("evidence_refs", [])),
            )
            for assumption in data.get("assumptions", [])
        ),
        conflicts=tuple(
            ArtifactConflict(
                id=conflict["id"],
                field=conflict["field"],
                values=tuple(conflict.get("values", [])),
                evidence_refs=tuple(conflict.get("evidence_refs", [])),
            )
            for conflict in data.get("conflicts", [])
        ),
        project_title=data.get("project_title"),
    )


def _issue_from_dict(data: dict) -> Issue:
    return Issue(
        id=data["id"],
        artifact_type=ArtifactType(data["artifact_type"]),
        dimension=data["dimension"],
        severity=data["severity"],
        title=data["title"],
        why=data["why"],
        recommendation=data["recommendation"],
        evidence_refs=tuple(data["evidence_refs"]),
        clarification=data.get("clarification"),
        status=data.get("status", "open"),
        dimensions=tuple(data.get("dimensions", [])),
        finding_type=data.get("finding_type", ""),
        section=data.get("section", ""),
        recommendation_from_oslo=data.get("recommendation_from_oslo", True),
        load_bearing=data.get("load_bearing", True),
        exposure_rank=float(data.get("exposure_rank", 0)),
        finding_basis=data.get("finding_basis", ""),
        structural_target=data.get("structural_target", ""),
        primary_act=data.get("primary_act", ""),
        also_offered=tuple(data.get("also_offered", [])),
        classification_state=data.get("classification_state", "unclassified"),
        sensitivity=(
            float(data["sensitivity"])
            if data.get("sensitivity") is not None
            else None
        ),
        sensitivity_trace=data.get("sensitivity_trace"),
        sensitivity_state=data.get("sensitivity_state", "unavailable"),
        unassessed=bool(data.get("unassessed", False)),
    )


def _assessment_from_dict(data: dict) -> Assessment:
    from oslo_api.analysis.load_bearing import (
        PlanDependencyGraph,
        PlanEdge,
        PlanNode,
        SensitivityCandidate,
        StructuralTarget,
    )

    basis = data.get("reliability_basis", {})
    graph_data = data.get("dependency_graph")
    dependency_graph = None
    if graph_data:
        dependency_graph = PlanDependencyGraph(
            nodes=tuple(PlanNode(**node) for node in graph_data.get("nodes", [])),
            edges=tuple(PlanEdge(**edge) for edge in graph_data.get("edges", [])),
        )
    return Assessment(
        confidence_index=data["confidence_index"],
        confidence_band=data["confidence_band"],
        reliability=data["reliability"],
        clarity=data["clarity"],
        alignment=data["alignment"],
        feasibility=data["feasibility"],
        issues=tuple(_issue_from_dict(issue) for issue in data["issues"]),
        understanding_stage=data.get("understanding_stage", "orientation"),
        reliability_basis=ReliabilityBasis(
            coverage=basis.get("coverage", "Low"),
            evidence=basis.get("evidence", "Low"),
            assessability=basis.get("assessability", "Low"),
        ),
        confidence_direction=data.get("confidence_direction", "unchanged"),
        limiting_dimension=data.get("limiting_dimension", "feasibility"),
        false_confidence=data.get("false_confidence", False),
        confidence_explanation=data.get("confidence_explanation", ""),
        resolved_issue_count=data.get("resolved_issue_count", 0),
        confirmed_dependency_count=data.get("confirmed_dependency_count", 0),
        outcome_checkpoints=tuple(
            OutcomeCheckpoint(
                id=item["id"],
                workstream=item["workstream"],
                leading_indicator=item["leading_indicator"],
                timing=item["timing"],
                lever=item["lever"],
                registered=bool(item["registered"]),
                evidence_refs=tuple(item.get("evidence_refs", [])),
            )
            for item in data.get("outcome_checkpoints", [])
        ),
        integrity=_integrity_from_dict(data.get("integrity")),
        dependency_graph=dependency_graph,
        sensitivity_candidates=tuple(
            SensitivityCandidate(
                id=item["id"],
                node_id=item["node_id"],
                structural_target=StructuralTarget(item["structural_target"]),
                favorable_integrity=float(item["favorable_integrity"]),
                adverse_integrity=float(item["adverse_integrity"]),
                runway_factor=float(item["runway_factor"]),
                edge_key=(
                    (str(item["edge_key"][0]), str(item["edge_key"][1]))
                    if isinstance(item.get("edge_key"), (list, tuple))
                    and len(item["edge_key"]) == 2
                    else None
                ),
                stakes=(
                    float(item["stakes"])
                    if item.get("stakes") is not None
                    else None
                ),
            )
            for item in data.get("sensitivity_candidates", [])
        ),
    )


def _integrity_from_dict(data: dict | None) -> Integrity | None:
    if data is None:
        return None
    pillars = tuple(
        Pillar(
            key=item["key"],
            band=item["band"],
            basis=float(item["basis"]),
            why=tuple(item.get("why", [])),
        )
        for item in data["decomposition"]
    )
    return Integrity(
        level=data["level"],
        limiting_pillar=data["limiting_pillar"],
        decomposition=pillars,  # type: ignore[arg-type]
        posture=data.get("posture", "moment-in-time"),
        tracking=data.get("tracking", "pending-execution"),
        complete=bool(data.get("complete", True)),
        sound_claim_blocked=bool(data.get("sound_claim_blocked", False)),
        under_review_regions=tuple(data.get("under_review_regions", [])),
    )


def _snapshot_dict(snapshot: AssessmentSnapshot) -> dict:
    payload = json.loads(json.dumps(asdict(snapshot), default=_json_default))
    payload["provenance"] = build_project_provenance(
        artifacts=snapshot.artifacts,
        issues=snapshot.assessment.issues,
    )
    return payload


def _public_snapshot_summary(value: str) -> str:
    if not value.startswith("USER_ARTIFACT_EDIT"):
        return value
    match = re.search(
        r"(At the (?:orientation|expanded|validated) stage,.*)$",
        value,
        re.DOTALL,
    )
    return (
        match.group(1)
        if match
        else "The retained project read was refreshed from governed evidence."
    )


def _snapshot_from_dict(data: dict) -> AssessmentSnapshot:
    return AssessmentSnapshot(
        id=UUID(data["id"]),
        analysis_run_id=UUID(data["analysis_run_id"]),
        workspace_id=UUID(data["workspace_id"]),
        project_id=UUID(data["project_id"]),
        state=data["state"],
        summary=_public_snapshot_summary(data["summary"]),
        artifacts=tuple(_artifact_from_dict(item) for item in data["artifacts"]),
        assessment=_assessment_from_dict(data["assessment"]),
        published_at=datetime.fromisoformat(data["published_at"]),
        evidence_citations=tuple(
            EvidenceCitation(
                reference=item["reference"],
                source_name=item["source_name"],
                location=item["location"],
                excerpt=item["excerpt"],
            )
            for item in data.get("evidence_citations", [])
        ),
        project_title=data.get("project_title"),
        source_document_count=int(data.get("source_document_count", 0)),
    )


def _active_issue_keys(issues: tuple[Issue, ...]) -> set[str]:
    return {issue.id for issue in issues if issue.status != "resolved"}


def _issue_observation_dimension(issue: Issue) -> str | None:
    """Keep model-gap observations unclassified at the persistence boundary."""

    return issue.dimension or None


def _primary_outcome_title(artifacts: tuple[Artifact, ...]) -> str | None:
    """Use the evidence-derived intent statement, not extractor progress copy."""

    intent = next(
        (artifact for artifact in artifacts if artifact.artifact_type is ArtifactType.INTENT),
        None,
    )
    if intent is None:
        return None

    preferred_sections = tuple(
        section
        for section in intent.sections
        if re.search(r"executive summary|purpose|outcome|intent", section.heading, re.I)
    )
    candidates: list[str] = []
    for section in preferred_sections:
        candidates.extend((section.body, *section.bullets))
        candidates.extend(
            next((cell for cell in row[1:] if cell.strip()), row[0] if row else "")
            for row in section.rows
        )
    if not candidates:
        candidates.append(intent.summary)

    for candidate in candidates:
        normalized = re.sub(r"\s+", " ", candidate).strip()
        if not normalized:
            continue
        sentence = re.split(r"(?<=[.!?])\s+", normalized, maxsplit=1)[0]
        normalized_sentence = sentence.casefold()
        names_outcome_concept = re.search(
            r"\b(outcome|purpose|objective|goal|benefit|success)\b",
            normalized_sentence,
        )
        says_it_is_missing = re.search(
            r"\b(is|are|was|were) not (yet )?"
            r"(defined|documented|provided|stated|specified|identified|known|confirmed)\b"
            r"|\bno (purpose|objective|outcome|goal|benefit|success)\b",
            normalized_sentence,
        )
        if names_outcome_concept and says_it_is_missing:
            continue
        return sentence if len(sentence) <= 320 else f"{sentence[:317].rstrip()}…"
    return None


class DatabaseAnalysisStore:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def create_run(self, request: AnalysisRunRequest) -> AnalysisRun:
        run_id = uuid4()
        key = request.idempotency_key or str(run_id)
        with self._engine.begin() as connection:
            inserted = connection.execute(
                text(
                    """
                    insert into public.analysis_runs (
                      id, workspace_id, project_id, requested_by, kind, status,
                      description, source_names, source_document_ids, user_evidence,
                      idempotency_key, parent_run_id, consumes_analysis_allowance,
                      pass_kind, reanalysis_trigger, consolidated_event_ids,
                      provisional, auto_retry_count
                    ) values (
                      :id, :workspace_id, :project_id, :requested_by, :kind, 'queued',
                      :description, cast(:source_names as jsonb),
                      cast(:source_document_ids as jsonb), cast(:user_evidence as jsonb),
                      :key, :parent_run_id,
                      :consumes_analysis_allowance, :pass_kind, :reanalysis_trigger,
                      cast(:consolidated_event_ids as jsonb), :provisional,
                      :auto_retry_count
                    )
                    on conflict (workspace_id, idempotency_key) do nothing
                    returning id
                    """
                ),
                {
                    "id": run_id,
                    "workspace_id": request.workspace_id,
                    "project_id": request.project_id,
                    "requested_by": request.requested_by,
                    "kind": request.kind.value,
                    "description": request.description,
                    "source_names": json.dumps(request.source_names),
                    "source_document_ids": json.dumps(
                        [str(document_id) for document_id in request.source_document_ids]
                    ),
                    "user_evidence": json.dumps([asdict(item) for item in request.user_evidence]),
                    "key": key,
                    "parent_run_id": request.parent_run_id,
                    "consumes_analysis_allowance": request.consumes_analysis_allowance,
                    "pass_kind": request.pass_kind.value,
                    "reanalysis_trigger": request.reanalysis_trigger.value,
                    "consolidated_event_ids": json.dumps(
                        [str(event_id) for event_id in request.consolidated_event_ids]
                    ),
                    "provisional": request.provisional,
                    "auto_retry_count": request.auto_retry_count,
                },
            ).scalar_one_or_none()
            actual_id = (
                inserted
                or connection.execute(
                    text(
                        """
                    select id from public.analysis_runs
                    where workspace_id = :workspace_id and idempotency_key = :key
                    """
                    ),
                    {"workspace_id": request.workspace_id, "key": key},
                ).scalar_one()
            )
            if inserted:
                self._append_event(
                    connection,
                    actual_id,
                    "analysis.queued",
                    AnalysisRunStatus.QUEUED,
                )
        run = self.get_run(actual_id)
        if run is None:
            raise RuntimeError("ANALYSIS_RUN_CREATE_FAILED")
        return run

    def get_run(self, run_id: UUID) -> AnalysisRun | None:
        with self._engine.connect() as connection:
            row = (
                connection.execute(
                    text(
                        """
                        select id, workspace_id, project_id, requested_by, kind, status,
                               description, source_names, source_document_ids, user_evidence,
                               idempotency_key, parent_run_id,
                               consumes_analysis_allowance, pass_kind,
                               reanalysis_trigger, consolidated_event_ids,
                               provisional, auto_retry_count,
                               current_phase, error_code, created_at, updated_at
                        from public.analysis_runs where id = :run_id
                        """
                    ),
                    {"run_id": run_id},
                )
                .mappings()
                .one_or_none()
            )
            if row is None:
                return None
            completed = connection.execute(
                text(
                    """
                    select phase from public.analysis_run_events
                    where analysis_run_id = :run_id
                      and event_type = 'analysis.phase_completed'
                    order by sequence_no
                    """
                ),
                {"run_id": run_id},
            ).scalars()
            checkpoint = (
                connection.execute(
                    text(
                        """
                        select state_json from public.analysis_checkpoints
                        where analysis_run_id = :run_id
                        order by created_at desc limit 1
                        """
                    ),
                    {"run_id": run_id},
                )
                .mappings()
                .one_or_none()
            )
            snapshot_row = (
                connection.execute(
                    text(
                        """
                        select snapshot_json from public.assessment_snapshots
                        where analysis_run_id = :run_id
                        """
                    ),
                    {"run_id": run_id},
                )
                .mappings()
                .one_or_none()
            )
        request = AnalysisRunRequest(
            workspace_id=row["workspace_id"],
            project_id=row["project_id"],
            requested_by=row["requested_by"],
            kind=RunKind(row["kind"]),
            description=row["description"],
            source_names=tuple(row["source_names"]),
            source_document_ids=tuple(
                UUID(document_id) for document_id in row["source_document_ids"]
            ),
            user_evidence=tuple(
                EvidenceFragment(
                    reference=item["reference"],
                    content=item["content"],
                    source_name=item.get("source_name"),
                    location=item.get("location"),
                )
                for item in row["user_evidence"]
            ),
            idempotency_key=row["idempotency_key"],
            parent_run_id=row["parent_run_id"],
            consumes_analysis_allowance=bool(row["consumes_analysis_allowance"]),
            pass_kind=AnalysisPassKind(row["pass_kind"]),
            reanalysis_trigger=ReanalysisTrigger(row["reanalysis_trigger"]),
            consolidated_event_ids=tuple(
                UUID(event_id) for event_id in row["consolidated_event_ids"]
            ),
            provisional=bool(row["provisional"]),
            auto_retry_count=int(row["auto_retry_count"]),
        )
        return AnalysisRun(
            id=row["id"],
            request=request,
            status=AnalysisRunStatus(row["status"]),
            current_phase=AnalysisPhase(row["current_phase"]) if row["current_phase"] else None,
            completed_phases=[AnalysisPhase(phase) for phase in completed if phase],
            checkpoint_state=_restore_state(checkpoint["state_json"]) if checkpoint else {},
            error_code=row["error_code"],
            snapshot=_snapshot_from_dict(snapshot_row["snapshot_json"]) if snapshot_row else None,
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def merge_queued_run(
        self,
        run_id: UUID,
        *,
        evidence: tuple[EvidenceFragment, ...],
        event_ids: tuple[UUID, ...],
    ) -> AnalysisRun:
        with self._engine.begin() as connection:
            updated = connection.execute(
                text(
                    """
                    update public.analysis_runs
                    set user_evidence = user_evidence || cast(:evidence as jsonb),
                        consolidated_event_ids = (
                          select coalesce(jsonb_agg(distinct item), '[]'::jsonb)
                          from jsonb_array_elements(
                            consolidated_event_ids || cast(:event_ids as jsonb)
                          ) item
                        ),
                        updated_at = now()
                    where id = :run_id and status = 'queued'
                    """
                ),
                {
                    "run_id": run_id,
                    "evidence": json.dumps([asdict(item) for item in evidence]),
                    "event_ids": json.dumps([str(event_id) for event_id in event_ids]),
                },
            )
            if updated.rowcount != 1:
                raise ValueError("Only a queued analysis run can accept another change")
            self._append_event(
                connection,
                run_id,
                "analysis.batch_extended",
                AnalysisRunStatus.QUEUED,
            )
        run = self.get_run(run_id)
        if run is None:  # pragma: no cover - guarded by the update above
            raise RuntimeError("ANALYSIS_RUN_NOT_FOUND_AFTER_BATCH_MERGE")
        return run

    def withdraw_queued_event(
        self,
        run_id: UUID,
        *,
        event_id: UUID,
        evidence_references: tuple[str, ...],
    ) -> AnalysisRun:
        with self._engine.begin() as connection:
            updated = connection.execute(
                text(
                    """
                    update public.analysis_runs
                    set user_evidence = (
                          select coalesce(jsonb_agg(item), '[]'::jsonb)
                          from jsonb_array_elements(user_evidence) item
                          where not (item->>'reference' = any(:references))
                        ),
                        consolidated_event_ids = (
                          select coalesce(jsonb_agg(item), '[]'::jsonb)
                          from jsonb_array_elements(consolidated_event_ids) item
                          where item #>> '{}' <> :event_id
                        ),
                        updated_at = now()
                    where id = :run_id and status = 'queued'
                    """
                ),
                {
                    "run_id": run_id,
                    "event_id": str(event_id),
                    "references": list(evidence_references),
                },
            )
            if updated.rowcount != 1:
                raise ValueError("Only a queued analysis run can withdraw a pending change")
            self._append_event(
                connection,
                run_id,
                "analysis.pending_change_withdrawn",
                AnalysisRunStatus.QUEUED,
            )
        run = self.get_run(run_id)
        if run is None:  # pragma: no cover - guarded by the update above
            raise RuntimeError("ANALYSIS_RUN_NOT_FOUND_AFTER_PENDING_WITHDRAWAL")
        return run

    def latest_run_for_project(
        self,
        project_id: UUID,
        kind: RunKind,
    ) -> AnalysisRun | None:
        with self._engine.connect() as connection:
            run_id = connection.execute(
                text(
                    """
                    select id
                    from public.analysis_runs
                    where project_id = :project_id and kind = :kind
                    order by created_at desc, id desc
                    limit 1
                    """
                ),
                {"project_id": project_id, "kind": kind.value},
            ).scalar_one_or_none()
        return self.get_run(run_id) if run_id else None

    def evidence_for(self, request: AnalysisRunRequest) -> tuple[EvidenceFragment, ...]:
        if not request.source_document_ids:
            return ()
        with self._engine.connect() as connection:
            rows = (
                connection.execute(
                    text(
                        """
                        select fragment.source_document_id, fragment.ordinal,
                               fragment.content, fragment.locator,
                               document.file_name
                        from public.source_fragments fragment
                        join public.source_documents document
                          on document.id = fragment.source_document_id
                         and document.workspace_id = fragment.workspace_id
                        where fragment.workspace_id = :workspace_id
                          and fragment.project_id = :project_id
                          and fragment.source_document_id = any(:document_ids)
                        order by fragment.source_document_id, fragment.ordinal
                        """
                    ),
                    {
                        "workspace_id": request.workspace_id,
                        "project_id": request.project_id,
                        "document_ids": list(request.source_document_ids),
                    },
                )
                .mappings()
                .all()
            )
        return tuple(
            EvidenceFragment(
                reference=evidence_reference(
                    document_id=row["source_document_id"],
                    ordinal=row["ordinal"],
                    locator=row["locator"],
                ),
                content=row["content"],
                source_name=row["file_name"],
                location=evidence_location(row["locator"]),
            )
            for row in rows
        )

    def completed_artifacts(self, run_id: UUID) -> dict[ArtifactType, Artifact]:
        with self._engine.connect() as connection:
            rows = (
                connection.execute(
                    text(
                        """
                        select artifact_type, output_json
                        from public.analysis_artifact_jobs
                        where analysis_run_id = :run_id
                          and status = 'completed'
                          and output_json is not null
                        """
                    ),
                    {"run_id": run_id},
                )
                .mappings()
                .all()
            )
        return {
            ArtifactType(row["artifact_type"]): _artifact_from_dict(row["output_json"])
            for row in rows
        }

    def start_artifact_job(self, run_id: UUID, artifact_type: ArtifactType) -> None:
        with self._engine.begin() as connection:
            context = (
                connection.execute(
                    text(
                        """
                        select workspace_id, project_id
                        from public.analysis_runs
                        where id = :run_id
                        """
                    ),
                    {"run_id": run_id},
                )
                .mappings()
                .one()
            )
            connection.execute(
                text(
                    """
                    insert into public.analysis_artifact_jobs (
                      workspace_id, project_id, analysis_run_id, artifact_type,
                      status, attempt_count, lease_owner, lease_expires_at,
                      heartbeat_at, started_at
                    ) values (
                      :workspace_id, :project_id, :run_id, :artifact_type,
                      'running', 1, cast(:run_id as text), now() + interval '2 minutes',
                      now(), now()
                    )
                    on conflict (analysis_run_id, artifact_type) do update
                    set status = 'running',
                        attempt_count = public.analysis_artifact_jobs.attempt_count + 1,
                        safe_error_code = null,
                        retryable = null,
                        lease_owner = cast(:run_id as text),
                        lease_expires_at = now() + interval '2 minutes',
                        heartbeat_at = now(),
                        started_at = now(),
                        completed_at = null,
                        updated_at = now()
                    """
                ),
                {
                    "workspace_id": context["workspace_id"],
                    "project_id": context["project_id"],
                    "run_id": run_id,
                    "artifact_type": artifact_type.value,
                },
            )
            self._append_event(
                connection,
                run_id,
                "analysis.artifact_started",
                self._run_status(connection, run_id),
                AnalysisPhase.CONSTRUCT_ARTIFACTS,
                {"artifact_type": artifact_type.value},
            )

    def complete_artifact_job(
        self,
        run_id: UUID,
        artifact: Artifact,
        metadata: HarnessCallMetadata | None = None,
    ) -> None:
        values = asdict(metadata) if metadata is not None else {}
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.analysis_artifact_jobs
                    set status = 'completed',
                        output_json = cast(:output_json as jsonb),
                        safe_error_code = null,
                        retryable = null,
                        lease_owner = null,
                        lease_expires_at = null,
                        heartbeat_at = now(),
                        provider = :provider,
                        model_id = :model_id,
                        prompt_version = :prompt_version,
                        provider_response_id = :provider_response_id,
                        input_tokens = :input_tokens,
                        output_tokens = :output_tokens,
                        duration_ms = :duration_ms,
                        execution_mode = :execution_mode,
                        fallback_reason = :fallback_reason,
                        completed_at = now(),
                        updated_at = now()
                    where analysis_run_id = :run_id
                      and artifact_type = :artifact_type
                    """
                ),
                {
                    "run_id": run_id,
                    "artifact_type": artifact.artifact_type.value,
                    "output_json": json.dumps(asdict(artifact), default=_json_default),
                    "provider": values.get("provider"),
                    "model_id": values.get("model"),
                    "prompt_version": values.get("prompt_version"),
                    "provider_response_id": values.get("response_id"),
                    "input_tokens": values.get("input_tokens"),
                    "output_tokens": values.get("output_tokens"),
                    "duration_ms": values.get("duration_ms"),
                    "execution_mode": values.get("mode"),
                    "fallback_reason": values.get("fallback_reason"),
                },
            )
            self._append_event(
                connection,
                run_id,
                "analysis.artifact_completed",
                self._run_status(connection, run_id),
                AnalysisPhase.CONSTRUCT_ARTIFACTS,
                {"artifact_type": artifact.artifact_type.value},
            )

    def fail_artifact_job(
        self,
        run_id: UUID,
        artifact_type: ArtifactType,
        *,
        error_code: str,
        retryable: bool,
    ) -> None:
        safe_code = error_code[:120]
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.analysis_artifact_jobs
                    set status = 'failed',
                        safe_error_code = :error_code,
                        retryable = :retryable,
                        lease_owner = null,
                        lease_expires_at = null,
                        heartbeat_at = now(),
                        completed_at = now(),
                        updated_at = now()
                    where analysis_run_id = :run_id
                      and artifact_type = :artifact_type
                    """
                ),
                {
                    "run_id": run_id,
                    "artifact_type": artifact_type.value,
                    "error_code": safe_code,
                    "retryable": retryable,
                },
            )
            self._append_event(
                connection,
                run_id,
                "analysis.artifact_failed",
                self._run_status(connection, run_id),
                AnalysisPhase.CONSTRUCT_ARTIFACTS,
                {
                    "artifact_type": artifact_type.value,
                    "code": safe_code,
                    "retryable": retryable,
                },
            )

    def start_run(self, run_id: UUID) -> None:
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.analysis_runs
                    set status = 'running', started_at = coalesce(started_at, now()),
                        error_code = null, updated_at = now()
                    where id = :run_id and status <> 'completed'
                    """
                ),
                {"run_id": run_id},
            )
            self._append_event(
                connection,
                run_id,
                "analysis.started",
                AnalysisRunStatus.RUNNING,
            )

    def queue_run(self, run_id: UUID) -> None:
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.analysis_runs
                    set status = 'queued', error_code = null, completed_at = null,
                        updated_at = now()
                    where id = :run_id and status <> 'completed'
                    """
                ),
                {"run_id": run_id},
            )
            self._append_event(
                connection,
                run_id,
                "analysis.retry_queued",
                AnalysisRunStatus.QUEUED,
            )

    def queue_auto_retry(self, run_id: UUID) -> AnalysisRun:
        with self._engine.begin() as connection:
            updated = connection.execute(
                text(
                    """
                    update public.analysis_runs
                    set status = 'queued', error_code = null, completed_at = null,
                        auto_retry_count = 1, updated_at = now()
                    where id = :run_id and status = 'failed'
                      and auto_retry_count = 0
                    """
                ),
                {"run_id": run_id},
            )
            if updated.rowcount != 1:
                raise ValueError("The transient automatic retry is not available")
            self._append_event(
                connection,
                run_id,
                "analysis.auto_retry_queued",
                AnalysisRunStatus.QUEUED,
            )
        run = self.get_run(run_id)
        if run is None:  # pragma: no cover - guarded by the update above
            raise RuntimeError("ANALYSIS_RUN_NOT_FOUND_AFTER_AUTO_RETRY")
        return run

    def start_phase(self, run_id: UUID, phase: AnalysisPhase) -> None:
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.analysis_runs
                    set current_phase = :phase, updated_at = now()
                    where id = :run_id
                    """
                ),
                {"run_id": run_id, "phase": phase.value},
            )
            attempt = connection.execute(
                text(
                    """
                    select coalesce(max(attempt_no), 0) + 1
                    from public.analysis_node_attempts
                    where analysis_run_id = :run_id and phase = :phase
                    """
                ),
                {"run_id": run_id, "phase": phase.value},
            ).scalar_one()
            workspace_id = self._workspace_id(connection, run_id)
            connection.execute(
                text(
                    """
                    insert into public.analysis_node_attempts (
                      workspace_id, analysis_run_id, phase, attempt_no, status
                    ) values (:workspace_id, :run_id, :phase, :attempt, 'running')
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "run_id": run_id,
                    "phase": phase.value,
                    "attempt": attempt,
                },
            )
            self._append_event(
                connection,
                run_id,
                "analysis.phase_started",
                self._run_status(connection, run_id),
                phase,
            )

    def complete_phase(
        self,
        run_id: UUID,
        phase: AnalysisPhase,
        checkpoint_state: dict[str, object] | None = None,
    ) -> None:
        state = _state_json(checkpoint_state or {})
        state_text = json.dumps(state, sort_keys=True, separators=(",", ":"))
        harness_calls = state.get("harness_calls", {})
        call_metadata = harness_calls.get(phase.value) if isinstance(harness_calls, dict) else None
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.analysis_node_attempts
                    set status = 'completed', completed_at = now(),
                        provider = :provider,
                        model_id = :model_id,
                        prompt_version = :prompt_version,
                        provider_response_id = :provider_response_id,
                        input_tokens = :input_tokens,
                        output_tokens = :output_tokens,
                        duration_ms = :duration_ms,
                        execution_mode = :execution_mode,
                        fallback_reason = :fallback_reason
                    where id = (
                      select id from public.analysis_node_attempts
                      where analysis_run_id = :run_id and phase = :phase
                      order by attempt_no desc limit 1
                    )
                    """
                ),
                {
                    "run_id": run_id,
                    "phase": phase.value,
                    "provider": (
                        call_metadata.get("provider") if isinstance(call_metadata, dict) else None
                    ),
                    "model_id": (
                        call_metadata.get("model") if isinstance(call_metadata, dict) else None
                    ),
                    "prompt_version": (
                        call_metadata.get("prompt_version")
                        if isinstance(call_metadata, dict)
                        else None
                    ),
                    "provider_response_id": (
                        call_metadata.get("response_id")
                        if isinstance(call_metadata, dict)
                        else None
                    ),
                    "input_tokens": (
                        call_metadata.get("input_tokens")
                        if isinstance(call_metadata, dict)
                        else None
                    ),
                    "output_tokens": (
                        call_metadata.get("output_tokens")
                        if isinstance(call_metadata, dict)
                        else None
                    ),
                    "duration_ms": (
                        call_metadata.get("duration_ms")
                        if isinstance(call_metadata, dict)
                        else None
                    ),
                    "execution_mode": (
                        call_metadata.get("mode") if isinstance(call_metadata, dict) else None
                    ),
                    "fallback_reason": (
                        call_metadata.get("fallback_reason")
                        if isinstance(call_metadata, dict)
                        else None
                    ),
                },
            )
            if isinstance(call_metadata, dict):
                connection.execute(
                    text(
                        """
                        update public.analysis_runs
                        set prompt_versions = prompt_versions ||
                              jsonb_build_object(
                                cast(:phase as text),
                                cast(:prompt_version as text)
                              ),
                            model_versions = model_versions ||
                              jsonb_build_object(
                                cast(:phase as text),
                                cast(:model_id as text)
                              ),
                            updated_at = now()
                        where id = :run_id
                        """
                    ),
                    {
                        "run_id": run_id,
                        "phase": phase.value,
                        "prompt_version": call_metadata.get("prompt_version"),
                        "model_id": call_metadata.get("model"),
                    },
                )
            workspace_id = self._workspace_id(connection, run_id)
            completed = connection.execute(
                text(
                    """
                    select coalesce(jsonb_agg(phase order by sequence_no), '[]'::jsonb)
                    from public.analysis_run_events
                    where analysis_run_id = :run_id
                      and event_type = 'analysis.phase_completed'
                    """
                ),
                {"run_id": run_id},
            ).scalar_one()
            completed = list(completed) + [phase.value]
            connection.execute(
                text(
                    """
                    insert into public.analysis_checkpoints (
                      workspace_id, analysis_run_id, checkpoint_key, completed_phases,
                      state_json, state_hash, graph_version
                    ) values (
                      :workspace_id, :run_id, :key, cast(:completed as jsonb),
                      cast(:state as jsonb), :state_hash, 'slice2-graph-v1'
                    )
                    on conflict (analysis_run_id, checkpoint_key) do update set
                      completed_phases = excluded.completed_phases,
                      state_json = excluded.state_json,
                      state_hash = excluded.state_hash,
                      created_at = now()
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "run_id": run_id,
                    "key": phase.value,
                    "completed": json.dumps(completed),
                    "state": state_text,
                    "state_hash": sha256(state_text.encode()).hexdigest(),
                },
            )
            self._append_event(
                connection,
                run_id,
                "analysis.phase_completed",
                self._run_status(connection, run_id),
                phase,
            )

    def publish(self, run_id: UUID, snapshot: AssessmentSnapshot) -> None:
        with self._engine.begin() as connection:
            if not snapshot.project_title:
                project_name = connection.execute(
                    text("select name from public.projects where id = :project_id"),
                    {"project_id": snapshot.project_id},
                ).scalar_one_or_none()
                normalized_title = str(project_name or "").strip()
                if normalized_title:
                    snapshot = replace(
                        snapshot,
                        project_title=normalized_title,
                        artifacts=tuple(
                            artifact
                            if artifact.project_title
                            else replace(artifact, project_title=normalized_title)
                            for artifact in snapshot.artifacts
                        ),
                    )
            payload = _snapshot_dict(snapshot)
            run_row = (
                connection.execute(
                    text(
                        """
                        select kind, consumes_analysis_allowance, requested_by
                        from public.analysis_runs
                        where id = :run_id
                        """
                    ),
                    {"run_id": run_id},
                )
                .mappings()
                .one()
            )
            connection.execute(
                text("select pg_advisory_xact_lock(hashtext(cast(:project_id as text)))"),
                {"project_id": snapshot.project_id},
            )
            previous_snapshot_payload = connection.execute(
                text(
                    """
                    select retained.snapshot_json
                    from public.projects project
                    left join public.assessment_snapshots retained
                      on retained.analysis_run_id = project.current_analysis_run_id
                    where project.id = :project_id
                    """
                ),
                {"project_id": snapshot.project_id},
            ).scalar_one_or_none()
            previous_issue_keys = _active_issue_keys(
                _snapshot_from_dict(previous_snapshot_payload).assessment.issues
                if previous_snapshot_payload
                else ()
            )
            connection.execute(
                text(
                    """
                    insert into public.assessment_snapshots (
                      id, workspace_id, project_id, analysis_run_id,
                      snapshot_state, snapshot_json, published_at
                    ) values (
                      :id, :workspace_id, :project_id, :run_id,
                      :state, cast(:snapshot as jsonb), :published_at
                    )
                    on conflict (analysis_run_id) do nothing
                    """
                ),
                {
                    "id": snapshot.id,
                    "workspace_id": snapshot.workspace_id,
                    "project_id": snapshot.project_id,
                    "run_id": run_id,
                    "state": snapshot.state,
                    "snapshot": json.dumps(payload),
                    "published_at": snapshot.published_at,
                },
            )
            primary_outcome = _primary_outcome_title(snapshot.artifacts)
            if primary_outcome is not None:
                connection.execute(
                    text(
                        "update public.project_outcomes set title = :title "
                        "where project_id = :project_id and is_primary "
                        "and provenance = 'inferred'"
                    ),
                    {
                        "project_id": snapshot.project_id,
                        "title": primary_outcome,
                    },
                )
                connection.execute(
                    text(
                        "insert into public.project_outcomes "
                        "(workspace_id, project_id, title, is_primary, provenance, created_by) "
                        "select :workspace_id, :project_id, :title, true, 'inferred', "
                        ":created_by where not exists ("
                        "  select 1 from public.project_outcomes "
                        "  where project_id = :project_id and is_primary"
                        ")"
                    ),
                    {
                        "workspace_id": snapshot.workspace_id,
                        "project_id": snapshot.project_id,
                        "title": primary_outcome,
                        "created_by": run_row["requested_by"],
                    },
                )
            else:
                connection.execute(
                    text(
                        "delete from public.project_outcomes "
                        "where project_id = :project_id and is_primary "
                        "and provenance = 'inferred'"
                    ),
                    {"project_id": snapshot.project_id},
                )
            for artifact in snapshot.artifacts:
                artifact_payload = {
                    "title": artifact.title,
                    "summary": artifact.summary,
                    "reliability": artifact.reliability,
                    "basis": artifact.basis,
                    "evidence_refs": list(artifact.evidence_refs),
                    "content": {"sections": [asdict(section) for section in artifact.sections]},
                    "assumptions": [asdict(assumption) for assumption in artifact.assumptions],
                    "conflicts": [asdict(conflict) for conflict in artifact.conflicts],
                }
                previous_artifact = (
                    connection.execute(
                        text(
                            """
                            select title, summary, reliability, basis, evidence_refs,
                                   content_json, assumptions_json, conflicts_json,
                                   revision
                            from public.artifact_versions
                            where project_id = :project_id
                              and artifact_type = cast(
                                :artifact_type as public.plan_artifact_type
                              )
                            order by revision desc, created_at desc
                            limit 1
                            """
                        ),
                        {
                            "project_id": snapshot.project_id,
                            "artifact_type": artifact.artifact_type.value,
                        },
                    )
                    .mappings()
                    .one_or_none()
                )
                previous_payload = (
                    {
                        "title": previous_artifact["title"],
                        "summary": previous_artifact["summary"],
                        "reliability": previous_artifact["reliability"],
                        "basis": previous_artifact["basis"],
                        "evidence_refs": previous_artifact["evidence_refs"],
                        "content": previous_artifact["content_json"],
                        "assumptions": previous_artifact["assumptions_json"],
                        "conflicts": previous_artifact["conflicts_json"],
                    }
                    if previous_artifact is not None
                    else None
                )
                if previous_artifact is None:
                    next_revision = 1
                elif _stable_payload_hash(previous_payload) == _stable_payload_hash(
                    artifact_payload
                ):
                    next_revision = int(previous_artifact["revision"])
                else:
                    next_revision = int(previous_artifact["revision"]) + 1
                revision = connection.execute(
                    text(
                        """
                        insert into public.artifact_versions (
                          workspace_id, project_id, analysis_run_id, artifact_type,
                          title, summary, reliability, basis, evidence_refs,
                          content_json, assumptions_json, conflicts_json, revision
                        ) values (
                          :workspace_id, :project_id, :run_id, :artifact_type,
                          :title, :summary, :reliability, :basis,
                          cast(:evidence_refs as jsonb), cast(:content as jsonb),
                          cast(:assumptions as jsonb), cast(:conflicts as jsonb), :revision
                        )
                        on conflict (analysis_run_id, artifact_type) do nothing
                        returning revision
                        """
                    ),
                    {
                        "workspace_id": snapshot.workspace_id,
                        "project_id": snapshot.project_id,
                        "run_id": run_id,
                        "artifact_type": artifact.artifact_type.value,
                        "title": artifact_payload["title"],
                        "summary": artifact_payload["summary"],
                        "reliability": artifact_payload["reliability"],
                        "basis": artifact_payload["basis"],
                        "evidence_refs": json.dumps(artifact_payload["evidence_refs"]),
                        "content": json.dumps(artifact_payload["content"]),
                        "assumptions": json.dumps(artifact_payload["assumptions"]),
                        "conflicts": json.dumps(artifact_payload["conflicts"]),
                        "revision": next_revision,
                    },
                ).scalar_one_or_none()
                if revision is None:
                    continue
                draft = (
                    connection.execute(
                        text(
                            """
                            update public.artifact_drafts
                            set source_snapshot_id = :snapshot_id,
                                updated_at = now()
                            where project_id = :project_id
                              and artifact_type = cast(
                                :artifact_type as public.plan_artifact_type
                              )
                            returning id, workspace_id, content_json, version,
                                      provenance, updated_by
                            """
                        ),
                        {
                            "snapshot_id": snapshot.id,
                            "project_id": snapshot.project_id,
                            "artifact_type": artifact.artifact_type.value,
                            "revision": revision,
                        },
                    )
                    .mappings()
                    .one_or_none()
                )
                if draft is not None:
                    connection.execute(
                        text(
                            """
                            insert into public.artifact_draft_versions (
                              workspace_id, project_id, artifact_type,
                              artifact_draft_id, version, content_json,
                              provenance, changed_by, analysis_run_id
                            ) values (
                              :workspace_id, :project_id,
                              cast(:artifact_type as public.plan_artifact_type),
                              :draft_id, :version, cast(:content as jsonb),
                              :provenance, :changed_by, :run_id
                            )
                            on conflict (artifact_draft_id, version) do nothing
                            """
                        ),
                        {
                            "workspace_id": draft["workspace_id"],
                            "project_id": snapshot.project_id,
                            "artifact_type": artifact.artifact_type.value,
                            "draft_id": draft["id"],
                            "version": draft["version"],
                            "content": json.dumps(draft["content_json"]),
                            "provenance": draft["provenance"],
                            "changed_by": draft["updated_by"],
                            "run_id": run_id,
                        },
                    )
            # A model failing to reproduce a finding is not resolution evidence.
            # Existing issue rows therefore keep their lifecycle state unless the
            # governed snapshot explicitly carries a new state for the same stable
            # issue key.
            for issue in snapshot.assessment.issues:
                issue_id = connection.execute(
                    text(
                        """
                        insert into public.issues (
                          workspace_id, project_id, stable_key, current_status
                        ) values (
                          :workspace_id, :project_id, :stable_key, :status
                        )
                        on conflict (project_id, stable_key) do update set
                          updated_at = now()
                        returning id
                        """
                    ),
                    {
                        "workspace_id": snapshot.workspace_id,
                        "project_id": snapshot.project_id,
                        "stable_key": issue.id,
                        "status": issue.status,
                    },
                ).scalar_one()
                connection.execute(
                    text(
                        """
                        insert into public.issue_observations (
                          workspace_id, project_id, issue_id, analysis_run_id,
                          artifact_type, dimension, severity, status,
                          observation_json
                        ) values (
                          :workspace_id, :project_id, :issue_id, :run_id,
                          :artifact_type, :dimension, :severity, :status,
                          cast(:observation as jsonb)
                        )
                        on conflict (analysis_run_id, issue_id) do nothing
                        """
                    ),
                    {
                        "workspace_id": snapshot.workspace_id,
                        "project_id": snapshot.project_id,
                        "issue_id": issue_id,
                        "run_id": run_id,
                        "artifact_type": issue.artifact_type.value,
                        "dimension": _issue_observation_dimension(issue),
                        "severity": issue.severity,
                        "status": issue.status,
                        "observation": json.dumps(
                            {
                                "stable_key": issue.id,
                                "title": issue.title,
                                "why": issue.why,
                                "recommendation": issue.recommendation,
                                "clarification": issue.clarification,
                                "evidence_refs": issue.evidence_refs,
                            }
                        ),
                    },
                )
                connection.execute(
                    text(
                        """
                        insert into public.issue_proposals (
                          workspace_id, project_id, issue_stable_key, stable_key,
                          kind, resolver_key, title, rationale, artifact_type,
                          load_bearing, created_by_run_id
                        ) values (
                          :workspace_id, :project_id, :issue_stable_key,
                          :stable_key, 'build', :resolver_key, :title, :rationale,
                          cast(:artifact_type as public.plan_artifact_type),
                          :load_bearing, :run_id
                        )
                        on conflict (project_id, stable_key) do nothing
                        """
                    ),
                    {
                        "workspace_id": snapshot.workspace_id,
                        "project_id": snapshot.project_id,
                        "issue_stable_key": issue.id,
                        "stable_key": f"build:{issue.id}:primary",
                        "resolver_key": f"{issue.artifact_type.value}:primary",
                        "title": issue.recommendation or f"Address {issue.title}",
                        "rationale": issue.why,
                        "artifact_type": issue.artifact_type.value,
                        "load_bearing": issue.load_bearing,
                        "run_id": run_id,
                    },
                )
            connection.execute(
                text(
                    """
                    update public.analysis_runs
                    set status = 'completed', completed_at = now(), updated_at = now()
                    where id = :run_id
                    """
                ),
                {"run_id": run_id},
            )
            connection.execute(
                text(
                    """
                    update public.projects
                    set current_analysis_run_id = :run_id,
                        status = 'active',
                        name = case
                          when name in ('Project', 'Untitled project')
                            and nullif(trim(cast(:project_title as text)), '') is not null
                          then trim(cast(:project_title as text))
                          else name
                        end,
                        updated_at = now()
                    where id = :project_id
                    """
                ),
                {
                    "run_id": run_id,
                    "project_id": snapshot.project_id,
                    "project_title": snapshot.project_title,
                },
            )
            self._append_event(
                connection,
                run_id,
                "assessment.published",
                AnalysisRunStatus.COMPLETED,
                payload={"snapshot_id": str(snapshot.id), "state": snapshot.state},
            )
            if bool(run_row["consumes_analysis_allowance"]):
                connection.execute(
                    text(
                        """
                        insert into public.workspace_analysis_usage (
                          workspace_id, project_id, analysis_run_id,
                          usage_kind, period_start
                        ) values (
                          :workspace_id, :project_id, :run_id,
                          'user_requested_analysis',
                          date_trunc('month', now())::date
                        )
                        on conflict (analysis_run_id) do nothing
                        """
                    ),
                    {
                        "workspace_id": snapshot.workspace_id,
                        "project_id": snapshot.project_id,
                        "run_id": run_id,
                    },
                )
            run_kind = str(run_row["kind"])
            # History describes the atomically published read, not every issue row
            # retained for lifecycle/audit purposes. Counting retained rows here made
            # History disagree with Overview and Issues after a fresh reanalysis.
            current_issue_keys = _active_issue_keys(snapshot.assessment.issues)
            opened = sorted(current_issue_keys - previous_issue_keys)
            attested_in_run = {
                str(issue_key)
                for issue_key in connection.execute(
                    text(
                        """
                        select distinct on (issue_stable_key) issue_stable_key
                        from public.issue_attestations
                        where analysis_run_id = :run_id
                          and act not in ('flag', 'fix', 'withdraw')
                        order by issue_stable_key, created_at desc
                        """
                    ),
                    {"run_id": run_id},
                ).scalars()
            }
            resolved = sorted((previous_issue_keys - current_issue_keys) | attested_in_run)
            append_history_event(
                connection,
                workspace_id=snapshot.workspace_id,
                project_id=snapshot.project_id,
                analysis_run_id=run_id,
                actor_type="oslo",
                category="analysis",
                event_type=f"analysis.{run_kind}_completed",
                summary=(
                    "Initial Analysis complete"
                    if run_kind == "initial"
                    else "Extended Analysis complete"
                ),
                detail=(
                    "The first evidence-qualified read is available."
                    if run_kind == "initial"
                    else "The deeper evidence read is now the current trusted view."
                ),
                idempotency_key=f"history:analysis-completed:{run_id}",
                payload={
                    "snapshot_id": str(snapshot.id),
                    "confidence_index": snapshot.assessment.confidence_index,
                    "confidence_band": snapshot.assessment.confidence_band,
                    "clarity": snapshot.assessment.clarity,
                    "alignment": snapshot.assessment.alignment,
                    "feasibility": snapshot.assessment.feasibility,
                },
            )
            append_history_event(
                connection,
                workspace_id=snapshot.workspace_id,
                project_id=snapshot.project_id,
                analysis_run_id=run_id,
                actor_type="system",
                category="issues",
                event_type="issues.reconciled",
                summary=f"{len(current_issue_keys)} issues detected",
                detail=(f"{len(opened)} opened and {len(resolved)} resolved in this read."),
                idempotency_key=f"history:issues-reconciled:{run_id}",
                payload={"opened": opened, "resolved": resolved},
            )
            append_history_event(
                connection,
                workspace_id=snapshot.workspace_id,
                project_id=snapshot.project_id,
                analysis_run_id=run_id,
                actor_type="system",
                category="versions",
                event_type="artifacts.versions_retained",
                summary=f"{len(snapshot.artifacts)} plan-artifact versions retained",
                detail="A read-only version of every plan artifact was retained.",
                idempotency_key=f"history:artifact-versions:{run_id}",
                payload={
                    "artifact_types": [
                        artifact.artifact_type.value for artifact in snapshot.artifacts
                    ]
                },
            )

    def complete_run(self, run_id: UUID) -> None:
        with self._engine.begin() as connection:
            already_completed = connection.execute(
                text(
                    """
                    select exists(
                      select 1 from public.analysis_run_events
                      where analysis_run_id = :run_id
                        and event_type = 'analysis.completed'
                    )
                    """
                ),
                {"run_id": run_id},
            ).scalar_one()
            connection.execute(
                text(
                    """
                    update public.analysis_runs
                    set status = 'completed', completed_at = coalesce(completed_at, now()),
                        updated_at = now()
                    where id = :run_id
                    """
                ),
                {"run_id": run_id},
            )
            if not already_completed:
                self._append_event(
                    connection,
                    run_id,
                    "analysis.completed",
                    AnalysisRunStatus.COMPLETED,
                )

    def fail(
        self,
        run_id: UUID,
        *,
        error_code: str,
        phase: AnalysisPhase,
        retryable: bool = True,
    ) -> None:
        safe_code = error_code[:120]
        with self._engine.begin() as connection:
            run_context = (
                connection.execute(
                    text(
                        """
                        select workspace_id, project_id
                        from public.analysis_runs
                        where id = :run_id
                        """
                    ),
                    {"run_id": run_id},
                )
                .mappings()
                .one()
            )
            connection.execute(
                text(
                    """
                    update public.analysis_runs
                    set status = 'failed', error_code = :error_code,
                        current_phase = :phase, completed_at = now(), updated_at = now()
                    where id = :run_id
                    """
                ),
                {"run_id": run_id, "error_code": safe_code, "phase": phase.value},
            )
            connection.execute(
                text(
                    """
                    update public.analysis_node_attempts
                    set status = 'failed', safe_error_code = :error_code, completed_at = now()
                    where id = (
                      select id from public.analysis_node_attempts
                      where analysis_run_id = :run_id and phase = :phase
                      order by attempt_no desc limit 1
                    )
                    """
                ),
                {"run_id": run_id, "phase": phase.value, "error_code": safe_code},
            )
            self._append_event(
                connection,
                run_id,
                "analysis.failed",
                AnalysisRunStatus.FAILED,
                phase,
                {"code": safe_code, "retryable": retryable},
            )
            append_history_event(
                connection,
                workspace_id=run_context["workspace_id"],
                project_id=run_context["project_id"],
                analysis_run_id=run_id,
                actor_type="system",
                category="analysis",
                event_type="analysis.failed",
                summary="Analysis did not complete",
                detail="The last-good project read remains current and can be retried.",
                idempotency_key=f"history:analysis-failed:{run_id}",
                payload={
                    "phase": phase.value,
                    "error_code": safe_code,
                    "retryable": retryable,
                },
            )

    def current_snapshot(self, project_id: UUID) -> AssessmentSnapshot | None:
        with self._engine.connect() as connection:
            row = connection.execute(
                text(
                    """
                    select snapshot.snapshot_json, project.name as project_name
                    from public.projects project
                    join public.assessment_snapshots snapshot
                      on snapshot.analysis_run_id = project.current_analysis_run_id
                    where project.id = :project_id
                    """
                ),
                {"project_id": project_id},
            ).mappings().one_or_none()
        if row is None:
            return None
        snapshot = _snapshot_from_dict(row["snapshot_json"])
        if snapshot.project_title:
            return snapshot
        project_name = str(row["project_name"] or "").strip()
        return replace(snapshot, project_title=project_name or None)

    def snapshot_for_run(self, run_id: UUID) -> AssessmentSnapshot | None:
        with self._engine.connect() as connection:
            payload = connection.execute(
                text(
                    """
                    select snapshot_json
                    from public.assessment_snapshots
                    where analysis_run_id = :run_id
                    """
                ),
                {"run_id": run_id},
            ).scalar_one_or_none()
        return _snapshot_from_dict(payload) if payload else None

    def events_after(self, run_id: UUID, sequence: int) -> tuple[AnalysisEvent, ...]:
        with self._engine.connect() as connection:
            rows = (
                connection.execute(
                    text(
                        """
                        select analysis_run_id, sequence_no, event_type, status,
                               phase, payload, occurred_at
                        from public.analysis_run_events
                        where analysis_run_id = :run_id and sequence_no > :sequence
                        order by sequence_no
                        """
                    ),
                    {"run_id": run_id, "sequence": sequence},
                )
                .mappings()
                .all()
            )
        return tuple(
            AnalysisEvent(
                run_id=row["analysis_run_id"],
                sequence=row["sequence_no"],
                event_type=row["event_type"],
                status=row["status"],
                phase=AnalysisPhase(row["phase"]) if row["phase"] else None,
                occurred_at=row["occurred_at"],
                error_code=row["payload"].get("code"),
                retryable=row["payload"].get("retryable"),
                artifact_type=(
                    ArtifactType(row["payload"]["artifact_type"])
                    if row["payload"].get("artifact_type")
                    else None
                ),
            )
            for row in rows
        )

    def wait_for_events(
        self,
        run_id: UUID,
        sequence: int,
        timeout: float,
    ) -> tuple[AnalysisEvent, ...]:
        deadline = monotonic() + timeout
        while monotonic() < deadline:
            events = self.events_after(run_id, sequence)
            if events:
                return events
            sleep(0.2)
        return ()

    @staticmethod
    def _workspace_id(connection: Connection, run_id: UUID) -> UUID:
        return connection.execute(
            text("select workspace_id from public.analysis_runs where id = :run_id"),
            {"run_id": run_id},
        ).scalar_one()

    @staticmethod
    def _run_status(connection: Connection, run_id: UUID) -> AnalysisRunStatus:
        status = connection.execute(
            text("select status from public.analysis_runs where id = :run_id"),
            {"run_id": run_id},
        ).scalar_one()
        return AnalysisRunStatus(status)

    def _append_event(
        self,
        connection: Connection,
        run_id: UUID,
        event_type: str,
        status: AnalysisRunStatus,
        phase: AnalysisPhase | None = None,
        payload: dict | None = None,
    ) -> None:
        run = (
            connection.execute(
                text(
                    """
                    select workspace_id, project_id from public.analysis_runs
                    where id = :run_id for update
                    """
                ),
                {"run_id": run_id},
            )
            .mappings()
            .one()
        )
        sequence = connection.execute(
            text(
                """
                select coalesce(max(sequence_no), 0) + 1
                from public.analysis_run_events where analysis_run_id = :run_id
                """
            ),
            {"run_id": run_id},
        ).scalar_one()
        event_payload = payload or {}
        connection.execute(
            text(
                """
                insert into public.analysis_run_events (
                  workspace_id, project_id, analysis_run_id, sequence_no,
                  event_type, phase, status, payload
                ) values (
                  :workspace_id, :project_id, :run_id, :sequence,
                  :event_type, :phase, :status, cast(:payload as jsonb)
                )
                """
            ),
            {
                "workspace_id": run["workspace_id"],
                "project_id": run["project_id"],
                "run_id": run_id,
                "sequence": sequence,
                "event_type": event_type,
                "phase": phase.value if phase else None,
                "status": status.value,
                "payload": json.dumps(event_payload),
            },
        )
        connection.execute(
            text(
                """
                insert into public.outbox_events (
                  workspace_id, aggregate_type, aggregate_id, event_type, payload
                ) values (
                  :workspace_id, 'analysis_run', :run_id, :event_type,
                  cast(:payload as jsonb)
                )
                """
            ),
            {
                "workspace_id": run["workspace_id"],
                "run_id": run_id,
                "event_type": event_type,
                "payload": json.dumps({"sequence": sequence, **event_payload}),
            },
        )
