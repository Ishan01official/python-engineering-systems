# 04 — Logging and observability

When a Lambda fails at 3am, your logs are everything. Get this right early — retrofitting logging to a working pipeline is painful.

## Use `logging`, never `print`

In a Lambda, `print` writes to CloudWatch. So does `logger.info`. The difference is structure:

- `print(f"processed {n} rows")` → free text, hard to query
- `logger.info("processed", extra={"row_count": n, "source": source})` → structured

CloudWatch Logs Insights can filter and aggregate on the structured fields. Free text needs regex parsing.

## A standard logger setup for Lambda

```python
import json
import logging
import sys


class JsonFormatter(logging.Formatter):
    def format(self, record):
        base = {
            "ts": self.formatTime(record),
            "level": record.levelname,
            "msg": record.getMessage(),
            "logger": record.name,
        }
        # Attach any extra= fields
        for k, v in record.__dict__.items():
            if k not in {
                "name", "msg", "args", "levelname", "levelno", "pathname",
                "filename", "module", "exc_info", "exc_text", "stack_info",
                "lineno", "funcName", "created", "msecs", "relativeCreated",
                "thread", "threadName", "processName", "process",
                "taskName", "message",
            }:
                base[k] = v
        return json.dumps(base, default=str)


logger = logging.getLogger()
logger.setLevel(logging.INFO)
# In Lambda, the default handler is already attached. Just replace its formatter.
for h in logger.handlers:
    h.setFormatter(JsonFormatter())
```

Now every log line is JSON. CloudWatch Insights can do `fields @timestamp, row_count, source | filter level = "ERROR"` and it just works.

## What to log

For every Lambda invocation, log at least:

```python
logger.info("start", extra={
    "request_id": context.aws_request_id,
    "function_version": context.function_version,
    "source": event_source(event),
    "input_key": input_key,
})

# ... do work ...

logger.info("done", extra={
    "request_id": context.aws_request_id,
    "input_rows": n_in,
    "output_rows": n_out,
    "dropped_rows": n_in - n_out,
    "output_key": output_key,
    "duration_ms": int((time.time() - start) * 1000),
})
```

The "shape" of the invocation in one event: how much came in, how much went out, where. This is the bread and butter of "what happened?" debugging.

## Surface the important things; suppress the rest

The default verbosity of AWS SDKs (boto3, botocore) is **noisy**. Quiet them:

```python
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
```

This is the lesson from your recent CloudWatch log-verbosity tuning: keep the signal (filename, S3 event time, Lambda execution time, the structured fields you care about); kill the noise. Full SNS record dumps are great for debugging, but only at DEBUG level — not flooding INFO.

## Log levels — use them properly

| Level | When |
|---|---|
| DEBUG | full dumps of inputs, intermediate values. Off in prod. |
| INFO | one or two lines per invocation summarizing the work. |
| WARNING | a record was dropped, a fallback was used, something to look at later. |
| ERROR | something failed; the invocation may have raised. |
| CRITICAL | the system is in a bad state. Rare. |

Don't log every row at INFO. Log totals.

## Correlation IDs

Every log line for a single invocation should share a `request_id` (or `trace_id`). Then a query for `request_id = X` shows you the full story of that invocation across services. Lambda gives you `context.aws_request_id` for free; thread it through to downstream calls.

## Metrics, not just logs

For numbers you'll want to chart (counts, latencies, error rates), use CloudWatch Custom Metrics or EMF (Embedded Metric Format):

```python
import json
print(json.dumps({
    "_aws": {
        "Timestamp": int(time.time() * 1000),
        "CloudWatchMetrics": [{
            "Namespace": "Aarkax/Pipeline",
            "Dimensions": [["source"]],
            "Metrics": [{"Name": "rows_processed", "Unit": "Count"}],
        }],
    },
    "source": "supplier_terms",
    "rows_processed": 1234,
}))
```

CloudWatch picks this up automatically and turns it into a metric you can graph and alarm on.

## Read deeper

- AWS CloudWatch Logs Insights query syntax
- AWS Embedded Metric Format (EMF) docs
- Python `logging` docs
