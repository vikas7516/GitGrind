# 🚀 PHASE 3 — Writing Real Content (Levels + Exercises)

---

## 🎯 Goal

Create real teaching content that your game will use. You'll write actual Git lessons, practice exercises, and a stage progression map.

After this phase, you'll have playable content — even though the "player" (runner) doesn't exist yet.

---

## 🔹 Step 1 — Plan Your MVP Content

For an MVP, you need just enough content to prove the game loop works. Three stages:

| Stage | Topic | Commands |
|-------|-------|----------|
| Setup | Installing & configuring Git | `git --version`, `git config` |
| Level 1 | Starting a repo | `git init`, `git status` |
| Level 2 | Staging & committing | `git add`, `git commit` |

That's it. 3 playable stages. You can add more levels later.

---

## 🔹 Step 2 — Understand What Good Content Looks Like

### Teaching Slides

Each teaching teaches ONE command. It needs:

- **Command:** What the command is (`git init`)
- **Explanation:** What it does and when you'd use it (2-4 sentences in plain English)
- **Syntax:** The command template (`git add <file>`)
- **Example output:** What the terminal would show — make it look real
- **Pro tip:** A practical tip (optional)

**Bad explanation:**

```
"Initializes a repository."
```

**Good explanation:**

```
"Creates a brand new Git repository in your current folder.
This is always the FIRST Git command you run when starting
a new project. It creates a hidden .git folder that tracks
all your changes from this point forward."
```

The good version tells you what it does, WHEN to use it, and what happens behind the scenes.

### Exercises

Each exercise asks the player to recall or apply what they just learned.

**Bad exercise:**

```
prompt: "Type the command."
```

**Good exercise:**

```
prompt: "You just created a new project folder called 'my-app'.
What command do you run to start tracking it with Git?"
```

The good version gives CONTEXT — the player imagines a real scenario.

**Every exercise needs:**
- At least one answer in `answers`
- An `explanation` (shown when they get it wrong — teaches them WHY)
- A `sim_output` for correct answers when possible (simulates the terminal)

---

## 🔹 Step 3 — Write Your Content (`content/levels_mvp.py`)

Create `content/levels_mvp.py`. This file contains all the actual game content.

Here's a complete example to follow. You should modify the text to make it your own — but keep the structure.

```python
"""
GitGrind MVP — Level content.
Contains teachings and exercises for each level.
"""
from content.models import Teaching, Exercise, Level


# ═══════════════════════════════════════════════════════════
#  SETUP LEVEL (Level 0)
# ═══════════════════════════════════════════════════════════

SETUP_TEACHINGS = [
    Teaching(
        command="git --version",
        explanation=(
            "Checks if Git is installed on your computer and shows which version.\n"
            "If this command doesn't work, you need to install Git first."
        ),
        syntax="git --version",
        example_output="$ git --version\ngit version 2.43.0",
    ),
    Teaching(
        command="git config",
        explanation=(
            "Sets up your identity for Git. Every commit you make will have\n"
            "your name and email attached to it, so people know who made\n"
            "the change. You only need to do this once per computer."
        ),
        syntax="git config --global user.name \"Your Name\"",
        example_output=(
            '$ git config --global user.name "Ada Lovelace"\n'
            '$ git config --global user.email "ada@example.com"'
        ),
        pro_tip="Use the same email as your GitHub account if you have one.",
    ),
]

SETUP_EXERCISES = [
    Exercise(
        type="recall",
        prompt=(
            "You just installed Git on your computer.\n"
            "What command checks that Git is working and shows the version?"
        ),
        answers=["git --version"],
        hint="It's a flag that asks for the version number.",
        explanation=(
            "git --version prints the installed Git version.\n"
            "If it says 'command not found', Git isn't installed yet."
        ),
        sim_output="$ git --version\ngit version 2.43.0",
    ),
    Exercise(
        type="recall",
        prompt=(
            "Before making your first commit, Git needs to know who you are.\n"
            "What command sets your name for all future commits?"
        ),
        answers=[
            'git config --global user.name "Your Name"',
            "git config --global user.name",
        ],
        hint="It uses --global and user.name",
        explanation=(
            "git config --global user.name sets your name for all repos.\n"
            "--global means it applies everywhere, not just this one project."
        ),
    ),
]

SETUP_LEVEL = Level(
    number=0,
    name="Setup",
    tagline="Get Git ready on your machine",
    concept=(
        "Before writing any code, we need to make sure Git is installed\n"
        "and configured with your name and email."
    ),
    commands_taught=["git --version", "git config"],
    teachings=SETUP_TEACHINGS,
    exercises=SETUP_EXERCISES,
)


# ═══════════════════════════════════════════════════════════
#  LEVEL 1 — Init & Status
# ═══════════════════════════════════════════════════════════

LEVEL_1_TEACHINGS = [
    Teaching(
        command="git init",
        explanation=(
            "Creates a new Git repository in your current folder.\n"
            "This is the FIRST thing you do when starting a new project.\n"
            "It creates a hidden .git folder that tracks everything."
        ),
        syntax="git init",
        example_output=(
            "$ git init\n"
            "Initialized empty Git repository in /home/user/my-project/.git/"
        ),
        pro_tip="Only run this once per project — right at the beginning.",
    ),
    Teaching(
        command="git status",
        explanation=(
            "Shows what's happening in your repo right now.\n"
            "It tells you which files are new, modified, or ready to commit.\n"
            "Use this constantly — it's your 'what's going on?' command."
        ),
        syntax="git status",
        example_output=(
            "$ git status\n"
            "On branch main\n"
            "Untracked files:\n"
            "  app.py\n"
            "  README.md"
        ),
        pro_tip="Run git status before AND after every other git command.",
    ),
]

LEVEL_1_EXERCISES = [
    Exercise(
        type="recall",
        prompt=(
            "You just created a new project folder called 'my-app'.\n"
            "What command do you run inside it to start tracking with Git?"
        ),
        answers=["git init", "git init ."],
        hint="This command creates a hidden .git folder.",
        explanation=(
            "git init creates a new Git repository.\n"
            "It's always the first Git command in a new project."
        ),
        sim_output=(
            "$ git init\n"
            "Initialized empty Git repository in /my-app/.git/"
        ),
    ),
    Exercise(
        type="scenario",
        prompt=(
            "You've been editing files for a while and lost track of what\n"
            "you changed. What command shows you the current state of your repo?"
        ),
        answers=["git status"],
        hint="This command is like asking Git 'what's going on?'",
        explanation=(
            "git status shows untracked, modified, and staged files.\n"
            "It's the most-used Git command — run it often."
        ),
        sim_output=(
            "$ git status\n"
            "On branch main\n"
            "Changes not staged for commit:\n"
            "  modified: app.py"
        ),
    ),
    Exercise(
        type="recall",
        prompt="What hidden folder does git init create inside your project?",
        answers=[".git"],
        hint="It starts with a dot, which makes it hidden.",
        explanation=(
            "git init creates a .git folder.\n"
            "This hidden folder contains all of Git's tracking data.\n"
            "If you delete it, you lose all version history."
        ),
    ),
]

LEVEL_1 = Level(
    number=1,
    name="Init & Status",
    tagline="Start a repo and check what's happening",
    concept=(
        "Every Git project starts with git init, and git status is your\n"
        "constant companion — telling you what's changed and what's ready."
    ),
    commands_taught=["git init", "git status"],
    teachings=LEVEL_1_TEACHINGS,
    exercises=LEVEL_1_EXERCISES,
)


# ═══════════════════════════════════════════════════════════
#  LEVEL 2 — Staging & Committing
# ═══════════════════════════════════════════════════════════

LEVEL_2_TEACHINGS = [
    Teaching(
        command="git add",
        explanation=(
            "Stages a file — tells Git 'I want to include this file in\n"
            "my next commit.' Think of it as putting files in a box before\n"
            "shipping. You pick which files go in the box."
        ),
        syntax="git add <file>",
        example_output="$ git add app.py",
        pro_tip="Use 'git add .' to stage ALL changed files at once.",
    ),
    Teaching(
        command="git commit",
        explanation=(
            "Saves a snapshot of all staged files. This is permanent —\n"
            "Git remembers this exact version forever.\n"
            "The -m flag lets you write a short message describing what changed."
        ),
        syntax='git commit -m "your message"',
        example_output=(
            '$ git commit -m "Add homepage"\n'
            "[main abc1234] Add homepage\n"
            " 1 file changed, 42 insertions(+)"
        ),
        pro_tip="Write messages that explain WHY, not just what. 'Fix login bug' > 'Update code'.",
    ),
]

LEVEL_2_EXERCISES = [
    Exercise(
        type="scenario",
        prompt=(
            "You just finished writing app.py and want to include it\n"
            "in your next commit. What command stages this file?"
        ),
        answers=["git add app.py"],
        hint="You're adding a specific file to the staging area.",
        explanation=(
            "git add <file> stages one specific file.\n"
            "Staging means 'mark this file to be included in the next commit.'"
        ),
        sim_output="$ git add app.py",
    ),
    Exercise(
        type="scenario",
        prompt=(
            "You've modified 5 files and want to stage ALL of them\n"
            "at once. What command does that?"
        ),
        answers=["git add .", "git add --all", "git add -A"],
        hint="There's a shortcut that means 'everything in this folder.'",
        explanation=(
            "git add . stages all changed files in the current directory.\n"
            "The dot (.) means 'everything here.'"
        ),
        sim_output="$ git add .",
    ),
    Exercise(
        type="scenario",
        prompt=(
            "You've staged your files with git add. Now you want to save\n"
            "a snapshot with the message 'Initial commit'.\n"
            "What command do you run?"
        ),
        answers=[
            'git commit -m "Initial commit"',
            "git commit -m 'Initial commit'",
        ],
        hint="Use the -m flag followed by your message in quotes.",
        explanation=(
            'git commit -m "message" saves a snapshot of staged files.\n'
            "The -m flag lets you write the commit message inline."
        ),
        sim_output=(
            '$ git commit -m "Initial commit"\n'
            "[main abc1234] Initial commit\n"
            " 3 files changed, 156 insertions(+)"
        ),
    ),
]

LEVEL_2 = Level(
    number=2,
    name="Staging & Committing",
    tagline="Save your work with Git",
    concept=(
        "The Git workflow is: edit files → stage them (git add) →\n"
        "commit them (git commit). Staging lets you choose exactly\n"
        "which changes go into each commit."
    ),
    commands_taught=["git add", "git commit"],
    teachings=LEVEL_2_TEACHINGS,
    exercises=LEVEL_2_EXERCISES,
)


# ═══════════════════════════════════════════════════════════
#  LEVEL REGISTRY
# ═══════════════════════════════════════════════════════════

# This dictionary maps level numbers to Level objects.
# The runner uses this to look up content: LEVELS[1] → Level 1
LEVELS = {
    0: SETUP_LEVEL,
    1: LEVEL_1,
    2: LEVEL_2,
}
```

### Understanding the structure:

```
LEVELS dict
  ├── 0: SETUP_LEVEL
  │     ├── teachings: [Teaching, Teaching]
  │     └── exercises: [Exercise, Exercise]
  ├── 1: LEVEL_1
  │     ├── teachings: [Teaching, Teaching]
  │     └── exercises: [Exercise, Exercise, Exercise]
  └── 2: LEVEL_2
        ├── teachings: [Teaching, Teaching]
        └── exercises: [Exercise, Exercise, Exercise]
```

---

## 🔹 Step 4 — Test Your Content

Add this at the bottom of `levels_mvp.py`:

```python
# Temporary test — delete this later
if __name__ == "__main__":
    for key, level in LEVELS.items():
        print(f"Level {level.number}: {level.name}")
        print(f"  Teachings: {len(level.teachings)}")
        print(f"  Exercises: {len(level.exercises)}")

        # Check every exercise has an explanation
        for i, ex in enumerate(level.exercises):
            if not ex.explanation:
                print(f"  ⚠️  Exercise {i+1} is MISSING an explanation!")
        print()
```

Run:

```
python -m content.levels_mvp
```

> **Why `-m content.levels_mvp` instead of `python content/levels_mvp.py`?**
> Because `levels_mvp.py` imports from `content.models`. When you run a file directly, Python doesn't know about the package structure. Using `-m` tells Python to treat it as a module inside a package.

**You should see:**

```
Level 0: Setup
  Teachings: 2
  Exercises: 2

Level 1: Init & Status
  Teachings: 2
  Exercises: 3

Level 2: Staging & Committing
  Teachings: 2
  Exercises: 3
```

No warnings about missing explanations? Good. **Delete the test code.**

---

## 🔹 Step 5 — Create the Stage Map (`content/stage_map.py`)

The stage map defines the ORDER the player goes through stages. It's the game's progression path.

Create `content/stage_map.py`:

```python
"""
GitGrind MVP — Stage progression map.
Defines the order stages are played in.
"""
from content.models import Stage

# The player goes through these stages in order.
# stage_type tells the runner what kind of stage it is.
# data_key tells the runner which level to load from LEVELS dict.
STAGE_MAP = [
    Stage(stage_type="setup", data_key=0, label="⚙️ Setup"),
    Stage(stage_type="level", data_key=1, label="Level 1 — Init & Status"),
    Stage(stage_type="level", data_key=2, label="Level 2 — Staging & Committing"),
]
```

### Test it:

```python
# Add to bottom of stage_map.py temporarily
if __name__ == "__main__":
    for i, stage in enumerate(STAGE_MAP):
        print(f"Stage {i}: [{stage.stage_type}] {stage.label} → Level {stage.data_key}")
```

Run:

```
python -m content.stage_map
```

**You should see:**

```
Stage 0: [setup] ⚙️ Setup → Level 0
Stage 1: [level] Level 1 — Init & Status → Level 1
Stage 2: [level] Level 2 — Staging & Committing → Level 2
```

**Delete the test code.**

---

## ✅ Checklist (Don't Move On Until)

- [ ] `content/levels_mvp.py` runs without import errors
- [ ] Setup level has teachings and exercises
- [ ] Level 1 and Level 2 have teachings and exercises
- [ ] Every exercise has an `explanation` (checked by your test)
- [ ] `content/stage_map.py` has 3 stages in order
- [ ] `LEVELS` dict maps numbers to Level objects

---

## 🛟 If Something Goes Wrong

**"ModuleNotFoundError: No module named 'content.models'"**
→ Make sure `content/__init__.py` exists. Run with `python -m content.levels_mvp` not `python content/levels_mvp.py`.

**Long strings look ugly in your code?**
→ Use parenthesized string concatenation:
```python
explanation=(
    "Line one.\n"
    "Line two.\n"
    "Line three."
)
```
Python automatically joins these strings together.

**"How many exercises per level?"**
→ For MVP: 2-4 per level is plenty. Quality over quantity.

---

**Phase 3 done? You have real content! Now build the answer checker → [phase4.md](phase4.md)**
