import unittest

from src.game.characters.actions.definitions import (
    ActionDefinition,
    ActionPhase,
)
from src.game.characters.actions.cancellation import ActionCancellationResolver


class ActionCancellationResolverTests(unittest.TestCase):

    def test_cancellable_action_can_cancel_inside_window(self):
        action = ActionDefinition(
            action_id="attack",
            phases=(
                ActionPhase.WINDUP,
                ActionPhase.EXECUTION,
                ActionPhase.RECOVERY,
            ),
            composition_id="attack.composition",
            cancellable=True,
            cancel_windows=(
                ActionPhase.EXECUTION,
            ),
        )

        resolver = ActionCancellationResolver()

        self.assertTrue(
            resolver.can_cancel(
                action,
                ActionPhase.EXECUTION,
            )
        )

    def test_cancellable_action_cannot_cancel_outside_window(self):
        action = ActionDefinition(
            action_id="attack",
            phases=(
                ActionPhase.WINDUP,
                ActionPhase.EXECUTION,
                ActionPhase.RECOVERY,
            ),
            composition_id="attack.composition",
            cancellable=True,
            cancel_windows=(
                ActionPhase.EXECUTION,
            ),
        )

        resolver = ActionCancellationResolver()

        self.assertFalse(
            resolver.can_cancel(
                action,
                ActionPhase.WINDUP,
            )
        )

        self.assertFalse(
            resolver.can_cancel(
                action,
                ActionPhase.RECOVERY,
            )
        )

    def test_non_cancellable_action_cannot_cancel(self):
        action = ActionDefinition(
            action_id="attack",
            phases=(ActionPhase.EXECUTION,),
            composition_id="attack.composition",
            cancellable=False,
            cancel_windows=(
                ActionPhase.EXECUTION,
            ),
        )

        resolver = ActionCancellationResolver()

        self.assertFalse(
            resolver.can_cancel(
                action,
                ActionPhase.EXECUTION,
            )
        )

    def test_cancellable_action_without_windows_cannot_cancel(self):
        action = ActionDefinition(
            action_id="attack",
            phases=(ActionPhase.EXECUTION,),
            composition_id="attack.composition",
            cancellable=True,
        )

        resolver = ActionCancellationResolver()

        self.assertFalse(
            resolver.can_cancel(
                action,
                ActionPhase.EXECUTION,
            )
        )

    def test_cancellation_resolution_is_deterministic(self):
        action = ActionDefinition(
            action_id="attack",
            phases=(ActionPhase.EXECUTION,),
            composition_id="attack.composition",
            cancellable=True,
            cancel_windows=(
                ActionPhase.EXECUTION,
            ),
        )

        resolver = ActionCancellationResolver()

        first = resolver.can_cancel(
            action,
            ActionPhase.EXECUTION,
        )

        second = resolver.can_cancel(
            action,
            ActionPhase.EXECUTION,
        )

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
