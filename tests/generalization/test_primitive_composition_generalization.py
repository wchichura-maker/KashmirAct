import unittest

from src.game.characters.primitives.definitions import (
    PrimitiveDefinition,
    PrimitiveRequest,
)
from src.game.characters.primitives.composition import (
    PrimitiveComposition,
    PrimitiveCompositionResolver,
)


class PrimitiveCompositionGeneralizationTests(unittest.TestCase):

    def setUp(self):
        self.catalog = {
            "step": PrimitiveDefinition(
                primitive_id="step",
                duration=0.25,
                distance=1.0,
            ),
            "lunge": PrimitiveDefinition(
                primitive_id="lunge",
                duration=0.5,
                distance=3.0,
            ),
            "turn": PrimitiveDefinition(
                primitive_id="turn",
                duration=0.1,
                rotation_degrees=90.0,
            ),
        }

        self.composition = PrimitiveComposition(
            composition_id="step-turn-lunge",
            requests=(
                PrimitiveRequest("step", direction_x=1.0),
                PrimitiveRequest("turn"),
                PrimitiveRequest("lunge", direction_y=1.0),
            ),
        )

    def test_same_composition_contract_supports_different_consumers(self):
        player_result = PrimitiveCompositionResolver.resolve(
            self.composition,
            self.catalog,
        )

        npc_result = PrimitiveCompositionResolver.resolve(
            self.composition,
            self.catalog,
        )

        self.assertEqual(player_result, npc_result)

    def test_composition_does_not_depend_on_character_identity(self):
        player_composition = self.composition
        npc_composition = PrimitiveComposition(
            composition_id="step-turn-lunge",
            requests=player_composition.requests,
        )

        self.assertEqual(
            PrimitiveCompositionResolver.resolve(
                player_composition,
                self.catalog,
            ),
            PrimitiveCompositionResolver.resolve(
                npc_composition,
                self.catalog,
            ),
        )

    def test_same_primitive_sequence_can_represent_different_actions(self):
        movement_action = PrimitiveComposition(
            composition_id="movement-action",
            requests=self.composition.requests,
        )

        future_attack_action = PrimitiveComposition(
            composition_id="future-attack-action",
            requests=self.composition.requests,
        )

        movement_result = PrimitiveCompositionResolver.resolve(
            movement_action,
            self.catalog,
        )

        attack_result = PrimitiveCompositionResolver.resolve(
            future_attack_action,
            self.catalog,
        )

        self.assertEqual(
            movement_result.primitive_results,
            attack_result.primitive_results,
        )

    def test_composition_is_deterministic(self):
        first = PrimitiveCompositionResolver.resolve(
            self.composition,
            self.catalog,
        )

        second = PrimitiveCompositionResolver.resolve(
            self.composition,
            self.catalog,
        )

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
