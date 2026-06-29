# 02 — Paths with `pathlib`

`os.path` is the old way. `pathlib.Path` is the modern way. **Use `pathlib`.** It's object-oriented, much more readable, and works the same on every OS.

## The basics

```python
from pathlib import Path

p = Path("data") / "raw" / "users.csv"
# Path('data/raw/users.csv')

p.exists()             # True/False
p.is_file()            # True/False
p.is_dir()             # True/False
p.name                 # 'users.csv'
p.stem                 # 'users'
p.suffix               # '.csv'
p.parent               # Path('data/raw')
p.parts                # ('data', 'raw', 'users.csv')
p.absolute()           # full path
```

The `/` operator joins paths — no more `os.path.join`. Works the same on Windows and Unix.

## Read and write directly

```python
text = Path("config.txt").read_text(encoding="utf-8")
data = Path("img.png").read_bytes()

Path("out.txt").write_text("hello\n", encoding="utf-8")
Path("blob.bin").write_bytes(b"\x00\x01\x02")
```

For one-shot read/write of small files, this is cleaner than the `open` boilerplate.

## Iteration

```python
# Direct children
for child in Path(".").iterdir():
    print(child)

# Pattern match in a directory
for csv in Path("data").glob("*.csv"):
    process(csv)

# Recursive
for py in Path(".").rglob("*.py"):
    print(py)
```

## Common operations

```python
p = Path("data/raw/users.csv")

# Make sure parent directory exists
p.parent.mkdir(parents=True, exist_ok=True)

# Rename / move
p.rename(p.with_name("users_renamed.csv"))

# Delete
p.unlink()                        # for files
p.parent.rmdir()                  # for empty directories

# Change extension while keeping the rest
p.with_suffix(".parquet")         # Path('data/raw/users.parquet')

# Resolve symlinks and relative pieces to an absolute, real path
p.resolve()
```

## Working directories and `__file__`

```python
# Current working directory (where the user ran the script from)
Path.cwd()

# Where THIS .py file lives
here = Path(__file__).resolve().parent
data_dir = here / "data"          # relative to the script, not the CWD
```

Use `Path(__file__).parent` when your code needs files relative to itself (e.g. a config file shipped with your package). Use `Path.cwd()` when relative to where the user invoked the script.

## Avoid string-based path manipulation

Don't do:

```python
# BAD
path = base + "/" + filename
parent = path[:path.rfind("/")]
ext = path.split(".")[-1]
```

Do:

```python
# GOOD
path = Path(base) / filename
parent = path.parent
ext = path.suffix
```

You'll write fewer Windows-vs-Unix bugs.

## Read deeper

- Python docs: https://docs.python.org/3/library/pathlib.html
- The migration guide at the bottom of those docs shows `os.path` → `pathlib` equivalents.
