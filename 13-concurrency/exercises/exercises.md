# Module 13 — Exercises

## E13.1 — Pick the right tool

For each, decide: `ThreadPoolExecutor`, `ProcessPoolExecutor`, or `asyncio`. Justify in one sentence each.
1. Download 200 web pages.
2. Compute the SHA-256 of 50 multi-GB files (pure Python, no C extension).
3. Resize 50 JPEGs using Pillow.
4. Read 10,000 small JSON files from disk.
5. Run a custom regex over 1 GB of pure-Python text — no NumPy/pandas.

## E13.2 — Threaded URL fetcher

Write `fetch_all(urls, max_workers=10)` that fetches all URLs using `ThreadPoolExecutor` and returns `dict[url, status_code]`. Use `urllib.request` (no installs needed). Time it vs a sequential version using `time.perf_counter`.

## E13.3 — CPU-bound benchmark

Write a CPU-heavy function `count_primes(start, end)`. Benchmark serial vs `ThreadPoolExecutor` vs `ProcessPoolExecutor`. Confirm that threads give no speedup while processes scale roughly with `os.cpu_count()`.

## E13.4 — asyncio with `gather`

Using `asyncio.sleep` (no real network), simulate fetching N "URLs" each taking 0.5s. Show that `await asyncio.gather(*tasks)` finishes in ~0.5s regardless of N (up to maybe 1000), demonstrating asyncio's scaling.

## E13.5 — Cancellation

Start a task that runs an infinite `while True: await asyncio.sleep(0.1)`. After 1 second, cancel it. Catch `asyncio.CancelledError` inside the task and print a "cleanup" message. Show that the cleanup runs.

## E13.6 — Race condition

This buggy code under-counts. Why? Show a fix using `threading.Lock`.
```python
import threading
counter = 0
def increment():
    global counter
    for _ in range(100_000):
        counter += 1

ts = [threading.Thread(target=increment) for _ in range(8)]
[t.start() for t in ts]
[t.join() for t in ts]
print(counter)   # not 800_000
```
