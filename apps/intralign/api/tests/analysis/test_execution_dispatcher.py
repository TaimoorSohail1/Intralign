from uuid import uuid4

from oslo_api.analysis.service import InlineAnalysisExecutor


def test_inline_analysis_executor_finishes_work_before_submit_returns() -> None:
    run_id = uuid4()
    completed: list[object] = []

    result = InlineAnalysisExecutor().submit(
        lambda submitted_run_id: completed.append(submitted_run_id) or "completed",
        run_id,
    )

    assert result == "completed"
    assert completed == [run_id]
