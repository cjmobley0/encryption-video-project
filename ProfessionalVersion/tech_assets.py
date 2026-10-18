"""The objects the professional cut needs on top of the simplified one.

``assets.py`` is the simplified video's object library, copied here unchanged
so a key drawn in that cut is the identical key in this one. Everything in
this file is new: the pieces a technical audience needs to see — a real
pipeline, an elliptic curve, a certificate, a hash box, a key-size comparison.

Keeping them apart rather than growing ``assets.py`` means the two videos
cannot drift: ``assets.py`` is the same file in both directories, and the
professional cut's extra machinery lives only where it is used.

Same rules as ``assets.py``: every object is a small ``VGroup`` built from
basic shapes, parts that get animated on their own are named attributes, and
nothing uses LaTeX — labels are ``Text``, exponents are Unicode (2¹²⁸).
"""

from __future__ import annotations

from manim import *

from assets import Gear, Key, Padlock, Person, Snooper, icon
from style import (
    ALGO, BG, BODY, CIPHER, FG, LABEL, MONO, PLAIN, PRIVATE, PUBLIC, SMALL,
    SNOOP, STROKE, STROKE_THIN, SURFACE, SURFACE_HI, caption, heading, mono,
)

# --- marks -----------------------------------------------------------------


def check_mark(color: str = PLAIN, height: float = 0.4) -> VMobject:
    """A tick. Used wherever a step succeeds or verifies."""
    m = VMobject(color=color, stroke_width=STROKE + 1)
    m.set_points_as_corners([
        [-0.22, 0.05, 0], [-0.05, -0.16, 0], [0.26, 0.3, 0],
    ])
    m.scale_to_fit_height(height)
    return m


def cross_mark(color: str = CIPHER, height: float = 0.4) -> VGroup:
    """An X. Used wherever a step fails."""
    g = VGroup(
        Line(UL, DR, color=color, stroke_width=STROKE + 1),
        Line(UR, DL, color=color, stroke_width=STROKE + 1),
    )
    g.scale_to_fit_height(height)
    return g


def verdict(ok: bool, height: float = 0.4) -> VMobject:
    return check_mark(height=height) if ok else cross_mark(height=height)


# --- the chapter tag -------------------------------------------------------


class ChapterTag(VGroup):
    """The small "2 · Types of Encryption" pill pinned to the top-left.

    It stays on screen for a whole chapter, so a viewer who joins eight
    minutes in still knows where they are. Scene 1 grows a chapter card into
    the title and then shrinks it into one of these, so the tag has to be
    transformable from a full-size card: ``card()`` builds that larger form
    out of the same submobjects, in the same order.
    """

    def __init__(self, number: int, title: str, color: str = FG, **kw):
        super().__init__(**kw)
        num = caption(str(number), color=PRIVATE, size=SMALL)
        label = caption(title, color=color, size=SMALL)
        row = VGroup(num, label).arrange(RIGHT, buff=0.22)
        shell = RoundedRectangle(
            width=row.width + 0.56, height=row.height + 0.34,
            corner_radius=0.14, color=color, stroke_width=2.2,
            stroke_opacity=0.5, fill_color=SURFACE, fill_opacity=0.65,
        ).move_to(row)
        self.add(shell, num, label)
        self.shell, self.number_text, self.label = shell, num, label
        self.number, self.title = number, title
        self.to_corner(UL, buff=0.35)
        self.base_width = self.width

    def pin_to(self, frame: Mobject, buff: float = 0.35) -> "ChapterTag":
        """Hold the tag in the corner of a moving camera.

        A ``MovingCameraScene`` that zooms or pulls back would otherwise swing
        the tag into the middle of the shot, or shrink it to nothing. Pinned,
        it sits in the same place and at the same apparent size in every
        scene, zoomed or not — which is the whole point of having it.
        """
        base = config.frame_width

        def follow(tag: Mobject) -> None:
            k = frame.width / base
            tag.scale_to_fit_width(self.base_width * k)
            tag.move_to(frame.get_corner(UL) + (RIGHT + DOWN) * buff * k,
                        aligned_edge=UL)

        self.add_updater(follow)
        follow(self)
        return self

    def card(self, size: int = BODY) -> VGroup:
        """The same tag as a full-size centre-screen card."""
        big = ChapterTag(self.number, self.title, color=self.label.color)
        big.number_text.font_size = size
        big.label.font_size = size
        return big.scale(size / SMALL).move_to(ORIGIN)


def chapter_card(number: int, title: str, color: str = FG) -> VGroup:
    """A centred chapter card: the big number over its title."""
    num = heading(str(number), color=PRIVATE, size=72)
    name = heading(title, color=color)
    rule = Line(LEFT * 1.4, RIGHT * 1.4, color=PRIVATE, stroke_width=3)
    return VGroup(num, rule, name).arrange(DOWN, buff=0.34)


# --- the history timeline (intro, scene 1) ---------------------------------


class HistoryTimeline(VGroup):
    """Caesar → Enigma → DES → AES along one line.

    The ticks are evenly spaced rather than to scale: two thousand years sit
    between the first two, and a true axis would bunch the last three into a
    single pixel. The dates are on screen, so nothing is being claimed about
    the spacing.
    """

    STOPS = (
        ("Caesar cipher", "~50 BC"),
        ("Enigma", "1920s"),
        ("DES", "1977"),
        ("AES", "2001"),
    )

    def __init__(self, width: float = 10.0, color: str = FG, **kw):
        super().__init__(**kw)
        axis = Line(LEFT * width / 2, RIGHT * width / 2,
                    color=color, stroke_width=STROKE_THIN)
        head = Triangle(color=color, stroke_width=0, fill_color=color,
                        fill_opacity=1).scale_to_fit_height(0.2)
        head.rotate(-PI / 2).move_to(axis.get_right())

        marks, labels = VGroup(), VGroup()
        n = len(self.STOPS)
        for i, (name, when) in enumerate(self.STOPS):
            x = interpolate(-width / 2 + 0.6, width / 2 - 0.9, i / (n - 1))
            at = RIGHT * x
            dot = Dot(at, radius=0.085, color=PRIVATE)
            tick = Line(at + DOWN * 0.16, at + UP * 0.16,
                        color=PRIVATE, stroke_width=3)
            label = caption(name, color=color, size=SMALL)
            year = caption(when, color=SNOOP, size=SMALL - 3)
            stack = VGroup(label, year).arrange(DOWN, buff=0.1)
            stack.next_to(at, UP if i % 2 == 0 else DOWN, buff=0.3)
            marks.add(VGroup(tick, dot))
            labels.add(stack)

        self.add(axis, head, marks, labels)
        self.axis, self.head, self.marks, self.labels = axis, head, marks, labels

    def write_anim(self, run_time: float = 2.4):
        """Draw the axis, then land the stops on it one at a time."""
        return Succession(
            AnimationGroup(Create(self.axis), FadeIn(self.head),
                           run_time=run_time * 0.3),
            LaggedStart(*[
                AnimationGroup(GrowFromCenter(m), FadeIn(l, shift=UP * 0.15))
                for m, l in zip(self.marks, self.labels)
            ], lag_ratio=0.45, run_time=run_time * 0.7),
        )

    def compress_anim(self, run_time: float = 1.0):
        """Squeeze to a thin line and slide off to the left.

        Scene 1 opens on this: the intro's whole timeline collapsing is what
        "now that we have looked at the history" looks like.
        """
        return AnimationGroup(
            FadeOut(self.labels, self.head, shift=UP * 0.2),
            self.marks.animate.set_opacity(0),
            self.axis.animate.stretch(0.04, 1).shift(LEFT * 16),
            run_time=run_time,
        )


# --- the pipeline (scenes 2, 3, 5) -----------------------------------------


class AlgoBox(VGroup):
    """A labelled process box with two gears turning inside it."""

    def __init__(self, label: str = "ALGORITHM", color: str = ALGO,
                 width: float = 2.7, height: float = 1.5, gears: bool = True,
                 **kw):
        super().__init__(**kw)
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.18, color=color,
            stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        self.add(shell)
        self.shell = shell
        self.gears = VGroup()
        if gears:
            big = Gear(color=color, radius=0.33, teeth=10)
            small = Gear(color=color, radius=0.22, teeth=8)
            big.move_to(shell.get_center() + LEFT * 0.26 + UP * 0.2)
            small.move_to(big.get_center() + RIGHT * 0.52 + DOWN * 0.14)
            self.gears.add(big, small)
            self.add(self.gears)
        text = caption(label, color=color, size=SMALL)
        text.move_to(shell.get_center() + (DOWN * 0.42 if gears else ORIGIN))
        self.add(text)
        self.label = text

    def turn(self, angle: float = TAU, **kw):
        """Both gears turning, the small one faster and the other way."""
        if not self.gears:
            return Wait(kw.get("run_time", 1.0))
        return AnimationGroup(
            Rotate(self.gears[0], angle, **kw),
            Rotate(self.gears[1], -angle * 1.4, **kw),
        )

    def set_label(self, text: str) -> "AlgoBox":
        new = caption(text, color=self.label.color, size=self.label.font_size)
        new.move_to(self.label)
        self.remove(self.label)
        self.add(new)
        self.label = new
        return self


class Pipeline(VGroup):
    """plaintext → ALGORITHM (+ key) → ciphertext, laid out left to right.

    The input and the output are slots rather than fixed text: the same
    pipeline carries a note in scene 2, runs backwards in scene 3 and takes a
    stream of blocks in scene 5. ``input_at`` and ``output_at`` say where a
    payload belongs, so a caller never has to know the internal spacing.
    """

    def __init__(self, label: str = "ALGORITHM", width: float = 9.0,
                 key_color: str = PRIVATE, **kw):
        super().__init__(**kw)
        algo = AlgoBox(label)
        gap = (width - algo.width) / 2

        in_slot = RoundedRectangle(
            width=gap * 0.62, height=1.5, corner_radius=0.14, color=PLAIN,
            stroke_width=STROKE_THIN, fill_color=BG, fill_opacity=1,
        ).next_to(algo, LEFT, buff=gap * 0.38)
        out_slot = in_slot.copy().set_stroke(color=CIPHER)
        out_slot.next_to(algo, RIGHT, buff=gap * 0.38)

        a_in = Arrow(in_slot.get_right(), algo.get_left(), buff=0.12,
                     color=FG, stroke_width=6, max_tip_length_to_length_ratio=0.22)
        a_out = Arrow(algo.get_right(), out_slot.get_left(), buff=0.12,
                      color=FG, stroke_width=6, max_tip_length_to_length_ratio=0.22)

        key = Key(key_color, height=0.5)
        key.next_to(algo, UP, buff=0.5)
        slot = Line(
            algo.get_top() + LEFT * 0.1, algo.get_top() + LEFT * 0.1 + UP * 0.18,
            color=key_color, stroke_width=5,
        )

        self.add(in_slot, a_in, algo, a_out, out_slot, slot, key)
        self.in_slot, self.out_slot = in_slot, out_slot
        self.arrow_in, self.arrow_out = a_in, a_out
        self.algo, self.key, self.key_slot = algo, key, slot
        self.body = VGroup(in_slot, a_in, algo, a_out, out_slot)

    def input_at(self):
        return self.in_slot.get_center()

    def output_at(self):
        return self.out_slot.get_center()

    def insert_key_anim(self, run_time: float = 0.6):
        """Drop the key into the slot on top of the algorithm box."""
        return self.key.animate(run_time=run_time).next_to(
            self.algo, UP, buff=0.12
        )

    def flow_anim(self, payload: Mobject, run_time: float = 1.4):
        """Carry something from the input slot through to the output slot."""
        path = VMobject().set_points_as_corners([
            self.input_at(), self.algo.get_center(), self.output_at(),
        ])
        return AnimationGroup(
            MoveAlongPath(payload, path, run_time=run_time),
            self.algo.turn(TAU, run_time=run_time),
        )


# --- hex and ciphertext ----------------------------------------------------


class HexText(VGroup):
    """A hex string on screen: monospace, wrapped, one ``Text`` per line.

    Kept as separate lines rather than one ``Text`` with newlines so a caller
    can recolour character *n* of the digest without counting past the line
    breaks — ``char(i)`` does that arithmetic. Scene 10's avalanche highlight
    is the reason this exists.
    """

    def __init__(self, text: str, color: str = CIPHER, width: int = 32,
                 size: int = SMALL, buff: float = 0.14, **kw):
        super().__init__(**kw)
        self.string = text
        self.width_chars = width
        self.lines = VGroup(*[
            Text(text[i:i + width], font=MONO, font_size=size, color=color)
            for i in range(0, len(text), width)
        ]).arrange(DOWN, buff=buff, aligned_edge=LEFT)
        self.add(self.lines)

    def char(self, i: int) -> Mobject:
        """Glyph ``i`` of the whole string, across the line breaks."""
        return self.lines[i // self.width_chars][i % self.width_chars]

    def chars(self, indices) -> VGroup:
        return VGroup(*[self.char(i) for i in indices])

    def type_anim(self, per_char: float = 0.012):
        return Succession(*[
            AddTextLetterByLetter(line, time_per_char=per_char)
            for line in self.lines
        ])


# --- the keyspace counter (scene 5) ----------------------------------------


class KeyspaceCounter(VGroup):
    """A brute-force attempt that visibly gets nowhere.

    The counter spins through billions of keys a second while the bar under
    it stays at zero. That gap is the whole point of "computationally
    impractical", and it reads better than any number written out.
    """

    KEYSPACE_128 = "2¹²⁸ ≈ 3.4 × 10³⁸ possible keys"

    def __init__(self, bar_width: float = 5.4, **kw):
        super().__init__(**kw)
        self.tracker = ValueTracker(0)

        tried = VGroup(
            caption("keys tried", color=SNOOP, size=SMALL),
            # mob_class=Text, not the MathTex default: this video has no
            # LaTeX install behind it, and a DecimalNumber would reach for one.
            DecimalNumber(0, num_decimal_places=0, group_with_commas=True,
                          color=CIPHER, font_size=BODY, mob_class=Text),
        ).arrange(RIGHT, buff=0.3)
        tried[1].add_updater(
            lambda d: d.set_value(self.tracker.get_value())
        )

        total = caption(self.KEYSPACE_128, color=FG, size=SMALL)

        track = RoundedRectangle(
            width=bar_width, height=0.3, corner_radius=0.15, color=SNOOP,
            stroke_width=2.5, fill_color=SURFACE, fill_opacity=1,
        )
        # Deliberately a sliver, not zero: an empty bar reads as "not started"
        # rather than "started, and this is how far it got".
        fill = RoundedRectangle(
            width=0.1, height=0.3, corner_radius=0.15, color=CIPHER,
            stroke_width=0, fill_color=CIPHER, fill_opacity=1,
        ).align_to(track, LEFT)
        percent = caption("0.000000 %", color=SNOOP, size=SMALL - 2)
        percent.next_to(track, RIGHT, buff=0.3)

        bar = VGroup(track, fill, percent)
        stack = VGroup(tried, total, bar).arrange(DOWN, buff=0.4)
        self.add(stack)
        self.counter, self.caption_total = tried[1], total
        self.track, self.fill, self.percent = track, fill, percent

    def count_to_anim(self, keys: float, run_time: float = 3.0):
        """Spin the counter up. ``rate_func=linear`` keeps it machine-like."""
        return self.tracker.animate(run_time=run_time, rate_func=linear) \
            .set_value(keys)

    def freeze(self) -> "KeyspaceCounter":
        self.counter.clear_updaters()
        return self


# --- pillars (scenes 6, 13) ------------------------------------------------


def _wrapped(label: str, max_width: float, size: int) -> str:
    """Break a label over two lines if one line would not fit.

    Measures the real rendered text rather than counting characters, since
    "Key length and randomness" and "Algorithm quality" have the same word
    count and very different widths.
    """
    if caption(label, size=size).width <= max_width:
        return label
    words = label.split()
    if len(words) < 2:
        return label
    # The split that leaves the two lines closest in length.
    best = min(
        range(1, len(words)),
        key=lambda i: abs(
            caption(" ".join(words[:i]), size=size).width
            - caption(" ".join(words[i:]), size=size).width
        ),
    )
    return " ".join(words[:best]) + "\n" + " ".join(words[best:])


class Pillar(VGroup):
    """An outline that fills from the bottom as its point is made."""

    def __init__(self, label: str, color: str = PUBLIC, width: float = 2.1,
                 height: float = 2.9, size: int = SMALL, **kw):
        super().__init__(**kw)
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.14, color=color,
            stroke_width=STROKE, fill_opacity=0,
        )
        fill = Rectangle(
            width=width - 0.14, height=0.001, color=color, stroke_width=0,
            fill_color=color, fill_opacity=0.18,
        )
        fill.align_to(shell, DOWN).shift(UP * 0.07)
        # Wrap rather than shrink: three pillars side by side with their
        # labels set at three different sizes reads as a mistake.
        text = caption(_wrapped(label, width - 0.3, size), color=color, size=size)
        if text.width > width - 0.2:
            text.scale((width - 0.2) / text.width)
        text.next_to(shell, DOWN, buff=0.25)
        self.add(shell, fill, text)
        self.shell, self.fill, self.label = shell, fill, text
        self.pad = 0.07

    def body_at(self):
        """Where an icon sits inside the pillar."""
        return self.shell.get_center()

    def fill_anim(self, fraction: float = 1.0, run_time: float = 0.7):
        # Measured off the shell as it is now, not off the size it was built
        # at: a pillar is usually scaled into its layout after construction,
        # and a stored height would send the fill straight out of the top.
        inner = self.shell.height - 2 * self.pad * self.shell.height / 2.9
        target = self.fill.copy()
        target.stretch_to_fit_height(max(inner * fraction, 0.001))
        target.align_to(self.shell, DOWN).shift(UP * inner * 0.02)
        return Transform(self.fill, target, run_time=run_time)


# --- the key lifecycle ring (scene 6) --------------------------------------


class LifecycleRing(VGroup):
    """generate → store → distribute → rotate → revoke, as a closed ring.

    A ring rather than a list because the last step feeds the first: key
    management is the thing that never finishes.
    """

    STEPS = ("generate", "store", "distribute", "rotate", "revoke")

    def __init__(self, steps=None, radius: float = 1.7, color: str = PUBLIC,
                 **kw):
        super().__init__(**kw)
        steps = tuple(steps or self.STEPS)
        ring = Circle(radius=radius, color=color, stroke_width=STROKE_THIN)
        dots, labels = VGroup(), VGroup()
        self.points_on_ring = []
        for i, step in enumerate(steps):
            angle = PI / 2 - TAU * i / len(steps)
            at = radius * np.array([np.cos(angle), np.sin(angle), 0])
            self.points_on_ring.append(at)
            dots.add(Dot(at, radius=0.08, color=PRIVATE))
            label = caption(step, color=FG, size=SMALL - 2)
            label.move_to(at)
            outward = at / np.linalg.norm(at)
            label.shift(outward * (label.width / 2 + 0.52)
                        + UP * outward[1] * (label.height / 2 + 0.1))
            labels.add(label)
        self.add(ring, dots, labels)
        self.ring, self.dots, self.labels, self.steps = ring, dots, labels, steps

    def draw_anim(self, run_time: float = 2.0):
        return Succession(
            Create(self.ring, run_time=run_time * 0.4),
            LaggedStart(*[
                AnimationGroup(GrowFromCenter(d), FadeIn(l, scale=0.7))
                for d, l in zip(self.dots, self.labels)
            ], lag_ratio=0.5, run_time=run_time * 0.6),
        )

    def travel_anim(self, key: Mobject, run_time: float = 3.0):
        """A key going round the ring, step after step, for ever.

        The path is a copy of the circle on screen rather than a fresh one of
        the construction radius, so it still fits after the ring is scaled
        into a layout.
        """
        return MoveAlongPath(key, self.ring.copy(), run_time=run_time,
                             rate_func=linear)


# --- spec cards (scenes 7, 8) ----------------------------------------------


class SpecCard(VGroup):
    """A named algorithm and the three or four facts that matter about it."""

    def __init__(self, title: str, lines, color: str = PUBLIC,
                 width: float = 4.1, **kw):
        super().__init__(**kw)
        head = heading(title, color=color, size=BODY)
        rule = Line(LEFT * (width / 2 - 0.4), RIGHT * (width / 2 - 0.4),
                    color=color, stroke_width=2.2, stroke_opacity=0.6)
        body = VGroup(*[
            VGroup(
                Dot(radius=0.045, color=color),
                caption(line, color=FG, size=SMALL - 2),
            ).arrange(RIGHT, buff=0.18)
            for line in lines
        ]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        if body.width > width - 0.7:
            body.scale((width - 0.7) / body.width)
        stack = VGroup(head, rule, body).arrange(DOWN, buff=0.24)
        shell = RoundedRectangle(
            width=width, height=stack.height + 0.8, corner_radius=0.18,
            color=color, stroke_width=STROKE_THIN,
            fill_color=SURFACE, fill_opacity=1,
        ).move_to(stack)
        self.add(shell, stack)
        self.shell, self.title, self.body = shell, head, body

    def flip_in(self, run_time: float = 0.7):
        """Turn in edge-on, like a card being dealt face up.

        Squashed to nothing horizontally and then opened out, rather than
        rotated about UP: a half turn in a 2D scene leaves the card facing
        the right way but with every glyph mirrored.
        """
        target = self.copy()
        self.stretch_to_fit_width(0.02).set_opacity(0)
        return Succession(
            self.animate(run_time=run_time * 0.25).set_opacity(1),
            Transform(self, target, run_time=run_time * 0.75),
        )


# --- Eve -------------------------------------------------------------------


class Eve(VGroup):
    """The attacker. The simplified cut's hooded figure, with her name on."""

    def __init__(self, height: float = 1.6, named: bool = True, **kw):
        super().__init__(**kw)
        figure = Snooper(height=height)
        self.add(figure)
        self.figure = figure
        self.name_label = None
        if named:
            self.name_label = caption("Eve", color=SNOOP, size=SMALL)
            self.name_label.next_to(figure, DOWN, buff=0.2)
            self.add(self.name_label)


def cast(height: float = 1.7) -> tuple[Person, Person, Eve]:
    """Maya, Sam and Eve, the three figures the whole video is built on."""
    return (
        Person(FG, height=height, name="Maya"),
        Person(FG, height=height, name="Sam"),
        Eve(height=height * 0.95),
    )


# --- throughput (scene 8) --------------------------------------------------


class ThroughputBar(VGroup):
    """A bar that fills at a given rate, for racing symmetric vs asymmetric.

    Qualitative on purpose: the plan asks for no numbers here. Real figures
    depend on hardware, key size and mode, and a made-up ratio on screen
    would be the one inaccurate frame in a video built on real values.
    """

    def __init__(self, label: str, rate: float = 1.0, color: str = PLAIN,
                 width: float = 5.0, **kw):
        super().__init__(**kw)
        self.rate = rate
        self.bar_width = width
        self.tracker = ValueTracker(0)

        track = RoundedRectangle(
            width=width, height=0.46, corner_radius=0.2, color=color,
            stroke_width=2.2, stroke_opacity=0.55,
            fill_color=SURFACE, fill_opacity=1,
        )
        fill = RoundedRectangle(
            width=0.001, height=0.46, corner_radius=0.2, color=color,
            stroke_width=0, fill_color=color, fill_opacity=1,
        )

        def resize(mob: Mobject) -> None:
            frac = min(self.tracker.get_value() * self.rate, 1.0)
            grown = RoundedRectangle(
                width=max(width * frac, 0.001), height=0.46, corner_radius=0.2,
                color=color, stroke_width=0, fill_color=color, fill_opacity=1,
            )
            # Pin to the track's left edge in both axes. Aligning only on x
            # leaves the fill at the origin once the bar is moved into a
            # layout, which puts it nowhere near its own track.
            grown.move_to(track.get_left(), aligned_edge=LEFT)
            mob.become(grown)

        fill.add_updater(resize)
        text = caption(label, color=color, size=SMALL)
        text.next_to(track, LEFT, buff=0.35)
        self.add(track, fill, text)
        self.track, self.fill, self.label = track, fill, text

    def run_anim(self, run_time: float = 2.2):
        return self.tracker.animate(run_time=run_time, rate_func=linear) \
            .set_value(1.0)

    def freeze(self) -> "ThroughputBar":
        self.fill.clear_updaters()
        return self


# --- elliptic curve (scene 8) ----------------------------------------------


class EllipticCurve(VGroup):
    """y² = x³ + ax + b, drawn for real, with points that hop along it.

    Defaults to a = -1, b = 1: a single smooth component, which is the shape
    a viewer pictures when they hear "elliptic curve". The equation is on
    screen in Unicode, since the whole video avoids LaTeX.
    """

    def __init__(self, a: float = -1.0, b: float = 1.0, color: str = PUBLIC,
                 x_range=(-1.6, 2.4), y_range=(-3.0, 3.0), **kw):
        super().__init__(**kw)
        self.a, self.b = a, b
        axes = Axes(
            x_range=[x_range[0], x_range[1], 1],
            y_range=[y_range[0], y_range[1], 1],
            x_length=4.2, y_length=4.0,
            axis_config={"color": SNOOP, "stroke_width": 2.2,
                         "include_ticks": False, "tip_length": 0.18},
        )
        curve = axes.plot_implicit_curve(
            lambda x, y: y ** 2 - x ** 3 - a * x - b,
            color=color,
        ).set_stroke(width=STROKE_THIN)
        equation = caption("y² = x³ + ax + b", color=color, size=SMALL)
        equation.next_to(axes, DOWN, buff=0.22)
        self.add(axes, curve, equation)
        self.axes, self.curve, self.equation = axes, curve, equation

    def point(self, x: float, upper: bool = True) -> np.ndarray:
        """A point on the curve at ``x``, on the upper or lower branch."""
        y2 = x ** 3 + self.a * x + self.b
        y = float(np.sqrt(max(y2, 0.0)))
        return self.axes.c2p(x, y if upper else -y)

    def hop_anim(self, dot: Mobject, xs, run_time: float = 2.0):
        """A point hopping from x to x along the curve, as scalar multiples."""
        steps = []
        for i, x in enumerate(xs):
            steps.append(dot.animate.move_to(self.point(x, upper=i % 2 == 0)))
        return Succession(*steps, run_time=run_time)


class KeySizeBars(VGroup):
    """RSA 3072 against ECC 256, at the same ~128-bit security level.

    Bar lengths are the key sizes themselves — 3072 and 256 bits — so the
    picture is the real ratio, not an illustration of one.
    """

    def __init__(self, width: float = 5.6, **kw):
        super().__init__(**kw)
        rows = VGroup()
        self.bars = VGroup()
        for name, bits, color in (("RSA", 3072, CIPHER), ("ECC", 256, PLAIN)):
            bar = Rectangle(
                width=max(width * bits / 3072, 0.12), height=0.5,
                color=color, stroke_width=0, fill_color=color, fill_opacity=0.85,
            )
            label = caption(f"{name} {bits}-bit", color=color, size=SMALL - 2)
            label.next_to(bar, RIGHT, buff=0.25)
            row = VGroup(bar, label)
            self.bars.add(bar)
            rows.add(row)
        for row in rows:
            row.align_to(rows[0][0], LEFT)
        rows.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        note = caption("same security level (~128-bit)", color=SNOOP, size=SMALL - 3)
        note.next_to(rows, DOWN, buff=0.35)
        self.add(rows, note)
        self.rows, self.note = rows, note

    def grow_anim(self, run_time: float = 1.4):
        return LaggedStart(*[
            GrowFromEdge(bar, LEFT) for bar in self.bars
        ], lag_ratio=0.45, run_time=run_time)


# --- HTTPS (scene 9) -------------------------------------------------------


class Certificate(VGroup):
    """The server's certificate: subject lines, a seal and a signature."""

    def __init__(self, host: str = "example.com", color: str = PUBLIC,
                 width: float = 3.0, **kw):
        super().__init__(**kw)
        title = caption("CERTIFICATE", color=color, size=SMALL - 2)
        lines = VGroup(*[
            caption(t, color=FG, size=SMALL - 4)
            for t in (f"subject: {host}", "issuer: Example CA", "public key: ECC P-256")
        ]).arrange(DOWN, buff=0.13, aligned_edge=LEFT)
        seal = VGroup(
            Circle(radius=0.26, color=PRIVATE, stroke_width=3),
            check_mark(PRIVATE, height=0.22),
        )
        body = VGroup(lines, seal).arrange(RIGHT, buff=0.3)
        stack = VGroup(title, body).arrange(DOWN, buff=0.22)
        if stack.width > width - 0.5:
            stack.scale((width - 0.5) / stack.width)
        shell = RoundedRectangle(
            width=width, height=stack.height + 0.6, corner_radius=0.14,
            color=color, stroke_width=STROKE_THIN,
            fill_color=SURFACE, fill_opacity=1,
        ).move_to(stack)
        self.add(shell, stack)
        self.shell, self.seal, self.lines = shell, seal, lines


class SessionKeyMerge(VGroup):
    """Two half-keys sliding together into one gold session key.

    Both sides derive the same key without it ever crossing the wire; the two
    halves are that, drawn. ``merge_anim`` leaves the finished key in place of
    the halves so the caller can go on using ``self.key``.
    """

    def __init__(self, height: float = 0.55, **kw):
        super().__init__(**kw)
        left = Key(PUBLIC, height=height)
        right = Key(PRIVATE, height=height)
        left.set_opacity(0.85)
        right.set_opacity(0.85)
        VGroup(left, right).arrange(RIGHT, buff=1.2)
        key = Key(PRIVATE, height=height).move_to(
            (left.get_center() + right.get_center()) / 2
        )
        key.set_opacity(0)
        self.add(left, right, key)
        self.left, self.right, self.key = left, right, key

    def merge_anim(self, run_time: float = 1.0):
        at = self.key.get_center()
        return AnimationGroup(
            self.left.animate.move_to(at).set_opacity(0),
            self.right.animate.move_to(at).set_opacity(0),
            self.key.animate.set_opacity(1),
            run_time=run_time,
        )


def data_record(color: str = PRIVATE, width: float = 0.42) -> VGroup:
    """One small locked record, for the session-data stream."""
    shell = RoundedRectangle(
        width=width, height=width * 0.72, corner_radius=0.07, color=color,
        stroke_width=2.2, fill_color=SURFACE, fill_opacity=1,
    )
    dot = Dot(radius=0.045, color=color).move_to(shell)
    return VGroup(shell, dot)


# --- hashing and signatures (scene 10) -------------------------------------


class HashBox(VGroup):
    """SHA-256 as a one-way box: an arrow in, an arrow out, no way back."""

    def __init__(self, label: str = "SHA-256", width: float = 2.4, **kw):
        super().__init__(**kw)
        box = AlgoBox(label, color=ALGO, width=width, height=1.1, gears=False)
        one_way = VGroup(
            Arrow(LEFT * 0.42, RIGHT * 0.42, color=SNOOP, buff=0,
                  stroke_width=3.5, max_tip_length_to_length_ratio=0.3),
            caption("one way", color=SNOOP, size=SMALL - 5),
        ).arrange(DOWN, buff=0.08)
        one_way.next_to(box, UP, buff=0.18)
        self.add(box, one_way)
        self.box, self.one_way = box, one_way


class DbTable(VGroup):
    """A users table with its salt and hash columns, as a password store."""

    def __init__(self, rows, width: float = 7.2, **kw):
        super().__init__(**kw)
        header = ("user", "salt", "sha256(salt + password)")
        grid = VGroup()
        self.rows = VGroup()
        col_x = (-width / 2 + 0.7, -width / 2 + 2.1, -width / 2 + 3.6)
        for r, record in enumerate((header, *rows)):
            is_head = r == 0
            line = VGroup()
            for x, cell in zip(col_x, record):
                t = (caption(cell, color=PUBLIC, size=SMALL - 3) if is_head
                     else Text(cell, font=MONO, font_size=SMALL - 4, color=FG))
                t.move_to(RIGHT * x, aligned_edge=LEFT)
                line.add(t)
            line.shift(DOWN * r * 0.46)
            grid.add(line)
            if not is_head:
                self.rows.add(line)
        rule = Line(LEFT * width / 2, RIGHT * width / 2,
                    color=PUBLIC, stroke_width=2, stroke_opacity=0.5)
        rule.next_to(grid[0], DOWN, buff=0.14).set_x(0)
        self.add(grid, rule)
        self.grid, self.rule, self.header = grid, rule, grid[0]


class SignatureFlow(VGroup):
    """message → hash → sign (private) → verify (public) → ✓ or ✗.

    Four stations in a row with the keys over the two that use them, so the
    gold key signing and the blue key verifying are visibly the same pair
    pulled apart.
    """

    STATIONS = ("message", "hash", "sign", "verify")

    def __init__(self, width: float = 10.0, **kw):
        super().__init__(**kw)
        colors = (PLAIN, ALGO, PRIVATE, PUBLIC)
        boxes = VGroup()
        for name, color in zip(self.STATIONS, colors):
            label = caption(name, color=color, size=SMALL - 2)
            shell = RoundedRectangle(
                width=1.9, height=0.9, corner_radius=0.14, color=color,
                stroke_width=STROKE_THIN, fill_color=SURFACE, fill_opacity=1,
            ).move_to(label)
            boxes.add(VGroup(shell, label))
        boxes.arrange(RIGHT, buff=(width - 4 * 1.9) / 3)

        arrows = VGroup(*[
            Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.1,
                  color=FG, stroke_width=4.5,
                  max_tip_length_to_length_ratio=0.3)
            for i in range(len(boxes) - 1)
        ])
        sign_key = Key(PRIVATE, height=0.38).next_to(boxes[2], UP, buff=0.22)
        verify_key = Key(PUBLIC, height=0.38).next_to(boxes[3], UP, buff=0.22)

        self.add(boxes, arrows, sign_key, verify_key)
        self.boxes, self.arrows = boxes, arrows
        self.sign_key, self.verify_key = sign_key, verify_key

    def station(self, name: str) -> VGroup:
        return self.boxes[self.STATIONS.index(name)]

    def build_anim(self, run_time: float = 2.4):
        steps = [GrowFromCenter(self.boxes[0])]
        for arrow, box in zip(self.arrows, self.boxes[1:]):
            steps.append(AnimationGroup(GrowArrow(arrow), GrowFromCenter(box)))
        return LaggedStart(*steps, lag_ratio=0.6, run_time=run_time)


# --- VPNs, rings and the globe (scenes 12, 13) -----------------------------


class Tunnel(VGroup):
    """An encrypted tunnel: two parallel walls with a dashed line down it.

    The dashes move, so the tunnel reads as carrying traffic rather than
    being a drawn pipe. ``flow_anim`` is the thing to play under a VPN beat.
    """

    def __init__(self, start, end, color: str = PRIVATE, radius: float = 0.42,
                 bow: float = 0.55, **kw):
        super().__init__(**kw)
        start, end = np.array(start, dtype=float), np.array(end, dtype=float)
        mid = (start + end) / 2 + UP * bow
        normal = UP * radius

        spine = VMobject()
        spine.set_points_smoothly([start, mid, end])
        walls = VGroup()
        for side in (1, -1):
            wall = VMobject(color=color, stroke_width=STROKE_THIN)
            wall.set_points_smoothly([
                start + normal * side, mid + normal * side, end + normal * side,
            ])
            walls.add(wall)
        dashes = DashedVMobject(
            spine.copy().set_stroke(color=color, width=3, opacity=0.8),
            num_dashes=22, dashed_ratio=0.45,
        )
        self.add(walls, dashes)
        self.spine, self.walls, self.dashes = spine, walls, dashes
        self.tunnel_color = color

    def draw_anim(self, run_time: float = 1.2):
        return AnimationGroup(
            Create(self.walls, lag_ratio=0.2),
            FadeIn(self.dashes),
            run_time=run_time,
        )

    def flow_anim(self, payload: Mobject, run_time: float = 1.6):
        return MoveAlongPath(payload, self.spine, run_time=run_time)


class DefenseRings(VGroup):
    """Concentric rings: encryption inside, the other controls around it.

    Scene 13 needs the gaps between them to be visible, so the rings are
    drawn with gaps in the stroke rather than as solid circles — the point
    being made is that the layers do not meet.
    """

    def __init__(self, labels, inner: float = 1.25, step: float = 0.72,
                 colors=None, **kw):
        super().__init__(**kw)
        labels = tuple(labels)
        colors = colors or (PRIVATE, PUBLIC, PLAIN, ALGO)
        self.rings, self.labels = VGroup(), VGroup()
        for i, name in enumerate(labels):
            r = inner + i * step
            color = colors[i % len(colors)]
            ring = Circle(radius=r, color=color, stroke_width=STROKE_THIN)
            tag = caption(name, color=color, size=SMALL - 3)
            tag.move_to(UP * r)
            tag.add_background_rectangle(color=BG, opacity=1, buff=0.1)
            self.rings.add(ring)
            self.labels.add(tag)
        self.add(self.rings, self.labels)
        self.outer_radius = inner + (len(labels) - 1) * step

    def draw_anim(self, run_time: float = 2.6):
        return LaggedStart(*[
            AnimationGroup(Create(ring), FadeIn(tag))
            for ring, tag in zip(self.rings, self.labels)
        ], lag_ratio=0.55, run_time=run_time)

    def gaps(self, count: int = 3) -> VGroup:
        """Points between the rings, where scene 13 puts its spotlights."""
        out = VGroup()
        for k in range(count):
            angle = PI / 2 + TAU * (k + 0.5) / count
            r = self.outer_radius - 0.36
            out.add(Dot(r * np.array([np.cos(angle), np.sin(angle), 0]),
                        radius=0.06, color=CIPHER))
        return out


class NetworkGlobe(VGroup):
    """A wire globe of connected nodes, for the last shot of the video."""

    def __init__(self, radius: float = 2.0, rings: int = 4, nodes: int = 7,
                 color: str = PUBLIC, **kw):
        super().__init__(**kw)
        outline = Circle(radius=radius, color=color, stroke_width=STROKE_THIN)
        meridians = VGroup(*[
            Ellipse(width=2 * radius * w, height=2 * radius,
                    color=color, stroke_width=1.8, stroke_opacity=0.5)
            for w in (0.28, 0.62, 1.0)
        ])
        parallels = VGroup(*[
            Line(LEFT * radius * np.cos(np.arcsin(y)),
                 RIGHT * radius * np.cos(np.arcsin(y)),
                 color=color, stroke_width=1.6, stroke_opacity=0.4)
            .shift(UP * radius * y)
            for y in (-0.62, -0.25, 0.25, 0.62)
        ])

        dots = VGroup()
        for i in range(nodes):
            angle = TAU * i / nodes + 0.4
            r = radius * (0.55 + 0.4 * ((i * 3) % 5) / 5)
            dots.add(Dot(r * np.array([np.cos(angle), np.sin(angle), 0]),
                         radius=0.075, color=PRIVATE))
        links = VGroup(*[
            Line(dots[i].get_center(), dots[(i + 2) % nodes].get_center(),
                 color=PRIVATE, stroke_width=1.8, stroke_opacity=0.55)
            for i in range(nodes)
        ])

        self.add(outline, meridians, parallels, links, dots)
        self.outline, self.dots, self.links = outline, dots, links
        self.shell = VGroup(outline, meridians, parallels)

    def spin_anim(self, run_time: float = 6.0, angle: float = TAU / 8):
        return Rotate(self.shell, angle, run_time=run_time, rate_func=linear)


# --- the extra flat icons this cut needs -----------------------------------


def tech_icon(kind: str, color: str = FG, height: float = 0.9) -> VGroup:
    """Icons the simplified cut never needed. Same flat geometric language.

    ``assets.icon`` is left exactly as the simplified video has it, so the two
    files stay interchangeable; anything new to this cut is here instead.
    Unknown kinds fall through to ``assets.icon`` so a caller can ask either
    library for any icon in the video.
    """
    g = VGroup()

    if kind == "usb":
        body = RoundedRectangle(
            width=0.75, height=1.25, corner_radius=0.1, color=color,
            stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        plug = Rectangle(
            width=0.42, height=0.4, color=color, stroke_width=STROKE_THIN,
            fill_color=SURFACE_HI, fill_opacity=1,
        ).next_to(body, UP, buff=0)
        notch = VGroup(*[
            Line(ORIGIN, RIGHT * 0.26, color=color, stroke_width=2.5)
            for _ in range(2)
        ]).arrange(DOWN, buff=0.1).move_to(plug)
        g.add(body, plug, notch)

    elif kind == "cloud":
        puff = Union(
            Circle(radius=0.36).shift(LEFT * 0.34),
            Circle(radius=0.46).shift(UP * 0.1),
            Circle(radius=0.34).shift(RIGHT * 0.42),
            Rectangle(width=1.5, height=0.5).shift(DOWN * 0.2),
            color=color, stroke_width=STROKE,
            fill_color=SURFACE, fill_opacity=1,
        )
        g.add(puff)

    elif kind == "chip":
        shell = RoundedRectangle(
            width=1.0, height=1.0, corner_radius=0.1, color=color,
            stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        core = Square(side_length=0.42, color=color, stroke_width=2.5)
        legs = VGroup()
        for side, d in ((UP, UP), (DOWN, DOWN), (LEFT, LEFT), (RIGHT, RIGHT)):
            for k in (-1, 0, 1):
                across = np.array([d[1], d[0], 0]) * k * 0.28
                legs.add(Line(
                    side * 0.5 + across, side * 0.72 + across,
                    color=color, stroke_width=2.8,
                ))
        g.add(legs, shell, core)

    elif kind == "vault":
        shell = RoundedRectangle(
            width=1.4, height=1.4, corner_radius=0.12, color=color,
            stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        dial = VGroup(
            Circle(radius=0.3, color=color, stroke_width=3.5),
            Circle(radius=0.1, color=color, stroke_width=0,
                   fill_color=color, fill_opacity=1),
        )
        spokes = VGroup(*[
            Line(ORIGIN, UP * 0.38, color=color, stroke_width=3).rotate(
                TAU * k / 4, about_point=ORIGIN)
            for k in range(4)
        ])
        g.add(shell, spokes, dial)

    elif kind == "sticky":
        pad = Square(side_length=1.1, color=PRIVATE, stroke_width=STROKE_THIN,
                     fill_color=PRIVATE, fill_opacity=0.22)
        fold = Polygon(
            pad.get_corner(DR), pad.get_corner(DR) + LEFT * 0.3,
            pad.get_corner(DR) + UP * 0.3, color=PRIVATE,
            stroke_width=STROKE_THIN, fill_color=BG, fill_opacity=1,
        )
        scrawl = VGroup(*[
            Line(ORIGIN, RIGHT * w, color=PRIVATE, stroke_width=2.6)
            for w in (0.62, 0.5, 0.4)
        ]).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(pad).shift(UP * 0.08)
        g.add(pad, fold, scrawl)

    elif kind == "dice":
        shell = RoundedRectangle(
            width=1.0, height=1.0, corner_radius=0.16, color=color,
            stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        pips = VGroup(*[
            Dot(radius=0.07, color=color).move_to(np.array([x, y, 0]) * 0.26)
            for x, y in ((-1, 1), (0, 0), (1, -1), (-1, -1), (1, 1))
        ])
        g.add(shell, pips)

    elif kind == "hook":
        # A J: the shank drops to the bend's start point, the bend sweeps a
        # half circle under it, and the barb kicks back up off its end.
        bend = Arc(radius=0.3, start_angle=0, angle=-PI,
                   arc_center=[-0.3, -0.12, 0], color=color,
                   stroke_width=STROKE)
        shank = Line(UP * 0.56, bend.get_start(), color=color,
                     stroke_width=STROKE)
        barb = Line(bend.get_end(), bend.get_end() + UP * 0.26 + RIGHT * 0.1,
                    color=color, stroke_width=STROKE_THIN)
        eye = Circle(radius=0.1, color=color, stroke_width=3)
        eye.move_to(shank.get_start() + UP * 0.08)
        g.add(eye, shank, bend, barb)

    elif kind == "call":
        head = Circle(radius=0.22, color=color, stroke_width=STROKE,
                      fill_color=BG, fill_opacity=1)
        torso = Arc(radius=0.42, start_angle=0, angle=PI,
                    color=color, stroke_width=STROKE)
        torso.next_to(head, DOWN, buff=0.04)
        handset = RoundedRectangle(
            width=0.22, height=0.62, corner_radius=0.09, color=PRIVATE,
            stroke_width=STROKE_THIN, fill_color=SURFACE, fill_opacity=1,
        ).next_to(head, RIGHT, buff=0.06)
        waves = VGroup(*[
            Arc(radius=r, start_angle=-PI / 5, angle=2 * PI / 5,
                color=PRIVATE, stroke_width=2.4, stroke_opacity=0.8)
            .move_to(handset.get_right() + RIGHT * r * 0.42)
            for r in (0.22, 0.36)
        ])
        g.add(torso, head, handset, waves)

    elif kind == "terminal":
        shell = RoundedRectangle(
            width=1.0, height=1.5, corner_radius=0.12, color=color,
            stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        screen = RoundedRectangle(
            width=0.74, height=0.5, corner_radius=0.06, color=color,
            stroke_width=0, fill_color=BG, fill_opacity=1,
        ).move_to(shell.get_top() + DOWN * 0.42)
        slot = Rectangle(width=0.6, height=0.08, color=color, stroke_width=0,
                         fill_color=color, fill_opacity=0.9)
        slot.move_to(shell.get_bottom() + UP * 0.3)
        keys = VGroup(*[
            Dot(radius=0.045, color=color) for _ in range(6)
        ]).arrange_in_grid(rows=2, cols=3, buff=0.13)
        keys.move_to(shell.get_center() + DOWN * 0.06)
        g.add(shell, screen, keys, slot)

    elif kind == "database":
        band = VGroup()
        for k in range(3):
            band.add(Ellipse(width=1.3, height=0.34, color=color,
                             stroke_width=STROKE_THIN,
                             fill_color=SURFACE, fill_opacity=1)
                     .shift(DOWN * k * 0.38))
        side = VGroup(
            Line(LEFT * 0.65, LEFT * 0.65 + DOWN * 0.76, color=color,
                 stroke_width=STROKE_THIN),
            Line(RIGHT * 0.65, RIGHT * 0.65 + DOWN * 0.76, color=color,
                 stroke_width=STROKE_THIN),
        )
        g.add(side, *reversed(band.submobjects))

    elif kind == "rug":
        rug = Polygon(
            [-0.9, -0.12, 0], [0.9, -0.12, 0], [0.75, 0.2, 0], [-0.75, 0.2, 0],
            color=color, stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        fringe = VGroup(*[
            Line(ORIGIN, DOWN * 0.1, color=color, stroke_width=2.2)
            for _ in range(9)
        ]).arrange(RIGHT, buff=0.12)
        fringe.set_width(rug.width * 0.9)
        fringe.next_to(rug, DOWN, buff=0)
        g.add(rug, fringe)

    else:
        return icon(kind, color=color, height=height)

    if kind == "rug":
        # A rug is wide and flat. Sizing it by height like the others would
        # blow it to three times the width of everything beside it.
        g.scale_to_fit_width(height * 2.4)
    else:
        g.scale_to_fit_height(height)
    return g


def channel(start, end, color: str = SNOOP) -> tuple[DashedLine, Line]:
    """An insecure channel: the dashes to look at, and a path to travel.

    ``DashedLine`` is a group of separate dashes with no points of its own, so
    ``MoveAlongPath`` cannot ride it. The second return value is the invisible
    straight line to animate along.
    """
    dashes = DashedLine(start, end, color=color, stroke_width=3,
                        dash_length=0.16)
    return dashes, Line(start, end).set_opacity(0)


def stamp_anim(mob: Mobject, color: str = PRIVATE, run_time: float = 0.5):
    """A padlock landing on something: grow, overshoot, flash."""
    return Succession(
        GrowFromCenter(mob, run_time=run_time * 0.6),
        Flash(mob, color=color, line_length=0.12, flash_radius=0.35,
              run_time=run_time * 0.4),
    )


def tag_below(mob: Mobject, text: str, color: str = FG,
              size: int = SMALL, buff: float = 0.25) -> Text:
    t = caption(text, color=color, size=size)
    t.next_to(mob, DOWN, buff=buff)
    return t
