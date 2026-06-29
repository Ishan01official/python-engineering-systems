# 02 — Inheritance

A subclass extends or specializes a parent class. It inherits all the parent's attributes and methods, and can override or add to them.

```python
class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return f"{self.name} makes a sound"


class Dog(Animal):
    def speak(self) -> str:                  # override
        return f"{self.name} barks"


class Puppy(Dog):
    def speak(self) -> str:
        # Call parent's implementation
        parent_msg = super().speak()
        return f"{parent_msg} (excitedly)"
```

```python
p = Puppy("Fido")
print(p.speak())     # "Fido barks (excitedly)"
print(p.name)        # "Fido" — inherited from Animal via Dog
```

## `super()`

`super()` calls the parent's version of a method. Use it inside `__init__` and overridden methods to extend rather than replace:

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)        # let Animal initialize name
        self.breed = breed
```

Without `super().__init__(...)`, the parent's `__init__` doesn't run and `self.name` won't exist.

## MRO — method resolution order

In multiple inheritance, Python uses the C3 linearization algorithm to decide which parent's method to call. You can inspect it:

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print(D.__mro__)
# (D, B, C, A, object)
```

When `D` is asked for an attribute, Python walks the MRO left to right until it finds it. The key intuition: **methods are resolved according to the MRO, not by literally walking up to "the parent"**.

Multiple inheritance is a sharp tool. Use it only when you've thought through the MRO carefully. In most cases, composition or mixins are cleaner.

## When NOT to use inheritance

Inheritance is overused. A common antipattern is creating a deep class hierarchy where each level adds one method:

```
Vehicle → LandVehicle → MotorVehicle → Car → SportsCar → ConvertibleSportsCar
```

This is fragile. Each subclass is tightly coupled to its ancestors. Change a parent and every descendant might break.

**Prefer composition.** Instead of `Car(Vehicle)`, have `Car` hold a `Vehicle` (engine, wheels, ...) as fields. Module 08.05 expands on this.

A rule of thumb:

- "Is a Dog a kind of Animal?" → inheritance can fit.
- "Does a Car *have* an Engine?" → composition.

If you can't honestly say "subclass IS-A superclass in every way", inheritance is the wrong tool.

## Abstract base classes

Sometimes you want to say "any subclass MUST implement these methods":

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

    @abstractmethod
    def perimeter(self) -> float: ...


class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14 * self.r ** 2
    def perimeter(self): return 2 * 3.14 * self.r

# Shape()  ← TypeError: Can't instantiate abstract class
```

Python 3.12+ also supports **Protocols** (Module 11), which give you structural typing — sometimes a better fit than ABCs.

## Read deeper

- **LP** 6e, Ch. 28–31 — OOP in depth
- **FP** 2e, Ch. 14 — inheritance and the diamond problem; what to use instead
- **EP** 3e — items on inheritance and abstract base classes
