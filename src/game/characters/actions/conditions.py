"""Reusable, data-driven action conditions."""

from __future__ import annotations

from dataclasses import dataclass

from .definitions import ActionContext


@dataclass(frozen=True)
class BooleanCondition:
    """Checks a boolean value in ActionContext."""

    key: str
    expected: bool

    def __post_init__(self) -> None:
        if not self.key:
            raise ValueError("key cannot be empty")


@dataclass(frozen=True)
class ScalarCondition:
    """Compares a scalar value in ActionContext."""

    key: str
    operator: str
    value: float

    def __post_init__(self) -> None:
        if not self.key:
            raise ValueError("key cannot be empty")

        if self.operator not in {"==", "!=", ">", ">=", "<", "<="}:
            raise ValueError(
                f"unsupported scalar condition operator: {self.operator}"
            )


class ConditionEvaluator:
    """Evaluates reusable conditions against an ActionContext."""

    @staticmethod
    def evaluate(
        condition: BooleanCondition | ScalarCondition,
        context: ActionContext,
    ) -> bool:
        if isinstance(condition, BooleanCondition):
            current = context.boolean_values.get(condition.key)

            if current is None:
                return False

            return current == condition.expected

        if isinstance(condition, ScalarCondition):
            current = context.scalar_values.get(condition.key)

            if current is None:
                return False

            if condition.operator == "==":
                return current == condition.value

            if condition.operator == "!=":
                return current != condition.value

            if condition.operator == ">":
                return current > condition.value

            if condition.operator == ">=":
                return current >= condition.value

            if condition.operator == "<":
                return current < condition.value

            if condition.operator == "<=":
                return current <= condition.value

        raise TypeError(
            f"unsupported condition type: {type(condition).__name__}"
        )
