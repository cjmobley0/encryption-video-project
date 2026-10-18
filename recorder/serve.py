"""Open the narration booth, for whichever version of the video you are on.

    python3 recorder/serve.py                       # the default version
    python3 recorder/serve.py --project simplified
    python3 recorder/serve.py --list

``./record.sh`` from the repository root is the same thing, shorter. Nothing
outside the standard library is needed — `ffmpeg` on PATH is the one
requirement, for saving takes — so this runs on the system python without a
virtualenv. See server.py for the booth itself and projects.py for how a
version is found.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from recorder import projects  # noqa: E402
from recorder.server import serve  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-p", "--project", default="",
                        help="which version to open on (default: Professional, "
                             "or the first one that is built)")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-open", action="store_true",
                        help="do not open a browser window")
    parser.add_argument("--list", action="store_true",
                        help="print the versions the booth can record for")
    args = parser.parse_args(argv)

    if args.list:
        found = projects.discover()
        chosen = projects.default(found)
        for project in found:
            mark = "→" if chosen and project.key == chosen.key else " "
            note = project.detail or f"{project.name}/"
            print(f"  {mark} {project.key:<14} {project.label:<14} {note}")
        return 0

    return serve(port=args.port, open_browser=not args.no_open,
                 default=args.project)


if __name__ == "__main__":
    sys.exit(main())
