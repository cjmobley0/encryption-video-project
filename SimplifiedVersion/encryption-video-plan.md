# Simplified Encryption Video: Manim Proof of Concept

Oct 17, 2026 · @Chris Mobley

## At a glance

The whole video is animated in [Manim Community Edition](https://github.com/ManimCommunity/manim), with no AI-generated video. It runs about 3:30: a 2-second music intro, roughly 3:19 of narrated animation, and a 7-second end card. Manim renders every label, shape and transition exactly, so the visuals stay consistent from start to finish.

|  | Plan |
| --- | --- |
| Runtime | \~3:30 |
| Source | 100% Manim (plus narration and background music) |
| Structure | 10 scenes, 46 narrated beats, one beat per sentence or phrase |
| Pacing assumption | \~2.4 spoken words per second (\~145 words per minute), plus \~1 second for each scene transition |
| Text on screen | Short labels only (PLAINTEXT, PUBLIC KEY…), so viewers listen rather than read |

**Visual style for both.** Flat, geometric, 3Blue1Brown-like: a dark navy background (#14213D), thick clean outlines, no gradients. One color code everywhere:

| Meaning | Color | Hex |
| --- | --- | --- |
| Plaintext (readable) | Green | #3DDC97 |
| Ciphertext (scrambled) | Red-orange | #FF6B4A |
| Private / shared secret key | Gold | #FFC93C |
| Public key | Light blue | #5BC0EB |
| Attacker / snooper | Gray | #8D99AE |
| Labels and text | Off-white | #F1FAEE |

The recurring story: **Maya sends a note to Sam**. Maya and Sam are simple geometric figures (a circle head and rounded body) so they are quick to build from basic Manim shapes.

## Narration

This version stays close to the group's original script. The only changes are one short opening line, shorter sentences, and a few combined paragraphs so it fits the time. It is about 530 words, roughly 3:30 including the music intro, transitions and end card. The scene plan below splits it into timed beats with the exact words for each.

> **\[1\] Intro.** Every day, we send private information online: messages, passwords, and payment details. Encryption is what keeps it safe. So, how does encryption actually work, and why do we use it so often?
>
> **\[2\] Plaintext and ciphertext.** Encryption is a way of turning a readable message into a secret code. The readable message is called plaintext. After encryption, it becomes ciphertext, which looks like meaningless information to anyone who isn't supposed to read it.
>
> **\[3\] Locked box.** Imagine putting a note inside a locked box. The note is the message, the lock is the encryption, and the key is what opens the box. The person receiving the message needs the right key to unlock it and read it.
>
> **\[4\] The math.** Computers do this with math. An encryption algorithm changes the message using a secret key. The receiver then uses the correct key to change it back.
>
> **\[5\] Symmetric.** There are two main types of encryption. The first is symmetric encryption. It uses the same key to lock and unlock the information. It's fast, so it's great for protecting lots of data. The challenge is that both people need to get the same secret key safely.
>
> **\[6\] Asymmetric.** The second is asymmetric encryption, also called public-key encryption. It uses two keys: a public key and a private key. The public key can be shared with everyone. The private key must be kept secret. Think of a mailbox. Anyone can drop a letter in, like using your public key. But only you, with your private key, can open the mailbox and read the letters.
>
> **\[7\] Both together + HTTPS.** Many real systems use both types together. When you visit a secure website, public-key encryption helps your device and the website agree on a secret key. Then fast symmetric encryption protects the rest of the conversation. That's what the padlock symbol in your browser means. HTTPS is encrypting the connection and protecting your passwords, shopping information, and personal details.
>
> **\[8\] Everyday uses.** Encryption is used in many parts of daily life. Messaging apps can use end-to-end encryption, so a message stays protected from one phone to another. Phones and computers can encrypt stored files, so your information is harder to access if a device is lost or stolen. Banks, online stores, hospitals, businesses, government agencies, and VPNs use it too.
>
> **\[9\] Not magic.** Encryption is extremely important, but it isn't magic. It can't protect someone who gives away their password, clicks a dangerous link, or lets a malicious program onto their device. Encryption protects the information, but people still need strong passwords and safe decisions.
>
> **\[10\] Outro.** In short, encryption is like a digital lock. It keeps private information private while it's being sent, stored, or shared.

## Scene plan

Each row is one beat: the words spoken in that window and what Manim shows while they are spoken. Times assume \~2.4 words per second, with slower pacing on lists so each item gets its own visual. Re-time after recording the real narration; the order of beats stays the same.

### 1. Intro (0:00–0:18)

| Time | Narration | On screen |
| --- | --- | --- |
| 0:00–0:02 | *(music only)* | Navy screen. A gold key draws itself; the title "Encryption" writes on beside it, then both shrink to the top corner and fade. |
| 0:02–0:05 | "Every day, we send private information online:" | Maya (circle-head figure) appears holding a phone. Light-blue network lines spread out from the phone to a grid of glowing dots, like a city map. |
| 0:05–0:08 | "messages, passwords, and payment details." | Three icons pop up beside the phone, one per word: chat bubble, password field (••••), credit card. |
| 0:08–0:11 | "Encryption is what keeps it safe." | A small gold padlock snaps onto each icon in turn. |
| 0:11–0:17 | "So, how does encryption actually work, and why do we use it so often?" | Icons fade. A green note leaves the phone and travels along the network lines, passing gray figures at the dots who turn to watch. The note glides to the center of the screen. |
| 0:17–0:18 | *(transition)* | The note grows to fill the middle of the frame. |

### 2. Plaintext and ciphertext (0:18–0:37)

| Time | Narration | On screen |
| --- | --- | --- |
| 0:18–0:24 | "Encryption is a way of turning a readable message into a secret code." | "Meet at 3pm" writes on in green. An arrow grows to the right, and a scrambled red copy appears at its tip. |
| 0:24–0:27 | "The readable message is called plaintext." | The green text pulses; the label **PLAINTEXT** writes on underneath. |
| 0:27–0:30 | "After encryption, it becomes ciphertext," | The red text keeps flickering through random characters; the label **CIPHERTEXT** writes on underneath. |
| 0:30–0:36 | "which looks like meaningless information to anyone who isn't supposed to read it." | A gray figure leans toward the red text; three "?" marks pop above its head. |
| 0:36–0:37 | *(transition)* | The green copy fades. The red note folds and drops into an open box. |

### 3. Locked box (0:37–0:55)

| Time | Narration | On screen |
| --- | --- | --- |
| 0:37–0:41 | "Imagine putting a note inside a locked box." | The note settles into the box and the lid swings shut. |
| 0:41–0:43 | "The note is the message," | The box turns semi-transparent so the note glows inside; label **message**. |
| 0:43–0:45 | "the lock is the encryption," | A padlock snaps onto the box; label **encryption**. |
| 0:45–0:48 | "and the key is what opens the box." | A gold key appears; label **key**. It slides into the padlock and turns a quarter turn. |
| 0:48–0:54 | "The person receiving the message needs the right key to unlock it and read it." | The box slides right past two gray figures who rattle it with no luck. Sam receives it, opens it with a matching gold key, and the note unscrambles back to green "Meet at 3pm". |
| 0:54–0:55 | *(transition)* | The camera zooms into the padlock's keyhole. |

### 4. The math (0:55–1:08)

| Time | Narration | On screen |
| --- | --- | --- |
| 0:55–0:58 | "Computers do this with math." | The keyhole fills the screen and becomes a box labeled **ALGORITHM** with spinning gears. A few math symbols (+, ×, =) float through it. |
| 0:58–1:02 | "An encryption algorithm changes the message using a secret key." | A gold key plugs into the top; its teeth morph into "1011 0110". Green "Meet at 3pm" enters from the left and exits the right side as red ciphertext. |
| 1:02–1:07 | "The receiver then uses the correct key to change it back." | The flow reverses: red enters from the right and comes out the left as green. |
| 1:07–1:08 | *(transition)* | The key slides out of the machine; the machine fades. |

### 5. Symmetric encryption (1:08–1:29)

| Time | Narration | On screen |
| --- | --- | --- |
| 1:08–1:11 | "There are two main types of encryption." | Two empty panels appear side by side, numbered 1 and 2. |
| 1:11–1:14 | "The first is symmetric encryption." | Panel 1 brightens with the label **SYMMETRIC**; panel 2 dims. |
| 1:14–1:18 | "It uses the same key to lock and unlock the information." | The gold key duplicates. Maya holds one, Sam holds the other, with an "=" between them. Maya locks a box; Sam unlocks it. |
| 1:18–1:22 | "It's fast, so it's great for protecting lots of data." | A tall stack of files appears; padlocks ripple onto every file in under a second. |
| 1:22–1:28 | "The challenge is that both people need to get the same secret key safely." | A key copy travels along a dashed line from Maya toward Sam. A gray hand rises from below the line, and a large "?" appears. |
| 1:28–1:29 | *(transition)* | The hand grabs at the key, but the key splits into two keys: one light blue, one gold. |

### 6. Asymmetric encryption (1:29–1:59)

| Time | Narration | On screen |
| --- | --- | --- |
| 1:29–1:32 | "The second is asymmetric encryption," | Panel 2 brightens with the label **ASYMMETRIC**. |
| 1:32–1:34 | "also called public-key encryption." | "(public-key)" fades in under the label. |
| 1:34–1:39 | "It uses two keys: a public key and a private key." | The blue key slides left with the label **PUBLIC KEY**; the gold key slides right with **PRIVATE KEY**. |
| 1:39–1:42 | "The public key can be shared with everyone." | Copies of the blue key fan out to five small figures around the screen. |
| 1:42–1:45 | "The private key must be kept secret." | The gold key moves to Sam; a glowing circle surrounds it. |
| 1:45–1:47 | "Think of a mailbox." | A mailbox builds itself around the blue key, which becomes its letter slot. |
| 1:47–1:52 | "Anyone can drop a letter in, like using your public key." | Three figures slide up one at a time and drop envelopes through the slot. |
| 1:52–1:58 | "But only you, with your private key, can open the mailbox and read the letters." | Sam walks up; the gold key opens the mailbox door. Envelopes fly out and unfold into green text. |
| 1:58–1:59 | *(transition)* | The mailbox shrinks and slides left; a laptop and a server slide in. |

### 7. Both together + HTTPS (1:59–2:25)

| Time | Narration | On screen |
| --- | --- | --- |
| 1:59–2:02 | "Many real systems use both types together." | A laptop on the left and a server on the right. A gold key icon and a blue-and-gold key icon float above them and merge. |
| 2:02–2:10 | "When you visit a secure website, public-key encryption helps your device and the website agree on a secret key." | The server shows a blue mailbox slot. The laptop makes a new gold key, sends it along a line, and drops it in the slot. The server opens it with its private key. Both now hold matching gold keys. |
| 2:10–2:14 | "Then fast symmetric encryption protects the rest of the conversation." | A rapid stream of small locked boxes flows back and forth between the laptop and server. |
| 2:14–2:18 | "That's what the padlock symbol in your browser means." | The camera zooms into the laptop screen: a drawn browser bar with a padlock and "https://" that pulses. |
| 2:18–2:24 | "HTTPS is encrypting the connection and protecting your passwords, shopping information, and personal details." | "https" glows. Three icons pop under the bar, one per item: password field, shopping cart, ID card. |
| 2:24–2:25 | *(transition)* | The padlock lifts off the browser bar and floats to the center. |

### 8. Everyday uses (2:25–2:51)

| Time | Narration | On screen |
| --- | --- | --- |
| 2:25–2:29 | "Encryption is used in many parts of daily life." | The padlock sits in the center; faint icons orbit around it. |
| 2:29–2:36 | "Messaging apps can use end-to-end encryption, so a message stays protected from one phone to another." | Two phones, left and right. A chat bubble locks into a small box, travels across, and opens only when it reaches the second phone. |
| 2:36–2:44 | "Phones and computers can encrypt stored files, so your information is harder to access if a device is lost or stolen." | A laptop with a folder; a padlock stamps onto the folder. A gray hand pulls the laptop away and opens the folder, but finds only red scrambled text. |
| 2:44–2:50 | "Banks, online stores, hospitals, businesses, government agencies, and VPNs use it too." | A 3×2 grid fills in, one icon per word: bank, shopping cart, hospital cross, office building, government building, VPN shield. A padlock stamps each. |
| 2:50–2:51 | *(transition)* | The grid fades; Maya and her phone return. An email icon with a red "!" arrives. |

### 9. Not magic (2:51–3:11)

| Time | Narration | On screen |
| --- | --- | --- |
| 2:51–2:55 | "Encryption is extremely important, but it isn't magic." | A locked box sits in the center, glowing and solid. |
| 2:55–2:59 | "It can't protect someone who gives away their password," | The email opens with a password field. Maya hands her gold key to a gray hooded figure who appears from the phone. |
| 2:59–3:01 | "clicks a dangerous link," | A red link icon appears; a cursor clicks it and the screen flashes red. |
| 3:01–3:04 | "or lets a malicious program onto their device." | A small red bug crawls into the phone. |
| 3:04–3:06 | "Encryption protects the information," | The hooded figure opens the box with the stolen key. The lid lifts cleanly: nothing is broken. |
| 3:06–3:10 | "but people still need strong passwords and safe decisions." | Three icons write on in a row: strong password, think before you click, keep devices updated. |
| 3:10–3:11 | *(transition)* | A rewind effect pulls everything back to the green note from Scene 2. |

### 10. Outro (3:11–3:28)

| Time | Narration | On screen |
| --- | --- | --- |
| 3:11–3:15 | "In short, encryption is like a digital lock." | A fast replay: green note scrambles to red, drops into the box, padlock snaps shut. |
| 3:15–3:21 | "It keeps private information private while it's being sent, stored, or shared." | One visual per verb: the box travels along a line (sent), rests inside a folder (stored), and copies to two friends (shared). |
| 3:21–3:28 | *(music only)* | Title "Encryption: a digital lock." End card with group names, class, and "Animated with Manim Community Edition". |

## Manim build guide

Build the reusable objects once in a shared file, then write one Manim `Scene` class per scene. Claude Code can draft each scene from the beat tables above; review, render and tweak.

**1. Setup**

1. Install Manim Community Edition by following the official installation guide (`pip install manim` plus its system dependencies).
2. Use only `Text` (not `MathTex` or `Tex`) for all labels, so you can skip installing LaTeX.
3. Render low quality while iterating and high quality at the end:
   - `manim -pql scenes.py Scene02Ciphertext` for a fast 480p preview
   - `manim -qh scenes.py Scene02Ciphertext` for the 1080p final

**2. Project structure**

```
encryption-video/
  style.py        # colors, fonts, background, timing helper
  assets.py       # all reusable objects (table below)
  scenes.py       # Scene01Intro ... Scene10Outro
  audio/          # narration per scene (scene01.mp3 ...) + music
  renders/        # rendered scene videos
  edit/           # editor project that joins scenes, audio, captions
```

**3. Shared objects (`assets.py`).** Each is a small `VGroup` built from basic shapes, so every scene uses the identical drawing.

| Object | Built from | Used in scenes |
| --- | --- | --- |
| `Key(color)` | Circle (bow) + Rectangle (shaft) + small rectangles (teeth) | 1, 3, 4, 5, 6, 7, 9, 10 |
| `Box()` | Rectangle body + Rectangle lid that rotates on a corner | 2, 3, 5, 9, 10 |
| `Padlock()` | Arc (shackle) + RoundedRectangle (body) | 1, 3, 7, 8 |
| `Note(text, color)` | RoundedRectangle + `Text` | 1, 2, 3, 10 |
| `ScrambleText(msg)` | `Text` cycled through random characters, then settled | 2, 3, 4, 8, 10 |
| `Person(color)` | Circle head + RoundedRectangle body (Maya, Sam, crowd) | 1, 3, 5, 6, 9 |
| `Snooper()` / `HoodedFigure()` | Gray `Person` with a triangle hood | 1, 2, 3, 9 |
| `GrabHand()` | Gray rounded polygon rising from the bottom edge | 5, 8 |
| `NetworkMap()` | Grid of `Dot`s joined by light-blue `Line`s | 1 |
| `Mailbox()` | RoundedRectangle + slot + door Rectangle + post | 6, 7 |
| `Envelope()` | Rectangle + two Lines for the flap | 6 |
| `Phone()`, `Laptop()`, `Server()` | RoundedRectangles with screen insets; server as stacked bars | 1, 7, 8, 9 |
| `BrowserBar()` | RoundedRectangle + small `Padlock` + `Text("https://")` | 7 |
| `Gear()` | Circle + small rectangles around the edge | 4 |
| `FileStack()`, `Folder()` | Offset rectangles; tabbed rectangle | 5, 8 |
| Icons (chat, password field, card, cart, ID, bank, hospital, office, government, VPN shield, link, bug, email) | Simple shapes, or free SVG icons loaded with `SVGMobject` | 1, 7, 8, 9 |

**4. Animation recipes per scene**

| # | Core Manim moves |
| --- | --- |
| 1 | `Create` the key and `Write` the title; `Create` the `NetworkMap` lines with `lag_ratio`; icons appear with `LaggedStart(FadeIn(...))`; padlocks with `GrowFromCenter`; note travels with `MoveAlongPath` on a path through the dots while snoopers `Rotate` to face it. |
| 2 | `Write` green text; `GrowArrow`; scramble loop with `Transform` at `run_time=0.1`; labels with `Write`; "?" marks with `FadeIn(shift=UP)`; fold with `ApplyMethod(note.stretch, 0.1, 1)` then `animate.move_to(box)`. |
| 3 | `Rotate` the lid shut; set box `fill_opacity` to show the note; key turn with `Rotate(key, PI/2)`; `box.animate.shift(RIGHT*6)`; `Wiggle` the snoopers; reverse the scramble on arrival. |
| 4 | Use `MovingCameraScene` and `self.camera.frame.animate.scale(0.2).move_to(keyhole)`; gears spin with an updater; `Transform` key teeth into `Text("1011 0110")`; text flows with `animate.shift`. |
| 5 | Panels as `RoundedRectangle`s; `TransformFromCopy` duplicates the key; files lock with `LaggedStart(..., lag_ratio=0.05)`; traveling key uses `MoveAlongPath` on a `DashedLine`; hand rises with `animate.shift(UP)`; `ReplacementTransform` one key into two. |
| 6 | Labels with `Write`; blue key copies fan out with `LaggedStart(TransformFromCopy...)`; mailbox assembles with `Create` around the blue key, then `Transform` the key into the slot; envelopes drop with `MoveAlongPath`; door opens with `Rotate`. |
| 7 | Key travels with `MoveAlongPath`; box stream as a `LaggedStart` of small `Box` copies shifting both ways; zoom with `self.camera.frame`; `Indicate` the padlock and "https://". |
| 8 | Locked chat bubble travels with `MoveAlongPath`; padlock stamp as `animate.scale(1.3)` then back; hand pulls laptop off-screen and the folder opens to `ScrambleText`; icon grid with `LaggedStart(FadeIn(...))` timed one icon per spoken word. |
| 9 | Key handoff with `animate.move_to(hooded_figure)`; red flash with `Flash` or a full-screen rectangle fading in and out; bug crawls with `MoveAlongPath`; lid lifts with `Rotate` and no shake; tip icons with `Write`. |
| 10 | Rebuild Scene 2–3 objects and play them at about 0.4× the original `run_time`; three mini-vignettes for sent, stored, shared; `Write` the closing title. |

**5. Starter code (Scene 2, first two beats).** A starting point for the core effect; test and adjust.

```python
from manim import *
import random, string

BG, PLAIN, CIPHER = "#14213D", "#3DDC97", "#FF6B4A"
config.background_color = BG

class Scene02Ciphertext(Scene):
    def construct(self):
        msg = "Meet at 3pm"
        note = Text(msg, color=PLAIN).scale(1.3)
        label = Text("PLAINTEXT", color=PLAIN).scale(0.5).next_to(note, DOWN)
        self.play(Write(note), FadeIn(label))
        self.wait(0.5)

        pool = string.ascii_letters + string.digits + "#$%&*@!?"
        for _ in range(7):
            noise = "".join(c if c == " " else random.choice(pool) for c in msg)
            self.play(Transform(note, Text(noise, color=CIPHER).scale(1.3).move_to(note)),
                      run_time=0.1)

        new_label = Text("CIPHERTEXT", color=CIPHER).scale(0.5).move_to(label)
        self.play(Transform(label, new_label))
        self.wait(1)
```

**6. Syncing to the narration.** Treat each beat's time window as its duration. In each scene, sum the `run_time` of the animations in a beat, then add `self.wait()` to fill the rest of the window. After recording the real narration, measure each sentence and update the windows. The `manim-voiceover` plugin is an optional way to time animations to the narration automatically.

## Proof-of-concept test

Build Scenes 2, 3 and 6 first (0:18–0:55 and 1:29–1:59, about 67 seconds). Together they test the core objects (note, box, keys, mailbox), the morph transitions, and how well beat timing matches real narration.

- [ ] Install Manim and render the starter Scene 2 code at low quality
- [ ] Build `Note`, `ScrambleText`, `Box`, `Padlock`, `Key`, `Person`, `Mailbox` and `Envelope` in `assets.py`
- [ ] Animate Scenes 2 → 3 as one continuous sequence (scramble, fold into box, lock, deliver past snoopers, unlock)
- [ ] Animate Scene 6 (key split, labels, fan-out to the crowd, mailbox build, envelopes, unlock)
- [ ] Record or generate narration for those beats and re-time each beat window to the real audio
- [ ] Join the renders and audio in an editor (CapCut, DaVinci Resolve or Canva) and add captions
- [ ] Review as a group: does each visual land on its words, are labels readable, do transitions feel smooth?

**If it works,** build the remaining scenes in order, reusing the same assets. **If timing feels rushed,** slow the narration slightly or drop a visual from the busiest beats (2:02–2:10 and 2:36–2:44) rather than cutting words.
