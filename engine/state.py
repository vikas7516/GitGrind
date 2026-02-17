"""
GitGrind — Game state management and persistence.
Tracks progress, stats, and saves to disk.
"""
from __future__ import annotations

import json
import logging
import os
import tempfile
import time
from datetime import datetime
from typing import Any, Dict

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

SAVE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "save_data.json")


def _default_state() -> Dict[str, Any]:
    return {
        "current_stage_index": 0,
        "cleared_stages": [],
        "setup_complete": False,
        "glossary_seen": False,
        "stats": {
            "total_correct": 0,
            "total_wrong": 0,
            "total_commands_typed": 0,
            "first_try_correct": 0,
            "hints_used": 0,
            "current_streak": 0,
            "best_streak": 0,
            "start_time": datetime.now().isoformat(),
            "sessions": 0,
            "time_played_seconds": 0,
        },
        "commands_learned": [],
        "notebook_entries": {},  # {command: {syntax, explanation, pro_tip}}
        "game_complete": False,
    }


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge 'override' into 'base'.
    For dicts: recurse. For everything else: override wins.
    Returns the merged dict (mutates base).
    """
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def _load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Save file is not a JSON object")
    return data


def _atomic_write_json(path: str, data: Dict[str, Any]) -> bool:
    dir_path = os.path.dirname(path)
    fd, temp_path = tempfile.mkstemp(prefix=".gitgrind_save_", dir=dir_path)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.flush()
            try:
                os.fsync(f.fileno())
            except OSError:
                pass
        os.replace(temp_path, path)
        return True
    except (OSError, IOError, ValueError) as e:
        logger.warning("Failed to write save file: %s", e)
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except OSError:
            pass
        return False


class GameState:
    """Manages all game progress, stats, and save/load."""

    def __init__(self):
        self.data = _default_state()
        self._session_start = time.time()
        # Session-level counters (not persisted — reset each play session)
        self._session_correct = 0
        self._session_wrong = 0
        self._session_skipped = 0
        self._session_stages_cleared = 0
        self._session_active = False

    # ── Persistence ──────────────────────────────────────

    def save(self) -> None:
        elapsed = time.time() - self._session_start
        self.data["stats"]["time_played_seconds"] += int(elapsed)
        self._session_start = time.time()
        if not _atomic_write_json(SAVE_FILE, self.data):
            logger.warning("Progress not saved; will retry on next save.")

    def load(self) -> bool:
        if os.path.exists(SAVE_FILE):
            try:
                saved = _load_json(SAVE_FILE)
                _deep_merge(self.data, saved)
                self.data["stats"]["sessions"] += 1
                self._session_start = time.time()
                return True
            except (ValueError, json.JSONDecodeError, OSError, IOError, KeyError, TypeError) as e:
                logger.warning("Save file corrupted, starting fresh: %s", e)
                self.data = _default_state()
                return False
        return False

    def reset(self) -> None:
        self.data = _default_state()
        if os.path.exists(SAVE_FILE):
            try:
                os.remove(SAVE_FILE)
            except OSError:
                logger.warning("Failed to remove save file: %s", SAVE_FILE)

    # ── Progress ─────────────────────────────────────────

    @property
    def current_stage_index(self):
        return self.data["current_stage_index"]

    @current_stage_index.setter
    def current_stage_index(self, value):
        self.data["current_stage_index"] = value

    @property
    def cleared_stages(self):
        return self.data["cleared_stages"]

    @property
    def setup_complete(self):
        return self.data["setup_complete"]

    @setup_complete.setter
    def setup_complete(self, value):
        self.data["setup_complete"] = value

    @property
    def glossary_seen(self):
        return self.data.get("glossary_seen", False)

    @glossary_seen.setter
    def glossary_seen(self, value):
        self.data["glossary_seen"] = value

    @property
    def game_complete(self):
        return self.data["game_complete"]

    @game_complete.setter
    def game_complete(self, value):
        self.data["game_complete"] = value

    def clear_stage(self, stage_index):
        if stage_index not in self.data["cleared_stages"]:
            self.data["cleared_stages"].append(stage_index)
        if stage_index + 1 > self.data["current_stage_index"]:
            self.data["current_stage_index"] = stage_index + 1
        self._session_stages_cleared += 1
        self.save()

    def show_save_indicator(self):
        """Briefly show that progress was saved."""
        from rich.console import Console
        c = Console()
        c.print("  [dim]💾 Progress saved[/dim]")

    def is_stage_cleared(self, stage_index):
        return stage_index in self.data["cleared_stages"]

    # ── Stats ────────────────────────────────────────────

    def record_correct(self, first_try: bool = False) -> None:
        self.data["stats"]["total_correct"] += 1
        self.data["stats"]["total_commands_typed"] += 1
        if first_try:
            self.data["stats"]["first_try_correct"] += 1

        # Track streak
        self.data["stats"]["current_streak"] = self.data["stats"].get("current_streak", 0) + 1
        if self.data["stats"]["current_streak"] > self.data["stats"].get("best_streak", 0):
            self.data["stats"]["best_streak"] = self.data["stats"]["current_streak"]

        # Session tracking
        self._session_correct += 1

    def record_wrong(self) -> None:
        self.data["stats"]["total_wrong"] += 1
        self.data["stats"]["total_commands_typed"] += 1

        # Reset streak
        self.data["stats"]["current_streak"] = 0

        # Session tracking
        self._session_wrong += 1

    def record_hint(self) -> None:
        self.data["stats"]["hints_used"] += 1

    def record_skip(self) -> None:
        """Record that an exercise was skipped (for session summary)."""
        self._session_skipped += 1

    def learn_commands(self, commands):
        for cmd in commands:
            if cmd not in self.data["commands_learned"]:
                self.data["commands_learned"].append(cmd)

    # ── Notebook ─────────────────────────────────────────

    def add_notebook_entry(self, teaching) -> None:
        """Save a teaching to the notebook for later reference."""
        self.data.setdefault("notebook_entries", {})
        self.data["notebook_entries"][teaching.command] = {
            "syntax": teaching.syntax,
            "explanation": teaching.explanation,
            "pro_tip": teaching.pro_tip,
        }

    @property
    def notebook_entries(self) -> dict:
        """Get all notebook entries."""
        return self.data.get("notebook_entries", {})

    # ── Session Tracking ─────────────────────────────────

    def start_session(self) -> None:
        """Reset session-level counters for a new play session."""
        self._session_correct = 0
        self._session_wrong = 0
        self._session_skipped = 0
        self._session_stages_cleared = 0
        self._session_active = True

    @property
    def session_correct(self):
        return self._session_correct

    @property
    def session_wrong(self):
        return self._session_wrong

    @property
    def session_skipped(self):
        return self._session_skipped

    @property
    def session_stages_cleared(self):
        return self._session_stages_cleared

    @property
    def session_active(self):
        return self._session_active

    # ── Computed Properties ──────────────────────────────

    @property
    def accuracy(self) -> int:
        total = self.data["stats"]["total_correct"] + self.data["stats"]["total_wrong"]
        if total == 0:
            return 0
        return int(round(self.data["stats"]["total_correct"] / total * 100))

    @property
    def first_try_accuracy(self) -> int:
        total = self.data["stats"]["total_correct"] + self.data["stats"]["total_wrong"]
        if total == 0:
            return 0
        return int(round(self.data["stats"]["first_try_correct"] / total * 100))

    @property
    def total_commands_typed(self):
        return self.data["stats"]["total_commands_typed"]

    @property
    def hints_used(self):
        return self.data["stats"].get("hints_used", 0)

    @property
    def time_played_display(self):
        secs = self.data["stats"]["time_played_seconds"]
        secs += int(time.time() - self._session_start)
        if secs < 60:
            return f"{secs}s"
        mins = secs // 60
        if mins < 60:
            return f"{mins}m {secs % 60}s"
        hours = mins // 60
        remaining_mins = mins % 60
        if hours < 24:
            return f"{hours}h {remaining_mins}m"
        days = hours // 24
        remaining_hours = hours % 24
        return f"{days}d {remaining_hours}h"

    @property
    def current_streak(self):
        return self.data["stats"].get("current_streak", 0)

    @property
    def best_streak(self):
        return self.data["stats"].get("best_streak", 0)
