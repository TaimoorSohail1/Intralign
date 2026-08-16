from __future__ import annotations

import json
import re
from datetime import UTC, datetime, timedelta
from datetime import time as wall_time
from hashlib import sha256
from secrets import token_urlsafe
from threading import Event, Thread
from typing import Any
from urllib.parse import quote
from uuid import UUID
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from sqlalchemy import Connection, Engine, text

from oslo_api.analysis.history import append_history_event
from oslo_api.collaboration.asana import AsanaGateway, executable_plan_items


class CollaborationError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


def _freeze_public_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Return a self-consistent, public-safe projection of a retained read.

    The analysis summary can begin with the original free-text intake description.
    That description may be older than the documents which established the current
    project title.  A public snapshot must not expose that stale, cross-project
    preamble, so retain the governed analysis explanation and anchor it to the
    current snapshot title instead.
    """

    frozen = json.loads(json.dumps(snapshot))
    issues = frozen.get("assessment", {}).get("issues", [])
    open_issue_count = sum(
        1 for issue in issues if issue.get("status") != "resolved"
    )
    open_label = (
        f"{open_issue_count} open finding"
        f"{'s' if open_issue_count != 1 else ''}"
    )
    summary = frozen.get("summary")
    title = str(frozen.get("project_title") or "").strip()
    if isinstance(summary, str):
        analysis_detail = re.search(
            r"\bAt the (?:orientation|expanded|validated) stage,.*$",
            summary,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if title and analysis_detail:
            summary = f"{title}. {analysis_detail.group(0)}"
        summary = re.sub(
            r"\b\d+\s+open findings?\b",
            open_label,
            summary,
            count=1,
            flags=re.IGNORECASE,
        )
        frozen["summary"] = summary
    elif title:
        artifact_count = len(frozen.get("artifacts") or [])
        frozen["summary"] = (
            f"{title}. This retained read contains {artifact_count} plan artifacts "
            f"and {open_label}."
        )
    return frozen


class DatabaseCollaborationService:
    """Tenant-scoped collaboration boundary for R2 Slice 6.

    Analysis remains owned by Slice 2. This service owns principals, comments,
    bearer grants, review attestations and export audit records.
    """

    def __init__(
        self,
        engine: Engine,
        web_url: str,
        report_mailer: Any | None = None,
        review_mailer: Any | None = None,
        asana_gateway: AsanaGateway | None = None,
    ) -> None:
        self._engine = engine
        self._web_url = web_url.rstrip("/")
        self._report_mailer = report_mailer
        self._review_mailer = review_mailer if review_mailer is not None else report_mailer
        self._asana_gateway = asana_gateway
        self._report_worker_stop = Event()
        self._report_worker: Thread | None = None
        if report_mailer is not None:
            self._report_worker = Thread(
                target=self._report_delivery_loop,
                name="intralign-report-delivery",
                daemon=True,
            )
            self._report_worker.start()

    def state(self, *, actor_user_id: UUID, project_id: UUID) -> dict:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        with self._engine.connect() as connection:
            participants = [
                dict(row)
                for row in connection.execute(
                    text(
                        """
                        select m.user_id::text as id, p.display_name, m.role::text as role,
                               'member' as principal_type
                        from public.memberships m
                        join public.profiles p on p.id = m.user_id
                        where m.workspace_id = :workspace_id
                        order by lower(p.display_name)
                        """
                    ),
                    {"workspace_id": workspace_id},
                ).mappings()
            ]
            comments = [
                dict(row)
                for row in connection.execute(
                    text(
                        """
                        select c.id::text, c.issue_stable_key as issue_id, c.body, c.mentions,
                               c.created_at, p.display_name as author_name
                        from public.project_comments c
                        join public.profiles p on p.id = c.author_id
                        where c.project_id = :project_id
                        order by c.created_at
                        """
                    ),
                    {"project_id": project_id},
                ).mappings()
            ]
            reviews = [
                dict(row)
                for row in connection.execute(
                    text(
                        """
                        select g.id::text, g.issue_stable_key as issue_id, g.reviewer_name,
                               g.reviewer_email::text, g.expires_at, g.resolved_at, g.revoked_at,
                               g.question_text as question, g.source_ref, g.source_excerpt,
                               g.delivery_state::text, g.delivery_attempts, g.delivered_at,
                               g.responded_at, g.withdrawn_at, g.scope_kind::text,
                               r.id::text as response_id, r.response_kind::text,
                               r.body as response_body, r.analysis_run_id::text,
                               r.basis, r.evidence_ref, r.attributed_to,
                               r.created_at as response_created_at
                        from public.project_review_grants g
                        left join public.project_review_responses r on r.review_grant_id = g.id
                        where g.project_id = :project_id
                        order by g.created_at desc
                        """
                    ),
                    {"project_id": project_id},
                ).mappings()
            ]
            share_links = [
                dict(row)
                for row in connection.execute(
                    text(
                        """
                        select l.id::text, l.expires_at, l.revoked_at, l.created_at,
                               l.recipient_name, l.recipient_email::text,
                               v.first_viewed_at, v.last_viewed_at
                        from public.project_share_links l
                        left join public.project_snapshot_views v
                          on v.share_link_id = l.id
                        where l.project_id = :project_id
                        order by l.created_at desc
                        """
                    ),
                    {"project_id": project_id},
                ).mappings()
            ]
            plan_code = connection.execute(
                text(
                    """
                    select plan_code
                    from public.workspace_subscriptions
                    where workspace_id = :workspace_id
                    """
                ),
                {"workspace_id": workspace_id},
            ).scalar_one_or_none()
        return {
            "workspace_id": str(workspace_id),
            "project_id": str(project_id),
            "actor_role": role,
            "plan": {
                "name": "Basic" if plan_code == "basic" else "Free",
                "collaborators_unmetered": True,
                "invitations_unmetered": True,
                "viewers_unlimited": True,
                "reviewers_unmetered": True,
                "export_formats": ["pdf"],
            },
            "participants": participants,
            "comments": comments,
            "reviews": reviews,
            "share_links": share_links,
        }

    def roll_up(self, *, actor_user_id: UUID, project_id: UUID) -> dict:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        snapshot, statuses, reviewers = self._collaboration_projection_data(project_id)
        assessment = snapshot.get("assessment") or {}
        nodes = self._grounding_nodes(
            project_id,
            assessment.get("issues") or [],
            statuses,
            reviewers,
        )
        decision_queue = [node for node in nodes if node["state"] != "grounded"]
        decision_queue.sort(key=lambda item: item["exposure_rank"], reverse=True)
        integrity = assessment.get("integrity") or {
            "level": assessment.get("confidence_band", "Developing"),
            "limiting_pillar": "Grounding",
            "decomposition": [],
            "posture": "moment-in-time",
        }
        return {
            "workspace_id": str(workspace_id),
            "project_id": str(project_id),
            "actor_role": role,
            "integrity": integrity,
            "trend": assessment.get("confidence_direction", "unchanged"),
            "decision_queue": decision_queue,
            "reviewers": reviewers,
            "who_is_grounding_what": [
                {
                    "reviewer_name": reviewer["reviewer_name"],
                    "issue_id": reviewer["issue_id"],
                    "state": reviewer["delivery_state"],
                    "href": (
                        f"/projects/{project_id}/issues?issue="
                        f"{quote(str(reviewer['issue_id']), safe='')}"
                    ),
                }
                for reviewer in reviewers
                if reviewer["issue_id"]
            ],
            "rests_on": {
                state: sum(1 for node in nodes if node["state"] == state)
                for state in ("grounded", "addressed", "routed", "inferred")
            },
        }

    def grounding_map(self, *, actor_user_id: UUID, project_id: UUID) -> dict:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        snapshot, statuses, reviewers = self._collaboration_projection_data(project_id)
        issues = (snapshot.get("assessment") or {}).get("issues") or []
        nodes = self._grounding_nodes(project_id, issues, statuses, reviewers)
        return {
            "workspace_id": str(workspace_id),
            "project_id": str(project_id),
            "actor_role": role,
            "nodes": nodes,
            "counts": {
                state: sum(1 for node in nodes if node["state"] == state)
                for state in ("grounded", "addressed", "routed", "inferred")
            },
        }

    def _collaboration_projection_data(
        self,
        project_id: UUID,
    ) -> tuple[dict, dict[str, str], list[dict]]:
        with self._engine.connect() as connection:
            snapshot = connection.execute(
                text(
                    """
                    select snapshot_json from public.assessment_snapshots
                    where project_id = :project_id
                    order by published_at desc limit 1
                    """
                ),
                {"project_id": project_id},
            ).scalar_one_or_none()
            if snapshot is None:
                raise CollaborationError("NO_SNAPSHOT", "Analyze the project first", 409)
            statuses = {
                str(row["stable_key"]): str(row["current_status"])
                for row in connection.execute(
                    text(
                        """
                        select stable_key, current_status::text
                        from public.issues where project_id = :project_id
                        """
                    ),
                    {"project_id": project_id},
                ).mappings()
            }
            reviewers = [
                dict(row)
                for row in connection.execute(
                    text(
                        """
                        select g.id::text, g.issue_stable_key as issue_id,
                               g.reviewer_name, g.delivery_state::text,
                               g.expires_at, g.responded_at,
                               r.response_kind::text, r.analysis_run_id::text
                        from public.project_review_grants g
                        left join public.project_review_responses r
                          on r.review_grant_id = g.id
                        where g.project_id = :project_id
                          and g.revoked_at is null
                          and g.withdrawn_at is null
                        order by g.created_at desc
                        """
                    ),
                    {"project_id": project_id},
                ).mappings()
            ]
        return dict(snapshot), statuses, reviewers

    @staticmethod
    def _grounding_nodes(
        project_id: UUID,
        issues: list[dict],
        statuses: dict[str, str],
        reviewers: list[dict],
    ) -> list[dict]:
        routed_ids = {
            str(reviewer["issue_id"])
            for reviewer in reviewers
            if reviewer["issue_id"] and reviewer["responded_at"] is None
        }
        nodes: list[dict] = []
        for issue in issues:
            issue_id = str(issue.get("id") or "")
            current_status = statuses.get(issue_id, str(issue.get("status") or "open"))
            if current_status == "resolved":
                state = "grounded"
            elif current_status == "addressed":
                state = "addressed"
            elif issue_id in routed_ids or current_status == "routed":
                state = "routed"
            else:
                state = "inferred"
            nodes.append(
                {
                    "issue_id": issue_id,
                    "title": issue.get("title") or "Open issue",
                    "detail": issue.get("why") or issue.get("recommendation") or "",
                    "artifact_type": issue.get("artifact_type") or "project",
                    "pillar": issue.get("pillar") or "Grounding",
                    "state": state,
                    "exposure_rank": float(issue.get("exposure_rank") or 0),
                    "href": (
                        f"/projects/{project_id}/issues?issue="
                        f"{quote(issue_id, safe='')}"
                    ),
                }
            )
        return nodes

    def add_comment(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        issue_id: str,
        body: str,
        mentions: list[str],
    ) -> dict:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        self._require_editor(role)
        clean = body.strip()
        if not clean:
            raise CollaborationError("EMPTY_COMMENT", "Comment cannot be empty")
        with self._engine.begin() as connection:
            row = (
                connection.execute(
                    text(
                        """
                        insert into public.project_comments (
                          workspace_id, project_id, issue_stable_key, author_id, body, mentions
                        ) values (
                          :workspace_id, :project_id, :issue_id, :author_id, :body,
                          cast(:mentions as jsonb)
                        )
                        returning id::text, issue_stable_key as issue_id, body, mentions, created_at
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                        "issue_id": issue_id,
                        "author_id": actor_user_id,
                        "body": clean,
                        "mentions": json.dumps(mentions[:20]),
                    },
                )
                .mappings()
                .one()
            )
            normalized_mentions = {
                mention.strip().removeprefix("@").lower()
                for mention in mentions[:20]
                if mention.strip().removeprefix("@").strip()
            }
            members = list(
                connection.execute(
                    text(
                        """
                        select m.user_id, p.display_name, u.email::text
                        from public.memberships m
                        join public.profiles p on p.id = m.user_id
                        left join auth.users u on u.id = m.user_id
                        where m.workspace_id = :workspace_id
                        """
                    ),
                    {"workspace_id": workspace_id},
                ).mappings()
            )
            actor_name = next(
                (
                    member["display_name"]
                    for member in members
                    if member["user_id"] == actor_user_id
                ),
                "A teammate",
            )
            for member in members:
                email_local = str(member["email"] or "").split("@", 1)[0].lower()
                display_name = str(member["display_name"] or "").strip().lower()
                aliases = {
                    display_name,
                    display_name.replace(" ", "-"),
                    display_name.replace(" ", "."),
                    email_local,
                }
                if (
                    member["user_id"] == actor_user_id
                    or not normalized_mentions.intersection(aliases)
                ):
                    continue
                notification_payload = {
                    "project_id": str(project_id),
                    "issue_id": issue_id,
                    "comment_id": row["id"],
                    "actor_name": actor_name,
                    "recipient_user_id": str(member["user_id"]),
                    "salience": "miss_worthy",
                }
                connection.execute(
                    text(
                        """
                        insert into public.outbox_events (
                          workspace_id, aggregate_type, aggregate_id, event_type, payload
                        ) values (
                          :workspace_id, 'comment', :comment_id,
                          'notify.direct_mention', cast(:payload as jsonb)
                        )
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "comment_id": row["id"],
                        "payload": json.dumps(notification_payload),
                    },
                )
            self._append_collaboration_history(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                actor_user_id=actor_user_id,
                event_type="collaboration.comment_added",
                summary="Comment added",
                detail=f"A project comment was added to {issue_id}.",
                issue_id=issue_id,
                payload={"comment_id": row["id"], "mentions": mentions[:20]},
                idempotency_key=f"collaboration:comment:{row['id']}",
            )
        return {**dict(row), "author_name": actor_name}

    def create_snapshot_link(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        recipient_name: str,
        recipient_email: str | None,
    ) -> dict:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        self._require_editor(role)
        recipient = recipient_name.strip()
        if not recipient:
            raise CollaborationError("RECIPIENT_REQUIRED", "Snapshot recipient name is required")
        raw = token_urlsafe(32)
        expires_at = datetime.now(UTC) + timedelta(days=30)
        with self._engine.begin() as connection:
            snapshot_row = (
                connection.execute(
                    text(
                        """
                        select id, snapshot_json from public.assessment_snapshots
                        where project_id = :project_id
                        order by published_at desc limit 1
                        """
                    ),
                    {"project_id": project_id},
                )
                .mappings()
                .one_or_none()
            )
            if snapshot_row is None:
                raise CollaborationError("NO_SNAPSHOT", "Analyze the project before sharing", 409)
            snapshot_id = snapshot_row["id"]
            frozen_snapshot = json.loads(json.dumps(snapshot_row["snapshot_json"]))
            lifecycle_statuses = dict(
                connection.execute(
                    text(
                        """
                        select stable_key, current_status::text
                        from public.issues
                        where project_id = :project_id
                        """
                    ),
                    {"project_id": project_id},
                ).all()
            )
            for issue in frozen_snapshot.get("assessment", {}).get("issues", []):
                issue_id = str(issue.get("id") or "")
                if issue_id in lifecycle_statuses:
                    issue["status"] = lifecycle_statuses[issue_id]
            frozen_snapshot = _freeze_public_snapshot(frozen_snapshot)
            link_id = connection.execute(
                text(
                    """
                    insert into public.project_share_links (
                      workspace_id, project_id, snapshot_id, token_hash, created_by, expires_at,
                      recipient_name, recipient_email, frozen_snapshot_json
                    ) values (
                      :workspace_id, :project_id, :snapshot_id, :token_hash,
                      :created_by, :expires_at, :recipient_name, :recipient_email,
                      cast(:frozen_snapshot_json as jsonb)
                    ) returning id
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "snapshot_id": snapshot_id,
                    "token_hash": sha256(raw.encode()).digest(),
                    "created_by": actor_user_id,
                    "expires_at": expires_at,
                    "recipient_name": recipient,
                    "recipient_email": recipient_email.strip() if recipient_email else None,
                    "frozen_snapshot_json": json.dumps(frozen_snapshot),
                },
            ).scalar_one()
            self._append_collaboration_history(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                actor_user_id=actor_user_id,
                event_type="share.created",
                summary="Frozen snapshot shared",
                detail=f"A frozen read-only snapshot was created for {recipient}.",
                payload={"share_link_id": str(link_id), "recipient_name": recipient},
                idempotency_key=f"collaboration:share:{link_id}:created",
            )
        return {
            "id": str(link_id),
            "url": f"{self._web_url}/share/{raw}",
            "expires_at": expires_at,
            "recipient_name": recipient,
        }

    def create_review_grant(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        issue_id: str | None,
        reviewer_name: str,
        reviewer_email: str | None,
        question: str,
        source_ref: str,
        source_excerpt: str,
    ) -> dict:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        self._require_editor(role)
        name = reviewer_name.strip()
        if not name:
            raise CollaborationError("REVIEWER_REQUIRED", "Reviewer name is required")
        clean_question = question.strip()
        clean_source_ref = source_ref.strip()
        clean_source_excerpt = source_excerpt.strip()
        if not issue_id or not clean_question or not clean_source_ref or not clean_source_excerpt:
            raise CollaborationError(
                "REVIEW_SCOPE_REQUIRED",
                "A scoped review requires one issue, question, and cited source",
            )
        raw = token_urlsafe(32)
        expires_at = datetime.now(UTC) + timedelta(days=7)
        with self._engine.begin() as connection:
            issue_exists = connection.execute(
                text(
                    """
                    select exists(
                      select 1 from public.issues
                      where project_id = :project_id
                        and stable_key = :issue_id
                        and current_status <> 'resolved'
                    )
                    """
                ),
                {"project_id": project_id, "issue_id": issue_id},
            ).scalar_one()
            if not issue_exists:
                raise CollaborationError(
                    "REVIEW_ISSUE_UNAVAILABLE",
                    "The selected issue is not available for external review",
                    409,
                )
            prior_grants = list(
                connection.execute(
                    text(
                        """
                        update public.project_review_grants
                        set revoked_at = coalesce(revoked_at, now()),
                            withdrawn_at = coalesce(withdrawn_at, now()),
                            delivery_state = 'withdrawn'
                        where project_id = :project_id
                          and issue_stable_key = :issue_id
                          and scope_kind = 'scoped'
                          and revoked_at is null
                          and withdrawn_at is null
                        returning id::text
                        """
                    ),
                    {"project_id": project_id, "issue_id": issue_id},
                ).scalars()
            )
            token_version = connection.execute(
                text(
                    """
                    select coalesce(max(token_version), 0) + 1
                    from public.project_review_grants
                    where project_id = :project_id and issue_stable_key = :issue_id
                    """
                ),
                {"project_id": project_id, "issue_id": issue_id},
            ).scalar_one()
            grant_id = connection.execute(
                text(
                    """
                    insert into public.project_review_grants (
                      workspace_id, project_id, issue_stable_key, reviewer_name,
                      reviewer_email, token_hash, created_by, expires_at,
                      scope_kind, question_text, source_ref, source_excerpt,
                      delivery_state, token_version
                    ) values (
                      :workspace_id, :project_id, :issue_id, :reviewer_name,
                      :reviewer_email, :token_hash, :created_by, :expires_at,
                      'scoped', :question, :source_ref, :source_excerpt,
                      'draft', :token_version
                    ) returning id
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "issue_id": issue_id,
                    "reviewer_name": name,
                    "reviewer_email": reviewer_email.strip() if reviewer_email else None,
                    "token_hash": sha256(raw.encode()).digest(),
                    "created_by": actor_user_id,
                    "expires_at": expires_at,
                    "question": clean_question,
                    "source_ref": clean_source_ref,
                    "source_excerpt": clean_source_excerpt,
                    "token_version": token_version,
                },
            ).scalar_one()
            self._append_collaboration_history(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                actor_user_id=actor_user_id,
                event_type="review.requested",
                summary="Scoped review drafted",
                detail=f"A one-question review link was prepared for {name}.",
                issue_id=issue_id,
                payload={
                    "review_grant_id": str(grant_id),
                    "reviewer_name": name,
                    "scope_kind": "scoped",
                    "delivery_state": "draft",
                },
                idempotency_key=f"collaboration:review:{grant_id}:created",
            )
            if prior_grants:
                self._append_collaboration_history(
                    connection,
                    workspace_id=workspace_id,
                    project_id=project_id,
                    actor_user_id=actor_user_id,
                    event_type="review.rerouted",
                    summary="Scoped review rerouted",
                    detail="The previous scoped link was withdrawn before a new link was issued.",
                    issue_id=issue_id,
                    payload={
                        "review_grant_id": str(grant_id),
                        "withdrawn_grant_ids": prior_grants,
                        "token_version": token_version,
                    },
                    idempotency_key=f"collaboration:review:{grant_id}:rerouted",
                )
        url = f"{self._web_url}/review/{raw}"
        delivery = {
            "delivery_state": "draft",
            "delivery_attempts": 0,
            "delivered_at": None,
        }
        if reviewer_email:
            delivery = self._deliver_review_by_email(
                actor_user_id=actor_user_id,
                project_id=project_id,
                grant_id=grant_id,
                reviewer_name=name,
                reviewer_email=reviewer_email.strip(),
                question=clean_question,
                source_ref=clean_source_ref,
                url=url,
            )
        return {
            "id": str(grant_id),
            "url": url,
            "expires_at": expires_at,
            **delivery,
        }

    def _deliver_review_by_email(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        grant_id: UUID,
        reviewer_name: str,
        reviewer_email: str,
        question: str,
        source_ref: str,
        url: str,
    ) -> dict:
        attempts = 0
        delivered = False
        last_error = "REVIEW_DELIVERY_UNAVAILABLE"
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.project_review_grants
                    set delivery_state = 'sending'
                    where id = :grant_id and project_id = :project_id
                    """
                ),
                {"grant_id": grant_id, "project_id": project_id},
            )
        if self._review_mailer is not None:
            for attempt_number in range(1, 4):
                attempts = attempt_number
                try:
                    self._review_mailer.send_report(
                        email=reviewer_email,
                        subject="You have one evidence question from Intralign",
                        project_name="Scoped evidence review",
                        recipient_label=reviewer_name,
                        sections=[
                            {"title": "Question", "body": [question]},
                            {"title": "Cited source", "body": [source_ref]},
                            {"title": "Open the secure review", "body": [url]},
                        ],
                    )
                    delivered = True
                    break
                except Exception as error:  # provider boundary; link remains usable
                    last_error = type(error).__name__
        with self._engine.begin() as connection:
            delivered_at = datetime.now(UTC) if delivered else None
            delivery_state = "awaiting" if delivered else "failed"
            connection.execute(
                text(
                    """
                    update public.project_review_grants
                    set delivery_state = cast(:delivery_state as public.review_delivery_state),
                        delivery_attempts = :attempts,
                        delivered_at = :delivered_at
                    where id = :grant_id and project_id = :project_id
                    """
                ),
                {
                    "delivery_state": delivery_state,
                    "attempts": attempts,
                    "delivered_at": delivered_at,
                    "grant_id": grant_id,
                    "project_id": project_id,
                },
            )
            workspace_id = connection.execute(
                text(
                    "select workspace_id from public.project_review_grants where id = :grant_id"
                ),
                {"grant_id": grant_id},
            ).scalar_one()
            event_type = "review.delivered" if delivered else "review.delivery_failed"
            payload = {
                "project_id": str(project_id),
                "review_grant_id": str(grant_id),
                "delivery_state": delivery_state,
                "delivery_attempts": attempts,
                "channel": "email",
            }
            if not delivered:
                payload["error_code"] = last_error
            connection.execute(
                text(
                    """
                    insert into public.outbox_events (
                      workspace_id, aggregate_type, aggregate_id, event_type, payload
                    ) values (
                      :workspace_id, 'review_request', :grant_id,
                      :event_type, cast(:payload as jsonb)
                    )
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "grant_id": grant_id,
                    "event_type": event_type,
                    "payload": json.dumps(payload),
                },
            )
            self._append_collaboration_history(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                actor_user_id=actor_user_id,
                event_type=event_type,
                summary=("Scoped review delivered" if delivered else "Review delivery failed"),
                detail=(
                    f"{reviewer_name} was sent one question and its cited source."
                    if delivered
                    else (
                        "Email delivery failed after three attempts; the secure "
                        "copy-link fallback remains available."
                    )
                ),
                payload=payload,
                idempotency_key=f"collaboration:review:{grant_id}:{event_type}",
            )
        return {
            "delivery_state": delivery_state,
            "delivery_attempts": attempts,
            "delivered_at": delivered_at,
        }

    def mark_review_delivered(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        grant_id: UUID,
    ) -> dict:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        self._require_editor(role)
        with self._engine.begin() as connection:
            row = (
                connection.execute(
                    text(
                        """
                        update public.project_review_grants
                        set delivery_state = case
                              when delivery_state in ('answered', 'withdrawn') then delivery_state
                              else 'awaiting'::public.review_delivery_state
                            end,
                            delivered_at = coalesce(delivered_at, now())
                        where id = :grant_id and project_id = :project_id
                          and workspace_id = :workspace_id
                          and revoked_at is null and withdrawn_at is null
                        returning id::text, delivery_state::text, delivery_attempts,
                                  delivered_at
                        """
                    ),
                    {
                        "grant_id": grant_id,
                        "project_id": project_id,
                        "workspace_id": workspace_id,
                    },
                )
                .mappings()
                .one_or_none()
            )
            if row is None:
                raise CollaborationError(
                    "REVIEW_NOT_FOUND", "Review request was not found", 404
                )
            payload = {
                "project_id": str(project_id),
                "review_grant_id": str(grant_id),
                "delivery_state": row["delivery_state"],
                "channel": "manual_copy",
            }
            connection.execute(
                text(
                    """
                    insert into public.outbox_events (
                      workspace_id, aggregate_type, aggregate_id, event_type, payload
                    ) values (
                      :workspace_id, 'review_request', :grant_id,
                      'review.delivered', cast(:payload as jsonb)
                    )
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "grant_id": grant_id,
                    "payload": json.dumps(payload),
                },
            )
            self._append_collaboration_history(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                actor_user_id=actor_user_id,
                event_type="review.delivered",
                summary="Scoped review handed off",
                detail="The secure scoped link was copied for manual delivery.",
                payload=payload,
                idempotency_key=f"collaboration:review:{grant_id}:manual-delivery",
            )
        return dict(row)

    def resolve_snapshot(self, token: str) -> dict:
        self._forbid_cross_scope(token=token, expected="snapshot")
        with self._engine.begin() as connection:
            row = (
                connection.execute(
                    text(
                        """
                        select l.id as share_link_id, l.workspace_id, l.project_id,
                               l.recipient_name,
                               coalesce(
                                 nullif(s.snapshot_json ->> 'project_title', ''),
                                 p.name
                               ) as project_name,
                               coalesce(l.frozen_snapshot_json, s.snapshot_json) as snapshot_json,
                               s.snapshot_state, s.published_at, l.expires_at
                        from public.project_share_links l
                        join public.projects p on p.id = l.project_id
                        join public.assessment_snapshots s on s.id = l.snapshot_id
                        where l.token_hash = :token_hash and l.revoked_at is null
                          and l.expires_at > now()
                        """
                    ),
                    {"token_hash": sha256(token.encode()).digest()},
                )
                .mappings()
                .one_or_none()
            )
            if row is None:
                raise CollaborationError(
                    "LINK_UNAVAILABLE",
                    "This snapshot link is invalid or expired",
                    404,
                )
            first_view = connection.execute(
                text(
                    """
                    insert into public.project_snapshot_views (
                      workspace_id, project_id, share_link_id, recipient_label
                    ) values (
                      :workspace_id, :project_id, :share_link_id, :recipient_label
                    )
                    on conflict (share_link_id) do update
                    set last_viewed_at = now()
                    returning (xmax = 0) as first_view
                    """
                ),
                {
                    "workspace_id": row["workspace_id"],
                    "project_id": row["project_id"],
                    "share_link_id": row["share_link_id"],
                    "recipient_label": row["recipient_name"] or "Named recipient",
                },
            ).scalar_one()
            if first_view:
                connection.execute(
                    text(
                        """
                        insert into public.outbox_events (
                          workspace_id, aggregate_type, aggregate_id, event_type, payload
                        ) values (
                          :workspace_id, 'shared_snapshot', :share_link_id,
                          'snapshot.viewed', cast(:payload as jsonb)
                        )
                        """
                    ),
                    {
                        "workspace_id": row["workspace_id"],
                        "share_link_id": row["share_link_id"],
                        "payload": json.dumps(
                            {
                                "project_id": str(row["project_id"]),
                                "share_link_id": str(row["share_link_id"]),
                                "recipient_label": row["recipient_name"]
                                or "Named recipient",
                                "audit_scope": "first_and_latest_only",
                            }
                        ),
                    },
                )
        return {
            "project_name": row["project_name"],
            "recipient_name": row["recipient_name"],
            "snapshot_json": row["snapshot_json"],
            "snapshot_state": row["snapshot_state"],
            "published_at": row["published_at"],
            "expires_at": row["expires_at"],
            "view_audit_disclosure": "First and latest view times are retained for 90 days.",
        }

    def resolve_review(self, token: str) -> dict:
        self._forbid_cross_scope(token=token, expected="review")
        with self._engine.connect() as connection:
            row = (
                connection.execute(
                    text(
                        """
                        select g.id::text, g.reviewer_name, g.expires_at,
                               g.question_text as question, g.source_ref,
                               g.source_excerpt,
                               coalesce(
                                 nullif(latest.snapshot_json ->> 'project_title', ''),
                                 p.name
                               ) as project_name,
                               r.response_kind::text as response_kind
                        from public.project_review_grants g
                        join public.projects p on p.id = g.project_id
                        left join lateral (
                          select s.snapshot_json
                          from public.assessment_snapshots s
                          where s.project_id = g.project_id
                          order by s.published_at desc
                          limit 1
                        ) latest on true
                        left join public.project_review_responses r on r.review_grant_id = g.id
                        where g.token_hash = :token_hash and g.revoked_at is null
                          and g.withdrawn_at is null
                          and g.expires_at > now()
                          and g.scope_kind = 'scoped'
                          and not exists (
                            select 1 from public.issues i
                            where i.project_id = g.project_id
                              and i.stable_key = g.issue_stable_key
                              and i.current_status = 'resolved'
                          )
                        """
                    ),
                    {"token_hash": sha256(token.encode()).digest()},
                )
                .mappings()
                .one_or_none()
            )
        if row is None:
            raise CollaborationError(
                "REVIEW_UNAVAILABLE",
                "This review request is invalid or expired",
                404,
            )
        return {
            "id": row["id"],
            "reviewer_name": row["reviewer_name"],
            "project_name": row["project_name"],
            "expires_at": row["expires_at"],
            "question": row["question"],
            "source": {
                "reference": row["source_ref"],
                "excerpt": row["source_excerpt"],
            },
            "response_kind": row["response_kind"],
        }

    def _forbid_cross_scope(self, *, token: str, expected: str) -> None:
        digest = sha256(token.encode()).digest()
        other_table = (
            "public.project_review_grants"
            if expected == "snapshot"
            else "public.project_share_links"
        )
        with self._engine.connect() as connection:
            exists = connection.execute(
                text(f"select exists(select 1 from {other_table} where token_hash = :token_hash)"),
                {"token_hash": digest},
            ).scalar_one()
        if exists:
            raise CollaborationError(
                "TOKEN_SCOPE_FORBIDDEN",
                "This access token is not valid for that resource",
                403,
            )

    def respond_to_review(self, *, token: str, kind: str, body: str) -> dict:
        allowed = {"comment", "approve", "reject", "suggest_alternative"}
        if kind not in allowed:
            raise CollaborationError("INVALID_RESPONSE", "Choose a supported review response")
        clean = body.strip()
        if not clean:
            raise CollaborationError("EMPTY_RESPONSE", "A review note is required")
        digest = sha256(token.encode()).digest()
        with self._engine.begin() as connection:
            grant = (
                connection.execute(
                    text(
                        """
                        select * from public.project_review_grants
                        where token_hash = :token_hash and revoked_at is null
                          and withdrawn_at is null and expires_at > now()
                        for update
                        """
                    ),
                    {"token_hash": digest},
                )
                .mappings()
                .one_or_none()
            )
            if grant is None:
                raise CollaborationError(
                    "REVIEW_UNAVAILABLE",
                    "This review request is invalid or expired",
                    404,
                )
            existing = (
                connection.execute(
                    text(
                        """
                        select id, response_kind::text as response_kind, body,
                               analysis_run_id
                        from public.project_review_responses
                        where review_grant_id = :grant_id
                        """
                    ),
                    {"grant_id": grant["id"]},
                )
                .mappings()
                .one_or_none()
            )
            if existing is not None:
                if existing["analysis_run_id"] is not None:
                    raise CollaborationError(
                        "ALREADY_RESPONDED",
                        "This review has already been submitted",
                        409,
                    )
                response_id = existing["id"]
                kind = existing["response_kind"]
                clean = existing["body"]
            else:
                response_id = connection.execute(
                    text(
                        """
                        insert into public.project_review_responses (
                          workspace_id, project_id, review_grant_id, issue_stable_key,
                          response_kind, body, basis, evidence_ref, attributed_to,
                          idempotency_key
                        ) values (
                          :workspace_id, :project_id, :grant_id, :issue_id,
                          cast(:kind as public.review_response_kind), :body,
                          :basis, :evidence_ref, cast(:attributed_to as jsonb),
                          :idempotency_key
                        ) returning id
                        """
                    ),
                    {
                        "workspace_id": grant["workspace_id"],
                        "project_id": grant["project_id"],
                        "grant_id": grant["id"],
                        "issue_id": grant["issue_stable_key"],
                        "kind": kind,
                        "body": clean,
                        "basis": "answered" if kind in {"approve", "reject"} else None,
                        "evidence_ref": (
                            grant["source_ref"] if kind in {"approve", "reject"} else None
                        ),
                        "attributed_to": json.dumps(
                            {
                                "display_name": grant["reviewer_name"],
                                "role": "external",
                            }
                        ),
                        "idempotency_key": f"review:{grant['id']}",
                    },
                ).scalar_one()
                connection.execute(
                    text(
                        """
                        update public.project_review_grants
                        set responded_at = coalesce(responded_at, now()),
                            delivery_state = 'answered'
                        where id = :grant_id
                        """
                    ),
                    {"grant_id": grant["id"]},
                )
        return {
            "id": str(response_id),
            "project_id": str(grant["project_id"]),
            "issue_id": grant["issue_stable_key"],
            "response_kind": kind,
            "body": clean,
            "created_by": str(grant["created_by"]),
            "reviewer_name": grant["reviewer_name"],
        }

    def link_review_run(self, *, response_id: UUID, run_id: UUID | None) -> None:
        with self._engine.begin() as connection:
            response = (
                connection.execute(
                    text(
                        """
                        select r.workspace_id, r.project_id, r.review_grant_id,
                               r.issue_stable_key, r.response_kind::text as response_kind,
                               g.reviewer_name, g.reviewer_email::text, g.created_by
                        from public.project_review_responses r
                        join public.project_review_grants g on g.id = r.review_grant_id
                        where r.id = :response_id
                        for update
                        """
                    ),
                    {"response_id": response_id},
                )
                .mappings()
                .one_or_none()
            )
            if response is None:
                raise CollaborationError(
                    "REVIEW_RESPONSE_NOT_FOUND",
                    "The reviewer response could not be linked",
                    404,
                )
            connection.execute(
                text(
                    """
                    update public.project_review_responses
                    set analysis_run_id = :run_id
                    where id = :response_id
                    """
                ),
                {"response_id": response_id, "run_id": run_id},
            )
            connection.execute(
                text(
                    """
                    update public.project_review_grants
                    set resolved_at = coalesce(resolved_at, now())
                    where id = :grant_id
                    """
                ),
                {"grant_id": response["review_grant_id"]},
            )
            event_payload = {
                "project_id": str(response["project_id"]),
                "issue_id": response["issue_stable_key"],
                "reviewer_name": response["reviewer_name"],
                "response_kind": response["response_kind"],
                "analysis_run_id": str(run_id) if run_id else None,
                "salience": "miss_worthy",
            }
            for event_type in ("review.responded", "notify.routed_response"):
                connection.execute(
                    text(
                        """
                        insert into public.outbox_events (
                          workspace_id, aggregate_type, aggregate_id, event_type, payload
                        ) values (
                          :workspace_id, 'review_response', :response_id,
                          :event_type, cast(:payload as jsonb)
                        )
                        """
                    ),
                    {
                        "workspace_id": response["workspace_id"],
                        "response_id": response_id,
                        "event_type": event_type,
                        "payload": json.dumps(event_payload),
                    },
                )
            response_copy = {
                "approve": (
                    "Reviewer confirmed",
                    "submitted a confirmation response.",
                ),
                "reject": (
                    "Reviewer rejected",
                    "submitted a rejection response.",
                ),
                "comment": (
                    "Reviewer commented",
                    "submitted a comment.",
                ),
                "suggest_alternative": (
                    "Reviewer suggested an alternative",
                    "submitted an alternative suggestion.",
                ),
            }
            response_summary, response_detail = response_copy[response["response_kind"]]
            self._append_collaboration_history(
                connection,
                workspace_id=response["workspace_id"],
                project_id=response["project_id"],
                actor_user_id=response["created_by"],
                event_type=f"collaboration.reviewer_{response['response_kind']}",
                summary=response_summary,
                detail=f"{response['reviewer_name']} {response_detail}",
                issue_id=response["issue_stable_key"],
                payload=event_payload,
                idempotency_key=f"collaboration:review-response:{response_id}",
            )
            if (
                response["reviewer_email"]
                and response["response_kind"] in {"approve", "reject"}
            ):
                invite_payload = {
                    "project_id": str(response["project_id"]),
                    "review_response_id": str(response_id),
                    "reviewer_name": response["reviewer_name"],
                    "reviewer_email": response["reviewer_email"],
                    "state": "draft",
                }
                connection.execute(
                    text(
                        """
                        insert into public.outbox_events (
                          workspace_id, aggregate_type, aggregate_id, event_type, payload
                        ) values (
                          :workspace_id, 'review_response', :response_id,
                          'invite.drafted', cast(:payload as jsonb)
                        )
                        """
                    ),
                    {
                        "workspace_id": response["workspace_id"],
                        "response_id": response_id,
                        "payload": json.dumps(invite_payload),
                    },
                )
                self._append_collaboration_history(
                    connection,
                    workspace_id=response["workspace_id"],
                    project_id=response["project_id"],
                    actor_user_id=response["created_by"],
                    event_type="invite.drafted",
                    summary="Collaborator invitation drafted",
                    detail=(
                        "OSLO prepared an optional invitation after the attributed "
                        "review response. Nothing was sent."
                    ),
                    issue_id=response["issue_stable_key"],
                    payload=invite_payload,
                    idempotency_key=f"collaboration:invite-draft:{response_id}",
                )

    def review_response_for_evidence(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        response_id: UUID,
    ) -> dict:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        self._require_editor(role)
        with self._engine.connect() as connection:
            response = (
                connection.execute(
                    text(
                        """
                        select r.id::text, r.project_id::text, r.issue_stable_key as issue_id,
                               r.response_kind::text, r.body,
                               r.analysis_run_id::text,
                               g.reviewer_name, g.created_by::text
                        from public.project_review_responses r
                        join public.project_review_grants g on g.id = r.review_grant_id
                        where r.id = :response_id
                          and r.project_id = :project_id
                          and r.workspace_id = :workspace_id
                        """
                    ),
                    {
                        "response_id": response_id,
                        "project_id": project_id,
                        "workspace_id": workspace_id,
                    },
                )
                .mappings()
                .one_or_none()
            )
        if response is None:
            raise CollaborationError(
                "REVIEW_RESPONSE_NOT_FOUND",
                "The reviewer response could not be found",
                404,
            )
        if response["analysis_run_id"] is not None:
            raise CollaborationError(
                "REVIEW_RESPONSE_ALREADY_PROMOTED",
                "This reviewer response is already project evidence",
                409,
            )
        return dict(response)

    def revoke_share_link(
        self, *, actor_user_id: UUID, project_id: UUID, link_id: UUID
    ) -> None:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        self._require_editor(role)
        with self._engine.begin() as connection:
            result = connection.execute(
                text(
                    """
                    update public.project_share_links
                    set revoked_at = coalesce(revoked_at, now())
                    where id = :link_id and project_id = :project_id
                      and workspace_id = :workspace_id
                    """
                ),
                {
                    "link_id": link_id,
                    "project_id": project_id,
                    "workspace_id": workspace_id,
                },
            )
            if result.rowcount != 1:
                raise CollaborationError("LINK_NOT_FOUND", "Share link was not found", 404)
            self._append_collaboration_history(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                actor_user_id=actor_user_id,
                event_type="share.revoked",
                summary="Snapshot share revoked",
                detail="A read-only project snapshot link was revoked.",
                payload={"share_link_id": str(link_id)},
                idempotency_key=f"collaboration:share:{link_id}:revoked",
            )

    def revoke_review_grant(
        self, *, actor_user_id: UUID, project_id: UUID, grant_id: UUID
    ) -> None:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        self._require_editor(role)
        with self._engine.begin() as connection:
            result = connection.execute(
                text(
                    """
                    update public.project_review_grants
                    set revoked_at = coalesce(revoked_at, now()),
                        withdrawn_at = coalesce(withdrawn_at, now()),
                        delivery_state = 'withdrawn'
                    where id = :grant_id and project_id = :project_id
                      and workspace_id = :workspace_id
                    """
                ),
                {
                    "grant_id": grant_id,
                    "project_id": project_id,
                    "workspace_id": workspace_id,
                },
            )
            if result.rowcount != 1:
                raise CollaborationError("REVIEW_NOT_FOUND", "Review request was not found", 404)
            self._append_collaboration_history(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                actor_user_id=actor_user_id,
                event_type="review.withdrawn",
                summary="Scoped review withdrawn",
                detail="The scoped review link was withdrawn; its history was retained.",
                payload={"review_grant_id": str(grant_id)},
                idempotency_key=f"collaboration:review:{grant_id}:revoked",
            )

    def record_export(self, *, actor_user_id: UUID, project_id: UUID) -> dict:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        self._require_editor(role)
        with self._engine.begin() as connection:
            row = (
                connection.execute(
                    text(
                        """
                        select p.name as project_name, s.id as snapshot_id, s.snapshot_json,
                               s.snapshot_state, s.published_at
                        from public.projects p
                        join lateral (
                          select id, snapshot_json, snapshot_state, published_at
                          from public.assessment_snapshots
                          where project_id = p.id order by published_at desc limit 1
                        ) s on true
                        where p.id = :project_id
                        """
                    ),
                    {"project_id": project_id},
                )
                .mappings()
                .one_or_none()
            )
            if row is None:
                raise CollaborationError("NO_SNAPSHOT", "Analyze the project before exporting", 409)
            export_id = connection.execute(
                text(
                    """
                    insert into public.project_exports (
                      workspace_id, project_id, snapshot_id, exported_by, format
                    ) values (:workspace_id, :project_id, :snapshot_id, :exported_by, 'pdf')
                    returning id
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "snapshot_id": row["snapshot_id"],
                    "exported_by": actor_user_id,
                },
            ).scalar_one()
            self._append_collaboration_history(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                actor_user_id=actor_user_id,
                event_type="collaboration.snapshot_exported",
                summary="Project snapshot exported",
                detail="A governed PDF export was generated from the current snapshot.",
                payload={"export_id": str(export_id), "format": "pdf"},
                idempotency_key=f"collaboration:export:{export_id}",
            )
        return dict(row)

    @staticmethod
    def _next_weekly_run(
        *, weekday: int, local_time: wall_time, timezone: str, after: datetime
    ) -> datetime:
        try:
            zone = ZoneInfo(timezone)
        except ZoneInfoNotFoundError as error:
            raise CollaborationError(
                "INVALID_TIMEZONE", "Choose a valid IANA timezone.", 422
            ) from error
        local_after = after.astimezone(zone)
        days_ahead = (weekday - local_after.weekday()) % 7
        candidate = datetime.combine(
            local_after.date() + timedelta(days=days_ahead),
            local_time,
            tzinfo=zone,
        )
        if candidate <= local_after:
            candidate += timedelta(days=7)
        return candidate.astimezone(UTC)

    def report_schedules(self, *, actor_user_id: UUID, project_id: UUID) -> list[dict]:
        workspace_id, _role = self._project_access(actor_user_id, project_id)
        with self._engine.connect() as connection:
            rows = connection.execute(
                text(
                    """
                    select id::text, recipient_email::text, recipient_class,
                           weekday, local_time::text, timezone, state,
                           next_run_at, last_run_at, last_delivery_id::text,
                           created_at, updated_at
                    from public.project_report_schedules
                    where project_id = :project_id and workspace_id = :workspace_id
                    order by created_at desc
                    """
                ),
                {"project_id": project_id, "workspace_id": workspace_id},
            ).mappings()
        return [dict(row) for row in rows]

    def asana_handoff_state(
        self, *, actor_user_id: UUID, project_id: UUID
    ) -> dict:
        workspace_id, _role = self._project_access(actor_user_id, project_id)
        with self._engine.connect() as connection:
            subscription = connection.execute(
                text(
                    """
                    select plan_code, status
                    from public.workspace_subscriptions
                    where workspace_id = :workspace_id
                    """
                ),
                {"workspace_id": workspace_id},
            ).mappings().one_or_none()
            current = connection.execute(
                text(
                    """
                    select snapshot.id::text as snapshot_id, snapshot.snapshot_json
                    from public.projects project
                    join public.assessment_snapshots snapshot
                      on snapshot.analysis_run_id = project.current_analysis_run_id
                    where project.id = :project_id
                      and project.workspace_id = :workspace_id
                    """
                ),
                {"project_id": project_id, "workspace_id": workspace_id},
            ).mappings().one_or_none()
            latest = connection.execute(
                text(
                    """
                    select id::text, state, total_count, completed_count,
                           safe_error_code, destination_gid, created_at, updated_at
                    from public.project_asana_handoffs
                    where project_id = :project_id and workspace_id = :workspace_id
                    order by created_at desc
                    limit 1
                    """
                ),
                {"project_id": project_id, "workspace_id": workspace_id},
            ).mappings().one_or_none()
        if current is None:
            raise CollaborationError("NO_SNAPSHOT", "Analyze before importing.", 409)
        plan_active = bool(
            subscription
            and subscription["plan_code"] == "basic"
            and subscription["status"] in {"active", "grace"}
        )
        preview = executable_plan_items(dict(current["snapshot_json"]))
        return {
            "configured": self._asana_gateway is not None,
            "entitled": plan_active,
            "destination_gid": (
                self._asana_gateway.destination_gid if self._asana_gateway else None
            ),
            "snapshot_id": current["snapshot_id"],
            "preview": preview,
            "latest": dict(latest) if latest else None,
        }

    def import_asana_handoff(
        self, *, actor_user_id: UUID, project_id: UUID
    ) -> dict:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        self._require_editor(role)
        if self._asana_gateway is None:
            raise CollaborationError(
                "ASANA_NOT_CONNECTED",
                "Connect an Asana project before importing. Manual exports remain available.",
                409,
            )
        with self._engine.begin() as connection:
            subscription = connection.execute(
                text(
                    """
                    select plan_code, status
                    from public.workspace_subscriptions
                    where workspace_id = :workspace_id
                    """
                ),
                {"workspace_id": workspace_id},
            ).mappings().one_or_none()
            if not subscription or subscription["plan_code"] != "basic" or subscription[
                "status"
            ] not in {"active", "grace"}:
                raise CollaborationError(
                    "BASIC_REQUIRED",
                    "Asana hand-off requires the Basic plan. Manual exports remain free.",
                    402,
                )
            current = connection.execute(
                text(
                    """
                    select snapshot.id, snapshot.analysis_run_id, snapshot.snapshot_json
                    from public.projects project
                    join public.assessment_snapshots snapshot
                      on snapshot.analysis_run_id = project.current_analysis_run_id
                    where project.id = :project_id
                      and project.workspace_id = :workspace_id
                    """
                ),
                {"project_id": project_id, "workspace_id": workspace_id},
            ).mappings().one_or_none()
            if current is None:
                raise CollaborationError("NO_SNAPSHOT", "Analyze before importing.", 409)
            items = executable_plan_items(dict(current["snapshot_json"]))
            if not items:
                raise CollaborationError(
                    "NO_EXECUTABLE_ITEMS",
                    "The current plan has no executable items to import.",
                    409,
                )
            handoff = connection.execute(
                text(
                    """
                    insert into public.project_asana_handoffs (
                      workspace_id, project_id, snapshot_id, requested_by,
                      destination_gid, state, total_count
                    ) values (
                      :workspace_id, :project_id, :snapshot_id, :requested_by,
                      :destination_gid, 'running', :total_count
                    )
                    on conflict (project_id, snapshot_id, destination_gid) do update
                    set requested_by = excluded.requested_by,
                        state = 'running', safe_error_code = null, updated_at = now()
                    returning id::text
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "snapshot_id": current["id"],
                    "requested_by": actor_user_id,
                    "destination_gid": self._asana_gateway.destination_gid,
                    "total_count": len(items),
                },
            ).mappings().one()

        completed = 0
        failures = 0
        for item in items:
            with self._engine.begin() as connection:
                existing = connection.execute(
                    text(
                        """
                        insert into public.project_asana_handoff_items (
                          handoff_id, item_key, task_name
                        ) values (:handoff_id, :item_key, :task_name)
                        on conflict (handoff_id, item_key) do update
                        set task_name = excluded.task_name, updated_at = now()
                        returning external_task_gid, state
                        """
                    ),
                    {
                        "handoff_id": handoff["id"],
                        "item_key": item["item_key"],
                        "task_name": item["task"],
                    },
                ).mappings().one()
            if existing["external_task_gid"]:
                completed += 1
                continue
            try:
                external = self._asana_gateway.create_task(item)
            except Exception:
                failures += 1
                with self._engine.begin() as connection:
                    connection.execute(
                        text(
                            """
                            update public.project_asana_handoff_items
                            set state = 'failed', safe_error_code = 'ASANA_REQUEST_FAILED',
                                updated_at = now()
                            where handoff_id = :handoff_id and item_key = :item_key
                            """
                        ),
                        {"handoff_id": handoff["id"], "item_key": item["item_key"]},
                    )
                continue
            completed += 1
            with self._engine.begin() as connection:
                connection.execute(
                    text(
                        """
                        update public.project_asana_handoff_items
                        set external_task_gid = :external_task_gid,
                            external_permalink = :external_permalink,
                            state = 'completed', safe_error_code = null, updated_at = now()
                        where handoff_id = :handoff_id and item_key = :item_key
                        """
                    ),
                    {
                        "external_task_gid": external["gid"],
                        "external_permalink": external.get("permalink_url") or None,
                        "handoff_id": handoff["id"],
                        "item_key": item["item_key"],
                    },
                )

        state = "completed" if completed == len(items) else "partial" if completed else "failed"
        error_code = "ASANA_REQUEST_FAILED" if failures else None
        with self._engine.begin() as connection:
            result = connection.execute(
                text(
                    """
                    update public.project_asana_handoffs
                    set state = :state, completed_count = :completed_count,
                        safe_error_code = :safe_error_code, updated_at = now()
                    where id = :handoff_id
                    returning id::text, state, total_count, completed_count,
                              safe_error_code, destination_gid, created_at, updated_at
                    """
                ),
                {
                    "state": state,
                    "completed_count": completed,
                    "safe_error_code": error_code,
                    "handoff_id": handoff["id"],
                },
            ).mappings().one()
            event_type = "export.done" if state == "completed" else "export.failed"
            self._append_collaboration_history(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                actor_user_id=actor_user_id,
                event_type=event_type,
                summary=(
                    "Executable plan imported to Asana"
                    if state == "completed"
                    else "Asana import needs attention"
                ),
                detail=f"{completed} of {len(items)} executable plan items were imported.",
                payload={
                    "handoff_id": handoff["id"],
                    "format": "asana",
                    "completed_count": completed,
                    "total_count": len(items),
                    "source_analysis_run_id": str(current["analysis_run_id"]),
                    "safe_error_code": error_code,
                },
                idempotency_key=(
                    f"history:asana:{handoff['id']}:{state}:{completed}:{len(items)}"
                ),
            )
        return dict(result)

    def record_report_export(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        export_format: str,
        content_checksum: str | None = None,
    ) -> dict:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        self._require_editor(role)
        with self._engine.begin() as connection:
            snapshot = connection.execute(
                text(
                    """
                    select snapshot.id, snapshot.analysis_run_id
                    from public.projects project
                    join public.assessment_snapshots snapshot
                      on snapshot.analysis_run_id = project.current_analysis_run_id
                    where project.id = :project_id
                      and project.workspace_id = :workspace_id
                    """
                ),
                {"project_id": project_id, "workspace_id": workspace_id},
            ).mappings().one_or_none()
            if snapshot is None:
                raise CollaborationError("NO_SNAPSHOT", "Analyze before exporting.", 409)
            row = connection.execute(
                text(
                    """
                    insert into public.project_export_records (
                      workspace_id, project_id, requested_by, snapshot_id,
                      source_analysis_run_id, read_signature, format, status,
                      content_checksum, completed_at
                    ) values (
                      :workspace_id, :project_id, :requested_by, :snapshot_id,
                      :analysis_run_id, :read_signature, :format, 'completed',
                      :content_checksum, now()
                    )
                    returning id::text, format, status, read_signature,
                              content_checksum, created_at, completed_at
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "requested_by": actor_user_id,
                    "snapshot_id": snapshot["id"],
                    "analysis_run_id": snapshot["analysis_run_id"],
                    "read_signature": (
                        f"{snapshot['analysis_run_id']}:{snapshot['id']}"
                    ),
                    "format": export_format,
                    "content_checksum": content_checksum,
                },
            ).mappings().one()
            self._append_collaboration_history(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                actor_user_id=actor_user_id,
                event_type="export.done",
                summary=f"{export_format.upper()} export completed",
                detail="A current, governed project projection was exported.",
                payload={
                    "export_id": row["id"],
                    "format": export_format,
                    "read_signature": row["read_signature"],
                },
                idempotency_key=f"history:report-export:{row['id']}",
            )
        return dict(row)

    def create_report_schedule(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        recipient_email: str,
        recipient_class: str,
        weekday: int,
        local_time: wall_time,
        timezone: str,
    ) -> dict:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        self._require_editor(role)
        next_run_at = self._next_weekly_run(
            weekday=weekday,
            local_time=local_time,
            timezone=timezone,
            after=datetime.now(UTC),
        )
        with self._engine.begin() as connection:
            subscription = connection.execute(
                text(
                    """
                    select plan_code, status
                    from public.workspace_subscriptions
                    where workspace_id = :workspace_id
                    """
                ),
                {"workspace_id": workspace_id},
            ).mappings().one_or_none()
            if not subscription or subscription["plan_code"] != "basic" or subscription[
                "status"
            ] not in {"active", "grace"}:
                raise CollaborationError(
                    "BASIC_REQUIRED",
                    "Weekly report delivery requires the Basic plan. Send now remains free.",
                    402,
                )
            row = dict(
                connection.execute(
                    text(
                        """
                        insert into public.project_report_schedules (
                          workspace_id, project_id, created_by, recipient_email,
                          recipient_class, weekday, local_time, timezone, next_run_at
                        ) values (
                          :workspace_id, :project_id, :created_by, :recipient_email,
                          :recipient_class, :weekday, :local_time, :timezone, :next_run_at
                        )
                        returning id::text, recipient_email::text, recipient_class,
                                  weekday, local_time::text, timezone, state,
                                  next_run_at, last_run_at, created_at, updated_at
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                        "created_by": actor_user_id,
                        "recipient_email": recipient_email,
                        "recipient_class": recipient_class,
                        "weekday": weekday,
                        "local_time": local_time,
                        "timezone": timezone,
                        "next_run_at": next_run_at,
                    },
                ).mappings().one()
            )
            self._append_collaboration_history(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                actor_user_id=actor_user_id,
                event_type="schedule.created",
                summary="Weekly Executive Briefing scheduled",
                detail=f"Weekly delivery to {recipient_class} begins {next_run_at.isoformat()}.",
                payload={"schedule_id": row["id"], "timezone": timezone},
                idempotency_key=f"history:report-schedule:{row['id']}",
            )
        return row

    def update_report_schedule(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        schedule_id: UUID,
        state: str,
    ) -> dict:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        self._require_editor(role)
        with self._engine.begin() as connection:
            row = connection.execute(
                text(
                    """
                    update public.project_report_schedules
                    set state = :state, updated_at = now()
                    where id = :schedule_id and project_id = :project_id
                      and workspace_id = :workspace_id
                    returning id::text, recipient_email::text, recipient_class,
                              weekday, local_time::text, timezone, state,
                              next_run_at, last_run_at, created_at, updated_at
                    """
                ),
                {
                    "state": state,
                    "schedule_id": schedule_id,
                    "project_id": project_id,
                    "workspace_id": workspace_id,
                },
            ).mappings().one_or_none()
            if row is None:
                raise CollaborationError("SCHEDULE_NOT_FOUND", "Schedule not found.", 404)
            self._append_collaboration_history(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                actor_user_id=actor_user_id,
                event_type="schedule.updated",
                summary=f"Weekly Executive Briefing {state}",
                detail=f"Weekly delivery to {row['recipient_class']} is now {state}.",
                payload={"schedule_id": row["id"], "state": state},
                idempotency_key=(
                    f"history:report-schedule:{row['id']}:{state}:{row['updated_at'].isoformat()}"
                ),
            )
        return dict(row)

    def delete_report_schedule(
        self, *, actor_user_id: UUID, project_id: UUID, schedule_id: UUID
    ) -> None:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        self._require_editor(role)
        with self._engine.begin() as connection:
            deleted = connection.execute(
                text(
                    """
                    delete from public.project_report_schedules
                    where id = :schedule_id and project_id = :project_id
                      and workspace_id = :workspace_id
                    returning recipient_class
                    """
                ),
                {
                    "schedule_id": schedule_id,
                    "project_id": project_id,
                    "workspace_id": workspace_id,
                },
            ).scalar_one_or_none()
            if deleted is None:
                raise CollaborationError("SCHEDULE_NOT_FOUND", "Schedule not found.", 404)
            self._append_collaboration_history(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                actor_user_id=actor_user_id,
                event_type="schedule.removed",
                summary="Weekly Executive Briefing removed",
                detail=f"Weekly delivery to {deleted} was removed.",
                payload={"schedule_id": str(schedule_id)},
                idempotency_key=f"history:report-schedule:{schedule_id}:removed",
            )

    def report_state(self, *, actor_user_id: UUID, project_id: UUID) -> dict:
        workspace_id, _role = self._project_access(actor_user_id, project_id)
        with self._engine.connect() as connection:
            current = (
                connection.execute(
                    text(
                        """
                        select p.name as project_name, s.id as snapshot_id,
                               s.published_at as analysis_completed_at
                        from public.projects p
                        join public.assessment_snapshots s
                          on s.analysis_run_id = p.current_analysis_run_id
                        where p.id = :project_id and p.workspace_id = :workspace_id
                        """
                    ),
                    {"project_id": project_id, "workspace_id": workspace_id},
                )
                .mappings()
                .one_or_none()
            )
            if current is None:
                raise CollaborationError(
                    "NO_SNAPSHOT", "Analyze the project before creating a report", 409
                )
            draft = (
                connection.execute(
                    text(
                        """
                        select content_json, updated_at, recipient_class,
                               composition_depth, included_json, revision,
                               source_analysis_run_id::text, read_signature
                        from public.project_report_drafts
                        where project_id = :project_id and snapshot_id = :snapshot_id
                        """
                    ),
                    {
                        "project_id": project_id,
                        "snapshot_id": current["snapshot_id"],
                    },
                )
                .mappings()
                .one_or_none()
            )
            deliveries = [
                dict(item)
                for item in connection.execute(
                    text(
                        """
                        select id::text, recipient_email::text, recipient_label,
                               status, scheduled_for, sent_at, error_code, created_at,
                               currency_state, previous_analysis_confirmed,
                               report_version, source_analysis_run_id::text,
                               analysis_completed_at, read_signature,
                               content_checksum, disclaimer_version,
                               content_json as content
                        from public.project_report_deliveries
                        where project_id = :project_id
                        order by created_at desc
                        limit 20
                        """
                    ),
                    {"project_id": project_id},
                ).mappings()
            ]
        return {
            "project_id": str(project_id),
            "project_name": current["project_name"],
            "snapshot_id": str(current["snapshot_id"]),
            "content": dict(draft["content_json"]) if draft else None,
            "updated_at": draft["updated_at"] if draft else None,
            "recipient_class": draft["recipient_class"] if draft else "exec-sponsor",
            "composition_depth": draft["composition_depth"] if draft else "full",
            "included": dict(draft["included_json"]) if draft else {},
            "revision": draft["revision"] if draft else 0,
            "source_analysis_run_id": (
                draft["source_analysis_run_id"] if draft else None
            ),
            "read_signature": draft["read_signature"] if draft else None,
            "analysis_completed_at": current["analysis_completed_at"],
            "deliveries": deliveries,
        }

    def save_report(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        snapshot_id: UUID,
        content: dict,
        recipient_class: str = "exec-sponsor",
        composition_depth: str = "full",
        included: dict | None = None,
        revision: int = 1,
    ) -> dict:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        self._require_editor(role)
        with self._engine.begin() as connection:
            current_snapshot_id = connection.execute(
                text(
                    """
                    select s.id
                    from public.projects p
                    join public.assessment_snapshots s
                      on s.analysis_run_id = p.current_analysis_run_id
                    where p.id = :project_id and p.workspace_id = :workspace_id
                    """
                ),
                {"project_id": project_id, "workspace_id": workspace_id},
            ).scalar_one_or_none()
            if current_snapshot_id != snapshot_id:
                raise CollaborationError(
                    "REPORT_SNAPSHOT_STALE",
                    "The project changed. Refresh the report before saving.",
                    409,
                )
            snapshot = connection.execute(
                text(
                    """
                    select id, analysis_run_id
                    from public.assessment_snapshots
                    where id = :snapshot_id and project_id = :project_id
                      and workspace_id = :workspace_id
                    """
                ),
                {
                    "snapshot_id": snapshot_id,
                    "project_id": project_id,
                    "workspace_id": workspace_id,
                },
            ).mappings().one()
            updated_at = connection.execute(
                text(
                    """
                    insert into public.project_report_drafts (
                      project_id, workspace_id, snapshot_id, content_json, updated_by,
                      recipient_class, composition_depth, included_json,
                      revision, source_analysis_run_id, read_signature
                    ) values (
                      :project_id, :workspace_id, :snapshot_id,
                      cast(:content as jsonb), :updated_by, :recipient_class,
                      :composition_depth, cast(:included as jsonb), :revision,
                      :source_analysis_run_id, :read_signature
                    )
                    on conflict (project_id) do update set
                      workspace_id = excluded.workspace_id,
                      snapshot_id = excluded.snapshot_id,
                      content_json = excluded.content_json,
                      updated_by = excluded.updated_by,
                      recipient_class = excluded.recipient_class,
                      composition_depth = excluded.composition_depth,
                      included_json = excluded.included_json,
                      revision = greatest(
                        public.project_report_drafts.revision,
                        excluded.revision
                      ),
                      source_analysis_run_id = excluded.source_analysis_run_id,
                      read_signature = excluded.read_signature,
                      updated_at = now()
                    returning updated_at
                    """
                ),
                {
                    "project_id": project_id,
                    "workspace_id": workspace_id,
                    "snapshot_id": snapshot_id,
                    "content": json.dumps(content),
                    "updated_by": actor_user_id,
                    "recipient_class": recipient_class,
                    "composition_depth": composition_depth,
                    "included": json.dumps(included or {}),
                    "revision": revision,
                    "source_analysis_run_id": snapshot["analysis_run_id"],
                    "read_signature": f"{snapshot['analysis_run_id']}:{snapshot_id}",
                },
            ).scalar_one()
        return {
            "project_id": str(project_id),
            "snapshot_id": str(snapshot_id),
            "content": content,
            "updated_at": updated_at,
            "recipient_class": recipient_class,
            "composition_depth": composition_depth,
            "included": included or {},
            "revision": revision,
        }

    def deliver_report(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        snapshot_id: UUID,
        recipient_email: str,
        recipient_label: str,
        subject: str,
        content: dict,
        scheduled_for: datetime | None,
        confirm_previous_analysis: bool = False,
    ) -> dict:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        self._require_editor(role)
        deliver_at = scheduled_for or datetime.now(UTC)
        if deliver_at.tzinfo is None:
            deliver_at = deliver_at.replace(tzinfo=UTC)
        if deliver_at > datetime.now(UTC) + timedelta(days=90):
            raise CollaborationError(
                "REPORT_SCHEDULE_TOO_FAR",
                "Reports can be scheduled up to 90 days ahead.",
                422,
            )
        with self._engine.begin() as connection:
            snapshot_state = (
                connection.execute(
                text(
                    """
                    select current_snapshot.id as current_snapshot_id,
                           requested_snapshot.id is not null as requested_snapshot_exists,
                           requested_snapshot.analysis_run_id as source_analysis_run_id,
                           requested_snapshot.published_at as analysis_completed_at
                    from public.projects p
                    left join public.assessment_snapshots current_snapshot
                      on current_snapshot.analysis_run_id = p.current_analysis_run_id
                    left join public.assessment_snapshots requested_snapshot
                      on requested_snapshot.id = :snapshot_id
                     and requested_snapshot.project_id = p.id
                     and requested_snapshot.workspace_id = p.workspace_id
                    where p.id = :project_id and p.workspace_id = :workspace_id
                    """
                ),
                {
                    "project_id": project_id,
                    "workspace_id": workspace_id,
                    "snapshot_id": snapshot_id,
                },
                )
                .mappings()
                .one_or_none()
            )
            if snapshot_state is None or not snapshot_state["requested_snapshot_exists"]:
                raise CollaborationError(
                    "REPORT_SNAPSHOT_NOT_FOUND",
                    "The selected report snapshot is not available for this project.",
                    404,
                )
            is_previous_analysis = snapshot_state["current_snapshot_id"] != snapshot_id
            if is_previous_analysis:
                raise CollaborationError(
                    "REPORT_PREVIOUS_ANALYSIS_BLOCKED",
                    (
                        "Refresh the report from the current analysis before "
                        "sending or scheduling it."
                    ),
                    409,
                )
            currency_state = "current"
            delivery_content = json.loads(json.dumps(content))
            delivery_subject = subject
            read_signature = (
                f"{snapshot_state['source_analysis_run_id']}:{snapshot_id}"
            )
            content_checksum = sha256(
                json.dumps(
                    delivery_content,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest()
            connection.execute(
                text("select pg_advisory_xact_lock(hashtextextended(:key, 0))"),
                {"key": f"report-version:{project_id}"},
            )
            report_version = connection.execute(
                text(
                    """
                    select coalesce(max(report_version), 0) + 1
                    from public.project_report_deliveries
                    where project_id = :project_id
                    """
                ),
                {"project_id": project_id},
            ).scalar_one()
            delivery_id = connection.execute(
                text(
                    """
                    insert into public.project_report_deliveries (
                      workspace_id, project_id, snapshot_id, requested_by,
                      recipient_email, recipient_label, subject, content_json,
                      status, scheduled_for, currency_state,
                      previous_analysis_confirmed, report_version,
                      source_analysis_run_id, analysis_completed_at,
                      read_signature, content_checksum
                    ) values (
                      :workspace_id, :project_id, :snapshot_id, :requested_by,
                      :recipient_email, :recipient_label, :subject,
                      cast(:content as jsonb), 'scheduled', :scheduled_for,
                      :currency_state, :previous_analysis_confirmed, :report_version,
                      :source_analysis_run_id, :analysis_completed_at,
                      :read_signature, :content_checksum
                    )
                    returning id
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "snapshot_id": snapshot_id,
                    "requested_by": actor_user_id,
                    "recipient_email": recipient_email,
                    "recipient_label": recipient_label,
                    "subject": delivery_subject,
                    "content": json.dumps(delivery_content),
                    "scheduled_for": deliver_at,
                    "currency_state": currency_state,
                    "previous_analysis_confirmed": False,
                    "report_version": report_version,
                    "source_analysis_run_id": snapshot_state["source_analysis_run_id"],
                    "analysis_completed_at": snapshot_state["analysis_completed_at"],
                    "read_signature": read_signature,
                    "content_checksum": content_checksum,
                },
            ).scalar_one()
            scheduled = scheduled_for is not None and deliver_at > datetime.now(UTC)
            self._append_collaboration_history(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                actor_user_id=actor_user_id,
                event_type="report.scheduled" if scheduled else "report.delivery_requested",
                summary="Report scheduled" if scheduled else "Report delivery requested",
                detail=(
                    f"Delivery to {recipient_label} ({recipient_email}) at "
                    f"{deliver_at.isoformat()}."
                    if scheduled
                    else f"Delivery to {recipient_label} ({recipient_email}) was requested."
                ),
                payload={
                    "delivery_id": str(delivery_id),
                    "recipient_email": recipient_email,
                    "scheduled_for": deliver_at.isoformat(),
                    "currency_state": currency_state,
                },
                idempotency_key=f"history:report-request:{delivery_id}",
            )
        delay = max(0.0, (deliver_at - datetime.now(UTC)).total_seconds())
        if delay <= 1:
            self._send_report_delivery(delivery_id)
        return self._report_delivery(delivery_id)

    def _report_delivery_loop(self) -> None:
        while not self._report_worker_stop.wait(5):
            try:
                schedules = self._claim_due_report_schedules()
                for schedule in schedules:
                    if not schedule["content"] or not schedule["snapshot_is_current"]:
                        continue
                    delivery = self.deliver_report(
                        actor_user_id=schedule["created_by"],
                        project_id=schedule["project_id"],
                        snapshot_id=schedule["snapshot_id"],
                        recipient_email=schedule["recipient_email"],
                        recipient_label=schedule["recipient_class"].replace("-", " ").title(),
                        subject=f"{schedule['project_name']} Executive Briefing",
                        content=dict(schedule["content"]),
                        scheduled_for=None,
                    )
                    with self._engine.begin() as connection:
                        connection.execute(
                            text(
                                """
                                update public.project_report_schedules
                                set last_delivery_id = :delivery_id, updated_at = now()
                                where id = :schedule_id
                                """
                            ),
                            {
                                "delivery_id": delivery["id"],
                                "schedule_id": schedule["id"],
                            },
                        )
                with self._engine.begin() as connection:
                    connection.execute(
                        text(
                            """
                            update public.project_report_deliveries
                            set status = 'scheduled'
                            where status = 'sending'
                              and scheduled_for < now() - interval '10 minutes'
                            """
                        )
                    )
                    delivery_ids = list(
                        connection.execute(
                            text(
                                """
                                select id
                                from public.project_report_deliveries
                                where status = 'scheduled' and scheduled_for <= now()
                                order by scheduled_for
                                limit 20
                                """
                            )
                        ).scalars()
                    )
                for delivery_id in delivery_ids:
                    self._send_report_delivery(delivery_id)
            except Exception:
                # A later poll retries durable scheduled rows after transient DB failures.
                continue

    def _claim_due_report_schedules(self) -> list[dict]:
        """Advance due weekly rows before enqueueing a current-truth memo.

        A schedule only travels when its stored authored draft has the same read
        signature as the project's current retained analysis. If the read moved,
        this deliberately fails closed until the owner regenerates the draft.
        """
        now = datetime.now(UTC)
        claimed: list[dict] = []
        with self._engine.begin() as connection:
            rows = list(
                connection.execute(
                    text(
                        """
                        select schedule.id, schedule.created_by,
                               schedule.project_id, schedule.recipient_email::text,
                               schedule.recipient_class, schedule.weekday,
                               schedule.local_time, schedule.timezone,
                               project.name as project_name,
                               snapshot.id as snapshot_id,
                               draft.content_json as content,
                               draft.read_signature =
                                 snapshot.analysis_run_id::text || ':' || snapshot.id::text
                                 as snapshot_is_current
                        from public.project_report_schedules schedule
                        join public.projects project on project.id = schedule.project_id
                        join public.assessment_snapshots snapshot
                          on snapshot.analysis_run_id = project.current_analysis_run_id
                        left join public.project_report_drafts draft
                          on draft.project_id = project.id
                         and draft.snapshot_id = snapshot.id
                        where schedule.state = 'enabled'
                          and schedule.next_run_at <= :now
                        order by schedule.next_run_at
                        for update of schedule skip locked
                        limit 20
                        """
                    ),
                    {"now": now},
                ).mappings()
            )
            for row in rows:
                next_run_at = self._next_weekly_run(
                    weekday=row["weekday"],
                    local_time=row["local_time"],
                    timezone=row["timezone"],
                    after=now,
                )
                connection.execute(
                    text(
                        """
                        update public.project_report_schedules
                        set last_run_at = :now, next_run_at = :next_run_at,
                            updated_at = now()
                        where id = :schedule_id
                        """
                    ),
                    {
                        "now": now,
                        "next_run_at": next_run_at,
                        "schedule_id": row["id"],
                    },
                )
                claimed.append(dict(row))
        return claimed

    def _report_delivery(self, delivery_id: UUID) -> dict:
        with self._engine.connect() as connection:
            row = (
                connection.execute(
                    text(
                        """
                        select id::text, recipient_email::text, recipient_label,
                               status, scheduled_for, sent_at, error_code, created_at,
                               currency_state, previous_analysis_confirmed,
                               report_version, source_analysis_run_id::text,
                               analysis_completed_at, read_signature,
                               content_checksum, disclaimer_version,
                               content_json as content
                        from public.project_report_deliveries where id = :delivery_id
                        """
                    ),
                    {"delivery_id": delivery_id},
                )
                .mappings()
                .one()
            )
        return dict(row)

    def _send_report_delivery(self, delivery_id: UUID) -> None:
        with self._engine.begin() as connection:
            row = (
                connection.execute(
                    text(
                        """
                        update public.project_report_deliveries delivery
                        set status = 'sending', error_code = null
                        from public.projects project
                        where delivery.id = :delivery_id
                          and delivery.status = 'scheduled'
                          and delivery.project_id = project.id
                        returning delivery.recipient_email::text,
                                  delivery.recipient_label, delivery.subject,
                                  delivery.content_json, delivery.workspace_id,
                                  delivery.project_id, delivery.requested_by,
                                  project.name as project_name
                        """
                    ),
                    {"delivery_id": delivery_id},
                )
                .mappings()
                .one_or_none()
            )
        if row is None:
            return
        try:
            if self._report_mailer is None:
                raise RuntimeError("REPORT_MAILER_UNAVAILABLE")
            self._report_mailer.send_report(
                email=row["recipient_email"],
                subject=row["subject"],
                project_name=row["project_name"],
                recipient_label=row["recipient_label"],
                sections=list(dict(row["content_json"]).get("sections", [])),
            )
        except Exception:
            with self._engine.begin() as connection:
                connection.execute(
                    text(
                        """
                        update public.project_report_deliveries
                        set status = 'failed', error_code = 'REPORT_DELIVERY_FAILED'
                        where id = :delivery_id
                        """
                    ),
                    {"delivery_id": delivery_id},
                )
                self._append_collaboration_history(
                    connection,
                    workspace_id=row["workspace_id"],
                    project_id=row["project_id"],
                    actor_user_id=row["requested_by"],
                    event_type="report.delivery_failed",
                    summary="Report delivery failed",
                    detail=(
                        f"Delivery to {row['recipient_label']} "
                        f"({row['recipient_email']}) failed and can be retried."
                    ),
                    payload={"delivery_id": str(delivery_id)},
                    idempotency_key=f"history:report-failed:{delivery_id}",
                )
        else:
            with self._engine.begin() as connection:
                connection.execute(
                    text(
                        """
                        update public.project_report_deliveries
                        set status = 'sent', sent_at = now()
                        where id = :delivery_id
                        """
                    ),
                    {"delivery_id": delivery_id},
                )
                self._append_collaboration_history(
                    connection,
                    workspace_id=row["workspace_id"],
                    project_id=row["project_id"],
                    actor_user_id=row["requested_by"],
                    event_type="report.sent",
                    summary="Report sent",
                    detail=(
                        f"Report delivered to {row['recipient_label']} "
                        f"({row['recipient_email']})."
                    ),
                    payload={"delivery_id": str(delivery_id)},
                    idempotency_key=f"history:report-sent:{delivery_id}",
                )

    def _project_access(self, actor_user_id: UUID, project_id: UUID) -> tuple[UUID, str]:
        with self._engine.connect() as connection:
            row = (
                connection.execute(
                    text(
                        """
                        select p.workspace_id, m.role::text as role
                        from public.projects p
                        join public.memberships m on m.workspace_id = p.workspace_id
                        where p.id = :project_id and m.user_id = :user_id
                        """
                    ),
                    {"project_id": project_id, "user_id": actor_user_id},
                )
                .mappings()
                .one_or_none()
            )
        if row is None:
            raise CollaborationError("PROJECT_FORBIDDEN", "Project access denied", 403)
        return row["workspace_id"], row["role"]

    @staticmethod
    def _require_editor(role: str) -> None:
        if role != "owner":
            raise CollaborationError(
                "COLLABORATION_FORBIDDEN",
                "Only workspace owners can change collaboration settings",
                403,
            )

    @staticmethod
    def _append_collaboration_history(
        connection: Connection,
        *,
        workspace_id: UUID,
        project_id: UUID,
        actor_user_id: UUID,
        event_type: str,
        summary: str,
        idempotency_key: str,
        detail: str | None = None,
        issue_id: str | None = None,
        payload: dict | None = None,
    ) -> None:
        """Retain project-scoped collaboration activity without creating a run."""

        analysis_run_id = connection.execute(
            text(
                """
                select current_analysis_run_id
                from public.projects
                where id = :project_id
                """
            ),
            {"project_id": project_id},
        ).scalar_one_or_none()
        if analysis_run_id is None:
            return
        append_history_event(
            connection,
            workspace_id=workspace_id,
            project_id=project_id,
            analysis_run_id=analysis_run_id,
            actor_type="user",
            actor_id=actor_user_id,
            category="collaboration",
            event_type=event_type,
            summary=summary,
            detail=detail,
            issue_id=issue_id,
            payload=payload,
            idempotency_key=idempotency_key,
        )
