# 01 — `unittest`

The standard library's testing framework. You'll see it in older code. For new projects, use pytest. But it's good to recognize.

## A typical unittest file

```python
import unittest

def add(a, b):
    return a + b


class TestAdd(unittest.TestCase):

    def test_positive(self):
        self.assertEqual(add(2, 3), 5)

    def test_negative(self):
        self.assertEqual(add(-1, -1), -2)

    def test_zero(self):
        self.assertEqual(add(0, 5), 5)


if __name__ == "__main__":
    unittest.main()
```

Run it:

```
python test_add.py
```

## Why it's verbose

- You write a class per related group of tests.
- Each test is a method starting with `test_`.
- You use `self.assertEqual`, `self.assertTrue`, `self.assertRaises`, etc. — a lot of methods to remember.

It works, it's in the stdlib, and you don't need to install anything. But pytest's `assert x == y` is so much cleaner that most projects switch.

## Quick reference of assertions

```python
self.assertEqual(a, b)
self.assertNotEqual(a, b)
self.assertTrue(x)
self.assertFalse(x)
self.assertIsNone(x)
self.assertIsNotNone(x)
self.assertIn(item, container)
self.assertIsInstance(x, type)
self.assertAlmostEqual(a, b, places=7)        # for floats
with self.assertRaises(ValueError):
    do_thing()
```

## setUp / tearDown

```python
class TestThing(unittest.TestCase):
    def setUp(self):
        self.db = create_test_db()

    def tearDown(self):
        self.db.close()

    def test_query(self):
        ...
```

Runs before/after each test method.

## When you'd actually use unittest

- You're maintaining old code that already uses it.
- You can't add third-party deps and you need *something*.
- You like the class-based structure.

For everything else, go to pytest.
