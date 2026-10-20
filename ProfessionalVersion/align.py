"""Cut one long narration recording into the per-beat files the cut expects.

The booth recorded one line at a time, so every take was already named after
the beat it belonged to. A single continuous read is not: it is one file with
every line in it, and nothing saying where one line ends and the next begins.
This finds those boundaries and writes the same ``audio/sceneNN_beatMM.mp3``
files the rest of the pipeline already reads.

    python3 align.py transcribe p1simplifiednarration.mp4   # once, needs whisper
    python3 align.py check  p1simplifiednarration.mp4 --from SceneAWhyItMatters
    python3 align.py split  p1simplifiednarration.mp4 --from SceneAWhyItMatters

``transcribe`` is the only step that needs anything beyond the standard
library and ffmpeg. It writes the word timings to ``audio/raw/<name>.words.json``
and that file is committed, so nobody else has to install whisper to re-run
the split.

How a boundary is found:

1. Whisper gives every word it heard, with a start and an end.
2. The lines we are looking for come from the beat blocks in scenes.py (or
   from ``--lines``), so the target is a known sequence of words.
3. The two word sequences are aligned with ``difflib``, which tolerates the
   reader going off script — a dropped "the", "mathematics" for "math" — and
   still says which heard word each scripted word became.
4. That gives each line a rough start and end. The cut itself is then moved
   to the middle of the nearest real silence, so a clip never opens or closes
   on half a consonant.

A line the reader did not say, said in a different order, or ran together
with its neighbour cannot be cut cleanly, and ``check`` says so rather than
writing a bad clip.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import narrate

HERE = Path(__file__).resolve().parent
RAW = narrate.AUDIO / "raw"
REPORT = narrate.AUDIO / ".aligned.json"

# Default whisper model. small.en is enough: the words are already known, so
# the model only has to put a time on them.
MODEL = "small.en"

# A clip is cut this far outside the speech it holds, when there is silence
# there to take it from. narrate.py trims its own silence off the front and
# back when it lays the clip down, so a generous margin here costs nothing and
# protects the first and last consonant.
MARGIN = 0.12

# Below this, a line's words did not really turn up in the recording: it was
# skipped, reworded past recognition, or the reader was somewhere else.
MATCH_FLOOR = 0.60

# A gap this long between two lines holds more than a breath: a take the
# reader abandoned, or an aside. Long enough to be worth saying out loud,
# where a two-second gap at a chapter card is not.
DISCARDED = 4.0

# A gap shorter than this between two lines is not a pause, it is one
# continuous phrase. Cutting inside it leaves a seam that the pad in
# ``narrate.py retime`` then widens into an audible hole mid-sentence.
MIN_GAP = 0.18

# Wordings that mean the same thing to the alignment. Applied to both sides so
# a scripted "World War Two" still matches a heard "World War II".
SYNONYMS = {
    "ii": "two",
    "2001": "two thousand one",
    "1970s": "nineteen seventies",
    "1970's": "nineteen seventies",
    "plaintext": "plain text",
    "ciphertext": "cipher text",
    "https": "h t t p s",
    "vpns": "vpn",
    "cannot": "can not",
    "isn't": "is not",
    "it's": "it is",
    "doesn't": "does not",
    "don't": "do not",
    "can't": "can not",
    "won't": "will not",
    "who's": "who is",
    "that's": "that is",
    "codebreakers": "code breakers",
}


# --- the words that were said ----------------------------------------------


def words_path(media: Path) -> Path:
    return RAW / f"{media.stem}.words.json"


def find_whisper_python() -> str | None:
    """An interpreter that can ``import whisper``.

    Whisper is a heavy dependency and only the transcribe step needs it, so it
    is not in the render venv. Any python on the machine that has it will do.
    """
    candidates = [sys.executable, "python3"]
    candidates += [
        str(p) for p in sorted(
            Path("/Library/Frameworks/Python.framework/Versions").glob("*/bin/python3"),
            reverse=True,
        )
    ]
    candidates += [str(p) for p in (Path("/opt/homebrew/bin/python3"),)]
    seen = set()
    for cand in candidates:
        exe = shutil.which(cand) if not cand.startswith("/") else cand
        if not exe or exe in seen or not Path(exe).exists():
            continue
        seen.add(exe)
        probe = subprocess.run([exe, "-c", "import whisper"], capture_output=True)
        if probe.returncode == 0:
            return exe
    return None


TRANSCRIBE = """
import json, sys
import whisper
wav, out, model_name = sys.argv[1:4]
model = whisper.load_model(model_name, device="cpu")
result = model.transcribe(wav, language="en", word_timestamps=True, fp16=False,
                          condition_on_previous_text=False, temperature=0.0)
words = [
    {"word": w["word"].strip(), "start": round(w["start"], 3),
     "end": round(w["end"], 3), "prob": round(w.get("probability", 0.0), 3)}
    for seg in result["segments"] for w in seg.get("words", [])
]
json.dump({"model": model_name, "text": result["text"].strip(), "words": words,
           "segments": [{"start": round(s["start"], 3), "end": round(s["end"], 3),
                         "text": s["text"].strip()} for s in result["segments"]]},
          open(out, "w"), indent=1)
print(f"{len(words)} words")
"""


def cmd_transcribe(args: argparse.Namespace) -> int:
    media = Path(args.media)
    if not media.exists():
        print(f"{media}: not found", file=sys.stderr)
        return 1
    out = words_path(media)
    if out.exists() and not args.force:
        print(f"{out.relative_to(HERE)} is already there — --force to redo it")
        return 0

    exe = args.python or find_whisper_python()
    if not exe:
        print("no python here can `import whisper`. Install it with:\n"
              "  python3 -m pip install -U openai-whisper\n"
              "or point --python at an interpreter that has it.", file=sys.stderr)
        return 1

    wav = transcribe_audio(media)
    out.parent.mkdir(parents=True, exist_ok=True)
    print(f"transcribing {wav.name} with {args.model} ({exe})")
    subprocess.run([exe, "-c", TRANSCRIBE, str(wav), str(out), args.model],
                   check=True)
    print(f"{out.relative_to(HERE)}")
    return 0


def source_audio(media: Path) -> Path:
    """The audio the clips are cut from: audio/raw/<name>.m4a.

    The recording arrives as a screen capture, because the reader was watching
    the animation. The picture was only ever their cue, so it is dropped and
    the audio track demuxed out losslessly. That m4a is what is kept and what
    every clip is cut from; the original recording does not have to survive.
    """
    RAW.mkdir(parents=True, exist_ok=True)
    keep = RAW / f"{media.stem}.m4a"
    if media.resolve() == keep.resolve():
        return keep
    if not media.exists():
        if keep.exists():
            return keep
        raise SystemExit(f"{media}: not found, and no {keep.relative_to(HERE)} "
                         f"to fall back on")
    if not keep.exists() or keep.stat().st_mtime < media.stat().st_mtime:
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(media),
                        "-vn", "-map", "0:a:0", "-c:a", "copy", str(keep)], check=True)
    return keep


def transcribe_audio(media: Path) -> Path:
    """A 16k mono wav for the transcriber, made from the kept audio.

    Only whisper reads this, and whisper wants one channel at 16k, so it is
    not what any clip is cut from and it is not worth keeping around.
    """
    src = source_audio(media)
    wav = RAW / f"{media.stem}.wav"
    if not wav.exists() or wav.stat().st_mtime < src.stat().st_mtime:
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(src),
                        "-vn", "-ac", "1", "-ar", "16000",
                        "-c:a", "pcm_s16le", str(wav)], check=True)
    return wav


# --- normalising, so the two word lists can be compared --------------------


_PUNCT = re.compile(r"[^a-z0-9' ]+")


def tokens(text: str) -> list[str]:
    """A line, as the bare words the alignment compares."""
    text = text.lower().replace("—", " ").replace("-", " ").replace("’", "'")
    text = _PUNCT.sub(" ", text)
    out: list[str] = []
    for word in text.split():
        out.extend(SYNONYMS.get(word, word).split())
    return out


# --- the lines we are looking for ------------------------------------------


@dataclass
class Target:
    """One line to find in the recording, and where it goes when found."""

    stem: str            # sceneNN_beatMM — the file this becomes
    label: str           # scene and beat, for the report
    line: str
    tokens: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.tokens = tokens(self.line)


def targets_from_scenes(first: str | None, last: str | None) -> list[Target]:
    """The spoken beats of scenes.py, between two scene classes inclusive."""
    scenes = narrate.read_scenes()
    names = [s.name for s in scenes]
    start = names.index(first) if first else 0
    end = names.index(last) if last else len(names) - 1
    if start > end:
        raise SystemExit(f"--from {first} comes after --to {last}")
    out = []
    for scene in scenes[start:end + 1]:
        for beat in scene.beats:
            if beat.spoken:
                out.append(Target(beat.stem, f"{scene.name} beat {beat.index}",
                                  beat.note))
    if not out:
        raise SystemExit("no spoken beats in that range")
    return out


def targets_from_file(path: Path) -> list[Target]:
    """One line per non-empty line of a file, named ``line01`` upward.

    For a recording made before the scenes it belongs to exist: the timings
    come out of it, and the scenes get written against them.
    """
    lines = [ln.strip() for ln in path.read_text().splitlines() if ln.strip()]
    return [Target(f"line{i:02d}", f"{path.name}:{i}", ln)
            for i, ln in enumerate(lines, start=1)]


def split_sentences(path: Path) -> list[Target]:
    """Every sentence of a file, in order, named ``sent01`` upward."""
    text = " ".join(path.read_text().split())
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", text) if p.strip()]
    return [Target(f"sent{i:02d}", f"{path.name} sentence {i}", p)
            for i, p in enumerate(parts, start=1)]


# --- aligning --------------------------------------------------------------


@dataclass
class Found:
    target: Target
    start: float | None
    end: float | None
    matched: int
    heard: str
    cut_start: float | None = None
    cut_end: float | None = None
    gap_before: float | None = None
    notes: list[str] = field(default_factory=list)

    @property
    def ratio(self) -> float:
        return self.matched / len(self.target.tokens) if self.target.tokens else 0.0

    @property
    def speech(self) -> float | None:
        if self.start is None or self.end is None:
            return None
        return round(self.end - self.start, 3)

    @property
    def ok(self) -> bool:
        return self.start is not None and self.ratio >= MATCH_FLOOR


def align(targets: list[Target], words: list[dict]) -> list[Found]:
    """Put a start and an end on every target line.

    The scripted words and the heard words are one long sequence each.
    ``difflib`` pairs them up; a scripted word inside a matched run gets the
    time of the word it was heard as, and one inside a run the reader reworded
    is placed proportionally across whatever they said instead. So a line is
    still timed even when its middle came out differently, as long as enough
    of it turned up somewhere.
    """
    want: list[str] = []
    owner: list[int] = []        # which target each scripted word belongs to
    for i, target in enumerate(targets):
        want.extend(target.tokens)
        owner.extend([i] * len(target.tokens))

    heard = [tokens(w["word"]) for w in words]
    said: list[str] = []
    said_at: list[int] = []      # which heard word each token came from
    for i, group in enumerate(heard):
        for tok in group:
            said.append(tok)
            said_at.append(i)

    # exact: a scripted word that was certainly heard, and which word it was.
    # loose: a scripted word placed inside a reworded run, for timing only.
    exact: dict[int, int] = {}
    loose: dict[int, int] = {}
    matcher = difflib.SequenceMatcher(None, want, said, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                exact[i1 + k] = said_at[j1 + k]
        elif tag in ("replace", "delete"):
            span = j2 - j1
            for k in range(i1, i2):
                if span == 0:
                    # Said nothing here: lean on the last heard word, so the
                    # line still has somewhere to sit.
                    loose[k] = said_at[j1 - 1] if j1 > 0 else 0
                else:
                    off = int((k - i1) / max(1, i2 - i1) * (span - 1))
                    loose[k] = said_at[j1 + off]

    found: list[Found] = []
    for i, target in enumerate(targets):
        mine = [k for k, who in enumerate(owner) if who == i]
        hits = sorted(exact[k] for k in mine if k in exact)
        keep = _best_take(hits, len(target.tokens))
        loose_hits = [loose[k] for k in mine if k in loose]
        if keep:
            # Only the loose words that fall inside the take we kept: one
            # from a discarded take would stretch the clip back over it.
            span = range(keep[0], keep[-1] + 1)
            loose_hits = [j for j in loose_hits if j in span]
        any_hit = sorted(keep + loose_hits)
        matched = len(keep)
        if not any_hit:
            found.append(Found(target, None, None, 0, ""))
            continue
        lo, hi = any_hit[0], any_hit[-1]
        said_text = " ".join(words[j]["word"] for j in range(lo, hi + 1))
        item = Found(target, float(words[lo]["start"]),
                     float(words[hi]["end"]), matched, said_text)
        if len(hits) > len(keep):
            item.notes.append(
                f"said more than once — kept the take at "
                f"{float(words[lo]['start']):.2f}s and ignored "
                f"{len(hits) - len(keep)} word(s) from another"
            )
        found.append(item)

    _flag_order(found)
    return found


def _best_take(hits: list[int], line_len: int) -> list[int]:
    """Which of several attempts at the same line to cut.

    A reader who fluffs a line says it again, so its words turn up twice in
    the recording with the rest of the read in between. Spanning from the
    first to the last would cut a clip holding both takes and everything
    between them, so the hits are grouped into attempts and only one is kept.

    The fullest attempt wins — a retake usually exists because the first one
    dropped or garbled a word — and the later one breaks a tie, because that
    is the one the reader meant to stand.
    """
    if not hits:
        return []
    # A gap wider than the line itself means a different attempt, not a pause
    # inside this one.
    apart = max(line_len, 6)
    takes, run = [], [hits[0]]
    for a, b in zip(hits, hits[1:]):
        if b - a > apart:
            takes.append(run)
            run = [b]
        else:
            run.append(b)
    takes.append(run)
    return max(takes, key=lambda t: (len(t), t[0]))


def _flag_order(found: list[Found]) -> None:
    """Note any line the reader did not reach in the order we expect it."""
    last = -1.0
    for item in found:
        if item.start is None:
            item.notes.append("not found in the recording")
            continue
        if item.ratio < MATCH_FLOOR:
            item.notes.append(f"only {item.ratio:.0%} of its words were heard")
        if item.start < last - 0.25:
            item.notes.append("read out of order — it comes earlier than the "
                              "line before it")
        last = max(last, item.start)


# --- where the real silences are -------------------------------------------


def silences(audio: Path, noise: str = "-40dB", hold: float = 0.08
             ) -> list[tuple[float, float]]:
    """Every stretch of near-silence in the recording, as (start, end).

    Measured through the same cleanup the mixdown uses, so a lip smack in a
    pause does not read as speech here and then get trimmed away later.
    """
    proc = subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "info", "-i", str(audio), "-af",
         f"{narrate.CLEANUP},silencedetect=noise={noise}:d={hold}",
         "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    )
    out: list[tuple[float, float]] = []
    open_at: float | None = None
    for kind, value in re.findall(r"silence_(start|end): (-?[0-9.]+)", proc.stderr):
        if kind == "start":
            open_at = float(value)
        elif open_at is not None:
            out.append((open_at, float(value)))
            open_at = None
    if open_at is not None:
        out.append((open_at, narrate._ffprobe_duration(audio)))
    return out


def place_cuts(found: list[Found], quiet: list[tuple[float, float]],
               duration: float) -> None:
    """Turn each line's speech span into the clip to cut out of the file.

    The transcript says which line is which; the waveform says where to cut.
    Whisper puts a word within a few tenths of a second of where it was said,
    and at the edge of a sentence it is routinely further out than that — it
    hands a segment an end time and gives the next segment the same number,
    with the breath between them unaccounted for. Cutting on those numbers
    clips the last word of one line and leaves it on the front of the next.

    So every boundary between two lines is moved onto the breath that is
    really there. The pause is looked for around where the transcript put the
    join, and the longest one in reach wins: the reader's breath between two
    sentences is longer than the stop inside a word, and a comma they paused
    on is shorter than both. The first line opens, and the last closes, on the
    nearest edge of speech the same way.

    Nothing is segmented on pauses alone. A reader draws breath mid-sentence
    too, and a line keeps whatever pauses fall inside it.

    Where no real pause can be found at a boundary, the two lines were read as
    one continuous phrase. The cut then falls on the word boundary and both
    lines are flagged: beats like that want merging in scenes.py, rather than
    a sentence sliced in half and each piece padded back out.
    """
    # How far from the transcript's idea of a boundary a real pause may sit.
    tol = 1.0

    real = [(lo, hi) for lo, hi in quiet if hi - lo >= MIN_GAP]
    onsets = [hi for _, hi in real]
    offsets = [lo for lo, _ in real]

    def nearest(t: float, edges: list[float]) -> float | None:
        near = [e for e in edges if abs(e - t) <= tol]
        return min(near, key=lambda e: abs(e - t)) if near else None

    def pause_between(a: float, b: float) -> tuple[float, float] | None:
        """The breath at a boundary the transcript put between a and b."""
        lo, hi = min(a, b) - tol, max(a, b) + tol
        mid = (a + b) / 2
        here = [p for p in real if p[1] > lo and p[0] < hi]
        if not here:
            return None
        # Longest wins; a tie goes to the one nearest the join.
        return max(here, key=lambda p: (round(p[1] - p[0], 2),
                                        -min(abs(p[0] - mid), abs(p[1] - mid))))

    live = [f for f in found if f.start is not None]
    if not live:
        return

    # Keep what the transcript said, to fall back on and to report against.
    heard_at = [(f.start, f.end) for f in live]

    # The outer edges.
    first = nearest(live[0].start, onsets + [0.0])
    if first is not None:
        live[0].start = round(min(first, live[0].start), 3)
    last = nearest(live[-1].end, offsets + [duration])
    if last is not None:
        live[-1].end = round(max(last, live[-1].end), 3)

    # Every join between two lines.
    for n in range(len(live) - 1):
        here, after = live[n], live[n + 1]
        a, b = heard_at[n][1], heard_at[n + 1][0]
        if b - a > 2 * tol:
            # Something sits between these two that belongs to neither: a
            # discarded take, or a stretch the reader talked through. Close
            # the first line where it ended and open the second where it
            # began, rather than looking for one breath to share — the
            # longest pause across a gap that wide is somewhere in the
            # middle of whatever was abandoned.
            shut = nearest(a, offsets)
            here.end = round(shut if shut is not None else a, 3)
            open_ = nearest(b, onsets)
            after.start = round(open_ if open_ is not None else b, 3)
            if b - a > DISCARDED:
                after.notes.append(
                    f"{b - a:.1f}s between this line and the one before it, "
                    f"which goes into neither clip — most likely a take that "
                    f"was read again. Worth a listen if it is not."
                )
            continue
        pause = pause_between(a, b)
        if pause is not None:
            here.end = round(pause[0], 3)
            after.start = round(pause[1], 3)
        else:
            edge = round((a + b) / 2, 3)
            here.end = after.start = edge
            note = (f"read as one continuous phrase with "
                    f"{here.target.stem} / {after.target.stem} — no breath to "
                    f"cut at, so these beats want merging into one")
            here.notes.append(note)
            after.notes.append(note)

    for n, item in enumerate(live):
        if item.end <= item.start:
            item.end = round(item.start + 0.1, 3)
        before = live[n - 1].end if n else 0.0
        behind = live[n + 1].start if n + 1 < len(live) else duration
        # Reach into the quiet at each end, but never into a neighbour's clip.
        item.cut_start = round(max(before, item.start - MARGIN, 0.0), 3)
        item.cut_end = round(min(behind, item.end + MARGIN, duration), 3)
        item.gap_before = round(item.start - before, 3) if n else None


# --- reporting -------------------------------------------------------------


def run(args: argparse.Namespace) -> tuple[list[Found], Path, float]:
    media = Path(args.media)
    wp = words_path(media)
    if not wp.exists():
        raise SystemExit(f"no transcript at {wp.relative_to(HERE)} — run "
                         f"`align.py transcribe {media.name}` first")
    words = json.loads(wp.read_text())["words"]

    if args.lines:
        targets = targets_from_file(Path(args.lines))
    elif args.sentences:
        targets = split_sentences(Path(args.sentences))
    else:
        targets = targets_from_scenes(getattr(args, "first", None),
                                      getattr(args, "last", None))

    audio = source_audio(media)
    duration = narrate._ffprobe_duration(audio)
    found = align(targets, words)
    place_cuts(found, silences(audio), duration)
    return found, audio, duration


def report(found: list[Found], duration: float) -> None:
    print(f"{len(found)} lines against {duration:.2f}s of recording\n")
    print(f"{'line':<22} {'start':>7} {'end':>7} {'secs':>6} {'gap':>6} "
          f"{'match':>6}")
    print("-" * 70)
    for item in found:
        if item.start is None:
            print(f"{item.target.stem:<22} {'—':>7} {'—':>7} {'—':>6} {'—':>6} "
                  f"{'0%':>6}   {item.target.line[:40]}")
            continue
        gap = f"{item.gap_before:.2f}" if item.gap_before is not None else "—"
        print(f"{item.target.stem:<22} {item.start:7.2f} {item.end:7.2f} "
              f"{item.speech:6.2f} {gap:>6} {item.ratio:5.0%}   "
              f"{item.target.line[:40]}")

    bad = [f for f in found if f.notes]
    if bad:
        print(f"\n{len(bad)} lines need a look:\n")
        for item in bad:
            print(f"  {item.target.stem}  ({item.target.label})")
            print(f"    script: {item.target.line}")
            print(f"    heard:  {item.heard[:160] or '—'}")
            for note in item.notes:
                print(f"    ! {note}")
            print()

    good = [f for f in found if f.ok]
    spoken = sum(f.speech for f in good)
    print(f"{len(good)}/{len(found)} lines located, {spoken:.1f}s of speech")


def cmd_check(args: argparse.Namespace) -> int:
    found, _, duration = run(args)
    report(found, duration)
    return 0 if all(f.ok for f in found) else 1


def cmd_split(args: argparse.Namespace) -> int:
    found, audio, duration = run(args)
    report(found, duration)

    writable = [f for f in found if f.ok]
    if not writable:
        print("\nnothing to write", file=sys.stderr)
        return 1
    blocked = [f for f in found if not f.ok]
    if blocked and not args.force:
        print(f"\n{len(blocked)} lines could not be located and would be "
              f"skipped. Fix the wording in scenes.py, or pass --force to "
              f"write the rest anyway.", file=sys.stderr)
        return 1

    narrate.AUDIO.mkdir(exist_ok=True)
    scratch = set()
    if narrate.SCRATCH_LOG.exists():
        scratch = set(json.loads(narrate.SCRATCH_LOG.read_text()))

    print()
    for item in writable:
        out = narrate.AUDIO / f"{item.target.stem}.mp3"
        if args.dry_run:
            print(f"  would write {out.name}  "
                  f"{item.cut_start:.2f}–{item.cut_end:.2f}s")
            continue
        subprocess.run(
            ["ffmpeg", "-nostdin", "-v", "error", "-y",
             "-ss", f"{item.cut_start:.4f}", "-to", f"{item.cut_end:.4f}",
             "-i", str(audio), "-c:a", "libmp3lame", "-q:a", "2",
             "-ar", "48000", "-ac", "1", str(out)],
            check=True,
        )
        # It is a real take now, whatever it was before: take it off the list
        # of lines the scratch pass is allowed to speak over.
        scratch.discard(out.name)
        print(f"  {out.name}  {item.speech:5.2f}s  {item.target.line[:46]}")

    if args.dry_run:
        print(f"\n{len(writable)} clips would be written (dry run)")
        return 0

    # A merge or a split can leave a name on the list that is no longer any
    # beat's file. Nothing would speak over it — there is no beat to speak —
    # but it reads as an outstanding placeholder, so drop what is not there.
    scratch = {n for n in scratch if (narrate.AUDIO / n).exists()}
    narrate.SCRATCH_LOG.write_text(json.dumps(sorted(scratch), indent=2) + "\n")
    REPORT.write_text(json.dumps({
        "source": Path(args.media).name,
        "duration": round(duration, 3),
        "lines": [{
            "stem": f.target.stem, "label": f.target.label,
            "line": f.target.line, "heard": f.heard,
            "start": f.start, "end": f.end,
            "cut": [f.cut_start, f.cut_end],
            "match": round(f.ratio, 3), "notes": f.notes,
        } for f in found],
    }, indent=2) + "\n")

    print(f"\n{len(writable)} clips written to {narrate.AUDIO.name}/, "
          f"{len(blocked)} skipped")
    print(f"Next: ./render.sh -qh  &&  .venv/bin/python narrate.py retime")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("transcribe", help="word timings for a recording")
    p.add_argument("media")
    p.add_argument("--model", default=MODEL)
    p.add_argument("--python", default=None,
                   help="interpreter that has whisper (default: find one)")
    p.add_argument("--force", action="store_true", help="redo an existing one")
    p.set_defaults(func=cmd_transcribe)

    for name, func, help_text in (
        ("check", cmd_check, "where every line sits, and what does not fit"),
        ("split", cmd_split, "write one audio/<beat>.mp3 per line"),
    ):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("media")
        p.add_argument("--from", dest="first", default=None,
                       help="first scene class in the recording")
        p.add_argument("--to", dest="last", default=None,
                       help="last scene class in the recording")
        p.add_argument("--lines", default=None,
                       help="a file of lines to find, one per beat, instead "
                            "of the beats in scenes.py")
        p.add_argument("--sentences", default=None,
                       help="a file to split into sentences and find")
        if name == "split":
            p.add_argument("--force", action="store_true",
                           help="write the clips that did line up, and skip "
                                "the ones that did not")
            p.add_argument("--dry-run", action="store_true")
        p.set_defaults(func=func)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
