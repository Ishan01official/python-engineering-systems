# 03 — Setting up your environment

The bare minimum so you can write, run, and isolate Python projects without making a mess.

## 1. Install Python 3.11 or newer

Check what you have:

```bash
python3 --version
```

If it's older than 3.11 or missing:

- **macOS:** install [Homebrew](https://brew.sh), then `brew install python@3.12`
- **Ubuntu/Debian:** `sudo apt update && sudo apt install python3.12 python3.12-venv`
- **Windows:** install from [python.org](https://www.python.org/downloads/). Check "Add Python to PATH" during install.

A common alternative on macOS/Linux is **`pyenv`** which lets you keep multiple Python versions side by side. Worth setting up once you outgrow the system Python.

## 2. Why virtual environments matter

If you install packages globally (`pip install pandas`), every Python project on your machine shares them. Two projects needing different versions of the same library will fight. Virtual environments solve this by giving each project its **own isolated** Python and packages.

Create one for this repo:

```bash
cd python-engineering-systems
python3 -m venv .venv
```

Activate it:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Your shell prompt should now show `(.venv)`. Install the requirements:

```bash
pip install -r requirements.txt
```

When you're done working: `deactivate`.

**Rule of thumb:** never `pip install` something without a venv active. The pain you save is significant.

## 3. Editor

Use **VS Code** with the official Python extension (free). Other strong choices: PyCharm Community Edition, Cursor.

Two settings that pay back immediately:

- Turn on **format on save** with **Ruff** or **Black** as the formatter. Stops you from arguing with yourself about whitespace.
- Turn on **inline type checking** (Pylance in VS Code). It catches a huge class of bugs before you run anything.

## 4. The REPL is your best friend

```bash
python3
>>> 2 + 2
4
>>> "hello".upper()
'HELLO'
```

The REPL (Read-Eval-Print Loop) lets you try things interactively. Use it constantly while learning — don't write a 50-line script to test an idea, just paste a few lines into the REPL.

A nicer REPL: **IPython** (`pip install ipython`). Tab completion, syntax highlighting, history. Run it with `ipython`.

## 5. Sanity-check your setup

Run [`examples/02_check_setup.py`](./examples/02_check_setup.py):

```bash
python 00-foundations/examples/02_check_setup.py
```

It should print your Python version, executable path, and confirm `numpy` and `pandas` import.

Next note: [`04-mental-model-execution.md`](./04-mental-model-execution.md).

## Read deeper

- **PCC** 3e, Ch. 1 — most beginner-friendly setup walkthrough.
