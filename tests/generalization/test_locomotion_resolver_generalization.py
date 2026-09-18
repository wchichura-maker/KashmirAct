import unittest

from src.game.characters.input_intent import InputIntent
from src.game.characters.locomotion import (
    LocomotionController,
    MotionState,
)
from src.game.characters.movement_profile import MovementProfile


class LocomotionResolverGeneralizationTests(unittest.TestCase):

    def test_same_resolver_accepts_different_character_profiles(self):
        humanoid = MovementProfile(
            walk_speed=4.0,
            sprint_speed=7.0,
            acceleration=12.0,
            deceleration=18.0,
            rotation_speed=10.0,
        )

        heavy_creature = MovementProfile(
            walk_speed=2.0,
            sprint_speed=3.0,
            acceleration=5.0,
            deceleration=8.0,
            rotation_speed=4.0,
        )

        intent = InputIntent.move(1.0, 0.0)

        humanoid_result = LocomotionController.resolve(
            intent,
            humanoid,
            MotionState(),
            0.1,
        )

        heavy_result = LocomotionController.resolve(
            intent,
            heavy_creature,
            MotionState(),
            0.1,
        )

        self.assertGreater(
            humanoid_result.motion.speed,
            heavy_result.motion.speed,
        )

    def test_same_resolver_accepts_player_and_ai_intents(self):
        player_intent = InputIntent.move(1.0, 0.0)
        ai_intent = InputIntent.move(-1.0, 0.0)

        profile = MovementProfile()

        player_result = LocomotionController.resolve(
            player_intent,
            profile,
            MotionState(),
            1.0,
        )

        ai_result = LocomotionController.resolve(
            ai_intent,
            profile,
            MotionState(),
            1.0,
        )

        self.assertGreater(player_result.motion.velocity_x, 0.0)
        self.assertLess(ai_result.motion.velocity_x, 0.0)

    def test_resolver_has_no_character_specific_symbols(self):
        from pathlib import Path

        root = Path(__file__).resolve().parents[2]
        source = (
            root / "src" / "game" / "characters" / "locomotion.py"
        ).read_text(encoding="utf-8").lower()

        forbidden = (
            "player_001",
            "enemy_001",
            "p0character",
            "if player",
            "if enemy",
            "elif player",
            "elif enemy",
        )

        for token in forbidden:
            self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
