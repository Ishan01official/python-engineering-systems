# 02 — `asyncio`

For I/O concurrency in a single thread, asyncio is usually the best tool. It scales further than thread pools (you can have thousands of concurrent connections), uses less memory, and is the standard in modern Python web frameworks (FastAPI, aiohttp, etc.).

## The mental model

An asyncio program runs an **event loop**. Async functions (`async def`) yield control back to the loop whenever they hit an `await` on an I/O operation. While they wait, the loop runs *other* async functions. One thread, many in-flight operations.

This isn't magic. It only works for I/O that uses async-aware libraries. A blocking `requests.get(url)` will freeze the whole event loop. Use `aiohttp` or `httpx`'s async interface instead.

## Hello, asyncio

```python
import asyncio

async def fetch(name: str, delay: float) -> str:
    print(f"  {name} starting")
    await asyncio.sleep(delay)        # yields to the event loop
    print(f"  {name} done")
    return f"result_{name}"

async def main():
    # Run three concurrently
    results = await asyncio.gather(
        fetch("a", 1.0),
        fetch("b", 0.5),
        fetch("c", 0.7),
    )
    print(results)

asyncio.run(main())
```

Run time is ~1 second (the longest sleep), not 2.2 seconds (the sum).

## Core primitives

```python
# Run async code from sync code (top-level)
asyncio.run(main())

# Run multiple coroutines concurrently, wait for all
results = await asyncio.gather(coro1, coro2, coro3)

# Like gather but you can iterate as results arrive
for coro in asyncio.as_completed(coros):
    result = await coro

# Schedule a coroutine to run, get a Task back
task = asyncio.create_task(some_coro())
# ... later
result = await task
task.cancel()       # if needed

# Sleep (the canonical "yield to the loop" call)
await asyncio.sleep(0.5)

# Timeout a block
async with asyncio.timeout(5):
    await long_operation()
```

## When to use asyncio vs threads

- **Many connections (1000+), each mostly waiting** → asyncio. Web servers, scrapers, chat backends.
- **Modest concurrency (≤100), mixed sync libraries** → threads. Often simpler.
- **The whole stack supports async** → asyncio is the cleaner model.

A hybrid pattern that often works well: most code is sync; the parts that hit many remote services use a small async wrapper.

## Pitfalls

- **Don't call blocking code from async.** A `time.sleep(5)` inside an async function freezes everything. Use `await asyncio.sleep(5)`. For sync libraries you can't avoid, wrap with `await asyncio.to_thread(blocking_fn)`.
- **Don't `await` for "just one thing" inside a sync function.** If your function isn't async, you can't `await`. You'd need to be already inside an event loop.
- **Tasks need to be awaited or you'll get warnings.** `create_task(...)` schedules; if nothing ever awaits it and it raises, the error is silent.
- **Cancellation is cooperative.** A task only cancels at the next `await`. If it's stuck in a tight pure-Python loop, it won't cancel until the loop yields.

## A practical example

```python
import asyncio
import httpx

async def fetch(client: httpx.AsyncClient, url: str) -> int:
    r = await client.get(url, timeout=10)
    return len(r.content)

async def main(urls: list[str]) -> list[int]:
    async with httpx.AsyncClient() as client:
        tasks = [fetch(client, u) for u in urls]
        return await asyncio.gather(*tasks)

sizes = asyncio.run(main(urls))
```

50 URLs concurrently, one thread, low memory.

## Read deeper

- **FP** 2e, Ch. 21 — asyncio in depth
- **EP** 3e — items on asyncio
- Python docs: `asyncio`
