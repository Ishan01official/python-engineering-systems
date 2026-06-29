"""A tiny ETL framework — swap any of the three stages."""
from .pipeline import Pipeline, RunResult
from .protocols import Extractor, Loader, Record, Transformer

__all__ = ["Pipeline", "RunResult", "Extractor", "Loader", "Transformer", "Record"]
