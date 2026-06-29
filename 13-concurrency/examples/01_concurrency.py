"""
Concurrency: threads, processes, asyncio.

Run:
    python 13-concurrency/examples/01_concurrency.py
"""
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


# ---- simulated I/O-bound work ---------------------------------------------

def fetch_io(name: str, delay: float = 0.5) -> str:
    """Simulates an I/O call by sleeping."""
    time.sleep(delay)
    return f"got_{name}"


# ---- pure-CPU work --------------------------------------------------------

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True


# ---- 1. Sequential baseline -----------------------------------------------

def sequential(items, fn) -> tuple[list, float]:
    start = time.perf_counter()
    results = [fn(item) for item in items]
    return results, time.perf_counter() - start


# ---- 2. Threads (good for I/O) -------------------------------------------

def with_threads(items, fn, workers=8) -> tuple[list, float]:
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(fn, items))
    return results, time.perf_counter() - start


# ---- 3. Processes (good for CPU) -----------------------------------------

def with_processes(items, fn, workers=4) -> tuple[list, float]:
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(fn, items))
    return results, time.perf_counter() - start


# ---- 4. asyncio (best for many I/O ops) ---------------------------------

async def fetch_async(name: str, delay: float = 0.5) -> str:
    await asyncio.sleep(delay)        # async-aware sleep
    return f"got_{name}"


async def with_asyncio(names) -> tuple[list, float]:
    start = time.perf_counter()
    results = await asyncio.gather(*[fetch_async(n) for n in names])
    return results, time.perf_counter() - start


# ---- run -----------------------------------------------------------------

if __name__ == "__main__":
    names = [f"req{i}" for i in range(8)]

    print("=== I/O work (8 fake requests, 0.5s each) ===")
    _, t_seq = sequential(names, fetch_io)
    print(f"  sequential:    {t_seq:.2f}s")

    _, t_thr = with_threads(names, fetch_io, workers=8)
    print(f"  threads (8):   {t_thr:.2f}s")

    _, t_async = asyncio.run(with_asyncio(names))
    print(f"  asyncio:       {t_async:.2f}s")

    # CPU work
    big = [99_999_989, 99_999_991, 99_999_999, 99_999_997, 99_999_959, 99_999_931]
    print("\n=== CPU work (primality of 6 large numbers) ===")

    _, t_cpu_seq = sequential(big, is_prime)
    print(f"  sequential:        {t_cpu_seq:.2f}s")

    _, t_cpu_thr = with_threads(big, is_prime, workers=4)
    print(f"  threads (4):       {t_cpu_thr:.2f}s   (no speedup — GIL serializes)")

    _, t_cpu_proc = with_processes(big, is_prime, workers=4)
    print(f"  processes (4):     {t_cpu_proc:.2f}s   (true parallelism)")
