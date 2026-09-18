import unittest

from src.game.characters.input_intent import InputIntent
from src.game.characters.locomotion import (
    LocomotionController,
    MotionState,
)
from src.game.characters.movement_profile import MovementProfile


class LocomotionTests(unittest.TestCase):

    def setUp(self):
        self.profile = MovementProfile(
            walk_speed=4.0,
            sprint_speed=8.0,
            acceleration=10.0,
            deceleration=20.0,
            rotation_speed=10.0,
        )

    def test_idle_preserves_zero_velocity(self):
        result = LocomotionController.resolve(
            InputIntent.idle(),
            self.profile,
            MotionState(),
            0.1,
        )

        self.assertEqual(result.motion.velocity_x, 0.0)
        self.assertEqual(result.motion.velocity_y, 0.0)

    def test_acceleration_is_limited_by_profile(self):
        result = LocomotionController.resolve(
            InputIntent.move(1.0, 0.0),
            self.profile,
            MotionState(),
            0.1,
        )

        self.assertAlmostEqual(result.motion.velocity_x, 1.0)
        self.assertAlmostEqual(result.motion.velocity_y, 0.0)

    def test_velocity_reaches_walk_target(self):
        result = LocomotionController.resolve(
            InputIntent.move(1.0, 0.0),
            self.profile,
            MotionState(),
            1.0,
        )

        self.assertAlmostEqual(result.motion.velocity_x, 4.0)

    def test_sprint_changes_target_speed(self):
        result = LocomotionController.resolve(
            InputIntent.move(1.0, 0.0, sprint=True),
            self.profile,
            MotionState(),
            1.0,
        )

        self.assertAlmostEqual(result.motion.velocity_x, 8.0)

    def test_deceleration_uses_deceleration_parameter(self):
        result = LocomotionController.resolve(
            InputIntent.idle(),
            self.profile,
            MotionState(velocity_x=10.0),
            0.1,
        )

        self.assertAlmostEqual(result.motion.velocity_x, 8.0)

    def test_direction_is_normalized(self):
        result = LocomotionController.resolve(
            InputIntent(move_x=1.0, move_y=1.0),
            self.profile,
            MotionState(),
            1.0,
        )

        self.assertAlmostEqual(
            result.desired_direction_x,
            2 ** -0.5,
            places=6,
        )

        self.assertAlmostEqual(
            result.desired_direction_y,
            2 ** -0.5,
            places=6,
        )

    def test_negative_delta_is_rejected(self):
        with self.assertRaises(ValueError):
            LocomotionController.resolve(
                InputIntent.idle(),
                self.profile,
                MotionState(),
                -0.1,
            )

    def test_same_input_and_state_are_deterministic(self):
        intent = InputIntent.move(0.5, -0.75)
        state = MotionState(velocity_x=1.2, velocity_y=-0.5)

        first = LocomotionController.resolve(
            intent,
            self.profile,
            state,
            0.016,
        )

        second = LocomotionController.resolve(
            intent,
            self.profile,
            state,
            0.016,
        )

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
