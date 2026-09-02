import logging
import os
from socket import gethostname
from time import sleep
from uuid import uuid4

from oslo_api.analysis.job_queue import DatabaseAnalysisJobQueue
from oslo_api.analysis.service import build_slice_two_application
from oslo_api.database import create_database_engine
from oslo_api.settings import Settings

logger = logging.getLogger("oslo.analysis.worker")


def run_worker() -> None:
    settings = Settings()  # type: ignore[call-arg]
    engine = create_database_engine(settings.database_url)
    queue = DatabaseAnalysisJobQueue(engine)
    application = build_slice_two_application()
    worker_id = f"{gethostname()}:{os.getpid()}:{uuid4()}"
    logger.info("analysis worker started", extra={"worker_id": worker_id})
    while True:
        run_id = queue.claim(
            worker_id=worker_id,
            lease_seconds=settings.analysis_worker_lease_seconds,
        )
        if run_id is None:
            sleep(settings.analysis_worker_poll_seconds)
            continue
        try:
            application.execute_queued_run(run_id)
        except Exception as error:
            logger.exception("analysis worker job crashed", extra={"run_id": str(run_id)})
            queue.release(
                run_id,
                error_code=type(error).__name__,
                delay_seconds=min(60, max(1, int(settings.analysis_worker_poll_seconds)) * 5),
            )
        else:
            queue.complete(run_id)


if __name__ == "__main__":
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    run_worker()
