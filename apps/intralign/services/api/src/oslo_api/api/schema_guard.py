from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from fastapi import FastAPI


class PublicSchemaViolation(RuntimeError):
    """Raised when a public DTO exposes a prohibited numeric assessment value."""


_ASSESSMENT_TERMS = re.compile(r"\b(?:confidence|maturity)\b", re.IGNORECASE)
_NUMERIC_TYPES = {"integer", "number"}


def validate_public_schema(schema: Mapping[str, Any]) -> None:
    """Reject numeric confidence or maturity values anywhere in public OpenAPI."""

    components = schema.get("components", {}).get("schemas", {})

    def resolve(reference: str) -> Mapping[str, Any] | None:
        prefix = "#/components/schemas/"
        if not reference.startswith(prefix):
            return None
        target = components.get(reference.removeprefix(prefix))
        return target if isinstance(target, Mapping) else None

    def allows_numeric(
        candidate: Mapping[str, Any],
        visited_references: frozenset[str] = frozenset(),
    ) -> bool:
        declared_type = candidate.get("type")
        if declared_type in _NUMERIC_TYPES:
            return True
        if isinstance(declared_type, list) and _NUMERIC_TYPES.intersection(declared_type):
            return True
        if any(
            isinstance(value, (int, float)) and not isinstance(value, bool)
            for value in candidate.get("enum", ())
        ):
            return True
        constant = candidate.get("const")
        if isinstance(constant, (int, float)) and not isinstance(constant, bool):
            return True
        reference = candidate.get("$ref")
        if isinstance(reference, str) and reference not in visited_references:
            target = resolve(reference)
            if target is not None and allows_numeric(
                target, visited_references | {reference}
            ):
                return True
        return any(
            isinstance(option, Mapping)
            and allows_numeric(option, visited_references)
            for keyword in ("allOf", "anyOf", "oneOf")
            for option in candidate.get(keyword, ())
        )

    def walk(node: Any, path: str) -> None:
        if isinstance(node, Mapping):
            properties = node.get("properties")
            if isinstance(properties, Mapping):
                for name, property_schema in properties.items():
                    if not isinstance(property_schema, Mapping):
                        continue
                    semantic_text = " ".join(
                        str(value)
                        for value in (
                            name,
                            property_schema.get("title", ""),
                            property_schema.get("description", ""),
                        )
                    )
                    if _ASSESSMENT_TERMS.search(semantic_text) and allows_numeric(
                        property_schema
                    ):
                        raise PublicSchemaViolation(
                            "Public OpenAPI exposes prohibited numeric confidence or "
                            f"maturity at {path}.properties.{name}"
                        )
            for key, value in node.items():
                walk(value, f"{path}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{path}[{index}]")

    walk(schema, "$")


def install_public_schema_guard(app: FastAPI) -> None:
    """Validate every generated public OpenAPI document before it is served."""

    generate_openapi = app.openapi

    def guarded_openapi() -> dict[str, Any]:
        schema = generate_openapi()
        validate_public_schema(schema)
        return schema

    app.openapi = guarded_openapi
    guarded_openapi()
