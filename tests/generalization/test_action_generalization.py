import unittest

from src.game.characters.actions.definitions import (
    ActionDefinition,
    ActionPhase,
    ActionRequest,
    ActionRequestBinding,
)
from src.game.characters.actions.resolver import ActionResolver
from src.game.characters.primitives.composition import PrimitiveComposition
from src.game.characters.primitives.definitions import (
    PrimitiveDefinition,
    PrimitiveRequest,
)


class ActionGeneralizationTests(unittest.TestCase):

    def setUp(self):
        self.primitives = {
            "step": PrimitiveDefinition(
                primitive_id="step",
                duration=0.25,
                distance=1.0,
            ),
            "retreat": PrimitiveDefinition(
                primitive_id="retreat",
                duration=0.25,
                distance=1.0,
            ),
            "turn": PrimitiveDefinition(
                primitive_id="turn",
                duration=0.10,
                rotation_degrees=90.0,
            ),
            "turn_negative": PrimitiveDefinition(
                primitive_id="turn_negative",
                duration=0.10,
                rotation_degrees=-90.0,
            ),
            "lunge": PrimitiveDefinition(
                primitive_id="lunge",
                duration=0.50,
                distance=3.0,
            ),
        }

        self.compositions = {
            "step.turn.lunge": PrimitiveComposition(
                composition_id="step.turn.lunge",
                requests=(
                    PrimitiveRequest("step", direction_x=1.0),
                    PrimitiveRequest("turn"),
                    PrimitiveRequest("lunge", direction_x=1.0),
                ),
            ),
            "retreat.turn_negative.lunge": PrimitiveComposition(
                composition_id="retreat.turn_negative.lunge",
                requests=(
                    PrimitiveRequest("retreat", direction_x=-1.0),
                    PrimitiveRequest("turn_negative"),
                    PrimitiveRequest("lunge", direction_x=1.0),
                ),
            ),
            "step.turn.step.turn.lunge": PrimitiveComposition(
                composition_id="step.turn.step.turn.lunge",
                requests=(
                    PrimitiveRequest("step", direction_x=1.0),
                    PrimitiveRequest("turn"),
                    PrimitiveRequest("step", direction_x=1.0),
                    PrimitiveRequest("turn"),
                    PrimitiveRequest("lunge", direction_x=1.0),
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
                composition_id="step.turn.lunge",
                bindings=(
                    ActionRequestBinding(
                        primitive_index=0,
                        use_direction=True,
                        use_intensity=True,
                    ),
                    ActionRequestBinding(
                        primitive_index=2,
                        use_direction=True,
                        use_intensity=True,
                    ),
                ),
            ),
            "action.retreat.turn_negative.lunge": ActionDefinition(
                action_id="action.retreat.turn_negative.lunge",
                phases=(
                    ActionPhase.WINDUP,
                    ActionPhase.EXECUTION,
                    ActionPhase.RECOVERY,
                ),
                composition_id="retreat.turn_negative.lunge",
                bindings=(
                    ActionRequestBinding(
                        primitive_index=0,
                        use_direction=True,
                        use_intensity=True,
                    ),
                    ActionRequestBinding(
                        primitive_index=2,
                        use_direction=True,
                        use_intensity=True,
                    ),
                ),
            ),
            "action.step.turn.step.turn.lunge": ActionDefinition(
                action_id="action.step.turn.step.turn.lunge",
                phases=(
                    ActionPhase.WINDUP,
                    ActionPhase.EXECUTION,
                    ActionPhase.RECOVERY,
                ),
                composition_id="step.turn.step.turn.lunge",
                bindings=(
                    ActionRequestBinding(
                        primitive_index=0,
                        use_direction=True,
                        use_intensity=True,
                    ),
                    ActionRequestBinding(
                        primitive_index=2,
                        use_direction=True,
                        use_intensity=True,
                    ),
                    ActionRequestBinding(
                        primitive_index=4,
                        use_direction=True,
                        use_intensity=True,
                    ),
                ),
            ),
        }

        self.resolver = ActionResolver(
            actions=self.actions,
            compositions=self.compositions,
            primitives=self.primitives,
        )

    def test_three_structurally_different_actions_use_same_core(self):
        requests = (
            ActionRequest(
                action_id="action.step.turn.lunge",
                direction_x=1.0,
                direction_y=0.0,
                intensity=1.0,
            ),
            ActionRequest(
                action_id="action.retreat.turn_negative.lunge",
                direction_x=1.0,
                direction_y=0.0,
                intensity=1.0,
            ),
            ActionRequest(
                action_id="action.step.turn.step.turn.lunge",
                direction_x=1.0,
                direction_y=0.0,
                intensity=1.0,
            ),
        )

        results = tuple(
            self.resolver.resolve(request)
            for request in requests
        )

        self.assertTrue(all(result.valid for result in results))

        self.assertEqual(
            len(results[0].playback_result.steps),
            3,
        )

        self.assertEqual(
            len(results[1].playback_result.steps),
            3,
        )

        self.assertEqual(
            len(results[2].playback_result.steps),
            5,
        )

    def test_actions_produce_different_results_from_data(self):
        step_lunge = self.resolver.resolve(
            ActionRequest(
                action_id="action.step.turn.lunge",
            )
        )

        retreat_lunge = self.resolver.resolve(
            ActionRequest(
                action_id="action.retreat.turn_negative.lunge",
            )
        )

        chained = self.resolver.resolve(
            ActionRequest(
                action_id="action.step.turn.step.turn.lunge",
            )
        )

        self.assertNotEqual(
            step_lunge.playback_result,
            retreat_lunge.playback_result,
        )

        self.assertNotEqual(
            step_lunge.playback_result,
            chained.playback_result,
        )

        self.assertNotEqual(
            retreat_lunge.playback_result,
            chained.playback_result,
        )

    def test_generalization_is_deterministic(self):
        for action_id in self.actions:
            request = ActionRequest(
                action_id=action_id,
                direction_x=1.0,
                direction_y=0.0,
                intensity=1.25,
            )

            first = self.resolver.resolve(request)
            second = self.resolver.resolve(request)

            self.assertEqual(first, second)

    def test_core_does_not_depend_on_action_identity(self):
        action_ids = tuple(self.actions)

        results = tuple(
            self.resolver.resolve(
                ActionRequest(action_id=action_id)
            )
            for action_id in action_ids
        )

        self.assertTrue(
            all(result.valid for result in results)
        )


if __name__ == "__main__":
    unittest.main()
