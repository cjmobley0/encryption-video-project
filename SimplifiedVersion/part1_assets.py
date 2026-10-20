"""The objects only this cut's Part 1 uses.

The timeline and the AES card are drawn differently in the professional cut —
different stops, different styling — so they are not in ``assets.py``, which
is byte-identical across both versions. Caesar's alphabet rows and the Enigma
rotors are shared, and live there.
"""

from __future__ import annotations

from manim import *

from assets import *
from style import (
    BG, FG, PLAIN, PRIVATE, SMALL, SNOOP, STROKE, STROKE_THIN, SURFACE,
    caption, title,
)


class HistoryTimeline(VGroup):
    """The line along the bottom of Part 1, with a marker that slides.

    One stop per era the narration reaches, so the viewer always knows where
    in the story they are. ``above(i)`` is where that era's picture goes.
    """

    STOPS = ("Ancient Rome", "1940s", "1970s", "2001", "Today")

    def __init__(self, width: float = 10.6, color: str = SNOOP,
                 marker_color: str = PRIVATE, size: int = SMALL, **kw):
        super().__init__(**kw)
        axis = Line(LEFT * width / 2, RIGHT * width / 2, color=color,
                    stroke_width=STROKE_THIN)
        ticks, labels = VGroup(), VGroup()
        last = len(self.STOPS) - 1
        for i, name in enumerate(self.STOPS):
            x = -width / 2 + width * i / last
            tick = Line(UP * 0.17, DOWN * 0.17, color=color,
                        stroke_width=STROKE_THIN).move_to(RIGHT * x)
            label = caption(name, color, size).next_to(tick, DOWN, buff=0.24)
            ticks.add(tick)
            labels.add(label)
        marker = Triangle(color=marker_color, fill_color=marker_color,
                          fill_opacity=1, stroke_width=0)
        marker.scale_to_fit_height(0.3).rotate(PI)
        marker.next_to(ticks[0], UP, buff=0.1)
        self.add(axis, ticks, labels, marker)
        self.axis, self.ticks, self.labels, self.marker = axis, ticks, labels, marker

    def at(self, i: int):
        return self.ticks[i].get_center()

    def above(self, i: int, buff: float = 1.0):
        """A point clear of the marker, where that era's picture belongs."""
        return self.at(i) + UP * buff

    def slide(self, i: int, **kw):
        """The marker moving to stop ``i``."""
        spot = self.at(i) + UP * (self.marker.get_center()[1] - self.at(i)[1])
        return self.marker.animate(**kw).move_to(spot)


class AESCard(VGroup):
    """The AES card that drops in at 2001, and the seal that stamps it."""

    def __init__(self, color: str = PRIVATE, width: float = 3.4, **kw):
        super().__init__(**kw)
        shell = RoundedRectangle(
            width=width, height=width * 0.62, corner_radius=0.18, color=color,
            stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        name = title("AES", color, 46).move_to(shell.get_center() + UP * 0.22)
        full = caption("Advanced Encryption Standard", FG, 15)
        full.move_to(shell.get_center() + DOWN * 0.55)
        self.add(shell, name, full)
        self.shell, self.name = shell, name

        # Built but not added: the scene stamps it on when the words land.
        self.seal = VGroup(
            Circle(radius=0.46, color=PLAIN, stroke_width=STROKE,
                   fill_color=BG, fill_opacity=0.9),
            caption("U.S.", PLAIN, 15).shift(UP * 0.12),
            caption("standard", PLAIN, 13).shift(DOWN * 0.13),
        )
        self.seal.move_to(shell.get_corner(DR))

    def badge(self, height: float = 0.5) -> VGroup:
        """The same card shrunk to a badge, for hopping onto a device."""
        b = VGroup(
            RoundedRectangle(width=height * 1.7, height=height,
                             corner_radius=0.08, color=PRIVATE,
                             stroke_width=STROKE_THIN, fill_color=SURFACE,
                             fill_opacity=1),
            caption("AES", PRIVATE, 14),
        )
        return b
