# 🚀 PHASE 10 — Testing, Hardening & Release

---

## 🎯 Goal

Write the test suite, fix edge cases, and ship a robust game.

You've built a complex system with state persistence, input validation, and game loops. Now you need to prove it works — and keep it working when you change things.

> **Open `tests/test_core.py` to follow along.**

---

## What You'll Learn

- **Dependency Injection**: How to test file saving without overwriting your real save.
- **Idempotency**: Ensuring `clear_stage(1)` called twice doesn't break the game.
- **Edge Case Hardening**: Validating whitespace, casing, and weird inputs.
- **Distribution**: How to package your Python script as a standalone `.exe`.

---

## Step 1 — Testing the Validator

The validator is the core mechanic. If it's flaky, the game is frustrating. We test it with `pytest`.

### Normalization Logic

```python
def test_normalize_basic():
    assert normalize("  Git Init  ") == "git init"
    assert normalize("GIT STATUS") == "git status"
```

**Why test this?** Punctuation and casing are common user errors. If "Git Init" fails, the player feels cheated.

### Fuzzy Matching

```python
def test_check_answer_multiple_accepted():
    # Both should work
    assert check_answer("git add .", ["git add .", "git add -A"])[0] is True
    assert check_answer("git add -A", ["git add .", "git add -A"])[0] is True
```

**Why test this?** Git has aliases. We explicitly allow multiple correct answers to be fair.

---

## Step 2 — Testing Game State (The Tricky Part)

Testing `GameState` is hard because it reads/writes files. We don't want tests to delete your actual save file!

### mocking `SAVE_FILE`

We use `unittest.mock.patch` to redirect the save path **only during the test**.

```python
from unittest.mock import patch
import tempfile

def test_save_and_load():
    # Create a temporary directory that cleans itself up
    with tempfile.TemporaryDirectory() as tmpdir:
        fake_save = os.path.join(tmpdir, "test_save.json")
        
        # MAGIC: Redirect 'engine.state.SAVE_FILE' to our fake path
        with patch('engine.state.SAVE_FILE', fake_save):
            state = GameState()
            state.save()  # Writes to fake_save
            assert os.path.exists(fake_save)
```

**Why usage `tempfile`?**
It guarantees a clean environment for every test run. No leftover files from previous runs = no flaky tests.

### Idempotency

```python
def test_clear_stage_idempotent():
    state = GameState()
    state.clear_stage(0)
    state.clear_stage(0)  # Call it again
    assert state.cleared_stages.count(0) == 1  # Should still be 1, not 2
```

**Why test this?**
Logic bugs often call functions multiple times. If `cleared_stages` had `[0, 0]`, the progress bar calculation might show >100%. Idempotency protects against this.

---

## Step 3 — Hardening Checklist

Before releasing, verify these specific edge cases:

### 1. The "Infinite Loop" Guard
In `main.py`, the boss retry loop has a safety brake:
```python
MAX_ITERATIONS = 100
while iterations < MAX_ITERATIONS:
```
**Verify:** Intentionally break the retry logic (make it always return False). Confirm the game dumps you out after 100 tries instead of hanging forever.

### 2. The Atomic Save
In `engine/state.py`:
```python
def _atomic_write_json(path, data):
    fd, temp_path = tempfile.mkstemp(...)
    # ... write ...
    os.replace(temp_path, path)
```
**Verify:** Kill the process *while* it's saving (simulated). The save file should either be the old valid one or the new valid one — never a half-written corrupt file.

### 3. The Mercy Rule
In `main.py`:
```python
if boss_attempts >= 5:
    # Show "Skip" option
```
**Verify:** Fail a boss 5 times. Does the "Skip" option appear? Does choosing it advance the stage counter?

---

## Step 4 — Bonus: Distribution with PyInstaller

You've built a game. Now share it with friends who don't have Python installed.

We use **PyInstaller** to bundle everything into one `.exe`.

### 1. Install PyInstaller
```bash
pip install pyinstaller
```

### 2. Build the Executable
Run this command in the project root:

```bash
pyinstaller --onefile --name "GitGrind" --add-data "content;content" main.py
```

-   `--onefile`: Bundles everything into a single `.exe` file.
-   `--name "GitGrind"`: Names your executable.
-   `--add-data "content;content"`: Tells PyInstaller to include your `content/` folder inside the exe (crucial for `notebook.py` and `glossary.py` data).

### 3. Run It
Look in the `dist/` folder. You'll see `GitGrind.exe`. You can send this file to anyone on Windows, and it will run instantly.

> **Note:** Because we use `winsound`, the exe will strictly be Windows-only. To support Mac/Linux, you'd need to replace `winsound` with a cross-platform library or rely on the silent fallback we wrote in Phase 8.

---

## 🎓 Conclusion

You have built a complete, robust, architectural software project.

-   **Phase 1-2**: You designed the data models and file structure.
-   **Phase 3-6**: You built the engine (Validator, State, Runner, Main).
-   **Phase 7**: You added a professional UI layer.
-   **Phase 8**: You added polish (Sound, Notebook).
-   **Phase 9**: You authored the curriculum.
-   **Phase 10**: You hardened it with tests and packaged it for release.

This is exactly how professional software is built. You didn't just write a script; you engineered a system.

**Keep grinding. 🚀**
