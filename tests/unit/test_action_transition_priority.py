import unittest

from src.game.characters.actions.definitions import (
    ActionContext,
    ActionDefinition,
    ActionPhase,
    TransitionRule,
)
from src.game.characters.actions.transitions import ActionTransitionResolver


class ActionTransitionPriorityTests(unittest.TestCase):

    def test_higher_priority_transition_is_returned_first(self):
        actions = {
            "run": ActionDefinition(
                action_id="run",
                phases=(ActionPhase.EXECUTION,),
                composition_id="run.composition",
                transitions=(
                    TransitionRule(
                        from_action="run",
                        to_action="attack",
                        priority=5,
                    ),
                    TransitionRule(
                        from_action="run",
                        to_action="dodge",
                        priority=10,
                    ),
                    TransitionRule(
                        from_action="run",
                        to_action="jump",
                        priority=1,
                    ),
                ),
            )
        }

        resolver = ActionTransitionResolver(actions)

        result = resolver.resolve(
            current_action="run",
            elapsed_time=0.0,
            context=ActionContext(),
        )

        self.assertEqual(
            result,
            ("dodge", "attack", "jump"),
        )

    def test_same_priority_uses_deterministic_action_order(self):
        actions = {
            "run": ActionDefinition(
                action_id="run",
                phases=(ActionPhase.EXECUTION,),
                composition_id="run.composition",
                transitions=(
                    TransitionRule(
                        from_action="run",
                        to_action="z_action",
                        priority=5,
                    ),
                    TransitionRule(
                        from_action="run",
                        to_action="a_action",
                        priority=5,
                    ),
                ),
            )
        }

        resolver = ActionTransitionResolver(actions)

        result = resolver.resolve(
            current_action="run",
            elapsed_time=0.0,
            context=ActionContext(),
        )

        self.assertEqual(
            result,
            ("a_action", "z_action"),
        )

    def test_invalid_transition_does_not_affect_priority_order(self):
        actions = {
            "run": ActionDefinition(
                action_id="run",
                phases=(ActionPhase.EXECUTION,),
                composition_id="run.composition",
                transitions=(
                    TransitionRule(
                        from_action="run",
                        to_action="blocked",
                        priority=100,
                        required_tags=("missing",),
                    ),
                    TransitionRule(
                        from_action="run",
                        to_action="attack",
                        priority=5,
                    ),
                    TransitionRule(
                        from_action="run",
                        to_action="dodge",
                        priority=10,
                    ),
                ),
            )
        }

        resolver = ActionTransitionResolver(actions)

        result = resolver.resolve(
            current_action="run",
            elapsed_time=0.0,
            context=ActionContext(),
        )

        self.assertEqual(
            result,
            ("dodge", "attack"),
        )

    def test_priority_resolution_is_deterministic(self):
        actions = {
            "run": ActionDefinition(
                action_id="run",
                phases=(ActionPhase.EXECUTION,),
                composition_id="run.composition",
                transitions=(
                    TransitionRule(
                        from_action="run",
                        to_action="attack",
                        priority=5,
                    ),
                    TransitionRule(
                        from_action="run",
                        to_action="dodge",
                        priority=10,
                    ),
                ),
            )
        }

        resolver = ActionTransitionResolver(actions)

        first = resolver.resolve(
            current_action="run",
            elapsed_time=0.0,
            context=ActionContext(),
        )

        second = resolver.resolve(
            current_action="run",
            elapsed_time=0.0,
            context=ActionContext(),
        )

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
