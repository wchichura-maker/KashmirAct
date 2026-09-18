import unittest

from src.game.characters.input_intent import InputIntent
from src.game.characters.movement_profile import MovementProfile


class LocomotionGeneralizationTests(unittest.TestCase):

    def test_same_intent_contract_accepts_two_sources(self):
        player_input = InputIntent.move(1.0, 0.0)
        ai_input = InputIntent.move(0.0, 1.0)

        self.assertTrue(player_input.has_movement)
        self.assertTrue(ai_input.has_movement)

        self.assertNotEqual(
            (player_input.move_x, player_input.move_y),
            (ai_input.move_x, ai_input.move_y),
        )

    def test_same_movement_profile_supports_two_characters(self):
        character_a = MovementProfile(
            walk_speed=3.0,
            sprint_speed=5.5,
        )

        character_b = MovementProfile(
            walk_speed=1.5,
            sprint_speed=8.0,
        )

        self.assertEqual(character_a.walk_speed, 3.0)
        self.assertEqual(character_b.walk_speed, 1.5)
        self.assertEqual(character_b.sprint_speed, 8.0)

    def test_new_character_does_not_require_new_profile_type(self):
        humanoid = MovementProfile(
            walk_speed=3.0,
            sprint_speed=5.5,
        )

        heavy_creature = MovementProfile(
            walk_speed=2.0,
            sprint_speed=3.5,
            acceleration=10.0,
            deceleration=14.0,
            rotation_speed=5.0,
        )

        self.assertIsInstance(humanoid, MovementProfile)
        self.assertIsInstance(heavy_creature, MovementProfile)

    def test_no_character_specific_branch_exists_in_contracts(self):
        from pathlib import Path

        root = Path(__file__).resolve().parents[2]
        files = [
            root / "src" / "game" / "characters" / "input_intent.py",
            root / "src" / "game" / "characters" / "movement_profile.py",
        ]

        forbidden_tokens = (
            "player_001",
            "enemy_001",
            "P0Character",
            "if character",
            "elif character",
        )

        for path in files:
            source = path.read_text(encoding="utf-8").lower()

            for token in forbidden_tokens:
                self.assertNotIn(
                    token.lower(),
                    source,
                    f"Character-specific logic detected in {path}: {token}",
                )


if __name__ == "__main__":
    unittest.main()
