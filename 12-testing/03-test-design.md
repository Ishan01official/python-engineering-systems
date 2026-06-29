# 03 — Test design — what to test, what not to

Tests are code. They have costs (writing, maintaining, running). Bad tests are worse than no tests — they pin you to your current implementation and break on every refactor.

## What to test

- **Business logic and pure functions.** This is where bugs hide and tests pay off most.
- **Boundary conditions.** Empty inputs, single-element inputs, max-size, off-by-one.
- **Error paths.** What if the file is missing? What if the API returns 500?
- **Bugs you've fixed.** Add a test before fixing, then again after, so a regression is caught.

## What NOT to test

- **Code you don't own** (the stdlib, third-party libraries). They have their own tests.
- **Trivial getters/setters and dataclasses.** Testing `p.name == "x"` after `Person("x")` adds nothing.
- **Implementation details.** "Did it call method `_compute_total` 3 times?" → fragile. Test behavior, not how.
- **Random / time-dependent values.** Inject a fixed seed or a frozen clock instead.

## The shape of a good test

Three parts: **Arrange, Act, Assert** (AAA):

```python
def test_apply_discount():
    # Arrange
    cart = Cart([Item("a", 100), Item("b", 50)])
    # Act
    total = cart.total_with_discount(0.1)
    # Assert
    assert total == 135.0
```

Each test should:

1. Read top-to-bottom in seconds.
2. Test **one** thing. Multiple asserts are fine if they verify the same idea; multiple unrelated checks → split into multiple tests.
3. Have a name that says what it tests: `test_total_with_discount_applies_percent` beats `test_cart_works`.

## Test independence

Tests must not depend on each other. They should be runnable in any order. The order pytest runs in is configurable; relying on order is a bug.

If tests share setup, use fixtures. If they share data, make sure each gets a fresh copy.

## Mocks and fakes — used sparingly

A mock replaces a real dependency. Useful when the real thing is slow, expensive, or external (network, database, filesystem).

```python
from unittest.mock import Mock

def test_sends_alert():
    notifier = Mock()
    process(notifier)
    notifier.send.assert_called_once_with("alert")
```

**Don't over-mock.** A test that mocks every internal call is testing the structure of your code, not its behavior. If you find yourself mocking a lot, your code might be too coupled — refactor to push side effects to the edges, and test the pure middle directly.

## A useful default project setup

```
my-project/
├── src/mypackage/...
├── tests/
│   ├── conftest.py        # shared fixtures
│   ├── test_unit/         # fast, pure unit tests
│   └── test_integration/  # slower, may hit DB or filesystem
└── pyproject.toml
```

Mark slow tests so you can run them selectively:

```python
@pytest.mark.slow
def test_huge_dataset(): ...
```

Then `pytest -m "not slow"` for fast feedback, `pytest -m slow` before pushing.

## TDD — Test Driven Development (brief)

Write a failing test, then write the smallest code that passes it, then refactor. Loop.

Worth trying. Not worth being religious about. Many great Python codebases were not written test-first.

## Read deeper

- **PCC** 3e, Ch. 11 — accessible intro
- **EP** 3e — testing items
- "Test Driven Development by Example" (Kent Beck) — short, classic
