# 04 — Virtual environments and dependency management

## The problem

Without isolation, every Python project on your machine shares one set of installed packages. Two projects needing different versions of the same library will conflict. Worse, your system Python (the one your OS uses) gets polluted.

The fix is to give each project its own isolated Python with its own packages.

## `venv` — the built-in tool

```bash
# Create
python3 -m venv .venv

# Activate
source .venv/bin/activate           # macOS / Linux
.venv\Scripts\Activate.ps1          # Windows PowerShell

# Now `python` and `pip` refer to the venv's
pip install pandas numpy

# Deactivate when done
deactivate
```

After activation, your prompt should show `(.venv)`. `pip install` from this point installs only into the venv. No global pollution.

## `requirements.txt`

A flat list of dependencies. The simplest way to make a project reproducible:

```
pandas>=2.1
numpy>=1.26
pytest>=8.0
```

Install with:

```bash
pip install -r requirements.txt
```

To freeze your current state into a file (so a teammate can reproduce):

```bash
pip freeze > requirements.txt
```

`pip freeze` outputs every installed package with exact versions — handy for snapshots, but verbose. For libraries you write yourself, list only direct dependencies, not transitive ones.

## `pyproject.toml` — the modern way

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "pandas>=2.1",
    "numpy>=1.26",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "ruff", "mypy"]
```

Install your project (and its deps) in editable mode:

```bash
pip install -e .[dev]
```

This is the format most new projects use. `pip` understands it; so do `uv`, `poetry`, `hatch`, etc.

## Choosing a tool

- **`venv` + `pip`** — built in, fine for learning and small projects.
- **`uv`** — much faster than pip, manages venvs and installs together. Currently a strong default for new Python projects.
- **`poetry`** — older but mature; manages venvs, dependencies, and packaging together.
- **`conda`** — when your dependencies include heavy non-Python pieces (CUDA, GDAL, certain scientific libs).

For this curriculum, `venv` + `pip` is enough.

## Common workflow

```bash
# new project
cd my-project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# day to day
source .venv/bin/activate         # always before working
# ... do work ...
deactivate                         # when leaving

# adding a dep
pip install some-lib
# then add `some-lib>=1.0` to requirements.txt (or pyproject.toml) so others can reproduce
```

## Pitfalls

- **Forgetting to activate.** `which python` should show the `.venv` path. If it shows `/usr/bin/python3`, you're in the system Python.
- **Mixing global and venv installs.** If you ever did `sudo pip install ...` on macOS or Linux, that polluted your system Python. Don't do that. Use venvs.
- **Committing the `.venv/` directory.** Don't. It's in our `.gitignore`. Reproducibility comes from the `requirements.txt`, not from shipping binaries.
- **Editable installs and tests.** When testing a package you're developing, `pip install -e .` lets you import it from anywhere in the venv without rerunning install on each edit.

## Read deeper

- Python docs: https://docs.python.org/3/library/venv.html
- pip docs: https://pip.pypa.io
- `uv` docs: https://github.com/astral-sh/uv
