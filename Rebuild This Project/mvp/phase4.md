# 🚀 PHASE 4 — Answer Validator (Is The Answer Correct?)

---

## 🎯 Goal

Build the function that checks if the player's answer is correct. This is the core game logic — get it wrong, and the game feels broken.

You'll build two functions:
- `normalize()` — cleans up text for comparison
- `check_answer()` — checks if the input matches any accepted answer

---

## 🔹 Step 1 — Understand Why You Need Normalization

The player types `"  GIT  INIT  "`. The correct answer is `"git init"`. Are they the same?

To a human: yes, obviously. To a computer: **no**. These are different strings:

```python
"  GIT  INIT  " == "git init"   # False — different!
```

They differ in:
- **Case:** `GIT` vs `git`
- **Leading/trailing spaces:** `"  GIT..."` vs `"git..."`
- **Multiple spaces:** `"GIT  INIT"` vs `"git init"`

Normalization means converting both strings to the same format before comparing. After normalization:

```
"  GIT  INIT  " → "git init"
"git init"      → "git init"
Now they match! ✅
```

---

## 🔹 Step 2 — Build `normalize()` (`engine/validator.py`)

Create `engine/validator.py` and write this:

```python
"""
GitGrind — Answer validation.
Checks if player input matches accepted answers.
"""
import re


def normalize(text):
    """
    Clean up text for fair comparison.

    What it does:
    1. Strips spaces from both ends
    2. Converts everything to lowercase
    3. Collapses multiple spaces into one
    4. Replaces "smart quotes" with regular quotes

    Example:
        normalize("  GIT  INIT  ") → "git init"
    """
    text = text.strip()             # "  GIT  INIT  " → "GIT  INIT"
    text = text.lower()             # "GIT  INIT" → "git  init"
    text = re.sub(r"\s+", " ", text)  # "git  init" → "git init"

    # Smart quotes → regular quotes
    # (Some keyboards/phones auto-replace " with " or ")
    text = text.replace("\u201c", '"')    # Left smart quote  " → "
    text = text.replace("\u201d", '"')    # Right smart quote " → "
    text = text.replace("\u2018", "'")    # Left single quote ' → '
    text = text.replace("\u2019", "'")    # Right single quote ' → '

    return text
```

### Understanding each line:

| Line | What It Does | Example |
|------|-------------|---------|
| `text.strip()` | Removes spaces from start and end | `"  hello  "` → `"hello"` |
| `text.lower()` | Makes everything lowercase | `"GIT INIT"` → `"git init"` |
| `re.sub(r"\s+", " ", text)` | Replaces 1 or more spaces with exactly 1 | `"git   init"` → `"git init"` |

### What is `re.sub()`?

`re` is Python's "regular expressions" module. Regular expressions are patterns for matching text.

- `re.sub(pattern, replacement, text)` = "find the pattern, replace it"
- `\s` means "any whitespace character" (space, tab, etc.)
- `+` means "one or more"
- So `\s+` = "one or more whitespace characters"
- `re.sub(r"\s+", " ", text)` = "replace any chunk of whitespace with a single space"

The `r` before the string (`r"\s+"`) means "raw string" — it tells Python not to treat backslashes specially. Without it, `\s` might be interpreted as an escape code.

---

## 🔹 Step 3 — Build `check_answer()`

Add this function to `engine/validator.py`:

```python
def check_answer(user_input, accepted_answers):
    """
    Check if the user's input matches any accepted answer.

    Args:
        user_input: What the player typed (raw, not yet normalized)
        accepted_answers: List of acceptable answer strings

    Returns:
        A tuple of (is_correct, matched_answer):
        - (True, "git init")  if the input matched "git init"
        - (False, None)       if no match was found

    Example:
        check_answer("GIT INIT", ["git init", "git init ."])
        → (True, "git init")
    """
    # Normalize what the user typed
    cleaned = normalize(user_input)

    # Compare against each accepted answer
    for answer in accepted_answers:
        if cleaned == normalize(answer):
            return (True, answer)

    # No match found
    return (False, None)
```

### Understanding the code:

1. Normalize the user's input once
2. Loop through every accepted answer
3. Normalize each accepted answer and compare
4. If ANY answer matches → return `(True, that_answer)`
5. If none match → return `(False, None)`

### Why return a tuple?

A tuple is just two values packed together. You can "unpack" them:

```python
is_correct, matched = check_answer("git init", ["git init"])

# is_correct = True
# matched = "git init"

if is_correct:
    print(f"You got it! Matched: {matched}")
```

This lets the caller know BOTH whether it was correct AND which answer it matched.

---

## 🔹 Step 4 — Test Your Validator

Add this at the bottom of `engine/validator.py`:

```python
# Temporary test — delete this later
if __name__ == "__main__":
    # Test normalize
    print("=== Testing normalize ===")
    print(f"'  GIT  INIT  ' → '{normalize('  GIT  INIT  ')}'")
    print(f"'git init'      → '{normalize('git init')}'")
    print(f"''              → '{normalize('')}'")
    print()

    # Test check_answer — should be correct
    print("=== Testing check_answer ===")

    result, matched = check_answer("git init", ["git init"])
    print(f"'git init' vs ['git init'] → Correct: {result}, Matched: {matched}")

    result, matched = check_answer("GIT INIT", ["git init"])
    print(f"'GIT INIT' vs ['git init'] → Correct: {result}, Matched: {matched}")

    result, matched = check_answer("  git  init  ", ["git init"])
    print(f"'  git  init  ' vs ['git init'] → Correct: {result}, Matched: {matched}")

    result, matched = check_answer("git init .", ["git init", "git init ."])
    print(f"'git init .' vs ['git init', 'git init .'] → Correct: {result}, Matched: {matched}")

    # Test check_answer — should be wrong
    result, matched = check_answer("git status", ["git init"])
    print(f"'git status' vs ['git init'] → Correct: {result}, Matched: {matched}")

    result, matched = check_answer("", ["git init"])
    print(f"'' vs ['git init'] → Correct: {result}, Matched: {matched}")
```

Run:

```
python engine/validator.py
```

**You should see:**

```
=== Testing normalize ===
'  GIT  INIT  ' → 'git init'
'git init'      → 'git init'
''              → ''

=== Testing check_answer ===
'git init' vs ['git init'] → Correct: True, Matched: git init
'GIT INIT' vs ['git init'] → Correct: True, Matched: git init
'  git  init  ' vs ['git init'] → Correct: True, Matched: git init
'git init .' vs ['git init', 'git init .'] → Correct: True, Matched: git init .
'git status' vs ['git init'] → Correct: False, Matched: None
'' vs ['git init'] → Correct: False, Matched: None
```

Every "Correct" should be True for the first 4, and False for the last 2.

**If your output doesn't match, check:**
- Did you import `re` at the top?
- Is `normalize()` called on BOTH sides (user input AND accepted answer)?

**Delete the test code** when all tests pass.

---

## 🔹 Step 5 — Why This Matters

The validator is what makes the game feel FAIR or UNFAIR. Imagine:

| Input | Answer | Without normalize | With normalize |
|-------|--------|-------------------|---------------|
| `"git init"` | `"git init"` | ✅ Match | ✅ Match |
| `"Git Init"` | `"git init"` | ❌ Wrong! | ✅ Match |
| `"  git init  "` | `"git init"` | ❌ Wrong! | ✅ Match |
| `"git  init"` | `"git init"` | ❌ Wrong! | ✅ Match |

Without normalization, the player would constantly get "wrong" for answers that are clearly right. They'd blame your app and stop playing. Normalization makes the game forgiving where it should be.

---

## ✅ Checklist (Don't Move On Until)

- [ ] `normalize()` handles extra spaces, case, and smart quotes
- [ ] `check_answer()` returns `(True, matched)` for correct answers
- [ ] `check_answer()` returns `(False, None)` for wrong answers
- [ ] Multiple accepted answers work (e.g., `["git init", "git init ."]`)
- [ ] Empty input returns `(False, None)` — doesn't crash
- [ ] All test cases pass with expected output

---

## 🛟 If Something Goes Wrong

**"ModuleNotFoundError: No module named 're'"**
→ `re` is built into Python — you don't install it. Just add `import re` at the top. If you still get this error, your Python installation may be broken.

**Correct answers showing as wrong**
→ Make sure you normalize BOTH sides: `normalize(user_input)` and `normalize(answer)`. If you only normalize one side, they won't match.

**Smart quotes still not matching**
→ Check that the hex codes are correct: `\u201c`, `\u201d`, `\u2018`, `\u2019`.

---

**Phase 4 done? You can check answers! Now build the save system → [phase5.md](phase5.md)**
