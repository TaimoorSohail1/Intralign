from __future__ import annotations

import re
from hashlib import sha256
from typing import Any, Protocol

import httpx


class AsanaGateway(Protocol):
    destination_gid: str

    def create_task(self, item: dict[str, Any]) -> dict[str, str]: ...


class HttpAsanaGateway:
    """Narrow Asana boundary: executable-plan fields only, never the OSLO read."""

    def __init__(
        self,
        *,
        access_token: str,
        destination_gid: str,
        client: httpx.Client | None = None,
    ) -> None:
        self.destination_gid = destination_gid
        self._access_token = access_token
        self._client = client or httpx.Client(timeout=20)

    def create_task(self, item: dict[str, Any]) -> dict[str, str]:
        notes = [
            f"Owner: {item.get('owner') or 'Unassigned'}",
            f"Source date: {item.get('source_date') or 'Not set'}",
            f"OSLO provenance: {item.get('provenance') or 'Not recorded'}",
            f"OSLO item key: {item['item_key']}",
        ]
        data: dict[str, Any] = {
            "name": item["task"],
            "notes": "\n".join(notes),
            "projects": [self.destination_gid],
        }
        if item.get("start_on"):
            data["start_on"] = item["start_on"]
        if item.get("due_on"):
            data["due_on"] = item["due_on"]
        response = self._client.post(
            "https://app.asana.com/api/1.0/tasks",
            headers={
                "authorization": f"Bearer {self._access_token}",
                "content-type": "application/json",
            },
            json={"data": data},
        )
        response.raise_for_status()
        task = response.json()["data"]
        return {
            "gid": str(task["gid"]),
            "permalink_url": str(task.get("permalink_url") or ""),
        }


def executable_plan_items(snapshot: dict[str, Any]) -> list[dict[str, str | None]]:
    """Project a retained snapshot into task/owner/date/provenance only."""

    items: list[dict[str, str | None]] = []
    for artifact in snapshot.get("artifacts") or []:
        artifact_refs = artifact.get("evidence_refs") or []
        content = artifact.get("content") or {}
        for section in content.get("sections") or []:
            columns = [str(value).strip() for value in section.get("columns") or []]
            for index, row in enumerate(section.get("rows") or []):
                fields = {
                    columns[column_index].lower(): str(value).strip()
                    for column_index, value in enumerate(row)
                    if column_index < len(columns) and str(value).strip()
                }
                task = _first_field(
                    fields,
                    "task",
                    "item",
                    "deliverable",
                    "work package",
                    "milestone",
                    "activity",
                    "action",
                )
                if not task:
                    continue
                refs = (section.get("row_evidence_refs") or [])
                provenance = refs[index] if index < len(refs) else artifact_refs
                items.append(
                    _plan_item(
                        task=task,
                        owner=_first_field(fields, "owner", "responsible", "accountable"),
                        start_on=_date_field(fields, "start", "start date", "starts"),
                        due_on=_date_field(fields, "due", "due date", "end", "end date", "date"),
                        provenance=" | ".join(str(value) for value in provenance),
                    )
                )

    if not items:
        assessment = snapshot.get("assessment") or {}
        for issue in assessment.get("issues") or []:
            if issue.get("status") == "resolved":
                continue
            task = str(issue.get("recommendation") or issue.get("title") or "").strip()
            if task:
                items.append(
                    _plan_item(
                        task=task,
                        owner=None,
                        start_on=None,
                        due_on=None,
                        provenance=" | ".join(
                            str(value) for value in issue.get("evidence_refs") or []
                        ),
                    )
                )
    unique: dict[str, dict[str, str | None]] = {}
    for item in items:
        unique[str(item["item_key"])] = item
    return list(unique.values())[:100]


def _first_field(fields: dict[str, str], *names: str) -> str | None:
    for name in names:
        if fields.get(name):
            return fields[name]
    return None


def _date_field(fields: dict[str, str], *names: str) -> str | None:
    value = _first_field(fields, *names)
    if not value:
        return None
    match = re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)
    return value if match else None


def _plan_item(
    *,
    task: str,
    owner: str | None,
    start_on: str | None,
    due_on: str | None,
    provenance: str,
) -> dict[str, str | None]:
    item_key = sha256(
        "\x1f".join((task, owner or "", start_on or "", due_on or "", provenance)).encode()
    ).hexdigest()
    return {
        "item_key": item_key,
        "task": task,
        "owner": owner,
        "start_on": start_on,
        "due_on": due_on,
        "source_date": due_on or start_on,
        "provenance": provenance,
    }
