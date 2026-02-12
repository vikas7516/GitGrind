#!/usr/bin/env python3
"""
GitGrind Validation Script
Run this anytime to validate the codebase integrity.

Usage: python validate.py
"""
import sys

def main():
    print("=" * 70)
    print("GITGRIND VALIDATION")
    print("=" * 70)

    errors = []

    # Test 1: Import main modules
    print("\n[1/4] Testing module imports...")
    try:
        import main
        import ui
        import cheatsheet
        from engine import runner, state, validator
        from content import models, stage_map
        from content.levels_basics import BASICS_LEVELS
        from content.levels_branch import BRANCH_LEVELS
        from content.levels_remote import REMOTE_LEVELS
        from content.levels_adv import ADVANCED_LEVELS
        from content.exercises import ALL_EXERCISE_ROUNDS
        from content.bossfights import ALL_BOSS_FIGHTS
        print("      OK - All modules import successfully")
    except ImportError as e:
        errors.append(f"Import error: {e}")
        print(f"      FAIL - {e}")

    # Test 2: Validate stage map
    print("\n[2/4] Validating stage map...")
    try:
        from content.stage_map import STAGE_MAP
        from content.models import STAGE_LEVEL, STAGE_EXERCISE, STAGE_BOSS

        ALL_LEVELS = {}
        ALL_LEVELS.update(BASICS_LEVELS)
        ALL_LEVELS.update(BRANCH_LEVELS)
        ALL_LEVELS.update(REMOTE_LEVELS)
        ALL_LEVELS.update(ADVANCED_LEVELS)

        for i, stage in enumerate(STAGE_MAP):
            # Check for proper data_key usage
            if not hasattr(stage, 'data_key'):
                errors.append(f"Stage {i}: Missing data_key attribute")

            # Check for deprecated attributes
            if hasattr(stage, 'level_number'):
                errors.append(f"Stage {i}: Using deprecated level_number")
            if hasattr(stage, 'round_number'):
                errors.append(f"Stage {i}: Using deprecated round_number")
            if hasattr(stage, 'fight_number'):
                errors.append(f"Stage {i}: Using deprecated fight_number")

            # Validate references
            if stage.stage_type == STAGE_LEVEL and stage.data_key not in ALL_LEVELS:
                errors.append(f"Stage {i}: Invalid level reference {stage.data_key}")
            elif stage.stage_type == STAGE_EXERCISE and stage.data_key not in ALL_EXERCISE_ROUNDS:
                errors.append(f"Stage {i}: Invalid exercise reference {stage.data_key}")
            elif stage.stage_type == STAGE_BOSS and stage.data_key not in ALL_BOSS_FIGHTS:
                errors.append(f"Stage {i}: Invalid boss reference {stage.data_key}")

        print(f"      OK - {len(STAGE_MAP)} stages validated")
    except Exception as e:
        errors.append(f"Stage validation error: {e}")
        print(f"      FAIL - {e}")

    # Test 3: Check Exercise structures
    print("\n[3/4] Validating exercise structures...")
    try:
        def validate_exercise(ex, context):
            if not hasattr(ex, 'answers') or not ex.answers:
                errors.append(f"{context}: Empty or missing answers")
            if not hasattr(ex, 'prompt'):
                errors.append(f"{context}: Missing prompt")
            # explanation should always exist due to dataclass default
            if not hasattr(ex, 'explanation'):
                errors.append(f"{context}: Missing explanation (unexpected)")

        for level_num, level in ALL_LEVELS.items():
            for i, ex in enumerate(level.exercises):
                validate_exercise(ex, f"Level {level_num}, Exercise {i}")
            for i, drill in enumerate(level.drills):
                validate_exercise(drill, f"Level {level_num}, Drill {i}")

        for round_num, er in ALL_EXERCISE_ROUNDS.items():
            for i, ex in enumerate(er.exercises):
                validate_exercise(ex, f"Round {round_num}, Exercise {i}")

        for boss_num, boss in ALL_BOSS_FIGHTS.items():
            for i, step in enumerate(boss.steps):
                validate_exercise(step, f"Boss {boss_num}, Step {i}")

        print("      OK - All exercises validated")
    except Exception as e:
        errors.append(f"Exercise validation error: {e}")
        print(f"      FAIL - {e}")

    # Test 4: Syntax check all Python files
    print("\n[4/4] Checking Python syntax...")
    try:
        import py_compile
        import os

        python_files = []
        for root, dirs, files in os.walk('.'):
            # Skip __pycache__ and hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            for file in files:
                if file.endswith('.py') and not file.startswith('.'):
                    python_files.append(os.path.join(root, file))

        for filepath in python_files:
            try:
                py_compile.compile(filepath, doraise=True)
            except py_compile.PyCompileError as e:
                errors.append(f"Syntax error in {filepath}: {e}")

        print(f"      OK - {len(python_files)} files checked")
    except Exception as e:
        errors.append(f"Syntax check error: {e}")
        print(f"      FAIL - {e}")

    # Summary
    print("\n" + "=" * 70)
    if errors:
        print(f"VALIDATION FAILED - {len(errors)} error(s) found:")
        for error in errors:
            print(f"  - {error}")
        print("=" * 70)
        return 1
    else:
        print("VALIDATION PASSED - All checks successful!")
        print("=" * 70)
        return 0

if __name__ == "__main__":
    sys.exit(main())

