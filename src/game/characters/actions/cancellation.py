"""Deterministic cancellation validation for actions."""

from __future__ import annotations

from .definitions import ActionDefinition, ActionPhase


class ActionCancellationResolver:
    """Determines whether an action may be cancelled in a given phase."""

    def can_cancel(
        self,
        action: ActionDefinition,
        phase: ActionPhase,
    ) -> bool:
        if not action.cancellable:
            return False

        return phase in action.cancel_windows
