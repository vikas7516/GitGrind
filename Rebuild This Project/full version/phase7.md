# 🚀 PHASE 7 — The Terminal UI

---

## 🎯 Goal

Build the full UI module — 30+ functions powered by the **Rich** library that handle every visual aspect of the game. This includes the logo, menus, progress bars, feedback panels, teaching slides, and success animations.

The UI is the "face" of your code. A clean, colorful terminal UI makes a simple script feel like a professional product.

> **Open `ui.py` and follow along.** This guide explains how to build a beautiful CLI (Command Line Interface) using modern Python tools.

---

## What You'll Learn

- The **Rich Markup Syntax** (`[bold bright_green]text[/]`)
- How `Panel()` creates bordered, professional containers
- How to format data with `Table()` (no ASCII art needed)
- Visualizing math: converting percentages to block characters (`██░░`)
- Adaptive color thresholds (Red → Orange → Yellow → Green)
- Safe input handling with `get_input()`

---

## Step 1 — The Rich Library Crash Course

GitGrind uses [Rich](https://github.com/Textualize/rich) for all its visuals. Rich is HTML for the terminal.

### Basic Styling

Instead of ANSI escape codes (`\033[92m`), you use tags:

```python
from rich.console import Console
console = Console()

console.print("[bold bright_red]Error![/bold bright_red]")
console.print("[italic cyan]Type 'git init' to start...[/italic cyan]")
```

### Panels

A `Panel` wraps content in a box. The game uses this for headers and exercises.

```python
from rich.panel import Panel

console.print(Panel(
    "Your repository is empty.",
    title="[bold yellow]Git Status[/bold yellow]",
    border_style="bright_white"
))
```

---

## Step 2 — Safe Input Handling (`get_input`)

Find the `get_input()` function. This is a wrapper around the standard `input()`.

```python
def get_input(prompt_text="  ▸ ", save_fn=None):
    try:
        return console.input(f"[bold bright_yellow]{prompt_text}[/bold bright_yellow]").strip()
    except (EOFError, KeyboardInterrupt):
        console.print("\n[italic bright_cyan]💾 Saving and exiting...[/italic bright_cyan]")
        if save_fn:
            save_fn()
        sys.exit(0)
```

**Why wrap input?**
1.  **Styling**: `console.input()` allows Rich markup in the prompt.
2.  **Crash Safety**: If the user presses `Ctrl+C` (KeyboardInterrupt), standard Python crashes with a traceback. This wrapper catches it, saves the game state, and exits gracefully.

---

## Step 3 — Visualizing Progress (`show_main_menu`)

The main menu shows a visual progress bar. Here's the logic behind the "drawing":

```python
    prog = len(state.cleared_stages)
    pct = int(prog / total_stages * 100) if total_stages else 0
    
    # 1. Calculate how many blocks to fill
    bar_len = 25
    filled = int(bar_len * pct / 100)

    # 2. Build the string
    bar_filled = "█" * filled           # "█████"
    bar_empty = "░" * (bar_len - filled) # "░░░░░"
```

### Adaptive Coloring

The bar changes color based on how close you are to completion. This is a simple visually rewarding feedback loop.

| Percentage | Color |
| :--- | :--- |
| 90%+ | `bold bright_green` |
| 70-89% | `bold green` |
| 50-69% | `bold yellow` |
| 25-49% | `bold orange1` |
| < 25% | `bold red` |

This logic is used in `show_main_menu` to make the progress bar feel "hotter" as you progress.

---

## Step 4 — Mastery Badges

The game calculates a "Mastery" score based on accuracy and first-try success rate.

```python
mastery = int(round(state.accuracy * 0.7 + state.first_try_accuracy * 0.3))
```

It then assigns a badge:

-   **90+**: 🏆 **Pro** (Green)
-   **75+**: ⭐ **Strong** (Yellow)
-   **60+**: 📈 **Developing** (Orange)
-   **<60**: 🌱 **Beginner** (Cyan)

This gamification element (in `show_main_menu`) gives players a reason to care about accuracy, not just completion.

---

## Step 5 — The Teaching Slide Layout

Find `show_teaching()`. This illustrates how to display complex structured data. It creates a layout with:

1.  **Header**: The command (`git commit`)
2.  **Syntax**: The usage pattern (`git commit -m "message"`)
3.  **Explanation**: Putting it in `[dim]` makes the important parts pop.
4.  **Example**: A code block.
5.  **Pro Tip**: A distinctive yellow/orange panel for extra value.

```python
    # Example logic for the "Pro Tip" panel
    if teaching.pro_tip:
        console.print(Panel(
            f"[italic]{teaching.pro_tip}[/italic]",
            title="[bold bright_yellow]💡 Pro Tip[/bold bright_yellow]",
            border_style="yellow"
        ))
```

Using conditional rendering (`if teaching.pro_tip`) keeps the UI clean — if there's no tip, no empty box appears.

---

## Step 6 — Feedback Panels (`show_correct` / `show_wrong`)

### Success
`show_correct()` uses `show_success_animation()` which simply breaks the static flow:

```python
def show_success_animation(message="Success!"):
    console.print(f"\n  [bold bright_green]✨ {message} ✨[/bold bright_green]")
    time.sleep(0.3)  # Tiny pause to let the user register the success
```

The `time.sleep(0.3)` is crucial "game feel." It adds weight to the success event.

### Failure (Wrong Answer)
`show_wrong_retry()` is careful **not** to show the answer immediately.

```python
    console.print(Panel(
        f"[red]You typed:[/red] [bold white]{user_answer}[/bold white]\n\n"
        f"[dim]That's not quite right. Try again![/dim]",
        title="[bold red]❌ Incorrect[/bold red]",
        border_style="red"
    ))
```

It repeats the user's input back to them. This helps them catch typos ("Oh, I typed `gti` instead of `git`").

---

## Step 7 — The "Ghost" Skip Hint

In `show_skip_hint()`, we use visual hierarchy to make the "skip" option available but discouraged.

```python
def show_skip_hint():
    console.print("\n  [dim]Stuck? Type 'skip' to see the answer and move on.[/dim]")
```

By using `[dim]`, the text recedes into the background. It's there if you look for it, but it doesn't scream "CLICK ME" like a bright button would. This guides the player to keep trying.

---

## Step 8 — Notebook & Glossary

### The Notebook (`show_notebook`)
This uses a loop to generate a dictionary-like view. Note the handling of empty states:

```python
    if not state.notebook_entries:
        console.print(Panel("Your notebook is empty.", style="dim red"))
        return
```

### The Glossary (`show_glossary`)
This function uses **pagination** (waiting for Enter between sections) to avoid wall-of-text syndrome.

```python
    pause()  # Wait for user input
    clear()  # Clear screen for next page
```

---

## Step 9 — Animations

### `show_loading()`
This uses Rich's `Progress` context manager to show a spinner.

```python
    with Progress(
        SpinnerColumn(style="bright_cyan"),
        TextColumn("{task.description}"),
        transient=True  # Disappears when done!
    ) as progress:
        task = progress.add_task("Loading...", total=None)
        time.sleep(0.8)
```

`transient=True` is the key teaching point here. It means the loading bar removes itself from the terminal after it finishes, keeping the history clean.

### `show_streak()`
Displays a fire emoji 🔥 relative to the streak count.

```python
    count = min(streak_count, 5)  # Max 5 flames
    flames = "🔥" * count
```

Simple math, big visual impact.

---

## ✅ Quality Gate

- [ ] `get_input` prevents crashes on Ctrl+C.
- [ ] Progress bars use `█` and `░` characters correctly.
- [ ] Color logic adapts (Red -> Green) based on percentage.
- [ ] Panels are used to group related content.
- [ ] `transient=True` is used for temporary animations.
- [ ] Empty states (empty notebook) are handled gracefully.

---

**Phase 7 complete? Now let's fill the game with Content → [phase8.md](phase8.md)**
