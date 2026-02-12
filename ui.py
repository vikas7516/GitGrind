"""
GitGrind — Terminal UI powered by Rich.
Handles all display, prompts, and visual feedback.
"""
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from content.models import STAGE_BOSS, STAGE_EXERCISE, STAGE_SETUP

console = Console()


# ═══════════════════════════════════════════════════════════
#  UTILITIES
# ═══════════════════════════════════════════════════════════

def clear():
    console.clear()


def pause():
    console.print("\n  [dim]Press Enter to continue...[/dim]")
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
        return console.input(f"[bold cyan]{prompt_text}[/bold cyan]").strip()
    except (EOFError, KeyboardInterrupt):
        console.print("\n[dim]Saving and exiting...[/dim]")
        if save_fn:
            save_fn()
        sys.exit(0)


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
    console.print(f"[bold green]{LOGO}[/bold green]")
    console.print("  [dim]Learn Git by doing. No repos needed.[/dim]\n")


def show_main_menu(state, total_stages):
    show_logo()
    prog = len(state.cleared_stages)
    pct = int(prog / total_stages * 100) if total_stages else 0
    bar_len = 25
    filled = int(bar_len * pct / 100)
    bar = "█" * filled + "░" * (bar_len - filled)

    # Determine accuracy color
    acc = state.accuracy
    if acc >= 90:
        acc_color = "green"
    elif acc >= 75:
        acc_color = "yellow"
    elif acc >= 60:
        acc_color = "orange1"
    else:
        acc_color = "red"

    stats_table = Table(show_header=False, box=None, padding=(0, 2))
    stats_table.add_column(style="dim")
    stats_table.add_column(style="bold")
    stats_table.add_row("Progress", f"{bar} {pct}% ({prog}/{total_stages})")
    stats_table.add_row("Accuracy", f"[{acc_color}]{state.accuracy}%[/{acc_color}]")
    stats_table.add_row("First-Try", f"{state.first_try_accuracy}%")
    stats_table.add_row("Commands", f"{state.total_commands_typed}")
    stats_table.add_row("Hints Used", f"{state.hints_used}")
    if state.best_streak > 0:
        stats_table.add_row("Best Streak", f"🔥 {state.best_streak}")
    stats_table.add_row("Time", f"{state.time_played_display}")
    console.print(Panel(stats_table, title="[bold]Stats[/bold]", border_style="blue", width=50))

    # Show recently learned commands
    recent = state.data["commands_learned"][-3:] if state.data["commands_learned"] else []
    if recent:
        console.print("\n  [dim]Recently learned:[/dim]")
        for cmd in reversed(recent):
            console.print(f"    [green]✓[/green] [dim]{cmd}[/dim]")

    console.print()
    if state.game_complete:
        console.print("  [bold green][C][/bold green] Replay any stage")
    elif prog > 0:
        console.print("  [bold green][C][/bold green] Continue")
    else:
        console.print("  [bold green][C][/bold green] Start")
    console.print("  [bold yellow][R][/bold yellow] Replay a cleared stage")
    console.print("  [bold red][X][/bold red] Reset all progress")
    console.print("  [bold dim][Q][/bold dim] Quit")
    console.print()


# ═══════════════════════════════════════════════════════════
#  LEVEL MAP
# ═══════════════════════════════════════════════════════════

def show_level_map(stages, cleared):
    """Show the full stage progression map."""
    console.print("\n  [bold underline]📍 Stage Map[/bold underline]\n")
    for i, stage in enumerate(stages):
        label = stage.label

        if i in cleared:
            marker = "[green]✅[/green]"
        else:
            marker = "[dim]🔒[/dim]"

        # Color by type (no extra emoji — labels already have them)
        if stage.stage_type == STAGE_BOSS:
            label = f"[red]{label}[/red]"
        elif stage.stage_type == STAGE_EXERCISE:
            label = f"[blue]{label}[/blue]"
        elif stage.stage_type == STAGE_SETUP:
            label = f"[yellow]{label}[/yellow]"

        console.print(f"    {marker} {label}")
    console.print()


# ═══════════════════════════════════════════════════════════
#  LESSON / TEACHING DISPLAY
# ═══════════════════════════════════════════════════════════

def show_lesson_intro(level):
    """Show a banner indicating the lesson phase is starting."""
    console.print(f"\n  [bold white on blue] 📖 LESSON — {level.name} [/bold white on blue]")
    console.print(f"  [dim]Let's learn {len(level.teachings)} command{'s' if len(level.teachings) != 1 else ''} before practicing.[/dim]\n")


def show_teaching(teaching, index, total):
    """
    Display one teaching slide: command, syntax, explanation, example, and tip.
    """
    # Build the content
    content_parts = []

    # Syntax line
    content_parts.append(f"  [bold yellow]Syntax:[/bold yellow]  [bold white]{teaching.syntax}[/bold white]")
    content_parts.append("")

    # Explanation
    for line in teaching.explanation.strip().split("\n"):
        content_parts.append(f"  {line}")
    content_parts.append("")

    # Example output in a nested panel
    if teaching.example_output:
        example_lines = teaching.example_output.strip()
        content_parts.append(f"  [dim]Example:[/dim]")
        content_parts.append("")
        for line in example_lines.split("\n"):
            content_parts.append(f"    [green]{line}[/green]")
        content_parts.append("")

    # Pro tip
    if teaching.pro_tip:
        content_parts.append(f"  [bold yellow]💡 Tip:[/bold yellow] {teaching.pro_tip}")
        content_parts.append("")

    body = "\n".join(content_parts)

    console.print(Panel(
        body,
        title=f"[bold cyan]📖 {teaching.command}  ({index}/{total})[/bold cyan]",
        border_style="cyan",
        width=70,
        padding=(1, 1),
    ))
    pause()


# ═══════════════════════════════════════════════════════════
#  EXERCISE PROMPTS
# ═══════════════════════════════════════════════════════════

def show_exercise_prompt(exercise, index=None, total=None):
    """Display an exercise prompt based on its type."""
    progress = f"[dim][{index}/{total}][/dim] " if index and total else ""
    type_badges = {
        "recall": "[bold blue]RECALL[/bold blue]",
        "rapid_fire": "[bold magenta]⚡ RAPID FIRE[/bold magenta]",
        "fill_blank": "[bold yellow]FILL BLANK[/bold yellow]",
        "multi_choice": "[bold cyan]MULTIPLE CHOICE[/bold cyan]",
        "error_fix": "[bold red]🔧 ERROR FIX[/bold red]",
        "scenario": "[bold green]📋 SCENARIO[/bold green]",
        "reverse": "[bold white]🔄 REVERSE[/bold white]",
        "multi_step": "[bold red]🔗 MULTI-STEP[/bold red]",
    }
    badge = type_badges.get(exercise.type, "[bold]EXERCISE[/bold]")
    console.print(f"\n  {progress}{badge}")
    console.print(f"  {exercise.prompt}")

    if exercise.type == "fill_blank" and exercise.blank_template:
        console.print(f"  [dim]{exercise.blank_template}[/dim]")

    if exercise.type == "multi_choice" and exercise.choices:
        for choice in exercise.choices:
            console.print(f"    {choice}")

    if exercise.type == "error_fix" and exercise.error_output:
        console.print(Panel(exercise.error_output, title="[red]Error Output[/red]",
                            border_style="red", width=70))

    if exercise.type == "reverse" and exercise.sim_output:
        console.print(Panel(exercise.sim_output, title="[white]Terminal Output[/white]",
                            border_style="white", width=70))

    console.print("  [dim](type 'quit' to return to menu)[/dim]")


# ═══════════════════════════════════════════════════════════
#  FEEDBACK
# ═══════════════════════════════════════════════════════════

def show_correct(sim_output=None):
    console.print("  [bold green]✅ Correct![/bold green]")
    if sim_output:
        console.print(Panel(sim_output, title="[green]Simulated Output[/green]",
                            border_style="green", width=70))


def show_wrong(correct_answer, explanation=None):
    console.print("  [bold red]❌ Not quite.[/bold red]")
    console.print(f"  [dim]Correct answer:[/dim] [bold]{correct_answer}[/bold]")
    if explanation:
        console.print(f"  [bold yellow]💡 Why:[/bold yellow] {explanation}")



def show_hint(hint_text):
    console.print(f"  [bold yellow]💡 Hint:[/bold yellow] {hint_text}")
    console.print("  [dim]Try again:[/dim]")


# ═══════════════════════════════════════════════════════════
#  STAGE HEADERS
# ═══════════════════════════════════════════════════════════

def show_level_header(level):
    clear()
    title = f"Level {level.number} — {level.name}"
    console.print(Panel(
        f"[italic]{level.tagline}[/italic]\n\n{level.concept}",
        title=f"[bold green]{title}[/bold green]",
        border_style="green",
        width=70,
    ))
    pause()


def show_exercise_round_header(er):
    clear()
    required, total = er.pass_threshold
    console.print(Panel(
        f"[italic]{er.tagline}[/italic]\n\nPass: [bold]{required}/{total}[/bold] correct",
        title=f"[bold blue]💪 Exercise Round {er.number} — {er.name}[/bold blue]",
        border_style="blue",
        width=70,
    ))
    pause()


def show_boss_header(boss):
    clear()
    console.print(Panel(
        f"[italic]{boss.tagline}[/italic]\n\n{boss.story}",
        title=f"[bold red]⚔️  BOSS FIGHT {boss.number} — {boss.name}[/bold red]",
        border_style="red",
        width=70,
    ))
    console.print("\n  [bold red]ALL STEPS MUST BE CORRECT.[/bold red]")
    pause()


def show_setup_intro():
    clear()
    console.print(Panel(
        "[italic]Before we begin, let's make sure Git is configured.[/italic]",
        title="[bold yellow]⚙️  Setup[/bold yellow]",
        border_style="yellow",
        width=70,
    ))


# ═══════════════════════════════════════════════════════════
#  DRILL ZONE
# ═══════════════════════════════════════════════════════════

def show_drill_header(required, total):
    console.print(f"\n  [bold white on red] 🎯 DRILL ZONE [/bold white on red]")
    console.print(f"  [dim]Get {required}/{total} correct to pass this level.[/dim]\n")


def show_drill_progress(correct, wrong, required, total):
    remaining = total - correct - wrong
    console.print(f"  [green]✅ {correct}[/green]  [red]❌ {wrong}[/red]  "
                  f"[dim]Remaining: {remaining}  |  Need: {required}[/dim]")


# ═══════════════════════════════════════════════════════════
#  RESULTS
# ═══════════════════════════════════════════════════════════

def show_stage_cleared(stage_label, msg=None):
    content = f"[bold green]🎉 CLEARED: {stage_label}[/bold green]"
    if msg:
        content += f"\n\n{msg}"
    console.print(Panel(content, border_style="green", width=70))
    pause()


def show_stage_failed(stage_label, msg=None):
    content = f"[bold red]💀 FAILED: {stage_label}[/bold red]"
    if msg:
        content += f"\n\n{msg}"
    console.print(Panel(content, border_style="red", width=70))


def show_boss_failed_mercy(stage_label, attempt_count, max_attempts):
    """Show boss failure with mercy option after too many attempts."""
    content = (
        f"[bold red]💀 FAILED: {stage_label}[/bold red]\n\n"
        f"Attempt {attempt_count}/{max_attempts}.\n"
    )
    if attempt_count >= max_attempts:
        content += "[yellow]You can type 'skip' to move past this boss fight.[/yellow]"
    console.print(Panel(content, border_style="red", width=70))


def show_game_complete(state):
    clear()
    console.print(Panel(
        f"[bold green]🏆 CONGRATULATIONS! 🏆[/bold green]\n\n"
        f"You completed GitGrind!\n\n"
        f"[dim]Final Stats[/dim]\n"
        f"  Accuracy:           {state.accuracy}%\n"
        f"  Commands typed:     {state.total_commands_typed}\n"
        f"  Commands learned:   {len(state.data['commands_learned'])}\n"
        f"  Time played:        {state.time_played_display}\n\n"
        f"[bold]A cheat sheet has been saved for you![/bold]",
        title="[bold yellow]🎓 GAME COMPLETE[/bold yellow]",
        border_style="yellow",
        width=70,
    ))
    # No pause() here — main.py handles the post-game flow
