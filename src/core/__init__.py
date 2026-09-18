"""KashmirAct Core — engine-independent rules, data, IDs, and events."""

from core.contracts.result import OpResult, ValidationResult
from core.data.attributes import AttributeDefinition, AttributeRuntime
from core.data.catalog import SCHEMA_VERSION, CoreCatalog
from core.events.bus import EventBus
from core.events.event import CoreEvent
from core.ids.entity_id import EntityId, EntityTypeRegistry
from core.rules.validator import RuleValidator

__all__ = [
    "SCHEMA_VERSION",
    "AttributeDefinition",
    "AttributeRuntime",
    "CoreCatalog",
    "CoreEvent",
    "EntityId",
    "EntityTypeRegistry",
    "EventBus",
    "OpResult",
    "RuleValidator",
    "ValidationResult",
]
