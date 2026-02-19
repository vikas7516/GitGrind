# 🚀 PHASE 5 — State Engine (Save Progress, Track Stats)

---

## 🎯 Goal

Build a system that:
1. Tracks the player's progress (which stage they're on)
2. Tracks statistics (correct answers, wrong answers, accuracy)
3. Saves everything to a JSON file
4. Loads it back when the game restarts

Without this, the player starts from scratch every time they close the terminal.

---

## 🔹 Step 1 — Understand JSON

JSON is a text format for storing structured data. It looks almost exactly like a Python dictionary:

```json
{
  "name": "Player1",
  "score": 42,
  "levels_cleared": [1, 2]
}
```

Python can read and write JSON files using the built-in `json` module.

### Writing JSON:

```python
import json

data = {"score": 42, "name": "Player1"}

with open("test.json", "w") as f:
    json.dump(data, f, indent=2)
```

This creates a file called `test.json` with readable content. `indent=2` adds spacing so the file isn't all on one line.

### Reading JSON:

```python
import json

with open("test.json", "r") as f:
    loaded = json.load(f)

print(loaded)           # {'score': 42, 'name': 'Player1'}
print(loaded["score"])  # 42
```

### What can go wrong?

- **File doesn't exist yet** (first time playing) → `FileNotFoundError`
- **File is corrupted** (player edited it, crash during save) → `json.JSONDecodeError`

You need to handle both cases so the game doesn't crash.

---

## 🔹 Step 2 — Design the Save Data

Before coding, decide what to save. Here's what our game needs:

```python
{
    "current_stage_index": 0,    # Which stage the player is on (0, 1, 2...)
    "cleared_stages": [],        # List of stage indices that have been cleared
    "stats": {
        "correct": 0,            # Total correct answers
        "wrong": 0,              # Total wrong answers
        "hints_used": 0          # Total hints requested
    }
}
```

That's it. For MVP, we don't need anything fancier.

---

## 🔹 Step 3 — Build the GameState Class (`engine/state.py`)

Create `engine/state.py` with this complete code:

```python
"""
GitGrind — Game state management.
Tracks progress, stats, and saves/loads to JSON.
"""
import json
import os
import copy


# Where the save file lives — in the project root folder
SAVE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),  # Go up from engine/ to project root
    "save_data.json"
)


def _default_state():
    """
    Returns a fresh state dictionary with all default values.
    This is what a brand new player starts with.
    """
    return {
        "current_stage_index": 0,
        "cleared_stages": [],
        "stats": {
            "correct": 0,
            "wrong": 0,
            "hints_used": 0,
        },
    }


class GameState:
    """
    Manages all game progress and statistics.

    Usage:
        state = GameState()
        state.load()            # Load save file (or use defaults)
        state.record_correct()  # Player got one right
        state.save()            # Write to disk
    """

    def __init__(self):
        # Start with a fresh copy of the defaults.
        # copy.deepcopy() creates a completely independent copy —
        # changing this won't affect the original _default_state.
        self.data = copy.deepcopy(_default_state())

    # ── Properties (shortcuts to access nested data) ─────────

    def get_current_stage_index(self):
        """Which stage the player is currently on."""
        return self.data["current_stage_index"]

    # Python lets us access this like a variable instead of calling it
    # as a method. So we can write state.current_stage_index
    # instead of state.get_current_stage_index()
    current_stage_index = property(get_current_stage_index)

    def get_cleared_stages(self):
        """List of stage indices that have been cleared."""
        return self.data["cleared_stages"]

    cleared_stages = property(get_cleared_stages)

    def get_accuracy(self):
        """
        Calculate accuracy as a percentage.
        Returns 0.0 if no exercises have been attempted (avoids division by zero).
        """
        stats = self.data["stats"]
        total = stats["correct"] + stats["wrong"]
        if total == 0:
            return 0.0
        return stats["correct"] / total * 100

    accuracy = property(get_accuracy)

    # ── Recording results ────────────────────────────────────

    def record_correct(self, first_try=False):
        """Record a correct answer."""
        self.data["stats"]["correct"] += 1

    def record_wrong(self):
        """Record a wrong answer."""
        self.data["stats"]["wrong"] += 1

    def record_hint(self):
        """Record that a hint was used."""
        self.data["stats"]["hints_used"] += 1

    # ── Stage progression ────────────────────────────────────

    def clear_stage(self, index):
        """
        Mark a stage as cleared and advance to the next one.
        Won't add duplicates if the same stage is cleared twice.
        """
        if index not in self.data["cleared_stages"]:
            self.data["cleared_stages"].append(index)
        self.data["current_stage_index"] = index + 1

    # ── Save and Load ────────────────────────────────────────

    def save(self):
        """Save the current state to save_data.json."""
        with open(SAVE_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def load(self):
        """
        Load state from save_data.json.
        If the file doesn't exist → use defaults (first time playing).
        If the file is corrupted → warn and use defaults.
        """
        if not os.path.exists(SAVE_FILE):
            return  # No save file yet — use defaults

        try:
            with open(SAVE_FILE, "r") as f:
                saved = json.load(f)
            self.data = saved
        except (json.JSONDecodeError, Exception):
            print("⚠️ Save file corrupted. Starting fresh.")
            self.data = copy.deepcopy(_default_state())

    def reset(self):
        """Reset all progress and delete the save file."""
        self.data = copy.deepcopy(_default_state())
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
```

### Understanding the key parts:

| Part | What It Does |
|------|-------------|
| `_default_state()` | Returns a fresh dictionary. Every new player starts with this. |
| `copy.deepcopy()` | Creates a completely independent copy of a dictionary. Without it, multiple GameState objects would share the same dict. |
| `current_stage_index = property(...)` | Lets you write `state.current_stage_index` instead of `state.data["current_stage_index"]`. Cleaner to read. |
| `if total == 0: return 0.0` | Prevents division by zero when no exercises have been attempted. |
| `clear_stage(index)` | Adds the stage to cleared list AND advances to the next stage. |
| `try/except` in `load()` | Catches corrupted save files so the app doesn't crash. |

### Why `property()`?

Without properties, you'd write:

```python
print(state.data["current_stage_index"])   # Ugly and long
```

With properties, you write:

```python
print(state.current_stage_index)   # Clean and short
```

Both do the same thing. Properties are just a convenience.

---

## 🔹 Step 4 — Test Your State Engine

Add this at the bottom of `engine/state.py`:

```python
# Temporary test — delete this later
if __name__ == "__main__":
    state = GameState()

    # Test fresh state
    print("=== Fresh State ===")
    print(f"Stage: {state.current_stage_index}")   # 0
    print(f"Accuracy: {state.accuracy}")            # 0.0
    print(f"Cleared: {state.cleared_stages}")       # []
    print()

    # Test recording
    print("=== After Recording ===")
    state.record_correct()
    state.record_correct()
    state.record_wrong()
    print(f"Correct: {state.data['stats']['correct']}")     # 2
    print(f"Wrong: {state.data['stats']['wrong']}")         # 1
    print(f"Accuracy: {state.accuracy:.1f}%")               # 66.7%
    print()

    # Test save
    state.save()
    print(f"Saved to: {SAVE_FILE}")
    print()

    # Test load (create a NEW state and load from file)
    state2 = GameState()
    state2.load()
    print("=== After Load ===")
    print(f"Loaded accuracy: {state2.accuracy:.1f}%")       # 66.7%
    print()

    # Test clear stage
    state.clear_stage(0)
    print("=== After Clearing Stage 0 ===")
    print(f"Cleared: {state.cleared_stages}")               # [0]
    print(f"Current stage: {state.current_stage_index}")    # 1
    print()

    # Test reset
    state.reset()
    print("=== After Reset ===")
    print(f"Stage: {state.current_stage_index}")    # 0
    print(f"Accuracy: {state.accuracy}")             # 0.0
    print(f"Cleared: {state.cleared_stages}")        # []
    print(f"Save file exists: {os.path.exists(SAVE_FILE)}")  # False
```

Run:

```
python engine/state.py
```

**You should see:**

```
=== Fresh State ===
Stage: 0
Accuracy: 0.0
Cleared: []

=== After Recording ===
Correct: 2
Wrong: 1
Accuracy: 66.7%

Saved to: C:\...\GitGrind-MVP\save_data.json

=== After Load ===
Loaded accuracy: 66.7%

=== After Clearing Stage 0 ===
Cleared: [0]
Current stage: 1

=== After Reset ===
Stage: 0
Accuracy: 0.0
Cleared: []
Save file exists: False
```

### Also test these edge cases manually:

1. **Delete `save_data.json`** and run again → should start fresh, no errors
2. **Open `save_data.json`**, type random garbage in it, save → run again → should print "⚠️ Save file corrupted" and use defaults

**Delete the test code** when everything passes.

---

## ✅ Checklist (Don't Move On Until)

- [ ] Fresh state has accuracy 0.0 (no division error!)
- [ ] `record_correct()` and `record_wrong()` update stats
- [ ] `accuracy` returns correct percentage (66.7% for 2/3)
- [ ] `save()` creates `save_data.json` (open it — it should be readable JSON)
- [ ] `load()` restores data from the file correctly
- [ ] Missing save file doesn't crash (first-time player)
- [ ] Corrupted save file doesn't crash
- [ ] `reset()` clears everything and deletes the save file
- [ ] `clear_stage()` updates both `cleared_stages` and `current_stage_index`

---

## 🛟 If Something Goes Wrong

**Accuracy always shows 0.0**
→ Make sure you're updating `self.data["stats"]`, not a local variable. Check that `record_correct` modifies `self.data["stats"]["correct"]`.

**FileNotFoundError on load**
→ Check that your `load()` method handles `if not os.path.exists(SAVE_FILE): return`.

**Changes don't persist between runs**
→ Are you calling `state.save()` after making changes? The data only exists in memory until you save.

**save_data.json shows up in engine/ folder instead of project root**
→ Check the `SAVE_FILE` path. `os.path.dirname(__file__)` gives `engine/`, and the second `os.path.dirname()` goes up to the project root.

---

**Phase 5 done? You have persistent state! Now connect everything into a playable game → [phase6.md](phase6.md)**
