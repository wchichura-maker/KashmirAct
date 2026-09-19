from __future__ import annotations

from .conditions import ConditionEvaluator
from .definitions import ActionContext, ActionDefinition


class ActionTransitionResolver:
    def __init__(self, actions: dict[str, ActionDefinition]) -> None:
        self._actions = actions

    def action(self, action_id: str) -> ActionDefinition | None:
        return self._actions.get(action_id)

    def resolve(
        self,
        current_action: str,
        elapsed_time: float,
        context: ActionContext,
    ) -> tuple[str, ...]:
        definition = self._actions.get(current_action)

        if definition is None:
            return ()

        context_tags = set(context.tags)
        valid: list[tuple[int, str]] = []

        for transition in definition.transitions:
            if transition.from_action != current_action:
                continue

            if elapsed_time < transition.min_time:
                continue

            if (
                transition.max_time is not None
                and elapsed_time > transition.max_time
            ):
                continue

            if not all(tag in context_tags for tag in transition.required_tags):
                continue

            if any(tag in context_tags for tag in transition.blocked_tags):
                continue

            if not all(
                ConditionEvaluator.evaluate(condition, context)
                for condition in transition.conditions
            ):
                continue

            valid.append((transition.priority, transition.to_action))

        valid.sort(key=lambda item: (-item[0], item[1]))

        return tuple(action_id for _, action_id in valid)
