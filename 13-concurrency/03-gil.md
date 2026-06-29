# 03 — The GIL

The **Global Interpreter Lock** is a mutex inside CPython that ensures only one thread executes Python bytecode at a time. It exists because CPython's memory management (reference counting) isn't thread-safe; the GIL is a coarse-grained solution that protects everything at once.

Practical consequences:

- **Threads don't give you CPU parallelism in pure Python.** Two threads doing pure-Python math on a 4-core machine won't run faster than one thread.
- **Threads DO give you I/O concurrency.** While a thread is waiting on a network call, the GIL is released. Other threads run. This is why thread pools are useful for parallel HTTP requests, parallel file reads, etc.
- **C extensions can release the GIL.** NumPy, pandas, image libraries, etc. release it during their heavy loops. So when 99% of your CPU time is in NumPy, threading *does* give you parallelism.
- **Multiprocessing bypasses the GIL.** Each process has its own interpreter and its own GIL — but they don't conflict. Use it for CPU-bound pure-Python work.

## Python 3.13's experimental no-GIL mode

Python 3.13 added an experimental "free-threaded" build with no GIL. It's not the default, has performance overhead in single-threaded code, and many libraries haven't yet certified safety. For now, design as if the GIL is present. Watch the space over the next few years.

## What to choose

| Workload | Choice |
|---|---|
| Many I/O calls (HTTP, files, DB) | **asyncio** (best), or threads |
| Mostly NumPy/pandas | threads — the C code releases the GIL |
| Pure-Python CPU crunching | **multiprocessing** |
| Single-threaded, just want it faster | Profile first. Maybe just rewrite the hot loop with NumPy. |

## The TL;DR

Threads in Python feel like threads in other languages but aren't — they give you concurrency, not parallelism, for pure Python. Don't reach for them to "speed up math".
