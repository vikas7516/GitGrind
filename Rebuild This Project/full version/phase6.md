# 🚀 PHASE 6 — Wiring `main.py`

---

## 🎯 Goal

Connect everything together. `main.py` is the entry point — it loads saved state, shows the menu, dispatches to the correct runner for each stage type, handles boss retries with a mercy rule, and ensures progress is ALWAYS saved on exit.

> **Open `main.py` and follow along.** This guide explains every design decision, showing how the entry point ties all your modules into a working game.

---

## What You'll Learn

- How module-level validation catches content bugs at startup (not mid-game)
- How the boss retry handler uses a "mercy rule" with a safety guard against infinite loops
- Why `try/finally` guarantees saves even on crashes
- How replay mode uses a display-number-to-index mapping
- The "destructive confirmation" pattern for dangerous operations

---

## Step 1 — Content Registry and Startup Validation

Before the game starts, `main.py` builds registries of ALL content and validates that everything connects properly.

### Building the Level Registry

```python
ALL_LEVELS = {}
ALL_LEVELS.update(BASICS_LEVELS)
ALL_LEVELS.update(BRANCH_LEVELS)
ALL_LEVELS.update(REMOTE_LEVELS)
ALL_LEVELS.update(ADVANCED_LEVELS)
```

**Why `.update()` instead of `{**BASICS_LEVELS, **BRANCH_LEVELS, ...}`?**

Both work. `.update()` is chosen for clarity — each line is one content module. If you add `COLLAB_LEVELS` later, you add one line. The `{**dict1, **dict2}` syntax requires rebuilding the entire expression.

### Duplicate Detection

```python
_level_counts = {}
for src in (BASICS_LEVELS, BRANCH_LEVELS, REMOTE_LEVELS, ADVANCED_LEVELS):
    for key in src:
        _level_counts[key] = _level_counts.get(key, 0) + 1
_duplicates = [k for k, v in _level_counts.items() if v > 1]
if _duplicates:
    raise ValueError(f"Duplicate level keys found: {_duplicates}")
```

If two content files accidentally use the same key (like `"basics_1"`), the second `.update()` silently overwrites the first. Without this check, you'd have a level that mysteriously disappeared — the content is there, the stage map references it, but it was overwritten by another file using the same key.

**Why is this at module level (not inside a function)?** Because it runs at import time — the game won't even start if there's a conflict. You see the error immediately when you run `python main.py`, not 20 minutes into a play session.

### Stage Map Validation

```python
_missing_stages = []
for i, stage in enumerate(STAGE_MAP):
    if stage.stage_type == STAGE_LEVEL and stage.data_key not in ALL_LEVELS:
        _missing_stages.append(f"Stage {i}: Level {stage.data_key} not found")
    elif stage.stage_type == STAGE_EXERCISE and stage.data_key not in ALL_EXERCISE_ROUNDS:
        _missing_stages.append(f"Stage {i}: Exercise round {stage.data_key} not found")
    elif stage.stage_type == STAGE_BOSS and stage.data_key not in ALL_BOSS_FIGHTS:
        _missing_stages.append(f"Stage {i}: Boss fight {stage.data_key} not found")
if _missing_stages:
    raise ValueError(f"Stage map references missing content:\n" + "\n".join(_missing_stages))
```

This catches a dangerous category of bug: the stage map says "play boss_collab at stage 30," but you haven't written that boss fight yet. Without this check, the player reaches stage 30 and the game silently returns `False` (failed) — they can never progress past a fight that doesn't exist.

This is the **fail-fast principle** from Phase 1 again: catch configuration errors before the user encounters them.

---

## Step 2 — Stage Dispatch

Find `run_stage()` in the file. This is the router — it looks at the stage type and calls the correct runner:

```python
def run_stage(stage_index, state):
    if not (0 <= stage_index < len(STAGE_MAP)):
        return False
    stage = STAGE_MAP[stage_index]
    
    if stage.stage_type == STAGE_SETUP:
        return run_level(SETUP_LEVEL, state)
    elif stage.stage_type == STAGE_LEVEL:
        return run_level(ALL_LEVELS[stage.data_key], state)
    elif stage.stage_type == STAGE_EXERCISE:
        return run_exercise_round(ALL_EXERCISE_ROUNDS[stage.data_key], state)
    elif stage.stage_type == STAGE_BOSS:
        return run_boss_fight(ALL_BOSS_FIGHTS[stage.data_key], state)
    return False
```

### Why Validate the Index?

`state.current_stage_index` is loaded from a JSON file the user could edit. If they manually change the save file to `"current_stage_index": 999`, the game would crash at `STAGE_MAP[999]` with an `IndexError`. The bounds check returns `False` (failed) instead of crashing — the game recovers gracefully.

### Why Lazy Import for SETUP_LEVEL?

```python
if stage.stage_type == STAGE_SETUP:
    from content.levels_basics import SETUP_LEVEL
    return run_level(SETUP_LEVEL, state)
```

Setup is only run ONCE (first launch), then never again. Importing it inside the function means it's only loaded when needed — every subsequent launch skips this import entirely.

### Why `.get()` Instead of Direct Access?

```python
level = ALL_LEVELS.get(stage.data_key)
if level:
    return run_level(level, state)
```

`.get()` returns `None` if the key doesn't exist, instead of raising `KeyError`. Combined with the `if level:` check, this provides defense-in-depth: even if the startup validation somehow missed a bad key, the game won't crash.

---

## Step 3 — Boss Retry Handler

Find `handle_boss_retry()`. This manages what happens when a player fails a boss fight.

### The Mercy Rule

```python
BOSS_MAX_ATTEMPTS = 5
```

Boss fights are intentionally hard — ALL steps must be correct with NO hints. A player who fails 5 times is clearly stuck. At that point, blocking progress hurts more than it teaches.

**Before mercy (attempts 1-4):**

```python
retry = ui.get_input("  Retry? (y/n): ", save_fn=state.save)
if retry not in ("y", "yes", "retry", "r"):
    return False
```

Simple binary: retry or quit.

**After mercy (attempt 5+):**

```python
retry = ui.get_input("  Retry / Skip / Quit? (r/s/q): ", save_fn=state.save)
if retry in ("s", "skip"):
    state.clear_stage(stage_idx)  # mark as cleared!
    return True
```

A third option appears: skip. The stage counts as cleared (no asterisk, no penalty). The design philosophy: the game teaches Git, not frustration tolerance.

### The Safety Guard

```python
MAX_ITERATIONS = 100
iterations = 0
while iterations < MAX_ITERATIONS:
    iterations += 1
    # ... retry logic ...
```

**Why not `while True`?** Infinite loops are a real risk in retry logic. If a bug prevents the function from ever returning `True` or `False`, the game hangs forever. The safety guard breaks after 100 iterations (which should never happen — who retries a boss 100 times?).

This is **defensive programming**: protect against bugs in your own code, not just bad user input.

---

## Step 4 — The Main Game Loop

Find `play_continue()`. This is the core gameplay loop:

```python
def play_continue(state):
    state.start_session()
    while state.current_stage_index < TOTAL_STAGES:
        idx = state.current_stage_index
        stage = STAGE_MAP[idx]
        result = run_stage(idx, state)
        # ... handle result ...
```

### Why `< TOTAL_STAGES` and Not `<=`?

`current_stage_index` is 0-based. With 35 stages (indices 0-34), when the player clears stage 34, `clear_stage()` sets `current_stage_index` to 35. Since `35 < 35` is `False`, the loop exits. This is the standard off-by-one prevention pattern for 0-based indexing.

### Handling Each Stage Result

```
result = run_stage(idx, state)

Three possible outcomes:
├── QUIT_SENTINEL  → save + session summary → return to menu
├── True (cleared) → mark stage cleared → advance to next
└── False (failed) → offer retry
    ├── Boss fight → handle_boss_retry() (with mercy)
    └── Non-boss   → simple retry? (y/n)
```

### Why Save + Session Summary on EVERY Exit?

```python
if result == QUIT_SENTINEL:
    state.save()
    ui.show_session_summary(state)
    return
```

There are MANY ways to exit the play loop — quit, fail and decline retry, boss mercy quit. Every single one needs to save and show the session summary. Missing even one creates a "progress lost" scenario.

Count the exit paths in `play_continue()`:
1. Player types "quit" during a stage → `QUIT_SENTINEL`
2. Player fails a non-boss stage, declines retry → return
3. Player fails a boss fight, declines retry → `handle_boss_retry()` returns `False`
4. Player completes all stages → loop exits naturally
5. `KeyboardInterrupt` → caught by outer `try/except`

All five need saving.

### Game Completion Detection

```python
if not state.game_complete:
    state.game_complete = True
    state.save()
    ui.show_game_complete(state)
```

**Why check `if not state.game_complete`?** The player might replay the last stage or the game loop might reach this point multiple times. Without the check, the completion screen would show every time.

---

## Step 5 — Replay Mode

Find `play_replay()`. This lets players re-run cleared stages for practice:

### The Display Mapping Problem

Internally, cleared stages might be indices `[0, 2, 5, 8, 12]`. But showing:

```
[0] Git Basics
[2] Branching
[5] Boss Fight
```

Is confusing — where are 1, 3, 4? The player should see:

```
[1] Git Basics
[2] Branching
[3] Boss Fight
```

The `menu_map` dictionary handles this:

```python
menu_map = {}
for display_num, idx in enumerate(cleared, 1):
    ui.console.print(f"  [{display_num}] {stage.label}")
    menu_map[str(display_num)] = idx
```

When the player types `"2"`, `menu_map["2"]` gives the real stage index (5 in this example).

**Why `str(display_num)` as the key?** Because `ui.get_input()` returns a string. Comparing `"2" in menu_map` is simpler than converting the input to an integer and catching `ValueError`.

### Color Coding by Stage Type

```python
if stage.stage_type == STAGE_BOSS:
    label_color = "bright_red"
elif stage.stage_type == STAGE_EXERCISE:
    label_color = "bright_blue"
else:
    label_color = "bright_cyan"
```

Visual categorization without a legend — boss fights are red (dangerous), exercise rounds are blue, regular levels are cyan. The colors match the stage map display for consistency.

---

## Step 6 — Notebook and Glossary

### Notebook — `play_notebook()`

```python
def play_notebook(state):
    ui.show_notebook(state)
    if not state.notebook_entries:
        ui.pause()
        return
    choice = ui.get_input("  Choose: ", save_fn=state.save).lower().strip()
    if choice in ("s", "save"):
        path = generate_notebook_txt(state)
```

**Why early return if no entries?** If the player hasn't completed any teaching levels, the notebook is empty. Showing save/back options for an empty notebook is confusing. The early return goes straight back to the menu.

**Why import `generate_notebook_txt` from `notebook.py`?** Because file generation logic (formatting text, writing to disk) doesn't belong in the game loop. The notebook module is a standalone utility — it takes state and produces a file.

### Reset — The Destructive Confirmation Pattern

```python
confirm = ui.get_input("  Type 'RESET' to confirm: ", save_fn=state.save)
if confirm == "RESET":  # case-sensitive! Not "reset"
```

This is a standard UX pattern for destructive actions. Requiring the player to type a specific word:
- Prevents accidental resets from hitting Enter
- Prevents typos from triggering deletion
- Makes the action deliberate and conscious
- The word is short enough to not be annoying

**Why case-sensitive?** Extra friction. Typing `RESET` in all caps is an active choice, not a habit.

---

## Step 7 — The `main()` Function — Four Layers of Defense

Find `main()`. This function has four layers of error handling:

### Layer 1: Load Failure Recovery

```python
try:
    state = GameState()
    state.load()
except Exception as e:
    state = GameState()  # fresh start
```

If the save file is so corrupted that even `GameState.load()` crashes (despite its own `try/except`), the game starts fresh. The player loses progress but the game runs.

### Layer 2: First-Launch Flow

```python
if not state.glossary_seen:
    ui.show_welcome_animation()
    ui.show_glossary()
    state.glossary_seen = True
    state.save()
```

**Why save immediately after setting `glossary_seen`?** If the player quits during the glossary, the flag is already saved. Without this save, they'd see the glossary on every launch until they complete a stage (which triggers the next save).

### Layer 3: Game Loop Exception Handling

```python
try:
    while True:
        # menu → dispatch → play
except KeyboardInterrupt:
    # Ctrl+C — graceful shutdown
except Exception as e:
    # Any unexpected bug — print traceback for debugging
    traceback.print_exc()
```

**Why `except Exception` (catch-all)?** Because the game should NEVER crash without saving. Even if there's a bug in the UI, or a content file has bad data, or a library throws unexpectedly — the game catches it, prints the error for debugging, and continues to the `finally` block.

**Why `traceback.print_exc()`?** Without the full traceback, you'd only see `"Unexpected error: 'NoneType' has no attribute 'type'"` — useless for debugging. The traceback shows exactly which file and line caused it.

### Layer 4: The `finally` Guarantee

```python
finally:
    try:
        state.save()
    except Exception as e:
        ui.console.print(f"❌ Failed to save: {e}")
```

**`finally` always runs** — whether the `try` block completed normally, raised an exception, or was interrupted. This is the ultimate guarantee that progress is saved.

**Why `try/except` INSIDE `finally`?** Because `state.save()` itself could fail (disk full, permissions error). If save fails in the finally block without catching, the save error replaces the ORIGINAL error in the traceback — making debugging impossible. Catching the save error preserves the original cause.

### Python Version Check

```python
if sys.version_info < (3, 10):
    print("Error: Python 3.10 or higher is required.")
    sys.exit(1)
```

The game uses Python 3.10+ features (like `from __future__ import annotations` behavior). If someone runs it with Python 3.8, they'd get cryptic `SyntaxError`s. This check gives a clear, actionable message instead.

**Why use `print()` here, not `ui.console.print()`?** Because importing `ui` triggers importing `rich`, which might fail on ancient Python versions. Using plain `print()` works on any Python version.

**Why `sys.exit(1)` (not `sys.exit(0)`)?** Exit code `0` means "success." Exit code `1` (or any non-zero) means "error." Scripts and tools that call your program check the exit code to determine if it succeeded.

---

## ✅ Quality Gate

- [ ] All imports resolve (no missing modules)
- [ ] Duplicate level key detection catches conflicts at startup
- [ ] Stage map validation catches missing content at startup
- [ ] `run_stage()` handles invalid indices from corrupted saves
- [ ] Boss retry has mercy rule after 5 attempts
- [ ] Boss retry has safety guard against infinite loops
- [ ] Every exit path from `play_continue()` saves + shows session summary
- [ ] `play_reset()` requires typing `RESET` (case-sensitive)
- [ ] `finally` block always saves, even after crashes
- [ ] Python version check uses `print()`, not `ui.console.print()`
- [ ] All tests pass: `python -m pytest tests/ -v`

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ValueError: Duplicate level keys` | Two level files use the same key — rename one |
| `ValueError: Stage map references missing content` | `stage_map.py` uses a key that doesn't exist in the content dicts |
| Boss can't be skipped | Check `boss_attempts >= BOSS_MAX_ATTEMPTS` — is the count incrementing? |
| Progress lost on crash | Check that `finally` block runs `state.save()` |
| Menu choice doesn't work | `.lower().strip()` should handle whitespace and casing |
| Replay shows wrong stages | Check that `sorted(state.cleared_stages)` returns valid indices |

---

**Phase 6 complete? Now build the full UI module → [phase7.md](phase7.md)**
