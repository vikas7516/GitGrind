# 🚀 PHASE 3 — Validator Upgrade

---

## 🎯 Goal

Upgrade your validator to handle all 8 exercise types, support placeholder-aware matching (so `git add <file>` matches `git add app.py`), and tolerate the `git ` prefix being present or absent.

The validator is the game's referee. If it rejects correct answers, the player feels cheated. If it accepts wrong ones, the player learns nothing. This phase makes it fair and robust.

> **Open `engine/validator.py` and follow along.** This guide walks through every function, explaining how it works and why it's designed that way.

---

## What You'll Learn

- How `functools.lru_cache` caches function results for performance
- How `re.escape()` protects literal strings inside regex patterns
- How to build dynamic regex patterns from templates
- Why variant-based matching eliminates frustrating false rejections
- How `.rstrip()` handles multiple valid input formats

---

## Step 1 — Understand the Problem

Your MVP validator does this:

```python
def check_answer(user_input, accepted_answers):
    cleaned = normalize(user_input)
    for answer in accepted_answers:
        if cleaned == normalize(answer):
            return (True, answer)
    return (False, None)
```

This works for exact matches like `"git init"`. But the full version has answers like:

```python
answers=["git add <file>"]    # Player could type "git add app.py" or "git add ."
answers=["git push <remote> <branch>"]  # "git push origin main"
```

Exact matching fails here — `"git add app.py" != "git add <file>"`.

You also need new validators:
- **fill_blank**: player types just the missing word (`"commit"` for `git ____ -m 'msg'`)
- **multi_choice**: player types a letter (`"b"` or `"b)"`)

---

## Step 2 — `normalize(text)` — Making Comparisons Fair

This is the most important function. Without it, `"GIT  INIT"` ≠ `"git init"` and the player feels cheated.

Open `engine/validator.py` and find `normalize()`. It does three things:

### 2.1 — Strip and Lowercase

```python
text = text.strip().lower()
```

`.strip()` removes leading/trailing whitespace: `"  git init  "` → `"git init"`. `.lower()` normalizes casing: `"GIT INIT"` → `"git init"`.

**Why `.strip()` first?** Because the player might press space before or after typing. This is the most common input quirk.

### 2.2 — Collapse Whitespace

```python
text = re.sub(r'\s+', ' ', text)
```

`re.sub(r'\s+', ' ', text)` replaces ANY run of whitespace (spaces, tabs, multiple spaces) with a single space. So `"git    init"` and `"git\tinit"` and `"git init"` all become `"git init"`.

**Why `\s+` (not just spaces)?** `\s` matches spaces, tabs, newlines, and other whitespace characters. `+` means "one or more." Together, `\s+` catches every possible whitespace variation in one regex.

### 2.3 — Smart Quote Replacement

```python
text = text.replace('\u201c', '"').replace('\u201d', '"')
text = text.replace('\u2018', "'").replace('\u2019', "'")
```

Some phones and keyboards auto-replace `"` with `"` or `"` (curly/smart quotes). These look identical to the player but are different Unicode characters. Without these lines, `git commit -m "fix"` typed on a phone would fail because the quotes are `\u201c` and `\u201d` instead of plain `"`.

**Unicode point reference:**

| Character | Unicode | Common Source |
|-----------|---------|---------------|
| `"` | `\u201c` | Left double smart quote |
| `"` | `\u201d` | Right double smart quote |
| `'` | `\u2018` | Left single smart quote |
| `'` | `\u2019` | Right single smart quote (also apostrophe on iOS) |

One line of normalization prevents thousands of frustrated players on mobile.

---

## Step 3 — `_strip_git_prefix(text)` — Handling Two Valid Formats

Find `_strip_git_prefix()` in the file:

```python
def _strip_git_prefix(text):
    if text.startswith("git "):
        return text[4:]     # "git init" → "init"
    return text              # "init" → "init" (unchanged)
```

When the answer is `"git init"`, BOTH of these should be correct:
- Player types `"git init"` → correct (exact match)
- Player types `"init"` → also correct (they know the command, just omitted `git`)

**How the variant system works:**

`check_answer` creates **variants** of both the user's input and each accepted answer:

```python
user_variants = {user_norm, _strip_git_prefix(user_norm)}
# If player typed "git init": {"git init", "init"}
# If player typed "init":     {"init", "init"} → {"init"}

answer_variants = {answer_norm, _strip_git_prefix(answer_norm)}
# For answer "git init": {"git init", "init"}
```

Then it checks if ANY user variant matches ANY answer variant. Using a `set` means Python checks membership in O(1) time — instantaneous even with many variants.

This creates a 2×2 matrix of comparisons without writing 4 separate `if` statements:

| | `"git init"` (answer) | `"init"` (answer stripped) |
|---|---|---|
| `"git init"` (user) | ✅ match | — |
| `"init"` (user stripped) | — | ✅ match |

---

## Step 4 — `_build_placeholder_regex(answer_norm)` — Dynamic Pattern Building

This is the most complex function. It converts an answer template like `"git push <remote> <branch>"` into a regex that matches `"git push origin main"`.

### Step-by-Step Walkthrough

```
Input: "git push <remote> <branch>"

Step 1: Split into tokens
  → ["git", "push", "<remote>", "<branch>"]

Step 2: Process each token
  "git"      → re.escape("git")      → "git"     (literal match)
  "push"     → re.escape("push")     → "push"    (literal match)
  "<remote>" → matches <...> pattern  → r"\S+"    (any non-whitespace word)
  "<branch>" → matches <...> pattern  → r"\S+"    (any non-whitespace word)

Step 3: Join with r"\s+" and wrap with anchors
  → r"^git\s+push\s+\S+\s+\S+$"

Step 4: Compile into regex object
  → re.compile(r"^git\s+push\s+\S+\s+\S+$")
```

### Why `re.escape()` on Literal Tokens?

`re.escape("file.txt")` returns `r"file\.txt"`. Without escaping, the `.` in `file.txt` would match ANY character in regex — so `"filextxt"` would match. `re.escape()` tells regex to treat special characters (`.`, `*`, `?`, etc.) as literal.

### Why `\S+` for Placeholders (Not `.*`)?

`\S+` matches exactly one word (any non-whitespace characters). `.*` would match EVERYTHING including multiple words and whitespace — so `"git push hello world foo bar"` would incorrectly match `"git push <remote>"`.

| Pattern | Matches | Doesn't Match |
|---------|---------|--------------|
| `\S+` | `origin`, `my-file.txt`, `feature/login` | `origin main` (two words) |
| `.*` | `origin`, `origin main extra` (too greedy) | Nothing — matches everything |

### How Placeholder Detection Works

```python
re.fullmatch(r"<[^>]+>", token)
```

This matches tokens that are EXACTLY `<something>` — starts with `<`, ends with `>`, with one or more non-`>` characters inside.

- `"<file>"` → matches ✅
- `"<remote>"` → matches ✅
- `"git"` → no match (no angle brackets)
- `"<>"` → no match (`[^>]+` requires at least one character)

### Why `@functools.lru_cache(maxsize=256)`?

```python
@functools.lru_cache(maxsize=256)
def _build_placeholder_regex(answer_norm):
```

`lru_cache` is a **memoization decorator** — it remembers the results of previous function calls. The first time you call `_build_placeholder_regex("git add <file>")`, it builds the regex and caches the result. The next 99 times you call it with the same argument, it returns the cached regex instantly.

**Why cache this function specifically?** Because `re.compile()` (building a regex from a string) is expensive relative to string comparison. The drill zone might check the same answer pattern dozens of times per session. Caching means you pay the compilation cost once per unique pattern.

**Why `maxsize=256`?** The game has ~200 exercises. 256 covers all unique answer patterns with room to spare. After 256 cached patterns, the **Least Recently Used** (LRU) one gets evicted — hence the name `lru_cache`.

**Important:** `lru_cache` only works on functions with **hashable** arguments. Strings are hashable ✅. Lists and dicts are NOT hashable ❌. That's why this function takes a string, not a list.

---

## Step 5 — `check_answer()` — The Full Flow

This is the main validator. Find `check_answer()` in the file and trace through its logic:

### Pass 1: Exact Match (Fast Path)

```python
for user_variant in user_variants:
    if user_variant in answer_variants:
        return True, answer
```

95% of exercises use simple answers like `"git init"`. Exact string comparison in a set is O(1) — essentially free. This handles the common case without running any regex.

### Pass 2: Placeholder Regex Match (Fallback)

```python
for answer_variant in answer_variants:
    regex = _build_placeholder_regex(answer_variant)
    if regex.match(user_norm):
        return True, answer
    if regex.match(_strip_git_prefix(user_norm)):
        return True, answer
```

Only runs if exact match failed — no point building regex patterns for `"git init"`.

**Why check both `user_norm` AND `_strip_git_prefix(user_norm)` against the regex?**

Because the answer might be `"add <file>"` (no git prefix) and the user typed `"git add app.py"` (with git prefix). Checking both variants ensures the git-prefix tolerance works with placeholder matching too.

### Return (False, None)

If nothing matched across any accepted answer, the input is wrong. The tuple `(False, None)` tells the caller: "wrong answer, no match found." The `None` is important — the runner displays the canonical answer (`accepted_answers[0]`) when showing the correct answer, not the matched variant.

---

## Step 6 — `check_fill_blank()` and `check_multi_choice()`

### Fill-in-the-blank

```python
def check_fill_blank(user_input, accepted_answers):
    user_norm = normalize(user_input)
    for answer in accepted_answers:
        if user_norm == normalize(answer):
            return True, answer
    return False, None
```

The UI shows `git ____ -m 'message'` and the player types just `"commit"`. The accepted answer is `["commit"]`. This is just normalized string matching — no git-prefix stripping (the player isn't typing a full command), no placeholders (the blank IS the placeholder).

### Multiple Choice

```python
def check_multi_choice(user_input, correct_letter):
    user_norm = normalize(user_input).strip().rstrip(')')
    correct_norm = normalize(correct_letter).strip().rstrip(')')
    return user_norm == correct_norm, correct_letter
```

The player sees options like `a) git add`, `b) git commit`, `c) git push`. They can type `"b"`, `"b)"`, `"B)"`, or `" B ) "` — all should match.

**Why `.rstrip(')')` on BOTH sides?** Because the correct answer might be stored as `"b"` or `"b)"` depending on how the content author wrote it. Stripping `)` from both the input and the answer makes the comparison robust regardless of format.

**Why does `check_multi_choice` take `correct_letter` (a string) instead of `accepted_answers` (a list)?** Because there's exactly ONE correct letter. The runner passes `exercise.answers[0]` — the first (and only) element of the answers list. This keeps the function signature simple.

---

## Step 7 — The Validation Dispatch

The runner needs ONE function that routes to the correct validator based on exercise type:

```python
# In engine/runner.py (you'll build this in Phase 5):
if exercise.type == "fill_blank":
    correct, matched = check_fill_blank(user_input, exercise.answers)
elif exercise.type == "multi_choice":
    correct, matched = check_multi_choice(user_input, exercise.answers[0])
else:
    # recall, scenario, error_fix, reverse, rapid_fire
    correct, matched = check_answer(user_input, exercise.answers)
```

**Why is this dispatch in `runner.py`, not `validator.py`?**

Because it depends on the `Exercise` model (from `content/models.py`). The validator is **pure logic** — it takes strings and lists, not domain objects. By keeping the dispatch in the runner, the validator stays a clean, testable utility with zero project dependencies.

**Why do 5 out of 8 types use the same `check_answer()` function?**

Because `recall`, `scenario`, `error_fix`, `reverse`, and `rapid_fire` all work the same way: the player types a command, we check it against accepted answers. Their difference is in the UI — how the question is displayed — not in validation. Type-specific validators only exist when the INPUT FORMAT is different (filling a blank vs. picking a letter).

---

## Step 8 — The Fairness Matrix

Your validator must live on this spectrum:

| Input | Expected | Why |
|-------|----------|-----|
| `GIT ADD .` | ✅ Pass | Case normalization |
| `git  add  .` | ✅ Pass | Whitespace collapsing |
| `init` for answer `git init` | ✅ Pass | Git-prefix tolerance |
| `git add app.py` for answer `git add <file>` | ✅ Pass | Placeholder matching |
| `git push origin main` for answer `git push <remote> <branch>` | ✅ Pass | Multi-placeholder |
| `git commit` for answer `git add` | ❌ Fail | Wrong command |
| `git add` for answer `git add <file>` | ❌ Fail | Missing argument |
| `b)` for correct `b` | ✅ Pass | Parenthesis tolerance |
| `COMMIT` for fill-blank `commit` | ✅ Pass | Case insensitive |

**Rule: Accept formatting variations. Reject semantic mistakes.** The player should never feel cheated by typo rejection, but should never get credit for the wrong command.

---

## ✅ Quality Gate

- [ ] `normalize()` handles case, whitespace, and smart quotes
- [ ] `check_answer()` handles exact match AND placeholder templates
- [ ] `_strip_git_prefix()` makes `"init"` match `"git init"`
- [ ] `_build_placeholder_regex()` is cached with `@lru_cache`
- [ ] `check_fill_blank()` compares just the blank portion
- [ ] `check_multi_choice()` handles `a`, `a)`, `A`
- [ ] All tests pass: `python -m pytest tests/ -v`

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Regex doesn't match anything | Print the pattern: `print(regex.pattern)` and compare visually |
| `re.escape()` adding backslashes | That's normal — `"file.txt"` becomes `r"file\.txt"` |
| Multi-choice always fails | Check that you're stripping `)` from BOTH sides |
| Fill-blank passes when it shouldn't | Make sure you're comparing just the blank, not the full command |
| `lru_cache` not working | The function must receive HASHABLE arguments — strings work, lists don't |

---

**Phase 3 complete? Now upgrade the state engine → [phase4.md](phase4.md)**
