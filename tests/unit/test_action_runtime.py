import unittest

from src.game.characters.actions import (
    ActionDefinition,
    ActionPhase,
    ActionRequest,
    ActionResolver,
)
from src.game.characters.actions.runtime import ActionRuntime
from src.game.characters.primitives import (
    PrimitiveComposition,
    PrimitiveDefinition,
    PrimitiveRequest,
)


class ActionRuntimeTests(unittest.TestCase):

    def setUp(self):
        self.step = PrimitiveDefinition(
            primitive_id="primitive_step",
            duration=0.20,
            distance=1.0,
        )

        self.turn = PrimitiveDefinition(
            primitive_id="primitive_turn",
            duration=0.10,
            distance=0.0,
            rotation_degrees=90.0,
        )

        self.composition = PrimitiveComposition(
            composition_id="composition_step_turn",
            requests=(
                PrimitiveRequest(
                    primitive_id="primitive_step",
                    direction_x=1.0,
                ),
                PrimitiveRequest(
                    primitive_id="primitive_turn",
                ),
            ),
        )

        self.action = ActionDefinition(
            action_id="action_step_turn",
            phases=(
                ActionPhase.WINDUP,
                ActionPhase.EXECUTION,
                ActionPhase.RECOVERY,
            ),
            composition_id="composition_step_turn",
        )

        self.resolver = ActionResolver(
            actions={
                self.action.action_id: self.action,
            },
            compositions={
                self.composition.composition_id: self.composition,
            },
            primitives={
                self.step.primitive_id: self.step,
                self.turn.primitive_id: self.turn,
            },
        )

        self.result = self.resolver.resolve(
            ActionRequest(
                action_id=self.action.action_id,
                direction_x=1.0,
            )
        )

    def test_start_activates_action(self):
        runtime = ActionRuntime()

        state = runtime.start(self.result)

        self.assertTrue(state.active)
        self.assertFalse(state.completed)
        self.assertFalse(state.interrupted)
        self.assertEqual(state.current_primitive_index, 0)
        self.assertAlmostEqual(state.elapsed_time, 0.0)

    def test_advance_stays_on_first_primitive(self):
        runtime = ActionRuntime()
        runtime.start(self.result)

        state = runtime.advance(0.10)

        self.assertTrue(state.active)
        self.assertEqual(state.current_primitive_index, 0)
        self.assertAlmostEqual(state.elapsed_time, 0.10)

    def test_advance_moves_to_next_primitive(self):
        runtime = ActionRuntime()
        runtime.start(self.result)

        state = runtime.advance(0.25)

        self.assertTrue(state.active)
        self.assertEqual(state.current_primitive_index, 1)
        self.assertAlmostEqual(state.elapsed_time, 0.25)

    def test_advance_completes_action(self):
        runtime = ActionRuntime()
        runtime.start(self.result)

        state = runtime.advance(0.30)

        self.assertFalse(state.active)
        self.assertTrue(state.completed)
        self.assertFalse(state.interrupted)
        self.assertEqual(state.current_primitive_index, 2)
        self.assertAlmostEqual(state.elapsed_time, 0.30)

    def test_interrupt_stops_action(self):
        runtime = ActionRuntime()
        runtime.start(self.result)
        runtime.advance(0.10)

        state = runtime.interrupt()

        self.assertFalse(state.active)
        self.assertFalse(state.completed)
        self.assertTrue(state.interrupted)
        self.assertEqual(state.current_primitive_index, 0)
        self.assertAlmostEqual(state.elapsed_time, 0.10)

    def test_advance_after_interrupt_does_not_progress(self):
        runtime = ActionRuntime()
        runtime.start(self.result)
        runtime.advance(0.10)
        runtime.interrupt()

        state = runtime.advance(1.0)

        self.assertTrue(state.interrupted)
        self.assertFalse(state.completed)
        self.assertAlmostEqual(state.elapsed_time, 0.10)

    def test_negative_delta_is_rejected(self):
        runtime = ActionRuntime()
        runtime.start(self.result)

        with self.assertRaises(ValueError):
            runtime.advance(-0.01)

    def test_invalid_action_cannot_start(self):
        runtime = ActionRuntime()

        invalid = self.resolver.resolve(
            ActionRequest(action_id="unknown_action")
        )

        with self.assertRaises(ValueError):
            runtime.start(invalid)


    def test_advance_completes_with_floating_point_tolerance(self):
        runtime = ActionRuntime()
        runtime.start(self.result)

        state = runtime.advance(0.1)
        state = runtime.advance(0.2)

        self.assertFalse(state.active)
        self.assertTrue(state.completed)
        self.assertFalse(state.interrupted)
        self.assertEqual(state.current_primitive_index, 2)
        self.assertAlmostEqual(state.elapsed_time, 0.30)


if __name__ == "__main__":
    unittest.main()
