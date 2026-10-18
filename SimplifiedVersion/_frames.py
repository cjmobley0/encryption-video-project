"""Pull a strip of sample frames out of a render, for checking a scene.

    .venv/bin/python _frames.py Scene02Ciphertext 8
"""
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent / "media" / "frames"


def grab(scene: str, n: int = 8, quality: str = "480p15") -> Path:
    src = Path(f"media/videos/scenes/{quality}/{scene}.mp4")
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(src)],
        capture_output=True, text=True, check=True).stdout.strip())
    OUT.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = dur * (i + 0.5) / n
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}",
                        "-i", str(src), "-frames:v", "1",
                        str(OUT / f"tile_{i:03d}.png")], check=True)
    sheet = OUT / f"{scene}_sheet.png"
    cols = 2
    rows = (n + cols - 1) // cols
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1",
         "-i", str(OUT / "tile_%03d.png"),
         "-vf", f"scale=720:-1,tile={cols}x{rows}:margin=8:padding=8:color=0x101820",
         "-frames:v", "1", str(sheet)], check=True)
    print(f"{scene}: {dur:.2f}s -> {sheet}")
    return sheet


if __name__ == "__main__":
    grab(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8)
