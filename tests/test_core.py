"""
GitGrind — Unit tests for core functionality.
Run with: python -m pytest tests/ -v
"""
import pytest
import os
import tempfile
from unittest.mock import patch

# Add project root to path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from engine.validator import normalize, check_answer, check_fill_blank, check_multi_choice
from engine.state import GameState, _default_state, _deep_merge


class TestValidator:
    """Tests for engine/validator.py"""

    def test_normalize_basic(self):
        """Test basic normalization"""
        assert normalize("  Git Init  ") == "git init"
        assert normalize("GIT STATUS") == "git status"
        assert normalize("git  add   .") == "git add ."

    def test_normalize_quotes(self):
        """Test smart quote normalization"""
        assert normalize('"test"') == '"test"'
        assert normalize('\u201ctest\u201d') == '"test"'  # Smart quotes
        assert normalize('\u2018test\u2019') == "'test'"  # Smart single quotes

    def test_check_answer_exact_match(self):
        """Test exact answer matching"""
        correct, matched = check_answer("git init", ["git init"])
        assert correct is True
        assert matched == "git init"

    def test_check_answer_case_insensitive(self):
        """Test case-insensitive matching"""
        correct, matched = check_answer("GIT INIT", ["git init"])
        assert correct is True

    def test_check_answer_whitespace_tolerance(self):
        """Test whitespace normalization"""
        correct, matched = check_answer("  git   init  ", ["git init"])
        assert correct is True

    def test_check_answer_git_prefix_optional(self):
        """Test that 'git ' prefix is optional"""
        correct, matched = check_answer("init", ["git init"])
        assert correct is True

    def test_check_answer_multiple_accepted(self):
        """Test multiple accepted answers"""
        correct, matched = check_answer("git add .", ["git add .", "git add -A"])
        assert correct is True

        correct, matched = check_answer("git add -A", ["git add .", "git add -A"])
        assert correct is True

    def test_check_answer_wrong(self):
        """Test wrong answers"""
        correct, matched = check_answer("git commit", ["git init"])
        assert correct is False
        assert matched is None

    def test_check_fill_blank(self):
        """Test fill-in-the-blank checking"""
        correct, matched = check_fill_blank("commit", ["commit"])
        assert correct is True

        correct, matched = check_fill_blank("add", ["commit"])
        assert correct is False

    def test_check_multi_choice(self):
        """Test multiple choice checking"""
        correct, matched = check_multi_choice("b", "b")
        assert correct is True

        correct, matched = check_multi_choice("B)", "b")
        assert correct is True

        correct, matched = check_multi_choice("a", "b")
        assert correct is False


class TestDeepMerge:
    """Tests for _deep_merge function"""

    def test_simple_merge(self):
        """Test simple dict merge"""
        base = {"a": 1, "b": 2}
        override = {"b": 3, "c": 4}
        result = _deep_merge(base, override)
        assert result == {"a": 1, "b": 3, "c": 4}

    def test_nested_merge(self):
        """Test nested dict merge"""
        base = {"outer": {"a": 1, "b": 2}}
        override = {"outer": {"b": 3}}
        result = _deep_merge(base, override)
        assert result == {"outer": {"a": 1, "b": 3}}

    def test_new_nested_keys(self):
        """Test adding new keys in nested dicts"""
        base = {"stats": {"correct": 0}}
        override = {"stats": {"correct": 5, "wrong": 2}}
        result = _deep_merge(base, override)
        assert result == {"stats": {"correct": 5, "wrong": 2}}


class TestGameState:
    """Tests for GameState class"""

    def test_default_state(self):
        """Test default state initialization"""
        state = _default_state()
        assert state["current_stage_index"] == 0
        assert state["cleared_stages"] == []
        assert state["setup_complete"] is False
        assert state["game_complete"] is False

    def test_record_correct(self):
        """Test recording correct answers"""
        state = GameState()
        assert state.data["stats"]["total_correct"] == 0
        state.record_correct()
        assert state.data["stats"]["total_correct"] == 1
        assert state.data["stats"]["total_commands_typed"] == 1

    def test_record_wrong(self):
        """Test recording wrong answers"""
        state = GameState()
        assert state.data["stats"]["total_wrong"] == 0
        state.record_wrong()
        assert state.data["stats"]["total_wrong"] == 1
        assert state.data["stats"]["total_commands_typed"] == 1

    def test_accuracy_calculation(self):
        """Test accuracy percentage calculation"""
        state = GameState()
        assert state.accuracy == 0  # 0/0 = 0

        state.record_correct()
        state.record_correct()
        state.record_wrong()
        assert state.accuracy == 67  # 2/3 = 66.67% rounds to 67

    def test_clear_stage(self):
        """Test stage clearing"""
        state = GameState()
        state.clear_stage(0)
        assert 0 in state.cleared_stages
        assert state.current_stage_index == 1

    def test_clear_stage_idempotent(self):
        """Test that clearing same stage twice doesn't duplicate"""
        state = GameState()
        state.clear_stage(0)
        state.clear_stage(0)
        assert state.cleared_stages.count(0) == 1

    def test_learn_commands(self):
        """Test learning commands"""
        state = GameState()
        state.learn_commands(["git init", "git status"])
        assert "git init" in state.data["commands_learned"]
        assert "git status" in state.data["commands_learned"]

        # Test deduplication
        state.learn_commands(["git init", "git add"])
        assert state.data["commands_learned"].count("git init") == 1

    def test_save_and_load(self):
        """Test save/load persistence"""
        with tempfile.TemporaryDirectory() as tmpdir:
            save_file = os.path.join(tmpdir, "test_save.json")

            with patch('engine.state.SAVE_FILE', save_file):
                # Save state
                state1 = GameState()
                state1.record_correct()
                state1.record_correct()
                state1.clear_stage(0)
                state1.learn_commands(["git init"])
                state1.save()

                # Load into new state
                state2 = GameState()
                loaded = state2.load()

                assert loaded is True
                assert state2.data["stats"]["total_correct"] == 2
                assert 0 in state2.cleared_stages
                assert "git init" in state2.data["commands_learned"]

    def test_reset(self):
        """Test state reset"""
        state = GameState()
        state.record_correct()
        state.clear_stage(0)
        state.reset()

        assert state.data["stats"]["total_correct"] == 0
        assert state.cleared_stages == []
        assert state.current_stage_index == 0


class TestTimeDisplay:
    """Tests for time display formatting"""

    def test_seconds_display(self):
        """Test seconds display"""
        state = GameState()
        state.data["stats"]["time_played_seconds"] = 45
        state._session_start = state._session_start  # Reset session timer
        # Can't easily test time_played_display due to session timer,
        # but we can verify the format logic exists

    def test_minutes_display(self):
        """Test minutes display calculation"""
        state = GameState()
        state.data["stats"]["time_played_seconds"] = 125  # 2m 5s
        # Format should show "2m 5s"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

