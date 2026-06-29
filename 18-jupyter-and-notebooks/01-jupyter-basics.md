# 01 — Jupyter basics

A **notebook** is a sequence of cells (code or text) that you run interactively. State persists across cell executions, so you can poke at variables, plot inline, and iterate fast.

## Installing and starting

```bash
pip install jupyter
jupyter lab           # the modern interface
# or
jupyter notebook      # the classic one
```

JupyterLab is the default for new work. The notebook file format is `.ipynb` (JSON under the hood) — same on both.

## Cell types

- **Code** — Python that runs when you press Shift+Enter. Output appears below.
- **Markdown** — formatted text. For headings, prose, equations, embedded images.
- **Raw** — text passed through unchanged. Rarely used.

A typical exploratory notebook is ~70% code, ~30% markdown explaining what each section does.

## Essential shortcuts

| Key | What |
|---|---|
| Shift+Enter | run cell, move to next |
| Ctrl+Enter | run cell, stay |
| Esc + a / b | new cell above / below |
| Esc + d d | delete cell |
| Esc + m / y | switch to markdown / code |
| Tab | autocomplete |
| Shift+Tab | docstring popup |

## IPython magics

Commands starting with `%` (line) or `%%` (cell):

```python
%timeit some_expr()              # micro-benchmark
%time some_expr()                # one-shot timing
%who                              # list variables in scope
%load_ext autoreload
%autoreload 2                     # reload imported modules on every cell run

%%bash
ls -la                            # run shell in this cell

%%writefile /tmp/snippet.py
def hello(): print("hi")          # write the cell's body to a file
```

`%autoreload 2` is the magic that makes notebook development bearable: edit a `.py` file in your project, then re-run a cell, and your changes are picked up automatically.

## Plots inline

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x))
plt.show()
```

In modern Jupyter, `plt.show()` isn't strictly needed — the last expression of a cell auto-displays. But it's harmless and explicit.

## A useful starter cell

Put this at the top of every analysis notebook:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%load_ext autoreload
%autoreload 2

pd.set_option("display.max_columns", 100)
pd.set_option("display.width", 200)
```

## Tips

- **Cells are not files.** Save often (it's just a JSON file on disk).
- **Restart and run all** before declaring an analysis done. Notebooks let you run cells out of order, which is convenient and dangerous — final results should be reproducible top-to-bottom.
- **Long outputs** (10,000-row DataFrames) bloat the file. Truncate or save to disk; don't dump them in cells.
