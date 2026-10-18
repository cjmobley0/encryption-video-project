"""Palette, typography and the base scene for the encryption video.

Every colour here comes from encryption-video-plan.md and carries the same
meaning in every scene. Do not add a colour without updating that plan.

The names deliberately avoid Manim's own constants (GOLD, BLUE, GRAY...) so
that ``from manim import *`` followed by ``from style import *`` is safe in
either order.
"""

from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path

from manim import *

# --- palette ---------------------------------------------------------------

BG = "#14213D"       # background, dark navy
FG = "#F1FAEE"       # labels and text, off-white
PLAIN = "#3DDC97"    # plaintext: readable
CIPHER = "#FF6B4A"   # ciphertext: scrambled
PRIVATE = "#FFC93C"  # private / shared secret key, and every lock
PUBLIC = "#5BC0EB"   # public key
SNOOP = "#8D99AE"    # attacker / snooper

# Surfaces, tuned to sit on the navy without reading as a new colour.
SURFACE = "#1B2F52"
SURFACE_HI = "#24406E"

config.background_color = BG

# --- typography ------------------------------------------------------------

TITLE = 56
HEAD = 40
BODY = 30
LABEL = 24
SMALL = 19

SANS = "Avenir Next"  # geometric sans, to match the flat 3Blue1Brown look
MONO = "Menlo"  # ciphertext and plaintext notes, so scrambles keep their width

# Everything built with a bare Text() picks the family up from here.
Text.set_default(font=SANS)

# Outlines are thick and flat: no gradients anywhere in this video.
STROKE = 5
STROKE_THIN = 3.5


def title(text: str, color: str = FG, size: int = TITLE) -> Text:
    return Text(text, font=SANS, font_size=size, color=color, weight=BOLD)


def heading(text: str, color: str = FG, size: int = HEAD) -> Text:
    return Text(text, font=SANS, font_size=size, color=color, weight=SEMIBOLD)


def body(text: str, color: str = FG, size: int = BODY) -> Text:
    return Text(text, font=SANS, font_size=size, color=color)


def caption(text: str, color: str = FG, size: int = LABEL) -> Text:
    """A short on-screen label: PLAINTEXT, PUBLIC KEY, message..."""
    return Text(text, font=SANS, font_size=size, color=color, weight=MEDIUM)


def mono(text: str, color: str = PLAIN, size: int = BODY) -> Text:
    return Text(text, font_size=size, color=color, font=MONO)


# --- base scene ------------------------------------------------------------


class _BeatMixin:
    """Timing against the plan's beat tables.

    Each row of a beat table is one ``with self.beat(seconds, "...")`` block.
    Whatever the animations inside cost, the block holds the last frame until
    the window is full, so a scene always lands on the plan's clock. An
    overrun is logged rather than silently stealing time from the next beat.

    Every render also writes the windows it actually played to
    ``<media_dir>/timing/<Scene>.json``. ``narrate.py mix`` lays the narration
    down against that log rather than against the numbers in scenes.py, so a
    line still lands on its animation even if its beat overran the window.
    """

    TARGET: float | None = None

    def setup(self) -> None:
        self.camera.background_color = BG

    @property
    def beats(self) -> list[dict[str, float | str]]:
        """The beat windows played so far, in order."""
        log = getattr(self, "_beat_log", None)
        if log is None:
            log = self._beat_log = []
        return log

    def tear_down(self) -> None:
        """Hand the played beat windows to the audio mixdown."""
        if not self.beats:
            return
        out = Path(config.media_dir) / "timing" / f"{type(self).__name__}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({
            "scene": type(self).__name__,
            "target": self.TARGET,
            "duration": round(self.elapsed, 4),
            "frame_rate": float(config.frame_rate),
            "beats": self.beats,
        }, indent=2) + "\n")

    @property
    def elapsed(self) -> float:
        """Screen time rendered so far, read from Manim's own clock.

        Never count run times by hand: ``wait()`` is implemented as
        ``play(Wait(...))``, so hooking both counts every hold twice.
        """
        return float(getattr(self.renderer, "time", 0.0))

    def hold(self, seconds: float) -> None:
        if seconds > 1.5 / config.frame_rate:
            self.wait(seconds)

    @contextmanager
    def beat(self, seconds: float, note: str = ""):
        start = self.elapsed
        yield
        # What the animations inside actually cost, before any hold: the floor
        # narrate.py will not re-time this beat below.
        animation = self.elapsed - start
        over = animation - seconds
        if over > 0.05:
            logger.warning(
                f"{type(self).__name__}: beat overran by {over:+.2f}s "
                f"({seconds:.1f}s window) — {note}"
            )
        else:
            self.hold(-over)
        self.beats.append({
            "index": len(self.beats) + 1,
            "note": note,
            "window": seconds,
            "animation": round(animation, 4),
            "start": round(start, 4),
            "end": round(self.elapsed, 4),
        })

    def pad_to_target(self) -> None:
        """Hold the last frame until the scene fills its slot in the plan."""
        if self.TARGET is None:
            return
        left = self.TARGET - self.elapsed
        if left < -0.05:
            logger.warning(
                f"{type(self).__name__}: ran {-left:.2f}s over its "
                f"{self.TARGET:.0f}s slot"
            )
        self.hold(left)


class VideoScene(_BeatMixin, Scene):
    pass


class MovingVideoScene(_BeatMixin, MovingCameraScene):
    pass
