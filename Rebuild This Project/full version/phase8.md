# 🚀 PHASE 8 — Supporting Systems

---

## 🎯 Goal

Build the three supporting modules that round out the game:
1.  **`sounds.py`**: Audio feedback (Windows-only, with safe fallbacks).
2.  **`notebook.py`**: Commmand reference system + text file export.
3.  **`content/glossary.py`**: The dictionary of Git terminology.

> **Open `sounds.py`, `notebook.py`, and `content/glossary.py`.** These modules add the "polish" that makes the game feel complete.

---

## What You'll Learn

- **Platform Safety**: How to import OS-specific libraries without crashing on other systems.
- **Daemon Threads**: Preventing sound effects from blocking the game loop.
- **Lazy Initialization**: Checking capabilities once at import time.
- **Data Grouping**: Organizing flat command lists into categorized notebook entries.
- **Tuple vs Dict**: When to use tuples for ordered, read-only content.

---

## Step 1 — Audio Feedback (`sounds.py`)

The sound system plays short melodies on game events. It uses `winsound.Beep`, which is available **only on Windows**.

### Platform Safety Pattern

```python
_HAS_WINSOUND = False
if sys.platform == "win32":
    try:
        import winsound
        _HAS_WINSOUND = True
    except ImportError:
        pass
```

**Why strict checking?** If you run this on Mac or Linux, `import winsound` creates an `ImportError`. By wrapping it in `try/except` and checking `sys.platform`, we ensure the game runs silently on other OSs instead of crashing.

### Non-Blocking Audio with Daemon Threads

Functions like `_beep` and `_melody` run in their own threads:

```python
def _beep(freq, duration_ms):
    def _play():
        try:
            winsound.Beep(freq, duration_ms)
        except Exception:
            pass
    threading.Thread(target=_play, daemon=True).start()
```

**Why `daemon=True`?**
 Daemon threads are killed instantly when the main program exits. If a player quits the game while a 5-second melody is playing:
-   **Without daemon**: The process hangs until the melody finishes.
-   **With daemon**: The process exits immediately, cutting off the sound.

**Why `try/except` inside the thread?**
Because `winsound.Beep` can crash if the frequency is too low/high or if the audio driver is busy. Sound is "juice" — it should **never** crash the application. If it fails, fail silently.

### The Melody System

Instead of a single beep, `_melody` plays a sequence of notes:

```python
def sound_correct():
    """Bright ascending chirp — nailed it."""
    _melody([
        (523, 80),    # C5
        (659, 80),    # E5
        (784, 120),   # G5
    ])
```

Each event (`correct`, `wrong`, `stage_cleared`, `boss_intro`) has a distinct sonic identity. This leverages the player's audio memory to reinforce feedback.

---

## Step 2 — The Notebook System (`notebook.py`)

The notebook collects every command the player learns. It has two jobs:
1.  Display in-game (UI).
2.  Export to text file (for keeping).

### The Grouping Problem

Levels teach commands in a pedagogical order (`git init` → `git add` → `git status`). But a reference manual should be grouped by **topic**.

The `category_map` solves this. It's a flat dictionary mapping commands to categories:

```python
category_map = {
    "git init": "Basics",
    "git status": "Basics",
    "git branch": "Branching",
    # ...
}
```

**Why a flat dict?**
It separates content (commands) from presentation (categories). You can move `git checkout` from "Branching" to "Undo & Restore" just by changing one line in the map, without touching the level files.

### The "Other" Bucket

```python
cat = category_map.get(cmd, "Other")
```

If a level teaches a new command but you forget to add it to `category_map`, it falls into "Other". This prevents data loss — the command still appears in the notebook, just not in a specific category.

### Exporting to File

`generate_notebook_txt(state)` iterates through `state.notebook_entries`, groups them using the map, and writes a formatted `.txt` file.

**Why `os.path.dirname(__file__)`?**
It writes the file to the **game directory**, not the user's current working directory. This ensures the player can always find their notes.

---

## Step 3 — The Glossary (`content/glossary.py`)

The glossary provides definitions for terms like "Repo", "Staging Area", and "HEAD".

```python
GIT_GLOSSARY = [
    ("Core Concepts", [
        ("Repository", "A folder Git covers..."),
        ("Commit", "A snapshot..."),
    ]),
    ("Working Areas", [ ... ]),
]
```

### Tuples vs. Classes vs. Dicts

We use a **list of tuples** here. Why?

1.  **Ordering Matters**: We want "Core Concepts" to appear before "Advanced Concepts". A standard `dict` (before Python 3.7) didn't guarantee order. A list does.
2.  **Read-Only**: This data never changes. Tuples are immutable and slightly faster/lighter than objects.
3.  **Simplicity**: We don't need methods or inheritance. It's just text.

This is **Data-Oriented Design**: use the simplest structure that fits the data's access pattern.

---

## ✅ Quality Gate

- [ ] `sounds.py` checks `sys.platform == "win32"`.
- [ ] Sound functions use `daemon=True` threads.
- [ ] `category_map` covers all taught commands (check `notebook.py`).
- [ ] Glossary uses lists/tuples to preserve reading order.
- [ ] Notebook export handles empty states gracefully.

---

**Phase 8 complete? Now let's author the Content → [phase9.md](phase9.md)**
