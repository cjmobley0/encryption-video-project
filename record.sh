#!/usr/bin/env bash
# Open the narration booth in a browser: one line at a time, with the
# animation it belongs to playing beside it.
#
#   ./record.sh                       # the Professional cut (the default)
#   ./record.sh --project simplified  # the Simplified cut
#   ./record.sh --list                # which versions it can record for
#   ./record.sh --port 8800 --no-open
#
# Takes land in <Version>/audio/, named after the beat they belong to. The
# booth needs a render to exist so it can show you the picture — run that
# version's ./render.sh first. See README.md.

set -euo pipefail
cd "$(dirname "$0")"
exec python3 recorder/serve.py "$@"
