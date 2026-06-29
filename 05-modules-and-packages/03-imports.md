# 03 — Imports: how they actually work

## The search path: `sys.path`

When you `import x`, Python walks through directories in `sys.path` looking for `x`. Roughly:

1. The directory of the running script (or current working directory in an interactive shell).
2. Directories listed in the `PYTHONPATH` environment variable.
3. Directories of installed packages (your venv's `site-packages`).
4. Built-in / standard-library locations.

```python
import sys
print(sys.path)        # see the list
```

If you ever get `ModuleNotFoundError: No module named 'X'`, the first questions are:

- Is `X` actually installed in this Python? (`pip show X` or `python -m pip list`)
- Is the venv activated? Is the right Python being used? (`which python`, `python -c "import sys; print(sys.executable)"`)
- Is your current directory the project root?

## The import cache

The first time a module is imported, Python:

1. Finds it.
2. Compiles it to bytecode (cached in `__pycache__`).
3. Executes the top-level code, building a module object.
4. Stores the module object in `sys.modules`.

Subsequent imports just look up `sys.modules[name]` and return the same object. **Module-level code runs once per process.** If you change the file, you have to restart Python (or use `importlib.reload`, but that's a rabbit hole).

## Avoiding circular imports

If `a.py` imports from `b.py` and `b.py` imports from `a.py`, you get a circular import. Sometimes it works (Python is forgiving), sometimes it doesn't (and the error message is confusing).

Fixes:

1. **Reorganize.** Often the two modules share something that should be in a third module.
2. **Import inside a function.** Top-level imports run on first import; function-body imports run when the function is called.
   ```python
   def serialize(obj):
       from .formats import json_format    # lazy import
       return json_format.dump(obj)
   ```
3. **Import only what you need at top level**, and the rest inside functions.

## `from X import *` — say no

Three reasons not to:

1. Readers can't tell where a name came from.
2. It silently overrides any local name with the same name from `X`.
3. It tightly couples your namespace to whatever `X` happens to expose.

The single exception: in your package's `__init__.py`, for deliberate re-exports. Even then, list `__all__` to be explicit:

```python
# my_pkg/__init__.py
from .core import Engine, run
__all__ = ["Engine", "run"]
```

## Import order convention (PEP 8)

```python
# 1. Standard library
import json
import os
from pathlib import Path

# 2. Third-party packages
import numpy as np
import pandas as pd

# 3. Your own modules
from my_project.data import load
from my_project.models import Linear
```

Tools like `ruff`, `isort`, and `black` will enforce this automatically. Turn one on.

## A useful debugging tool: `python -i script.py`

Runs `script.py`, then drops you into an interactive prompt **with all the script's variables in scope**. Great for poking at state after a script runs.

## Read deeper

- **LP** 6e, Ch. 23 (module coding basics), Ch. 25 (advanced module topics)
- Python's docs: https://docs.python.org/3/reference/import.html
