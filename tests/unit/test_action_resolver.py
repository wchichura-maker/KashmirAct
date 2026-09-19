import unittest

from src.game.characters.actions.definitions import (
    ActionDefinition,
    ActionPhase,
    ActionRequest,
)
from src.game.characters.actions.resolver import ActionResolver
from src.game.characters.primitives.composition import PrimitiveComposition
from src.game.characters.primitives.definitions import (
    PrimitiveDefinition,
    PrimitiveRequest,
)


class ActionResolverTests(unittest.TestCase):

    def setUp(self):
        self.primitives = {
            "step": PrimitiveDefinition(
                primitive_id="step",
                duration=0.5,
                distance=2.0,
            ),
            "turn": PrimitiveDefinition(
                primitive_id="turn",
                duration=0.2,
                rotation_degrees=90.0,
            ),
            "lunge": PrimitiveDefinition(
                primitive_id="lunge",
                duration=0.4,
                distance=3.0,
            ),
        }

        self.compositions = {
            "composition.step.turn.lunge": PrimitiveComposition(
                composition_id="composition.step.turn.lunge",
                requests=(
                    PrimitiveRequest(
                        primitive_id="step",
                        direction_x=1.0,
                        direction_y=0.0,
                    ),
                    PrimitiveRequest(
                        primitive_id="turn",
                    ),
                    PrimitiveRequest(
                        primitive_id="lunge",
                        direction_x=1.0,
                        direction_y=0.0,
                    ),
                ),
            ),
        }

        self.actions = {
            "action.step.turn.lunge": ActionDefinition(
                action_id="action.step.turn.lunge",
                phases=(
                    ActionPhase.WINDUP,
                    ActionPhase.EXECUTION,
                    ActionPhase.RECOVERY,
                ),
                composition_id="composition.step.turn.lunge",
            ),
        }

        self.resolver = ActionResolver(
            actions=self.actions,
            compositions=self.compositions,
            primitives=self.primitives,
        )

    def test_known_action_is_resolved(self):
        result = self.resolver.resolve(
            ActionRequest(
                action_id="action.step.turn.lunge",
            )
        )

        self.assertTrue(result.valid)
        self.assertEqual(
            result.action_id,
            "action.step.turn.lunge",
        )

    def test_resolver_reuses_primitive_playback(self):
        result = self.resolver.resolve(
            ActionRequest(
                action_id="action.step.turn.lunge",
            )
        )

        playback = result.playback_result

        self.assertIsNotNone(playback)
        self.assertEqual(
            playback.composition_id,
            "composition.step.turn.lunge",
        )
        self.assertEqual(len(playback.steps), 3)

    def test_total_duration_is_preserved(self):
        result = self.resolver.resolve(
            ActionRequest(
                action_id="action.step.turn.lunge",
            )
        )

        self.assertAlmostEqual(
            result.total_duration,
            1.1,
        )

    def test_final_rotation_is_preserved(self):
        result = self.resolver.resolve(
            ActionRequest(
                action_id="action.step.turn.lunge",
            )
        )

        self.assertAlmostEqual(
            result.final_rotation_degrees,
            90.0,
        )

    def test_unknown_action_is_rejected(self):
        result = self.resolver.resolve(
            ActionRequest(
                action_id="action.unknown",
            )
        )

        self.assertFalse(result.valid)
        self.assertIn("unknown action", result.errors)

    def test_unknown_composition_is_rejected(self):
        actions = {
            "action.invalid": ActionDefinition(
                action_id="action.invalid",
                phases=(ActionPhase.EXECUTION,),
                composition_id="composition.unknown",
            )
        }

        resolver = ActionResolver(
            actions=actions,
            compositions=self.compositions,
            primitives=self.primitives,
        )

        result = resolver.resolve(
            ActionRequest(
                action_id="action.invalid",
            )
        )

        self.assertFalse(result.valid)
        self.assertIn("unknown composition", result.errors)

    def test_same_request_is_deterministic(self):
        request = ActionRequest(
            action_id="action.step.turn.lunge",
        )

        first = self.resolver.resolve(request)
        second = self.resolver.resolve(request)

        self.assertEqual(first, second)

    def test_different_action_definitions_use_same_core(self):
        actions = {
            "action.a": ActionDefinition(
                action_id="action.a",
                phases=(ActionPhase.EXECUTION,),
                composition_id="composition.step.turn.lunge",
            ),
            "action.b": ActionDefinition(
                action_id="action.b",
                phases=(ActionPhase.EXECUTION,),
                composition_id="composition.step.turn.lunge",
            ),
        }

        resolver = ActionResolver(
            actions=actions,
            compositions=self.compositions,
            primitives=self.primitives,
        )

        first = resolver.resolve(ActionRequest(action_id="action.a"))
        second = resolver.resolve(ActionRequest(action_id="action.b"))

        self.assertTrue(first.valid)
        self.assertTrue(second.valid)
        self.assertEqual(
            first.playback_result,
            second.playback_result,
        )


if __name__ == "__main__":
    unittest.main()
