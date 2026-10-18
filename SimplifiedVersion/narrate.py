"""Narration: list the lines, fake a take, re-time the cut, mix the audio in.

The narration already lives in scenes.py — every ``self.beat(seconds, "...")``
carries the line spoken over that window. This tool reads those lines straight
out of the source with ``ast``, so the recording list, the timing and the
mixdown can never drift from what the animation actually says.

    .venv/bin/python narrate.py list      # audio/NARRATION.md: what to record
    .venv/bin/python narrate.py status    # which lines are in audio/, how long
    .venv/bin/python narrate.py scratch   # a stand-in take, via macOS `say`
    .venv/bin/python narrate.py retime    # beat windows + TARGET <- real lengths
    .venv/bin/python narrate.py mix ...   # lay a scene's audio under its video

``mix`` is called by render.sh; the other three are run by hand. See the
README's "Adding the narration" section for the whole loop.
"""

from __future__ import annotations

import argparse
import ast
import json
import math
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCENES = HERE / "scenes.py"
PLAN = HERE / "encryption-video-plan.md"
AUDIO = HERE / "audio"
MEASURED = AUDIO / ".measured.json"
SCRATCH_LOG = AUDIO / ".scratch.json"

# A beat whose line is one of these is not spoken: it keeps the window the
# animation was built against, and no audio is laid under it.
SILENT_NOTES = ("(music only)", "(transition)")

# Recordings may arrive in any of these; the first one found wins.
EXTENSIONS = (".mp3", ".wav", ".m4a", ".aiff", ".aif", ".flac", ".aac")

# Breathing room after each line, so one sentence does not run into the next.
DEFAULT_PAD = 0.35

# Bumped whenever _speech_span or CLEANUP changes, to throw away stale
# measurements.
MEASURE_VERSION = 4

# Tidying applied to every take, before it is levelled or laid under a scene.
#
#   highpass  drops rumble and the thump of a plosive, below anything a voice
#             needs
#   adeclick  removes the short impulsive ticks a mouth makes
#   agate     expands downwards below -40dB, which is well under speech and
#             well over the room, so the mouth noise between words comes down
#             while the words themselves are untouched
#
# Measurement runs through it too: a lip smack in the run-up reads as speech to
# the silence trim otherwise, and the line gets laid down late.
CLEANUP = (
    "highpass=f=80,"
    "adeclick,"
    "agate=threshold=-40dB:ratio=3:range=0.03:attack=4:release=180:"
    "knee=6:detection=rms"
)

SAY = Path("/usr/bin/say")
SCRATCH_VOICE = "Samantha"
SCRATCH_RATE = 165


# --- reading the beats out of scenes.py ------------------------------------


@dataclass
class Beat:
    scene: str
    index: int           # 1-based, counting every beat in the scene
    note: str            # the narration line, or a SILENT_NOTES marker
    window: float        # the beat's current first argument
    span: tuple[int, int, int, int]  # where that number sits in scenes.py

    @property
    def spoken(self) -> bool:
        return self.note not in SILENT_NOTES

    @property
    def stem(self) -> str:
        return f"{scene_slug(self.scene)}_beat{self.index:02d}"

    def audio(self) -> Path | None:
        """The recording for this line, whatever format it arrived in."""
        if not self.spoken:
            return None
        for ext in EXTENSIONS:
            path = AUDIO / (self.stem + ext)
            if path.exists():
                return path
        return None


@dataclass
class SceneBeats:
    name: str
    target: float
    target_span: tuple[int, int, int, int] | None
    beats: list[Beat]


def scene_slug(name: str) -> str:
    """Scene01Intro -> scene01, so a filename says nothing but its slot."""
    m = re.match(r"Scene(\d+)", name)
    return f"scene{m.group(1)}" if m else name.lower()


def _span(node: ast.AST) -> tuple[int, int, int, int]:
    return (node.lineno, node.col_offset, node.end_lineno, node.end_col_offset)


def _beat_calls(fn: ast.FunctionDef) -> list[ast.Call]:
    """Every ``self.beat(...)`` inside ``fn``, in source order."""
    found: list[ast.Call] = []

    def walk(node: ast.AST) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.With):
                for item in child.items:
                    call = item.context_expr
                    if (
                        isinstance(call, ast.Call)
                        and isinstance(call.func, ast.Attribute)
                        and call.func.attr == "beat"
                        and isinstance(call.func.value, ast.Name)
                        and call.func.value.id == "self"
                    ):
                        found.append(call)
            walk(child)

    walk(fn)
    return sorted(found, key=lambda c: (c.lineno, c.col_offset))


def read_scenes(path: Path = SCENES) -> list[SceneBeats]:
    """Parse the beat tables out of scenes.py."""
    tree = ast.parse(path.read_text(), filename=str(path))
    out: list[SceneBeats] = []

    for cls in tree.body:
        if not isinstance(cls, ast.ClassDef):
            continue
        bases = {b.id for b in cls.bases if isinstance(b, ast.Name)}
        if not bases & {"VideoScene", "MovingVideoScene"}:
            continue

        target, target_span = 0.0, None
        construct = None
        for stmt in cls.body:
            if isinstance(stmt, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "TARGET" for t in stmt.targets
            ):
                if isinstance(stmt.value, ast.Constant):
                    target = float(stmt.value.value)
                    target_span = _span(stmt.value)
            elif isinstance(stmt, ast.FunctionDef) and stmt.name == "construct":
                construct = stmt
        if construct is None:
            continue

        beats = []
        for i, call in enumerate(_beat_calls(construct), start=1):
            if len(call.args) < 2:
                raise SystemExit(
                    f"{path.name}:{call.lineno}: self.beat() needs its seconds "
                    f"and its line as positional arguments"
                )
            secs, note = call.args[0], call.args[1]
            if not isinstance(secs, ast.Constant) or not isinstance(
                secs.value, (int, float)
            ):
                raise SystemExit(
                    f"{path.name}:{call.lineno}: beat window is not a plain "
                    f"number, so it cannot be re-timed"
                )
            if not isinstance(note, ast.Constant) or not isinstance(note.value, str):
                raise SystemExit(
                    f"{path.name}:{call.lineno}: beat line is not a plain string"
                )
            beats.append(
                Beat(
                    scene=cls.name,
                    index=i,
                    note=" ".join(note.value.split()),
                    window=float(secs.value),
                    span=_span(secs),
                )
            )
        out.append(SceneBeats(cls.name, target, target_span, beats))

    if not out:
        raise SystemExit(f"no scene classes found in {path}")
    return out


# --- what the plan allowed each line ---------------------------------------


PLAN_ROW = re.compile(
    r"\|\s*(\d+):(\d\d)\s*[\u2013-]\s*(\d+):(\d\d)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$"
)


def plan_budgets(path: Path = PLAN) -> list[tuple[float, str]]:
    """Every beat's slot in the plan's tables, in order: (seconds, line).

    A re-time overwrites the windows in scenes.py, so the plan is the only
    place the *intended* length of a line survives. The recorder shows it as
    the target to read against.
    """
    out: list[tuple[float, str]] = []
    for line in path.read_text().splitlines():
        m = PLAN_ROW.match(line)
        if not m:
            continue
        start = int(m.group(1)) * 60 + int(m.group(2))
        end = int(m.group(3)) * 60 + int(m.group(4))
        note = (m.group(5)
                .replace("*(music only)*", "(music only)")
                .replace("*(transition)*", "(transition)")
                .strip().strip('"').strip())
        out.append((float(end - start), " ".join(note.split())))
    return out


def budgets_by_beat(
    scenes: list[SceneBeats], path: Path = PLAN
) -> dict[tuple[str, int], float]:
    """The plan's budget for each beat, matched to the code by position.

    The plan's tables and the beat blocks are the same list in the same order,
    so they line up one to one. A row whose line no longer matches the code is
    left out rather than guessed at: a budget on the wrong beat would be worse
    than none.
    """
    rows = plan_budgets(path)
    beats = [b for scene in scenes for b in scene.beats]
    if len(rows) != len(beats):
        logger_warn(f"{path.name} has {len(rows)} beat rows but scenes.py has "
                    f"{len(beats)} beats — budgets left out")
        return {}
    out = {}
    for (budget, note), beat in zip(rows, beats):
        if note == beat.note:
            out[(beat.scene, beat.index)] = budget
    return out


def logger_warn(message: str) -> None:
    print(f"warning: {message}", file=sys.stderr)


# --- measuring a recording -------------------------------------------------


def _ffprobe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(out)


def _stream_duration(path: Path, kind: str) -> float | None:
    """How long one stream of a file runs, or None if it has no such stream."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", f"{kind}:0",
         "-show_entries", "stream=duration", "-of", "default=nw=1:nk=1",
         str(path)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return None


def _speech_span(
    path: Path, duration: float
) -> tuple[float, float, dict[str, float]]:
    """Where the speech starts and stops, and how loud it is.

    Ignores silence at either end:

    A recording carries dead air around the line — the mic was already live
    when the reader drew breath. Timing against the whole file would push
    every sentence late, so measure (and later place) the speech itself.
    """
    proc = subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "info", "-i", str(path),
         "-af", f"{CLEANUP},silencedetect=noise=-40dB:d=0.10,volumedetect",
         "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    )
    levels = {}
    for name in ("mean", "max"):
        m = re.search(rf"{name}_volume: (-?[0-9.]+) dB", proc.stderr)
        if m:
            levels[name] = float(m.group(1))
    # Pair the events into silence blocks. A block that runs to the end of the
    # file may be closed with a silence_end at the duration, or not closed at
    # all — both mean the same thing, and reading only one of the two forms
    # leaves the tail of every real recording counted as speech.
    blocks: list[list[float | None]] = []
    for kind, value in re.findall(
        r"silence_(start|end): (-?[0-9.]+)", proc.stderr
    ):
        if kind == "start":
            blocks.append([float(value), None])
        elif blocks and blocks[-1][1] is None:
            blocks[-1][1] = float(value)

    start, end = 0.0, duration
    # Silence at the very top of the file is the reader's run-up.
    if blocks and blocks[0][0] <= 0.05 and blocks[0][1] is not None:
        start = blocks[0][1]
    # Silence running to the end is the gap before they stopped recording.
    if blocks:
        last_start, last_end = blocks[-1]
        at_eof = last_end is None or last_end >= duration - 0.05
        if at_eof and last_start > start:
            end = last_start

    if end - start < 0.08:  # all silence, or a threshold we got wrong
        start, end = 0.0, duration
    else:
        # Leave a little of the silence in, so no consonant gets clipped.
        start, end = max(0.0, start - 0.06), min(duration, end + 0.08)
    return start, end, levels


def measure(path: Path, cache: dict[str, dict] | None = None) -> dict:
    """Duration and speech span of a recording, cached against its mtime."""
    stat = path.stat()
    key = path.name
    # The version is part of the stamp so that a change to how a file is
    # measured invalidates what was cached under the old rules.
    stamp = [MEASURE_VERSION, round(stat.st_mtime, 3), stat.st_size]
    if cache is not None:
        hit = cache.get(key)
        if hit and hit.get("stamp") == stamp:
            return hit

    duration = _ffprobe_duration(path)
    start, end, levels = _speech_span(path, duration)
    entry = {
        "stamp": stamp,
        "duration": round(duration, 4),
        "start": round(start, 4),
        "end": round(end, 4),
        "speech": round(end - start, 4),
        "mean": levels.get("mean"),
        "peak": levels.get("max"),
    }
    if cache is not None:
        cache[key] = entry
    return entry


def load_cache() -> dict[str, dict]:
    if MEASURED.exists():
        try:
            return json.loads(MEASURED.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_cache(cache: dict[str, dict]) -> None:
    AUDIO.mkdir(exist_ok=True)
    MEASURED.write_text(json.dumps(cache, indent=2, sort_keys=True) + "\n")


def have_narration() -> bool:
    """Is there any narration in audio/ at all?"""
    return any(
        beat.audio() for scene in read_scenes() for beat in scene.beats
    )


# --- list ------------------------------------------------------------------


def cmd_list(args: argparse.Namespace) -> int:
    scenes = read_scenes()
    lines = [
        "# Narration",
        "",
        "Generated by `narrate.py list` — the lines come straight out of",
        "`scenes.py`, so this file is a view of the code, not a second copy of",
        "the script. Re-run it after any wording change.",
        "",
        "Record one file per line, named in the first column, into `audio/`.",
        f"Any of {', '.join(EXTENSIONS)} will do. Leave a moment of silence at",
        "each end if it helps you read — it gets trimmed. Beats marked *(no",
        "speech)* are music or a transition: there is nothing to record.",
        "",
    ]
    total = 0
    for scene in scenes:
        lines += [f"## {scene.name}", "", "| File | Line |", "| --- | --- |"]
        for beat in scene.beats:
            if beat.spoken:
                total += 1
                lines.append(f"| `{beat.stem}.mp3` | {beat.note} |")
            else:
                lines.append(f"| — | *(no speech)* — `{beat.note}` |")
        lines.append("")
    lines += [f"{total} lines to record, across {len(scenes)} scenes.", ""]

    AUDIO.mkdir(exist_ok=True)
    out = AUDIO / "NARRATION.md"
    out.write_text("\n".join(lines))
    print(f"{out.relative_to(HERE)}: {total} lines to record")
    return 0


# --- status ----------------------------------------------------------------


def cmd_status(args: argparse.Namespace) -> int:
    scenes = read_scenes()
    cache = load_cache()
    scratch = set(json.loads(SCRATCH_LOG.read_text())) if SCRATCH_LOG.exists() else set()

    missing = 0
    spoken = 0
    for scene in scenes:
        rows = []
        measured_total = 0.0
        for beat in scene.beats:
            if not beat.spoken:
                measured_total += beat.window
                continue
            spoken += 1
            path = beat.audio()
            if path is None:
                missing += 1
                rows.append(f"    {beat.index:2d}  {'—':>7}          missing   {beat.note[:52]}")
                measured_total += beat.window
                continue
            m = measure(path, cache)
            kind = "scratch" if path.name in scratch else "recorded"
            rows.append(
                f"    {beat.index:2d}  {m['speech']:6.2f}s  "
                f"(window {beat.window:5.2f}s)  {kind:8s}  {beat.note[:52]}"
            )
            measured_total += m["speech"] + args.pad
        print(f"{scene.name}  TARGET {scene.target:.2f}s   "
              f"re-timed would be {measured_total:.2f}s")
        print("\n".join(rows))
    save_cache(cache)

    print()
    print(f"{spoken - missing}/{spoken} lines present, {missing} missing")
    return 0


# --- scratch ---------------------------------------------------------------


def cmd_scratch(args: argparse.Namespace) -> int:
    if not SAY.exists():
        print(f"{SAY} not found — scratch narration needs macOS `say`",
              file=sys.stderr)
        return 1
    if not shutil.which("ffmpeg"):
        print("ffmpeg not found", file=sys.stderr)
        return 1

    AUDIO.mkdir(exist_ok=True)
    scratch = set(json.loads(SCRATCH_LOG.read_text())) if SCRATCH_LOG.exists() else set()
    made = kept = 0

    for scene in read_scenes():
        for beat in scene.beats:
            if not beat.spoken:
                continue
            existing = beat.audio()
            if existing is not None and not args.force:
                # Never speak over a real recording; only over our own take.
                if existing.name not in scratch:
                    kept += 1
                    continue
                if not args.refresh:
                    kept += 1
                    continue

            out = AUDIO / f"{beat.stem}.mp3"
            aiff = out.with_suffix(".scratch.aiff")
            subprocess.run(
                [str(SAY), "-v", args.voice, "-r", str(args.rate),
                 "-o", str(aiff), beat.note],
                check=True,
            )
            subprocess.run(
                ["ffmpeg", "-y", "-nostdin", "-loglevel", "error", "-i", str(aiff),
                 "-c:a", "libmp3lame", "-q:a", "4", str(out)],
                check=True,
            )
            aiff.unlink()
            scratch.add(out.name)
            made += 1
            print(f"  {out.name}  {beat.note[:60]}")

    SCRATCH_LOG.write_text(json.dumps(sorted(scratch), indent=2) + "\n")
    print(f"\nscratch narration: {made} written, {kept} left alone "
          f"(voice {args.voice}, {args.rate} wpm)")
    if kept and not args.force:
        print("real recordings are never overwritten; --refresh redoes the "
              "scratch ones, --force redoes everything")
    return 0


# --- retime ----------------------------------------------------------------


def _num(value: float) -> str:
    """Format a duration the way the beat tables already read: 2.0, 3.45."""
    text = f"{round(value, 2):.2f}".rstrip("0")
    return text + "0" if text.endswith(".") else text


def animation_costs(media_dir: str) -> dict[tuple[str, int, str], float]:
    """What each beat's animations cost in the last render, by scene and beat.

    A line can be read faster than the picture it belongs to can be drawn. A
    window trimmed to the line alone would then cut nothing — ``beat()`` just
    stops holding — but the scene would run past its slot and the pacing would
    be wrong. So a re-time never goes below what the animation needs, and the
    last render is what knows that number.

    The line is part of the key: a log left over from before a beat was added
    or reworded would otherwise hand a cost to the wrong beat.
    """
    costs: dict[tuple[str, int, str], float] = {}
    timing = Path(media_dir) / "timing"
    for log in sorted(timing.glob("*.json")):
        try:
            data = json.loads(log.read_text())
        except json.JSONDecodeError:
            continue
        for beat in data.get("beats", []):
            if "animation" in beat:
                key = (data["scene"], int(beat["index"]), beat["note"])
                costs[key] = float(beat["animation"])
    return costs


def cmd_retime(args: argparse.Namespace) -> int:
    scenes = read_scenes()
    cache = load_cache()
    costs = {} if args.no_floor else animation_costs(args.media_dir)
    source = SCENES.read_text()
    lines = source.splitlines(keepends=True)

    # (line, col, end_line, end_col, replacement), applied back to front so
    # earlier edits cannot move later ones.
    edits: list[tuple[int, int, int, int, str]] = []
    missing: list[str] = []
    floored: list[str] = []
    changed = 0

    for scene in scenes:
        total = 0.0
        for beat in scene.beats:
            if not beat.spoken:
                total += beat.window
                continue
            path = beat.audio()
            if path is None:
                missing.append(f"{beat.stem}  {beat.note[:56]}")
                total += beat.window
                continue
            window = round(measure(path, cache)["speech"] + args.pad, 2)
            floor = costs.get((scene.name, beat.index, beat.note))
            if floor is not None and floor > window:
                window = math.ceil(floor * 100) / 100
                floored.append(
                    f"{beat.stem}  {window:5.2f}s (the line runs "
                    f"{measure(path, cache)['speech']:.2f}s)  {beat.note[:40]}"
                )
            total += window
            if abs(window - beat.window) >= 0.01:
                edits.append((*beat.span, _num(window)))
                changed += 1

        total = round(total, 2)
        if scene.target_span and abs(total - scene.target) >= 0.01:
            edits.append((*scene.target_span, _num(total)))
        print(f"{scene.name}  {scene.target:6.2f}s -> {total:6.2f}s")

    save_cache(cache)

    if args.dry_run:
        print(f"\n{changed} beat windows would change (dry run)")
        return 0

    for line, col, end_line, end_col, text in sorted(edits, reverse=True):
        if line != end_line:
            raise SystemExit(f"scenes.py:{line}: number spans lines, refusing")
        row = lines[line - 1]
        lines[line - 1] = row[:col] + text + row[end_col:]

    SCENES.write_text("".join(lines))
    print(f"\nscenes.py: {changed} beat windows and {len(edits) - changed} "
          f"scene totals updated (pad {args.pad}s)")
    if floored:
        print(f"\n{len(floored)} windows are held open by their animation "
              f"rather than by the line:")
        for item in floored:
            print(f"  {item}")
    if missing:
        print(f"\n{len(missing)} lines have no recording yet and keep their "
              f"current window:")
        for item in missing:
            print(f"  {item}")
    return 0


# --- levelling ---------------------------------------------------------------

# Where the narration should sit, as a mean level in dB. Recordings often come
# off a laptop mic 15dB quieter than this, which leaves the video sounding
# faint next to anything else and puts the music bed on top of the voice.
NARRATION_DB = -21.0

# Never push a peak closer to full scale than this.
PEAK_CEILING = -1.5


def narration_gain(target: float = NARRATION_DB) -> float:
    """One gain for the whole narration, in dB.

    A single figure for every line rather than one each: the takes already sit
    within a few dB of each other, and levelling them individually would flatten
    the differences a reader puts there on purpose. The gain is held back if it
    would drive the loudest peak into the ceiling.
    """
    cache = load_cache()
    means, peaks = [], []
    for scene in read_scenes():
        for beat in scene.beats:
            path = beat.audio()
            if path is None:
                continue
            m = measure(path, cache)
            if m.get("mean") is not None:
                means.append(m["mean"])
            if m.get("peak") is not None:
                peaks.append(m["peak"])
    save_cache(cache)
    if not means:
        return 0.0

    means.sort()
    wanted = target - means[len(means) // 2]
    if peaks:
        wanted = min(wanted, PEAK_CEILING - max(peaks))
    return round(max(wanted, 0.0), 2)


# --- mix -------------------------------------------------------------------


def cmd_mix(args: argparse.Namespace) -> int:
    """Lay a scene's narration under its rendered video.

    The beat starts come from the timing log the render itself wrote, not from
    the numbers in scenes.py: if a beat's animations overran its window, the
    render is the truth and the audio has to follow it.
    """
    timing_path = Path(args.media_dir) / "timing" / f"{args.scene}.json"
    if not timing_path.exists():
        print(f"no timing log at {timing_path} — render {args.scene} first",
              file=sys.stderr)
        return 1
    timing = json.loads(timing_path.read_text())

    scenes = {s.name: s for s in read_scenes()}
    if args.scene not in scenes:
        print(f"unknown scene {args.scene}", file=sys.stderr)
        return 1
    beats = scenes[args.scene].beats
    played = timing["beats"]
    if len(played) != len(beats):
        print(f"{args.scene}: scenes.py has {len(beats)} beats but the render "
              f"played {len(played)} — re-render the scene", file=sys.stderr)
        return 1

    video = Path(args.video)
    duration = _ffprobe_duration(video)
    gain = args.gain if args.gain is not None else narration_gain()
    cache = load_cache()

    inputs: list[str] = []
    chains: list[str] = []
    labels: list[str] = []
    for beat, window in zip(beats, played):
        path = beat.audio()
        if path is None:
            continue
        m = measure(path, cache)
        start = float(window["start"])
        room = float(window["end"]) - start
        if m["speech"] > room + 0.05:
            print(f"  ! {args.scene} beat {beat.index}: line is "
                  f"{m['speech']:.2f}s but its window is only {room:.2f}s — "
                  f"re-run `narrate.py retime`", file=sys.stderr)

        # Input 0 is the video, so this clip is stream len(labels) + 1.
        stream = len(labels) + 1
        inputs += ["-i", str(path)]
        label = f"a{stream}"
        labels.append(label)
        chains.append(
            f"[{stream}:a]"
            f"atrim=start={m['start']:.4f}:end={m['end']:.4f},"
            f"asetpts=N/SR/TB,"
            f"{CLEANUP},"
            f"volume={gain}dB,"
            f"aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
            f"adelay={int(round(start * 1000))}:all=1"
            f"[{label}]"
        )
    save_cache(cache)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    # Mix onto a silence the length of the scene. It anchors the result at
    # t=0 and fixes its length, which matters when the first line does not
    # start at the top of the scene: given only delayed inputs, amix hands the
    # encoder timestamps that run backwards and the track comes out empty. It
    # also gives a scene with no narration at all a track of the right length,
    # so the concat at the end sees the same streams on every segment.
    base = (
        f"anullsrc=channel_layout=stereo:sample_rate=48000,"
        f"atrim=end={duration:.4f},asetpts=N/SR/TB[base]"
    )
    graph = ";".join([base] + chains) + ";" + (
        "[base]" + "".join(f"[{l}]" for l in labels)
        + f"amix=inputs={len(labels) + 1}:normalize=0:dropout_transition=0[aout]"
    )

    subprocess.run(
        ["ffmpeg", "-y", "-nostdin", "-loglevel", "error", "-i", str(video),
         *inputs, "-filter_complex", graph,
         "-map", "0:v", "-map", "[aout]",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-t", f"{duration:.4f}", str(out)],
        check=True,
    )

    # ffmpeg can build a broken filter graph, write a track a fraction of a
    # second long, and still exit 0 — so a zero exit code is not the check.
    # The track has to be as long as the picture it goes under.
    got = _stream_duration(out, "a")
    if got is None or abs(got - duration) > 0.2:
        print(f"{args.scene}: the mixed audio is {got}s against {duration:.2f}s "
              f"of video — the mix is wrong, not the recording", file=sys.stderr)
        return 1

    lift = f", lifted {gain:+.1f}dB" if gain else ""
    print(f"  {args.scene}: {len(labels)} lines laid under {duration:.2f}s{lift}")
    return 0


# --- serve -----------------------------------------------------------------


def cmd_serve(args: argparse.Namespace) -> int:
    """Open the recording booth, on this version.

    The booth itself lives one level up, at ../recorder, and serves every
    version of the video — it is not part of this directory any more. This is
    the shorthand for ``../record.sh --project simplified``.
    """
    sys.path.insert(0, str(HERE.parent))
    try:
        from recorder.server import serve
    except ModuleNotFoundError:
        print(f"the booth is not where it should be: {HERE.parent / 'recorder'}",
              file=sys.stderr)
        return 1

    return serve(port=args.port, open_browser=not args.no_open,
                 default=HERE.name)


# --- cli -------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="write audio/NARRATION.md: what to record")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("status", help="what is in audio/, and how long it runs")
    p.add_argument("--pad", type=float, default=DEFAULT_PAD)
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("scratch", help="stand-in narration via macOS `say`")
    p.add_argument("--voice", default=SCRATCH_VOICE)
    p.add_argument("--rate", type=int, default=SCRATCH_RATE,
                   help=f"words per minute (default {SCRATCH_RATE})")
    p.add_argument("--refresh", action="store_true",
                   help="redo lines this tool generated earlier")
    p.add_argument("--force", action="store_true",
                   help="redo every line, real recordings included")
    p.set_defaults(func=cmd_scratch)

    p = sub.add_parser("retime", help="beat windows and TARGET <- real lengths")
    p.add_argument("--pad", type=float, default=DEFAULT_PAD,
                   help=f"seconds of breathing room after each line "
                        f"(default {DEFAULT_PAD})")
    p.add_argument("--no-floor", action="store_true",
                   help="let a window shrink below what its animation costs")
    p.add_argument("--media-dir", default="media",
                   help="where the render left its beat timing logs")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_retime)

    p = sub.add_parser("mix", help="lay a scene's narration under its video")
    p.add_argument("scene")
    p.add_argument("video")
    p.add_argument("out")
    p.add_argument("--media-dir", default="media")
    p.add_argument("--gain", type=float, default=None,
                   help="dB to lift the narration by (default: work it out)")
    p.set_defaults(func=cmd_mix)

    p = sub.add_parser("serve", help="the recording booth, in a browser")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--no-open", action="store_true",
                   help="do not open a browser window")
    p.set_defaults(func=cmd_serve)

    p = sub.add_parser("have-narration",
                       help="exit 0 if audio/ holds any narration")
    p.set_defaults(func=lambda a: 0 if have_narration() else 1)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
