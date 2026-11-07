"""Order pipeline: gather fan-out + semaphore bound + per-step isolation.

Each order fans out to three simulated external calls. return_exceptions
isolates failures so one broken step can't cancel the other two in
flight; the semaphore keeps total concurrency under the downstream cap.

Run: python order_pipeline.py
"""

import asyncio
from dataclasses import dataclass


@dataclass
class Order:
    id: int
    items: int
    total: float


async def check_inventory(order: Order) -> str:
    await asyncio.sleep(0.05)
    if order.items <= 0:
        raise ValueError("empty order")
    return "reserved"


async def process_payment(order: Order) -> str:
    await asyncio.sleep(0.05)
    if order.total <= 0:
        raise ValueError("invalid amount")
    return "charged"


async def arrange_shipping(order: Order) -> str:
    await asyncio.sleep(0.05)
    return "label_created"


async def process_order(order: Order) -> dict:
    inventory, payment, shipping = await asyncio.gather(
        check_inventory(order),
        process_payment(order),
        arrange_shipping(order),
        return_exceptions=True,
    )
    errors = [
        name
        for name, result in zip(
            ("inventory", "payment", "shipping"), (inventory, payment, shipping)
        )
        if isinstance(result, Exception)
    ]
    return {"order_id": order.id, "ok": not errors, "errors": errors}


async def main() -> None:
    semaphore = asyncio.Semaphore(10)
    orders = [Order(id=i, items=1, total=49.99) for i in range(50)]
    orders[7] = Order(id=7, items=0, total=49.99)  # one bad order

    async def limited(order: Order) -> dict:
        async with semaphore:
            return await process_order(order)

    results = await asyncio.gather(*[limited(o) for o in orders])
    failed = [r for r in results if not r["ok"]]
    print(f"{len(results) - len(failed)}/{len(results)} orders processed")
    for r in failed:
        print(f"  order {r['order_id']} failed: {r['errors']}")


if __name__ == "__main__":
    asyncio.run(main())
