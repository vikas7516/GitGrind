# 🚀 PHASE 4 — State Engine Upgrade

---

## 🎯 Goal

Upgrade your state engine from a simple JSON dump to a resilient persistence system with atomic writes, schema evolution, streak tracking, session stats, and notebook storage.

The state engine is the backbone of player trust. If they lose progress, they quit. This phase makes data loss virtually impossible.

> **Open `engine/state.py` and follow along.** This guide explains every function, every design decision, and the real-world problems each one solves.

---

## What You'll Learn

- How `tempfile.mkstemp()` + `os.replace()` creates atomic writes
- How `os.fsync()` forces data to disk (vs. OS buffer)
- How deep merging handles schema evolution without data loss
- How Python `@property` creates a clean API over raw dictionary storage
- Why session counters are ephemeral (not saved to disk)
- How to format time displays that scale from seconds to days

---

## Step 1 — The Corruption Problem

Your MVP does this:

```python
def save(self):
    with open("save_data.json", "w") as f:
        json.dump(self.data, f)
```

This looks fine. But what if the power goes out DURING `json.dump()`?

```
save_data.json before: {"current_stage_index": 5, "stats": {...}}
save_data.json during: {"current_stage_index": 5, "st
                                                     ↑ POWER OFF HERE
save_data.json after:  {"current_stage_index": 5, "st    ← CORRUPTED
```

JSON is now broken. `json.load()` crashes. Player loses ALL progress — not just the current save, but everything since they started playing.

**The probability seems low, but with thousands of players it's guaranteed to happen.** The fix costs 6 lines of code.

---

## Step 2 — Atomic Writes (How `_atomic_write_json` Works)

Find `_atomic_write_json()` in `engine/state.py`. This function ensures save files are NEVER half-written.

### The Pattern: Write to Temp, Then Rename

```python
fd, temp_path = tempfile.mkstemp(prefix=".gitgrind_save_", dir=dir_path)
```

`tempfile.mkstemp()` creates a temporary file with a random name (like `.gitgrind_save_abc123`) in the same directory as the real save file. It returns two things:
- `fd` — a file descriptor (a low-level file handle, an integer)
- `temp_path` — the path to the temp file

**Why same directory?** Because `os.replace()` (used later) only works atomically when source and destination are on the same filesystem. Same directory guarantees same filesystem.

**Why the `.gitgrind_save_` prefix?** So if the process crashes before cleanup, you can identify and delete orphaned temp files. Without a prefix, they'd be indistinguishable from other temp files.

### Writing the Data

```python
with os.fdopen(fd, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
    f.flush()
    try:
        os.fsync(f.fileno())
    except OSError:
        pass
```

**Why `os.fdopen(fd, "w")` instead of `open(temp_path, "w")`?**

`tempfile.mkstemp()` already opened the file and gave you the descriptor `fd`. Using `os.fdopen()` wraps that existing descriptor into a normal Python file object. If you used `open(temp_path, "w")` instead, you'd have TWO open handles to the same file, which can cause data corruption on some operating systems.

**What does `f.flush()` do?**

Python buffers writes in memory for performance. `.flush()` pushes Python's internal buffer to the operating system. But the OS has its OWN buffer — data might still be in RAM, not on disk.

**What does `os.fsync(f.fileno())` do?**

It forces the operating system to write its buffer to the physical disk. Without `fsync`, a power loss could still lose data that was in the OS buffer. After `fsync`, the data is physically on disk — even if power is cut 1 millisecond later.

**Why the `try/except OSError`?**

Some filesystems (like network drives or some virtual filesystems) don't support `fsync`. Wrapping it in `try/except` means the save works everywhere — with the strongest guarantee possible on that particular system.

### The Atomic Rename

```python
os.replace(temp_path, path)
```

`os.replace()` renames the temp file to the real save file. On most operating systems, **rename is atomic** — it either fully completes or doesn't happen at all. There's no in-between state where the file is half-renamed.

**The critical insight:** At no point does the real save file contain partial data:

```
Timeline:
  1. Real save file:  {"stage": 5, ...}        ← UNTOUCHED
  2. Temp file:       {"stage": 6, ...}        ← written + synced
  3. os.replace()     ← INSTANT swap
  4. Real save file:  {"stage": 6, ...}        ← COMPLETE
```

If the process crashes at step 2, the real save file still has the old (complete) data. The player loses at most one save — they don't lose all progress.

### Error Recovery

```python
except (OSError, IOError, ValueError) as e:
    logger.warning("Failed to write save file: %s", e)
    try:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    except OSError:
        pass
    return False
```

If writing fails (disk full, permission denied, etc.):
1. Log the error (for debugging, not shown to player)
2. Clean up the temp file (if it exists)
3. Return `False` so the caller knows the save failed

The nested `try/except` around `os.remove()` handles the edge case where even cleanup fails (e.g., temp file was already deleted by the OS).

---

## Step 3 — The Schema Evolution Problem (Deep Merge)

Version 1.0 of your game saves this:

```json
{"current_stage_index": 5, "stats": {"total_correct": 42}}
```

Version 2.0 adds notebook tracking:

```json
{"current_stage_index": 5, "stats": {...}, "notebook_entries": {}, "game_complete": false}
```

What happens when a v2.0 game loads a v1.0 save file? The save has no `notebook_entries` key. Without deep merge:

```python
# Option A: Overwrite defaults entirely
self.data = saved_data
# → notebook_entries MISSING → KeyError when runner tries to save a teaching
```

### How Deep Merge Solves This

Find `_deep_merge()` in the file:

```python
def _deep_merge(base, override):
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
    return base
```

**What this does:**

1. Start with `base` = `_default_state()` (has ALL fields, including new ones)
2. Walk through `override` = saved data (only has old fields)
3. For each key in the save:
   - If BOTH sides have a dict → recurse and merge the nested dicts
   - Otherwise → the saved value wins (override the default)

**Example:**

```
base (defaults):     {"stats": {"total_correct": 0, "hints_used": 0}, "notebook_entries": {}}
override (save file): {"stats": {"total_correct": 42}}

Step 1: key="stats" → both are dicts → RECURSE
  Step 1a: key="total_correct" → not a dict → override wins → 42
  (key="hints_used" not in override → keeps default → 0)
Step 2: key="notebook_entries" not in override → keeps default → {}

Result: {"stats": {"total_correct": 42, "hints_used": 0}, "notebook_entries": {}}
```

The player's saved progress (42 correct answers) is preserved. The new field (`notebook_entries`) gets its default value. Nothing crashes. Nothing is lost.

**Why is this recursive?** Because `stats` is a nested dict. If you used a simple `dict.update()`, the entire `stats` dict from the save file would REPLACE the default `stats` dict — losing any new stat fields that weren't in the old save.

---

## Step 4 — `_default_state()` — The Schema

Find `_default_state()` — it's a function, not a constant:

```python
def _default_state():
    return {
        "current_stage_index": 0,
        "cleared_stages": [],
        "setup_complete": False,
        "glossary_seen": False,
        "stats": {
            "total_correct": 0,
            "total_wrong": 0,
            "total_commands_typed": 0,
            "first_try_correct": 0,
            "hints_used": 0,
            "current_streak": 0,
            "best_streak": 0,
            "start_time": datetime.now().isoformat(),
            "sessions": 0,
            "time_played_seconds": 0,
        },
        "commands_learned": [],
        "notebook_entries": {},
        "game_complete": False,
    }
```

**Why a function, not a dict constant?**

Same reason as `field(default_factory=list)` from Phase 2 — if it were a constant, every `GameState` instance would share the SAME dict. Mutating one would mutate all. A function creates a fresh dict every time.

**Why `datetime.now().isoformat()` for `start_time`?**

`.isoformat()` produces a string like `"2024-03-15T14:30:00"`. This is:
- Human-readable in the JSON file
- JSON-serializable (plain string)
- Parseable back to a datetime if needed

**Understanding each field:**

| Field | Purpose | Persisted? |
|-------|---------|-----------|
| `current_stage_index` | Which stage the player should play next | ✅ Yes |
| `cleared_stages` | List of completed stage indices | ✅ Yes |
| `setup_complete` | Whether the intro tutorial is done | ✅ Yes |
| `glossary_seen` | Whether "NEW" badge should show on glossary | ✅ Yes |
| `stats.total_correct` | Lifetime correct answers | ✅ Yes |
| `stats.total_wrong` | Lifetime wrong answers | ✅ Yes |
| `stats.total_commands_typed` | Total inputs (correct + wrong) | ✅ Yes |
| `stats.first_try_correct` | Correct on first attempt (no retries) | ✅ Yes |
| `stats.hints_used` | Number of times player typed "hint" | ✅ Yes |
| `stats.current_streak` | Consecutive correct answers | ✅ Yes |
| `stats.best_streak` | All-time highest streak | ✅ Yes |
| `stats.sessions` | Number of play sessions | ✅ Yes |
| `stats.time_played_seconds` | Cumulative play time | ✅ Yes |
| `commands_learned` | Commands for the notebook system | ✅ Yes |
| `notebook_entries` | Teaching data for notebook display | ✅ Yes |
| `game_complete` | Whether all 35 stages are cleared | ✅ Yes |

---

## Step 5 — The `GameState` Class

### `__init__` — Two Layers of State

```python
def __init__(self):
    self.data = _default_state()
    self._session_start = time.time()
    self._session_correct = 0
    self._session_wrong = 0
    self._session_skipped = 0
    self._session_stages_cleared = 0
    self._session_active = False
```

Notice two categories:
1. **`self.data`** — persisted to disk (saved in JSON)
2. **`self._session_*`** — ephemeral (reset every app restart)

**Why separate session counters?** Session stats show "this session: 12 correct, 3 wrong." But you don't want to save these — next time the player opens the app, it's a fresh session. The underscore prefix (`_session_correct`) is a Python convention meaning "private, don't access from outside."

**Why `time.time()` for `_session_start`?** `time.time()` returns seconds since epoch (a float). When saving, you calculate `elapsed = time.time() - self._session_start` to know how many seconds this session lasted. Then reset the timer for the next save interval.

### `save()` — Time Accumulation + Atomic Write

```python
def save(self):
    elapsed = time.time() - self._session_start
    self.data["stats"]["time_played_seconds"] += int(elapsed)
    self._session_start = time.time()
    if not _atomic_write_json(SAVE_FILE, self.data):
        logger.warning("Progress not saved; will retry on next save.")
```

**Why accumulate time on each save, not at exit?**

Because if the app crashes, the "on exit" code never runs. By accumulating on every save, the worst you lose is time since the last save — typically a few seconds.

**Why `int(elapsed)` (truncating fractional seconds)?**

Sub-second precision in play time is meaningless. Truncating to integers prevents floating-point accumulation errors over hundreds of saves.

**Why reset `_session_start` after each save?**

To prevent double-counting. Without the reset, each save would add the TOTAL session time (from app start), not the INCREMENT since last save.

### `load()` — Deep Merge + Session Counter

```python
def load(self):
    if os.path.exists(SAVE_FILE):
        try:
            saved = _load_json(SAVE_FILE)
            _deep_merge(self.data, saved)
            self.data["stats"]["sessions"] += 1
            self._session_start = time.time()
            return True
        except (ValueError, json.JSONDecodeError, OSError, IOError, KeyError, TypeError) as e:
            logger.warning("Save file corrupted, starting fresh: %s", e)
            self.data = _default_state()
            return False
    return False
```

**The exception list is long on purpose.** Each type covers a different corruption scenario:

| Exception | What Happened |
|-----------|--------------|
| `ValueError` | `_load_json` said "not a JSON object" |
| `json.JSONDecodeError` | Invalid JSON (truncated, garbled) |
| `OSError` | File exists but can't be read (permissions) |
| `IOError` | I/O failure during read |
| `KeyError` | JSON loaded but missing expected keys |
| `TypeError` | JSON has wrong types (e.g., string where dict expected) |

**Why `self.data = _default_state()` on error?** Fresh start — better to lose progress than crash in an infinite error loop with a corrupted file.

**Why increment `sessions` on load, not on save?** Because a "session" is one app startup. You load once per startup. If you incremented on save, playing for 30 minutes and saving 100 times would count as 100 sessions.

### `reset()` — Clean Slate

```python
def reset(self):
    self.data = _default_state()
    if os.path.exists(SAVE_FILE):
        try:
            os.remove(SAVE_FILE)
        except OSError:
            logger.warning("Failed to remove save file: %s", SAVE_FILE)
```

Reset both memory AND disk. The `try/except` handles the case where the file is locked by another process or the user doesn't have write permissions.

---

## Step 6 — The Property Pattern

Look at how `GameState` wraps raw dictionary access:

```python
@property
def current_stage_index(self):
    return self.data["current_stage_index"]

@current_stage_index.setter
def current_stage_index(self, value):
    self.data["current_stage_index"] = value
```

**Why `@property` instead of direct dict access?**

Without properties, throughout your entire codebase you'd write:

```python
# Every file that reads stage progress:
state.data["current_stage_index"]
state.data["stats"]["current_streak"]
state.data["stats"]["best_streak"]
```

With properties:

```python
state.current_stage_index
state.current_streak
state.best_streak
```

Benefits:
1. **Cleaner code** — `state.current_streak` reads better than `state.data["stats"]["current_streak"]`
2. **Encapsulation** — if you rename the key in `_default_state()`, you only update the property, not every file
3. **Computed values** — properties can calculate on-the-fly (like `accuracy`)
4. **`.get()` safety** — `self.data["stats"].get("current_streak", 0)` handles missing keys gracefully

### Why Some Properties Use `.get()` and Others Don't

```python
# Direct access (crashes if missing):
@property
def current_stage_index(self):
    return self.data["current_stage_index"]

# Safe access (returns default if missing):
@property
def current_streak(self):
    return self.data["stats"].get("current_streak", 0)
```

Fields that existed in the MVP (like `current_stage_index`) are guaranteed to exist in any save file. Fields added later (like `current_streak`) might be missing in old save files that haven't been deep-merged yet. `.get(key, default)` returns the default value instead of crashing.

---

## Step 7 — Computed Properties

### `accuracy` — Division Safety

```python
@property
def accuracy(self):
    total = self.data["stats"]["total_correct"] + self.data["stats"]["total_wrong"]
    if total == 0:
        return 0
    return int(round(self.data["stats"]["total_correct"] / total * 100))
```

**Why check `total == 0`?** Division by zero. Before the player answers any questions, both `total_correct` and `total_wrong` are 0. Without the check: `0 / 0` → `ZeroDivisionError` crash.

**Why `int(round(...))`?** `round()` gives `80.0` (float). The UI expects an integer for display like `"80%"`. `int()` converts `80.0` → `80`.

### `time_played_display` — Adaptive Formatting

```python
@property
def time_played_display(self):
    secs = self.data["stats"]["time_played_seconds"]
    secs += int(time.time() - self._session_start)
    if secs < 60:
        return f"{secs}s"
    mins = secs // 60
    if mins < 60:
        return f"{mins}m {secs % 60}s"
    hours = mins // 60
    remaining_mins = mins % 60
    if hours < 24:
        return f"{hours}h {remaining_mins}m"
    days = hours // 24
    remaining_hours = hours % 24
    return f"{days}d {remaining_hours}h"
```

**Why add `time.time() - self._session_start`?** The persisted time only updates on save. Between saves, the current session time isn't included. Adding the current elapsed time gives an accurate display at any moment.

**Why adaptive formatting?** `"3600s"` is unreadable. `"1h 0m"` is clear. The cascading `if` statements pick the right unit:

| Duration | Display |
|----------|---------|
| 45 seconds | `45s` |
| 5 minutes 30 seconds | `5m 30s` |
| 2 hours 15 minutes | `2h 15m` |
| 3 days 7 hours | `3d 7h` |

---

## Step 8 — Recording Stats

### `record_correct()` — Streak Management

```python
def record_correct(self, first_try=False):
    self.data["stats"]["total_correct"] += 1
    self.data["stats"]["total_commands_typed"] += 1
    if first_try:
        self.data["stats"]["first_try_correct"] += 1
    
    # Streak tracking
    self.data["stats"]["current_streak"] += 1
    if self.data["stats"]["current_streak"] > self.data["stats"]["best_streak"]:
        self.data["stats"]["best_streak"] = self.data["stats"]["current_streak"]
    
    self._session_correct += 1
```

**Why `first_try` parameter?** The runner knows if the player got it right on the first attempt (before any retries). First-try accuracy is a separate, more meaningful stat — it shows genuine mastery vs. eventually-getting-it-right.

**Why update `best_streak` inside `record_correct()`?** Because best streak can ONLY change when the current streak grows. Checking every time a correct answer is recorded is the natural place.

### `record_wrong()` — Streak Reset

```python
def record_wrong(self):
    self.data["stats"]["total_wrong"] += 1
    self.data["stats"]["total_commands_typed"] += 1
    self.data["stats"]["current_streak"] = 0
    self._session_wrong += 1
```

**Why reset `current_streak` to 0?** A streak is consecutive correct answers. One wrong answer breaks the chain. Note that `best_streak` is NOT reset — it preserves the all-time record.

### `clear_stage()` — Progress Advancement

```python
def clear_stage(self, stage_index):
    if stage_index not in self.data["cleared_stages"]:
        self.data["cleared_stages"].append(stage_index)
    if stage_index + 1 > self.data["current_stage_index"]:
        self.data["current_stage_index"] = stage_index + 1
    self._session_stages_cleared += 1
    self.save()
```

**Why `if stage_index not in cleared_stages`?** Prevents duplicates if the player replays a stage.

**Why `stage_index + 1 > current_stage_index` (not just `=`)?** Because the player might replay stage 3 (which sets `current_stage_index` to 4), but they're already on stage 10. Without the `>` check, replaying would move them BACKWARD.

**Why `self.save()` here?** Clearing a stage is the most important state change. Auto-saving ensures progress is never lost even if the player force-quits right after clearing.

---

## Step 9 — Notebook Integration

```python
def add_notebook_entry(self, teaching):
    self.data.setdefault("notebook_entries", {})
    self.data["notebook_entries"][teaching.command] = {
        "syntax": teaching.syntax,
        "explanation": teaching.explanation,
        "pro_tip": teaching.pro_tip,
    }
```

**Why `.setdefault()` before writing?** Old save files might not have `notebook_entries`. `.setdefault("notebook_entries", {})` creates the key with an empty dict ONLY if it doesn't already exist. If it exists, it does nothing.

**Why store entries by command name?** `{"git init": {...}, "git add": {...}}`. Using the command as the key means:
- No duplicates — replaying a level overwrites the same entry
- O(1) lookup — checking if a command is in the notebook is instant
- Natural ordering — the notebook displays commands alphabetically

---

## Step 10 — The Save File Path

```python
SAVE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "save_data.json")
```

**Parsing this:**

| Expression | Value |
|-----------|-------|
| `__file__` | Path to `engine/state.py` |
| `os.path.dirname(__file__)` | Path to `engine/` |
| `os.path.dirname(os.path.dirname(__file__))` | Path to project root |
| `os.path.join(..., "save_data.json")` | `<project_root>/save_data.json` |

**Why `os.path.dirname` twice?** `state.py` is inside `engine/`, which is inside the project root. Two `dirname` calls go up two levels.

**Why not just `"save_data.json"`?** Because Python resolves relative paths from the CURRENT WORKING DIRECTORY, not the file's location. If the player runs `python GitGrind/main.py` from their home directory, `"save_data.json"` would create the file in their home directory, not in the project.

---

## ✅ Quality Gate

- [ ] `_atomic_write_json()` uses tempfile + os.replace (never writes directly to save file)
- [ ] `_deep_merge()` recursively merges dicts without losing new fields
- [ ] `_default_state()` is a function (not a constant dict)
- [ ] `load()` handles all corruption types gracefully
- [ ] Session counters (`_session_correct`, etc.) are NOT saved to disk
- [ ] Properties provide clean access to nested dict values
- [ ] `clear_stage()` auto-saves after progress changes
- [ ] `time_played_display` adapts format based on duration
- [ ] All tests pass: `python -m pytest tests/ -v`

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `PermissionError` on save | Close any program that has `save_data.json` open |
| Save file always empty | Check that `json.dump(data, f)` isn't receiving `None` |
| Session count climbs too fast | Only increment on `load()`, not on `save()` |
| Time display shows negative | `_session_start` wasn't reset — check `save()` |
| Old save file missing new fields | `_deep_merge()` should handle this — check the merge order |

---

**Phase 4 complete? Now build the runner that drives all gameplay → [phase5.md](phase5.md)**
