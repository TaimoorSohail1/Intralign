"""Project-command + evidence/artifact request bodies (DTM-0034; API Contract §5).

Response DTOs are the canonical ``Project`` entity (``shared.entities``, Data
Model v1.2 §7 verbatim) for the project commands; the evidence/artifact intake
commands return the persisted intake ``artifact`` row (the LDM §2.3 evidence
anchor) as produced by the EXISTING ``submit_artifact`` seam — only the INPUT
shapes live here.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class CreateProjectRequest(BaseModel):
    """``POST /projects`` body — ``{title?, description?}`` (§5)."""

    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    description: str | None = None


class UpdateProjectRequest(BaseModel):
    """``PATCH /projects/{pid}`` body — ``{title?, description?}`` (§5).

    Metadata-only patch (the lifecycle is moved by the engine / the archive
    command, never by this patch).
    """

    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    description: str | None = None


class AddEvidenceRequest(BaseModel):
    """``POST /projects/{pid}/evidence`` body — ``{source_type, content_ref, provenance?}``.

    ``source_type`` is the evidence-source kind (mapped to the intake ``source``);
    ``content_ref`` is the submitted body/reference (the intake ``content``).
    ``provenance`` is optional extra attribution preserved alongside the
    intake-derived who/when/from-where.
    """

    model_config = ConfigDict(extra="forbid")

    source_type: str
    content_ref: str
    provenance: dict | None = None


class CreateArtifactRequest(BaseModel):
    """``POST /projects/{pid}/artifacts`` body — ``{artifact_type, content}`` (§5)."""

    model_config = ConfigDict(extra="forbid")

    artifact_type: str
    content: str


class CreateArtifactVersionRequest(BaseModel):
    """``POST /artifacts/{aid}/versions`` body — ``{content, authored_by_kind?}`` (§5).

    A re-submission of the parent artifact's source with new ``content`` — the
    intake seam appends a NEW artifact version (``version+1``/``supersedes_id``).
    """

    model_config = ConfigDict(extra="forbid")

    content: str
    authored_by_kind: str | None = None
