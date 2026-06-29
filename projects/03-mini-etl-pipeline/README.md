# Project 3 — Mini ETL pipeline

A small framework that lets you build an Extract → Transform → Load pipeline by swapping any of the three stages. Consolidates modules 06 (I/O), 07 (errors), 11 (typing/protocols), 12 (testing), and 20 (data engineering patterns).

## Goals

- Express each stage as a Protocol — anyone can implement an Extractor, Transformer, or Loader.
- Wire stages together with no hardcoded references.
- Validate input at the boundary; let the pipeline assume clean data internally.
- Log a structured manifest of every run.

## Architecture

```
                   ┌────────────────────────────────┐
                   │           Pipeline             │
                   │   wires the three stages       │
                   └────────────────────────────────┘
                          │           │           │
                   ┌──────┘   ┌───────┘   ┌───────┘
                   ▼          ▼           ▼
           ┌──────────┐  ┌──────────┐  ┌──────────┐
           │ Extractor│  │Transform │  │  Loader  │
           │ Protocol │  │ Protocol │  │ Protocol │
           └──────────┘  └──────────┘  └──────────┘
                ▲              ▲              ▲
                │              │              │
        FileExtractor  RecordValidator  ParquetLoader
        HTTPExtractor  RecordEnricher   S3JSONLoader (mock)
        ...            ...              ...
```

## Files

```
03-mini-etl-pipeline/
├── README.md
├── etl/
│   ├── __init__.py
│   ├── protocols.py        # Extractor / Transformer / Loader Protocols
│   ├── pipeline.py         # the Pipeline orchestrator
│   ├── extractors.py       # FileExtractor
│   ├── transformers.py     # validate + enrich
│   └── loaders.py          # FileLoader (writes JSON Lines)
├── tests/
│   ├── test_pipeline.py
│   └── test_transformers.py
└── pyproject.toml
```

## Stretch goals

- Add `HTTPExtractor` (`urllib.request`).
- Add `S3Loader` using `boto3` or a `moto`-mocked S3.
- Add a `--config config.yaml` mode that wires stages from config.
- Add a manifest file (`run_<timestamp>.json`) with row counts, durations, errors.
