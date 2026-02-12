<div align="center">

# 🎮 GitGrind

### *Master Git Through Interactive Practice*

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Learn Git by doing. No repos needed. No frustration. Just results.**

[Quick Start](QUICKSTART.md) • [Features](#-features) • [Screenshots](#-screenshots) • [Installation](#-installation) • [How to Play](#-how-to-play) • [Contributing](#-contributing)

---

</div>

## 🌟 Why GitGrind?

Most Git tutorials teach you to **memorize commands**. GitGrind teaches you to **understand Git**.

- ✅ **Instant Feedback** - Learn from mistakes with clear explanations
- ✅ **Progressive Learning** - 20 levels from beginner to advanced
- ✅ **Real Scenarios** - Boss fights simulate actual workflows
- ✅ **No Setup Required** - Practice without creating repositories
- ✅ **Track Progress** - Save your journey and earn rewards
- ✅ **100% Educational** - 433 exercises with detailed explanations

## 📸 Screenshots

<!-- TODO: Add screenshots here
![Main Menu](screenshots/main-menu.png)
![Level Screen](screenshots/level.png)
![Exercise Example](screenshots/exercise.png)
-->

*Screenshots coming soon!*

## ✨ Features

### 🎓 **Comprehensive Learning Path**
- **20 Progressive Levels** - From `git init` to `git rebase --interactive`
- **5 Exercise Rounds** - Grinding sessions to build muscle memory  
- **5 Boss Fights** - Complex multi-step workflows
- **433 Total Exercises** - Each with contextual explanations

### 💡 **Smart Teaching System**
- **Teaching Slides** - Detailed explanations with examples before practice
- **Pro Tips** - Industry best practices throughout
- **Contextual Hints** - Get help when stuck
- **Error Explanations** - Understand WHY you were wrong, not just what's correct
- **8 Exercise Types** - Recall, scenarios, fill-blank, multi-choice, error-fixing, and more

### 📊 **Gamification & Progress**
- **XP System** - Earn experience and level up
- **Streak Tracking** - Build momentum with consecutive correct answers
- **Accuracy Stats** - Track improvement over time
- **Auto-Save** - Never lose progress
- **Cheat Sheet Reward** - Unlock a personalized command reference

### 🎨 **Beautiful Terminal UI**
- Powered by [Rich](https://github.com/Textualize/rich)
- Color-coded feedback
- Formatted code examples
- Clean, professional interface

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/gitgrind.git
cd gitgrind

# Install dependencies
pip install -r requirements.txt

# Launch the game
python main.py
```

### Alternative: Using Virtual Environment (Recommended)

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
2. Press **C** to start or continue your journey
3. Complete levels to progress through the curriculum

### During Gameplay
- **Type your answers** - Commands are validated in real-time
- **Type `hint`** - Get contextual help (when available)
- **Type `quit`** - Return to main menu anytime
- **Press Enter** - Continue through teaching slides

### Level Structure
Each level follows a proven learning pattern:

1. **📖 Concept Introduction** - Understand the why
2. **🎓 Teaching Phase** - Learn commands with examples
3. **✏️ Exercises** - Apply what you learned
4. **🔥 Drill Zone** - Rapid-fire practice (8/10 to pass)

### Progression System
- Clear **31 total stages** (20 levels + 5 rounds + 5 boss fights + setup)
- Earn **XP** for correct answers
- Build **streaks** for consecutive successes
- Unlock **cheat sheet** upon completion

## 📚 What You'll Learn

### 🟢 Beginner (Levels 1-6)
- Repository initialization and status
- Staging and committing changes
- Using .gitignore effectively  
- Viewing diffs and history
- Advanced log filtering

### 🟡 Intermediate (Levels 7-14)
- Creating and managing branches
- Switching between branches
- Merging strategies
- Resolving merge conflicts
- Working with remotes (GitHub/GitLab)
- Cloning, pushing, and pulling
- Fetch vs pull workflows

### 🔴 Advanced (Levels 15-20)
- Restoring and resetting changes
- Safe undo with revert
- Stashing work in progress
- Using reflog for recovery
- Interactive rebasing
- Cherry-picking commits
- Tagging releases
- Force-push safely
- Git blame and aliases

### 💪 Boss Fights
1. **The Broken Repo** - Fix .gitignore mistakes
2. **Three-Way Collision** - Merge multiple conflicting branches
3. **The Sync Disaster** - Resolve push/pull conflicts
4. **Detached HEAD Nightmare** - Recover lost commits
5. **THE FINAL BOSS** - Complete professional workflow from clone to release

## 📊 Content Overview

| Component | Count | Description |
|-----------|-------|-------------|
| **Levels** | 20 | Progressive learning modules |
| **Exercise Rounds** | 5 | Focused practice sessions |
| **Boss Fights** | 5 | Multi-step challenges |
| **Total Exercises** | 433 | Each with explanations |
| **Commands Taught** | 60+ | From basics to advanced |
| **Teaching Slides** | 50+ | Detailed explanations |

## 🛠️ Project Structure

```
gitgrind/
├── main.py                    # Entry point and game loop
├── ui.py                      # Rich-powered terminal UI
├── cheatsheet.py              # Reward generator
├── requirements.txt           # Python dependencies
├── save_data.json             # Progress persistence
├── tests/                     # Unit tests
│   └── test_validator.py
├── engine/                    # Game logic
│   ├── __init__.py
│   ├── runner.py              # Exercise execution
│   ├── state.py               # State management & save/load
│   └── validator.py           # Answer validation
└── content/                   # Educational content
    ├── __init__.py
    ├── models.py              # Data structures
    ├── stage_map.py           # Progression mapping
    ├── levels_basics.py       # Levels 1-6
    ├── levels_branch.py       # Levels 7-10
    ├── levels_remote.py       # Levels 11-14
    ├── levels_adv.py          # Levels 15-20
    ├── exercises.py           # Exercise rounds 1-5
    └── bossfights.py          # Boss fights 1-5
```

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/test_validator.py
```

## 🎓 Learning Philosophy

GitGrind is built on proven educational principles:

1. **Active Learning** - Learning by doing, not passive reading
2. **Immediate Feedback** - Explanations appear when you need them
3. **Spaced Repetition** - Drill zones reinforce knowledge
4. **Progressive Difficulty** - Build on previous concepts
5. **Contextual Understanding** - Learn WHY commands work, not just HOW

## 📄 Documentation

For developers and contributors, additional technical documentation is available:
- See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- Check the `/content` directory for exercise and level structure
- Review `/engine` for game logic and validation

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

- 🐛 **Report bugs** - Open an issue with reproduction steps
- 💡 **Suggest features** - Share ideas for new exercises or features
- 📝 **Improve content** - Submit better explanations or exercises
- 🔧 **Fix issues** - Submit PRs for open issues
- 📚 **Write docs** - Help improve documentation

### Development Setup

```bash
git clone https://github.com/yourusername/gitgrind.git
cd gitgrind
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python -m pytest  # Run tests
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Inspired by real Git pain points and learning challenges
- Thanks to all contributors and beta testers

## 🌟 Star History

If GitGrind helped you learn Git, please ⭐ star this repository!

---

<div align="center">

**Made with ❤️ for developers learning Git**

[Report Bug](https://github.com/yourusername/gitgrind/issues) • [Request Feature](https://github.com/yourusername/gitgrind/issues) • [Discussions](https://github.com/yourusername/gitgrind/discussions)

**Keep grinding. You've got this. 🚀**

</div>

