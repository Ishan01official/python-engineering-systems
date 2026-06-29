# 03 — CSV and JSON

Two structured formats you'll encounter constantly. The stdlib handles both.

## JSON

JSON maps cleanly to Python's built-in types:

| JSON | Python |
|---|---|
| object | `dict` |
| array | `list` |
| string | `str` |
| number | `int` or `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

### Read

```python
import json
from pathlib import Path

# From a file
data = json.loads(Path("config.json").read_text(encoding="utf-8"))

# Or directly streaming
import json
with open("config.json", encoding="utf-8") as f:
    data = json.load(f)        # note: `load`, not `loads`
```

`json.loads(s)` parses a **str**; `json.load(f)` parses from a **file**.

### Write

```python
text = json.dumps(data, indent=2, sort_keys=True)
Path("config.json").write_text(text, encoding="utf-8")

# Or streaming
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
```

`indent=2` gives you pretty-printed JSON. Drop it for the smallest possible output.

### What JSON can't handle

- `datetime` objects → convert to ISO strings before serializing.
- `set` → convert to `list` (sets don't exist in JSON).
- Custom objects → write a `default=` function or convert to a dict first.

```python
from datetime import datetime
def default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Can't serialize {type(obj)}")

json.dumps({"now": datetime.now()}, default=default)
```

## CSV

```python
import csv
from pathlib import Path

# Read as lists of strings (each row is a list)
with open("users.csv", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        print(row)

# Read as dicts (each row is {column: value}) — usually what you want
with open("users.csv", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["email"])
```

The `newline=""` parameter avoids double-newlines on Windows.

### Write

```python
rows = [
    {"name": "Alice", "age": 30},
    {"name": "Bob",   "age": 25},
]

with open("users.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows(rows)
```

### CSV gotchas

- **Everything is a string.** A column of `"42"` is the string `"42"`, not an integer. Convert explicitly when you read.
- **Quoting matters.** A value with a comma in it gets wrapped in quotes by the writer. The default `csv` quoting handles this; don't roll your own with `",".join(...)`.
- **For real data work, use pandas.** `pd.read_csv(path)` does type inference, missing-value handling, chunked reading, and a thousand other things the stdlib doesn't.

### When to use stdlib `csv` vs pandas

- Stdlib `csv`: tiny scripts, well-formed files, no dependency on pandas.
- pandas: anything bigger than a toy. Module 16 covers it.

## Other formats worth knowing

| Format | Library | When |
|---|---|---|
| TOML | `tomllib` (stdlib, 3.11+) for read; `tomli_w` for write | Config files (`pyproject.toml`) |
| YAML | `PyYAML` (third party) | Human-friendly config — but use TOML when you can |
| Parquet | `pyarrow` or pandas | Columnar storage, much faster + smaller than CSV |
| JSON Lines | json + line iteration | Streaming JSON, one record per line |

For data engineering specifically, **Parquet is the right default**. CSV is for sharing across teams/tools that don't know better.

## Read deeper

- **PfDA** 3e, Ch. 6 — data loading in pandas, including all of these formats.
- Python docs for `json` and `csv`.
