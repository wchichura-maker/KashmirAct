from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tests.helpers import DATA, load_catalog

from core.contracts import reasons
from core.data.catalog import CoreCatalog


class CatalogTests(unittest.TestCase):
    def test_loads_official_data(self) -> None:
        catalog = load_catalog()
        self.assertIsNotNone(catalog.entity_types)
        self.assertIn("player", catalog.entity_types.types)
        self.assertIn("attribute_health_001", catalog.attributes)
        self.assertIn("attribute_stamina_001", catalog.attributes)

    def test_rejects_invalid_json(self) -> None:
        catalog = CoreCatalog()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.json"
            path.write_text("{not json", encoding="utf-8")
            result = catalog.load_entity_types(path)
        self.assertFalse(result.valid)
        self.assertIn(reasons.INVALID_DATA_FILE, result.reason_codes)

    def test_rejects_attribute_id_from_display_name(self) -> None:
        catalog = CoreCatalog()
        self.assertTrue(catalog.load_entity_types(DATA / "rules" / "entity_types.json").valid)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "attributes.json"
            path.write_text(
                json.dumps(
                    {
                        "schema_version": "0.1",
                        "attributes": [
                            {
                                "id": "attribute_health",
                                "display_name": "Health",
                                "min_value": 0,
                                "max_value": 100,
                                "default_value": 100,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = catalog.load_attributes(path)
        self.assertFalse(result.valid)
        self.assertIn(reasons.ID_DERIVED_FROM_DISPLAY_NAME, result.reason_codes)
        self.assertEqual(catalog.attributes, {})

    def test_missing_file_is_explicit(self) -> None:
        catalog = CoreCatalog()
        result = catalog.load_entity_types(Path("/tmp/does-not-exist-kashmiract.json"))
        self.assertFalse(result.valid)
        self.assertIn(reasons.INVALID_DATA_FILE, result.reason_codes)


if __name__ == "__main__":
    unittest.main()
