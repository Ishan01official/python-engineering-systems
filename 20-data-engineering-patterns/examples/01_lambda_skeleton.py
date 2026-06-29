"""
A realistic SNS-triggered Lambda handler — runnable locally with a mock event.

This mirrors the shape of supplier_terms_enriched.py-style functions Ishan works on.

Run:
    python 20-data-engineering-patterns/examples/01_lambda_skeleton.py
"""
import json
import logging
import os
import time
from typing import Any
from urllib.parse import unquote_plus


# ---- module-level setup: runs ONCE per cold start ------------------------

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Quiet noisy AWS SDK loggers (the lesson from CloudWatch tuning)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


# ---- parsing -------------------------------------------------------------

def parse_sns_event(event: dict) -> list[dict]:
    """Pull JSON payloads out of an SNS-wrapped event."""
    records = []
    for record in event.get("Records", []):
        if record.get("EventSource") != "aws:sns":
            logger.warning("non-sns record", extra={"source": record.get("EventSource")})
            continue
        msg = record["Sns"]["Message"]
        try:
            payload = json.loads(msg)
        except json.JSONDecodeError:
            logger.exception("bad sns payload", extra={"message_id": record["Sns"]["MessageId"]})
            raise
        records.append({
            "message_id": record["Sns"]["MessageId"],
            "timestamp": record["Sns"]["Timestamp"],
            "payload": payload,
        })
    return records


# ---- the actual transform ------------------------------------------------

def enrich_supplier_terms(payload: dict) -> dict | None:
    """Pure function — easy to unit test. Returns None if record should be dropped."""
    if not payload.get("supplier_id") or not payload.get("terms"):
        return None
    return {
        "supplier_id": payload["supplier_id"],
        "terms": payload["terms"],
        "currency": payload.get("currency", "INR"),
        "enriched_at": int(time.time()),
        # ... enrichment logic goes here
    }


def output_key(payload: dict, message_id: str) -> str:
    """
    Idempotent S3 key: anchored on the event, not on now().
    Re-runs overwrite the same key.
    """
    event_date = payload.get("event_date", "unknown")
    supplier_id = payload.get("supplier_id", "unknown")
    return f"raw/source=supplier_terms/dt={event_date}/supplier={supplier_id}/{message_id}.json"


# ---- handler --------------------------------------------------------------

def lambda_handler(event: dict, context: Any) -> dict:
    start = time.time()
    request_id = getattr(context, "aws_request_id", "local")

    logger.info("start", extra={
        "request_id": request_id,
        "n_records_in_event": len(event.get("Records", [])),
    })

    records = parse_sns_event(event)

    written = 0
    dropped = 0
    for record in records:
        enriched = enrich_supplier_terms(record["payload"])
        if enriched is None:
            dropped += 1
            logger.warning("dropped", extra={
                "request_id": request_id,
                "message_id": record["message_id"],
                "reason": "missing required fields",
            })
            continue

        key = output_key(record["payload"], record["message_id"])

        # In real Lambda this would be: s3.put_object(Bucket=..., Key=key, Body=...)
        # For the local example, just log it.
        logger.info("would_write", extra={
            "request_id": request_id,
            "message_id": record["message_id"],
            "key": key,
            "bytes": len(json.dumps(enriched)),
        })
        written += 1

    logger.info("done", extra={
        "request_id": request_id,
        "written": written,
        "dropped": dropped,
        "duration_ms": int((time.time() - start) * 1000),
    })

    return {"written": written, "dropped": dropped}


# ---- local test harness ---------------------------------------------------

def _mock_sns_event(payloads: list[dict]) -> dict:
    """Build an event shaped like SNS would deliver."""
    return {
        "Records": [
            {
                "EventSource": "aws:sns",
                "Sns": {
                    "MessageId": f"mock-{i}",
                    "Timestamp": "2026-06-29T14:30:00.000Z",
                    "Message": json.dumps(p),
                },
            }
            for i, p in enumerate(payloads)
        ]
    }


class _MockContext:
    aws_request_id = "local-test-001"
    function_version = "$LATEST"


if __name__ == "__main__":
    event = _mock_sns_event([
        {"supplier_id": "S001", "terms": "net 30", "event_date": "2026-06-29"},
        {"supplier_id": "S002", "terms": "net 45", "currency": "USD", "event_date": "2026-06-29"},
        {"supplier_id": "S003"},  # missing terms — should be dropped
    ])
    result = lambda_handler(event, _MockContext())
    print(f"\nResult: {result}")
