# Encryption videos

An explainer on how encryption works, animated end to end in
[Manim Community](https://www.manim.community/)
Two cuts, from the same plan, palette and script:

| | | |
| --- | --- | --- |
| [`ProfessionalVersion/`](ProfessionalVersion) | **animated** — silent cut in `ProfessionalVersion/renders/`, narration still to record; the history intro is still to be written | the full cut: 13 scenes, 77 narrated beats, 8:00 |
| [`SimplifiedVersion/`](SimplifiedVersion) | **done** — the cut is in `SimplifiedVersion/renders/` | the proof of concept: 10 scenes, 46 narrated beats, ~3:28 |

Each version is self-contained. What they share sits at the root:

```
EncryptionVideos/
├── record.sh              the narration booth, for either version
├── recorder/              the booth itself — see recorder/server.py
├── manim/                 the Manim checkout both venvs install from
├── ProfessionalVersion/   scenes.py, narrate.py, render.sh, audio/, renders/
└── SimplifiedVersion/     the same shape, finished
```

Inside a version:

| Path | What it holds |
| --- | --- |
| `*encryption-video-plan.md` | The plan that cut follows. The source of truth. |
| `scenes.py` | Every scene, with the narration line on each beat. |
| `style.py`, `assets.py` | The palette and the reusable objects. `assets.py` is byte-identical in both versions. |
| `tech_assets.py` | Objects only the full cut needs. Professional only. |
| `narrate.py` | The narration pipeline: list the lines, re-time the cut, mix. |
| `render.sh` | Renders every scene in order and stitches them. |
| `audio/` | One file per line of narration, plus `music.mp3` if there is one. |
| `renders/` | The stitched video. |
| `media/` | Manim's own output. The 1080p60 scene renders and beat-timing logs are tracked, so the booth has a picture to play; the rest is cache. |
| `.venv/` | That version's virtualenv. |

Deeper detail lives in each version's own README:
[`SimplifiedVersion/README.md`](SimplifiedVersion/README.md) for the timing
model, the mixdown and the conventions;
[`ProfessionalVersion/README.md`](ProfessionalVersion/README.md) for the
pending history intro and the real AES and SHA-256 values on screen.

## How it fits together

The narration lives *in* the animation: every beat is a
`self.beat(seconds, "the line spoken here")` block in `scenes.py`, and
`narrate.py` reads the lines from there. Recording list, file names, beat
windows and final mix all come from that one place.

So the loop is **render → record → re-time → render again**:

1. **Render** — gives the booth a picture, and logs what each animation costs.
2. **Record** each line to that picture.
3. **Re-time** — each beat's window stretches to the line actually read.
4. **Render again** — the cut, with the audio under it.

## Setup

Only needed to render. The booth needs none of it: standard-library Python
plus `ffmpeg`, on the system `python3`.

One Manim checkout at the root, which both versions install from:

```bash
git clone https://github.com/ManimCommunity/manim.git
git -C manim checkout v0.22.0
```

Then once per version:

```bash
brew install pkgconf ffmpeg    # pkgconf builds pycairo; ffmpeg stitches and converts
cd SimplifiedVersion           # or ProfessionalVersion
python3 -m venv .venv
.venv/bin/python -m pip install -e ../manim
```

No LaTeX: every label is `Text`, never `Tex`.

## Recording the narration

The booth takes one line at a time, with the animation that line belongs to
playing beside it.

### Getting set up

```bash
brew install ffmpeg
git clone https://github.com/cjmobley0/encryption-video-project.git
cd encryption-video-project
```

### Reading the lines

```bash
git pull                              # start from everyone else's takes
./record.sh                           # Professional, the default
```

That opens the booth at <http://localhost:8765>. The countdown ends, and the
picture and the recorder start together, so you read to what the viewer will
see rather than to a stopwatch. Keeping a take writes
`<Version>/audio/<line>.mp3` under the right name by itself — nothing to name,
rename or drag anywhere.

![The narration booth, on the professional cut](RecorderUI.png)

**Pick your microphone in the top right before the first take**, and watch the
level meter.

Every take is kept under `<Version>/audio/takes/`, so <kbd>u</kbd> can always
go back, and the microphone each line was recorded with is stored alongside it.

### Pushing your takes

```bash
git add ProfessionalVersion/audio
git commit -m "Record scenes 3 and 4"
git push
```

Add the whole `audio/` folder rather than the mp3 files alone, so that
`audio/.scratch.json` goes with them. It is the list of lines that are still a
machine `say` placeholder; the booth takes a line off it the moment you keep a
real take, and a recording that arrives without the updated list can be spoken
over later as though it were still a placeholder.

An `.mp3` is a binary and Git cannot merge two of them, so pull before you
start, and split the work by scene rather than by line.

## Rendering either video

Each version renders itself, from its own directory:

```bash
cd ProfessionalVersion     # or SimplifiedVersion
./render.sh                # 480p15 preview — fast
./render.sh -qh            # 1080p60 final
./render.sh -qk            # 4K60
```

What a run does:

- every scene in order, each line laid under its own beat
- stitched into `renders/`
- `audio/music.mp3` mixed under the whole cut, if there is one
- an empty `audio/` gives the same cut, silent

One scene at a time, while iterating:

```bash
.venv/bin/manim -ql --disable_caching --media_dir media scenes.py Scene05Symmetric
```

`-p` plays it when it finishes; `-s` renders the final frame only, as a PNG —
much quicker when adjusting layout.

### Re-timing to the real narration

Scene lengths start out from the plan. Once lines are recorded, take them from
the reads instead:

```bash
./render.sh -qh                        # log what the animations cost
.venv/bin/python narrate.py retime     # beat windows and TARGET <- real lengths
./render.sh -qh                        # the cut, with audio
```

Re-time at the quality you are shipping at: animation costs are measured in
whole frames, so re-timing from a `-ql` preview leaves dead air at `-qh`. A
second `retime` reports no change once it has settled.

```bash
.venv/bin/python narrate.py status     # what is recorded, and how long it runs
```

### Keeping the booth's picture current

The booth plays the 1080p60 render of each scene, and `media/timing/` says
where each line sits inside it. Both are tracked, so a fresh clone has the
picture. `./render.sh -qh` writes both — commit them with whatever changed in
the scene:

```bash
./render.sh -qh
git add media && git commit && git push
```

Both have to come from that same `-qh` render: the timing logs carry the frame
rate they were measured at, and at 15fps a beat lands up to half a second away
from where it lands at 60fps.
