# 04 — Concurrency idioms

These are the higher-level rules of thumb. Module 13 covers mechanics.

## Use `concurrent.futures` instead of raw `Thread` / `Process`

Higher-level, simpler API, easier to switch between threads and processes.

## Don't share mutable state between threads

If two threads write to the same dict or list, you have a race condition. Solutions:

- **Don't.** Have each thread do its own work and return a value; combine results in the main thread.
- **Queues.** `queue.Queue` is thread-safe; use it to pass work between threads.
- **Locks.** Last resort. Easy to forget, easy to deadlock.

## Don't share large objects between processes

Pickling 100 MB across a process boundary is expensive. Either:

- Pass small keys/identifiers; have each worker load what it needs.
- Use `multiprocessing.shared_memory` for true shared arrays.

## Use asyncio for many concurrent I/O operations

Better scaling than threads (thousands of concurrent connections), single thread, no race conditions on shared state.

## Don't mix sync I/O into async code

A `time.sleep`, `requests.get`, or `open().read()` in an async function freezes the event loop. Use `await asyncio.sleep`, `httpx` / `aiohttp`, `aiofiles` — or wrap sync code with `await asyncio.to_thread(...)`.

## Profile before parallelizing

A common mistake: adding threads/processes to "make it faster" without measuring. Often the bottleneck is somewhere else entirely (the algorithm, the database, the network), and parallelism just adds complexity. Use `time.perf_counter` or `cProfile` first.

## Beware the GIL surprise

Pure-Python CPU work doesn't speed up with threads. Use processes. NumPy/pandas/PIL CPU work *does* speed up with threads — those release the GIL.

## Read deeper

- **EP** 3e — concurrency chapter
- **FP** 2e, Ch. 19–21 — concurrent and parallel programming
