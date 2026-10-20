"""The thirteen scenes of the professional encryption video.

Each class is one scene of professional-encryption-video-plan.md, and each
``with self.beat(seconds, "...")`` block is one row of that scene's beat
table: the narration spoken over that window, and what is on screen while it
is spoken. The block holds the last frame until the window is full, so the cut
stays on the plan's clock whatever the animations inside cost.

The beat lines are the group's script word for word, so ``narrate.py`` can
read them straight out of this file and match each one to its budget in the
plan. Changing a line here means changing it in the plan too, or the budgets
stop lining up.

**The intro is not here yet.** The plan budgets 0:30–2:00 before Scene 1 for
the history of encryption, and that script is still being written. Scene 1
opens on the history timeline the intro is to end on, already on screen, and
compresses it — so when ``Scene00Intro`` is written it hands straight over
with nothing else to change. Until then the cut starts at Scene 1 and runs
8:00. See the placeholder in render.sh.

Render one scene while iterating:

    .venv/bin/manim -ql --disable_caching --media_dir media scenes.py Scene02Pipeline

Render the whole video and stitch it:  ./render.sh
"""

from __future__ import annotations

from pathlib import Path

from manim import *

from assets import *
from style import *
from tech_assets import *
from values import (
    AES_B64, AES_HEX, LONG_INPUT, MSG, MSG_TAMPERED, PASSWORD, SALT,
    SHA_LONG, SHA_MSG, SHA_PASSWORD, SHA_SHORT, SHA_TAMPERED, diff_positions,
)

# The end card in Scene13Conclusion. Same credits as the simplified cut.
CREDITS_LOGO = Path(__file__).resolve().parent.parent / "team_logo.svg"
CREDITS_TEAM = (
    ("Michael Ansara", "Script Writer"),
    ("Eric Griffin", "Video Editor"),
    ("Kenneth Joyce", "Script Writer"),
    ("Chris Mobley", "Animator"),
    ("Derrick Patterson", "Narrator"),
)
CREDITS_CLASS = "CST 349"
CREDITS_TOOLS = "Animated with Manim Community Edition"


def team_logo(height: float = 1.15) -> VGroup:
    """The Otter Digital mark, on the white card its artwork needs.

    The logo is drawn navy on white, and that navy is near enough the
    video's own background to disappear into it, so the mark sits on a
    plate rather than straight on BG.

    It is the traced ``team_logo.svg`` rather than the ``team_logo.png`` it
    came from: an SVG stays crisp at 4K, and Manim's raster path is broken
    against current Pillow anyway. The root README says how it is traced.
    """
    mark = SVGMobject(CREDITS_LOGO).scale_to_fit_height(height)
    plate = RoundedRectangle(
        corner_radius=0.16, width=mark.width + 0.55, height=mark.height + 0.4,
        fill_color=WHITE, fill_opacity=1.0, stroke_width=0,
    ).move_to(mark)
    return VGroup(plate, mark)


def team_roster(size: int = SMALL) -> VGroup:
    """Who did what: names in one column, roles in the one beside it.

    Each column is one multi-line Text rather than a row of them, so the
    five rows share a single set of baselines however long the names and
    the roles run.
    """
    column = dict(font=SANS, font_size=size, weight=MEDIUM, line_spacing=0.6)
    names = Text("\n".join(n for n, _ in CREDITS_TEAM), color=FG, **column)
    roles = Text("\n".join(r for _, r in CREDITS_TEAM), color=SNOOP, **column)
    roles.next_to(names, RIGHT, buff=0.55).align_to(names, UP)
    return VGroup(names, roles)

# The three chapters, as the corner tag shows them.
CHAPTERS = (
    (1, "How Encryption Works"),
    (2, "Types of Encryption"),
    (3, "Applications"),
)


def tag_for(chapter: int, scene: Scene | None = None) -> ChapterTag:
    """The corner tag for a chapter, built the same way in every scene.

    Pass the scene when its camera moves, and the tag rides along in the
    corner instead of being dragged across the frame by the zoom.
    """
    number, title = CHAPTERS[chapter - 1]
    tag = ChapterTag(number, title)
    if scene is not None:
        tag.pin_to(scene.camera.frame)
    return tag


# --- Part 1: history and evolution -----------------------------------------
#
# Scenes A to F, lettered so that adding them in front of the cut left the
# existing scene numbers — and the audio already named after them — alone.
# Every window is the length of the line as it was actually read.
#
# The timeline is Part 1's spine. Each scene rebuilds it in the same place
# with the marker on the era it opens in, so it holds still across the cuts
# and only moves when the narration moves.


def _history(stop: int = 0) -> HistoryTimeline:
    """The timeline, parked at ``stop``, in the same spot every scene.

    The marker is placed after the scaling and the move, because ``at`` reads
    the tick where it is now.
    """
    line = HistoryTimeline(marker=True).scale(0.8)
    line.to_edge(DOWN, buff=0.5)
    line.marker.move_to(line.at(stop))
    return line


def _magnifier(color: str = SNOOP, radius: float = 0.34) -> VGroup:
    """A lens on a handle, for Eve studying something in the open."""
    lens = Circle(radius=radius, color=color, stroke_width=4,
                  fill_color=BG, fill_opacity=0.25)
    grip = Line(ORIGIN, RIGHT * radius * 1.25, color=color, stroke_width=5)
    grip.rotate(-PI / 4, about_point=ORIGIN)
    grip.shift(lens.get_center() + DR * radius * 0.72)
    return VGroup(lens, grip)


def _bar(width: float, color: str, height: float = 0.34) -> Rectangle:
    return Rectangle(width=width, height=height, color=color,
                     stroke_width=0, fill_color=color, fill_opacity=0.9)


# --- A. The algorithm isn't the secret -------------------------------------


class SceneAKerckhoffs(VideoScene):
    """The cipher can be public. Only the key cannot."""

    TARGET = 15.14

    def construct(self):
        with self.beat(2.0, "(music only)"):
            grid = VGroup(*[
                HexText(h, SNOOP, width=24, size=SMALL - 6).set_opacity(0.16)
                for h in (AES_HEX[:48], SHA_MSG[:48], AES_HEX[16:64])
            ]).arrange(DOWN, buff=0.9).move_to(ORIGIN)
            word = title("Encryption")
            self.play(FadeIn(grid, lag_ratio=0.3), run_time=0.7)
            self.play(Write(word), run_time=0.8)
            self.play(FadeOut(word, grid, shift=UP * 0.3), run_time=0.5)

        pipe = Pipeline(width=8.6).scale(0.92).move_to(UP * 0.7)

        with self.beat(4.94, "The security of an encrypted system should not "
                             "depend on keeping the algorithm secret."):
            self.play(FadeIn(pipe.body, lag_ratio=0.15), run_time=1.0)
            plain = pipe.fit(mono("Meet at 3pm", PLAIN, SMALL - 1), "in")
            self.play(FadeIn(plain, scale=0.7), run_time=0.5)
            # The box is glass: its workings are on show, and only the key
            # is held back.
            self.play(pipe.algo.shell.animate.set_fill(opacity=0.1),
                      run_time=0.6)
            open_tag = caption("public", ALGO, size=SMALL - 2)
            open_tag.next_to(pipe.algo, DOWN, buff=0.3)
            self.play(Write(open_tag), run_time=0.6)
            self.play(FadeIn(pipe.key, pipe.key_slot, shift=DOWN * 0.3),
                      run_time=0.5)
            secret_tag = caption("secret", PRIVATE, size=SMALL - 2)
            secret_tag.next_to(pipe.key, RIGHT, buff=0.25)
            self.play(Write(secret_tag),
                      Flash(pipe.key, color=PRIVATE, flash_radius=0.45),
                      run_time=0.7)
            cipher = pipe.fit(
                mono(scrambled("Meet at 3pm", seed=21), CIPHER, SMALL - 1), "out")
            self.play(TransformFromCopy(plain, cipher), pipe.algo.turn(TAU),
                      run_time=0.9)
            self.tags = VGroup(open_tag, secret_tag)
            self.plain, self.cipher = plain, cipher

        eve = Eve(height=1.55).move_to(DOWN * 2.2)

        with self.beat(3.31, "An attacker may capture the traffic and study "
                             "the cipher."):
            self.play(FadeIn(eve, shift=UP * 0.3), run_time=0.45)
            grab = self.cipher.copy()
            self.add(grab)
            self.play(grab.animate.scale(0.75).next_to(eve.figure, LEFT,
                                                       buff=0.35),
                      run_time=0.6)
            lens = _magnifier().move_to(pipe.algo.get_center() + DR * 0.3)
            self.play(FadeIn(lens, scale=0.6), run_time=0.4)
            self.play(lens.animate.shift(LEFT * 0.9 + UP * 0.2), run_time=0.5)
            self.eve_bits = VGroup(grab, lens)

        with self.beat(3.89, "Without the key, that knowledge should not be "
                            "enough to recover the data."):
            self.play(FadeOut(self.eve_bits[1], self.plain, self.cipher,
                              self.tags, shift=UP * 0.2), run_time=0.35)
            guess = Key(SNOOP, height=0.5).next_to(eve.figure, UP, buff=0.3)
            self.play(FadeOut(pipe.key, scale=0.5),
                      FadeIn(guess, scale=0.6), run_time=0.4)
            self.play(guess.animate.next_to(pipe.algo, UP, buff=0.12),
                      run_time=0.5)
            noise = pipe.fit(
                mono(scrambled("Meet at 3pm", seed=33), SNOOP, SMALL - 1), "out")
            self.play(self.eve_bits[0].animate.move_to(pipe.input_at()),
                      run_time=0.4)
            self.play(FadeOut(self.eve_bits[0]), FadeIn(noise),
                      pipe.algo.turn(TAU), run_time=0.6)
            no = cross_mark(CIPHER, height=0.44).next_to(noise, RIGHT, buff=0.3)
            self.play(GrowFromCenter(no), run_time=0.35)
            # Along the top: the foot of the frame belongs to Eve and her
            # name, and a caption there lands on top of it.
            law = heading("Kerckhoffs's principle, 1883", SNOOP, size=LABEL)
            law.to_edge(UP, buff=0.55)
            self.play(Write(law), run_time=0.5)
            self.closing = VGroup(pipe, guess, noise, no, law, eve)

        with self.beat(1.0, "(transition)"):
            line = _history(0)
            self.play(FadeOut(self.closing, shift=UP * 0.3), run_time=0.5)
            self.play(line.write_anim(run_time=0.5), run_time=0.5)

        self.pad_to_target()


# --- B. Caesar cipher -------------------------------------------------------


class SceneBCaesar(VideoScene):
    """A key space small enough to walk through by hand."""

    TARGET = 12.92

    def construct(self):
        line = _history(0)
        self.add(line)

        rows = AlphabetShift(k=3, width=10.8, size=19).move_to(UP * 2.1)
        plain = mono("MEET", PLAIN, 34).move_to(LEFT * 3.0 + UP * 0.35)
        cipher = VGroup()

        with self.beat(5.0, "Caesar's cipher is the simplest example: shift "
                            "each letter by a fixed amount."):
            self.play(FadeIn(rows.top, lag_ratio=0.02), run_time=0.45)
            self.play(FadeIn(rows.bottom, lag_ratio=0.02), run_time=0.4)
            self.add(rows)
            tag = caption("key = 3", PRIVATE, size=SMALL - 1)
            tag.move_to(UP * 3.1)
            self.play(rows.slide(run_time=0.7), FadeOut(rows.leaving()),
                      FadeIn(tag), run_time=0.7)
            self.play(Write(plain), run_time=0.5)
            for i, ch in enumerate("MEET"):
                letter = mono(rows.cipher(ch).text, PRIVATE, 34)
                letter.move_to(plain.get_right() + RIGHT * (0.95 + i * 0.6))
                cipher.add(letter)
            self.play(LaggedStart(*[
                TransformFromCopy(rows.cipher(ch), c)
                for ch, c in zip("MEET", cipher)
            ], lag_ratio=0.12), run_time=0.9)
            self.tag = tag

        with self.beat(3.75, "With so few possible offsets, an attacker can "
                             "test every one."):
            self.play(FadeOut(rows, self.tag, shift=UP * 0.3),
                      VGroup(plain, cipher).animate.move_to(UP * 2.3),
                      run_time=0.45)
            # Every shift of PHHW, in one column. Only one of them is English.
            tries = VGroup()
            for n in range(1, 14):
                guess = "".join(chr((ord(c) - 65 - n) % 26 + 65) for c in "PHHW")
                hit = guess == "MEET"
                row = VGroup(
                    caption(f"{n:2d}", SNOOP, size=SMALL - 4),
                    mono(guess, PLAIN if hit else SNOOP, SMALL - 1),
                ).arrange(RIGHT, buff=0.35)
                tries.add(row)
            tries.arrange(DOWN, buff=0.1).move_to(DOWN * 0.55)
            tries.scale(0.82)
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tries],
                                  lag_ratio=0.06), run_time=1.5)
            box = SurroundingRectangle(tries[2], color=PLAIN, buff=0.1,
                                       corner_radius=0.08, stroke_width=3)
            self.play(Create(box), run_time=0.5)
            self.tries = VGroup(tries, box)

        with self.beat(3.17, "The key space is too small to provide "
                             "meaningful security."):
            self.play(FadeOut(self.tries, plain, cipher, shift=UP * 0.3),
                      run_time=0.4)
            small = _bar(0.22, CIPHER)
            wide = _bar(12.4, PUBLIC)
            small.move_to(LEFT * 5.4 + UP * 1.3, aligned_edge=LEFT)
            wide.move_to(LEFT * 5.4 + UP * 0.2, aligned_edge=LEFT)
            l1 = caption("25 keys", CIPHER, size=SMALL - 2)
            l1.next_to(small, RIGHT, buff=0.3)
            l2 = caption("2¹²⁸ keys", PUBLIC, size=SMALL - 2)
            l2.next_to(wide, UP, buff=0.18).align_to(wide, LEFT)
            self.play(GrowFromEdge(small, LEFT), Write(l1), run_time=0.6)
            self.play(GrowFromEdge(wide, LEFT), Write(l2), run_time=0.9)
            self.bars = VGroup(small, wide, l1, l2)

        with self.beat(1.0, "(transition)"):
            self.play(FadeOut(self.bars, shift=UP * 0.3),
                      line.slide(1, run_time=0.8), run_time=0.8)

        self.pad_to_target()


# --- C. Enigma --------------------------------------------------------------


class SceneCEnigma(VideoScene):
    """Rotors that move, and the two things that broke them anyway."""

    TARGET = 14.23

    def construct(self):
        line = _history(1)
        self.add(line)

        mach = EnigmaRotors(numbered=True).scale(0.95).move_to(UP * 1.5)

        with self.beat(3.53, "Enigma changed substitutions as its rotors "
                             "advanced."):
            self.play(FadeIn(mach.wheels, lag_ratio=0.2), run_time=0.4)
            self.play(FadeIn(mach.lamps, lag_ratio=0.02),
                      FadeIn(mach.letters, lag_ratio=0.02), run_time=0.35)
            pressed = caption("A", PLAIN, 28).next_to(mach, LEFT, buff=0.6)
            self.play(FadeIn(pressed, scale=0.6), run_time=0.2)
            # The same key five times, a different lamp every time.
            for ch in "BDZGO":
                self.play(mach.step(run_time=0.17),
                          Indicate(pressed, color=PLAIN, scale_factor=1.15,
                                   run_time=0.17))
                self.play(mach.lit(ch), run_time=0.12)
                if ch != "O":
                    self.play(mach.dark(ch), run_time=0.09)
            out = caption("A A A A A  →  B D Z G O", PRIVATE, size=SMALL - 1)
            out.move_to(DOWN * 1.15)
            self.play(Write(out), run_time=0.35)
            self.pressed, self.out = pressed, out

        with self.beat(5.03, "Polish cryptanalysts made the first major "
                             "breakthroughs, and teams at Bletchley Park "
                             "built on them."):
            self.play(mach.dark("O"), FadeOut(self.pressed, self.out),
                      run_time=0.3)
            poles = labelled(Person(FG, 1.0), "Polish Cipher Bureau, 1932",
                             FG, SMALL - 3)
            bp = labelled(Person(FG, 1.0), "Bletchley Park", FG, SMALL - 3)
            # Between the lamp board above and the timeline below.
            poles.move_to(LEFT * 4.4 + DOWN * 1.1)
            bp.move_to(RIGHT * 4.4 + DOWN * 1.1)
            self.play(FadeIn(poles, shift=RIGHT * 0.3),
                      FadeIn(bp, shift=LEFT * 0.3), run_time=0.7)
            book = VGroup(
                RoundedRectangle(width=0.8, height=0.58, corner_radius=0.06,
                                 color=PRIVATE, stroke_width=STROKE_THIN,
                                 fill_color=SURFACE, fill_opacity=1),
                Line(UP * 0.29, DOWN * 0.29, color=PRIVATE, stroke_width=2),
            ).next_to(poles, UP, buff=0.25)
            tag = caption("rotor wiring", PRIVATE, size=SMALL - 4)
            tag.next_to(book, LEFT, buff=0.18)
            self.play(FadeIn(book, scale=0.6), FadeIn(tag),
                      Flash(book, color=PRIVATE, flash_radius=0.4),
                      run_time=0.7)
            hop = ArcBetweenPoints(book.get_center(),
                                   bp.get_top() + UP * 0.42, angle=-PI / 3)
            self.play(MoveAlongPath(book, hop), FadeOut(tag), run_time=1.1)
            self.groups = VGroup(poles, bp, book)

        with self.beat(4.67, "The work exploited both the machine's structure "
                             "and weaknesses in how it was used."):
            self.play(FadeOut(self.groups, shift=DOWN * 0.3), run_time=0.35)
            heads = VGroup(
                caption("STRUCTURE", PUBLIC, size=SMALL - 1).move_to(
                    LEFT * 3.4 + DOWN * 0.3),
                caption("USAGE", SNOOP, size=SMALL - 1).move_to(
                    RIGHT * 3.4 + DOWN * 0.3),
            )
            rule = DashedLine(DOWN * 0.6, DOWN * 2.0, color=SNOOP,
                              stroke_width=2, dash_length=0.1)
            self.play(FadeIn(heads), Create(rule), run_time=0.4)

            # Structure gets the animation: pressing A can light any lamp
            # except A, which is the flaw that made cribs testable.
            never = caption("A never lights A", PUBLIC, size=SMALL - 2)
            never.move_to(LEFT * 3.4 + DOWN * 1.15)
            self.play(Write(never), run_time=0.5)
            for ch in "QKM":
                self.play(mach.lit(ch), run_time=0.14)
                self.play(mach.dark(ch), run_time=0.1)
            struck = VGroup(
                mach.lamp("A").copy().set_stroke(CIPHER),
                Line(mach.lamp("A").get_corner(DL),
                     mach.lamp("A").get_corner(UR),
                     color=CIPHER, stroke_width=4),
            )
            self.play(FadeIn(struck), run_time=0.45)

            # Usage is stated rather than animated: one card, read in place.
            crib = VGroup(
                caption("predictable openings", FG, size=SMALL - 2),
                mono("WETTERBERICHT", CIPHER, SMALL - 1),
                caption("(weather report)", SNOOP, size=SMALL - 4),
            ).arrange(DOWN, buff=0.16)
            card = SurroundingRectangle(crib, color=SNOOP, buff=0.26,
                                        corner_radius=0.12, stroke_width=2.5)
            # Sized against the timeline below it: the card clears it by
            # a quarter unit rather than sitting on the AES label.
            usage = VGroup(card, crib).move_to(RIGHT * 3.4 + DOWN * 1.2)
            self.play(FadeIn(usage, shift=UP * 0.2), run_time=0.7)
            self.split = VGroup(heads, rule, never, struck, usage)

        with self.beat(1.0, "(transition)"):
            self.play(
                LaggedStart(*[Rotate(w, -TAU / 13, about_point=w.get_center())
                              for w in mach.wheels], lag_ratio=0.15),
                FadeOut(mach, self.split, shift=UP * 0.3),
                line.slide(2, run_time=0.8),
                run_time=1.0,
            )

        self.pad_to_target()


# --- D. The key-exchange problem -------------------------------------------


class SceneDKeyExchange(VideoScene):
    """Why a shared secret is hard to establish over an open network."""

    TARGET = 16.52

    def construct(self):
        line = _history(1)
        self.add(line)

        with self.beat(3.62, "As networks expanded, key exchange became its "
                             "own challenge."):
            self.play(line.slide(2, run_time=0.5))
            net = NetworkMap(cols=6, rows=3, spacing=1.5, seed=6)
            net.scale(0.82).move_to(UP * 0.9)
            self.play(Create(net.lines, lag_ratio=0.04),
                      FadeIn(net.dots, lag_ratio=0.04), run_time=1.2)
            self.net = net

        maya, sam, eve = cast(height=1.45)
        maya.move_to(LEFT * 5.2 + UP * 0.9)
        sam.move_to(RIGHT * 5.2 + UP * 0.9)
        eve.move_to(UP * 0.9)

        with self.beat(4.36, "How do two systems establish a shared secret "
                             "without first meeting on a trusted channel?"):
            self.play(net.animate.set_opacity(0.22), run_time=0.3)
            self.play(FadeIn(maya, shift=RIGHT * 0.3),
                      FadeIn(sam, shift=LEFT * 0.3), run_time=0.6)
            wire, _ = channel(maya.figure.get_right() + RIGHT * 0.3,
                              sam.figure.get_left() + LEFT * 0.3)
            self.play(Create(wire), run_time=0.6)
            self.play(FadeIn(eve, shift=UP * 0.3), run_time=0.5)
            ask = title("?", SNOOP, 54).move_to(UP * 2.4)
            self.play(FadeIn(ask, shift=DOWN * 0.2), run_time=0.5)
            self.wire, self.ask = wire, ask

        # The answer, drawn as the two halves that never cross the wire. The
        # same object returns in scene 9 as the HTTPS session key, so this is
        # where the viewer meets it.
        merge = SessionKeyMerge(height=0.62).move_to(UP * 0.9)

        with self.beat(3.4, "Diffie and Hellman's nineteen seventy-six work "
                            "offered an answer,"):
            self.play(FadeOut(self.ask, eve, shift=UP * 0.3), run_time=0.35)
            self.play(FadeIn(merge.left, shift=RIGHT * 0.5),
                      FadeIn(merge.right, shift=LEFT * 0.5), run_time=0.55)
            self.play(merge.merge_anim(run_time=0.7))
            shared = caption("shared secret — never sent", PRIVATE,
                             size=SMALL - 2)
            shared.next_to(merge.key, DOWN, buff=0.35)
            stamp = caption("Diffie–Hellman key exchange, 1976", SNOOP,
                            size=SMALL - 3).move_to(UP * 2.5)
            self.play(Write(shared), FadeIn(stamp), run_time=0.6)
            self.dh = VGroup(merge, shared, stamp)

        with self.beat(4.14, "but unauthenticated key exchange still leaves "
                             "room for an active attacker."):
            self.play(FadeOut(self.dh, shift=UP * 0.3), run_time=0.35)
            # Eve runs the exchange twice, once with each side, so each of
            # them shares a secret with her rather than with the other.
            eve2 = Eve(height=1.45).move_to(UP * 0.9)
            self.play(FadeIn(eve2, scale=0.8), run_time=0.4)
            left = SessionKeyMerge(height=0.44)
            left.move_to(midpoint(maya.get_center(), eve2.get_center()))
            right = SessionKeyMerge(height=0.44)
            right.move_to(midpoint(eve2.get_center(), sam.get_center()))
            self.play(FadeIn(left.left, left.right),
                      FadeIn(right.left, right.right), run_time=0.45)
            self.play(left.merge_anim(run_time=0.5),
                      right.merge_anim(run_time=0.5))
            box = SurroundingRectangle(eve2, color=CIPHER, buff=0.22,
                                       corner_radius=0.12, stroke_width=3)
            label = caption("man-in-the-middle", CIPHER, size=SMALL - 1)
            label.next_to(box, UP, buff=0.22)
            self.play(Create(box), Write(label), run_time=0.7)
            self.mitm = VGroup(eve2, left, right, label, box)

        with self.beat(1.0, "(transition)"):
            self.play(FadeOut(self.mitm, self.wire, maya, sam, self.net,
                              shift=UP * 0.3),
                      line.slide(3, run_time=0.8), run_time=0.8)

        self.pad_to_target()


# --- E. From DES to AES -----------------------------------------------------


class SceneEDesToAes(VideoScene):
    """One standard outgrown, and the competition that replaced it."""

    TARGET = 19.02

    def construct(self):
        line = _history(2)
        self.add(line)

        with self.beat(5.57, "The Data Encryption Standard, or DES, became a "
                             "U.S. federal standard in nineteen seventy-seven."):
            self.play(line.slide(3, run_time=0.5))
            card = SpecCard("DES", (
                "block cipher, 64-bit blocks",
                "56-bit effective key",
                "16 rounds",
            ), color=PUBLIC).scale(0.95).move_to(LEFT * 3.0 + UP * 0.9)
            self.play(card.flip_in(run_time=0.8))
            # The ring is sized from the words rather than guessed at, so
            # the longest line always clears it.
            seal_text = VGroup(
                caption("U.S. federal", PLAIN, size=SMALL - 4),
                caption("standard 1977", PLAIN, size=SMALL - 5),
            ).arrange(DOWN, buff=0.1)
            seal = VGroup(
                Circle(radius=seal_text.width / 2 + 0.34, color=PLAIN,
                       stroke_width=STROKE, fill_color=BG, fill_opacity=0.9),
                seal_text,
            ).move_to(RIGHT * 3.1 + UP * 0.9)
            self.play(GrowFromCenter(seal),
                      Flash(seal, color=PLAIN, flash_radius=0.75),
                      run_time=0.8)
            self.play(Rotate(seal, -0.1), run_time=0.3)
            self.des = VGroup(card, seal)

        with self.beat(5.54, "Its effective fifty-six-bit key ultimately "
                             "became too small to resist exhaustive search."):
            self.play(FadeOut(self.des, shift=UP * 0.3), run_time=0.4)
            head = caption("2⁵⁶ ≈ 7.2 × 10¹⁶ keys", PRIVATE, size=SMALL - 1)
            head.move_to(UP * 1.9)
            track = Rectangle(width=9.6, height=0.46, color=SNOOP,
                              stroke_width=2.5).move_to(UP * 0.95)
            fill = _bar(0.01, CIPHER, height=0.4)
            fill.move_to(track.get_left() + RIGHT * 0.005, aligned_edge=LEFT)
            self.play(Write(head), Create(track), run_time=0.6)
            self.add(fill)
            self.play(fill.animate.stretch_to_fit_width(9.5)
                      .move_to(track.get_left(), aligned_edge=LEFT),
                      run_time=1.6)
            done = caption("1998: the EFF's DES Cracker found a key in about "
                           "56 hours", SNOOP, size=SMALL - 3)
            done.move_to(UP * 0.1)
            self.play(Write(done), run_time=0.9)
            self.brute = VGroup(head, track, fill, done)

        with self.beat(7.91, "In two thousand and one, NIST standardized the "
                             "Advanced Encryption Standard, or AES, after a "
                             "public competition to select a stronger "
                             "successor."):
            self.play(FadeOut(self.brute, shift=UP * 0.3), run_time=0.4)
            self.play(line.slide(4, run_time=0.6))
            fifteen = caption("15 candidates", SNOOP, size=SMALL - 2)
            fifteen.move_to(LEFT * 4.4 + UP * 1.5)
            finalists = VGroup(*[
                caption(n, FG, size=SMALL - 3) for n in
                ("MARS", "RC6", "Rijndael", "Serpent", "Twofish")
            ]).arrange(DOWN, buff=0.26).move_to(LEFT * 0.6 + UP * 1.5)
            a1 = Arrow(fifteen.get_right() + RIGHT * 0.15,
                       finalists.get_left() + LEFT * 0.15, color=SNOOP,
                       buff=0, stroke_width=3.5,
                       max_tip_length_to_length_ratio=0.18)
            self.play(FadeIn(fifteen, shift=RIGHT * 0.2), run_time=0.5)
            self.play(GrowArrow(a1), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.15)
                                    for f in finalists],
                                  lag_ratio=0.18), run_time=1.1)
            five = caption("5 finalists", SNOOP, size=SMALL - 3)
            five.next_to(finalists, UP, buff=0.3)
            self.play(FadeIn(five), run_time=0.4)
            # Rijndael is the one that becomes the standard.
            pick = finalists[2]
            self.play(
                *[f.animate.set_opacity(0.25) for i, f in enumerate(finalists)
                  if i != 2],
                pick.animate.set_color(PRIVATE), run_time=0.6,
            )
            card = SpecCard("AES", (
                "Rijndael, selected 2001",
                "128-bit blocks",
                "128, 192 or 256-bit keys",
            ), color=PRIVATE).scale(0.92).move_to(RIGHT * 4.0 + UP * 1.4)
            a2 = Arrow(finalists.get_right() + RIGHT * 0.15,
                       card.get_left() + LEFT * 0.15, color=PRIVATE,
                       buff=0, stroke_width=3.5,
                       max_tip_length_to_length_ratio=0.18)
            self.play(GrowArrow(a2), run_time=0.4)
            self.play(card.flip_in(run_time=0.8))
            stamp = caption("NIST FIPS 197, 2001", PLAIN, size=SMALL - 3)
            stamp.next_to(card, DOWN, buff=0.3)
            self.play(Write(stamp), run_time=0.7)
            self.aes_card = card
            self.bracket = VGroup(fifteen, finalists, five, a1, a2, stamp)

        self.pad_to_target()


# --- F. Beyond the cipher ---------------------------------------------------


class SceneFBeyond(VideoScene):
    """The cipher is one part of a system that has to hold up as a whole."""

    TARGET = 9.75

    def construct(self):
        line = _history(4)
        self.add(line)
        card = SpecCard("AES", (
            "Rijndael, selected 2001",
            "128-bit blocks",
            "128, 192 or 256-bit keys",
        ), color=PRIVATE).scale(0.92).move_to(RIGHT * 4.0 + UP * 1.4)
        self.add(card)

        pillars = VGroup(
            Pillar("key establishment", PUBLIC),
            Pillar("authentication", PLAIN),
            Pillar("implementation", ALGO),
        ).arrange(RIGHT, buff=0.95).move_to(DOWN * 0.75)

        with self.beat(3.69, "Today, evaluating encryption means looking at "
                            "more than the cipher:"):
            core = card.copy()
            self.play(FadeOut(card), run_time=0.01)
            self.add(core)
            self.play(core.animate.scale(0.42).move_to(UP * 2.3),
                      FadeOut(line, shift=DOWN * 0.3), run_time=0.9)
            self.play(LaggedStart(*[Create(p.shell) for p in pillars],
                                  lag_ratio=0.2), run_time=0.9)
            self.play(LaggedStart(*[FadeIn(p.label, shift=UP * 0.15)
                                    for p in pillars],
                                  lag_ratio=0.2), run_time=0.7)
            self.core = core

        with self.beat(5.06, "how keys are established, how endpoints are "
                             "authenticated, and how the system is "
                             "implemented."):
            # One pillar fills per phrase, so each lands on its own words.
            for pillar in pillars:
                self.play(pillar.fill_anim(1.0, run_time=0.65))
                self.wait(0.42)

        with self.beat(1.0, "(transition)"):
            # Hand the frame to Scene 1, which opens on the finished timeline.
            full = HistoryTimeline().scale(0.95).move_to(UP * 0.2)
            self.play(FadeOut(pillars, self.core, shift=UP * 0.3),
                      run_time=0.5)
            self.play(FadeIn(full), run_time=0.5)

        self.pad_to_target()


# --- 1. Bridge from the intro (0:00-0:14) ----------------------------------


class Scene01Bridge(VideoScene):
    """The handover from the history intro into the body of the video."""

    TARGET = 10.27

    def construct(self):
        # Already on screen when the scene opens: this is the frame the intro
        # is to end on, so the cut joins without a visible seam.
        timeline = HistoryTimeline().scale(0.95).move_to(UP * 0.2)
        self.add(timeline)

        with self.beat(2.73, "Now that we looked at the history of "
                            "encryption,"):
            # Hold the intro's last frame for a moment: the line is about
            # what we just watched, so it should still be there as it lands.
            self.wait(0.3)
            self.play(timeline.compress_anim(run_time=1.9))
            self.remove(timeline)

        cards = VGroup(
            chapter_card(1, "How it works"),
            chapter_card(2, "Types"),
            chapter_card(3, "Applications"),
        )
        for card in cards:
            card.scale(0.62)
        cards.arrange(RIGHT, buff=1.0).move_to(ORIGIN)

        with self.beat(6.54, "we can examine how encryption works, the major "
                            "types of encryption, and how encryption is used "
                            "in modern technology."):
            # One card per phrase, so each lands on the words that name it.
            for card in cards:
                self.play(FadeIn(card, shift=UP * 0.4), run_time=0.8)
                self.wait(1.1)

        with self.beat(1.0, "(transition)"):
            tag = tag_for(1)
            self.play(
                cards[1].animate.set_opacity(0.25),
                cards[2].animate.set_opacity(0.25),
                ReplacementTransform(cards[0], tag),
                run_time=1.0,
            )
            self.remove(cards)
            self.add(tag)

        self.pad_to_target()


# --- 2. Plaintext and ciphertext (0:14-0:48) -------------------------------


class Scene02Pipeline(VideoScene):
    """plaintext → algorithm + key → real AES-256-GCM ciphertext."""

    TARGET = 29.73

    def construct(self):
        self.add(tag_for(1))

        green = mono(MSG, PLAIN, size=HEAD).move_to(LEFT * 3.5 + UP * 1.3)
        arrow = Arrow(LEFT * 1.2, RIGHT * 1.2, color=FG, buff=0, stroke_width=7)
        arrow.move_to(UP * 1.3)
        red = mono(scrambled(MSG, seed=3), CIPHER, size=HEAD)
        red.move_to(RIGHT * 3.5 + UP * 1.3)

        with self.beat(9.24, "At its most basic level, encryption is the "
                             "process of transforming readable information "
                             "into an unreadable format so that unauthorized "
                             "people cannot understand it."):
            self.play(Write(green), run_time=1.6)
            self.play(GrowArrow(arrow), run_time=0.7)
            self.play(TransformFromCopy(green, red), run_time=1.5)
            scramble(self, red, steps=6, run_time=0.1)

            observer = Snooper(height=1.8).move_to(RIGHT * 3.4 + DOWN * 1.5)
            question = Text("?", font_size=52, color=SNOOP)
            question.next_to(observer, UP, buff=0.18).shift(RIGHT * 0.4)
            self.play(FadeIn(observer, shift=UP * 0.4), run_time=0.9)
            self.play(
                FadeIn(question, scale=0.5),
                Rotate(observer, 0.22, about_point=observer.get_bottom(),
                       rate_func=there_and_back),
                run_time=1.1,
            )
            self.lead_in = VGroup(green, arrow, red, observer, question)

        plabel = caption("PLAINTEXT", PLAIN).next_to(green, DOWN, buff=0.4)
        with self.beat(3.45, "The original readable information is called "
                            "plaintext."):
            self.play(Indicate(green, scale_factor=1.14, color=PLAIN),
                      run_time=1.0)
            self.play(Write(plabel), run_time=0.9)

        pipe = Pipeline().scale(0.82).move_to(DOWN * 0.45)
        key_label = caption("KEY", PRIVATE, size=SMALL)
        key_label.next_to(pipe.key, RIGHT, buff=0.25)

        with self.beat(5.69, "Encryption uses a mathematical algorithm and a "
                            "key to transform the plaintext into ciphertext."):
            self.play(
                FadeOut(self.lead_in, plabel, shift=UP * 0.6),
                run_time=0.6,
            )
            self.play(
                FadeIn(pipe.in_slot), GrowArrow(pipe.arrow_in),
                Create(pipe.algo.shell), run_time=0.7,
            )
            self.play(
                FadeIn(pipe.algo.gears), Write(pipe.algo.label),
                GrowArrow(pipe.arrow_out), FadeIn(pipe.out_slot), run_time=0.8,
            )
            in_text = pipe.fit(caption("PLAINTEXT", PLAIN, size=SMALL), "in")
            out_text = pipe.fit(
                caption("CIPHERTEXT", CIPHER, size=SMALL), "out")
            self.play(FadeIn(in_text), FadeIn(out_text), run_time=0.5)
            self.play(FadeIn(pipe.key, shift=DOWN * 0.3), FadeIn(key_label),
                      Create(pipe.key_slot), run_time=0.7)
            self.play(
                pipe.insert_key_anim(run_time=0.6),
                key_label.animate.shift(DOWN * 0.38),
            )
            self.play(pipe.algo.turn(TAU, run_time=1.0))
            self.pipe_text = VGroup(in_text, out_text)

        # Big enough to actually read: this is the only place in the video a
        # viewer sees what ciphertext really looks like.
        hex_out = HexText(AES_HEX, CIPHER, width=27, size=BODY - 2)
        hex_out.move_to(DOWN * 2.45)
        hex_tag = caption("AES-256-GCM", CIPHER, size=SMALL - 2)
        hex_tag.next_to(hex_out, UP, buff=0.25)

        with self.beat(4.44, "Ciphertext may look like a random sequence of "
                            "letters, numbers, or symbols."):
            self.play(FadeIn(hex_tag), run_time=0.3)
            self.play(hex_out.type_anim(per_char=0.022))
            # The same bytes, written another way: the encoding is a
            # presentation choice, the ciphertext underneath has not moved.
            b64 = Text(AES_B64, font=MONO, font_size=BODY - 2, color=CIPHER)
            b64.move_to(hex_out)
            b64_tag = caption("the same bytes, as Base64", SNOOP, size=SMALL - 2)
            b64_tag.move_to(hex_tag)
            self.play(ReplacementTransform(hex_out, b64),
                      ReplacementTransform(hex_tag, b64_tag), run_time=0.9)
            self.cipher_out, self.cipher_tag = b64, b64_tag

        with self.beat(6.91, "Although the ciphertext still contains the "
                             "original information, it is designed to be "
                             "meaningless to anyone who does not have the "
                             "correct key."):
            self.play(FadeOut(self.cipher_out, self.cipher_tag,
                              self.pipe_text[1]), run_time=0.5)
            wrong = Key(SNOOP, height=0.5).move_to(pipe.key)
            self.play(
                FadeOut(pipe.key, key_label, shift=UP * 0.3),
                FadeIn(wrong, shift=DOWN * 0.3), run_time=0.8,
            )
            noise = pipe.fit(
                mono(scrambled(MSG, seed=11), SNOOP, size=SMALL - 1), "out")
            self.play(
                pipe.algo.turn(-TAU, run_time=1.4),
                FadeIn(noise, run_time=1.4),
            )
            for seed in (21, 31, 41):
                self.play(Transform(noise, pipe.fit(
                    mono(scrambled(MSG, seed=seed), SNOOP, size=SMALL - 1),
                    "out")), run_time=0.2)
            no = cross_mark(CIPHER, height=0.7).move_to(pipe.output_at())
            self.play(FadeOut(noise), GrowFromCenter(no), run_time=0.6)
            note = caption("same information, unreadable without the key",
                           SNOOP, size=SMALL - 2)
            note.move_to(DOWN * 2.6)
            self.play(Write(note), run_time=1.2)

        self.pad_to_target()


# --- 3. Decryption (0:48-0:59) ---------------------------------------------


class Scene03Decryption(VideoScene):
    """The pipeline run backwards, closing the loop."""

    TARGET = 9.91

    def construct(self):
        self.add(tag_for(1))

        pipe = Pipeline().scale(0.82).move_to(UP * 0.5)
        pipe.algo.set_label("ENCRYPT")
        cipher_in = pipe.fit(caption("CIPHERTEXT", CIPHER, size=SMALL), "out")
        plain_in = pipe.fit(caption("PLAINTEXT", PLAIN, size=SMALL), "in")
        self.add(pipe.body, plain_in, cipher_in)

        sam = Person(FG, height=1.5, name="Sam")
        sam.move_to(RIGHT * 5.3 + DOWN * 1.9)

        with self.beat(6.6, "The intended recipient can then use a key and a "
                            "decryption algorithm to turn the ciphertext "
                            "back into plaintext."):
            self.play(FadeIn(sam, shift=LEFT * 0.4), run_time=0.7)

            # The return leg, drawn under the forward one: same two slots,
            # same box, the arrows the other way round.
            back = AlgoBox("DECRYPT").scale(0.82)
            back.move_to(pipe.algo.get_center() + DOWN * 2.4)
            a_back_in = Arrow(
                pipe.out_slot.get_bottom(), back.get_right(), buff=0.18,
                color=FG, stroke_width=6, max_tip_length_to_length_ratio=0.2,
                path_arc=-1.1,
            )
            a_back_out = Arrow(
                back.get_left(), pipe.in_slot.get_bottom(), buff=0.18,
                color=FG, stroke_width=6, max_tip_length_to_length_ratio=0.2,
                path_arc=-1.1,
            )
            self.play(Create(back), run_time=0.6)

            gold = Key(PRIVATE, height=0.45)
            gold.next_to(back, DOWN, buff=0.3)
            self.play(FadeIn(gold, shift=LEFT * 0.5), run_time=0.5)
            self.play(gold.animate.next_to(back, DOWN, buff=0.08), run_time=0.4)

            self.play(GrowArrow(a_back_in), run_time=0.6)
            payload = pipe.fit(
                mono(scrambled(MSG, seed=5), CIPHER, size=LABEL), "out")
            self.play(
                MoveAlongPath(payload, a_back_in.copy().reverse_direction()),
                run_time=0.9,
            )
            self.play(
                back.turn(TAU, run_time=1.0),
                Transform(payload, mono(MSG, PLAIN, size=LABEL)
                          .move_to(back.get_center())),
            )
            self.play(GrowArrow(a_back_out), run_time=0.5)
            self.play(MoveAlongPath(payload, a_back_out), run_time=0.9)
            self.play(FadeOut(payload, scale=1.3), run_time=0.3)
            self.loop = VGroup(back, a_back_in, a_back_out, gold)

        with self.beat(2.31, "This process is called decryption."):
            enc = caption("ENCRYPTION", ALGO, size=SMALL)
            enc.next_to(pipe.algo, UP, buff=0.75)
            dec = caption("DECRYPTION", ALGO, size=SMALL)
            dec.next_to(self.loop[0], DOWN, buff=0.55)
            self.play(Write(enc), Write(dec), run_time=1.1)
            self.labels = VGroup(enc, dec)

        with self.beat(1.0, "(transition)"):
            box = Box(FG, width=2.2, height=1.5).move_to(ORIGIN)
            whole = VGroup(pipe.body, plain_in, cipher_in, self.loop,
                           self.labels, sam)
            self.play(
                FadeOut(whole, scale=0.3),
                FadeIn(box, scale=0.6),
                run_time=1.0,
            )

        self.pad_to_target()


# --- 4. Locked-box analogy (0:59-1:25) -------------------------------------


class Scene04LockedBox(MovingVideoScene):
    """The analogy, and then the camera into the keyhole."""

    TARGET = 19.3

    def construct(self):
        self.add(tag_for(1, self))

        box = Box(FG, width=2.6, height=1.8).move_to(ORIGIN)
        with self.beat(2.66, "A simple analogy is a locked box."):
            self.add(box)
            self.play(box.open_anim(run_time=1.0))
            self.wait(0.4)

        note = Note(MSG, PLAIN, size=LABEL).scale(0.62)
        note.move_to(box.get_top() + UP * 1.6)
        with self.beat(3.7, "The plaintext is the message placed inside the "
                            "box."):
            self.play(FadeIn(note, shift=DOWN * 0.3), run_time=0.7)
            self.play(note.animate.move_to(box.inside()), run_time=0.9)
            link = DashedLine(
                note.get_left() + LEFT * 0.1, LEFT * 3.4,
                color=PLAIN, stroke_width=2.6, dash_length=0.1,
            )
            tag = caption("plaintext", PLAIN, size=SMALL)
            tag.next_to(link, LEFT, buff=0.18)
            self.play(Create(link), FadeIn(tag), run_time=0.9)
            self.plain_tag = VGroup(link, tag)

        lock = Padlock(PRIVATE, height=0.8)
        with self.beat(3.41, "The encryption algorithm is the locking "
                            "mechanism,"):
            self.play(FadeOut(self.plain_tag, shift=LEFT * 0.3), run_time=0.3)
            self.play(box.close_anim(run_time=0.6))
            lock.move_to(box.body.get_right() + LEFT * 0.42)
            self.play(stamp_anim(lock, run_time=0.7))
            link = DashedLine(
                lock.get_right() + RIGHT * 0.1, RIGHT * 3.2,
                color=PRIVATE, stroke_width=2.6, dash_length=0.1,
            )
            tag = caption("algorithm", PRIVATE, size=SMALL)
            tag.next_to(link, RIGHT, buff=0.18)
            self.play(Create(link), FadeIn(tag), run_time=0.7)
            self.algo_tag = VGroup(link, tag)

        key = Key(PRIVATE, height=0.6)
        with self.beat(2.95, "and the key is what allows the box to be "
                            "opened."):
            self.play(FadeOut(self.algo_tag, shift=RIGHT * 0.3), run_time=0.3)
            key.next_to(box, LEFT, buff=1.0)
            self.play(FadeIn(key, shift=RIGHT * 0.5), run_time=0.8)
            tag = caption("key", PRIVATE, size=SMALL)
            tag.next_to(key, DOWN, buff=0.25)
            self.play(Write(tag), run_time=0.6)
            self.play(Indicate(VGroup(key, tag), scale_factor=1.15,
                               color=PRIVATE), run_time=0.9)
            self.key_tag = tag

        with self.beat(5.58, "Anyone can see the locked box, but only "
                             "someone with the correct key should be able "
                             "to access the message."):
            parcel = VGroup(box, lock, note)
            self.play(
                FadeOut(self.key_tag),
                parcel.animate.scale(0.42).move_to(LEFT * 5.2 + UP * 1.4),
                key.animate.scale(0.75).move_to(RIGHT * 5.0 + DOWN * 2.2),
                run_time=0.5,
            )

            net = NetworkMap(cols=5, rows=3, spacing=1.5, seed=4)
            net.scale(0.86).move_to(UP * 0.3)
            self.play(Create(net.lines, lag_ratio=0.05),
                      FadeIn(net.dots, lag_ratio=0.05), run_time=0.6)

            watchers = VGroup(*[
                Snooper(height=0.85).move_to(net.at(i, j) + DOWN * 0.55)
                for i, j in ((1, 2), (2, 0), (3, 2))
            ])
            self.play(LaggedStart(*[FadeIn(w, shift=UP * 0.2) for w in watchers],
                                  lag_ratio=0.3), run_time=0.45)

            sam = Person(FG, height=1.3, name="Sam")
            sam.move_to(RIGHT * 5.2 + UP * 0.4)
            self.play(FadeIn(sam, shift=LEFT * 0.3), run_time=0.25)

            path = net.path([(0, 1), (1, 2), (2, 1), (3, 2), (4, 1)])
            self.play(
                MoveAlongPath(parcel, path, run_time=1.1),
                LaggedStart(*[
                    Rotate(w, 0.3, about_point=w.get_bottom(),
                           rate_func=there_and_back)
                    for w in watchers
                ], lag_ratio=0.5, run_time=1.1),
            )
            self.play(parcel.animate.next_to(sam, LEFT, buff=0.5),
                      net.animate.set_opacity(0.25), run_time=0.35)

            key.generate_target()
            key.target.scale(0.55).next_to(lock, RIGHT, buff=0.1)
            self.play(MoveToTarget(key), run_time=0.35)
            self.play(Rotate(key, PI / 2, about_point=key.get_left()),
                      run_time=0.3)
            self.play(lock.unlock_anim(), run_time=0.25)
            self.play(box.open_anim(run_time=0.3))
            self.play(note.animate.move_to(box.get_top() + UP * 0.45)
                      .set_color(PLAIN),
                      Flash(note, color=PLAIN, line_length=0.14,
                            flash_radius=0.4),
                      run_time=0.45)
            self.scene_bits = VGroup(net, watchers, sam, parcel, key)

        with self.beat(1.0, "(transition)"):
            self.play(
                self.camera.frame.animate.scale(0.18)
                .move_to(lock.keyhole.get_center()),
                FadeOut(note, self.scene_bits - lock, run_time=0.5),
                run_time=1.0,
            )

        self.pad_to_target()


# --- 5. Mathematics, not hiding (1:25-1:41) --------------------------------


class Scene05Math(MovingVideoScene):
    """Security by obscurity against security by arithmetic."""

    TARGET = 14.21

    def construct(self):
        # Scene 4 left the camera inside the keyhole; pull back out of it.
        self.camera.frame.scale(0.18)
        self.add(tag_for(1, self))

        divider = DashedLine(UP * 3.2, DOWN * 3.2, color=SNOOP,
                             stroke_width=2, dash_length=0.12)

        # Left: hiding. A note under a rug, and a hand that just lifts it.
        rug = tech_icon("rug", SNOOP, height=0.9).move_to(LEFT * 3.6 + DOWN * 0.4)
        hidden = Note("Meet at 3pm", PLAIN, size=SMALL).scale(0.5)
        hidden.move_to(rug.get_center() + DOWN * 0.1)
        hide_head = heading("hiding", SNOOP, size=LABEL)
        hide_head.move_to(LEFT * 3.6 + UP * 2.2)

        # Right: mathematics. Bits through a transform that is not reversible
        # by looking at it.
        math_head = heading("mathematics", ALGO, size=LABEL)
        math_head.move_to(RIGHT * 3.6 + UP * 2.2)
        bits = Text("01001101", font=MONO, font_size=SMALL, color=PLAIN)
        bits.move_to(RIGHT * 1.8 + DOWN * 0.4)
        transform_box = AlgoBox("AES", width=1.7, height=1.0, gears=False)
        transform_box.move_to(RIGHT * 3.7 + DOWN * 0.4)
        out_bits = Text("11010010", font=MONO, font_size=SMALL, color=CIPHER)
        out_bits.move_to(RIGHT * 5.6 + DOWN * 0.4)

        with self.beat(4.5, "Modern encryption is based on mathematics rather "
                            "than simply hiding information."):
            self.play(self.camera.frame.animate.scale(1 / 0.18).move_to(ORIGIN),
                      run_time=0.7)
            self.play(Create(divider), FadeIn(hide_head), FadeIn(math_head),
                      run_time=0.5)
            self.play(FadeIn(hidden), FadeIn(rug, shift=UP * 0.2), run_time=0.4)

            hand = GrabHand(SNOOP, height=1.0)
            hand.move_to(rug.get_right() + RIGHT * 0.5 + DOWN * 0.6)
            self.play(FadeIn(hand, shift=UP * 0.4), run_time=0.3)
            self.play(
                rug.animate.shift(UP * 0.5).rotate(-0.25),
                hand.animate.shift(UP * 0.5),
                run_time=0.4,
            )
            no = cross_mark(CIPHER, height=0.45)
            no.next_to(hidden, UP, buff=0.3)
            self.play(GrowFromCenter(no), run_time=0.3)

            self.play(FadeIn(bits), Create(transform_box), run_time=0.4)
            self.play(TransformFromCopy(bits, out_bits), run_time=0.5)
            yes = check_mark(PLAIN, height=0.45)
            yes.next_to(transform_box, UP, buff=0.3)
            self.play(GrowFromCenter(yes), run_time=0.3)

            note = caption("The algorithm can be public; only the key is "
                           "secret.", FG, size=SMALL - 2)
            note.to_edge(DOWN, buff=0.4)
            self.play(Write(note), run_time=0.7)
            self.left = VGroup(hide_head, rug, hidden, hand, no)
            self.right = VGroup(math_head, bits, transform_box, out_bits, yes)
            self.footer = note

        with self.beat(4.98, "Algorithms are designed so that encrypting "
                            "information is easy when the correct key is "
                            "available,"):
            self.play(FadeOut(self.left, self.right, divider, self.footer,
                              shift=UP * 0.4), run_time=0.6)
            pipe = Pipeline("AES-256").scale(0.75).move_to(UP * 0.4)
            plain = pipe.fit(mono(MSG, PLAIN, size=LABEL), "in")
            self.play(FadeIn(pipe.body), FadeIn(plain),
                      FadeIn(pipe.key, pipe.key_slot), run_time=0.8)
            self.play(pipe.insert_key_anim(run_time=0.4))
            # One quick flash: with the key, this costs nothing.
            self.play(
                pipe.flow_anim(plain, run_time=0.7),
                Flash(pipe.algo, color=PRIVATE, line_length=0.2,
                      flash_radius=1.0, run_time=0.7),
            )
            self.play(
                Transform(plain, pipe.fit(
                    mono(scrambled(MSG, seed=7), CIPHER, size=LABEL), "out")),
                run_time=0.4,
            )
            ok = check_mark(PLAIN, height=0.5).next_to(pipe.out_slot, RIGHT,
                                                       buff=0.4)
            self.play(GrowFromCenter(ok), run_time=0.4)
            fast = caption("microseconds, with the key", PLAIN, size=SMALL - 2)
            fast.next_to(pipe, DOWN, buff=0.5)
            self.play(Write(fast), run_time=0.7)
            self.easy = VGroup(pipe.body, pipe.key, pipe.key_slot, plain, ok, fast)

        counter = KeyspaceCounter().scale(0.85).move_to(DOWN * 0.3)
        with self.beat(3.73, "but reversing the process without the key is "
                            "computationally impractical."):
            self.play(FadeOut(self.easy, shift=UP * 0.5), run_time=0.4)
            self.play(FadeIn(counter), run_time=0.5)
            # A billion keys a second for three seconds: still nowhere.
            self.play(counter.count_to_anim(3.2e9, run_time=2.6))
            counter.freeze()

        with self.beat(1.0, "(transition)"):
            # Scene 6 grows its own three pillars, so previewing one here
            # only flashed something up and took it away again.
            self.play(
                counter.animate.scale(0.2).move_to(DOWN * 0.6).set_opacity(0),
                run_time=1.0,
            )
            self.remove(counter)

        self.pad_to_target()


# --- 6. What makes encryption strong (1:41-2:22) ---------------------------


class Scene06Strength(VideoScene):
    """Three pillars, three ways a key is lost, and the lifecycle ring."""

    TARGET = 31.7

    def construct(self):
        tag = tag_for(1)
        self.add(tag)

        pillars = VGroup(
            Pillar("Algorithm quality", PUBLIC),
            Pillar("Key length and randomness", PRIVATE),
            Pillar("Key storage", PLAIN),
        ).arrange(RIGHT, buff=0.8).scale(0.86).move_to(UP * 0.25)

        with self.beat(3.03, "The strength of encryption depends on several "
                            "factors."):
            self.play(LaggedStart(*[
                GrowFromEdge(p.shell, DOWN) for p in pillars
            ], lag_ratio=0.3), run_time=1.4)
            self.play(LaggedStart(*[
                FadeIn(p.label, shift=UP * 0.2) for p in pillars
            ], lag_ratio=0.3), run_time=0.9)

        with self.beat(2.46, "These include the quality of the algorithm,"):
            # Name cards, not spec cards: at the size that fits inside a
            # pillar, bullet lines are a grey smudge.
            def name_card(text, color):
                label = caption(text, color=color, size=SMALL - 4)
                shell = RoundedRectangle(
                    width=1.45, height=0.6, corner_radius=0.1, color=color,
                    stroke_width=STROKE_THIN, fill_color=SURFACE,
                    fill_opacity=1,
                ).move_to(label)
                return VGroup(shell, label)

            good = name_card("AES", PLAIN)
            good.move_to(pillars[0].body_at() + UP * 0.5)
            bad = name_card("DIY cipher", CIPHER)
            bad.move_to(pillars[0].body_at() + DOWN * 0.6)
            self.play(pillars[0].fill_anim(1.0, run_time=0.6),
                      FadeIn(good, scale=0.8), run_time=0.7)
            self.play(FadeIn(bad, scale=0.8), run_time=0.4)
            crack = Line(bad.get_corner(UL) + RIGHT * 0.25,
                         bad.get_corner(DR) + LEFT * 0.25,
                         color=CIPHER, stroke_width=4)
            self.play(Create(crack), bad.animate.set_opacity(0.4), run_time=0.6)
            self.col1 = VGroup(good, bad, crack)

        with self.beat(2.26, "the length and randomness of the key,"):
            bar = Rectangle(width=0.3, height=0.2, color=PRIVATE,
                            stroke_width=0, fill_color=PRIVATE, fill_opacity=0.8)
            bar.move_to(pillars[1].body_at() + UP * 0.55)
            bar.align_to(pillars[1].shell, LEFT).shift(RIGHT * 0.2)
            size_label = caption("56-bit", PRIVATE, size=SMALL - 4)
            size_label.next_to(bar, UP, buff=0.14)
            self.play(pillars[1].fill_anim(1.0, run_time=0.5),
                      FadeIn(bar), FadeIn(size_label), run_time=0.6)
            for width, text in ((0.75, "128-bit"), (1.45, "256-bit")):
                new_bar = bar.copy().stretch_to_fit_width(width)
                new_bar.align_to(bar, LEFT)
                new_label = caption(text, PRIVATE, size=SMALL - 4)
                new_label.next_to(new_bar, UP, buff=0.14)
                self.play(Transform(bar, new_bar),
                          Transform(size_label, new_label), run_time=0.45)
            strong = Text("9f2a·c7e1", font=MONO, font_size=SMALL - 5,
                          color=PLAIN)
            weak = Text("password123", font=MONO, font_size=SMALL - 5,
                        color=CIPHER)
            pair = VGroup(strong, weak).arrange(DOWN, buff=0.18)
            pair.move_to(pillars[1].body_at() + DOWN * 0.72)
            self.play(FadeIn(pair, shift=UP * 0.15), run_time=0.5)
            self.col2 = VGroup(bar, size_label, pair)

        with self.beat(2.33, "and how securely the key is stored."):
            vault = tech_icon("vault", PLAIN, height=0.75)
            vault_key = Key(PRIVATE, height=0.26).move_to(vault.get_center())
            safe = VGroup(vault, vault_key)
            safe.move_to(pillars[2].body_at() + UP * 0.55)
            sticky = tech_icon("sticky", PRIVATE, height=0.7)
            sticky_key = Key(PRIVATE, height=0.24)
            sticky_key.move_to(sticky.get_center() + DOWN * 0.02)
            exposed = VGroup(sticky, sticky_key)
            exposed.move_to(pillars[2].body_at() + DOWN * 0.7)
            self.play(pillars[2].fill_anim(1.0, run_time=0.5),
                      FadeIn(safe, scale=0.8), run_time=0.7)
            self.play(FadeIn(exposed, scale=0.8), run_time=0.5)
            bad_mark = cross_mark(CIPHER, height=0.3)
            bad_mark.next_to(exposed, RIGHT, buff=0.12)
            self.play(GrowFromCenter(bad_mark), run_time=0.4)
            self.col3 = VGroup(safe, exposed, bad_mark)

        with self.beat(5.85, "Even a strong algorithm can be compromised if a "
                            "key is stolen, guessed, or accidentally "
                            "exposed."):
            self.play(FadeOut(pillars, self.col1, self.col2, self.col3,
                              shift=DOWN * 0.4), run_time=0.6)
            # One icon per verb, landing on the word.
            stolen = VGroup(GrabHand(SNOOP, height=0.9),
                            Key(PRIVATE, height=0.38))
            stolen[1].move_to(stolen[0].get_top() + UP * 0.1)
            guessed = tech_icon("dice", SNOOP, height=0.9)
            exposed = VGroup(Laptop(SNOOP, height=1.0),
                             Key(PRIVATE, height=0.3))
            exposed[1].move_to(exposed[0].screen.get_center())
            trio = VGroup(
                labelled(stolen, "stolen", SNOOP),
                labelled(guessed, "guessed", SNOOP),
                labelled(exposed, "exposed", SNOOP),
            ).arrange(RIGHT, buff=1.5).move_to(UP * 0.2)
            for item in trio:
                self.play(FadeIn(item, shift=UP * 0.3, scale=0.85),
                          run_time=0.55)
                self.wait(1.1)
            self.trio = trio

        with self.beat(6.73, "For example, if an attacker obtains a password "
                            "used to protect the encrypted file, the "
                            "encryption itself may not be broken."):
            self.play(FadeOut(self.trio, shift=UP * 0.4), run_time=0.5)
            eve = Eve(height=1.8).move_to(LEFT * 4.3 + DOWN * 0.3)
            sticky = tech_icon("sticky", PRIVATE, height=0.95)
            sticky.next_to(eve, RIGHT, buff=0.4).shift(UP * 0.3)
            pw = Text(PASSWORD, font=MONO, font_size=SMALL - 3, color=PRIVATE)
            pw.move_to(sticky).shift(DOWN * 0.02)
            self.play(FadeIn(eve, shift=RIGHT * 0.4), run_time=0.7)
            self.play(FadeIn(sticky, scale=0.8), Write(pw), run_time=0.9)

            locked = VGroup(tech_icon("file", PUBLIC, height=1.7),
                            Padlock(PRIVATE, height=0.75))
            locked[1].move_to(locked[0].get_center())
            locked.move_to(RIGHT * 3.4 + UP * 0.1)
            self.play(FadeIn(locked, shift=LEFT * 0.4), run_time=0.7)
            intact = caption("the algorithm is not broken", PLAIN,
                             size=SMALL - 2)
            intact.next_to(locked, DOWN, buff=0.5)
            self.play(
                Indicate(locked[1], scale_factor=1.1, color=PRIVATE),
                Write(intact), run_time=1.3,
            )
            self.theft = VGroup(eve, sticky, pw, locked, intact)

        with self.beat(4.06, "Instead, the attackers obtain the key needed "
                             "to unlock the information."):
            self.play(FadeOut(self.theft[4]), run_time=0.3)
            pw_box = VGroup(self.theft[1], self.theft[2])
            kdf = AlgoBox("key derivation", width=2.8, height=0.9, gears=False)
            kdf.scale(0.9).move_to(LEFT * 0.4 + UP * 0.1)
            derived = Key(PRIVATE, height=0.5).move_to(RIGHT * 2.4 + UP * 0.1)
            a1 = Arrow(pw_box.get_right(), kdf.get_left(), buff=0.2, color=FG,
                       stroke_width=5, max_tip_length_to_length_ratio=0.25)
            a2 = Arrow(kdf.get_right(), derived.get_left(), buff=0.25,
                       color=FG, stroke_width=5,
                       max_tip_length_to_length_ratio=0.25)
            self.play(
                self.theft[3].animate.scale(0.75).move_to(RIGHT * 5.0 + DOWN * 1.6),
                run_time=0.5,
            )
            self.play(GrowArrow(a1), Create(kdf), run_time=0.7)
            self.play(GrowArrow(a2), FadeIn(derived, scale=0.6), run_time=0.7)
            self.play(
                derived.animate.move_to(self.theft[3][1].get_center()),
                run_time=0.7,
            )
            self.play(self.theft[3][1].unlock_anim(), run_time=0.4)
            opened = check_mark(PLAIN, height=0.45)
            opened.next_to(self.theft[3], UP, buff=0.2)
            self.play(GrowFromCenter(opened), run_time=0.4)
            self.derive = VGroup(kdf, a1, a2, derived, opened)

        ring = LifecycleRing().scale(0.82).move_to(DOWN * 0.1)
        with self.beat(3.98, "This is why key management is one of the most "
                            "important parts of cybersecurity."):
            self.play(FadeOut(self.theft, self.derive, shift=DOWN * 0.5),
                      run_time=0.5)
            title_text = heading("key management", PRIVATE, size=LABEL)
            title_text.to_edge(UP, buff=0.9)
            self.play(Write(title_text), run_time=0.5)
            self.play(ring.draw_anim(run_time=1.3))
            travelling = Key(PRIVATE, height=0.4)
            travelling.move_to(ring.points_on_ring[0] + ring.get_center())
            self.play(FadeIn(travelling, scale=0.6), run_time=0.25)
            self.play(ring.travel_anim(travelling, run_time=1.2))
            self.ring_bits = VGroup(ring, travelling, title_text)

        with self.beat(1.0, "(transition)"):
            next_tag = tag_for(2)
            self.play(
                FadeOut(self.ring_bits, scale=0.7),
                ReplacementTransform(tag, next_tag),
                run_time=1.0,
            )

        self.pad_to_target()


# --- 7. Symmetric encryption (2:22-3:11) -----------------------------------


class Scene07Symmetric(VideoScene):
    """One shared key — and the problem of getting it to the other end."""

    TARGET = 42.96

    def construct(self):
        self.add(tag_for(2))

        with self.beat(2.0, "(music only)"):
            card = chapter_card(2, "Types of Encryption")
            self.play(FadeIn(card, shift=UP * 0.3), run_time=0.7)
            self.wait(0.5)
            self.play(FadeOut(card, shift=UP * 0.3), run_time=0.5)

        def panel(title, keys, color):
            shell = RoundedRectangle(
                width=5.6, height=3.6, corner_radius=0.22, color=color,
                stroke_width=STROKE_THIN, fill_color=SURFACE, fill_opacity=0.5,
            )
            head = caption(title, color=color, size=LABEL)
            head.next_to(shell.get_top(), DOWN, buff=0.35)
            art = VGroup(*keys).arrange(RIGHT, buff=0.5)
            art.move_to(shell.get_center() + DOWN * 0.2)
            return VGroup(shell, head, art)

        sym = panel("SYMMETRIC", [Key(PRIVATE, height=0.7)], PRIVATE)
        asym = panel("ASYMMETRIC",
                     [Key(PUBLIC, height=0.7), Key(PRIVATE, height=0.7)],
                     PUBLIC)
        VGroup(sym, asym).arrange(RIGHT, buff=0.7).scale(0.92).move_to(UP * 0.2)

        with self.beat(5.33, "There are two main categories of encryption. "
                             "Symmetric encryption and asymmetric "
                             "encryption."):
            self.play(FadeIn(sym, shift=RIGHT * 0.3), run_time=0.9)
            self.wait(0.8)
            self.play(FadeIn(asym, shift=LEFT * 0.3), run_time=0.9)

        with self.beat(4.27, "Symmetric encryption uses the same key for both "
                            "encryption and decryption."):
            # Dim the other panel and slide it clear rather than growing
            # the symmetric one on top of it.
            self.play(asym.animate.set_opacity(0.15).shift(RIGHT * 1.4),
                      sym.animate.scale(1.1).move_to(LEFT * 3.1 + UP * 0.2),
                      run_time=0.7)
            key = sym[2][0]
            lock_arrow = Arrow(LEFT * 1.4, LEFT * 0.35, color=PLAIN, buff=0,
                               stroke_width=5)
            unlock_arrow = Arrow(RIGHT * 0.35, RIGHT * 1.4, color=CIPHER,
                                 buff=0, stroke_width=5)
            VGroup(lock_arrow, unlock_arrow).move_to(
                key.get_center() + UP * 0.95)
            l1 = caption("encrypt", PLAIN, size=SMALL - 3)
            l1.next_to(lock_arrow, UP, buff=0.12)
            l2 = caption("decrypt", CIPHER, size=SMALL - 3)
            l2.next_to(unlock_arrow, UP, buff=0.12)
            self.play(GrowArrow(lock_arrow), FadeIn(l1), run_time=0.5)
            self.play(GrowArrow(unlock_arrow), FadeIn(l2), run_time=0.5)
            self.play(Indicate(key, scale_factor=1.25, color=PRIVATE),
                      run_time=0.8)
            self.arrows = VGroup(lock_arrow, unlock_arrow, l1, l2)

        with self.beat(5.44, "The sender uses the key to encrypt the message, "
                            "and the recipient uses that same key to decrypt "
                            "it."):
            self.play(FadeOut(sym, asym, self.arrows), run_time=0.5)
            maya = Person(FG, height=1.6, name="Maya").move_to(LEFT * 4.9)
            sam = Person(FG, height=1.6, name="Sam").move_to(RIGHT * 4.9)
            self.play(FadeIn(maya, shift=RIGHT * 0.3),
                      FadeIn(sam, shift=LEFT * 0.3), run_time=0.55)

            k_maya = Key(PRIVATE, height=0.5)
            k_maya.next_to(maya.figure, RIGHT, buff=0.3).shift(UP * 0.2)
            k_sam = Key(PRIVATE, height=0.5)
            k_sam.next_to(sam.figure, LEFT, buff=0.3).shift(UP * 0.2)
            self.play(FadeIn(k_maya, scale=0.6), FadeIn(k_sam, scale=0.6),
                      run_time=0.4)
            equals = Text("=", font_size=42, color=PRIVATE).move_to(UP * 1.7)
            self.play(Write(equals), run_time=0.3)
            self.play(Indicate(equals, scale_factor=1.4, color=PRIVATE),
                      run_time=0.5)

            msg = Note(MSG, PLAIN, size=SMALL).scale(0.6)
            msg.move_to(k_maya.get_center() + DOWN * 1.3)
            self.play(FadeIn(msg, scale=0.6), run_time=0.4)
            lock = Padlock(PRIVATE, height=0.42)
            lock.move_to(msg.get_right() + RIGHT * 0.25)
            self.play(stamp_anim(lock, run_time=0.5))
            locked = VGroup(msg, lock)
            self.play(
                msg.label.animate.set_color(CIPHER),
                locked.animate.move_to(DOWN * 1.1),
                run_time=0.65,
            )
            self.play(locked.animate.move_to(k_sam.get_center() + DOWN * 1.3),
                      run_time=0.65)
            self.play(lock.unlock_anim(),
                      msg.label.animate.set_color(PLAIN), run_time=0.45)
            self.pair = VGroup(maya, sam, k_maya, k_sam, equals, locked)

        with self.beat(6.13, "Symmetric encryption is generally fast and "
                            "efficient, which makes it useful for encrypting "
                            "large amounts of data."):
            self.play(FadeOut(self.pair, shift=DOWN * 0.4), run_time=0.5)
            algo = AlgoBox("AES-256").scale(0.9).move_to(ORIGIN)
            self.play(Create(algo), run_time=0.5)

            blocks = VGroup(*[
                Square(side_length=0.3, color=PLAIN, stroke_width=2.5,
                       fill_color=PLAIN, fill_opacity=0.25)
                for _ in range(18)
            ]).arrange_in_grid(rows=3, cols=6, buff=0.12)
            blocks.move_to(LEFT * 4.6)
            self.play(FadeIn(blocks, lag_ratio=0.04), run_time=0.6)

            disk = VGroup(tech_icon("database", PUBLIC, height=1.5))
            disk.move_to(RIGHT * 4.6)
            self.play(FadeIn(disk), run_time=0.4)

            # Streaming, not marching: the point of the beat is throughput.
            self.play(
                LaggedStart(*[
                    Succession(
                        b.animate(run_time=0.5).move_to(algo.get_center()),
                        b.animate(run_time=0.01).set_color(CIPHER),
                        b.animate(run_time=0.5).move_to(
                            disk.get_center()
                            + RIGHT * 0.001 * i).scale(0.3).set_opacity(0),
                    )
                    for i, b in enumerate(blocks)
                ], lag_ratio=0.1),
                algo.turn(TAU * 3, run_time=3.0),
                run_time=3.2,
            )
            vault_lock = Padlock(PRIVATE, height=0.55)
            vault_lock.move_to(disk.get_center())
            self.play(stamp_anim(vault_lock, run_time=0.5))
            self.stream = VGroup(algo, blocks, disk, vault_lock)

        with self.beat(6.29, "Common symmetric encryption algorithms include "
                            "the Advanced Encryption Standard, or AES, and "
                            "ChaCha20."):
            self.play(FadeOut(self.stream, shift=UP * 0.4), run_time=0.5)
            aes = SpecCard("AES", [
                "block cipher",
                "128-bit blocks",
                "128 / 192 / 256-bit keys",
            ], PRIVATE)
            chacha = SpecCard("ChaCha20", [
                "stream cipher",
                "256-bit key",
                "fast in software",
            ], PLAIN)
            VGroup(aes, chacha).arrange(RIGHT, buff=1.0).move_to(UP * 0.1)
            self.play(aes.flip_in(run_time=0.9))
            self.wait(1.2)
            self.play(chacha.flip_in(run_time=0.9))
            self.cards = VGroup(aes, chacha)

        maya = Person(FG, height=1.6, name="Maya").move_to(LEFT * 5.0 + UP * 0.3)
        sam = Person(FG, height=1.6, name="Sam").move_to(RIGHT * 5.0 + UP * 0.3)
        wire, wire_path = channel(
            maya.figure.get_right() + RIGHT * 0.3,
            sam.figure.get_left() + LEFT * 0.3,
        )
        channel_tag = caption("insecure channel", SNOOP, size=SMALL - 2)
        channel_tag.next_to(wire, UP, buff=0.3)

        with self.beat(6.72, "However, symmetric encryption creates an "
                            "important challenge: both parties need to "
                            "obtain the same secret key securely."):
            self.play(FadeOut(self.cards, shift=DOWN * 0.4), run_time=0.5)
            self.play(FadeIn(maya, shift=RIGHT * 0.3),
                      FadeIn(sam, shift=LEFT * 0.3), run_time=0.7)
            self.play(Create(wire), FadeIn(channel_tag), run_time=0.8)
            travelling = Key(PRIVATE, height=0.5)
            travelling.move_to(wire_path.get_start())
            self.play(FadeIn(travelling, scale=0.6), run_time=0.4)
            self.play(MoveAlongPath(travelling, wire_path), run_time=2.2)
            self.play(Flash(travelling, color=PRIVATE, line_length=0.14,
                            flash_radius=0.4), run_time=0.5)
            self.travelling = travelling

        with self.beat(5.78, "If the key is sent through an insecure channel "
                            "and intercepted, an attacker may be able to "
                            "decrypt the communication."):
            self.play(self.travelling.animate.move_to(wire_path.get_start()),
                      run_time=0.4)
            eve = Eve(height=1.7).move_to(DOWN * 2.1)
            self.play(FadeIn(eve, shift=UP * 0.4), run_time=0.6)

            # Eve takes a copy mid-flight; the original carries on, which is
            # what makes passive interception so hard to notice.
            self.play(MoveAlongPath(self.travelling, wire_path), run_time=0.85,
                      rate_func=lambda t: t * 0.5)
            stolen = Key(SNOOP, height=0.5).move_to(self.travelling)
            self.play(
                TransformFromCopy(self.travelling, stolen), run_time=0.5,
            )
            self.play(stolen.animate.next_to(eve.figure, UP, buff=0.2),
                      run_time=0.5)
            self.play(MoveAlongPath(self.travelling, wire_path), run_time=0.75,
                      rate_func=lambda t: 0.5 + t * 0.5)

            cipher = mono(scrambled(MSG, seed=13), CIPHER, size=SMALL)
            cipher.move_to(wire.get_center())
            self.play(FadeIn(cipher), run_time=0.4)
            plain = mono(MSG, PLAIN, size=SMALL)
            plain.next_to(eve.figure, RIGHT, buff=0.4)
            self.play(TransformFromCopy(cipher, plain), run_time=0.65)
            alert = SurroundingRectangle(
                VGroup(eve, stolen, plain), color=CIPHER, buff=0.3,
                corner_radius=0.14, stroke_width=3,
            )
            self.play(Create(alert), run_time=0.6)
            self.scene_bits = VGroup(maya, sam, wire, channel_tag,
                                     self.travelling, eve, cipher, plain, alert)
            self.stolen = stolen

        with self.beat(1.0, "(transition)"):
            blue = Key(PUBLIC, height=0.5)
            gold = Key(PRIVATE, height=0.5)
            VGroup(blue, gold).arrange(RIGHT, buff=0.6).move_to(ORIGIN)
            self.play(
                FadeOut(self.scene_bits, scale=0.7),
                ReplacementTransform(self.stolen, VGroup(blue, gold)),
                run_time=1.0,
            )
            self.remove(blue, gold)

        self.pad_to_target()


# --- 8. Asymmetric encryption (3:11-4:16) ----------------------------------


class Scene08Asymmetric(VideoScene):
    """The key pair, the directory, the speed cost, RSA and ECC."""

    TARGET = 54.33

    def construct(self):
        self.add(tag_for(2))

        pub = Key(PUBLIC, height=0.8)
        priv = Key(PRIVATE, height=0.8)
        VGroup(pub, priv).arrange(RIGHT, buff=3.2).move_to(UP * 0.7)
        pub_tag = caption("PUBLIC KEY", PUBLIC, size=SMALL)
        pub_tag.next_to(pub, DOWN, buff=0.3)
        priv_tag = caption("PRIVATE KEY", PRIVATE, size=SMALL)
        priv_tag.next_to(priv, DOWN, buff=0.3)
        bond = Line(pub.get_right(), priv.get_left(), color=FG,
                    stroke_width=2.5, stroke_opacity=0.6)
        bond_tag = caption("mathematically related", FG, size=SMALL - 3)
        bond_tag.next_to(bond, UP, buff=0.25)

        with self.beat(7.6, "Asymmetric encryption, also called public-key "
                            "encryption, uses a pair of mathematically "
                            "related keys: a public key and a private key."):
            self.play(FadeIn(pub, scale=0.6), FadeIn(priv, scale=0.6),
                      run_time=0.8)
            self.play(Write(pub_tag), Write(priv_tag), run_time=0.9)
            self.wait(1.0)
            self.play(Create(bond), FadeIn(bond_tag), run_time=0.9)
            self.play(Flash(bond.get_center(), color=FG, line_length=0.2,
                            flash_radius=0.5), run_time=0.6)
            self.pair = VGroup(pub, priv, pub_tag, priv_tag, bond, bond_tag)

        with self.beat(2.25, "The public key can be shared openly."):
            crowd = VGroup(*[
                Person(SNOOP, height=0.95) for _ in range(5)
            ]).arrange(RIGHT, buff=0.9).move_to(DOWN * 2.2)
            self.play(FadeIn(crowd, lag_ratio=0.1, shift=UP * 0.2),
                      run_time=0.6)
            copies = VGroup(*[
                Key(PUBLIC, height=0.34).next_to(p, UP, buff=0.15)
                for p in crowd
            ])
            self.play(LaggedStart(*[
                TransformFromCopy(pub, c) for c in copies
            ], lag_ratio=0.12), run_time=1.6)
            self.crowd, self.copies = crowd, copies

        vault = tech_icon("vault", PRIVATE, height=1.2)
        with self.beat(2.16, "The private key must be kept secret."):
            sam = Person(FG, height=1.4, name="Sam").move_to(RIGHT * 5.1 + DOWN * 1.9)
            vault.next_to(sam.figure, LEFT, buff=0.45)
            # Make room on the right: the crowd fills the width, and Sam's
            # vault would otherwise land on top of the last figure.
            self.play(self.crowd.animate.shift(LEFT * 1.9),
                      self.copies.animate.shift(LEFT * 1.9),
                      FadeIn(sam, shift=LEFT * 0.3), FadeIn(vault, scale=0.7),
                      run_time=0.7)
            self.play(priv.animate.scale(0.5).move_to(vault.get_center()),
                      FadeOut(priv_tag, bond, bond_tag), run_time=0.9)
            self.play(Flash(vault, color=PRIVATE, line_length=0.15,
                            flash_radius=0.7), run_time=0.5)
            self.sam, self.vault = sam, vault

        with self.beat(5.37, "Information encrypted with the public key can "
                            "generally be decrypted only with the "
                            "corresponding private key."):
            self.play(FadeOut(self.crowd, self.copies, self.sam, pub_tag,
                              shift=DOWN * 0.3), run_time=0.5)
            msg = Note(MSG, PLAIN, size=SMALL).scale(0.75).move_to(LEFT * 3.4)
            self.play(FadeIn(msg, scale=0.7), run_time=0.4)
            self.play(pub.animate.scale(0.55).next_to(msg, UP, buff=0.3),
                      run_time=0.45)
            lock = Padlock(PUBLIC, height=0.5)
            lock.move_to(msg.get_right() + RIGHT * 0.3)
            self.play(stamp_anim(lock, run_time=0.5),
                      msg.label.animate.set_color(CIPHER))

            try_blue = Key(PUBLIC, height=0.45).move_to(ORIGIN + UP * 0.9)
            self.play(FadeIn(try_blue, shift=DOWN * 0.3), run_time=0.3)
            self.play(try_blue.animate.next_to(lock, RIGHT, buff=0.2),
                      run_time=0.4)
            no = cross_mark(CIPHER, height=0.4).next_to(try_blue, RIGHT, buff=0.2)
            self.play(GrowFromCenter(no),
                      Wiggle(lock, scale_value=1.05), run_time=0.55)

            # The same private key that went into the vault, coming back
            # out — not a second one that would outlive the beat.
            gold = priv
            self.play(FadeOut(try_blue, no, shift=UP * 0.3), run_time=0.25)
            self.play(gold.animate.scale(1.8).next_to(lock, RIGHT, buff=0.2),
                      run_time=0.55)
            self.play(lock.unlock_anim(),
                      msg.label.animate.set_color(PLAIN), run_time=0.4)
            yes = check_mark(PLAIN, height=0.42).next_to(gold, RIGHT, buff=0.25)
            self.play(GrowFromCenter(yes), run_time=0.3)
            self.lock_demo = VGroup(msg, pub, lock, gold, yes)

        with self.beat(7.02, "For example, if someone wants to send a secure "
                             "message to a recipient, they can encrypt the "
                             "message using the recipient’s public key."):
            self.play(FadeOut(self.lock_demo, self.vault, shift=UP * 0.4),
                      run_time=0.5)
            # A public directory: where a real sender gets a public key from.
            entries = VGroup(*[
                VGroup(
                    caption(name, FG, size=SMALL - 3),
                    Key(PUBLIC, height=0.26),
                ).arrange(RIGHT, buff=0.3)
                for name in ("Sam", "Priya", "Lee")
            ]).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
            dir_head = caption("public directory", PUBLIC, size=SMALL - 2)
            dir_head.next_to(entries, UP, buff=0.3)
            shell = RoundedRectangle(
                width=entries.width + 1.0,
                height=entries.height + dir_head.height + 1.0,
                corner_radius=0.16, color=PUBLIC, stroke_width=STROKE_THIN,
                fill_color=SURFACE, fill_opacity=1,
            ).move_to(VGroup(entries, dir_head))
            directory = VGroup(shell, dir_head, entries).move_to(UP * 0.4)

            maya = Person(FG, height=1.6, name="Maya")
            maya.move_to(LEFT * 5.0 + DOWN * 0.3)
            self.play(FadeIn(maya, shift=RIGHT * 0.3), run_time=0.6)
            self.play(FadeIn(directory, shift=DOWN * 0.3), run_time=0.9)
            self.wait(1.0)

            taken = Key(PUBLIC, height=0.42)
            self.play(TransformFromCopy(entries[0][1], taken), run_time=0.7)
            self.play(taken.animate.next_to(maya.figure, RIGHT, buff=0.4)
                      .shift(UP * 0.5), run_time=0.8)

            msg = Note(MSG, PLAIN, size=SMALL).scale(0.7)
            msg.next_to(maya.figure, RIGHT, buff=0.4).shift(DOWN * 0.7)
            self.play(FadeIn(msg, scale=0.7), run_time=0.5)
            lock = Padlock(PUBLIC, height=0.45)
            lock.move_to(msg.get_right() + RIGHT * 0.28)
            self.play(stamp_anim(lock, run_time=0.6),
                      msg.label.animate.set_color(CIPHER))
            self.play(Indicate(VGroup(msg, lock), scale_factor=1.08,
                               color=PUBLIC), run_time=0.8)
            self.maya, self.directory = maya, directory
            self.sealed, self.taken = VGroup(msg, lock), taken

        with self.beat(3.22, "Only the recipient’s private key should be "
                            "able to decrypt it."):
            self.play(FadeOut(self.directory, self.taken, shift=UP * 0.3),
                      run_time=0.4)
            eve = Eve(height=1.5).move_to(UP * 1.6)
            eve_key = Key(PUBLIC, height=0.34)
            eve_key.next_to(eve.figure, RIGHT, buff=0.2)
            sam = Person(FG, height=1.5, name="Sam").move_to(RIGHT * 4.9 + DOWN * 0.3)
            sam_key = Key(PRIVATE, height=0.4)
            sam_key.next_to(sam.figure, LEFT, buff=0.3).shift(UP * 0.3)
            self.play(FadeIn(eve, eve_key), FadeIn(sam, sam_key), run_time=0.4)
            self.play(self.sealed.animate.move_to(UP * 0.2), run_time=0.4)

            self.play(eve_key.animate.next_to(self.sealed, UP, buff=0.2),
                      run_time=0.3)
            no = cross_mark(CIPHER, height=0.38).next_to(eve_key, RIGHT, buff=0.2)
            self.play(GrowFromCenter(no), Wiggle(self.sealed[1]), run_time=0.4)

            self.play(FadeOut(eve_key, no), run_time=0.2)
            self.play(self.sealed.animate.next_to(sam.figure, LEFT, buff=0.6),
                      run_time=0.4)
            self.play(sam_key.animate.next_to(self.sealed, UP, buff=0.2),
                      run_time=0.25)
            self.play(self.sealed[1].unlock_anim(),
                      self.sealed[0].label.animate.set_color(PLAIN),
                      run_time=0.35)
            self.cast_bits = VGroup(self.maya, eve, sam, sam_key, self.sealed)

        with self.beat(5.76, "Asymmetric encryption solves much of the "
                            "key-distribution problem because the public key "
                            "does not need to be kept secret."):
            self.play(FadeOut(self.cast_bits, shift=DOWN * 0.3), run_time=0.5)
            # The callback: scene 7's channel, with a public key on it.
            maya = Person(FG, height=1.5, name="Maya").move_to(LEFT * 5.0 + UP * 0.4)
            sam = Person(FG, height=1.5, name="Sam").move_to(RIGHT * 5.0 + UP * 0.4)
            wire, wire_path = channel(
                maya.figure.get_right() + RIGHT * 0.3,
                sam.figure.get_left() + LEFT * 0.3,
            )
            tag = caption("insecure channel", SNOOP, size=SMALL - 2)
            tag.next_to(wire, UP, buff=0.3)
            self.play(FadeIn(maya, sam), Create(wire), FadeIn(tag),
                      run_time=0.65)

            blue = Key(PUBLIC, height=0.45).move_to(wire_path.get_start())
            self.play(FadeIn(blue, scale=0.6), run_time=0.25)
            eve = Eve(height=1.6).move_to(DOWN * 2.0)
            self.play(FadeIn(eve, shift=UP * 0.3), run_time=0.4)
            self.play(MoveAlongPath(blue, wire_path), run_time=1.1,
                      rate_func=lambda t: t * 0.55)
            copy = Key(PUBLIC, height=0.4).move_to(blue)
            self.play(TransformFromCopy(blue, copy), run_time=0.4)
            self.play(copy.animate.next_to(eve.figure, UP, buff=0.2),
                      MoveAlongPath(blue, wire_path,
                                    rate_func=lambda t: 0.55 + t * 0.45),
                      run_time=0.85)
            shrug = Text("¯\\_(ツ)_/¯", font_size=28, color=SNOOP)
            shrug.next_to(eve, RIGHT, buff=0.4)
            nothing = caption("public by design — nothing gained", SNOOP,
                              size=SMALL - 2)
            nothing.next_to(eve, DOWN, buff=0.25)
            self.play(FadeIn(shrug, scale=0.7), Write(nothing), run_time=0.85)
            self.callback = VGroup(maya, sam, wire, tag, blue, eve, copy,
                                   shrug, nothing)

        with self.beat(4.98, "However, it is typically slower and more "
                            "computationally expensive than symmetric "
                            "encryption."):
            self.play(FadeOut(self.callback, shift=UP * 0.4), run_time=0.5)
            fast = ThroughputBar("symmetric", rate=1.0, color=PLAIN)
            slow = ThroughputBar("asymmetric", rate=0.16, color=CIPHER)
            VGroup(fast, slow).arrange(DOWN, buff=1.0, aligned_edge=RIGHT)
            VGroup(fast, slow).move_to(UP * 0.2)
            note = caption("relative throughput, same hardware", SNOOP,
                           size=SMALL - 3)
            note.next_to(slow, DOWN, buff=0.6)
            self.play(FadeIn(fast), FadeIn(slow), FadeIn(note), run_time=0.6)
            self.play(fast.run_anim(run_time=2.6), slow.run_anim(run_time=2.6))
            fast.freeze()
            slow.freeze()
            self.race = VGroup(fast, slow, note)

        with self.beat(6.44, "Examples of public-key algorithms include RSA "
                            "and elliptic-curve cryptography, often called "
                            "ECC."):
            self.play(FadeOut(self.race, shift=UP * 0.4), run_time=0.4)

            # RSA: two primes multiply easily, the product does not factor.
            p_text = Text("p", font=MONO, font_size=BODY, color=PUBLIC)
            q_text = Text("q", font=MONO, font_size=BODY, color=PUBLIC)
            times = Text("×", font_size=BODY, color=FG)
            eq = Text("=", font_size=BODY, color=FG)
            n_text = Text("n", font=MONO, font_size=BODY, color=PRIVATE)
            row = VGroup(p_text, times, q_text, eq, n_text)
            row.arrange(RIGHT, buff=0.22)
            easy = caption("easy →", PLAIN, size=SMALL - 4)
            easy.next_to(row, UP, buff=0.25)
            hard = caption("← hard", CIPHER, size=SMALL - 4)
            hard.next_to(row, DOWN, buff=0.25)
            rsa = VGroup(
                heading("RSA", PUBLIC, size=LABEL),
                VGroup(row, easy, hard),
                caption("factoring two large primes", FG, size=SMALL - 4),
            ).arrange(DOWN, buff=0.4).move_to(LEFT * 3.5 + DOWN * 0.1)

            curve = EllipticCurve().scale(0.62)
            ecc = VGroup(heading("ECC", PLAIN, size=LABEL), curve)
            ecc.arrange(DOWN, buff=0.25).move_to(RIGHT * 3.5 + DOWN * 0.1)

            self.play(FadeIn(rsa, shift=RIGHT * 0.3), run_time=0.8)
            self.play(FadeIn(ecc[0]), Create(curve.axes), run_time=0.5)
            self.play(Create(curve.curve), FadeIn(curve.equation), run_time=1.0)
            hop = Dot(curve.point(1.4), radius=0.07, color=PRIVATE)
            self.play(FadeIn(hop, scale=0.5), run_time=0.3)
            self.play(curve.hop_anim(hop, [0.4, 1.9, -0.6, 1.1], run_time=1.4))
            self.algos = VGroup(rsa, ecc, hop)

        with self.beat(8.53, "ECC can provide strong security with shorter "
                             "key sizes, which makes it useful in mobile "
                             "devices, web browsers, and other systems with "
                             "limited resources."):
            self.play(FadeOut(self.algos, shift=UP * 0.4), run_time=0.5)
            bars = KeySizeBars().scale(0.95).move_to(UP * 1.0)
            self.play(FadeIn(bars.rows[0][1]), FadeIn(bars.rows[1][1]),
                      FadeIn(bars.note), run_time=0.4)
            self.play(bars.grow_anim(run_time=1.8))
            self.wait(1.6)

            devices = VGroup(
                labelled(Phone(PUBLIC, height=1.2), "phone", FG),
                labelled(BrowserBar("https://", width=2.6).scale(0.8),
                         "browser", FG),
                labelled(tech_icon("chip", PUBLIC, height=1.1), "small chip", FG),
            ).arrange(RIGHT, buff=1.2).move_to(DOWN * 1.9)
            for item in devices:
                self.play(FadeIn(item, shift=UP * 0.3, scale=0.85),
                          run_time=0.5)
                self.wait(0.7)
            self.sizes = VGroup(bars, devices)

        with self.beat(1.0, "(transition)"):
            merged = RoundedRectangle(
                width=5.0, height=2.6, corner_radius=0.22, color=FG,
                stroke_width=STROKE_THIN, fill_color=SURFACE, fill_opacity=0.5,
            )
            self.play(FadeOut(self.sizes, scale=0.7),
                      FadeIn(merged, scale=1.2), run_time=1.0)
            self.remove(merged)

        self.pad_to_target()


# --- 9. Hybrid encryption and HTTPS (4:16-4:47) ----------------------------


class Scene09Hybrid(VideoScene):
    """Asymmetric to agree a key, symmetric to carry the data."""

    TARGET = 26.62

    def construct(self):
        self.add(tag_for(2))

        with self.beat(4.69, "In practice, many modern systems use a hybrid "
                            "approach that combines both types."):
            shell = RoundedRectangle(
                width=6.4, height=4.3, corner_radius=0.22, color=FG,
                stroke_width=STROKE_THIN, fill_color=SURFACE, fill_opacity=0.4,
            ).move_to(UP * 0.1)
            head = caption("HYBRID", FG, size=LABEL)
            head.next_to(shell.get_top(), DOWN, buff=0.3)
            self.play(FadeIn(shell), Write(head), run_time=0.8)

            pair = VGroup(Key(PUBLIC, height=0.55), Key(PRIVATE, height=0.55))
            pair.arrange(RIGHT, buff=0.7).move_to(shell.get_center() + UP * 0.75)
            pair_tag = caption("asymmetric: agree a key", PUBLIC, size=SMALL - 3)
            pair_tag.next_to(pair, UP, buff=0.22)
            self.play(FadeIn(pair, scale=0.7), FadeIn(pair_tag), run_time=0.8)

            session = Key(PRIVATE, height=0.65)
            session.move_to(shell.get_center() + DOWN * 1.0)
            session_tag = caption("symmetric: carry the data", PRIVATE,
                                  size=SMALL - 3)
            session_tag.next_to(session, DOWN, buff=0.22)
            feed = VGroup(*[
                Arrow(k.get_bottom() + DOWN * 0.1, session.get_top() + UP * 0.1,
                      buff=0.1, color=FG, stroke_width=3.5,
                      max_tip_length_to_length_ratio=0.25)
                for k in pair
            ])
            self.play(LaggedStart(*[GrowArrow(a) for a in feed],
                                  lag_ratio=0.25), run_time=0.8)
            self.play(FadeIn(session, scale=0.6), Write(session_tag),
                      run_time=0.9)
            self.panel = VGroup(shell, head, pair, pair_tag, feed, session,
                                session_tag)

        laptop = Laptop(FG, height=2.3).move_to(LEFT * 4.4 + DOWN * 0.5)
        bar = BrowserBar("https://example.com", width=4.4).scale(0.62)
        bar.next_to(laptop, UP, buff=0.4)
        server = Server(FG, height=2.6).move_to(RIGHT * 4.6 + DOWN * 0.3)
        server_tag = caption("server", FG, size=SMALL)
        server_tag.next_to(server, DOWN, buff=0.25)

        with self.beat(3.92, "For example, when a user visits a website using "
                            "HTTPS,"):
            self.play(FadeOut(self.panel, scale=0.8), run_time=0.5)
            self.play(FadeIn(laptop, shift=RIGHT * 0.3),
                      FadeIn(server, server_tag, shift=LEFT * 0.3),
                      run_time=0.8)
            self.play(FadeIn(bar, shift=DOWN * 0.3), run_time=0.6)
            self.play(Indicate(bar.lock, scale_factor=1.3, color=PRIVATE),
                      run_time=0.7)

        with self.beat(6.23, "asymmetric cryptography can help the browser and "
                            "the server authenticate each other and establish "
                            "a shared session key."):
            cert = Certificate("example.com", width=2.8).scale(0.9)
            cert.move_to(server.get_left() + LEFT * 1.4 + UP * 0.9)
            self.play(FadeIn(cert, shift=LEFT * 0.4), run_time=0.6)
            self.play(cert.animate.move_to(laptop.get_right() + RIGHT * 1.5
                                           + UP * 0.9), run_time=0.85)
            checking = caption("signature checked", PLAIN, size=SMALL - 3)
            checking.next_to(cert, UP, buff=0.22)
            self.play(Indicate(cert.seal, scale_factor=1.3, color=PRIVATE),
                      Write(checking), run_time=0.85)
            self.play(FadeOut(cert, checking, shift=UP * 0.3), run_time=0.4)

            # Each side contributes a half; the shared key appears on both
            # sides at once and never crosses the wire.
            merge = SessionKeyMerge(height=0.6)
            merge.move_to(DOWN * 0.4)
            self.play(FadeIn(merge.left, shift=RIGHT * 0.5),
                      FadeIn(merge.right, shift=LEFT * 0.5), run_time=0.7)
            self.play(merge.merge_anim(run_time=0.85))
            shared = caption("shared session key", PRIVATE, size=SMALL - 2)
            shared.next_to(merge.key, DOWN, buff=0.3)
            self.play(Write(shared), run_time=0.5)

            on_each = VGroup(
                Key(PRIVATE, height=0.4).next_to(laptop, UP, buff=1.4),
                Key(PRIVATE, height=0.4).next_to(server, UP, buff=0.4),
            )
            self.play(
                TransformFromCopy(merge.key, on_each[0]),
                TransformFromCopy(merge.key, on_each[1]),
                run_time=0.8,
            )
            self.play(FadeOut(merge.key, shared), run_time=0.35)
            self.session_keys = on_each

        with self.beat(6.35, "After that, symmetric encryption is usually used "
                            "to protect the actual data exchange during the "
                            "session because it is faster."):
            out_lane = Line(laptop.get_right() + RIGHT * 0.3 + UP * 0.35,
                            server.get_left() + LEFT * 0.3 + UP * 0.35)
            in_lane = Line(server.get_left() + LEFT * 0.3 + DOWN * 0.55,
                           laptop.get_right() + RIGHT * 0.3 + DOWN * 0.55)
            lane_tag = caption("AES-256-GCM", PRIVATE, size=SMALL - 3)
            lane_tag.next_to(out_lane, UP, buff=0.25)
            self.play(FadeIn(lane_tag), run_time=0.3)

            for round_ in range(3):
                up_records = VGroup(*[data_record() for _ in range(4)])
                down_records = VGroup(*[data_record(PRIVATE) for _ in range(4)])
                self.play(
                    LaggedStart(*[
                        MoveAlongPath(r, out_lane) for r in up_records
                    ], lag_ratio=0.18, run_time=1.4),
                    LaggedStart(*[
                        MoveAlongPath(r, in_lane) for r in down_records
                    ], lag_ratio=0.18, run_time=1.4),
                )
                self.remove(up_records, down_records)
            self.lanes = lane_tag

        with self.beat(4.43, "This combination provides both secure key "
                            "exchange and efficient communication."):
            ticks = VGroup(
                VGroup(check_mark(PLAIN, 0.34),
                       caption("secure key exchange", PLAIN, size=SMALL - 2))
                .arrange(RIGHT, buff=0.25),
                VGroup(check_mark(PLAIN, 0.34),
                       caption("efficient communication", PLAIN, size=SMALL - 2))
                .arrange(RIGHT, buff=0.25),
            ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
            ticks.move_to(DOWN * 2.5)
            for tick in ticks:
                self.play(FadeIn(tick, shift=RIGHT * 0.3), run_time=0.55)
                self.wait(0.5)
            self.ticks = ticks

        with self.beat(1.0, "(transition)"):
            card = Note(MSG, PLAIN, size=LABEL).move_to(ORIGIN)
            self.play(
                FadeOut(laptop, bar, server, server_tag, self.session_keys,
                        self.lanes, self.ticks, scale=0.7),
                FadeIn(card, scale=1.3),
                run_time=1.0,
            )
            self.remove(card)

        self.pad_to_target()


# --- 10. Hashing and digital signatures (4:47-5:25) ------------------------


class Scene10Hashing(VideoScene):
    """One-way hashing, the avalanche, and what a signature is for."""

    TARGET = 29.91

    def construct(self):
        tag = tag_for(2)
        self.add(tag)

        with self.beat(3.3, "It is also important to distinguish encryption "
                            "from hashing."):
            divider = DashedLine(UP * 3.2, DOWN * 3.2, color=SNOOP,
                                 stroke_width=2, dash_length=0.12)
            enc_head = heading("encryption", ALGO, size=LABEL)
            enc_head.move_to(LEFT * 3.5 + UP * 2.2)
            hash_head = heading("hashing", PUBLIC, size=LABEL)
            hash_head.move_to(RIGHT * 3.5 + UP * 2.2)
            self.play(Create(divider), FadeIn(enc_head), FadeIn(hash_head),
                      run_time=0.8)

            two_way = VGroup(
                Arrow(LEFT * 1.2, RIGHT * 1.2, color=PLAIN, buff=0,
                      stroke_width=5),
                Arrow(RIGHT * 1.2, LEFT * 1.2, color=CIPHER, buff=0,
                      stroke_width=5),
            ).arrange(DOWN, buff=0.3).move_to(LEFT * 3.5 + UP * 0.6)
            two_tag = caption("encrypt ⇄ decrypt", FG, size=SMALL - 2)
            two_tag.next_to(two_way, DOWN, buff=0.3)
            one_way = Arrow(LEFT * 1.2, RIGHT * 1.2, color=PUBLIC, buff=0,
                            stroke_width=5).move_to(RIGHT * 3.5 + UP * 0.6)
            one_tag = caption("one way only", FG, size=SMALL - 2)
            one_tag.next_to(one_way, DOWN, buff=0.3)
            self.play(GrowArrow(two_way[0]), GrowArrow(two_way[1]),
                      FadeIn(two_tag), run_time=0.8)
            self.play(GrowArrow(one_way), FadeIn(one_tag), run_time=0.7)
            self.split = VGroup(divider, enc_head, hash_head, two_way,
                                two_tag, one_way, one_tag)

        with self.beat(6.24, "Hashing transforms data into a fixed-length "
                            "value, called a hash, but it is not designed to "
                            "be reversed."):
            self.play(FadeOut(self.split, shift=UP * 0.4), run_time=0.5)
            box = HashBox().move_to(ORIGIN + UP * 0.4)
            self.play(FadeIn(box), run_time=0.5)

            # A two-character input and a long paragraph: same width out.
            short_in = mono('"hi"', PLAIN, size=SMALL)
            short_in.move_to(LEFT * 4.6 + UP * 1.4)
            long_in = Paragraph(
                "Encryption is the process",
                "of transforming readable",
                "information into an …",
                font=SANS, font_size=SMALL - 6, color=PLAIN, line_spacing=0.6,
            )
            long_in.move_to(LEFT * 4.6 + DOWN * 0.9)

            short_out = HexText(SHA_SHORT, FG, width=32, size=SMALL - 5)
            short_out.move_to(RIGHT * 3.6 + UP * 1.4)
            long_out = HexText(SHA_LONG, FG, width=32, size=SMALL - 5)
            long_out.move_to(RIGHT * 3.6 + DOWN * 0.9)

            self.play(FadeIn(short_in), FadeIn(long_in), run_time=0.6)
            self.play(short_out.type_anim(per_char=0.006),
                      run_time=0.9)
            self.play(long_out.type_anim(per_char=0.006), run_time=0.9)
            same = caption("64 hex characters either way", PUBLIC,
                           size=SMALL - 3)
            same.move_to(RIGHT * 3.6 + DOWN * 2.3)
            self.play(Write(same), run_time=0.8)

            back = Arrow(box.get_right() + RIGHT * 1.4 + DOWN * 1.3,
                         box.get_bottom() + DOWN * 0.3, buff=0.1,
                         color=SNOOP, stroke_width=4,
                         max_tip_length_to_length_ratio=0.25, path_arc=-0.9)
            self.play(GrowArrow(back), run_time=0.5)
            no = cross_mark(CIPHER, height=0.5).move_to(
                box.get_bottom() + DOWN * 0.95 + RIGHT * 0.75)
            self.play(GrowFromCenter(no), run_time=0.5)
            self.hashing = VGroup(box, short_in, long_in, short_out, long_out,
                                  same, back, no)

        # Read as one sentence, so storing passwords and detecting a change
        # share a window: the salted table, then the avalanche under it.
        with self.beat(5.16, "Hashing is commonly used to store passwords "
                             "securely and to verify whether data has been "
                             "changed."):
            self.play(FadeOut(self.hashing, shift=UP * 0.4), run_time=0.4)
            table = DbTable([
                ("maya", SALT, SHA_PASSWORD[:34] + "…"),
                ("sam", "b19c4e02", "c41d8fa0372e55b9d6e17c8ab4590f3c…"),
            ], width=9.4).scale(0.95).move_to(UP * 0.9)
            recipe = VGroup(
                caption("password", PRIVATE, size=SMALL - 2),
                Text("+", font_size=BODY, color=FG),
                caption("random salt", PUBLIC, size=SMALL - 2),
                Arrow(ORIGIN, RIGHT * 0.8, color=FG, buff=0, stroke_width=4),
                caption("SHA-256", ALGO, size=SMALL - 2),
            ).arrange(RIGHT, buff=0.25).move_to(DOWN * 1.4)
            self.play(FadeIn(recipe, shift=UP * 0.2), run_time=0.5)
            self.play(FadeIn(table.header), Create(table.rule), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2)
                                    for r in table.rows],
                                  lag_ratio=0.3), run_time=0.7)
            login = VGroup(
                caption("at login: hash again, compare", FG, size=SMALL - 3),
                check_mark(PLAIN, 0.3),
            ).arrange(RIGHT, buff=0.25).move_to(DOWN * 2.4)
            self.play(FadeIn(login), run_time=0.45)
            self.store = VGroup(table, recipe, login)

            self.play(FadeOut(self.store, shift=UP * 0.4), run_time=0.4)
            rows = VGroup()
            for text, digest in ((MSG, SHA_MSG), (MSG_TAMPERED, SHA_TAMPERED)):
                label = mono(f'"{text}"', PLAIN, size=SMALL)
                arrow = Arrow(ORIGIN, RIGHT * 1.0, color=FG, buff=0,
                              stroke_width=4)
                hexes = HexText(digest, FG, width=32, size=SMALL - 3)
                rows.add(VGroup(label, arrow, hexes).arrange(RIGHT, buff=0.3))
            rows.arrange(DOWN, buff=1.0).move_to(UP * 0.2)
            head = caption("SHA-256", ALGO, size=LABEL).move_to(UP * 2.4)
            self.play(FadeIn(head), run_time=0.25)
            self.play(FadeIn(rows[0]), run_time=0.35)
            self.play(FadeIn(rows[1]), run_time=0.35)

            # One character in, almost every character out.
            changed = diff_positions()
            self.play(
                rows[1][0][7].animate.set_color(CIPHER),
                *[rows[1][2].char(i).animate.set_color(CIPHER)
                  for i in changed],
                run_time=0.7,
            )
            count = caption(f"{len(changed)} of 64 characters differ", CIPHER,
                            size=SMALL - 2)
            count.move_to(DOWN * 2.3)
            self.play(Write(count), run_time=0.55)
            self.avalanche = VGroup(head, rows, count)

        with self.beat(5.31, "Digital signatures are related to public-key "
                            "cryptography as well, but they serve a different "
                            "purpose."):
            self.play(FadeOut(self.avalanche, shift=UP * 0.4), run_time=0.5)
            maya = Person(FG, height=1.6, name="Maya").move_to(LEFT * 4.6)
            pair = VGroup(Key(PRIVATE, height=0.5), Key(PUBLIC, height=0.5))
            pair.arrange(RIGHT, buff=0.9).next_to(maya.figure, RIGHT, buff=0.9)
            tags = VGroup(
                caption("Maya's private", PRIVATE, size=SMALL - 3)
                .next_to(pair[0], DOWN, buff=0.22),
                caption("Maya's public", PUBLIC, size=SMALL - 3)
                .next_to(pair[1], DOWN, buff=0.22),
            )
            self.play(FadeIn(maya, shift=RIGHT * 0.3), run_time=0.6)
            self.play(FadeIn(pair, scale=0.7), FadeIn(tags), run_time=0.9)
            self.wait(1.2)
            self.owner = VGroup(maya, pair, tags)

        with self.beat(3.03, "Encryption is mainly used to protect "
                            "confidentiality,"):
            lock = Padlock(PRIVATE, height=1.2).move_to(RIGHT * 3.6 + UP * 0.4)
            label = caption("CONFIDENTIALITY", PRIVATE, size=SMALL)
            label.next_to(lock, DOWN, buff=0.35)
            self.play(stamp_anim(lock, run_time=0.7), run_time=0.8)
            self.play(Write(label), run_time=0.8)
            self.conf = VGroup(lock, label)

        with self.beat(5.87, "while digital signatures help verify the "
                            "identity of the sender and confirm that the "
                            "message has not been modified."):
            self.play(FadeOut(self.owner, self.conf, shift=UP * 0.4),
                      run_time=0.5)
            flow = SignatureFlow(width=10.4).scale(0.92).move_to(UP * 0.6)
            self.play(flow.build_anim(run_time=1.9))
            self.play(Indicate(flow.sign_key, scale_factor=1.3, color=PRIVATE),
                      run_time=0.5)
            self.play(Indicate(flow.verify_key, scale_factor=1.3,
                               color=PUBLIC), run_time=0.5)
            ok = check_mark(PLAIN, height=0.55)
            ok.next_to(flow.station("verify"), RIGHT, buff=0.4)
            ok_tag = caption("untouched, and really from Maya", PLAIN,
                             size=SMALL - 3)
            ok_tag.next_to(flow, DOWN, buff=0.7)
            self.play(GrowFromCenter(ok), Write(ok_tag), run_time=0.7)

            # The same flow over an altered message fails at the last step.
            self.play(FadeOut(ok, ok_tag), run_time=0.25)
            tampered = caption("one byte changed", CIPHER, size=SMALL - 3)
            tampered.next_to(flow.station("message"), DOWN, buff=0.45)
            bad = cross_mark(CIPHER, height=0.55)
            bad.next_to(flow.station("verify"), RIGHT, buff=0.4)
            bad_tag = caption("verification fails", CIPHER, size=SMALL - 3)
            bad_tag.next_to(flow, DOWN, buff=0.7)
            self.play(Write(tampered),
                      flow.station("message")[0].animate.set_stroke(CIPHER),
                      run_time=0.5)
            self.play(GrowFromCenter(bad), Write(bad_tag), run_time=0.6)
            self.sig = VGroup(flow, tampered, bad, bad_tag)

        with self.beat(1.0, "(transition)"):
            self.play(
                FadeOut(self.sig, scale=0.8),
                ReplacementTransform(tag, tag_for(3)),
                run_time=1.0,
            )

        self.pad_to_target()


# --- 11. Web, messaging and storage (5:25-6:29) ----------------------------


class Scene11Applications(MovingVideoScene):
    """HTTPS, end-to-end messaging, and encryption at rest."""

    TARGET = 51.55

    def construct(self):
        self.add(tag_for(3, self))

        with self.beat(2.0, "(music only)"):
            card = chapter_card(3, "Applications of Encryption")
            self.play(FadeIn(card, shift=UP * 0.3), run_time=0.7)
            self.wait(0.5)
            self.play(FadeOut(card, shift=UP * 0.3), run_time=0.5)

        with self.beat(2.54, "Encryption is used throughout everyday "
                            "computing."):
            hub = Padlock(PRIVATE, height=1.4).move_to(ORIGIN)
            self.play(GrowFromCenter(hub), run_time=0.5)
            ring = VGroup(*[
                tech_icon(kind, PUBLIC, height=0.85)
                for kind in ("chat", "card", "cloud", "usb", "bank", "email")
            ])
            for i, item in enumerate(ring):
                angle = PI / 2 + TAU * i / len(ring)
                item.move_to(3.0 * np.array([np.cos(angle) * 1.5,
                                             np.sin(angle), 0]))
            spokes = VGroup(*[
                Line(hub.get_center(), item.get_center(), color=PUBLIC,
                     stroke_width=2, stroke_opacity=0.4)
                for item in ring
            ])
            self.play(
                LaggedStart(*[
                    AnimationGroup(Create(sp), FadeIn(ic, scale=0.6))
                    for sp, ic in zip(spokes, ring)
                ], lag_ratio=0.12), run_time=1.6,
            )
            self.constellation = VGroup(hub, ring, spokes)

        bar = BrowserBar("https://example.com", width=6.0)
        with self.beat(5.9, "One of the most familiar examples is HTTPS, "
                            "which protects communication between a web "
                            "browser and a website."):
            self.play(FadeOut(self.constellation, scale=0.7), run_time=0.5)
            bar.move_to(UP * 0.4)
            self.play(FadeIn(bar, shift=DOWN * 0.3), run_time=0.7)
            self.play(self.camera.frame.animate.scale(0.5).move_to(bar),
                      run_time=1.0)
            self.play(Indicate(bar.lock, scale_factor=1.4, color=PRIVATE),
                      run_time=0.8)
            self.wait(0.4)
            self.play(self.camera.frame.animate.scale(2.0).move_to(ORIGIN),
                      run_time=0.9)
            meaning = caption("encrypted between the browser and the site",
                              PLAIN, size=SMALL - 2)
            meaning.next_to(bar, DOWN, buff=0.6)
            self.play(Write(meaning), run_time=0.9)
            self.bar_bits = VGroup(bar, meaning)

        with self.beat(9.3, "When a website uses HTTPS, information such as "
                             "login credentials, personal information, and "
                             "payment information is encrypted while "
                             "traveling across the internet."):
            self.play(FadeOut(self.bar_bits, shift=UP * 0.4), run_time=0.5)
            net = NetworkMap(cols=5, rows=3, spacing=1.6, seed=9)
            net.scale(0.88).move_to(UP * 0.4)
            self.play(Create(net.lines, lag_ratio=0.05),
                      FadeIn(net.dots, lag_ratio=0.05), run_time=0.8)
            observers = VGroup(*[
                Snooper(height=0.7).move_to(net.at(i, j) + DOWN * 0.5)
                for i, j in ((1, 2), (3, 0))
            ])
            self.play(FadeIn(observers, lag_ratio=0.3), run_time=0.5)

            route = net.path([(0, 1), (1, 2), (2, 1), (3, 0), (4, 1)])
            # One packet per item in the sentence, each locking as it leaves.
            for kind, label in (("password", "login"), ("id", "personal"),
                                ("card", "payment")):
                packet = tech_icon(kind, PLAIN, height=0.55)
                packet.move_to(route.get_start())
                tag = caption(label, PLAIN, size=SMALL - 5)
                tag.next_to(packet, DOWN, buff=0.14)
                group = VGroup(packet, tag)
                self.play(FadeIn(group, scale=0.6), run_time=0.3)
                self.play(
                    packet.animate.set_color(CIPHER),
                    tag.animate.set_color(CIPHER),
                    Flash(packet, color=CIPHER, line_length=0.1,
                          flash_radius=0.35),
                    run_time=0.35,
                )
                self.play(MoveAlongPath(group, route), run_time=1.25)
                self.play(FadeOut(group, scale=0.6), run_time=0.22)
            blind = caption("every hop sees only ciphertext", SNOOP,
                            size=SMALL - 2)
            blind.move_to(DOWN * 2.6)
            self.play(Write(blind), run_time=0.7)
            self.web = VGroup(net, observers, blind)

        phone_a = Phone(FG, height=2.3).move_to(LEFT * 4.8)
        phone_b = Phone(FG, height=2.3).move_to(RIGHT * 4.8)
        relay = Server(SNOOP, height=2.0).move_to(ORIGIN + UP * 0.1)
        relay_tag = caption("provider", SNOOP, size=SMALL)
        relay_tag.next_to(relay, DOWN, buff=0.25)

        with self.beat(3.04, "Encryption is also used in messaging "
                            "applications."):
            self.play(FadeOut(self.web, shift=UP * 0.4), run_time=0.5)
            self.play(FadeIn(phone_a, shift=RIGHT * 0.3),
                      FadeIn(phone_b, shift=LEFT * 0.3),
                      FadeIn(relay, relay_tag), run_time=1.0)

        with self.beat(6.57, "End-to-end encryption is designed so that a "
                            "message is encrypted on the sender’s device "
                            "and only decrypted on the recipient’s "
                            "device."):
            wire = Line(phone_a.get_right() + RIGHT * 0.2,
                        phone_b.get_left() + LEFT * 0.2, color=PUBLIC,
                        stroke_width=2.5, stroke_opacity=0.5)
            self.play(Create(wire), run_time=0.5)

            msg = Note(MSG, PLAIN, size=SMALL - 3).scale(0.62)
            msg.move_to(phone_a.screen.get_center())
            self.play(FadeIn(msg, scale=0.6), run_time=0.5)
            lock = Padlock(PRIVATE, height=0.34)
            lock.next_to(msg, DOWN, buff=0.14)
            self.play(stamp_anim(lock, run_time=0.6),
                      msg.label.animate.set_color(CIPHER))

            sealed = VGroup(msg, lock)
            self.play(sealed.animate.move_to(relay.get_center() + UP * 0.1),
                      run_time=1.05)
            self.play(Indicate(sealed, scale_factor=1.08, color=CIPHER),
                      run_time=0.6)
            self.play(sealed.animate.move_to(phone_b.screen.get_center()),
                      run_time=1.05)
            self.play(lock.unlock_anim(),
                      msg.label.animate.set_color(PLAIN), run_time=0.5)

            brace_line = Line(phone_a.get_bottom() + DOWN * 0.4,
                              phone_b.get_bottom() + DOWN * 0.4,
                              color=PLAIN, stroke_width=2.5)
            e2e = caption("END-TO-END", PLAIN, size=SMALL)
            e2e.next_to(brace_line, DOWN, buff=0.22)
            self.play(Create(brace_line), Write(e2e), run_time=0.8)
            self.e2e = VGroup(wire, sealed, brace_line, e2e)

        with self.beat(5.0, "Ideally, even the messaging provider cannot read "
                            "the contents of the message while it is in "
                            "transit."):
            staff = Person(SNOOP, height=1.1)
            staff.next_to(relay, LEFT, buff=0.5).shift(DOWN * 0.3)
            self.play(FadeIn(staff, shift=RIGHT * 0.3), run_time=0.6)
            blob = Note(scrambled(MSG, seed=17), CIPHER, size=SMALL - 3)
            blob.scale(0.62).move_to(relay.get_center() + UP * 0.1)
            self.play(FadeIn(blob, scale=0.7), run_time=0.5)
            question = Text("?", font_size=46, color=SNOOP)
            question.next_to(staff, UP, buff=0.15)
            self.play(FadeIn(question, scale=0.5),
                      Rotate(staff, 0.2, about_point=staff.get_bottom(),
                             rate_func=there_and_back), run_time=0.9)
            self.wait(1.4)
            cant = caption("ciphertext in, ciphertext out", SNOOP,
                           size=SMALL - 2)
            cant.move_to(UP * 2.6)
            self.play(Write(cant), run_time=0.9)
            self.provider = VGroup(staff, blob, question, cant)

        shelf = VGroup()
        with self.beat(2.72, "Another major application is data storage."):
            self.play(FadeOut(phone_a, phone_b, relay, relay_tag, self.e2e,
                              self.provider, shift=DOWN * 0.4), run_time=0.6)
            board = Line(LEFT * 5.4, RIGHT * 5.4, color=FG, stroke_width=4)
            board.move_to(DOWN * 1.5)
            legs = VGroup(
                Line(board.get_left() + RIGHT * 0.6,
                     board.get_left() + RIGHT * 0.6 + DOWN * 0.7,
                     color=FG, stroke_width=4),
                Line(board.get_right() + LEFT * 0.6,
                     board.get_right() + LEFT * 0.6 + DOWN * 0.7,
                     color=FG, stroke_width=4),
            )
            shelf.add(board, legs)
            self.play(Create(board), Create(legs), run_time=0.9)

        devices = VGroup(
            labelled(Laptop(PUBLIC, height=1.3), "computers", FG, size=SMALL - 3),
            labelled(Phone(PUBLIC, height=1.4), "smartphones", FG, size=SMALL - 3),
            labelled(tech_icon("usb", PUBLIC, height=1.3), "USB drives", FG,
                     size=SMALL - 3),
            labelled(tech_icon("cloud", PUBLIC, height=1.1), "cloud services",
                     FG, size=SMALL - 3),
        ).arrange(RIGHT, buff=1.1)
        devices.next_to(shelf[0], UP, buff=0.3)

        with self.beat(5.14, "Computers, smartphones, USB drives, and cloud "
                            "services can encrypt stored files."):
            locks = VGroup()
            for item in devices:
                self.play(FadeIn(item, shift=UP * 0.3, scale=0.85),
                          run_time=0.35)
                lock = Padlock(PRIVATE, height=0.4)
                lock.move_to(item[0].get_center() + DOWN * 0.1)
                locks.add(lock)
                self.play(stamp_anim(lock, run_time=0.4))
                self.wait(0.3)
            self.locks = locks

        with self.beat(2.28, "This is called encryption at rest."):
            at_rest = caption("AT REST", PRIVATE, size=LABEL)
            at_rest.next_to(shelf[0], DOWN, buff=0.75)
            self.play(Write(at_rest), run_time=0.8)
            # The contrast the term only makes sense against.
            inset = VGroup(
                tech_icon("card", CIPHER, height=0.3),
                Arrow(ORIGIN, RIGHT * 0.5, color=SNOOP, buff=0,
                      stroke_width=2.5),
                tech_icon("cloud", CIPHER, height=0.3),
            ).arrange(RIGHT, buff=0.15)
            in_transit = VGroup(inset, caption("IN TRANSIT", SNOOP,
                                               size=SMALL - 4))
            in_transit.arrange(DOWN, buff=0.15)
            frame = RoundedRectangle(
                width=in_transit.width + 0.5, height=in_transit.height + 0.4,
                corner_radius=0.1, color=SNOOP, stroke_width=2,
                stroke_opacity=0.6, fill_color=SURFACE, fill_opacity=1,
            ).move_to(in_transit)
            inset_box = VGroup(frame, in_transit).to_corner(DR, buff=0.5)
            self.play(FadeIn(inset_box, shift=LEFT * 0.3), run_time=0.8)
            self.rest = VGroup(at_rest, inset_box)

        with self.beat(6.06, "If a device is lost or stolen, encryption can "
                             "make it much more difficult for someone to "
                             "access the information stored on it."):
            self.play(FadeOut(devices[1:], self.locks[1:], self.rest,
                              shift=UP * 0.3), run_time=0.6)
            laptop_group = devices[0]
            self.play(
                laptop_group.animate.scale(1.6).move_to(LEFT * 2.6 + UP * 0.3),
                self.locks[0].animate.scale(1.6).move_to(LEFT * 2.6 + UP * 0.15),
                FadeOut(shelf), run_time=0.8,
            )

            hand = GrabHand(SNOOP, height=1.8)
            hand.move_to(laptop_group.get_bottom() + DOWN * 2.2)
            self.play(FadeIn(hand, shift=UP * 0.5), run_time=0.7)
            taken = VGroup(laptop_group, self.locks[0])
            self.play(
                taken.animate.shift(RIGHT * 0.5 + UP * 0.2),
                hand.animate.shift(RIGHT * 0.5 + UP * 1.2),
                run_time=0.9,
            )

            drive = RoundedRectangle(
                width=4.6, height=2.6, corner_radius=0.16, color=CIPHER,
                stroke_width=STROKE_THIN, fill_color=SURFACE, fill_opacity=1,
            ).move_to(RIGHT * 3.6 + UP * 0.3)
            contents = HexText(
                (SHA_MSG + SHA_TAMPERED)[:96], CIPHER, width=24, size=SMALL - 4,
            ).move_to(drive)
            drive_tag = caption("what the drive actually holds", SNOOP,
                                size=SMALL - 3)
            drive_tag.next_to(drive, DOWN, buff=0.3)
            self.play(FadeIn(drive), run_time=0.5)
            self.play(contents.type_anim(per_char=0.008), run_time=1.4)
            self.play(Write(drive_tag), run_time=0.8)
            self.theft = VGroup(taken, hand, drive, contents, drive_tag)

        with self.beat(1.0, "(transition)"):
            bank = tech_icon("bank", FG, height=2.2).move_to(ORIGIN)
            self.play(FadeOut(self.theft, shift=LEFT * 0.6),
                      FadeIn(bank, shift=UP * 0.6), run_time=1.0)
            self.remove(bank)

        self.pad_to_target()


# --- 12. Banking, VPNs and organizations (6:29-7:10) -----------------------


class Scene12Organizations(MovingVideoScene):
    """Payments, the VPN tunnel and where it ends, and defence in depth."""

    TARGET = 39.87

    def construct(self):
        self.add(tag_for(3, self))

        bank = tech_icon("bank", FG, height=2.0).move_to(LEFT * 4.2 + UP * 0.3)
        terminal = tech_icon("terminal", FG, height=1.9)
        terminal.move_to(RIGHT * 4.2 + UP * 0.3)
        link = Line(bank.get_right() + RIGHT * 0.3,
                    terminal.get_left() + LEFT * 0.3,
                    color=PUBLIC, stroke_width=3)

        with self.beat(3.97, "Encryption is also important in online banking "
                            "and electronic payments."):
            self.play(FadeIn(bank, shift=RIGHT * 0.3),
                      FadeIn(terminal, shift=LEFT * 0.3), run_time=0.9)
            self.play(Create(link), run_time=0.7)
            lock = Padlock(PRIVATE, height=0.55).move_to(link.get_center())
            self.play(stamp_anim(lock, run_time=0.6))
            self.payments = VGroup(bank, terminal, link, lock)

        with self.beat(8.12, "Financial institutions use cryptographic "
                            "protocols to protect account information, "
                            "verify transactions, and reduce the risk of "
                            "unauthorized access."):
            self.play(self.payments.animate.scale(0.52).to_edge(UP, buff=0.55),
                      run_time=0.6)

            # One panel per clause, landing on its words.
            record = VGroup(tech_icon("file", PUBLIC, height=1.1),
                            Padlock(PRIVATE, height=0.5))
            record[1].move_to(record[0].get_center())
            panel1 = labelled(record, "account information", FG, size=SMALL - 4)

            txn = VGroup(
                tech_icon("card", PUBLIC, height=0.9),
                check_mark(PLAIN, 0.4),
            ).arrange(RIGHT, buff=0.25)
            panel2 = labelled(txn, "verify transactions", FG, size=SMALL - 4)

            shield = tech_icon("shield", PLAIN, height=1.2)
            intruder = Eve(height=0.9, named=False)
            intruder.next_to(shield, LEFT, buff=0.35)
            panel3 = labelled(VGroup(shield, intruder),
                              "block unauthorized access", FG, size=SMALL - 4)

            panels = VGroup(panel1, panel2, panel3)
            panels.arrange(RIGHT, buff=1.3).move_to(DOWN * 0.7)
            for panel in panels:
                self.play(FadeIn(panel, shift=UP * 0.3, scale=0.85),
                          run_time=0.5)
                self.wait(1.3)
            self.play(
                intruder.animate.shift(LEFT * 0.4),
                Flash(shield, color=PLAIN, line_length=0.15, flash_radius=0.7),
                run_time=0.6,
            )
            self.panels = panels

        with self.beat(6.87, "Virtual private networks, or VPNs, use "
                            "encryption to protect data traveling between a "
                            "device and a VPN server."):
            self.play(FadeOut(self.payments, self.panels, shift=UP * 0.4),
                      run_time=0.5)
            laptop = Laptop(FG, height=1.7).move_to(LEFT * 4.9 + DOWN * 1.0)
            cafe = caption("public Wi-Fi", SNOOP, size=SMALL - 2)
            cafe.next_to(laptop, DOWN, buff=0.3)
            vpn = VGroup(Server(FG, height=1.9), tech_icon("vpn", PLAIN, 0.7))
            vpn[1].move_to(vpn[0].get_center())
            vpn.move_to(RIGHT * 0.6 + DOWN * 1.0)
            vpn_tag = caption("VPN server", PLAIN, size=SMALL - 2)
            vpn_tag.next_to(vpn, DOWN, buff=0.3)
            self.play(FadeIn(laptop, cafe, shift=RIGHT * 0.3),
                      FadeIn(vpn, vpn_tag, shift=LEFT * 0.3), run_time=0.9)

            tube = Tunnel(laptop.get_right() + RIGHT * 0.25,
                          vpn.get_left() + LEFT * 0.25, bow=0.45)
            self.play(tube.draw_anim(run_time=1.3))
            tube_tag = caption("encrypted tunnel", PRIVATE, size=SMALL - 3)
            tube_tag.next_to(tube, UP, buff=0.3)
            self.play(FadeIn(tube_tag), run_time=0.4)
            for _ in range(2):
                parcel = data_record(PRIVATE, width=0.38)
                self.play(tube.flow_anim(parcel, run_time=1.2))
                self.remove(parcel)
            self.vpn_bits = VGroup(laptop, cafe, vpn, vpn_tag, tube, tube_tag)

        with self.beat(4.52, "This can help prevent people on the same network "
                            "from easily viewing the user’s traffic."):
            snoop = Snooper(height=1.3).move_to(LEFT * 3.4 + UP * 1.9)
            self.play(FadeIn(snoop, shift=DOWN * 0.3), run_time=0.5)
            sees = caption("sees only the tunnel", SNOOP, size=SMALL - 3)
            sees.next_to(snoop, UP, buff=0.2)
            self.play(Write(sees),
                      Wiggle(snoop, scale_value=1.06), run_time=0.9)

            # Where the protection stops, said plainly: the plan asks for it.
            onward = Line(self.vpn_bits[2].get_right() + RIGHT * 0.3,
                          RIGHT * 5.6 + DOWN * 1.0, color=SNOOP,
                          stroke_width=2.5)
            web = tech_icon("cloud", SNOOP, height=0.9)
            web.move_to(RIGHT * 6.0 + DOWN * 1.0)
            ends = caption("protection ends here", SNOOP, size=SMALL - 3)
            ends.next_to(onward, UP, buff=0.25)
            self.play(Create(onward), FadeIn(web), run_time=0.7)
            self.play(Write(ends), run_time=0.7)
            parcel = data_record(SNOOP, width=0.38)
            self.play(MoveAlongPath(parcel, onward), run_time=0.9)
            self.remove(parcel)
            self.snoop_bits = VGroup(snoop, sees, onward, web, ends)

        folders = VGroup()
        with self.beat(7.68, "Businesses and governments use encryption to "
                            "protect confidential records, intellectual "
                            "property, medical data, and classified "
                            "information."):
            self.play(FadeOut(self.vpn_bits, self.snoop_bits, shift=UP * 0.4),
                      run_time=0.5)
            for name in ("confidential\nrecords", "intellectual\nproperty",
                         "medical\ndata", "classified\ninformation"):
                folder = Folder(PUBLIC, height=1.3)
                label = caption(name, FG, size=SMALL - 4)
                label.next_to(folder, DOWN, buff=0.22)
                folders.add(VGroup(folder, label))
            folders.arrange(RIGHT, buff=0.9).move_to(UP * 0.1)
            stamps = VGroup()
            for item in folders:
                self.play(FadeIn(item, shift=UP * 0.3, scale=0.85),
                          run_time=0.42)
                stamp = Padlock(PRIVATE, height=0.42)
                stamp.move_to(item[0].shell.get_center())
                stamps.add(stamp)
                self.play(stamp_anim(stamp, run_time=0.38))
                self.wait(0.75)
            self.folders = VGroup(folders, stamps)

        rings = DefenseRings(
            ["encryption", "access control", "authentication", "monitoring"],
            inner=1.3, step=0.78,
        ).scale(0.78)

        with self.beat(7.71, "In these environments, encryption is often "
                            "combined with access controls, authentication, "
                            "monitoring, and other security measures."):
            # Drop the captions as the folders shrink: at ring scale they
            # are three unreadable pixels of grey, which reads as dirt.
            self.play(
                FadeOut(VGroup(*[item[1] for item in self.folders[0]])),
                self.folders.animate.scale(0.38).move_to(ORIGIN),
                run_time=0.7,
            )
            rings.move_to(ORIGIN)
            self.play(rings.draw_anim(run_time=3.4))
            self.wait(1.2)
            self.rings = rings

        with self.beat(1.0, "(transition)"):
            gaps = rings.gaps(3)
            self.play(
                self.camera.frame.animate.scale(1.25),
                LaggedStart(*[
                    AnimationGroup(GrowFromCenter(g),
                                   Flash(g, color=CIPHER, line_length=0.12,
                                         flash_radius=0.3))
                    for g in gaps
                ], lag_ratio=0.2),
                run_time=1.0,
            )
            self.gaps = gaps

        self.pad_to_target()


# --- 13. Limits and conclusion (7:10-8:00) ---------------------------------


class Scene13Conclusion(MovingVideoScene):
    """What encryption does not do, the three goals, and the end card."""

    TARGET = 45.43

    def construct(self):
        self.add(tag_for(3, self))

        # Scene 12 ended pulled back on the rings with their gaps showing.
        self.camera.frame.scale(1.25)
        rings = DefenseRings(
            ["encryption", "access control", "authentication", "monitoring"],
            inner=1.3, step=0.78,
        ).scale(0.78).move_to(ORIGIN)
        gaps = rings.gaps(3)
        self.add(rings, gaps)

        with self.beat(3.28, "However, encryption does not solve every "
                            "security problem."):
            spots = VGroup(*[
                Circle(radius=0.55, color=CIPHER, stroke_width=2.5,
                       fill_color=CIPHER, fill_opacity=0.12).move_to(g)
                for g in gaps
            ])
            self.play(LaggedStart(*[GrowFromCenter(s) for s in spots],
                                  lag_ratio=0.25), run_time=1.3)
            self.play(LaggedStart(*[
                Indicate(s, scale_factor=1.25, color=CIPHER) for s in spots
            ], lag_ratio=0.2), run_time=1.3)
            self.outer = VGroup(rings, gaps, spots)

        with self.beat(3.76, "It cannot protect data from a person who already "
                            "has authorized access,"):
            self.play(FadeOut(self.outer, scale=0.8),
                      self.camera.frame.animate.scale(1 / 1.25), run_time=0.6)
            insider = Person(FG, height=1.7, name="authorized user")
            insider.move_to(LEFT * 3.0)
            badge = Key(PRIVATE, height=0.42)
            badge.next_to(insider.figure, RIGHT, buff=0.35).shift(UP * 0.2)
            folder = Folder(PUBLIC, height=1.6).move_to(RIGHT * 2.6)
            lock = Padlock(PRIVATE, height=0.5)
            lock.move_to(folder.shell.get_center())
            self.play(FadeIn(insider, badge, shift=RIGHT * 0.3),
                      FadeIn(folder, lock, shift=LEFT * 0.3), run_time=0.8)
            self.play(badge.animate.next_to(lock, LEFT, buff=0.2),
                      run_time=0.7)
            self.play(lock.unlock_anim(), run_time=0.5)
            opens = caption("encryption has no opinion about this", SNOOP,
                            size=SMALL - 2)
            opens.move_to(DOWN * 2.3)
            self.play(Write(opens), run_time=1.0)
            self.insider = VGroup(insider, badge, folder, lock, opens)

        with self.beat(4.49, "and it cannot prevent every type of malware, "
                            "phishing attack, or social-engineering attack."):
            self.play(FadeOut(self.insider, shift=UP * 0.4), run_time=0.5)
            phish = VGroup(tech_icon("email", SNOOP, height=1.0),
                           tech_icon("hook", CIPHER, height=0.9))
            phish[1].next_to(phish[0], RIGHT, buff=-0.25).shift(UP * 0.2)
            threats = VGroup(
                labelled(tech_icon("bug", SNOOP, height=1.1), "malware", FG),
                labelled(phish, "phishing", FG),
                labelled(tech_icon("call", SNOOP, height=1.1),
                         "social engineering", FG),
            ).arrange(RIGHT, buff=1.4).move_to(UP * 0.1)
            for threat in threats:
                self.play(FadeIn(threat, shift=UP * 0.3, scale=0.85),
                          run_time=0.4)
                self.wait(0.75)
            self.threats = threats

        with self.beat(5.18, "Encryption protects the information. The "
                             "surrounding systems and users must also be "
                             "secure."):
            self.play(FadeOut(self.threats, shift=UP * 0.4), run_time=0.5)
            box = Box(FG, width=2.4, height=1.7)
            lock = Padlock(PRIVATE, height=0.6)
            lock.move_to(box.body.get_center())
            core = VGroup(box, lock).move_to(ORIGIN)
            self.play(FadeIn(core, scale=0.8), run_time=0.7)
            machine = labelled(Laptop(SNOOP, height=1.5), "the system", SNOOP)
            machine.move_to(LEFT * 4.2)
            people = labelled(Person(SNOOP, height=1.6), "the people", SNOOP)
            people.move_to(RIGHT * 4.2)
            self.play(FadeIn(machine, shift=RIGHT * 0.3),
                      FadeIn(people, shift=LEFT * 0.3), run_time=0.9)
            surround = DashedVMobject(
                Ellipse(width=11.0, height=5.2, color=SNOOP, stroke_width=2.5),
                num_dashes=40, dashed_ratio=0.5,
            )
            self.play(Create(surround), run_time=1.3)
            also = caption("encryption is one layer, not the whole system",
                           SNOOP, size=SMALL - 2)
            also.move_to(DOWN * 3.1)
            self.play(Write(also), run_time=1.0)
            self.system = VGroup(core, machine, people, surround, also)

        pillars = VGroup(
            Pillar("CONFIDENTIALITY", PRIVATE),
            Pillar("INTEGRITY", PUBLIC),
            Pillar("AUTHENTICATION", PLAIN),
        ).arrange(RIGHT, buff=0.75).scale(0.9).move_to(UP * 0.2)

        with self.beat(6.62, "Overall, encryption supports three major "
                            "security goals: confidentiality, integrity, and "
                            "authentication."):
            self.play(FadeOut(self.system, shift=DOWN * 0.4), run_time=0.6)
            for pillar in pillars:
                self.play(GrowFromEdge(pillar.shell, DOWN),
                          FadeIn(pillar.label, shift=UP * 0.2), run_time=0.55)
                self.wait(0.6)

        with self.beat(7.22, "It helps keep information private, helps detect "
                            "unauthorized changes, and can help verify the "
                            "identity of the people or systems involved."):
            # Each pillar lights up with the icon it earned earlier in the
            # video: the padlock from scene 2, the changed hash and the
            # signature tick from scene 10.
            padlock = Padlock(PRIVATE, height=0.9)
            padlock.move_to(pillars[0].body_at())

            changed = VGroup(
                Text("96af04…", font=MONO, font_size=SMALL - 3, color=FG),
                Text("5bf79f…", font=MONO, font_size=SMALL - 3, color=CIPHER),
            ).arrange(DOWN, buff=0.22)
            changed.move_to(pillars[1].body_at())

            signature = VGroup(Key(PUBLIC, height=0.42),
                               check_mark(PLAIN, height=0.5))
            signature.arrange(RIGHT, buff=0.3)
            signature.move_to(pillars[2].body_at())

            lines = (
                "keeps information\nprivate",
                "detects unauthorized\nchanges",
                "verifies who\nsent it",
            )
            for pillar, art, line in zip(pillars, (padlock, changed, signature),
                                         lines):
                sub = caption(line, pillar.label.color, size=SMALL - 4)
                sub.next_to(pillar.label, DOWN, buff=0.22)
                self.play(
                    pillar.fill_anim(1.0, run_time=0.6),
                    FadeIn(art, scale=0.7), FadeIn(sub, shift=UP * 0.15),
                    run_time=0.8,
                )
                self.wait(1.5)
                pillars.add(sub)
            self.goals = VGroup(pillars, padlock, changed, signature)

        globe = NetworkGlobe(radius=2.2).move_to(ORIGIN)
        with self.beat(8.88, "As more communications, commerce, and personal "
                            "activity move online, encryption has become a "
                            "fundamental part of modern computer science and "
                            "cybersecurity."):
            self.play(FadeOut(self.goals, scale=0.4), run_time=0.8)
            self.play(Create(globe.shell, lag_ratio=0.15), run_time=1.4)
            self.play(
                LaggedStart(*[GrowFromCenter(d) for d in globe.dots],
                            lag_ratio=0.12),
                run_time=1.2,
            )
            self.play(Create(globe.links, lag_ratio=0.15), run_time=1.0)

            # The video's own icons, settling into orbit around it.
            orbit = VGroup(*[
                tech_icon(kind, PUBLIC, height=0.6)
                for kind in ("chat", "card", "bank", "cloud", "hospital",
                             "government")
            ])
            for i, item in enumerate(orbit):
                angle = PI / 2 + TAU * i / len(orbit)
                item.move_to(4.6 * np.array([np.cos(angle) * 1.25,
                                             np.sin(angle) * 0.72, 0]))
            self.play(
                LaggedStart(*[FadeIn(o, scale=0.6) for o in orbit],
                            lag_ratio=0.12),
                globe.spin_anim(run_time=2.4),
                run_time=2.4,
            )
            self.globe_bits = VGroup(globe, orbit)

        with self.beat(6.0, "(music only)"):
            self.play(FadeOut(self.globe_bits, scale=0.5), run_time=0.8)
            key = Key(PRIVATE, height=1.0)
            word = title("Encryption")
            logo = VGroup(key, word).arrange(RIGHT, buff=0.5)
            logo.to_edge(UP, buff=0.65)
            self.play(DrawBorderThenFill(key), run_time=0.7)
            self.play(Write(word), run_time=0.8)

            tail = VGroup(
                caption(CREDITS_CLASS, SNOOP, size=SMALL - 3),
                caption(CREDITS_TOOLS, SNOOP, size=SMALL - 4),
            ).arrange(DOWN, buff=0.18)
            credits = VGroup(team_logo(), team_roster(), tail)
            credits.arrange(DOWN, buff=0.55)
            credits.next_to(logo, DOWN, buff=0.6)
            self.play(FadeIn(credits, shift=UP * 0.3, lag_ratio=0.2),
                      run_time=1.4)
            self.wait(1.2)
            self.play(FadeOut(logo, credits, run_time=0.9))

        self.pad_to_target()
