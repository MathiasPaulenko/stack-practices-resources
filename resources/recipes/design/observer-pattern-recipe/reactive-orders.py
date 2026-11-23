"""Reactive order events with RxPY: subject + filtered subscriptions."""
from rx import operators
from rx.subject import Subject

order_subject = Subject()

order_subject.subscribe(
    on_next=lambda event: print(f"Email service: Order {event['id']} created"),
    on_error=lambda e: print(f"Error: {e}"),
)

order_subject.subscribe(
    on_next=lambda event: print(f"Analytics: Tracking order {event['id']}"),
)

order_subject.pipe(
    operators.filter(lambda e: e["total"] > 100),
    operators.map(lambda e: {**e, "vip": True}),
).subscribe(on_next=lambda event: print(f"VIP handler: {event}"))

order_subject.on_next({"id": "123", "total": 50})
order_subject.on_next({"id": "124", "total": 250})
