"""The thirteen scenes of the encryption video.

Scenes A to C are Part 1 — why it matters, and a short history. Scenes 1 to
10 are Part 2 — how encryption works. The letters keep Part 2's numbering,
and the audio named after it, unchanged now that Part 1 sits in front.

Each class is one scene of encryption-video-plan.md, and each
``with self.beat(seconds, "...")`` block is one row of that scene's beat
table: the narration for the window, and what is on screen while it is
spoken. The block holds the last frame until the window is full, so the cut
stays on the plan's clock whatever the animations inside cost.

Render one scene while iterating:

    .venv/bin/manim -ql --disable_caching scenes.py Scene02Ciphertext

Render the whole video and stitch it:  ./render.sh
"""

from __future__ import annotations

from pathlib import Path

from manim import *

from assets import *
from part1_assets import *
from style import *

# The end card in Scene10Outro.
CREDITS_LOGO = Path(__file__).resolve().parent.parent / "team_logo.svg"
CREDITS_TEAM = (
    ("Michael Ansara", "Script Writer"),
    ("Eric Griffin", "Video Editor"),
    ("Kenneth Joyce", "Script Writer"),
    ("Chris Mobley", "Animator"),
    ("Derrick Patterson", "Narrator"),
)
CREDITS_CLASS = "CST 349"
CREDITS_TOOLS = "Animated with manim.community"


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


def team_roster(size: int = 21) -> VGroup:
    """Who did what: names in one column, roles in the one beside it.

    Each column is one multi-line Text rather than a row of them, so the
    five rows share a single set of baselines however long the names and
    the roles run.
    """
    column = dict(font=SANS, font_size=size, line_spacing=0.6)
    names = Text("\n".join(n for n, _ in CREDITS_TEAM), color=FG, **column)
    roles = Text("\n".join(r for _, r in CREDITS_TEAM), color=SNOOP, **column)
    roles.next_to(names, RIGHT, buff=0.55).align_to(names, UP)
    return VGroup(names, roles)

MSG = "Meet at 3pm"


# --- Part 1: why it matters, and a short history ---------------------------
#
# Scenes A to C, lettered so that adding them in front of the cut left the
# existing scene numbers — and the audio already named after them — alone.
# Every window below is the length of the line as it was actually read.
#
# The timeline is the spine of Part 1. Each scene rebuilds it at the same
# place with the marker on the era it opens in, so it holds still across the
# three cuts and only moves when the narration moves.


def _timeline(stop: int = 0) -> HistoryTimeline:
    """The history line, parked at ``stop``, in the same spot every scene."""
    line = HistoryTimeline()
    line.to_edge(DOWN, buff=0.45)
    line.marker.next_to(line.ticks[stop], UP, buff=0.1)
    return line


def _city(seed: int = 11):
    """Maya, her phone, the network and the bank: the opening picture.

    Scene 1 of Part 2 opens on this same arrangement, so the picture carries
    across the join from Part 1 without a cut.
    """
    net = NetworkMap(cols=6, rows=4, spacing=1.15, seed=seed)
    net.scale(0.78).move_to(RIGHT * 2.7 + UP * 0.2)
    maya = Person(FG, height=1.9, name="Maya").move_to(LEFT * 5.1 + DOWN * 0.4)
    phone = Phone(height=1.05).next_to(maya.figure, RIGHT, buff=0.18)
    rays = VGroup(*[
        Line(phone.get_right(), net.at(0, j), color=PUBLIC,
             stroke_width=2.4, stroke_opacity=0.55)
        for j in range(4)
    ])
    return net, maya, phone, rays


# --- A. Why it matters (0:00-0:12) ---------------------------------------


class SceneAWhyItMatters(VideoScene):
    TARGET = 12.45

    def construct(self):
        with self.beat(2.0, "(music only)"):
            key = Key(PRIVATE, height=1.0)
            word = title("Encryption")
            logo = VGroup(key, word).arrange(RIGHT, buff=0.5).move_to(ORIGIN)
            self.play(DrawBorderThenFill(key), run_time=0.8)
            self.play(Write(word), run_time=0.7)
            self.play(logo.animate.scale(0.3).to_corner(UL).set_opacity(0),
                      run_time=0.45)
            self.remove(logo)

        net, maya, phone, rays = _city()
        bank = icon("bank", FG, 1.35).move_to(RIGHT * 5.9 + UP * 0.2)
        app = icon("bank", PUBLIC, 0.42).move_to(phone.screen.get_center())

        with self.beat(3.97, "When you check your bank account online, "
                             "information travels between your device and "
                             "the bank."):
            self.play(FadeIn(maya, shift=RIGHT * 0.4), FadeIn(phone, scale=0.8),
                      run_time=0.7)
            self.play(FadeIn(app, scale=0.6), run_time=0.4)
            self.play(FadeIn(bank, shift=LEFT * 0.4), run_time=0.5)
            self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.18),
                      run_time=0.7)
            self.play(Create(net.lines, lag_ratio=0.04),
                      FadeIn(net.dots, lag_ratio=0.04), run_time=1.0)
            tail = Line(net.at(5, 2), bank.get_left(), color=PUBLIC,
                        stroke_width=2.4, stroke_opacity=0.55)
            self.play(Create(tail), run_time=0.5)

        city = VGroup(net, rays, tail)
        route = net.path([(0, 1), (1, 2), (2, 2), (3, 1), (4, 1), (5, 2)])
        packet = Note("....", PLAIN, size=15).scale(0.62)
        packet.move_to(net.at(0, 1))

        with self.beat(1.59, "Encryption helps keep it private."):
            self.play(FadeIn(packet, scale=0.5), run_time=0.3)
            seal = Padlock(PRIVATE, 0.34)
            seal.move_to(packet.get_corner(UR))
            self.play(GrowFromCenter(seal),
                      Flash(seal, color=PRIVATE, flash_radius=0.3,
                            line_length=0.08), run_time=0.6)

        locked = VGroup(packet, seal)

        with self.beat(3.69, "Even if someone intercepts the data, they "
                            "shouldn't be able to read it without the right "
                            "key."):
            snoop = Snooper(height=1.15).move_to(net.at(3, 0) + DOWN * 0.35)
            self.play(FadeIn(snoop, shift=UP * 0.3), run_time=0.4)
            self.play(MoveAlongPath(locked, route), run_time=1.2)
            # the copy it takes away opens, and holds nothing readable
            stolen = locked.copy()
            self.add(stolen)
            self.play(stolen.animate.scale(1.5).move_to(
                snoop.get_center() + DOWN * 1.5), run_time=0.5)
            # The packet's card was cut for four dots; what is really inside
            # is a whole line, so the card grows to hold it as the seal goes.
            gibberish = scrambled("Meet at 3pm", seed=4)
            self.play(FadeOut(stolen[1], scale=0.4),
                      Transform(stolen[0].card,
                                stolen[0].fitted_card(gibberish)
                                .set_stroke(CIPHER)), run_time=0.2)
            scramble(self, stolen[0].label, steps=4, run_time=0.09,
                     settle=gibberish)
            q = title("?", SNOOP, 46).next_to(snoop, UP, buff=0.12)
            self.play(FadeIn(q, shift=UP * 0.25), run_time=0.4)

        with self.beat(1.2, "(transition)"):
            line = _timeline(0)
            self.play(
                FadeOut(city, maya, phone, app, bank, locked, stolen, snoop, q),
                run_time=0.6,
            )
            self.play(Create(line.axis), run_time=0.3)
            self.play(FadeIn(line.ticks, lag_ratio=0.1),
                      FadeIn(line.labels, lag_ratio=0.1),
                      FadeIn(line.marker, shift=DOWN * 0.2), run_time=0.5)

        self.pad_to_target()


# --- B. Caesar and Enigma (0:12-0:32) ------------------------------------


class SceneBCaesarEnigma(VideoScene):
    TARGET = 19.82

    def construct(self):
        line = _timeline(0)
        self.add(line)

        with self.beat(2.11, "Protecting messages isn't a new challenge."):
            scroll = icon("scroll", FG, 1.05).move_to(line.above(0, 1.2))
            self.play(FadeIn(scroll, shift=UP * 0.3, scale=0.7), run_time=0.9)

        rows = AlphabetShift(k=3).move_to(UP * 1.5)
        plain = mono("MEET", PLAIN, 40).move_to(LEFT * 3.2 + DOWN * 0.9)
        cipher = VGroup()

        with self.beat(3.34, "Julius Caesar used a cipher that shifted letters "
                             "along the alphabet."):
            self.play(FadeOut(scroll, scale=0.7), run_time=0.25)
            self.play(FadeIn(rows.top, lag_ratio=0.02), run_time=0.4)
            self.play(FadeIn(rows.bottom, lag_ratio=0.02), run_time=0.35)
            self.add(rows)
            tag = caption("shift 3", PRIVATE, 22).move_to(UP * 2.65)
            self.play(rows.slide(run_time=0.7), FadeOut(rows.leaving()),
                      FadeIn(tag), run_time=0.7)
            self.play(Write(plain), run_time=0.45)
            # MEET -> PHHW, one letter at a time, each from its own cell
            for i, ch in enumerate("MEET"):
                cell = rows.cipher(ch)
                letter = mono(cell.text, PRIVATE, 40)
                letter.move_to(plain.get_right() + RIGHT * (0.9 + i * 0.62))
                cipher.add(letter)
            self.play(LaggedStart(*[
                TransformFromCopy(rows.cipher(ch), letter)
                for ch, letter in zip("MEET", cipher)
            ], lag_ratio=0.12), run_time=0.8)

        with self.beat(3.41, "It could hide a message from a casual reader, "
                             "but it's easy to break now."):
            passer = Person(SNOOP, height=1.3).move_to(RIGHT * 4.6 + DOWN * 1.0)
            shrug = title("?", SNOOP, 40).next_to(passer, UP, buff=0.12)
            self.play(FadeIn(passer, shift=LEFT * 0.3), FadeIn(shrug),
                      run_time=0.6)
            lap = Laptop(FG, 1.7).move_to(RIGHT * 4.6 + DOWN * 1.0)
            self.play(FadeOut(passer, shrug, scale=0.8),
                      FadeIn(lap, scale=0.8), run_time=0.5)
            # every offset tried at once, and the readable one falls out
            trial = mono("PHHW", SNOOP, 22).move_to(lap.screen.get_center())
            self.add(trial)
            for n in range(1, 4):
                guess = "".join(
                    chr((ord(c) - 65 - n) % 26 + 65) for c in "PHHW")
                self.play(Transform(
                    trial, mono(guess, SNOOP, 22).move_to(trial)), run_time=0.13)
            out = mono("MEET", PLAIN, 34).move_to(RIGHT * 4.6 + UP * 0.45)
            self.play(ReplacementTransform(trial, out),
                      Flash(out, color=PLAIN, flash_radius=0.6), run_time=0.7)

        with self.beat(5.63, "During World War Two, German forces used Enigma "
                             "machines that changed how letters were scrambled "
                             "with every keystroke."):
            self.play(FadeOut(rows, plain, cipher, tag, lap, out), run_time=0.4)
            self.play(line.slide(1, run_time=0.6))
            mach = EnigmaRotors()
            mach.scale(0.92).move_to(UP * 1.25)
            self.play(FadeIn(mach.wheels, lag_ratio=0.2), run_time=0.5)
            self.play(FadeIn(mach.lamps, lag_ratio=0.02),
                      FadeIn(mach.letters, lag_ratio=0.02), run_time=0.5)
            pressed = caption("A", PLAIN, 30).next_to(mach, LEFT, buff=0.55)
            self.play(FadeIn(pressed, scale=0.6), run_time=0.3)
            # the same key, five times, and a different lamp every time
            for ch in "BDZGO":
                self.play(mach.step(run_time=0.26),
                          Indicate(pressed, color=PLAIN, scale_factor=1.2,
                                   run_time=0.26))
                self.play(mach.lit(ch), run_time=0.2)
                if ch != "O":
                    self.play(mach.dark(ch), run_time=0.14)

        with self.beat(4.33, "Polish mathematicians made early breakthroughs, "
                             "and Allied codebreakers built on that work."):
            self.play(FadeOut(pressed), run_time=0.2)
            poland = labelled(Person(FG, 1.05), "Poland", FG, 19)
            allies = labelled(Person(FG, 1.05), "Allied codebreakers", FG, 19)
            poland.move_to(LEFT * 4.5 + DOWN * 1.65)
            allies.move_to(RIGHT * 4.5 + DOWN * 1.65)
            self.play(FadeIn(poland, shift=RIGHT * 0.3),
                      FadeIn(allies, shift=LEFT * 0.3), run_time=0.7)
            book = VGroup(
                RoundedRectangle(width=0.72, height=0.52, corner_radius=0.06,
                                 color=PRIVATE, stroke_width=STROKE_THIN,
                                 fill_color=SURFACE, fill_opacity=1),
                Line(UP * 0.26, DOWN * 0.26, color=PRIVATE, stroke_width=2),
            ).next_to(poland, UP, buff=0.2)
            self.play(FadeIn(book, scale=0.6),
                      Flash(book, color=PRIVATE, flash_radius=0.4), run_time=0.5)
            hop = ArcBetweenPoints(book.get_center(),
                                   allies.get_top() + UP * 0.38, angle=-PI / 3)
            self.play(MoveAlongPath(book, hop), run_time=1.0)
            # the lit letters give the plaintext back
            self.play(mach.dark("O"), run_time=0.25)
            back = caption("A A A A A", PLAIN, 26)
            back.move_to(mach.lamps.get_center())
            self.play(FadeOut(mach.lamps, mach.letters, scale=0.85),
                      FadeIn(back, scale=0.8), run_time=0.7)

        with self.beat(1.0, "(transition)"):
            self.play(FadeOut(mach.wheels, back, poland, allies, book),
                      line.slide(2, run_time=0.8), run_time=0.8)

        self.pad_to_target()


# --- C. Computers and AES (0:32-0:56) ------------------------------------


class SceneCComputersAES(VideoScene):
    TARGET = 24.17

    def construct(self):
        line = _timeline(2)
        self.add(line)

        with self.beat(4.94, "As computers spread into everyday life, "
                             "encryption had to protect more than military "
                             "messages."):
            env = Envelope(FG, 1.15).move_to(UP * 1.6)
            mil = caption("military", SNOOP, 19).next_to(env, DOWN, buff=0.22)
            self.play(FadeIn(env, scale=0.7), FadeIn(mil), run_time=0.8)
            spread = VGroup(*[
                icon(k, FG, 0.92) for k in ("email", "card", "chat", "cart")
            ]).arrange(RIGHT, buff=1.25).move_to(UP * 1.5)
            self.play(FadeOut(mil), run_time=0.25)
            self.play(
                LaggedStart(*[TransformFromCopy(env, g) for g in spread],
                            lag_ratio=0.22),
                run_time=1.9,
            )
            self.play(FadeOut(env, scale=0.5), run_time=0.4)

        with self.beat(5.95, "In the nineteen seventies, researchers developed "
                             "new ways for computers to protect data and "
                             "establish shared keys."):
            self.play(FadeOut(spread, shift=UP * 0.3), run_time=0.4)
            era = heading("1970s", PRIVATE, 32).move_to(UP * 2.75)
            self.play(Write(era), run_time=0.5)
            left = Laptop(FG, 2.0).move_to(LEFT * 4.0 + UP * 0.9)
            right = Laptop(FG, 2.0).move_to(RIGHT * 4.0 + UP * 0.9)
            self.play(FadeIn(left, shift=RIGHT * 0.3),
                      FadeIn(right, shift=LEFT * 0.3), run_time=0.7)
            # first half of the sentence: the data itself is protected
            block = VGroup(*[
                Rectangle(width=1.5, height=0.26, color=PUBLIC,
                          stroke_width=STROKE_THIN, fill_color=SURFACE,
                          fill_opacity=1)
                for _ in range(3)
            ]).arrange(DOWN, buff=0.1).move_to(UP * 0.9)
            self.play(FadeIn(block, lag_ratio=0.2), run_time=0.6)
            clamp = Padlock(PRIVATE, 0.5).next_to(block, UP, buff=0.14)
            self.play(GrowFromCenter(clamp),
                      Flash(clamp, color=PRIVATE, flash_radius=0.45),
                      run_time=0.6)
            # second half: and the two ends end up holding the same key
            self.play(FadeOut(block, clamp, scale=0.8), run_time=0.4)
            kl = Key(PRIVATE, 0.55).next_to(left, DOWN, buff=0.3)
            kr = Key(PRIVATE, 0.55).next_to(right, DOWN, buff=0.3)
            mid = Key(PRIVATE, 0.7).move_to(UP * 0.9)
            self.play(FadeIn(mid, scale=0.6), run_time=0.4)
            eq = title("=", FG, 38).move_to(UP * 0.9)
            self.play(TransformFromCopy(mid, kl), TransformFromCopy(mid, kr),
                      ReplacementTransform(mid, eq), run_time=1.0)

        with self.beat(7.09, "In two thousand and one, the United States "
                            "adopted the Advanced Encryption Standard, or "
                            "AES, to protect sensitive digital information."):
            self.play(FadeOut(left, right, kl, kr, eq, era), run_time=0.5)
            self.play(line.slide(3, run_time=0.7))
            card = AESCard().move_to(UP * 1.35)
            self.play(FadeIn(card, shift=DOWN * 0.8), run_time=1.0)
            card.seal.move_to(card.shell.get_corner(DR) + RIGHT * 0.38
                              + DOWN * 0.12)
            self.play(GrowFromCenter(card.seal),
                      Flash(card.seal, color=PLAIN, flash_radius=0.6),
                      run_time=0.8)
            self.play(Rotate(card.seal, -0.12, run_time=0.3))
            guarded = VGroup(*[
                icon(k, PUBLIC, 0.62) for k in ("file", "card", "id")
            ]).arrange(RIGHT, buff=0.75).next_to(card, DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.2, scale=0.7)
                                    for g in guarded], lag_ratio=0.3),
                      run_time=1.2)
            stamps = VGroup(*[
                Padlock(PRIVATE, 0.3).move_to(g.get_corner(DR) + RIGHT * 0.2)
                for g in guarded
            ])
            self.play(LaggedStart(*[GrowFromCenter(st) for st in stamps],
                                  lag_ratio=0.15), run_time=0.7)

        with self.beat(4.99, "Today, AES is widely used to protect data on "
                             "devices and across networks."):
            self.play(FadeOut(guarded, stamps), run_time=0.4)
            self.play(line.slide(4, run_time=0.6))
            badge = card.badge(0.48).move_to(card.get_center())
            self.play(FadeOut(card.seal, scale=0.5),
                      ReplacementTransform(VGroup(card), badge), run_time=0.8)
            phone = Phone(FG, 1.5).move_to(LEFT * 4.3 + UP * 0.4)
            lap = Laptop(FG, 1.9).move_to(UP * 0.4)
            wire = Line(RIGHT * 2.6 + UP * 0.4, RIGHT * 5.6 + UP * 0.4,
                        color=PUBLIC, stroke_width=4)
            self.play(FadeIn(phone, scale=0.8), FadeIn(lap, scale=0.8),
                      Create(wire), run_time=0.7)
            for host in (phone, lap, wire):
                spot = host.get_center() + UP * 1.05
                self.play(badge.animate.move_to(spot), run_time=0.35)
                self.play(Flash(host, color=PRIVATE, flash_radius=0.7),
                          run_time=0.3)

        with self.beat(1.2, "(transition)"):
            # hand the picture to Part 2: the same arrangement scene 1 opens on
            net, maya, phone2, rays = _city()
            self.play(FadeOut(line, badge, phone, lap, wire), run_time=0.5)
            self.play(FadeIn(maya, phone2, net, rays), run_time=0.7)

        self.pad_to_target()


# --- 1. The big question (0:56-1:01) -------------------------------------


class Scene01Intro(VideoScene):
    TARGET = 4.63

    def construct(self):
        # Part 1 ends on Maya, her phone and the network, so this scene opens
        # on them rather than building them again: the picture carries over
        # the cut and only the note is new.
        net = NetworkMap(cols=6, rows=4, spacing=1.15)
        net.scale(0.78).move_to(RIGHT * 2.7 + UP * 0.2)
        maya = Person(FG, height=1.9, name="Maya")
        maya.move_to(LEFT * 5.1 + DOWN * 0.4)
        phone = Phone(height=1.05).next_to(maya.figure, RIGHT, buff=0.18)
        rays = VGroup(*[
            Line(phone.get_right(), net.at(0, j), color=PUBLIC,
                 stroke_width=2.4, stroke_opacity=0.55)
            for j in range(4)
        ])
        backdrop = VGroup(net, rays)
        self.add(maya, phone, backdrop)

        note = Note(MSG, PLAIN, size=22).scale(0.72)
        with self.beat(3.63, "So, how does encryption actually work and why do "
                            "we use it so often?"):
            snoops = VGroup(*[
                Snooper(height=0.95).move_to(net.at(i, j))
                for i, j in ((2, 3), (4, 0))
            ])
            self.play(FadeIn(snoops, shift=UP * 0.2), run_time=0.4)
            note.move_to(phone.get_center())
            self.play(FadeIn(note, scale=0.4), run_time=0.3)
            path = net.path([(0, 1), (1, 2), (2, 2), (3, 1), (4, 1), (5, 2)])
            self.play(
                MoveAlongPath(note, path),
                LaggedStart(*[
                    Rotate(s, 0.3, about_point=s.get_bottom(),
                           rate_func=there_and_back)
                    for s in snoops
                ], lag_ratio=0.45),
                run_time=2.0,
            )
            self.play(note.animate.move_to(ORIGIN).scale(1.3),
                      backdrop.animate.set_opacity(0.3), run_time=0.7)

        with self.beat(1.0, "(transition)"):
            self.play(FadeOut(backdrop, maya, phone, snoops),
                      note.animate.scale(1.9).move_to(ORIGIN), run_time=1.0)

        self.pad_to_target()


# --- 2. Plaintext and ciphertext (1:01-1:13) -----------------------------


class Scene02Ciphertext(VideoScene):
    TARGET = 12.78

    def construct(self):
        green = mono(MSG, PLAIN, size=38).move_to(LEFT * 3.6 + UP * 1.1)
        arrow = Arrow(LEFT * 1.3, RIGHT * 1.3, color=FG, buff=0,
                      stroke_width=7).shift(UP * 1.1)
        mark = Padlock(PRIVATE, height=0.5).next_to(arrow, UP, buff=0.18)
        red = mono(scrambled(MSG, seed=3), CIPHER, size=38)
        red.move_to(RIGHT * 3.6 + UP * 1.1)

        with self.beat(3.44, "Encryption is a way of turning a readable "
                             "message into a secret code."):
            self.play(Write(green), run_time=1.1)
            self.play(GrowArrow(arrow), run_time=0.6)
            self.play(FadeIn(mark, shift=DOWN * 0.25), run_time=0.4)
            self.play(TransformFromCopy(green, red), run_time=1.1)

        plabel = caption("PLAINTEXT", PLAIN).next_to(green, DOWN, buff=0.45)
        with self.beat(2.39, "The readable message is called plaintext."):
            self.play(Indicate(green, scale_factor=1.12, color=PLAIN), run_time=1.0)
            self.play(Write(plabel), run_time=0.9)

        clabel = caption("CIPHERTEXT", CIPHER).next_to(red, DOWN, buff=0.45)
        snoop = Snooper(height=2.0).move_to(RIGHT * 0.9 + DOWN * 1.9)
        qs = VGroup(*[Text("?", font_size=44, color=SNOOP) for _ in range(3)])
        qs.arrange(RIGHT, buff=0.42).move_to(RIGHT * 3.4 + DOWN * 1.1)
        qs[0].shift(DOWN * 0.22)
        qs[2].shift(UP * 0.22)

        # Read as one sentence, so the label and the snooper share one window:
        # the ciphertext names itself, then someone tries to read it.
        with self.beat(5.95, "After encryption, it becomes ciphertext, which "
                             "should look like meaningless information to "
                             "anyone who's not supposed to read it."):
            self.play(Write(clabel), run_time=0.8)
            scramble(self, red, steps=7, run_time=0.1)
            self.play(FadeIn(snoop, shift=UP * 0.5), run_time=0.7)
            self.play(Rotate(snoop, -0.22, about_point=snoop.get_bottom()),
                      run_time=0.6)
            self.play(LaggedStart(*[FadeIn(q, shift=UP * 0.3) for q in qs],
                                  lag_ratio=0.35), run_time=1.3)
            scramble(self, red, steps=7, run_time=0.1)

        with self.beat(1.0, "(transition)"):
            box = Box(FG, width=2.9, height=1.9, open_=True).move_to(DOWN * 1.2)
            card = Note(scrambled(MSG, seed=11), CIPHER, size=26).scale(0.85)
            card.move_to(UP * 1.9)
            self.play(
                FadeOut(green, plabel, clabel, arrow, mark, snoop, qs),
                ReplacementTransform(red, card),
                Create(box),
                run_time=1.0,
            )

        self.pad_to_target()


# --- 3. Locked box (1:13-1:27) -------------------------------------------


class Scene03LockedBox(MovingVideoScene):
    TARGET = 13.91

    def construct(self):
        box = Box(FG, width=2.9, height=1.9, open_=True).move_to(DOWN * 1.2)
        card = Note(scrambled(MSG, seed=11), CIPHER, size=26).scale(0.85)
        card.move_to(UP * 1.9)
        self.add(box, card)

        with self.beat(2.5, "Imagine putting a note inside a locked box."):
            self.play(card.animate.scale(0.62).move_to(box.inside()), run_time=1.0)
            self.bring_to_front(box)
            self.play(box.close_anim(run_time=0.8))
            self.play(VGroup(box, card).animate.move_to(ORIGIN), run_time=0.5)

        lbl_msg = caption("message", PLAIN).next_to(box, DOWN, buff=0.4)
        with self.beat(2.0, "The note is the original message."):
            self.play(box.body.animate.set_fill(opacity=0.25), run_time=0.5)
            self.play(Write(lbl_msg), Indicate(card, color=PLAIN, scale_factor=1.15),
                      run_time=1.0)

        lock = Padlock(PRIVATE, height=0.95)
        lock.move_to(box.body.get_right())
        lbl_enc = caption("encryption", PRIVATE).next_to(lock, RIGHT, buff=0.3)
        key = Key(PRIVATE, height=0.75).move_to(RIGHT * 4.6)
        lbl_key = caption("key", PRIVATE).next_to(key, DOWN, buff=0.35)

        # Lock and key are one sentence in the read, so they share a window:
        # the padlock snaps on and is named, then the key arrives and turns.
        with self.beat(4.16, "The lock is the encryption process, and the key "
                             "is what unlocks the box."):
            self.play(GrowFromCenter(lock), run_time=0.5)
            self.play(Write(lbl_enc), Flash(lock, color=PRIVATE, flash_radius=0.7),
                      run_time=0.7)
            self.play(FadeIn(key, shift=LEFT * 0.5), Write(lbl_key), run_time=0.8)
            hole = lock.keyhole.get_center()
            self.play(key.animate.scale(0.75).move_to(hole + LEFT * 0.42),
                      FadeOut(lbl_key), run_time=0.8)
            self.play(Rotate(key, PI / 2, about_point=hole), run_time=0.7)

        parcel = VGroup(box, card, lock, key)
        with self.beat(4.25, "The person receiving the message needs the "
                             "right key to be able to unlock it and read it."):
            snoopers = VGroup(Snooper(height=1.5), Snooper(height=1.5))
            snoopers.arrange(RIGHT, buff=2.6).move_to(DOWN * 2.3)
            sam = Person(FG, height=1.8, name="Sam").move_to(RIGHT * 5.0)
            self.play(
                FadeOut(lbl_msg, lbl_enc),
                parcel.animate.scale(0.72).move_to(LEFT * 4.6 + UP * 0.4),
                FadeIn(snoopers, shift=UP * 0.3), FadeIn(sam, shift=LEFT * 0.4),
                run_time=0.7,
            )
            self.play(
                parcel.animate.move_to(RIGHT * 2.1 + UP * 0.4),
                LaggedStart(*[Wiggle(s, scale_value=1.1) for s in snoopers],
                            lag_ratio=0.4),
                run_time=1.2,
            )
            sam_key = Key(PRIVATE, height=0.5).next_to(parcel, UP, buff=0.35)
            self.play(FadeIn(sam_key, shift=DOWN * 0.3), run_time=0.3)
            self.play(sam_key.animate.move_to(lock.keyhole.get_center()),
                      run_time=0.3)
            self.play(FadeOut(sam_key, key), lock.unlock_anim(), run_time=0.4)
            self.bring_to_front(card)
            self.play(box.open_anim(run_time=0.5),
                      card.animate.shift(UP * 0.85).scale(1.3), run_time=0.5)
            scramble(self, card.label, steps=3, run_time=0.09, settle=MSG)
            self.play(card.card.animate.set_stroke(PLAIN), run_time=0.25)

        with self.beat(1.0, "(transition)"):
            self.play(
                self.camera.frame.animate.scale(0.05).move_to(
                    lock.keyhole.get_center()),
                run_time=1.0,
            )

        self.pad_to_target()


# --- 4. The math (1:27-1:37) ---------------------------------------------


class Scene04Math(VideoScene):
    TARGET = 10.15

    def construct(self):
        # Scene 3 ended inside the padlock's keyhole, so this one opens there.
        field = Rectangle(
            width=config.frame_width + 1, height=config.frame_height + 1,
            color=PRIVATE, fill_color=PRIVATE, fill_opacity=1, stroke_width=0,
        )
        keyhole = VGroup(
            Circle(radius=0.11, color=BG, fill_opacity=1, stroke_width=0),
            Triangle(color=BG, fill_opacity=1, stroke_width=0)
            .scale_to_fit_height(0.2).rotate(PI).stretch(0.55, 0),
        )
        keyhole[1].next_to(keyhole[0], DOWN, buff=-0.05)
        keyhole.scale_to_fit_height(2.9).move_to(ORIGIN)
        self.add(field, keyhole)

        machine = RoundedRectangle(
            width=6.2, height=3.4, corner_radius=0.22, color=FG,
            stroke_width=STROKE, fill_color=SURFACE, fill_opacity=1,
        )
        lab = caption("ALGORITHM", FG, 26)
        lab.move_to(machine.get_bottom() + UP * 0.42)
        g1 = Gear(PUBLIC, 0.52).move_to(machine.get_center() + LEFT * 2.0 + UP * 0.95)
        g2 = Gear(PUBLIC, 0.34).move_to(machine.get_center() + LEFT * 1.3 + UP * 0.42)
        syms = VGroup(*[
            Text(s, font_size=30, color=PUBLIC).set_opacity(0.6)
            for s in ("+", "×", "=")
        ])
        for s, pos in zip(syms, (RIGHT * 2.6 + UP * 1.05, RIGHT * 2.0 + UP * 0.3,
                                 RIGHT * 2.5 + DOWN * 0.85)):
            s.move_to(machine.get_center() + pos)

        with self.beat(2.74, "Computers do this using complicated mathematics."):
            self.play(FadeOut(field), ReplacementTransform(keyhole, machine),
                      run_time=0.9)
            self.play(Write(lab),
                      LaggedStart(GrowFromCenter(g1), GrowFromCenter(g2),
                                  lag_ratio=0.3), run_time=0.8)
            g1.add_updater(lambda m, dt: m.rotate(0.9 * dt))
            g2.add_updater(lambda m, dt: m.rotate(-1.35 * dt))
            self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.35) for s in syms],
                                  lag_ratio=0.25), run_time=0.8)

        key = Key(PRIVATE, height=0.75).rotate(-PI / 2)
        key.move_to(machine.get_top() + UP * 1.3)
        bits = mono("1011 0110", PRIVATE, 22)
        # the message travels through the machine along this line, kept clear
        # of the gears and the floating symbols
        lane = machine.get_center() + DOWN * 0.35

        with self.beat(3.32, "An encryption algorithm changes the message "
                             "using a secret key."):
            self.play(FadeIn(key, shift=DOWN * 0.4), run_time=0.4)
            self.play(key.animate.move_to(machine.get_top()), run_time=0.5)
            bits.move_to(machine.get_top() + DOWN * 0.5 + RIGHT * 1.15)
            self.play(TransformFromCopy(key.teeth, bits), run_time=0.6)
            green = mono(MSG, PLAIN, 26).move_to(LEFT * 9 + UP * lane[1])
            self.add(green)
            self.play(green.animate.move_to(lane + LEFT * 1.4), run_time=0.6)
            red = mono(scrambled(MSG, seed=5), CIPHER, 26)
            red.move_to(lane + RIGHT * 1.4)
            self.play(ReplacementTransform(green, red), run_time=0.4)
            self.play(red.animate.move_to(RIGHT * 9 + UP * lane[1]), run_time=0.7)
            self.remove(red)

        with self.beat(3.09, "The receiver then uses the correct key to "
                            "change it back."):
            red2 = mono(scrambled(MSG, seed=5), CIPHER, 26)
            red2.move_to(RIGHT * 9 + UP * lane[1])
            self.add(red2)
            self.play(red2.animate.move_to(lane + RIGHT * 1.4), run_time=0.9)
            green2 = mono(MSG, PLAIN, 26).move_to(lane + LEFT * 1.4)
            self.play(ReplacementTransform(red2, green2), run_time=0.6)
            self.play(green2.animate.move_to(LEFT * 9 + UP * lane[1]), run_time=1.0)
            self.remove(green2)

        with self.beat(1.0, "(transition)"):
            g1.clear_updaters()
            g2.clear_updaters()
            self.play(key.animate.shift(UP * 1.8),
                      FadeOut(machine, lab, g1, g2, syms, bits), run_time=1.0)

        self.pad_to_target()


# --- 5. Symmetric encryption (1:37-1:54) ---------------------------------


def _panels():
    """The two numbered panels that scenes 5 and 6 each take one of."""
    left = RoundedRectangle(
        width=5.8, height=3.8, corner_radius=0.25, color=FG,
        stroke_width=STROKE, fill_color=SURFACE, fill_opacity=0.55,
    )
    right = left.copy()
    VGroup(left, right).arrange(RIGHT, buff=0.9).move_to(ORIGIN)
    return left, right


def _expand(panel, label):
    """Open a panel out to fill the frame, with its label at the top."""
    return (
        panel.animate.stretch_to_fit_width(12.8).stretch_to_fit_height(5.7)
        .move_to(DOWN * 0.5),
        label.animate.scale(0.8).move_to(UP * 2.95),
    )


class Scene05Symmetric(VideoScene):
    TARGET = 16.45

    def construct(self):
        p1, p2 = _panels()
        n1 = title("1", SNOOP, 70).move_to(p1)
        n2 = title("2", SNOOP, 70).move_to(p2)

        with self.beat(1.98, "There are two main types of encryption."):
            self.play(LaggedStart(Create(p1), Create(p2), lag_ratio=0.35),
                      run_time=1.1)
            self.play(Write(n1), Write(n2), run_time=0.75)

        lab = heading("SYMMETRIC", PRIVATE, 34)
        with self.beat(2.12, "The first is symmetric encryption."):
            self.play(p1.animate.set_stroke(PRIVATE),
                      ReplacementTransform(n1, lab.move_to(p1)),
                      VGroup(p2, n2).animate.set_opacity(0.22), run_time=0.9)
            self.play(FadeOut(p2, n2, shift=RIGHT * 1.5), *_expand(p1, lab),
                      run_time=1.1)

        maya = Person(FG, height=1.5, name="Maya").move_to(LEFT * 4.6 + DOWN * 0.7)
        sam = Person(FG, height=1.5, name="Sam").move_to(RIGHT * 4.6 + DOWN * 0.7)
        kA = Key(PRIVATE, 0.55).next_to(maya.figure, UP, buff=0.3)
        kB = Key(PRIVATE, 0.55).next_to(sam.figure, UP, buff=0.3)

        with self.beat(3.4, "It uses the same key to lock and unlock the "
                             "information."):
            k0 = Key(PRIVATE, 0.8).move_to(UP * 1.5)
            self.play(FadeIn(maya, shift=RIGHT * 0.3), FadeIn(sam, shift=LEFT * 0.3),
                      GrowFromCenter(k0), run_time=0.8)
            eq = title("=", FG, 44).move_to(UP * 1.5)
            self.play(TransformFromCopy(k0, kA), TransformFromCopy(k0, kB),
                      ReplacementTransform(k0, eq), run_time=1.0)
            box = Box(FG, width=2.1, height=1.35).move_to(DOWN * 0.9)
            lock = Padlock(PRIVATE, 0.62).move_to(box.body.get_right())
            self.play(FadeIn(box, scale=0.85), run_time=0.5)
            self.play(GrowFromCenter(lock),
                      Flash(lock, color=PRIVATE, flash_radius=0.5), run_time=0.6)
            self.play(lock.unlock_anim(), run_time=0.5)

        # The read drops "it's fast", but the ripple keeps the point: the
        # whole stack is locked in the time it takes to say the line, and
        # scene 7 leans on symmetric encryption being the quick one.
        with self.beat(2.69, "This is very useful for protecting large "
                            "amounts of data."):
            self.play(FadeOut(box, lock, eq), run_time=0.35)
            files = VGroup(*[icon("file", FG, 0.62) for _ in range(15)])
            files.arrange_in_grid(rows=3, cols=5, buff=(0.4, 0.3))
            files.move_to(DOWN * 0.75)
            self.play(LaggedStart(*[FadeIn(f, scale=0.7) for f in files],
                                  lag_ratio=0.05), run_time=1.2)
            stamps = VGroup(*[
                Padlock(PRIVATE, 0.3).move_to(f.get_corner(DR)) for f in files
            ])
            self.play(LaggedStart(*[GrowFromCenter(s) for s in stamps],
                                  lag_ratio=0.04), run_time=1.0)

        with self.beat(5.26, "The challenge is that both people or devices "
                             "need to receive the same secret key safely."):
            self.play(FadeOut(files, stamps), run_time=0.5)
            dash = DashedLine(kA.get_right() + RIGHT * 0.3,
                              kB.get_left() + LEFT * 0.3,
                              color=SNOOP, stroke_width=4, dash_length=0.2)
            self.play(Create(dash), run_time=0.9)
            trav = Key(PRIVATE, 0.5).move_to(dash.get_start())
            self.play(FadeIn(trav, scale=0.6), run_time=0.3)
            self.play(trav.animate.move_to(dash.get_center()), run_time=1.3)
            hand = GrabHand(height=1.7)
            hand.move_to(dash.get_center() + DOWN * 3.4)
            self.play(hand.animate.shift(UP * 2.3), run_time=0.8)
            q = title("?", SNOOP, 80).next_to(dash.get_center(), UP, buff=0.45)
            self.play(FadeIn(q, shift=UP * 0.3), run_time=0.7)

        with self.beat(1.0, "(transition)"):
            kblue = Key(PUBLIC, 0.55).move_to(trav.get_center() + LEFT * 0.85)
            kgold = Key(PRIVATE, 0.55).move_to(trav.get_center() + RIGHT * 0.85)
            self.play(
                hand.animate.shift(UP * 0.4),
                ReplacementTransform(trav, VGroup(kblue, kgold)),
                FadeOut(dash, q, maya, sam, kA, kB, lab, p1),
                run_time=1.0,
            )

        self.pad_to_target()


# --- 6. Asymmetric encryption (1:54-2:19) --------------------------------


class Scene06Asymmetric(VideoScene):
    TARGET = 25.33

    def construct(self):
        p1, p2 = _panels()
        lab1 = caption("SYMMETRIC", SNOOP, 26).move_to(p1)
        p1.set_stroke(SNOOP)
        self.add(p1, p2, lab1)

        lab2 = heading("ASYMMETRIC", PUBLIC, 32).move_to(p2)
        sub = caption("(public-key)", SNOOP, 22)

        # One sentence in the read: the panel opens on the name, and the alias
        # writes on under it as it is said.
        with self.beat(4.12, "Second is asymmetric encryption, also called "
                             "public key encryption."):
            self.play(p2.animate.set_stroke(PUBLIC), Write(lab2),
                      VGroup(p1, lab1).animate.set_opacity(0.22), run_time=1.2)
            self.play(FadeOut(p1, lab1, shift=LEFT * 1.5), *_expand(p2, lab2),
                      run_time=1.3)
            sub.next_to(lab2, DOWN, buff=0.12)
            self.play(FadeIn(sub, shift=DOWN * 0.15), run_time=0.8)

        kb = Key(PUBLIC, 0.85).move_to(LEFT * 0.9 + UP * 1.4)
        kg = Key(PRIVATE, 0.85).move_to(RIGHT * 0.9 + UP * 1.4)
        lb = caption("PUBLIC KEY", PUBLIC)
        lg = caption("PRIVATE KEY", PRIVATE)

        with self.beat(2.26, "This uses a public key and a private key."):
            self.play(FadeIn(kb, scale=0.7), FadeIn(kg, scale=0.7), run_time=0.5)
            self.play(kb.animate.move_to(LEFT * 3.8 + UP * 1.4),
                      kg.animate.move_to(RIGHT * 3.8 + UP * 1.4), run_time=0.8)
            lb.next_to(kb, DOWN, buff=0.35)
            lg.next_to(kg, DOWN, buff=0.35)
            self.play(Write(lb), Write(lg), run_time=0.8)

        crowd = VGroup(*[Person(FG, height=1.0) for _ in range(5)])
        crowd.arrange(RIGHT, buff=0.72).move_to(LEFT * 3.4 + DOWN * 2.2)

        with self.beat(2.04, "The public key can be shared with everyone."):
            self.play(FadeIn(crowd, shift=UP * 0.3, lag_ratio=0.12), run_time=0.5)
            copies = VGroup(*[
                Key(PUBLIC, 0.42).next_to(p, UP, buff=0.14) for p in crowd
            ])
            self.play(LaggedStart(*[TransformFromCopy(kb, c) for c in copies],
                                  lag_ratio=0.13), run_time=1.4)

        sam = Person(FG, height=1.6, name="Sam").move_to(RIGHT * 4.9 + DOWN * 1.7)
        glow = Circle(radius=0.82, color=PRIVATE, stroke_width=4,
                      fill_color=PRIVATE, fill_opacity=0.12)

        with self.beat(1.81, "The private key must be kept secret."):
            self.play(FadeIn(sam, shift=LEFT * 0.3), run_time=0.4)
            self.play(kg.animate.next_to(sam.figure, UP, buff=0.25), FadeOut(lg),
                      run_time=0.7)
            glow.move_to(kg)
            self.add(glow)
            self.bring_to_back(glow)
            self.play(Create(glow),
                      Flash(kg, color=PRIVATE, flash_radius=0.7), run_time=0.6)

        # Not in the plan: the read has a sentence here that states plainly
        # what the mailbox then illustrates. One of the public keys already in
        # the crowd's hands locks a note, it travels to Sam, and only his gold
        # key opens it.
        with self.beat(5.08, "Someone can send you an encrypted message with "
                             "your public key, but only your private key "
                             "should be able to unlock it."):
            sender = crowd[1]
            note = Note(MSG, PLAIN, size=15).scale(0.9)
            note.next_to(sender, UP, buff=0.95)
            self.play(FadeIn(note, shift=UP * 0.25), run_time=0.4)
            seal = Padlock(PUBLIC, 0.34).move_to(note.get_corner(DR))
            self.play(TransformFromCopy(copies[1], seal), run_time=0.55)
            locked = VGroup(note, seal)
            self.play(note.label.animate.set_color(CIPHER),
                      note.card.animate.set_stroke(CIPHER), run_time=0.35)
            scramble(self, note.label, steps=4, run_time=0.08)
            self.play(locked.animate.move_to(sam.get_center() + UP * 1.9),
                      run_time=0.9)
            # The public key sealed it; it cannot open it again.
            self.play(Indicate(kg, color=PRIVATE, scale_factor=1.2), run_time=0.4)
            self.play(FadeOut(seal, scale=0.4), run_time=0.25)
            scramble(self, note.label, steps=3, run_time=0.08, settle=MSG)
            self.play(note.card.animate.set_stroke(PLAIN),
                      note.label.animate.set_color(PLAIN), run_time=0.25)
            self.play(FadeOut(note, scale=0.7), run_time=0.25)

        mb = Mailbox(height=3.0).move_to(RIGHT * 0.6 + DOWN * 0.5)
        with self.beat(2.1, "A useful example is a mailbox."):
            self.play(kb.animate.move_to(mb.slot_point()), FadeOut(lb),
                      run_time=0.6)
            rest = VGroup(*[m for m in mb.submobjects if m is not mb.slot])
            self.play(ReplacementTransform(kb, mb.slot), Create(rest), run_time=1.2)
            self.bring_to_front(mb.slot)

        # One sentence in the read, so the letters go in and come out again
        # inside a single window.
        with self.beat(6.92, "Anyone can put letters inside, like using a "
                             "public key, but only the person with the private "
                             "key could open the mailbox and read the letters."):
            envs = VGroup(*[
                Envelope(FG, 0.52).next_to(crowd[i], UP, buff=0.55)
                for i in (0, 2, 4)
            ])
            self.play(LaggedStart(*[FadeIn(e, scale=0.7) for e in envs],
                                  lag_ratio=0.2), run_time=0.7)
            self.play(
                LaggedStart(*[
                    Succession(
                        e.animate(run_time=0.8).move_to(mb.slot_point()).scale(0.55),
                        FadeOut(e, run_time=0.12),
                    ) for e in envs
                ], lag_ratio=0.4),
                run_time=1.7,
            )
            self.play(sam.animate.move_to(RIGHT * 3.4 + DOWN * 1.7),
                      kg.animate.move_to(RIGHT * 3.4 + DOWN * 0.5),
                      glow.animate.move_to(RIGHT * 3.4 + DOWN * 0.5), run_time=0.7)
            self.play(FadeOut(glow),
                      kg.animate.scale(0.75).move_to(mb.knob.get_center()),
                      run_time=0.5)
            self.play(mb.open_door_anim(run_time=0.8))
            outs = VGroup(*[Envelope(PLAIN, 0.55) for _ in range(3)])
            outs.arrange(RIGHT, buff=0.45).next_to(mb, UP, buff=0.45)
            self.play(LaggedStart(*[FadeIn(e, shift=UP * 0.6) for e in outs],
                                  lag_ratio=0.2), run_time=0.9)
            notes = VGroup(*[Note(MSG, PLAIN, size=16) for _ in outs])
            notes.arrange(RIGHT, buff=0.3).next_to(mb, UP, buff=0.4)
            self.play(LaggedStart(*[
                ReplacementTransform(e, n) for e, n in zip(outs, notes)
            ], lag_ratio=0.2), run_time=1.0)

        with self.beat(1.0, "(transition)"):
            self.play(FadeOut(mb, notes, crowd, copies, sam, kg, lab2, sub, p2,
                              shift=LEFT * 1.2), run_time=1.0)

        self.pad_to_target()


# --- 7. Both together, HTTPS and daily life (2:19-2:47) ------------------


def _parcel(width: float = 0.7):
    """A small locked box, for the streams of traffic in scenes 7 and 8."""
    b = Box(FG, width=width, height=width * 0.68)
    l = Padlock(PRIVATE, width * 0.42).move_to(b.body.get_center())
    return VGroup(b, l)


class Scene07Https(MovingVideoScene):
    TARGET = 27.45

    def construct(self):
        laptop = Laptop(FG, height=2.5).move_to(LEFT * 4.2 + DOWN * 0.7)
        server = Server(FG, height=3.0).move_to(RIGHT * 4.6 + DOWN * 0.5)

        with self.beat(2.7, "Many real systems use both types together."):
            self.play(FadeIn(laptop, shift=RIGHT * 0.5),
                      FadeIn(server, shift=LEFT * 0.5), run_time=0.9)
            one = Key(PRIVATE, 0.5)
            two = VGroup(Key(PUBLIC, 0.5), Key(PRIVATE, 0.5)).arrange(RIGHT, buff=0.2)
            VGroup(one, two).arrange(RIGHT, buff=1.6).move_to(UP * 2.5)
            self.play(FadeIn(one, shift=UP * 0.2), FadeIn(two, shift=UP * 0.2),
                      run_time=0.7)
            merged = VGroup(Key(PUBLIC, 0.55), Key(PRIVATE, 0.55))
            merged.arrange(RIGHT, buff=0.2).move_to(UP * 2.5)
            self.play(ReplacementTransform(VGroup(one, two), merged), run_time=0.9)

        shared_l = Key(PRIVATE, 0.5).next_to(laptop, UP, buff=0.45)
        shared_r = Key(PRIVATE, 0.5).next_to(server, UP, buff=0.45)

        with self.beat(6.51, "For example, when visiting a secure website, "
                             "public key encryption helps your device and the "
                             "website agree on a secret key."):
            self.play(FadeOut(merged), run_time=0.3)
            slot = RoundedRectangle(
                width=1.4, height=0.22, corner_radius=0.11, color=PUBLIC,
                fill_color=PUBLIC, fill_opacity=1, stroke_width=0,
            ).next_to(server, UP, buff=0.45)
            slot_lab = caption("public key", PUBLIC, 20).next_to(slot, UP, buff=0.18)
            self.play(GrowFromCenter(slot), FadeIn(slot_lab), run_time=0.8)
            newkey = Key(PRIVATE, 0.5).next_to(laptop, UP, buff=0.45)
            self.play(FadeIn(newkey, scale=0.5),
                      Flash(newkey, color=PRIVATE, flash_radius=0.6), run_time=0.8)
            arc = ArcBetweenPoints(newkey.get_center(), slot.get_center(),
                                   angle=-PI / 3)
            self.play(MoveAlongPath(newkey, arc), run_time=1.5)
            self.play(FadeOut(newkey, scale=0.4), run_time=0.35)
            srv_key = Key(PRIVATE, 0.45).next_to(server, DOWN, buff=0.35)
            self.play(FadeIn(srv_key, shift=UP * 0.2), run_time=0.45)
            self.play(FadeOut(slot, slot_lab),
                      ReplacementTransform(srv_key, shared_r),
                      FadeIn(shared_l, scale=0.6), run_time=0.8)
            eq = title("=", FG, 40).move_to(UP * 1.9)
            self.play(Write(eq), Indicate(shared_l, color=PRIVATE),
                      Indicate(shared_r, color=PRIVATE), run_time=0.9)

        with self.beat(3.83, "Then, fast symmetric encryption protects the "
                             "rest of the conversation."):
            self.play(FadeOut(eq), run_time=0.3)
            start_l = laptop.get_right() + RIGHT * 0.5 + UP * 0.5
            end_r = server.get_left() + LEFT * 0.5 + UP * 0.5
            fwd = VGroup(*[_parcel().move_to(start_l) for _ in range(5)])
            back = VGroup(*[
                _parcel().move_to(end_r + DOWN * 1.0) for _ in range(4)
            ])
            self.play(
                LaggedStart(*[m.animate.move_to(end_r) for m in fwd],
                            lag_ratio=0.18),
                LaggedStart(*[m.animate.move_to(start_l + DOWN * 1.0)
                              for m in back], lag_ratio=0.22),
                run_time=2.6,
            )
            self.play(FadeOut(fwd, back), run_time=0.4)

        # The read widens out to everyday life here, before it narrows to the
        # browser padlock as the first example of it. Faint icons gather round
        # the pair rather than replacing them, so the laptop is still there to
        # zoom into on the next beat.
        with self.beat(2.39, "Encryption is used in many parts of daily life."):
            self.play(FadeOut(shared_l, shared_r), run_time=0.3)
            halo = VGroup()
            for kind, spot in zip(
                ("chat", "card", "cart", "id", "email", "file"),
                (LEFT * 5.7 + UP * 2.5, LEFT * 2.1 + UP * 3.0,
                 RIGHT * 1.5 + UP * 3.0, RIGHT * 5.5 + UP * 2.5,
                 LEFT * 6.0 + DOWN * 2.7, RIGHT * 6.0 + DOWN * 2.7),
            ):
                halo.add(icon(kind, SNOOP, 0.5).set_opacity(0.45).move_to(spot))
            self.play(LaggedStart(*[FadeIn(i, scale=0.7) for i in halo],
                                  lag_ratio=0.1), run_time=1.5)

        bar = BrowserBar("https://")
        bar.scale_to_fit_width(laptop.screen.width * 0.86)
        bar.move_to(laptop.screen.get_center() + UP * 0.38)

        # One sentence in the read, covering both the padlock and what it is
        # doing, so the zoom and the glow share a window.
        with self.beat(6.93, "When you see a padlock symbol in your web "
                             "browser, HTTPS is helping encrypt the connection "
                             "between your device and the website."):
            self.play(FadeIn(bar), FadeOut(halo), run_time=0.6)
            self.play(
                self.camera.frame.animate
                .scale_to_fit_height(laptop.screen.height * 1.6)
                .move_to(laptop.screen.get_center()),
                run_time=1.5,
            )
            self.play(Indicate(bar.lock, color=PRIVATE, scale_factor=1.35),
                      run_time=1.0)
            self.play(bar.url_text.animate.set_color(PLAIN),
                      Flash(bar.url_text, color=PLAIN, flash_radius=0.4),
                      run_time=1.0)
            # the connection itself: a locked channel under the bar, device to
            # website, pulsing once as it is named
            pipe = DashedLine(
                bar.get_corner(DL) + DOWN * 0.42 + RIGHT * 0.05,
                bar.get_corner(DR) + DOWN * 0.42 + LEFT * 0.05,
                color=PUBLIC, stroke_width=3, dash_length=0.06,
            )
            seal = Padlock(PRIVATE, 0.2).move_to(pipe.get_center())
            self.play(Create(pipe), run_time=0.7)
            self.play(GrowFromCenter(seal),
                      Flash(seal, color=PRIVATE, flash_radius=0.18,
                            line_length=0.05), run_time=0.6)

        with self.beat(4.09, "This helps protect passwords, shopping "
                             "information, and other personal details."):
            trio = VGroup(
                icon("password", PUBLIC, 0.34),
                icon("cart", PUBLIC, 0.34),
                icon("id", PUBLIC, 0.34),
            ).arrange(RIGHT, buff=0.32).next_to(pipe, DOWN, buff=0.28)
            self.play(
                LaggedStart(*[FadeIn(i, shift=UP * 0.12, scale=0.7) for i in trio],
                            lag_ratio=0.5),
                run_time=2.4,
            )

        with self.beat(1.0, "(transition)"):
            big = Padlock(PRIVATE, 1.7).move_to(ORIGIN)
            self.play(
                self.camera.frame.animate.scale_to_fit_height(
                    config.frame_height).move_to(ORIGIN),
                FadeOut(laptop, server, bar, trio, pipe, seal),
                FadeIn(big, scale=0.4),
                run_time=1.0,
            )

        self.pad_to_target()


# --- 8. Everyday uses (2:47-3:11) ----------------------------------------


class Scene08Everyday(VideoScene):
    TARGET = 24.19

    def construct(self):
        lock = Padlock(PRIVATE, 1.7)
        self.add(lock)

        with self.beat(5.62, "Messaging apps can use end-to-end encryption so "
                             "that a message is protected while traveling from "
                             "one phone to another."):
            self.play(FadeOut(lock), run_time=0.35)
            pa = Phone(FG, 2.3).move_to(LEFT * 5.0 + DOWN * 0.3)
            pb = Phone(FG, 2.3).move_to(RIGHT * 5.0 + DOWN * 0.3)
            self.play(FadeIn(pa, shift=RIGHT * 0.3), FadeIn(pb, shift=LEFT * 0.3),
                      run_time=0.7)
            bub = icon("chat", PLAIN, 0.85).move_to(pa.get_center())
            self.play(FadeIn(bub, scale=0.6), run_time=0.5)
            parcel = _parcel(1.1).move_to(bub)
            self.play(ReplacementTransform(bub, parcel), run_time=0.7)
            self.play(parcel.animate.move_to(pb.get_center()), run_time=1.7)
            bub2 = icon("chat", PLAIN, 0.85).move_to(pb.get_center())
            self.play(ReplacementTransform(parcel, bub2), run_time=0.7)
            e2e = caption("end-to-end", PLAIN, 22).move_to(DOWN * 2.6)
            self.play(FadeIn(e2e, shift=UP * 0.2), run_time=0.45)

        with self.beat(7.17, "Phones and computers can also encrypt stored "
                             "files to make sure that information is harder to "
                             "access if the device is lost or stolen."):
            self.play(FadeOut(pa, pb, bub2, e2e), run_time=0.5)
            lap = Laptop(FG, 2.8).move_to(LEFT * 3.2 + UP * 0.2)
            folder = Folder(PUBLIC, 1.3).move_to(lap.screen.get_center())
            self.play(FadeIn(lap, scale=0.9), FadeIn(folder, scale=0.7),
                      run_time=0.9)
            stamp = Padlock(PRIVATE, 0.55).move_to(folder.get_corner(DR))
            self.play(GrowFromCenter(stamp), run_time=0.4)
            self.play(stamp.animate.scale(1.35), run_time=0.2)
            self.play(stamp.animate.scale(1 / 1.35), run_time=0.25)
            hand = GrabHand(height=2.1).move_to(RIGHT * 1.6 + DOWN * 3.8)
            self.play(hand.animate.move_to(RIGHT * 1.6 + DOWN * 1.3), run_time=0.8)
            self.play(VGroup(lap, folder, stamp).animate.shift(RIGHT * 4.4),
                      hand.animate.shift(RIGHT * 2.2), run_time=1.1)
            # the folder opens on the stolen laptop and holds nothing readable
            junk = VGroup(*[
                mono(scrambled("Meet at 3pm", seed=20 + i), CIPHER, 19)
                for i in range(3)
            ]).arrange(DOWN, buff=0.18)
            junk.scale_to_fit_width(lap.screen.width * 0.8)
            junk.move_to(lap.screen.get_center())
            self.play(FadeOut(stamp), FadeOut(folder, scale=1.4),
                      FadeIn(junk, shift=UP * 0.25), run_time=0.9)
            self.play(Wiggle(hand, scale_value=1.08), run_time=0.8)

        with self.beat(5.72, "Encryption is used by banks, online stores, "
                             "hospitals, businesses, and government agencies."):
            self.play(FadeOut(lap, junk, hand), run_time=0.5)
            kinds = ("bank", "cart", "hospital", "office", "government")
            grid = VGroup(*[icon(k, FG, 1.0) for k in kinds])
            grid.arrange(RIGHT, buff=0.95).move_to(UP * 0.2)
            self.play(
                LaggedStart(*[FadeIn(g, shift=UP * 0.3, scale=0.7) for g in grid],
                            lag_ratio=0.62),
                run_time=3.6,
            )
            stamps = VGroup(*[
                Padlock(PRIVATE, 0.38).move_to(g.get_corner(DR) + RIGHT * 0.26)
                for g in grid
            ])
            self.play(LaggedStart(*[GrowFromCenter(s) for s in stamps],
                                  lag_ratio=0.1), run_time=1.0)

        # The read gives VPNs their own sentence, so they get more than the
        # last cell of a grid: the tunnel itself, with traffic inside it.
        with self.beat(4.68, "It's also used to protect the information sent "
                             "through virtual private networks or VPNs."):
            self.play(FadeOut(grid, stamps), run_time=0.5)
            here = Laptop(FG, 1.9).move_to(LEFT * 5.0 + DOWN * 0.2)
            there = Server(FG, 2.2).move_to(RIGHT * 5.1)
            self.play(FadeIn(here, shift=RIGHT * 0.3),
                      FadeIn(there, shift=LEFT * 0.3), run_time=0.6)
            tube = VGroup(
                Line(LEFT * 4.1 + UP * 0.75, RIGHT * 4.2 + UP * 0.75,
                     color=PUBLIC, stroke_width=4),
                Line(LEFT * 4.1 + DOWN * 0.55, RIGHT * 4.2 + DOWN * 0.55,
                     color=PUBLIC, stroke_width=4),
            )
            self.play(Create(tube, lag_ratio=0), run_time=0.7)
            # the shield glyph carries its own VPN label
            shield = icon("vpn", PRIVATE, 1.05).move_to(UP * 2.15)
            self.play(FadeIn(shield, scale=0.6), run_time=0.7)
            flow = VGroup(*[
                _parcel(0.62).move_to(LEFT * 3.3 + UP * 0.1) for _ in range(4)
            ])
            self.play(
                LaggedStart(*[m.animate.move_to(RIGHT * 3.4 + UP * 0.1)
                              for m in flow], lag_ratio=0.2),
                run_time=1.9,
            )

        with self.beat(1.0, "(transition)"):
            maya = Person(FG, 1.9, "Maya").move_to(LEFT * 4.0 + DOWN * 0.4)
            phone = Phone(FG, 1.2).next_to(maya.figure, RIGHT, buff=0.25)
            mail = icon("email", CIPHER, 0.9).move_to(RIGHT * 1.6 + UP * 0.6)
            bang = title("!", CIPHER, 38).next_to(mail, RIGHT, buff=0.2)
            self.play(FadeOut(here, there, tube, shield, flow),
                      FadeIn(maya, phone),
                      FadeIn(mail, shift=LEFT * 0.6), FadeIn(bang), run_time=1.0)

        self.pad_to_target()


# --- 9. Not magic (3:11-3:28) --------------------------------------------


class Scene09NotMagic(VideoScene):
    TARGET = 16.92

    def construct(self):
        maya = Person(FG, 1.9, "Maya").move_to(LEFT * 5.1 + DOWN * 0.9)
        phone = Phone(FG, 1.2).next_to(maya.figure, RIGHT, buff=0.25)
        mail = icon("email", CIPHER, 0.9).move_to(RIGHT * 4.6 + UP * 2.0)
        bang = title("!", CIPHER, 38).next_to(mail, RIGHT, buff=0.2)
        self.add(maya, phone, mail, bang)

        box = Box(FG, width=2.4, height=1.6).move_to(UP * 0.4)
        lock = Padlock(PRIVATE, 0.78).move_to(box.body.get_right())
        halo = Circle(radius=1.75, color=PRIVATE, stroke_width=4,
                      fill_color=PRIVATE, fill_opacity=0.08).move_to(box)

        with self.beat(2.98, "Encryption is extremely important, but it is "
                             "not magic."):
            self.play(FadeIn(box, scale=0.85), GrowFromCenter(lock), run_time=1.0)
            self.add(halo)
            self.bring_to_back(halo)
            self.play(Create(halo), Indicate(lock, color=PRIVATE), run_time=1.3)

        mkey = Key(PRIVATE, 0.5).next_to(maya.figure, UP, buff=0.25)
        hood = Snooper(SNOOP, 1.8).move_to(LEFT * 2.3 + DOWN * 1.9)

        # One sentence listing three ways encryption is got round, so all
        # three play inside one window: the handed-over key, the clicked link,
        # then the program that walks in.
        with self.beat(7.03, "It cannot protect someone who gives away their "
                             "password, clicks on a dangerous link, or allows "
                             "a malicious program onto the device."):
            pw = icon("password", CIPHER, 0.6).next_to(mail, DOWN, buff=0.35)
            self.play(FadeIn(pw, shift=DOWN * 0.2), run_time=0.5)
            self.play(FadeIn(hood, shift=UP * 0.4), FadeIn(mkey, scale=0.6),
                      run_time=0.6)
            self.play(mkey.animate.next_to(hood, UP, buff=0.15), run_time=0.9)

            link = icon("link", CIPHER, 0.75).move_to(RIGHT * 2.6 + DOWN * 2.0)
            cur = icon("cursor", FG, 0.5).next_to(link, DR, buff=0.02)
            self.play(FadeIn(link), FadeIn(cur), run_time=0.45)
            self.play(cur.animate.shift(UP * 0.12 + LEFT * 0.12), run_time=0.2)
            red_flash = Rectangle(
                width=config.frame_width, height=config.frame_height,
                color=CIPHER, fill_color=CIPHER, fill_opacity=0.3, stroke_width=0,
            )
            self.play(FadeIn(red_flash), run_time=0.2)
            self.play(FadeOut(red_flash), run_time=0.3)

            bug = icon("bug", CIPHER, 0.6).move_to(RIGHT * 1.4 + DOWN * 3.0)
            self.play(FadeIn(bug), run_time=0.35)
            crawl = ArcBetweenPoints(bug.get_center(), phone.get_center(),
                                     angle=-PI / 4)
            self.play(MoveAlongPath(bug, crawl), run_time=1.3)
            self.play(FadeOut(bug, scale=0.3),
                      Flash(phone, color=CIPHER, flash_radius=0.8), run_time=0.5)

        # One sentence: the box opens cleanly with the stolen key, and the
        # answer to that is the three habits, not a stronger lock.
        with self.beat(5.91, "Encryption protects the information, but people "
                             "still need to use strong passwords and make safe "
                             "decisions."):
            self.play(mkey.animate.scale(0.85).move_to(lock.keyhole.get_center()),
                      run_time=0.6)
            self.play(FadeOut(mkey, halo), lock.unlock_anim(),
                      box.open_anim(run_time=0.8), run_time=0.8)
            self.play(FadeOut(box, lock, hood, link, cur, pw, mail, bang,
                              maya, phone), run_time=0.5)
            tips = VGroup(
                labelled(icon("password", PLAIN, 0.95), "strong passwords",
                         PLAIN, 21),
                labelled(icon("link", PLAIN, 0.95), "think before you click",
                         PLAIN, 21),
                labelled(icon("shield", PLAIN, 0.95), "keep devices updated",
                         PLAIN, 21),
            ).arrange(RIGHT, buff=1.4, aligned_edge=UP)
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.3) for t in tips],
                                  lag_ratio=0.45), run_time=2.4)

        with self.beat(1.0, "(transition)"):
            note = Note(MSG, PLAIN, 28)
            self.play(FadeOut(tips, shift=DOWN * 0.3), FadeIn(note, scale=0.4),
                      run_time=1.0)

        self.pad_to_target()


# --- 10. Outro (3:28-3:42) -----------------------------------------------


class Scene10Outro(VideoScene):
    TARGET = 13.86

    def construct(self):
        note = Note(MSG, PLAIN, 28).move_to(UP * 1.3 + RIGHT * 0.7)
        self.add(note)

        with self.beat(2.52, "In short, encryption is like a digital lock."):
            scramble(self, note.label, steps=5, run_time=0.07)
            self.play(note.card.animate.set_stroke(CIPHER), run_time=0.2)
            box = Box(FG, width=2.8, height=1.8, open_=True).move_to(DOWN * 1.1)
            self.play(Create(box), run_time=0.4)
            self.play(note.animate.scale(0.55).move_to(box.inside()), run_time=0.45)
            self.bring_to_front(box)
            self.play(box.close_anim(run_time=0.4))
            lock = Padlock(PRIVATE, 0.75).move_to(box.body.get_right())
            self.play(GrowFromCenter(lock),
                      Flash(lock, color=PRIVATE, flash_radius=0.6), run_time=0.5)

        parcel = VGroup(box, note, lock)
        with self.beat(4.34, "It helps keep private information private while "
                             "it's being sent, stored, or shared."):
            self.play(parcel.animate.scale(0.45).move_to(LEFT * 5.6 + UP * 0.2),
                      run_time=0.5)
            track = Arrow(LEFT * 6.0 + DOWN * 0.6, LEFT * 2.9 + DOWN * 0.6,
                          color=SNOOP, buff=0, stroke_width=4)
            w1 = caption("sent", PLAIN, 24).move_to(LEFT * 4.4 + DOWN * 2.3)
            self.play(Create(track), Write(w1), run_time=0.5)
            self.play(parcel.animate.move_to(LEFT * 3.2 + UP * 0.2), run_time=0.7)
            folder = Folder(PUBLIC, 1.7).move_to(DOWN * 0.3)
            w2 = caption("stored", PLAIN, 24).move_to(DOWN * 2.3)
            self.play(FadeIn(folder, scale=0.8), Write(w2), run_time=0.5)
            self.bring_to_front(parcel)
            self.play(parcel.animate.scale(0.75).move_to(folder.shell.get_center()),
                      run_time=0.7)
            two = VGroup(Person(FG, 1.0), Person(FG, 1.0))
            two.arrange(RIGHT, buff=1.0).move_to(RIGHT * 4.4 + DOWN * 0.9)
            w3 = caption("shared", PLAIN, 24).move_to(RIGHT * 4.4 + DOWN * 2.3)
            self.play(FadeIn(two, lag_ratio=0.2), Write(w3), run_time=0.5)
            c1, c2 = parcel.copy(), parcel.copy()
            self.play(c1.animate.move_to(two[0].get_top() + UP * 0.5),
                      c2.animate.move_to(two[1].get_top() + UP * 0.5), run_time=0.75)

        with self.beat(7.0, "(music only)"):
            self.play(FadeOut(*self.mobjects), run_time=0.8)
            key = Key(PRIVATE, 1.0)
            head = title("Encryption: a digital lock.", FG, 42)
            lockup = VGroup(key, head).arrange(RIGHT, buff=0.55)
            lockup.to_edge(UP, buff=0.7)
            self.play(DrawBorderThenFill(key), Write(head), run_time=1.9)
            tail = VGroup(
                body(CREDITS_CLASS, SNOOP, 21),
                body(CREDITS_TOOLS, SNOOP, 18),
            ).arrange(DOWN, buff=0.2)
            credits = VGroup(team_logo(), team_roster(), tail)
            credits.arrange(DOWN, buff=0.55)
            credits.next_to(lockup, DOWN, buff=0.6)
            self.play(FadeIn(credits, shift=UP * 0.3, lag_ratio=0.25), run_time=1.7)

        self.pad_to_target()
