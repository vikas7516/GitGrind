# 🚀 PHASE 6 — The Runner (Making It Playable)

---

## 🎯 Goal

Connect all your pieces into a working game loop:

```
Show level intro → Show teachings → Show exercises → Check answers → Give feedback → Save progress
```

After this phase, you can actually PLAY your game.

This is the biggest phase because you'll:
1. Add new display functions to `ui.py`
2. Build the runner (`engine/runner.py`)
3. Update `main.py` to use everything

---

## 🔹 Step 1 — Add UI Functions to `ui.py`

Your runner needs these display functions. Open `ui.py` and add them.

Here's the complete updated `ui.py`:

```python
"""
GitGrind — Terminal UI.
All display and input functions live here.
"""
import os
from rich.console import Console
from rich.panel import Panel

console = Console()


def clear():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    """Wait for the user to press Enter."""
    console.print()
    console.input("  [dim]Press Enter to continue...[/dim]")


def get_input(prompt_text="  ▸ "):
    """Read and clean user input. Returns 'quit' on Ctrl+C."""
    try:
        user_text = input(prompt_text)
        return user_text.strip().lower()
    except (KeyboardInterrupt, EOFError):
        print()
        return "quit"


def show_main_menu(state, total_stages):
    """
    Display the main menu with progress stats.

    Args:
        state: GameState object (for showing progress)
        total_stages: Total number of stages in the game
    """
    clear()

    console.print(Panel(
        "[bold bright_cyan]⚡ GitGrind[/bold bright_cyan]",
        border_style="bright_cyan",
    ))

    # Show progress
    cleared = len(state.cleared_stages)
    acc = state.accuracy
    console.print(f"  Stages: {cleared}/{total_stages}  |  Accuracy: {acc:.0f}%")
    console.print()
    console.print("  [bold][C][/bold]  Continue")
    console.print("  [bold][Q][/bold]  Quit")
    console.print()


def show_level_intro(level):
    """Show the level name and concept before teachings begin."""
    clear()
    console.print()
    console.print(f"  [bold bright_cyan]━━━ {level.name} ━━━[/bold bright_cyan]")
    console.print(f"  [dim]{level.tagline}[/dim]")
    console.print()
    console.print(f"  {level.concept}")
    console.print()
    console.print(f"  [dim]Commands: {', '.join(level.commands_taught)}[/dim]")
    pause()


def show_teaching(teaching):
    """Display one teaching slide (lesson)."""
    clear()
    console.print()
    console.print(f"  [bold yellow]📖 LESSON → {teaching.command}[/bold yellow]")
    console.print()
    console.print(f"  {teaching.explanation}")
    console.print()

    # Show syntax in a box
    console.print(Panel(
        f"  {teaching.syntax}",
        title="Syntax",
        border_style="green",
    ))

    # Show example output
    if teaching.example_output:
        console.print(f"  [dim]Example:[/dim]")
        for line in teaching.example_output.split("\n"):
            console.print(f"    [dim]{line}[/dim]")
        console.print()

    # Show pro tip if available
    if teaching.pro_tip:
        console.print(f"  [italic bright_cyan]💡 {teaching.pro_tip}[/italic bright_cyan]")
        console.print()

    pause()


def show_exercise(exercise, index, total):
    """
    Display an exercise prompt.

    Args:
        exercise: Exercise object
        index: Current exercise number (1, 2, 3...)
        total: Total number of exercises in this level
    """
    console.print()
    console.print(f"  [bold]Exercise {index}/{total}[/bold]")
    console.print()
    console.print(f"  {exercise.prompt}")
    console.print()


def show_correct(sim_output=None):
    """
    Show positive feedback for a correct answer.

    Args:
        sim_output: Optional simulated terminal output to display
    """
    console.print()
    console.print("  [bold green]✅ Correct![/bold green]")

    if sim_output:
        console.print()
        for line in sim_output.split("\n"):
            console.print(f"    [dim]{line}[/dim]")

    console.print()


def show_wrong(correct_answer, explanation=""):
    """
    Show feedback for a wrong answer.

    Args:
        correct_answer: The expected answer string
        explanation: Why this answer is correct
    """
    console.print()
    console.print("  [bold red]❌ Not quite.[/bold red]")
    console.print(f"  [yellow]Expected:[/yellow] {correct_answer}")

    if explanation:
        console.print()
        console.print(f"  [dim]{explanation}[/dim]")

    console.print()


def show_hint(hint_text):
    """Show a hint in a styled panel."""
    console.print()
    console.print(Panel(
        f"  {hint_text}",
        title="💡 Hint",
        border_style="yellow",
    ))
    console.print()


def show_level_complete(level, correct, total):
    """
    Show a summary after completing a level.

    Args:
        level: The Level object that was completed
        correct: Number of correct answers
        total: Total number of exercises
    """
    console.print()
    console.print(Panel(
        f"  [bold green]✅ {level.name} — Complete![/bold green]\n"
        f"  Score: {correct}/{total}",
        border_style="green",
    ))
    pause()
```

### What each new function does:

| Function | When It's Called | What It Shows |
|----------|-----------------|---------------|
| `show_main_menu(state, total)` | Before every menu prompt | Game title + progress + options |
| `show_level_intro(level)` | When starting a new level | Level name, concept, commands |
| `show_teaching(teaching)` | For each lesson in a level | Command, explanation, syntax, example |
| `show_exercise(ex, i, n)` | Before each exercise | "Exercise 2/4" + the question |
| `show_correct(sim_output)` | When answer is right | Green ✅ + simulated output |
| `show_wrong(answer, expl)` | When answer is wrong | Red ❌ + expected answer + why |
| `show_hint(text)` | When player types "hint" | Hint in a yellow box |
| `show_level_complete(...)` | After finishing a level | Score summary in a green box |

### Test the new UI functions:

```python
# Add to bottom of ui.py temporarily
if __name__ == "__main__":
    from content.models import Teaching, Exercise

    # Test teaching slide
    t = Teaching(
        command="git init",
        explanation="Creates a new Git repo in your current folder.",
        syntax="git init",
        example_output="$ git init\nInitialized empty Git repository",
        pro_tip="Only run this once per project."
    )
    show_teaching(t)

    # Test correct feedback
    show_correct("$ git init\nInitialized empty Git repository")
    pause()

    # Test wrong feedback
    show_wrong("git init", "git init creates a new Git repository.")
    pause()

    # Test hint
    show_hint("This command creates a hidden .git folder.")
    pause()
```

Run `python ui.py`, check that everything displays nicely, then **delete the test code**.

---

## 🔹 Step 2 — Build the Runner (`engine/runner.py`)

This file orchestrates the game — it calls UI functions, validates answers, and updates state. Each function has ONE job.

Create `engine/runner.py`:

```python
"""
GitGrind — Game runner.
Orchestrates the flow: teachings → exercises → feedback → state updates.
"""
import ui
from engine.validator import check_answer


# Sentinel object — a unique value that means "player wants to quit."
# We can't use True/False because those mean "correct" and "wrong."
# We can't use None because that could be a missing value.
# object() creates a unique item that nothing else can be equal to.
QUIT_SENTINEL = object()


def run_exercise(exercise, state, index=None, total=None):
    """
    Run a single exercise from start to finish.

    Flow:
        1. Show the exercise prompt
        2. Read the player's answer
        3. Handle "quit" and "hint" commands
        4. Check if the answer is correct
        5. Show feedback and update stats
        6. Return the result

    Returns:
        True           — player answered correctly
        False          — player answered incorrectly
        QUIT_SENTINEL  — player typed "quit"
    """
    # 1. Show the exercise
    ui.show_exercise(exercise, index, total)

    # 2. Get the player's answer
    user_input = ui.get_input()

    # 3. Handle special commands
    if user_input == "quit":
        return QUIT_SENTINEL

    if user_input == "hint":
        if exercise.hint:
            ui.show_hint(exercise.hint)
            state.record_hint()
        else:
            ui.console.print("  [dim]No hint available for this one.[/dim]")

        # After showing the hint, ask for the answer again
        user_input = ui.get_input()
        if user_input == "quit":
            return QUIT_SENTINEL

    # 4. Check the answer
    is_correct, matched = check_answer(user_input, exercise.answers)

    # 5. Give feedback and update stats
    if is_correct:
        state.record_correct()
        ui.show_correct(exercise.sim_output)
        return True
    else:
        state.record_wrong()
        ui.show_wrong(exercise.answers[0], exercise.explanation)
        return False


def run_level(level, state):
    """
    Run a complete level: intro → teachings → exercises → result.

    Returns:
        True           — level completed
        QUIT_SENTINEL  — player quit mid-level
    """
    # 1. Show level intro
    ui.show_level_intro(level)

    # 2. Show each teaching slide
    for teaching in level.teachings:
        ui.show_teaching(teaching)

    # 3. Run each exercise
    correct = 0
    total = len(level.exercises)

    for i, exercise in enumerate(level.exercises):
        result = run_exercise(exercise, state, index=i + 1, total=total)

        if result is QUIT_SENTINEL:
            return QUIT_SENTINEL
        if result is True:
            correct += 1

    # 4. Show level complete summary
    ui.show_level_complete(level, correct, total)
    return True
```

### Understanding the flow:

```
run_level("Init & Status", state)
  ├── show_level_intro()
  ├── show_teaching("git init")         ← player reads lesson
  ├── show_teaching("git status")       ← player reads lesson
  ├── run_exercise(exercise_1, state)   ← player answers
  │     ├── show_exercise()             ← shows the question
  │     ├── get_input()                 ← reads their answer
  │     ├── check_answer()              ← checks if correct
  │     └── show_correct/show_wrong()   ← gives feedback
  ├── run_exercise(exercise_2, state)   ← player answers
  ├── run_exercise(exercise_3, state)   ← player answers
  └── show_level_complete()             ← shows score
```

Each function calls other functions. Nobody does more than their own job.

### Why `is` instead of `==`?

```python
if result is QUIT_SENTINEL:  # ✅ Correct — identity check
if result == QUIT_SENTINEL:  # ❌ Wrong — equality check
```

`is` checks if two variables point to the **same object in memory**. Since `QUIT_SENTINEL = object()` creates a unique object, `is` is the correct way to check for it.

---

## 🔹 Step 3 — Update `main.py` (Wire Everything Together)

Now update `main.py` to use the runner and state. Replace the entire file:

```python
"""
GitGrind — Main entry point.
Runs the menu loop and dispatches stages.
"""
import ui
from engine.state import GameState
from engine.runner import run_level, QUIT_SENTINEL
from content.levels_mvp import LEVELS
from content.stage_map import STAGE_MAP


def main():
    """Main game loop."""
    # Load saved progress (or start fresh)
    state = GameState()
    state.load()

    total_stages = len(STAGE_MAP)

    try:
        while True:
            # Show menu with current progress
            ui.show_main_menu(state, total_stages)

            choice = ui.get_input("  Choose: ")

            if choice in ("c", "continue"):
                # Check if the player has finished all stages
                if state.current_stage_index >= total_stages:
                    ui.console.print("\n  [bold green]🏆 You've completed all stages![/bold green]")
                    ui.console.print("  [dim]You can reset progress to play again.[/dim]")
                    ui.pause()
                    continue

                # Get the current stage from the map
                stage = STAGE_MAP[state.current_stage_index]

                # Look up the level content
                level = LEVELS[stage.data_key]

                # Run the level
                result = run_level(level, state)

                if result is QUIT_SENTINEL:
                    # Player typed "quit" during a level — just go back to menu
                    continue

                # Level completed — save progress
                state.clear_stage(state.current_stage_index)
                state.save()

            elif choice in ("q", "quit"):
                state.save()
                ui.console.print("\n  [dim]Progress saved. Goodbye![/dim]\n")
                break

            else:
                ui.console.print("\n  [red]Invalid option. Try C or Q.[/red]")
                ui.pause()

    except KeyboardInterrupt:
        state.save()
        ui.console.print("\n\n  [dim]Progress saved. Goodbye![/dim]\n")


if __name__ == "__main__":
    main()
```

### What changed from Phase 1:

| Before (Phase 1) | After (Phase 6) |
|-------------------|------------------|
| `show_main_menu()` with no arguments | `show_main_menu(state, total_stages)` shows progress |
| "Game starting soon..." placeholder | Actually runs a level with `run_level()` |
| No imports except `ui` | Imports state, runner, content, stage map |
| No save/load | Loads on startup, saves on quit and after each stage |

---

## 🔹 Step 4 — Play Your Game!

```
python main.py
```

### Full Test Walkthrough:

**Test 1 — First Run (no save file):**

1. Press `C` → Setup stage starts
2. Read the teaching slides (press Enter to advance)
3. Answer the exercises — try getting some right and some wrong
4. After all exercises → see "Setup — Complete!" with your score
5. Back at menu → press `C` → Level 1 starts (not Setup again!)
6. Press `Q` → "Progress saved. Goodbye!"

**Test 2 — Resume:**

7. Run `python main.py` again
8. Menu should show "Stages: 1/3" (you cleared setup)
9. Press `C` → Level 1 starts (not Setup — it remembers!)

**Test 3 — Hints:**

10. During an exercise, type `hint` → should see hint in yellow box
11. Then type your actual answer

**Test 4 — Quit Mid-Level:**

12. During an exercise, type `quit` → should return to menu (not crash)
13. Press `C` again → same stage restarts from the beginning

**Test 5 — Completion:**

14. Complete all 3 stages
15. Press `C` → should say "You've completed all stages!"

**If anything fails**, check the "If Something Goes Wrong" section below.

---

## ✅ Checklist (Don't Move On Until)

- [ ] Can complete Setup from the menu
- [ ] Can complete Level 1 after Setup
- [ ] Teaching slides display before exercises
- [ ] Correct answer shows ✅ with simulated output
- [ ] Wrong answer shows ❌ with expected answer + explanation
- [ ] Typing `hint` shows the hint (if one exists)
- [ ] Typing `quit` during an exercise returns to menu
- [ ] Progress saves between sessions (close → reopen → resumes)
- [ ] Menu shows correct Stages count and Accuracy

---

## 🛟 If Something Goes Wrong

**"ModuleNotFoundError: No module named 'engine.validator'"**
→ Make sure `engine/__init__.py` exists. Run from the project root (`GitGrind-MVP/` folder).

**Teaching slides don't appear**
→ Check that `level.teachings` isn't empty in `levels_mvp.py`.

**Wrong answer shows no explanation**
→ Check that every Exercise in `levels_mvp.py` has an `explanation` string.

**Stage doesn't advance after completion**
→ Check that `state.clear_stage()` is called in `main.py` after `run_level` returns True.

**"QUIT_SENTINEL" crashes with NameError**
→ Make sure you import it in `main.py`: `from engine.runner import run_level, QUIT_SENTINEL`

**Game resets progress every time**
→ Check that `state.load()` is called BEFORE the menu loop starts, and `state.save()` is called after clearing a stage.

---

**Phase 6 done? YOUR GAME IS PLAYABLE! 🎮 Now let's make it reliable with tests → [phase7.md](phase7.md)**
