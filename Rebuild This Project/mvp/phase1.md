# 🚀 PHASE 1 — Project Setup + First Runnable App

---

## 🎯 Goal

By the end of this phase, you'll have a Python app that runs in your terminal, shows a styled menu, reads your input, and responds. No game logic yet — just the skeleton.

---

## 🔹 Step 1 — Create Your Project Folder

Open your terminal (PowerShell on Windows, Terminal on Mac/Linux) and run these commands one at a time:

```
mkdir GitGrind-MVP
cd GitGrind-MVP
```

This creates a folder called `GitGrind-MVP` and moves inside it.

---

## 🔹 Step 2 — Create a Virtual Environment

A virtual environment is a private space for your project's packages. Without it, every Python project shares the same installed libraries — and they can conflict with each other.

Run this:

```
python -m venv venv
```

This creates a folder called `venv/` inside your project. It contains a private copy of Python and pip.

Now activate it:

```
# Windows (PowerShell):
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

**How to know it worked:** Your terminal prompt will now show `(venv)` at the beginning, like this:

```
(venv) PS C:\Users\You\GitGrind-MVP>
```

If you don't see `(venv)`, the activation didn't work. Try running the activate command again.

---

## 🔹 Step 3 — Install Rich

Rich is a library that makes terminal output beautiful — colors, boxes, styled text. We'll use it for the entire UI.

```
pip install rich
```

You should see output ending with something like:

```
Successfully installed rich-13.x.x markdown-it-py-x.x.x ...
```

Now create a file called `requirements.txt` in your project folder with this content:

```
rich
```

**Why?** When someone else downloads your project, they can run `pip install -r requirements.txt` to install everything they need.

---

## 🔹 Step 4 — Create the Folder Structure

Create these folders and files. Every file starts empty for now.

```
GitGrind-MVP/
├── main.py
├── ui.py
├── requirements.txt
├── engine/
│   └── __init__.py
├── content/
│   └── __init__.py
└── tests/
```

**What is `__init__.py`?**

It's an empty file that tells Python "this folder is a package — you can import code from it." Without it, `from engine.validator import ...` would fail.

You can create the folders and files from terminal:

```
mkdir engine
mkdir content
mkdir tests
New-Item engine/__init__.py    # Windows PowerShell
New-Item content/__init__.py   # Windows PowerShell
```

Or on Mac/Linux:

```
mkdir engine content tests
touch engine/__init__.py content/__init__.py
```

---

## 🔹 Step 5 — Build `ui.py` (The Display Layer)

This file handles everything the user SEES. It prints menus, shows feedback, reads input. It never does any game logic.

Open `ui.py` and write this code. I'll explain every line below.

```python
"""
GitGrind — Terminal UI.
All display and input functions live here.
"""
import os
from rich.console import Console
from rich.panel import Panel

# This is the Rich console object. We use it instead of print().
# It can show colors, bold text, panels, and more.
console = Console()


def clear():
    """Clear the terminal screen."""
    # os.system runs a terminal command.
    # "cls" clears the screen on Windows. "clear" does it on Mac/Linux.
    # os.name == "nt" means "we're on Windows"
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    """Wait for the user to press Enter before continuing."""
    console.print()
    console.input("  [dim]Press Enter to continue...[/dim]")


def get_input(prompt_text="  ▸ "):
    """
    Read input from the user. Returns the text they typed,
    with extra spaces removed and converted to lowercase.

    If the user presses Ctrl+C, we catch it and return "quit"
    so the app doesn't crash with an ugly error.
    """
    try:
        user_text = input(prompt_text)
        # .strip() removes spaces from both ends: "  git init  " → "git init"
        # .lower() makes it lowercase: "GIT INIT" → "git init"
        return user_text.strip().lower()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C or Ctrl+D pressed — treat it as "quit"
        print()  # Move to next line so output looks clean
        return "quit"


def show_main_menu():
    """
    Display the main menu. This is the first thing the player sees.
    """
    clear()

    # Panel() draws a box around text. border_style sets the color.
    console.print(Panel(
        "[bold bright_cyan]⚡ GitGrind[/bold bright_cyan]",
        border_style="bright_cyan",
    ))

    console.print()
    console.print("  [bold][C][/bold]  Continue")
    console.print("  [bold][Q][/bold]  Quit")
    console.print()
```

### What each part does:

| Code | What It Does |
|------|-------------|
| `from rich.console import Console` | Imports Rich's Console class for styled printing |
| `console = Console()` | Creates one console object we reuse everywhere |
| `os.system("cls" if os.name == "nt" else "clear")` | Clears the terminal (cross-platform) |
| `user_text.strip().lower()` | Cleans user input: removes spaces, makes lowercase |
| `except (KeyboardInterrupt, EOFError)` | Catches Ctrl+C so the app exits cleanly |
| `Panel("text", border_style="cyan")` | Draws a colored box around text |
| `[bold bright_cyan]...[/bold bright_cyan]` | Rich markup — like HTML but for terminals |

### Test it now

Add this at the very bottom of `ui.py`:

```python
# Temporary test — delete this later
if __name__ == "__main__":
    show_main_menu()
```

Run it:

```
python ui.py
```

**You should see:**

```
╭──────────────────────────────────────╮
│ ⚡ GitGrind                          │
╰──────────────────────────────────────╯

  [C]  Continue
  [Q]  Quit

```

If you see this menu with a cyan border, it works. If you get an error, check:
- Is your venv active? (look for `(venv)` in your prompt)
- Did `pip install rich` succeed?
- Are you running from inside the `GitGrind-MVP/` folder?

**Now delete the test code** (the `if __name__` block) from the bottom of `ui.py`.

---

## 🔹 Step 6 — Build `main.py` (The Brain)

This file is the entry point — the thing you run. It shows the menu, reads what the user picks, and responds.

Open `main.py` and write this:

```python
"""
GitGrind — Main entry point.
Runs the menu loop.
"""
import ui


def main():
    """
    The main game loop.
    Shows the menu, reads the user's choice, and acts on it.
    This loop runs forever until the user quits.
    """
    try:
        while True:
            # Step 1: Show the menu
            ui.show_main_menu()

            # Step 2: Read what the user types
            choice = ui.get_input("  Choose: ")

            # Step 3: Act on their choice
            if choice in ("c", "continue"):
                ui.console.print("\n  [yellow]Game starting soon...[/yellow]")
                ui.pause()

            elif choice in ("q", "quit"):
                ui.console.print("\n  [dim]Goodbye![/dim]\n")
                break  # Exit the while loop → program ends

            else:
                # They typed something invalid
                ui.console.print("\n  [red]Invalid option. Try C or Q.[/red]")
                ui.pause()

    except KeyboardInterrupt:
        # If Ctrl+C is pressed while the menu is showing
        ui.console.print("\n\n  [dim]Goodbye![/dim]\n")


# This is the standard Python entry point.
# It means: "only run main() if this file is executed directly"
# (not when imported by another file)
if __name__ == "__main__":
    main()
```

### What each part does:

| Code | What It Does |
|------|-------------|
| `import ui` | Imports your ui.py file so you can call its functions |
| `while True:` | Loop forever (until `break` is called) |
| `choice = ui.get_input(...)` | Reads and cleans user input |
| `choice in ("c", "continue")` | Checks if they typed either `c` OR `continue` |
| `break` | Exits the `while True` loop |
| `try/except KeyboardInterrupt` | Catches Ctrl+C at the menu level |
| `if __name__ == "__main__":` | Standard Python pattern — only runs when you execute this file directly |

### Test it now

```
python main.py
```

**Test these inputs:**

| You Type | What Should Happen |
|----------|-------------------|
| `c` | Shows "Game starting soon..." then returns to menu |
| `C` | Same thing (because we lowercased the input) |
| `q` | Prints "Goodbye!" and exits |
| `Q` | Same thing |
| ` c ` (with spaces) | Works (because we stripped spaces) |
| `xyz` | Shows "Invalid option" then returns to menu |
| Just press Enter | Shows "Invalid option" |
| Ctrl+C | Exits cleanly with "Goodbye!" — no ugly error |

**If any of these don't work, fix them now.** This menu loop is the foundation everything else builds on.

---

## 🔹 Step 7 — Understand What You Built

You now have two files working together:

```
main.py  →  The BRAIN (decides what happens)
ui.py    →  The FACE (decides how things look)
```

This separation is important. Here's why:

- Want to change the menu color from cyan to green? → Edit `ui.py`. Don't touch `main.py`.
- Want to add a new menu option (like "Reset Progress")? → Edit `main.py`. Don't touch the colors in `ui.py`.

When everything is in one giant file, a small change can break everything. With separation, each file has ONE job.

---

## ✅ Checklist (Don't Move On Until)

- [ ] `python ui.py` shows the styled menu (if __name__ test)
- [ ] `python main.py` shows menu and responds to input
- [ ] `c`, `C`, and ` c ` all work as "continue"
- [ ] `q` and `Q` both quit cleanly
- [ ] Invalid input shows error message, returns to menu
- [ ] Ctrl+C exits cleanly (no traceback)
- [ ] `engine/` and `content/` folders exist with `__init__.py`

---

## 🛟 If Something Goes Wrong

**"ModuleNotFoundError: No module named 'rich'"**
→ Your venv isn't active. Run `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux), then `pip install rich`.

**"ModuleNotFoundError: No module named 'ui'"**
→ You're running from the wrong folder. `cd` into `GitGrind-MVP/` first, then run `python main.py`.

**Menu shows but colors don't work**
→ Some terminals don't support colors. Try VS Code's built-in terminal, or Windows Terminal.

**"SyntaxError" on a specific line**
→ Check for missing colons `:` at the end of `def`, `if`, `while` lines. Check for unclosed quotes or parentheses.

---

**Phase 1 done? You have a running app! Now let's define the data structures → [phase2.md](phase2.md)**
