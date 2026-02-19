# 🚀 PHASE 7 — Testing and Debugging

---

## 🎯 Goal

Make your game reliable. Write automated tests that catch bugs before your players do. Learn a debugging workflow that saves you hours.

---

## 🔹 Step 1 — Install pytest

pytest is the standard testing tool for Python. You already installed it (or should have):

```
pip install pytest
```

Check it works:

```
python -m pytest --version
```

You should see: `pytest 8.x.x`

---

## 🔹 Step 2 — Write Your First Test

Create a file called `tests/test_example.py`:

```python
def test_addition():
    assert 1 + 1 == 2

def test_string_upper():
    assert "hello".upper() == "HELLO"
```

Run it:

```
python -m pytest tests/test_example.py -v
```

**You should see:**

```
tests/test_example.py::test_addition PASSED
tests/test_example.py::test_string_upper PASSED

========== 2 passed ==========
```

### Understanding the basics:

| Concept | What It Means |
|---------|--------------|
| Test files are named `test_*.py` | pytest finds them automatically |
| Test functions start with `test_` | pytest runs them automatically |
| `assert something == expected` | If `something` doesn't equal `expected`, the test fails |
| `-v` flag | Verbose — shows each test name and result |
| `python -m pytest` | Runs pytest using your venv's Python (safer than just `pytest`) |

**Delete `tests/test_example.py`** — it was just for learning.

---

## 🔹 Step 3 — Write Validator Tests

Create `tests/test_validator.py`:

```python
"""Tests for the answer validator."""
from engine.validator import normalize, check_answer


# ── normalize() tests ──

def test_normalize_lowercase():
    """Input should be converted to lowercase."""
    assert normalize("GIT INIT") == "git init"

def test_normalize_strips_whitespace():
    """Leading and trailing spaces should be removed."""
    assert normalize("  git init  ") == "git init"

def test_normalize_collapses_spaces():
    """Multiple spaces between words should become one."""
    assert normalize("git   init") == "git init"

def test_normalize_empty_string():
    """Empty string should stay empty (not crash)."""
    assert normalize("") == ""


# ── check_answer() tests ──

def test_exact_match():
    """Exact answer should be correct."""
    correct, matched = check_answer("git init", ["git init"])
    assert correct is True
    assert matched == "git init"

def test_case_insensitive():
    """Answers should be case-insensitive."""
    correct, _ = check_answer("GIT INIT", ["git init"])
    assert correct is True

def test_extra_spaces():
    """Extra spaces should be tolerated."""
    correct, _ = check_answer("git  init", ["git init"])
    assert correct is True

def test_wrong_answer():
    """Wrong answer should be rejected."""
    correct, _ = check_answer("git status", ["git init"])
    assert correct is False

def test_multiple_accepted_answers():
    """Any of the accepted answers should be correct."""
    correct, _ = check_answer("git init .", ["git init", "git init ."])
    assert correct is True

def test_empty_input():
    """Empty input should be wrong, not crash."""
    correct, _ = check_answer("", ["git init"])
    assert correct is False
```

Run:

```
python -m pytest tests/test_validator.py -v
```

**You should see 8 tests, all PASSED (green).**

If any test fails:
- Read the error message — it tells you exactly what went wrong
- Fix the **code** in `engine/validator.py`, not the test
- Unless the test itself has a typo (re-read it carefully)

---

## 🔹 Step 4 — Write State Tests

Create `tests/test_state.py`:

```python
"""Tests for the game state engine."""
from engine.state import GameState


def test_fresh_accuracy_no_crash():
    """Fresh state should have 0% accuracy (no division by zero!)."""
    state = GameState()
    assert state.accuracy == 0.0

def test_record_correct():
    """Recording a correct answer should update stats."""
    state = GameState()
    state.record_correct()
    assert state.data["stats"]["correct"] == 1

def test_record_wrong():
    """Recording a wrong answer should update stats."""
    state = GameState()
    state.record_wrong()
    assert state.data["stats"]["wrong"] == 1

def test_accuracy_calculation():
    """Accuracy should be correct percentage."""
    state = GameState()
    state.record_correct()
    state.record_correct()
    state.record_wrong()
    # 2 out of 3 = 66.7%
    assert 66.0 < state.accuracy < 67.0

def test_clear_stage():
    """Clearing a stage should update cleared list and advance index."""
    state = GameState()
    state.clear_stage(0)
    assert 0 in state.cleared_stages
    assert state.current_stage_index == 1

def test_clear_stage_no_duplicates():
    """Clearing the same stage twice should not add duplicates."""
    state = GameState()
    state.clear_stage(0)
    state.clear_stage(0)
    assert state.cleared_stages.count(0) == 1

def test_reset():
    """Reset should clear all progress."""
    state = GameState()
    state.record_correct()
    state.clear_stage(0)
    state.reset()
    assert state.current_stage_index == 0
    assert state.accuracy == 0.0
    assert len(state.cleared_stages) == 0
```

Run:

```
python -m pytest tests/test_state.py -v
```

**You should see 7 tests, all PASSED.**

---

## 🔹 Step 5 — Write Content Integrity Tests

These tests check that your game content is valid — no missing explanations, no empty answer lists.

Add this to a new file `tests/test_content.py`:

```python
"""Tests for game content integrity."""
from content.levels_mvp import LEVELS
from content.stage_map import STAGE_MAP


def test_all_exercises_have_explanations():
    """Every exercise must have an explanation for wrong answers."""
    for key, level in LEVELS.items():
        for i, ex in enumerate(level.exercises):
            assert ex.explanation, (
                f"Level {level.number} ({level.name}), "
                f"exercise {i+1} is missing an explanation!"
            )

def test_all_exercises_have_answers():
    """Every exercise must have at least one accepted answer."""
    for key, level in LEVELS.items():
        for i, ex in enumerate(level.exercises):
            assert len(ex.answers) > 0, (
                f"Level {level.number} ({level.name}), "
                f"exercise {i+1} has no answers!"
            )

def test_stage_map_references_valid_levels():
    """Every stage must point to a level that exists."""
    for i, stage in enumerate(STAGE_MAP):
        assert stage.data_key in LEVELS, (
            f"Stage {i} ({stage.label}) references Level "
            f"{stage.data_key} which doesn't exist in LEVELS!"
        )
```

Run ALL tests at once:

```
python -m pytest tests/ -v
```

**You should see all tests PASSED:**

```
tests/test_content.py::test_all_exercises_have_explanations PASSED
tests/test_content.py::test_all_exercises_have_answers PASSED
tests/test_content.py::test_stage_map_references_valid_levels PASSED
tests/test_state.py::test_fresh_accuracy_no_crash PASSED
tests/test_state.py::test_record_correct PASSED
...
========== 18 passed ==========
```

---

## 🔹 Step 6 — Manual Smoke Test

Automated tests can't test everything (like UI display). Run through this checklist by hand:

```
1. Delete save_data.json
2. Run python main.py
3. Press C → should start Setup stage
4. Complete Setup (answer all exercises)
5. Press C → should start Level 1 (not Setup again!)
6. Get one answer wrong on purpose → should see ❌ + explanation
7. Type "hint" on another exercise → should see hint
8. Complete Level 1
9. Press Q → should say "Progress saved"
10. Run python main.py again
11. Press C → should resume at Level 2 (not restart!)
12. Complete Level 2
13. Press C → should say "You've completed all stages!"
14. Check that save_data.json exists and has correct data
```

If any step fails, fix it before moving on.

---

## 🔹 Step 7 — The Debug Workflow

When you find a bug, always follow these four steps in order:

```
1. REPRODUCE  — Make it happen again. Note the exact steps.
2. ISOLATE    — Find the smallest piece of code that causes it.
3. FIX        — Change the smallest amount of code possible.
4. TEST       — Write a test that catches this bug.
```

Step 4 is crucial. If you don't write the test, the bug WILL come back.

---

## ✅ Checklist (Don't Move On Until)

- [ ] `python -m pytest tests/ -v` → all tests pass (green)
- [ ] Validator tests: 8 passing
- [ ] State tests: 7 passing
- [ ] Content tests: 3 passing
- [ ] Manual smoke test: all 14 steps pass
- [ ] No crash paths in normal usage

---

## 🛟 If Something Goes Wrong

**"ModuleNotFoundError" when running tests**
→ Run `python -m pytest` from the project root folder, not from inside `tests/`.

**A test passes when it should fail**
→ Double-check your assert. `assert True` always passes. Make sure you're testing the right thing.

**One fix breaks something else**
→ Run the full test suite after EVERY fix, not just the affected test.

---

**Phase 7 done? Your app works and is tested. Time to polish and ship → [phase8.md](phase8.md)**
