"""Load Core definitions from data files. Invalid data is rejected, never skipped."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.contracts import reasons
from core.contracts.result import ValidationResult, fail, ok
from core.data.attributes import AttributeDefinition, validate_attribute_definition
from core.ids.entity_id import EntityTypeRegistry

SCHEMA_VERSION = "0.1"


class CoreCatalog:
    def __init__(self) -> None:
        self.schema_version = SCHEMA_VERSION
        self.entity_types: EntityTypeRegistry | None = None
        self.attributes: dict[str, AttributeDefinition] = {}

    def load_entity_types(self, path: Path) -> ValidationResult:
        payload, error = _read_json(path, operation="load_entity_types")
        if error is not None:
            return error
        assert payload is not None
        version = payload.get("schema_version")
        if version != SCHEMA_VERSION:
            return fail(
                reasons.INVALID_DATA_FILE,
                message=f"unsupported schema_version '{version}'",
                operation="load_entity_types",
                data_id=str(path),
            )
        raw_types = payload.get("types")
        if not isinstance(raw_types, list) or not raw_types:
            return fail(
                reasons.MISSING_FIELD,
                message="types must be a non-empty list",
                operation="load_entity_types",
                data_id=str(path),
            )
        ids: list[str] = []
        for entry in raw_types:
            if not isinstance(entry, dict) or "id" not in entry:
                return fail(
                    reasons.MISSING_FIELD,
                    message="each entity type requires an id",
                    operation="load_entity_types",
                    data_id=str(path),
                )
            ids.append(str(entry["id"]))
        try:
            self.entity_types = EntityTypeRegistry(ids)
        except ValueError as exc:
            return fail(
                reasons.INVALID_DATA_FILE,
                message=str(exc),
                operation="load_entity_types",
                data_id=str(path),
            )
        return ok(operation="load_entity_types", data_id=str(path))

    def load_attributes(self, path: Path) -> ValidationResult:
        if self.entity_types is None:
            return fail(
                reasons.MISSING_FIELD,
                message="entity types must be loaded before attributes",
                operation="load_attributes",
            )
        payload, error = _read_json(path, operation="load_attributes")
        if error is not None:
            return error
        assert payload is not None
        if payload.get("schema_version") != SCHEMA_VERSION:
            return fail(
                reasons.INVALID_DATA_FILE,
                message=f"unsupported schema_version '{payload.get('schema_version')}'",
                operation="load_attributes",
                data_id=str(path),
            )
        raw = payload.get("attributes")
        if not isinstance(raw, list) or not raw:
            return fail(
                reasons.MISSING_FIELD,
                message="attributes must be a non-empty list",
                operation="load_attributes",
                data_id=str(path),
            )
        loaded: dict[str, AttributeDefinition] = {}
        for entry in raw:
            parsed, check = _parse_attribute(entry, self.entity_types)
            if not check.valid or parsed is None:
                return check
            if parsed.id in loaded:
                return fail(
                    reasons.DUPLICATE_ID,
                    message=f"duplicate attribute id '{parsed.id}'",
                    operation="load_attributes",
                    data_id=parsed.id,
                )
            loaded[parsed.id] = parsed
        self.attributes = loaded
        return ok(operation="load_attributes", data_id=str(path))

    def get_attribute(self, attribute_id: str) -> tuple[AttributeDefinition | None, ValidationResult]:
        definition = self.attributes.get(attribute_id)
        if definition is None:
            return None, fail(
                reasons.UNKNOWN_ATTRIBUTE,
                message=f"unknown attribute '{attribute_id}'",
                operation="get_attribute",
                data_id=attribute_id,
            )
        return definition, ok(operation="get_attribute", data_id=attribute_id)


def _parse_attribute(entry: Any, types: EntityTypeRegistry) -> tuple[AttributeDefinition | None, ValidationResult]:
    if not isinstance(entry, dict):
        return None, fail(reasons.INVALID_DATA_FILE, message="attribute entry must be an object", operation="load_attributes")
    required = ("id", "display_name", "min_value", "max_value", "default_value")
    for field in required:
        if field not in entry:
            return None, fail(
                reasons.MISSING_FIELD,
                message=f"missing field '{field}'",
                operation="load_attributes",
                data_id=str(entry.get("id")),
            )
    entity, id_check = types.parse(str(entry["id"]))
    if not id_check.valid or entity is None:
        return None, id_check
    if entity.entity_type != "attribute":
        return None, fail(
            reasons.UNKNOWN_ENTITY_TYPE,
            message=f"attribute id '{entry['id']}' must use entity type 'attribute'",
            operation="load_attributes",
            data_id=str(entry["id"]),
        )
    try:
        definition = AttributeDefinition(
            id=entity.value(),
            display_name=str(entry["display_name"]),
            min_value=float(entry["min_value"]),
            max_value=float(entry["max_value"]),
            default_value=float(entry["default_value"]),
        )
    except (TypeError, ValueError):
        return None, fail(
            reasons.INVALID_ATTRIBUTE_VALUE,
            message=f"attribute '{entry['id']}' has non-numeric bounds",
            operation="load_attributes",
            data_id=str(entry["id"]),
        )
    check = validate_attribute_definition(definition)
    if not check.valid:
        return None, check
    unique, name_check = types.make("attribute", entity.unique, display_name=definition.display_name)
    if unique is None:
        return None, name_check
    return definition, ok(operation="load_attributes", data_id=definition.id)


def _read_json(path: Path, *, operation: str) -> tuple[dict[str, Any] | None, ValidationResult | None]:
    if not path.is_file():
        return None, fail(
            reasons.INVALID_DATA_FILE,
            message=f"file not found: {path}",
            operation=operation,
            data_id=str(path),
        )
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, fail(
            reasons.INVALID_DATA_FILE,
            message=f"invalid JSON: {exc}",
            operation=operation,
            data_id=str(path),
        )
    if not isinstance(payload, dict):
        return None, fail(
            reasons.INVALID_DATA_FILE,
            message="JSON root must be an object",
            operation=operation,
            data_id=str(path),
        )
    return payload, None
