"""In-memory event bus. Observes; does not mutate gameplay state."""

from __future__ import annotations

from collections.abc import Callable, Sequence

from core.contracts import reasons
from core.contracts.result import ValidationResult, fail
from core.events.event import CoreEvent, build_event, validate_event
from core.ids.entity_id import EntityTypeRegistry


class EventBus:
    def __init__(self, types: EntityTypeRegistry, *, session_id: str | None = None) -> None:
        self._types = types
        self._session_id = session_id
        self._events: list[CoreEvent] = []
        self._subscribers: list[Callable[[CoreEvent], None]] = []
        self._next_index = 1

    @property
    def session_id(self) -> str | None:
        return self._session_id

    def set_session(self, session_id: str) -> ValidationResult:
        parsed, parsed_check = self._types.parse(session_id)
        if parsed_check.valid and parsed is not None:
            if parsed.entity_type != "session":
                return fail(
                    reasons.UNKNOWN_ENTITY_TYPE,
                    message="session_id must use entity type 'session'",
                    operation="set_session",
                    data_id=session_id,
                )
            self._session_id = parsed.value()
            return parsed_check
        entity, made = self._types.make("session", session_id)
        if not made.valid or entity is None:
            return made
        self._session_id = entity.value()
        return made

    def subscribe(self, handler: Callable[[CoreEvent], None]) -> None:
        self._subscribers.append(handler)

    def publish(self, event_type: str, **fields: object) -> tuple[CoreEvent | None, ValidationResult]:
        event_id = f"event_{self._next_index:06d}"
        payload = fields.pop("payload", None)
        if payload is not None and not isinstance(payload, dict):
            return None, fail(
                reasons.INVALID_PAYLOAD,
                message="payload must be an object of scalars",
                operation="publish",
                data_id=event_id,
            )
        event = build_event(
            event_id=event_id,
            event_type=event_type,
            sequence=self._next_index,
            session_id=self._session_id,
            timestamp=_opt_float(fields.pop("timestamp", None)),
            actor_id=_opt_str(fields.pop("actor_id", None)),
            target_id=_opt_str(fields.pop("target_id", None)),
            action_id=_opt_str(fields.pop("action_id", None)),
            primitive_id=_opt_str(fields.pop("primitive_id", None)),
            attack_id=_opt_str(fields.pop("attack_id", None)),
            weapon_id=_opt_str(fields.pop("weapon_id", None)),
            position=_opt_vec3(fields.pop("position", None)),
            direction=_opt_vec3(fields.pop("direction", None)),
            distance_to_target=_opt_float(fields.pop("distance_to_target", None)),
            stamina_before=_opt_float(fields.pop("stamina_before", None)),
            stamina_after=_opt_float(fields.pop("stamina_after", None)),
            result=_opt_str(fields.pop("result", None)),
            payload=payload if isinstance(payload, dict) else None,
        )
        if fields:
            return None, fail(
                reasons.INVALID_PAYLOAD,
                message=f"unknown event fields: {sorted(fields)}",
                operation="publish",
                data_id=event_id,
            )
        check = validate_event(event)
        if not check.valid:
            return None, check
        self._events.append(event)
        self._next_index += 1
        for handler in self._subscribers:
            handler(event)
        return event, check

    def events(self) -> tuple[CoreEvent, ...]:
        return tuple(self._events)

    def event_types(self) -> Sequence[str]:
        return tuple(event.event_type for event in self._events)


def _opt_str(value: object) -> str | None:
    if value is None:
        return None
    return str(value)


def _opt_float(value: object) -> float | None:
    if value is None:
        return None
    return float(value)  # type: ignore[arg-type]


def _opt_vec3(value: object) -> tuple[float, float, float] | None:
    if value is None:
        return None
    if isinstance(value, (tuple, list)) and len(value) == 3:
        return (float(value[0]), float(value[1]), float(value[2]))
    raise TypeError("position/direction must be a 3-tuple or None")
