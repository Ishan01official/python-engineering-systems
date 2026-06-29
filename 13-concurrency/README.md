# 13 — Concurrency

How to make Python do more than one thing at a time. The right answer depends on whether the work is I/O-bound or CPU-bound, and is shaped by the GIL.

## Notes

1. [`01-threading-vs-multiprocessing.md`](./01-threading-vs-multiprocessing.md) — the choice, framed by the GIL
2. [`02-asyncio.md`](./02-asyncio.md) — async/await for I/O concurrency
3. [`03-gil.md`](./03-gil.md) — what it is, why it matters

## Diagrams

- [`diagrams/io-vs-cpu.mmd`](./diagrams/io-vs-cpu.mmd)

## Read deeper

- **FP** 2e, Ch. 19–21 — *the* deep dive on Python concurrency
- **EP** 3e — items on threads, processes, asyncio
