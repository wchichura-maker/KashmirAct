"""Attribute definitions and runtime (P0 spec §7, §26).

Stamina clamp, consume, and regenerate live here as attribute operations.
Action gating that *uses* stamina belongs to later combat phases.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.contracts import reasons
from core.contracts.result import OpResult, fail, ok

EPS = 1e-9


def _finite(value: float) -> bool:
    return isinstance(value, (int, float)) and value == value and value not in (float("inf"), float("-inf"))


@dataclass(frozen=True)
class AttributeDefinition:
    id: str
    display_name: str
    min_value: float
    max_value: float
    default_value: float


def validate_attribute_definition(definition: AttributeDefinition) -> ValidationResult:
    if not definition.id:
        return fail(reasons.INVALID_ID, message="attribute definition id is required", operation="validate_definition")
    if not definition.display_name:
        return fail(
            reasons.MISSING_FIELD,
            message="display_name is required",
            operation="validate_definition",
            data_id=definition.id,
        )
    if not all(_finite(v) for v in (definition.min_value, definition.max_value, definition.default_value)):
        return fail(
            reasons.INVALID_ATTRIBUTE_VALUE,
            message="attribute bounds must be finite numbers",
            operation="validate_definition",
            data_id=definition.id,
        )
    if definition.min_value > definition.max_value:
        return fail(
            reasons.INVALID_ATTRIBUTE_BOUNDS,
            message="min_value cannot exceed max_value",
            operation="validate_definition",
            data_id=definition.id,
        )
    if definition.default_value < definition.min_value or definition.default_value > definition.max_value:
        return fail(
            reasons.INVALID_ATTRIBUTE_BOUNDS,
            message="default_value is outside [min_value, max_value]",
            operation="validate_definition",
            data_id=definition.id,
        )
    return ok(operation="validate_definition", data_id=definition.id)


class AttributeRuntime:
    def __init__(
        self,
        definition: AttributeDefinition,
        *,
        current_value: float | None = None,
        max_value: float | None = None,
        regeneration_rate: float = 0.0,
    ) -> None:
        check = validate_attribute_definition(definition)
        if not check.valid:
            raise ValueError(check.message)
        self._definition = definition
        self.definition_id = definition.id
        self.max_value = definition.max_value if max_value is None else float(max_value)
        if not _finite(self.max_value) or self.max_value < definition.min_value or self.max_value > definition.max_value:
            raise ValueError("runtime max_value is outside the definition bounds")
        if not _finite(regeneration_rate):
            raise ValueError("regeneration_rate must be finite")
        self.regeneration_rate = float(regeneration_rate)
        initial = definition.default_value if current_value is None else float(current_value)
        self._current = self._clamp(initial)

    @property
    def definition(self) -> AttributeDefinition:
        return self._definition

    def get_value(self) -> float:
        return self._current

    def set_value(self, value: float) -> OpResult:
        if not _finite(value):
            return OpResult(
                ok=False,
                reason_code=reasons.INVALID_ATTRIBUTE_VALUE,
                value=self._current,
                validation=fail(
                    reasons.INVALID_ATTRIBUTE_VALUE,
                    message="set_value requires a finite number",
                    operation="set_value",
                    data_id=self.definition_id,
                ),
            )
        self._current = self._clamp(float(value))
        return OpResult(ok=True, value=self._current, validation=ok(operation="set_value", data_id=self.definition_id))

    def modify(self, delta: float) -> OpResult:
        if not _finite(delta):
            return OpResult(
                ok=False,
                reason_code=reasons.INVALID_ATTRIBUTE_VALUE,
                value=self._current,
                validation=fail(
                    reasons.INVALID_ATTRIBUTE_VALUE,
                    message="modify requires a finite delta",
                    operation="modify",
                    data_id=self.definition_id,
                ),
            )
        return self.set_value(self._current + float(delta))

    def consume(self, amount: float) -> OpResult:
        if not _finite(amount) or amount < 0:
            return OpResult(
                ok=False,
                reason_code=reasons.NEGATIVE_AMOUNT,
                value=self._current,
                validation=fail(
                    reasons.NEGATIVE_AMOUNT,
                    message="consume amount must be a finite value >= 0",
                    operation="consume",
                    data_id=self.definition_id,
                ),
            )
        if amount > self._current + EPS:
            return OpResult(
                ok=False,
                reason_code=reasons.INSUFFICIENT_ATTRIBUTE,
                value=self._current,
                validation=fail(
                    reasons.INSUFFICIENT_ATTRIBUTE,
                    message="insufficient attribute value",
                    operation="consume",
                    data_id=self.definition_id,
                ),
            )
        self._current = self._clamp(self._current - float(amount))
        return OpResult(ok=True, value=self._current, validation=ok(operation="consume", data_id=self.definition_id))

    def regenerate(self, dt: float) -> OpResult:
        if not _finite(dt) or dt < 0:
            return OpResult(
                ok=False,
                reason_code=reasons.NEGATIVE_DELTA_TIME,
                value=self._current,
                validation=fail(
                    reasons.NEGATIVE_DELTA_TIME,
                    message="regenerate dt must be a finite value >= 0",
                    operation="regenerate",
                    data_id=self.definition_id,
                ),
            )
        return self.modify(self.regeneration_rate * float(dt))

    def is_empty(self) -> bool:
        return self._current <= self._definition.min_value + EPS

    def is_full(self) -> bool:
        return self._current >= self.max_value - EPS

    def _clamp(self, value: float) -> float:
        lo = self._definition.min_value
        hi = self.max_value
        if value < lo + EPS:
            return lo
        if value > hi - EPS:
            return hi
        return value
