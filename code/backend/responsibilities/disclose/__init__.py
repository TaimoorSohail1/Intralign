"""Disclose — exposure of derived cognition to surfaces (via render service). Consume only; produces no canonical fact."""

from backend.responsibilities.disclose.projection_writer import (
    ProjectionMaterializer,
    chr_to_projection_row,
    projection_id_for,
    projection_subject,
)

__all__ = [
    "ProjectionMaterializer",
    "chr_to_projection_row",
    "projection_id_for",
    "projection_subject",
]
