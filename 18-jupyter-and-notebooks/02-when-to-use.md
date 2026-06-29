# 02 — Notebooks vs scripts vs production code

Notebooks are great for some things and terrible for others. Choosing the right tool saves real pain.

## Notebooks are great for

- **Exploration.** "What does this data look like? What's the distribution? Is there a correlation?"
- **One-off analysis** that produces a report or chart and is then thrown away.
- **Teaching and presentations.** Inline plots + markdown narrative is the killer feature.
- **Tutorials and reproducible papers.** Anyone can follow along by running cells.

## Notebooks are bad for

- **Anything that goes to production.** Cron jobs, ETL pipelines, services, APIs. Use scripts/modules.
- **Code that grows past ~200 lines.** Notebooks become unwieldy — no proper testing, no easy diff, no module structure.
- **Code reuse.** You can't `import` a notebook cleanly. If you find yourself copy-pasting between notebooks, extract a `.py` module and import from both.
- **Long-running jobs.** A notebook that runs for hours and dies mid-cell loses everything. Scripts can be restarted, logged, retried.
- **Anything tested.** Notebooks aren't testable in the normal sense. Move the logic to a module; test the module; call from the notebook.

## The healthy split

A common project layout:

```
my-analysis/
├── src/myproject/         # importable code: functions, classes
│   ├── data.py
│   └── models.py
├── tests/                  # tests for src/
├── notebooks/              # exploratory; throw-away
│   ├── 01-explore-data.ipynb
│   └── 02-prototype-model.ipynb
└── scripts/                # production-y entry points
    ├── train.py
    └── score.py
```

The notebook imports from `src/`. The scripts import from `src/`. The tests verify `src/`. The notebook is *not* the source of truth — `src/` is.

This way:
- The fast-iteration notebook gives you the prototyping speed.
- The `.py` files give you testability, versioning, code review.
- The same logic powers exploration AND production.

## Promoting notebook code to a module

When a notebook function "works", and you'll use it more than twice:

1. Move it to `src/myproject/something.py`.
2. Import it back in the notebook (`from myproject.something import the_fn`).
3. Use `%autoreload 2` so edits to the module are picked up live.
4. Write a test in `tests/`.

That migration path is the single most important habit for moving from "notebook user" to "Python engineer."

## Sharing notebooks

- **GitHub renders `.ipynb` files** directly. Just commit them. Outputs are visible without re-running.
- **`nbviewer.org`** for shareable links.
- **`papermill`** runs notebooks programmatically with parameters — great for "run this notebook every morning with yesterday's date."
- **`jupytext`** keeps a `.py` "mirror" of your notebook in version control, which diffs cleanly. Optional but nice.

## Don't commit outputs you don't want public

A notebook can leak: a printed API key, a head of a customer dataset, a screenshot showing internal salaries. Use `nbstripout` (a git pre-commit hook) to strip outputs from committed notebooks if your repo is public.
