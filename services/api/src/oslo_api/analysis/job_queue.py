from collections.abc import Callable
from uuid import UUID

from sqlalchemy import Engine, text


class DatabaseAnalysisJobQueue:
    """Postgres-backed analysis dispatcher with leases and crash recovery."""

    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def submit(self, function: Callable[[UUID], object], run_id: UUID) -> None:
        del function
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    insert into public.analysis_jobs (analysis_run_id, status)
                    values (:run_id, 'queued')
                    on conflict (analysis_run_id) do update set
                      status = 'queued', available_at = now(), locked_at = null,
                      locked_by = null, last_error = null, updated_at = now()
                    """
                ),
                {"run_id": run_id},
            )

    def claim(self, *, worker_id: str, lease_seconds: int) -> UUID | None:
        with self._engine.begin() as connection:
            return connection.execute(
                text(
                    """
                    with candidate as (
                      select analysis_run_id
                      from public.analysis_jobs
                      where (
                        status = 'queued' and available_at <= now()
                      ) or (
                        status = 'running'
                        and locked_at < now() - make_interval(secs => :lease_seconds)
                      )
                      order by available_at, created_at
                      for update skip locked
                      limit 1
                    )
                    update public.analysis_jobs job
                    set status = 'running', attempts = attempts + 1,
                        locked_at = now(), locked_by = :worker_id, updated_at = now()
                    from candidate
                    where job.analysis_run_id = candidate.analysis_run_id
                    returning job.analysis_run_id
                    """
                ),
                {"worker_id": worker_id, "lease_seconds": lease_seconds},
            ).scalar_one_or_none()

    def complete(self, run_id: UUID) -> None:
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.analysis_jobs
                    set status = 'completed', locked_at = null, locked_by = null,
                        last_error = null, updated_at = now()
                    where analysis_run_id = :run_id
                    """
                ),
                {"run_id": run_id},
            )

    def release(self, run_id: UUID, *, error_code: str, delay_seconds: int) -> None:
        safe_error = error_code[:120]
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.analysis_jobs
                    set status = 'queued', locked_at = null, locked_by = null,
                        last_error = :error_code,
                        available_at = now() + make_interval(secs => :delay_seconds),
                        updated_at = now()
                    where analysis_run_id = :run_id
                    """
                ),
                {
                    "run_id": run_id,
                    "error_code": safe_error,
                    "delay_seconds": delay_seconds,
                },
            )
