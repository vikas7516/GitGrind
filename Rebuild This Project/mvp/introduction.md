# 🎮 GitGrind MVP — Build It From Scratch

---

## What You Are Building

A terminal-based Git learning game. The player sees a question, types a Git command, gets instant feedback, and progresses through stages.

That's it. No web server. No database. No GUI framework. Just Python + terminal.

---

## What The Final MVP Looks Like

```
╭──────────────────────────────────────╮
│ ⚡ GitGrind                          │
╰──────────────────────────────────────╯

  Stages: 2/3  |  Accuracy: 85%

  [C]  Continue
  [Q]  Quit

> C

  📖 LESSON → git init

  Creates a new Git repository in your current folder.
  This is the FIRST thing you do when starting a new project.

  ┌─────────────────────────┐
  │  git init               │
  └─────────────────────────┘

  Exercise 1/3

  You just created a new project folder called 'my-app'.
  What command do you run to start tracking with Git?

  ▸ git init

  ✅ Correct!
    $ git init
    Initialized empty Git repository in /my-app/.git/
```

If this loop works — lesson → question → validate → feedback → progress — your MVP is real.

---

## What You Must Know First

You need basic Python knowledge. If any of these look unfamiliar, pause and learn them first.

### 1️⃣ Variables and Strings

```python
name = "GitGrind"
score = 0
prompt = "What command initializes a repo?"
```

### 2️⃣ Dictionaries

```python
state = {
    "current_stage": 0,
    "score": 42,
    "cleared": [0, 1, 2]
}
```

### 3️⃣ Lists

```python
exercises = [
    {"prompt": "Init a repo", "answer": "git init"},
    {"prompt": "Check status", "answer": "git status"},
]
```

### 4️⃣ While Loops with Input

```python
while True:
    choice = input("> ").strip().lower()
    if choice == "q":
        break
```

Everything else (dataclasses, JSON, Rich, testing) is taught in the phase files.

---

## How CLI Apps Work

Every terminal app follows this loop:

```
Initialize everything (load state, set up data)

WHILE app is running:
    1. Show a menu or prompt
    2. Read user input
    3. Process the input
    4. Show the result
    5. Save if needed
```

GitGrind is just logic inside this loop — with teaching slides, exercises, and answer validation.

---

## 🧩 Architecture (Think First, Code Later)

Before writing a single line, understand the systems:

| System | Its Job | File |
|--------|---------|------|
| UI | Display text, read input | `ui.py` |
| Models | Define data shapes (Exercise, Level) | `content/models.py` |
| Content | Actual questions and lessons | `content/levels_mvp.py` |
| Stage Map | Define the stage order | `content/stage_map.py` |
| Validator | Check if answers are correct | `engine/validator.py` |
| State | Track progress, save/load to disk | `engine/state.py` |
| Runner | Orchestrate: show → validate → feedback | `engine/runner.py` |
| Main | Menu loop, wire everything together | `main.py` |

### Why This Split?

> **Rule: every file has ONE job.**

* `ui.py` never checks if an answer is right.
* `validator.py` never prints anything.
* `state.py` never asks the user a question.

If you mix responsibilities, your code becomes impossible to debug.

---

## Project Structure

```
GitGrind-MVP/
├── main.py                    # Entry point — menu loop
├── ui.py                      # All display and input functions
├── engine/
│   ├── __init__.py            # Empty (makes it a package)
│   ├── validator.py           # Answer checking logic
│   ├── state.py               # Progress tracking + save/load
│   └── runner.py              # Exercise/level execution
├── content/
│   ├── __init__.py            # Empty (makes it a package)
│   ├── models.py              # Dataclass definitions
│   ├── levels_mvp.py          # Actual lesson + exercise data
│   └── stage_map.py           # Ordered list of stages
├── tests/
│   ├── test_validator.py
│   ├── test_state.py
│   └── test_content.py
├── save_data.json             # Auto-generated (player progress)
├── requirements.txt           # rich
└── README.md
```

---

## Build Order (Follow This Exactly)

You build bottom-up. Foundation first, wiring last.

```
Phase 1 → Project setup + first runnable app (ui.py + main.py)
Phase 2 → Data models (define what an Exercise/Level looks like)
Phase 3 → Content (write actual questions and teachings)
Phase 4 → Validator (check if "git init" is correct)
Phase 5 → State engine (save progress, track stats)
Phase 6 → Runner + wire everything (connect all pieces, make it playable)
Phase 7 → Testing and debugging (automated tests + smoke test)
Phase 8 → Polish, document, release
```

Each phase has its own file. Follow them in order.

---

## Non-Negotiable Rules

1. **Run your app after every small change.** Don't write 100 lines then run.
2. **Fix bugs immediately.** Don't stack changes on top of broken code.
3. **Write it yourself.** If you can't explain a line, you don't own it.
4. **Use AI for help, not for copy-paste.** Ask it to explain concepts, not write your code.

---

## Tools You Need

| Tool | What It Does | Install |
|------|-------------|---------|
| Python 3.10+ | Runs your code | `python.org` |
| `rich` | Beautiful terminal output | `pip install rich` |
| A code editor | Write code | VS Code recommended |
| A terminal | Run code | PowerShell / Terminal |

---

**Ready? Open [phase1.md](phase1.md) and start building.**
