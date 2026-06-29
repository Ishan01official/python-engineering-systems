# 01 — Reading and writing files

## The `open` function

```python
f = open("data.txt", "r", encoding="utf-8")
contents = f.read()
f.close()
```

That works but leaks the handle if anything between `open` and `close` raises. **Always use `with`**:

```python
with open("data.txt", "r", encoding="utf-8") as f:
    contents = f.read()
# file is automatically closed here, even on exception
```

The `with` block is a context manager — Module 06.04 explains the mechanics. For now, internalize: **every `open()` should be inside a `with` block.**

## Modes

| Mode | Meaning |
|---|---|
| `"r"` | Read text (default) |
| `"w"` | Write text — truncates existing file! |
| `"a"` | Append text |
| `"x"` | Create new — fails if exists |
| `"rb"`, `"wb"` | Binary read/write |
| `"r+"` | Read and write |

Always pass `encoding="utf-8"` for text. The default depends on your OS, which is a recipe for bugs that only appear on someone else's machine.

For binary files (images, compressed files, anything not text), use `"rb"` / `"wb"` and you get `bytes` back, not `str`.

## Three ways to read text

```python
# 1. All at once — fine for small files
with open(path, encoding="utf-8") as f:
    text = f.read()

# 2. All lines as a list — also reads everything into memory
with open(path, encoding="utf-8") as f:
    lines = f.readlines()

# 3. Line by line — memory-efficient, works for huge files
with open(path, encoding="utf-8") as f:
    for line in f:               # the file object IS the iterator
        process(line.rstrip("\n"))
```

Use #3 by default. It scales to any file size because only one line is in memory at a time.

## Writing

```python
with open(path, "w", encoding="utf-8") as f:
    f.write("hello\n")
    f.write("world\n")

# Or with multiple lines:
with open(path, "w", encoding="utf-8") as f:
    f.writelines([f"line {i}\n" for i in range(5)])
```

`write` doesn't add a newline; you do. `print(..., file=f)` does add one, which can be more convenient:

```python
with open(path, "w") as f:
    for record in records:
        print(format_line(record), file=f)
```

## Common patterns

### Process a big file streaming

```python
total = 0
with open("huge.log", encoding="utf-8") as f:
    for line in f:
        if "ERROR" in line:
            total += 1
print(f"{total} error lines")
```

Never `f.read()` a file you can't fit in memory. Stream it.

### Read JSON

```python
import json
with open("config.json", encoding="utf-8") as f:
    config = json.load(f)         # parses directly from the file
```

### Write JSON

```python
with open("out.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
```

## Newlines and encoding gotchas

- **Newlines** differ across platforms (`\n` on Unix/macOS, `\r\n` on Windows). Python's `open` translates them transparently in text mode. In binary mode (`"rb"`), bytes are bytes — you see them raw.
- **UTF-8 BOM** sometimes precedes Windows-saved files. Open with `encoding="utf-8-sig"` to skip it.
- **Encoding errors** (`UnicodeDecodeError`) on read = wrong encoding. The fix is to *find out* which encoding the file actually uses, not to slap `errors="ignore"` on it (that silently drops data).

## Read deeper

- **LP** 6e, Ch. 9 — files in full detail.
- **PfDA** 3e, Ch. 6 — text and binary I/O for data work.
