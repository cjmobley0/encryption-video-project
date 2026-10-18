"""Every reusable object in the video, built from basic Manim shapes.

Each one is a small ``VGroup`` so that a key drawn in scene 1 is the identical
key in scene 10. Parts that get animated on their own (a lid, a door, a key's
teeth) are kept as named attributes.

Nothing here uses LaTeX: labels are ``Text`` only, so no TeX install is needed.
"""

from __future__ import annotations

import random
import string

from manim import *

from style import (
    BG, BODY, CIPHER, FG, LABEL, MONO, PLAIN, PRIVATE, PUBLIC, SMALL, SNOOP,
    STROKE, STROKE_THIN, SURFACE, SURFACE_HI, caption, mono,
)

# --- keys, locks, boxes ----------------------------------------------------


class Key(VGroup):
    """Circle bow, rectangular shaft, two teeth. Points right."""

    def __init__(self, color: str = PRIVATE, height: float = 0.55, **kw):
        super().__init__(**kw)
        bow = Annulus(
            inner_radius=0.17, outer_radius=0.33,
            color=color, fill_opacity=1, stroke_width=0,
        )
        shaft = Rectangle(
            width=1.0, height=0.17, color=color, fill_opacity=1, stroke_width=0,
        ).next_to(bow, RIGHT, buff=-0.05)
        teeth = VGroup()
        for dx, h in ((0.56, 0.24), (0.80, 0.17)):
            t = Rectangle(
                width=0.14, height=h, color=color, fill_opacity=1, stroke_width=0,
            )
            t.move_to(shaft.get_left() + RIGHT * dx + DOWN * (h / 2))
            teeth.add(t)
        self.add(bow, shaft, teeth)
        self.bow, self.shaft, self.teeth = bow, shaft, teeth
        self.key_color = color
        self.scale_to_fit_height(height)


class Padlock(VGroup):
    """Arc shackle over a rounded body, with a keyhole the camera can zoom to."""

    def __init__(self, color: str = PRIVATE, height: float = 1.1,
                 locked: bool = True, **kw):
        super().__init__(**kw)
        body = RoundedRectangle(
            width=0.95, height=0.78, corner_radius=0.14,
            color=color, fill_opacity=1, stroke_width=0,
        )
        shackle = Arc(
            radius=0.3, start_angle=0, angle=PI, color=color, stroke_width=10,
        )
        shackle.move_to(body.get_top() + UP * 0.22)
        keyhole = VGroup(
            Circle(radius=0.11, color=BG, fill_opacity=1, stroke_width=0),
            Triangle(color=BG, fill_opacity=1, stroke_width=0)
            .scale_to_fit_height(0.2).rotate(PI).stretch(0.55, 0),
        )
        keyhole[1].next_to(keyhole[0], DOWN, buff=-0.05)
        keyhole.move_to(body.get_center())
        self.add(shackle, body, keyhole)
        self.body, self.shackle, self.keyhole = body, shackle, keyhole
        self.lock_color = color
        if not locked:
            self.unlock()
        self.scale_to_fit_height(height)

    def unlock(self) -> "Padlock":
        self.shackle.shift(UP * 0.14).rotate(-0.5, about_point=self.shackle.get_left())
        return self

    def unlock_anim(self):
        return self.shackle.animate.shift(UP * 0.14 * self.height).rotate(
            -0.5, about_point=self.shackle.get_left()
        )


class Box(VGroup):
    """A box with a lid that swings open on its top-left corner."""

    def __init__(self, color: str = FG, width: float = 2.3, height: float = 1.6,
                 open_: bool = False, **kw):
        super().__init__(**kw)
        body = Rectangle(
            width=width, height=height, color=color, stroke_width=STROKE,
            fill_color=SURFACE, fill_opacity=1,
        )
        lid = Rectangle(
            width=width + 0.16, height=0.26, color=color, stroke_width=STROKE,
            fill_color=SURFACE_HI, fill_opacity=1,
        ).next_to(body, UP, buff=0)
        self.add(body, lid)
        self.body, self.lid = body, lid
        self.is_open = False
        if open_:
            self.open()

    @property
    def hinge(self):
        """Where the lid meets the body.

        Read live rather than stored: a stored point goes stale the moment the
        box is moved, and the lid then swings about somewhere off in the frame.
        """
        return self.body.get_corner(UL)

    def open(self, angle: float = 1.25) -> "Box":
        self.lid.rotate(angle, about_point=self.hinge)
        self.is_open = True
        return self

    def open_anim(self, angle: float = 1.25, **kw):
        self.is_open = True
        return Rotate(self.lid, angle, about_point=self.hinge, **kw)

    def close_anim(self, angle: float = 1.25, **kw):
        self.is_open = False
        return Rotate(self.lid, -angle, about_point=self.hinge, **kw)

    def inside(self):
        """Where a note sits when it is in the box."""
        return self.body.get_center()


class Note(VGroup):
    """A folded-paper card carrying a short message."""

    def __init__(self, text: str = "Meet at 3pm", color: str = PLAIN,
                 size: int = BODY, pad: float = 0.34, **kw):
        super().__init__(**kw)
        label = mono(text, color=color, size=size)
        card = RoundedRectangle(
            width=label.width + 2 * pad, height=label.height + 2 * pad,
            corner_radius=0.14, stroke_color=color, stroke_width=STROKE,
            fill_color=BG, fill_opacity=1,
        ).move_to(label)
        self.add(card, label)
        self.card, self.label = card, label
        self.message = text


POOL = string.ascii_letters + string.digits + "#$%&*@!?"


def scrambled(text: str, seed: int | None = None) -> str:
    rng = random.Random(seed)
    return "".join(" " if c == " " else rng.choice(POOL) for c in text)


def scramble(scene, mob: Text, steps: int = 7, color: str = CIPHER,
             run_time: float = 0.09, settle: str | None = None,
             size: float | None = None) -> None:
    """Cycle a ``Text`` through random characters, then settle on ``settle``.

    The size is pinned to whatever the text was first scrambled at.
    ``Text.font_size`` is derived from the mobject's current height, so every
    ``Transform`` to a string with different ascenders drifts it a little and
    the text would shrink a few percent per frame.
    """
    if size is None:
        size = getattr(mob, "_scramble_size", None) or mob.font_size
    mob._scramble_size = size

    source = settle if settle is not None else mob.text
    frames = [scrambled(source, seed=i) for i in range(steps)]
    if settle is not None:
        frames.append(settle)
    for i, s in enumerate(frames):
        landed = settle is not None and i == len(frames) - 1
        new = Text(
            s, font=MONO, font_size=size, color=PLAIN if landed else color,
        ).move_to(mob)
        new._scramble_size = size
        scene.play(Transform(mob, new), run_time=run_time)
        mob._scramble_size = size


# --- people ----------------------------------------------------------------


class Person(VGroup):
    """Circle head over a rounded body. Maya, Sam, and the crowd."""

    def __init__(self, color: str = FG, height: float = 1.5,
                 name: str | None = None, **kw):
        super().__init__(**kw)
        head = Circle(
            radius=0.27, color=color, stroke_width=STROKE,
            fill_color=BG, fill_opacity=1,
        )
        torso = RoundedRectangle(
            width=0.8, height=0.82, corner_radius=0.3, color=color,
            stroke_width=STROKE, fill_color=BG, fill_opacity=1,
        ).next_to(head, DOWN, buff=0.1)
        figure = VGroup(head, torso)
        self.add(figure)
        self.head, self.torso, self.figure = head, torso, figure
        figure.scale_to_fit_height(height)
        self.name_label = None
        if name:
            self.name_label = caption(name, color=color, size=LABEL)
            self.name_label.next_to(figure, DOWN, buff=0.22)
            self.add(self.name_label)


class Snooper(VGroup):
    """A grey figure in a hood: a dark face opening under a peaked cowl."""

    def __init__(self, color: str = SNOOP, height: float = 1.4, **kw):
        super().__init__(**kw)
        hood = VMobject(
            color=color, stroke_width=STROKE,
            fill_color=SURFACE, fill_opacity=1,
        )
        hood.set_points_smoothly([
            [-0.52, -0.42, 0], [-0.46, 0.12, 0], [0, 0.66, 0],
            [0.46, 0.12, 0], [0.52, -0.42, 0], [0, -0.52, 0], [-0.52, -0.42, 0],
        ])
        face = Ellipse(width=0.5, height=0.56, color=BG,
                       fill_opacity=1, stroke_width=0)
        face.move_to([0, 0.04, 0])
        eyes = VGroup(
            Dot(radius=0.04, color=color), Dot(radius=0.04, color=color),
        ).arrange(RIGHT, buff=0.15).move_to([0, 0.08, 0])
        torso = RoundedRectangle(
            width=1.34, height=0.76, corner_radius=0.3, color=color,
            stroke_width=STROKE, fill_color=BG, fill_opacity=1,
        )
        torso.move_to([0, -0.84, 0])
        self.add(torso, hood, face, eyes)
        self.head, self.hood, self.torso = hood, hood, torso
        self.scale_to_fit_height(height)


class GrabHand(VGroup):
    """A grey mitten that rises from the bottom of the frame."""

    def __init__(self, color: str = SNOOP, height: float = 1.4, **kw):
        super().__init__(**kw)
        palm = RoundedRectangle(
            width=0.9, height=0.95, corner_radius=0.22, color=color,
            stroke_width=STROKE, fill_color=BG, fill_opacity=1,
        )
        fingers = VGroup(*[
            RoundedRectangle(
                width=0.19, height=0.52, corner_radius=0.09, color=color,
                stroke_width=STROKE_THIN, fill_color=BG, fill_opacity=1,
            ) for _ in range(3)
        ]).arrange(RIGHT, buff=0.06)
        fingers.next_to(palm, UP, buff=-0.1).align_to(palm, RIGHT).shift(LEFT * 0.06)
        thumb = RoundedRectangle(
            width=0.19, height=0.4, corner_radius=0.09, color=color,
            stroke_width=STROKE_THIN, fill_color=BG, fill_opacity=1,
        ).rotate(0.5).next_to(palm, LEFT, buff=-0.12).shift(UP * 0.18)
        wrist = Rectangle(
            width=0.6, height=0.6, color=color, stroke_width=STROKE,
            fill_color=BG, fill_opacity=1,
        ).next_to(palm, DOWN, buff=-0.08)
        self.add(wrist, fingers, thumb, palm)
        self.scale_to_fit_height(height)


# --- the network -----------------------------------------------------------


class NetworkMap(VGroup):
    """A grid of dots joined by light-blue lines, like a city map."""

    def __init__(self, cols: int = 6, rows: int = 4, spacing: float = 1.15,
                 color: str = PUBLIC, seed: int = 7, **kw):
        super().__init__(**kw)
        rng = random.Random(seed)
        self.grid = {}
        dots = VGroup()
        for i in range(cols):
            for j in range(rows):
                p = RIGHT * i * spacing + UP * j * spacing
                p = p + RIGHT * rng.uniform(-0.13, 0.13) + UP * rng.uniform(-0.13, 0.13)
                d = Dot(p, radius=0.065, color=color)
                self.grid[(i, j)] = d
                dots.add(d)
        lines = VGroup()
        for (i, j), d in self.grid.items():
            for di, dj in ((1, 0), (0, 1)):
                other = self.grid.get((i + di, j + dj))
                if other is not None and rng.random() < 0.72:
                    lines.add(Line(
                        d.get_center(), other.get_center(),
                        color=color, stroke_width=2.2, stroke_opacity=0.55,
                    ))
        self.add(lines, dots)
        self.dots, self.lines = dots, lines
        self.center()

    def at(self, i: int, j: int):
        return self.grid[(i, j)].get_center()

    def path(self, waypoints) -> VMobject:
        """A smooth path through grid positions, for ``MoveAlongPath``."""
        pts = [self.at(i, j) for i, j in waypoints]
        p = VMobject()
        p.set_points_smoothly(pts)
        return p


# --- mail ------------------------------------------------------------------


class Mailbox(VGroup):
    """Rounded body, a blue letter slot, a door that swings, and a post."""

    def __init__(self, color: str = FG, slot_color: str = PUBLIC,
                 height: float = 2.6, **kw):
        super().__init__(**kw)
        shell = Union(
            Rectangle(width=2.2, height=0.95).shift(DOWN * 0.475),
            Sector(radius=1.1, start_angle=0, angle=PI).stretch(0.75, 1),
            color=color, stroke_width=STROKE,
            fill_color=SURFACE, fill_opacity=1,
        )
        slot = VGroup(
            RoundedRectangle(
                width=1.1, height=0.2, corner_radius=0.1, color=slot_color,
                stroke_width=0, fill_color=slot_color, fill_opacity=1,
            ),
            RoundedRectangle(
                width=0.94, height=0.07, corner_radius=0.035, color=BG,
                stroke_width=0, fill_color=BG, fill_opacity=1,
            ),
        )
        slot.move_to(shell.get_top() + DOWN * 0.42)
        door = RoundedRectangle(
            width=1.45, height=0.62, corner_radius=0.1, color=color,
            stroke_width=STROKE_THIN, fill_color=SURFACE_HI, fill_opacity=1,
        ).move_to(shell.get_center() + DOWN * 0.36)
        knob = Dot(door.get_right() + LEFT * 0.17, radius=0.07, color=PRIVATE)
        post = Rectangle(
            width=0.3, height=1.15, color=color, stroke_width=0,
            fill_color=color, fill_opacity=0.8,
        ).next_to(shell, DOWN, buff=-0.02)
        foot = Rectangle(
            width=0.8, height=0.14, color=color, stroke_width=0,
            fill_color=color, fill_opacity=0.8,
        ).next_to(post, DOWN, buff=0)
        self.add(foot, post, shell, door, knob, slot)
        self.shell, self.slot, self.door, self.knob, self.post = (
            shell, slot, door, knob, post
        )
        self.scale_to_fit_height(height)

    def open_door_anim(self, **kw):
        hinge = self.door.get_corner(UL)
        return AnimationGroup(
            Rotate(self.door, -2.0, axis=UP, about_point=hinge, **kw),
            Rotate(self.knob, -2.0, axis=UP, about_point=hinge, **kw),
        )

    def slot_point(self):
        return self.slot.get_center()


class Envelope(VGroup):
    def __init__(self, color: str = FG, height: float = 0.6,
                 fill: str = SURFACE, **kw):
        super().__init__(**kw)
        back = Rectangle(
            width=1.5, height=1.0, color=color, stroke_width=STROKE_THIN,
            fill_color=fill, fill_opacity=1,
        )
        flap = VMobject(color=color, stroke_width=STROKE_THIN)
        flap.set_points_as_corners([
            back.get_corner(UL), back.get_center() + DOWN * 0.08, back.get_corner(UR),
        ])
        self.add(back, flap)
        self.back, self.flap = back, flap
        self.scale_to_fit_height(height)


# --- devices ---------------------------------------------------------------


class Phone(VGroup):
    def __init__(self, color: str = FG, height: float = 2.0, **kw):
        super().__init__(**kw)
        shell = RoundedRectangle(
            width=1.0, height=1.9, corner_radius=0.16, color=color,
            stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        screen = RoundedRectangle(
            width=0.8, height=1.5, corner_radius=0.07, color=color,
            stroke_width=0, fill_color=BG, fill_opacity=1,
        ).move_to(shell)
        home = Line(LEFT * 0.16, RIGHT * 0.16, color=color, stroke_width=4)
        home.move_to(shell.get_bottom() + UP * 0.12)
        self.add(shell, screen, home)
        self.shell, self.screen = shell, screen
        self.scale_to_fit_height(height)


class Laptop(VGroup):
    def __init__(self, color: str = FG, height: float = 2.0, **kw):
        super().__init__(**kw)
        lid = RoundedRectangle(
            width=2.9, height=1.9, corner_radius=0.12, color=color,
            stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        screen = RoundedRectangle(
            width=2.6, height=1.6, corner_radius=0.06, color=color,
            stroke_width=0, fill_color=BG, fill_opacity=1,
        ).move_to(lid)
        base = Polygon(
            lid.get_corner(DL) + LEFT * 0.45 + DOWN * 0.3,
            lid.get_corner(DR) + RIGHT * 0.45 + DOWN * 0.3,
            lid.get_corner(DR), lid.get_corner(DL),
            color=color, stroke_width=STROKE, fill_color=SURFACE_HI, fill_opacity=1,
        )
        self.add(base, lid, screen)
        self.lid, self.screen, self.base = lid, screen, base
        self.scale_to_fit_height(height)


class Server(VGroup):
    def __init__(self, color: str = FG, height: float = 2.6, **kw):
        super().__init__(**kw)
        bays = VGroup()
        for _ in range(4):
            bay = RoundedRectangle(
                width=1.7, height=0.5, corner_radius=0.08, color=color,
                stroke_width=STROKE_THIN, fill_color=SURFACE, fill_opacity=1,
            )
            lights = VGroup(
                Dot(radius=0.05, color=PLAIN), Dot(radius=0.05, color=PUBLIC),
            ).arrange(RIGHT, buff=0.12)
            lights.move_to(bay.get_left() + RIGHT * 0.3)
            vent = VGroup(*[
                Line(ORIGIN, RIGHT * 0.5, color=color, stroke_width=2.2)
                for _ in range(2)
            ]).arrange(DOWN, buff=0.1)
            vent.move_to(bay.get_right() + LEFT * 0.45)
            bays.add(VGroup(bay, lights, vent))
        bays.arrange(DOWN, buff=0.1)
        self.add(bays)
        self.bays = bays
        self.scale_to_fit_height(height)


class BrowserBar(VGroup):
    def __init__(self, url: str = "https://", width: float = 5.2, **kw):
        super().__init__(**kw)
        bar = RoundedRectangle(
            width=width, height=0.8, corner_radius=0.4, color=FG,
            stroke_width=STROKE_THIN, fill_color=SURFACE, fill_opacity=1,
        )
        lock = Padlock(color=PRIVATE, height=0.42)
        lock.move_to(bar.get_left() + RIGHT * 0.55)
        text = Text(url, font=MONO, font_size=28, color=FG)
        text.next_to(lock, RIGHT, buff=0.28)
        self.add(bar, lock, text)
        self.bar, self.lock, self.url_text = bar, lock, text


class Gear(VGroup):
    def __init__(self, color: str = PUBLIC, radius: float = 0.6,
                 teeth: int = 10, **kw):
        super().__init__(**kw)
        ring = Annulus(
            inner_radius=radius * 0.42, outer_radius=radius,
            color=color, fill_opacity=1, stroke_width=0,
        )
        spikes = VGroup()
        for k in range(teeth):
            a = TAU * k / teeth
            t = Rectangle(
                width=radius * 0.3, height=radius * 0.34, color=color,
                fill_opacity=1, stroke_width=0,
            )
            t.move_to(radius * 1.08 * np.array([np.cos(a), np.sin(a), 0]))
            t.rotate(a, about_point=t.get_center())
            spikes.add(t)
        self.add(ring, spikes)


class Folder(VGroup):
    def __init__(self, color: str = PUBLIC, height: float = 1.4, **kw):
        super().__init__(**kw)
        tab = RoundedRectangle(
            width=0.85, height=0.3, corner_radius=0.07, color=color,
            stroke_width=STROKE_THIN, fill_color=SURFACE, fill_opacity=1,
        )
        shell = RoundedRectangle(
            width=1.9, height=1.3, corner_radius=0.11, color=color,
            stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        tab.next_to(shell, UP, buff=-0.08).align_to(shell, LEFT).shift(RIGHT * 0.18)
        self.add(tab, shell)
        self.shell, self.tab = shell, tab
        self.scale_to_fit_height(height)


class FileStack(VGroup):
    """Offset sheets of paper, seen from slightly above."""

    def __init__(self, n: int = 5, color: str = FG, width: float = 1.5, **kw):
        super().__init__(**kw)
        sheets = VGroup()
        for k in range(n):
            sheet = RoundedRectangle(
                width=width, height=width * 1.3, corner_radius=0.1, color=color,
                stroke_width=STROKE_THIN, fill_color=SURFACE, fill_opacity=1,
            )
            lines = VGroup(*[
                Line(ORIGIN, RIGHT * width * w, color=color,
                     stroke_width=2.6, stroke_opacity=0.7)
                for w in (0.5, 0.5, 0.3)
            ]).arrange(DOWN, buff=width * 0.17, aligned_edge=LEFT).move_to(sheet)
            page = VGroup(sheet, lines)
            page.shift(RIGHT * k * width * 0.17 + UP * k * width * 0.17)
            sheets.add(page)
        self.add(*reversed(sheets.submobjects))
        self.sheets = sheets


# --- icons -----------------------------------------------------------------


def _shield(color):
    s = Polygon(
        [-0.5, 0.6, 0], [0.5, 0.6, 0], [0.5, -0.1, 0],
        [0, -0.7, 0], [-0.5, -0.1, 0],
        color=color, stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
    )
    return s


def icon(kind: str, color: str = FG, height: float = 0.9) -> VGroup:
    """Flat, geometric icons. One drawing per kind, reused everywhere."""
    g = VGroup()

    if kind == "chat":
        bubble = RoundedRectangle(
            width=1.3, height=0.9, corner_radius=0.22, color=color,
            stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        tail = Triangle(color=color, stroke_width=0, fill_color=color,
                        fill_opacity=1).scale_to_fit_height(0.3).rotate(PI)
        tail.next_to(bubble, DOWN, buff=-0.06).shift(LEFT * 0.35)
        lines = VGroup(*[
            Line(ORIGIN, RIGHT * w, color=color, stroke_width=3.5)
            for w in (0.7, 0.5)
        ]).arrange(DOWN, buff=0.17, aligned_edge=LEFT).move_to(bubble)
        g.add(tail, bubble, lines)

    elif kind == "password":
        field = RoundedRectangle(
            width=1.5, height=0.62, corner_radius=0.12, color=color,
            stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        dots = VGroup(*[Dot(radius=0.075, color=color) for _ in range(4)])
        dots.arrange(RIGHT, buff=0.14).move_to(field)
        g.add(field, dots)

    elif kind == "card":
        shell = RoundedRectangle(
            width=1.5, height=0.95, corner_radius=0.12, color=color,
            stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        stripe = Rectangle(width=1.5, height=0.18, color=color,
                           fill_opacity=1, stroke_width=0)
        stripe.move_to(shell.get_top() + DOWN * 0.26)
        chip = RoundedRectangle(
            width=0.26, height=0.2, corner_radius=0.04, color=color,
            stroke_width=2.5, fill_opacity=0,
        ).move_to(shell.get_corner(DL) + RIGHT * 0.3 + UP * 0.25)
        g.add(shell, stripe, chip)

    elif kind == "cart":
        basket = Polygon(
            [-0.5, 0.25, 0], [0.55, 0.25, 0], [0.38, -0.3, 0], [-0.33, -0.3, 0],
            color=color, stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        handle = VMobject(color=color, stroke_width=STROKE)
        handle.set_points_as_corners([[-0.85, 0.6, 0], [-0.6, 0.6, 0], [-0.5, 0.25, 0]])
        wheels = VGroup(Dot(radius=0.09, color=color), Dot(radius=0.09, color=color))
        wheels.arrange(RIGHT, buff=0.42).next_to(basket, DOWN, buff=0.05)
        g.add(basket, handle, wheels)

    elif kind == "id":
        shell = RoundedRectangle(
            width=1.5, height=1.0, corner_radius=0.12, color=color,
            stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        face = Circle(radius=0.17, color=color, stroke_width=3.5)
        face.move_to(shell.get_left() + RIGHT * 0.38)
        lines = VGroup(*[
            Line(ORIGIN, RIGHT * w, color=color, stroke_width=3.5)
            for w in (0.55, 0.4, 0.5)
        ]).arrange(DOWN, buff=0.13, aligned_edge=LEFT)
        lines.next_to(face, RIGHT, buff=0.18)
        g.add(shell, face, lines)

    elif kind == "bank":
        roof = Triangle(color=color, stroke_width=STROKE, fill_color=SURFACE,
                        fill_opacity=1).stretch_to_fit_width(1.9).stretch_to_fit_height(0.55)
        cols = VGroup(*[
            Rectangle(width=0.16, height=0.6, color=color, stroke_width=0,
                      fill_color=color, fill_opacity=0.9) for _ in range(4)
        ]).arrange(RIGHT, buff=0.16)
        cols.next_to(roof, DOWN, buff=0.02)
        base = Rectangle(width=1.7, height=0.15, color=color, stroke_width=0,
                         fill_color=color, fill_opacity=0.9)
        base.next_to(cols, DOWN, buff=0.04)
        g.add(roof, cols, base)

    elif kind == "hospital":
        shell = RoundedRectangle(
            width=1.25, height=1.25, corner_radius=0.2, color=color,
            stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        cross = VGroup(
            Rectangle(width=0.7, height=0.22, color=color, stroke_width=0,
                      fill_color=color, fill_opacity=1),
            Rectangle(width=0.22, height=0.7, color=color, stroke_width=0,
                      fill_color=color, fill_opacity=1),
        ).move_to(shell)
        g.add(shell, cross)

    elif kind == "office":
        shell = Rectangle(width=1.1, height=1.5, color=color,
                          stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1)
        wins = VGroup(*[
            Square(side_length=0.18, color=color, stroke_width=0,
                   fill_color=color, fill_opacity=0.85) for _ in range(8)
        ]).arrange_in_grid(rows=4, cols=2, buff=0.14).move_to(shell).shift(UP * 0.08)
        g.add(shell, wins)

    elif kind == "government":
        block = Rectangle(width=1.6, height=0.8, color=color,
                          stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1)
        dome = Sector(radius=0.42, start_angle=0, angle=PI, color=color,
                      stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1)
        dome.next_to(block, UP, buff=0)
        spire = Line(ORIGIN, UP * 0.2, color=color, stroke_width=3.5)
        spire.next_to(dome, UP, buff=0)
        bars = VGroup(*[
            Line(UP * 0.26, DOWN * 0.26, color=color, stroke_width=3.5)
            for _ in range(3)
        ]).arrange(RIGHT, buff=0.32).move_to(block)
        g.add(block, dome, spire, bars)

    elif kind == "vpn":
        shell = _shield(color)
        txt = Text("VPN", font_size=22, color=color, weight=BOLD).scale(0.8)
        txt.move_to(shell.get_center() + UP * 0.03)
        g.add(shell, txt)

    elif kind == "shield":
        shell = _shield(color)
        check = VMobject(color=color, stroke_width=STROKE)
        check.set_points_as_corners([[-0.2, 0.08, 0], [-0.05, -0.1, 0], [0.24, 0.3, 0]])
        g.add(shell, check)

    elif kind == "link":
        a = RoundedRectangle(width=0.75, height=0.42, corner_radius=0.21,
                             color=color, stroke_width=STROKE)
        b = a.copy()
        a.rotate(-PI / 4).shift(LEFT * 0.16 + UP * 0.16)
        b.rotate(-PI / 4).shift(RIGHT * 0.16 + DOWN * 0.16)
        g.add(a, b)

    elif kind == "bug":
        shell = Ellipse(width=0.8, height=1.0, color=color, stroke_width=STROKE,
                        fill_color=SURFACE, fill_opacity=1)
        spine = Line(UP * 0.45, DOWN * 0.45, color=color, stroke_width=3)
        legs = VGroup()
        for side in (LEFT, RIGHT):
            for dy in (0.26, 0.0, -0.26):
                legs.add(Line(
                    side * 0.33 + UP * dy, side * 0.62 + UP * (dy + 0.14),
                    color=color, stroke_width=3.2,
                ))
        ants = VGroup(
            Line(UP * 0.45 + LEFT * 0.1, UP * 0.72 + LEFT * 0.26, color=color, stroke_width=3),
            Line(UP * 0.45 + RIGHT * 0.1, UP * 0.72 + RIGHT * 0.26, color=color, stroke_width=3),
        )
        g.add(legs, shell, spine, ants)

    elif kind == "email":
        g.add(Envelope(color=color, height=1.0, fill=SURFACE))

    elif kind == "file":
        sheet = RoundedRectangle(
            width=0.95, height=1.25, corner_radius=0.1, color=color,
            stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        lines = VGroup(*[
            Line(ORIGIN, RIGHT * w, color=color, stroke_width=3)
            for w in (0.55, 0.55, 0.35)
        ]).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(sheet)
        g.add(sheet, lines)

    elif kind == "cursor":
        g.add(Polygon(
            [0, 0, 0], [0, -0.62, 0], [0.17, -0.45, 0], [0.3, -0.72, 0],
            [0.42, -0.66, 0], [0.29, -0.4, 0], [0.5, -0.38, 0],
            color=FG, stroke_width=3, fill_color=FG, fill_opacity=1,
        ))

    else:
        raise ValueError(f"unknown icon: {kind}")

    g.scale_to_fit_height(height)
    return g


def labelled(mob: Mobject, text: str, color: str = FG, size: int = SMALL,
             buff: float = 0.22, direction=DOWN) -> VGroup:
    """An icon with its one-word label under it."""
    t = caption(text, color=color, size=size)
    t.next_to(mob, direction, buff=buff)
    return VGroup(mob, t)
