"""A minimal in-memory PostgREST-shaped Supabase client fake (test transport).

Stands in for ``supabase.Client`` so the platform repos (DTM-0031) and the
DTM-0018 ``SupabaseProjectionReader`` can be exercised through the SAME chained
call surface they use in production —
``client.table(name).insert/update/select(...).eq(...).order(...).limit(...).execute()``
and ``client.schema(s).table(name)...`` — without a live Supabase stack. This is
the house "fake the transport, exercise the real seam" style (cf.
``tests/positive/disclose`` FakeProjectionStore).

Scope: only the operators the repos + read seam use. Rows are plain dicts kept
in ``(schema, table)`` buckets; mutations apply in place (platform tables are
mutable — NOT append-only). No canonical-table semantics are simulated here: the
canonical append-only guard lives in the DB migration, not this fake.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class _Response:
    def __init__(self, data: list[dict[str, Any]]) -> None:
        self.data = data


class _Query:
    """A lazily-built PostgREST query over one ``(schema, table)`` bucket."""

    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self._rows = rows  # live reference to the table's row list
        self._op: str | None = None
        self._payload: list[dict[str, Any]] = []
        self._on_conflict: str | None = None
        self._filters: list[tuple[str, Any]] = []
        self._order: list[tuple[str, bool]] = []
        self._limit: int | None = None

    # -- write ops ---------------------------------------------------------
    def insert(self, payload: Mapping[str, Any] | list[Mapping[str, Any]]) -> _Query:
        self._op = "insert"
        self._payload = [dict(payload)] if isinstance(payload, Mapping) else [dict(p) for p in payload]
        return self

    def upsert(self, payload: Mapping[str, Any], on_conflict: str | None = None) -> _Query:
        self._op = "upsert"
        self._payload = [dict(payload)]
        self._on_conflict = on_conflict
        return self

    def update(self, payload: Mapping[str, Any]) -> _Query:
        self._op = "update"
        self._payload = [dict(payload)]
        return self

    def delete(self) -> _Query:
        self._op = "delete"
        return self

    # -- read op + modifiers ----------------------------------------------
    def select(self, _columns: str = "*") -> _Query:
        self._op = "select"
        return self

    def eq(self, column: str, value: Any) -> _Query:
        self._filters.append((column, value))
        return self

    def order(self, column: str, desc: bool = False) -> _Query:
        self._order.append((column, desc))
        return self

    def limit(self, n: int) -> _Query:
        self._limit = n
        return self

    # -- terminal ----------------------------------------------------------
    def _matches(self, row: dict[str, Any]) -> bool:
        return all(str(row.get(col)) == str(val) for col, val in self._filters)

    def execute(self) -> _Response:
        if self._op == "insert":
            self._rows.extend(self._payload)
            return _Response([dict(r) for r in self._payload])

        if self._op == "upsert":
            row = self._payload[0]
            key = self._on_conflict
            if key is not None:
                for existing in self._rows:
                    if str(existing.get(key)) == str(row.get(key)):
                        existing.update(row)
                        return _Response([dict(existing)])
            self._rows.append(row)
            return _Response([dict(row)])

        if self._op == "update":
            changed = []
            for row in self._rows:
                if self._matches(row):
                    row.update(self._payload[0])
                    changed.append(dict(row))
            return _Response(changed)

        if self._op == "delete":
            kept, removed = [], []
            for row in self._rows:
                (removed if self._matches(row) else kept).append(row)
            self._rows[:] = kept
            return _Response([dict(r) for r in removed])

        # select
        result = [dict(r) for r in self._rows if self._matches(row=r)]
        for column, desc in reversed(self._order):
            result.sort(key=lambda r, c=column: (r.get(c) is None, r.get(c)), reverse=desc)
        if self._limit is not None:
            result = result[: self._limit]
        return _Response(result)


class _Schema:
    def __init__(self, client: FakeSupabaseClient, schema: str) -> None:
        self._client = client
        self._schema = schema

    def table(self, name: str) -> _Query:
        return _Query(self._client._bucket(self._schema, name))


class FakeSupabaseClient:
    """In-memory stand-in for ``supabase.Client`` (public schema + named schemas)."""

    def __init__(self) -> None:
        self._tables: dict[tuple[str, str], list[dict[str, Any]]] = {}

    def _bucket(self, schema: str, name: str) -> list[dict[str, Any]]:
        return self._tables.setdefault((schema, name), [])

    def table(self, name: str) -> _Query:
        return _Query(self._bucket("public", name))

    def schema(self, schema: str) -> _Schema:
        return _Schema(self, schema)
