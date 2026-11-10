"""Tests for event_bus.EventBus."""
from event_bus import Event, EventBus


def test_publish_reaches_all_subscribers():
    bus = EventBus()
    hits = []
    bus.subscribe("OrderPlaced", lambda e: hits.append("a"))
    bus.subscribe("OrderPlaced", lambda e: hits.append("b"))
    bus.publish(Event("OrderPlaced", {"id": 1}))
    assert hits == ["a", "b"]


def test_unsubscribe_stops_delivery():
    bus = EventBus()
    hits = []
    unsub = bus.subscribe("Ping", lambda e: hits.append(e.payload["n"]))
    bus.publish(Event("Ping", {"n": 1}))
    unsub()
    bus.publish(Event("Ping", {"n": 2}))
    assert hits == [1]


def test_only_matching_event_types_dispatch():
    bus = EventBus()
    hits = []
    bus.subscribe("A", lambda e: hits.append("a"))
    bus.publish(Event("B", {}))
    assert hits == []


def test_failing_handler_does_not_block_others():
    bus = EventBus()
    hits = []

    def boom(e):
        raise RuntimeError("broken subscriber")

    bus.subscribe("E", boom)
    bus.subscribe("E", lambda e: hits.append("survivor"))
    bus.publish(Event("E", {}))
    assert hits == ["survivor"]


def test_handler_can_unsubscribe_during_dispatch():
    bus = EventBus()
    hits = []
    holder = {}

    def self_removing(e):
        hits.append("once")
        holder["unsub"]()

    holder["unsub"] = bus.subscribe("E", self_removing)
    bus.subscribe("E", lambda e: hits.append("every"))
    bus.publish(Event("E", {}))
    bus.publish(Event("E", {}))
    assert hits == ["once", "every", "every"]
