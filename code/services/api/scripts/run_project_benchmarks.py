"""Re-run existing projects through the governed analysis pipeline.

This is an operational benchmark helper, not production analysis logic. It
reuses each project's latest source-document envelope, waits for the automatic
extended read, and emits a compact JSON result suitable for regression reports.
"""

import argparse
import json
import time
from dataclasses import asdict
from pathlib import Path
from uuid import UUID, uuid4

from sqlalchemy import create_engine, text

from oslo_api.analysis.evaluation import (
    BenchmarkManifest,
    evaluate_benchmark,
    manifest_from_mapping,
)
from oslo_api.analysis.models import AnalysisRunStatus, RunKind
from oslo_api.analysis.service import build_slice_two_application
from oslo_api.settings import Settings


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project",
        action="append",
        required=True,
        type=UUID,
        help="Existing project UUID. Repeat for multiple independent fixtures.",
    )
    parser.add_argument("--timeout", type=float, default=900)
    parser.add_argument(
        "--manifest",
        action="append",
        default=[],
        metavar="PROJECT_UUID=MANIFEST.json",
        help=(
            "Optional expected-findings manifest. It is used only for offline "
            "regression scoring and is never passed to the analysis pipeline."
        ),
    )
    return parser.parse_args()


def _load_manifests(values: list[str]) -> dict[UUID, BenchmarkManifest]:
    manifests: dict[UUID, BenchmarkManifest] = {}
    for value in values:
        project_value, separator, path_value = value.partition("=")
        if not separator:
            raise ValueError("--manifest must use PROJECT_UUID=MANIFEST.json")
        payload = json.loads(Path(path_value).read_text(encoding="utf-8"))
        manifests[UUID(project_value)] = manifest_from_mapping(payload)
    return manifests


def main() -> int:
    arguments = _arguments()
    manifests = _load_manifests(arguments.manifest)
    settings = Settings()  # type: ignore[call-arg]
    engine = create_engine(settings.database_url, pool_pre_ping=True)
    application = build_slice_two_application()
    started_at = time.monotonic()
    project_started_at: dict[UUID, float] = {}
    runs: dict[UUID, tuple[UUID, UUID]] = {}

    with engine.connect() as connection:
        for project_id in arguments.project:
            active_run = connection.execute(
                text(
                    """
                    select id
                    from public.analysis_runs
                    where project_id = :project_id
                      and status in ('queued', 'running')
                    order by created_at desc
                    limit 1
                    """
                ),
                {"project_id": project_id},
            ).scalar_one_or_none()
            if active_run is not None:
                raise RuntimeError(
                    f"Project {project_id} already has active run {active_run}"
                )
            source = (
                connection.execute(
                    text(
                        """
                        select run.description, run.source_names,
                               run.source_document_ids,
                               membership.user_id
                        from public.analysis_runs run
                        join public.memberships membership
                          on membership.workspace_id = run.workspace_id
                        where run.project_id = :project_id
                        order by
                          case membership.role when 'owner' then 0 else 1 end,
                          run.created_at desc
                        limit 1
                        """
                    ),
                    {"project_id": project_id},
                )
                .mappings()
                .one()
            )
            actor_id = UUID(str(source["user_id"]))
            run = application.start_analysis(
                actor_user_id=actor_id,
                project_id=project_id,
                description=source["description"],
                source_names=tuple(source["source_names"]),
                source_document_ids=tuple(
                    UUID(str(item)) for item in source["source_document_ids"]
                ),
                kind=RunKind.INITIAL,
                key=f"benchmark:{project_id}:{uuid4()}",
            )
            runs[project_id] = (actor_id, run.id)
            project_started_at[project_id] = time.monotonic()

    completed: dict[UUID, dict[str, object]] = {}
    while len(completed) < len(runs):
        if time.monotonic() - started_at > arguments.timeout:
            pending = [str(item) for item in runs if item not in completed]
            raise TimeoutError(f"Benchmark timed out for: {', '.join(pending)}")
        for project_id, (actor_id, initial_run_id) in runs.items():
            if project_id in completed:
                continue
            initial = application.get_run(
                actor_user_id=actor_id,
                run_id=initial_run_id,
            )
            if initial.status is AnalysisRunStatus.FAILED:
                completed[project_id] = {
                    "status": "failed",
                    "run_id": str(initial.id),
                    "error_code": initial.error_code,
                }
                continue
            extended = application.latest_extended_run(
                actor_user_id=actor_id,
                project_id=project_id,
            )
            if extended is None or extended.request.parent_run_id != initial.id:
                continue
            if extended.status is AnalysisRunStatus.FAILED:
                completed[project_id] = {
                    "status": "failed",
                    "run_id": str(extended.id),
                    "error_code": extended.error_code,
                }
                continue
            if extended.status is not AnalysisRunStatus.COMPLETED:
                continue
            snapshot = application.current_overview(
                actor_user_id=actor_id,
                project_id=project_id,
            )
            assessment = snapshot.assessment
            duration_seconds = round(
                time.monotonic() - project_started_at[project_id],
                1,
            )
            completed[project_id] = {
                "status": "completed",
                "run_id": str(extended.id),
                "duration_seconds": duration_seconds,
                "confidence": assessment.confidence_band,
                "clarity": assessment.clarity,
                "alignment": assessment.alignment,
                "feasibility": assessment.feasibility,
                "reliability": assessment.reliability,
                "open_issues": sum(
                    issue.status != "resolved" for issue in assessment.issues
                ),
                "critical_issues": sum(
                    issue.status != "resolved" and issue.severity == "Critical"
                    for issue in assessment.issues
                ),
                "issues": [
                    {
                        "id": issue.id,
                        "artifact": issue.artifact_type.value,
                        "dimension": issue.dimension,
                        "severity": issue.severity,
                        "title": issue.title,
                        "evidence_refs": list(issue.evidence_refs),
                    }
                    for issue in assessment.issues
                    if issue.status != "resolved"
                ],
            }
            manifest = manifests.get(project_id)
            if manifest is not None:
                completed[project_id]["benchmark"] = asdict(
                    evaluate_benchmark(
                        manifest,
                        assessment.issues,
                        duration_seconds=duration_seconds,
                        ratings=(
                            assessment.clarity,
                            assessment.alignment,
                            assessment.feasibility,
                            assessment.reliability,
                            assessment.confidence_band,
                        ),
                    )
                )
        time.sleep(1)

    print(
        json.dumps(
            {str(project_id): result for project_id, result in completed.items()},
            indent=2,
        )
    )
    return 0 if all(item["status"] == "completed" for item in completed.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
