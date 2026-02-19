# 🚀 PHASE 1 — Foundation Upgrade

---

## 🎯 Goal

Prepare your MVP codebase for scaling. Add new files, verify your architecture, and migrate your MVP content — all before writing a single feature.

---

## What You'll Learn

- Why multi-file projects need strict import rules
- What circular imports are and how to prevent them
- How to use stub files to verify architecture before building
- How to safely migrate existing working code

---

## Step 1 — Understand Why This Phase Exists

Your MVP has ~5 working files. The full version will have 15+. You could jump straight into features, but here's what happens:

1. You write 200 lines of boss fight logic
2. You try to import it → `ImportError: circular import`
3. You spend 2 hours restructuring files
4. You break your working MVP in the process

**Foundation first, features later.** This phase takes 30 minutes and saves hours.

---

## Step 2 — Understand Circular Imports

This is the #1 project-killer in multi-file Python apps.

### What Is a Circular Import?

When File A imports File B, and File B imports File A:

```python
# engine/runner.py
from content.models import Exercise  # ✅ Content is "below" engine — fine

# content/models.py
from engine.runner import run_exercise  # ❌ CIRCULAR — content imports engine
```

Python tries to load both at the same time and crashes:

```
ImportError: cannot import name 'run_exercise' from partially initialized module
```

### Why It Happens

When Python sees `from content.models import Exercise` inside `runner.py`, it pauses loading `runner.py` and starts loading `models.py`. But if `models.py` also says `from engine.runner import run_exercise`, Python would need to go back and finish loading `runner.py` first — which it already paused. This creates a deadlock: both files are half-loaded, waiting for the other.

The error message says "partially initialized module" because Python has started creating the module object (so the name exists) but hasn't finished executing the file (so the classes/functions inside aren't defined yet).

### How to Prevent It

Think of your project as layers stacked on top of each other. Each layer can only import from layers BELOW it, never above:

```
           ┌─────────────────────┐
Layer 4:   │ main.py             │  ← imports everything
           ├─────────────────────┤
Layer 3:   │ engine/runner.py    │  ← imports engine/*, content/*, ui
           ├─────────────────────┤
Layer 2:   │ engine/validator.py │  ← imports nothing from project (except re, difflib)
           │ engine/state.py     │  ← imports nothing from project (except json, os)
           │ ui.py               │  ← imports content/glossary (for display)
           ├─────────────────────┤
Layer 1:   │ content/*.py        │  ← imports ONLY content/models
           │ notebook.py         │  ← imports os
           │ sounds.py           │  ← imports threading, winsound
           └─────────────────────┘

Rule: arrows only point DOWN, never UP.
```

**Why does `runner.py` sit at Layer 3 while `validator.py` and `state.py` sit at Layer 2?**

Because `runner.py` imports from `ui`, `validator`, and `state` — it depends on all of them. But `validator.py` only depends on Python standard libraries (`re`, `functools`), and `state.py` only depends on standard libraries (`json`, `os`, `time`). They don't reach up to runner or main, so they sit lower in the stack.

**Why does `ui.py` import from `content/`?**

The glossary is a content file (`content/glossary.py`), but the UI needs to display it. This is a one-way dependency: UI reads content data, content never reads from UI. One-way is safe. Circular (two-way) is what crashes.

### How to Check

Open a terminal in your project root and run:

```
grep -rn "from engine" content/*.py
grep -rn "import engine" content/*.py
grep -rn "from ui" engine/*.py
grep -rn "import ui" engine/validator.py engine/state.py
```

**Every single one should return nothing.** If any return results, you have a boundary violation.

---

## Step 3 — Create New Files

Your project needs these new files. Create each one as a **stub** — a file with just a docstring explaining what will go there:

### Root Level

| File | Purpose |
|------|---------|
| `notebook.py` | Notebook system — tracks learned commands, exports to `.txt` |
| `sounds.py` | Sound feedback — plays melodies via `winsound` (Windows) or silent fallback |
| `validate.py` | Codebase integrity checker — run anytime to verify your project structure |

### Content Package

| File | Purpose |
|------|---------|
| `content/levels_basics.py` | Levels 1-6: init, status, add, commit, .gitignore, diff, log |
| `content/levels_branch.py` | Levels 7-10: branching, switching, merging, conflicts |
| `content/levels_remote.py` | Levels 11-14: remotes, clone, push, pull & fetch |
| `content/levels_adv.py` | Levels 15-21: restore, revert, stash, reflog, rebase, pro moves |
| `content/exercises.py` | 7 exercise rounds — mixed grinding sessions |
| `content/bossfights.py` | 6 boss fight multi-step challenges |
| `content/glossary.py` | Git terminology glossary data |

### What's a Stub?

A stub looks like this:

```python
"""GitGrind — Notebook system.
Progressive reference of all commands learned during gameplay.
"""
```

That's it — just a docstring. No code. The docstring tells anyone reading the file what will eventually go here.

### Why Stubs, Not Empty Files?

Two reasons:

1. **Documentation** — when you come back to `content/bossfights.py` four phases later, you immediately know "Right, this holds BossFight objects" without having to remember your plan.

2. **Import testing** — you can verify that Python can find and load every file BEFORE writing 500 lines of code.

### Root Level (Dependencies)

Create `requirements.txt` with these libraries:

```text
rich
pytest
```

Run `pip install -r requirements.txt` to install them.
 A broken import discovered after writing 500 lines means 500 lines that can't run.

---

## Step 4 — Verify Import Health

This is the "smoke test" for your architecture. Create a temporary file:

```python
# test_imports.py (delete this after it passes)
"""Quick check: can Python find all our modules?"""

# Root modules
import main
import ui
import notebook
import sounds

# Engine package
from engine import validator, state, runner

# Content package
from content import models, stage_map

# New content stubs
import content.levels_basics
import content.levels_branch
import content.levels_remote
import content.levels_adv
import content.exercises
import content.bossfights
import content.glossary

print("✅ All imports clean!")
```

Run it:

```
python test_imports.py
```

### What This Test Does

Python executes every `import` statement, which forces it to load every file in your project. If any file has a syntax error, missing dependency, or circular import, it will fail HERE — not during gameplay where the error is harder to debug.

This is a **fail-fast** pattern: discover architecture problems immediately, not after building features on a broken foundation.

### If It Fails

| Error | What's Happening | Fix |
|-------|-----------------|-----|
| `ModuleNotFoundError: No module named 'notebook'` | Python can't find the file | Create `notebook.py` in project root |
| `ModuleNotFoundError: No module named 'content.levels_basics'` | File doesn't exist in `/content/` | Create the stub file |
| `ModuleNotFoundError: No module named 'content'` | Missing package marker | Create empty `content/__init__.py` |
| `ImportError: cannot import name ...` | Circular import (see Step 2) | Remove the violating import |
| `SyntaxError` | Typo in one of your stub docstrings | Open the file and fix the syntax |

Fix all errors, run again. Once it prints `✅ All imports clean!`, delete `test_imports.py` — it has served its purpose.

---

## Step 5 — Migrate Your MVP Content

Your MVP has `content/levels_mvp.py` (or similar) with 3 levels. The full version splits levels into 4 topic files. Here's how to migrate safely.

### 5.1 — Copy, Don't Move

Copy your MVP levels into `content/levels_basics.py`. Don't delete the old file yet.

```python
from content.models import Level, Exercise, Teaching

BASICS_LEVELS = {
    # Paste your MVP levels here with the SAME numeric keys
    # 1: Level(number=1, name="Init & Status", ...),
    # 2: Level(number=2, name="Staging Files", ...),
    # 3: Level(number=3, name="Committing", ...),
}
```

**Why copy, not rename?** Because renaming breaks every `import` instantly. Copying lets you update imports one file at a time while the old file still exists as a fallback. If anything breaks, the old file is still there.

**Why keep the same numeric keys?** Because `stage_map.py` references levels by number. If your MVP uses `1`, `2`, `3` as keys, the full version must too — otherwise the stage map can't find the levels.

### 5.2 — Find Every Reference to the Old File

```
grep -rn "levels_mvp" *.py engine/*.py content/*.py tests/*.py
```

This command searches every `.py` file for the string `"levels_mvp"`. Each result shows you a file and line number that needs updating:

```python
# Before
from content.levels_mvp import LEVELS

# After
from content.levels_basics import BASICS_LEVELS
```

### 5.3 — Update, Test, Repeat

After updating each file's imports:

```
python -m pytest tests/ -v
```

Fix any failures before moving to the next file. This "change one thing, test, repeat" pattern prevents cascading errors.

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: levels_mvp` | Missed an import | Run the grep again |
| `KeyError` in runner | Changed dictionary keys | Use the SAME numeric keys |
| Tests fail but app works | Test file still imports the old path | Update test imports too |

### 5.4 — Delete the Old File

Only after ALL tests pass and the app runs correctly:

```
del content\levels_mvp.py
```

Run tests one final time to confirm absolutely nothing depended on it.

---

## Step 6 — Verify Your Full Project Structure

Your project should now look like this:

```
GitGrind/
├── main.py                    ← updated imports
├── ui.py
├── notebook.py                ← NEW (stub)
├── sounds.py                  ← NEW (stub)
├── validate.py                ← NEW (stub)
├── engine/
│   ├── __init__.py
│   ├── validator.py
│   ├── state.py
│   └── runner.py
├── content/
│   ├── __init__.py
│   ├── models.py
│   ├── levels_basics.py       ← NEW (migrated from levels_mvp.py)
│   ├── levels_branch.py       ← NEW (stub)
│   ├── levels_remote.py       ← NEW (stub)
│   ├── levels_adv.py          ← NEW (stub)
│   ├── exercises.py           ← NEW (stub)
│   ├── bossfights.py          ← NEW (stub)
│   ├── glossary.py            ← NEW (stub)
│   └── stage_map.py           ← updated imports if needed
├── tests/
│   └── test_core.py
├── save_data.json
├── requirements.txt
└── README.md
```

Count: **8 new files** plus updated imports in existing files. Nothing is broken. Your MVP still runs.

---

## What You Just Did (And Why It Matters)

You didn't write a single feature. But you:

1. **Prevented circular imports** by understanding the layer model
2. **Created architectural space** for every feature that's coming
3. **Verified everything imports** before writing business logic
4. **Migrated safely** by copying before deleting
5. **Preserved your working MVP** as the foundation

This is how professional projects scale. You don't delete and start over — you expand the container first, then fill it.

---

## ✅ Quality Gate

- [ ] All 8 new files exist (even if empty stubs)
- [ ] `python test_imports.py` passes (all imports clean)
- [ ] MVP content migrated to `levels_basics.py`
- [ ] All old imports updated (no references to `levels_mvp`)
- [ ] Existing tests pass: `python -m pytest tests/ -v`
- [ ] No circular import errors
- [ ] App still runs: `python main.py`

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Import errors everywhere | Missing stub file | Create it, even if empty |
| Circular import | Content file imports from engine | Remove that import, restructure |
| Tests fail after migration | Import path still points to old file | `grep -rn "levels_mvp" .` to find it |
| App crashes on startup | Main.py imports something that doesn't exist yet | Check your main.py imports |

---

**Phase 1 complete? Your foundation is ready. Now expand your data models → [phase2.md](phase2.md)**
