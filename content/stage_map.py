"""
GitGrind — Ordered list of all 31 stages in the game.
Defines the master progression: setup → levels → exercises → bosses.
"""
from content.models import Stage, STAGE_SETUP, STAGE_LEVEL, STAGE_EXERCISE, STAGE_BOSS


STAGE_MAP = [
    # ── Setup ────────────────────────────────────────────
    Stage(stage_type=STAGE_SETUP,    data_key=0,  label="⚙️  Setup Intro"),

    # ── Basics (Levels 1-3) ──────────────────────────────
    Stage(stage_type=STAGE_LEVEL,    data_key=1,  label="Level 1 — Init & Status"),
    Stage(stage_type=STAGE_LEVEL,    data_key=2,  label="Level 2 — Staging Files"),
    Stage(stage_type=STAGE_LEVEL,    data_key=3,  label="Level 3 — Committing"),

    # ── Exercise Round 1 ─────────────────────────────────
    Stage(stage_type=STAGE_EXERCISE, data_key=1,  label="💪 Exercise Round 1 — Absolute Basics"),

    # ── Basics cont (Levels 4-6) + Boss 1 ────────────────
    Stage(stage_type=STAGE_LEVEL,    data_key=4,  label="Level 4 — .gitignore"),
    Stage(stage_type=STAGE_LEVEL,    data_key=5,  label="Level 5 — Seeing Changes"),
    Stage(stage_type=STAGE_LEVEL,    data_key=6,  label="Level 6 — Reading History"),

    # ── Exercise Round 2 ─────────────────────────────────
    Stage(stage_type=STAGE_EXERCISE, data_key=2,  label="💪 Exercise Round 2 — Solo Repo Mastery"),

    # ── Boss Fight 1 ─────────────────────────────────────
    Stage(stage_type=STAGE_BOSS,     data_key=1,  label="⚔️  Boss Fight 1 — The Broken Repo"),

    # ── Branching (Levels 7-10) ──────────────────────────
    Stage(stage_type=STAGE_LEVEL,    data_key=7,  label="Level 7 — Branching"),
    Stage(stage_type=STAGE_LEVEL,    data_key=8,  label="Level 8 — Switching Branches"),
    Stage(stage_type=STAGE_LEVEL,    data_key=9,  label="Level 9 — Merging"),
    Stage(stage_type=STAGE_LEVEL,    data_key=10, label="Level 10 — Merge Conflicts"),

    # ── Exercise Round 3 ─────────────────────────────────
    Stage(stage_type=STAGE_EXERCISE, data_key=3,  label="💪 Exercise Round 3 — Branch Warfare"),

    # ── Boss Fight 2 ─────────────────────────────────────
    Stage(stage_type=STAGE_BOSS,     data_key=2,  label="⚔️  Boss Fight 2 — Three-Way Collision"),

    # ── Remotes (Levels 11-14) ───────────────────────────
    Stage(stage_type=STAGE_LEVEL,    data_key=11, label="Level 11 — Remotes & Origin"),
    Stage(stage_type=STAGE_LEVEL,    data_key=12, label="Level 12 — Clone"),
    Stage(stage_type=STAGE_LEVEL,    data_key=13, label="Level 13 — Push"),
    Stage(stage_type=STAGE_LEVEL,    data_key=14, label="Level 14 — Pull & Fetch"),

    # ── Exercise Round 4 ─────────────────────────────────
    Stage(stage_type=STAGE_EXERCISE, data_key=4,  label="💪 Exercise Round 4 — Remote Ops"),

    # ── Boss Fight 3 ─────────────────────────────────────
    Stage(stage_type=STAGE_BOSS,     data_key=3,  label="⚔️  Boss Fight 3 — The Sync Disaster"),

    # ── Advanced (Levels 15-20) ──────────────────────────
    Stage(stage_type=STAGE_LEVEL,    data_key=15, label="Level 15 — Restore & Reset"),
    Stage(stage_type=STAGE_LEVEL,    data_key=16, label="Level 16 — Revert"),
    Stage(stage_type=STAGE_LEVEL,    data_key=17, label="Level 17 — Stash"),
    Stage(stage_type=STAGE_LEVEL,    data_key=18, label="Level 18 — Reflog"),
    Stage(stage_type=STAGE_LEVEL,    data_key=19, label="Level 19 — Rebase"),
    Stage(stage_type=STAGE_LEVEL,    data_key=20, label="Level 20 — Pro Moves"),

    # ── Exercise Round 5 ─────────────────────────────────
    Stage(stage_type=STAGE_EXERCISE, data_key=5,  label="💪 Exercise Round 5 — The Final Grind"),

    # ── Boss Fight 4 ─────────────────────────────────────
    Stage(stage_type=STAGE_BOSS,     data_key=4,  label="⚔️  Boss Fight 4 — Detached HEAD Nightmare"),

    # ── THE FINAL BOSS ───────────────────────────────────
    Stage(stage_type=STAGE_BOSS,     data_key=5,  label="⚔️  Boss Fight 5 — THE FINAL BOSS"),
]
