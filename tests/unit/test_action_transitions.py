import unittest

from src.game.characters.actions.definitions import (
    ActionContext,
    ActionDefinition,
    ActionPhase,
    TransitionRule,
)
from src.game.characters.actions.transitions import ActionTransitionResolver


class ActionTransitionResolverTests(unittest.TestCase):

    def setUp(self):
        self.actions = {
            "step": ActionDefinition(
                action_id="step",
                phases=(ActionPhase.EXECUTION,),
                composition_id="step.composition",
                transitions=(
                    TransitionRule(
                        from_action="step",
                        to_action="lunge",
                    ),
                ),
            ),
            "lunge": ActionDefinition(
                action_id="lunge",
                phases=(ActionPhase.EXECUTION,),
                composition_id="lunge.composition",
                transitions=(
                    TransitionRule(
                        from_action="lunge",
                        to_action="dodge",
                        min_time=0.5,
                    ),
                ),
            ),
            "dodge": ActionDefinition(
                action_id="dodge",
                phases=(ActionPhase.EXECUTION,),
                composition_id="dodge.composition",
                transitions=(
                    TransitionRule(
                        from_action="dodge",
                        to_action="step",
                    ),
                ),
            ),
        }

        self.resolver = ActionTransitionResolver(self.actions)

    def test_valid_transition_is_returned(self):
        result = self.resolver.resolve(
            current_action="step",
            elapsed_time=0.1,
            context=ActionContext(),
        )

        self.assertEqual(result, ("lunge",))

    def test_transition_respects_min_time(self):
        result = self.resolver.resolve(
            current_action="lunge",
            elapsed_time=0.2,
            context=ActionContext(),
        )

        self.assertEqual(result, ())

    def test_transition_becomes_valid_after_min_time(self):
        result = self.resolver.resolve(
            current_action="lunge",
            elapsed_time=0.5,
            context=ActionContext(),
        )

        self.assertEqual(result, ("dodge",))

    def test_unknown_action_has_no_transitions(self):
        result = self.resolver.resolve(
            current_action="unknown",
            elapsed_time=0.0,
            context=ActionContext(),
        )

        self.assertEqual(result, ())

    def test_transition_respects_max_time(self):
        actions = {
            "step": ActionDefinition(
                action_id="step",
                phases=(ActionPhase.EXECUTION,),
                composition_id="step.composition",
                transitions=(
                    TransitionRule(
                        from_action="step",
                        to_action="lunge",
                        max_time=0.5,
                    ),
                ),
            )
        }

        resolver = ActionTransitionResolver(actions)

        self.assertEqual(
            resolver.resolve(
                current_action="step",
                elapsed_time=0.5,
                context=ActionContext(),
            ),
            ("lunge",),
        )

        self.assertEqual(
            resolver.resolve(
                current_action="step",
                elapsed_time=0.51,
                context=ActionContext(),
            ),
            (),
        )

    def test_transition_resolution_is_deterministic(self):
        first = self.resolver.resolve(
            current_action="step",
            elapsed_time=0.1,
            context=ActionContext(),
        )

        second = self.resolver.resolve(
            current_action="step",
            elapsed_time=0.1,
            context=ActionContext(),
        )

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
