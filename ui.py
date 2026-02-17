"""
GitGrind — Terminal UI powered by Rich.
Handles all display, prompts, and visual feedback.
"""
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.style import Style
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.live import Live
from content.models import STAGE_BOSS, STAGE_EXERCISE, STAGE_SETUP
import sounds

console = Console()

# ── Brand color used for the logo everywhere ──
LOGO_COLOR = "bold orange1"


# ═══════════════════════════════════════════════════════════
#  UTILITIES
# ═══════════════════════════════════════════════════════════

def clear():
    console.clear()


def separator():
    """Print a dim separator line for visual breathing room between sections."""
    console.print(f"\n  [dim]{'─' * 60}[/dim]\n")


def pause():
    console.print("\n  [italic bright_cyan]Press Enter to continue...[/italic bright_cyan]")
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass


def get_input(prompt_text="  ▸ ", save_fn=None):
    """
    Get user input. Returns the trimmed string.
    On Ctrl+C / EOF, saves state via save_fn (if provided) and exits.
    Type 'quit' during exercises to return to menu.
    """
    try:
        return console.input(f"[bold bright_yellow]{prompt_text}[/bold bright_yellow]").strip()
    except (EOFError, KeyboardInterrupt):
        console.print("\n[italic bright_cyan]💾 Saving and exiting...[/italic bright_cyan]")
        if save_fn:
            save_fn()
        sys.exit(0)


def show_loading(message="Loading", duration=0.8):
    """Show an animated loading spinner."""
    with Progress(
        SpinnerColumn(style="bright_cyan"),
        TextColumn("[bright_white]{task.description}[/bright_white]"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task(f"[bright_cyan]{message}...[/bright_cyan]", total=None)
        time.sleep(duration)


def show_success_animation(message="Success!"):
    """Show a success message with brief animation."""
    console.print(f"\n  [bold bright_green]✨ {message} ✨[/bold bright_green]")
    time.sleep(0.3)


# ═══════════════════════════════════════════════════════════
#  LOGO & MENU
# ═══════════════════════════════════════════════════════════

LOGO = r"""
   ██████╗ ██╗████████╗ ██████╗ ██████╗ ██╗███╗   ██╗██████╗
  ██╔════╝ ██║╚══██╔══╝██╔════╝ ██╔══██╗██║████╗  ██║██╔══██╗
  ██║  ███╗██║   ██║   ██║  ███╗██████╔╝██║██╔██╗ ██║██║  ██║
  ██║   ██║██║   ██║   ██║   ██║██╔══██╗██║██║╚██╗██║██║  ██║
  ╚██████╔╝██║   ██║   ╚██████╔╝██║  ██║██║██║ ╚████║██████╔╝
   ╚═════╝ ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝
"""


def show_logo():
    clear()
    console.print(f"[{LOGO_COLOR}]{LOGO}[/{LOGO_COLOR}]")
    tagline = Text("Learn Git by Grinding.", style="italic bright_cyan")
    console.print("  ", tagline)
    console.print()


def show_main_menu(state, total_stages, next_stage_label=None):
    show_logo()
    prog = len(state.cleared_stages)
    pct = int(prog / total_stages * 100) if total_stages else 0
    bar_len = 25
    filled = int(bar_len * pct / 100)

    # Create colorful progress bar with gradient effect
    bar_filled = "█" * filled
    bar_empty = "░" * (bar_len - filled)

    # Color the filled portion based on progress
    if pct >= 90:
        bar_color = "bold bright_green"
    elif pct >= 70:
        bar_color = "bold green"
    elif pct >= 50:
        bar_color = "bold yellow"
    elif pct >= 25:
        bar_color = "bold orange1"
    else:
        bar_color = "bold red"

    colored_bar = f"[{bar_color}]{bar_filled}[/{bar_color}][dim]{bar_empty}[/dim]"

    mastery = int(round(state.accuracy * 0.7 + state.first_try_accuracy * 0.3))
    if mastery >= 90:
        mastery_label = "🏆 Pro"
        mastery_color = "bold bright_green"
    elif mastery >= 75:
        mastery_label = "⭐ Strong"
        mastery_color = "bold yellow"
    elif mastery >= 60:
        mastery_label = "📈 Developing"
        mastery_color = "bold orange1"
    else:
        mastery_label = "🌱 Beginner"
        mastery_color = "cyan"

    stats_table = Table(show_header=False, box=None, padding=(0, 2))
    stats_table.add_column(style="bold cyan")
    stats_table.add_column(style="bold white")

    stats_table.add_row("🎯 Journey", f"{colored_bar} [{bar_color}]{pct}%[/{bar_color}] [dim]({prog}/{total_stages})[/dim]")

    if next_stage_label and not state.game_complete:
        stats_table.add_row("⏭️  Next Stage", f"[bold bright_yellow]{next_stage_label}[/bold bright_yellow]")

    stats_table.add_row("💪 Mastery", f"[{mastery_color}]{mastery}% {mastery_label}[/{mastery_color}]")

    # Colorful accuracy display
    acc_color = "bright_green" if state.accuracy >= 80 else "yellow" if state.accuracy >= 60 else "red"
    first_try_color = "bright_green" if state.first_try_accuracy >= 70 else "yellow" if state.first_try_accuracy >= 50 else "red"
    stats_table.add_row(
        "📊 Accuracy",
        f"[{acc_color}]{state.accuracy}%[/{acc_color}]  [dim]|[/dim]  First-try [{first_try_color}]{state.first_try_accuracy}%[/{first_try_color}]"
    )

    # Streak with fire emoji and colors
    streak_color = "bright_red" if state.current_streak >= 10 else "orange1" if state.current_streak >= 5 else "yellow"
    stats_table.add_row(
        "🔥 Streak",
        f"[{streak_color}]{state.current_streak}[/{streak_color}]  [dim]|[/dim]  Best [bold bright_red]🔥 {state.best_streak}[/bold bright_red]"
    )

    stats_table.add_row("📚 Commands Learned", f"[bold magenta]{len(state.data['commands_learned'])}[/bold magenta]")
    stats_table.add_row(
        "⚡ Practice Volume",
        f"[bold cyan]{state.total_commands_typed}[/bold cyan] commands  [dim]|[/dim]  hints [yellow]{state.hints_used}[/yellow]"
    )
    stats_table.add_row("⏱️  Time Invested", f"[bold green]{state.time_played_display}[/bold green]")

    console.print(Panel(
        stats_table,
        title="[bold bright_white]📈 Progress Report[/bold bright_white]",
        border_style="bright_blue",
        width=80
    ))

    # Show recently learned commands with colorful styling
    recent = state.data["commands_learned"][-3:] if state.data["commands_learned"] else []
    if recent:
        console.print("\n  [bold bright_cyan]✨ Recently Mastered:[/bold bright_cyan]")
        for i, cmd in enumerate(reversed(recent), 1):
            cmd_color = "bright_yellow" if i % 2 == 1 else "bright_magenta"
            console.print(f"    [bright_green]✓[/bright_green] [bold {cmd_color}]{cmd}[/bold {cmd_color}]")

    separator()

    console.print("  [bold bright_white]🎮 Actions:[/bold bright_white]\n")

    if state.game_complete:
        console.print("  [bold bright_green]  🔄 [C][/bold bright_green] [bright_white]Replay any stage[/bright_white]")
    elif prog > 0:
        console.print("  [bold bright_green]  ▶️  [C][/bold bright_green] [bright_white]Continue your journey[/bright_white]")
    else:
        console.print("  [bold bright_green]  🚀 [C][/bold bright_green] [bright_white]Start your adventure[/bright_white]")
    console.print("  [bold bright_yellow]  🔁 [R][/bold bright_yellow] [bright_cyan]Replay a cleared stage[/bright_cyan]")

    # Notebook option — show learned command count
    notebook_count = len(state.notebook_entries)
    if notebook_count > 0:
        console.print(f"  [bold bright_magenta]  📓 [N][/bold bright_magenta] [bright_white]Notebook[/bright_white] [dim]({notebook_count} commands)[/dim]")
    else:
        console.print(f"  [dim]  📓 [N][/dim] [dim]Notebook (empty — start playing!)[/dim]")

    # Glossary option
    console.print("  [bold bright_cyan]  📖 [G][/bold bright_cyan] [bright_white]Git Glossary[/bright_white]")

    console.print("  [bold bright_red]  🗑️  [X][/bold bright_red] [bright_magenta]Reset all progress[/bright_magenta]")
    console.print("  [dim]  👋 [Q][/dim] [dim]Quit[/dim]")
    console.print()


# ═══════════════════════════════════════════════════════════
#  GIT GLOSSARY
# ═══════════════════════════════════════════════════════════

def show_glossary():
    """
    Display the Git terminology glossary in paginated category panels.
    Each category is shown as its own panel; user presses Enter to advance.
    """
    from content.glossary import GIT_GLOSSARY

    clear()
    console.print(f"\n  [{LOGO_COLOR}]📖 GIT GLOSSARY[/{LOGO_COLOR}]")
    console.print("  [italic bright_cyan]Git jargon explained in plain English.[/italic bright_cyan]")
    console.print(f"  [dim]{len(GIT_GLOSSARY)} categories • Press Enter to advance[/dim]\n")

    for cat_idx, (category_name, terms) in enumerate(GIT_GLOSSARY, 1):
        content_lines = []
        for term, explanation in terms:
            content_lines.append(f"  [bold bright_yellow]{term}[/bold bright_yellow]")
            content_lines.append(f"    [bright_white]{explanation}[/bright_white]")
            content_lines.append("")

        body = "\n".join(content_lines).rstrip()

        console.print(Panel(
            body,
            title=f"[bold bright_cyan]{category_name}  [dim]({cat_idx}/{len(GIT_GLOSSARY)})[/dim][/bold bright_cyan]",
            border_style="bright_cyan",
            width=75,
            padding=(1, 2),
        ))

        if cat_idx < len(GIT_GLOSSARY):
            console.print("  [italic bright_cyan]Press Enter for next category...[/italic bright_cyan]")
            try:
                input()
            except (EOFError, KeyboardInterrupt):
                return

    separator()
    console.print("  [bold bright_green]✅ That's all the essential Git terminology![/bold bright_green]")
    console.print("  [dim]You'll learn each of these through hands-on practice in the game.[/dim]")
    console.print()
    pause()


# ═══════════════════════════════════════════════════════════
#  LEVEL MAP
# ═══════════════════════════════════════════════════════════

def show_level_map(stages, cleared):
    """Show the full stage progression map."""
    console.print("\n  [bold bright_white underline]🗺️  Stage Map[/bold bright_white underline]")
    console.print("  [dim]Your journey through Git mastery[/dim]\n")

    for i, stage in enumerate(stages):
        label = stage.label

        if i in cleared:
            marker = "[bright_green]✅[/bright_green]"
            status = "[dim bright_green](Cleared)[/dim bright_green]"
        else:
            marker = "[yellow]🔒[/yellow]" if i == len(cleared) else "[dim]🔒[/dim]"
            status = "[bright_yellow](Next)[/bright_yellow]" if i == len(cleared) else ""

        # Color by type with enhanced colors
        if stage.stage_type == STAGE_BOSS:
            label = f"[bold bright_red]{label}[/bold bright_red]"
        elif stage.stage_type == STAGE_EXERCISE:
            label = f"[bold bright_blue]{label}[/bold bright_blue]"
        elif stage.stage_type == STAGE_SETUP:
            label = f"[bold bright_yellow]{label}[/bold bright_yellow]"
        else:
            label = f"[bold bright_cyan]{label}[/bold bright_cyan]"

        console.print(f"    {marker} {label} {status}")

    separator()


# ═══════════════════════════════════════════════════════════
#  LESSON / TEACHING DISPLAY
# ═══════════════════════════════════════════════════════════

def show_lesson_intro(level):
    """Show a banner indicating the lesson phase is starting."""
    console.print(f"\n  [bold bright_white on bright_blue] 📖 LESSON — {level.name} [/bold bright_white on bright_blue]")
    console.print(f"  [italic cyan]Let's learn {len(level.teachings)} command{'s' if len(level.teachings) != 1 else ''} before practicing.[/italic cyan]\n")


def show_teaching(teaching, index, total):
    """
    Display one teaching slide: command, syntax, explanation, example, and tip.
    """
    # Build the content
    content_parts = []

    # Syntax line with enhanced colors
    content_parts.append(f"  [bold bright_yellow]📌 Syntax:[/bold bright_yellow]  [bold bright_white on grey15]{teaching.syntax}[/bold bright_white on grey15]")
    content_parts.append("")

    # Explanation
    for line in teaching.explanation.strip().split("\n"):
        content_parts.append(f"  [bright_white]{line}[/bright_white]")
    content_parts.append("")

    # Example output in a nested panel with colorful display
    if teaching.example_output:
        example_lines = teaching.example_output.strip()
        content_parts.append(f"  [bold bright_cyan]💻 Example:[/bold bright_cyan]")
        content_parts.append("")
        for line in example_lines.split("\n"):
            content_parts.append(f"    [bright_green]{line}[/bright_green]")
        content_parts.append("")

    # Pro tip with enhanced styling
    if teaching.pro_tip:
        content_parts.append(f"  [bold bright_yellow]💡 Pro Tip:[/bold bright_yellow] [italic yellow]{teaching.pro_tip}[/italic yellow]")
        content_parts.append("")

    body = "\n".join(content_parts)

    console.print(Panel(
        body,
        title=f"[bold bright_cyan]📖 {teaching.command}  [dim]({index}/{total})[/dim][/bold bright_cyan]",
        border_style="bright_cyan",
        width=70,
        padding=(1, 2),
    ))
    pause()
    separator()


# ═══════════════════════════════════════════════════════════
#  EXERCISE PROMPTS
# ═══════════════════════════════════════════════════════════

def show_exercise_prompt(exercise, index=None, total=None):
    """Display an exercise prompt based on its type."""
    progress = f"[bold bright_magenta][{index}/{total}][/bold bright_magenta] " if index and total else ""
    type_badges = {
        "recall": "[bold bright_blue]📝 RECALL[/bold bright_blue]",
        "rapid_fire": "[bold bright_magenta]⚡ RAPID FIRE[/bold bright_magenta]",
        "fill_blank": "[bold bright_yellow]✏️  FILL BLANK[/bold bright_yellow]",
        "multi_choice": "[bold bright_cyan]🎯 MULTIPLE CHOICE[/bold bright_cyan]",
        "error_fix": "[bold bright_red]🔧 ERROR FIX[/bold bright_red]",
        "scenario": "[bold bright_green]📋 SCENARIO[/bold bright_green]",
        "reverse": "[bold bright_white]🔄 REVERSE[/bold bright_white]",
        "multi_step": "[bold bright_red]🔗 MULTI-STEP[/bold bright_red]",
    }
    badge = type_badges.get(exercise.type, "[bold bright_white]📌 EXERCISE[/bold bright_white]")

    console.print(f"\n  {progress}{badge}")
    console.print(f"  [bold bright_white]{exercise.prompt}[/bold bright_white]")

    if exercise.type == "fill_blank" and exercise.blank_template:
        console.print(f"\n  [italic bright_cyan]{exercise.blank_template}[/italic bright_cyan]")

    if exercise.type == "multi_choice" and exercise.choices:
        console.print()
        for i, choice in enumerate(exercise.choices, 1):
            choice_color = "bright_yellow" if i % 2 == 1 else "bright_cyan"
            console.print(f"    [bold {choice_color}]{choice}[/bold {choice_color}]")

    if exercise.type == "error_fix" and exercise.error_output:
        console.print()
        console.print(Panel(
            f"[bright_red]{exercise.error_output}[/bright_red]",
            title="[bold bright_red]❌ Error Output[/bold bright_red]",
            border_style="bright_red",
            width=70
        ))

    if exercise.type == "reverse" and exercise.sim_output:
        console.print()
        console.print(Panel(
            f"[bright_green]{exercise.sim_output}[/bright_green]",
            title="[bold bright_white]💻 Terminal Output[/bold bright_white]",
            border_style="bright_cyan",
            width=70
        ))

    console.print("\n  [dim italic](type [bright_yellow]'quit'[/bright_yellow] to return to menu)[/dim italic]")


# ═══════════════════════════════════════════════════════════
#  FEEDBACK
# ═══════════════════════════════════════════════════════════

def show_correct(sim_output=None):
    sounds.sound_correct()
    console.print("\n  [bold bright_green]✨ ✅ Correct! Well done![/bold bright_green]")
    if sim_output:
        console.print()
        console.print(Panel(sim_output, title="[bright_green]💻 Simulated Output[/bright_green]",
                            border_style="bright_green", width=70))
    separator()


def show_wrong(correct_answer, explanation=None):
    """Legacy wrong-answer display (still used for first wrong attempt in non-retry contexts)."""
    sounds.sound_wrong()
    console.print("\n  [bold bright_red]❌ Not quite. Try again![/bold bright_red]")
    console.print(f"  [italic dim]Correct answer:[/italic dim] [bold bright_yellow]{correct_answer}[/bold bright_yellow]")
    if explanation:
        console.print(f"  [bold bright_cyan]💡 Why:[/bold bright_cyan] [italic cyan]{explanation}[/italic cyan]")
    separator()


def show_wrong_retry(user_answer, near_miss_hint=None):
    """
    Show wrong-answer feedback during retry loop.
    Does NOT reveal the correct answer — just shows what the user typed,
    an optional near-miss hint, and encourages them to try again.
    """
    sounds.sound_wrong()
    console.print("\n  [bold bright_red]❌ Not quite![/bold bright_red]")
    console.print(f"  [dim]You entered:[/dim] [bold bright_white]{user_answer}[/bold bright_white]")

    if near_miss_hint:
        console.print(f"  [bold bright_yellow]💡 {near_miss_hint}[/bold bright_yellow]")
    else:
        console.print("  [italic bright_yellow]↻ Try again![/italic bright_yellow]")
    console.print()


def show_skip_hint():
    """
    Show the ghost 'skip' hint after 2 failed retry attempts.
    Displayed as dim text so the user knows the option exists but isn't pressured.
    """
    console.print("  [dim italic](type [bright_yellow]'skip'[/bright_yellow] to see the answer and move on)[/dim italic]")


def show_skip_result(user_answer, correct_answer, explanation=None):
    """
    Show comparison panel when the user types 'skip'.
    Displays: what you typed vs the correct answer, plus the explanation.
    """
    sounds.sound_skip()
    comparison = (
        f"  [bold bright_red]Your answer:[/bold bright_red]    [bright_white]{user_answer}[/bright_white]\n"
        f"  [bold bright_green]Correct answer:[/bold bright_green] [bold bright_yellow]{correct_answer}[/bold bright_yellow]"
    )

    if explanation:
        comparison += f"\n\n  [bold bright_cyan]💡 Explanation:[/bold bright_cyan]\n  [italic cyan]{explanation}[/italic cyan]"

    console.print()
    console.print(Panel(
        comparison,
        title="[bold bright_yellow]⏭️  Skipped — Here's the answer[/bold bright_yellow]",
        border_style="bright_yellow",
        width=70,
        padding=(1, 1),
    ))
    separator()


def show_hint(hint_text):
    sounds.sound_hint()
    console.print(f"\n  [bold bright_yellow]💡 Hint:[/bold bright_yellow] [italic yellow]{hint_text}[/italic yellow]")
    console.print("  [italic dim]Try again:[/italic dim]\n")


# ═══════════════════════════════════════════════════════════
#  QUICK RECAP BEFORE DRILLS
# ═══════════════════════════════════════════════════════════

def show_drill_recap(level):
    """
    Show a quick reminder of the commands taught in this level
    right before the drill zone starts.
    """
    if not level.teachings:
        return

    content_lines = []
    for t in level.teachings:
        content_lines.append(f"  [bold bright_yellow]{t.command}[/bold bright_yellow]")
        content_lines.append(f"    [dim]{t.syntax}[/dim]")
        content_lines.append("")

    body = "\n".join(content_lines).rstrip()

    console.print()
    console.print(Panel(
        body,
        title="[bold bright_cyan]📋 Quick Recap — Commands You Just Learned[/bold bright_cyan]",
        border_style="bright_cyan",
        width=70,
        padding=(1, 1),
    ))
    separator()


# ═══════════════════════════════════════════════════════════
#  SESSION SUMMARY
# ═══════════════════════════════════════════════════════════

def show_session_summary(state):
    """
    Show a summary of this play session's performance
    when the player returns to the main menu.
    """
    total_attempted = state.session_correct + state.session_wrong
    if total_attempted == 0 and state.session_stages_cleared == 0:
        return  # Nothing to show — player didn't do anything

    content_parts = []

    # Session stats
    if total_attempted > 0:
        sess_acc = int(round(state.session_correct / total_attempted * 100))
        acc_color = "bright_green" if sess_acc >= 80 else "bright_yellow" if sess_acc >= 60 else "bright_red"
        content_parts.append(f"  [bold bright_cyan]📊 Exercises:[/bold bright_cyan]  [bright_green]✅ {state.session_correct}[/bright_green]  [bright_red]❌ {state.session_wrong}[/bright_red]  [dim]⏭️ {state.session_skipped} skipped[/dim]")
        content_parts.append(f"  [bold bright_cyan]🎯 Accuracy:[/bold bright_cyan]   [{acc_color}]{sess_acc}%[/{acc_color}]")

    if state.session_stages_cleared > 0:
        content_parts.append(f"  [bold bright_cyan]🏆 Cleared:[/bold bright_cyan]    [bold bright_green]{state.session_stages_cleared} stage{'s' if state.session_stages_cleared != 1 else ''}[/bold bright_green]")

    body = "\n".join(content_parts)

    console.print()
    console.print(Panel(
        body,
        title="[bold bright_white]📈 Session Summary[/bold bright_white]",
        border_style="bright_blue",
        width=70,
        padding=(1, 1),
    ))
    console.print()


# ═══════════════════════════════════════════════════════════
#  NOTEBOOK
# ═══════════════════════════════════════════════════════════

def show_notebook(state):
    """
    Display all learned commands from the notebook, organized by category.
    Shows command, syntax, explanation, and pro tip for each entry.
    """
    from notebook import category_map, CATEGORY_ORDER

    entries = state.notebook_entries
    if not entries:
        console.print(Panel(
            "  [dim]Your notebook is empty. Start playing to learn commands![/dim]",
            title="[bold bright_magenta]📓 Notebook[/bold bright_magenta]",
            border_style="bright_magenta",
            width=70,
        ))
        return

    # Group entries by category
    categorized = {cat: [] for cat in CATEGORY_ORDER}
    categorized["Other"] = []

    for cmd, data in entries.items():
        cat = category_map.get(cmd, "Other")
        if cat not in categorized:
            categorized[cat] = []
        categorized[cat].append((cmd, data))

    # Display header
    clear()
    console.print(f"\n  [bold bright_magenta]📓 YOUR NOTEBOOK[/bold bright_magenta]  [dim]({len(entries)} command{'s' if len(entries) != 1 else ''})[/dim]\n")

    for cat in CATEGORY_ORDER + ["Other"]:
        cmds = categorized.get(cat, [])
        if not cmds:
            continue

        console.print(f"  [bold bright_cyan]📂 {cat.upper()}[/bold bright_cyan]")
        console.print(f"  [dim]{'─' * 60}[/dim]")

        for cmd, data in cmds:
            console.print(f"\n    [bold bright_yellow]{cmd}[/bold bright_yellow]")
            if data.get("syntax"):
                console.print(f"      [dim]Syntax:[/dim] [bright_white]{data['syntax']}[/bright_white]")
            if data.get("explanation"):
                # Show first 2 lines of explanation to keep it compact
                explanation_lines = data["explanation"].strip().split("\n")
                for line in explanation_lines[:2]:
                    console.print(f"      [dim]{line}[/dim]")
                if len(explanation_lines) > 2:
                    console.print(f"      [dim italic]...({len(explanation_lines) - 2} more lines)[/dim italic]")
            if data.get("pro_tip"):
                console.print(f"      [italic yellow]💡 {data['pro_tip']}[/italic yellow]")

        console.print()

    separator()
    console.print("  [bold bright_white]Options:[/bold bright_white]")
    console.print("    [bold bright_green][S][/bold bright_green] Save notebook as text file")
    console.print("    [dim][B][/dim] Back to menu")
    console.print()


# ═══════════════════════════════════════════════════════════
#  STAGE HEADERS
# ═══════════════════════════════════════════════════════════

def show_level_header(level):
    clear()
    title = f"Level {level.number} — {level.name}"
    console.print()
    console.print(Panel(
        f"[italic bright_cyan]{level.tagline}[/italic bright_cyan]\n\n[bright_white]{level.concept}[/bright_white]",
        title=f"[bold bright_green]🎓 {title}[/bold bright_green]",
        border_style="bright_green",
        width=70,
        padding=(1, 2),
    ))
    pause()


def show_exercise_round_header(er):
    clear()
    required, total = er.pass_threshold
    console.print()
    console.print(Panel(
        f"[italic bright_blue]{er.tagline}[/italic bright_blue]\n\n"
        f"Pass: [bold bright_yellow]{required}/{total}[/bold bright_yellow] correct",
        title=f"[bold bright_blue]💪 Exercise Round {er.number} — {er.name}[/bold bright_blue]",
        border_style="bright_blue",
        width=70,
        padding=(1, 2),
    ))
    pause()


def show_boss_header(boss):
    clear()
    sounds.sound_boss_intro()
    console.print()
    console.print(Panel(
        f"[italic bright_red]{boss.tagline}[/italic bright_red]\n\n[bright_white]{boss.story}[/bright_white]",
        title=f"[bold bright_red]⚔️  BOSS FIGHT {boss.number} — {boss.name}[/bold bright_red]",
        border_style="bright_red",
        width=70,
        padding=(1, 2),
    ))
    console.print("\n  [bold bright_red]⚠️  ALL STEPS MUST BE CORRECT. ⚠️[/bold bright_red]")
    pause()


def show_setup_intro():
    clear()
    console.print()
    console.print(Panel(
        "[italic bright_yellow]Before we begin, let's make sure Git is configured.[/italic bright_yellow]",
        title="[bold bright_yellow]⚙️  Setup[/bold bright_yellow]",
        border_style="bright_yellow",
        width=70,
        padding=(1, 2),
    ))


# ═══════════════════════════════════════════════════════════
#  DRILL ZONE
# ═══════════════════════════════════════════════════════════

def show_drill_header(required, total):
    separator()
    console.print(f"  [bold bright_white on bright_red] 🎯 DRILL ZONE [/bold bright_white on bright_red]")
    console.print(f"  [italic cyan]Get [bold bright_yellow]{required}/{total}[/bold bright_yellow] correct to pass this level.[/italic cyan]\n")


def show_drill_progress(correct, wrong, required, total):
    remaining = total - correct - wrong
    console.print(f"\n  [bright_green]✅ {correct}[/bright_green]  [bright_red]❌ {wrong}[/bright_red]  "
                  f"[dim]Remaining: [bright_white]{remaining}[/bright_white]  |  Need: [bright_yellow]{required}[/bright_yellow][/dim]")


# ═══════════════════════════════════════════════════════════
#  RESULTS
# ═══════════════════════════════════════════════════════════

def show_stage_cleared(stage_label, msg=None):
    sounds.sound_stage_cleared()
    content = f"[bold bright_green]🎉 ✨ CLEARED: {stage_label} ✨ 🎉[/bold bright_green]"
    if msg:
        content += f"\n\n[bright_white]{msg}[/bright_white]"
    separator()
    console.print(Panel(content, border_style="bright_green", width=70, padding=(1, 2)))
    pause()


def show_stage_failed(stage_label, msg=None):
    sounds.sound_stage_failed()
    content = f"[bold bright_red]💀 FAILED: {stage_label}[/bold bright_red]"
    if msg:
        content += f"\n\n[bright_yellow]{msg}[/bright_yellow]"
    separator()
    console.print(Panel(content, border_style="bright_red", width=70, padding=(1, 2)))


def show_boss_failed_mercy(stage_label, attempt_count, max_attempts):
    """Show boss failure with mercy option after too many attempts."""
    sounds.sound_stage_failed()
    content = (
        f"[bold bright_red]💀 FAILED: {stage_label}[/bold bright_red]\n\n"
        f"[bright_white]Attempt [bold]{attempt_count}/{max_attempts}[/bold].[/bright_white]\n"
    )
    if attempt_count >= max_attempts:
        content += "\n[bright_yellow]💡 You can type 'skip' to move past this boss fight.[/bright_yellow]"
    separator()
    console.print(Panel(content, border_style="bright_red", width=70, padding=(1, 2)))


def show_game_complete(state):
    sounds.sound_game_complete()
    clear()
    mastery = int(round(state.accuracy * 0.7 + state.first_try_accuracy * 0.3))
    if mastery >= 90:
        rank = "🏆 GitGrind Grandmaster"
        rank_color = "bright_yellow"
    elif mastery >= 75:
        rank = "⭐ GitGrind Pro"
        rank_color = "bright_green"
    elif mastery >= 60:
        rank = "🎓 GitGrind Practitioner"
        rank_color = "bright_cyan"
    else:
        rank = "🌟 GitGrind Graduate"
        rank_color = "bright_blue"

    console.print()
    console.print(Panel(
        f"[bold bright_green]🏆 ✨ CONGRATULATIONS! ✨ 🏆[/bold bright_green]\n\n"
        f"[bright_white]You completed GitGrind![/bright_white]\n\n"
        f"[bold bright_cyan]Final Rank:[/bold bright_cyan] [{rank_color}]{rank}[/{rank_color}]\n"
        f"[bold bright_cyan]Mastery Score:[/bold bright_cyan] [bold bright_yellow]{mastery}%[/bold bright_yellow]\n\n"
        f"[bold bright_magenta]📊 Final Stats[/bold bright_magenta]\n\n"
        f"  [bright_cyan]Accuracy:[/bright_cyan]           [bright_green]{state.accuracy}%[/bright_green]\n"
        f"  [bright_cyan]First-try:[/bright_cyan]          [bright_green]{state.first_try_accuracy}%[/bright_green]\n"
        f"  [bright_cyan]Best streak:[/bright_cyan]        [bright_red]🔥 {state.best_streak}[/bright_red]\n"
        f"  [bright_cyan]Commands typed:[/bright_cyan]     [bright_yellow]{state.total_commands_typed}[/bright_yellow]\n"
        f"  [bright_cyan]Commands learned:[/bright_cyan]   [bright_magenta]{len(state.data['commands_learned'])}[/bright_magenta]\n"
        f"  [bright_cyan]Time played:[/bright_cyan]        [bright_green]{state.time_played_display}[/bright_green]\n\n"
        f"[bold bright_white]📓 Check your Notebook [N] for a full reference of everything you learned![/bold bright_white]",
        title="[bold bright_yellow]🎓 ✨ GAME COMPLETE ✨ 🎓[/bold bright_yellow]",
        border_style="bright_yellow",
        width=70,
        padding=(1, 2),
    ))
    # No pause() here — main.py handles the post-game flow


# ═══════════════════════════════════════════════════════════
#  WELCOME & ANIMATIONS
# ═══════════════════════════════════════════════════════════

def show_welcome_animation():
    """Show a colorful welcome animation for first-time players."""
    clear()

    # Red-orange branded logo
    console.print(f"[{LOGO_COLOR}]{LOGO}[/{LOGO_COLOR}]")
    console.print()

    # Animated welcome message
    messages = [
        ("[bright_cyan]", "Welcome to GitGrind!"),
        ("[bright_yellow]", "Master Git through interactive challenges."),
        ("[bright_green]", "Learn by doing. No repositories needed."),
        ("[bright_magenta]", "Your progress is automatically saved."),
    ]

    for color, msg in messages:
        console.print(f"  {color}{msg}[/{color[1:-1]}]")
        time.sleep(0.3)

    separator()
    console.print(f"  [bold bright_white]✨ Let's begin your Git journey! ✨[/bold bright_white]\n")
    pause()


def show_stage_transition(from_stage=None, to_stage=None):
    """Show a colorful transition between stages."""
    if to_stage:
        separator()
        console.print(f"  [bold bright_yellow]⏭️  Loading:[/bold bright_yellow] [bright_cyan]{to_stage}[/bright_cyan]")
        separator()
        time.sleep(0.3)


def show_streak(streak_count):
    """Show streak notification."""
    if streak_count >= 10:
        sounds.sound_streak()
        console.print(f"\n  [bold bright_red]🔥🔥🔥 {streak_count} STREAK! UNSTOPPABLE! 🔥🔥🔥[/bold bright_red]\n")
    elif streak_count >= 5:
        sounds.sound_streak()
        console.print(f"\n  [bold orange1]🔥🔥 {streak_count} streak! Keep it up! 🔥🔥[/bold orange1]\n")
    elif streak_count >= 3:
        console.print(f"\n  [bold yellow]🔥 {streak_count} streak! Nice![/bold yellow]\n")
