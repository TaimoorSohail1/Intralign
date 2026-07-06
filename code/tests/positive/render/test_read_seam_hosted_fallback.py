from __future__ import annotations

from typing import Any

from backend.services.render.read_seam import SupabaseHistoryReader, SupabaseProjectionReader


class _FailingQuery:
    def __init__(self, exc: Exception) -> None:
        self._exc = exc

    def select(self, _columns: str = "*") -> _FailingQuery:
        return self

    def eq(self, _column: str, _value: Any) -> _FailingQuery:
        return self

    def order(self, _column: str, desc: bool = False) -> _FailingQuery:
        return self

    def limit(self, _n: int) -> _FailingQuery:
        return self

    def execute(self) -> object:
        raise self._exc


class _FailingSchema:
    def __init__(self, exc: Exception) -> None:
        self._exc = exc

    def table(self, _name: str) -> _FailingQuery:
        return _FailingQuery(self._exc)


class _FailingClient:
    def __init__(self, derived_exc: Exception, public_exc: Exception) -> None:
        self._derived_exc = derived_exc
        self._public_exc = public_exc

    def schema(self, _schema: str) -> _FailingSchema:
        return _FailingSchema(self._derived_exc)

    def table(self, _name: str) -> _FailingQuery:
        return _FailingQuery(self._public_exc)


def test_read_seam_returns_empty_when_hosted_supabase_hides_derived_schema() -> None:
    reader = SupabaseProjectionReader(
        _FailingClient(
            derived_exc=Exception(
                "{'message': 'Invalid schema: derived', 'code': 'PGRST106'}"
            ),
            public_exc=Exception("unused"),
        )
    )

    assert reader.list_projection("project-1", "finding") == []
    assert reader.get_projection("finding", "finding-1") is None


def test_read_seam_returns_empty_when_platform_read_tables_are_missing() -> None:
    reader = SupabaseProjectionReader(
        _FailingClient(
            derived_exc=Exception("unused"),
            public_exc=Exception(
                "{'message': \"Could not find the table 'public.analysis_run'\", "
                "'code': 'PGRST205'}"
            ),
        )
    )

    assert reader.list_analysis_runs("project-1") == []
    assert reader.get_analysis_run("run-1") is None


def test_read_seam_returns_empty_when_canonical_receipt_tables_are_missing() -> None:
    reader = SupabaseProjectionReader(
        _FailingClient(
            derived_exc=Exception("unused"),
            public_exc=Exception(
                "{'message': \"Could not find the table 'public.attested_assertion'\", "
                "'code': 'PGRST205'}"
            ),
        )
    )

    assert reader.list_plan_facts("project-1") == []

    reader = SupabaseProjectionReader(
        _FailingClient(
            derived_exc=Exception("unused"),
            public_exc=Exception(
                "{'message': \"Could not find the table 'public.user_acceptance_record'\", "
                "'code': 'PGRST205'}"
            ),
        )
    )

    assert reader.list_acceptances("project-1") == []


def test_history_reader_returns_empty_when_chr_table_is_missing() -> None:
    reader = SupabaseHistoryReader(
        _FailingClient(
            derived_exc=Exception("unused"),
            public_exc=Exception(
                "{'message': \"Could not find the table 'public.cognition_history_record'\", "
                "'code': 'PGRST205'}"
            ),
        )
    )

    assert reader.list_history("project-1") == []
