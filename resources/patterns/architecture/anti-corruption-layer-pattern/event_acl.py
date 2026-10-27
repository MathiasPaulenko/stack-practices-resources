# acl/event_acl.py — translate legacy events to domain events
from typing import Callable, Dict, List
from dataclasses import dataclass

@dataclass
class LegacyEvent:
    event_type: str  # "CUST_ADD", "CUST_MOD", "CUST_DEL"
    cust_id: str
    email_addr: str
    stat_cd: str
    timestamp: str

@dataclass
class DomainEvent:
    event_type: str  # "CustomerCreated", "CustomerUpdated", "CustomerDeleted"
    customer_id: str
    email: str
    status: str
    occurred_at: str

class EventTranslator:
    """Translate legacy events to domain events."""

    TYPE_MAP = {
        "CUST_ADD": "CustomerCreated",
        "CUST_MOD": "CustomerUpdated",
        "CUST_DEL": "CustomerDeleted"
    }

    STATUS_MAP = {"1": "active", "2": "suspended", "3": "churned"}

    @staticmethod
    def to_domain(legacy: LegacyEvent) -> DomainEvent:
        return DomainEvent(
            event_type=EventTranslator.TYPE_MAP.get(legacy.event_type, "Unknown"),
            customer_id=legacy.cust_id,
            email=legacy.email_addr.lower() if legacy.email_addr else "",
            status=EventTranslator.STATUS_MAP.get(legacy.stat_cd, "active"),
            occurred_at=legacy.timestamp
        )

class EventACL:
    """Subscribe to legacy events, publish domain events."""

    def __init__(self):
        self._translator = EventTranslator()
        self._handlers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def on_legacy_event(self, legacy_event: LegacyEvent):
        """Called when a legacy event arrives."""
        domain_event = self._translator.to_domain(legacy_event)

        handlers = self._handlers.get(domain_event.event_type, [])
        for handler in handlers:
            handler(domain_event)
