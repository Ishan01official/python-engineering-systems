# 05 — Composition vs inheritance

A classic OO debate. In Python, the practical rule is: **favor composition over inheritance** by default. Use inheritance only for genuine "is-a" relationships, and even then, keep hierarchies shallow.

## What composition looks like

```python
class Engine:
    def start(self): return "vroom"
    def stop(self):  return "click"


class Car:
    def __init__(self, engine: Engine):
        self.engine = engine

    def start(self):
        return self.engine.start()    # delegate
```

`Car` *has an* `Engine`. It doesn't *inherit from* one. This means:

- You can swap engines (`ElectricEngine`, `DieselEngine`) without changing `Car`'s class hierarchy.
- `Car` is decoupled from `Engine`'s internals.
- Testing `Car` is easy — pass a mock engine.

## What inheritance looks like

```python
class Vehicle:
    def start(self): return "default vroom"


class Car(Vehicle):
    pass
```

`Car` *is a* `Vehicle`. This works when:

- The is-a relationship genuinely holds.
- You expect Car to inherit (and rarely override) most of Vehicle's behavior.
- Other code treats Cars as Vehicles polymorphically.

## When inheritance becomes painful

Three telltale signs you're using inheritance wrong:

1. **You override most methods.** If `Car.start`, `Car.stop`, `Car.fuel`, etc. all override `Vehicle`'s versions, the parent class is more nuisance than help.
2. **Deep hierarchies.** `A → B → C → D → E` means any change to `A` ripples through five classes. Refactoring nightmare.
3. **Subclasses need attributes the parent doesn't.** If `SportsCar` needs a turbo and `Truck` needs a bed, those go in `Vehicle` how? They don't — composition is better.

## Mixins — the middle ground

A mixin is a small class designed to be combined with others to add a specific capability:

```python
class JSONSerializableMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)


class User(JSONSerializableMixin):
    def __init__(self, name): self.name = name
```

Mixins work when they're truly single-purpose, name-prefixed (e.g. `*Mixin`), and don't have state of their own. Use them sparingly.

## Practical guideline

```
For each candidate inheritance relationship, ask:
  - Is this honestly "X is a Y"?    → maybe inherit
  - Is this "X has a Y"?            → compose

If you're unsure → compose. You can always refactor to inheritance later.
The reverse refactor (un-inheriting) is much harder.
```

## Example: Notification system done two ways

### Inheritance (overused)

```python
class Notification: ...
class EmailNotification(Notification): ...
class SMSNotification(Notification): ...
class PushNotification(Notification): ...
class UrgentEmailNotification(EmailNotification): ...
class ScheduledSMSNotification(SMSNotification): ...
```

Adding "urgent push" or "scheduled email" requires more subclasses. Combinatorial explosion.

### Composition

```python
@dataclass
class Notification:
    transport: "Transport"          # Email, SMS, or Push (a Protocol or ABC)
    urgent: bool = False
    scheduled_for: datetime | None = None
```

Now "urgent scheduled push" is just `Notification(transport=Push, urgent=True, scheduled_for=...)`. No new class needed.

## Read deeper

- **FP** 2e, Ch. 14 — exactly this debate, with strong examples.
- **EP** 3e — items on composition, mixins, and avoiding inheritance pitfalls.
