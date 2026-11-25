"""Pattern 6: the same problem in Python — asyncio.Lock serializes
concurrent transfers so the check-and-act can't interleave.

Run: python asyncio_transfer.py  (expected: A: 600, B: 900, all True)
"""
import asyncio


class Account:
    def __init__(self, balance: float):
        self.balance = balance


async def transfer(from_acc: Account, to_acc: Account, amount: float, lock: asyncio.Lock):
    async with lock:
        if from_acc.balance >= amount:
            from_acc.balance -= amount
            to_acc.balance += amount
            return True
        return False


async def main():
    account_a = Account(1000)
    account_b = Account(500)
    lock = asyncio.Lock()

    results = await asyncio.gather(
        transfer(account_a, account_b, 200, lock),
        transfer(account_a, account_b, 300, lock),
        transfer(account_b, account_a, 100, lock),
    )
    print(f"A: {account_a.balance}, B: {account_b.balance}")
    print(f"Results: {results}")


if __name__ == "__main__":
    asyncio.run(main())
