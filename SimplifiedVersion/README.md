# Encryption video (Manim)

The video laid out in [`encryption-video-plan.md`](encryption-video-plan.md):
thirteen scenes, 3:42, 100% [Manim Community](https://www.manim.community/)
— no AI-generated footage anywhere. Part 1 (Scenes A–C) is why it matters and
a short history; Part 2 (Scenes 1–10) is how encryption works.

The final cut lands at `renders/encryption-full.mp4`.

## Layout

| Path | What it holds |
| --- | --- |
| `encryption-video-plan.md` | The plan this build follows. The source of truth. |
| `style.py` | Palette, type, and the base scene with the beat timer. |
| `assets.py` | Every reusable object: keys, boxes, people, mailbox, icons. |
| `scenes.py` | `SceneAWhyItMatters` … `SceneCComputersAES`, then `Scene01Intro` … `Scene10Outro`. |
| `_frames.py` | Pulls a strip of sample frames out of a render, for checking. |
| `narrate.py` | The narration pipeline: list the lines, re-time the cut, mix the audio. |
| `align.py` | Cuts one long recording into the per-beat files, by what was said. |
| `render.sh` | Renders all thirteen scenes in order and stitches the cut. |
| `audio/` | One file per line of narration (`scene01_beat02.mp3` …), plus `music.mp3`. |
| `audio/raw/` | The continuous reads the clips were cut from, and their word timings. |
| `renders/` | The stitched video. |
| `media/` | Manim's own output. The 1080p60 renders and `timing/` are tracked for the booth; the rest is cache. |

`audio/` is tracked — the narration travels with the source, so whoever
records a line and whoever renders the cut need not be the same person; see
[Pushing your takes](#pushing-your-takes). Most of `media/` is not, but the
1080p60 scene renders and `media/timing/` are, so the booth has an animation to
play on a fresh clone. `renders/` is not: that is the finished cut. Nor is
`.venv/`, which `Setup` below builds per machine from the shared Manim
checkout at [`../manim`](..).

## The cut

| # | Scene | Slot | Length |
| --- | --- | --- | --- |
| A | `SceneAWhyItMatters` | 0:00–0:12 | 12s |
| B | `SceneBCaesarEnigma` | 0:12–0:32 | 20s |
| C | `SceneCComputersAES` | 0:32–0:56 | 24s |
| 1 | `Scene01Intro` | 0:56–1:01 | 5s |
| 2 | `Scene02Ciphertext` | 1:01–1:13 | 13s |
| 3 | `Scene03LockedBox` | 1:13–1:27 | 14s |
| 4 | `Scene04Math` | 1:27–1:38 | 10s |
| 5 | `Scene05Symmetric` | 1:38–1:54 | 16s |
| 6 | `Scene06Asymmetric` | 1:54–2:19 | 25s |
| 7 | `Scene07Https` | 2:19–2:47 | 27s |
| 8 | `Scene08Everyday` | 2:47–3:11 | 24s |
| 9 | `Scene09NotMagic` | 3:11–3:28 | 17s |
| 10 | `Scene10Outro` | 3:28–3:42 | 14s |

These are the real lengths: the cut has been re-timed to the recorded
narration, so each slot is the lines in it plus their breathing room.
`narrate.py status` reprints them, and a re-time after any re-record will move
them again.

## Rendering

```bash
./render.sh          # 480p15 preview — fast
./render.sh -qh      # 1080p60 final
./render.sh -qk      # 4K60
```

To work on one scene while iterating:

```bash
.venv/bin/manim -ql --disable_caching --media_dir media scenes.py Scene05Symmetric
```

Add `-p` to play it when it finishes, or `-s` to render only the final frame as
a PNG — much quicker when adjusting layout.

To check a render without watching it end to end:

```bash
.venv/bin/python _frames.py Scene05Symmetric 8
```

## Timing

Each scene class carries its slot length in `TARGET`, and each beat of the
plan's tables is one `with self.beat(seconds, "narration")` block. Whatever the
animations inside cost, the block holds the last frame until the window is
full, so the cut stays on the plan's clock. A beat that runs long logs a
warning naming the scene and the overrun, rather than quietly stealing time
from the next one — so a clean render means every beat still fits.

Never count run times by hand to measure a scene: `wait()` is implemented as
`play(Wait(...))`, so hooking both counts every hold twice. `VideoScene.elapsed`
reads Manim's own clock.

Every render also writes the windows it actually played to
`media/timing/<Scene>.json`, including what each beat's animations cost before
any hold. That log is what the narration is laid against, and what stops a
re-time from trimming a beat shorter than its own animation.

## Adding the narration

The narration is already in the code: every `self.beat(seconds, "...")` carries
the line spoken over that window. `narrate.py` reads those lines straight out of
`scenes.py` with `ast`, so the recording list, the timing and the mixdown cannot
drift from what the animation actually says.

### Read it straight through, and cut it up

This is how the narration in `audio/` was made, and the route to use for a
re-record. One continuous read of the whole part, in whatever app records
comfortably — the takes here came in as screen recordings, so they arrived as
`.mp4` with the picture attached. `align.py` throws the picture away, finds
each line inside the audio, and writes the same per-beat files the rest of the
pipeline already reads.

```bash
python3 align.py transcribe p1simplifiednarration.mp4   # once per recording
python3 align.py check      p1simplifiednarration.mp4 --from SceneAWhyItMatters
python3 align.py split      p1simplifiednarration.mp4 --from SceneAWhyItMatters
```

`--from` and `--to` say which scenes the recording covers, so one file can hold
one part and another the rest. `check` prints where every line landed and
writes nothing; `split` writes `audio/sceneNN_beatMM.mp3`. Both are safe to
re-run.

How a line is found:

1. **Transcribe once.** `transcribe` runs [whisper](https://github.com/openai/whisper)
   and saves the word timings to `audio/raw/<name>.words.json`. That file is
   tracked, so this is the only step that needs whisper installed — everyone
   else can re-cut from the saved timings with the standard library and
   `ffmpeg`. It will find any python on the machine that can `import whisper`;
   `--python` names one if it guesses wrong.
2. **Match the words.** The lines to look for come out of the beat blocks in
   `scenes.py`, so the target is known. The scripted words and the heard words
   are aligned with `difflib`, which tolerates the reader going off script — a
   dropped "the", "mathematics" for "math" — and still says which heard word
   each scripted word became.
3. **Cut on the breath, not the transcript.** Whisper places a word within a
   few tenths of a second, and at the edge of a sentence it is routinely
   further out: it gives a segment an end time and hands the next segment the
   same number, with the breath between them unaccounted for. So every
   boundary is moved onto the pause that is really there, found by
   `silencedetect` through the same cleanup the mixdown uses. Pauses inside a
   line are left alone — readers breathe mid-sentence too.

It also copes with a line read more than once. A reader who fluffs a sentence
says it again, so its words turn up twice with the rest of the read in
between; the hits are grouped into attempts and only one is cut — the fullest,
and the later one if two are equally full, because that is the take meant to
stand. The audio in between goes into no clip, and `check` says so.

`check` flags anything it could not cut cleanly, and those flags are worth
reading before `split`:

- **a line that was not found**, or only partly: the reader said something
  else. Either the wording in `scenes.py` is wrong or that line needs doing
  again.
- **two lines read as one continuous phrase**: there is no breath in the
  middle to cut at. Cutting anyway would put the pad from
  `narrate.py retime` into the middle of a sentence, so those beats want
  merging in `scenes.py` instead — one window, with both animations in it.
- **a line read out of order**: the read reached it somewhere else, and the
  scene order has to follow.
- **a long gap before a line**: several seconds that go into no clip. Usually
  a take the reader abandoned and did again, which is handled; worth a listen
  to confirm that is what it was.

`split` refuses to write while anything is flagged. `--force` writes the clips
that did line up and skips the rest; `--dry-run` shows the cuts without
writing. Everything it decided is left in `audio/.aligned.json`.

A line arriving this way is a real take, so `narrate.py scratch` will not speak
over it afterwards.

### Record one line at a time, in the booth

The booth is the other way in, and still works — it was not used for the
recordings in `audio/`.

```bash
../record.sh --project simplified      # or: .venv/bin/python narrate.py serve
```

opens the recording booth at `localhost:8765`. The booth itself lives at
[`../recorder/`](../recorder) and serves both versions of the video — see the
[root README](../README.md); this is the one that records against this cut. It takes one line at a time, with
the animation that line belongs to playing beside it: the countdown ends, and
the picture and the recorder start together, so you read to what the viewer
will see rather than to a stopwatch. Keeping a take writes
`audio/<line>.mp3` under the right name by itself — there is no file to name,
rename or drag anywhere.

Under the line is a band with the two numbers that actually constrain a read:

- **the left edge** is what that beat's animation costs. Reading faster buys
  nothing, because the window cannot shrink below the picture — the time comes
  back as a pause.
- **the right edge** is what the plan allowed for the line. Reading past it is
  not an error; it just makes the video that much longer.

Land between them and the cut stays on the plan's clock.

| Key | |
| --- | --- |
| <kbd>space</kbd> | start / stop recording |
| <kbd>enter</kbd> | keep the take and move to the next line |
| <kbd>r</kbd> | redo |
| <kbd>p</kbd> | hear the take, played against the animation |
| <kbd>w</kbd> | watch the animation on its own |
| <kbd>u</kbd> | go back to the take before this one |
| <kbd>↑</kbd> <kbd>↓</kbd> | previous / next line |

Pick your microphone in the top right and watch the level meter before the
first take — the list includes virtual devices, and choosing one of those is
the easy way to record a silent file. Echo cancellation, noise suppression and
auto gain are all turned off: they are built for calls, and they chew the ends
off words and move the level between takes.

Every take is kept in `audio/takes/<line>/`, so <kbd>u</kbd> can always go
back, and the device each line was recorded with is stored alongside — useful
when someone re-records one line a week later on a different microphone.

Lines that are still the `say` scratch take are marked; <kbd>p</kbd> plays one
so you can hear the intended pacing before your own take.

Two things to know. The booth shows you the animation, so it needs a render to
exist — run `./render.sh` first, and it will say so if a scene is missing. And
it is **localhost only**: browsers refuse microphone access over plain `http`
to anything else, so recording from a phone on the same wifi does not work
without setting up https. Chrome is the one to use; Safari's recorder is less
predictable.

### Record by hand instead

The booth is a convenience, not a dependency. `narrate.py list` writes
`audio/NARRATION.md`: one row per line, with the filename to record it as.
Record one file per sentence into `audio/` — `scene06_beat04.mp3` is the fourth
beat of `Scene06Asymmetric`. `.mp3`, `.wav`, `.m4a`, `.aiff`, `.flac` and `.aac`
all work. Leave a moment of silence at each end if it helps you read: silence at
the ends is measured out and trimmed, so only the speech is timed and placed.

One file per sentence rather than one per scene is what makes the rest
mechanical. A retake is one sentence, and every line's real length is known, so
each one lands on the animation it belongs to instead of being guessed at from a
scene total.

Beats marked *(no speech)* are music or a transition. There is nothing to record
for them; they keep the length the animation was built against.

### A stand-in take

To exercise the whole pipeline before anyone records:

```bash
.venv/bin/python narrate.py scratch
```

speaks every line with macOS `say` into those same filenames. A line that
already has a file is left alone; `--refresh` redoes the ones this tool made
earlier, and nothing short of `--force` writes over a real recording.

Swapping your own recording in is just saving over the file. Drop
`scene03_beat02.mp3` in and the next re-time and render use it, with the
scratch take still standing in for the lines you have not got to yet — so you
can hear the whole thing at every stage of recording.

### Pushing your takes

The narration is in the repo, so recording and rendering can be two different
people on two different machines: you record your lines, push them, and whoever
is rendering pulls them.

```bash
git pull                              # start from everyone else's takes
../record.sh --project simplified     # record
git add audio/ && git commit && git push
```

Commit `audio/.scratch.json` with the mp3s, every time. It is the list of lines
that are still a `say` placeholder, the booth takes a line off it the moment you
keep a real take, and `narrate.py scratch --refresh` speaks over anything still
on it — so a real recording that arrives without the updated list can be
overwritten later as though it were a placeholder.

Three things the repo deliberately does not carry:

- **`audio/takes/`** — the raw take behind every <kbd>u</kbd>. It is yours, it
  grows with every retake, and a render only ever reads `audio/<line>.mp3`.
- **`audio/.takes.json`** — the index into it, including which microphone each
  line was read on.
- **`audio/.measured.json`** — a cache keyed on each file's mtime, which Git
  does not preserve. It rebuilds itself on the first retime or mix.

An `.mp3` is a binary: Git cannot merge two of them, so two people recording
the same line is a conflict somebody has to resolve by choosing a take. Pull
before you start, and split the work by scene rather than by line.

### Re-time, then render

```bash
./render.sh                            # once, to log what the animations cost
.venv/bin/python narrate.py retime     # beat windows and TARGET <- real lengths
./render.sh -qh                        # the cut, with audio
```

`retime` changes nothing in `scenes.py` but numbers. Each spoken beat's window
becomes its line's measured length plus `--pad` (0.35s by default, for breathing
room), and each scene's `TARGET` becomes the sum of its beats. Lines you have not
recorded yet keep their current window, so you can record a scene at a time and
re-time as you go.

Re-time against the quality you are going to ship at. A beat's animation cost
is measured in whole frames, so it comes out a little longer at 15fps than at
60fps — re-timing from a `-ql` preview and then rendering at `-qh` left about
three seconds of dead air across this cut. `./render.sh -qh` then
`narrate.py retime` then `./render.sh -qh` again settles it; the second
`retime` reports no change once it has.

A window never shrinks below what its animation costs. A line can be read faster
than the picture it belongs to can be drawn, and trimming the window to the line
would leave the scene running past its own slot — so the animation holds the
window open, and `retime` names every window that happened to. Those costs come
from `media/timing/`, which is why `retime` wants a render behind it; `--no-floor`
turns it off. Once it has settled, a second `retime` after a render reports no
change.

```bash
.venv/bin/python narrate.py status     # what is recorded, and how long it runs
```

The plan's timecodes come from the same numbers, so bring them with it:

```bash
.venv/bin/python narrate.py replan
```

That rewrites every beat row, scene heading and chapter banner in the plan
from the lengths in `scenes.py`, and touches nothing else — not the wording,
not the *On screen* column. Running it twice changes nothing the second time.
Without it the plan quietly disagrees with the cut, and the plan is what the
next person reads.

### The mix

`render.sh` picks audio up if it is there and ignores it if it is not: with an
empty `audio/` it renders exactly the silent cut it always has. With narration
present, each scene's video is muxed with its own lines before the concat, and
`audio/music.mp3` — if you add one — is looped and mixed under the whole cut,
fading in and out at the ends.

The bed is measured and scaled to `MUSIC_DB`, a mean level in dB, rather than
multiplied by a fixed gain: the narration is levelled to about -22 dB, and the
default of -34 puts the music well under it whether the track you drop in was
exported quiet or loud. `MUSIC_DB=-30 ./render.sh -qh` lifts it; the render
prints what it measured and how far it trimmed.

Every take is tidied first, by `CLEANUP` in `narrate.py`: a highpass at 80Hz
for rumble and plosives, `adeclick` for the short ticks a mouth makes, and a
downward expander below -40dB — well under speech, well over the room — so the
breath and lip noise between words comes down while the words do not. On these
recordings it took the gaps from about 18dB above the room tone to below it,
and moved speech by under a decibel.

This matters more than it sounds, because the levelling below lifts whatever
is there: mouth noise that was inaudible in the raw take is not inaudible once
the voice has been brought up to level. Measurement runs through the same
chain, so a lip smack in the run-up cannot read as the start of the line and
push it late.

The narration itself is levelled too. A laptop mic typically records 15dB
quieter than a video wants to be, which leaves the voice faint and lets the
music sit on top of it. `narrate.py mix` works out one gain for the whole
narration — one figure, not one per line, so the differences a reader puts in
on purpose survive — and holds it back if it would drive the loudest peak
above -1.5 dB. `narrate.py mix --gain 0` turns it off.

Each line is placed against the beat starts the render itself logged, not against
the numbers in `scenes.py`. If a beat overran its window, the render is the truth
and the audio follows the picture rather than the page.

### Why not `manim-voiceover`

The plan names [`manim-voiceover`](https://voiceover.manim.community/) as an
option, and it is the obvious thing to reach for. It does not fit this project:

- **It has no way to use pre-recorded files.** Its speech services are five
  cloud TTS APIs, one local TTS, a `RecorderService` that records you
  interactively in the middle of a render through `pyaudio`, and a stitcher that
  splits one long take on silence. Pointing it at `audio/scene06_beat04.mp3`
  means writing a custom `SpeechService` — more code than the muxing it saves.
- **The audio would end up inside each scene's `.mp4`.** `voiceover()` goes
  through `Scene.add_sound()`, so the scene files stop being silent, and "an
  empty `audio/` renders the silent cut" would need a second set of scene
  classes.
- **Every scene would be restructured.** Scenes would subclass
  `VoiceoverScene` and call `set_speech_service()`, and `beat(seconds, line)` —
  a window the animation is held to — would become `voiceover(text)`, a window
  the audio decides. The brief was to leave the animation alone.
- **It adds seven runtime dependencies**, `sox` and `pip` itself among them, to
  a project that needs nothing but Manim and ffmpeg.

So the muxing is hand-rolled in `narrate.py` on top of ffmpeg, which `render.sh`
already uses to stitch the cut. Nothing new to install.

## The end card

`Scene10Outro` ends on an end card built from `CREDITS_LOGO`, `CREDITS_TEAM`,
`CREDITS_CLASS` and `CREDITS_TOOLS` at the top of `scenes.py`, laid out by the
`team_logo` and `team_roster` helpers beside them. `CREDITS_TEAM` is a name and
a role per member, and the roster draws them as two columns. The professional
cut carries the same four, so change them in both.

`CREDITS_LOGO` is the shared `team_logo.svg` at the root of the repo; see the
root README on where it comes from.

## Setup

From a fresh clone there is no `.venv`, and no Manim checkout to install from.
Both cuts share one, at the root of the repo rather than in either version:

```bash
git -C .. clone https://github.com/ManimCommunity/manim.git
git -C ../manim checkout v0.22.0
python3 -m venv .venv
.venv/bin/python -m pip install -e ../manim
```

System dependencies, via Homebrew:

```bash
brew install pkgconf ffmpeg
```

- `pkgconf` — needed to build `pycairo`
- `ffmpeg` — stitches the scenes; Manim itself renders through PyAV

No LaTeX needed: every label is `Text`, never `Tex` or `MathTex`, as the plan
requires.

## Conventions

Colours come from the plan and carry the same meaning in every scene. Do not
add a colour without updating the plan first.

| Meaning | Colour | Hex | Name in `style.py` |
| --- | --- | --- | --- |
| Plaintext (readable) | green | `#3DDC97` | `PLAIN` |
| Ciphertext (scrambled) | red-orange | `#FF6B4A` | `CIPHER` |
| Private / shared secret key, and every lock | gold | `#FFC93C` | `PRIVATE` |
| Public key | light blue | `#5BC0EB` | `PUBLIC` |
| Attacker / snooper | grey | `#8D99AE` | `SNOOP` |
| Labels and text | off-white | `#F1FAEE` | `FG` |
| Background | navy | `#14213D` | `BG` |

The names avoid Manim's own `GOLD`, `BLUE` and `GRAY` on purpose, so that
`from manim import *` and `from style import *` cannot shadow each other.

Scenes subclass `VideoScene`, or `MovingVideoScene` where the camera moves
(scenes 3 and 7). Text is `Avenir Next` for labels and `Menlo` for anything
standing in for a message, so plaintext and ciphertext keep the same width
through a scramble.
