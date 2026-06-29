"""End-to-end pipeline tests with in-memory stages."""
from pathlib import Path

import pytest

from etl import Pipeline
from etl.extractors import InMemoryExtractor, JSONLinesExtractor
from etl.loaders import InMemoryLoader, JSONLinesLoader
from etl.transformers import AddTimestamp, CoerceTypes, RequiredFields


def test_pipeline_with_all_clean_data():
    src = InMemoryExtractor([
        {"id": "1", "value": "10"},
        {"id": "2", "value": "20"},
    ])
    sink = InMemoryLoader()
    p = Pipeline(
        extractor=src,
        transformers=[
            RequiredFields("id", "value"),
            CoerceTypes(id=int, value=float),
        ],
        loader=sink,
    )
    result = p.run()

    assert result.extracted == 2
    assert result.transformed == 2
    assert result.dropped == 0
    assert result.loaded == 2
    assert sink.loaded == [
        {"id": 1, "value": 10.0},
        {"id": 2, "value": 20.0},
    ]


def test_pipeline_drops_missing_required():
    src = InMemoryExtractor([
        {"id": "1", "value": "10"},
        {"id": "2"},                  # missing value
        {"value": "30"},              # missing id
    ])
    sink = InMemoryLoader()
    p = Pipeline(src, [RequiredFields("id", "value")], sink)
    result = p.run()
    assert result.extracted == 3
    assert result.transformed == 1
    assert result.dropped == 2


def test_pipeline_drops_records_that_fail_coercion():
    src = InMemoryExtractor([
        {"id": "1", "value": "10"},
        {"id": "2", "value": "not a number"},
    ])
    sink = InMemoryLoader()
    p = Pipeline(src, [CoerceTypes(value=float)], sink)
    result = p.run()
    assert result.transformed == 1
    assert result.dropped == 1


def test_addtimestamp_uses_injected_clock():
    src = InMemoryExtractor([{"id": 1}])
    sink = InMemoryLoader()
    pinned = AddTimestamp(clock=lambda: 1_700_000_000.0)
    Pipeline(src, [pinned], sink).run()
    assert sink.loaded[0]["enriched_at"] == 1_700_000_000


def test_full_disk_roundtrip(tmp_path: Path):
    raw = tmp_path / "in.jsonl"
    raw.write_text(
        '{"id":"1","value":"10"}\n'
        '{"id":"2","value":"20"}\n'
        '{"id":"3"}\n',                      # bad — will be dropped
        encoding="utf-8",
    )
    out = tmp_path / "out.jsonl"

    p = Pipeline(
        extractor=JSONLinesExtractor(raw),
        transformers=[
            RequiredFields("id", "value"),
            CoerceTypes(id=int, value=float),
        ],
        loader=JSONLinesLoader(out),
    )
    result = p.run()
    assert result.loaded == 2
    assert out.exists()
    lines = [line for line in out.read_text(encoding="utf-8").splitlines() if line]
    assert len(lines) == 2
