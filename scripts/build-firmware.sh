#!/usr/bin/env bash
set -euo pipefail
: "${IDF_PATH:=/workspaces/time-series-ai-esp32s3/.tooling/esp-idf}"
source "$IDF_PATH/export.sh" >/dev/null
idf.py -C firmware reconfigure >/dev/null
scripts/apply-espdl-reference-profile.sh firmware/managed_components/espressif__esp-dl
idf.py -C firmware -B firmware/build/qemu-reference \
  -D SDKCONFIG=firmware/build/qemu-reference/sdkconfig \
  -D 'SDKCONFIG_DEFAULTS=sdkconfig.defaults;sdkconfig.qemu-reference.defaults' \
  set-target esp32s3
idf.py -C firmware -B firmware/build/qemu-reference build

elf=firmware/build/qemu-reference/time_series_ai_esp32s3.elf
map_file=firmware/build/qemu-reference/time_series_ai_esp32s3.map
source_manifest=firmware/build/qemu-reference/esp-idf/espressif__esp-dl/dl_compile_srcs.cmake
if xtensa-esp32s3-elf-nm --defined-only "${elf}" | grep -Eiq '(^|[[:space:]])(dl_)?tie728'; then
  echo "Reference ELF exports an ESP32-S3 PIE/TIE kernel symbol." >&2
  exit 1
fi
if grep -Eiq 'dl/base/isa/tie728|dl_tie728' "${map_file}" "${source_manifest}"; then
  echo "Reference link includes an ESP32-S3 PIE/TIE kernel object." >&2
  exit 1
fi

