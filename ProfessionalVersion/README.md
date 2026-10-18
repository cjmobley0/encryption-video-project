# Professional encryption video (Manim)

The full cut: thirteen scenes, 91 beats, **8:00** of animation, built from
[`professional-encryption-video-plan.md`](professional-encryption-video-plan.md).
Same palette, same objects and same pipeline as the simplified cut, pitched at
a technical audience — real AES-256-GCM output, real SHA-256 digests, a drawn
elliptic curve, accurate key sizes and an accurate HTTPS handshake.

The machinery (beat timing, the recording booth, re-timing, the mixdown) is
the same in both cuts and is documented once, in
[`../SimplifiedVersion/README.md`](../SimplifiedVersion/README.md). This file
covers what is specific to this one.

## The intro is not here yet

The plan budgets **0:30–2:00** before Scene 1 for the history of encryption,
and that script is still being written. So:

- there is no `Scene00Intro` class, and nothing in the pipeline expects one
- `Scene01Bridge` opens with the history timeline (Caesar → Enigma → DES →
  AES) **already on screen**, then compresses it and slides it off — which is
  exactly the handover the plan describes
- every timecode in the plan starts at 0:00 for this portion

When the intro script lands: write `Scene00Intro` ending on
`HistoryTimeline()`, add it to the top of the `SCENES` list in
[`render.sh`](render.sh), and add its beat table to the plan. Nothing else
changes — the beat order of scenes 1–13 is unaffected, and every timecode
shifts by the intro's length.

## Layout

| Path | What it holds |
| --- | --- |
| `professional-encryption-video-plan.md` | The plan. The source of truth. |
| `scenes.py` | The thirteen scenes, one `self.beat(...)` per plan row. |
| `style.py` | The palette. The simplified cut's, plus `ALGO`. |
| `assets.py` | The shared objects — **byte-identical to the simplified cut's**. |
| `tech_assets.py` | What this cut adds: pipeline, curve, certificate, hash box… |
| `values.py` | The real AES and SHA-256 strings shown on screen. |
| `narrate.py` | The narration pipeline. |
| `render.sh` | Renders every scene in order and stitches the cut. |
| `audio/` | One file per line of narration, plus `music.mp3` if there is one. |
| `renders/` | `professional-encryption-video.mp4`. |

`audio/` is tracked, so a line recorded on one machine renders on another —
the simplified cut's README covers
[pushing takes](../SimplifiedVersion/README.md#pushing-your-takes). Every
line in here is still a `say` placeholder, listed in `audio/.scratch.json`;
the booth clears a line off that list as soon as a real take replaces it.

`renders/`, `media/` and `.venv/` are not in the repo, and neither is the
shared Manim checkout at [`../manim`](..) — `Setup` below rebuilds them.

`assets.py` is kept identical to the simplified cut's on purpose: a key drawn
in that video is the same key here. Anything this cut needs that the other one
does not goes in `tech_assets.py` instead, so the shared file never diverges.

## The cut

| # | Scene | Beats | Length |
| --- | --- | --- | --- |
| | *Intro — history and evolution (pending)* | — | *0:30–2:00* |
| 1 | `Scene01Bridge` | 3 | 0:14 |
| 2 | `Scene02Pipeline` | 5 | 0:34 |
| 3 | `Scene03Decryption` | 3 | 0:11 |
| 4 | `Scene04LockedBox` | 6 | 0:26 |
| 5 | `Scene05Math` | 4 | 0:16 |
| 6 | `Scene06Strength` | 9 | 0:41 |
| 7 | `Scene07Symmetric` | 9 | 0:49 |
| 8 | `Scene08Asymmetric` | 11 | 1:05 |
| 9 | `Scene09Hybrid` | 6 | 0:31 |
| 10 | `Scene10Hashing` | 8 | 0:38 |
| 11 | `Scene11Applications` | 12 | 1:04 |
| 12 | `Scene12Organizations` | 7 | 0:41 |
| 13 | `Scene13Conclusion` | 8 | 0:50 |
| | **Total** | **91** | **8:00** |

91 beats, of which 77 are spoken; the other 14 are the chapter cards and
scene transitions, which carry music rather than narration.

A corner tag (`ChapterTag`) sits top-left for the whole video so a viewer who
joins eight minutes in knows where they are. In the scenes whose camera moves,
it is pinned to the camera frame, so it stays the same size and in the same
place through every zoom.

## Nothing on screen is invented

Every value a technical viewer can read is computed, not typed out.
[`values.py`](values.py) produces them at import, so a caption and the string
under it cannot drift apart:

```bash
.venv/bin/python values.py     # print them all
```

| On screen | What it is |
| --- | --- |
| `43d9d0aa954d…` (scene 2) | AES-256-GCM of `Meet at 3pm`, demo key `00..1f`, zero nonce |
| `Q9nQqpVN9507…` (scene 2) | the same 27 bytes, Base64 |
| `96af04f2…` / `5bf79f4c…` (scene 10) | SHA-256 of `Meet at 3pm` and `Meet at 4pm` |
| `60 of 64 characters differ` (scene 10) | counted from those two digests, not asserted |
| RSA 3072 vs ECC 256 (scene 8) | bar lengths are the key sizes themselves |
| `2¹²⁸ ≈ 3.4 × 10³⁸` (scene 5) | the 128-bit keyspace |

The AES key is fixed so the value is reproducible by anyone reading the plan.
It is a demo key and nothing else: with AES-GCM, one repeated nonce under one
key is enough to break the encryption.

The one deliberately qualitative picture is the throughput race in scene 8 —
the plan asks for no numbers there, because a real ratio depends on hardware,
key size and mode, and a made-up one would be the single inaccurate frame in a
video built on real values.

## Rendering

```bash
./render.sh          # 480p15 preview — fast
./render.sh -qh      # 1080p60 final
./render.sh -qk      # 4K60
```

The result lands in `renders/`. With an empty `audio/` it renders the same cut
silently; narration is picked up if it is there.

One scene while iterating:

```bash
.venv/bin/manim -ql --disable_caching --media_dir media scenes.py Scene08Asymmetric
```

Add `-s` to render only the last frame as a PNG, which is much quicker when
adjusting layout. [`_frames.py`](_frames.py) pulls a contact sheet out of a
render for checking a whole scene at once:

```bash
.venv/bin/python _frames.py Scene08Asymmetric 10
```

## Narration

The lines live in `scenes.py`, one per `self.beat(...)`, copied word for word
from the group's script via the plan. `narrate.py` reads them straight out of
the source, so the recording list, the beat windows and the mix all come from
one place.

```bash
.venv/bin/python narrate.py list      # audio/NARRATION.md: the 77 lines
.venv/bin/python narrate.py status    # what is recorded, and how long it runs
../record.sh                          # the booth, on this cut by default
.venv/bin/python narrate.py retime    # beat windows + TARGET <- the real reads
```

`narrate.py` cross-checks itself against the plan: the plan's 91 beat-table
rows and the 91 `self.beat(...)` blocks have to line up one to one, and a beat
whose line no longer matches the plan is reported rather than guessed at. If
you change a line here, change it in the plan too.

The loop is **render → record → re-time → render again**, and it is described
in full in the simplified cut's README. Re-time against the quality you are
going to ship at; re-timing from a `-ql` preview and rendering at `-qh` leaves
dead air.

## Two accuracy notes from the plan

- **Scene 9** says the narration "can help the browser and the server
  authenticate each other". Most HTTPS connections authenticate only the
  server; client certificates are optional and uncommon. The script is used as
  written, and **the animation shows the server-only version**: the server
  sends a certificate, the browser checks its signature, and nothing goes the
  other way.
- **Scene 13** lists confidentiality, integrity and authentication. The
  classic CIA triad ends in *availability*; the script lists what encryption
  itself supports, which is accurate as written. Expect the question.

## Setup

Both cuts install from one Manim checkout, at the root of the repo rather than
in either version, and it is not tracked. Clone it first if the simplified cut
has not already:

```bash
git -C .. clone https://github.com/ManimCommunity/manim.git
git -C ../manim checkout v0.22.0
```

Then the environment, from here:

```bash
brew install pkgconf ffmpeg
python3 -m venv .venv
.venv/bin/python -m pip install -e ../manim
.venv/bin/python -m pip install cryptography
```

Installing from the one checkout is the point: both videos render against
exactly the same Manim (Community 0.22.0). `cryptography` is only needed by
`values.py` for the AES line; without it the baked literal is used, and it is
the same string.

No LaTeX: every label is `Text`, never `Tex`, as the plan requires. Exponents
are Unicode (2¹²⁸), hex and hashes are `font=MONO`, and `DecimalNumber` is
constructed with `mob_class=Text` so it does not reach for a TeX install.
