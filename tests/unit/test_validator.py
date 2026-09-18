from __future__ import annotations

import unittest

from tests.helpers import load_catalog

from core.contracts import reasons
from core.data.attributes import AttributeDefinition
from core.rules.validator import RuleValidator


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = load_catalog()
        self.validator = RuleValidator(self.catalog)

    def test_valid_entity_id(self) -> None:
        result = self.validator.validate_entity_id("player_001")
        self.assertTrue(result.valid)

    def test_invalid_entity_id_has_reason_code(self) -> None:
        result = self.validator.validate_entity_id("not an id")
        self.assertFalse(result.valid)
        self.assertTrue(result.reason_codes)
        record = result.to_error_record()
        self.assertEqual(record["system"], "CORE")
        self.assertEqual(record["operation"], "parse_id")

    def test_known_attribute(self) -> None:
        result = self.validator.require_known_attribute("attribute_stamina_001")
        self.assertTrue(result.valid)

    def test_unknown_attribute(self) -> None:
        result = self.validator.require_known_attribute("attribute_mana_001")
        self.assertFalse(result.valid)
        self.assertIn(reasons.UNKNOWN_ATTRIBUTE, result.reason_codes)

    def test_attribute_definition_bounds(self) -> None:
        bad = AttributeDefinition(
            id="attribute_health_001",
            display_name="Health",
            min_value=10,
            max_value=1,
            default_value=5,
        )
        result = self.validator.validate_attribute_definition(bad)
        self.assertFalse(result.valid)
        self.assertIn(reasons.INVALID_ATTRIBUTE_BOUNDS, result.reason_codes)

    def test_primitive_without_catalog_is_unknown_not_guessed(self) -> None:
        result = self.validator.validate_primitive_id("primitive_swing_001")
        self.assertFalse(result.valid)
        self.assertIn(reasons.UNKNOWN_PRIMITIVE, result.reason_codes)

    def test_attack_without_catalog_is_unknown_not_guessed(self) -> None:
        result = self.validator.validate_attack_id("attack_sword_basic_001")
        self.assertFalse(result.valid)
        self.assertIn(reasons.UNKNOWN_ATTACK, result.reason_codes)

    def test_weapon_without_catalog_is_unknown_not_guessed(self) -> None:
        result = self.validator.validate_weapon_id("weapon_sword_001")
        self.assertFalse(result.valid)
        self.assertIn(reasons.UNKNOWN_WEAPON, result.reason_codes)


if __name__ == "__main__":
    unittest.main()
