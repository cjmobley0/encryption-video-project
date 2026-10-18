"""A local recording booth for the narration, served at localhost.

One line at a time, with the animation it belongs to playing beside it: the
countdown ends, the picture starts and recording starts together, so the read
is paced by what the viewer will see rather than by a stopwatch.

The booth serves every version of the video at once — Professional by default,
Simplified beside it — and the picker in the top left switches between them
without restarting anything. Everything it knows about a script comes from
that version's own ``narrate.py``, the same parse of its ``scenes.py`` that the
re-timer and the mixdown use, so the booth cannot show a line the animation
does not actually say. See ``projects.py`` for how a version is found.

    ./record.sh                     # the booth, on the default version
    ./record.sh --project simplified

Only the filenames a version's narrate.py derives from its scenes.py can be
written, and only into that version's audio/. Nothing else on disk is
reachable from the page.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import threading
import webbrowser
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from recorder import projects  # noqa: E402
from recorder.projects import Project  # noqa: E402

STATIC = HERE / "static"

# What a browser hands us, by what MediaRecorder picked.
RAW_SUFFIX = {
    "audio/webm": ".webm",
    "audio/ogg": ".ogg",
    "audio/mp4": ".m4a",
    "audio/mpeg": ".mp3",
    "audio/wav": ".wav",
}

MIME = {
    ".html": "text/html; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".mp4": "video/mp4",
    ".mp3": "audio/mpeg",
    ".json": "application/json",
}


def takes_dir(project: Project) -> Path:
    return project.narrate.AUDIO / "takes"


def take_log_path(project: Project) -> Path:
    return project.narrate.AUDIO / ".takes.json"


# --- what the page needs to know -------------------------------------------


def take_log(project: Project) -> dict[str, dict]:
    path = take_log_path(project)
    if path.exists():
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_take_log(project: Project, log: dict[str, dict]) -> None:
    project.narrate.AUDIO.mkdir(exist_ok=True)
    take_log_path(project).write_text(json.dumps(log, indent=2, sort_keys=True) + "\n")


def clip_windows(project: Project, scene: str) -> list[dict]:
    path = project.media_dir / "timing" / f"{scene}.json"
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text()).get("beats", [])
    except json.JSONDecodeError:
        return []


def scene_video(project: Project, scene: str) -> Path | None:
    """The most recently rendered video for a scene, whatever quality."""
    root = project.media_dir / "videos" / "scenes"
    found = sorted(root.glob(f"*/{scene}.mp4"), key=lambda p: p.stat().st_mtime)
    return found[-1] if found else None


def state(project: Project) -> dict:
    """Every beat, with its target, its clip window and what is recorded."""
    narrate = project.narrate
    scenes = narrate.read_scenes()
    budgets = narrate.budgets_by_beat(scenes)
    costs = narrate.animation_costs(str(project.media_dir))
    cache = narrate.load_cache()
    scratch = set()
    if narrate.SCRATCH_LOG.exists():
        try:
            scratch = set(json.loads(narrate.SCRATCH_LOG.read_text()))
        except json.JSONDecodeError:
            pass
    log = take_log(project)

    out_scenes = []
    missing_render = []
    for scene in scenes:
        played = clip_windows(project, scene.name)
        video = scene_video(project, scene.name)
        if video is None or len(played) != len(scene.beats):
            missing_render.append(scene.name)
        beats = []
        for i, beat in enumerate(scene.beats):
            window = played[i] if i < len(played) else None
            path = beat.audio()
            entry = {
                "stem": beat.stem,
                "scene": scene.name,
                "index": beat.index,
                "line": beat.note,
                "spoken": beat.spoken,
                "budget": budgets.get((scene.name, beat.index)),
                "floor": costs.get((scene.name, beat.index, beat.note)),
                "clipStart": float(window["start"]) if window else None,
                "clipEnd": float(window["end"]) if window else None,
                "status": "missing",
                "duration": None,
                "speech": None,
                "trimStart": None,
                "device": None,
                "recordedAt": None,
            }
            if path is not None:
                m = narrate.measure(path, cache)
                entry["status"] = "scratch" if path.name in scratch else "recorded"
                entry["file"] = path.name
                entry["duration"] = m["duration"]
                entry["speech"] = m["speech"]
                entry["trimStart"] = m["start"]
                meta = log.get(beat.stem, {})
                entry["device"] = meta.get("device")
                entry["recordedAt"] = meta.get("at")
            beats.append(entry)
        out_scenes.append({
            "name": scene.name,
            "target": scene.target,
            "video": f"/api/clip/{project.key}/{scene.name}" if video else None,
            "beats": beats,
        })
    narrate.save_cache(cache)

    spoken = [b for s in out_scenes for b in s["beats"] if b["spoken"]]
    return {
        "project": project.as_json(),
        "scenes": out_scenes,
        "counts": {
            "spoken": len(spoken),
            "recorded": sum(1 for b in spoken if b["status"] == "recorded"),
            "scratch": sum(1 for b in spoken if b["status"] == "scratch"),
            "missing": sum(1 for b in spoken if b["status"] == "missing"),
        },
        "needsRender": missing_render,
    }


def empty_state(project: Project) -> dict:
    """What a version that has not been built yet reports.

    The picker still offers it, so the page has to be able to show it: no
    scenes, nothing recorded, and the reason in `detail`.
    """
    return {
        "project": project.as_json(),
        "scenes": [],
        "counts": {"spoken": 0, "recorded": 0, "scratch": 0, "missing": 0},
        "needsRender": [],
    }


# --- saving a take ----------------------------------------------------------


def known_stems(project: Project) -> dict[str, object]:
    return {
        b.stem: b
        for scene in project.narrate.read_scenes()
        for b in scene.beats
        if b.spoken
    }


def save_take(project: Project, stem: str, blob: bytes, content_type: str,
              device: str) -> dict:
    """Write a browser recording into audio/ as mp3, keeping the raw take.

    The raw file is kept because the transcode is the only lossy step here and
    a bad one should never cost somebody their read.
    """
    narrate = project.narrate
    beat = known_stems(project).get(stem)
    if beat is None:
        raise KeyError(stem)

    suffix = RAW_SUFFIX.get(content_type.split(";")[0].strip(), ".webm")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    raw_dir = takes_dir(project) / stem
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw = raw_dir / f"{stamp}{suffix}"
    raw.write_bytes(blob)

    out = narrate.AUDIO / f"{stem}.mp3"
    # Mono at 48k: it is one voice, and the mixdown lays it out to stereo.
    subprocess.run(
        ["ffmpeg", "-y", "-nostdin", "-loglevel", "error", "-i", str(raw),
         "-ac", "1", "-ar", "48000", "-c:a", "libmp3lame", "-q:a", "2",
         str(out)],
        check=True,
    )
    # Any earlier recording of this line in another format would still be
    # found first by narrate.Beat.audio(), so clear those out.
    for ext in narrate.EXTENSIONS:
        stale = narrate.AUDIO / (stem + ext)
        if ext != ".mp3" and stale.exists():
            stale.unlink()

    log = take_log(project)
    log[stem] = {
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "device": device,
        "raw": str(raw.relative_to(narrate.AUDIO)),
        "contentType": content_type,
    }
    save_take_log(project, log)

    # A freshly written file must not read as the one we measured before.
    cache = narrate.load_cache()
    cache.pop(out.name, None)
    m = narrate.measure(out, cache)
    narrate.save_cache(cache)

    scratch_path = narrate.SCRATCH_LOG
    if scratch_path.exists():
        try:
            scratch = set(json.loads(scratch_path.read_text()))
        except json.JSONDecodeError:
            scratch = set()
        if out.name in scratch:
            scratch.discard(out.name)
            scratch_path.write_text(json.dumps(sorted(scratch), indent=2) + "\n")

    return {"stem": stem, "duration": m["duration"], "speech": m["speech"],
            "trimStart": m["start"]}


def restore_previous(project: Project, stem: str) -> dict:
    """Put the take before this one back, if there is one."""
    narrate = project.narrate
    raw_dir = takes_dir(project) / stem
    takes = sorted(raw_dir.glob("*")) if raw_dir.exists() else []
    if len(takes) < 2:
        raise FileNotFoundError(stem)
    takes[-1].unlink()
    previous = takes[-2]
    out = narrate.AUDIO / f"{stem}.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-nostdin", "-loglevel", "error", "-i", str(previous),
         "-ac", "1", "-ar", "48000", "-c:a", "libmp3lame", "-q:a", "2",
         str(out)],
        check=True,
    )
    cache = narrate.load_cache()
    cache.pop(out.name, None)
    m = narrate.measure(out, cache)
    narrate.save_cache(cache)
    return {"stem": stem, "duration": m["duration"], "speech": m["speech"],
            "restored": previous.name}


# --- http -------------------------------------------------------------------


class Booth(ThreadingHTTPServer):
    """A server that does not shout when a browser hangs up.

    Keep-alive connections are dropped by the browser all the time — closing a
    tab, seeking away from a clip, or just letting an idle socket lapse — and
    socketserver's default is to print a full traceback for each one. They are
    not faults, and burying real errors under them helps nobody.
    """

    daemon_threads = True

    def handle_error(self, request, client_address) -> None:
        kind = sys.exc_info()[0]
        if kind is not None and issubclass(
            kind, (ConnectionResetError, BrokenPipeError, ConnectionAbortedError)
        ):
            return
        super().handle_error(request, client_address)


class Handler(BaseHTTPRequestHandler):
    server_version = "NarrationBooth/2.0"
    # Seeking a clip costs dozens of range requests; keep-alive spares them a
    # new connection each. Every response here sends a Content-Length, which
    # is what HTTP/1.1 needs to frame them.
    protocol_version = "HTTP/1.1"
    default_project = ""

    def log_message(self, fmt: str, *args) -> None:
        if "/api/clip/" in (self.path or ""):
            return  # video range requests, dozens per seek
        sys.stderr.write(f"  {self.address_string()} {fmt % args}\n")

    # -- helpers

    def _json(self, payload: dict, status: int = HTTPStatus.OK) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _error(self, status: int, message: str) -> None:
        self._json({"error": message}, status)

    def _project(self, key: str) -> Project | None:
        """The version a route names, or None once the error is sent."""
        project = projects.by_key(key) if key else None
        if project is None:
            self._error(HTTPStatus.NOT_FOUND, f"no such version: {key}")
            return None
        return project

    def _send_file(self, path: Path, *, ranged: bool = False) -> None:
        if not path.is_file():
            return self._error(HTTPStatus.NOT_FOUND, f"no such file: {path.name}")
        ctype = MIME.get(path.suffix, "application/octet-stream")
        size = path.stat().st_size
        rng = self.headers.get("Range") if ranged else None

        start, end = 0, size - 1
        status = HTTPStatus.OK
        if rng:
            m = re.match(r"bytes=(\d*)-(\d*)", rng)
            if m:
                if m.group(1):
                    start = int(m.group(1))
                    end = int(m.group(2)) if m.group(2) else size - 1
                elif m.group(2):            # bytes=-N, the last N bytes
                    start = max(0, size - int(m.group(2)))
                if start >= size:
                    self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                    self.send_header("Content-Range", f"bytes */{size}")
                    self.end_headers()
                    return
                end = min(end, size - 1)
                status = HTTPStatus.PARTIAL_CONTENT

        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(end - start + 1))
        if ranged:
            self.send_header("Accept-Ranges", "bytes")
        if status == HTTPStatus.PARTIAL_CONTENT:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        with path.open("rb") as fh:
            fh.seek(start)
            remaining = end - start + 1
            while remaining > 0:
                chunk = fh.read(min(64 * 1024, remaining))
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    return      # the player seeked away; nothing to clean up
                remaining -= len(chunk)

    # -- routes

    def do_GET(self) -> None:
        route = unquote(urlparse(self.path).path)

        if route in ("/", "/index.html"):
            return self._send_file(STATIC / "index.html")
        if route in ("/app.js", "/app.css"):
            return self._send_file(STATIC / route.lstrip("/"))

        if route == "/api/projects":
            found = projects.discover()
            chosen = projects.by_key(self.default_project) if self.default_project \
                else projects.default(found)
            return self._json({
                "projects": [p.as_json() for p in found],
                "default": chosen.key if chosen else None,
            })

        if route.startswith("/api/state/"):
            project = self._project(route[len("/api/state/"):])
            if project is None:
                return
            if not project.ready:
                return self._json(empty_state(project))
            try:
                return self._json(state(project))
            except SystemExit as exc:            # narrate.py refused to parse
                return self._error(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

        if route.startswith("/api/clip/"):
            key, _, scene = route[len("/api/clip/"):].partition("/")
            project = self._project(key)
            if project is None:
                return
            if not project.ready or scene not in project.scene_names():
                return self._error(HTTPStatus.NOT_FOUND, f"no scene {scene}")
            video = scene_video(project, scene)
            if video is None:
                return self._error(HTTPStatus.NOT_FOUND, f"no render for {scene}")
            return self._send_file(video, ranged=True)

        if route.startswith("/api/audio/"):
            key, _, stem = route[len("/api/audio/"):].partition("/")
            project = self._project(key)
            if project is None:
                return
            beat = known_stems(project).get(stem) if project.ready else None
            if beat is None:
                return self._error(HTTPStatus.NOT_FOUND, "unknown line")
            path = beat.audio()
            if path is None:
                return self._error(HTTPStatus.NOT_FOUND, "nothing recorded")
            return self._send_file(path, ranged=True)

        return self._error(HTTPStatus.NOT_FOUND, "no such route")

    def _take_route(self) -> tuple[Project | None, str]:
        route = unquote(urlparse(self.path).path)
        if not route.startswith("/api/take/"):
            self._error(HTTPStatus.NOT_FOUND, "no such route")
            return None, ""
        key, _, stem = route[len("/api/take/"):].partition("/")
        project = self._project(key)
        if project is None:
            return None, ""
        if not project.ready:
            self._error(HTTPStatus.NOT_FOUND, project.detail)
            return None, ""
        return project, stem

    def do_POST(self) -> None:
        project, stem = self._take_route()
        if project is None:
            return

        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return self._error(HTTPStatus.BAD_REQUEST, "empty recording")
        if length > 64 * 1024 * 1024:
            return self._error(HTTPStatus.BAD_REQUEST, "recording too large")
        blob = self.rfile.read(length)
        ctype = self.headers.get("Content-Type", "audio/webm")
        device = self.headers.get("X-Input-Device", "")

        try:
            result = save_take(project, stem, blob, ctype, device)
        except KeyError:
            return self._error(HTTPStatus.NOT_FOUND, f"unknown line: {stem}")
        except subprocess.CalledProcessError:
            return self._error(HTTPStatus.INTERNAL_SERVER_ERROR,
                               "ffmpeg could not read that recording")
        return self._json(result)

    def do_DELETE(self) -> None:
        project, stem = self._take_route()
        if project is None:
            return
        try:
            return self._json(restore_previous(project, stem))
        except FileNotFoundError:
            return self._error(HTTPStatus.NOT_FOUND, "no earlier take to go back to")
        except subprocess.CalledProcessError:
            return self._error(HTTPStatus.INTERNAL_SERVER_ERROR, "ffmpeg failed")


def serve(port: int = 8765, open_browser: bool = True,
          default: str = "") -> int:
    """Open the booth. `default` names the version it opens on."""
    if not shutil.which("ffmpeg"):
        print("ffmpeg not found — the booth needs it to save takes", file=sys.stderr)
        return 1
    if not (STATIC / "index.html").exists():
        print(f"missing {STATIC / 'index.html'}", file=sys.stderr)
        return 1

    found = projects.discover()
    if not found:
        print(f"no video directories found in {projects.ROOT}", file=sys.stderr)
        return 1

    chosen = projects.by_key(default) if default else projects.default(found)
    if chosen is None:
        print(f"no such version: {default}", file=sys.stderr)
        print(f"  try one of: {', '.join(p.key for p in found)}", file=sys.stderr)
        return 1

    Handler.default_project = chosen.key
    httpd = Booth(("127.0.0.1", port), Handler)
    url = f"http://localhost:{port}/"

    print(f"Narration booth: {url}")
    for project in found:
        mark = "→" if project is chosen or project.key == chosen.key else " "
        if not project.ready:
            print(f"  {mark} {project.label}: {project.detail}")
            continue
        snapshot = state(project)
        counts = snapshot["counts"]
        print(f"  {mark} {project.label}: {counts['recorded']} recorded, "
              f"{counts['scratch']} scratch, {counts['missing']} not yet done")
        if snapshot["needsRender"]:
            print(f"      no current render for: {', '.join(snapshot['needsRender'])}")
            print(f"      run {project.name}/render.sh so the booth can show "
                  f"the animation")
    print("  ctrl-c to stop")

    if open_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        httpd.server_close()
    return 0
