# 03 — S3 pipelines: partitioning, idempotency, schema

S3 is the default data lake substrate at most companies on AWS. Used well, it's effectively infinite storage with cheap reads; used poorly, it's a swamp of duplicated, inscrutable files.

## Partition by time, source, and tenant

A good key naming convention:

```
s3://<bucket>/<layer>/source=<src>/<tenant=...>/dt=YYYY-MM-DD/hour=HH/<file>
```

Concrete:

```
s3://aarkax-lake/raw/source=supplier_terms/dt=2026-06-29/hour=14/sns-abcdef.json
s3://aarkax-lake/staged/source=supplier_terms/dt=2026-06-29/supplier_terms.parquet
s3://aarkax-lake/curated/source=supplier_terms/dt=2026-06-29/supplier_terms.parquet
```

Why this works:

- **Query engines (Athena, Spark, DuckDB) prune partitions.** A query for `dt=2026-06-29` reads only that directory.
- **Backfills are scoped.** Re-run a single day without touching others.
- **Cost transparency.** You can see how much each source/tenant/day consumes.

## Pick the right file format

| Format | When |
|---|---|
| CSV | only for human handoff or legacy interop |
| JSON / JSON Lines | logs, semi-structured data, when schema isn't fixed |
| Parquet | tabular data — columnar, compressed, typed. Default for analytics. |
| Avro | streaming-heavy use (Kafka ecosystem) with schema evolution |

For data engineering on AWS, **Parquet is the default**. CSV is for the boundary with other teams or systems.

## Idempotent writes

A naive write — `s3.put_object(Bucket=b, Key=k, Body=data)` — is already idempotent at the object level (same key overwrites). The trap is when *the key depends on time of execution*:

```python
# BAD — re-running creates duplicates with different timestamps
key = f"raw/{source}/{datetime.now().isoformat()}.json"

# GOOD — re-running overwrites the same key
key = f"raw/{source}/dt={event_date}/{message_id}.json"
```

Anchor your key on attributes of the *input* (event ID, content hash, source timestamp), not the *run* (now()).

## Reading files: streaming vs in-memory

```python
obj = s3.get_object(Bucket=b, Key=k)

# Small file — fine
data = obj["Body"].read()

# Large file — stream
for line in obj["Body"].iter_lines():
    process(line)

# Pandas reads directly from S3 with the right extras
import pandas as pd
df = pd.read_parquet(f"s3://{b}/{k}")            # needs `s3fs`
```

For Lambda, prefer streaming. Memory in a Lambda is finite and you pay for it.

## Schema evolution

Production pipelines run for years. Schemas change. Three strategies:

1. **Versioned schemas.** Each record carries a `schema_version`. Code branches accordingly. Simple, works forever.
2. **Backward-compatible additions.** New fields are optional with defaults. Old code ignores them, new code uses them.
3. **Schema registry.** A service (AWS Glue Schema Registry, Confluent) holds canonical schemas; producers and consumers fetch and validate against it.

For internal data, (1) or (2) is enough. (3) earns its complexity at company scale with many producers and consumers.

## Compaction

A pipeline that writes one Parquet per Lambda invocation produces many tiny files. Query engines hate this — overhead per file dominates.

The fix is a **compaction** job: nightly (or hourly), read all the small files for a partition, write them out as one larger file (target: 100 MB - 1 GB per file). Delete the small files. This is the standard "many small files → few big files" maintenance step.

## Lifecycle policies — pay attention to cost

S3 has tiers: Standard → Standard-IA → Glacier → Glacier Deep Archive. Set lifecycle rules so old raw data moves to cheaper tiers automatically:

```
30 days: Standard → Standard-IA
180 days: → Glacier
1 year: → Glacier Deep Archive  (or delete)
```

For raw data you keep "just in case", lifecycle policies are the difference between a $200/month bill and a $20,000/month bill.

## Read deeper

- AWS Athena / EMR / Glue docs on partitioning
- Parquet docs
- *Designing Data-Intensive Applications* (Kleppmann), Ch. 4 — encoding & evolution
