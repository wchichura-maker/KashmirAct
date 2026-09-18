import unittest

from src.game.characters.primitives import (
    PrimitiveDefinition,
    PrimitiveRequest,
    PrimitiveResolver,
)


class PrimitiveRuntimeTests(unittest.TestCase):

    def setUp(self):
        self.step = PrimitiveDefinition(
            primitive_id="primitive_step",
            duration=0.20,
            distance=1.0,
            rotation_degrees=0.0,
            acceleration=10.0,
            constraints=("grounded",),
            tags=("movement", "step"),
            cancellable=True,
        )

    def test_step_resolves_displacement(self):
        result = PrimitiveResolver.resolve(
            self.step,
            PrimitiveRequest(
                primitive_id="primitive_step",
                direction_x=1.0,
                direction_y=0.0,
            ),
        )

        self.assertAlmostEqual(result.displacement_x, 1.0)
        self.assertAlmostEqual(result.displacement_y, 0.0)

    def test_result_contains_velocity(self):
        result = PrimitiveResolver.resolve(
            self.step,
            PrimitiveRequest(
                primitive_id="primitive_step",
                direction_x=1.0,
                direction_y=0.0,
            ),
        )

        self.assertAlmostEqual(result.velocity_x, 5.0)
        self.assertAlmostEqual(result.velocity_y, 0.0)

    def test_result_contains_rotation(self):
        turning_step = PrimitiveDefinition(
            primitive_id="primitive_turn_step",
            duration=0.20,
            distance=1.0,
            rotation_degrees=45.0,
        )

        result = PrimitiveResolver.resolve(
            turning_step,
            PrimitiveRequest(
                primitive_id="primitive_turn_step",
            ),
        )

        self.assertAlmostEqual(result.rotation_degrees, 45.0)

    def test_duration_override_changes_velocity(self):
        result = PrimitiveResolver.resolve(
            self.step,
            PrimitiveRequest(
                primitive_id="primitive_step",
                direction_x=1.0,
                duration_override=0.50,
            ),
        )

        self.assertAlmostEqual(result.velocity_x, 2.0)
        self.assertAlmostEqual(result.displacement_x, 1.0)

    def test_intensity_changes_displacement(self):
        result = PrimitiveResolver.resolve(
            self.step,
            PrimitiveRequest(
                primitive_id="primitive_step",
                direction_x=1.0,
                intensity=2.0,
            ),
        )

        self.assertAlmostEqual(result.displacement_x, 2.0)

    def test_direction_is_normalized_during_resolution(self):
        result = PrimitiveResolver.resolve(
            self.step,
            PrimitiveRequest(
                primitive_id="primitive_step",
                direction_x=10.0,
                direction_y=0.0,
            ),
        )

        self.assertAlmostEqual(result.displacement_x, 1.0)
        self.assertAlmostEqual(result.displacement_y, 0.0)

    def test_result_reports_active_phase_and_completion(self):
        result = PrimitiveResolver.resolve(
            self.step,
            PrimitiveRequest(
                primitive_id="primitive_step",
            ),
        )

        self.assertEqual(result.phase, "active")
        self.assertTrue(result.completed)

    def test_definition_metadata_is_preserved(self):
        self.assertEqual(
            self.step.constraints,
            ("grounded",),
        )

        self.assertEqual(
            self.step.tags,
            ("movement", "step"),
        )

        self.assertTrue(self.step.cancellable)

    def test_mismatched_ids_are_rejected(self):
        with self.assertRaises(ValueError):
            PrimitiveResolver.resolve(
                self.step,
                PrimitiveRequest(
                    primitive_id="primitive_lunge",
                ),
            )


if __name__ == "__main__":
    unittest.main()
