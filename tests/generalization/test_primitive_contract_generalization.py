import unittest
from pathlib import Path

from src.game.characters.primitives import (
    PrimitiveDefinition,
    PrimitiveRequest,
    PrimitiveResolver,
)


class PrimitiveGeneralizationTests(unittest.TestCase):

    def test_step_and_lunge_use_identical_runtime_contract(self):
        step = PrimitiveDefinition(
            primitive_id="primitive_step",
            duration=0.20,
            distance=1.0,
        )

        lunge = PrimitiveDefinition(
            primitive_id="primitive_lunge",
            duration=0.45,
            distance=3.0,
        )

        step_result = PrimitiveResolver.resolve(
            step,
            PrimitiveRequest(
                primitive_id="primitive_step",
                direction_x=1.0,
            ),
        )

        lunge_result = PrimitiveResolver.resolve(
            lunge,
            PrimitiveRequest(
                primitive_id="primitive_lunge",
                direction_x=1.0,
            ),
        )

        self.assertEqual(type(step_result), type(lunge_result))
        self.assertGreater(
            lunge_result.displacement,
            step_result.displacement,
        )

    def test_same_primitive_can_be_consumed_by_different_actions(self):
        step = PrimitiveDefinition(
            primitive_id="primitive_step",
            duration=0.20,
            distance=1.0,
        )

        dodge = PrimitiveResolver.resolve(
            step,
            PrimitiveRequest(
                primitive_id="primitive_step",
                direction_x=1.0,
                intensity=2.0,
                context={"action_type": "dodge"},
            ),
        )

        attack_setup = PrimitiveResolver.resolve(
            step,
            PrimitiveRequest(
                primitive_id="primitive_step",
                direction_y=1.0,
                intensity=0.75,
                context={"action_type": "attack_setup"},
            ),
        )

        self.assertNotEqual(
            (dodge.displacement_x, dodge.displacement_y),
            (attack_setup.displacement_x, attack_setup.displacement_y),
        )

    def test_runtime_has_no_content_specific_branches(self):
        path = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "game"
            / "characters"
            / "primitives"
            / "runtime.py"
        )

        source = path.read_text(encoding="utf-8").lower()

        forbidden_tokens = (
            "if primitive_id ==",
            "elif primitive_id ==",
            "primitive_step",
            "primitive_lunge",
            "if step",
            "if lunge",
            "if weapon",
            "if attack",
            "if player",
        )

        for token in forbidden_tokens:
            self.assertNotIn(token, source)

    def test_runtime_is_deterministic(self):
        primitive = PrimitiveDefinition(
            primitive_id="primitive_generic",
            duration=0.30,
            distance=2.0,
            rotation_degrees=30.0,
        )

        request = PrimitiveRequest(
            primitive_id="primitive_generic",
            direction_x=0.5,
            direction_y=0.75,
            intensity=1.25,
        )

        first = PrimitiveResolver.resolve(primitive, request)
        second = PrimitiveResolver.resolve(primitive, request)

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
