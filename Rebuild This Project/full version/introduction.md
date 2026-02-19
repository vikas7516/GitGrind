# 🎮 GitGrind Full Version — Build the Complete Game

---

## What You Are Building

You're taking your MVP — a 3-stage terminal game — and turning it into a complete Git learning platform with 35 stages, 8 exercise types, boss fights, drill zones, a command notebook, sound effects, and a glossary.

Here's everything in the full version:

```
35 stages total:
  ├── 1 setup intro
  ├── 21 teaching levels (basics → branching → remotes → advanced)
  ├── 7 exercise rounds (mixed review sessions)
  └── 6 boss fights (multi-step fail-fast challenges)

8 exercise types:
  recall, scenario, fill_blank, multi_choice,
  error_fix, multi_step, reverse, rapid_fire

Extra systems:
  ├── Retry loop (keep trying until correct, or skip)
  ├── Near-miss detection ("Almost! You had a typo…")
  ├── Drill zones (randomized review with pass/fail threshold)
  ├── Boss fights (sequential steps — one wrong = fail)
  ├── Command notebook (tracks what you've learned, exportable)
  ├── Sound effects (melodies for correct/wrong/clear/boss)
  ├── Streak tracking (consecutive correct answers)
  ├── Session summaries (stats for each play session)
  ├── Glossary (Git terms reference)
  └── Game completion rewards (cheatsheet + mastery report)
```

---

## How This Guide Works

> **The project code IS the full version.** Every `.py` file you see in this repository is the final, working code. This guide does NOT paste entire code files — instead, it teaches you HOW the code works, WHY it's designed that way, and WHAT each component does.

**When you see "Open `engine/validator.py`"**, open that file in the project, read it, and follow along as the guide explains each function line by line.

**You learn by understanding, not by copying.** A beginner can't stare at 400 lines of code and understand it. This guide breaks down every function, every design decision, every line of logic — so you understand not just WHAT the code does, but WHY.

---

## Prerequisites

**You MUST have a working MVP first.** This guide assumes:

- [x] Phase 1-8 of the MVP guide are complete
- [x] 3 stages play end-to-end
- [x] Tests pass
- [x] Save/load works

If any of these are false, go back to the MVP guide.

---

## Architecture

Every file in the full project, with its role:

```
GitGrind/
├── main.py                    ← Menu loop, stage dispatch, retry logic
├── ui.py                      ← ALL terminal display (813 lines, 49 functions)
├── notebook.py                ← Command notebook: track + export learned commands
├── sounds.py                  ← Sound effects via winsound (Windows) or silent fallback
├── validate.py                ← Codebase integrity checker (run anytime)
│
├── engine/
│   ├── validator.py           ← Answer checking (normalize, placeholders, 3 validators)
│   ├── state.py               ← Progress tracking, save/load, streaks, sessions
│   └── runner.py              ← Exercise/level/round/boss execution engine
│
├── content/
│   ├── models.py              ← Data shapes (Teaching, Exercise, Level, Round, Boss, Stage)
│   ├── levels_basics.py       ← Levels 1-6 (init, add, commit, ignore, diff, log)
│   ├── levels_branch.py       ← Levels 7-10 (branch, switch, merge, conflicts)
│   ├── levels_remote.py       ← Levels 11-14 (remote, clone, push, pull)
│   ├── levels_adv.py          ← Levels 15-21 (restore, revert, stash, reflog, rebase...)
│   ├── exercises.py           ← 7 exercise rounds (mixed review sessions)
│   ├── bossfights.py          ← 6 boss fights (multi-step scenarios)
│   ├── glossary.py            ← Git terminology glossary data
│   └── stage_map.py           ← Master progression: 35 stages in order
│
├── tests/
│   └── test_core.py           ← Unit tests for validator + state
│
├── save_data.json             ← Auto-generated player progress
└── requirements.txt           ← rich
```

### How Data Flows Through the System

When a player starts a level, this happens:

```
main.py                          ← Player presses "C" to continue
  │
  ├── state.current_stage_index  ← "Where am I?" → stage 5
  ├── STAGE_MAP[5]               ← "What kind?" → Level, data_key=3
  ├── ALL_LEVELS[3]              ← Get Level 3 (Committing)
  │
  └── runner.run_level(level)
        │
        ├── ui.show_level_header()     ← Show "Level 3 — Committing"
        ├── ui.show_teaching()         ← Show each lesson slide
        │
        ├── runner.run_exercise()      ← For each exercise:
        │     ├── ui.show_exercise_prompt()  ← Show the question
        │     ├── ui.get_input()              ← Read player's answer
        │     ├── validator.check_answer()    ← Correct?
        │     │
        │     ├── [if correct]
        │     │     ├── state.record_correct()
        │     │     ├── sounds.sound_correct()
        │     │     └── ui.show_correct()
        │     │
        │     └── [if wrong]
        │           ├── runner._retry_loop()     ← Keep trying!
        │           │     ├── _analyze_near_miss()  ← "Almost! Missing -m flag"
        │           │     └── ui.show_wrong_retry()
        │           └── state.record_wrong()
        │
        ├── [drill zone]
        │     ├── randomized drill questions
        │     ├── must score ≥ threshold to pass
        │     └── ui.show_drill_progress()
        │
        └── state.clear_stage() → state.save()
```

### Import Rules

These are strict — breaking them creates circular imports that crash on startup:

```
Content Layer:  content/*.py     ← NEVER imports engine/ or ui.py
Engine Layer:   engine/*.py      ← imports content, NEVER imports ui directly
UI Layer:       ui.py            ← imports content (for glossary)
Standalone:     notebook.py      ← imports nothing from engine
                sounds.py        ← imports nothing from the project
Orchestration:  main.py          ← imports everything
                runner.py        ← imports ui, validator, state
```

Why? Because if `content/models.py` imports `engine/runner.py`, and `engine/runner.py` imports `content/models.py`... Python tries to load both at once and crashes with `ImportError: cannot import name ... from partially initialized module`.

---

## The Stage Progression Map

All 35 stages, in order:

```
 1. ⚙️  Setup Intro
 2. Level 1  — Init & Status
 3. Level 2  — Staging Files
 4. Level 3  — Committing
 5. 💪 Exercise Round 1 — Absolute Basics
 6. Level 4  — .gitignore
 7. Level 5  — Seeing Changes
 8. Level 6  — Reading History
 9. 💪 Exercise Round 2 — Solo Repo Mastery
10. ⚔️ Boss Fight 1 — The Broken Repo
11. Level 7  — Branching
12. Level 8  — Switching Branches
13. Level 9  — Merging
14. Level 10 — Merge Conflicts
15. 💪 Exercise Round 3 — Branch Warfare
16. ⚔️ Boss Fight 2 — Three-Way Collision
17. 💪 Exercise Round 6 — Retention Sprint I
18. Level 11 — Remotes & Origin
19. Level 12 — Clone
20. Level 13 — Push
21. Level 14 — Pull & Fetch
22. 💪 Exercise Round 4 — Remote Ops
23. ⚔️ Boss Fight 3 — The Sync Disaster
24. Level 15 — Restore & Reset
25. Level 16 — Revert
26. Level 17 — Stash
27. Level 18 — Reflog
28. Level 19 — Rebase
29. Level 20 — Pro Moves
30. Level 21 — Maintenance & Team Flow
31. 💪 Exercise Round 5 — The Final Grind
32. ⚔️ Boss Fight 4 — Detached HEAD Nightmare
33. 💪 Exercise Round 7 — Retention Marathon
34. ⚔️ Boss Fight 5 — THE FINAL BOSS
35. ⚔️ Boss Fight 6 — COMMAND ARENA (GRAND FINAL)
```

Notice the pattern: **learn → practice → prove**. A few levels of teaching, then an exercise round to review, then a boss fight to prove mastery. This repeats for each topic area.

---

## Build Order

You build bottom-up, same as MVP — foundation first, wiring last:

```
Phase 1  → Foundation upgrade (new files, stubs, migrate MVP content)
Phase 2  → Expand data models (Round, BossFight, StageType enum, new Exercise fields)
Phase 3  → Upgrade validator (placeholder regex, fill_blank, multi_choice)
Phase 4  → Upgrade state engine (atomic writes, deep merge, streaks, sessions, notebook)
Phase 5  → Build the full runner (retry loop, near-miss, drills, boss fights, rounds)
Phase 6  → Wire main.py (stage dispatch, boss retry, replay, reset, notebook, glossary)
Phase 7  → Build the full UI (49 functions — teaching, exercises, feedback, maps, animations)
Phase 8  → Build supporting systems (notebook.py, sounds.py, validate.py, glossary)
Phase 9  → Author all content (21 levels + 7 rounds + 6 bosses across 4 topic areas)
Phase 10 → Testing, hardening, and release
```

Each phase has its own file. Follow them in order.

---

## What's Different From the MVP

| Concept | MVP | Full Version |
|---------|-----|--------------|
| Wrong answer | Show answer, move on | Retry until correct (with skip option) |
| Answer checking | Exact match only | Placeholder-aware, git-prefix-tolerant |
| Stage types | 1 (level) | 4 (setup, level, exercise round, boss fight) |
| Exercise types | 2 (recall, scenario) | 8 types with type-specific UI and validation |
| Persistence | Simple JSON dump | Atomic writes, schema evolution with deep merge |
| State tracking | Basic correct/wrong | Streaks, first-try tracking, session stats, notebook |
| Feedback | "Almost right" awareness | Fuzzy matching with SequenceMatcher, word-overlap hints |
| UI complexity | ~10 functions | 49 functions with animations, maps, panels |

Each of these upgrades is taught in its phase — with the thinking behind it, not just the code.

---

## Rules

1. **Build on top of your working MVP.** Don't start over.
2. **Run your app after every small change.**
3. **Fix bugs immediately.** Don't build on top of broken code.
4. **If you can't explain a line, don't move on.**

---

**Ready? Open [phase1.md](phase1.md) to start upgrading your foundation.**
