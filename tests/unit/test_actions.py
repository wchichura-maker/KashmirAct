import unittest

from src.game.characters.actions.definitions import (
    ActionContext,
    ActionDefinition,
    ActionPhase,
    ActionRequest,
    TransitionRule,
)
from src.game.characters.actions.validation import ActionValidator


class ActionValidationTests(unittest.TestCase):

    def setUp(self):
        self.validator = ActionValidator()

    def make_action(self, **overrides):
        data = {
            "action_id": "action.test",
            "phases": (
                ActionPhase.WINDUP,
                ActionPhase.EXECUTION,
                ActionPhase.RECOVERY,
            ),
            "composition_id": "composition.test",
        }
        data.update(overrides)
        return ActionDefinition(**data)

    def test_valid_action_is_accepted(self):
        result = self.validator.validate(self.make_action())

        self.assertTrue(result.valid)
        self.assertEqual(result.errors, ())

    def test_empty_action_id_is_rejected_by_definition(self):
        with self.assertRaises(ValueError):
            self.make_action(action_id="")

    def test_empty_composition_id_is_rejected_by_definition(self):
        with self.assertRaises(ValueError):
            self.make_action(composition_id="")

    def test_cancel_window_must_exist_in_phases(self):
        action = self.make_action(
            cancel_windows=(ActionPhase.EXECUTION,)
        )

        result = self.validator.validate(action)

        self.assertTrue(result.valid)

    def test_invalid_cancel_window_is_rejected(self):
        action = self.make_action(
            phases=(ActionPhase.EXECUTION,),
            cancel_windows=(ActionPhase.RECOVERY,),
        )

        result = self.validator.validate(action)

        self.assertFalse(result.valid)
        self.assertIn(
            "cancel window phase is not part of action phases: recovery",
            result.errors,
        )

    def test_transition_must_start_from_current_action(self):
        transition = TransitionRule(
            from_action="action.other",
            to_action="action.next",
        )

        action = self.make_action(
            transitions=(transition,),
        )

        result = self.validator.validate(action)

        self.assertFalse(result.valid)
        self.assertIn(
            "transition from_action does not match definition action_id",
            result.errors,
        )

    def test_transition_from_current_action_is_valid(self):
        transition = TransitionRule(
            from_action="action.test",
            to_action="action.next",
        )

        action = self.make_action(
            transitions=(transition,),
        )

        result = self.validator.validate(action)

        self.assertTrue(result.valid)
        self.assertEqual(result.errors, ())

    def test_validator_does_not_depend_on_specific_content(self):
        actions = (
            self.make_action(
                action_id="action.step.turn.lunge",
                composition_id="composition.step.turn.lunge",
            ),
            self.make_action(
                action_id="action.retreat.turn.lunge",
                composition_id="composition.retreat.turn.lunge",
            ),
            self.make_action(
                action_id="action.step.turn.step.turn.lunge",
                composition_id="composition.step.turn.step.turn.lunge",
            ),
        )

        for action in actions:
            result = self.validator.validate(action)

            self.assertTrue(result.valid)

    def test_context_and_request_are_independent_contracts(self):
        context = ActionContext(
            tags=("movement",),
            scalar_values={"speed": 1.0},
            boolean_values={"grounded": True},
            identifiers={"actor": "test"},
        )

        request = ActionRequest(
            action_id="action.test",
            direction_x=1.0,
            direction_y=0.0,
        )

        self.assertEqual(context.tags, ("movement",))
        self.assertEqual(request.action_id, "action.test")


if __name__ == "__main__":
    unittest.main()
