"""I/O-bound work with ThreadPoolExecutor, CPU-bound with ProcessPoolExecutor."""
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

import requests


def fetch_url(url):
    response = requests.get(url, timeout=10)
    return response.json()


urls = [
    "https://api.example.com/users/1",
    "https://api.example.com/users/2",
    "https://api.example.com/users/3",
]

# I/O-bound: more workers than cores is fine
with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(fetch_url, url): url for url in urls}
    for future in as_completed(futures):
        url = futures[future]
        try:
            data = future.result()
            print(f"Fetched {url}: {data}")
        except Exception as e:
            print(f"Failed {url}: {e}")


# CPU-bound: use processes, not threads (the GIL serializes threads)
def process_data(chunk):
    return sum(x ** 2 for x in chunk)


data = [range(0, 1000000), range(1000000, 2000000)]
with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_data, data))
