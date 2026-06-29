# 02 — AWS Lambda patterns

A Lambda function is a Python function that AWS runs in response to events. The model is simple, the production patterns are not. This note covers the patterns that come up in real S3/SNS-triggered pipelines (the shape of work Ishan does at Aarkax).

## The shape

Every Lambda has a `handler(event, context)`:

```python
def lambda_handler(event, context):
    ...
    return {"statusCode": 200}
```

`event` is whatever the trigger sent — different shape per source (S3 notification vs SNS message vs API Gateway request).

## Anatomy of a robust handler

```python
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # 1. Log the event with enough metadata to debug
    logger.info("invocation", extra={
        "request_id": context.aws_request_id,
        "function_version": context.function_version,
        "remaining_ms": context.get_remaining_time_in_millis(),
    })

    # 2. Parse the event — be defensive at the boundary
    try:
        records = parse_event(event)
    except (KeyError, json.JSONDecodeError) as e:
        logger.exception("malformed event")
        raise

    # 3. Do the actual work, per record
    results = []
    for record in records:
        try:
            result = process_record(record)
            results.append(result)
        except Exception as e:
            # Decide: fail fast (re-raise) vs continue (collect failures)
            logger.exception("failed record", extra={"record_id": record.get("id")})
            # for at-least-once delivery, raise so the source retries
            raise

    return {"processed": len(results)}
```

The defensive-at-the-boundary, fail-fast-internally pattern is the right default.

## SNS-triggered Lambda

An SNS message arrives as:

```python
{
    "Records": [
        {
            "EventSource": "aws:sns",
            "Sns": {
                "Message": "<the actual payload, often JSON-encoded>",
                "MessageId": "...",
                "Timestamp": "2026-06-29T14:30:00.000Z",
            },
        },
    ],
}
```

Parse it carefully:

```python
def parse_event(event):
    out = []
    for record in event["Records"]:
        msg = record["Sns"]["Message"]
        out.append(json.loads(msg))            # often the payload is JSON-in-string
    return out
```

## S3-triggered Lambda

An S3 PutObject event arrives as:

```python
{
    "Records": [
        {
            "eventSource": "aws:s3",
            "eventName": "ObjectCreated:Put",
            "s3": {
                "bucket": {"name": "..."},
                "object": {"key": "<URL-encoded key>"},
            },
        },
    ],
}
```

Watch out: the key is **URL-encoded**. `path%2Fto%2Ffile.csv` should be decoded with `urllib.parse.unquote_plus(key)` before use.

## Configuration via environment variables

```python
import os

BUCKET = os.environ["OUTPUT_BUCKET"]            # fail at cold start if missing
PREFIX = os.environ.get("OUTPUT_PREFIX", "raw")   # safe default
```

Don't hardcode bucket names, table names, or arns. Lambdas of the same code go to multiple environments (dev/staging/prod); env vars are how you parameterize them.

## Cold start mitigation

Module-level code runs once per "cold start" (new container). Use it for expensive setup:

```python
import boto3

s3 = boto3.client("s3")        # reused across invocations on the same container

def lambda_handler(event, context):
    s3.get_object(Bucket=..., Key=...)        # fast — connection pool warmed
```

Don't create the client inside the handler — you'd pay setup cost every invocation.

## Idempotency

Lambdas can be invoked twice for the same event (especially with SNS/SQS sources). Make your handler idempotent: writing to a deterministic output key (e.g., based on input filename + content hash) overwrites cleanly on retry. Don't append to a shared sink.

## Common pitfalls

- **Timeouts.** Default 3 seconds. For S3 reads of large files or DB queries, raise it deliberately. But also: long-running work should usually be split, not just given more time.
- **Memory.** Configured in MB, but CPU scales with memory. A 128 MB Lambda gets a fraction of a vCPU; a 1769 MB Lambda gets 1 full vCPU. If your job is CPU-bound, raise memory.
- **Concurrency limits.** Default 1000 per account, per region. A burst of S3 events can throttle. Configure reserved/provisioned concurrency for critical paths.
- **Reading huge S3 objects.** Stream with `body = obj["Body"].iter_lines()` rather than `obj["Body"].read()` for files that don't fit in memory.

## A pattern: SNS → Lambda → partitioned S3 write

```python
def lambda_handler(event, context):
    for record in event["Records"]:
        payload = json.loads(record["Sns"]["Message"])
        rows = transform(payload)

        # Partition by event date — typical pattern
        dt = payload["event_date"]            # "2026-06-29"
        key = f"raw/topic={payload['topic']}/dt={dt}/{record['Sns']['MessageId']}.json"
        s3.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=json.dumps(rows).encode(),
        )
    return {"ok": True}
```

The MessageId in the key gives idempotency: same SNS message → same key → safe to overwrite.

## Read deeper

- AWS Lambda Operator Guide
- AWS docs: S3, SNS, Lambda integrations
- *Serverless Architectures on AWS* (Manning) for deeper patterns
