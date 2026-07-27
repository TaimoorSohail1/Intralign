from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from secrets import token_urlsafe
from uuid import UUID

from sqlalchemy import Connection, Engine, text

from oslo_api.analysis.history import append_history_event


class CollaborationError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


class DatabaseCollaborationService:
    """Tenant-scoped collaboration boundary for Slice 9.

    Analysis remains owned by Slice 2. This service owns principals, comments,
    bearer grants, review attestations and export audit records.
    """

    def __init__(self, engine: Engine, web_url: str) -> None:
        self._engine = engine
        self._web_url = web_url.rstrip("/")

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
                        order by
                          case m.role when 'owner' then 0 when 'collaborator' then 1 else 2 end,
                          lower(p.display_name)
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
                               r.response_kind::text, r.body as response_body,
                               r.created_at as responded_at
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
                        select id::text, expires_at, revoked_at, created_at
                        from public.project_share_links
                        where project_id = :project_id
                        order by created_at desc
                        """
                    ),
                    {"project_id": project_id},
                ).mappings()
            ]
            monthly_invites_used = connection.execute(
                text(
                    """
                    select count(*)
                    from public.invitations
                    where workspace_id = :workspace_id
                      and created_at >= date_trunc('month', now())
                      and (
                        status = 'accepted'
                        or (status = 'pending' and expires_at > now())
                      )
                    """
                ),
                {"workspace_id": workspace_id},
            ).scalar_one()
        return {
            "workspace_id": str(workspace_id),
            "project_id": str(project_id),
            "actor_role": role,
            "plan": {
                "name": "Free",
                "collaborator_seats": 3,
                "collaborator_seats_used": sum(
                    1 for participant in participants if participant["role"] != "viewer"
                ),
                "monthly_invites": 2,
                "monthly_invites_used": monthly_invites_used,
                "viewers_unlimited": True,
                "reviewers_unmetered": True,
                "export_formats": ["pdf"],
            },
            "participants": participants,
            "comments": comments,
            "reviews": reviews,
            "share_links": share_links,
        }

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
        return dict(row)

    def create_snapshot_link(
        self, *, actor_user_id: UUID, project_id: UUID
    ) -> dict:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        self._require_editor(role)
        raw = token_urlsafe(32)
        expires_at = datetime.now(UTC) + timedelta(days=30)
        with self._engine.begin() as connection:
            snapshot_id = connection.execute(
                text(
                    """
                    select id from public.assessment_snapshots
                    where project_id = :project_id
                    order by published_at desc limit 1
                    """
                ),
                {"project_id": project_id},
            ).scalar_one_or_none()
            if snapshot_id is None:
                raise CollaborationError("NO_SNAPSHOT", "Analyze the project before sharing", 409)
            link_id = connection.execute(
                text(
                    """
                    insert into public.project_share_links (
                      workspace_id, project_id, snapshot_id, token_hash, created_by, expires_at
                    ) values (
                      :workspace_id, :project_id, :snapshot_id, :token_hash,
                      :created_by, :expires_at
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
                },
            ).scalar_one()
            self._append_collaboration_history(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                actor_user_id=actor_user_id,
                event_type="collaboration.snapshot_shared",
                summary="Project snapshot shared",
                detail="A read-only project snapshot link was created.",
                payload={"share_link_id": str(link_id)},
                idempotency_key=f"collaboration:share:{link_id}:created",
            )
        return {
            "id": str(link_id),
            "url": f"{self._web_url}/share/{raw}",
            "expires_at": expires_at,
        }

    def create_review_grant(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        issue_id: str | None,
        reviewer_name: str,
        reviewer_email: str | None,
    ) -> dict:
        workspace_id, role = self._project_access(actor_user_id, project_id)
        self._require_editor(role)
        name = reviewer_name.strip()
        if not name:
            raise CollaborationError("REVIEWER_REQUIRED", "Reviewer name is required")
        raw = token_urlsafe(32)
        expires_at = datetime.now(UTC) + timedelta(days=14)
        with self._engine.begin() as connection:
            grant_id = connection.execute(
                text(
                    """
                    insert into public.project_review_grants (
                      workspace_id, project_id, issue_stable_key, reviewer_name,
                      reviewer_email, token_hash, created_by, expires_at
                    ) values (
                      :workspace_id, :project_id, :issue_id, :reviewer_name,
                      :reviewer_email, :token_hash, :created_by, :expires_at
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
                },
            ).scalar_one()
            self._append_collaboration_history(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                actor_user_id=actor_user_id,
                event_type="collaboration.review_invited",
                summary="Reviewer invited",
                detail=f"{name} was invited to review a project issue.",
                issue_id=issue_id,
                payload={
                    "review_grant_id": str(grant_id),
                    "reviewer_name": name,
                },
                idempotency_key=f"collaboration:review:{grant_id}:created",
            )
        return {
            "id": str(grant_id),
            "url": f"{self._web_url}/review/{raw}",
            "expires_at": expires_at,
        }

    def resolve_snapshot(self, token: str) -> dict:
        with self._engine.connect() as connection:
            row = (
                connection.execute(
                    text(
                        """
                        select p.name as project_name, s.snapshot_json, s.snapshot_state,
                               s.published_at, l.expires_at
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
        return dict(row)

    def resolve_review(self, token: str) -> dict:
        with self._engine.connect() as connection:
            row = (
                connection.execute(
                    text(
                        """
                        select g.id, g.project_id, g.issue_stable_key as issue_id,
                               g.reviewer_name, g.expires_at, p.name as project_name,
                               s.snapshot_json,
                               case when r.analysis_run_id is not null
                                 then r.response_kind::text
                               end as response_kind,
                               case when r.analysis_run_id is not null
                                 then r.body
                               end as response_body
                        from public.project_review_grants g
                        join public.projects p on p.id = g.project_id
                        join lateral (
                          select snapshot_json from public.assessment_snapshots
                          where project_id = g.project_id order by published_at desc limit 1
                        ) s on true
                        left join public.project_review_responses r on r.review_grant_id = g.id
                        where g.token_hash = :token_hash and g.revoked_at is null
                          and g.expires_at > now()
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
        return dict(row)

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
                        where token_hash = :token_hash and revoked_at is null and expires_at > now()
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
                          response_kind, body
                        ) values (
                          :workspace_id, :project_id, :grant_id, :issue_id,
                          cast(:kind as public.review_response_kind), :body
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
                    },
                ).scalar_one()
        return {
            "id": str(response_id),
            "project_id": str(grant["project_id"]),
            "issue_id": grant["issue_stable_key"],
            "response_kind": kind,
            "body": clean,
            "created_by": str(grant["created_by"]),
            "reviewer_name": grant["reviewer_name"],
        }

    def link_review_run(self, *, response_id: UUID, run_id: UUID) -> None:
        with self._engine.begin() as connection:
            response = (
                connection.execute(
                    text(
                        """
                        select r.workspace_id, r.project_id, r.review_grant_id,
                               r.issue_stable_key, r.response_kind::text as response_kind,
                               g.reviewer_name
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
            connection.execute(
                text(
                    """
                    insert into public.outbox_events (
                      workspace_id, aggregate_type, aggregate_id, event_type, payload
                    ) values (
                      :workspace_id, 'review_response', :response_id,
                      'review.responded', cast(:payload as jsonb)
                    )
                    """
                ),
                {
                    "workspace_id": response["workspace_id"],
                    "response_id": response_id,
                    "payload": json.dumps(
                        {
                            "project_id": str(response["project_id"]),
                            "issue_id": response["issue_stable_key"],
                            "reviewer_name": response["reviewer_name"],
                            "response_kind": response["response_kind"],
                            "analysis_run_id": str(run_id),
                        }
                    ),
                },
            )

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
                event_type="collaboration.snapshot_share_revoked",
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
                    set revoked_at = coalesce(revoked_at, now())
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
                event_type="collaboration.review_revoked",
                summary="Review invitation revoked",
                detail="A project review invitation was revoked.",
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
        if role not in {"owner", "collaborator"}:
            raise CollaborationError(
                "COLLABORATION_FORBIDDEN",
                "Only owners and collaborators can change collaboration settings",
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
