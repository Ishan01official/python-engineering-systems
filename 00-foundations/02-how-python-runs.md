# 02 — How Python actually runs your code

When you type `python my_script.py` and hit Enter, here is what really happens. (Simplified, but accurate.)

## The pipeline

```
your_code.py
    │
    │  (1) Read the source file (text → tokens)
    ▼
Tokens     e.g. NAME("x"), OP("="), NUMBER(5)
    │
    │  (2) Parse tokens into a tree (Abstract Syntax Tree)
    ▼
AST        a tree representation of the program's structure
    │
    │  (3) Compile the AST into bytecode
    ▼
Bytecode   .pyc files; a sequence of simple ops for the Python VM
    │
    │  (4) The Python Virtual Machine executes bytecode, op by op
    ▼
Behavior   things print, files get written, etc.
```

You can actually see step 3 yourself:

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
```

You'll see something like:

```
LOAD_FAST    a
LOAD_FAST    b
BINARY_OP    +
RETURN_VALUE
```

Those four lines are the bytecode the interpreter executes. They're stack-based — values get pushed onto a stack, operations consume them.

## CPython, PyPy, and "is Python compiled or interpreted?"

People argue about this. The honest answer is: **both**.

- "Python" the language is a specification.
- "CPython" is the standard implementation — the one you get from python.org. It's written in C.
- CPython **compiles** your source to bytecode, then **interprets** the bytecode.
- Other implementations exist: **PyPy** (which JIT-compiles bytecode to machine code at runtime — often 4–10× faster); **MicroPython** (for microcontrollers); etc.

When this curriculum says "Python", read it as "CPython 3.11+ unless noted".

## What `.pyc` files are

The first time you import a module, CPython compiles its source to bytecode and caches it in `__pycache__/module.cpython-311.pyc`. Next import → reads the cached bytecode → skips re-compilation.

This is purely an optimization. You can delete `__pycache__/` any time; it'll be regenerated. Never commit it (the `.gitignore` in this repo blocks it).

## The Global Interpreter Lock (GIL) — a teaser

CPython has a famous design choice: at any moment, **only one thread of Python code runs at a time**, even on a multi-core machine. This is the GIL. It simplifies the interpreter's memory management at a real cost: pure-Python multithreading doesn't give you parallel CPU speedup.

We'll come back to this in [Module 13 — Concurrency](../13-concurrency/). For now, just know: this is *why* NumPy and pandas drop into C, and why "threads" in Python aren't always what you'd expect from threads in Java.

(Note: Python 3.13+ introduced an experimental no-GIL mode. The traditional GIL is still the default and what most code assumes.)

## What this means for you as a learner

- When you write `x = 5`, the interpreter creates an `int` object, makes the name `x` refer to it, and that's a chunk of bytecode getting executed.
- "Reading code" is also what the interpreter does. If you can trace through code line by line in your head, you're doing what the interpreter does — just slower.
- Performance debugging often starts at the bytecode level (`dis.dis(fn)`). You don't need it on day one. But knowing it exists prevents magical thinking later.

## Try it yourself

Run [`examples/01_disassemble.py`](./examples/01_disassemble.py).

Next note: [`03-setup-environment.md`](./03-setup-environment.md).

## Read deeper

- **LP** 6e, Ch. 2 — covers the runtime model in much more depth.
- **FP** 2e, Ch. 1 — the Python data model, which is the next layer up.
