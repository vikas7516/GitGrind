"""
GitGrind — Sound feedback system.
Plays short melodies on key game events using winsound (Windows)
or a silent fallback on other platforms.

All sounds run in background threads so they never block the game.
"""
import threading
import sys

# ── Platform detection ──
_HAS_WINSOUND = False
if sys.platform == "win32":
    try:
        import winsound
        _HAS_WINSOUND = True
    except ImportError:
        pass


def _beep(freq, duration_ms):
    """Play a single tone in a background thread (non-blocking)."""
    if not _HAS_WINSOUND:
        return
    def _play():
        try:
            winsound.Beep(freq, duration_ms)
        except Exception:
            pass  # Never crash the game for a sound
    threading.Thread(target=_play, daemon=True).start()


def _melody(notes):
    """
    Play a sequence of (freq, duration_ms) tones in a background thread.
    Each note plays sequentially so the melody is audible.
    """
    if not _HAS_WINSOUND:
        return
    def _play():
        try:
            for freq, dur in notes:
                winsound.Beep(freq, dur)
        except Exception:
            pass
    threading.Thread(target=_play, daemon=True).start()


# ═══════════════════════════════════════════════════════════
#  GAME EVENT SOUNDS
# ═══════════════════════════════════════════════════════════

def sound_correct():
    """Bright ascending chirp — nailed it."""
    _melody([
        (523, 80),    # C5
        (659, 80),    # E5
        (784, 120),   # G5  — hold the top note slightly
    ])


def sound_wrong():
    """Low descending buzz — wrong answer."""
    _melody([
        (330, 120),   # E4
        (262, 180),   # C4
    ])


def sound_skip():
    """Neutral slide — skipped."""
    _melody([
        (392, 100),   # G4
        (349, 100),   # F4
        (330, 120),   # E4
    ])


def sound_hint():
    """Gentle ascending tap — hint unlocked."""
    _melody([
        (440, 70),    # A4
        (494, 70),    # B4
        (523, 90),    # C5
    ])


def sound_stage_cleared():
    """Triumphant 5-note fanfare — stage conquered."""
    _melody([
        (523, 100),   # C5
        (587, 80),    # D5
        (659, 80),    # E5
        (784, 100),   # G5
        (1047, 200),  # C6  — big finish
    ])


def sound_stage_failed():
    """Somber 3-note descend — didn't make it."""
    _melody([
        (440, 130),   # A4
        (349, 130),   # F4
        (262, 200),   # C4  — low end
    ])


def sound_streak():
    """Quick rising scale — streak milestone."""
    _melody([
        (659, 60),    # E5
        (784, 60),    # G5
        (880, 60),    # A5
        (1047, 100),  # C6
    ])


def sound_game_complete():
    """Grand 7-note celebration — game finished!"""
    _melody([
        (523, 100),   # C5
        (587, 80),    # D5
        (659, 80),    # E5
        (698, 80),    # F5
        (784, 100),   # G5
        (880, 100),   # A5
        (1047, 250),  # C6  — hold the climax
    ])


def sound_boss_intro():
    """Ominous 5-note low rumble — boss incoming."""
    _melody([
        (220, 150),   # A3
        (208, 130),   # Ab3
        (196, 130),   # G3
        (175, 150),   # F3
        (147, 200),   # D3  — deep rumble
    ])
