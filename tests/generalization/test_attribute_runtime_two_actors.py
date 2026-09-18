"""Same Core attribute runtime for two actor types — no Core exceptions."""

from __future__ import annotations

import inspect
import unittest

from tests.helpers import load_catalog

from core.data import attributes as attributes_module
from core.data.attributes import AttributeRuntime
from core.events.bus import EventBus
from core.ids.entity_id import parse_entity_id


class GeneralizationTests(unittest.TestCase):
    def test_player_and_enemy_share_attribute_runtime(self) -> None:
        catalog = load_catalog()
        stamina, check = catalog.get_attribute("attribute_stamina_001")
        self.assertTrue(check.valid)
        assert stamina is not None

        player_id, player_check = parse_entity_id("player_001", catalog.entity_types.types)
        enemy_id, enemy_check = parse_entity_id("enemy_001", catalog.entity_types.types)
        self.assertTrue(player_check.valid)
        self.assertTrue(enemy_check.valid)
        assert player_id is not None
        assert enemy_id is not None

        player_stamina = AttributeRuntime(stamina)
        enemy_stamina = AttributeRuntime(stamina)
        self.assertTrue(player_stamina.consume(40).ok)
        self.assertTrue(enemy_stamina.consume(40).ok)
        self.assertEqual(player_stamina.get_value(), enemy_stamina.get_value())

        bus = EventBus(catalog.entity_types)
        bus.set_session("session_001")
        bus.publish("STAMINA_CHANGED", actor_id=player_id.value(), stamina_before=100, stamina_after=60)
        bus.publish("STAMINA_CHANGED", actor_id=enemy_id.value(), stamina_before=100, stamina_after=60)
        actors = {event.actor_id for event in bus.events()}
        self.assertEqual(actors, {"player_001", "enemy_001"})

    def test_new_entity_type_does_not_require_core_edit(self) -> None:
        catalog = load_catalog()
        extended = catalog.entity_types.extend(["trainee"])
        entity, check = extended.parse("trainee_007")
        self.assertTrue(check.valid, check.message)
        assert entity is not None
        self.assertEqual(entity.entity_type, "trainee")
        stamina, _ = catalog.get_attribute("attribute_stamina_001")
        assert stamina is not None
        runtime = AttributeRuntime(stamina)
        self.assertTrue(runtime.consume(1).ok)

    def test_core_has_no_actor_content_branches(self) -> None:
        source = inspect.getsource(attributes_module)
        self.assertNotIn("player_001", source)
        self.assertNotIn("if character", source)
        self.assertNotIn("if actor", source)


if __name__ == "__main__":
    unittest.main()
