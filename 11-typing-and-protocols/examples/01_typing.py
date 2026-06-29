"""
Type hints, Protocols, generics.

Run:
    python 11-typing-and-protocols/examples/01_typing.py

To type-check:
    pip install mypy
    mypy 11-typing-and-protocols/examples/01_typing.py
"""
from typing import Protocol, runtime_checkable, TypedDict


# ---- 1. Plain hints -------------------------------------------------------

def greet(name: str, times: int = 1) -> str:
    return f"Hello, {name}!\n" * times


def parse_ages(rows: list[dict[str, str]]) -> dict[str, int]:
    return {row["name"]: int(row["age"]) for row in rows}


# ---- 2. Optional and union ------------------------------------------------

def find_user(users: dict[int, str], id_: int) -> str | None:
    return users.get(id_)


# ---- 3. Protocol ----------------------------------------------------------

@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...


class Resource:
    def __init__(self, name: str):
        self.name = name
        self.closed = False

    def close(self) -> None:
        self.closed = True
        print(f"  closed {self.name}")


def safely_close(item: Closeable) -> None:
    item.close()


# ---- 4. TypedDict ---------------------------------------------------------

class UserRecord(TypedDict):
    id: int
    name: str
    email: str


def save_user(u: UserRecord) -> None:
    print(f"  saving {u['name']} ({u['email']})")


# ---- 5. Generic function (3.12+ syntax) ----------------------------------

def first[T](items: list[T]) -> T:
    return items[0]


def first_or_default[T](items: list[T], default: T) -> T:
    return items[0] if items else default


# ---- run -----------------------------------------------------------------

if __name__ == "__main__":
    print("--- greet ---")
    print(greet("Ishan", 2), end="")

    print("--- parse_ages ---")
    rows = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
    print(parse_ages(rows))
    print()

    print("--- Optional ---")
    users = {1: "Alice", 2: "Bob"}
    print(find_user(users, 1))         # Alice
    print(find_user(users, 99))        # None
    print()

    print("--- Protocol (structural typing) ---")
    safely_close(Resource("db_conn"))
    print(f"isinstance check: {isinstance(Resource('x'), Closeable)}")
    print()

    print("--- TypedDict ---")
    save_user({"id": 1, "name": "Ishan", "email": "i@x.com"})
    print()

    print("--- Generic function preserves type ---")
    print(first([1, 2, 3]))            # int
    print(first(["a", "b", "c"]))      # str
    print(first_or_default([], "fallback"))
