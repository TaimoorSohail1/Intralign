import json
from collections.abc import Callable
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from uuid import UUID

from sqlalchemy import Engine, text

from oslo_api.analysis.documents import (
    MAX_DOCUMENT_BYTES,
    DocumentRejected,
    ParsedDocument,
    parse_document,
)
from oslo_api.analysis.object_storage import LocalObjectStorage, ObjectStorage

PARSER_VERSION = "oslo-parser-v2"
RETRYABLE_PARSE_ERRORS = {"DOCUMENT_OCR_FAILED", "DOCUMENT_PARSING_FAILED"}


@dataclass(frozen=True, slots=True)
class UploadedDocument:
    id: UUID
    file_name: str
    object_key: str
    status: str
    fragment_count: int


class DatabaseDocumentStore:
    def __init__(
        self,
        *,
        engine: Engine,
        object_store: ObjectStorage | None = None,
        object_root: Path | None = None,
        parser: Callable[..., ParsedDocument] = parse_document,
        max_parse_attempts: int = 3,
    ) -> None:
        self._engine = engine
        if object_store is None:
            if object_root is None:
                raise ValueError("OBJECT_STORE_REQUIRED")
            object_store = LocalObjectStorage(object_root)
        self._object_store = object_store
        self._parser = parser
        self._max_parse_attempts = max(1, max_parse_attempts)

    def ingest(
        self,
        *,
        workspace_id: UUID,
        project_id: UUID,
        submitted_by: UUID,
        file_name: str,
        declared_content_type: str | None,
        content: bytes,
        document_limit: int | None = None,
        word_limit: int | None = None,
    ) -> UploadedDocument:
        if not content:
            raise DocumentRejected("DOCUMENT_EMPTY")
        if len(content) > MAX_DOCUMENT_BYTES:
            raise DocumentRejected("DOCUMENT_TOO_LARGE")
        checksum = sha256(content).hexdigest()
        safe_name = Path(file_name).name[:255] or "document"
        upload_title = " ".join(Path(safe_name).stem.replace("_", " ").split())[:160]
        suffix = Path(safe_name).suffix.lower()
        object_key = f"{workspace_id}/{project_id}/{checksum}{suffix}"

        with self._engine.begin() as connection:
            existing = (
                connection.execute(
                    text(
                        """
                        select id, file_name, object_key, status
                        from public.source_documents
                        where workspace_id = :workspace_id
                          and project_id = :project_id
                          and checksum = :checksum
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                        "checksum": checksum,
                    },
                )
                .mappings()
                .one_or_none()
            )
            if existing is not None:
                fragment_count = connection.execute(
                    text(
                        """
                        select count(*) from public.source_fragments
                        where source_document_id = :document_id
                        """
                    ),
                    {"document_id": existing["id"]},
                ).scalar_one()
                if existing["status"] == "parsed":
                    return UploadedDocument(
                        id=existing["id"],
                        file_name=existing["file_name"],
                        object_key=existing["object_key"],
                        status=existing["status"],
                        fragment_count=fragment_count,
                    )
                document_id = existing["id"]
                safe_name = existing["file_name"]
                object_key = existing["object_key"]
            else:
                document_id = None

        if document_id is not None:
            stored_content = (
                self._object_store.get(object_key)
                if self._object_store.exists(object_key)
                else content
            )
            return self._parse_and_persist(
                workspace_id=workspace_id,
                project_id=project_id,
                document_id=document_id,
                safe_name=safe_name,
                declared_content_type=declared_content_type,
                content=stored_content,
                object_key=object_key,
                document_limit=document_limit,
                word_limit=word_limit,
            )

        self._object_store.put(object_key, content)
        with self._engine.begin() as connection:
            intake_id = connection.execute(
                text(
                    """
                    insert into public.intake_submissions (
                      workspace_id, project_id, submitted_by, start_method, description
                    ) values (
                      :workspace_id, :project_id, :submitted_by, 'documents', ''
                    )
                    returning id
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "submitted_by": submitted_by,
                },
            ).scalar_one()
            document_id = connection.execute(
                text(
                    """
                    insert into public.source_documents (
                      workspace_id, project_id, intake_submission_id, file_name,
                      object_key, detected_mime_type, byte_size, checksum,
                      status, parser_version
                    ) values (
                      :workspace_id, :project_id, :intake_id, :file_name,
                      :object_key, :content_type, :byte_size, :checksum,
                      'uploaded', :parser_version
                    )
                    returning id
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "intake_id": intake_id,
                    "file_name": safe_name,
                    "object_key": object_key,
                    "content_type": declared_content_type,
                    "byte_size": len(content),
                    "checksum": checksum,
                    "parser_version": PARSER_VERSION,
                },
            ).scalar_one()
            connection.execute(
                text(
                    """
                    update public.projects
                    set name = :upload_title, updated_at = now()
                    where id = :project_id
                      and name = 'Untitled project'
                      and nullif(trim(cast(:upload_title as text)), '') is not null
                    """
                ),
                {
                    "project_id": project_id,
                    "upload_title": upload_title,
                },
            )
        return self._parse_and_persist(
            workspace_id=workspace_id,
            project_id=project_id,
            document_id=document_id,
            safe_name=safe_name,
            declared_content_type=declared_content_type,
            content=content,
            object_key=object_key,
            document_limit=document_limit,
            word_limit=word_limit,
        )

    def _parse_and_persist(
        self,
        *,
        workspace_id: UUID,
        project_id: UUID,
        document_id: UUID,
        safe_name: str,
        declared_content_type: str | None,
        content: bytes,
        object_key: str,
        document_limit: int | None,
        word_limit: int | None,
    ) -> UploadedDocument:
        with self._engine.connect() as connection:
            previous_attempts = connection.execute(
                text(
                    """
                    select coalesce(max(attempt_no), 0)
                    from public.document_parse_attempts
                    where source_document_id = :document_id
                    """
                ),
                {"document_id": document_id},
            ).scalar_one()
        for attempt_offset in range(1, self._max_parse_attempts + 1):
            attempt_no = previous_attempts + attempt_offset
            with self._engine.begin() as connection:
                connection.execute(
                    text(
                        """
                        insert into public.document_parse_attempts (
                          workspace_id, project_id, source_document_id, attempt_no,
                          status, parser_version
                        ) values (
                          :workspace_id, :project_id, :document_id, :attempt_no,
                          'running', :parser_version
                        )
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                        "document_id": document_id,
                        "attempt_no": attempt_no,
                        "parser_version": PARSER_VERSION,
                    },
                )
                connection.execute(
                    text(
                        """
                        update public.source_documents
                        set status = 'parsing', parse_attempt_count = :attempt_no,
                            last_attempt_at = now(), failure_code = null
                        where id = :document_id
                        """
                    ),
                    {"document_id": document_id, "attempt_no": attempt_no},
                )
            try:
                parsed = self._parser(
                    file_name=safe_name,
                    declared_content_type=declared_content_type,
                    content=content,
                )
            except DocumentRejected as error:
                code = str(error)
                retryable = code in RETRYABLE_PARSE_ERRORS
                self._record_failed_attempt(
                    document_id=document_id,
                    attempt_no=attempt_no,
                    error_code=code,
                    retryable=retryable,
                )
                if retryable and attempt_offset < self._max_parse_attempts:
                    continue
                raise
            except Exception as error:
                code = "DOCUMENT_PARSING_FAILED"
                self._record_failed_attempt(
                    document_id=document_id,
                    attempt_no=attempt_no,
                    error_code=code,
                    retryable=True,
                )
                if attempt_offset < self._max_parse_attempts:
                    continue
                raise DocumentRejected(code) from error

            with self._engine.begin() as connection:
                connection.execute(
                    text("select pg_advisory_xact_lock(hashtext(cast(:project_id as text)))"),
                    {"project_id": project_id},
                )
                existing_document_count = int(
                    connection.execute(
                        text(
                            """
                            select count(*)
                            from public.source_documents
                            where project_id = :project_id
                              and status = 'parsed'
                              and id <> :document_id
                            """
                        ),
                        {
                            "project_id": project_id,
                            "document_id": document_id,
                        },
                    ).scalar_one()
                )
                existing_word_count = int(
                    connection.execute(
                        text(
                            """
                            select coalesce(sum(
                              cardinality(
                                regexp_split_to_array(
                                  trim(sf.content),
                                  '[[:space:]]+'
                                )
                              )
                            ), 0)
                            from public.source_fragments sf
                            join public.source_documents sd
                              on sd.id = sf.source_document_id
                            where sd.project_id = :project_id
                              and sd.status = 'parsed'
                              and sd.id <> :document_id
                            """
                        ),
                        {
                            "project_id": project_id,
                            "document_id": document_id,
                        },
                    ).scalar_one()
                )
                parsed_word_count = sum(
                    len(fragment.content.split()) for fragment in parsed.fragments
                )
                exceeds_documents = (
                    document_limit is not None
                    and existing_document_count + 1 > document_limit
                )
                exceeds_words = (
                    word_limit is not None
                    and existing_word_count + parsed_word_count > word_limit
                )
                if exceeds_documents or exceeds_words:
                    rejection_code = (
                        "PLAN_DOCUMENT_LIMIT_REACHED"
                        if exceeds_documents
                        else "PLAN_WORD_LIMIT_REACHED"
                    )
                    connection.execute(
                        text(
                            """
                            update public.document_parse_attempts
                            set status = 'failed', error_code = :error_code,
                                retryable = false, completed_at = now()
                            where source_document_id = :document_id
                              and attempt_no = :attempt_no
                            """
                        ),
                        {
                            "document_id": document_id,
                            "attempt_no": attempt_no,
                            "error_code": rejection_code,
                        },
                    )
                    connection.execute(
                        text(
                            """
                            update public.source_documents
                            set status = 'rejected', failure_code = :error_code
                            where id = :document_id
                            """
                        ),
                        {
                            "document_id": document_id,
                            "error_code": rejection_code,
                        },
                    )
                    connection.commit()
                    raise DocumentRejected(rejection_code)
                connection.execute(
                    text("delete from public.source_fragments where source_document_id = :id"),
                    {"id": document_id},
                )
                for fragment in parsed.fragments:
                    connection.execute(
                        text(
                            """
                            insert into public.source_fragments (
                              workspace_id, project_id, source_document_id, ordinal,
                              content, locator, checksum
                            ) values (
                              :workspace_id, :project_id, :document_id, :ordinal,
                              :content, cast(:locator as jsonb), :checksum
                            )
                            """
                        ),
                        {
                            "workspace_id": workspace_id,
                            "project_id": project_id,
                            "document_id": document_id,
                            "ordinal": fragment.ordinal,
                            "content": fragment.content,
                            "locator": json.dumps(fragment.locator),
                            "checksum": sha256(fragment.content.encode()).hexdigest(),
                        },
                    )
                connection.execute(
                    text(
                        """
                        update public.document_parse_attempts
                        set status = 'completed', completed_at = now()
                        where source_document_id = :document_id
                          and attempt_no = :attempt_no
                        """
                    ),
                    {"document_id": document_id, "attempt_no": attempt_no},
                )
                connection.execute(
                    text(
                        """
                        update public.source_documents
                        set status = 'parsed', detected_mime_type = :content_type,
                            parser_version = :parser_version, parsed_at = now(),
                            failure_code = null, ocr_used = :ocr_used
                        where id = :document_id
                        """
                    ),
                    {
                        "document_id": document_id,
                        "content_type": parsed.detected_content_type,
                        "parser_version": PARSER_VERSION,
                        "ocr_used": any(
                            fragment.locator.get("ocr") is True for fragment in parsed.fragments
                        ),
                    },
                )
            return UploadedDocument(
                id=document_id,
                file_name=safe_name,
                object_key=object_key,
                status="parsed",
                fragment_count=len(parsed.fragments),
            )
        raise DocumentRejected("DOCUMENT_PARSING_FAILED")

    def _record_failed_attempt(
        self,
        *,
        document_id: UUID,
        attempt_no: int,
        error_code: str,
        retryable: bool,
    ) -> None:
        document_status = "failed" if retryable else "rejected"
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.document_parse_attempts
                    set status = 'failed', error_code = :error_code,
                        retryable = :retryable, completed_at = now()
                    where source_document_id = :document_id
                      and attempt_no = :attempt_no
                    """
                ),
                {
                    "document_id": document_id,
                    "attempt_no": attempt_no,
                    "error_code": error_code,
                    "retryable": retryable,
                },
            )
            connection.execute(
                text(
                    """
                    update public.source_documents
                    set status = :status, failure_code = :error_code
                    where id = :document_id
                    """
                ),
                {
                    "document_id": document_id,
                    "status": document_status,
                    "error_code": error_code,
                },
            )
