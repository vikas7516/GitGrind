# 🚀 PHASE 2 — Expanded Data Models

---

## 🎯 Goal

Add new data models to support exercise rounds, boss fights, all 8 exercise types, and a StageType enum. After this phase, you'll have the data shapes for EVERY feature in the full version.

> **Open `content/models.py` and follow along.** This guide explains every field and every design decision in that file.

---

## What You'll Learn

- Why Python needs `field(default_factory=list)` for mutable defaults
- How to design flexible data models using optional fields
- How `str, Enum` dual inheritance works and why it matters
- How `__post_init__` lets you run code after dataclass creation
- Why one flexible Exercise class beats 8 specialized ones

---

## Step 1 — Understand the Mutable Default Bug

Before writing any models, you need to understand the single most dangerous bug in Python dataclasses. It's invisible until it destroys your data.

### The Bug

```python
@dataclass
class Level:
    exercises: list = []     # ❌ LOOKS fine, but it's a bomb
```

### Why It's Dangerous

Python creates `[]` ONCE, when the class is defined — not when you create an instance. Every instance then shares that SAME list object:

```python
level1 = Level()
level2 = Level()
level1.exercises.append("git init")
print(level2.exercises)  # → ["git init"]  ← WHAT?!
```

`level2` never touched exercises, but it has `"git init"` because both instances point to the same list in memory.

**Why does this happen?** When Python sees `exercises: list = []`, it evaluates `[]` once during class definition and stores that single list object as the default. Every new `Level()` that doesn't provide its own `exercises` argument gets a reference to that same object — not a copy.

This is different from how function defaults work in most beginner tutorials. With simple types like `int` or `str`, sharing defaults is harmless because numbers and strings are **immutable** — you can't change `0` in place. But lists are **mutable** — `.append()` changes the list object itself, and since all instances share the same object, they all see the change.

### The Fix

```python
from dataclasses import dataclass, field

@dataclass
class Level:
    exercises: list = field(default_factory=list)  # ✅ NEW list per instance
```

`field(default_factory=list)` tells Python: "don't reuse one list — call `list()` fresh every time you create an instance." Each `Level()` gets its own independent list.

### The Rule

| Type | Can use `= value`? | Needs `field(default_factory=...)`? |
|------|--------------------|-------------------------------------|
| `str` | ✅ `= ""` | No — strings are immutable |
| `int` | ✅ `= 0` | No — integers are immutable |
| `float` | ✅ `= 0.0` | No — floats are immutable |
| `bool` | ✅ `= False` | No — booleans are immutable |
| `tuple` | ✅ `= (8, 10)` | No — tuples are immutable |
| `list` | ❌ Never use `= []` | ✅ `field(default_factory=list)` |
| `dict` | ❌ Never use `= {}` | ✅ `field(default_factory=dict)` |
| `set` | ❌ Never use `= set()` | ✅ `field(default_factory=set)` |

**If it's mutable (can be changed in place), use `default_factory`.** If it's immutable (can't be changed), a simple `= value` is fine.

---

## Step 2 — Understand Enum (Why Not Just Strings)

Your MVP used plain strings like `"recall"` and `"scenario"` for exercise types. That works, but strings have no guardrails:

```python
# No error — "boos" is fine as a string
stage = Stage(stage_type="boos", data_key=1, label="Boss Fight")
# ... crashes at RUNTIME later when nothing matches "boos"
```

An Enum catches this at definition time:

```python
class StageType(str, Enum):
    SETUP = "setup"
    LEVEL = "level"
    EXERCISE = "exercise"
    BOSS = "boss"
```

Now `StageType.BOOS` throws `AttributeError` immediately. You catch the typo before running a single game loop.

### Why `str, Enum` (Dual Inheritance)?

`StageType` inherits from BOTH `str` and `Enum`. This is unusual but critical:

```python
stage_type = StageType.LEVEL

# It's an Enum (catches typos, auto-complete in editors):
stage_type == StageType.LEVEL      # True

# It's ALSO a string (can be compared to plain strings):
stage_type == "level"              # True

# It can be serialized to JSON directly:
json.dumps({"type": stage_type})   # '{"type": "level"}'
```

Without `str` inheritance, `StageType.LEVEL == "level"` would be `False`. This would break your entire codebase, because your MVP already uses string comparisons everywhere: `if stage.stage_type == STAGE_LEVEL:`. The dual inheritance means the Enum IS a string — old code keeps working and new code gets typo protection.

---

## Step 3 — Understand `from __future__ import annotations`

Open `content/models.py` — the very first line (after the docstring) is:

```python
from __future__ import annotations
```

**What does this do?** It tells Python: "don't evaluate type annotations at class-definition time — just store them as strings."

**Why does this matter?** Without it, if you write:

```python
class Exercise:
    steps: list[Exercise]  # ← Python tries to evaluate "Exercise" RIGHT NOW
```

Python would crash because `Exercise` isn't fully defined yet — you're still in the middle of defining it! This is called a **forward reference** problem.

With `from __future__ import annotations`, Python stores `"list[Exercise]"` as a string instead of trying to evaluate it. The type checkers (like mypy) still understand it, but Python itself doesn't crash.

**Rule of thumb:** Always put this import at the top of any file where classes reference each other or themselves in type hints.

---

## Step 4 — Walk Through Every Model

Open `content/models.py`. Let's walk through each class, understanding every field and why it exists.

### `Teaching` — A Lesson Slide

```python
@dataclass
class Teaching:
    command: str         # e.g. "git init"
    explanation: str     # 2-4 sentences: what it does, when/why
    syntax: str          # syntax template, e.g. "git add <file>"
    example_output: str  # simulated terminal session
    pro_tip: str = ""    # optional best practice / gotcha
```

Each field serves a different part of the UI display:

| Field | Where It Appears | Why It's Separate |
|-------|-----------------|-------------------|
| `command` | Header of the teaching slide | The player needs to know WHAT command they're learning |
| `explanation` | Body text | WHY and WHEN to use this command |
| `syntax` | Syntax box | The generic template with `<placeholders>` |
| `example_output` | Terminal simulation panel | Shows WHAT HAPPENS when you run it |
| `pro_tip` | Highlighted tip at the bottom | Best practices — optional, not every command needs one |

**Why not combine `explanation` and `pro_tip`?** Because the UI renders them differently. `explanation` is plain text. `pro_tip` gets a special highlighted box with a 💡 icon. If they were combined, the UI function would need to parse them apart.

**Why is `pro_tip` the only field with a default (`= ""`)? ** Because not every command needs a tip. But every teaching MUST have a command, explanation, syntax, and example output — those are required fields. In dataclasses, fields without defaults (required) must come before fields with defaults (optional). That's why `pro_tip` is last.

### `Exercise` — One Flexible Class for 8 Types

```python
@dataclass
class Exercise:
    type: str            # 'recall', 'fill_blank', 'scenario', etc.
    prompt: str
    answers: list        # list of acceptable answer strings
    hint: str = ""
    explanation: str = ""
    sim_output: str = ""
    error_output: str = ""      # only for 'error_fix' type
    blank_template: str = ""    # only for 'fill_blank' type
    choices: list = field(default_factory=list)   # only for 'multi_choice'
    steps: list = field(default_factory=list)     # only for 'multi_step'
```

**Why one class with optional fields instead of 8 separate classes?**

With 8 classes (`RecallExercise`, `FillBlankExercise`, etc.), every function would need:

```python
def run_exercise(exercise):
    if isinstance(exercise, RecallExercise): ...
    elif isinstance(exercise, FillBlankExercise): ...
    # ... 6 more elif blocks
```

With one class and a `type` field, validation is simpler — the runner checks `exercise.type` to decide which validator to call. Most types use the same `check_answer()` function; only `fill_blank` and `multi_choice` need special validators.

The trade-off: some fields sit unused. A `recall` exercise creates an empty `choices` list it never uses. For ~200 exercises, the wasted memory is negligible.

**Understanding each field:**

| Field | Used By | Purpose |
|-------|---------|---------|
| `type` | All | Tells the runner/UI which behavior to use |
| `prompt` | All | The question text shown to the player |
| `answers` | All | Accepted answers (first = canonical for display) |
| `hint` | All (optional) | Shown when player types "hint" |
| `explanation` | All (optional) | Shown after wrong answer or skip to teach |
| `sim_output` | All (optional) | Simulated terminal output shown after correct answer |
| `error_output` | `error_fix` only | The error message the player must diagnose |
| `blank_template` | `fill_blank` only | Template like `git ____ -m 'msg'` |
| `choices` | `multi_choice` only | The list of options: `["a) git add", "b) git commit", ...]` |
| `steps` | `multi_step` only | Sub-exercises that must be completed in order |

Notice that `choices` and `steps` use `field(default_factory=list)` while `hint`, `explanation`, `sim_output`, `error_output`, and `blank_template` use `= ""`. That's the mutable default rule from Step 1: strings are immutable (safe to share), lists are mutable (must create fresh copies).

### `Level` — A Teaching + Practice + Drill Unit

```python
@dataclass
class Level:
    number: int
    name: str
    tagline: str
    concept: str              # 2-3 line concept card
    commands_taught: list     # for notebook tracking
    exercises: list           # guided practice
    drills: list              # randomized test pool
    teachings: list = field(default_factory=list)
    drill_pass: tuple = (8, 10)   # (required, total)
```

**Why does Level have BOTH `exercises` and `drills`?**

They serve different gameplay phases:

```
Level Flow:
  Phase 1: Teaching slides  → teach the concepts
  Phase 2: Exercises        → guided practice (skip OK, order matters)
  Phase 3: Drill zone       → randomized review (must score ≥ threshold)
```

Exercises are handcrafted, ordered, and specific — designed to walk the player through scenarios in a particular sequence. Drills are randomized from a pool and scored against a threshold.

If they were combined in one list, the runner would need to figure out which exercises are "for learning" vs "for testing." Keeping them separate means the runner just iterates each list at the right time.

**Why is `teachings` optional (`field(default_factory=list)`) but `exercises` is required?**

The setup intro (Level 0) has exercises but no teachings — it's a tutorial on how the game works, not a Git lesson. By making `teachings` optional, Level 0 can exist without dummy teaching objects.

**Why is `drill_pass` a tuple `(8, 10)` instead of a percentage?**

Because `(8, 10)` is instantly readable: "get 8 out of 10 right." A percentage like `0.8` requires mental math or documentation to know the total. The tuple also lets the runner know exactly how many questions to draw: `pool = _build_pool(drills, 10)`.

### `ExerciseRound` — Grinding Sessions

```python
@dataclass
class ExerciseRound:
    number: int
    name: str
    tagline: str
    exercises: list
    pass_threshold: tuple    # (required, total)
```

An exercise round is like a level's drill zone but standalone — not attached to any level. It draws from mixed topics for spaced review.

**Why does it have `pass_threshold` instead of `drill_pass`?** Different name, same concept. Using a different field name makes the code clearer: levels have "drill pass" (pass the drill), rounds have "pass threshold" (minimum to pass the round).

### `BossFight` — Multi-Step Scenario Gauntlets

```python
@dataclass
class BossFight:
    number: int
    name: str
    tagline: str
    story: str           # narrative intro
    steps: list          # list of Exercise objects
```

**Why are boss steps `Exercise` objects, not a separate `BossStep` class?**

Because they already need everything `Exercise` has: `prompt`, `answers`, `explanation`, `sim_output`. Creating a `BossStep` class with the same fields would be duplication.

Using `Exercise` for boss steps means:
- The validator works on boss steps without changes
- The UI can display step prompts with existing functions
- Adding hints to boss steps later requires zero new code

**Why does `BossFight` have a `story` field?**

Boss fights are narrative-driven — each one tells a scenario ("Your teammate pushed to the wrong branch..."). The `story` is displayed before the steps begin, setting the scene.

### `Stage` — The Stage Map Entry

```python
@dataclass
class Stage:
    stage_type: Union[str, StageType]
    data_key: int
    label: str

    def __post_init__(self) -> None:
        if isinstance(self.stage_type, StageType):
            self.stage_type = self.stage_type.value
```

**What is `__post_init__`?**

It's a special method that `@dataclass` calls automatically AFTER `__init__` finishes. Normal `__init__` (which `@dataclass` generates for you) just assigns `self.stage_type = stage_type`. Then `__post_init__` runs and normalizes the type.

This lets you create stages both ways:

```python
# Using the Enum (clean, catches typos):
Stage(stage_type=StageType.LEVEL, data_key=1, label="Level 1")

# Using a plain string (backward compatible):
Stage(stage_type="level", data_key=1, label="Level 1")
```

Both produce the same result: `stage.stage_type == "level"`. Without `__post_init__`, you'd need to normalize manually every time you create a `Stage`.

**What is `Union[str, StageType]`?**

It's a type hint saying "this field accepts either a `str` or a `StageType`." This is how the function signature documents that both formats are valid. The `__post_init__` method then normalizes everything to `str` internally.

### Legacy Constants

```python
STAGE_SETUP = StageType.SETUP.value      # "setup"
STAGE_LEVEL = StageType.LEVEL.value      # "level"
STAGE_EXERCISE = StageType.EXERCISE.value # "exercise"  
STAGE_BOSS = StageType.BOSS.value        # "boss"
```

Your MVP uses `STAGE_LEVEL` as a plain string everywhere. These constants let old code keep working without changing every comparison. It's a **backward compatibility layer**: old code uses constants, new code uses the Enum, both produce the same string.

---

## Step 5 — Dataclass Field Ordering Rule

Python dataclasses have a strict rule: **fields without defaults (required) must come BEFORE fields with defaults (optional).**

```python
# ❌ This CRASHES:
@dataclass
class Exercise:
    hint: str = ""       # optional field
    prompt: str          # required field AFTER optional — TypeError!

# ✅ This works:
@dataclass
class Exercise:
    prompt: str          # required first
    hint: str = ""       # optional after
```

**Why?** Because Python generates an `__init__` method where required fields become positional arguments and optional fields become keyword arguments. In Python function signatures, positional arguments must always come before keyword arguments.

Look at the `Level` class in `models.py`:
- `number`, `name`, `tagline`, `concept`, `commands_taught`, `exercises`, `drills` — all required, no defaults
- `teachings` — optional, has `field(default_factory=list)`
- `drill_pass` — optional, has `= (8, 10)`

The required fields come first. The optional fields come last. This ordering is NOT arbitrary — it's enforced by Python.

---

## Step 6 — Test Your Models

Open `content/models.py` and verify:

1. All 7 classes exist: `StageType`, `Teaching`, `Exercise`, `Level`, `ExerciseRound`, `BossFight`, `Stage`
2. All mutable defaults use `field(default_factory=...)`
3. `from __future__ import annotations` is at the top
4. Required fields come before optional fields in every class

Then run:

```
python -m pytest tests/ -v
```

If anything breaks, check:

| Error | Fix |
|-------|-----|
| `TypeError: unexpected keyword argument` | You renamed a field — update the code that creates these objects |
| `TypeError: missing required argument` | You removed a default — add it back |
| `TypeError: non-default argument follows default argument` | Move required fields before optional fields |
| `ImportError: cannot import name 'BossFight'` | Class not defined yet — add it to models.py |

---

## ✅ Quality Gate

- [ ] `content/models.py` has all 7 classes
- [ ] `Exercise` has 11 fields (3 required + 8 optional)
- [ ] All list/dict fields use `field(default_factory=...)`
- [ ] `StageType` has 4 values: SETUP, LEVEL, EXERCISE, BOSS
- [ ] `Stage.__post_init__` normalizes Enum to string
- [ ] Legacy constants exist for backward compatibility
- [ ] `from __future__ import annotations` is at the top
- [ ] Required fields come before optional fields in every class
- [ ] Existing tests still pass

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `TypeError: non-default argument follows default argument` | Required fields (no default) must come BEFORE optional fields |
| `NameError: 'field' is not defined` | Add `field` to import: `from dataclasses import dataclass, field` |
| Shared list bug (one instance leaks into another) | Replace `= []` with `field(default_factory=list)` |
| `Stage.__post_init__` not running | Method name must be exactly `__post_init__` (double underscores both sides) |
| `StageType.BOOS` not throwing error | That's correct — Enum catches the typo at definition time |

---

**Phase 2 complete? Now upgrade the validator to handle all exercise types → [phase3.md](phase3.md)**
