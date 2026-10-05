#!/usr/bin/env bash
set -euo pipefail
: "${IDF_PATH:=/workspaces/time-series-ai-esp32s3/.tooling/esp-idf}"
source "$IDF_PATH/export.sh" >/dev/null
mkdir -p outputs/release
qemu_bin="$(scripts/install-pinned-qemu.sh)"
scripts/build-firmware.sh
export PATH="$(dirname "${qemu_bin}"):${PATH}"
python3 scripts/capture-qemu-uart.py \
  --log outputs/release/qemu-uart.log \
  --deadline 90 \
  -- idf.py -C firmware -B firmware/build/qemu-reference qemu
python3 scripts/parse-qemu-uart.py outputs/release/qemu-uart.log > outputs/release/qemu-parser-evidence.json

