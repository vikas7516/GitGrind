"""
GitGrind — Exercise runner.
Handles running levels, drill zones, exercise rounds, and boss fights.
"""
import random
import itertools
import difflib
from engine.validator import normalize, check_answer, check_fill_blank, check_multi_choice
import ui


# Special sentinel returned by run_exercise when player types 'quit'
QUIT_SENTINEL = "__QUIT__"

# Number of wrong retry attempts before the "skip" ghost hint appears
SKIP_UNLOCK_RETRIES = 2


# ═══════════════════════════════════════════════════════════
#  NEAR-MISS / "ALMOST RIGHT" DETECTION
# ═══════════════════════════════════════════════════════════

def _analyze_near_miss(user_input, accepted_answers):
    """
    Compare the user's input against accepted answers using fuzzy matching.
    Returns a helpful hint string if the answer is close, or None.
    """
    user_norm = normalize(user_input)

    best_ratio = 0.0
    best_answer = accepted_answers[0] if accepted_answers else ""
    best_answer_norm = normalize(best_answer)

    for answer in accepted_answers:
        answer_norm = normalize(answer)
        ratio = difflib.SequenceMatcher(None, user_norm, answer_norm).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_answer = answer
            best_answer_norm = answer_norm

    # Not even remotely close — no useful hint
    if best_ratio < 0.4:
        return None

    # Typo detection: very close but not identical
    if best_ratio >= 0.8:
        # Find the specific difference
        diff_parts = []
        sm = difflib.SequenceMatcher(None, user_norm, best_answer_norm)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "replace":
                diff_parts.append(f"'{user_norm[i1:i2]}' → '{best_answer_norm[j1:j2]}'")
            elif tag == "delete":
                diff_parts.append(f"remove '{user_norm[i1:i2]}'")
            elif tag == "insert":
                diff_parts.append(f"add '{best_answer_norm[j1:j2]}'")

        if diff_parts:
            fix_hint = ", ".join(diff_parts[:2])  # max 2 changes shown
            return f"Almost! Tiny fix needed: {fix_hint}"
        return "Almost! Check your spelling carefully"

    # Check if user answer is a subset (missing parts)
    if best_answer_norm.startswith(user_norm) and len(user_norm) < len(best_answer_norm):
        missing = best_answer_norm[len(user_norm):].strip()
        return f"You're on the right track but missing something at the end"

    if best_answer_norm.endswith(user_norm) and len(user_norm) < len(best_answer_norm):
        return f"Incomplete — you're missing the beginning part of the command"

    if user_norm in best_answer_norm:
        return "Getting closer! Your answer is part of it, but incomplete"

    # Check if user has extra parts
    if best_answer_norm in user_norm:
        return "Too much! You added extra parts that aren't needed"

    # Moderately close — generic encouragement
    if best_ratio >= 0.6:
        return "Close! Your answer is on the right track but not quite right"

    # Somewhat close
    if best_ratio >= 0.4:
        return "Not far off — rethink your approach"

    return None


# ═══════════════════════════════════════════════════════════
#  VALIDATION HELPER
# ═══════════════════════════════════════════════════════════

def _validate_input(exercise, user_input):
    """
    Validate user input against the exercise's accepted answers.
    Returns (correct: bool, matched_answer_or_None).
    """
    if exercise.type == "fill_blank":
        return check_fill_blank(user_input, exercise.answers)
    elif exercise.type == "multi_choice":
        return check_multi_choice(user_input, exercise.answers[0])
    else:
        return check_answer(user_input, exercise.answers)


# ═══════════════════════════════════════════════════════════
#  RETRY LOOP
# ═══════════════════════════════════════════════════════════

def _retry_loop(exercise, state, save_fn, allow_hint, first_user_input):
    """
    Core retry loop used after a wrong answer.
    The user must keep trying until they get it right or type 'skip'.
    Skip becomes available as a ghost hint after SKIP_UNLOCK_RETRIES wrong retries.

    Returns:
        True   — user eventually got the correct answer
        False  — user skipped the exercise
        QUIT_SENTINEL — user typed 'quit'
    """
    retry_wrong_count = 0
    last_user_input = first_user_input

    # Show first wrong-answer feedback with near-miss analysis
    near_miss = _analyze_near_miss(last_user_input, exercise.answers)
    ui.show_wrong_retry(last_user_input, near_miss)

    while True:
        retry_wrong_count += 1

        # After enough wrong retries, show the ghost skip hint
        if retry_wrong_count >= SKIP_UNLOCK_RETRIES:
            ui.show_skip_hint()

        # Get the next attempt
        user_input = ui.get_input(save_fn=save_fn)

        if user_input.lower() == "quit":
            return QUIT_SENTINEL

        # Check for skip (only actually skip if the hint has been shown)
        if user_input.lower() == "skip" and retry_wrong_count >= SKIP_UNLOCK_RETRIES:
            ui.show_skip_result(last_user_input, exercise.answers[0], exercise.explanation)
            state.record_skip()
            return False  # skipped

        # Check for hint
        if allow_hint and user_input.lower() == "hint" and exercise.hint:
            state.record_hint()
            ui.show_hint(exercise.hint)
            continue  # don't count hint as a wrong attempt

        # Validate
        correct, matched = _validate_input(exercise, user_input)
        last_user_input = user_input

        if correct:
            ui.show_correct(exercise.sim_output)
            return True
        else:
            # Near-miss analysis for better feedback
            near_miss = _analyze_near_miss(user_input, exercise.answers)
            ui.show_wrong_retry(user_input, near_miss)
            # Don't re-record wrong stats — was already recorded on first wrong attempt


def _retry_loop_step(step, state, save_fn, first_user_input):
    """
    Retry loop for a single sub-step of a multi_step exercise.
    Same logic as _retry_loop but for sub-steps.

    Returns:
        True   — user eventually got the correct answer
        False  — user skipped
        QUIT_SENTINEL — user typed 'quit'
    """
    retry_wrong_count = 0
    last_user_input = first_user_input

    near_miss = _analyze_near_miss(last_user_input, step.answers)
    ui.show_wrong_retry(last_user_input, near_miss)

    while True:
        retry_wrong_count += 1

        if retry_wrong_count >= SKIP_UNLOCK_RETRIES:
            ui.show_skip_hint()

        user_input = ui.get_input(save_fn=save_fn)

        if user_input.lower() == "quit":
            return QUIT_SENTINEL

        if user_input.lower() == "skip" and retry_wrong_count >= SKIP_UNLOCK_RETRIES:
            ui.show_skip_result(last_user_input, step.answers[0], step.explanation)
            state.record_skip()
            return False

        # Check for hint on sub-step
        if user_input.lower() == "hint" and step.hint:
            state.record_hint()
            ui.show_hint(step.hint)
            continue

        correct, matched = check_answer(user_input, step.answers)
        last_user_input = user_input

        if correct:
            ui.show_correct(step.sim_output)
            return True
        else:
            near_miss = _analyze_near_miss(user_input, step.answers)
            ui.show_wrong_retry(user_input, near_miss)


# ═══════════════════════════════════════════════════════════
#  EXERCISE RUNNER
# ═══════════════════════════════════════════════════════════

def run_exercise(exercise, state, index=None, total=None, allow_hint=True, record_stats=True):
    """
    Run a single exercise.

    Returns:
        True          — answered correctly (first try or via retries)
        False         — skipped (counts as wrong in drill/exercise rounds)
        QUIT_SENTINEL — player typed 'quit'
    """
    ui.show_exercise_prompt(exercise, index, total)

    save_fn = state.save

    # ── Multi-step exercises: run each sub-step in sequence ──
    if exercise.type == "multi_step" and exercise.steps:
        any_skipped = False
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

                # Enter retry loop for this sub-step
                result = _retry_loop_step(step, state, save_fn, user_input)
                if result == QUIT_SENTINEL:
                    return QUIT_SENTINEL
                if not result:
                    any_skipped = True
                # Continue to next step regardless

        # If any sub-step was skipped, the whole exercise is "skipped" (counts as wrong in drills)
        return not any_skipped

    # ── Single-answer exercises ──

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

    # Validate
    correct, matched = _validate_input(exercise, user_input)

    if correct:
        if record_stats:
            state.record_correct(first_try=first_attempt)
        ui.show_correct(exercise.sim_output)

        # Show streak if notable
        if state.current_streak >= 3:
            ui.show_streak(state.current_streak)

        return True
    else:
        # First wrong — record stats
        if record_stats:
            state.record_wrong()

        # Enter retry loop (no answer revealed, must try again or skip)
        result = _retry_loop(exercise, state, save_fn, allow_hint, user_input)
        if result == QUIT_SENTINEL:
            return QUIT_SENTINEL

        # Return the retry result: True if eventually correct, False if skipped
        return result


# ═══════════════════════════════════════════════════════════
#  LEVEL RUNNER
# ═══════════════════════════════════════════════════════════

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
            # Save each teaching to the notebook for later reference
            state.add_notebook_entry(teaching)
        state.save()

    # ── Phase 2: Exercises ───────────────────────────────
    # In the exercise phase, pass/fail doesn't matter — we just practice.
    # If they skip, it's fine. We only check QUIT_SENTINEL.
    ui.console.print(panel_header("📝 EXERCISES — Now let's practice!"))
    for i, ex in enumerate(level.exercises, 1):
        result = run_exercise(ex, state, i, len(level.exercises))
        if result == QUIT_SENTINEL:
            return QUIT_SENTINEL
        ui.console.print()

    # ── Phase 3: Quick Recap before Drills ────────────────
    if level.teachings:
        ui.show_drill_recap(level)

    # ── Phase 4: Drill Zone ──────────────────────────────
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


# ═══════════════════════════════════════════════════════════
#  EXERCISE ROUND RUNNER
# ═══════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════
#  BOSS FIGHT RUNNER
# ═══════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════
#  SETUP RUNNER
# ═══════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════
#  UTILITIES
# ═══════════════════════════════════════════════════════════

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
