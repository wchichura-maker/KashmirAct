from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

DATA = ROOT / "data"


def load_catalog():
    from core.data.catalog import CoreCatalog

    catalog = CoreCatalog()
    types_result = catalog.load_entity_types(DATA / "rules" / "entity_types.json")
    if not types_result.valid:
        raise AssertionError(types_result.message)
    attr_result = catalog.load_attributes(DATA / "rules" / "attributes.json")
    if not attr_result.valid:
        raise AssertionError(attr_result.message)
    return catalog
