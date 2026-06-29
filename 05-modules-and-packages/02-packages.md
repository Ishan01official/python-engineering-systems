# 02 — Packages

A **package** is a directory containing modules, with an optional `__init__.py` to mark it. Packages let you group related modules into a namespace.

## Layout

```
my_project/
├── data/
│   ├── __init__.py
│   ├── load.py
│   └── clean.py
├── models/
│   ├── __init__.py
│   ├── linear.py
│   └── tree.py
└── main.py
```

Now `data.load`, `data.clean`, `models.linear` are all importable from `main.py`:

```python
from data.load import read_csv
from models.linear import train
```

## `__init__.py`

The presence of `__init__.py` (even empty) marks the directory as a *regular package*. It runs the first time any module in the package is imported.

Common uses:

- **Empty file** — just marks the directory.
- **Re-exports** — make the package's API flat:
  ```python
  # data/__init__.py
  from .load import read_csv, read_parquet
  from .clean import dropna_strict
  ```
  Now callers can write `from data import read_csv` instead of `from data.load import read_csv`.
- **Package-level constants** — version strings, defaults.

Python 3.3+ supports "**namespace packages**" — directories without `__init__.py` that still work as packages. For most projects, just use `__init__.py`. It's explicit and the tooling is universal.

## Relative imports

Inside a package, you can import sibling modules with `.`:

```python
# data/clean.py
from .load import read_csv          # same package
from ..models import linear          # parent package
```

- `.` = current package
- `..` = parent package

Relative imports only work inside a package being imported — not when you run a file directly with `python clean.py`. Use `python -m data.clean` instead, or absolute imports.

**Rule of thumb:** prefer absolute imports (`from data.load import ...`). Use relative imports only within tightly-coupled modules of the same package.

## Project layout that scales

A common modern layout (assumed by tools like `pip`, `pytest`):

```
my-project/
├── README.md
├── pyproject.toml         # project metadata, deps, build config
├── src/
│   └── my_project/        # the actual Python package
│       ├── __init__.py
│       ├── data.py
│       └── models.py
├── tests/
│   ├── test_data.py
│   └── test_models.py
└── docs/
```

The `src/` layout prevents accidentally importing your package from the project root when running tests — a subtle issue that's saved many teams. Not mandatory for learning projects, but worth knowing.

## `pyproject.toml` (briefly)

The modern way to declare a Python project. Minimal version:

```toml
[project]
name = "my-project"
version = "0.1.0"
dependencies = [
    "pandas>=2.1",
    "requests>=2.31",
]

[build-system]
requires = ["setuptools>=64", "wheel"]
build-backend = "setuptools.build_meta"
```

`pip install -e .` installs your project in "editable" mode — changes to the source are picked up immediately. Great for development.

## Read deeper

- **LP** 6e, Ch. 24 (package imports)
- **PCC** 3e, Ch. 9 — class organization across modules
- Official guide: https://packaging.python.org/
