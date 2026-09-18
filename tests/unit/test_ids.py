from __future__ import annotations

import unittest

from tests.helpers import load_catalog

from core.contracts import reasons
from core.ids.entity_id import make_entity_id, parse_entity_id


class EntityIdTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = load_catalog()
        self.types = self.catalog.entity_types.types

    def test_spec_examples_parse(self) -> None:
        examples = {
            "player_001": ("player", "001"),
            "enemy_001": ("enemy", "001"),
            "weapon_sword_001": ("weapon", "sword_001"),
            "attack_sword_basic_001": ("attack", "sword_basic_001"),
            "primitive_swing_001": ("primitive", "swing_001"),
        }
        for raw, (entity_type, unique) in examples.items():
            entity, check = parse_entity_id(raw, self.types)
            self.assertTrue(check.valid, check.message)
            assert entity is not None
            self.assertEqual(entity.entity_type, entity_type)
            self.assertEqual(entity.unique, unique)
            self.assertEqual(entity.value(), raw)

    def test_ids_are_stable_when_display_name_changes(self) -> None:
        entity, check = make_entity_id("weapon", "sword_001", self.types, display_name="Iron Sword")
        self.assertTrue(check.valid, check.message)
        assert entity is not None
        renamed, renamed_check = make_entity_id("weapon", "sword_001", self.types, display_name="Broken Stick")
        self.assertTrue(renamed_check.valid, renamed_check.message)
        assert renamed is not None
        self.assertEqual(entity.value(), renamed.value())
        self.assertEqual(entity.value(), "weapon_sword_001")

    def test_id_cannot_be_derived_from_display_name(self) -> None:
        entity, check = make_entity_id("weapon", "iron_sword", self.types, display_name="Iron Sword")
        self.assertIsNone(entity)
        self.assertFalse(check.valid)
        self.assertIn(reasons.ID_DERIVED_FROM_DISPLAY_NAME, check.reason_codes)

    def test_unknown_type_is_explicit(self) -> None:
        entity, check = parse_entity_id("dragon_001", self.types)
        self.assertIsNone(entity)
        self.assertEqual(check.status, reasons.INVALID)
        self.assertIn(reasons.UNKNOWN_ENTITY_TYPE, check.reason_codes)

    def test_uppercase_and_spaces_are_rejected(self) -> None:
        for raw in ("Player_001", "player 001", "", "player_", "_001"):
            entity, check = parse_entity_id(raw, self.types)
            self.assertIsNone(entity, raw)
            self.assertFalse(check.valid, raw)

    def test_make_rejects_unknown_type(self) -> None:
        entity, check = make_entity_id("dragon", "001", self.types)
        self.assertIsNone(entity)
        self.assertIn(reasons.UNKNOWN_ENTITY_TYPE, check.reason_codes)


if __name__ == "__main__":
    unittest.main()
