# Simplified Encryption Video: Manim Proof of Concept

Oct 17, 2026 · @Chris Mobley

## At a glance

The whole video is animated in [Manim Community Edition](https://github.com/ManimCommunity/manim), with no AI-generated video. With Part 1 added it runs **3:42**: 0:56 of "why it matters" and history, then 2:45 on how encryption works. Manim renders every label, shape and transition exactly, so the visuals stay consistent from start to finish.

**Runtime:** 3:42 is inside the 3–4 minute window set earlier, so none of the trims this plan used to list are needed. The narration came in quicker than the 2.4 words per second it was planned at — the read averages about 2.9 — and the beat windows below are the lengths of the lines as they were actually recorded rather than estimates.

|  | Plan |
| --- | --- |
| Runtime | 3:42 (Part 1: 0:56, Part 2: 2:45) |
| Source | 100% Manim (plus narration and background music) |
| Structure | Part 1 (Scenes A–C) + 10 scenes, 64 beats of which 50 are narrated |
| Pacing | Measured from the two recorded reads, not assumed |
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

Both parts are the group's own script, read straight through in two takes and
cut into one clip per beat. The wording below is what was actually recorded,
which is the group's original script rather than the shortened version this
plan carried before: the read ran several sentences together, split the VPN
sentence out on its own, reached everyday life before the browser padlock, and
added a sentence about the two keys that the shorter version had dropped. The
animation was conformed to the read rather than the read re-recorded.

Part 1 is used word for word; "two thousand and one" is read as the words and
the screen shows 2001. Part 2 no longer opens with "Every day, we send private
information online…", because Part 1 now does that job, and it starts on the
group's own question instead.

> ***Part 1: Why it matters and a short history***
>
> **\[A. Why it matters\]** When you check your bank account online, information travels between your device and the bank. Encryption helps keep it private. Even if someone intercepts the data, they shouldn't be able to read it without the right key.
>
> **\[B. Caesar and Enigma\]** Protecting messages isn't a new challenge. Julius Caesar used a cipher that shifted letters along the alphabet. It could hide a message from a casual reader, but it's easy to break now. During World War Two, German forces used Enigma machines that changed how letters were scrambled with every keystroke. Polish mathematicians made early breakthroughs, and Allied codebreakers built on that work.
>
> **\[C. Computers and AES\]** As computers spread into everyday life, encryption had to protect more than military messages. In the nineteen seventies, researchers developed new ways for computers to protect data and establish shared keys. In two thousand and one, the United States adopted the Advanced Encryption Standard, or AES, to protect sensitive digital information. Today, AES is widely used to protect data on devices and across networks.
>
> ***Part 2: How encryption works***
>
> **\[1\] The big question.** So, how does encryption actually work and why do we use it so often?
>
> **\[2\] Plaintext and ciphertext.** Encryption is a way of turning a readable message into a secret code. The readable message is called plaintext. After encryption, it becomes ciphertext, which should look like meaningless information to anyone who's not supposed to read it.
>
> **\[3\] Locked box.** Imagine putting a note inside a locked box. The note is the original message. The lock is the encryption process, and the key is what unlocks the box. The person receiving the message needs the right key to be able to unlock it and read it.
>
> **\[4\] The math.** Computers do this using complicated mathematics. An encryption algorithm changes the message using a secret key. The receiver then uses the correct key to change it back.
>
> **\[5\] Symmetric.** There are two main types of encryption. The first is symmetric encryption. It uses the same key to lock and unlock the information. This is very useful for protecting large amounts of data. The challenge is that both people or devices need to receive the same secret key safely.
>
> **\[6\] Asymmetric.** Second is asymmetric encryption, also called public key encryption. This uses a public key and a private key. The public key can be shared with everyone. The private key must be kept secret. Someone can send you an encrypted message with your public key, but only your private key should be able to unlock it. A useful example is a mailbox. Anyone can put letters inside, like using a public key, but only the person with the private key could open the mailbox and read the letters.
>
> **\[7\] Both together, HTTPS and daily life.** Many real systems use both types together. For example, when visiting a secure website, public key encryption helps your device and the website agree on a secret key. Then, fast symmetric encryption protects the rest of the conversation. Encryption is used in many parts of daily life. When you see a padlock symbol in your web browser, HTTPS is helping encrypt the connection between your device and the website. This helps protect passwords, shopping information, and other personal details.
>
> **\[8\] Everyday uses.** Messaging apps can use end-to-end encryption so that a message is protected while traveling from one phone to another. Phones and computers can also encrypt stored files to make sure that information is harder to access if the device is lost or stolen. Encryption is used by banks, online stores, hospitals, businesses, and government agencies. It's also used to protect the information sent through virtual private networks or VPNs.
>
> **\[9\] Not magic.** Encryption is extremely important, but it is not magic. It cannot protect someone who gives away their password, clicks on a dangerous link, or allows a malicious program onto the device. Encryption protects the information, but people still need to use strong passwords and make safe decisions.
>
> **\[10\] Outro.** In short, encryption is like a digital lock. It helps keep private information private while it's being sent, stored, or shared.

## Scene plan

Each row is one beat: the words spoken in that window and what Manim shows
while they are spoken. Every narrated window is the measured length of that
line in the recording plus 0.35s of breathing room, or the length of its own
animation where the picture needs longer than the line. Timecodes run
continuously from the title card (0:00) to the end card (3:42).
`narrate.py retime` writes these numbers, so re-run it after any re-record and
bring this table with it. Part 1 scenes are lettered A–C so the existing scene
numbers, and the audio already named after them, stay the same.

**Part 1: Why it matters and a short history (0:00–0:56)**

### A. Why it matters (0:00–0:12)

| Time | Narration | On screen |
| --- | --- | --- |
| 0:00–0:02 | *(music only)* | Navy screen. A gold key draws itself; the title "Encryption" writes on beside it, then both shrink to the top corner and fade. |
| 0:02–0:05 | "When you check your bank account online, information travels between your device and the bank." | Maya holds a phone showing a bank app. Light-blue network lines spread from the phone across a grid of glowing dots, like a city map, to a bank building. |
| 0:05–0:07 | "Encryption helps keep it private." | A data packet on the line takes a gold padlock. |
| 0:07–0:11 | "Even if someone intercepts the data, they shouldn't be able to read it without the right key." | A gray figure at one of the dots takes a copy of the packet and opens it: only red scrambled symbols. A "?" pops above its head. |
| 0:11–0:12 | *(transition)* | The city fades; a history timeline draws along the bottom: **Ancient Rome · 1940s · 1970s · 2001 · Today**. The marker sits on Ancient Rome. |

### B. Caesar and Enigma (0:12–0:32)

| Time | Narration | On screen |
| --- | --- | --- |
| 0:12–0:14 | "Protecting messages isn't a new challenge." | A rolled scroll appears above the marker. |
| 0:14–0:17 | "Julius Caesar used a cipher that shifted letters along the alphabet." | Two alphabet rows; the lower row slides 3 places. "MEET" turns into **PHHW**, one letter at a time, each drawn from its own cell. |
| 0:17–0:21 | "It could hide a message from a casual reader, but it's easy to break now." | A passer-by shrugs at PHHW. Then a laptop runs through the offsets and **MEET** falls out in green. |
| 0:21–0:26 | "During World War Two, German forces used Enigma machines that changed how letters were scrambled with every keystroke." | The marker slides to the 1940s. A simple Enigma: three rotor wheels over a lamp board. The A key is pressed five times; the rotors click and a different lamp lights each time: **B, D, Z, G, O**. |
| 0:26–0:31 | "Polish mathematicians made early breakthroughs, and Allied codebreakers built on that work." | A figure labelled **Poland** passes a glowing notebook to one labelled **Allied codebreakers**. The lit letters give **AAAAA** back. |
| 0:31–0:32 | *(transition)* | The marker slides to the 1970s. |

### C. Computers and AES (0:32–0:56)

| Time | Narration | On screen |
| --- | --- | --- |
| 0:32–0:37 | "As computers spread into everyday life, encryption had to protect more than military messages." | A military envelope multiplies into everyday icons: email, bank card, chat, shopping cart. |
| 0:37–0:43 | "In the nineteen seventies, researchers developed new ways for computers to protect data and establish shared keys." | Label **1970s**. Two computers: a block of data takes a padlock (protect data), then both ends end up holding matching gold keys (shared keys). |
| 0:43–0:50 | "In two thousand and one, the United States adopted the Advanced Encryption Standard, or AES, to protect sensitive digital information." | The marker slides to **2001**. An **AES** card drops in and a seal stamps it **U.S. standard**; files, a card and an ID take padlocks. |
| 0:50–0:55 | "Today, AES is widely used to protect data on devices and across networks." | The marker slides to **Today**. The card shrinks into a small badge that hops onto a phone, a laptop and a network line. |
| 0:55–0:56 | *(transition)* | The timeline fades; Maya, her phone and the network return — the picture Part 2 opens on. |

**Part 2: How encryption works (0:56–3:42)**

### 1. The big question (0:56–1:01)

| Time | Narration | On screen |
| --- | --- | --- |
| 0:56–1:00 | "So, how does encryption actually work and why do we use it so often?" | A green note leaves Maya's phone and travels along the network lines, passing gray figures who turn to watch. The note glides to the centre of the screen. |
| 1:00–1:01 | *(transition)* | The note grows to fill the middle of the frame. |

### 2. Plaintext and ciphertext (1:01–1:13)

| Time | Narration | On screen |
| --- | --- | --- |
| 1:01–1:04 | "Encryption is a way of turning a readable message into a secret code." | "Meet at 3pm" writes on in green. An arrow grows to the right under a gold padlock, and a scrambled red copy appears at its tip. |
| 1:04–1:06 | "The readable message is called plaintext." | The green text pulses; the label **PLAINTEXT** writes on underneath. |
| 1:06–1:12 | "After encryption, it becomes ciphertext, which should look like meaningless information to anyone who's not supposed to read it." | The label **CIPHERTEXT** writes on under the red text, which keeps flickering through random characters. A gray figure leans toward it and three "?" marks pop above its head. |
| 1:12–1:13 | *(transition)* | The green copy fades. The red note folds and drops into an open box. |

### 3. Locked box (1:13–1:27)

| Time | Narration | On screen |
| --- | --- | --- |
| 1:13–1:16 | "Imagine putting a note inside a locked box." | The note settles into the box and the lid swings shut. |
| 1:16–1:18 | "The note is the original message." | The box turns semi-transparent so the note glows inside; label **message**. |
| 1:18–1:22 | "The lock is the encryption process, and the key is what unlocks the box." | A padlock snaps onto the box; label **encryption**. A gold key appears, labelled **key**, slides into the padlock and turns a quarter turn. |
| 1:22–1:26 | "The person receiving the message needs the right key to be able to unlock it and read it." | The box slides right past two gray figures who rattle it with no luck. Sam receives it, opens it with a matching gold key, and the note unscrambles back to green "Meet at 3pm". |
| 1:26–1:27 | *(transition)* | The camera zooms into the padlock's keyhole. |

### 4. The math (1:27–1:37)

| Time | Narration | On screen |
| --- | --- | --- |
| 1:27–1:30 | "Computers do this using complicated mathematics." | The keyhole fills the screen and becomes a box labelled **ALGORITHM** with spinning gears. A few math symbols (+, ×, =) float through it. |
| 1:30–1:33 | "An encryption algorithm changes the message using a secret key." | A gold key plugs into the top; its teeth morph into "1011 0110". Green "Meet at 3pm" enters from the left and exits the right side as red ciphertext. |
| 1:33–1:36 | "The receiver then uses the correct key to change it back." | The flow reverses: red enters from the right and comes out the left as green. |
| 1:36–1:37 | *(transition)* | The key slides out of the machine; the machine fades. |

### 5. Symmetric encryption (1:37–1:54)

| Time | Narration | On screen |
| --- | --- | --- |
| 1:37–1:39 | "There are two main types of encryption." | Two empty panels appear side by side, numbered 1 and 2. |
| 1:39–1:42 | "The first is symmetric encryption." | Panel 1 brightens with the label **SYMMETRIC** and opens out to fill the frame; panel 2 dims and goes. |
| 1:42–1:45 | "It uses the same key to lock and unlock the information." | The gold key duplicates. Maya holds one, Sam the other, with an "=" between them. A box locks, then unlocks. |
| 1:45–1:48 | "This is very useful for protecting large amounts of data." | A stack of fifteen files appears; padlocks ripple onto every file in about a second. |
| 1:48–1:53 | "The challenge is that both people or devices need to receive the same secret key safely." | A key copy travels along a dashed line from Maya toward Sam. A gray hand rises from below the line, and a large "?" appears. |
| 1:53–1:54 | *(transition)* | The hand grabs at the key, but the key splits into two keys: one light blue, one gold. |

### 6. Asymmetric encryption (1:54–2:19)

| Time | Narration | On screen |
| --- | --- | --- |
| 1:54–1:58 | "Second is asymmetric encryption, also called public key encryption." | Panel 2 brightens with the label **ASYMMETRIC** and opens out to fill the frame; "(public-key)" fades in underneath. |
| 1:58–2:00 | "This uses a public key and a private key." | The blue key slides left with the label **PUBLIC KEY**; the gold key slides right with **PRIVATE KEY**. |
| 2:00–2:02 | "The public key can be shared with everyone." | Copies of the blue key fan out to five small figures across the screen. |
| 2:02–2:04 | "The private key must be kept secret." | The gold key moves to Sam; a glowing ring surrounds it. |
| 2:04–2:09 | "Someone can send you an encrypted message with your public key, but only your private key should be able to unlock it." | One of the crowd seals a green note with their public key; it scrambles to red and travels to Sam, and only his gold key opens it back to green. |
| 2:09–2:11 | "A useful example is a mailbox." | A mailbox builds itself around the blue key, which becomes its letter slot. |
| 2:11–2:18 | "Anyone can put letters inside, like using a public key, but only the person with the private key could open the mailbox and read the letters." | Three figures slide up one at a time and drop envelopes through the slot. Then Sam walks up, the gold key opens the mailbox door, and the envelopes fly out and unfold into green text. |
| 2:18–2:19 | *(transition)* | The mailbox and the crowd slide off to the left. |

### 7. Both together, HTTPS and daily life (2:19–2:47)

| Time | Narration | On screen |
| --- | --- | --- |
| 2:19–2:22 | "Many real systems use both types together." | A laptop on the left and a server on the right. A gold key icon and a blue-and-gold pair float above them and merge. |
| 2:22–2:28 | "For example, when visiting a secure website, public key encryption helps your device and the website agree on a secret key." | The server shows a blue public-key slot. The laptop makes a new gold key, arcs it over into the slot, and the server opens it with its private key. Both now hold matching gold keys. |
| 2:28–2:32 | "Then, fast symmetric encryption protects the rest of the conversation." | A rapid stream of small locked boxes flows back and forth between the laptop and the server. |
| 2:32–2:35 | "Encryption is used in many parts of daily life." | Faint everyday icons gather around the pair: chat, bank card, shopping cart, ID, email, files. |
| 2:35–2:42 | "When you see a padlock symbol in your web browser, HTTPS is helping encrypt the connection between your device and the website." | A browser bar with a padlock and "https://" appears on the laptop screen, and the camera zooms into it. The padlock is picked out, "https" glows, and a locked channel draws itself under the bar. |
| 2:42–2:46 | "This helps protect passwords, shopping information, and other personal details." | Three icons pop under the channel, one per item: password field, shopping cart, ID card. |
| 2:46–2:47 | *(transition)* | The padlock lifts off the browser bar and floats to the centre. |

### 8. Everyday uses (2:47–3:11)

| Time | Narration | On screen |
| --- | --- | --- |
| 2:47–2:52 | "Messaging apps can use end-to-end encryption so that a message is protected while traveling from one phone to another." | Two phones, left and right. A chat bubble locks into a small box, travels across, and opens only when it reaches the second phone; the label **end-to-end** writes on. |
| 2:52–2:59 | "Phones and computers can also encrypt stored files to make sure that information is harder to access if the device is lost or stolen." | A laptop with a folder; a padlock stamps onto the folder. A gray hand pulls the laptop away and opens the folder, but finds only red scrambled text. |
| 2:59–3:05 | "Encryption is used by banks, online stores, hospitals, businesses, and government agencies." | Five icons fill in, one per item: bank, shopping cart, hospital cross, office building, government building. A padlock stamps each. |
| 3:05–3:10 | "It's also used to protect the information sent through virtual private networks or VPNs." | A laptop and a server at either edge, a tunnel drawn between them and a **VPN** shield above it. Locked boxes flow through the tunnel. |
| 3:10–3:11 | *(transition)* | The tunnel fades; Maya and her phone return. An email icon with a red "!" arrives. |

### 9. Not magic (3:11–3:28)

| Time | Narration | On screen |
| --- | --- | --- |
| 3:11–3:14 | "Encryption is extremely important, but it is not magic." | A locked box sits in the centre, glowing and solid. |
| 3:14–3:21 | "It cannot protect someone who gives away their password, clicks on a dangerous link, or allows a malicious program onto the device." | The email opens with a password field and Maya hands her gold key to a gray hooded figure. A red link icon appears; a cursor clicks it and the screen flashes red. A small red bug crawls into the phone. |
| 3:21–3:27 | "Encryption protects the information, but people still need to use strong passwords and make safe decisions." | The hooded figure opens the box with the stolen key. The lid lifts cleanly: nothing is broken. Then three icons write on in a row: strong passwords, think before you click, keep devices updated. |
| 3:27–3:28 | *(transition)* | A rewind effect pulls everything back to the green note from Scene 2. |

### 10. Outro (3:28–3:42)

| Time | Narration | On screen |
| --- | --- | --- |
| 3:28–3:30 | "In short, encryption is like a digital lock." | A fast replay: the green note scrambles to red, drops into the box, and the padlock snaps shut. |
| 3:30–3:35 | "It helps keep private information private while it's being sent, stored, or shared." | One visual per verb: the box travels along a line (sent), rests inside a folder (stored), and copies to two friends (shared). |
| 3:35–3:42 | *(music only)* | Title "Encryption: a digital lock." End card with the group names, the class, and "Animated with manim.community". |

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
  scenes.py       # SceneA ... SceneC (Part 1), Scene01 ... Scene10
  audio/          # narration per scene (scene01.mp3 ...) + music
  renders/        # rendered scene videos
  edit/           # editor project that joins scenes, audio, captions
```

**3. Shared objects (`assets.py`).** Each is a small `VGroup` built from basic shapes, so every scene uses the identical drawing.

| Object | Built from | Used in scenes |
| --- | --- | --- |
| `Key(color)` | Circle (bow) + Rectangle (shaft) + small rectangles (teeth) | A, C, 3, 4, 5, 6, 7, 9, 10 |
| `Box()` | Rectangle body + Rectangle lid that rotates on a corner | 2, 3, 5, 9, 10 |
| `Padlock()` | Arc (shackle) + RoundedRectangle (body) | A, C, 3, 7, 8 |
| `Note(text, color)` | RoundedRectangle + `Text` | 1, 2, 3, 10 |
| `ScrambleText(msg)` | `Text` cycled through random characters, then settled | A, 2, 3, 4, 8, 10 |
| `Person(color)` | Circle head + RoundedRectangle body (Maya, Sam, crowd, codebreakers) | A, B, 1, 3, 5, 6, 9 |
| `Snooper()` / `HoodedFigure()` | Gray `Person` with a triangle hood | A, 1, 2, 3, 9 |
| `GrabHand()` | Gray rounded polygon rising from the bottom edge | 5, 8 |
| `NetworkMap()` | Grid of `Dot`s joined by light-blue `Line`s | A, 1 |
| `HistoryTimeline()` | `NumberLine` with labeled ticks (Ancient Rome, 1940s, 1970s, 2001, Today) and a sliding marker | A–C |
| `AlphabetShift(k)` | Two rows of 26 letter cells; the bottom row shifts k places with wraparound | B |
| `EnigmaRotors()` | Three `Circle` wheels with letter rings, plus a lamp board of 26 small circles | B |
| `AESCard()` | RoundedRectangle + `Text("AES")` + a round seal stamp | C |
| `Mailbox()` | RoundedRectangle + slot + door Rectangle + post | 6, 7 |
| `Envelope()` | Rectangle + two Lines for the flap | C, 6 |
| `Phone()`, `Laptop()`, `Server()` | RoundedRectangles with screen insets; server as stacked bars | A, B, C, 1, 7, 8, 9 |
| `BrowserBar()` | RoundedRectangle + small `Padlock` + `Text("https://")` | 7 |
| `Gear()` | Circle + small rectangles around the edge | 4 |
| `FileStack()`, `Folder()` | Offset rectangles; tabbed rectangle | 5, 8 |
| Icons (bank, scroll, chat, password field, card, cart, ID, hospital, office, government, VPN shield, link, bug, email) | Simple shapes, or free SVG icons loaded with `SVGMobject` | A, B, C, 7, 8, 9 |

`HistoryTimeline`, `AlphabetShift` and `EnigmaRotors` are also used in the professional video. Build them once in the shared `common/` folder so both videos use the same drawings.

**4. Animation recipes per scene**

| # | Core Manim moves |
| --- | --- |
| A | `Create` the key and `Write` the title; `Create` the `NetworkMap` lines with `lag_ratio`; the packet travels with `MoveAlongPath` and a padlock appears with `GrowFromCenter`; the snooper's copy opens to `ScrambleText`; `HistoryTimeline` draws with `Create`. |
| B | `AlphabetShift`: the bottom row slides with `animate.shift` and wraparound copies, and PHHW letters `TransformFromCopy` from the top row; the laptop runs a quick `Transform` loop through shifts until MEET appears; `EnigmaRotors`: the right rotor `Rotate`s by 2π/26 per key press while lamps light B, D, Z, G, O in turn (real Enigma output, verified in code); the notebook handoff uses `MoveAlongPath`. |
| C | The envelope `TransformFromCopy`s into four icons with `LaggedStart`; the data block gets a padlock, then gold keys `GrowFromCenter` on both computers; the AES card drops with `FadeIn(shift=DOWN)` and its seal with `GrowFromCenter`; the card `animate.scale(0.3)` and hops between devices with `MoveAlongPath`. |
| 1 | The note leaves the phone and travels with `MoveAlongPath` through the network dots while snoopers `Rotate` to face it; the note `animate.scale(2)` into the center. |
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

Build Scenes 2, 3 and 6 first (1:24–2:01 and 2:35–3:05, about 67 seconds). Together they test the core objects (note, box, keys, mailbox), the morph transitions, and how well beat timing matches real narration. If time allows, add Scene B (Caesar and Enigma, 0:19–0:48): its alphabet shift and rotor animation are the newest pieces in Part 1.

- [ ] Install Manim and render the starter Scene 2 code at low quality
- [ ] Build `Note`, `ScrambleText`, `Box`, `Padlock`, `Key`, `Person`, `Mailbox` and `Envelope` in `assets.py`
- [ ] Animate Scenes 2 → 3 as one continuous sequence (scramble, fold into box, lock, deliver past snoopers, unlock)
- [ ] Animate Scene 6 (key split, labels, fan-out to the crowd, mailbox build, envelopes, unlock)
- [ ] Optional: build `AlphabetShift` and `EnigmaRotors` in `common/` and animate Scene B
- [ ] Record or generate narration for those beats and re-time each beat window to the real audio
- [ ] Join the renders and audio in an editor (CapCut, DaVinci Resolve or Canva) and add captions
- [ ] Review as a group: does each visual land on its words, are labels readable, do transitions feel smooth?

**If it works,** build the remaining scenes in order, starting with Part 1 and reusing the same assets. **If timing feels rushed,** slow the narration slightly or drop a visual from the busiest beats (3:08–3:16 and 3:42–3:50) rather than cutting words. **If the video runs long,** see the runtime options at the top.
