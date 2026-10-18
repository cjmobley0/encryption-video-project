"""The videos the booth can record for, and how it reaches into each one.

Each video is a self-contained directory next to this one — ``scenes.py`` for
the animation, ``narrate.py`` for the narration pipeline, ``audio/`` for the
takes, ``media/`` for what Manim rendered. The booth owns none of that. It
loads a video's own ``narrate.py`` and asks it, so the recording list, the beat
windows and the file names can never drift from the animation that version
actually plays.

Two versions are loaded as two separate modules, by file path, under names of
their own. ``narrate.py`` resolves everything from the file it is in — audio,
scenes, the measurement cache — so one process can hold both without either
one's paths leaking into the other.

Professional is the default; Simplified was the proof of concept. A version
that has not been built yet still shows up in the picker, marked, rather than
disappearing from it: a missing scenes.py is a stage of the work, not an error.
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parent.parent

# The order they are offered in. Anything else found alongside them is listed
# after, alphabetically.
PREFERRED = ("ProfessionalVersion", "SimplifiedVersion")

LABELS = {
    "ProfessionalVersion": "Professional",
    "SimplifiedVersion": "Simplified",
}


@dataclass
class Project:
    key: str                  # "professional" — what the page and URL use
    name: str                 # "ProfessionalVersion" — the directory
    label: str                # "Professional" — what the picker shows
    dir: Path
    detail: str = ""          # why it is not ready, when it is not

    @property
    def ready(self) -> bool:
        return not self.detail

    @property
    def media_dir(self) -> Path:
        """Absolute: the booth runs from the root, not from inside a version."""
        return self.dir / "media"

    @property
    def narrate(self) -> ModuleType:
        """That version's own narration module, loaded once and kept."""
        return _load(self)

    def scene_names(self) -> set[str]:
        return {scene.name for scene in self.narrate.read_scenes()}

    def as_json(self) -> dict:
        return {
            "key": self.key,
            "name": self.name,
            "label": self.label,
            "ready": self.ready,
            "detail": self.detail,
        }


_loaded: dict[str, ModuleType] = {}


def _load(project: Project) -> ModuleType:
    if project.key in _loaded:
        return _loaded[project.key]
    path = project.dir / "narrate.py"
    # A name of its own per version, so the second import does not hand back
    # the first version's module — and its paths — out of sys.modules.
    mod_name = f"_narrate_{project.key}"
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise FileNotFoundError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    _loaded[project.key] = module
    return module


def _why_not_ready(folder: Path) -> str:
    missing = [f for f in ("scenes.py", "narrate.py") if not (folder / f).exists()]
    if missing:
        return f"no {' or '.join(missing)} in {folder.name}/ yet"
    return ""


def discover() -> list[Project]:
    """Every version directory next to the booth, the preferred ones first."""
    folders = {
        p.name: p
        for p in sorted(ROOT.iterdir())
        if p.is_dir()
        and not p.name.startswith(".")
        and p.name != "recorder"
        and (p.name in PREFERRED or (p / "scenes.py").exists())
    }
    order = [n for n in PREFERRED if n in folders]
    order += [n for n in folders if n not in PREFERRED]

    out = []
    for name in order:
        folder = folders[name]
        out.append(Project(
            key=name.replace("Version", "").lower(),
            name=name,
            label=LABELS.get(name, name.replace("Version", "")),
            dir=folder,
            detail=_why_not_ready(folder),
        ))
    return out


def by_key(key: str) -> Project | None:
    """Find a version by its key, its directory name or its label."""
    wanted = key.strip().lower().replace("version", "")
    for project in discover():
        if wanted in (project.key, project.name.lower(), project.label.lower()):
            return project
    return None


def default(projects: list[Project] | None = None) -> Project | None:
    """Professional, unless it has not been built yet.

    Falling back rather than opening an empty booth: the picker still says
    which version is showing, and the page says why it is not the default one.
    """
    projects = projects if projects is not None else discover()
    for project in projects:
        if project.ready:
            return project
    return projects[0] if projects else None
