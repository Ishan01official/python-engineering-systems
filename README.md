# python-engineering-systems

Python fundamentals to advanced concepts explained with the Feynman technique:
read, explain simply, practice, then build.

This repo now has two complementary tracks:

- `Books/`, `practice/`, and `projects/learning_python_6e/` for book-driven study notes and applied exercises.
- Module folders `00-foundations/` through `20-data-engineering-patterns/` for a structured Python engineering curriculum with notes, examples, exercises, diagrams, and projects.

## Current Track

Primary book:

- `Books/Learning_Python-6th(Mark-Lutz)/` - notes for *Learning Python, 6th Edition* by Mark Lutz, published by O'Reilly.

Support book:

- `Books/Effective Python/` - idioms and professional Python habits to revisit after fundamentals.

The curriculum modules also reference these books:

| Tag | Book | Best for |
|-----|------|----------|
| **PCC** | Python Crash Course, 3rd Edition (Eric Matthes) | Basics, projects, "just get going" |
| **LP** | Learning Python, 6th Edition (Mark Lutz) | Encyclopedic reference, language details |
| **EP** | Effective Python, 3rd Edition (Brett Slatkin) | Idioms, "the right way" |
| **FP** | Fluent Python, 2nd Edition (Luciano Ramalho) | Data model, advanced patterns, mastery |
| **PfDA** | Python for Data Analysis, 3rd Edition (Wes McKinney) | NumPy, pandas, data work |

See [`BOOK_MAP.md`](./BOOK_MAP.md) for chapter-by-chapter mapping.

## How This Repo Is Organized

```text
Books/
  Learning_Python-6th(Mark-Lutz)/
    00_Study_System/          # progress, templates, review questions
    Part_1_...Part_8_...      # chapter notes grouped by book phase

practice/
  learning_python_6e/         # small focused exercises by part

projects/
  learning_python_6e/         # applied mini-projects
  01-cli-task-tracker/        # tested CLI project
  02-csv-to-dataframe-pipeline/
  03-mini-etl-pipeline/

00-foundations/ ... 20-data-engineering-patterns/
  README.md                   # why this module matters
  01-*.md, 02-*.md, ...       # ordered notes
  examples/                   # runnable code
  exercises/                  # practice prompts
```

## How to Use the Curriculum

1. Read the module README first - it explains why the topic matters before what it is.
2. Read the numbered notes (`01-*.md`, `02-*.md`, ...) in order.
3. Open the `examples/` folder, run the scripts, change a line, re-run. Do not just read code.
4. Do the `exercises/`. Commit your solutions in the same folder as `solution_*.py`.
5. Check off the module in [`ROADMAP.md`](./ROADMAP.md).

To run any example:

```bash
python <module>/examples/<file>.py
```

To run tests on a project:

```bash
cd projects/01-cli-task-tracker
python -m pytest tests/ -v
```

## Learning Path

### Tier 1 - Foundations

- **00** - How computation and Python actually work
- **01** - Syntax, types, mutability
- **02** - Control flow
- **03** - Built-in data structures: list, tuple, dict, set
- **04** - Functions, scope, first-class functions

### Tier 2 - Real Programs

- **05** - Modules, packages, imports, virtual environments
- **06** - Files and I/O
- **07** - Errors and exceptions
- **08** - Object-oriented programming
- **09** - Iterators and generators
- **10** - Decorators and context managers

### Tier 3 - Professional Python

- **11** - Type hints, protocols, generics
- **12** - Testing: unittest and pytest
- **13** - Concurrency: threading, multiprocessing, asyncio, GIL
- **14** - Effective Python patterns

### Tier 4 - Data Engineering Track

- **15** - NumPy
- **16** - pandas
- **17** - Data cleaning, joins, reshaping
- **18** - Jupyter notebooks
- **20** - Data engineering patterns: ETL, AWS Lambda, S3 pipelines

### Tier 5 - Mastery

- **19** - Fluent Python deep dives: data model, dunders, metaclasses

## Study Loop

For each chapter or module:

1. Read once without coding.
2. Write a short Feynman explanation in your own words.
3. Reproduce the important examples from memory.
4. Solve 3-5 small exercises.
5. Build or improve one tiny applied program.
6. Record unclear points in `00_Study_System/questions.md` or a local module notes file.

## Repo Conventions

- Every curriculum module has a `README.md`, numbered notes, runnable examples, and exercises.
- Diagrams are Mermaid (`.mmd`) and render directly on GitHub.
- Code targets Python 3.11+.
- All examples are runnable as `python path/to/file.py` from the repo root.

See [`CONVENTIONS.md`](./CONVENTIONS.md) for full details.

## Rule

Do not just collect notes. Every concept should produce code in `practice/`, `projects/`, or a module `examples/` or `exercises/` folder.
