# Projects

Three increasingly substantial projects that apply the curriculum end-to-end. Each has a `README.md` with the spec, a starter scaffold, and a test suite.

## 1. [`01-cli-task-tracker/`](./01-cli-task-tracker/)

**Modules: 00–08.** A small command-line task manager. Practices arg parsing, file I/O, JSON, classes, exceptions, and testing.

Skills: CLI design, JSON persistence, OOP, pytest.

## 2. [`02-csv-to-dataframe-pipeline/`](./02-csv-to-dataframe-pipeline/)

**Modules: 06, 09, 12, 15, 16, 17.** Take a messy CSV, validate it, clean it, summarize per group, and write Parquet output.

Skills: pandas, data cleaning, generators, testing data code.

## 3. [`03-mini-etl-pipeline/`](./03-mini-etl-pipeline/)

**Modules: 06, 07, 11, 12, 20.** A miniature ETL framework: extract from a source (file or HTTP), transform with validation, load to a destination (file or S3-like). Designed so you can swap any of the three stages.

Skills: protocols, dependency injection, structured logging, testable pipelines.

---

## How to use these

1. Read the project README.
2. Try to design before peeking at the scaffold.
3. Implement; commit per logical step (`PROJECT(01): add storage layer` etc.).
4. Run the tests.
5. Extend with a feature of your own.
