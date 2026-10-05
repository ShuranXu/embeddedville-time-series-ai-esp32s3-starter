#!/usr/bin/env bash
set -euo pipefail
: "${IDF_PATH:=/workspaces/time-series-ai-esp32s3/.tooling/esp-idf}"
source "$IDF_PATH/export.sh" >/dev/null
idf.py -C firmware set-target esp32s3
idf.py -C firmware build

