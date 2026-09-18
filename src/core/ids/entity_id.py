"""Entity identifiers (P0 spec §8).

Format: `{entity_type}_{unique}`

IDs are not derived from display names and stay stable when names change.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from core.contracts import reasons
from core.contracts.result import ValidationResult, fail, ok

_TYPE_RE = re.compile(r"^[a-z][a-z0-9]*$")
_UNIQUE_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
_ID_RE = re.compile(r"^[a-z][a-z0-9_]{1,127}$")


@dataclass(frozen=True)
class EntityId:
    entity_type: str
    unique: str

    def value(self) -> str:
        return f"{self.entity_type}_{self.unique}"

    def __str__(self) -> str:
        return self.value()


class EntityTypeRegistry:
    def __init__(self, types: Iterable[str]):
        normalized = tuple(types)
        check = _validate_type_set(normalized)
        if not check.valid:
            raise ValueError(check.message)
        self._types = frozenset(normalized)

    @property
    def types(self) -> frozenset[str]:
        return self._types

    def has(self, entity_type: str) -> bool:
        return entity_type in self._types

    def parse(self, raw: str) -> tuple[EntityId | None, ValidationResult]:
        return parse_entity_id(raw, self._types)

    def make(self, entity_type: str, unique: str, *, display_name: str | None = None) -> tuple[EntityId | None, ValidationResult]:
        return make_entity_id(entity_type, unique, self._types, display_name=display_name)

    def extend(self, extra_types: Iterable[str]) -> "EntityTypeRegistry":
        """Return a new registry with additional types. Does not modify Core source."""
        return EntityTypeRegistry(set(self._types) | set(extra_types))


def _validate_type_set(types: Iterable[str]) -> ValidationResult:
    items = list(types)
    if not items:
        return fail(reasons.UNKNOWN_ENTITY_TYPE, message="entity type registry is empty", operation="register_types")
    seen: set[str] = set()
    for item in items:
        if item in seen:
            return fail(reasons.DUPLICATE_ID, message=f"duplicate entity type '{item}'", operation="register_types", data_id=item)
        if not _TYPE_RE.fullmatch(item):
            return fail(reasons.UNKNOWN_ENTITY_TYPE, message=f"illegal entity type '{item}'", operation="register_types", data_id=item)
        seen.add(item)
    for a in items:
        for b in items:
            if a != b and b.startswith(a + "_"):
                return fail(
                    reasons.AMBIGUOUS_ENTITY_TYPE,
                    message=f"entity type '{a}' is a prefix of '{b}'",
                    operation="register_types",
                    data_id=a,
                )
    return ok(operation="register_types")


def make_entity_id(
    entity_type: str,
    unique: str,
    known_types: Iterable[str],
    *,
    display_name: str | None = None,
) -> tuple[EntityId | None, ValidationResult]:
    known = frozenset(known_types)
    if entity_type not in known:
        return None, fail(
            reasons.UNKNOWN_ENTITY_TYPE,
            message=f"unknown entity type '{entity_type}'",
            operation="make_id",
            data_id=entity_type,
        )
    if not _UNIQUE_RE.fullmatch(unique):
        return None, fail(
            reasons.INVALID_ID,
            message=f"unique identifier '{unique}' is not a stable lowercase token",
            operation="make_id",
            data_id=f"{entity_type}_{unique}",
        )
    if display_name is not None and _slug(display_name) == unique:
        return None, fail(
            reasons.ID_DERIVED_FROM_DISPLAY_NAME,
            message="IDs must not be derived from display names",
            operation="make_id",
            data_id=f"{entity_type}_{unique}",
        )
    entity = EntityId(entity_type=entity_type, unique=unique)
    return entity, ok(operation="make_id", data_id=entity.value())


def parse_entity_id(raw: str, known_types: Iterable[str]) -> tuple[EntityId | None, ValidationResult]:
    if not isinstance(raw, str) or not _ID_RE.fullmatch(raw):
        return None, fail(
            reasons.INVALID_ID,
            message=f"illegal entity id '{raw}'",
            operation="parse_id",
            data_id=str(raw),
        )
    known = frozenset(known_types)
    matches = [t for t in known if raw.startswith(t + "_")]
    if not matches:
        prefix = raw.split("_", 1)[0]
        return None, fail(
            reasons.UNKNOWN_ENTITY_TYPE,
            message=f"no registered entity type in '{raw}'",
            operation="parse_id",
            entity=raw,
            data_id=prefix,
        )
    entity_type = max(matches, key=len)
    unique = raw[len(entity_type) + 1 :]
    if not unique or not _UNIQUE_RE.fullmatch(unique):
        return None, fail(
            reasons.INVALID_ID,
            message=f"entity id '{raw}' has an empty or illegal unique part",
            operation="parse_id",
            data_id=raw,
        )
    return EntityId(entity_type=entity_type, unique=unique), ok(operation="parse_id", data_id=raw)


def _slug(display_name: str) -> str:
    token = re.sub(r"[^a-z0-9]+", "_", display_name.strip().lower()).strip("_")
    return token
