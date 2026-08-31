import httpx

from oslo_api.collaboration.asana import HttpAsanaGateway, executable_plan_items


def test_executable_plan_projection_excludes_assessment_and_read_fields() -> None:
    snapshot = {
        "summary": "Private OSLO read",
        "assessment": {"integrity": {"level": "Fragile"}, "issues": []},
        "artifacts": [
            {
                "title": "Schedule",
                "evidence_refs": ["document:plan:page:2"],
                "content": {
                    "sections": [
                        {
                            "heading": "Milestones",
                            "columns": ["Task", "Owner", "Start", "Due"],
                            "rows": [["Confirm launch", "Maya", "2026-09-01", "2026-09-03"]],
                            "row_evidence_refs": [["document:plan:page:3:fragment:2"]],
                        }
                    ]
                },
            }
        ],
    }

    items = executable_plan_items(snapshot)

    assert len(items) == 1
    assert items[0]["task"] == "Confirm launch"
    assert items[0]["owner"] == "Maya"
    assert items[0]["start_on"] == "2026-09-01"
    assert items[0]["due_on"] == "2026-09-03"
    assert items[0]["provenance"] == "document:plan:page:3:fragment:2"
    assert "summary" not in items[0]
    assert "assessment" not in items[0]


def test_asana_gateway_sends_only_executable_fields() -> None:
    captured: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["authorization"] = request.headers["authorization"]
        captured["body"] = request.read().decode()
        return httpx.Response(
            201,
            json={"data": {"gid": "task-1", "permalink_url": "https://app.asana.com/0/1/1"}},
        )

    gateway = HttpAsanaGateway(
        access_token="secret-token",
        destination_gid="project-1",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    result = gateway.create_task(
        {
            "item_key": "stable-key",
            "task": "Confirm launch",
            "owner": "Maya",
            "start_on": "2026-09-01",
            "due_on": "2026-09-03",
            "source_date": "2026-09-03",
            "provenance": "document:plan:page:3",
        }
    )

    assert result["gid"] == "task-1"
    assert captured["authorization"] == "Bearer secret-token"
    assert "Confirm launch" in captured["body"]
    assert "Private OSLO read" not in captured["body"]
    assert "Fragile" not in captured["body"]
