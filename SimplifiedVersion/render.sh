#!/usr/bin/env bash
# Render every scene of encryption-video-plan.md and stitch them into one file.
#
#   ./render.sh          # 480p15 preview, fast
#   ./render.sh -qh      # 1080p60 final
#   ./render.sh -qk      # 4K60
#
# Output: renders/encryption-full.mp4, plus the individual scenes under
# media/videos/scenes/<resolution>/.
#
# Audio is picked up if it is there and ignored if it is not:
#
#   audio/sceneNN_beatMM.mp3   one line of narration, laid under its own beat
#   audio/music.mp3            a bed, mixed under the whole cut at MUSIC_GAIN
#
# With an empty audio/ this renders exactly the silent cut it always has.
# See the README's "Adding the narration" section, and narrate.py.

set -euo pipefail
cd "$(dirname "$0")"

QUALITY="${1:--ql}"
VENV="$PWD/.venv/bin"
OUT_DIR="renders"
MUSIC="audio/music.mp3"
# Where the music bed sits, as a mean level in dB. The narration runs around
# -20 dB, so -34 puts the bed well under it. This is a target, not a trim: the
# bed is measured and scaled to it, so a quiet export does not vanish and a
# loud one does not sit on top of the voice.
MUSIC_DB="${MUSIC_DB:--34}"

if [[ ! -x "$VENV/manim" ]]; then
  echo "manim not found in $VENV — create the venv first (see README.md)" >&2
  exit 1
fi

SCENES=(
  Scene01Intro
  Scene02Ciphertext
  Scene03LockedBox
  Scene04Math
  Scene05Symmetric
  Scene06Asymmetric
  Scene07Https
  Scene08Everyday
  Scene09NotMagic
  Scene10Outro
)

case "$QUALITY" in
  -ql) RES_DIR="480p15";  FPS=15 ;;
  -qm) RES_DIR="720p30";  FPS=30 ;;
  -qh) RES_DIR="1080p60"; FPS=60 ;;
  -qp) RES_DIR="1440p60"; FPS=60 ;;
  -qk) RES_DIR="2160p60"; FPS=60 ;;
  *) echo "unknown quality flag: $QUALITY (use -ql, -qm, -qh, -qp or -qk)" >&2; exit 1 ;;
esac

# Is there narration to lay under the scenes? narrate.py reads the beat lines
# out of scenes.py and answers for the whole cut.
NARRATION=0
if "$VENV/python" narrate.py have-narration; then
  NARRATION=1
  echo "narration found in audio/ — mixing it in"
fi

mkdir -p "$OUT_DIR"
LIST="$OUT_DIR/.concat.txt"
: > "$LIST"
if (( NARRATION )); then
  MIX_DIR="$OUT_DIR/.scenes-with-audio/$RES_DIR"
  mkdir -p "$MIX_DIR"
fi

for scene in "${SCENES[@]}"; do
  echo "--- $scene"
  "$VENV/manim" "$QUALITY" --disable_caching --media_dir media scenes.py "$scene"
  produced="media/videos/scenes/$RES_DIR/$scene.mp4"
  if [[ ! -f "$produced" ]]; then
    echo "expected output missing: $produced" >&2
    exit 1
  fi
  if (( NARRATION )); then
    # Each line goes under the beat it belongs to, using the beat starts the
    # render itself just logged to media/timing/.
    "$VENV/python" narrate.py mix "$scene" "$produced" "$MIX_DIR/$scene.mp4" \
      --media-dir media
    produced="$MIX_DIR/$scene.mp4"
  fi
  echo "file '$PWD/$produced'" >> "$LIST"
done

FULL="$OUT_DIR/encryption-full.mp4"
echo "--- stitching $FULL"
# Every scene comes from the same encoder at the same size, so a stream copy
# would do; re-encoding keeps one consistent GOP structure across the cut.
if (( NARRATION )); then
  ffmpeg -y -loglevel error -f concat -safe 0 -i "$LIST" \
    -r "$FPS" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k "$FULL"
else
  ffmpeg -y -loglevel error -f concat -safe 0 -i "$LIST" \
    -r "$FPS" -c:v libx264 -crf 18 -pix_fmt yuv420p "$FULL"
fi
rm -f "$LIST"

if [[ -f "$MUSIC" ]]; then
  echo "--- mixing $MUSIC under the cut"
  DUR=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$FULL")
  FADE_OUT=$(awk -v d="$DUR" 'BEGIN { printf "%.3f", (d > 3 ? d - 3 : 0) }')
  # How loud the track is to begin with, so it can be scaled to MUSIC_DB.
  MEAN=$(ffmpeg -nostdin -v info -i "$MUSIC" -af volumedetect -f null - 2>&1 \
         | sed -n 's/.*mean_volume: \(-*[0-9.]*\) dB.*/\1/p' | tail -1)
  if [[ -z "$MEAN" ]]; then
    echo "    could not measure $MUSIC — mixing it in untouched" >&2
    TRIM=0
  else
    TRIM=$(awk -v m="$MEAN" -v t="$MUSIC_DB" 'BEGIN { printf "%.2f", t - m }')
    echo "    track is ${MEAN} dB mean; trimming ${TRIM} dB to sit at ${MUSIC_DB} dB"
  fi
  BED="[1:a]volume=${TRIM}dB,afade=t=in:d=2,afade=t=out:st=$FADE_OUT:d=3"
  BED="$BED,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo"
  WITH_MUSIC="$OUT_DIR/.with-music.mp4"
  if (( NARRATION )); then
    # duration=first keeps the bed from outliving the picture.
    GRAPH="$BED[bed];[0:a][bed]amix=inputs=2:duration=first:normalize=0[aout]"
  else
    GRAPH="$BED,atrim=end=$DUR[aout]"
  fi
  # The bed loops, so a short track still covers the whole cut.
  ffmpeg -y -loglevel error -i "$FULL" -stream_loop -1 -i "$MUSIC" \
    -filter_complex "$GRAPH" -map 0:v -map "[aout]" \
    -c:v copy -c:a aac -b:a 192k -t "$DUR" "$WITH_MUSIC"
  mv "$WITH_MUSIC" "$FULL"
fi

echo
echo "Done: $FULL"
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$FULL" \
  | awk '{printf "Runtime: %d:%02d  (plan: 3:28 of animation)\n", $1/60, $1%60}'
