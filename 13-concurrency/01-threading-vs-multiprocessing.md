# 01 — Threading vs multiprocessing

The first concurrency decision: many threads, or many processes? Driven by what kind of work you're doing.

## `concurrent.futures` — the easy API

For most use cases, don't touch `threading.Thread` or `multiprocessing.Process` directly. Use `concurrent.futures`:

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# I/O work — threads are fine
with ThreadPoolExecutor(max_workers=10) as pool:
    results = list(pool.map(fetch_url, urls))

# CPU work — separate processes bypass the GIL
with ProcessPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(crunch_numbers, datasets))
```

Same API, different executor. The cost of switching is a one-line change.

## Threads: when they help

- **Many concurrent I/O operations** — downloading 100 URLs, hitting many databases, reading many files.
- **Calling NumPy/pandas/PIL/etc. in parallel** — those release the GIL during their C code.
- **Keeping a GUI/server responsive** while doing background work.

Threads share memory by default, which is both convenient and dangerous (race conditions, deadlocks). Use `queue.Queue` to pass work between them; avoid sharing mutable state.

## Processes: when they help

- **CPU-bound pure-Python work** — image processing in pure Python, simulations, heavy parsing.
- **Workloads that benefit from isolation** — a crashed worker doesn't take down the rest.

Processes don't share memory; each has its own Python interpreter. To pass data, the executor pickles and unpickles it across an IPC channel. That has a real cost — sending large objects is slow. Profile before assuming multiprocessing is faster.

## A typical I/O-bound example

```python
import time, urllib.request
from concurrent.futures import ThreadPoolExecutor

def fetch(url: str) -> int:
    with urllib.request.urlopen(url, timeout=10) as r:
        return len(r.read())

urls = [...]   # 50 URLs

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=20) as pool:
    sizes = list(pool.map(fetch, urls))
print(f"{time.perf_counter() - start:.2f}s for {len(urls)} URLs")
```

Serial fetching of 50 URLs at 200 ms each: ~10 seconds.
Threaded with 20 workers: ~0.5 seconds. The GIL doesn't matter because threads are waiting on the network.

## A typical CPU-bound example

```python
from concurrent.futures import ProcessPoolExecutor

def is_prime(n: int) -> bool:
    if n < 2: return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True

big_numbers = [99999989, 99999991, ...]   # many

with ProcessPoolExecutor() as pool:
    results = list(pool.map(is_prime, big_numbers))
```

With threads, the GIL serializes execution and you'd see near-zero speedup. With processes, each worker is on its own core.

## Pitfalls

- **`max_workers` too high** — diminishing returns, then it makes things worse. For threads: ~2–4× your CPU count for I/O, less for mixed. For processes: usually `os.cpu_count()`.
- **Sharing mutable state between threads** without locks → race conditions.
- **Pickling cost in multiprocessing** — sending 100 MB per call kills your throughput. Use shared memory or chunk the work.
- **Process pools and Windows / Jupyter** — child processes re-import the module, so guards like `if __name__ == "__main__":` are required.

## Read deeper

- **FP** 2e, Ch. 19 — threads, processes, futures
- **EP** 3e — items on `concurrent.futures`, threads vs processes
