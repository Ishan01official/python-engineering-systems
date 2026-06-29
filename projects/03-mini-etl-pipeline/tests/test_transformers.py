"""Unit tests for individual transformers."""
import pytest

from etl.transformers import AddTimestamp, CoerceTypes, RequiredFields


class TestRequiredFields:
    def test_passes_complete_record(self):
        t = RequiredFields("id", "name")
        assert t.transform({"id": 1, "name": "Alice"}) == {"id": 1, "name": "Alice"}

    def test_drops_missing_field(self):
        t = RequiredFields("id", "name")
        assert t.transform({"id": 1}) is None

    def test_drops_none_value(self):
        t = RequiredFields("id")
        assert t.transform({"id": None}) is None

    def test_drops_empty_string(self):
        t = RequiredFields("id")
        assert t.transform({"id": ""}) is None


class TestCoerceTypes:
    def test_coerces_known_fields(self):
        t = CoerceTypes(age=int, price=float)
        assert t.transform({"age": "30", "price": "9.99", "name": "X"}) == {
            "age": 30, "price": 9.99, "name": "X",
        }

    def test_returns_none_on_bad_value(self):
        t = CoerceTypes(age=int)
        assert t.transform({"age": "not a number"}) is None

    def test_ignores_missing_fields(self):
        t = CoerceTypes(age=int)
        # field 'age' is absent — that's fine, we leave it alone
        assert t.transform({"name": "Alice"}) == {"name": "Alice"}


class TestAddTimestamp:
    def test_adds_field(self):
        t = AddTimestamp(clock=lambda: 1234567890.5)
        out = t.transform({"id": 1})
        assert out["enriched_at"] == 1234567890

    def test_doesnt_mutate_input(self):
        original = {"id": 1}
        AddTimestamp(clock=lambda: 1.0).transform(original)
        assert "enriched_at" not in original
