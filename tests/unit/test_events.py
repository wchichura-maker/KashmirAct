from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError

from tests.helpers import load_catalog

from core.contracts import reasons
from core.events.bus import EventBus
from core.events.types import KNOWN_EVENT_TYPES, REQUIRED_BUS_EVENTS, STAMINA_CHANGED


class EventBusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = load_catalog()
        self.bus = EventBus(self.catalog.entity_types)
        self.bus.set_session("session_001")

    def test_required_bus_events_are_registered(self) -> None:
        self.assertTrue(REQUIRED_BUS_EVENTS.issubset(KNOWN_EVENT_TYPES))
        self.assertEqual(len(REQUIRED_BUS_EVENTS), 19)

    def test_publish_is_immutable(self) -> None:
        event, check = self.bus.publish(
            STAMINA_CHANGED,
            actor_id="player_001",
            stamina_before=100,
            stamina_after=70,
        )
        self.assertTrue(check.valid, check.message)
        assert event is not None
        with self.assertRaises(FrozenInstanceError):
            event.event_type = "ATTACK_HIT"  # type: ignore[misc]
        with self.assertRaises(TypeError):
            event.payload["x"] = 1  # type: ignore[index]

    def test_unknown_event_type_is_not_stored(self) -> None:
        event, check = self.bus.publish("FLAP_WINGS", actor_id="player_001")
        self.assertIsNone(event)
        self.assertIn(reasons.UNKNOWN_EVENT_TYPE, check.reason_codes)
        self.assertEqual(self.bus.events(), ())

    def test_order_is_preserved(self) -> None:
        self.bus.publish("DODGE_STARTED", actor_id="player_001")
        self.bus.publish("PRIMITIVE_STARTED", actor_id="player_001", primitive_id="primitive_turn_001")
        self.bus.publish("ATTACK_STARTED", actor_id="player_001", attack_id="attack_sword_basic_001")
        self.assertEqual(
            list(self.bus.event_types()),
            ["DODGE_STARTED", "PRIMITIVE_STARTED", "ATTACK_STARTED"],
        )
        self.assertEqual(self.bus.events()[0].sequence, 1)
        self.assertEqual(self.bus.events()[2].event_id, "event_000003")
        self.assertEqual(self.bus.events()[0].session_id, "session_001")

    def test_subscribers_receive_the_same_frozen_event(self) -> None:
        seen: list[str] = []

        def handler(event) -> None:
            seen.append(event.event_id)
            with self.assertRaises(FrozenInstanceError):
                event.result = "mutated"  # type: ignore[misc]

        self.bus.subscribe(handler)
        event, check = self.bus.publish("INPUT_ACTION", actor_id="player_001", action_id="DODGE")
        self.assertTrue(check.valid)
        assert event is not None
        self.assertEqual(seen, [event.event_id])

    def test_null_fields_allowed(self) -> None:
        event, check = self.bus.publish("MOVEMENT_STARTED", actor_id="player_001")
        self.assertTrue(check.valid, check.message)
        assert event is not None
        self.assertIsNone(event.target_id)
        self.assertIsNone(event.weapon_id)
        self.assertIsNone(event.position)


if __name__ == "__main__":
    unittest.main()
