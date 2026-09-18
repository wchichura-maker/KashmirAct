from __future__ import annotations

import unittest

from tests.helpers import DATA, load_catalog

from core.contracts import reasons
from core.data.attributes import AttributeRuntime
from core.data.catalog import CoreCatalog


class AttributeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = load_catalog()
        self.health, _ = self.catalog.get_attribute("attribute_health_001")
        self.stamina, _ = self.catalog.get_attribute("attribute_stamina_001")
        assert self.health is not None
        assert self.stamina is not None

    def test_catalog_loads_p0_attributes(self) -> None:
        self.assertEqual(self.health.display_name, "Health")
        self.assertEqual(self.stamina.display_name, "Stamina")
        self.assertEqual(self.health.id, "attribute_health_001")
        self.assertNotEqual(self.health.id, "Health")

    def test_stamina_consumption(self) -> None:
        runtime = AttributeRuntime(self.stamina)
        result = runtime.consume(30)
        self.assertTrue(result.ok)
        self.assertEqual(runtime.get_value(), 70)

    def test_stamina_clamp(self) -> None:
        runtime = AttributeRuntime(self.stamina)
        high = runtime.set_value(999)
        self.assertTrue(high.ok)
        self.assertEqual(runtime.get_value(), 100)
        self.assertTrue(runtime.is_full())
        low = runtime.set_value(-40)
        self.assertTrue(low.ok)
        self.assertEqual(runtime.get_value(), 0)
        self.assertTrue(runtime.is_empty())

    def test_consume_does_not_go_negative(self) -> None:
        runtime = AttributeRuntime(self.stamina)
        runtime.set_value(20)
        failed = runtime.consume(50)
        self.assertFalse(failed.ok)
        self.assertEqual(failed.reason_code, reasons.INSUFFICIENT_ATTRIBUTE)
        self.assertEqual(runtime.get_value(), 20)

    def test_consume_rejects_negative_amount(self) -> None:
        runtime = AttributeRuntime(self.stamina)
        failed = runtime.consume(-1)
        self.assertFalse(failed.ok)
        self.assertEqual(failed.reason_code, reasons.NEGATIVE_AMOUNT)
        self.assertEqual(runtime.get_value(), 100)

    def test_regenerate_and_modify(self) -> None:
        runtime = AttributeRuntime(self.stamina, current_value=10, regeneration_rate=20)
        regen = runtime.regenerate(1.0)
        self.assertTrue(regen.ok)
        self.assertEqual(runtime.get_value(), 30)
        runtime.modify(100)
        self.assertEqual(runtime.get_value(), 100)
        runtime.regenerate(2.0)
        self.assertEqual(runtime.get_value(), 100)

    def test_display_name_is_not_the_id(self) -> None:
        renamed = type(self.health)(
            id=self.health.id,
            display_name="Vitality",
            min_value=self.health.min_value,
            max_value=self.health.max_value,
            default_value=self.health.default_value,
        )
        self.assertEqual(renamed.id, "attribute_health_001")
        self.assertEqual(renamed.display_name, "Vitality")

    def test_invalid_data_is_not_silently_loaded(self) -> None:
        empty = CoreCatalog()
        result = empty.load_attributes(DATA / "rules" / "attributes.json")
        self.assertFalse(result.valid)
        self.assertEqual(empty.attributes, {})

    def test_identical_operations_are_deterministic(self) -> None:
        a = AttributeRuntime(self.stamina)
        b = AttributeRuntime(self.stamina)
        for runtime in (a, b):
            runtime.consume(15)
            runtime.consume(5)
            runtime.modify(-2)
            runtime.regenerate(0)
        self.assertEqual(a.get_value(), b.get_value())


if __name__ == "__main__":
    unittest.main()
