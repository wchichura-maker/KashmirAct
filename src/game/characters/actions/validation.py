"""Validation contracts for the P0.5 Action System."""

from __future__ import annotations

from dataclasses import dataclass

from .definitions import ActionDefinition


@dataclass(frozen=True)
class ActionValidationResult:
    """Result of validating an action definition."""

    valid: bool
    errors: tuple[str, ...] = ()


class ActionValidator:
    """Validates action definitions without executing them."""

    def validate(self, definition: ActionDefinition) -> ActionValidationResult:
        errors: list[str] = []

        if not definition.action_id:
            errors.append("action_id cannot be empty")

        if not definition.composition_id:
            errors.append("composition_id cannot be empty")

        if not definition.phases:
            errors.append("action must contain at least one phase")

        for phase in definition.cancel_windows:
            if phase not in definition.phases:
                errors.append(
                    f"cancel window phase is not part of action phases: {phase.value}"
                )

        for transition in definition.transitions:
            if transition.from_action != definition.action_id:
                errors.append(
                    "transition from_action does not match definition action_id"
                )

        return ActionValidationResult(
            valid=not errors,
            errors=tuple(errors),
        )
