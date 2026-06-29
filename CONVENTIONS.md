# Conventions

## Folder structure for every module

```
NN-topic/
├── README.md              # The "why" — what this module is for, what you'll learn
├── 01-thing-one.md        # The "what" — notes, in reading order
├── 02-thing-two.md
├── ...
├── examples/              # Runnable .py files demonstrating each concept
│   ├── 01_thing_one.py
│   └── ...
├── exercises/             # Problems to do yourself
│   └── exercises.md
└── diagrams/              # Mermaid diagrams (.mmd) — render on GitHub
    └── *.mmd
```

## Note style

- **Short over long.** Notes are study aids, not textbooks. The books cover the depth.
- **One idea per heading.** Use a runnable example for every concept.
- **End with a "Common mistakes" or "Pitfalls" section** so you remember what trips people up.
- **Cross-reference the books** at the top: a "Read deeper" block linking the relevant chapters by tag (PCC, LP, EP, FP, PfDA).

## Code style

- Python 3.11+.
- Use type hints in non-trivial code.
- Each example file starts with a docstring saying what it demonstrates.
- Use `if __name__ == "__main__":` so files are both importable and runnable.

## Diagrams

- Mermaid (`.mmd`) for flowcharts, sequence, class diagrams. GitHub renders them inline.
- Use when the concept is *structural* (call stack, class hierarchy, dataflow). Don't draw a diagram of a `for` loop.

## Commit messages

Use a tag prefix so history is greppable:

```
NOTES(03): add dict ordering note
CODE(04): closure example
DIAGRAM(08): class inheritance for Shape/Circle
FIX(02): typo in for-loop note
PROJECT(01): scaffold CLI task tracker
```
