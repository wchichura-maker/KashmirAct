"""Immutable core events (P0 spec §29–§30).

Published events cannot be mutated. Optional fields are None when irrelevant.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from core.contracts import reasons
from core.contracts.result import ValidationResult, fail, ok
from core.events.types import KNOWN_EVENT_TYPES

_PAYLOAD_TYPES = (type(None), str, int, float, bool)


def _freeze_payload(payload: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if payload is None:
        return MappingProxyType({})
    frozen: dict[str, Any] = {}
    for key, value in payload.items():
        if not isinstance(key, str):
            raise TypeError("payload keys must be strings")
        if isinstance(value, (list, tuple)):
            frozen[key] = tuple(value)
        else:
            frozen[key] = value
    return MappingProxyType(frozen)


@dataclass(frozen=True)
class CoreEvent:
    event_id: str
    event_type: str
    sequence: int
    session_id: str | None = None
    timestamp: float | None = None
    actor_id: str | None = None
    target_id: str | None = None
    action_id: str | None = None
    primitive_id: str | None = None
    attack_id: str | None = None
    weapon_id: str | None = None
    position: tuple[float, float, float] | None = None
    direction: tuple[float, float, float] | None = None
    distance_to_target: float | None = None
    stamina_before: float | None = None
    stamina_after: float | None = None
    result: str | None = None
    payload: Mapping[str, Any] = MappingProxyType({})


def validate_event(event: CoreEvent) -> ValidationResult:
    if event.event_type not in KNOWN_EVENT_TYPES:
        return fail(
            reasons.UNKNOWN_EVENT_TYPE,
            message=f"unknown event type '{event.event_type}'",
            operation="validate_event",
            data_id=event.event_id,
            entity=event.actor_id,
        )
    if not event.event_id:
        return fail(reasons.INVALID_ID, message="event_id is required", operation="validate_event")
    for key, value in dict(event.payload).items():
        if isinstance(value, tuple):
            if not all(isinstance(item, _PAYLOAD_TYPES) for item in value):
                return fail(
                    reasons.INVALID_PAYLOAD,
                    message=f"payload '{key}' contains a non-scalar item",
                    operation="validate_event",
                    data_id=event.event_id,
                )
        elif not isinstance(value, _PAYLOAD_TYPES):
            return fail(
                reasons.INVALID_PAYLOAD,
                message=f"payload '{key}' is not a scalar",
                operation="validate_event",
                data_id=event.event_id,
            )
    return ok(operation="validate_event", data_id=event.event_id, entity=event.actor_id)


def build_event(
    *,
    event_id: str,
    event_type: str,
    sequence: int,
    session_id: str | None = None,
    timestamp: float | None = None,
    actor_id: str | None = None,
    target_id: str | None = None,
    action_id: str | None = None,
    primitive_id: str | None = None,
    attack_id: str | None = None,
    weapon_id: str | None = None,
    position: tuple[float, float, float] | None = None,
    direction: tuple[float, float, float] | None = None,
    distance_to_target: float | None = None,
    stamina_before: float | None = None,
    stamina_after: float | None = None,
    result: str | None = None,
    payload: Mapping[str, Any] | None = None,
) -> CoreEvent:
    return CoreEvent(
        event_id=event_id,
        event_type=event_type,
        sequence=sequence,
        session_id=session_id,
        timestamp=timestamp,
        actor_id=actor_id,
        target_id=target_id,
        action_id=action_id,
        primitive_id=primitive_id,
        attack_id=attack_id,
        weapon_id=weapon_id,
        position=position,
        direction=direction,
        distance_to_target=distance_to_target,
        stamina_before=stamina_before,
        stamina_after=stamina_after,
        result=result,
        payload=_freeze_payload(payload),
    )
