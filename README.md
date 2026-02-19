<div align="center">

# 🎮 GitGrind

### *Master Git Through Interactive Practice*

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Learn Git by doing. No repos needed. No frustration. Just results.**

[Quick Start](QUICKSTART.md) • [Build From Scratch](Rebuild%20This%20Project/full%20version/introduction.md) • [Features](#-features) • [Installation](#-installation) • [How to Play](#-how-to-play) • [Contributing](#-contributing)

---

</div>

## 🌟 Why GitGrind?

Most Git tutorials teach you to **memorize commands**. GitGrind teaches you to **understand Git**.

- ✅ **Instant Feedback** — Learn from mistakes with clear explanations
- ✅ **Progressive Learning** — 21 levels from beginner to advanced
- ✅ **Real Scenarios** — Boss fights simulate actual workflows
- ✅ **No Setup Required** — Practice without creating repositories
- ✅ **Track Progress** — Save your journey and earn rewards
- ✅ **400+ Exercises** — Each with detailed explanations

## 🏗️ Want to build this?
> **This entire project is a tutorial.**
> You can rebuild GitGrind from scratch — line by line — to master Python architecture.
>
> 👉 **[Start the "Rebuild This Project" Guide](Rebuild%20This%20Project/full%20version/introduction.md)**

## ✨ Features

### 🎓 Comprehensive Learning Path
- **21 Progressive Levels** — From `git init` to advanced maintenance workflows
- **7 Exercise Rounds** — Grinding + spaced-repetition sessions
- **6 Boss Fights** — Complex multi-step workflows (including final gauntlet)
- **400+ Total Exercises** — Each with contextual explanations

### 💡 Smart Teaching System
- **Teaching Slides** — Detailed explanations with examples before practice
- **Pro Tips** — Industry best practices throughout
- **Contextual Hints** — Type `hint` when you're stuck
- **Retry / Skip System** — Wrong answers enter a retry loop; skip unlocks after 2 retries with a side-by-side comparison of your answer vs the correct one
- **"Almost Right" Detection** — Near-miss feedback for typos, missing parts, and extra arguments (e.g. *"Almost! Tiny fix needed: add 'm'"*)
- **Quick Recap** — A command summary panel appears before each drill zone
- **8 Exercise Types** — Recall, scenarios, fill-blank, multi-choice, error-fixing, reverse, multi-step, and rapid fire

### 📖 Git Glossary
- **22 terms** explained in plain English — no jargon
- **5 categories**: Core Concepts, Working Areas, Everyday Actions, History & Debugging, Advanced
- **First-launch walkthrough** — automatically shown on your very first run
- **Always accessible** from the main menu via **[G]**

### 📓 Notebook
- **Auto-populated** as you complete lessons — every command you learn is saved
- **Organized by category** (Basics, Branching, Remotes, Advanced, etc.)
- **Includes syntax, explanation, and pro tips** for each command
- **Export to text file** — save your notebook as `git_notebook.txt` anytime

### 📊 Gamification & Progress
- **Streak Tracking** — Build momentum with consecutive correct answers
- **Accuracy Stats** — Overall and first-try accuracy tracked
- **Session Summary** — See your performance each time you return to the menu
- **Auto-Save** — Never lose progress
- **Mastery Rank** — Earn your rank upon completion (Grandmaster / Pro / Practitioner / Graduate)

### 🎨 Beautiful Terminal UI
- Powered by [Rich](https://github.com/Textualize/rich)
- Color-coded feedback and progress bars
- Formatted code examples and comparison panels
- Visual separators and clean spacing
- **Sound feedback** — Multi-note melodies for correct answers, wrong answers, streaks, stage clears, boss intros, and more (Windows; silent fallback on other platforms)

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Quick Start

```bash
# Clone the repository
git clone https://github.com/vikas7516/GitGrind.git
cd GitGrind

# Install dependencies
pip install -r requirements.txt

# Launch the game
python main.py
```

### Using a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install and run
pip install -r requirements.txt
python main.py
```

## 🎯 How to Play

### Getting Started
1. Launch with `python main.py`
2. On first launch, read through the **Git Glossary** — key terms explained simply
3. Press **C** to start or continue your journey
4. Complete levels to progress through the curriculum

### During Gameplay
| Command | Action |
|---------|--------|
| *(type your answer)* | Submit answer — validated in real-time |
| `hint` | Get contextual help (during exercises) |
| `skip` | Skip after 2 wrong retries — shows answer comparison |
| `quit` | Return to main menu (progress saved) |
| `Enter` | Continue through teaching slides |

### Main Menu
| Key | Action |
|-----|--------|
| **C** | Continue / Start your journey |
| **R** | Replay a cleared stage |
| **N** | Open your Notebook (view & export learned commands) |
| **G** | Open the Git Glossary (terminology reference) |
| **X** | Reset all progress |
| **Q** | Quit |

### Level Structure
Each level follows a proven learning pattern:

1. **📖 Concept Introduction** — Understand the why
2. **🎓 Teaching Phase** — Learn commands with examples (saved to Notebook)
3. **✏️ Exercises** — Apply what you learned (with retry/skip)
4. **📋 Quick Recap** — Command summary before the drill
5. **🔥 Drill Zone** — Rapid-fire practice (8/10 to pass)

### Progression System
- Clear **35 total stages** (21 levels + 7 rounds + 6 boss fights + setup)
- Build **streaks** for consecutive successes
- Track **overall and first-try accuracy**
- View **session summary** after each play session
- Earn your **mastery rank** upon completion

## 📚 What You'll Learn

### 🟢 Beginner (Levels 1–6)
- Repository initialization and status
- Staging and committing changes
- Using .gitignore effectively
- Viewing diffs and history
- Advanced log filtering

### 🟡 Intermediate (Levels 7–14)
- Creating and managing branches
- Switching between branches
- Merging strategies
- Resolving merge conflicts
- Working with remotes (GitHub/GitLab)
- Cloning, pushing, and pulling
- Fetch vs pull workflows

### 🔴 Advanced (Levels 15–21)
- Restoring and resetting changes
- Safe undo with revert
- Stashing work in progress
- Using reflog for recovery
- Interactive rebasing
- Cherry-picking commits
- Tagging releases
- Force-push safely
- Git blame and aliases
- Maintenance commands (show/clean/mv/grep)
- Branch comparison and squash merge
- Bisect workflow for regression hunting

### 💪 Boss Fights
1. **The Broken Repo** — Fix .gitignore mistakes
2. **Three-Way Collision** — Merge multiple conflicting branches
3. **The Sync Disaster** — Resolve push/pull conflicts
4. **Detached HEAD Nightmare** — Recover lost commits
5. **THE FINAL BOSS** — Complete professional workflow from clone to release
6. **COMMAND ARENA (GRAND FINAL)** — Multi-phase all-commands gauntlet

## 📊 Content Overview

| Component | Count | Description |
|-----------|-------|-------------|
| **Levels** | 21 | Progressive learning modules |
| **Exercise Rounds** | 7 | Focused + spaced-repetition sessions |
| **Boss Fights** | 6 | Multi-step challenges |
| **Total Exercises** | 400+ | Each with explanations |
| **Commands Taught** | 70+ | From basics to advanced |
| **Teaching Slides** | 60+ | Detailed explanations |
| **Glossary Terms** | 22 | Plain-English definitions |

## 🛠️ Project Structure

```
GitGrind/
├── main.py                    # Entry point and game loop
├── ui.py                      # Rich-powered terminal UI
├── sounds.py                  # Sound feedback (winsound melodies)
├── notebook.py                # Notebook system (categories + export)
├── validate.py                # Codebase integrity checker
├── requirements.txt           # Python dependencies
├── tests/
│   └── test_core.py           # Unit tests
├── engine/
│   ├── runner.py              # Exercise execution + retry/skip loop
│   ├── state.py               # State management + save/load
│   └── validator.py           # Answer validation + fuzzy matching
└── content/
    ├── models.py              # Data structures (Level, Exercise, Teaching)
    ├── stage_map.py           # Stage progression mapping
    ├── glossary.py            # Git terminology glossary
    ├── levels_basics.py       # Levels 1–6
    ├── levels_branch.py       # Levels 7–10
    ├── levels_remote.py       # Levels 11–14
    ├── levels_adv.py          # Levels 15–21
    ├── exercises.py           # Exercise rounds 1–7
    └── bossfights.py          # Boss fights 1–6
```

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest tests/ -v

# Run codebase validation
python validate.py
```

## 🎓 Learning Philosophy

GitGrind is built on proven educational principles:

1. **Active Learning** — Learning by doing, not passive reading
2. **Immediate Feedback** — Explanations appear when you need them
3. **Spaced Repetition** — Drill zones and exercise rounds reinforce knowledge
4. **Progressive Difficulty** — Build on previous concepts
5. **Contextual Understanding** — Learn WHY commands work, not just HOW

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

- 🐛 **Report bugs** — Open an issue with reproduction steps
- 💡 **Suggest features** — Share ideas for new exercises or features
- 📝 **Improve content** — Submit better explanations or exercises
- 🔧 **Fix issues** — Submit PRs for open issues

### Development Setup

```bash
git clone https://github.com/vikas7516/GitGrind.git
cd GitGrind
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python -m pytest  # Run tests
```

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Inspired by real Git pain points and learning challenges

---

<div align="center">

**Made with ❤️ for developers learning Git**

[Report Bug](https://github.com/vikas7516/GitGrind/issues) • [Request Feature](https://github.com/vikas7516/GitGrind/issues)

**Keep grinding. You've got this. 🚀**

</div>
