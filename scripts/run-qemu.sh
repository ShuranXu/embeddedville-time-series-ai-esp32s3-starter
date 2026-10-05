#!/usr/bin/env bash
set -euo pipefail
: "${IDF_PATH:=/workspaces/time-series-ai-esp32s3/.tooling/esp-idf}"
source "$IDF_PATH/export.sh" >/dev/null
mkdir -p outputs/release
set +e
timeout 45s idf.py -C firmware qemu --qemu-extra-args "-nographic" 2>&1 | tee outputs/release/qemu-uart.log
status=${PIPESTATUS[0]}
set -e
grep -q '"event":"course_summary"' outputs/release/qemu-uart.log
grep -q '"passed":true' outputs/release/qemu-uart.log
test "$status" -eq 0 -o "$status" -eq 124

