"""
A pytest example. Run with:
    pip install pytest
    pytest 12-testing/examples/01_test_cart.py -v

Note: the filename intentionally starts with `01_test_` for pytest discovery.
"""
from dataclasses import dataclass, field

import pytest


# ---- code under test ------------------------------------------------------

@dataclass
class Item:
    name: str
    price: float
    quantity: int = 1


@dataclass
class Cart:
    items: list[Item] = field(default_factory=list)

    def add(self, item: Item) -> None:
        self.items.append(item)

    def subtotal(self) -> float:
        return sum(i.price * i.quantity for i in self.items)

    def total_with_discount(self, pct: float) -> float:
        if not 0 <= pct <= 1:
            raise ValueError("discount must be in [0, 1]")
        return self.subtotal() * (1 - pct)


# ---- fixtures -------------------------------------------------------------

@pytest.fixture
def sample_cart() -> Cart:
    return Cart([Item("a", 100, 1), Item("b", 50, 2)])     # subtotal = 200


# ---- tests ----------------------------------------------------------------

def test_empty_cart_subtotal_is_zero():
    assert Cart().subtotal() == 0


def test_subtotal_sums_quantities(sample_cart):
    assert sample_cart.subtotal() == 200


def test_discount_applies_percent(sample_cart):
    assert sample_cart.total_with_discount(0.1) == pytest.approx(180.0)


def test_zero_discount_equals_subtotal(sample_cart):
    assert sample_cart.total_with_discount(0) == sample_cart.subtotal()


def test_discount_outside_range_raises(sample_cart):
    with pytest.raises(ValueError, match="discount"):
        sample_cart.total_with_discount(1.5)


@pytest.mark.parametrize(
    "items, pct, expected",
    [
        ([Item("a", 100)], 0.0, 100.0),
        ([Item("a", 100)], 0.25, 75.0),
        ([Item("a", 100), Item("b", 50)], 0.1, 135.0),
        ([], 0.5, 0.0),
    ],
)
def test_total_with_discount_table(items, pct, expected):
    cart = Cart(items)
    assert cart.total_with_discount(pct) == pytest.approx(expected)
