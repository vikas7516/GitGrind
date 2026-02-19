# 🚀 PHASE 2 — Data Models (What Things Look Like In Code)

---

## 🎯 Goal

Before you can build a game, you need to decide: what IS an exercise? What IS a level? What IS a teaching slide?

In this phase, you'll define the **shape** of your data using Python dataclasses. After this, every other file will use these shapes.

---

## 🔹 Step 1 — Understand the Problem

Right now, if you wanted to store an exercise, you might use a dictionary:

```python
exercise = {
    "prompt": "What command initializes a repo?",
    "answer": "git init",
}
```

This works, but it has a serious problem. Watch:

```python
exercise = {
    "promt": "What command initializes a repo?",   # ← Typo! "promt" not "prompt"
    "answer": "git init",
}
print(exercise["prompt"])  # 💥 KeyError! Python doesn't catch the typo.
```

You misspelled `"prompt"` as `"promt"` — and Python didn't warn you. You'd only discover this when the code crashes at runtime.

**Dataclasses fix this.** They force you to define the exact fields upfront, and Python catches mistakes immediately.

---

## 🔹 Step 2 — Learn Dataclasses (5-Minute Crash Course)

A dataclass is a clean way to define structured data. Here's the simplest example:

```python
from dataclasses import dataclass

@dataclass
class Dog:
    name: str
    age: int

my_dog = Dog(name="Buddy", age=3)
print(my_dog)        # Dog(name='Buddy', age=3)
print(my_dog.name)   # Buddy
print(my_dog.age)    # 3
```

**What's happening here?**

| Code | What It Does |
|------|-------------|
| `from dataclasses import dataclass` | Imports the dataclass feature |
| `@dataclass` | A "decorator" — it tells Python to auto-generate setup code for this class |
| `class Dog:` | Defines a new type called `Dog` |
| `name: str` | Says "every Dog must have a `name` that's a string" |
| `age: int` | Says "every Dog must have an `age` that's a number" |
| `Dog(name="Buddy", age=3)` | Creates a Dog object with these values |
| `my_dog.name` | Access the name using a dot |

**If you misspell a field:**

```python
my_dog = Dog(naem="Buddy", age=3)
# 💥 TypeError: Dog.__init__() got an unexpected keyword argument 'naem'
```

Python catches it immediately! That's the point.

### Optional Fields (With Defaults)

Some fields are optional — not every exercise has a hint. You do this with default values:

```python
@dataclass
class Dog:
    name: str       # Required — must always be provided
    age: int        # Required
    color: str = "brown"  # Optional — defaults to "brown" if not provided

dog1 = Dog(name="Buddy", age=3)           # color will be "brown"
dog2 = Dog(name="Rex", age=5, color="black")  # color is "black"
```

**One rule:** Required fields must come BEFORE optional fields. This won't work:

```python
# ❌ WRONG — optional field before required field
@dataclass
class Dog:
    color: str = "brown"   # Optional
    name: str              # Required — ERROR! Can't come after optional
```

Python will say: `TypeError: non-default argument follows default argument`

### Lists as Fields

If a field is a list, you need a special trick:

```python
from dataclasses import dataclass, field

@dataclass
class Dog:
    name: str
    tricks: list = field(default_factory=list)  # Default is an empty list
```

**Why `field(default_factory=list)` instead of just `tricks: list = []`?**

Because if you write `tricks: list = []`, ALL dogs would share the SAME list object. Adding a trick to one dog would add it to every dog. `field(default_factory=list)` creates a fresh new list for each dog.

You don't need to fully understand why right now — just remember the pattern: **mutable defaults (lists, dicts) need `field(default_factory=...)`**.

---

## 🔹 Step 3 — Design Your Models

Your game needs 4 data types. Here's what each one is:

### Teaching — A Single Lesson Slide

When the player enters a level, they first see teaching slides that explain Git commands. Each slide teaches ONE command.

```
A Teaching has:
  command        → "git init" (the command being taught)
  explanation    → What it does and when to use it (2-4 sentences)
  syntax         → The command template, like "git add <file>"
  example_output → What the terminal would show after running it
  pro_tip        → Optional handy tip (not every teaching has one)
```

### Exercise — A Single Question

After the teachings, the player answers exercises to practice what they learned.

```
An Exercise has:
  type           → "recall" or "scenario" (what kind of question)
  prompt         → The question text shown to the player
  answers        → A LIST of acceptable answers (any match = correct)
  hint           → Optional help text (shown when player types "hint")
  explanation    → Shown after a wrong answer (explains WHY it's wrong)
  sim_output     → Shown after a correct answer (simulated terminal output)
```

**Why is `answers` a list?** Because some questions have multiple correct answers:

```python
answers = ["git init", "git init ."]   # Both are valid!
```

### Level — A Collection of Teachings + Exercises

A level groups teachings and exercises about one topic.

```
A Level has:
  number           → 1, 2, 3...
  name             → "Init & Status"
  tagline          → Short description
  concept          → Intro paragraph (2-3 sentences)
  commands_taught  → List of command strings taught in this level
  teachings        → List of Teaching objects
  exercises        → List of Exercise objects
```

### Stage — One Entry in the Progression Map

The stage map defines the order: setup → level 1 → level 2. Each entry in the map is a Stage.

```
A Stage has:
  stage_type → "setup" or "level" (what kind of stage)
  data_key   → Which level number it points to (0, 1, 2...)
  label      → Display name like "Level 1 — Init & Status"
```

---

## 🔹 Step 4 — Write the Code (`content/models.py`)

Now translate those designs into Python. Open `content/models.py` and write this:

```python
"""
GitGrind — Data models.
Defines the shape of every piece of game data.
"""
from dataclasses import dataclass, field


@dataclass
class Teaching:
    """A single teaching slide shown during a lesson."""
    command: str          # e.g. "git init"
    explanation: str      # What it does, when/why to use it
    syntax: str           # Command template, e.g. "git add <file>"
    example_output: str   # Simulated terminal output
    pro_tip: str = ""     # Optional best practice or gotcha


@dataclass
class Exercise:
    """A single exercise (question) within a level."""
    type: str             # "recall" or "scenario"
    prompt: str           # The question text
    answers: list         # List of acceptable answer strings
    hint: str = ""        # Optional help text
    explanation: str = "" # Shown after wrong answer
    sim_output: str = ""  # Shown after correct answer


@dataclass
class Level:
    """One complete level with teachings and exercises."""
    number: int
    name: str
    tagline: str
    concept: str                          # Intro paragraph
    commands_taught: list                 # e.g. ["git init", "git status"]
    teachings: list = field(default_factory=list)   # List of Teaching objects
    exercises: list = field(default_factory=list)   # List of Exercise objects


@dataclass
class Stage:
    """One entry in the stage progression map."""
    stage_type: str   # "setup" or "level"
    data_key: int     # Which level number (0, 1, 2...)
    label: str        # Display name
```

### Understanding the code:

| Line | Why It's There |
|------|---------------|
| `command: str` | Required field — every Teaching MUST have a command |
| `pro_tip: str = ""` | Optional field — defaults to empty string if not provided |
| `answers: list` | Required list — every Exercise MUST have at least one answer |
| `teachings: list = field(default_factory=list)` | Optional list — defaults to empty list |

---

## 🔹 Step 5 — Test Your Models

Add this at the bottom of `content/models.py`:

```python
# Temporary test — delete this later
if __name__ == "__main__":
    # Create a Teaching
    t = Teaching(
        command="git init",
        explanation="Creates a new Git repo in your current folder.",
        syntax="git init",
        example_output="$ git init\nInitialized empty Git repository in /project/.git/",
        pro_tip="Only run this once per project."
    )
    print(t)
    print(f"Command: {t.command}")
    print()

    # Create an Exercise
    ex = Exercise(
        type="recall",
        prompt="What command initializes a repo?",
        answers=["git init", "git init ."],
        hint="It creates a hidden .git folder.",
        explanation="git init creates a new Git repository.",
    )
    print(ex)
    print(f"Prompt: {ex.prompt}")
    print(f"Answers: {ex.answers}")
    print(f"Has hint: {bool(ex.hint)}")
    print()

    # Create an Exercise WITHOUT optional fields
    ex2 = Exercise(
        type="scenario",
        prompt="You need to check the repo status.",
        answers=["git status"],
    )
    print(ex2)
    print(f"Hint: '{ex2.hint}'")       # Empty string
    print(f"Explanation: '{ex2.explanation}'")  # Empty string
```

Run it:

```
python content/models.py
```

**You should see** clean output with your Teaching and Exercise objects printed, showing all their fields. No errors.

**If you get an error:**
- `"ModuleNotFoundError"` → Make sure `content/__init__.py` exists
- `"TypeError: non-default argument follows default argument"` → Check that all required fields come before optional fields

**Now delete the test code** from the bottom of `models.py`.

---

## ✅ Checklist (Don't Move On Until)

- [ ] `content/models.py` exists and runs without errors
- [ ] You can create a Teaching object and access its fields
- [ ] You can create an Exercise WITH optional fields (hint, explanation)
- [ ] You can create an Exercise WITHOUT optional fields (they default to "")
- [ ] You understand WHY `answers` is a list, not a single string

---

## 🛟 If Something Goes Wrong

**"TypeError: non-default argument follows default argument"**
→ Required fields (no `=`) must come BEFORE optional fields (with `=`). Check the order.

**"NameError: name 'dataclass' is not defined"**
→ Add `from dataclasses import dataclass, field` at the top.

**"TypeError: ... got an unexpected keyword argument"**
→ You misspelled a field name when creating the object. Check spelling exactly.

---

**Phase 2 done? You have data structures. Now let's fill them with real content → [phase3.md](phase3.md)**
