"""The ten scenes of the encryption video.

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

from manim import *

from assets import *
from style import *

# The end card in Scene10Outro.
CREDITS_NAMES = "Otter Digital"
CREDITS_MEMBERS = ("Michael Ansara · Eric Griffin · Kenneth Joyce · "
                   "Chris Mobley · Derrick Patterson")
CREDITS_CLASS = "CST 349"
CREDITS_TOOLS = "Animated with manim.community"

MSG = "Meet at 3pm"


# --- 1. Intro (0:00-0:18) --------------------------------------------------


class Scene01Intro(VideoScene):
    TARGET = 16.25

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

        net = NetworkMap(cols=6, rows=4, spacing=1.15)
        net.scale(0.78).move_to(RIGHT * 2.7 + UP * 0.2)
        maya = Person(FG, height=1.9, name="Maya")
        maya.move_to(LEFT * 5.1 + DOWN * 0.4)
        phone = Phone(height=1.05).next_to(maya.figure, RIGHT, buff=0.18)

        with self.beat(2.9, "Every day, we send private information online:"):
            self.play(FadeIn(maya, shift=RIGHT * 0.4), FadeIn(phone, scale=0.8),
                      run_time=0.8)
            rays = VGroup(*[
                Line(phone.get_right(), net.at(0, j), color=PUBLIC,
                     stroke_width=2.4, stroke_opacity=0.55)
                for j in range(4)
            ])
            self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.18),
                      run_time=0.9)
            self.play(Create(net.lines, lag_ratio=0.04),
                      FadeIn(net.dots, lag_ratio=0.04), run_time=1.2)

        icons = VGroup(
            icon("chat", PLAIN, 0.8),
            icon("password", PUBLIC, 0.8),
            icon("card", PRIVATE, 0.8),
        ).arrange(DOWN, buff=0.52).move_to(LEFT * 1.9 + UP * 0.1)
        backdrop = VGroup(net, rays)

        with self.beat(2.65, "messages, passwords, and payment details."):
            self.play(backdrop.animate.set_opacity(0.28), run_time=0.35)
            self.play(
                LaggedStart(*[FadeIn(i, shift=UP * 0.3, scale=0.7) for i in icons],
                            lag_ratio=0.5),
                run_time=2.3,
            )

        with self.beat(2.4, "Encryption is what keeps it safe."):
            locks = VGroup(*[
                Padlock(PRIVATE, height=0.46).move_to(i.get_right() + RIGHT * 0.45)
                for i in icons
            ])
            self.play(
                LaggedStart(*[
                    AnimationGroup(GrowFromCenter(l), Flash(l, color=PRIVATE,
                                                            line_length=0.12,
                                                            flash_radius=0.4))
                    for l in locks
                ], lag_ratio=0.55),
                run_time=2.4,
            )

        note = Note(MSG, PLAIN, size=22).scale(0.72)
        with self.beat(5.3, "So, how does encryption actually work, and "
                             "why do we use it so often?"):
            self.play(FadeOut(icons, locks, shift=LEFT * 0.4),
                      backdrop.animate.set_opacity(1.0), run_time=0.6)
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
                run_time=3.0,
            )
            self.play(note.animate.move_to(ORIGIN).scale(1.3),
                      backdrop.animate.set_opacity(0.3), run_time=1.0)

        with self.beat(1.0, "(transition)"):
            self.play(FadeOut(backdrop, maya, phone, snoops),
                      note.animate.scale(1.9).move_to(ORIGIN), run_time=1.0)

        self.pad_to_target()


# --- 2. Plaintext and ciphertext (0:18-0:37) -------------------------------


class Scene02Ciphertext(VideoScene):
    TARGET = 13.34

    def construct(self):
        green = mono(MSG, PLAIN, size=38).move_to(LEFT * 3.6 + UP * 1.1)
        arrow = Arrow(LEFT * 1.3, RIGHT * 1.3, color=FG, buff=0,
                      stroke_width=7).shift(UP * 1.1)
        mark = Padlock(PRIVATE, height=0.5).next_to(arrow, UP, buff=0.18)
        red = mono(scrambled(MSG, seed=3), CIPHER, size=38)
        red.move_to(RIGHT * 3.6 + UP * 1.1)

        with self.beat(4.2, "Encryption is a way of turning a readable message "
                            "into a secret code."):
            self.play(Write(green), run_time=1.5)
            self.play(GrowArrow(arrow), run_time=0.8)
            self.play(FadeIn(mark, shift=DOWN * 0.25), run_time=0.5)
            self.play(TransformFromCopy(green, red), run_time=1.4)

        plabel = caption("PLAINTEXT", PLAIN).next_to(green, DOWN, buff=0.45)
        with self.beat(2.27, "The readable message is called plaintext."):
            self.play(Indicate(green, scale_factor=1.12, color=PLAIN), run_time=1.0)
            self.play(Write(plabel), run_time=0.9)

        clabel = caption("CIPHERTEXT", CIPHER).next_to(red, DOWN, buff=0.45)
        with self.beat(2.16, "After encryption, it becomes ciphertext,"):
            self.play(Write(clabel), run_time=0.9)
            scramble(self, red, steps=9, run_time=0.11)

        snoop = Snooper(height=2.0).move_to(RIGHT * 0.9 + DOWN * 1.9)
        qs = VGroup(*[Text("?", font_size=44, color=SNOOP) for _ in range(3)])
        qs.arrange(RIGHT, buff=0.42).move_to(RIGHT * 3.4 + DOWN * 1.1)
        qs[0].shift(DOWN * 0.22)
        qs[2].shift(UP * 0.22)

        with self.beat(3.7, "which looks like meaningless information to anyone "
                            "who isn't supposed to read it."):
            self.play(FadeIn(snoop, shift=UP * 0.5), run_time=0.8)
            self.play(Rotate(snoop, -0.22, about_point=snoop.get_bottom()),
                      run_time=0.7)
            self.play(LaggedStart(*[FadeIn(q, shift=UP * 0.3) for q in qs],
                                  lag_ratio=0.35), run_time=1.5)
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


# --- 3. Locked box (0:37-0:55) ---------------------------------------------


class Scene03LockedBox(MovingVideoScene):
    TARGET = 15.1

    def construct(self):
        box = Box(FG, width=2.9, height=1.9, open_=True).move_to(DOWN * 1.2)
        card = Note(scrambled(MSG, seed=11), CIPHER, size=26).scale(0.85)
        card.move_to(UP * 1.9)
        self.add(box, card)

        with self.beat(3.0, "Imagine putting a note inside a locked box."):
            self.play(card.animate.scale(0.62).move_to(box.inside()), run_time=1.3)
            self.bring_to_front(box)
            self.play(box.close_anim(run_time=1.0))
            self.play(VGroup(box, card).animate.move_to(ORIGIN), run_time=0.7)

        lbl_msg = caption("message", PLAIN).next_to(box, DOWN, buff=0.4)
        with self.beat(1.5, "The note is the message,"):
            self.play(box.body.animate.set_fill(opacity=0.25), run_time=0.5)
            self.play(Write(lbl_msg), Indicate(card, color=PLAIN, scale_factor=1.15),
                      run_time=1.0)

        lock = Padlock(PRIVATE, height=0.95)
        lock.move_to(box.body.get_right())
        lbl_enc = caption("encryption", PRIVATE).next_to(lock, RIGHT, buff=0.3)
        with self.beat(1.5, "the lock is the encryption,"):
            self.play(GrowFromCenter(lock), run_time=0.6)
            self.play(Write(lbl_enc), Flash(lock, color=PRIVATE, flash_radius=0.7),
                      run_time=0.9)

        key = Key(PRIVATE, height=0.75).move_to(RIGHT * 4.6)
        lbl_key = caption("key", PRIVATE).next_to(key, DOWN, buff=0.35)
        with self.beat(2.7, "and the key is what opens the box."):
            self.play(FadeIn(key, shift=LEFT * 0.5), Write(lbl_key), run_time=1.0)
            hole = lock.keyhole.get_center()
            self.play(key.animate.scale(0.75).move_to(hole + LEFT * 0.42),
                      FadeOut(lbl_key), run_time=0.9)
            self.play(Rotate(key, PI / 2, about_point=hole), run_time=0.8)

        parcel = VGroup(box, card, lock, key)
        with self.beat(5.4, "The person receiving the message needs the right key "
                            "to unlock it and read it."):
            snoopers = VGroup(Snooper(height=1.5), Snooper(height=1.5))
            snoopers.arrange(RIGHT, buff=2.6).move_to(DOWN * 2.3)
            sam = Person(FG, height=1.8, name="Sam").move_to(RIGHT * 5.0)
            self.play(
                FadeOut(lbl_msg, lbl_enc),
                parcel.animate.scale(0.72).move_to(LEFT * 4.6 + UP * 0.4),
                FadeIn(snoopers, shift=UP * 0.3), FadeIn(sam, shift=LEFT * 0.4),
                run_time=0.9,
            )
            self.play(
                parcel.animate.move_to(RIGHT * 2.1 + UP * 0.4),
                LaggedStart(*[Wiggle(s, scale_value=1.1) for s in snoopers],
                            lag_ratio=0.4),
                run_time=1.7,
            )
            sam_key = Key(PRIVATE, height=0.5).next_to(parcel, UP, buff=0.35)
            self.play(FadeIn(sam_key, shift=DOWN * 0.3), run_time=0.4)
            self.play(sam_key.animate.move_to(lock.keyhole.get_center()),
                      run_time=0.4)
            self.play(FadeOut(sam_key, key), lock.unlock_anim(), run_time=0.5)
            self.bring_to_front(card)
            self.play(box.open_anim(run_time=0.7),
                      card.animate.shift(UP * 0.85).scale(1.3), run_time=0.7)
            scramble(self, card.label, steps=4, run_time=0.1, settle=MSG)
            self.play(card.card.animate.set_stroke(PLAIN), run_time=0.3)

        with self.beat(1.0, "(transition)"):
            self.play(
                self.camera.frame.animate.scale(0.05).move_to(
                    lock.keyhole.get_center()),
                run_time=1.0,
            )

        self.pad_to_target()


# --- 4. The math (0:55-1:08) -----------------------------------------------


class Scene04Math(VideoScene):
    TARGET = 10.58

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

        with self.beat(2.9, "Computers do this with math."):
            self.play(FadeOut(field), ReplacementTransform(keyhole, machine),
                      run_time=1.1)
            self.play(Write(lab),
                      LaggedStart(GrowFromCenter(g1), GrowFromCenter(g2),
                                  lag_ratio=0.3), run_time=0.9)
            g1.add_updater(lambda m, dt: m.rotate(0.9 * dt))
            g2.add_updater(lambda m, dt: m.rotate(-1.35 * dt))
            self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.35) for s in syms],
                                  lag_ratio=0.25), run_time=0.9)

        key = Key(PRIVATE, height=0.75).rotate(-PI / 2)
        key.move_to(machine.get_top() + UP * 1.3)
        bits = mono("1011 0110", PRIVATE, 22)
        # the message travels through the machine along this line, kept clear
        # of the gears and the floating symbols
        lane = machine.get_center() + DOWN * 0.35

        with self.beat(3.8, "An encryption algorithm changes the message using "
                            "a secret key."):
            self.play(FadeIn(key, shift=DOWN * 0.4), run_time=0.5)
            self.play(key.animate.move_to(machine.get_top()), run_time=0.6)
            bits.move_to(machine.get_top() + DOWN * 0.5 + RIGHT * 1.15)
            self.play(TransformFromCopy(key.teeth, bits), run_time=0.7)
            green = mono(MSG, PLAIN, 26).move_to(LEFT * 9 + UP * lane[1])
            self.add(green)
            self.play(green.animate.move_to(lane + LEFT * 1.4), run_time=0.7)
            red = mono(scrambled(MSG, seed=5), CIPHER, 26)
            red.move_to(lane + RIGHT * 1.4)
            self.play(ReplacementTransform(green, red), run_time=0.5)
            self.play(red.animate.move_to(RIGHT * 9 + UP * lane[1]), run_time=0.8)
            self.remove(red)

        with self.beat(2.88, "The receiver then uses the correct key to change "
                            "it back."):
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


# --- 5. Symmetric encryption (1:08-1:29) -----------------------------------


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
    TARGET = 16.31

    def construct(self):
        p1, p2 = _panels()
        n1 = title("1", SNOOP, 70).move_to(p1)
        n2 = title("2", SNOOP, 70).move_to(p2)

        with self.beat(2.21, "There are two main types of encryption."):
            self.play(LaggedStart(Create(p1), Create(p2), lag_ratio=0.35),
                      run_time=1.3)
            self.play(Write(n1), Write(n2), run_time=0.9)

        lab = heading("SYMMETRIC", PRIVATE, 34)
        with self.beat(2.4, "The first is symmetric encryption."):
            self.play(p1.animate.set_stroke(PRIVATE),
                      ReplacementTransform(n1, lab.move_to(p1)),
                      VGroup(p2, n2).animate.set_opacity(0.22), run_time=1.1)
            self.play(FadeOut(p2, n2, shift=RIGHT * 1.5), *_expand(p1, lab),
                      run_time=1.3)

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

        with self.beat(2.8, "It's fast, so it's great for protecting lots of data."):
            self.play(FadeOut(box, lock, eq), run_time=0.4)
            files = VGroup(*[icon("file", FG, 0.62) for _ in range(15)])
            files.arrange_in_grid(rows=3, cols=5, buff=(0.4, 0.3))
            files.move_to(DOWN * 0.75)
            self.play(LaggedStart(*[FadeIn(f, scale=0.7) for f in files],
                                  lag_ratio=0.05), run_time=1.3)
            stamps = VGroup(*[
                Padlock(PRIVATE, 0.3).move_to(f.get_corner(DR)) for f in files
            ])
            self.play(LaggedStart(*[GrowFromCenter(s) for s in stamps],
                                  lag_ratio=0.04), run_time=1.1)

        with self.beat(4.5, "The challenge is that both people need to get the "
                            "same secret key safely."):
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


# --- 6. Asymmetric encryption (1:29-1:59) ----------------------------------


class Scene06Asymmetric(VideoScene):
    TARGET = 23.72

    def construct(self):
        p1, p2 = _panels()
        lab1 = caption("SYMMETRIC", SNOOP, 26).move_to(p1)
        p1.set_stroke(SNOOP)
        self.add(p1, p2, lab1)

        lab2 = heading("ASYMMETRIC", PUBLIC, 32).move_to(p2)
        with self.beat(2.7, "The second is asymmetric encryption,"):
            self.play(p2.animate.set_stroke(PUBLIC), Write(lab2),
                      VGroup(p1, lab1).animate.set_opacity(0.22), run_time=1.3)
            self.play(FadeOut(p1, lab1, shift=LEFT * 1.5), *_expand(p2, lab2),
                      run_time=1.4)

        with self.beat(2.01, "also called public-key encryption."):
            sub = caption("(public-key)", SNOOP, 22).next_to(lab2, DOWN, buff=0.12)
            self.play(FadeIn(sub, shift=DOWN * 0.15), run_time=0.9)

        kb = Key(PUBLIC, 0.85).move_to(LEFT * 0.9 + UP * 1.4)
        kg = Key(PRIVATE, 0.85).move_to(RIGHT * 0.9 + UP * 1.4)
        lb = caption("PUBLIC KEY", PUBLIC)
        lg = caption("PRIVATE KEY", PRIVATE)

        with self.beat(3.1, "It uses two keys: a public key and a private key."):
            self.play(FadeIn(kb, scale=0.7), FadeIn(kg, scale=0.7), run_time=0.7)
            self.play(kb.animate.move_to(LEFT * 3.8 + UP * 1.4),
                      kg.animate.move_to(RIGHT * 3.8 + UP * 1.4), run_time=1.2)
            lb.next_to(kb, DOWN, buff=0.35)
            lg.next_to(kg, DOWN, buff=0.35)
            self.play(Write(lb), Write(lg), run_time=1.2)

        crowd = VGroup(*[Person(FG, height=1.0) for _ in range(5)])
        crowd.arrange(RIGHT, buff=0.72).move_to(LEFT * 3.4 + DOWN * 2.2)

        with self.beat(2.4, "The public key can be shared with everyone."):
            self.play(FadeIn(crowd, shift=UP * 0.3, lag_ratio=0.12), run_time=0.7)
            copies = VGroup(*[
                Key(PUBLIC, 0.42).next_to(p, UP, buff=0.14) for p in crowd
            ])
            self.play(LaggedStart(*[TransformFromCopy(kb, c) for c in copies],
                                  lag_ratio=0.13), run_time=1.7)

        sam = Person(FG, height=1.6, name="Sam").move_to(RIGHT * 4.9 + DOWN * 1.7)
        glow = Circle(radius=0.82, color=PRIVATE, stroke_width=4,
                      fill_color=PRIVATE, fill_opacity=0.12)

        with self.beat(2.3, "The private key must be kept secret."):
            self.play(FadeIn(sam, shift=LEFT * 0.3), run_time=0.5)
            self.play(kg.animate.next_to(sam.figure, UP, buff=0.25), FadeOut(lg),
                      run_time=0.9)
            glow.move_to(kg)
            self.add(glow)
            self.bring_to_back(glow)
            self.play(Create(glow),
                      Flash(kg, color=PRIVATE, flash_radius=0.7), run_time=0.9)

        mb = Mailbox(height=3.0).move_to(RIGHT * 0.6 + DOWN * 0.5)
        with self.beat(1.8, "Think of a mailbox."):
            self.play(kb.animate.move_to(mb.slot_point()), FadeOut(lb),
                      run_time=0.6)
            rest = VGroup(*[m for m in mb.submobjects if m is not mb.slot])
            self.play(ReplacementTransform(kb, mb.slot), Create(rest), run_time=1.2)
            self.bring_to_front(mb.slot)

        with self.beat(3.5, "Anyone can drop a letter in, like using your public key."):
            envs = VGroup(*[
                Envelope(FG, 0.52).next_to(crowd[i], UP, buff=0.55)
                for i in (0, 2, 4)
            ])
            self.play(LaggedStart(*[FadeIn(e, scale=0.7) for e in envs],
                                  lag_ratio=0.2), run_time=0.9)
            self.play(
                LaggedStart(*[
                    Succession(
                        e.animate(run_time=0.9).move_to(mb.slot_point()).scale(0.55),
                        FadeOut(e, run_time=0.15),
                    ) for e in envs
                ], lag_ratio=0.4),
                run_time=2.6,
            )

        with self.beat(4.91, "But only you, with your private key, can open the "
                            "mailbox and read the letters."):
            self.play(sam.animate.move_to(RIGHT * 3.4 + DOWN * 1.7),
                      kg.animate.move_to(RIGHT * 3.4 + DOWN * 0.5),
                      glow.animate.move_to(RIGHT * 3.4 + DOWN * 0.5), run_time=0.9)
            self.play(FadeOut(glow),
                      kg.animate.scale(0.75).move_to(mb.knob.get_center()),
                      run_time=0.7)
            self.play(mb.open_door_anim(run_time=0.9))
            outs = VGroup(*[Envelope(PLAIN, 0.55) for _ in range(3)])
            outs.arrange(RIGHT, buff=0.45).next_to(mb, UP, buff=0.45)
            self.play(LaggedStart(*[FadeIn(e, shift=UP * 0.6) for e in outs],
                                  lag_ratio=0.2), run_time=1.1)
            notes = VGroup(*[Note(MSG, PLAIN, size=16) for _ in outs])
            notes.arrange(RIGHT, buff=0.3).next_to(mb, UP, buff=0.4)
            self.play(LaggedStart(*[
                ReplacementTransform(e, n) for e, n in zip(outs, notes)
            ], lag_ratio=0.2), run_time=1.3)

        with self.beat(1.0, "(transition)"):
            self.play(FadeOut(mb, notes, crowd, copies, sam, kg, lab2, sub, p2,
                              shift=LEFT * 1.2), run_time=1.0)

        self.pad_to_target()


# --- 7. Both together + HTTPS (1:59-2:25) ----------------------------------


def _parcel(width: float = 0.7):
    """A small locked box, for the streams of traffic in scenes 7 and 8."""
    b = Box(FG, width=width, height=width * 0.68)
    l = Padlock(PRIVATE, width * 0.42).move_to(b.body.get_center())
    return VGroup(b, l)


class Scene07Https(MovingVideoScene):
    TARGET = 20.79

    def construct(self):
        laptop = Laptop(FG, height=2.5).move_to(LEFT * 4.2 + DOWN * 0.7)
        server = Server(FG, height=3.0).move_to(RIGHT * 4.6 + DOWN * 0.5)

        with self.beat(2.74, "Many real systems use both types together."):
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

        with self.beat(6.5, "When you visit a secure website, public-key "
                            "encryption helps your device and the website agree "
                            "on a secret key."):
            self.play(FadeOut(merged), run_time=0.3)
            slot = RoundedRectangle(
                width=1.4, height=0.22, corner_radius=0.11, color=PUBLIC,
                fill_color=PUBLIC, fill_opacity=1, stroke_width=0,
            ).next_to(server, UP, buff=0.45)
            slot_lab = caption("public key", PUBLIC, 20).next_to(slot, UP, buff=0.18)
            self.play(GrowFromCenter(slot), FadeIn(slot_lab), run_time=0.9)
            newkey = Key(PRIVATE, 0.5).next_to(laptop, UP, buff=0.45)
            self.play(FadeIn(newkey, scale=0.5),
                      Flash(newkey, color=PRIVATE, flash_radius=0.6), run_time=0.9)
            arc = ArcBetweenPoints(newkey.get_center(), slot.get_center(),
                                   angle=-PI / 3)
            self.play(MoveAlongPath(newkey, arc), run_time=1.6)
            self.play(FadeOut(newkey, scale=0.4), run_time=0.4)
            srv_key = Key(PRIVATE, 0.45).next_to(server, DOWN, buff=0.35)
            self.play(FadeIn(srv_key, shift=UP * 0.2), run_time=0.5)
            self.play(FadeOut(slot, slot_lab),
                      ReplacementTransform(srv_key, shared_r),
                      FadeIn(shared_l, scale=0.6), run_time=0.9)
            eq = title("=", FG, 40).move_to(UP * 1.9)
            self.play(Write(eq), Indicate(shared_l, color=PRIVATE),
                      Indicate(shared_r, color=PRIVATE), run_time=1.0)

        with self.beat(3.54, "Then fast symmetric encryption protects the rest "
                            "of the conversation."):
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

        bar = BrowserBar("https://")
        bar.scale_to_fit_width(laptop.screen.width * 0.86)
        bar.move_to(laptop.screen.get_center() + UP * 0.38)

        with self.beat(3.1, "That's what the padlock symbol in your browser means."):
            self.play(FadeOut(shared_l, shared_r), run_time=0.3)
            self.play(FadeIn(bar), run_time=0.5)
            self.play(
                self.camera.frame.animate
                .scale_to_fit_height(laptop.screen.height * 1.6)
                .move_to(laptop.screen.get_center()),
                run_time=1.4,
            )
            self.play(Indicate(bar.lock, color=PRIVATE, scale_factor=1.35),
                      run_time=0.9)

        with self.beat(3.91, "HTTPS is encrypting the connection and protecting "
                            "your passwords, shopping information, and personal "
                            "details."):
            self.play(bar.url_text.animate.set_color(PLAIN),
                      Flash(bar.url_text, color=PLAIN, flash_radius=0.4),
                      run_time=0.9)
            trio = VGroup(
                icon("password", PUBLIC, 0.34),
                icon("cart", PUBLIC, 0.34),
                icon("id", PUBLIC, 0.34),
            ).arrange(RIGHT, buff=0.32).next_to(bar, DOWN, buff=0.3)
            self.play(
                LaggedStart(*[FadeIn(i, shift=UP * 0.12, scale=0.7) for i in trio],
                            lag_ratio=0.5),
                run_time=2.6,
            )

        with self.beat(1.0, "(transition)"):
            big = Padlock(PRIVATE, 1.7).move_to(ORIGIN)
            self.play(
                self.camera.frame.animate.scale_to_fit_height(
                    config.frame_height).move_to(ORIGIN),
                FadeOut(laptop, server, bar, trio),
                FadeIn(big, scale=0.4),
                run_time=1.0,
            )

        self.pad_to_target()


# --- 8. Everyday uses (2:25-2:51) ------------------------------------------


class Scene08Everyday(VideoScene):
    TARGET = 21.21

    def construct(self):
        lock = Padlock(PRIVATE, 1.7)
        self.add(lock)

        with self.beat(2.5, "Encryption is used in many parts of daily life."):
            ring = VGroup()
            for k, a in zip(("chat", "card", "file", "id", "cart", "email"),
                            np.linspace(0, TAU, 6, endpoint=False)):
                ic = icon(k, SNOOP, 0.55).set_opacity(0.5)
                ic.move_to(np.array([3.4 * np.cos(a), 2.1 * np.sin(a), 0]))
                ring.add(ic)
            self.play(LaggedStart(*[FadeIn(i) for i in ring], lag_ratio=0.12),
                      run_time=1.7)

            def orbit(m, dt):
                m.rotate(0.3 * dt, about_point=ORIGIN)
                for sub in m:  # counter-rotate so the icons stay upright
                    sub.rotate(-0.3 * dt)

            ring.add_updater(orbit)

        with self.beat(6.0, "Messaging apps can use end-to-end encryption, so a "
                            "message stays protected from one phone to another."):
            ring.clear_updaters()
            self.play(FadeOut(ring, lock), run_time=0.6)
            pa = Phone(FG, 2.3).move_to(LEFT * 5.0 + DOWN * 0.3)
            pb = Phone(FG, 2.3).move_to(RIGHT * 5.0 + DOWN * 0.3)
            self.play(FadeIn(pa, shift=RIGHT * 0.3), FadeIn(pb, shift=LEFT * 0.3),
                      run_time=0.8)
            bub = icon("chat", PLAIN, 0.85).move_to(pa.get_center())
            self.play(FadeIn(bub, scale=0.6), run_time=0.6)
            parcel = _parcel(1.1).move_to(bub)
            self.play(ReplacementTransform(bub, parcel), run_time=0.8)
            self.play(parcel.animate.move_to(pb.get_center()), run_time=1.9)
            bub2 = icon("chat", PLAIN, 0.85).move_to(pb.get_center())
            self.play(ReplacementTransform(parcel, bub2), run_time=0.8)
            e2e = caption("end-to-end", PLAIN, 22).move_to(DOWN * 2.6)
            self.play(FadeIn(e2e, shift=UP * 0.2), run_time=0.5)

        with self.beat(6.61, "Phones and computers can encrypt stored files, so "
                            "your information is harder to access if a device is "
                            "lost or stolen."):
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

        with self.beat(5.1, "Banks, online stores, hospitals, businesses, "
                            "government agencies, and VPNs use it too."):
            self.play(FadeOut(lap, junk, hand), run_time=0.5)
            kinds = ("bank", "cart", "hospital", "office", "government", "vpn")
            grid = VGroup(*[icon(k, FG, 1.05) for k in kinds])
            grid.arrange_in_grid(rows=2, cols=3, buff=(2.0, 1.2))
            self.play(
                LaggedStart(*[FadeIn(g, shift=UP * 0.3, scale=0.7) for g in grid],
                            lag_ratio=0.52),
                run_time=3.3,
            )
            stamps = VGroup(*[
                Padlock(PRIVATE, 0.42).move_to(g.get_corner(DR) + RIGHT * 0.4)
                for g in grid
            ])
            self.play(LaggedStart(*[GrowFromCenter(s) for s in stamps],
                                  lag_ratio=0.12), run_time=1.3)

        with self.beat(1.0, "(transition)"):
            maya = Person(FG, 1.9, "Maya").move_to(LEFT * 4.0 + DOWN * 0.4)
            phone = Phone(FG, 1.2).next_to(maya.figure, RIGHT, buff=0.25)
            mail = icon("email", CIPHER, 0.9).move_to(RIGHT * 1.6 + UP * 0.6)
            bang = title("!", CIPHER, 38).next_to(mail, RIGHT, buff=0.2)
            self.play(FadeOut(grid, stamps), FadeIn(maya, phone),
                      FadeIn(mail, shift=LEFT * 0.6), FadeIn(bang), run_time=1.0)

        self.pad_to_target()


# --- 9. Not magic (2:51-3:11) ----------------------------------------------


class Scene09NotMagic(VideoScene):
    TARGET = 15.15

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

        with self.beat(2.56, "Encryption is extremely important, but it isn't magic."):
            self.play(FadeIn(box, scale=0.85), GrowFromCenter(lock), run_time=1.0)
            self.add(halo)
            self.bring_to_back(halo)
            self.play(Create(halo), Indicate(lock, color=PRIVATE), run_time=1.3)

        mkey = Key(PRIVATE, 0.5).next_to(maya.figure, UP, buff=0.25)
        hood = Snooper(SNOOP, 1.8).move_to(LEFT * 2.3 + DOWN * 1.9)

        with self.beat(2.6, "It can't protect someone who gives away their password,"):
            pw = icon("password", CIPHER, 0.6).next_to(mail, DOWN, buff=0.35)
            self.play(FadeIn(pw, shift=DOWN * 0.2), run_time=0.7)
            self.play(FadeIn(hood, shift=UP * 0.4), FadeIn(mkey, scale=0.6),
                      run_time=0.8)
            self.play(mkey.animate.next_to(hood, UP, buff=0.15), run_time=1.1)

        with self.beat(1.3, "clicks a dangerous link,"):
            link = icon("link", CIPHER, 0.75).move_to(RIGHT * 2.6 + DOWN * 2.0)
            cur = icon("cursor", FG, 0.5).next_to(link, DR, buff=0.02)
            self.play(FadeIn(link), FadeIn(cur), run_time=0.5)
            self.play(cur.animate.shift(UP * 0.12 + LEFT * 0.12), run_time=0.2)
            red_flash = Rectangle(
                width=config.frame_width, height=config.frame_height,
                color=CIPHER, fill_color=CIPHER, fill_opacity=0.3, stroke_width=0,
            )
            self.play(FadeIn(red_flash), run_time=0.25)
            self.play(FadeOut(red_flash), run_time=0.35)

        with self.beat(2.6, "or lets a malicious program onto their device."):
            bug = icon("bug", CIPHER, 0.6).move_to(RIGHT * 1.4 + DOWN * 3.0)
            self.play(FadeIn(bug), run_time=0.4)
            crawl = ArcBetweenPoints(bug.get_center(), phone.get_center(),
                                     angle=-PI / 4)
            self.play(MoveAlongPath(bug, crawl), run_time=1.5)
            self.play(FadeOut(bug, scale=0.3),
                      Flash(phone, color=CIPHER, flash_radius=0.8), run_time=0.6)

        with self.beat(1.78, "Encryption protects the information,"):
            self.play(mkey.animate.scale(0.85).move_to(lock.keyhole.get_center()),
                      run_time=0.7)
            self.play(FadeOut(mkey, halo), lock.unlock_anim(),
                      box.open_anim(run_time=0.9), run_time=0.9)

        with self.beat(3.3, "but people still need strong passwords and safe "
                            "decisions."):
            self.play(FadeOut(box, lock, hood, link, cur, pw, mail, bang,
                              maya, phone), run_time=0.6)
            tips = VGroup(
                labelled(icon("password", PLAIN, 0.95), "strong passwords",
                         PLAIN, 21),
                labelled(icon("link", PLAIN, 0.95), "think before you click",
                         PLAIN, 21),
                labelled(icon("shield", PLAIN, 0.95), "keep devices updated",
                         PLAIN, 21),
            ).arrange(RIGHT, buff=1.4, aligned_edge=UP)
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.3) for t in tips],
                                  lag_ratio=0.45), run_time=2.7)

        with self.beat(1.0, "(transition)"):
            note = Note(MSG, PLAIN, 28)
            self.play(FadeOut(tips, shift=DOWN * 0.3), FadeIn(note, scale=0.4),
                      run_time=1.0)

        self.pad_to_target()


# --- 10. Outro (3:11-3:28) -------------------------------------------------


class Scene10Outro(VideoScene):
    TARGET = 15.05

    def construct(self):
        note = Note(MSG, PLAIN, 28).move_to(UP * 1.3 + RIGHT * 0.7)
        self.add(note)

        with self.beat(2.95, "In short, encryption is like a digital lock."):
            scramble(self, note.label, steps=6, run_time=0.08)
            self.play(note.card.animate.set_stroke(CIPHER), run_time=0.25)
            box = Box(FG, width=2.8, height=1.8, open_=True).move_to(DOWN * 1.1)
            self.play(Create(box), run_time=0.5)
            self.play(note.animate.scale(0.55).move_to(box.inside()), run_time=0.6)
            self.bring_to_front(box)
            self.play(box.close_anim(run_time=0.5))
            lock = Padlock(PRIVATE, 0.75).move_to(box.body.get_right())
            self.play(GrowFromCenter(lock),
                      Flash(lock, color=PRIVATE, flash_radius=0.6), run_time=0.6)

        parcel = VGroup(box, note, lock)
        with self.beat(5.1, "It keeps private information private while it's "
                            "being sent, stored, or shared."):
            self.play(parcel.animate.scale(0.45).move_to(LEFT * 5.6 + UP * 0.2),
                      run_time=0.6)
            track = Arrow(LEFT * 6.0 + DOWN * 0.6, LEFT * 2.9 + DOWN * 0.6,
                          color=SNOOP, buff=0, stroke_width=4)
            w1 = caption("sent", PLAIN, 24).move_to(LEFT * 4.4 + DOWN * 2.3)
            self.play(Create(track), Write(w1), run_time=0.6)
            self.play(parcel.animate.move_to(LEFT * 3.2 + UP * 0.2), run_time=0.9)
            folder = Folder(PUBLIC, 1.7).move_to(DOWN * 0.3)
            w2 = caption("stored", PLAIN, 24).move_to(DOWN * 2.3)
            self.play(FadeIn(folder, scale=0.8), Write(w2), run_time=0.6)
            self.bring_to_front(parcel)
            self.play(parcel.animate.scale(0.75).move_to(folder.shell.get_center()),
                      run_time=0.9)
            two = VGroup(Person(FG, 1.0), Person(FG, 1.0))
            two.arrange(RIGHT, buff=1.0).move_to(RIGHT * 4.4 + DOWN * 0.9)
            w3 = caption("shared", PLAIN, 24).move_to(RIGHT * 4.4 + DOWN * 2.3)
            self.play(FadeIn(two, lag_ratio=0.2), Write(w3), run_time=0.6)
            c1, c2 = parcel.copy(), parcel.copy()
            self.play(c1.animate.move_to(two[0].get_top() + UP * 0.5),
                      c2.animate.move_to(two[1].get_top() + UP * 0.5), run_time=0.9)

        with self.beat(7.0, "(music only)"):
            self.play(FadeOut(*self.mobjects), run_time=0.8)
            key = Key(PRIVATE, 1.0)
            head = title("Encryption: a digital lock.", FG, 42)
            VGroup(key, head).arrange(RIGHT, buff=0.55).move_to(UP * 1.1)
            self.play(DrawBorderThenFill(key), Write(head), run_time=1.9)
            credits = VGroup(
                body(CREDITS_NAMES, FG, 28),
                body(CREDITS_MEMBERS, FG, 21),
                body(CREDITS_CLASS, SNOOP, 21),
                body(CREDITS_TOOLS, SNOOP, 18),
            ).arrange(DOWN, buff=0.3).move_to(DOWN * 1.5)
            self.play(FadeIn(credits, shift=UP * 0.3, lag_ratio=0.25), run_time=1.7)

        self.pad_to_target()
