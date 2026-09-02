import asyncio
import aiohttp


async def fetch_pages(base_url, total_pages, page_size=100):
    """Async generator that yields paginated API data lazily."""
    async with aiohttp.ClientSession() as session:
        for offset in range(0, total_pages, page_size):
            url = f"{base_url}?offset={offset}&limit={page_size}"
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                data = await response.json()
                if not data:
                    break
                yield data


async def fetch_lines(file_path):
    """Async generator that yields lines from a file without loading it all."""
    with open(file_path, 'r') as f:
        for line in f:
            await asyncio.sleep(0)  # Yield control to event loop
            yield line.strip()


async def process_all():
    """Consumer that processes pages with constant memory."""
    total = 0
    async for page in fetch_pages("https://api.example.com/items", 10000):
        for item in page:
            total += item["price"]
        print(f"Processed page, running total: {total}")
    print(f"Final total: {total}")


async def process_with_early_exit():
    """Consumer that breaks early and properly closes the generator."""
    gen = fetch_pages("https://api.example.com/items", 10000)
    try:
        async for page in gen:
            if len(page) == 0:
                break
            print(f"Got {len(page)} items")
            break
    finally:
        await gen.aclose()


if __name__ == "__main__":
    asyncio.run(process_all())
