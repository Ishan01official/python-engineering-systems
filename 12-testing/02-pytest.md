# 02 — pytest

The de facto standard for testing in Python. Install: `pip install pytest`.

## A pytest file

```python
# test_add.py
from mymodule import add

def test_positive():
    assert add(2, 3) == 5

def test_negative():
    assert add(-1, -1) == -2

def test_zero():
    assert add(0, 5) == 5
```

Run:

```
pytest                       # discovers and runs all tests in CWD
pytest test_add.py           # one file
pytest test_add.py::test_zero   # one test
pytest -v                    # verbose
pytest -k "positive"          # only tests with 'positive' in the name
pytest -x                    # stop at first failure
pytest --lf                   # rerun only last-failed
```

Key advantages over unittest:

- Plain `assert` statements. pytest rewrites them so failure messages are detailed:
  ```
  assert add(2, 3) == 6
  AssertionError: assert 5 == 6
  ```
- No class boilerplate (though you can use classes if you want).
- Fixtures (next section) replace setUp/tearDown more flexibly.
- Huge plugin ecosystem (`pytest-cov`, `pytest-xdist`, `pytest-mock`, ...).

## Fixtures

A fixture is a reusable setup, declared with `@pytest.fixture`:

```python
import pytest

@pytest.fixture
def sample_users():
    return [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]

def test_count(sample_users):
    assert len(sample_users) == 2

def test_first_name(sample_users):
    assert sample_users[0]["name"] == "A"
```

Tests **declare** which fixtures they need by accepting them as parameters. pytest looks up matching fixture names and injects them.

Fixtures can also do teardown:

```python
@pytest.fixture
def temp_db():
    db = create_test_db()
    yield db                  # the test runs here
    db.close()                # cleanup after
```

## Parametrize — many cases, one test

```python
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

pytest runs this test three times, once per row. The names in the test report show the inputs, so failures point at the exact case.

## Testing exceptions

```python
import pytest

def test_raises_on_zero():
    with pytest.raises(ValueError, match="divide"):
        divide(10, 0)
```

`match` is a regex on the exception message — gives you a meaningful check beyond just "an exception happened".

## Coverage

Install `pytest-cov`, then:

```
pytest --cov=mymodule
pytest --cov=mymodule --cov-report=html
```

The HTML report shows which lines are uncovered. Aim for high coverage of the logic, but don't chase 100% — covered ≠ correct.

## Layout

The standard layout that pytest discovers without configuration:

```
my-project/
├── src/
│   └── mypackage/
│       └── __init__.py
├── tests/
│   ├── test_thing.py
│   └── test_other.py
└── pyproject.toml
```

Test files start with `test_`, functions start with `test_`. Add a `conftest.py` in `tests/` for shared fixtures.

## Read deeper

- pytest docs: https://docs.pytest.org
- **EP** 3e — items on test design and pytest
