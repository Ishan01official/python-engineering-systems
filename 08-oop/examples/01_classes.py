"""
OOP patterns: classes, inheritance, dunders, dataclasses.

Run:
    python 08-oop/examples/01_classes.py
"""
from dataclasses import dataclass, field
from typing import ClassVar


# ---- 1. A plain class with methods ---------------------------------------

class Account:
    """A toy bank account demonstrating instance state and methods."""

    interest_rate: ClassVar[float] = 0.05      # class attribute, shared

    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount

    def __repr__(self) -> str:
        return f"Account(owner={self.owner!r}, balance={self.balance:.2f})"


# ---- 2. Inheritance ------------------------------------------------------

class SavingsAccount(Account):
    """Extends Account with monthly interest accrual."""

    def __init__(self, owner: str, balance: float = 0.0, rate: float | None = None):
        super().__init__(owner, balance)
        self.rate = rate if rate is not None else Account.interest_rate

    def accrue(self) -> None:
        self.balance += self.balance * self.rate


# ---- 3. A class with rich dunders ---------------------------------------

class Vector:
    """2D vector with operator overloading."""

    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __add__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)

    def __abs__(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __bool__(self) -> bool:
        return bool(abs(self))


# ---- 4. dataclass --------------------------------------------------------

@dataclass
class Product:
    name: str
    price: float
    tags: list[str] = field(default_factory=list)    # SAFE default

    def discounted(self, pct: float) -> float:
        return self.price * (1 - pct)


@dataclass(frozen=True, slots=True)
class Point:
    """Immutable, memory-efficient, hashable."""
    x: float
    y: float


# ---- run -----------------------------------------------------------------

if __name__ == "__main__":
    print("--- Account ---")
    a = Account("Ishan", 1000)
    a.deposit(500)
    a.withdraw(200)
    print(a)

    print("\n--- SavingsAccount (inheritance + super) ---")
    s = SavingsAccount("Ishan", 1000)
    s.accrue()
    print(s)
    print(f"isinstance(s, Account)? {isinstance(s, Account)}")

    print("\n--- Vector (dunders) ---")
    v = Vector(3, 4)
    w = Vector(1, 1)
    print(f"v = {v}")
    print(f"v + w = {v + w}")
    print(f"v * 2 = {v * 2}")
    print(f"abs(v) = {abs(v)}")
    print(f"{{v: 'origin offset'}} = {{Vector(3,4): 'origin offset'}}  (works because hashable)")

    print("\n--- Product (dataclass) ---")
    p = Product("Notebook", 199.0, tags=["paper", "ruled"])
    print(p)
    print(f"discounted 10%: {p.discounted(0.1)}")
    p2 = Product("Notebook", 199.0, tags=["paper", "ruled"])
    print(f"equal by value? {p == p2}")

    print("\n--- Point (frozen + slots) ---")
    pt = Point(1.5, 2.5)
    print(pt)
    try:
        pt.x = 9.0
    except Exception as e:
        print(f"can't mutate frozen: {type(e).__name__}: {e}")
    print(f"hash works: hash(pt) = {hash(pt)}")
