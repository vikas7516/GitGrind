"""
GitGrind — Main entry-point and game loop.
"""
import sys
import ui
from engine.state import GameState
from engine.runner import (
    run_level, run_exercise_round, run_boss_fight, QUIT_SENTINEL,
)
from content.models import STAGE_SETUP, STAGE_LEVEL, STAGE_EXERCISE, STAGE_BOSS
from content.stage_map import STAGE_MAP
from content.levels_basics import BASICS_LEVELS
from content.levels_branch import BRANCH_LEVELS
from content.levels_remote import REMOTE_LEVELS
from content.levels_adv import ADVANCED_LEVELS
from content.exercises import ALL_EXERCISE_ROUNDS
from content.bossfights import ALL_BOSS_FIGHTS
from cheatsheet import generate_cheatsheet
from notebook import generate_notebook_txt


ALL_LEVELS = {}
ALL_LEVELS.update(BASICS_LEVELS)
ALL_LEVELS.update(BRANCH_LEVELS)
ALL_LEVELS.update(REMOTE_LEVELS)
ALL_LEVELS.update(ADVANCED_LEVELS)

# Validate no duplicate level keys
_level_counts = {}
for src in (BASICS_LEVELS, BRANCH_LEVELS, REMOTE_LEVELS, ADVANCED_LEVELS):
    for key in src:
        _level_counts[key] = _level_counts.get(key, 0) + 1
_duplicates = [k for k, v in _level_counts.items() if v > 1]
if _duplicates:
    raise ValueError(f"Duplicate level keys found: {_duplicates}")

# Validate all stages can be resolved
_missing_stages = []
for i, stage in enumerate(STAGE_MAP):
    if stage.stage_type == STAGE_LEVEL and stage.data_key not in ALL_LEVELS:
        _missing_stages.append(f"Stage {i}: Level {stage.data_key} not found")
    elif stage.stage_type == STAGE_EXERCISE and stage.data_key not in ALL_EXERCISE_ROUNDS:
        _missing_stages.append(f"Stage {i}: Exercise round {stage.data_key} not found")
    elif stage.stage_type == STAGE_BOSS and stage.data_key not in ALL_BOSS_FIGHTS:
        _missing_stages.append(f"Stage {i}: Boss fight {stage.data_key} not found")
if _missing_stages:
    raise ValueError(f"Stage map references missing content:\n" + "\n".join(_missing_stages))

TOTAL_STAGES = len(STAGE_MAP)

# Boss fight mercy rule — after this many attempts, allow skipping
BOSS_MAX_ATTEMPTS = 5


# ═══════════════════════════════════════════════════════════
#  STAGE DISPATCH
# ═══════════════════════════════════════════════════════════

def run_stage(stage_index, state):
    """
    Dispatch to the correct runner based on stage type.
    Returns True (cleared), False (failed), or QUIT_SENTINEL.
    """
    # Validate stage index to prevent crashes from corrupted saves
    if not (0 <= stage_index < len(STAGE_MAP)):
        import logging
        logging.getLogger(__name__).error("Invalid stage index: %d", stage_index)
        return False

    stage = STAGE_MAP[stage_index]

    if stage.stage_type == STAGE_SETUP:
        from content.levels_basics import SETUP_LEVEL
        return run_level(SETUP_LEVEL, state)

    elif stage.stage_type == STAGE_LEVEL:
        level = ALL_LEVELS.get(stage.data_key)
        if level:
            return run_level(level, state)

    elif stage.stage_type == STAGE_EXERCISE:
        er = ALL_EXERCISE_ROUNDS.get(stage.data_key)
        if er:
            return run_exercise_round(er, state)

    elif stage.stage_type == STAGE_BOSS:
        bf = ALL_BOSS_FIGHTS.get(stage.data_key)
        if bf:
            return run_boss_fight(bf, state)

    return False


# ═══════════════════════════════════════════════════════════
#  BOSS RETRY HANDLER
# ═══════════════════════════════════════════════════════════

def handle_boss_retry(stage_idx, stage, state):
    """
    Handle boss fight retry flow with mercy rule.
    Returns True if stage cleared, False if user quits.
    """
    boss_attempts = 1
    MAX_ITERATIONS = 100  # Safety guard against infinite loops
    iterations = 0

    while iterations < MAX_ITERATIONS:
        iterations += 1

        if boss_attempts >= BOSS_MAX_ATTEMPTS:
            ui.show_boss_failed_mercy(stage.label, boss_attempts, BOSS_MAX_ATTEMPTS)
            retry = ui.get_input("  Retry / Skip / Quit? (r/s/q): ", save_fn=state.save)
            retry = retry.lower().strip()
            if retry in ("s", "skip"):
                state.clear_stage(stage_idx)
                ui.console.print("  [bold bright_yellow]⏭️  Boss skipped. Moving on...[/bold bright_yellow]")
                ui.pause()
                return True
            elif retry in ("q", "quit", "n", "no"):
                return False
        else:
            retry = ui.get_input("  Retry? (y/n): ", save_fn=state.save)
            retry = retry.lower().strip()
            if retry not in ("y", "yes", "retry", "r"):
                return False

        result = run_stage(stage_idx, state)
        if result == QUIT_SENTINEL:
            return False

        boss_attempts += 1
        if result:
            state.clear_stage(stage_idx)
            ui.show_stage_cleared(stage.label)
            return True
        else:
            if boss_attempts < BOSS_MAX_ATTEMPTS:
                ui.show_stage_failed(stage.label)

    # Safety guard triggered
    import logging
    logging.getLogger(__name__).error("Boss retry exceeded safety limit")
    return False


# ═══════════════════════════════════════════════════════════
#  PLAY MODES
# ═══════════════════════════════════════════════════════════

def play_continue(state):
    """Continue from the current stage index."""
    state.start_session()

    while state.current_stage_index < TOTAL_STAGES:
        idx = state.current_stage_index
        stage = STAGE_MAP[idx]

        ui.show_level_map(STAGE_MAP, state.cleared_stages)
        ui.console.print(f"  [bold bright_yellow]⏭️  Next Up:[/bold bright_yellow] [bold bright_white]{stage.label}[/bold bright_white]\n")
        ui.pause()

        result = run_stage(idx, state)

        if result == QUIT_SENTINEL:
            state.save()
            ui.show_session_summary(state)
            return

        if result:
            state.clear_stage(idx)
            ui.show_stage_cleared(stage.label)
        else:
            ui.show_stage_failed(stage.label)

            # Boss fight mercy rule
            if stage.stage_type == STAGE_BOSS:
                if not handle_boss_retry(idx, stage, state):
                    state.save()
                    ui.show_session_summary(state)
                    return
            else:
                # Non-boss retry
                retry = ui.get_input("  Retry? (y/n): ", save_fn=state.save)
                retry = retry.lower().strip()
                if retry not in ("y", "yes", "retry", "r"):
                    state.save()
                    ui.show_session_summary(state)
                    return
                else:
                    continue  # retry the same stage

    # All stages cleared!
    if not state.game_complete:
        state.game_complete = True
        state.save()
        ui.show_game_complete(state)
        ui.pause()
        generate_cheatsheet(state)
        ui.console.print("\n  [bold bright_green]🎁 Rewards saved:[/bold bright_green] [bright_cyan]git_cheatsheet.txt[/bright_cyan] [dim]+[/dim] [bright_magenta]git_mastery_report.txt[/bright_magenta]")
        ui.pause()

    ui.show_session_summary(state)


def play_replay(state):
    """Replay a previously cleared stage."""
    cleared = sorted(state.cleared_stages)
    if not cleared:
        ui.console.print("  [italic bright_yellow]No stages cleared yet! Start playing to unlock replays.[/italic bright_yellow]")
        ui.pause()
        return

    ui.console.print("\n  [bold bright_cyan underline]🔁 Replay a Stage[/bold bright_cyan underline]")
    ui.console.print("  [dim]Practice makes perfect![/dim]\n")
    # Show human-friendly numbering, not raw indices
    menu_map = {}
    for display_num, idx in enumerate(cleared, 1):
        stage = STAGE_MAP[idx]
        # Color code by stage type
        if stage.stage_type == STAGE_BOSS:
            label_color = "bright_red"
        elif stage.stage_type == STAGE_EXERCISE:
            label_color = "bright_blue"
        else:
            label_color = "bright_cyan"
        ui.console.print(f"  [bold bright_white][{display_num}][/bold bright_white] [{label_color}]{stage.label}[/{label_color}]")
        menu_map[str(display_num)] = idx

    ui.console.print(f"  [dim][0] Back[/dim]\n")
    choice = ui.get_input("  Choose: ", save_fn=state.save)

    if choice == "0" or choice.lower() in ("back", "b", "q"):
        return

    if choice in menu_map:
        stage_idx = menu_map[choice]
        result = run_stage(stage_idx, state)
        if result == QUIT_SENTINEL:
            state.save()
            return
        stage = STAGE_MAP[stage_idx]
        if result:
            ui.show_stage_cleared(stage.label, "[bright_white]Replayed successfully![/bright_white]")
        else:
            ui.show_stage_failed(stage.label)
    else:
        ui.console.print("  [bold bright_red]❌ Invalid choice.[/bold bright_red]")
        ui.pause()


def play_notebook(state):
    """View the notebook and optionally save it as a text file."""
    ui.show_notebook(state)

    if not state.notebook_entries:
        ui.pause()
        return

    choice = ui.get_input("  Choose: ", save_fn=state.save).lower().strip()
    if choice in ("s", "save"):
        path = generate_notebook_txt(state)
        if path:
            ui.console.print(f"  [bold bright_green]✅ Notebook saved to:[/bold bright_green] [bright_cyan]{path}[/bright_cyan]")
        else:
            ui.console.print("  [bold bright_red]❌ Nothing to save — notebook is empty.[/bold bright_red]")
        ui.pause()


def play_reset(state):
    """Reset all progress."""
    ui.console.print("\n  [bold bright_red]⚠️  WARNING: This will DELETE all progress![/bold bright_red]")
    ui.console.print("  [italic bright_yellow]This action cannot be undone.[/italic bright_yellow]")
    confirm = ui.get_input("  Type 'RESET' to confirm: ", save_fn=state.save)
    if confirm == "RESET":
        state.reset()
        ui.console.print("  [bold bright_green]✅ Progress reset successfully.[/bold bright_green]")
    else:
        ui.console.print("  [italic bright_cyan]Reset cancelled.[/italic bright_cyan]")
    ui.pause()


# ═══════════════════════════════════════════════════════════
#  MAIN LOOP
# ═══════════════════════════════════════════════════════════

def main():
    """Main game loop with error handling."""
    try:
        state = GameState()
        state.load()
    except Exception as e:
        ui.console.print(f"[bold bright_red]⚠️  Error loading game state:[/bold bright_red] [bright_yellow]{e}[/bright_yellow]")
        ui.console.print("[italic bright_cyan]Starting with fresh save...[/italic bright_cyan]")
        state = GameState()

    try:
        while True:
            next_stage_label = None
            if 0 <= state.current_stage_index < TOTAL_STAGES:
                next_stage_label = STAGE_MAP[state.current_stage_index].label
            ui.show_main_menu(state, TOTAL_STAGES, next_stage_label)
            choice = ui.get_input("  Choose: ", save_fn=state.save).lower().strip()

            if choice in ("c", "start", "continue"):
                play_continue(state)
            elif choice in ("r", "replay"):
                play_replay(state)
            elif choice in ("n", "notebook"):
                play_notebook(state)
            elif choice in ("x", "reset"):
                play_reset(state)
            elif choice in ("q", "quit", "exit"):
                ui.console.print("  [bold bright_cyan]👋 See you next time, Git Master![/bold bright_cyan]")
                break
            else:
                ui.console.print("  [bold bright_red]❌ Invalid choice.[/bold bright_red] [dim]Try again.[/dim]")
                ui.pause()
    except KeyboardInterrupt:
        ui.console.print("\n[italic bright_cyan]💾 Interrupted. Saving progress...[/italic bright_cyan]")
    except Exception as e:
        ui.console.print(f"\n[bold bright_red]⚠️  Unexpected error:[/bold bright_red] [bright_yellow]{e}[/bright_yellow]")
        ui.console.print("[italic bright_cyan]Progress will be saved.[/italic bright_cyan]")
        import traceback
        traceback.print_exc()
    finally:
        # Always save on exit, whether normal or exceptional
        try:
            state.save()
        except Exception as e:
            ui.console.print(f"[bold bright_red]❌ Failed to save:[/bold bright_red] [bright_yellow]{e}[/bright_yellow]")


if __name__ == "__main__":
    # Check Python version
    if sys.version_info < (3, 10):
        print("Error: Python 3.10 or higher is required.")
        print(f"You are running Python {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)

    main()
