# 20 — Data engineering patterns

The patterns that make data pipelines correct, observable, and rerunnable. This module is closest to day-job Python for someone who works on AWS Lambda + S3 pipelines (the kind of work Ishan does at Aarkax).

## Notes

1. [`01-etl-basics.md`](./01-etl-basics.md) — Extract, Transform, Load — the mental frame
2. [`02-lambda-patterns.md`](./02-lambda-patterns.md) — AWS Lambda function structure, SNS/S3 triggers
3. [`03-s3-pipelines.md`](./03-s3-pipelines.md) — partitioned paths, idempotency, schema evolution
4. [`04-logging-and-observability.md`](./04-logging-and-observability.md) — CloudWatch, structured logs, what to log

## Diagrams

- [`diagrams/etl-flow.mmd`](./diagrams/etl-flow.mmd) — typical SNS → Lambda → S3 partitioned write

## Read deeper

- **PfDA** 3e, Ch. 6 (loading), Ch. 12–13 (advanced data wrangling, modeling)
- AWS docs: Lambda best practices, S3 storage patterns
