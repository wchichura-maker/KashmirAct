"""Rule Validator — Phase 02 slice.

Validates entity IDs, attribute definitions, and event types.
Primitive / attack / weapon catalogs are not loaded yet; those checks
return explicit UNKNOWN_* codes instead of guessing.
"""

from __future__ import annotations

from core.contracts import reasons
from core.contracts.result import ValidationResult, fail
from core.data.attributes import AttributeDefinition, validate_attribute_definition
from core.data.catalog import CoreCatalog
from core.events.event import CoreEvent, validate_event
from core.ids.entity_id import EntityTypeRegistry, parse_entity_id


class RuleValidator:
    def __init__(self, catalog: CoreCatalog) -> None:
        self._catalog = catalog

    @property
    def types(self) -> EntityTypeRegistry:
        if self._catalog.entity_types is None:
            raise RuntimeError("catalog has no entity types")
        return self._catalog.entity_types

    def validate_entity_id(self, raw: str) -> ValidationResult:
        _, check = parse_entity_id(raw, self.types.types)
        return check

    def validate_attribute_definition(self, definition: AttributeDefinition) -> ValidationResult:
        id_check = self.validate_entity_id(definition.id)
        if not id_check.valid:
            return id_check
        parsed, _ = parse_entity_id(definition.id, self.types.types)
        if parsed is None or parsed.entity_type != "attribute":
            return fail(
                reasons.UNKNOWN_ENTITY_TYPE,
                message="attribute ids must use type 'attribute'",
                operation="validate_attribute_definition",
                data_id=definition.id,
            )
        return validate_attribute_definition(definition)

    def validate_event(self, event: CoreEvent) -> ValidationResult:
        return validate_event(event)

    def validate_primitive_id(self, primitive_id: str) -> ValidationResult:
        id_check = self.validate_entity_id(primitive_id)
        if not id_check.valid:
            return id_check
        return fail(
            reasons.UNKNOWN_PRIMITIVE,
            message="no primitive catalog is registered in Phase 02",
            operation="validate_primitive_id",
            data_id=primitive_id,
        )

    def validate_attack_id(self, attack_id: str) -> ValidationResult:
        id_check = self.validate_entity_id(attack_id)
        if not id_check.valid:
            return id_check
        return fail(
            reasons.UNKNOWN_ATTACK,
            message="no attack catalog is registered in Phase 02",
            operation="validate_attack_id",
            data_id=attack_id,
        )

    def validate_weapon_id(self, weapon_id: str) -> ValidationResult:
        id_check = self.validate_entity_id(weapon_id)
        if not id_check.valid:
            return id_check
        return fail(
            reasons.UNKNOWN_WEAPON,
            message="no weapon catalog is registered in Phase 02",
            operation="validate_weapon_id",
            data_id=weapon_id,
        )

    def require_known_attribute(self, attribute_id: str) -> ValidationResult:
        _, check = self._catalog.get_attribute(attribute_id)
        return check
