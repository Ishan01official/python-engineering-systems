# 01 — ETL: Extract, Transform, Load

The grandparent abstraction of all data engineering work. Modern variants (ELT, streaming, lakehouse) are all ETL with the steps in different orders.

## The three steps

1. **Extract** — get data out of a source (API, database, file drop, queue, log).
2. **Transform** — clean, validate, enrich, reshape it to fit downstream needs.
3. **Load** — write it to a destination (S3, warehouse, search index, downstream API).

A pipeline is the orchestration of these steps on a schedule (cron, EventBridge) or on a trigger (S3 PutObject, SNS message, Kafka topic).

## Design principles you'll come back to

### 1. Be idempotent

Running the same job twice should produce the same result. If your output path is `s3://bucket/data/dt=2026-06-29/run_id=abc/...`, re-running with `run_id=abc` overwrites cleanly. Without a run identifier, you might double-write.

Idempotency is what lets you retry on failure without fear. Build it in from day one.

### 2. Partition by time

Output paths usually look like:

```
s3://lake/raw/orders/dt=2026-06-29/hour=14/orders.parquet
s3://lake/raw/orders/dt=2026-06-29/hour=15/orders.parquet
```

Queries that only need yesterday's data scan one partition, not the whole bucket. The cost difference is enormous.

### 3. Separate raw, staged, and curated layers

```
raw/        ← what the upstream sent, untouched. Reread-safe.
staged/     ← parsed, validated, typed. Still per-batch.
curated/    ← deduped, joined, business-meaningful. Query-ready.
```

If a downstream is broken, you can replay `raw → staged → curated` without re-fetching from the source. Each layer is recoverable from the one before it.

### 4. Schema is contract

Define and version the schema for what you read and write. JSON Schema, Avro, Protobuf, or just a pydantic model — pick one and use it. Schema validation at the boundary catches bad inputs before they corrupt downstream data.

### 5. Log what you'd want at 3am

When the pipeline fails, you want to know: what file was being processed, when, by which version, with which inputs. See note 04 on logging.

## A minimal ETL function shape

```python
def run_etl(input_path: str, output_path: str, run_id: str) -> dict:
    # Extract
    records = read(input_path)

    # Transform (this is where most logic lives)
    cleaned = [c for c in (transform(r) for r in records) if c is not None]

    # Load
    write(output_path, cleaned, run_id=run_id)

    return {
        "input": input_path,
        "output": output_path,
        "run_id": run_id,
        "input_count": len(records),
        "output_count": len(cleaned),
        "dropped": len(records) - len(cleaned),
    }
```

The return value is the audit trail. Log it. Store it. Use it for monitoring.

## What makes a pipeline production-ready

| Stage | "Works on my laptop" | Production |
|---|---|---|
| Failure | crashes | retries, dead-letter queue |
| Logging | print | structured, indexed, with run_id |
| Replays | "re-run the script" | re-runnable from any starting point |
| Schema changes | breaks silently | validated, alerted, versioned |
| Tests | none | unit tests for transforms + integration for the wire-up |
| Cost | unmonitored | per-run resource accounting |

You don't need all of this on day one. You do need to recognize where you are on each axis.

## Read deeper

- **PfDA** 3e, Ch. 6 — data loading
- *The Data Engineering Cookbook* (free online) — practical patterns
- AWS Well-Architected: Data Analytics lens
