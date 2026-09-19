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


class ActionBindingTests(unittest.TestCase):

    def setUp(self):
        self.primitives = {
            "step": PrimitiveDefinition(
                primitive_id="step",
                duration=0.5,
                distance=2.0,
            ),
            "lunge": PrimitiveDefinition(
                primitive_id="lunge",
                duration=0.4,
                distance=3.0,
            ),
        }

        self.compositions = {
            "composition.test": PrimitiveComposition(
                composition_id="composition.test",
                requests=(
                    PrimitiveRequest(
                        primitive_id="step",
                        direction_x=1.0,
                        direction_y=0.0,
                        intensity=1.0,
                    ),
                    PrimitiveRequest(
                        primitive_id="lunge",
                        direction_x=1.0,
                        direction_y=0.0,
                        intensity=1.0,
                    ),
                ),
            ),
        }

    def make_action(self, bindings):
        return ActionDefinition(
            action_id="action.test",
            phases=(ActionPhase.EXECUTION,),
            composition_id="composition.test",
            bindings=bindings,
        )

    def make_resolver(self, action):
        return ActionResolver(
            actions={"action.test": action},
            compositions=self.compositions,
            primitives=self.primitives,
        )

    def test_binding_can_target_one_primitive(self):
        binding = ActionRequestBinding(
            primitive_index=0,
            use_direction=True,
            use_intensity=True,
        )

        action = self.make_action((binding,))
        resolver = self.make_resolver(action)

        result = resolver.resolve(
            ActionRequest(
                action_id="action.test",
                direction_x=0.0,
                direction_y=1.0,
                intensity=2.0,
            )
        )

        self.assertTrue(result.valid)

        first = result.playback_result.steps[0].result
        second = result.playback_result.steps[1].result

        self.assertAlmostEqual(first.displacement_x, 0.0)
        self.assertAlmostEqual(first.displacement_y, 4.0)

        self.assertAlmostEqual(second.displacement_x, 3.0)
        self.assertAlmostEqual(second.displacement_y, 0.0)

    def test_binding_can_target_multiple_primitives(self):
        bindings = (
            ActionRequestBinding(
                primitive_index=0,
                use_intensity=True,
            ),
            ActionRequestBinding(
                primitive_index=1,
                use_intensity=True,
            ),
        )

        action = self.make_action(bindings)
        resolver = self.make_resolver(action)

        result = resolver.resolve(
            ActionRequest(
                action_id="action.test",
                intensity=2.0,
            )
        )

        self.assertTrue(result.valid)

        self.assertAlmostEqual(
            result.playback_result.steps[0].result.displacement,
            4.0,
        )

        self.assertAlmostEqual(
            result.playback_result.steps[1].result.displacement,
            6.0,
        )

    def test_unbound_primitive_keeps_definition_request(self):
        action = self.make_action(
            (
                ActionRequestBinding(
                    primitive_index=0,
                    use_direction=True,
                ),
            )
        )

        resolver = self.make_resolver(action)

        result = resolver.resolve(
            ActionRequest(
                action_id="action.test",
                direction_x=0.0,
                direction_y=1.0,
                intensity=2.0,
            )
        )

        second = result.playback_result.steps[1].result

        self.assertAlmostEqual(second.displacement_x, 3.0)
        self.assertAlmostEqual(second.displacement_y, 0.0)

    def test_binding_does_not_depend_on_action_name(self):
        action_a = ActionDefinition(
            action_id="action.a",
            phases=(ActionPhase.EXECUTION,),
            composition_id="composition.test",
            bindings=(
                ActionRequestBinding(
                    primitive_index=0,
                    use_direction=True,
                ),
            ),
        )

        action_b = ActionDefinition(
            action_id="action.b",
            phases=(ActionPhase.EXECUTION,),
            composition_id="composition.test",
            bindings=(
                ActionRequestBinding(
                    primitive_index=0,
                    use_direction=True,
                ),
            ),
        )

        resolver = ActionResolver(
            actions={
                "action.a": action_a,
                "action.b": action_b,
            },
            compositions=self.compositions,
            primitives=self.primitives,
        )

        request = ActionRequest(
            action_id="action.a",
            direction_x=0.0,
            direction_y=1.0,
        )

        result_a = resolver.resolve(request)

        result_b = resolver.resolve(
            ActionRequest(
                action_id="action.b",
                direction_x=0.0,
                direction_y=1.0,
            )
        )

        self.assertEqual(
            result_a.playback_result,
            result_b.playback_result,
        )


if __name__ == "__main__":
    unittest.main()
