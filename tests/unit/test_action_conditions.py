import unittest

from src.game.characters.actions.conditions import (
    BooleanCondition,
    ConditionEvaluator,
    ScalarCondition,
)
from src.game.characters.actions.definitions import ActionContext


class ConditionEvaluatorTests(unittest.TestCase):

    def test_boolean_condition_is_true(self):
        condition = BooleanCondition(
            key="grounded",
            expected=True,
        )

        context = ActionContext(
            boolean_values={
                "grounded": True,
            },
        )

        self.assertTrue(
            ConditionEvaluator.evaluate(condition, context)
        )

    def test_boolean_condition_is_false_when_value_differs(self):
        condition = BooleanCondition(
            key="grounded",
            expected=True,
        )

        context = ActionContext(
            boolean_values={
                "grounded": False,
            },
        )

        self.assertFalse(
            ConditionEvaluator.evaluate(condition, context)
        )

    def test_missing_boolean_condition_is_false(self):
        condition = BooleanCondition(
            key="grounded",
            expected=True,
        )

        context = ActionContext()

        self.assertFalse(
            ConditionEvaluator.evaluate(condition, context)
        )

    def test_scalar_greater_than_condition(self):
        condition = ScalarCondition(
            key="speed",
            operator=">",
            value=5.0,
        )

        context = ActionContext(
            scalar_values={
                "speed": 6.0,
            },
        )

        self.assertTrue(
            ConditionEvaluator.evaluate(condition, context)
        )

    def test_scalar_condition_fails_when_requirement_is_not_met(self):
        condition = ScalarCondition(
            key="speed",
            operator=">",
            value=5.0,
        )

        context = ActionContext(
            scalar_values={
                "speed": 4.0,
            },
        )

        self.assertFalse(
            ConditionEvaluator.evaluate(condition, context)
        )

    def test_scalar_equal_condition(self):
        condition = ScalarCondition(
            key="stamina",
            operator="==",
            value=10.0,
        )

        context = ActionContext(
            scalar_values={
                "stamina": 10.0,
            },
        )

        self.assertTrue(
            ConditionEvaluator.evaluate(condition, context)
        )

    def test_missing_scalar_condition_is_false(self):
        condition = ScalarCondition(
            key="speed",
            operator=">",
            value=5.0,
        )

        context = ActionContext()

        self.assertFalse(
            ConditionEvaluator.evaluate(condition, context)
        )

    def test_invalid_operator_is_rejected(self):
        with self.assertRaises(ValueError):
            ScalarCondition(
                key="speed",
                operator="contains",
                value=5.0,
            )


if __name__ == "__main__":
    unittest.main()
