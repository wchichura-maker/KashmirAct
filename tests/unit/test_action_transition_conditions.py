import unittest

from src.game.characters.actions.conditions import BooleanCondition, ScalarCondition
from src.game.characters.actions.definitions import (
    ActionContext,
    ActionDefinition,
    ActionPhase,
    TransitionRule,
)
from src.game.characters.actions.transitions import ActionTransitionResolver


class ActionTransitionConditionTests(unittest.TestCase):

    def test_boolean_condition_controls_transition(self):
        actions = {
            "step": ActionDefinition(
                action_id="step",
                phases=(ActionPhase.EXECUTION,),
                composition_id="step.composition",
                transitions=(
                    TransitionRule(
                        from_action="step",
                        to_action="lunge",
                        conditions=(
                            BooleanCondition(
                                key="grounded",
                                expected=True,
                            ),
                        ),
                    ),
                ),
            )
        }

        resolver = ActionTransitionResolver(actions)

        valid = resolver.resolve(
            current_action="step",
            elapsed_time=0.0,
            context=ActionContext(
                boolean_values={"grounded": True},
            ),
        )

        invalid = resolver.resolve(
            current_action="step",
            elapsed_time=0.0,
            context=ActionContext(
                boolean_values={"grounded": False},
            ),
        )

        self.assertEqual(valid, ("lunge",))
        self.assertEqual(invalid, ())

    def test_scalar_condition_controls_transition(self):
        actions = {
            "run": ActionDefinition(
                action_id="run",
                phases=(ActionPhase.EXECUTION,),
                composition_id="run.composition",
                transitions=(
                    TransitionRule(
                        from_action="run",
                        to_action="jump_attack",
                        conditions=(
                            ScalarCondition(
                                key="speed",
                                operator=">=",
                                value=5.0,
                            ),
                        ),
                    ),
                ),
            )
        }

        resolver = ActionTransitionResolver(actions)

        valid = resolver.resolve(
            current_action="run",
            elapsed_time=0.0,
            context=ActionContext(
                scalar_values={"speed": 5.0},
            ),
        )

        invalid = resolver.resolve(
            current_action="run",
            elapsed_time=0.0,
            context=ActionContext(
                scalar_values={"speed": 4.99},
            ),
        )

        self.assertEqual(valid, ("jump_attack",))
        self.assertEqual(invalid, ())

    def test_all_conditions_must_be_true(self):
        actions = {
            "action": ActionDefinition(
                action_id="action",
                phases=(ActionPhase.EXECUTION,),
                composition_id="action.composition",
                transitions=(
                    TransitionRule(
                        from_action="action",
                        to_action="next",
                        conditions=(
                            BooleanCondition(
                                key="grounded",
                                expected=True,
                            ),
                            ScalarCondition(
                                key="speed",
                                operator=">",
                                value=5.0,
                            ),
                        ),
                    ),
                ),
            )
        }

        resolver = ActionTransitionResolver(actions)

        valid = resolver.resolve(
            current_action="action",
            elapsed_time=0.0,
            context=ActionContext(
                boolean_values={"grounded": True},
                scalar_values={"speed": 6.0},
            ),
        )

        invalid = resolver.resolve(
            current_action="action",
            elapsed_time=0.0,
            context=ActionContext(
                boolean_values={"grounded": True},
                scalar_values={"speed": 4.0},
            ),
        )

        self.assertEqual(valid, ("next",))
        self.assertEqual(invalid, ())


if __name__ == "__main__":
    unittest.main()
