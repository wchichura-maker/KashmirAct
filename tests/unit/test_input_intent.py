import unittest

from src.game.characters.input_intent import InputIntent


class InputIntentTests(unittest.TestCase):

    def test_idle_intent_is_zero(self):
        intent = InputIntent.idle()

        self.assertEqual(intent.move_x, 0.0)
        self.assertEqual(intent.move_y, 0.0)
        self.assertEqual(intent.move_magnitude, 0.0)
        self.assertFalse(intent.has_movement)

    def test_axis_values_are_clamped(self):
        intent = InputIntent(
            move_x=5.0,
            move_y=-5.0,
            look_x=3.0,
            look_y=-3.0,
        )

        self.assertLessEqual(intent.move_x, 1.0)
        self.assertGreaterEqual(intent.move_y, -1.0)
        self.assertLessEqual(intent.look_x, 1.0)
        self.assertGreaterEqual(intent.look_y, -1.0)

    def test_diagonal_movement_is_normalized(self):
        intent = InputIntent(move_x=1.0, move_y=1.0)

        self.assertAlmostEqual(intent.move_magnitude, 1.0, places=6)

    def test_action_requests_are_part_of_intent(self):
        intent = InputIntent(
            request_sprint=True,
            request_dodge=True,
            request_block=True,
            request_primary_action=True,
        )

        self.assertTrue(intent.request_sprint)
        self.assertTrue(intent.request_dodge)
        self.assertTrue(intent.request_block)
        self.assertTrue(intent.request_primary_action)

    def test_intent_is_immutable(self):
        intent = InputIntent.move(1.0, 0.0)

        with self.assertRaises(AttributeError):
            intent.move_x = 0.0


if __name__ == "__main__":
    unittest.main()
