"""
GitGrind — Main entry-point and game loop.
"""
import sys
import ui
from engine.state import GameState
from engine.runner import (
    run_level, run_exercise_round, run_boss_fight, run_setup, QUIT_SENTINEL,
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
        from content.levels_basics import SETUP_EXERCISES
        return run_setup(SETUP_EXERCISES, state)

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
                ui.console.print("  [yellow]Boss skipped. Moving on.[/yellow]")
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
    while state.current_stage_index < TOTAL_STAGES:
        idx = state.current_stage_index
        stage = STAGE_MAP[idx]

        ui.show_level_map(STAGE_MAP, state.cleared_stages)
        ui.console.print(f"  [bold]Next: {stage.label}[/bold]\n")
        ui.pause()

        result = run_stage(idx, state)

        if result == QUIT_SENTINEL:
            state.save()
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
                    return
            else:
                # Non-boss retry
                retry = ui.get_input("  Retry? (y/n): ", save_fn=state.save)
                retry = retry.lower().strip()
                if retry not in ("y", "yes", "retry", "r"):
                    state.save()
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
        ui.console.print("\n  [bold green]📄 Your cheat sheet has been saved to git_cheatsheet.txt![/bold green]")
        ui.pause()


def play_replay(state):
    """Replay a previously cleared stage."""
    cleared = sorted(state.cleared_stages)
    if not cleared:
        ui.console.print("  [dim]No stages cleared yet![/dim]")
        ui.pause()
        return

    ui.console.print("\n  [bold underline]Replay a Stage[/bold underline]\n")
    # Show human-friendly numbering, not raw indices
    menu_map = {}
    for display_num, idx in enumerate(cleared, 1):
        stage = STAGE_MAP[idx]
        ui.console.print(f"  [{display_num}] {stage.label}")
        menu_map[str(display_num)] = idx

    ui.console.print(f"  [0] Back\n")
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
            ui.show_stage_cleared(stage.label, "Replayed successfully!")
        else:
            ui.show_stage_failed(stage.label)
    else:
        ui.console.print("  [red]Invalid choice.[/red]")
        ui.pause()


def play_reset(state):
    """Reset all progress."""
    ui.console.print("\n  [bold red]⚠️  This will DELETE all progress![/bold red]")
    confirm = ui.get_input("  Type 'RESET' to confirm: ", save_fn=state.save)
    if confirm == "RESET":
        state.reset()
        ui.console.print("  [green]Progress reset.[/green]")
    else:
        ui.console.print("  [dim]Cancelled.[/dim]")
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
        ui.console.print(f"[red]Error loading game state: {e}[/red]")
        ui.console.print("[yellow]Starting with fresh save...[/yellow]")
        state = GameState()

    try:
        while True:
            ui.show_main_menu(state, TOTAL_STAGES)
            choice = ui.get_input("  Choose: ", save_fn=state.save).lower().strip()

            if choice in ("c", "start", "continue"):
                play_continue(state)
            elif choice in ("r", "replay"):
                play_replay(state)
            elif choice in ("x", "reset"):
                play_reset(state)
            elif choice in ("q", "quit", "exit"):
                ui.console.print("  [dim]See you next time! 👋[/dim]")
                break
            else:
                ui.console.print("  [red]Invalid choice.[/red]")
                ui.pause()
    except KeyboardInterrupt:
        ui.console.print("\n[dim]Interrupted. Saving...[/dim]")
    except Exception as e:
        ui.console.print(f"\n[red]Unexpected error: {e}[/red]")
        ui.console.print("[yellow]Progress will be saved.[/yellow]")
        import traceback
        traceback.print_exc()
    finally:
        # Always save on exit, whether normal or exceptional
        try:
            state.save()
        except Exception as e:
            ui.console.print(f"[red]Failed to save: {e}[/red]")


if __name__ == "__main__":
    # Check Python version
    if sys.version_info < (3, 10):
        print("Error: Python 3.10 or higher is required.")
        print(f"You are running Python {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)

    main()
