"""
GitGrind — Exercise runner.
Handles running levels, drill zones, exercise rounds, and boss fights.
"""
import random
import itertools
from engine.validator import check_answer, check_fill_blank, check_multi_choice
import ui


# Special sentinel returned by run_exercise when player types 'quit'
QUIT_SENTINEL = "__QUIT__"


def run_exercise(exercise, state, index=None, total=None, allow_hint=True, record_stats=True):
    """
    Run a single exercise. Returns True if correct, False if wrong,
    or QUIT_SENTINEL if the player typed 'quit'.
    """
    ui.show_exercise_prompt(exercise, index, total)

    save_fn = state.save

    # Multi-step exercises: run each sub-step in sequence
    if exercise.type == "multi_step" and exercise.steps:
        for si, step in enumerate(exercise.steps, 1):
            first_attempt = True
            ui.console.print(f"  [dim]Step {si}/{len(exercise.steps)}:[/dim] {step.prompt}")
            user_input = ui.get_input(save_fn=save_fn)
            if user_input.lower() == "quit":
                return QUIT_SENTINEL

            if allow_hint and user_input.lower() == "hint" and step.hint:
                if record_stats:
                    state.record_hint()
                ui.show_hint(step.hint)
                first_attempt = False
                user_input = ui.get_input(save_fn=save_fn)
                if user_input.lower() == "quit":
                    return QUIT_SENTINEL

            correct, matched = check_answer(user_input, step.answers)
            if correct:
                if record_stats:
                    state.record_correct(first_try=first_attempt)
                ui.show_correct(step.sim_output)
            else:
                if record_stats:
                    state.record_wrong()
                ui.show_wrong(step.answers[0], step.explanation)
                return False
        return True

    first_attempt = True
    user_input = ui.get_input(save_fn=save_fn)

    # Allow 'quit' command to exit to menu
    if user_input.lower() == "quit":
        return QUIT_SENTINEL

    # Allow 'hint' command
    if allow_hint and user_input.lower() == "hint" and exercise.hint:
        if record_stats:
            state.record_hint()
        ui.show_hint(exercise.hint)
        first_attempt = False
        user_input = ui.get_input(save_fn=save_fn)
        if user_input.lower() == "quit":
            return QUIT_SENTINEL

    # Validate based on type
    if exercise.type == "fill_blank":
        correct, matched = check_fill_blank(user_input, exercise.answers)
    elif exercise.type == "multi_choice":
        correct, matched = check_multi_choice(user_input, exercise.answers[0])
    else:
        correct, matched = check_answer(user_input, exercise.answers)

    if correct:
        if record_stats:
            state.record_correct(first_try=first_attempt)
        ui.show_correct(exercise.sim_output)

        # Show streak if notable
        if state.current_streak >= 3:
            ui.show_streak(state.current_streak)

        return True
    else:
        if record_stats:
            state.record_wrong()
        ui.show_wrong(exercise.answers[0], exercise.explanation)
        return False


def run_level(level, state):
    """
    Run a full level: concept → LESSON → exercises → drill zone.
    Returns True if cleared, False if failed, or QUIT_SENTINEL if quit.
    """
    ui.show_level_header(level)

    # ── Phase 1: Lesson (teach each command) ─────────────
    if level.teachings:
        ui.show_lesson_intro(level)
        for i, teaching in enumerate(level.teachings, 1):
            ui.show_teaching(teaching, i, len(level.teachings))

    # ── Phase 2: Exercises ───────────────────────────────
    ui.console.print(panel_header("📝 EXERCISES — Now let's practice!"))
    for i, ex in enumerate(level.exercises, 1):
        result = run_exercise(ex, state, i, len(level.exercises))
        if result == QUIT_SENTINEL:
            return QUIT_SENTINEL
        ui.console.print()

    # ── Phase 3: Drill Zone ──────────────────────────────
    required, total = level.drill_pass
    ui.show_drill_header(required, total)

    drills = _build_pool(level.drills, total)

    correct_count = 0
    wrong_count = 0

    for i, drill in enumerate(drills, 1):
        ui.show_drill_progress(correct_count, wrong_count, required, total)
        result = run_exercise(drill, state, i, total, allow_hint=False)
        if result == QUIT_SENTINEL:
            return QUIT_SENTINEL
        if result:
            correct_count += 1
        else:
            wrong_count += 1

    if correct_count >= required:
        state.learn_commands(level.commands_taught)
        return True
    else:
        return False


def run_exercise_round(er, state):
    """
    Run an exercise round (grinding session).
    Returns True if cleared, False if failed, or QUIT_SENTINEL if quit.
    """
    ui.show_exercise_round_header(er)

    required, total = er.pass_threshold
    exercises = _build_pool(er.exercises, total)

    correct_count = 0
    wrong_count = 0

    for i, ex in enumerate(exercises, 1):
        ui.show_drill_progress(correct_count, wrong_count, required, total)
        result = run_exercise(ex, state, i, total, allow_hint=False)
        if result == QUIT_SENTINEL:
            return QUIT_SENTINEL
        if result:
            correct_count += 1
        else:
            wrong_count += 1

    if correct_count >= required:
        return True
    else:
        return False


def run_boss_fight(boss, state):
    """
    Run a boss fight — sequential chain of steps. ALL must be correct.
    Stats are recorded per attempt for accuracy and learning tracking.
    """
    ui.show_boss_header(boss)

    total_steps = len(boss.steps)

    for i, step in enumerate(boss.steps, 1):
        ui.console.print(f"\n  [bold red]Step {i}/{total_steps}[/bold red]")
        result = run_exercise(step, state, i, total_steps, allow_hint=False, record_stats=True)

        if result == QUIT_SENTINEL:
            return QUIT_SENTINEL

        if not result:
            return False

    return True


def run_setup(setup_exercises, state):
    """
    Run the setup intro (not a level).
    Stats are NOT recorded — this is purely informational.
    """
    ui.show_setup_intro()

    for i, ex in enumerate(setup_exercises, 1):
        result = run_exercise(ex, state, i, len(setup_exercises), record_stats=False)
        if result == QUIT_SENTINEL:
            return QUIT_SENTINEL
        ui.console.print()

    state.setup_complete = True
    state.save()
    return True


def panel_header(text):
    """Quick section divider."""
    return f"\n  [bold white on grey23] {text} [/bold white on grey23]\n"


def _build_pool(items, total):
    """Build a shuffled pool of items sized to total, repeating if needed."""
    pool = list(items)
    if not pool:
        return []
    if len(pool) < total:
        pool = list(itertools.islice(itertools.cycle(pool), total))
    random.shuffle(pool)
    return pool[:total]
