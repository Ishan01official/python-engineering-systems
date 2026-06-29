# Module 12 — Exercises

## E12.1 — First pytest tests

Take the `Stack` class from E08.1. Write a pytest file with at least 5 tests covering: empty behaviour, push/pop, peek, `len`, `bool`, and "popping an empty stack raises". Run `pytest -v` and make them all green.

## E12.2 — Parametrize

A function `slugify(s)` takes a string and returns a URL slug: lowercase, spaces→hyphens, drop punctuation, collapse multiple hyphens. Write one parametrized test covering 6+ cases including edge cases (empty, all-punctuation, mixed Unicode).

## E12.3 — Test exceptions

Write tests for `Account.withdraw` from Module 08. Cover: normal withdrawal, withdrawal of exactly the balance, withdrawal of more than the balance (should raise `ValueError`), withdrawal of a negative amount.

## E12.4 — Fixture for setup/teardown

Write a fixture that creates a temp file, writes test data to it, yields the path, and deletes the file after each test. Use it in two tests that load and parse the file.

## E12.5 — Spot a bad test

What's wrong with each? Rewrite:
```python
def test_user():
    u = User("Alice")
    u.add_friend("Bob")
    u.remove_friend("Bob")
    u.set_active(False)
    assert u.name == "Alice"
    assert not u.is_active()
    assert u.friends == []
```
```python
def test_send_calls_internal_method():
    notifier = Notifier()
    notifier._format = Mock()
    notifier.send("hi")
    notifier._format.assert_called_once()
```

## E12.6 — Coverage

Install `pytest-cov`. Run `pytest --cov=12-testing/examples/01_test_cart`. What lines are uncovered? Add tests until coverage is 100%. Reflect: did the new tests catch any real bug, or just paint lines green?
