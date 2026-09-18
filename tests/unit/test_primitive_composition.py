import unittest

from src.game.characters.primitives.definitions import (
    PrimitiveDefinition,
    PrimitiveRequest,
)
from src.game.characters.primitives.composition import (
    PrimitiveComposition,
    PrimitiveCompositionResolver,
)

from src.game.characters.primitives.playback import (
    PrimitivePlayback,
)

class PrimitiveCompositionTests(unittest.TestCase):

    def setUp(self):
        self.step = PrimitiveDefinition(
            primitive_id="step",
            duration=0.25,
            distance=1.0,
        )
        self.lunge = PrimitiveDefinition(
            primitive_id="lunge",
            duration=0.5,
            distance=3.0,
        )
        self.turn = PrimitiveDefinition(
            primitive_id="turn",
            duration=0.1,
            rotation_degrees=90.0,
        )
        self.catalog = {
            "step": self.step,
            "lunge": self.lunge,
            "turn": self.turn,
        }

    def test_preserves_primitive_order(self):
        composition = PrimitiveComposition(
            composition_id="step-turn-lunge",
            requests=(
                PrimitiveRequest("step", direction_x=1.0),
                PrimitiveRequest("turn"),
                PrimitiveRequest("lunge", direction_y=1.0),
            ),
        )
        result = PrimitiveCompositionResolver.resolve(
            composition, self.catalog
        )
        self.assertEqual(
            [item.primitive_id for item in result.primitive_results],
            ["step", "turn", "lunge"],
        )

    def test_same_primitive_can_be_repeated(self):
        composition = PrimitiveComposition(
            composition_id="double-step",
            requests=(
                PrimitiveRequest("step", direction_x=1.0),
                PrimitiveRequest("step", direction_x=1.0),
            ),
        )
        result = PrimitiveCompositionResolver.resolve(
            composition, self.catalog
        )
        self.assertEqual(len(result.primitive_results), 2)
        self.assertEqual(result.primitive_results[0].primitive_id, "step")
        self.assertEqual(result.primitive_results[1].primitive_id, "step")

    def test_empty_composition_is_valid_and_complete(self):
        composition = PrimitiveComposition(
            composition_id="empty",
            requests=(),
        )
        result = PrimitiveCompositionResolver.resolve(
            composition, self.catalog
        )
        self.assertEqual(result.primitive_results, ())
        self.assertTrue(result.completed)

    def test_different_primitives_share_same_contract(self):
        composition = PrimitiveComposition(
            composition_id="step-lunge",
            requests=(
                PrimitiveRequest("step", direction_x=1.0),
                PrimitiveRequest("lunge", direction_y=1.0),
            ),
        )
        result = PrimitiveCompositionResolver.resolve(
            composition, self.catalog
        )
        self.assertEqual(len(result.primitive_results), 2)
        self.assertEqual(result.primitive_results[0].primitive_id, "step")
        self.assertEqual(result.primitive_results[1].primitive_id, "lunge")

    def test_composition_is_deterministic(self):
        composition = PrimitiveComposition(
            composition_id="deterministic",
            requests=(
                PrimitiveRequest("step", direction_x=1.0),
                PrimitiveRequest("turn"),
                PrimitiveRequest("lunge", direction_y=1.0),
            ),
        )
        first = PrimitiveCompositionResolver.resolve(
            composition, self.catalog
        )
        second = PrimitiveCompositionResolver.resolve(
            composition, self.catalog
        )
        self.assertEqual(first, second)

    def test_unknown_primitive_is_rejected(self):
        composition = PrimitiveComposition(
            composition_id="invalid",
            requests=(
                PrimitiveRequest("does_not_exist"),
            ),
        )
        with self.assertRaises(KeyError):
            PrimitiveCompositionResolver.resolve(
                composition, self.catalog
            )

    def test_composition_accumulates_rotation(self):
        composition = PrimitiveComposition(
            composition_id="step-turn",
            requests=(
                PrimitiveRequest("step", direction_y=1.0),
                PrimitiveRequest("turn"),
            ),
        )
        result = PrimitiveCompositionResolver.resolve(
            composition, self.catalog
        )
        self.assertEqual(result.final_rotation_degrees, 90.0)

    def test_later_primitive_receives_updated_orientation(self):
        composition = PrimitiveComposition(
            composition_id="step-turn-lunge",
            requests=(
                PrimitiveRequest("step", direction_y=1.0),
                PrimitiveRequest("turn"),
                PrimitiveRequest("lunge", direction_y=1.0),
            ),
        )
        result = PrimitiveCompositionResolver.resolve(
            composition, self.catalog
        )
        lunge = result.primitive_results[2]
        self.assertAlmostEqual(lunge.displacement_x, -3.0, places=6)
        self.assertAlmostEqual(lunge.displacement_y, 0.0, places=6)

    def test_individual_primitive_results_are_preserved(self):
        composition = PrimitiveComposition(
            composition_id="step-turn-lunge",
            requests=(
                PrimitiveRequest("step", direction_y=1.0),
                PrimitiveRequest("turn"),
                PrimitiveRequest("lunge", direction_y=1.0),
            ),
        )
        result = PrimitiveCompositionResolver.resolve(
            composition, self.catalog
        )
        self.assertEqual(len(result.primitive_results), 3)
        self.assertEqual(result.primitive_results[0].primitive_id, "step")
        self.assertEqual(result.primitive_results[1].primitive_id, "turn")
        self.assertEqual(result.primitive_results[2].primitive_id, "lunge")

    def test_multiple_turns_accumulate(self):
        composition = PrimitiveComposition(
            composition_id="two-turns",
            requests=(
                PrimitiveRequest("turn"),
                PrimitiveRequest("turn"),
            ),
        )
        result = PrimitiveCompositionResolver.resolve(
            composition, self.catalog
        )
        self.assertEqual(result.final_rotation_degrees, 180.0)

    def test_full_rotation_returns_to_original_direction(self):
        composition = PrimitiveComposition(
            composition_id="full-rotation",
            requests=(
                PrimitiveRequest("turn"),
                PrimitiveRequest("turn"),
                PrimitiveRequest("turn"),
                PrimitiveRequest("turn"),
                PrimitiveRequest("lunge", direction_y=1.0),
            ),
        )
        result = PrimitiveCompositionResolver.resolve(
            composition, self.catalog
        )
        lunge = result.primitive_results[-1]
        self.assertAlmostEqual(lunge.displacement_x, 0.0, places=6)
        self.assertAlmostEqual(lunge.displacement_y, 3.0, places=6)

    def test_negative_rotation_changes_direction_correctly(self):
        self.catalog["turn_left"] = PrimitiveDefinition(
            primitive_id="turn_left",
            duration=0.1,
            rotation_degrees=-90.0,
        )
        composition = PrimitiveComposition(
            composition_id="turn-left-lunge",
            requests=(
                PrimitiveRequest("turn_left"),
                PrimitiveRequest("lunge", direction_y=1.0),
            ),
        )
        result = PrimitiveCompositionResolver.resolve(
            composition, self.catalog
        )
        lunge = result.primitive_results[-1]
        self.assertAlmostEqual(lunge.displacement_x, 3.0, places=6)
        self.assertAlmostEqual(lunge.displacement_y, 0.0, places=6)

    def test_playback_preserves_primitive_order(self):
        composition = PrimitiveComposition(
            composition_id="playback-step-turn-lunge",
            requests=(
                PrimitiveRequest("step", direction_y=1.0),
                PrimitiveRequest("turn"),
                PrimitiveRequest("lunge", direction_y=1.0),
            ),
        )

        result = PrimitivePlayback.resolve(
            composition,
            self.catalog,
        )

        self.assertEqual(
            [step.result.primitive_id for step in result.steps],
            ["step", "turn", "lunge"],
        )

    def test_playback_accumulates_duration(self):
        composition = PrimitiveComposition(
            composition_id="playback-duration",
            requests=(
                PrimitiveRequest("step", direction_y=1.0),
                PrimitiveRequest("turn"),
                PrimitiveRequest("lunge", direction_y=1.0),
            ),
        )

        result = PrimitivePlayback.resolve(
            composition,
            self.catalog,
        )

        self.assertAlmostEqual(
            result.total_duration,
            0.25 + 0.1 + 0.5,
            places=6,
        )

    def test_playback_tracks_elapsed_time_per_step(self):
        composition = PrimitiveComposition(
            composition_id="playback-timeline",
            requests=(
                PrimitiveRequest("step", direction_y=1.0),
                PrimitiveRequest("turn"),
                PrimitiveRequest("lunge", direction_y=1.0),
            ),
        )

        result = PrimitivePlayback.resolve(
            composition,
            self.catalog,
        )

        self.assertAlmostEqual(
            result.steps[0].elapsed_before,
            0.0,
            places=6,
        )
        self.assertAlmostEqual(
            result.steps[0].elapsed_after,
            0.25,
            places=6,
        )

        self.assertAlmostEqual(
            result.steps[1].elapsed_before,
            0.25,
            places=6,
        )
        self.assertAlmostEqual(
            result.steps[1].elapsed_after,
            0.35,
            places=6,
        )

        self.assertAlmostEqual(
            result.steps[2].elapsed_before,
            0.35,
            places=6,
        )
        self.assertAlmostEqual(
            result.steps[2].elapsed_after,
            0.85,
            places=6,
        )

    def test_playback_preserves_composition_rotation(self):
        composition = PrimitiveComposition(
            composition_id="playback-rotation",
            requests=(
                PrimitiveRequest("step", direction_y=1.0),
                PrimitiveRequest("turn"),
                PrimitiveRequest("lunge", direction_y=1.0),
            ),
        )

        result = PrimitivePlayback.resolve(
            composition,
            self.catalog,
        )

        self.assertEqual(
            result.final_rotation_degrees,
            90.0,
        )

    def test_playback_supports_duration_override(self):
        composition = PrimitiveComposition(
            composition_id="playback-duration-override",
            requests=(
                PrimitiveRequest(
                    "step",
                    direction_y=1.0,
                    duration_override=0.5,
                ),
                PrimitiveRequest("turn"),
            ),
        )

        result = PrimitivePlayback.resolve(
            composition,
            self.catalog,
        )

        self.assertAlmostEqual(
            result.total_duration,
            0.6,
            places=6,
        )

    def test_empty_playback_is_complete(self):
        composition = PrimitiveComposition(
            composition_id="empty-playback",
            requests=(),
        )

        result = PrimitivePlayback.resolve(
            composition,
            self.catalog,
        )

        self.assertEqual(result.steps, ())
        self.assertTrue(result.completed)
        self.assertEqual(result.total_duration, 0.0)

    def test_playback_is_deterministic(self):
        composition = PrimitiveComposition(
            composition_id="deterministic-playback",
            requests=(
                PrimitiveRequest("step", direction_y=1.0),
                PrimitiveRequest("turn"),
                PrimitiveRequest("lunge", direction_y=1.0),
            ),
        )

        first = PrimitivePlayback.resolve(
            composition,
            self.catalog,
        )

        second = PrimitivePlayback.resolve(
            composition,
            self.catalog,
        )

        self.assertEqual(first, second)

if __name__ == "__main__":
    unittest.main()
