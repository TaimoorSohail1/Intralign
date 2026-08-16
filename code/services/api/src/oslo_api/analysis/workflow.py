import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, replace
from datetime import UTC, datetime
from threading import BoundedSemaphore
from time import sleep
from typing import TypedDict
from uuid import uuid4

from langgraph.graph import END, START, StateGraph

from oslo_api.analysis.evidence_graph import build_evidence_graph
from oslo_api.analysis.harness import AgentHarness, AgentHarnessError
from oslo_api.analysis.issue_identity import deduplicate_issues, stabilize_issue_ids
from oslo_api.analysis.models import (
    ARTIFACT_TYPES,
    AnalysisPassKind,
    AnalysisPhase,
    AnalysisRunRequest,
    AnalysisRunResult,
    AnalysisRunStatus,
    Artifact,
    ArtifactSection,
    ArtifactType,
    Assessment,
    AssessmentSnapshot,
    EvidenceCitation,
    EvidenceFragment,
    HarnessInvocation,
    Perception,
    RunKind,
)
from oslo_api.analysis.result_contract import canonicalize_assessment
from oslo_api.analysis.semantic_validation import (
    apply_evidence_rubric,
    audit_artifact_conflicts,
    audit_project_evidence,
    merge_semantic_issues,
    normalize_artifact_provenance,
)
from oslo_api.analysis.store import AnalysisStore
from oslo_api.analysis.understanding import enrich_assessment

SAMPLE_PLAN_DESCRIPTION = (
    "DevNorth 2026 is a one-day developer conference for approximately 450 attendees "
    "on 18 September. Confirm the venue, programme, Wi-Fi capacity, sponsors, budget, "
    "schedule and delivery owners."
)


class _GraphState(TypedDict):
    run_id: object


class AnalysisWorkflow:
    def __init__(
        self,
        *,
        store: AnalysisStore,
        harness: AgentHarness,
        phase_delay_seconds: float = 0,
        artifact_workers_per_run: int = 2,
        artifact_worker_limit: int = 4,
        artifact_attempts_per_run: int = 1,
    ) -> None:
        self._store = store
        self._harness = harness
        self._phase_delay_seconds = phase_delay_seconds
        self._artifact_workers_per_run = max(1, min(4, artifact_workers_per_run))
        self._artifact_slots = BoundedSemaphore(max(1, artifact_worker_limit))
        self._artifact_attempts_per_run = max(1, min(3, artifact_attempts_per_run))
        builder = StateGraph(_GraphState)
        phases = tuple(AnalysisPhase)
        for phase in phases:
            builder.add_node(
                phase.value,
                lambda graph_state, selected=phase: self._graph_node(graph_state, selected),
            )
        builder.add_edge(START, phases[0].value)
        for current, following in zip(phases, phases[1:], strict=False):
            builder.add_edge(current.value, following.value)
        builder.add_edge(phases[-1].value, END)
        self._graph = builder.compile()

    def run(self, request: AnalysisRunRequest) -> AnalysisRunResult:
        run = self._store.create_run(request)
        if run.status is AnalysisRunStatus.COMPLETED:
            return AnalysisRunResult(run.id, run.status, run.snapshot)
        return self._execute(run.id)

    def resume(self, run_id) -> AnalysisRunResult:
        run = self._store.get_run(run_id)
        if run is None:
            raise KeyError(f"Unknown analysis run: {run_id}")
        if run.status is AnalysisRunStatus.COMPLETED:
            return AnalysisRunResult(run.id, run.status, run.snapshot)
        return self._execute(run.id)

    def _execute(self, run_id) -> AnalysisRunResult:
        run = self._store.get_run(run_id)
        if run is None:
            raise KeyError(f"Unknown analysis run: {run_id}")
        self._store.start_run(run.id)
        try:
            self._graph.invoke({"run_id": run.id})
            latest = self._store.get_run(run.id)
            return AnalysisRunResult(
                run.id,
                AnalysisRunStatus.COMPLETED,
                latest.snapshot if latest else None,
            )
        except Exception as error:
            current = self._store.get_run(run.id)
            phase = (
                current.current_phase
                if current and current.current_phase
                else AnalysisPhase.SUBMIT_INTAKE
            )
            error_code, retryable = self._safe_failure(error)
            self._store.fail(
                run.id,
                error_code=error_code,
                phase=phase,
                retryable=retryable,
            )
            return AnalysisRunResult(
                run.id,
                AnalysisRunStatus.FAILED,
                None,
                error_code,
            )

    def _graph_node(self, graph_state: _GraphState, phase: AnalysisPhase) -> _GraphState:
        run_id = graph_state["run_id"]
        run = self._store.get_run(run_id)
        if run is None:
            raise KeyError(f"Unknown analysis run: {run_id}")
        if phase in set(run.completed_phases):
            return graph_state
        request = run.request
        harness_kind = (
            RunKind.INITIAL
            if request.pass_kind is AnalysisPassKind.FAST
            else RunKind.EXTENDED
        )
        state = dict(run.checkpoint_state)

        if phase in {
            AnalysisPhase.SUBMIT_INTAKE,
            AnalysisPhase.VALIDATE_SCOPE,
            AnalysisPhase.INGEST_PARSE,
            AnalysisPhase.RETRIEVE_EVIDENCE,
            AnalysisPhase.CHECKPOINT,
            AnalysisPhase.PROJECT_BROWSER,
            AnalysisPhase.EXTENDED_TRANSITION,
        }:
            self._phase(run.id, request, phase, state)
        elif phase is AnalysisPhase.PERCEIVE:
            self._start(run.id, request, phase)
            invocation = self._harness_invocation(run.id, phase, state)
            evidence = self._store.evidence_for(request) + request.user_evidence
            governed_description = self._governed_description(
                request.description,
                evidence,
            )
            state["governed_description"] = governed_description
            perception = self._harness.perceive(
                description=governed_description,
                source_names=request.source_names,
                evidence=evidence,
                kind=harness_kind,
                invocation=invocation,
            )
            evidence_graph = build_evidence_graph(perception.evidence)
            state["perception"] = replace(
                perception,
                structured_claims=evidence_graph.claims,
                claim_relations=evidence_graph.relations,
            )
            self._record_harness_call(state, invocation)
            self._store.complete_phase(run.id, phase, state)
        elif phase is AnalysisPhase.CONSTRUCT_ARTIFACTS:
            self._start(run.id, request, phase)
            completed = self._store.completed_artifacts(run.id)
            results = self._parent_artifacts_for_edit(request)
            results.update(completed)
            remaining = tuple(
                artifact_type
                for artifact_type in ARTIFACT_TYPES
                if artifact_type not in results
            )
            failures: list[Exception] = []

            def construct_one(artifact_type):
                for attempt in range(1, self._artifact_attempts_per_run + 1):
                    try:
                        with self._artifact_slots:
                            invocation = self._harness_invocation(run.id, phase, state)
                            artifact = normalize_artifact_provenance(
                                (
                                    self._harness.construct_artifact(
                                        perception=state["perception"],
                                        artifact_type=artifact_type,
                                        kind=harness_kind,
                                        invocation=invocation,
                                    ),
                                )
                            )[0]
                    except Exception as error:
                        _error_code, retryable = self._safe_failure(error)
                        if retryable and attempt < self._artifact_attempts_per_run:
                            continue
                        if retryable and self._can_fallback_artifact(error):
                            return (
                                self._fallback_artifact(
                                    perception=state["perception"],
                                    artifact_type=artifact_type,
                                ),
                                invocation,
                            )
                        raise
                    return artifact, invocation
                raise RuntimeError("ARTIFACT_ATTEMPTS_EXHAUSTED")

            # Persist job lifecycle changes in a stable order. The model calls run
            # concurrently, but concurrent event writers would contend on the run's
            # ordered event sequence and can deadlock in Postgres.
            for artifact_type in remaining:
                self._store.start_artifact_job(run.id, artifact_type)
            with ThreadPoolExecutor(
                max_workers=self._artifact_workers_per_run,
                thread_name_prefix="oslo-artifact",
            ) as pool:
                futures = {
                    pool.submit(construct_one, artifact_type): artifact_type
                    for artifact_type in remaining
                }
                for future in as_completed(futures):
                    artifact_type = futures[future]
                    try:
                        artifact, invocation = future.result()
                    except Exception as error:
                        error_code, retryable = self._safe_failure(error)
                        self._store.fail_artifact_job(
                            run.id,
                            artifact_type,
                            error_code=error_code,
                            retryable=retryable,
                        )
                        failures.append(error)
                        continue
                    results[artifact_type] = artifact
                    self._store.complete_artifact_job(
                        run.id,
                        artifact,
                        invocation.metadata,
                    )
                    self._record_artifact_harness_call(
                        state,
                        artifact_type,
                        invocation,
                    )
            if failures:
                raise failures[0]
            state["artifacts"] = tuple(results[item] for item in ARTIFACT_TYPES)
            self._store.complete_phase(run.id, phase, state)
        elif phase is AnalysisPhase.EVALUATE_ADVISE:
            self._start(run.id, request, phase)
            invocation = self._harness_invocation(run.id, phase, state)
            model_assessment = self._harness.evaluate(
                artifacts=state["artifacts"],
                perception=state["perception"],
                kind=harness_kind,
                context=str(state.get("governed_description", request.description)),
                invocation=invocation,
            )
            state["assessment"] = canonicalize_assessment(
                apply_evidence_rubric(
                    replace(
                        model_assessment,
                        issues=merge_semantic_issues(
                            model_assessment.issues,
                            (
                                *audit_project_evidence(state["perception"].evidence),
                                *audit_artifact_conflicts(state["artifacts"]),
                            ),
                        ),
                    ),
                    state["perception"].evidence,
                )
            )
            self._record_harness_call(state, invocation)
            self._store.complete_phase(run.id, phase, state)
        elif phase is AnalysisPhase.VALIDATE_RESULT:
            self._start(run.id, request, phase)
            artifacts = state["artifacts"]
            if tuple(artifact.artifact_type for artifact in artifacts) != ARTIFACT_TYPES:
                raise ValueError("SEVEN_ARTIFACT_CONTRACT_FAILED")
            if not all(artifact.evidence_refs for artifact in artifacts):
                raise ValueError("EVIDENCE_CONTRACT_FAILED")
            self._store.complete_phase(run.id, phase, state)
        elif phase is AnalysisPhase.PUBLISH:
            self._start(run.id, request, phase)
            previous_snapshot = self._store.current_snapshot(request.project_id)
            raw_assessment = canonicalize_assessment(state["assessment"])
            state["assessment"] = replace(
                raw_assessment,
                issues=deduplicate_issues(
                    stabilize_issue_ids(
                        raw_assessment.issues,
                        (
                            previous_snapshot.assessment.issues
                            if previous_snapshot
                            else ()
                        ),
                    )
                ),
            )
            assessment = enrich_assessment(
                assessment=state["assessment"],
                artifacts=state["artifacts"],
                kind=request.kind,
                previous_snapshot=previous_snapshot,
                description=str(state.get("governed_description", request.description)),
                user_evidence=request.user_evidence,
            )
            state["assessment"] = assessment
            project_title = next(
                (
                    artifact.project_title
                    for artifact in state["artifacts"]
                    if artifact.project_title
                ),
                None,
            )
            project_title = project_title or self._supported_project_title(state["perception"])
            if project_title:
                state["artifacts"] = tuple(
                    artifact
                    if artifact.project_title
                    else replace(artifact, project_title=project_title)
                    for artifact in state["artifacts"]
                )
            snapshot = AssessmentSnapshot(
                id=uuid4(),
                analysis_run_id=run.id,
                workspace_id=request.workspace_id,
                project_id=request.project_id,
                state="current" if request.kind is RunKind.EXTENDED else "provisional",
                summary=self._summary(
                    description=str(state.get("governed_description", request.description)),
                    perception=state["perception"],
                    artifacts=state["artifacts"],
                    assessment=assessment,
                ),
                artifacts=state["artifacts"],
                assessment=assessment,
                published_at=datetime.now(UTC),
                evidence_citations=self._evidence_citations(
                    perception=state["perception"],
                    artifacts=state["artifacts"],
                    assessment=assessment,
                ),
                project_title=project_title,
                source_document_count=len(set(request.source_document_ids))
                or len(set(request.source_names)),
            )
            self._store.publish(run.id, snapshot)
            self._store.complete_phase(run.id, phase, state)
        if phase is AnalysisPhase.EXTENDED_TRANSITION:
            self._store.complete_run(run.id)
        return graph_state

    @staticmethod
    def _governed_description(
        description: str,
        evidence: tuple[EvidenceFragment, ...],
    ) -> str:
        """Keep the built-in demo copy out of a real document-backed read."""

        base, separator, clarification = description.partition("\n\nUSER_CLARIFICATION")
        normalized_base = " ".join(base.split())
        has_documents = any(
            item.reference.startswith("document:") for item in evidence
        )
        if has_documents and normalized_base == SAMPLE_PLAN_DESCRIPTION:
            return f"USER_CLARIFICATION{clarification}" if separator else ""
        return description

    @staticmethod
    def _can_fallback_artifact(error: Exception) -> bool:
        return isinstance(error, AgentHarnessError) and error.code in {
            "EVIDENCE_REFERENCE_CONTRACT_FAILED",
            "OPENAI_OUTPUT_LIMIT",
            "OPENAI_RATE_LIMIT",
            "OPENAI_SCHEMA_INVALID",
            "OPENAI_TIMEOUT",
            "OPENAI_UNAVAILABLE",
        }

    @staticmethod
    def _fallback_artifact(
        *,
        perception: Perception,
        artifact_type: ArtifactType,
    ) -> Artifact:
        """Retain a usable, visibly provisional artifact after provider exhaustion."""

        evidence_refs = tuple(
            dict.fromkeys(
                (
                    *perception.evidence_refs,
                    *(item.reference for item in perception.evidence),
                )
            )
        )[:20]
        if not evidence_refs:
            evidence_refs = ("description:1",)
        bullets = tuple(
            item.strip()
            for item in (*perception.facts, *perception.claims, *perception.gaps)
            if item.strip()
        )[:12]
        if not bullets:
            bullets = ("Available project evidence is retained for confirmation.",)
        label = artifact_type.value.replace("_", " ").title()
        return Artifact(
            artifact_type=artifact_type,
            title=label,
            summary=(
                f"A provisional {label.lower()} view was assembled from the available "
                "evidence and should be confirmed."
            ),
            reliability="Low",
            evidence_refs=evidence_refs,
            basis="inferred",
            sections=(
                ArtifactSection(
                    heading="Evidence retained",
                    bullets=bullets,
                    evidence_refs=evidence_refs,
                ),
            ),
        )

    def _scope_artifact_edit(
        self,
        *,
        request: AnalysisRunRequest,
        constructed: tuple[Artifact, ...],
    ) -> tuple[Artifact, ...]:
        """Keep unrelated artifacts stable during a single-artifact edit run."""

        edited_types = {
            item.reference.split(":", 3)[2]
            for item in request.user_evidence
            if item.reference.startswith("user:artifact:")
            and len(item.reference.split(":", 3)) == 4
        }
        if len(edited_types) != 1 or request.parent_run_id is None:
            return constructed
        parent = self._store.get_run(request.parent_run_id)
        if parent is None or parent.snapshot is None:
            return constructed
        edited_type = next(iter(edited_types))
        parent_by_type = {
            artifact.artifact_type.value: artifact for artifact in parent.snapshot.artifacts
        }
        return tuple(
            artifact
            if artifact.artifact_type.value == edited_type
            else parent_by_type.get(artifact.artifact_type.value, artifact)
            for artifact in constructed
        )

    def _parent_artifacts_for_edit(
        self,
        request: AnalysisRunRequest,
    ) -> dict[ArtifactType, Artifact]:
        """Reuse unrelated parent artifacts before scheduling model work.

        Artifact edits and issue clarifications rebuild the owning artifact plus
        the later cross-artifact evaluator. Source-document changes still rebuild
        all seven artifacts.
        """
        edited_types = {
            item.reference.split(":", 3)[2]
            for item in request.user_evidence
            if item.reference.startswith("user:artifact:")
            and len(item.reference.split(":", 3)) == 4
        }
        if request.parent_run_id is None:
            return {}
        parent = self._store.get_run(request.parent_run_id)
        if parent is None or parent.snapshot is None:
            return {}
        if len(edited_types) == 1:
            edited_type = next(iter(edited_types))
        else:
            clarification_ids = {
                match.group("issue")
                for item in request.user_evidence
                if (
                    match := re.fullmatch(
                        r"user:clarification:(?P<issue>[^:]+):answer:[^:]+",
                        item.reference,
                    )
                )
            }
            if len(clarification_ids) != 1:
                return {}
            clarification_id = next(iter(clarification_ids))
            previous_issue = next(
                (
                    issue
                    for issue in parent.snapshot.assessment.issues
                    if issue.id == clarification_id
                ),
                None,
            )
            if previous_issue is None:
                return {}
            edited_type = previous_issue.artifact_type.value
        return {
            artifact.artifact_type: artifact
            for artifact in parent.snapshot.artifacts
            if artifact.artifact_type.value != edited_type
        }

    @staticmethod
    def _supported_project_title(perception: Perception) -> str | None:
        """Extract a repeated governed-document title without guessing.

        Many project packs repeat ``<project title> <document id> |`` in the
        header of every artifact. Requiring the same candidate in two distinct
        source documents keeps automatic naming evidence-backed.
        """
        title_sources: dict[str, set[str]] = {}
        display_titles: dict[str, str] = {}
        header_pattern = re.compile(
            r"^\s*(?P<title>[A-Za-z0-9][A-Za-z0-9 &'(),./+-]{2,159}?)"
            r"\s+[A-Z][A-Z0-9]*-[A-Z0-9-]{2,}\s*\|"
        )
        for fragment in perception.evidence:
            match = header_pattern.search(fragment.content[:300])
            if match is None:
                continue
            title = " ".join(match.group("title").split()).strip(" -|")
            if not 3 <= len(title) <= 160 or not 2 <= len(title.split()) <= 16:
                continue
            key = title.casefold()
            display_titles.setdefault(key, title)
            title_sources.setdefault(key, set()).add(fragment.source_name or fragment.reference)
        supported = [
            (len(sources), display_titles[key])
            for key, sources in title_sources.items()
            if len(sources) >= 2
        ]
        if not supported:
            return None
        supported.sort(key=lambda item: (-item[0], item[1].casefold()))
        return supported[0][1]

    def _phase(
        self,
        run_id,
        request: AnalysisRunRequest,
        phase: AnalysisPhase,
        state: dict[str, object],
    ) -> None:
        self._start(run_id, request, phase)
        self._store.complete_phase(run_id, phase, state)

    def _start(self, run_id, request: AnalysisRunRequest, phase: AnalysisPhase) -> None:
        self._store.start_phase(run_id, phase)
        if request.fail_at is phase:
            raise RuntimeError(f"{phase.value.upper()}_FAILED")
        if self._phase_delay_seconds > 0:
            sleep(self._phase_delay_seconds)

    @staticmethod
    def _harness_invocation(
        run_id,
        phase: AnalysisPhase,
        state: dict[str, object],
    ) -> HarnessInvocation:
        del state
        return HarnessInvocation(
            run_id=run_id,
            phase=phase,
        )

    @staticmethod
    def _record_harness_call(
        state: dict[str, object],
        invocation: HarnessInvocation,
    ) -> None:
        if invocation.metadata is None:
            return
        calls = state.setdefault("harness_calls", {})
        if isinstance(calls, dict):
            calls[invocation.phase.value] = asdict(invocation.metadata)

    @staticmethod
    def _record_artifact_harness_call(
        state: dict[str, object],
        artifact_type: ArtifactType,
        invocation: HarnessInvocation,
    ) -> None:
        if invocation.metadata is None:
            return
        calls = state.setdefault("artifact_harness_calls", {})
        if isinstance(calls, dict):
            calls[artifact_type.value] = asdict(invocation.metadata)

    @staticmethod
    def _summary(
        *,
        description: str,
        perception: Perception,
        artifacts: tuple[Artifact, ...],
        assessment: Assessment,
    ) -> str:
        document_fact = next(
            (
                " ".join(fragment.content.split())
                for fragment in perception.evidence
                if fragment.reference.startswith("document:")
                and fragment.content.strip()
            ),
            "",
        )
        visible_description = description.split(
            "\n\nUSER_CLARIFICATION",
            maxsplit=1,
        )[0]
        normalized = " ".join(visible_description.split())
        evidence_fact = next(
            (
                " ".join(fact.split())
                for fact in perception.facts
                if fact and fact != "Document evidence supplied."
            ),
            "",
        )
        # Uploaded documents are the governed source for the current read. A stale
        # intake prompt must never name a different project in a retained summary.
        if document_fact and normalized:
            project_read = document_fact
        else:
            project_read = evidence_fact or document_fact or normalized
        project_read = project_read[:320].rstrip()

        project_read = re.sub(
            r"\s*\[?document:[^\]\s]*\]?",
            "",
            project_read,
        ).strip()
        if project_read and project_read[-1] not in ".!?":
            project_read += "."

        artifact_names = ", ".join(artifact.title.lower() for artifact in artifacts)
        open_count = sum(issue.status != "resolved" for issue in assessment.issues)
        understanding_sentence = (
            f"At the {assessment.understanding_stage} stage, OSLO mapped the supplied "
            f"evidence into {len(artifacts)} plan artifacts covering {artifact_names}. "
            f"The read is {assessment.confidence_band.lower()} confidence, limited by "
            f"{assessment.limiting_dimension}; {open_count} open "
            f"finding{'s' if open_count != 1 else ''} identify the main uncertainty."
        )
        basis = assessment.reliability_basis
        reliability_sentence = (
            f"Reliability is {assessment.reliability.lower()}, based on "
            f"{basis.coverage.lower()} coverage, {basis.evidence.lower()} evidence "
            f"availability, and {basis.assessability.lower()} assessability."
        )
        advisory_boundary = (
            "This is OSLO's understanding of the plan—not project health, readiness, "
            "or a probability of success."
        )
        return " ".join(
            sentence
            for sentence in (
                project_read,
                understanding_sentence,
                reliability_sentence,
                advisory_boundary,
            )
            if sentence
        )

    @staticmethod
    def _evidence_citations(
        *,
        perception: Perception,
        artifacts: tuple[Artifact, ...],
        assessment: Assessment,
    ) -> tuple[EvidenceCitation, ...]:
        referenced = (
            {reference for artifact in artifacts for reference in artifact.evidence_refs}
            | {
                reference
                for artifact in artifacts
                for section in artifact.sections
                for reference in section.evidence_refs
            }
            | {
                reference
                for artifact in artifacts
                for section in artifact.sections
                for row_references in section.row_evidence_refs
                for reference in row_references
            }
            | {
                reference
                for artifact in artifacts
                for assumption in artifact.assumptions
                for reference in assumption.evidence_refs
            }
            | {
                reference
                for artifact in artifacts
                for conflict in artifact.conflicts
                for reference in conflict.evidence_refs
            }
            | {reference for issue in assessment.issues for reference in issue.evidence_refs}
        )
        citations = []
        for fragment in perception.evidence:
            if fragment.reference not in referenced:
                continue
            excerpt = " ".join(fragment.content.split())[:500].rstrip()
            citations.append(
                EvidenceCitation(
                    reference=fragment.reference,
                    source_name=fragment.source_name or "Project description",
                    location=fragment.location or "Intake",
                    excerpt=excerpt,
                )
            )
        return tuple(citations)

    @staticmethod
    def _safe_failure(error: Exception) -> tuple[str, bool]:
        if isinstance(error, AgentHarnessError):
            return error.code, error.retryable
        message = str(error)
        if (
            message
            and len(message) <= 120
            and all(
                character.isupper() or character.isdigit() or character == "_"
                for character in message
            )
        ):
            return message, True
        return "ANALYSIS_FAILED", True
