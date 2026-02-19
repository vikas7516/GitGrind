# 🚀 PHASE 5 — The Runner Engine

---

## 🎯 Goal

Build the runner — the engine that drives ALL gameplay. It handles running exercises (with retry loops), levels (teach → practice → drill), exercise rounds (grinding sessions), boss fights (fail-fast chains), and the setup intro.

The runner is the single most complex file. But its complexity comes from handling edge cases gracefully — the core logic is simple loops.

> **Open `engine/runner.py` and follow along.** This guide walks through every function, every design decision, and every edge case.

---

## What You'll Learn

- How `QUIT_SENTINEL` propagates graceful exits through nested function calls
- How `difflib.SequenceMatcher` powers near-miss ("almost right!") detection
- How the retry loop balances learning with frustration prevention
- How `_build_pool` creates spaced repetition from limited question banks
- Why boss fights use fail-fast design (one wrong = restart)
- How `save_fn` pattern enables interrupt-safe saves

---

## Step 1 — The Sentinel Pattern

Find `QUIT_SENTINEL` at the top of `engine/runner.py`:

```python
QUIT_SENTINEL = "__QUIT__"
```

### Why Not Just Return `None` or `False`?

The exercise runner returns multiple things:
- `True` = answered correctly
- `False` = skipped (counts as wrong)
- Need a third option: player typed "quit"

If "quit" returned `False`, the caller would treat it as a skip and continue to the next exercise. The player would NEVER be able to exit to the menu.

If "quit" returned `None`, you'd need `if result is None` everywhere (not `if not result`, since `None` is falsy like `False`).

A sentinel string is **unambiguous**:

```python
result = run_exercise(exercise, state)
if result == QUIT_SENTINEL:
    return QUIT_SENTINEL  # propagate upward
```

### How Sentinel Propagation Works

When the player types "quit" deep inside a retry loop, the quit signal must bubble up through every nested function call:

```
main.py
  └── run_level()
        └── run_exercise()
              └── _retry_loop()
                    └── user types "quit"
                          └── return QUIT_SENTINEL  ← starts here
                    return QUIT_SENTINEL  ← propagates up
              if result == QUIT_SENTINEL:
                  return QUIT_SENTINEL    ← propagates up
        if result == QUIT_SENTINEL:
            return QUIT_SENTINEL          ← propagates up
  # back in main.py — return to menu
```

Every function checks for `QUIT_SENTINEL` and passes it upward. This is called **sentinel propagation** — the value acts as a signal that travels up the call stack.

---

## Step 2 — Near-Miss Detection

Find `_analyze_near_miss()` in the file. This is what makes feedback intelligent instead of just "Wrong! Try again."

### How `difflib.SequenceMatcher` Works

```python
ratio = difflib.SequenceMatcher(None, user_norm, answer_norm).ratio()
```

`SequenceMatcher` compares two strings and returns a similarity ratio between `0.0` (completely different) and `1.0` (identical). It finds the longest common subsequences — similar to how `git diff` works.

| User Typed | Correct Answer | Ratio | Meaning |
|-----------|---------------|-------|---------|
| `"git init"` | `"git init"` | 1.0 | Perfect match |
| `"git innit"` | `"git init"` | 0.9 | Typo (extra 'n') |
| `"git add"` | `"git add ."` | 0.86 | Missing argument |
| `"git status"` | `"git init"` | 0.55 | Different command |
| `"hello"` | `"git init"` | 0.15 | Completely wrong |

### The Detection Tiers

The function uses ratio thresholds to decide what kind of feedback to give:

```
Ratio < 0.4  → Not even close → return None (no useful hint)
Ratio ≥ 0.4  → "Not far off — rethink your approach"
Ratio ≥ 0.6  → "Close! Your answer is on the right track"
Ratio ≥ 0.8  → "Almost! Tiny fix needed: <specific diff>"
```

### Getting Specific Diffs (ratio ≥ 0.8)

When the answer is VERY close (≥ 0.8), the function shows exactly what's wrong:

```python
sm = difflib.SequenceMatcher(None, user_norm, best_answer_norm)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "replace":
        diff_parts.append(f"'{user_norm[i1:i2]}' → '{best_answer_norm[j1:j2]}'")
    elif tag == "delete":
        diff_parts.append(f"remove '{user_norm[i1:i2]}'")
    elif tag == "insert":
        diff_parts.append(f"add '{best_answer_norm[j1:j2]}'")
```

**What is `get_opcodes()`?**

It returns a list of operations needed to transform the user's input into the correct answer. Each operation is `(tag, i1, i2, j1, j2)`:

| Tag | Meaning | Example |
|-----|---------|---------|
| `"equal"` | Characters match | `"git "` in both strings |
| `"replace"` | Characters differ | `"innit"` → `"init"` |
| `"delete"` | User has extra characters | Remove `"x"` |
| `"insert"` | User is missing characters | Add `"."` |

**Example walkthrough:**

```
User typed:   "git innit"
Correct:      "git init"

get_opcodes() returns:
  ("equal",   0, 4, 0, 4)   → "git " matches
  ("replace", 4, 9, 4, 8)   → "innit" → "init"

Output: "Almost! Tiny fix needed: 'innit' → 'init'"
```

### Substring Checks (Partial Answers)

After the ratio tiers, the function checks for partial matches:

```python
if best_answer_norm.startswith(user_norm):
    return "You're on the right track but missing something at the end"

if best_answer_norm.endswith(user_norm):
    return "Incomplete — you're missing the beginning part"

if user_norm in best_answer_norm:
    return "Getting closer! Your answer is part of it, but incomplete"

if best_answer_norm in user_norm:
    return "Too much! You added extra parts"
```

| User Typed | Correct | Detection | Message |
|-----------|---------|-----------|---------|
| `"git add"` | `"git add ."` | `startswith` | Missing something at the end |
| `"commit -m 'fix'"` | `"git commit -m 'fix'"` | `endswith` | Missing the beginning |
| `"add"` | `"git add ."` | `in` (user in answer) | Part of it, incomplete |
| `"git add . --verbose"` | `"git add ."` | `in` (answer in user) | Added extra parts |

### Why `[:2]` Limit on Diff Parts?

```python
fix_hint = ", ".join(diff_parts[:2])  # max 2 changes shown
```

More than 2 differences means the answer is fundamentally different, not just a typo. Showing 5+ string operations would confuse more than help.

---

## Step 3 — The Retry Loop

Find `_retry_loop()` in the file. This is the core learning mechanic — the player must keep trying until correct (or skip).

### The Flow

```
Player answers wrong
  │
  ├── Show wrong feedback + near-miss analysis
  │
  └── While True:
        ├── wrong_count++
        │
        ├── If wrong_count ≥ 2: show "skip" ghost hint
        │
        ├── Get next input
        │
        ├── "quit" → return QUIT_SENTINEL
        │
        ├── "skip" (if unlocked) → show answer + return False
        │
        ├── "hint" → show hint, continue (don't count as wrong)
        │
        ├── Validate
        │   ├── Correct → return True
        │   └── Wrong → show near-miss feedback, loop again
```

### Why Require 2 Wrong Attempts Before Skip?

```python
SKIP_UNLOCK_RETRIES = 2
```

This prevents the pattern: "I don't know → skip → I don't know → skip → I don't know → skip." The player who never tries never learns.

By requiring 2 genuine attempts before revealing the skip option, you ensure:
1. The player has actually tried
2. The near-miss hints have had a chance to help
3. Skipping is a last resort, not a first choice

The skip hint appears as a ghost (dimmed text) so it doesn't look like a button — it's a safety valve, not the expected path.

### Why Don't Retries Re-Record Wrong Stats?

```python
# Don't re-record wrong stats — was already recorded on first wrong attempt
```

If every retry counted as a separate wrong answer, a player who tried 5 times before getting it right would show 4 wrong + 1 correct = 20% accuracy on that question. In reality, they learned — they should show 1 wrong + 1 correct = 50% for that attempt.

Stats are recorded ONCE on first wrong, then only the retry outcome matters.

### The `save_fn` Pattern

```python
save_fn = state.save
user_input = ui.get_input(save_fn=save_fn)
```

**Why pass `state.save` as a parameter?**

`ui.get_input()` wraps `console.input()` in a `try/except KeyboardInterrupt`. When the player presses Ctrl+C:

```python
# Inside ui.get_input():
try:
    user_input = console.input(">>> ")
except (KeyboardInterrupt, EOFError):
    if save_fn:
        save_fn()  # Save progress before exiting!
    return "quit"
```

By passing the save function, the UI can save progress even during an abrupt Ctrl+C — without importing or knowing about the state module (maintaining the layer boundary from Phase 1).

---

## Step 4 — `run_exercise()` — The Core Function

Find `run_exercise()` in the file. This is the function that everything else calls.

### Parameters Explained

```python
def run_exercise(exercise, state, index=None, total=None, allow_hint=True, record_stats=True):
```

| Parameter | Purpose | Default |
|-----------|---------|---------|
| `exercise` | The Exercise object to run | Required |
| `state` | GameState for recording stats | Required |
| `index` | Current question number (for display "3/10") | `None` |
| `total` | Total questions (for display "3/10") | `None` |
| `allow_hint` | Whether typing "hint" shows a hint | `True` |
| `record_stats` | Whether correct/wrong counts are recorded | `True` |

**Why are `allow_hint` and `record_stats` configurable?**

Different contexts need different behavior:

| Context | `allow_hint` | `record_stats` | Why |
|---------|-------------|----------------|-----|
| Level exercises | `True` | `True` | Learning mode — hints help |
| Drill zone | `False` | `True` | Testing mode — no hints on tests |
| Exercise rounds | `False` | `True` | Grinding mode — challenge yourself |
| Boss fights | `False` | `True` | Prove mastery — no help |
| Setup intro | `True` | `False` | Tutorial — don't pollute stats |

### Multi-Step Exercise Handling

```python
if exercise.type == "multi_step" and exercise.steps:
    any_skipped = False
    for si, step in enumerate(exercise.steps, 1):
        # ... run each step
        if not result:
            any_skipped = True
        # Continue to next step regardless
    return not any_skipped
```

**Key decision: continue even if a step is skipped.** In a multi-step exercise like "Set up a Git repo" (init → add → commit), failing step 1 doesn't mean you can't attempt step 2. Each step is independent knowledge.

**Why `return not any_skipped`?** If any step was skipped, the whole exercise counts as "not passed" (`False`). If all steps were correct (even if some needed retries), it counts as passed (`True`).

### Streak Display

```python
if state.current_streak >= 3:
    ui.show_streak(state.current_streak)
```

Streaks below 3 aren't notable enough to display. The threshold prevents visual clutter for trivial streaks (getting 2 easy questions right sequentially).

---

## Step 5 — `run_level()` — The Four-Phase Flow

Find `run_level()`. A level has four distinct phases:

```
Phase 1: Teaching slides  → learn the concepts
Phase 2: Exercises        → guided practice
Phase 3: Quick recap      → refresh before test
Phase 4: Drill zone       → must score ≥ threshold to pass
```

### Phase 1: Teaching Slides

```python
if level.teachings:
    ui.show_lesson_intro(level)
    for i, teaching in enumerate(level.teachings, 1):
        ui.show_teaching(teaching, i, len(level.teachings))
        state.add_notebook_entry(teaching)
    state.save()
```

**Why save after ALL teachings, not after each?** I/O is expensive. Saving once after the teaching phase completes is more efficient than saving 5 times (one per teaching). If the player quits mid-teaching (Ctrl+C), the `save_fn` pattern saves progress anyway.

**Why `if level.teachings`?** The setup intro level has exercises but no teachings. Without this check, calling `show_lesson_intro` on an empty list would show a "Lessons" header with nothing under it.

### Phase 2: Exercises (No Pass/Fail)

```python
for i, ex in enumerate(level.exercises, 1):
    result = run_exercise(ex, state, i, len(level.exercises))
    if result == QUIT_SENTINEL:
        return QUIT_SENTINEL
```

Notice: **no pass/fail tracking.** Exercises are for learning. The player can skip all of them and still proceed to drills. The drill zone is where pass/fail matters.

### Phase 4: Drill Zone

```python
required, total = level.drill_pass
drills = _build_pool(level.drills, total)
correct_count = 0
wrong_count = 0

for i, drill in enumerate(drills, 1):
    result = run_exercise(drill, state, i, total, allow_hint=False)
    if result:
        correct_count += 1
    else:
        wrong_count += 1

if correct_count >= required:
    state.learn_commands(level.commands_taught)
    return True
else:
    return False
```

**Why `allow_hint=False` in drills?** Drills test retention. Hints defeat the purpose — if you need a hint, you haven't learned the command yet.

**Why `learn_commands()` only on pass?** The notebook tracks which commands you've mastered. If you fail the drill, you haven't demonstrated mastery yet.

---

## Step 6 — `_build_pool()` — Spaced Repetition Builder

Find `_build_pool()` at the bottom of the file:

```python
def _build_pool(items, total):
    pool = list(items)
    if not pool:
        return []
    if len(pool) < total:
        pool = list(itertools.islice(itertools.cycle(pool), total))
    random.shuffle(pool)
    return pool[:total]
```

### Step-by-Step Walkthrough

```
Input: items = [Q1, Q2, Q3], total = 10

Step 1: pool = [Q1, Q2, Q3]              → 3 items
Step 2: len(pool) < 10 → true
Step 3: cycle → Q1,Q2,Q3,Q1,Q2,Q3,Q1,Q2,Q3,Q1  → 10 items (repeats)
Step 4: shuffle → [Q3,Q1,Q2,Q1,Q3,Q2,Q1,Q2,Q3,Q1]  → randomized
Step 5: [:10] → all 10 items (already exactly 10)
```

**Why repeat items?** A level might only have 5 drill questions, but `drill_pass = (8, 10)` requires 10 questions. Repeating questions (in random order) ensures the player practices enough without requiring content authors to write excess questions.

**Why `itertools.cycle` + `itertools.islice`?**

`itertools.cycle(pool)` creates an infinite repeating iterator: `Q1,Q2,Q3,Q1,Q2,Q3,...` forever.

`itertools.islice(..., total)` takes exactly `total` items from that infinite stream and stops.

This is more memory-efficient than `pool * 4` (which creates a full list immediately). For 10 items it doesn't matter, but it's the correct pattern.

**Why shuffle?** Without shuffling, the player would see Q1→Q2→Q3→Q1→Q2→Q3... The pattern makes memorization too easy. Randomization forces genuine recall.

**Why `[:total]` at the end?** If `len(pool)` started at 8 and `total` is 10, after cycling we have 10. But if `len(pool)` started at 15 and `total` is 10, after shuffling we take only the first 10. The slice guarantees exactly `total` items.

---

## Step 7 — Boss Fight Runner

Find `run_boss_fight()`:

```python
def run_boss_fight(boss, state):
    ui.show_boss_header(boss)
    for i, step in enumerate(boss.steps, 1):
        result = run_exercise(step, state, i, total_steps, allow_hint=False, record_stats=True)
        if result == QUIT_SENTINEL:
            return QUIT_SENTINEL
        if not result:
            return False  # ← FAIL-FAST: one wrong step = entire fight fails
    return True
```

### Why Fail-Fast?

Boss fights simulate real scenarios: "Your production server is broken. Fix it." In reality, you can't skip a step — if you don't `git stash` first, you can't `git pull`. Each step depends on the previous one succeeding.

Compare this to drills, where questions are independent — getting Q3 wrong doesn't affect Q4. Boss fights are sequential by nature.

### Why No Hints in Boss Fights?

Boss fights test mastery. They appear AFTER the player has completed teaching levels AND exercise rounds for that topic area. By this point, they should know the commands. Hints would defeat the purpose.

The retry loop still works (the player can keep trying each step), but the "skip" option causes the entire fight to fail.

---

## Step 8 — Exercise Round Runner

Find `run_exercise_round()`:

```python
def run_exercise_round(er, state):
    ui.show_exercise_round_header(er)
    required, total = er.pass_threshold
    exercises = _build_pool(er.exercises, total)
    # ... same scoring loop as drill zone
```

Exercise rounds are structurally identical to drill zones — pool builder, scoring, pass threshold. The difference is:
- Drills are at the END of a level (testing what you just learned)
- Exercise rounds are STANDALONE stages (reviewing everything so far)

The code reuse is intentional: `_build_pool()` and the scoring loop work for both.

---

## Step 9 — Setup Runner

Find `run_setup()`:

```python
def run_setup(setup_exercises, state):
    ui.show_setup_intro()
    for i, ex in enumerate(setup_exercises, 1):
        result = run_exercise(ex, state, i, len(setup_exercises), record_stats=False)
        if result == QUIT_SENTINEL:
            return QUIT_SENTINEL
    state.setup_complete = True
    state.save()
    return True
```

**Why `record_stats=False`?** The setup intro is a tutorial about how the game works ("type 'git init' to try"). Recording these as "correct/wrong" would skew the player's accuracy stats with trivial practice answers.

**Why `state.setup_complete = True` and `state.save()`?** So the setup only runs once. On next launch, `main.py` checks `state.setup_complete` and skips directly to the menu.

---

## ✅ Quality Gate

- [ ] `QUIT_SENTINEL` propagates from retry loop → exercise → level → main
- [ ] Near-miss detection uses `difflib.SequenceMatcher` with ratio thresholds
- [ ] Retry loop unlocks "skip" after `SKIP_UNLOCK_RETRIES` wrong attempts
- [ ] `_build_pool()` handles fewer items than needed (via `itertools.cycle`)
- [ ] Boss fight uses fail-fast (one skip/wrong = entire fight fails)
- [ ] Level has 4 phases: teaching → exercises → recap → drills
- [ ] `record_stats=False` for setup intro
- [ ] `allow_hint=False` for drills, rounds, and boss fights
- [ ] All tests pass: `python -m pytest tests/ -v`

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Can't quit mid-level | Check every `run_exercise()` call has `if result == QUIT_SENTINEL` |
| Near-miss never triggers | Check that `normalize()` is called before `SequenceMatcher` |
| Skip available immediately | `SKIP_UNLOCK_RETRIES` should be ≥ 1 |
| Drill zone always passes | Check `correct_count >= required` (not `>`) |
| Boss fight doesn't fail-fast | The `if not result: return False` line must be inside the step loop |

---

**Phase 5 complete? Now wire everything together in main.py → [phase6.md](phase6.md)**
