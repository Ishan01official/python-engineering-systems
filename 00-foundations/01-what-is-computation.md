# 01 — What is computation?

Before talking about Python, talk about what a program *is*.

## A computer is a machine that follows instructions on data

That's the whole job. Two things:

1. **Data** — numbers, in the end. Even text is numbers (codepoints). Even images are numbers (pixel values).
2. **Instructions** — "add these two numbers", "compare them", "jump to this point if they're equal".

Both data and instructions live in **memory** (RAM), as patterns of bits — 0s and 1s.

The **CPU** is the part that reads instructions one at a time and executes them. It has a tiny amount of ultra-fast storage called **registers** where it holds the values it's actively working on.

```
         ┌─────────────┐
         │   CPU       │   ← reads instructions, does math, decides "what next?"
         │  (registers)│
         └──────▲──────┘
                │
         ┌──────┴──────┐
         │    RAM      │   ← holds your program's data AND instructions
         └──────▲──────┘
                │
         ┌──────┴──────┐
         │   Disk      │   ← persistent storage. Slow.
         └─────────────┘
```

Speed gap matters: registers are ~1 ns, RAM is ~100 ns, disk is millions of ns. This is why "is my data in memory?" is the question that decides whether your program is fast or slow.

## Levels of abstraction

CPUs only understand **machine code** — raw binary instructions specific to the chip (x86, ARM, etc.). Nobody writes that by hand anymore. We climb a ladder of abstraction:

| Level | Example | Who runs it |
|---|---|---|
| Machine code | `10110000 01100001` | CPU directly |
| Assembly | `mov al, 0x61` | Assembler translates to machine code |
| C | `int x = 97;` | Compiler translates to machine code |
| Python | `x = 97` | Python interpreter (which itself is written in C) |

Each level **trades performance for ergonomics**. Python is many layers above the metal. You give up some speed; you gain enormous expressive power and don't have to think about memory layout, types, or hardware.

## Why Python?

Python was designed by Guido van Rossum (released 1991) with explicit goals:

- **Readable.** Code should look like pseudocode. Indentation enforces structure.
- **Batteries included.** A huge standard library out of the box.
- **One obvious way to do it.** (Mostly — see Tim Peters' "Zen of Python": `import this` in a Python shell.)
- **Glue language.** Easy to wrap C/C++ libraries, which is exactly how NumPy and pandas became dominant.

Trade-off: Python is **slower** than C for raw CPU work. But for the vast majority of programs, that doesn't matter — and for the parts where it does (NumPy, pandas), the heavy lifting is done in C anyway.

## What this means for you

- You're not writing instructions for a CPU. You're writing instructions for the **Python interpreter**, which then talks to the CPU on your behalf.
- "Run my code" really means "Python reads my source, turns it into bytecode, then walks through that bytecode executing each step."
- Most performance surprises in Python come from misunderstanding what the interpreter does for you "for free" — like copying objects, allocating new memory, or looking up attributes.

Next note: [`02-how-python-runs.md`](./02-how-python-runs.md).

## Read deeper

- **LP** 6e, Ch. 1–2 — Mark Lutz's framing of "why Python exists" is excellent.
