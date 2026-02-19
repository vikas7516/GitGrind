# 🚀 PHASE 9 — Content Authoring

---

## 🎯 Goal

Build the entire game curriculum: 21 levels, 7 exercise rounds, 6 boss fights, and the stage map that sequences it all.

This is where the engine becomes a game. You will write the **content**: the explanations, the drills, the stories, and the progression logic.

> **Open `content/stage_map.py` and any file in `content/` (e.g. `levels_basics.py`) to follow along.**

---

## What You'll Learn

- **The Progression Pattern**: Learn → Grind → Test → Review.
- **Level Anatomy**: Converting concepts into `Teaching` and `Exercise` objects.
- **Exercise Rounds**: Designing drilled repetition with pass thresholds.
- **Boss Fights**: Building multi-step narrative challenges.
- **Stage Mapping**: Sequencing 35 distinct stages into a logical flow.

---

## Step 1 — The Progression Pattern

The game follows a strict pedagogical rhythm defined in `content/stage_map.py`:

```
1. Learn (3 Levels)      → Introduces new commands (init, add, commit)
2. Grind (Exercise Round) → Drills those commands (80% pass required)
3. Learn (3 More Levels) → Adds complexity (diff, log, .gitignore)
4. Grind (Exercise Round) → Drills new + old commands
5. Boss (Boss Fight)     → A real-world scenario combining EVERYTHING
```

This pattern ensures **mastery before progression**. You can't reach the Boss until you prove you know the commands in the Exercise Round. You can't reach the Exercise Round until you've seen the Teaching in the Levels.

### Spaced Repetition

Note the "Retention Sprints" in the stage map. These appear **between** major topics (e.g. after Boss 2 but before Remotes). They force the player to recall *everything* learned so far, preventing early concepts from fading.

---

## Step 2 — Anatomy of a Level

Levels are defined in `content/levels_*.py`. Unlike typical games where levels are code, here they are **data**.

A `Level` object contains:
1.  **Metadata**: Number, name, tagline, concept explanation.
2.  **Teachings**: List of `Teaching` objects (slides).
3.  **Exercises**: List of `Exercise` objects (immediate practice).

### The Content Definition

```python
LEVEL_1 = Level(
    number=1,
    name="Git Init & Status",
    tagline="Start tracking your project.",
    concept="Git needs to be told to watch your folder...",
    commands_taught=["git init", "git status"],
    teachings=[
        Teaching(
            command="git init",
            syntax="git init",
            explanation="Creates a hidden .git folder...",
            example_output="Initialized empty Git repository...",
            pro_tip="Only run this once per project!"
        ),
        # ... more teachings
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="What command creates the .git folder?",
            answers=["git init"],
            explanation="This turns a regular folder into a repo."
        ),
        # ... more exercises
    ]
)
```

**Why separate `teachings` and `exercises`?**
The engine runs them in two phases:
1.  **Lecture Mode**: Player reads through `Teaching` slides.
2.  **Quiz Mode**: Player answers `Exercise` questions immediately to reinforce the lecture.

---

## Step 3 — Exercise Rounds (The Grind)

Exercise Rounds are distinct from Levels. They have NO teaching — only testing.

```python
EXERCISE_ROUND_1 = ExerciseRound(
    number=1,
    pass_threshold=(12, 15),  # 80% to pass
    exercises=[
        # A pool of ~20-30 different exercises
    ]
)
```

**Pass Threshold `(12, 15)`**:
This means the engine will pick 15 exercises (randomly shuffled from the pool) and the player must get 12 right. This provides **replayability** — if they fail, they might get a slightly different set of questions next time.

### Question Mix

Good rounds mix valid `Exercise` types:
-   **`recall`**: "What command commits?"
-   **`fill_blank`**: "git commit -m '____'"
-   **`reverse`**: "What command produced this output?"
-   **`error_fix`**: "Fatal: not a git repo. Fix it."

---

## Step 4 — Boss Fights (The Test)

Boss Fights are linear stories. Unlike Rounds (where order is random), Boss steps are **sequential**.

```python
BOSS_FIGHT_1 = BossFight(
    name="The Broken Repo",
    story="You accidentally committed node_modules. Fix it.",
    steps=[
        Exercise(..., prompt="First, check status."),
        Exercise(..., prompt="Now create a .gitignore."),
        Exercise(..., prompt="Remove the cached files."),
        Exercise(..., prompt="Commit the fix."),
    ]
)
```

**The "Fail-Fast" Rule**:
In a Boss Fight, if you get **one step wrong**, you fail the entire fight. No hints. No skipping (until mercy rule kicks in). This simulates the high-stakes feel of breaking a production repo.

**The Narrative**:
Boss 1 is "Cleanup". Boss 2 is "Merge Conflict". Boss 3 is "Sync Disaster". Each fight represents a specific *pain point* every developer encounters.

---

## Step 5 — The Stage Map (`stage_map.py`)

This file is the **spine** of the game. It lists every `Stage` in order.

```python
STAGE_MAP = [
    Stage(STAGE_SETUP, 0, "Setup"),
    Stage(STAGE_LEVEL, 1, "Level 1"),
    Stage(STAGE_LEVEL, 2, "Level 2"),
    Stage(STAGE_LEVEL, 3, "Level 3"),
    Stage(STAGE_EXERCISE, 1, "Round 1"),
    # ...
    Stage(STAGE_BOSS, 6, "GRAND FINAL"),
]
```

**Why a list of objects?**
It separates the *definition* of content (Levels) from the *sequencing* (Map). You could reorder the levels just by changing this list, without touching the level files themselves.

### Startup Validation (from Phase 6)

Remember `main.py`? It iterates this `STAGE_MAP` and verifies that every `data_key` exists in your content dictionaries. This ensures you never ship a broken map.

---

## ✅ Quality Gate

- [ ] **Completeness**: 21 Levels, 7 Rounds, 6 Bosses defined.
- [ ] **Progression**: Taught commands appear in subsequent Rounds.
- [ ] **Variety**: Rounds use multiple question types (`recall`, `reverse`, `error_fix`).
- [ ] **Narrative**: Boss fights tell a coherent story (Problem → Diagnosis → Fix).
- [ ] **Thresholds**: Rounds require ~80% accuracy (challenging but fair).
- [ ] **Map Validity**: All stages in `STAGE_MAP` resolve to actual content.

---

**Phase 9 complete? Finish and Distribute → [phase10.md](phase10.md)**
