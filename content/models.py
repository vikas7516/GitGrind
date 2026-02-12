"""
GitGrind — Data models for levels, exercises, boss fights, and exercise rounds.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Union


class StageType(str, Enum):
    """Enumeration of stage types in the game."""
    SETUP = "setup"
    LEVEL = "level"
    EXERCISE = "exercise"
    BOSS = "boss"


@dataclass
class Teaching:
    """A single teaching slide shown during the lesson phase of a level."""
    command: str         # e.g. "git init"
    explanation: str     # 2-4 sentences: what it does, when/why
    syntax: str          # syntax template, e.g. "git add <file>"
    example_output: str  # simulated terminal session
    pro_tip: str = ""    # optional best practice / gotcha


@dataclass
class Exercise:
    """A single exercise prompt within a level, drill, exercise round, or boss fight."""
    type: str  # 'recall', 'fill_blank', 'scenario', 'multi_choice', 'error_fix',
               # 'rapid_fire', 'reverse', 'multi_step'
    prompt: str
    answers: list  # list of acceptable answer strings (any match = correct)
    hint: str = ""
    explanation: str = ""       # shown after wrong answer to explain why it's wrong
    sim_output: str = ""        # shown after correct answer
    error_output: str = ""      # shown if type is 'error_fix' (the error to diagnose)
    blank_template: str = ""    # for fill_blank: template like "git ____ -m 'msg'"
    choices: list = field(default_factory=list)  # for multi_choice: ['a) ...', 'b) ...']
    steps: list = field(default_factory=list)    # for multi_step: list of Exercise sub-steps


@dataclass
class Level:
    """One of the 20 main levels."""
    number: int
    name: str
    tagline: str
    concept: str           # 2-3 line concept card
    commands_taught: list  # e.g. ['git init', 'git status'] — for cheat sheet
    exercises: list        # list of Exercise
    drills: list           # list of Exercise (drill prompts)
    teachings: list = field(default_factory=list)  # list of Teaching (lesson phase)
    drill_pass: tuple = (8, 10)  # (required_correct, total)


@dataclass
class ExerciseRound:
    """One of the 5 exercise rounds (grinding sessions)."""
    number: int
    name: str
    tagline: str
    exercises: list          # list of Exercise
    pass_threshold: tuple    # (required_correct, total)


@dataclass
class BossFight:
    """One of the 5 boss fights — multi-step scenario gauntlets."""
    number: int
    name: str
    tagline: str
    story: str               # narrative intro
    steps: list              # list of Exercise (each step in the chain)


# Legacy constants for backward compatibility (deprecated, use StageType enum)
STAGE_SETUP = StageType.SETUP.value
STAGE_LEVEL = StageType.LEVEL.value
STAGE_EXERCISE = StageType.EXERCISE.value
STAGE_BOSS = StageType.BOSS.value


@dataclass
class Stage:
    """A single entry in the master stage map (31 stages total)."""
    stage_type: Union[str, StageType]  # one of StageType values
    data_key: int                # level number, exercise round number, or boss fight number
    label: str                   # display name

    def __post_init__(self) -> None:
        """Normalize stage_type to string for backward compatibility."""
        if isinstance(self.stage_type, StageType):
            self.stage_type = self.stage_type.value
